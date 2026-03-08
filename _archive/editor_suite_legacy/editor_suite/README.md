# GoSquad Editor Suite

Organized tools for different stages of manuscript editing.

## 📁 Directory Structure

```
editor_suite/
├── line_editing/          ← **YOU ARE HERE** (Book 1 polish phase)
│   └── Tools for catching duplicates, typos, continuity errors
│
├── structural_analysis/   ← Early drafting stage
│   └── Understanding chapter structure, pacing, architecture
│
├── quality_evaluation/    ⚠️ USE WITH CAUTION
│   └── Conventional literary standards (may not match your voice)
│
├── diagnostics/           ← Meta-tools
│   └── Batch processing, testing, orchestration
│
├── deprecated/            ← Archive
│   └── Old versions kept for reference
│
└── knowledge_system/      ← Not editing tools
    └── Load series context for AI assistants
```

## Quick Start

### Current Need: Book 1 Line Editing

**Interactive Chapter-by-Chapter Correction (RECOMMENDED):**

```bash
cd line_editing
python3 chapter_corrector.py /path/to/manuscript.txt --chapter 5
```

This extracts Chapter 5, shows you each issue for approval, and exports a corrected .txt file ready to paste into Dabble Writer.

**Or use the `/lineedit` slash command** for quick access.

### What Gets Fixed:
- ✅ Duplicate sentences (drafting artifacts)
- ✅ Typos and technical errors
- ✅ Double words ("the the")
- ✅ Spacing issues
- ⚠️ Repetitive phrases (flagged for review)

**Every change requires your approval** - you decide what stays and what goes.

**Start here:** `line_editing/`

### What You DON'T Need

**Avoid:** `quality_evaluation/` - These tools judge against conventional rules:
- "Too much passive voice" (but that's Ahdia's detached voice!)
- "Don't use adverbs" (but that's intentional!)
- "Avoid clichés" (but pop culture refs are her frame of reference!)

These tools are calibrated for MFA workshops, not for your actual voice.

## Philosophy

### Line Editing (Technical)
**Goal:** Catch mistakes while preserving voice
- ✅ "This sentence appears twice on pages 45 and 127"
- ❌ "This sentence is too passive"

### Structural Analysis (Descriptive)
**Goal:** Show patterns, not prescribe fixes
- ✅ "Chapter 12 is 2x longer than others"
- ❌ "Chapter 12 should be shorter"

### Quality Evaluation (External Perspective)
**Goal:** See how conventions view your work
- ✅ "Conventional readers might note X"
- ❌ "You must fix X to be good"

## Usage by Stage

### Stage 1: Drafting (structural_analysis/)
- Understanding your own patterns
- Seeing chapter lengths, pacing rhythms
- Descriptive, not prescriptive

### Stage 2: Revision (Not yet built)
- Consistency checking
- Character voice drift detection
- Tracking your own rules

### Stage 3: Line Editing ← **YOU ARE HERE**
- Duplicate sentence removal
- Typo catching
- Continuity error spotting
- Technical polish

### Stage 4: External Validation (quality_evaluation/)
- See how conventions judge your work
- Prepare for submission
- Understand agent/publisher perspective
- **NOT** a list of things to fix

## Creating New Tools

When building new editing tools, ask:
1. **Is this catching errors or judging style?** (Errors = good, judgment = caution)
2. **Am I checking consistency or convention?** (Consistency = useful)
3. **Does this preserve author voice?** (Should be yes)

## Current Status

**Line editing tools (COMPLETE ✅):**
- [x] **Interactive chapter corrector** - Fix one chapter at a time with approval workflow
- [x] Duplicate sentence finder
- [x] Continuity checker (character details, numbers, facts)
- [x] Proximity repetition detector
- [x] Typo scanner
- [x] Master line editor (runs all tools)

**Ready for Book 1 line editing!** Use `chapter_corrector.py` for chapter-by-chapter workflow.

## Documentation

Each directory has its own README explaining:
- When to use those tools
- What each tool does
- Philosophy and warnings

Read the README before using tools from a new directory.
