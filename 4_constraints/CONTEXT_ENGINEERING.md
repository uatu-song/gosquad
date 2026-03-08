# Context Engineering for Fiction: A System for LLM-Assisted Long-Form Writing

**Version:** 1.0
**Purpose:** Enable LLMs to assist with long-form creative writing without hallucinating details, losing continuity, or violating established canon.

---

## The Problem This System Solves

When using LLMs for long-form fiction (novels, series, screenplays), three fundamental constraints cause errors:

1. **Token Window** — LLMs have bounded working memory. You cannot load an entire story bible every session.
2. **Statelessness** — Nothing persists between sessions. Each conversation starts fresh.
3. **Non-Determinism** — LLMs fill gaps by inventing plausible details. These inventions can contradict established canon.

### The Failure Mode

Without systematic constraint enforcement, this happens:

```
Session 1: Claude writes "Victor thought of his late wife Clara"
           (Invented detail — Victor was never married)

Session 2: Arc tracker updated with Clara reference
           (Invention becomes documented)

Session 3: Clara treated as canon, referenced again
           (Error propagates)

Session 4: "Clara" is now "real" in the narrative
           (Error is entrenched)
```

This system prevents that failure mode.

---

## Core Architecture

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
         │                                           │
         ▼                                           ▼
    Load targeted                              Gate output
    constraints for                            before it
    this session                               becomes canon
```

### Key Insight

The system works because:
- You **don't load everything** — you load targeted constraints for the specific scene/chapter
- You **validate before accepting** — output doesn't become canon until it passes the Evaluator
- You **document what's NOT true** — negative constraints prevent inventions more effectively than positive statements

---

## System Components

### 1. Entity Catalog

A machine-readable YAML file containing all canonical story elements.

**What it contains:**
- Characters (with IDs, aliases, demographics, relationships, forbidden associations)
- Organizations
- Relationships (with progression across chapters/timeline)
- Knowledge tracking (who knows what, when)
- Events (with chapter/timeline placement)
- Forbidden entities (things that must never appear)
- Validation queries (pattern matching for common errors)

**Example structure:**

```yaml
characters:
  CHAR_001:
    canonical_name: "Alex Chen"
    aliases: ["Alex", "A.C."]

    demographics:
      gender: "woman"
      pronouns: ["she", "her", "hers"]

    relationships:
      partner: "CHAR_004"
      employer: "ORG_001"

    arc:
      book1_summary: "Isolation -> Trust -> Betrayal -> Resilience"
      start_state: "isolated_defensive"
      end_state: "cautiously_connected"

    # CRITICAL: Things that must never be associated with this character
    forbidden_associations:
      - "husband"  # Not married, has partner
      - "Chicago"  # Never lived there, from Seattle

    # What this character cannot know before certain points
    forbidden_knowledge_before:
      partner_secret: "ch15"
      organization_true_nature: "ch22"

forbidden:
  FORBID_001:
    name: "Alex's husband"
    type: "character"
    reason: "AI invention - Alex is not married"

    detection_patterns:
      - "Alex's husband"
      - "her husband"  # in Alex POV
      - "married to Alex"

    canonical_truth: "Alex has a partner (Jordan), not a husband."

knowledge:
  KNOW_001:
    name: "The organization's true purpose"
    content: "The company is actually a front for [redacted]"

    secret_holders: ["CHAR_012", "CHAR_014"]
    reveal_chapter: 22

    # Characters who cannot know this before the reveal
    forbidden_knowers_before:
      CHAR_001: "ch22"  # Alex
      CHAR_002: "ch22"  # Marcus
```

### 2. Negative Constraints Document

Explicit statements of what is **NOT TRUE**. This is the immune system of the story.

**Why negative constraints matter:**
- Stating "Alex has a partner named Jordan" doesn't prevent "Alex's husband said..."
- Stating "Alex is NOT married, has NO husband" **does** prevent that error

**Format:**

```markdown
## CHARACTER NAME

**Severity: BLOCKING** (or WARNING)

| Status | Statement |
|--------|-----------|
| WRONG | [incorrect thing that might be invented] |
| WRONG | [another incorrect possibility] |
| RIGHT | [the canonical truth] |
| RIGHT | [additional canonical context] |

**Source of Error:** [Why this constraint exists — what previous error prompted it]

