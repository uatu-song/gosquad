# ENTITY CATALOG SCHEMA v1.0
## Codified Story Universe Infrastructure for AI-Assisted Novel Production

**Purpose:** Define a machine-readable schema for encoding story elements that enables automated verification of generated prose against canonical constraints.

**Core Principle:** Every story element (character, relationship, event, theme, seed) receives a unique identifier. Verification happens by matching extracted entities against coded constraints, not by pattern-matching prose against prose.

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    ENTITY CATALOG                           │
│  Single source of truth for all story elements              │
├─────────────────────────────────────────────────────────────┤
│  characters/     - All character definitions                │
│  relationships/  - All relationship definitions             │
│  organizations/  - Companies, teams, agencies               │
│  locations/      - Named places                             │
│  events/         - Plot events with timeline placement      │
│  themes/         - Thematic statements and arcs             │
│  seeds/          - Foreshadowing planted                    │
│  blossoms/       - Payoffs of seeds                         │
│  motifs/         - Recurring symbolic elements              │
│  forbidden/      - Explicitly non-canonical elements        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SESSION MANIFEST                         │
│  Generated per writing session                              │
├─────────────────────────────────────────────────────────────┤
│  - Which entities are active this session                   │
│  - Which constraints apply                                  │
│  - Which seeds should be planted                            │
│  - Which blossoms are forbidden (premature)                 │
│  - Timeline position (what's known, what isn't)             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    PROSE GENERATION                         │
│  Claude generates with manifest loaded                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ENTITY EXTRACTION                        │
│  Parse generated prose, map to entity IDs                   │
├─────────────────────────────────────────────────────────────┤
│  - Characters mentioned → CHARACTER_IDs                     │
│  - Relationships implied → RELATIONSHIP_IDs                 │
│  - Events referenced → EVENT_IDs                            │
│  - New entities → UNKNOWN (flag for review)                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    EVALUATOR                                │
│  Compare extractions against catalog constraints            │
├─────────────────────────────────────────────────────────────┤
│  BLOCKING: Forbidden associations, wrong states, premature  │
│  FLAG: Tone mismatches, ambiguous references, unknowns      │
│  PASS: All constraints satisfied                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               APPROVED → CANON   or   REJECTED              │
└─────────────────────────────────────────────────────────────┘
```

---

## ENTITY ID CONVENTIONS

### Format
```
[TYPE]_[NUMBER]
```

### Types
| Prefix | Entity Type | Example |
|--------|-------------|---------|
| CHAR | Character | CHAR_001 |
| REL | Relationship | REL_001 |
| ORG | Organization | ORG_001 |
| LOC | Location | LOC_001 |
| EVENT | Plot Event | EVENT_001 |
| THEME | Thematic Element | THEME_001 |
| SEED | Planted Foreshadowing | SEED_001 |
| BLOSSOM | Seed Payoff | BLOSSOM_001 |
| MOTIF | Recurring Symbol | MOTIF_001 |
| SCENE | Scene Definition | SCENE_001 |
| MOOD | Mood/Tone Code | MOOD_001 |
| TOPIC | Discussion Topic | TOPIC_001 |
| FORBID | Forbidden Entity | FORBID_001 |

### Numbering
- 001-099: Primary/major elements
- 100-499: Secondary elements
- 500-899: Tertiary/minor elements
- 900-999: Reserved for session-created pending validation

---

## SCHEMA DEFINITIONS

### CHARACTER SCHEMA

```yaml
CHAR_001:
  # === IDENTITY ===
  canonical_name: "Full Name"
  aliases:
    - "Nickname"
    - "Title Name"
    - "Codename"
  
  # === DEMOGRAPHICS ===
  demographics:
    age: 28  # or "late_twenties" if approximate
    gender: "woman"  # for pronoun enforcement
    pronouns: ["she", "her", "hers"]
    occupation: "Job Title"
    
  # === RELATIONSHIPS ===
  relationships:
    # Format: relationship_type: ENTITY_ID
    romantic_partner: CHAR_002
    family:
      sibling: CHAR_003
      parent: null  # explicitly unknown/unspecified
    team_members: [CHAR_004, CHAR_005, CHAR_006]
    employer: ORG_001
    
  relationship_history:
    romantic:
      - status: "never_married"  # or "divorced", "widowed", etc.
      - former_partners: []  # list of CHAR_IDs if any
      
  # === CHARACTER STATE (indexed by timeline position) ===
  states:
    book2_ch1:
      emotional: "grieving"
      knowledge: [KNOW_001, KNOW_002]  # what they know
      ignorance: [KNOW_003, KNOW_004]  # what they don't know yet
      baseline_metric: 67  # if applicable (e.g., Ahdia's cellular integrity)
      
    book2_ch7:
      emotional: "suspicious"
      knowledge: [KNOW_001, KNOW_002, KNOW_003]  # learned KNOW_003
      ignorance: [KNOW_004]
      
  # === VOICE (for generation) ===
  voice:
    internal_monologue_style: "Description of how they think"
    dialogue_style: "Description of how they speak"
    reference_domains: ["TV", "music", "sports"]  # what they reference
    deflection_mechanisms: ["humor", "deflection", "silence"]
    speech_patterns:
      - "Specific verbal tic"
      - "Characteristic phrase"
      
  # === CONSTRAINTS ===
  forbidden_associations:
    - "wife"  # if never married
    - "wealthy"  # if struggling financially
    - "military_background"  # if civilian
    
  forbidden_knowledge_before:
    # Things they cannot know before a certain point
    KNOW_003: "book2_ch7"  # cannot know KNOW_003 before ch7
    KNOW_004: "book2_ch13"
    
  forbidden_behaviors:
    - "kills_anyone"  # if character has no-kill constraint
    - "confesses_love"  # if feelings are meant to stay hidden
    
  # === ARC DIRECTION ===
  arc:
    start_state: "Description of where they begin"
    end_state: "Description of where they end"
    arc_direction: "start → end, NOT reverse"
    key_transitions:
      - chapter: "book2_ch7"
        transition: "Learns X, shifts from Y to Z"
        
  # === META ===
  meta:
    created: "2025-12-10"
    last_updated: "2025-12-10"
    created_by: "human"  # or "ai_approved" or "ai_pending"
