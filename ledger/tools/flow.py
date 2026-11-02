#!/usr/bin/env python3
"""
flow.py — reading-load instrument (2026-09-14).

Measures what a page COSTS to hold, per ~page window, from signals that are
independent of sentence shape (so it cannot simply re-detect the tics already run
to zero). Validated backward against human-labeled sites before it is trusted.

LOAD (per 300-word window, narration + dialogue as noted):
  amb     third-person pronoun with >=2 same-gender characters in the prior 200 words
          and no same-gender name in the prior 40 words  (per 100 words)
  unanch  pronoun with NO same-gender name in the prior 300 words (per 100 words)
  refdist mean words back from a pronoun to the nearest same-gender name (cap 300)
  clause  mean commas + dashes + semicolons per narration sentence
  long    share of narration sentences >= 30 words
  neg     share of narration sentences carrying a negator
  names   distinct character names in the window

PULL (proxy only; the ledgers are too sparse to drive it):
  novel   first-ever appearances of proper nouns, per 1,000 words
  dial    dialogue share of words

LOAD index = mean z-score of (amb, refdist, clause, long, neg); unanch reported, not scored, z against the
book's own windows. Diagnostic only. Never a gate. Route, then read.

Usage:  python3 ledger/tools/flow.py            # report to stdout + ledger/FLOW_REPORT.md

Names and genders come from ledger/codex/CHARACTERS.yaml (demographics.pronouns) plus
suite.pronoun_overrides. Validation sites (human-labeled heavy/light passages) come
from suite.flow_labels: [["HIGH"|"LOW", "description", "CH06", "exact text on the line"], ...].
Until labels exist the instrument is UNVALIDATED for this book: rank, then read.
"""
import glob, os, re, statistics as st, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import ROOT, CFG, prose_files, chapter_id, characters
OUT = os.path.join(ROOT, "ledger", "FLOW_REPORT.md")
WIN = 300
PRON_SHE = {"she","her","hers","herself"}
PRON_HE  = {"he","him","his","himself"}

def _gendered_names():
    she, he = set(), set()
    skip = set(CFG.get("name_skip_tokens") or [])
    for k, v in characters().items():
        pr = {str(x).lower() for x in (((v or {}).get("demographics") or {}).get("pronouns") or [])}
        target = she if pr & PRON_SHE else he if pr & PRON_HE else None
        if target is None:
            continue
        for t in re.findall(r"[A-Z][a-z]{2,}", str((v or {}).get("canonical_name") or k)):
            if t not in skip:
                target.add(t)
    for name, g in (CFG.get("pronoun_overrides") or {}).items():
        she.discard(name); he.discard(name)
        (she if g == "fem" else he).add(name)
    return she, he

SHE, HE = _gendered_names()
NEG = re.compile(r"\b(?:not|n’t|no|never|nothing|none|neither|nor|without)\b", re.I)
DQ  = re.compile(r"“[^”]*”")
STOP_CAPS = {"The","A","An","And","But","Then","She","He","It","They","Her","His","In","On","At",
             "For","To","Of","No","Not","So","If","When","What","Who","Why","How","There","This",
             "That","These","Those","Now","Here","One","Two","Three","Four","Five","Six","Seven",
             "Eight","Nine","Ten","I","You","We","Yes","Okay","Oh","Well","Just","Still","Behind",
             "Below","Above","Inside","Outside","Somewhere","Nothing","Everything","Something",
             "Nobody","Everyone","Someone","Each","Every","All","Both","Then","Later","Once",
             "Chapter","CHAPTER"}

def tokens(text):
    """word tokens with (word, is_dialogue) flags."""
    out = []
    pos = 0
    for m in DQ.finditer(text):
        for w in text[pos:m.start()].split(): out.append((w, False))
        for w in m.group(0).split(): out.append((w, True))
        pos = m.end()
    for w in text[pos:].split(): out.append((w, False))
    return out

def bare(w): return re.sub(r"^[^A-Za-z’']+|[^A-Za-z’']+$", "", w)

def sentences(narr_text):
    return [s for s in re.split(r"(?<=[.!?])\s+", narr_text) if s.strip()]