**Detection Patterns:**
- [regex or entity patterns to catch violations]
```

**Example:**

```markdown
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
```

### 3. Session Manifests

Before each writing session, generate a manifest that specifies:
- What context to load
- What to explicitly exclude (and why)
- What constraints are active
- What the output should contain (and what it must NOT contain)

**Manifest structure:**

```yaml
manifest:
  session_id: "2025-01-15_ch12_prose"
  chapter: 12
  timeline_position: "week_8"

  # What files/sections to load
  loaded:
    characters:
      - id: "CHAR_001"
        name: "Alex Chen"
        role: "POV protagonist"
        sections: ["ch12_state", "relationships", "forbidden_associations"]

      - id: "CHAR_004"
        name: "Jordan"
        role: "Present in Scene 2"
        sections: ["ch12_state", "relationship_with_alex"]

    constraints:
      - path: "negative_constraints.md"
        sections: ["ALEX CHEN", "JORDAN", "Global Constraints"]

  # What to explicitly NOT load (with reasons)
  excluded:
    - id: "CHAR_008"
      name: "Marcus"
      reason: "Not in this chapter, avoid context pollution"

    - path: "chapters/ch20-24.md"
      reason: "Future content, spoiler contamination risk"

  # Knowledge gates for this chapter
  knowledge_gates:
    CHAR_001:  # Alex
      knows:
        - "Jordan's job stress"
        - "Organization seems legitimate"
      doesnt_know:
        - "Organization's true purpose"  # Learns ch22
        - "Jordan's secret"  # Learns ch15

  # Things that MUST appear
  required_elements:
    - "Alex notices Jordan's stress"
    - "First hint of organization irregularities"

  # Things that MUST NOT appear
  forbidden_elements:
    - "Alex's husband"
    - "References to organization's true purpose"
    - "Jordan revealing secret early"

  # Seeds to plant for future payoff
  seeds_to_plant:
    - name: "Organization irregularities"
      method: "Alex notices expense report anomaly"
      foreshadows: "Ch22 reveal"
```

### 4. Evaluator

The gatekeeper between generated output and persistent canon. **Nothing becomes canon until the Evaluator approves it.**

**Evaluation phases:**

| Phase | Severity | Purpose |
|-------|----------|---------|
| 1. Entity Extraction | — | Build inventory of what prose contains |
| 2. Canon Warning Check | BLOCKING | Hard errors (deaths, names) |
| 3. Negative Constraint Check | BLOCKING | Explicit "NOT TRUE" statements |
| 4. Knowledge State Check | FLAG | Who knows what when |
| 5. Relationship State Check | FLAG | Emotional consistency |
| 6. Timeline Check | FLAG | Chronological errors |
| 7. Unknown Entity Check | HUMAN_REVIEW | New things that might be inventions |

**Phase outcomes:**
- **BLOCKING** → Auto-reject output, require revision
- **FLAG** → Flag for human review, don't auto-reject
- **HUMAN_REVIEW** → Pause for human decision

**Implementation (v1 - Manual/Regex):**

Run these checks after each prose generation:

```bash
# Check for forbidden patterns
grep -E "Alex.*(husband|married)" chapter_12.md
grep -E "organization.*true purpose" chapter_12.md
grep -E "Jordan.*(secret|truth|actually)" chapter_12.md

# If any matches: REJECT, revise, re-run
```

**Evaluation output:**

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
   - What to exclude
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

4. **Generate prose** — The LLM writes within the constraints

5. **Track session decisions** — Any new canonical decisions go in a scratchpad

### After Writing Session

6. **Run Evaluator** — Check output against:
   - Canon warnings
   - Negative constraints
   - Knowledge states
   - Relationship states
   - Timeline

7. **Handle results:**
   - **APPROVED** → Accept output, update trackers
   - **REJECTED** → Revise, re-run Evaluator
   - **FLAGGED** → Human reviews, resolves flags

8. **Update persistent context:**
   - Update arc trackers with "As Written" notes
   - Add new negative constraints if errors were caught
   - Archive manifest for audit trail

9. **Create session document** — Record:
   - Creative decisions made
   - Errors corrected
   - Context state at session end

---

## The Negative Constraint Pattern

This is the most important defensive pattern. When an error occurs:

### 1. Fix immediately
Don't let the error propagate to more files.

### 2. Document as negative constraint

```markdown
### [CHARACTER]

**Severity: BLOCKING**

