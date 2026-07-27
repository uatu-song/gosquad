# The Chess-Narrative Engine — Book 1 Instance, Extracted

**Status:** PROTOTYPE / EXPERIMENT. Not canon, not manuscript, not an editorial decision.
Nothing here changes Book 1 or Book 2 work. Built 2026-07-27 to test one question:
**can the engine be recovered from the steward outlines, and can it then drive new
writing assignments on its own?**

**Method:** two agents read the ten Book 1 steward outlines *blind* (forbidden from
opening the PGN, the triplet file, or the move map) and tried to reconstruct the engine
from the beats alone. Three more agents built the move-indexed beat matrix. The chess
layer was then verified move by move against the actual game with a board engine, so
every claim below about pieces and captures is checked rather than repeated.

---

## 1. The game

| | |
|---|---|
| **Players** | Magnus Carlsen (White) vs Ian Nepomniachtchi (Black) |
| **Event** | FIDE World Championship Match 2021, Dubai, Round 6 |
| **Date** | 2021-12-03 |
| **Opening** | D02 — Queen's Pawn Game, Symmetrical Variation, Pseudo-Catalan |
| **Length** | 136 moves / 271 plies — the longest game in World Championship history |
| **Result** | 1-0, Black resigns in a lost position (no on-board mate) |
| **Faction assignment** | **White = Go Squad. Black = the antagonist side.** |
| **Source** | `6_manuscript/book_1/book1_chess_game.pgn` |

**Why this game carries Book 1.** A quiet symmetrical opening; the decisive material
event is front-loaded (queen trade at M26); then roughly 110 moves of grinding attrition
to a quiet knight finish. The shape is *win by endurance, not fireworks* — which is the
book's thesis. Two White pawns reach the 6th and 5th ranks at the very end and neither
promotes: the structural image of arrested transcendence.

**Verified game statistics** (computed, not asserted):

- 25 captures total across 271 plies; 28 plies deliver check.
- **Zero captures between M83 and M99** — seventeen consecutive moves of nothing.
- Only 2 captures in the 38 moves from M41 to M78.
- Most-moved piece: the **Black Queen, 68 moves**, which survives to the end.
- Most captures by one piece: the **White a1 rook, 5**.

---

## 2. Piece-to-character mapping (the triplets)

Each character reads the game through three pieces. The triplet is a lens onto *this*
game, rebuilt per book. Pieces recur across characters deliberately — the same square
carries two incompatible meanings and the characters never know they share it.

| Character | Faction | Piece 1 | Piece 2 | Piece 3 |
|---|---|---|---|---|
| **Ahdia Bacchus** | White | ♔ King e1 — passive identity, the prize | ♘ Knight b1 — active self | ♟ e-pawn — what she could become |
| **Firas Bacchus** | White | ♕ Queen d1 — the protagonist fakeout | ♖ Rook a1 — the crime-fighting self | ♟ f-pawn — the autoinjector |
| **Ruth Carter** | White | ♖ Rook h1 — field leader | ♗ Bishop f1 — the scientist | ♟ d-pawn — CR-7, the treatment |
| **Ryu Matsuda** | White/CADENS | ♘ Knight b1 — what he watches | ♟ f-pawn — what he is | ♔ King e1 — where he stands |
| **Ben Bukowski** | White | ♖ Rook a1 — combat self | ♟ b-pawn — discipline | ♗ Bishop c1 — precision |
| **Tess Whitford** | White | ♘ Knight g1 — the strike that costs itself | ♟ g-pawn — defender turned aggressor | ♟ h-pawn — the medication baseline |
| **Leah Turner** | White | ♗ Bishop f1 — quick deployment | ♟ d-pawn — first-swing aggression | ♟ c-pawn — over-extension |
| **Victor Hernandez** | White | ♗ Bishop c1 — the one ethical strike | ♟ a-pawn — community roots | ♞ **Black** Knight — the lost youth *(cross-faction)* |
| **Harriet Bourn** | White/CADENS | ♔ King e1 — the asset she authorized | ♕ Queen d1 — the doomed-status file | ♟ a-pawn — Mother FAERIS |
| **Harding Kain** | Black | ♚ King e8 — the public face | ♝ Bishop f8 — the Tank Cop | ♟ g-pawn — expendables |
| **Bellatrix** | Black | ♛ **Queen d8** — the orchestrator | *(held in reserve — no steward in Run 1)* | |

