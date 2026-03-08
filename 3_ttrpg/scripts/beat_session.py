#!/usr/bin/env python3
"""
Beat Sheet Session
Generate story beats (no prose) for scene planning
"""

import sys
import os
import argparse

# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
os.chdir(script_dir)

from core.book3_context import Book3Context
from core.beat_sheet_generator import BeatSheetGenerator


class BeatSession:
    """Generate beat sheets for story planning"""

    def __init__(self):
        self.book3 = Book3Context()
        self.beat_gen = BeatSheetGenerator(self.book3)
        self.history = []

        if self.book3.active:
            print(f"[Book 3 Context Loaded - Act: {self.book3.get_current_act()}]")
        else:
            print("[No Book 3 context found - using generic mode]")

    def process_prompt(self, prompt: str) -> str:
        """Process a story prompt and generate beat sheet"""
        # Parse prompt
        parsed = self._parse_prompt(prompt)

        # Determine scene type
        scene_type = self._determine_scene_type(parsed)

        # Extract characters
        characters = self._extract_characters(parsed)

        # Build context
        context = {
            'location': parsed.get('location', 'unspecified'),
            'tension': parsed.get('tension', 'moderate'),
            'user_intent': prompt
        }

        # Generate beat sheet
        beat_sheet = self.beat_gen.generate_beat_sheet(
            prompt, scene_type, characters, context
        )

        # Store in history
        self.history.append({
            'prompt': prompt,
            'beat_sheet': beat_sheet
        })

        # Format and return
        return self.beat_gen.format_beat_sheet(beat_sheet)

    def _parse_prompt(self, prompt: str) -> dict:
        """Parse user prompt to extract key information"""
        parsed = {
            'raw': prompt,
            'characters': [],
            'action': None,
            'location': None,
            'tension': 'moderate'
        }

        # Detect characters
        char_names = {
            'ahdia': 'ahdia_bacchus',
            'ruth': 'ruth_carter',
            'ben': 'ben_bukowski',
            'victor': 'victor_hernandez',
            'leah': 'leah_turner',
            'tess': 'tess_whitford',
            'faeris': 'faeris_drone',
            'korede': 'korede_owolowo',
            'ryu': 'ryu_tanaka',
            'tanaka': 'ryu_tanaka',
            'bourn': 'harriet_bourn',
            'harriet': 'harriet_bourn',
            'kain': 'president_kain',
            'prime': 'ahdia_prime',
            'diana': 'ahdia_prime',
            'jericho': 'rahs_jericho',
            'bellatrix': 'bellatrix',
            'eidolon': 'eidolon',
            'mother': 'mother_faeris'
        }

        for name, char_id in char_names.items():
            if name.lower() in prompt.lower():
                if char_id not in parsed['characters']:
                    parsed['characters'].append(char_id)

        # Detect action keywords (order matters - check specific before general)
        if any(word in prompt.lower() for word in ['flashback', 'montage', 'memory', 'recalls', 'remembers', 'origin', 'witness', 'perceives']):
            parsed['action'] = 'narrative'
        elif any(word in prompt.lower() for word in ['training', 'practice', 'drill', 'exercise', 'spar', 'workout']):
            parsed['action'] = 'narrative'  # Training montage is narrative
        elif any(word in prompt.lower() for word in ['meet', 'face to face', 'explains', 'reveals', 'tells', 'learns', 'confronts', 'gives', 'confesses', 'admits']):
            parsed['action'] = 'revelation'
        elif any(word in prompt.lower() for word in ['infiltrate', 'investigate', 'search', 'examine', 'look', 'find', 'discover']):
            parsed['action'] = 'investigation'
        elif any(word in prompt.lower() for word in ['fight', 'attack', 'combat', 'battle', 'defend', 'seize', 'evacuate', 'escape', 'raid']):
            parsed['action'] = 'combat'
        elif any(word in prompt.lower() for word in ['talk', 'negotiate', 'convince', 'persuade', 'argue', 'discuss']):
            parsed['action'] = 'social'
        elif any(word in prompt.lower() for word in ['temporal manipulation', 'time freeze', 'rewind time']):  # More specific
            parsed['action'] = 'temporal'

        # Detect locations
        if any(word in prompt.lower() for word in ['apartment', 'ahdia\'s apartment']):
            parsed['location'] = "Ahdia's apartment"
        elif any(word in prompt.lower() for word in ['lab', 'laboratory']):
            parsed['location'] = "Laboratory"
        elif any(word in prompt.lower() for word in ['cadens', 'facility']):
            parsed['location'] = 'CADENS facility'
        elif any(word in prompt.lower() for word in ['warehouse', 'abandoned']):
            parsed['location'] = 'Abandoned warehouse'
        elif any(word in prompt.lower() for word in ['rooftop', 'roof']):
            parsed['location'] = 'Rooftop'

        # Detect tension
        if any(word in prompt.lower() for word in ['urgent', 'emergency', 'crisis', 'desperate']):
            parsed['tension'] = 'high'
        elif any(word in prompt.lower() for word in ['careful', 'cautious', 'quiet', 'stealth']):
            parsed['tension'] = 'low'

        return parsed

    def _determine_scene_type(self, parsed: dict) -> str:
        """Determine scene type from parsed prompt"""
        if parsed.get('action'):
            return parsed['action']
        return 'generic'

    def _extract_characters(self, parsed: dict) -> list:
        """Extract character list"""
        chars = parsed.get('characters', [])
        if not chars:
            chars = ['ahdia_bacchus']  # Default
        return chars

    def get_context_summary(self) -> str:
        """Get summary of current Book 3 context"""
        if not self.book3.active:
            return "No Book 3 context loaded"

        lines = []
        lines.append("="*70)
        lines.append("BOOK 3 CONTEXT SUMMARY")
        lines.append("="*70)
        lines.append(f"Current Act: {self.book3.get_current_act().title()}")
        lines.append("")

        lines.append("Key Plot States:")
        lines.append(f"  - FAERIS Network: {self.book3.get_plot_state('faeris_network')}")
        lines.append(f"  - Mother FAERIS: {self.book3.get_plot_state('mother_faeris')}")
        lines.append(f"  - Kain: {self.book3.get_plot_state('kain_status')}")
        lines.append(f"  - CADENS: {self.book3.get_plot_state('cadens_control')}")
        lines.append(f"  - Artificial Sun: {self.book3.get_plot_state('artificial_sun')}")
        lines.append("")

        lines.append("Key Character States:")
        lines.append(f"  - Ahdia: {self.book3.get_character_state('ahdia_bacchus').get('temporal_powers', 'unknown')} powers")
        lines.append(f"  - Diana: {self.book3.get_character_state('ahdia_prime').get('cover_identity', 'unknown')}")
        lines.append(f"  - Ryu knows about Mother: {self.book3.get_character_state('ryu_tanaka').get('knows_about_mother_faeris', False)}")
        lines.append("="*70)

        return '\n'.join(lines)

    def update_plot_state(self, element: str, new_state: str):
        """Update plot milestone"""
        if self.book3.active:
            self.book3.update_plot_state(element, new_state)
            print(f"[Updated: {element} → {new_state}]")
        else:
            print("[No Book 3 context to update]")

    def set_act(self, act: str):
        """Update current act"""
        if self.book3.active:
            self.book3.set_act(act)
            print(f"[Act set to: {act}]")
        else:
            print("[No Book 3 context to update]")


def main():
    parser = argparse.ArgumentParser(description='Generate beat sheets for Book 3 scenes')
    parser.add_argument('--prompt', type=str, help='Story prompt to generate beats for')
    parser.add_argument('--context', action='store_true', help='Show current Book 3 context')
    parser.add_argument('--update-plot', type=str, help='Update plot state (format: element=state)')
    parser.add_argument('--set-act', type=str, choices=['confidence', 'incomprehensible_challenge', 'collapse'],
                       help='Set current story act')

    args = parser.parse_args()

    session = BeatSession()

    if args.context:
        print(session.get_context_summary())
        return

    if args.update_plot:
        try:
            element, state = args.update_plot.split('=')
            session.update_plot_state(element.strip(), state.strip())
        except ValueError:
            print("Error: Format should be element=state (e.g., faeris_network=seized)")
        return

    if args.set_act:
        session.set_act(args.set_act)
        return

    if args.prompt:
        result = session.process_prompt(args.prompt)
        print(result)
    else:
        print("Usage: python3 beat_session.py --prompt 'Your story prompt here'")
        print("       python3 beat_session.py --context")
        print("       python3 beat_session.py --update-plot element=state")
        print("       python3 beat_session.py --set-act confidence")


if __name__ == '__main__':
    main()