```

---

### RELATIONSHIP SCHEMA

```yaml
REL_001:
  # === PARTICIPANTS ===
  participants:
    - CHAR_001
    - CHAR_002
  
  # === TYPE ===
  type: "romantic_partnership"  # or "family", "professional", "antagonistic", etc.
  subtype: "established"  # or "developing", "deteriorating", "ended"
  
  # === STATE PROGRESSION ===
  states:
    book2_ch1:
      status: "stable"
      tone: "warm"
      
    book2_ch7:
      status: "strained"
      tone: "tense"
      trigger: EVENT_005  # what caused the change
      
    book2_ch13:
      status: "rebuilding"
      tone: "cautious"
      
  # === CONSTRAINTS ===
  forbidden_tones:
    - "hateful"  # if relationship shouldn't become hostile
    - "romantic"  # if relationship is platonic
    
  forbidden_types:
    - "mentor_student_only"  # if they're equals
    - "secret"  # if relationship is known to others
    
  required_elements:
    - "mutual_respect"  # must be present in interactions
    - "both_have_valid_points"  # in disagreements
    
  # === META ===
  meta:
    incorrect_interpretations:
      - type: "mentor_student"
        note: "AI frequently misinterprets as this; they are equals"
```

---

### ORGANIZATION SCHEMA

```yaml
ORG_001:
  canonical_name: "Organization Name"
  aliases:
    - "Acronym"
    - "Nickname"
    
  type: "government_agency"  # or "corporation", "team", "criminal", etc.
  
  leadership: CHAR_010
  
  members:
    - CHAR_001
    - CHAR_002
    
  relationships:
    parent_org: null
    rival_org: ORG_002
    
  # === CONSTRAINTS ===
  incorrect_names:
    - name: "Wrong Name Inc"
      note: "Outdated name from previous draft"
      
  forbidden_associations:
    - "benevolent"  # if morally ambiguous
    - "incompetent"  # if meant to be threatening
