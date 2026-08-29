#!/usr/bin/env python3
"""
check_style.py — band gate for cold-pass drafts against the ruled ch1-11 standard.

WHY BANDS. The first two metric rewrites (CH18, CH24, 2026-08-29) were gated on
one-sided floors, and CH24 sailed through while overshooting the author on the
LONG side — mean sentence 2x his, commas 115/1K vs his 60, similes 1.8x. A
floor proves the disease is gone; only a band proves the replacement is HIS
texture and not a third thing.

WHY NARRATION-ONLY. Dialogue is frozen by Director ruling ("don't change any
dialogue"), so the draft's dialogue is byte-identical to the source and gating
it measures nothing the agent controls. Worse, whole-text rates mislead: the
author's exclamation marks are 96% inside dialogue (0.23/1K narration vs 5.3
whole), so a low-dialogue chapter "suppressing" exclamations is actually
correct. Sentences are classified in place (>50% of a sentence's characters
inside quotes = dialogue); quoted spans are never split out and re-measured
separately — extraction manufactures sentence boundaries ("Really?" she asked.
is ONE sentence) and that error once put a wrong floor in front of the Director.

Author constants measured 2026-08-29 over ch1-11 of book_1_clean (23,488 words),
normalised via bookconfig.norm(). Bands are roughly +/-40% around the author,
snapped to round numbers. See canon/book_1_ed1/STYLE_PROFILE.md.

Usage:
    python3 _canon/tools/check_style.py DRAFT.txt --source CHAPTER.txt [--allow-chest N]
    --source: the first-edition chapter whose dialogue the draft freezes.
              Enables the dialogue byte-identity check and the length band
              (source words +/-20%). Omit for a free-standing measurement.
Exit 0 = all gates pass. Exit 1 = failures (each printed with its band).
"""
import argparse, os, re, sys, statistics as st
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bookconfig import norm

MOTIFS = {'the go squad', 'the hyper seed', 'the tamois heart', 'in frozen time'}

# (label, lo, hi) — narration-only unless stated. Author value in the comment.
BANDS = {
    'narr_burst':   (3.0, 12.0),   # 7.2  short (<=4w) narration sentences /1K whole
    'narr_mean':    (11.0, 20.0),  # 15.8 words
    'narr_median':  (9.0, 17.0),   # 13
    'narr_u10':     (25.0, 50.0),  # 35.9 % of narration sentences under 10 words
    'narr_20plus':  (20.0, 42.0),  # 31.5 %
    'narr_30plus':  (6.0, 17.0),   # 10.9 %
    'narr_em':      (0.0, 3.0),    # 1.1  /1K narration
    'narr_comma':   (40.0, 72.0),  # 55.1 /1K narration
    'narr_like':    (1.5, 5.5),    # 3.7  /1K narration
    'narr_ly':      (12.0, 27.0),  # 19.5 /1K narration
    'para_mean':    (22.0, 45.0),  # 32.9 words
}
BANS = [
    ('anaphoric "Not X. Not Y."', r'\bNot [^.]{1,25}\.\s+Not\b'),
    ('began/started to',          r'\b(?:began|started) to\b'),
    ('voice was / voice came out', r"voice (?:was|came out)"),
    ('"the particular"',          r'\bthe particular\b'),
]


def prep(path):
    t = open(path, encoding='utf-8').read()
    t = re.sub(r'<!--.*?-->', '', t, flags=re.DOTALL)
    return [l.strip() for l in norm(t).split('\n')
            if l.strip() and not re.match(r'^\s*(#|---)', l)]


