#!/usr/bin/env python3
"""
Complete Story Generation System Demo
Shows all features: campaign generation, scene creation, mechanics integration
"""

import os
import sys

# Ensure correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from core.story_generator import StoryGenerator
from core.dm_master import DMSession


def print_divider(title=""):
    if title:
        print(f"\n{'='*70}")
        print(f"  {title.center(66)}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'='*70}\n")


def main():
    print_divider("GO SQUAD BOOK 3 - COMPLETE STORY SYSTEM DEMO")

    # Initialize
    print("Initializing story generator and game mechanics...")
    story_gen = StoryGenerator()
    dm = DMSession()
    print("✓ Systems initialized\n")

    # DEMO 1: Campaign Generation
    print_divider("DEMO 1: CAMPAIGN OUTLINE GENERATION")

    print("Generating campaign: Temporal Instability theme, Ahdia focus")
    outline = story_gen.generate_campaign_outline(
        focus_character='ahdia_bacchus',
        theme='temporal_instability',
        duration_months=3
    )

    print(f"\nTitle: {outline.title}")
    print(f"\nPremise:\n{outline.premise}")
    print(f"\nThemes: {', '.join(outline.themes)}")
    print(f"Session Count: {outline.session_count}")
    print(f"Key NPCs: {', '.join(outline.key_npcs)}")

    print("\nThree-Act Structure:")
    for i, act in enumerate(outline.acts, 1):
        print(f"\n  Act {i}: {act['name']}")
        print(f"  {act['description']}")
        print(f"  Themes: {', '.join(act['themes'])}")

    print("\nMajor Campaign Events:")
    for event in outline.major_events:
        print(f"  - {event}")

    # DEMO 2: Scene Generation
    print_divider("DEMO 2: SCENE GENERATION")

    print("Generating investigation scene with Ahdia and Ruth...")
    scene = story_gen.generate_scene(
        scene_type='investigation',
        characters=['ahdia_bacchus', 'ruth_carter'],
        context={'tension': 'high'}
    )

    print(f"\nTitle: {scene.title}")
    print(f"Setting: {scene.setting}")
    print(f"Characters: {', '.join(scene.characters)}")
    print(f"\nHook: {scene.hook}")

    print(f"\nComplications:")
    for comp in scene.complications:
        print(f"  - {comp}")

    print(f"\nNarrative Beats:")
    for i, beat in enumerate(scene.narrative_beats, 1):
        print(f"  {i}. {beat}")

    print(f"\nSuggested Checks:")
    for check in scene.suggested_checks:
        print(f"  - {check['character']}: {check['skill']} (DC: {check['difficulty']})")

    print(f"\nDM Notes:\n  {scene.dm_notes}")

    # DEMO 3: Mechanics Integration
    print_divider("DEMO 3: RUNNING SCENE WITH MECHANICS")

    print("Executing the suggested skill checks...")

    for check in scene.suggested_checks:
        print(f"\n--- {check['character']} makes {check['skill']} check ({check['difficulty']}) ---")
        try:
            result = dm.make_skill_check(
                check['character'],
                check['skill'],
                check['difficulty'],
                check.get('modifiers', {})
            )
            print(f"{result['formatted']}")
            print(f"Quality: {result['interpretation'].replace('_', ' ').title()}")

            # Narrate based on outcome
            if result['result'].success:
                print("✓ Success! The investigation yields valuable information.")
            else:
                print("✗ Failure. Complications arise...")

        except Exception as e:
            print(f"Error: {e}")

    # DEMO 4: Temporal Powers Scene
    print_divider("DEMO 4: TEMPORAL POWERS SCENE")

    print("Generating scene that requires Ahdia's temporal powers...")
    temporal_scene = story_gen.generate_scene(
        scene_type='temporal',
        characters=['ahdia_bacchus'],
        context={}
    )

    print(f"\nTitle: {temporal_scene.title}")
    print(f"Hook: {temporal_scene.hook}")

    print(f"\nAhdia's current state:")
    ahdia = dm.get_character_systems('ahdia_bacchus')
    status = ahdia['temporal'].get_current_status()
    print(f"  TC (Temporal Charge): {status['resources']['tc']}/100")
    print(f"  TS (Temporal Strain): {status['resources']['ts']}/100")
    print(f"  TIP (Temporal Instability): {status['resources']['tip']}/100")

    print("\nAhdia uses 'temporal_perception' power...")
    power_result = ahdia['temporal'].use_power('temporal_perception', context="Critical investigation moment")

    if power_result.success:
        print(f"✓ Power activated: {power_result.power_name}")
        print(f"  Cost: -{power_result.tc_cost} TC, +{power_result.ts_cost} TS")
        print(f"  New TC: {power_result.new_resources.tc}/100")
        print(f"  New TS: {power_result.new_resources.ts}/100")

        strain_status = power_result.strain_status
        if isinstance(strain_status, dict):
            print(f"  Status: {strain_status.get('status', 'normal')}")
        else:
            print(f"  Status: {strain_status}")

        print("\nNarrative: Ahdia's perception shifts. Time seems to slow slightly,")
        print("           revealing details that would otherwise be invisible.")
    else:
        print("✗ Cannot use power (insufficient resources)")

    # DEMO 5: Full Session Plan
    print_divider("DEMO 5: COMPLETE SESSION PLAN")

    print("Generating Session 1 from campaign outline...")
    session = story_gen.generate_session_plan(
        session_number=1,
        outline=outline,
        previous_outcomes=[]
    )

    print(f"\nSession {session['session_number']}: {session['act']}")
    print(f"\n{session['act_description']}")

    print(f"\nSession Goals:")
    for goal in session['session_goals']:
        print(f"  - {goal}")

    print(f"\nPlanned Scenes ({len(session['scenes'])}):")
    for i, sc in enumerate(session['scenes'], 1):
        print(f"\n  Scene {i}: {sc.title}")
        print(f"    Setting: {sc.setting}")
        print(f"    Characters: {', '.join(sc.characters)}")
        print(f"    Hook: {sc.hook}")
        print(f"    Checks: {len(sc.suggested_checks)}")

    print(f"\nDM Prep Notes:")
    print(f"  {session['dm_prep_notes']}")

    # DEMO 6: Different Campaign Themes
    print_divider("DEMO 6: ALTERNATIVE CAMPAIGN THEMES")

    themes = ['resistance_against_kain', 'institutional_collapse', 'trust_and_betrayal']
    for theme in themes:
        outline = story_gen.generate_campaign_outline(
            focus_character='ben_bukowski',
            theme=theme,
            duration_months=2
        )
        print(f"\nTheme: {theme}")
        print(f"Title: {outline.title}")
        print(f"Premise: {outline.premise[:150]}...")

    # DEMO 7: Combat Scene
    print_divider("DEMO 7: COMBAT SCENE WITH MECHANICS")

    combat_scene = story_gen.generate_scene(
        scene_type='combat',
        characters=['ben_bukowski', 'ruth_carter'],
        context={}
    )

    print(f"Title: {combat_scene.title}")
    print(f"Setting: {combat_scene.setting}")
    print(f"Hook: {combat_scene.hook}")

    print("\nRunning combat round: Ben vs Victor (training)")
    combat = dm.run_combat_round('ben_bukowski', 'victor_hernandez', 'Training exercise')

    print(f"\nAttacker: {combat['attacker']}")
    print(f"Defender: {combat['defender']}")
    print(f"\nAttack Roll: {combat['attack_roll']['formatted']}")
    print(f"Defense Roll: {combat['defense_roll']['formatted']}")

    if combat['hit']:
        print(f"\n✓ HIT!")
        print(f"  Damage: {combat['damage']}")
        if combat['injury']:
            print(f"  Injury: {combat['injury'].severity} (penalty: {combat['injury'].penalty})")
        print(f"  {combat['defender']} Health: {combat['defender_health']}")
    else:
        print(f"\n✗ MISS! {combat['defender']} evades the attack.")

    # Summary
    print_divider("SYSTEM SUMMARY")

    summary = dm.get_session_summary()

    print("✅ Story Generation Features:")
    print("  - Campaign outline generation (5 themes)")
    print("  - Scene generation (5 types: investigation, combat, social, temporal, rest)")
    print("  - Full session planning with multiple scenes")
    print("  - Character-focused narratives")
    print("  - Lore integration (Book 1 & 2 context)")

    print("\n✅ Mechanics Integration:")
    print("  - Skill checks with dice rolls")
    print("  - Combat system with damage and injuries")
    print("  - Temporal powers (TC/TS/TIP tracking)")
    print("  - Character state management")
    print("  - Health and stamina tracking")

    print(f"\n📊 Session Stats:")
    print(f"  Total rolls this session: {summary['total_rolls']}")
    print(f"  Characters active: {', '.join(summary['characters_active'])}")

    print_divider()
    print("Story generation system fully functional!")
    print("\nTo use interactively:")
    print("  python3 run_story_session.py")
    print("\nTo use as library:")
    print("  from core.story_generator import StoryGenerator")
    print("  story_gen = StoryGenerator()")
    print("  outline = story_gen.generate_campaign_outline(...)")
    print_divider()


if __name__ == '__main__':
    main()
