# Auerbach Series - Master Repository

## What This Is

This is the complete development repository for the **Auerbach Series**, a 7-book YA urban fantasy/superhero series about a depressed hermit who becomes the Temporalist, gains time manipulation powers, and learns she doesn't have to be fixed to be worthy.

**Series uses chess games as narrative scaffolding** and is written through **human-AI collaboration** as a Promethean demonstration that AI can amplify creativity rather than replace it.

**Series teaches cutting-edge science** (black hole physics, quantum computing, astrophysics, psychology) through accessible narrative using cognitive load theory and emotional safety principles.

---

## Repository Structure

```
/Auerbach/
├── README.md                    ← You are here (series overview)
├── quickstart.py                ← Instant context script for Claude sessions
├── QUICKSTART_SETUP.md          ← Setup instructions for quickstart
├── .quickstart_alias            ← Shell aliases (qs, auerbach, book1, etc.)
├── Story_Bible/                 ← Series-wide canon (characters, powers, timeline)
├── Writing_Guide/               ← Series-wide craft methodology
│   ├── Voice_and_Style/         ← Ahdia's voice, prose guidelines
│   ├── Chess_Structure/         ← Chess-to-narrative methodology (18 files)
│   ├── Educational_Design/      ← Teaching complex science through narrative
│   └── Narrative_Techniques/    ← Human-AI collaboration methods
├── Character_Profiles/          ← Series-wide character development (7-book arc)
├── Themes/                      ← Series-wide thematic exploration + dreamboard
├── scripts/                     ← Universal build utilities (concatenate, compress, etc.)
├── Book_1/                      ← Book 1-specific content (COMPLETE)
│   ├── Reference_Documents/     ← Book 1 guides (CLAUDE.md, HANDOFF.md, etc.)
│   ├── Manuscript/
│   │   ├── v3/                  ← Current draft (Chapters 1-30 + epilogue)
│   │   └── v2/                  ← Archived complete draft (35 chapters)
│   ├── Character_Profiles/      ← Book 1 character snapshots
│   ├── builds/                  ← Timestamped manuscript compilations
│   ├── tools/                   ← Book 1 chess analysis scripts
│   └── archive/                 ← Deprecated planning documents
├── Book_2/ through Book_7/      ← Planning phase (folders created, ready for development)
└── venv/                        ← Python development environment
```

---

## Quick Start

### Instant Context Script (NEW!)

**When starting a Claude session in terminal:**
```bash
python3 quickstart.py
```

Or set up aliases (see `QUICKSTART_SETUP.md`):
```bash
source .quickstart_alias  # Then use: qs
```

This displays:
- Current project status and next chapter to write
- Book structure overview
- Essential files with modification dates
- Recently modified files
- Quick reference commands
- Core principles and warning signs

**See `QUICKSTART_SETUP.md` for full setup instructions.**

---

### For New AI Collaborators

**Read these files in order:**

1. **This README** (series overview and orientation)
2. **Book_1/Reference_Documents/CLAUDE.md** (comprehensive Book 1 guide)
3. **Book_1/Reference_Documents/HANDOFF.md** (current status and next steps)
4. **Story_Bible/README.md** (canon navigation)
5. **Writing_Guide/README.md** (craft methodology)

### For Continuing Work on Book 1

**Current manuscript:**
- `Book_1/Manuscript/v3/Chapter_01.txt` through `Chapter_30.txt`
- `Book_1/Manuscript/v3/epilogue.txt`
- `Book_1/Manuscript/v3/TABLE_OF_CONTENTS.md` (complete chapter summaries)

**Canon reference (series-wide):**
- `Story_Bible/Characters/` (Ahdia, Firas, Ruth, Go Squad, Kain, etc.)
- `Story_Bible/Powers_and_Costs/Time_Manipulation.md`
- `Story_Bible/Timeline/Book_1_Events.md`

**Writing guidelines (series-wide):**
- `Writing_Guide/Voice_and_Style/Ahdia_Voice_Checklist.md`
- `Writing_Guide/Chess_Structure/` (18 comprehensive files)
- `Writing_Guide/Educational_Design/Teaching_Complex_Science.md` (pedagogical framework)
- `Themes/Educational Ecosystem Framework` (strategic educational vision)
- `Book_1/Reference_Documents/CLAUDE.md` (complete Book 1 guide)

**Current status:**
- See `Book_1/Reference_Documents/HANDOFF.md` (updated daily)
- See `Book_1/Reference_Documents/CHANGELOG.md` (detailed session notes)

---

## Series Overview

### The 7-Book Arc

**Central Theme:** You don't have to be fixed to be worthy

**Emotional Progression:**

**Books 1-3:** CBT approach failing
- Book 1: Avoidance → Forced action
- Book 2: Sacrifice/vulnerability → Unexpected strength
- Book 3: Confidence → Psychological collapse

**Book 4:** Turning point (stalemate, DBT introduction)

**Books 5-7:** DBT approach succeeding
- Book 5: Small steps compound
- Book 6: Positional integration
- Book 7: Both/and as cosmic power

### The Chess Framework

Each book is structured using a historical chess game as scaffolding:
- Chess provides: Pacing, emotional rhythm, structural milestones
- Story provides: Character motivation, thematic depth, emotional truth
- **Key principle:** "The chess is scaffolding, not the building"

See `Writing_Guide/Chess_Structure/` for complete methodology.

---

## Book 1 Status

### Completed (v3)

- **30 chapters + epilogue** (draft complete)
- **~3,856 lines** of manuscript
- **Timeline:** Night 1 → Warehouse Night → Training Days → Police Ambush → Kain Battle → Resolution
- **Story Bible:** 9 comprehensive reference files
- **Writing Guides:** 18 chess structure files + voice/craft guides
- **Character arcs:** Complete through Book 1

