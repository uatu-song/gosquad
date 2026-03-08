# Book 2 Prose Generation Guide

**Purpose:** Everything an LLM needs to generate prose for Go Squad Book 2.

**Last Updated:** 2026-02-15

---

## Quick Start

### Before Writing ANY Chapter

```bash
# 1. Load current session context
Read GO_SQUAD_SESSION_HANDOFF.md

# 2. Query character states for the chapter you're writing
cd _tools/perspective_engine
python engine.py chapter -ch [NUMBER]

# 3. Read the chapter outline
Read 5_story_bibles/book_2/structure/Chapter_[N]_OUTLINE.md
# (If no OUTLINE exists, use Chapter_[N]_STRUCTURE.md)

# 4. Check canon warnings
python engine.py know -c [POV_CHARACTER] -ch [NUMBER]
```

---

## Reference Files (Priority Order)

### 1. Session Handoff (Start Here)
`GO_SQUAD_SESSION_HANDOFF.md`
- Current project state
- Canon warnings (CRITICAL—check every time)
- Recent decisions
- What to remember

### 2. Book 2 Canon
`5_story_bibles/book_2/CANON.md`
- Character states
- Timeline
- What each character knows when
- Relationship states

### 3. Book 2 Claude Guide
`5_story_bibles/book_2/CLAUDE.md`
- Book 2 structure overview
- Educational mission
- Quality checks
- The tragedy engine

### 4. Chapter Structure
`5_story_bibles/book_2/structure/Chapter_[N]_OUTLINE.md` or `Chapter_[N]_STRUCTURE.md`
- Scene-by-scene beats
- Touchpoints A→B
- Emotional arc
- Prose notes

### 5. Character Voices
`2_method_actor/stewards/[Character]_Steward.md`
- Voice patterns
- Internal monologue style
- What they know/don't know
- Arc position

### 6. Perspective Engine Queries
```bash
python engine.py know -c [char] -ch [num]    # What character knows
python engine.py chapter -ch [num]            # Full chapter context
python engine.py relationship -c [char1] --char2 [char2] -ch [num]
python engine.py secrets -ch [num]            # Active secrets
```

---

## Canon Warnings (Memorize These)

### Critical (Check Every Time)

| Warning | Details |
|---------|---------|
| **READER IS FOOLED** | Reader believes Ahdia is depressed/grieving until Ruth's discovery. No Ahdia secret-ops POV until after reveal. |
| **Ahdia appears fridged** | She's shown as absent, depressed, withdrawing. News tickers (dictators vanishing, crises averted) are seeds—reader doesn't connect them to Ahdia. |
| **Ruth discovers at END** | Final pages of Book 2. Ruth finds Ahdia passed out, TV playing Exile Island. This is the reveal. |
| **Flashback retrospective AFTER reveal** | Ahdia's actual ops (Secret Superman content) shown as flashback AFTER Ruth discovers. Not before. |
| **37 dictators** | On Exile Island. Not 28. |
| **Team does NOT know** | About Exile Island until Book 3 (Ruth/Ryu discover end of Book 2, team learns Book 3). |
| **Tess does NOT kill Webb** | Brutalizes but leaves alive. |
| **Victor has NO dead wife** | Partner is Leah. No "Clara." |
| **Ryu NEVER confesses love** | To Ahdia in Book 2. Reader infers, Ahdia doesn't know. |
| **Bourn is a WOMAN** | She/her pronouns always. |
| **Eidolon AMPLIFIES fear** | Cannot create new fears. |
| **Leah is a barista** | NOT harassment investigator. |

### Reader vs Character Knowledge

**CRITICAL DISTINCTION:**
- **Reader** believes Ahdia is depressed/absent until Ruth's discovery (end of book)
- **Team** believes Ahdia is depressed/absent until Book 3
- **Ruth/Ryu** discover truth at end of Book 2
- News ticker seeds (dictators vanishing, arms deals collapsing) are visible to reader but not connected to Ahdia

### Character Knowledge Gates

Use Perspective Engine to verify, but key gates:

| Secret | Who Knows | Reader Learns | Characters Learn |
|--------|-----------|---------------|------------------|
| Exile Island ops | Ahdia, Ryu | End of Book 2 (Ruth discovers) | Ruth/Ryu: End Book 2. Team: Book 3. |
| Ahdia terminal decline | Ahdia, Ryu, Ruth | Ch7 (Ruth learns) | Ch7 |
| Father's complicity | Tess | Ch8 (confirms) | Ch8 |
| Tess attacks Webb | Tess only | Never in Book 2 | Never in Book 2 |

