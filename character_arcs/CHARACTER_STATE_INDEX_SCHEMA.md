# Character State Index Schema
**Purpose:** Hierarchical indexing system for queryable character state traversal without loading full arc tracker documents.

**Design Philosophy:** Broad → Narrow. Start with character, drill to arc thread, then chapter-specific state.

---

## Schema Structure (YAML)

```yaml
# CHARACTER_STATE_INDEX.yaml
# Machine-queryable index for Go Squad character states
# Companion to prose arc trackers in /character_arcs/

version: "1.0"
book: 2
last_updated: "2025-12-07"

# ============================================
# CHARACTER ENTRIES
# ============================================

characters:

  # ------------------------------------------
  # AHDIA BACCHUS (Protagonist)
  # ------------------------------------------
  ahdia:
    arc_tracker: "Ahdia_Arc_Tracker.md"
    codename: "Auerbach"
    book2_role: "protagonist_pov"

    # HIGH-LEVEL ARC
    arc_summary: "Sacrifice everything → Win through vulnerability"
    arc_type: "cbf_failing"  # CBT approach failing

    # CORE MOTIVES (stable across book)
    motives:
      - save_lives
      - prove_worth
      - protect_team
      - control_outcomes  # CBT thinking - will fail

    # EMOTIONAL ARC (progression)
    emotional_progression:
      - stage: "confident_operator"
        chapters: [1, 2, 3, 4, 5]
      - stage: "secret_keeper"
        chapters: [6, 7, 8, 9, 10]
      - stage: "exposed_desperate"
        chapters: [11, 12, 13, 14, 15]
      - stage: "sacrificial"
        chapters: [16, 17, 18, 19, 20]
      - stage: "hollow_victory"
        chapters: [21, 22, 23, 24]

    # THREAD TRACKING (queryable arcs)
    threads:

      baseline_decline:
        type: "resource_depletion"
        chapters: [1, 4, 8, 11, 15, 19, 23, 24]
        gates:
          ch1: { value: "90%→67-71%", event: "47_min_freeze" }
          ch4: { value: "→52%", event: "eastern_europe_ops" }
          ch11: { value: "→7%", event: "manhunt_defense" }
          ch24: { value: "7%→0.7%", event: "reactor_translocation" }

      exile_island_secret:
        type: "hidden_operation"
        chapters: [3, 5, 7, 9, 11, 13]
        reveal_chapter: 13
        gates:
          ch3: "begins_solo_ops"
          ch7: "28_targets_identified"
          ch13: "team_discovers"

      team_trust:
        type: "relationship_arc"
        chapters: [1, 7, 13, 17, 21]
        gates:
          ch1: "trusted_member"
          ch7: "lying_about_decline"
          ch13: "exile_secret_exposed"
          ch17: "rebuilding"
          ch21: "earned_back"

    # CHAPTER-BY-CHAPTER STATE SNAPSHOTS
    chapter_states:

      1:
        location: "caledonia_memorial_protest"
        emotional: "determined_operator"
        baseline: { start: "90%", end: "67-71%" }
        knows:
          - team_dynamics
          - power_costs
          - kain_threat
        learns:
          - eidolon_fear_amplification
          - cant_save_everyone
        doesnt_know:
          - geneva_is_bellatrix
          - prime_watching
        relationships:
          ruth: "close_friend"
          team: "trusted_member"
        key_actions:
          - burns_47_minutes_frozen
          - saves_23_loses_16
          - witnesses_korede_save

      # [Additional chapters to be filled as prose is written]

      24:
        location: "fusion_reactor_facility"
        emotional: "sacrificial_exhausted"
        baseline: { start: "7%", end: "0.7%" }
        knows:
          - full_triomf_scope
          - kain_clone_immortality
          - team_positions
        learns:
          - prime_exists
          - other_timelines
        relationships:
          ruth: "profound_bond"
          team: "willing_to_die_for"
        key_actions:
          - translocates_team_800_miles
          - freezes_reactor_meltdown
          - survives_barely

  # ------------------------------------------
  # TESS WHITFORD
  # ------------------------------------------
  tess:
    arc_tracker: "Tess_Arc_Tracker.md"
    codename: "Gloom Girl"
    book2_role: "investigation_lead_institutional"

    arc_summary: "Father's betrayal → Vigilante justice"
    arc_type: "institutional_betrayal"

    motives:
      - protect_family_image  # early
      - seek_truth  # middle
      - avenge_leta  # late
      - destroy_corrupt_systems  # end

    emotional_progression:
      - stage: "defensive_denial"
        chapters: [1, 2, 3, 4, 5]
      - stage: "reluctant_investigator"
        chapters: [6, 7, 8, 9]
      - stage: "truth_seeker"
        chapters: [10, 11, 12, 13, 14]
      - stage: "grieving_vigilante"
        chapters: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    threads:

      father_complicity:
        type: "betrayal_discovery"
        chapters: [3, 5, 8, 12, 15, 19]
        related_characters: [chief_whitford, ben, isaiah_bennett]
        gates:
          ch3: "first_suspicion"
          ch5: "finds_evidence"
          ch8: "confirms_complicity"
          ch12: "confronts_father"
          ch15: "full_scope_revealed"
          ch19: "cuts_ties"

      leta_relationship:
        type: "romantic_arc"
        chapters: [1, 6, 11, 17, 21]
        terminus: "death_ch21"
        gates:
          ch1: "established_partners"
          ch6: "harassment_strain"
          ch11: "protective"
          ch17: "fear_for_safety"
          ch21: "witnesses_death"

      webb_vengeance:
        type: "vigilante_arc"
        chapters: [21, 22, 23]
        constraints:
          - "does_NOT_kill"
          - "brutalizes_but_leaves_alive"
          - "masked_solo_action"
          - "team_doesnt_know"
        gates:
          ch21: "leta_killed_by_webb"
          ch22: "tracks_webb"
          ch23: "brutalizes_masked"

    chapter_states:

      1:
        location: "memorial_protest"
        emotional: "defensive_about_institutions"
        knows:
          - father_is_chief
          - isaiah_killed_by_police
        doesnt_know:
          - father_signed_cover_up
          - webb_specific_role
        relationships:
          leta: "partners"
          father: "complicated_loyalty"

      21:
        location: "street_confrontation"
        emotional: "shattered_rage"
        knows:
          - father_full_complicity
          - webb_killed_isaiah
          - triomf_connection
        learns:
          - webb_killed_leta
        relationships:
          leta: "dead"
          father: "severed"
          korede: "witnessed_identity_reveal"
        key_actions:
          - reveals_gosquad_identity_to_korede
          - vows_vengeance

  # ------------------------------------------
  # BEN BUKOWSKI
  # ------------------------------------------
  ben:
    arc_tracker: "Ben_Arc_Tracker.md"
    codename: "Night Knight"
    book2_role: "investigation_lead_evidence"

    arc_summary: "Perfect evidence → System failure → Faith shattered"
    arc_type: "institutional_faith_collapse"

    motives:
      - build_airtight_case
      - trust_the_system
      - protect_through_order

    emotional_progression:
      - stage: "methodical_investigator"
        chapters: [1, 2, 3, 4, 5, 6, 7]
      - stage: "hopeful_prosecutor"
        chapters: [8, 9, 10]
      - stage: "disillusioned"
        chapters: [11, 12, 13, 14, 15]
      - stage: "faith_shattered"
        chapters: [16, 17, 18, 19, 20, 21, 22, 23, 24]

    threads:

      tank_kain_investigation:
        type: "evidence_building"
        chapters: [2, 4, 6, 8, 10]
        gates:
          ch2: "begins_investigation"
          ch4: "massacre_evidence"
          ch6: "triomf_connection"
          ch8: "case_complete"
          ch10: "leaks_publicly"

      system_faith:
        type: "belief_collapse"
        chapters: [8, 10, 12, 14, 16]
        key_moment: "ch12_evidence_ignored"
        gates:
          ch8: "confident_system_works"
          ch10: "48_hours_of_hope"
          ch12: "eidolon_reframes"
          ch14: "officers_cleared"
          ch16: "what_am_i_conserving"

    chapter_states:

      8:
        emotional: "triumphant_confident"
        knows:
          - full_tank_kain_evidence
          - riot_funding_trail
          - triomf_coordination
        believes: "system_will_work"

      16:
        emotional: "shattered_questioning"
        knows:
          - evidence_perfect_and_irrelevant
          - system_protects_power
        key_line: "What the hell am I conserving?"

  # ------------------------------------------
  # LEAH TURNER
  # ------------------------------------------
  leah:
    arc_tracker: "Leah_Arc_Tracker.md"
    codename: "Battlea"
    book2_role: "investigation_abuse_pattern"

    arc_summary: "Silent complicity → Public action → Solidarity too late"
    arc_type: "white_moderate_awakening"

    motives:
      - avoid_conflict  # early
      - process_own_trauma  # middle
      - speak_for_silenced  # late

    threads:

      kain_harassment_investigation:
        type: "evidence_building"
        chapters: [3, 6, 9, 12, 15, 18]
        personal_stake: "harassed_at_red_dress_heist_book1"
        gates:
          ch3: "begins_quietly"
          ch6: "finds_nda_pattern"
          ch9: "15-20_victims"
          ch12: "recording_obtained"
          ch15: "decides_to_release"
          ch18: "releases_recording"

      solidarity_learning:
        type: "political_awakening"
        chapters: [1, 7, 14, 21, 24]
        gates:
          ch1: "uncomfortable_at_protest"
          ch7: "victor_teaches"
          ch14: "starting_to_get_it"
          ch21: "leta_death_impact"
          ch24: "solidarity_learned_too_late"

  # ------------------------------------------
  # RUTH CARTER
  # ------------------------------------------
  ruth:
    arc_tracker: "Ruth_Arc_Tracker.md"
    codename: "Nightingale"
    book2_role: "team_leader"

    arc_summary: "Leadership burden → Can't save everyone → Acceptance"
    arc_type: "caretaker_limits"

    threads:

      ahdia_treatment:
        type: "medical_caretaker"
        chapters: [1, 4, 7, 11, 15, 19, 24]
        gates:
          ch1: "routine_treatment"
          ch7: "discovers_decline_severity"
          ch11: "emergency_stabilization"
          ch24: "critical_intervention"

      leadership_burden:
        type: "responsibility_weight"
        chapters: [1, 5, 10, 15, 21]
        gates:
          ch1: "confident_leader"
          ch5: "weight_accumulating"
          ch10: "hope_then_crash"
          ch15: "cant_save_everyone"
          ch21: "leta_loss"

  # ------------------------------------------
  # ADDITIONAL CHARACTERS (condensed)
  # ------------------------------------------

  victor:
    arc_tracker: "Victor_Arc_Tracker.md"
    codename: "Crimson Sable"
    book2_role: "connector_mentor"
    key_function: "teaches_both_and_thinking"
    network_save: "month_11_safe_houses"

  leta:
    arc_tracker: "Leta_Arc_Tracker.md"
    book2_role: "harassment_victim_activist"
    death_chapter: 21
    killed_by: "officer_webb"
    key_contribution: "fear_resistance_practice"

  korede:
    arc_tracker: "Korede_Arc_Tracker.md"
    book2_role: "observer_radicalized"
    key_chapters: [1, 21]
    radicalization_event: "witnesses_sister_death_ch21"
    learns_gosquad_identity: "ch21"

  ryu:
    arc_tracker: "Ryu_Arc_Tracker.md"
    book2_role: "enabler"
    arc_summary: "Doctor → Enabler → Complicit"
    threads:
      enablement:
        type: "ethical_erosion"
        chapters: [2, 5, 8, 12, 16]
        gates:
          ch2: "first_intel_handoff"
          ch5: "falsifies_records"
          ch8: "provides_coordinates"
          ch12: "deep_complicity"
    secret: "loves_ahdia_never_confesses"

# ============================================
# CROSS-CHARACTER QUERIES
# ============================================

knowledge_tracking:

  exile_island:
    secret_holder: "ahdia"
    reveal_chapter: 13
    who_knows_when:
      ch1-12: [ahdia]
      ch13+: [ahdia, ruth, ben, tess, victor, leah]

  ahdia_terminal_decline:
    secret_holders: [ahdia, ryu]
    reveal_chapter: 7
    who_knows_when:
      ch1-6: [ahdia, ryu]
      ch7+: [ahdia, ryu, ruth]

  tess_webb_attack:
    secret_holder: "tess"
    reveal_chapter: null  # never revealed in book 2
    who_knows_when:
      ch23+: [tess]  # only tess knows

  gosquad_identity:
    korede_learns: "ch21"
    context: "tess_reveals_during_leta_death"

# ============================================
# RELATIONSHIP MATRIX (Chapter Snapshots)
# ============================================

relationships:

  ahdia_ruth:
    type: "best_friends"
    progression:
      ch1: "close_trusted"
      ch7: "strained_by_lies"
      ch13: "rebuilding"
      ch24: "profound_bond"

  tess_leta:
    type: "romantic_partners"
    progression:
      ch1: "established_loving"
      ch11: "protective_fearful"
      ch21: "severed_by_death"

  tess_father:
    type: "family_betrayal"
    progression:
      ch1: "complicated_loyalty"
      ch8: "suspicious"
      ch12: "confrontational"
      ch19: "severed"

# ============================================
# METADATA
# ============================================

canon_warnings:
  - id: "tess_kill"
    warning: "Tess does NOT kill anyone. She brutalizes Webb but leaves him alive."
  - id: "isaiah_killer"
    warning: "Isaiah killed by Officer Webb PRE-Book 2, not by Tess."
  - id: "company_name"
    warning: "Company is TRIOMF, not 'Titan Strategic' (outdated)."

tag_definitions:
  cbf_failing: "CBT approach failing - trying to control outcomes makes things worse"
  both_and: "Victor's teaching - holding contradictory truths simultaneously"
  institutional_betrayal: "Discovery that trusted institutions protect power"
  white_moderate: "MLK concept - learning solidarity through crisis"
```

---

## Usage Examples

### Query: "What does Tess know about her father in Chapter 8?"

```
Path: characters.tess.threads.father_complicity.gates.ch8
Result: "confirms_complicity"

Path: characters.tess.chapter_states.8
Result: (not yet populated - needs prose generation)
```

### Query: "Who knows about Exile Island by Chapter 10?"

```
Path: knowledge_tracking.exile_island.who_knows_when.ch1-12
Result: [ahdia]
```

### Query: "Ahdia's baseline at each crisis point?"

```
Path: characters.ahdia.threads.baseline_decline.gates
Result:
  ch1: 90%→67-71% (47_min_freeze)
  ch4: →52% (eastern_europe_ops)
  ch11: →7% (manhunt_defense)
  ch24: 7%→0.7% (reactor_translocation)
```

---

## Integration with Workflow

**Before writing scene:**
1. Query index for participant states at chapter
2. Load any sparse chapter_states entries that need detail
3. Reference thread gates for what's known/unknown

**After writing scene:**
1. Update chapter_states with specific details from prose
2. Add any new knowledge gates discovered
3. Update relationship progressions if shifted

**The index is the map. The arc trackers are the territory.**