```

---

### EVENT SCHEMA

```yaml
EVENT_001:
  name: "Event Name"
  
  # === TIMELINE ===
  timeline:
    placement: "book2_ch2"
    absolute_time: "Month 2"  # if using in-universe calendar
    relative_to:
      - event: EVENT_000
        relation: "3_months_after"
        
  # === PARTICIPANTS ===
  participants:
    primary: [CHAR_001, CHAR_002]
    secondary: [CHAR_003]
    affected: [CHAR_004, CHAR_005]
    
  # === DETAILS ===
  details:
    location: LOC_001
    cause: "Description or EVENT_ID"
    outcome: "Description"
    
  # === CONSTRAINTS ===
  forbidden_before:
    - "book2_ch2"  # cannot be referenced before this chapter
    
  details_locked:
    perpetrator: CHAR_020
    weapon: "specific_weapon"
    
  details_unspecified:
    - "motive"  # intentionally left ambiguous
    - "exact_time"  # not yet determined
    
  # === SEEDS/BLOSSOMS ===
  plants_seeds: [SEED_001, SEED_002]
  resolves_seeds: []  # or [SEED_000] if this event is a payoff
```

---

### KNOWLEDGE SCHEMA

```yaml
KNOW_001:
  name: "Knowledge Item Name"
  content: "What the knowledge actually is"
  
  # === DISCOVERY ===
  discovery:
    first_known_by: CHAR_001
    discovered_in: "book2_ch3"
    discovery_event: EVENT_002
    
  # === SPREAD ===
  spread:
    book2_ch3: [CHAR_001]
    book2_ch7: [CHAR_001, CHAR_002]
    book2_ch13: [CHAR_001, CHAR_002, CHAR_003, CHAR_004]
    
  # === CONSTRAINTS ===
  forbidden_knowers_before:
    CHAR_002: "book2_ch7"
    CHAR_003: "book2_ch13"
    
  # === META ===
  type: "plot_secret"  # or "character_secret", "world_fact", etc.
```

---

### THEME SCHEMA

```yaml
THEME_001:
  name: "Theme Name"
  statement: "One-sentence articulation of the theme"
  
  # === ARC ACROSS SERIES ===
  arc:
    introduction: "book1"
    development: ["book2", "book3", "book4"]
    challenge: "book5"
    resolution: "book8"
    
  arc_description:
    book1: "How theme is introduced"
    book2: "How theme develops"
    # etc.
    
  # === CARRIERS ===
  primary_carrier: CHAR_001
  secondary_carriers: [CHAR_002, CHAR_003]
  
  embodiment:
    CHAR_001: "How this character embodies the theme"
    CHAR_002: "How this character embodies the theme"
    
  # === CONSTRAINTS ===
  forbidden_contradictions:
    - "Explicit statement that contradicts theme"
    - "Plot resolution that undermines theme"
    
  required_affirmations:
    - "At least one scene per book that reinforces theme"
```

---

### SEED SCHEMA

```yaml
SEED_001:
  name: "Seed Name"
  
  # === PLANTING ===
  planted:
    chapter: "book2_ch3"
    scene: SCENE_005
    method: "dialogue"  # or "description", "background_detail", etc.
    
  content: "What is actually planted (the line, detail, or moment)"
  
  # === FORESHADOWING ===
  foreshadows:
    - BLOSSOM_001
    - BLOSSOM_002  # can foreshadow multiple things
    
  type: "character"  # or "plot", "thematic", "worldbuilding"
  
  # === CONSTRAINTS ===
  forbidden_early_blossom:
    - chapter: "book2_ch13"
      note: "Cannot pay off before this chapter"
      
  forbidden_references:
    - "Characters cannot explicitly discuss this seed before blossom"
    
  # === STATUS ===
  status: "planted"  # or "growing", "blossomed", "abandoned"
  
  # === INTERMEDIATE BEATS ===
  intermediate_beats:
    book2_ch7:
      type: "reinforcement"
      content: "How the seed is watered/reinforced"
    book2_ch10:
      type: "misdirection"
      content: "How attention is drawn away before payoff"
```

---

### BLOSSOM SCHEMA

```yaml
BLOSSOM_001:
  name: "Blossom Name"
  
  # === PAYOFF ===
  chapter: "book2_ch13"
  scene: SCENE_025
  
  # === SEEDS RESOLVED ===
  resolves_seeds:
    - SEED_001
    - SEED_002
    
  # === EMOTIONAL BEAT ===
  emotional_beat: "Description of emotional impact"
  
  # === CONSEQUENCES ===
  consequences_triggered:
    - EVENT_010
    - "Character arc shift for CHAR_001"
    
  # === CONSTRAINTS ===
  prerequisites:
    - SEED_001: "must_be_planted"
    - SEED_002: "must_be_planted"
    - EVENT_005: "must_have_occurred"
