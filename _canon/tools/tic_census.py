#!/usr/bin/env python3
"""
tic_census.py — the DISEASE MAP. Rate-based prose tics that line-regex rules
can't express, measured per chapter, with the early→late escalation ratio that
diagnosed the amplification mechanism in the first place.

    python3 _canon/tools/tic_census.py --book book_1_ed1
    python3 _canon/tools/tic_census.py --book book_2 --csv

WHY A SEPARATE TOOL. audit.py flags individual lines. But the disease
documented in PROSE_VOICE_DESIGN_PROBLEM.md is a RATE phenomenon — "still" is
a normal word at 0.7/1K and a tic at 6/1K; fragments are craft in isolation
and infection at 29.5/1K. Rates need denominators and chapter structure, which
a line matcher doesn't have. This is a fresh cut of the ideas in
_tools/quality_evaluation/ (the battery that produced the original audit),
reduced to the measures the rebuild actually watches.

MEASURES (per chapter, per 1K words)
  em-dash        — density (1.9→10.4/1K escalation was Book 1's curve)
  still/already/just — watched-word rates (PROSE_VOICE audit tables)
  short-burst    — sentences of ≤4 words: an honest PROXY for the audit's
                   "fragments" count, not the same measure. Consistent across
                   books, so the SHAPE (escalation) is comparable even though
                   absolute numbers differ from the 2026-04-03 audit.
  the-particular / not-constructions / hedges — same regexes as series RULES
  scent-opener   — first prose line contains smell/scent/odor/aroma
                   (NEGATIVE_CONSTRAINTS.md prose-openings ban — positional,
                   so it lives here, not in RULES.yaml)

ESCALATION = late rate / early rate (last 5 vs first 5 chapters). The Book 1
signature was ~9x on fragments: the human→AI prose boundary made measurable.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bookconfig as cfg
from bookconfig import norm

C = dict(red="\033[31m", yel="\033[33m", grn="\033[32m", cyan="\033[36m",
         dim="\033[2m", bold="\033[1m", off="\033[0m")


def c(s, k):
    return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else str(s)


SKIP_LINE = re.compile(r"^\s*(<!--|-{3,}\s*$|#{1,6}\s)")

WORD_TICS = {
    "still": re.compile(r"\bstill\b", re.I),
    "already": re.compile(r"\balready\b", re.I),
    "just": re.compile(r"\bjust\b", re.I),
}
PATTERN_TICS = {
    "the-particular": re.compile(r"\bthe particular\b", re.I),
    # full formulaic-negation family (mirrors series R101, ferret pass 2026-07-26)
    "not-constr": re.compile(
        r"\b[Nn]ot [^.!?;]{1,36}, (?:but|just)\b"
        r"|\b(?:was|is|are|did|does)n't [^.!?;]{1,32}\. It was\b"
        r"|\b[Nn]ot [^.!?;]{1,30}\. Not \b"
        r"|\b[Dd]idn't [^.!?;]{1,30}\. Didn't\b"
        r"|\b[Nn]o [^.!?;,]{1,20}, no [^.!?;,]{1,24}[,.]"
        r"|\b(?:was|is)n't just\b"
        r"|\bso much as\b"),
    "hedge": re.compile(r"\b[Aa] kind of\b|\b[Aa] sort of\b|\b[Ss]omething like\b|\b[Aa]lmost as if\b"),
    "in-chest": re.compile(r"\bin (?:her|his|their) chest\b", re.I),
    # counting-as-interiority (Director-ruled 2026-08-31). Author rate 0.07/1K and his
    # single hit is the idiom "too many to count"; his rate for the BEHAVIOR is zero.
    # Expected hits in Ahdia chapters ONLY — compulsive quantification is her trait.
    "counting": re.compile(
        r"\b(?:counted|counting|counts)\b(?![^.!?]{0,20}\b(?:as|for)\b)"
        r"|\bcount(?:ed)? (?:the|them|it|backward|off)\b"
        r"|\bin \w+ counted \w+\b", re.I),
    # accounting-metaphor family: the same tic wearing a different coat. Author rate ZERO
    # across all 23,536 words of his own chapters.
    "accounting": re.compile(
        r"\barithmetic\b|\bcame due\b|\ban accounting\b|\bexchange rate\b"
        r"|\bthe bill line by line\b|\bclosing its accounts\b|\bthe ledger\b", re.I),
    "kind-of": re.compile(r"\bthe kind of\b", re.I),
    "voice-was": re.compile(r"\b\w+'s voice was\b|\b[Hh](?:er|is) voice was\b|\bvoice came out\b"),
    "looked-at": re.compile(r"\b(?:looked|stared|glanced) at\b", re.I),
    # the epigram template ("Alone, then." / "Triage, then.") — one shape of
    # the closing-aphorism tic flagged by the Director on CH18 v2 (2026-07-26)
    "epigram-then": re.compile(r"\b[A-Z]\w*, then\."),
}
SCENT = re.compile(r"\b(smell|smelled|smelt|scent|odor|odour|stank|stunk|aroma)\b", re.I)


def chapter_text(path):
    lines = [l for l in open(path, encoding="utf-8", errors="replace").read().split("\n")
             if not SKIP_LINE.match(l)]
    return "\n".join(lines).strip()


def sentences(text):
    """Boundary-aware split. FIXED 2026-07-26: the old splitter used
    re.split(r"[.!?]+"), which fragments every ellipsis ("..." -> empty
    pieces) and every abbreviation into spurious 1-word "sentences". It
    inflated short-burst by ~1.7x on the author's prose and ~1.25x on the
    infected chapters. Ratios between corpora were preserved (all corpora were
    measured with the same bug), but every ABSOLUTE burst figure reported
    before this date is high. Requires a following space, so mid-ellipsis
    splits no longer occur."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def census_chapter(path):
    raw = chapter_text(path)
    ntext = norm(raw)
    words = len(ntext.split())
    row = {"words": words}
    row["em-dash"] = raw.count("—") + len(re.findall(r"(?<!-)--(?!-)", raw.replace("—", "")))
    for k, pat in WORD_TICS.items():
        row[k] = len(pat.findall(ntext))
    for k, pat in PATTERN_TICS.items():
        row[k] = len(pat.findall(ntext))
    sents = sentences(ntext)
    row["short-burst"] = sum(1 for s in sents if len(s.split()) <= 4)
    # dialogue share — CH18 v5 shipped at 21% against a guide demanding 66%
    # and no gate measured it either way (Director, 2026-07-26).
    dq = re.findall(r'"([^"]*)"', ntext)
    row["dialogue%"] = round(100 * sum(len(d.split()) for d in dq) / max(words, 1), 1)
    first = next((l for l in raw.split("\n") if l.strip()), "")
    row["scent-open"] = 1 if SCENT.search(first) else 0
    return row


