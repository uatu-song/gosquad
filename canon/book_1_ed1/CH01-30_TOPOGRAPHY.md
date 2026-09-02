# Book 1, ch1–30 + epilogue — Topography for cold agents

**This file SUPERSEDES `CH01-11_TOPOGRAPHY.md`, `CH01-22_TOPOGRAPHY.md` AND
`CH01-25_TOPOGRAPHY.md`.** It carries forward everything in those files that
still holds and extends it through the end of the book (ch26–30 and the
epilogue), with the ch22 entry REPLACED (the chapter was rebuilt after the
ch25 file was written) and every ruling logged 2026-08-30 → 2026-09-02
applied. Read this one alone and you have the whole world; do not also load
the older files, and where they disagree, THIS FILE WINS. Where this file and
`DECISIONS_LOG.md` disagree, the log wins; where this file and the shipped
draft disagree, say so rather than guess — a list of the collisions found
while writing it is at the bottom, UNRESOLVED ON PURPOSE.

## STATUS

- **Shipped:** 30 chapters + epilogue. Ch1–11 are the author's own, vetted;
  ch12–30 are metric rebuilds gated against frozen source dialogue. The
  epilogue is ch30's final section, promoted to a labelled Epilogue with its
  own TOC entry in the ARC build (presentation only; no text changed).
- **ARC:** `6_manuscript/book_1/GoSquad_Book1_ARC.epub`, cut at commit
  **8d6417f**. `build_compilation_epub.py` remains the working artifact; the
  ARC script formats and never edits.
- **Word count: 77,584.** ch01 2172 · ch02 3269 · ch03 2717 · ch04 2187 ·
  ch05 2297 · ch06 1854 · ch07 1849 · ch08 551 · ch09 2244 · ch10 1932 ·
  ch11 1976 · ch12 2276 · ch13 2832 · ch14 5803 (14a+14b) · ch15 4272 ·
  ch16 2264 · ch17 3503 · ch18 2108 (v3) · ch19 2582 · ch20 3316 · ch21 3776 ·
  ch22 3457 · ch23 2579 · ch24 2008 · ch25 1231 · ch26 3036 · ch27 1212 ·
  ch28 1665 · ch29 2286 · ch30 4330 (incl. epilogue).
- **Gates: green.** Every rebuilt chapter passes all bands; ch14a+b as a
  pair; **ch22 green on its ruled length band 3000:3600** (the source-derived
  ±20% band is explicitly overridden for ch22 only, log 2026-09-01). Adverb
  band is ceiling-only (0–17/1K), no floor. Dropped-tag census: **0 across
  all 30 chapters** (log 2026-09-02). Frozen spans byte-identical everywhere
  verified (ch19 81/81, ch21 162/162, ch22 44/44, ch30 176/176).
- **Veto-open crew calls that touch facts in this file** (log): the figure
  "twenty-six hours" (Director delegated the number; crew derived it);
  Colonel Mack as the Main Street ground commander; the ch22 "That was fun"
  reorder; the ch30 paragraph merge; ch25's "two weeks" read as
  characterised error; "Marky Mark" kept. Staging A for ch22 is **ruled**,
  no longer a crew default.

**Canonical draft filenames are resolved through
`6_manuscript/book_1/build_compilation_epub.py`, never by convention.** Every
rebuilt chapter is `chapter_NN_metric_v1.txt` EXCEPT **ch18, which is
`chapter_18_metric_v3.txt`** — a holdover from the five-generation pilot.
`chapter_18_metric_v1.txt` is a dead draft. Editing it silently does nothing.
Ch1–11 live in `first_edition_clean/`. Frozen-dialogue authority for every
rebuilt chapter is `first_edition_clean/chapter_NN.txt`.

**What this is:** the vetted map of everything established in the shipped
book, so an agent drafting Book 2 material or a Book 2 steward inherits the
world without spending a context window on the prose. For voice and register
this file is useless: that is `STYLE_PROFILE.md` plus your packet's
exemplars. For how Ahdia's power works — trigger, field, cost, the team's
distributed abilities, the calendar, the fifth Tank, naming — use
`../series/TEMPORAL_MECHANICS.md`, which is the arbiter and is not duplicated
here. **Three of its sections lag the log (see the collisions list): the log
wins.**

**How to use it:** read all of it. If your work touches a specific scene (a
callback, a returning location, a repeated line), ask for that single
chapter's full text rather than guessing texture from this summary.

---

**THE TANKS ARE FIVE, NOT FOUR** (ruled 2026-08-30, bible §7h). Edgar, Ogden,
Philips and Orlansky are the four who fight at Main Street; **all four are
dead by the end of ch27** — husks, the Heart's fragments drawn out of them
and back into Kain. The fifth — the articulate one with the forgettable face
who hunts Ruth in ch18 and goes through a container in ch19 — **survives,
off the board, and never returns in Book 1.** Never add him to a Main Street
scene; never name him among the four. Ahdia's push is not a kill; **she has no
body count in Book 1**, and nobody ever tells her she removed an enemy
permanently about twenty-six hours before the climax.

## NOBODY COUNTS — the banned families (ruled 2026-08-31; the Ahdia carve-out REVERSED the same day)

**NOBODY COUNTS. There is no character exemption, Ahdia included.** The
morning's "reserved to Ahdia" formulation was a crew carve-out written
without asking and was reversed by the Director ("get rid of that",
unqualified). Any counting-as-interiority hit in any chapter is a defect
regardless of POV. Series rules R105/R106.

Banned corpus-wide in narration:
- **Counting as interiority** — a POV character counting under stress,
  tallying, doing arithmetic about their own life; the shape is *count + a
  subordinate clause explaining the psychology*. Not the tic: the idiomatic
  verb ("counted as applause"), machines counting (a timestamp, a reply
  count), Ryu counting aloud on his fingers in ch24 (the author's own beat),
  Kain's forty-seven-second elevator in the epilogue (his cognition, author's
  beat), and frozen dialogue.
