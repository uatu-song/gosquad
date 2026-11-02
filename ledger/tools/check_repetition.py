#!/usr/bin/env python3
"""Flag repeated distinctive phrases (n-grams) across the manuscript.

Reads globs, thresholds, and motif exemptions from ledger/config.json.
A phrase flags when it appears >= flag_threshold_per_file times in one file,
or when its cumulative count exceeds flag_threshold_per_10k_words per 10k
words of total manuscript. Registered motifs are exempt. N-grams made
entirely of stopwords are ignored.

This is a crude flagger by design: it surfaces candidates; a human (or a
Claude session reading in context) judges them. Exit code is always 0 —
repetition is a review item, not a build failure.

Globs: "manuscript_globs" in ledger/config.json, else suite.prose_globs.
Tokenizer (fixed for the suite): curly apostrophes are folded to straight BEFORE
tokenizing, so "doesn’t" is one token. The Resonance version split it into
"doesn t", which buried the real signal under ~5,900 contraction artifacts.

Usage: python3 ledger/tools/check_repetition.py [repo-root]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

STOPWORDS = set(
    "the a an and or but of to in on at for with from by as is was were are be been being "
    "it its he she they them his her their that this these those i you we me my your our "
    "had has have do did not no so if then than there here when where what who how".split()
)


def tokenize(text: str):
    text = text.replace("\u2019", "'").replace("\u2018", "'").lower()
    return [t.strip("'") for t in re.findall(r"[a-z0-9']+", text) if t.strip("'")]


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    cfg_path = root / "ledger" / "config.json"
    if not cfg_path.exists():
        print(f"ERROR: {cfg_path} not found")
        return 0
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    motifs = [m.lower() for m in cfg.get("motifs", [])]
    sizes = cfg.get("ngram_sizes", [2, 3, 4])
    per_file_thresh = cfg.get("flag_threshold_per_file", 3)
    per_10k = cfg.get("flag_threshold_per_10k_words", 4)

    files = []
    for g in cfg.get("manuscript_globs") or (cfg.get("suite") or {}).get("prose_globs", []):
        files.extend(sorted(root.glob(g)))
    files = [f for f in dict.fromkeys(files) if f.is_file()]
    if not files:
        print(f"No manuscript files matched globs in {cfg_path.name} (root: {root}).")
        print("Adjust manuscript_globs to the repo's chapter layout.")
        return 0

    total_words = 0
    cumulative = Counter()
    per_file_hits = defaultdict(list)  # ngram -> [(file, count)]

    for f in files:
        toks = tokenize(f.read_text(encoding="utf-8", errors="replace"))
        total_words += len(toks)
        counts = Counter()
        for n in sizes:
            for i in range(len(toks) - n + 1):
                gram = toks[i:i + n]
                if all(w in STOPWORDS for w in gram):
                    continue
                counts[" ".join(gram)] += 1
        for gram, c in counts.items():
            cumulative[gram] += c
            if c >= per_file_thresh:
                per_file_hits[gram].append((f.name, c))

    def is_motif(gram: str) -> bool:
        return any(m in gram or gram in m for m in motifs)

    cum_thresh = max(per_file_thresh, round(per_10k * total_words / 10000))
    flags = []
    for gram, c in cumulative.items():
        if is_motif(gram):
            continue
        in_file = per_file_hits.get(gram, [])
        if in_file or c >= cum_thresh:
            # suppress sub-phrases of longer flagged phrases with same count
            flags.append((c, gram, in_file))

    # keep longest version of nested phrases
    flags.sort(key=lambda x: (-x[0], -len(x[1])))
    kept, seen_text = [], []
    for c, gram, in_file in flags:
        if any(gram in longer and c <= lc for lc, longer, _ in kept):
            continue
        kept.append((c, gram, in_file))

    print(f"REPETITION CHECK — {len(files)} files, {total_words} words "
          f"(cumulative threshold: {cum_thresh}, per-file: {per_file_thresh})")
    if not kept:
        print("No phrases flagged.")
        return 0
    print(f"\nFLAGGED ({len(kept)}) — candidates for review, motifs exempt:")
    for c, gram, in_file in kept[:60]:
        loc = "; ".join(f"{name}×{n}" for name, n in in_file) if in_file else "spread across files"
        print(f"  {c:>4}×  \"{gram}\"  [{loc}]")
    if len(kept) > 60:
        print(f"  … and {len(kept) - 60} more (raise thresholds in config.json if noisy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
