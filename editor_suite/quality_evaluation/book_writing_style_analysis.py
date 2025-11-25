#!/usr/bin/env python3
"""
Book Writing Style Analysis Script
Analyzes writing style including voice (active/passive), word choice,
dialogue patterns, clichés, and various stylistic metrics.
"""

import re
import sys
import json
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


class WritingStyleAnalyzer:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.text = ""
        self.sentences = []
        self.paragraphs = []
        self.chapters = []
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
    
    def extract_components(self):
        """Extract sentences, paragraphs, chapters, and words"""
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        self.sentences = [s.strip() for s in re.split(sentence_pattern, self.text) 
                         if s.strip() and len(s.strip()) > 10]
        
        self.paragraphs = [p.strip() for p in self.text.split('\n\n') if p.strip()]
        
        chapter_patterns = [
            r'Chapter\s+\d+',
            r'Chapter\s+[IVXLCDM]+',
            r'CHAPTER\s+\d+',
            r'CHAPTER\s+[IVXLCDM]+',
        ]
        combined_pattern = '|'.join(f'({p})' for p in chapter_patterns)
        chapter_splits = re.split(f'({combined_pattern})', self.text, flags=re.MULTILINE)
        
        if len(chapter_splits) > 3:
            current_chapter = []
            for part in chapter_splits:
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
        
        word_pattern = r'\b[a-zA-Z]+\b'
        self.words = re.findall(word_pattern, self.text.lower())
        
        print(f"✓ Extracted {len(self.sentences):,} sentences, {len(self.paragraphs):,} paragraphs")
        print(f"✓ Detected {len(self.chapters)} chapters, {len(self.words):,} words")
    
    def analyze_voice(self):
        """Analyze active vs passive voice usage"""
        passive_indicators = [
            r'\b(was|were|been|being|is|are|am)\s+\w+ed\b',
            r'\b(was|were|been|being|is|are|am)\s+\w+en\b',
            r'\b(get|gets|got|gotten|getting)\s+\w+ed\b',
            r'\bby\s+(?:the|a|an)\s+\w+',
        ]
        
        active_count = 0
        passive_count = 0
        passive_examples = []
        
        for sentence in self.sentences:
            is_passive = False
            for pattern in passive_indicators:
                if re.search(pattern, sentence, re.IGNORECASE):
                    is_passive = True
                    if len(passive_examples) < 10:
                        passive_examples.append(sentence[:100] + '...' if len(sentence) > 100 else sentence)
                    break
            
            if is_passive:
                passive_count += 1
            else:
                active_count += 1
        
        return {
            'active_count': active_count,
            'passive_count': passive_count,
            'passive_ratio': passive_count / (active_count + passive_count) if (active_count + passive_count) > 0 else 0,
            'passive_examples': passive_examples[:5]
        }
    
    def analyze_word_types(self):
        """Analyze adverbs, adjectives, and other word types"""
        adverb_pattern = r'\b\w+ly\b'
        adjective_indicators = ['very', 'really', 'quite', 'rather', 'extremely', 'fairly', 'pretty']
        
        # Words ending in 'ly' that are NOT adverbs
        not_adverbs = {'family', 'anomaly', 'italy', 'lily', 'ally', 'bully', 'chilly', 
                      'daily', 'early', 'elderly', 'friendly', 'holy', 'jolly', 'lonely',
                      'lovely', 'multiply', 'rely', 'reply', 'supply', 'ugly', 'weekly',
                      'yearly', 'assembly', 'belly', 'billy', 'bodily', 'brotherly', 
                      'costly', 'deadly', 'fatherly', 'fly', 'folly', 'godly', 'hilly',
                      'homely', 'jelly', 'july', 'kindly', 'likely', 'lively', 'manly',
                      'melancholy', 'monthly', 'motherly', 'oily', 'only', 'orderly',
                      'panoply', 'pearly', 'poly', 'rally', 'sally', 'scholarly', 'silly',
                      'sly', 'smelly', 'sparkly', 'steely', 'surly', 'tally', 'timely',
                      'ugly', 'unlikely', 'woolly', 'worldly', 'monopoly', 'apply'}
        
        potential_adverbs = re.findall(adverb_pattern, self.text.lower())
        
        # Filter out non-adverbs
        adverbs = [word for word in potential_adverbs if word not in not_adverbs]
        
        adverb_counts = Counter(adverbs)
        common_adverbs = ['really', 'probably', 'actually', 'finally', 
                         'usually', 'simply', 'certainly', 'clearly']
        overused_adverbs = [word for word, count in adverb_counts.items() 
                           if word not in common_adverbs and count > 5]
        
        adjective_count = 0
        for sentence in self.sentences:
            words = sentence.lower().split()
            for i, word in enumerate(words):
                if word in adjective_indicators:
                    adjective_count += 1
                if i > 0 and words[i-1] in ['very', 'really', 'quite', 'rather', 'extremely']:
                    adjective_count += 1
        
        strong_verbs = ['sprint', 'dash', 'leap', 'plunge', 'soar', 'crash', 'shatter',
                       'whisper', 'roar', 'glide', 'stumble', 'creep', 'burst']
        weak_verbs = ['go', 'went', 'get', 'got', 'make', 'made', 'do', 'did', 'have', 'had']
        
        strong_verb_count = sum(1 for word in self.words if word in strong_verbs)
        weak_verb_count = sum(1 for word in self.words if word in weak_verbs)
        
        return {
            'adverb_count': len(adverbs),
            'adverb_density': len(adverbs) / len(self.words) if self.words else 0,
            'top_adverbs': adverb_counts.most_common(10),
            'overused_adverbs': overused_adverbs[:10],
            'adjective_density': adjective_count / len(self.words) if self.words else 0,
            'strong_verb_ratio': strong_verb_count / (strong_verb_count + weak_verb_count) if (strong_verb_count + weak_verb_count) > 0 else 0
        }
    
    def detect_cliches(self):
        """Detect clichés and overused phrases"""
        cliches = [
            'at the end of the day', 'back to square one', 'beat around the bush',
            'better late than never', 'bite the bullet', 'break the ice',
            'burning the midnight oil', 'caught red-handed', 'crystal clear',
            'dead as a doornail', 'easier said than done', 'face the music',
            'fit as a fiddle', 'hit the nail on the head', 'in the nick of time',
            'kill two birds', 'last but not least', 'leave no stone unturned',
            'let the cat out', 'piece of cake', 'raining cats and dogs',
            'the tip of the iceberg', 'time flies', 'under the weather',
            'when pigs fly', 'worth its weight in gold', 'a dime a dozen',
            'actions speak louder', 'all ears', 'barking up the wrong tree',
            'beat a dead horse', 'bend over backwards', 'between a rock and a hard place',
            'bite off more than', 'blessing in disguise', 'break a leg',
            'butterflies in my stomach', 'can\'t judge a book', 'costs an arm and a leg',
            'cry over spilled milk', 'curiosity killed the cat', 'devil\'s advocate',
            'don\'t count your chickens', 'don\'t put all your eggs', 'every cloud has',
            'give the benefit of the doubt', 'go the extra mile', 'hit the ground running'
        ]
        
        found_cliches = defaultdict(int)
        cliche_examples = defaultdict(list)
        
        text_lower = self.text.lower()
        for cliche in cliches:
            pattern = re.escape(cliche)
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                found_cliches[cliche] += 1
                if len(cliche_examples[cliche]) < 2:
                    start = max(0, match.start() - 50)
                    end = min(len(self.text), match.end() + 50)
                    context = self.text[start:end].strip()
                    cliche_examples[cliche].append(context)
        
        phrase_pattern = r'\b(\w+\s+\w+\s+\w+)\b'
        three_word_phrases = re.findall(phrase_pattern, text_lower)
        phrase_counts = Counter(three_word_phrases)
        
        overused_phrases = [(phrase, count) for phrase, count in phrase_counts.items() 
                           if count > 10 and not any(word in ['the', 'and', 'but', 'for', 'with'] 
                                                     for word in phrase.split())]
        
        return {
            'cliches_found': dict(found_cliches),
            'cliche_count': sum(found_cliches.values()),
            'cliche_examples': dict(cliche_examples),
            'overused_phrases': sorted(overused_phrases, key=lambda x: x[1], reverse=True)[:15]
        }
    
    def analyze_dialogue_narrative_ratio(self):
        """Analyze the ratio of dialogue to narrative text"""
        dialogue_pattern = r'"[^"]+"|\'[^\']+\''
        
        dialogue_chars = 0
        dialogue_sections = re.findall(dialogue_pattern, self.text)
        for section in dialogue_sections:
            dialogue_chars += len(section)
        
        narrative_chars = len(self.text) - dialogue_chars
        
        dialogue_heavy_chapters = []
        narrative_heavy_chapters = []
        
        for i, chapter in enumerate(self.chapters, 1):
            chapter_dialogue = sum(len(m) for m in re.findall(dialogue_pattern, chapter))
            chapter_ratio = chapter_dialogue / len(chapter) if chapter else 0
            
            if chapter_ratio > 0.4:
                dialogue_heavy_chapters.append((i, chapter_ratio))
            elif chapter_ratio < 0.1:
                narrative_heavy_chapters.append((i, chapter_ratio))
        
        return {
            'dialogue_chars': dialogue_chars,
            'narrative_chars': narrative_chars,
            'dialogue_ratio': dialogue_chars / len(self.text) if self.text else 0,
            'dialogue_sections': len(dialogue_sections),
            'avg_dialogue_length': dialogue_chars / len(dialogue_sections) if dialogue_sections else 0,
            'dialogue_heavy_chapters': dialogue_heavy_chapters[:5],
            'narrative_heavy_chapters': narrative_heavy_chapters[:5]
        }
    
    def analyze_sentence_variety(self):
        """Analyze sentence structure variety"""
        sentence_types = {
            'simple': 0,
            'compound': 0,
            'complex': 0,
            'compound_complex': 0,
            'question': 0,
            'exclamation': 0
        }
        
        sentence_starters = defaultdict(int)
        sentence_lengths = []
        
        for sentence in self.sentences:
            sentence_lengths.append(len(sentence.split()))
            
            if sentence.strip().endswith('?'):
                sentence_types['question'] += 1
            elif sentence.strip().endswith('!'):
                sentence_types['exclamation'] += 1
            
            conjunctions = len(re.findall(r'\b(and|but|or|nor|for|yet|so)\b', sentence.lower()))
            subordinators = len(re.findall(r'\b(because|although|since|when|while|if|unless|after|before)\b', sentence.lower()))
            
            if conjunctions > 0 and subordinators > 0:
                sentence_types['compound_complex'] += 1
            elif subordinators > 0:
                sentence_types['complex'] += 1
            elif conjunctions > 0:
                sentence_types['compound'] += 1
            else:
                sentence_types['simple'] += 1
            
            first_word = sentence.split()[0].lower() if sentence.split() else ''
            if first_word:
                sentence_starters[first_word] += 1
        
        length_variance = np.std(sentence_lengths) if sentence_lengths else 0
        
        return {
            'sentence_types': sentence_types,
            'avg_sentence_length': np.mean(sentence_lengths) if sentence_lengths else 0,
            'sentence_length_variance': length_variance,
            'shortest_sentence': min(sentence_lengths) if sentence_lengths else 0,
            'longest_sentence': max(sentence_lengths) if sentence_lengths else 0,
            'common_starters': Counter(sentence_starters).most_common(10),
            'variety_score': length_variance / np.mean(sentence_lengths) if sentence_lengths and np.mean(sentence_lengths) > 0 else 0
        }
    
    def analyze_repetition_patterns(self):
        """Detect repetitive words and phrases"""
        word_distances = defaultdict(list)
        
        for i, word in enumerate(self.words):
            if len(word) > 4:
                word_distances[word].append(i)
        
        repetitive_words = {}
        for word, positions in word_distances.items():
            if len(positions) > 10:
                distances = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
                avg_distance = np.mean(distances)
                if avg_distance < 100:
                    repetitive_words[word] = {
                        'count': len(positions),
                        'avg_distance': avg_distance,
                        'frequency': len(positions) / len(self.words)
                    }
        
        repeated_sentence_starts = []
        for i in range(len(self.sentences) - 1):
            if self.sentences[i][:20] == self.sentences[i+1][:20]:
                repeated_sentence_starts.append(self.sentences[i][:50])
        
        alliteration_count = 0
        for sentence in self.sentences[:1000]:
            words = sentence.split()
            for i in range(len(words) - 2):
                if (len(words[i]) > 2 and len(words[i+1]) > 2 and 
                    words[i][0].lower() == words[i+1][0].lower() == words[i+2][0].lower()):
                    alliteration_count += 1
        
        return {
            'repetitive_words': sorted(repetitive_words.items(), 
                                     key=lambda x: x[1]['frequency'], 
                                     reverse=True)[:20],
            'repeated_starts': repeated_sentence_starts[:5],
            'alliteration_frequency': alliteration_count / min(1000, len(self.sentences)) if self.sentences else 0
        }
    
    def analyze_pacing(self):
        """Analyze pacing through sentence and paragraph lengths"""
        chapter_pacing = []
        
        for i, chapter in enumerate(self.chapters, 1):
            sentences = re.split(r'[.!?]+', chapter)
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            
            if sentence_lengths:
                pacing_data = {
                    'chapter': i,
                    'avg_sentence_length': np.mean(sentence_lengths),
                    'sentence_variance': np.std(sentence_lengths),
                    'short_sentences': sum(1 for l in sentence_lengths if l < 10),
                    'long_sentences': sum(1 for l in sentence_lengths if l > 25),
                    'action_words': len(re.findall(r'\b(ran|jumped|fought|struck|grabbed|pushed|pulled|threw|caught|fell)\b', chapter.lower()))
                }
                
                if pacing_data['avg_sentence_length'] < 12 and pacing_data['action_words'] > 10:
                    pacing_data['pace'] = 'fast'
                elif pacing_data['avg_sentence_length'] > 20:
                    pacing_data['pace'] = 'slow'
                else:
                    pacing_data['pace'] = 'moderate'
                
                chapter_pacing.append(pacing_data)
        
        return chapter_pacing
    
    def create_visualizations(self, output_dir='analysis_output'):
        """Create writing style visualizations"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'Writing Style Analysis: {self.file_path.name}', fontsize=16)
        
        voice_data = self.analyze_voice()
        labels = ['Active Voice', 'Passive Voice']
        sizes = [voice_data['active_count'], voice_data['passive_count']]
        colors = ['#2ecc71', '#e74c3c']
        axes[0, 0].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        axes[0, 0].set_title('Active vs Passive Voice')
        
        word_types = self.analyze_word_types()
        categories = ['Adverbs', 'Adjectives', 'Other']
        adverb_pct = word_types['adverb_density'] * 100
        adj_pct = word_types['adjective_density'] * 100
        other_pct = 100 - adverb_pct - adj_pct
        axes[0, 1].bar(categories, [adverb_pct, adj_pct, other_pct], 
                      color=['coral', 'skyblue', 'lightgray'])
        axes[0, 1].set_ylabel('Percentage of Total Words')
        axes[0, 1].set_title('Word Type Distribution')
        
        dialogue_data = self.analyze_dialogue_narrative_ratio()
        labels = ['Dialogue', 'Narrative']
        sizes = [dialogue_data['dialogue_chars'], dialogue_data['narrative_chars']]
        colors = ['#9b59b6', '#3498db']
        axes[0, 2].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=45)
        axes[0, 2].set_title('Dialogue vs Narrative')
        
        sentence_variety = self.analyze_sentence_variety()
        sentence_types = list(sentence_variety['sentence_types'].keys())
        counts = list(sentence_variety['sentence_types'].values())
        axes[1, 0].bar(sentence_types, counts, color='steelblue')
        axes[1, 0].set_xlabel('Sentence Type')
        axes[1, 0].set_ylabel('Count')
        axes[1, 0].set_title('Sentence Structure Variety')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        pacing_data = self.analyze_pacing()
        chapters = [d['chapter'] for d in pacing_data]
        avg_lengths = [d['avg_sentence_length'] for d in pacing_data]
        axes[1, 1].plot(chapters, avg_lengths, marker='o', color='darkgreen', linewidth=2)
        axes[1, 1].set_xlabel('Chapter')
        axes[1, 1].set_ylabel('Avg Words per Sentence')
        axes[1, 1].set_title('Pacing by Chapter')
        axes[1, 1].axhline(y=15, color='gray', linestyle='--', alpha=0.5)
        
        top_adverbs = word_types['top_adverbs'][:10]
        if top_adverbs:
            words, counts = zip(*top_adverbs)
            axes[1, 2].barh(words, counts, color='purple')
            axes[1, 2].set_xlabel('Frequency')
            axes[1, 2].set_title('Most Common Adverbs')
        
        plt.tight_layout()
        plt.savefig(output_path / 'writing_style_charts.png', dpi=150, bbox_inches='tight')
        print(f"✓ Saved visualizations to {output_path / 'writing_style_charts.png'}")
        plt.close()
    
    def generate_report(self):
        """Generate comprehensive writing style report"""
        print("\n" + "="*60)
        print("WRITING STYLE ANALYSIS REPORT")
        print("="*60)
        
        self.load_text()
        self.extract_components()
        
        print("\n🎯 VOICE ANALYSIS")
        print("-"*40)
        voice_data = self.analyze_voice()
        print(f"  Active sentences: {voice_data['active_count']:,} ({(1-voice_data['passive_ratio'])*100:.1f}%)")
        print(f"  Passive sentences: {voice_data['passive_count']:,} ({voice_data['passive_ratio']*100:.1f}%)")
        if voice_data['passive_ratio'] > 0.2:
            print("  ⚠️  High passive voice usage detected (>20%)")
        print("\n  Example passive constructions:")
        for example in voice_data['passive_examples'][:3]:
            print(f"    • {example}")
        
        print("\n📝 WORD CHOICE ANALYSIS")
        print("-"*40)
        word_types = self.analyze_word_types()
        print(f"  Adverb density: {word_types['adverb_density']*100:.2f}%")
        print(f"  Adjective density: {word_types['adjective_density']*100:.2f}%")
        if word_types['adverb_density'] > 0.05:
            print("  ⚠️  High adverb usage (>5%) - consider stronger verbs")
        print(f"\n  Most common adverbs:")
        for word, count in word_types['top_adverbs'][:5]:
            print(f"    • {word}: {count} times")
        if word_types['overused_adverbs']:
            print(f"\n  Potentially overused adverbs:")
            for word in word_types['overused_adverbs'][:5]:
                print(f"    • {word}")
        
        print("\n💬 DIALOGUE VS NARRATIVE")
        print("-"*40)
        dialogue_data = self.analyze_dialogue_narrative_ratio()
        print(f"  Dialogue: {dialogue_data['dialogue_ratio']*100:.1f}% of text")
        print(f"  Total dialogue sections: {dialogue_data['dialogue_sections']:,}")
        print(f"  Average dialogue length: {dialogue_data['avg_dialogue_length']:.0f} characters")
        if dialogue_data['dialogue_heavy_chapters']:
            print(f"\n  Most dialogue-heavy chapters:")
            for chapter, ratio in dialogue_data['dialogue_heavy_chapters'][:3]:
                print(f"    • Chapter {chapter}: {ratio*100:.1f}% dialogue")
        
        print("\n🔄 CLICHÉS AND REPETITION")
        print("-"*40)
        cliche_data = self.detect_cliches()
        if cliche_data['cliches_found']:
            print(f"  Clichés found: {cliche_data['cliche_count']}")
            for cliche, count in list(cliche_data['cliches_found'].items())[:5]:
                print(f"    • '{cliche}': {count} times")
        else:
            print("  ✓ No common clichés detected")
        
        if cliche_data['overused_phrases']:
            print(f"\n  Overused phrases (3+ words):")
            for phrase, count in cliche_data['overused_phrases'][:5]:
                print(f"    • '{phrase}': {count} times")
        
        print("\n📊 SENTENCE VARIETY")
        print("-"*40)
        sentence_variety = self.analyze_sentence_variety()
        print(f"  Average sentence length: {sentence_variety['avg_sentence_length']:.1f} words")
        print(f"  Shortest: {sentence_variety['shortest_sentence']} words")
        print(f"  Longest: {sentence_variety['longest_sentence']} words")
        print(f"  Variety score: {sentence_variety['variety_score']:.2f}")
        print(f"\n  Sentence types:")
        total_sentences = sum(sentence_variety['sentence_types'].values())
        for stype, count in sentence_variety['sentence_types'].items():
            percentage = (count / total_sentences * 100) if total_sentences > 0 else 0
            print(f"    • {stype.capitalize()}: {count} ({percentage:.1f}%)")
        
        print("\n⚡ PACING ANALYSIS")
        print("-"*40)
        pacing_data = self.analyze_pacing()
        fast_chapters = [d['chapter'] for d in pacing_data if d.get('pace') == 'fast']
        slow_chapters = [d['chapter'] for d in pacing_data if d.get('pace') == 'slow']
        
        if fast_chapters:
            print(f"  Fast-paced chapters: {fast_chapters[:5]}")
        if slow_chapters:
            print(f"  Slow-paced chapters: {slow_chapters[:5]}")
        
        avg_pace = np.mean([d['avg_sentence_length'] for d in pacing_data])
        print(f"  Overall pacing: {'Fast' if avg_pace < 12 else 'Slow' if avg_pace > 20 else 'Moderate'}")
        
        print("\n🔁 REPETITION PATTERNS")
        print("-"*40)
        repetition_data = self.analyze_repetition_patterns()
        if repetition_data['repetitive_words']:
            print("  Most repetitive words:")
            for word, data in repetition_data['repetitive_words'][:5]:
                print(f"    • '{word}': {data['count']} times (avg {data['avg_distance']:.0f} words apart)")
        
        print(f"  Alliteration frequency: {repetition_data['alliteration_frequency']:.2%}")
        
        self.create_visualizations()
        
        output_path = Path('analysis_output')
        output_path.mkdir(exist_ok=True)
        
        full_report = {
            'file': str(self.file_path),
            'voice_analysis': voice_data,
            'word_types': {
                'adverb_density': word_types['adverb_density'],
                'adjective_density': word_types['adjective_density'],
                'top_adverbs': word_types['top_adverbs'],
                'overused_adverbs': word_types['overused_adverbs']
            },
            'dialogue_narrative': dialogue_data,
            'cliches': {
                'count': cliche_data['cliche_count'],
                'found': cliche_data['cliches_found'],
                'overused_phrases': cliche_data['overused_phrases']
            },
            'sentence_variety': sentence_variety,
            'pacing': pacing_data,
            'repetition': {
                'repetitive_words': repetition_data['repetitive_words'][:10],
                'alliteration_frequency': repetition_data['alliteration_frequency']
            }
        }
        
        with open(output_path / 'writing_style_report.json', 'w') as f:
            json.dump(full_report, f, indent=2, default=str)
        
        print(f"\n✓ Full report saved to {output_path / 'writing_style_report.json'}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Analyze writing style of a book')
    parser.add_argument('file', help='Path to the book text file')
    parser.add_argument('--verbose', action='store_true',
                       help='Show more detailed analysis')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    analyzer = WritingStyleAnalyzer(args.file)
    analyzer.generate_report()


if __name__ == '__main__':
    main()