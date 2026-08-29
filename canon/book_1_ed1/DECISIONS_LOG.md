# DECISIONS LOG — Book 1 first edition (quarry)

**The don't-relitigate list.** Newest first.

---

## 2026-08-29 — Pass 6 target: per-chapter floors, dialogue frozen

**Rulings, verbatim, in the order given:**
- ch12 seam: **"The second half should align with the first"**
- how far: **the author's baseline, ~13/1K** (chosen over CH18 v5's 31.8)
- mid-session constraint: **"don't change any dialogue"**
- reconciliation: **"Per-chapter floors — each chapter targets its own"**
- scope: **"Fix the guide but don't do any revisions. We'll do revisions for another phase"**

**Why a single number could not work.** With dialogue frozen, each chapter has a
floor it cannot go below — its dialogue short-bursts are untouchable. Measured
in place (classifying real sentences, NOT by extracting quoted spans, which
manufactures boundaries: "Really?" she asked. is ONE 5-word sentence whole but
becomes a 1-word burst when extracted — that error produced an inflated 26.4/1K
aggregate floor and negative allowances in ch1-11 before it was caught):

    ch1-11  STANDARD : whole 12.9 = dialogue  5.6 + narration  7.2 /1K
    ch12-30 WORK     : whole 57.9 = dialogue 14.8 + narration 43.1 /1K

Eleven of nineteen back-half chapters have floors above 13.0.

**Operational definition — target = that chapter's dialogue floor + 7.2**, the
front half's measured narration allowance. Narration is the only workable
surface; the floor is arithmetic, not judgement.

| ch | now | floor (frozen) | target |
|---|---|---|---|
| 12 | 35.3 | 16.5 | **23.7** |
| 13 | 43.9 | 16.9 | **24.1** |
| 14 | 40.0 | 6.7 | **13.9** |
| 15 | 32.8 | 22.2 | **29.4** |
| 16 | 31.8 | 3.2 | **10.4** |
| 17 | 46.3 | 16.1 | **23.3** |
| 18 | 97.4 | 19.7 | **26.9** |
| 19 | 75.3 | 20.1 | **27.3** |
| 20 | 53.2 | 24.5 | **31.7** |
| 21 | 52.0 | 23.6 | **30.8** |
| 22 | 72.2 | 5.9 | **13.1** |
| 23 | 72.6 | 30.1 | **37.3** |
| 24 | 101.9 | 7.5 | **14.7** |
| 25 | 36.5 | 17.8 | **25.0** |
| 26 | 72.2 | 7.7 | **14.9** |
| 27 | 101.7 | 2.0 | **9.2** |
| 28 | 93.5 | 11.3 | **18.5** |
| 29 | 102.9 | 2.3 | **9.5** |
| 30 | 44.0 | 17.8 | **25.0** |

**Supersedes:** CH18 v5's "development finished" (2026-07-26). v5 sits at 97.4
whole against a 26.9 target and will need another pass. This is a deliberate
supersession under a later ruling, NOT a relitigation — do not reopen the
question, only the chapter.

**NOT started.** Ruled scope is the guide only; the prose revisions are a later
phase.

**Ruled by:** Director

---

## 2026-08-29 — Motifs registered; Book 2 Ahdia POV deferred

**Motifs, ruled:** **"All of them, no?"** — all four registered and exempt from
all Pass 4 repetition flagging: "the Go Squad" (47), "the hyper seed" (23),
"the Tamois Heart" (19), "in frozen time" (12).
*Consequence accepted:* "in frozen time" is the only true stylistic motif of the
four, so nothing downstream will ever flag it if it becomes overused.

**Book 2 Ahdia POV:** **"Defer — Book 1 first."** The oldest open question in the
repo stays open by choice. The Book 2 bridge remains blocked; that is intended,
not neglect.

**Ruled by:** Director

---

