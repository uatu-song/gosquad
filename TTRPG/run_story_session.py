#!/usr/bin/env python3
"""
Interactive Story Session Runner
Combines story generation with game mechanics for complete DM experience
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


def print_section(title):
    print(f"\n{'-'*70}")
    print(f"  {title}")
    print(f"{'-'*70}\n")


def main():
    print_divider("GO SQUAD BOOK 3 - STORY SESSION")

    # Initialize systems
    print("Initializing story generation and game mechanics...")
    story_gen = StoryGenerator()
    dm = DMSession()
    print("✓ Systems ready!\n")

    # Main menu
    while True:
        print_section("MAIN MENU")
        print("1. Generate new campaign outline")
        print("2. Generate scene with mechanics")
        print("3. Run full session plan")
        print("4. Quick story demo")
        print("5. Exit")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            generate_campaign_menu(story_gen)
        elif choice == '2':
            generate_scene_menu(story_gen, dm)
        elif choice == '3':
            run_session_menu(story_gen, dm)
        elif choice == '4':
            quick_demo(story_gen, dm)
        elif choice == '5':
            print("\nEnding session. Goodbye!")
            break
        else:
            print("Invalid choice.")


def generate_campaign_menu(story_gen):
    """Generate a campaign outline"""
    print_section("GENERATE CAMPAIGN OUTLINE")

    print("Available characters:")
    print("  1. ahdia_bacchus")
    print("  2. ruth_carter")
    print("  3. ben_bukowski")
    print("  4. tess_whitford")
    print("  5. victor_hernandez")

    char_choice = input("\nFocus character (or press Enter for Ahdia): ").strip()
    char_map = {
        '1': 'ahdia_bacchus',
        '2': 'ruth_carter',
        '3': 'ben_bukowski',
        '4': 'tess_whitford',
        '5': 'victor_hernandez'
    }
    focus_char = char_map.get(char_choice, 'ahdia_bacchus')

    print("\nAvailable themes:")
    print("  1. resistance_against_kain")
    print("  2. institutional_collapse")
    print("  3. temporal_instability")
    print("  4. personal_sacrifice")
    print("  5. trust_and_betrayal")

    theme_choice = input("\nTheme (or press Enter for random): ").strip()
    theme_map = {
        '1': 'resistance_against_kain',
        '2': 'institutional_collapse',
        '3': 'temporal_instability',
        '4': 'personal_sacrifice',
        '5': 'trust_and_betrayal'
    }
    theme = theme_map.get(theme_choice, None)

    duration = input("\nDuration in months (default 3): ").strip()
    duration = int(duration) if duration.isdigit() else 3

    print("\nGenerating campaign outline...")
    outline = story_gen.generate_campaign_outline(focus_char, theme, duration)

    print_divider()
    print(f"TITLE: {outline.title}")
    print_divider()
    print(f"PREMISE:\n{outline.premise}")
    print(f"\nTHEMES: {', '.join(outline.themes)}")
    print(f"SESSIONS: {outline.session_count}")
    print(f"KEY NPCs: {', '.join(outline.key_npcs)}")

    print("\nACTS:")
    for i, act in enumerate(outline.acts, 1):
        print(f"\n  Act {i}: {act['name']}")
        print(f"  {act['description']}")
        print(f"  Duration: {act['duration_sessions']} sessions")

    print("\nMAJOR EVENTS:")
    for event in outline.major_events:
        print(f"  - {event}")

    print_divider()


def generate_scene_menu(story_gen, dm):
    """Generate a scene with mechanics"""
    print_section("GENERATE SCENE")

    print("Scene types:")
    print("  1. Investigation")
    print("  2. Combat")
    print("  3. Social/Dialogue")
    print("  4. Temporal (Ahdia)")
    print("  5. Rest/Recovery")

    scene_map = {
        '1': 'investigation',
        '2': 'combat',
        '3': 'social',
        '4': 'temporal',
        '5': 'rest'
    }

    scene_choice = input("\nScene type: ").strip()
    scene_type = scene_map.get(scene_choice, 'investigation')

    print("\nCharacters (comma-separated):")
    print("Available: ahdia_bacchus, ruth_carter, ben_bukowski, victor_hernandez, leah_turner, tess_whitford")
    char_input = input("Characters: ").strip()
    characters = [c.strip() for c in char_input.split(',') if c.strip()]

    if not characters:
        characters = ['ahdia_bacchus']

    print("\nGenerating scene...")
    scene = story_gen.generate_scene(scene_type, characters, {})

    print_divider(scene.title)
    print(f"SETTING: {scene.setting}")
    print(f"CHARACTERS: {', '.join(scene.characters)}")
    print(f"\nHOOK:\n{scene.hook}")

    print(f"\nCOMPLICATIONS:")
    for comp in scene.complications:
        print(f"  - {comp}")

    print(f"\nNARRATIVE BEATS:")
    for i, beat in enumerate(scene.narrative_beats, 1):
        print(f"  {i}. {beat}")

    print(f"\nSUGGESTED CHECKS:")
    for check in scene.suggested_checks:
        print(f"  - {check['character']}: {check['skill']} ({check['difficulty']})")

    print(f"\nDM NOTES:\n{scene.dm_notes}")

    # Offer to run the checks
    print_divider()
    run_checks = input("Run the suggested checks? (y/n): ").strip().lower()

    if run_checks == 'y':
        print("\nRunning checks...")
        for check in scene.suggested_checks:
            try:
                result = dm.make_skill_check(
                    check['character'],
                    check['skill'],
                    check['difficulty'],
                    check.get('modifiers', {})
                )
                print(f"\n{result['formatted']}")
                print(f"Quality: {result['interpretation'].replace('_', ' ').title()}")
            except Exception as e:
                print(f"Error: {e}")

    print_divider()


def run_session_menu(story_gen, dm):
    """Run a full session plan"""
    print_section("RUN FULL SESSION")

    # First generate a campaign
    print("Generating campaign outline...")
    outline = story_gen.generate_campaign_outline('ahdia_bacchus', 'temporal_instability', 3)

    print(f"\nCampaign: {outline.title}")
    print(f"Sessions planned: {outline.session_count}")

    session_num = input("\nWhich session to generate? (1-12): ").strip()
    session_num = int(session_num) if session_num.isdigit() else 1

    print(f"\nGenerating Session {session_num}...")
    session = story_gen.generate_session_plan(session_num, outline, [])

    print_divider(f"SESSION {session['session_number']}")
    print(f"ACT: {session['act']}")
    print(f"\n{session['act_description']}")

    print(f"\nSESSION GOALS:")
    for goal in session['session_goals']:
        print(f"  - {goal}")

    print(f"\nSCENES ({len(session['scenes'])}):")
    for i, scene in enumerate(session['scenes'], 1):
        print(f"\n  {i}. {scene.title}")
        print(f"     Setting: {scene.setting}")
        print(f"     Characters: {', '.join(scene.characters)}")
        print(f"     Hook: {scene.hook}")

    print(f"\nDM PREP:")
    print(f"  {session['dm_prep_notes']}")

    # Offer to run scenes
    print_divider()
    run_scenes = input("Run scenes interactively? (y/n): ").strip().lower()

    if run_scenes == 'y':
        for i, scene in enumerate(session['scenes'], 1):
            print_divider(f"SCENE {i}: {scene.title}")
            print(f"Setting: {scene.setting}")
            print(f"\n{scene.hook}")

            input("\nPress Enter to see complications...")
            print("\nComplications:")
            for comp in scene.complications:
                print(f"  - {comp}")

            input("\nPress Enter to run checks...")
            for check in scene.suggested_checks:
                try:
                    result = dm.make_skill_check(
                        check['character'],
                        check['skill'],
                        check['difficulty'],
                        check.get('modifiers', {})
                    )
                    print(f"\n{result['formatted']}")
                    print(f"Quality: {result['interpretation'].replace('_', ' ').title()}")
                except Exception as e:
                    print(f"Error: {e}")

            input("\nPress Enter for next scene...")

    print_divider()


def quick_demo(story_gen, dm):
    """Run a quick demonstration"""
    print_divider("QUICK STORY DEMO")

    print("Generating temporal instability campaign for Ahdia...")
    outline = story_gen.generate_campaign_outline('ahdia_bacchus', 'temporal_instability', 2)

    print(f"\nTitle: {outline.title}")
    print(f"Premise: {outline.premise[:200]}...")

    print("\nGenerating opening scene...")
    scene = story_gen.generate_scene('temporal', ['ahdia_bacchus', 'ruth_carter'], {})

    print(f"\nScene: {scene.title}")
    print(f"Hook: {scene.hook}")

    print("\nRunning Ahdia's skill check...")
    result = dm.make_skill_check('ahdia_bacchus', 'combat', 'hard', {})
    print(f"\n{result['formatted']}")
    print(f"Quality: {result['interpretation'].replace('_', ' ').title()}")

    print("\nChecking Ahdia's temporal resources...")
    ahdia = dm.get_character_systems('ahdia_bacchus')
    if 'temporal' in ahdia:
        status = ahdia['temporal'].get_current_status()
        print(f"  TC: {status['resources']['tc']}/100")
        print(f"  TS: {status['resources']['ts']}/100")
        # strain_status might be a string or dict
        strain_status = status.get('strain_status', 'normal')
        if isinstance(strain_status, dict):
            print(f"  Status: {strain_status.get('status', 'normal')}")
        else:
            print(f"  Status: {strain_status}")

    print_divider()
    print("Demo complete! Story generation integrated with game mechanics.")
    print_divider()


if __name__ == '__main__':
    main()
