#!/usr/bin/env python3
"""
Go Squad Knowledge Loader
Dynamically loads and presents all knowledge base content for the Go Squad series.

Usage:
    python3 gosquad_knowledge_loader.py              # Full load
    python3 gosquad_knowledge_loader.py --summary    # Quick summary only
    python3 gosquad_knowledge_loader.py --category characters  # Specific category
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class KnowledgeFile:
    """Represents a single knowledge base file"""
    path: Path
    category: str
    name: str
    content: str = ""
    size_lines: int = 0
    metadata: Dict = field(default_factory=dict)

    def load(self):
        """Load file content"""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.size_lines = len(self.content.splitlines())
        except Exception as e:
            self.content = f"[Error loading: {e}]"
            self.size_lines = 0

    def summary(self) -> str:
        """Generate brief summary"""
        lines = self.content.splitlines()
        preview_lines = min(5, len(lines))
        preview = '\n'.join(lines[:preview_lines])
        return f"{self.name} ({self.size_lines} lines)\n{preview}"


@dataclass
class KnowledgeBase:
    """Complete Go Squad knowledge base"""
    root_path: Path
    files: Dict[str, List[KnowledgeFile]] = field(default_factory=lambda: defaultdict(list))
    metadata: Dict = field(default_factory=dict)

    # Category definitions - maps directory patterns to categories
    CATEGORY_PATTERNS = {
        'character_profiles': 'characters',
        'character_arcs': 'character_arcs',
        'story_bibles/artifacts': 'artifacts',
        'story_bibles/organizations': 'organizations',
        'story_bibles/locations': 'locations',
        'story_bibles/powers and cost': 'powers',
        'story_bibles/timeline': 'timeline',
        'story_bibles/book 2': 'book2_planning',
        'story_bibles/book 3': 'book3_planning',
        'story_bibles/book 4': 'book4_planning',
        'themes': 'themes',
        'TTRPG': 'ttrpg',
        '.gosquad': 'knowledge_base',
    }

    # Important root files
    ROOT_FILES = [
        'SERIES_SYNOPSIS.md',
        'README.md',
        'book1_manuscript.txt',
        'KNOWLEDGE_LOADER_README.md',
    ]

    def discover_files(self):
        """Automatically discover all knowledge base files"""
        print("🔍 Discovering knowledge base files...")

        # Scan for categorized files
        for pattern, category in self.CATEGORY_PATTERNS.items():
            search_path = self.root_path / pattern
            if search_path.exists():
                self._scan_directory(search_path, category)

        # Scan root files
        for filename in self.ROOT_FILES:
            file_path = self.root_path / filename
            if file_path.exists():
                kf = KnowledgeFile(
                    path=file_path,
                    category='root',
                    name=filename
                )
                self.files['root'].append(kf)

        # Calculate metadata
        self.metadata['total_files'] = sum(len(files) for files in self.files.values())
        self.metadata['categories'] = list(self.files.keys())

        print(f"✓ Discovered {self.metadata['total_files']} files across {len(self.metadata['categories'])} categories")

    def _scan_directory(self, directory: Path, category: str):
        """Recursively scan directory for markdown and text files"""
        if not directory.exists():
            return

        for item in directory.rglob('*'):
            if item.is_file() and item.suffix in ['.md', '.txt', '.json']:
                # Skip hidden files and system files
                if any(part.startswith('.') for part in item.parts):
                    if not any(part == '.gosquad' for part in item.parts):
                        continue

                relative_path = item.relative_to(self.root_path)
                kf = KnowledgeFile(
                    path=item,
                    category=category,
                    name=str(relative_path)
                )
                self.files[category].append(kf)

    def load_all(self, categories: Optional[List[str]] = None):
        """Load content from all or specific categories"""
        categories_to_load = categories or self.files.keys()

        total_files = sum(len(self.files[cat]) for cat in categories_to_load if cat in self.files)
        loaded = 0

        print(f"\n📚 Loading {total_files} files...")

        for category in categories_to_load:
            if category not in self.files:
                continue

            print(f"\n  Loading {category}...")
            for kf in self.files[category]:
                kf.load()
                loaded += 1
                if loaded % 10 == 0:
                    print(f"    {loaded}/{total_files} files loaded...")

        print(f"✓ Loaded {loaded} files\n")

    def generate_summary(self) -> str:
        """Generate comprehensive summary of knowledge base"""
        lines = []
        lines.append("=" * 80)
        lines.append("GO SQUAD KNOWLEDGE BASE SUMMARY")
        lines.append("=" * 80)
        lines.append("")

        # Overall stats
        total_lines = sum(kf.size_lines for files in self.files.values() for kf in files)
        lines.append(f"Total Files: {self.metadata['total_files']}")
        lines.append(f"Total Lines: {total_lines:,}")
        lines.append(f"Categories: {len(self.metadata['categories'])}")
        lines.append("")

        # Category breakdown
        lines.append("CATEGORY BREAKDOWN:")
        lines.append("-" * 80)

        for category in sorted(self.files.keys()):
            files = self.files[category]
            category_lines = sum(kf.size_lines for kf in files)
            lines.append(f"\n{category.upper()} ({len(files)} files, {category_lines:,} lines)")
            lines.append("-" * 40)

            for kf in sorted(files, key=lambda x: x.name):
                lines.append(f"  • {kf.name} ({kf.size_lines} lines)")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    def generate_detailed_report(self, category: Optional[str] = None) -> str:
        """Generate detailed report with content previews"""
        lines = []
        lines.append("=" * 80)
        lines.append("GO SQUAD KNOWLEDGE BASE - DETAILED REPORT")
        lines.append("=" * 80)
        lines.append("")

        categories_to_show = [category] if category else sorted(self.files.keys())

        for cat in categories_to_show:
            if cat not in self.files:
                lines.append(f"⚠ Category '{cat}' not found")
                continue

            lines.append("")
            lines.append("=" * 80)
            lines.append(f"CATEGORY: {cat.upper()}")
            lines.append("=" * 80)
            lines.append("")

            for kf in sorted(self.files[cat], key=lambda x: x.name):
                lines.append("-" * 80)
                lines.append(f"FILE: {kf.name}")
                lines.append(f"Size: {kf.size_lines} lines")
                lines.append("-" * 80)

                # Show first 20 lines as preview
                preview_lines = kf.content.splitlines()[:20]
                lines.append("\n".join(preview_lines))

                if kf.size_lines > 20:
                    lines.append(f"\n... ({kf.size_lines - 20} more lines)")

                lines.append("")

        return "\n".join(lines)

    def get_essential_context(self) -> str:
        """Generate essential context for quick catch-up"""
        lines = []
        lines.append("=" * 80)
        lines.append("GO SQUAD - ESSENTIAL CONTEXT")
        lines.append("=" * 80)
        lines.append("")

        # Load key files for context - ordered by importance
        essential_files = [
            # Core synopsis
            ('SERIES_SYNOPSIS.md', None, 200),

            # Critical Book 2 planning (Geneva/Bellatrix reveal)
            ('story_bibles/book 2/Time_Loop_Utopia_Iterations.md', None, 150),
            ('story_bibles/book 2/CANON.md', 100, 50),

            # Book 3 key moments
            ('story_bibles/book 3/book3_ahdia_stranded_beats.md', None, 100),
            ('story_bibles/book 3/BOOK3_PLANNING_STATUS.md', None, 100),

            # Book 4 current state
            ('story_bibles/book 4/SESSION_DECISIONS_2025-11-24.md', None, 150),
            ('story_bibles/book 4/EMOTIONAL_ARC_AHDIA_ARRYU.md', None, 80),

            # Key character profiles
            ('character_profiles/Ahdia Bacchus (Auerbach)', None, 100),
            ('character_profiles/Bellatrix_Naima.md', None, 80),

            # Critical worldbuilding
            ('story_bibles/artifacts/Hyper_Seed.md', None, 50),
        ]

        for file_info in essential_files:
            if len(file_info) == 3:
                filename, offset, limit = file_info
            else:
                filename, limit = file_info
                offset = None

            file_path = self.root_path / filename
            if file_path.exists():
                lines.append("")
                lines.append("=" * 80)
                lines.append(f"FILE: {filename}")
                lines.append("=" * 80)
                lines.append("")

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_lines = content.splitlines()

                    # Handle offset and limit
                    start = offset if offset is not None else 0
                    end = start + limit if limit is not None else len(content_lines)

                    preview = '\n'.join(content_lines[start:end])
                    lines.append(preview)

                    total_lines = len(content_lines)
                    shown_lines = end - start
                    if shown_lines < total_lines:
                        remaining = total_lines - end
                        lines.append(f"\n... ({remaining} more lines, {total_lines} total)")

                lines.append("")
            else:
                lines.append(f"⚠ Essential file not found: {filename}")
                lines.append("")

        return "\n".join(lines)

    def search(self, query: str) -> List[Tuple[KnowledgeFile, List[str]]]:
        """Search for query across all loaded files"""
        results = []
        query_lower = query.lower()

        for category, files in self.files.items():
            for kf in files:
                if not kf.content:
                    kf.load()

                matching_lines = [
                    line for line in kf.content.splitlines()
                    if query_lower in line.lower()
                ]

                if matching_lines:
                    results.append((kf, matching_lines))

        return results

    def export_json(self, output_path: Path):
        """Export knowledge base as JSON"""
        data = {
            'metadata': self.metadata,
            'categories': {}
        }

        for category, files in self.files.items():
            data['categories'][category] = [
                {
                    'name': kf.name,
                    'path': str(kf.path),
                    'size_lines': kf.size_lines,
                    'content': kf.content
                }
                for kf in files
            ]

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Exported knowledge base to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Load and present Go Squad knowledge base',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--summary',
        action='store_true',
        help='Show summary only (no content loading)'
    )

    parser.add_argument(
        '--category',
        type=str,
        help='Load specific category only'
    )

    parser.add_argument(
        '--essential',
        action='store_true',
        help='Show essential context only (fast catch-up)'
    )

    parser.add_argument(
        '--search',
        type=str,
        help='Search for query across all files'
    )

    parser.add_argument(
        '--export',
        type=str,
        help='Export knowledge base to JSON file'
    )

    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Show detailed report with content previews'
    )

    args = parser.parse_args()

    # Initialize knowledge base
    # Go up two levels from editor_suite/knowledge_system/ to workspace root
    root_path = Path(__file__).parent.parent.parent
    kb = KnowledgeBase(root_path=root_path)

    # Discover files
    kb.discover_files()

    # Handle different modes
    if args.essential:
        print(kb.get_essential_context())
        return

    # Load files
    categories = [args.category] if args.category else None
    kb.load_all(categories=categories)

    if args.search:
        print(f"\n🔍 Searching for '{args.search}'...\n")
        results = kb.search(args.search)

        if results:
            print(f"Found {len(results)} files with matches:\n")
            for kf, lines in results:
                print(f"📄 {kf.name} ({len(lines)} matches)")
                for line in lines[:3]:  # Show first 3 matches
                    print(f"   {line.strip()}")
                if len(lines) > 3:
                    print(f"   ... ({len(lines) - 3} more matches)")
                print()
        else:
            print("No matches found.")
        return

    if args.export:
        output_path = Path(args.export)
        kb.export_json(output_path)
        return

    # Generate output
    if args.summary:
        print(kb.generate_summary())
    elif args.detailed:
        print(kb.generate_detailed_report(category=args.category))
    else:
        # Default: show essential context
        print(kb.get_essential_context())


if __name__ == '__main__':
    main()
