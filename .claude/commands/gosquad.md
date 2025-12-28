Load and absorb all Go Squad knowledge base to get fully caught up on the book series.

## Pre-Reading (Load These First)

Before running the knowledge loader, read these critical documents:

1. **CLAUDE_PROTOCOL.md** - How to collaborate (execute, don't confirm)
2. **GOSQUAD_PROSE_VOICE.md** - Syntactic signatures and voice patterns
3. **context/THEMATIC_CONSTRAINTS.md** - What NOT to write thematically
4. **story_bibles/CALLBACK_TRACKER.md** - Active seeds/payoffs

For Ahdia POV work, also load: **Ahdia_voice_sample.md**

## Knowledge Loader

Run the knowledge loader script to generate comprehensive context:

```bash
python3 gosquad_knowledge_loader.py --essential
```

Then read the output and confirm you're ready to work with Go Squad material. Summarize:
- Series structure (8 books, CBT→DBT journey)
- Current status (Book 1 complete, Book 2 prose in progress)
- Core thesis ("You don't have to be fixed to be worthy")
- Key characters and their arcs
- Major plot points and continuity notes
- TTRPG methodology (beats → prose pipeline)

## Available Options

- `--summary` - File counts and categories only
- `--essential` - Quick catch-up context (recommended)
- `--detailed` - Full content with previews
- `--search "query"` - Search across all files
- `--category characters` - Load specific category
- `--export output.json` - Export as JSON

## Key Files Reference

| Purpose | File |
|---------|------|
| Collaboration style | `CLAUDE_PROTOCOL.md` |
| Voice patterns | `GOSQUAD_PROSE_VOICE.md` |
| Ahdia's voice | `Ahdia_voice_sample.md` |
| Theme protection | `context/THEMATIC_CONSTRAINTS.md` |
| Factual constraints | `context/negative_constraints.md` |
| Character states | `character_arcs/CHARACTER_STATE_INDEX.yaml` |
| Callbacks | `story_bibles/CALLBACK_TRACKER.md` |
| Book 2 handoff | `story_bibles/book 2/HANDOFF.md` |
