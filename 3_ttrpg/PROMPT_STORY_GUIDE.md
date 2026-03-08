# Prompt-Driven Story System

## What Is This?

A **dynamic narrative engine** where you tell the system what you want to happen, and it generates the story in real-time with full game mechanics integration.

## How to Use

### Start the Interactive Session

```bash
python3 interactive_story.py
```

### Tell Your Story

Just type what you want to happen:

```
What happens? > Ahdia infiltrates a CADENS facility to steal evidence about Kain
```

The system will:
1. **Generate the scene** (setting, hook, complications)
2. **Suggest skill checks** to resolve the action
3. **Roll dice** and narrate outcomes
4. **Ask what happens next**

## Example Session

```
What happens? > Ahdia sneaks into a CADENS facility

──────────────────────────────────────────────────────────────────────
  GENERATING SCENE
──────────────────────────────────────────────────────────────────────

**Setting**: CADENS facility

Ahdia Bacchus has received a tip about Kain's activities. Time to investigate.

**Actions to resolve:**
  1. Ahdia Bacchus must make a investigation check (hard)
  2. Ahdia Bacchus must make a stealth check (moderate)
  3. Ahdia Bacchus must make a tech check (very_hard)

Run these checks? (y/n) > y

──────────────────────────────────────────────────────────────────────
  RESOLVING ACTIONS
──────────────────────────────────────────────────────────────────────

**Ahdia Bacchus** attempts a **stealth** check...
Ahdia Bacchus: d10=8 + 8 = 16 vs DC 15 → SUCCESS by 1
Result: **Narrow Success**

✓ **Success.** The objective is achieved.

Ideas for what to do next:
  1. Capitalize on the success
  2. Ahdia uses temporal powers
  3. Search for clues

What happens? > Ahdia finds encrypted files and must decrypt them quickly

[System generates tech challenge scene...]

What happens? > Guards arrive, Ahdia uses temporal freeze to escape

[System generates temporal powers scene with TC/TS tracking...]
```

## Commands

### Story Prompts
Just type what you want:
- `Ahdia infiltrates CADENS`
- `Ruth treats Ahdia's injuries`
- `FAERIS detects an ambush`
- `Ben and Tess interrogate a suspect`
- `Combat breaks out on the rooftop`

### Status Commands
- `status ahdia_bacchus` - Check character health, stamina, temporal resources
- `context` - View current characters, location, recent events
- `suggestions` - Get ideas for what to do next
- `save mysession` - Save your story
- `load mysession` - Continue a saved story
- `quit` - End session

## What The System Understands

### Characters
Detects character names automatically:
- Ahdia, Ruth, Ben, Victor, Leah, Tess, FAERIS, Leta

### Actions
Recognizes action types:
- **Investigation**: infiltrate, search, examine, investigate
- **Combat**: fight, attack, defend, battle
- **Social**: talk, negotiate, convince, persuade
- **Temporal**: temporal, time, freeze, powers
- **Rest**: rest, recover, heal, sleep

### Locations
Picks up on locations:
- CADENS facility
- Police station
- Warehouse
- Rooftop
- And generates appropriate settings

### Tension Levels
Adjusts based on keywords:
- **High**: urgent, emergency, crisis, desperate
- **Low**: careful, cautious, quiet, stealth

## Features

### Automatic Scene Generation
- Setting appropriate to your prompt
- Narrative hooks
- Complications
- Suggested skill checks

### Full Mechanics Integration
- Dice rolls (d10 + competency)
- Success/failure narration
- Critical successes and failures
- Complications on failures

### Context Tracking
The system remembers:
- Who's present
- Current location
- Recent events
- Tension level

### Dynamic Suggestions
After each prompt, get ideas for what to do next based on:
- Success/failure of checks
- Characters present
- Story tension

### Character Systems
Full integration with:
- Health and injuries
- Stamina and exhaustion
- Temporal powers (TC/TS/TIP)
- Equipment and bonuses

### Save/Load
Save your story and continue later:
```
What happens? > save my_ahdia_story
✓ Session saved to my_ahdia_story.json

[Later...]
What happens? > load my_ahdia_story
✓ Session loaded from my_ahdia_story.json
```

## Example Prompts

### Investigation
- `Ahdia infiltrates Kain's campaign headquarters`
- `Ben and Tess investigate the police evidence locker`
- `FAERIS scans the warehouse for threats`