### Verified piece fates

Every triplet claim was checked against the actual game by tracking each piece's identity
from its starting square across all 271 plies. **The mapping holds up.**

| Piece | Owner | First move | Moves | Captures | Fate |
|---|---|---|---|---|---|
| ♘ b1 | Ahdia / Ryu | M10 | 25 | 2 (M11, M40) | **Survives** — plays `Ng7` at M136 |
| ♔ e1 | Ahdia / Ryu / Bourn | M5 | 17 | 1 | **Survives** on h4 |
| ♟ e2 | Ahdia | M29 | 4 | 0 | **Survives on e6** — e3(M29) → e4(M110) → e5(M129) → e6(M133). Never promotes |
| ♕ d1 | Firas / Bourn | M9 | 5 | 1 | Captured M26 by the h8 rook |
| ♖ a1 | Firas / Ben | M18 | 19 | **5 — most in the game** | Captured M80 by the Black King |
| ♟ f2 | Firas / Ryu | M59 | 3 | 0 | **Survives on f5** — never promotes |
| ♖ h1 | Ruth | M5 | **49** | 1 | **Survives** — takes the f8 bishop at M82 |
| ♗ f1 | Ruth / Leah | M4 | 1 | **0** | Captured M20 by the c8 bishop |
| ♟ d2 | Ruth / Leah | M1 | 2 | 1 (the game's first capture, M7) | Captured M7 |
| ♗ c1 | Ben / Victor | M16 | 2 | 1 (M17) | Captured M17 by the g7 pawn |
| ♟ b2 | Ben | M6 | 2 | 0 | Captured M39 by the Black Queen |
| ♘ g1 | Tess | M2 | 2 | 1 (M19) | Captured M19 by the f8 bishop |
| ♟ g2 | Tess | M3 | 2 | 1 (M114) | Captured M115 by the Black Queen |
| ♟ h2 | Tess | M30 | 1 | 0 | Captured M53 by the Black Queen, with check |
| ♟ c2 | Leah | M8 | 1 | 0 | Captured M8 — **a one-move lifespan** |
| ♟ a2 | Victor / Bourn | M14 | 1 | 0 | Captured M33 by the f8 bishop, after 19 moves untouched |
| ♚ e8 | Kain | M5 | 23 | 1 | **Survives** — resigns, never captured |
| ♝ f8 | Kain (the Tank) | M4 | 20 | 3 | Captured M82 by Ruth's h1 rook |
| ♟ g7 | Kain | M17 | 2 | 1 | Captured M79 by the a1 rook |
| ♛ d8 | Bellatrix | M9 | **68 — most active piece in the game** | 3 | **Survives** |
| ♟ f7 | *(unassigned)* | **never moves** | 0 | 0 | Captured M80 in its starting square — "the watcher" |

**The Black Queen never comes off the board.** The antagonist faction's real command node
plays more moves than any other piece, takes three of the Go Squad's pieces (Ben's
discipline at M39, Tess's baseline at M53, Tess's g-pawn at M115), and survives the loss
untouched — and she has no steward, so no one voices her. White wins the game; the
intelligence running Black walks away. That is the "loses the game, wins the war"
inversion sitting in the actual move data, not imposed on it.

---

## 3. The interpretive rules

Recovered by the blind agents from the beats alone, then confirmed against the ratified
files. These are the grammar that turns a chess event into a scene:

1. **Piece-fate ≠ character-fate.** A captured piece is a defeat of that *facet*, not a
   death. Leah loses her entire triplet by M20 and survives the book.
2. **The triplet is three scales of one self** — what others see, what the character does,
   what they could become.
3. **Move ownership.** Each steward owns a small set of numbered moves and writes only
   there, plus the convergence points. The rest of the game passes without them.
