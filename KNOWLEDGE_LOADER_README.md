# Go Squad Knowledge Loader

**Dynamic knowledge base loader for the Go Squad series**

## What It Does

Automatically discovers, loads, and presents all knowledge base content across the workspace:
- Character profiles
- Story bibles (artifacts, organizations, locations, powers, timelines)
- Themes and worldbuilding research
- TTRPG system documentation
- Series synopsis and planning documents

**Nothing is hard-coded.** The script dynamically scans directories and adapts as files are added or changed.

## Quick Start

### Get Essential Context (Recommended for Catch-Up)
```bash
python3 gosquad_knowledge_loader.py --essential
```

Loads and displays:
- Series synopsis (7-book arc structure)
- Corruption correction notes (critical canon fixes)
- Main character list

**Use case:** Starting a new session and need to catch up quickly.

### View Summary (Fast Overview)
```bash
python3 gosquad_knowledge_loader.py --summary
```

Shows:
- Total files and line counts
- Category breakdown
- File listings by category

**Use case:** See what's available without loading full content.

### Search Across All Files
```bash
python3 gosquad_knowledge_loader.py --search "temporal powers"
```

Searches all knowledge base files and shows:
- Files containing matches
- Context lines around matches
- Match counts per file

**Use case:** Find specific information quickly (e.g., "where did we define CADENS?", "what are Ahdia's powers?")

### Load Specific Category
```bash
python3 gosquad_knowledge_loader.py --category characters
```

Loads only files from specified category:
- `characters` - Character profiles
- `character_arcs` - Per-character arc trackers (Ahdia, Ruth, Tess, Ryu, Ben, Victor, Leah, Korede, Diana, Leta, Suzie, Jericho)
- `artifacts` - Hyper Seed, FAERIS drones
- `organizations` - CADENS, Titan Strategic
- `locations` - Facilities and settings
- `powers` - Time manipulation mechanics
- `timeline` - Book 1-2 event timelines
- `universe` - **CRITICAL** Cyclic universe cosmology, time travel mechanics
- `themes` - Core themes, arcs, worldbuilding
- `ttrpg` - TTRPG system documentation
- `book2_planning` - Book 2 story bible and beats
- `book3_planning` - Book 3 story bible and beats
- `book4_planning` - Book 4 story bible and beats
- `root` - Top-level synopsis and notes

**Use case:** Deep dive into specific aspect of the universe.

### Generate Detailed Report
```bash
python3 gosquad_knowledge_loader.py --detailed
```

Shows detailed report with content previews (first 20 lines of each file).

**Use case:** Browse content to find what you need to read fully.

### Export to JSON
```bash
python3 gosquad_knowledge_loader.py --export knowledge_base.json
```

Exports entire knowledge base as structured JSON.

**Use case:** Processing with other tools, backup, version snapshots.

## How It Works

### Automatic Discovery
The script scans the workspace for knowledge files using category patterns:

```
character_profiles/          → characters
character_arcs/              → character_arcs
story_bibles/artifacts/      → artifacts
story_bibles/organizations/  → organizations
story_bibles/locations/      → locations
story_bibles/powers and cost → powers
story_bibles/timeline/       → timeline
story_bibles/universe/       → universe (CRITICAL: cyclic cosmology)
themes/                      → themes
TTRPG/                       → ttrpg
.gosquad/                    → knowledge_base
```

Plus root files:
- `SERIES_SYNOPSIS.md`
- `README.md`

### Category System
Files are automatically categorized by their location in the directory tree. No configuration needed—just organize files logically and the script adapts.

### Flexible Output
Choose the level of detail you need:
- **Essential** - Quick catch-up (100 lines per key file)
- **Summary** - File counts and structure
- **Detailed** - Content previews (20 lines per file)
- **Full Load** - Complete content (all lines)

## Use Cases

### 1. Starting a New Session
```bash
python3 gosquad_knowledge_loader.py --essential
```
Get caught up on series structure, key characters, and critical notes.

### 2. Checking Character Details
```bash
python3 gosquad_knowledge_loader.py --category characters --detailed
```
Browse all character profiles with content previews.

### 3. Finding Specific Information
```bash
python3 gosquad_knowledge_loader.py --search "Hyper Seed"
```
Find all mentions of the Hyper Seed across the knowledge base.

### 4. Verifying Continuity
```bash
python3 gosquad_knowledge_loader.py --category timeline
```
Load all timeline files to check event sequences.

### 5. Understanding Power Mechanics
```bash
python3 gosquad_knowledge_loader.py --search "temporal charge"
```
Find all references to temporal power costs and mechanics.

### 6. Creating Knowledge Snapshot
```bash
python3 gosquad_knowledge_loader.py --export snapshots/kb_2025-01-15.json
```
Export current state of knowledge base for version control.

## Integration with /gosquad Command

The `/gosquad` slash command now uses this script for quick context loading:

```
/gosquad
```

This runs:
```bash
python3 gosquad_knowledge_loader.py --essential
```

And provides comprehensive context about:
- Series structure and status
- Core themes
- Key characters
- Major plot points
- TTRPG methodology

## Current Stats

