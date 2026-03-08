#!/usr/bin/env python3
"""
validate_chunk.py - Validate prose chunks against canon and style requirements

Usage:
    python validate_chunk.py 01                    # Validate latest chunk of Chapter 1
    python validate_chunk.py 01 --lines 850-920    # Validate specific line range
    python validate_chunk.py 01 --full             # Validate entire chapter
    python validate_chunk.py 01 --python-only      # Skip LLM, structural checks only

Input:
    - book2_manuscript/chapter_XX.md (chapter prose)
    - editor_suite/packets/chapter_XX_packet.md (compressed beats)
    - character_arcs/CHARACTER_STATE_INDEX.yaml (structured canon)

Output:
    - Validation report to terminal
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed.")
    print("Run: pip install anthropic")
    sys.exit(1)


# =============================================================================
# CONFIGURATION
# =============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent
MANUSCRIPT = REPO_ROOT / "book2_manuscript"
PACKETS_DIR = Path(__file__).parent.parent / "packets"
CHARACTER_ARCS = REPO_ROOT / "character_arcs"

# LLM Configuration
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 2048

# Validation thresholds
MIN_CHUNK_WORDS = 100
MAX_CHUNK_WORDS = 1500
HUMOR_TARGET_PER_500 = (1, 3)  # min, max per 500 words


# =============================================================================
# FILE LOADING
# =============================================================================

def load_chapter_prose(chapter_num: int) -> Optional[str]:
    """Load the chapter manuscript."""
    patterns = [
        f"chapter_{chapter_num:02d}.md",
        f"chapter_{chapter_num}.md",
        f"Chapter_{chapter_num}.md",
    ]

    for pattern in patterns:
        path = MANUSCRIPT / pattern
        if path.exists():
            return path.read_text()

    print(f"ERROR: Could not find manuscript for Chapter {chapter_num}")
    available = sorted(MANUSCRIPT.glob("chapter_*.md"))
    if available:
        print(f"Available: {[f.name for f in available]}")
    return None


def load_chapter_packet(chapter_num: int) -> Optional[str]:
    """Load the compressed chapter packet."""
    path = PACKETS_DIR / f"chapter_{chapter_num:02d}_packet.md"
    if path.exists():
        return path.read_text()

    print(f"WARNING: No packet found for Chapter {chapter_num}")
    print(f"Run: python compress_chapter.py {chapter_num}")
    return None


def load_character_state_index() -> dict:
    """Load structured canon from YAML."""
    path = CHARACTER_ARCS / "CHARACTER_STATE_INDEX.yaml"
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f)
    return {}


def extract_chunk(prose: str, line_range: Optional[str] = None) -> tuple[str, int, int]:
    """Extract a chunk from the prose, return (chunk, start_line, end_line)."""
    lines = prose.split("\n")

    if line_range:
        # Parse "850-920" format
        match = re.match(r"(\d+)-(\d+)", line_range)
        if match:
            start = int(match.group(1)) - 1  # Convert to 0-indexed
            end = int(match.group(2))
            chunk_lines = lines[start:end]
            return "\n".join(chunk_lines), start + 1, end

    # Default: find the last scene/beat section
    # Look for ### Beat or ## Scene markers
    last_section_start = 0
    for i, line in enumerate(lines):
        if line.startswith("### Beat") or line.startswith("## Scene"):
            last_section_start = i

    # Get from last section to end
    chunk_lines = lines[last_section_start:]
    return "\n".join(chunk_lines), last_section_start + 1, len(lines)


# =============================================================================
# PYTHON VALIDATION (PASS 1 - FAST)
# =============================================================================

class ValidationResult:
    def __init__(self):
        self.passed = True
        self.structural_issues = []
        self.warnings = []
        self.info = []

    def fail(self, issue: str):
        self.passed = False
        self.structural_issues.append(issue)

    def warn(self, warning: str):
        self.warnings.append(warning)

    def add_info(self, info: str):
        self.info.append(info)


def validate_structural(chunk: str, start_line: int) -> ValidationResult:
    """Fast Python-based structural validation."""
    result = ValidationResult()
    words = chunk.split()
    word_count = len(words)

    # Word count check
    result.add_info(f"Word count: {word_count}")
    if word_count < MIN_CHUNK_WORDS:
        result.warn(f"Chunk is short ({word_count} words, minimum {MIN_CHUNK_WORDS})")
    if word_count > MAX_CHUNK_WORDS:
        result.warn(f"Chunk is long ({word_count} words, consider splitting)")

    # Repetitive sentence starters
    lines = [l.strip() for l in chunk.split("\n") if l.strip() and not l.startswith("#")]
    sentence_starters = []
    for line in lines:
        # Get first word of sentences
        sentences = re.split(r'[.!?]\s+', line)
        for sent in sentences:
            if sent.strip():
                first_word = sent.strip().split()[0] if sent.strip().split() else ""
                sentence_starters.append(first_word.lower())

    # Check for 3+ consecutive same starters
    for i in range(len(sentence_starters) - 2):
        if (sentence_starters[i] == sentence_starters[i+1] == sentence_starters[i+2]
            and sentence_starters[i] in ['she', 'he', 'the', 'ahdia', 'ruth', 'ben']):
            result.warn(f"Repetitive sentence starter: '{sentence_starters[i]}' appears 3+ times consecutively")
            break

    # Check for scaffolding markers that should be removed
    scaffolding_patterns = [
        (r'\*\*Rolls?:\*\*', "Roll marker still present"),
        (r'### Beat \d+', "Beat header still present (scaffolding)"),
        (r'\[TODO\]', "TODO marker found"),
        (r'\[TBD\]', "TBD marker found"),
    ]

    for pattern, message in scaffolding_patterns:
        if re.search(pattern, chunk):
            result.warn(message)

    # Check for empty dialogue
    if '""' in chunk or "''" in chunk:
        result.warn("Empty dialogue found")

    # Check for generation artifacts
    # 1. Triple-adjective staccato patterns
    staccato_pattern = r'\.\s+[A-Z][a-z]+\.\s+[A-Z][a-z]+\.'
    staccato_matches = re.findall(staccato_pattern, chunk)
    if len(staccato_matches) > 2:
        result.warn(f"Triple-adjective staccato pattern appears {len(staccato_matches)} times (max 2 per scene)")

    # 2. Hedge phrases
    hedge_phrases = [
        r'something (?:that )?look(?:ed|s) like',
        r'something like',
        r'the kind of .+ that',
        r'the sort of .+ that',
    ]
    hedge_count = sum(len(re.findall(p, chunk, re.IGNORECASE)) for p in hedge_phrases)
    if hedge_count > 2:
        result.warn(f"Hedge phrases appear {hedge_count} times (commit or cut)")

    # 3. Over-explained brain activity
    brain_patterns = [
        r'her brain did that thing where',
        r'her brain .+ tried to',
        r'her brain .+ cycled through',
    ]
    for pattern in brain_patterns:
        if re.search(pattern, chunk, re.IGNORECASE):
            result.warn(f"Over-explained brain activity: '{pattern}' (just do the thing)")

    # Check for character name consistency
    name_variants = {
        'auerbach': 'Ahdia',  # Should be Ahdia in prose, Auerbach only in comms
        'nightingale': 'Ruth',
        'night knight': 'Ben',
        'crimson sable': 'Victor',
        'gloom girl': 'Tess',
        'battlea': 'Leah',
    }

    lower_chunk = chunk.lower()
    for codename, real_name in name_variants.items():
        # Codenames are fine in dialogue/comms, but narrator should use real names
        # This is a soft check - just info
        if codename in lower_chunk:
            result.add_info(f"Codename '{codename}' used (verify it's in dialogue/comms)")

    return result


def extract_must_hits_from_packet(packet: str) -> list[str]:
    """Extract must-hit items from the packet."""
    must_hits = []
    in_must_hits = False

    for line in packet.split("\n"):
        if "## MUST-HITS" in line or "## MUST HITS" in line:
            in_must_hits = True
            continue
        if in_must_hits:
            if line.startswith("##"):
                break
            if line.strip().startswith("-"):
                # Extract the beat description (before the →)
                beat = line.strip().lstrip("-").strip()
                if "→" in beat:
                    beat = beat.split("→")[0].strip()
                if beat:
                    must_hits.append(beat)

    return must_hits


def extract_prose_beats_from_packet(packet: str) -> list[str]:
    """Extract prose beats from the packet."""
    beats = []
    in_prose_beats = False

    for line in packet.split("\n"):
        if "## PROSE BEATS" in line:
            in_prose_beats = True
            continue
        if in_prose_beats:
            if line.startswith("## "):
                break
            # Match numbered beats like "1. " or "12. "
            match = re.match(r'\d+\.\s+(.+)', line.strip())
            if match:
                beats.append(match.group(1))

    return beats


# =============================================================================
# LLM VALIDATION (PASS 2 - SEMANTIC)
# =============================================================================

def build_validation_prompt(
    chunk: str,
    start_line: int,
    end_line: int,
    chapter_so_far: str,
    packet: str,
    canon_warnings: list[dict],
    must_hits: list[str],
) -> str:
    """Build the prompt for LLM validation."""

    # Truncate chapter_so_far to last 1000 words for context
    chapter_words = chapter_so_far.split()
    if len(chapter_words) > 1000:
        chapter_context = "...\n" + " ".join(chapter_words[-1000:])
    else:
        chapter_context = chapter_so_far

    warnings_text = "\n".join(
        f"- [{w.get('severity', 'info').upper()}] {w.get('warning', '')}"
        for w in canon_warnings
    ) if canon_warnings else "None"

    must_hits_text = "\n".join(f"- {h}" for h in must_hits) if must_hits else "None listed"

    prompt = f"""You are validating a prose chunk for canon compliance, continuity, and voice consistency.