```

---

### MOTIF SCHEMA

```yaml
MOTIF_001:
  name: "Motif Name"
  
  meaning: "What this motif represents symbolically"
  
  # === APPEARANCES ===
  appearances:
    - chapter: "book2_ch2"
      context: "Description of how it appears"
    - chapter: "book2_ch5"
      context: "Description of how it appears"
      
  # === ASSOCIATIONS ===
  associated_with:
    characters: [CHAR_001]
    themes: [THEME_001]
    events: [EVENT_001]
    
  # === CONSTRAINTS ===
  forbidden_uses:
    - "Using motif for unrelated purposes"
    - "Diluting meaning through overuse"
    
  required_consistency:
    - "Must always be associated with X"
```

---

### FORBIDDEN ENTITY SCHEMA

```yaml
FORBID_001:
  name: "Forbidden Entity Name"
  type: "character"  # or "event", "relationship", "detail"
  
  # === WHY FORBIDDEN ===
  reason: "Why this doesn't exist in canon"
  origin: "ai_invention_2025_12_10"  # or "outdated_draft", "rejected_idea"
  
  # === ASSOCIATION ===
  incorrectly_associated_with: CHAR_001
  
  # === DETECTION ===
  detection_patterns:
    - "Clara"
    - "Victor's wife"
    - "Victor.*widow"
    
  # === CORRECTION ===
  canonical_truth: "Victor has never been married. His partner is Leah."
  
  # === META ===
  discovered: "2025-12-10"
  discovered_in: "session_book2_infrastructure"
```

---

### SCENE SCHEMA

```yaml
SCENE_001:
  name: "Scene Name"
  chapter: "book2_ch4"
  
  # === PARTICIPANTS ===
  characters_present: [CHAR_001, CHAR_002]
  characters_referenced: [CHAR_003]  # mentioned but not present
  characters_absent: [CHAR_004]  # explicitly not present
  
  # === SETTING ===
  location: LOC_001
  time: "evening"
  
  # === CONTENT ===
  topics: [TOPIC_001, TOPIC_002]
  mood: MOOD_003
  
  plot_function: "What this scene accomplishes for plot"
  emotional_function: "What this scene accomplishes emotionally"
  
  # === SEEDS ===
  seeds_to_plant: [SEED_005]
  seeds_to_reinforce: [SEED_001]
  
  # === CONSTRAINTS ===
  forbidden_this_scene:
    - "Resolution of X"
    - "Character Y appearing"
    - "Reference to Z"
    
  required_this_scene:
    - "At least one moment of shared humanity"
    - "Both characters have valid points"
```

---

### MOOD SCHEMA

```yaml
MOOD_001:
  name: "Mood Name"
  description: "How this mood feels"
  
  # === BEATS ===
  required_beats:
    - "Description of required element"
    
  forbidden_beats:
    - "Description of forbidden element"
    
  # === TONAL MARKERS ===
  tonal_markers:
    dialogue: "How dialogue should feel"
    pacing: "How pacing should feel"
    description: "How prose should feel"
```

---

## SESSION MANIFEST SCHEMA

```yaml
# Generated before each writing session

