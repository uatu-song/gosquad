# Python Script Schema for Manuscript Analysis

## High-Level Architecture

```python
"""
Manuscript Analysis Tool
Reads full manuscript in chunks, performs craft analysis using Claude API
"""

import anthropic
import os
from pathlib import Path
from typing import List, Dict, Optional
import json
```

## Core Components

### 1. Document Chunking Strategy

```python
class ManuscriptChunker:
    """
    Handles splitting manuscript into analyzable chunks
    Preserves chapter boundaries and context
    """
    
    def __init__(self, file_path: str, chunk_size: int = 15000):
        self.file_path = Path(file_path)
        self.chunk_size = chunk_size  # Characters per chunk
        self.chapters = []
        
    def find_chapter_boundaries(self, text: str) -> List[Dict]:
        """
        Locate chapter markers (CHAPTER 1, CHAPTER 2, etc.)
        Returns list of {chapter_num, start_pos, end_pos, title}
        """
        import re
        pattern = r'^CHAPTER\s+(\d+)'
        matches = re.finditer(pattern, text, re.MULTILINE)
        
        boundaries = []
        for match in matches:
            boundaries.append({
                'chapter_num': int(match.group(1)),
                'start_pos': match.start(),
                'line_num': text[:match.start()].count('\n') + 1
            })
        return boundaries
    
    def chunk_by_chapters(self, text: str, chapters_per_chunk: int = 2) -> List[Dict]:
        """
        Group N chapters together for analysis
        Maintains narrative continuity
        """
        boundaries = self.find_chapter_boundaries(text)
        chunks = []
        
        for i in range(0, len(boundaries), chapters_per_chunk):
            batch = boundaries[i:i + chapters_per_chunk]
            start = batch[0]['start_pos']
            end = boundaries[i + chapters_per_chunk]['start_pos'] if i + chapters_per_chunk < len(boundaries) else len(text)
            
            chunks.append({
                'chapters': [b['chapter_num'] for b in batch],
                'text': text[start:end],
                'start_line': batch[0]['line_num'],
                'word_count': len(text[start:end].split())
            })
        
        return chunks
```

### 2. Analysis Prompt System

```python
class AnalysisPrompts:
    """
    Structured prompts for different analysis types
    """
    
    INITIAL_CONTEXT = """You are analyzing a manuscript in sections. This is a craft analysis focused on:
- Story structure and pacing
- Character voice consistency
- Dialogue quality
- Action choreography
- Thematic integration
- Prose mechanics (filter words, passive voice, clarity)
- Emotional beats and their setup
- Genre execution

Provide specific, actionable feedback with line references where possible."""

    CHAPTER_ANALYSIS = """Analyze chapters {chapter_range} for:

1. **Pacing & Structure**: Does the chapter advance plot/character? Are beats earned?
2. **Character Voice**: Is POV consistent? Dialogue distinct?
3. **Prose Craft**: Filter words, passive constructions, clarity issues
4. **Emotional Beats**: Do character moments feel earned or forced?
5. **Technical Issues**: Continuity errors, unclear action, pronoun confusion
6. **Standout Moments**: What works exceptionally well?

Be specific. Quote lines when identifying issues. Celebrate strengths."""

    CUMULATIVE_ANALYSIS = """Based on chapters {start}-{end}, assess:

1. **Arc Development**: Character growth trajectories
2. **Thematic Threads**: What patterns emerge?
3. **Setup/Payoff**: What's been planted? What's paying off?
4. **Tonal Consistency**: Voice and style maintenance
5. **Structural Issues**: Pacing problems, redundancy, gaps

Synthesize across chapters. Look for patterns."""

    FINAL_SYNTHESIS = """You've now read the complete manuscript (chapters {total}).

Provide:

1. **Overall Assessment**: Publishability, market positioning
2. **Strongest Elements**: What makes this work exceptional?
3. **Core Weaknesses**: Structural or recurring issues
4. **Standout Scenes**: The moments readers will remember
5. **Revision Priorities**: Top 5 issues to address
6. **Comparable Titles**: Market positioning
7. **The Hook**: One-sentence pitch

Be honest but constructive. Focus on craft, not taste."""
```

### 3. API Integration

```python
class ManuscriptAnalyzer:
    """
    Orchestrates analysis via Claude API
    """
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.conversation_history = []
        self.analysis_results = []
        
    def analyze_chunk(
        self, 
        chunk_text: str, 
        chapter_nums: List[int],
        context: Optional[str] = None
    ) -> str:
        """
        Analyze a single chunk with context from previous chunks
        """
        
        prompt = f"""
{AnalysisPrompts.INITIAL_CONTEXT}

{AnalysisPrompts.CHAPTER_ANALYSIS.format(
    chapter_range=f"{min(chapter_nums)}-{max(chapter_nums)}"
)}

{'PREVIOUS CONTEXT: ' + context if context else ''}

CHAPTERS TO ANALYZE:
{chunk_text}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=16000,
            temperature=0.3,  # Lower temp for consistent analysis
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        analysis = response.content[0].text
        
        # Store for context building
        self.analysis_results.append({
            'chapters': chapter_nums,
            'analysis': analysis
        })
        
        return analysis
    
    def build_context_summary(self, last_n: int = 2) -> str:
        """
        Summarize recent analyses for context
        """
        if not self.analysis_results:
            return ""
        
        recent = self.analysis_results[-last_n:]
        summaries = []
        
        for result in recent:
            prompt = f"""Summarize this analysis in 3-4 sentences, focusing on:
- Key character/plot developments
- Major craft issues identified
- Important setups for future chapters

ANALYSIS:
{result['analysis']}"""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            summaries.append(f"Chapters {result['chapters']}: {response.content[0].text}")
        
        return "\n\n".join(summaries)
    
    def cumulative_analysis(self, chapters_analyzed: List[int]) -> str:
        """
        Synthesize across multiple chunks
        """
        # Get all previous analyses
        all_analyses = "\n\n---\n\n".join([
            f"CHAPTERS {r['chapters']}: {r['analysis']}" 
            for r in self.analysis_results
        ])
        
        prompt = f"""
{AnalysisPrompts.CUMULATIVE_ANALYSIS.format(
    start=min(chapters_analyzed),
    end=max(chapters_analyzed)
)}

PREVIOUS ANALYSES:
{all_analyses}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def final_synthesis(self, total_chapters: int) -> str:
        """
        Final comprehensive assessment
        """
        # Summarize all analyses
        all_analyses = "\n\n---\n\n".join([
            f"CHAPTERS {r['chapters']}: {r['analysis']}" 
            for r in self.analysis_results
        ])
        
        prompt = f"""
{AnalysisPrompts.FINAL_SYNTHESIS.format(total=total_chapters)}

ALL CHAPTER ANALYSES:
{all_analyses}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=16000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
```

