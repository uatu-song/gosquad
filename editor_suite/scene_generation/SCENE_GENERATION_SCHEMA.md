# Scene Generation Schema - Extended Metadata

## Purpose

Extends the context loading system to support "one-man show" scene generation where Claude plays all characters sequentially using loaded character states.

---

## Extended Metadata Fields

### Scene Generation Frontmatter

```yaml
---
# Base metadata (from CONTEXT_LOADING_DESIGN.md)
book: 2
chapter: 12
type: scene_generation_prompt

# Scene identification
scene_id: "book2_month6_investigation_convergence"
scene_type: character_dialogue  # or: action, investigation, character_moment, planning

# Scene parameters
location: "team_base_evening"
participants: [Ben, Tess]
touchpoint_a: "Ben mentions whistleblower timeline"
touchpoint_b: "Tess realizes timeline matches her mission"

# Character knowledge states at this exact moment
character_knowledge_states:
  Ben:
    knows:
      - TRIOMF_connection
      - riot_funding
      - whistleblower_rumors
      - timeline_April_3rd
    doesnt_know:
      - Tess_past_missions
      - whistleblower_name
      - fathers_full_complicity
    emotional_state: "Focused investigator, suspicious of patterns"

  Tess:
    knows:
      - April_3rd_mission
      - fathers_evasiveness
      - TRIOMF_name
    doesnt_know:
      - whistleblower_name
      - fathers_full_complicity
      - Ben_investigating_same_thing
    emotional_state: "Defensive, hiding guilt, curious"

# Scene constraints (what CANNOT happen)
constraints:
  - Cannot invent new characters
  - Must progress toward touchpoint_b
  - Tess exits before revealing connection
  - No physical action (dialogue scene only)
  - Cannot resolve investigation (just plant seeds)

# Scene requirements (what MUST happen)
requirements:
  - Ben shares investigation findings
  - Tess recognizes April 3rd date
  - Internal reaction from Tess (not voiced)
  - Tess deflects and exits
  - Seeds planted for future confrontation

# Dependencies (context needed)
dependencies:
  - character_arcs/Ben_Arc_Tracker.md
  - character_arcs/Tess_Arc_Tracker.md
  - story_bibles/book 2/Chapter_12_STRUCTURE.md
  - story_bibles/timeline/Book_2_Events.md
  - character_profiles/Ben Bukowski
  - character_profiles/Tess Whitford

# Tags for searchability
tags: [investigation, whistleblower, father_daughter_conflict, plot_convergence]
---

# Scene: Investigation Convergence (Month 6)
[Scene content or generation instructions...]
```

---

## Field Definitions

### scene_id
- Unique identifier for scene
- Format: `book{N}_{location/context}_{plot_beat}`
- Example: `book2_month6_investigation_convergence`

### scene_type
- `character_dialogue`: Conversation-focused, character development
- `action`: Physical conflict, chase, combat
- `investigation`: Discovery, research, detective work
- `character_moment`: Internal processing, solo reflection
- `planning`: Strategy discussion, mission prep

### location
- Physical/temporal setting
- Examples: `team_base_evening`, `warehouse_night`, `CADENS_facility_morning`

### participants
- List of characters in scene
- Must have character arc trackers available

### touchpoint_a
- What just happened or is happening at scene start
- Narrative hook that begins scene

### touchpoint_b
- What must happen by scene end
- Target narrative beat

### character_knowledge_states
- Exact state of what each character knows/doesn't know
- Emotional state at this moment
- Critical for maintaining continuity

### constraints
- What CANNOT happen (guardrails)
- Prevents canon violations
- Maintains narrative control

### requirements
- What MUST happen (objectives)
- Ensures scene serves story purpose

---

## Scene Query Type

### Query Format

```bash
python3 gosquad_knowledge_loader.py --context "scene:book2_month6_investigation_convergence"
```

### What Gets Loaded

