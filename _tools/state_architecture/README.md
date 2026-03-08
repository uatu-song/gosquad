# Go Squad State Architecture

RLM-based external state management for multi-agent creative collaboration.

## Overview

This system provides queryable external state for Go Squad agents. Instead of loading entire documents into context, agents query specific information as needed.

**Core Principle:** Extend, don't replace. The existing `CHARACTER_STATE_INDEX.yaml` is the foundation.

## Files

```
_tools/state_architecture/
├── SCHEMAS.yaml      # Schema definitions for all state types
├── query.py          # Python query interface
└── README.md         # This file
```

## Schemas

### 1. Character State (existing - formalized)
- Source: `7_characters/arcs/CHARACTER_STATE_INDEX.yaml`
- Tracks: meta, arc, motives, emotional_progression, threads, chapter_states
- Query: `get_character_state("ahdia", 1)`

### 2. Location (new - GAP_001 addressed)
- Source: `5_story_bibles/locations/*.yaml`
- Tracks: physical layout, atmosphere, narrative function, choreography notes
- Query: `get_location("caledonia_memorial")`

### 3. Object/Prop (new)
- Source: `5_story_bibles/artifacts/OBJECTS_INDEX.yaml`
- Tracks: physical description, function, narrative role, possession history
- Query: `get_object("ahdia_baseline")`

### 4. Timeline/Event (existing - uses CHARACTER_STATE_INDEX)
- Query: `get_chapter_timeline(1)`

### 5. Process Log (new)
- Schema only - used for agent output validation
- Fields: query_log, domain_declaration, source_attribution, deferred_items, mode

## Query Interface

### Python API

```python
from query import StateQuery

sq = StateQuery()

# Character queries
state = sq.get_character_state("ahdia", 1)
knows = sq.character_knows("ahdia", "exile_island", 13)
who = sq.who_knows("exile_island", 13)
warnings = sq.get_canon_warnings("tess")
thread = sq.get_thread_state("ahdia", "baseline_decline", 11)

# Location queries
loc = sq.get_location("caledonia_memorial")
scenes = sq.get_scenes_at_location("caledonia_memorial")

# Object queries
obj = sq.get_object("ahdia_baseline")
owned = sq.get_objects_owned_by("ahdia")

# Timeline queries
timeline = sq.get_chapter_timeline(1)
chapters = sq.get_chapters_in_month(11)

# Relationship queries
rel = sq.get_relationship("ahdia", "ruth", chapter=7)
```

### CLI

```bash
# Character state at chapter 1
python3 query.py character ahdia 1

# Check if Ahdia knows about exile_island at chapter 12
python3 query.py knows ahdia exile_island 12

# Who knows about exile_island at chapter 13
python3 query.py who-knows exile_island 13

# Get location
python3 query.py location caledonia_memorial

# Get object
python3 query.py object ahdia_baseline

# Canon warnings for Tess
python3 query.py warnings --character tess

# Thread state
python3 query.py thread ahdia baseline_decline 11

# Timeline for chapter
python3 query.py timeline 1
```

## QueryResult

All queries return a `QueryResult` with:

```python
@dataclass
class QueryResult:
    success: bool           # Did query succeed?
    data: Any               # The result data
    source_file: str        # Path to source file
    source_section: str     # Section within file (for attribution)
    error: str              # Error message if failed
```

This enables source attribution in Process Logs.

## Adding New State

### New Location

Create `5_story_bibles/locations/[location_id].yaml` following the schema in `SCHEMAS.yaml`.

### New Object

Add entry to `5_story_bibles/artifacts/OBJECTS_INDEX.yaml` under `objects:`.

### New Character

Add entry to `7_characters/arcs/CHARACTER_STATE_INDEX.yaml` following the existing pattern.

## Integration with Go Squad Agents

Agents should:

1. **Query before assuming** - Don't guess character states
2. **Include source attribution** - Use `result.source_file` and `result.source_section`
3. **Check canon warnings** - Before generating content involving a character
4. **Respect knowledge gates** - Use `character_knows()` before revealing information

## Example: Generating a Scene

```python
from query import StateQuery

sq = StateQuery()

def pre_scene_check(character: str, chapter: int, location_id: str):
    """Pre-flight check before scene generation."""

    # 1. Get canon warnings
    warnings = sq.get_canon_warnings(character)
    print(f"Canon warnings for {character}:")
    for w in warnings.data:
        print(f"  [{w['severity']}] {w['warning']}")

    # 2. Get character state
    state = sq.get_character_state(character, chapter)
    print(f"\n{character} at ch{chapter}:")
    print(f"  Location: {state.data.get('location')}")
    print(f"  Emotional: {state.data.get('emotional')}")
    print(f"  Knows: {state.data.get('knows')}")

    # 3. Get location
    loc = sq.get_location(location_id)
    print(f"\nLocation: {loc.data['meta']['name']}")
    print(f"  Type: {loc.data['physical']['layout_type']}")

    # 4. Return sources for attribution
    return {
        'warnings_source': warnings.source_file,
        'state_source': f"{state.source_file}#{state.source_section}",
        'location_source': loc.source_file
    }
```

## Phase 1 Status

✅ Schema definitions (SCHEMAS.yaml)
✅ Location schema (GAP_001 addressed)
✅ Object/Prop schema
✅ Process Log schema
✅ Query interface (query.py)
✅ Test with Ahdia + Caledonia Memorial

## Phase 2: Process Log Integration ✓

### Process Log Generator

```python
from process_log import ProcessLog

log = ProcessLog(
    agent_role="status_tracker",
    task_id="ST_001_knowledge_check"
)

# Log queries made
log.add_query(
    query="who_knows('exile_island', 13)",
    target="archivist",
    response_summary="Found 7 characters who know"
)

# Declare domain (required)
log.declare_domain(
    task_description="Check character knowledge state",
    justification="Knowledge tracking is Status Tracker domain"
)

# Attribute sources (required for factual claims)
log.add_source(
    claim="7 characters know at chapter 13",
    source_file="CHARACTER_STATE_INDEX.yaml",
    source_section="knowledge_tracking.exile_island.awareness.ch13"
)

# Set output
log.set_output(
    content={"who_knows": ["ahdia", "ryu", "ruth", ...]},
    confidence="high"
)

# Validate
result = log.validate()
print(result.status)  # APPROVED, REJECTED, or FLAGGED
```

### Gate Validator

Validates process logs against Go Squad protocol:

**Rejection criteria:**
- Missing domain declaration
- Task declared outside domain
- Missing queries when task type requires them
- Missing source attribution for factual claims
- Character Steward missing mode declaration

**Warning flags:**
- All queries answered by self
- Complex operation with no deferrals
- Task description doesn't match role's domain keywords

### Consultation Logging

```python
from process_log import get_consultation_log

consultation_log = get_consultation_log()

# Log when Agent A queries Agent B
consultation_log.log_consultation(
    requester_role="status_tracker",
    requester_task_id="ST_001",
    responder_role="archivist",
    query="who_knows('exile_island', 13)",
    response_summary="Found 7 characters",
    response_sources=["CHARACTER_STATE_INDEX.yaml"]
)

# Get consultation chain for a task
chain = consultation_log.get_chain("ST_001")
```

### Running Tests

```bash
# Test process log demos
python3 process_log.py --demo valid
python3 process_log.py --demo missing_query
python3 process_log.py --demo missing_domain

# Run full agent workflow tests
python3 test_agent_workflow.py
```

**Next:** Real agent integration (Phase 3 when ready)
