# PASS 4 — REPETITION & WATCHED WORDS (the long pass; several sessions)

Read GUARDRAILS.md first (rules 1, 3, 5, 8, 12). Motifs in ledger/config.json are EXEMPT.

Measured counts to work from (whole book = 71,562 words; see 02_BASELINE.md):
  "very" 269 · "just" 291 · "something" 157 · "looked" 196 · "hum" 59 · "smile/smiled" 83 ·
  "eyes" 102 · "heart" 85 · "felt" 96 · "breath" 66 · "in her chest" 23 · "the way" 36 ·
  "suddenly" 15 · "realized" 10 · -ly adverbs ~101/10k (RESONANCE runs 39/10k)

Method, per watched word — one word at a time, never batched:
1. CENSUS: `python3 ledger/tools/census.py "\bvery\b" --sites` lists every site with
   chapter:line and context, split narration/dialogue. The census is the single source of
   truth for "how many" — any instruction of the form "get rid of X" starts and ends at the
   census, with no invented filters narrowing the population.
2. TRIAGE with the author: which uses are doing a job (a character's verbal tic, a motif, a
   plot-relevant echo) and which are filler. Author culls; you do not.
3. FIX site by site. Each fix is a read: rewrite the sentence so it doesn't need the word —
   never mechanical deletion, never synonym-swap (that's how a tic becomes a different tic).
4. RECOUNT and log: `census.py "<pattern>" --since <commit-before-the-pass>` gives before → after
   and a DISPLACEMENT check (did "something" just become "a thing"?). Log "word X: 157 → 41, N sites
   ruled kept" in DECISIONS_LOG; the pre-commit gate blocks a sweep claim with no number.
5. Read every changed site after the batch, not just the count. A count of 398 → 0 once shipped
   "Elena's elbow… Elena's elbow."

Priority order (impact × density): very → just → something → looked → -ly sweep →
in her chest → hum → smile family → the rest.

Dialogue is exempt from narration-word rules unless the author says otherwise — people say
"very" and "just". Sweep NARRATION first, show dialogue counts separately.

Also run `python3 ledger/tools/check_repetition.py` (repeated n-grams, motifs exempt) and bring
the list to the author for triage — same method. Repeated SENTENCE SHAPES and figures across
chapters are pass 11.
