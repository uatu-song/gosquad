#!/usr/bin/env python3
"""
Book Character Analysis Script
Analyzes character appearances, interactions, dialogue patterns,
and emotional arcs throughout a book.
"""

import re
import sys
import json
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from itertools import combinations


class CharacterAnalyzer:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.text = ""
        self.chapters = []
        self.characters = {}
        self.dialogue_patterns = defaultdict(list)
        self.character_interactions = defaultdict(int)
        self.character_sentiments = defaultdict(list)
        
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
            for part in chapter_splits:
                if re.match(combined_pattern, part, re.MULTILINE):
                    if current_chapter:
                        self.chapters.append(''.join(current_chapter))
                    current_chapter = [part]
                else:
                    current_chapter.append(part)
            if current_chapter:
                self.chapters.append(''.join(current_chapter))
        else:
            chunk_size = len(self.text) // 10
            self.chapters = [self.text[i:i+chunk_size] for i in range(0, len(self.text), chunk_size)]
        
        print(f"✓ Detected {len(self.chapters)} chapters/sections")
    
    def detect_characters(self, min_mentions=5):
        """Detect character names using NER-like patterns"""
        name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        
        potential_names = re.findall(name_pattern, self.text)
        name_counts = Counter(potential_names)
        
        common_words = set(['The', 'This', 'That', 'These', 'Those', 'What', 'When',
                           'Where', 'Why', 'How', 'Who', 'Which', 'Chapter', 'Part',
                           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                           'Saturday', 'Sunday', 'January', 'February', 'March',
                           'April', 'May', 'June', 'July', 'August', 'September',
                           'October', 'November', 'December', 'Mr', 'Mrs', 'Ms',
                           'Dr', 'Prof', 'Lord', 'Lady', 'Sir', 'Dame'])
        
        self.characters = {}
        for name, count in name_counts.items():
            if count >= min_mentions and name not in common_words:
                if ' ' in name:
                    first_name = name.split()[0]
                    last_name = name.split()[-1]
                    self.characters[name] = {
                        'full_name': name,
                        'first_name': first_name,
                        'last_name': last_name,
                        'count': count,
                        'aliases': [name, first_name, last_name]
                    }
                else:
                    self.characters[name] = {
                        'full_name': name,
                        'first_name': name,
                        'last_name': '',
                        'count': count,
                        'aliases': [name]
                    }
        
        self._merge_character_variants()
        print(f"✓ Detected {len(self.characters)} characters (min {min_mentions} mentions)")
    
    def _merge_character_variants(self):
        """Merge character name variants (e.g., 'John', 'John Smith', 'Mr. Smith')"""
        merged = {}
        processed = set()
        
        for name1, data1 in self.characters.items():
            if name1 in processed:
                continue
            
            merged_data = data1.copy()
            merged_data['aliases'] = set(data1['aliases'])
            merged_data['count'] = data1['count']
            
            for name2, data2 in self.characters.items():
                if name1 != name2 and name2 not in processed:
                    if (data1['first_name'] and data1['first_name'] == data2['first_name']) or \
                       (data1['last_name'] and data1['last_name'] == data2['last_name']):
                        merged_data['aliases'].update(data2['aliases'])
                        merged_data['count'] += data2['count']
                        processed.add(name2)
            
            merged[name1] = merged_data
            merged[name1]['aliases'] = list(merged_data['aliases'])
            processed.add(name1)
        
        self.characters = merged
    
    def analyze_dialogue(self):
        """Extract and analyze dialogue patterns"""
        dialogue_pattern = r'"([^"]+)"(?:\s*(?:said|says|asked|replied|shouted|whispered|muttered|exclaimed|answered|responded|cried|yelled|demanded|suggested|insisted|continued|added|interrupted|agreed|explained|wondered|thought)\s+([A-Z][a-z]+))?'
        
        dialogues = re.findall(dialogue_pattern, self.text)
        
        for dialogue, speaker in dialogues:
            if speaker:
                for char_name, char_data in self.characters.items():
                    if speaker in char_data['aliases']:
                        self.dialogue_patterns[char_name].append({
                            'text': dialogue,
                            'length': len(dialogue.split()),
                            'sentences': len(re.split(r'[.!?]', dialogue))
                        })
                        break
        
        alt_pattern = r'([A-Z][a-z]+)\s+(?:said|says|asked|replied|shouted|whispered|muttered|exclaimed|answered|responded|cried|yelled|demanded|suggested|insisted|continued|added|interrupted|agreed|explained|wondered|thought)[,:]?\s*"([^"]+)"'
        alt_dialogues = re.findall(alt_pattern, self.text)
        
        for speaker, dialogue in alt_dialogues:
            for char_name, char_data in self.characters.items():
                if speaker in char_data['aliases']:
                    self.dialogue_patterns[char_name].append({
                        'text': dialogue,
                        'length': len(dialogue.split()),
                        'sentences': len(re.split(r'[.!?]', dialogue))
                    })
                    break
        
        print(f"✓ Extracted dialogue for {len(self.dialogue_patterns)} characters")
    
    def analyze_interactions(self, window_size=150):
        """Analyze character co-occurrences and interactions"""
        sentences = re.split(r'[.!?]+', self.text)
        
        for sentence in sentences:
            words = sentence.split()
            for i in range(0, len(words), window_size):
                window = ' '.join(words[i:i+window_size])
                
                chars_in_window = []
                for char_name, char_data in self.characters.items():
                    for alias in char_data['aliases']:
                        if alias in window:
                            chars_in_window.append(char_name)
                            break
                
                chars_in_window = list(set(chars_in_window))
                
                for char1, char2 in combinations(chars_in_window, 2):
                    key = tuple(sorted([char1, char2]))
                    self.character_interactions[key] += 1
        
        print(f"✓ Analyzed {len(self.character_interactions)} character relationships")
    
    def analyze_character_sentiment(self):
        """Analyze sentiment around character mentions"""
        positive_words = set(['happy', 'joy', 'love', 'loved', 'loving', 'smile', 'smiled',
                             'smiling', 'laugh', 'laughed', 'laughing', 'wonderful', 'beautiful',
                             'brilliant', 'excellent', 'good', 'great', 'pleased', 'delighted',
                             'cheerful', 'excited', 'enthusiasm', 'warm', 'kind', 'gentle'])
        
        negative_words = set(['sad', 'angry', 'anger', 'hate', 'hated', 'fear', 'feared',
                             'frown', 'frowned', 'cry', 'cried', 'crying', 'terrible', 'awful',
                             'horrible', 'bad', 'evil', 'disappointed', 'upset', 'miserable',
                             'pain', 'hurt', 'worried', 'anxious', 'nervous', 'scared'])
        
        for char_name, char_data in self.characters.items():
            for alias in char_data['aliases']:
                pattern = rf'\b{re.escape(alias)}\b(.{{0,100}})'
                matches = re.finditer(pattern, self.text, re.IGNORECASE)
                
                for match in matches:
                    context = match.group(1).lower()
                    words = context.split()
                    
                    positive_score = sum(1 for w in words if w in positive_words)
                    negative_score = sum(1 for w in words if w in negative_words)
                    
                    if positive_score > 0 or negative_score > 0:
                        sentiment = (positive_score - negative_score) / (positive_score + negative_score)
                        self.character_sentiments[char_name].append(sentiment)
        
        print(f"✓ Analyzed sentiment for {len(self.character_sentiments)} characters")
    
    def calculate_character_importance(self):
        """Calculate character importance scores"""
        importance_scores = {}
        
        for char_name, char_data in self.characters.items():
            mention_score = char_data['count'] / max(c['count'] for c in self.characters.values())
            
            dialogue_score = 0
            if char_name in self.dialogue_patterns:
                total_dialogue = sum(len(d) for d in self.dialogue_patterns.values())
                if total_dialogue > 0:
                    dialogue_score = len(self.dialogue_patterns[char_name]) / total_dialogue
            
            interaction_score = 0
            char_interactions = sum(count for (c1, c2), count in self.character_interactions.items()
                                  if c1 == char_name or c2 == char_name)
            total_interactions = sum(self.character_interactions.values())
            if total_interactions > 0:
                interaction_score = char_interactions / total_interactions
            
            importance_scores[char_name] = {
                'mention_score': mention_score,
                'dialogue_score': dialogue_score,
                'interaction_score': interaction_score,
                'overall_importance': (mention_score * 0.4 + dialogue_score * 0.3 + interaction_score * 0.3)
            }
        
        return importance_scores
    
    def analyze_character_arcs(self):
        """Track character presence and activity across chapters"""
        character_arcs = defaultdict(list)
        
        for i, chapter in enumerate(self.chapters, 1):
            chapter_lower = chapter.lower()
            
            for char_name, char_data in self.characters.items():
                mentions = 0
                for alias in char_data['aliases']:
                    mentions += len(re.findall(rf'\b{re.escape(alias)}\b', chapter, re.IGNORECASE))
                
                character_arcs[char_name].append({
                    'chapter': i,
                    'mentions': mentions,
                    'presence': mentions > 0
                })
        
        return character_arcs
    
    def create_character_network(self, output_dir='analysis_output'):
        """Create character interaction network graph"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        G = nx.Graph()
        
        importance_scores = self.calculate_character_importance()
        top_characters = sorted(importance_scores.items(), 
                              key=lambda x: x[1]['overall_importance'], 
                              reverse=True)[:15]
        
        for char_name, scores in top_characters:
            G.add_node(char_name, importance=scores['overall_importance'])
        
        for (char1, char2), weight in self.character_interactions.items():
            if char1 in [c[0] for c in top_characters] and char2 in [c[0] for c in top_characters]:
                if weight > 2:
                    G.add_edge(char1, char2, weight=weight)
        
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        node_sizes = [G.nodes[node]['importance'] * 3000 for node in G.nodes()]
        edge_weights = [G[u][v]['weight'] / 5 for u, v in G.edges()]
        
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue',
                              edgecolors='navy', linewidths=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5)
        
        plt.title('Character Interaction Network', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path / 'character_network.png', dpi=150, bbox_inches='tight')
        print(f"✓ Saved character network to {output_path / 'character_network.png'}")
        plt.close()
    
    def create_visualizations(self, output_dir='analysis_output'):
        """Create character analysis visualizations"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'Character Analysis: {self.file_path.name}', fontsize=16)
        
        importance_scores = self.calculate_character_importance()
        top_10 = sorted(importance_scores.items(), 
                       key=lambda x: x[1]['overall_importance'], 
                       reverse=True)[:10]
        
        names = [name for name, _ in top_10]
        scores = [score['overall_importance'] for _, score in top_10]
        axes[0, 0].barh(names, scores, color='steelblue')
        axes[0, 0].set_xlabel('Importance Score')
        axes[0, 0].set_title('Top 10 Characters by Importance')
        
        dialogue_counts = {name: len(dialogues) for name, dialogues in self.dialogue_patterns.items()}
        if dialogue_counts:
            top_speakers = sorted(dialogue_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            speaker_names, line_counts = zip(*top_speakers)
            axes[0, 1].bar(range(len(speaker_names)), line_counts, color='forestgreen')
            axes[0, 1].set_xticks(range(len(speaker_names)))
            axes[0, 1].set_xticklabels(speaker_names, rotation=45, ha='right')
            axes[0, 1].set_ylabel('Number of Dialogue Lines')
            axes[0, 1].set_title('Most Talkative Characters')
        
        character_arcs = self.analyze_character_arcs()
        top_5_chars = [name for name, _ in top_10[:5]]
        chapters = list(range(1, len(self.chapters) + 1))
        
        for char_name in top_5_chars:
            arc_data = character_arcs[char_name]
            mentions = [d['mentions'] for d in arc_data]
            axes[0, 2].plot(chapters, mentions, marker='o', label=char_name, linewidth=2)
        
        axes[0, 2].set_xlabel('Chapter')
        axes[0, 2].set_ylabel('Mentions')
        axes[0, 2].set_title('Character Presence Across Chapters')
        axes[0, 2].legend(fontsize=8)
        
        if self.dialogue_patterns:
            avg_dialogue_lengths = {}
            for char, dialogues in self.dialogue_patterns.items():
                if len(dialogues) >= 5:
                    avg_length = np.mean([d['length'] for d in dialogues])
                    avg_dialogue_lengths[char] = avg_length
            
            if avg_dialogue_lengths:
                top_lengths = sorted(avg_dialogue_lengths.items(), key=lambda x: x[1], reverse=True)[:10]
                char_names, lengths = zip(*top_lengths)
                axes[1, 0].barh(char_names, lengths, color='coral')
                axes[1, 0].set_xlabel('Average Words per Dialogue')
                axes[1, 0].set_title('Character Verbosity')
        
        if self.character_sentiments:
            sentiment_avgs = {}
            for char, sentiments in self.character_sentiments.items():
                if len(sentiments) >= 5:
                    sentiment_avgs[char] = np.mean(sentiments)
            
            if sentiment_avgs:
                top_sentiments = sorted(sentiment_avgs.items(), key=lambda x: abs(x[1]), reverse=True)[:10]
                char_names, sentiments = zip(*top_sentiments)
                colors = ['green' if s > 0 else 'red' for s in sentiments]
                axes[1, 1].barh(char_names, sentiments, color=colors)
                axes[1, 1].set_xlabel('Average Sentiment (-1 to 1)')
                axes[1, 1].set_title('Character Sentiment Analysis')
                axes[1, 1].axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        
        top_interactions = sorted(self.character_interactions.items(), 
                                key=lambda x: x[1], reverse=True)[:10]
        if top_interactions:
            labels = [f"{c1}-{c2}" for (c1, c2), _ in top_interactions]
            values = [count for _, count in top_interactions]
            axes[1, 2].bar(range(len(labels)), values, color='purple')
            axes[1, 2].set_xticks(range(len(labels)))
            axes[1, 2].set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
            axes[1, 2].set_ylabel('Co-occurrence Count')
            axes[1, 2].set_title('Top Character Interactions')
        
        plt.tight_layout()
        plt.savefig(output_path / 'character_analysis_charts.png', dpi=150, bbox_inches='tight')
        print(f"✓ Saved visualizations to {output_path / 'character_analysis_charts.png'}")
        plt.close()
        
        self.create_character_network(output_dir)
    
    def generate_character_profiles(self):
        """Generate detailed profiles for main characters"""
        importance_scores = self.calculate_character_importance()
        top_characters = sorted(importance_scores.items(), 
                              key=lambda x: x[1]['overall_importance'], 
                              reverse=True)[:10]
        
        profiles = {}
        for char_name, importance in top_characters:
            char_data = self.characters[char_name]
            
            profile = {
                'name': char_name,
                'aliases': char_data['aliases'],
                'total_mentions': char_data['count'],
                'importance_score': importance['overall_importance'],
                'dialogue_lines': len(self.dialogue_patterns.get(char_name, [])),
                'avg_dialogue_length': 0,
                'sentiment': 'neutral',
                'key_relationships': [],
                'first_appearance': None,
                'last_appearance': None
            }
            
            if char_name in self.dialogue_patterns:
                dialogues = self.dialogue_patterns[char_name]
                if dialogues:
                    profile['avg_dialogue_length'] = np.mean([d['length'] for d in dialogues])
            
            if char_name in self.character_sentiments:
                sentiments = self.character_sentiments[char_name]
                if sentiments:
                    avg_sentiment = np.mean(sentiments)
                    if avg_sentiment > 0.2:
                        profile['sentiment'] = 'positive'
                    elif avg_sentiment < -0.2:
                        profile['sentiment'] = 'negative'
            
            relationships = []
            for (c1, c2), count in self.character_interactions.items():
                if c1 == char_name:
                    relationships.append({'character': c2, 'interactions': count})
                elif c2 == char_name:
                    relationships.append({'character': c1, 'interactions': count})
            profile['key_relationships'] = sorted(relationships, 
                                                 key=lambda x: x['interactions'], 
                                                 reverse=True)[:5]
            
            character_arc = self.analyze_character_arcs()[char_name]
            for i, chapter_data in enumerate(character_arc):
                if chapter_data['presence'] and profile['first_appearance'] is None:
                    profile['first_appearance'] = i + 1
                if chapter_data['presence']:
                    profile['last_appearance'] = i + 1
            
            profiles[char_name] = profile
        
        return profiles
    
    def generate_report(self):
        """Generate comprehensive character analysis report"""
        print("\n" + "="*60)
        print("CHARACTER ANALYSIS REPORT")
        print("="*60)
        
        self.load_text()
        self.detect_chapters()
        self.detect_characters(min_mentions=5)
        
        if not self.characters:
            print("\n⚠️  No characters detected. Try adjusting minimum mention threshold.")
            return
        
        self.analyze_dialogue()
        self.analyze_interactions()
        self.analyze_character_sentiment()
        
        print("\n👥 CHARACTER OVERVIEW")
        print("-"*40)
        print(f"  Total characters detected: {len(self.characters)}")
        print(f"  Characters with dialogue: {len(self.dialogue_patterns)}")
        print(f"  Character relationships: {len(self.character_interactions)}")
        
        print("\n🌟 TOP CHARACTERS BY IMPORTANCE")
        print("-"*40)
        importance_scores = self.calculate_character_importance()
        top_10 = sorted(importance_scores.items(), 
                       key=lambda x: x[1]['overall_importance'], 
                       reverse=True)[:10]
        
        for i, (name, scores) in enumerate(top_10, 1):
            print(f"  {i}. {name}")
            print(f"     Mentions: {self.characters[name]['count']}")
            print(f"     Dialogue lines: {len(self.dialogue_patterns.get(name, []))}")
            print(f"     Importance score: {scores['overall_importance']:.3f}")
        
        print("\n💬 DIALOGUE STATISTICS")
        print("-"*40)
        if self.dialogue_patterns:
            total_dialogue = sum(len(d) for d in self.dialogue_patterns.values())
            print(f"  Total dialogue lines: {total_dialogue}")
            
            most_talkative = max(self.dialogue_patterns.items(), key=lambda x: len(x[1]))
            print(f"  Most talkative: {most_talkative[0]} ({len(most_talkative[1])} lines)")
            
            avg_lengths = {}
            for char, dialogues in self.dialogue_patterns.items():
                if dialogues:
                    avg_lengths[char] = np.mean([d['length'] for d in dialogues])
            
            if avg_lengths:
                most_verbose = max(avg_lengths.items(), key=lambda x: x[1])
                print(f"  Most verbose: {most_verbose[0]} ({most_verbose[1]:.1f} words/line)")
        
        print("\n🤝 KEY RELATIONSHIPS")
        print("-"*40)
        top_relationships = sorted(self.character_interactions.items(), 
                                 key=lambda x: x[1], reverse=True)[:5]
        for (char1, char2), count in top_relationships:
            print(f"  {char1} ↔ {char2}: {count} interactions")
        
        print("\n😊😐😞 CHARACTER SENTIMENT")
        print("-"*40)
        if self.character_sentiments:
            sentiment_summary = {}
            for char, sentiments in self.character_sentiments.items():
                if len(sentiments) >= 5:
                    avg_sentiment = np.mean(sentiments)
                    if avg_sentiment > 0.2:
                        sentiment_summary[char] = 'Positive'
                    elif avg_sentiment < -0.2:
                        sentiment_summary[char] = 'Negative'
                    else:
                        sentiment_summary[char] = 'Neutral'
            
            for char, sentiment in list(sentiment_summary.items())[:5]:
                print(f"  {char}: {sentiment}")
        
        self.create_visualizations()
        
        profiles = self.generate_character_profiles()
        
        output_path = Path('analysis_output')
        output_path.mkdir(exist_ok=True)
        
        full_report = {
            'file': str(self.file_path),
            'total_characters': len(self.characters),
            'character_list': list(self.characters.keys()),
            'importance_scores': importance_scores,
            'character_profiles': profiles,
            'top_relationships': [
                {'characters': [c1, c2], 'interactions': count}
                for (c1, c2), count in top_relationships
            ],
            'dialogue_statistics': {
                'total_lines': sum(len(d) for d in self.dialogue_patterns.values()),
                'by_character': {char: len(lines) for char, lines in self.dialogue_patterns.items()}
            }
        }
        
        with open(output_path / 'character_analysis_report.json', 'w') as f:
            json.dump(full_report, f, indent=2, default=str)
        
        print(f"\n✓ Full report saved to {output_path / 'character_analysis_report.json'}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Analyze characters in a book')
    parser.add_argument('file', help='Path to the book text file')
    parser.add_argument('--min-mentions', type=int, default=5,
                       help='Minimum mentions to consider as character (default: 5)')
    parser.add_argument('--top-n', type=int, default=10,
                       help='Number of top characters to analyze (default: 10)')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    analyzer = CharacterAnalyzer(args.file)
    analyzer.generate_report()


if __name__ == '__main__':
    main()