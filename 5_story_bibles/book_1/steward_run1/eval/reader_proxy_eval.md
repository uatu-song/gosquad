# Reader Proxy — Book 1 Steward Run 1 Evaluation

**Agent:** Reader Proxy (Production Crew, role 6 of 12)
**Domain:** Audience knowledge & dramatic irony — what the READER knows vs. what each CHARACTER knows, and whether those layers are tracked consistently across stewards.
**Scope:** 10 steward outputs + 3 convergence files (M26/M82/M131) against `BOOK1_MOVE_MAP.md` and `BOOK1_FINAL_STATE.md`.
**Out of lane (deferred, not judged here):** chess-move timing reconciliation (Timeline Keeper), character-state facts/baseline math (Status Tracker), thematic load (Theme Guardian), tension-curve quality (Pacing Monitor).

---

## Domain & method

I read every beat asking two questions only: (1) what does the READER know at this point, and (2) what does each CHARACTER know — and do the stewards keep those two ledgers separate and mutually consistent? An irony layer is "sound" when the reader is given privileged knowledge that is set up before it pays off, and when no character is shown knowing something the canon says they can't know yet. I flag three failure types: **premature knowledge** (a character knows too early), **dropped/contradicted irony** (a layer the reader holds gets fumbled), and **un-set-up privilege** (the reader is expected to know something that was never planted).

---

## Irony-layer map (the six load-bearing layers)

| # | Irony | Reader knows | Characters know | Reveal point | Owning stewards |
|---|-------|--------------|-----------------|--------------|-----------------|
| 1 | **Protagonist fakeout** (Firas→Ahdia) | Reader is *meant to be fooled* until M26 | Firas believes it's his story; Ahdia knows she's the hidden center | M26 (CP-1) | Firas (seed M1), Ahdia (payoff M26), Bourn |
| 2 | **Fake death** (warehouse) | Reader knows Ahdia is alive | Team believes she died; Bourn *suspects* alive; Kain doesn't care yet | M26 → undone at M82 for Ruth | Ahdia, Firas, Bourn, Kain |
| 3 | **Powers-source secret** | Reader/Ahdia know it's her, dying | Ruth learns M82; team learns ~Ch25/M110; each member believed abilities were earned | M82 (Ruth) → ~Ch25 (team) | Ahdia, Ruth, Ryu, Leah, Victor, Tess, Ben |
| 4 | **Ahdia is dying** | Reader + Ahdia + Ruth + Ryu know | Team does NOT know, even after Ch25 power reveal | Withheld all book from team | All — and they hold the line (see Sound) |
| 5 | **"Death" = transcendence, not death** | Reader knows (via final-state framing) | NO ONE in-world knows — not Ahdia, Ruth, Ryu | Withheld from everyone | Ahdia, Ruth, Ryu |
| 6 | **Kain clone-survives / Firas displaced not dead / Bellatrix clocked Ahdia** | Reader knows all three | Team believes Kain dead + Firas dead; only Ahdia glimpsed Bellatrix | Epilogue (Kain) / withheld (Firas, Bellatrix) | Kain, Bourn, Ahdia, Firas |

---

## Findings

### F1 — Team's power-reveal (~Ch25/M110) is asserted but never *staged* by any steward — FIX
The move map and final-state both fix the team learning the truth at ~Ch25/M110. Every team steward (Ben, Tess, Leah, Victor) references it in past tense — "the reveal already told the others" (Tess), "he read the truth ~Ch25" (Ben), "the truth lands ~Ch25" (Leah), "M82+ the reckoning" (Victor). But **no steward owns the M110 reveal beat itself.** Ahdia's run jumps M82 → M108 → M133 with no team-reveal beat; Ruth's jumps M82 → M131. The single most important irony-collapse for four characters happens entirely off-page in the current footage.
- **Irony issue:** The reader's biggest shared-with-team transition (layer 3) has no staged moment. Worse, the stewards disagree on *when* the team knows relative to M82: Victor anchors his reckoning "~M82+" and treats himself as confronting Ahdia *right after the Docks*, while Tess/Ben/Leah anchor to ~Ch25/M110 (~28 moves later). That is a 4-character knowledge-state inconsistency.
- **Severity:** FIX (BLOCKER-adjacent — it's the spine of layer 3).
- **Fix:** Assign the M110 team-reveal as an owned convergence-style beat (Ahdia or Ruth anchors, team stewards diverge). Lock whether Victor's reckoning is at M82 (he alone, impossible — he's not at the Docks) or at M110 (with the team). Recommend M110 for all four; Victor cannot know at M82 because only Ruth witnessed.
- **Source:** `Victor_run1.md` §"The reckoning (~M82+)"; `Tess_run1.md` CP-3 ("the reveal (~Ch25) already told the others"); `Ben_run1.md` CP-3 ("read the truth ~Ch25"); `BOOK1_MOVE_MAP.md` Stud 4b ("team learns Ch25 (~M110)").

