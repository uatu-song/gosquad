#!/usr/bin/env python3
"""
audit.py — THE canon audit. One command.

    python3 ledger/tools/audit.py            # full audit
    python3 ledger/tools/audit.py --quiet    # summary only
    python3 ledger/tools/audit.py --rule R001
    python3 ledger/tools/audit.py --candidates   # ALSO run ledger/codex/RULES_CANDIDATES.yaml, report-only

WHY THIS EXISTS
    On 2026-07-13 a dead mechanic ("Standard's protective aura") was cut from
    the prose. It survived in SEVEN places across FIVE codex files, and was
    found by hand, one file at a time, over an entire session. The prose was
    audited with ad-hoc greps. A bespoke regex "deletion guard" was written and
    FAILED ITS OWN TEST.

    The author's verdict: "The codex isn't the problem, it's not making it
    central that is egregious. The point of the codex is to do these types of
    audits expediently."

    So: the rules live in ledger/codex/RULES.yaml (path set in ledger/config.json), and
    this runs them. Rules not yet ruled for this book wait in
    ledger/codex/RULES_CANDIDATES.yaml; --candidates runs them as warnings only.

WHAT IT CHECKS
    1. PARSE     — every canon file loads. (Two had NEVER parsed.)
    2. FOSSILS   — the codex is grepped for statements that CONTRADICT its own
                   rules. This is what catches "seven places, five files" in one
                   command instead of one session.
    3. PROSE     — the manuscript is checked against the rules, POV-scoped via
                   CHAPTER_INDEX.yaml, with dialogue exempted where the rule
                   only governs narration.

EXIT CODE
    0 = clean or warnings only.  1 = blocking violation.
"""
import argparse, glob, os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import (ROOT as REPO, CFG, data, prose_files, pov_map, pov_of,
                    chapter_num, characters, norm, strip_dialogue, load_yaml)
