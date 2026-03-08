#!/usr/bin/env python3
"""
Drift Detector for Go Squad Prose Indexer
Version: 1.0

Compares prose against canonical values in the codex and ENTITY_CATALOG
to detect inconsistencies, contradictions, and knowledge violations.

Usage:
    python drift_detector.py validate <book_N> [--chapter M]
    python drift_detector.py validate-all
    python drift_detector.py report <book_N> [--format html|yaml]
    python drift_detector.py --summary

Output:
    _tools/prose_indexer/logs/{timestamp}_drift_report.yaml
"""

import argparse
import re
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
CHARACTER_STATE_INDEX = PROJECT_ROOT / "7_characters" / "arcs" / "CHARACTER_STATE_INDEX.yaml"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class DriftEntry:
    """Record of a detected drift."""
    drift_id: str
    drift_type: str
    severity: str  # critical, moderate, warning, info
    location: str  # coordinate
    entity_id: Optional[str]
    attribute: Optional[str]
    expected: str
    found: str
    prose_excerpt: str
    resolution: str = "pending"
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class DriftReport:
    """Collection of drift entries for a validation run."""
    book: int
    chapters_validated: list
    timestamp: str
    drift_entries: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def add_drift(self, entry: DriftEntry):
        self.drift_entries.append(entry)

    def generate_summary(self):
        self.summary = {
            "total_drifts": len(self.drift_entries),
            "by_severity": {
                "critical": len([d for d in self.drift_entries if d.severity == "critical"]),
                "moderate": len([d for d in self.drift_entries if d.severity == "moderate"]),
                "warning": len([d for d in self.drift_entries if d.severity == "warning"]),
                "info": len([d for d in self.drift_entries if d.severity == "info"]),
            },
            "by_type": {},
            "entities_affected": list(set(d.entity_id for d in self.drift_entries if d.entity_id)),
        }
        for entry in self.drift_entries:
            self.summary["by_type"][entry.drift_type] = (
                self.summary["by_type"].get(entry.drift_type, 0) + 1
            )


# ============================================================
# DRIFT DETECTOR
# ============================================================

