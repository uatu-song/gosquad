# PASS 13 — FLOW (reading load), validated before trusted

Read GUARDRAILS.md and COLLABORATOR_RULES.md first.

`python3 ledger/tools/flow.py` ranks every ~300-word window by what it costs to hold: pronoun
ambiguity (two same-gender names in play, none near), reference distance, clause density, long
sentences, negation share. It writes `ledger/FLOW_REPORT.md`. Diagnostic only; never a gate; never
write to the number.

1. **It needs CHARACTERS.yaml with pronouns** (pass 1). Without names the pronoun columns read zero.
2. **Validate it on this book before trusting any ranking.** Collect 5 passages human readers found
   hard (reviewers, Joe, beta readers) and 5 they found easy or praised. Put each in
   `ledger/config.json` → `suite.flow_labels` as `["HIGH"|"LOW", "who said what", "CH07", "exact text
   on the line"]`. Rerun. Pass = HIGH labels in the top quartile, LOW in the bottom. If it fails, the
   instrument doesn't see what this book's readers feel; say so and stop.
3. If it passes: the heaviest 15 windows go to a human reader (Joe, or a cold agent with the
   function test loaded), who reads each and says what actually costs. Fixes then follow pass 8's
   protocol. Pronoun-load fixes are usually a name restored where two people share a gender.
4. What it cannot see: a dull premise, a flat character, a disliked voice, and load that comes from
   withheld cause rather than sentence mechanics ("withhold cause, never withhold event" is a device).
