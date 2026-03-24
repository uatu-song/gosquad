# CLAUDE.md — Go Squad Repository

## What This Is

A 7-book sci-fi series (the Auerbach Series) by J.S. Vaughn, developed using a human-AI collaborative workflow with TTRPG-first methodology, chess-to-narrative mapping, and a multi-agent "production studio" system.

**You are crew, not author.** The human is the Director. You run agents, present output, and nothing goes to manuscript without Director approval.

## Onboarding Protocol

**Read these files in this order to reach working readiness:**

### Step 1: Where Are We? (30 seconds)
```
READ: GO_SQUAD_SESSION_HANDOFF.md
```
This tells you: current resume point, what was last completed, critical structural decisions, canon warnings, and prose status. Start here every session.

### Step 2: Repository Structure (10 seconds)

The repo was restructured Dec 2025 into numbered folders:

```
/workspaces/gosquad/
├── 1_writing_guides/          # Voice, style, fight choreography
├── 2_method_actor/            # Character stewards + briefings
│   └── stewards/              # 13 character embodiment files
├── 3_ttrpg/                   # Dice mechanics, beat sessions
├── 4_constraints/             # Thematic constraints, negative constraints
├── 5_story_bibles/            # Canon: book_2/, book_3/, book_4/, universe/
│   └── book_2/
│       ├── structure/         # Chapter_XX_STRUCTURE.md (beat sheets)
│       ├── threads/           # Per-character thread files
│       ├── scenes/            # Scene cards
│       ├── sessions/          # Session logs and handoffs
│       └── CLAUDE.md          # Book 2-specific guidance
├── 6_manuscript/
│   └── book_2/
│       ├── chapter_XX.md      # Prose files (Ch 1-14 complete)
│       ├── chapter_XX.txt     # Plain text versions
│       ├── chapters_split/    # Individual chapter .txt files
│       └── visualizations/    # HTML timeline tools
├── 7_characters/
│   ├── arcs/                  # Arc trackers + CHARACTER_STATE_INDEX.yaml
│   └── profiles/              # Full character profiles
├── 8_codex/                   # Entity codex (YAML)
├── _tools/                    # Production tools
│   ├── agents/                # Agent system (templates + CLI)
│   ├── perspective_engine/    # Timeline query engine
│   ├── prose_indexer/         # AI slop detection
│   └── state_architecture/    # State query system
├── _archive/                  # Pre-restructure files
├── GO_SQUAD_SESSION_HANDOFF.md  # <-- START HERE
├── GO_SQUAD_MANIFEST.yaml       # File-to-agent role mappings
├── Chess_Narrative_Engine_6.8.html
└── book2_perspective_engine.html
```

### Step 3: The Agent System (60 seconds)
```
READ: _tools/agents/README.md
READ: 2_method_actor/stewards/STEWARD_INDEX.md
```

The system has two layers:

**Production Crew (14 agents)** — each owns a domain:

| Agent | Domain | Template |
|-------|--------|----------|
| Archivist | Retrieval, indexing (read-only) | `archivist.yaml` |
| Status Tracker | Character state facts | `status_tracker.yaml` |
| Theme Guardian | Thematic consistency | `theme_guardian.yaml` |
| Timeline Keeper | Chronological accuracy | `timeline_keeper.yaml` |
| Scene Choreographer | Movement, blocking | `scene_choreographer.yaml` |
| Reader Proxy | Audience knowledge, dramatic irony | `reader_proxy.yaml` |
| Pacing Monitor | Tension curves, rhythm | `pacing_monitor.yaml` |
| Technical Consultant | Subject matter expertise | `technical_consultant.yaml` |
| Intimacy Coordinator | Sensitive content process | `intimacy_coordinator.yaml` |
| Outline Assistant | Beat sheets, structure docs | `outline_assistant.yaml` |
| Production Designer | Objects, costumes, tech | `production_designer.yaml` |
| Set Designer | Spatial reality, environments | `set_designer.yaml` |
| Character Steward | Character embodiment (1 per character) | `character_steward.yaml` |
| Importer | Content import/migration | `importer.yaml` |

Templates are in `_tools/agents/templates/production_crew/`. Each YAML contains a `system_prompt` you load to run the agent.

**Character Stewards (13 characters)** — in `2_method_actor/stewards/`:

