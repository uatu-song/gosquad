#!/usr/bin/env python3
"""
Session Recap Generator
Creates narrative summaries of line editing sessions for documentation,
blog posts, or behind-the-scenes content about the writing process.

Tracks:
- Chapters edited
- Issues found and fixed
- Before/after examples
- Statistics and insights
- Process notes
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class SessionRecapGenerator:
    def __init__(self, output_dir='line_editing_output'):
        self.output_dir = Path(output_dir)
        self.session_file = self.output_dir / 'editing_sessions.json'
        self.sessions = []

        # Load existing sessions
        self.load_sessions()

    def load_sessions(self):
        """Load previous sessions from file"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    self.sessions = json.load(f)
                print(f"✓ Loaded {len(self.sessions)} previous sessions")
            except:
                self.sessions = []
        else:
            self.sessions = []

    def save_sessions(self):
        """Save sessions to file"""
        self.output_dir.mkdir(exist_ok=True)
        with open(self.session_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)

    def start_new_session(self):
        """Start a new editing session"""
        session = {
            'date': datetime.now().isoformat(),
            'date_readable': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'chapters_edited': [],
            'total_issues_found': 0,
            'total_fixes_applied': 0,
            'total_issues_flagged': 0,
            'total_skipped': 0,
            'by_type': defaultdict(int),
            'examples': [],
            'notes': []
        }
        return session

    def add_chapter_to_session(self, session, chapter_num, issues_found,
                               fixes_applied, flagged, skipped, examples=None, notes=None):
        """Add a chapter's editing results to the session"""
        chapter_data = {
            'chapter': chapter_num,
            'issues_found': issues_found,
            'fixes_applied': fixes_applied,
            'flagged': flagged,
            'skipped': skipped,
            'status': 'clean' if issues_found == 0 else 'corrected'
        }

        if examples:
            chapter_data['examples'] = examples
        if notes:
            chapter_data['notes'] = notes

        session['chapters_edited'].append(chapter_data)
        session['total_issues_found'] += issues_found
        session['total_fixes_applied'] += fixes_applied
        session['total_issues_flagged'] += flagged
        session['total_skipped'] += skipped

    def generate_recap(self, session, format='markdown'):
        """Generate a narrative recap of the session"""
        if format == 'markdown':
            return self._generate_markdown_recap(session)
        elif format == 'html':
            return self._generate_html_recap(session)
        elif format == 'text':
            return self._generate_text_recap(session)

    def _generate_markdown_recap(self, session):
        """Generate markdown format recap"""
        md = f"""# Line Editing Session - {session['date_readable']}

## Session Summary

**Chapters Edited:** {len(session['chapters_edited'])}
**Total Issues Found:** {session['total_issues_found']}
**Fixes Applied:** {session['total_fixes_applied']}
**Flagged for Review:** {session['total_issues_flagged']}
**Kept Original:** {session['total_skipped']}

"""

        # Chapters breakdown
        md += "## Chapters Edited\n\n"
        for chapter_data in session['chapters_edited']:
            status_emoji = "✨" if chapter_data['status'] == 'clean' else "✏️"
            md += f"### {status_emoji} Chapter {chapter_data['chapter']}\n\n"

            if chapter_data['status'] == 'clean':
                md += "**Status:** Clean - no issues found!\n\n"
            else:
                md += f"- **Issues found:** {chapter_data['issues_found']}\n"
                md += f"- **Fixes applied:** {chapter_data['fixes_applied']}\n"
                md += f"- **Flagged for review:** {chapter_data['flagged']}\n"
                md += f"- **Kept original:** {chapter_data['skipped']}\n\n"

            # Examples
            if chapter_data.get('examples'):
                md += "**Notable fixes:**\n\n"
                for example in chapter_data['examples']:
                    md += f"- {example['description']}\n"
                    if 'before' in example and 'after' in example:
                        md += f"  - Before: `{example['before']}`\n"
                        md += f"  - After: `{example['after']}`\n"
                    md += "\n"

            # Notes
            if chapter_data.get('notes'):
                md += "**Process notes:**\n\n"
                for note in chapter_data['notes']:
                    md += f"- {note}\n"
                md += "\n"

        # Issue types breakdown
        if session['by_type']:
            md += "## Issues by Type\n\n"
            for issue_type, count in sorted(session['by_type'].items(),
                                          key=lambda x: x[1], reverse=True):
                md += f"- **{issue_type.replace('_', ' ').title()}:** {count}\n"
            md += "\n"

        # Overall notes
        if session.get('notes'):
            md += "## Session Notes\n\n"
            for note in session['notes']:
                md += f"- {note}\n"
            md += "\n"

        # Insights
        md += "## Process Insights\n\n"

        if session['total_issues_found'] == 0:
            md += "All chapters reviewed were technically clean! The drafting process was thorough.\n\n"
        else:
            fix_rate = (session['total_fixes_applied'] / session['total_issues_found'] * 100) if session['total_issues_found'] > 0 else 0
            md += f"Applied {session['total_fixes_applied']} fixes out of {session['total_issues_found']} issues found ({fix_rate:.1f}% fix rate).\n\n"

            if session['total_issues_flagged'] > 0:
                md += f"{session['total_issues_flagged']} items flagged for manual review - these require author judgment rather than automatic correction.\n\n"

            if session['total_skipped'] > 0:
                md += f"Kept {session['total_skipped']} items as-is - intentional style choices or acceptable variations.\n\n"

        md += "---\n\n"
        md += f"*Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n"

        return md

    def _generate_html_recap(self, session):
        """Generate HTML format recap"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Line Editing Session - {session['date_readable']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; font-size: 1.1em; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        .stat-box {{
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            display: block;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .content {{ padding: 40px; }}
        .chapter-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 25px;
        }}
        .chapter-card.clean {{ border-left-color: #28a745; }}
        .chapter-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }}
        .chapter-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .status-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        .status-badge.clean {{ background: #d4edda; color: #155724; }}
        .status-badge.corrected {{ background: #fff3cd; color: #856404; }}
        .chapter-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        .chapter-stat {{
            background: white;
            padding: 10px;
            border-radius: 6px;
            text-align: center;
        }}
        .chapter-stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .chapter-stat-label {{
            font-size: 0.85em;
            color: #666;
            margin-top: 3px;
        }}
        .examples {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
        }}
        .example-item {{
            padding: 10px 0;
            border-bottom: 1px solid #e9ecef;
        }}
        .example-item:last-child {{ border-bottom: none; }}
        .before-after {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 8px;
        }}
        .before, .after {{
            padding: 8px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9em;
        }}
        .before {{ background: #f8d7da; }}
        .after {{ background: #d4edda; }}
        .insights {{
            background: #e7f3ff;
            border-left: 4px solid #2196f3;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
        }}
        .insights h2 {{
            color: #1976d2;
            margin-bottom: 15px;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Line Editing Session</h1>
            <p>{session['date_readable']}</p>
        </div>

        <div class="stats">
            <div class="stat-box">
                <span class="stat-value">{len(session['chapters_edited'])}</span>
                <div class="stat-label">Chapters</div>
            </div>
            <div class="stat-box">
                <span class="stat-value">{session['total_issues_found']}</span>
                <div class="stat-label">Issues Found</div>
            </div>
            <div class="stat-box">
                <span class="stat-value">{session['total_fixes_applied']}</span>
                <div class="stat-label">Fixes Applied</div>
            </div>
            <div class="stat-box">
                <span class="stat-value">{session['total_issues_flagged']}</span>
                <div class="stat-label">Flagged</div>
            </div>
        </div>

        <div class="content">
            <h2 style="margin-bottom: 20px; color: #2c3e50;">Chapters Edited</h2>
"""

        # Chapters
        for chapter_data in session['chapters_edited']:
            status_class = 'clean' if chapter_data['status'] == 'clean' else 'corrected'
            status_emoji = "✨" if chapter_data['status'] == 'clean' else "✏️"
            status_text = "Clean" if chapter_data['status'] == 'clean' else "Corrected"

            html += f"""
            <div class="chapter-card {status_class}">
                <div class="chapter-header">
                    <span class="chapter-title">{status_emoji} Chapter {chapter_data['chapter']}</span>
                    <span class="status-badge {status_class}">{status_text}</span>
                </div>
"""

            if chapter_data['status'] != 'clean':
                html += f"""
                <div class="chapter-stats">
                    <div class="chapter-stat">
                        <div class="chapter-stat-value">{chapter_data['issues_found']}</div>
                        <div class="chapter-stat-label">Issues</div>
                    </div>
                    <div class="chapter-stat">
                        <div class="chapter-stat-value">{chapter_data['fixes_applied']}</div>
                        <div class="chapter-stat-label">Fixed</div>
                    </div>
                    <div class="chapter-stat">
                        <div class="chapter-stat-value">{chapter_data['flagged']}</div>
                        <div class="chapter-stat-label">Flagged</div>
                    </div>
                    <div class="chapter-stat">
                        <div class="chapter-stat-value">{chapter_data['skipped']}</div>
                        <div class="chapter-stat-label">Skipped</div>
                    </div>
                </div>
"""

                if chapter_data.get('examples'):
                    html += '<div class="examples"><strong>Notable Fixes:</strong>'
                    for example in chapter_data['examples']:
                        html += f'<div class="example-item">{example["description"]}'
                        if 'before' in example and 'after' in example:
                            html += f"""
                            <div class="before-after">
                                <div class="before"><strong>Before:</strong><br>{example['before']}</div>
                                <div class="after"><strong>After:</strong><br>{example['after']}</div>
                            </div>
"""
                        html += '</div>'
                    html += '</div>'

            html += '</div>'

        # Insights
        html += '<div class="insights"><h2>📊 Process Insights</h2>'

        if session['total_issues_found'] == 0:
            html += '<p>All chapters reviewed were technically clean! The drafting process was thorough.</p>'
        else:
            fix_rate = (session['total_fixes_applied'] / session['total_issues_found'] * 100) if session['total_issues_found'] > 0 else 0
            html += f'<p>Applied <strong>{session["total_fixes_applied"]}</strong> fixes out of <strong>{session["total_issues_found"]}</strong> issues found ({fix_rate:.1f}% fix rate).</p>'

            if session['total_issues_flagged'] > 0:
                html += f'<p style="margin-top: 10px;"><strong>{session["total_issues_flagged"]}</strong> items flagged for manual review - these require author judgment.</p>'

        html += '</div></div>'

        html += f"""
        <div class="footer">
            Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        </div>
    </div>
</body>
</html>
"""

        return html

    def _generate_text_recap(self, session):
        """Generate plain text format recap"""
        text = "=" * 70 + "\n"
        text += f"LINE EDITING SESSION - {session['date_readable']}\n"
        text += "=" * 70 + "\n\n"

        text += "SESSION SUMMARY\n"
        text += "-" * 70 + "\n"
        text += f"Chapters Edited:     {len(session['chapters_edited'])}\n"
        text += f"Total Issues Found:  {session['total_issues_found']}\n"
        text += f"Fixes Applied:       {session['total_fixes_applied']}\n"
        text += f"Flagged for Review:  {session['total_issues_flagged']}\n"
        text += f"Kept Original:       {session['total_skipped']}\n\n"

        text += "CHAPTERS EDITED\n"
        text += "-" * 70 + "\n\n"

        for chapter_data in session['chapters_edited']:
            status = "✨ CLEAN" if chapter_data['status'] == 'clean' else "✏️ CORRECTED"
            text += f"Chapter {chapter_data['chapter']} - {status}\n"

            if chapter_data['status'] != 'clean':
                text += f"  Issues found:      {chapter_data['issues_found']}\n"
                text += f"  Fixes applied:     {chapter_data['fixes_applied']}\n"
                text += f"  Flagged:           {chapter_data['flagged']}\n"
                text += f"  Skipped:           {chapter_data['skipped']}\n"

                if chapter_data.get('examples'):
                    text += "\n  Notable fixes:\n"
                    for example in chapter_data['examples']:
                        text += f"    - {example['description']}\n"
                        if 'before' in example and 'after' in example:
                            text += f"      Before: {example['before']}\n"
                            text += f"      After:  {example['after']}\n"

            text += "\n"

        return text

    def create_recap_for_chapter(self, chapter_num, issues_found=0, fixes_applied=0,
                                flagged=0, skipped=0, examples=None, notes=None):
        """Quick method to create a recap for a single chapter"""
        session = self.start_new_session()
        self.add_chapter_to_session(session, chapter_num, issues_found,
                                   fixes_applied, flagged, skipped, examples, notes)
        return session