4. **Dormancy is latency; a piece's first move is character activation.** The e-pawn
   asleep 28 moves is Ahdia pre-activation; the f-pawn dormant 58 plies is CADENS coming
   online too late.
5. **Promotion = transcendence. Failure to promote = arrested transformation.** The two
   pawns frozen at e6 and f5 are the book's two near-transformations.
6. **Capture count and lifespan are characterization.** "Removed with zero captures to its
   name" is Leah's whole arc; a one-move lifespan is over-extension as a born trait.
7. **Shared pieces are read divergently, never identically** — and the characters are not
   permitted to know they share them.
8. **Cross-faction pieces are interpretive only.** Victor never moves the black knight he
   reads his grief through.
9. **The board image and the canonical mechanism can come apart.** At M82 the board says
   Ruth's rook captures; canon says Ahdia lands the blow in frozen time and Ruth's piece
   marks the *witnessing*. The gap is used deliberately to generate misattribution inside
   the fiction.
10. **Resignation ≠ mate, and the gap is plot.** The Black King is never captured, which is
    exactly why Kain clone-survives off-board.
11. **Quiet moves are mandatory beats.** Non-forcing stretches are assigned as endurance
    beats where the drama is that there is no drama.
12. **When every piece is spent, the character participates as hands.** Four stewards
    independently reached the climax with nothing on the board and wrote the same move.

### Convergence protocol

Three convergence points. Ahdia writes first; her beat is circulated as a
`convergence_M*_ahdia.md` extract; every other steward reads it and must **diverge** —
write their own tension, not an echo.

| CP | Move | Event | Stewards |
|---|---|---|---|
| **CP-1** | M26 `Qxc8 Rxc8` | The Queen falls — protagonist fakeout breaks; warehouse fire | Ahdia, Firas, Bourn, Kain |
| **CP-2** | M82 `Rxa7` | The Docks reveal — Ruth learns the truth | Ahdia, Ruth, Ryu, Kain |
| **CP-3** | M131–136 | The singularity / the finish — all hands | all ten |

---

## 4. Errors found

Verifying the mapping against the real game turned up three defects. All are in the
upstream scaffold, not introduced by the stewards.

**1. Victor's cross-faction piece is the wrong knight.** `BOOK1_TRIPLETS.md` assigns him
"Black Knight b8" as the lost youth and points it at the M17 capture. But the knight
captured at M17 by `Bxf6` started on **g8** — it played `1...Nf6` on the first move. The
actual b8 knight went `Nc6 / Nb4 / Nc6 / Nd4` and was captured at **M19 by Tess's g1
knight**. Victor's grief lens and Tess's one strike are pointed at swapped pieces. The
reading still works — "first Black piece to move, among the first taken" is true of the
g8 knight — but the label is wrong and should be corrected to **Black Knight g8** before
anything else is built on it.

**2. M20 is off by one ply.** The move map and four steward files write the fianchetto
bishop's fall as `M20 Bxg2 / Kxg2`. In the game White's 20th move is `Qa2`; `Bxg2` is
Black's 20th ply and `Kxg2` is White's **21st**. Harmless for narrative purposes, but it
means the compressed `M20 Bxg2/Kxg2` notation in the move map is not legal PGN, and any
tool that parses these strings will fail on them.

