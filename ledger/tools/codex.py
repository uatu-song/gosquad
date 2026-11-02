#!/usr/bin/env python3
"""
codex.py — THE FILING SYSTEM. Ask the repo for a thing by its code.

    python3 ledger/tools/codex.py CHR-NAME          # the dossier
    python3 ledger/tools/codex.py name              # fuzzy — same thing
    python3 ledger/tools/codex.py MEC-X --prose     # every live site in the book
    python3 ledger/tools/codex.py --list            # every code
    python3 ledger/tools/codex.py --list mec
    python3 ledger/tools/codex.py --find "some phrase"       # who owns this string?
    python3 ledger/tools/codex.py --gaps            # what the system does NOT know

WHY
    Six registries described the same book and shared no key. To ask "what does
    the repo know about the Drop?" you had to read CHARACTERS.yaml, CORE.yaml,
    GEOMETRY_TRACKER.yaml, PROMISES.jsonl, CANON_FACTS.jsonl and RULES.yaml. So
    nobody did, and a dead mechanic lived in eight places across six files.

    A code is an address. This resolves it.

TWO KINDS OF CODE
    HAND-FILED  CHR- THM- MEC- WRD-   live in ledger/codex/INDEX.yaml
    DERIVED     PRM- FCT- CON- RUL-   read from their owner file AT QUERY TIME,
                                      never copied. Copying is how fossils spread.

THE PROSE IS THE AUTHORITY
    Every dossier greps the manuscript live and reports what is TRUE NOW, with
    chapter, line and POV — not what a YAML file said last time someone edited it.
"""
import argparse, glob, io, json, os, re, sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import (ROOT as REPO, P, CFG, data, prose_files, pov_map, pov_of,
                    chapter_id, chapter_num, characters, norm, load_yaml, load_jsonl, rel)

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", cyan="\033[36m",
         dim="\033[2m", bold="\033[1m", off="\033[0m")
def c(s, k):
    return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else str(s)

# ── BUILD THE CODE TABLE ─────────────────────────────────────────────────────
def build():
    codes = {}
    try:
        idx = load_yaml(data("INDEX.yaml")) or {}
    except OSError:
        idx = {}

    for section, kind in (("characters", "CHR"), ("themes", "THM"),
                          ("mechanics", "MEC"), ("words", "WRD")):
        for code, v in (idx.get(section) or {}).items():
            v = dict(v or {})
            v.update(kind=kind, code=code, source="INDEX.yaml", derived=False)
            codes[code] = v

    # DERIVED — read from the owner, never copied into INDEX.yaml
    for pr in load_jsonl(P("ledger/PROMISES.jsonl")):
        codes[f"PRM-{pr['id']}"] = dict(
            kind="PRM", code=f"PRM-{pr['id']}", derived=True,
            source="ledger/PROMISES.jsonl", owner="ledger/PROMISES.jsonl",
            name=str(pr.get("setup") or pr["id"])[:100],
            status=pr.get("status"), raw=pr,
            aliases=[], note=str(pr.get("payoff") or pr.get("notes") or ""))

    for ft in load_jsonl(P("ledger/CANON_FACTS.jsonl")):
        codes[f"FCT-{ft['id']}"] = dict(
            kind="FCT", code=f"FCT-{ft['id']}", derived=True,
            source="ledger/CANON_FACTS.jsonl", owner="ledger/CANON_FACTS.jsonl",
            name=str(ft.get("fact") or ft["id"])[:100],
            status=ft.get("status"), raw=ft,
            aliases=[], note=str(ft.get("value") or ft.get("source") or ""))

    try:
        core = load_yaml(data("CORE.yaml")) or {}
    except OSError:
        core = {}
    for grp, items in (core.get("constraints") or {}).items():
        for it in items or []:
            codes[it["id"]] = dict(
                kind="CON", code=it["id"], derived=True, severity=grp,
                source=rel(data("CORE.yaml")), owner=rel(data("CORE.yaml")) + " > constraints",
                name=it.get("name", ""), note=it.get("rule", ""), aliases=[], raw=it)

    try:
        rules = (load_yaml(data("RULES.yaml")) or {}).get("rules") or {}
    except OSError:
        rules = {}
    for rid, r in rules.items():
        short = rid.split("_")[0]                 # R001_no_proximity… -> R001
        codes[short] = dict(
            kind="RUL", code=short, derived=True, full_id=rid,
            source=rel(data("RULES.yaml")), owner=r.get("owner", ""),
            name=rid, severity=r.get("severity"),
            note=" ".join(str(r.get("statement", "")).split()), aliases=[], raw=r)
    return codes


