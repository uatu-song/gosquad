# Go Squad Session Handoff

**Last Updated:** 2026-07-26 (fresh-start rebuild: new canon system + numbering ruling + prose pipeline proven)
**Session:** Kit ingest → `_canon` engine → 8-book renumbering → style-constraint layer → CH18 cold-rewrite pilot (5 generations)

> ⚠️ **This repo changed shape on 2026-07-26.** There is now a working
> canon/verification system (`_canon/` + `canon/`), the A/B book numbering is
> retired, and a cold-agent prose pipeline is proven. Read this file, then
> `5_story_bibles/sessions/SESSION_LOG_2026-07-26.md` for the full detail.

---

## FIRST ACTION, EVERY SESSION

```bash
python3 _canon/tools/audit.py --book book_1      # canon check (any book key)
python3 _canon/tools/codex.py --book book_1 --gaps
python3 _canon/tools/check_promises.py --book book_2   # the Director's open questions
```

The pre-commit wall runs `audit` + `typography` + `codex --enforce` across all
books on every commit. `git push` needs `--no-verify` (git-lfs missing in the
devcontainer; text-only commits).

---

## IMMEDIATE RESUME POINT

### Book 2 bridge rewrites — BLOCKED on one Director ruling (2026-07-26)

**The block:** four of Book 2's six worst chapters are Ahdia POV. `CLAUDE.md`
says flatly *"NO internal Ahdia scenes in Book 2"* — but the drafted first
edition has **nine** Ahdia-POV chapters (01, 02, 05, 06, 07, 08, 09, 13, 18).

**Evidence gathered:** zero mentions of Exile Island, dictators, or the
operations in *any* drafted chapter (the only hits are "translocation", the
power mechanic). The draft withholds the **secret**, not her presence — the
grief chapters *are* the fridging mechanism, and the reader is fooled because
the depression on the page is real.

**Recommended reading, awaiting ruling** (filed in `canon/book_2/PROMISES.jsonl`):
Ahdia POV is permitted and necessary; what is banned is any scene depicting or
hinting at the operations. If the ruling is instead a hard ban on her POV, nine
chapters need POV reassignment before any rewrite is meaningful.

**Once ruled, in order:**
1. Cut a **Book 2 Ahdia embodiment** — the 10 ratified embodiments are
   Book-1-arc-specific; Book 2 Ahdia (performing grief over live operations) is
   a different psyche. Scavenge: `2_method_actor/stewards/Ahdia_Bacchus_Steward.md`
   (Book-2-specific), `1_writing_guides/Ahdia_Voice.md`, and the ratified 5-D
   format in `2_method_actor/book1_embodiment/`.
   *Note:* no Book 2 chess scaffold exists (Director selects the game), so the
   embodiment cannot use a triplet lens — build the spine on the double life.
2. **Pilot CH08** with `_canon/REWRITE_PACKET_TEMPLATE.md` to prove the
   template generalizes beyond CH18.
3. Batch the rest.

**Book 2 worst chapters** (composite tic burden; CH18-ed1 = 219 was the
Director-confirmed "egregious" calibration point):
CH09 (307, but only 446w) · **CH08 (274)** · CH15 (237, Ruth/Leah intercut) ·
CH18 (236) · CH07 (235) · CH19 (227, Ben). Book 2's *median* chapter scores
where Book 1's *worst* do.

---

## Standing doctrine (ruled 2026-07-26)

- **Fresh start.** The old tree is **quarry**. Nothing legacy is edit-of-record
  until re-declared in the new system. When a need arises: scavenge the best
  existing asset, then cut a **fresh customized version** into the new system —
  never wire the old file in directly.
- **Series numbering — LOCKED.** 8 books, sequential integers, **no letter
  suffixes ever.** Splits are not pre-declared; if a book earns one during
  generation it takes two numbers then and downstream renumbers.
  Translation table: `/LEGACY_NUMBERING.md`.
- **Emergent-first.** Book 1 is near-done (polish only). Everything beyond it is
  regenerable through the chess-steward pipeline. Books 5–8's Jan-2026 READMEs
  are candidate studs, not canon.
- **The rewrite pipeline is a BRIDGE**, not repair-for-what-ships. It holds
  chapters until the rebuild reaches them. ⇒ Book 1's climax is **out of
  scope** (the rebuild is 1–2 steps away); Book 2 is the bridge target.
- **Surface, don't fix.** Only the Director rules a wobble, a red-herring, or a
  motif. Crew files questions; crew does not pick winners.

---

## The two workflows

