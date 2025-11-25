#!/usr/bin/env python3
"""
Interactive Prompt-Driven Story Session
Tell the system what you want to happen, and it generates the story
"""

import os
import sys

# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from core.narrative_engine import NarrativeEngine


def print_divider(char="="):
    print(f"\n{char*70}\n")


def print_section_header(title):
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}\n")


def main():
    print_divider()
    print("  GO SQUAD BOOK 3 - INTERACTIVE STORY SESSION".center(70))
    print("  Prompt-Driven Narrative Engine".center(70))
    print_divider()

    print("How it works:")
    print("  1. Tell me what you want to happen (e.g., 'Ahdia infiltrates CADENS')")
    print("  2. I'll generate the scene and run the mechanics")
    print("  3. I'll narrate what happens based on dice rolls")
    print("  4. You decide what happens next\n")

    print("Commands:")
    print("  - Type your story prompt to continue")
    print("  - 'status <character>' - Check character status")
    print("  - 'context' - View current story context")
    print("  - 'campaign' - View campaign status (month, resources, consequences)")
    print("  - 'advance' - Advance to next month")
    print("  - 'suggestions' - Get ideas for what to do next")
    print("  - 'save <filename>' - Save your session")
    print("  - 'load <filename>' - Load a saved session")
    print("  - 'quit' - End session")

    print_divider()

    # Initialize engine with campaign tracking
    import sys
    campaign_file = sys.argv[1] if len(sys.argv) > 1 else "default_campaign.json"
    engine = NarrativeEngine(campaign_file)

    # Track prompt count
    prompt_count = 0

    while True:
        # Get user input
        print_section_header(f"PROMPT {prompt_count + 1}")
        user_input = input("What happens? > ").strip()

        if not user_input:
            continue

        # Handle commands
        if user_input.lower() == 'quit':
            print("\nEnding session. Your story continues...")
            print_divider()
            break

        elif user_input.lower() == 'context':
            print_section_header("CURRENT CONTEXT")
            print(f"Characters present: {', '.join(engine.context['characters_present']) if engine.context['characters_present'] else 'None'}")
            print(f"Location: {engine.context['location'] or 'Unknown'}")
            print(f"Tension level: {engine.context['tension_level']}")
            print(f"\nRecent events:")
            for event in engine.context['recent_events'][-5:]:
                print(f"  - {event}")
            continue

        elif user_input.lower() == 'campaign':
            print_section_header("CAMPAIGN STATUS")
            print(engine.get_campaign_status())
            print(f"\nPending consequences:")
            applicable = engine.campaign.consequences.get_applicable(engine.campaign.timeline.current_month)
            if applicable:
                for i, cons in enumerate(applicable[:5], 1):
                    print(f"  {i}. {cons['description']}")
            else:
                print("  None")
            continue

        elif user_input.lower() == 'advance':
            new_month = engine.advance_month()
            print(f"\n✓ Advanced to Month {new_month}")
            print(engine.get_campaign_status())
            continue

        elif user_input.lower() == 'suggestions':
            print_section_header("WHAT HAPPENS NEXT?")
            suggestions = engine.get_continuation_suggestions()
            for i, sug in enumerate(suggestions, 1):
                print(f"  {i}. {sug}")
            print("\nOr describe your own action!")
            continue

        elif user_input.lower().startswith('status '):
            char_id = user_input[7:].strip()
            print_section_header(f"CHARACTER STATUS: {char_id.upper()}")
            status = engine.get_character_status(char_id)
            if 'error' in status:
                print(f"Error: {status['error']}")
            else:
                print(f"Health: {status['health']}")
                print(f"Stamina: {status['stamina']}")
                if 'temporal' in status:
                    print(f"\nTemporal Resources:")
                    print(f"  TC: {status['temporal']['tc']}/100")
                    print(f"  TS: {status['temporal']['ts']}/100")
                    print(f"  TIP: {status['temporal']['tip']}/100")
            continue

        elif user_input.lower().startswith('save '):
            filename = user_input[5:].strip()
            if not filename.endswith('.json'):
                filename += '.json'
            saved_path = engine.save_session(filename)
            print(f"✓ Session saved to {saved_path}")
            print(f"✓ Campaign state auto-saved")
            continue

        elif user_input.lower() == 'save':
            # Save just campaign state
            saved_path = engine.save_session()
            print(f"✓ Campaign state saved to {saved_path}")
            continue

        elif user_input.lower().startswith('load '):
            filename = user_input[5:].strip()
            if not filename.endswith('.json'):
                filename += '.json'
            try:
                engine.load_session(filename)
                print(f"✓ Session loaded from {filename}")
                prompt_count = len(engine.story_history)
            except Exception as e:
                print(f"✗ Error loading session: {e}")
            continue

        # Process story prompt
        print_section_header("GENERATING SCENE")
        print(f"Processing: \"{user_input}\"\n")

        try:
            # Generate scene from prompt
            response = engine.process_prompt(user_input)

            # Show narration
            print(response['narration'])

            # Show suggested checks
            if response['checks']:
                print_divider("─")
                print("**Actions to resolve:**")
                for i, check in enumerate(response['checks'], 1):
                    char_name = engine.story_gen._get_character_context(check['character'])['name']
                    print(f"  {i}. {char_name} must make a {check['skill']} check ({check['difficulty']})")

                print_divider("─")

                # Ask if user wants to run checks
                run_checks = input("Run these checks? (y/n, or press Enter for yes) > ").strip().lower()

                if run_checks in ['', 'y', 'yes']:
                    print_section_header("RESOLVING ACTIONS")

                    # Execute checks
                    results = engine.execute_checks(response['scene'])

                    for result in results:
                        print(result['narration'])
                        print_divider("─")

                    # Show what happens next
                    print("\n**Story continues...**")
                    suggestions = engine.get_continuation_suggestions()
                    print("\nIdeas for what to do next:")
                    for i, sug in enumerate(suggestions[:3], 1):
                        print(f"  {i}. {sug}")
                    print()
                else:
                    print("\n(Checks skipped - you can narrate the outcome yourself)")
            else:
                # Pure narrative scene - no checks required
                print_divider("─")
                print("**This is a narrative scene. The story unfolds without mechanical resolution.**")
                print("\nIdeas for what to do next:")
                suggestions = engine.get_continuation_suggestions()
                for i, sug in enumerate(suggestions[:3], 1):
                    print(f"  {i}. {sug}")
                print()

            prompt_count += 1

        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("Try rephrasing your prompt or use 'suggestions' for ideas.")

    # Show session summary
    if prompt_count > 0:
        print_section_header("SESSION SUMMARY")
        print(f"Total story beats: {prompt_count}")
        print(f"Characters involved: {', '.join(set(engine.context['characters_present']))}")
        print(f"Final location: {engine.context['location'] or 'Unknown'}")
        print_divider()


if __name__ == '__main__':
    main()
