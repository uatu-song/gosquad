#!/usr/bin/env python3
"""
Simplified Book Character Analysis Script
Works with single chapters and doesn't require networkx
"""

import re
import sys
import json
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
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
        """Simple chapter detection or treat as single chapter"""
        self.chapters = [self.text]  # Treat entire text as one chapter
        print(f"✓ Treating as single chapter/section")
    
    def detect_characters(self, min_mentions=1):
        """Detect character names with very low threshold for single chapters"""
        # Multiple patterns for character detection
        patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Standard names
            r'\b[A-Z][a-z]+\b',  # Single names
            r'\bMr\.\s+[A-Z][a-z]+\b',  # Mr. titles
            r'\bMs\.\s+[A-Z][a-z]+\b',  # Ms. titles  
            r'\bDr\.\s+[A-Z][a-z]+\b',  # Dr. titles
        ]
        
        all_names = []
        for pattern in patterns:
            names = re.findall(pattern, self.text)
            all_names.extend(names)
        
        name_counts = Counter(all_names)
        
        # Extended list of common words to exclude
        common_words = set(['The', 'This', 'That', 'These', 'Those', 'What', 'When',
                           'Where', 'Why', 'How', 'Who', 'Which', 'Chapter', 'Part',
                           'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                           'Saturday', 'Sunday', 'January', 'February', 'March',
                           'April', 'May', 'June', 'July', 'August', 'September',
                           'October', 'November', 'December', 'Mr', 'Mrs', 'Ms',
                           'Dr', 'Prof', 'Lord', 'Lady', 'Sir', 'Dame', 'New',
                           'Old', 'First', 'Last', 'Next', 'Previous', 'Every',
                           'Some', 'Any', 'All', 'Most', 'Many', 'Few', 'Several',
                           'Each', 'Both', 'Either', 'Neither', 'Other', 'Another',
                           'Such', 'Only', 'Just', 'Even', 'Still', 'Also', 'Too',
                           'Very', 'So', 'But', 'And', 'Or', 'If', 'Then', 'Than',
                           'Now', 'Here', 'There', 'Where', 'When', 'Why', 'How'])
        
        # Also look for specific character indicators in dialogue
        dialogue_speakers = re.findall(r'"[^"]+"\s+(?:said|says|asked|replied|shouted|whispered|muttered)\s+([A-Z][a-z]+)', self.text)
        dialogue_speakers.extend(re.findall(r'([A-Z][a-z]+)\s+(?:said|says|asked|replied|shouted|whispered|muttered)', self.text))
        
        for speaker in dialogue_speakers:
            name_counts[speaker] += 1
        
        self.characters = {}
        for name, count in name_counts.items():
            if count >= min_mentions and name not in common_words:
                # Check if it's actually used as a name in context
                if self._verify_as_character(name):
                    self.characters[name] = {
                        'full_name': name,
                        'first_name': name.split()[0] if ' ' in name else name,
                        'last_name': name.split()[-1] if ' ' in name else '',
                        'count': count,
                        'aliases': [name]
                    }
        
        # If no characters found with standard detection, look for pronouns and references
        if not self.characters:
            print("  No named characters found, analyzing unnamed references...")
            self._detect_unnamed_characters()
        
        print(f"✓ Detected {len(self.characters)} characters (min {min_mentions} mentions)")
        
        # Print detected characters for debugging
        if self.characters:
            print("  Characters found:")
            for name, data in sorted(self.characters.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
                print(f"    • {name}: {data['count']} mentions")
    
    def _verify_as_character(self, name):
        """Verify if a capitalized word is actually used as a character name"""
        # Check if it appears with character-indicating context
        character_contexts = [
            rf'\b{re.escape(name)}\s+(?:said|says|asked|replied|walked|ran|looked|smiled|frowned|laughed)',
            rf'(?:said|asked|told|called)\s+{re.escape(name)}\b',
            rf'\b{re.escape(name)}\'s\s+\w+',  # Possessive
            rf'\b(?:he|she|they)\s+(?:was|were)\s+{re.escape(name)}\b',
        ]
        
        for pattern in character_contexts:
            if re.search(pattern, self.text, re.IGNORECASE):
                return True
        
        return False
    
    def _detect_unnamed_characters(self):
        """Detect unnamed characters like 'the child', 'the pilot', etc."""
        unnamed_patterns = [
            r'the\s+(?:child|boy|girl|man|woman|pilot|captain|doctor|soldier|guard)',
            r'(?:he|she|they|it)\s+(?:said|asked|replied|walked|ran|looked)',
        ]
        
        for pattern in unnamed_patterns:
            matches = re.findall(pattern, self.text.lower())
            if matches:
                char_name = matches[0].split()[0] if ' ' in matches[0] else matches[0]
                char_name = char_name.capitalize()
                if char_name not in self.characters and len(matches) >= 1:
                    self.characters[char_name] = {
                        'full_name': char_name,
                        'first_name': char_name,
                        'last_name': '',
                        'count': len(matches),
                        'aliases': [char_name],
                        'type': 'unnamed'
                    }
    
    def analyze_dialogue(self):
        """Extract and analyze dialogue patterns"""
        # Multiple dialogue patterns
        patterns = [
            (r'"([^"]+)"\s+(?:said|says|asked|replied|shouted|whispered|muttered|exclaimed|answered|responded)\s+([A-Z][a-z]+)', 'quote_first'),
            (r'([A-Z][a-z]+)\s+(?:said|says|asked|replied|shouted|whispered|muttered|exclaimed|answered|responded)[,:]?\s*"([^"]+)"', 'name_first'),
            (r'"([^"]+)"', 'unattributed'),  # Unattributed dialogue
        ]
        
        for pattern, pattern_type in patterns:
            dialogues = re.findall(pattern, self.text)
            
            if pattern_type == 'quote_first':
                for dialogue, speaker in dialogues:
                    self._add_dialogue(speaker, dialogue)
            elif pattern_type == 'name_first':
                for speaker, dialogue in dialogues:
                    self._add_dialogue(speaker, dialogue)
            elif pattern_type == 'unattributed':
                # Try to attribute to nearest character mention
                for dialogue in dialogues:
                    if isinstance(dialogue, str):
                        self._add_dialogue('Unknown', dialogue)
        
        print(f"✓ Extracted dialogue for {len(self.dialogue_patterns)} characters")
    
    def _add_dialogue(self, speaker, dialogue):
        """Add dialogue to the appropriate character"""
        for char_name, char_data in self.characters.items():
            if speaker in char_data['aliases'] or speaker.lower() == char_name.lower():
                self.dialogue_patterns[char_name].append({
                    'text': dialogue,
                    'length': len(dialogue.split()),
                    'sentences': len(re.split(r'[.!?]', dialogue))
                })
                break
        else:
            # If speaker not found in characters, add to Unknown
            if speaker and speaker != 'Unknown':
                self.dialogue_patterns[speaker].append({
                    'text': dialogue,
                    'length': len(dialogue.split()),
                    'sentences': len(re.split(r'[.!?]', dialogue))
                })
    
    def analyze_interactions(self, window_size=150):
        """Analyze character co-occurrences"""
        words = self.text.split()
        
        for i in range(0, len(words), window_size//2):  # Overlap windows
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
        """Simple sentiment analysis around character mentions"""
        positive_words = set(['happy', 'joy', 'love', 'loved', 'loving', 'smile', 'smiled',
                             'smiling', 'laugh', 'laughed', 'laughing', 'wonderful', 'beautiful',
                             'brilliant', 'excellent', 'good', 'great', 'pleased', 'delighted'])
        
        negative_words = set(['sad', 'angry', 'anger', 'hate', 'hated', 'fear', 'feared',
                             'frown', 'frowned', 'cry', 'cried', 'crying', 'terrible', 'awful',
                             'horrible', 'bad', 'evil', 'disappointed', 'upset', 'miserable'])
        
        for char_name, char_data in self.characters.items():
            for alias in char_data['aliases']:
                pattern = rf'\b{re.escape(alias)}\b(.{{0,50}})'
                matches = re.finditer(pattern, self.text, re.IGNORECASE)
                
                for match in matches:
                    context = match.group(1).lower()
                    words = context.split()
                    
                    positive_score = sum(1 for w in words if w in positive_words)
                    negative_score = sum(1 for w in words if w in negative_words)
                    
                    if positive_score > 0 or negative_score > 0:
                        sentiment = (positive_score - negative_score) / max(1, (positive_score + negative_score))
                        self.character_sentiments[char_name].append(sentiment)
        
        print(f"✓ Analyzed sentiment for {len(self.character_sentiments)} characters")
    
    def create_visualizations(self, output_dir='analysis_output'):
        """Create character analysis visualizations without networkx"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        if not self.characters:
            print("  ⚠ No characters to visualize")
            # Create empty plot
            fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            ax.text(0.5, 0.5, 'No characters detected in this text', 
                   ha='center', va='center', fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            plt.savefig(output_path / 'character_analysis_charts.png', dpi=150, bbox_inches='tight')
            plt.close()
            return
        
        # Create visualization with available data
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'Character Analysis: {self.file_path.name}', fontsize=16)
        
        # Top characters by mentions
        top_chars = sorted(self.characters.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
        if top_chars:
            names = [name for name, _ in top_chars]
            counts = [data['count'] for _, data in top_chars]
            
            axes[0, 0].barh(names, counts, color='steelblue')
            axes[0, 0].set_xlabel('Mentions')
            axes[0, 0].set_title('Top Characters by Mentions')
        else:
            axes[0, 0].text(0.5, 0.5, 'No character data', ha='center', va='center')
            axes[0, 0].axis('off')
        
        # Dialogue distribution
        if self.dialogue_patterns:
            dialogue_counts = {name: len(dialogues) for name, dialogues in self.dialogue_patterns.items()}
            top_speakers = sorted(dialogue_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            if top_speakers:
                speaker_names, line_counts = zip(*top_speakers)
                axes[0, 1].bar(range(len(speaker_names)), line_counts, color='forestgreen')
                axes[0, 1].set_xticks(range(len(speaker_names)))
                axes[0, 1].set_xticklabels(speaker_names, rotation=45, ha='right')
                axes[0, 1].set_ylabel('Dialogue Lines')
                axes[0, 1].set_title('Characters with Dialogue')
        else:
            axes[0, 1].text(0.5, 0.5, 'No dialogue detected', ha='center', va='center')
            axes[0, 1].axis('off')
        
        # Character interactions
        if self.character_interactions:
            top_interactions = sorted(self.character_interactions.items(), 
                                     key=lambda x: x[1], reverse=True)[:10]
            if top_interactions:
                labels = [f"{c1}-{c2}" for (c1, c2), _ in top_interactions]
                values = [count for _, count in top_interactions]
                axes[1, 0].bar(range(len(labels)), values, color='purple')
                axes[1, 0].set_xticks(range(len(labels)))
                axes[1, 0].set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
                axes[1, 0].set_ylabel('Co-occurrences')
                axes[1, 0].set_title('Character Interactions')
        else:
            axes[1, 0].text(0.5, 0.5, 'No interactions detected', ha='center', va='center')
            axes[1, 0].axis('off')
        
        # Sentiment analysis
        if self.character_sentiments:
            sentiment_avgs = {}
            for char, sentiments in self.character_sentiments.items():
                if sentiments:
                    sentiment_avgs[char] = np.mean(sentiments)
            
            if sentiment_avgs:
                top_sentiments = sorted(sentiment_avgs.items(), key=lambda x: abs(x[1]), reverse=True)[:10]
                char_names, sentiments = zip(*top_sentiments)
                colors = ['green' if s > 0 else 'red' for s in sentiments]
                axes[1, 1].barh(char_names, sentiments, color=colors)
                axes[1, 1].set_xlabel('Sentiment (-1 to 1)')
                axes[1, 1].set_title('Character Sentiment')
                axes[1, 1].axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        else:
            axes[1, 1].text(0.5, 0.5, 'No sentiment data', ha='center', va='center')
            axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(output_path / 'character_analysis_charts.png', dpi=150, bbox_inches='tight')
        print(f"✓ Saved visualizations to {output_path / 'character_analysis_charts.png'}")
        plt.close()
    
    def generate_report(self):
        """Generate character analysis report"""
        print("\n" + "="*60)
        print("CHARACTER ANALYSIS REPORT")
        print("="*60)
        
        self.load_text()
        self.detect_chapters()
        self.detect_characters(min_mentions=1)  # Very low threshold for single chapters
        
        if not self.characters:
            print("\n⚠️  No characters detected in this text.")
            print("  This might be due to:")
            print("  • Text being too short")
            print("  • No proper names mentioned")
            print("  • Narrative style without named characters")
            
            # Still create output files
            self.create_visualizations()
            
            output_path = Path('analysis_output')
            output_path.mkdir(exist_ok=True)
            
            report = {
                'file': str(self.file_path),
                'total_characters': 0,
                'character_list': [],
                'message': 'No characters detected in this text'
            }
            
            with open(output_path / 'character_analysis_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"\n✓ Report saved to {output_path / 'character_analysis_report.json'}")
            print("="*60)
            return
        
        self.analyze_dialogue()
        self.analyze_interactions()
        self.analyze_character_sentiment()
        
        print("\n👥 CHARACTER OVERVIEW")
        print("-"*40)
        print(f"  Total characters detected: {len(self.characters)}")
        print(f"  Characters with dialogue: {len(self.dialogue_patterns)}")
        print(f"  Character relationships: {len(self.character_interactions)}")
        
        print("\n🌟 TOP CHARACTERS")
        print("-"*40)
        top_chars = sorted(self.characters.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
        for i, (name, data) in enumerate(top_chars, 1):
            print(f"  {i}. {name}: {data['count']} mentions")
            if name in self.dialogue_patterns:
                print(f"     Dialogue lines: {len(self.dialogue_patterns[name])}")
        
        if self.dialogue_patterns:
            print("\n💬 DIALOGUE STATISTICS")
            print("-"*40)
            total_dialogue = sum(len(d) for d in self.dialogue_patterns.values())
            print(f"  Total dialogue lines: {total_dialogue}")
            
            if total_dialogue > 0:
                most_talkative = max(self.dialogue_patterns.items(), key=lambda x: len(x[1]))
                print(f"  Most talkative: {most_talkative[0]} ({len(most_talkative[1])} lines)")
        
        if self.character_interactions:
            print("\n🤝 KEY RELATIONSHIPS")
            print("-"*40)
            top_relationships = sorted(self.character_interactions.items(), 
                                     key=lambda x: x[1], reverse=True)[:5]
            for (char1, char2), count in top_relationships:
                print(f"  {char1} ↔ {char2}: {count} interactions")
        
        self.create_visualizations()
        
        # Save report
        output_path = Path('analysis_output')
        output_path.mkdir(exist_ok=True)
        
        report = {
            'file': str(self.file_path),
            'total_characters': len(self.characters),
            'character_list': list(self.characters.keys()),
            'character_details': self.characters,
            'dialogue_statistics': {
                'total_lines': sum(len(d) for d in self.dialogue_patterns.values()),
                'by_character': {char: len(lines) for char, lines in self.dialogue_patterns.items()}
            },
            'top_relationships': [
                {'characters': [c1, c2], 'interactions': count}
                for (c1, c2), count in sorted(self.character_interactions.items(), 
                                             key=lambda x: x[1], reverse=True)[:10]
            ]
        }
        
        with open(output_path / 'character_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n✓ Full report saved to {output_path / 'character_analysis_report.json'}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Analyze characters in a book')
    parser.add_argument('file', help='Path to the book text file')
    parser.add_argument('--min-mentions', type=int, default=1,
                       help='Minimum mentions to consider as character (default: 1)')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    analyzer = CharacterAnalyzer(args.file)
    analyzer.generate_report()


if __name__ == '__main__':
    main()