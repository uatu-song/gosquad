# METHOD — Enumerate → Cull → Draft
*Session-marked 2026-07-18. A record of the divergent-drafting method as it was worked out live, kept so
Joe can recount it when explaining it later. Not canon; process. Joe articulated the mechanics — his
framing is preserved here because it is the clearest statement of why the method works.*

---

## The 60-second version
To get genuinely *different* strong options from a model (endings, scenes, titles), do not run four blind
drafters in parallel and hope they fork. Instead have **one context enumerate 15–20 short treatments,
each required to differ from every one before it.** Then **you cull to 3–4.** Then hand each survivor to
a **fresh** drafter. Enumerate → cull → draft. Pitching loglines → greenlight meeting → writing the scripts.

## Why enumeration forces divergence when blindness can't
A model's first answer to any creative prompt is **the centroid** — the highest-probability rendering of
that brief. Four *blind* drafters give four independent draws from the *same* distribution, which is why
they converge: **independence prevents copying, not sameness.** But when one context generates variation
#12 with #1–11 sitting in front of it, **every previous idea is an explicit repulsor.** You are no longer
sampling the distribution; you are **systematically draining it.** The first three or four exhaust the
defaults (the ideas any competent writer would reach for). Five through twelve are where it gets
interesting, because the model is now forced off its mode into genuinely **low-probability territory**.
The "crazy and unpredictable" is **mechanical, not lucky** — you pay the model to leave its comfort zone
by making the comfort zone off-limits, item by item.

## The two methods have opposite failure modes — which is why they compose
- **Blind panel** = *depth but designer-limited breadth.* Four fully committed drafts, but the briefs are
  only as diverse as whoever wrote them. (My withheld/irony/body/tender axes were *my guess* at the space.)
- **Enumeration** = *breadth but no depth.* Twenty sketches, none executed, and the **late tail degrades
  into novelty-for-novelty** — differentiation pressure selects for surface difference (weirder framing,
  gimmick POVs), not better scenes. The quality curve is an **inverted U; the sweet spot is ideas ~5–12.**

Enumeration **discovers the possibility space empirically** instead of trusting the designer to have
guessed it. So: enumerate for breadth, then draft the survivors for depth.

## The three stages (and the rules that make each work)
1. **Enumerate** — one context, 15–20 one-paragraph treatments. Each must differ from all priors along
   **named axes — POV structure / reveal mechanism / scene grammar / where the wrong note enters — NOT
   tone** (tone-difference just yields new adjectives). Lock whatever is fixed (here: the author's final
   image). *Refinement:* run **opposed personas** (e.g. restraint-minimalist vs quiet-distrusting
   maximalist vs formalist) for cross-persona spread on top of intra-list forced difference.
2. **Cull** — pick the top 3–4. **Critical: do NOT let the enumerator rank its own list.** A model ranking
   its own twenty ideas shows **self-preference and mode gravity** — it promotes the safe early entries you
   just spent nineteen items escaping. Use independent judges, or **honestly, the author** — reading twenty
   loglines takes three minutes and *the author's taste is the point of the whole exercise.* Agents may
   *triage* (dedup clusters, flag wildcards and the novelty-only tail) as **advisory**, never as the gate.
3. **Draft** — hand each surviving treatment to a **fresh-context** committed drafter, one brief each, with
   an anti-convergence clause. Then adversarial judges, then synthesis. **Keep this separate** from
   enumeration: execution quality decays in a context stuffed with nineteen rejected siblings. **Depth wants
   a clean room; breadth wants a crowded one.**

## The built-in diagnostic (designed vs discovered)
Let the designer's guessed briefs compete in the same cull as the discovered treatments. **If the designed
briefs keep winning, the guesses were good; if they keep losing, the enumeration stage earned its tokens.**
Either way you learn something about the instrument. (Bet on the run: at least one route in ideas 8–14 that
neither party would have written on purpose.)

## How it played out this session (the story to recount)
- I first built the standard move: a **blind judge-panel** — 4 drafters (withheld/irony/body/tender) → 12
  adversarial judges → synthesis. Correct instinct, incomplete.
- Joe: *"What stops them writing similarly to one another — isn't this a practice in redundancy?"* Exactly
  right. I upgraded the panel from *tonal* tilts to structural **routes** + an anti-convergence clause, and
  locked the final image. Better, but still four briefs *I* guessed.
- Joe named the missing half: **enumeration.** And corrected two things I'd gotten wrong in my first
  ideation build — (a) I let each enumerator **self-rank** (the exact self-preference trap; fixed: no
  self-ranking, triage is advisory only), and (b) **the author is the culler**, not an agent. Also: **opposed
  personas** beat my topic-regions.
- Resolution: **resume** the designed panel to completion (its drafts become free "designed" entries in the
  cull pile) + launch the corrected **ideation v2** (3 opposed personas × 12, forced-distinct on named axes,
  no self-rank, advisory triage) → a menu for Joe to cull → survivors drafted in clean rooms → judges →
  synthesis. Bake-off: designed vs discovered.

## How to run it again (recipe)
- Ideation workflow: `scratchpad/ending_ideation_v2.js` (3 personas × 12 → triage → menu).
- Panel/draft workflow: `resonance-ending-panel-*.js` (routes → judges → synthesis); reused for the
  culled survivors by swapping the ANGLES array for the greenlit treatments.
- Sequence: **enumerate (agents) → cull (JOE) → draft (fresh agents) → judge → synthesize → author ratifies.**
- Guardrails that matter most: named-axes-not-tone · no self-ranking · author culls · clean-room drafting
  · lock the fixed element · watch the inverted-U tail.

*Cross-ref: memory `enumerate-cull-draft-pipeline`. Method only — the ending content itself is drafted,
vetted, and elevated through the seal/break-glass pipeline like any other prose.*
