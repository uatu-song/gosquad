# The Steward Experiment — User Manual

**What:** A decentralized AI-driven outline generation system where 13 character-embodying agents independently plot their arcs across a chess game scaffold, producing raw narrative "footage" that a human Director then assembles into a book.

**Why:** Traditional plotting asks "what happens next?" The Steward Experiment asks "what does this moment mean to *this character*?" — 13 times, simultaneously. The contradictions between perspectives are the creative material.

**Where:** `5_story_bibles/book_2b/steward_experiment/`

---

## Core Concepts

### The Chess Scaffold

A real chess game (jcksng vs jssong3, Scandinavian Defense, 28 moves, 0-1) provides the structural skeleton. Each move in the game maps to a narrative beat. The game's outcome is locked: **White (Go Squad) loses. Black (TRIOMF) wins. Qe3# is checkmate.**

The chess game is not a metaphor being forced onto narrative — it's a neutral external structure that doesn't care about the characters. Its shape (opening, middlegame, crisis, endgame) naturally maps to narrative structure, and its evaluation swings map to tension.

**Game phases:**
| Phase | Moves | Narrative |
|-------|-------|-----------|
| Opening | M1–M8 | Sunday confrontation → team fractures |
| Middlegame | M9–M18 | Overreach → evidence gets inverted |
| Crisis | M19–M24 | Rook rampage → Eidolon cracks |
| Endgame | M25–M28 | Election Night → Checkmate |

### Stewards

Each of the 13 major characters has a **steward** — an AI agent prompted to embody that character's perspective, voice, and worldview. A steward doesn't write prose. It generates **outline beats**: what this character does, feels, and means at each move they own.

Stewards are split by faction:
- **White (Go Squad, losing side):** Ahdia, Ruth, Tess, Ben, Ryu, Victor, Leah, Korede/Leta, Bourn
- **Black (TRIOMF, winning side):** Bellatrix, Kain, Eidolon
- **Unaligned:** Prime (reveals herself at the end)

### The Triplet Lens

Each steward is assigned **3 chess pieces** as an interpretive lens. These aren't arbitrary — they're chosen to reflect the character's arc and role. The steward reads every move through their three pieces and extracts narrative meaning.