class DriftDetector:
    """Detects drift between prose and canonical values."""

    DRIFT_TYPES = {
        "value_mismatch": {
            "description": "Prose contradicts established canonical value",
            "severity": "critical",
        },
        "alias_unknown": {
            "description": "Name used that doesn't match known aliases",
            "severity": "warning",
        },
        "timeline_inconsistency": {
            "description": "Time marker conflicts with established timeline",
            "severity": "critical",
        },
        "relationship_contradiction": {
            "description": "Relationship described differently than established",
            "severity": "moderate",
        },
        "knowledge_violation": {
            "description": "Character references knowledge before reveal point",
            "severity": "critical",
        },
        "pronoun_ambiguity": {
            "description": "Pronoun could not be confidently resolved",
            "severity": "info",
        },
        "forbidden_association": {
            "description": "Entity associated with forbidden term",
            "severity": "critical",
        },
    }

    def __init__(self, book: int, verbose: bool = True):
        self.book = book
        self.verbose = verbose
        self.drift_counter = 0
        self.report = DriftReport(
            book=book,
            chapters_validated=[],
            timestamp=datetime.now().isoformat(),
        )

        # Load data sources
        self.codex = self._load_codex()
        self.entity_catalog = self._load_entity_catalog()
        self.character_states = self._load_character_states()

    def _load_codex(self) -> dict:
        """Load the codex for this book."""
        codex_path = CODEX_DIR / f"book_{self.book}" / "codex.yaml"
        if codex_path.exists():
            with open(codex_path) as f:
                return yaml.safe_load(f) or {}
        return {}

    def _load_entity_catalog(self) -> dict:
        """Load the entity catalog."""
        if not ENTITY_CATALOG_PATH.exists():
            return {}

        try:
            with open(ENTITY_CATALOG_PATH) as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError:
            # ENTITY_CATALOG may have non-YAML patterns in validation_queries
            # Try to extract just the characters section
            print("Warning: YAML parse error in entity catalog, attempting partial load")
            try:
                with open(ENTITY_CATALOG_PATH) as f:
                    content = f.read()
                import re
                chars_match = re.search(
                    r"^characters:\s*\n(.*?)(?=^[a-z_]+:|^#\s*=|\Z)",
                    content,
                    re.MULTILINE | re.DOTALL
                )
                if chars_match:
                    chars_yaml = "characters:\n" + chars_match.group(1)
                    return yaml.safe_load(chars_yaml) or {}
            except Exception as e:
                print(f"Error loading entity catalog: {e}")
            return {}

    def _load_character_states(self) -> dict:
        """Load character state index."""
        if CHARACTER_STATE_INDEX.exists():
            with open(CHARACTER_STATE_INDEX) as f:
                return yaml.safe_load(f) or {}
        return {}

    def _create_drift_id(self) -> str:
        """Generate unique drift ID."""
        self.drift_counter += 1
        return f"DRIFT_b{self.book}_{self.drift_counter:04d}"

    def validate_book(self, chapters: Optional[list] = None):
        """Run all validations for the book."""
        if not self.codex:
            print(f"No codex found for book {self.book}. Run prose_indexer.py first.")
            return

        indexed_chapters = self.codex.get("meta", {}).get("chapters_indexed", [])
        chapters_to_validate = chapters or indexed_chapters
        self.report.chapters_validated = chapters_to_validate

        print(f"Validating book {self.book}, chapters: {chapters_to_validate}")

        # Run validations
        self._validate_forbidden_associations()
        self._validate_knowledge_timing()
        self._validate_character_attributes()
        self._validate_timeline_consistency()
        self._validate_pronoun_resolution()

        # Generate summary
        self.report.generate_summary()

        return self.report

    def _validate_forbidden_associations(self):
        """Check for forbidden associations from ENTITY_CATALOG."""
        characters = self.entity_catalog.get("characters", {})

        # Common pronouns that need special handling - they often refer to
        # other characters in the same context, not the character being tracked
        PRONOUN_TERMS = {"he", "him", "his", "she", "her", "hers", "they", "them", "their"}

        for entity_id, char_data in characters.items():
            forbidden = char_data.get("forbidden_associations", [])
            if not forbidden:
                continue

            canonical_name = char_data.get("canonical_name", "")
            aliases = [a.lower() for a in char_data.get("aliases", [])]
            all_names = [canonical_name.lower()] + aliases

            # Check codex appearances for this character
            codex_char = self.codex.get("characters", {}).get(entity_id, {})
            for appearance in codex_char.get("appearances", []):
                context = appearance.get("context", "").lower()
                ref_form = appearance.get("reference_form", "").lower()

                for forbidden_term in forbidden:
                    term_lower = forbidden_term.lower()

                    # Special handling for pronoun-based forbidden associations
                    # (e.g., Harriet should not be referred to as "he")
                    # Only flag if the pronoun appears to reference this character
                    if term_lower in PRONOUN_TERMS:
                        # Only flag if the reference_form IS the forbidden pronoun
                        # (meaning this character was tracked via that pronoun)
                        if ref_form == term_lower:
                            self.report.add_drift(DriftEntry(
                                drift_id=self._create_drift_id(),
                                drift_type="forbidden_association",
                                severity="critical",
                                location=appearance.get("location", "unknown"),
                                entity_id=entity_id,
                                attribute=None,
                                expected=f"Character should not be referred to as '{forbidden_term}'",
                                found=f"Pronoun '{forbidden_term}' used for {canonical_name}",
                                prose_excerpt=appearance.get("context", "")[:200],
                                notes=f"Character {canonical_name} has forbidden pronoun: {forbidden_term}. See canonical_truth in ENTITY_CATALOG.",
                            ))
                            if self.verbose:
                                print(f"[CRITICAL] Forbidden pronoun: {canonical_name} referred to as '{forbidden_term}'")
                    else:
                        # Non-pronoun forbidden terms: check if they appear in context
                        if term_lower in context:
                            self.report.add_drift(DriftEntry(
                                drift_id=self._create_drift_id(),
                                drift_type="forbidden_association",
                                severity="critical",
                                location=appearance.get("location", "unknown"),
                                entity_id=entity_id,
                                attribute=None,
                                expected=f"No mention of '{forbidden_term}'",
                                found=f"Found '{forbidden_term}' in context",
                                prose_excerpt=appearance.get("context", "")[:200],
                                notes=f"Character {canonical_name} has forbidden association: {forbidden_term}. See canonical_truth in ENTITY_CATALOG.",
                            ))
                            if self.verbose:
                                print(f"[CRITICAL] Forbidden association: {canonical_name} + '{forbidden_term}'")

    def _validate_knowledge_timing(self):
        """Check that characters don't reference knowledge before they learn it."""
        characters = self.entity_catalog.get("characters", {})

        for entity_id, char_data in characters.items():
            forbidden_before = char_data.get("forbidden_knowledge_before", {})
            if not forbidden_before:
                continue

            codex_char = self.codex.get("characters", {}).get(entity_id, {})

            for knowledge_item, reveal_point in forbidden_before.items():
                # Parse reveal point (e.g., "book2_ch2" -> book 2, chapter 2)
                reveal_book, reveal_chapter = self._parse_knowledge_point(reveal_point)

                # Check all appearances before reveal point
                for appearance in codex_char.get("appearances", []):
                    loc = appearance.get("location", "")
                    app_book, app_chapter = self._parse_location(loc)

                    if app_book is None or reveal_book is None:
                        continue

                    # Is this appearance before the reveal?
                    is_before = (app_book < reveal_book) or (
                        app_book == reveal_book and app_chapter < reveal_chapter
                    )

                    if is_before:
                        context = appearance.get("context", "").lower()
                        # Check if context mentions the forbidden knowledge
                        if self._context_contains_knowledge(context, knowledge_item):
                            self.report.add_drift(DriftEntry(
                                drift_id=self._create_drift_id(),
                                drift_type="knowledge_violation",
                                severity="critical",
                                location=loc,
                                entity_id=entity_id,
                                attribute=knowledge_item,
                                expected=f"Knowledge not available until {reveal_point}",
                                found=f"Referenced at {loc}",
                                prose_excerpt=appearance.get("context", "")[:200],
                                notes=f"{char_data.get('canonical_name')} should not know about '{knowledge_item}' before {reveal_point}",
                            ))
                            if self.verbose:
                                print(f"[CRITICAL] Knowledge violation: {char_data.get('canonical_name')} knows '{knowledge_item}' too early")

    def _parse_knowledge_point(self, point: str) -> tuple:
        """Parse knowledge point like 'book2_ch2' -> (2, 2)."""
        match = re.match(r"book(\d+)_ch(\d+)", point)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def _parse_location(self, loc: str) -> tuple:
        """Parse location coordinate -> (book, chapter)."""
        match = re.match(r"b(\d+):ch(\d+)", loc)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def _context_contains_knowledge(self, context: str, knowledge_item: str) -> bool:
        """Check if context mentions forbidden knowledge."""
        # Convert knowledge_item to searchable terms
        # e.g., "geneva_is_bellatrix" -> ["geneva", "bellatrix"]
        terms = knowledge_item.lower().replace("_", " ").split()
        # Check if multiple terms appear together
        context_lower = context.lower()
        matches = sum(1 for term in terms if term in context_lower)
        return matches >= 2  # At least 2 terms must match

    def _validate_character_attributes(self):
        """Check character attributes against canonical values."""
        codex_chars = self.codex.get("characters", {})
        catalog_chars = self.entity_catalog.get("characters", {})

        for entity_id, codex_data in codex_chars.items():
            catalog_data = catalog_chars.get(entity_id, {})

            # Check baseline tracking (specific to Ahdia)
            baseline_tracking = catalog_data.get("book2_baseline_tracking", {})
            for chapter_key, baseline_data in baseline_tracking.items():
                # Extract chapter number
                chapter_match = re.match(r"ch(\d+)", chapter_key)
                if not chapter_match:
                    continue
                chapter_num = int(chapter_match.group(1))

                # Look for baseline mentions in codex
                for attr_name, attr_data in codex_data.get("attributes", {}).items():
                    if "baseline" in attr_name.lower():
                        for mention in attr_data.get("mentions", []):
                            loc = mention.get("location", "")
                            _, mention_chapter = self._parse_location(loc)
                            if mention_chapter == chapter_num:
                                prose_value = mention.get("value_in_prose", "")
                                expected_start = baseline_data.get("start", "")
                                expected_end = baseline_data.get("end", "")

                                # Check for mismatch
                                if prose_value and expected_start:
                                    if expected_start not in prose_value and expected_end not in prose_value:
                                        self.report.add_drift(DriftEntry(
                                            drift_id=self._create_drift_id(),
                                            drift_type="value_mismatch",
                                            severity="critical",
                                            location=loc,
                                            entity_id=entity_id,
                                            attribute=attr_name,
                                            expected=f"Baseline: {expected_start} -> {expected_end}",
                                            found=prose_value,
                                            prose_excerpt=mention.get("context", "")[:200] if mention.get("context") else "",
                                        ))

    def _validate_timeline_consistency(self):
        """Check time markers for internal consistency."""
        time_markers = self.codex.get("time_markers", [])

        if len(time_markers) < 2:
            return

        # Group by chapter
        by_chapter = {}
        for marker in time_markers:
            loc = marker.get("location", "")
            _, chapter = self._parse_location(loc)
            if chapter:
                by_chapter.setdefault(chapter, []).append(marker)

        # Check each chapter for time jumps
        for chapter, markers in by_chapter.items():
            # Sort by position
            sorted_markers = sorted(markers, key=lambda m: m.get("chapter_timeline_position", 0))

            prev_normalized = None
            prev_marker = None

            for marker in sorted_markers:
                if marker.get("marker_type") != "absolute":
                    continue

                normalized = marker.get("normalized")
                if not normalized:
                    continue

                if prev_normalized:
                    # Compare times (simple string comparison works for HH:MM:SS)
                    if normalized < prev_normalized:
                        # Time went backwards without explicit indicator
                        self.report.add_drift(DriftEntry(
                            drift_id=self._create_drift_id(),
                            drift_type="timeline_inconsistency",
                            severity="critical",
                            location=marker.get("location", "unknown"),
                            entity_id=None,
                            attribute="time",
                            expected=f"Time after {prev_marker.get('raw_text')} ({prev_normalized})",
                            found=f"{marker.get('raw_text')} ({normalized})",
                            prose_excerpt=f"Previous: {prev_marker.get('raw_text')} at {prev_marker.get('location')}",
                            notes="Time appears to go backwards without flashback or scene break indicator",
                        ))
                        if self.verbose:
                            print(f"[CRITICAL] Timeline inconsistency in chapter {chapter}")

                prev_normalized = normalized
                prev_marker = marker

    def _validate_pronoun_resolution(self):
        """Flag unresolved or ambiguous pronouns."""
        codex_chars = self.codex.get("characters", {})

        for entity_id, data in codex_chars.items():
            for appearance in data.get("appearances", []):
                if appearance.get("reference_type") == "pronoun":
                    resolution = appearance.get("pronoun_resolution", {})
                    confidence = resolution.get("confidence", "unknown")

                    if confidence in ("low", "ambiguous"):
                        self.report.add_drift(DriftEntry(
                            drift_id=self._create_drift_id(),
                            drift_type="pronoun_ambiguity",
                            severity="info",
                            location=appearance.get("location", "unknown"),
                            entity_id=entity_id,
                            attribute=None,
                            expected="Clear pronoun reference",
                            found=f"Ambiguous ({confidence}): {appearance.get('reference_form')}",
                            prose_excerpt=appearance.get("context", "")[:200],
                            notes=f"Candidates: {resolution.get('candidates', [])}",
                        ))

    def save_report(self, format: str = "yaml") -> Path:
        """Save drift report to file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_drift_report_book{self.book}.{format}"
        report_path = LOGS_DIR / filename

        if format == "yaml":
            output = {
                "meta": {
                    "book": self.report.book,
                    "chapters_validated": self.report.chapters_validated,
                    "timestamp": self.report.timestamp,
                    "generated_at": datetime.now().isoformat(),
                },
                "summary": self.report.summary,
                "drift_entries": [
                    {
                        "drift_id": d.drift_id,
                        "drift_type": d.drift_type,
                        "severity": d.severity,
                        "location": d.location,
                        "entity_id": d.entity_id,
                        "attribute": d.attribute,
                        "expected": d.expected,
                        "found": d.found,
                        "prose_excerpt": d.prose_excerpt,
                        "resolution": d.resolution,
                        "notes": d.notes,
                    }
                    for d in self.report.drift_entries
                ],
            }

            with open(report_path, "w") as f:
                yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        elif format == "html":
            html = self._generate_html_report()
            with open(report_path, "w") as f:
                f.write(html)

        print(f"\nDrift report saved to: {report_path}")
        return report_path

    def _generate_html_report(self) -> str:
        """Generate HTML drift report."""
        severity_colors = {
            "critical": "#ff4444",
            "moderate": "#ffaa00",
            "warning": "#ffff00",
            "info": "#aaaaff",
        }

        entries_html = ""
        for d in sorted(self.report.drift_entries, key=lambda x: (
            {"critical": 0, "moderate": 1, "warning": 2, "info": 3}.get(x.severity, 4),
            x.location
        )):
            color = severity_colors.get(d.severity, "#ffffff")
            entries_html += f"""
            <tr style="background-color: {color}22;">
                <td><strong>{d.drift_id}</strong></td>
                <td><span style="background-color: {color}; padding: 2px 6px; border-radius: 3px;">{d.severity.upper()}</span></td>
                <td>{d.drift_type}</td>
                <td><code>{d.location}</code></td>
                <td>{d.entity_id or '-'}</td>
                <td>{d.expected}</td>
                <td>{d.found}</td>
                <td><small>{d.prose_excerpt[:100]}...</small></td>
            </tr>
            """

        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Drift Report - Book {self.report.book}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 20px; background: #1a1a2e; color: #eee; }}
        h1, h2 {{ color: #00d4ff; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
        th {{ background: #16213e; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }}
        .summary-card {{ background: #16213e; padding: 20px; border-radius: 8px; text-align: center; }}
        .summary-card h3 {{ margin: 0; color: #888; font-size: 14px; }}
        .summary-card .value {{ font-size: 36px; font-weight: bold; margin: 10px 0; }}
        .critical {{ color: #ff4444; }}
        .moderate {{ color: #ffaa00; }}
        .warning {{ color: #ffff00; }}
        .info {{ color: #aaaaff; }}
        code {{ background: #333; padding: 2px 4px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>Drift Report - Book {self.report.book}</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Chapters validated: {self.report.chapters_validated}</p>

    <div class="summary">
        <div class="summary-card">
            <h3>Total Drifts</h3>
            <div class="value">{self.report.summary.get('total_drifts', 0)}</div>
        </div>
        <div class="summary-card">
            <h3>Critical</h3>
            <div class="value critical">{self.report.summary.get('by_severity', {}).get('critical', 0)}</div>
        </div>
        <div class="summary-card">
            <h3>Moderate</h3>
            <div class="value moderate">{self.report.summary.get('by_severity', {}).get('moderate', 0)}</div>
        </div>
        <div class="summary-card">
            <h3>Warnings</h3>
            <div class="value warning">{self.report.summary.get('by_severity', {}).get('warning', 0)}</div>
        </div>
    </div>

    <h2>Drift Entries</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Severity</th>
            <th>Type</th>
            <th>Location</th>
            <th>Entity</th>
            <th>Expected</th>
            <th>Found</th>
            <th>Excerpt</th>
        </tr>
        {entries_html}
    </table>
</body>
</html>
"""

    def print_summary(self):
        """Print drift summary to console."""
        print("\n" + "=" * 60)
        print(f"DRIFT REPORT - Book {self.book}")
        print("=" * 60)
        print(f"Chapters validated: {self.report.chapters_validated}")
        print(f"Total drifts found: {self.report.summary.get('total_drifts', 0)}")
        print("\nBy Severity:")
        for severity, count in self.report.summary.get("by_severity", {}).items():
            if count > 0:
                print(f"  {severity.upper()}: {count}")
        print("\nBy Type:")
        for dtype, count in self.report.summary.get("by_type", {}).items():
            print(f"  {dtype}: {count}")

        if self.report.summary.get("entities_affected"):
            print(f"\nEntities affected: {', '.join(self.report.summary['entities_affected'])}")

        # Print critical drifts
        critical = [d for d in self.report.drift_entries if d.severity == "critical"]
        if critical:
            print("\n" + "-" * 60)
            print("CRITICAL DRIFTS (require immediate attention):")
            print("-" * 60)
            for d in critical:
                print(f"\n[{d.drift_id}] {d.drift_type}")
                print(f"  Location: {d.location}")
                print(f"  Entity: {d.entity_id}")
                print(f"  Expected: {d.expected}")
                print(f"  Found: {d.found}")
                if d.notes:
                    print(f"  Notes: {d.notes}")


