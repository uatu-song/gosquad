#!/usr/bin/env python3
"""
ferret.py — REPEATED-CONSTRUCTION MINER. Finds the formulas the rules don't
know about yet: empirical n-gram mining over narration, the full negative-
construction family with per-chapter counts, and sentence-starter frequency.

    python3 _canon/tools/ferret.py --book book_2
    python3 _canon/tools/ferret.py --compare book_1_ed1 book_2

WHY. The documented tics (the-particular, not-constructions) were found by
hand-reading. This mines them mechanically, so each new draft generation can
be ferreted for NEW mutations — the amplification mechanism guarantees each
book develops different ones (PROSE_VOICE_DESIGN_PROBLEM.md). The 2026-07-26
pass on the first editions found mutations the 2026-04 audit missed: "in her
chest" (41 uses across both books), the "X's voice was" formula (~50 in Book
2), and "Didn't X. Didn't Y." as a late-stage variant.

THE FUNCTION TEST still applies to everything this prints: a repeated phrase
may be a deliberate motif, not a defect ("hand still reaching" ×9 in Book 2
reads as an intentional image). This tool surfaces; only the Director rules.
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bookconfig as cfg
from bookconfig import norm

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", cyan="\033[36m",
         dim="\033[2m", bold="\033[1m", off="\033[0m")


def c(s, k):
    return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else str(s)


SKIP = re.compile(r"^\s*(<!--|-{3,}\s*$|#{1,6}\s)")

NEG = {
    "not-X-but-Y":        re.compile(r"\b[Nn]ot [^.!?;]{1,40}, but\b"),
    "not-X-just-Y":       re.compile(r"\b[Nn]ot [^.!?;]{1,40}, just\b"),
    "wasnt-X-it-was":     re.compile(r"\b(?:was|is|are|did|does)n't [^.!?;]{1,36}\. It was\b"),
    "not-X-period-not-Y": re.compile(r"\b[Nn]ot [^.!?;]{1,30}\. Not \b"),
    "no-X-no-Y":          re.compile(r"\b[Nn]o [^.!?;,]{1,20}, no [^.!?;,]{1,24}[,.]"),
    "so-much-as":         re.compile(r"\bso much as\b"),
    "not-because":        re.compile(r"\b[Nn]ot because\b"),
    "less-X-than":        re.compile(r"\bless [a-z]+ than\b"),
    "never-X-only":       re.compile(r"\b[Nn]ever [^.!?;]{1,30}, only\b"),
    "didnt-X-didnt":      re.compile(r"\b[Dd]idn't [^.!?;]{1,30}\. Didn't\b"),
    "wasnt-just":         re.compile(r"\b(?:was|is)n't just\b"),
    "not-quite":          re.compile(r"\b[Nn]ot quite\b"),
    "not-yet":            re.compile(r"\b[Nn]ot yet[,.]"),
    "nothing-X-just":     re.compile(r"\b[Nn]othing [^.!?;]{1,30}, just\b"),
}

STOP = set("""the a an and or but of to in on at for with from by as is was are were be been being
that this these those it its he she his her him they them their we our you your i my me not no""".split())


def strip_dialogue(t):
    return re.sub(r'"[^"]*"', " ", t)


def load(bookkey):
    book = cfg.load(bookkey)
    out = []
    for f in book.prose_files(strict=True):
        lines = [l for l in open(f, encoding="utf-8", errors="replace").read().split("\n")
                 if not SKIP.match(l)]
        out.append((book.short(f), norm("\n".join(lines))))
    return out


def neg_census(chs):
    per, examples = defaultdict(Counter), defaultdict(list)
    for short, text in chs:
        for name, pat in NEG.items():
            for m in pat.finditer(text):
                per[name][short] += 1
                if len(examples[name]) < 4:
                    examples[name].append((short, m.group(0)[:70]))
    return per, examples


def ngram_mine(chs, n_lo=3, n_hi=6, min_count=8):
    counts = Counter()
    for _, text in chs:
        words = re.findall(r"[a-z']+", strip_dialogue(text).lower())
        for n in range(n_lo, n_hi + 1):
            for i in range(len(words) - n):
                counts[tuple(words[i:i + n])] += 1
    keep = {}
    for g, cnt in counts.items():
        if cnt < min_count or not [w for w in g if w not in STOP]:
            continue
        keep[" ".join(g)] = cnt
    final = dict(keep)
    for g1 in list(keep):          # drop shorter grams subsumed by longer ones
        for g2 in keep:
            if g1 != g2 and g1 in g2 and keep[g2] >= keep[g1] * 0.8:
                final.pop(g1, None)
                break
    return Counter(final)


def starters(chs, min_count=15):
    cnt = Counter()
    for _, text in chs:
        for s in re.split(r"[.!?]+", strip_dialogue(text)):
            w = re.findall(r"[A-Za-z']+", s)
            if len(w) >= 2:
                cnt[f"{w[0].lower()} {w[1].lower()}"] += 1
    return Counter({k: v for k, v in cnt.items() if v >= min_count})


def report(bookkey):
    chs = load(bookkey)
    total_w = sum(len(t.split()) for _, t in chs)
    print(c(f"\n{'=' * 78}\n{bookkey}  —  {len(chs)} chapters, {total_w:,} words\n{'=' * 78}", "bold"))

    per, ex = neg_census(chs)
    print(c("\nNEGATIVE-CONSTRUCTION FAMILY  (narration + dialogue)", "bold"))
    grand = 0
    for name in sorted(per, key=lambda n: -sum(per[n].values())):
        tot = sum(per[name].values())
        grand += tot
        chsl = " ".join(f"{k}:{v}" for k, v in sorted(per[name].items())[:12])
        print(f"  {c(name.ljust(22), 'yel')} {tot:4}   {c(chsl, 'dim')}{' …' if len(per[name]) > 12 else ''}")
        for short, e in ex[name][:2]:
            print(c(f"      {short}  “{e}”", "dim"))
    print(f"  {'TOTAL':22} {grand:4}   ({grand / (total_w / 1000):.1f}/1K words)")

    print(c("\nREPEATED CONSTRUCTIONS — mined n-grams (narration only, ≥8 uses)", "bold") +
          c("  function-test before ruling: motifs are exempt", "dim"))
    mined = ngram_mine(chs)
    for g, cnt in mined.most_common(28):
        print(f"  {cnt:5}  {g}")

    print(c("\nSENTENCE STARTERS (first two words, narration, ≥15 uses)", "bold"))
    for g, cnt in starters(chs).most_common(15):
        print(f"  {cnt:5}  {g}")
    return mined


def main():
    ap = argparse.ArgumentParser()
    cfg.add_book_arg(ap)
    ap.add_argument("--compare", nargs=2, metavar=("BOOK_A", "BOOK_B"),
                    help="mine both books and show shared constructions (the AI defaults)")
    a = ap.parse_args()
    if a.compare:
        m1, m2 = report(a.compare[0]), report(a.compare[1])
        print(c(f"\n{'=' * 78}\nSHARED ACROSS BOTH (AI defaults, not book-specific mutations)\n{'=' * 78}", "bold"))
        shared = set(m1) & set(m2)
        for g in sorted(shared, key=lambda g: -(m1[g] + m2[g]))[:20]:
            print(f"  {a.compare[0]}:{m1[g]:4}  {a.compare[1]}:{m2[g]:4}   {g}")
        return 0
    report(a.book or cfg.load(None).key)
    return 0


if __name__ == "__main__":
    sys.exit(main())
