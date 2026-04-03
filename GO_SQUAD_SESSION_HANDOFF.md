# Go Squad Session Handoff

**Last Updated:** 2026-04-03
**Session:** Prose Audit, Embodiment Design, Book 1 Rebuild Decision

---

## IMMEDIATE RESUME POINT

### Series Topology — Then Book 1 Rebuild (2026-04-03)

**Resume at:** Build the series-wide topology. This is the agreed first step before anything else.

**Why series topology first:** Book 1 is being rebuilt from studs (see below). The series topology identifies what Book 1 must deliver for Books 2-8 — cross-book arcs, seed-to-payoff mapping, locked endpoints per book. Without the series view, the rebuild risks preserving studs that aren't actually load-bearing downstream, or missing ones that are.

**Sequence:**
1. **Series topology** — the ceiling everything fits under
2. **Book 4 topology** (old Book 3, dir `book_3/`) — direct recipient of Book 2B output, richest planning material (40 files)
3. **Books 5-8 topologies** — Phase 1 skeletons
4. **Book 1 move mapping** — assign 136 chess moves to chapters/phases, anchor 8 studs to specific moves
5. **Triplet assignments** — 3 chess pieces per character as cognitive architecture
6. **Embodiment instructions** — the missing layer between character bible and prose
7. **Steward runs for Book 1** — characters generate beats through triplet lenses
8. **Book 1 prose generation** — with embodiment active from word one

---

## MAJOR DECISION: Book 1 Rebuild (2026-04-03)

**Director decided to rebuild Book 1 from structural studs rather than retrofit prose fixes.** Not a rewrite (trying to say the same thing better). A rebuild (lay constraints, let the story emerge).

**Rationale:**
- Prose audit revealed amplification mechanism in AI-assisted writing (see below)
- Retrofitting fights AI defaults sentence by sentence
- Remanence (Director's other novel) proved AI prose survives disclosure scrutiny when the AI *embodies* characters rather than *describes* them
- The steward experiment's triplet mechanism (proven in Book 2B) provides the embodiment vehicle
- Book 1's early chapters were the Director's original pre-AI prose; later chapters show increasing AI default voice. The escalation isn't accumulation within sessions — it's the boundary between human and AI prose.

**Chess game selected:** Carlsen vs Nepomniachtchi, World Championship 2021, Game 6 (136 moves, longest WCC game ever, White wins). PGN saved at `6_manuscript/book_1/book1_chess_game.pgn`.

**8 studs locked** (everything else emergent):
1. Protagonist fakeout (Firas → Ahdia)
2. Ahdia and Firas's strained relationship (early)
3. Police ambush/trap (institutional power as threat)
4. Ahdia's fake death / powers reveal (source of others' abilities)
5. Bidirectional time manipulation discovery (speed up to self-administer treatment)
6. Firas gives Ahdia his suit (blink change, too big, still barefoot)
7. Autoinjector transfer + "Oh hey. I knew you were in there somewhere."
8. Firas dissolves into the singularity (human chain pulls Ahdia back)

**Full studs document:** `6_manuscript/book_1/BOOK1_REBUILD_STUDS.md`

**Book 2A:** Will be rebuilt after Book 1, using the embodiment instructions proven at book scale. Not simultaneous.

---

## What Happened This Session (2026-04-03)

### 1. Steward Experiment Manual Built
- `5_story_bibles/book_2b/steward_experiment/STEWARD_EXPERIMENT_MANUAL.md`
- Full user manual for the steward experiment system: core concepts, how to run it, evaluation pipeline, design principles
- Written so a fresh chat or human reader can understand the full system cold

### 2. Cross-Book Prose Audit
Ran 4-audit battery on both Book 1 and Book 2A manuscripts:

