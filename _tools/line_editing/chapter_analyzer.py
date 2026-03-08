import re
import json
import sys
import argparse

class ManuscriptAnalyzer:
    def __init__(self, manuscript_path):
        with open(manuscript_path, 'r', encoding='utf-8') as f:
            self.full_text = f.read()
        self.chapters = self._extract_chapters()
    
    def _extract_chapters(self):
        chapter_pattern = r'CHAPTER (\d+)'
        splits = re.split(chapter_pattern, self.full_text)
        
        chapters = {}
        for i in range(1, len(splits), 2):
            chapter_num = int(splits[i])
            chapter_text = splits[i+1].strip()
            chapters[chapter_num] = chapter_text
        return chapters
    
    def get_chapter(self, num):
        return self.chapters.get(num, "Chapter not found")
    
    def extract_characters(self, chapter_text):
        """Extract character names (capitalized words that appear multiple times or in dialogue attribution)"""
        characters = set()
        
        # Common English words to exclude
        common_words = {
            'The', 'A', 'An', 'But', 'And', 'Or', 'If', 'When', 'Where', 'Why', 'How', 
            'Chapter', 'He', 'She', 'It', 'They', 'We', 'You', 'I', 'Me', 'My', 'His', 
            'Her', 'Their', 'Our', 'Your', 'This', 'That', 'These', 'Those', 'What', 
            'Who', 'Which', 'Some', 'Any', 'All', 'Most', 'Many', 'Few', 'Several', 
            'Each', 'Every', 'Either', 'Neither', 'Both', 'One', 'Two', 'Three', 'Four', 
            'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'First', 'Second', 'Third', 
            'Last', 'Next', 'New', 'Old', 'Good', 'Bad', 'Great', 'Small', 'Large', 
            'Long', 'Short', 'High', 'Low', 'Early', 'Late', 'Yes', 'No', 'Not', 'Now', 
            'Then', 'Here', 'There', 'Where', 'Why', 'How', 'Because', 'Since', 'After', 
            'Before', 'During', 'Through', 'Above', 'Below', 'Between', 'Under', 'Over',
            'Just', 'Only', 'Also', 'Still', 'Even', 'Well', 'Much', 'Very', 'Too',
            'So', 'As', 'For', 'With', 'Without', 'About', 'Into', 'From', 'By', 'In',
            'On', 'At', 'To', 'Of', 'Up', 'Down', 'Out', 'Off', 'Can', 'Could', 'Would',
            'Should', 'Will', 'May', 'Might', 'Must', 'Shall', 'Do', 'Does', 'Did',
            'Have', 'Has', 'Had', 'Is', 'Are', 'Was', 'Were', 'Be', 'Been', 'Being',
            'Today', 'Yesterday', 'Tomorrow', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday', 'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
            'Inside', 'Outside', 'England', 'America', 'Europe', 'Asia', 'Africa',
            'North', 'South', 'East', 'West', 'Northern', 'Southern', 'Eastern', 'Western',
            'Mr', 'Mrs', 'Ms', 'Dr', 'Professor', 'Captain', 'Lord', 'Lady', 'Sir',
            'Dynamics', 'Corporation', 'Company', 'Institute', 'University', 'Department'
        }
        
        # Find names in dialogue attribution (said, asked, etc.)
        dialogue_pattern = r'([A-Z][a-z]+)(?:\s+said|\s+asked|\s+whispered|\s+shouted|\s+replied|\s+answered|\s+thought|\s+wondered|\s+realized|\s+knew|\s+felt|\'s\s+)'
        matches = re.findall(dialogue_pattern, chapter_text)
        for match in matches:
            if match not in common_words:
                characters.add(match)
        
        # Find potential character names (proper nouns that appear multiple times)
        # Look for capitalized words, including compounds like "Mary Jane"
        name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
        potential_names = re.findall(name_pattern, chapter_text)
        
        # Count occurrences
        name_counts = {}
        for name in potential_names:
            if name not in common_words:
                name_counts[name] = name_counts.get(name, 0) + 1
        
        # Add names that appear 4+ times (raised threshold)
        for name, count in name_counts.items():
            if count >= 4:
                # Additional check: is it followed by action verbs?
                action_check = re.search(rf'\b{name}\s+(walked|ran|sat|stood|looked|turned|smiled|frowned|nodded|shook|reached|grabbed|held|took|gave|went|came|entered|left|stayed|moved|stopped|started|continued|began|ended)', chapter_text)
                if action_check or count >= 6:  # If followed by action verb OR appears 6+ times
                    characters.add(name)
        
        # Special patterns for names with titles
        title_pattern = r'\b(?:Mr\.|Mrs\.|Ms\.|Dr\.|Professor|Captain|Lord|Lady|Sir)\s+([A-Z][a-z]+)\b'
        title_matches = re.findall(title_pattern, chapter_text)
        characters.update(title_matches)
        
        return sorted(list(characters))
    
    def extract_numbers(self, chapter_text):
        """Extract all numbers and measurements from the text"""
        numbers = {}
        
        # Extract time references
        time_pattern = r'\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap]\.?[Mm]\.?)?'
        times = re.findall(time_pattern, chapter_text)
        if times:
            numbers['times'] = times
        
        # Extract years
        year_pattern = r'\b(19\d{2}|20\d{2}|2\d{3})\b'
        years = re.findall(year_pattern, chapter_text)
        if years:
            numbers['years'] = years
        
        # Extract percentages
        percent_pattern = r'\d+(?:\.\d+)?%'
        percentages = re.findall(percent_pattern, chapter_text)
        if percentages:
            numbers['percentages'] = percentages
        
        # Extract general numbers with context
        num_context_pattern = r'(\w+\s+)?(\d+(?:,\d{3})*(?:\.\d+)?)\s+(\w+)'
        num_contexts = re.findall(num_context_pattern, chapter_text)
        if num_contexts:
            numbers['measurements'] = [f"{ctx[0]}{ctx[1]} {ctx[2]}".strip() for ctx in num_contexts][:10]
        
        # Extract standalone numbers
        standalone_pattern = r'\b\d+(?:\.\d+)?\b'
        standalone = re.findall(standalone_pattern, chapter_text)
        if standalone:
            numbers['standalone'] = list(set(standalone))[:10]
        
        return numbers
    
    def extract_locations(self, chapter_text):
        """Extract location references"""
        locations = []
        
        # Common location indicators
        location_patterns = [
            r'(?:in|at|to|from|near|outside|inside|beneath|above|behind)\s+(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Street|Avenue|Road|Boulevard|Building|Tower|Office|Room|Floor)',
            r'(?:the\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:office|kitchen|bedroom|bathroom|hallway|lobby|penthouse)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, chapter_text, re.IGNORECASE)
            locations.extend([m for m in matches if len(m) > 2])
        
        # Remove duplicates and limit
        locations = sorted(list(set(locations)))[:15]
        return locations
    
    def extract_plot_points(self, chapter_text):
        """Extract key plot points based on action words and sentence structure"""
        plot_points = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', chapter_text)
        
        # Action indicators
        action_words = ['realized', 'discovered', 'found', 'saw', 'heard', 'felt', 'knew', 'understood',
                       'opened', 'closed', 'arrived', 'left', 'died', 'lived', 'appeared', 'disappeared',
                       'remembered', 'forgot', 'broke', 'fixed', 'created', 'destroyed', 'began', 'ended',
                       'attacked', 'defended', 'escaped', 'caught', 'revealed', 'hid', 'connected', 'separated']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:
                for action in action_words:
                    if action in sentence.lower():
                        plot_points.append(sentence)
                        break
        
        return plot_points[:10]
    
    def extract_dialogue_snippets(self, chapter_text):
        """Extract key dialogue moments"""
        dialogue_pattern = r'"([^"]+)"'
        dialogues = re.findall(dialogue_pattern, chapter_text)
        
        # Filter for significant dialogue
        significant = [d for d in dialogues if 10 < len(d) < 150]
        
        return significant[:10]
    
    def analyze_chapter_details(self, chapter_num):
        """Comprehensive detail extraction for a chapter"""
        chapter_text = self.get_chapter(chapter_num)
        
        return {
            "chapter_number": chapter_num,
            "word_count": len(chapter_text.split()),
            "characters": self.extract_characters(chapter_text),
            "numbers": self.extract_numbers(chapter_text),
            "locations": self.extract_locations(chapter_text),
            "plot_points": self.extract_plot_points(chapter_text),
            "key_dialogue": self.extract_dialogue_snippets(chapter_text),
            "first_paragraph": chapter_text[:500] if chapter_text else "",
            "last_paragraph": chapter_text[-500:] if chapter_text else ""
        }
    
    def analyze_chapter_flow(self, ch1, ch2):
        """Analyze flow between two chapters"""
        ch1_end = self.get_chapter(ch1)[-500:]
        ch2_start = self.get_chapter(ch2)[:500]
        
        return {
            "chapter_1_ends": ch1_end,
            "chapter_2_begins": ch2_start,
            "analysis_prompt": f"Analyze flow from Ch{ch1} to Ch{ch2} based on these specific excerpts"
        }
    
    def create_analysis_file(self, chapter_num, format='json'):
        """Create basic analysis file for a chapter"""
        chapter_text = self.get_chapter(chapter_num)
        
        output = {
            "chapter_number": chapter_num,
            "full_text": chapter_text,
            "word_count": len(chapter_text.split()),
            "first_paragraph": chapter_text[:500],
            "last_paragraph": chapter_text[-500:],
            "instruction": "Analyze ONLY this exact text. Do not reference other chapters from memory."
        }
        
        if format == 'json':
            with open(f'chapter_{chapter_num}_analysis.json', 'w') as f:
                json.dump(output, f, indent=2)
        elif format == 'md':
            self._write_markdown_analysis(chapter_num, output)
    
    def _write_markdown_analysis(self, chapter_num, data):
        with open(f'chapter_{chapter_num}_analysis.md', 'w') as f:
            f.write(f"# Chapter {chapter_num} Analysis\n\n")
            f.write(f"**Word Count:** {data['word_count']}\n\n")
            f.write("---\n\n")
            f.write("## Analysis Instructions\n\n")
            f.write(f"{data['instruction']}\n\n")
            f.write("---\n\n")
            f.write("## First Paragraph (First 500 characters)\n\n")
            f.write(f"{data['first_paragraph']}\n\n")
            f.write("---\n\n")
            f.write("## Last Paragraph (Last 500 characters)\n\n")
            f.write(f"{data['last_paragraph']}\n\n")
            f.write("---\n\n")
            f.write("## Full Chapter Text\n\n")
            f.write(data['full_text'])
    
    def create_flow_analysis_file(self, ch1, ch2, format='json'):
        flow_data = self.analyze_chapter_flow(ch1, ch2)
        
        if format == 'json':
            with open(f'chapter_{ch1}_to_{ch2}_flow.json', 'w') as f:
                json.dump(flow_data, f, indent=2)
        elif format == 'md':
            with open(f'chapter_{ch1}_to_{ch2}_flow.md', 'w') as f:
                f.write(f"# Chapter {ch1} to Chapter {ch2} Flow Analysis\n\n")
                f.write(f"## {flow_data['analysis_prompt']}\n\n")
                f.write("---\n\n")
                f.write(f"### Chapter {ch1} Ends With:\n\n")
                f.write(f"{flow_data['chapter_1_ends']}\n\n")
                f.write("---\n\n")
                f.write(f"### Chapter {ch2} Begins With:\n\n")
                f.write(f"{flow_data['chapter_2_begins']}\n\n")
    
    def create_consistency_report(self, chapter_nums, format='md'):
        """Create a detailed consistency report for specified chapters"""
        reports = {}
        for num in chapter_nums:
            reports[num] = self.analyze_chapter_details(num)
        
        if format == 'json':
            filename = f'chapters_{"_".join(map(str, chapter_nums))}_consistency.json'
            with open(filename, 'w') as f:
                json.dump(reports, f, indent=2)
            return filename
        
        elif format == 'md':
            filename = f'chapters_{"_".join(map(str, chapter_nums))}_consistency.md'
            with open(filename, 'w') as f:
                f.write(f"# Consistency Report: Chapters {', '.join(map(str, chapter_nums))}\n\n")
                
                for num, details in reports.items():
                    f.write(f"## Chapter {num}\n\n")
                    f.write(f"**Word Count:** {details['word_count']}\n\n")
                    
                    f.write("### Characters\n")
                    if details['characters']:
                        for char in details['characters']:
                            f.write(f"- {char}\n")
                    else:
                        f.write("- No named characters identified\n")
                    f.write("\n")
                    
                    f.write("### Numbers & Measurements\n")
                    if details['numbers']:
                        for category, values in details['numbers'].items():
                            f.write(f"**{category.title()}:**\n")
                            for val in values:
                                f.write(f"- {val}\n")
                        f.write("\n")
                    else:
                        f.write("- No specific numbers found\n\n")
                    
                    f.write("### Locations\n")
                    if details['locations']:
                        for loc in details['locations']:
                            f.write(f"- {loc}\n")
                    else:
                        f.write("- No specific locations identified\n")
                    f.write("\n")
                    
                    f.write("### Key Plot Points\n")
                    if details['plot_points']:
                        for i, point in enumerate(details['plot_points'], 1):
                            f.write(f"{i}. {point}\n")
                    else:
                        f.write("- No significant plot points extracted\n")
                    f.write("\n")
                    
                    f.write("### Key Dialogue\n")
                    if details['key_dialogue']:
                        for dialogue in details['key_dialogue'][:5]:
                            f.write(f'> "{dialogue}"\n\n')
                    else:
                        f.write("- No dialogue found\n\n")
                    
                    f.write("---\n\n")
                
                # Cross-chapter analysis
                f.write("## Cross-Chapter Consistency Analysis\n\n")
                
                # Character appearances
                f.write("### Character Appearances\n")
                all_chars = {}
                for num, details in reports.items():
                    for char in details['characters']:
                        if char not in all_chars:
                            all_chars[char] = []
                        all_chars[char].append(num)
                
                for char, chapters in sorted(all_chars.items()):
                    f.write(f"- **{char}**: Appears in chapters {', '.join(map(str, chapters))}\n")
                f.write("\n")
                
                # Recurring numbers
                f.write("### Recurring Numbers/Times\n")
                all_numbers = {}
                for num, details in reports.items():
                    if 'times' in details['numbers']:
                        for time in details['numbers']['times']:
                            if time not in all_numbers:
                                all_numbers[time] = []
                            all_numbers[time].append(num)
                
                recurring = False
                for number, chapters in sorted(all_numbers.items()):
                    if len(chapters) > 1:
                        f.write(f"- **{number}**: Appears in chapters {', '.join(map(str, chapters))}\n")
                        recurring = True
                
                if not recurring:
                    f.write("- No recurring times/numbers found across chapters\n")
                
            return filename

def main():
    parser = argparse.ArgumentParser(description='Analyze manuscript chapters for consistency and details')
    parser.add_argument('manuscript', nargs='?', default='/home/josephsong15/editor/remanence-2025-08-04T04_08_43.txt',
                        help='Path to manuscript file')
    parser.add_argument('--chapters', '-c', nargs='+', type=int,
                        help='Chapter numbers to analyze (e.g., -c 1 2 3)')
    parser.add_argument('--mode', '-m', choices=['basic', 'flow', 'consistency', 'all'], default='all',
                        help='Analysis mode: basic, flow, consistency, or all')
    parser.add_argument('--format', '-f', choices=['json', 'md'], default='md',
                        help='Output format: json or md')
    
    args = parser.parse_args()
    
    try:
        analyzer = ManuscriptAnalyzer(args.manuscript)
        print(f"Loaded manuscript with {len(analyzer.chapters)} chapters")
        print(f"Available chapters: {sorted(analyzer.chapters.keys())}\n")
        
        # Default to chapters 1 and 2 if not specified
        chapters = args.chapters if args.chapters else [1, 2]
        
        if args.mode in ['basic', 'all']:
            print(f"Creating basic analysis for chapters {chapters}...")
            for ch in chapters:
                analyzer.create_analysis_file(ch, format=args.format)
                print(f"✓ Created chapter_{ch}_analysis.{args.format}")
            print()
        
        if args.mode in ['flow', 'all'] and len(chapters) >= 2:
            print("Creating flow analysis...")
            for i in range(len(chapters)-1):
                analyzer.create_flow_analysis_file(chapters[i], chapters[i+1], format=args.format)
                print(f"✓ Created chapter_{chapters[i]}_to_{chapters[i+1]}_flow.{args.format}")
            print()
        
        if args.mode in ['consistency', 'all']:
            print(f"Creating consistency report for chapters {chapters}...")
            filename = analyzer.create_consistency_report(chapters, format=args.format)
            print(f"✓ Created {filename}")
            
            # Print summary
            print("\nChapter Summaries:")
            for ch in chapters:
                details = analyzer.analyze_chapter_details(ch)
                print(f"  Chapter {ch}:")
                print(f"    - Word count: {details['word_count']}")
                print(f"    - Characters: {len(details['characters'])}")
                print(f"    - Locations: {len(details['locations'])}")
                print(f"    - Plot points: {len(details['plot_points'])}")
                print(f"    - Dialogues: {len(details['key_dialogue'])}")
        
    except FileNotFoundError:
        print(f"Error: Could not find manuscript file: {args.manuscript}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()