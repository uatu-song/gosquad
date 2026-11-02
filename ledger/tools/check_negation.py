#!/usr/bin/env python3
"""check_negation.py — the negation-restatement detector (Resonance R008b).

Five shapes, NARRATION ONLY (dialogue inside quotes is excluded):
  1. "Not X. Y."            verbless corrective at sentence start
  2. "It isn't X. It's Y."  copula corrective
  3. "X and not Y" / "not X but Y"
  4. "not X—Y"              em-dash corrective
  5. "It does not X. It does not Y."  paired negative declaratives
Prints every site as chapter:line + the full line, so the author reads sentences, not a
summary. Exit 1 if any site exists (gate mode); --census always exits 0.

In Resonance the author banned all five shapes (2026-09-05): "When Joe bans a shape, the
answer is a count of zero, not a list of survivors." For a new book that ban is a
CANDIDATE until the author rules it — run with --census and show him the sites.

Usage: check_negation.py [--census]
Validated 2026-09-05 against the Resonance ARC text (89 sites) and v7 (87).
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import CFG, prose_files, chapter_id, in_dialogue

# apostrophes: match curly AND straight (a straight-only pattern returns zero on curly text)
SHAPES = {
 "Not X. Y.":        re.compile(r"(?:^|[.!?—]\s+)Not\s+[a-z][^.!?\n]{0,40}\.\s+[A-Z][^.!?\n]{0,40}\.", re.M),
 "It isn't X. Y.":   re.compile(r"\bIt (?:isn[’']t|wasn[’']t|is not|was not)\s+[^.!?\n]{1,40}\.\s+(?:Just\s+)?[A-Z][^.!?\n]{0,40}\."),
 "X and not Y":      re.compile(r"\b\w+ and not (?:a |an |the )?\w+\b|\bnot (?:a |an |the )?\w+ but (?:a |an |the )?\w+\b"),
 "not X—Y":          re.compile(r"\b[Nn]ot [^—.\n]{1,30}—(?:just )?[a-z]"),
 "does not… does not": re.compile(r"\b(?:It|She|He|The \w+) (?:does|did) not \w+[^.!?\n]{0,20}\.\s+(?:It|She|He|The \w+) (?:does|did) not \w+"),
}
def main():
    skip = set(CFG.get("narration_skip_chapters") or [])
    sites, seen = [], set()
    for f in prose_files():
        ch = chapter_id(f)
        if ch in skip: continue
        for i, line in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
            for name, p in SHAPES.items():
                for mm in p.finditer(line):
                    if in_dialogue(line, mm.start()): continue
                    if (ch, i) in seen: continue
                    seen.add((ch, i)); sites.append((ch, i, name, line))
    for ch, i, name, line in sites:
        print(f"[{ch}:{i}] ({name}) {line}")
    print(f"\nNEGATION SITES IN NARRATION: {len(sites)}")
    if "--census" in sys.argv: return 0
    return 1 if sites else 0

if __name__ == "__main__":
    sys.exit(main())
