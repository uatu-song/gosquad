# Fresh-Start Rebuild — Session Log 2026-07-26

**Scope:** Stood up an entirely new canon/verification system from a portable
kit, retired the A/B book numbering, built a measured style-constraint layer
from the repo's own audit findings, and ran a cold-agent rewrite pipeline
through 5 Director-reviewed generations on one chapter. Started from "read this
kit"; ended with a proven prose pipeline and a generalized packet template.

**Series-level, not book-level** — hence `5_story_bibles/sessions/` rather than
a per-book directory. This session touched numbering, tooling, and doctrine
across all 8 books.

---

## What was accomplished (in order)

1. **Read + pressure-tested the portable kit** (`book_canon_system_kit_20260725.zip`).
   Verified rather than assumed: `audit.py` crashed on its own template
   (`rules: []` vs `.items()`), `INDEX.yaml`'s schema didn't match its reader,
   `bookconfig.py` had zero importers, and `check_typography.py` scanned 0
   files while printing "house typography intact ✓" — the exact
   zero-reads-as-clean trap its own docs warn about.

2. **Built the new engine fresh** (`_canon/`) rather than porting the broken
   paths. Config-driven via `_canon/books.yaml`, multi-book, no literal paths
   in any tool. Every gate now **refuses to report clean on zero files.**
   Pre-commit wall installed and green across all 8 books.

3. **Director ruling — series numbering.** 8 books, sequential integers, **no
   letter suffixes ever.** Splits are not pre-locked; if a book earns one
   during generation it takes two numbers then and downstream renumbers.
   Executed: `book_2b`+`book_2B` → `book_3`; old `book_3` → `book_4`; the
   Nov-2025 duplicate → `book_4/early_planning_2025/`. Legacy file *contents*
   deliberately unrewritten (quarry is translated on ingest, not falsified).
   Translation table: `/LEGACY_NUMBERING.md`.

4. **Asset gathering (4 scavenger hunts):** story bibles, character
   stewards/profiles/embodiments, writing style guides ("the beating heart"),
   and the generation method. Findings in the handoff; key discovery is that
   the method exists only as *instances* (a Book-3-specific manual, a
   Book-1-specific scaffold) — there is still no book-agnostic pipeline doc.

5. **Recovered a usable Book 1 source.** No clean manuscript existed — the .txt
   and the .epub are both the same PDF extraction (318 embedded running
   headers, 418 broken words). Extracted the epub's 30 chapters and cleaned
   **artifacts only** → `6_manuscript/book_1/first_edition/`, registered as
   `book_1_ed1`, marked measurement-grade quarry.

6. **Built the style-constraint layer** from the repo's own measured tic
   inventory (`canon/series/RULES.yaml`, series-wide so a fix lands
   everywhere): R100 the-particular, R101 the full negation family, R102
   hedges, R103 somatic default, R104 voice-described. All `warning` severity
   — the layer measures quarry, it does not block it.

7. **Built three new tools:** `tic_census.py` (rate-based tics + early/late
   escalation ratio), `ferret.py` (n-gram mining for *undocumented* mutations),
   `check_nouns.py` (proper-noun drift gate for generated drafts).

8. **Reproduced the documented disease independently.** Book 1 ed1: fragment
   density 20/1K in the author's early chapters → 100–120/1K from ~Ch12, with
   em-dash escalation 7.4×. Book 2: no escalation curve, saturated from page
   one. Book 1 got infected midway; Book 2 was born infected.

9. **Ferret pass found mutations the 2026-04 audit missed:** "in her/his chest"
   (41 uses across both books) and the "X's voice was" formula (60 in Book 2,
   15 in Ch15 alone) — both showing **∞ escalation in Book 1** (zero instances
   in the author's own chapters). Pure-AI markers with near-zero
   false-positive risk against the author's voice.

10. **Determined POV for all 53 drafted chapters** by mechanical interiority
    scoring, evidence cited, ambiguous chapters verified by reading; filed to
    `CHAPTER_INDEX.yaml` for both books. INTERCUT chapters marked (POV-scoped
    rules auto-downgrade there).

11. **Cross-tabbed register by POV.** Book 2's four main POVs sit in one tight
    band — the Grade-C homogenization, now a number. The exception is
    Bellatrix's Ch12, the steward-embodiment chapter, which is structurally
    distinct: empirical support for embodiment-over-description.

12. **Ran the cold-rewrite pipeline on Book 1 CH18** — 5 generations, Director
    review at every step (detail below).

13. **Generalized the pipeline** → `_canon/REWRITE_PACKET_TEMPLATE.md`.

---

## The CH18 pilot — 5 generations

| | what changed | outcome |
|---|---|---|
| **v1** | first cold agent, packet v1 | passed every mechanical gate — while putting a civilian at the team's door and inventing "Delancey"/"Central City" |
| **v2** | + world constraints, name table; `check_nouns.py` built | secrecy + nouns clean; Director: epigram engine, villain collapse, bodiless prose, checklist takedowns |
| **v3** | + epigram budget, villain subtraction, embodied drain, takedown variation | villain became the chapter's strongest passage; but the epigram cull took two *ideas* out with the tic |
| **v4** | 11 Director-directed restorations + fixes | restorations landed; created a downstream redundancy and a new tic ("unhurried" ×4) |
| **v5** | 4 Director trims; grief line restored to the cold agent's original wording | **Director verdict: development finished** |

**Measured, ed1 → v5:** short-burst 120.1 → 31.8 /1K · em-dash 9.3 → 2.5 /1K ·
banned constructions present → 0 · invented proper nouns 0 · dialogue 21%.

---

## Director decisions made this session

- **Fresh start.** The old tree is quarry. Nothing legacy is edit-of-record
  until re-declared in the new system. Scavenge-then-fresh-cut, per need.
- **Series numbering — LOCKED.** 8 books, sequential integers, no letters. Splits
  emerge; they are not pre-declared.
- **"Auerbach" is Ahdia's CADENS codename**, not her surname (surname stays
  Bacchus). Codename class: Howitzer, Greyhound, Mercury, Overseer. Prose
  receipts: literal "Codename: Overseer" + the badge scene in ed1.
  ⇒ *The series is named for her codename.*
