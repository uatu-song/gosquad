# Go Squad TTRPG - DM Script System

**⚠️ IMPORTANT: Story content has been moved to the main project directories.**
- **Book 3 planning/prose** → `/Book_3/`
- **Book 4 planning** → `/Book_4/`
- **Series planning** → `/_ACTIVE_REFERENCE/`

This directory (formerly named `v3`) now contains **only the TTRPG game engine and tools**.

---

A complete tabletop RPG system for running Book 3 of the Go Squad narrative, featuring:
- **Story generation** with campaign outlines and scene creation
- **Temporal powers** with resource management (TC/TS/TIP)
- **FAERIS drone** bonding system
- **d10 dice mechanics** with advantage/disadvantage
- **Stamina and health** tracking
- **Modular JSON data** architecture
- **Automated state persistence**
- **Book 1 & 2 lore integration** for rich narrative context

## Quick Start

**👉 New here? Read [GETTING_STARTED.md](GETTING_STARTED.md) for a complete walkthrough!**

### **🆕 Option 1: Prompt-Driven Story** (Recommended!)

Tell the system what you want to happen, it generates the story:

```bash
python3 interactive_story.py
```

**Example**: Type "Ahdia infiltrates CADENS" → System generates scene, runs mechanics, narrates outcome

### **🆕 Option 2: Story Generation Demo**

See complete story generation with campaigns, scenes, and mechanics:

```bash
python3 demo_story_system.py
```

### **🆕 Option 3: Interactive Campaign Builder**

Generate full campaigns and run scenes interactively:

```bash
python3 run_story_session.py
```

### **Option 3: Run Example Session**

See a complete narrative session with mechanics:

```bash
python3 example_session.py
```

### **Option 4: Interactive Mechanics Session**

Play interactively with menu system (mechanics only):

```bash
python3 start_session.py
```

### **Option 5: Test All Systems**

Run the demo to see all mechanics:

```bash
python3 core/dm_master.py
```

### **Option 6: Use as Python Library**

```python
from core.dm_master import DMSession

# Start a session
dm = DMSession()

# Make a skill check
result = dm.make_skill_check(
    'ahdia_bacchus',
    'investigation',
    'hard',
    modifiers={'FAERIS_drone': 5}
)
print(result['formatted'])

# Run combat
combat = dm.run_combat_round('ben_bukowski', 'police_officer', "Rooftop chase")

# Use temporal power
ahdia = dm.get_character_systems('ahdia_bacchus')
power_result = ahdia['temporal'].use_power('temporal_perception', context="Surveillance")
```

## Project Structure

```
TTRPG_Engine/
├── core/                      # Core game systems (Python)
│   ├── data_loader.py         # Fast cached data access
│   ├── dice_system.py         # d10 mechanics
│   ├── dm_master.py           # Main orchestrator
│   ├── narrative_engine.py    # Story generation
│   ├── story_generator.py     # Campaign/scene generation
│   ├── beat_sheet_generator.py# Beat sheet creation
│   ├── campaign_state.py      # State persistence
│   └── book3_context.py       # Book 3 lore integration
│
├── data/                      # Game data (JSON)
│   ├── characters/            # Character definitions with stats
│   ├── archetypes/            # Character archetypes
│   ├── technology/            # Equipment & FAERIS system
│   ├── powers/                # Temporal powers
│   ├── mechanics/             # DCs, injuries, Eidolon intensity
│   ├── canon/                 # Nexus events
│   ├── lore/                  # Book 1 & 2 summaries (20KB structured)
│   └── state/                 # Runtime character states
│       ├── campaigns/         # Campaign save files
│       ├── character_states/  # Character progression
│       └── saves/             # Game state snapshots
│
├── campaigns/                 # TTRPG campaign scripts (NEW)
│   ├── ahdia_rift_campaign.py        # Tess/Ahdia rift campaign
│   ├── generate_ahdia_rift.py        # Campaign generator
│   ├── ahdia_rift_campaign_log.json  # Campaign state
│   ├── chapter14_escape_results.json # Game results
│   └── book2_campaign_02.json        # Book 2 campaign data
│
├── worldbuilding_research/    # Development notes (NEW)
│   ├── Development Archives/  # Mechanics development docs
│   ├── Core Themes Guide      # Thematic research
│   ├── Educational Ecosystem  # Worldbuilding systems
│   ├── cutting edge science   # Tech research
│   └── [8+ research documents]
│
├── tools/                     # Interactive Python scripts
│   ├── interactive_story.py   # Prompt-driven story gen
│   ├── demo_story_system.py   # Full system demo
│   ├── run_story_session.py   # Campaign builder
│   └── [5+ more session runners]
│
├── docs/                      # Game system documentation
│   ├── design/                # Design documents
│   ├── reference/             # Reference materials
│   └── guides/                # User guides
│
├── reference/                 # Original source materials
│   ├── campaigns/             # Campaign templates
│   └── original/              # Source manuscripts
│
└── README.md                  # This file
```

