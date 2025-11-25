# Diagnostic & Batch Tools

**When to use:** Running multiple analyses, testing tools, batch processing

**Purpose:** Meta-tools that orchestrate other tools or test functionality

## Tools

### book_analysis_suite.py
**Purpose:** Master orchestrator - runs all analysis modules at once
- Coordinates text, character, style, and structural analysis
- Generates comprehensive HTML reports
- Runs all modules with single command

**Usage:**
```bash
python3 book_analysis_suite.py /path/to/manuscript.txt
python3 book_analysis_suite.py /path/to/manuscript.txt --modules text structure
python3 book_analysis_suite.py /path/to/manuscript.txt --quick
```

**Output:**
- Combined analysis report (HTML + JSON)
- All visualizations in one place
- Executive summary

### analyze_all_chapters.py
**Purpose:** Batch process all chapter files
- Runs analysis on every chapter file in a directory
- Creates index of all analyses
- Generates summary reports

**Usage:**
```bash
python3 analyze_all_chapters.py /path/to/chapters/directory
```

**Output:**
- Per-chapter analysis sessions
- HTML index of all chapters
- Success/failure summary

### analyzer_diagnostic.py
**Purpose:** Test that all analyzer tools are working
- Checks dependencies (matplotlib, numpy, etc.)
- Tests each analyzer with sample text
- Validates script functionality

**Usage:**
```bash
python3 analyzer_diagnostic.py
```

**Output:**
- Dependency status
- Script functionality tests
- Existing analysis results

## When to Use These

- **book_analysis_suite.py**: Want everything analyzed at once
- **analyze_all_chapters.py**: Processing multiple chapter files
- **analyzer_diagnostic.py**: Troubleshooting, checking if tools work

## Philosophy

These are **convenience wrappers** - they run other tools for you rather than doing new analysis.
