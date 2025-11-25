#!/usr/bin/env python3
"""
Example DM Session - Go Squad Book 3
Demonstrates how to use the system

Context: Kain has won the presidential election (end of Book 2).
This session takes place in the aftermath of his victory.
"""

from core.dm_master import DMSession

def print_divider(title=""):
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'='*70}\n")

def main():
    print_divider("GO SQUAD - EXAMPLE SESSION")

    # Initialize session
    print("Initializing DM session...")
    dm = DMSession()
    print("✓ Session ready!\n")

    # Scene 1: Investigation
    print_divider("SCENE 1: Warehouse Investigation")
    print("Ahdia and Ruth investigate an abandoned warehouse for clues about")
    print("the recent Enhanced attacks. FAERIS provides aerial surveillance.")

    print("\n--- Ahdia makes an investigation check ---")
    result = dm.make_skill_check(
        'ahdia_bacchus',
        'investigation',
        'hard',
        modifiers={'FAERIS_drone': 5, 'night_vision': 2}
    )
    print(result['formatted'])
    print(f"Quality: {result['interpretation'].replace('_', ' ').title()}")

    if result['result'].success:
        print("\nNarration: Ahdia spots unusual energy signatures in the corner.")
        print("The patterns suggest temporal manipulation - but not hers.")

    # Scene 2: Combat Encounter
    print_divider("SCENE 2: Unexpected Encounter")
    print("Victor appears - testing the team's combat readiness in a sparring match.")

    print("\n--- Ben spars with Victor ---")
    combat = dm.run_combat_round('ben_bukowski', 'victor_hernandez', "Training sparring")
    print(f"\nAttack: {combat['attack_roll']['formatted']}")
    print(f"Defense: {combat['defense_roll']['formatted']}")

    if combat['hit']:
        print(f"\n✓ HIT! Damage: {combat['damage']}")
        print(f"Victor injured: {combat['injury'].severity}")
        print(f"Remaining health: {combat['defender_health']}")
    else:
        print(f"\n✗ MISS! Victor deflects Ben's attack with practiced ease.")

    # Scene 3: Temporal Power Usage
    print_divider("SCENE 3: Temporal Intervention")
    print("The situation escalates! Ahdia uses Temporal Perception to predict")
    print("the next moves and guide the team strategically.")

    ahdia = dm.get_character_systems('ahdia_bacchus')

    print("\n--- Checking Ahdia's temporal resources ---")
    status = ahdia['temporal'].get_current_status()
    print(f"TC: {status['resources']['tc']}")
    print(f"TS: {status['resources']['ts']}")
    print(f"Status: {status['strain_status']}")

    print("\n--- Ahdia uses Temporal Perception ---")
    power_result = ahdia['temporal'].use_power(
        'temporal_perception',
        context="Predict combat patterns during training"
    )

    if power_result.success:
        print(f"✓ Power activated!")
        print(f"Cost: -{power_result.tc_cost} TC, +{power_result.ts_cost} TS")
        print(f"New TC: {power_result.new_resources.tc}/100")
        print(f"New TS: {power_result.new_resources.ts}/100")
        print(f"\nNarration: Ahdia's perception shifts. She sees the next 6 seconds")
        print("of possible futures, analyzing combat patterns for tactical advantage.")

    # Scene 4: Escape
    print_divider("SCENE 4: Rooftop Escape")
    print("The team scales the fire escape. Ruth makes a difficult athletics check.")

    print("\n--- Ruth attempts a hard climb ---")
    result = dm.make_skill_check(
        'ruth_carter',
        'combat',  # Using combat as proxy for athletics
        'hard',
        modifiers={'tactical_gear': 2}
    )
    print(result['formatted'])

    if result['result'].success:
        print("\nNarration: Ruth pulls herself onto the roof, breathing hard but safe.")
    else:
        print("\nNarration: Ruth struggles, her injured shoulder slowing her down.")
        print("Ben reaches down and hauls her up the last few feet.")

    # Scene 5: Recovery
    print_divider("SCENE 5: Safe House - Recovery")
    print("The team reaches a safe house. Time to rest and treat injuries.")

    print("\n--- Ruth rests (long rest) ---")
    recovered = ahdia['stamina'].rest(short_rest=False)
    print(f"✓ Stamina recovered: +{recovered}")

    print("\n--- Ahdia sleeps for 8 hours ---")
    ahdia['temporal'].sleep(hours=8)
    status = ahdia['temporal'].get_current_status()
    print(f"✓ Sleep complete")
    print(f"  TC: {status['resources']['tc']}/100")
    print(f"  TS: {status['resources']['ts']}/100")

    # Session Summary
    print_divider("SESSION SUMMARY")
    summary = dm.get_session_summary()
    print(f"Month: {summary['month']}")
    print(f"Characters active: {', '.join(summary['characters_active'])}")
    print(f"Total dice rolls: {summary['total_rolls']}")
    print(f"\nSystems used:")
    for char, systems in summary['systems_loaded'].items():
        print(f"  {char}: {', '.join(systems)}")

    print_divider()
    print("Session complete! The team completed their training exercise")
    print("and Ahdia practiced managing her temporal powers efficiently.")
    print_divider()

if __name__ == '__main__':
    main()
