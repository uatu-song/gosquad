# PASS 7 — CONTINUITY HARVEST & AUDIT

Read GUARDRAILS.md first (rules 2, 4, 6, 7).

Part A — HARVEST (populate the ledgers created in 01_SETUP), chapter by chapter, reading in
full — no skimming:
1. CANON_FACTS: every hard number, date, age, distance, spec → jsonl with source. On
   conflict: mark, surface, never resolve silently.
2. PROMISES: every detectable setup (objects, secrets, questions, threats, named-but-unseen
   things) → "open". Payoffs you detect → "paid" with location.
3. CHRONOLOGY: datable events with precision tags. Travel times and simultaneity claims are
   where books break — log every "X hours later" and every two-places-at-once risk.
4. STRUCTURE_MAP: verify the seeded pov/tense row per chapter while you're in there.

Part B — AUDIT (only after the harvest is complete):
1. Facts: contradictions and wobbles → author list.
2. Promises: every "open" at book end is a CANDIDATE hole — author rules paid/red-herring/fix
   (rule 6: only the author).
3. Chronology: walk the timeline start to finish once; flag impossible travel, doubled days,
   characters present after the book moved them elsewhere.
4. Character-state checks: injuries that vanish, objects that teleport, knowledge characters
   shouldn't have yet (who-knows-what-when is its own sweep for any secret-driven plot).
VERIFY every audit finding against the prose before it reaches the author (rule 2) — grep the
MECHANIC, not the character name (the site that breaks a rule rarely contains the name you'd
search for), and normalize typography in every pattern (rule 4).

Tools for this pass:
- File facts and setups as you harvest; then `python3 ledger/tools/codex.py FCT-<id>` / `PRM-<id>`
  shows each one with its live prose sites. `check_facts.py` / `check_promises.py` validate the ledgers
  and list what's wobbling and open.
- `python3 ledger/tools/check_time.py` lists every time-figure in the prose by phrase ("two days ago",
  "that same night"). File the ruled timeline as one fact (id `master-timeline`) and reconcile every
  figure against it by hand. Add the book's anchor events to `suite.time_anchor_events`.
- Rules that must hold everywhere (a mechanic, a name spelling, a banned descriptor) go into
  `ledger/codex/RULES.yaml` or a WRD- code with `expect_in_prose: absent`, so `audit.py` and
  `codex.py --enforce` hold them from then on. Only with Joe's ruling.
- `codex.py --gaps` at the end: broken references, codes naming nothing, wobbling facts, open setups.