# ── RESOLVE A USER'S STRING TO A CODE ────────────────────────────────────────
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
def chapters():
    global _CH
    if _CH is None:
        povs = pov_map()
        _CH = []
        for f in prose_files():
            _CH.append(dict(
                stem=os.path.splitext(os.path.basename(f))[0], rel=rel(f),
                num=chapter_num(f), short=chapter_id(f),
                pov=pov_of(f, povs) or "?",
                lines=io.open(f, encoding="utf-8").read().split("\n")))
    return _CH

def prose_sites(aliases, limit=None):
    """Every live site of these aliases in the edit-of-record."""
    out = []
    if not aliases:
        return out
    # Aliases are literal substrings UNLESS prefixed "re:" — then the remainder is
    # a raw regex applied to the norm()'d line. Added 2026-08-06: literal-only
    # aliases were blind to inflection ("filed it away" vs alias "files it away")
    # and interposition ("words EVER landed") — five banned-construction sites
    # shipped in ARC v4 through that blindness. Author regexes against norm() text.
    pat = re.compile("|".join(
        str(a)[3:] if str(a).startswith("re:") else re.escape(norm(str(a)))
        for a in aliases), re.I)
    for ch in chapters():
        for i, line in enumerate(ch["lines"], 1):
            m = pat.search(norm(line))
            if m:
                out.append((ch["short"], ch["pov"], i, m.group(0), line.strip(), ch["rel"]))
                if limit and len(out) >= limit:
                    return out
    return out


