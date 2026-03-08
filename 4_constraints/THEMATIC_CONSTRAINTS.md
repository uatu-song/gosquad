# Go Squad - Thematic Constraints

**Version:** 1.0
**Purpose:** Protect thematic integrity. These constraints prevent LLM drift from the series' core meaning.

---

## Core Thesis

> "You don't have to be fixed to be worthy."

The gift (powers) arrives without consent. Worthiness is irrelevant to receiving it. The question is what you do WITH the gift, not whether you deserve it.

---

## BLOCKING Constraints

These will cause draft rejection. Non-negotiable.

### The Gift Paradigm

| Status | Statement |
|--------|-----------|
| WRONG | Characters earning/deserving powers through virtue |
| WRONG | Powers as punishment or reward |
| WRONG | "You deserve this" / "You've proven yourself" |
| WRONG | Powers going to the "right" people for moral reasons |
| RIGHT | Powers arrive without consent |
| RIGHT | Worthiness is irrelevant to power |
| RIGHT | The question is what you DO with the gift |
| RIGHT | Bad people can have powers; good people can lack them |

**Detection Patterns:**
- "prove.*worthy"
- "earn.*right"
- "deserve.*power"
- "chosen.*because"
- "meant to have"

---

### Binary Resolution (Ahdia's Arc)

| Status | Statement |
|--------|-----------|
| WRONG | Ahdia finding "the answer" |
| WRONG | Clear good/evil resolution |
| WRONG | "Now I understand everything" |
| WRONG | Her mental health "fixed" by the end |
| WRONG | Either/or resolution to complex problems |
| RIGHT | Both/and rather than either/or |
| RIGHT | Acceptance without resolution |
| RIGHT | DBT progression: holding contradictions |
| RIGHT | Growth that doesn't mean "cured" |

**Source:** Ahdia's arc is CBT→DBT: from trying to fix herself (failure) to accepting herself (growth). She doesn't become "healthy"—she becomes someone who can function while still struggling.

**Detection Patterns:**
- "finally understood"
- "realized the truth"
- "the answer was"
- "everything made sense"
- "was healed"

---

### Villain Complexity

| Status | Statement |
|--------|-----------|
| WRONG | Kain as mustache-twirling evil |
| WRONG | Easy moral clarity for antagonists |
| WRONG | Villains who are stupid or cartoonishly malevolent |
| WRONG | Any character existing only to be refuted |
| RIGHT | Every antagonist believes something defensible |
| RIGHT | The audience can feel the pull of each position |
| RIGHT | Kain's logic is coherent (even if his actions are wrong) |
| RIGHT | Eidolon's fear-amplification has a purpose |

**Detection Patterns:**
- "evil" (used unironically as descriptor)
- "cackled"
- "gloated"
- "obviously wrong"
- "stupid enough to believe"

---

### Power Mechanics Consistency

| Status | Statement |
|--------|-----------|
| WRONG | Temporal powers with no cost |
| WRONG | Ignoring cellular degradation |
| WRONG | Powers working differently than established |
| WRONG | Eidolon CREATING fear (can only amplify) |
| WRONG | AR-Ryu having memories he shouldn't have |
| RIGHT | Every temporal use has physical cost |
| RIGHT | Baseline tracking is narrative, not just mechanical |
| RIGHT | Eidolon amplifies EXISTING fear |
| RIGHT | AR-Ryu only knows what was uploaded |

**Source:** `story_bibles/SERIES_MECHANICS.md`

---

### Knowledge Gates

| Status | Statement |
|--------|-----------|
| WRONG | Characters knowing things they shouldn't know yet |
| WRONG | Ahdia knowing Ryu loves her (Book 2) |
| WRONG | Ruth knowing the full degradation timeline (early Book 2) |
| WRONG | Prime/Bellatrix reveals before designated chapters |
| RIGHT | Knowledge gates per chapter enforced |
| RIGHT | Dramatic irony used intentionally |
| RIGHT | Reader may know more than characters |

**Source:** `character_arcs/CHARACTER_STATE_INDEX.yaml`

---

## WARNING Constraints

These will flag for human review. May be acceptable in context.

### Lecture Mode

| Status | Statement |
|--------|-----------|
| WRONG | Characters explaining the theme |
| WRONG | Speeches about power/responsibility |
| WRONG | Debates that map cleanly to real-world positions |
| WRONG | "Let me explain why this matters" |
| RIGHT | Embody, don't articulate |
| RIGHT | Actions and images carry weight |
| RIGHT | The reader infers; characters live |

**Detection Patterns:**
- Monologues > 200 words on theme
- "you see.*the problem is"
- "what you don't understand"
- "the real issue is"

---

### Gratuitous Darkness

| Status | Statement |
|--------|-----------|
| WRONG | Violence without narrative purpose |
| WRONG | Trauma porn (dwelling on suffering for effect) |
| WRONG | Hopelessness without counterweight |
| RIGHT | Dark moments that reveal character |
| RIGHT | Violence with consequences |
| RIGHT | Hope earned through struggle |

---

### Easy Resolution

| Status | Statement |
|--------|-----------|
| WRONG | Problems solved by one conversation |
| WRONG | Misunderstandings cleared up immediately |
| WRONG | Conflicts that don't leave residue |
| RIGHT | Resolution that takes time and action |
| RIGHT | Cleared misunderstandings that still leave scars |
| RIGHT | Progress that's two steps forward, one back |

---

## Thematic Pillars (What TO Write)

### 1. Found Family
The Go Squad becomes family. Not replacement family—additional family. Chosen bonds alongside blood bonds.

### 2. Functional Imperfection
Characters don't get "fixed." They get functional. Ahdia at series end still has depression—she just knows how to work with it.

### 3. Cost of Power
Every power has a price. Temporal manipulation costs cellular integrity. Leadership costs relationships. Secrets cost trust.

### 4. Both/And
Not either/or. Ahdia can be a hero AND a mess. Kain can be an antagonist AND have valid points. Ruth can be a caretaker AND need care.

### 5. Gift ≠ Deserving
Powers arrive. You don't earn them. You don't deserve them. They just ARE, and now you have to figure out what to do.

---

## Integration with Other Constraints

This file handles **thematic** constraints.

For **factual** constraints (who knows what, character details): `context/negative_constraints.md`

For **knowledge gates** (per-chapter): `character_arcs/CHARACTER_STATE_INDEX.yaml`

For **voice** constraints: `GOSQUAD_PROSE_VOICE.md`

---

## Validation Process

Before submitting a chapter draft:

1. Check against BLOCKING constraints above
2. Check against `context/negative_constraints.md` for factual issues
3. Verify knowledge gates for this chapter
4. Flag any WARNING constraints for human review

---

*Thematic Constraints Version 1.0 — December 2025*
