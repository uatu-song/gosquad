# Canon Arbitrations — Book 4 Conflict Resolutions

**Arbitrator:** Claude (crew, not author)
**Date:** 2026-05-18
**Director:** J. S. Vaughn
**Status:** PROPOSED — pending Director ratification

---

## How to read this file

Each entry has:
- **Conflict** — the disagreement
- **Sources** — which docs claim what
- **Arbitration** — the proposed resolution
- **Class** — `HARD` (documentation-reconciliation, no creative judgment; I called it) or `SOFT` (creative fork; I proposed a default but the Director should confirm)
- **Reasoning** — why this resolution
- **Action items** — what needs to be updated in repo

Override any of these by replying "override [Cn]: [new resolution]" and I'll update.

---

# HARD Arbitrations (docs reconciliation; ratified absent override)

## C1 — Iteration count (5 vs 47)

**Conflict:** Master plan's prologue prose has Prime say "This is iteration 47. I've tried everything." The current 5-iteration canon would make this line wrong.

**Sources:**
- `BOOK3_MASTER_PLAN.md` (2025-10-14): "iteration 47"
- `BOOK3_PLANNING_STATUS.md`: "5 Total Iterations (NOT 43/47)" — explicitly marked as corrected
- `CHARACTER_QUICK_REFERENCE.md`: "5 iterations total. Prime = Ahdia-1. Current = Ahdia-5."
- Root `CLAUDE.md`: "Prime = Ahdia-1. Current Ahdia = Ahdia-5. 5 total iterations (NOT 43/47 from early planning)."

**Arbitration:** **5 iterations is canon.** Master plan is stale on this point.

**Class:** HARD

**Reasoning:** Three sources agree explicitly that the 5-iteration model is the corrected canon, with one (planning status) explicitly marking the 43/47 references as wrong.

**Action items:**
- Prologue prose needs a one-line rewrite: "iteration 47" → "iteration 5" (or remove the numeric and keep "I've tried everything")
- Master plan should be updated or marked stale when next touched

---

## C2 — Bellatrix's motive

**Conflict:** Two framings of Bellatrix's reason for being in Iteration 5.

**Sources:**
- `BOOK3_MASTER_PLAN.md`: "Ultimate CBT practitioner. Wants to eliminate consciousness copies to solve the problem."
- `Bellatrix_Motives_v3.md` (newer, filename signals iteration): "Maternal obsession disguised as scientific curiosity. She gave consciousness to children via clone avatars; becoming a mother triggered emotions her Type IV civilization had eliminated. She is in Iteration 5 to observe Ahdia (her consciousness fragment that became genuinely human) and test whether love survives impossible pressure."

**Arbitration:** **v3 supersedes master plan.** Bellatrix's motive is maternal obsession testing whether love can survive — NOT "eliminate consciousness copies."

**Class:** HARD

