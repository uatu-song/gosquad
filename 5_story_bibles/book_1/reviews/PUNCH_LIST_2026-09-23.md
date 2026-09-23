# Book 1 Punch List — from the Sept 22 report receipt

Source: `2026-09-22_editorial_review_report_receipt.md`. Each item: what, evidence, owner, Director ruling needed?

## A. Prose — RULED 2026-09-23, see canon/book_1_ed1/DECISIONS_LOG.md

| # | Item | Evidence | Ruling |
|---|---|---|---|
| A1 | ch15 em-dash rate 119/10k, 9x the ch1–11 target of ~13 | Unchanged since Aug 29 spec (118) | Harmonize, or rule it a deliberate register for the CADENS chapters |
| A2 | ch8 mean sentence 6.0, fragments 48%, dashes 55 | Flagged Aug 29 as "open set-piece ruling"; still open | Rule: set-piece exemption yes/no |
| A3 | ch23 mean 6.8, fragments 45%, dashes 43 | Outside ch12–30 harmonized band (9.4 / 34% / 35) | Harmonize, or exempt as combat chapter |
| A4 | ch3 fragments 42%, dashes 52; ch5 fragments 42% | Inside the "ch1–11 register" span but outside its own target | Lighter pass or exempt |
| A5 | "just" still 182 occurrences | Down from 291; "very" went 269→33 so the pass works | Set a target count or leave |

## B. Canon / naming (ledger seeds, no prose change)

| # | Item | Evidence | Action |
|---|---|---|---|
| B1 | Firas is absorbed and gone at ch29–30, not translocated | ch29 "Gone." ch30 "We just lost Firas." | Knowledge Registrar seed: team believes Firas dead. Any later "translocated" framing is a Book 2+ reveal, not Book 1 fact. Check 2A/2B planning docs for the word "translocation" applied to Firas and tag them as post-Book-1 |
| B2 | Eighth autoinjector was not self-administered | ch24 lined up; ch29 Firas injects her; ch30 "She didn't take" it | Numbers Clerk seed: doses taken = 7 self + 1 by Firas. Body/Ground seed for who held the injector |
| B3 | Vessel "Forty-seven" is a Kain clone tank number | Epilogue only | Codex note: unrelated to the retired 43/47 Ahdia iteration count. Numbers Clerk must not merge them |
| B4 | "Agent Auerbach", not "Operative Auerbach" | Text usage | Codex alias list: reject "Operative" |
| B5 | "Scattered Seeds" appears 0 times in Book 1 | Text search | If the term is canon for later books, record first-use book/chapter when it lands |
| B6 | Bellatrix in Book 1 = observer, 2 mentions, epilogue only | Text search | Knowledge Registrar reader-belief entry: reader knows only "observes, doesn't interfere" |

## C. Repo hygiene

| # | Item | Action |
|---|---|---|
| C1 | `book1_manuscript.txt` is the damaged PDF extraction (bit both of us). **first_edition_clean/ is NOT stale — it is the ch1–11 source for the epub.** | DONE 09-23: PDF extraction moved to `_archive/book1_pdf_extraction/`. first_edition_clean/ untouched. |
| C2 | No per-chapter v1.0 text in the repo; only the epub | DONE 09-23: `6_manuscript/book_1/v1_0/` (30 ch + epilogue) |
| C3 | ~~`REVIEW_VERSION` is a 4-byte file~~ | Not a defect: it is the version stamp ("1.0") the builder reads. Struck. |
| C4 | The report PDF is not in the repo | Save to `5_story_bibles/book_1/reviews/` next to the receipt |
| C5 | Uncommitted: receipt note, punch list, `REVIEW_BOARD.md` | Commit and push |

## D. Board setup (blocks Run 1)

| # | Item |
|---|---|
| D1 | ~~Director approves Section 4~~ DONE 09-23 |
| D2 | DONE 09-23 (Section 4.7). Was: add Book 1 rows to Section 4: Firas status, autoinjector count, Kain clone tanks, 18-month clock, Tamois Heart, CR-7 synthesis, 47x impact amplification |
| D3 | Build `board.py` (Batch API + caching), source = C2 extraction |
| D4 | Dry run on Book 1 ch1 and Book 2A ch1; Director judges signal |

## Not ours
- Page 2 subtitle overprint in the PDF: producer defect, ignore.
- The report's BPM labels and the retail-code-words scene: no text basis, no action beyond noting it in the receipt.
