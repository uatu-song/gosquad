#!/usr/bin/env python3
"""
Book Structural Analysis Script
Analyzes book structure including chapters, scenes, POV shifts,
plot arcs, timeline, and narrative patterns.
"""

import re
import sys
import json
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


class StructuralAnalyzer:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.text = ""
        self.chapters = []
        self.scenes = []
        self.paragraphs = []
        self.sentences = []
        
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
        """Detect and analyze chapter structure"""
        chapter_patterns = [
            (r'Chapter\s+(\d+)', 'numbered'),
            (r'Chapter\s+([IVXLCDM]+)', 'roman'),
            (r'CHAPTER\s+(\d+)', 'numbered_caps'),
            (r'CHAPTER\s+([IVXLCDM]+)', 'roman_caps'),
            (r'^(\d+)\.?\s*$', 'numeric_only'),
            (r'^Part\s+(\d+)', 'parts'),
            (r'^PART\s+(\d+)', 'parts_caps'),
            (r'^([A-Z][A-Za-z\s]{2,30})$', 'named_chapters')
        ]
        
        chapter_data = []
        chapter_type = None
        
        for pattern, ptype in chapter_patterns:
            matches = list(re.finditer(pattern, self.text, re.MULTILINE))
            if len(matches) > 2:
                chapter_type = ptype
                
                for i, match in enumerate(matches):
                    start = match.start()
                    end = matches[i+1].start() if i+1 < len(matches) else len(self.text)
                    
                    chapter_text = self.text[start:end]
                    chapter_data.append({
                        'number': i + 1,
                        'title': match.group(0).strip(),
                        'type': ptype,
                        'start': start,
                        'end': end,
                        'text': chapter_text,
                        'length': len(chapter_text),
                        'word_count': len(re.findall(r'\b\w+\b', chapter_text))
                    })
                break
        
        if not chapter_data:
            chunk_size = len(self.text) // 10
            for i in range(0, len(self.text), chunk_size):
                chapter_text = self.text[i:i+chunk_size]
                chapter_data.append({
                    'number': i // chunk_size + 1,
                    'title': f'Section {i // chunk_size + 1}',
                    'type': 'auto_divided',
                    'start': i,
                    'end': min(i + chunk_size, len(self.text)),
                    'text': chapter_text,
                    'length': len(chapter_text),
                    'word_count': len(re.findall(r'\b\w+\b', chapter_text))
                })
        
        self.chapters = chapter_data
        print(f"✓ Detected {len(self.chapters)} chapters (type: {chapter_type or 'auto-divided'})")
        
        return chapter_data
    
    def detect_scenes(self):
        """Detect scene breaks within chapters"""
        scene_break_patterns = [
            r'\n\s*\*\s*\*\s*\*\s*\n',
            r'\n\s*\#\s*\n',
            r'\n\s*\~\s*\~\s*\~\s*\n',
            r'\n\s*\-\s*\-\s*\-\s*\n',
            r'\n\s*\•\s*\•\s*\•\s*\n',
            r'\n{3,}',
            r'\n\s*\[\s*\]\s*\n',
            r'\n\s*\§\s*\n'
        ]
        
        all_scenes = []
        
        for chapter in self.chapters:
            chapter_text = chapter['text']
            scenes_in_chapter = []
            
            combined_pattern = '|'.join(f'({p})' for p in scene_break_patterns)
            scene_splits = re.split(combined_pattern, chapter_text)
            
            current_pos = 0
            for i, scene_text in enumerate(scene_splits):
                if scene_text and len(scene_text.strip()) > 100:
                    scenes_in_chapter.append({
                        'chapter': chapter['number'],
                        'scene_number': len(scenes_in_chapter) + 1,
                        'text': scene_text,
                        'word_count': len(re.findall(r'\b\w+\b', scene_text)),
                        'position': current_pos
                    })
                current_pos += len(scene_text) if scene_text else 0
            
            if not scenes_in_chapter:
                scenes_in_chapter.append({
                    'chapter': chapter['number'],
                    'scene_number': 1,
                    'text': chapter_text,
                    'word_count': chapter['word_count'],
                    'position': 0
                })
            
            all_scenes.extend(scenes_in_chapter)
        
        self.scenes = all_scenes
        print(f"✓ Detected {len(self.scenes)} scenes across all chapters")
        
        return all_scenes
    
    def detect_pov_shifts(self):
        """Detect potential POV shifts and narrative voice changes"""
        pov_indicators = {
            'first_person': [r'\bI\s+\w+', r'\bme\b', r'\bmy\b', r'\bmyself\b', r'\bwe\b', r'\bour\b'],
            'second_person': [r'\byou\s+\w+', r'\byour\b', r'\byourself\b'],
            'third_limited': [r'\bhe\s+thought\b', r'\bshe\s+thought\b', r'\bhe\s+felt\b', r'\bshe\s+felt\b'],
            'third_omniscient': [r'\bmeanwhile\b', r'\bunbeknownst\b', r'\blittle\s+did\s+\w+\s+know\b']
        }
        
        pov_analysis = []
        
        for chapter in self.chapters:
            chapter_text = chapter['text'].lower()
            pov_counts = defaultdict(int)
            
            for pov_type, patterns in pov_indicators.items():
                for pattern in patterns:
                    matches = len(re.findall(pattern, chapter_text))
                    pov_counts[pov_type] += matches
            
            total_indicators = sum(pov_counts.values())
            if total_indicators > 0:
                dominant_pov = max(pov_counts, key=pov_counts.get)
                confidence = pov_counts[dominant_pov] / total_indicators
            else:
                dominant_pov = 'unclear'
                confidence = 0
            
            pov_analysis.append({
                'chapter': chapter['number'],
                'dominant_pov': dominant_pov,
                'confidence': confidence,
                'indicators': dict(pov_counts)
            })
        
        pov_shifts = []
        for i in range(1, len(pov_analysis)):
            if pov_analysis[i]['dominant_pov'] != pov_analysis[i-1]['dominant_pov']:
                if pov_analysis[i]['confidence'] > 0.6 and pov_analysis[i-1]['confidence'] > 0.6:
                    pov_shifts.append({
                        'from_chapter': pov_analysis[i-1]['chapter'],
                        'to_chapter': pov_analysis[i]['chapter'],
                        'from_pov': pov_analysis[i-1]['dominant_pov'],
                        'to_pov': pov_analysis[i]['dominant_pov']
                    })
        
        return {
            'chapter_pov': pov_analysis,
            'pov_shifts': pov_shifts
        }
    
    def analyze_plot_arc(self):
        """Analyze plot arc indicators and story progression"""
        tension_words = ['conflict', 'struggle', 'fight', 'battle', 'danger', 'threat',
                        'risk', 'challenge', 'problem', 'crisis', 'trouble', 'fear',
                        'angry', 'rage', 'fury', 'tension', 'suspense', 'worry']
        
        resolution_words = ['solved', 'resolved', 'fixed', 'answered', 'realized',
                           'understood', 'discovered', 'revealed', 'peace', 'calm',
                           'relief', 'success', 'victory', 'triumph', 'happy']
        
        action_words = ['ran', 'jumped', 'fought', 'struck', 'grabbed', 'pushed',
                       'pulled', 'threw', 'caught', 'fell', 'crashed', 'exploded',
                       'attacked', 'defended', 'escaped', 'chased']
        
        plot_progression = []
        
        for chapter in self.chapters:
            text_lower = chapter['text'].lower()
            words_in_chapter = len(re.findall(r'\b\w+\b', text_lower))
            
            tension_count = sum(text_lower.count(word) for word in tension_words)
            resolution_count = sum(text_lower.count(word) for word in resolution_words)
            action_count = sum(text_lower.count(word) for word in action_words)
            
            dialogue_ratio = len(re.findall(r'"[^"]+"|\'[^\']+\'', chapter['text'])) / len(chapter['text'])
            
            intensity_score = (tension_count * 2 + action_count * 1.5) / words_in_chapter * 100 if words_in_chapter > 0 else 0
            
            plot_progression.append({
                'chapter': chapter['number'],
                'tension_density': tension_count / words_in_chapter * 100 if words_in_chapter > 0 else 0,
                'resolution_density': resolution_count / words_in_chapter * 100 if words_in_chapter > 0 else 0,
                'action_density': action_count / words_in_chapter * 100 if words_in_chapter > 0 else 0,
                'dialogue_ratio': dialogue_ratio,
                'intensity_score': intensity_score,
                'word_count': words_in_chapter
            })
        
        climax_candidates = sorted(plot_progression, 
                                  key=lambda x: x['intensity_score'], 
                                  reverse=True)[:3]
        
        potential_climax = None
        for candidate in climax_candidates:
            if candidate['chapter'] > len(self.chapters) * 0.6:
                potential_climax = candidate['chapter']
                break
        
        return {
            'progression': plot_progression,
            'potential_climax': potential_climax,
            'climax_candidates': climax_candidates
        }
    
    def analyze_timeline(self):
        """Extract and analyze temporal references"""
        time_patterns = {
            'specific_dates': r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s+\d{4})?',
            'years': r'\b(?:19|20)\d{2}\b',
            'time_of_day': r'\b(?:morning|afternoon|evening|night|midnight|dawn|dusk|sunrise|sunset|noon)\b',
            'days_of_week': r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',
            'relative_time': r'\b(?:yesterday|today|tomorrow|last\s+\w+|next\s+\w+|ago|later|earlier|before|after)\b',
            'duration': r'\b\d+\s+(?:second|minute|hour|day|week|month|year)s?\b',
            'seasons': r'\b(?:spring|summer|fall|autumn|winter)\b'
        }
        
        timeline_data = []
        
        for chapter in self.chapters:
            chapter_timeline = defaultdict(list)
            
            for time_type, pattern in time_patterns.items():
                matches = re.finditer(pattern, chapter['text'], re.IGNORECASE)
                for match in matches:
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(chapter['text']), match.end() + 50)
                    context = chapter['text'][context_start:context_end]
                    
                    chapter_timeline[time_type].append({
                        'text': match.group(),
                        'context': context,
                        'position': match.start()
                    })
            
            timeline_data.append({
                'chapter': chapter['number'],
                'temporal_references': dict(chapter_timeline),
                'total_time_references': sum(len(refs) for refs in chapter_timeline.values())
            })
        
        flashback_indicators = ['remembered', 'recalled', 'used to', 'had been', 
                               'years ago', 'when he was', 'when she was', 'in the past']
        flashforward_indicators = ['would be', 'will be', 'years later', 'in the future',
                                  'one day', 'someday', 'eventually']
        
        temporal_shifts = []
        for chapter in self.chapters:
            text_lower = chapter['text'].lower()
            
            flashback_count = sum(1 for indicator in flashback_indicators if indicator in text_lower)
            flashforward_count = sum(1 for indicator in flashforward_indicators if indicator in text_lower)
            
            if flashback_count > 2:
                temporal_shifts.append({
                    'chapter': chapter['number'],
                    'type': 'flashback',
                    'strength': flashback_count
                })
            if flashforward_count > 2:
                temporal_shifts.append({
                    'chapter': chapter['number'],
                    'type': 'flashforward',
                    'strength': flashforward_count
                })
        
        return {
            'timeline': timeline_data,
            'temporal_shifts': temporal_shifts
        }
    
    def detect_hooks_and_cliffhangers(self):
        """Detect chapter openings (hooks) and endings (cliffhangers)"""
        question_pattern = r'[?]'
        exclamation_pattern = r'[!]'
        suspense_words = ['suddenly', 'without warning', 'but', 'however', 'although',
                         'despite', 'nevertheless', 'unexpected', 'strange', 'mysterious']
        
        hooks_and_cliffhangers = []
        
        for chapter in self.chapters:
            opening = chapter['text'][:500] if len(chapter['text']) > 500 else chapter['text']
            ending = chapter['text'][-500:] if len(chapter['text']) > 500 else chapter['text']
            
            opening_questions = len(re.findall(question_pattern, opening))
            opening_exclamations = len(re.findall(exclamation_pattern, opening))
            opening_suspense = sum(1 for word in suspense_words if word in opening.lower())
            
            ending_questions = len(re.findall(question_pattern, ending))
            ending_exclamations = len(re.findall(exclamation_pattern, ending))
            ending_suspense = sum(1 for word in suspense_words if word in ending.lower())
            
            opening_score = opening_questions * 2 + opening_exclamations + opening_suspense
            ending_score = ending_questions * 3 + ending_exclamations + ending_suspense * 1.5
            
            opening_sentence = re.split(r'[.!?]', opening)[0].strip()
            ending_sentence = re.split(r'[.!?]', ending)[-2].strip() if len(re.split(r'[.!?]', ending)) > 1 else ending.strip()
            
            hooks_and_cliffhangers.append({
                'chapter': chapter['number'],
                'opening_hook_score': opening_score,
                'closing_cliffhanger_score': ending_score,
                'opening_sentence': opening_sentence[:150],
                'closing_sentence': ending_sentence[:150],
                'has_strong_hook': opening_score > 3,
                'has_cliffhanger': ending_score > 4
            })
        
        return hooks_and_cliffhangers
    
    def analyze_structure_patterns(self):
        """Analyze overall structural patterns"""
        chapter_lengths = [ch['word_count'] for ch in self.chapters]
        
        avg_length = np.mean(chapter_lengths)
        std_length = np.std(chapter_lengths)
        
        short_chapters = [ch for ch in self.chapters if ch['word_count'] < avg_length - std_length]
        long_chapters = [ch for ch in self.chapters if ch['word_count'] > avg_length + std_length]
        
        consistency_score = 1 - (std_length / avg_length) if avg_length > 0 else 0
        
        scene_counts = Counter(scene['chapter'] for scene in self.scenes)
        avg_scenes_per_chapter = np.mean(list(scene_counts.values()))
        
        structure_type = 'unknown'
        if consistency_score > 0.7:
            structure_type = 'consistent'
        elif len(short_chapters) > len(self.chapters) * 0.3:
            structure_type = 'varied_with_short_interludes'
        elif std_length > avg_length * 0.5:
            structure_type = 'highly_varied'
        else:
            structure_type = 'moderately_varied'
        
        return {
            'avg_chapter_length': avg_length,
            'chapter_length_std': std_length,
            'consistency_score': consistency_score,
            'structure_type': structure_type,
            'short_chapters': [ch['number'] for ch in short_chapters],
            'long_chapters': [ch['number'] for ch in long_chapters],
            'avg_scenes_per_chapter': avg_scenes_per_chapter,
            'total_scenes': len(self.scenes)
        }
    
    def create_visualizations(self, output_dir='analysis_output'):
        """Create structural analysis visualizations"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'Structural Analysis: {self.file_path.name}', fontsize=16)
        
        chapters = [ch['number'] for ch in self.chapters]
        lengths = [ch['word_count'] for ch in self.chapters]
        
        axes[0, 0].bar(chapters, lengths, color='steelblue')
        axes[0, 0].axhline(y=np.mean(lengths), color='red', linestyle='--', label='Average')
        axes[0, 0].set_xlabel('Chapter')
        axes[0, 0].set_ylabel('Word Count')
        axes[0, 0].set_title('Chapter Lengths')
        axes[0, 0].legend()
        
        scene_counts = Counter(scene['chapter'] for scene in self.scenes)
        scene_chapters = list(scene_counts.keys())
        scene_nums = list(scene_counts.values())
        axes[0, 1].bar(scene_chapters, scene_nums, color='forestgreen')
        axes[0, 1].set_xlabel('Chapter')
        axes[0, 1].set_ylabel('Number of Scenes')
        axes[0, 1].set_title('Scenes per Chapter')
        
        plot_arc = self.analyze_plot_arc()
        intensities = [p['intensity_score'] for p in plot_arc['progression']]
        axes[0, 2].plot(chapters, intensities, color='darkred', linewidth=2, marker='o')
        if plot_arc['potential_climax']:
            axes[0, 2].axvline(x=plot_arc['potential_climax'], color='red', 
                              linestyle=':', label='Potential Climax')
        axes[0, 2].set_xlabel('Chapter')
        axes[0, 2].set_ylabel('Intensity Score')
        axes[0, 2].set_title('Plot Intensity Arc')
        axes[0, 2].legend()
        
        tensions = [p['tension_density'] for p in plot_arc['progression']]
        resolutions = [p['resolution_density'] for p in plot_arc['progression']]
        axes[1, 0].plot(chapters, tensions, label='Tension', color='red', alpha=0.7)
        axes[1, 0].plot(chapters, resolutions, label='Resolution', color='green', alpha=0.7)
        axes[1, 0].fill_between(chapters, tensions, alpha=0.3, color='red')
        axes[1, 0].fill_between(chapters, resolutions, alpha=0.3, color='green')
        axes[1, 0].set_xlabel('Chapter')
        axes[1, 0].set_ylabel('Density %')
        axes[1, 0].set_title('Tension vs Resolution')
        axes[1, 0].legend()
        
        hooks_data = self.detect_hooks_and_cliffhangers()
        hook_scores = [h['opening_hook_score'] for h in hooks_data]
        cliff_scores = [h['closing_cliffhanger_score'] for h in hooks_data]
        
        x = np.arange(len(chapters))
        width = 0.35
        axes[1, 1].bar(x - width/2, hook_scores, width, label='Opening Hooks', color='purple')
        axes[1, 1].bar(x + width/2, cliff_scores, width, label='Cliffhangers', color='orange')
        axes[1, 1].set_xlabel('Chapter')
        axes[1, 1].set_ylabel('Score')
        axes[1, 1].set_title('Hooks and Cliffhangers')
        axes[1, 1].set_xticks(x[::2])
        axes[1, 1].set_xticklabels(chapters[::2])
        axes[1, 1].legend()
        
        timeline_data = self.analyze_timeline()
        time_refs = [t['total_time_references'] for t in timeline_data['timeline']]
        axes[1, 2].plot(chapters, time_refs, marker='s', color='navy', linewidth=2)
        axes[1, 2].set_xlabel('Chapter')
        axes[1, 2].set_ylabel('Temporal References')
        axes[1, 2].set_title('Timeline Complexity')
        
        for shift in timeline_data['temporal_shifts']:
            if shift['type'] == 'flashback':
                axes[1, 2].scatter(shift['chapter'], time_refs[shift['chapter']-1], 
                                 color='red', s=100, marker='v', label='Flashback' if shift == timeline_data['temporal_shifts'][0] else '')
            else:
                axes[1, 2].scatter(shift['chapter'], time_refs[shift['chapter']-1], 
                                 color='blue', s=100, marker='^', label='Flashforward' if shift == timeline_data['temporal_shifts'][0] else '')
        
        plt.tight_layout()
        plt.savefig(output_path / 'structural_analysis_charts.png', dpi=150, bbox_inches='tight')
        print(f"✓ Saved visualizations to {output_path / 'structural_analysis_charts.png'}")
        plt.close()
    
    def generate_report(self):
        """Generate comprehensive structural analysis report"""
        print("\n" + "="*60)
        print("STRUCTURAL ANALYSIS REPORT")
        print("="*60)
        
        self.load_text()
        self.detect_chapters()
        self.detect_scenes()
        
        print("\n📚 CHAPTER STRUCTURE")
        print("-"*40)
        structure_patterns = self.analyze_structure_patterns()
        print(f"  Total chapters: {len(self.chapters)}")
        print(f"  Average length: {structure_patterns['avg_chapter_length']:,.0f} words")
        print(f"  Structure type: {structure_patterns['structure_type'].replace('_', ' ').title()}")
        print(f"  Consistency score: {structure_patterns['consistency_score']:.2f}")
        
        if structure_patterns['short_chapters']:
            print(f"  Short chapters: {structure_patterns['short_chapters'][:5]}")
        if structure_patterns['long_chapters']:
            print(f"  Long chapters: {structure_patterns['long_chapters'][:5]}")
        
        print("\n🎬 SCENE BREAKDOWN")
        print("-"*40)
        print(f"  Total scenes: {structure_patterns['total_scenes']}")
        print(f"  Average scenes per chapter: {structure_patterns['avg_scenes_per_chapter']:.1f}")
        
        scene_counts = Counter(scene['chapter'] for scene in self.scenes)
        most_scenes = max(scene_counts.items(), key=lambda x: x[1]) if scene_counts else (0, 0)
        print(f"  Most scenes in chapter: {most_scenes[0]} ({most_scenes[1]} scenes)")
        
        print("\n👁️ POV ANALYSIS")
        print("-"*40)
        pov_data = self.detect_pov_shifts()
        pov_types = Counter(ch['dominant_pov'] for ch in pov_data['chapter_pov'])
        dominant_pov = max(pov_types.items(), key=lambda x: x[1])[0] if pov_types else 'unclear'
        print(f"  Dominant POV: {dominant_pov.replace('_', ' ').title()}")
        
        if pov_data['pov_shifts']:
            print(f"  POV shifts detected: {len(pov_data['pov_shifts'])}")
            for shift in pov_data['pov_shifts'][:3]:
                print(f"    • Chapter {shift['from_chapter']} → {shift['to_chapter']}: "
                      f"{shift['from_pov']} → {shift['to_pov']}")
        else:
            print("  No significant POV shifts detected")
        
        print("\n📈 PLOT ARC ANALYSIS")
        print("-"*40)
        plot_arc = self.analyze_plot_arc()
        if plot_arc['potential_climax']:
            print(f"  Potential climax: Chapter {plot_arc['potential_climax']}")
        
        print(f"  Highest intensity chapters:")
        for candidate in plot_arc['climax_candidates'][:3]:
            print(f"    • Chapter {candidate['chapter']}: intensity {candidate['intensity_score']:.2f}")
        
        avg_tension = np.mean([p['tension_density'] for p in plot_arc['progression']])
        avg_resolution = np.mean([p['resolution_density'] for p in plot_arc['progression']])
        print(f"  Average tension density: {avg_tension:.2f}%")
        print(f"  Average resolution density: {avg_resolution:.2f}%")
        
        print("\n⏰ TIMELINE ANALYSIS")
        print("-"*40)
        timeline_data = self.analyze_timeline()
        total_time_refs = sum(t['total_time_references'] for t in timeline_data['timeline'])
        print(f"  Total temporal references: {total_time_refs}")
        
        if timeline_data['temporal_shifts']:
            flashbacks = [s for s in timeline_data['temporal_shifts'] if s['type'] == 'flashback']
            flashforwards = [s for s in timeline_data['temporal_shifts'] if s['type'] == 'flashforward']
            
            if flashbacks:
                print(f"  Flashback chapters: {[f['chapter'] for f in flashbacks][:5]}")
            if flashforwards:
                print(f"  Flashforward chapters: {[f['chapter'] for f in flashforwards][:5]}")
        
        print("\n🎣 HOOKS & CLIFFHANGERS")
        print("-"*40)
        hooks_data = self.detect_hooks_and_cliffhangers()
        strong_hooks = [h for h in hooks_data if h['has_strong_hook']]
        cliffhangers = [h for h in hooks_data if h['has_cliffhanger']]
        
        print(f"  Chapters with strong hooks: {len(strong_hooks)}")
        print(f"  Chapters with cliffhangers: {len(cliffhangers)}")
        
        if cliffhangers:
            print(f"  Strongest cliffhangers:")
            top_cliffs = sorted(cliffhangers, key=lambda x: x['closing_cliffhanger_score'], reverse=True)[:3]
            for cliff in top_cliffs:
                print(f"    • Chapter {cliff['chapter']} (score: {cliff['closing_cliffhanger_score']:.1f})")
        
        self.create_visualizations()
        
        output_path = Path('analysis_output')
        output_path.mkdir(exist_ok=True)
        
        full_report = {
            'file': str(self.file_path),
            'structure': {
                'total_chapters': len(self.chapters),
                'chapter_details': [
                    {
                        'number': ch['number'],
                        'title': ch['title'],
                        'word_count': ch['word_count'],
                        'type': ch['type']
                    } for ch in self.chapters
                ],
                'patterns': structure_patterns
            },
            'scenes': {
                'total': len(self.scenes),
                'by_chapter': dict(Counter(scene['chapter'] for scene in self.scenes))
            },
            'pov': pov_data,
            'plot_arc': {
                'potential_climax': plot_arc['potential_climax'],
                'progression': plot_arc['progression']
            },
            'timeline': timeline_data,
            'hooks_and_cliffhangers': hooks_data
        }
        
        with open(output_path / 'structural_analysis_report.json', 'w') as f:
            json.dump(full_report, f, indent=2, default=str)
        
        print(f"\n✓ Full report saved to {output_path / 'structural_analysis_report.json'}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Analyze book structure')
    parser.add_argument('file', help='Path to the book text file')
    parser.add_argument('--chapters', action='store_true',
                       help='Show detailed chapter analysis')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    analyzer = StructuralAnalyzer(args.file)
    analyzer.generate_report()


if __name__ == '__main__':
    main()