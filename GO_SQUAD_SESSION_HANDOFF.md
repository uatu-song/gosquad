# GO SQUAD — SESSION HANDOFF

**Updated:** 2026-09-02, end of session. **Read this first.**

---

## RESUME POINT

**BOOK 1 IS SHIPPED.** ARC at commit `8d6417f`:
`6_manuscript/book_1/GoSquad_Book1_ARC.epub` — 30 chapters + epilogue,
**77,500 words**, uncorrected-proof notice stamped with date + git SHA, no
internal notes, no provenance lines. 17/17 default-band chapters green, ch22
green on its Director-ruled band (`--length-band 3000:3600`), ch14a/14b green
as a pair. Exact tag census: **0 hanging comma-quotes across all 30 chapters.**
Every frozen span byte-identical to `first_edition_clean/`.

**The Director wants to move on to the subsequent books.** Nothing on Book 1
blocks that. What remains on Book 1 is veto-only (see OPEN below).

**Book 2 resume point:** 23 chapters, 47,848 words, `6_manuscript/book_2/`.
**The first thing Book 2 needs is a ruling**, not prose:
`ahdia-pov-withheld-scope` in `canon/book_2/PROMISES.jsonl` — does "Ahdia's POV
is withheld in Book 2" ban Ahdia-POV chapters outright, or only scenes that
would show her secret operations? Everything downstream in the Book 1→2 bridge
waits on it. Book 2's own signature tic is "the particular" (R100, 104 warnings
in the audit) and its "voice was" rate is 1.75/1K.

---

## HOW THE PIPELINE WORKS (for any future rebuild)

1. **Beats come from the scaffolds**, never from the source prose:
   `5_story_bibles/book_1/BOOK1_MOVE_MAP.md` (stud table; several studs are
   Director-framed and binding) and `5_story_bibles/book_1/steward_run1/`.
2. **Dialogue is frozen** — extracted programmatically from
   `6_manuscript/book_1/first_edition_clean/chapter_NN.txt`, byte-identical.
   A Director dialogue edit goes into the source pre-freeze so spans stay in sync.
3. **The cold drafting agent NEVER sees the source draft.** Packet reading list
   only. (Line-edit agents restoring tags this session consulted the source for
   attribution facts — disclosed in the log; not the cold-draft rule's concern,
   but crew decides what an agent sees. Say so in the brief either way.)
4. **Revisions go back to the agent.** Crew does not write prose. Mechanical
   one-word fixes with a literal anchor and a count assert are fine.
5. **Canonical filenames resolve through `build_compilation_epub.py`.**
   ch18 is `chapter_18_metric_v3.txt`; ch14 is `14a` + `14b`.
6. **Typeset** with the scratchpad `chicago.py` (recreate per session). Round-trip
   two shipped chapters before trusting it.
7. **Gate:** `_canon/tools/check_style.py` (20 bands, narration-only; `-ly`
   ceiling-only; `--length-band MIN:MAX` needs a logged ruling) + `check_nouns.py`.
8. **Build and then VERIFY THE ARTIFACT**, not the inputs — open the epub and
   probe the text. The wall-of-text bug lived in every epub ever built until
   somebody read one.

---

## STANDING RULES EARNED THE HARD WAY

- **Stage commits BY NAME. Never `git add -A`.** It swept the Director's live
  edits into a crew commit. **Always push after committing.**
- **A frozen-span divergence gets ATTRIBUTED before it gets "fixed."**
- **An unqualified instruction does not get qualified by crew.** No invented
  carve-outs. If a carve-out looks obviously right, that's the one to ask about.
- **DECISIONS_LOG attribution convention** (top of that file): Director /
  Director-assignment+crew-model / crew-veto-open. A crew decision does not
  become a Director ruling by going unchallenged.
- **No gate band may have a floor that padding can satisfy.**
- **Never regex a span boundary.** Literal anchor + count assert.
- **A truncated match is not a checked match.** Three errors this session came
  from reading a cut-off grep line and calling it verified (an age, a speaker,
  a quote's tail). Print the whole line or don't conclude.
- **Check the harness before believing a mass failure.** 0/17 green was a
  script running from the wrong directory. A tool reporting everything broken
  is usually the thing that's broken.
- **Rebuild packets: reduce a tag to "said"; never drop it.** The rebuild
  agents dropped whole tags wherever the source tag carried an adverb or a
  non-said verb, leaving 41 hanging comma-quotes and two lines in the wrong
  mouth. The detector is trivial: a comma-quote at end of line.
- **Counting-as-interiority and the accounting-metaphor family are gone
  corpus-wide** (R105/R106, no exemptions except Kain-POV for R106). Also swept:
  "the way X verbs" simile frame, trailing ", which is/was", unlicensed adverbs.
  Fix by deletion, never by synonym swap.

---

## BOOK 1 — RULINGS THIS SESSION (all logged)

- **Whitford:** minor in Book 1, an ongoing threat in Book 2, corrupt only.
  His vanishing after ch17 is scope. Tess facing her father is Book 2's.
- **Staging A** (Tess on the camera grid, then in) ruled for ch22.
- **Twenty-six hours** for Ahdia's time under, both ch24 sites, derived from
  the page's own clock (docks 2100 → isotopes at 2am → mansion "tonight" a day
  later → she surfaces during the mansion feeds). Eighteen was never coherent.
- **41 dropped tags restored**, zero period conversions; ch22 "That was fun"
  returned to Tess; ch19 "Worth it." returned to Ahdia.
- **ch9 training paragraph cut to two sentences** — paid by ch22.
- **Ages:** twenty-seven at both sites (ch14a, ch19).

---

## OPEN, AWAITING THE DIRECTOR (veto-only — none blocks Book 2)

1. **The number twenty-six** — crew derivation, shown in the log. Veto open.
2. **ch22 order** Victor "insane" → Tess "fun" → Leah's laugh (agent's call);
   the plinth case cracking when a guard is shoved into it (a new physical fact
   the ch22 agent added to open Kain's route). Both reversible.
3. **ch30** three paragraphs merged to one at the Carl Tucker greeting.
4. **The Intermediary** — the woman on the phone with no line into the
   building (ch17 only, promises to call again) never returns on the page; the
   epilogue's "a woman's voice" is presumably her, unconnected. Not ruled.
   Presumed Book 2 setup (Bellatrix/Geneva, hidden orchestrator) like Whitford.
5. Veto open on: audit rejections A1/A2/B3; any single deletion from the
   the-way / adverb / counting sweeps.

---

## KEY FILES

| Purpose | File |
|---|---|
| **The shippable ARC** | `6_manuscript/book_1/GoSquad_Book1_ARC.epub` (builder: `build_arc_epub.py`) |
| World state for agents | `canon/book_1_ed1/CH01-25_TOPOGRAPHY.md` |
| Mechanics + rulings | `canon/series/TEMPORAL_MECHANICS.md` (§5b, §7–§7h) |
| Rulings log | `canon/book_1_ed1/DECISIONS_LOG.md` |
| Punch list | `canon/book_1_ed1/PUNCH_LIST.md` |
| Series style rules | `canon/series/RULES.yaml` (R100–R106) |
| Packet template | `_canon/REWRITE_PACKET_TEMPLATE.md` |
| Beats | `5_story_bibles/book_1/BOOK1_MOVE_MAP.md`, `steward_run1/` |
| Book 2 blocker | `canon/book_2/PROMISES.jsonl` → `ahdia-pov-withheld-scope` |
