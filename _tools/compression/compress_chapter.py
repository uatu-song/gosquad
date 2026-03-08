#!/usr/bin/env python3
"""
compress_chapter.py - Compress beat sheets into prose-ready chapter packets

Usage:
    python compress_chapter.py 01              # Compress Chapter 1
    python compress_chapter.py 01 --dry-run    # Preview without writing
    python compress_chapter.py 01 --verbose    # Show LLM prompts/responses

Input:
    - story_bibles/book 2/Chapter_X_STRUCTURE.md (beat sheet)
    - character_arcs/*.md (relevant character trackers)
    - character_arcs/CHARACTER_STATE_INDEX.yaml (structured canon)
    - character_profiles/*.md (method actor briefs - personality, voice, traits)
    - story_bibles/book 2/CLAUDE.md (voice guide)
    - Ahdia_voice_sample.md (Book 1 prose for voice infection)
    - book2_manuscript/chapter_XX.md (previous chapter ending, if exists)

Output:
    - editor_suite/packets/chapter_XX_packet.md (~400 lines)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

# Add parent to path for potential shared utilities
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import anthropic, provide helpful error if missing
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
BOOK2_BIBLE = REPO_ROOT / "story_bibles" / "book 2"
CHARACTER_ARCS = REPO_ROOT / "character_arcs"
CHARACTER_PROFILES = REPO_ROOT / "character_profiles"
MANUSCRIPT = REPO_ROOT / "book2_manuscript"
PACKETS_DIR = Path(__file__).parent.parent / "packets"
VOICE_SAMPLE = REPO_ROOT / "Ahdia_voice_sample.md"

# Character name to profile filename mapping
# If profile doesn't exist, check character_arcs for arc tracker as fallback
CHARACTER_PROFILE_MAP = {
    "Ahdia": "Ahdia_Bacchus.md",
    "Ruth": "Ruth_Carter.md",
    "Ryu": "Shiba_Ryu.md",
    "Ben": "Ben_Harrison.md",  # May not exist yet
    "Tess": "Tess_Whitford.md",  # May not exist yet
    "Leah": "Leah_Turner.md",  # May not exist yet
    "Victor": "Victor_Okafor.md",  # May not exist yet
    "Leta": "Leta_Okafor.md",  # May not exist yet
    "Korede": "Korede_Okafor.md",  # May not exist yet
    "Bourn": "Harriet_Bourn.md",  # May not exist yet - use arc tracker
    "Diana": "Diana_Prime.md",  # May not exist yet
    "Kain": "Harding_Kain.md",
    "Jericho": "Rahs_Jericho.md",
    "Bellatrix": "Bellatrix_Naima.md",
}

# Fallback: if profile doesn't exist, try arc tracker
CHARACTER_ARC_FALLBACK = {
    "Bourn": "Harriet_Bourn_Arc_Tracker.md",
    "Ben": "Ben_Arc_Tracker.md",
    "Tess": "Tess_Arc_Tracker.md",
    "Leah": "Leah_Arc_Tracker.md",
    "Victor": "Victor_Arc_Tracker.md",
    "Leta": "Leta_Arc_Tracker.md",
    "Korede": "Korede_Arc_Tracker.md",
    "Diana": "Diana_Arc_Tracker.md",
}

# LLM Configuration
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096


# =============================================================================
# FILE LOADING
# =============================================================================

def load_beat_sheet(chapter_num: int) -> Optional[str]:
    """Load the beat sheet for a chapter."""
    # Try different naming patterns
    patterns = [
        f"Chapter_{chapter_num}_STRUCTURE.md",
        f"Chapter_{chapter_num:02d}_STRUCTURE.md",
        f"chapter_{chapter_num}_STRUCTURE.md",
    ]

    for pattern in patterns:
        path = BOOK2_BIBLE / pattern
        if path.exists():
            return path.read_text()

    # List available chapters
    available = sorted(BOOK2_BIBLE.glob("Chapter_*_STRUCTURE.md"))
    print(f"ERROR: Could not find beat sheet for Chapter {chapter_num}")
    print(f"Available: {[f.name for f in available[:5]]}...")
    return None


def load_claude_md() -> str:
    """Load voice guide from CLAUDE.md."""
    path = BOOK2_BIBLE / "CLAUDE.md"
    if path.exists():
        return path.read_text()
    return ""


def load_voice_sample() -> str:
    """Load Ahdia voice sample for voice infection."""
    if VOICE_SAMPLE.exists():
        return VOICE_SAMPLE.read_text()
    return ""


def load_character_state_index() -> dict:
    """Load structured canon from YAML."""
    path = CHARACTER_ARCS / "CHARACTER_STATE_INDEX.yaml"
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f)
    return {}


def load_character_trackers(characters: list[str]) -> dict[str, str]:
    """Load relevant character arc trackers."""
    trackers = {}
    for char in characters:
        # Try different naming patterns
        patterns = [
            f"{char}_Arc_Tracker.md",
            f"{char.replace(' ', '_')}_Arc_Tracker.md",
            f"{char.lower()}_Arc_Tracker.md",
        ]
        for pattern in patterns:
            path = CHARACTER_ARCS / pattern
            if path.exists():
                trackers[char] = path.read_text()
                break
    return trackers


def load_character_profiles(characters: list[str]) -> dict[str, str]:
    """Load full character profiles for method actor context.

    Falls back to arc trackers if profile doesn't exist.
    """
    profiles = {}
    for char in characters:
        # Try profile first
        filename = CHARACTER_PROFILE_MAP.get(char)
        if filename:
            path = CHARACTER_PROFILES / filename
            if path.exists():
                profiles[char] = path.read_text()
                continue

        # Fallback to arc tracker
        fallback = CHARACTER_ARC_FALLBACK.get(char)
        if fallback:
            path = CHARACTER_ARCS / fallback
            if path.exists():
                profiles[char] = path.read_text()

    return profiles


def extract_method_actor_brief(profile: str, char_name: str) -> str:
    """Extract condensed method actor info from a character profile.

    Pulls: personality, voice patterns, neurodivergent traits, key relationships.
    ~200-300 words per character.
    """
    lines = profile.split("\n")
    brief_sections = []

    # Sections we want to extract
    target_sections = [
        "Personality",
        "Core Traits",
        "Speech Patterns",
        "Voice Patterns",
        "Neurodivergent Traits",
        "Voice and Dialogue Patterns",
        "Voice Examples",
        "Writing Notes",
    ]

    current_section = None
    section_content = []

    for line in lines:
        # Check if this is a header
        if line.startswith("##") or line.startswith("###"):
            # Save previous section if it was a target
            if current_section and section_content:
                brief_sections.append(f"**{current_section}:**\n" + "\n".join(section_content[:15]))

            # Check if new section is a target
            header_text = line.lstrip("#").strip()
            current_section = None
            section_content = []

            for target in target_sections:
                if target.lower() in header_text.lower():
                    current_section = header_text
                    break
        elif current_section:
            if line.strip():
                section_content.append(line)

    # Don't forget last section
    if current_section and section_content:
        brief_sections.append(f"**{current_section}:**\n" + "\n".join(section_content[:15]))

    if not brief_sections:
        # Fallback: grab first 20 non-empty lines
        content_lines = [l for l in lines if l.strip() and not l.startswith("#")][:20]
        return f"### {char_name}\n" + "\n".join(content_lines)

    return f"### {char_name}\n" + "\n\n".join(brief_sections)


def load_previous_chapter_ending(chapter_num: int, words: int = 300) -> str:
    """Load the last N words of the previous chapter."""
    if chapter_num <= 1:
        return ""

    prev_chapter = chapter_num - 1
    patterns = [
        f"chapter_{prev_chapter:02d}.md",
        f"chapter_{prev_chapter}.md",
    ]

    for pattern in patterns:
        path = MANUSCRIPT / pattern
        if path.exists():
            content = path.read_text()
            # Get last N words
            all_words = content.split()
            if len(all_words) <= words:
                return content
            return " ".join(all_words[-words:])

    return ""


# =============================================================================
# PARSING
# =============================================================================

def extract_characters_from_beat_sheet(beat_sheet: str) -> list[str]:
    """Extract character names mentioned in the beat sheet."""
    # Look for Present: lines and character mentions
    characters = set()

    # All known characters to look for
    all_characters = [
        # Go Squad
        "Ahdia", "Ruth", "Ben", "Tess", "Leah", "Victor", "Leta", "Korede",
        # CADENS
        "Ryu", "Bourn", "Jericho",
        # Antagonists/Others
        "Kain", "Diana", "Bellatrix",
    ]

    for char in all_characters:
        if char.lower() in beat_sheet.lower():
            characters.add(char)

    # Also check Present: lines
    present_pattern = r"\*\*Present:\*\*\s*([^\n]+)"
    matches = re.findall(present_pattern, beat_sheet)
    for match in matches:
        for char in all_characters:
            if char.lower() in match.lower():
                characters.add(char)

    return list(characters)


def extract_voice_reminders(claude_md: str) -> list[str]:
    """Extract voice pattern bullets from CLAUDE.md."""
    reminders = []

    # Look for voice patterns section
    in_voice_section = False
    for line in claude_md.split("\n"):
        if "Voice Patterns" in line or "voice patterns" in line:
            in_voice_section = True
            continue
        if in_voice_section:
            if line.startswith("```"):
                in_voice_section = False
                continue
            if line.strip().startswith("✓"):
                reminders.append(line.strip())
            if len(reminders) >= 6:
                break

    # Fallback defaults if nothing found
    if not reminders:
        reminders = [
            "✓ Casual/contemporary language",
            "✓ Self-correction pattern: '[Statement]. Or rather, [correction]?'",
            "✓ TV/movie processing of real events",
            "✓ Deadpan acceptance of absurd situations",
            "✓ Specific details over generic descriptions",
        ]

    return reminders[:5]


def extract_canon_warnings(state_index: dict, chapter_num: int) -> list[str]:
    """Extract relevant canon warnings for this chapter."""
    warnings = []

    if "canon_warnings" in state_index:
        for warning in state_index["canon_warnings"]:
            warnings.append(f"[{warning.get('severity', 'info').upper()}] {warning.get('warning', '')}")

    return warnings


def extract_timeline_context(state_index: dict, chapter_num: int) -> str:
    """Get timeline context for this chapter."""
    if "timeline" not in state_index:
        return ""

    timeline = state_index["timeline"]
    chapter_key = f"ch{chapter_num}"

    if chapter_key in timeline:
        entry = timeline[chapter_key]
        return f"Month {entry.get('month', '?')}: {entry.get('event', 'unknown')}"

    return ""


# =============================================================================
# LLM COMPRESSION
# =============================================================================

def build_compression_prompt(
    beat_sheet: str,
    character_trackers: dict[str, str],
    timeline_context: str,
    canon_warnings: list[str],
) -> str:
    """Build the prompt for LLM compression."""

    # Truncate character trackers to relevant sections
    tracker_excerpts = []
    for char, content in character_trackers.items():
        # Try to find the Book 2 section
        lines = content.split("\n")
        book2_start = None
        for i, line in enumerate(lines):
            if "Book 2" in line or "## Book 2" in line:
                book2_start = i
                break

        if book2_start is not None:
            # Get ~50 lines from Book 2 section
            excerpt = "\n".join(lines[book2_start:book2_start + 50])
        else:
            # Get first 30 lines
            excerpt = "\n".join(lines[:30])

        tracker_excerpts.append(f"### {char}\n{excerpt}")

    trackers_text = "\n\n".join(tracker_excerpts)
    warnings_text = "\n".join(f"- {w}" for w in canon_warnings) if canon_warnings else "None"

    prompt = f"""You are compressing a detailed beat sheet into prose-ready beats for a novelist.