### Combat
- `Guards discover Ahdia, combat breaks out`
- `Ruth defends the medical supplies from looters`
- `Victor fights off enhanced police officers`

### Social
- `Ahdia negotiates with Director Bourn`
- `Tess confronts her father about the corruption`
- `Ben tries to convince a witness to testify`

### Temporal Powers
- `Ahdia uses temporal freeze to escape`
- `Ahdia glimpses the future to avoid danger`
- `Ahdia's powers spike dangerously high`

### Rest & Recovery
- `The team rests at a safe house`
- `Ruth treats Ahdia's cellular degradation`
- `Ahdia sleeps to recover temporal strain`

### Complications
- `The investigation goes wrong`
- `Reinforcements arrive during the fight`
- `Ahdia's baseline drops critically low`

## Tips

### Be Specific
❌ `Something happens`
✓ `Ahdia sneaks into the CADENS lab to steal Ryu's research`

### Include Characters
❌ `Someone investigates`
✓ `Ben and Tess investigate the police station`

### Set the Scene
❌ `Fight`
✓ `Combat breaks out on the rooftop during the thunderstorm`

### Chain Actions
Follow the story beats:
1. Setup: `Ahdia infiltrates CADENS`
2. Complication: `Security detects her presence`
3. Response: `Ahdia uses temporal powers to escape`
4. Consequence: `Ruth must treat Ahdia's elevated temporal strain`

### Use Context Commands
Check status regularly:
```
What happens? > status ahdia_bacchus
Health: 150/150
Stamina: 120/150
Temporal Resources:
  TC: 75/100
  TS: 35/100
  TIP: 8/100
```

## How It Works

1. **Prompt Parsing**: System analyzes your prompt for characters, actions, locations
2. **Scene Generation**: Uses story generator to create appropriate scene
3. **Context Integration**: Applies recent events and current state
4. **Mechanics Resolution**: Runs dice rolls with full game system
5. **Outcome Narration**: Generates narrative based on results
6. **Continuation**: Suggests what could happen next

## Lore Integration

The system knows:
- Book 1 & 2 backstory
- Character relationships
- Trauma and motivations
- World state (Kain's presidency, CADENS, etc.)
- Temporal power mechanics
- Equipment and bonuses

All narration is **lore-aware** and **character-consistent**.

## Comparison to Pre-Generated Campaigns

| Pre-Generated Campaigns | Prompt-Driven Stories |
|------------------------|----------------------|
| Fixed structure | Freeform improvisation |
| Pre-planned scenes | Dynamic scene generation |
| Campaign outline first | Make it up as you go |
| Best for traditional play | Best for creative exploration |

Both systems share:
- Same game mechanics
- Same lore integration
- Same character systems
- Save/load functionality

## Advanced Usage

### Multi-Character Scenes
```
What happens? > Ruth and Ben investigate together while Ahdia provides overwatch
```

System will generate checks for all characters present.

### Continuing Failed Actions
```
What happens? > Ahdia tries to hack the terminal
[FAILURE]

What happens? > Ahdia calls FAERIS for help with the decryption
```

### Building Tension
```
What happens? > Ahdia carefully investigates the quiet warehouse
[Low tension scene]

What happens? > Suddenly, Tank cops burst through the door!
[High tension scene]
```

### Using Character Abilities
```
What happens? > status ahdia_bacchus
[Check TC: 85/100]

What happens? > Ahdia uses temporal perception to predict the ambush
[Temporal scene generated, TC reduced]
```

## Files

- `core/narrative_engine.py` - Core prompt-driven engine
- `interactive_story.py` - Interactive terminal runner
- `PROMPT_STORY_GUIDE.md` - This guide

## Troubleshooting

**Issue**: Scene doesn't match my prompt
**Solution**: Be more specific about characters, actions, location

**Issue**: Wrong characters appear
**Solution**: Name specific characters in your prompt

**Issue**: Can't find character for status check
**Solution**: Use full character ID (e.g., `ahdia_bacchus` not `ahdia`)

**Issue**: Want to undo a prompt
**Solution**: Load a saved session from before that prompt

## Get Started

```bash
python3 interactive_story.py
```

Then just start telling your story!

```
What happens? > Ahdia wakes up after Kain's election victory, realizing time is running out
```

The system handles the rest!
