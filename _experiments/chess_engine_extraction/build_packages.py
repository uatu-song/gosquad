#!/usr/bin/env python3
"""Assemble ten paste-ready external-LLM packages, dossiers truncated to move 15."""
import json, os, re

BASE = "/workspace/_experiments/chess_engine_extraction"
P = f"{BASE}/blind_pass"
OUT = f"{P}/external_packages"
os.makedirs(OUT, exist_ok=True)

gt = json.load(open(f"{BASE}/data/engine_ground_truth.json"))
plies = gt["plies"]
fates = {f["label"]: f for f in gt["piece_fates"]}
NAMEP = {"K":"king","Q":"queen","R":"rook","B":"bishop","N":"knight","P":"pawn"}
def desc(lab):
    f = fates[lab]
    return f"{f['color']} {NAMEP[f['piece'].upper()]} ({lab})"

MAP = {
 "Ahdia":["e1","b1","e2"], "Firas":["d1","a1","f2"], "Ruth":["h1","f1","d2"],
 "Ryu":["b1","f2","e1"],   "Ben":["a1","b2","c1"],   "Tess":["g1","g2","h2"],
 "Leah":["f1","d2","c2"],  "Victor":["c1","a2","g8"],"Bourn":["e1","d1","a2"],
 "Kain":["e8","f8","g7"],
}
OWNERS = {}
for ch, sqs in MAP.items():
    for s in sqs:
        OWNERS.setdefault(s, []).append(ch)

CUT = 15
world  = open(f"{P}/01_WORLD_RULES.md").read().strip()
fact   = open(f"{P}/02_FACTIONS.md").read().strip()
method = open(f"{P}/03_METHOD.md").read().strip()

def truncated_dossier(ch):
    sqs = MAP[ch]
    L = [f"Your pieces, and their status as of move {CUT}.",
         "(Nothing beyond move 15 is stated — you do not know these pieces' later fates.)",
         "",
         "| Piece | Starts on | First moves | Moves so far | Captures so far | Status at move 15 |",
         "|---|---|---|---|---|---|"]
    for s in sqs:
        f = fates[s]
        fmp = f["first_move_ply"]
        first_mv = (fmp + 1)//2 if fmp else None
        first = (f"move {first_mv}" if first_mv and first_mv <= CUT
                 else f"**has not moved by move {CUT}**")
        moves = sum(1 for p in plies if p["mover_origin"] == s and p["move_no"] <= CUT)
        caps  = sum(1 for p in plies if p["mover_origin"] == s and p["capture"] and p["move_no"] <= CUT)
        cp = f["captured_at_ply"]
        cmv = (cp + 1)//2 if cp else None
        status = (f"**captured on move {cmv}**" if cmv and cmv <= CUT else "still on the board")
        shared = [c for c in OWNERS[s] if c != ch]
        share = f" *(shared with {', '.join(shared)})*" if shared else ""
        cross = (" — **opposing-side piece; a lens only, never controlled by this character**"
                 if f["color"] != ("black" if ch == "Kain" else "white") else "")
        L.append(f"| {desc(s)}{share}{cross} | {s} | {first} | {moves} | {caps} | {status} |")
    L += ["", "Events involving your pieces, moves 1-15.", "",
          "Columns: move · side to move · notation · what mechanically happened · "
          "material left on each side in pawn units (white/black) · "
          "how many moves since the last capture anywhere on the board.", "",
          "| Move | | SAN | Event | Mat. | Quiet |", "|---|---|---|---|---|---|"]
    # reuse the already-built dossier rows, filtered
    rows = [ln for ln in open(f"{P}/dossiers/{ch}.md").read().split("\n")
            if re.match(r"^\| \d+ \|", ln)]
    kept = [ln for ln in rows if int(ln.split("|")[1].strip()) <= CUT]
    L += kept
    L += ["", f"*{len(kept)} events in this span.*", ""]
    evm = sorted({int(ln.split('|')[1].strip()) for ln in kept})
    quiet, prev = [], 0
    for m in evm + [CUT + 1]:
        if m - prev > 3 and prev:
            caps = sum(1 for p in plies if prev < p["move_no"] < m and p["capture"])
            quiet.append(f"- **moves {prev+1}-{m-1}** — nothing of yours moves or is touched. "
                         f"{caps} capture{'s' if caps != 1 else ''} elsewhere on the board.")
        prev = m
    if evm and evm[0] > 3:
        quiet.insert(0, f"- **moves 1-{evm[0]-1}** — nothing of yours has moved yet.")
    L += ["Quiet spans inside moves 1-15 (invent a beat for these if the personality supports one):", ""]
    L += quiet or ["- none of any length"]
    return "\n".join(L)

