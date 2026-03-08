# GoSquad Book 1 - Line Editing Quick Reference

## 🎯 Recommended Workflow: Chapter-by-Chapter

Edit one chapter at a time, review each fix, export for Dabble Writer:

```bash
cd editor_suite/line_editing

# Edit Chapter 1
python3 chapter_corrector.py /workspaces/gosquad/book1_manuscript.txt --chapter 1

# Edit Chapter 2
python3 chapter_corrector.py /workspaces/gosquad/book1_manuscript.txt --chapter 2

# ... repeat for all chapters
```

**Or use the slash command:**
```
/lineedit
```

## What Happens

1. **Extracts Chapter** - Shows word count, stats
2. **Finds Issues** - Typos, double words, repetitions, spacing
3. **Interactive Review** - You approve/reject each fix:
   - `y` = Yes, apply fix
   - `n` = No, keep original
   - `s` = Skip, flag for later
   - `q` = Quit review

4. **Exports** - `chapter_X_corrected.txt` ready for Dabble Writer

## Example Session

```bash
$ python3 chapter_corrector.py manuscript.txt --chapter 5

✓ Chapter 5 extracted
  • 2,403 words
  • 18 lines

Found 12 issues:
  • 2 double words
  • 1 common typo
  • 4 proximity repetitions
  • 5 continuity notes

═══════════════════════════════════════════
Issue #1: Double word "the the"
───────────────────────────────────────────
Context:
"She walked through the the door"

Suggested fix:
"She walked through the door"
───────────────────────────────────────────
Apply this fix? [y/n/s/q]: y
✓ Fix will be applied

[... continues for each issue ...]

✅ Chapter corrected!
💾 Exported: chapter_5_corrected.txt
```

## Paste into Dabble Writer

1. Open corrected chapter file: `line_editing_output/chapter_5_corrected.txt`
2. Copy all text
3. Open Dabble Writer → Chapter 5
4. Select All → Paste
5. Save
6. Done!

## Alternative: Full Manuscript Scan

Get overview of all issues across entire book:

```bash
python3 line_editor.py /workspaces/gosquad/book1_manuscript.txt
```

Opens dashboard at: `line_editing_output/line_editing_dashboard.html`

Good for initial assessment, but chapter-by-chapter is better for actual corrections.

## What Gets Found

### Auto-Fix Candidates (High Priority)
- ✅ Double words: "the the building"
- ✅ Common typos: "teh" → "the", "recieve" → "receive"
- ✅ Spacing errors: "word.Another" → "word. Another"
- ✅ Multiple spaces

### Review Items (Judgment Calls)
- ⚠️ Repeated phrases within 500 characters
- ⚠️ Distinctive words used twice in close proximity
- ⚠️ Similar sentence openings

### Informational (Flagged, Not Fixed)
- ℹ️ Continuity notes (character details mentioned differently)
- ℹ️ Timeline observations

## Philosophy

**Line editing = catching mistakes, NOT changing your voice**

These tools:
- ✅ Find technical errors
- ✅ Preserve your style
- ✅ Require YOUR approval for every change

These tools DON'T:
- ❌ Judge writing style
- ❌ "Fix" intentional choices
- ❌ Change voice to match conventions

## Output Location

All files save to: `editor_suite/line_editing/line_editing_output/`

- `chapter_X_corrected.txt` - Ready for Dabble Writer
- `chapter_X_review_notes.txt` - Items you flagged for later
- Various HTML/JSON reports from full scans

## Individual Tools (Advanced)

Run specific analyses:

```bash
cd editor_suite/line_editing

# Just find duplicates
python3 duplicate_sentence_finder.py manuscript.txt

# Just check continuity
python3 continuity_checker.py manuscript.txt

# Just find repetitions
python3 proximity_repetition_detector.py manuscript.txt

# Just scan for typos
python3 typo_scanner.py manuscript.txt
```

Good for deep dives on specific issues.

## Manuscript Locations

- **Source manuscript (PDF):** `/workspaces/gosquad/Go Squad.pdf`
- **Extracted text:** `/workspaces/gosquad/book1_manuscript.txt`
- **Corrected chapters:** `editor_suite/line_editing/line_editing_output/chapter_X_corrected.txt`

## Need Help?

- **Line editing tools README:** `editor_suite/line_editing/README.md`
- **Full suite README:** `editor_suite/README.md`
- **Use `/lineedit` slash command** for quick reference

---

**Status: Book 1 (31 chapters) ready for line editing**

Start with Chapter 1, work through sequentially, paste corrected chapters into Dabble Writer.
