#!/usr/bin/env python3
"""
Book Analysis Suite - Master Script
Runs all book analysis modules and generates a comprehensive report.
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import time
import shutil
from typing import Dict, List, Any


class BookAnalysisSuite:
    def __init__(self, file_path: str, output_dir: str = 'analysis_output'):
        self.file_path = Path(file_path)
        self.output_dir = Path(output_dir)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.results = {}
        self.errors = []
        self.start_time = None
        
        self.analysis_modules = [
            {
                'name': 'Text Analysis',
                'script': 'book_text_analysis.py',
                'key': 'text',
                'description': 'Word frequency, readability scores, chapter statistics'
            },
            {
                'name': 'Character Analysis',
                'script': 'book_character_analysis.py',
                'key': 'character',
                'description': 'Character detection, interactions, dialogue patterns'
            },
            {
                'name': 'Writing Style',
                'script': 'book_writing_style_analysis.py',
                'key': 'style',
                'description': 'Voice analysis, clichés, sentence variety'
            },
            {
                'name': 'Structural Analysis',
                'script': 'book_structural_analysis.py',
                'key': 'structure',
                'description': 'Chapters, scenes, POV, plot arc, timeline'
            }
        ]
    
    def validate_input(self) -> bool:
        """Validate input file exists and is readable"""
        if not self.file_path.exists():
            print(f"❌ Error: File '{self.file_path}' not found")
            return False
        
        if not self.file_path.is_file():
            print(f"❌ Error: '{self.file_path}' is not a file")
            return False
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                sample = f.read(1000)
            return True
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False
    
    def check_dependencies(self) -> bool:
        """Check if all required analysis scripts exist"""
        missing_scripts = []
        script_dir = Path(__file__).parent
        
        for module in self.analysis_modules:
            script_path = script_dir / module['script']
            if not script_path.exists():
                missing_scripts.append(module['script'])
        
        if missing_scripts:
            print("❌ Missing analysis scripts:")
            for script in missing_scripts:
                print(f"   - {script}")
            return False
        
        return True
    
    def setup_output_directory(self):
        """Create output directory structure"""
        self.output_dir.mkdir(exist_ok=True)
        
        self.session_dir = self.output_dir / f'analysis_{self.timestamp}'
        self.session_dir.mkdir(exist_ok=True)
        
        subdirs = ['reports', 'visualizations', 'data']
        for subdir in subdirs:
            (self.session_dir / subdir).mkdir(exist_ok=True)
    
    def run_analysis_module(self, module: Dict) -> bool:
        """Run a single analysis module"""
        print(f"\n📊 Running {module['name']}...")
        print(f"   {module['description']}")
        
        try:
            script_path = Path(__file__).parent / module['script']
            
            result = subprocess.run(
                [sys.executable, str(script_path), str(self.file_path)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(f"   ✓ {module['name']} completed successfully")
                
                report_file = self.output_dir / f"{module['key']}_analysis_report.json"
                if report_file.exists():
                    with open(report_file, 'r') as f:
                        self.results[module['key']] = json.load(f)
                    
                    shutil.copy(report_file, self.session_dir / 'data' / report_file.name)
                
                # Look for chart files in the default analysis_output directory
                chart_patterns = [
                    f"{module['key']}_analysis_charts.png",
                    f"{module['key']}_analysis_*.png",
                    f"*{module['key']}*.png"
                ]
                
                for pattern in chart_patterns:
                    chart_files = list(self.output_dir.glob(pattern))
                    for chart in chart_files:
                        shutil.copy(chart, self.session_dir / 'visualizations' / chart.name)
                
                return True
            else:
                error_msg = f"Failed with error: {result.stderr[:200]}"
                print(f"   ❌ {module['name']} failed")
                self.errors.append({
                    'module': module['name'],
                    'error': error_msg
                })
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ⚠️  {module['name']} timed out")
            self.errors.append({
                'module': module['name'],
                'error': 'Analysis timed out after 5 minutes'
            })
            return False
        except Exception as e:
            print(f"   ❌ {module['name']} error: {str(e)}")
            self.errors.append({
                'module': module['name'],
                'error': str(e)
            })
            return False
    
    def generate_executive_summary(self) -> Dict:
        """Generate executive summary from all analyses"""
        summary = {
            'file': str(self.file_path.name),
            'analysis_date': datetime.now().isoformat(),
            'duration': time.time() - self.start_time if self.start_time else 0,
            'completed_analyses': list(self.results.keys()),
            'failed_analyses': [e['module'] for e in self.errors]
        }
        
        if 'text' in self.results:
            text_data = self.results['text']
            summary['book_statistics'] = {
                'total_words': text_data.get('basic_metrics', {}).get('total_words', 0),
                'unique_words': text_data.get('basic_metrics', {}).get('unique_words', 0),
                'chapters': text_data.get('basic_metrics', {}).get('total_chapters', 0),
                'avg_chapter_length': text_data.get('basic_metrics', {}).get('avg_chapter_length', 0),
                'readability': {
                    'flesch_reading_ease': text_data.get('readability_scores', {}).get('flesch_reading_ease', 0),
                    'grade_level': text_data.get('readability_scores', {}).get('flesch_kincaid_grade', 0)
                }
            }
        
        if 'character' in self.results:
            char_data = self.results['character']
            summary['characters'] = {
                'total_characters': char_data.get('total_characters', 0),
                'main_characters': len(char_data.get('character_profiles', {})),
                'total_dialogue_lines': char_data.get('dialogue_statistics', {}).get('total_lines', 0)
            }
            
            if char_data.get('character_profiles'):
                top_chars = list(char_data['character_profiles'].keys())[:5]
                summary['characters']['protagonists'] = top_chars
        
        if 'style' in self.results:
            style_data = self.results['style']
            summary['writing_style'] = {
                'voice': {
                    'passive_ratio': style_data.get('voice_analysis', {}).get('passive_ratio', 0),
                    'active_ratio': 1 - style_data.get('voice_analysis', {}).get('passive_ratio', 0)
                },
                'dialogue_ratio': style_data.get('dialogue_narrative', {}).get('dialogue_ratio', 0),
                'cliches_found': style_data.get('cliches', {}).get('count', 0),
                'sentence_variety': style_data.get('sentence_variety', {}).get('variety_score', 0)
            }
        
        if 'structure' in self.results:
            struct_data = self.results['structure']
            summary['structure'] = {
                'total_chapters': struct_data.get('structure', {}).get('total_chapters', 0),
                'total_scenes': struct_data.get('scenes', {}).get('total', 0),
                'potential_climax': struct_data.get('plot_arc', {}).get('potential_climax'),
                'structure_type': struct_data.get('structure', {}).get('patterns', {}).get('structure_type', 'unknown')
            }
        
        key_insights = self.generate_insights()
        summary['key_insights'] = key_insights
        
        return summary
    
    def generate_insights(self) -> List[str]:
        """Generate key insights from the analysis"""
        insights = []
        
        if 'text' in self.results:
            readability = self.results['text'].get('readability_scores', {})
            if readability.get('flesch_reading_ease', 0) < 30:
                insights.append("📚 Complex writing style suitable for academic/professional audience")
            elif readability.get('flesch_reading_ease', 0) > 70:
                insights.append("📖 Accessible writing style suitable for general audience")
        
        if 'character' in self.results:
            char_count = self.results['character'].get('total_characters', 0)
            if char_count > 20:
                insights.append(f"👥 Large cast of {char_count} characters - complex narrative")
            elif char_count < 5:
                insights.append(f"👤 Focused narrative with {char_count} main characters")
        
        if 'style' in self.results:
            passive_ratio = self.results['style'].get('voice_analysis', {}).get('passive_ratio', 0)
            if passive_ratio > 0.3:
                insights.append("⚠️ High passive voice usage (>30%) - consider more active voice")
            
            dialogue_ratio = self.results['style'].get('dialogue_narrative', {}).get('dialogue_ratio', 0)
            if dialogue_ratio > 0.4:
                insights.append("💬 Dialogue-heavy narrative (>40% dialogue)")
            elif dialogue_ratio < 0.1:
                insights.append("📝 Narrative-heavy with minimal dialogue (<10%)")
        
        if 'structure' in self.results:
            struct_type = self.results['structure'].get('structure', {}).get('patterns', {}).get('structure_type', '')
            if 'varied' in struct_type:
                insights.append("🎢 Varied chapter lengths create dynamic pacing")
            elif 'consistent' in struct_type:
                insights.append("📏 Consistent chapter structure provides steady pacing")
        
        return insights
    
    def generate_html_report(self):
        """Generate comprehensive HTML report"""
        summary = self.generate_executive_summary()
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Analysis Report - {self.file_path.name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .content {{
            padding: 40px;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .stat-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}
        .stat-card .label {{
            color: #666;
            font-size: 0.9em;
        }}
        .insights {{
            background: #e8f4f8;
            border-radius: 8px;
            padding: 25px;
            margin: 30px 0;
        }}
        .insights h2 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        .insights ul {{
            list-style: none;
        }}
        .insights li {{
            padding: 10px 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }}
        .insights li:last-child {{
            border-bottom: none;
        }}
        .section {{
            margin: 40px 0;
        }}
        .section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .chart-container {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        .chart-container h3 {{
            margin-top: 10px;
            color: #495057;
        }}
        .error-section {{
            background: #fee;
            border-left: 4px solid #e74c3c;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .error-section h3 {{
            color: #c0392b;
            margin-bottom: 10px;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
        .progress-bar {{
            background: #e9ecef;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin: 20px 0;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }}
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            .content {{
                padding: 20px;
            }}
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Book Analysis Report</h1>
            <p>{summary['file']}</p>
            <p style="font-size: 0.9em; margin-top: 10px; opacity: 0.8;">
                Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </p>
        </div>
        
        <div class="content">
            <div class="summary-grid">
"""
        
        if 'book_statistics' in summary:
            stats = summary['book_statistics']
            html_content += f"""
                <div class="stat-card">
                    <h3>Word Count</h3>
                    <div class="value">{stats['total_words']:,}</div>
                    <div class="label">Total Words</div>
                </div>
                <div class="stat-card">
                    <h3>Vocabulary</h3>
                    <div class="value">{stats['unique_words']:,}</div>
                    <div class="label">Unique Words</div>
                </div>
                <div class="stat-card">
                    <h3>Chapters</h3>
                    <div class="value">{stats['chapters']}</div>
                    <div class="label">Total Chapters</div>
                </div>
                <div class="stat-card">
                    <h3>Readability</h3>
                    <div class="value">{stats['readability']['grade_level']:.1f}</div>
                    <div class="label">Grade Level</div>
                </div>
"""
        
        if 'characters' in summary:
            chars = summary['characters']
            html_content += f"""
                <div class="stat-card">
                    <h3>Characters</h3>
                    <div class="value">{chars['total_characters']}</div>
                    <div class="label">Total Characters</div>
                </div>
                <div class="stat-card">
                    <h3>Dialogue</h3>
                    <div class="value">{chars['total_dialogue_lines']:,}</div>
                    <div class="label">Dialogue Lines</div>
                </div>
"""
        
        if 'writing_style' in summary:
            style = summary['writing_style']
            html_content += f"""
                <div class="stat-card">
                    <h3>Active Voice</h3>
                    <div class="value">{style['voice']['active_ratio']*100:.0f}%</div>
                    <div class="label">Active Sentences</div>
                </div>
                <div class="stat-card">
                    <h3>Dialogue Ratio</h3>
                    <div class="value">{style['dialogue_ratio']*100:.0f}%</div>
                    <div class="label">Of Total Text</div>
                </div>
"""
        
        html_content += """
            </div>
            
            <div class="insights">
                <h2>🔍 Key Insights</h2>
                <ul>
"""
        
        for insight in summary.get('key_insights', []):
            html_content += f"                    <li>{insight}</li>\n"
        
        html_content += """
                </ul>
            </div>
            
            <div class="section">
                <h2>📊 Analysis Progress</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {:.0f}%"></div>
                </div>
                <p>Completed {}/{} analyses in {:.1f} seconds</p>
            </div>
""".format(
            len(self.results) / len(self.analysis_modules) * 100,
            len(self.results),
            len(self.analysis_modules),
            summary.get('duration', 0)
        )
        
        viz_dir = self.session_dir / 'visualizations'
        if viz_dir.exists() and list(viz_dir.glob('*.png')):
            html_content += """
            <div class="section">
                <h2>📈 Visualizations</h2>
                <div class="chart-grid">
"""
            
            for chart_file in viz_dir.glob('*.png'):
                chart_name = chart_file.stem.replace('_', ' ').title()
                relative_path = f"visualizations/{chart_file.name}"
                html_content += f"""
                    <div class="chart-container">
                        <img src="{relative_path}" alt="{chart_name}">
                        <h3>{chart_name}</h3>
                    </div>
"""
            
            html_content += """
                </div>
            </div>
"""
        
        if self.errors:
            html_content += """
            <div class="error-section">
                <h3>⚠️ Analysis Errors</h3>
                <ul>
"""
            for error in self.errors:
                html_content += f"                    <li><strong>{error['module']}:</strong> {error['error'][:100]}...</li>\n"
            
            html_content += """
                </ul>
            </div>
"""
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>Book Analysis Suite v1.0 | Generated with Python</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Analysis session: {}_{}
            </p>
        </div>
    </div>
