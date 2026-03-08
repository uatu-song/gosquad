# Chess Narrative Engine - Technical Specification

**Version:** 1.0 (Planning Document)
**Created:** 2026-01-22
**Purpose:** Foundation document for building a professional chess-to-narrative mapping engine using Stockfish WASM.

---

## Table of Contents

1. [Chess.js Library Primer](#1-chessjs-library-primer)
2. [Stockfish WASM Deep Dive](#2-stockfish-wasm-deep-dive)
3. [Integration Architecture Spec](#3-integration-architecture-spec)
4. [Narrative Mapping Schema](#4-narrative-mapping-schema)
5. [Implementation Roadmap](#5-implementation-roadmap)

---

## 1. Chess.js Library Primer

### What It Does

Chess.js is a JavaScript library for chess move generation, validation, and PGN parsing. It handles all the chess rules so you don't have to implement them yourself.

**Key capabilities:**
- Parse PGN notation into move sequences
- Validate legal moves
- Track board state through a game
- Generate FEN strings for any position
- Detect check, checkmate, stalemate, draw conditions
- Convert between SAN (Nf3) and UCI (g1f3) notation

### Installation

```bash
# npm
npm install chess.js

# CDN (no build tools)
<script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.13.4/chess.min.js"></script>
```

**Note:** As of 2024, chess.js v1.0+ uses ES modules. For simple HTML files without bundlers, use v0.13.4 or load as ES module.

### Key Methods

#### Creating a Game Instance

```javascript
// Start from initial position
const chess = new Chess();

// Start from specific FEN
const chess = new Chess('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1');
```

#### Loading a PGN

```javascript
const pgn = `[Event "Example"]
[White "Player1"]
[Black "Player2"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6`;

const chess = new Chess();
chess.loadPgn(pgn);

// Access move history
const moves = chess.history();
// → ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6"]

// Access with detailed info
const detailedMoves = chess.history({ verbose: true });
// → [{ color: 'w', from: 'e2', to: 'e4', piece: 'p', san: 'e4', ... }, ...]
```

#### Getting FEN at Any Position

```javascript
const chess = new Chess();
chess.loadPgn('1. e4 e5 2. Nf3 Nc6');

// Current position FEN
const fen = chess.fen();
// → "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
```

#### Replaying Moves (For Per-Position Analysis)

```javascript
const pgn = '1. e4 e5 2. Nf3 Nc6 3. Bb5';
const chess = new Chess();
chess.loadPgn(pgn);
const moves = chess.history({ verbose: true });

// Reset and replay to get FEN at each position
const replay = new Chess();
const positions = [{ fen: replay.fen(), move: null }]; // Starting position

for (const move of moves) {
  replay.move(move.san);
  positions.push({
    fen: replay.fen(),
    move: move,
    uci: move.from + move.to + (move.promotion || '') // UCI format for Stockfish
  });
}
```

#### Converting SAN to UCI

Stockfish uses UCI notation (e2e4), PGN uses SAN (e4). Chess.js verbose history gives you both:

```javascript
const move = chess.move('Nf3'); // Returns detailed move object
// move.from = 'g1'
// move.to = 'f3'
// UCI format = 'g1f3'

// For promotions:
const promoMove = chess.move('e8=Q');
// UCI format = 'e7e8q' (lowercase promotion piece)
```

#### Game State Detection

```javascript
chess.isCheck();        // Is current player in check?
chess.isCheckmate();    // Is it checkmate?
chess.isStalemate();    // Is it stalemate?
chess.isDraw();         // Is it a draw? (stalemate, insufficient material, 50-move, threefold)
chess.isGameOver();     // Is the game over?
chess.turn();           // 'w' or 'b'
```

#### Board State Access

```javascript
// Get piece at square
const piece = chess.get('e4');
// → { type: 'p', color: 'w' } or null

// Get all pieces
const board = chess.board();
// → 8x8 array of pieces or null
```

### Example: Full PGN Parsing Workflow

```javascript
function parsePgnToPositions(pgnString) {
  const chess = new Chess();

  // Load and extract moves
  chess.loadPgn(pgnString);
  const moves = chess.history({ verbose: true });

  // Replay to capture each position
  const replay = new Chess();
  const positions = [{
    moveNumber: 0,
    fen: replay.fen(),
    san: null,
    uci: null,
    turn: 'w',
    isCheck: false,
    isCheckmate: false
  }];

  moves.forEach((move, index) => {
    replay.move(move.san);
    positions.push({
      moveNumber: index + 1,
      fen: replay.fen(),
      san: move.san,
      uci: move.from + move.to + (move.promotion || ''),
      turn: replay.turn(),
      isCheck: replay.isCheck(),
      isCheckmate: replay.isCheckmate(),
      capturedPiece: move.captured || null,
      piece: move.piece,
      from: move.from,
      to: move.to
    });
  });

  return positions;
}
```

---

## 2. Stockfish WASM Deep Dive

### UCI Protocol Basics

UCI (Universal Chess Interface) is a text-based protocol. You send command strings, receive response strings.

#### Initialization Sequence

```
→ uci                          # Request UCI mode
← id name Stockfish 16         # Engine identifies itself
← id author T. Romstad, etc.
← option name Hash type spin default 16 min 1 max 33554432
← option name Threads type spin default 1 min 1 max 1024
← ... more options ...
← uciok                        # Ready for commands

→ setoption name Hash value 256    # Configure hash table (MB)
→ setoption name Threads value 1   # Single thread (WASM limitation without SharedArrayBuffer)
→ isready                          # Confirm ready
← readyok                          # Engine is ready
```

#### Setting a Position

```
# From starting position
→ position startpos

# From starting position with moves played
→ position startpos moves e2e4 e7e5 g1f3 b8c6

# From FEN
→ position fen rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1

# From FEN with subsequent moves
→ position fen <fen> moves g8f6 b1c3
```

**Important:** UCI uses long algebraic notation (from-square + to-square):
- `e2e4` not `e4`
- `g1f3` not `Nf3`
- `e7e8q` for pawn promotion to queen

#### Requesting Analysis

```
# Depth-limited (most predictable for batch analysis)
→ go depth 15

# Time-limited
→ go movetime 5000       # 5 seconds

# Infinite (requires manual stop)
→ go infinite
→ stop                   # When you want results

# With specific position constraints
→ go depth 20 searchmoves e2e4 d2d4   # Only analyze these moves
```

#### Response Format

During analysis, Stockfish streams `info` lines:

```
← info depth 1 seldepth 1 score cp 20 nodes 20 nps 10000 time 2 pv e2e4
← info depth 2 seldepth 2 score cp 15 nodes 58 nps 29000 time 2 pv e2e4 e7e5
← info depth 3 seldepth 4 score cp 25 nodes 182 nps 91000 time 2 pv e2e4 e7e5 g1f3
...
← info depth 15 seldepth 22 score cp 31 nodes 284920 nps 1892133 time 151 pv e2e4 e7e5 g1f3 b8c6 f1b5
← bestmove e2e4 ponder e7e5
```

**Info line fields:**

| Field | Description |
|-------|-------------|
| `depth N` | Current search depth (plies) |
| `seldepth N` | Selective search depth (deeper in some lines) |
| `score cp N` | Centipawn evaluation (100 = 1 pawn) |
| `score mate N` | Forced mate in N moves (positive = engine mates, negative = engine gets mated) |
| `nodes N` | Positions evaluated |
| `nps N` | Nodes per second |
| `time N` | Time spent (ms) |
| `pv move1 move2...` | Principal variation (best line) |
| `multipv N` | Which line (if analyzing multiple) |

**Bestmove line:**
```
bestmove e2e4 ponder e7e5
```
- `bestmove`: The recommended move
- `ponder`: Expected opponent reply (for pondering, not needed for analysis)

### NPM Package and Initialization

**Recommended package:** `stockfish` (official npm package)

```bash
npm install stockfish
```

**CDN for no-build-tools approach:**
```html
<script src="https://cdn.jsdelivr.net/npm/stockfish@16/src/stockfish-nnue-16.js"></script>
```

#### Web Worker Setup

**stockfish-worker.js:**
```javascript
// Load Stockfish WASM
importScripts('https://cdn.jsdelivr.net/npm/stockfish@16/src/stockfish-nnue-16.js');

// Initialize engine
const stockfish = STOCKFISH();

// Forward engine output to main thread
stockfish.onmessage = function(line) {
  self.postMessage({ type: 'engine-output', data: line });
};

// Listen for commands from main thread
self.onmessage = function(e) {
  if (e.data.type === 'command') {
    stockfish.postMessage(e.data.command);
  }
};

// Signal ready
self.postMessage({ type: 'worker-ready' });
```

**main.js - Engine wrapper class:**
```javascript
class StockfishEngine {
  constructor() {
    this.worker = null;
    this.ready = false;
    this.messageHandlers = [];
  }

  async init() {
    return new Promise((resolve, reject) => {
      this.worker = new Worker('stockfish-worker.js');

      this.worker.onmessage = (e) => {
        if (e.data.type === 'worker-ready') {
          this.initUCI().then(resolve);
        } else if (e.data.type === 'engine-output') {
          this.handleMessage(e.data.data);
        }
      };

      this.worker.onerror = reject;
    });
  }

  async initUCI() {
    await this.sendAndWait('uci', 'uciok');
    this.send('setoption name Hash value 256');
    await this.sendAndWait('isready', 'readyok');
    this.ready = true;
  }

  send(command) {
    this.worker.postMessage({ type: 'command', command });
  }

  handleMessage(line) {
    this.messageHandlers.forEach(handler => handler(line));
  }

  onMessage(handler) {
    this.messageHandlers.push(handler);
    return () => {
      this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
    };
  }

  sendAndWait(command, waitFor) {
    return new Promise((resolve) => {
      const unsubscribe = this.onMessage((line) => {
        if (line.startsWith(waitFor) || line === waitFor) {
          unsubscribe();
          resolve(line);
        }
      });
      this.send(command);
    });
  }

  async analyze(fen, depth = 15) {
    const result = {
      depth: 0,
      score: null,
      scoreType: null,
      pv: [],
      bestmove: null
    };

    return new Promise((resolve) => {
      const unsubscribe = this.onMessage((line) => {
        if (line.startsWith('info depth')) {
          const parsed = this.parseInfo(line);
          if (parsed.depth > result.depth) {
            Object.assign(result, parsed);
          }
        } else if (line.startsWith('bestmove')) {
          result.bestmove = line.split(' ')[1];
          unsubscribe();
          resolve(result);
        }
      });

      this.send(`position fen ${fen}`);
      this.send(`go depth ${depth}`);
    });
  }

  parseInfo(line) {
    const info = {};

    const depthMatch = line.match(/depth (\d+)/);
    if (depthMatch) info.depth = parseInt(depthMatch[1]);

    const cpMatch = line.match(/score cp (-?\d+)/);
    const mateMatch = line.match(/score mate (-?\d+)/);

    if (cpMatch) {
      info.score = parseInt(cpMatch[1]);
      info.scoreType = 'cp';
    } else if (mateMatch) {
      info.score = parseInt(mateMatch[1]);
      info.scoreType = 'mate';
    }

    const pvMatch = line.match(/ pv (.+)$/);
    if (pvMatch) {
      info.pv = pvMatch[1].split(' ');
    }

    return info;
  }

  destroy() {
    if (this.worker) {
      this.worker.terminate();
      this.worker = null;
    }
  }
}
```

### Single Position Analysis Example

```javascript
async function analyzePosition() {
  const engine = new StockfishEngine();
  await engine.init();

  const fen = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1';
  const result = await engine.analyze(fen, 15);

  console.log('Best move:', result.bestmove);
  console.log('Evaluation:', result.scoreType === 'cp'
    ? (result.score / 100).toFixed(2) + ' pawns'
    : 'Mate in ' + Math.abs(result.score));
  console.log('Best line:', result.pv.join(' '));

  engine.destroy();
}
```

### Response Data Structures

**Raw info line:**
```
info depth 15 seldepth 22 multipv 1 score cp 35 nodes 284920 nps 1892133 time 151 pv g1f3 b8c6 f1b5
```

**Parsed result object:**
```javascript
{
  depth: 15,
  score: 35,           // Centipawns (or mate distance if scoreType='mate')
  scoreType: 'cp',     // 'cp' or 'mate'
  pv: ['g1f3', 'b8c6', 'f1b5'],
  bestmove: 'g1f3'
}
```

**Normalized for narrative use:**
```javascript
{
  depth: 15,
  evalCentipawns: 35,
  evalPawns: 0.35,
  isMate: false,
  mateIn: null,
  bestMove: 'g1f3',
  bestLine: ['g1f3', 'b8c6', 'f1b5'],
  whiteAdvantage: true  // Derived: score > 0
}
```

---

## 3. Integration Architecture Spec

### Proposed File Structure

```
chess-narrative-engine/
├── index.html                    # Main UI
├── css/
│   └── styles.css               # Styling
├── js/
│   ├── main.js                  # App entry point, UI logic
│   ├── chess-parser.js          # PGN parsing, position tracking (uses chess.js)
│   ├── stockfish-engine.js      # Stockfish WASM wrapper
│   ├── pattern-detector.js      # Tactical pattern detection (fork, pin, etc.)
│   ├── narrative-mapper.js      # Chess events → Story beats mapping
│   └── utils.js                 # Shared utilities
├── workers/
│   └── stockfish-worker.js      # Web Worker for Stockfish
├── data/
│   ├── narrative-rules.json     # Mapping rules configuration
│   └── genre-tropes.json        # Genre-specific trope database
└── lib/
    └── chess.min.js             # Chess.js library (if not using CDN)
```

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INPUT                                      │
│                                                                             │
│    PGN Text                    Genre Selection         Story Context        │
│       │                              │                      │               │
└───────┼──────────────────────────────┼──────────────────────┼───────────────┘
        │                              │                      │
        ▼                              │                      │
┌───────────────────┐                  │                      │
│   chess-parser.js │                  │                      │
│                   │                  │                      │
│ • Load PGN        │                  │                      │
│ • Extract moves   │                  │                      │
│ • Generate FENs   │                  │                      │
│ • Convert to UCI  │                  │                      │
└─────────┬─────────┘                  │                      │
          │                            │                      │
          │ positions[]                │                      │
          ▼                            │                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ANALYSIS LAYER                                       │
│                                                                             │
│  ┌────────────────────────┐         ┌────────────────────────┐             │
│  │  stockfish-engine.js   │         │  pattern-detector.js   │             │
│  │                        │         │                        │             │
│  │  For each position:    │         │  For each position:    │             │
│  │  • Send FEN            │         │  • Analyze board       │             │
│  │  • Get eval (cp/mate)  │         │  • Detect tactics:     │             │
│  │  • Get best move       │         │    - Fork              │             │
│  │  • Get best line (PV)  │         │    - Pin               │             │
│  │                        │         │    - Skewer            │             │
│  │  Returns:              │         │    - Discovery         │             │
│  │  • evalCentipawns      │         │    - Sacrifice         │             │
│  │  • isMate / mateIn     │         │    - etc.              │             │
│  │  • bestMove            │         │                        │             │
│  └───────────┬────────────┘         └───────────┬────────────┘             │
│              │                                   │                          │
│              │ engineAnalysis[]                  │ patternAnalysis[]        │
│              │                                   │                          │
│              └─────────────┬─────────────────────┘                          │
│                            │                                                │
│                            ▼                                                │
│               ┌────────────────────────┐                                    │
│               │     MERGE & ENRICH     │                                    │
│               │                        │                                    │
│               │ • Combine eval + tactic│                                    │
│               │ • Calculate eval swing │                                    │
│               │ • Detect turning points│                                    │
│               │ • Flag dramatic moments│                                    │
│               └───────────┬────────────┘                                    │
│                           │                                                 │
│                           │ analyzedPositions[]                             │
│                           │                                                 │
└───────────────────────────┼─────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       NARRATIVE MAPPING LAYER                                │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    narrative-mapper.js                              │    │
│  │                                                                     │    │
│  │   Inputs:                        Outputs:                          │    │
│  │   • analyzedPositions[]          • storyBeats[]                    │    │
│  │   • narrativeRules               • plotStructure                   │    │
│  │   • genreTropes                  • characterMoments                │    │
│  │   • storyContext                 • dramaticArcs                    │    │
│  │                                                                     │    │
│  │   Process:                                                          │    │
│  │   1. Identify game phases (opening/middle/end)                     │    │
│  │   2. Map eval swings to dramatic beats                             │    │
│  │   3. Map tactics to plot events                                    │    │
│  │   4. Apply genre-specific trope selection                          │    │
│  │   5. Build narrative arc structure                                 │    │
│  │                                                                     │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                            │
                            │ narrativeOutput
                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OUTPUT / UI                                     │
│                                                                             │
│   • Beat sheet (move-by-move story prompts)                                 │
│   • Plot structure visualization                                            │
│   • Dramatic moment highlights                                              │
│   • Export options (JSON, Markdown, etc.)                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Analyzed Position Data Shape

Each position in the game produces this data structure:

```typescript
interface AnalyzedPosition {
  // === POSITION IDENTIFICATION ===
  moveNumber: number;           // 1, 2, 3... (half-moves from start)
  ply: number;                  // Same as moveNumber (chess term)
  fen: string;                  // Full FEN string
  turn: 'w' | 'b';             // Whose turn AFTER this move

  // === MOVE INFORMATION ===
  move: {
    san: string;               // "Nf3", "exd5", "O-O"
    uci: string;               // "g1f3", "e4d5", "e1g1"
    piece: string;             // 'p', 'n', 'b', 'r', 'q', 'k'
    from: string;              // "g1"
    to: string;                // "f3"
    captured: string | null;   // 'p', 'n', etc. or null
    promotion: string | null;  // 'q', 'r', 'b', 'n' or null
  } | null;                    // null for starting position

  // === GAME STATE ===
  isCheck: boolean;
  isCheckmate: boolean;
  isStalemate: boolean;
  isDraw: boolean;

  // === STOCKFISH EVALUATION ===
  engine: {
    depth: number;             // Search depth achieved
    evalCentipawns: number;    // Raw centipawn score (+ = white better)
    evalPawns: number;         // evalCentipawns / 100
    isMate: boolean;           // Is this a forced mate?
    mateIn: number | null;     // Moves to mate (+ = white mates, - = black mates)
    bestMove: string;          // UCI notation
    bestLine: string[];        // Principal variation
  };

  // === EVAL DYNAMICS ===
  dynamics: {
    evalDelta: number;              // Change from previous position (centipawns)
    evalDeltaPawns: number;         // evalDelta / 100
    isBlunder: boolean;             // evalDelta magnitude > 200 (bad for mover)
    isMistake: boolean;             // evalDelta magnitude 100-200 (bad for mover)
    isInaccuracy: boolean;          // evalDelta magnitude 50-100 (bad for mover)
    isBrilliant: boolean;           // Large positive swing + non-obvious
    isTurningPoint: boolean;        // Eval sign changed
    momentumShift: 'none' | 'slight' | 'moderate' | 'major' | 'decisive';
  };

  // === PATTERN DETECTION ===
  tactics: {
    detected: TacticType[];         // ['fork', 'check']
    fork: ForkInfo | null;
    pin: PinInfo | null;
    skewer: SkewerInfo | null;
    discoveredAttack: DiscoveryInfo | null;
    discoveredCheck: boolean;
    doubleCheck: boolean;
    battery: BatteryInfo | null;
    sacrifice: SacrificeInfo | null;
  };

  // === POSITIONAL CATEGORY ===
  category: {
    primary: PositionCategory;      // 'development', 'threat', 'advance', etc.
    isCapture: boolean;
    isCastling: boolean;
    isPromotion: boolean;
  };

  // === GAME PHASE ===
  phase: 'opening' | 'middlegame' | 'endgame';
}

// Supporting types
type TacticType = 'fork' | 'pin' | 'skewer' | 'discoveredAttack' | 'discoveredCheck' |
                  'doubleCheck' | 'battery' | 'sacrifice' | 'check' | 'checkmate';

type PositionCategory = 'development' | 'advance' | 'retreat' | 'threat' |
                        'convergence' | 'defense' | 'exchange' | 'winningCapture' |
                        'reposition' | 'castling';

interface ForkInfo {
  attacker: string;           // Piece type doing the forking
  targets: string[];          // Piece types being forked
  squares: string[];          // Squares of forked pieces
}

interface PinInfo {
  pinner: string;             // Piece creating the pin
  pinned: string;             // Piece that is pinned
  pinnedTo: string;           // Piece behind (usually king or queen)
}

interface SkewerInfo {
  attacker: string;
  front: string;              // More valuable piece in front
  back: string;               // Less valuable piece behind
}

interface SacrificeInfo {
  sacrificed: string;         // Piece given up
  captured: string;           // Piece taken in exchange
  materialDelta: number;      // Negative = material given up
}
```

### How Pattern Detection and Stockfish Data Merge

```javascript
async function analyzeGame(pgn, options = { depth: 15 }) {
  // Step 1: Parse PGN into positions
  const positions = parsePgnToPositions(pgn);

  // Step 2: Initialize Stockfish
  const engine = new StockfishEngine();
  await engine.init();

  // Step 3: Analyze each position
  const analyzed = [];
  let prevEval = 0;

  for (let i = 0; i < positions.length; i++) {
    const pos = positions[i];

    // Get Stockfish evaluation
    const engineResult = await engine.analyze(pos.fen, options.depth);

    // Get pattern detection
    const patterns = detectPatterns(pos, positions[i - 1] || null);

    // Calculate dynamics
    const currentEval = engineResult.isMate
      ? (engineResult.mateIn > 0 ? 10000 : -10000)
      : engineResult.score;

    const evalDelta = i === 0 ? 0 : currentEval - prevEval;
    const wasMoversMove = i > 0 && (i % 2 === 1 ? 'w' : 'b') === positions[i-1].turn;

    // Merge all data
    analyzed.push({
      ...pos,
      engine: {
        depth: engineResult.depth,
        evalCentipawns: engineResult.score,
        evalPawns: engineResult.score / 100,
        isMate: engineResult.scoreType === 'mate',
        mateIn: engineResult.scoreType === 'mate' ? engineResult.score : null,
        bestMove: engineResult.bestmove,
        bestLine: engineResult.pv
      },
      dynamics: computeDynamics(evalDelta, prevEval, currentEval, wasMoversMove),
      tactics: patterns.tactics,
      category: patterns.category,
      phase: detectPhase(i, positions.length, pos)
    });

    prevEval = currentEval;

    // Progress callback
    if (options.onProgress) {
      options.onProgress(i + 1, positions.length);
    }
  }

  engine.destroy();
  return analyzed;
}

function computeDynamics(evalDelta, prevEval, currentEval, wasMoversMove) {
  const absDelta = Math.abs(evalDelta);

  // Determine if this was good or bad for the mover
  // (positive delta = good for white, negative = good for black)
  const goodForMover = wasMoversMove
    ? (evalDelta > 0 === (prevEval >= 0))  // Simplified; real logic more complex
    : true;

  return {
    evalDelta,
    evalDeltaPawns: evalDelta / 100,
    isBlunder: absDelta > 200 && !goodForMover,
    isMistake: absDelta > 100 && absDelta <= 200 && !goodForMover,
    isInaccuracy: absDelta > 50 && absDelta <= 100 && !goodForMover,
    isBrilliant: absDelta > 100 && goodForMover, // Simplified
    isTurningPoint: (prevEval > 0) !== (currentEval > 0),
    momentumShift: categorizeMomentum(absDelta)
  };
}

function categorizeMomentum(absDelta) {
  if (absDelta < 20) return 'none';
  if (absDelta < 50) return 'slight';
  if (absDelta < 100) return 'moderate';
  if (absDelta < 200) return 'major';
  return 'decisive';
}
```

---

## 4. Narrative Mapping Schema

### Categories of Chess Events → Story Beats

#### Tier 1: Evaluation-Based Events (From Stockfish)

| Chess Event | Detection | Narrative Beat |
|------------|-----------|----------------|
| **Blunder** | evalDelta > 200cp against mover | Character makes critical mistake |
| **Brilliant Move** | evalDelta > 100cp, non-obvious | Character finds hidden solution |
| **Turning Point** | Eval sign flips (+ to - or vice versa) | Power dynamic reverses |
| **Crushing Advantage** | Eval reaches ±300cp | One side gains decisive upper hand |
| **Mate Threat Emerges** | First `score mate N` appears | Climax approaching |
| **Checkmate** | Game ends in mate | Resolution / Climax |
| **Stalemate** | Game ends in stalemate | Pyrrhic victory / Tragic draw |

#### Tier 2: Tactical Events (From Pattern Detection)

| Chess Event | Narrative Beat |
|------------|----------------|
| **Fork** | Character creates impossible choice for opponent |
| **Pin** | Character is frozen, paralyzed by circumstances |
| **Skewer** | Attacking the shield exposes the real target |
| **Discovered Attack** | Hidden threat revealed through misdirection |
| **Double Check** | Overwhelming assault from multiple angles |
| **Sacrifice** | Character pays a price for strategic advantage |
| **Piece Captured** | Loss / defeat of a character element |

#### Tier 3: Positional Events (From Category Detection)

| Chess Event | Narrative Beat |
|------------|----------------|
| **Development** | Character enters the conflict / takes position |
| **Advance** | Pushing into enemy territory, escalation |
| **Retreat** | Pulling back, regrouping, loss of ground |
| **Castling** | Seeking safety, defensive consolidation |
| **Promotion** | Transformation, character reaches full potential |
| **Exchange** | Mutual sacrifice, neither side gains |

#### Tier 4: Phase Events (From Game Structure)

| Chess Event | Narrative Beat |
|------------|----------------|
| **Opening → Middlegame** | Exposition complete, conflict begins |
| **Middlegame → Endgame** | Core conflict resolves, denouement begins |
| **First Check** | First direct confrontation |
| **First Capture** | First casualty, stakes become real |

### Proposed Mapping Rules Structure

```json
{
  "version": "1.0",
  "rules": [
    {
      "id": "blunder_to_mistake",
      "priority": 100,
      "conditions": {
        "dynamics.isBlunder": true
      },
      "output": {
        "beatType": "character_mistake",
        "intensity": "high",
        "description": "A critical error with serious consequences"
      }
    },
    {
      "id": "sacrifice_with_advantage",
      "priority": 90,
      "conditions": {
        "tactics.sacrifice": { "$exists": true },
        "dynamics.evalDelta": { "$gt": 50 }
      },
      "output": {
        "beatType": "heroic_sacrifice",
        "intensity": "high",
        "description": "Giving something up leads to unexpected advantage"
      }
    },
    {
      "id": "sacrifice_losing",
      "priority": 90,
      "conditions": {
        "tactics.sacrifice": { "$exists": true },
        "dynamics.evalDelta": { "$lt": -50 }
      },
      "output": {
        "beatType": "desperate_gambit",
        "intensity": "high",
        "description": "A sacrifice that doesn't pay off - desperation"
      }
    },
    {
      "id": "fork_creates_dilemma",
      "priority": 80,
      "conditions": {
        "tactics.fork": { "$exists": true }
      },
      "output": {
        "beatType": "impossible_choice",
        "intensity": "medium",
        "description": "Character must choose what to save"
      }
    },
    {
      "id": "turning_point",
      "priority": 95,
      "conditions": {
        "dynamics.isTurningPoint": true
      },
      "output": {
        "beatType": "reversal",
        "intensity": "high",
        "description": "The tide turns - who was winning is now losing"
      }
    },
    {
      "id": "mate_approaching",
      "priority": 100,
      "conditions": {
        "engine.isMate": true,
        "engine.mateIn": { "$lte": 5, "$gt": 0 }
      },
      "output": {
        "beatType": "climax_approaching",
        "intensity": "very_high",
        "description": "Endgame is in sight - victory is near"
      }
    }
  ]
}
```

### Example Mapping: Dramatic Reversal

**Chess situation:**
- Move 23: White plays Nxf7 (sacrifice)
- Previous eval: +0.52 (slight white advantage)
- New eval: +4.21 (winning for white)
- Tactics detected: sacrifice, fork (attacks king and queen)

**Analyzed position data:**
```javascript
{
  moveNumber: 23,
  move: { san: 'Nxf7', piece: 'n', captured: 'p' },
  engine: { evalCentipawns: 421, isMate: false },
  dynamics: {
    evalDelta: 369,
    isBlunder: false,  // Good for white, who played it
    isBrilliant: true,
    momentumShift: 'decisive'
  },
  tactics: {
    detected: ['sacrifice', 'fork'],
    sacrifice: { sacrificed: 'n', captured: 'p', materialDelta: -2 },
    fork: { attacker: 'n', targets: ['k', 'q'], squares: ['e8', 'd8'] }
  }
}
```

**Narrative mapping output:**
```javascript
{
  beatType: 'brilliant_sacrifice',
  intensity: 'very_high',
  description: 'A knight sacrifice that forks the king and queen',
  narrativePrompt: 'The sacrifice seemed reckless, but it revealed a devastating double threat. The opponent must choose: save the leader or the strongest ally.',
  genreTropes: {
    battle: 'The Feint That Won the War',
    mystery: 'The Hidden Connection',
    sports: 'The Impossible Play'
  }
}
```

### Intensity Levels

| Level | evalDelta Range | Narrative Weight |
|-------|-----------------|------------------|
| `minimal` | 0-20cp | Background action, normal play |
| `low` | 20-50cp | Minor development, slight tension |
| `medium` | 50-100cp | Significant moment, rising tension |
| `high` | 100-200cp | Major event, key plot point |
| `very_high` | 200cp+ or mate threat | Climactic moment, turning point |

---

## 5. Implementation Roadmap

### Phase 1: Foundation
- [ ] Set up project structure
- [ ] Implement chess-parser.js (PGN → positions with FEN/UCI)
- [ ] Implement stockfish-engine.js (Web Worker wrapper)
- [ ] Create basic UI for PGN input and analysis display
- [ ] Test: Can load PGN, get eval for each position

### Phase 2: Pattern Detection
- [ ] Port pattern detection from v6.8 prototype
- [ ] Integrate with position analysis pipeline
- [ ] Add additional patterns (discovered attacks, batteries)
- [ ] Test: Patterns detected match expected results

### Phase 3: Data Merge Layer
- [ ] Implement merged AnalyzedPosition data structure
- [ ] Add eval dynamics calculation (deltas, blunders, turning points)
- [ ] Add game phase detection
- [ ] Test: Full analyzed output for sample games

### Phase 4: Narrative Mapping
- [ ] Design narrative rules JSON schema
- [ ] Implement rule evaluation engine
- [ ] Create initial mapping rules
- [ ] Add genre-specific trope selection
- [ ] Test: Chess events produce expected story beats

### Phase 5: UI/Output
- [ ] Build beat sheet output view
- [ ] Add dramatic moment highlighting
- [ ] Create export options (JSON, Markdown)
- [ ] Add visualization for eval graph
- [ ] Polish UI/UX

### Phase 6: Refinement
- [ ] Test with diverse PGN games
- [ ] Tune evaluation thresholds
- [ ] Expand genre trope database
- [ ] Performance optimization
- [ ] Documentation

---

## Appendix: Quick Reference

### UCI Command Cheat Sheet

```
uci                           # Initialize, get engine info
isready                       # Ping, waits for 'readyok'
setoption name X value Y      # Configure engine
position startpos             # Set starting position
position startpos moves ...   # Set position with moves
position fen <fen>            # Set position from FEN
go depth N                    # Search to depth N
go movetime N                 # Search for N milliseconds
go infinite                   # Search until 'stop'
stop                          # Stop searching, get bestmove
quit                          # Terminate engine
```

### Centipawn Evaluation Guide

| Score | Meaning |
|-------|---------|
| 0 | Equal |
| +50 | Slight white edge |
| +100 | Clear white advantage (1 pawn) |
| +200 | Strong white advantage |
| +300 | Winning for white |
| +500 | Completely winning |
| mate N | Forced mate in N moves |

### Chess.js Key Methods

```javascript
new Chess()                    // Create game
chess.loadPgn(pgn)            // Load PGN
chess.history({ verbose: true }) // Get detailed moves
chess.fen()                   // Get current FEN
chess.move(san)               // Make move, returns details
chess.isCheck()               // Check state
chess.isCheckmate()           // Checkmate state
chess.turn()                  // 'w' or 'b'
```

---

*End of specification document.*