---

## Prose Style

### Ahdia's Voice (Protagonist)

```
✓ Casual/contemporary ("What the actual hell?")
✓ Self-correction: "[Statement]. Or rather, [correction]?"
✓ Rambling run-ons when stressed
✓ Deadpan acceptance of absurd situations
✓ TV/movie processing of real events
✓ Specific details over generic ("Thursday nights on SyFy" not "TV shows")
```

### Ensemble Voice (Book 2 Focus)

Book 2 is ensemble-focused. Ruth, Ben, Tess, Victor, Leah, Leta carry narrative while Ahdia appears "grieving."

Each character has distinct voice patterns in their Steward files:
- `2_method_actor/stewards/Ruth_Carter_Steward.md`
- `2_method_actor/stewards/Tess_Whitford_Steward.md`
- etc.

### General Style

- **No purple prose.** Contemporary, direct.
- **Specificity over vagueness.** Concrete details.
- **Dialogue reads aloud naturally.** Test it.
- **Humor is coping, not dismissal.** Stakes remain real.
- **Powers described viscerally.** Not technical manuals.

---

## Chapter Outline Format

Each OUTLINE file contains:

```markdown
# Chapter N: "Title"

**Month:** X
**Emotional Arc:** State A → State B → State C

## SCENE 1: [Name]
**Location:** Where
**Present:** Who
**Tone:** How it feels

### Touchpoint A
[Starting emotional/plot state]

### Beats
1. [Specific action/dialogue moment]
2. [Next moment]
...

### Touchpoint B
[Ending emotional/plot state for scene]

## SCENE 2: ...

## CHAPTER CLOSE
[Final image/line]

## PROSE NOTES
[Specific guidance for this chapter]
```

### How to Use

1. **Touchpoint A→B** defines the scene's emotional journey
2. **Beats** are guideposts, not scripts—expand naturally
3. **Prose Notes** contain chapter-specific warnings
4. **Maintain arc** through scenes—each builds on previous

---

## The Tragedy Engine

Book 2 plants seeds for devastation. Every chapter should:

