# Go Squad Planning Workflow

**Purpose:** Document the Director-led planning process for developing story beats into production-ready scene cards.

**Principle:** The Director leads. Agents serve. Vision comes from human creativity; agents validate, explore, and maintain consistency.

---

## What Exists for Book 2

| Asset | Location | Status |
|-------|----------|--------|
| 24-chapter beat structure | `5_story_bibles/book_2/Chapter_*_STRUCTURE.md` | Complete |
| CHARACTER_STATE_INDEX.yaml | `7_characters/arcs/` | Partial chapter_states |
| Thread tracking | `5_story_bibles/book_2/threads/` | 9 thread files |
| Canon warnings | CHARACTER_STATE_INDEX.yaml | Active |
| Character Stewards | `2_method_actor/stewards/` | 12 stewards ready |

---

## What Planning Work Requires

1. Fill plot holes
2. Test if character motivations hold
3. Ensure continuity across threads
4. Break beats into granular moments
5. Discover scenes through exploration

---

## The Six-Phase Workflow

### Phase 1: Director Reviews Structure

**Who:** Director (Joe) only - no agents

**Purpose:** Establish vision, identify gaps

**Process:**
1. Read existing beat structure for target chapter(s)
2. Identify:
   - What feels solid
   - What feels thin or uncertain
   - Where you have questions about character choices
   - Plot holes or logical gaps
3. Make notes on what needs exploration

**Output:** List of questions and uncertainties to explore

---

### Phase 2: Character Steward Consultations

**Who:** Director + individual Character Stewards

**Purpose:** Test if beats hold from character perspective

**Process:**
1. Load relevant Character Steward
2. Set mode: **EXPLORATION**
3. Ask directly in scene context:
   - "In Chapter X, you do Y. Walk me through what's happening internally."
4. Steward responds in character voice with process log
5. Interrogate further:
   - "What if Z happened instead? Would that change anything?"
   - "What are you afraid of in this moment?"
   - "What do you want that you're not saying?"
6. Steward advocates for the character

**Example:**
```
Director: "In Chapter 12, you confront your father. The beat says
you sever the relationship. Walk me through what's happening internally."

Tess Steward (Exploration): "I've known he was corrupt for years.
That's why I became Gloom Girl. But knowing and PROVING are different.
Standing in his office with the evidence in my hand... I'm not hoping
he'll deny it. I'm hoping he'll explain. That there's something I
missed. Some reason that makes it not what it looks like.

There isn't. There never was.

The severance isn't the moment I learn the truth. It's the moment
I stop hoping for a different truth."

[Process Log: Source - Tess_Whitford_Steward.md, canon_warning:
tess_already_knows_corruption, mode: exploration]
```

**Output:** Validated or revised understanding of character motivation

---

### Phase 3: Multi-Character Scene Exploration

**Who:** Director + multiple Character Stewards (sequentially)

**Purpose:** Discover scene dynamics through collision

**Process:**
1. Identify scene with multiple key characters
2. Load each relevant Steward sequentially
3. Give each the same scene setup
4. Ask each:
   - "What do you want in this scene?"
   - "What are you afraid of?"
   - "What are you hiding?"
5. Look for natural conflict/alignment
6. Discover dynamics you didn't plan

**Example: Chapter 13 - Exile Island Exposed**

Load Ahdia, Ruth, Ben, Tess sequentially:

| Character | Question | Discovery |
|-----------|----------|-----------|
| Ahdia | "How do you defend yourself?" | Defensive, statistics-focused, guilty |
| Ruth | "How do you react to betrayal?" | Hurt but not surprised - saw signs |
| Ben | "Does this change faith in team?" | Shaken - if Ahdia lied, who else? |
| Tess | "Does this mirror your father?" | Recognition - secrets to "protect" others |

**Output:** Scene dynamics emerge from character collisions, not top-down plotting

---

### Phase 4: Production Crew Validation

**Who:** Director + specialist agents

**Purpose:** Check work against system constraints

**Process:**
Once exploration complete and direction chosen, consult:

| Agent | Question |
|-------|----------|
| **Status Tracker** | "What state changes happen in this scene?" |
| **Timeline Keeper** | "Does this fit the chronology?" |
| **Theme Guardian** | "Does this serve the CBT-failing arc?" |
| **Reader Proxy** | "What does audience know vs. characters?" |

They flag problems. Ensure consistency. Don't make creative decisions.

