#!/usr/bin/env python3
"""
Diagnostic script for the book analysis suite
Tests each analyzer module for functionality and dependencies
"""

import sys
import importlib
import subprocess
from pathlib import Path
import json

def test_import(module_name):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        return True, "OK"
    except Exception as e:
        return False, str(e)

def test_python_script(script_name):
    """Test if a Python script can be run with --help"""
    try:
        result = subprocess.run([sys.executable, script_name, '--help'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "Script runs successfully"
        else:
            return False, f"Exit code: {result.returncode}, Error: {result.stderr[:200]}"
    except Exception as e:
        return False, str(e)

def test_analyzer_module(script_name, test_file):
    """Test if an analyzer can process a small test file"""
    try:
        # Create a small test file
        test_content = """Chapter 1: Test Chapter
        
This is a test paragraph with some text. The protagonist walked down the street.
"Hello," said John. "How are you today?"
"I'm fine," replied Mary. "Just testing the analyzer."

This is another paragraph to test the analysis capabilities."""
        
        test_path = Path("test_chapter.txt")
        test_path.write_text(test_content)
        
        # Run the analyzer
        result = subprocess.run([sys.executable, script_name, str(test_path)], 
                              capture_output=True, text=True, timeout=30)
        
        # Clean up
        test_path.unlink()
        
        if result.returncode == 0:
            return True, "Analyzer works correctly"
        else:
            return False, f"Error: {result.stderr[:200]}"
    except Exception as e:
        # Clean up if test file exists
        if Path("test_chapter.txt").exists():
            Path("test_chapter.txt").unlink()
        return False, str(e)

def main():
    print("=" * 60)
    print("BOOK ANALYSIS SUITE DIAGNOSTIC")
    print("=" * 60)
    
    # Test Python version
    print(f"\nPython version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Test required dependencies
    print("\n" + "-" * 40)
    print("TESTING DEPENDENCIES")
    print("-" * 40)
    
    dependencies = {
        'matplotlib': 'Plotting and visualization',
        'numpy': 'Numerical computations',
        'networkx': 'Character network analysis',
        're': 'Regular expressions (built-in)',
        'json': 'JSON handling (built-in)',
        'collections': 'Data structures (built-in)'
    }
    
    for module, description in dependencies.items():
        success, message = test_import(module)
        status = "✓" if success else "✗"
        print(f"{status} {module:<15} - {description:<30} [{message}]")
    
    # Test analyzer scripts
    print("\n" + "-" * 40)
    print("TESTING ANALYZER SCRIPTS")
    print("-" * 40)
    
    analyzers = [
        ('book_text_analysis.py', 'Text metrics and readability'),
        ('book_character_analysis.py', 'Character detection and analysis'),
        ('book_writing_style_analysis.py', 'Writing style metrics'),
        ('book_structural_analysis.py', 'Structure and plot analysis'),
        ('book_analysis_suite.py', 'Master analysis suite'),
        ('chapter_analyzer.py', 'Basic chapter analyzer'),
        ('analyze_all_chapters.py', 'Batch chapter analyzer')
    ]
    
    for script, description in analyzers:
        if Path(script).exists():
            success, message = test_python_script(script)
            status = "✓" if success else "✗"
            print(f"{status} {script:<30} - {description}")
            if not success:
                print(f"  └─ {message}")
        else:
            print(f"✗ {script:<30} - File not found")
    
    # Test analyzer functionality with sample text
    print("\n" + "-" * 40)
    print("TESTING ANALYZER FUNCTIONALITY")
    print("-" * 40)
    
    test_analyzers = [
        'book_text_analysis.py',
        'book_structural_analysis.py'
    ]
    
    for analyzer in test_analyzers:
        if Path(analyzer).exists():
            print(f"\nTesting {analyzer} with sample text...")
            success, message = test_analyzer_module(analyzer, "test_chapter.txt")
            status = "✓" if success else "✗"
            print(f"{status} {analyzer}: {message}")
    
    # Check for existing analysis results
    print("\n" + "-" * 40)
    print("EXISTING ANALYSIS RESULTS")
    print("-" * 40)
    
    output_dir = Path("analysis_output")
    if output_dir.exists():
        analyses = sorted(output_dir.glob("analysis_*"))
        print(f"Found {len(analyses)} analysis sessions")
        if analyses:
            # Show last 5
            for analysis in analyses[-5:]:
                print(f"  - {analysis.name}")
    else:
        print("No analysis output directory found")
    
    # Check chapter files
    print("\n" + "-" * 40)
    print("CHAPTER FILES")
    print("-" * 40)
    
    chapters_dir = Path("chapters")
    if chapters_dir.exists():
        md_files = list(chapters_dir.glob("*.md"))
        txt_files = list(chapters_dir.glob("*.txt"))
        print(f"Found {len(md_files)} .md files and {len(txt_files)} .txt files")
    else:
        print("Chapters directory not found")
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()