1. **Advance surface plot** (investigations, team ops)
2. **Plant tragedy seeds** (Leta's death, Ben's breakdown, Ruth's limits)
3. **Maintain "fridging" illusion** (Ahdia appears broken)
4. **Serve theme** ("You don't have to be fixed to be worthy")

### Undercurrent Question

Throughout Book 2, underneath everything: **"Why didn't you save her?"**

- Ahdia: Guilt about Geneva, team, everyone
- Ruth: Firas (Book 1), Ahdia (enabling), triage limits
- Ben: Sarah (wife), eventually the election
- Tess: Leta (warning wasn't enough)
- Leah: Leta (silence enabled harassment)

This question isn't stated—it's felt.

---

## Current Prose Status

**Chapters with prose:** 1-10
**Next chapter:** 11 "Coordinated"

### Chapter 11-12 Sequence

These form a two-chapter action sequence:

| Chapter | File | Arc |
|---------|------|-----|
| 11 | `Chapter_11_OUTLINE.md` | Confidence → Chaos → Paralysis |
| 12 | `Chapter_12_OUTLINE.md` | Choice → Consequences → Reckoning |

**Ch11 ends:** Ruth frozen, all sites failing, impossible choice
**Ch12 opens:** Ruth's triage call (the climax)

---

## Prose Generation Workflow

### Phase 1: Context Loading

1. Read `GO_SQUAD_SESSION_HANDOFF.md`
2. Read chapter OUTLINE file
3. Query Perspective Engine for character states
4. Read relevant Steward files for POV characters

### Phase 2: Scene-by-Scene Writing

For each scene in the outline:

1. **Establish Touchpoint A** — Where are we emotionally/plot-wise?
2. **Expand beats** — Turn bullet points into prose
3. **Maintain voice** — Check against character patterns
4. **Land Touchpoint B** — Complete the scene's emotional movement
5. **Transition** — Set up next scene

### Phase 3: Quality Check

Before finalizing:

- [ ] Character knowledge correct? (They don't know what they shouldn't)
- [ ] Voice consistent? (Sounds like this person)
- [ ] Emotional arc complete? (Scene moves from A to B)
- [ ] Specificity? (Concrete details, not vague)
- [ ] Stakes maintained? (Humor doesn't dismiss danger)
- [ ] Canon respected? (Check warnings)

### Phase 4: Output

Save prose to: `6_manuscript/book_2/chapter_[NN].md`

---

## Tools Available

### Perspective Engine

```bash
cd _tools/perspective_engine

# What does character know at chapter?
python engine.py know -c tess -ch 12

# Who is present in chapter?
python engine.py present -ch 21

# Find overlap moments (multi-character scenes)
python engine.py overlaps

# Get relationship state
python engine.py relationship -c ahdia --char2 ruth -ch 13

# Get active secrets
python engine.py secrets -ch 8

# Full chapter summary
python engine.py chapter -ch 21

# Export character scaffold
python engine.py scaffold -c tess
```

### Prose Indexer (Post-Writing)

```bash
cd _tools/prose_indexer

# Check for AI slop (banned names, patterns)
python prose_indexer.py slop --book 2

# Index entities
python prose_indexer.py ingest --book 2
```

### Visualization

Open `book2_perspective_engine.html` in browser for timeline view.

---

## Common Mistakes to Avoid

### Knowledge Violations
- Character acts on information they don't have yet
- **Fix:** Query `engine.py know -c [char] -ch [num]` before writing

### Voice Drift
- Character sounds generic or like another character
- **Fix:** Re-read their Steward file, check dialogue aloud

### Purple Prose
- Flowery descriptions, overwrought emotion
- **Fix:** Cut adjectives, use concrete actions

### Stakes Dismissal
- Humor undermines danger, trauma treated lightly
- **Fix:** Humor as coping mechanism, stakes stay real

### Canon Violations
- Dead wife for Victor, Tess kills Webb, wrong dictator count
- **Fix:** Check warnings list before writing

### Rushing Emotional Beats
- Major moments happen too fast, no landing zone
- **Fix:** Let scenes breathe, especially debrief/processing scenes

---

## Book 2 Emotional Map

| Chapters | Phase | Team State |
|----------|-------|------------|
| 1-5 | Confident operators | "We've got this" |
| 6-10 | Cracks forming | Investigations, secrets, strain |
| 11-15 | Crisis revealed | Limits exposed, can't save everyone |
| 16-20 | Fighting the system | Evidence fails, faith shatters |
| 21-24 | Tragedy and survival | Leta dies, election lost, team endures |

### Key Emotional Beats

- **Ch7:** Ruth discovers Ahdia's decline severity
- **Ch11-12:** Team learns they can't save everyone
- **Ch13:** Exile Island exposed to team (Ruth's discovery is END of book, not here)
- **Ch17:** Eidolon reframes evidence, Kain +12 points
- **Ch23:** Leta killed by Webb (Month 11 manhunt), Tess witnesses
- **Ch24:** Election night, reactor crisis, Prime reveals herself

---

## Starting a Session

### Prompt Template

```
Read GO_SQUAD_SESSION_HANDOFF.md to get current status.

Today I'm writing Chapter [N] prose.

Load context:
1. Read 5_story_bibles/book_2/structure/Chapter_[N]_OUTLINE.md
2. Query: python engine.py chapter -ch [N]
3. Read Steward files for POV characters

Then begin prose generation scene by scene.
```

### Mid-Session Checks

Every few scenes, verify:
- Still following outline arc?
- Character voices consistent?
- No canon violations crept in?

### Session Close

After writing:
1. Save prose to `6_manuscript/book_2/chapter_[NN].md`
2. Run `prose_indexer.py slop --book 2`
3. Note any decisions/changes in handoff file

---

## Summary

**The work is:**
1. Load context (handoff, outline, character states)
2. Write scene-by-scene following touchpoint structure
3. Maintain voice, verify knowledge, respect canon
4. Let emotional beats breathe
5. Check quality, save, index

**The tools are:**
- `GO_SQUAD_SESSION_HANDOFF.md` — Current state
- `Chapter_[N]_OUTLINE.md` — Scene structure
- `engine.py` — Character knowledge queries
- Steward files — Voice patterns
- `CANON.md` — Ground truth

**The goal is:**
Prose that sounds like these specific people, navigating impossible situations, planting seeds for tragedy while maintaining hope—because you don't have to be fixed to be worthy.

---

**Ready to write.**
