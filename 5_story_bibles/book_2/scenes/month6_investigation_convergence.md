---
# Base metadata
book: 2
chapter: 12
type: scene_generation_prompt

# Scene identification
scene_id: "book2_month6_investigation_convergence"
scene_type: character_dialogue

# Scene parameters
location: "team_base_evening"
participants: [Ben, Tess]
touchpoint_a: "Ben reviewing whistleblower timeline, notices pattern"
touchpoint_b: "Tess internally realizes April 3rd connection but conceals it"

# Character knowledge states at this exact moment
character_knowledge_states:
  Ben:
    knows:
      - TRIOMF funding the riots
      - Whistleblower leaked info about police violence
      - Timeline: Whistleblower active around April
      - Police response was unusually coordinated
      - Someone tipped off TRIOMF about whistleblower
    doesnt_know:
      - Whistleblower's name is Isaiah Bennett
      - Tess ran mission April 3rd for her father
      - Chief Whitford is involved
      - Tess's father connection to case
    character_state_reference: "character_arcs/Ben_Arc_Tracker.md#book2-month6"
    voice: "Direct, military precision, asks specific questions"

  Tess:
    knows:
      - She ran mission April 3rd (broke into apartment)
      - Father sent her, was evasive about target
      - TRIOMF name from team investigations
      - Father has been acting strange
      - She suspects father's involved in something bad
    doesnt_know:
      - Target was whistleblower Isaiah Bennett
      - Her mission led to Isaiah's death
      - Father specifically set up the whistleblower
      - Ben is investigating same timeline
      - Full scope of father's complicity
    character_state_reference: "character_arcs/Tess_Arc_Tracker.md#book2-month6"
    voice: "Gen Z slang, deflects with sarcasm, hedges when uncertain"

# Scene constraints (what CANNOT happen)
constraints:
  - Cannot invent new characters
  - Cannot name the whistleblower (neither knows yet)
  - Must progress toward touchpoint_b naturally
  - Tess exits before revealing connection overtly
  - No physical action (pure dialogue)
  - Cannot resolve investigation (seeds only)
  - Tess cannot confess father's missions
  - Ben cannot guess Whitford connection

# Scene requirements (what MUST happen)
requirements:
  - Ben shares investigation findings about timeline
  - Ben mentions April 3rd specifically
  - Tess recognizes the date internally
  - Tess shows physical tell (freezes, deflects)
  - Internal monologue: Tess's guilt/horror
  - Tess deflects and exits quickly
  - Ben notices her reaction but doesn't push
  - Seeds planted for future confrontation
  - Maintains dramatic irony (reader knows more than Ben)

# Dependencies (context needed)
dependencies:
  - character_arcs/Ben_Arc_Tracker.md
  - character_arcs/Tess_Arc_Tracker.md
  - story_bibles/book 2/Chapter_12_STRUCTURE.md
  - story_bibles/timeline/Book_2_Events.md
  - character_profiles/Ben Bukowski
  - character_profiles/Tess Whitford
  - story_bibles/book 2/SUBPLOT_Whistleblower_Connection.md

# Tags
tags: [investigation, whistleblower, father_daughter_conflict, plot_convergence, dramatic_irony]
---

# Scene: Investigation Convergence (Month 6)

**NARRATIVE PURPOSE:** Plant seeds of Tess's connection to whistleblower case without revealing it to Ben yet. Build tension through dramatic irony.

**DRAMATIC IRONY:** Reader knows Tess ran April 3rd mission for her father. Ben doesn't know. Tess doesn't know the mission was connected to this investigation.

---

## Scene Context

### What Came Before (Touchpoint A)
- Ben has been investigating TRIOMF funding
- Discovered connection to police-coordinated violence
- Found timeline: Whistleblower was active early April
- Whistleblower disappeared April 5th (killed by police at protest)
- Someone tipped off TRIOMF about the whistleblower before death
- Ben reviewing documents at team base, evening

### What Must Happen (Touchpoint B)
- Tess recognizes April 3rd as her mission date
- Internal horror: "Did I...?"
- Conceals recognition from Ben
- Exits scene carrying new guilt
- Ben left with suspicion about her reaction

---

## Scene Beats

### Beat 1: Entry
- Tess enters base, sees Ben working
- Casual banter attempt
- Ben distracted, focused on documents

### Beat 2: The Timeline
- Ben shares: "Found pattern in whistleblower case"
- Mentions early April timeline
- Tess feigning interest (actually curious about father's activities)

### Beat 3: April 3rd
- **Ben:** "Someone broke into whistleblower's apartment April 3rd"
- **Tess (internal):** Recognition. Horror.
- **Tess (external):** Deflects, asks clarifying question to hide reaction

### Beat 4: The Tell
- Tess shows physical tell (freeze, hesitation, forced casualness)
- Ben notices but doesn't call it out
- Tess makes excuse to exit
- Ben watching her leave, suspicious

### Beat 5: Exit
- Tess leaves quickly
- Internal monologue: Processing horror
- Ben alone with documents, noting her reaction

---

## Generation Notes

### Voice Reminders

**Ben:**
- Military precision: "Timeline shows coordination"
- Specific questions: "What do you know about April 3rd?"
- Doesn't ramble, gets to point
- Patient but persistent

**Tess:**
- Gen Z casual: "That's sus" / "No cap?"
- Deflects with sarcasm when uncomfortable
- Tech jargon slips in
- Hedges: "Maybe" / "I think" / "Sort of"

### Physical Tells for Tess
- Stops typing mid-keystroke
- Looks up too quickly
- Forced casual tone
- Leg bouncing (nervous energy)
- Makes excuse about homework/code

### Dramatic Irony Maintenance
- Tess doesn't know target was whistleblower
- Ben doesn't know Tess did the break-in
- Reader knows both
- Neither makes full connection yet

---

## Expected Output Format

```
[NARRATOR]: Scene description, location, mood

[AS BEN, military investigator, focused]:
Dialogue and action

[AS TESS, Gen Z hacker, defensive]:
Dialogue and action

[AS BEN]:
Response

[Continue alternating until touchpoint_b achieved]

[END SCENE]
```

---

**Status:** Ready for scene generation
**Test Query:** `--context "scene:book2_month6_investigation_convergence"`
**Expected Result:** Loads all dependencies, populates template, Claude performs scene
