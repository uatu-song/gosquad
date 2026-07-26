# CODEX CHANGELOG — Book 1

Every change to `RULES.yaml` or a code's declaration in `INDEX.yaml`, newest
first, with the `codex_version` it produced. Bump the version on every rule
change; `audit.py` is re-run after each entry.

This file and `RULES.yaml` are excluded from the fossil scan — they *describe*
fossils, so a fossil quoted here is documentation, not a defect.

---

## v1 — 2026-07-26 — canon layer created (empty, pre-prose)

**Change:** Stood up `canon/book_1/` — INDEX, RULES, CHAPTER_INDEX, CANON_FACTS,
PROMISES, DECISIONS_LOG, this file. All registries deliberately empty.

**Why:** Book 1 is mid-rebuild at step 8 (cinematic blocking); prose generation
is step 9 and has not started. `books.yaml` therefore sets
`prose_expected: false` for this book, so 0 chapters is the CORRECT state and
the tools say so explicitly rather than reporting a vacuous "clean."

This is the FORWARD case, and it is the better one: codes get filed as chapters
are written, each carrying its prose site from birth. The kit this system
descends from is explicit that retroactive ingest is "harder and more error-
prone than tagging as you write" — Book 1 gets to skip that risk entirely.

**Not canon:** `6_manuscript/book_1/book1_manuscript.txt` is a PDF text-
extraction of the PRE-REBUILD draft — 318 embedded running headers
("Vaughn / Go Squad / N"), 418 broken words ("wasn' t", "reemer ge"), no chapter
delimiters, whole pages collapsed to single lines. It is not a manuscript source
and must not be ingested. The rebuild replaces it.

**Audit after:** `AUDIT CLEAN (book_1) — 0 rules run over 0 chapters, 5 codex files.`
