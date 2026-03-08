#!/usr/bin/env python3
"""
Go Squad Perspective Engine
===========================
Parses CHARACTER_STATE_INDEX.yaml and provides query interface for
character states, knowledge tracking, relationships, and overlap detection.

Usage:
    from engine import PerspectiveEngine
    engine = PerspectiveEngine()
    engine.load()

    # Query examples
    engine.what_does_character_know('tess', 12)
    engine.who_is_present_at_event('ch21_leta_death')
    engine.find_overlaps(['ahdia', 'ruth', 'tess'])
    engine.get_relationship_state('ahdia', 'ruth', 13)
    engine.secrets_active(8)
"""

import yaml
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict


@dataclass
class CharacterState:
    """Character state at a specific chapter"""
    character: str
    chapter: int
    location: str = ""
    emotional: str = ""
    physical: dict = field(default_factory=dict)
    knows: list = field(default_factory=list)
    learns: list = field(default_factory=list)
    doesnt_know: list = field(default_factory=list)
    believes: list = field(default_factory=list)
    relationships: dict = field(default_factory=dict)
    key_actions: list = field(default_factory=list)


@dataclass
class Event:
    """A story event with participants"""
    id: str
    chapter: int
    month: int
    event_type: str  # action, revelation, emotional
    title: str
    description: str = ""
    participants: dict = field(default_factory=dict)  # char -> {role, action, state_change}
    knowledge_changes: list = field(default_factory=list)
    relationship_changes: list = field(default_factory=list)
    secrets_involved: list = field(default_factory=list)


@dataclass
class Overlap:
    """A moment where multiple character arcs intersect"""
    chapter: int
    event_id: str
    title: str
    characters: list
    overlap_type: str  # action_ensemble, confrontation, tragedy, revelation
    stewards_needed: list
    knowledge_delta: dict = field(default_factory=dict)


