# PASS 9 — NEGATION-RESTATEMENT CENSUS AND SIEVE

Read GUARDRAILS.md and COLLABORATOR_RULES.md first.

**Background.** In Resonance, Joe banned the negation-restatement construction in narration, all
five shapes, and ruled it four times before it reached zero ("JUST FUCKING DO IT", 2026-09-05):
  "Not X. Y." · "It isn't X. It's Y." · "X and not Y" / "not X but Y" · "not X—Y" ·
  "It does not X. It does not Y."
It is collaborator house style: it re-enters any prose a model touches. For this book the ban is a
CANDIDATE (`ledger/codex/RULES_CANDIDATES.yaml` R008b) until Joe rules it here.

## Step 1 — census, show, ask
```bash
python3 ledger/tools/check_negation.py --census     # every site, chapter:line, full line
```
Show Joe the count and a sample of 10 representative sites. Ask one line: does the ban apply to
this book? Log his words. If yes, move R008b into RULES.yaml (his words, today's date); from then
on `audit.py` blocks new sites.

## Step 2 — if ruled in: proposals, then a harsh sieve (never a blind sweep)
Resonance's lesson: 923 rewrite proposals were graded by a separate editor told to be harsh
("when in doubt, it is not a nugget") — **90 were real improvements, 357 sideways, 476 harmful.**
About one in ten. So:
1. Proposers (one per chapter range) write a rewrite per site. Each rewrite must keep the event:
   often the negation IS the event (a non-answer, a refusal, the thing that didn't happen).
2. A separate grader, cold, labels each NUGGET / SIDEWAYS / HARMFUL with a one-line reason.
   Why most fail: the negation was the event; a joke or dry line died; a deliberate triplet or
   callback broke; a withheld mystery got named; the rewrite invented a gesture or ran clunkier.
   Proposers also start their own tics — check the rewrites for repeated phrasings.
3. Joe gets ONLY the nuggets, in a file (`ledger/review/NEGATION_SIEVE.md`): numbered, chapter:line,
   **now:** full sentence, **proposed:** full sentence, `MARK:` line. He marks Y/N or writes his own.
4. Apply exactly his marks under an open seal. Recount with `check_negation.py`; log before → after.

If he rules a zero (as in Resonance): "When Joe bans a shape, the answer is a count of zero, not a
list of survivors." Survivors exist only if he names them in advance. Dialogue is exempt.
