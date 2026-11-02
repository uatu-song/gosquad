#!/usr/bin/env python3
"""
check_time.py — LIVE catalogue of every time-figure in the prose.

WHY THIS EXISTS (Resonance, 2026-07-18): time-figures ("fourteen months ago", "since she
was seven", "three years") are the most error-prone canon in a book — the same phrase
points at different anchor events at different sites, and a STORED table of them
fossilizes (Resonance's TIMELINE.yaml drifted to "6 months ago" while the ruled spine
said ~14). So this tool stores NOTHING. It greps the prose live and lists every figure
with its site, so each can be reconciled BY HAND against the one ruled timeline
(file it in ledger/CANON_FACTS.jsonl, e.g. id "master-timeline", and read it with
codex.py FCT-master-timeline).

The book's own anchor events ("since the Drop") go in suite.time_anchor_events.
It is a lister, not a judge.
"""
import collections, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import CFG, prose_files, chapter_id

def norm(s):  # curly apostrophes break naive patterns
    return s.replace("’", "'").replace("‘", "'")

NUM = (r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
       r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
       r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|\d+)")
PATS = [
    re.compile(rf"\b{NUM}(?:[- ]{NUM})?\s+(?:month|year|week|day|hour|minute|decade|centur)"
               rf"(?:s|ies|y)?\s+(?:ago|later|earlier|before|after|old)", re.I),
    re.compile(r"\bsince (?:she|he|they|it|I|we) (?:was|were) \w+", re.I),
    re.compile(rf"\bfor (?:the past |the last )?{NUM}\s+(?:month|year|week|day|hour)s?", re.I),
    re.compile(rf"\b{NUM}\s+(?:months?|years?)\b(?!\s+(?:old|ago))", re.I),  # bare "eighteen months"
    re.compile(r"\b(?:that same|the next|the following|the previous) (?:night|day|morning|evening|week)\b", re.I),
]
anchors = [re.escape(a) for a in (CFG.get("time_anchor_events") or [])]
if anchors:
    PATS.append(re.compile(r"\b(?:since|before|after) the (?:" + "|".join(anchors) + r")\b", re.I))

def figures():
    by_phrase = collections.defaultdict(list)
    for path in prose_files():
        chap = chapter_id(path)
        for i, raw in enumerate(open(path, encoding="utf-8"), 1):
            line = norm(raw)
            for pat in PATS:
                for m in pat.finditer(line):
                    ph = re.sub(r"\s+", " ", m.group(0).strip().lower())
                    by_phrase[ph].append((chap, i, line.strip()[:100]))
    return by_phrase

def main():
    bp = figures()
    total = sum(len(v) for v in bp.values())
    print(f"TIME-FIGURE CATALOGUE — {CFG['book']} — {len(bp)} distinct phrases, {total} sites (live grep)")
    print("Reconcile each against the ruled timeline (codex.py FCT-master-timeline once filed).")
    print("─" * 66)
    for ph in sorted(bp, key=lambda p: (-len(bp[p]), p)):
        sites = bp[ph]
        print(f"\n  “{ph}”  ×{len(sites)}")
        for chap, ln, snip in sites:
            print(f"      {chap}:{ln}  {snip}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
