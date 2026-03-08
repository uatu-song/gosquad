# Method Actor System - Templates & Examples

**Companion document to METHOD_ACTOR_SYSTEM_PACKAGE.md**

This file contains copy-paste ready templates for implementing the Method Actor System.

---

## Table of Contents

1. [Entity Catalog Template](#1-entity-catalog-template)
2. [Negative Constraints Template](#2-negative-constraints-template)
3. [Session Manifest Template](#3-session-manifest-template)
4. [Character State Index Template](#4-character-state-index-template)
5. [Character Arc Tracker Template](#5-character-arc-tracker-template)
6. [Method Actor Scene Template](#6-method-actor-scene-template)
7. [Beat Sheet Template](#7-beat-sheet-template)
8. [Evaluator Checklist Template](#8-evaluator-checklist-template)
9. [Session Document Template](#9-session-document-template)
10. [TTRPG Dice Integration Template](#10-ttrpg-dice-integration-template)

---

## 1. Entity Catalog Template

```yaml
# ENTITY_CATALOG.yaml
# Version: 1.0
# Purpose: Single source of canonical truth

meta:
  version: "1.0"
  series: "[YOUR SERIES NAME]"
  current_book: 1
  last_updated: "[DATE]"

# ============================================
# CHARACTERS
# ============================================

characters:

  CHAR_001:
    canonical_name: "[FULL NAME]"
    aliases: ["[NICKNAME]", "[OTHER NAME]"]

    demographics:
      gender: "[gender]"
      pronouns: ["[pronoun]", "[pronoun]", "[pronoun]"]
      age: [number]
      ethnicity: "[ethnicity]"  # Optional

    role:
      book_role: "[protagonist | deuteragonist | antagonist | supporting]"
      occupation: "[job/role]"

    relationships:
      # Use character IDs
      partner: "CHAR_XXX"
      employer: "ORG_XXX"
      mentor: "CHAR_XXX"
      enemy: "CHAR_XXX"

    arc:
      book1_summary: "[Start State] -> [Mid Point] -> [End State]"
      start_state: "[emotional/situational state]"
      end_state: "[emotional/situational state]"
      arc_type: "[trust_arc | redemption | fall | hero_journey | etc]"

    # CRITICAL: Things that must NEVER be associated with this character
    forbidden_associations:
      - "[thing that is NOT true]"
      - "[another thing that is NOT true]"

    # Knowledge gates - what character cannot know before certain points
    forbidden_knowledge_before:
      secret_name: "ch[N]"
      another_secret: "ch[N]"

    voice:
      speech_patterns:
        - "[pattern 1]"
        - "[pattern 2]"
      vocabulary_level: "[casual | formal | technical | mixed]"
      verbal_tics: ["[tic 1]", "[tic 2]"]

  # Add more characters...
  CHAR_002:
    # ...

# ============================================
# ORGANIZATIONS
# ============================================

organizations:

  ORG_001:
    name: "[ORGANIZATION NAME]"
    aliases: ["[ALIAS]"]
    type: "[company | government | secret | etc]"
    purpose_public: "[what people think it is]"
    purpose_true: "[what it actually is]"  # If different
    reveal_chapter: [N]  # When truth is revealed, if applicable

    members:
      - role: "[role]"
        character: "CHAR_XXX"

  # Add more organizations...

# ============================================
# RELATIONSHIPS (Progression Tracking)
# ============================================

relationships:

  "[char1]_[char2]":
    type: "[romantic | friendship | rivalry | mentor | family]"
    progression:
      ch1: { state: "[state]", notes: "[optional notes]" }
      ch5: { state: "[state]", trigger: "[what changed it]" }
      ch12: { state: "[state]", notes: null }
      # Add chapters where relationship changes...

  # Add more relationships...

# ============================================
# KNOWLEDGE TRACKING (Secrets & Reveals)
# ============================================

knowledge:

  KNOW_001:
    name: "[SECRET NAME]"
    content: "[What the secret is]"

    secret_holders: ["CHAR_XXX", "CHAR_XXX"]
    reveal_chapter: [N]

    # Who learns it and when
    awareness_progression:
      ch1: ["CHAR_XXX"]
      ch[N]: ["CHAR_XXX", "CHAR_XXX"]  # After reveal

    # Characters who CANNOT know before reveal
    forbidden_knowers_before:
      CHAR_XXX: "ch[N]"

  # Add more secrets...

# ============================================
# MAJOR EVENTS
# ============================================

events:

  EVENT_001:
    name: "[EVENT NAME]"
    chapter: [N]
    timeline_position: "[month/week/day]"  # Optional
    participants: ["CHAR_XXX", "CHAR_XXX"]

    consequences:
      - "[consequence 1]"
      - "[consequence 2]"

    triggers:
      - "[what this event causes]"

  # Add more events...

# ============================================
# FORBIDDEN ENTITIES (AI Inventions to Reject)
# ============================================

forbidden:

  FORBID_001:
    name: "[INVENTED THING]"
    type: "[character | event | detail | relationship]"
    reason: "[Why this is wrong - what session invented it]"
    origin: "ai_invention_[DATE]"

    detection_patterns:
      - "[regex or text pattern to catch it]"
      - "[another pattern]"

    canonical_truth: "[What is actually true instead]"

  # Add as errors are discovered...

# ============================================
# CANON WARNINGS (Critical Errors)
# ============================================

canon_warnings:

  - id: "[unique_id]"
    severity: "[critical | moderate]"
    warning: "[Clear statement of what is true]"
    applies_to: ["[character_id]"]
    error_source: "[What previous error prompted this]"  # Optional

  # Add warnings as needed...
```

---

## 2. Negative Constraints Template

```markdown
# NEGATIVE_CONSTRAINTS.md
# Version: 1.0
# Purpose: Explicit statements of what is NOT TRUE
# Authority: BLOCKING - violations reject output

---

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

### [Category Name]
| Status | Statement |
|--------|-----------|
| WRONG | [incorrect thing] |
| RIGHT | [correct thing] |

### [Another Category]
| Status | Statement |
|--------|-----------|
| WRONG | [incorrect thing] |
| RIGHT | [correct thing] |

---

## Character-Specific Constraints

---

### [CHARACTER NAME]

**Severity: BLOCKING**

#### [Category - e.g., Relationship Status]
| Status | Statement |
|--------|-----------|
| WRONG | [incorrect thing] |
| WRONG | [another incorrect thing] |
| RIGHT | [correct thing] |
| RIGHT | [additional context] |

**Source of Error:** [What session/context caused this constraint to be needed]

**Detection Patterns:**
- [regex or text pattern]
- [another pattern]

---

### [ANOTHER CHARACTER]

**Severity: BLOCKING/WARNING**

#### [Category]
| Status | Statement |
|--------|-----------|
| WRONG | [incorrect] |
| RIGHT | [correct] |

**Source of Error:** [explanation]

**Detection Patterns:**
- [patterns]

---

## Timeline-Locked Constraints

**Severity: BLOCKING**

These events happen at SPECIFIC chapters. Do not move them earlier.

| Event | Chapter | Constraint |
|-------|---------|------------|
| [Event] | [N] | Cannot reference before ch[N] |
| [Event] | [N] | Cannot reference before ch[N] |

**Detection Method:** Check chapter number against event. If character references event before its chapter, REJECT.

---

## Knowledge State Constraints

**Severity: WARNING** (flag for review)

Characters cannot know things before they learn them.

Common violations to check:
- [Character] referencing [secret] before ch[N]
- [Character] knowing about [event] before ch[N]

---

## Adding New Constraints

When a Claude session invents something incorrect:

1. **Add immediately** - Don't wait
2. **Use table format** - WRONG/RIGHT for scannability
3. **Include Source of Error** - Why did this happen?
4. **Add Detection Patterns** - How to catch automatically
5. **Set Severity** - BLOCKING or WARNING

### Template for New Constraint

```markdown
### [CHARACTER NAME]

**Severity: BLOCKING/WARNING**

#### [Category]
| Status | Statement |
|--------|-----------|
| WRONG | [incorrect thing] |
| RIGHT | [correct thing] |

**Source of Error:** [explanation]

**Detection Patterns:**
- [pattern]
```

---

## Constraint Review Log

| Date | Constraint Added | Source of Error | Added By |
|------|------------------|-----------------|----------|
| [DATE] | [description] | [source] | [human/auto] |

---

*Last Updated: [DATE]*
*Version: 1.0*
```

---

## 3. Session Manifest Template

```yaml
# SESSION_MANIFEST_[DATE]_ch[N].yaml

# ============================================
# META
# ============================================

meta:
  session_id: "[DATE]_chapter[N]_[tasktype]"
  created: "[ISO 8601 datetime]"
  task: "[Human-readable task description]"
  chapter: [N]
  timeline_position: "[month/week in story]"

# ============================================
# CONTEXT LOADED
# ============================================

loaded:

  # Canon documents (always load core constraints)
  canon:
    - path: "entity_catalog/ENTITY_CATALOG.yaml"
      sections: ["[relevant sections]"]
      reason: "[why needed]"

    - path: "context/negative_constraints.md"
      sections: ["[character sections needed]"]
      reason: "Constraint enforcement"

  # Character arc trackers for characters in scene
  characters:
    - path: "character_arcs/[Name]_Arc_Tracker.md"
      sections: ["Chapter [N]", "[relevant threads]"]
      reason: "[why needed]"

    # Add more as needed...

  # Structure documents (beat sheets, outlines)
  structure:
    - path: "story_bibles/Chapter_[N]_STRUCTURE.md"
      reason: "Beat sheet for this chapter"

  # Previous chapter(s) for continuity
  continuity:
    - path: "manuscript/chapter_[N-1].md"
      reason: "Previous chapter for state continuity"

# ============================================
# CONTEXT EXCLUDED
# ============================================

excluded:
  - path: "[file path]"
    reason: "[why deliberately not loaded]"

  # Common reasons:
  # - "Character does not appear in this chapter"
  # - "Future content, spoiler contamination risk"
  # - "Irrelevant to current task"

# ============================================
# VALIDATION SCOPE
# ============================================

validation:

  # Canon warnings to enforce
  canon_warnings_active:
    - "[warning_id]"
    - "[warning_id]"

  # Knowledge gates - what characters know/don't know at this chapter
  knowledge_gates:
    [character_name]:
      knows:
        - "[fact]"
        - "[fact]"
      doesnt_know:
        - "[secret/fact they don't know yet]"

    [another_character]:
      knows:
        - "[fact]"
      doesnt_know:
        - "[fact]"

  # Relationship states to maintain
  relationship_states:
    "[char1]_[char2]": "[state]"

  # Negative constraints to enforce
  negative_constraints:
    - "[constraint description]"

# ============================================
# OUTPUT EXPECTATIONS
# ============================================

output:
  type: "[prose | outline | revision]"
  file: "manuscript/chapter_[N].md"

  required_elements:
    - "[thing that MUST appear]"
    - "[another requirement]"

  forbidden_elements:
    - "[thing that MUST NOT appear]"
    - "[another prohibition]"

# ============================================
# SCRATCHPAD (Session-Scoped)
# ============================================

scratchpad:
  pending_decisions: []
  flags: []
  human_review_needed: []

# ============================================
# OUTPUT LINEAGE (Added After Generation)
# ============================================

output_lineage:
  file: ""                    # Actual output file (fill after)
  generated_at: ""            # Timestamp (fill after)
  manifest_id: ""             # Links back to this manifest
  evaluator_result: ""        # "APPROVED" | "REJECTED" | "FLAGGED"
  human_review: false         # True if human reviewed
```

---

## 4. Character State Index Template

```yaml
# CHARACTER_STATE_INDEX.yaml
# Version: 1.0
# Purpose: Queryable character states across chapters

meta:
  version: "1.0"
  book: [N]
  last_updated: "[DATE]"
  total_chapters: [N]

# ============================================
# TIMELINE MAPPING
# ============================================

timeline:
  ch1:  { month: [N], event: "[event_name]", date_approx: "[early/mid/late]" }
  ch2:  { month: [N], event: "[event_name]" }
  # ... all chapters

# ============================================
# CANON WARNINGS (query before any generation)
# ============================================

canon_warnings:

  - id: "[unique_id]"
    severity: "[critical | moderate]"
    warning: "[Clear statement]"
    applies_to: ["[character]"]

  # Add all critical warnings...

# ============================================
# CHARACTERS
# ============================================

characters:

  [character_id]:
    meta:
      arc_tracker: "[Name]_Arc_Tracker.md"
      codename: "[if applicable]"
      full_name: "[Full Name]"
      book_role: "[role]"

    arc:
      summary: "[Start] -> [Mid] -> [End]"
      type: "[arc_type]"

    motives:
      stable:
        - { id: "[motive]", priority: 1 }
        - { id: "[motive]", priority: 2 }
      evolving:
        - { id: "[motive]", chapters: [1,2,3,4,5], note: "[context]" }
        - { id: "[motive]", chapters: [6,7,8,9,10], note: "[context]" }

    emotional_progression:
      - { stage: "[stage_name]", chapters: [1,2,3], description: "[description]" }
      - { stage: "[stage_name]", chapters: [4,5,6], description: "[description]" }

    threads:

      [thread_name]:
        type: "[thread_type]"
        description: "[what this thread tracks]"
        chapters: [1,4,8,12]
        gates:
          ch1:
            state: "[state]"
            trigger: "[what caused this]"
            knows: ["[fact]"]
          ch4:
            state: "[state]"
            trigger: "[what caused this]"
            consequence: "[result]"

    chapter_states:
      ch[N]:
        location: "[location]"
        emotional: "[emotional state]"
        physical:
          injuries: "[any injuries]"
          fatigue: "[fatigue level]"
        knows:
          - "[fact]"
        learns:
          - "[new fact this chapter]"
        doesnt_know:
          - "[fact they don't know]"
        believes:
          - "[belief]"
        relationships:
          [other_char]: { state: "[state]", notes: "[optional]" }
        key_actions:
          - "[action taken]"

# ============================================
# KNOWLEDGE TRACKING
# ============================================

knowledge_tracking:

  [secret_name]:
    description: "[What the secret is]"
    secret_holder: "[character]"
    reveal_chapter: [N]
    awareness:
      ch1: [[characters who know]]
      ch[N]: [[characters who know after reveal]]

# ============================================
# RELATIONSHIP EVENTS
# ============================================

relationship_events:
  - { relationship: "[char1]_[char2]", event: "[event]", chapter: [N] }

# ============================================
# KNOWLEDGE EVENTS
# ============================================

knowledge_events:
  - { knowledge: "[secret]", character: "[who learns]", learned_chapter: [N], source: "[how learned]" }
```

---

## 5. Character Arc Tracker Template

```markdown
# [Character Name] - Character Arc Tracker

**Purpose:** Track [Name]'s emotional state, knowledge, relationships, and capabilities at each major story point

---

## Book [N]: [Arc Title]

### Pre-Story State
- **Role:** [Role in story]
- **Relationships:** [Key relationships]
- **Knowledge:** [What they know]
- **Emotional:** [Emotional state]
- **Skills:** [Relevant skills]

---

### Chapter [N]: [Chapter Title/Event]

**The Event:** [What happens]

**[Name]'s Response:**
- [Action/reaction]
- [Internal response]

**State After:**
- **Emotional:** [State]
- **Knowledge:** [What they now know]
- **Relationships:** [Any changes]
- **Physical:** [Any injuries/changes]

---

### Chapter [N]: [Chapter Title/Event]

[Continue pattern for each significant chapter...]

---

## Book [N] Arc Summary

**The Journey:**
- [Start state] -> [Key turning point] -> [End state]

**What They Learned:**
- [Lesson 1]
- [Lesson 2]

**Key Relationships Evolved:**
- [Relationship]: [How it changed]

**Setup for Book [N+1]:**
- [Thread that continues]

---

## Relationship Summary

### [Other Character Name]
- [Relationship type]
- [How it evolved]

### [Another Character]
- [Relationship type]
- [How it evolved]

---

**Status:** [Current state of this tracker]
```

---

## 6. Method Actor Scene Template

```markdown
## BACKSTAGE (Context Loaded):

**Scene ID:** [book]_ch[N]_scene[N]_[description]
**Location:** [Where], [When]
**Participants:** [Character1], [Character2], [etc]

**Character States:**

- **[Character1]:** [Loaded from arc tracker]
  - Knows: [fact], [fact]
  - Doesn't know: [secret], [future event]
  - Emotional: [state]
  - Physical: [any relevant state]

- **[Character2]:** [Loaded from arc tracker]
  - Knows: [fact]
  - Doesn't know: [fact]
  - Emotional: [state]

**Touchpoints:**
- **A:** [Starting state/what just happened]
- **B:** [Ending state/what must happen by scene end]

**Constraints:**
- [Thing that CANNOT happen]
- [Another constraint]

**Requirements:**
- [Thing that MUST happen]
- [Another requirement]

---

## ON STAGE NOW:

[CURTAIN RISES]

[NARRATOR]: [Setting description in POV character's voice/perspective]

[AS [CHARACTER1], [emotional context/state]]:
[Dialogue and/or internal monologue in their authentic voice]

[AS [CHARACTER2], [emotional context/state]]:
[Their response in their voice]

[NARRATOR]: [Action/description]

[Continue alternating until touchpoint_b achieved...]

[END SCENE]

---

## DIRECTOR NOTES:

**Requirements Met:**
- [ ] [Requirement 1] - [How it was met]
- [ ] [Requirement 2] - [How it was met]

**Constraints Respected:**
- [ ] [Constraint 1] - Verified
- [ ] [Constraint 2] - Verified

**State Changes:**
- [Character1]: [What changed]
- [Character2]: [What changed]

**Seeds Planted:**
- [Foreshadowing element] -> [Future payoff chapter]

**Consequences Propagating:**
- [What carries forward to next scene/chapter]
```

---

## 7. Beat Sheet Template

```markdown
# Chapter [N]: [Chapter Title]

## Overview
- **Timeline:** [Month/Week/Day in story]
- **POV:** [Character]
- **Word Count Target:** [X,XXX]
- **Emotional Arc:** [Start] -> [End]

---

## Scene 1: [Scene Title]

**Location:** [Where]
**Characters:** [Who]
**Time:** [When]

**Touchpoint A:** [Starting state]
**Touchpoint B:** [Ending state]

**Beats:**
1. [What happens first]
2. [What happens next]
3. [Key moment]
4. [Resolution of scene]

**Requirements:**
- [Must include]

**Constraints:**
- [Cannot include]

**Seeds to Plant:**
- [Foreshadowing for ch[N]]

---

## Scene 2: [Scene Title]

[Same structure...]

---

## Scene 3: [Scene Title]

[Same structure...]

---

## Chapter Summary

**What Changed:**
- [Character]: [Change]
- [Relationship]: [Change]

**Knowledge Gained:**
- [Character] learned [fact]

**Threads Advanced:**
- [Thread name]: [Progress]

**Setup for Next Chapter:**
- [What's coming]
```

---

## 8. Evaluator Checklist Template

```markdown
# Evaluator Checklist - Chapter [N]

## Pre-Acceptance Validation

### Phase 1: Entity Extraction
- [ ] List all characters mentioned
- [ ] List all organizations mentioned
- [ ] List all events referenced
- [ ] Note any NEW entities not in catalog

### Phase 2: Canon Warning Check (BLOCKING)
- [ ] No forbidden entity names appear
- [ ] No character deaths that shouldn't happen
- [ ] No timeline violations (events before they occur)

**Check each warning:**
- [ ] [warning_id]: [description] - PASS/FAIL
- [ ] [warning_id]: [description] - PASS/FAIL

### Phase 3: Negative Constraint Check (BLOCKING)
- [ ] No forbidden associations
- [ ] No explicit "NOT TRUE" violations

**Run detection patterns:**
```bash
grep -E "[pattern]" chapter_[N].md
# Result:
```

### Phase 4: Knowledge State Check (FLAG)
- [ ] [Character] only knows what they should at ch[N]
- [ ] No premature secret reveals
- [ ] No references to future events

### Phase 5: Relationship State Check (FLAG)
- [ ] [Relationship] matches documented state
- [ ] Emotional tone consistent

### Phase 6: Timeline Check (FLAG)
- [ ] Events referenced happened before this chapter
- [ ] No anachronisms

### Phase 7: Unknown Entity Check (HUMAN_REVIEW)
- [ ] New character introduced? → [Canonize or Reject]
- [ ] New organization introduced? → [Canonize or Reject]
- [ ] New detail invented? → [Canonize or Reject]

---

## Results

**Overall Result:** [APPROVED | REJECTED | FLAGGED]

**If REJECTED:**
- Violation: [description]
- Evidence: [line reference]
- Required Change: [what to fix]

**If FLAGGED:**
- Flag: [description]
- Recommendation: [approve/reject/modify]
- Human Decision: [pending/approved/rejected]

---

**Evaluator:** [human/auto]
**Date:** [DATE]
**Chapter:** [N]
**Manifest ID:** [manifest reference]
```

---

## 9. Session Document Template

```markdown
# Session Log - [DATE]

## Session Metadata
- **Date:** [DATE]
- **Duration:** [X hours]
- **Chapter(s):** [N]
- **Task:** [Description]
- **Manifest:** [manifest file reference]

---

## Work Completed

### Prose Generated
- Chapter [N], Scene [N]: [X] words
- [Additional work]

### Evaluator Results
- **Result:** [APPROVED/REJECTED/FLAGGED]
- **Violations Fixed:** [list if any]
- **Flags Resolved:** [list if any]

---

## Creative Decisions Made

### Canonical Decisions
1. [Decision]: [What was decided and why]
2. [Decision]: [What was decided and why]

### Voice Calibrations
- [Character]: [Adjustment made]

---

## Errors Discovered

### Errors Caught by Evaluator
1. [Error]: [Description]
   - **Fix Applied:** [What was changed]
   - **Constraint Added:** [If new constraint needed]

### Errors Caught by Human Review
1. [Error]: [Description]
   - **Fix Applied:** [What was changed]

---

## Context Updates Made

### Arc Trackers Updated
- [Character]_Arc_Tracker.md: [What was added]

### Negative Constraints Added
- [Constraint]: [Description]

### Entity Catalog Updated
- [What was added/changed]

---

## Flags for Future Sessions

- [Thing to remember for next session]
- [Unresolved question]

---

## Learnings

- [What worked well]
- [What to do differently]

---

*Session closed: [TIME]*
```

---

## 10. TTRPG Dice Integration Template

```yaml
# TTRPG Scene Definition

scene_id: "[book]_ch[N]_scene[N]_[description]"

# Fixed points (story MUST hit these)
touchpoint_a: "[Starting state]"
touchpoint_b: "[Ending state]"

# Participants
participants: ["[Character1]", "[Character2]"]

# ============================================
# ROLL DEFINITIONS
# ============================================

rolls:

  - roll_id: "[unique_id]"
    type: "[action | consequence | discovery | resource]"
    description: "[What this roll determines]"

    # Modifiers
    base: "d20"
    modifiers:
      - name: "[modifier name]"
        value: [+/- N]
        reason: "[why this modifier applies]"

    # Outcome table
    outcomes:
      critical_success:  # 20
        description: "[Best possible outcome]"
        consequence: "[What happens]"
      success:           # 15-19
        description: "[Clean success]"
        consequence: "[What happens]"
      partial:           # 10-14
        description: "[Success with cost]"
        consequence: "[What happens]"
      failure:           # 5-9
        description: "[Failure, try another way]"
        consequence: "[What happens]"
      critical_failure:  # 1-4
        description: "[Failure with additional problem]"
        consequence: "[What happens]"

  - roll_id: "[another_roll]"
    # ... same structure

# ============================================
# ACTUAL ROLLS (Fill during session)
# ============================================

dice_results:
  - roll_id: "[roll_id]"
    natural_roll: [1-20]
    modifiers_applied: [+/- N total]
    final_result: [N]
    outcome_tier: "[critical_success | success | partial | failure | critical_failure]"
    consequence_applied: "[What actually happened]"

# ============================================
# STATE AFTER ROLLS
# ============================================

character_states_after:
  [character_name]:
    physical:
      injuries: "[any new injuries]"
      resources: "[resource state]"
    emotional: "[emotional state after events]"
    knows:
      - "[new knowledge from this scene]"

# ============================================
# PROPAGATION
# ============================================

propagates_to:
  - scene: "[next scene id]"
    carries: "[what state carries forward]"
```

### Dice Outcome Quick Reference

```
d20 System:
- Critical Success (20):    Best outcome + bonus
- Success (15-19):          Clean success
- Partial Success (10-14):  Success with cost/complication
- Failure (5-9):            Fail, try different approach
- Critical Failure (1-4):   Fail + additional problem

Common Modifiers:
- Skill/Training:     +2 to +5
- Environmental:      -2 to +2
- Equipment:          -2 to +2
- Injury Penalty:     -1 to -3
- Previous Scene:     +/- based on outcome
```

---

## Quick Start Checklist

### New Project Setup

```markdown
- [ ] Create entity_catalog/ENTITY_CATALOG.yaml
- [ ] Create context/negative_constraints.md
- [ ] Create character_arcs/CHARACTER_STATE_INDEX.yaml
- [ ] Create character_arcs/[Name]_Arc_Tracker.md for each major character
- [ ] Create story_bibles/Chapter_[N]_STRUCTURE.md for planned chapters
- [ ] Create manifest template
- [ ] Create evaluator checklist template
```

### Per-Session Workflow

```markdown
1. [ ] Generate manifest from template
2. [ ] Load specified context into LLM
3. [ ] Generate prose using Method Actor format
4. [ ] Run Evaluator checklist
5. [ ] Fix any violations
6. [ ] Update arc trackers
7. [ ] Create session document
8. [ ] Archive manifest
```

---

*Templates Version 1.0 — December 2025*