**Book 1 (74K words, 30 chapters):**
- Fragment punches: 1,023 total. **9x escalation** from early (3.3/1K) to late (29.5/1K)
- Not-constructions: 113 (concentrated in back half)
- "Still": 125 (spikes in final act)
- Em-dashes: 1.9/1K early → 10.4/1K late (5.5x, all POVs)
- "The particular": 0 (hadn't developed yet)
- POV voice: **Grade C**

**Book 2A (48K words, 23 chapters):**
- Not-constructions: 119
- "The particular [noun] of": 48 (across every POV — Book 2A's signature tic)
- "Still": 133 (2.8/1K)
- Fragments: 87 (much more controlled than Book 1)
- POV voice: **Grade C+** (dialogue B+/A-, narration C-/D+)

**Key finding:** The disease isn't specific tics — it's an **amplification mechanism**. The AI discovers a default early and reaches for it increasingly under pressure. Different books develop different mutations. Same mechanism.

**Root cause discovery:** Book 1's escalation maps to the literal boundary between the Director's original pre-AI prose (early chapters, clean) and AI-revised prose (later chapters, infected). The AI doesn't imitate the author's voice — it overwrites it.

### 3. Embodiment vs Description — Core Design Principle
- AI prose quality tracks to the **operation performed**, not the ratio of AI content
- **Embodiment** ("be this character") → natural voice. Remanence used this. Survived disclosure scrutiny.
- **Description** ("write about this character") → homogeneous narrator voice. Go Squad has this.
- The triplet mechanism bridges the gap: gives the AI a cognitive architecture to inhabit, not facts to report
- **Design problem document:** `PROSE_VOICE_DESIGN_PROBLEM.md`

### 4. The Missing Layer Identified
```
Character Bible       → WHO they are
Steward Prompt        → HOW they interpret events
[EMBODIMENT INSTRUCTIONS] → HOW the narrator sounds inside their head
Prose Output          → The actual sentences
```
The embodiment instruction must specify per character:
1. Cognitive architecture under different states
2. What the character does NOT do (negative constraints as firewall)
3. The repeatable operation (triplet equivalent for prose)
4. Grief/stress register
5. Structural resistances to accumulation

### 5. Book 1 Rebuild Decision
Director decided to rebuild from studs rather than retrofit. 8 canonical moments locked. Chess game selected (Carlsen-Nepo 2021 Game 6, 136 moves). Everything between studs is emergent.

---

## Files Created This Session
- `5_story_bibles/book_2b/steward_experiment/STEWARD_EXPERIMENT_MANUAL.md` — Steward experiment user manual
- `PROSE_VOICE_DESIGN_PROBLEM.md` — Embodiment vs description design problem
- `6_manuscript/book_1/book1_chess_game.pgn` — Carlsen-Nepo 2021 Game 6 PGN
- `6_manuscript/book_1/BOOK1_REBUILD_STUDS.md` — 8 locked studs for rebuild

## Files NOT Modified
- Existing topology files unchanged
- Existing manuscript files unchanged (rebuild is a fresh start, not edits)

---

## Still Pending (Unchanged from Previous Handoff)

### Book 2B 5-Agent Evaluation Pipeline
Not started. Full spec unchanged:
1. Timeline Keeper, Status Tracker, Theme Guardian, Reader Proxy, Pacing Monitor → against 13 steward outputs
2. Enforcer validation
3. Director-led cinematic blocking
4. 12 editorial issues pending Director decisions

**Note:** This pipeline should now run against the series topology once it exists, for cross-book validation.

### Topology Files Needed
| Book | File | Phase | Status |
|------|------|-------|--------|
| Book 1 | `BOOK1_TOPOLOGY.yaml` | 4 (complete) | Exists — architecture reference for rebuild |
| Book 2A | `BOOK2A_TOPOLOGY.yaml` | 4 (complete) | Exists |
| Book 2B | `BOOK2B_TOPOLOGY.yaml` | 2-3 | Exists |
| Book 4 | Not yet created | — | 40 planning files exist |
| Books 5-8 | Not yet created | — | Unknown |
| Series | Not yet created | — | **NEXT SESSION PRIORITY** |

---

## Beta Reader Status
- **Beta reader 1:** Finished Book 1. Flagged "first draft" feel. Praised emotional beats, trope subversion (protagonist fakeout specifically), action clarity.
- **Beta reader 2:** Has Book 1, hasn't started. Will read current version for story/architecture feedback — what lands, what characters work, what feels earned. Do NOT prime her with audit findings.

---

## Canon Warnings (Unchanged)

### Critical
- **Ahdia POV withheld in Book 2A** — revealed end of 2A when Ruth discovers Exile Island
- **28 dictators in prose, 37 in planning docs** — UNRESOLVED
- **Kain wins election** — 312 EV
- **Leta dies Book 2B** — killed by Webb
- **Prime = Ahdia-1** — 5 total iterations (NOT 43/47)
- **Firas does NOT die conventionally** — dissolves into singularity, absorbed, gone

### Character
- Victor has NO dead wife (partner is Leah)
- Bourn is a WOMAN (she/her)
- Korede is 17 (NOT 15)
- Eidolon AMPLIFIES fear (cannot create)
- Tess does NOT kill Webb
- Leah is a BARISTA

---

**End of Handoff**
