# GO SQUAD — SESSION HANDOFF

**Updated:** 2026-08-31, end of session. **Read this first.**

---

## RESUME POINT

**Book 1 metric rebuild: ch12–27 complete and gated.** Next chapter is **CH28**.

Compilation: `6_manuscript/book_1/GoSquad_Book1_compilation.epub` — 27 chapters,
~68,000 words. All 15 gated units clean (ch14a/14b gate as a combined pair
against the ch14 source, 139/139 spans).

---

## HOW THE PIPELINE ACTUALLY WORKS (corrected this session)

1. **Beats come from the scaffolds**, not from the first-edition prose:
   `5_story_bibles/book_1/BOOK1_MOVE_MAP.md` (stud anchor table — several studs
   are Director-framed and are binding) and `5_story_bibles/book_1/steward_run1/`
   (ten per-character beat files). `BOOK1_BLOCKING.md` covers **Ch1–8 only**.
   **The steward runs are SILENT for ch23–27** and resume at **M131–136**, which
   is ch28–30. **CH28 HAS AUTHORED BEATS. USE THEM.**
2. **Dialogue is frozen** — extracted programmatically from
   `6_manuscript/book_1/first_edition_clean/chapter_NN.txt`, byte-identical.
3. **The cold agent NEVER sees the source draft.** Packet reading list only.
4. **Revisions go back to the agent.** Crew does not write prose. Mechanical
   trims to hit a band are fine; new sentences and new beats are not.
5. **Canonical filenames resolve through `build_compilation_epub.py`**, never by
   convention. **ch18 is `chapter_18_metric_v3.txt`** — `_v1` is a dead draft.
6. **Typeset** with the scratchpad `chicago.py` (recreate per session; it gets
   wiped). It has bitten twice: a quote after an em dash, and nested single
   quotes. **Round-trip two shipped chapters before trusting it.**
7. **Gate:** `check_style.py` (20 bands, narration-only) + `check_nouns.py`.

---

## STANDING RULES EARNED THE HARD WAY

- **Stage commits BY NAME. Never `git add -A`.** It swept the Director's live
  edits into a crew commit.
- **A frozen-span divergence gets ATTRIBUTED before it gets "fixed."** Ask who
  wrote it. The Director's edits are canon; source and packet follow them.
- **An unqualified instruction does not get qualified by crew.** No invented
  filters narrowing a population. If a carve-out looks obviously right, that is
  exactly the one to ask about.
- **DECISIONS_LOG attribution convention** (top of that file): Director /
  Director-assignment+crew-model / crew-veto-open. A crew decision does not
  become a Director ruling by going unchallenged.
- **No gate band may have a floor that can be satisfied by padding.** The -ly
  floor caused agents to add appraisal adverbs; it is gone (ceiling-only 0–17).

---

## CH28 REQUIREMENTS (locked)

- **"We killed them." must get an owner.** It is unattributed in ch27 by design
  (Kain cannot tell who spoke). If ch28 also stays outside the team's interior,
  the Go Squad became killers offstage. **Director-ruled: ch28 pays this.**
- **The ch25 anger at Ruth stays alive** — assigned as a beat, registered from
  outside, unresolved.
- Steward beats exist for Ahdia, Firas, Ruth, Kain and Tess at M131–136: the
  singularity, the human chain, the autoinjector into HER not him, *"Oh hey. I
  knew you were in there somewhere,"* Firas displaced (not dead; returns Book 7),
  Kain clone-surviving off-board, Bourn's missile as the real kill.

---

## OPEN, AWAITING THE DIRECTOR

1. **`canon/book_1_ed1/AUTHOR_CHAPTERS_SURFACED.md`** — ch08 is the only author
   chapter with a measurable problem (ch01/03/04/05 measured clean). Nothing
   changed; per-passage rulings needed. Recommendation: the surgical option.
2. **The ch24 "three hours" → "eighteen hours" dialogue edit** was crew-derived
   from §7d and has **never been explicitly confirmed.** Still pending.
3. Veto open on: the A1/A2/B3 audit rejections, and any single adverb or
   "the way" deletion from this session's sweeps.

---

## KEY FILES

| Purpose | File |
|---|---|
| World state for agents | `canon/book_1_ed1/CH01-25_TOPOGRAPHY.md` |
| Mechanics + rulings | `canon/series/TEMPORAL_MECHANICS.md` (§5b, §7–§7h) |
| Rulings log | `canon/book_1_ed1/DECISIONS_LOG.md` |
| Series style rules | `canon/series/RULES.yaml` (R100–R106) |
| Packet template | `_canon/REWRITE_PACKET_TEMPLATE.md` |
| Beats | `5_story_bibles/book_1/BOOK1_MOVE_MAP.md`, `steward_run1/` |