### F2 — Victor's M82 reckoning lets him know the source before the team should — FIX
Victor's "reckoning (~M82+)" beat has him personally confronting Ahdia about manipulation-vs-protection. But per canon (`BOOK1_FINAL_STATE.md` Docks Reveal: "First person besides CADENS to know the truth" = Ruth), only Ruth witnesses at M82, and she *covers* — tells the team she "got separated" (`Ruth_run1.md` M82). Victor cannot be reckoning with the source-truth at M82; he doesn't have it yet.
- **Irony issue:** Premature knowledge. If Victor knows at M82, the reader's careful M82→M110 staging of "Ruth alone, ahead of the team" (which Ryu's beat explicitly leans on — "the room getting more crowded," only Ruth joins the circle) is contradicted.
- **Severity:** FIX.
- **Fix:** Re-anchor Victor's reckoning to post-M110. His content is excellent and unchanged; only the timing label is wrong. Leah's "Reveal-aftermath (~M82+)" carries the same loose anchor and should likewise move to ~M110.
- **Source:** `Victor_run1.md`; `Leah_run1.md` §"Reveal-aftermath (~M82+)"; `Ruth_run1.md` M82 ("She will tell the team she 'got separated'"); `Ryu_run1.md` M82 ("now Ruth's inside the circle").

### F3 — Bourn "suspects Ahdia is alive" at M26 risks deflating the reader's fake-death irony — NOTE
Bourn's M26 beat has her privately concluding the fire is staged ("*asset's status — do not list deceased*") and keeping the file open. This is strong characterization, but it quietly **adds a third knower** to the fake-death layer (reader + Ahdia + now Bourn/CADENS). Final-state confirms CADENS surveillance "catches everything," so this is canon-consistent — but the reader needs to understand Bourn *suspects* (not *confirms*), or the dramatic-irony tension of "the whole world thinks she's dead" softens.
- **Irony issue:** Potential dilution of layer 2 if staged as certainty rather than suspicion.
- **Severity:** NOTE.
- **Fix:** Keep Bourn's read as *suspicion managed as acquisition*, explicitly uncertain ("too clean… do not list deceased" is the right register — it's a hold, not a confirmation). Flag for blocking: don't let Bourn's POV confirm Ahdia alive to the reader in a way that pre-empts the M82 reveal's punch.
- **Source:** `Bourn_run1.md` M26.

### F4 — The "transcendence not death" layer (5) is reader-privileged but never set up *in Book 1 footage* — FIX
Ahdia's M133 and CP-3 beats lean hard on the reader knowing this is "transcendence, not death" ("she thinks she was rescued from suicide; she was rescued from ascension"). Ruth and Ryu beats correctly state they *don't* know it. But the reader can only hold this irony if the prose plants the seed — and **no steward beat plants it.** Ahdia "files" the red direction as a tool (M108) and reads e6 as "leaving the shape of a person" (M133), which is evocative but ambiguous; a first-time reader may simply read it as death, exactly as the characters do.
- **Irony issue:** Un-set-up privilege. If the reader doesn't independently know it's transcendence, layer 5 isn't dramatic irony at all — it's just authorial back-matter. The whole "rescued from ascension not suicide" reframe lands only on a re-read.
- **Severity:** FIX.
- **Fix:** Director decision — either (a) accept that layer 5 is a *Book-7 retroactive* irony (reader learns later, not in Book 1), and stop the stewards from writing as though the reader already holds it; or (b) plant a concrete reader-only signal at M108/M133 (e.g., the dream-vision shows Ahdia something the narration frames as a door *opening*, not closing). Recommend (a) for honesty about reader state: in Book 1 the reader shares the characters' belief that this is death. That is cleaner and makes Book 7 pay off.
- **Source:** `Ahdia_run1.md` M133 & CP-3; `Ruth_run1.md` CP-3 ("does not know he is displaced… believes it completely"); `BOOK1_FINAL_STATE.md` ("What She Doesn't Know: Treatment prevents transcendence, not death").

