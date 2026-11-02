# PASS 12 — REGISTER CENSUS (where collaborator house style entered the prose)

Read GUARDRAILS.md and COLLABORATOR_RULES.md first. **This pass shows; it never executes.**

Any prose a model drafted or revised carries the model's register: aphoristic chapter closers
("Comfort is a loan and somebody always comes to collect."), the corrective pair, triads, "its own
small X", "the kind of Y that only comes when Z", "lets herself", "finds that it isn't nothing".
Resonance's census (2026-10-17) found it chapter-specific, not spread evenly.

## Method (as run on Resonance)
1. **Regex battery** per chapter: a list of LLM-fiction tells (corrective pairs, "something like",
   "the weight of", "silence stretches", "breath she didn't know", "ghost of a smile", "which is to
   say", aphorism-closers, "But" openers, one-word sentences, -ly rates). Compare chapters against
   each other with `census.py` per pattern; report per-1k rates, not raw counts.
2. **Three blind cold reads** (separate agents, identical brief, no access to the regex output):
   score each chapter 0–10 for model-register intensity and quote the strongest lines. Include a
   control slice of chapters you expect to be clean.
3. **Provenance**, if drafts exist: share of sentences ≥8 words surviving verbatim from any
   machine-drafted file. A chapter can read hot and be Joe's.
4. Verify every quoted line against the live file.

## Calibration — read before presenting anything
- **The census measures a register, not authorship.** In Resonance an author-written chapter scored
  8/10 from blind readers who could not tell it from the collaborator's. Joe's own read of the book:
  the presence was "not detectable or obvious."
- **Your taste is the sieve, and it is biased toward you.** Plain, blunt lines get flagged by models
  and are often his; your own smooth lines never get flagged. A census label is counsel until he rules.
- Present: hot list (chapters), strongest instances verified, what the sweeps already cleared.
  He rules what, if anything, happens. Often the right outcome is "file it" — Resonance's census was
  filed for the record and nothing in the shipped text changed.