### A. Rebuild (generation) — Book 1 at step 9 of 10
Topology → studs → chess game → move map → triplets → embodiments → steward run
→ 5-agent eval + Enforcer → **cinematic blocking (NEXT)** → prose.
Book 1's ratified assets: `BOOK1_TRIPLETS.md`, `BOOK1_MOVE_MAP.md`,
`BOOK1_REBUILD_STUDS.md`, `2_method_actor/book1_embodiment/` (10 files),
`steward_run1/` + `eval/`. Two Director calls from the 2026-06-14 session are
**still open** (reader-irony rulings; Firas's canonical sidelining move —
though the 06-14 log records M7 as decided; verify before acting).

### B. Bridge (prose repair) — proven on CH18, 5 generations
Packet (`_canon/REWRITE_PACKET_TEMPLATE.md`) → **cold agent** (fresh context,
never shown infected prose, never reused) → 3 mechanical gates → Director read.
**The packet is the memory; agents stay disposable.** Every rejected draft
becomes a constraint, so the failure never recurs.

CH18 measured, ed1 → v5: short-burst **120.1 → 31.8**/1K · em-dash **9.3 →
2.5**/1K · banned constructions **present → 0** · invented nouns **0**.

---

## Canon warnings (verify against the codex before relying on these)

### Critical
- **Ahdia POV in Book 2** — see the blocking question above; scope is unruled.
- **"Auerbach" is Ahdia's CADENS codename**, not her surname (Bacchus).
  Codename class: Howitzer, Greyhound, Mercury, Overseer. *The series is named
  for her codename.*
- **Firas is DISPLACED, not dead** — dissolves into the singularity; returns Book 7.
- **The team's powers were never real** — Ahdia slowing time, amplified and
  distributed by FAERIS drones. An EMP kills the *relay*, never in-body tech.
- **Prime = Ahdia-1; current = Ahdia-5**; 5 iterations total (NOT 43/47).
- **Kain wins the presidency** (312 EV). **Leta dies** (Book 3, killed by Webb).
- **28 vs 37 dictators** — UNRESOLVED.

### Character
Victor has NO dead wife (partner is Leah) · Bourn is a WOMAN (she/her) ·
Korede is 17 · Eidolon AMPLIFIES fear (cannot create) · Tess does NOT kill Webb ·
Leah is a BARISTA · Ben's background is MILITARY, not police · Ben's wife
Sarah — cause of death UNSPECIFIED (never invent).

---

## Open questions awaiting the Director

| # | Question | Where |
|---|---|---|
| 1 | **Ahdia POV scope in Book 2** — blocking the bridge | `canon/book_2/PROMISES.jsonl` |
| 2 | Forgettable-face signature: rhyme with the Kain clone, or collision? | `canon/book_1/PROMISES.jsonl` |
| 3 | House typography — gate stays census-only until ruled | `_canon/books.yaml` |
| 4 | Motif function-tests → `protected_sites`: "hand still reaching" ×9, "forty seven minutes" ×8, "two thousand people" ×10 | unfiled |
| 5 | Book 5's Jericho/Eidolon conflict vs ratified Book 4 Eidolon canon | unfiled |
| 6 | Two open Book 1 rebuild calls from 2026-06-14 (reader irony; Firas sidelining) | prior session log |

---

## Key file pointers

| Purpose | File |
|---------|------|
| **This session's full detail** | `5_story_bibles/sessions/SESSION_LOG_2026-07-26.md` |
| **Book registry / numbering authority** | `_canon/books.yaml` |
| Legacy-label translation | `/LEGACY_NUMBERING.md` |
| The engine | `_canon/tools/` (audit, codex, tic_census, ferret, check_nouns, check_facts, check_promises) |
| **Reusable rewrite packet** | `_canon/REWRITE_PACKET_TEMPLATE.md` |
| Series style rules (R100–R104) | `canon/series/RULES.yaml` |
| Per-book canon layers | `canon/book_1/` … `canon/book_8/`, `canon/book_1_ed1/` |
| Book 1 first edition (quarry, 30 ch) | `6_manuscript/book_1/first_edition/` |
| CH18 pilot lineage (packet + v1–v5) | `6_manuscript/book_1/rewrite_pilot/` |
| Rulings (don't relitigate) | `canon/book_1_ed1/DECISIONS_LOG.md` |
| Book 1 rebuild assets | `5_story_bibles/book_1/` + `2_method_actor/book1_embodiment/` |
| Prose doctrine | `PROSE_VOICE_DESIGN_PROBLEM.md` |

---

**End of Handoff**
