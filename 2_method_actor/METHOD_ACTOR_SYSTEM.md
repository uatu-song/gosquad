# The Method Actor System
## A Framework for LLM-Assisted Long-Form Fiction

**Version:** 1.0
**Purpose:** Enable LLMs to generate consistent, voice-accurate prose for novels and series without hallucinating details, losing continuity, or violating established canon.

---

## Table of Contents

1. [Overview](#overview)
2. [The Core Problem](#the-core-problem)
3. [System Architecture](#system-architecture)
4. [Component 1: Entity Catalog](#component-1-entity-catalog)
5. [Component 2: Negative Constraints](#component-2-negative-constraints)
6. [Component 3: Session Manifests](#component-3-session-manifests)
7. [Component 4: Character State Index](#component-4-character-state-index)
8. [Component 5: Method Actor Prose Generation](#component-5-method-actor-prose-generation)
9. [Component 6: TTRPG Dice Mechanics (Optional)](#component-6-ttrpg-dice-mechanics-optional)
10. [Component 7: Evaluator](#component-7-evaluator)
11. [Workflow](#workflow)
12. [Templates](#templates)
13. [Lessons Learned](#lessons-learned)

---

## Overview

The Method Actor System is a structured approach to using LLMs for long-form fiction. It solves three fundamental problems:

1. **LLMs have bounded context** — You can't load an entire story bible every session
2. **LLMs are stateless** — Nothing persists between sessions
3. **LLMs fill gaps by inventing** — These inventions can contradict established canon

The system works by:
- Loading **targeted context** for each session (not everything)
- Tracking **what is NOT true** (negative constraints prevent invention)
- Validating output **before it becomes canon** (Evaluator catches errors)
- Having the LLM **perform characters sequentially** (Method Actor format)

---

## The Core Problem

### The Failure Mode Without This System

```
Session 1: LLM writes "Marcus thought of his late wife Elena"
           (Invented detail — Marcus was never married)

Session 2: Arc tracker updated with Elena reference
           (Invention becomes documented)

Session 3: Elena treated as canon, referenced again
           (Error propagates)

Session 4: "Elena" is now "real" in the narrative
           (Error is entrenched)
```

### Why Positive Documentation Fails

Simply stating "Marcus has a girlfriend named Sara" doesn't prevent the LLM from inventing "Marcus's late wife Elena." Positive statements don't exclude negative inventions.

### Why Negative Constraints Work

Stating "Marcus is NOT married, has NO wife, has NEVER been married" **does** prevent that error. The LLM sees the explicit prohibition.

**Key insight:** You can't prevent LLMs from inventing. You can only catch inventions before they become canon.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 PERSISTENT CONTEXT REPOSITORY               │
│  Entity Catalog / Negative Constraints / Session Documents  │
└─────────────────────────────────────────────────────────────┘
         │                    ▲                    │
         ▼                    │                    ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│    CONTEXT      │   │    CONTEXT      │   │    CONTEXT      │
│  CONSTRUCTOR    │──▶│    UPDATER      │──▶│   EVALUATOR     │
│   (Manifest)    │   │   (Session)     │   │  (Validation)   │
└─────────────────┘   └─────────────────┘   └─────────────────┘
         │                                           │
         ▼                                           ▼
    Load targeted                              Gate output
    constraints for                            before it
    this session                               becomes canon
```

---

## Component 1: Entity Catalog

A machine-readable YAML file containing all canonical story elements.

### What It Contains

- Characters (with IDs, demographics, relationships, forbidden associations)
- Organizations
- Relationships (with progression across chapters/timeline)
- Knowledge tracking (who knows what, when)
- Events (with timeline placement)
- Forbidden entities (things that must never appear)

### Example Structure

```yaml
meta:
  version: "1.0"
  series: "Your Series Name"
  current_book: 1
  last_updated: "2025-01-15"

characters:
  CHAR_001:
    canonical_name: "Alex Chen"
    aliases: ["Alex", "A.C.", "Dr. Chen"]

    demographics:
      gender: "woman"
      pronouns: ["she", "her", "hers"]
      age: 32

    relationships:
      partner: "CHAR_004"  # Jordan
      employer: "ORG_001"

    arc:
      book1_summary: "Isolation -> Trust -> Betrayal -> Resilience"
      start_state: "isolated_defensive"
      end_state: "cautiously_connected"

    # CRITICAL: Things that must never be associated with this character
    forbidden_associations:
      - "husband"        # Not married, has partner
      - "Chicago"        # Never lived there, from Seattle
      - "sister"         # Only child

    # What this character cannot know before certain points
    forbidden_knowledge_before:
      partner_secret: "ch15"
      organization_true_nature: "ch22"

  CHAR_004:
    canonical_name: "Jordan Rivera"
    aliases: ["Jordan", "J"]
    # ... etc

organizations:
  ORG_001:
    name: "Meridian Corp"
    type: "tech_company"
    true_nature: "front for [redacted]"  # Revealed ch22
    # ...

relationships:
  alex_jordan:
    type: "romantic_partners"
    progression:
      ch1: { state: "early_dating", notes: null }
      ch8: { state: "committed", notes: "moved in together" }
      ch15: { state: "strained", notes: "secret discovered" }
      ch22: { state: "reconciled", notes: "worked through betrayal" }

knowledge:
  KNOW_001:
    name: "Organization's true purpose"
    content: "Meridian is actually a front for [redacted]"

    secret_holders: ["CHAR_012", "CHAR_014"]
    reveal_chapter: 22

    # Characters who cannot know this before the reveal
    forbidden_knowers_before:
      CHAR_001: "ch22"  # Alex
      CHAR_004: "ch22"  # Jordan

events:
  EVENT_001:
    name: "The Warehouse Incident"
    chapter: 8
    participants: ["CHAR_001", "CHAR_002", "CHAR_003"]
    consequences:
      - "Alex learns about powers"
      - "Marcus injured"

forbidden:
  FORBID_001:
    name: "Alex's husband"
    type: "character"
    reason: "AI invention - Alex is not married"
    origin: "ai_invention_2025_01_10"

    detection_patterns:
      - "Alex's husband"
      - "her husband"  # in Alex POV
      - "married to Alex"

    canonical_truth: "Alex has a partner (Jordan), not a husband."

canon_warnings:
  - id: "alex_not_married"
    severity: "critical"
    warning: "Alex is NOT married. She has a partner named Jordan."
    applies_to: ["alex"]

  - id: "marcus_alive"
    severity: "critical"
    warning: "Marcus is injured, not dead. He recovers in ch12."
    applies_to: ["marcus"]
```

---

## Component 2: Negative Constraints

Explicit statements of what is **NOT TRUE**. This is the immune system of your story.

### Format

```markdown
# NEGATIVE_CONSTRAINTS.md

## Usage
Before any prose generation:
1. Load this document
2. Load constraints for characters appearing in scene
3. Evaluator checks output against all applicable constraints

**Severity Levels:**
- **BLOCKING:** Evaluator rejects output automatically
- **WARNING:** Evaluator flags for human review

---

## Global Constraints (Always Active)

### Company Names
| Status | Statement |
|--------|-----------|
| WRONG | "Titan Corp" - OUTDATED, do not use |
| RIGHT | "Meridian Corp" - Correct company name |

### Character Deaths
| Status | Statement |
|--------|-----------|
| WRONG | Marcus dies in Book 1 |
| RIGHT | Marcus is injured but survives |

---

## Character-Specific Constraints

### ALEX CHEN

**Severity: BLOCKING**

#### Relationship Status
| Status | Statement |
|--------|-----------|
| WRONG | Alex is married |
| WRONG | Alex has a husband |
| WRONG | Alex's husband [anything] |
| RIGHT | Alex has a partner named Jordan |
| RIGHT | They are not married |

**Source of Error:** Previous session invented a husband named "David"

**Detection Patterns:**
- "Alex" + (husband | married | wife)
- "her husband" in Alex POV scenes

---

### JORDAN RIVERA

**Severity: BLOCKING**

#### The Secret
| Status | Statement |
|--------|-----------|
| WRONG | Alex knows Jordan's secret before ch15 |
| RIGHT | Jordan's secret is revealed IN ch15 |
| RIGHT | Before ch15, Alex is unaware |

**Detection Patterns:**
- Alex referencing Jordan's secret before ch15
- Alex acting on knowledge of secret before ch15
```

### Why Negative Constraints Matter

- Stating "Alex has a partner named Jordan" doesn't prevent "Alex's husband said..."
- Stating "Alex is NOT married, has NO husband" **does** prevent that error

---

## Component 3: Session Manifests

Before each writing session, generate a manifest that specifies what context to load, what to exclude, and what constraints are active.

### Manifest Schema

```yaml
# SESSION_MANIFEST.yaml

meta:
  session_id: "2025-01-15_ch12_prose"
  created: "2025-01-15T14:30:00Z"
  task: "Chapter 12 prose generation"
  chapter: 12
  timeline_position: "week_8"

# What files/sections to load
loaded:
  canon:
    - path: "entity_catalog/ENTITY_CATALOG.yaml"
      sections: ["characters.CHAR_001", "knowledge", "canon_warnings"]
      reason: "Core queryable state"

    - path: "context/negative_constraints.md"
      sections: ["Global Constraints", "ALEX CHEN", "JORDAN RIVERA"]
      reason: "Constraint enforcement"

  characters:
    - path: "character_arcs/Alex_Arc_Tracker.md"
      sections: ["Chapter 12", "threads.relationship"]
      reason: "POV character state"

    - path: "character_arcs/Jordan_Arc_Tracker.md"
      sections: ["Chapter 12"]
      reason: "Present in scene"

  structure:
    - path: "story_bibles/Chapter_12_STRUCTURE.md"
      reason: "Beat sheet for this chapter"

  continuity:
    - path: "manuscript/chapter_11.md"
      reason: "Previous chapter for state continuity"

# What to explicitly NOT load (and why)
excluded:
  - path: "character_arcs/Marcus_Arc_Tracker.md"
    reason: "Marcus does not appear in Chapter 12"

  - path: "story_bibles/chapters_20-24.md"
    reason: "Future content, spoiler contamination risk"

# Validation scope
validation:
  canon_warnings_active:
    - "alex_not_married"
    - "marcus_alive"

  knowledge_gates:
    alex:
      knows:
        - "Jordan's job stress"
        - "Organization seems legitimate"
      doesnt_know:
        - "Organization's true purpose"  # Learns ch22
        - "Jordan's secret"              # Learns ch15

    jordan:
      knows:
        - "Own secret"
        - "Organization's true purpose"
      doesnt_know:
        - "Alex is investigating"

  relationship_states:
    alex_jordan: "strained"

  negative_constraints:
    - "Alex is NOT married"
    - "Alex does NOT know Jordan's secret yet"

# Output expectations
output:
  type: "prose"
  file: "manuscript/chapter_12.md"

  required_elements:
    - "Alex notices Jordan's stress"
    - "First hint of organization irregularities"

  forbidden_elements:
    - "Alex's husband"
    - "References to organization's true purpose"
    - "Jordan revealing secret early"

# Session scratchpad
scratchpad:
  pending_decisions: []
  flags: []
  human_review_needed: []
```

---

## Component 4: Character State Index

A queryable YAML file tracking character states across chapters.

### Structure

```yaml
# CHARACTER_STATE_INDEX.yaml

meta:
  version: "1.0"
  book: 1
  total_chapters: 24

# Timeline mapping
timeline:
  ch1:  { month: 1, event: "inciting_incident" }
  ch8:  { month: 2, event: "warehouse_incident" }
  ch12: { month: 3, event: "investigation_deepens" }
  ch15: { month: 4, event: "secret_revealed" }
  ch22: { month: 6, event: "truth_exposed" }
  ch24: { month: 6, event: "resolution" }

# Canon warnings (query before any generation)
canon_warnings:
  - id: "alex_not_married"
    severity: "critical"
    warning: "Alex is NOT married. She has a partner named Jordan."
    applies_to: ["alex"]

  - id: "secret_timing"
    severity: "critical"
    warning: "Jordan's secret is revealed IN ch15. Alex cannot know before."
    applies_to: ["alex", "jordan"]

# Character entries
characters:
  alex:
    meta:
      arc_tracker: "Alex_Arc_Tracker.md"
      full_name: "Alex Chen"
      book_role: "protagonist_pov"

    arc:
      summary: "Isolation -> Trust -> Betrayal -> Resilience"
      type: "trust_arc"

    threads:
      investigation:
        type: "discovery"
        chapters: [3, 6, 9, 12, 18, 22]
        gates:
          ch3:
            state: "begins_investigation"
            knows: ["something_wrong"]
          ch12:
            state: "deepening"
            knows: ["pattern_emerging"]
          ch22:
            state: "truth_revealed"
            knows: ["full_scope"]

      relationship:
        type: "romantic_arc"
        chapters: [1, 8, 15, 22]
        gates:
          ch1:
            state: "early_dating"
          ch8:
            state: "committed"
          ch15:
            state: "strained"
            trigger: "secret_discovered"
          ch22:
            state: "reconciled"

    chapter_states:
      ch12:
        location: "office"
        emotional: "suspicious_focused"
        physical:
          injuries: null
        knows:
          - "pattern_emerging"
          - "organization_anomalies"
        doesnt_know:
          - "jordan_secret"
          - "organization_true_nature"
        believes:
          - "something_is_wrong"
        relationships:
          jordan: { state: "committed_but_stressed", notes: null }

# Knowledge tracking
knowledge_tracking:
  jordan_secret:
    description: "Jordan's hidden past"
    secret_holder: "jordan"
    reveal_chapter: 15
    awareness:
      ch1: [jordan]
      ch14: [jordan]
      ch15: [jordan, alex]
      ch24: [jordan, alex, team]

  organization_truth:
    description: "Meridian's true purpose"
    secret_holders: [marcus, director]
    reveal_chapter: 22
    awareness:
      ch1: [marcus, director]
      ch21: [marcus, director]
      ch22: [marcus, director, alex, jordan, team]

# Relationship tracking
relationships:
  alex_jordan:
    type: "romantic_partners"
    progression:
      ch1: { state: "early_dating" }
      ch8: { state: "committed" }
      ch15: { state: "strained", trigger: "secret_discovered" }
      ch22: { state: "reconciled" }
```

---

## Component 5: Method Actor Prose Generation

The Method Actor format has Claude perform characters sequentially, using loaded context and constraints.

### Format

```markdown
## BACKSTAGE (Context Loaded):

**Scene ID:** book1_ch12_scene2
**Location:** Office, evening
**Participants:** Alex, Jordan

**Character States:**
- Alex: [Loaded from arc tracker]
  - Knows: Pattern emerging, organization anomalies
  - Doesn't know: Jordan's secret, organization truth
  - Emotional: Suspicious, focused

- Jordan: [Loaded from arc tracker]
  - Knows: Own secret, organization truth
  - Doesn't know: Alex is investigating
  - Emotional: Stressed, evasive

**Touchpoints:**
- A: Alex mentions timeline anomaly
- B: Jordan deflects, Alex notices

**Constraints:**
- Alex cannot reveal she's investigating
- Jordan cannot reveal secret
- Must plant seed for ch15 confrontation

---

## ON STAGE NOW:

[CURTAIN RISES]

[NARRATOR]: Evening at the office. Alex at her desk, files spread.
Jordan enters, coat still on.

[AS ALEX, suspicious but hiding it]:
"You're late." I didn't look up from the files. Couldn't let him
see what I was reading.

[AS JORDAN, stressed, deflecting]:
"Traffic." He loosened his tie. "What are you working on?"

[AS ALEX, carefully casual]:
"Expense reports. The April ones don't add up."

[Continue scene...]

[END SCENE when touchpoint_b achieved]

---

## DIRECTOR NOTES:
- Requirements met: [checklist]
- State changes: [what changed for each character]
- Seeds planted: [foreshadowing for later]
- Consequences propagating: [what carries forward]
```

### Voice Cards

Each character needs a voice card defining their speech patterns:

```markdown
### ALEX CHEN (Protagonist POV)

**Core:** Analytical, guarded, processes through observation
**Background:** Data scientist, trained to see patterns

**Voice Patterns:**
- Precise language, specific details
- Internal analysis: "[Statement]. Or rather, [correction]?"
- Notices small details others miss
- Deadpan delivery when stressed
- Questions everything, trusts data

**Physical Tells:**
- Adjusts glasses when thinking
- Taps fingers when processing
- Goes still when suspicious

**Example:**
"The numbers didn't lie. They just didn't tell the whole story yet."
```

---

## Component 6: TTRPG Dice Mechanics (Optional)

Add controlled randomness to scene outcomes while keeping major beats fixed.

### Philosophy

**Fixed (Touchpoints):**
- Touchpoint A (starting state)
- Touchpoint B (ending state)
- Story must reach B from A

**Variable (Dice):**
- How character arrives at B
- What complications occur
- Character state when reaching B
- Resource costs paid

**Result:** Same destination, different journey.

### Dice System (d20)

```
- Critical Success (20):    Best outcome, bonus benefit
- Success (15-19):          Outcome achieved cleanly
- Partial Success (10-14):  Outcome with complication or cost
- Failure (5-9):            Must try different approach
- Critical Failure (1-4):   Outcome not achieved, additional problem
```

### Roll Types

**Action Rolls:** Character attempting specific action
**Consequence Rolls:** Determining severity of unavoidable event
**Discovery Rolls:** Finding resources or information
**Resource Rolls:** Determining efficiency or output

### Integration with Method Actor

```yaml
scene_id: "book1_ch8_scene1_warehouse"
touchpoint_a: "Alex enters warehouse"
touchpoint_b: "Alex discovers evidence"

dice_rolls:
  - roll_id: "stealth_entry"
    result: 12  # Partial success
    consequence: "Made noise, guards alerted"

  - roll_id: "evidence_quality"
    result: 17  # Success
    consequence: "Found clear documentation"

character_state_after:
  alex:
    knows:
      - "organization_connected_to_incident"
    physical: "Minor bruise from close call"
    emotional: "Vindicated, worried about guards"
```

Method Actor then performs the scene with those constraints.

---

## Component 7: Evaluator

The gatekeeper between generated output and persistent canon. **Nothing becomes canon until the Evaluator approves it.**

### Evaluation Phases

| Phase | Severity | Purpose |
|-------|----------|---------|
| 1. Entity Extraction | — | Inventory what prose contains |
| 2. Canon Warning Check | BLOCKING | Hard errors (deaths, names) |
| 3. Negative Constraint Check | BLOCKING | Explicit "NOT TRUE" violations |
| 4. Knowledge State Check | FLAG | Who knows what when |
| 5. Relationship State Check | FLAG | Emotional consistency |
| 6. Timeline Check | FLAG | Chronological errors |
| 7. Unknown Entity Check | HUMAN_REVIEW | New things that might be inventions |

### Phase Outcomes

- **BLOCKING** → Auto-reject output, require revision
- **FLAG** → Flag for human review, don't auto-reject
- **HUMAN_REVIEW** → Pause for human decision

### Manual Evaluation (v1)

```bash
# Check for forbidden patterns
grep -E "Alex.*(husband|married)" chapter_12.md
grep -E "organization.*true purpose" chapter_12.md
grep -E "Jordan.*(secret|truth|actually)" chapter_12.md

# If any matches: REJECT, revise, re-run
```

### Evaluation Output

```yaml
result: REJECTED  # or APPROVED or FLAGGED
phase: "negative_constraint_check"

violation:
  constraint: "alex_not_married"
  evidence: "Line 45: 'Alex's husband had warned her about this'"
  required_change: "Alex has a partner (Jordan), not a husband"
  reference: "negative_constraints.md#ALEX CHEN"

action: "Revise prose, re-run Evaluator"
```

---

## Workflow

### Before Writing Session

1. **Determine scope** — What chapter/scene? Which characters present?

2. **Generate manifest** — Specify:
   - What context to load
   - What to exclude (and why)
   - What constraints are active
   - What's required in output
   - What's forbidden in output

3. **Load targeted context** — Give the LLM:
   - The manifest
   - Relevant sections of Entity Catalog
   - Relevant negative constraints
   - Previous chapter (for continuity)
   - Scene structure/beat sheet

### During Writing Session

4. **Generate prose** — Use Method Actor format

5. **Track session decisions** — Any new canonical decisions go in scratchpad

### After Writing Session

6. **Run Evaluator** — Check output against constraints

7. **Handle results:**
   - **APPROVED** → Accept output, update trackers
   - **REJECTED** → Revise, re-run Evaluator
   - **FLAGGED** → Human reviews, resolves flags

8. **Update persistent context:**
   - Update arc trackers with "As Written" notes
   - Add new negative constraints if errors were caught
   - Archive manifest for audit trail

9. **Create session document** — Record decisions made, errors corrected

---

## Templates

### New Project Setup Checklist

```markdown
## Project: [Your Project Name]

### Step 1: Create Entity Catalog
- [ ] Define meta section (version, series name)
- [ ] Add all major characters
- [ ] Add organizations
- [ ] Add key relationships
- [ ] Add known secrets with reveal timing
- [ ] Add forbidden entities (start empty, populate when errors occur)

### Step 2: Create Negative Constraints
- [ ] Create file with global constraints
- [ ] Add character-specific sections (populate as needed)
- [ ] Define severity levels

### Step 3: Create Character State Index
- [ ] Define timeline mapping
- [ ] Add canon warnings
- [ ] Add character entries with thread tracking
- [ ] Set up knowledge tracking
- [ ] Set up relationship tracking

### Step 4: Create Arc Trackers
- [ ] One per major character
- [ ] Chapter-by-chapter state tracking
- [ ] Emotional progression
- [ ] Key knowledge gates

### Step 5: Create Manifest Template
- [ ] Copy schema
- [ ] Customize for your project structure

### Step 6: Define Evaluator Checklist
- [ ] List BLOCKING checks
- [ ] List FLAG checks
- [ ] Define HUMAN_REVIEW triggers
```

### Session Pre-Flight Checklist

```markdown
## Session: [Date] - [Chapter/Scene]

### Before Starting
- [ ] Manifest created
- [ ] Correct characters loaded
- [ ] Negative constraints for scene loaded
- [ ] Previous chapter loaded for continuity
- [ ] Beat sheet/structure loaded
- [ ] Knowledge gates verified

### During Session
- [ ] Using Method Actor format
- [ ] Recording decisions in scratchpad
- [ ] Flagging uncertain elements

### After Session
- [ ] Evaluator checks run
- [ ] Violations fixed
- [ ] Arc trackers updated
- [ ] Session document created
- [ ] Manifest archived
```

### Character Voice Card Template

```markdown
### [CHARACTER NAME]

**Core:** [One sentence essence]
**Background:** [Relevant history that shapes voice]

**Voice Patterns:**
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]
- [Stress response]

**Physical Tells:**
- [Tell 1]
- [Tell 2]

**Forbidden:**
- [Things this character would NEVER say/do]

**Example Dialogue:**
"[Characteristic line]"

**Example Internal Monologue:**
[Characteristic thought pattern]
```

---

## Lessons Learned

### From Actual Production Use

These patterns emerged from generating 100k+ words of fiction with this system:

1. **Bulk prose generation doesn't work.** Claude invents details to fill gaps instead of asking. Errors sneak in.

2. **Scene-by-scene generation is required.** Check structure file before each chunk. Consult constraints.

3. **Written instructions don't constrain Claude effectively.** Each session starts fresh. QC burden falls on the human.

4. **Positive documentation doesn't prevent negative invention.** "Victor has a girlfriend" doesn't prevent "Victor's late wife." You need explicit negatives.

5. **Errors propagate faster than fixes.** One session's invention becomes three sessions' canon if not caught immediately.

6. **The Evaluator is the gate.** Nothing is canon until validated. This discipline prevents cascading errors.

7. **Archive everything.** Manifests, session documents, error logs. You'll need the audit trail.

### The Meta-Pattern

This system works because it addresses core LLM limitations:

1. **Token window** → Solved by loading only what's needed (manifests)
2. **Statelessness** → Solved by session documents and Entity Catalog
3. **Non-determinism** → Solved by Evaluator (catch inventions before they propagate)

**Key insight:** You can't prevent LLMs from inventing. You can only catch inventions before they become canon.

The Evaluator is the gate. Nothing passes until validated.

---

## File Structure

```
project/
├── entity_catalog/
│   ├── ENTITY_CATALOG.yaml          # Canonical truth
│   └── manifests/
│       └── ch[N]_session_manifest.yaml
│
├── context/
│   ├── negative_constraints.md       # What is NOT true
│   ├── manifest_schema.md            # Manifest structure reference
│   └── evaluator_spec.md             # Validation rules
│
├── character_arcs/
│   ├── CHARACTER_STATE_INDEX.yaml    # Queryable state
│   └── [Name]_Arc_Tracker.md         # Narrative documents
│
├── story_bibles/
│   ├── Chapter_[N]_STRUCTURE.md      # Beat sheets
│   └── [Book]_STRUCTURE.md           # Overall structure
│
├── manuscript/
│   └── chapter_[N].md                # Generated prose
│
└── session_documents/
    ├── SESSION_LOG_YYYY-MM-DD.md     # What happened
    └── SESSION_REFLECTION_*.md       # Learnings
```

---

## Quick Reference

### When starting a session:
1. Create manifest (what to load, what to forbid)
2. Load targeted constraints
3. Include previous chapter for continuity

### When writing:
1. Use Method Actor format
2. Perform one character at a time
3. Note any new canonical decisions in scratchpad
4. Don't invent — flag uncertainty for human review

### When finishing:
1. Run Evaluator checks
2. Fix any violations
3. Update trackers
4. Create session document
5. Add any new negative constraints discovered

### When an error is found:
1. Fix in prose immediately
2. Add to negative constraints
3. Add to forbidden entities
4. Add canon warning if critical
5. Document source of error

---

*Version 1.0 — December 2025*
*Derived from production use on 200k+ word novel series*
