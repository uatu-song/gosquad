---
# Base metadata
book: 4
chapter: 15
type: scene_generation_prompt

# Scene identification
scene_id: "book4_ch15_strategic_argument"
scene_type: character_dialogue

# Scene parameters
location: "resistance_hq_command_room"
participants: [Ruth, Korede, Diana, Ben, Victor, Tess]
touchpoint_a: "Ruth presents rescue plan after signal detection"
touchpoint_b: "Coalition splits - Ruth proceeds, Korede stays"

# Character knowledge states at this exact moment
character_knowledge_states:
  Ruth:
    knows:
      - Clone army defeated days ago
      - Artificial signal detected from The Between
      - Signal matches Diana's coordinates
      - Ahdia was thrown through rift by Bellatrix
      - Rescue requires artificial sun facility
      - Fusion collapse = 4 minute window, supernova risk
      - Million+ lives at stake
    doesnt_know:
      - If signal is actually Ahdia (no proof)
      - What Ahdia has experienced in The Between
      - If Bellatrix is baiting them
      - Whether international facility will cooperate
    character_state_reference: "character_arcs/Ruth_Arc_Tracker.md#book4-chapter15"
    voice: "Direct, medical precision, fierce when defending family"

  Korede:
    knows:
      - Clone army defeated but TRIOMF/Kain/Bellatrix still active
      - Defending civilian evacuation routes daily
      - Signal detected but unverified
      - Rescue requires massive resources
      - His sister Leta died in Book 2
      - Team lost many in clone war
    doesnt_know:
      - If signal is Ahdia or trap
      - Full scope of rescue requirements
      - Why Ruth is so certain
    character_state_reference: "character_arcs/Korede_Arc_Tracker.md#book4-chapter15"
    voice: "17 years old, tactical, protective of civilians, grief-driven"

  Diana:
    knows:
      - She's Ahdia Prime from erased timeline
      - Has temporal powers (team knows now)
      - Calculated coordinates for The Between
      - Fusion collapse mechanics
      - Risk of supernova
      - 43 iterations of timeline experience
    doesnt_know:
      - If this timeline's Ahdia survived
      - What's waiting in The Between
      - If Bellatrix is interfering
    character_state_reference: "character_arcs/Diana_Arc_Tracker.md#book4-chapter15"
    voice: "Older, weary, precise, carries timeline weight"

  Ben:
    knows:
      - Ahdia is family
      - Signal is artificial (someone sent it)
      - Rescue is dangerous
      - Lost many in clone war
      - Evidence-based investigator background
    doesnt_know:
      - If signal is Ahdia
      - If rescue will work
      - Cost to civilians if they're wrong
    character_state_reference: "character_arcs/Ben_Arc_Tracker.md#book4-chapter15"
    voice: "Former cop, military tactics, wants proof but siding with Ruth"

  Victor:
    knows:
      - Both/and thinking (sees multiple truths)
      - Korede and Ruth both right
      - Rescue is faith-based, not proof-based
      - Community networks matter
    doesnt_know:
      - Which choice is "correct"
      - If he should go or stay
    character_state_reference: "character_arcs/Victor_Arc_Tracker.md#book4-chapter15"
    voice: "Environmental organizer, both/and teacher, sees complexity"

  Tess:
    knows:
      - Ahdia saved her life multiple times
      - Signal could be trap
      - Korede's position is valid
      - Ruth won't abandon Ahdia
    doesnt_know:
      - If she's making right choice
      - What her father would think (complicated)
    character_state_reference: "character_arcs/Tess_Arc_Tracker.md#book4-chapter15"
    voice: "Gen Z hacker, loyal but anxious, father issues"

# Scene constraints (what CANNOT happen)
constraints:
  - Cannot resolve with everyone agreeing (split must happen)
  - Korede cannot abandon civilians (his position is valid)
  - Ruth cannot abandon Ahdia (her position is valid)
  - No one is villain (both/and - both right)
  - Cannot have proof signal is Ahdia
  - Cannot minimize supernova risk
  - Must respect Korede's grief (Leta died Book 2)
  - Must show Ruth's determination without dismissing opposition

# Scene requirements (what MUST happen)
requirements:
  - Ruth presents rescue plan to group
  - Korede challenges resource allocation
  - Debate about strategic priorities (rescue vs active threats)
  - Diana provides technical data (fusion collapse, risks)
  - Ben sides with Ruth (evidence thin but family matters)
  - Victor sees both sides (both/and thinking)
  - Tess torn but ultimately sides with Ruth
  - Korede refuses to help (stays to defend civilians)
  - Ruth accepts his choice, proceeds anyway
  - Coalition forms: Ruth, Diana, Ben, Victor, Tess, Ryu
  - Opposition clear: Korede, resistance leaders
  - Pattern established: "CADENS waits. Go Squad go."
  - Respectful split (no animosity, painful separation)

# Dependencies (context needed)
dependencies:
  - story_bibles/book 4/book4_chapter15_beats.md
  - story_bibles/book 4/SESSION_DECISIONS_2025-11-24.md
  - story_bibles/book 4/EARTH_ARC_STRUCTURE.md
  - character_arcs/Ruth_Arc_Tracker.md
  - character_arcs/Korede_Arc_Tracker.md
  - character_arcs/Diana_Arc_Tracker.md

# Tags
tags: [strategic_debate, coalition_split, family_vs_duty, both_and_conflict, korede_turning_point_setup]
---

# Scene: The Strategic Argument (Chapter 15, Scene 5)

**NARRATIVE PURPOSE:** Establish the central conflict of Earth arc - Ruth's coalition pursuing rescue despite strategic opposition. Show both sides as valid (both/and). Set up Korede's absence and eventual Chapter 27 return.

