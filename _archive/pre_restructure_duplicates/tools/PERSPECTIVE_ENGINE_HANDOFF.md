# Perspective Engine — Handoff Document

## What It Is

`tools/perspective_engine.html` is a standalone HTML tool that takes a chess game (PGN) and generates per-character narrative scaffolding for the Auerbach Series. It's the Go Squad version of the generic Perspective Engine in `reference/perspective_engine.html`.

## How It Works

### Two-Phase Flow

**Phase 1 — Raw Analysis:**
1. Paste or select a PGN (Book 2 is pre-loaded)
2. Engine simulates every half-move, tracking all 32 pieces
3. Per-piece journey cards show: moves, captures, deaths, threats, witnesses, checks, promotions
4. Each card includes an SVG trail visualization of the piece's path across the board
5. You read the journeys and decide which Go Squad character fits which piece arc

**Phase 2 — Character Assignment + Scaffold:**
1. Assign characters from dropdown (17 Go Squad characters, organized by faction)
2. Click "Build Scaffold" to generate per-character narrative scaffolding
3. Optionally export as standalone HTML file

### Locked Constraints
- **Ahdia Bacchus** is auto-locked to whichever piece delivers checkmate
- **Bellatrix** is auto-locked to the Black Queen
- All other assignments are manual — determined by studying the piece journey and matching it to the character whose arc it fits

### What the Scaffold Generates Per Character
- **Identity** — role, summary, series arc (pulled from embedded character profiles)
- **Chess Arc** — entry move, exit (death/survival), active range, kills, threats, witnesses
- **Journey Trail** — SVG board visualization of the piece's path
- **Key Moments** — captures, checks, promotions, checkmate, death
- **Relationships In Play** — cross-references other assigned characters, notes allied/opposed side
- **Temporal Cost Tracking** — Ahdia-specific: maps piece activity to cellular degradation progression
- **Theme Resonance** — which series themes activate in which phases based on the character's activity
- **Writing Prompts** — Go Squad-native prompts for exposition, climax, violence, and sustained danger
- **Witnessed Events** — what the character saw happen to others (adjacency-based)
- **Pawn Companions** — toggle pawns onto major pieces to extend thin stories
- **Move-by-Move Timeline** — filtered to assigned characters, with board snapshots and phase markers

### Plot Structure Detection
The engine auto-detects five narrative phases from the chess game:
- **Exposition** — before pieces cross the center
- **Inciting Incident** — first territorial crossing
- **Rising Action** — between conflict and climax
- **Climax** — the decisive check sequence before checkmate
- **Resolution** — checkmate or final position

## Pre-Loaded Data

### Characters (17)
Go Squad: Ahdia, Firas, Ruth, Tess, Leah, Victor, Ben
TRIOMF: Harding Kain, Chief Whitford
CADENS: Director Bourn, Dr. Shiba Ryu, Rahs Jericho, Colonel Mack
Cosmic: Bellatrix, The Intermediary, Ahdia-Prime
Civilian: Geneva Windrow, Isaiah Bennett

Each character includes: faction, role, summary, arc, themes, relationships, powers.

### Series Themes (11)
Worthiness, procrastination as signal, both/and thinking, sacrifice, collective power, truth vs power, systemic evil, love as infection, perfection as destruction, asking for help, non-linear progress. Each theme is mapped to the narrative phases where it resonates most.

### Pre-Loaded Games
- **Book 2:** `1. e4 e6 2. Bc4 c6 3. Nc3 b5...26. Qxd7# 1-0` — Black accumulates +19 material advantage, White delivers devastating checkmate

## Architecture

Single standalone HTML file (~1070 lines). No dependencies except Google Fonts (Playfair Display, Source Sans 3). No build step.

### Key Components
- **Board class** — full chess board simulation with move resolution, attack maps, adjacency
- **parseMove()** — PGN move parser (handles castling, en passant, promotion, disambiguation)
- **analyzeGame()** — main analysis loop: simulates game, tracks per-piece data, detects plot structure
- **autoAssignLocked()** — locks Ahdia to checkmate piece, Bellatrix to Black Queen
- **renderJourneys()** — Phase 1 UI: journey cards with SVG trails and assignment dropdowns
- **buildScaffold()** — Phase 2: generates full per-character scaffolding HTML
- **buildCharacterScaffold()** — per-character section with Go Squad context
- **buildTimeline()** — move-by-move timeline filtered to assigned characters
- **exportHTML()** — bundles scaffold output into downloadable standalone HTML

### Known Technical Detail
The `exportHTML()` function contains a template literal with `<script>` tags inside it. These are split using string concatenation (`<` + `script>`) to prevent the browser's HTML parser from prematurely closing the outer `<script>` block. If you modify the export template, maintain this pattern.

## Origin

Built from the generic Perspective Engine (`reference/perspective_engine.html`) which was designed for classroom collaborative writing. The Go Squad version replaces the generic "student assigns character to piece" flow with the Auerbach universe — pre-loaded character profiles, faction coloring, series themes, temporal cost tracking, and Go Squad-native writing prompts.

The generic engine's Google Sheets save/load feature was removed (not needed for single-author use). The piece selection UI was replaced with the two-phase journey-first workflow.

## Future Work
- Add more pre-loaded games as chess games are assigned to Books 3-7
- Character list will grow as new characters are introduced in later books
- Theme list can be extended as series themes evolve
- Consider adding material advantage tracking (Black's +19 in Book 2 is thematically significant)
- Could add a "what this character knows at move N" continuity tracker
