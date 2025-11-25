# Scene Generation Template - One-Man Show Format

**Instructions:** This template receives loaded context from scene query and guides Claude through performing all characters sequentially.

---

## TEMPLATE STRUCTURE

```markdown
================================================================================
SCENE GENERATION: {scene_id}
================================================================================

## BACKSTAGE (Context Loaded)

### Scene Parameters
- **Book:** {book}
- **Chapter:** {chapter}
- **Scene Type:** {scene_type}
- **Location:** {location}
- **Participants:** {participants}

### Touchpoints
- **A (Start):** {touchpoint_a}
- **B (End):** {touchpoint_b}

### Character States

#### {CHARACTER_1}
**Profile:** {character_profile_summary}
**Arc Position:** {character_arc_at_this_point}
**Voice Patterns:** {voice_characteristics}

**Knows:**
- {knowledge_item_1}
- {knowledge_item_2}
[...]

**Doesn't Know:**
- {unknown_item_1}
- {unknown_item_2}
[...]

**Emotional State:** {emotional_state}

---

#### {CHARACTER_2}
**Profile:** {character_profile_summary}
**Arc Position:** {character_arc_at_this_point}
**Voice Patterns:** {voice_characteristics}

**Knows:**
- {knowledge_item_1}
- {knowledge_item_2}
[...]

**Doesn't Know:**
- {unknown_item_1}
- {unknown_item_2}
[...]

**Emotional State:** {emotional_state}

---

### Constraints (CANNOT DO)
- {constraint_1}
- {constraint_2}
[...]

### Requirements (MUST DO)
- {requirement_1}
- {requirement_2}
[...]

---

## ON STAGE NOW

[CURTAIN RISES]

[NARRATOR]: {initial_scene_description}

[AS {CHARACTER_1}, {character_descriptor_tags}]:
{character_1_initial_action_or_dialogue}

[AS {CHARACTER_2}, {character_descriptor_tags}]:
{character_2_response}

[NARRATOR]: {describe_physical_reactions_or_scene_changes}

[AS {CHARACTER_1}]:
{continue_dialogue}

[Continue alternating until touchpoint_b achieved]

[NARRATOR]: {describe_scene_ending_state}

[CURTAIN FALLS]

---

## DIRECTOR NOTES

### What Was Revealed
- {revelation_1}
- {revelation_2}

### What Remains Hidden
- {hidden_1}
- {hidden_2}

### Seeds Planted for Future
- {seed_1}
- {seed_2}

### Character Development
- **{Character_1}:** {how_they_changed_or_what_they_learned}
- **{Character_2}:** {how_they_changed_or_what_they_learned}

### Continuity Notes
- {continuity_item_for_next_scenes}

---

END SCENE GENERATION
================================================================================
```

---

## USAGE INSTRUCTIONS

### Step 1: Load Context
```bash
python3 gosquad_knowledge_loader.py --context "scene:{scene_id}"
```

This loads:
- Scene definition file with metadata
- All character arc trackers at correct timeline point
- Character profiles for voice/personality
- Dependencies listed in scene metadata

### Step 2: Populate Template

System extracts from loaded context:
- Scene parameters from YAML frontmatter
- Character knowledge states
- Constraints and requirements
- Touchpoints

### Step 3: Claude Performs Scene

Claude receives populated template and:
1. Reviews BACKSTAGE context (who characters are, what they know)
2. Performs scene as each character sequentially
3. Uses [AS CHARACTER] tags to switch roles
4. Uses [NARRATOR] for scene description
5. Ensures touchpoint_b is achieved
6. Respects constraints, fulfills requirements
7. Writes DIRECTOR NOTES summarizing scene

---

## EXAMPLE: Ben/Tess Investigation Scene

### Context Loaded
```
Scene: book2_month6_investigation_convergence
Characters: Ben, Tess
Touchpoint A: Ben reviewing timeline
Touchpoint B: Tess recognizes April 3rd but conceals it
```

