#!/usr/bin/env python3
"""census.py — the anti-false-completion tool.

Any instruction of the form "get rid of X" must start and end here. It reports the
FULL population, never a filtered subset, and it detects displacement (the agent
trading one vague word for another).

  census.py "<regex>"                 population now: total / narration / dialogue / per chapter
  census.py "<regex>" --since <ref>   before -> after vs a git ref, plus DISPLACEMENT check
  census.py "<regex>" --sites         every occurrence with context (no filtering, ever)

Patterns run on RAW text: write curly ’ for apostrophes, or use [’'] to catch both.

Built 2026-08-07 (Resonance) after a sweep was reported complete four times while 300+
instances remained. The rule it enforces: a completion claim is a measured number, not a sentence.
"""
import collections, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import ROOT, prose_files, chapter_id, rel

CH = prose_files()
DIAL = re.compile(r'“[^”]*”|"[^"\n]*"')

def count(pat, text):
    return len(re.findall(pat, text, re.I))

def population(pat, at=None):
    tot = nar = dia = 0; per = collections.Counter()
    for f in CH:
        t = (subprocess.run(["git", "show", f"{at}:{rel(f)}"], capture_output=True, text=True, cwd=ROOT).stdout
             if at else open(f, encoding="utf-8").read())
        n = DIAL.sub(" ", t)
        c, cn = count(pat, t), count(pat, n)
        tot += c; nar += cn; dia += c - cn
        if c: per[chapter_id(f)] = c
    return tot, nar, dia, per

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    pat = sys.argv[1]
    if not CH: sys.exit("census: no prose files matched suite.prose_globs (ledger/config.json)")
    tot, nar, dia, per = population(pat)
    print(f"\n  PATTERN  {pat}")
    print(f"  TOTAL {tot}   narration {nar}   dialogue {dia}")
    print("  per chapter: " + " ".join(f"{k}:{v}" for k, v in per.most_common()))
    if "--sites" in sys.argv:
        print("\n  EVERY SITE (unfiltered):")
        for f in CH:
            for i, line in enumerate(open(f, encoding="utf-8"), 1):
                for m in re.finditer(pat, line, re.I):
                    print(f"    {chapter_id(f)}:{i}  …{line[max(0,m.start()-50):m.end()+50].strip()}…")
    if "--since" in sys.argv:
        ref = sys.argv[sys.argv.index("--since") + 1]
        o_tot, o_nar, _, _ = population(pat, at=ref)
        print(f"\n  vs {ref}:  total {o_tot} -> {tot}  ({tot-o_tot:+d})   narration {o_nar} -> {nar} ({nar-o_nar:+d})")
        print(f"  COMPLETION: {'CLEAN — narration at zero' if nar==0 else f'INCOMPLETE — {nar} narration instances remain'}")
        print("\n  DISPLACEMENT CHECK (did the fix just move the problem?):")
        for probe in [r"\ba thing\b", r"\bthings?\b", r"\bnothing\b", r"\bsomething\b", r"\bit\b"]:
            if probe.strip(r"\b") in pat: continue
            a, an, _, _ = population(probe, at=ref); b, bn, _, _ = population(probe)
            flag = "  <-- DISPLACED" if bn - an > 5 else ""
            print(f"    {probe:<16} narration {an} -> {bn}  ({bn-an:+d}){flag}")
    print()

if __name__ == "__main__":
    main()
