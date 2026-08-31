# COLD-REWRITE PACKET — reusable template

> Generalized 2026-07-26 from the CH18 pilot (5 generations, Director-reviewed
> at every step). Copy this per chapter, fill the `<…>` slots, delete this
> block. The constraint sections below are NOT per-chapter — they are the
> accumulated judgment of the pilot and carry forward unchanged.

**The method in one line:** a cold agent (fresh context, no project history,
never shown the infected prose) writes a first draft from beats + embodiment +
constraints; three mechanical gates run before any human reads it; the Director
reviews only what passes.

**Why cold:** an agent with no history has no accumulated defaults — the pilot's
first cold draft cut fragment density from 120/1K to 44/1K on contact. The
trade is that it also has no knowledge, so **the packet is the memory.** Never
reuse an agent across drafts; always improve the packet instead.

---

## Fill these per chapter

- **Book / chapter:** `<book_N, chapter NN>`
- **POV + tense:** `<Character>, third limited, past`
- **Situation:** `<where in the arc; who is present; what the POV character
  knows and does NOT know at this moment; what is withheld from the reader>`
- **Load (the ONLY repo files the agent opens):**
  1. this packet
  2. **`1_writing_guides/voice_cards/<Character>_Book<N>_VOICE_CARD.md`** —
     the register authority. If no card exists for this POV, **build it first**;
     CH18 cost five Director rounds for a chapter whose voice layer didn't exist.
  3. `<path to the POV character's embodiment instruction>` — for WHAT, not HOW
  4. ~~`1_writing_guides/GOSQUAD_PROSE_VOICE.md`~~ — **PULLED FROM THE PACKET
     2026-07-26 by Director ruling. Do not load it.** It is not a register
     problem; it is a doctrine problem. It contains live instructions that
     countermand `canon/series/RULES.yaml` inside the same context window
     ("Fragments land as beats, not errors. Don't 'fix' them"; a section headed
     "Em-Dashes for Pivots") and those instructions win, because they read as
     permission and are more specific than a lint rule. Its named style
     exemplars are ch22 (88.0 burst) and ch27 (104.3) against an author
     baseline of 24.9 — both post-ch12 AI-era chapters. Its "66% dialogue"
     prescription is unfounded at any level of measurement (see below). The
     likely history: the guide was written by observing the book's most
     distinctive-feeling chapters, which were the infected ones. It did not
     catch the infection; it canonized it, and has transmitted it since.
     **Rebuild required, not edits. Blocked until then.**
- **Beat scaffold:** `<numbered, order fixed, texture free. Extract from the
  existing chapter's events — never from its prose.>`
- **Canon locks:** `<verbatim lines that must survive; character facts; the
  chapter's entry and exit state; anything a wrong guess would break>`

**Contamination rule (state it in the agent prompt too):** the agent must not
open the first-edition prose, prior drafts of this chapter, other books'
manuscripts, or any .epub. The packet is its entire world.

---

## World constraints (carry forward; add per book)

- **SECRECY / public knowledge:** `<what the world knows about the cast at this
  point — get this exact; the pilot's v1 put a civilian at the team's door>`