- **The accounting-metaphor family** — arithmetic, the ledger, came due, an
  accounting, the bill, exchange rate, priced. **Exempt inside Kain's POV
  only** (Director, ch27 review: "when the metaphor system belongs to the
  character's actual worldview it stops being a tell and becomes voice").
  Kain's chapters run on it; nobody else's may.
- **The "X, the way Y verbs" simile frame** — swept to zero outside ch26,
  where seven remain under the Director's own hand. Directional idioms ("the
  way in") are not the tic.
- **Trailing ", which is/was" clauses** — not a ban; the author uses it once;
  clusters thinned (Director: "thin clusters only").
- **Unlicensed adverbs** — the narrator-appraisal family (patiently,
  entirely, visibly, briefly, thoroughly, personally, deliberately,
  currently, and the over-hot licensed six). Kill-list at zero in narration.
  Dialogue untouched. Rebuild-packet rule: reduce a tag to "said"; never drop
  it.

The author's own rate for all of these is zero or near it. What he does in
that slot is physical business, trained habit rendered as action, or plain
statement. He shows the hands.

## WHAT PEOPLE CALL EACH OTHER (ruled 2026-08-30 — bible §7g; extended 2026-08-31 for ch28–29)

Naming follows **whose head the narration is in**, not whether it is a fight.

- **Ruth's proximity → first names** (Ben, Victor, Leah, Tess), even mid-battle.
- **Ahdia's proximity → codenames** for as long as she has never met them.
  **That expired in ch25**, and the Director ruled the vocabulary DRIFTS BY
  CONTACT across ch28–29, unremarked by the narration: **Battlea becomes
  LEAH the moment she shoves Ahdia clear of the fist (ch28); Crimson Sable
  becomes VICTOR the moment he takes the backhand into the pharmacy (ch28);
  Night Knight and Gloom Girl stay codenames until the human-chain paragraph
  of ch29, where they become BEN and TESS and nowhere earlier.** Ruth and
  Firas are always names in her head. Do not back-port the drift into ch26,
  where she still reads the roofs as Gloom Girl, Battlea, Night Knight,
  Crimson Sable.
- **The team's own proximity →** codenames on the job, first names off it.
- **Public / press / external cameras →** codenames, plus "the Go Squad."
- **Kain's proximity →** "the girl," "the medic," codenames; never a first
  name for the team. He has had a file on **Ruth Carter** since ch17.
- **CADENS →** "Auerbach" (Bourn, Ryu, the badge), "Ms. Bacchus" (Bourn,
  once, ch30, at the moment she files her as closed), "Dr. Carter." Ryu's
  "Dr." wore off in the ch30 debrief and nobody went back for it — first-name
  basis, nothing said about it. **"Overseer"** is Bourn: Ryu says "Overseer
  wants to see you" (ch30); Mack reports to "Overseer" by comm (ch28).
- **The ground at Main Street is Colonel Bentley Mack, never Bourn.** Bourn
  is Overseer and is never on the pavement (ch28/29 corrections, derived from
  locked canon; veto open on Mack).

The gap between what Ruth calls them and what Ahdia calls them measures how
alone Ahdia has been; the drift in ch28–29 is that gap closing at the moment
every one of them has hands on her. Do not flatten it and do not comment on it.

**Register follows POV as well** (bible §7g). Wit lives in dialogue; the
narration takes its temperature from whose head it is in. Kain's chapters are
cold and Ruth-under-threat is dry, and that is correct. Ch24 scores zero on
comedy and should. Never raise comic density in a chapter whose POV character
is not funny.

## AGES (ruled 2026-09-01)

**Ahdia is TWENTY-SEVEN.** Both sites (ch14a's heart-attack line, ch19's
"twenty-seven years old") now read twenty-seven; twenty-three is gone. That
puts **Firas at twenty-five**, founding the team at twenty-one. **Ahdia was
EIGHT at Montana, Firas six** (ch02 corrected; ch03's "over fifteen years
ago" is the anchor). The book is **undated**: late September at the docks,
and **August 14 is the only date ever named** (ch13 playback). No year, no
month otherwise, no calendar arithmetic on the page.

## THE CAST (the ruled codename map — do not deviate)

| Person | Codename | Sketch | State at end of book |
|---|---|---|---|
| **Firas Bacchus** | none — he refused one | Founder. Owns the Parkour Instructional School ("the Academy"). Disciplined, corny one-liners he can't land, radio-jargon nerd. Shotgunned CH03; bedridden CH04; walking on it anyway from ch21. Vigilantism began as suicide-avoidance after the parents vanished. Wears his armor under his clothes "just in case." | **PAGE-LEVEL: LOST.** Drove a sedan into Kain (ch26), gave Ahdia his armor, held her hands at the singularity with no Seed and no field, injected her with the palmed dose, and went into the point: "went down into a space smaller than a fist and was absorbed. Gone." Every character reads death ("Yesterday, we lost someone"). **AUTHOR-LEVEL: DISPLACED, NOT DEAD** (bible §5b endpoint; log ch29/ch30) — never on the page, never in any character's mouth. |
| **Ahdia Bacchus** | **AUERBACH** (CADENS-issued, ch15; she "never once answered to [it] in her own head") | Firas's OLDER sister, **27**. Ex-shut-in on inheritance money; smokes Parliaments, processes everything through TV/movies; does the voiceover on herself from slightly to the left. Shot CH07, presumed dead in the CH08 fire. Bonded to the Hyper Seed. CADENS asset from ch13. | **Alive. Seed "dormant. Maybe permanently"** (her words, ch30). Pushed and pulled at once through one body (ch29); went into the corridor and was put back. **Declined the CADENS badge.** Told CADENS she is going back to her couch; **is in fact running the team from a stolen CADENS mobile command center on a roof**, unlit cigarette in hand. Gave Ruth access to her penthouse and bank account (Ruth's line, ch30). Has told no one about the corridor beyond "somewhere else" / "a collapsing dimension." |
| **Ruth Carter** | NIGHTINGALE ("Gale") | ER doctor, Johns Hopkins, Firas's girlfriend of years. Invented CR-7. Best traceur on the team. Field lead while Firas is down. Has no power and never did — her case is the one §7 leaves AMBIGUOUS forever. | **Leads the Go Squad.** Called it over ("It's all over... we're not the Go Squad without Firas"), then rebuilt it on Ahdia's return: "we start over... cataclysms, cops and Kain." Organised the human chain. Bruised throat from ch24. **Never absolved in words; followed in fact.** Heels left the gravel an inch on the last roof — unexplained on the page. |
| **Ben Bukowski** | NIGHT KNIGHT | Ex-marine, personal trainer. Tactical lead. Argues for guns, never crosses the line. Precinct contact who feeds him tips (ch18). | Alive. Held Edgar in a restraint (ch27); tackled Leah, Victor and Ahdia out of the fist's radius (ch28); anchored Leah in the chain. Holds the line on the drives: "We have the proof to expose the cops." Old vest over the new suit. |
| **Leah Turner** | BATTLEA ("Lea") | Barista at the Bean Post; jammer, Caledonia Roller Derby. Fastest of the team; joined for her anger issues. Anger-management workbooks she actually does. | Alive. Shoved Ahdia clear of the fist (ch28); ran across Kain's front for Victor; held Victor in the chain. Delivered the "You've been carrying us" speech to Ruth (ch30). Skating pads over the new suit. |
| **Tess Whitford** | GLOOM GIRL ("Gloomy") | Depression, Sertraline 100mg. Bankrolls gear hardest after Firas. Agile, not fast; goes around things. Runs the Go Squad social accounts — she started #GoSquad. **Chief John Whitford is her father** (Ruth, ch12: "your father, the Caledonia Police Chief"); estranged. Her translocation is the only power that survived the docks (drone-executed). Wants a different codename since the ch22 alley; has not chosen one. | Alive. Got the whole team out of the mansion (ch22). Ported Firas off the sidewalk during the drop (ch27) and came back; **said "We killed them"** (ruled hers, ch28) and was gone with Firas before the missile; the end of the chain, legs against the bus (ch29). Hood up on the last roof. A FAERIS drone settled on her shoulder in ch25 and was never explained. |
| **Victor Hernandez** | CRIMSON SABLE ("Crimson") | Director at a shoestring community nonprofit. Fights with found staffs (rebar). Private. **No dead wife — ruled, ever.** | Alive; **right arm in a sling "from the pull, not the temporal forces."** Backhanded into the pharmacy's second floor (ch28). His consumer advocacy group has **filed a lawsuit over the money paid to the Kain PAC**; expects the drives to hit the PAC and leave Kain clean. Rebar taped at one end on the last roof. |

**The team is EXACTLY six** (Firas + five) and **ends the book at five on the
page**, with Ahdia on comms. Never invent a seventh member, support staff, or
recruit. Codenames are years old; **in CH12 all five give up their real names
to each other** for the first time. Ruth+Firas were always the exception.

---

## THE CITY AND ITS INSTITUTIONS

- **Caledonia:** third-biggest US city, between twin rivers, 150-year commerce
  hub. Named places you may use: Little Poland, Renata's Bakery on Grand, the
  Natural History Museum on Grand Ave, Caledonia Harbor/the docks (District 7),
  the Overlook, midtown (Ahdia's penthouse, 34th floor, keycard access), the
  Frederick Douglass Bridge, Old Caledonia, the Bean Post, Rodriguez's Bodega on
  Morrison Street, Montclair Country Club, Kain's tower and mansion, and now
  **Main Street downtown** — the intersection with the bank (ten stories;
  leaned and held), the pharmacy (second floor took Victor), the overturned
  bus, the sandwich place, a mailbox, a hydrant, and the crater, scorch going
  pale at the edges. Bourn: "downtown looks like a meteor strike." Coin
  nothing else.
- **CCPD** runs a near-police-state under **Chief John Whitford** — military
  equipment, qualified immunity, raids filed under "probable cause." Kain owns
  him: the drives Ben copied in ch21 contain proof the chief is on Kain's
  payroll. **Nothing has been done with them by the end of the book.**
- **The Academy** is publicly a parkour school and covertly the base. Firas
  built the team's whole method there — silent footfalls, lifting and tossing
  one another to reach grips, the dark routine, smoke and goggles — and ch22
  is that method at full size on the one night he could not climb the
  stairs. **The team does not drive — ever** (bible §7b). **Two ruled
  exceptions, no more:** a vehicle used as COVER, hired under a false name
  and abandoned with the disguise (the ch21 catering van); and **the endgame
  MCC — a BASE, not transport** (see CADENS). Wingsuits are descent gear
  licensed from ch30. Neither licenses a car, a van, or a team vehicle in any
  book. **UNRULED COLLISION:** ch26 has Firas — benched, in civilian clothes —
  drive a gray civilian sedan with a front-quarter dent Ahdia recognises into
  Kain. §7b lists no exception for it and the log has no entry. Do not extend
  it into precedent; do not "fix" it; flag it.
- **Rules of the squad:** stay secret, never take credit; NO GUNS; take people
  down, don't kill them. **The no-kill line broke without their knowledge in
  ch27** — the four Tanks died at their hands because Kain had seeded them
  with the Heart's fragments to be broken open. Ruth saw the light move first
  ("You're feeding him!"). **Nobody on the page has processed it after ch28**;
  ch30 does not mention the Tanks.
- **Secrecy** is gone in practice: Tess's posts made the codenames public
  (ch18); a neighbour asked Leah for a photograph (ch22: "We see you. All of
  us."); the mansion, Main Street and the singularity happened in front of
  cameras. What the public was TOLD about the Main Street night: **a
  "supposed critical gas leak in the city's center," a full evacuation of
  Caledonia, the National Guard called in** (Carl Tucker, ch30) — and, from
  Kain, **a "terrorist attack" by "criminal elements" impersonating him.** No
  chapter states what the public believes about the Go Squad's part in it.
- **The rally cry** (Firas's, from their first job): "No better place than
  here." / "No better time than now." Ch1 (Firas and Ruth on the radio), ch7,
  ch18 before the docks, ch21 before the gala, ch22 as Ruth's phone-call
  identifier, **ch26 — Ahdia screams the first half from the middle of Main
  Street and the roofs scream back the second (ch27 opens on it)**, and
  **ch30 — Ruth on the ledge: "No better place." / "No better time," they said
  back.**
- **The public** runs #GoSquad, #CaledoniaHope, #CaledoniaHeroes, compilation
  videos, @CaledoniaNights, @WestSideWatch. Kain's friendly media: "Carl Tucker
  Tonight," which framed the evacuation as leadership hysteria over "prank
  calls from some yahoos."
- **CR-7:** Ruth's cellular-regeneration therapy; three years of dismissed
  research; first human use on Firas. In ch20 she builds **CR-7 Temporal
  Variant** in a CADENS lab in four hours — pale blue. **Nine doses, THREE
  WEEKS apart, then monthly** (bible §7e). Dose one goes in at ch20. In ch24
  Ahdia lines up the remaining eight and **takes SEVEN in about fifteen
  seconds of self-acceleration; the eighth she fakes — "nothing went in. Her
  fist took it under the gown"** (Director-ruled, ch29 entry; 11 words changed
  in ch24; nobody in the room notices). Ryu reads the sequence as "maybe
  thirty percent total regeneration"; CADENS' later scan says she left at
  "approximately one-third cellular recovery." **The palmed dose rides at her
  hip through ch25–29 and goes into HER, by Firas's hand, at the singularity.**
  No dose remains on the page. Her treatment status after ch29 is **not
  stated in numbers anywhere**; do not supply one.

---

## CADENS

- **Cataclysm Activity Detection and Engagement Network Sentry** — exactly one
  expansion, ever. Monitors and responds to cosmic-level threats: dimensional
  incursions, reality fractures, artifacts. 247 active monitoring sites (890
  during the Cold War). A meta-human tracking board — "hundreds of them" (Tess,
  ch23). Personnel files on the team by face and legal name (Victor found his,
  ch23).
- Funded through Special Access Programs, black budget, autonomous. Only the
  Secretary of Defense has contact with its leadership and cannot give it
  orders. Its head answers to one person: **Director, codename OVERSEER**.
  **Director Harriet Bourn IS Overseer** ("Director Overseer Bourn," ch19).
  **Above her someone pulls strings** (ch30): she requested executive
  clearance to intervene **six hours before Ahdia went downtown** and received
  it **fourteen hours after the event concluded, forty-seven minutes before
  her ch30 scene with Ryu**, with a note thanking CADENS for its "patience and
  restraint during the review process." Her reading: "They wanted plausible
  deniability. If Auerbach failed, no connection to CADENS. If she succeeded,
  no political fallout." Her plan: "We document everything. We build the
  file. And we wait." Her closing instruction: "Monitor cataclysm activity.
  **Track the Seed-bearers.**" — plural; other Seed-bearers exist and are
  tracked. Nothing more is said about them.
- **Director Harriet Bourn** — silver-gray, past fifty-five, boardroom suits,
  flat affect, keeps her beliefs like spare batteries. Sent Ahdia downtown by
  saying "We're out of time" (ch24) and "wrote it up as a result." Verdict on
  the palmed dose: "It was reckless. And effective." Never confronts Ahdia
  about it. Asked "How close did you come to draining all of your life force
  yesterday?" and got a cashier's smile. **Colonel Bentley Mack** — military
  bearing, dry; **commands the ground at Main Street (ch28–29)**, twenty
  operators in black kit; ordered deployment over protocol in ch23 ("Override
  that... NOW"); **fired the cruise missile into Kain without waiting for the
  Pentagon**: "Overseer wanted authorization before engaging. Pentagon wanted
  assurances. SecDef wanted contingencies. We stopped waiting... Some things
  are more important than careers, ma'am." **Dr. Ryu Matsuda** — late
  twenties, Japanese, FAERIS Operations, over-talks, Spider-Man and Dragon
  Ball Z; the only person who can interface with FAERIS without the drones
  going haywire; Ahdia's handler and Ruth's guide. **Ryu Matsuda is the name;
  "Shiba" was drift and is gone; "Marcus" never appears.** Let Ahdia leave the
  facility early (ch30) and is not admonished for it. Other CADENS codenames
  on the page: Howitzer, Greyhound, Mercury, HAZARD (a comms voice, ch23).
- **The facility:** underground under a nondescript government office building,
  four hundred feet of rock. Command floor with a wall of live disaster feeds
  (thirty-one crises on four continents, ch23), Research Division, medical
  bay, armory, training room, quarters (Ahdia has Quarters 7), a surveillance
  bunker, a landing pad, and **a hangar** — from which Ahdia removed a mobile
  command center "without filling in anything" (ch30). Translocation vomit
  has a cleanup protocol ("Protocol Sigma"). Ahdia's chair in Bourn's office
  is too low for the desk and she will never mention it.
- **CADENS' classification of the ending:** "a Terminus-level gravitational
  anomaly" (Bourn, ch30); "cataclysm science is still in its nascence"
  (Ahdia, and Bourn agrees). The mechanism, in CADENS' words: "opposing
  temporal forces to burn out the Tamois essence while containing the
  collapse."
- **FAERIS** — Field-Adaptive Entanglement Reconnaissance and Infiltration
  System. Drones. Surveillance, holographic playback, translocation, and the
  amplification half of the team's "powers." **They are learning** (ch20):
  three days before the gala one performed an enhancement alone, no Ahdia, no
  temporal field, at ~10% effectiveness; projection 50% in six months, full
  capability in twelve to eighteen months. One turned to face the observation
  window. In ch25 one **settled on Tess's shoulder and stayed** when told to
  go; never explained. Ryu will not use the word "sentient."
- **Ahdia's kit (ch15):** matte-black armored suit rated for temporal shear,
  bulletproof plates; AR HUD; a panic watch; a black domino mask; a silver
  crest — cracked shield, CADENS, **AUERBACH**. **She fought Main Street in
  none of it** — hospital gown, then Firas's armor. **The badge** (ch30):
  silver, cracked shield, the agency's letters, the name — offered by Bourn
  with "your methods are not CADENS ways of doing things, but that's where
  you'd be an asset"; **declined.** "Let me know if you ever change your
  mind. Until then, I trust you can keep CADENS under your hat." "We have no
  reason to monitor you anymore, Ms. Bacchus."
- **CADENS' terms with Ahdia (ch14b–15):** she works with them; they spend
  everything on extending her life. Her condition: **the deception holds.**
  **It did not hold** — Ruth told the team in ch23, Ahdia told them herself in
  ch25 — and CADENS never raises the breach. By ch30 CADENS treats her as an
  asset that has stopped producing.
- **CADENS' terms with Ruth (ch19–20):** keep Ahdia alive; full lab; be the
  liaison and "manage the transition." **Also moot by ch30**; Ruth is on the
  page in the team's living room and on the roof, not at the facility. Her
  liaison status is never formally ended on the page.
- **The team's suits (ch23/ch30):** four cases of matte-black armor cut to
  measurements nobody gave, boots with derby laces run through. The team took
  them without clearance (ch23), fought in them, and **"the armored cases had
  gone back down the elevator that morning with two men who signed for
  them"** (ch30) — CADENS reclaimed them. On the last roof **all five are in
  "the matte black armor, cut to their measurements, the same suits that had
  come off them after downtown."** No one explains it; no one comments.
  (Log: the stolen-armor payoff — Ahdia's duffel by the door. Reader-level
  inference; the page never says she took them.)
- **The MCC (ch30, Director-ruled, bible §7b second exception):** "a machine
  she had taken out of a hangar," "a machine that belonged to nobody," cloaked
  ("forty feet of nothing hummed on a residential roof and threw no shadow at
  all"), thirty blocks south of the roof the team launches from; a horseshoe
  of monitors "she had no clearance to touch." **A base, not transport:
  nobody drives it anywhere, ever.** The bible places it on the roof of her
  penthouse; the page says "a residential roof." **CADENS is not shown
  noticing the theft**; Ryu's line about "equipment inventory" is the only
  cue and it is not attached to it.

---

## THE OPPOSITION

- **Harding Kain** — DIAMOND MAGNATE, TRIOMF, presidential candidate (election
  in November). Not a mayor. Rotund, heavy rings, three-piece suits, bad
  hairpiece. Three generations: grandfather pulled diamonds and broke strikes,
  father built the armored cars. Monetize fear, call it safety. Prices
  everything; hates what he cannot price. Aide: **Reed** (ch17). **Bonded the
  Heart in ch22** — in his own office, on his knees at the plinth while Tess
  chose Ben — after watching four unarmed people take twelve armed
  professionals apart with the EMP working: **he mispriced the category.**
  Training cannot be jammed or bought, and the only unbuyable thing in the
  house was on the plinth. Walked out through his own stone wall with the
  Heart in his chest; razed a line northeast to Main Street; twenty feet
  (ch23), twenty-three (ch24–26), forty-plus (ch27–28). **Cut the Heart and
  seeded the four Tanks with its fragments himself, as bait to be broken open
  by whoever proved strong enough; the Go Squad broke them and fed him** (ch27:
  "Thank you. I was wondering how to reclaim those fragments"). **Killed by a
  CADENS cruise missile (ch28: "Confirmed. Kain is dead.")**; the body
  collapsed into a point above the crater, the point became a singularity,
  and **Ahdia burned it out** (ch29). **Alive on television the next morning**
  (ch30): "I was nowhere near downtown," a lookalike, "an attempt by criminal
  elements to impersonate me and destabilize my campaign," "this terrorist
  attack." Mansion insured and already rebuilding; campaign "rolling right
  along"; polling "would be good." **The epilogue: the body that fought was
  Forty-seven.** A white corridor four unrecorded levels under an unnamed
  building (the ch17 vault was four levels under the tower, door labelled
  CLIMATE ARCHIVE — the page does not say it is the same building); a tank
  room, rows of bodies "with chin down and hands open" — "A boy of nine. A
  young man with hair. Himself at forty, at fifty, at the weight he carried
  now"; cylinder **Forty-seven** open and dry: "our best integration... The
  Tamois Heart had fully bonded. Years of work. Gone." "That's the point of
  redundancy." **"We have three more [Hearts] in storage. We can begin the
  bonding process within a week."** Kain's own words on the Seed: "The Seed
  was dormant, we made sure—" (cut off; unexplained). He has "a file on the
  girl... thin... cheap... a line through it as of yesterday afternoon." **"The
  plan was always to eliminate her once the Seed went dormant." / "Plans
  change."** His role, assigned: "Focus on the election. Win the presidency."
  Whether the Kain of ch17–22 was Forty-seven throughout, and whether the
  Kain in the tank room is the "original," **is not on the page. Do not
  resolve.**
- **The woman in the white coat (epilogue; "a woman's voice")** — appears
  at the end of a row without having arrived; white coat, no badge, "no age
  on her at all," proportions "a degree off in a direction he had long ago
  stopped trying to put a word to." **Unnamed.** Knows CADENS' readings
  ("According to the readings CADENS picked up... She transcended. Briefly.
  Made contact with higher-dimensional space. She saw the hallway"). Knows the
  codename: **"Agent Auerbach saw Bellatrix."** Knows the Seeds' provenance:
  "That's why they were scattered in the first place. To see what would
  happen. Who would find them. What they'd do with them." Speaks of
  **Bellatrix in the third person — "Bellatrix doesn't interfere. She
  observes. But she acknowledged Auerbach. That means something... the girl
  is more important than we thought."** Commands Kain ("That's your role. Let
  me worry about the girl"). **Do not identify her with the ch17
  Intermediary on the page** — the rhyme (a woman's voice, clinical, knows
  things she should not) is there and is UNRULED. Whether she IS Bellatrix is
  likewise not stated on the page (see collisions). **Even she does not know
  Firas survives** (log ch30).
- **Chief John Whitford** — got CADENS' existence and a VULNERABILITIES
  document from the Secretary of Defense over golf at Montclair. His fear is
  obsolescence. **Director-ruled 2026-09-02: a MINOR character in Book 1, an
  ONGOING THREAT in Book 2, and "he only figures in so much that he's depicted
  as corrupt."** His vanishing after ch17 is scope, not a dropped thread.
  **Tess never facing her father is Book 2's business.** The drives hold
  proof he is on Kain's payroll; Victor expects that proof to reach the PAC
  and stop there.
- **Dr. Jericho** — anthropologist, curated the museum sub-basement; abducted
  CH05, held six weeks, rescued ch22, worked by Ruth in ch23 (the threat that
  broke him: Kain waking up). Gave the prognosis (organic, a seed from
  something vast, irreversible, consumed not empowered, hours to twelve, sixty
  percent he completes, only another Temporalist can stop him). **Last seen
  strapped into the transport in ch23, bound for protective custody with all
  his research.** Not on the page after.
- **The Heart of Tamois / Tamois Heart** — fist-sized, crystalline, red to
  amber/gold. 4.7 billion years, Maghreb dig, worshipped by the Amazigh. Kain
  wanted to replicate, scale and distribute it (ch21). **Consumed at the
  singularity: "Whatever had been in the middle of it to burn was burned."**
  Three more exist in storage (epilogue).
- **THE TANKS — FIVE; four fought; four are dead** (bible §7h; ch27). Seven
  feet of torn CCPD uniform each, unaffected by the EMP, carrying Heart
  fragments. **Edgar** (bald, wet knuckles), **Ogden** (scar through the left
  eyebrow), **Philips** (thick neck; the hands on Ruth's throat), **Orlansky**
  (the young one, eyes too wide). Officers "with names and mortgages and
  wives who packed lunches" (Kain). Died as husks, "smaller than the man had
  been." **The fifth is the one from ch18–19** — around thirty, clean-shaven,
  a face nobody would remember, takes his helmet off, calls Ruth "Dr.
  Carter." **Alive, hospitalised or in custody, unstated; never returns in
  Book 1; nobody tells Ahdia.** Filed as promise `fifth-tank-survivor`,
  payoff unassigned; carries the forgettable-face signature that rhymes with
  the Kain clone.
- **The Intermediary (ch17)** — a woman's voice on a phone with no wire behind
  the wall. Third call in six months. Wants the Go Squad eliminated
  permanently in exchange for the Heart's activation protocols; says "his
  civilization" of Jericho's; dismisses CADENS ("CADENS observes. They do not
  enhance"); knows the real source of the team's abilities and refuses to say.
  **Never returns on the page. She promised to call again and did not.**
  Name, face, employer and species are unestablished. Presumed Book 2. Do not
  invent them and do not join her to the epilogue's woman.

---

## CHAPTER MAP (compressed; state changes bolded)

**The clock.** Bible §7d runs to "late September: ch17–23." Extend it as:
**night N** = the docks (ch18, 2100). **N+1** = the labs in the morning, the
gala and the mansion in the evening, the rampage, Ahdia's real waking at
about 2300 (twenty-six hours after 2100 N). **N+1 into N+2, one continuous
night** = ch24's street through ch29. **N+2** = the debrief, the living room,
the roof at sunset. **The epilogue** is after Kain's morning press conference;
its day is not pinned (see collisions). Warehouse → docks is six weeks; Ruth's
CADENS day is one day; FAERIS independence is three days old at ch20.

### CH01–CH11 — the author's own chapters

**CH01** (Firas; night A, his 64th engagement) — solo patrol, the alley rescue
at Renata's, dinner plans for the next night with Ruth and Ahdia. Ends on the
rally cry exchanged over the radio and "Thanks, Ruth" — the couple, the
ritual, and the last ordinary night.

**CH02** (the children; Montana, over fifteen years back) — Faraz's
chosen-one / black-hole lore; Naima's lesson: *"You don't always have to fix
things for other people"*; "you are already trapped in one event horizon, my
queen." **Ahdia eight, Firas six.** Ends on "Mom and dad. They aren't here." —
the disappearance lands as a child's sentence.

**CH03** (Ahdia; night B, ~Aug 12) — the dinner Firas misses; the parents
"over fifteen years ago"; Ahdia finds him shotgunned; **CR-7's first human
use.** Ends on Ruth: "He's alive... Ask me the rest in the morning."

**CH04** (Ahdia; day C) — Ruth's account of the team: the codenames, the
rules, no guns, four years. Ends on Ruth's "I feel really bad for them" — the
team's competence stated before we see it.

**CH05** (Ahdia) — Firas's account: the museum abduction, the docks, Kain, the
four-dimensional object in the TRIOMF crate; Ruth needs a real lab. Ahdia
decides Firas is faking. Ends on "We'll see," and the walk to the warehouse.

**CH06** (Ahdia; night C, Aug 14) — Ahdia and Ruth in the warehouse; the crate.
Ends on "Put your hands up!"

**CH07** (Ahdia/Ruth) — **Ahdia shot in the chest**; Kain beats Ruth; the
team arrives; Kain on the catwalk with the RPG. Ends on the trigger already
pulled.

**CH08** (Ruth) — **everyone impossibly outside and unhurt, Kain and his
detail professionally bound by nobody**; the fire; **the team believes Ahdia
died in it.** Director-ruled: the event has no duration, so the chapter is as
long as the gap ("They literally transported"). Ends on "At Ahdia's pyre."

**CH09** (the team; +2 nights) — the news cycle, Chief Whitford, the Carl
Tucker framing; **Ruth reaching back to the training to explain the warehouse
and finding "the training had no answer in it"** (the paragraph is now two
sentences; ch22 pays the rest); the traffic stop begins. Ends on a child's cry
over the radio.

**CH10** (the team) — Gloom Girl breaks stand-down; the impossible police
response; "Elvis" scatter; **Gloom Girl's swan dive off the bridge**, finger
raised. Ends on Ruth's "No!" through binoculars.

**CH11** (the team) — Battlea shot into her armor; **every police weapon
jams, Sable kicks a man a block, Battlea charges two through a ledge** —
powers, while Ahdia is "dead." Ends on Sable: "I'm a freakin' superhero!"

### CH12–CH21 — the rebuild

**CH12** (Ahdia, hidden; the Academy, the morning after the ambush) — Ben
can't repeat the jump; Firas floats **disbanding** and is voted down; who
leaked; **all five give up their real names**; **Tess confesses the accounts
and #GoSquad**; **Ruth names Whitford as Tess's father.** Firas says Ahdia
"didn't make it," then "already dead inside," and the room takes him apart.
**Ahdia is behind the foam vault, hears all of it, freezes the room — and a
FAERIS drone translocates her out.** Ends on the corner by the vault staying
empty — the room never knows she was there.

**CH13** (Ahdia; the roof, then the facility) — **Bourn and Mack introduce
CADENS.** Playback of the warehouse: 3.7% survival, the bonding, 47 minutes
subjective at 0.00 real, **Aug 14 timestamped**; she bound Kain herself.
Seven Temporalists in three millennia. **They have watched her since before
the warehouse.** Montana as bait. Ends on "The police ambush. That's when we
knew for certain." — the reveal cut mid-sentence.

**CH14a** (Ahdia; flashback, the night of Aug 14) — the run home inside an
unconscious freeze; dead elevators; **the heart trick and what it cost**; the
terror over sleeping Firas; **"please" releases the freeze.** Emotion pulls
the trigger, calm releases it. Ends on her in the dark kitchen staring at the
mug — the power as a thing that could kill him for saying good morning.

**CH14b** (Ahdia; the two training days, framed by the conference room) — the
pillow, **force amplification**; the homes of Ruth, Tess, Victor (the
scratched-out wedding photograph, untouched) and Leah; **the bridge catch and
selective dilation**; three simultaneous ambushes. **23% of reserves in one
night. Permanent depletion. Eighteen months baseline.** Ends on "I'm in... But
I have conditions."

**CH15** (Ahdia; the facility, one day) — **the condition: protect the lie.**
**Ryu becomes her handler.** Med bay: the Seed's threads. Armory: the kit.
Training room: shrinking the field buys "another year, maybe more."
**Codename AUERBACH.** Ends on "Small victories" and sleep — doing was new.

**CH16** (Ahdia; weeks in the bunker → late September) — **the trigger table
chosen and locked.** The Old Caledonia community-center raid: thirty seconds,
five cops zip-tied. **Nosebleeds, hemoglobin drop, microsecond aging.** Ryu:
"You bought yourself a year... This week you spent it on them." Tess's cut
trends; **people with titles run it frame by frame.** Ends on the dread
keeping its seat through the celebration.

**CH17** (Kain; his tower, an evening before the docks) — fifteen viewings of
a smeared climb. The Ruth Carter file; **acquire her research after she is
neutralized.** **Whitford brings CADENS, Overseer, VULNERABILITIES**; six
weeks of drone signatures. **Jericho, the vault, the Heart, forty-eight
hours.** **The Intermediary calls**: elimination for activation protocols.
Ends on "Problematic... an understatement" — the fifteenth viewing.

**CH18** (Ruth; night N, 2100, the docks) — Ben's precinct tip; the lot fills
with fifteen units in eight seconds. Smoke works — **then the EMP kills the
gear and the powers.** **The Tank breaks Victor's arm, puts Leah through a
pallet, lifts Ben by the throat.** Ruth draws him off, is cornered at the
water; he knows her name and Kain's price. Ends on "The fist came back. The
water waited."

**CH19** (Ruth; night N → ~0200 N+1) — **Ahdia freezes the punch**, moves Ruth
ten feet, puts the Tank through a container on release (**the fifth; alive**).
**She collapses and stops breathing.** **Ruth reasons the whole thing out on
the dock and says it aloud.** Ryu extracts them. Telomere integrity 18%,
tonight cost 4%. **Ruth takes the deal** and texts "Had to split off. I'm
clear. Meet at Academy." "Worth it." is Ahdia's line. Ends on Ruth getting
nothing back from her own reflection over the girl the city buried.

**CH20** (Ruth; N+1 morning, the labs; the last paragraph at Ahdia's bed) —
cellular stress, not a temporal problem; **CR-7 Temporal Variant in four
hours.** **FAERIS enhancing alone at 10%**; the drone that turns to watch.
"Useful versus worthy." **Dose one.** "Every three weeks to start. Monthly
once she stabilizes." "Don't tell him. Please. Not yet." Ends on Ahdia
watching the ceiling, waiting to be told which way she is turning.

**CH21** (Tess; N+1, the Academy, then the gala on feeds) — the video: powers
gone, Gale dark, only her translocation works and it is slow and sickening.
Firas plans the rescue and cannot walk it. **"Sophie Clement's name on that
list had cost a donation to Kain's PAC, and Firas had signed it out of his
sister's estate."** Leah in the red dress with the slit; Ben and Victor as
catering; Tess two blocks out. The vault stays shut; **Jericho is upstairs.**
Leah puts Kain on the carpet; **Ben copies the drives (proof the chief is on
the payroll)**; **Kain shows the Heart and means to replicate and distribute
it.** The floor plate. Ends on Tess watching every screen stop moving.

### CH22 — REBUILT (Tess POV; staging A; three movements)

**Timing:** N+1, evening ("tonight"; "four years of asking does not switch
off in a day"); the first cold snap of the year. **POV: Tess**, on the
twelve-camera grid two blocks east for movements 1–2, in the room for 3.

**M1 — smoke.** "Open fire!" reaches her twice, Ben's apron cam and the house
system. Twelve weapons at the near door, one at the balcony window. **Leah
wheels the zip-tied Kain into the middle of the floor as a nine-figure
obstruction** — "He sat at the center of all of them now." Ben: "Gloom Girl.
We're pinned. Need an exit." Her exit is bad: four trips minimum, slower each
time. Copy bar at thirty seconds. Victor tips the champagne bucket; goggles;
smoke. **Leah's heels come off as ordnance**; she fights barefoot in the gown.
Battlea takes the chair apart for two armrests; the second goes over her
shoulder into a hand already open for it. The team makes no sound — four years
of "do it again, softer." **Ben's forearm as a rail; Leah's derby whip across
the office "at a speed her own legs could not have produced"** — "She had
never once seen it done in a gown." Ben and Victor back to back, the shape
they have a name for. Tess is proud and it has a cold under it: they are
holding without her, without Gale, without whatever did this for them. Kain
in the smoke, chin up, "his face did what her father's face did at a car
dealership. He thought he was watching equipment... he would find out who,
and then he would buy two."

**M2 — the window, and they keep winning.** The balcony man finds a firing
position; Ben runs the paneling and puts a guard through the west glass —
a four-foot hole; the smoke pours out; "They had just broken the window it
lived behind." **"And they kept winning."** Lit room, rifles, three people
with two chair arms: the bookcase, the drape, the throw that is delivery,
Leah over the desk from six feet in the air. **"Somebody went hard into the
plinth. The case on top jumped on its base and came down starred across one
corner"** — Kain's route needs nobody to unlock anything. Every loose rifle
goes out the hole. The guards drift to the walls. "Firas built this... on the
one night he could not get up the stairs." **Kain stops moving his head and
looks at the plinth** — Tess reads it as inventory and goes back to the copy
bar: eleven seconds.

**M3 — the fresh ones, the lights, Tess in.** Clear-eyed reinforcements
through both doors. Victor takes a forehead; Leah takes a hostage and loses
both hands to it; "Gale?" — nothing; Ben remembers nobody has known where
Ruth is since the water. A knife on Ben; Victor cornered at the plinth with
a dozen barrels, hands out, three steps into the open. **A guard saws Kain's
ties with his eyes on the fight "and went back to the line without once
having looked at the man's face. Kain did not get up. He put his freed hands
flat on his knees and went on looking at the plinth."** Then the lights die.
Tess left the crate two minutes earlier: jump 1 structure roof → boxwood
(bad landing, stomach two blocks behind); 2 kitchen door; 3 service stair;
4 the electrical room window; 5 inside it — every breaker; 6 the linen shelf;
**7 Jericho to a loading dock three blocks east**, glasses folded into his
shirt; 8 the office crown molding, goggles on, the room a route. **"There
were two things down there and one second to spend on them"** — the knife on
Ben, and a man on his hands and knees at the plinth with his face turned up
into the light. **"She picked Ben."** 9 Ben out from under the knife; 10 the
chandelier onto the doorway men; 11 Battlea off the wall onto the desk.
Emergency circuit: **"The chair by the desk lay on its side and empty, the
ties cut through, and on the plinth the light had changed color while she was
not watching it."** (The fight ends verbatim on that sentence.) "Hands up!"
again; she takes Ben's collar and Leah's — "Now!" — through the hole; back for
Victor "doing the honest math of a man with nothing left in his hands";
"Trust me"; four more jumps bend the fall into the fountain.

**The alley, three blocks east.** "What the hell just happened?" / "Gloom Girl
happened." / Victor: "That was insane." / **Tess: "That was fun."** / Leah
wrings out the dress and laughs. **Firas arrives on foot**, a hand over his
ribs — "Walking was the only way any of them ever went." Jericho "at the
extraction point... Unconscious but breathing. Got all his research too." The
bathrobe neighbour; Leah's photograph; "We see you. All of us." Then the light
behind them, red and gold, and Tess knows it in her shins: **space folding,
run backward.** **Kain walks out through the front wall of his own house**,
the Heart sunk in his chest, "eyes flickered rapidly between one state and
another," checks the sky like weather, finds them three blocks off, smiles,
walks through an apartment building. "We need to call someone." / "The cops
who work for him?" Tess's phone: unknown number; **"No better place than
here," Ruth said in her ear.** Gloom Girl was a name she picked at nineteen;
**she decides she wants a different one.** "Get somewhere safe. I'm sending
help." The bus-sized aircraft decloaks forty feet up; a ramp; **Ruth in full
tactical gear nobody has seen.** Ends on "Need a ride?" — the help arriving
as Ruth, in someone else's uniform.

**Ch22 pays:** ch9's training paragraph (the room is its spec); ch12's derby
jammer and ch7's "fleshy brick wall" (the whip); ch21's tactical slit (the
heels); ch16's film vocabulary (staging A); and it shows "each of them opening
the next one's line" without powers before ch27 shows it with them. **Kain's
integration is now on the page as decision (the look) separated from
opportunity (the sawn ties), which is what makes it desperation.** Ch27's "He
had priced that before he ever put it in his chest" stays as the lie he tells
himself.

### CH23–CH25 — as before, with the twenty-six hours and the palmed dose

**CH23** (Ruth; N+1 night — the transport, the extraction point, the briefing
room; the Main Street rampage is one hour old at the end; Ruth "awake past
thirty hours"). **Firas does not board** — takes the drives from Ben's fist
and turns east on foot; "He asked nothing." Ruth tells the team the truth
with **one thing withheld — the name**: never theirs; distributed through
drone networks; someone dying to keep them safe; FAERIS; CADENS by full name;
Kain integrated and transforming; "A monster with a grudge." HAZARD reports
him razing northeast. **Ruth works Jericho** (the threat: Kain waking up) and
gets the prognosis: organic, irreversible, consumed, hours to twelve, sixty
percent he completes, **only another Temporalist**. Ben gets there: "The
person who's been enhancing us." Victor's three questions — "You know them" /
"they asked you not to" / "Even though we have a right to know" — and **Ruth
says nothing**. Leah: "How long do they have?" — **"Weeks. Maybe less."** Ben:
"We can't ask someone to die for us." Ruth: **"It's not your choice. It's
theirs."** Bourn on the pad: "Ryu says she's awake... Saw the feeds from the
mansion... already asking when she can deploy" — **stale by hours (§7f)**;
Ruth hears the timestamp. Ryu's estimate: days, a week if lucky. The briefing
room: thirty-one crises, the tracking board, Victor's file with his legal
name, four cases of gear, the offer — "Can we think about it?" "Of course."
Amber light: **Kain at twenty feet on Main Street with four Tanks.** Mack:
"Override that. Deploy all available units. NOW." Seven minutes to muster,
eleven to the site; the team takes the cases and goes without clearance;
Bourn: "You'll die out there." Tess: "Probably." Ruth: "I'm going with them."
Bourn, low: "Ahdia—" / "Ryu can handle it." Ends on **Bourn alone in her
briefing room** watching five people with no powers run at a god.

**CH24** (Ahdia; the dream, then ~2300 N+1 — twenty-six hours after the docks;
then Main Street). The rain going up; **"You only ever pull... What if you
pushed?"**; the stacked frozen moments; **the hallway of blue doors (left,
always opened) and red doors (right, never)**; herself at eight on the
Montana log: "You keep looking back. What if you looked forward instead?" /
"I'm scared." / "Good. That means you're moving." A red door open, warm.
**Something too big for the hallway comes down it — old, curious, neither
hostile nor kind — looks at her and passes.** She reaches for the red door;
**a second voice, cold and final, "not the Seed": "Wake up."** She surfaces:
IV torn, no memory of it. **"You've been out for twenty-six hours."** Ruth
"left. With the others." The feed: Kain, "growing for the past hour." "They
don't have powers." / "I know." / "They're going to die." Bourn: eight doses,
three weeks each, six months. "I don't have six months." Ryu: **"You've been
unconscious for twenty-six hours."** Bourn came to say no and says **"We're
out of time."** Eight autoinjectors in foam. **The Seed burns RED for the first
time: blue is pull, red is push.** Seven doses through self-acceleration —
RATIO = 1:2000, TOO FAST = CELLS BURN, TRY 1:1500, SLOW DOWN unread — **"The
eighth went to her thigh, same press, same sound, and nothing went in. Her
fist took it under the gown."** Fifteen seconds on the wall clock. Ryu:
"First few integrated. Last ones barely worked. Maybe thirty percent." "It
has to be." She reaches for the Seed and is gone; the cabinet's foam stripped
bare; Ryu and Bourn turn to the feeds. Main Street: the drone's light, space
creasing, **Ahdia barefoot in the gown, the Seed blue again; Kain frozen
mid-strike at twenty-three feet with two teenagers alive in his fist**; Edgar
with Victor, Ogden an inch from Leah, Philips and Orlansky mid-charge.
Civilians run; the team does not. Ends on Ruth whispering **"Ahdia"** through a
bruised throat in front of four people who grieved that name for somebody
else's sake.

**CH25** (Ruth; the same minute). Ahdia sends the drone away — **it settles on
Tess's shoulder and stays**; Tess goes rigid. **"Hi, guys, first-time caller,
long-time fan, I'm Ahdia, Firas's big sister."** Firas is east of here with
no idea, and Ruth chose that. Leah: "Are we dead?" Victor: tropical beach.
Ruth crosses and reads the patient. **"You took the rest of the treatment,
didn't you?" / "Yeah, what gave it away?"** — Ruth believes all eight went in.
**"I'm not actually freezing Marky Mark and the Funky Bunch over there. I'm
doing the other thing."** — she is accelerating everyone else, worked out
fifteen minutes ago; she hitched a ride on a drone from "CADENS HQ." Tess
picks the word out of the air: **"You knew about her? This whole time? You've
been working with CADENS. You knew. You've been lying."** Victor: "How long?"
Ahdia: **"two weeks ago? Maybe three? Time's been weird"** — **one day; Ruth
knows and lets it lie, because one day was enough.** Ahdia's confession in
two halves (she loses the thread at "but then it became—"): she asked Ruth to
keep it; she did not think she deserved powers when they had none; "guts and
gear and giving a damn"; **"even without me, you guys are, well . . .
super."** Ben: **"We trusted you."** — the floor tilts under Ruth. Leah: "Can
we? Because it seems like you've been keeping a lot of secrets." Nobody is
asking Ahdia anything; Ruth feels them stop hearing her as the voice they went
through doors on. Victor: "We don't have time for this!" Ahdia, red teeth: "I
can hold this. But not forever." All four turn to Ruth — "a liar with a plan
beat four honest people without one." **The stillness is not a wall but a
window.** Tess comes last and it costs her. Ends on **"Then let's run."**

### CH26–CH30 + EPILOGUE — new

**CH26** (Ahdia; Main Street, continuous from ch25; her head — codenames
throughout). Barefoot in the gown, blood down her arm, the voiceover running
("The girl in the gown was in serious trouble"). Kain at twenty-three feet,
translucent, bones moving, "left 'human' behind somewhere around the
fifteen-foot mark." The four Tanks named by feature — Ryu's tablet faces made
flesh. Banter: "hospital chic," pad thai Tuesdays, "You're no hero." / **"No.
I'm really, really not."** — "the truest thing she had said out loud in
weeks," and it goes by him. She reads the roofs: Gloom Girl on the bank
cornice, Battlea behind the bus, Night Knight on the pharmacy fire escape with
two canisters, Crimson Sable in the alley mouth with rebar, **Ruth at the
corner talking into her collar "and all four of them moved when she spoke,
and not one of them looked at her while they did it"** — the ch25 trust debt
registered from outside, a beat, not a scene. **"You're about to have a
really bad fifteen seconds."** Kain moves two fingers; the four charge; **she
picks up the anger like dropped keys and the street stops** (pull). She walks
in among them and moves Ogden's forearm a few degrees, Edgar's hip, leaves
Orlansky ("already going to miss"), barely touches Philips; lets go — Looney
Tunes: four men collide "like a filing cabinet coming off a truck." Kain's
fist comes down; **she stops the street again**, walks fifteen feet, folds her
arms to hide her hands, lets go; his arm goes into the pavement to the wrist.
Philips draws; **she takes the round out of his pistol inside the freeze**,
squares his grip up "like she was fixing a kid's hold on a bat," steps clear:
click, click. **Then her body quits** — grey from the edges, drowning standing
up. **Kain does not swing: he has learned.** He folds down, closes a hand
around her middle, lifts and squeezes; **a rib lets go.** The cold is "a long
way off with the lights out." **Headlights the wrong way up Main Street: a
gray sedan with a front-quarter dent she knows.** "You... had... enough?" The
sedan jumps broken asphalt into him. **She PUSHES** — "red, going forward,
expensive past discussing... never inside a fist with her ribs coming apart,
and never with somebody else to drag along" — and takes herself, the car and
the driver out ahead of the world: steam standing, glass hanging, Kain's face
half through a thought. She works out of the loosened fist and falls. The
driver: **"It was her brother. It was Firas. Of course it was him. He
wouldn't miss a kaiju even if he were dying in a hospital bed."** She pulls
him out through the window into stopped time; he looks at a world where
nothing drips, then at her. **The voiceover cuts out. "Hey, Ahdia." / "Hey,
little bro."** — first words between them since he was shot. Her pet peeve
about family and weight; his "I'm sorry. This... is all because of me. I
shouldn't have come to your place." / **"I know."** She does not tell him it
is okay: what he said in that room "went through her like rounds through
drywall and confirmed the whole case she had been building against herself
since she was a kid. And he had driven his car at a kaiju anyway." **"We need
to talk about it. Later. When we're with more polite company." / "Later."**
He strips to the armor he wore under his clothes ("Habit... the guy who packs
a go-bag"); "You can't fight in a hospital gown... I'm benched. You're not."
She slams it onto the frozen street — **"She was already wearing it"** — too
big in the shoulders, a plate over the broken rib, feet still bare; Firas
starts a question and does not ask it. "The team?" / **"Positioned. Rooftops.
Fire escapes. Ruth's coordinating. Waiting for your signal."** He backs to
the sandwich-place doorway in a t-shirt. She walks to the middle of the
intersection in armor built for somebody else and **lets the whole street
go**; Kain finishes his sentence — "Let's give them an opening." — and she
puts everything she has into her lungs: **"No better place than here!"** Ends
on the second half screamed back off the roofs and **the Go Squad coming down
off the buildings, all of them, yelling** — the team joining her fight inside
her field, on her call.

**CH27** (Kain; the same seconds). "No better time than now!" Five people at
something twenty-three feet tall "priced out as suicide." The girl in black
armor he had not seen her put on — "Somewhere in the noise she had acquired a
costume. He set it down without turning it over." **The drop stops behaving
like a drop — and this time he can see where it is coming from: the girl
swaying, paying openly.** Battlea takes Ogden at the hip; Crimson Sable lands
on Philips with the rebar and the asphalt breaks in a ring; Night Knight
corrects mid-strike and catches Edgar centre mass; Nightingale goes through
Orlansky's guard "as though it were a door somebody had left unlatched."
**Gloom Girl hits nobody: she drops onto the sidewalk beside "a man in a
t-shirt," raises her middle finger at the intersection, and takes them both
out of it.** "Four down. Five standing in a ring around the girl in the
middle, and the girl had not thrown a punch." "What are you?" — "she had
nothing left to answer with." Second wave: Ogden takes rebar to the temple;
Philips goes under a sweep and Gloom Girl arrives on him out of clear air
(**she came back**); Edgar into Night Knight's restraint with Sable following
in, "the medic left standing behind them"; **Orlansky last — all five
converge, "each of them opening the next one's line."** "They were taking
people down rather than killing them, and he found the care faintly
sentimental." Then: **the light leaves Ogden "like marrow leaves a bone... and
what lay there afterward was smaller than the man had been"**; it crosses to
Kain like filings to a magnet; Philips, Edgar, Orlansky; **"He had cut the
Heart and distributed the fragments himself. He had made four weapons out of
four men and put them in the street to be broken open by whoever proved strong
enough... The Heart came back together behind his sternum, whole."**
Nightingale sees it first — **"NO! STOP!... You're feeding him!"** Someone in
the ring, low: **"We killed them."** — he cannot tell who and does not care
(ch28 gives it to Tess). The husks: officers "with names and mortgages and
wives who packed lunches." "Grief is a luxury good, and they were buying it in
the worst hour of their lives." **"Thank you. I was wondering how to reclaim
those fragments."** Twenty-five, twenty-eight, thirty-one, forty feet; skin
clear enough to read by; the Heart taking its fee. "He had priced that before
he ever put it in his chest. He had decided it was worth the fee." (The lie
he tells himself — log.) Ends on **"She had saved all of them, and she had fed
him doing it."** — the win converted to the loss in one sentence, from the
enemy's head. Accounting metaphors throughout are Kain's voice, exempt.

**CH28** (Ahdia; continuous; the contact drift begins). On one knee, the suit
hanging off her. The four husks named. **"Somebody in the ring had said we
killed them, and Ahdia had been standing in the middle of that ring, close
enough to know. It was Gloom Girl. Gloom Girl had translocated out with Firas
before any of this, and the sentence was still lying in the street without
her."** ("Before any of this" = before the CADENS engagement, log 2026-09-01;
the ring was five.) Kain at forty feet and growing, bones cracking like
gunshots. Ruth: "We have to move." The fist. **She reaches for the Seed and
nothing comes** — "She had spent it getting them here, on surviving the
impact, on changing her clothes in a blink." **Something takes her in the hip
— Leah, elbow in her ribs, already gone: LEAH from here on.** "Scatter! Don't
let him track patterns!" Leah draws him; Crimson Sable's two-handed swing at
the ankle **bounces**; "It's not working!" — grief in it. **The backhand,
almost courteous, puts him through the pharmacy's second floor and brick
comes down after him, "and Victor did not move": VICTOR from here on.** Leah
turns the wrong way, straight across Kain's front, rolls out of the fist's
landing and gets to him: "I'm okay." Night Knight tackles all three out of the
radius. **"Futile. You've already lost. You fed me. Made me whole. Now watch
what that bought you."** Nobody answers. She reaches again — "cold and thin, a
flicker" — and the intersection does not slow. **Then the sky screams**: the
pressure, then the thing crossing above the rooftops, into Kain's chest; a
small sun; every window for three blocks; forty feet of him hits the street.
Twenty operators in black kit take angles on a dead thing. **Mack** at the lip,
two fingers to his ear: "Overseer... Target is down." Bourn's voice, affect
sanded off: "Confirmed kill?" **"Confirmed. Kain is dead."** Unasked: "Overseer
wanted authorization before engaging. Pentagon wanted assurances. SecDef
wanted contingencies. We stopped waiting... Some things are more important
than careers, ma'am." Ahdia sits in the road: **"Dead. They'd won."** A medic;
Ruth: "I'm a doctor. ER. I've got this." "Where's Firas? Where's Gloom Girl?"
— operative: **"Safe. Translocated out before engagement. We tracked them
to—"** The ground moves, spaced like a heartbeat. **The body folds toward the
Heart with nothing alive in it**: forty, thirty, twenty (breath visible),
fifteen, ten, five — **a point two feet above the crater floor, "no bigger than
a basketball, so dense the air bent going past it."** "Singularity! Everyone
out! NOW!" Debris first — the rebar where Victor dropped it. The pull on her
body; Ruth hauling and losing an inch at a time. **The bank leaning**, windows
going out a row at a time, a sound lower than a scream that does not stop.
Ends on **"everyone still standing in it was underneath."** — the second
threat replaces the first inside a paragraph of the win.

**CH29** (Ahdia; continuous; the human chain — BEN and TESS become names
inside it). The pull takes her hair, her suit, the glass off the road, a
parking sign. Mack's twenty give ground backward in order. Ruth has her arm.
She sees all of them: Leah with Victor half off the pavement, Night Knight
down the pharmacy front with an elbow locked to his ribs, **Gloom Girl by the
bus, leaning back against the drag** (she and Firas are back; the return is
unstaged — ruled coherent: she can teleport). **"Go... Get them out! All of
them!"** — she shoves Ruth down into the glass with nothing kind in it and
walks at the crater. "Stop her!" Ruth gets four strides and is pinned at a
parking meter; Leah at a light pole; to cross the last ground either would
have had to let go of what she was holding. "AHDIA!" "Don't you DARE do
this!" Every foot is work; at ten feet the ground spiderwebs and she plants.
**Right hand out at the point: the red — "it was permission... Whatever it
had left to burn, it could burn all of it in one breath."** Not enough — it
would take the bank next. **Left hand back at the city: the blue — "the pull
she had used her whole life, running as a shell around the acceleration,
holding the edge of the thing still while the inside of it raced." Both
directions at once, through one body, in opposite hands.** "The Seed could
do it... she was only the wire it came through, and the wire was not rated
for this." **Her skin opens — fissures up both forearms and across her chest;
inside is not blood but white, with structure, going down further than a
body goes.** She screams and cannot feel it. **Her vision comes apart into
panes and at the edge of every pane is a corridor with doors; she shuts her
eyes and refuses it.** **Then hands over her hands — Firas: "I'm not losing
you again!"** No Seed, no field, skin and everything he had; **the same cracks
come up his forearms.** "Let go!" / "No." / **"We do this together."** — decided
before he touched her, never reopened. **Her left hand goes to her hip, to the
faked dose — "It was for him. It had always been for him." She cannot turn her
hand over: the fingers are going, the injector in a hand that is in more
places than one.** "Firas—" **Then the street is gone.** The corridor is all
of it, doors running past where seeing stops, each lit a different colour;
**no hands — "light in the shape of where she had been," structure and depth
"that had nothing to do with meat," older versions of her stacked out of
order like frames of film.** **The doors are lives**: the apartment she never
left, forty years of it; the warehouse floor and her body cooling; "close,
standing open a crack: Firas alive, and no Ahdia anywhere in it at all."
**Something turns its attention on her** — at the far end and directly in
front of her, both true; "It had never been human. It had never been anything
that had to work its way up to being what it was." **Recognition in both
directions, no words. She has every question since the warehouse. "It
acknowledged her. Then it took its attention elsewhere, and whether that was
dismissal or whether it was permission she could not tell."** **UNNAMED. No
speculation in the narration.** **"Then something took hold of her and put her
back"** — violent, torn open and reassembled in one instant, "three directions
and one clock," a body that hurts and weighs and has edges. Firas inches from
her face. **A sharp pain low in her abdomen: the autoinjector against her,
his thumb on the plunger, "and there was nothing in his face that was
fighting anything."** **The chain: Ruth locked on her arm; Victor around Ruth's
waist; Leah holding Victor; Ben anchoring Leah, boots braced; Tess at the end
with her arms around Ben and her legs jammed against the bus.** "They had come
for her, all of them, and nobody had asked her first." "NO!" — she tries to
tear his wrist off the injector and stand; the chain lets her do neither.
**"Oh hey," he said. "I knew you were in there somewhere."** "Firas, please—"
The cracks up his neck and jaw, light through them, more of it and less of
him. **"Nothing dragged him. He moved, and the space he was standing in
shifted over and took him along with it." He keeps his eyes on her; at the
edge he looks back once; "went down into a space smaller than a fist and was
absorbed. Gone."** The point pulses brighter than the street can stand and is
not there: **"The red had finished what it was doing. Whatever had been in the
middle of it to burn was burned."** Air rushes in; everything falls and
stops; **the bank groans and holds**; no sound. The chain goes down in a heap;
Ruth never let go and drags her into the middle of it; a hand on the back of
her neck. No body, no mark but the scorch. Ends on **"She was alive because he
decided she would be. / She never got to say goodbye."** — death, read on
the page, in her terms. **Zero transcendence language anywhere in the
chapter; Firas dissolves believing he is dead and that it worked; Ahdia
comes back believing she was rescued from dying.**

**CH30** (six sections, five POVs; N+2 and after; 176 spans).

*§1 — Ahdia; the command-centre glass, then Bourn's office; N+2 afternoon
("Twelve hours of debriefing had worn the Dr. off his name").* "You holding
up?" / "I'm standing." / "That counts for something." **The team: "Checked
out clean. No temporal anomalies, no residual Seed energy, no cellular
degradation... Victor's arm is in a sling but that's from the pull."** Bourn:
"I'm very sorry for your loss." / "Sure. Thanks." — flat, and left flat.
"Impressively, you did it on your own." / **"I had the Go Squad. They formed
the chain. Pulled me back. They almost died doing it."** Ahdia heads off the
idea: "It probably shouldn't give you ideas... Next time, they die." How did
she know the acceleration wouldn't tear them apart — **"I guessed. The Seed
was channeling through me, not them. They were pulling on flesh and bone, not
exotic energy."** "And your brother—" / **"Don't. Don't analyze that."** **The
badge; declined**: "I can't use my powers anymore. The Seed's dormant. Maybe
permanently." / "We don't value that nearly as much as we value what you bring
to the table regardless." She sets it back down. "The couch has been booty
calling me." "Keep CADENS under your hat." / "It's not like you won't have
FAERIS tracking me anyway." / **"We have no reason to monitor you anymore, Ms.
Bacchus."** Handshake, dry and short. **"How close did you come to draining all
of your life force yesterday?"** — behind her eyes the corridor and the thing
that turned its attention elsewhere; "It would go into a folder with a review
date and it would belong to them"; **she smiles the cashier smile and goes.**
Intercom: "Please send in Dr. Ryu." Function of the section's end: the one
person who could name what happened to her chooses not to hand it over.

*§2 — Ruth; a living room with a fireplace nobody uses and an elevator; the
television on "a day and a half."* Carl Tucker on the evacuation ("a supposed
critical gas leak," "The National Guard gets called in?"); Ruth kills the
sound. The gear is theirs again: ham radios with tape on the battery doors,
line, washed black cloth. **"The armored cases had gone back down the elevator
that morning with two men who signed for them."** Victor: "I wish they let us
keep the suits." / Leah: "Lot of good it did you." / "My arm might have been
taken clean off without it!" **Ruth: "We don't need them because we're done.
The Go Squad. It's all over."** Ben: "We have the proof to expose the cops."
**Victor: "my consumer advocacy group has filed a lawsuit against the money we
paid to the Kain PAC... Ahdia may not get her money back but neither will
Kain. That money will get frozen."** Ruth: **"Kain is no worse off than
before... already rebuilding his mansion. His campaign is just rolling right
along."** Ben: exposing the chief has to connect to him. **Victor: "Wrong.
Ruth's right. It'll connect to the PAC. His hands will be clean."** Tess: "And
what about Ahdia?" **Ruth: "We haven't seen her since yesterday. Since
downtown. Where is she? She just sends me access to her penthouse and bank
account and doesn't make contact?... we're not the Go Squad without Firas. He
started all this. It was always his."** Leah: "You've been holding us
together... You organized the chain. You've been carrying us." Then: "this
world doesn't need us. We're just a bunch of crazies... And we just lost—" —
the name goes out from under her; she stands in it — **"We just lost Firas.
Yesterday... That's as much of a price I'm willing to pay to keep doing this.
I can't lose any of you, too."** **"You won't," Ahdia said.** — in the doorway,
hands in her coat pockets, **"a duffel bag on the floor at her feet, packed
and zipped, sitting there like something that intended to stay."** Function:
the resignation answered by an arrival, not an argument.

*§3 — Ryu; Bourn's office, ~forty-seven minutes after the authorization
arrived.* Not admonished for letting Auerbach leave early. **"She lied to us.
The eighth treatment. The one she told you she'd completed before leaving the
facility." / He finished it for her: "She didn't take it."** "Medical analysis
confirms she left at approximately one-third cellular recovery. Far below
combat readiness, let alone channeling opposing temporal forces through her
body... a Terminus-level event critically compromised. It's a miracle she's
alive." Ryu remembers her saying the eighth was in, sleeve already down.
"Tactically unsound." / **"It was reckless. And effective."** Second issue —
**Kain's press conference "this morning"**: nowhere near downtown, criminal
elements impersonating him. "He's spinning it. Claims the entity at the
singularity was a lookalike. Some kind of bioweapon or cataclysm construct."
Ryu: "We have footage. Thermal signatures. Energy readings from the Tamois
Heart in his chest." / "And he has lawyers." / **"We can't touch him. Not
officially."** The authorization: requested six hours before Auerbach went
downtown; received **forty-seven minutes ago, fourteen hours after the event
concluded**, with thanks for "patience and restraint." "They wanted us
hamstrung." / "They wanted plausible deniability." Either way Kain walks. "We
document everything. We build the file. And we wait." — for Kain's mistake,
for the authorization to mean something, "for whoever's pulling strings above
us." **"In the meantime, we do our job. Monitor cataclysm activity. Track the
Seed-bearers. And hope that next time, a depressed girl with time powers and
a death wish isn't our only line of defense."** Function: CADENS' knowledge
and impotence stated in the same breath; the reader learns the dose was
found out and that nobody will say so to her.

*§4 — Ruth; the living room, continuous from §2.* Everyone talks at once
(Victor: how did she get up here; Tess: has she eaten). **Ahdia's speech**:
"You guys saved my life yesterday. Downtown. The singularity. When I was
channeling those opposing forces, **when I went . . . somewhere else . . . you
pulled me back. Formed that chain and hauled me out of a collapsing
dimension.**" (The only words the team ever gets about where she went.) "Even
without me helping you in the background, you guys are real, genuine heroes.
You inspired me to get off the couch... At first, I thought it was just to
prove to Firas that I wasn't a screwup... this city needs us. This world, this
universe, this dimension and all others... you're the only family I have and
my family is unbeatable." (**"You're super" is CUT from here — it belongs to
ch25** and the cut is Director-ruled; this half of the construction was
surfaced and left.) Leah: "How can we say no to that?" / Ben: "We don't. We
keep up the fight." / Victor: "we help the people who need it the most." /
Tess: "Because there's no one but us." All four turn to Ruth. **Ahdia: "This
doesn't work without you, boss."** **Ruth: "If we do this, we start over. Build
it up from the bottom because we're not just beating up muggers and getting
old ladies safely across the street anymore. We need to be ready for
cataclysms, cops and Kain."** Victor pulls Ahdia in with his good arm. Leah:
"So . . . ?" Ends on Ruth with her teeth in her lower lip and the room letting
her have the whole length of it — the answer given by the next section, not
by her mouth.

*§5 — Ruth, then Ahdia; sunset, the highest roof in the city; the MCC thirty
blocks south.* Five shadows on the gravel. **"All of them were in the matte
black armor, cut to their measurements, the same suits that had come off them
after downtown."** Ben's old vest over his; Leah's skating pads; Tess's hood
up; Victor's rebar taped; Ruth's twice-rebuilt harness. "Thirty blocks south,
forty feet of nothing hummed on a residential roof and threw no shadow at
all." **"All clear," Ahdia said in their ears. "Happy hunting."** Ruth on the
ledge: **"This is it. Yesterday, we lost someone. Today, we keep going. Because
that's what Firas would've wanted... It's not just Caledonia anymore. Not
just muggers and corrupt cops. It's singularities and cosmic entities and
things we don't have names for yet. No better place." / "No better time,"
they said back.** "Everyone's in position. Ready when you are." She goes off
backward, arms out; the others four seconds apart, spacing drilled "on a
stairwell in a school with no roof access at all." **"The wings caught and
hardened."** They fan out over the grid. Ruth flies her lane, tucks, flares,
lands on a gravel roof across from a corner store with a man inside holding
a bag. **"Then the gravel let go of her. An inch, maybe. Her heels came up off
it. They hung there. Then they settled back down. There was nothing in her
hands, no cable, no wing out, no reason for it anywhere in the equipment she
was wearing. / Thirty blocks south, a machine that belonged to nobody hummed
on a roof."** "Thank you," Ruth said into the radio, and went over the
parapet. / **"Go get 'em. I got your back."** **Ahdia in a horseshoe of
monitors "she had no clearance to touch, in a machine she had taken out of a
hangar without filling in anything, wearing a coat and socks and holding a
cigarette she had not lit."** "Down there they had a whole building for nights
like this one. They would log it, and file it, and wait for the right
signature... Nobody down there was going to get to him tonight." Function:
the book's answer to CADENS — the team goes without a signature, with Ahdia
as the building. **The float is UNEXPLAINED on the page** (log reads it as the
FAERIS enhancement from ch20 — reader-level only).

*§6 — EPILOGUE — Kain; the press conference, the elevators, the tank room.
Ratified as drafted (Director, 2026-08-31): do not re-cut it or reassign its
speakers.* Lights set low and warm, no shadow under the eyes: "Grief
photographs badly. Steadiness photographs well." **"I was nowhere near
downtown... an attempt by criminal elements to impersonate me and destabilize
my campaign... this terrorist attack."** Thirty cameras; polling overnight
"would be good, and the good would be worth more than the mansion, which was
insured." "That's all for tonight." A service elevator; a second elevator
down, "past four levels that appear on no drawing filed with any office in
the city. Forty-seven seconds, lobby to bottom. He had counted it once, back
when this part still made him nervous." A seamless white corridor, sensors in
the walls. **The tank room: rows of bodies floating chin down, hands open — a
boy of nine, a young man with hair, himself at forty, at fifty, at his
present weight and one he had not been in twenty years. "All of them asleep.
All of them paid for."** Cylinder **Forty-seven** open and dry: "An acceptable
loss. The accounting on it was clean." **"You look tired," a woman's voice
said.** She was not there a moment ago: white coat, no badge, no age, the
proportions a degree off. **Kain: "Forty-seven was our best integration. The
Tamois Heart had fully bonded. Years of work. Gone." / "And yet you're
here." / "That's the point of redundancy." / "I know the point. I'm living
it." / "Are you?" / "Forty-seven thought he was special too. Thought the Heart
made him more than a vessel. Look where that got him." / "How long until we
can reintegrate a Heart?" / "We have three more in storage. We can begin the
bonding process within a week. But that's not what you should be worried
about." / "What should I be worried about?" / "Agent Auerbach saw
Bellatrix." / "During the singularity?" / "According to the readings CADENS
picked up, yes. She transcended. Briefly. Made contact with higher-dimensional
space. She saw the hallway." / "That's not possible. The Seed was dormant, we
made sure—" / "Nothing is ever certain with the Seeds. That's why they were
scattered in the first place. To see what would happen. Who would find them.
What they'd do with them." / "Bellatrix doesn't interfere. She observes. But
she acknowledged Auerbach. That means something." / "What does it mean?" / "It
means the girl is more important than we thought. It means her death might
have consequences we can't predict. It means we proceed carefully."** His file
on the girl, "a line through it as of yesterday afternoon." **"The plan was
always to eliminate her once the Seed went dormant." / "Plans change... Focus
on the election. Win the presidency. That's your role. Let me worry about the
girl."** The door takes her. Ends on **"He stood where he was, in the hum,
among the rows of himself, every one of them asleep and waiting to be
worn."** — the villain restored, and reduced to a garment. Span 156 is the
woman, 157–158 are Kain, so "Are you?" and the Forty-seven needle land on him.

---

## KNOWLEDGE GATES AT END OF THE BOOK (violating these kills a draft)

**The shape of the ending:** every person on the page believes Firas is dead;
nobody on the page has been told, or will be, that Ahdia palmed a dose, that
she went into a corridor and was looked at, that a fifth Tank lives, or that
the man on the podium is a body from a tank. **The reader alone holds all of
it, and even the reader is never told Firas survives.**

**Ahdia (Auerbach — a name she declined)** — Knows: she pushes and pulls,
both at once through one body, and what that did to her skin; that she went
somewhere with doors that were lives and **was looked at and acknowledged by
something that had never been human** — she has no name for it and has never
heard "Bellatrix"; that she was "put back," by what she does not know; that
Firas held her hands with no Seed, injected her with the dose she had kept
for him, said "I knew you were in there somewhere," and went into the point —
**she reads death**; that the Seed is dormant, maybe permanently; that
CADENS found the team clean; that Bourn offered a badge and she refused it;
that CADENS says it has no reason to monitor her; that she took an MCC out of
a hangar and runs the team from it; that she gave Ruth her penthouse and
bank access; that Kain is on television alive claiming a lookalike (§2's
Carl Tucker is on in her own doorway — whether she watched Kain's presser is
not stated). **Does not know:** the fifth Tank; the Intermediary; the tank
room, Forty-seven, the woman, "Agent Auerbach saw Bellatrix," the plan to
eliminate her or its suspension; that Ryu and Bourn know she lied about the
eighth dose; CADENS' authorization politics; that her float-inch on Ruth's
heels happened. **Has told no one about the corridor** — not Ryu, not Bourn
(asked directly; smiled), not the team beyond "somewhere else" and "a
collapsing dimension." **"We need to talk about it. Later." — never happened
and never will on the page.** Her standing "Don't tell him" was overtaken by
Firas finding her on Main Street himself; how he learned she was alive and
came to be there is not on the page.

**Ruth** — Knows everything the team knows, plus: Ryu's private estimate of
days-to-a-week (ch23; she said "Weeks. Maybe less" to the team and never
corrected it); that Ahdia's "two weeks" was one day; that she was on the
pad when Bourn's stale report came in; that she saw the light leave Ogden
first. Believes all eight doses went in (ch25 — asked, told yes); was on
Ahdia's arm when Firas's injector went in (ch29) — **whether she registered
what it was is not on the page.** Has been given Ahdia's penthouse and bank
access. Called the team over and reversed it. Leads: "we start over." **Never
absolved in words by anyone**; Leah credits her with holding them together
and organising the chain; Ahdia calls her boss. **Her own case (§7) remains
unresolved and her heels left the gravel — she has not remarked on it.** Her
CADENS liaison role is never formally ended on the page.

**Ben, Leah, Victor, Tess** — Know: everything in the ch25 gate; that Ahdia
is Firas's sister and alive; that she accelerated them and then did "the
other thing" with both hands at the crater; that they killed four officers
by breaking them open ("You're feeding him!"; Tess: "We killed them"); that
CADENS dropped a missile into downtown (Mack's twenty were on the street with
Ruth, Ahdia, Ben, Leah and Victor; Tess and Firas were away); that Kain's body
became a singularity and Firas went into it; that Ahdia was "somewhere else"
and they hauled her out of "a collapsing dimension" (her words); that Kain is
alive on television claiming a lookalike and rebuilding his mansion; that
CADENS reclaimed the suits, and that they are wearing them again anyway; that
Ahdia is on comms from somewhere with an all-clear. **Do not know:** the
Intermediary; the words Temporalist, Hyper Seed, Auerbach; whether "Overseer"
reached them on the street (Mack said it in Ahdia's hearing; unstated for the
rest); how long Ahdia had or has; the palmed dose; the corridor, the doors,
the entity; the fifth Tank; the tank room; that Bourn's authorization came
fourteen hours late; where the MCC came from. **Their powers never came back
and never will on their own** — everything from ch24 to ch29 was inside
Ahdia's field, and on the last roof they fly on wings. **The CADENS offer was
never answered**; the cases going back down the elevator is the only answer
on the page. **Victor's lawsuit** against the PAC money is filed. **Tess** has
not chosen a new codename and has not faced her father (Book 2). **Victor's
arm is in a sling.**

**Firas** — Page-level: learned his sister was alive when she pulled him out
of the sedan (ch26), apologised, was told "I know," gave her his armor, was
ported off the street by Tess (ch27), came back (unstaged), held her hands at
the crater, injected her, and is gone. He was never told about CADENS by
Ruth; he saw the transport and asked nothing (ch23). **The only conversation
the siblings ever had on the page is the one in stopped time in ch26.**
Author-level: **displaced, not dead (bible §5b endpoint; log ch29/ch30)** —
never voiced by anyone, never hinted by the narration, not even known to the
woman in the tank room.

**Kain (the body in the tank room)** — Knows: Forty-seven and the bonded
Heart are gone; three Hearts remain; a bonding can begin within a week; "Agent
Auerbach saw Bellatrix" and Bellatrix acknowledged her; the Seed was
dormant ("we made sure"); his own thin file on the girl has a line through it
and the plan to eliminate her is suspended by someone above him; his role is
the election. Public position: nowhere near downtown, a lookalike, terrorism,
full confidence in law enforcement. **Does not know** Firas survives (log:
even the woman does not). Has known **Ruth Carter** by name since ch17 (the
file; the fifth Tank's "Dr. Carter"). Whether he knows Ahdia's real name is
not on the page — the woman calls her Agent Auerbach; the narration calls
her "the girl." Whether he knows the other four's names: not on the page.

**The woman in the white coat** — Knows CADENS' readings, the codename
Auerbach, the Seeds' scattering and purpose, the Hearts in storage,
Bellatrix. Outranks Kain. **Unnamed; do not name her, do not join her to the
Intermediary, do not decide whether she is Bellatrix.**

**Bourn, Ryu, Mack (CADENS)** — Know: the palmed dose ("She didn't take
it"); one-third cellular recovery at departure; the mechanism (opposing
forces; the Seed channelling through Ahdia, not the team); Terminus-level;
the team clean, no residual Seed energy; Victor's sling from the pull; the
Seed dormant (Ahdia's statement; Bourn accepts it and closes the file); Kain's
spin and their inability to touch him; the authorization's timing and what it
means; that Mack fired without it; the existence of other Seed-bearers to
track. **Have readings on Ahdia at the singularity** that the woman in the
tank room also has (a leak the page states from Kain's side only). **Do not
know:** the corridor (asked; refused); the fifth Tank's status is not
mentioned by anyone; **the MCC's absence is not shown noticed.** Never
confront Ahdia about the dose.

**Whitford / the Intermediary / Jericho** — Whitford unchanged since ch17;
the drives remain unused. The Intermediary has not called again and CADENS
has never been shown aware of her. Jericho is in protective custody with his
research, off the page since ch23.

**Reader knows (dramatic irony to carry into Book 2):** that Firas is
"displaced" only at author level — the page reads death and so must every
character; that Ahdia palmed the dose and CADENS found out; that a fifth Tank
is alive with a face nobody remembers; that the Kain on the podium is one of
a row of Kains and that the one who fought was Forty-seven; that three more
Hearts exist; that a woman with no age commands Kain and has CADENS' readings;
that what looked at Ahdia in the corridor is called Bellatrix by that woman
and by nobody else; that "the plan was always to eliminate her" and "plans
change"; that the ch24 dream held two presences (the vast curious one; the
cold "Wake up") and the ch29 entity is not on the page identified with
either; that the drone on Tess's shoulder and the inch under Ruth's heels are
both unexplained and both sit beside a machine that is learning to do
Ahdia's job; that CADENS' clearance arrived fourteen hours late by design;
that the Intermediary's "CADENS observes. They do not enhance" is now
contradicted by ch20 and ch30 and nobody on the page knows it.

---

## WHAT BOOK 2 INHERITS

**PAGE-LEVEL — on the page and unresolved (source in brackets):**

1. **Kain is alive, running for President, and is a row of bodies.**
   Forty-seven fought and died; three Hearts in storage; "bonding process
   within a week"; the mansion rebuilding; the campaign rolling; the public
   story a gas leak and a terrorist attack. [ch30 §2, §3, epilogue]
2. **The woman in the white coat** — unnamed, ageless, off-proportion,
   commands Kain, has CADENS' readings, calls the girl "Agent Auerbach," has
   taken "the girl" as her own concern: "Plans change... Let me worry about
   the girl." [epilogue]
3. **"Agent Auerbach saw Bellatrix" / "she acknowledged Auerbach."** The
   name exists only in the woman's mouth. Ahdia's own account has no name.
   [ch29; epilogue]
4. **The plan to eliminate Ahdia** "once the Seed went dormant" — stated,
   then suspended, not cancelled. [epilogue]
5. **The Intermediary** (ch17) — a woman's voice, "his civilization," Power
   Extempore, "CADENS observes. They do not enhance," "subjects," wanted the
   team dead for the activation protocols; promised to call again; never
   did. Identity, employer, species unestablished. Presumed Book 2. [ch17;
   base file item 8; not ruled]
6. **Chief Whitford** — Director-ruled an ongoing Book 2 threat, corrupt only;
   **Tess never facing her father is Book 2's business.** The drives hold
   proof he is on the payroll; Ben wants them used; Victor expects them to
   stop at the PAC. [log 2026-09-02; ch21; ch30 §2]
7. **Victor's lawsuit** over the PAC donation Firas signed out of Ahdia's
   estate; "Ahdia may not get her money back but neither will Kain."
   [ch21 clause, Director-ruled 2026-09-01; ch30 §2]
8. **The fifth Tank** — alive, off the board, forgettable face, calls Ruth
   "Dr. Carter"; promise `fifth-tank-survivor`, payoff unassigned; any later
   use is a Director call. Ahdia never told. [bible §7h; PROMISES.jsonl]
9. **"We killed them."** Four officers dead at the team's hands, unprocessed
   after ch28; the no-kill rule broken without their knowledge; Tess said it
   and was not there to carry it. [ch27–28; log ch28 ruling]
10. **Ahdia and Firas: "We need to talk about it. Later."** Unpaid. What Firas
    said in ch12 "confirmed the whole case she had been building against
    herself since she was a kid" and the only reply he ever got was "I know."
    [ch26]
11. **The corridor** — the doors that are lives ("Firas alive, and no Ahdia
    anywhere in it"); the thing that acknowledged her; "something took hold
    of her and put her back" (what, unstated); she has told no one. CADENS
    has readings; so does Kain's side. [ch29; ch30 §1; epilogue]
12. **The ch24 dream's two presences** — the vast, patient, curious thing
    that passed down the hallway; the cold, final "Wake up" that "did not
    belong to the Seed." Neither named, explained, or on the page connected
    to the ch29 entity. Promise `B1P-015-vast-watcher` (ch13, ch24) remains
    open in the file. [ch24; PROMISES.jsonl]
13. **The Seed is "dormant. Maybe permanently"** — Ahdia's words; Bourn
    closes the file on them; the woman: "Nothing is ever certain with the
    Seeds." No number for Ahdia's remaining time is given after ch29. [ch30]
14. **FAERIS** — three days into independence at 10% (ch20); a drone that
    would not leave Tess's shoulder (ch25); an inch under Ruth's heels with
    "no reason for it anywhere in the equipment" (ch30 §5). None explained.
    Projection: 50% in six months, full in twelve to eighteen. [ch20, 25, 30]
15. **The stolen MCC** — CADENS' machine on a roof, cloaked, "belonged to
    nobody"; CADENS not shown noticing. Wingsuits. [ch30 §5; bible §7b]
16. **The suits came back** — reclaimed by two men who signed for them,
    worn again that sunset, unexplained on the page. [ch30 §2, §5]
17. **CADENS' politics** — "whoever's pulling strings above us"; the
    authorization designed to arrive late; Mack's career line; Bourn building
    a file and waiting. [ch28; ch30 §3]
18. **"Track the Seed-bearers."** Other Seed-bearers exist and CADENS tracks
    them. Nothing more. [ch30 §3]
19. **The CADENS offer to the team** — never answered in words. [ch23; ch30]
20. **Ruth** — unforgiven in words, followed in fact; her §7 ambiguity never
    resolved; the float; her liaison status never ended; she now leads a
    team aimed at "cataclysms, cops and Kain." [ch25–26, ch30]
21. **Tess wants a new codename** and has not chosen one. [ch22]
22. **Jericho** in protective custody with all his research. [ch23]
23. **The scratched-out wedding photograph** in the nonprofit's back office
    (ch14b), touched by no one. The no-dead-wife ruling stands regardless.
24. **Kain's file on Ruth Carter** and his stated intent to take her research
    (ch17) — the man who wanted it is dead; the man on the podium may or may
    not remember wanting it. Not on the page.
25. **Bible OPEN QUESTIONS 1–4** carry unchanged: the exchange rate; her
    phone; FAERIS inside vs outside her field; whether hunger/aging inside
    long holds accumulate. Do not resolve.
26. **Promises file status (PROMISES.jsonl, as filed — the file has not been
    re-statused; the bracket is where the page touches each):**
    B1P-001 museum-abductee open [Jericho, ch17/22/23] · 002 triomf open ·
    003 4d-object open [the Heart; consumed ch29; three more exist] ·
    004 ahdia-presumed-dead open [the team learns ch24–25; Firas ch26] ·
    005 who-tied-kain PAID (ch13) · 006 guns-jam open [ch16 trigger table] ·
    007 police-foreknowledge open · 008 parents-vanished open · 009 chosen-one
    open · 010 cr7-lab open [ch19–20] · 011 whitford-name open [ch12 states
    the father link] · 012 event-horizon-line open · 013 keycard-blood PAID ·
    014 47-motif open [the epilogue's cylinder Forty-seven, forty-seven
    seconds, forty-seven minutes] · 015 vast-watcher open ·
    fifth-tank-survivor open.

**AUTHOR-LEVEL — ruled, never on the page, never in a character's mouth:**

- **The endpoint is metamorphosis; every character models it as death.**
  Firas is displaced, not dead. Ryu's terminal framing is sincere. No
  character speculates; no narration editorialises the door. The only
  whispering is the conversion language itself. [bible §5b, Director-ruled
  punch #8; log ch29 "Firas dissolves believing he is dead"; log ch30 "even
  she does not know Firas survives"]
- **The corridor entity is named only in the epilogue's dialogue.** Ahdia's
  POV never names it and offers no speculation. [log ch29]
- **The fifth Tank's forgettable face rhymes with the Kain clone's
  facelessness** — a planted signature, payoff unassigned. [bible §7h]
- **Ruth's inch is the FAERIS enhancement from ch20** — reader-level reading
  in the log; the page says only "no reason for it anywhere in the equipment
  she was wearing." [log 2026-09-01 punch item 1]
- **The suits on the last roof are the stolen-armor payoff** (the duffel).
  [log punch item 1]
- **Bourn's ch23 report was stale**; Ahdia surfaced during the mansion feeds
  and did not keep it. [bible §7f]
- **Tess's ch22 second — "She picked Ben"** — is a debt nobody ever tells her
  about. [log ch22 rebuild]

---

## Vetting corrections already in the text (do not "restore" old readings)

Sable's murdered wife — excised, ruled never to exist · parents are
collectors, not engineers · disappearance "over fifteen years ago" · judo, not
jiu-jitsu · CH07 rally cry standardized · "Kaine" → Kain · Kain is a
presidential candidate, never a mayor · Bourn is a woman, and is Overseer ·
the team owns no vehicle, in ops as well as patrol · no year appears in the
prose · CH18 fan-gratitude drift excised — the only public gratitude scene
that stands is the ch22 alley photograph, and nothing public touches the
Academy · **"Marcus" never appears; "Shiba" was drift and is gone — Ryu
Matsuda** · CADENS has exactly one expansion.

**Ruled since the ch25 file — these were open and are now closed:**
**Ch22 is REBUILT** — Tess POV, staging A (camera grid for M1–2, in for M3),
three movements, Kain's mispricing on the page, the plinth case starred by a
shoved guard, the fight ending verbatim on the light having changed color;
the old ch22 entry is void · **ch9's training paragraph is two sentences**,
paid by ch22; the survivor is "the training had no answer in it" · **Ahdia is
twenty-seven** at both sites; Firas twenty-five · **twenty-six hours**, both
ch24 sites; eighteen is gone (crew derivation from the on-page clock, Director
delegated; veto open on the figure) · **counting and the accounting family
are BANNED for everyone; the "reserved to Ahdia" reading was a crew carve-out
and is reversed** (R105/R106) · Kain-POV exempt from the accounting ban only ·
"the way X verbs" swept to zero outside ch26 · adverb floor removed; the
appraisal vocabulary swept · trailing which-clauses thinned · **the palmed
dose** (ch24, 11 words; ch29 payoff; ch30 discovery) · **"You're super" cut
from ch30**; it lands in ch25 · **the PAC clause added to ch21** (Firas signed
the donation from his sister's estate — not from "Gale's accounts," which was
a caught crew error) · ch10 "under and around" · **ch28/ch29: Mack commands
the ground, Bourn is never on the pavement** · **naming drifts by contact in
ch28–29** · **"We killed them" is Tess's** · ch22 "That was fun" is Tess ·
ch19 "Worth it." is Ahdia · the 41 dropped tags restored (tags reduced to
"said," never dropped) · ch08's two narration constructions fixed; "Counted
heads" and the fragmentation stay (Director: "They literally transported") ·
ch23's CADENS expansion, Bourn's pronouns, and the van fixed · Bourn's ch24
clothes are the ch23 suit · the epilogue ratified as drafted · **§7b has two
exceptions** — the cover vehicle and the endgame MCC base; wingsuits from ch30 ·
Whitford closed, no action.

---

## COLLISIONS FOUND WHILE WRITING THIS FILE (1, 2, 5 resolved in canon the same day; 3, 4, 6–9 UNRULED — do not resolve; listed for the Director)

1. **Eighteen vs twenty-six hours — RESOLVED 2026-09-02 (crew, same pass as this file).** Bible §7f now reads "twenty-six hours under" and §7h "the night before the climax"; committed with this file. History, for the record: at 8d6417f bible
   §7f says "surfacing from eighteen hours under" and §7h says "eighteen
   hours before the climax"; the log's 2026-08-30 ch24 entries say "The
   calendar keeps eighteen" and mark the three→eighteen edit "STILL PENDING";
   the log's 2026-09-02 entry and both shipped ch24 sites say **twenty-six**.
   The log and the draft win. **An UNCOMMITTED working-tree edit to the bible
   (two lines, dated 2026-09-02 10:47, not made by the agent that wrote this
   file) already changes §7f to "twenty-six hours under" and §7h to "the
   night before the climax."** Whoever commits next should know it is sitting
   there. This file uses twenty-six.
2. **Ahdia twenty-three vs twenty-seven — RESOLVED 2026-09-02.** Bible §8 now says twenty-seven; `CANON_FACTS.jsonl` B1V-015 and `CHRONOLOGY.jsonl` B1C-001 now carry eight/six and the nineteen-year gap. History: §8 listed "Ahdia twenty-three"
   among the relative anchors; the ch25 log entry calls her "a 23-year-old";
   the 2026-09-01 ruling and shipped ch19 say twenty-seven. Ruling wins; §8 is
   stale. `CANON_FACTS.jsonl` (B1V-015: ~7/~5 at Montana) and
   `CHRONOLOGY.jsonl` (B1C-001: ~7/~5, "over ten years") are also stale
   against the eight/six and fifteen-plus rulings.
3. **§7b vs ch26's sedan.** §7b: no team vehicle ever, two exceptions (cover;
   MCC). Ch26: Firas drives "a gray sedan, civilian, with a front-quarter dent
   nobody had ever gotten around to fixing" into Kain, and Ahdia recognises
   the dent ("here came the dent in the front quarter panel"). No earlier
   chapter establishes the car; no log entry addresses it; ch26 was
   line-edited by the Director personally. Flagged, not extended.
4. **Bellatrix and the woman's voice.** The packet brief for this file
   states Bellatrix is on the page "at ch25's near-transcendence and,
   unnamed, as the epilogue's 'a woman's voice.'" On the page the
   near-transcendence is ch29 (ch25 is the introduction and the plan), and
   the woman speaks of Bellatrix in the third person ("Bellatrix doesn't
   interfere. She observes. But she acknowledged Auerbach"). Nothing in
   `canon/` rules the woman's identity for Book 1. This file records the
   page and leaves her unnamed.
5. **§7g vs the ch28 ruling — RESOLVED 2026-09-02.** The contact drift (Leah at the shove, Victor at the building, Ben and Tess inside the human chain; Mack on the street, Bourn never) is now appended to §7g. History: §7g grounded Ahdia's codenames in
   "She has never met them" with no mention of the contact drift the Director
   ruled for ch28–29 (log only). The log wins; §7g lags.
6. **The press conference clock.** Bourn (ch30 §3): "You saw the press
   conference this morning?" The epilogue's broadcast carries the same
   lines and ends "That's all for tonight." Kain's file has "a line through
   it as of yesterday afternoon." The epilogue's day is not pinned by the
   page; this file does not pin it.
7. **The older topographies' "photograph folded behind her school photo in
   her father's desk frame"** (carried from CH01-22 into CH01-25, item 12)
   could not be located in any shipped draft (ch09, ch16, ch17 checked).
   Dropped from this file's inherited list; treat as NOT ON THE PAGE unless
   someone finds the line.
8. **Who owns the "three unpaid debts."** The ch22 rebuild entry calls "She
   picked Ben" Tess's "third unpaid debt after the fifth Tank and 'We killed
   them'"; §7h assigns the fifth Tank's uncollected credit to Ahdia. A
   wording wobble in the log, not a state conflict; recorded so nobody
   builds on it.
9. **The base ch25 gate said Kain "does not know any of their real names."**
   Ch17's Ruth Carter file and ch18's "Dr. Carter" contradict it for Ruth.
   Corrected above; noted because the older file said otherwise.
