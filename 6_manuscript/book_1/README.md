# Book 1 — Go Squad

## THE CURRENT BOOK IS `GoSquad_Book1_v1.2.epub`

| File | What it is |
|---|---|
| **`GoSquad_Book1_v1.2.epub`** | **The book.** Review copy v1.2, copyedited near-final, built 2026-10-11. |
| `GoSquad_Book1_v1.2.pdf` | The same text as a PDF. |
| `GoSquad_Book1_v1.2.md` | The same text as one Markdown file. |
| `v1_2/` | The same text as plain chapter files. Read-only; never edit here. |

There is exactly one epub at this level. If you find a second one, something is wrong.
Everything superseded lives in `_archive/` (see its README). Nothing in `_archive/` ships.

## What v1.2 contains

- v1.0 — whole-book copyedit (the review copy).
- v1.1 — cadence rulings on ch3/ch5/ch8; 25 narration "just" cuts.
- v1.2 — ch21 dialogue typo, ch25 attribution, five Chicago quote-punctuation sites.

## Where the text actually lives (edit here, not in the epub)

The book is assembled from two source folders. The folder names are historical:

- Chapters 1–11: `first_edition_clean/chapter_01.txt` … `chapter_11.txt`
- Chapters 12–30: `rewrite_pilot/chapter_NN_metric_v1.txt`
  - **Chapter 18 is `chapter_18_metric_v3.txt`.** Every other ch18 draft is archived.
  - Chapter 14 is `chapter_14a_metric_v1.txt` + `chapter_14b_metric_v1.txt`.

`first_edition_clean/` chapters 12–30 are the OLD first-edition text. They stay because
the style tools use them as the author's measurement baseline. They are not in the book.

The authoritative list is the `CHAPTERS` list in `build_review_epub.py`.

## Making a new version

1. Edit the source files above.
2. Change `REVIEW_VERSION` (e.g. `1.2` → `1.3`).
3. `python3 build_review_epub.py`, then `python3 build_review_pdf.py` and `python3 build_review_md.py`.
   Each builder writes `GoSquad_Book1_v<VERSION>.*` and moves any older version into
   `_archive/epubs/` automatically.
4. Re-extract the plain text into a new `v1_3/` folder and move `v1_2/` into `_archive/`.
5. Rebuild `/workspace/exports/` from the new epub.

## Also here (planning, not versions of the book)

- `BOOK1_REBUILD_STUDS.md` — the eight canonical studs the rebuild was built from.
- `book1_chess_game.pgn` — the chess scaffold.
