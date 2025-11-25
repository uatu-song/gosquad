# Quality Evaluation Tools

**When to use:** Post-draft, when seeking external validation or preparing for submission

**Purpose:** Evaluate against conventional literary standards. USE WITH CAUTION - these tools judge against "rules" that may not apply to your voice.

## ⚠️ WARNING ⚠️

**These tools use CONVENTIONAL literary rules that may not match your intentional style choices.**

They will flag things like:
- Passive voice (which might be your character's detached voice)
- Adverb usage (which might be intentional)
- "Clichés" (which might be your character quoting pop culture)
- Dialogue patterns (which might be your character's awkwardness)

**Use these tools to see how your work measures against conventions, NOT as a list of things to fix.**

## Tools

### book_writing_style_analysis.py
**Purpose:** Analyze style against conventional writing advice
- Active vs passive voice ratio
- Adverb and adjective density
- Cliché detection
- Dialogue vs narrative ratio
- Sentence variety
- Pacing analysis

**Usage:**
```bash
python3 book_writing_style_analysis.py /path/to/manuscript.txt
```

**Output:**
- Voice analysis (active/passive percentages)
- Word choice metrics
- Cliché report (may flag intentional pop culture refs!)
- Sentence structure variety
- Style visualizations

### book_character_analysis.py
**Purpose:** Character presence and dialogue analysis
- Character detection across chapters
- Dialogue attribution patterns
- Character interaction networks
- Speaking patterns

**Usage:**
```bash
python3 book_character_analysis.py /path/to/manuscript.txt
```

### evaluate_book.py
**Purpose:** External quality assessment using AI judge (PKD Award criteria)
- Reads continuous sections from beginning/middle/end
- Evaluates against literary award standards
- Provides "would this win an award" perspective

**Usage:**
```bash
python3 evaluate_book.py /path/to/manuscript.pdf --title "Title" --author "Author" --api-key YOUR_KEY
```

**Requires:** Anthropic API key, PDF input

### evaluate_book_sequential.py
Alternative version of evaluate_book.py

## When to Use These

**For external perspective:**
- Preparing for agent/publisher submission
- Want to know how conventional readers might react
- Curious about award criteria alignment

**Do NOT use these:**
- As a checklist of "fixes"
- To change your voice to match conventions
- To eliminate intentional style choices

## Philosophy

Quality evaluation shows how you measure against **external standards**, not whether your book is good.

A book can have 30% passive voice and be brilliant. A book can follow all the rules and be boring.

**Trust your voice first. Use these tools second.**
