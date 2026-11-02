#!/usr/bin/env python3
"""check_thing.py — placeholder-'thing' census (Resonance R008c, 2026-09-05).

Author's rule in Resonance, verbatim: "'Thing'? What thing? Don't be so abstract. Either
use a noun or leave out that sentence."  Discriminator used there (author may veto by class):
  A  placeholder for a noun the narrator can name, or a pure-abstraction gloss -> NOUN or CUT
  B  ordinary usage with a concrete referent in the sentence ("the only thing left to hear") -> left
  C  the POV genuinely cannot name it yet, or a deliberate insult ("A thing.") -> left
Prints every BLOCK-shape narration site with context, plus the total narration count.
For a new book this is a CANDIDATE rule until the author rules it.

Usage: check_thing.py [--census] [--sites]   (--sites: every narration 'thing', not just block shapes)
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import CFG, prose_files, chapter_id

BLOCK = re.compile(r"\bof (?:a|the) thing (?:that|gone|which|already|being)\b|\ba (?:\w+ )?thing (?:she|he|they|you|it) (?:knows?|knew|carried|carries|decided|meant|means|could|can|had)\b|\bthe wrongest thing\b|\ba stronger thing\b")
strip = lambda t: re.sub(r'“[^”]*”|"[^"\n]*"|\*things?\*', "", t)

def main():
    skip = set(CFG.get("narration_skip_chapters") or [])
    total = 0; block = []; every = []
    for f in prose_files():
        ch = chapter_id(f)
        if ch in skip: continue
        for i, raw in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
            t = strip(raw)
            for m in re.finditer(r"\bthings?\b", t, re.I):
                total += 1
                every.append((ch, i, t[max(0, m.start()-60):m.end()+40].strip()))
            for m in BLOCK.finditer(t):
                block.append((ch, i, t[max(0, m.start()-60):m.end()+40].strip()))
    for ch, i, s in (every if "--sites" in sys.argv else block):
        print(f"[{ch}:{i}] …{s}…")
    print(f"\nnarration 'thing' total: {total}   BLOCK-shape sites: {len(block)}")
    if "--census" in sys.argv: return 0
    return 1 if block else 0

if __name__ == "__main__":
    sys.exit(main())