### F5 — "Firas displaced not dead" + "Bellatrix clocked Ahdia": which does the reader hold in Book 1? — FIX
Two stewards write the reader as holding privileged knowledge the Book-1 reader may not actually have:
- **Firas displaced:** Firas's own beat ("I do not know I'm displaced not dead… I return Book 7") and Ahdia/Ruth/Ben/Tess all confirm the *characters* believe him dead. But is the *reader* let in? Final-state says "displaced, not dead" is the truth; whether Book 1 reveals it to the reader (a hint, a final image of Firas conscious in the Between) is undefined. Stewards write as if the reader knows. If so, that must be staged (a closing reader-only beat). If not, stop writing it as held irony.
- **Bellatrix clocked Ahdia:** Ahdia "briefly saw Bellatrix" (canon — she knows). But "Bellatrix is now watching, patient" / "clocked her" is asserted as reader knowledge by Ahdia, Kain, and Ruth-adjacent framing. Kain's epilogue ("she saw Bellatrix… proceed carefully") is the natural place the *reader* learns Bellatrix is now hunting Ahdia. That works — but it means the reader gets it at the epilogue, not earlier; Ahdia's CP-3 ("Bellatrix… is now watching") slightly front-runs it.
- **Irony issue:** Inconsistent reader-knowledge anchoring for layer 6 across stewards.
- **Severity:** FIX.
- **Fix:** Director to set, per sub-layer: (i) does Book 1 reveal Firas-alive to the reader, yes/no? If yes, assign a closing beat; if no, the stewards should treat his death as straight (reader shares the grief). (ii) Lock that the reader learns "Bellatrix is now watching Ahdia" at **Kain's epilogue** — and make Ahdia's CP-3 not pre-state it as settled. The reader should leave the climax thinking it's over; the epilogue is the gut-punch.
- **Source:** `Firas_run1.md` CP-3; `Kain_run1.md` epilogue; `Ahdia_run1.md` CP-3; `BOOK1_FINAL_STATE.md` Kain end-state ("Knows she contacted Bellatrix") + Ahdia ("Firas will return (Book 7)" under *What She Doesn't Know*).

### F6 — Kain clone-survival is reader-only and cleanly handled, but timing of reader's knowledge needs a lock — NOTE
Kain's epilogue is the *only* place the reader learns he clone-survives ("I wake in a new body… the team buries a kaiju; I change clothes"). Bourn's ~M128 beat correctly keeps her ignorant ("she believes she is ending Kain… clone-survives off-board… Bourn's files have no entry"). This is the best-handled deep irony in the set — character belief (Kain dead) and reader knowledge (Kain alive) are cleanly split and the reveal vector (Kain's own POV epilogue) is unambiguous.
- **Irony issue:** Minor — the team believing Ng7/the missile killed Kain is consistent, but confirm the reader does NOT get clone-survival until the epilogue (no earlier Kain-POV leak), so the climax reads as a clean team victory before the rug-pull.
- **Severity:** NOTE.
- **Fix:** Keep Kain's clone-survival sealed to the epilogue. No change needed beyond confirming no earlier Kain-POV beat reveals it.
- **Source:** `Kain_run1.md` M131–136 epilogue; `Bourn_run1.md` ~M128.

---

## Out-of-domain deferrals

- **Timeline Keeper:** The M82-vs-M110 traffic around the team reveal (F1/F2) is partly a *timing reconciliation* problem — exact move anchor for the team learning the truth, and whether Victor's reckoning is M82 or M110. I flag the irony consequence; the linear-sequence fix is yours.
- **Status Tracker:** Who-knows-what as *character-state facts* (Ruth/Ryu hold full operational truth; team holds powers-but-not-dying; Bourn holds Mother FAERIS but not TRIOMF). I used these as inputs; authoritative tracking is yours. Also: Ahdia's baseline at CP-3 — Ahdia's beat says "~30%," final-state says "18% at Docks (M82)" then recovery; the 30% figure is a Status Tracker reconciliation, not mine.
- **Theme Guardian:** Whether layer 5 (transcendence) should be reader-visible in Book 1 is partly thematic (the "you don't have to be fixed" payoff). I flag the irony mechanics; the thematic call is yours.
- **Pacing Monitor:** Whether the epilogue rug-pulls (Kain alive, Bellatrix watching) land with the right delay after the climax is a tension-curve question.

---

## What's sound (well-handled)

1. **The protagonist fakeout (layer 1) is set up and paid off coherently.** Firas's M1 beat plants it from the inside ("the opening nobody reads as the real story — he's certain it's his"); Ahdia's M26 pays it off ("the protagonist was never the flashy piece"); Bourn's M26 reinforces it institutionally ("the Queen was never the file she was protecting"). Three stewards, one consistent reader-experience. **No fix needed.**

2. **The "Ahdia is dying" secret (layer 4) is held with discipline.** Every team steward explicitly carries the gap: Leah "does NOT know Ahdia is dying for it" (and the steward notes this keeps her resentment a *pride-wound not guilt-wound*); Victor "prosecutes the manipulation case without knowing she's dying"; Ben "does NOT know she's dying." This is the strongest cross-steward consistency in the whole run and it generates real reader irony (the reader feels the reframe each character can't).

3. **The M82 reveal asymmetry is beautifully tracked.** Ahdia experiences it as *being caught* (exposure-as-defeat); Ruth as *a patient hitting the floor* (medic, not handler); Ryu as *the room getting more crowded* (his necessity diluting); Kain as *a logistics anomaly he can't close* (never sees Ahdia at all). Four characters, four knowledge-states, all internally consistent and all correctly *behind* the reader, who sees the whole mechanism. Exemplary irony layering.

4. **Ryu's unspoken love (the reader-sees/Ahdia-doesn't layer) is cleanly subtext.** His self-check confirms it's never named on the page; the reader holds it, Ahdia mostly doesn't. Final-state corroborates ("unspoken, telegraphed to reader"). Consistent.

5. **Kain's clone-survival and Bourn's ignorance of it** are the cleanest deep-irony split in the set (see F6).

---

## Verdict

**Conditional pass.** The *cornerstone* ironies — the protagonist fakeout (1), the dying secret (4), the M82 reveal asymmetry, Ryu's love, and Kain's clone-survival — are set up and tracked with real craft and strong cross-steward consistency. The reader's privileged-knowledge spine is largely intact.

But **three reader-knowledge anchors need Director locks before blocking**, all clustered on *when the reader and the team cross knowledge thresholds*:
- **F1/F2 (FIX):** the team's ~Ch25/M110 power-reveal is referenced by four stewards but staged by none, and Victor/Leah loosely anchor it to M82 — a 4-character premature-knowledge inconsistency. Assign and lock the M110 reveal beat.
- **F4/F5 (FIX):** the "transcendence-not-death," "Firas-displaced," and "Bellatrix-watching" layers are written as Book-1 reader-held irony, but none is set up in Book-1 footage. Decide per layer whether the reader holds it now (then stage it) or only retroactively (then stop writing it as held). Recommend: reader shares the characters' grief in Book 1 (transcendence + Firas-death sealed for Book 7); reader learns Bellatrix-watching only at Kain's epilogue.
- **F3/F6 (NOTE):** keep Bourn's fake-death read as suspicion-not-confirmation, and keep Kain's clone-survival sealed to the epilogue, so neither pre-empts a later reveal's punch.

No BLOCKERS. The flagged FIXes are about *anchoring the reader's knowledge transitions*, not rewriting content — the steward material itself is strong.

---

*Process note: claims sourced to specific steward files + canon (`BOOK1_MOVE_MAP.md`, `BOOK1_FINAL_STATE.md`). Character-knowledge facts queried as inputs; authoritative tracking deferred to Status Tracker. Confidence: high on layers 1–4 and the M82 asymmetry; medium on layers 5–6, where reader-knowledge anchoring is genuinely under-specified in the source docs and needs a Director call.*
