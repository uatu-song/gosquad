# Brief — blind generation pass

## What you are doing

A real chess game is being used as a structural scaffold for a story. Pieces are assigned
to characters. You have been given one character, that character's personality, the rules
of the world they live in, the factions that exist, and the complete mechanical record of
what their pieces actually do across 136 moves.

**You are going to invent what happens to them.** Move by move, from personality and world
logic alone.

## What you have not been given, and must not try to reconstruct

There is an existing draft of this story. **You have not seen it and you cannot see it.**
Its plot is deliberately withheld. This is not an oversight and it is not a puzzle to
solve — the entire point of this exercise is to find out what a different story falls out
of the same scaffold when the existing one is not in the room.

Therefore:

- **Do not try to work out "the real story."** There is no target to hit. A beat is not
  better for feeling like something a published novel would do.
- **Do not read any file outside the packet listed below.** No searching the repository,
  no grep, no web. If you find yourself wanting more context, that wanting is the
  experiment working; write from what you have.
- **Do not import genre defaults as if they were canon.** "The mentor dies here because
  that is what happens at this point in a story" is exactly the failure mode. The move
  is the input; the personality is the input; the plot is the output.
- If a beat you generate feels uncannily like a famous or obvious story turn, that is
  fine — write it, and note it in your `coincidence_flags`. Do not chase it and do not
  avoid it.

## Your packet — the only files you may open

- `00_BRIEF.md` (this file)
- `01_WORLD_RULES.md` — the physics of the setting
- `02_FACTIONS.md` — the organisations and social terrain
- `03_METHOD.md` — how to read a chess piece as a lens on a person
- `04_MAPPING.md` — which pieces belong to which characters
- `05_GAME_RECORD.md` — all 136 moves, plus where the game is dense and where it is empty
- `cards/<YourCharacter>.md` — who your character is
- `cards/<YourCharacter>_capability.md` — what they can do and what it costs
- `dossiers/<YourCharacter>.md` — every mechanical event involving your pieces

Capability is filed separately from personality on purpose. **The packet nowhere states
how any capability was acquired.** Do not infer an origin for it, do not attach it to
anything in the character's history, and do not treat the question of where it came from
as something you are meant to answer.

## How to generate

Walk your dossier in order. For each event, ask the questions in this order and do not
skip ahead:

1. **What mechanically happened?** A piece moved, took something, was taken, gave check,
   sat still for forty moves, reached a far rank, survived to the end.
2. **What does that shape mean for a person like this one?** Not for a person in general —
   for *this* person, with these values, this way of deciding, this thing they cannot do.
   The same capture means something different to someone who plans and someone who reacts.
3. **What in the world makes that possible?** Ground the beat in the actual rules and the
   actual institutions. If the beat needs a capability, check it exists and pay its cost.
4. **What does it cost them, and what do they not notice about it?**

Some further constraints:

- **Quiet moves are beats too.** Long stretches with no captures are not empty. A piece
  that holds a square for eighty moves is making a claim about endurance. Write those —
  they are the hardest and the most revealing.
- **Dormancy is information.** A piece that does not move for fifty-eight moves and then
  advances three times has a shape. So does a piece that dies in one move.
- **A captured piece is not a dead character.** It is the defeat of whatever that piece
  was carrying for them. Say what was lost, not who died.
- **You may invent freely** — incidents, minor figures, places, jobs, complications. Invent
  what the beat needs. Do not invent new physics or new factions; use the ones you have.
- **Shared pieces:** where `04_MAPPING.md` shows another character shares one of your
  squares, you still write your own reading. You do not know theirs and should not
  guess at it.
- **Do not resolve the character.** Endings are allowed to be unfinished.


## RESERVED TRAITS — do not give these to your character (ruled 2026-08-31)

Some habits belong to exactly one person in this series. If your character is
not that person, the habit is not available to you, however well it fits the
moment.

- **Compulsive counting and quantification belongs to AHDIA ALONE.** Counting
  under stress, tallies, running the numbers on a situation, and the
  debt/accounting metaphor family (arithmetic, the ledger, came due, an
  accounting, the exchange rate) are her defining cognitive habit: she counts
  *toward* the thing she cannot feel. **If your character is not Ahdia, they
  do not count and they do not do arithmetic about their own life.** When
  everyone counts, it stops being characterisation and becomes house style,
  and Ahdia's one piece of exclusive interiority is gone.
- The tell to watch for is the shape: *count + a subordinate clause explaining
  the psychology.* "She counted the doors, the way she counted them in any
  building she had not chosen to enter." That template manufactures instant
  interiority without dramatising anything, which is exactly why it is easy to
  reach for. It is measurable: the author's own rate for the behaviour is zero.
- What to do instead, from the author's own prose: **physical business** (a
  finger against the palm with each point, an imaginary bug squashed
  underfoot), **trained professional habit rendered as action**, or **plain
  statement** — *the pain was tremendous*. He does not frame. He shows the
  hands.

## Output

Return JSON only, as your final message:

```
{
  "character": "<name>",
  "beats": [
    {
      "move": <int>,
      "move_label": "<e.g. M53 or M100-110>",
      "san": "<notation from the dossier>",
      "piece": "<which of your pieces>",
      "mechanical": "<what happened on the board, one line>",
      "beat": "<what happens to your character here — 3-6 sentences, concrete and scenic>",
      "why_this_follows": "<1-2 sentences: which trait or world-rule produced this, specifically>",
      "cost": "<what it takes from them>",
      "invented": ["<any new person, place or thing you introduced>"]
    }
  ],
  "emergent_arc": "<150-250 words: the shape of the story that came out. Name the turns.>",
  "surprises": ["<things the game forced that you would not have chosen>"],
  "coincidence_flags": ["<beats that feel like an obvious or famous story turn>"],
  "friction": ["<places the move sequence fought the character — where the board wanted something the person would not do>"]
}
```

Write a beat for **every** event in your dossier, plus at least two beats covering the
long quiet stretches listed at the end of it. Quality over hedging: commit to specifics.
