#!/usr/bin/env python3
"""Report on PROMISES.jsonl: open setups (candidate plot holes at end of draft),
verify-status items, open questions. Red-herring / unimportant entries are exempt
and counted only — ONLY the Director assigns those. Exit 1 on schema problems.

Usage: python3 _canon/tools/check_promises.py [--book book_2] [path]
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bookconfig as cfg

REQUIRED = {"id", "type", "promise", "status"}
EXEMPT = {"red-herring", "unimportant"}
VALID_STATUS = {"open", "paid", "verify", "abandoned"} | EXEMPT
VALID_TYPE = {"setup-awaiting-payoff", "payoff-needing-setup", "open-question"}


def main() -> int:
    ap = argparse.ArgumentParser()
    cfg.add_book_arg(ap)
    ap.add_argument("path", nargs="?")
    a = ap.parse_args()
    path = Path(a.path) if a.path else cfg.load(a.book).promises_f

    if not path.exists():
        print(f"ERROR: {path} not found")
        return 1

    problems = []
    buckets = {"open-setups": [], "verify": [], "open-questions": [], "exempt": [], "paid": []}
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
            continue
        if rec["status"] not in VALID_STATUS:
            problems.append(f"line {lineno} ({rec['id']}): unknown status '{rec['status']}'")
        if rec["type"] not in VALID_TYPE:
            problems.append(f"line {lineno} ({rec['id']}): unknown type '{rec['type']}'")
        # A payoff claimed without a citation is the class of error that lets an
        # unpaid setup read as paid for the rest of the draft.
        if rec["status"] == "paid" and not rec.get("payoff"):
            problems.append(f"line {lineno} ({rec['id']}): status 'paid' with no payoff citation")
        s, t = rec["status"], rec["type"]
        if s in EXEMPT:
            buckets["exempt"].append(rec)
        elif s == "paid":
            buckets["paid"].append(rec)
        elif s == "verify":
            buckets["verify"].append(rec)
        elif t == "open-question":
            buckets["open-questions"].append(rec)
        elif s == "open":
            buckets["open-setups"].append(rec)

    print(f"PROMISES — {path.name}")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  ✗ {p}")

    def show(title, items):
        if items:
            print(f"\n{title} ({len(items)}):")
            for r in items:
                print(f"  • [{r['type']}] {r['id']}: {r['promise']}")

    show("OPEN SETUPS — candidate plot holes at end of draft", buckets["open-setups"])
    show("VERIFY — payoffs whose setups need prose confirmation", buckets["verify"])
    show("OPEN QUESTIONS — the Director's to land", buckets["open-questions"])
    print(f"\nSummary: {len(buckets['paid'])} paid, {len(buckets['exempt'])} exempt "
          f"(red-herring/unimportant), {len(buckets['open-setups'])} open setups, "
          f"{len(buckets['verify'])} to verify, {len(buckets['open-questions'])} open questions.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
