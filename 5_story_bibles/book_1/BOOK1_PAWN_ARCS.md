# Book 1 Pawn Arcs — Carlsen-Nepo 2021 G6

**Source:** `6_manuscript/book_1/book1_chess_game.pgn`
**Generated:** 2026-05-19 (parsed from PGN via python-chess)
**Purpose:** Per-pawn arc dossier to complement the Chess Chronicles tool output, which excludes pawns and kings. Used by the Book 1 triplet system (see `BOOK1_TRIPLETS.md`).

---

## How to Read This File

Each pawn is tracked by its **starting square identity** (e.g., "White e-pawn (e2)"). Pawns are referenced by file letter throughout the rebuild — Ahdia's e-pawn, Firas's f-pawn, etc.

For each pawn:
- **Entry** = first move it makes (`M{n}`)
- **Exit** = how it leaves the game: captured, promoted, or survives to end
- **Path** = squares visited in order
- **Captures** = pieces this pawn took
- **Threats received** = ply-states under attack (rough pressure metric — not a count of distinct threats)
- **Checks given** = if this pawn delivered any checks
- **Witnesses** = major-piece capture events while this pawn was alive on the board

---

## Headline Findings

1. **No pawn promotes in this game.** White's e-pawn reaches e6 and f-pawn reaches f5, both poised to queen, but the mate falls before promotion. The Black pawns get to a3 and h4 but die before transformation. **Every pawn that "transcends" is frozen at the edge of transformation.** This shapes how Ahdia's e-pawn and Firas's f-pawn can be read.

2. **Black f7 never moves.** It is captured at M80 in its starting square. The piece that watches the entire game and is killed in its chair. 18 major-event witnesses — the highest of any pawn that took no action.

3. **White e-pawn endures 90 ply-states of threat** — the most-pressured pawn in the game. Dormant for 28 moves, then crawls e2 → e3 → e4 → e5 → e6 over 100+ moves while under constant attack.

4. **The fianchetto pawn (White g) makes a late kill.** g3 at M3 (the defensive fianchetto), then captures Black h-pawn at M114, then dies M115 to Black Queen. The defensive pawn becomes a killer right at the end and is immediately taken.

5. **One-move pawns exist on both sides.** White c-pawn: c4 at M8, dies M8. Black c-pawn: c5 at M6, dies M7. Black d-pawn captures White c-pawn at M8 then dies M11. These are the "swung once, taken" pawns.

---

## White Pawns

### White a-pawn (a2)
- **Entry:** M14
- **Exit:** Captured M33 by Black Bishop
- **Path:** a2 → a3
- **Captures:** 0
- **Threats received:** 21 ply-states
- **Witnesses (11 major):** M7, M11, M17, M19, M20, M21, M26 (Black Rook captured by White Queen), M29 (Black Rook captured by White Bishop), and the chain through M33.

### White b-pawn (b2)
- **Entry:** M6
- **Exit:** Captured M39 by Black Queen
- **Path:** b2 → b3 → b4
- **Captures:** 0
- **Threats received:** 20 ply-states
- **Witnesses (13 major)**

### White c-pawn (c2)
- **Entry:** M8
- **Exit:** **Captured M8** by Black d-pawn (same move — one-move lifespan)
- **Path:** c2 → c4
- **Captures:** 0
- **Threats received:** 1 ply-state
- **Witnesses (1):** M7

