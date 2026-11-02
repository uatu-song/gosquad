# GoSquad Book 1 — Measured Baseline (computed 2026-08-29, from GoSquad_Book1_clean.epub)

Not a prompt — reference data every pass cites. Descriptive, never prescriptive.

**Method note (2026-11-02).** These figures came from a one-off script on the August text. The
suite's `style_metrics.py` splits sentences differently (a closing quote alone does not end a
sentence; a paragraph break does) and reads different rates on the same text. Before comparing
anything, recompute the table on the CURRENT text with `python3 ledger/tools/style_metrics.py`
and compare like with like. The August numbers stay here as the record of that draft.
RESONANCE comparison figures are from the same scripts run over its final text (115,603 words
incl. transcript; said-share 79%, mean sentence 10.2/median 7, fragments 32.6%, dialogue
19.1%, em 120/10k, ellipses 0, semicolons 6.1/10k, -ly 39/10k, "like" 23/10k).

## Book totals
71,562 words · 30 chapters (mean 2,385; range 552 [ch8] – 5,309 [ch14]) · 8,276 sentences ·
mean sentence 8.6 / median 6 · fragments (≤4 words) 3,035 = 36.7% · dialogue 30.7% of words ·
all past tense · close-third rotating POV · em dashes 544 (76/10k) · ellipses 200 (28/10k) ·
semicolons 12 · -ly ~101/10k · "like" 385 (54/10k) · "said" 445 of 715 tags (62%).

## THE SEAM AT CH12
ch1-11:  mean sentence 14.9 · fragments ~16% · em dashes ~2/ch
ch12-30: mean sentence  7.0 · fragments ~42% · em dashes ~28/ch
Peak fragment chapters: 18 (52.8%), 24 (52.7%), 27 (54.8%), 28 (51.6%), 29 (53.7%).
Pass 06 exists because of this table.

## Watched-word counts (whole book)
"just" 291 · "very" 269 · "looked" 196 · "something" 157 · "eyes" 102 · "felt" 96 ·
"heart" 85 · smile/smiled 83 · "breath" 66 · "hum" 59 · "the way" 36 · "in her chest" 23 ·
"suddenly" 15 · "could feel" 14 · "realized" 10 · "stomach" 10 · "grief" 2 · "seam" 1
Density flags vs RESONANCE-final: "in her chest" ~2x; "something" at RESONANCE's PRE-cut
density (it cut 328→0 in narration); "very"/"just" have no RESONANCE analogue (near-absent
there).

## Motif candidates (register before Pass 4; author confirms)
"the Go Squad" 47 · "the hyper seed" 23 · "the Tamois Heart" 19 · "in frozen time" 12

## Typography
~4,336 straight double quotes alongside curly apostrophes — mixed convention; Pass 3 runs
before everything else because of this. Spaced em dashes: 0.

