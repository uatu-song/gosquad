# Go Squad Session Handoff

**Last Updated:** 2026-08-29 (the metric-rewrite era: ch12–16 generated and
gated, ch1–11 vetted, the bible written, the sample epub reads 1–16)
**Session:** Chicago typography → ch1–11 vetting rulings → style profile +
band gate → dialogue-frozen cold-agent pipeline → ch12–16 + CH18/CH24 pilots
→ temporal mechanics bible → sample epub ch1–16

---

## FIRST ACTION, EVERY SESSION

```bash
cp _canon/hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
python3 _canon/tools/audit.py --book book_1_clean
python3 _canon/tools/check_promises.py --book book_2
```
**The wall does NOT survive a fresh clone/codespace** — reinstall it first
(this session found it silently absent). `git push` may need `--no-verify`
only for git-lfs issues; text commits push clean.

Then read `canon/book_1_ed1/DECISIONS_LOG.md` top-down until you hit a ruling
you remember. That file is the real handoff.

---

## IMMEDIATE RESUME POINT

**Next chapter in the pipeline: CH17 — Kain POV** (census lead), the first
non-Ahdia chapter through the dialogue-frozen cold pass and the first test of
`2_method_actor/book1_embodiment/Harding_Kain_Book1_Embodiment.md`.

**Awaiting Director reads:** ch15, ch16 (ch12–14b already read; notes applied).

### The pipeline (proven across 8 generations, ch12–16 + 18 + 24)
1. Read source chapter in full (vet-eye: canon drift gets fixed BEFORE freezing).
2. Extract dialogue spans programmatically — never retyped — with attributions.
3. Build `CHxx_METRIC_PACKET.md` in `6_manuscript/book_1/rewrite_pilot/`:
   frozen spans + beats + canon locks + band targets. Packets cite THE BIBLE
   (`canon/series/TEMPORAL_MECHANICS.md`) and the topography
   (`canon/book_1_ed1/CH01-11_TOPOGRAPHY.md`).
4. Cold agent reads packet + bible + topography + **all prior metric drafts
   (read-up-to-where-you-write — the fix for the van/Academy context errors)**
   + the POV embodiment. Nothing else. Forbid grep explicitly.
5. Typeset via the chicago converter (scratchpad; recreate from
   DECISIONS_LOG history if gone), then gate:
   `python3 _canon/tools/check_style.py DRAFT --source SOURCE [--allow-chest N]`
   plus `check_nouns.py --book book_1_clean`.
6. Texture failures → SendMessage the SAME agent with the numbers ("landings
   and beats; convert, don't add") — landed ch15 and ch16 on the second pass.
7. Commit with gates in the message. Directors' read notes → applied to
   draft+source+packet (dialogue changes are Director-ruled ONLY), logged
   verbatim.

### Current artifacts
| What | Where |
|---|---|
| Metric drafts, gated | `rewrite_pilot/chapter_{12,13,14a,14b,15,16}_metric_v1.txt`, `chapter_18_metric_v2.txt`, `chapter_24_metric_v2.txt` |
| Sample epub 1–16 (14a+14b bound as one Ch14) | `6_manuscript/book_1/GoSquad_Book1_sample_ch01-16.epub` + `build_sample_epub.py` |
| Clean full epub | `GoSquad_Book1_clean.epub` (+ `build_epub.py`, reads first_edition_clean) |
| THE BIBLE | `canon/series/TEMPORAL_MECHANICS.md` — governs all mechanics; §7 = team powers/trigger table; OPEN QUESTIONS stay open |
| Band gate | `_canon/tools/check_style.py` — narration-only, offset-masked, bands not floors, tag-comma swaps noted |
| Style authority | `canon/book_1_ed1/STYLE_PROFILE.md` (ch1–11 measured; floors AND ceilings) |
| Vetting + ledgers | `canon/book_1_ed1/` — VETTING_CH01-11.md (CLEARED), CANON_FACTS/PROMISES/CHRONOLOGY jsonl, CH01-11_TOPOGRAPHY.md |
| Harmonization brief (future phase) | `canon/book_1_ed1/HARMONIZATION_BRIEF.md` — narration-register + action-choreography seams, both parked |

---

## Standing doctrine (ruled — do not relitigate; full entries in DECISIONS_LOG)

- **Register:** the book committed to the metric-rewrite voice. Contrast
  doctrine: plain stretches at stakes; Ryu carries comedy; Bourn is a lab
  result; narration never tops the dialogue. Small physical costs get paid on
  the page (ears ring; sweat).
- **Structure:** back half aligns to ch1–11 per-chapter (dialogue floor +
  7.2/1K narration allowance); **dialogue is frozen** — Director edits only.
- **Typography:** full Chicago everywhere, NBSP-spaced ellipses, enforced.
- **Canon:** Bacchus surname; AUERBACH = CADENS codename class (Howitzer,
  Greyhound, Mercury); **Ryu Matsuda** (three Shiba drifts fixed); Kain =
  diamond magnate running for President ("Mayor" was drift); exactly six Go
  Squad; the team does not drive; SABLE=Victor, GLOOM GIRL=Tess, no dead wife
  ever; codenames internal, Tess leaked them; disappearance ~15+ years ago;
  Whitford father-link = author-level irony, never surfaced; Ruth's
  maybe-power NEVER resolved; the meter: 18 months is BASELINE, ambush = 23%
  capital.
- **Book 2 Ahdia POV: DEFERRED — Book 1 first** (oldest open blocker, by choice).

## Open items
- ch12 commas 72.1 vs 72.0 ceiling (standing chapter; logged, untouched).
- Wobbles filed: Firas recovery timeline (B1V-046), squad-age residue,
  hour≈3-minutes exchange rate (bible OQ#1).
- Editorial backlog unchanged (Book 2b/3 items, ch22 van, `Firas's` copyedit).
- The `/gosquad` skill loader is still broken (wrong root path) — worked
  around by reading directly.

**End of Handoff**