# ── DOSSIER ──────────────────────────────────────────────────────────────────
def dossier(codes, code, show_prose=False):
    v = codes[code]
    kind = v["kind"]
    print()
    print(c(f"  {code}", "bold") + c(f"   {v.get('name','')}", "cyan"))
    print(c("  " + "─" * 74, "dim"))

    if v.get("status"):
        s = str(v["status"])
        col = "grn" if s in ("paid", "canonical") else "yel" if s in ("open", "wobbling") else "dim"
        print(f"  {'status':14}{c(s, col)}")
    for f in ("severity", "polarity", "scope", "voice", "core_id"):
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

    # raw payload for derived codes (the ledger row / the constraint / the rule)
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
            g = str(g)
            tgt = codes.get(g) or codes.get(g.split("_")[0])
            if tgt:
                print(f"    {c(tgt['code'].ljust(10), 'yel')} {str(tgt.get('note') or tgt.get('name'))[:62]}")
            else:
                print(f"    {c(g.ljust(10), 'red')} ⚠ BROKEN LINK — no such code")

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
        sites = prose_sites(al)
        print()
        print(c(f"  IN THE MANUSCRIPT   {len(sites)} sites", "bold") +
              c(f"  ({', '.join(str(a) for a in al)})", "dim"))
        if not sites:
            print(c("    none — this code names nothing in the prose. Codex-only.", "yel"))
        else:
            chs = sorted({s[0] for s in sites}, key=lambda x: int(re.sub(r"\D", "", x) or 999))
            print(f"    {c('chapters', 'dim')}  {', '.join(chs)}")
            show = sites if show_prose else sites[:6]
            for shrt, pov, i, hit, line, rel in show:
                print(f"    {c((shrt + ':' + str(i)).ljust(11), 'grn')} {c('[' + pov[:14] + ']', 'dim')} {line[:74]}")
            if not show_prose and len(sites) > 6:
                print(c(f"    … {len(sites) - 6} more — rerun with --prose", "dim"))

    # who else points here
    back = [k for k, o in codes.items()
            if code in [str(x) for x in (o.get("see") or [])] and k != code]
    if back:
        print()
        print(c("  FILED UNDER THIS BY", "bold") + "  " + ", ".join(c(b, "cyan") for b in back))

    # decisions
    dl = P("ledger/DECISIONS_LOG.md")
    if os.path.exists(dl) and (al or v.get("name")):
        terms = [str(x) for x in al] + [str(v.get("name", ""))]
        hits = [ln.strip() for ln in io.open(dl, encoding="utf-8")
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

def do_list(codes, filt):
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

def do_find(codes, q):
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

    sites = prose_sites([norm(q)])
    print()
    print(c(f"  IN THE MANUSCRIPT   {len(sites)} sites", "bold"))
    for shrt, pov, i, hit, line, rel in sites[:20]:
        print(f"    {c((shrt + ':' + str(i)).ljust(11), 'grn')} {c('[' + pov[:14] + ']', 'dim')} {line[:74]}")
    if len(sites) > 20:
        print(c(f"    … {len(sites) - 20} more", "dim"))

    cf = []
    for f in sorted(set(sum([glob.glob(P(g)) for g in CFG["codex_globs"]], []))):
        if os.path.basename(f) in ("INDEX.yaml", "RULES.yaml", "RULES_CANDIDATES.yaml", "CODEX_CHANGELOG.md"):
            continue
        for i, ln in enumerate(io.open(f, encoding="utf-8", errors="replace").read().split("\n"), 1):
            if ql in norm(ln).lower():
                cf.append((os.path.relpath(f, REPO), i, ln.strip()))
    print()
    print(c(f"  IN THE CODEX   {len(cf)} sites", "bold") +
          c("   ← if the prose count is 0 and this is not, you have a fossil", "dim"))
    for f, i, ln in cf[:12]:
        print(f"    {c((f + ':' + str(i)), 'yel')}  {ln[:66]}")
    print()

def do_gaps(codes, enforce=False):
    """What the filing system does NOT know. The system reporting its own holes.
    enforce=True: return 1 if any HARD defect exists (gate mode for the pre-commit wall).
    Hard = broken cross-ref, a banned/absent code appearing in prose, or a wobbling/
    contradicted fact. Open setups, unfiled characters and 'names nothing' are warnings."""
    print()
    print(c("  GAPS — what is not filed, and what is filed but dead", "bold"))
    print(c("  " + "─" * 74, "dim"))
    n = 0
    hard = 0   # gate-blocking subset of n

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

    # 2. characters in CHARACTERS.yaml with no code
    try:
        chars = characters()
        filed = " ".join(str(v.get("name", "")) + str(v.get("owner", ""))
                         for v in codes.values() if v["kind"] == "CHR").upper()
        unfiled = [k for k in chars if k.upper().replace("_", " ").split()[-1] not in filed
                   and k.upper() not in filed]
        if unfiled:
            n += len(unfiled)
            print()
            print(c(f"  ! {len(unfiled)} CHARACTER(S) IN CHARACTERS.yaml WITH NO CODE", "yel"))
            for u in unfiled:
                print(f"      {u}")
    except Exception as e:
        print(c(f"  (character check failed: {e})", "dim"))

    # 3. EXPECTATION CHECK — the direction of the test depends on the code.
    #    For a banned word or a protected reveal, ZERO hits is the PASS and any
    #    hit is the DEFECT. Encoding this is what stops the next agent reading
    #    "0 sites" as "dead code" and deleting the guard.
    absent_ok, absent_violated, unexplained = [], [], []
    for v in codes.values():
        al = v.get("aliases") or []
        if not al:
            continue
        allow = [norm(str(x)) for x in (v.get("allow") or [])]
        live = [st for st in prose_sites(al)
                if not any(a in norm(st[4]) for a in allow)]     # sanctioned sites are not violations
        if v.get("expect_in_prose") == "absent":
            (absent_violated if live else absent_ok).append(v)
        elif not live and v.get("status") != "CODEX-ONLY":
            unexplained.append(v)

    if absent_violated:
        n += len(absent_violated)
        hard += len(absent_violated)
        print()
        print(c(f"  ✗ {len(absent_violated)} CODE(S) APPEAR IN THE PROSE THAT MUST NOT", "red"))
        for v in absent_violated:
            print(f"      {c(v['code'].ljust(24), 'red')} {str(v.get('note',''))[:52]}")
            # recompute THIS code's sites — `live` above is the last-iterated code's
            # leftover; reusing it printed every violation at the wrong location.
            vallow = [norm(str(x)) for x in (v.get("allow") or [])]
            vsites = [st for st in prose_sites(v.get("aliases") or [])
                      if not any(a in norm(st[4]) for a in vallow)]
            for shrt, pov, i, hit, line, rel in vsites[:3]:
                print(f"        {c(shrt + ':' + str(i), 'red')} [{pov[:12]}] {line[:58]}")
    if absent_ok:
        print()
        print(c(f"  ✓ {len(absent_ok)} ABSENCE(S) HOLDING", "grn") +
              c("   zero hits is the PASS for these — bans and protected reveals", "dim"))
        for v in absent_ok:
            print(f"      {c(v['code'].ljust(24), 'grn')} {str(v.get('note',''))[:52]}")
    if unexplained:
        n += len(unexplained)
        print()
        print(c(f"  ! {len(unexplained)} CODE(S) NAME NOTHING IN THE PROSE", "yel") +
              c("   undeclared — fossil, or needs expect_in_prose: absent", "dim"))
        for v in unexplained:
            print(f"      {v['code'].ljust(24)}")

    # 4. unpaid setups
    open_prm = [v for v in codes.values() if v["kind"] == "PRM" and v.get("status") == "open"]
    if open_prm:
        print()
        print(c(f"  · {len(open_prm)} OPEN SETUP(S)", "cyan") +
              c(f"   candidate holes — only {CFG['author']} rules them red-herring/unimportant", "dim"))
        for v in open_prm:
            print(f"      {v['code'].ljust(28)} {str(v.get('name',''))[:46]}")

    # 5. wobbling facts
    wob = [v for v in codes.values() if v["kind"] == "FCT" and v.get("status") in ("wobbling", "contradicted")]
    if wob:
        n += len(wob)
        # NOT hard: wobbling/contradicted facts are a 'flag for the author's ruling' state
        # (repo principle: flag, don't fix). Surfaced, but must not block unrelated commits.
        print()
        print(c(f"  ✗ {len(wob)} FACT(S) WOBBLING OR CONTRADICTED", "red"))
        for v in wob:
            print(f"      {v['code'].ljust(28)} {str(v.get('name',''))[:46]}")

    print()
    print(c("  " + "─" * 74, "dim"))
    if n == 0:
        print(c("  NO GAPS", "grn") + "  — every code resolves, every code lives in the book.")
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
    ap.add_argument("code", nargs="?", help="a filing code, or any fuzzy fragment of one")
    ap.add_argument("--list", nargs="?", const="", metavar="KIND")
    ap.add_argument("--find", metavar="TEXT", help="which code owns this string?")
    ap.add_argument("--gaps", action="store_true", help="what the system does not know")
    ap.add_argument("--enforce", action="store_true",
                    help="gate mode: run --gaps and exit 1 on any HARD defect (for the pre-commit wall)")
    ap.add_argument("--prose", action="store_true", help="every prose site, not the first 6")
    a = ap.parse_args()

    codes = build()

    if a.enforce:
        return do_gaps(codes, enforce=True)
    if a.gaps:
        return do_gaps(codes)
    if a.find:
        return do_find(codes, a.find) or 0
    if a.list is not None:
        return do_list(codes, a.list) or 0
    if not a.code:
        print(__doc__)
        print(c(f"  {len(codes)} codes filed. --list to see them.\n", "dim"))
        return 0

    hits = resolve(codes, a.code)
    if not hits:
        print(c(f"\n  no code matches {a.code!r}.", "red"))
        print(c("  --list to see them all, or --find to search the prose instead.\n", "dim"))
        return 1
    if len(hits) > 8:
        print(c(f"\n  {a.code!r} matches {len(hits)} codes:", "yel"))
        for h in hits:
            print(f"    {c(h.ljust(28), 'cyan')} {str(codes[h].get('name',''))[:44]}")
        print()
        return 0
    for h in hits:
        dossier(codes, h, show_prose=a.prose)
    return 0


if __name__ == "__main__":
    sys.exit(main())
