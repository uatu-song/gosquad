#!/usr/bin/env python3
"""
Prose Indexer for Go Squad
Version: 1.0

Ingests prose files and outputs codex entries tracking entity appearances,
canonical values, and location coordinates.

Usage:
    python prose_indexer.py ingest <prose_file> [--book N] [--chapter M]
    python prose_indexer.py ingest-all <book_dir> [--book N]
    python prose_indexer.py reindex <book_N>
    python prose_indexer.py status
    python prose_indexer.py approve <entity_id>
    python prose_indexer.py --summary  # Reduce log verbosity

Output:
    8_codex/book_N/codex.yaml
    _tools/prose_indexer/logs/{timestamp}_{operation}.yaml
"""

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
CODEX_DIR = PROJECT_ROOT / "8_codex"
LOGS_DIR = Path(__file__).parent / "logs"
ENTITY_CATALOG_PATH = PROJECT_ROOT / "entity_catalog" / "ENTITY_CATALOG.yaml"
MANUSCRIPT_DIR = PROJECT_ROOT / "6_manuscript"

# Ensure directories exist
CODEX_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ============================================================
# BANNED NAMES - AI SLOP DETECTION
# ============================================================
# Names that are telltale signs of AI-generated content.
# If these appear in prose, flag them for human revision.
# They should NOT be proposed as characters.

BANNED_NAMES = {
    # Generic AI-favored names
    "Marcus",
    "Chen",
    "Wei",
    "Zhang",
    "Patel",
    "Singh",
    "Rodriguez",  # Note: Victor Hernandez is allowed, Rodriguez is not
    "Thompson",
    "Williams",
    "Johnson",
    "Smith",
    # Add more as patterns emerge
}

# Full name patterns that are banned (checked against full extracted name)
BANNED_NAME_PATTERNS = [
    r"\bMarcus\b",
    r"\bChen\b",
    r"\bAgent\s+\w+\s+(?:Smith|Johnson|Williams|Thompson)\b",
    r"\bOfficer\s+\w+\s+(?:Smith|Johnson|Williams|Thompson)\b",
    r"\bDr\.\s+(?:Smith|Johnson|Williams|Chen|Patel)\b",
]


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class Coordinate:
    """Location coordinate in prose: b2:ch1:beat11:p2:s1"""
    book: int
    chapter: int
    beat: Optional[int] = None
    paragraph: Optional[int] = None
    sentence: Optional[int] = None

    def __str__(self) -> str:
        parts = [f"b{self.book}", f"ch{self.chapter}"]
        if self.beat is not None:
            parts.append(f"beat{self.beat}")
        if self.paragraph is not None:
            parts.append(f"p{self.paragraph}")
        if self.sentence is not None:
            parts.append(f"s{self.sentence}")
        return ":".join(parts)

    @classmethod
    def from_string(cls, coord_str: str) -> "Coordinate":
        """Parse coordinate string back to object."""
        pattern = r"b(\d+):ch(\d+)(?::beat(\d+))?(?::p(\d+))?(?::s(\d+))?"
        match = re.match(pattern, coord_str)
        if not match:
            raise ValueError(f"Invalid coordinate format: {coord_str}")
        groups = match.groups()
        return cls(
            book=int(groups[0]),
            chapter=int(groups[1]),
            beat=int(groups[2]) if groups[2] else None,
            paragraph=int(groups[3]) if groups[3] else None,
            sentence=int(groups[4]) if groups[4] else None,
        )


@dataclass
class Appearance:
    """Record of an entity appearing in prose."""
    location: Coordinate
    context: str
    reference_form: str
    reference_type: str  # name, alias, pronoun, descriptor
    pronoun_resolution: Optional[dict] = None


@dataclass
class AttributeMention:
    """Record of an attribute being mentioned."""
    location: Coordinate
    value_in_prose: str
    status: str  # canonical, drift, unset


@dataclass
class EntityAttribute:
    """Tracked attribute of an entity."""
    canonical_value: Optional[str] = None
    established_at: Optional[Coordinate] = None
    source: str = "prose"  # prose, entity_catalog, director_override
    mentions: list = field(default_factory=list)


@dataclass
class TrackedEntity:
    """Base class for tracked entities."""
    entity_id: str
    status: str  # canonical, proposed
    canonical_name: str
    aliases_in_prose: list = field(default_factory=list)
    appearances: list = field(default_factory=list)
    attributes: dict = field(default_factory=dict)


@dataclass
class TimeMarker:
    """Explicit time reference in prose."""
    marker_id: str
    location: Coordinate
    raw_text: str
    marker_type: str  # absolute, relative, duration, vague
    normalized: Optional[str] = None
    chapter_timeline_position: int = 0
    anchors_to: Optional[str] = None


@dataclass
class SlopAlert:
    """Record of potential AI-generated content detected."""
    alert_id: str
    location: Coordinate
    banned_name: str
    full_context: str
    severity: str = "warning"  # warning, critical


@dataclass
class SetupPayoff:
    """Narrative callback tracking."""
    callback_id: str
    description: str
    category: str  # character, plot, object, dialogue, worldbuilding
    setup_location: Coordinate
    setup_text: str
    setup_planted_by: str  # narrator, character_action, dialogue, description
    payoff_location: Optional[Coordinate] = None
    payoff_text: Optional[str] = None
    payoff_type: Optional[str] = None  # direct, subverted, escalated, partial
    status: str = "planted"  # planted, paid, abandoned, deferred_to_later_book
    expected_payoff_window: Optional[str] = None


# ============================================================
# PROCESS LOGGER
# ============================================================