## CANON WARNINGS (MUST NOT VIOLATE)
{warnings_text}

## MUST-HITS FOR THIS CHAPTER (check if any are addressed)
{must_hits_text}

## CHAPTER SO FAR (last 1000 words for context)
{chapter_context}

## NEW CHUNK TO VALIDATE (lines {start_line}-{end_line})
{chunk}

## VALIDATION TASKS

Check for these issues and report ONLY problems found:

### 1. CANON VIOLATIONS
- Does anything contradict the canon warnings above?
- Character knowledge errors (someone knows something they shouldn't yet)
- Timeline errors
- Spatial logic errors (character can't see/hear something from their location)

### 2. CONTINUITY ERRORS
- Does the chunk repeat an observation already made earlier in the chapter?
- Does a character react to something they already reacted to?
- Inconsistent descriptions (character in two places, weather changing randomly)

### 3. VOICE CHECK (Ahdia POV)
- Is there humor/wit present? (Target: 1-3 instances per 500 words)
- Are there TV/pop culture references? (At least one per major scene)
- Does prose get too formal/purple? (Should be casual, contemporary)
- Are there self-corrections or rambling when stressed?

### 4. MUST-HIT COVERAGE
- Which must-hits from the list does this chunk address?
- Which critical ones are still missing?

## OUTPUT FORMAT

```
## VALIDATION REPORT

### CANON: [PASS/FAIL]
[If FAIL, list specific issues with line references]

### CONTINUITY: [PASS/FAIL]
[If FAIL, list specific issues]

### VOICE: [PASS/FAIL]
- Humor instances: [count]
- Pop culture refs: [count]
[If FAIL, explain what's missing or wrong]

### MUST-HITS ADDRESSED
- [List any must-hits this chunk covers]

### MUST-HITS REMAINING
- [List critical ones still needed]

### ACTION ITEMS
[Numbered list of specific fixes needed, with line references where possible]
```

If everything passes, still provide the full report but with PASS for each section.
Be specific about line numbers when flagging issues.
Output ONLY the validation report, no preamble."""

    return prompt


def validate_with_llm(prompt: str, verbose: bool = False) -> str:
    """Call Claude for semantic validation."""
    client = anthropic.Anthropic()

    if verbose:
        print("\n" + "=" * 60)
        print("VALIDATION PROMPT (first 800 chars):")
        print(prompt[:800])
        print("..." if len(prompt) > 800 else "")
        print("=" * 60 + "\n")

    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = message.content[0].text

    if verbose:
        print("\n" + "=" * 60)
        print("LLM RESPONSE:")
        print(response)
        print("=" * 60 + "\n")

    return response


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def format_python_results(result: ValidationResult, start_line: int, end_line: int) -> str:
    """Format Python validation results for terminal."""
    output = []
    output.append(f"\n{'=' * 60}")
    output.append(f"STRUCTURAL VALIDATION (Lines {start_line}-{end_line})")
    output.append(f"{'=' * 60}")

    # Info
    for info in result.info:
        output.append(f"  ℹ {info}")

    # Warnings
    if result.warnings:
        output.append("")
        for warning in result.warnings:
            output.append(f"  ⚠ {warning}")

    # Failures
    if result.structural_issues:
        output.append("")
        for issue in result.structural_issues:
            output.append(f"  ✗ {issue}")

    # Summary
    output.append("")
    if result.passed and not result.warnings:
        output.append("  ✓ Structural checks passed")
    elif result.passed:
        output.append(f"  ⚠ Passed with {len(result.warnings)} warnings")
    else:
        output.append(f"  ✗ FAILED: {len(result.structural_issues)} issues")

    return "\n".join(output)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Validate prose chunks against canon and style requirements"
    )
    parser.add_argument(
        "chapter",
        type=int,
        help="Chapter number to validate (e.g., 1, 2, 12)"
    )
    parser.add_argument(
        "--lines",
        type=str,
        help="Line range to validate (e.g., 850-920)"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Validate entire chapter"
    )
    parser.add_argument(
        "--python-only",
        action="store_true",
        help="Skip LLM validation, structural checks only"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show LLM prompts and full responses"
    )

    args = parser.parse_args()
    chapter_num = args.chapter

    print(f"\n{'=' * 60}")
    print(f"VALIDATING CHAPTER {chapter_num}")
    print(f"{'=' * 60}")

    # Load prose
    print("\nLoading chapter prose...")
    prose = load_chapter_prose(chapter_num)
    if not prose:
        sys.exit(1)
    print(f"  → {len(prose.split())} words total")

    # Load packet
    print("Loading chapter packet...")
    packet = load_chapter_packet(chapter_num)
    if not packet:
        print("  → Proceeding without packet (limited validation)")
    else:
        print(f"  → Packet loaded")

    # Load canon
    print("Loading canon index...")
    state_index = load_character_state_index()
    canon_warnings = state_index.get("canon_warnings", [])
    print(f"  → {len(canon_warnings)} canon warnings")

    # Extract chunk
    if args.full:
        chunk = prose
        start_line, end_line = 1, len(prose.split("\n"))
    else:
        chunk, start_line, end_line = extract_chunk(prose, args.lines)

    print(f"\nValidating lines {start_line}-{end_line} ({len(chunk.split())} words)")

    # Pass 1: Python structural validation
    print("\n[Pass 1] Running structural checks...")
    struct_result = validate_structural(chunk, start_line)
    print(format_python_results(struct_result, start_line, end_line))

    # Pass 2: LLM semantic validation
    if not args.python_only:
        print(f"\n{'=' * 60}")
        print("[Pass 2] Running semantic validation (LLM)...")
        print(f"{'=' * 60}")

        # Get must-hits from packet
        must_hits = []
        if packet:
            must_hits = extract_must_hits_from_packet(packet)
            print(f"  → {len(must_hits)} must-hits to check")

        # Get chapter context (everything before the chunk)
        chunk_start_in_prose = prose.find(chunk[:100])  # Find chunk by first 100 chars
        if chunk_start_in_prose > 0:
            chapter_so_far = prose[:chunk_start_in_prose]
        else:
            chapter_so_far = ""

        # Build and run LLM validation
        prompt = build_validation_prompt(
            chunk=chunk,
            start_line=start_line,
            end_line=end_line,
            chapter_so_far=chapter_so_far,
            packet=packet or "",
            canon_warnings=canon_warnings,
            must_hits=must_hits,
        )

        print(f"  → Prompt: ~{len(prompt.split())} words")
        print("  → Calling Claude...")

        llm_result = validate_with_llm(prompt, verbose=args.verbose)

        print(f"\n{llm_result}")

    print(f"\n{'=' * 60}")
    print("VALIDATION COMPLETE")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