def analyze():
    files = prose_files()
    skip_ch = set(CFG.get("flow_skip_chapters") or [])
    hdr = int(CFG.get("chapter_header_lines") or 0)
    seen_names = set()
    windows = []
    for f in files:
        ch = chapter_id(f)
        if ch in skip_ch:  # e.g. a script/transcript chapter with no narration
            continue
        lines = open(f, encoding="utf-8").read().split("\n")
        body_lines = lines[hdr:] if len(lines) > hdr else lines
        # token stream with line numbers
        toks = []  # (word, is_dialogue, lineno)
        for ln, line in enumerate(body_lines, start=hdr + 1):
            for w, d in tokens(line): toks.append((w, d, ln))
        n = len(toks)
        # precompute name positions by gender (names count wherever they appear)
        namepos = []  # (idx, gender, name)
        for i, (w, d, ln) in enumerate(toks):
            b = bare(w)
            if b in SHE: namepos.append((i, "f", b))
            elif b in HE: namepos.append((i, "m", b))
        # windows
        for start in range(0, n, WIN):
            seg = toks[start:start+WIN]
            if len(seg) < 120:
                if windows and windows[-1]["ch"] == ch:
                    # fold a short tail into the previous window
                    prev = windows[-1]; prev["end_line"] = seg[-1][2]; prev["words"] += len(seg)
                continue
            words = len(seg)
            narr = " ".join(w for w, d, ln in seg if not d)
            dial = sum(1 for w, d, ln in seg if d)
            S = sentences(narr)
            L = [len(s.split()) for s in S] or [1]
            frag = sum(1 for l in L if l <= 4) / len(L)
            longr = sum(1 for l in L if l >= 30) / len(L)
            clause = st.mean(s.count(",") + s.count("—") + s.count(";") for s in S) if S else 0
            neg = sum(1 for s in S if NEG.search(s)) / len(S) if S else 0
            # pronouns in narration only
            # Pronoun load exists only when >=2 same-gender candidates are in play
            # (a pronoun with one possible referent costs the reader nothing).
            amb = unanch = 0; dists = []
            for j in range(start, start+len(seg)):
                w, d, ln = toks[j]
                if d: continue
                b = bare(w).lower()
                g = "f" if b in PRON_SHE else "m" if b in PRON_HE else None
                if not g: continue
                back = [(j - i, nm) for i, gg, nm in namepos if gg == g and 0 < j - i <= 600]
                cands = {nm for dd, nm in back}
                if len(cands) < 2: continue            # single-candidate: no load
                near = [dd for dd, nm in back if dd <= 300]
                if not near:
                    unanch += 1; continue                      # counted, not scored
                nearest = min(near)
                dists.append(nearest)
                recent_names = {nm for dd, nm in back if dd <= 200}
                if len(recent_names) >= 2 and nearest > 40:
                    amb += 1
            names = {nm for i, gg, nm in namepos if start <= i < start+len(seg)}
            # novelty: first-ever proper nouns (book order), crude
            novel = 0
            for k, (w, d, ln) in enumerate(seg):
                b = bare(w)
                if not b or not b[0].isupper() or b in STOP_CAPS or len(b) < 3: continue
                prev = bare(seg[k-1][0]) if k else ""
                if k == 0 or prev.endswith((".", "!", "?", "”")): continue  # sentence-start guard
                if b not in seen_names:
                    seen_names.add(b); novel += 1
            windows.append(dict(ch=ch, start_line=seg[0][2], end_line=seg[-1][2], words=words,
                amb=amb / words * 100, unanch=unanch / words * 100,
                refdist=st.mean(dists) if dists else 0, clause=clause, long=longr, frag=frag,
                neg=neg, names=len(names), novel=novel / words * 1000, dial=dial / words))
    return windows

def zscores(windows, key):
    v = [w[key] for w in windows]; mu = st.mean(v); sd = st.pstdev(v) or 1
    for w in windows: w["z_" + key] = (w[key] - mu) / sd

LOAD_KEYS = ["amb", "refdist", "clause", "long", "neg"]   # unanch dropped: solo scenes are not load

def label_sites(windows):
    """Human-labeled sites (strings in the current text) → the window holding them."""
    LABELS = [tuple(x) for x in (CFG.get("flow_labels") or [])]
    files = {chapter_id(f): f for f in prose_files()}
    out = []
    for side, desc, ch, needle in LABELS:
        if ch not in files:
            out.append((side, desc, ch, None, None)); continue
        lines = open(files[ch], encoding="utf-8").read().split("\n")
        ln = next((i + 1 for i, l in enumerate(lines) if needle in l), None)
        win = next((w for w in windows if w["ch"] == ch and w["start_line"] <= (ln or -1) <= w["end_line"]), None)
        out.append((side, desc, ch, ln, win))
    return out

