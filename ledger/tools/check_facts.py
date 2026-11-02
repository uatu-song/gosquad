#!/usr/bin/env python3
"""Validate CANON_FACTS.jsonl: JSON validity, required keys, duplicate ids,
and a status report of everything not settled. Exit 1 if problems found.

Usage: python3 ledger/tools/check_facts.py [path-to-jsonl]
"""
import json
import sys
from pathlib import Path

REQUIRED = {"id", "fact", "value", "sources", "status"}
SETTLED = {"canonical"}
VALID_STATUS = {"canonical", "wobbling", "contradicted", "needs-prose-check"}


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "CANON_FACTS.jsonl"
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
            problems.append(f"line {lineno}: duplicate id '{rid}' (first at line {seen[rid]}) — possible conflicting assertion")
        elif rid:
            seen[rid] = lineno
        status = rec.get("status", "")
        if status not in VALID_STATUS:
            problems.append(f"line {lineno} ({rid}): unknown status '{status}'")
        elif status not in SETTLED:
            unsettled.append((status, rid, rec.get("fact", ""), rec.get("notes", "")))

    print(f"CANON FACTS CHECK — {path.name}: {len(seen)} facts")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  ✗ {p}")
    if unsettled:
        print(f"\nAWAITING RULING ({len(unsettled)}):")
        for status, rid, fact, notes in sorted(unsettled):
            print(f"  [{status}] {rid}: {fact}")
            if notes:
                print(f"      {notes}")
    if not problems and not unsettled:
        print("All facts valid and settled.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
