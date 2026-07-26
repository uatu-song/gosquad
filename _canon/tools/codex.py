#!/usr/bin/env python3
"""
codex.py — THE FILING SYSTEM. Ask the repo for a thing by its code.

    python3 _canon/tools/codex.py CHR-AHDIA          # the dossier
    python3 _canon/tools/codex.py ahdia              # fuzzy — same thing
    python3 _canon/tools/codex.py MEC-SEED --prose   # every live site in the book
    python3 _canon/tools/codex.py --list             # every code
    python3 _canon/tools/codex.py --list chr
    python3 _canon/tools/codex.py --find "Exile Island"   # who owns this string?
    python3 _canon/tools/codex.py --gaps             # what the system does NOT know
    python3 _canon/tools/codex.py --book book_1 --gaps

WHY
    Canon for this series lives in 5_story_bibles/, 7_characters/arcs/, 8_codex/,
    4_constraints/ and a dozen handoff docs, and none of them share a key. To ask
    "what does the repo know about Exile Island?" you had to read six trees and
    trust that none had rotted. So nobody asked, and contradictions (28 vs 37
    dictators; Korede 15 vs 17) survived for months across multiple files.

    A code is an address. This resolves it.

TWO KINDS OF CODE
    HAND-FILED  CHR- THM- MEC- WRD-   live in <data_dir>/INDEX.yaml
    DERIVED     PRM- FCT- CON- RUL-   read from their owner file AT QUERY TIME,
                                      never copied. Copying is how fossils spread.

THE PROSE IS THE AUTHORITY
    Every dossier greps the manuscript live and reports what is TRUE NOW, with
    chapter and line — not what a YAML said last time someone edited it.
"""
import argparse
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bookconfig as cfg
from bookconfig import norm

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", cyan="\033[36m",
         dim="\033[2m", bold="\033[1m", off="\033[0m")


def c(s, k):
    return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else str(s)