**3. M80 carries two contradictory ratified readings.** `BOOK1_TRIPLETS.md` gives the a1
rook to both Firas ("removal from active duty by injury, explicitly **NOT** a personal
Kain duel") and Ben ("a personal defeat **at Kain's hands**"). Same piece, same move,
mutually exclusive. Ben's steward noticed and deferred to the move map; Firas's steward
pre-empted it with a canon note. **This one needs a Director ruling** — it is the only
finding here that is an editorial question rather than a mechanical error.

Two smaller wobbles: Ruth's rook is credited with "11 late checks" and actually delivers
**10** (M81, 83, 87, 95, 96, 101, 107, 111, 127, 128). Ben's M6 beat describes `b3` as
"opening the long diagonal for the fianchetto," but no bishop ever occupies that diagonal
in this game — White plays `Qb2` at M13 instead.

---

## 5. Is the engine extractable from the steward work?

This was the actual experiment. Two agents attempted it blind. The answer splits cleanly
by layer.

| Layer | Recoverable? | Detail |
|---|---|---|
| **Game identity** | Yes — but by leak | `Ahdia_run1.md` names it in its header: *"Carlsen–Nepo 2021 G6 — 136 moves, White wins."* No inference required. Redacted, it would still be identifiable from the fingerprint alone (136 moves, decisive, `26. Qxc8 Rxc8`, final move `Ng7`) |
| **Interpretive rules** | **Yes, strongly** | Both blind agents independently recovered the full rule set above. The stewards restate the grammar from so many angles that it survives intact |
| **Piece→character map** | **Yes** | All sixteen White pieces have named owners recoverable from the outlines; shared and cross-faction mechanics are stated explicitly enough to reconstruct as rules |
| **Move sequence** | **No — about one third** | Only **45 of 136 moves** carry any notation anywhere in the ten outlines. Roughly 28% of plies |
| **Board positions** | **No** | Nothing after about M8 is reconstructable. Non-contiguous SAN, no castling record, no disambiguation for repeated rook moves, ~17 White-only plies with no Black reply |

**Verdict: the interpretation layer survives; the scaffold does not.** The steward outputs
are lossy in a specific and predictable direction — a steward records the moves it
personally owns and nothing else, so coverage collapses exactly where no character was
assigned. The move-by-move scaffold lives entirely upstream and cannot be back-derived
from the beats.

For the practical goal — using the engine to generate new writing assignments
independently — that is fine, because the upstream artifacts exist (`BOOK1_MOVE_MAP.md`,
`BOOK1_TRIPLETS.md`, `BOOK1_PAWN_ARCS.md`, the PGN). What this experiment establishes is
that **the four documents together are the engine, and the steward outputs are not a
substitute for them.** Losing the move map would cost roughly two thirds of the game.

---

## 6. What the matrix shows

58 anchored beats across 10 characters. Full data in
`data/beat_matrix.json`; rendered view in the accompanying HTML page.

**Coverage is barbell-shaped.** Beats cluster in M1–M40 and M100–M136. The stretches
M21–25, M41–52, M54–71, M89–99 and M116–130 have almost no beats from anyone — and this
tracks the game itself, which has only 2 captures between M41 and M78 and none at all
between M83 and M99. The scaffold under-serves the Grind because the *game* under-serves
the Grind.

**Stewards fill the gap unprompted.** Tess wrote a beat at M88 and Victor at M72 — neither
is in their assigned move list or in the move map. Both independently invented the same
kind of scene: endurance without event, attrition with no clash to mark it. That is the
strongest signal in the run that the Grind needs assigned beats rather than silence.

**Four stewards reach the finish with zero pieces on the board.** Ben, Tess, Leah and
Victor all read CP-3 through absence — "hands, not pieces." The rhyme is real and
load-bearing, but four characters narrating the same conceit will read as repetition
unless the blocking pass deliberately varies it.

**Silences worth noting.** Leah has no beat between M20 and M110 — ninety moves, which her
steward argues is the point. Ruth has nothing between M20 and M82, a 62-move gap covering
her entire "ahead of the team, behind the truth" buildup. Firas is absent M80–M116, which
is diegetically motivated: the board removed him.

---

## 7. Files

| File | Contents |
|---|---|
| `ENGINE_SPEC.md` | This document |
| `data/engine_ground_truth.json` | Per-ply board state for all 271 plies: FEN, SAN, mover, victim, check flag — plus per-piece provenance and fate for all 32 pieces |
| `data/beat_matrix.json` | The 58 anchored beats, move-indexed, with chess reading, narrative beat, convergence flags and source quotes |
| `data/build_engine_data.py` | Regenerates the ground truth from the PGN (requires `python-chess`) |

The board-position data is the one component of the engine that existed nowhere in the
repo before this experiment. Everything else was already documented; this pass verified
it and found the three errors above.