class ProcessLogger:
    """Logs all indexer operations."""

    def __init__(self, operation: str, verbose: bool = True):
        self.operation = operation
        self.verbose = verbose
        self.timestamp = datetime.now().isoformat()
        self.entries: list[dict] = []
        self.summary_stats = {
            "files_processed": 0,
            "entities_found": 0,
            "proposed_entities": 0,
            "appearances_logged": 0,
            "time_markers_found": 0,
            "warnings": 0,
            "errors": 0,
        }

    def log(self, level: str, message: str, **context):
        """Add log entry."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
        }
        if context:
            entry["context"] = context
        self.entries.append(entry)

        # Update summary stats
        if level == "warning":
            self.summary_stats["warnings"] += 1
        elif level == "error":
            self.summary_stats["errors"] += 1

        # Print if verbose
        if self.verbose or level in ("warning", "error"):
            print(f"[{level.upper()}] {message}")

    def debug(self, message: str, **context):
        if self.verbose:
            self.log("debug", message, **context)

    def info(self, message: str, **context):
        self.log("info", message, **context)

    def warning(self, message: str, **context):
        self.log("warning", message, **context)

    def error(self, message: str, **context):
        self.log("error", message, **context)

    def save(self):
        """Write log to file."""
        filename = f"{self.timestamp.replace(':', '-')}_{self.operation}.yaml"
        log_path = LOGS_DIR / filename

        output = {
            "meta": {
                "operation": self.operation,
                "started_at": self.timestamp,
                "completed_at": datetime.now().isoformat(),
                "verbose_mode": self.verbose,
            },
            "summary": self.summary_stats,
        }

        if self.verbose:
            output["entries"] = self.entries

        with open(log_path, "w") as f:
            yaml.dump(output, f, default_flow_style=False, sort_keys=False)

        print(f"\nLog saved to: {log_path}")
        return log_path


# ============================================================
# ENTITY CATALOG LOADER
# ============================================================

class EntityCatalog:
    """Loads and queries the ENTITY_CATALOG.yaml."""

    def __init__(self):
        self.characters: dict = {}
        self.organizations: dict = {}
        self.locations: dict = {}
        self.objects: dict = {}
        self._load()

    def _load(self):
        """Load entity catalog from YAML."""
        if not ENTITY_CATALOG_PATH.exists():
            print(f"Warning: Entity catalog not found at {ENTITY_CATALOG_PATH}")
            return

        try:
            with open(ENTITY_CATALOG_PATH) as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            # ENTITY_CATALOG may have non-YAML patterns in validation_queries
            # Try to load just the characters section
            print(f"Warning: YAML parse error in entity catalog, attempting partial load")
            try:
                with open(ENTITY_CATALOG_PATH) as f:
                    content = f.read()
                # Find and extract just the characters section
                # This is a fallback for files with custom syntax in later sections
                import re
                chars_match = re.search(
                    r"^characters:\s*\n(.*?)(?=^[a-z_]+:|^#\s*=|\Z)",
                    content,
                    re.MULTILINE | re.DOTALL
                )
                if chars_match:
                    chars_yaml = "characters:\n" + chars_match.group(1)
                    data = yaml.safe_load(chars_yaml)
                else:
                    print(f"Error: Could not extract characters from entity catalog")
                    return
            except Exception as e2:
                print(f"Error loading entity catalog: {e2}")
                return

        self.characters = data.get("characters", {})
        self.organizations = data.get("organizations", {})
        # Add locations/objects if they exist in catalog

    def find_character_by_name(self, name: str) -> Optional[tuple[str, dict]]:
        """Find character by name or alias. Returns (entity_id, data) or None."""
        name_lower = name.lower()
        for entity_id, data in self.characters.items():
            # Check canonical name
            if data.get("canonical_name", "").lower() == name_lower:
                return (entity_id, data)
            # Check aliases
            for alias in data.get("aliases", []):
                if alias.lower() == name_lower:
                    return (entity_id, data)
        return None

    def get_character(self, entity_id: str) -> Optional[dict]:
        """Get character data by ID."""
        return self.characters.get(entity_id)

    def get_forbidden_knowledge(self, entity_id: str) -> dict:
        """Get forbidden_knowledge_before for a character."""
        char = self.characters.get(entity_id, {})
        return char.get("forbidden_knowledge_before", {})


# ============================================================
# PROSE PARSER
# ============================================================

class ProseParser:
    """Parses prose files into structural components."""

    # Patterns for chapter structure
    CHAPTER_PATTERN = re.compile(r"^#\s+Chapter\s+(\d+):\s*(.+)$", re.MULTILINE)
    SCENE_PATTERN = re.compile(r"^##\s+Scene\s+\d+:\s*(.+)$", re.MULTILINE)
    BEAT_PATTERN = re.compile(r"^###\s+(?:Beat|Beats)\s+([\d-]+)", re.MULTILINE)

    # Character name patterns (capitalized words, handling possessives)
    NAME_PATTERN = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b")

    # Time patterns
    TIME_PATTERNS = [
        (re.compile(r"\b(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))\b"), "absolute"),
        (re.compile(r"\b(\d{1,2}\s*(?:AM|PM|am|pm))\b"), "absolute"),
        (re.compile(r"\b((?:three|two|five|ten|\d+)\s+(?:days?|hours?|minutes?|weeks?)\s+(?:later|earlier|ago))\b", re.IGNORECASE), "relative"),
        (re.compile(r"\b(that\s+(?:morning|evening|night|afternoon))\b", re.IGNORECASE), "relative"),
        (re.compile(r"\b(the\s+next\s+(?:day|morning|evening))\b", re.IGNORECASE), "relative"),
    ]

    def __init__(self, book: int, chapter: int):
        self.book = book
        self.chapter = chapter
        self.current_beat: Optional[int] = None
        self.current_paragraph = 0
        self.current_sentence = 0

    def parse_file(self, filepath: Path) -> dict:
        """Parse a prose file into structured data."""
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        result = {
            "filepath": str(filepath),
            "hash": hashlib.sha256(content.encode()).hexdigest(),
            "book": self.book,
            "chapter": self.chapter,
            "beats": [],
            "raw_paragraphs": [],
        }

        # Split into beats
        beat_splits = list(self.BEAT_PATTERN.finditer(content))

        if not beat_splits:
            # No beat markers, treat whole content as one segment
            result["beats"].append({
                "beat_num": None,
                "content": content,
                "paragraphs": self._split_paragraphs(content),
            })
        else:
            # Process each beat section
            for i, match in enumerate(beat_splits):
                beat_str = match.group(1)
                # Handle "Beats 6-8" format
                if "-" in beat_str:
                    beat_num = int(beat_str.split("-")[0])
                else:
                    beat_num = int(beat_str)

                # Get content until next beat or end
                start = match.end()
                end = beat_splits[i + 1].start() if i + 1 < len(beat_splits) else len(content)
                beat_content = content[start:end].strip()

                result["beats"].append({
                    "beat_num": beat_num,
                    "content": beat_content,
                    "paragraphs": self._split_paragraphs(beat_content),
                })

        return result

    def _split_paragraphs(self, text: str) -> list[dict]:
        """Split text into paragraphs with sentence breakdown."""
        paragraphs = []
        # Split on double newlines, filter empty
        raw_paras = [p.strip() for p in re.split(r"\n\n+", text) if p.strip()]

        for i, para in enumerate(raw_paras):
            # Skip markdown headers and metadata
            if para.startswith("#") or para.startswith("**Rolls:**"):
                continue

            sentences = self._split_sentences(para)
            if sentences:
                paragraphs.append({
                    "index": i + 1,
                    "text": para,
                    "sentences": sentences,
                })

        return paragraphs

    def _split_sentences(self, text: str) -> list[dict]:
        """Split paragraph into sentences."""
        # Simple sentence splitting (handles common cases)
        # More sophisticated NLP could be added later
        sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z"])')
        parts = sentence_endings.split(text)

        sentences = []
        for i, sent in enumerate(parts):
            sent = sent.strip()
            if sent:
                sentences.append({
                    "index": i + 1,
                    "text": sent,
                })
        return sentences

    def make_coordinate(self, beat: Optional[int], paragraph: int, sentence: int) -> Coordinate:
        """Create a coordinate for current position."""
        return Coordinate(
            book=self.book,
            chapter=self.chapter,
            beat=beat,
            paragraph=paragraph,
            sentence=sentence,
        )


# ============================================================
# ENTITY EXTRACTOR
# ============================================================

class EntityExtractor:
    """Extracts and tracks entities from parsed prose."""

    # Common words to skip as potential names
    # This is extensive to avoid false positives - better to miss a character
    # than to flood the proposed list with garbage
    SKIP_WORDS = {
        # Pronouns and determiners
        "The", "This", "That", "What", "When", "Where", "Why", "How",
        "She", "He", "They", "It", "Her", "His", "Their", "Its",
        "We", "You", "Your", "My", "Our", "Who", "Which",
        # Conjunctions and prepositions
        "But", "And", "Or", "Not", "Just", "Like", "Even", "So",
        "For", "From", "With", "Into", "Through", "After", "Before",
        "About", "Between", "To", "In", "On", "At", "By", "Of",
        # Common sentence starters and transitions
        "Now", "Then", "There", "Here", "Still", "Already", "Yet",
        "First", "Second", "Third", "Next", "Last", "Finally",
        "Also", "Too", "Very", "Really", "Only", "Maybe", "Perhaps",
        "Because", "Although", "However", "Therefore", "Meanwhile",
        "Instead", "Otherwise", "Anyway", "Besides", "Furthermore",
        # Structural markers
        "Chapter", "Scene", "Beat", "Beats", "Part",
        # Days and months
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
        # Numbers as words
        "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
        "Eighteen", "Nineteen", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
        "Seventy", "Eighty", "Ninety", "Hundred", "Thousand",
        # Common verbs (capitalized at sentence start)
        "Said", "Asked", "Told", "Looked", "Turned", "Moved", "Made", "Took",
        "Got", "Went", "Came", "Saw", "Felt", "Thought", "Knew", "Wanted",
        "Started", "Stopped", "Tried", "Needed", "Seemed", "Found", "Left",
        "Let", "Keep", "Kept", "Hold", "Held", "Watch", "Watched", "Wait",
        "Waited", "Stand", "Standing", "Stood", "Sit", "Sitting", "Sat",
        "Run", "Running", "Ran", "Walk", "Walking", "Walked", "Move", "Moving",
        # Common adjectives (capitalized at sentence start)
        "Good", "Bad", "Great", "Small", "Big", "Old", "New", "Young",
        "Long", "Short", "High", "Low", "Dark", "Light", "Bright",
        "Black", "White", "Red", "Blue", "Green", "Yellow", "Gray", "Grey",
        "Better", "Best", "Worse", "Worst", "More", "Most", "Less", "Least",
        "Real", "True", "False", "Right", "Wrong", "Same", "Different",
        "Empty", "Full", "Clean", "Dirty", "Wet", "Dry", "Cold", "Hot",
        "Close", "Far", "Near", "Deep", "Shallow", "Quiet", "Loud",
        # Common nouns (capitalized at sentence start)
        "People", "Someone", "Anyone", "Everyone", "Nobody", "Nothing",
        "Something", "Anything", "Everything", "Time", "Times", "Day", "Days",
        "Night", "Nights", "Morning", "Evening", "Afternoon", "Hour", "Hours",
        "Minute", "Minutes", "Second", "Seconds", "Week", "Weeks", "Month",
        "Year", "Years", "Hand", "Hands", "Eye", "Eyes", "Face", "Head",
        "Body", "Heart", "Blood", "Breath", "Voice", "Sound", "Words",
        "Room", "Door", "Window", "Wall", "Floor", "Street", "Road",
        "City", "Town", "Building", "House", "Home", "Place", "Side",
        "Front", "Back", "Top", "Bottom", "Center", "Edge", "Corner",
        # Common adverbs
        "Slowly", "Quickly", "Carefully", "Quietly", "Suddenly", "Finally",
        # Dialogue markers
        "Yes", "Yeah", "No", "Nope", "Okay", "Ok", "Sorry", "Thanks",
        "Please", "Hey", "Hello", "Hi", "Bye", "Goodbye",
        # Misc common words that appear capitalized
        "Feed", "Feeds", "Signs", "Candles", "Fists", "Frozen", "Cellular",
        "Military", "Medical", "Security", "Professional", "Mobile",
        "Status", "Copy", "Movement", "Training", "Resources",
        # Contractions and fragments that get extracted
        "Don", "Didn", "Couldn", "Wouldn", "Shouldn", "Isn", "Aren", "Wasn",
    }

    # Pronouns for resolution
    FEMALE_PRONOUNS = {"she", "her", "hers", "herself"}
    MALE_PRONOUNS = {"he", "him", "his", "himself"}
    NEUTRAL_PRONOUNS = {"they", "them", "their", "theirs", "themself", "themselves"}

    def __init__(self, catalog: EntityCatalog, logger: ProcessLogger):
        self.catalog = catalog
        self.logger = logger
        self.tracked_entities: dict[str, TrackedEntity] = {}
        self.proposed_entities: dict[str, TrackedEntity] = {}
        self.time_markers: list[TimeMarker] = []
        self.time_marker_counter = 0
        self.slop_alerts: list[SlopAlert] = []
        self.slop_alert_counter = 0

        # Track recent characters for pronoun resolution
        self.recent_characters: list[tuple[str, str]] = []  # (entity_id, gender)

    def process_parsed_prose(self, parsed: dict):
        """Process parsed prose data and extract entities."""
        book = parsed["book"]
        chapter = parsed["chapter"]

        for beat_data in parsed["beats"]:
            beat_num = beat_data["beat_num"]

            for para in beat_data["paragraphs"]:
                para_idx = para["index"]

                for sent in para["sentences"]:
                    sent_idx = sent["index"]
                    sent_text = sent["text"]

                    coord = Coordinate(book, chapter, beat_num, para_idx, sent_idx)

                    # Extract character names
                    self._extract_characters(sent_text, coord)

                    # Extract time markers
                    self._extract_time_markers(sent_text, coord)

                    # Process pronouns
                    self._process_pronouns(sent_text, coord)

    def _extract_characters(self, text: str, coord: Coordinate):
        """Find and track character mentions in text."""
        # First, check for banned names (AI slop detection)
        self._check_for_banned_names(text, coord)

        # Find potential names
        for match in ProseParser.NAME_PATTERN.finditer(text):
            name = match.group(1)

            # Skip common words
            if name in self.SKIP_WORDS:
                continue

            # Skip single short words that aren't in the catalog
            # (likely sentence-initial common words we missed)
            if len(name) < 4 and " " not in name:
                result = self.catalog.find_character_by_name(name)
                if not result:
                    continue

            # Check if this name contains a banned word - skip proposing it
            name_words = set(name.split())
            if name_words & BANNED_NAMES:
                # Already flagged by _check_for_banned_names, don't propose
                continue

            # Look up in catalog
            result = self.catalog.find_character_by_name(name)

            if result:
                entity_id, char_data = result
                self._add_character_appearance(
                    entity_id=entity_id,
                    canonical_name=char_data.get("canonical_name", name),
                    reference_form=name,
                    reference_type="name" if name == char_data.get("canonical_name") else "alias",
                    coord=coord,
                    context=text[:100],
                    status="canonical",
                    gender=self._get_gender(char_data),
                )
            else:
                # Only propose entities that look like real names:
                # - Multi-word names (e.g., "Daniel Farah")
                # - Or single words that appear multiple times in the chapter
                # For now, only propose multi-word or catalog matches
                if " " in name:
                    self._propose_character(name, coord, text[:100])

    def _check_for_banned_names(self, text: str, coord: Coordinate):
        """Check text for banned names (AI slop indicators)."""
        for banned_name in BANNED_NAMES:
            # Check for the banned name as a word boundary match
            pattern = rf"\b{re.escape(banned_name)}\b"
            if re.search(pattern, text, re.IGNORECASE):
                self.slop_alert_counter += 1
                alert = SlopAlert(
                    alert_id=f"SLOP_{self.slop_alert_counter:04d}",
                    location=coord,
                    banned_name=banned_name,
                    full_context=text[:150],
                    severity="warning",
                )
                self.slop_alerts.append(alert)
                self.logger.warning(
                    f"BANNED NAME DETECTED: '{banned_name}' - potential AI slop",
                    location=str(coord),
                    context=text[:80],
                )

        # Also check full patterns
        for pattern in BANNED_NAME_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                self.slop_alert_counter += 1
                match = re.search(pattern, text, re.IGNORECASE)
                alert = SlopAlert(
                    alert_id=f"SLOP_{self.slop_alert_counter:04d}",
                    location=coord,
                    banned_name=match.group(0) if match else pattern,
                    full_context=text[:150],
                    severity="critical",
                )
                self.slop_alerts.append(alert)
                self.logger.warning(
                    f"BANNED PATTERN DETECTED: '{match.group(0) if match else pattern}' - potential AI slop",
                    location=str(coord),
                    context=text[:80],
                )

    def _get_gender(self, char_data: dict) -> str:
        """Extract gender from character data."""
        demographics = char_data.get("demographics", {})
        gender = demographics.get("gender", "unknown")
        return gender

    def _add_character_appearance(
        self,
        entity_id: str,
        canonical_name: str,
        reference_form: str,
        reference_type: str,
        coord: Coordinate,
        context: str,
        status: str,
        gender: str = "unknown",
        pronoun_resolution: Optional[dict] = None,
    ):
        """Add or update character tracking."""
        if entity_id not in self.tracked_entities:
            self.tracked_entities[entity_id] = TrackedEntity(
                entity_id=entity_id,
                status=status,
                canonical_name=canonical_name,
                aliases_in_prose=[],
            )

        entity = self.tracked_entities[entity_id]

        # Track alias
        if reference_form not in entity.aliases_in_prose and reference_form != canonical_name:
            if reference_type != "pronoun":
                entity.aliases_in_prose.append(reference_form)

        # Add appearance
        appearance = Appearance(
            location=coord,
            context=context,
            reference_form=reference_form,
            reference_type=reference_type,
            pronoun_resolution=pronoun_resolution,
        )
        entity.appearances.append(appearance)

        # Update recent characters for pronoun resolution
        if reference_type in ("name", "alias"):
            # Add to front of recent list
            self.recent_characters = [(entity_id, gender)] + [
                (eid, g) for eid, g in self.recent_characters if eid != entity_id
            ][:5]  # Keep last 5

        self.logger.debug(
            f"Character appearance: {canonical_name} ({reference_form})",
            entity_id=entity_id,
            location=str(coord),
        )
        self.logger.summary_stats["appearances_logged"] += 1

    def _propose_character(self, name: str, coord: Coordinate, context: str):
        """Create proposed entity for Director review."""
        # Generate proposed ID
        proposed_num = len(self.proposed_entities) + 900  # Start at 900 to avoid conflicts
        entity_id = f"CHAR_{proposed_num:03d}"

        if name not in [e.canonical_name for e in self.proposed_entities.values()]:
            self.proposed_entities[entity_id] = TrackedEntity(
                entity_id=entity_id,
                status="proposed",
                canonical_name=name,
                aliases_in_prose=[name],
                appearances=[
                    Appearance(
                        location=coord,
                        context=context,
                        reference_form=name,
                        reference_type="name",
                    )
                ],
            )
            self.logger.info(
                f"Proposed new character: {name}",
                entity_id=entity_id,
                location=str(coord),
            )
            self.logger.summary_stats["proposed_entities"] += 1
        else:
            # Add appearance to existing proposed entity
            for eid, entity in self.proposed_entities.items():
                if entity.canonical_name == name:
                    entity.appearances.append(
                        Appearance(
                            location=coord,
                            context=context,
                            reference_form=name,
                            reference_type="name",
                        )
                    )
                    break

    def _process_pronouns(self, text: str, coord: Coordinate):
        """Attempt to resolve pronouns to characters."""
        text_lower = text.lower()
        words = set(re.findall(r"\b\w+\b", text_lower))

        # Check for female pronouns
        female_found = words & self.FEMALE_PRONOUNS
        male_found = words & self.MALE_PRONOUNS

        if female_found:
            self._resolve_pronoun(list(female_found)[0], "woman", coord, text)
        if male_found:
            self._resolve_pronoun(list(male_found)[0], "man", coord, text)

    def _resolve_pronoun(self, pronoun: str, target_gender: str, coord: Coordinate, context: str):
        """Try to resolve a pronoun to a recent character."""
        # Find candidates of matching gender
        candidates = [
            (eid, g) for eid, g in self.recent_characters
            if g == target_gender
        ]

        if len(candidates) == 0:
            # No candidates
            self.logger.debug(
                f"Pronoun '{pronoun}' has no candidates",
                location=str(coord),
            )
            return

        if len(candidates) == 1:
            # High confidence - only one candidate
            entity_id = candidates[0][0]
            entity = self.tracked_entities.get(entity_id)
            if entity:
                self._add_character_appearance(
                    entity_id=entity_id,
                    canonical_name=entity.canonical_name,
                    reference_form=pronoun,
                    reference_type="pronoun",
                    coord=coord,
                    context=context[:100],
                    status="canonical",
                    gender=target_gender,
                    pronoun_resolution={
                        "resolved_to": entity_id,
                        "confidence": "high",
                        "reason": "single candidate of matching gender",
                    },
                )
        else:
            # Multiple candidates - log as ambiguous
            self.logger.debug(
                f"Pronoun '{pronoun}' is ambiguous",
                location=str(coord),
                candidates=[c[0] for c in candidates],
            )

    def _extract_time_markers(self, text: str, coord: Coordinate):
        """Find explicit time references."""
        for pattern, marker_type in ProseParser.TIME_PATTERNS:
            for match in pattern.finditer(text):
                self.time_marker_counter += 1
                marker_id = f"b{coord.book}_ch{coord.chapter}_tm{self.time_marker_counter:03d}"

                marker = TimeMarker(
                    marker_id=marker_id,
                    location=coord,
                    raw_text=match.group(1),
                    marker_type=marker_type,
                    chapter_timeline_position=self.time_marker_counter,
                )

                # Try to normalize absolute times
                if marker_type == "absolute":
                    marker.normalized = self._normalize_time(match.group(1))

                self.time_markers.append(marker)
                self.logger.debug(
                    f"Time marker: {match.group(1)} ({marker_type})",
                    location=str(coord),
                )
                self.logger.summary_stats["time_markers_found"] += 1

    def _normalize_time(self, time_str: str) -> Optional[str]:
        """Convert time string to normalized format."""
        # Simple normalization - could be enhanced
        time_str = time_str.strip().upper()
        try:
            # Handle "6:47 PM" format
            if ":" in time_str:
                parts = time_str.replace("AM", "").replace("PM", "").strip().split(":")
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
                if "PM" in time_str and hour < 12:
                    hour += 12
                elif "AM" in time_str and hour == 12:
                    hour = 0
                return f"{hour:02d}:{minute:02d}:00"
        except (ValueError, IndexError):
            pass
        return None


# ============================================================
# CODEX WRITER
# ============================================================

class CodexWriter:
    """Writes codex YAML files."""

    def __init__(self, book: int):
        self.book = book
        self.codex_path = CODEX_DIR / f"book_{book}" / "codex.yaml"
        self.codex_path.parent.mkdir(parents=True, exist_ok=True)
        self.existing_data = self._load_existing()

    def _load_existing(self) -> dict:
        """Load existing codex if present."""
        if self.codex_path.exists():
            with open(self.codex_path) as f:
                return yaml.safe_load(f) or {}
        return {}

    def write(
        self,
        entities: dict[str, TrackedEntity],
        proposed: dict[str, TrackedEntity],
        time_markers: list[TimeMarker],
        prose_sources: list[dict],
        chapters_indexed: list[int],
        slop_alerts: list[SlopAlert] = None,
    ):
        """Write codex to YAML."""
        codex = {
            "meta": {
                "book": self.book,
                "chapters_indexed": sorted(set(
                    self.existing_data.get("meta", {}).get("chapters_indexed", [])
                    + chapters_indexed
                )),
                "last_indexed": datetime.now().isoformat(),
                "indexer_version": "1.0",
                "prose_sources": prose_sources,
            },
            "characters": self._format_entities(entities),
            "locations": {},  # Placeholder for future
            "objects": {},  # Placeholder for future
            "time_markers": [self._format_time_marker(tm) for tm in time_markers],
            "relationships": [],  # Placeholder for future
            "themes": {},  # Placeholder for future
            "setups_payoffs": [],  # Placeholder for future
            "canonical_values": self._extract_canonical_values(entities),
            "proposed_entities": {
                "characters": self._format_entities(proposed),
                "locations": {},
                "objects": {},
            },
            "slop_alerts": [self._format_slop_alert(sa) for sa in (slop_alerts or [])],
        }

        # Merge with existing data
        codex = self._merge_with_existing(codex)

        with open(self.codex_path, "w") as f:
            yaml.dump(codex, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f"\nCodex written to: {self.codex_path}")
        return self.codex_path

    def _format_entities(self, entities: dict[str, TrackedEntity]) -> dict:
        """Format entities for YAML output."""
        result = {}
        for entity_id, entity in entities.items():
            result[entity_id] = {
                "canonical_name": entity.canonical_name,
                "status": entity.status,
                "aliases_in_prose": entity.aliases_in_prose,
                "appearances": [
                    {
                        "location": str(app.location),
                        "context": app.context,
                        "reference_form": app.reference_form,
                        "reference_type": app.reference_type,
                        **({"pronoun_resolution": app.pronoun_resolution} if app.pronoun_resolution else {}),
                    }
                    for app in entity.appearances
                ],
                "attributes": {
                    name: {
                        "canonical_value": attr.canonical_value,
                        "established_at": str(attr.established_at) if attr.established_at else None,
                        "source": attr.source,
                        "mentions": [
                            {
                                "location": str(m.location),
                                "value_in_prose": m.value_in_prose,
                                "status": m.status,
                            }
                            for m in attr.mentions
                        ],
                    }
                    for name, attr in entity.attributes.items()
                },
            }
        return result

    def _format_time_marker(self, tm: TimeMarker) -> dict:
        """Format time marker for YAML output."""
        return {
            "marker_id": tm.marker_id,
            "location": str(tm.location),
            "raw_text": tm.raw_text,
            "marker_type": tm.marker_type,
            "normalized": tm.normalized,
            "chapter_timeline_position": tm.chapter_timeline_position,
            "anchors_to": tm.anchors_to,
        }

    def _format_slop_alert(self, sa: SlopAlert) -> dict:
        """Format slop alert for YAML output."""
        return {
            "alert_id": sa.alert_id,
            "location": str(sa.location),
            "banned_name": sa.banned_name,
            "full_context": sa.full_context,
            "severity": sa.severity,
        }

    def _extract_canonical_values(self, entities: dict[str, TrackedEntity]) -> dict:
        """Build canonical values quick-reference."""
        values = {}
        for entity_id, entity in entities.items():
            for attr_name, attr in entity.attributes.items():
                if attr.canonical_value:
                    key = f"{entity_id}.{attr_name}"
                    values[key] = {
                        "value": attr.canonical_value,
                        "established_at": str(attr.established_at) if attr.established_at else None,
                    }
        return values

    def _merge_with_existing(self, new_codex: dict) -> dict:
        """Merge new data with existing codex."""
        if not self.existing_data:
            return new_codex

        # Merge characters
        existing_chars = self.existing_data.get("characters", {})
        for entity_id, data in new_codex.get("characters", {}).items():
            if entity_id in existing_chars:
                # Merge appearances
                existing_apps = existing_chars[entity_id].get("appearances", [])
                existing_locs = {a["location"] for a in existing_apps}
                for app in data.get("appearances", []):
                    if app["location"] not in existing_locs:
                        existing_apps.append(app)
                existing_chars[entity_id]["appearances"] = existing_apps

                # Merge aliases
                existing_aliases = set(existing_chars[entity_id].get("aliases_in_prose", []))
                existing_aliases.update(data.get("aliases_in_prose", []))
                existing_chars[entity_id]["aliases_in_prose"] = list(existing_aliases)
            else:
                existing_chars[entity_id] = data

        new_codex["characters"] = existing_chars

        # Merge time markers (avoid duplicates by location)
        existing_markers = self.existing_data.get("time_markers", [])
        existing_marker_locs = {m["location"] for m in existing_markers}
        for marker in new_codex.get("time_markers", []):
            if marker["location"] not in existing_marker_locs:
                existing_markers.append(marker)
        new_codex["time_markers"] = existing_markers

        # Merge proposed entities
        existing_proposed = self.existing_data.get("proposed_entities", {}).get("characters", {})
        new_proposed = new_codex.get("proposed_entities", {}).get("characters", {})

        for entity_id, data in new_proposed.items():
            name = data.get("canonical_name", "")
            # Check if this name already exists in existing proposed (may have different ID)
            existing_match = None
            for eid, edata in existing_proposed.items():
                if edata.get("canonical_name") == name:
                    existing_match = eid
                    break

            if existing_match:
                # Merge appearances
                existing_apps = existing_proposed[existing_match].get("appearances", [])
                existing_locs = {a["location"] for a in existing_apps}
                for app in data.get("appearances", []):
                    if app["location"] not in existing_locs:
                        existing_apps.append(app)
                existing_proposed[existing_match]["appearances"] = existing_apps
            else:
                # Generate new ID that doesn't conflict
                max_id = 899
                for eid in existing_proposed.keys():
                    if eid.startswith("CHAR_"):
                        try:
                            num = int(eid.split("_")[1])
                            if num > max_id:
                                max_id = num
                        except ValueError:
                            pass
                new_id = f"CHAR_{max_id + 1}"
                existing_proposed[new_id] = data

        new_codex["proposed_entities"] = {"characters": existing_proposed, "locations": {}, "objects": {}}

        # Merge slop alerts (avoid duplicates by location+banned_name)
        existing_alerts = self.existing_data.get("slop_alerts", [])
        existing_alert_keys = {(a["location"], a["banned_name"]) for a in existing_alerts}
        for alert in new_codex.get("slop_alerts", []):
            key = (alert["location"], alert["banned_name"])
            if key not in existing_alert_keys:
                existing_alerts.append(alert)
        new_codex["slop_alerts"] = existing_alerts

        return new_codex


# ============================================================
# MAIN CLI
# ============================================================

def ingest_file(filepath: Path, book: int, chapter: int, verbose: bool = True):
    """Ingest a single prose file."""
    # Resolve to absolute path
    filepath = filepath.resolve()

    logger = ProcessLogger("ingest", verbose=verbose)
    logger.info(f"Starting ingest: {filepath}")

    # Load entity catalog
    catalog = EntityCatalog()

    # Parse prose
    parser = ProseParser(book, chapter)
    parsed = parser.parse_file(filepath)
    logger.summary_stats["files_processed"] = 1

    # Extract entities
    extractor = EntityExtractor(catalog, logger)
    extractor.process_parsed_prose(parsed)
    logger.summary_stats["entities_found"] = len(extractor.tracked_entities)

    # Write codex
    writer = CodexWriter(book)
    writer.write(
        entities=extractor.tracked_entities,
        proposed=extractor.proposed_entities,
        time_markers=extractor.time_markers,
        prose_sources=[{
            "path": str(filepath.relative_to(PROJECT_ROOT)),
            "hash": parsed["hash"],
            "indexed_at": datetime.now().isoformat(),
        }],
        chapters_indexed=[chapter],
        slop_alerts=extractor.slop_alerts,
    )

    # Save log
    logger.save()

    # Print summary
    print("\n" + "=" * 50)
    print("INGEST SUMMARY")
    print("=" * 50)
    print(f"  File: {filepath.name}")
    print(f"  Characters found: {len(extractor.tracked_entities)}")
    print(f"  Proposed entities: {len(extractor.proposed_entities)}")
    print(f"  Time markers: {len(extractor.time_markers)}")
    print(f"  Total appearances: {logger.summary_stats['appearances_logged']}")
    print(f"  Warnings: {logger.summary_stats['warnings']}")

    if extractor.slop_alerts:
        print(f"\n  ⚠️  SLOP ALERTS: {len(extractor.slop_alerts)} banned names detected!")
        print("  These require human revision (not character proposals):")
        for alert in extractor.slop_alerts:
            print(f"    - '{alert.banned_name}' at {alert.location}")
            print(f"      Context: \"{alert.full_context[:60]}...\"")

    if extractor.proposed_entities:
        print("\n  PROPOSED ENTITIES (require Director approval):")
        for eid, entity in extractor.proposed_entities.items():
            print(f"    - {entity.canonical_name} ({eid}): {len(entity.appearances)} appearances")


def ingest_book(book_dir: Path, book: int, verbose: bool = True):
    """Ingest all chapter files in a book directory."""
    chapter_pattern = re.compile(r"chapter_(\d+)\.md$")

    chapter_files = []
    for f in sorted(book_dir.iterdir()):
        match = chapter_pattern.match(f.name)
        if match:
            chapter_num = int(match.group(1))
            chapter_files.append((f, chapter_num))

    if not chapter_files:
        print(f"No chapter files found in {book_dir}")
        return

    print(f"Found {len(chapter_files)} chapters to index")

    for filepath, chapter in chapter_files:
        print(f"\n{'=' * 50}")
        print(f"Processing Chapter {chapter}")
        print("=" * 50)
        ingest_file(filepath, book, chapter, verbose=verbose)


def show_status():
    """Show current indexing status."""
    print("\nPROSE INDEXER STATUS")
    print("=" * 50)

    for book_dir in sorted(CODEX_DIR.iterdir()):
        if book_dir.is_dir() and book_dir.name.startswith("book_"):
            codex_path = book_dir / "codex.yaml"
            if codex_path.exists():
                with open(codex_path) as f:
                    data = yaml.safe_load(f)
                meta = data.get("meta", {})
                slop_count = len(data.get("slop_alerts", []))
                print(f"\n{book_dir.name}:")
                print(f"  Chapters indexed: {meta.get('chapters_indexed', [])}")
                print(f"  Last indexed: {meta.get('last_indexed', 'Never')}")
                print(f"  Characters: {len(data.get('characters', {}))}")
                print(f"  Proposed: {len(data.get('proposed_entities', {}).get('characters', {}))}")
                if slop_count > 0:
                    print(f"  ⚠️  Slop alerts: {slop_count}")
            else:
                print(f"\n{book_dir.name}: No codex.yaml")


def list_proposed(book: Optional[int] = None):
    """List all proposed entities awaiting approval."""
    print("\nPROPOSED ENTITIES")
    print("=" * 60)

    books_to_check = []
    if book:
        books_to_check = [CODEX_DIR / f"book_{book}"]
    else:
        books_to_check = sorted(CODEX_DIR.iterdir())

    total_proposed = 0

    for book_dir in books_to_check:
        if not book_dir.is_dir() or not book_dir.name.startswith("book_"):
            continue

        codex_path = book_dir / "codex.yaml"
        if not codex_path.exists():
            continue

        with open(codex_path) as f:
            data = yaml.safe_load(f)

        proposed = data.get("proposed_entities", {}).get("characters", {})
        if not proposed:
            continue

        book_num = book_dir.name.split("_")[1]
        print(f"\n{book_dir.name}:")
        print("-" * 60)

        # Sort by appearance count (descending) to show most common first
        sorted_proposed = sorted(
            proposed.items(),
            key=lambda x: len(x[1].get("appearances", [])),
            reverse=True
        )

        for entity_id, entity_data in sorted_proposed:
            name = entity_data.get("canonical_name", "Unknown")
            appearances = len(entity_data.get("appearances", []))
            # Get first appearance location for context
            first_loc = ""
            if entity_data.get("appearances"):
                first_loc = entity_data["appearances"][0].get("location", "")

            print(f"  {entity_id}: {name}")
            print(f"      {appearances} appearances, first at {first_loc}")

            # Show context from first appearance
            if entity_data.get("appearances"):
                context = entity_data["appearances"][0].get("context", "")[:60]
                if context:
                    print(f"      Context: \"{context}...\"")

            total_proposed += 1

    print(f"\n{'=' * 60}")
    print(f"Total proposed entities: {total_proposed}")
    print("\nTo approve: python prose_indexer.py approve <entity_id> --book <N>")
    print("To reject:  python prose_indexer.py reject <entity_id> --book <N>")


def list_slop_alerts(book: Optional[int] = None):
    """List all slop alerts (banned names requiring human revision)."""
    print("\n⚠️  SLOP ALERTS - Banned Names Requiring Human Revision")
    print("=" * 60)
    print("These names indicate potential AI-generated content.")
    print("They are NOT character proposals - they need to be revised or removed.\n")

    books_to_check = []
    if book:
        books_to_check = [CODEX_DIR / f"book_{book}"]
    else:
        books_to_check = sorted(CODEX_DIR.iterdir())

    total_alerts = 0

    for book_dir in books_to_check:
        if not book_dir.is_dir() or not book_dir.name.startswith("book_"):
            continue

        codex_path = book_dir / "codex.yaml"
        if not codex_path.exists():
            continue

        with open(codex_path) as f:
            data = yaml.safe_load(f)

        alerts = data.get("slop_alerts", [])
        if not alerts:
            continue

        book_num = book_dir.name.split("_")[1]
        print(f"{book_dir.name}: {len(alerts)} alert(s)")
        print("-" * 60)

        # Group by banned name
        by_name: dict[str, list] = {}
        for alert in alerts:
            name = alert.get("banned_name", "Unknown")
            if name not in by_name:
                by_name[name] = []
            by_name[name].append(alert)

        for name, name_alerts in sorted(by_name.items()):
            print(f"\n  '{name}' ({len(name_alerts)} occurrence(s)):")
            for alert in name_alerts:
                loc = alert.get("location", "unknown")
                severity = alert.get("severity", "warning")
                context = alert.get("full_context", "")[:70]
                sev_icon = "🔴" if severity == "critical" else "⚠️"
                print(f"    {sev_icon} {loc}")
                print(f"       \"{context}...\"")
            total_alerts += len(name_alerts)

    print(f"\n{'=' * 60}")
    print(f"Total slop alerts: {total_alerts}")
    if total_alerts > 0:
        print("\nAction required: Edit the manuscript to rename or remove these names.")
        print("Banned names are: " + ", ".join(sorted(BANNED_NAMES)))


def approve_entity(entity_id: str, book: int, new_name: Optional[str] = None):
    """Promote a proposed entity to canonical status."""
    codex_path = CODEX_DIR / f"book_{book}" / "codex.yaml"

    if not codex_path.exists():
        print(f"Error: No codex found for book {book}")
        return False

    with open(codex_path) as f:
        data = yaml.safe_load(f)

    proposed = data.get("proposed_entities", {}).get("characters", {})

    if entity_id not in proposed:
        print(f"Error: Entity {entity_id} not found in proposed entities for book {book}")
        print("\nAvailable proposed entities:")
        for eid in list(proposed.keys())[:10]:
            print(f"  - {eid}: {proposed[eid].get('canonical_name')}")
        if len(proposed) > 10:
            print(f"  ... and {len(proposed) - 10} more")
        return False

    entity_data = proposed[entity_id]
    original_name = entity_data.get("canonical_name", "Unknown")

    # Use new name if provided, otherwise keep original
    final_name = new_name if new_name else original_name

    # Generate a new canonical ID (find next available CHAR_XXX)
    existing_ids = set(data.get("characters", {}).keys())
    new_id = None
    for i in range(1, 1000):
        candidate = f"CHAR_{i:03d}"
        if candidate not in existing_ids:
            new_id = candidate
            break

    if not new_id:
        print("Error: Could not generate new entity ID")
        return False

    # Create canonical entry
    canonical_entry = {
        "canonical_name": final_name,
        "status": "canonical",
        "aliases_in_prose": entity_data.get("aliases_in_prose", [final_name]),
        "appearances": entity_data.get("appearances", []),
        "attributes": entity_data.get("attributes", {}),
        "promoted_from": entity_id,
        "promoted_at": datetime.now().isoformat(),
    }

    # Add to canonical characters
    if "characters" not in data:
        data["characters"] = {}
    data["characters"][new_id] = canonical_entry

    # Remove from proposed
    del data["proposed_entities"]["characters"][entity_id]

    # Save updated codex
    with open(codex_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n✓ APPROVED: {original_name}")
    print(f"  Proposed ID: {entity_id}")
    print(f"  New canonical ID: {new_id}")
    print(f"  Final name: {final_name}")
    print(f"  Appearances: {len(canonical_entry['appearances'])}")
    print(f"\nCodex updated: {codex_path}")

    return True


def reject_entity(entity_id: str, book: int):
    """Remove a proposed entity (discard it)."""
    codex_path = CODEX_DIR / f"book_{book}" / "codex.yaml"

    if not codex_path.exists():
        print(f"Error: No codex found for book {book}")
        return False

    with open(codex_path) as f:
        data = yaml.safe_load(f)

    proposed = data.get("proposed_entities", {}).get("characters", {})

    if entity_id not in proposed:
        print(f"Error: Entity {entity_id} not found in proposed entities for book {book}")
        return False

    entity_data = proposed[entity_id]
    name = entity_data.get("canonical_name", "Unknown")
    appearances = len(entity_data.get("appearances", []))

    # Remove from proposed
    del data["proposed_entities"]["characters"][entity_id]

    # Save updated codex
    with open(codex_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n✗ REJECTED: {name}")
    print(f"  Entity ID: {entity_id}")
    print(f"  Appearances discarded: {appearances}")
    print(f"\nCodex updated: {codex_path}")

    return True


def bulk_reject(book: int, pattern: Optional[str] = None, max_appearances: Optional[int] = None):
    """Reject multiple proposed entities matching criteria."""
    codex_path = CODEX_DIR / f"book_{book}" / "codex.yaml"

    if not codex_path.exists():
        print(f"Error: No codex found for book {book}")
        return False

    with open(codex_path) as f:
        data = yaml.safe_load(f)

    proposed = data.get("proposed_entities", {}).get("characters", {})

    to_reject = []
    for entity_id, entity_data in proposed.items():
        name = entity_data.get("canonical_name", "")
        appearances = len(entity_data.get("appearances", []))

        # Check pattern match
        if pattern:
            if not re.search(pattern, name, re.IGNORECASE):
                continue

        # Check max appearances
        if max_appearances is not None:
            if appearances > max_appearances:
                continue

        to_reject.append((entity_id, name, appearances))

    if not to_reject:
        print("No entities match the criteria")
        return False

    print(f"\nEntities to reject ({len(to_reject)}):")
    for entity_id, name, appearances in to_reject:
        print(f"  - {entity_id}: {name} ({appearances} appearances)")

    # Remove all matching entities
    for entity_id, name, _ in to_reject:
        del data["proposed_entities"]["characters"][entity_id]

    # Save updated codex
    with open(codex_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n✗ REJECTED {len(to_reject)} entities")
    print(f"Codex updated: {codex_path}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Prose Indexer for Go Squad",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--summary", action="store_true", help="Reduce log verbosity")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a single prose file")
    ingest_parser.add_argument("file", type=Path, help="Path to prose file")
    ingest_parser.add_argument("--book", type=int, required=True, help="Book number")
    ingest_parser.add_argument("--chapter", type=int, required=True, help="Chapter number")

    # ingest-all command
    ingest_all_parser = subparsers.add_parser("ingest-all", help="Ingest all chapters in a book")
    ingest_all_parser.add_argument("book_dir", type=Path, help="Path to book manuscript directory")
    ingest_all_parser.add_argument("--book", type=int, required=True, help="Book number")

    # status command
    subparsers.add_parser("status", help="Show indexing status")

    # proposed command - list proposed entities
    proposed_parser = subparsers.add_parser("proposed", help="List proposed entities awaiting approval")
    proposed_parser.add_argument("--book", type=int, help="Filter to specific book")

    # approve command
    approve_parser = subparsers.add_parser("approve", help="Promote a proposed entity to canonical")
    approve_parser.add_argument("entity_id", help="Entity ID to approve (e.g., CHAR_900)")
    approve_parser.add_argument("--book", type=int, required=True, help="Book number")
    approve_parser.add_argument("--name", type=str, help="Override the canonical name")

    # reject command
    reject_parser = subparsers.add_parser("reject", help="Discard a proposed entity")
    reject_parser.add_argument("entity_id", help="Entity ID to reject (e.g., CHAR_900)")
    reject_parser.add_argument("--book", type=int, required=True, help="Book number")

    # bulk-reject command
    bulk_reject_parser = subparsers.add_parser("bulk-reject", help="Reject multiple proposed entities")
    bulk_reject_parser.add_argument("--book", type=int, required=True, help="Book number")
    bulk_reject_parser.add_argument("--pattern", type=str, help="Regex pattern to match names")
    bulk_reject_parser.add_argument("--max-appearances", type=int, help="Only reject entities with <= N appearances")

    # slop command - list banned name alerts
    slop_parser = subparsers.add_parser("slop", help="List banned name alerts (AI slop detection)")
    slop_parser.add_argument("--book", type=int, help="Filter to specific book")

    args = parser.parse_args()
    verbose = not args.summary

    if args.command == "ingest":
        ingest_file(args.file, args.book, args.chapter, verbose=verbose)
    elif args.command == "ingest-all":
        ingest_book(args.book_dir, args.book, verbose=verbose)
    elif args.command == "status":
        show_status()
    elif args.command == "proposed":
        list_proposed(book=args.book)
    elif args.command == "approve":
        approve_entity(args.entity_id, args.book, new_name=args.name)
    elif args.command == "reject":
        reject_entity(args.entity_id, args.book)
    elif args.command == "bulk-reject":
        bulk_reject(args.book, pattern=args.pattern, max_appearances=args.max_appearances)
    elif args.command == "slop":
        list_slop_alerts(book=args.book)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