**Output:** Validation or flags for revision

---

### Phase 5: Granular Beat Breakdown

**Who:** Director

**Purpose:** Break chapter beats into "shots"

**Process:**
Take a chapter beat and decompose into granular moments:

**Before:**
```
Chapter 12 beat: "Tess confronts father"
```

**After:**
```
12.1: Tess arrives at father's office
12.2: Surface conversation - pretending normal
12.3: Tess presents evidence
12.4: Father's deflection/justification
12.5: Tess's response (what?)
12.6: The break - what words?
12.7: Exit - how does she leave?
```

Each sub-beat is a "shot" when prose is generated.

**Output:** Numbered sub-beats ready for scene cards

---

### Phase 6: Scene Cards

**Who:** Director

**Purpose:** Create production-ready "scripts" for prose generation

**Format:**
```yaml
scene: 12.3
title: "Tess presents evidence"
characters: [tess, chief_whitford]
location: chief_whitford_office
tess_wants: "Confession, explanation, anything"
whitford_wants: "Make this go away"
conflict: "Truth vs. protection"
state_changes:
  - tess.relationship.father: "suspicious → confirmed betrayal"
emotional_register: "Controlled anger, desperate hope underneath"
seeds_to_plant: []
constraints:
  - "Tess ALREADY knows he's corrupt - discovering scope, not base fact"
```

**Output:** Scene cards ready for Method Actor prose generation

---

## Example Planning Session

```
DIRECTOR: "I'm uncertain about Chapter 8. Ben's case is complete
but I don't know how he feels about it. Let me talk to Ben."

[Load Ben_Bukowski_Steward.md]
[Set mode: EXPLORATION]

DIRECTOR: "Ben, you've just compiled airtight evidence against Kain.
Walk me through where you are emotionally."

BEN STEWARD: "Six months of work. Every document verified. Every
source triple-checked. I've got offshore accounts, falsified safety
reports, a body count. Everything documented, everything verifiable.

And I feel... good. Cautiously good.

The system works when you give it good evidence. That's what I've
always believed. I'm about to prove it."

[Process Log: Source - Ben_Bukowski_Steward.md, emotional_stage:
methodical_faith (ch1-8), mode: exploration]

DIRECTOR: "Do you actually believe the system will act on this?"

BEN STEWARD: "I have to. If evidence this airtight doesn't matter...
then what does? What have I been building my whole career on?

No. The evidence matters. The system will act."

[Process Log: This is setup for ch17 collapse - "What am I conserving?"]

DIRECTOR: "Good. That's the setup for Chapter 17's devastation.
Note for Status Tracker: Ben's belief state at Chapter 8 is
'confident in institutions.'"
```

---

## The Director's Role

| Responsibility | Description |
|----------------|-------------|
| **Choose** | Which agents to consult |
| **Ask** | The questions that drive exploration |
| **Decide** | Accept or reject agent contributions |
| **Approve** | Final call on all creative choices |
| **Maintain** | The vision across all sessions |

**The agents serve. They don't lead.**

---

## When to Use Each Phase

| Situation | Phases to Use |
|-----------|---------------|
| "I don't understand this character's choice" | Phase 2 (Steward consultation) |
| "This scene feels flat" | Phase 3 (Multi-character exploration) |
| "Does this break continuity?" | Phase 4 (Production Crew validation) |
| "This beat is too vague to write" | Phase 5 (Granular breakdown) |
| "Ready to generate prose" | Phase 6 (Scene cards) |

---

## Integration with Existing Tools

| Tool | Use In Workflow |
|------|-----------------|
| Character Stewards | Phases 2-3 (exploration) |
| CHARACTER_STATE_INDEX.yaml | Phase 4 (validation), Phase 6 (state_changes) |
| Thread files | Phase 4 (continuity checking) |
| Canon warnings | All phases (constraint enforcement) |
| Method Actor System | After Phase 6 (prose generation) |

---

## Output Chain

```
Phase 1 (Review)
    → Questions/uncertainties

Phase 2-3 (Exploration)
    → Validated motivations, discovered dynamics

Phase 4 (Validation)
    → Continuity-checked direction

Phase 5 (Breakdown)
    → Granular sub-beats

Phase 6 (Scene Cards)
    → Production-ready scripts

Method Actor System
    → Prose
```

---

*Go Squad Planning Workflow v1.0 — January 2026*