### 4. Main Execution Flow

```python
def analyze_manuscript(
    file_path: str,
    api_key: str,
    output_dir: str = "./analysis_output",
    chapters_per_chunk: int = 2
):
    """
    Main execution function
    """
    
    # Setup
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Read manuscript
    with open(file_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    print(f"📖 Loaded manuscript: {len(full_text)} characters")
    
    # Chunk by chapters
    chunker = ManuscriptChunker(file_path)
    chunks = chunker.chunk_by_chapters(full_text, chapters_per_chunk)
    
    print(f"📚 Split into {len(chunks)} chunks")
    
    # Initialize analyzer
    analyzer = ManuscriptAnalyzer(api_key)
    
    # Analyze each chunk
    for i, chunk in enumerate(chunks):
        print(f"\n🔍 Analyzing chapters {chunk['chapters']}...")
        
        # Build context from previous chunks
        context = analyzer.build_context_summary() if i > 0 else None
        
        # Analyze
        analysis = analyzer.analyze_chunk(
            chunk_text=chunk['text'],
            chapter_nums=chunk['chapters'],
            context=context
        )
        
        # Save individual analysis
        output_file = output_path / f"analysis_chapters_{min(chunk['chapters'])}-{max(chunk['chapters'])}.md"
        with open(output_file, 'w') as f:
            f.write(f"# Chapters {chunk['chapters']} Analysis\n\n")
            f.write(analysis)
        
        print(f"✅ Saved to {output_file}")
        
        # Periodic cumulative analysis (every 10 chapters)
        if (max(chunk['chapters']) % 10 == 0):
            print(f"\n📊 Running cumulative analysis through chapter {max(chunk['chapters'])}...")
            cumulative = analyzer.cumulative_analysis(
                list(range(1, max(chunk['chapters']) + 1))
            )
            
            cumulative_file = output_path / f"cumulative_analysis_ch1-{max(chunk['chapters'])}.md"
            with open(cumulative_file, 'w') as f:
                f.write(cumulative)
            
            print(f"✅ Saved cumulative analysis")
    
    # Final synthesis
    print(f"\n🎯 Running final synthesis...")
    all_chapters = [c for chunk in chunks for c in chunk['chapters']]
    final = analyzer.final_synthesis(max(all_chapters))
    
    final_file = output_path / "FINAL_ANALYSIS.md"
    with open(final_file, 'w') as f:
        f.write(f"# Complete Manuscript Analysis\n\n")
        f.write(final)
    
    print(f"✅ Complete! Final analysis saved to {final_file}")
    
    return analyzer.analysis_results


# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze manuscript craft")
    parser.add_argument("manuscript", help="Path to manuscript file")
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    parser.add_argument("--output", default="./analysis", help="Output directory")
    parser.add_argument("--chapters-per-chunk", type=int, default=2, help="Chapters to analyze together")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("API key required: --api-key or ANTHROPIC_API_KEY env var")
    
    analyze_manuscript(
        file_path=args.manuscript,
        api_key=api_key,
        output_dir=args.output,
        chapters_per_chunk=args.chapters_per_chunk
    )
```

## Usage

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run analysis
python manuscript_analyzer.py my_novel.txt --output ./analysis --chapters-per-chunk 2

# Output structure:
# ./analysis/
#   analysis_chapters_1-2.md
#   analysis_chapters_3-4.md
#   ...
#   cumulative_analysis_ch1-10.md
#   cumulative_analysis_ch1-20.md
#   FINAL_ANALYSIS.md
```

## Key Features

1. **Context Preservation**: Each chunk includes summary of previous analyses
2. **Incremental Processing**: Doesn't hold entire manuscript in memory
3. **Structured Output**: Organized by chapter ranges
4. **Cumulative Synthesis**: Periodic big-picture assessments
5. **Final Report**: Comprehensive publishability assessment

## Cost Estimation

- Input: ~5K tokens per chapter pair
- Output: ~4K tokens per analysis
- 30 chapters = 15 chunks × 9K tokens = ~135K tokens
- At Claude Sonnet 4 rates: ~$0.40 per full manuscript analysis

This mirrors our collaborative process—reading in digestible chunks, maintaining context, building to synthesis.