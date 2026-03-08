---
# Base metadata
book: 4
chapter: 16
type: scene_generation_prompt

# Scene identification
scene_id: "book4_ch16_the_between_arrival"
scene_type: survival_horror

# Scene parameters
location: "the_between_dimensional_prison"
participants: [Ahdia, AR-Ryu]
touchpoint_a: "Bellatrix throws Ahdia through rift (Book 3 ending)"
touchpoint_b: "First night in panic room, water system built, severely exhausted"

# TTRPG Roll Results
dice_rolls:
  landing_severity:
    roll: 22  # 19 + 3 from Victor's training
    outcome: "Perfect landing, no injuries"
    consequence: "Bruised but fully functional, no movement penalties"

  unconscious_duration:
    roll: 12
    outcome: "47 minutes unconscious"
    consequence: "Air supply: 5h 13m remaining when wakes"

  ar_ryu_functionality:
    roll: 13
    outcome: "Standard functionality"
    consequence: "Hologram and audio fully operational"

  environmental_scan:
    roll: 9
    outcome: "HUD malfunctioning, distance unclear"
    consequence: "Ruins visible but rangefinding unreliable, dimensional interference"

  morale_check:
    roll: 12  # 14 - 2
    outcome: "Functional despite fear"
    consequence: "Determined to survive, pushes through cosmic displacement terror"

  navigation_ruins:
    roll: 9  # 7 + 2
    outcome: "Lost in ruins"
    consequence: "3+ hours lost wandering, only 2h air remaining when finds panic room"

  panic_room_condition:
    roll: 8
    outcome: "Marginal air quality"
    consequence: "Breathable but stale, recyclers barely functioning, needs repairs"

  water_system_build:
    roll: 21  # 19 + 2
    outcome: "Critical success"
    consequence: "4 hours build time, 1.5L/day output, 0.5% battery drain"

  first_night_rest:
    roll: 4  # 6 - 2
    outcome: "Critical failure - Insomnia"
    consequence: "Cannot sleep, severe exhaustion, -2 to all rolls Chapter 17/18"

# Character knowledge states at this exact moment
character_knowledge_states:
  Ahdia:
    knows:
      - Bellatrix threw her through dimensional rift
      - She's in The Between (Bellatrix's prison dimension)
      - Powers don't work here (tried, failed)
      - Victor's training saved her from broken spine
      - Rift sealed behind her, no visible way back
      - Team cannot contact her (comms dead)
      - AR-Ryu is holographic AI, not actual Ryu
      - Got lost in ruins for 3+ hours (nearly died)
      - Found ancient panic room with marginal air
      - Built water recycler (1.5L/day, excellent result)
      - Cannot sleep despite exhaustion
    doesnt_know:
      - If team is searching for her
      - How long she was unconscious (AR-Ryu told her 47min but felt longer)
      - What this dimension actually is
      - Who built the ruins/panic room
      - How Bellatrix survived here
      - If there's food anywhere
      - How to get home
      - Why visor sensors glitch on distance readings
    physical_state: "No injuries, severely exhausted from insomnia, adrenaline crash"
    emotional_state: "Functional but fragile, cosmic displacement terror, determination fighting despair"
    resources: "Battery 95.5% (190 days), Water 1.5L/day, Air breathable (marginal quality)"
    capabilities: "NO temporal powers, human skills only, AR-Ryu guidance, nanotech battlesuit"
    character_state_reference: "character_arcs/Ahdia_Arc_Tracker.md#book4-chapter16"
    voice: "TV-saturated hermit, pop culture lens, casual profanity when stressed, processes terror through references"

  AR-Ryu:
    knows:
      - Ahdia stranded in dimensional space
      - Powers non-functional (sensors confirm)
      - Environmental readings: Unbreathable atmosphere outside panic room
      - Battery status and drain rates
      - Water system specifications and output
      - Ahdia's vital signs (elevated stress, no sleep)
    doesnt_know:
      - Return path to Earth
      - Dimensional physics principles
      - Who built panic room
      - Food source locations
      - Long-term survival probability
    ai_state: "Clinical, precise, primary function is survival assistance"
    personality: "Not yet developed, pure utility at this stage"
    capabilities: "Environmental scanning, technical guidance, holographic projection, vital monitoring"
    limitations: "Hologram only (cannot manipulate objects), limited by visor sensors, no dimensional knowledge"
    voice: "Ryu's voice (confusing for Ahdia), formal/clinical phrasing, directive instructions"