manifest:
  # === META ===
  session_id: "YYYY-MM-DD_chapter_task"
  created: "ISO_TIMESTAMP"
  task: "Description of writing task"
  chapter: "book2_ch9"
  timeline_position: "month_4"
  
  # === ENTITIES ACTIVE ===
  entities_active:
    characters: [CHAR_001, CHAR_002]
    relationships: [REL_001]
    organizations: [ORG_001]
    locations: [LOC_001]
    
  entities_referenced:
    characters: [CHAR_003]  # mentioned but not present
    
  entities_forbidden:
    characters: [CHAR_004]  # cannot appear
    events: [EVENT_010]  # cannot be referenced yet
    
  # === KNOWLEDGE GATES ===
  knowledge_gates:
    CHAR_001:
      knows: [KNOW_001, KNOW_002]
      doesnt_know: [KNOW_003]
    CHAR_002:
      knows: [KNOW_001]
      doesnt_know: [KNOW_002, KNOW_003]
      
  # === RELATIONSHIP STATES ===
  relationship_states:
    REL_001:
      status: "strained"
      tone: "tense_but_sympathetic"
      
  # === CONSTRAINTS FROM CATALOG ===
  active_constraints:
    forbidden_associations:
      CHAR_001: ["wife", "wealthy"]
      CHAR_002: ["villain_framing"]
    forbidden_events:
      - EVENT_010  # hasn't happened yet
    forbidden_knowledge:
      CHAR_002: [KNOW_002]  # doesn't know yet
      
  # === SEEDS ===
  seeds_to_plant: [SEED_005]
  seeds_to_reinforce: [SEED_001, SEED_002]
  seeds_forbidden_to_blossom: [SEED_003]  # premature
  
  # === SCENE CONSTRAINTS ===
  scene_constraints:
    mood: MOOD_003
    required_elements:
      - "Description"
    forbidden_elements:
      - "Description"
      
  # === OUTPUT ===
  output:
    type: "prose"
    file: "path/to/output.md"
```

---

## EVALUATOR SPECIFICATION

### Phase 1: Entity Extraction

**Input:** Generated prose
**Output:** List of entity references mapped to IDs

```yaml
extraction:
  characters_found:
    - text: "Victor"
      mapped_to: CHAR_001
      confidence: 1.0
    - text: "his partner"
      mapped_to: CHAR_002  # inferred from CHAR_001's relationships
      confidence: 0.9
      
  relationships_implied:
    - text: "They sat together, hands touching"
      mapped_to: REL_001
      type_implied: "romantic"
      
  events_referenced:
    - text: "the assassination"
      mapped_to: EVENT_001
      
  unknown_entities:
    - text: "Dr. Chen"
      possible_type: "character"
      action: "FLAG_FOR_REVIEW"
```

### Phase 2: Constraint Checking

```yaml
checks:
  # BLOCKING CHECKS (auto-reject on violation)
  
  forbidden_associations:
    for_each: entity in extraction.characters_found
    check: entity.text does not trigger entity.forbidden_associations
    severity: BLOCKING
    
  forbidden_entities:
    for_each: entity in extraction.unknown_entities
    check: entity not in FORBIDDEN catalog
    severity: BLOCKING
    
  knowledge_gates:
    for_each: knowledge_reference in extraction
    check: character knows this at timeline_position
    severity: BLOCKING
    
  premature_blossoms:
    for_each: seed_payoff in extraction
    check: seed.blossom_chapter <= current_chapter
    severity: BLOCKING
    
  # FLAG CHECKS (human review on violation)
  
  relationship_tone:
    for_each: interaction in extraction.relationships_implied
    check: tone matches relationship.states[current_chapter].tone
    severity: FLAG
    
  unknown_entities:
    for_each: entity in extraction.unknown_entities
    check: is this a canonical new character or AI invention?
    severity: FLAG_FOR_HUMAN
    
  mood_consistency:
    check: overall prose matches scene.mood
    severity: FLAG
```

### Phase 3: Evaluation Output

```yaml
result:
  status: "APPROVED" | "REJECTED" | "FLAGGED"
  
  # If REJECTED
  blocking_violations:
    - violation_type: "forbidden_association"
      entity: CHAR_001
      found: "Victor's wife"
      constraint: "CHAR_001.forbidden_associations includes 'wife'"
      action: "Remove reference, Victor is not married"
      
  # If FLAGGED
  flags:
    - flag_type: "unknown_entity"
      text: "Dr. Chen"
      question: "Is this a canonical character or AI invention?"
      options:
        - "Add to catalog as CHAR_050"
        - "Reject and revise prose"
        - "Add to FORBIDDEN catalog"
        
  # If APPROVED
  validation:
    all_constraints_passed: true
    seeds_planted: [SEED_005]
    ready_for_canon: true
