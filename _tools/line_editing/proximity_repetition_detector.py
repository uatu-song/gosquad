#!/usr/bin/env python3
"""
Proximity Repetition Detector
Finds phrases and words repeated too close together in the text.

This catches repetitive phrasing like:
- Same 5+ word phrase used within a few paragraphs
- Distinctive words repeated in consecutive sentences
- Character names over-used in a single paragraph

Does NOT flag:
- Common words (the, and, but, etc.)
- Single words (unless very distinctive and close)
- Intentional stylistic repetition (parallel structure)
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict


class ProximityRepetitionDetector:
    def __init__(self, file_path, proximity_threshold=500):
        self.file_path = Path(file_path)
        self.proximity_threshold = proximity_threshold  # characters
        self.text = ""
        self.paragraphs = []

        # Results
        self.phrase_repetitions = []
        self.word_repetitions = []
        self.opening_repetitions = []

        # Common words to ignore
        self.common_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
            'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there',
            'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get',
            'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no',
            'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
            'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
            'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
            'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
            'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has',
            'had', 'were', 'said', 'did', 'having', 'may', 'should', 'am'
        }

    def load_text(self):
        """Load text from file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
            print(f"✓ Loaded {len(self.text):,} characters from {self.file_path.name}")
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)

    def extract_paragraphs(self):
        """Extract paragraphs with their positions"""
        para_splits = self.text.split('\n\n')

        position = 0
        for para_text in para_splits:
            if para_text.strip() and len(para_text.strip()) > 50:
                # Calculate line number
                line_num = self.text[:position].count('\n') + 1

                self.paragraphs.append({
                    'text': para_text.strip(),
                    'position': position,
                    'line': line_num
                })

            position += len(para_text) + 2  # +2 for \n\n

        print(f"✓ Extracted {len(self.paragraphs):,} paragraphs")

    def find_phrase_repetitions(self, min_words=4):
        """Find repeated phrases within proximity threshold"""
        print(f"\n🔍 Finding repeated phrases ({min_words}+ words)...")

        # Extract all n-word phrases
        phrases = defaultdict(list)

        words = re.findall(r'\b\w+\b', self.text.lower())

        # Generate sliding window of phrases
        for i in range(len(words) - min_words + 1):
            phrase_words = words[i:i+min_words]

            # Skip if it's all common words
            if all(w in self.common_words for w in phrase_words):
                continue

            phrase = ' '.join(phrase_words)

            # Calculate character position (approximate)
            position = self.text.lower().find(phrase)
            if position != -1:
                line_num = self.text[:position].count('\n') + 1

                phrases[phrase].append({
                    'position': position,
                    'line': line_num,
                    'index': i
                })

        # Find phrases that appear multiple times
        for phrase, occurrences in phrases.items():
            if len(occurrences) < 2:
                continue

            # Check if any occurrences are within proximity threshold
            for i in range(len(occurrences)):
                for j in range(i + 1, len(occurrences)):
                    distance = abs(occurrences[j]['position'] - occurrences[i]['position'])

                    if distance < self.proximity_threshold:
                        # Get context
                        context1 = self._get_context(occurrences[i]['position'], phrase)
                        context2 = self._get_context(occurrences[j]['position'], phrase)

                        self.phrase_repetitions.append({
                            'phrase': phrase,
                            'distance': distance,
                            'occurrence1': {
                                'line': occurrences[i]['line'],
                                'position': occurrences[i]['position'],
                                'context': context1
                            },
                            'occurrence2': {
                                'line': occurrences[j]['line'],
                                'position': occurrences[j]['position'],
                                'context': context2
                            }
                        })

        print(f"   Found {len(self.phrase_repetitions)} phrase repetitions within {self.proximity_threshold} characters")

    def find_distinctive_word_repetitions(self):
        """Find distinctive words repeated too close together"""
        print(f"\n🔍 Finding distinctive word repetitions...")

        # Extract sentences
        sentences = re.split(r'[.!?]+', self.text)

        # Track word positions
        word_positions = defaultdict(list)

        position = 0
        for sent_text in sentences:
            words = re.findall(r'\b\w+\b', sent_text.lower())

            for word in words:
                # Only track distinctive words (5+ chars, not common)
                if len(word) >= 5 and word not in self.common_words:
                    line_num = self.text[:position].count('\n') + 1
                    word_positions[word].append({
                        'position': position + sent_text.lower().find(word),
                        'line': line_num,
                        'sentence': sent_text.strip()[:100]
                    })

            position += len(sent_text) + 1

        # Find words repeated within threshold
        for word, occurrences in word_positions.items():
            if len(occurrences) < 2:
                continue

            for i in range(len(occurrences) - 1):
                distance = occurrences[i + 1]['position'] - occurrences[i]['position']

                # Only flag if VERY close (within 300 chars)
                if distance < 300:
                    self.word_repetitions.append({
                        'word': word,
                        'distance': distance,
                        'occurrence1': occurrences[i],
                        'occurrence2': occurrences[i + 1]
                    })

        print(f"   Found {len(self.word_repetitions)} distinctive word repetitions")

    def find_sentence_opening_repetitions(self):
        """Find repeated sentence openings in close proximity"""
        print(f"\n🔍 Finding repeated sentence openings...")

        # Extract sentences with positions
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z"])'
        parts = re.split(f'({sentence_pattern})', self.text)

        sentences = []
        position = 0

        for part in parts:
            if part.strip() and len(part.strip()) > 20:
                # Get first 3-4 words
                words = re.findall(r'\b\w+\b', part.strip())[:4]
                if len(words) >= 3:
                    opening = ' '.join(words).lower()

                    line_num = self.text[:position].count('\n') + 1

                    sentences.append({
                        'opening': opening,
                        'full_text': part.strip()[:100],
                        'position': position,
                        'line': line_num
                    })

            position += len(part)

        # Find repeated openings
        openings = defaultdict(list)
        for sent in sentences:
            openings[sent['opening']].append(sent)

        # Check for repetitions within proximity
        for opening, occurrences in openings.items():
            if len(occurrences) < 2:
                continue

            # Skip common openings
            if any(word in self.common_words for word in opening.split()):
                if len(occurrences) < 3:  # Only flag if appears 3+ times
                    continue

            for i in range(len(occurrences) - 1):
                distance = occurrences[i + 1]['position'] - occurrences[i]['position']

                if distance < self.proximity_threshold:
                    self.opening_repetitions.append({
                        'opening': opening,
                        'distance': distance,
                        'occurrence1': occurrences[i],
                        'occurrence2': occurrences[i + 1]
                    })

        print(f"   Found {len(self.opening_repetitions)} repeated sentence openings")

    def _get_context(self, position, phrase):
        """Get context around a phrase"""
        start = max(0, position - 50)
        end = min(len(self.text), position + len(phrase) + 50)
        return self.text[start:end].strip()

    def generate_report(self, output_dir='line_editing_output'):
        """Generate detailed reports"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\n📊 Generating reports...")

        # JSON report
        json_report = {
            'file': str(self.file_path),
            'proximity_threshold': self.proximity_threshold,
            'phrase_repetitions': {
                'count': len(self.phrase_repetitions),
                'instances': self.phrase_repetitions
            },
            'word_repetitions': {
                'count': len(self.word_repetitions),
                'instances': self.word_repetitions
            },
            'opening_repetitions': {
                'count': len(self.opening_repetitions),
                'instances': self.opening_repetitions
            }
        }

        json_path = output_path / 'proximity_repetitions.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2)
        print(f"   ✓ JSON report: {json_path}")

        # HTML report
        self._generate_html_report(output_path)

        # Text summary
        self._generate_text_summary(output_path)

    def _generate_text_summary(self, output_path):
        """Generate human-readable summary"""
        summary_path = output_path / 'proximity_summary.txt'

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("PROXIMITY REPETITION REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"File: {self.file_path.name}\n")
            f.write(f"Proximity threshold: {self.proximity_threshold} characters\n\n")

            # Phrase repetitions
            f.write("=" * 80 + "\n")
            f.write("REPEATED PHRASES\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Found {len(self.phrase_repetitions)} phrase repetitions\n\n")

            for i, rep in enumerate(sorted(
                self.phrase_repetitions,
                key=lambda x: x['distance']
            )[:20], 1):
                f.write(f"\n[{i}] \"{rep['phrase']}\" - Distance: {rep['distance']} chars\n")
                f.write(f"    Line {rep['occurrence1']['line']}:\n")
                f.write(f"    \"{rep['occurrence1']['context']}\"\n\n")
                f.write(f"    Line {rep['occurrence2']['line']}:\n")
                f.write(f"    \"{rep['occurrence2']['context']}\"\n")

            # Sentence openings
            if self.opening_repetitions:
                f.write("\n" + "=" * 80 + "\n")
                f.write("REPEATED SENTENCE OPENINGS\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Found {len(self.opening_repetitions)} repeated openings\n\n")

                for i, rep in enumerate(sorted(
                    self.opening_repetitions,
                    key=lambda x: x['distance']
                )[:15], 1):
                    f.write(f"\n[{i}] \"{rep['opening']}\" - Distance: {rep['distance']} chars\n")
                    f.write(f"    Line {rep['occurrence1']['line']}:\n")
                    f.write(f"    \"{rep['occurrence1']['full_text']}\"\n\n")
                    f.write(f"    Line {rep['occurrence2']['line']}:\n")
                    f.write(f"    \"{rep['occurrence2']['full_text']}\"\n")

        print(f"   ✓ Text summary: {summary_path}")

    def _generate_html_report(self, output_path):
        """Generate interactive HTML report"""
        html_path = output_path / 'proximity_repetitions.html'

        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Proximity Repetition Report</title>
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
            background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
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
            color: #f39c12;
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
            border-bottom: 2px solid #f39c12;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .repetition-item {
            background: #fff;
            border: 1px solid #e0e0e0;
            border-left: 4px solid #f39c12;
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .phrase-highlight {
            background: #fff3cd;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
            font-weight: bold;
            color: #856404;
        }
        .distance-badge {
            display: inline-block;
            background: #f39c12;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .context-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .location-tag {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            margin-bottom: 5px;
        }
        .comparison {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔄 Proximity Repetition Report</h1>
            <p>""" + str(self.file_path.name) + """</p>
            <p style="opacity: 0.9; margin-top: 5px;">Threshold: """ + str(self.proximity_threshold) + """ characters</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.phrase_repetitions)) + """</div>
                <div class="stat-label">Phrase Repetitions</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.opening_repetitions)) + """</div>
                <div class="stat-label">Repeated Openings</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.word_repetitions)) + """</div>
                <div class="stat-label">Word Repetitions</div>
            </div>
        </div>

        <div class="content">
