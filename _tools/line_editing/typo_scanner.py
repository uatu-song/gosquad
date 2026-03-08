#!/usr/bin/env python3
"""
Typo Scanner
Catches common typos, double words, and potential errors.

This tool finds:
- Double words ("the the")
- Common typos ("teh" instead of "the")
- Homophone errors (their/there/they're)
- Extra/missing spaces
- Common misspellings

Does NOT:
- Do spell checking (that requires a dictionary)
- Flag intentional stylistic choices
- Judge word choices
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict


class TypoScanner:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.text = ""

        # Results
        self.double_words = []
        self.common_typos = []
        self.homophone_errors = []
        self.spacing_issues = []
        self.punctuation_issues = []

        # Common typo patterns
        self.typo_patterns = {
            r'\bteh\b': 'the',
            r'\brecieve\b': 'receive',
            r'\boccured\b': 'occurred',
            r'\bseperate\b': 'separate',
            r'\bdefinately\b': 'definitely',
            r'\baccross\b': 'across',
            r'\bwich\b': 'which',
            r'\bwon\'t\b': 'won\'t',  # Common smart quote issue
            r'\bcant\b': 'can\'t',
            r'\bdont\b': 'don\'t',
            r'\bwont\b': 'won\'t',
            r'\bisnt\b': 'isn\'t',
            r'\barent\b': 'aren\'t',
            r'\bhasnt\b': 'hasn\'t',
            r'\bhavent\b': 'haven\'t',
            r'\bdidnt\b': 'didn\'t',
            r'\bdoesnt\b': 'doesn\'t',
            r'\bcouldnt\b': 'couldn\'t',
            r'\bwouldnt\b': 'wouldn\'t',
            r'\bshouldnt\b': 'shouldn\'t',
        }

        # Homophone patterns (context-sensitive, so just flag for review)
        self.homophones = {
            'their': ['there', 'they\'re'],
            'your': ['you\'re'],
            'its': ['it\'s'],
            'whose': ['who\'s'],
            'affect': ['effect'],
            'than': ['then'],
            'lose': ['loose']
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

    def find_double_words(self):
        """Find consecutive repeated words"""
        print("\n🔍 Finding double words...")

        # Pattern: word boundary, word, whitespace, same word
        pattern = r'\b(\w+)\s+\1\b'

        matches = re.finditer(pattern, self.text, re.IGNORECASE)

        for match in matches:
            word = match.group(1)

            # Get context
            start = max(0, match.start() - 50)
            end = min(len(self.text), match.end() + 50)
            context = self.text[start:end].strip()

            # Calculate line number
            line_num = self.text[:match.start()].count('\n') + 1

            self.double_words.append({
                'word': word,
                'position': match.start(),
                'line': line_num,
                'context': context
            })

        print(f"   Found {len(self.double_words)} double word instances")

    def find_common_typos(self):
        """Find common typo patterns"""
        print("\n🔍 Finding common typos...")

        for pattern, correction in self.typo_patterns.items():
            matches = re.finditer(pattern, self.text, re.IGNORECASE)

            for match in matches:
                typo = match.group(0)

                # Get context
                start = max(0, match.start() - 50)
                end = min(len(self.text), match.end() + 50)
                context = self.text[start:end].strip()

                # Calculate line number
                line_num = self.text[:match.start()].count('\n') + 1

                self.common_typos.append({
                    'typo': typo,
                    'correction': correction,
                    'position': match.start(),
                    'line': line_num,
                    'context': context
                })

        print(f"   Found {len(self.common_typos)} common typos")

    def find_homophone_issues(self):
        """Flag potential homophone misuse for manual review"""
        print("\n🔍 Flagging potential homophone issues...")

        # This is context-sensitive, so we just flag all uses for manual review
        # We'll find sentences that contain these words for review

        for base_word, alternatives in self.homophones.items():
            all_forms = [base_word] + alternatives

            for form in all_forms:
                pattern = r'\b' + re.escape(form) + r'\b'
                matches = re.finditer(pattern, self.text, re.IGNORECASE)

                for match in matches:
                    # Get the full sentence
                    # Find sentence boundaries
                    sent_start = self.text.rfind('.', 0, match.start()) + 1
                    sent_end = self.text.find('.', match.end())
                    if sent_end == -1:
                        sent_end = len(self.text)

                    sentence = self.text[sent_start:sent_end].strip()

                    # Only flag if sentence is not too long (likely a real sentence)
                    if 10 < len(sentence) < 200:
                        line_num = self.text[:match.start()].count('\n') + 1

                        self.homophone_errors.append({
                            'word': match.group(0),
                            'alternatives': all_forms,
                            'position': match.start(),
                            'line': line_num,
                            'sentence': sentence[:150]
                        })

        print(f"   Flagged {len(self.homophone_errors)} homophone uses for review")

    def find_spacing_issues(self):
        """Find spacing problems"""
        print("\n🔍 Finding spacing issues...")

        # Multiple spaces
        pattern = r' {2,}'
        matches = re.finditer(pattern, self.text)

        for match in matches:
            # Get context
            start = max(0, match.start() - 30)
            end = min(len(self.text), match.end() + 30)
            context = self.text[start:end].strip()

            line_num = self.text[:match.start()].count('\n') + 1

            self.spacing_issues.append({
                'type': 'multiple_spaces',
                'spaces': len(match.group(0)),
                'position': match.start(),
                'line': line_num,
                'context': context
            })

        # Missing space after punctuation
        pattern = r'[.!?][A-Z]'
        matches = re.finditer(pattern, self.text)

        for match in matches:
            # Get context
            start = max(0, match.start() - 30)
            end = min(len(self.text), match.end() + 30)
            context = self.text[start:end].strip()

            line_num = self.text[:match.start()].count('\n') + 1

            self.spacing_issues.append({
                'type': 'missing_space_after_punctuation',
                'position': match.start(),
                'line': line_num,
                'context': context
            })

        # Space before punctuation (common typo)
        pattern = r'\s+[,;:!?]'
        matches = re.finditer(pattern, self.text)

        for match in matches:
            # Get context
            start = max(0, match.start() - 30)
            end = min(len(self.text), match.end() + 30)
            context = self.text[start:end].strip()

            line_num = self.text[:match.start()].count('\n') + 1

            self.spacing_issues.append({
                'type': 'space_before_punctuation',
                'position': match.start(),
                'line': line_num,
                'context': context
            })

        print(f"   Found {len(self.spacing_issues)} spacing issues")

    def find_punctuation_issues(self):
        """Find punctuation problems"""
        print("\n🔍 Finding punctuation issues...")

        # Missing closing quote
        # Count quotes in each paragraph
        paragraphs = self.text.split('\n\n')
        position = 0

        for para in paragraphs:
            quote_count = para.count('"')
            single_quote_count = para.count("'")

            # Check for unbalanced quotes (simple check)
            if quote_count % 2 != 0:
                line_num = self.text[:position].count('\n') + 1

                self.punctuation_issues.append({
                    'type': 'unbalanced_quotes',
                    'position': position,
                    'line': line_num,
                    'context': para[:150]
                })

            position += len(para) + 2

        # Multiple punctuation marks (unless intentional like "!?")
        pattern = r'[.]{2,}(?!\.)|[!]{2,}|[?]{2,}'
        matches = re.finditer(pattern, self.text)

        for match in matches:
            # Skip ellipsis (...) intentional
            if match.group(0) == '...':
                continue

            start = max(0, match.start() - 30)
            end = min(len(self.text), match.end() + 30)
            context = self.text[start:end].strip()

            line_num = self.text[:match.start()].count('\n') + 1

            self.punctuation_issues.append({
                'type': 'multiple_punctuation',
                'position': match.start(),
                'line': line_num,
                'context': context
            })

        print(f"   Found {len(self.punctuation_issues)} punctuation issues")

    def generate_report(self, output_dir='line_editing_output'):
        """Generate detailed reports"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\n📊 Generating reports...")

        # JSON report
        json_report = {
            'file': str(self.file_path),
            'double_words': {
                'count': len(self.double_words),
                'instances': self.double_words
            },
            'common_typos': {
                'count': len(self.common_typos),
                'instances': self.common_typos
            },
            'homophone_flags': {
                'count': len(self.homophone_errors),
                'instances': self.homophone_errors
            },
            'spacing_issues': {
                'count': len(self.spacing_issues),
                'instances': self.spacing_issues
            },
            'punctuation_issues': {
                'count': len(self.punctuation_issues),
                'instances': self.punctuation_issues
            }
        }

        json_path = output_path / 'typo_scan.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2)
        print(f"   ✓ JSON report: {json_path}")

        # HTML report
        self._generate_html_report(output_path)

        # Text summary
        self._generate_text_summary(output_path)

    def _generate_text_summary(self, output_path):
        """Generate human-readable summary"""
        summary_path = output_path / 'typo_summary.txt'

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("TYPO SCAN REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"File: {self.file_path.name}\n\n")

            # Double words
            f.write("=" * 80 + "\n")
            f.write("DOUBLE WORDS\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Found {len(self.double_words)} instances\n\n")

            for i, dw in enumerate(self.double_words[:20], 1):
                f.write(f"[{i}] Line {dw['line']}: \"{dw['word']} {dw['word']}\"\n")
                f.write(f"    Context: {dw['context']}\n\n")

            # Common typos
            if self.common_typos:
                f.write("\n" + "=" * 80 + "\n")
                f.write("COMMON TYPOS\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Found {len(self.common_typos)} instances\n\n")

                for i, typo in enumerate(self.common_typos[:20], 1):
                    f.write(f"[{i}] Line {typo['line']}: \"{typo['typo']}\" → \"{typo['correction']}\"\n")
                    f.write(f"    Context: {typo['context']}\n\n")

            # Spacing issues
            if self.spacing_issues:
                f.write("\n" + "=" * 80 + "\n")
                f.write("SPACING ISSUES\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Found {len(self.spacing_issues)} instances\n\n")

                for i, issue in enumerate(self.spacing_issues[:15], 1):
                    f.write(f"[{i}] Line {issue['line']}: {issue['type'].replace('_', ' ')}\n")
                    f.write(f"    Context: {issue['context']}\n\n")

            # Punctuation issues
            if self.punctuation_issues:
                f.write("\n" + "=" * 80 + "\n")
                f.write("PUNCTUATION ISSUES\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Found {len(self.punctuation_issues)} instances\n\n")

                for i, issue in enumerate(self.punctuation_issues[:15], 1):
                    f.write(f"[{i}] Line {issue['line']}: {issue['type'].replace('_', ' ')}\n")
                    f.write(f"    Context: {issue['context']}\n\n")

        print(f"   ✓ Text summary: {summary_path}")

    def _generate_html_report(self, output_path):
        """Generate interactive HTML report"""
        html_path = output_path / 'typo_scan.html'

        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Typo Scan Report</title>
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
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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
            color: #e74c3c;
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
            border-bottom: 2px solid #e74c3c;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .issue-item {
            background: #fff;
            border: 1px solid #e0e0e0;
            border-left: 4px solid #e74c3c;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .line-tag {
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            margin-right: 10px;
        }
        .correction {
            background: #d4edda;
            padding: 5px 10px;
            border-radius: 4px;
            display: inline-block;
            margin: 10px 0;
            color: #155724;
        }
        .context-box {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Typo Scan Report</h1>
            <p>""" + str(self.file_path.name) + """</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.double_words)) + """</div>
                <div class="stat-label">Double Words</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.common_typos)) + """</div>
                <div class="stat-label">Common Typos</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.spacing_issues)) + """</div>
                <div class="stat-label">Spacing Issues</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">""" + str(len(self.punctuation_issues)) + """</div>
                <div class="stat-label">Punctuation</div>
            </div>
        </div>

        <div class="content">
"""

        # Double words
        if self.double_words:
            html += """
            <div class="section">
                <h2>📝 Double Words</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    The same word appears twice in a row.
                </p>
"""

            for dw in self.double_words[:30]:
                html += f"""
                <div class="issue-item">
                    <span class="line-tag">Line {dw['line']}</span>
                    <strong>"{dw['word']} {dw['word']}"</strong>
                    <div class="context-box">{dw['context']}</div>
                </div>
"""

            html += """
            </div>
"""

        # Common typos
        if self.common_typos:
            html += """
            <div class="section">
                <h2>✏️ Common Typos</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    Common misspellings detected.
                </p>
"""

            for typo in self.common_typos[:30]:
                html += f"""
                <div class="issue-item">
                    <span class="line-tag">Line {typo['line']}</span>
                    <strong>"{typo['typo']}"</strong>
                    <div class="correction">→ "{typo['correction']}"</div>
                    <div class="context-box">{typo['context']}</div>
                </div>
"""

            html += """
            </div>
"""

        # Spacing issues
        if self.spacing_issues:
            html += """
            <div class="section">
                <h2>↔️ Spacing Issues</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    Extra/missing spaces detected.
                </p>
"""

            for issue in self.spacing_issues[:20]:
                html += f"""
                <div class="issue-item">
                    <span class="line-tag">Line {issue['line']}</span>
                    <strong>{issue['type'].replace('_', ' ').title()}</strong>
                    <div class="context-box">{issue['context']}</div>
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
        """Run the complete scan"""
        print("\n" + "="*80)
        print("TYPO SCANNER")
        print("="*80)

        self.load_text()
        self.find_double_words()
        self.find_common_typos()
        self.find_homophone_issues()
        self.find_spacing_issues()
        self.find_punctuation_issues()
        self.generate_report()

        print("\n" + "="*80)
        print("✅ SCAN COMPLETE")
        print("="*80)
        print(f"\nResults:")
        print(f"  • {len(self.double_words)} double words")
        print(f"  • {len(self.common_typos)} common typos")
        print(f"  • {len(self.spacing_issues)} spacing issues")
        print(f"  • {len(self.punctuation_issues)} punctuation issues")
        print(f"  • {len(self.homophone_errors)} homophone uses flagged for review")
        print(f"\nReports saved to: line_editing_output/")


def main():
    parser = argparse.ArgumentParser(
        description='Scan for common typos and errors',
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

    scanner = TypoScanner(args.file)
    scanner.run()


if __name__ == '__main__':
    main()