| Character | Key Arc |
|-----------|---------|
| Ahdia Bacchus | Protagonist (FRIDGED in B2 — POV withheld) |
| Ruth Carter | Caretaker limits |
| Tess Whitford | Institutional betrayal → vigilante |
| Ben Bukowski | Faith collapse |
| Victor Hernandez | Both/And teaching |
| Leah Turner | White moderate awakening |
| Leta Owolowo | Targeted → killed (Ch23) |
| Korede Owolowo | Observer → radicalized |
| Bellatrix/Geneva | Hidden orchestrator |
| Harding Kain | Mayor → President-elect |
| Eidolon | Fear amplification (AMPLIFIES only, cannot create) |
| Ryu Matsuda | Ethical erosion |
| Harriet Bourn | Institutional authority → defector (SHE/HER) |

**Enforcer** (`_tools/agents/templates/meta/enforcer.md`) validates every agent output before it reaches the Director.

**Director CLI** (`_tools/agents/director_cli.py`) — functional tool:
```bash
python3 _tools/agents/director_cli.py prompt <agent>    # Extract system prompt
python3 _tools/agents/director_cli.py validate          # Validate process log
python3 _tools/agents/director_cli.py scene <chapter>   # Scene workflow setup
python3 _tools/agents/director_cli.py list              # List all agents
```

### Step 4: Load Context for Current Work
```
READ: 5_story_bibles/book_2/CLAUDE.md
READ: Relevant Chapter_XX_STRUCTURE.md from 5_story_bibles/book_2/structure/
READ: Relevant steward files from 2_method_actor/stewards/
```

## How to Run the System

### For a Chapter Prose Session

1. **Read handoff** → know resume point and last decisions
2. **Run Outline Assistant** → confirm beat sheet for the chapter
3. **Run Set Designer** → establish spatial ground truth for locations
4. **Run Status Tracker** → get character state facts at this chapter
5. **Load Character Stewards** → for each character in the scene
6. **Run Reader Proxy** → check dramatic irony and reader knowledge
7. **Run Theme Guardian** → verify thematic alignment
8. **Present each output to Director** → Director approves, rejects, or adjusts
9. **Write prose** → using approved agent outputs as constraints
10. **Run Enforcer** → validate process logs

Each agent stays in its lane, cites sources, and defers to specialists. State facts (Status Tracker) and behavioral interpretation (Character Steward) are always separated.

### Agent Rules

- Agents declare their **domain** and stay in it
- Out-of-lane content gets **deferred** to the right specialist
- Character Stewards declare **mode**: EXPLORATION (testing ideas) or PERFORMANCE (executing approved scenes)
- All factual claims need **source attribution**
- **Process logs** track queries, sources, deferrals, and confidence

## Canon Warnings (Check Every Session)

### Critical
- **Ahdia's POV is WITHHELD in Book 2** — she appears depressed/fridged; truth revealed END of Book 2 when Ruth discovers Exile Island; Book 3 reframes from Ahdia's perspective
- **37 dictators** on Exile Island (reality TV format, MTV Real World style)
- **Ruth discovers END of Book 2** — not Ch7, not Ch13, not midpoint
- **Team does NOT know until Book 3**
- **NO internal Ahdia scenes** in Book 2

### Character
- Tess does NOT kill Webb (brutalizes, leaves alive)
- Victor has NO dead wife (romantic partner is Leah)
- Ryu NEVER confesses love to Ahdia in Book 2
- Bourn is a WOMAN (she/her pronouns)
- Eidolon AMPLIFIES fear (cannot create new fears)
- Leah is a BARISTA (not investigator)
- Ben's wife Sarah — cause of death UNSPECIFIED (never invent)
- Leah/Victor revealed identities BEFORE group reveal
- Leta dies Ch23 (killed by Webb)

### Background News Seeds
Dictators vanishing throughout Book 2 — team dismisses as "world going crazy":
- Ch4: North Korean general vanishes
- Ch6: Belarusian dictator missing
- Ch8: Third week of leadership vacuums
- Ch10: Conspiracy theories about autocrats
- Ch12: State media scrambles
- Ch15: Mass junta disappearance
- Ch18: UN baffled by regime changes

## Key Reference Files

