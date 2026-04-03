# Prose Voice Design Problem

**Date:** 2026-04-03
**Status:** Principle solved. Implementation open.

---

## The Discovery

Cross-book prose audit (2026-04-03) of Book 1 (~74K words) and Book 2A (~48K words) revealed an amplification mechanism in AI-assisted writing. The AI discovers a default prose pattern early in production and reaches for it increasingly under pressure. Different books develop different mutations from different early defaults — Book 1 amplified fragments (1,023 total, 9x escalation early→late), Book 2A amplified "the particular [noun] of" (48 instances) and em-dash self-correction. Same mechanism, different symptoms.

The escalation in Book 1 mapped to a literal boundary: early chapters were the author's original pre-AI draft. Later chapters were AI-revised. The "disease" is the AI's default narrator voice replacing the author's voice as it takes on more of the writing.

## The Key Variable

The ratio of AI-to-human prose isn't what determines quality. **The operation the AI performs is.**

**Embodiment** ("be this character, do what you'd do") produces voice naturally. This is what happened in Remanence — characters were co-created with the AI, the AI was told to *be* them, and the resulting prose survived disclosure scrutiny. No one flagged it as AI writing.

**Description** ("write this character based on these facts") produces narrator-with-character-facts. This is what happened in Go Squad — the AI was handed characters with established voices from the author's original draft and asked to write *about* them. The result: a single homogeneous narrator voice across all POV characters (Grade C/C+), with character differentiation only in dialogue (B+/A-) where the steward system provided genuine embodiment.

Same tool. Same author. Fundamentally different operation. The output quality tracks to the operation, not the volume.

## The Missing Layer

The production system has a gap:

```
Character Bible       → WHO they are (facts, arc, relationships)
Steward Prompt        → HOW they interpret events (triplet, moves, faction)
[MISSING LAYER]       → HOW the narrator sounds inside their head
Prose Output          → The actual sentences
```

This gap is where the AI defaults to its own narrator voice. The missing layer is not a "styleguide" — it's a set of **embodiment instructions** that let the AI *be* each character the way it naturally was its own characters in Remanence.

## The Proof of Concept

The Bellatrix steward output (Book 2B Run 1) demonstrates the mechanism:

- **Triplet:** Black Queen (waits, then acts once) / Black Bishop on f8 (never moves, witnesses everything) / Black Knight (infiltrates from inside)
- This isn't characterization. It's a **cognitive architecture** — a repeatable operation the AI applies to every moment. "Read this through the queen that waits, the bishop that witnesses, the rook that acts once."
- The voice follows automatically. Bellatrix's output is declarative, patient, never self-corrects, never fragments for emphasis — because the architecture structurally prevents those patterns.

Compare: Ben's steward says "military/analytical/list-making." That's description, not architecture. Under pressure, the prose agent has no repeatable operation to apply, so it defaults to its own narrator voice. Result: Ben sounds like Ahdia in the manuscript.

## What the Embodiment Instruction Must Specify

1. **Cognitive architecture under different states.** Not "Ben is analytical" but "Ben under emotional threat reverts to spatial inventory — counts exits, measures distances, catalogues physical facts. The sentences become lists that pretend they aren't emotional."

2. **What the character does NOT do.** Negative constraints as firewall against narrator bleed. Bellatrix never asks questions in narration. Never self-corrects mid-clause. Ruth doesn't use metaphor. These are as load-bearing as the positive traits.

3. **The repeatable operation.** A frame the AI applies sentence-by-sentence. Ben's: "Every observation is an assessment. Every assessment implies an action. If the action is impossible, the sentence stops." Ahdia's: "Observe, deflect with humor, circle back to the real feeling."

4. **Grief/stress register.** How does this character carry what they can't metabolize? The bishop on f8 — present at every move, contributing nothing, unable to be captured — is a prose-level instruction for how Bellatrix holds Geneva's death. Each character needs the equivalent.

5. **Structural resistances to accumulation.** Which AI-default tics will naturally bleed in over sessions, and how does this character's architecture prevent them? Bellatrix doesn't em-dash because she doesn't interrupt herself. That's a resistance built into the architecture, not a rule to remember.

## The Open Design Problem

**The principle is solved.** Embodiment instructions with cognitive architecture produce distinct, AI-resistant voice. The triplet mechanism works. Remanence proves the outcome is achievable.

**The implementation for existing characters is open.** Remanence characters were co-created with the AI from scratch — embodiment was natural. Go Squad characters already exist. They have prose in the world. They have established voices from the author's original draft. Someone has to design their cognitive architectures carefully from existing evidence — reverse-engineering the embodiment instruction from finished prose rather than building it alongside the character.

This is a different design problem than Remanence faced:

| | Remanence | Go Squad |
|---|---|---|
| Characters | Co-created with AI | Pre-existing |
| Voice source | Emerged from embodiment | Exists in author's original draft |
| AI operation | "Be yourself" | "Write this person" |
| Design task | None (natural) | Reverse-engineer architecture from existing prose |
| Risk | Low (voice is native) | High (AI replaces voice with its own defaults) |

The triplet-as-cognitive-architecture approach works for both — but for existing characters, the triplet must be **derived from** the author's prose, not invented fresh. The author's early Go Squad chapters (pre-AI) are the source material for what each character's narrator voice actually sounds like before the AI gets involved.

## Remediation Sequence

1. **Wait for beta reader 2** (Book 1). Beta reader 1 flagged "first draft" feel but praised emotional beats, trope subversion, and action clarity. Unbiased second read provides tolerance data.
2. **Combine beta feedback + audit data** → build remediation protocol. What readers catch tells you what matters. What they don't catch tells you about tolerance.
3. **Build embodiment instructions per character** from combined picture — derived from the author's original prose + the audit's negative-space data (what *doesn't* work).
4. **Revision pass on Book 1** using the embodiment instructions.
5. **Book 2B prose generation** uses embodiment instructions from the start — never develops the disease.

## Audit Data (Summary)

### Book 1

| Metric | Value | Notes |
|--------|-------|-------|
| Not-constructions | 113 | Ch1-11: only 4. Ch29 alone: 10. |
| "Still" | 125 (1.68/1K) | Ch24: 6.04/1K. Final act = 35% of all uses. |
| "Already" | 55 (0.74/1K) | Normal range. |
| Fragments | 1,023 | 9x escalation early→late. Ch26: 89 fragments. |
| Em-dashes | 1.9/1K early → 10.4/1K late | 5.5x increase, all POVs. |
| "The particular" | 0 | Hadn't developed yet. |
| POV voice | Grade C | Back half homogenizes completely. |

### Book 2A

| Metric | Value | Notes |
|--------|-------|-------|
| Not-constructions | 119 | ~72 correction/redefinition + ~30 negation-correction |
| "Still" | 133 (2.8/1K) | Ch7/Ch8: 6.1/1K |
| "Already" | 64 (1.3/1K) | Ch5: 6.4/1K |
| Fragments | 87 | Controlled. Different mutation than Book 1. |
| "The particular" | 48 | Across every POV. Book 2A's signature tic. |
| POV voice | Grade C+ | Dialogue B+/A-, narration C-/D+. |

---

*This document captures the design problem as understood on 2026-04-03. The principle is clear. The implementation — building embodiment instructions for characters who already exist — is the next design challenge, blocked on beta reader 2 feedback.*
