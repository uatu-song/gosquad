# Timeline Keeper — Book 1 Steward Run 1 Evaluation

**Agent:** timeline_keeper
**Task:** Reconcile all 10 stewards' beats into one linear move-sequence; flag every chronological problem (timing contradictions, convergence traffic jams, ordering conflicts, move-fact errors).
**Sources:** `book1_chess_game.pgn` (136-ply, Carlsen–Nepo 2021 G6, 1-0), `BOOK1_MOVE_MAP.md` (stud anchors + phase skeleton), the 10 `*_run1.md` steward files.
**Domain:** Chronological accuracy only. Character-state math, theme, irony, and pacing deferred to the named specialists below.

---

## Domain & method

I built a single linear move-spine from the PGN, placed every steward-owned beat on it by its cited move number, and checked three things at each occupied move: (1) does the cited PGN move-text match the actual game; (2) do co-located beats agree on what move-number an event sits at; (3) does any beat assume an event the move map says hasn't happened yet. I treat the PGN as ground truth for move-text and `BOOK1_MOVE_MAP.md` as ground truth for stud→move anchoring. I do **not** judge whether the timing *works* dramatically (Pacing Monitor) or whether character states are numerically consistent (Status Tracker).

### Reconciled move-spine (steward beats placed on PGN)

| Move | PGN (verified) | Stewards present | Convergence |
|------|----------------|------------------|-------------|
| M1 | `d4` | Firas (♕ opening) | — |
| M3 | `g3` | Tess (g-pawn enlists) | — |
| M4 | `Bg2` | Leah (bishop deploys) | — |
| M6 | `b3` | Ben (b-pawn perimeter) | — |
| M7 | `dxc5 Bxc5` | Ruth (CR-7 / d-pawn), Leah (first punch / d-pawn) | shared piece, no conflict |
| M8 | `c4 dxc4` | Leah (c-pawn over-extension) | — |
| M11 | `Nxc4` | Ahdia (♘ first capture) | — |
| M14 | `a3` | Victor (a-pawn roots) | — |
| M17 | `Bxf6 gxf6` | Ben (♗), Victor (♗ + cross-faction ♞), Kain (g-pawn) | shared piece, **see F2** |
| M19 | `Nxd4 (Bxd4)` | Tess (♘ strike) | — |
| M20 | `Bxg2 Kxg2` | Ruth (♗ dies), Leah (♗ falls) | shared piece, no conflict |
| **M26** | `Qxc8 Rxc8` | Ahdia (CP-1, fire), Firas (shot + told Ahdia dead), Bourn (CP-1) | **CP-1 — see Sound** |
| M27 | `Rxc8 Qd5` | Ryu (intro) | **move-text error — see F1** |
| M29 | `e3` | Ahdia (e-pawn wakes) | — |
| M30 | `h4` | Tess (h-pawn baseline) | — |
| M33 | `Rd1 Bxa3` | Victor (a-pawn overrun), Bourn (Mother FAERIS) | shared piece, no conflict |
| M39 | `Nc5 Qxb4` | Ben (b-pawn falls) | — |
| M40 | `Nxe4` | Ahdia (♘ 2nd capture) | — |
| M53 | `Rxa3 Qxh4+` | Tess (h-pawn punched through) | — |
| M59 | `f3` | Ryu (f-pawn / system wakes) | — |
| M79 | `Rxf5` | (Kain references g-pawn exit) | — |
| **M80** | `Rxf7+ Kxf7` | Firas (♖ sidelined), Ben (♖ removed / EMP), Kain (♝ trap) | **see F3** |
| **M82** | `Rxa7` | Ahdia (CP-2), Ruth (CP-2 reveal), Ryu (CP-2), Kain (CP-2), + Leah/Victor aftermath ~M82+ | **CP-2 — see Sound + F4** |
| ~M108/110 | `Rd4` / `e4` | Ahdia (bidirectional-time discovery) | — |
| M114–115 | `gxh4 / Qxh4` | Tess (g-pawn vigilante seed) | — |
| ~M116–120 | `Rd3 Kf8 … Re3` | Firas (the suit) | — |
| ~M128 | `Re5+ Kf7 / Rf5+ Ke8` | Bourn (missile authorization) | — |
| M133 | `e6` | Ahdia (near-transcendence), Firas (autoinjector) | — |
| **M131–136** | `… e6 … f5 … Ng7 1-0` | ALL TEN | **CP-3 — see F5 + Sound** |

---

## Findings

