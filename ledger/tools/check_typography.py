#!/usr/bin/env python3
"""
TYPOGRAPHY — census, then (once the author rules a house style) the round-trip drift gate.

WHY THIS EXISTS (Resonance, 2026-07-24). The manuscript was 100% house-style, then
markdown revision rounds silently rewrote the typography on import — ~4,800 curly
quotes flattened to straight, 394 closed em dashes opened to the spaced form — and
four imports were promoted, sealed and SHIPPED to contest judges before anyone
compared the character inventory. The house rules existed in a document. Nothing
executed them.

TWO MODES
  1. CENSUS (always available; the only mode until the author rules):
         python3 ledger/tools/check_typography.py --census
     Per-chapter counts of every competing form. Show the author this BEFORE any
     conversion. Never fails.
  2. GATE (once ledger/config.json -> suite.typography_house_style is set):
         python3 ledger/tools/check_typography.py
     Exit 1 on any form the ruled style forbids. Run before every reseal.

suite.typography_house_style (each key optional; omit = not ruled, not enforced):
    "quotes":   "curly"                      flags straight " and in-word straight '
    "em_dash":  "closed" | "spaced"          flags the other form
    "italics":  "asterisk"                   flags **bold** and _underscore_ italics
    "ellipsis": "spaced" | "character" | "three-dot"
                 spaced = ". . ."   character = "…"   three-dot = "..."
Extra rendered files to scan (front/back matter) go in suite.typography_extra_files.

Two reasons this is not a RULES.yaml pattern: audit.py's norm() folds curly quotes
and em dashes BEFORE matching, so a typography rule there either never fires or
flags the whole clean book. This reads the RAW bytes. And drift arrives in BULK,
so a census tells you at once whether prose changed or a converter ran.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import ROOT, CFG, P, prose_files, chapter_id

FORMS = [  # (key, label, pattern) — every form counted in the census
    ("dq_straight", 'straight double quote (")', re.compile(r'"')),
    ("ap_straight", "straight apostrophe in word (don't)", re.compile(r"(?<=[A-Za-z])'(?=[A-Za-z])")),
    ("dq_curly",    "curly double quotes (“ ”)", re.compile(r"[“”]")),
    ("ap_curly",    "curly apostrophe/single (’ ‘)", re.compile(r"[’‘]")),
    ("em_spaced",   "spaced em dash ( — )", re.compile(r"[ ]—[ ]")),
    ("em_closed",   "closed em dash (word—word)", re.compile(r"\S—\S")),
    ("ell_char",    "ellipsis character (…)", re.compile(r"…")),
    ("ell_three",   "three-dot ellipsis (...)", re.compile(r"(?<!\.)\.\.\.(?!\.)")),
    ("ell_spaced",  "spaced ellipsis (. . .)", re.compile(r"\. \. \.")),
    ("bold",        "double-asterisk (**x**)", re.compile(r"\*\*")),
    ("underscore",  "underscore italics (_x_)", re.compile(r"(?<![A-Za-z0-9])_[^_\n]+_(?![A-Za-z0-9])")),
    ("dash_quote",  "mis-faced interruption quote (—“ with no close before it)",
     re.compile(r"^(?:[^”\n]*)(?<=\S)—“", re.M)),
]
LABEL = {k: l for k, l, _ in FORMS}

def forbidden(style):
    """Form keys the ruled house style forbids."""
    out = []
    if style.get("quotes") == "curly":
        out += ["dq_straight", "ap_straight", "dash_quote"]
    if style.get("em_dash") == "closed":
        out += ["em_spaced"]
    elif style.get("em_dash") == "spaced":
        out += ["em_closed"]
    if style.get("italics") == "asterisk":
        out += ["bold", "underscore"]
    e = style.get("ellipsis")
    if e:
        out += [k for k, v in (("ell_char", "character"), ("ell_three", "three-dot"),
                               ("ell_spaced", "spaced")) if v != e]
    return out

def files():
    out = prose_files()
    for g in CFG.get("typography_extra_files") or []:
        if os.path.exists(P(g)):
            out.append(P(g))
    return out

def read_rendered(f):
    if not f.endswith((".yaml", ".yml")):
        return open(f, encoding="utf-8").read()
    # in YAML a straight quote is usually syntax; inspect only the string VALUES
    import yaml
    vals = []
    def walk(o):
        if isinstance(o, dict):
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
        elif isinstance(o, str): vals.append(o)
    walk(yaml.safe_load(open(f, encoding="utf-8")))
    return "\n".join(vals)

def main():
    census = "--census" in sys.argv
    style = CFG.get("typography_house_style") or {}
    fs = files()
    if not fs:
        print("TYPOGRAPHY: no prose files matched suite.prose_globs"); return 1
    counts = {}   # file -> {key: n}
    for f in fs:
        raw = read_rendered(f)
        counts[f] = {k: len(p.findall(raw)) for k, _, p in FORMS}

    if census or not style:
        print(f"TYPOGRAPHY CENSUS — {CFG['book']} — {len(fs)} files")
        if not style:
            print("  house style NOT RULED (suite.typography_house_style is empty): census only.")
        keys = [k for k, _, _ in FORMS]
        tot = {k: sum(c[k] for c in counts.values()) for k in keys}
        print()
        for k in keys:
            print(f"  {tot[k]:7}  {LABEL[k]}")
        print("\n  per chapter (non-zero forms):")
        for f in fs:
            nz = " ".join(f"{k}={n}" for k, n in counts[f].items() if n)
            print(f"    {chapter_id(f):8} {nz}")
        return 0

    bad = forbidden(style)
    hits = {}
    for f in fs:
        for k in bad:
            if counts[f][k]:
                hits.setdefault(k, []).append((os.path.relpath(f, ROOT), counts[f][k]))
    print(f"TYPOGRAPHY GATE — {CFG['book']} — house style {style}")
    if not hits:
        print(f"  {len(fs)} files scanned — house typography intact  ✓")
        return 0
    for k, lst in hits.items():
        print(f"\n  ✗ {sum(n for _, n in lst):5}  {LABEL[k]}")
        for r, n in lst[:6]:
            print(f"          {n:5}  {r}")
        if len(lst) > 6:
            print(f"          … and {len(lst) - 6} more files")
    print("\n🚫 TYPOGRAPHY DRIFT — fix before sealing. Typography commits carry typography only.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
