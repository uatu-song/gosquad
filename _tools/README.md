# Go Squad Tools

**Purpose:** Tools for managing the Go Squad series development

---

## Perspective Engine

**Location:** `perspective_engine/`

Multi-character timeline visualization and query interface. Reads from `CHARACTER_STATE_INDEX.yaml`.

**Quick Start:**
```bash
cd perspective_engine

# Query what a character knows
python engine.py know -c tess -ch 12

# Find multi-Steward scenes (overlaps)
python engine.py overlaps

# Get chapter summary
python engine.py chapter -ch 21

# Generate HTML visualization
python generate_visualization.py
```

**Output:** `book2_perspective_engine.html` (open in browser)

See `perspective_engine/README.md` for full documentation.

---

## Prose Indexer

**Location:** `prose_indexer/`

AI slop detection and entity indexing for manuscript files.

**Usage:**
```bash
python prose_indexer/prose_indexer.py slop --book 2
python prose_indexer/prose_indexer.py ingest --book 2
```

---

## Knowledge Loaders

**Purpose:** Load GoSquad series context for AI assistants

### gosquad_knowledge_loader.py
Base knowledge loader - always works, no API dependencies
```bash
python3 gosquad_knowledge_loader.py --essential
python3 gosquad_knowledge_loader.py --summary
```

### gosquad_knowledge_loader_advanced.py
Enhanced loader with AI-powered features (requires API key)
```bash
python3 gosquad_knowledge_loader_advanced.py --essential
```

---

## Chess Narrative Engine

**Spec:** `chess_narrative_engine_spec.md`

Technical specification for building a professional chess-to-narrative mapping engine using Stockfish WASM. The classroom prototype is at `/workspaces/gosquad/Chess_Narrative_Engine_6.8.html`.

---

## Slash Command

The `/gosquad` slash command loads series context:
- Series overview (7-book arc)
- Character profiles and corrections
- Major plot points
- Canon corrections
