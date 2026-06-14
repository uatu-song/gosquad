# Character Profiles - Directory Guide

**Purpose:** Explain the file hierarchy and when to use each type.

---

## File Naming Convention

| Pattern | Purpose | Editable? |
|---------|---------|-----------|
| `Character_Name.md` | Current working profile (Book 2+) | Yes |
| `Character_Name_Book1_Final.md` | Locked Book 1 snapshot | **NO** |
| `Character_Name_EXTENDED.md` | Detailed planning docs (richer content) | Reference/merge |
| `Character_Name_CORRECTED.md` | Canon fix for AI hallucinations | Reference only |

---

## Which File to Load?

### For Book 2 Drafting:

1. **Primary:** `Character_Name.md` (current state)
2. **Voice/Psychology:** `Character_Name_EXTENDED.md` (dialogue patterns, psychological profile)
3. **Reference:** `Character_Name_Book1_Final.md` (backstory consistency)
4. **Arc:** `../character_arcs/Character_Name_Arc_Tracker.md` (progression)

**Important:** The `*_EXTENDED.md` files contain rich content not in base files:
- Psychological profiles and internal conflicts
- Dialogue patterns and voice characteristics
- Character strengths/weaknesses
- Quote collections and example dialogue
- Thematic significance

For POV work, always load BOTH the base `.md` AND the `_EXTENDED.md`.

### For Continuity Checking:

1. Load `../character_arcs/CHARACTER_STATE_INDEX.yaml`
2. Check knowledge gates for current chapter
3. Cross-reference profiles as needed

---

## File Categories

### Protagonist
- `Ahdia_Bacchus.md` / `Ahdia_Bacchus_Book1_Final.md`
- Voice file: `../Ahdia_voice_sample.md`

### Go Squad Core
- `Ruth_Carter.md` / `Ruth_Carter_Book1_Final.md`
- `Firas_Bacchus.md` / `Firas_Bacchus_Book1_Final.md`
- `Ryu_Matsuda.md` (Handler)

### Supporting Cast
- `Rahs_Jericho.md`
- `Isaiah_Bennett.md` (deceased, but referenced)

### Antagonists
- `Harding_Kain.md` / `Harding_Kain_Book1_Final.md`
- `Bellatrix_Naima.md`
- `Eidolon.md`

### Organizations & Groups
- `Go_Squad.md` / `The_Go_Squad_Book1_Final.md`
- `The_Conclave.md`
- `The_Helminth.md`
- `The_Intermediary.md`

### Mechanics
- `Consciousness_Copy_Mechanics.md` (AR-Ryu system)

---

## Archived Files

Extension-less files (legacy format) have been moved to:
`../_archive/legacy_profiles/`

These are superseded by the `.md` versions.

---

## Adding New Characters

1. Create `Character_Name.md` with standard template
2. Add entry to `../character_arcs/CHARACTER_STATE_INDEX.yaml`
3. Create `../character_arcs/Character_Name_Arc_Tracker.md` if significant
4. Document in this README

---

## Profile Template

```markdown
# [Character Name]

## Basic Information
- **Full Name:**
- **Role:**
- **First Appearance:**

## Background
[Relevant history]

## Personality
[Key traits, patterns]

## Voice Patterns
[How they speak, verbal tics]

## Relationships
[Key connections to other characters]

## Arc Summary
[Where they start, where they're going]

## Constraints
[Things this character would NEVER do/say]
```

---

*Last Updated: December 2025*