"""

        # Phrase repetitions
        if self.phrase_repetitions:
            html += """
            <div class="section">
                <h2>📝 Repeated Phrases</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    The same multi-word phrases appearing within close proximity.
                    Review to determine if this is intentional or accidental.
                </p>
"""

            for i, rep in enumerate(sorted(
                self.phrase_repetitions,
                key=lambda x: x['distance']
            )[:30], 1):
                html += f"""
                <div class="repetition-item">
                    <div class="distance-badge">{rep['distance']} characters apart</div>
                    <div class="phrase-highlight">"{rep['phrase']}"</div>
                    <div class="comparison">
                        <div class="context-box">
                            <span class="location-tag">Line {rep['occurrence1']['line']}</span>
                            <div style="margin-top: 10px;">"{rep['occurrence1']['context']}"</div>
                        </div>
                        <div class="context-box">
                            <span class="location-tag">Line {rep['occurrence2']['line']}</span>
                            <div style="margin-top: 10px;">"{rep['occurrence2']['context']}"</div>
                        </div>
                    </div>
                </div>
"""

            html += """
            </div>
"""

        # Sentence openings
        if self.opening_repetitions:
            html += """
            <div class="section">
                <h2>🎯 Repeated Sentence Openings</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    Consecutive sentences starting with similar patterns.
                    Can create unintentional rhythm or feel repetitive.
                </p>