- **Emergent-first.** Book 1 is near-done (polish only); everything beyond it is
  regenerable. Books 5–8's Jan-2026 READMEs are candidate studs, not canon.
- **Cold-agent rewrites approved** for first drafts, with styleguides + scaffolds.
- **The rewrite pipeline is a BRIDGE**, not repair-for-what-ships — it holds
  chapters until the rebuild reaches them. ⇒ Book 1's climax is *out of scope*
  (the rebuild is 1–2 steps away); **Book 2 is the bridge target** (its rebuild
  waits until all of Book 1 completes).
- **CH18 v5: development finished.** Remaining irregularities are voice.

---

## The 11 craft constraints (each earned by a rejected draft)

Now carried in the packet template, so no future cold pass re-learns them:
epigram budget (≤5, no repeated shape) · cutting-a-tic-must-not-cut-an-idea ·
villain speech = subtraction · earn the drop · vary repeated structures · the
body is present · logistics survive a reread · no dropped nouns · endings stay
in register · a patch is not local · preserve text, not descriptions of text.

---

## Immediate next step

**Book 2 bridge rewrites — BLOCKED on one Director ruling.**

Four of Book 2's six worst chapters are Ahdia POV, and CLAUDE.md states flatly
*"NO internal Ahdia scenes in Book 2"* — but the draft has **nine**
Ahdia-POV chapters. Evidence gathered: **zero** mentions of Exile Island,
dictators, or the operations in any drafted chapter. The draft withholds the
*secret*, not her presence. Recommended reading (filed, awaiting ruling): Ahdia
POV is permitted; what is banned is any scene depicting or hinting at the ops.
If the ruling is instead a hard ban, 9 chapters need POV reassignment first.

**Then, in order:** cut a Book 2 Ahdia embodiment (the 10 ratified ones are
Book-1-arc-specific; Book 2 Ahdia — performing grief over live operations — is
a different psyche) → pilot CH08 to prove the template generalizes → batch.

**Book 2 worst chapters by composite tic burden:** CH09 (307, 446w
interstitial), CH08 (274), CH15 (237, Ruth/Leah intercut), CH18 (236), CH07
(235), CH19 (227, Ben). Book 2's *median* scores where Book 1's *worst* do.

---

## Open questions awaiting the Director

| # | Question | Filed in |
|---|---|---|
| 1 | Ahdia POV scope in Book 2 (**blocking** the bridge) | `canon/book_2/PROMISES.jsonl` |
| 2 | Forgettable-face signature: deliberate rhyme with the Kain clone, or collision? | `canon/book_1/PROMISES.jsonl` |
| 3 | House typography — `enforce` stays false until ruled | `_canon/books.yaml` |
| 4 | Motif function-tests: "hand still reaching" ×9, "forty seven minutes" ×8, "two thousand people" ×10 | unfiled — needs ruling to become `protected_sites` |
| 5 | Book 5's Jericho/Eidolon conflict vs ratified Book 4 Eidolon canon | unfiled |
| 6 | 28 vs 37 dictators (carried from prior sessions) | unfiled |

---

## Key file pointers

| Purpose | File |
|---------|------|
| **Book registry / numbering authority** | `_canon/books.yaml` |
| Legacy-label translation | `/LEGACY_NUMBERING.md` |
| The engine | `_canon/tools/` — `audit.py`, `codex.py`, `tic_census.py`, `ferret.py`, `check_nouns.py`, `check_facts.py`, `check_promises.py` |
| The wall | `_canon/hooks/pre-commit` (installed to `.git/hooks/`) |
| **Reusable rewrite packet** | `_canon/REWRITE_PACKET_TEMPLATE.md` |
| Series style rules | `canon/series/RULES.yaml` |
| Per-book canon layers | `canon/book_1/` … `canon/book_8/`, `canon/book_1_ed1/` |
| Book 1 first edition (quarry) | `6_manuscript/book_1/first_edition/` (30 ch) |
| CH18 pilot lineage | `6_manuscript/book_1/rewrite_pilot/` (packet + v1–v5) |
| Rulings | `canon/book_1_ed1/DECISIONS_LOG.md` |
