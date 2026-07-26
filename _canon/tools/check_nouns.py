#!/usr/bin/env python3
"""
check_nouns.py — PROPER-NOUN DRIFT GATE for generated drafts.

    python3 _canon/tools/check_nouns.py <draft-file> [--book book_1_ed1]

WHY (2026-07-26). The CH18 cold-rewrite pilot passed every register gate while
inventing "Delancey" (street), "Central City" (city — canon is Caledonia), and
"Central City General" (hospital). Style gates can't catch a plausible proper
noun; only corpus comparison can. Per CON-B1-NO-INVENTED-PROPER-NOUNS, a
generating agent may not coin proper nouns — so any capitalized name in a
draft that appears nowhere in the reference corpus (the book's prose) or the
canon layer is either a canon error or new lore needing a Director ruling.

VERIFICATION IS SUBSTRING, NOT TOKEN: a candidate passes if its lowercase form
occurs anywhere in the lowercased corpus+canon text. This keeps recombinations
("Ruth Carter") and all-caps renditions of known lines, while catching genuinely
new names regardless of casing. Candidates are filtered hard first — a word
whose lowercase form is ordinary corpus vocabulary ("listen", "gear", "mine")
is never a candidate, so dialogue-initial capitals don't spam the report.
A noisy gate is an ignored gate.

Exit 1 on any unresolved noun (gate mode for the rewrite pipeline; NOT wired
into the pre-commit wall — committed quarry legitimately contains old drift).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bookconfig as cfg
from bookconfig import norm

C = dict(red="\033[31m", grn="\033[32m", dim="\033[2m", bold="\033[1m", off="\033[0m")


def c(s, k):
    return f"{C[k]}{s}{C['off']}" if sys.stdout.isatty() else str(s)


SKIP = re.compile(r"^\s*(<!--|-{3,}\s*$|#{1,6}\s)")
GENERIC = set("""monday tuesday wednesday thursday friday saturday sunday january february march
april may june july august september october november december first second third fourth fifth
sixth seventh eighth ninth tenth eleventh twelfth thirteenth twentieth god jesus christmas okay ok
mr mrs ms dr sr jr st tv gps ir emp swat er icu cpr mri ai dm dms twitter youtube tiktok instagram
facebook google batman daredevil kevlar lycra espn""".split())


def text_of(path):
    return norm("\n".join(l for l in open(path, encoding="utf-8", errors="replace").read().split("\n")
                          if not SKIP.match(l)))


def candidates(text, common_vocab):
    """Title-Case / ALL-CAPS runs worth checking. A single word is a candidate
    only if its lowercase form is NOT ordinary vocabulary anywhere."""
    out = set()
    for m in re.finditer(r"\b[A-Z][a-zA-Z']*(?:\s+(?:of\s+|the\s+)?[A-Z][a-zA-Z']*)*\b", text):
        run = m.group(0).strip()
        words = [w for w in run.split() if w.lower() not in ("of", "the")]
        if not words:
            continue
        if len(words) == 1:
            w = words[0]
            lw = w.lower()
            if len(w) < 3 or lw in GENERIC or lw in common_vocab:
                continue
            out.add(w)
        else:
            # multiword run: candidate unless every word is generic
            if all(w.lower() in GENERIC or w.lower() in common_vocab for w in words):
                # still a candidate if it's a Title Case NAME-shaped pair like
                # "Central City" — common words composing a place name. Keep
                # pairs/triples where each word is capitalized mid-run.
                if len(words) <= 3 and not run.isupper():
                    out.add(run)
                continue
            out.add(run)
    return out


def common_vocab_of(text):
    """Every token that appears in lowercase — i.e., ordinary vocabulary."""
    return set(w for w in re.findall(r"\b[a-z][a-z']+\b", text))


def main():
    ap = argparse.ArgumentParser()
    cfg.add_book_arg(ap)
    ap.add_argument("draft", help="generated draft file to check")
    a = ap.parse_args()
    book = cfg.load(a.book)

    corpus = "\n".join(text_of(f) for f in book.prose_files(strict=False))
    canon_txt = ""
    for f in book.canon_files() + [str(book.constraints_f), str(book.index_f)]:
        if os.path.exists(f):
            canon_txt += "\n" + norm(open(f, encoding="utf-8", errors="replace").read())
    if not corpus.strip() and not canon_txt.strip():
        print(c("✗ reference corpus is EMPTY — wrong --book? Refusing to pass a draft against nothing.", "red"))
        return 1
    ref_lower = (corpus + canon_txt).lower()

    draft_text = text_of(a.draft)
    vocab = common_vocab_of(corpus) | common_vocab_of(draft_text)
    lines = draft_text.split("\n")

    def known_word(w):
        """Ordinary vocabulary, not a name: lowercase form seen in corpus/draft
        (contractions checked against their base: Equipment's -> equipment)."""
        lw = w.lower()
        base = re.sub(r"'(s|d|m|re|ll|ve|t)$", "", lw)
        return (lw in vocab or base in vocab or lw in GENERIC
                or base + "s" in vocab or base.rstrip("s") in vocab)

    midset = set(re.findall(r"(?<=[a-z,;] )[A-Z][a-zA-Z']+", draft_text))
    unknown = {}
    for cand in sorted(candidates(draft_text, vocab)):
        if cand.lower() in ref_lower:
            continue
        # strip leading/trailing ordinary words (imperatives, contractions,
        # possessives of known names) and re-test the remaining core
        words = cand.split()
        while words and (known_word(words[0]) or re.sub(r"'s$", "", words[0]).lower() in ref_lower):
            words.pop(0)
        while words and known_word(words[-1]):
            words.pop()
        if not words:
            continue
        core = " ".join(words)
        if core.lower() in ref_lower:
            continue
        if len(words) == 1 and known_word(words[0]):
            continue
        # A single word seen ONLY at sentence/dialogue starts is capitalized
        # grammar, not a name ("Anterior dislocation...", "Somebody left...").
        # A real name shows up mid-sentence somewhere ("carjacking on Delancey").
        if len(words) == 1 and words[0] not in midset:
            continue
        for i, ln in enumerate(lines, 1):
            if core in ln or cand in ln:
                unknown.setdefault(core, (i, ln.strip()[:80]))
                break

    print(c(f"PROPER-NOUN DRIFT — {os.path.basename(a.draft)} vs {book.key} corpus+canon", "bold"))
    if not unknown:
        print(c("  no invented proper nouns — every name resolves ✓", "grn"))
        return 0
    print(c(f"\n  ✗ {len(unknown)} NAME(S) NOT IN CORPUS OR CANON", "red") +
          c("   (CON-B1-NO-INVENTED-PROPER-NOUNS: canon error, or new lore needing a ruling)", "dim"))
    for pn, (i, ln) in unknown.items():
        print(f"    {c(pn.ljust(28), 'red')} line {i}: {ln}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