# Scene constraints (what CANNOT happen)
constraints:
  - Powers cannot work in The Between
  - Rift cannot reopen (sealed)
  - Team cannot contact her (no comms)
  - Cannot find food this chapter (next chapter problem)
  - Cannot sleep despite exhaustion (insomnia locked in)
  - Panic room air quality cannot be excellent (rolled marginal)
  - Navigation cannot be easy (already lost 3+ hours)
  - AR-Ryu cannot have personality yet (develops over time)
  - Cannot minimize cosmic displacement horror

# Scene requirements (what MUST happen)
requirements:
  - Scene 1: Fall through rift, emergency EVA deploys, perfect landing (Victor's training)
  - Scene 2: Wake to AR-Ryu's voice, disoriented hope → crushing reveal (not actual Ryu)
  - Scene 3: Survey wrong sky, alien landscape, ruins visible but distance unclear
  - Scene 4: Realize complete isolation, powers don't work, team unreachable
  - Scene 5: Navigate ruins, get lost, air running critically low (2h remaining when finds room)
  - Scene 6: Find panic room, marginal air quality, relief mixed with concern
  - Scene 7: Build water system in 4 hours (critical success), 1.5L/day output
  - Scene 8: First night, cannot sleep (insomnia), severe exhaustion for next chapter
  - Victor's training callback (saved her life)
  - Dune reference during water build
  - Battery tracking: 100% → 98% (fall/unconscious) → 96% (lost/scanning) → 95.5% (water system)
  - Air crisis felt viscerally (near-death at 2h remaining)
  - AR-Ryu establishes as tool, not companion (yet)

# Dependencies (context needed)
dependencies:
  - story_bibles/book 3/book3_chapter19_beats.md  # Bellatrix throws her through rift
  - story_bibles/book 4/book4_chapter16_beats.md  # Beat sheet structure
  - story_bibles/book 4/SESSION_DECISIONS_2025-11-24.md  # Between expansion
  - story_bibles/book 4/EMOTIONAL_ARC_AHDIA_ARRYU.md  # Relationship progression
  - character_arcs/Ahdia_Arc_Tracker.md  # Character state through Book 4
  - editor_suite/scene_generation/TTRPG_DICE_MECHANICS.md  # Roll system

# Tags
tags: [the_between, survival_horror, ar_ryu_introduction, dimensional_prison, water_system, insomnia_consequences, ttrpg_rolled]

---

# Scene: The Between Arrival (Chapter 16)

**NARRATIVE PURPOSE:** Establish Ahdia's stranded state in The Between. Show survival without powers. Introduce AR-Ryu. Near-death air crisis creates stakes. Water system success gives hope. Insomnia sets up exhaustion consequences for next chapter.

**DRAMATIC TENSION:** Cosmic displacement + isolation + resource management + time pressure. Roll results created: perfect landing (relief) → lost navigation (terror) → water success (hope) → insomnia (cost carrying forward).

**TTRPG ROLLED:** This scene incorporates dice roll outcomes. State propagates to Chapter 17/18.

---

## Scene Context

### What Came Before (Touchpoint A)
- Book 3 Chapter 19 ending: Bellatrix throws Ahdia through dimensional rift
- Team witnesses but cannot follow
- Rift seals immediately
- Ahdia falls through alien space
- Emergency EVA protocols activate mid-fall

### What Must Happen (Touchpoint B)
- Ahdia survives fall (perfect landing, Victor's training)
- Wakes to AR-Ryu (disorienting reveal)
- Realizes isolation and powerlessness
- Gets lost in ruins (3+ hours, air crisis)
- Finds panic room (marginal air quality)
- Builds water system (critical success, 1.5L/day)
- Cannot sleep first night (insomnia, exhaustion)
- Battery: 95.5%, Water: secured, Mental state: fragile but determined

---

## Expected Output Format

```
[NARRATOR]: Scene description, location, mood

[AS AHDIA, depressed hermit with time powers that don't work here, TV-saturated voice, processing cosmic horror through pop culture]:
Internal monologue, dialogue, action

[AS AR-RYU, holographic AI assistant with Ryu's voice, clinical and directive, no personality yet]:
Technical guidance, status updates

[NARRATOR]: Environmental details, physical sensations, time passage

[Continue alternating]

[END SCENE]
```

---

## Generation Notes

### Voice Reminders

**Ahdia:**
- TV references as coping mechanism
- Casual profanity when stressed ("Where the fuck am I?")
- Hermit observational style (external commentary on internal crisis)
- Pop culture lens: "alien Minecraft", Dune stillsuit reference
- Tired cynicism mixed with stubborn survival
- Parents' archaeology training surfaces (reading ruins)
- Victor's training callback (grateful, specific)

**AR-Ryu:**
- Ryu's voice (creates confusion/hope initially)
- Clinical precision: "You were unconscious for 47 minutes"
- Directive instructions: "Rotate 15 degrees. Connect blue conduit."
- Status updates: "Air supply: 2 hours remaining"
- No warmth yet (pure utility, personality develops later)
- Clarification phrasing: "Clarification: I am AR-Ryu, holographic AI assistant"

### Physical Tells

**Ahdia:**
- Perfect landing (Victor's drills, muscle memory)
- Exhaustion visible (stumbling, fumbling)
- Adrenaline crash during water build
- Cannot sleep (restless, eyes open, processing)
- Visor HUD glow in darkness

**AR-Ryu:**
- Hologram flickers to life
- Miniature projection (palm-sized Ryu)
- Cannot touch physical objects (guidance only)
- Appears/disappears as needed

### Key Emotional Beats by Scene

**Scene 1 - Fall:**
- Terror → Muscle memory → Darkness

**Scene 2 - Waking:**
- Hope (Ryu's voice!) → Crushing disappointment (just AI) → Loneliness

**Scene 3 - Wrong Sky:**
- Growing horror at wrongness → Existential displacement → "Not Earth. Not even close."

**Scene 4 - Alone:**
- Tries powers (nothing) → Tries comms (silence) → Acceptance: Must move or die

**Scene 5 - Lost in Ruins:**
- Navigation failure → Air dropping → Mounting panic → "I'm going to die in space Ikea"

**Scene 6 - Panic Room:**
- Relief (breathable air!) → Concern (marginal quality) → Gratitude (alive)

**Scene 7 - Water System:**
- Desperate focus → Small victories → Critical success → "We're not dying of thirst"

**Scene 8 - First Night:**
- Exhaustion → Cannot sleep → Processing cosmic displacement → Insomnia's weight

### Roll Result Integration

**Show consequences naturally:**
- Perfect landing: "Victor's drills. Hundred times through campus parkour. He saved my life."
- Lost navigation: Time passing, air warnings, wrong turns, panic rising
- Water success: System working better than expected, relief moment
- Insomnia: Eyes open, processing, exhaustion without sleep, dread for tomorrow

**Battery tracking visible:**
- HUD updates as percentages drop
- Ahdia calculating days remaining
- Decision to deactivate EVA (saves power)
- Water system drain rate established

---

## Validation Checklist

Before ending scene generation, verify:

- [ ] Perfect landing shown (Victor's training saved her)
- [ ] AR-Ryu introduction: Voice → hope → crushing reveal
- [ ] Lost navigation: 3+ hours, air crisis at 2h remaining
- [ ] Panic room: Marginal air quality acknowledged
- [ ] Water system build: 4 hours, critical success, 1.5L/day
- [ ] Insomnia: Cannot sleep, exhaustion visible
- [ ] Battery tracking: 100% → 95.5% with reasons shown
- [ ] Powers don't work (tried, failed)
- [ ] Team unreachable (comms dead)
- [ ] Cosmic displacement horror felt
- [ ] Ahdia's voice: TV references, casual profanity, hermit style
- [ ] AR-Ryu voice: Clinical, directive, Ryu's voice confusing
- [ ] Victor callback (training saved her)
- [ ] Dune reference (water recycling)
- [ ] Setup for Chapter 17/18: Exhausted (-2 rolls), water secured, food unsolved

---

**Status:** Ready for method actor performance with TTRPG roll results
**Roll State File:** `/workspaces/gosquad/story_bibles/book 4/CHAPTER16_ROLL_STATE.md` (to be created)
**Expected Result:** Seven-scene chapter showing survival through near-death air crisis, establishing Between as hostile environment, AR-Ryu as tool companion, insomnia carrying forward as consequence
