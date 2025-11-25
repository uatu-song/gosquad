#!/usr/bin/env python3
"""
Run analysis suite on all chapter files in the chapters directory.
"""

import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime
import time


def get_chapter_files(chapters_dir):
    """Get all chapter markdown and text files"""
    chapters_dir = Path(chapters_dir)
    
    # Get all .md and .txt files, excluding analysis scripts
    chapter_files = []
    
    # Add all markdown chapters
    for file in sorted(chapters_dir.glob('*.md')):
        if not file.name.startswith('.'):
            chapter_files.append(file)
    
    # Add prologue.txt
    prologue = chapters_dir / 'prologue.txt'
    if prologue.exists():
        chapter_files.insert(0, prologue)  # Put prologue first
    
    return chapter_files


def run_analysis_on_chapter(chapter_file, output_base):
    """Run the analysis suite on a single chapter"""
    chapter_name = chapter_file.stem.replace('_', ' ').title()
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {chapter_name}")
    print(f"File: {chapter_file.name}")
    print('='*60)
    
    # Create output directory for this chapter
    safe_name = chapter_file.stem
    output_dir = Path(output_base) / safe_name
    
    try:
        # Run the analysis suite with quick mode for efficiency
        result = subprocess.run(
            [sys.executable, 'book_analysis_suite.py', str(chapter_file), 
             '--output', str(output_dir), '--quick'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"✓ Analysis complete for {chapter_name}")
            return {
                'name': chapter_name,
                'file': chapter_file.name,
                'success': True,
                'output_dir': str(output_dir)
            }
        else:
            print(f"✗ Analysis failed for {chapter_name}")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            return {
                'name': chapter_name,
                'file': chapter_file.name,
                'success': False,
                'error': result.stderr[:500] if result.stderr else 'Unknown error'
            }
            
    except subprocess.TimeoutExpired:
        print(f"⚠ Analysis timed out for {chapter_name}")
        return {
            'name': chapter_name,
            'file': chapter_file.name,
            'success': False,
            'error': 'Analysis timed out after 60 seconds'
        }
    except Exception as e:
        print(f"✗ Error analyzing {chapter_name}: {str(e)}")
        return {
            'name': chapter_name,
            'file': chapter_file.name,
            'success': False,
            'error': str(e)
        }


def generate_summary_report(results, output_base):
    """Generate a summary report of all chapter analyses"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    # Create summary report
    summary = {
        'timestamp': timestamp,
        'total_chapters': len(results),
        'successful': len(successful),
        'failed': len(failed),
        'chapters': results
    }
    
    # Save JSON report
    json_path = Path(output_base) / 'all_chapters_summary.json'
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 JSON summary saved to: {json_path}")
    
    # Generate HTML summary
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Complete Chapter Analysis - Remanence</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #333; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        .chapters-list {{
            padding: 30px;
        }}
        .chapter-item {{
            background: white;
            margin: 15px 0;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.2s;
        }}
        .chapter-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .chapter-success {{
            border-left: 4px solid #4caf50;
        }}
        .chapter-failed {{
            border-left: 4px solid #f44336;
        }}
        .chapter-name {{
            font-weight: 600;
            color: #333;
        }}
        .chapter-status {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .status-icon {{
            font-size: 1.2em;
        }}
        .view-link {{
            color: #667eea;
            text-decoration: none;
            padding: 5px 15px;
            border: 1px solid #667eea;
            border-radius: 5px;
            transition: all 0.3s;
        }}
        .view-link:hover {{
            background: #667eea;
            color: white;
        }}
        .success-rate {{
            padding: 20px;
            text-align: center;
            background: #f8f9fa;
        }}
        .progress-bar {{
            background: #e9ecef;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin: 20px auto;
            max-width: 600px;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #4caf50, #8bc34a);
            height: 100%;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Remanence - Complete Chapter Analysis</h1>
            <p>Generated: {timestamp}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{len(results)}</div>
                <div class="stat-label">Total Chapters</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #4caf50">{len(successful)}</div>
                <div class="stat-label">Successfully Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #f44336">{len(failed)}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(successful)/len(results)*100:.0f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
        
        <div class="success-rate">
            <h2>Analysis Progress</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {len(successful)/len(results)*100}%">
                    {len(successful)}/{len(results)} Completed
                </div>
            </div>
        </div>
        
        <div class="chapters-list">
            <h2 style="margin-bottom: 20px;">Chapter Analysis Results</h2>
"""
    
    for result in results:
        status_class = 'chapter-success' if result['success'] else 'chapter-failed'
        status_icon = '✅' if result['success'] else '❌'
        
        html_content += f"""
            <div class="chapter-item {status_class}">
                <div>
                    <div class="chapter-name">{result['name']}</div>
                    <div style="color: #666; font-size: 0.9em; margin-top: 5px;">{result['file']}</div>
                </div>
                <div class="chapter-status">
                    <span class="status-icon">{status_icon}</span>
"""
        
        if result['success']:
            # Find the most recent analysis session
            output_dir = Path(result['output_dir'])
            if output_dir.exists():
                sessions = sorted([d for d in output_dir.iterdir() if d.is_dir()])
                if sessions:
                    latest_session = sessions[-1]
                    report_path = latest_session / 'reports' / 'analysis_report.html'
                    if report_path.exists():
                        relative_path = report_path.relative_to(Path(output_base).parent)
                        html_content += f"""
                    <a href="{relative_path}" class="view-link">View Analysis</a>
"""
        else:
            html_content += f"""
                    <span style="color: #f44336; font-size: 0.9em;">Failed</span>
"""
        
        html_content += """
                </div>
            </div>
"""
    
    html_content += """
        </div>
    </div>
</body>
</html>
"""
    
    html_path = Path(output_base) / 'all_chapters_index.html'
    with open(html_path, 'w') as f:
        f.write(html_content)
    
    print(f"📄 HTML index saved to: {html_path}")
    
    return json_path, html_path


def main():
    chapters_dir = Path('/home/josephsong15/editor/chapters')
    
    if not chapters_dir.exists():
        print(f"Error: Directory '{chapters_dir}' not found")
        sys.exit(1)
    
    print(f"\n📚 REMANENCE - CHAPTER-BY-CHAPTER ANALYSIS")
    print("="*60)
    print(f"Chapters directory: {chapters_dir}")
    
    # Get all chapter files
    chapter_files = get_chapter_files(chapters_dir)
    print(f"Found {len(chapter_files)} chapter files to analyze")
    
    if not chapter_files:
        print("No chapter files found!")
        sys.exit(1)
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_base = Path('chapter_analysis_output') / f'full_analysis_{timestamp}'
    output_base.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_base}")
    
    # Analyze each chapter
    print(f"\n🔬 Starting analysis of {len(chapter_files)} chapters...")
    print("(Using quick mode for efficiency)")
    
    start_time = time.time()
    results = []
    
    for i, chapter_file in enumerate(chapter_files, 1):
        print(f"\n[{i}/{len(chapter_files)}]", end="")
        result = run_analysis_on_chapter(chapter_file, output_base)
        results.append(result)
    
    elapsed_time = time.time() - start_time
    
    # Generate summary reports
    print("\n" + "="*60)
    print("📊 GENERATING SUMMARY REPORTS")
    print("="*60)
    
    json_report, html_report = generate_summary_report(results, output_base)
    
    # Final summary
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE")
    print("="*60)
    print(f"Total chapters analyzed: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Success rate: {len(successful)/len(results)*100:.1f}%")
    print(f"Total time: {elapsed_time:.1f} seconds")
    print(f"\n📂 All results saved to: {output_base}")
    print(f"📄 View summary at: {html_report}")
    
    if failed:
        print(f"\n⚠️ Failed chapters:")
        for result in failed:
            print(f"  • {result['name']}: {result.get('error', 'Unknown error')[:50]}")


if __name__ == '__main__':
    main()