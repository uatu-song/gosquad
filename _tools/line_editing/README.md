# Line Editing Tools

**When to use:** Final polish phase, catching technical errors

**Purpose:** Find duplicate sentences, typos, continuity errors, and technical mistakes that survived the drafting process. These tools DO NOT judge your style choices.

## Quick Start

### Full Manuscript Scan
Run all line editing tools at once:
```bash
python3 line_editor.py /path/to/manuscript.txt
```
This generates a dashboard with all results.

### Interactive Chapter Correction (RECOMMENDED)
Fix one chapter at a time, reviewing each issue:
```bash
python3 chapter_corrector.py manuscript.txt --chapter 5
```
This extracts Chapter 5, shows you each issue, lets you approve/reject fixes, and exports a clean .txt file ready to paste into Dabble Writer.

## Tools

### ⭐ chapter_corrector.py (RECOMMENDED - Interactive Corrector)
**Purpose:** Extract a chapter, review issues interactively, export corrected version for Dabble Writer
- **Every fix requires your approval** - you decide what changes
- Shows context for each issue
- Exports clean .txt ready to paste into Dabble Writer
- Creates review notes for flagged items

**Usage:**
```bash
# Correct Chapter 5
python3 chapter_corrector.py manuscript.txt --chapter 5

# Interactive prompts for each issue:
# "Found double word 'the the'. Fix? [y/n/s/q]"
# y = apply fix
# n = keep original
# s = skip, flag for later
# q = quit review
```

**Finds:**
- Double words (the the)
- Common typos (teh → the)
- Spacing issues (missing space after period)
- Repeated phrases too close together

**Output:**
- `chapter_5_corrected.txt` → Ready to paste into Dabble Writer
- `chapter_5_review_notes.txt` → Items flagged for manual review

**Workflow:**
1. Run corrector on a chapter
2. Review each issue, approve/reject
3. Get corrected .txt file
4. Open Dabble Writer, select chapter
5. Select All → Paste corrected text
6. Done! Move to next chapter.

---

### 🎯 line_editor.py (Master Script - Full Scan)
**Purpose:** Run all line editing tools and generate master dashboard
- Orchestrates all tools
- Creates combined HTML dashboard
- Can run selective tools
- Good for initial overview of entire manuscript

**Usage:**
```bash
# Run all tools
python3 line_editor.py manuscript.txt

# Run specific tools only
python3 line_editor.py manuscript.txt --tools duplicates typos

# Custom output directory
python3 line_editor.py manuscript.txt --output my_results/
```

### 📝 duplicate_sentence_finder.py
**Purpose:** Find exact and near-duplicate sentences
- Catches drafting artifacts (same sentence in two places)
- Finds very similar sentences (>90% match)
- Shows context for each duplicate

**Usage:**
```bash
python3 duplicate_sentence_finder.py manuscript.txt
python3 duplicate_sentence_finder.py manuscript.txt --similarity 0.85
```

**Catches:**
- "The door opened slowly" appearing on pages 45 and 127
- Near-identical sentences with minor variations

### 🔍 continuity_checker.py
**Purpose:** Track character attributes and facts for contradictions
- Monitors physical descriptions (eye color, hair, height)
- Tracks ages and timeline consistency
- Flags potential contradictions

**Usage:**
```bash
python3 continuity_checker.py manuscript.txt
```

**Catches:**
- Character has blue eyes in Ch 2, brown eyes in Ch 10
- Character is 25 in Ch 1, 27 in Ch 5 (without time skip)
- Location described differently in different chapters

### 🔄 proximity_repetition_detector.py
**Purpose:** Find phrases repeated too close together
- Catches same multi-word phrase within 500 characters
- Finds distinctive words repeated in consecutive sentences
- Identifies repeated sentence openings

**Usage:**
```bash
python3 proximity_repetition_detector.py manuscript.txt
python3 proximity_repetition_detector.py manuscript.txt --threshold 1000
```

**Catches:**
- "She turned around" used 3 times in one paragraph
- Starting 5 consecutive sentences with "He thought"
- Distinctive words like "discombobulated" used twice in one page

### ✏️ typo_scanner.py
**Purpose:** Find common typos and mechanical errors
- Double words ("the the")
- Common misspellings ("teh" → "the")
- Spacing issues (missing/extra spaces)
- Punctuation problems

**Usage:**
```bash
python3 typo_scanner.py manuscript.txt
```

**Catches:**
- "the the building" (double word)
- "recieve" → should be "receive"
- "word.Another" (missing space after period)
- Multiple spaces between words

### 📊 chapter_analyzer.py (Legacy/Supplemental)
**Purpose:** Extract granular details from each chapter
- Extracts characters, locations, numbers, dialogue
- Creates per-chapter reports
- Useful for manual continuity checking

**Usage:**
```bash
python3 chapter_analyzer.py manuscript.txt --chapters 1 2 3
python3 chapter_analyzer.py manuscript.txt --mode consistency
```

---

### 📝 session_recap_generator.py (Documentation)
**Purpose:** Generate narrative recaps of editing sessions for blog posts, documentation, or process tracking
- Creates markdown/HTML/text recaps
- Tracks chapters edited and issues found/fixed
- Shows before/after examples
- Perfect for behind-the-scenes content

**Usage:**
```bash
# Generate recap for a chapter you just finished
python3 session_recap_generator.py --chapter 5 --issues 3 --fixed 2 --flagged 1 --format markdown

# Generate HTML version for blog post
python3 session_recap_generator.py --chapter 5 --issues 3 --fixed 2 --format html --output my_recap.html

# List all previous sessions
python3 session_recap_generator.py --list
```

**Output formats:**
- **Markdown:** For blog posts, documentation
- **HTML:** Beautiful styled pages for sharing
- **Text:** Plain text for simple records

**Great for:**
- Documenting your editing journey
- Creating "behind the scenes" blog posts
- Tracking progress over time
- Sharing the writing/editing process

## Philosophy

Line editing is about **mechanical correctness**, not style judgment.
- ✅ "This sentence appears twice on pages 45 and 127"
- ❌ "You use passive voice too much"

We preserve your voice while catching technical errors.