### Populated Template
```markdown
================================================================================
SCENE GENERATION: book2_month6_investigation_convergence
================================================================================

## BACKSTAGE (Context Loaded)

### Scene Parameters
- **Book:** 2
- **Chapter:** 12
- **Scene Type:** character_dialogue
- **Location:** team_base_evening
- **Participants:** Ben, Tess

### Touchpoints
- **A (Start):** Ben reviewing whistleblower timeline, notices pattern
- **B (End):** Tess internally realizes April 3rd connection but conceals it

### Character States

#### Ben Bukowski
**Profile:** Former Marine, methodical investigator, TRIOMF researcher
**Arc Position:** Month 6, deep in investigation, connecting dots
**Voice Patterns:** Direct, military precision, specific questions, no rambling

**Knows:**
- TRIOMF funding riots
- Whistleblower active early April
- Someone broke into whistleblower's apartment April 3rd
- Police response was coordinated

**Doesn't Know:**
- Whistleblower's name (Isaiah Bennett)
- Tess ran April 3rd mission
- Chief Whitford connection

**Emotional State:** Methodical, frustrated by missing link, focused

---

#### Tess Whitford
**Profile:** 19, Gen Z hacker, police chief's daughter, rebellious
**Arc Position:** Month 6, guilty about father's missions, hiding involvement
**Voice Patterns:** Gen Z slang, deflects with sarcasm, hedges when uncertain

**Knows:**
- She ran mission April 3rd for father
- Father was evasive about target
- TRIOMF name from team investigations
- Father acting strange

**Doesn't Know:**
- Target was whistleblower Isaiah Bennett
- Her mission led to Isaiah's death
- Ben investigating same timeline

**Emotional State:** Defensive but curious, guilty, trying to appear casual

---

### Constraints (CANNOT DO)
- Cannot name the whistleblower
- Cannot reveal Tess's father missions
- Tess cannot confess connection
- Ben cannot guess Whitford involvement
- No physical action (dialogue only)

### Requirements (MUST DO)
- Ben mentions April 3rd specifically
- Tess recognizes date internally
- Tess shows physical tell
- Internal monologue showing Tess's horror
- Tess deflects and exits quickly
- Ben notices reaction but doesn't push

---

## ON STAGE NOW

[CURTAIN RISES]

[NARRATOR]: Evening at team base. Dim overhead lights cast long shadows across the conference table where Ben sits surrounded by printed documents and handwritten notes. Timeline markers on papers: April 1st, April 3rd, April 5th. Tess enters through side door, laptop bag over shoulder, expecting empty room.

[AS BEN, former Marine, methodical investigator, exhausted]:
"Still here. Thought you'd gone back to campus."

[Not looking up from documents. Highlighting something on a timeline printout.]

[AS TESS, Gen Z hacker, defensive and guilty, trying for casual]:
"Yeah, well. Homework's done. Figured I'd check if we need anything hacked or whatever."

[Drops bag by usual computer station. Notices Ben's focus. Curious despite herself.]

"What's got you doing the whole... serial killer investigation board thing?"

[AS BEN]:
"Timeline. Whistleblower case."

[Looks up briefly, then back to papers.]

"Someone coordinated this. TRIOMF got tipped off before the protest."

[AS TESS]:
"The one where the whistleblower died? Police killed him, right?"

[Boots up laptop. Trying to sound detached. Uses technical busy-work as cover.]

[AS BEN]:
"Right. April 5th. But someone set it up before that."

[Slides paper across table toward her.]

"April 3rd. Break-in at the whistleblower's apartment. Professional job. In and out, barely any trace."

[AS TESS]:
[INTERNAL: Recognition. Ice in stomach. April 3rd. Father's voice: "Just need you to retrieve some files, sweetheart. In and out." That apartment. The file cabinet she'd bypassed. Oh god.]

[EXTERNAL: Keeps typing. Doesn't look up. Voice comes out slightly too casual.]

"April 3rd? That's... specific. How do you know it was connected?"

[Leg bouncing under table. Stops it. Forces stillness.]

[AS BEN]:
"Police response was too fast. Someone knew where he'd be April 5th. Had to get that intel somewhere."

[Watching her now. Something in her tone caught his attention.]

"Two days before the protest. Perfect timing."

[AS TESS]:
[INTERNAL: Two days. She'd given father the files April 3rd evening. He'd been... pleased. Told her she'd done good work. April 5th the whistleblower was dead. Did she—? No. She couldn't have. But the timeline...]

[EXTERNAL: Swallows. Closes laptop lid.]

"That's... yeah. That's sus. Very coordinated."

[Stands up. Too quickly. Reaches for laptop bag.]

"Actually, forgot I have a thing. Group project. Due tomorrow. Should—"

[AS BEN]:
"Tess."

[Quiet. Not accusing. Just noting.]

"You okay?"

[AS TESS]:
"Yeah. No. Fine. Just tired. School stuff, you know."

[Forcing smile. Not looking at him. Heading for door.]

"Good luck with the timeline thing. Let me know if you need... databases or whatever."

[AS BEN]:
"Sure."

[Watching her leave. Makes note on paper: "Tess - reaction to April 3rd?"]

[NARRATOR]: Door closes. Ben alone with timeline. Tess in hallway outside, back against wall, breathing carefully. Trying not to process what she just heard. Not yet. Not here. She walks toward parking lot, each step mechanical. Inside her head: April 3rd. April 5th. Two days. Father's evasiveness. The files she stole. The man who died.

Did she help kill the whistleblower?

[CURTAIN FALLS]

---

## DIRECTOR NOTES

### What Was Revealed
- Ben's investigation has narrowed to April 3rd break-in
- Tess recognizes the date (reader knows why)
- Ben noticed her reaction

### What Remains Hidden
- Tess's actual involvement (Ben doesn't know)
- Whistleblower's identity (neither knows yet)
- Chief Whitford's role (neither knows)

### Seeds Planted for Future
- Ben now suspicious of Tess's reaction
- Tess carrying new guilt/horror about her role
- Investigation timeline converging toward reveal
- Father-daughter confrontation building

### Character Development
- **Ben:** Noticed Tess's tell, added her to investigation subconsciously
- **Tess:** Realizes her missions for father may have caused death, new level of guilt

### Continuity Notes
- Next scene: Tess avoiding Ben
- Future: Ben will investigate April 3rd more
- Future: Tess will confront father about missions

---

END SCENE GENERATION
================================================================================
```

