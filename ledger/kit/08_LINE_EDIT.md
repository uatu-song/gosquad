# PASS 8 — LINE-EDIT SUPPORT PROTOCOL (runs alongside the author's own reading pass)

Read GUARDRAILS.md first (rules 1, 7, 8, 10, 11). This pass has no checklist of its own —
it is the protocol for handling what the author finds while reading, which is where most real
defects come from (in RESONANCE, every major defect was found by a human reading, not a tool;
the tools then proved absence of siblings).

When the author flags something:
1. LOCATE it exactly; read the full scene, not the quoted line (rule 7).
2. Fix the INSTANCE, then hunt the CLASS: build a normalized-typography grep for the pattern
   and sweep the book, verifying each hit by reading (zero reads as clean — prove the pattern
   matches a known site first).
3. For any cut: two-step cut verification (rule 8) before it lands.
4. For any rewrite with creative latitude: enumerate → author culls → draft clean (rule 10).
5. For any beat the author dictates: place it, then read FORWARD two beats — a cut or insert
   inside a dialogue run orphans answers to questions that no longer exist.
6. Log every ruling verbatim, every session, before it ends (rule 11). End each session with
   a one-paragraph harvest report: what changed, what was logged, what awaits ruling.

Standing cautions for this manuscript specifically:
- The ch12-30 fragment texture is ruled territory (see 06) — line edits there must not
  regress the ruling.
- "The feeling arrives late / the body reports first" appears to be a recurring move
  (heart/chest/breath counts in 02_BASELINE.md) — before trimming interiority formulas,
  function-test whether the pattern is the book's somatic register.

Mechanics for every change in this pass:
- `seal.py break-glass --reason "..." --authorized-by joe` BEFORE any edit (script or tool), then
  harvest, log, `seal.py reseal`. Reseal refuses until a ruling is logged.
- Batches of small changes go to Joe as a file: numbered items, FULL current sentence and FULL
  proposed sentence, a MARK line each. He names the numbers he rejects.
- After a class sweep, `census.py "<pattern>" --since <ref>` for the measured before → after, and read
  each changed site.
