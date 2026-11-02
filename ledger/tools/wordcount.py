#!/usr/bin/env python3
"""
wordcount.py — one consistent word count, per chapter and total, every time.

Word counts are tool-dependent. Resonance lost a session to a count that silently
dropped the epilogue (a CH* glob) and another to spaced ellipses counted as words.
So this counts the files in suite.prose_globs (print the file list: a glob that
misses a chapter is the classic failure) and never counts punctuation-only tokens
(". . ." is not three words; an em dash is not a word).

A contest or vendor may count differently (Word/Google count the DOCX, headings
included). Record which number you report, and to whom, in the ledger.

Usage: wordcount.py [--files]
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _suite import CFG, prose_files, chapter_id, rel

PUNCT_ONLY = re.compile(r"^[.…—–,;:!?\"'“”‘’*_-]+$")

def count_words(s):
    return sum(1 for t in s.split() if not PUNCT_ONLY.match(t))

def main():
    fs = prose_files()
    if not fs:
        print("wordcount: no prose files matched suite.prose_globs"); return 1
    total = 0
    print(f"WORDCOUNT — {CFG['book']} — {len(fs)} files")
    for f in fs:
        n = count_words(open(f, encoding="utf-8").read())
        total += n
        print(f"  {chapter_id(f):8} {n:7,}" + (f"   {rel(f)}" if "--files" in sys.argv else ""))
    print(f"  {'TOTAL':8} {total:7,}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