TPL = """You are being given a blind writing assignment. You do not have the full context of what this material belongs to, and that is intentional — do not ask for more information, and do not assume genre conventions beyond what is stated below.

=== WORLD RULES ===
{world}

=== FACTIONS ===
{fact}

=== METHOD ===
{method}

=== YOUR CHARACTER: {NAME} ===

--- Personality ---
{card}

--- Capability ---
{cap}

--- Your piece's moves (moves 1-15 only) ---
{dossier}

=== YOUR TASK ===

Write {NAME}'s beats for moves 1 through 15, following the method described above.

A steward does not write prose. As the method states, a beat is a compact unit with two parts: a reading of the assigned game position, and the narrative meaning extracted from it. Produce one beat per event in the dossier above, plus a beat for each quiet span it lists.

Format every beat exactly like this, and write nothing between beats:

### Move <number> — `<notation>` — <which of your pieces>
**Reading.** What your piece is doing on the board, and what claim about a life that behaviour can support. Analytical. Name the pieces directly.
**Meaning.** What this configuration reveals about this person — stated as a claim, not experienced.

Rules:
1. Use only the material given above. Do not invent facts about the world, the factions, or other characters beyond what is stated here.
2. Ground every beat in the move's mechanical fact — advance, capture, being captured, check, sitting still — not in any assumption about a larger plot.
3. For a quiet span, the absence is the material. Write what it means that nothing of this person's is moving while the game goes on without them.
4. Do not try to guess the genre, the ending, or what the author "really wants." Write only what emerges from the material in front of you.
5. The **Meaning** half is analysis, not narration. Third person, plain register, one to three sentences. State a claim about what this configuration reveals about {NAME} that a reader would not already have had. Do not write in {NAME}'s voice. Do not render their interior experience as lived narration — no remembered scenes, no sensory detail, no rhythm matched to the Voice section. If a Meaning paragraph could be mistaken for a paragraph out of a novel, it has failed this rule regardless of length or word count.
6. Keep beats compact. Roughly 100 to 200 words each. A beat is not a scene and it is not an outline entry.
7. Hold to the standard the method sets out for good beats against generic ones. Make a specific, falsifiable claim about this person that was not available before. Let them be wrong in ways consistent with what they know. Prefer physical specificity over stated interiority. Do not resolve the moment tidily, and do not restate the scaffold in place of interpreting it.
8. If uncertain about a beat, prefer restraint over invention. A small, grounded reading beats a large, unsupported one.

Begin.
"""

import sys
only = [c for c in sys.argv[1:] if c in MAP] or list(MAP)
if len(only) < len(MAP):
    print(f"  (selective build: {', '.join(only)} — the other "
          f"{len(MAP) - len(only)} packages are left untouched)\n")
for ch in only:
    card = open(f"{P}/cards/{ch}.md").read().strip()
    cap  = open(f"{P}/cards/{ch}_capability.md").read().strip()
    txt = TPL.format(world=world, fact=fact, method=method, NAME=ch,
                     card=card, cap=cap, dossier=truncated_dossier(ch))
    open(f"{OUT}/{ch}.txt", "w").write(txt)
    print(f"  {ch:<8} {len(txt.split()):>5} words  {len(txt):>6} chars")
print(f"\nwritten to {OUT}")