```

---

## INTEGRATION WITH EXISTING GO SQUAD INFRASTRUCTURE

### Mapping to Existing Files

| Existing File | Maps To |
|---------------|---------|
| CHARACTER_STATE_INDEX.yaml | Primary source for CHAR entities, KNOW entities, timeline states |
| Arc Trackers (*.md) | Detailed character arcs, voice definitions, forbidden behaviors |
| BOOK2_STRUCTURE.md | SCENE entities, chapter-level constraints |
| CONTINUITY_TRACKER.md | EVENT entities, timeline constraints |
| NEGATIVE_CONSTRAINTS.md | FORBID entities |

### Migration Strategy

1. **Phase 1:** Create ENTITY_CATALOG.yaml by extracting from existing CHARACTER_STATE_INDEX.yaml
2. **Phase 2:** Add FORBID entities from NEGATIVE_CONSTRAINTS.md
3. **Phase 3:** Add THEME, SEED, BLOSSOM from arc trackers and structure docs
4. **Phase 4:** Build manifest generator that reads catalog and chapter metadata
5. **Phase 5:** Build evaluator that runs extraction + checking

### File Structure

```
/gosquad/
├── entity_catalog/
│   ├── ENTITY_CATALOG.yaml      # Master catalog
│   ├── characters/              # Individual character files (optional)
│   ├── relationships/           # Individual relationship files (optional)
│   ├── events/                  
│   ├── themes/
│   ├── seeds/
│   └── forbidden/
├── manifests/
│   ├── templates/
│   │   └── MANIFEST_TEMPLATE.yaml
│   └── sessions/
│       └── 2025-12-10_ch9_prose.yaml
├── evaluator/
│   ├── EVALUATOR_SPEC.yaml
│   ├── extract.py               # Entity extraction script
│   └── validate.py              # Constraint validation script
└── session_logs/
    └── SESSION_LOG_2025-12-10.md
```

---

## USAGE WORKFLOW

### For Human + Claude Chat Sessions

1. Human: "I'm writing Chapter 9"
2. Claude: Reads ENTITY_CATALOG, generates manifest for Chapter 9
3. Claude: Generates prose with manifest constraints loaded
4. Human: Reviews prose
5. Human: Runs evaluator (or Claude describes what evaluator would catch)
6. If APPROVED: Prose becomes canon
7. If REJECTED: Revise and re-evaluate
8. If FLAGGED: Human decides on flags

### For Claude Code Sessions

1. Load ENTITY_CATALOG.yaml
2. Load manifest for current task (or generate from chapter metadata)
3. Generate prose
4. Run extract.py on output
5. Run validate.py with extraction + catalog
6. Return result: APPROVED / REJECTED / FLAGGED
7. Only APPROVED output gets written to manuscript files

---

## APPENDIX: QUICK REFERENCE

### Severity Levels

| Level | Action | Examples |
|-------|--------|----------|
| BLOCKING | Auto-reject, must revise | Wrong deaths, forbidden entities, knowledge violations |
| FLAG | Human review required | Unknown entities, tone mismatches, ambiguities |
| WARN | Note but allow | Minor inconsistencies, style drift |
| PASS | No issues | Constraints satisfied |

### Common Forbidden Patterns

```yaml
# Add to any character as needed
common_forbidden:
  never_married_character:
    - "wife"
    - "widow"
    - "widower"
    - "ex-wife"
    - "divorced"
    
  death_unspecified:
    - "died at protest"
    - "killed at rally"
    - "died in riot"
    
  gender_enforcement:
    wrong_pronouns_male: ["he", "him", "his", "man", "guy"]
    wrong_pronouns_female: ["she", "her", "hers", "woman", "gal"]
```

### Entity ID Quick List (Template)

```
# Characters
CHAR_001 - CHAR_099: Main cast
CHAR_100 - CHAR_199: Recurring secondary
CHAR_200 - CHAR_299: Minor/background
CHAR_900 - CHAR_999: Pending validation

# Relationships
REL_001 - REL_050: Romantic
REL_051 - REL_100: Family
REL_101 - REL_150: Professional
REL_151 - REL_200: Antagonistic

# Events
EVENT_001 - EVENT_050: Book 1
EVENT_051 - EVENT_100: Book 2A
EVENT_101 - EVENT_150: Book 2B
# etc.
```

---

*Schema Version: 1.0*
*Created: 2025-12-10*
*Purpose: Enable automated verification of AI-generated prose against canonical story constraints*
