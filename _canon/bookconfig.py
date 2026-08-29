"""Single source of truth for THIS project's paths.

Every tool in _canon/tools/ imports from here. No tool carries a literal path.
The porting failure this prevents: the kit these tools descend from hardcoded
`RESONANCE/data/...` and `RESONANCE/chapters_final/RESONANCE_*.txt` inline in
five places, so `audit.py` crashed and `check_typography.py` scanned zero files
and printed "house typography intact ✓". Zero read as clean. Never again — see
prose_files(), which refuses to return an empty list silently.
"""
import argparse
import glob
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required:  pip install pyyaml --break-system-packages")

CANON_HOME = Path(__file__).resolve().parent          # <repo>/_canon
PROJECT_ROOT = Path(os.environ.get("BOOK_ROOT", CANON_HOME.parent))
REGISTRY = CANON_HOME / "books.yaml"


def _registry():
    with open(REGISTRY, encoding="utf-8") as f:
        return yaml.safe_load(f)


class Book:
    """Resolved paths for one book. Attribute access, no dict spelunking."""

    def __init__(self, key, spec, typography):
        self.key = key
        self.title = spec.get("title", key)
        self.status = spec.get("status", "unknown")
        self.prose_expected = bool(spec.get("prose_expected", True))
        self.manuscript_dir = PROJECT_ROOT / spec["manuscript_dir"]
        self.chapter_glob = spec.get("chapter_glob", "*.txt")
        self.chapter_num_re = spec.get("chapter_num_re", r"(\d+)")
        self.data_dir = PROJECT_ROOT / spec["data_dir"]
        self.typography = typography

    # ── the canon layer ──────────────────────────────────────────────────────
    @property
    def index_f(self):
        return self.data_dir / "INDEX.yaml"

    @property
    def rules_f(self):
        return self.data_dir / "RULES.yaml"

    @property
    def series_rules_f(self):
        """Series-wide rules (style tics, cross-book bans) — apply to EVERY
        book's prose. One file, so a rule fix lands everywhere at once instead
        of drifting across per-book copies. Book-local RULES.yaml overrides a
        series rule with the same id."""
        return PROJECT_ROOT / "canon" / "series" / "RULES.yaml"

    @property
    def chapter_index_f(self):
        return self.data_dir / "CHAPTER_INDEX.yaml"

    @property
    def facts_f(self):
        return self.data_dir / "CANON_FACTS.jsonl"

    @property
    def promises_f(self):
        return self.data_dir / "PROMISES.jsonl"

    @property
    def decisions_f(self):
        return self.data_dir / "DECISIONS_LOG.md"

    @property
    def changelog_f(self):
        return self.data_dir / "CODEX_CHANGELOG.md"

    @property
    def constraints_f(self):
        """Optional. Absent is fine — CON- codes simply won't exist."""
        return self.data_dir / "CONSTRAINTS.yaml"

    def canon_files(self):
        """Every file the codex layer owns — what audit.py greps for fossils."""
        out = []
        for pat in ("*.yaml", "*.md"):
            out += sorted(glob.glob(str(self.data_dir / pat)))
        # RULES.yaml *describes* the fossils; the changelog records their removal.
        # Neither is a fossil. Excluding them is why this list is a function.
        return [f for f in out
                if os.path.basename(f) not in ("RULES.yaml", "CODEX_CHANGELOG.md")]

    # ── the prose ────────────────────────────────────────────────────────────
    def prose_files(self, strict=True):
        """The manuscript, in chapter order.

        strict=True raises when a book that SHOULD have prose yields zero files.
        That is the whole point: a mispointed glob and a genuinely pre-prose book
        look identical from the outside, and only one of them is fine.
        """
        found = sorted(glob.glob(str(self.manuscript_dir / self.chapter_glob)))
        if not found and self.prose_expected and strict:
            raise SystemExit(
                f"\n  ✗ NO PROSE FOUND for '{self.key}' — but books.yaml says "
                f"prose_expected: true.\n"
                f"    glob: {self.manuscript_dir}/{self.chapter_glob}\n"
                f"    Either the glob is wrong or the book moved. Refusing to "
                f"report 'clean' on zero files.\n")
        return sorted(found, key=self.chapter_num)

    def chapter_num(self, path):
        m = re.search(self.chapter_num_re, os.path.basename(str(path)))
        return int(m.group(1)) if m else 999

    def chapter_stem(self, path):
        return os.path.basename(str(path)).rsplit(".", 1)[0]

    def short(self, path):
        n = self.chapter_num(path)
        return f"CH{n:02d}" if n != 999 else self.chapter_stem(path)

    def rel(self, path):
        return os.path.relpath(str(path), PROJECT_ROOT)


def load(book_key=None):
    reg = _registry()
    key = book_key or os.environ.get("BOOK") or reg.get("default_book")
    books = reg.get("books") or {}
    if key not in books:
        sys.exit(f"unknown book {key!r}. Registered: {', '.join(sorted(books))}")
    return Book(key, books[key], reg.get("typography") or {})


def add_book_arg(ap: argparse.ArgumentParser):
    """Every tool takes --book. One line, so no tool forgets."""
    ap.add_argument("--book", default=None,
                    help="book key from _canon/books.yaml (default: $BOOK or registry default)")
    return ap


# ── TYPOGRAPHY NORMALISATION ─────────────────────────────────────────────────
# Prose may use curly quotes; patterns get written with straight ones. A grep
# that cannot fire returns zero, and zero reads as clean. Every comparison in
# every tool normalises first — EXCEPT check_typography.py, which must see raw
# bytes (normalising there would make it flag everything or nothing).
def norm(s):
    return (s.replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"')
             .replace("—", "--").replace("–", "-")
             .replace("…", "...")
             # Chicago spaced ellipsis (ruled 2026-08-29) collapses to "..." like
             # the … glyph does. Without this the sentence splitter, which breaks
             # on \s+, splits INSIDE every ellipsis — NBSP is whitespace — and
             # short-burst inflates (43.1 -> 48.2 book-wide when Book 1 converted).
             # That is the mid-ellipsis split the April fix removed, arriving by a
             # different door.
             .replace(".\u00a0.\u00a0.", "...").replace(". . .", "..."))
