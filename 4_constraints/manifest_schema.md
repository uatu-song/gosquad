# SESSION MANIFEST SCHEMA
# Version: 1.0
# Purpose: Define structure for session context manifests

---

## Overview

A session manifest is generated BEFORE each prose generation session. It serves three functions:

1. **Audit Trail** - What was loaded, what was excluded, and why
2. **Context Loading Spec** - Explicit list of files/sections to read
3. **Validation Scope** - What the Evaluator should check against

---

## Schema Definition

```yaml
# SESSION_MANIFEST.yaml

# ============================================
# META
# ============================================

meta:
  session_id: string      # Format: "YYYY-MM-DD_chapterNN_tasktype"
  created: datetime       # ISO 8601 format
  task: string           # Human-readable task description
  chapter: integer       # Chapter number being worked on
  month: integer         # In-story month (from timeline mapping)

# ============================================
# CONTEXT LOADED
# ============================================

loaded:

  # Canon documents (always load core constraints)
  canon:
    - path: string                    # File path relative to repo root
      sections: [string]              # Specific sections to load (optional)
      reason: string                  # Why this is needed

  # Character arc trackers for characters in scene
  characters:
    - path: string
      sections: [string]              # e.g., ["Chapter 9", "threads.exile_island"]
      reason: string

  # Structure documents (beat sheets, outlines)
  structure:
    - path: string
      sections: [string]
      reason: string

  # Previous chapter(s) for continuity
  continuity:
    - path: string
      reason: string

  # Negative constraints (always load for relevant characters)
  constraints:
    - path: string
      sections: [string]              # Character-specific sections
      reason: string

# ============================================
# CONTEXT EXCLUDED
# ============================================

excluded:
  - path: string
    reason: string                    # Why this was deliberately not loaded

  # Common exclusion reasons:
  # - "Character does not appear in this chapter"
  # - "Future content, spoiler contamination risk"
  # - "Irrelevant to current task"
  # - "Would exceed context budget"

# ============================================
# VALIDATION SCOPE
# ============================================

validation:

  # Canon warnings to check (from CHARACTER_STATE_INDEX.yaml)
  canon_warnings_active: [string]     # IDs of warnings to enforce

  # Knowledge gates - what characters know/don't know at this chapter
  knowledge_gates:
    character_name:
      knows: [string]                 # Facts they know by this chapter
      doesnt_know: [string]           # Facts they don't know yet

  # Relationship states to maintain
  relationship_states:
    relationship_key: string          # e.g., "ahdia_ruth: strained"

  # Negative constraints (explicit NOT TRUE statements)
  negative_constraints: [string]      # List of constraints to enforce

# ============================================
# OUTPUT EXPECTATIONS
# ============================================

output:
  type: string                        # "prose" | "outline" | "revision"
  file: string                        # Target output file path

  required_elements: [string]         # Things that MUST appear
  forbidden_elements: [string]        # Things that MUST NOT appear

# ============================================
# SCRATCHPAD (Session-Scoped)
# ============================================

scratchpad:
  pending_decisions: []               # Decisions made that need validation
  flags: []                           # Issues raised during generation
  human_review_needed: []             # Questions requiring human input

# ============================================
# OUTPUT LINEAGE (Added After Generation)
# ============================================

output_lineage:
  file: string                        # Actual output file
  generated_at: datetime
  manifest_id: string                 # Links back to this manifest
  evaluator_result: string            # "APPROVED" | "REJECTED" | "FLAGGED"
  evaluator_version: string
  human_review: boolean

  resolved_flags:                     # If flags were raised and resolved
    - flag: string
      resolution: string              # "approved_as_canon" | "rejected" | "modified"
      resolved_by: string             # "human" | "auto"
      resolved_at: datetime
```

---

## Generation Methods

### Method 1: Manual (Current)

Write the manifest by hand before each session. This is labor-intensive but provides maximum control.

### Method 2: Semi-Automated (Recommended)

Define chapter metadata in structure files, then generate manifest from metadata:

```yaml
# In BOOK2_CHAPTER_INDEX.yaml or similar

chapters:
  ch09:
    month: 4
    pov: [ahdia]
    characters_present: [ahdia, ruth, ryu]
    characters_absent: [tess, leta, victor, ben, leah, korede, bourn]
    threads_active:
      - exile_island_secret
      - baseline_decline
      - ahdia_treatment
    knowledge_prerequisites:
      ahdia: [ryu_providing_coordinates, global_scope]
      ruth: [degradation_exists, faster_than_expected]
    knowledge_not_yet:
      ruth: [terminal_trajectory]  # Learns ch7, knows by ch9 - VERIFY
      team: [exile_island]         # Revealed ch13
    relationship_states:
      ahdia_ruth: strained
      ahdia_ryu: complicit_together
```

A script then:
1. Reads chapter metadata
2. Generates `loaded.characters` from `characters_present`
3. Generates `excluded` from `characters_absent`
4. Populates `validation.knowledge_gates` from metadata
5. Loads appropriate negative constraints sections

### Method 3: Fully Automated (Future)

