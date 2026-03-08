# Go Squad Perspective Engine

Multi-character timeline visualization and query interface for tracking character arcs, knowledge states, and overlap moments across the story.

## Quick Start

### Generate Visualization

```bash
cd /workspaces/gosquad/_tools/perspective_engine
python generate_visualization.py
```

This creates `book2_perspective_engine.html` in the repo root.

### Query Interface (CLI)

```bash
# What does Tess know in Chapter 12?
python engine.py know -c tess -ch 12

# Who is present in Chapter 21?
python engine.py present -ch 21

# Find all overlap moments
python engine.py overlaps

# Get relationship state
python engine.py relationship -c ahdia --char2 ruth -ch 13

# Get active secrets at Chapter 8
python engine.py secrets -ch 8

# Get character arc summary
python engine.py arc -c ben

# Get chapter summary
python engine.py chapter -ch 21

# Export character scaffold
python engine.py scaffold -c tess -o tess_scaffold.yaml

# Export timeline data as JSON
python engine.py export -o timeline.json
```

### Python API

```python
from engine import PerspectiveEngine

engine = PerspectiveEngine().load()

# Query knowledge
tess_ch12 = engine.what_does_character_know('tess', 12)
print(tess_ch12['knows'])
print(tess_ch12['doesnt_know'])

# Find overlaps
overlaps = engine.find_overlaps(['ahdia', 'ruth'])
for o in overlaps:
    print(f"Ch{o.chapter}: {o.title} ({o.overlap_type})")

# Get relationship
rel = engine.get_relationship_state('tess', 'leta', 21)
print(f"{rel['state']} - {rel['notes']}")

# Get active secrets
secrets = engine.secrets_active(8)
for s in secrets:
    print(f"{s['id']}: known by {s['known_by']}")

# Export for visualization
data = engine.export_timeline_data()
```

## Data Sources

The engine reads from existing Go Squad files:

| File | Purpose |
|------|---------|
| `7_characters/arcs/CHARACTER_STATE_INDEX.yaml` | Primary data source |
| `5_story_bibles/book_2/threads/TIMELINE_DATA.js` | Event positions |

No additional data files needed - it parses your existing architecture.

## Query Types

### 1. Knowledge Queries

"What does character X know at chapter Y?"

```python
engine.what_does_character_know('ruth', 7)
# Returns: knows, learns_this_chapter, doesnt_know, believes, secrets_aware_of
```

### 2. Presence Queries

"Who is active in chapter X?"

```python
engine.who_is_present(21)
# Returns: ['tess', 'leta', 'korede', ...]
```

### 3. Overlap Detection

"When do these characters' arcs intersect?"

```python
engine.find_overlaps(['ahdia', 'ruth', 'tess'])
# Returns list of Overlap objects with chapter, type, participants
```

### 4. Relationship Queries

"What's the relationship between X and Y at chapter Z?"

```python
engine.get_relationship_state('tess', 'father', 12)
# Returns: type, state, notes
```

### 5. Secret Tracking

"What secrets are active and who knows them?"

```python
engine.secrets_active(8)
# Returns list of secrets with known_by, revealed status
```

### 6. Character Arc Summary

"Give me the full arc for character X"

```python
engine.get_character_arc('ben')
# Returns: arc summary, motives, emotional_progression, threads, active_chapters
```

### 7. Chapter Summary

"What happens in chapter X?"

```python
engine.get_chapter_summary(21)
# Returns: event, characters_present, overlaps, active_secrets, character_states
```

## Visualization Features

The HTML visualization (`book2_perspective_engine.html`) provides:

- **Multi-track timeline** - All characters on parallel tracks
- **Chapter markers** - With overlap highlighting
- **Event markers** - Color-coded by type (action/revelation/emotional/tragedy)
- **Character filtering** - Show/hide specific characters
- **Knowledge heatmap** - Who knows which secrets when
- **Overlap cards** - Multi-Steward scene identification
- **Click-to-detail** - Drill down on any event

## Use Cases

### Steward Consultations

Before writing a scene, query the engine:

```bash
# What does Ruth know and believe at this point?
python engine.py know -c ruth -ch 13

# Who else is in this scene?
python engine.py present -ch 13

# What's the relationship state?
python engine.py relationship -c ahdia --char2 ruth -ch 13
```

### Multi-Steward Coordination

Find scenes that need multiple Character Steward input:

```bash
python engine.py overlaps
```

Output shows which chapters need coordinated Steward consultations.

### Canon Verification

Check what characters should/shouldn't know:

```bash
# Does Ruth know about Exile Island in Ch10?
python engine.py know -c ruth -ch 10
# → secrets_aware_of: ['terminal_decline'] (no exile_island yet)
```

### Dramatic Irony Tracking

See knowledge distribution:

```bash
python engine.py secrets -ch 10
# Shows: exile_island known by [ahdia, ryu], terminal_decline known by [ahdia, ryu, ruth]
```

## Integration with Go Squad Workflow

### Planning Phase

1. Open `book2_perspective_engine.html`
2. Filter to relevant characters
3. Identify overlap moments
4. Query for knowledge states
5. Plan multi-Steward consultations

### Steward Consultation Phase

```python
# Load character context
scaffold = engine.export_character_scaffold('tess')

# Use in Steward prompt:
# "You are Tess. Here's your journey so far: {scaffold}"
```

### Prose Generation Phase

Verify continuity before writing:

```bash
python engine.py chapter -ch 21
# Confirms: who's present, what they know, active secrets
```

## File Structure

```
_tools/perspective_engine/
├── engine.py              # Core engine + query interface
├── visualization.html     # HTML template
├── generate_visualization.py  # Generates standalone HTML
└── README.md              # This file
```

## Future Enhancements

- [ ] Beat-level granularity (parse Chapter_*_STRUCTURE.md)
- [ ] Relationship graph visualization
- [ ] Emotional arc quantification
- [ ] Real-time sync with prose changes
- [ ] Multi-book support