class PerspectiveEngine:
    """
    Main engine for querying character perspectives through the story timeline.
    """

    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            # Auto-detect repo root
            current = Path(__file__).resolve()
            for parent in current.parents:
                if (parent / "GO_SQUAD_MANIFEST.yaml").exists():
                    repo_root = parent
                    break
            if repo_root is None:
                repo_root = Path("/workspaces/gosquad")

        self.repo_root = Path(repo_root)
        self.state_index_path = self.repo_root / "7_characters/arcs/CHARACTER_STATE_INDEX.yaml"
        self.timeline_data_path = self.repo_root / "5_story_bibles/book_2/threads/TIMELINE_DATA.js"

        # Loaded data
        self.raw_data = {}
        self.characters = {}
        self.timeline = {}
        self.canon_warnings = []
        self.knowledge_tracking = {}
        self.relationships = {}
        self.events = []

        # Derived indices
        self._chapter_participants = defaultdict(set)
        self._character_chapters = defaultdict(list)
        self._knowledge_by_chapter = defaultdict(lambda: defaultdict(set))
        self._overlaps = []

    def load(self) -> "PerspectiveEngine":
        """Load all data sources"""
        self._load_state_index()
        self._load_timeline_data()
        self._build_indices()
        return self

    def _load_state_index(self):
        """Load CHARACTER_STATE_INDEX.yaml"""
        if not self.state_index_path.exists():
            raise FileNotFoundError(f"State index not found: {self.state_index_path}")

        with open(self.state_index_path, 'r') as f:
            self.raw_data = yaml.safe_load(f)

        self.timeline = self.raw_data.get('timeline', {})
        self.canon_warnings = self.raw_data.get('canon_warnings', [])
        self.characters = self.raw_data.get('characters', {})
        self.knowledge_tracking = self.raw_data.get('knowledge_tracking', {})
        self.relationships = self.raw_data.get('relationships', {})

    def _load_timeline_data(self):
        """Load TIMELINE_DATA.js events"""
        if not self.timeline_data_path.exists():
            return

        with open(self.timeline_data_path, 'r') as f:
            content = f.read()

        # Extract eventsData object from JS
        import re
        match = re.search(r'const eventsData = (\{[\s\S]*?\n\});', content)
        if match:
            # Convert JS object to JSON (handle trailing commas, single quotes)
            js_obj = match.group(1)
            # Simple conversion - this works for the current format
            js_obj = re.sub(r"'([^']+)':", r'"\1":', js_obj)
            js_obj = re.sub(r": '([^']*)'", r': "\1"', js_obj)
            js_obj = re.sub(r",(\s*[}\]])", r"\1", js_obj)

            try:
                events_data = json.loads(js_obj)
                self._process_timeline_events(events_data)
            except json.JSONDecodeError:
                pass  # Fall back to YAML-only data

    def _process_timeline_events(self, events_data: dict):
        """Convert timeline events to Event objects"""
        for char_id, events in events_data.items():
            for event in events:
                # Check if event already exists (multiple characters in same event)
                event_id = f"ch{event['chapter']}_{char_id}_{event['id']}"

                self.events.append(Event(
                    id=event_id,
                    chapter=event['chapter'],
                    month=self._get_month(event['chapter']),
                    event_type=event.get('type', 'action'),
                    title=event.get('text', ''),
                    participants={char_id: {'role': 'actor', 'action': event.get('text', '')}}
                ))

    def _get_month(self, chapter: int) -> int:
        """Get month for a chapter"""
        ch_key = f"ch{chapter}"
        if ch_key in self.timeline:
            return self.timeline[ch_key].get('month', 1)
        return ((chapter - 1) // 2) + 1  # Approximate

    def _build_indices(self):
        """Build derived indices for fast queries"""
        # Build chapter participation index from character chapter_states
        for char_id, char_data in self.characters.items():
            chapter_states = char_data.get('chapter_states', {})
            for ch_key in chapter_states.keys():
                ch_num = int(ch_key.replace('ch', ''))
                self._chapter_participants[ch_num].add(char_id)
                self._character_chapters[char_id].append(ch_num)

            # Also index from threads
            threads = char_data.get('threads', {})
            for thread_name, thread_data in threads.items():
                chapters = thread_data.get('chapters', [])
                for ch in chapters:
                    self._chapter_participants[ch].add(char_id)
                    if ch not in self._character_chapters[char_id]:
                        self._character_chapters[char_id].append(ch)

        # Build knowledge index
        for secret_id, secret_data in self.knowledge_tracking.items():
            awareness = secret_data.get('awareness', {})
            for ch_key, knowers in awareness.items():
                ch_num = int(ch_key.replace('ch', ''))
                for char in knowers:
                    self._knowledge_by_chapter[ch_num][char].add(secret_id)

        # Detect overlaps
        self._detect_overlaps()

    def _detect_overlaps(self):
        """Detect chapters where multiple protagonist arcs intersect significantly"""
        protagonists = {'ahdia', 'ruth', 'tess', 'ben', 'leah', 'leta', 'victor', 'korede'}

        for chapter in range(1, 25):
            present = self._chapter_participants[chapter] & protagonists
            if len(present) >= 2:
                # Determine overlap type based on timeline events
                ch_key = f"ch{chapter}"
                event_name = self.timeline.get(ch_key, {}).get('event', '')

                overlap_type = 'action_ensemble'
                if 'exposed' in event_name or 'revealed' in event_name:
                    overlap_type = 'revelation'
                elif 'killed' in event_name or 'death' in event_name:
                    overlap_type = 'tragedy'
                elif 'confronts' in event_name or 'discovers' in event_name:
                    overlap_type = 'confrontation'

                # Determine which stewards are most needed
                stewards_needed = list(present)[:4]  # Top 4 most relevant

                self._overlaps.append(Overlap(
                    chapter=chapter,
                    event_id=ch_key,
                    title=event_name.replace('_', ' ').title(),
                    characters=list(present),
                    overlap_type=overlap_type,
                    stewards_needed=stewards_needed
                ))

    # ==========================================
    # QUERY INTERFACE
    # ==========================================

    def what_does_character_know(self, character: str, chapter: int) -> dict:
        """
        Returns complete knowledge state for character at chapter boundary.

        Returns:
            {
                'knows': [...],           # Things they definitely know
                'learns_this_chapter': [...],  # New knowledge this chapter
                'doesnt_know': [...],     # Explicitly unknown things
                'believes': [...],        # Beliefs (may be wrong)
                'secrets_aware_of': [...]  # Tracked secrets they know
            }
        """
        char_data = self.characters.get(character, {})
        ch_key = f"ch{chapter}"

        # Get chapter state if exists
        chapter_state = char_data.get('chapter_states', {}).get(ch_key, {})

        # Get secrets they know about
        secrets = list(self._knowledge_by_chapter[chapter].get(character, set()))

        # Accumulate knowledge from threads
        accumulated_knows = set()
        accumulated_learns = set()

        threads = char_data.get('threads', {})
        for thread_name, thread_data in threads.items():
            gates = thread_data.get('gates', {})
            for gate_ch, gate_data in gates.items():
                gate_num = int(gate_ch.replace('ch', ''))
                if gate_num <= chapter:
                    if 'knows' in gate_data:
                        knows = gate_data['knows']
                        if isinstance(knows, list):
                            accumulated_knows.update(knows)
                        else:
                            accumulated_knows.add(str(knows))
                    if 'learns' in gate_data:
                        learns = gate_data['learns']
                        if isinstance(learns, list):
                            if gate_num == chapter:
                                accumulated_learns.update(learns)
                            accumulated_knows.update(learns)
                        else:
                            if gate_num == chapter:
                                accumulated_learns.add(str(learns))
                            accumulated_knows.add(str(learns))

        return {
            'character': character,
            'chapter': chapter,
            'knows': list(accumulated_knows) + chapter_state.get('knows', []),
            'learns_this_chapter': list(accumulated_learns) + chapter_state.get('learns', []),
            'doesnt_know': chapter_state.get('doesnt_know', []),
            'believes': chapter_state.get('believes', []),
            'secrets_aware_of': secrets
        }

    def who_is_present(self, chapter: int) -> list:
        """Returns all characters active/present in a chapter"""
        return list(self._chapter_participants.get(chapter, set()))

    def find_overlaps(self, characters: Optional[list] = None) -> list[Overlap]:
        """
        Returns chapters where specified characters' arcs intersect.
        If no characters specified, returns all significant overlaps.
        """
        if characters is None:
            return self._overlaps

        char_set = set(characters)
        return [
            overlap for overlap in self._overlaps
            if char_set.issubset(set(overlap.characters))
        ]

    def get_relationship_state(self, char1: str, char2: str, chapter: int) -> dict:
        """Returns relationship state between two characters at chapter"""
        # Try both orderings
        rel_key = f"{char1}_{char2}"
        if rel_key not in self.relationships:
            rel_key = f"{char2}_{char1}"

        rel_data = self.relationships.get(rel_key, {})
        rel_type = rel_data.get('type', 'unknown')
        progression = rel_data.get('progression', {})

        # Find most recent state at or before chapter
        state = {'type': rel_type, 'state': 'unknown', 'notes': None}
        for ch_key in sorted(progression.keys(), key=lambda x: int(x.replace('ch', ''))):
            ch_num = int(ch_key.replace('ch', ''))
            if ch_num <= chapter:
                state = {
                    'type': rel_type,
                    **progression[ch_key]
                }

        return {
            'characters': [char1, char2],
            'chapter': chapter,
            **state
        }

    def secrets_active(self, chapter: int) -> list[dict]:
        """Returns all tracked secrets with who knows and who doesn't at chapter"""
        secrets = []

        for secret_id, secret_data in self.knowledge_tracking.items():
            ch_key = f"ch{chapter}"
            awareness = secret_data.get('awareness', {})

            # Find awareness at or before chapter
            knowers = []
            for ck in sorted(awareness.keys(), key=lambda x: int(x.replace('ch', ''))):
                cn = int(ck.replace('ch', ''))
                if cn <= chapter:
                    knowers = awareness[ck]

            reveal_ch = secret_data.get('reveal_chapter')
            is_revealed = reveal_ch is not None and reveal_ch <= chapter

            secrets.append({
                'id': secret_id,
                'description': secret_data.get('description', ''),
                'known_by': knowers,
                'secret_holder': secret_data.get('secret_holder', ''),
                'revealed': is_revealed,
                'reveal_chapter': reveal_ch
            })

        return secrets

    def get_character_arc(self, character: str) -> dict:
        """Returns full arc summary for a character"""
        char_data = self.characters.get(character, {})

        return {
            'character': character,
            'meta': char_data.get('meta', {}),
            'arc': char_data.get('arc', {}),
            'motives': char_data.get('motives', {}),
            'emotional_progression': char_data.get('emotional_progression', []),
            'threads': list(char_data.get('threads', {}).keys()),
            'active_chapters': sorted(self._character_chapters.get(character, []))
        }

    def get_chapter_summary(self, chapter: int) -> dict:
        """Returns comprehensive summary of a chapter"""
        ch_key = f"ch{chapter}"
        timeline_entry = self.timeline.get(ch_key, {})

        present = self.who_is_present(chapter)
        overlaps = [o for o in self._overlaps if o.chapter == chapter]
        secrets = self.secrets_active(chapter)

        # Gather character states
        character_states = {}
        for char in present:
            char_data = self.characters.get(char, {})
            ch_state = char_data.get('chapter_states', {}).get(ch_key, {})
            if ch_state:
                character_states[char] = ch_state

        return {
            'chapter': chapter,
            'month': timeline_entry.get('month', 0),
            'event': timeline_entry.get('event', ''),
            'date_approx': timeline_entry.get('date_approx'),
            'characters_present': present,
            'overlaps': overlaps,
            'active_secrets': [s for s in secrets if not s['revealed']],
            'character_states': character_states
        }

    def get_canon_warnings(self, characters: Optional[list] = None) -> list:
        """Returns canon warnings, optionally filtered by characters"""
        if characters is None:
            return self.canon_warnings

        char_set = set(characters)
        return [
            w for w in self.canon_warnings
            if char_set & set(w.get('applies_to', []))
        ]

    def get_emotional_stage(self, character: str, chapter: int) -> dict:
        """Returns the emotional stage a character is in at a chapter"""
        char_data = self.characters.get(character, {})
        progression = char_data.get('emotional_progression', [])

        for stage in progression:
            if chapter in stage.get('chapters', []):
                return {
                    'character': character,
                    'chapter': chapter,
                    'stage': stage.get('stage', ''),
                    'description': stage.get('description', '')
                }

        return {
            'character': character,
            'chapter': chapter,
            'stage': 'unknown',
            'description': ''
        }

    # ==========================================
    # EXPORT METHODS
    # ==========================================

    def export_character_scaffold(self, character: str) -> dict:
        """
        Export a per-character scaffold (like chess perspective export).
        Shows their journey through the story with all relevant context.
        """
        char_data = self.characters.get(character, {})

        journey = []
        for chapter in sorted(self._character_chapters.get(character, [])):
            ch_key = f"ch{chapter}"

            state = char_data.get('chapter_states', {}).get(ch_key, {})
            knowledge = self.what_does_character_know(character, chapter)
            emotional = self.get_emotional_stage(character, chapter)

            # Find relevant relationships at this chapter
            relationships = {}
            for rel_key in self.relationships.keys():
                if character in rel_key:
                    other = rel_key.replace(character, '').replace('_', '')
                    if other:
                        relationships[other] = self.get_relationship_state(character, other, chapter)

            journey.append({
                'chapter': chapter,
                'month': self._get_month(chapter),
                'location': state.get('location', ''),
                'emotional_stage': emotional,
                'knowledge': knowledge,
                'relationships': relationships,
                'key_actions': state.get('key_actions', []),
                'physical': state.get('physical', {})
            })

        return {
            'character': character,
            'meta': char_data.get('meta', {}),
            'arc': char_data.get('arc', {}),
            'threads': char_data.get('threads', {}),
            'journey': journey,
            'canon_warnings': self.get_canon_warnings([character])
        }

    def export_timeline_data(self) -> dict:
        """Export data in format suitable for HTML visualization"""
        characters_data = {}

        for char_id in self.characters.keys():
            events = []
            for chapter in sorted(self._character_chapters.get(char_id, [])):
                ch_key = f"ch{chapter}"
                state = self.characters[char_id].get('chapter_states', {}).get(ch_key, {})
                emotional = self.get_emotional_stage(char_id, chapter)

                # Build event text from key_actions or emotional state
                actions = state.get('key_actions', [])
                text = ', '.join(actions[:2]) if actions else emotional.get('description', '')

                events.append({
                    'chapter': chapter,
                    'month': self._get_month(chapter),
                    'text': text,
                    'emotional': emotional.get('stage', ''),
                    'type': 'action' if actions else 'emotional',
                    'location': state.get('location', '')
                })

            characters_data[char_id] = events

        return {
            'characters': characters_data,
            'timeline': self.timeline,
            'overlaps': [
                {
                    'chapter': o.chapter,
                    'title': o.title,
                    'characters': o.characters,
                    'type': o.overlap_type
                }
                for o in self._overlaps
            ],
            'total_chapters': 24,
            'meta': self.raw_data.get('meta', {})
        }


# ==========================================
# CLI INTERFACE
# ==========================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Go Squad Perspective Engine')
    parser.add_argument('command', choices=[
        'know', 'present', 'overlaps', 'relationship', 'secrets',
        'arc', 'chapter', 'scaffold', 'export'
    ])
    parser.add_argument('--character', '-c', help='Character ID')
    parser.add_argument('--chapter', '-ch', type=int, help='Chapter number')
    parser.add_argument('--char2', help='Second character (for relationships)')
    parser.add_argument('--output', '-o', help='Output file for export')

    args = parser.parse_args()

    engine = PerspectiveEngine().load()

    if args.command == 'know':
        if not args.character or not args.chapter:
            print("Error: --character and --chapter required")
            return
        result = engine.what_does_character_know(args.character, args.chapter)
        print(yaml.dump(result, default_flow_style=False))

    elif args.command == 'present':
        if not args.chapter:
            print("Error: --chapter required")
            return
        result = engine.who_is_present(args.chapter)
        print(f"Characters present in Ch{args.chapter}:")
        for char in result:
            print(f"  - {char}")

    elif args.command == 'overlaps':
        chars = [args.character, args.char2] if args.character and args.char2 else None
        result = engine.find_overlaps(chars)
        for overlap in result:
            print(f"Ch{overlap.chapter}: {overlap.title}")
            print(f"  Type: {overlap.overlap_type}")
            print(f"  Characters: {', '.join(overlap.characters)}")
            print()

    elif args.command == 'relationship':
        if not args.character or not args.char2 or not args.chapter:
            print("Error: --character, --char2, and --chapter required")
            return
        result = engine.get_relationship_state(args.character, args.char2, args.chapter)
        print(yaml.dump(result, default_flow_style=False))

    elif args.command == 'secrets':
        if not args.chapter:
            print("Error: --chapter required")
            return
        result = engine.secrets_active(args.chapter)
        print(yaml.dump(result, default_flow_style=False))

    elif args.command == 'arc':
        if not args.character:
            print("Error: --character required")
            return
        result = engine.get_character_arc(args.character)
        print(yaml.dump(result, default_flow_style=False))

    elif args.command == 'chapter':
        if not args.chapter:
            print("Error: --chapter required")
            return
        result = engine.get_chapter_summary(args.chapter)
        print(yaml.dump(result, default_flow_style=False, sort_keys=False))

    elif args.command == 'scaffold':
        if not args.character:
            print("Error: --character required")
            return
        result = engine.export_character_scaffold(args.character)
        output = yaml.dump(result, default_flow_style=False, sort_keys=False)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Scaffold exported to {args.output}")
        else:
            print(output)

    elif args.command == 'export':
        result = engine.export_timeline_data()
        output = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Timeline data exported to {args.output}")
        else:
            print(output)


if __name__ == '__main__':
    main()
