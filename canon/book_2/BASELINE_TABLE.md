# BOOK 2 — BASELINE TABLE (month by month, under the proportional model)

**Status:** crew reference, built 2026-09-07 on the Director's punch #20 ruling ("Proportional, as Book 1 has it"). **Every parameter below is crew's and veto-open.** Nothing here is canon until the Director says so; the synopsis and the 2A topology are NOT updated by this file (the Director holds the synopsis rewrite — log entry 2026-09-07, "crew applies nothing").
**Companion:** `canon/book_2/baseline_table.csv` — the same rows, machine-readable (month, event, spend_type, duration, fraction_converted, doses, start_pct, end_pct, threshold_notes).
**Sources read:** `canon/book_2/DECISIONS_LOG.md` (#12, #16, #20); `canon/series/TEMPORAL_MECHANICS.md` (§5, §5b, §7, §7e); `canon/characters/Ahdia_Bacchus.md` §1–2; the shipped Book 1 drafts ch14b, 15, 16, 19, 20, 24, 30 (`6_manuscript/book_1/rewrite_pilot/`); `5_story_bibles/book_4/Series_synopsis.md` (Book 2 section, read-only); `5_story_bibles/book_2/BOOK2A_TOPOLOGY.yaml`.

---

## 1. The model, the parameters, the ambiguity

### The ruled model (Director, punch #20 — binding)
- Each use converts a **fraction of what REMAINS**, permanently. The number decays geometrically and never reaches zero.
- **Treatment adds back a FIXED absolute amount per dose** — the only way the number rises — on §7e's schedule (three weeks to start, monthly once stabilised).
- Thresholds absolute: **<50 concerning · <30 dangerous · <10 critical · <1 transcendence risk.**
- Translocation is FAERIS and costs **no** baseline (#16). Only freezes, dilation and field use burn.
- The Seed was never dormant; 2A opens from Book 1's one-third cellular recovery plus ~three months of treatment; nobody starts at 100 (#12).

### The scale
The percentage is FAERIS's ledger (§5b): **100 = the convertible substrate she had at the bonding** — the half of her the Seed left human ("replaced approximately half your life force," ch14b). Everything on Book 1's page is stated on this scale ("23% of total reserves" = 23% of what remained), so this table is too.

### The three crew parameters (veto-open)

| # | Parameter | Value chosen | Fit to |
|---|---|---|---|
| (a) | **Rate per field-minute.** Exposure E = minutes × (radius ÷ 6 m) × intensity × simultaneous fields. Fraction converted f = 1 − e^(−k·E). | **k = 0.0726 % of what remains per working field-minute at 6 m** (one hour ≈ 4.3 %) | ch14b: six hours, 47 amplifications, 23 % of what remained — the reference night. Radius 6 m is the page's default field (14a "~6.1 m"; ch19 "Six meters of field"). Intensity: *work* (moving people, amplifications at working scale) = 1, the reference; a plain *hold* = 0.5. The ch15 "cut in half" is the radius term (6 m → ~3 m). |
| (a′) | **Tier 2 — opposing temporal force.** A field held against another temporal/quantum source (Main Street against the Heart; the reactor's 28 quantum nodes) pays at a different order. | **≈ 31 % of what remains per minute** (M ≈ 516 × the Tier-1 rate) | Fit so the locked 10 m 47 s lands at 0.7 from where Month 11 ends (Path A). Sanity: Main Street (33 → "empty," ch28–30) then takes ~7.5 Tier-2 minutes — plausible for a fight run in bursts. Under Path B the fit is 25 %/min (Main Street ~9.5 min). |
| (b) | **Dose add-back D** | **+8 points per properly spaced dose** | ch24 arithmetic: docks level (single digits — "Weeks. Maybe less") + dose 1 + seven rushed doses at ~30 % yield ("fifty percent max"; "thirty percent total regeneration") = "one-third" (ch30). Docks at 8 % → D = 8.2; at 3 % → 9.8; at 12 % → 6.9. D = 8 is the middle. |
| (c) | **"One-third cellular recovery" = a LEVEL: 33.3 on the FAERIS scale** — see the ambiguity below. | Month 0 = **33.3** | The Director's ruling text uses it as the level 2A opens from. |

### THE AMBIGUITY (flagged, not resolved)
"Approximately one-third cellular recovery" (ch30, Bourn to Ryu) has three readings, and a fourth problem underneath them:
1. **A level — 33 % of the scale.** *Used here.* Matches the Director's "opens from Book 1's one-third cellular recovery."
2. **A third of the LOSS recovered** — docks level L + (100 − L)/3. With L in single digits this is 35–39. Numerically almost the same as (1).
3. **A third of the designed recovery** — the rushed seven doses yielded ~30 % of what a full course would have ("thirty percent total regeneration," ch24). With D = 8 and nine doses designed, that is again ≈ 33 on the scale. **All three readings converge on 33 ± 5, provided the docks left her in single digits — which "Weeks. Maybe less" and telomere 18 % CRITICAL support.**
4. **The real problem: the page measures the one-third BEFORE Main Street.** Ch30: "she LEFT at approximately one-third cellular recovery" — left the facility for the fight. Then Main Street drains her ("How close did you come to draining all of your life force yesterday?"; ch28 "empty"), and Firas's eighth dose goes in (ch29). Page-strict, Month 0 ≈ 2 + 8 = **~10**, not 33, and January would open at ~34 instead of 57; the riot alone would put her under 30 (dangerous) at the first use, and Exile Island at any real cadence would kill her by Month 4. **This table follows the ruling's text (Month 0 = 33.3) and asks the Director to confirm that Main Street's drain is absorbed into "one-third" — or to rule the page-strict number and accept a book that runs ~20 points lower throughout.**

### What the ledger does NOT carry (§5b: the frontier is a different face)
Nosebleeds, tremor, "nearly dies" (riot), "3–7 days to live" (ch17), "dead in 11 days without treatment" (topology ch4), "Weeks. Maybe less" (ch19) are **frontier prognoses** — shear damage at the conversion boundary — not ledger levels. The ledger has no passive decay under the ruled model; use spends it, doses raise it, nothing else moves it. Multi-field nights and panic-triggered wide fields push the frontier hardest whatever the ledger says.

---

## 2. The table — Month 0 to Month 12 (Path A: the ruling read literally)

**Cadence assumptions (all crew, all veto-open):**
- **Interregnum (Oct–Dec):** three monthly doses, no priced spend (nothing named; the first vanishing seed is ch4).
- **Exile Island:** 28 extractions, all before Ruth's discovery (topology ch19: "28 subjects, 47 episodes"), each **13 min at ~20 m** (a compound, not a room: freeze around the target, FAERIS extracts) = 3.1 % of what remains; distributed by the seven news seeds and ch17's "7 translocations in 5 days" / ch19's "3 today"; the ch15b junta (8 generals) as ONE 30-min, 40-m freeze. Kain's Month-4 exile priced as a standard extraction (may be Tier 2 — unruled).
- **Big ops:** Jakarta 60 min at 30 m; Eastern Europe 45 min at 30 m; Months 3–5 one Jakarta-class op each (50 min at 30 m) — the "global vigilantism escalates" line. Each big op is followed by an emergency dose (the ch8 pattern: intervention → emergency treatment → falsified record).
- **Doses:** scheduled monthly (§7e stabilised cadence) + the emergency doses the topology names. After ch18's ultimatum: monthly maintenance only, no emergency top-offs.
- **Months 7–10 (2B):** the synopsis names NO Ahdia ops; the topology says "continued ops between Ch19–22." Priced as one Jakarta-class + one mid-size (40 min at 20 m) op per month. Manhunt (Month 11): the ch23 escape freeze plus a cumulative chase-week allowance.
- **Endgame:** the 800-mile move is FAERIS (free); the 10 m 47 s freeze is Tier 2, fit to land 0.7.

| Mo | Event | Type | Duration | Start % | Spend / dose | End % | Threshold |
|---|---|---|---|---|---|---|---|
| 0 | END OF BOOK 1 — 'approximately one-third cellular recovery' (ch30), read as a LEVEL on FAERIS's scale | anchor |  | 33.3 | — | 33.3 | <50 CONCERNING |
| 0 | Interregnum Oct-Dec: 3 scheduled monthly doses (Director: 'plus ~three months of treatment'); no priced spend | dose | 3 doses | 33.3 | +24 (3 dose) | 57.3 | recrosses >=50 |
| 1 | Isaiah riot freeze — 47 min, plaza-scale (~30 m), work (saves 23), panic-triggered (no shrink) | freeze | 47 min @30 m | 57.3 | -15.7% | 48.3 | crosses <50 CONCERNING |
| 1 | Stampede freeze at the debate hall — 3 min (~20 m) | freeze | 3 min @20 m | 48.3 | -0.7% | 48.0 | <50 CONCERNING |
| 1 | Exile Island extraction #1 — NK general at a parade (ch4 seed) | extraction | 13 min @20 m | 48.0 | -3.1% | 46.5 | <50 CONCERNING |
| 1 | Scheduled monthly dose (ch4 treatment scene) | dose | 1 dose | 46.5 | +8 (1 dose) | 54.5 | recrosses >=50 |
| 1 | Jakarta operation (11,000 saved) — 60 min plaza-scale (~30 m) working field | op | 60 min @30 m | 54.5 | -19.6% | 43.8 | crosses <50 CONCERNING |
| 1 | Eidolon mob — FAERIS extracts her; costs nothing (#16) | faeris |  | 43.8 | — | 43.8 | <50 CONCERNING |
| 2 | Emergency dose after Jakarta (ch5) | dose | 1 dose | 43.8 | +8 (1 dose) | 51.8 | recrosses >=50 |
| 2 | Exile Island extraction #2 — Belarus (ch6); 'third straight week of vacuums' (ch8) | extraction | 13 min @20 m | 51.8 | -3.1% | 50.2 |  |
| 2 | Exile Island extraction #3 — Belarus (ch6); 'third straight week of vacuums' (ch8) | extraction | 13 min @20 m | 50.2 | -3.1% | 48.7 | crosses <50 CONCERNING |
| 2 | Exile Island extraction #4 — Belarus (ch6); 'third straight week of vacuums' (ch8) | extraction | 13 min @20 m | 48.7 | -3.1% | 47.1 | <50 CONCERNING |
| 2 | Ruth's top-off (ch7) = the scheduled monthly dose | dose | 1 dose | 47.1 | +8 (1 dose) | 55.1 | recrosses >=50 |
| 2 | Eastern Europe arms-shipment op (~8,000 saved) — 45 min plaza-scale field | op | 45 min @30 m | 55.1 | -15.1% | 46.8 | crosses <50 CONCERNING |
| 2 | Emergency dose after Eastern Europe (ch8; first falsified record) | dose | 1 dose | 46.8 | +8 (1 dose) | 54.8 | recrosses >=50 |
| 3 | Month 3 grinding: one Jakarta-class intervention (Ryu intel pipeline) — 50 min @30 m | op | 50 min @30 m | 54.8 | -16.6% | 45.7 | crosses <50 CONCERNING |
| 3 | Emergency dose after the intervention (the ch8 pattern) | dose | 1 dose | 45.7 | +8 (1 dose) | 53.7 | recrosses >=50 |
| 3 | Exile Island extraction #5 | extraction | 13 min @20 m | 53.7 | -3.1% | 52.1 |  |
| 3 | Exile Island extraction #6 | extraction | 13 min @20 m | 52.1 | -3.1% | 50.5 |  |
| 3 | Scheduled monthly dose | dose | 1 dose | 50.5 | +8 (1 dose) | 58.5 |  |
| 4 | Month 4 grinding: one Jakarta-class intervention (Ryu intel pipeline) — 50 min @30 m | op | 50 min @30 m | 58.5 | -16.6% | 48.8 | crosses <50 CONCERNING |
| 4 | Emergency dose after the intervention (the ch8 pattern) | dose | 1 dose | 48.8 | +8 (1 dose) | 56.8 | recrosses >=50 |
| 4 | Exile Island extraction #7 (ch10/ch12 seeds) | extraction | 13 min @20 m | 56.8 | -3.1% | 55.0 |  |
| 4 | Exile Island extraction #8 (ch10/ch12 seeds) | extraction | 13 min @20 m | 55.0 | -3.1% | 53.3 |  |
| 4 | Exile Island extraction #9 (ch10/ch12 seeds) | extraction | 13 min @20 m | 53.3 | -3.1% | 51.6 |  |
| 4 | Kain extraction (ch20: exiled Month 4; avatar melts, respawns) — priced as a standard extraction; MAY be Tier 2 | extraction | 13 min @20 m | 51.6 | -3.1% | 50.0 |  |
| 4 | Scheduled monthly dose | dose | 1 dose | 50.0 | +8 (1 dose) | 58.0 |  |
| 5 | Month 5 grinding: one Jakarta-class intervention (Ryu intel pipeline) — 50 min @30 m | op | 50 min @30 m | 58.0 | -16.6% | 48.4 | crosses <50 CONCERNING |
| 5 | Emergency dose after the intervention (the ch8 pattern) | dose | 1 dose | 48.4 | +8 (1 dose) | 56.4 | recrosses >=50 |
| 5 | Exile Island extraction #10 | extraction | 13 min @20 m | 56.4 | -3.1% | 54.7 |  |
| 5 | Exile Island extraction #11 | extraction | 13 min @20 m | 54.7 | -3.1% | 53.0 |  |
| 5 | Scheduled monthly dose | dose | 1 dose | 53.0 | +8 (1 dose) | 61.0 |  |
| 6 | Scheduled monthly dose (early June) | dose | 1 dose | 61.0 | +8 (1 dose) | 69.0 |  |
| 6 | Exile Island extraction #12 — SE Asia regime (ch14 seed) | extraction | 13 min @20 m | 69.0 | -3.1% | 66.8 |  |
| 6 | CHECK — topology ch17: 'was 68% last week' | anchor |  | 66.8 | — | 66.8 |  |
| 6 | Junta op — 8 generals in ONE freeze (ch15b seed) — 30 min @40 m (extractions #13-20) | extraction | 30 min @40 m | 66.8 | -13.5% | 57.8 |  |
| 6 | Exile Island extraction #21 — '7 translocations in 5 days' (ch17) | extraction | 13 min @20 m | 57.8 | -3.1% | 56.0 |  |
| 6 | Exile Island extraction #22 — '7 translocations in 5 days' (ch17) | extraction | 13 min @20 m | 56.0 | -3.1% | 54.3 |  |
| 6 | Exile Island extraction #23 — '7 translocations in 5 days' (ch17) | extraction | 13 min @20 m | 54.3 | -3.1% | 52.6 |  |
| 6 | Exile Island extraction #24 — '7 translocations in 5 days' (ch17) | extraction | 13 min @20 m | 52.6 | -3.1% | 51.0 |  |
| 6 | Exile Island extraction #25 — '7 translocations in 5 days' (ch17) | extraction | 13 min @20 m | 51.0 | -3.1% | 49.4 | crosses <50 CONCERNING |
| 6 | CHECK — topology ch17 eavesdrop: '54%' | anchor |  | 49.4 | — | 49.4 | <50 CONCERNING |
| 6 | Treatment given at the ch17 scene (emergency) | dose | 1 dose | 49.4 | +8 (1 dose) | 57.4 | recrosses >=50 |
| 7 | Exile Island extraction #26 — '3 translocations today' (ch19, the Friday) | extraction | 13 min @20 m | 57.4 | -3.1% | 55.6 |  |
| 7 | Exile Island extraction #27 — '3 translocations today' (ch19, the Friday) | extraction | 13 min @20 m | 55.6 | -3.1% | 53.9 |  |
| 7 | Exile Island extraction #28 — '3 translocations today' (ch19, the Friday) | extraction | 13 min @20 m | 53.9 | -3.1% | 52.2 |  |
| 7 | ANCHOR — ch19 discovery (Ruth + Ryu): topology says 53.1% | anchor |  | 52.2 | — | 52.2 |  |
| 7 | Scheduled monthly maintenance dose (Jul) — no emergency top-offs after ch18's limit [ASSUMED] | dose | 1 dose | 52.2 | +8 (1 dose) | 60.2 |  |
| 7 | Continued global intervention (Jul), Jakarta-class — 50 min @30 m [ASSUMED cadence; topology: 'continued ops between Ch19-22'] | op | 50 min @30 m | 60.2 | -16.6% | 50.2 |  |
| 7 | Continued global intervention (Jul), mid-size — 40 min @20 m [ASSUMED] | op | 40 min @20 m | 50.2 | -9.2% | 45.6 | crosses <50 CONCERNING |
| 8 | Scheduled monthly maintenance dose (Aug) — no emergency top-offs after ch18's limit [ASSUMED] | dose | 1 dose | 45.6 | +8 (1 dose) | 53.6 | recrosses >=50 |
| 8 | Continued global intervention (Aug), Jakarta-class — 50 min @30 m [ASSUMED cadence; topology: 'continued ops between Ch19-22'] | op | 50 min @30 m | 53.6 | -16.6% | 44.7 | crosses <50 CONCERNING |
| 8 | Continued global intervention (Aug), mid-size — 40 min @20 m [ASSUMED] | op | 40 min @20 m | 44.7 | -9.2% | 40.6 | <50 CONCERNING |
| 9 | Scheduled monthly maintenance dose (Sep) — no emergency top-offs after ch18's limit [ASSUMED] | dose | 1 dose | 40.6 | +8 (1 dose) | 48.6 | <50 CONCERNING |
| 9 | Continued global intervention (Sep), Jakarta-class — 50 min @30 m [ASSUMED cadence; topology: 'continued ops between Ch19-22'] | op | 50 min @30 m | 48.6 | -16.6% | 40.5 | <50 CONCERNING |
| 9 | Continued global intervention (Sep), mid-size — 40 min @20 m [ASSUMED] | op | 40 min @20 m | 40.5 | -9.2% | 36.8 | <50 CONCERNING |
| 9 | CHECK — topology ch22 (late Month 9): 'Ahdia returns <10%' | anchor |  | 36.8 | — | 36.8 | <50 CONCERNING |
| 10 | Scheduled monthly maintenance dose (Oct) — no emergency top-offs after ch18's limit [ASSUMED] | dose | 1 dose | 36.8 | +8 (1 dose) | 44.8 | <50 CONCERNING |
| 10 | Continued global intervention (Oct), Jakarta-class — 50 min @30 m [ASSUMED cadence; topology: 'continued ops between Ch19-22'] | op | 50 min @30 m | 44.8 | -16.6% | 37.3 | <50 CONCERNING |
| 10 | Continued global intervention (Oct), mid-size — 40 min @20 m [ASSUMED] | op | 40 min @20 m | 37.3 | -9.2% | 33.9 | <50 CONCERNING |
| 11 | Scheduled monthly dose (Nov, before the manhunt) | dose | 1 dose | 33.9 | +8 (1 dose) | 41.9 | <50 CONCERNING |
| 11 | Manhunt — penthouse-escape freeze (ch23), ~10 min @15 m | freeze | 10 min @15 m | 41.9 | -1.8% | 41.1 | <50 CONCERNING |
| 11 | Manhunt — chase-week freezes, cumulative (ch23 'Ahdia freezes'), ~20 min @15 m | freeze | 20 min @15 m | 41.1 | -3.6% | 39.7 | <50 CONCERNING |
| 11 | END OF MONTH 11 — pre-endgame level | anchor |  | 39.7 | — | 39.7 | <50 CONCERNING |
| 12 | Translocation, 800 miles, 8 people — FAERIS; costs NO baseline (#16) | faeris |  | 39.7 | — | 39.7 | <50 CONCERNING |
| 12 | Reactor freeze 10 m 47 s — TIER 2 (opposing quantum field): 31.2% of remaining per minute (M=516x), FIT to land 0.7 | freeze_T2 | 10m47s | 39.7 | -98.2% | 0.7 | crosses <1 TRANSCENDENCE RISK |
| 12 | Emergency stabilisation after the freeze — CLINICAL only; no ledger add (else 0.7 cannot hold; see UNRULED) | anchor |  | 0.7 | — | 0.7 | <1 TRANSCENDENCE RISK |

**Path A lands:** January opens 57 → riot 48 (first crossing of 50, at the first use) → Month 1 low 44 → oscillates 45–60 through Month 6 on the dose/spend equilibrium → ch17 week 65 → 47 → ch19 **52.2** → Months 7–10 floor toward the 30s → Month 11 ends **39.7** → reactor **0.7**.

### Second-half alternatives (Months 7–12) — the Director must choose one; the ruled model cannot produce the topology's single digits with monthly full-yield doses

Under a fixed add-back D and a monthly spend fraction s, the number cannot fall below **D ÷ s** while doses continue (D = 8, s ≈ 24 %/month → floor ≈ 33). That is arithmetic, not a choice. Three ways to the 0.7:

| Path | Months 7–10 doses | Month 11 ends | Tier-2 rate needed for 0.7 | "Safe 3–4 min" option would land | Notes |
|---|---|---|---|---|---|
| **A** (headline) | monthly, full yield | **39.7** | 31 %/min | 10.7 (just above critical) | Faithful to §7e and "fixed." Most of the book's burn happens in the last eleven minutes. Contradicts topology ch22 "<10 %" and "~7 pre-freeze." |
| **B** | **withheld** — Ruth keeps ch18's "or lose treatment access" after Ahdia breaks the 72-hour agreement (ch19) | **16.2** | 25 %/min | 5.9 (critical) | Closest to the topology's shape (dangerous by Month 8, teens by Month 10). Requires a plot beat: Ruth actually withholds for four months — not on any page. |
| **C** | monthly, but **yield fails below critical** (add = D × min(1, R/10): CR-7 repairs unconverted tissue; with little left there is nothing to repair — ch24's "cells burn") **plus heavier ops** (three Jakarta-class a month) | 22.5 | 27.5 %/min | ~8 | The only reading that also explains ch22's "treatment daily, still <10 %," the endgame's "emergency treatment stabilises at 0.7," and Book 3 opening at 0.7 with Ruth still treating. Modifies "fixed" — needs a ruling. |

---

## 3. Where this lands vs the synopsis's struck numbers (for the Director's eye — nothing fitted to them)

| Point | Synopsis / topology (struck or unanchored) | This table (Path A) | Comment |
|---|---|---|---|
| Book 1 end | ~90 % | **33.3** | Ruled (#12): nobody starts at 100. |
| January open | 100 % | **57.3** | 33 + three monthly doses. Four three-week doses would give 65. |
| After the riot | 100 → 90 | 57 → **48.3** (−15.7 % of remaining) | A 47-min plaza-scale freeze at panic. The old −10 points is reproduced in PROPORTION (−16 %) at a lower level; the first use of the power in 2A crosses 50. |
| After Jakarta | 90 → 67–71 (−16–20 %) | 54 → **43.6** (−19.6 %) | The old percentage falls out of a 60-min, 30-m field on its own. |
| After Eastern Europe | 73 → 52 (−29 %) | 54 → **46.1** (−15 %), dose → 54 | Smaller fall; the emergency dose pulls her back up. Old drop needs a 90-min field. |
| ch17 "68 last week" → "54" | 68 → 54 (−21 %) | **64.7 → 46.7** (−28 %) | Shape reproduced by the 7-ops-in-5-days week + the junta. |
| ch19 anchor | **53.1** | **52.2** | **Keepable.** 53.1 exactly needs extractions at 12.5 min instead of 13 — inside the noise of the assumption. |
| ch20–21 | ~30–40 | 45–60 (A) / 30–40 (B) | Only Path B or C reaches it. |
| ch22, late Month 9 | <10 | 36.8 (A) / 22.7 (B) / 19 (C) | **Not reachable with monthly full-yield doses.** See §2's alternatives. |
| Pre-freeze | 10 → 7 (translocation cost) | 39.7 (A) / 16.2 (B) | The 10 → 7 is struck on its face (#16: the jump is FAERIS's). |
| Post-freeze | 0.7 | **0.7** | Locked; hit by construction (Tier-2 fit). |

---

## 4. Sanity against Book 1's page — every on-page figure and whether the model reproduces it

| Page | Figure | Model | Verdict |
|---|---|---|---|
| ch14b | "replaced approximately half your life force" | 100 on the scale = the surviving half | Scale definition; consistent. |
| ch14b | "Six hours … 47 amplifications … 23 % of total reserves"; "a quarter of everything you had left" | Fit point: 360 working 6-m field-minutes → 23 % of remaining | Reproduced (by construction). |
| ch14b, 15, 16 | "eighteen months" at a survivable rate — "short freezes, small corrections" | From 68 (post-ambush) to <1 in 18 months = 21 %/month = ~11 working minutes a day at 6 m; to <10 = ~5 min a day | Consistent: "eighteen months" is a few minutes of use a day. |
| ch14b | "Four more like it and we are not having this conversation" | Five ambush nights leave 0.77⁵ = 27 % of the pre-ambush number — not zero | The line is TRUE as a frontier prognosis (five such nights = frontier collapse), not as ledger arithmetic. Under proportional decay no count of nights reaches zero. |
| ch15 | "reduced energy expenditure by thirty percent … cut your energy usage in half … bought yourself another year. Maybe more." | Radius term: 6 m → ~4.2 m = −30 %; → 3 m = half. Half rate: 68 → <1 takes 34 months instead of 18 | Reproduced; "another year, maybe more" is right. |
| ch16 | "You bought yourself a year in the training room. This week you spent it on them." | Team fields sit around the team, not her — they cannot be shrunk; the week's layered ops ran at the full rate | Consistent; the frontier (nosebleeds) paid the same week. |
| ch16 | "Eighteen months baseline. Maybe two years if you're conservative." | as above | Consistent. |
| ch19 | Telomere 18 % (CRITICAL); "Projected Viable Function: 18 months ± 6" if she stops completely | Frontier readouts; the ledger has no passive decay | Not contradicted; not ledger figures. |
| ch19 | "Tonight's intervention alone depleted another 4 %" | 4 % = 56 exposure units ≈ 28 min of two 6-m team fields, or 56 min of one, plus the container-yard finale | Reproduced by a docks night of ~1–2 h of intermittent team support (ch18: "Two hours in it tonight"). |
| ch19, 23 | "Weeks. Maybe less." | Frontier prognosis at her rate | Ledger-neutral. |
| ch20 | "Weeks to eighteen months, if it works. Two years if we're lucky." | D = 8 monthly against light use holds the number level indefinitely; against ops it buys exactly what Ruth says | Consistent. |
| ch24 | "eight more doses, three weeks between each one — six months" | §7e schedule; D applies per dose | Consistent. |
| ch24 | "fifty percent max"; "First few integrated. Last ones barely worked. Maybe thirty percent total regeneration." | Fit point for D (rushed yield ~30 % of 7 × D) | Reproduced with D ≈ 8 and a single-digit docks level. |
| ch30 | "she left at approximately one-third cellular recovery" | Month 0 = 33.3 (ruling); page-strict it is pre-Main-Street | **Flagged** — §1 ambiguity #4. |
| ch30 | "How close did you come to draining all of your life force yesterday?" (unanswered) | Main Street = Tier 2; 33 → ~2 in ~7.5 Tier-2 minutes at the endgame's fitted rate | Plausible; this is the only page check on Tier 2 and it is loose. |
| ch30 | "The Seed's dormant. Maybe permanently." | A lie (#12); the ledger is live at 33 | Consistent. |
| 14a | 23-minute unconscious freeze at ~6.1 m | 1.7 % of remaining | Not a page number; small enough that she would not have noticed, as written. |
| ch20 | FAERIS 10 % alone → 50 % in six months → full in 12–18 | Not the ledger. The 2A "someone's helping" fields (ch17) are not hers and are NOT priced | Consistent with #16 and §7. |

---

## 5. UNRULED — what the Director must rule (in order of consequence)

1. **Treatment after ch19 (Path A / B / C).** The single largest fork. A fixed monthly add-back floors her at D ÷ s ≈ 33; the topology's "<10 by Month 9–10" and Book 3's "0.7, Ruth still treating" need B (Ruth withholds) or C (yield fails below critical). Crew recommends **C** — it is the ch24 mechanism already on the page ("cells burn"; "energy expenditure is exceeding regeneration") and it is what lets 0.7 HOLD into Book 3 despite ch22's "treatment daily" and the endgame's "emergency treatment stabilises." But C modifies "fixed," so it is the Director's.
2. **Month 0: 33.3 (ruling text) or ~10 (page-strict, after Main Street).** §1 ambiguity #4. Twenty points of difference through the whole year.
3. **Dose size D = 8** (range 5–10 from the ch24 arithmetic). D = 5 opens January at 48 and cannot hold the 50s; D = 10 opens at 63 and floors the second half at 40+. Also: the interregnum as three monthly doses (57) vs four three-week doses (65).
4. **Cadence of ops in Months 3–5.** Priced as one Jakarta-class intervention a month plus 2–3 extractions and two doses; that cadence is what makes her oscillate in the 45–60 band that the 53.1 anchor sits in. Fewer ops and the doses push her toward 80; more and she is under 30 by Month 4.
5. **Exile Island: many small or few large.** 28 extractions at 5 min/3 m (a room, shrunk field) cost 0.2 % each — 5 % for all 28, invisible on the ledger; at 13 min/20 m (a compound) 3.1 % each — 60 % of what remains across the run, before doses; at 30 min/50 m (a palace, a parade ground) 16.6 % each — lethal by the tenth. The table uses the middle. The junta's eight-in-one-freeze is priced as one large field. Whether Kain's Month-4 exile is Tier 2 (an avatar carrying anything of the Heart) is also unruled; if it is, it costs ~30 % of remaining on its own.
6. **Sizes of Jakarta and Eastern Europe.** Priced 60 and 45 minutes at 30 m from "11,000 / 8,000 saved" and nothing else; the synopsis does not say what either op was. Radius scaling is linear (cost ∝ radius); if the Director prefers area scaling, plaza-scale freezes cost ~5× more and the riot alone is a 57 % event.
7. **Whether the endgame freeze alone can take her from Month 11 to 0.7.** Yes, under every path — because the Tier-2 rate is FIT to make it so, and nothing else on the page constrains it except Main Street (loose: 7–10 Tier-2 minutes at these rates, plausible for a fight in bursts). What the Director is really choosing is how much of the fall the reactor carries: 39 points (A), 15 (B), or 22 (C). The topology's "safe 3–4 min vs guaranteed 10+" framing is reproduced by all three (safe lands at 6–11, i.e. critical; full lands under 1).
8. **The post-freeze "emergency treatment stabilises at 0.7."** Under a fixed D = 8 add-back a dose after the freeze reads 8.7, not 0.7; the table treats the stabilisation as clinical (frontier), not ledger. Path C makes the dose read ~0.06 and the 0.7 holds. Same question as #1, seen from the other end.
9. **Months 7–10 have no NAMED Ahdia ops in the synopsis.** With named events only and monthly doses she RISES to 84 by Month 11 and the reactor needs 36 %/min. The "continued ops" cadence in the table is invented to a stated size and must be either named in the 2B synopsis or replaced by Path B.
10. **Whether the ledger decays passively.** The ruling's "each use converts" implies no; the page's "Cellular Degradation Rate: Accelerating" and "dead in 11 days without treatment" read as frontier. If the Director wants a passive term, everything above shifts down and treatment gets a second job (slowing the ledger, §5b's phrase) — not modelled.
11. **The interregnum's spend.** Priced at zero (nothing named; the opposition thinks her dormant). If she is already operating in Oct–Dec, January opens lower than 57.
12. **Team-support fields in 2A.** The team's powers are her dilation bubbles (§7), the expensive mode — but 2A keeps her absent from the team's fights and ch17 has the team "succeeding when Ahdia wasn't present — 'Someone's helping'" (FAERIS learning, or Prime — unruled, not hers). No team-support field is priced except the manhunt allowance. If the Director wants her fielding the team in any 2A op, add ~4 % per hour per simultaneous 6-m field.

---

*Built by crew 2026-09-07 from the page and the 2026-09-07 rulings. The synopsis (`5_story_bibles/book_4/Series_synopsis.md`) and the 2A topology were read and not touched. Script and fit in the session scratchpad; the CSV is the table's rows verbatim.*
