# PASS 3 — TYPOGRAPHY (mechanical; run BEFORE any prose pass)

Read GUARDRAILS.md first (rules 3, 4 especially).

The measured state (see 02_BASELINE.md): the manuscript MIXES conventions — curly apostrophes
alongside ~4,336 straight double quotes. Every later grep-based pass will silently miss text
if this isn't normalized first.

1. Census first, change second: `python3 ledger/tools/check_typography.py --census` reports
   every competing form per chapter. Show the author the census BEFORE changing anything.
2. Ask the author to pick the house style (RESONANCE's: curly quotes/apostrophes, closed
   em dashes word—word, … ellipsis). Log the ruling verbatim in DECISIONS_LOG.
3. Convert with a script that handles the hard cases: apostrophes inside words (don't),
   leading apostrophes ('em, 'cause — these curl BACKWARD and naive converters break them),
   nested quotes, quotes at paragraph starts in multi-paragraph speeches (open-quote
   convention: no close-quote on intermediate paragraphs — do not "fix" those as unbalanced).
4. NO other edits ride along with this pass. Typography commits contain typography only.
5. Write the ruling into `ledger/config.json` → `suite.typography_house_style` (e.g.
   `{"quotes": "curly", "em_dash": "closed", "ellipsis": "character", "italics": "asterisk"}`).
   From then on `check_typography.py` (no flag) exits 1 on drift, runs in the pre-commit gate and
   in the reseal cascade. Every future grep must still normalize typography (rule 4).
6. Conversion happens under an open seal (`seal.py break-glass`), as its own commit, then
   `census` of the forms before → after in DECISIONS_LOG.