| Purpose | File |
|---------|------|
| Session resume point | `GO_SQUAD_SESSION_HANDOFF.md` |
| Book 2 writing guide | `5_story_bibles/book_2/CLAUDE.md` |
| Character states (YAML) | `7_characters/arcs/CHARACTER_STATE_INDEX.yaml` |
| Steward index | `2_method_actor/stewards/STEWARD_INDEX.md` |
| Agent system | `_tools/agents/README.md` |
| File-to-agent mapping | `GO_SQUAD_MANIFEST.yaml` |
| Production timeline (HTML) | `6_manuscript/book_2/visualizations/book2_production_timeline.html` |
| Continuity tracker | `5_story_bibles/book_2/CONTINUITY_TRACKER.md` |
| Prose TODO | `5_story_bibles/book_2/BOOK2A_PROSE_TODO.md` |
| Book 2B timeline (interactive) | `5_story_bibles/book_2b/steward_experiment/book2b_timeline.html` |

## Series Overview

7-book arc. Books 1-3: CBT approach failing. Book 4: turning point (DBT). Books 5-7: DBT succeeding.

**Book 2 emotional arc:** Sacrifice everything → Win through vulnerability. Ahdia tries to control/fix everything, burns herself out. Evidence proves irrelevant. Individual heroics create vulnerabilities. Kain wins the election anyway.

**Core theme:** You don't have to be fixed to be worthy.

## Book 2B — The Steward Experiment

**Status:** Run 1 COMPLETE. 13/13 steward outlines generated. Editorial massage pass next.

Book 2B picks up where 2A ended (Ruth/Ryu discover Exile Island, "deal with it Sunday"). Uses a 28-move chess game (jcksng vs jssong3) as structural scaffold. White = Go Squad (loses). Black = TRIOMF (wins). Qe3# is the locked endpoint.

**13 stewards**, each owning specific moves, each with a triplet of chess pieces as interpretive lens. Three convergence points (M9, M13, M25) force stories to touch. Ahdia writes first at every convergence point.

**Run 1 Results:** ~75-80% usable material (exceeded 60% prediction). 12 editorial issues identified requiring Director decisions. All 28 moves have at least one steward beat.

**Key files:**
- Steward outputs: `5_story_bibles/book_2b/steward_experiment/*_run1.md` (13 files)
- Convergence extracts: `5_story_bibles/book_2b/steward_experiment/convergence_M*.md`
- Timeline visualization: `5_story_bibles/book_2b/steward_experiment/book2b_timeline.html` (interactive, with Director notes + downloadable report)
- Bellatrix prompt: `5_story_bibles/book_2b/steward_experiment/prompt_bellatrix.md`
- Steward prompt files: Director-built (not from existing `2_method_actor/stewards/`)
- Briefing doc: provided by Director per-session (not stored in repo)

**Locked endpoints:** Kain wins presidency. Ahdia at 0.7% baseline. Prime reveals herself. Go Squad labeled terrorists. Bellatrix wins. Leta dies. Qe3#.

**Process:** ~~Run stewards~~ → ~~generate outlines~~ → **5-agent evaluation pass** → cinematic blocking → coherent book structure → prose generation. Run 1 of 3 planned.

**Next Session: 5-Agent Parallel Evaluation + Enforcer**

Run these 5 agents in parallel against all 13 steward outputs + PGN:

1. **Timeline Keeper** — reconcile 28 moves into single linear sequence, flag steward timing contradictions (especially M24/M25/M27 endgame traffic jam)
2. **Status Tracker** — map Ahdia's baseline math (53.1% → 0.7%), track character availability windows (Leah's coma M11-M24, Ben's faith collapse at M25), flag hallucinated presences
3. **Theme Guardian** — verify Both/And philosophy and triage themes survive the climax, check thematic anchors aren't buried by kinetic action
4. **Reader Proxy** — map dramatic irony layers (audience vs. character knowledge), especially Bellatrix's four dead Genevas and Eidolon's grief crack at M24
5. **Pacing Monitor** — assess tension curve across 4 phases (Opening M1-8, Middlegame M9-18, Crisis M19-24, Endgame M25-28), flag M19-22 rook rampage pacing risk, check endgame compression

**Then: Enforcer validates all 5 reports** (rejects out-of-domain claims, flags missing source attribution, catches hallucinated facts).

