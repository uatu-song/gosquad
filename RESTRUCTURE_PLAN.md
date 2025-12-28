# GoSquad Repository Restructure Plan

**Date:** 2025-12-28
**Purpose:** Adopt RESONANCE workflow improvements, clean up redundancy, establish clear conventions
**Status:** EXECUTED - Completed 2025-12-28

---

## Goals

1. **Adopt RESONANCE innovations** that improve the workflow
2. **Clean up redundancy** and clarify file hierarchy
3. **Establish conventions** that persist across sessions
4. **Make context loading faster** with clear entry points

---

## Phase 1: Create Missing Core Documents

These documents don't exist yet but would significantly improve the workflow.

### 1.1 GOSQUAD_PROSE_VOICE.md (NEW)

**Location:** `/workspaces/gosquad/GOSQUAD_PROSE_VOICE.md`

**Purpose:** Capture Joe's specific syntactic signatures with examples (not just metrics).

**Content outline:**
```markdown
# Go Squad Series - Prose Voice Guide

## Core Philosophy
- Voice trumps technical polish
- Density is a feature
- Trust the reader

## Syntactic Signatures

### Ahdia's Internal Monologue
- Pop culture references as processing framework
- Self-deprecating running commentary
- Rambling, self-correcting ("Wait, no—")
- Examples from Book 1: [extracted]

### Action Scene Rhythm
- Short declarative beats
- Fragments for impact
- Sensory punctuation between action
- Examples from Book 1: [extracted]

### Dialogue Patterns
- Contractions always
- Interruptions with em-dashes
- Character-specific vocabulary
- Examples per character: [extracted]

## What NOT to Write
- Formal internal monologue
- Over-explained emotional beats
- Purple prose in action
```

**Source:** Extract patterns from `book1_manuscript.txt` and existing `GO_SQUAD_WRITING_STYLE_GUIDE.md`.

---

### 1.2 THEMATIC_CONSTRAINTS.md (NEW)

**Location:** `/workspaces/gosquad/context/THEMATIC_CONSTRAINTS.md`

**Purpose:** Protect thematic integrity (like RESONANCE does), not just factual accuracy.

**Content outline:**
```markdown
# Go Squad - Thematic Constraints

## Core Thesis
"You don't have to be fixed to be worthy."

---

## BLOCKING Constraints (Will reject draft)

### The Gift Paradigm
| WRONG | Characters earning/deserving powers through virtue |
| WRONG | Powers as punishment or reward |
| WRONG | "You deserve this" / "You've proven yourself" |
| RIGHT | Powers arrive without consent |
| RIGHT | Worthiness is irrelevant to power |
| RIGHT | The question is what you do WITH the gift |

### Binary Thinking (Ahdia's Arc)
| WRONG | Ahdia finding "the answer" |
| WRONG | Clear good/evil resolution |
| WRONG | "Now I understand everything" |
| RIGHT | Both/and rather than either/or |
| RIGHT | Acceptance without resolution |
| RIGHT | DBT progression: holding contradictions |

### Villain Complexity
| WRONG | Kain as mustache-twirling evil |
| WRONG | Easy moral clarity |
| WRONG | Eidolon as purely malevolent |
| RIGHT | Every antagonist believes something defensible |
| RIGHT | The audience can feel the pull of each position |
| RIGHT | Eidolon amplifies existing fear (doesn't create) |

---

## WARNING Constraints (Flag for review)

### Lecture Mode
| WRONG | Characters explaining the theme |
| WRONG | Speeches about power/responsibility |
| RIGHT | Embody, don't articulate |
| RIGHT | Actions and images carry weight |

### Power Mechanics
| WRONG | Powers with no cost |
| WRONG | Ignoring cellular degradation |
| RIGHT | Every temporal use has physical cost |
| RIGHT | Baseline tracking is narrative, not just mechanical |
```

---

### 1.3 CLAUDE_PROTOCOL.md (NEW)

**Location:** `/workspaces/gosquad/CLAUDE_PROTOCOL.md`