def main():
    parser = argparse.ArgumentParser(
        description='Generate narrative recaps of line editing sessions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate recap for latest session
  %(prog)s --latest --format markdown

  # Create recap for specific chapter
  %(prog)s --chapter 5 --issues 3 --fixed 2 --flagged 1

  # View all sessions
  %(prog)s --list
        """
    )

    parser.add_argument('--latest', action='store_true',
                       help='Generate recap for latest session')
    parser.add_argument('--list', action='store_true',
                       help='List all sessions')
    parser.add_argument('--chapter', type=int,
                       help='Create recap for single chapter')
    parser.add_argument('--issues', type=int, default=0,
                       help='Number of issues found')
    parser.add_argument('--fixed', type=int, default=0,
                       help='Number of fixes applied')
    parser.add_argument('--flagged', type=int, default=0,
                       help='Number flagged for review')
    parser.add_argument('--skipped', type=int, default=0,
                       help='Number kept as-is')
    parser.add_argument('--format', choices=['markdown', 'html', 'text'],
                       default='markdown',
                       help='Output format (default: markdown)')
    parser.add_argument('--output', help='Output file path')

    args = parser.parse_args()

    generator = SessionRecapGenerator()

    if args.list:
        print(f"\n{len(generator.sessions)} editing sessions found:\n")
        for i, session in enumerate(generator.sessions, 1):
            print(f"{i}. {session['date_readable']}")
            print(f"   Chapters: {len(session['chapters_edited'])}, "
                  f"Issues: {session['total_issues_found']}, "
                  f"Fixed: {session['total_fixes_applied']}")
            print()

    elif args.chapter:
        # Create single chapter recap
        session = generator.create_recap_for_chapter(
            args.chapter, args.issues, args.fixed, args.flagged, args.skipped
        )

        recap = generator.generate_recap(session, args.format)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(recap)
            print(f"✓ Recap saved to: {args.output}")
        else:
            print(recap)

    elif args.latest and generator.sessions:
        # Generate recap for latest session
        session = generator.sessions[-1]
        recap = generator.generate_recap(session, args.format)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(recap)
            print(f"✓ Recap saved to: {args.output}")
        else:
            print(recap)

    else:
        print("No action specified. Use --help for usage information.")


if __name__ == '__main__':
    main()
