# Structural Analysis Tools

**When to use:** Early drafting stage, understanding the shape of your book

**Purpose:** Understand chapter lengths, scene breaks, pacing patterns, and overall architecture. Descriptive, not prescriptive.

## Tools

### book_structural_analysis.py
**Purpose:** Analyze book structure and narrative patterns
- Chapter detection and lengths
- Scene break detection
- POV shift detection
- Plot arc intensity tracking
- Timeline/temporal reference analysis
- Hooks and cliffhangers identification

**Usage:**
```bash
python3 book_structural_analysis.py /path/to/manuscript.txt
```

**Output:**
- Chapter structure report
- Scene breakdown
- POV analysis
- Plot intensity charts
- Timeline complexity
- Structural visualizations (PNG charts)

### book_text_analysis.py
**Purpose:** Basic text metrics and readability
- Word frequency analysis
- Readability scores (Flesch-Kincaid, etc.)
- Sentence/paragraph statistics
- Chapter-level metrics
- Lexical diversity

**Usage:**
```bash
python3 book_text_analysis.py /path/to/manuscript.txt
```

**Output:**
- Word count statistics
- Readability scores
- Vocabulary analysis
- Chapter length comparisons
- Text metric visualizations

## When to Use These

**During drafting:**
- Check if chapter lengths wildly vary (unless intentional)
- See where intensity peaks and valleys are
- Understand your own pacing patterns

**These tools show patterns, not problems.** A "low readability score" isn't bad if you're writing literary fiction. Varied chapter lengths aren't wrong if they serve the story.

## Philosophy

Structural analysis is **descriptive** - showing you what you did, not telling you what to do.
