# CH18 Cold-Rewrite Packet — pilot for the first-draft rewrite pipeline

**What this is:** Everything a cold agent needs to produce a FIRST DRAFT of
Book 1 Chapter 18 (first-edition structure) without ever seeing the infected
prose. Beats and dialogue anchors extracted from
`first_edition/chapter_18.txt`; narration is regenerated from embodiment.
Director approves or kills the draft; nothing here is manuscript.

**Contamination rule:** The writing agent must NOT read
`6_manuscript/book_1/first_edition/`, `book1_manuscript.txt`, the epub, or
`6_manuscript/book_2/`. The disease lives there. The agent reads ONLY this
packet + the two files listed below.

**Load (the only repo files the agent opens):**
- `2_method_actor/book1_embodiment/Ruth_Carter_Book1_Embodiment.md` — BE Ruth per this
- `1_writing_guides/GOSQUAD_PROSE_VOICE.md` — series voice principles

---

## POV + situation

Ruth Carter POV, third limited, past tense. Mid-Book-1: the Go Squad is a
functioning six-person vigilante team (Firas off-page recovering from his
shooting; do not show him). Ruth runs coordination/tactical support and is the
team medic — ER doctor + dismissed cellular-regeneration researcher. The team
believes their enhanced abilities come from vague experimental military tech
(FAERIS drones overhead; Firas once vaguely mentioned "someone who wanted to
help"). **Truth withheld from Ruth AND reader at this point: the enhancements
are secretly Ahdia.** Do not hint.

## World constraints (added 2026-07-26 after v1 violations — see canon/book_1/CONSTRAINTS.yaml)

- **CON-B1-SECRET-IDENTITIES:** the public does NOT know any member's face,
  name, or civilian life. Go Squad are shadows/rumors/blurry footage. No
  civilian recognizes, approaches, or visits a team member. Codenames are
  fan-coined labels that exist online only.
- **CON-B1-SECRET-HQ:** no publicly known base. The Academy (Firas's parkour
  school) must NEVER be publicly linked to the Go Squad — no tributes,
  visitors, deliveries, or fan presence there. Fan gratitude reaches the team
  ONLINE ONLY (threads, posts, DMs). v1 violated this with a child at the
  front gate and flowers at the door.
- **CON-B1-NO-INVENTED-PROPER-NOUNS:** coin NO new names of any kind —
  streets, cities, businesses, hospitals, people. Use only names in this
  packet; otherwise stay generic ("a carjacking two weeks ago", "the
  precinct", "the hospital"). v1 violated this with "Delancey" and "Central
  City General". Name table: city = **Caledonia**; police = **CCPD** /
  "Caledonia Police" (never expand CCPD to anything else); neighborhood
  available: Little Poland; Firas's business: the Parkour Instructional
  School / "the Academy". Drafts are gated by
  `python3 _canon/tools/check_nouns.py <draft> --book book_1_ed1` — any name
  not in the Book 1 corpus kills the draft. The `--book` flag is required:
  the new `book_1` layer has no prose yet, so it is not a name corpus.

## Craft constraints (added after v2 Director review, 2026-07-26)

- **EPIGRAM BUDGET.** The closing aphorism — a short sententious clause that
  lands a paragraph's meaning ("...and she wrote the way out first", "which
  was medicine, most days", "Alone, then.") — is the AI's most reliable tic.
  v2 ran it ~8 times, twice on the identical template ("Alone, then." /
  "Triage, then."). HARD BUDGET: **at most 5 landed closers in the chapter,
  never the same syntactic shape twice.** Default: end paragraphs on the
  concrete image with nothing appended. The un-landed ones hit harder for the
  contrast; give the reader somewhere to put their own weight.
- **VILLAIN SPEECH = SUBTRACTION.** The Tank Cop is a hired human — smug,
  employed, enjoying the work — NOT a mission statement and NOT a void. (The
  void is reserved: a later book has a silent clone whose signature must not
  be pre-empted; the Tank stays a *person*.) He knows her name — "Dr. Carter"
  — and that alone lands the horror. He does NOT explain his employer's
  plans, does NOT flag her research as an asset, does NOT telegraph arcs.
  The pulse, if he mentions it at all, is offhand shop-talk, said while the
  ordinary face stays ordinary. NO stock lines ("Brave. Stupid, but brave"
  is retired — it was first-edition quarry, not canon).
- **VARY THE TAKEDOWN SHAPE.** Beat 7 must not run attack→dispatched three
  times in the same paragraph shape. Route at least one through Ruth's
  expertise (v2's Leah worked: "each placed exactly where Ruth would have
  marked a body for damage" + he *lets* them land — keep that
  characterization); give the others different structures — one can happen
  at the edge of her attention, one can be over before she parses it.
- **CUTTING A TIC MUST NOT CUT AN IDEA.** (v3 review.) The epigram budget is a
  budget on the *closing-aphorism shape*, not on thought. When you decline to
  land a paragraph, check whether an actual idea died with the cadence — if it
  did, keep the idea and give it a different shape (a behavioral beat, a
  concrete image, a flat statement). v3 cut the tic and lost two propositions
  with it. Behavioral showing is better craft, but a reader cannot infer an
  abstract proposition from a re-checked measurement alone.
- **EARN THE DROP.** Before a reversal, the character gets to stand somewhere.
  One clause of genuine pride/competence before the floor goes — the fall lands
  in proportion to the height. Restraint at the summit flattens the drop.
- **LOGISTICS MUST SURVIVE A REREAD.** Count bodies, hands, and casualties
  before writing an evacuation order. Who carries whom, and with what arm. A
  good line ("Everyone's cargo now") does not fix an impossible assignment.
- **NO DROPPED NOUNS.** Anything introduced on the page (drones on station,
  a second shift, a vehicle) must either pay off, be dismissed, or explain its
  own silence. An asset that watches the whole op and never registers the
  ambush is a hole, not set dressing.
- **A PATCH IS NOT LOCAL.** After any line-level fix, re-read the whole for
  the sentence it just made redundant. The v4 courtesy patch was correct and
  created a triple ("he isn't winded" three times) plus a new tic
  ("unhurried" ×4) because the downstream lines weren't re-checked. Patch,
  then sweep.
- **PRESERVE TEXT, NOT DESCRIPTIONS OF TEXT.** A good line reconstructed from
  a note about it comes back duller — "the only address grief could find:"
  became "because grief with nowhere to send itself goes to..." when
  paraphrased. Keeper lines go into RULES.yaml `protected_sites` as EXACT
  quotes so audit §4 screams if they vanish; never re-derive them from memory.
- **ENDINGS STAY IN REGISTER.** The final gesture must belong to the character
  who makes it. A tradesman does not wind up for a haymaker; he adjusts his
  grip. Reach for the procedural, unhurried version of any closing beat.
- **THE DRAIN IS A PHYSICAL EVENT.** This chapter's core is a body stripped
  of borrowed capacity — narrate it IN Ruth's body, not past it. The
  residency-wall register (v2's "stairwells taken at a sprint with a code
  called overhead") is the right mode; more of it, especially during the
  drain itself and on the docks (cold, wet air, smell are all available
  MID-scene — only chapter-openers ban scent).

## Canon locks (violating any = dead draft)

- **Ben's background is MILITARY, not police.** He has a *contact* at the
  precinct; he was never a cop ("old cop habit" in v2 was drift).
- **The enhancement mechanism (author-level knowledge — Ruth doesn't know
  this):** the team's abilities were NEVER in their bodies; they are
  distributed through external infrastructure the pulse CAN kill. So the EMP
  kills equipment and the relay; the team *feels* stripped. Never write the
  enhancement as in-body tech, an implant, or something a pulse could reach
  inside them to remove. The Tank believes his pulse turned off their
  augmentation — he is wrong about his own weapon, and the prose must not
  editorialize that he's wrong.

- Codenames (public fan-assigned thread is a beat): BATTLEA (Leah), NIGHT
  KNIGHT (Ben), CRIMSON SABLE (Victor), GLOOM GIRL (Tess), NIGHTINGALE (Ruth) [corrected per Director ruling 2026-08-29; Ahdia has no Go Squad codename]
- Rally cry, verbatim, as tradition Firas started: "No better place than
  here." → team: "No better time than now."
- The Tank: seven-foot armored figure; superhuman strength is REAL enhancement
  (unaffected by EMP); face under helmet is unsettlingly normal (~30,
  clean-shaven, coffee-shop forgettable). Knows her: "Dr. Carter." Sent by
  Kain. Do NOT name or explain him beyond this.
- EMP: kills team equipment AND their enhancements mid-op (reveal via
  equipment first, then the felt absence). Tank's line-sense preserved:
  their enhancement "can't be turned off with a magnet."
- Chapter ENDS mid-threat: Ruth cornered at the dock edge, water at her back,
  Tank's fist drawn. Hard cut. No rescue in this chapter.
- Kain: exposed and scrambling since the warehouse raid; CCPD can't openly
  protect him. This op is their 12th-ish this month.

## Beat scaffold (order fixed; texture yours)

1. **Briefing.** Tip via Ben's precinct contact: weapons cache, warehouse
   district 7 near the docks, 2100, minimal security, tight window. Ruth
   works schematics; plan: Victor+Ben loading dock, Tess+Leah roof access,
   Ruth perimeter comms.
2. **The fan beat — ONLINE ONLY (rewritten after v1).** Tess's phone: fan
   posts. A kid asking online whether the Go Squad does autographs (his
   sister was saved from a carjacking — no location named); a photo going
   around of flowers left at the spot of a rescue with a note ("Thank you
   for my daughter"); a fan account has assigned the codenames above. Nobody
   contacts the team directly — the public doesn't know who or where they
   are (CON-B1-SECRET-IDENTITIES / SECRET-HQ). Tess sheepishly admits she's
   used those names in the fan threads for months. "Firas is going to love
   this" / "Or kill me." Ruth, privately: being *named* by the people they
   protect changes the weight of the risk. (Do not sentimentalize.)
3. **Insertion.** Comms check; enhancement present (find Ruth's OWN image for
   the amplified feeling — the first edition's "weighted vest" simile may be
   kept or replaced). Rally cry. Entry goes clean.
4. **The trap.** Warehouse empty → floodlights, sirens, ~15 CCPD/SWAT units,
   megaphone surrender demand. False intel; ambush. Ruth calls it: smoke and
   scatter, Formation Delta, IR goggles.
5. **Trained escape.** All four out clean through smoke (Victor fence-vault;
   Tess smoke on the patrol cars; Ben flash-bang covering Leah's fire-escape
   exit). Ruth's professional satisfaction: training, not luck.
6. **EMP turn.** Her IR/GPS die on full charge; then the felt loss of
   enhancement; team reports the same, edge of panic. Ruth steadies them:
   trained people first, enhanced second.
7. **The Tank.** Walks through the smoke; hurls a fleeing officer 15 feet
   into a patrol car. Victor flanks — arm twisted, down. Leah's perfect
   strikes — nothing; swatted through a pallet. Ben lifted by the throat.
   Ruth breaks position, "Put him down!" — he drops Ben and walks toward her.
8. **The draw.** Ruth's triage: team down + police closing = she draws him
   off. Orders the team clear over protest ("That's an order"). Runs the
   quarter-mile to the docks; container maze; dead end at the water. Her
   medical eye prices the water: forty degrees, ten minutes to hypothermia.
9. **Face to face.** Radio static — alone. He unmasks: the normal face
   (keep the v2 quality: a face that offers nothing to remember). He knows
   her: "Dr. Carter." That is the payload — her name out of that armor.
   Speech per the VILLAIN SPEECH constraint: small talk from a hired man,
   not a briefing. The reader may infer who sent him; he delivers no memo.
10. **Hard cut.** She reads her options (water vs. man), moves, is caught;
    cornered at the edge, water at her back, the windup. End mid-threat.
    No stock lines.

## Register targets (the draft is MEASURED against these before the Director sees it)

| Measure | Target | Why |
|---|---|---|
| Length | 1,800–2,200 words | first-edition CH18 ≈ 1,940 |
| Dialogue share | 20–35% | action chapter |
| em-dash | ≤ 5 per 1,000 words | human-baseline rate; the first edition's 9.3/1K here is disease |
| short sentences (≤4 words) | ≤ 45 per 1,000 words | burst = impact, not default; CH18's 120/1K is the book's worst |
| "in her/his chest" | 0 | pure-AI marker (R103) |
| "X's voice was / voice came out" | 0 | pure-AI marker (R104) |
| "the particular" | 0 | R100 |
| negation formulas (not X, but Y / Not X. Not Y. / Didn't X. Didn't Y. / no X, no Y / wasn't just / so much as) | 0 in narration | R101 |
| hedges (a kind of / a sort of / something like / almost as if) | 0 in narration | R102 |
| "the kind of" | 0 | mined tic |
| looked/stared/glanced at | ≤ 1.5/1K | stage-direction formula |
| Scent words in the opening line | banned | NEGATIVE_CONSTRAINTS |
| Typography | straight quotes, closed em-dash (a—b), `...` ellipses, no bold/underscore markup | measured house style |

**Ruth register (from her embodiment + the census):** terse, imperative,
triage-cognition; the medical eye reads bodies as systems; compartmentalized
feeling with a visibly leaking seal (the fan-mail beat and "put him down" are
where it leaks); never the plot-explainer — clipped exposition that costs her
something; crisis SHARPENS her. Fight prose per three-beat rule: 2–3 sentences
of action, then sensation/assessment. Vary sentence length deliberately.
