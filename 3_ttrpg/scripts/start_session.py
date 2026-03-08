#!/usr/bin/env python3
"""
Interactive DM Session - Go Squad Book 3
Simple interface to run game sessions

Context: Book 2 has concluded with Kain winning the presidential election.
This campaign explores what happens AFTER Kain becomes President.
"""

import os
import sys

# Ensure we're running from the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from core.dm_master import DMSession

def print_divider():
    print("\n" + "="*70 + "\n")

def main():
    print_divider()
    print("GO SQUAD - BOOK 3 CAMPAIGN")
    print("Interactive DM Session")
    print("(After Kain's Election Victory)")
    print_divider()

    # Initialize session
    dm = DMSession()
    print("✓ Session initialized")
    print("✓ Character systems loaded")
    print("✓ Ready to play!\n")

    while True:
        print("\n" + "-"*70)
        print("MAIN MENU")
        print("-"*70)
        print("1. Make a skill check")
        print("2. Run combat round")
        print("3. Use Ahdia's temporal power")
        print("4. Check character status")
        print("5. Rest/Recovery")
        print("6. Session summary")
        print("7. Exit")

        choice = input("\nWhat would you like to do? ").strip()

        if choice == '1':
            skill_check_menu(dm)
        elif choice == '2':
            combat_menu(dm)
        elif choice == '3':
            temporal_powers_menu(dm)
        elif choice == '4':
            character_status_menu(dm)
        elif choice == '5':
            recovery_menu(dm)
        elif choice == '6':
            show_summary(dm)
        elif choice == '7':
            print("\nEnding session. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def skill_check_menu(dm):
    """Make a skill check"""
    print("\n--- SKILL CHECK ---")
    print("Available characters: ahdia_bacchus, ruth_carter, ben_bukowski")
    char_id = input("Character ID: ").strip()

    valid_chars = ['ahdia_bacchus', 'ruth_carter', 'ben_bukowski']
    if char_id not in valid_chars:
        print(f"❌ Invalid character! Must be one of: {', '.join(valid_chars)}")
        return

    print("\nSkills: combat, investigation, stealth, medical, leadership, tech")
    skill = input("Skill: ").strip()

    valid_skills = ['combat', 'investigation', 'stealth', 'medical', 'leadership', 'tech']
    if skill not in valid_skills:
        print(f"❌ Invalid skill! Must be one of: {', '.join(valid_skills)}")
        return

    print("\nDifficulty: trivial, easy, moderate, hard, very_hard, nearly_impossible")
    difficulty = input("Difficulty: ").strip()

    valid_difficulties = ['trivial', 'easy', 'moderate', 'hard', 'very_hard', 'nearly_impossible']
    if difficulty not in valid_difficulties:
        print(f"❌ Invalid difficulty! Must be one of: {', '.join(valid_difficulties)}")
        return

    # Optional modifiers
    print("\nModifiers (optional, press Enter to skip):")
    mod_name = input("  Modifier source (e.g., 'FAERIS_drone', 'darkness'): ").strip()
    modifiers = {}
    if mod_name:
        try:
            mod_value = int(input("  Modifier value (e.g., 5, -2): ").strip())
            modifiers[mod_name] = mod_value
        except ValueError:
            print("⚠️  Invalid modifier value, skipping modifiers")

    # Make the check
    try:
        result = dm.make_skill_check(char_id, skill, difficulty, modifiers)

        print_divider()
        print("RESULT:")
        print(result['formatted'])
        print(f"Quality: {result['interpretation'].replace('_', ' ').title()}")
        if result['modifier_details']:
            print(f"Modifiers: {', '.join(result['modifier_details'])}")
        print_divider()
    except Exception as e:
        print(f"❌ Error making skill check: {e}")
        print_divider()

def combat_menu(dm):
    """Run a combat round"""
    print("\n--- COMBAT ROUND ---")
    print("Available characters: ahdia_bacchus, ruth_carter, ben_bukowski, police_officer, tank_cop")

    attacker = input("Attacker ID: ").strip()
    defender = input("Defender ID: ").strip()
    context = input("Context (e.g., 'Rooftop chase'): ").strip()

    combat = dm.run_combat_round(attacker, defender, context)

    print_divider()
    print("COMBAT RESULT:")
    print(f"{combat['attacker']} vs {combat['defender']}")
    print(f"\nAttack: {combat['attack_roll']['formatted']}")
    print(f"Defense: {combat['defense_roll']['formatted']}")
    print(f"\n{'HIT!' if combat['hit'] else 'MISS!'}")

    if combat['hit']:
        print(f"Damage: {combat['damage']}")
        if combat['injury']:
            print(f"Injury: {combat['injury'].severity} (penalty: {combat['injury'].penalty})")
        print(f"{combat['defender']} Health: {combat['defender_health']}")
    print_divider()

def temporal_powers_menu(dm):
    """Use Ahdia's temporal powers"""
    print("\n--- TEMPORAL POWERS (AHDIA ONLY) ---")

    ahdia = dm.get_character_systems('ahdia_bacchus')

    if 'temporal' not in ahdia:
        print("Error: Only Ahdia can use temporal powers!")
        return

    tp = ahdia['temporal']
    status = tp.get_current_status()

    print(f"\nCurrent Resources:")
    print(f"  TC (Temporal Charge): {status['resources']['tc']}/100")
    print(f"  TS (Temporal Strain): {status['resources']['ts']}/100")
    print(f"  TIP (Temporal Instability): {status['resources']['tip']}/100")
    print(f"  Baseline: {status['resources']['baseline_percentage']:.1f}%")
    print(f"\nStatus: {status['strain_status']['status']}")

    print("\nAvailable Powers:")
    for i, power in enumerate(status['available_powers'], 1):
        print(f"  {i}. {power}")

    print("\n0. Cancel")
    choice = input("\nSelect power (number): ").strip()

    if choice == '0':
        return

    power_index = int(choice) - 1
    if 0 <= power_index < len(status['available_powers']):
        power_name = status['available_powers'][power_index]
        context = input("Context/description: ").strip()

        result = tp.use_power(power_name, context=context)

        print_divider()
        if result.success:
            print(f"✓ Used {result.power_name}")
            print(f"\nCosts:")
            print(f"  TC: {result.new_resources.tc}/100 (-{result.tc_cost})")
            print(f"  TS: {result.new_resources.ts}/100 (+{result.ts_cost})")
            if result.tip_cost > 0:
                print(f"  TIP: {result.new_resources.tip}/100 (+{result.tip_cost})")
            print(f"\nStatus: {result.strain_status['status']}")
        else:
            print(f"✗ Cannot use {power_name}: {result.message}")
        print_divider()

def character_status_menu(dm):
    """Check character status"""
    print("\n--- CHARACTER STATUS ---")
    char_id = input("Character ID: ").strip()

    systems = dm.get_character_systems(char_id)

    print_divider()
    print(f"STATUS: {char_id.upper()}")
    print_divider()

    # Health
    print(f"Health: {systems['health'].current_health}/{systems['health'].max_health}")
    if systems['health'].injuries:
        print(f"Injuries: {len(systems['health'].injuries)}")
        for inj in systems['health'].injuries:
            print(f"  - {inj.severity}: {inj.description} (penalty: {inj.penalty})")

    # Stamina
    print(f"\nStamina: {systems['stamina'].current_stamina}/{systems['stamina'].max_stamina}")
    print(f"Exhaustion Level: {systems['stamina'].exhaustion_level}")
    if systems['stamina'].exhaustion_level > 0:
        print(f"Penalty: {systems['stamina'].get_exhaustion_penalty()}")

    # Temporal (if Ahdia)
    if 'temporal' in systems:
        status = systems['temporal'].get_current_status()
        print(f"\nTemporal Resources:")
        print(f"  TC: {status['resources']['tc']}/100")
        print(f"  TS: {status['resources']['ts']}/100")
        print(f"  TIP: {status['resources']['tip']}/100")
        print(f"  Baseline: {status['resources']['baseline_percentage']:.1f}%")

    print_divider()

def recovery_menu(dm):
    """Rest and recovery"""
    print("\n--- REST & RECOVERY ---")
    char_id = input("Character ID: ").strip()

    systems = dm.get_character_systems(char_id)

    print("\n1. Short rest (recover some stamina)")
    print("2. Long rest (recover more stamina)")
    print("3. Sleep (8 hours - stamina + reduce TS for Ahdia)")
    print("4. Medical treatment (Ahdia only)")

    choice = input("\nChoice: ").strip()

    if choice == '1':
        recovered = systems['stamina'].rest(short_rest=True)
        print(f"✓ Short rest: +{recovered} stamina")

    elif choice == '2':
        recovered = systems['stamina'].rest(short_rest=False)
        print(f"✓ Long rest: +{recovered} stamina")

    elif choice == '3':
        recovered = systems['stamina'].rest(short_rest=False)
        print(f"✓ Sleep: +{recovered} stamina")

        if 'temporal' in systems:
            systems['temporal'].sleep(hours=8)
            status = systems['temporal'].get_current_status()
            print(f"✓ Temporal recovery: TC={status['resources']['tc']}, TS={status['resources']['ts']}")

    elif choice == '4':
        if 'temporal' not in systems:
            print("Only Ahdia needs temporal treatment!")
            return

        print("Providers: ruth_carter, dr_ryu_tanaka")
        provider = input("Provider: ").strip()

        result = systems['temporal'].receive_treatment(provider)
        if result.success:
            print(f"✓ Treatment successful")
            print(f"  Baseline restored: +{result.baseline_restored:.1f}%")
            print(f"  TS reduced: -{result.ts_reduced}")

def show_summary(dm):
    """Show session summary"""
    summary = dm.get_session_summary()

    print_divider()
    print("SESSION SUMMARY")
    print_divider()
    print(f"Month: {summary['month']}")
    print(f"Active Characters: {', '.join(summary['characters_active'])}")
    print(f"Total Rolls: {summary['total_rolls']}")
    print(f"\nSystems Loaded:")
    for char, systems in summary['systems_loaded'].items():
        print(f"  {char}: {', '.join(systems)}")
    print_divider()

if __name__ == '__main__':
    main()