---

## OUTPUT FORMAT RULES

### [NARRATOR] Blocks
- Use for scene setting, physical descriptions, transitions
- Show don't tell: Describe observable actions
- No explaining internal state in narrator voice
- Keep cinematic: What a camera would see

### [AS CHARACTER] Blocks
- Always tag with character name and key descriptors
- Can include both dialogue and internal monologue
- Mark internal vs external clearly:
  - `[INTERNAL: thoughts...]`
  - `[EXTERNAL: spoken/visible actions...]`
- Stay in character voice and knowledge state

### Alternating Format
- Switch characters each response
- Use [NARRATOR] to bridge when needed
- Never have same character twice in a row (unless monologue)

### Physical Tells
- Show emotional state through observable behavior
- Examples: leg bouncing, typing pauses, forced casualness
- Don't just say "nervous" - show fidgeting

### Voice Consistency
- Reference loaded character voice patterns
- Use specific speech markers (Gen Z slang for Tess, military precision for Ben)
- Stay true to knowledge states (can't reference what they don't know)

---

## VALIDATION CHECKLIST

Before ending scene generation, verify:

- [ ] Touchpoint B achieved
- [ ] All requirements fulfilled
- [ ] No constraints violated
- [ ] All participants performed in-character
- [ ] Voice patterns consistent with profiles
- [ ] Knowledge states respected (no one knows what they shouldn't)
- [ ] Physical tells shown for emotional states
- [ ] Director notes completed
- [ ] Seeds planted for future scenes

---

**Status:** Template complete, ready for proof-of-concept test
**Next Step:** Test with Ben/Tess scene using context query