def load_yaml(p, default=None):
    """Absent canon files are a legitimate state (a book mid-ingest), not a crash."""
    import yaml
    if not os.path.exists(p):
        return {} if default is None else default
    with io.open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_jsonl(p):
    out = []
    if not os.path.exists(p):
        return out
    for ln in io.open(p, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if isinstance(r, dict) and r.get("id") and "_schema" not in r:
            out.append(r)
    return out


# ── BUILD THE CODE TABLE ─────────────────────────────────────────────────────
def build(book):
    codes = {}
    idx = load_yaml(book.index_f)

    for section, kind in (("characters", "CHR"), ("themes", "THM"),
                          ("mechanics", "MEC"), ("words", "WRD")):
        for code, v in (idx.get(section) or {}).items():
            v = dict(v or {})
            v.update(kind=kind, code=code, source=book.rel(book.index_f), derived=False)
            codes[code] = v

    # DERIVED — read from the owner, never copied into INDEX.yaml
    for pr in load_jsonl(book.promises_f):
        codes[f"PRM-{pr['id']}"] = dict(
            kind="PRM", code=f"PRM-{pr['id']}", derived=True,
            source=book.rel(book.promises_f), owner=book.rel(book.promises_f),
            name=str(pr.get("promise") or pr.get("setup") or pr["id"])[:100],
            status=pr.get("status"), raw=pr, aliases=[],
            note=str(pr.get("payoff") or pr.get("notes") or ""))

    for ft in load_jsonl(book.facts_f):
        codes[f"FCT-{ft['id']}"] = dict(
            kind="FCT", code=f"FCT-{ft['id']}", derived=True,
            source=book.rel(book.facts_f), owner=book.rel(book.facts_f),
            name=str(ft.get("fact") or ft["id"])[:100],
            status=ft.get("status"), raw=ft, aliases=[],
            note=str(ft.get("value") or ""))

    # CONSTRAINTS.yaml is optional — absent simply means no CON- codes yet.
    for grp, items in (load_yaml(book.constraints_f).get("constraints") or {}).items():
        for it in items or []:
            codes[it["id"]] = dict(
                kind="CON", code=it["id"], derived=True, severity=grp,
                source=book.rel(book.constraints_f),
                owner=book.rel(book.constraints_f) + " > constraints",
                name=it.get("name", ""), note=it.get("rule", ""), aliases=[], raw=it)

    for rid, r in (load_yaml(book.rules_f).get("rules") or {}).items():
        short = rid.split("_")[0]                 # R001_no_ahdia_pov -> R001
        codes[short] = dict(
            kind="RUL", code=short, derived=True, full_id=rid,
            source=book.rel(book.rules_f), owner=r.get("owner", ""),
            name=rid, severity=r.get("severity"), aliases=[], raw=r,
            note=" ".join(str(r.get("statement", "")).split()))
    return codes


def resolve(codes, q):
    if q in codes:
        return [q]
    up = q.upper()
    hits = [k for k in codes if k.upper() == up]
    if hits:
        return hits
    hits = [k for k in codes if up in k.upper()]
    if hits:
        return sorted(hits)
    low = q.lower()
    return sorted(k for k, v in codes.items()
                  if low in str(v.get("name", "")).lower()
                  or any(low == str(a).lower() for a in (v.get("aliases") or [])))


# ── THE MANUSCRIPT ───────────────────────────────────────────────────────────
_CH = None


def chapters(book):
    global _CH
    if _CH is None:
        povs = {}
        try:
            for k, v in (load_yaml(book.chapter_index_f).get("chapters") or {}).items():
                povs[str(k)] = str((v or {}).get("pov", "?"))
        except Exception:
            pass
        _CH = []
        for f in book.prose_files(strict=False):
            stem = book.chapter_stem(f)
            _CH.append(dict(
                stem=stem, rel=book.rel(f), num=book.chapter_num(f),
                short=book.short(f), pov=povs.get(stem, "?"),
                lines=io.open(f, encoding="utf-8", errors="replace").read().split("\n")))
    return _CH


def prose_sites(book, aliases, limit=None):
    """Every live site of these aliases in the edit-of-record."""
    out = []
    if not aliases:
        return out
    pat = re.compile("|".join(re.escape(norm(str(a))) for a in aliases), re.I)
    for ch in chapters(book):
        for i, line in enumerate(ch["lines"], 1):
            m = pat.search(norm(line))
            if m:
                out.append((ch["short"], ch["pov"], i, m.group(0), line.strip(), ch["rel"]))
                if limit and len(out) >= limit:
                    return out
    return out


# ── DOSSIER ──────────────────────────────────────────────────────────────────
def dossier(book, codes, code, show_prose=False):
    v = codes[code]
    kind = v["kind"]
    print()
    print(c(f"  {code}", "bold") + c(f"   {v.get('name','')}", "cyan"))
    print(c("  " + "─" * 74, "dim"))

    if v.get("status"):
        s = str(v["status"])
        col = "grn" if s in ("paid", "canonical") else "yel" if s in ("open", "wobbling") else "dim"
        print(f"  {'status':14}{c(s, col)}")
    for f in ("severity", "polarity", "scope", "voice"):
        if v.get(f):
            print(f"  {f:14}{v[f]}")
    if v.get("owner"):
        print(f"  {'owner':14}{c(v['owner'], 'dim')}")
    if v.get("derived"):
        print(f"  {'derived from':14}{c(v['source'] + '  (read live, never copied)', 'dim')}")

    if v.get("note"):
        print()
        for ln in re.sub(r"\s+", " ", str(v["note"])).strip().split(". "):
            if ln.strip():
                print("  " + ln.strip().rstrip(".") + ".")

    if v.get("raw") and kind in ("PRM", "FCT"):
        print()
        for k2, v2 in v["raw"].items():
            if k2 in ("id", "status") or not v2:
                continue
            print(f"  {c(k2[:12].ljust(12), 'dim')}  {str(v2)[:100]}")

    if v.get("governed_by"):
        print()
        print(c("  GOVERNED BY", "bold"))
        for g in v["governed_by"]:
            tgt = codes.get(str(g)) or codes.get(str(g).split("_")[0])
            if tgt:
                print(f"    {c(tgt['code'].ljust(10), 'yel')} {str(tgt.get('note') or tgt.get('name'))[:62]}")
            else:
                print(f"    {c(str(g).ljust(10), 'red')} ⚠ BROKEN LINK — no such code")

    if v.get("see"):
        print()
        print(c("  SEE ALSO", "bold"))
        for s in v["see"]:
            tgt = codes.get(str(s))
            if tgt:
                print(f"    {c(str(s).ljust(26), 'cyan')} {str(tgt.get('name'))[:44]}")
            else:
                print(f"    {c(str(s).ljust(26), 'red')} ⚠ BROKEN LINK")

    # LIVE PROSE
    al = v.get("aliases") or []
    if al:
        sites = prose_sites(book, al)
        print()
        print(c(f"  IN THE MANUSCRIPT   {len(sites)} sites", "bold") +
              c(f"  ({', '.join(str(a) for a in al)})", "dim"))
        if not sites:
            if not book.prose_expected:
                print(c(f"    no prose yet for {book.key} — codex is running ahead of the manuscript.", "dim"))
            elif v.get("expect_in_prose") == "absent":
                print(c("    none — and none is the PASS for this code (protected absence).", "grn"))
            else:
                print(c("    none — this code names nothing in the prose. Codex-only.", "yel"))
        else:
            chs = sorted({s[0] for s in sites}, key=lambda x: int(re.sub(r"\D", "", x) or 999))
            print(f"    {c('chapters', 'dim')}  {', '.join(chs)}")
            for shrt, pov, i, hit, line, rel in (sites if show_prose else sites[:6]):
                print(f"    {c((shrt + ':' + str(i)).ljust(11), 'grn')} {c('[' + pov[:14] + ']', 'dim')} {line[:74]}")
            if not show_prose and len(sites) > 6:
                print(c(f"    … {len(sites) - 6} more — rerun with --prose", "dim"))

    back = [k for k, o in codes.items()
            if code in [str(x) for x in (o.get("see") or [])] and k != code]
    if back:
        print()
        print(c("  FILED UNDER THIS BY", "bold") + "  " + ", ".join(c(b, "cyan") for b in back))

    if os.path.exists(book.decisions_f) and (al or v.get("name")):
        terms = [str(x) for x in al] + [str(v.get("name", ""))]
        hits = [ln.strip() for ln in io.open(book.decisions_f, encoding="utf-8")
                if any(t and t.lower() in ln.lower() for t in terms)]
        if hits:
            print()
            print(c("  DECISIONS  (do not relitigate)", "bold"))
            for h in hits[:4]:
                print(f"    {h[:82]}")
    print()


# ── REPORTS ──────────────────────────────────────────────────────────────────
KINDS = [("CHR", "characters"), ("THM", "themes"), ("MEC", "mechanics/concepts"),
         ("WRD", "watched words"), ("PRM", "setups & payoffs"), ("FCT", "canon facts"),
         ("CON", "constraints"), ("RUL", "executable rules")]


def do_list(book, codes, filt):
    if not codes:
        print(c(f"\n  {book.key}: no codes filed yet.", "yel"))
        print(c(f"  Populate {book.rel(book.index_f)} one namespace at a time.\n", "dim"))
        return 0
    for k, label in KINDS:
        if filt and filt.upper() not in k:
            continue
        group = sorted([v for v in codes.values() if v["kind"] == k], key=lambda v: v["code"])
        if not group:
            continue
        print()
        print(c(f"  {k}  {label}", "bold") + c(f"   ({len(group)})", "dim") +
              (c("   derived — not copied", "dim") if group[0].get("derived") else ""))
        for v in group:
            st = str(v.get("status") or v.get("polarity") or v.get("severity") or "")
            col = "grn" if st in ("paid", "canonical", "protected") else \
                  "red" if st in ("banned", "blocking") else \
                  "yel" if st in ("open", "wobbling", "watched", "warning") else "dim"
            print(f"    {c(v['code'].ljust(28), 'cyan')} {c(st.ljust(10), col)} {str(v.get('name',''))[:44]}")
    print()
    return 0


def do_find(book, codes, q):
    """Which code owns this string — and where does it live in the book?"""
    print()
    ql = q.lower()
    owners = [v for v in codes.values()
              if any(ql in str(a).lower() or str(a).lower() in ql for a in (v.get("aliases") or []))]
    if owners:
        print(c(f"  {q!r} is filed under:", "bold"))
        for v in owners:
            print(f"    {c(v['code'].ljust(26), 'cyan')} {str(v.get('name',''))[:48]}")
    else:
        print(c(f"  {q!r} is filed under NO code.", "yel"))
        print(c("    If it matters, it needs one. If it doesn't, it shouldn't be in the prose.", "dim"))

    sites = prose_sites(book, [q])
    print()
    print(c(f"  IN THE MANUSCRIPT   {len(sites)} sites", "bold"))
    for shrt, pov, i, hit, line, rel in sites[:20]:
        print(f"    {c((shrt + ':' + str(i)).ljust(11), 'grn')} {c('[' + pov[:14] + ']', 'dim')} {line[:74]}")
    if len(sites) > 20:
        print(c(f"    … {len(sites) - 20} more", "dim"))

    cf = []
    for f in book.canon_files():
        for i, ln in enumerate(io.open(f, encoding="utf-8", errors="replace").read().split("\n"), 1):
            if ql in norm(ln).lower():
                cf.append((book.rel(f), i, ln.strip()))
    print()
    print(c(f"  IN THE CODEX   {len(cf)} sites", "bold") +
          c("   ← if the prose count is 0 and this is not, you have a fossil", "dim"))
    for f, i, ln in cf[:12]:
        print(f"    {c((f + ':' + str(i)), 'yel')}  {ln[:66]}")
    print()
    return 0


def do_gaps(book, codes, enforce=False):
    """What the filing system does NOT know. The system reporting its own holes.

    enforce=True: exit 1 on a HARD defect (gate mode for the pre-commit wall).
    Hard = broken cross-ref, or a code appearing in prose that must not.
    Open setups, unfiled entities and 'names nothing' are warnings. Wobbling
    facts are surfaced but NEVER hard: a wobble is a flag for the Director's
    ruling, and blocking unrelated commits on it would make the wall get
    disabled — which costs more than the wobble.
    """
    print()
    print(c(f"  GAPS — {book.key}: what is not filed, and what is filed but dead", "bold"))
    print(c("  " + "─" * 74, "dim"))
    n = hard = 0

    # 0. is there prose to check against at all?
    n_prose_files = len(book.prose_files(strict=False))
    if not n_prose_files:
        msg = ("pre-prose by design (books.yaml)" if not book.prose_expected
               else "NO PROSE FOUND — glob is wrong")
        col = "dim" if not book.prose_expected else "red"
        print()
        print(c(f"  · manuscript: 0 files — {msg}", col))
        if book.prose_expected:
            hard += 1
            n += 1

    # 1. broken cross-references
    broken = []
    for v in codes.values():
        for f in ("see", "governed_by"):
            for tgt in (v.get(f) or []):
                t = str(tgt)
                if t not in codes and t.split("_")[0] not in codes:
                    broken.append((v["code"], f, t))
    if broken:
        n += len(broken)
        hard += len(broken)
        print()
        print(c(f"  ✗ {len(broken)} BROKEN CROSS-REFERENCE(S)", "red"))
        for code, f, t in broken:
            print(f"      {code}.{f} → {c(t, 'red')} (no such code)")

    # 2. EXPECTATION CHECK — the direction of the test depends on the code.
    #    For a banned word or a protected reveal, ZERO hits is the PASS and any
    #    hit is the DEFECT. Encoding this is what stops the next agent reading
    #    "0 sites" as "dead code" and deleting the guard.
    absent_ok, absent_violated, unexplained = [], [], []
    for v in codes.values():
        al = v.get("aliases") or []
        if not al:
            continue
        allow = [norm(str(x)) for x in (v.get("allow") or [])]
        live = [st for st in prose_sites(book, al)
                if not any(a in norm(st[4]) for a in allow)]
        if v.get("expect_in_prose") == "absent":
            (absent_violated if live else absent_ok).append((v, live))
        elif not live and v.get("status") != "CODEX-ONLY" and n_prose_files:
            unexplained.append(v)

    if absent_violated:
        n += len(absent_violated)
        hard += len(absent_violated)
        print()
        print(c(f"  ✗ {len(absent_violated)} CODE(S) APPEAR IN THE PROSE THAT MUST NOT", "red"))
        for v, live in absent_violated:
            print(f"      {c(v['code'].ljust(24), 'red')} {str(v.get('note',''))[:52]}")
            for shrt, pov, i, hit, line, rel in live[:3]:
                print(f"        {c(shrt + ':' + str(i), 'red')} [{pov[:12]}] {line[:58]}")
    if absent_ok:
        print()
        print(c(f"  ✓ {len(absent_ok)} ABSENCE(S) HOLDING", "grn") +
              c("   zero hits is the PASS for these — bans and protected reveals", "dim"))
        for v, _ in absent_ok:
            print(f"      {c(v['code'].ljust(24), 'grn')} {str(v.get('note',''))[:52]}")
    if unexplained:
        n += len(unexplained)
        print()
        print(c(f"  ! {len(unexplained)} CODE(S) NAME NOTHING IN THE PROSE", "yel") +
              c("   undeclared — fossil, or needs expect_in_prose: absent", "dim"))
        for v in unexplained:
            print(f"      {v['code'].ljust(24)}")

    # 3. unpaid setups
    open_prm = [v for v in codes.values() if v["kind"] == "PRM" and v.get("status") == "open"]
    if open_prm:
        print()
        print(c(f"  · {len(open_prm)} OPEN SETUP(S)", "cyan") +
              c("   candidate holes — only the Director rules them red-herring/unimportant", "dim"))
        for v in open_prm:
            print(f"      {v['code'].ljust(28)} {str(v.get('name',''))[:46]}")

    # 4. wobbling facts — surfaced, never blocking (Director's ruling, not ours)
    wob = [v for v in codes.values()
           if v["kind"] == "FCT" and v.get("status") in ("wobbling", "contradicted")]
    if wob:
        n += len(wob)
        print()
        print(c(f"  ✗ {len(wob)} FACT(S) WOBBLING OR CONTRADICTED", "red") +
              c("   awaiting a Director ruling — never auto-resolved", "dim"))
        for v in wob:
            print(f"      {v['code'].ljust(28)} {str(v.get('name',''))[:46]}")

    print()
    print(c("  " + "─" * 74, "dim"))
    if n == 0:
        print(c("  NO GAPS", "grn") + f"  — {len(codes)} codes resolve; every one accounted for in the book.")
    else:
        print(f"  {c(str(n) + ' item(s) need attention', 'yel')}  (open setups are not defects)")
    print()
    if enforce:
        if hard:
            print(c(f"  🚫 ENFORCE: {hard} HARD DEFECT(S) — commit blocked.", "red"))
        return 1 if hard else 0
    return 0


def main():
    ap = argparse.ArgumentParser(add_help=True)
    cfg.add_book_arg(ap)
    ap.add_argument("code", nargs="?", help="a filing code, or any fuzzy fragment of one")
    ap.add_argument("--list", nargs="?", const="", metavar="KIND")
    ap.add_argument("--find", metavar="TEXT", help="which code owns this string?")
    ap.add_argument("--gaps", action="store_true", help="what the system does not know")
    ap.add_argument("--enforce", action="store_true",
                    help="gate mode: run --gaps and exit 1 on any HARD defect")
    ap.add_argument("--prose", action="store_true", help="every prose site, not the first 6")
    a = ap.parse_args()

    book = cfg.load(a.book)
    codes = build(book)

    if a.enforce:
        return do_gaps(book, codes, enforce=True)
    if a.gaps:
        return do_gaps(book, codes)
    if a.find:
        return do_find(book, codes, a.find)
    if a.list is not None:
        return do_list(book, codes, a.list)
    if not a.code:
        print(__doc__)
        print(c(f"  {book.key} ({book.title}) — {len(codes)} codes filed, "
                f"{len(book.prose_files(strict=False))} chapters. --list to see them.\n", "dim"))
        return 0

    hits = resolve(codes, a.code)
    if not hits:
        print(c(f"\n  no code matches {a.code!r} in {book.key}.", "red"))
        print(c("  --list to see them all, or --find to search the prose instead.\n", "dim"))
        return 1
    if len(hits) > 8:
        print(c(f"\n  {a.code!r} matches {len(hits)} codes:", "yel"))
        for h in hits:
            print(f"    {c(h.ljust(28), 'cyan')} {str(codes[h].get('name',''))[:44]}")
        print()
        return 0
    for h in hits:
        dossier(book, codes, h, show_prose=a.prose)
    return 0


if __name__ == "__main__":
    sys.exit(main())
