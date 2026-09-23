# GO SQUAD VOL 1 — "Editorial Review Board Evaluation Report" (received 2026-09-22)

Archived at receipt. Source file: `go_squad_editorial_review_report.pdf` (Joe upload, Sept 22). 2 pp, letter. PDF metadata: Producer ReportLab, created 2026-09-22 23:51 UTC, author anonymous. No build, word count, or reviewer identity stated. No project record of the "board" that produced it (checked Sept 22).

## Report contents (verbatim headings, condensed)

- **Verdict:** "dual-engine structure combining street-level parkour vigilante realism with covert quantum sci-fi mechanics… achieves an extraordinary narrative glide." No faults or revision items.
- **Macro-arc table:** 10 arcs, Ch 1–30 + Epilogue, each with a "tempo" label (e.g. Arc 1 Ch 1–3 "110–120 BPM Staccato"; Arc 4 Ch 10–12 "Maximum Velocity (130+ BPM)").
- **Prose cadence:** staccato action stride; tonal syncopation (Ruth shouting retail code words during a hostage situation); lyrical quantum dilation.
- **Characters:** Ahdia (Operative Auerbach), Firas, the Go Squad (Ruth, Ben, Victor, Leah, Tess).
- **Vol 2 horizons:** Vessel #47 / clone facility; Firas's translocation; Bellatrix.
- Page 2 layout defect: the subtitle line overprints body text mid-paragraph.

## Build checked (Sept 22–23)

`GoSquad_Book1_chapters.zip` (Joe upload; zip SHA-256 `5f0a9e47…0863e5f`). README: "Same text as GoSquad_Book1_REVIEW.epub v1.0 (review copy, near-final), exported 2026-09-22 from commit b73d917. 30 chapters + epilogue, 77,491 words." Chicago typography; 0 straight double quotes. Presumed to be the text the report read (same date; not stated in the report).

## Report claims vs. the v1.0 text

| Report claim | v1.0 text | Status |
|---|---|---|
| Arc 1 (Ch 1–3) "110–120 BPM Staccato" | ch1 26% fragments, ch2 24%, ch3 42% — only ch3 is choppy | Partly contradicted |
| Arc 4 (Ch 10–12) "Maximum Velocity (130+ BPM)" | ch10 mean 12.6 words, ch11 14.8 (among the longest-sentence chapters) | **Contradicted** |
| BPM figures | "BPM" occurs once in the book: Ryu's heart rate on a visor display (ch15) | No basis in text |
| Ruth shouting retail code words during a hostage situation | Not found | **Not found** |
| "8-autoinjector overdose" (Ch 22–24) | ch24: eight autoinjectors lined up, doses begin; ch30: "The eighth treatment… She didn't take" it; ch29: Firas injects her | **Contradicted** (the eighth was not self-administered) |
| "Firas did not die—space folded around him… location unknown" | ch29: "everything that had ever been her brother, went down into a space smaller than a fist and was absorbed. Gone." ch30: "We just lost Firas." "translocat-" does not occur after ch28 | **Contradicted** |
| Kain on Main Street was one clone; vessels await | "Main Street" ×8 (ch23–26); epilogue tank room, "Forty-seven thought he was special too… more than a vessel." | Consistent ("Vessel #47" as a label is not in the text) |
| Bellatrix observes Scattered Seeds; Ahdia contacted her | Bellatrix only in epilogue (×2): "Agent Auerbach saw Bellatrix." "Bellatrix doesn't interfere. She observes." "Scattered Seeds" ×0 | Mostly consistent |
| "Operative Auerbach" | Text uses "Agent Auerbach" | Wording differs |
| No faults | See cadence table below: ch8, ch15, ch23 remain outside the Aug 29 harmonization targets | Not mentioned |

Correction to the Sept 22 version of this doc: "Main Street not found" was checked against the Nov 2025 txt in the project, not v1.0. It is in v1.0.

## Cadence, v1.0 (measured Sept 23; tokenizer may differ slightly from the Aug 29 method; ch15 dash rate reproduces within 1)

| Span | Mean sentence | Median | Fragments (≤4 words) | Em dashes /10k |
|---|---|---|---|---|
| Target (ch1–11 register, spec) | ~12.4 | 9 | ~27% | ~13 |
| Aug 29 baseline ch12–30 | 6.1 | 5 | 48% | 108 |
| **v1.0 ch1–11** | 11.5 | 8 | 31% | 13 |
| **v1.0 ch12–30** | 9.4 | 7 | 34% | 35 |

Outliers in v1.0: **ch15** 8.4 / 40% / **119 dashes/10k** (unchanged from the spec's 118) · **ch23** 6.8 / 45% / 43 · **ch8** 6.0 / 48% / 55 (open set-piece ruling) · ch3 10.1 / 42% / 52 · ch5 8.5 / 42%.

Word level, v1.0 vs Aug 29: "something" 157 → 129 · "very" 269 → 33 · "just" 291 → 182 · "in her chest" 23 → 6 · said-share of common tags ~62% → ~75%. Ellipses: 7 (spaced, NBSP).

## Repo verification (Sept 23, crew)

- `6_manuscript/book_1/GoSquad_Book1_REVIEW.epub` is the v1.0 text: 30 ch + epilogue, ~77.9K words incl. front matter, "Main Street" ×8, last "translocat-" in ch28. Matches the zip README.
- `6_manuscript/book_1/book1_manuscript.txt` (71.5K) and `first_edition_clean/` (71.8K) are the older Nov 2025 text. **Do not verify claims against them.** Continuity board source for Book 1 = the REVIEW.epub, extracted per chapter.
