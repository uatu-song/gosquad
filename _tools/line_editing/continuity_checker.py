#!/usr/bin/env python3
"""
Continuity Checker
Tracks character details, numbers, locations, and facts across the manuscript
to identify potential contradictions.

This tool helps catch inconsistencies like:
- Character eye color changes
- Ages that don't add up
- Locations with different descriptions
- Numbers/dates that conflict
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict


class ContinuityChecker:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.text = ""
        self.chapters = []

        # Track various entities
        self.character_attributes = defaultdict(lambda: defaultdict(list))
        self.numbers = defaultdict(list)
        self.dates_times = defaultdict(list)
        self.locations = defaultdict(list)
        self.facts = []

        # Potential issues
        self.contradictions = []

    def load_text(self):
        """Load and split text into chapters"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
            print(f"✓ Loaded {len(self.text):,} characters from {self.file_path.name}")
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)

        # Split into chapters
        chapter_pattern = r'Chapter\s+\d+'
        splits = re.split(f'({chapter_pattern})', self.text, flags=re.IGNORECASE)

        current_chapter = ""
        chapter_num = 0

        for i, part in enumerate(splits):
            if re.match(chapter_pattern, part, re.IGNORECASE):
                if current_chapter:
                    self.chapters.append({
                        'number': chapter_num,
                        'text': current_chapter,
                        'start_pos': self.text.find(current_chapter)
                    })
                chapter_num += 1
                current_chapter = part
            else:
                current_chapter += part

        # Add final chapter
        if current_chapter:
            self.chapters.append({
                'number': chapter_num,
                'text': current_chapter,
                'start_pos': self.text.find(current_chapter)
            })

        print(f"✓ Detected {len(self.chapters)} chapters")

    def extract_character_names(self):
        """Extract likely character names from text"""
        # Common patterns for names
        name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'

        # Exclusion list
        common_words = {
            'The', 'A', 'An', 'Chapter', 'He', 'She', 'It', 'They', 'But',
            'And', 'Or', 'When', 'Where', 'Why', 'How', 'What', 'Who',
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
            'January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December',
            'North', 'South', 'East', 'West'
        }

        # Find all potential names
        potential_names = re.findall(name_pattern, self.text)
        name_counts = defaultdict(int)

        for name in potential_names:
            if name not in common_words and len(name) > 2:
                name_counts[name] += 1

        # Filter to names that appear multiple times (likely characters)
        characters = {name for name, count in name_counts.items() if count >= 5}

        print(f"✓ Identified {len(characters)} likely characters")
        return characters

    def track_character_attributes(self):
        """Track physical descriptions and attributes of characters"""
        print("\n🔍 Tracking character attributes...")

        characters = self.extract_character_names()

        # Attribute patterns
        attribute_patterns = {
            'eye_color': r"(\w+)\s+eyes?",
            'hair_color': r"(\w+)\s+hair",
            'hair_style': r"(long|short|curly|straight|wavy)\s+hair",
            'height': r"(tall|short|towering|petite|lanky)",
            'age': r"(\d+)[\s-]years?[\s-]old",
            'age_desc': r"(young|old|middle-aged|elderly|teenage|adolescent)"
        }

        for chapter in self.chapters:
            chapter_text = chapter['text']
            chapter_num = chapter['number']

            for character in characters:
                # Find sentences mentioning this character
                sentences = [s for s in re.split(r'[.!?]+', chapter_text)
                           if character in s]

                for sentence in sentences:
                    # Check each attribute pattern
                    for attr_type, pattern in attribute_patterns.items():
                        matches = re.finditer(pattern, sentence, re.IGNORECASE)
                        for match in matches:
                            # Verify it's near the character name
                            char_pos = sentence.find(character)
                            match_pos = match.start()

                            if abs(char_pos - match_pos) < 100:  # Within 100 chars
                                self.character_attributes[character][attr_type].append({
                                    'value': match.group(1).lower(),
                                    'chapter': chapter_num,
                                    'context': sentence.strip()[:150]
                                })

        # Check for contradictions
        for character, attributes in self.character_attributes.items():
            for attr_type, instances in attributes.items():
                unique_values = {}
                for instance in instances:
                    value = instance['value']
                    if value not in unique_values:
                        unique_values[value] = []
                    unique_values[value].append(instance)

                # If more than one unique value for same attribute
                if len(unique_values) > 1:
                    self.contradictions.append({
                        'type': 'character_attribute',
                        'character': character,
                        'attribute': attr_type,
                        'values': unique_values,
                        'severity': 'medium'
                    })

        print(f"   Found {len(self.character_attributes)} characters with tracked attributes")

    def track_numbers_and_dates(self):
        """Track numbers, dates, and times for consistency"""
        print("\n🔍 Tracking numbers, dates, and times...")

        patterns = {
            'specific_date': r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s+\d{4})?\b',
            'year': r'\b(19\d{2}|20\d{2})\b',
            'time': r'\b\d{1,2}:\d{2}(?:\s*[AaPp]\.?[Mm]\.?)?\b',
            'age_reference': r'\b(\d+)[\s-]years?[\s-]old\b',
            'duration': r'\b(\d+)\s+(second|minute|hour|day|week|month|year)s?\b',
            'quantity': r'\b(\d+)\s+(people|person|men|women|children|dollars?|miles?|feet)\b'
        }

        for chapter in self.chapters:
            chapter_num = chapter['number']
            chapter_text = chapter['text']

            for pattern_type, pattern in patterns.items():
                matches = re.finditer(pattern, chapter_text, re.IGNORECASE)
                for match in matches:
                    # Get context
                    start = max(0, match.start() - 50)
                    end = min(len(chapter_text), match.end() + 50)
                    context = chapter_text[start:end].strip()

                    self.numbers[pattern_type].append({
                        'value': match.group(0),
                        'chapter': chapter_num,
                        'context': context
                    })

        print(f"   Tracked {sum(len(v) for v in self.numbers.values())} number/date references")

    def track_location_descriptions(self):
        """Track location descriptions for consistency"""
        print("\n🔍 Tracking location descriptions...")

        # Extract locations (capitalized multi-word phrases)
        location_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b'

        # Common location indicators
        indicators = ['in', 'at', 'near', 'outside', 'inside', 'downtown', 'uptown']

        location_contexts = defaultdict(list)

        for chapter in self.chapters:
            chapter_num = chapter['number']
            sentences = re.split(r'[.!?]+', chapter['text'])

            for sentence in sentences:
                # Look for location patterns near indicators
                for indicator in indicators:
                    if indicator in sentence.lower():
                        matches = re.finditer(location_pattern, sentence)
                        for match in matches:
                            location = match.group(1)
                            # Skip single words and likely person names
                            if ' ' in location:
                                location_contexts[location].append({
                                    'chapter': chapter_num,
                                    'context': sentence.strip()[:200]
                                })

        # Filter to locations mentioned multiple times
        self.locations = {
            loc: contexts for loc, contexts in location_contexts.items()
            if len(contexts) >= 2
        }

        print(f"   Tracked {len(self.locations)} locations mentioned multiple times")

    def check_timeline_consistency(self):
        """Check for timeline contradictions"""
        print("\n🔍 Checking timeline consistency...")

        # Track age references
        age_refs = self.numbers.get('age_reference', [])

        # Group by character if mentioned
        characters = self.extract_character_names()
        character_ages = defaultdict(list)

        for age_ref in age_refs:
            context = age_ref['context'].lower()
            for character in characters:
                if character.lower() in context:
                    try:
                        age = int(re.search(r'\d+', age_ref['value']).group())
                        character_ages[character].append({
                            'age': age,
                            'chapter': age_ref['chapter'],
                            'context': age_ref['context']
                        })
                    except:
                        pass

        # Check for age inconsistencies
        for character, ages in character_ages.items():
            if len(ages) > 1:
                age_values = [a['age'] for a in ages]
                if len(set(age_values)) > 1:
                    # Ages differ - check if it makes sense
                    min_age = min(age_values)
                    max_age = max(age_values)

                    if max_age - min_age > 1:  # More than 1 year difference
                        self.contradictions.append({
                            'type': 'age_inconsistency',
                            'character': character,
                            'ages': ages,
                            'severity': 'high'
                        })

    def generate_report(self, output_dir='line_editing_output'):
        """Generate detailed continuity report"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\n📊 Generating continuity report...")

        # JSON report
        json_report = {
            'file': str(self.file_path),
            'chapters': len(self.chapters),
            'character_attributes': {
                char: {attr: [inst for inst in instances]
                      for attr, instances in attrs.items()}
                for char, attrs in self.character_attributes.items()
            },
            'numbers': dict(self.numbers),
            'locations': dict(self.locations),
            'contradictions': self.contradictions
        }

        json_path = output_path / 'continuity_report.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2)
        print(f"   ✓ JSON report: {json_path}")

        # HTML report
        self._generate_html_report(output_path)

        # Text summary
        self._generate_text_summary(output_path)

    def _generate_text_summary(self, output_path):
        """Generate human-readable summary"""
        summary_path = output_path / 'continuity_summary.txt'

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CONTINUITY CHECK REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"File: {self.file_path.name}\n")
            f.write(f"Chapters analyzed: {len(self.chapters)}\n\n")

            # Contradictions
            if self.contradictions:
                f.write("=" * 80 + "\n")
                f.write("⚠️  POTENTIAL CONTRADICTIONS\n")
                f.write("=" * 80 + "\n\n")

                for i, contra in enumerate(self.contradictions, 1):
                    f.write(f"\n[{i}] {contra['type'].replace('_', ' ').title()}\n")
                    f.write(f"    Severity: {contra['severity'].upper()}\n\n")

                    if contra['type'] == 'character_attribute':
                        f.write(f"    Character: {contra['character']}\n")
                        f.write(f"    Attribute: {contra['attribute'].replace('_', ' ')}\n")
                        f.write(f"    Different values found:\n\n")

                        for value, instances in contra['values'].items():
                            f.write(f"      '{value}' in:\n")
                            for inst in instances:
                                f.write(f"        - Chapter {inst['chapter']}\n")
                                f.write(f"          \"{inst['context']}\"\n\n")

                    elif contra['type'] == 'age_inconsistency':
                        f.write(f"    Character: {contra['character']}\n")
                        f.write(f"    Ages mentioned:\n\n")
                        for age_ref in contra['ages']:
                            f.write(f"      Age {age_ref['age']} in Chapter {age_ref['chapter']}:\n")
                            f.write(f"        \"{age_ref['context']}\"\n\n")
            else:
                f.write("✓ No obvious contradictions detected\n\n")

            # Character attribute summary
            if self.character_attributes:
                f.write("\n" + "=" * 80 + "\n")
                f.write("CHARACTER ATTRIBUTES TRACKED\n")
                f.write("=" * 80 + "\n\n")

                for character, attributes in sorted(self.character_attributes.items())[:10]:
                    f.write(f"\n{character}:\n")
                    for attr_type, instances in attributes.items():
                        values = set(inst['value'] for inst in instances)
                        f.write(f"  • {attr_type.replace('_', ' ')}: {', '.join(values)}\n")

        print(f"   ✓ Text summary: {summary_path}")

    def _generate_html_report(self, output_path):
        """Generate interactive HTML report"""
        html_path = output_path / 'continuity_report.html'

        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Continuity Check Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        .stat-box {
            background: white;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .content { padding: 30px; }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .contradiction-item {
            background: #fff;
            border: 1px solid #e0e0e0;
            border-left: 4px solid #e74c3c;
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .severity-high {
            border-left-color: #e74c3c;
        }
        .severity-medium {
            border-left-color: #f39c12;
        }
        .severity-low {
            border-left-color: #f1c40f;
        }
        .severity-badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        }
        .severity-badge.high { background: #e74c3c; }
        .severity-badge.medium { background: #f39c12; }
        .severity-badge.low { background: #f1c40f; }
        .context-box {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 0.95em;
        }
        .chapter-tag {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            margin-right: 5px;
        }
        .character-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .character-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .attribute-list {
            list-style: none;
            padding: 0;
        }
        .attribute-list li {
            padding: 5px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .attribute-list li:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Continuity Check Report</h1>
            <p>""" + str(self.file_path.name) + """</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.chapters)) + """</div>
                <div class="stat-label">Chapters</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.character_attributes)) + """</div>
                <div class="stat-label">Characters Tracked</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.contradictions)) + """</div>
                <div class="stat-label">Potential Issues</div>
            </div>
        </div>

        <div class="content">
