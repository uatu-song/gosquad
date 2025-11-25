#!/usr/bin/env python3
"""
Duplicate Sentence Finder
Finds exact and near-duplicate sentences in manuscripts.

This tool catches drafting artifacts where sentences were tried in different
locations and one copy wasn't removed.
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
import hashlib


class DuplicateSentenceFinder:
    def __init__(self, file_path, similarity_threshold=0.9):
        self.file_path = Path(file_path)
        self.similarity_threshold = similarity_threshold
        self.text = ""
        self.sentences = []
        self.exact_duplicates = defaultdict(list)
        self.near_duplicates = []

    def load_text(self):
        """Load text from file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
            print(f"✓ Loaded {len(self.text):,} characters from {self.file_path.name}")
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)

    def extract_sentences(self):
        """Extract sentences with their positions"""
        # Split on sentence boundaries but keep the text
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z"])'

        # Find all sentence boundaries
        parts = re.split(f'({sentence_pattern})', self.text)

        # Reconstruct sentences with positions
        position = 0
        current_sentence = ""

        for part in parts:
            current_sentence += part

            # Check if this completes a sentence
            if re.match(r'.*[.!?]\s*$', current_sentence.strip()):
                sentence = current_sentence.strip()

                # Only process sentences that are substantial
                if len(sentence) > 20 and not sentence.startswith('Chapter'):
                    # Calculate line number (approximate)
                    line_num = self.text[:position].count('\n') + 1

                    self.sentences.append({
                        'text': sentence,
                        'position': position,
                        'line': line_num,
                        'normalized': self._normalize_sentence(sentence)
                    })

                position += len(current_sentence)
                current_sentence = ""

        print(f"✓ Extracted {len(self.sentences):,} sentences")

    def _normalize_sentence(self, sentence):
        """Normalize sentence for comparison"""
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', sentence)
        # Remove punctuation for comparison
        normalized = re.sub(r'[^\w\s]', '', normalized)
        # Lowercase
        normalized = normalized.lower().strip()
        return normalized

    def _hash_sentence(self, normalized):
        """Create hash of normalized sentence"""
        return hashlib.md5(normalized.encode()).hexdigest()

    def find_exact_duplicates(self):
        """Find sentences that are exactly the same"""
        print("\n🔍 Finding exact duplicates...")

        sentence_map = defaultdict(list)

        for i, sent in enumerate(self.sentences):
            hash_key = self._hash_sentence(sent['normalized'])
            sentence_map[hash_key].append({
                'index': i,
                'text': sent['text'],
                'line': sent['line'],
                'position': sent['position']
            })

        # Filter to only duplicates (appears more than once)
        for hash_key, occurrences in sentence_map.items():
            if len(occurrences) > 1:
                self.exact_duplicates[hash_key] = occurrences

        print(f"   Found {len(self.exact_duplicates)} unique sentences that appear multiple times")
        total_duplicates = sum(len(occs) for occs in self.exact_duplicates.values())
        print(f"   Total duplicate instances: {total_duplicates}")

    def find_near_duplicates(self):
        """Find sentences that are very similar but not exactly the same"""
        print(f"\n🔍 Finding near-duplicates (>{int(self.similarity_threshold*100)}% similar)...")

        # This is O(n²) but necessary for fuzzy matching
        # Skip sentences already identified as exact duplicates
        exact_indices = set()
        for occurrences in self.exact_duplicates.values():
            for occ in occurrences:
                exact_indices.add(occ['index'])

        checked_pairs = set()

        for i, sent1 in enumerate(self.sentences):
            if i in exact_indices:
                continue

            for j in range(i + 1, len(self.sentences)):
                if j in exact_indices:
                    continue

                # Skip if too far apart in the text (likely intentional repetition)
                position_diff = abs(self.sentences[j]['position'] - sent1['position'])
                if position_diff < 500:  # Within 500 characters - too close
                    continue

                pair_key = (i, j)
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                sent2 = self.sentences[j]

                # Calculate similarity
                similarity = SequenceMatcher(None,
                                           sent1['normalized'],
                                           sent2['normalized']).ratio()

                if similarity >= self.similarity_threshold and similarity < 1.0:
                    self.near_duplicates.append({
                        'sentence1': {
                            'text': sent1['text'],
                            'line': sent1['line'],
                            'position': sent1['position']
                        },
                        'sentence2': {
                            'text': sent2['text'],
                            'line': sent2['line'],
                            'position': sent2['position']
                        },
                        'similarity': similarity
                    })

            # Progress indicator for long texts
            if (i + 1) % 100 == 0:
                print(f"   Checked {i + 1}/{len(self.sentences)} sentences...")

        print(f"   Found {len(self.near_duplicates)} near-duplicate pairs")

    def generate_report(self, output_dir='line_editing_output'):
        """Generate detailed reports"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\n📊 Generating reports...")

        # JSON report
        json_report = {
            'file': str(self.file_path),
            'total_sentences': len(self.sentences),
            'exact_duplicates': {
                'count': len(self.exact_duplicates),
                'instances': []
            },
            'near_duplicates': {
                'count': len(self.near_duplicates),
                'instances': self.near_duplicates
            }
        }

        # Convert exact duplicates to serializable format
        for hash_key, occurrences in self.exact_duplicates.items():
            json_report['exact_duplicates']['instances'].append({
                'text': occurrences[0]['text'],
                'occurrences': occurrences
            })

        json_path = output_path / 'duplicate_sentences.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2)
        print(f"   ✓ JSON report: {json_path}")

        # HTML report
        self._generate_html_report(output_path)

        # Text summary
        self._generate_text_summary(output_path)

    def _generate_text_summary(self, output_path):
        """Generate human-readable text summary"""
        summary_path = output_path / 'duplicate_summary.txt'

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("DUPLICATE SENTENCE REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"File: {self.file_path.name}\n")
            f.write(f"Total sentences analyzed: {len(self.sentences):,}\n\n")

            # Exact duplicates
            f.write("=" * 80 + "\n")
            f.write("EXACT DUPLICATES\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Found {len(self.exact_duplicates)} unique sentences that appear multiple times\n\n")

            for i, (hash_key, occurrences) in enumerate(sorted(
                self.exact_duplicates.items(),
                key=lambda x: len(x[1]),
                reverse=True
            ), 1):
                f.write(f"\n[{i}] Appears {len(occurrences)} times:\n")
                f.write(f"    \"{occurrences[0]['text']}\"\n\n")
                f.write("    Locations:\n")
                for occ in occurrences:
                    f.write(f"    - Line {occ['line']}\n")

            # Near duplicates
            if self.near_duplicates:
                f.write("\n" + "=" * 80 + "\n")
                f.write("NEAR-DUPLICATES (Very Similar Sentences)\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Found {len(self.near_duplicates)} pairs of very similar sentences\n\n")

                for i, pair in enumerate(sorted(
                    self.near_duplicates,
                    key=lambda x: x['similarity'],
                    reverse=True
                )[:20], 1):  # Top 20
                    f.write(f"\n[{i}] Similarity: {pair['similarity']*100:.1f}%\n")
                    f.write(f"    Line {pair['sentence1']['line']}:\n")
                    f.write(f"    \"{pair['sentence1']['text']}\"\n\n")
                    f.write(f"    Line {pair['sentence2']['line']}:\n")
                    f.write(f"    \"{pair['sentence2']['text']}\"\n")

        print(f"   ✓ Text summary: {summary_path}")

    def _generate_html_report(self, output_path):
        """Generate interactive HTML report"""
        html_path = output_path / 'duplicate_sentences.html'

        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Duplicate Sentences Report</title>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            color: #667eea;
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
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .duplicate-item {
            background: #fff;
            border: 1px solid #e0e0e0;
            border-left: 4px solid #e74c3c;
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .near-duplicate-item {
            border-left-color: #f39c12;
        }
        .sentence-text {
            font-size: 1.1em;
            color: #2c3e50;
            margin-bottom: 15px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .locations {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .location-tag {
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        .similarity-badge {
            display: inline-block;
            background: #f39c12;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .comparison {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 10px;
        }
        .comparison-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
        }
        .comparison-label {
            font-weight: bold;
            color: #666;
            margin-bottom: 5px;
        }
        .filter-controls {
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .filter-controls input {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.9em;
            width: 300px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Duplicate Sentences Report</h1>
            <p>""" + str(self.file_path.name) + """</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">""" + f"{len(self.sentences):,}" + """</div>
                <div class="stat-label">Total Sentences</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.exact_duplicates)) + """</div>
                <div class="stat-label">Exact Duplicates</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.near_duplicates)) + """</div>
                <div class="stat-label">Near-Duplicates</div>
            </div>
        </div>

        <div class="content">
"""

        # Exact duplicates section
        if self.exact_duplicates:
            html += """
            <div class="section">
                <h2>🎯 Exact Duplicates</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    These sentences appear word-for-word in multiple locations.
                    Likely drafting artifacts that should be reviewed.
                </p>
"""

            for i, (hash_key, occurrences) in enumerate(sorted(
                self.exact_duplicates.items(),
                key=lambda x: len(x[1]),
                reverse=True
            ), 1):
                html += f"""
                <div class="duplicate-item">
                    <strong>Duplicate #{i}</strong> - Appears {len(occurrences)} times
                    <div class="sentence-text">"{occurrences[0]['text']}"</div>
                    <div class="locations">
"""
                for occ in occurrences:
                    html += f'<span class="location-tag">Line {occ["line"]}</span>\n'

                html += """
                    </div>
                </div>
"""

            html += """
            </div>
"""

        # Near-duplicates section
        if self.near_duplicates:
            html += """
            <div class="section">
                <h2>🔍 Near-Duplicates</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    These sentence pairs are very similar but not identical.
                    May be intentional variations or drafting artifacts.
                </p>
"""

            for i, pair in enumerate(sorted(
                self.near_duplicates,
                key=lambda x: x['similarity'],
                reverse=True
            )[:30], 1):  # Top 30
                html += f"""
                <div class="duplicate-item near-duplicate-item">
                    <div class="similarity-badge">{pair['similarity']*100:.1f}% Similar</div>
                    <div class="comparison">
                        <div class="comparison-item">
                            <div class="comparison-label">Line {pair['sentence1']['line']}</div>
                            <div>"{pair['sentence1']['text']}"</div>
                        </div>
                        <div class="comparison-item">
                            <div class="comparison-label">Line {pair['sentence2']['line']}</div>
                            <div>"{pair['sentence2']['text']}"</div>
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
        print("DUPLICATE SENTENCE FINDER")
        print("="*80)

        self.load_text()
        self.extract_sentences()
        self.find_exact_duplicates()
        self.find_near_duplicates()
        self.generate_report()

        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE")
        print("="*80)
        print(f"\nResults:")
        print(f"  • {len(self.exact_duplicates)} unique sentences appear multiple times")
        print(f"  • {len(self.near_duplicates)} near-duplicate pairs found")
        print(f"\nReports saved to: line_editing_output/")


def main():
    parser = argparse.ArgumentParser(
        description='Find duplicate and near-duplicate sentences in manuscripts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s manuscript.txt
  %(prog)s manuscript.txt --similarity 0.85
  %(prog)s manuscript.txt --output results/
        """
    )

    parser.add_argument('file', help='Path to manuscript file')
    parser.add_argument('--similarity', type=float, default=0.9,
                       help='Similarity threshold for near-duplicates (0.0-1.0, default: 0.9)')
    parser.add_argument('--output', default='line_editing_output',
                       help='Output directory (default: line_editing_output)')

    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)

    if not 0 <= args.similarity <= 1:
        print("Error: Similarity threshold must be between 0.0 and 1.0")
        sys.exit(1)

    finder = DuplicateSentenceFinder(args.file, args.similarity)
    finder.run()


if __name__ == '__main__':
    main()