### F1 — Ryu cites the wrong PGN move-text for M27 · **FIX**
**File:** `Ryu_run1.md`, M27 beat header: "`M27 — \`Bf8\` (Black retreats the dark-square bishop; quiet regroup after the queen sac)`".
**Problem:** Per the PGN, **move 27 is `27. Rxc8 Qd5`** (White completes the rook recapture begun at M26; Black plays Qd5). **`Bf8` is Black's 41st move** (`41. Rac2 Bf8`) — verified by grep against the PGN. Ryu's chess-fact and the parenthetical gloss ("Black retreats the dark-square bishop") describe move 41, not move 27.
**Severity:** FIX. The *narrative* placement (Ryu's intro lands just after the queen sac, in the M26–29 settling) is chronologically fine and consistent with the move map. Only the move-text label is wrong.
**Reconciliation:** Either (a) keep the beat at M27 and correct the chess-fact to `27. Rxc8 Qd5` (White hauls the second rook to c8, Black consolidates with Qd5 — still a "quiet regroup after the queen sac," so the reading survives), or (b) re-anchor the beat to M41 `Bf8` if the "dark-square bishop retreats" image is load-bearing. Option (a) is cleaner: it keeps Ryu's intro in the immediate post-sac settle where the move map wants it, and the "regroup" reading holds under the real M27.

### F2 — M17 is claimed by three stewards through the same piece; order of the recapture must be fixed · **NOTE**
**Files:** `Ben_run1.md` (♗ "spots the seam," walks the counter-move into the gap), `Victor_run1.md` (♗ "single act of direct intervention," his ethical strike = the captured cross-faction knight), `Kain_run1.md` (g-pawn "answers a bishop... I spend a man").
**Problem:** Not a contradiction — the shared-piece design intends Ben+Victor to both read the c1-bishop and Kain to read the recapturing g-pawn. But chronologically, all three describe the *same single ply pair* (`Bxf6` then `gxf6`) as the seat of distinct dramatized events: Ben's "trap with a paper trail," Victor's "one act of direct intervention" that pulls a kid out, and Kain spending a uniform that results in "Firas takes the bullet, the docks happen." These cannot all be discrete on-screen moments at one move without a defined order.
**Severity:** NOTE (design intent is sound; blocking needs sequencing). Also note Kain's M17 gloss ("Firas takes the bullet, the docks happen") **forward-references the M26/M80 docks material** — at M17 the docks/shooting have not happened on the move-spine. That is fine as Kain's *causal* framing (he sets the trap here, it pays later) but must not be staged as if Firas is shot at M17.
**Reconciliation:** Treat M17 as one event read from three vantages (Ben's tactical read → Victor's strike → Kain's expended foot-soldier), not three separate scenes. Keep Kain's "docks/bullet" as seeded consequence, payoff at M26 (Firas shot) and M80 (trap springs). Defer the staging order to Scene Choreographer.

### F3 — M80 "Firas shot" vs "Firas sidelined" — two different injury moments must not collapse · **FIX**
**Files:** `Firas_run1.md` M26 ("a round goes through him... flat on a gurney with Ruth's hands in him") **and** `Firas_run1.md` M80 ("The injury takes him off the field... the midgame is the wound healing wrong"); `Ben_run1.md` M80; `Ruth_run1.md` M7 ("Firas is on the table with a gunshot wound"); `Ruth_run1.md` M20 ("Firas is alive but sidelined, recovering").
**Problem:** There are **two** Firas-injury events on the spine and the stewards distribute them inconsistently. Ruth's M7 beat treats Firas's gunshot/surgery as happening at **M7** (CR-7 saves him on the table). Firas's own M26 beat treats the gunshot as happening at **M26** ("in the same stretch of bad hours, the warehouse burns"). Firas's M80 beat treats M80 as the sidelining injury. The move map (Stud 3 / M80) is explicit: M80 is "NOT a personal Kain duel... the injury takes him off the field." So which move is the *bullet*, and which is the *sidelining*?
**Severity:** FIX. This is a genuine cross-steward timing contradiction on a stud-critical event. Ruth places the life-saving surgery at M7; Firas places the shooting at M26; both can't be the same wound, and the M80 sidelining is a third beat.
**Reconciliation (proposed, defer state-detail to Status Tracker):** The move map anchors Stud 1 payoff (queen sac = Firas leaves center) at M26 and Stud 3 payoff (EMP trap, Firas off the field) at M80. Cleanest linear reading: **M7** = an *early* wound that CR-7 treats (establishes the treatment, per Ruth's d-pawn reading) — a smaller incident, not the queen-sac shooting. **M26** = the queen-sacrifice shooting that removes Firas from center-stage protagonist status (Firas's own beat) coinciding with the warehouse fire. **M80** = the EMP trap that takes the *recovered* Firas off the field again for the long midgame. But Firas's M80 beat ("the midgame is the wound healing wrong") reads as if the *M26* wound is still healing through the M27–M80 stretch — which conflicts with him being active enough to be re-sidelined at M80. Ruth's M20 beat ("Firas is alive but sidelined, recovering... for the whole stretch ahead") compounds this by placing the long sidelining at **M20**, before M80. **Recommend the Director pick ONE sidelining move** (M26 vs M80) and make M7/M20 consistent with it. The PGN supports M80 as the trap (Stud 3), so M26 should be the shooting and the *recovery* should span M26→~M80, with M80 as a re-injury or the trap that keeps him down — not a fresh first wound. Flag the "M7 surgery vs M26 shooting vs M20 sidelining vs M80 sidelining" four-way spread for Status Tracker to reconcile against Firas's availability window.

### F4 — Leah & Victor place the reveal "~M82+" / "~Ch25"; canon move map splits these · **NOTE**
**Files:** `Leah_run1.md` ("Reveal-aftermath (~M82+)... The truth lands (~Ch25)"), `Victor_run1.md` ("The reckoning (~M82+)... He learns his 'tactical precognition' was Ahdia"); also `Ahdia` M82, `Ben` ("read the truth ~Ch25"), `Tess` ("the reveal (~Ch25)"), `Ruth` M82.
**Problem:** The move map (Stud 4b) is explicit: **Ruth learns at the Docks (M82, ≈Ch19); the team learns Ch25 (~M110).** Several stewards correctly distinguish these (Ruth knows at M82; Ben/Tess/Leah/Victor say "~Ch25" for the team). But Leah and Victor both tag their reckoning beats "**~M82+**," which reads as *adjacent to the Docks* when canon puts the team's learning ~28 moves later at ~M110/Ch25. Ahdia's own M82 beat correctly says only Ruth is present; her team-reveal awareness is Ch25.
**Severity:** NOTE (the stewards' prose says "~Ch25" in-body, so the intent is right; only the "~M82+" header label risks collapsing the two reveals). No steward actually has the *team* knowing at M82.
**Reconciliation:** Re-label Leah's and Victor's reckoning headers from "~M82+" to "~M110 / Ch25 (team reveal)" to keep them off the M82 Ruth-only beat. The two-tier reveal (Ruth M82 → team ~M110) is canon and currently intact in substance; this is purely a label-hygiene fix to prevent a future blocking pass from stacking the team reveal onto the Docks.

### F5 — CP-3 (M131–136) all-hands traffic: ordering of injection / Ng7 / missile / chain is consistent but unsequenced · **FIX (sequence lock needed)**
**Files:** all ten CP-3 beats; specifically `Ahdia` (e6 transcendence → autoinjector into her → Ng7 → Firas dissolves → lands ~30%), `Firas` (gives needle → singularity takes him), `Ruth` (organizes chain → watches injection → Firas gone), `Bourn` (~M128 missile already in the air → M136 kill), `Kain` (kaiju M131–135 → Tank 47 dies to missile+singularity → King "resigns"/walks off).
**Problem:** Six ply (M131–136) must contain, in a consistent order: (a) Ahdia reaching e6/transcendence [M133]; (b) the human chain forming; (c) Firas finding the last dose and injecting **her** [M133–135, f5 at M135]; (d) Bourn's CADENS missile [authorized ~M128, lands in this window]; (e) Tank 47 / kaiju destroyed by **missile + the singularity Ahdia burns out**; (f) `Ng7` [M136] as the image the team reads as the kill; (g) Firas dissolving/displaced; (h) Ahdia dragged back to ~30%. The stewards do not contradict each other on *what* happens, but no two fully agree on the *order* of (d)/(e)/(f)/(g) relative to each other, and the move map ties specific beats to specific ply: autoinjector at M133–135 (e6/f5), Ng7 the finish at M136, missile authorized ~M128. The risk is a "traffic jam" where injection, missile-impact, kaiju-death, Ng7, and dissolution all want to be "the climactic instant."
**Severity:** FIX. The canonical causal chain is stated across the move map and stewards but never locked into a single ordered sequence, and CP-3 is the most-occupied window in the book (10 stewards, 6 ply).
**Reconciliation — proposed canonical CP-3 order (for Director ratification; cinematic timing deferred to Pacing/Choreographer):**
1. **~M128 (pre-window):** Bourn signs the strike package; missile inbound. (Bourn beat — consistent.)
2. **M131–132:** Kain integrates Tamois Heart → Tank 47 kaiju at full output; chain begins forming. (Kain + all hands.)
3. **M133 (`e6`):** Ahdia hits e6 — transcending/dissolving upward; chain is hauling. (Ahdia + Ruth/Ben/Tess/Leah/Victor.)
4. **M134–135 (`f5`):** Firas finds the last dose, "*Oh hey. I knew you were in there somewhere,*" injects **her**, not himself. (Firas + Ahdia.)
5. **Kaiju kill:** Bourn's missile + the singularity Ahdia burns out destroy Tank 47 — the two-part canonical kill.
6. **M136 (`Ng7`):** the image the team reads as ending Kain; Black "resigns" (no on-board mate). Firas dissolves into the singularity, displaced.
7. **Aftermath:** Ahdia pulled back to a body at ~30% baseline; Kain clone-survives off-board (epilogue).
This order is consistent with every steward's stated content and with the move map's per-ply anchors. **The one ordering tension to confirm:** whether the missile/kaiju-death precedes or follows `Ng7`. The move map calls `136. Ng7` "the final blow the team believes ends Kain" and names "Bourn's CADENS missile + the singularity" as the *canonical* kill — i.e., the missile/singularity kill is the real mechanism and Ng7 is the *image* of it. So mechanically the kill (5) and the image (6) are simultaneous/concurrent, not sequential; the chain (3) overlaps both. Recommend Director treat 3–6 as one braided instant rather than four discrete ticks.

### F6 — "~30% baseline" endpoint is unanimous and chronologically anchored, but is a state-fact · **defer**
Every CP-3 beat lands Ahdia at "~30% baseline, 18–24 months with treatment." This is chronologically consistent (all stewards put it at the same move, M136). Whether 30% / 18–24 months is numerically correct against the cellular-integrity clock (M11 "97%" → M29 ledger opens → M82 crater → M136) is **not my call** — see deferral to Status Tracker.

---

## Out-of-domain deferrals

- **Status Tracker** — (a) Firas's injury/availability window (F3): reconcile M7 surgery vs M26 shooting vs M20/M80 sidelining into one availability timeline. (b) Ahdia's cellular-integrity math: M11 "97%" → M29 ledger → M82 crater → M133 dissolution → M136 "~30% baseline, 18–24 months." Confirm the numbers are monotonic and the 30% endpoint is sourced. (c) Whether CR-7 at M7 and CR-7's later role are the same prototype timeline.
- **Pacing Monitor** — whether the CP-3 six-ply window (F5) is over-stuffed for the tension curve, and whether the long M40→M80 midgame gap (only Ryu M59 occupies it) sags. Also the M19–M22 / M80 "rook rampage" pacing.
- **Reader Proxy** — the dramatic-irony layering at M82 (Ruth knows, team doesn't until ~M110) and CP-3 (transcendence-not-death; Firas displaced-not-dead; Bellatrix watching). I confirm the *timing* of who-knows-when; whether the irony lands is theirs.
- **Theme Guardian** — Kain's "you cannot punch fascism unconscious" epilogue thesis and the both/and survival; not a timing matter.
- **Scene Choreographer** — staging order *within* M17 (F2) and *within* the CP-3 braided instant (F5); I supply the move-order constraints, they block the bodies.

---

## What's sound

- **Every steward-cited PGN move-text is correct except Ryu's M27** (F1). M7, M8, M11, M14, M17, M19, M20, M26, M29, M30, M33, M39, M40, M53, M59, M79, M80, M82, M108/110, M114–115, M116–120, M128, M133, M135, M136 all verified against the PGN as written by their stewards.
- **CP-1 (M26)** is clean: Ahdia (fire/closed file), Firas (shot, told she's dead), and Bourn (refuses to list deceased) occupy the same move with three non-contradicting vantages. The fakeout (apparent-hero Queen off, King remains) is consistently read.
- **CP-2 (M82)** is chronologically coherent across Ahdia/Ruth/Ryu/Kain: the act is Ahdia's in frozen time, Ruth's rook merely registers/witnesses, Ryu is at the chair one remove away, Kain never sees it and defers upward. All four agree on **who knows what at M82** (Ruth in; team out; Kain mystified). The two-tier reveal (Ruth M82, team ~Ch25/M110) is intact in substance.
- **Stud→move anchoring holds** for every stud: fakeout M1→M26, e-pawn wake M29, costs M33/M53, rook sac M80, Docks M82, bidirectional time ~M108, suit ~M116–120, autoinjector M133–135, finish M131–136. No steward violates the phase skeleton's ordering.
- **Shared-piece beats** (d-pawn M7 Ruth/Leah; ♗ M17 Ben/Victor; a-pawn M33 Victor/Bourn; ♗ M20 Ruth/Leah; King/f-pawn Ahdia/Ryu) never place their shared move at *different* move-numbers — the sharing is consistent.
- **CP-3 content** (not order) is unanimous: injection into Ahdia not Firas, Ng7-as-image-not-mate, missile+singularity as real kill, ~30% endpoint, Firas displaced. No steward contradicts the canon line.

---

## One-line verdict

**Chronologically sound overall — one move-text error (Ryu M27, FIX), one genuine cross-steward injury-timing spread (Firas M7/M20/M26/M80, FIX), a CP-3 six-ply order that needs a one-time sequence-lock (FIX), plus two label-hygiene NOTES (M17 three-vantage staging, Leah/Victor "~M82+" vs Ch25); no BLOCKERS, and all three convergence points are clean on who-knows-what.**