**DRAMATIC TENSION:** Both Ruth and Korede are RIGHT. Neither is villain. Personal loyalty (Ruth) vs strategic necessity (Korede). Faith (signal is Ahdia) vs pragmatism (could be trap).

---

## Scene Context

### What Came Before (Touchpoint A)
- Clone army defeated days ago (Chapter 14)
- Team regrouping at resistance HQ
- Mother FAERIS detected artificial signal from The Between
- Signal matches Diana's coordinates but too weak to decode
- Ruth believes it's Ahdia
- Diana explained rescue requirements: Artificial sun facility, fusion collapse, 4-minute window, supernova risk if failed
- Ruth calls meeting to present rescue plan

### What Must Happen (Touchpoint B)
- Coalition splits after debate
- Ruth's coalition: Ruth, Diana, Ben, Victor, Tess, Ryu (pro-rescue)
- Opposition: Korede, resistance leaders (wrong priority, defending civilians)
- Korede refuses to help, stays at post
- Ruth respects his choice, proceeds anyway
- Pattern established: Go Squad acts despite opposition
- Setup for Korede's absence (Ch 15-26) and eventual return (Ch 27)

---

## Scene Beats

### Beat 1: The Proposal
- Ruth presents rescue plan to full group
- Diana provides technical requirements
- Mother FAERIS capabilities explained
- Enormous risk acknowledged (supernova danger)

### Beat 2: Korede's Challenge
- Korede: "We lost how many defending this city? Now abandon them for one person?"
- Questions resource allocation
- TRIOMF/Kain/Bellatrix still active threats
- Civilians need defending daily

### Beat 3: Ruth's Position
- Ruth: "She's family. We don't leave family behind."
- Personal loyalty absolute
- Won't abandon Ahdia
- Faith over proof

### Beat 4: The Debate
- Back and forth arguments
- Diana: Technical data supports dimensional origin
- Korede: Mathematics don't fight clone avatars
- Ben: Sides with Ruth (if it's her, must try)
- Victor: Sees both sides, both valid
- Tess: Torn but ultimately loyal to Ruth

### Beat 5: The Impasse
- No resolution possible
- Both positions valid
- Neither will change
- Respectful but painful

### Beat 6: Ruth's Decision
- Ruth: "Then stay. We'll go."
- Not angry, understanding
- Won't ask him to abandon civilians
- Won't abandon Ahdia either
- Both/and: Both choices matter

### Beat 7: The Split
- Coalition forms around Ruth
- Korede stays with resistance
- No animosity but clear separation
- Painful but necessary
- Pattern: Go Squad go

---

## Generation Notes

### Voice Reminders

**Ruth:**
- Direct, medical precision
- Fierce when defending family
- "We don't leave family behind" = core belief
- Won't argue once decision made

**Korede:**
- 17 years old (youngest perspective)
- Tactical, protective
- Lost sister Leta (grief driving choices)
- "I'm defending civilians every day" = his mission

**Diana:**
- Older Ahdia from erased timeline
- Weary, precise, clinical
- Carries 43 timelines of weight
- Supports Ruth but acknowledges risks

**Ben:**
- Former cop, evidence-based
- Military tactical thinking
- Wants proof but trusts Ruth
- "If it's her, we have to try"

**Victor:**
- Both/and teacher
- Sees multiple valid truths
- "Korede is right. Ruth is right. Both."
- Environmental organizer, community focus

**Tess:**
- Gen Z slang, tech focus
- Loyal but anxious
- Father issues (complicated)
- Young but committed

### Physical Tells

**Ruth:**
- Stands firm, doesn't pace
- Direct eye contact
- Hands steady (medical discipline)
- Won't back down

**Korede:**
- Younger, more kinetic
- Frustrated gestures
- Grief visible when mentioning casualties
- Defensive posture (protecting position)

**Diana:**
- Still, calculating
- Older exhaustion
- Timeline weight in movements
- Supports Ruth silently

### Both/And Emphasis

- Korede is RIGHT (civilians need defending)
- Ruth is RIGHT (family doesn't get abandoned)
- Ben is RIGHT (evidence thin but faith matters)
- Victor is RIGHT (both positions valid)
- No villain in this scene
- Painful because both sides matter

### Emotional Beats

- Ruth: Fierce determination, won't abandon Ahdia
- Korede: Defensive protection, won't abandon civilians
- Diana: Weary support, understands both
- Ben: Torn but loyal
- Victor: Seeing complexity
- Tess: Anxious but committed

---

## Expected Output Format

```
[NARRATOR]: Scene description, location, mood

[AS RUTH, trauma surgeon and Go Squad leader, fierce protector]:
Dialogue and action

[AS KOREDE, 17-year-old resistance tactician, grieving brother]:
Dialogue and action

[AS DIANA, Ahdia Prime from erased timeline, timeline-weary]:
Dialogue and action

[Continue alternating through all participants]

[END SCENE]
```

---

## Validation Checklist

Before ending scene generation, verify:

- [ ] Coalition split happens (Ruth proceeds, Korede stays)
- [ ] Both positions shown as valid (both/and)
- [ ] No proof signal is Ahdia (faith vs certainty)
- [ ] Supernova risk acknowledged (enormous stakes)
- [ ] Korede's grief visible (Leta's death matters)
- [ ] Ruth's determination clear (won't abandon family)
- [ ] Respectful split (no animosity, painful)
- [ ] Pattern established (Go Squad go despite opposition)
- [ ] Setup for Korede's Chapter 27 return

---

**Status:** Ready for scene generation
**Test Query:** `--context "scene:book4_ch15_strategic_argument"`
**Expected Result:** Multi-character debate showing both/and conflict, coalition split, respectful opposition