- **NO INVENTED PROPER NOUNS.** The agent may coin no new name of any kind —
  streets, cities, businesses, hospitals, brands, people. Only names in this
  packet are available; everything else stays generic ("the precinct", "a
  hospital", "a carjacking two weeks ago"). Include a **name table** of every
  proper noun the chapter may use. Enforced by `check_nouns.py`; one invented
  name kills the draft.


## ⚠️ REGISTER FIREWALL (measured 2026-07-26 — state this in the agent prompt)

The reference documents are analytical instruments written in an
essayistic-aphoristic register. A cold agent absorbs rhetorical signature along
with content. Words per 1,000, against the author's own pre-AI prose:

| corpus | burst | em-dash | aphorism |
|---|---|---|---|
| **Author (ed1 ch1-11) = THE TARGET** | **24.9** | **1.3** | **0.68** |
| the embodiments (loaded into every agent) | 23.2 | **23.5** | 1.20 |
| GOSQUAD_PROSE_VOICE.md (loaded into every agent) | **75.1** | 10.4 | **3.89** |
| steward run outlines | 40.2 | 17.7 | **5.70** |
| chapter structure docs | **80.2** | 4.8 | 2.35 |
| ed1 ch24-29 (the disease) | 98.4 | 16.1 | 4.55 |

**Read the reference corpus for WHAT, never for HOW.** The only register
authority is the author's own prose, the register table below, and the POV
character's voice card.

## Generative constraints — what to BUILD (not just avoid)

Guardrails alone produce careful prose, not distinctive prose. Every packet
must state, positively:

- **The POV character's five sentence-DOs** (from their voice card) — the
  operations their sentences perform, not traits they possess.
- **Their metaphor domain.** The two or three fields they may reach into for
  imagery (Ruth: medicine, ER logistics, drills). Outside it = not their voice.
- **One structural discovery to attempt.** Ask the agent for at least one beat
  where form does the work — CH18's best invention was Victor going down in
  Ruth's *peripheral vision*, which broke a checklist rhythm AND proved she was
  slowed, without saying so. Name this as a goal, not a hope.
- **The chapter's one unsayable thing** — what this POV knows and cannot say
  here. Concealment dramatized beats subject erased. (A POV with nothing to
  think about produces hollow chapters; that is the diagnosis for Book 2's
  nine Ahdia chapters.)
- **What the prose should cost the reader.** The feeling the chapter is buying.

## Craft constraints (carry forward unchanged — each earned by a rejected draft)

- **EPIGRAM BUDGET — max 5 per chapter, never the same syntactic shape twice.**
  The closing aphorism (a short sententious clause that lands a paragraph's
  meaning) is the model's most reliable tic; at fifteen it stops reading as
  authorial signature and becomes generation habit. Default: end on the
  concrete image with nothing appended. Instruct the agent explicitly: *when
  you finish a paragraph, check whether the last clause interprets what came
  before it; if so, cut it.*
- **CUTTING A TIC MUST NOT CUT AN IDEA.** The budget constrains a *shape*, not
  a thought. If declining to land a paragraph kills an actual proposition,
  keep the proposition and give it another form. A reader cannot infer an
  abstract idea from a behavioral beat alone.
- **VILLAIN / ANTAGONIST SPEECH = SUBTRACTION.** No employer memos, no
  arc-telegraphing, no stock menace lines. What the antagonist *knows* is the
  payload; what he explains is the author talking. Give him an occupation and
  let him sound like it.
- **EARN THE DROP.** Before a reversal, one clause of genuine pride or
  competence. The fall lands in proportion to the height.
- **VARY REPEATED STRUCTURES.** Three characters falling in three
  identically-shaped paragraphs is a checklist. Route one through the POV
  character's expertise; put one at the edge of their attention; make one
  over before it can be parsed.
- **THE BODY IS PRESENT.** Whatever the chapter's central physical event is,
  narrate it *in* the POV character's body. Sensory registers beyond the
  visual — weight, breath, temperature, smell — are available mid-scene
  (only chapter *openers* ban scent, per NEGATIVE_CONSTRAINTS).
- **LOGISTICS SURVIVE A REREAD.** Count bodies, hands, and injuries before
  writing an order. A good line does not fix an impossible assignment.
- **NO DROPPED NOUNS.** Anything introduced (a drone on station, a second
  shift, a vehicle) must pay off, be dismissed, or explain its own silence.
- **ENDINGS STAY IN REGISTER.** The final gesture belongs to the character who
  makes it. A tradesman adjusts his grip; he does not wind up.
- **A PATCH IS NOT LOCAL.** (For revision passes.) After any line-level fix,
  re-read the whole for the sentence it just made redundant.
- **PRESERVE TEXT, NOT DESCRIPTIONS OF TEXT.** A good line reconstructed from
  a note about it comes back duller. Keeper lines go into
  `canon/<book>/RULES.yaml` `protected_sites` as exact quotes; `audit.py` §4
  then screams if one vanishes.

---

## Register targets (tune per chapter; defaults from the pilot)

| Measure | Target | Note |
|---|---|---|
| Length | `<±10% of the source chapter>` | |
| Dialogue share | `<20–35% for action; higher for talk scenes>` | |
| em-dash | **≤ 2 / 1,000** (author measures 1.3) | disease runs 9–21; ceilings were set against the DISEASE and are being rebased on the AUTHOR |
| short sentences (≤4 words) | **≤ 30 / 1,000** (author measures 24.9) | burst = impact, not default |
| aphorism probes | ≤ 0.7 / 1,000 (author's rate) | the reference corpus runs 4–6× this |
| "the particular" | 0 | R100 |
| negation formulas | 0 in narration | R101 (full family) |
| hedges | 0 in narration | R102 |
| "in her/his chest" | 0 | R103 — pure-AI marker |
| "X's voice was" / "voice came out" | 0 | R104 — pure-AI marker |
| "the kind of" | 0 | mined tic |
| looked/stared/glanced at | ≤ 1.5 / 1,000 | stage-direction formula |
| scent in the opening line | banned | NEGATIVE_CONSTRAINTS |
| Typography | straight quotes, closed em-dash, `...` ellipses, no `**`/`_` | measured house style |

**Ceilings are not styles.** Landing far under a target is not better; if the
prose reads airless, loosen the number for that chapter.

---

## The gates (run all three before the Director reads anything)

```bash
python3 _canon/tools/tic_census.py  --book <book>          # register
python3 _canon/tools/check_nouns.py <draft> --book <book>  # invented names
python3 _canon/tools/audit.py       --book <book> --stats  # rule hits
```
Plus a human pass for what no gate can see: canon violations, logistics holes,
dropped nouns, epigram count (judgment, not regex), and whether it is any good.

## Generalization test (falsifiable)

CH18 took five rounds because the packet was being invented during it. If a
chapter drafted from THIS template needs more than **two** Director rounds, the
template has not generalized and the pipeline is blocked pending a redesign —
not another round. Record the round count for every chapter.

## Stopping rule

Stop when the remaining irregularities are the places where it sounds like a
person wrote it. The gates will happily accept a v6, v7, v8 — each smoother
and less alive. Convergence is not zero-defect.

## RESERVED TRAITS — carry this block into every packet (ruled 2026-08-31)

**Counting belongs to Ahdia alone.** If the POV character is not Ahdia, they
do not count under stress, do not tally, and do not do arithmetic about their
own life — and neither does the narration on their behalf. The banned shape is
*count + subordinate clause explaining the psychology*:

> ~~She counted the doors on both sides, the way she counted them in any
> building she had not chosen to enter.~~
> ~~Ruth counted the bill line by line because counting was the only medicine
> available.~~
> ~~Ruth crossed to her in eleven counted steps.~~

Also banned outside Ahdia's POV: the **accounting-metaphor family** —
arithmetic, the ledger, came due, an accounting, the bill, exchange rate — used
figuratively. **The author's rate for both is zero** across all 23,536 words of
his own chapters; the rewrite layer had reached 1.59/1K before this was caught.

The fix is nearly always **deletion**, not replacement: the counting frame is
usually bolted onto an observation that already worked, and the inventory that
follows it already *is* the reading. Where something must stand in its place,
use what the author uses — physical business in the dialogue tag, trained
professional habit rendered as action, or plain statement. Show the hands.

