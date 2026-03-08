#!/usr/bin/env python3
"""
Master Line Editor
Runs all line editing tools and generates a combined dashboard.

This orchestrator runs:
1. Duplicate Sentence Finder
2. Continuity Checker
3. Proximity Repetition Detector
4. Typo Scanner

Generates a master dashboard with all results.
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import time


class LineEditor:
    def __init__(self, file_path, output_dir='line_editing_output'):
        self.file_path = Path(file_path)
        self.output_dir = Path(output_dir)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.session_dir = self.output_dir / f'session_{self.timestamp}'

        self.tools = [
            {
                'name': 'Duplicate Sentence Finder',
                'script': 'duplicate_sentence_finder.py',
                'key': 'duplicates',
                'description': 'Finding exact and near-duplicate sentences'
            },
            {
                'name': 'Continuity Checker',
                'script': 'continuity_checker.py',
                'key': 'continuity',
                'description': 'Checking character attributes and facts'
            },
            {
                'name': 'Proximity Repetition Detector',
                'script': 'proximity_repetition_detector.py',
                'key': 'proximity',
                'description': 'Finding repeated phrases too close together'
            },
            {
                'name': 'Typo Scanner',
                'script': 'typo_scanner.py',
                'key': 'typos',
                'description': 'Scanning for common typos and errors'
            }
        ]

        self.results = {}
        self.errors = []

    def validate_input(self):
        """Validate input file"""
        if not self.file_path.exists():
            print(f"❌ Error: File '{self.file_path}' not found")
            return False

        if not self.file_path.is_file():
            print(f"❌ Error: '{self.file_path}' is not a file")
            return False

        return True

    def check_tools(self):
        """Check if all tool scripts exist"""
        script_dir = Path(__file__).parent
        missing = []

        for tool in self.tools:
            script_path = script_dir / tool['script']
            if not script_path.exists():
                missing.append(tool['script'])

        if missing:
            print("❌ Missing tool scripts:")
            for script in missing:
                print(f"   - {script}")
            return False

        return True

    def run_tool(self, tool):
        """Run a single tool"""
        print(f"\n{'='*60}")
        print(f"Running: {tool['name']}")
        print(f"{tool['description']}")
        print('='*60)

        script_dir = Path(__file__).parent
        script_path = script_dir / tool['script']

        try:
            result = subprocess.run(
                [sys.executable, str(script_path), str(self.file_path),
                 '--output', str(self.output_dir)],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )

            if result.returncode == 0:
                print(f"✅ {tool['name']} completed successfully")
                self.results[tool['key']] = {
                    'success': True,
                    'output': result.stdout
                }
                return True
            else:
                print(f"❌ {tool['name']} failed")
                if result.stderr:
                    print(f"Error: {result.stderr[:200]}")
                self.errors.append({
                    'tool': tool['name'],
                    'error': result.stderr[:500] if result.stderr else 'Unknown error'
                })
                return False

        except subprocess.TimeoutExpired:
            print(f"⚠️  {tool['name']} timed out")
            self.errors.append({
                'tool': tool['name'],
                'error': 'Tool timed out after 10 minutes'
            })
            return False
        except Exception as e:
            print(f"❌ {tool['name']} error: {str(e)}")
            self.errors.append({
                'tool': tool['name'],
                'error': str(e)
            })
            return False

    def generate_master_dashboard(self):
        """Generate master HTML dashboard"""
        print("\n📊 Generating master dashboard...")

        # Check what reports exist
        reports = {
            'duplicates': self.output_dir / 'duplicate_sentences.html',
            'continuity': self.output_dir / 'continuity_report.html',
            'proximity': self.output_dir / 'proximity_repetitions.html',
            'typos': self.output_dir / 'typo_scan.html'
        }

        existing_reports = {k: v for k, v in reports.items() if v.exists()}

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Line Editing Dashboard - {self.file_path.name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px 10px 0 0;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; margin-top: 5px; }}
        .content {{ padding: 40px; }}
        .intro {{
            background: #e3f2fd;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #2196f3;
        }}
        .intro h2 {{ color: #1976d2; margin-bottom: 10px; }}
        .intro p {{ color: #555; line-height: 1.6; }}
        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .tool-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 25px;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .tool-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }}
        .tool-card.success {{
            border-color: #4caf50;
        }}
        .tool-card.error {{
            border-color: #f44336;
        }}
        .tool-icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}
        .tool-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .tool-description {{
            color: #666;
            margin-bottom: 20px;
            line-height: 1.5;
        }}
        .tool-link {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            transition: background 0.3s;
        }}
        .tool-link:hover {{
            background: #5568d3;
        }}
        .tool-link.disabled {{
            background: #ccc;
            cursor: not-allowed;
        }}
        .status-badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .status-badge.success {{
            background: #d4edda;
            color: #155724;
        }}
        .status-badge.error {{
            background: #f8d7da;
            color: #721c24;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-radius: 0 0 10px 10px;
            border-top: 1px solid #dee2e6;
        }}
        .errors-section {{
            background: #fff3cd;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #ffc107;
        }}
        .errors-section h3 {{
            color: #856404;
            margin-bottom: 15px;
        }}
        .error-item {{
            background: white;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Line Editing Dashboard</h1>
            <p>{self.file_path.name}</p>
            <p style="font-size: 0.9em; margin-top: 10px;">
                Session: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
        </div>

        <div class="content">
            <div class="intro">
                <h2>What is Line Editing?</h2>
                <p>
                    Line editing focuses on technical correctness - catching duplicates, typos,
                    continuity errors, and mechanical issues. <strong>This is NOT about changing
                    your voice or style.</strong> These tools preserve your unique voice while
                    helping you find technical errors that slipped through drafting.
                </p>
            </div>
"""

        # Errors section if any
        if self.errors:
            html += """
            <div class="errors-section">
                <h3>⚠️ Tool Errors</h3>
                <p>Some tools encountered errors during execution:</p>
"""
            for error in self.errors:
                html += f"""
                <div class="error-item">
                    <strong>{error['tool']}:</strong> {error['error'][:100]}
                </div>
"""
            html += """
            </div>
"""

        # Tools grid
        html += """
            <div class="tools-grid">
"""

        tools_info = [
            {
                'key': 'duplicates',
                'icon': '📝',
                'title': 'Duplicate Sentences',
                'description': 'Exact and near-duplicate sentences found in your manuscript. These are likely drafting artifacts where you tried different versions and forgot to remove one.',
                'report': existing_reports.get('duplicates')
            },
            {
                'key': 'continuity',
                'icon': '🔍',
                'title': 'Continuity Check',
                'description': 'Character attributes, ages, and facts tracked across chapters. Flags potential contradictions like changing eye colors or inconsistent ages.',
                'report': existing_reports.get('continuity')
            },
            {
                'key': 'proximity',
                'icon': '🔄',
                'title': 'Proximity Repetition',
                'description': 'Phrases and words repeated too close together. Catches when you use the same distinctive phrase multiple times in a few paragraphs.',
                'report': existing_reports.get('proximity')
            },
            {
                'key': 'typos',
                'icon': '✏️',
                'title': 'Typo Scanner',
                'description': 'Common typos, double words, spacing issues, and mechanical errors. Pure technical cleanup - no judgment of style.',
                'report': existing_reports.get('typos')
            }
        ]

        for tool in tools_info:
            success = tool['key'] in self.results and self.results[tool['key']]['success']
            card_class = 'success' if success else 'error' if tool['key'] in [e['tool'] for e in self.errors] else ''
            status = 'success' if success else 'error'
            status_text = '✅ Completed' if success else '❌ Failed'

            html += f"""
                <div class="tool-card {card_class}">
                    <div class="tool-icon">{tool['icon']}</div>
                    <div class="status-badge {status}">{status_text}</div>
                    <div class="tool-title">{tool['title']}</div>
                    <div class="tool-description">{tool['description']}</div>
"""

            if tool['report']:
                rel_path = tool['report'].name
                html += f"""
                    <a href="{rel_path}" class="tool-link">View Report</a>
"""
            else:
                html += """
                    <span class="tool-link disabled">Report Not Available</span>
"""

            html += """
                </div>
"""

        html += """
            </div>
        </div>

        <div class="footer">
            <p>Line Editing Suite v1.0</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Reports saved to: """ + str(self.output_dir) + """
            </p>
        </div>
    </div>
</body>
</html>
"""

        dashboard_path = self.output_dir / 'line_editing_dashboard.html'
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Dashboard saved to: {dashboard_path}")
        return dashboard_path

    def run(self, tools_to_run=None):
        """Run the line editing suite"""
        print("\n" + "="*80)
        print("LINE EDITING SUITE")
        print("="*80)
        print(f"\nManuscript: {self.file_path.name}")
        print(f"File size: {self.file_path.stat().st_size / 1024:.1f} KB")

        if not self.validate_input():
            return False

        if not self.check_tools():
            print("\n⚠️  Some tools are missing")
            return False

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {self.output_dir}")

        # Determine which tools to run
        if tools_to_run:
            tools = [t for t in self.tools if t['key'] in tools_to_run]
        else:
            tools = self.tools

        print(f"\nRunning {len(tools)} tool(s)...")

        start_time = time.time()

        # Run each tool
        for i, tool in enumerate(tools, 1):
            print(f"\n[{i}/{len(tools)}]")
            self.run_tool(tool)

        elapsed = time.time() - start_time

        # Generate dashboard
        print("\n" + "="*80)
        print("GENERATING MASTER DASHBOARD")
        print("="*80)

        dashboard = self.generate_master_dashboard()

        # Summary
        print("\n" + "="*80)
        print("✅ LINE EDITING COMPLETE")
        print("="*80)
        print(f"\nTools run: {len(tools)}")
        print(f"Successful: {len([r for r in self.results.values() if r.get('success')])}")
        print(f"Failed: {len(self.errors)}")
        print(f"Total time: {elapsed:.1f} seconds")
        print(f"\n📊 View dashboard: {dashboard}")

        return True


def main():
    parser = argparse.ArgumentParser(
        description='Master Line Editor - Run all line editing tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Tools:
  duplicates  - Find duplicate sentences
  continuity  - Check continuity of characters and facts
  proximity   - Find repeated phrases too close together
  typos       - Scan for common typos and errors

Examples:
  %(prog)s manuscript.txt                       # Run all tools
  %(prog)s manuscript.txt --tools duplicates typos   # Run specific tools
  %(prog)s manuscript.txt --output results/     # Custom output directory
        """
    )

    parser.add_argument('file', help='Path to manuscript file')
    parser.add_argument('--tools', nargs='+',
                       choices=['duplicates', 'continuity', 'proximity', 'typos'],
                       help='Specific tools to run (default: all)')
    parser.add_argument('--output', default='line_editing_output',
                       help='Output directory (default: line_editing_output)')

    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)

    editor = LineEditor(args.file, args.output)

    try:
        success = editor.run(args.tools)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