MEASURES = ["em-dash", "still", "already", "just", "short-burst",
            "the-particular", "not-constr", "hedge",
            "in-chest", "kind-of", "voice-was", "looked-at", "epigram-then"]
# dialogue% is a SHARE not a rate — reported separately, never divided by words.
SHARES = ["dialogue%"]


def main():
    ap = argparse.ArgumentParser()
    cfg.add_book_arg(ap)
    ap.add_argument("--csv", action="store_true", help="machine-readable output")
    a = ap.parse_args()
    book = cfg.load(a.book)
    files = book.prose_files(strict=True)
    if not files:
        print(f"{book.key}: no prose (pre-prose by design)" if not book.prose_expected
              else f"{book.key}: NO PROSE FOUND — glob wrong")
        return 0 if not book.prose_expected else 1

    rows = [(book.short(f), census_chapter(f)) for f in files]
    total_w = sum(r["words"] for _, r in rows)

    if a.csv:
        print("chapter,words," + ",".join(MEASURES) + ",scent-open")
        for ch, r in rows:
            print(f"{ch},{r['words']}," + ",".join(str(r[m]) for m in MEASURES) + f",{r['scent-open']}")
        return 0

    print(c(f"\nTIC CENSUS — {book.key}", "bold") +
          c(f"   {len(rows)} chapters, {total_w:,} words. Rates are per 1K words.", "dim"))
    hdr = f"  {'ch':6}{'words':>7} " + "".join(f"{m:>10}" for m in MEASURES + SHARES)
    print(c(hdr, "dim"))
    for ch, r in rows:
        kw = r["words"] / 1000 or 1
        cells = ""
        for m in MEASURES:
            rate = r[m] / kw
            cells += f"{rate:>10.1f}"
        cells += f"{r['dialogue%']:>10.1f}"
        flag = c("  ← scent-open", "red") if r["scent-open"] else ""
        print(f"  {ch:6}{r['words']:>7} {cells}{flag}")

    # totals + escalation
    print(c("  " + "─" * (14 + 10 * len(MEASURES)), "dim"))
    kw_tot = total_w / 1000 or 1
    tot_cells = "".join(f"{sum(r[m] for _, r in rows) / kw_tot:>10.1f}" for m in MEASURES)
    _dw = sum(r["dialogue%"] * r["words"] for _, r in rows) / max(total_w, 1)
    tot_cells += f"{_dw:>10.1f}"
    print(c(f"  {'BOOK':6}{total_w:>7} {tot_cells}", "bold"))

    if len(rows) >= 10:
        early, late = rows[:5], rows[-5:]
        ew = sum(r["words"] for _, r in early) / 1000 or 1
        lw = sum(r["words"] for _, r in late) / 1000 or 1
        print()
        print(c("  ESCALATION  (last-5-chapter rate ÷ first-5-chapter rate — the amplification signature)", "bold"))
        line = "  "
        for m in MEASURES:
            er = sum(r[m] for _, r in early) / ew
            lr = sum(r[m] for _, r in late) / lw
            ratio = (lr / er) if er > 0.05 else float("inf") if lr > 0 else 1.0
            mark = "red" if ratio >= 3 else "yel" if ratio >= 1.8 else "grn"
            rtxt = "∞" if ratio == float("inf") else f"{ratio:.1f}x"
            line += c(f"{m}={rtxt}  ", mark)
        print(line)
    sc = [ch for ch, r in rows if r["scent-open"]]
    if sc:
        print()
        print(c(f"  SCENT-OPENERS (NEGATIVE_CONSTRAINTS ban): {', '.join(sc)}", "red"))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