## Core Systems

### Dice System
- d10 rolls with competency modifiers (0-10)
- Advantage/disadvantage mechanics
- Critical success (10) and critical failure (1)
- Skill challenges (multiple checks to threshold)
- Contested checks

### Temporal Powers
- **TC (Temporal Charge):** 0-100, spent to use powers
- **TS (Temporal Strain):** 0-100, accumulates with power use
- **TIP (Temporal Instability):** 0-100, reality distortions
- **Baseline:** Cellular health percentage
- 7 temporal abilities with varying costs
- Treatment system for recovery
- FAERIS synergies for enhanced abilities

### Character Systems
- **Stamina:** Action costs, exhaustion levels
- **Health:** Damage, injuries, bleeding, consciousness
- **Archetype-based:** Different stats for enhanced/elite/civilian

### Data Architecture
- Modular JSON files for all game data
- Fast cached loading (93%+ hit rate)
- Automatic state persistence
- Easy to edit and maintain

## Documentation

- **✨[Story Generation Guide](STORY_GENERATION_GUIDE.md)** - NEW! Complete story system guide
- **[DM Script Guide](docs/guides/DM_SCRIPT_COMPLETE.md)** - Complete system overview
- **[Data System Guide](docs/guides/DATA_SYSTEM_README.md)** - How to use the data system
- **[FAERIS Integration](docs/guides/FAERIS_TEMPORAL_INTEGRATION.md)** - FAERIS & temporal powers
- **[Lore System](docs/guides/LORE_SYSTEM_SUMMARY.md)** - Book 1 & 2 context system

## Testing

Each system has built-in tests:

```bash
# Test dice system
python3 core/dice_system.py

# Test temporal powers
python3 mechanics/temporal_powers.py

# Test stamina system
python3 mechanics/stamina_system.py

# Test health system
python3 mechanics/health_system.py

# Test DM master
python3 core/dm_master.py

# Test data loader
python3 core/data_loader.py
```

## Performance

- **Load time:** <10ms total initialization
- **Cache hit rate:** 93%+
- **State saves:** Automatic, <5ms
- **Memory:** ~100KB total

## Features

### Story Generation ✨NEW
✅ Campaign outline generation (5 themes)
✅ Scene generation (investigation, combat, social, temporal, rest)
✅ Full session planning with multiple scenes
✅ Character-focused narratives
✅ Book 1 & 2 lore integration
✅ NPC selection based on themes

### Game Mechanics
✅ Complete dice mechanics with modifiers
✅ Temporal powers system (TC/TS/TIP tracking)
✅ FAERIS bonding (5 levels, 4 synergies)
✅ Stamina/health tracking
✅ Character state persistence
✅ Equipment modifiers
✅ Injury system with penalties
✅ Treatment/rest mechanics

### Narrative Integration
✅ Narrative hooks and complications
✅ Suggested skill checks per scene
✅ DM notes with character context
✅ Lore-aware storytelling
✅ Relationship dynamics
✅ Emotional weight from Book 1 trauma

## Next Steps

To extend the system:

- **AI Narrative Generation:** GPT integration for dynamic storytelling
- **Investigation System:** Evidence gathering and tracking
- **Eidolon System:** Fear/anger amplification
- **Campaign State Persistence:** Save campaign progress
- **NPC Dialogue Generator:** Dynamic conversations
- **Complicity/Defiance:** Moral choice tracking
- **Branching Narratives:** Player choice consequences

## Requirements

- Python 3.7+
- No external dependencies (uses only Python stdlib)

## License

Personal project for Go Squad narrative campaign.
