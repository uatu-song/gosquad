# PASS 5 — DIALOGUE TAGS & SPEAKER INTEGRITY

Read GUARDRAILS.md first (rules 2, 3).

Measured state: "said" is 62% of dialogue tags (445 of 715); the rest are the
replied/shouted/whispered/snapped family. RESONANCE runs 79% said-default. Dialogue is 30.7%
of the book, so this pass touches a lot of text.

Part A — tag profile:
1. Census every non-said tag with chapter:line, grouped by verb:
   `census.py "[”\"],? (?:\w+ )?(replied|shouted|whispered|snapped|muttered|demanded)\b" --sites`
   (one verb family at a time; `style_metrics.py` gives the said-share per chapter).
2. Author rules on the default (said-default is the working recommendation, with non-said
   verbs kept where the verb carries information the line doesn't: whispered when volume
   matters, etc.). Log the ruling verbatim.
3. Convert site by site — and at each site, prefer deleting the tag entirely when an action
   beat already attributes the line. Also census adverb-on-tag ("said quietly") separately;
   those usually become beats or nothing.

Part B — speaker-volley audit (wrong-speaker tags are the embarrassing class; RESONANCE
shipped 18 of them to reviewers):
0. Tools first (both need CHARACTERS.yaml filled, pass 1):
   `python3 ledger/tools/speaker_volley.py` — consecutive TAGGED lines by the same speaker. Run at
   gap 0 for signal; widen (`--gap 2`) only to hunt a specific passage; gap>0 is mostly correct prose.
   Regression-test first: find (or construct in a scratch copy) one known same-speaker pair and
   confirm it fires before trusting a zero.
   `python3 ledger/tools/antecedents.py` — "he says" right after a named woman (MISATTRIB), pronouns
   with no owner (ORPHAN) or two close owners (AMBIGUOUS). AMBIGUOUS means a reader COULD misread it.
   Then the manual walk below, which is where untagged misattribution is found.
1. For every dialogue run of 4+ exchanges, walk the alternation and verify each attributed
   line is consistent with the volley — and that every UNATTRIBUTED line resolves to exactly
   one speaker via the alternation or an adjacent action beat.
2. Flag: (a) tags that break alternation without an on-page reason, (b) unattributed lines
   where two readings survive, (c) three-speaker scenes running bare alternation (they can't).
3. VERIFY each flag against the file before reporting (rule 2). Report with chapter:line,
   the two candidate speakers, and the prose evidence each way. The author rules ambiguous
   sites; do not guess.
