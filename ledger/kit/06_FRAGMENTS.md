# PASS 6 — THE CH12 SEAM & FRAGMENT CALIBRATION (author-heavy)

Read GUARDRAILS.md first — rule 9 IS this pass. Nothing here is fixed without a ruling.

Measured state (02_BASELINE.md): the book breaks in two at chapter 12.
  ch1-11:  mean sentence 14.9 words, fragment rate ~16%, em dashes ~2/chapter
  ch12-30: mean sentence 7.0 words,  fragment rate ~42%, em dashes ~28/chapter
  Peak chapters: 18, 24, 27, 28, 29 run over 50% fragments with 4-word median sentences.

Step 1 — DIAGNOSIS, with the author, before any edit:
  Is the seam (a) the book finding its voice mid-draft (then ch1-11 may want tightening
  TOWARD the back half), (b) a deliberate acceleration as the plot ignites (then the seam
  itself may be the design and nothing moves), or (c) two drafting eras that need blending?
  Present 3-4 representative passages from each side, side by side. The author names which
  book it is. Log verbatim. EVERYTHING downstream depends on this ruling.

Data for Step 1: `python3 ledger/tools/style_metrics.py` (per-chapter mean/median sentence,
fragment %, dialogue %, punctuation rates). Recompute on the current text; do not reuse August's table.

Step 2 — fragment calibration pass, per the ruling, one chapter at a time:
  Tool: the `rogers` subagent (`.claude/agents/rogers.md`). Before each pass, load the codex entries
  for every registered device in the chapter into its context (`codex.py --find`). It runs ~50%
  false positives on fragments; its verdicts are advice, never applied wholesale.
  For each flagged fragment: does it earn its shape? (Impact beat, breath, voice — earns.
  Reflexive default that dulls the real impact beats nearby — doesn't.) Build a fragment
  ledger per chapter: verdict KEEP / REWRITE with the proposed rewrite inline. The author
  reads the ledger and culls; apply only culled verdicts. Never smooth a run wholesale — the
  50%-fragment chapters may be climaxes wearing armor (rule 9).

Step 3 — recount and log the per-chapter fragment rates after edits into STYLE_PROFILE.md
  (`style_metrics.py <CH> --append`),
  so drift from the ruled design is visible next revision.
