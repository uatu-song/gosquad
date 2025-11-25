#!/usr/bin/env python3
"""
Demo script to show DMStoryGen functionality without interactive input
"""

from core.dm_master import DMSession

def print_divider():
    print("\n" + "="*70 + "\n")

def main():
    print_divider()
    print("GO SQUAD - BOOK 3 CAMPAIGN DEMO")
    print("Automated demonstration of game systems")
    print_divider()

    # Initialize session
    dm = DMSession()
    print("✓ Session initialized")
    print("✓ Character systems loaded")
    print("✓ Ready to play!\n")

    # Demo 1: Skill Check
    print_divider()
    print("DEMO 1: SKILL CHECK")
    print("Ahdia makes a stealth check (moderate difficulty)")
    print_divider()

    result = dm.make_skill_check('ahdia_bacchus', 'stealth', 'moderate', {})
    print("RESULT:")
    print(result['formatted'])
    print(f"Quality: {result['interpretation'].replace('_', ' ').title()}")

    # Demo 2: Character Status
    print_divider()
    print("DEMO 2: CHARACTER STATUS - Ahdia")
    print_divider()

    systems = dm.get_character_systems('ahdia_bacchus')
    print(f"Health: {systems['health'].current_health}/{systems['health'].max_health}")
    print(f"Stamina: {systems['stamina'].current_stamina}/{systems['stamina'].max_stamina}")

    if 'temporal' in systems:
        status = systems['temporal'].get_current_status()
        print(f"\nTemporal Resources:")
        print(f"  TC: {status['resources']['tc']}/100")
        print(f"  TS: {status['resources']['ts']}/100")
        print(f"  TIP: {status['resources']['tip']}/100")
        if 'baseline_percentage' in status['resources']:
            print(f"  Baseline: {status['resources']['baseline_percentage']:.1f}%")
        print(f"\nAvailable Powers: {', '.join(status['available_powers'])}")

    # Demo 3: Temporal Power
    print_divider()
    print("DEMO 3: TEMPORAL POWER")
    print("Ahdia uses 'glimpse_future' power")
    print_divider()

    ahdia_temporal = systems['temporal']
    # Use one of the available powers
    result = ahdia_temporal.use_power('temporal_perception', context='Scouting ahead')

    if result.success:
        print(f"✓ Used {result.power_name}")
        print(f"\nCosts:")
        print(f"  TC: {result.new_resources.tc}/100 (-{result.tc_cost})")
        print(f"  TS: {result.new_resources.ts}/100 (+{result.ts_cost})")
        print(f"\nStatus: {result.strain_status['status']}")
    else:
        print(f"✗ Cannot use power")

    # Demo 4: Combat
    print_divider()
    print("DEMO 4: COMBAT ROUND")
    print("Ben attacks Victor Hernandez")
    print_divider()

    combat = dm.run_combat_round('ben_bukowski', 'victor_hernandez', 'Training exercise')
    print(f"{combat['attacker']} vs {combat['defender']}")
    print(f"\nAttack: {combat['attack_roll']['formatted']}")
    print(f"Defense: {combat['defense_roll']['formatted']}")
    print(f"\n{'HIT!' if combat['hit'] else 'MISS!'}")

    if combat['hit']:
        print(f"Damage: {combat['damage']}")
        if combat['injury']:
            print(f"Injury: {combat['injury'].severity} (penalty: {combat['injury'].penalty})")
        print(f"{combat['defender']} Health: {combat['defender_health']}")

    # Demo 5: Session Summary
    print_divider()
    print("DEMO 5: SESSION SUMMARY")
    print_divider()

    summary = dm.get_session_summary()
    print(f"Month: {summary['month']}")
    print(f"Active Characters: {', '.join(summary['characters_active'])}")
    print(f"Total Rolls: {summary['total_rolls']}")
    print(f"\nSystems Loaded:")
    for char, systems in summary['systems_loaded'].items():
        print(f"  {char}: {', '.join(systems)}")

    print_divider()
    print("Demo complete!")
    print_divider()

if __name__ == '__main__':
    main()
