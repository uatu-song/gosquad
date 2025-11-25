# GoSquad Book Series

A 7-book psychological science fiction series exploring trauma, healing, and what it means to be worthy while still struggling.

**Core Theme:** "You don't have to be fixed to be worthy"

## Current Status

- **Book 1:** Complete (71,500 words, 319 pages PDF) - **Currently in line editing phase**
- **Book 2:** TTRPG campaign complete (24 chapters, 5000+ beats) - Prose conversion pending
- **Books 3-7:** Planned

## Quick Links

### For Writing/Editing
- 📝 **[LINE EDITING GUIDE](LINE_EDITING_GUIDE.md)** - Start here for Book 1 line editing
- 📚 **[Editor Suite](editor_suite/)** - All editing tools
- 📖 **[Series Synopsis](SERIES_SYNOPSIS.md)** - Full series overview

### For Context
- 🎮 **[Knowledge System](KNOWLEDGE_SYSTEM_OVERVIEW.md)** - Load series context for AI
- 📋 **[Handoff Notes](handoff.md)** - Current project status
- 🔧 **[API Configuration](API_CONFIGURATION_GUIDE.md)** - Setup guides

## Current Task: Book 1 Line Editing

Book 1 is complete and ready for line editing. Use the **interactive chapter corrector**:

```bash
cd editor_suite/line_editing
python3 chapter_corrector.py book1_manuscript.txt --chapter 1
```

Or use the slash command:
```
/lineedit
```

### What This Does
1. Extracts a chapter
2. Finds all technical issues (typos, duplicates, spacing)
3. Shows you each issue for approval
4. Exports corrected `.txt` ready to paste into Dabble Writer

**Every fix requires your approval** - you decide what changes.

See **[LINE_EDITING_GUIDE.md](LINE_EDITING_GUIDE.md)** for complete workflow.

## Project Structure

```
gosquad/
├── Go Squad.pdf                    # Book 1 manuscript (source)
├── book1_manuscript.txt            # Extracted text for editing
├── LINE_EDITING_GUIDE.md          # ⭐ Start here for editing
│
├── editor_suite/                   # All editing tools
│   ├── line_editing/              # ⭐ Current focus
│   │   ├── chapter_corrector.py   # Interactive chapter editor
│   │   ├── line_editor.py         # Full manuscript scan
│   │   └── [other tools]
│   ├── structural_analysis/       # Chapter structure, pacing
│   ├── quality_evaluation/        # ⚠️ Conventional standards
│   └── diagnostics/               # Batch processing
│
├── story_bibles/                   # Story world details
├── character_profiles/             # Character bibles
├── TTRPG/                         # Book 2 campaign materials
│
└── .claude/                       # Claude Code configuration
    └── commands/
        ├── gosquad.md             # /gosquad - Load series context
        └── lineedit.md            # /lineedit - Line editing help
```

## Available Slash Commands

- `/gosquad` - Load complete series context (characters, plots, themes)
- `/lineedit` - Quick reference for line editing tools

## Series Overview

### The 7-Book Arc
A character-driven sci-fi series following Ahdia Bacchus and the Go Squad vigilantes through a psychological journey from Cognitive Behavioral Therapy (CBT) to Dialectical Behavioral Therapy (DBT) thinking.

**Book 1: Origins** - Ahdia, a depressed hermit with time powers, is forced out of isolation when her brother is critically injured. Establishes core themes and CBT thinking patterns.

**Books 2-7:** Planned progression exploring both/and thinking, radical acceptance, and finding worth while still struggling.

### Core Themes
- Worthiness without "being fixed"
- Both/and thinking (not binary good/bad)
- Living with mental illness authentically
- Powers that cost (cellular degradation)
- Found family and vigilante justice

### Key Characters
- **Ahdia Bacchus:** Temporalist with depression, TV-reference frame
- **Firas Bacchus:** Parkour expert, Ahdia's brother
- **Ruth (Nightingale):** Healer, emotional core
- **Plus 5 more squad members:** Each with powers and struggles

## Tools Philosophy

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

**Line editing preserves your unique voice.** Never auto-fixes style choices.

## Knowledge Base

**38 files indexed** across 9 categories:
- Series overview and themes
- Character profiles (20 characters)
- Story bibles (world, locations, powers)
- Plot timelines and continuity
- TTRPG campaign materials
- Editing tools documentation

Load with:
```bash
python3 gosquad_knowledge_loader.py --essential
```

Or use `/gosquad` slash command.

## Getting Started

### For Line Editing Book 1
1. Read **[LINE_EDITING_GUIDE.md](LINE_EDITING_GUIDE.md)**
2. Run `/lineedit` or check `editor_suite/line_editing/README.md`
3. Start with Chapter 1:
   ```bash
   cd editor_suite/line_editing
   python3 chapter_corrector.py ../book1_manuscript.txt --chapter 1
   ```
4. Review issues, approve fixes
5. Paste corrected chapter into Dabble Writer
6. Repeat for all 31 chapters

### For Series Context
1. Run `/gosquad` to load knowledge base
2. Read **[SERIES_SYNOPSIS.md](SERIES_SYNOPSIS.md)**
3. Check character profiles in `character_profiles/`

### For Book 2 Planning
1. Review TTRPG campaign in `TTRPG/`
2. Check beat sheets and plot structure
3. (Prose conversion pending Book 1 completion)

## Contributing

This is a personal project, but the editing tools are reusable:
- Line editing tools work on any manuscript
- Knowledge loader framework is extensible
- TTRPG → prose pipeline can be adapted

## License

Manuscript content: © J.S. Vaughn (All Rights Reserved)
Editing tools: Available for adaptation (see individual tool headers)

---

**Current Focus:** Book 1 line editing, chapter by chapter
**Next Step:** Book 2 prose conversion after Book 1 complete
