# DECISIONS LOG — Book 1 first edition (quarry)

**The don't-relitigate list.** Newest first.

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
