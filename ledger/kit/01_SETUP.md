# PASS 1 — SETUP (paste this whole file as the prompt)

Read `ledger/kit/GUARDRAILS.md` and `ledger/kit/COLLABORATOR_RULES.md` first and follow them all session.

The editing suite is installed (`ledger/tools/`, `ledger/codex/`, the ledgers). This pass points
it at the book and fills the codex the tools depend on.

1. **Point the suite at the chapters.** Edit `ledger/config.json` → `suite.prose_globs` (and
   `seal_globs`) to match this repo's chapter files. Run `python3 ledger/tools/suite_check.py`
   until it lists EVERY chapter with the right id and says SUITE READY. If the book exists here
   only as a compiled EPUB, split it first:
   `python3 ledger/tools/split_epub.py BOOK.epub chapters/` (dry run), then `--write`.
2. **CHARACTERS.yaml** (`ledger/codex/`): one entry per named character with `canonical_name` and
   `demographics.pronouns`, each with an `evidence` quote (chapter:line) from the prose. The prose
   wins over any planning doc. The pronoun tools and `audit.py` R016 read this.
3. **CHAPTER_INDEX.yaml**: one entry per chapter id with `pov` and `tense`, each verified by READING
   the chapter's opening. The August baseline's "lead" column is a most-named proxy, not a POV.
4. **INDEX.yaml**: a CHR- code per main character (aliases = the names the prose uses). Mechanics
   and watched words get codes as they come up in later passes; don't file pre-emptively.
5. **STRUCTURE_MAP.jsonl**: one row per chapter (pov, tense, location, words from `wordcount.py`).
6. **Motifs — ask Joe.** `ledger/config.json` has `motif_candidates_awaiting_author`: "in frozen time",
   "the hyper seed", "the Tamois Heart", "the Go Squad". He confirms or extends; move confirmed ones
   into `motifs`. Nothing is flagged as repetition before this ruling.
7. **Show Joe where the book stands against his Resonance rulings** — report only:
   `python3 ledger/tools/audit.py --candidates`. He rules which, if any, apply to this book; move
   only those into `ledger/codex/RULES.yaml` with his words and the date.
8. Run `audit.py`, `codex.py --gaps`. Seal only when Joe says the text is the one to protect:
   `python3 ledger/tools/seal.py seal`.

End with a one-paragraph report: what was filled, what awaits Joe (motifs, candidate rules,
house style at minimum).
