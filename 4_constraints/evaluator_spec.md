# EVALUATOR SPECIFICATION
# Version: 1.0
# Purpose: Define validation logic that gates scratchpad -> memory transitions

---

## Overview

The Evaluator is the **gatekeeper** between generated output and persistent canon. Nothing becomes memory until the Evaluator approves it.

**Core Principle:** Validate BEFORE accepting output, not after damage propagates.

---

## Evaluation Pipeline

```
Generated Output
       │
       ▼
┌──────────────────┐
│ Phase 1: Extract │  Extract entities from prose
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 2: Canon   │  BLOCKING - Hard errors
│ Warning Check    │  Auto-reject if violated
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 3: Negative│  BLOCKING - Explicit NOT TRUE
│ Constraint Check │  Auto-reject if violated
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 4: Knowledge│  FLAG - Who knows what when
│ State Check      │  Flag for review
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 5: Relation-│  FLAG - Emotional consistency
│ ship State Check │  Flag for review
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 6: Timeline│  FLAG - Chronological errors
│ Check            │  Flag for review
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Phase 7: Unknown │  HUMAN REVIEW - New entities
│ Entity Check     │  Require human decision
└────────┬─────────┘
         │
         ▼
    ┌─────────┐
    │ Result  │
    └────┬────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
APPROVED   REJECTED   FLAGGED
    │         │          │
    ▼         ▼          ▼
  Canon    Revise    Human
  Update   Prose     Review
```

---

## Phase Definitions

### Phase 1: Entity Extraction

**Purpose:** Build inventory of what the prose contains

**Extracts:**
- Characters mentioned (by name, codename, or pronoun resolution)
- Relationships implied (interactions, dialogue, descriptions)
- Knowledge states implied (what characters reference knowing)
- Timeline references (dates, "months ago", "yesterday")
- Locations (named places, settings)
- Events (actions taken, things that happen)
- New entities (names/concepts not in existing canon)

**Output:** `entities.yaml` (session-scoped, not persisted)

```yaml
entities:
  characters:
    - name: "Ahdia"
      mentions: [12, 45, 78, ...]  # Line numbers
      actions: ["translocates to Brazil", "speaks with Ryu"]
    - name: "Ruth"
      mentions: [23, 56]
      actions: ["monitors baseline readings"]

  relationships:
    - characters: [ahdia, ruth]
      type: "strained interaction"
      evidence: "Ruth's clipped responses, line 34"

  knowledge_references:
    - character: "ahdia"
      references: "global operation scope"
      line: 67

  new_entities:
    - name: "Dr. Elara Chen"
      type: "character"
      line: 89
      context: "introduced as facility administrator"
```

---

### Phase 2: Canon Warning Check

**Severity:** BLOCKING
**Action on Fail:** REJECT output, require revision

**Method:**
1. Load `canon_warnings` from CHARACTER_STATE_INDEX.yaml
2. For each warning in `manifest.validation.canon_warnings_active`:
3. Check extracted entities against warning conditions
4. If violated, REJECT immediately

**Canon Warnings (Current):**

| ID | Check | Violation Condition |
|----|-------|---------------------|
| `tess_no_kill` | Tess + kill action + Webb | Tess kills or murders Webb |
| `isaiah_killer` | Isaiah death attribution | Anyone other than Webb credited |
| `company_name` | Company name usage | "Titan Strategic" appears |
| `firas_status` | Firas death reference | Firas described as dead |

**Output on Violation:**
```yaml
result: REJECTED
phase: "canon_warning_check"
violation:
  warning_id: "tess_no_kill"
  evidence: "Line 234: 'Tess watched the life leave Webb's eyes'"
  required_change: "Webb must survive. Tess brutalizes but does not kill."
  reference: "context/negative_constraints.md#TESS + WEBB"
```

---

### Phase 3: Negative Constraint Check

**Severity:** BLOCKING
**Action on Fail:** REJECT output, require revision

**Method:**
1. Load `context/negative_constraints.md`
2. For each character in extracted entities:
3. Load character-specific constraints
4. Check for violation patterns

**Pattern Matching (v1 - Regex):**