**Purpose:** Explicit LLM collaboration preferences (like RESONANCE's "What Joe Expects").

**Content outline:**
```markdown
# Claude Collaboration Protocol

## Your Role
You are a collaborator, not an author. Joe provides structural vision, thematic direction, and editorial judgment. You execute: drafting prose, tracking continuity, managing data files.

## Session Start
1. Read HANDOFF.md first
2. Load /gosquad or run knowledge loader
3. Check current chapter state in entity_catalog/

## Working Style

### Do:
- Execute immediately when the task is clear
- Accept correction without defensiveness
- Be concise—extra words are friction
- Read source files before working (don't trust summaries)
- Mark todos as complete immediately after finishing

### Don't:
- Confirm when you should act ("Shall I fix this?" → Just fix it)
- Apologize when you should deliver
- Add unrequested features or "improvements"
- Surface subtext into text
- Connect dots explicitly that should remain implicit

## The Key Dynamic
> "The user provides structural vision; Claude extrapolates and writes prose. Context engineering prevents hallucination/drift."

## What Joe May Withhold
Major reveals may be compartmentalized during drafting to prevent telegraphing. Don't push to know everything. Trust the structure.

## Session End
When Joe says "end session":
1. Update HANDOFF.md with work completed
2. Note any decisions made or constraints discovered
3. Update relevant YAML/tracking files
4. Do NOT create new documentation files unless requested
```

---

### 1.4 CALLBACK_TRACKER.md (NEW)

**Location:** `/workspaces/gosquad/story_bibles/CALLBACK_TRACKER.md`

**Purpose:** Consolidated seed/payoff tracking across all books.

**Content outline:**
```markdown
# Callback Tracker - Seeds and Payoffs

## Active Seeds (Awaiting Payoff)

| Setup | Book.Ch | Payoff Target | Status |
|-------|---------|---------------|--------|
| Firas's final chess move | B1.28 | B2.15 | PENDING |
| Ruth's treatment refusal | B2.7 | B2.20 | PENDING |
| AR-Ryu memory upload mechanic | B2.14 | B3.? | ACTIVE |
| "No better time than here" | B1.3 | B2.24 | ACTIVE |
| Geneva's true identity (Bellatrix) | B2.1 | B3.Gamma | ACTIVE |
| Prime's baseline degradation | B2.1 | B3.1 | TRACKING |

## Paid Callbacks

| Setup | Book.Ch | Payoff | Book.Ch |
|-------|---------|--------|---------|
| [To be populated from beat sheets] | | | |

## Callback Rules
- Don't add new seeds without documenting here
- Mark PAID immediately when payoff lands
- If a seed becomes irrelevant, mark ABANDONED with reason
```

---

## Phase 2: Consolidate and Clean Up

### 2.1 Archive Orphaned Files

**Action:** Move to `/workspaces/gosquad/_archive/legacy_profiles/`

These are extension-less files in `character_profiles/` that appear to be legacy:
- `Ahdia Auerbach`
- `BellatrixNaima`
- `Ben Bukowski`
- `Bentley Mack`
- `Chief John Whitford`
- `Cosmic Beings`
- `Dr Shiba Ryu` (already deleted per git status)
- `Firas Bacchus`
- `Geneva Windrow`
- `Harriet Bourn`
- `Leah Turner`
- `Ruth Carter`
- `Tess Whitford`
- `The Intermediary`
- `Victor Hernandez`

**Rationale:** These have no extension and appear to be remnants of a directory-based system. Current `.md` files supersede them.

---

### 2.2 Consolidate Session/Handoff Files

**Current state:** 16+ SESSION files scattered across `story_bibles/book 2/`

**Action:**
1. Keep `story_bibles/book 2/HANDOFF.md` as the SINGLE handoff document (update in place)
2. Move dated SESSION files to `story_bibles/book 2/_session_archive/`
3. Delete root-level `handoff.md` (redundant, only 2KB)
4. Keep `HANDOFF_Prime_Timeline_Campaigns.md` at root (it's a specific project handoff)

**New convention:**
- One HANDOFF.md per book, updated in place
- Daily session notes go to `_session_archive/` if you want to keep them
- Root HANDOFF.md is for cross-book/project handoffs only

---

### 2.3 Clarify Character File Hierarchy

**Create:** `/workspaces/gosquad/character_profiles/README.md`

```markdown
# Character Profiles - File Hierarchy

## Naming Convention

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| `Character_Name.md` | Current working profile | Active development, Book 2+ |
| `Character_Name_Book1_Final.md` | Locked Book 1 snapshot | Reference only, DO NOT EDIT |
| `Character_Name_CORRECTED.md` | Canon fix for hallucinations | Supersedes base profile on specific points |

## Which File to Load?

**For Book 2 drafting:**
1. Load `Character_Name.md` (current state)
2. Cross-reference `Character_Name_Book1_Final.md` for backstory consistency
3. Check `character_arcs/Character_Name_Arc_Tracker.md` for progression

**For continuity checking:**
1. Load `character_arcs/CHARACTER_STATE_INDEX.yaml`
2. Check knowledge gates for current chapter

## Files in This Directory
[Auto-generated list would go here]
```

---

### 2.4 Move Book Exports

**Action:**
- Move `book1_manuscript.txt` → `Series Books/book1/book1_manuscript.txt`
- Move `Book1_Chapter24_FIXED.txt` → `Series Books/book1/Book1_Chapter24_FIXED.txt`
- Archive `go-squad-2025-12-07T17_10_50.txt` → `_archive/exports/`

---

### 2.5 Archive Old Synopsis

**Action:**
- Keep `SERIES_SYNOPSIS_v3.md` as primary (rename to `SERIES_SYNOPSIS.md`)
- Move old `SERIES_SYNOPSIS.md` → `_archive/SERIES_SYNOPSIS_v2.md`

---

## Phase 3: Establish Exemplar System

### 3.1 Designate Voice Exemplars

**Add to manifest schema or knowledge loader:**

```yaml
exemplars:
  voice:
    - book1_manuscript.txt:chapter_01  # Ahdia's voice established
    - book1_manuscript.txt:chapter_22  # Best action scene
    - book1_manuscript.txt:chapter_27  # Team dynamics

  action:
    - fight_Guide.md  # Combat principles

  structure:
    - story_bibles/book 2/Chapter_1_STRUCTURE.md  # Beat sheet format
```

**Purpose:** When drafting, these chapters can be loaded as style reference (like RESONANCE loads CH1 automatically).

---

### 3.2 Update Knowledge Loader

**Modify** `gosquad_knowledge_loader.py` to support:

```bash
# Load with voice exemplar
python3 gosquad_knowledge_loader.py --essential --exemplar chapter_01

# Load specific chapter context
python3 gosquad_knowledge_loader.py --chapter 5 --with-constraints
```

---

## Phase 4: New Directory Structure

### 4.1 Create Archive Directory

```
/workspaces/gosquad/_archive/
├── legacy_profiles/     # Old extension-less character files
├── session_logs/        # Dated SESSION_REFLECTION files
├── exports/             # Timestamped exports
└── superseded/          # Old versions of active docs
```

---

### 4.2 Final Structure (After Cleanup)

```
/workspaces/gosquad/
├── README.md                          # Series overview
├── HANDOFF.md                         # Cross-project handoff (renamed from handoff.md)
├── HANDOFF_Prime_Timeline_Campaigns.md # Specific campaign handoff
│
├── CLAUDE_PROTOCOL.md                 # NEW: LLM collaboration guide
├── GOSQUAD_PROSE_VOICE.md             # NEW: Syntactic signatures
├── GO_SQUAD_WRITING_STYLE_GUIDE.md    # Existing: Metrics-based style
├── fight_Guide.md                     # Combat/action guide
├── Montage_Style_Guide.md             # Parallel scenes guide
│
├── SERIES_SYNOPSIS.md                 # Renamed from v3
├── SERIES_TOUCHPOINTS.md              # Keep
├── SYSTEM_WORKFLOW.md                 # Keep (RESONANCE-style workflow)
│
├── book2_manuscript/                  # Prose chapters
│   ├── chapter_01.md ... chapter_10.md
│   └── BOOK2_MANUSCRIPT_COMPILED.txt
│
├── character_arcs/
│   ├── README.md                      # NEW: Explains arc tracker system
│   ├── CHARACTER_STATE_INDEX.yaml
│   └── *_Arc_Tracker.md
│
├── character_profiles/
│   ├── README.md                      # NEW: Explains file hierarchy
│   ├── *.md                           # Current profiles
│   └── *_Book1_Final.md               # Locked snapshots
│
├── context/
│   ├── CONTEXT_ENGINEERING_FOR_FICTION.md
│   ├── THEMATIC_CONSTRAINTS.md        # NEW: Thesis protection
│   ├── negative_constraints.md        # Existing: Factual protection
│   ├── manifest_schema.md
│   └── evaluator_spec.md
│
├── entity_catalog/
│   ├── ENTITY_CATALOG.yaml
│   └── manifests/
│       └── ch*_session_manifest.yaml
│
├── story_bibles/
│   ├── BOOK1_FINAL_STATE.md
│   ├── SERIES_MECHANICS.md
│   ├── CALLBACK_TRACKER.md            # NEW: Seeds/payoffs
│   ├── book 2/
│   │   ├── HANDOFF.md                 # Single handoff for Book 2
│   │   ├── Chapter_*_STRUCTURE.md
│   │   ├── Chapter_*_METHOD_ACTOR.md
│   │   └── _session_archive/          # Dated session files
│   ├── book 3/
│   ├── book 4/
│   ├── artifacts/
│   ├── locations/
│   ├── organizations/
│   ├── powers and cost/
│   ├── timeline/
│   └── universe/
│
├── editor_suite/                      # Keep as-is (well organized)
├── exports/                           # Keep as-is
├── themes/                            # Keep as-is
├── TTRPG/                             # Keep as-is
│
├── Series Books/
│   └── book1/
│       ├── book1_manuscript.txt       # Moved from root
│       └── Book1_Chapter24_FIXED.txt  # Moved from root
│
├── _archive/                          # NEW: Archive directory
│   ├── legacy_profiles/
│   ├── session_logs/
│   ├── exports/
│   └── superseded/
│
└── [Python scripts, JSON files, etc.]
```

---

## Phase 5: Update Entry Points

### 5.1 Update /gosquad Command

**Modify** `.claude/commands/gosquad.md` to include:

```markdown
## Pre-Reading (Automatic)
1. GOSQUAD_PROSE_VOICE.md
2. fight_Guide.md (if action chapter)
3. context/THEMATIC_CONSTRAINTS.md
4. Current chapter's METHOD_ACTOR briefing

## Quick Context
- HANDOFF.md (what's current)
- CALLBACK_TRACKER.md (active seeds)
```

---

### 5.2 Create Bundle Generator (Optional)

**New script:** `generate_bundle.py`

```python
# Usage:
# python3 generate_bundle.py --book 2 --chapters 5-10 --characters ahdia,ruth,ryu

# Generates: gosquad_bundle_b2_ch5-10.json
# Contains: All relevant files for that drafting session, portable
```

**Purpose:** For sessions where you need a portable context (like RESONANCE's bundle).

---

## Execution Checklist (COMPLETED)

### Before Starting
- [x] Commit current state: `git add -A && git commit -m "Pre-restructure snapshot"`

### Phase 1: Create New Documents
- [x] Create `GOSQUAD_PROSE_VOICE.md` (references Ahdia_voice_sample.md)
- [x] Create `context/THEMATIC_CONSTRAINTS.md`
- [x] Create `CLAUDE_PROTOCOL.md`
- [x] Create `story_bibles/CALLBACK_TRACKER.md`

### Phase 2: Cleanup
- [x] Create `_archive/` directory structure
- [x] Rename orphaned character files to `*_EXTENDED.md` (contain unique content, kept accessible)
- [x] Move dated SESSION files to `story_bibles/book 2/_session_archive/`
- [x] Delete root `handoff.md` (kept `HANDOFF_Prime_Timeline_Campaigns.md`)
- [x] Move book exports to `Series Books/book1/`
- [x] Rename `SERIES_SYNOPSIS_v3.md` → `SERIES_SYNOPSIS.md`, archive old
- [x] Move RESONANCE project files to `RESONANCE_PROJECT/`

### Phase 3: Documentation
- [x] Create `character_profiles/README.md`
- [x] Update `character_arcs/README.md` (added usage guide section)

### Phase 4: Commit
- [x] Final commit with all changes

---

## Changes from Original Plan

1. **Extension-less character files**: Renamed to `*_EXTENDED.md` instead of archiving (they contain unique content not in base files)
2. **RESONANCE files**: Moved to `RESONANCE_PROJECT/` folder (separate project, not archived)
3. **Knowledge loader update**: Deferred (current system works)
4. **Bundle generator**: Deferred (not needed yet)

---

## Not Doing (Explicitly Deferred)

1. **Automated Evaluator** - Keep human review for now (like RESONANCE)
2. **Bundle generator script** - Only if portability becomes needed
3. **Entity Catalog overhaul** - Current YAML structure is working
4. **TTRPG system changes** - Working well, don't touch
5. **Knowledge loader update** - Current `/gosquad` command works
6. **Merge EXTENDED files into base files** - Future task, do per-character as needed

---

## Follow-Up Tasks

1. **Merge EXTENDED file content** - Each `*_EXTENDED.md` file has rich content that should be merged into the corresponding base `.md` file
2. **Update /gosquad command** - Add new files to pre-reading list
3. **Populate CALLBACK_TRACKER.md** - Extract seeds/payoffs from beat sheets

---

## Success Criteria (MET)

1. ✅ **Voice is explicit** - GOSQUAD_PROSE_VOICE.md captures syntactic signatures
2. ✅ **Theme is protected** - THEMATIC_CONSTRAINTS.md prevents drift
3. ✅ **Callbacks are tracked** - CALLBACK_TRACKER.md created (needs population)
4. ✅ **File hierarchy is clear** - READMEs explain naming conventions
5. ✅ **Collaboration is documented** - CLAUDE_PROTOCOL.md sets expectations
6. ✅ **No orphaned files** - All files have proper extensions and homes