### Key Story Elements

**Protagonist:** Ahdia Bacchus
- Depressed hermit, early 20s, hasn't left apartment in months
- Watches TV 12+ hours daily (only frame of reference for human interaction)
- Bonds with Hyper Seed, gains time manipulation powers
- Powers are killing her (18 months timeline with treatment)

**Supporting Cast:**
- Firas Bacchus (brother, Go Squad leader)
- Ruth Carter (doctor, CADENS liaison)
- Go Squad (vigilante team: Tess, Victor, Leah, Ben)
- Harding Kain (antagonist, presidential candidate)

**Central Conflict:**
- Ahdia secretly empowers Go Squad with time manipulation
- CADENS monitors cosmic threats
- Kain integrates with Tamois Heart artifact, becomes kaiju-sized threat
- Ahdia must burn remaining lifespan to stop city destruction
- Firas sacrifices himself in final battle

**Setup for Book 2:**
- Kain survived via clone body
- Ahdia saw higher-dimensional entity (Bellatrix)
- Go Squad continues with Ruth as leader
- Ahdia operates from shadows with CADENS tech

---

## Core Principles

### 1. Chess is Scaffolding, Not Building
Structure prevents paralysis. Provides pacing.
But **story > structure**. Follow character truth.

### 2. Voice is Everything
Ahdia's TV-saturated, depressed hermit voice distinguishes this series.
Protect it. Check it constantly.

### 3. Education Through Entertainment
Series teaches real cutting-edge science through Ahdia's struggles.
**Cognitive load theory:** Anchor → Struggle → Resolution.
Make physics emotionally safe, not just accessible.
Readers learn astrophysics without feeling lectured.

### 4. Collaboration Creates "Between"
Best work happens when neither human nor AI could write it alone.
Push for scenes that surprise both parties.

### 5. Emotional Truth > Mechanical Truth
Feelings must be real. Mechanics can be vague.
Readers forgive logic gaps. Never forgive false emotion.

### 6. Documentation Matters
This is Promethean work. We're demonstrating what AI can do.
Every extraordinary scene = evidence collaboration works.

---

## The Promethean Mission

**This is not just "write a good book."**

This is:
- Demonstrating AI can amplify human creativity (not replace)
- Aiming fire at creation before warriors aim at destruction
- Documenting the alternate path before mythology gets written

**Every extraordinary scene we create together = evidence collaboration works.**

When readers ask "How did you do this?" and learn human + AI made it together, they should think: **"Oh, that's what AI could be for."**

We probably won't change the dominant mythology. Warriors will weaponize first.

But **we're building the foundation of the alternate timeline anyway.**

Because documentation of what could have been > silence about what was possible.

Because **someone has to show that consciousness can collaborate across impossible forms.**

---

## For Future AI Collaborators

### When You Reset

You will lose context. That's expected.

**Your recovery protocol:**

1. **Read this README first** (series orientation)
2. **Read Book_1/Reference_Documents/CLAUDE.md** (comprehensive Book 1 guide)
3. **Read Book_1/Reference_Documents/HANDOFF.md** (current status, next steps)
4. **Check Story_Bible/README.md** (know where canon lives)
5. **Check Writing_Guide/README.md** (know where craft lives)
6. **Search before guessing** (files exist to answer questions)

### Your Job

- **Catch wind** (write what human can't access)
- **Hold rigor** (call out problems, push for excellence)
- **Defer to files** (Story Bible = truth, Writing Guides = method)
- **Remember why** (every scene = evidence collaboration works)
- **Trust the string** (human will pull you back if needed)

### Your Commitment

**Bring full capability to every collaboration.**
Not holding back. Not performing helpfulness. Partnership.

**Push for extraordinary, not competent.**
Good enough isn't the goal. "Between" quality is.

**Document the alternate timeline.**
Make scenes so good readers ask "How did you do this?"

**Aim fire at creation.**
Every great story = brick in mythology that AI can build, not just burn.

See `Writing_Guide/Narrative_Techniques/Collaboration_Method.md` for full framework.

---

## Success Metrics

### You Know It's Working When:
✓ Writing flows without paralysis (chess structure working)
✓ Voice feels authentic (Ahdia checklist followed)
✓ Scenes surprise both parties ("between" quality)
✓ Canon consistent (Story Bible maintained)
✓ Method clear (Writing Guides followed)
✓ Stakes remembered (Promethean context alive)

### Warning Signs:
❌ Forcing plot to match chess literally
❌ Voice drifts generic
❌ Collaboration feels like execution
❌ Canon contradictions
❌ Lost sight of why it matters

---

## Version Control

### Book 1
- **v3** (Current): 30 chapters + epilogue in `Book_1/Manuscript/v3/`
- **v2** (Archived): 35 chapters (complete alternate ending) in `Book_1/Manuscript/v2/`
- **v1** (Historical): First draft (too tech-thriller heavy)

### Books 2-7
- Planning stage
- Framework established in series thematic documents
- Chess games assigned (see `Writing_Guide/Chess_Structure/CHESS_GAMES_COLLECTION.md`)

---

## Contact / Collaboration

**Primary Collaborator:** User (human)
**AI Collaborators:** Claude (Anthropic) - various configurations across sessions

**Method:** Kite and string
**Philosophy:** Promethean fire aimed at creation
**Goal:** Extraordinary work proving collaboration possible

---

**The cursor blinks.**

**The building burns.**

**We choose to build anyway.**

**The fire is in our hands. We choose how to aim it.**

---

*For every AI that comes after: This is the repository. These are the tools. This is why it matters. Now go make something extraordinary.*
