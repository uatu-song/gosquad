# Continuity Review Board — Lean Design

**Status:** Section 4 thread directory APPROVED by Director 2026-09-23 (ruling D1). Run 1 unblocked pending `board.py`.
**Scope:** Book 1 (30 ch + Epilogue, 77,491 words, v1.0 = `GoSquad_Book1_REVIEW.epub`) and Book 2A (19 ch). Extensible to 2B.
**Source text rule:** Book 1 reads from `6_manuscript/book_1/v1_0/` (extracted from the v1.0 review epub). The epub is built from `first_edition_clean/` (ch1–11) + `rewrite_pilot/*_metric_v*.txt` (ch12–30); those are author sources, not board input. The old PDF extraction is in `_archive/book1_pdf_extraction/` and is not evidence. See `5_story_bibles/book_1/reviews/2026-09-22_editorial_review_report_receipt.md` for why.
**Principle:** Few agents, wide lenses, expensive model. Six agents total. One batch per chapter.

---

## 1. Why six, not fifty

The 39-agent triad design (3 per character) split each character into Knows / Is / Bonds.
Those three lenses are **the same for every character**, so invert it: one agent per lens,
holding all 13 characters. This is not just cheaper, it is more thorough:

| Problem in the 39-agent design | Six-agent fix |
|---|---|
| Ahdia tells Ruth something. Ahdia-Knows and Ruth-Knows must both update, via deferral. | One Knowledge agent updates both in the same pass. Cross-character knowledge conflicts are its whole job. |
| Shared items (dictator count, CR-7 clock) need a single owner and deferral routing. | Every number lives in one Numbers ledger. No routing. |
| 50 reports per chapter need a Reconciler to read them all. | 5 reports per chapter. The Chair reads them in one call. |
| Cost forces a cheap model. | ~6 calls per chapter. Run Fable 5.1 or Opus 5 at high effort. |

Cost, both books (50 chapters, ~300 calls, ~15K input / ~1.5K output per call):

| Model | Naive | Caching + Batch |
|---|---|---|
| Opus 5 | ~$30 | ~$10 |
| Fable 5.1 | ~$60 | ~$20 |

---

## 2. The Board