# ============================================================
# MAIN CLI
# ============================================================

def validate_book(book: int, chapters: Optional[list] = None, verbose: bool = True, format: str = "yaml"):
    """Run validation on a book."""
    detector = DriftDetector(book, verbose=verbose)
    detector.validate_book(chapters)
    detector.save_report(format=format)
    detector.print_summary()


def main():
    parser = argparse.ArgumentParser(
        description="Drift Detector for Go Squad Prose Indexer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--summary", action="store_true", help="Reduce output verbosity")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a book's codex against canonical values")
    validate_parser.add_argument("book", type=int, help="Book number (e.g., 2)")
    validate_parser.add_argument("--chapter", type=int, nargs="+", help="Specific chapters to validate")
    validate_parser.add_argument("--format", choices=["yaml", "html"], default="yaml", help="Output format")

    # validate-all command
    subparsers.add_parser("validate-all", help="Validate all indexed books")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate drift report")
    report_parser.add_argument("book", type=int, help="Book number")
    report_parser.add_argument("--format", choices=["yaml", "html"], default="yaml")

    args = parser.parse_args()
    verbose = not args.summary

    if args.command == "validate":
        validate_book(args.book, chapters=args.chapter, verbose=verbose, format=args.format)
    elif args.command == "validate-all":
        # Find all codex files
        for book_dir in sorted(CODEX_DIR.iterdir()):
            if book_dir.is_dir() and book_dir.name.startswith("book_"):
                book_num = int(book_dir.name.split("_")[1])
                codex_path = book_dir / "codex.yaml"
                if codex_path.exists():
                    print(f"\n{'=' * 60}")
                    print(f"Validating Book {book_num}")
                    print("=" * 60)
                    validate_book(book_num, verbose=verbose)
    elif args.command == "report":
        validate_book(args.book, verbose=verbose, format=args.format)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
