# VERIFICATION MANUAL — read this before touching anything

Every session starts here. Tools that don't do what their name suggests are marked. Do not
assume a tool works because it exists, and do not invent a verification method that isn't listed.

## THE ONE RULE

**Verify against the source. Never against a summary.**

The source is the manuscript (the chapter files in `suite.prose_globs`) and the codex
(`ledger/codex/`). Everything else — this manual, the ledgers, a work order, a subagent's report,
your own memory — is a summary, and summaries rot.

In the Resonance revision, six errors were made in one session (2026-07-13). Every one had the
same cause: acting on a summary instead of reading the text. A character "knew a word with no
acquisition event" (another character says it to her, on the page). A count of "11 instances" was
10. "The reader fears X is dead" — the book's last page is a letter to him. A dead mechanic was cut
from the prose and survived in four codex entries, ready to regrow.

**A ruled item is not a verified item. A subagent's confident framing is not evidence.**

---

## 0. START OF SESSION (in order)

```bash
python3 ledger/tools/suite_check.py     # the suite sees every chapter, the codex parses
python3 ledger/tools/audit.py           # canon check; never write on a failing audit
python3 ledger/tools/check_facts.py     # canon facts: valid + what's wobbling
python3 ledger/tools/check_promises.py  # open setups / candidate holes
```
Then read `ledger/DECISIONS_LOG.md`, newest first. If you flag something already ruled there,
you are spending Joe's time on a closed question.

## 1. THE CODEX — check it first

Ask by code, not by reading files: `codex.py <CODE>` · `--find "phrase"` · `--list` · `--gaps`.
The dossier greps the prose live. If the prose count is 0 and the codex count isn't, that's a fossil.

When you change a rule in the prose, change it in the codex (`ledger/codex/`), bump
`codex_meta.codex_version` in RULES.yaml for a rule change, and log it in DECISIONS_LOG.

## 2. THE MANUSCRIPT — the only authority on what is on the page

**Grep the mechanic, not the character name.** In Resonance a character was changed so he "drops
with everyone"; a grep for his name found nothing downstream, but another chapter still said
"People who don't drop at all." That line never says his name.

Negative claims ("nothing else references X") need **untruncated, pattern-diverse** greps. If you
are about to say "no other chapter does this," you have probably run one grep. Run three, with
different phrasings, typography-normalized (`[’']`).

**Read to the end before asserting.** A refusal beat ("I can't") is often reversed a few lines
later. Quote the closing lines of the span you're describing.

## 3. TOOLS — tested 2026-11-02 against a 30-chapter GoSquad draft

| Tool | What it proves | What it does NOT prove |
|---|---|---|
| `suite_check.py` | which files every tool reads; ids; codex parses | that the files are the CURRENT text |
| `audit.py` | codex parses · no fossils · prose obeys RULES.yaml · ruled spans still present · declared pronouns agree | anything not written as a rule; coreference |
| `audit.py --candidates` | where the book stands against Resonance rulings (warnings only) | that Joe wants them here |
| `codex.py` | every live site of a filed code; broken cross-refs; bans holding (`--enforce` gates) | anything unfiled |
| `census.py "<re>"` | the FULL population of a pattern; `--since <ref>` before→after + displacement | that each site was fixed WELL (read them) |
| `check_typography.py` | per-chapter census of every quote/dash/ellipsis form; once a house style is ruled, a gate | prose quality |
| `check_negation.py --census` | every negation-restatement site in narration, five shapes | whether a site is a device (Joe rules) |
| `check_thing.py --census` | placeholder-"thing" block shapes + total | — |
| `check_time.py` | every time-figure in the prose, by phrase | which one is wrong (reconcile to the ruled timeline) |
| `check_repetition.py` | repeated n-grams, motifs exempt (tokenizer fixed for curly ’) | intent; noisy by design — triage, never gate |
| `speaker_volley.py` | consecutive tagged lines by the same speaker (gap 0 = the real defect signature) | untagged misattribution; needs CHARACTERS.yaml |
| `antecedents.py` | pronouns with zero or two plausible owners; "he says" after a named woman | who is MEANT; AMBIGUOUS ≠ wrong |
| `flow.py` | reading-load ranking per ~300-word window | anything, until validated on human-labeled sites (`suite.flow_labels`) |
| `style_metrics.py` | per-chapter sentence/fragment/dialogue/punctuation rates | that a rate is a defect (cadence can be armor) |
| `wordcount.py` | one consistent count, per chapter | a vendor's or contest's count |
| `seal.py` | the sealed files haven't changed without an authorized break-glass | anything about content |
| `check_facts.py` / `check_promises.py` | ledgers are valid JSONL; what's wobbling / open | that the ledgers are complete |
| `split_epub.py` | an EPUB split into chapter files (only if no source files exist) | — |