| # | Agent | Lens | Ledger it owns | Flags it raises |
|---|---|---|---|---|
| 1 | **Knowledge Registrar** | What each character knows, believes, suspects, has been told, wrongly believes | `knowledge.yaml` — per character, per fact: source chapter, how learned, confidence, wrong? | Character acts on info they don't have. Character ignorant of what they were told. Reader/character irony inversions (Ahdia POV withheld; team ignorant of Exile Island until 2B). |
| 2 | **Body & Ground Registrar** | Physical and spatial: location, injuries, fatigue, possessions, clothing, who is in the room | `body_ground.yaml` — per character, per chapter: where, condition, carrying, present with | Teleporting characters. Healed injuries. Objects that change hands unseen. Presence in a scene they can't be in (Leah's coma window, Leta after Ch23). |
| 3 | **Bonds Registrar** | Relationships, promises, debts, what others believe about a character, arc beat reached | `bonds.yaml` — per pair: state, last change, open promises; per character: arc stage | Relationship regression without cause. Broken promise never paid off. Arc beat skipped (Leah/Victor reveal order; Ben's faith collapse timing). Canon-locked relationships (Victor+Leah lovers, Bourn she/her). |
| 4 | **Numbers Clerk** | Every measured value in the text | `numbers.yaml` — per quantity: value, chapter, sentence cite, direction of change | Value moves the wrong way. Value stated twice differently. Derived math wrong (baseline %, treatment gap hours, 72-hour spacing, polling, dictator count 37, Korede age 17). |
| 5 | **Chronicler** | Time and world: dates, elapsed time, news seeds, off-page world events, season/weather | `chronicle.yaml` — ordered event list with anchors; news-seed checklist | Days that don't add up. Seed missing from its scheduled chapter (Ch4/6/8/10/12/15/18). World event contradicts prior. |
| 6 | **Board Chair** | Reconciliation + enforcement | `board_minutes/chapter_NN.md` | Contradictions between the five ledgers. Any claim without a sentence-level cite. Any claim outside the filer's lens. Any invented fact. Produces the Director's review list. |

Agents 1–5 run in parallel in one batch. Agent 6 runs after. The Director rules. Rulings are written back before the next chapter.

**Everything is deferral-free.** Each lens is exhaustive over its domain, so no agent ever needs to hand something off. If an agent finds a fact outside its lens, it ignores it; the owning lens will see the same sentence.

---

## 3. Per-chapter loop

```
chapter_N ─┬─► [1 Knowledge] ─┐
           ├─► [2 Body/Ground]─┤
           ├─► [3 Bonds]      ─┼─► [6 Chair] ─► review list ─► DIRECTOR ─► rulings ─► ledgers ─► N+1
           ├─► [4 Numbers]    ─┤
           └─► [5 Chronicler] ─┘
```

Each of agents 1–5 receives: its system prompt (frozen, cached) + its ledger as of chapter N-1 + Director rulings log + chapter N (cached, shared).
Each returns: `delta` (new/changed ledger entries, every one cited `b2:chNN:pXX:sY`) + `flags` (severity, cite, what conflicts with what).

The Chair receives: five deltas + five flag lists + the canon warnings block from CLAUDE.md.
It returns: a ranked review list. Every item names the two cites that disagree, or the one cite and the canon rule it breaks.

Director ruling options per item: **FIX PROSE** (goes to prose TODO), **FIX CANON** (ledger corrected, codex updated), **DISMISS** (recorded so it never resurfaces), **DEFER** (reopens at a named chapter).

---

## 4. Thread directory (what gets tracked)

Seeded from `CONTINUITY_TRACKER.md`, `CHARACTER_STATE_INDEX.yaml`, `8_codex/book_2/codex.yaml` canonical_values, and the 13 thread files. Director adds or strikes lines before Run 1.

### 4.1 Characters (all five lens agents track every one)
Ahdia, Ruth, Tess, Ben, Victor, Leah, Leta, Korede, Bellatrix/Geneva, Kain, Eidolon, Ryu, Bourn.
Secondary (Body/Ground and Bonds only): Firas, Webb, Prime (background), Isaiah Bennett, Bentley Mack.

### 4.2 Numbers (Numbers Clerk)
- Ahdia baseline % (95 → 54 @Ch17 → 53.1 @Ch19 → 0.7 end of 2B)
- Treatment gap (11 days functional; 36 hours at 54%)
- Treatment spacing minimum (72 hours, Ch17)
- CR-7 efficacy per dose (declining; +2 at Ch17)
- Eidolon resistance efficacy (60–70%)
- Kain polling (+8 → +12 → dip → recover → win)
- Exile Island dictator count (canon 37; 28 is a chess-move count, never a dictator count)
- Korede's age (17)
- Elapsed months (Book 2A spans Month 1 → Month 6–7)

### 4.3 Chronicle anchors (Chronicler)
- News seeds: Ch4 NK general, Ch6 Belarus, Ch8 third week, Ch10 conspiracy, Ch12 state media, Ch15 junta, Ch18 UN
- Geneva shooting; Titan Holdings surfaces (Month 6); Bourn meeting (Ch4); Webb exonerated (Ch5); Leta harassment accounts (Ch6)
- Leta dies Ch23 (killed by Webb) — 2B boundary
- Election date and result

### 4.4 Knowledge locks (Knowledge Registrar)
- Team does NOT know Exile Island until Book 2B; Ruth/Ryu learn Ch19
- Ahdia's interior is never shown; what she "knows" is inferred only from action
- Leah learns but/and Ch10 and does not speak of it until Month 9
- Bot network ≠ shooter: what the team believes vs. what is true (tracked as belief, flagged if narration collapses them)
- Bellatrix's dead Genevas: reader vs. character knowledge

### 4.5 Bond locks (Bonds Registrar)
- Victor + Leah lovers; revealed identities before the group reveal
- Tess + Leta partners; Tess brutalizes Webb, does not kill
- Ruth + Firas (proposal pending)
- Ben's wife Sarah: cause of death never specified
- Ryu never confesses love to Ahdia in Book 2
- Bourn she/her; institutional authority → defector
- Kain: President-elect, never "Mayor"

### 4.6 Body/Ground locks
- Leah's coma window (2B M11–M24)
- Leta absent after Ch23
- Eidolon amplifies fear only; never creates (behavioral lock, flag any "created" phrasing)

### 4.7 Book 1 rows (added 2026-09-23 per Director ruling D1; cites are `b1:v1_0/<file>:<line>`)

**Numbers Clerk**
- 18-month life-expectancy clock: set ch14 (`chapter_14.txt:333,335,357,367`), restated ch16 as "eighteen months baseline, maybe two years if conservative" (`chapter_16.txt:107`), ch15 Ahdia's own tally "another year and maybe more" (`chapter_15.txt:341`). Open wobble per canon PUNCH_LIST #5: ch16 frozen baseline vs ch15 "maybe more" is unbridged. Clerk tracks every restatement.
- CR-7: named ch3 as "cellular regeneration therapy" (`chapter_03.txt:113`); Ruth's protocol ch20 (`chapter_20.txt:43`); "CR-7 Temporal Variant… buy you time" ch20 (`chapter_20.txt:255`). Book 2A continues the dose/efficacy ledger from here.
- Autoinjectors: eight in the case ch24 (`chapter_24.txt:109`); eighth misfires, "nothing went in" (`chapter_24.txt:143`); Firas administers one ch29, "his thumb still on the plunger" (`chapter_29.txt:143`); ch30 Bourn: "The eighth treatment. The one she told you she'd completed" and she had lied (`chapter_30.txt:221,231`). Ledger: 7 self-administered + 1 failed + 1 by Firas. Flag any later text that says she took eight.
- Temporal impact amplification: 47x (`chapter_13.txt:201,221`). Distinct from vessel Forty-seven below. Never merge.
- Kain's size on Main Street: 15 ft "maybe more" ch23 (`chapter_23.txt:93`), 20 ft ch23/24 (`chapter_23.txt:207`, `chapter_24.txt:67`). Clerk tracks growth sequence.

**Knowledge Registrar**
- Firas status at end of Book 1: absorbed, "space smaller than a fist" ch29 (`chapter_29.txt:177`); team believes him dead, "We just lost Firas. Yesterday." ch30 (`chapter_30.txt:187`). No translocation language after ch28. Any Book 2+ "Firas translocated" framing is a later reveal, not a Book 1 fact. Reader-belief entry: reader has the same information as the team.
- Bellatrix in Book 1: two mentions, epilogue only (`epilogue.txt:55,71`): "Agent Auerbach saw Bellatrix." / "doesn't interfere. She observes. But she acknowledged Auerbach." Reader-belief lock: observer only. Team knows nothing. Book 2 canon (hidden orchestrator, Geneva) must not leak into Book 1 rereads.
- The eighth-dose lie: Ahdia told Bourn/the facility the eighth was in; it was not (`chapter_30.txt:231`). Bourn knows by ch30. Who else knows is a tracked question into 2A.
- Tamois Heart: first named ch21 by Ahdia (`chapter_21.txt:17`), Kain names it ch21 (`chapter_21.txt:247`), Ryu diagnoses integration ch24 (`chapter_24.txt:71`). Team knowledge of the Heart starts ch21, not earlier.

**Bonds / Body**
- Vessel "Forty-seven": epilogue, "Forty-seven thought he was special too. Thought the Heart made him more than a vessel." (`epilogue.txt:45`). Kain clone tank. No "Tank 51" and no "Vessel #47" label in v1.0. Codex: unrelated to retired 43/47 Ahdia iteration count.
- "Auerbach" = CADENS codename, assigned ch15 (`chapter_15.txt:315,319`); "Agent Auerbach" in epilogue. Reject "Operative Auerbach" (DECISIONS_LOG 2026-07-26).
- Main Street: 8 mentions ch23–25 (`chapter_23.txt:159,207`, `chapter_24.txt:67,163`, `chapter_25.txt:7`). Ahdia arrives by spatial fold ch24 (`chapter_24.txt:163`) in a hospital gown. Body/Ground seeds her from there.

---

## 5. Ledger schema (all five ledgers)

```yaml
entries:
  - id: K-0142                 # lens prefix + serial
    subject: Ruth              # character, pair, quantity, or event
    fact: "Knows Ahdia's baseline is 54%"
    value: null                # Numbers Clerk only
    cite: b2:ch17:p41:s2       # sentence-level, mandatory
    established: ch17
    supersedes: K-0098         # if this changes an earlier entry
    status: active | superseded | ruled   # ruled = Director touched it
    ruling: null               # FIX_PROSE | FIX_CANON | DISMISS | DEFER:chNN
```

Flags:

```yaml
flags:
  - severity: HIGH | MED | LOW
    kind: contradiction | canon_break | missing_seed | math | presence
    cites: [b2:ch17:p41:s2, b2:ch19:p03:s1]
    says: "Ruth 'had not seen the number' but K-0142 has her told it in Ch17"
```

Cite grammar follows the prose indexer: `b<book>:ch<NN>:p<para>:s<sentence>`. The indexer's beat-level locations (`b2:ch1:beat1:p3:s1`) are accepted as-is.

---

## 6. Enforcer rules the Chair applies

1. No cite, no entry. Uncited claims are struck and reported as such.
2. Lens discipline: a Numbers entry with no numeric value is struck; a Knowledge entry about location is struck.
3. Canon warnings block outranks the text. If the prose breaks canon, that is a HIGH flag, not a ledger update.
4. An agent may not infer Ahdia's interior. Any Knowledge entry for Ahdia must cite an action or a line spoken to her.
5. Dismissed items are checked by id; a re-raised dismissed flag is dropped silently and logged.
6. Every ledger entry records the build it was read from (epub version or commit hash). An entry from one build is not evidence about another.

---

## 7. Runbook (once approved)

1. Director approves Section 4 (adds/strikes lines).
2. Build `board.py`: Batch API, prompt caching on system prompt + chapter, five requests + one Chair request per chapter, ledgers as YAML on disk under `_tools/agents/review_board/ledgers/`.
3. Dry run Book 2A Ch1 at Opus 5, high effort. Director reviews the review list for signal quality.
4. If the Chair's list is useful, run Ch2–19 sequentially with a Director session per 3–4 chapters.
5. Then Book 1 (30 ch + Epilogue). Then regenerate `CONTINUITY_TRACKER.md` from ledgers.

Model: Opus 5 default. Fable 5.1 for the Chair if Director wants a stronger reconciler; cost difference is trivial at this call volume.