**Reasoning:**
- v3 filename signals it as the third revision of this question (i.e., the author has already worked through the question and landed here)
- v3 framing is character-driven and produces stronger thematic alignment with the series core thesis ("you don't have to be fixed to be worthy" — Bellatrix is the antagonist precisely because she *can't* accept that broken is enough)
- The master plan's "ultimate CBT practitioner" framing is interesting but doesn't connect to her maternal relationship with Ahdia, which is the load-bearing emotional engine of Book 4's climax ("You chose correctly. I... chose wrong.")
- v3 framing makes Bellatrix the antagonist whose defeat is built into the CBT→DBT thematic arc (she's the maximum CBT practitioner; Ahdia's DBT acceptance disproves her)

**Action items:**
- All future Bellatrix scenes operate from v3 framing
- Master plan needs revision or stale marker

---

## C3 — Eidolon's nature

**Conflict:** Different framings of what Eidolon is.

**Sources:**
- `BOOK3_MASTER_PLAN.md`: "Eidolon was pure fear essence; Bellatrix grants ability to transfer consciousness into clone avatar (first time embodied)."
- `EIDOLON_CANON.md` (2025-10-13, explicitly marked "Series Canon"): "Eidolon is a Fear-fragment torn from a unified dimensional being that originally processed the full emotional spectrum (Fear, Hope, Joy, Rage, Grief, Love, etc.). Bellatrix mutilated the unified being and weaponized the Fear fragment. Other fragments exist, scattered across dimensions."

**Arbitration:** **EIDOLON_CANON.md supersedes master plan.** Eidolon is a tragic Fear-fragment victim, NOT a natural predator. Other fragments exist (Hope, Joy, Rage, Grief, Love) and are series-level seeds.

**Class:** HARD

**Reasoning:**
- EIDOLON_CANON is explicitly marked "Series Canon" with date (2025-10-13)
- The fragment framing connects to Book 2B's grief crack at M24 ("Why didn't the grief become fear?") — already canonized in BOOK2B_TOPOLOGY
- Opens a series-level reunification quest seed (Books 5-8) that doesn't exist in the master plan's pure-essence framing
- Thematically richer: makes Eidolon a parallel-victim to Ahdia (both mutilated by Bellatrix's choices)

**Action items:**
- Master plan needs revision
- Book 4 prose treats Eidolon as fragment-victim throughout
- The "embodiment via clone avatar" still happens — but as an additional violation on top of the original fragmentation, not as Eidolon's first physical existence

---

## C5 — Ryu's surname

**Conflict:** "Tanaka" vs "Matsuda."

**Sources:**
- Book 4 directory files (`BOOK3_MASTER_PLAN.md`, `CHARACTER_QUICK_REFERENCE.md`): "Ryu Tanaka"
- Root `CLAUDE.md`: "Ryu Matsuda"
- `BOOK1_TOPOLOGY.yaml`: "Ryu Matsuda"
- `BOOK2A_TOPOLOGY.yaml`, `BOOK2B_TOPOLOGY.yaml`: "Ryu Matsuda"

**Arbitration:** **Matsuda is canonical.** Tanaka references in Book 4 directory are stale.

**Class:** HARD

**Reasoning:** Three current topology files plus the root CLAUDE.md all use Matsuda. Book 4 directory files are the outliers.

**Action items:**
- Book 4 docs should be renamed in next planning pass
- Affects no prose yet (Ch1 prose may use either — needs check)

---

# SOFT Arbitrations (creative forks; proposed defaults pending Director)

## C4 — The "brother" identity

**Conflict:** Master plan + character_quick_reference reference an unnamed "brother" as Ahdia's other sibling, also progeny of clone avatars. Series canon: Firas is her brother, displaced into The Between, returns Book 7.

**Sources:**
- Master plan: "Ahdia and her brother are progeny of clone avatars. Mother: Bellatrix. Father: Unknown."
- Character quick reference: "Brother's appearance and role" marked as pending reveal
- Series canon (BOOK1_TOPOLOGY, root CLAUDE.md): "Firas displaced into dimensional space (NOT dead). Returns Book 7."

**Proposed resolution:** **This is Firas. The "appearance" in Book 4 planning docs is actually Firas's progeny status being revealed — not him physically appearing. He stays in The Between through Book 4 and returns in Book 7 per locked canon.**

**Alternative options:**
- **A (proposed):** Firas's progeny status is what's revealed in Book 4; he remains in The Between
- **B:** Separate sibling exists, introduced in Book 4 (NEW character)
- **C:** Firas returns early in Book 4 (rewrites the Book 7 return canon)
- **D:** Defer — leave it as an unresolved reveal for now

**Class:** SOFT — Director must confirm

**Reasoning for default (A):** Preserves locked series canon (Firas displaced through B6, returns B7). The progeny revelation is a major Book 4 beat regardless of whether Firas is physically present. Introducing a new sibling for Book 4 only would be unusual without prior seeding in B1-B2B.

**Action items if confirmed:** Rephrase planning docs to clarify "the brother" = Firas (whose progeny nature is the reveal, not his presence). Update CHARACTER_QUICK_REFERENCE accordingly.

---

## C6 — A/B split lock

**Conflict:** Whether Book 4 ships as one ~50-chapter book or splits A/B at Ch19.

**Sources:**
- Root CLAUDE.md: "Book 4 (old Book 3) will also likely split A/B."
- Braided structure: "~50-60 chapters... may split into Books 3 & 4"
- Climax structure: assumes single book Ch1-51

**Proposed resolution:** **Lock the A/B split at Ch19 (rift moment).** Series renumbers to 9 books total (or 8 with 4A/4B alternate naming, matching the 2A/2B pattern).

**Alternative options:**
- **A (proposed):** Lock split at Ch19. New canonical naming: Book 4A / Book 4B (matching 2A/2B pattern)
- **B:** Keep as single ~50-chapter book; deal with length in production
- **C:** Defer — proceed with planning until prose lengths force the call

**Class:** SOFT — structural call

**Reasoning for default (A):** Book 2 split for similar word-count reasons (120K+) and the precedent is established. The rift moment at Ch19 is a natural break with a structurally satisfying cliffhanger. A 50-chapter single volume would put Book 4 at ~150K words — outside typical commercial bounds.

**Action items if confirmed:**
- Rename topology to BOOK4A_TOPOLOGY.yaml + BOOK4B_TOPOLOGY.yaml
- Update SERIES_TOPOLOGY books section to add book_4b entry
- Series count becomes 9 (or 8 with A/B labels)

---

## C7 — Bellatrix's climax fate

**Conflict:** Three options outlined in climax structure; none locked.

**Sources:**
- CLIMAX_STRUCTURE_FINAL options:
  - A. Allows rescue ("Go. Be whole. Be enough.") — stays in The Between alone
  - B. Tries to stop, fails — team fights her off, escapes despite her
  - C. Sacrifices for rescue — "I'll hold it open" — dies/disappears ensuring safety

**Proposed resolution:** **Option A (Allows rescue).** Bellatrix stays in The Between, alone.

**Class:** SOFT — pure creative call

**Reasoning for default (A):**
- Option A is the cleanest match to Bellatrix's v3 motive (her test of love succeeded; she's allowed to acknowledge it without dying or being defeated)
- Preserves her as a potential ongoing presence for Books 5-8 without requiring a comeback arc
- Option B undercuts the v3 motive (treats her as defeated antagonist, not maternal observer)
- Option C is dramatically powerful but creates closure that may foreclose her arc in later books
- The "stays alone" outcome mirrors her isolation in higher dimensions — thematically resonant

**Action items if confirmed:** Lock Option A; flag her as "in The Between, alone" for Book 5 inheritance.

---

## C8 — Eidolon's climax fate

**Conflict:** Climax structure marks as TBD (freed? dies? flees?).

**Proposed resolution:** **Freed but ambiguous — Eidolon survives, connection to Bellatrix severed, fate TBD as "wandering."** Sets up Books 5-8 reunification arc with the other emotional fragments (Hope, Joy, Rage, Grief, Love).

**Alternative options:**
- **A (proposed):** Survives, freed, wanders — seeds reunification quest
- **B:** Dies — clone husk collapses with FAERIS counterattack
- **C:** Flees — escapes to dimensional fold, future antagonist
- **D:** Redemption begun — actively allied with team by Book 5

**Class:** SOFT — pure creative call

**Reasoning for default (A):**
- Eidolon as fragment-victim (per C3 arbitration) benefits from survival to enable the reunification arc
- Books 5-8 fragment quest is a series-level structural opportunity that only exists if Eidolon survives in some form
- "Wandering / fate TBD" leaves maximum optionality for Book 5 to direct
- Active alliance (D) closes the question prematurely

**Action items if confirmed:** Lock Eidolon survives in some form; designate fate as "wandering, fragmented, connection to Bellatrix severed" for B5 inheritance.

---

## C9 — Kain's climax fate

**Conflict:** Climax structure marks as TBD (captured? fled?).

**Proposed resolution:** **Fled, still in power, weakened.** Kain remains President; CADENS crippled but not destroyed; his clone system intact.

**Alternative options:**
- **A (proposed):** Fled, still in power, weakened but unkillable individually
- **B:** Captured — public trial in Book 5
- **C:** Killed (one clone) — another clone takes over
- **D:** Deposed — removed from presidency by counter-coup

**Class:** SOFT — pure creative call

**Reasoning for default (A):**
- Most consistent with Book 2B endpoint (Kain unkillable individually due to clone system; B2B locked endpoint)
- Preserves him as ongoing institutional threat for Books 5+ (the CBT-failing phase isn't complete just because individuals are defeated — institutions outlast them)
- B and D create premature closure on the political-power thread; the series' CBT critique is partly about how institutions absorb individual heroics
- C (kill one clone) is dramatically interesting but rolls into A functionally (consciousness transfers continue)

**Action items if confirmed:** Lock Kain still in office; CADENS crippled; clone count down by 1-2 but system intact.

---

## C10 — Tess's loyal FAERIS reveal timing

**Conflict:** Mystery established (her FAERIS stays loyal after Kain's seizure), quantum entanglement theory referenced, payoff timing not set.

**Proposed resolution:** **Reveal mid-Book 4 (around Ch22 "Loyal").** Tess discovers her FAERIS bonded to her differently — quantum entanglement formed during her teleportation training, which used Ahdia's temporal abilities. The bond carries an Ahdia-signature the FAERIS preserves.

**Alternative options:**
- **A (proposed):** Mid-Book 4 reveal — quantum-bond-via-Ahdia theory confirmed in Ch22
- **B:** Hold for Book 5 — keep mystery active across the book
- **C:** Earlier reveal — Ch10 when Tess uses it to track Ahdia
- **D:** Different mechanism entirely — Director rewrites the reason

**Class:** SOFT — affects pacing

**Reasoning for default (A):** Ch22 "Loyal" is already planned as Tess's solo chapter exploring this question; payoff there is structurally placed. Holding longer risks the audience forgetting the question matters.

**Action items if confirmed:** Lock Ch22 as reveal; confirm mechanism (quantum entanglement via Ahdia training).

---

## C11 — Pioneer mech (Pio) survival

**Conflict:** Climax structure implies mech left behind in extraction. Character profile says "Pio needs repairs, team helps."

**Proposed resolution:** **Pio comes through.** Damaged severely in the kaiju fight before extraction; Rivets and team repair her over Books 5-8. Iteration-3 tech on Earth is a series-level asset and seed.

**Alternative options:**
- **A (proposed):** Pio survives, badly damaged, repaired by team
- **B:** Pio stays — Rivets had to abandon her to make the rift in time; ongoing grief
- **C:** Pio is destroyed in the extraction sequence — Rivets loses everything, twice

**Class:** SOFT — affects Rivets' arc and Book 5 asset inventory

**Reasoning for default (A):** Pio is canonically Rivets' AI companion and emotional anchor (parallel to AR-Ryu). Losing her twice — once with Iteration 3, again at extraction — risks Rivets having no remaining anchor going into Book 5. Bringing Pio through gives Rivets something to repair (forward action), and the mech is a useful series asset.

**Action items if confirmed:** Lock Pio survives the rift; flag repair-over-Book-5 as character work for Rivets.

---

## C12 — Team Diana-reveal timing

**Conflict:** When does the full team (Ben, Victor, Leah, Tess, Korede) learn Diana = Ahdia-Prime?

**Sources:**
- Ruth knows Ch14
- Rest unspecified

**Proposed resolution:** **Reveal late in Book 4B during the rescue mission (Ch46-48).** When Diana coordinates the artificial sun activation and team sees her using temporal powers openly, the cover collapses.

**Alternative options:**
- **A (proposed):** Late Book 4B (Ch46-48) — operational necessity forces reveal
- **B:** During Exile Island close quarters (Ch10+) — pressure breaks the secret
- **C:** Climax aftermath (Ch50-51) — only after Ahdia rescued, in calm
- **D:** Carries into Book 5 — secret remains active

**Class:** SOFT — affects close-quarters drama and Book 5 inheritance

**Reasoning for default (A):**
- Operational reveal (open temporal power use) is the natural breaking point — secret breaks because it must, not because someone slips
- Preserves close-quarters tension on Exile Island without forcing a premature reveal
- Climax aftermath (C) is too late — denies the team agency in their last book act
- Book 5 carryover (D) would let the lie metastasize unnecessarily

**Action items if confirmed:** Lock late-Book-4B reveal during rescue mission coordination.

---

# Summary

## Arbitrations called HARD (4)
- **C1:** 5 iterations (not 47)
- **C2:** Bellatrix maternal-obsession motive (v3 supersedes master plan)
- **C3:** Eidolon fragment-victim (canon doc supersedes master plan)
- **C5:** Ryu Matsuda (not Tanaka)

## Arbitrations called SOFT (8) — Director defaults proposed
- **C4:** Brother = Firas (whose progeny nature is the reveal, not his presence)
- **C6:** Lock A/B split at Ch19
- **C7:** Bellatrix climax — Option A (allows rescue, stays in The Between)
- **C8:** Eidolon climax — survives, wanders, fragmented
- **C9:** Kain climax — fled, still in power, weakened
- **C10:** Tess loyal FAERIS — quantum-bond-via-Ahdia, revealed Ch22
- **C11:** Pio survives extraction, repaired over Books 5+
- **C12:** Team learns Diana late Book 4B during rescue mission

## To override
Reply "override Cn: [your call]" for any you want changed. Silence = ratification.

## Action items if ratified as-is
- Update BOOK4_TOPOLOGY.yaml: move resolved conflicts to `resolved_arbitrations` section
- Update SERIES_TOPOLOGY.yaml: mark related open questions as resolved
- Prologue prose rewrite: "iteration 47" → "iteration 5" (when next touched)
- Master plan (BOOK3_MASTER_PLAN.md) flagged as superseded on iteration count, Bellatrix motive, Eidolon origin
- Ryu surname: rename "Tanaka" → "Matsuda" in Book 4 directory files (next planning pass)
- Series count: confirm 9 books (with 4A/4B) or 8 books (with combined Book 4)

---

*Crew not author. These arbitrations are proposals. Director ratifies.*