### White d-pawn (d2)
- **Entry:** M1 (1. d4 — the game's opening move)
- **Exit:** Captured M7 by Black Bishop
- **Path:** d2 → d4 → c5
- **Captures (1):** M7: Black c-pawn (the d-pawn captures c5 by `dxc5`, then is itself recaptured `Bxc5` same move)
- **Threats received:** 2 ply-states

### White e-pawn (e2)
- **Entry:** M29 (dormant 28 moves)
- **Exit:** **Survives** (final square: e6)
- **Path:** e2 → e3 → e4 → e5 → e6
- **Captures:** 0
- **Threats received:** **90 ply-states** (most-pressured pawn in the game)
- **Witnesses (22 major)** — present for most of the game's significant exchanges from M29 onward

### White f-pawn (f2)
- **Entry:** M59 (dormant 58 moves)
- **Exit:** **Survives** (final square: f5)
- **Path:** f2 → f3 → f4 → f5
- **Captures:** 0
- **Threats received:** 61 ply-states
- **Witnesses (22 major)**

### White g-pawn (g2)
- **Entry:** M3 (3. g3 — the fianchetto)
- **Exit:** Captured M115 by Black Queen (one move after its own kill)
- **Path:** g2 → g3 → h4
- **Captures (1):** **M114: Black h-pawn** (`gxh4`)
- **Threats received:** 34 ply-states
- **Witnesses (21 major)**

### White h-pawn (h2)
- **Entry:** M30
- **Exit:** Captured M53 by Black Queen
- **Path:** h2 → h4
- **Captures:** 0
- **Threats received:** 2 ply-states
- **Witnesses (16 major)**

---

## Black Pawns

### Black a-pawn (a7)
- **Entry:** M23
- **Exit:** Captured M53 by White Rook
- **Path:** a7 → a5 → a4 → a3
- **Captures:** 0
- **Threats received:** 21 ply-states
- **Witnesses (15 major):** Long arc through opening and middlegame captures

### Black b-pawn (b7)
- **Entry:** M11
- **Exit:** Captured M34 by White Rook
- **Path:** b7 → b5
- **Captures:** 0
- **Threats received:** 5 ply-states
- **Witnesses (12 major)**

### Black c-pawn (c7)
- **Entry:** M6 (6...c5)
- **Exit:** **Captured M7** by White d-pawn
- **Path:** c7 → c5
- **Captures:** 0
- **Threats received:** 1 ply-state

### Black d-pawn (d7)
- **Entry:** M2
- **Exit:** Captured M11 by White Knight
- **Path:** d7 → d5 → c4
- **Captures (1):** M8: White c-pawn (`dxc4`)
- **Threats received:** 8 ply-states
- **Witnesses (1):** M7

### Black e-pawn (e7)
- **Entry:** M3
- **Exit:** Captured M40 by White Knight
- **Path:** e7 → e6 → e5 → e4
- **Captures:** 0
- **Threats received:** 10 ply-states
- **Witnesses (14 major)**

### Black f-pawn (f7)
- **Entry:** **Never moves**
- **Exit:** Captured M80 by White Rook (in its starting square)
- **Path:** f7 (only)
- **Captures:** 0
- **Threats received:** 12 ply-states
- **Witnesses (18 major)** — the watcher killed in their chair

### Black g-pawn (g7)
- **Entry:** M17 (17...gxf6)
- **Exit:** Captured M79 by White Rook
- **Path:** g7 → f6 → f5
- **Captures (1):** **M17: White Bishop** (the only Black pawn that captures a major piece)
- **Threats received:** 19 ply-states
- **Witnesses (16 major)**

### Black h-pawn (h7)
- **Entry:** M30
- **Exit:** **Captured M114 by White g-pawn** (the M114/M115 mutual destruction)
- **Path:** h7 → h5 → h4
- **Captures:** 0
- **Threats received:** 33 ply-states
- **Witnesses (21 major)**

---

## Pawn Capture Pairs (Mutual Exchanges)

| Move | White piece | Black piece | Note |
|---|---|---|---|
| M7 | White d-pawn captures Black c-pawn | Black Bishop captures White d-pawn (same ply) | The first capture in the game; initiates middlegame |
| M8 | White c-pawn (one move only) | Black d-pawn captures White c-pawn | Black d-pawn then dies M11 to White Knight |
| M114–M115 | White g-pawn captures Black h-pawn | Black Queen captures White g-pawn | The final pawn exchange before checkmate cascade |

---

## Survivors at Game End

| Piece | Final square | Role |
|---|---|---|
| White e-pawn | e6 | Frozen at edge of transformation (Ahdia's transcendence lens) |
| White f-pawn | f5 | One square from queening (Firas's autoinjector / Ryu's CADENS lens) |

These two pawns reach the climax alive but never promote. The game ends with both still on the board, threatening to queen but never doing so.

---

## Pawn → Character Triplet Index

For reference (see `BOOK1_TRIPLETS.md` for full triplet specifications):

| Pawn | Triplets it appears in | Reading |
|---|---|---|
| White e-pawn | Ahdia | Transcendence pawn (dormant → late march to 6th rank, never queens) |
| White f-pawn | Firas, Ryu | Firas: autoinjector. Ryu: slow CADENS advance. |
| White d-pawn | Ruth, Leah | Ruth: CR-7 treatment. Leah: first-swing aggression. |
| White c-pawn | Leah | Over-extension (one-move life) |
| White b-pawn | Ben | Structural discipline broken by pressure |
| White a-pawn | Victor, Bourn | Victor: community roots. Bourn: Mother FAERIS exploitation. |
| White g-pawn | Tess | Fianchetto defender that becomes a killer late (vigilante seed) |
| White h-pawn | Tess | Depression/medication baseline |
| Black f-pawn (f7, never moves) | Bourn (alternate) | Institutional observer killed in their chair |
| Black g-pawn | Kain | First-tier expendables (captures White Bishop M17 = takes out Victor) |

---

*Generated from PGN by direct parse. The Chess Chronicles tool excluded pawns entirely — this file restores them.*
