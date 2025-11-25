# Beat Sheet Generator Guide

## Overview

The Beat Sheet Generator creates **story structure without prose**. Instead of full narration and dialogue, you get:
- Scene title and type
- 5-7 structural beats (what happens)
- Emotional beats (how characters feel)
- Consequences (what changes)
- Next possibilities (what could happen next)

This lets you plan scenes quickly, then write the actual prose yourself.

## Quick Start

```bash
# Generate beats for a scene
python3 beat_session.py --prompt "Your scene description here"

# View current Book 3 context
python3 beat_session.py --context

# Update plot state
python3 beat_session.py --update-plot faeris_network=seized

# Change story act
python3 beat_session.py --set-act incomprehensible_challenge
```

## Example Usage

### Basic Scene Generation

```bash
python3 beat_session.py --prompt "Ahdia confronts Diana about secretly enhancing the team"
```

Output:
```
SCENE: Revelation: Ahdia confronts Diana about secretly enhancing the
Type: Revelation
Location: unspecified
Characters: Ahdia, Diana

STORY BEATS:
  1. Ahdia and Diana meet
  2. Truth is revealed or partially revealed
  3. Initial reaction - shock, denial, or acceptance
  4. Questions asked, some answered, some deflected
  5. New understanding reached (or new confusion created)

EMOTIONAL BEATS:
  - Tension builds before revelation
  - Emotional impact of truth
  - Relationship shifts in response

CONSEQUENCES:
  - Ahdia now knows something new
  - Trust either increases or decreases
  - New questions emerge

TENSION: Increases

WHAT COULD HAPPEN NEXT:
  1. Ahdia acts on new information
  2. Other characters react to the revelation
  3. Consequences of truth begin to unfold
```

### Managing Book 3 Context

The system tracks Book 3 state in `Book3/book3_context.json`. This includes:
- Character power status (Ahdia burned out, Diana active)
- Plot milestones (FAERIS network status, Mother FAERIS state, etc.)
- Current story act

**Check context:**
```bash
python3 beat_session.py --context
```

**Update plot states:**
```bash
# Mark FAERIS network as seized
python3 beat_session.py --update-plot faeris_network=seized

# Mark Mother FAERIS as awakened
python3 beat_session.py --update-plot mother_faeris=awake

# Mark Kain as controlling CADENS
python3 beat_session.py --update-plot cadens_control=kain

# Mark artificial sun as destabilizing
python3 beat_session.py --update-plot artificial_sun=destabilizing
```

**Change story act:**
```bash
# Act 1: Confidence (Go Squad is doing well)
python3 beat_session.py --set-act confidence

# Act 2: Incomprehensible Challenge (Everything falls apart)
python3 beat_session.py --set-act incomprehensible_challenge

# Act 3: Collapse (Desperate final confrontation)
python3 beat_session.py --set-act collapse
```

## Scene Types

The system detects scene types from your prompt keywords:

### **Narrative** (Flashbacks, memories, training montages)
Keywords: `flashback`, `montage`, `memory`, `training`, `practice`, `origin`

Example: `"Flashback to when Ryu first discovered FAERIS"`

Output: Story beats without skill checks, focuses on information revealed and thematic resonance.

### **Revelation** (Secrets revealed, confrontations)
Keywords: `meet`, `reveals`, `tells`, `learns`, `confronts`, `gives`, `confesses`, `admits`

Example: `"Bourn confesses to Ryu about Mother FAERIS exploitation"`

Output: Truth revelation structure with emotional impact and trust changes.

### **Investigation** (Searching for clues, examining evidence)
Keywords: `investigate`, `search`, `examine`, `look`, `find`, `discover`

Example: `"Ahdia searches CADENS files for evidence of Kain's plan"`

Output: Clue discovery beats with pattern emergence and complications.

### **Combat** (Fights, escapes, raids)
Keywords: `fight`, `attack`, `combat`, `battle`, `defend`, `seize`, `evacuate`, `escape`, `raid`

Example: `"Go Squad evacuates as Kain seizes CADENS facility"`

Output: Combat structure with turning points, physical consequences, and tactical changes.

### **Social** (Negotiations, arguments, persuasion)
Keywords: `talk`, `negotiate`, `convince`, `persuade`, `argue`, `discuss`

Example: `"Ruth argues with Diana about taking risks"`

