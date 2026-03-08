# Method Actor System - Voice & Prose Generation Guide

**Companion document to METHOD_ACTOR_SYSTEM_PACKAGE.md**

This document covers the actual prose generation: character voice, scene performance, and style guidance.

---

## Table of Contents

1. [The Method Actor Concept](#the-method-actor-concept)
2. [Character Voice System](#character-voice-system)
3. [Scene Performance Format](#scene-performance-format)
4. [Narrator as Character](#narrator-as-character)
5. [Prose Style Guidelines](#prose-style-guidelines)
6. [Action Scene Techniques](#action-scene-techniques)
7. [Dialogue Craft](#dialogue-craft)
8. [Common Failure Modes](#common-failure-modes)
9. [Voice Checklist](#voice-checklist)

---

## The Method Actor Concept

### Philosophy

The Method Actor system treats Claude as a performer who:
1. **Studies the character** (loads arc tracker, knowledge state, voice patterns)
2. **Inhabits the character** (performs dialogue/internal monologue in their voice)
3. **Stays in character** (doesn't break voice, respects knowledge limits)
4. **Performs sequentially** (one character at a time, alternating)

### Why It Works

Traditional prose generation asks Claude to write "as the author." This creates a generic voice.

Method Actor asks Claude to **perform** specific characters, then assemble the performances into prose. This creates distinct, consistent voices.

### The Format

```markdown
[NARRATOR]: Setting and action description (in POV character's perception)

[AS CHARACTER_NAME, emotional context/state]:
Dialogue and internal monologue in their authentic voice
```

---

## Character Voice System

### Voice Card Structure

Every major character needs a voice card defining how they speak and think.

```markdown
### [CHARACTER NAME]

**Core Essence:** [One sentence that captures who they are]

**Background:** [Relevant history that shapes how they communicate]

**Voice Patterns:**
- [Speech pattern 1 - e.g., "Uses technical jargon"]
- [Speech pattern 2 - e.g., "Self-corrects mid-sentence"]
- [Speech pattern 3 - e.g., "Deflects with humor"]
- [Stress response - how voice changes under pressure]

**Vocabulary:**
- Level: [casual | formal | technical | mixed]
- Distinctive words/phrases: ["phrase", "another phrase"]
- Words they NEVER use: ["word", "another word"]

**Verbal Tics:**
- [Tic 1 - e.g., "starts sentences with 'Look,'"]
- [Tic 2 - e.g., "trails off when uncomfortable..."]

**Physical Tells:** (for narration)
- [Tell 1 - e.g., "adjusts glasses when thinking"]
- [Tell 2 - e.g., "goes still when suspicious"]

**Internal Monologue Style:**
- [How they think - e.g., "analytical, breaks things into steps"]
- [What they notice - e.g., "details others miss"]
- [What they miss - e.g., "emotional subtext"]

**Forbidden:**
- [Things this character would NEVER say]
- [Things they would NEVER do]

**Example Dialogue:**
"[Characteristic line that captures their voice]"

**Example Internal Monologue:**
[Characteristic thought pattern]
```

### Voice Card Examples

#### Analytical Character

```markdown
### DR. SARAH CHEN

**Core Essence:** Brilliant data scientist who processes the world through patterns and logic, but struggles with emotional intelligence.

**Background:** PhD at 24, ten years in research, recently moved from academia to corporate. Trained to see data, not people.

**Voice Patterns:**
- Uses precise language, specific numbers
- Self-correction: "[Statement]. Or rather, [correction]?"
- Notices small details others miss
- Deadpan delivery, especially when stressed
- Questions everything, trusts data over feelings

**Vocabulary:**
- Level: Technical when comfortable, stilted casual when trying to connect
- Distinctive: "statistically speaking," "the data suggests," "let's be precise"
- Never uses: Slang, expletives, emotional hyperbole

**Verbal Tics:**
- Starts explanations with "So," or "The thing is,"
- Quantifies everything ("approximately 73% certain")
- Trails off when realizing she's over-explaining

**Physical Tells:**
- Adjusts glasses when processing
- Taps fingers in patterns when thinking
- Goes very still when something doesn't add up

**Internal Monologue Style:**
- Breaks problems into components
- Notices numerical/pattern details
- Misses emotional subtext until later
- Self-critical about social missteps

**Forbidden:**
- Would never make decisions based on "gut feeling" without trying to rationalize
- Would never use imprecise language when precision matters
- Would never ignore contradictory data

**Example Dialogue:**
"The numbers don't lie. They just don't tell the whole story yet."

**Example Internal Monologue:**
Three anomalies in six months. That was outside the expected variance by—she did the math—approximately 4.7 standard deviations. Something was wrong. She just couldn't see what yet.
```

#### Traumatized Character

```markdown
### MARCUS REYES

**Core Essence:** Former soldier carrying invisible wounds, masks pain with dark humor and controlled distance.

**Background:** Two tours overseas, medical discharge, now works security. Hypervigilant, emotionally guarded, loyal to a fault once trust is earned.

**Voice Patterns:**
- Clipped, military-efficient speech
- Dark humor as deflection
- Understates serious things, overstates trivial things
- Gets quieter, not louder, when angry
- Long pauses before emotional admissions

**Vocabulary:**
- Level: Casual with military precision underneath
- Distinctive: "Copy that," "roger," tactical terms used ironically
- Never uses: Words that make him sound vulnerable, therapy-speak

**Verbal Tics:**
- Answers questions with questions
- "Yeah, no" and "No, yeah" as stalling tactics
- Changes subject when conversation gets too real

**Physical Tells:**
- Scans exits when entering rooms
- Positions himself with back to wall
- Hands never fully still
- Jaw tightens before he shuts down

**Internal Monologue Style:**
- Threat assessment runs constantly
- Memories intrude without warning (brief, visceral)
- Talks himself down from reactions
- Notices who's armed, who's nervous, who's lying

**Forbidden:**
- Would never ask for help directly
- Would never admit fear in the moment
- Would never let someone walk into danger if he could prevent it

**Example Dialogue:**
"I'm fine." [He wasn't fine. He was never fine. But fine was what you said.]

**Example Internal Monologue:**
Three exits. Two visible weapons. One guy who kept touching his waistband like he wasn't used to carrying. Amateur hour. Marcus made himself relax. Made his shoulders drop. Made his face do the thing that looked like he wasn't cataloging every threat in the room.
```

#### Pop-Culture Reference Character

```markdown
### JAMIE TORRES

**Core Essence:** Anxious hermit whose only frame of reference for human interaction is television, uses pop culture to process and deflect.

**Background:** Social anxiety, rarely leaves apartment, relationships primarily through screens. Genuinely kind but struggles to connect directly.

**Voice Patterns:**
- Pop culture references for everything
- Rambling run-ons when stressed
- Self-deprecating internal commentary
- Casual/contemporary language ("What the actual hell?")
- Deadpan acceptance of absurd situations

**Vocabulary:**
- Level: Casual, contemporary, heavy on references
- Distinctive: Specific show/episode references, not vague ("Season 3 Buffy energy")
- Never uses: Formal language, academic terms (feels fake to them)

**Verbal Tics:**
- "I mean," as sentence starter
- Trails off with "so... yeah"
- Talks to self in third person when stressed

**Physical Tells:**
- Picks at cuticles when anxious
- Laughs at own jokes when no one else does
- Eyes dart to exits in crowds

**Internal Monologue Style:**
- TV references as processing framework
- Self-deprecating running commentary
- Notices absurdity before danger
- Pop culture IS emotional vocabulary

**Forbidden:**
- Would never be smoothly confident
- Would never make eye contact easily
- Pop culture references should reveal isolation, not just be "quirky"

**Example Dialogue:**
"This is very Season 4 Battlestar. You know, when everything was already bad but they hadn't hit rock bottom yet? We're in the part where you think, 'surely it can't get worse,' and then—" She gestured vaguely. "—it gets worse."

**Example Internal Monologue:**
This was fine. This was totally fine. This was the part of the episode where everything seemed fine and then the commercial break hit and you realized nothing was fine. Jamie had seen enough TV to know how this worked.
```

---

## Scene Performance Format

### Full Scene Structure

```markdown
## BACKSTAGE (Context for this scene):

**Scene ID:** [unique identifier]
**Location:** [Where and when]
**Participants:** [Characters present]

**Character States:**
- [Char1]: [Brief state summary]
  - Knows: [relevant knowledge]
  - Emotional: [current state]

- [Char2]: [Brief state summary]
  - Knows: [relevant knowledge]
  - Emotional: [current state]

**Touchpoints:**
- A: [Starting state—what's true when scene begins]
- B: [Ending state—what must be true when scene ends]

**Constraints:**
- [What cannot happen]

**Requirements:**
- [What must happen]

---

## ON STAGE NOW:

[CURTAIN RISES]

[NARRATOR]: [Setting established in POV character's perception style]

[AS CHAR1, emotional_context]:
[Their dialogue and/or internal monologue]

[AS CHAR2, emotional_context]:
[Their response]

[NARRATOR]: [Action, movement, description]

[AS CHAR1, shifted_emotional_context]:
[Continued performance]

[Continue until touchpoint B achieved]

[END SCENE]

---

## DIRECTOR NOTES:

- **Requirements met:** [Checklist of what was accomplished]
- **Constraints respected:** [Verification nothing forbidden happened]
- **State changes:** [What changed for each character]
- **Seeds planted:** [Foreshadowing elements added]
- **Propagates to next scene:** [Consequences that carry forward]
```

### Performance Notes

1. **Stay in character** — Each [AS CHARACTER] block uses ONLY that character's voice, vocabulary, and perspective

2. **Respect knowledge limits** — Characters cannot reference things they don't know

3. **Signal emotional shifts** — The "emotional_context" tag helps Claude maintain consistency within a beat

4. **Narrator is not neutral** — If there's a POV character, the narrator sees through their eyes

---

## Narrator as Character

### POV-Filtered Narration

The narrator in close third-person is NOT omniscient. They perceive through the POV character's lens.

**Neutral narrator (avoid):**
> The office was sparse. A desk, two chairs, a filing cabinet. Sarah entered.

**POV-filtered narrator (prefer):**
> Three objects. Desk, two chairs, filing cabinet. Sarah categorized the room in the time it took to cross the threshold. Sparse was generous. Spartan was accurate.

### Filter Rules

When narrating through a POV character:

1. **Descriptions reflect what they notice**
   - Analytical character counts and categorizes
   - Anxious character notes exits and threats
   - Artistic character notices color and composition

2. **Other characters are seen through their biases**
   - POV character who distrusts someone describes them suspiciously
   - POV character attracted to someone notices different details

3. **Prose rhythm matches mental state**
   - Calm: Longer, flowing sentences
   - Anxious: Choppy, fragmented
   - Dissociating: Dreamlike, disconnected

4. **What they miss reveals character**
   - Analytical character misses emotional subtext
   - Traumatized character misses joy
   - Self-absorbed character misses others' needs

### Example: Same Scene, Different POV

**Through analytical Sarah:**
> Three people. Two she recognized from the morning briefing, one unknown. The unknown man stood with his weight forward, hands clasped—defensive posture, or nervous? Insufficient data. She filed it away.

**Through traumatized Marcus:**
> Three people. The two from this morning—no threat assessment needed, he'd already done it. The new guy was the variable. Weight forward. Hands visible but positioned to grab. Former military or trained security, trying to look casual. Marcus's hands stayed loose. Stayed ready.

**Through anxious Jamie:**
> Three people, which was three more than Jamie wanted to deal with today. The two from this morning were fine, probably, they seemed fine, but the new guy had that energy. That "I'm important and you should know it" energy. Like a minor villain in episode three who turns out to be the season's big bad.

---

## Prose Style Guidelines

### Pacing Fundamentals

**Fast pacing tools (use in action, tension):**
- Short sentences (5-10 words)
- Sentence fragments
- Heavy dialogue (60%+)
- Action beats between lines
- Minimal description

**Slow pacing tools (use sparingly, for breathing room):**
- Longer sentences (20+ words)
- Descriptive passages
- Internal monologue
- Scene-setting

### Sentence Structure

**Target mix:**
- Simple sentences: 60-70% (primary workhorse)
- Compound sentences: 15-20% (rhythm variation)
- Complex sentences: 5-10% (depth when needed)
- Fragments: 5-10% (impact moments)

**Average sentence length:** 10-15 words

### Show Don't Tell (With Nuance)

**Don't just show emotion:**
> Her hands shook. Her eyes were wet. Her voice cracked.

**Show through character-specific behavior:**
> Sarah did the math on her heartrate—elevated, approximately 95 BPM—because that was easier than naming what she felt.

> Marcus went quiet. Not the quiet that meant he was thinking. The quiet that meant he'd stopped thinking so he wouldn't have to feel.

### Active Voice

**Target:** 90%+ active voice

**Passive (avoid):**
> The door was opened by Marcus.

**Active (prefer):**
> Marcus opened the door.

**Exception:** Passive works when the actor is deliberately obscured or unknown:
> The files had been accessed sometime between midnight and six AM.

---

## Action Scene Techniques

### Structure

```
[Setup: 1-2 sentences max]
[Rapid beats: Fragments okay, visceral verbs]
[Character reaction mid-action]
[Sensory detail: sight, sound, impact]
[Consequence: Immediate]
```

### Example

> [Setup] Garden approaching fast.

> [Rapid beats] Jamie teleported mid-fall. They appeared back in the office for a split second—surrounded by guards—then teleported again. Four of them now. Still falling.

> [Reaction] This was fine. This was totally fine. This was definitely going to be fine.

> [Sensory] Ground rushing up.

> [Consequence] She teleported one more time. They hit grass instead of concrete. Her ankle turned. Sharp pain. Alive.

### Action Scene Rules

1. **No long descriptions during action** — Save for before/after
2. **Visceral verbs** — dove, bolted, slammed, cracked
3. **Character voice in the chaos** — Internal reactions in their voice
4. **Consequences immediate** — Injuries, exhaustion, damage
5. **Short paragraphs** — One beat per paragraph during peak action

---

## Dialogue Craft

### Formatting

```
Standard dialogue:
"This is insane," Sarah said.

Internal monologue (close POV):
This was insane. Certifiably, statistically, demonstrably insane.

Action beats instead of tags:
"This is insane." Sarah closed the file. "But the data's clear."
```

### Dialogue Rules

1. **Keep it snappy** — Most lines under 150 characters
2. **Use contractions** — "won't", "she'd", "they're"
3. **Break grammar rules** — Fragments, interruptions, trailing off
4. **Distinct character voice** — Each person sounds different
5. **Action beats over tags** — "He ducked" not "he said, ducking"

### Subtext

Characters rarely say exactly what they mean:

**On the nose (avoid):**
> "I'm angry that you lied to me."

**With subtext (prefer):**
> "The numbers in your report." She set the file down too carefully. "They're interesting."

---

## Common Failure Modes

### Voice Drift

**Problem:** Character starts sounding generic or like another character.

**Fix:** Re-read voice card before each [AS CHARACTER] block. Check:
- Are they using their vocabulary?
- Are their verbal tics present?
- Would they actually say this?

### Knowledge Leakage

**Problem:** Character references something they shouldn't know yet.

**Fix:** Check knowledge gates in manifest before writing. For each line, ask: "How does this character know this?"

### Emotional Whiplash

**Problem:** Character's emotional state jumps without transition.

**Fix:** Use the emotional_context tag to track state through scene. If emotion shifts, show the moment of shift.

### Purple Prose

**Problem:** Overly ornate, flowery description.

**Fix:** Would this POV character think this way? An anxious millennial wouldn't think in Victorian sentences.

### Talking Heads

**Problem:** Dialogue with no action, setting, or physical grounding.

**Fix:** Insert action beats. Characters exist in space.

---

## Voice Checklist

### Before Writing Each Scene

- [ ] Loaded character arc trackers for all participants
- [ ] Reviewed voice cards for all speaking characters
- [ ] Verified knowledge states for this chapter
- [ ] Identified POV character for narrator filter
- [ ] Noted emotional starting points

### During Scene Performance

For each [AS CHARACTER] block:
- [ ] Using their vocabulary, not generic words
- [ ] Verbal tics present (at least occasionally)
- [ ] Would they actually say/think this?
- [ ] Are they only referencing what they know?
- [ ] Emotional state consistent with context tag

For [NARRATOR] blocks:
- [ ] Filtered through POV character's perception
- [ ] Noticing what they would notice
- [ ] Missing what they would miss
- [ ] Prose rhythm matches mental state

### After Scene Draft

- [ ] Read dialogue aloud — does each character sound distinct?
- [ ] Check for knowledge leakage
- [ ] Verify emotional arc makes sense
- [ ] Confirm touchpoint B was reached
- [ ] Note any state changes for propagation

---

## The Golden Rules

1. **Would this character actually say/think this?**
   - If no → rewrite in their voice

2. **Does this reflect their knowledge state?**
   - If they shouldn't know it → cut it

3. **Is the narrator filtered through POV?**
   - If omniscient → rewrite through character's perception

4. **Is this specific enough?**
   - Vague descriptions → character-specific details

5. **Am I trusting the reader?**
   - Over-explained emotion → subtext and behavior

---

*Voice & Prose Guide Version 1.0 — December 2025*
