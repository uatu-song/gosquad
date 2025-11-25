Interactive line editing for GoSquad Book 1 manuscripts.

# Line Editing Tools Available

## Interactive Chapter Corrector (RECOMMENDED)
Fix one chapter at a time with approval on each change:

```bash
cd /workspaces/gosquad/editor_suite/line_editing
python3 chapter_corrector.py /workspaces/gosquad/book1_manuscript.txt --chapter [NUMBER]
```

**What it does:**
- Extracts specified chapter
- Finds all issues (typos, double words, repetitions, spacing)
- Shows you EACH issue with context
- You approve/reject each fix (y/n/s/q)
- Exports `chapter_X_corrected.txt` ready for Dabble Writer

**Workflow:**
1. Run corrector on a chapter
2. Review each issue interactively
3. Get corrected .txt file
4. Paste into Dabble Writer
5. Move to next chapter

## Full Manuscript Scan
Get overview of all issues across entire manuscript:

```bash
cd /workspaces/gosquad/editor_suite/line_editing
python3 line_editor.py /workspaces/gosquad/book1_manuscript.txt
```

Opens dashboard with all reports.

## Individual Tools
Run specific analysis:

```bash
cd /workspaces/gosquad/editor_suite/line_editing

# Find duplicate sentences
python3 duplicate_sentence_finder.py /workspaces/gosquad/book1_manuscript.txt

# Check continuity
python3 continuity_checker.py /workspaces/gosquad/book1_manuscript.txt

# Find repeated phrases
python3 proximity_repetition_detector.py /workspaces/gosquad/book1_manuscript.txt

# Scan for typos
python3 typo_scanner.py /workspaces/gosquad/book1_manuscript.txt
```

# Philosophy

**Line editing = technical correctness, NOT style changes**

These tools:
✅ Find double words, typos, spacing errors
✅ Flag potential continuity issues
✅ Detect repeated phrases for your review
✅ Preserve your unique voice

These tools DON'T:
❌ Judge your writing style
❌ Tell you to "use less passive voice"
❌ Criticize pop culture references
❌ Change intentional style choices

# Output Location

All reports save to: `/workspaces/gosquad/editor_suite/line_editing/line_editing_output/`

Corrected chapters: `chapter_X_corrected.txt` (ready for Dabble Writer)
Review notes: `chapter_X_review_notes.txt` (flagged items)