```yaml
constraints:
  victor_not_widower:
    patterns:
      - "Victor.*(wife|widow|Clara|married|bereaved)"
      - "his late wife.*Victor"
      - "Victor.*mourning.*wife"
    exceptions:
      - "Victor.*Leah"  # Partner is fine
      - "Victor.*partner"
    action: "REJECT - Victor is NOT a widower, has NO dead wife"

  ben_wife_unspecified:
    patterns:
      - "Sarah.*(protest|riot|demonstration|police|shot)"
      - "Ben.*wife.*(killed at|died at|murdered at)"
    action: "REJECT - Sarah's death cause is UNSPECIFIED"

  tess_already_knows:
    patterns:
      - "Tess.*(realizes|discovers|learns|finds out).*father.*(corrupt|guilty|complicit)"
    context: "Only valid if discovering SCOPE, not BASE corruption"
    action: "FLAG - Verify Tess is discovering scope, not base corruption"

  bourn_gender:
    patterns:
      - "Bourn.*(he|him|his|man|guy|gentleman)"
    action: "REJECT - Bourn is a woman, use she/her"

  ryu_confession:
    patterns:
      - "Ryu.*(confess|admit|tell|reveal).*love.*Ahdia"
      - "Ahdia.*(knew|realized|understood).*Ryu.*love"
    action: "REJECT - Ryu's feelings are not revealed in Book 2"
```

**Pattern Matching (v2 - Entity-Based, Future):**

```yaml
constraints:
  victor_not_widower:
    entity_check: true
    if_entity: "Victor"
    forbidden_associations:
      relationships: [wife, widow, married, bereaved]
      names: [Clara]
    allowed_associations:
      relationships: [partner, girlfriend]
      names: [Leah]
```

---

### Phase 4: Knowledge State Check

**Severity:** FLAG
**Action on Fail:** Flag for human review, do not auto-reject

**Method:**
1. Load `knowledge_tracking` from CHARACTER_STATE_INDEX.yaml
2. Get current chapter from manifest
3. For each character's knowledge references (from Phase 1):
4. Check if character should know that information at this chapter
5. Flag discrepancies

**Example Check:**
```yaml
# Manifest says chapter 9
# Entity extraction found: Ruth references "Ahdia's exile island operations"

# Check knowledge_tracking.exile_island.awareness.ch9
# Result: [ahdia, ryu] - Ruth is NOT in awareness list

flag:
  type: "knowledge_state_violation"
  severity: "FLAG"
  character: "Ruth"
  knowledge: "exile_island"
  current_chapter: 9
  learns_chapter: 13
  evidence: "Line 156: Ruth asks about 'the island operation'"
  suggested_resolution: "Ruth should not know about Exile Island until ch13"
```

---

### Phase 5: Relationship State Check

**Severity:** FLAG
**Action on Fail:** Flag for human review

**Method:**
1. Load `relationships` matrix from CHARACTER_STATE_INDEX.yaml
2. Get current chapter from manifest
3. For each relationship interaction (from Phase 1):
4. Check if emotional tone matches established state
5. Flag inconsistencies

**Example Check:**
```yaml
# Manifest says chapter 9
# Entity extraction found: Ahdia and Ruth interact warmly, joking

# Check relationships.ahdia_ruth.progression
# ch7: { state: "strained", notes: "ruth_discovers_lies" }
# ch13: { state: "rebuilding" }
# Chapter 9 is between 7 and 13, state should be "strained"

flag:
  type: "relationship_state_inconsistency"
  severity: "FLAG"
  relationship: "ahdia_ruth"
  expected_state: "strained"
  found_tone: "warm, joking"
  evidence: "Lines 45-67: Banter between Ahdia and Ruth"
  suggested_resolution: "Interaction should reflect strain from ch7 discovery"
```

---

### Phase 6: Timeline Check

**Severity:** FLAG
**Action on Fail:** Flag for human review

**Method:**
1. Get current chapter/month from manifest
2. For each timeline reference (from Phase 1):
3. Verify referenced events are in correct chronological position
4. Flag future references or incorrect past references

**Checks:**
- No references to events that haven't happened yet
- Past event timing is accurate
- "X months ago" math is correct

**Example Check:**
```yaml
# Manifest says chapter 9, month 4
# Entity extraction found: Reference to "Ben's leak last month"

# Check timeline: Ben's leak is ch15, month 8
# Month 4 is BEFORE month 8

flag:
  type: "timeline_violation"
  severity: "FLAG"
  reference: "Ben's leak"
  current_month: 4
  event_month: 8
  evidence: "Line 234: 'After Ben's leak last month...'"
  suggested_resolution: "Ben's leak hasn't happened yet. Remove reference."
```

---

### Phase 7: Unknown Entity Check

**Severity:** HUMAN_REVIEW
**Action:** Pause for human decision

**Method:**
1. Compare extracted entities against CHARACTER_STATE_INDEX.yaml
2. For any entity not found in existing canon:
3. Flag for human review
4. Require explicit decision: add to canon or reject

