#!/usr/bin/env python3
"""
check_typography.py — the round-trip drift gate.

WHY THIS EXISTS. Markdown/plain-text round trips silently rewrite typography on
import: curly quotes flatten to straight, closed em dashes open to the spaced
form, `. . .` collapses to `...`. On the repo this system came from, four such
imports were promoted, audited, sealed and SHIPPED to contest judges before
anyone compared the character inventory to the last clean state.

Two reasons this is a separate tool and not more RULES.yaml patterns:
  1. audit.py's norm() folds curly→straight and —→"--" BEFORE matching, so a
     typography rule written the obvious way either never fires or flags the
     whole clean manuscript. Both happened. This reads RAW bytes.
  2. Drift arrives in BULK from an import, so a census beats a line-by-line
     flag: the counts tell you instantly whether prose changed or a converter
     ran over the whole book.

THIS PROJECT: the house style is declared in _canon/books.yaml and is currently
UNRULED, so the gate runs in census mode (`typography.enforce: false`) and
cannot block. It reports drift against whatever house style is declared. Flip
`enforce: true` once the Director rules — see docs/VERIFICATION_MANUAL.md.

Usage:
    python3 _canon/tools/check_typography.py               # gate (honours enforce)
    python3 _canon/tools/check_typography.py --census      # counts only, never fails
    python3 _canon/tools/check_typography.py --book book_1
Exit 0 = clean (or census/unruled). Exit 1 = drift, and enforcement is on.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bookconfig as cfg

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", dim="\033[2m", bold="\033[1m", off="\033[0m")


def c(s, k):
    return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else str(s)


# Each check is (key, label, pattern, why). Which ones RUN depends on the
# declared house style — enforcing curly quotes on a straight-quote manuscript
# would flag every line, and a noisy gate is an ignored gate.
def checks_for(house, always_banned):
    out = []
    if house.get("double_quote") == "curly":
        out.append(("straight double quote", re.compile(r'"'),
                    'house style is curly “ ” — plain-text/markdown import drift'))
    elif house.get("double_quote") == "straight":
        out.append(("curly double quote", re.compile(r"[“”]"),
                    'house style is straight " — mixed quoting means a partial import'))

    if house.get("apostrophe") == "curly":
        out.append(("straight apostrophe in word", re.compile(r"(?<=[A-Za-z])'(?=[A-Za-z])"),
                    "house style is curly ’ (don’t, it’s) — import drift"))
    elif house.get("apostrophe") == "straight":
        out.append(("curly apostrophe in word", re.compile(r"(?<=[A-Za-z])’(?=[A-Za-z])"),
                    "house style is straight ' — mixed apostrophes mean a partial import"))

    if house.get("em_dash") == "closed":
        out.append(("floating em dash ( — )", re.compile(r"[ ]—[ ]"),
                    "house style is closed word—word (Chicago); spaced is the AP/web default"))
    elif house.get("em_dash") == "spaced":
        out.append(("closed em dash (word—word)", re.compile(r"(?<=\w)—(?=\w)"),
                    "house style is spaced word — word"))
    out.append(("mis-faced interruption quote (—“)", re.compile(r"(?<=\S)—“"),
                "a dash-interrupted line CLOSES: should be —”"))

    ell = house.get("ellipsis")
    if ell == "spaced":
        out += [("ellipsis character (…)", re.compile(r"…"), "house style is spaced periods '. . .'"),
                ("collapsed ellipsis (...)", re.compile(r"(?<!\.)\.\.\.(?!\.)"), "house style is spaced periods '. . .'")]
    elif ell == "collapsed":
        out.append(("ellipsis character (…)", re.compile(r"…"),
                    "house style is three periods '...' — the … glyph is import drift"))

    if "stray_bold" in always_banned:
        out.append(("stray bold (**x**)", re.compile(r"\*\*"),
                    "house style is single-* italics; ** renders as literal * glyphs in the build"))
    if "underscore_italics" in always_banned:
        out.append(("underscore italics (_x_)", re.compile(r"(?<![A-Za-z0-9])_[^_\n]+_(?![A-Za-z0-9])"),
                    "house style is *asterisks* — underscores create phantom breaks in the build"))
    return out


# Structural markdown that is provenance, not prose. chapters_split/ files open
# with `# Chapter N: Title` and `<!-- STRUCT: … -->` comments; flagging those as
# typography would be a false-positive machine.
SKIP_LINE = re.compile(r"^\s*(<!--|-{3,}\s*$|#{1,6}\s)")


def main():
    ap = argparse.ArgumentParser()
    cfg.add_book_arg(ap)
    ap.add_argument("--census", action="store_true", help="counts only, never fails")
    a = ap.parse_args()

    book = cfg.load(a.book)
    typo = book.typography or {}
    enforce = bool(typo.get("enforce", False)) and not a.census
    house = typo.get("house") or {}
    CHECKS = checks_for(house, typo.get("always_banned") or [])

    files = book.prose_files(strict=True)

    print(c("TYPOGRAPHY — round-trip drift gate", "bold") + c(f"   [{book.key}]", "dim"))
    style = ", ".join(f"{k}={v}" for k, v in house.items()) or "(none declared)"
    print(c(f"  house: {style}", "dim"))
    print(c(f"  mode:  {'ENFORCING' if enforce else 'census only (books.yaml typography.enforce: false)'}", "dim"))

    # A gate that scans nothing must never print a checkmark. This is the exact
    # failure the imported version had: 0 files → "intact ✓" → exit 0.
    if not files:
        if not book.prose_expected:
            print(c(f"\n  0 files — {book.key} is pre-prose by design. Nothing to check.", "dim"))
            return 0
        print(c("\n  ✗ 0 files scanned but prose was expected — refusing to report clean.", "red"))
        return 1

    hits = {}
    for f in files:
        raw = "\n".join(ln for ln in open(f, encoding="utf-8", errors="replace").read().split("\n")
                        if not SKIP_LINE.match(ln))
        for label, pat, why in CHECKS:
            n = len(pat.findall(raw))
            if n:
                hits.setdefault(label, {"why": why, "n": 0, "files": []})
                hits[label]["n"] += n
                hits[label]["files"].append((book.rel(f), n))

    if not hits:
        print(f"\n  {len(files)} files scanned, {len(CHECKS)} checks — house typography intact" + c("  ✓", "grn"))
        return 0
    for label, d in hits.items():
        print(c(f"\n  ✗ {d['n']:6}  {label}", "yel" if not enforce else "red"))
        print(c(f"          {d['why']}", "dim"))
        for rel, n in d["files"][:6]:
            print(f"          {n:6}  {rel}")
        if len(d["files"]) > 6:
            print(c(f"          … and {len(d['files']) - 6} more files", "dim"))
    if not enforce:
        print(c(f"\n  ({len(files)} files. Census only — not blocking. Declare a house style and set "
                f"typography.enforce: true in _canon/books.yaml to make this a wall.)", "dim"))
        return 0
    print(c("\n🚫 TYPOGRAPHY DRIFT — the import-shortcut class. Fix before committing.", "red"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