"""

        # Contradictions section
        if self.contradictions:
            html += """
            <div class="section">
                <h2>⚠️ Potential Contradictions</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    These are potential inconsistencies detected. Review each to determine
                    if it's an actual error or an intentional variation.
                </p>
"""

            for i, contra in enumerate(self.contradictions, 1):
                severity = contra.get('severity', 'medium')
                html += f"""
                <div class="contradiction-item severity-{severity}">
                    <span class="severity-badge {severity}">{severity.upper()}</span>
                    <h3>#{i}: {contra['type'].replace('_', ' ').title()}</h3>
"""

                if contra['type'] == 'character_attribute':
                    html += f"""
                    <p><strong>Character:</strong> {contra['character']}</p>
                    <p><strong>Attribute:</strong> {contra['attribute'].replace('_', ' ')}</p>
                    <p style="margin-top: 10px;"><strong>Different values found:</strong></p>
"""
                    for value, instances in contra['values'].items():
                        html += f"<p style='margin-left: 20px;'><strong>'{value}'</strong>:</p>"
                        for inst in instances:
                            html += f"""
                            <div class="context-box">
                                <span class="chapter-tag">Chapter {inst['chapter']}</span>
                                "{inst['context']}"
                            </div>
"""

                elif contra['type'] == 'age_inconsistency':
                    html += f"""
                    <p><strong>Character:</strong> {contra['character']}</p>
                    <p style="margin-top: 10px;"><strong>Ages mentioned:</strong></p>