> **LEDGER MAPPING (2026-08-29).** The GOSQUAD_KIT editorial operation specifies a
> standalone `ledger/` directory. It was deliberately **not** created. GoSquad already
> has a live, pre-commit-enforced canon system, and standing up a second set of ledgers
> would create two competing sources of truth, one of which rots unread. The kit's
> ledgers map onto this directory as follows — if a kit pass tells you to open
> `ledger/X`, open the file on the right instead:
>
> | kit file | here |
> |---|---|
> | `ledger/DECISIONS_LOG.md` | `canon/book_1_ed1/DECISIONS_LOG.md` (this file) |
> | `ledger/CANON_FACTS.jsonl` | `canon/book_1_ed1/CANON_FACTS.jsonl` |
> | `ledger/PROMISES.jsonl` | `canon/book_1_ed1/PROMISES.jsonl` |
> | `ledger/CHRONOLOGY.jsonl` | `canon/book_1_ed1/CHRONOLOGY.jsonl` (new) |
> | `ledger/STRUCTURE_MAP.jsonl` | `canon/book_1_ed1/CHAPTER_INDEX.yaml` (already populated — POV determined for all 30) |
> | `ledger/STYLE_PROFILE.md` | `canon/book_1_ed1/STYLE_PROFILE.md` (new) |
> | `ledger/config.json` motifs | `canon/book_1_ed1/RULES.yaml` |
> | `tools/check_typography.py` | `_canon/tools/check_typography.py` (already exists) |
>
> The kit's `01_SETUP` epub-splitting step is already satisfied:
> `6_manuscript/book_1/first_edition_clean/` IS CH01–CH30 with paragraph breaks.

---

## 2026-08-29 — House style: Chicago, ellipses included

**Question:** The first edition mixes conventions — 4,336 straight double quotes
against 210 curly, 2,191 straight apostrophes against 159 curly, and a near-even
ellipsis split (106 `...` / 94 `…`). Every grep-based pass silently misses text
until this is normalized. Which house style, and does the book's destination
(print/retail vs working draft) drive it?

**Ruling, verbatim:** "working draft indefinitely. And for number 2, I don't
understand but the answer is probably Chicago style standards"

Asked to confirm, given that Chicago mandates curly quotes and therefore costs
~6,500 sites where the straight majority would have cost ~210, and given a
recommendation to deviate from Chicago on the ellipsis (single `…` glyph rather
than Chicago's spaced periods, to avoid dots orphaning across lines in a
reflowable EPUB), the Director ruled, verbatim:

**"just stick to it, ellipses included"**

**Scope:** Full Chicago for Book 1's first edition text —
- double quotes and apostrophes: **curly**
- em dashes: **closed** (`word—word`) — already uniform, 544 instances, 0 spaced
- ellipsis: **three spaced periods** (`. . .`), Chicago's form, NOT the `…` glyph

**Implementation note (crew, not a ruling):** the spaced ellipsis is set with
**nonbreaking spaces** between the points. This is Chicago's own specification
and it removes the line-break hazard that prompted the rejected `…`
recommendation — the concern is answered inside the ruling rather than against it.

**Deliberately out of scope:** Chicago also prefers `Firas's` over `Firas'`
(10 sites). That changes *words*, not punctuation, so it is a copyedit decision,
not typography, and it must not ride inside a 6,500-site punctuation diff where
no one could see it. Filed for a later pass; **unruled**.

**Ruled by:** Director

**Touches:** all 30 chapters of `6_manuscript/book_1/first_edition_clean/`,
`_canon/books.yaml` typography block (`enforce` flips true).

---

## 2026-08-29 — Book 1's destination: working draft indefinitely

**Question:** Is Book 1 headed for print / retail EPUB, or staying a working
draft? Raised because it determines whether the typography conversion is worth
paying now or deferring, and because it is a fact about the book's future the
canon system should carry in its own right.

**Ruling, verbatim:** "working draft indefinitely"

**Note:** this was ruled *alongside* full Chicago, which is the more expensive
option and the one the destination answer made optional. The Director chose
correctness over cost knowingly, after the tension was named. Do not "correct"
the apparent mismatch later — it is deliberate.

**Ruled by:** Director

**Touches:** the epub's `dc:description` still reads "Advanced Reader Copy — Not
for distribution"; left as-is, unruled.

---

## 2026-07-26 — "Auerbach" is Ahdia's CADENS codename, not a surname

**Question:** First edition prints both "Bacchus" (parents Faraz and Naima
Bacchus, Ch2) and "Auerbach" (CADENS address, Ch30) for Ahdia — contradiction?

**Ruling:** No contradiction. Surname = **Bacchus**. **Auerbach = her CADENS
codename**, same class as Howitzer, Greyhound, Mercury, and Overseer.

**Rationale:** Codenames are an established CADENS convention in the prose
itself — first edition contains the literal line "Codename: Overseer" and a
badge scene ("Auerbach," she said quietly, taking the badge). The series title
("Auerbach Series") is therefore named for her codename. Howitzer, Greyhound,
and Mercury do not yet appear in either first edition (0 hits) — roster known
to the Director; expect them in later books or the rebuild.

**Ruled by:** Director

**Touches:** FCT ahdia-surname-first-edition (now canonical),
canon/book_1_ed1/CANON_FACTS.jsonl, chapter_02/chapter_30 evidence.