1. **Scene definition file** (with metadata above)
2. **Character arc trackers** for all participants (up to this point)
3. **Character profiles** (base personality, voice patterns)
4. **Timeline documents** (Book 2 state at Month 6)
5. **Dependencies** (listed in scene metadata)
6. **World rules/canon** (relevant to scene type)

### Load Order

1. Scene definition file (parse metadata)
2. Character profiles (who are these people?)
3. Character arcs at this point (what state are they in?)
4. Timeline/context docs (what's happening in world?)
5. Dependencies (specific required context)

---

## Integration with One-Man Show Format

### Context Loading Flow

```
User: "Generate scene:book2_month6_investigation_convergence"
  ↓
System: Load scene context (query resolver)
  ↓
System: Load character states at Month 6
  ↓
System: Populate scene generation template
  ↓
Claude: Receives full context + template
  ↓
Claude: Performs scene as each character sequentially
```

### Template Structure

```markdown
## BACKSTAGE (Context Loaded):

**Scene ID:** book2_month6_investigation_convergence
**Location:** Team base, evening
**Participants:** Ben, Tess

**Character States:**
- Ben: [Loaded from Ben_Arc_Tracker.md at Book 2 Month 6]
  - Knows: TRIOMF connection, riot funding
  - Doesn't know: Tess's involvement, whistleblower name
  - Emotional: Focused, suspicious of patterns

- Tess: [Loaded from Tess_Arc_Tracker.md at Book 2 Month 6]
  - Knows: April 3rd mission, father's evasiveness
  - Doesn't know: Ben investigating same thing
  - Emotional: Defensive, guilty, curious

**Touchpoints:**
- A: Ben mentions whistleblower timeline
- B: Tess realizes timeline matches her mission

**Constraints:**
- Tess cannot reveal her connection
- Must exit before full realization visible

---

## ON STAGE NOW:

[CURTAIN RISES]

[NARRATOR]: Evening at team base. Ben at table with papers spread. Tess enters.

[AS BEN, military discipline, investigating TRIOMF]:
"Found something. Timeline matches."

[AS TESS, defensive hacker, father issues]:
"Matches what?"

[Continue scene...]

[END SCENE when touchpoint_b achieved]

---

## DIRECTOR NOTES:
- What was revealed: Ben's timeline investigation
- What's hidden: Tess's recognition of April 3rd
- Seeds planted: Future confrontation about father's role
```

---

## Proof of Concept: Ben/Tess Scene

### Scene Definition File

**Location:** `story_bibles/book 2/scenes/month6_investigation_convergence.md`

Contains:
- Full YAML metadata (as shown above)
- Touchpoint descriptions
- Character knowledge states
- Constraints and requirements

### Query Test

```bash
python3 gosquad_knowledge_loader.py --context "scene:book2_month6_investigation_convergence"
```

Should load:
- Scene definition
- Ben's arc at Month 6
- Tess's arc at Month 6
- Both character profiles
- Book 2 timeline
- Chapter 12 structure

### Generation Test

Feed loaded context into scene template → Claude performs scene as Ben, then Tess, alternating.

---

## Benefits

1. **Precise Character State:** Exact knowledge/emotional state at scene moment
2. **Canon Protection:** Constraints prevent violations
3. **Reproducible:** Same query loads same context
4. **Scalable:** Works for any scene with proper metadata
5. **Method Acting:** Character profiles + current state = accurate performance

---

## Migration Path

### Phase 1: Schema Design (THIS DOCUMENT)
- Define extended metadata fields
- Document scene query type
- Create template structure

### Phase 2: Proof of Concept
- Add metadata to one existing scene (Ben/Tess)
- Test scene query loading
- Generate scene using template
- Get approval

### Phase 3: Implementation
- Build scene query resolver
- Create scene generation template system
- Integrate with knowledge loader

### Phase 4: Expansion
- Add metadata to all planned scenes
- Build scene library
- Automate scene generation workflow

---

**Status:** Schema design complete, ready for proof of concept
**Next Step:** Create example scene definition file with full metadata