## CONTEXT
Timeline: {timeline_context}

## CANON WARNINGS (must respect)
{warnings_text}

## CHARACTER STATES (excerpt)
{trackers_text}

## BEAT SHEET TO COMPRESS
{beat_sheet}

## YOUR TASK

Compress this beat sheet from {len(beat_sheet.split())} words to ~800 words of prose-ready beats.

### OUTPUT FORMAT

```markdown
## PROSE BEATS

### Scene 1: [Title]
1. [Merged beat - 1-2 lines max]
2. [Merged beat]
...

### Scene 2: [Title]
...

## MUST-HITS
[List 10-15 beats that MUST be hit because they:]
- Pay off in later chapters (note which)
- Establish character knowledge that matters later
- Are arc milestones from character trackers
- Match canon warnings

Format: "- [Beat description] → [Why it matters]"

## CHARACTER KNOWLEDGE AT CHAPTER START
[For each POV character in this chapter:]

### [Character Name]
- Knows: [key facts they know at start]
- Doesn't know: [key facts hidden from them]
- Emotional state: [1 line]
- Baseline: [if Ahdia, her % baseline]
```

### COMPRESSION RULES

1. MERGE sequential actions by same character into single beats
2. MERGE dialogue exchanges into "[Characters] discuss [topic], achieving [outcome]"
3. FOLD description/atmosphere into action beats
4. PRESERVE: First and last beat of each scene
5. PRESERVE: Any beat mentioning future chapters or "pays off"
6. PRESERVE: Character knowledge changes ("learns", "discovers", "realizes")
7. FLAG as must-hit: Anything with downstream dependencies

