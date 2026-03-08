#!/usr/bin/env python3
"""
Generate Chapter 14 escape sequences programmatically
"""

import os
import sys
import json

# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from core.narrative_engine import NarrativeEngine

def generate_escape_sequence(engine, character, location, escape_method):
    """Generate an escape sequence for a character"""

    prompt = f"{character} translocates to {location} but CADENS and TRIOMF agents immediately ambush them. {character} must fight and escape using {escape_method}"

    print(f"\n{'='*70}")
    print(f"ESCAPE SEQUENCE: {character.upper()}")
    print(f"Location: {location}")
    print(f"{'='*70}\n")

    # Process the prompt
    response = engine.process_prompt(prompt)

    # Show narration
    print("SCENE GENERATION:")
    print(response['narration'])
    print()

    # Execute checks if any
    if response['checks']:
        print("SKILL CHECKS:")
        for check in response['checks']:
            char_name = engine.story_gen._get_character_context(check['character'])['name']
            print(f"  - {char_name}: {check['skill']} ({check['difficulty']})")
        print()

        print("ROLLING CHECKS...")
        results = engine.execute_checks(response['scene'])

        for result in results:
            print(result['narration'])
            print()

    return {
        'character': character,
        'location': location,
        'prompt': prompt,
        'scene': response,
        'results': results if response['checks'] else []
    }

def main():
    print("="*70)
    print("CHAPTER 14 ESCAPE SEQUENCE GENERATOR")
    print("="*70)

    # Initialize engine
    engine = NarrativeEngine("chapter14_escapes.json")

    all_results = []

    # 1. Ruth - Penthouse with wing-glider
    print("\n\n" + "="*70)
    print("SEQUENCE 1: RUTH CARTER")
    print("="*70)
    result = generate_escape_sequence(
        engine,
        "Ruth Carter",
        "Ahdia's penthouse",
        "grabbing Diana and leaping out window, deploying battlesuit wing-glider tech to escape"
    )
    all_results.append(result)

    # 2. Ben - TBD location
    print("\n\n" + "="*70)
    print("SEQUENCE 2: BEN BUKOWSKI")
    print("="*70)
    result = generate_escape_sequence(
        engine,
        "Ben Bukowski",
        "police station rooftop",
        "his combat training and acrobatic skills to evade"
    )
    all_results.append(result)

    # 3. Victor - TBD location
    print("\n\n" + "="*70)
    print("SEQUENCE 3: VICTOR HERNANDEZ")
    print("="*70)
    result = generate_escape_sequence(
        engine,
        "Victor Hernandez",
        "warehouse district",
        "his enhanced strength and tactical thinking"
    )
    all_results.append(result)

    # 4. Leah - TBD location
    print("\n\n" + "="*70)
    print("SEQUENCE 4: LEAH TURNER")
    print("="*70)
    result = generate_escape_sequence(
        engine,
        "Leah Turner",
        "downtown marketplace",
        "her stealth skills and crowd navigation"
    )
    all_results.append(result)

    # 5. Korede - TBD location (if present)
    print("\n\n" + "="*70)
    print("SEQUENCE 5: KOREDE")
    print("="*70)
    result = generate_escape_sequence(
        engine,
        "Korede",
        "industrial zone",
        "tech knowledge and improvisation"
    )
    all_results.append(result)

    # 6. Ahdia - Last, with Bellatrix confrontation
    print("\n\n" + "="*70)
    print("SEQUENCE 6: AHDIA BACCHUS (FINAL)")
    print("="*70)
    prompt = "Ahdia is last to escape. She faces Bellatrix briefly before Tess can translocate her. Bellatrix says something cryptic about testing. Ahdia barely escapes."
    response = engine.process_prompt(prompt)
    print("SCENE GENERATION:")
    print(response['narration'])
    print()

    if response['checks']:
        print("ROLLING CHECKS...")
        results = engine.execute_checks(response['scene'])
        for result in results:
            print(result['narration'])
            print()

    all_results.append({
        'character': 'Ahdia',
        'location': 'CADENS underground',
        'prompt': prompt,
        'scene': response,
        'results': results if response['checks'] else []
    })

    # Save all results
    output_file = "story_content/book3_chapters/chapter14_escape_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print("\n\n" + "="*70)
    print(f"RESULTS SAVED TO: {output_file}")
    print("="*70)

    return all_results

if __name__ == '__main__':
    main()
