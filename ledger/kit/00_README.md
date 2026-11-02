# GoSquad Book 1 — Editorial Passes

The same lenses RESONANCE went through, in the order that worked, each as a self-contained
prompt. Paste a pass file into a fresh Claude session in this repo. Every pass reads
`GUARDRAILS.md` first and ends by writing its results into the ledgers, so the next session
inherits state from FILES, not chat memory.

First kit: 2026-08-29 (passes 01–08). This edition, 2026-11-02, wires every pass to the suite's
tools (`ledger/tools/`) and adds the lenses Resonance received after August (09–13).

## Before any pass
```bash
python3 ledger/tools/suite_check.py   # SUITE READY? It must list every chapter.
python3 ledger/tools/audit.py
```

## Order of operations (do not shuffle)

0. `GUARDRAILS.md` + `COLLABORATOR_RULES.md` — read first, whole thing, every session.
1. `01_SETUP.md`        — fill the codex (characters, POV per chapter), motif ruling. One session.
2. `02_BASELINE.md`     — measured stats (August). Recompute with `style_metrics.py` before comparing.
3. `03_TYPOGRAPHY.md`   — mechanical; before prose passes so greps match reality.
4. `04_REPETITION.md`   — watched-word censuses and cuts. Longest pass; several sessions.
5. `05_DIALOGUE.md`     — tag profile + speaker-volley + pronoun attribution.
6. `06_FRAGMENTS.md`    — the ch12 cadence change and fragment calibration. AUTHOR-HEAVY.
7. `07_CONTINUITY.md`   — facts/promises/chronology harvest, then the audit.
8. `08_LINE_EDIT.md`    — the protocol for what Joe finds while reading.
9. `09_NEGATION.md`     — the negation-restatement census and sieve (Resonance's biggest ruled ban).
10. `10_DOUBLED_BEATS.md` — one rendering per beat; beats delivered twice; editing artifacts.
11. `11_REPEATED_CONSTRUCTIONS.md` — the same figure or sentence shape across chapters.
12. `12_REGISTER_CENSUS.md` — where collaborator house style (LLM register) has entered the prose.
13. `13_FLOW.md`        — reading-load ranking, validated against human-labeled passages.

Passes 9–13 assume 3 (typography) is done. Run 12 last: it reads best on a text the other passes
have already settled.