### WHAT TO CUT

- Moment-by-moment action choreography (keep outcome, cut blow-by-blow)
- Redundant emotional beats (one realization, not three)
- Atmospheric description that doesn't affect plot
- Backend-only notes marked "NOT FOR PROSE"

Output ONLY the markdown. No preamble."""

    return prompt


def compress_with_llm(prompt: str, verbose: bool = False) -> str:
    """Call Claude to compress the beat sheet."""
    client = anthropic.Anthropic()

    if verbose:
        print("\n" + "=" * 60)
        print("COMPRESSION PROMPT (first 500 chars):")
        print(prompt[:500])
        print("..." if len(prompt) > 500 else "")
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
        print("LLM RESPONSE (first 500 chars):")
        print(response[:500])
        print("..." if len(response) > 500 else "")
        print("=" * 60 + "\n")

    return response


# =============================================================================
# PACKET ASSEMBLY
# =============================================================================

def assemble_packet(
    chapter_num: int,
    compressed_beats: str,
    voice_reminders: list[str],
    previous_ending: str,
    timeline_context: str,
    canon_warnings: list[str],
    voice_sample: str,
    method_actor_briefs: str,
) -> str:
    """Assemble the final chapter packet."""

    # Clean up compressed beats (remove markdown fences if present)
    if compressed_beats.startswith("```markdown"):
        compressed_beats = compressed_beats[len("```markdown"):].strip()
    if compressed_beats.startswith("```"):
        compressed_beats = compressed_beats[3:].strip()
    if compressed_beats.endswith("```"):
        compressed_beats = compressed_beats[:-3].strip()

    voice_text = "\n".join(f"- {r}" for r in voice_reminders)
    warnings_text = "\n".join(f"- {w}" for w in canon_warnings) if canon_warnings else "- None"

    packet = f"""# Chapter {chapter_num} - Writing Packet
