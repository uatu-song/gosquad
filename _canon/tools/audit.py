#!/usr/bin/env python3
"""
audit.py — THE canon audit. One command. First command of every session.

    python3 _canon/tools/audit.py               # full audit, default book
    python3 _canon/tools/audit.py --book book_1
    python3 _canon/tools/audit.py --quiet       # summary only (used by the hook)
    python3 _canon/tools/audit.py --rule R001

WHAT IT CHECKS
    0. WIRING   — the config points at real files. A tool that scans nothing and
                  reports "clean" is worse than no tool; this refuses to.
    1. PARSE    — every canon file loads.
    2. FOSSILS  — the codex is grepped for statements that CONTRADICT its own
                  rules. This is what catches "the same dead fact in seven places
                  across five files" in one command instead of one session.
    3. PROSE    — the manuscript is checked against the rules, POV-scoped via
                  CHAPTER_INDEX.yaml, with dialogue exempted where a rule governs
                  narration only.
    4. DEVICES  — every ruled span (`cleared` / `allow` / `protected_sites`) is
                  still present in the prose. Ruled material gets deleted by GOOD
                  edits, not bad ones, so this runs regardless of edit quality.

EXIT CODE
    0 = clean or warnings only.  1 = blocking violation.
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bookconfig as cfg
from bookconfig import norm

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required:  pip install pyyaml --break-system-packages")

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", dim="\033[2m", bold="\033[1m", off="\033[0m")


def c(s, k):
    return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else s


def load_yaml(p, default=None):
    if not os.path.exists(p):
        return {} if default is None else default
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def strip_dialogue(line):
    """Remove quoted speech — a constraint on narration must not fire in dialogue."""
    return re.sub(r'"[^"]*"', " ", re.sub(r"[“”]", '"', line))


def main():
    ap = argparse.ArgumentParser()
    cfg.add_book_arg(ap)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--rule", help="run one rule id (prefix match)")
    ap.add_argument("--stats", action="store_true",
                    help="per-rule × per-chapter hit counts (disease map) instead of line-by-line output")
    args = ap.parse_args()
    if args.stats:
        args.quiet = True          # stats mode aggregates; line spam defeats it

    book = cfg.load(args.book)
    blocking, warning = [], []

    # ── 0. WIRING ────────────────────────────────────────────────────────────
    # The failure this exists to prevent: the ported tool globbed a path that did
    # not exist, scanned 0 files, and printed "intact ✓". Zero read as clean.
    if not args.quiet:
        print(c(f"\nAUDIT — {book.key}  ({book.title}, status: {book.status})", "bold"))
        print(c("\n0. WIRING", "bold"))
    pfiles = book.prose_files(strict=True)     # raises if prose_expected and none found
    if not args.quiet:
        print(f"   manuscript  {len(pfiles)} chapters  {c(book.rel(book.manuscript_dir) + '/' + book.chapter_glob, 'dim')}"
              + (c("  ✓", "grn") if pfiles else c("  (pre-prose by design)", "dim")))
        print(f"   canon layer {len(book.canon_files())} files      {c(book.rel(book.data_dir), 'dim')}"
              + (c("  ✓", "grn") if os.path.isdir(book.data_dir) else c("  ✗ MISSING", "red")))
    if not os.path.isdir(book.data_dir):
        blocking.append(("R000_wiring", book.rel(book.data_dir), 0, "canon data_dir does not exist"))

    # Series rules first, book rules layered over them (same id = book wins).
    series_rules = (load_yaml(book.series_rules_f).get("rules") or {})
    rules = (load_yaml(book.rules_f).get("rules") or {})
    if isinstance(rules, list) or isinstance(series_rules, list):
        blocking.append(("R000_wiring", book.rel(book.rules_f), 0,
                         "rules must be a MAPPING (rules: {}), not a list"))
        rules = {} if isinstance(rules, list) else rules
        series_rules = {} if isinstance(series_rules, list) else series_rules
    rules = {**series_rules, **rules}
    if args.rule:
        rules = {k: v for k, v in rules.items() if k.startswith(args.rule)}
        if not rules:
            sys.exit(f"no rule matching {args.rule!r}")

    # ── 1. PARSE ─────────────────────────────────────────────────────────────
    yfiles = sorted(glob.glob(str(book.data_dir / "**" / "*.yaml"), recursive=True))
    bad_parse = []
    for f in yfiles:
        try:
            with open(f, encoding="utf-8") as fh:
                yaml.safe_load(fh)
        except Exception as e:
            bad_parse.append((book.rel(f), str(e).split("\n")[0]))
    if not args.quiet:
        print(c("\n1. PARSE", "bold"))
        print(f"   {len(yfiles) - len(bad_parse)}/{len(yfiles)} canon files parse"
              + ("" if bad_parse else c("  ✓", "grn")))
    for f, e in bad_parse:
        blocking.append(("R009_codex_must_parse", f, 0, f"does not parse: {e}"))
        if not args.quiet:
            print(c(f"   ✗ {f}: {e}", "red"))

    # ── 2. FOSSILS IN THE CODEX ──────────────────────────────────────────────
    if not args.quiet:
        print(c("\n2. FOSSILS  (codex statements contradicting the codex's own rules)", "bold"))
    cfiles = book.canon_files()
    n_fossil = 0
    for rid, r in rules.items():
        for p in (r.get("forbidden_in_codex") or []):
            for f in cfiles:
                try:
                    lines = open(f, encoding="utf-8", errors="replace").read().split("\n")
                except OSError:
                    continue
                for i, line in enumerate(lines, 1):
                    # A line that DENIES, ANNOTATES or HISTORICISES the fossil is
                    # not a fossil. A comment explaining the fix is not the bug.
                    if re.search(r"\b(no|not|never|fossil|corrected|removed|abandoned|old entry|was a|superseded)\b",
                                 line, re.I):
                        continue
                    if line.lstrip().startswith("#"):
                        continue
                    if re.search(p, norm(line), re.I):
                        n_fossil += 1
                        blocking.append((rid, book.rel(f), i, line.strip()[:88]))
                        if not args.quiet:
                            print(c(f"   ✗ {book.rel(f)}:{i}", "red"))
                            print(f"       {c(rid, 'dim')}  matched {p!r}")
                            print(f"       {line.strip()[:88]}")
    if not args.quiet and not n_fossil:
        print(f"   {len(cfiles)} codex files scanned — no fossils" + c("  ✓", "grn"))

    # ── 3. PROSE ─────────────────────────────────────────────────────────────
    stats = {}          # rid -> {chapter_short: hits}   (feeds --stats)
    if not args.quiet:
        print(c("\n3. PROSE  (manuscript vs. the rules, POV-scoped)", "bold"))
    POV = {str(k): str((v or {}).get("pov", ""))
           for k, v in (load_yaml(book.chapter_index_f).get("chapters") or {}).items()}
    n_prose = 0
    for rid, r in rules.items():
        pats = r.get("forbidden_in_prose") or []
        # Typography rules MUST see raw bytes: norm() folds curly quotes to
        # straight and em dashes to '--', which would make such a rule either
        # silently never fire or flag the entire clean manuscript. Both happened.
        raw_pats = r.get("forbidden_in_prose_raw") or []
        if not pats and not raw_pats:
            continue
        scope = r.get("pov_scope")
        dlg_ex = r.get("dialogue_exempt", False)
        sev = r.get("severity", "warning")
        cleared = [x["text"] for x in (r.get("cleared") or [])]
        for f in pfiles:
            stem = book.chapter_stem(f)
            pov = POV.get(stem, "")
            if scope and scope.lower() not in pov.lower():
                continue
            # In an INTERCUT chapter we cannot know the line sits in that POV's
            # section. Report, but never block — a false block is how a tool
            # gets ignored, and an ignored tool is worse than no tool.
            fsev = "warning" if scope and "intercut" in pov.lower() else sev
            chnum = book.chapter_num(f)
            for i, raw in enumerate(open(f, encoding="utf-8", errors="replace").read().split("\n"), 1):
                line = strip_dialogue(raw) if dlg_ex else norm(raw)
                for spec in list(pats) + [dict(x, _raw=True) for x in raw_pats]:
                    hay = raw if spec.get("_raw") else line
                    after = spec.get("chapters_after")
                    if after and chnum <= after:
                        continue
                    mt = re.search(spec["pattern"], hay)
                    if not mt:
                        continue
                    if any(norm(x) in norm(raw) for x in spec.get("allow", [])):
                        continue
                    if any(norm(cl) in norm(raw) for cl in cleared):
                        continue     # ruled a non-defect; do not re-litigate
                    n_prose += 1
                    stats.setdefault(rid, {}).setdefault(book.short(f), 0)
                    stats[rid][book.short(f)] += 1
                    entry = (rid, book.rel(f), i, f"'{mt.group(0)}' — {spec.get('note','')}")
                    (blocking if fsev == "blocking" else warning).append(entry)
                    if not args.quiet:
                        col = "red" if fsev == "blocking" else "yel"
                        print(c(f"   {'✗' if fsev == 'blocking' else '!'} {book.rel(f)}:{i}  '{mt.group(0)}'", col))
                        print(f"       {c(rid, 'dim')}  {spec.get('note','')}")
                        print(f"       {raw.strip()[:88]}")
    if not args.quiet and not n_prose:
        print(f"   {len(pfiles)} chapters scanned — no violations" + c("  ✓", "grn"))

    # ── 4. DEVICES — the device-integrity guard ──────────────────────────────
    # Every `cleared`/`allow`/`protected_sites` text is an exact quote of a RULED
    # span. If one vanishes, ruled material was edited or normalized. The record
    # shows such deletions arrive from GOOD edits, so this runs unconditionally.
    if not args.quiet:
        print(c("\n4. DEVICES  (ruled spans still present in the prose)", "bold"))
    all_text = norm("\n".join(open(f, encoding="utf-8", errors="replace").read() for f in pfiles))
    n_dev = n_gone = 0
    for rid, r in rules.items():
        anchors = [x["text"] for x in (r.get("cleared") or [])]
        anchors += list(r.get("protected_sites") or [])
        for spec in (r.get("forbidden_in_prose") or []):
            anchors += list(spec.get("allow") or [])
        for a in anchors:
            n_dev += 1
            if norm(a) not in all_text:
                n_gone += 1
                warning.append((rid, book.rel(book.manuscript_dir), 0,
                                f"RULED SPAN VANISHED: '{a[:60]}' — edited or normalized; "
                                f"needs a ruling or a RULES update"))
                if not args.quiet:
                    print(c(f"   ! ruled span vanished: '{a[:66]}'", "yel"))
                    print(f"       {c(rid, 'dim')}  edit touched ruled material — ruling or RULES update required")
    if not args.quiet and not n_gone:
        print(f"   {n_dev} ruled spans anchored — all present" + c("  ✓", "grn"))

    # ── STATS MODE — the disease map ─────────────────────────────────────────
    if args.stats:
        print(c(f"\nSTATS — {book.key}: rule hits per chapter (warnings included)", "bold"))
        if not stats:
            print("  no rule hits anywhere.")
        else:
            chs = [book.short(f) for f in pfiles]
            for rid in sorted(stats):
                row = stats[rid]
                tot = sum(row.values())
                print(f"\n  {c(rid, 'yel')}  total {tot}")
                # compact sparkline-ish row: only chapters with hits
                line = "   "
                for ch in chs:
                    if row.get(ch):
                        line += f" {ch}:{row[ch]}"
                print(line)
        print()

    # ── SUMMARY ──────────────────────────────────────────────────────────────
    print(c("\n" + "─" * 62, "dim"))
    if not blocking and not warning:
        print(c(f"AUDIT CLEAN ({book.key})", "grn") +
              f"  — {len(rules)} rules run over {len(pfiles)} chapters, {len(cfiles)} codex files.")
        if not rules:
            print(c("  NOTE: 0 rules are filed. A clean audit with no rules proves wiring, not canon.", "yel"))
        return 0
    print(f"{c(str(len(blocking)) + ' BLOCKING', 'red') if blocking else '0 blocking'}"
          f"   {c(str(len(warning)) + ' warning', 'yel') if warning else '0 warnings'}")
    for rid, f, i, msg in blocking[:20]:
        print(f"  {c('BLOCK', 'red')}  {f}:{i}  {rid}  {msg}")
    for rid, f, i, msg in warning[:10]:
        print(f"  {c('warn ', 'yel')}  {f}:{i}  {rid}  {msg}")
    if len(blocking) + len(warning) > 30:
        print(f"  … and {len(blocking) + len(warning) - 30} more")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
