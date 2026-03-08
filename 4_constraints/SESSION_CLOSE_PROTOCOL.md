# SESSION CLOSE PROTOCOL
# Version: 1.0
# Purpose: Ensure session context graduates to persistent memory before chat ends

---

## Why This Exists

Chat context is transient:
- Fills up and gets summarized
- Creative decisions made in chat are lost
- Methodology refinements disappear
- The next Claude instance starts fresh

**This protocol ensures scratchpad → memory graduation.**

---

## When to Run This Protocol

Run **before ending any significant session** where:
- Creative decisions were made
- New constraints were identified
- Errors were corrected
- Infrastructure was created/modified
- Prose was written
- Character/arc understanding deepened

**Rule of thumb:** If you'd be frustrated recreating this context, capture it now.

---

## Session Close Checklist

### 1. Creative Decisions Capture

**Ask:** What decisions were made this session that future sessions need to know?

```markdown
## Creative Decisions (LOCKED)

### [Decision Category]
- **Decision:** [What was decided]
- **Rationale:** [Why - so future sessions don't reverse it]
- **Implications:** [What this affects]
```

**Common categories:**
- Character arc directions
- Plot structure decisions
- Pacing decisions (what NOT to add)
- Voice/tone decisions
- Relationship clarifications

### 2. Error Correction Capture

**Ask:** What errors were found and fixed this session?

```markdown
## Errors Corrected

### [Error Name]
- **What was wrong:** [The error]
- **What is correct:** [The fix]
- **Files updated:** [List]
- **Added to negative_constraints.md:** Yes/No
```

**If error was significant:** Add to `context/negative_constraints.md` immediately.

### 3. Infrastructure Changes

**Ask:** What files were created, modified, or deleted?

```markdown
## Infrastructure Changes

### Created
- `/path/to/file.md` - [purpose]

### Modified
- `/path/to/file.md` - [what changed]

### Deleted
- `/path/to/file.md` - [why]
```

### 4. Current State Capture

**Ask:** What is the state of the work right now?

```markdown
## Current State

### Manuscript
| Chapter | Words | Status |
|---------|-------|--------|
| ... | ... | ... |

### Ready for Next Session
- [What's scaffolded/prepared]

### Blocked/Needs Decision
- [What can't proceed without input]
```

### 5. Knowledge Transfer

**Ask:** What would the next Claude instance need to reconstruct this session's understanding?

```markdown
## Files to Load for Reconstruction

1. [File path] - [why needed]
2. [File path] - [why needed]
...
```

### 6. Next Steps

**Ask:** What should the next session do?

```markdown
## Next Session Tasks

### Immediate
1. [Task]

### If Time Permits
1. [Task]

### Blocked Until
1. [Task] - blocked by [reason]
```

---

## Document Types

### SESSION_LOG vs SESSION_HANDOFF

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `SESSION_LOG_[DATE].md` | Comprehensive session record | Infrastructure, methodology, multi-topic sessions |
| `SESSION_HANDOFF_[DATE].md` | Prose-focused handoff | Writing sessions, character development |
| `SESSION_HANDOFF_[DATE]_END.md` | End-of-day summary | When multiple sessions in one day |

**Multiple sessions per day:** Add qualifier (Morning, Evening) or use `_END` suffix.

### Location

All session documents go in: `/story_bibles/book 2/`

---

## Quick Close Template

For fast session closure, copy and fill:

```markdown
# SESSION [LOG/HANDOFF]: [DATE] [(qualifier if needed)]

## Session Focus
[One sentence summary]

## Creative Decisions (LOCKED)
- [Decision 1]
- [Decision 2]

## Errors Corrected
- [Error → Fix]

## Files Changed
- Created: [list]
- Modified: [list]

## Current State
[Brief status]

## Next Session
1. [Priority task]

## Load for Reconstruction
1. [This file]
2. [Key reference]
3. [Relevant arc tracker]
```

---

## The Negative Constraints Update

**CRITICAL:** If any of these occurred, update `context/negative_constraints.md`:

- [ ] Claude invented something that isn't true
- [ ] A character fact was wrong (relationships, deaths, knowledge)
- [ ] A timeline error occurred
- [ ] A constraint was violated

**Don't wait.** Add to negative constraints while context is fresh.

---

## Session Quiz Generation

For significant sessions, generate a quiz (see `UPDATE_PROTOCOL.md`):

```markdown
# SESSION QUIZ: [DATE]

## Canon Questions
1. [Question about critical decision]
   - Reference: [file to check]

## Character Questions
2. [Question about character state/knowledge]

## Constraint Questions
3. [Question about what is NOT true]
```

**Purpose:** Force active recall for next Claude instance. Passive reading ≠ understanding.

---

## Integration with Context Engineering System

This protocol is part of the larger system:

```
DURING SESSION
├── Chat context (scratchpad)
├── Decisions being made
└── Understanding accumulating

SESSION CLOSE (this protocol)
├── Capture decisions
├── Update negative constraints
├── Create session document
└── Scratchpad → Memory

NEXT SESSION START
├── Load session document
├── Load negative constraints
├── Load relevant arc trackers
└── Full context reconstructed
```

---

## Common Mistakes

### 1. "I'll remember this"
No you won't. The next Claude instance is fresh. Write it down.

### 2. "It's in the chat history"
Chat history gets summarized. Details are lost. Write it down.

### 3. "The files capture everything"
Files capture *what*, not *why*. Decisions need rationale. Write it down.

### 4. "This session was too short"
Even short sessions can have critical decisions. Check before closing.

### 5. "I'll update negative constraints later"
You'll forget. Add errors to negative constraints immediately.

---

## Protocol Summary

1. **Capture** creative decisions with rationale
2. **Record** errors corrected
3. **List** infrastructure changes
4. **Document** current state
5. **Specify** files needed for reconstruction
6. **Define** next session tasks
7. **Update** negative constraints if needed
8. **Generate** quiz if significant session

**The goal:** Next Claude instance can continue without losing momentum.

---

*Last Updated: 2025-12-10*
*Version: 1.0*