Generated for prose writing session. Load this instead of full beat sheet.

## VOICE SAMPLE (Read First - Match This Energy)

{voice_sample if voice_sample else "[No voice sample found]"}

---

## CHARACTERS PRESENT (Method Actor Briefs)

Read these before writing any character's dialogue or internal state.
These are condensed from full profiles—personality, voice patterns, traits.

{method_actor_briefs if method_actor_briefs else "[No character profiles found]"}

---

## TIMELINE
{timeline_context}

## CANON WARNINGS
{warnings_text}

---

{compressed_beats}

---

## VOICE REMINDERS (Ahdia POV)
{voice_text}

---

## PREVIOUS CHAPTER ENDING
{previous_ending if previous_ending else "[Chapter 1 - no previous chapter]"}

---

*Packet generated by compress_chapter.py*
*Full beat sheet: story_bibles/book 2/Chapter_{chapter_num}_STRUCTURE.md*
"""

    return packet


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Compress beat sheets into prose-ready chapter packets"
    )
    parser.add_argument(
        "chapter",
        type=int,
        help="Chapter number to compress (e.g., 1, 2, 12)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without writing packet file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show LLM prompts and responses"
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Open packet in VS Code for human review after generation"
    )

    args = parser.parse_args()
    chapter_num = args.chapter

    print(f"\n{'=' * 60}")
    print(f"COMPRESSING CHAPTER {chapter_num}")
    print(f"{'=' * 60}\n")

    # Load inputs
    print("Loading beat sheet...")
    beat_sheet = load_beat_sheet(chapter_num)
    if not beat_sheet:
        sys.exit(1)
    print(f"  → {len(beat_sheet.split())} words")

    print("Loading CLAUDE.md...")
    claude_md = load_claude_md()
    voice_reminders = extract_voice_reminders(claude_md)
    print(f"  → {len(voice_reminders)} voice reminders")

    print("Loading voice sample...")
    voice_sample = load_voice_sample()
    print(f"  → {len(voice_sample.split())} words" if voice_sample else "  → No voice sample found")

    print("Loading CHARACTER_STATE_INDEX.yaml...")
    state_index = load_character_state_index()
    canon_warnings = extract_canon_warnings(state_index, chapter_num)
    timeline_context = extract_timeline_context(state_index, chapter_num)
    print(f"  → {len(canon_warnings)} canon warnings")
    print(f"  → Timeline: {timeline_context}")

    print("Extracting characters from beat sheet...")
    characters = extract_characters_from_beat_sheet(beat_sheet)
    print(f"  → Found: {', '.join(characters)}")

    print("Loading character trackers...")
    character_trackers = load_character_trackers(characters)
    print(f"  → Loaded {len(character_trackers)} trackers")

    print("Loading character profiles (method actor briefs)...")
    character_profiles = load_character_profiles(characters)
    print(f"  → Loaded {len(character_profiles)} profiles")

    # Generate method actor briefs
    method_actor_briefs = []
    for char, profile in character_profiles.items():
        brief = extract_method_actor_brief(profile, char)
        method_actor_briefs.append(brief)
    method_actor_text = "\n\n---\n\n".join(method_actor_briefs)
    print(f"  → Generated {len(method_actor_briefs)} method actor briefs")

    print("Loading previous chapter ending...")
    previous_ending = load_previous_chapter_ending(chapter_num)
    print(f"  → {len(previous_ending.split())} words" if previous_ending else "  → No previous chapter")

    # Build prompt and compress
    print("\nBuilding compression prompt...")
    prompt = build_compression_prompt(
        beat_sheet=beat_sheet,
        character_trackers=character_trackers,
        timeline_context=timeline_context,
        canon_warnings=canon_warnings,
    )
    print(f"  → Prompt: {len(prompt.split())} words (~{len(prompt) // 4} tokens)")

    print("\nCalling Claude for compression...")
    compressed = compress_with_llm(prompt, verbose=args.verbose)
    print(f"  → Compressed: {len(compressed.split())} words")

    # Assemble packet
    print("\nAssembling packet...")
    packet = assemble_packet(
        chapter_num=chapter_num,
        compressed_beats=compressed,
        voice_reminders=voice_reminders,
        previous_ending=previous_ending,
        timeline_context=timeline_context,
        canon_warnings=canon_warnings,
        voice_sample=voice_sample,
        method_actor_briefs=method_actor_text,
    )
    print(f"  → Packet: {len(packet.split())} words, {len(packet.split(chr(10)))} lines")

    # Output
    if args.dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN - PACKET PREVIEW:")
        print("=" * 60)
        print(packet)
    else:
        output_path = PACKETS_DIR / f"chapter_{chapter_num:02d}_packet.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(packet)
        print(f"\n✓ Packet written to: {output_path}")

        # Open in VS Code for review if requested
        if args.review:
            import subprocess
            print(f"\n📝 Opening packet for human review...")
            try:
                subprocess.run(["code", str(output_path)], check=True)
                print(f"   → Review the packet, fix any compression errors")
                print(f"   → Save your changes before writing prose")
            except FileNotFoundError:
                print(f"   ⚠ 'code' command not found. Open manually:")
                print(f"   → {output_path}")

    # Summary
    print(f"\n{'=' * 60}")
    print("COMPRESSION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Input:  {len(beat_sheet.split()):,} words beat sheet")
    print(f"Output: {len(packet.split()):,} words packet")
    print(f"Ratio:  {len(beat_sheet.split()) / len(packet.split()):.1f}x compression")
    print()


if __name__ == "__main__":
    main()