## Per-chapter table
ch | words | paras | sents | mean | med | max | frag | frag% | dial% | em | ell | ; | tense | lead
1 | 2324 | 76 | 177 | 13.1 | 11 | 52 | 29 | 16.4 | 21.1 | 2 | 7 | 0 | PAST | Firas
2 | 3249 | 93 | 191 | 17.0 | 14 | 68 | 15 | 7.9 | 42.1 | 0 | 9 | 1 | PAST | Firas
3 | 2715 | 82 | 222 | 12.2 | 8 | 63 | 66 | 29.7 | 15.8 | 12 | 15 | 1 | PAST | Ruth
4 | 2184 | 63 | 148 | 14.8 | 11 | 70 | 32 | 21.6 | 19.0 | 7 | 8 | 1 | PAST | Firas
5 | 2231 | 76 | 201 | 11.1 | 9 | 59 | 54 | 26.9 | 61.8 | 2 | 22 | 1 | PAST | Ruth
6 | 1854 | 39 | 98 | 18.9 | 18 | 48 | 9 | 9.2 | 9.9 | 0 | 2 | 1 | PAST | Ahdia
7 | 1839 | 67 | 109 | 16.9 | 15 | 56 | 12 | 11.0 | 9.8 | 0 | 3 | 1 | PAST | Ruth
8 | 552 | 38 | 77 | 7.2 | 6 | 27 | 31 | 40.3 | 13.6 | 6 | 2 | 0 | PAST | Ruth
9 | 2651 | 77 | 160 | 16.6 | 12 | 77 | 27 | 16.9 | 32.8 | 0 | 8 | 4 | PAST | Ruth
10 | 1934 | 57 | 123 | 15.7 | 14 | 61 | 12 | 9.8 | 12.1 | 0 | 0 | 0 | PAST | Ruth
11 | 1972 | 48 | 119 | 16.6 | 16 | 55 | 13 | 10.9 | 4.7 | 1 | 3 | 2 | PAST | Firas
12 | 2178 | 111 | 238 | 9.2 | 7 | 38 | 77 | 32.4 | 40.6 | 21 | 21 | 0 | PAST | Firas
13 | 2586 | 159 | 331 | 7.8 | 7 | 37 | 113 | 34.1 | 48.4 | 15 | 10 | 0 | PAST | Ahdia
14 | 5309 | 268 | 632 | 8.4 | 7 | 43 | 209 | 33.1 | 26.0 | 49 | 9 | 0 | PAST | Ahdia
15 | 3908 | 189 | 424 | 9.2 | 7 | 44 | 126 | 29.7 | 54.4 | 64 | 12 | 0 | PAST | Ahdia
16 | 2551 | 111 | 253 | 10.1 | 7 | 51 | 79 | 31.2 | 10.7 | 36 | 1 | 0 | PAST | Ahdia
17 | 3454 | 218 | 453 | 7.6 | 6 | 32 | 158 | 34.9 | 39.0 | 23 | 1 | 0 | PAST | Kain
18 | 1944 | 140 | 358 | 5.4 | 4 | 27 | 189 | 52.8 | 20.6 | 18 | 2 | 0 | PAST | Ruth
19 | 2142 | 151 | 355 | 6.0 | 5 | 29 | 159 | 44.8 | 31.0 | 20 | 14 | 0 | PAST | Ruth
20 | 2833 | 168 | 379 | 7.5 | 6 | 44 | 149 | 39.3 | 56.9 | 18 | 7 | 0 | PAST | Ruth
21 | 3132 | 212 | 408 | 7.7 | 6 | 38 | 160 | 39.2 | 51.1 | 17 | 11 | 0 | PAST | Kain
22 | 1739 | 137 | 286 | 6.1 | 5 | 28 | 121 | 42.3 | 9.9 | 28 | 0 | 0 | PAST | Knight
23 | 2184 | 198 | 351 | 6.2 | 5 | 28 | 158 | 45.0 | 51.8 | 19 | 2 | 0 | PAST | Ruth
24 | 1749 | 109 | 330 | 5.3 | 4 | 24 | 174 | 52.7 | 15.6 | 22 | 0 | 0 | PAST | Ahdia
25 | 1016 | 50 | 115 | 8.8 | 7 | 34 | 37 | 32.2 | 52.2 | 13 | 10 | 0 | PAST | Ahdia
26 | 3028 | 164 | 444 | 6.8 | 5 | 41 | 209 | 47.1 | 14.8 | 41 | 4 | 0 | PAST | Kain
27 | 1053 | 76 | 186 | 5.7 | 4 | 29 | 102 | 54.8 | 2.5 | 21 | 0 | 0 | PAST | Kain
28 | 1428 | 101 | 256 | 5.6 | 4 | 33 | 132 | 51.6 | 10.2 | 23 | 0 | 0 | PAST | Kain
29 | 2226 | 152 | 419 | 5.3 | 4 | 27 | 225 | 53.7 | 3.3 | 46 | 0 | 0 | PAST | Ahdia
30 | 3597 | 196 | 433 | 8.3 | 6 | 43 | 158 | 36.5 | 53.8 | 20 | 17 | 0 | PAST | Ahdia

"lead" = most-named character (proxy for POV; verify in Pass 1's STRUCTURE_MAP).
Top character mentions: Ahdia 482 · Ruth 445 · Firas 231 · Kain 181 · Battlea 155 · Bourn 122
· Knight 110.
