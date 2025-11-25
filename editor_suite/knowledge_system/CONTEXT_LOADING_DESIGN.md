# Context Loading System - Infrastructure Design

## Problem Statement

Current system requires manual maintenance of "essential" file lists. Need dynamic, query-based context loading.

---

## Core Concept: Context Queries

Instead of:
```bash
python3 gosquad_knowledge_loader.py --essential
```

Use:
```bash
python3 gosquad_knowledge_loader.py --context "chapter:book4_ch16"
python3 gosquad_knowledge_loader.py --context "writing:book4_ch17_beats"
python3 gosquad_knowledge_loader.py --context "character:Ahdia:book4_ch15"
```

---

## File Metadata System

### Metadata Format (YAML frontmatter in each file)

```markdown
---
book: 4
chapter: 16
type: beat_sheet
timeline: between
characters: [Ahdia, AR-Ryu]
dependencies:
  - story_bibles/book 3/book3_chapter19_beats.md
  - story_bibles/book 4/SESSION_DECISIONS_2025-11-24.md
  - character_arcs/Ahdia_Arc_Tracker.md
  - story_bibles/artifacts/Hyper_Seed.md
tags: [the_between, bellatrix_prison, survival, nanotech]
---

# Book 4 - Chapter 16 Beats
[content...]
```

### Metadata Fields

- `book`: Book number
- `chapter`: Chapter number (optional)
- `type`: beat_sheet | character_arc | worldbuilding | planning | synopsis
- `timeline`: earth | between | flashback | (optional)
- `characters`: List of characters involved
- `dependencies`: Files this context requires
- `tags`: Searchable keywords

---

## Query Types

### 1. Chapter Context Query

**Query:** `--context "chapter:book4_ch16"`

**Loads:**
- Target chapter beats
- Previous chapter ending (continuity)
- Character arcs for all involved characters at that point
- Worldbuilding docs tagged in chapter metadata
- Book-level planning documents
- Dependencies listed in chapter metadata

### 2. Writing Context Query

**Query:** `--context "writing:book4_ch17_beats"`

**Loads:**
- Most recent chapter beats (for continuity)
- Character arcs current to that point
- Book planning documents
- Series synopsis
- Relevant worldbuilding

### 3. Character Context Query

**Query:** `--context "character:Ahdia:book4_ch15"`

**Loads:**
- Ahdia's arc tracker up to Chapter 15
- All chapters where Ahdia appears (Book 4)
- Related character arcs (Ruth, Ryu, etc.)
- Ahdia's character profile
- Relevant relationships

### 4. Timeline Context Query

**Query:** `--context "timeline:between:book4"`

**Loads:**
- All "between" timeline chapters (16, 18, 20, etc.)
- Ahdia's arc in The Between
- Worldbuilding: The Between, Bellatrix's prison
- Book 3 arrival beats (starting point)

### 5. Planning Context Query

**Query:** `--context "planning:book4"`

**Loads:**
- SESSION_DECISIONS documents
- EARTH_ARC_STRUCTURE
- EMOTIONAL_ARC documents
- ENDING structure
- Master planning files

---

## Dependency Graph System

### Automatic Dependency Detection

Files declare dependencies explicitly:
```yaml
dependencies:
  - story_bibles/book 3/book3_chapter19_beats.md  # What led here
  - character_arcs/Ahdia_Arc_Tracker.md           # Character state
```

### Transitive Loading

If Chapter 16 depends on Chapter 15, and Chapter 15 depends on Book 3 Ch 19, load all three.

### Circular Dependency Protection

Track loaded files, skip if already loaded.

---

## File Structure Requirements

### 1. Metadata Scanner

- Scan all markdown files
- Extract YAML frontmatter
- Build index: `knowledge_index.json`
- Update index when files change

### 2. Index Structure

```json
{
  "files": {
    "story_bibles/book 4/book4_chapter16_beats.md": {
      "book": 4,
      "chapter": 16,
      "type": "beat_sheet",
      "characters": ["Ahdia", "AR-Ryu"],
      "dependencies": [...],
      "tags": ["the_between", "survival"]
    }
  },
  "characters": {
    "Ahdia": ["path/to/file1.md", "path/to/file2.md"]
  },
  "books": {
    "4": ["path/to/file1.md", "path/to/file2.md"]
  },
  "tags": {
    "the_between": ["path/to/file1.md", "path/to/file2.md"]
  }
}
```

### 3. Query Resolver

Input: Query string
Output: List of files to load

```python
def resolve_query(query_string):
    query_type, params = parse_query(query_string)

    if query_type == "chapter":
        return resolve_chapter_context(params)
    elif query_type == "writing":
        return resolve_writing_context(params)
    elif query_type == "character":
        return resolve_character_context(params)
    # etc.
```

---

## Migration Path

### Phase 1: Add Metadata to Existing Files

- Add YAML frontmatter to beat sheets
- Add metadata to character arcs
- Add metadata to planning docs

### Phase 2: Build Index System

- Write metadata scanner
- Generate knowledge_index.json
- Update on file changes

### Phase 3: Implement Query System

- Write query parsers
- Write context resolvers
- Integrate with existing loader

### Phase 4: Deprecate Hardcoded Lists

- Remove `get_essential_context()` hardcoded paths
- Use queries instead
- Keep backward compatibility temporarily

---

## Example Usage

### Before (Hardcoded)
```bash
python3 gosquad_knowledge_loader.py --essential
# Loads manually maintained list
```

### After (Query-Based)
```bash
# Get everything needed to write Chapter 17
python3 gosquad_knowledge_loader.py --context "writing:book4_ch17"

# Get Ahdia's state at specific point
python3 gosquad_knowledge_loader.py --context "character:Ahdia:book4_ch16"

# Get all Between timeline context
python3 gosquad_knowledge_loader.py --context "timeline:between:book4"

# Multiple contexts
python3 gosquad_knowledge_loader.py --context "chapter:book4_ch16" --context "planning:book4"
```

---

## Benefits

1. **No Manual Maintenance:** Dependencies declared in files themselves
2. **Precise Context:** Only load what's needed for specific task
3. **Automatic Updates:** New files with metadata auto-discovered
4. **Flexible Queries:** Multiple ways to slice context
5. **Scalable:** Works for Books 1-8 without code changes

---

## Implementation Priority

1. Design metadata schema (DONE - this document)
2. Add metadata to Book 4 beat sheets (critical path)
3. Build index scanner
4. Implement chapter context query (most useful)
5. Expand to other query types
6. Full migration

---

**Status:** Design complete, ready for implementation
**Next Step:** Add metadata to book4_chapter16_beats.md as proof of concept
