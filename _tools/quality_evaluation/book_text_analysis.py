#!/usr/bin/env python3
"""
Book Text Analysis Script
Analyzes various text metrics including word frequency, readability scores,
sentence/paragraph statistics, and chapter-level analysis.
"""

import re
import sys
import json
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


class BookTextAnalyzer:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.text = ""
        self.chapters = []
        self.sentences = []
        self.paragraphs = []
        self.words = []
        
    def load_text(self):
        """Load text from file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.text = f.read()
            print(f"✓ Loaded {len(self.text):,} characters from {self.file_path.name}")
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)
    
    def detect_chapters(self):
        """Detect chapters based on common patterns"""
        chapter_patterns = [
            r'Chapter\s+\d+',
            r'Chapter\s+[IVXLCDM]+',
            r'CHAPTER\s+\d+',
            r'CHAPTER\s+[IVXLCDM]+',
            r'^\d+\.\s',
            r'^Part\s+\d+',
            r'^PART\s+\d+'
        ]
        
        combined_pattern = '|'.join(f'({p})' for p in chapter_patterns)
        
        chapter_splits = re.split(f'({combined_pattern})', self.text, flags=re.MULTILINE)
        
        if len(chapter_splits) > 1:
            current_chapter = []
            for i, part in enumerate(chapter_splits):
                if part and re.match(combined_pattern, part, re.MULTILINE):
                    if current_chapter:
                        self.chapters.append(''.join(current_chapter))
                    current_chapter = [part]
                elif part:
                    current_chapter.append(part)
            if current_chapter:
                self.chapters.append(''.join(current_chapter))
        else:
            chunk_size = len(self.text) // 10
            self.chapters = [self.text[i:i+chunk_size] for i in range(0, len(self.text), chunk_size)]
        
        print(f"✓ Detected {len(self.chapters)} chapters/sections")
    
    def extract_sentences(self):
        """Extract sentences from text"""
        sentence_pattern = r'[.!?]+[\s]+'
        raw_sentences = re.split(sentence_pattern, self.text)
        self.sentences = [s.strip() for s in raw_sentences if s.strip() and len(s.strip()) > 10]
        print(f"✓ Extracted {len(self.sentences):,} sentences")
    
    def extract_paragraphs(self):
        """Extract paragraphs from text"""
        self.paragraphs = [p.strip() for p in self.text.split('\n\n') if p.strip()]
        print(f"✓ Extracted {len(self.paragraphs):,} paragraphs")
    
    def extract_words(self):
        """Extract and clean words from text"""
        word_pattern = r'\b[a-zA-Z]+\b'
        self.words = re.findall(word_pattern, self.text.lower())
        print(f"✓ Extracted {len(self.words):,} words")
    
    def calculate_basic_metrics(self):
        """Calculate basic text metrics"""
        metrics = {
            'total_words': len(self.words),
            'unique_words': len(set(self.words)),
            'total_sentences': len(self.sentences),
            'total_paragraphs': len(self.paragraphs),
            'total_chapters': len(self.chapters),
            'avg_word_length': np.mean([len(w) for w in self.words]),
            'lexical_diversity': len(set(self.words)) / len(self.words) if self.words else 0
        }
        
        if self.sentences:
            words_per_sentence = [len(re.findall(r'\b[a-zA-Z]+\b', s)) for s in self.sentences]
            metrics['avg_sentence_length'] = np.mean(words_per_sentence)
            metrics['min_sentence_length'] = min(words_per_sentence)
            metrics['max_sentence_length'] = max(words_per_sentence)
            metrics['sentence_length_std'] = np.std(words_per_sentence)
        
        if self.paragraphs:
            words_per_paragraph = [len(re.findall(r'\b[a-zA-Z]+\b', p)) for p in self.paragraphs]
            sentences_per_paragraph = [len(re.split(r'[.!?]+', p)) - 1 for p in self.paragraphs]
            metrics['avg_paragraph_length'] = np.mean(words_per_paragraph)
            metrics['avg_sentences_per_paragraph'] = np.mean(sentences_per_paragraph)
        
        return metrics
    
    def calculate_readability_scores(self):
        """Calculate various readability scores"""
        scores = {}
        
        syllable_count = sum(self._count_syllables(word) for word in self.words)
        word_count = len(self.words)
        sentence_count = len(self.sentences)
        
        if word_count > 0 and sentence_count > 0:
            avg_syllables_per_word = syllable_count / word_count
            avg_words_per_sentence = word_count / sentence_count
            
            scores['flesch_reading_ease'] = (
                206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word
            )
            
            scores['flesch_kincaid_grade'] = (
                0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59
            )
            
            complex_words = sum(1 for w in self.words if self._count_syllables(w) >= 3)
            percent_complex = (complex_words / word_count) * 100 if word_count > 0 else 0
            scores['gunning_fog'] = 0.4 * (avg_words_per_sentence + percent_complex)
            
            scores['automated_readability_index'] = (
                4.71 * (len(self.text.replace(' ', '')) / word_count) + 
                0.5 * avg_words_per_sentence - 21.43
            )
            
            if avg_syllables_per_word > 0 and avg_words_per_sentence > 0:
                scores['coleman_liau'] = (
                    0.0588 * (len(self.text.replace(' ', '')) / word_count * 100) -
                    0.296 * (sentence_count / word_count * 100) - 15.8
                )
            
            scores['smog'] = (
                1.0430 * np.sqrt(complex_words * (30 / sentence_count)) + 3.1291
                if sentence_count >= 30 else None
            )
        
        return scores
    
    def _count_syllables(self, word):
        """Count syllables in a word (approximate)"""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        if word.endswith('e'):
            syllable_count -= 1
        if word.endswith('le') and len(word) > 2:
            syllable_count += 1
        if syllable_count == 0:
            syllable_count = 1
            
        return syllable_count
    
    def analyze_word_frequency(self, top_n=50):
        """Analyze word frequency"""
        word_freq = Counter(self.words)
        
        common_words = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                           'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
                           'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
                           'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one',
                           'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
                           'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when'])
        
        content_words = {word: freq for word, freq in word_freq.items() 
                        if word not in common_words and len(word) > 2}
        
        return {
            'most_common_all': word_freq.most_common(top_n),
            'most_common_content': Counter(content_words).most_common(top_n),
            'hapax_legomena': [word for word, freq in word_freq.items() if freq == 1][:100]
        }
    
    def analyze_chapters(self):
        """Analyze chapter-level statistics"""
        chapter_stats = []
        
        for i, chapter in enumerate(self.chapters, 1):
            words = re.findall(r'\b[a-zA-Z]+\b', chapter.lower())
            sentences = [s for s in re.split(r'[.!?]+', chapter) if s.strip()]
            paragraphs = [p for p in chapter.split('\n\n') if p.strip()]
            
            stats = {
                'chapter': i,
                'word_count': len(words),
                'sentence_count': len(sentences),
                'paragraph_count': len(paragraphs),
                'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
                'unique_words': len(set(words)),
                'lexical_diversity': len(set(words)) / len(words) if words else 0
            }
            chapter_stats.append(stats)
        
        return chapter_stats
    
    def create_visualizations(self, output_dir='analysis_output'):
        """Create visualization charts"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'Text Analysis: {self.file_path.name}', fontsize=16)
        
        chapter_stats = self.analyze_chapters()
        chapters = [s['chapter'] for s in chapter_stats]
        word_counts = [s['word_count'] for s in chapter_stats]
        
        axes[0, 0].bar(chapters, word_counts, color='steelblue')
        axes[0, 0].set_xlabel('Chapter')
        axes[0, 0].set_ylabel('Word Count')
        axes[0, 0].set_title('Words per Chapter')
        
        sentence_lengths = [len(re.findall(r'\b[a-zA-Z]+\b', s)) for s in self.sentences[:1000]]
        axes[0, 1].hist(sentence_lengths, bins=30, color='forestgreen', edgecolor='black')
        axes[0, 1].set_xlabel('Words per Sentence')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Sentence Length Distribution')
        
        word_lengths = [len(w) for w in self.words[:10000]]
        axes[0, 2].hist(word_lengths, bins=15, color='coral', edgecolor='black')
        axes[0, 2].set_xlabel('Word Length')
        axes[0, 2].set_ylabel('Frequency')
        axes[0, 2].set_title('Word Length Distribution')
        
        word_freq = Counter(self.words)
        top_words = word_freq.most_common(15)
        words, freqs = zip(*top_words)
        axes[1, 0].barh(words, freqs, color='purple')
        axes[1, 0].set_xlabel('Frequency')
        axes[1, 0].set_title('Top 15 Most Common Words')
        
        diversity = [s['lexical_diversity'] for s in chapter_stats]
        axes[1, 1].plot(chapters, diversity, marker='o', color='darkred')
        axes[1, 1].set_xlabel('Chapter')
        axes[1, 1].set_ylabel('Lexical Diversity')
        axes[1, 1].set_title('Vocabulary Diversity by Chapter')
        
        avg_sent_lengths = [s['avg_sentence_length'] for s in chapter_stats]
        axes[1, 2].plot(chapters, avg_sent_lengths, marker='s', color='navy')
        axes[1, 2].set_xlabel('Chapter')
        axes[1, 2].set_ylabel('Avg Words per Sentence')
        axes[1, 2].set_title('Sentence Complexity by Chapter')
        
        plt.tight_layout()
        plt.savefig(output_path / 'text_analysis_charts.png', dpi=150, bbox_inches='tight')
        print(f"✓ Saved visualizations to {output_path / 'text_analysis_charts.png'}")
        
        plt.close()
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*60)
        print("TEXT ANALYSIS REPORT")
        print("="*60)
        
        self.load_text()
        self.extract_words()
        self.extract_sentences()
        self.extract_paragraphs()
        self.detect_chapters()
        
        print("\n📊 BASIC METRICS")
        print("-"*40)
        metrics = self.calculate_basic_metrics()
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value:,}")
        
        print("\n📖 READABILITY SCORES")
        print("-"*40)
        scores = self.calculate_readability_scores()
        for score_name, value in scores.items():
            if value is not None:
                grade_equiv = ""
                if 'flesch_reading_ease' in score_name:
                    if value >= 90: grade_equiv = " (5th grade)"
                    elif value >= 80: grade_equiv = " (6th grade)"
                    elif value >= 70: grade_equiv = " (7th grade)"
                    elif value >= 60: grade_equiv = " (8-9th grade)"
                    elif value >= 50: grade_equiv = " (10-12th grade)"
                    elif value >= 30: grade_equiv = " (College)"
                    else: grade_equiv = " (Graduate)"
                print(f"  {score_name.replace('_', ' ').title()}: {value:.2f}{grade_equiv}")
        
        print("\n🔤 WORD FREQUENCY ANALYSIS")
        print("-"*40)
        freq_analysis = self.analyze_word_frequency(top_n=20)
        print("  Top 10 Content Words:")
        for word, freq in freq_analysis['most_common_content'][:10]:
            print(f"    • {word}: {freq:,}")
        print(f"\n  Unique words used only once: {len(freq_analysis['hapax_legomena']):,}")
        
        print("\n📚 CHAPTER ANALYSIS")
        print("-"*40)
        chapter_stats = self.analyze_chapters()
        avg_chapter_length = np.mean([s['word_count'] for s in chapter_stats])
        shortest = min(chapter_stats, key=lambda x: x['word_count'])
        longest = max(chapter_stats, key=lambda x: x['word_count'])
        
        print(f"  Average chapter length: {avg_chapter_length:,.0f} words")
        print(f"  Shortest chapter: #{shortest['chapter']} ({shortest['word_count']:,} words)")
        print(f"  Longest chapter: #{longest['chapter']} ({longest['word_count']:,} words)")
        
        pacing_variance = np.std([s['word_count'] for s in chapter_stats])
        print(f"  Pacing variance (std dev): {pacing_variance:,.0f} words")
        
        self.create_visualizations()
        
        output_path = Path('analysis_output')
        output_path.mkdir(exist_ok=True)
        
        full_report = {
            'file': str(self.file_path),
            'basic_metrics': metrics,
            'readability_scores': scores,
            'word_frequency': {
                'top_20_all': freq_analysis['most_common_all'],
                'top_20_content': freq_analysis['most_common_content'],
                'unique_single_use': len(freq_analysis['hapax_legomena'])
            },
            'chapter_statistics': chapter_stats
        }
        
        with open(output_path / 'text_analysis_report.json', 'w') as f:
            json.dump(full_report, f, indent=2)
        
        print(f"\n✓ Full report saved to {output_path / 'text_analysis_report.json'}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Analyze text metrics of a book')
    parser.add_argument('file', help='Path to the book text file')
    parser.add_argument('--format', choices=['txt', 'md'], default='txt',
                       help='Input file format (default: txt)')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    analyzer = BookTextAnalyzer(args.file)
    analyzer.generate_report()


if __name__ == '__main__':
    main()