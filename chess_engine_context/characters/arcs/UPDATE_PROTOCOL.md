# Character State Update Protocol

**Purpose:** How to maintain arc trackers and the YAML index during prose generation.

---

## When to Update

### During Prose Generation

**After completing each chapter's prose:**
1. Review what actually happened vs. what was planned
2. Update relevant arc trackers if prose deviated from beats
3. Note any new details that should be canon (specific dialogue, locations, etc.)

**After completing each scene:**
- No updates needed unless major deviation from beats

### After Session

**Before ending a writing session:**
1. Update `SESSION_HANDOFF_[DATE].md` with current state
2. Note any tracker updates needed but not yet made
3. Flag any canon inconsistencies discovered

---

## What to Update

### Arc Trackers (`character_arcs/[Name]_Arc_Tracker.md`)

**Update when:**
- Prose adds detail not in tracker (specific dialogue, emotional beats)
- Prose changes planned events
- New relationships or knowledge revealed

**Format:**
- Keep chapter-by-chapter structure
- Add specific quotes if they become key character lines
- Note "As Written" if prose differs from original beat

**Example:**
```markdown
### Chapter 3: Investigations Begin (Month 1, Late)

**As Written:**
- Ahdia's first solo op was to Brazil, not Eastern Europe
- Key line: "If I can help, I should help." (internal)

**State After:**
[updated state reflecting actual prose]
```

### YAML Index (`character_arcs/CHARACTER_STATE_INDEX.yaml`)

**Update when:**
- Knowledge states change (who knows what, when)
- Relationship states change
- Timeline/chapter mapping needs correction
- New canon warnings identified

**What NOT to update:**
- Don't add every prose detail to YAML
- YAML is for queryable state, not prose notes
- Keep it structural, not narrative

---

## Update Workflow

### Step 1: After Writing Chapter Prose

```
1. Read completed chapter prose
2. Compare to beat sheet and arc trackers
3. Note deviations in a "Prose Notes" section
4. Update arc trackers with "As Written" details
5. Update YAML only if:
   - Knowledge states changed
   - Timeline mapping changed
   - New canon warning needed
```

### Step 2: Cross-Character Consistency Check

```
For each chapter completed:
1. Check: Who was present?
2. Check: What did each character learn?
3. Check: Did any relationships change?
4. Update each affected character's tracker
5. Update YAML knowledge_tracking if needed
```

### Step 3: Session Handoff

```
Before ending session:
1. Create/update SESSION_HANDOFF_[DATE].md
2. List: Chapters completed
3. List: Tracker updates made
4. List: Tracker updates still needed
5. List: Any canon questions raised
```

---

## File Locations

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `character_arcs/[Name]_Arc_Tracker.md` | Detailed character state | After each chapter |
| `character_arcs/CHARACTER_STATE_INDEX.yaml` | Queryable state index | When structure changes |
| `story_bibles/book 2/SESSION_HANDOFF_[DATE].md` | Session continuity | End of each session |
| `story_bibles/book 2/CHANGELOG.md` | Major decisions | When canon decisions made |

---

## Canon Conflict Resolution

**If prose contradicts tracker:**
1. Prose is canon (what's written is what happened)
2. Update tracker to match prose
3. Note the change in CHANGELOG.md
4. Check for ripple effects on other characters

**If prose contradicts YAML:**
1. Update YAML to match prose
2. Run YAML validation: `python3 -c "import yaml; yaml.safe_load(open('CHARACTER_STATE_INDEX.yaml'))"`
3. Check knowledge_tracking for consistency

**If prose contradicts beat sheet:**
1. Prose is canon
2. Update beat sheet to reflect what was written
3. Check downstream beats for conflicts

---

## Quick Reference: What Lives Where

**Arc Trackers contain:**
- Emotional progression
- Key dialogue/lines
- Scene-by-scene state
- Relationship evolution
- "As Written" notes

**YAML Index contains:**
- Timeline mapping
- Knowledge states (who knows what, when)
- Canon warnings
- Relationship matrix (structural, not emotional)
- Queryable cross-references

**Beat Sheets contain:**
- Scene plans
- Dialogue suggestions
- Action sequences
- Pacing notes

**Prose contains:**
- Canon (what actually happened)
- Final authority on all disputes

---

## Example: Completing Chapter 1 Prose

```
1. Write Chapter 1 prose
2. Review: Did Ahdia actually freeze for 47 minutes?
   - Yes → No update needed
   - No, it was 32 minutes → Update Ahdia tracker, YAML baseline numbers
3. Review: Did she save Korede specifically?
   - Yes → No update needed
   - Different person → Update Ahdia and Korede trackers
4. Review: Any new canon details?
   - She said "This is insane" three times → Add to tracker as key pattern
5. Update SESSION_HANDOFF with completion status
```

---

## Validation Checklist

Before marking a chapter "complete":

- [ ] All present characters' trackers updated
- [ ] Knowledge states verified (who learned what)
- [ ] Relationship changes noted
- [ ] Any new canon warnings added to YAML
- [ ] Session handoff updated
- [ ] YAML validates (no syntax errors)

---

## Session End: Quiz Generation

**Purpose:** Force active recall for next Claude instance. Passive reading ≠ understanding.

### When to Generate

At the end of every significant session, create a quiz covering:
- Critical canon decisions made
- Character state changes
- Plot points that could cause continuity errors if misunderstood
- Any "NEVER do this" constraints established

### Quiz Format

**File:** `story_bibles/book N/SESSION_QUIZ_[DATE].md`

```markdown
# Session Quiz: [DATE]

**Instructions:** Answer these questions BEFORE proceeding with prose generation.
Wrong answers = re-read the referenced documents.

---

## Canon Questions

1. [Question about critical plot point]
   - Reference: [file to check if wrong]

2. [Question about character state]
   - Reference: [file to check if wrong]

3. [Question about constraint/warning]
   - Reference: [file to check if wrong]

---

## Character Voice Questions

4. [Quote a key line and ask which character said it / why it matters]

5. [Ask about a character's hidden motive or knowledge gap]

---

## Both/And Questions

6. [Question requiring nuanced answer, not binary]
   - Example: "Why did Ahdia's sacrifice both succeed AND fail?"

---

## Answers

<details>
<summary>Click to reveal answers (try first!)</summary>

1. [Answer]
2. [Answer]
3. [Answer]
4. [Answer]
5. [Answer]
6. [Answer]

</details>
```

### Quiz Question Types

**Canon Protection:**
- "Who killed [character]?" (prevents attribution errors)
- "What is the company name?" (prevents outdated terminology)
- "What CAN'T [character] do?" (prevents constraint violations)

**State Verification:**
- "What percentage baseline does Ahdia have at [point]?"
- "Who knows about [secret] by Chapter [N]?"
- "What is [character]'s relationship with [character] at [point]?"

**Voice Verification:**
- "What phrase does Victor use for both/and thinking?"
- "How does Ahdia cope with cosmic horror?" (TV references)
- "What's Ryu's hidden motive that drives his enablement?"

**Thematic Understanding:**
- "Why does the CBT approach fail in Books 1-4?"
- "What does 'you don't have to be fixed to be worthy' mean for [character]?"

### Quiz Difficulty

Aim for:
- 3-4 "must get right or stop" questions (critical canon)
- 2-3 "should know" questions (character understanding)
- 1-2 "deep understanding" questions (thematic/both-and)

### Failed Quiz Protocol

If next instance gets answers wrong:
1. Do NOT proceed with generation
2. Re-read referenced documents
3. Acknowledge the correction in response
4. Try quiz again or ask for clarification

---

**Last Updated:** 2025-12-07