RULES_F = data("RULES.yaml")
CANDIDATES_F = data("RULES_CANDIDATES.yaml")
CODEX_G = CFG["codex_globs"]
NOT_FOSSIL_FILES = ("RULES.yaml", "RULES_CANDIDATES.yaml", "CODEX_CHANGELOG.md")

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", dim="\033[2m", bold="\033[1m", off="\033[0m")
def c(s, k): return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else s

def codex_files():
    out = []
    for g in CODEX_G:
        out += glob.glob(os.path.join(REPO, g))
    # the rules file and the changelog DESCRIBE the fossils; they are not fossils
    return [f for f in sorted(set(out))
            if os.path.basename(f) not in NOT_FOSSIL_FILES]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--rule", help="run one rule id (prefix match)")
    ap.add_argument("--candidates", action="store_true",
                    help="also run ledger/codex/RULES_CANDIDATES.yaml (never blocks: warnings only)")
    args = ap.parse_args()

    try:
        rules = (load_yaml(RULES_F) or {}).get("rules") or {}
    except OSError:
        sys.exit(f"no rules file at {RULES_F} — see ledger/config.json 'suite.data_dir'")
    if args.candidates and os.path.exists(CANDIDATES_F):
        for rid, r in ((load_yaml(CANDIDATES_F) or {}).get("rules") or {}).items():
            r = dict(r or {}, severity="warning", _candidate=True)
            rules.setdefault("CANDIDATE:" + rid, r)
    if args.rule:
        rules = {k: v for k, v in rules.items() if k.startswith(args.rule)}
        if not rules:
            sys.exit(f"no rule matching {args.rule!r}")

    blocking, warning = [], []

    # ── 1. PARSE ────────────────────────────────────────────────────────────
    bad_parse = []
    yfiles = glob.glob(os.path.join(REPO, CFG["data_dir"], "**", "*.yaml"), recursive=True)
    for f in yfiles:
        try:
            load_yaml(f)
        except Exception as e:
            bad_parse.append((os.path.relpath(f, REPO), str(e).split("\n")[0]))
    n_yaml = len(yfiles)
    if not args.quiet:
        print(c("\n1. PARSE", "bold"))
        print(f"   {n_yaml - len(bad_parse)}/{n_yaml} canon files parse"
              + ("" if bad_parse else c("  ✓", "grn")))
    for f, e in bad_parse:
        blocking.append(("R009_codex_must_parse", f, 0, f"does not parse: {e}"))
        if not args.quiet: print(c(f"   ✗ {f}: {e}", "red"))

    # ── 2. FOSSILS IN THE CODEX ─────────────────────────────────────────────
    if not args.quiet: print(c("\n2. FOSSILS  (codex statements contradicting the codex's own rules)", "bold"))
    cfiles = codex_files()
    n_fossil = 0
    for rid, r in rules.items():
        pats = r.get("forbidden_in_codex") or []
        if not pats: continue
        for f in cfiles:
            try:
                lines = open(f, encoding="utf-8").read().split("\n")
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                # a line that DENIES the fossil is not a fossil
                # A line that DENIES, ANNOTATES or HISTORICISES the fossil is not a fossil.
                if re.search(r"\b(no|not|never|fossil|corrected|removed|abandoned|old entry|was a)\b", line, re.I):
                    continue
                if line.lstrip().startswith("#"):
                    continue     # a comment explaining the fix is not the bug
                for p in pats:
                    if re.search(p, norm(line), re.I):
                        n_fossil += 1
                        rel = os.path.relpath(f, REPO)
                        blocking.append((rid, rel, i, line.strip()[:88]))
                        if not args.quiet:
                            print(c(f"   ✗ {rel}:{i}", "red"))
                            print(f"       {c(rid, 'dim')}  matched {p!r}")
                            print(f"       {line.strip()[:88]}")
    if not args.quiet and not n_fossil:
        print(f"   {len(cfiles)} codex files scanned — no fossils" + c("  ✓", "grn"))

    # ── 3. PROSE ────────────────────────────────────────────────────────────
    if not args.quiet: print(c("\n3. PROSE  (manuscript vs. the rules, POV-scoped)", "bold"))
    POV = pov_map()
    pfiles = prose_files()
    n_prose = 0
    for rid, r in rules.items():
        pats = r.get("forbidden_in_prose") or []
        # Typography rules MUST see the raw bytes: norm() folds curly quotes to
        # straight and em dashes to '--', which would make such a rule either
        # silently never fire or flag the entire clean manuscript. (2026-07-24)
        raw_pats = r.get("forbidden_in_prose_raw") or []
        if not pats and not raw_pats: continue
        scope = r.get("pov_scope")
        dlg_ex = r.get("dialogue_exempt", False)
        sev = r.get("severity", "warning")
        cleared = [x["text"] for x in (r.get("cleared") or [])]
        for f in pfiles:
            pov = pov_of(f, POV)
            if scope and scope.lower() not in pov.lower():
                continue
            # In an INTERCUT chapter we cannot know the line sits in HER section.
            # Report, but never block on it — a false block is how a tool gets ignored.
            fsev = "warning" if scope and "intercut" in pov.lower() else sev
            chnum = chapter_num(f)
            for i, raw in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
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
                    rel = os.path.relpath(f, REPO)
                    entry = (rid, rel, i, f"'{mt.group(0)}' — {spec.get('note','')}")
                    (blocking if fsev == "blocking" else warning).append(entry)
                    if not args.quiet:
                        col = "red" if fsev == "blocking" else "yel"
                        print(c(f"   {'✗' if fsev=='blocking' else '!'} {rel}:{i}  '{mt.group(0)}'", col))
                        print(f"       {c(rid, 'dim')}  {spec.get('note','')}")
                        print(f"       {raw.strip()[:88]}")
    if not args.quiet and not n_prose:
        print(f"   {len(pfiles)} chapters scanned — no violations" + c("  ✓", "grn"))

    # ── 4. DEVICES — the device-integrity guard (Rogers Amendment, 2026-07-14) ──
    # Every `cleared`/`allow`/`protected_sites` text in RULES.yaml is an exact quote
    # of a RULED span. If one vanishes from the manuscript, ruled material was edited
    # or normalized — the record shows such deletions arrive from GOOD edits (rogers-
    # approved, blind-reader-praised), so this check runs regardless of edit quality.
    if not args.quiet: print(c("\n4. DEVICES  (ruled spans still present in the prose)", "bold"))
    all_text = norm("\n".join(open(f, encoding="utf-8").read() for f in pfiles))
    n_dev = n_gone = 0
    for rid, r in rules.items():
        if r.get("_candidate"):
            continue
        anchors = [x["text"] for x in (r.get("cleared") or [])]
        anchors += list(r.get("protected_sites") or [])
        for spec in (r.get("forbidden_in_prose") or []):
            anchors += list(spec.get("allow") or [])
        for a in anchors:
            n_dev += 1
            if norm(a) not in all_text:
                n_gone += 1
                warning.append((rid, "prose", 0,
                                f"RULED SPAN VANISHED: '{a[:60]}' — edited or normalized; needs a ruling or a RULES update"))
                if not args.quiet:
                    print(c(f"   ! ruled span vanished: '{a[:66]}'", "yel"))
                    print(f"       {c(rid, 'dim')}  edit touched ruled material — ruling or RULES update required")
    if not args.quiet and not n_gone:
        print(f"   {n_dev} ruled spans anchored — all present" + c("  ✓", "grn"))

    # ── 5. PRONOUNS  (R016, 2026-08-09) ──────────────────────────────────────
    # CHARACTERS.yaml declared Okonkwo `gender: "man"`. The prose says woman in
    # seven places and man in zero — and the fossil had already grown back into
    # CH35 three times. Nothing compared the two. Now something does.
    #
    # PRECISION OVER RECALL, deliberately. The first cut of this check used
    # "line names exactly one character" and produced 147 blocking hits, nearly
    # all of them a second character's pronoun ("Hendricks watches her" — her is
    # Standard). A rule that cries wolf is a rule that gets switched off, so this
    # fires ONLY on constructions where the pronoun is grammatically bound to the
    # name: reflexives, appositives, "the man NAME", "NAME is a woman", and YAML
    # keys that name a character. See R016.scope_note for what escapes it.
    prule = rules.get("R016_pronoun_consistency")
    if prule:
        if not args.quiet:
            print(c("\n5. PRONOUNS  (declared pronouns vs. how the book speaks)", "bold"))
        FEM  = {"she", "her", "hers", "herself", "woman", "women", "girl"}
        MASC = {"he", "him", "his", "himself", "man", "men", "boy"}
        chars = characters()
        ignore = {t for t in (prule.get("ignore_tokens") or [])}
        okay   = [norm(x) for x in (prule.get("known_exceptions") or [])]
        tok = {}
        for k, v in (chars or {}).items():
            dem = ((v or {}).get("demographics") or {})
            pr = {str(x).lower() for x in (dem.get("pronouns") or [])}
            g = "fem" if pr & FEM else ("masc" if pr & MASC else None)
            if not g:
                continue          # it/they — ungendered by declaration
            for t in re.findall(r"[A-Z][a-z]{3,}", str(v.get("canonical_name") or k)):
                if t in ignore:
                    continue
                tok[t] = None if tok.get(t, g) != g else g   # 2 claimants -> ambiguous
        tok = {t: g for t, g in tok.items() if g}
        WRONG = {"fem": MASC, "masc": FEM}
        n_pron = 0

        # Bound constructions ONLY. {T} is the character token.
        # Windows are deliberately tiny. At 30 chars pattern 1 matched a reflexive
        # belonging to a different character three clauses away; at 20 the "the man
        # NAME" appositive matched dialogue that merely ENDED near a name
        # (CH28:43 '"...a terrified old man hiding in a hole," Elena snaps').
        BOUND = [r"\b{T}\b[^.?!,\"]{{0,12}}\b(himself|herself)\b",
                 r"\b{T}\b\s*,\s*(he|she)\b",
                 r"\b{T}\b[^.?!,\"]{{0,15}}\b(?:is|was)\s+(?:a|an|the)\s+(man|woman)\b"]

        def bound_hit(text, t, g):
            for pat in BOUND:
                mt = re.search(pat.format(T=t), text, re.I)
                if mt and any(w in WRONG[g] for w in re.findall(r"[a-z]+", mt.group(0).lower())):
                    w = next(w for w in re.findall(r"[a-z]+", mt.group(0).lower()) if w in WRONG[g])
                    return mt.group(0), w
            return None, None

        def check(path, rel, blockit):
            n = 0
            try:
                lines = open(path, encoding="utf-8").read().split("\n")
            except OSError:
                return 0
            for i, raw in enumerate(lines, 1):
                if raw.lstrip().startswith("#") or any(x in norm(raw) for x in okay):
                    continue
                if re.search(r"\b(fossil|corrected|was declared|used to|old entry)\b", raw, re.I):
                    continue
                line = norm(raw)
                for t, g in tok.items():
                    span, w = bound_hit(line, t, g)
                    # a YAML key naming the character binds its own value
                    if not span:
                        # ONLY a possessive-style key binds its value. Any key merely
                        # CONTAINING the name does not: `she_asks_hendricks:` and
                        # `last_words_to_elena:` describe somebody else entirely, and
                        # they produced 14 of 14 false blocks on the first cut.
                        km = re.match(rf"\s*{t.lower()}(?:_(?:status|state|arc|profile|notes?))?\s*:(.*)$",
                                      line, re.I)
                        if km:
                            bad = [x for x in re.findall(r"[a-z]+", km.group(1).lower())
                                   if x in WRONG[g]]
                            if bad:
                                span, w = km.group(0).strip(), bad[0]
                    if not span:
                        continue
                    n += 1
                    msg = f"{t} is declared {g} but this says '{w}'"
                    (blocking if blockit else warning).append(
                        ("R016_pronoun_consistency", rel, i, msg))
                    if not args.quiet:
                        print(c(f"   {'✗' if blockit else '!'} {rel}:{i}  {msg}",
                                "red" if blockit else "yel"))
                        print(f"       {span.strip()[:88]}")
            return n

        for f in cfiles:                       # codex side — BLOCKING, it is the fossil
            n_pron += check(f, os.path.relpath(f, REPO), True)
        for f in pfiles:                       # prose side — warning, human reads it
            n_pron += check(f, os.path.relpath(f, REPO), False)

        if not args.quiet and not n_pron:
            print(f"   {len(tok)} named characters cross-checked — declarations agree"
                  + c("  ✓", "grn"))
            print(c("   (coreference is out of scope — see R016.scope_note)", "dim"))

    # ── SUMMARY ─────────────────────────────────────────────────────────────
    print(c("\n" + "─" * 62, "dim"))
    if not blocking and not warning:
        print(c("AUDIT CLEAN", "grn") + f"  — {len(rules)} rule(s): codex parses, no fossils, prose obeys the rules.")
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