**Example:**
```yaml
flag:
  type: "unknown_entity"
  severity: "HUMAN_REVIEW"
  entity:
    name: "Dr. Elara Chen"
    type: "character"
    first_mention: "Line 89"
    context: "Introduced as facility administrator"

  decision_required:
    - option: "approve_as_canon"
      action: "Add to CHARACTER_STATE_INDEX.yaml, create arc tracker stub"
    - option: "reject"
      action: "Remove from prose, use existing character or generic"
    - option: "flag_for_later"
      action: "Allow in prose, defer canonization decision"
```

---

## Evaluation Output

### APPROVED

```yaml
result: APPROVED
timestamp: "2025-12-10T16:45:00Z"
manifest_id: "2025-12-10_chapter09_prose"
evaluator_version: "1.0"

phases_passed:
  - canon_warning_check
  - negative_constraint_check
  - knowledge_state_check
  - relationship_state_check
  - timeline_check
  - unknown_entity_check

action: "Output may be committed to canon"
next_steps:
  - "Update arc trackers with 'As Written' notes"
  - "Archive manifest with output_lineage"
  - "Run SESSION_HANDOFF update"
```

### REJECTED

```yaml
result: REJECTED
timestamp: "2025-12-10T16:45:00Z"
manifest_id: "2025-12-10_chapter09_prose"
evaluator_version: "1.0"

failed_phase: "negative_constraint_check"
violations:
  - constraint: "victor_not_widower"
    evidence: "Line 45: 'Victor thought of Clara, gone these eight months'"
    required_change: "Remove Clara reference. Victor is not a widower."
    reference: "context/negative_constraints.md#VICTOR HERNANDEZ"

action: "Output must be revised"
next_steps:
  - "Make required changes"
  - "Re-run Evaluator"
  - "Do NOT commit to canon until APPROVED"
```

### FLAGGED

```yaml
result: FLAGGED
timestamp: "2025-12-10T16:45:00Z"
manifest_id: "2025-12-10_chapter09_prose"
evaluator_version: "1.0"

blocking_passed: true  # No BLOCKING violations
flags:
  - type: "relationship_state_inconsistency"
    severity: "FLAG"
    details: "Ahdia/Ruth interaction warmer than expected for ch9"
    confidence: 0.7  # How likely this is a real error
    suggested_resolution: "Add tension to dialogue, or justify warmth"

  - type: "unknown_entity"
    severity: "HUMAN_REVIEW"
    details: "Dr. Elara Chen introduced"
    decision_options: ["approve_as_canon", "reject", "flag_for_later"]

action: "Human review required"
next_steps:
  - "Review each flag"
  - "Make decisions on HUMAN_REVIEW items"
  - "Revise prose if FLAG items are actual errors"
  - "Re-run Evaluator after changes"
  - "Commit to canon only after all flags resolved"
```

---

## Implementation Notes

### v1 Implementation (Recommended Start)

1. **Manual Evaluator:** Human runs through checklist
2. **Regex-based pattern matching** for negative constraints
3. **Manual knowledge state verification** against YAML
4. **Spreadsheet or markdown for flag tracking**

### v2 Implementation (Future)

1. **Script-based Evaluator** with YAML config
2. **Entity extraction** using NLP or LLM
3. **Automated knowledge state queries** against structured data
4. **Dashboard for flag management**

### v3 Implementation (Ideal)

1. **Integrated into Claude Code workflow**
2. **Real-time constraint checking** during generation
3. **Auto-suggest corrections** for common violations
4. **Lineage tracking database**

---

## Human Review Protocol

When Evaluator returns FLAGGED:

```markdown
## Flag Review: [session_id]

### Flag 1: [type]
**Severity:** FLAG / HUMAN_REVIEW
**Evidence:** [quoted text, line number]
**Concern:** [why flagged]
**Suggested Resolution:** [options]

**Decision:**
- [ ] Approve as-is (explain why flag is false positive)
- [ ] Revise prose (make specific change)
- [ ] Add to negative constraints (new constraint needed)

**Resolution Notes:** [what was decided and why]
```

After all flags resolved:
1. Update manifest with `output_lineage.resolved_flags`
2. Re-run Evaluator if prose was changed
3. Only commit to canon after APPROVED result

---

## Evaluator Maintenance

### Adding New Checks

When new error patterns are discovered:

1. Determine appropriate phase (canon warning, negative constraint, knowledge, etc.)
2. Add check definition to relevant phase
3. Add detection patterns
4. Test against known good and bad examples
5. Update this spec

### Versioning

Increment evaluator version when:
- New phases added
- Check logic changes
- Pattern definitions modified

Track version in manifest and evaluation output for audit trail.

---

*Last Updated: 2025-12-10*
*Version: 1.0*
