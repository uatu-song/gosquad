# Getting Started with Go Squad DM System - Book 3

## 🎮 Quick Start - Three Ways to Play

### 1. **Run the Example Session** (Recommended First Time)

See a complete narrative session in action:

```bash
python3 example_session.py
```

This runs a pre-scripted session showing:
- Investigation checks with modifiers
- Combat between characters
- Temporal power usage
- Resource management
- Recovery mechanics

**Perfect for learning how the system works!**

---

### 2. **Interactive Session** (For Actual Play)

Launch the interactive menu system:

```bash
python3 start_session.py
```

**Note:** This requires an interactive terminal. You can:
- Make skill checks
- Run combat rounds
- Use Ahdia's temporal powers
- Check character status
- Manage rest/recovery
- View session summaries

**Perfect for guided gameplay!**

---

### 3. **Write Your Own Session** (Advanced)

Use the DM system as a Python library:

```python
from core.dm_master import DMSession

# Initialize
dm = DMSession()

# Make a check
result = dm.make_skill_check(
    'ahdia_bacchus',
    'investigation',
    'hard',
    modifiers={'FAERIS_drone': 5}
)

print(result['formatted'])
# Ahdia Bacchus: d10=8 + 7 (competency) +5 (mods) = 20 vs DC 20 → SUCCESS
```

**Perfect for custom campaigns!**

---

## 📋 Available Characters

- `ahdia_bacchus` - Hyper Temporalist (has temporal powers)
- `ruth_carter` - Medic/Tactical Leader
- `ben_bukowski` - Combat Specialist
- `victor_hernandez` - Combat Specialist
- `leah_turner` - Investigator
- `tess_whitford` - Stealth Specialist
- `leta_thompson` - Tech Specialist

---

## 🎲 Core Mechanics

### Skills
- `combat` - Fighting, attacking
- `investigation` - Finding clues, analyzing
- `stealth` - Sneaking, hiding
- `medical` - Healing, treating
- `leadership` - Commanding, inspiring
- `tech` - Hacking, technology

### Difficulty Levels
- `trivial` (DC 5) - Almost always succeeds
- `easy` (DC 10) - Usually succeeds
- `moderate` (DC 15) - 50/50 chance
- `hard` (DC 20) - Difficult
- `very_hard` (DC 25) - Very difficult
- `nearly_impossible` (DC 30) - Extremely difficult

### Dice System
- Roll d10 + competency (0-10) + modifiers
- Natural 10 = **Critical Success** 🎯
- Natural 1 = **Critical Failure** ⚠️
- Advantage = roll 2d10, take higher
- Disadvantage = roll 2d10, take lower

---

## ⚡ Ahdia's Temporal Powers

Available powers (from `data/powers/temporal_powers.json`):

1. **temporal_perception** - See 6 seconds into future (TC: 5, TS: 2)
2. **temporal_echo** - Leave echo in time (TC: 10, TS: 5)
3. **probability_collapse** - Manipulate outcomes (TC: 25, TS: 15, TIP: 3)
4. **temporal_anchor** - Freeze time for minutes (TC: varies, TS: varies)
5. **causal_thread** - Read object history (TC: 15, TS: 8)
6. **temporal_rewind** - Rewind 30 seconds (TC: 35, TS: 20, TIP: 5)
7. **temporal_fracture** - Timeline splits (TC: 50, TS: 30, TIP: 10)

### Resource Pools
- **TC (Temporal Charge):** 0-100, spent to use powers
- **TS (Temporal Strain):** 0-100, accumulates with use (dangerous at 96+)
- **TIP (Temporal Instability):** 0-100, reality distortion (CADENS watches)
- **Baseline:** Cellular health percentage (needs treatment below 50%)

### Recovery
- **Rest (1h):** +5 TC per hour
- **Sleep (8h):** +40 TC, -3 TS
- **Treatment (Ruth):** +6% baseline, -5 TS
- **Treatment (Ryu):** +6% baseline, -25 TS

---

## 🏥 Health & Stamina

### Health System
- Max health based on archetype (enhanced=150, elite=120, skilled=90)
- Injuries have severity: minor, moderate, serious, critical, fatal
- Each injury applies a penalty to rolls
- Bleeding injuries worsen over time

### Stamina System
- Used for actions (sprint, combat, climb, etc.)
- Exhaustion levels (0-3) when stamina is low
- Penalties from exhaustion: -2 to -10
- Short rest recovers some, long rest recovers more

---

## 💾 State Persistence

Character state automatically saves to `data/state/character_states/`:
- Temporal resources (Ahdia only)
- Power cooldowns
- Usage logs with timestamps
- Health and stamina

You can check Ahdia's state anytime:
```bash
cat data/state/character_states/ahdia_bacchus.json
```

---

## 📊 Example Workflow

1. **Start a session:**
   ```bash
   python3 example_session.py
   ```

2. **See dice rolls in action:**
   - d10 rolls with competency modifiers
   - Critical successes and failures
   - Success/failure narratives

3. **Watch resource management:**
   - Ahdia's TC/TS/TIP tracked automatically
   - State saves after every action
   - Recovery mechanics demonstrated

4. **Try interactive mode:**
   ```bash
   python3 start_session.py
   ```

---

## 🔧 Testing Individual Systems

Test each component:

```bash
# Test dice system
python3 core/dice_system.py

# Test temporal powers
python3 mechanics/temporal_powers.py

# Test stamina system
python3 mechanics/stamina_system.py

# Test health system
python3 mechanics/health_system.py

# Test DM master orchestrator
python3 core/dm_master.py
```

---

## 📚 Documentation

- **[README.md](README.md)** - Project overview
- **[DM_SCRIPT_COMPLETE.md](docs/guides/DM_SCRIPT_COMPLETE.md)** - Complete system guide
- **[DATA_SYSTEM_README.md](docs/guides/DATA_SYSTEM_README.md)** - Data architecture
- **[FAERIS_TEMPORAL_INTEGRATION.md](docs/guides/FAERIS_TEMPORAL_INTEGRATION.md)** - FAERIS & temporal powers
- **[LORE_SYSTEM_SUMMARY.md](docs/guides/LORE_SYSTEM_SUMMARY.md)** - Book 1 & 2 context

---

## ✨ Ready to Play!

**Recommended first steps:**

1. Run the example session to see everything in action
2. Read the output to understand the narrative flow
3. Check `data/state/character_states/ahdia_bacchus.json` to see state tracking
4. Try the interactive session for hands-on practice
5. Start writing your own campaign scenes!

**Have fun running Book 3 of the Go Squad campaign!** 🎲📖

---

## 📖 Story Context

**Book 1:** Original Go Squad forms, Firas dies stopping Kain (WRITTEN)
**Book 2:** Presidential campaign year, Kain wins election (PLANNED - see `reference/campaigns/book2_campaign_02.json`)
**Book 3:** This campaign - What happens AFTER Kain becomes President (PLAYABLE NOW)
