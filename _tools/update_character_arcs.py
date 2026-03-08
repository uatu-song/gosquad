#!/usr/bin/env python3
"""
Character Arc Update Script

Detects recently changed story files and prompts for character arc updates.
Run after committing story beats to keep character arcs synchronized.

Usage:
    python3 editor_suite/update_character_arcs.py
"""

import subprocess
import re
from pathlib import Path

# Character names to track
CHARACTERS = {
    'Ahdia': 'character_arcs/Ahdia_Arc_Tracker.md',
    'Ruth': 'character_arcs/Ruth_Arc_Tracker.md',
    'Ryu': 'character_arcs/Ryu_Arc_Tracker.md',
    'AR-Ryu': 'character_arcs/Ryu_Arc_Tracker.md',
    'Tess': 'character_arcs/Tess_Arc_Tracker.md',
    'Ben': 'character_arcs/Ben_Arc_Tracker.md',
    'Victor': 'character_arcs/Victor_Arc_Tracker.md',
    'Diana': 'character_arcs/Diana_Arc_Tracker.md',
    'Korede': 'character_arcs/Korede_Arc_Tracker.md',
    'Firas': 'character_arcs/Firas_Arc_Tracker.md',
    'Leah': 'character_arcs/Leah_Arc_Tracker.md',
}

def get_recent_changes():
    """Get list of recently modified story files from git."""
    try:
        # Get files changed in last commit
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split('\n')

        # Filter for story bible files
        story_files = [f for f in files if 'story_bibles' in f and f.endswith('.md')]

        return story_files
    except subprocess.CalledProcessError:
        print("⚠ No recent commits found or git error")
        return []

def detect_characters_in_file(filepath):
    """Scan file for character mentions."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        found = set()
        for char_name in CHARACTERS.keys():
            # Case-insensitive search for character names
            if re.search(rf'\b{char_name}\b', content, re.IGNORECASE):
                found.add(char_name)

        return found
    except FileNotFoundError:
        return set()

def main():
    print("=" * 80)
    print("CHARACTER ARC UPDATE DETECTOR")
    print("=" * 80)
    print()

    # Get recent changes
    changed_files = get_recent_changes()

    if not changed_files:
        print("No story bible files changed in last commit.")
        print("Run this script after committing chapter beats.")
        return

    print("Recently changed files:")
    for f in changed_files:
        print(f"  - {f}")
    print()

    # Detect affected characters
    all_characters = set()
    for filepath in changed_files:
        chars = detect_characters_in_file(filepath)
        all_characters.update(chars)

    if not all_characters:
        print("No character mentions detected in changed files.")
        return

    # Map to arc tracker files
    arc_files = set()
    for char in all_characters:
        arc_files.add(CHARACTERS[char])

    print("Affected characters detected:")
    for char in sorted(all_characters):
        print(f"  - {char}")
    print()

    print("Character arc files to update:")
    for arc_file in sorted(arc_files):
        print(f"  - {arc_file}")
    print()

    print("=" * 80)
    print("ACTION REQUIRED:")
    print("Claude should now update the above character arc tracker files")
    print("based on the story changes, then checkpoint commit.")
    print("=" * 80)

if __name__ == '__main__':
    main()
