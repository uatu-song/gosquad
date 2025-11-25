# Knowledge System

**Purpose:** Load GoSquad series context for AI assistants

**NOTE:** These are NOT editing tools. They load story bibles, character profiles, and series information to provide context when working with AI assistants.

## Tools

### gosquad_knowledge_loader.py
**Purpose:** Base knowledge loader - always works, no API dependencies
- Discovers all knowledge base files
- Loads essential context
- Works offline

**Usage:**
```bash
python3 gosquad_knowledge_loader.py --essential
python3 gosquad_knowledge_loader.py --summary
```

### gosquad_knowledge_loader_advanced.py
**Purpose:** Enhanced loader with AI-powered features (optional)
- Everything from base loader
- AI-powered analysis (requires API key)
- Advanced querying

**Usage:**
```bash
python3 gosquad_knowledge_loader_advanced.py --essential
```

## Slash Command

The `/gosquad` slash command uses these loaders to bring AI assistants up to speed on:
- Series overview (7-book arc)
- Character profiles and corrections
- Major plot points
- Canon corrections (e.g., Isaiah killed by police, NOT Tess)

## When to Use

Use at the start of a new AI session to load series context before:
- Editing manuscripts
- Planning future books
- Checking continuity
- Discussing character arcs

## Not Editing Tools

These don't analyze or edit your manuscript. They just load story context so AI assistants understand your world.
