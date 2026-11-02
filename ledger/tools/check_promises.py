#!/usr/bin/env python3
"""Report on PROMISES.jsonl: open setups (candidate plot holes at end of draft),
verify-status items, open questions. Red-herring / unimportant entries are exempt
and listed only in the summary count. Exit 1 on JSON/schema problems only.

Usage: python3 ledger/tools/check_promises.py [path-to-jsonl]
"""
import json
import sys
from pathlib import Path

REQUIRED = {"id", "type", "promise", "status"}
EXEMPT = {"red-herring", "unimportant"}
VALID_STATUS = {"open", "paid", "verify", "abandoned"} | EXEMPT
VALID_TYPE = {"setup-awaiting-payoff", "payoff-needing-setup", "open-question"}


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "PROMISES.jsonl"
    if not path.exists():
        print(f"ERROR: {path} not found")
        return 1

    problems, buckets = [], {"open-setups": [], "verify": [], "open-questions": [], "exempt": [], "paid": []}
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

    print(f"PROMISES CHECK — {path.name}")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"  ✗ {p}")

    def show(title, items, hint=""):
        if items:
            print(f"\n{title} ({len(items)}){hint}:")
            for r in items:
                print(f"  • [{r['type']}] {r['id']}: {r['promise']}")

    show("OPEN SETUPS — candidate plot holes at end of draft", buckets["open-setups"])
    show("VERIFY — payoffs whose setups need prose confirmation", buckets["verify"])
    show("OPEN QUESTIONS — Joe's to land", buckets["open-questions"])
    print(f"\nSummary: {len(buckets['paid'])} paid, {len(buckets['exempt'])} exempt (red-herring/unimportant), "
          f"{len(buckets['open-setups'])} open setups, {len(buckets['verify'])} to verify, "
          f"{len(buckets['open-questions'])} open questions.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
