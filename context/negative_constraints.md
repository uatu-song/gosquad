# NEGATIVE_CONSTRAINTS.md
# Version: 1.0
# Purpose: Explicit statements of what is NOT TRUE
# Authority: BLOCKING - violations reject output

---

## Usage

Before any prose generation:
1. Load this document
2. Load constraints for characters appearing in scene
3. Evaluator checks output against all applicable constraints

**Severity Levels:**
- **BLOCKING:** Evaluator rejects output automatically
- **WARNING:** Evaluator flags for human review

---

## Global Constraints (Always Active)

### Company Names
| Status | Statement |
|--------|-----------|
| WRONG | "Titan Strategic" - OUTDATED, do not use |
| RIGHT | "TRIOMF" - Correct company name |

### Character Deaths - Timing
| Status | Statement |
|--------|-----------|
| WRONG | Firas is dead |
| RIGHT | Firas is displaced (returns Book 7) |
| WRONG | Leta dies before Chapter 21 |
| RIGHT | Leta dies IN Chapter 21, killed by Webb |
| WRONG | Isaiah dies during Book 2 |
| RIGHT | Isaiah was killed 6-8 months BEFORE Book 2 begins |

### Power Mechanics
| Status | Statement |
|--------|-----------|
| WRONG | Eidolon creates fear |
| RIGHT | Eidolon AMPLIFIES existing fear (cannot create new fear) |
| WRONG | Ahdia can translocate without cost |
| RIGHT | Translocation costs cellular baseline percentage |

---

## Character-Specific Constraints

---

### VICTOR HERNANDEZ

**Severity: BLOCKING**

#### Relationship Status
| Status | Statement |
|--------|-----------|
| WRONG | Victor is a widower |
| WRONG | Victor has/had a wife named Clara |
| WRONG | Victor's wife died |
| WRONG | Victor's wife died at a protest |
| WRONG | Victor has ever been married |
| RIGHT | Victor is in a relationship with Leah (partner, not wife) |
| RIGHT | Victor has never been married |

#### Backstory
| Status | Statement |
|--------|-----------|
| WRONG | Victor has a "dead wife" backstory |
| RIGHT | Victor's motivation is community organizing, environmental justice |
| RIGHT | Victor's grounding comes from community work, not personal tragedy |

**Source of Error:** Previous Claude sessions conflated Victor with Ben's backstory, inventing "Clara" as Victor's dead wife.

**Detection Patterns:**
- "Victor" + (wife | widow | Clara | married | bereaved)
- "his late wife" in Victor POV or Victor scenes
- Any funeral/death mourning in Victor's backstory

---

### BEN BUKOWSKI

**Severity: BLOCKING**

#### Wife's Death
| Status | Statement |
|--------|-----------|
| RIGHT | Ben's wife Sarah died |
| WRONG | Sarah died at a protest |
| WRONG | Sarah died at a riot |
| WRONG | Sarah died at a demonstration |
| WRONG | Sarah was killed by police |
| WRONG | Sarah was killed by Kain's people |
| RIGHT | Sarah's death cause is UNSPECIFIED (intentionally) |

**Why Unspecified:** Death cause is reserved for potential future reveal. Do not invent details.

**Detection Patterns:**
- "Sarah" + (protest | riot | demonstration | police | shot | killed by)
- Any specific cause of death for Sarah

---

### TESS WHITFORD

**Severity: BLOCKING**

#### Father Knowledge - CRITICAL
| Status | Statement |
|--------|-----------|
| WRONG | Tess "learns" or "discovers" father is corrupt during Book 2 |
| WRONG | Tess is "conflicted about" whether father is good |
| WRONG | Tess "believes father is a good man" at start of Book 2 |
| WRONG | Tess starts Book 2 in denial about father |
| RIGHT | Tess ALREADY KNOWS father is corrupt BEFORE Book 2 |
| RIGHT | This knowledge is WHY she became Gloom Girl |
| RIGHT | Her arc is USING this knowledge, not discovering it |

#### What Tess Discovers vs Already Knows
| Status | Statement |
|--------|-----------|
| RIGHT | She discovers the SCOPE of his corruption (specific cover-ups) |
| RIGHT | She discovers the TRIOMF connection |
| RIGHT | She discovers specific evidence she can use |
| WRONG | She discovers he is corrupt (she already knew this) |

**Source of Error:** Previous sessions misread her arc as "daughter learns father is bad" instead of "daughter who knows father is bad decides to act."

**Detection Patterns:**
- "Tess" + (realizes | discovers | learns | finds out) + "father" + (corrupt | bad | wrong)
- Tess having a "revelation" about father's character
- Tess defending father's character in internal monologue

---

### TESS + WEBB (Chapter 23)

**Severity: BLOCKING**