**Not carried, on purpose:** Resonance's `check_orphans.py` (the "deletion guard") is broken — it
hung on a real diff and failed its own test (the orphan it was built for shared one word plus a
negation with the cut). Use the codex and mechanic greps instead.

**Zero reads as clean — so distrust zero.** Before trusting a tool's zero, prove it can fire:
run it on a known site. `speaker_volley.py` was regression-tested on the exact defect it was
built for before its whole-book output was trusted. Do the same after changing any pattern.

## 4. PROSE VERIFICATION — agents, not scripts

Scripts cannot judge prose.

- **`rogers` subagent** (`.claude/agents/rogers.md`) — fragment and prose-friction pass. Earns its
  keep inside its class: it once caught a wound "under the jacket" that a character was supposedly
  reading in a mirror. It runs ~50% false positives on fragments (measured twice). Rule each finding
  individually; never apply wholesale.
  **The Rogers amendment (measured):** (1) rogers verdicts are advisory on prose you composed —
  "rogers clean" cannot close a decision on your own work; route it to Joe or a cold instance.
  (2) Before any rogers pass, load the codex entries for every registered device in the span and
  put them in its context; re-litigating a registered device is a pipeline defect. (3) Its catch
  profile is ~95% fragment/rhythm. It is fine-grain QA, not the judgment layer.
- **Cold-adversarial read** — two independent cold agents + adjudication, on any substantive edit.
  Cold agents catch unstated facts a flow-read glides over.
- **Never self-review a substantive edit.** Run an independent reviewer.
- **A reader's "never resolved for me" is not a defect until you read the payoff** and it fails on its
  own terms. A wrong model the text never corrects can be a red herring working.

## 5. WHEN YOU CHANGE PROSE — the checklist

1. Read the passage in the manuscript. Not the work order's quote of it.
2. Seal open? `seal.py break-glass` BEFORE any edit, script or tool.
3. Grep the MECHANIC across all chapters.
4. For a cut: grep DOWNSTREAM for what the cut removes (callbacks die invisibly), then a damage-read
   of the surrounding page. Word-count parity is not proof a cut is safe.
5. Update the codex if a rule changed.
6. Rogers pass on anything you composed.
7. Harvest (SUITE_PROTOCOL.md standing duties).
8. Log the ruling, Joe's words verbatim. A sweep claim carries a measured count from `census.py`.
9. `seal.py reseal`.

## 6. THINGS THAT ARE NOT VERIFICATION

- Re-reading your own summary of a file.
- A subagent's final report. That's a lead. Read the primary text.
- This manual, the ledgers, memory. All summaries.
- A count. A sweep verified by count (398 → 0) once shipped "Elena's elbow… Elena's elbow" because
  no one read each substitution. Read the sites.
- Structural symmetry. Do not invent obligations to balance a ledger ("the reader must be told X
  survived") — Joe struck one: reader anxiety does not persist over places the story has left.

## 7. AUTHOR-ONLY

Only Joe assigns `red-herring` or `unimportant`. `wobbling` = two sources disagree and he hasn't
ruled. Only Joe moves a rule from RULES_CANDIDATES.yaml into RULES.yaml, sets the typography house
style, registers a motif, or authorizes a break-glass.
