#!/usr/bin/env python3
"""
Interactive Chapter Corrector
Extract a chapter, review issues interactively, and export corrected version.

This tool:
1. Extracts a single chapter
2. Finds all issues (duplicates, typos, repetitions)
3. Presents each issue for your review
4. Applies only approved fixes
5. Exports clean .txt ready for Dabble Writer
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher


class ChapterCorrector:
    def __init__(self, file_path, chapter_num):
        self.file_path = Path(file_path)
        self.chapter_num = chapter_num
        self.text = ""
        self.chapter_text = ""
        self.chapter_start = 0
        self.chapter_end = 0

        # Issues found
        self.issues = []
        self.applied_fixes = []
        self.skipped = []
        self.flagged = []

        # Common words to ignore
        self.common_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
            'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there',
            'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get'
        }

    def load_text(self):
        """Load manuscript"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
            print(f"✓ Loaded manuscript: {len(self.text):,} characters")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            sys.exit(1)

    def extract_chapter(self):
        """Extract the specified chapter"""
        print(f"\n📖 Extracting Chapter {self.chapter_num}...")

        # Find chapter boundaries
        chapter_pattern = r'Chapter\s+\d+'
        matches = list(re.finditer(chapter_pattern, self.text, re.IGNORECASE))

        if not matches:
            print("❌ No chapters found in manuscript")
            sys.exit(1)

        # Find our chapter
        chapter_match = None
        next_match = None

        for i, match in enumerate(matches):
            chapter_text = match.group()
            num = int(re.search(r'\d+', chapter_text).group())

            if num == self.chapter_num:
                chapter_match = match
                if i + 1 < len(matches):
                    next_match = matches[i + 1]
                break

        if not chapter_match:
            print(f"❌ Chapter {self.chapter_num} not found")
            print(f"   Found chapters: 1-{len(matches)}")
            sys.exit(1)

        # Extract chapter text
        self.chapter_start = chapter_match.start()
        self.chapter_end = next_match.start() if next_match else len(self.text)
        self.chapter_text = self.text[self.chapter_start:self.chapter_end]

        # Calculate stats
        word_count = len(re.findall(r'\b\w+\b', self.chapter_text))
        line_count = self.chapter_text.count('\n')

        print(f"✓ Chapter {self.chapter_num} extracted")
        print(f"  • {word_count:,} words")
        print(f"  • {line_count:,} lines")
        print(f"  • {len(self.chapter_text):,} characters")

    def find_double_words(self):
        """Find double words in chapter"""
        pattern = r'\b(\w+)\s+\1\b'
        matches = re.finditer(pattern, self.chapter_text, re.IGNORECASE)

        for match in matches:
            word = match.group(1)
            start = match.start()
            end = match.end()

            # Get context
            context_start = max(0, start - 50)
            context_end = min(len(self.chapter_text), end + 50)
            context = self.chapter_text[context_start:context_end].strip()

            # Create fix
            fixed_text = self.chapter_text[start:end].replace(
                match.group(0),
                word,
                1
            )

            self.issues.append({
                'type': 'double_word',
                'severity': 'high',
                'word': word,
                'position': start,
                'length': end - start,
                'context': context,
                'original': match.group(0),
                'fixed': word,
                'description': f'Double word "{word}"'
            })

    def find_typos(self):
        """Find common typos"""
        typo_patterns = {
            r'\bteh\b': 'the',
            r'\brecieve\b': 'receive',
            r'\boccured\b': 'occurred',
            r'\bseperate\b': 'separate',
            r'\bdefinately\b': 'definitely',
            r'\baccross\b': 'across',
            r'\bwich\b': 'which',
        }

        for pattern, correction in typo_patterns.items():
            matches = re.finditer(pattern, self.chapter_text, re.IGNORECASE)

            for match in matches:
                start = match.start()
                end = match.end()

                context_start = max(0, start - 50)
                context_end = min(len(self.chapter_text), end + 50)
                context = self.chapter_text[context_start:context_end].strip()

                self.issues.append({
                    'type': 'typo',
                    'severity': 'high',
                    'position': start,
                    'length': end - start,
                    'context': context,
                    'original': match.group(0),
                    'fixed': correction,
                    'description': f'Common typo: "{match.group(0)}" → "{correction}"'
                })

    def find_spacing_issues(self):
        """Find spacing problems"""
        # Multiple spaces
        pattern = r' {2,}'
        matches = re.finditer(pattern, self.chapter_text)

        for match in matches:
            start = match.start()
            end = match.end()

            context_start = max(0, start - 30)
            context_end = min(len(self.chapter_text), end + 30)
            context = self.chapter_text[context_start:context_end].strip()

            self.issues.append({
                'type': 'spacing',
                'severity': 'medium',
                'position': start,
                'length': end - start,
                'context': context,
                'original': match.group(0),
                'fixed': ' ',
                'description': f'Multiple spaces ({len(match.group(0))} spaces)'
            })

        # Missing space after punctuation
        pattern = r'[.!?][A-Z]'
        matches = re.finditer(pattern, self.chapter_text)

        for match in matches:
            start = match.start()
            end = match.end()

            context_start = max(0, start - 30)
            context_end = min(len(self.chapter_text), end + 30)
            context = self.chapter_text[context_start:context_end].strip()

            fixed = match.group(0)[0] + ' ' + match.group(0)[1]

            self.issues.append({
                'type': 'spacing',
                'severity': 'high',
                'position': start,
                'length': end - start,
                'context': context,
                'original': match.group(0),
                'fixed': fixed,
                'description': 'Missing space after punctuation'
            })

    def find_repeated_phrases(self):
        """Find phrases repeated in close proximity"""
        words = re.findall(r'\b\w+\b', self.chapter_text.lower())

        # Look for 4+ word phrases
        phrases = defaultdict(list)
        min_words = 4

        for i in range(len(words) - min_words + 1):
            phrase_words = words[i:i+min_words]

            # Skip if all common words
            if all(w in self.common_words for w in phrase_words):
                continue

            phrase = ' '.join(phrase_words)

            # Find position in original text
            position = self.chapter_text.lower().find(phrase)
            if position != -1:
                phrases[phrase].append(position)

        # Find phrases that repeat within 500 characters
        for phrase, positions in phrases.items():
            if len(positions) < 2:
                continue

            for i in range(len(positions) - 1):
                distance = positions[i + 1] - positions[i]

                if distance < 500:
                    # Get contexts
                    context1_start = max(0, positions[i] - 50)
                    context1_end = min(len(self.chapter_text), positions[i] + len(phrase) + 50)
                    context1 = self.chapter_text[context1_start:context1_end].strip()

                    context2_start = max(0, positions[i + 1] - 50)
                    context2_end = min(len(self.chapter_text), positions[i + 1] + len(phrase) + 50)
                    context2 = self.chapter_text[context2_start:context2_end].strip()

                    self.issues.append({
                        'type': 'repetition',
                        'severity': 'low',
                        'phrase': phrase,
                        'distance': distance,
                        'position': positions[i + 1],  # Second occurrence
                        'length': 0,  # Don't auto-fix
                        'context': f"First: {context1}\n\nSecond: {context2}",
                        'original': None,
                        'fixed': None,
                        'description': f'Phrase "{phrase}" repeated {distance} chars apart'
                    })
                    break  # Only report first repetition

    def analyze_chapter(self):
        """Run all analysis tools"""
        print("\n🔍 Analyzing chapter for issues...")

        self.find_double_words()
        self.find_typos()
        self.find_spacing_issues()
        self.find_repeated_phrases()

        # Sort issues by position
        self.issues.sort(key=lambda x: x['position'])

        # Count by type
        counts = defaultdict(int)
        for issue in self.issues:
            counts[issue['type']] += 1

        print(f"\n✓ Analysis complete. Found {len(self.issues)} issues:")
        for issue_type, count in sorted(counts.items()):
            print(f"  • {count} {issue_type.replace('_', ' ')}")

    def review_issues_interactively(self):
        """Present each issue for user review"""
        if not self.issues:
            print("\n✅ No issues found! Chapter looks clean.")
            return

        print("\n" + "═" * 70)
        print("INTERACTIVE REVIEW")
        print("═" * 70)
        print("\nFor each issue, you can:")
        print("  y = Yes, apply fix")
        print("  n = No, keep original")
        print("  s = Skip for now, flag for later review")
        print("  q = Quit review (keep remaining as-is)")
        print()

        for i, issue in enumerate(self.issues, 1):
            print("\n" + "═" * 70)
            print(f"Issue #{i}/{len(self.issues)}: {issue['description']}")
            print("─" * 70)

            # Show context
            print(f"\nContext (position {issue['position']}):")
            print(f'"{issue["context"]}"')

            # Show fix if available
            if issue['fixed']:
                print("\n" + "─" * 70)
                print(f"Original: \"{issue['original']}\"")
                print(f"Fixed:    \"{issue['fixed']}\"")
            else:
                print("\n" + "─" * 70)
                print("ℹ️  Informational only - no auto-fix suggested")
                print("   Review manually and decide if change needed")

            print("─" * 70)

            # Get user decision
            while True:
                if issue['fixed']:
                    choice = input("\nApply this fix? [y/n/s/q]: ").lower().strip()
                else:
                    choice = input("\nFlag for review? [y/n/s/q]: ").lower().strip()

                if choice in ['y', 'n', 's', 'q']:
                    break
                print("Invalid choice. Please enter y, n, s, or q")

            if choice == 'q':
                print("\n⏸️  Review paused. Keeping remaining issues as-is.")
                break
            elif choice == 'y':
                if issue['fixed']:
                    self.applied_fixes.append(issue)
                    print("✓ Fix will be applied")
                else:
                    self.flagged.append(issue)
                    print("🏴 Flagged for manual review")
            elif choice == 's':
                self.flagged.append(issue)
                print("⚠️  Flagged for later review")
            else:
                self.skipped.append(issue)
                print("✗ Keeping original")

    def apply_fixes(self):
        """Apply approved fixes to chapter text"""
        if not self.applied_fixes:
            print("\n📝 No fixes to apply")
            return self.chapter_text

        print(f"\n📝 Applying {len(self.applied_fixes)} fixes...")

        # Sort by position (reverse) to apply from end to start
        fixes = sorted(self.applied_fixes, key=lambda x: x['position'], reverse=True)

        corrected = self.chapter_text

        for fix in fixes:
            start = fix['position']
            end = start + fix['length']

            # Replace the text
            corrected = corrected[:start] + fix['fixed'] + corrected[end:]
            print(f"  ✓ Fixed: {fix['description']}")

        return corrected

    def export_chapter(self, corrected_text):
        """Export corrected chapter to file"""
        output_filename = f"chapter_{self.chapter_num}_corrected.txt"
        output_path = Path('line_editing_output') / output_filename
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(corrected_text)

        print(f"\n💾 Exported to: {output_path}")
        return output_path

    def generate_review_notes(self):
        """Generate notes file for flagged issues"""
        if not self.flagged:
            return

        notes_filename = f"chapter_{self.chapter_num}_review_notes.txt"
        notes_path = Path('line_editing_output') / notes_filename

        with open(notes_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"CHAPTER {self.chapter_num} - ITEMS FLAGGED FOR REVIEW\n")
            f.write("=" * 80 + "\n\n")

            for i, issue in enumerate(self.flagged, 1):
                f.write(f"\n[{i}] {issue['description']}\n")
                f.write(f"Position: {issue['position']}\n")
                f.write(f"\nContext:\n{issue['context']}\n")
                f.write("\n" + "-" * 80 + "\n")

        print(f"📋 Review notes saved to: {notes_path}")

    def print_summary(self):
        """Print session summary"""
        print("\n" + "═" * 70)
        print("SESSION SUMMARY")
        print("═" * 70)
        print(f"\nChapter {self.chapter_num}:")
        print(f"  • Total issues found: {len(self.issues)}")
        print(f"  ✓ Fixes applied: {len(self.applied_fixes)}")
        print(f"  ✗ Kept original: {len(self.skipped)}")
        print(f"  ⚠  Flagged for review: {len(self.flagged)}")

        if self.applied_fixes:
            print(f"\n✅ Chapter corrected and exported")
            print(f"   Ready to paste into Dabble Writer")

        if self.flagged:
            print(f"\n⚠️  {len(self.flagged)} items need manual review")

    def run(self):
        """Run the complete correction workflow"""
        print("\n" + "═" * 70)
        print("INTERACTIVE CHAPTER CORRECTOR")
        print("═" * 70)

        self.load_text()
        self.extract_chapter()
        self.analyze_chapter()

        if not self.issues:
            # No issues, just export original
            self.export_chapter(self.chapter_text)
            print("\n✅ Chapter is clean! Exported original for reference.")
            return

        self.review_issues_interactively()

        # Apply fixes
        corrected_text = self.apply_fixes()

        # Export
        self.export_chapter(corrected_text)

        # Generate review notes if needed
        self.generate_review_notes()

        # Summary
        self.print_summary()

        print("\n" + "═" * 70)
        print("✅ CHAPTER CORRECTION COMPLETE")
        print("═" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Interactive chapter corrector - review and fix issues one by one',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  %(prog)s manuscript.txt --chapter 5

  This will:
  1. Extract Chapter 5
  2. Find all issues (typos, duplicates, repetitions)
  3. Present each issue for your review
  4. Apply only the fixes you approve
  5. Export corrected chapter ready for Dabble Writer
        """
    )

    parser.add_argument('file', help='Path to manuscript file')
    parser.add_argument('--chapter', '-c', type=int, required=True,
                       help='Chapter number to correct')

    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"❌ Error: File '{args.file}' not found")
        sys.exit(1)

    corrector = ChapterCorrector(args.file, args.chapter)

    try:
        corrector.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