def main():
    if not (SHE or HE):
        print("flow: ! no gendered names in ledger/codex/CHARACTERS.yaml — pronoun-load columns (amb, unanch,\n"
              "  refdist) will read zero. Clause/long/neg/novelty still measure. Declare pronouns for a full run.\n")
    W = analyze()
    for k in LOAD_KEYS + ["novel", "dial"]: zscores(W, k)
    for w in W:
        w["LOAD"] = st.mean(w["z_" + k] for k in LOAD_KEYS)
        w["PULL"] = st.mean([w["z_novel"], w["z_dial"]])
    ranked = sorted(W, key=lambda w: -w["LOAD"])
    N = len(W)
    for r, w in enumerate(ranked): w["pct"] = 100 * (1 - r / N)
    lines = []
    P = lines.append
    P(f"# FLOW REPORT — {CFG['book']} — reading-load instrument\n")
    P(f"Windows: {N} × ~{WIN} words. LOAD = mean z of amb, unanch, refdist, clause, long, neg. "
      "PULL = mean z of novelty and dialogue share (proxy). Percentile = LOAD rank, 100 = heaviest.\n")
    P("## Validation against human labels (the pass condition)\n")
    P("| side | site | ch:line | LOAD pct | amb | unanch | refdist | clause | long | neg |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    hi, lo = [], []
    labels = label_sites(W)
    if not labels:
        P("_No suite.flow_labels yet: this run is UNVALIDATED for this book. Label 5 heavy and 5 light "
          "passages a human reader found, then rerun before trusting any ranking._\n")
    for side, desc, ch, ln, w in labels:
        if not w: P(f"| {side} | {desc} | {ch}:{ln} | NOT FOUND | | | | | | |"); continue
        (hi if side == "HIGH" else lo).append(w["pct"])
        P(f"| {side} | {desc} | {ch}:{w['start_line']}-{w['end_line']} | **{w['pct']:.0f}** | {w['amb']:.2f} | {w['unanch']:.2f} | {w['refdist']:.0f} | {w['clause']:.2f} | {w['long']*100:.0f}% | {w['neg']*100:.0f}% |")
    P("")
    if hi and lo:
        P(f"HIGH-label median percentile: **{st.median(hi):.0f}** · LOW-label median percentile: **{st.median(lo):.0f}** "
          f"(pass = HIGH in top quartile, LOW in bottom; separation {st.median(hi)-st.median(lo):+.0f} points)\n")
    P("## Heaviest 15 windows (send a human here)\n")
    P("| # | ch:lines | LOAD | amb | unanch | refdist | clause | long | neg | dial | names |")
    P("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, w in enumerate(ranked[:15], 1):
        P(f"| {i} | {w['ch']}:{w['start_line']}-{w['end_line']} | {w['LOAD']:+.2f} | {w['amb']:.2f} | {w['unanch']:.2f} | {w['refdist']:.0f} | {w['clause']:.2f} | {w['long']*100:.0f}% | {w['neg']*100:.0f}% | {w['dial']*100:.0f}% | {w['names']} |")
    P("")
    P("## Lightest 10 windows\n")
    P("| # | ch:lines | LOAD | dial | frag |")
    P("|---|---|---|---|---|")
    for i, w in enumerate(ranked[-10:][::-1], 1):
        P(f"| {i} | {w['ch']}:{w['start_line']}-{w['end_line']} | {w['LOAD']:+.2f} | {w['dial']*100:.0f}% | {w['frag']*100:.0f}% |")
    P("")
    P("## Per-chapter LOAD (mean of windows) and pronoun ambiguity\n")
    P("| ch | windows | LOAD | amb/100w | unanch/100w | refdist | long% | neg% | dial% |")
    P("|---|---|---|---|---|---|---|---|---|")
    chs = []
    for ch in dict.fromkeys(w["ch"] for w in W):
        ws = [w for w in W if w["ch"] == ch]
        chs.append((ch, len(ws), st.mean(w["LOAD"] for w in ws), st.mean(w["amb"] for w in ws),
                    st.mean(w["unanch"] for w in ws), st.mean(w["refdist"] for w in ws),
                    st.mean(w["long"] for w in ws), st.mean(w["neg"] for w in ws), st.mean(w["dial"] for w in ws)))
    for ch, n, L, a, u, rd, lg, ng, dl in chs:
        P(f"| {ch} | {n} | {L:+.2f} | {a:.2f} | {u:.2f} | {rd:.0f} | {lg*100:.0f} | {ng*100:.0f} | {dl*100:.0f} |")
    P("")
    P("## What this cannot see\n")
    P("A dull premise, a flat character, a voice a reader dislikes, and any load that comes from withheld "
      "cause rather than sentence mechanics. The PULL side is a proxy; the promise/fact ledgers are too "
      "sparse to drive it. Diagnostic only. Never write to this number.\n")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))
    print(f"\n… full report: {OUT}")

if __name__ == "__main__":
    main()