#### Violence Outcome
| Status | Statement |
|--------|-----------|
| WRONG | Tess kills Webb |
| WRONG | Webb dies |
| WRONG | Tess murders anyone in Book 2 |
| WRONG | Webb is found dead |
| RIGHT | Tess BRUTALIZES Webb (severely) |
| RIGHT | Webb SURVIVES |
| RIGHT | Webb is left alive (intentionally) |
| RIGHT | Tess acts masked and solo |
| RIGHT | Team does not know Tess attacked Webb |

**Detection Patterns:**
- "Tess" + (kills | murders | killed) + "Webb"
- "Webb" + (dead | died | body | corpse) after Chapter 23
- Any indication Webb does not survive

---

### HARRIET BOURN

**Severity: BLOCKING**

#### Gender
| Status | Statement |
|--------|-----------|
| WRONG | Bourn is a man |
| WRONG | "he/him/his" pronouns for Bourn |
| RIGHT | Bourn is a woman |
| RIGHT | "she/her/hers" pronouns for Bourn |

**Detection Patterns:**
- "Bourn" + (he | him | his | man | guy | gentleman)
- Male-coded descriptions of Bourn

---

### RYU MATSUDA

**Severity: BLOCKING**

#### Hidden Feelings
| Status | Statement |
|--------|-----------|
| WRONG | Ryu confesses love to Ahdia in Book 2 |
| WRONG | Ryu's feelings for Ahdia are revealed to her |
| WRONG | Ahdia knows Ryu loves her |
| RIGHT | Ryu loves Ahdia (hidden motivation for enabling) |
| RIGHT | This is NEVER explicitly revealed in Book 2 |
| RIGHT | Reader may infer from behavior, Ahdia does not know |

**Detection Patterns:**
- Ryu confessing or declaring feelings to Ahdia
- Ahdia acknowledging or responding to Ryu's romantic feelings
- Direct statement "Ryu loved her and she knew"

---

### VICTOR + LEAH Relationship

**Severity: WARNING** (less critical than death/gender errors)

#### Relationship Type
| Status | Statement |
|--------|-----------|
| WRONG | Victor and Leah are only mentor/student |
| WRONG | Victor and Leah are just friends |
| WRONG | Victor and Leah are married |
| RIGHT | Victor and Leah are romantic partners |
| RIGHT | Victor ALSO mentors Leah on solidarity (both/and teaching) |
| RIGHT | The relationship is BOTH romantic AND has mentor elements |

**Note:** The mentor dynamic exists within the romantic relationship. They are partners who also learn from each other.

---

## Timeline-Locked Constraints

**Severity: BLOCKING**

These events happen at SPECIFIC chapters. Do not move them earlier.

| Event | Chapter | Constraint |
|-------|---------|------------|
| Team learns about Exile Island | 13 | Cannot reference before ch13 |
| Ruth learns terminal trajectory | 7 | Cannot reference before ch7 |
| Ben's evidence released | 15 | Cannot reference before ch15 |
| Leta dies | 21 | Cannot reference before ch21 |
| Kain wins election | 24 | Cannot reference before ch24 |
| Clone immortality revealed | 14 | Team cannot know before ch14 |
| Gala infiltration | ~12 | Tess/Korede cannot reference before |

**Detection Method:** Check chapter number against event. If character references event before its chapter, REJECT.

---

## Knowledge State Constraints

**Severity: WARNING** (flag for review)

Characters cannot know things before they learn them. Check `knowledge_tracking` in CHARACTER_STATE_INDEX.yaml.

Common violations:
- Ruth referencing Ahdia's "terminal" state before ch7
- Team referencing "Exile Island" before ch13
- Anyone referencing clone immortality before ch14
- Korede knowing Go Squad identities before ch21

---

## Adding New Constraints

When a Claude session invents something incorrect:

1. **Add immediately** - Don't wait, add while context is fresh
2. **Use table format** - WRONG/RIGHT for scannability
3. **Include Source of Error** - Why did this happen?
4. **Add Detection Patterns** - How to catch this automatically
5. **Set Severity** - BLOCKING (auto-reject) or WARNING (flag)
6. **Update canon_warnings** in CHARACTER_STATE_INDEX.yaml if critical

### Template for New Constraint

```markdown
### [CHARACTER NAME]

**Severity: BLOCKING/WARNING**

#### [Category]
| Status | Statement |
|--------|-----------|
| WRONG | [incorrect thing] |
| RIGHT | [correct thing] |

**Source of Error:** [why this happened]

**Detection Patterns:**
- [regex or entity pattern]
```

---

## Constraint Review Log

| Date | Constraint Added | Source of Error | Added By |
|------|------------------|-----------------|----------|
| 2025-12-10 | Victor not widower | Clara invention | Human review |
| 2025-12-10 | Tess already knows | Arc misread | Human review |
| 2025-12-10 | Sarah death unspecified | Protest invention | Human review |
| 2025-12-10 | Bourn is woman | Pronoun errors | Human review |

---

*Last Updated: 2025-12-10*
*Version: 1.0*
*Update Trigger: Context engineering system implementation*
