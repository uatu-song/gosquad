# PASS 11 — REPEATED CONSTRUCTIONS (figures and sentence shapes across chapters)

Read GUARDRAILS.md and COLLABORATOR_RULES.md first.

Joe's frame (Resonance, 2026-10-17): repeated sentence constructions are the placeholders — the
same figure reached for again because it was nearest, not because it was meant. Word-level repetition
is pass 4; this is the shape level: "gave nothing back" ×9, "held breath" ×11, "swallowed whole" ×6,
"its own small grief/horror".

1. **Find candidates.** `check_repetition.py` surfaces repeated n-grams; read its output for FIGURES
   and frames, not function phrases. Then sweep for families by mechanic, typography-normalized:
   `census.py "held (?:its |her |his |a )?breath|holding (?:its|her|his) breath" --sites`.
   Search the inflections; a literal string misses "holds"/"holding"/"held".
2. **Census per construction**, every site with chapter:line and the clause, dialogue marked (dlg).
   A file: `ledger/review/REPEATS_CENSUS_<date>.md`.
3. **Joe rules per construction**: motif (register it in config.json `motifs` — then it's exempt
   forever), leave, or vary. Some are a character's idiom ("That's the whole X" ×6 was Elena's);
   some are a deliberate rhyme between two characters. Ask; don't infer.
4. For "vary": proposals in a file with the FULL printed sentence and the FULL proposed sentence,
   numbered. He replies with the numbers he rejects, or "take all" / "leave all".
   Resonance's last batch: "leave all." That is a valid outcome — log it and stop.
5. A new figure must not repeat a figure already in the book (check with `codex.py --find`).