**Example — Bellatrix's triplet:**
- **Black Queen** — Bellatrix herself. Sits idle for most of the game, then explodes in four devastating moves (Qd7, Qh3+, Qxf3, Qe3#). Patience measured in billions of years, then precision.
- **Black dark-square Bishop** — The Genevas. Moves constantly, probes, sacrifices itself. Four bishops sacrificed = four Genevas who died and uploaded back to Bellatrix.
- **Black Knight (g8)** — The infiltrator. Kain, artifacts, proxy work. Positioned deep behind enemy lines before the queen delivers checkmate.

The triplet creates **divergence by design**. The same chess move means completely different things to different stewards because they're reading it through different pieces. Victor's Bc1 (blocked bishop = trapped teacher) vs Leah's Bc1 (the life she was trying to escape) vs Bourn's Bc1 (imprisoned by her own bureaucracy).

### Convergence Points

Three moves are designated **convergence points** where multiple storylines must touch:

| Move | Title | Stewards |
|------|-------|----------|
| M9 | THE OVERREACH | Ahdia, Ruth, Victor (White) + Kain, Bellatrix (Black) |
| M13 | THE WRONG DIRECTION | Ahdia, Ryu, Korede/Leta (White) + Bellatrix (Black) |
| M25 | THE MATING NET BEGINS | Ahdia, Tess, Ben (White) + Bellatrix, Kain (Black) |

**Ahdia writes first** at every convergence point. Her output is extracted into a standalone file and provided to other stewards writing the same moment. They must read it — but not conform to it. The goal is genuine tension between perspectives, not diplomatic agreement.

### Move Ownership

Each steward owns specific moves. They only write beats for moves they own. Some moves have multiple stewards (especially convergence points). Some stewards own many moves (Ahdia: 7), some own few (Bourn: 1, Victor: 2, Leah: 2).

Low-move stewards aren't lesser — constraint produces compression. Run 1 showed that the stewards with fewest moves produced the most emotionally concentrated material.

---

## How to Run a Steward Experiment

### Prerequisites

- A chess game selected as scaffold (PGN notation)
- Move-to-metaphor mapping (what each move represents narratively at a high level)
- Character-to-faction assignments (which side each character is on)
- Triplet assignments (3 chess pieces per steward)
- Move ownership assignments (which steward writes which moves)
- Convergence point designations
- Canon constraints and locked endpoints
- A shared preamble document

### Step 1: Build the Shared Preamble

Every steward terminal receives the same foundational material:

1. **The PGN** — full game notation with evaluation scores per move
2. **Move metaphor table** — one-line narrative interpretation of each move (e.g., "M9: f4?! exf4 — Overreach punished immediately")
3. **Three rules:**
   - Your triplet is your lens. Read every move through your three pieces.
   - You own your moves. Only write beats for moves assigned to you.
   - At convergence points, read Ahdia's output first. Do not conform. Write genuine tension.
4. **Convergence protocol** — which moves are convergence points, who shares them, where to find Ahdia's output
5. **Locked endpoints** — non-negotiable outcomes the story must reach

### Step 2: Build Individual Steward Prompts

Each steward prompt contains (in this order):

1. **Identity** — who the character is, their emotional core, their worldview
2. **Faction** — White or Black, what it means for them to be on the winning or losing side
3. **Triplet** — their 3 chess pieces, what each piece represents for this character, and how the pieces relate to each other
4. **Move list** — which moves they own, with convergence points marked
5. **Convergence protocol** — where to find Ahdia's output at convergence points
6. **Starting state** — what this character knows at the top of Book 2B
7. **Emotional core** — the deep thematic engine driving this character
8. **Output format** — beats, not prose. Chess reading + narrative meaning.

See `prompt_bellatrix.md` for a complete example.

The Director builds these prompts. They are **not** the same as the character steward files in `2_method_actor/stewards/` — those are for prose-level embodiment. Experiment prompts are custom-built for chess-scaffolded outline generation.

### Step 3: Run Ahdia First

Ahdia is the **convergence anchor**. Run her steward first. She writes beats for all her moves, including convergence points M9, M13, and M25.

Extract her convergence outputs into standalone files:
- `convergence_M9_ahdia.md`
- `convergence_M13_ahdia.md`
- `convergence_M25_ahdia.md`

These get fed to other stewards who share those convergence points.

### Step 4: Run All Other Stewards in Parallel

Each steward runs in its own terminal/session. They receive:

1. The shared preamble
2. Their character-specific prompt
3. Ahdia's convergence output files (if they share a convergence point)

They do not see each other's output. They work independently. This is by design — divergence is the goal.

**VS Code shortcut:** The task file (`.vscode/tasks.json`) has a "Launch All Steward Terminals" task that opens 13 named terminal tabs simultaneously.

### Step 5: Collect and Evaluate

Once all stewards complete their runs, collect the output files. Each is named `{character}_run1.md`.

**What to look for:**
- **Usable beats** — moments that feel true to the character and advance the narrative
- **Editorial issues** — contradictions between stewards (ages, mechanics, timeline overlaps, ownership claims)
- **Standout beats** — moments that surprise you, that are better than what you would have written alone
- **Canon violations** — stewards inventing facts that contradict established canon
- **Triplet divergence** — are different stewards genuinely reading the same moves differently, or converging on similar interpretations?

### Step 6: Visualize and Annotate

Build or use an interactive timeline (like `book2b_timeline.html`) that displays all beats in chronological move order, color-coded by faction. This reveals:

- Timing overlaps (two characters claiming the same moment)
- Gaps (moves with no beats)
- Pacing problems (too many beats crammed into the endgame)
- Choreography needs (who is physically where during shared moments)

The Director adds notes per move. These notes persist (localStorage) and can be exported as a downloadable `.md` report to feed into the next session.

---

## After the Run: The Evaluation Pipeline

Steward output is **raw footage, not a script**. It requires evaluation before it becomes a book outline.

### 5-Agent Parallel Evaluation

Run these production crew agents against all steward outputs:

| Agent | Evaluates | Key Questions |
|-------|-----------|---------------|
| **Timeline Keeper** | Chronological coherence | Do 28 moves form a single linear sequence? Where do stewards contradict on timing? |
| **Status Tracker** | Character state facts | Is the baseline math correct? Are characters available where stewards place them? |
| **Theme Guardian** | Thematic integrity | Do the core themes survive the climax, or get buried by action? |
| **Reader Proxy** | Dramatic irony | What does the audience know vs. characters? Are irony layers tracked correctly? |
| **Pacing Monitor** | Tension curve | Does the 4-phase structure (opening, middlegame, crisis, endgame) have correct rhythm? |

### Enforcer Validation

The Enforcer (`_tools/agents/templates/meta/enforcer.md`) validates all 5 reports:
- Rejects out-of-domain claims (e.g., Timeline Keeper making thematic judgments)
- Flags missing source attribution
- Catches hallucinated facts
- No report reaches the Director without Enforcer sign-off

### Director-Led Cinematic Blocking

With evaluated footage in hand, the Director instructs Scene Choreographer + Pacing Monitor on:
- Which beats play simultaneously vs. sequentially
- Where POV shifts occur
- How convergence points choreograph across characters
- Intercutting rhythm between storylines

### Editorial Resolution

Resolve contradictions between stewards. These are creative decisions, not errors — each represents a fork where the Director chooses which steward's interpretation becomes canon.

---

## Multiple Runs

The experiment is designed for multiple runs with **different triplet variants**. Giving stewards different chess pieces as their lens produces genuinely different readings of the same moments. Run 1 establishes the baseline. Runs 2–3 explore alternative interpretations.

What stays constant across runs:
- The chess game (PGN)
- Move ownership
- Convergence points and protocol
- Canon constraints and locked endpoints
- Character identities and factions

What changes:
- Triplet assignments (different 3-piece combinations)
- Potentially the move metaphor table (refined based on previous run insights)

---

## Results from Run 1

**Prediction:** ~60% usable material.
**Actual:** ~75-80% usable.

### What Worked

- **Triplet lens produced genuine divergence.** Same moves read completely differently through different pieces.
- **Convergence points produced tension, not diplomacy.** Multiple genuine perspectives on the same catastrophe.
- **Antagonist stewards outperformed.** Writing from a position of strength gave permission for clarity. Bellatrix, Kain, and Eidolon's outputs were among the strongest.
- **Low-move stewards produced concentrated material.** Constraint = compression = power. Victor (2 moves) and Leah (2 moves) delivered the most emotionally potent beats. Bourn wrote a complete arc in one move.
- **The chess game's actual shape matters.** The +8.83 evaluation at M25 followed by d7?? Qe3# (overreach instead of consolidation) mapped perfectly to the book's theme.

### 12 Editorial Issues Identified

Contradictions between stewards that require Director decisions. Not errors — creative forks. See `SESSION_LOG_2026-03-10_run1.md` for full list.

### Standout Beats

- **Eidolon M24 — THE FIRST CRACK:** Three-phase structure ending with grief Eidolon can't metabolize.
- **Ben M25 — GEOMETRY, NOT FAITH:** The Marine defaults to spatial awareness when faith collapses.
- **Victor M23 — THE CHECK THAT DIDN'T MATTER:** Scope shrinks from community to one hand.
- **Bourn M15 — NOT THE QUEEN:** Complete arc in one move. "Fair exchanges don't win games."
- **Korede/Leta M26 — THE CLOSED LAPTOP:** Documentation outlives both pawns.
- **Bellatrix M27 — THE REMOVAL:** "You do not push the mountain down. You wait for the mountain to become sand."

---

## File Reference

| File | Purpose |
|------|---------|
| `prompt_bellatrix.md` | Example steward prompt (only one committed to repo) |
| `convergence_M9_ahdia.md` | Ahdia's M9 convergence output |
| `convergence_M13_ahdia.md` | Ahdia's M13 convergence output |
| `convergence_M13_ryu.md` | Ryu's M13 convergence output |
| `convergence_M25_ahdia.md` | Ahdia's M25 convergence output |
| `{character}_run1.md` | 13 steward output files from Run 1 |
| `book2b_timeline.html` | Interactive timeline with Director notes + download |
| `SESSION_LOG_2026-03-10_run1.md` | Complete session log for Run 1 |
| `BOOK2B_TOPOLOGY.yaml` | Topology file built from Run 1 outputs |
| `.vscode/tasks.json` | VS Code task to launch all 13 steward terminals |

---

## Design Principles

1. **Character-first, not plot-first.** "What would I do?" beats "What should happen?"
2. **Constraint produces creativity.** Locked endings, assigned moves, and triplet lenses force stewards to be inventive within walls.
3. **Divergence by design.** Stewards don't see each other's work. Contradictions are features, not bugs.
4. **Generation and evaluation are separate phases.** Stewards generate freely. Production crew agents evaluate rigorously. Mixing the two kills both.
5. **The Director is the author.** The system produces footage. The human assembles the film. Nothing reaches manuscript without Director approval.
6. **The chess game is neutral scaffolding.** It provides structure without prescribing content. The same move means different things to different characters — that's the point.