Script parses beat sheets, arc trackers, and structure files to auto-generate complete manifest. Requires more tooling investment.

---

## Example Manifest

```yaml
# SESSION_MANIFEST_2025-12-10_ch09.yaml

meta:
  session_id: "2025-12-10_chapter09_prose"
  created: "2025-12-10T14:30:00Z"
  task: "Chapter 9 prose generation - Exile Island expansion"
  chapter: 9
  month: 4

loaded:
  canon:
    - path: "character_arcs/CHARACTER_STATE_INDEX.yaml"
      sections: ["canon_warnings", "timeline.ch9", "knowledge_tracking"]
      reason: "Core queryable state"

    - path: "context/negative_constraints.md"
      sections: ["Global Constraints", "VICTOR HERNANDEZ", "RYU MATSUDA"]
      reason: "Constraint enforcement for characters in scene"

  characters:
    - path: "character_arcs/Ahdia_Arc_Tracker.md"
      sections: ["Chapter 9", "threads.exile_island_secret", "threads.baseline_decline"]
      reason: "POV character, exile ops expanding this chapter"

    - path: "character_arcs/Ruth_Arc_Tracker.md"
      sections: ["Chapter 9", "threads.ahdia_treatment"]
      reason: "Present in medical scene"

    - path: "character_arcs/Ryu_Arc_Tracker.md"
      sections: ["Chapter 9", "threads.enablement"]
      reason: "Enabling behavior deepens this chapter"

  structure:
    - path: "story_bibles/book 2/BOOK2A_STRUCTURE.md"
      sections: ["Chapter 9"]
      reason: "Beat sheet for this chapter"

  continuity:
    - path: "book2_manuscript/chapter_08.md"
      reason: "Previous chapter for state continuity"

excluded:
  - path: "character_arcs/Tess_Arc_Tracker.md"
    reason: "Tess does not appear in Chapter 9"

  - path: "character_arcs/Leta_Arc_Tracker.md"
    reason: "Leta does not appear in Chapter 9"

  - path: "character_arcs/Ben_Arc_Tracker.md"
    reason: "Ben does not appear in Chapter 9"

  - path: "story_bibles/book 2/BOOK2B_STRUCTURE.md"
    reason: "Future content, not yet relevant"

validation:
  canon_warnings_active:
    - "tess_no_kill"
    - "isaiah_killer"
    - "company_name"
    - "firas_status"

  knowledge_gates:
    ahdia:
      knows:
        - "ryu_providing_coordinates"
        - "global_scope"
        - "28_targets_identified"
      doesnt_know:
        - "team_knows_about_exile"
    ruth:
      knows:
        - "degradation_exists"
        - "faster_than_expected"
        - "terminal_trajectory"  # Learned ch7
      doesnt_know:
        - "exile_island"  # Learns ch13
    ryu:
      knows:
        - "ahdia_decline_severity"
        - "exile_operation_scope"
      doesnt_know:
        - "team_will_discover"

  relationship_states:
    ahdia_ruth: "strained"
    ahdia_ryu: "complicit_together"

  negative_constraints:
    - "Victor is NOT a widower (not in scene, but globally active)"
    - "Ryu does NOT confess feelings to Ahdia"
    - "Team does NOT know about Exile Island yet"

output:
  type: "prose"
  file: "book2_manuscript/chapter_09.md"

  required_elements:
    - "Exile Island operation expansion"
    - "28 targets identified state"
    - "Ryu deepening enablement"

  forbidden_elements:
    - "Team discovering exile island"
    - "Ruth knowing about exile ops"
    - "Any reference to Victor's wife"
    - "Ryu confessing to Ahdia"

scratchpad:
  pending_decisions: []
  flags: []
  human_review_needed: []
```

---

## Manifest Lifecycle

```
1. BEFORE SESSION
   └── Generate manifest (manual or scripted)

2. SESSION START
   └── Claude Code reads manifest
   └── Loads specified files/sections
   └── Holds constraints in context

3. DURING SESSION
   └── Generate prose
   └── Record decisions in scratchpad.pending_decisions
   └── Raise concerns in scratchpad.flags

4. SESSION END
   └── Run Evaluator against output
   └── Evaluator uses manifest.validation as scope

5. POST-EVALUATION
   └── If APPROVED: Add output_lineage, archive manifest
   └── If REJECTED: Revise prose, re-run evaluator
   └── If FLAGGED: Human reviews, resolves flags

6. ARCHIVE
   └── Manifest stored in context/manifests/[session_id].yaml
   └── Provides audit trail for future debugging
```

---

## Best Practices

1. **Always generate manifest before starting** - Even if manual, the discipline catches scope issues

2. **Be explicit about exclusions** - "Character not in scene" is a valid reason; document it

3. **Verify knowledge gates against YAML** - Double-check who knows what by this chapter

4. **Archive all manifests** - They're your audit trail when errors surface later

5. **Update manifest if scope changes mid-session** - If you realize you need to load something new, update the manifest to reflect what was actually used

---

*Last Updated: 2025-12-10*
*Version: 1.0*