"""
                    for age_ref in contra['ages']:
                        html += f"""
                        <div class="context-box">
                            <span class="chapter-tag">Chapter {age_ref['chapter']}</span>
                            Age {age_ref['age']}: "{age_ref['context']}"
                        </div>
"""

                html += """
                </div>
"""

            html += """
            </div>
"""
        else:
            html += """
            <div class="section">
                <h2>✅ No Obvious Contradictions</h2>
                <p style="color: #666;">
                    No clear contradictions were detected in tracked attributes.
                    This doesn't mean there are none - manual review is still recommended.
                </p>
            </div>
"""

        # Character attributes section
        if self.character_attributes:
            html += """
            <div class="section">
                <h2>👥 Character Attributes Tracked</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    Physical descriptions and attributes mentioned for each character.
                </p>
"""

            for character, attributes in sorted(self.character_attributes.items())[:15]:
                html += f"""
                <div class="character-card">
                    <div class="character-name">{character}</div>
                    <ul class="attribute-list">
"""
                for attr_type, instances in attributes.items():
                    values = set(inst['value'] for inst in instances)
                    chapters = sorted(set(inst['chapter'] for inst in instances))
                    html += f"""
                        <li>
                            <strong>{attr_type.replace('_', ' ').title()}:</strong> {', '.join(values)}
                            <span style="color: #999; font-size: 0.9em;">
                                (mentioned in chapter{'s' if len(chapters) > 1 else ''} {', '.join(map(str, chapters))})
                            </span>
                        </li>
