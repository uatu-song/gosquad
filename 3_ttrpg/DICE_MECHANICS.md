# TTRPG Dice Mechanics for Go Squad Scene Generation

**Philosophy:** Touchpoints are anchors. Dice determine the journey and state between them.

---

## Core Concept

**Fixed:**
- Touchpoint A (starting state)
- Touchpoint B (ending state)
- Story must reach B from A

**Variable:**
- How character arrives at B
- What complications occur
- Character state when reaching B
- Resource costs paid

**Result:** Same destination, different journey. Consequences propagate to next scene.

---

## Dice System

**Using d20 system (familiar, flexible):**

- **Critical Success (20):** Best possible outcome, bonus benefit
- **Success (15-19):** Intended outcome achieved cleanly
- **Partial Success (10-14):** Outcome achieved with complication or cost
- **Failure (5-9):** Outcome not achieved, must try different approach
- **Critical Failure (1-4):** Outcome not achieved, additional complication

**Modifiers:**
- Character skills: +2 to +5 (Victor's training = +3 to parkour landing)
- Environmental factors: -2 to +2
- Resource availability: -2 to +2
- Previous scene state: Injuries/exhaustion = -1 to -3

---

## Roll Types

### Action Rolls
Character attempting specific action.
- **Examples:** Landing safely, building water system, finding panic room
- **On success:** Action succeeds as intended
- **On failure:** Action fails, must find alternative or pay cost

### Consequence Rolls
Determining severity of unavoidable event.
- **Examples:** How badly injured from forced landing, how long unconscious
- **On high roll:** Minor consequence
- **On low roll:** Severe consequence

### Discovery Rolls
Finding resources, information, or opportunities.
- **Examples:** Finding breathable air source, discovering ancient tech
- **On high roll:** Found quickly, good condition
- **On low roll:** Takes longer, damaged, incomplete

### Resource Rolls
Determining efficiency or output of systems.
- **Examples:** Water recycler output, battery drain rate, air consumption
- **On high roll:** Better than expected efficiency
- **On low roll:** Worse efficiency, higher costs

---

## Chapter 16 Example Roll Points

### Scene 1: Through the Rift

**Fixed Touchpoint A:** Bellatrix throws Ahdia through rift (Book 3 ending)
**Fixed Touchpoint B:** Ahdia unconscious on ground in The Between

**Roll 1 - Landing Severity (Consequence Roll):**
- Base roll: d20
- Modifier: +3 (Victor's training)
- **20:** Perfect landing, just winded (no injuries)
- **15-19:** Bruised but functional (no movement penalty)
- **10-14:** Twisted ankle (-2 to movement for 3 scenes)
- **5-9:** Concussion (disoriented, -2 to perception for 2 scenes)
- **1-4:** Broken rib + concussion (-3 to physical actions, -2 perception)

**Roll 2 - Unconscious Duration (Consequence Roll):**
- Base roll: d20
- Modifier: +/- from Roll 1 result
- **20:** 15 minutes (air supply: 5h 45m)
- **15-19:** 30 minutes (air supply: 5h 30m)
- **10-14:** 47 minutes (air supply: 5h 13m) [beat sheet default]
- **5-9:** 90 minutes (air supply: 4h 30m)
- **1-4:** 2+ hours (air supply: 4h, AR-Ryu emergency wake protocol)

**State Propagates:** Injuries and air supply affect Scene 2+

---

### Scene 2: Waking to Ryu's Voice

**Fixed Touchpoint A:** Ahdia unconscious
**Fixed Touchpoint B:** Ahdia awake, AR-Ryu introduced

**Roll 3 - AR-Ryu Functionality (Resource Roll):**
- Base roll: d20
- Modifier: None (new system)
- **20:** Full capability + personality matrix active early
- **15-19:** Full capability, personality develops normally
- **10-14:** Standard functionality [beat sheet default]
- **5-9:** Glitchy hologram, audio clear but visual stutters
- **1-4:** Audio only, hologram offline (visor damage from fall)

**State Propagates:** AR-Ryu limitations affect all future scenes

---

### Scene 3: The Wrong Sky

**Fixed Touchpoint A:** Ahdia surveying environment
**Fixed Touchpoint B:** Ahdia identifies ruins as destination

**Roll 4 - Environmental Scan (Discovery Roll):**
- Base roll: d20
- Modifier: +/- based on AR-Ryu functionality, injuries
- **20:** Identifies optimal path to ruins + secondary shelter option spotted
- **15-19:** Clear path identified, estimated travel time accurate
- **10-14:** Ruins visible, path uncertain [beat sheet default]
- **5-9:** Ruins visible but HUD malfunctioning, distance unclear
- **1-4:** Disoriented, multiple ruin clusters visible, unclear which is closest

---

### Scene 4: Alone

**Fixed Touchpoint A:** Ahdia realizes isolation
**Fixed Touchpoint B:** Ahdia begins walking toward ruins

**Roll 5 - Morale Check (Consequence Roll):**
- Base roll: d20
- Modifier: -2 (cosmic displacement trauma)
- **20:** Determination strengthens ("I survived Books 1-2, I'll survive this")
- **15-19:** Acceptance, moving forward
- **10-14:** Functional despite fear [beat sheet default]
- **5-9:** Panic attack, must calm self (10 minutes, air cost)
- **1-4:** Breakdown, AR-Ryu must talk her through crisis (30 minutes, air cost)

---

### Scene 5: The Ruins

**Fixed Touchpoint A:** Approaching ruins
**Fixed Touchpoint B:** Inside panic room with breathable air

**Roll 6 - Navigation Through Ruins (Action Roll):**
- Base roll: d20
- Modifier: +2 (parents' archaeology training) + injury penalties
- **20:** Direct path to panic room, arrives with 4h air remaining
- **15-19:** Efficient route, 3h 30m air remaining [beat sheet default]
- **10-14:** Wandering, wrong turns, 3h air remaining
- **5-9:** Lost in ruins, 2h air remaining when found
- **1-4:** Critically lost, finds panic room with <1h air (desperate state)

**Roll 7 - Panic Room Condition (Discovery Roll):**
- Base roll: d20
- Modifier: None (ancient facility)
- **20:** Fully functional + bonus supplies (emergency rations for 7 days)
- **15-19:** Breathable air, systems functional [beat sheet default]
- **10-14:** Breathable air, some systems offline (must repair)
- **5-9:** Marginal air quality, significant repairs needed
- **1-4:** Barely breathable, emergency only, must find better shelter

---

### Scene 6: Building Water System

**Fixed Touchpoint A:** Realizes water scarcity
**Fixed Touchpoint B:** Water system operational

**Roll 8 - Water System Build (Action Roll):**
- Base roll: d20
- Modifier: +2 (AR-Ryu guidance) - injury penalties
- **20:** 4 hours, 1.5L/day output, 0.5% battery drain
- **15-19:** 6 hours, 1.2L/day output, 0.8% battery drain
- **10-14:** 8 hours, 1L/day output, 1% battery drain [beat sheet default]
- **5-9:** 12 hours, 0.7L/day output, 1.5% battery drain
- **1-4:** 16 hours, 0.5L/day (barely sustainable), 2% battery drain

**State Propagates:** Water output and battery drain affect all future chapters

---

### Scene 7: First Night

**Fixed Touchpoint A:** Water system complete
**Fixed Touchpoint B:** Ahdia sleeps, battery status established

**Roll 9 - First Night Rest (Resource Roll):**
- Base roll: d20
- Modifier: -2 (alien environment stress) - injury penalties
- **20:** Deep sleep, recovers 1 injury penalty level
- **15-19:** Restful sleep, ready for tomorrow
- **10-14:** Fitful sleep, functional tomorrow [beat sheet default]
- **5-9:** Nightmares, exhausted tomorrow (-1 to all rolls next chapter)
- **1-4:** Insomnia, severe exhaustion (-2 to all rolls next chapter)

---

## State Tracking Between Scenes

**Injuries:**
- Track type, severity, duration
- Apply modifiers to relevant rolls
- Heal over time or with treatment

**Resources:**
- Air supply (current hours:minutes)
- Battery % (tracks to exact decimal)
- Water output (L/day)
- Food (when found)

**Morale:**
- Current mental state
- Modifiers to future morale checks
- Can improve or degrade

**Equipment Status:**
- AR-Ryu functionality level
- Battlesuit integrity
- Visor HUD status
- Water system efficiency

**Knowledge:**
- Discovered information
- Mapped areas
- Identified threats/resources

---

## Integration with Method Actor System

**Sequence:**
1. **Touchpoint A defined** (starting state)
2. **Roll dice for variable events** (outcomes determined)
3. **Touchpoint B defined** (ending state based on rolls)
4. **Method actor generates scene** using:
   - Character knowledge state
   - Roll outcomes as constraints
   - Character voice/personality
   - Emotional beats from results

**Example:**

```yaml
scene_id: "book4_ch16_scene1_rift_fall"
touchpoint_a: "Bellatrix throws Ahdia through rift"
touchpoint_b: "Ahdia unconscious on ground"

dice_rolls:
  - roll_id: "landing_severity"
    result: 12  # Twisted ankle
    consequence: "Twisted right ankle, -2 to movement for 3 scenes"

  - roll_id: "unconscious_duration"
    result: 8   # 90 minutes
    consequence: "Air supply: 4h 30m remaining"

character_knowledge_states:
  Ahdia:
    knows:
      - Bellatrix threw her through rift
      - Powers don't work here
      - Victor's training saved her spine
      - Right ankle twisted
      - Lost 90 minutes unconscious
    doesnt_know:
      - Where she is
      - If team is searching
      - How to get back
    physical_state: "Twisted ankle (-2 movement), bruised, disoriented"
    resources: "Air: 4h 30m, Battery: 98%"
```

Method actor then performs scene with those constraints.

---

## Chaos vs Control Balance

**Controlled (No Dice):**
- Major plot beats (Ahdia must survive, must reach Chapter 31 convergence)
- Character relationships (canon personalities)
- World rules (powers don't work in Between)

**Chaotic (Dice Determine):**
- Injury severity
- Resource efficiency
- Discovery timing
- Complication types
- Character state variations

**Result:** Story reaches predetermined points via unpredictable paths. Same broad strokes, different details each playthrough.

---

## Future Expansion

**Potential additions:**
- **Threat Encounters:** Roll for hostile entity discovery/aggression
- **Tech Failures:** Random equipment malfunctions
- **Resource Finds:** Unexpected supply discoveries
- **Time Anomalies:** Dimensional distortion events
- **Relationship Shifts:** NPC reaction variations (when Suzie appears)

**Combat System (if needed):**
- Initiative (d20 + modifiers)
- Attack/Defense rolls
- Damage/Healing
- Tactical positioning

---

**Status:** Framework designed, ready for Chapter 16 implementation
**Next:** Define roll sequence for Chapter 16, run TTRPG session, feed results to method actor
