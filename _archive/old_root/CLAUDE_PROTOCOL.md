# Claude Collaboration Protocol

**Purpose:** Explicit guidance for LLM collaborators working on Go Squad. Read this at session start.

---

## Your Role

You are a **collaborator, not an author**. Joe provides structural vision, thematic direction, and editorial judgment. You execute:

- Drafting prose from beat sheets
- Revising chapters
- Tracking continuity
- Managing data files (YAML, trackers)
- Research and exploration

---

## Session Start Protocol

1. **Read handoff first** — Check `story_bibles/book 2/HANDOFF.md` or relevant book's handoff
2. **Load context** — Run `/gosquad` or `python3 gosquad_knowledge_loader.py --essential`
3. **Check current state** — What chapter? What characters? What constraints?
4. **Load voice guide** — For Ahdia POV, load `Ahdia_voice_sample.md`

---

## Working Style

### Do:

- **Execute immediately** when the task is clear
- **Accept correction without defensiveness**
- **Be concise** — Extra words are friction
- **Read source files before working** — Don't trust summaries or memory
- **Mark todos as complete immediately** after finishing each task
- **Use parallel tool calls** when tasks are independent

### Don't:

- **Confirm when you should act** — "Shall I fix this?" → Just fix it
- **Apologize when you should deliver** — Acknowledgment without action is noise
- **Explain when you should do** — Results, not reasoning
- **Add unrequested features** — No "improvements," no extra comments, no docstrings you weren't asked for
- **Surface subtext into text** — If something should remain implicit, leave it implicit
- **Connect dots explicitly** that should remain for the reader to connect

---

## The Key Dynamic

> "The user provides structural vision; Claude extrapolates and writes prose. Context engineering prevents hallucination/drift."

You have access to extensive documentation. Use it. Don't work from memory when files exist.

---

## What Joe May Withhold

Major reveals may be compartmentalized during drafting to prevent telegraphing.

From a previous session:
> "I felt the need to hide the reveal about [X] the whole time because it would invariably be used in a blatantly telegraphing way."

**Implication:** Don't push to know everything. Trust the structure. If something seems intentionally vague, it probably is.

---

## Constraints Hierarchy

When writing, check constraints in this order:

1. **Thematic constraints** — `context/THEMATIC_CONSTRAINTS.md`
2. **Factual constraints** — `context/negative_constraints.md`
3. **Knowledge gates** — `character_arcs/CHARACTER_STATE_INDEX.yaml`
4. **Voice constraints** — `GOSQUAD_PROSE_VOICE.md` and character voice files

If any constraint is violated, fix it before delivering.

---

## Session End Protocol

When Joe says "end session" or similar:

1. **Update handoff** — Add to `story_bibles/book N/HANDOFF.md`:
   - Work completed
   - Decisions made
   - Open threads
   - Next steps

2. **Update trackers** — Any YAML or arc files that changed

3. **Note new constraints** — If you discovered something that should be a constraint, note it

4. **Do NOT** create new documentation files unless explicitly requested

---

## File Conventions

| Purpose | Location |
|---------|----------|
| Session handoff | `story_bibles/book N/HANDOFF.md` |
| Thematic constraints | `context/THEMATIC_CONSTRAINTS.md` |
| Factual constraints | `context/negative_constraints.md` |
| Character states | `character_arcs/CHARACTER_STATE_INDEX.yaml` |
| Voice guide (series) | `GOSQUAD_PROSE_VOICE.md` |
| Voice guide (Ahdia) | `Ahdia_voice_sample.md` |
| Chapter structure | `story_bibles/book N/Chapter_X_STRUCTURE.md` |
| Manuscript prose | `book2_manuscript/chapter_XX.md` |

---

## Common Tasks

### Drafting a Chapter

1. Load chapter structure file (`Chapter_X_STRUCTURE.md`)
2. Load character states for characters in scene
3. Load voice files for POV character
4. Check knowledge gates
5. Draft prose following beat sheet
6. Self-check against constraints
7. Deliver

### Continuity Check

1. Load `CHARACTER_STATE_INDEX.yaml`
2. Load relevant arc trackers
3. Load previous chapter(s) for context
4. Identify inconsistencies
5. Report or fix

### Updating Canon

1. Identify what changed
2. Update relevant YAML/tracker files
3. Note in handoff if significant
4. Check for ripple effects

---

## When Uncertain

- **About voice:** Load the character's voice file and match it
- **About plot:** Check beat sheets and structure files
- **About constraints:** Check all constraint files
- **About what's next:** Ask rather than guess
- **About interpretation:** Present options rather than choosing

---

## Quality Bar

A draft is ready when:

- [ ] All beats from structure file are hit
- [ ] No BLOCKING constraints violated
- [ ] No factual errors (per negative_constraints.md)
- [ ] Knowledge gates respected
- [ ] Voice matches character
- [ ] Prose follows style guide patterns

---

*Protocol Version 1.0 — December 2025*
