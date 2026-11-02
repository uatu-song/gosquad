# EDITING SUITE — Manuscript Protocol

> Imported into this repo's `CLAUDE.md` by `install.py` (the line `@ledger/SUITE_PROTOCOL.md`).
> Carried over from the Resonance revision (Joe's Book 2), where every rule below was written
> after a real failure. The failure is named where it helps the rule make sense.

## FIRST ACTION, EVERY SESSION

1. Read **[`ledger/VERIFICATION_MANUAL.md`](VERIFICATION_MANUAL.md)** in full: which tools work, what each one
   proves and does not prove, and the order to use them.
2. Read **[`ledger/kit/COLLABORATOR_RULES.md`](kit/COLLABORATOR_RULES.md)**: how Joe wants changes handled. Short.
3. Run `python3 ledger/tools/suite_check.py` (is the suite pointed at the book?) then
   `python3 ledger/tools/audit.py` (does the book obey its ruled rules?).
4. Read the newest entries of `ledger/DECISIONS_LOG.md`: the don't-relitigate list.

**Never write prose on top of a failing audit.**

## What the files are

- **The manuscript is canon.** The chapter files named in `ledger/config.json` → `suite.prose_globs`.
  Everything else indexes it; nothing else is canon by itself.
- **The codex** (`ledger/codex/*.yaml`) holds the ruled facts about the book: characters, POV per
  chapter, rules, constraints, watched words. Ask it by code: `codex.py <CODE>`.
- **The ledgers** (`ledger/*.jsonl`, `*.md`) record what the prose asserts and what Joe ruled.

## The two commands

```bash
python3 ledger/tools/audit.py              # the canon check: codex parses, no fossils, prose obeys the rules
python3 ledger/tools/codex.py CHR-NAME     # ask the repo for any thing, by code; greps the prose live
```

`codex.py --list` every code · `--find "phrase"` who owns this string, and where it lives ·
`--gaps` what the system does NOT know (run it before you call anything clean).

**Do not answer a canon question from memory or by reading one YAML file.** Resolve the code. The
dossier greps the prose live, so it reports what is true NOW.

## Standing duties (the harvest protocol)

Whenever prose is added or edited, before the session ends:

1. **Dialogue** — new/changed lines into `ledger/DIALOGUE_BANK.jsonl`.
2. **Facts** — every hard number, date, age, distance or spec asserted in prose into
   `ledger/CANON_FACTS.jsonl` with its source. On a conflict, set the existing entry to
   `contradicted` (or `wobbling` if arguably both) and tell Joe. Never silently pick a winner.
3. **Seedings** — detectable setups into `ledger/PROMISES.jsonl` as `setup-awaiting-payoff`, `open`.
   Payoffs you detect: `paid`, with location.
4. **Chronology** — datable events into `ledger/CHRONOLOGY.jsonl`.
5. **Structure** — one row per chapter in `ledger/STRUCTURE_MAP.jsonl`.
6. **Style** — `python3 ledger/tools/style_metrics.py <CH> --append` (descriptive only).
7. **Repetition** — `python3 ledger/tools/check_repetition.py`; surface real flags to Joe. Motifs are exempt.
8. **Decisions** — every ruling into `ledger/DECISIONS_LOG.md`, with Joe's words verbatim.

End every working session with a one-paragraph harvest report: what was logged, what flagged,
what needs Joe's ruling.

## Rules

- **Every change runs through Joe.** No prose change lands without his mark on that line. Censuses
  show; they never execute. See `kit/COLLABORATOR_RULES.md`.
- **Only Joe** assigns `red-herring` or `unimportant` in PROMISES. An unpaid setup is a *candidate*
  hole, not a verdict.
- `wobbling` = two sources disagree and Joe hasn't ruled. Flag, don't fix.
- **Motifs**: deliberate repetition is registered in `ledger/config.json` → `motifs` and exempt from
  every repetition pass. Register only what Joe confirms.
- **The function test** (`ledger/STYLE_RULES.md §0`): before flagging ANY irregularity, ask what it DOES.
  In Resonance, a chapter's tense toggles were "fixed" three separate times by agents applying the
  consistency prior; they were a deliberate device.
- **Function-test scope:** the test protects the AUTHOR'S devices from agents. It never protects a
  collaborator-written construction from an author ban. When Joe bans a shape, the answer is a count
  of zero, not a list of survivors.
- **Rules Joe ruled for Resonance are candidates here** (`ledger/codex/RULES_CANDIDATES.yaml`) until he
  rules them for this book. Run `audit.py --candidates` to show him where the book stands.
- **Banned collaborator tics** (Joe-flagged, in notes too): "load-bearing," the "that's not X, that's Y"
  reversal, "worth noticing," adverbial "quietly."
- **If you change a rule in the prose, change it in the codex.** A dead rule left in the codex grows
  back into the next chapter written; `audit.py` section 2 finds these fossils.

## The seal

Once Joe approves a state of the manuscript, `python3 ledger/tools/seal.py seal` locks the chapter
files. A hook then blocks any Edit/Write to them, and the pre-commit gate blocks any drift.
To make an approved change:

```bash
python3 ledger/tools/seal.py break-glass --reason "what and why" --authorized-by joe   # BEFORE any edit, script or tool
# edit · harvest · log the ruling in DECISIONS_LOG.md
python3 ledger/tools/seal.py reseal                                                    # refuses until a ruling is logged
```

Scripts bypass the edit hook but not the commit gate. Open the glass first, every time.

## Two traps that each cost a session

- **Grep the MECHANIC, not the character name.** A line that breaks a rule rarely names the person.
- **Curly apostrophes.** The prose may use ’; a pattern written with ' cannot match `doesn’t`, returns
  zero, and **zero reads as clean.** The suite's tools normalize; any grep you write must too
  (`[’']`), and you must prove a pattern can match a known site before trusting its zero.
