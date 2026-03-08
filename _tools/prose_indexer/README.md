# Prose Indexer

A bidirectional indexing system for Go Squad prose. Tracks entity appearances, canonical values, and detects drift between prose and established canon.

## Core Principle

**Prose stays prose.** The codex is a parallel index that tracks:
- Where entities appear (location coordinates)
- What their canonical values are
- When values were established
- What drifts from canon

## Directory Structure

```
_tools/prose_indexer/
├── prose_indexer.py      # Main ingestion script
├── drift_detector.py     # Drift detection mode
├── schemas/
│   └── CODEX_SCHEMA.yaml # Schema definition
├── logs/                 # Process logs
└── README.md

8_codex/
├── book_1/
│   └── codex.yaml
├── book_2/
│   └── codex.yaml
└── CODEX_MASTER.yaml     # Cross-book canonical values (future)
```

## Quick Start

### 1. Index a Single Chapter

```bash
cd /workspaces/gosquad
python _tools/prose_indexer/prose_indexer.py ingest \
    6_manuscript/book_2/chapter_01.md \
    --book 2 --chapter 1
```

### 2. Index All Chapters in a Book

```bash
python _tools/prose_indexer/prose_indexer.py ingest-all \
    6_manuscript/book_2/ \
    --book 2
```

### 3. Check Indexing Status

```bash
python _tools/prose_indexer/prose_indexer.py status
```

### 4. Run Drift Detection

```bash
python _tools/prose_indexer/drift_detector.py validate 2
```

### 5. Generate HTML Drift Report

```bash
python _tools/prose_indexer/drift_detector.py validate 2 --format html
```

## Coordinate System

Coordinates preserve the beat structure for queryability:

```
b2:ch1:beat11:p2:s1
│  │   │      │  └── Sentence 1
│  │   │      └───── Paragraph 2
│  │   └──────────── Beat 11
│  └──────────────── Chapter 1
└─────────────────── Book 2
```

**Why beats matter:** "Show me all Ahdia appearances in beat 11" is meaningful. "Show me all appearances in paragraph 47" is not.

## What Gets Indexed

### Entities
- **Characters**: Names, aliases, pronouns (with resolution confidence)
- **Locations**: Named places and settings
- **Objects**: Significant items, technology, artifacts
- **Time Markers**: Explicit time references

### Tracking
- **Appearances**: Every mention with coordinate
- **Attributes**: Canonical values with establishment point
- **Relationships**: Between entities
- **Setup/Payoff**: Narrative callbacks

### Proposed Entities
Unrecognized names are flagged as `status: proposed` and logged for Director approval. They don't become canonical until confirmed.

## Pronoun Resolution

The indexer attempts pronoun resolution with confidence flagging:

| Confidence | Condition | Action |
|------------|-----------|--------|
| `high` | Single candidate of matching gender in recent context | Index automatically |
| `medium` | Multiple candidates but one is clearly most recent | Index with flag |
| `low` | Multiple recent candidates, unclear | Flag for review |
| `ambiguous` | Cannot determine | Do not index, log only |

## Drift Detection

Drift types (from `CODEX_SCHEMA.yaml`):

| Type | Severity | Description |
|------|----------|-------------|
| `value_mismatch` | critical | Prose contradicts canonical value |
| `knowledge_violation` | critical | Character knows something before reveal point |
| `forbidden_association` | critical | Entity paired with forbidden term (e.g., Victor + "wife") |
| `timeline_inconsistency` | critical | Time markers conflict |
| `relationship_contradiction` | moderate | Relationship described differently |
| `alias_unknown` | warning | Name not in known aliases |
| `pronoun_ambiguity` | info | Pronoun couldn't be resolved |

### Integration with ENTITY_CATALOG

Drift detection reads from `entity_catalog/ENTITY_CATALOG.yaml`:

- `forbidden_associations`: Terms that must never appear with this entity
- `forbidden_knowledge_before`: Knowledge items with reveal points
- `book2_baseline_tracking`: Ahdia's baseline values per chapter

## Process Logging

All operations are logged to `_tools/prose_indexer/logs/`:

```
2026-01-18T14-30-00_ingest.yaml
2026-01-18T15-00-00_drift_report_book2.yaml
```

### Verbosity Modes

- **Default (verbose)**: Logs every entity match, pronoun resolution attempt, time marker found
- **Summary (`--summary`)**: Logs only operation-level stats

```bash
# Verbose (default)
python prose_indexer.py ingest chapter_01.md --book 2 --chapter 1

# Summary only
python prose_indexer.py ingest chapter_01.md --book 2 --chapter 1 --summary
```

## Workflow

### Prose → Codex (Writing Populates Index)

1. Write prose in `6_manuscript/book_N/chapter_XX.md`
2. Run `prose_indexer.py ingest` to parse and index
3. Review proposed entities, approve or reject
4. Run `drift_detector.py validate` to check consistency

### Codex → Prose (Drift Detection)

1. Canonical values established in codex
2. New prose written
3. `drift_detector.py` compares prose against codex
4. Drift report shows mismatches
5. Either fix prose or update canon (with approval)

## Integration Points

| System | Integration |
|--------|-------------|
| `ENTITY_CATALOG.yaml` | Character definitions, forbidden associations |
| `CHARACTER_STATE_INDEX.yaml` | Character state per chapter |
| `SCHEMAS.yaml` | Shared enums (relationship_types, arc_types) |
| Process logs | Agent workflow audit trail |

## Example Codex Entry

```yaml
characters:
  CHAR_001:
    canonical_name: "Ahdia Sade Bacchus"
    status: canonical
    aliases_in_prose:
      - "Ahdia"
      - "Auerbach"
    appearances:
      - location: "b2:ch1:beat1:p1:s3"
        context: "Introduced in penthouse, monitoring feeds"
        reference_form: "Ahdia"
        reference_type: name
      - location: "b2:ch1:beat1:p1:s4"
        context: "Adjusting hoodie"
        reference_form: "she"
        reference_type: pronoun
        pronoun_resolution:
          resolved_to: CHAR_001
          confidence: high
          reason: "single candidate of matching gender"
    attributes:
      penthouse_temperature:
        canonical_value: "cold"
        established_at: "b2:ch1:beat1:p1:s4"
        source: prose
        mentions:
          - location: "b2:ch1:beat1:p1:s4"
            value_in_prose: "The penthouse was cold—she kept it that way"
            status: canonical
```

## Future Enhancements

- [ ] `approve` command for proposed entities
- [ ] `update-canon` command with Director confirmation
- [ ] Cross-book `CODEX_MASTER.yaml` generation
- [ ] Theme extraction
- [ ] Setup/payoff tracking
- [ ] Location and object extraction
- [ ] Web UI for drift review