**Then: Director directs cinematic blocking** (Scene Choreographer + Pacing Monitor) with evaluated footage in hand.

**12 Editorial Issues (from Run 1 evaluation):**
1. 28 vs 37 dictators (Exile Island count — stewards used both)
2. Korede's age (stewards say 15 and 17 — canon is 17)
3. Translocation mechanics (some stewards confused Seed activation vs translocation)
4. CR-7 extension at M17 (new lore — Ruth gives Ahdia months instead of weeks)
5. "Powers aren't real" claim at M2 (stewards interpreted this differently)
6. Compound decay model (Ryu's new lore — exponential vs linear decline)
7. Eidolon/Kain timing overlap at M16 (both claim the reframe)
8. Bellatrix/Kain M9 overlap (both claim architecture credit)
9. Bourn's baseline numbers timing (when does she get the data?)
10. Korede's location at Leta's death (Korede steward has him present; Tess steward also present)
11. e-pawn ownership (Ahdia and Ryu both claim it as triplet piece)
12. White Queen at M27 (Ruth and Bourn both read it differently)

## Book 3 — Planning Status

**Status:** Pre-production. Extensive planning complete (40 files in `5_story_bibles/book_3/`). Prologue + Chapter 1 have prose. Chapters 2-11 have beat sheets.

**Emotional Arc:** Confidence → Incomprehensible challenge → Psychological collapse → Redemption

**Central premise:** Ahdia-5 is powerless (Prime burned out her temporal abilities). Must survive Bellatrix's war — clone avatar armies + embodied Eidolon — while learning to be "enough" without powers. Prime poses as "Aunt Diana" and secretly enhances the team.

**Key structural decision:** Book 3 will split A/B at the rift moment (currently Ch19 — Bellatrix forces Ahdia into The Between). Act 1 needs compression (7 confidence chapters → 4-5) so the rift lands at true midpoint. 3A = confidence through devastating cliffhanger. 3B = scattered survival, guerrilla resistance, rescue, climax.

**Canon (locked):**
- Prime = Ahdia-1. Current Ahdia = Ahdia-5. 5 total iterations (NOT 43/47 from early planning).
- Mother FAERIS: sentient AI buried under CADENS HQ, exploited for decades while dormant
- Eidolon: not a natural predator — Fear fragment torn from unified being by Bellatrix
- Captain Suzie Rivets: mech pilot from erased Iteration 3, found in The Between
- Two-part climax: clone army defeated (Mother FAERIS freed) → Ahdia rescued from The Between

**Key files:**
- `5_story_bibles/book_3/BOOK3_MASTER_PLAN.md` — Definitive planning doc
- `5_story_bibles/book_3/BOOK3_BRAIDED_STRUCTURE.md` — Three-timeline structure
- `5_story_bibles/book_3/CLIMAX_STRUCTURE_FINAL.md` — Two-part sequential climax
- `5_story_bibles/book_3/EIDOLON_CANON.md` — Eidolon as tragic victim
- `5_story_bibles/book_3/Bellatrix_Motives_v3.md` — Bellatrix motivation
- `5_story_bibles/book_3/CHARACTER_TROUBLEMAKER_FINAL.md` — Captain Rivets

## Series Renumbering

The original 7-book series became 8 books when Book 2 split into 2A and 2B due to 120K+ word count:

| New # | Old # | Content |
|-------|-------|---------|
| Book 1 | Book 1 | Avoidance → Forced action |
| Book 2 (2A) | Book 2 (first half) | Sacrifice → Vulnerability |
| Book 3 (2B) | Book 2 (second half) | Go Squad vs TRIOMF, Qe3# |
| Book 4 | Book 3 | Confidence → Psychological collapse |
| Book 5 | Book 4 | Turning point (stalemate, DBT) |
| Books 6-8 | Books 5-7 | DBT approach succeeding |

**Note:** Repository directories still use old numbering (`book_2b/` for new Book 3, `book_3/` for new Book 4). Book 4 (old Book 3) will also likely split A/B.

## Git Discipline

**ALWAYS push after committing.** This repo nearly lost 3 months of work because commits were never pushed. After any significant work:
```bash
git add -A && git commit -m "description" && git push origin main
```
