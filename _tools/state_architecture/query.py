#!/usr/bin/env python3
"""
Go Squad State Query Interface
Simple file-based queries for RLM-style external state retrieval.

Usage:
    from query import StateQuery
    sq = StateQuery()

    # Character queries
    state = sq.get_character_state("ahdia", 1)
    knows = sq.character_knows("ahdia", "exile_island", 1)  # False
    knows = sq.character_knows("ahdia", "exile_island", 13) # True

    # Location queries
    loc = sq.get_location("caledonia_memorial")

    # Knowledge queries
    who = sq.who_knows("exile_island", 13)  # ['ahdia', 'ryu', 'ruth', ...]

    # Object queries
    obj = sq.get_object("ahdia_baseline")
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass


@dataclass
class QueryResult:
    """Standardized query result with source attribution"""
    success: bool
    data: Any
    source_file: str
    source_section: Optional[str] = None
    error: Optional[str] = None


class StateQuery:
    """
    Query interface for Go Squad state architecture.
    Retrieves data from YAML files without loading everything into memory.
    """

    def __init__(self, root_path: Optional[Path] = None):
        """
        Initialize with repository root path.
        Defaults to two levels up from this file.
        """
        if root_path is None:
            # Go up: state_architecture -> _tools -> repository root
            root_path = Path(__file__).parent.parent.parent

        self.root = Path(root_path)
        self._cache: Dict[str, Any] = {}

        # Key file paths
        self.character_state_index = self.root / "7_characters" / "arcs" / "CHARACTER_STATE_INDEX.yaml"
        self.locations_dir = self.root / "5_story_bibles" / "locations"
        self.objects_index = self.root / "5_story_bibles" / "artifacts" / "OBJECTS_INDEX.yaml"
        self.schemas = self.root / "_tools" / "state_architecture" / "SCHEMAS.yaml"

    def _load_yaml(self, path: Path, use_cache: bool = True) -> Optional[Dict]:
        """Load and optionally cache a YAML file."""
        path_str = str(path)

        if use_cache and path_str in self._cache:
            return self._cache[path_str]

        if not path.exists():
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if use_cache:
                    self._cache[path_str] = data
                return data
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return None

    # ========================================
    # CHARACTER QUERIES
    # ========================================

    def get_character_state(self, character_id: str, chapter: int) -> QueryResult:
        """
        Get character state at specific chapter.

        Args:
            character_id: Character identifier (e.g., 'ahdia', 'tess')
            chapter: Chapter number

        Returns:
            QueryResult with chapter_states entry if found
        """
        data = self._load_yaml(self.character_state_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error="Character state index not found"
            )

        characters = data.get('characters', {})
        if character_id not in characters:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error=f"Character '{character_id}' not found"
            )

        character = characters[character_id]
        chapter_key = f"ch{chapter}"

        # Check for exact chapter state
        chapter_states = character.get('chapter_states', {})
        if chapter_key in chapter_states:
            return QueryResult(
                success=True,
                data=chapter_states[chapter_key],
                source_file=str(self.character_state_index),
                source_section=f"characters.{character_id}.chapter_states.{chapter_key}"
            )

        # If exact chapter not found, return character overview
        return QueryResult(
            success=True,
            data={
                'meta': character.get('meta', {}),
                'arc': character.get('arc', {}),
                'emotional_progression': self._get_stage_for_chapter(
                    character.get('emotional_progression', []),
                    chapter
                ),
                'note': f"No specific state for ch{chapter}, returning overview"
            },
            source_file=str(self.character_state_index),
            source_section=f"characters.{character_id}"
        )

    def _get_stage_for_chapter(self, progression: List[Dict], chapter: int) -> Optional[Dict]:
        """Find which emotional stage a character is in for a given chapter."""
        for stage in progression:
            chapters = stage.get('chapters', [])
            if chapter in chapters:
                return stage
        return None

    def character_knows(self, character_id: str, knowledge_item: str, chapter: int) -> QueryResult:
        """
        Check if character knows something at a specific chapter.

        Args:
            character_id: Character identifier
            knowledge_item: Knowledge item to check (e.g., 'exile_island')
            chapter: Chapter number

        Returns:
            QueryResult with boolean data
        """
        data = self._load_yaml(self.character_state_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error="Character state index not found"
            )

        # Check knowledge_tracking section
        knowledge_tracking = data.get('knowledge_tracking', {})

        if knowledge_item in knowledge_tracking:
            awareness = knowledge_tracking[knowledge_item].get('awareness', {})
            chapter_key = f"ch{chapter}"

            if chapter_key in awareness:
                knows = character_id in awareness[chapter_key]
                return QueryResult(
                    success=True,
                    data=knows,
                    source_file=str(self.character_state_index),
                    source_section=f"knowledge_tracking.{knowledge_item}.awareness.{chapter_key}"
                )

        # Check character's chapter_states.knows/learns
        characters = data.get('characters', {})
        if character_id in characters:
            chapter_states = characters[character_id].get('chapter_states', {})
            chapter_key = f"ch{chapter}"

            if chapter_key in chapter_states:
                state = chapter_states[chapter_key]
                knows_list = state.get('knows', []) + state.get('learns', [])

                # Fuzzy match
                for item in knows_list:
                    if knowledge_item.lower() in item.lower():
                        return QueryResult(
                            success=True,
                            data=True,
                            source_file=str(self.character_state_index),
                            source_section=f"characters.{character_id}.chapter_states.{chapter_key}.knows"
                        )

        return QueryResult(
            success=True,
            data=False,
            source_file=str(self.character_state_index),
            source_section="knowledge_tracking (not found)"
        )

    def who_knows(self, knowledge_item: str, chapter: int) -> QueryResult:
        """
        Get list of characters who know something at a specific chapter.

        Args:
            knowledge_item: Knowledge item identifier
            chapter: Chapter number

        Returns:
            QueryResult with list of character_ids
        """
        data = self._load_yaml(self.character_state_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error="Character state index not found"
            )

        knowledge_tracking = data.get('knowledge_tracking', {})

        if knowledge_item in knowledge_tracking:
            awareness = knowledge_tracking[knowledge_item].get('awareness', {})
            chapter_key = f"ch{chapter}"

            if chapter_key in awareness:
                return QueryResult(
                    success=True,
                    data=awareness[chapter_key],
                    source_file=str(self.character_state_index),
                    source_section=f"knowledge_tracking.{knowledge_item}.awareness.{chapter_key}"
                )

        return QueryResult(
            success=False,
            data=[],
            source_file=str(self.character_state_index),
            error=f"Knowledge item '{knowledge_item}' not tracked"
        )

    def get_canon_warnings(self, character_id: Optional[str] = None) -> QueryResult:
        """
        Get canon warnings, optionally filtered by character.

        Args:
            character_id: Optional character to filter by

        Returns:
            QueryResult with list of warnings
        """
        data = self._load_yaml(self.character_state_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error="Character state index not found"
            )

        warnings = data.get('canon_warnings', [])

        if character_id:
            filtered = [
                w for w in warnings
                if character_id in w.get('applies_to', [])
            ]
            return QueryResult(
                success=True,
                data=filtered,
                source_file=str(self.character_state_index),
                source_section=f"canon_warnings (filtered by {character_id})"
            )

        return QueryResult(
            success=True,
            data=warnings,
            source_file=str(self.character_state_index),
            source_section="canon_warnings"
        )

    def get_thread_state(self, character_id: str, thread_name: str, chapter: int) -> QueryResult:
        """
        Get state of a character's thread at specific chapter.

        Args:
            character_id: Character identifier
            thread_name: Thread name (e.g., 'baseline_decline', 'father_complicity')
            chapter: Chapter number

        Returns:
            QueryResult with thread gate data
        """
        data = self._load_yaml(self.character_state_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error="Character state index not found"
            )

        characters = data.get('characters', {})
        if character_id not in characters:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error=f"Character '{character_id}' not found"
            )

        threads = characters[character_id].get('threads', {})
        if thread_name not in threads:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error=f"Thread '{thread_name}' not found for {character_id}"
            )

        thread = threads[thread_name]
        gates = thread.get('gates', {})

        # Find most recent gate at or before requested chapter
        best_gate = None
        best_chapter = 0

        for gate_key, gate_data in gates.items():
            gate_chapter = int(gate_key.replace('ch', '').replace('_post', ''))
            if gate_chapter <= chapter and gate_chapter > best_chapter:
                best_gate = gate_data
                best_chapter = gate_chapter

        if best_gate:
            return QueryResult(
                success=True,
                data={
                    'thread_info': {
                        'type': thread.get('type'),
                        'description': thread.get('description')
                    },
                    'state_at_chapter': best_gate,
                    'gate_chapter': best_chapter
                },
                source_file=str(self.character_state_index),
                source_section=f"characters.{character_id}.threads.{thread_name}.gates.ch{best_chapter}"
            )

        return QueryResult(
            success=False,
            data=None,
            source_file=str(self.character_state_index),
            error=f"No gate found for thread '{thread_name}' at or before chapter {chapter}"
        )

    # ========================================
    # LOCATION QUERIES
    # ========================================

    def get_location(self, location_id: str) -> QueryResult:
        """
        Get location data.

        Args:
            location_id: Location identifier (e.g., 'caledonia_memorial')

        Returns:
            QueryResult with full location data
        """
        location_file = self.locations_dir / f"{location_id}.yaml"
        data = self._load_yaml(location_file)

        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(location_file),
                error=f"Location '{location_id}' not found"
            )

        return QueryResult(
            success=True,
            data=data,
            source_file=str(location_file)
        )

    def get_scenes_at_location(self, location_id: str) -> QueryResult:
        """
        Get all scenes that occur at a location.

        Args:
            location_id: Location identifier

        Returns:
            QueryResult with list of scenes
        """
        result = self.get_location(location_id)
        if not result.success:
            return result

        scenes = result.data.get('narrative_function', {}).get('scenes', [])

        return QueryResult(
            success=True,
            data=scenes,
            source_file=result.source_file,
            source_section="narrative_function.scenes"
        )

    def list_locations(self) -> QueryResult:
        """List all available locations."""
        if not self.locations_dir.exists():
            return QueryResult(
                success=False,
                data=[],
                source_file=str(self.locations_dir),
                error="Locations directory not found"
            )

        locations = [
            f.stem for f in self.locations_dir.glob("*.yaml")
        ]

        return QueryResult(
            success=True,
            data=locations,
            source_file=str(self.locations_dir)
        )

    # ========================================
    # OBJECT QUERIES
    # ========================================

    def get_object(self, object_id: str) -> QueryResult:
        """
        Get object/prop data.

        Args:
            object_id: Object identifier (e.g., 'ahdia_baseline', 'faeris_core')

        Returns:
            QueryResult with object data
        """
        data = self._load_yaml(self.objects_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.objects_index),
                error="Objects index not found"
            )

        objects = data.get('objects', {})
        if object_id not in objects:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.objects_index),
                error=f"Object '{object_id}' not found"
            )

        return QueryResult(
            success=True,
            data=objects[object_id],
            source_file=str(self.objects_index),
            source_section=f"objects.{object_id}"
        )

    def get_objects_owned_by(self, owner_id: str) -> QueryResult:
        """
        Get all objects owned by a character or organization.

        Args:
            owner_id: Owner identifier

        Returns:
            QueryResult with list of object_ids
        """
        data = self._load_yaml(self.objects_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.objects_index),
                error="Objects index not found"
            )

        by_owner = data.get('by_owner', {})
        if owner_id not in by_owner:
            return QueryResult(
                success=True,
                data=[],
                source_file=str(self.objects_index),
                source_section="by_owner"
            )

        return QueryResult(
            success=True,
            data=by_owner[owner_id],
            source_file=str(self.objects_index),
            source_section=f"by_owner.{owner_id}"
        )

    # ========================================
    # TIMELINE QUERIES
    # ========================================

    def get_chapter_timeline(self, chapter: int) -> QueryResult:
        """
        Get timeline info for a chapter.

        Args:
            chapter: Chapter number

        Returns:
            QueryResult with month, event, date_approx
        """
        data = self._load_yaml(self.character_state_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error="Character state index not found"
            )

        timeline = data.get('timeline', {})
        chapter_key = f"ch{chapter}"

        if chapter_key not in timeline:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error=f"Chapter {chapter} not in timeline"
            )

        return QueryResult(
            success=True,
            data=timeline[chapter_key],
            source_file=str(self.character_state_index),
            source_section=f"timeline.{chapter_key}"
        )

    def get_chapters_in_month(self, month: int) -> QueryResult:
        """
        Get all chapters that occur in a specific month.

        Args:
            month: Month number (1-12)

        Returns:
            QueryResult with list of chapter numbers
        """
        data = self._load_yaml(self.character_state_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error="Character state index not found"
            )

        timeline = data.get('timeline', {})
        chapters = [
            int(ch.replace('ch', ''))
            for ch, info in timeline.items()
            if info.get('month') == month
        ]

        return QueryResult(
            success=True,
            data=sorted(chapters),
            source_file=str(self.character_state_index),
            source_section="timeline"
        )

    # ========================================
    # RELATIONSHIP QUERIES
    # ========================================

    def get_relationship(self, char1: str, char2: str, chapter: Optional[int] = None) -> QueryResult:
        """
        Get relationship between two characters.

        Args:
            char1: First character
            char2: Second character
            chapter: Optional chapter for state at that point

        Returns:
            QueryResult with relationship data
        """
        data = self._load_yaml(self.character_state_index)
        if data is None:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error="Character state index not found"
            )

        relationships = data.get('relationships', {})

        # Try both orderings
        rel_key = f"{char1}_{char2}"
        if rel_key not in relationships:
            rel_key = f"{char2}_{char1}"

        if rel_key not in relationships:
            return QueryResult(
                success=False,
                data=None,
                source_file=str(self.character_state_index),
                error=f"Relationship between {char1} and {char2} not tracked"
            )

        rel_data = relationships[rel_key]

        if chapter is not None:
            progression = rel_data.get('progression', {})
            chapter_key = f"ch{chapter}"

            # Find most recent state
            best_state = None
            best_chapter = 0

            for ch_key, state in progression.items():
                ch_num = int(ch_key.replace('ch', ''))
                if ch_num <= chapter and ch_num > best_chapter:
                    best_state = state
                    best_chapter = ch_num

            if best_state:
                return QueryResult(
                    success=True,
                    data={
                        'type': rel_data.get('type'),
                        'state_at_chapter': best_state,
                        'state_chapter': best_chapter
                    },
                    source_file=str(self.character_state_index),
                    source_section=f"relationships.{rel_key}.progression.ch{best_chapter}"
                )

        return QueryResult(
            success=True,
            data=rel_data,
            source_file=str(self.character_state_index),
            source_section=f"relationships.{rel_key}"
        )


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

_default_query: Optional[StateQuery] = None

def _get_default_query() -> StateQuery:
    global _default_query
    if _default_query is None:
        _default_query = StateQuery()
    return _default_query


def get_character_state(character_id: str, chapter: int) -> QueryResult:
    """Convenience function for character state queries."""
    return _get_default_query().get_character_state(character_id, chapter)


def character_knows(character_id: str, knowledge_item: str, chapter: int) -> QueryResult:
    """Convenience function for knowledge checks."""
    return _get_default_query().character_knows(character_id, knowledge_item, chapter)


def who_knows(knowledge_item: str, chapter: int) -> QueryResult:
    """Convenience function for knowledge tracking."""
    return _get_default_query().who_knows(knowledge_item, chapter)


def get_location(location_id: str) -> QueryResult:
    """Convenience function for location queries."""
    return _get_default_query().get_location(location_id)


def get_object(object_id: str) -> QueryResult:
    """Convenience function for object queries."""
    return _get_default_query().get_object(object_id)


def get_canon_warnings(character_id: Optional[str] = None) -> QueryResult:
    """Convenience function for canon warnings."""
    return _get_default_query().get_canon_warnings(character_id)


# ========================================
# CLI INTERFACE
# ========================================

def main():
    """CLI for testing queries."""
    import argparse

    parser = argparse.ArgumentParser(description="Go Squad State Query Interface")

    subparsers = parser.add_subparsers(dest='command', help='Query type')

    # Character state
    char_parser = subparsers.add_parser('character', help='Get character state')
    char_parser.add_argument('character_id', help='Character identifier')
    char_parser.add_argument('chapter', type=int, help='Chapter number')

    # Knowledge check
    knows_parser = subparsers.add_parser('knows', help='Check if character knows something')
    knows_parser.add_argument('character_id', help='Character identifier')
    knows_parser.add_argument('knowledge_item', help='Knowledge item')
    knows_parser.add_argument('chapter', type=int, help='Chapter number')

    # Who knows
    who_parser = subparsers.add_parser('who-knows', help='Get who knows something')
    who_parser.add_argument('knowledge_item', help='Knowledge item')
    who_parser.add_argument('chapter', type=int, help='Chapter number')

    # Location
    loc_parser = subparsers.add_parser('location', help='Get location')
    loc_parser.add_argument('location_id', help='Location identifier')

    # Object
    obj_parser = subparsers.add_parser('object', help='Get object')
    obj_parser.add_argument('object_id', help='Object identifier')

    # Canon warnings
    warn_parser = subparsers.add_parser('warnings', help='Get canon warnings')
    warn_parser.add_argument('--character', help='Filter by character')

    # Timeline
    time_parser = subparsers.add_parser('timeline', help='Get chapter timeline')
    time_parser.add_argument('chapter', type=int, help='Chapter number')

    # Thread state
    thread_parser = subparsers.add_parser('thread', help='Get thread state')
    thread_parser.add_argument('character_id', help='Character identifier')
    thread_parser.add_argument('thread_name', help='Thread name')
    thread_parser.add_argument('chapter', type=int, help='Chapter number')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    sq = StateQuery()

    if args.command == 'character':
        result = sq.get_character_state(args.character_id, args.chapter)
    elif args.command == 'knows':
        result = sq.character_knows(args.character_id, args.knowledge_item, args.chapter)
    elif args.command == 'who-knows':
        result = sq.who_knows(args.knowledge_item, args.chapter)
    elif args.command == 'location':
        result = sq.get_location(args.location_id)
    elif args.command == 'object':
        result = sq.get_object(args.object_id)
    elif args.command == 'warnings':
        result = sq.get_canon_warnings(args.character)
    elif args.command == 'timeline':
        result = sq.get_chapter_timeline(args.chapter)
    elif args.command == 'thread':
        result = sq.get_thread_state(args.character_id, args.thread_name, args.chapter)
    else:
        parser.print_help()
        return

    # Print result
    import json
    print(f"\nSuccess: {result.success}")
    print(f"Source: {result.source_file}")
    if result.source_section:
        print(f"Section: {result.source_section}")
    if result.error:
        print(f"Error: {result.error}")
    print(f"\nData:")

    if isinstance(result.data, (dict, list)):
        print(json.dumps(result.data, indent=2, default=str))
    else:
        print(result.data)


if __name__ == '__main__':
    main()
