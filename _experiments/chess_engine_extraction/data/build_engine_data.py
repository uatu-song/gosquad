#!/usr/bin/env python3
"""Ground-truth extraction from the Book 1 PGN.

Produces per-ply board state AND per-piece provenance (which ORIGINAL piece,
identified by its starting square, is on each square at each moment). Piece
provenance is what the triplet system actually depends on -- 'Ahdia's knight
is the b1 knight' is a claim about identity across 136 moves, and python-chess
does not track it, so we do.
"""
import json, sys
import chess, chess.pgn

PGN = "/workspace/6_manuscript/book_1/book1_chess_game.pgn"
OUT = "/tmp/claude-1000/-workspace/07655e4a-a8e4-4a50-a262-bfe0909799ba/scratchpad"

game = chess.pgn.read_game(open(PGN))
headers = dict(game.headers)
board = game.board()

# identity map: square -> label of the piece that STARTED there
ident = {}
for sq in chess.SQUARES:
    p = board.piece_at(sq)
    if p:
        ident[sq] = chess.square_name(sq)

origin = {v: v for v in ident.values()}      # label -> label (stable)
fate = {v: dict(label=v, piece=str(board.piece_at(chess.parse_square(v))),
                color="white" if board.piece_at(chess.parse_square(v)).color else "black",
                first_move_ply=None, moves=0, captures=[], captured_at_ply=None,
                captured_by=None, promoted_to=None, final_square=None, survives=True)
        for v in ident.values()}

plies = []
ply = 0
for mv in game.mainline_moves():
    ply += 1
    move_no = (ply + 1) // 2
    side = "white" if board.turn == chess.WHITE else "black"
    san = board.san(mv)
    mover = ident.get(mv.from_square)
    is_cap = board.is_capture(mv)
    victim = None
    if is_cap:
        cap_sq = mv.to_square
        if board.is_en_passant(mv):
            cap_sq = mv.to_square + (-8 if board.turn == chess.WHITE else 8)
        victim = ident.get(cap_sq)
        if victim:
            fate[victim].update(captured_at_ply=ply, captured_by=mover, survives=False)
            ident.pop(cap_sq, None)
    # move identity
    if mover:
        if fate[mover]["first_move_ply"] is None:
            fate[mover]["first_move_ply"] = ply
        fate[mover]["moves"] += 1
        if victim:
            fate[mover]["captures"].append(dict(ply=ply, move_no=move_no, victim=victim, san=san))
        ident.pop(mv.from_square, None)
        ident[mv.to_square] = mover
        if mv.promotion:
            fate[mover]["promoted_to"] = chess.piece_symbol(mv.promotion)
    # castling moves the rook too
    if board.is_castling(mv):
        rank = 0 if side == "white" else 7
        if chess.square_file(mv.to_square) == 6:      # kingside
            rf, rt = chess.square(7, rank), chess.square(5, rank)
        else:                                          # queenside
            rf, rt = chess.square(0, rank), chess.square(3, rank)
        rid = ident.pop(rf, None)
        if rid:
            ident[rt] = rid
            fate[rid]["moves"] += 1
            if fate[rid]["first_move_ply"] is None:
                fate[rid]["first_move_ply"] = ply

    board.push(mv)
    plies.append(dict(ply=ply, move_no=move_no, side=side, san=san, mover_origin=mover,
                      capture=is_cap, victim_origin=victim, check=board.is_check(),
                      fen=board.fen()))

for sq, lab in ident.items():
    fate[lab]["final_square"] = chess.square_name(sq)

data = dict(headers=headers, total_plies=ply, total_moves=(ply + 1) // 2,
            result=headers.get("Result"), plies=plies, piece_fates=list(fate.values()))
json.dump(data, open(f"{OUT}/engine_ground_truth.json", "w"), indent=1)

# ---- verification of specific canon claims -------------------------------
def at(move_no, side):
    return [p for p in plies if p["move_no"] == move_no and p["side"] == side]

print(f"GAME: {headers.get('White')} vs {headers.get('Black')}, {headers.get('Event')} "
      f"{headers.get('Site')} {headers.get('Date')} R{headers.get('Round')} -> {headers.get('Result')}")
print(f"{data['total_moves']} moves / {ply} plies\n")

print("=== CANON CLAIM CHECKS ===")
checks = [
    ("M136 Ng7 played by the b1 knight (Ahdia's active self)", 136, "white"),
    ("M17 Bxf6 - which black knight dies", 17, "white"),
    ("M19 Nxd4 - by which white knight", 19, "white"),
    ("M20 white move (canon says Bxg2/Kxg2)", 20, "white"),
    ("M20 black move", 20, "black"),
    ("M26 Qxc8 - victim", 26, "white"),
    ("M33 Bxa3 - victim", 33, "black"),
    ("M53 Rxa3 - victim", 53, "white"),
    ("M80 Rxf7+ - which white rook, victim", 80, "white"),
    ("M82 Rxa7 - which white rook, victim", 82, "white"),
    ("M79 Rxf5 - victim", 79, "white"),
    ("M114 gxh4 - by which pawn, victim", 114, "white"),
    ("M115 Qxh4 - victim", 115, "black"),
]
for label, mn, side in checks:
    for p in at(mn, side):
        print(f"  {label}\n      M{mn} {side}: {p['san']:<8} mover={p['mover_origin']} "
              f"victim={p['victim_origin']} check={p['check']}")

print("\n=== TRIPLET-CRITICAL PIECE FATES ===")
for lab in ["b1", "g1", "d1", "a1", "h1", "c1", "f1", "e1",
            "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
            "e8", "f8", "b8", "g8", "g7", "f7", "d8"]:
    f = fate[lab]
    cap = (f"captured M{(f['captured_at_ply']+1)//2} by {f['captured_by']}"
           if f["captured_at_ply"] else f"SURVIVES on {f['final_square']}")
    fm = f"first moved M{(f['first_move_ply']+1)//2}" if f["first_move_ply"] else "never moved"
    print(f"  {lab} {f['piece']:<2} {f['color']:<5} {fm:<18} moves={f['moves']:<3} "
          f"captures={len(f['captures']):<2} {cap}")