"""

            for i, rep in enumerate(sorted(
                self.opening_repetitions,
                key=lambda x: x['distance']
            )[:20], 1):
                html += f"""
                <div class="repetition-item">
                    <div class="distance-badge">{rep['distance']} characters apart</div>
                    <div class="phrase-highlight">"{rep['opening']}"</div>
                    <div class="comparison">
                        <div class="context-box">
                            <span class="location-tag">Line {rep['occurrence1']['line']}</span>
                            <div style="margin-top: 10px;">"{rep['occurrence1']['full_text']}"</div>
                        </div>
                        <div class="context-box">
                            <span class="location-tag">Line {rep['occurrence2']['line']}</span>
                            <div style="margin-top: 10px;">"{rep['occurrence2']['full_text']}"</div>
                        </div>
                    </div>
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
        """Run the complete analysis"""
        print("\n" + "="*80)
        print("PROXIMITY REPETITION DETECTOR")
        print("="*80)

        self.load_text()
        self.extract_paragraphs()
        self.find_phrase_repetitions()
        self.find_distinctive_word_repetitions()
        self.find_sentence_opening_repetitions()
        self.generate_report()

        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE")
        print("="*80)
        print(f"\nResults:")
        print(f"  • {len(self.phrase_repetitions)} phrase repetitions")
        print(f"  • {len(self.opening_repetitions)} repeated sentence openings")
        print(f"  • {len(self.word_repetitions)} distinctive word repetitions")
        print(f"\nReports saved to: line_editing_output/")


def main():
    parser = argparse.ArgumentParser(
        description='Detect phrases and words repeated too close together',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s manuscript.txt
  %(prog)s manuscript.txt --threshold 1000
  %(prog)s manuscript.txt --output results/
        """
    )

    parser.add_argument('file', help='Path to manuscript file')
    parser.add_argument('--threshold', type=int, default=500,
                       help='Proximity threshold in characters (default: 500)')
    parser.add_argument('--output', default='line_editing_output',
                       help='Output directory (default: line_editing_output)')

    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)

    detector = ProximityRepetitionDetector(args.file, args.threshold)
    detector.run()


if __name__ == '__main__':
    main()