</body>
</html>
""".format(self.timestamp[:8], self.timestamp[9:])
        
        report_path = self.session_dir / 'reports' / 'analysis_report.html'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n📄 HTML report saved to: {report_path}")
        
        return report_path
    
    def generate_combined_json(self):
        """Generate combined JSON report"""
        summary = self.generate_executive_summary()
        
        combined = {
            'metadata': {
                'file': str(self.file_path),
                'file_size': self.file_path.stat().st_size,
                'analysis_date': datetime.now().isoformat(),
                'analysis_duration': summary.get('duration', 0),
                'version': '1.0'
            },
            'summary': summary,
            'detailed_results': self.results,
            'errors': self.errors
        }
        
        report_path = self.session_dir / 'reports' / 'combined_analysis.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=2, default=str)
        
        print(f"📊 Combined JSON report saved to: {report_path}")
        
        return report_path
    
    def run_suite(self, modules: List[str] = None):
        """Run the complete analysis suite"""
        print("\n" + "="*60)
        print("📚 BOOK ANALYSIS SUITE")
        print("="*60)
        print(f"\nAnalyzing: {self.file_path.name}")
        print(f"File size: {self.file_path.stat().st_size / 1024:.1f} KB")
        
        if not self.validate_input():
            return False
        
        if not self.check_dependencies():
            print("\n⚠️  Please ensure all analysis scripts are in the same directory")
            return False
        
        self.setup_output_directory()
        print(f"\nOutput directory: {self.session_dir}")
        
        modules_to_run = self.analysis_modules
        if modules:
            modules_to_run = [m for m in self.analysis_modules if m['key'] in modules]
        
        self.start_time = time.time()
        
        print(f"\nRunning {len(modules_to_run)} analysis modules...")
        print("-" * 40)
        
        success_count = 0
        for i, module in enumerate(modules_to_run, 1):
            print(f"\n[{i}/{len(modules_to_run)}]", end="")
            if self.run_analysis_module(module):
                success_count += 1
        
        elapsed_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("📊 ANALYSIS COMPLETE")
        print("="*60)
        print(f"\n✓ Successfully completed: {success_count}/{len(modules_to_run)} analyses")
        print(f"⏱️  Total time: {elapsed_time:.1f} seconds")
        
        if self.errors:
            print(f"\n⚠️  {len(self.errors)} analyses failed:")
            for error in self.errors:
                print(f"   - {error['module']}")
        
        print("\n📁 Generating reports...")
        
        json_report = self.generate_combined_json()
        html_report = self.generate_html_report()
        
        print("\n" + "="*60)
        print("✅ SUITE COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"\n📂 All results saved to: {self.session_dir}")
        print(f"📄 View HTML report: {html_report}")
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Book Analysis Suite - Comprehensive text analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available analysis modules:
  text       - Word frequency, readability, chapter statistics
  character  - Character detection, interactions, dialogue
  style      - Writing style, voice, clichés, variety
  structure  - Chapters, scenes, POV, plot arc, timeline

Examples:
  %(prog)s mybook.txt                    # Run all analyses
  %(prog)s mybook.txt --modules text character  # Run specific analyses
  %(prog)s mybook.txt --output results   # Custom output directory
        """
    )
    
    parser.add_argument('file', help='Path to the book text file')
    parser.add_argument('--modules', nargs='+', 
                       choices=['text', 'character', 'style', 'structure'],
                       help='Specific modules to run (default: all)')
    parser.add_argument('--output', default='analysis_output',
                       help='Output directory (default: analysis_output)')
    parser.add_argument('--quick', action='store_true',
                       help='Run only text and structure analysis for quick overview')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    modules = args.modules
    if args.quick:
        modules = ['text', 'structure']
        print("🚀 Running quick analysis (text and structure only)...")
    
    suite = BookAnalysisSuite(args.file, args.output)
    
    try:
        success = suite.run_suite(modules)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()