"""

                html += """
                    </ul>
                </div>
"""

            html += """
            </div>
"""

        html += """
        </div>
    </div>
</body>
</html>
"""

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"   ✓ HTML report: {html_path}")

    def run(self):
        """Run the complete continuity check"""
        print("\n" + "="*80)
        print("CONTINUITY CHECKER")
        print("="*80)

        self.load_text()
        self.track_character_attributes()
        self.track_numbers_and_dates()
        self.track_location_descriptions()
        self.check_timeline_consistency()
        self.generate_report()

        print("\n" + "="*80)
        print("✅ CONTINUITY CHECK COMPLETE")
        print("="*80)
        print(f"\nResults:")
        print(f"  • {len(self.character_attributes)} characters tracked")
        print(f"  • {len(self.contradictions)} potential contradictions found")
        print(f"\nReports saved to: line_editing_output/")


def main():
    parser = argparse.ArgumentParser(
        description='Check continuity of character attributes, numbers, and facts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s manuscript.txt
  %(prog)s manuscript.txt --output results/
        """
    )

    parser.add_argument('file', help='Path to manuscript file')
    parser.add_argument('--output', default='line_editing_output',
                       help='Output directory (default: line_editing_output)')

    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)

    checker = ContinuityChecker(args.file)
    checker.run()


if __name__ == '__main__':
    main()