Based on latest scan:
- **170+ files** across **13 categories**
- **17 character arc trackers** (heroes, villains, supporting cast)
- **20+ character profiles**
- **5 TTRPG guides**
- **Book 2-4 planning** (story bibles, beat sheets, session decisions)
- **Books 5-8 touchpoints** (SERIES_TOUCHPOINTS.md)
- **Comprehensive worldbuilding** (themes, research, frameworks)

### Key Planning Documents
- `SERIES_TOUCHPOINTS.md` - Complete 8-book arc guide with touchpoints, antagonists, New Earth migration
- `SERIES_SYNOPSIS.md` - Detailed Books 1-4 synopsis
- `character_arcs/README.md` - Index of all character arc trackers
- `Villain_Concepts_Books_4-7.md` - Additional antagonist concepts
- `story_bibles/universe/CYCLIC_UNIVERSE_COSMOLOGY.md` - **CRITICAL** Core time travel mechanics and cyclic universe theory

### Book 4 Key Documents (Chapters 15-31)
- `story_bibles/book 4/BOOK4_BRAIDED_TOUCHPOINTS.md` - Four-timeline structure (Ahdia/Ruth/Korede/Antagonist)
- `story_bibles/book 4/BOOK4_SIGNAL_COMMUNICATION_MECHANIC.md` - **CRITICAL** How Earth detects Ahdia (fold echoes/temporal wake), picoframe solution, THE POWERS TRUTH (her powers DO work in The Between)
- `story_bibles/book 4/book4_chapter15-21_beats.md` - TTRPG-rolled chapter beats
- `character_arcs/Ahdia_Arc_Tracker.md` - THE POWERS TRUTH section (her powers work differently, not "not at all")
- `character_arcs/Rahs_Jericho_Arc_Tracker.md` - **CRITICAL** Full mastermind arc, Bourn's asset reveal, Dr. Doom analog

## Extending the System

### Adding New Categories
Create a new directory and the script will automatically discover it on next run. To formalize a category pattern:

1. Add to `CATEGORY_PATTERNS` in `gosquad_knowledge_loader.py`:
   ```python
   CATEGORY_PATTERNS = {
       'new_directory_name': 'new_category',
       # ...
   }
   ```

### Adding New Root Files
Add important top-level files to `ROOT_FILES`:
```python
ROOT_FILES = [
    'SERIES_SYNOPSIS.md',
    'YOUR_NEW_FILE.md',
    # ...
]
```

### Custom Search Queries
Search supports regex patterns:
```bash
python3 gosquad_knowledge_loader.py --search "Book [0-9]"
```

## Architecture

```
KnowledgeBase
├── discover_files()      # Scan workspace for knowledge files
├── load_all()            # Load content from files
├── generate_summary()    # Create summary report
├── generate_detailed()   # Create detailed report with previews
├── get_essential()       # Generate quick catch-up context
├── search()              # Search across all content
└── export_json()         # Export as structured JSON

KnowledgeFile
├── path                  # File location
├── category              # Auto-detected category
├── name                  # Display name
├── content               # File contents
├── size_lines            # Line count
└── metadata              # Additional data
```

## Performance

- **Discovery:** <100ms for 37 files
- **Loading:** ~1-2 seconds for all files
- **Search:** <500ms across all content
- **Export:** ~500ms for complete JSON

## Future Enhancements

Potential additions:
- **Caching:** Cache loaded content between runs
- **Filtering:** Advanced filters (by date, author, status)
- **Diff Mode:** Compare knowledge base snapshots
- **Interactive Mode:** Browse files interactively
- **Web Interface:** HTML dashboard for knowledge base
- **Auto-update:** Watch files and reload on changes
- **Validation:** Check for broken references, missing files
- **Statistics:** Word counts, reading time estimates

## Notes

- The script is **read-only**—it never modifies source files
- All file loading is **UTF-8 encoded**
- Supports **.md, .txt, .json** files
- Hidden files are skipped (except `.gosquad/`)
- Empty files are handled gracefully
- Errors are reported but don't stop execution

## Examples

### Example 1: Quick Catch-Up
```bash
$ python3 gosquad_knowledge_loader.py --essential

🔍 Discovering knowledge base files...
✓ Discovered 37 files across 9 categories

================================================================================
GO SQUAD - ESSENTIAL CONTEXT
================================================================================

[Series synopsis, corrections, character list...]
```

### Example 2: Search for Power Costs
```bash
$ python3 gosquad_knowledge_loader.py --search "baseline"

Found 8 files with matches:

📄 story_bibles/powers and cost/Time_Manipulation.md (15 matches)
   - **Baseline:** Cellular health percentage
   - Ahdia needs ongoing treatments to prevent reaching baseline threshold
   - Treatment PREVENTS transcendence by stabilizing cellular structure
   ...
```

### Example 3: Export Knowledge Base
```bash
$ python3 gosquad_knowledge_loader.py --export kb.json

✓ Exported knowledge base to kb.json

$ ls -lh kb.json
-rw-r--r-- 1 user user 2.4M Jan 15 10:30 kb.json
```

## Questions?

This script is designed to be self-documenting and extensible. For help:
```bash
python3 gosquad_knowledge_loader.py --help
```