def classify(flat):
    """Sentences with in-place dialogue classification. Never extract spans."""
    inq = [False] * len(flat)
    for m in re.finditer(r'"[^"]*"', flat):
        for i in range(m.start(), m.end()):
            inq[i] = True
    narr, dial, pos = [], [], 0
    for s in re.split(r"(?<=[.!?])\s+", flat):
        i = flat.find(s, pos)
        pos = i + len(s) if i >= 0 else pos
        if not s.strip():
            continue
        (dial if sum(inq[i:i+len(s)]) / max(len(s), 1) > 0.5 else narr).append(s)
    return narr, dial, inq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('draft')
    ap.add_argument('--source', help='first-edition chapter the draft freezes dialogue from')
    ap.add_argument('--allow-chest', type=int, default=1,
                    help='max "chest" uses (raise ONLY for chapters where the Seed/Heart seat is content)')
    a = ap.parse_args()

    paras = prep(a.draft)
    flat = ' '.join(paras)
    W = len(flat.split())
    if W == 0:
        print('✗ empty draft — refusing to report clean'); return 1
    narr, dial, _ = classify(flat)
    ntext = ' '.join(narr)
    NW = max(len(ntext.split()), 1)
    NL = [len(s.split()) for s in narr]
    results = []

    def band(key, val, label):
        lo, hi = BANDS[key]
        results.append((lo <= val <= hi, f'{label:44} {val:6.1f}   band {lo}-{hi}'))

    band('narr_burst', 1000 * sum(1 for x in NL if x <= 4) / W, 'narration short-burst /1K-of-whole')
    band('narr_mean', st.mean(NL), 'narration sentence mean')
    band('narr_median', st.median(NL), 'narration sentence median')
    band('narr_u10', 100 * sum(1 for x in NL if x < 10) / len(NL), 'narration % sentences <10 words')
    band('narr_20plus', 100 * sum(1 for x in NL if x >= 20) / len(NL), 'narration % sentences 20+')
    band('narr_30plus', 100 * sum(1 for x in NL if x >= 30) / len(NL), 'narration % sentences 30+')
    r = lambda p, t=None: 1000 * len(re.findall(p, t if t is not None else ntext)) / NW
    band('narr_em', r('--'), 'narration em dash /1K')
    band('narr_comma', r(','), 'narration commas /1K')
    band('narr_like', r(r'\blike\b'), 'narration "like" /1K')
    band('narr_ly', r(r'\b\w+ly\b'), 'narration -ly /1K')
    band('para_mean', st.mean([len(p.split()) for p in paras]), 'paragraph mean words')

    for label, pat in BANS:
        n = len(re.findall(pat, flat))
        results.append((n == 0, f'{label:44} {n:6}   must be 0'))
    nch = len(re.findall(r'\bchest\b', flat))
    results.append((nch <= a.allow_chest, f'{"chest (anatomical only)":44} {nch:6}   max {a.allow_chest}'))
    nat = len(re.findall(r'\b(?:said|asked|replied|answered)\s+\w+ly\b', flat))
    results.append((nat <= 1, f'{"adverb-on-tag":44} {nat:6}   max 1'))

    words = re.sub(r"[^a-z0-9\s']", ' ', flat.lower()).split()
    c4 = Counter(' '.join(words[i:i+4]) for i in range(len(words) - 3))
    rep4 = [k for k, v in c4.items() if v >= 3 and not any(m in k for m in MOTIFS)]
    c5 = Counter(' '.join(words[i:i+5]) for i in range(len(words) - 4))
    rep5 = [k for k, v in c5.items() if v >= 3 and not any(m in k for m in MOTIFS)]
    results.append((10000 * len(rep4) / W <= 12, f'{"repeated 4-grams /10K (motifs excl)":44} {10000*len(rep4)/W:6.1f}   max 12'))
    results.append((len(rep5) == 0, f'{"repeated 5-grams (>=3x)":44} {len(rep5):6}   must be 0'))

    if a.source:
        sflat = ' '.join(prep(a.source))
        SW = len(sflat.split())
        results.append((0.8 * SW <= W <= 1.2 * SW, f'{"length vs source +/-20%":44} {W:6}   band {int(0.8*SW)}-{int(1.2*SW)}'))
        # byte-identity on the TYPESET files, no normalisation
        draw = re.sub(r'<!--.*?-->', '', open(a.draft, encoding='utf-8').read(), flags=re.DOTALL)
        sraw = re.sub(r'<!--.*?-->', '', open(a.source, encoding='utf-8').read(), flags=re.DOTALL)
        da = re.findall(r'“[^”]*”', draw)
        sa = re.findall(r'“[^”]*”', sraw)
        ok = da == sa
        results.append((ok, f'{"frozen dialogue byte-identical, in order":44} {len(da):3}/{len(sa):<3}'))
        if not ok:
            for i, (x, y) in enumerate(zip(da, sa), 1):
                if x != y:
                    print(f'   first dialogue divergence at span {i}:')
                    print(f'     draft:  {x[:90]}')
                    print(f'     source: {y[:90]}')
                    break

    fails = 0
    print(f'STYLE BANDS — {os.path.basename(a.draft)} vs ch1-11 standard   ({W} words, narration {NW})')
    for ok, line in results:
        print(('  PASS  ' if ok else '  FAIL  ') + line)
        fails += not ok
    if rep4 and 10000 * len(rep4) / W > 12:
        print('        4-grams: ' + ' | '.join(rep4[:5]))
    print(f'\n{fails} failure(s)' if fails else '\nall bands pass ✓')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
