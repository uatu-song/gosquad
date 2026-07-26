#!/usr/bin/env python3
"""Validate CANON_FACTS.jsonl: JSON validity, required keys, duplicate ids, and a
status report of everything not settled. Exit 1 on problems (not on unsettled —
a wobble is a flag for the Director, not a defect).

Usage: python3 _canon/tools/check_facts.py [--book book_2] [path]
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bookconfig as cfg

REQUIRED = {"id", "fact", "value", "sources", "status"}
SETTLED = {"canonical"}
VALID_STATUS = {"canonical", "wobbling", "contradicted", "needs-prose-check"}


def main() -> int:
    ap = argparse.ArgumentParser()
    cfg.add_book_arg(ap)
    ap.add_argument("path", nargs="?")
    a = ap.parse_args()
    path = Path(a.path) if a.path else cfg.load(a.book).facts_f

    if not path.exists():
        print(f"ERROR: {path} not found")
        return 1

    problems, unsettled, seen = [], [], {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError as e:
            problems.append(f"line {lineno}: invalid JSON ({e})")
            continue
        if "_schema" in rec:
            continue
        missing = REQUIRED - rec.keys()
        if missing:
            problems.append(f"line {lineno} ({rec.get('id', '?')}): missing keys {sorted(missing)}")
        rid = rec.get("id")
        if rid in seen:
            problems.append(f"line {lineno}: duplicate id '{rid}' (first at line {seen[rid]}) "
                            f"— possible conflicting assertion")
        elif rid:
            seen[rid] = lineno
        # A fact with no source is a memory-based claim. That is the thing this
        # whole system exists to make impossible.
        if not rec.get("sources"):
            problems.append(f"line {lineno} ({rid}): no sources — every fact cites its prose site")
        status = rec.get("status", "")
        if status not in VALID_STATUS:
            problems.append(f"line {lineno} ({rid}): unknown status '{status}'")
        elif status not in SETTLED:
            unsettled.append((status, rid, rec.get("fact", ""), rec.get("notes", "")))

    print(f"CANON FACTS — {path.name}: {len(seen)} facts")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  ✗ {p}")
    if unsettled:
        print(f"\nAWAITING A DIRECTOR RULING ({len(unsettled)}):")
        for status, rid, fact, notes in sorted(unsettled):
            print(f"  [{status}] {rid}: {fact}")
            if notes:
                print(f"      {notes}")
    if not problems and not unsettled:
        print("All facts valid and settled." if seen else "No facts filed yet.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
