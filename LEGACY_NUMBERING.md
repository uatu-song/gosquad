# LEGACY NUMBERING — the translation table (ruled 2026-07-26)

**Director ruling (2026-07-26):** The series is **8 books, numbered 1–8, sequential
integers, no letter suffixes — ever.** If a book someday earns a split during
generation, it takes two numbers at that point and everything downstream
renumbers. Splits are not pre-locked; they must emerge.

`_canon/books.yaml` is the canonical registry. Directories now match it.

## The table

| Canonical | Legacy label(s) | Old directory | Now lives at |
|---|---|---|---|
| **Book 1** | Book 1 | `5_story_bibles/book_1/` | unchanged |
| **Book 2** | "Book 2A", "Book 2 (first half)" | `5_story_bibles/book_2/` | unchanged (name was already right) |
| **Book 3** | "Book 2B", "Book 2 (second half)" | `5_story_bibles/book_2b/` + case-twin `book_2B/` | `5_story_bibles/book_3/` (twins merged) |
| **Book 4** | "Book 3" (old numbering) | `5_story_bibles/book_3/` (2026 planning) **and** `5_story_bibles/book_4/` (Nov-2025 planning — same book, two dirs) | `5_story_bibles/book_4/` (2026 planning at top level; Nov-2025 material in `early_planning_2025/`) |
| **Book 5** | "Book 4" (old) — Turning Point | `5_story_bibles/book_5/` | unchanged (already new numbering) |
| **Book 6** | "Book 5" (old) — Radical Acceptance | `5_story_bibles/book_6/` | unchanged |
| **Book 7** | "Book 6" (old) — Both/And Mastery | `5_story_bibles/book_7/` | unchanged |
| **Book 8** | "Book 7" (old) — Worth Without Fixing | `5_story_bibles/book_8/` | unchanged |

Manuscript dirs (`6_manuscript/book_1/`, `6_manuscript/book_2/`) were already canonical.

## Reading legacy files

Files *inside* the renamed directories are quarry from before this ruling and
still say "Book 2B", "BOOK3_MASTER_PLAN", `book_2a:`/`book_2b:` (e.g. in
`SERIES_TOPOLOGY.yaml`), etc. **Their content was deliberately not rewritten** —
falsifying quarry is worse than translating it. Translate on ingest:

- "2A" → Book 2 · "2B" → Book 3 · old "Book 3" → Book 4 · old "Book N" (N≥4) → Book N+1
- A file's *directory* tells you its canonical book; its *text* tells you its era.

Each affected directory carries a `_NUMBERING_NOTE.md` saying the same thing.