Output: Dialogue beats with positions stated, persuasion attempts, and relationship impacts.

### **Temporal** (Time manipulation scenes)
Keywords: `temporal manipulation`, `time freeze`, `rewind time`

Example: `"Diana uses temporal manipulation to save the team"`

Output: Power usage with temporal effects and costs. NOTE: System checks Book 3 context to see who actually has temporal powers (Ahdia burned out, Diana active).

## Book 3 Context Integration

The beat generator uses `Book3/book3_context.json` to ensure accuracy:

### Character Power Status
- **Ahdia (ahdia_bacchus)**: Powers burned out, can't use temporal abilities
- **Diana (ahdia_prime)**: Has active temporal powers, secretly enhancing team
- System won't suggest temporal power checks for Ahdia

### Plot Awareness
- FAERIS network status: operational → seized → restored
- Mother FAERIS: dormant → awakening → awake
- Kain: elected → seizing CADENS → controlling network
- Artificial sun: stable → destabilizing → collapsed

### Character Recognition
The system recognizes these names in prompts:
- Ahdia, Diana/Prime
- Ruth
- Ryu/Tanaka
- FAERIS, Mother
- Bourn/Harriet
- Kain
- Jericho
- Bellatrix
- Eidolon
- Ben, Victor, Tess, Leta, Leah

## Location Detection

Add locations to your prompts for context:
- "at Ahdia's apartment"
- "in the CADENS facility"
- "at the laboratory"
- "on the rooftop"
- "in an abandoned warehouse"

Example: `"Ruth and Ahdia talk at Ahdia's apartment"`

## Tension Control

Control scene tension with keywords:
- **High tension**: `urgent`, `emergency`, `crisis`, `desperate`
- **Low tension**: `careful`, `cautious`, `quiet`, `stealth`

Example: `"Ahdia makes a desperate escape from CADENS"`

## Workflow Example

### Planning a Story Arc

1. **Start with context check:**
   ```bash
   python3 beat_session.py --context
   ```

2. **Generate opening scene:**
   ```bash
   python3 beat_session.py --prompt "Go Squad on routine patrol with FAERIS support"
   ```

3. **Generate crisis:**
   ```bash
   python3 beat_session.py --prompt "FAERIS network suddenly goes dark during patrol"
   ```

4. **Update plot state:**
   ```bash
   python3 beat_session.py --update-plot faeris_network=seized
   ```

5. **Generate response scene:**
   ```bash
   python3 beat_session.py --prompt "Diana secretly enhances the team to compensate"
   ```

6. **Generate consequences:**
   ```bash
   python3 beat_session.py --prompt "Ruth confronts 'Ahdia' about her powers working again"
   ```

7. **Check updated context:**
   ```bash
   python3 beat_session.py --context
   ```

## Tips

1. **Be specific in prompts**: "Ahdia trains with Ruth" is better than "training scene"

2. **Use character names**: The system uses names to detect who's in the scene

3. **Update context as you go**: Mark major plot changes so later beats reflect them

4. **Don't over-specify**: The system generates structure, not prose. Let it be loose.

5. **Scene types are suggestions**: If a scene gets tagged wrong, the beats are still useful structure

6. **Location optional**: Only add if it matters to the scene

7. **Iterate quickly**: Generate beats, see what works, adjust and regenerate

## Output Structure

Every beat sheet includes:

- **Scene Title**: Auto-generated from prompt
- **Type**: Scene category (revelation, combat, etc.)
- **Location**: Where it happens
- **Characters**: Who's present
- **Story Beats**: 5-7 structural points
- **Emotional Beats**: How characters feel
- **Consequences**: What changes
- **Tension**: Increases/decreases/peaks/steady
- **What Could Happen Next**: 3 continuation suggestions

You take these beats and write the actual prose, dialogue, and details yourself.

## Files

- `beat_session.py` - Main CLI tool
- `core/beat_sheet_generator.py` - Beat generation logic
- `core/book3_context.py` - Context manager
- `Book3/book3_context.json` - Current Book 3 state (auto-updates)

## Philosophy

**The system gives you structure, you add the art.**

Beat sheets are:
- ✓ Story architecture
- ✓ Structural suggestions
- ✓ Quick planning tool
- ✗ Not final prose
- ✗ Not prescriptive
- ✗ Not limiting your creativity

Use beats as scaffolding, then write your own way.
