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

## Series Overview

7-book arc. Books 1-3: CBT approach failing. Book 4: turning point (DBT). Books 5-7: DBT succeeding.

**Book 2 emotional arc:** Sacrifice everything → Win through vulnerability. Ahdia tries to control/fix everything, burns herself out. Evidence proves irrelevant. Individual heroics create vulnerabilities. Kain wins the election anyway.

**Core theme:** You don't have to be fixed to be worthy.

## Git Discipline

**ALWAYS push after committing.** This repo nearly lost 3 months of work because commits were never pushed. After any significant work:
```bash
git add -A && git commit -m "description" && git push origin main
```