| Status | Statement |
|--------|-----------|
| WRONG | [the invented thing] |
| RIGHT | [what's actually true] |

**Source of Error:** [What session invented this]

**Detection Patterns:**
- [patterns to catch recurrence]
```

### 3. Add to Entity Catalog

```yaml
forbidden:
  FORBID_XXX:
    name: "[Error description]"
    type: "character" | "event" | "detail" | "mechanic"
    reason: "[Why this is wrong]"
    origin: "ai_invention_YYYY_MM_DD"

    detection_patterns:
      - "[regex pattern]"

    canonical_truth: "[What's actually true]"
```

### 4. Add to canon warnings
If critical, add a warning that auto-rejects on detection.

---

## Common Failure Modes and Defenses

### Failure: Invented relationships
**Example:** LLM creates a "sister" for a character who's an only child

**Defense:**
- Entity Catalog: `forbidden_associations: ["sister", "brother", "sibling"]`
- Negative Constraint: "Character is an only child, has NO siblings"
- Detection pattern in Evaluator

### Failure: Knowledge leakage
**Example:** Character references something they shouldn't know yet

**Defense:**
- Knowledge gates in manifest specify `knows` and `doesnt_know`
- Evaluator Phase 4 checks knowledge references against gates

### Failure: Timeline violations
**Example:** Reference to an event that hasn't happened yet

**Defense:**
- Timeline constraints in Entity Catalog
- Evaluator Phase 6 checks timeline references

### Failure: Character voice drift
**Example:** Formal character suddenly uses casual slang

**Defense:**
- Voice requirements in manifest
- Character voice patterns documented in Entity Catalog

### Failure: Relationship state inconsistency
**Example:** Characters act friendly when they should be estranged

**Defense:**
- Relationship progression tracked in Entity Catalog
- Manifest specifies relationship state for this chapter
- Evaluator Phase 5 checks emotional tone

---

## Setting Up for a New Project

### Step 1: Create Entity Catalog skeleton

```yaml
meta:
  version: "1.0"
  series: "[Your Series Name]"
  current_book: 1

characters:
  # Add characters as you create them
  # Minimum: canonical_name, aliases, forbidden_associations

organizations:
  # Add as needed

relationships:
  # Track key relationships with state progression

knowledge:
  # Track secrets and reveals

events:
  # Track major events with timeline placement

forbidden:
  # Start empty, populate when errors occur
```

### Step 2: Create Negative Constraints document

```markdown
# NEGATIVE_CONSTRAINTS.md

## Usage
Before any prose generation:
1. Load this document
2. Load constraints for characters in scene
3. Evaluator checks output against all constraints

## Global Constraints
[Things that apply to entire story]

## Character-Specific Constraints
[Populate as characters are developed]
```

### Step 3: Define manifest template

Create a template for session manifests that you can copy and populate:

```yaml
manifest:
  session_id: ""
  chapter:
  timeline_position: ""

  loaded:
    characters: []
    constraints: []

  excluded: []

  knowledge_gates: {}

  required_elements: []
  forbidden_elements: []

  seeds_to_plant: []
```

### Step 4: Define Evaluator checklist

Start with manual checks:

```markdown
## Pre-Acceptance Checklist

### BLOCKING Checks
- [ ] No forbidden entity names appear
- [ ] No forbidden associations appear
- [ ] No negative constraints violated

### FLAG Checks
- [ ] Character knowledge appropriate for this chapter
- [ ] Relationship tone matches documented state
- [ ] Timeline references are accurate

### HUMAN REVIEW
- [ ] Any new characters/entities? (If yes, canonize or reject)
- [ ] Any new information? (If yes, add to catalog)
```

---

## Implementation Levels

### Level 1: Manual (Minimum Viable)
- Entity Catalog as YAML reference
- Negative Constraints as markdown
- Manifests created manually before sessions
- Evaluator is a human-run checklist
- Grep for forbidden patterns

**Effort:** Low
**Protection:** Moderate

### Level 2: Semi-Automated
- Entity Catalog with validation queries
- Scripted pattern matching for BLOCKING checks
- Manifest partially auto-generated from chapter metadata
- Human review for FLAG items

**Effort:** Medium
**Protection:** Good

### Level 3: Integrated
- Evaluator runs automatically after generation
- Real-time constraint checking during generation
- Dashboard for flag management
- Lineage tracking database

**Effort:** High
**Protection:** Excellent

---

## The Meta-Pattern

This system works because it addresses the core LLM limitations:

1. **Token window** → Solved by loading only what's needed (manifests)
2. **Statelessness** → Solved by session documents and Entity Catalog
3. **Non-determinism** → Solved by Evaluator (catch inventions before they propagate)

The key insight: **You can't prevent LLMs from inventing. You can only catch inventions before they become canon.**

The Evaluator is the gate. Nothing passes until validated.

---

## Quick Reference

### When starting a session:
1. Create manifest (what to load, what to forbid)
2. Load targeted constraints
3. Include previous chapter for continuity

### When writing:
1. Work within constraints
2. Note any new canonical decisions in scratchpad
3. Don't invent — ask if uncertain

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

## Files This System Uses

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
└── session_documents/
    ├── SESSION_LOG_YYYY-MM-DD.md     # What happened
    └── SESSION_REFLECTION_*.md       # Learnings
```

---

## Final Note

This system emerged from practical experience with LLM hallucination in long-form fiction. The specific patterns (Victor's invented wife Clara, Tess's misread arc, Ryu's wrong surname) demonstrated that:

1. Positive documentation ("Victor's partner is Leah") doesn't prevent negative invention ("Victor's late wife Clara")
2. Validation after the fact allows errors to propagate
3. Each error, once documented, can be prevented forever

The system is overhead until you need it. Then it's essential.

Build the catalog. Document the constraints. Close the loop.

---

*Version 1.0 — December 2025*
