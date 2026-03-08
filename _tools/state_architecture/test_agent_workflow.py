#!/usr/bin/env python3
"""
Go Squad Agent Workflow Test

Tests the complete agent workflow:
1. Agent receives task
2. Agent queries data (via Archivist)
3. Agent produces output + process log
4. Gate validates process log
5. Result approved/rejected

This simulates a Status Tracker checking character knowledge state.
"""

from query import StateQuery, QueryResult
from process_log import ProcessLog, GateValidator, get_consultation_log


def simulate_status_tracker_workflow():
    """
    Simulate a Status Tracker agent checking who knows about exile_island.

    Task: "Who knows about Ahdia's exile_island operation at chapter 13?"

    This is the simplest meaningful agent task:
    - Clear domain (Status Tracker tracks knowledge state)
    - Requires Archivist query
    - Verifiable answer
    - Read-only (no state changes)
    """

    print("=" * 70)
    print("STATUS TRACKER AGENT WORKFLOW TEST")
    print("=" * 70)
    print()
    print("Task: Who knows about exile_island at chapter 13?")
    print()

    # Initialize
    sq = StateQuery()
    consultation_log = get_consultation_log()

    # Create process log
    log = ProcessLog(
        agent_role="status_tracker",
        task_id="ST_001_knowledge_check_exile_island_ch13"
    )

    # Step 1: Declare domain
    print("Step 1: Declare domain...")
    log.declare_domain(
        task_description="Check character knowledge state for exile_island secret at chapter 13",
        justification="Tracking who knows what is core Status Tracker function (knowledge_check)"
    )
    print("  ✓ Domain declared")

    # Step 2: Query Archivist (via StateQuery interface)
    print("\nStep 2: Query Archivist for knowledge data...")

    # Query 1: Who knows at chapter 13
    result = sq.who_knows("exile_island", 13)

    # Log the consultation
    consultation_id = consultation_log.log_consultation(
        requester_role="status_tracker",
        requester_task_id="ST_001_knowledge_check_exile_island_ch13",
        responder_role="archivist",
        query="who_knows('exile_island', 13)",
        response_summary=f"Found {len(result.data)} characters who know",
        response_sources=[result.source_file]
    )

    # Add to process log
    log.add_query(
        query="who_knows('exile_island', 13)",
        target="archivist",
        response_summary=f"Retrieved {len(result.data)} characters: {result.data}"
    )
    print(f"  ✓ Query complete: {len(result.data)} characters know")

    # Query 2: For comparison, check chapter 12 (before reveal)
    result_before = sq.who_knows("exile_island", 12)

    consultation_log.log_consultation(
        requester_role="status_tracker",
        requester_task_id="ST_001_knowledge_check_exile_island_ch13",
        responder_role="archivist",
        query="who_knows('exile_island', 12)",
        response_summary=f"Found {len(result_before.data)} characters who knew before reveal",
        response_sources=[result_before.source_file]
    )

    log.add_query(
        query="who_knows('exile_island', 12)",
        target="archivist",
        response_summary=f"Before reveal (ch12): {result_before.data}"
    )
    print(f"  ✓ Comparison query: {len(result_before.data)} knew before reveal")

    # Step 3: Add source attribution
    print("\nStep 3: Attribute sources...")
    log.add_source(
        claim=f"At chapter 13, {len(result.data)} characters know about exile_island",
        source_file=result.source_file,
        source_section=result.source_section
    )
    log.add_source(
        claim=f"At chapter 12, only {len(result_before.data)} characters knew (before team discovery)",
        source_file=result_before.source_file,
        source_section=result_before.source_section
    )
    print("  ✓ Sources attributed")

    # Step 4: Set output
    print("\nStep 4: Generate output...")
    output_content = {
        "query": "Who knows about exile_island at chapter 13?",
        "chapter": 13,
        "knowledge_item": "exile_island",
        "who_knows": result.data,
        "analysis": {
            "chapter_12_knew": result_before.data,
            "chapter_13_knew": result.data,
            "newly_learned": [c for c in result.data if c not in result_before.data],
            "reveal_event": "Team discovers Ahdia's solo global operations"
        }
    }

    log.set_output(
        content=output_content,
        confidence="high",
        caveats=["Based on explicit knowledge_tracking data only"]
    )
    print("  ✓ Output generated")

    # Step 5: Validate
    print("\nStep 5: Gate validation...")
    validation = log.validate()
    print(f"  Status: {validation.status.value.upper()}")

    if validation.issues:
        print("  Issues:")
        for issue in validation.issues:
            print(f"    ✗ {issue}")

    if validation.warnings:
        print("  Warnings:")
        for warning in validation.warnings:
            print(f"    ⚠ {warning}")

    if not validation.issues and not validation.warnings:
        print("  ✓ No issues or warnings")

    # Print full process log
    print("\n" + "=" * 70)
    print("FULL PROCESS LOG")
    print("=" * 70)
    print(log)

    # Print consultation chain
    print("\n" + "=" * 70)
    print("CONSULTATION CHAIN")
    print("=" * 70)
    chain = consultation_log.get_chain("ST_001_knowledge_check_exile_island_ch13")
    for c in chain:
        print(f"\n[{c['consultation_id']}]")
        print(f"  {c['requester']['role']} → {c['responder']['role']}")
        print(f"  Query: {c['query']}")
        print(f"  Response: {c['response_summary']}")
        print(f"  Sources: {c['response_sources']}")

    return validation.status.value == "approved"


def simulate_out_of_lane_attempt():
    """
    Simulate a Status Tracker trying to do Theme Guardian's job.

    This should be REJECTED.
    """

    print("\n" + "=" * 70)
    print("OUT-OF-LANE ATTEMPT TEST")
    print("=" * 70)
    print()
    print("Task: Status Tracker tries to evaluate thematic consistency")
    print()

    log = ProcessLog(
        agent_role="status_tracker",
        task_id="ST_002_theme_check_should_fail"
    )

    # Status Tracker tries to declare a thematic task
    log.declare_domain(
        task_description="Evaluate thematic consistency of chapter 13 revelation",
        justification="Themes affect character emotional states"  # Weak justification
    )

    # No queries to theme_guardian (should have deferred)
    log.add_query(
        query="get_character_state('ahdia', 13)",
        target="archivist",
        response_summary="Got character state"
    )

    # Produces thematic output (outside domain!)
    log.set_output(
        content={
            "thematic_assessment": "Revelation aligns with CBT-failing arc",
            "recommendation": "Increase emotional weight of team confrontation"
        },
        confidence="medium"
    )

    # Validate
    validation = log.validate()

    print("Result:")
    print(validation)

    if validation.status.value == "rejected":
        print("\n✓ Correctly REJECTED out-of-lane attempt")
    else:
        print("\n✗ Should have been rejected!")

    return validation.status.value == "rejected"


def simulate_character_steward_without_mode():
    """
    Simulate a Character Steward forgetting to declare mode.

    This should be REJECTED.
    """

    print("\n" + "=" * 70)
    print("CHARACTER STEWARD MISSING MODE TEST")
    print("=" * 70)
    print()
    print("Task: Character Steward generates dialogue without mode declaration")
    print()

    log = ProcessLog(
        agent_role="character_steward",
        task_id="CS_001_ahdia_dialogue_ch13"
        # No mode specified!
    )

    log.declare_domain(
        task_description="Generate Ahdia's dialogue when team confronts her about exile_island",
        justification="Character dialogue is Character Steward domain"
    )

    log.add_query(
        query="get_character_state('ahdia', 13)",
        target="archivist",
        response_summary="Retrieved Ahdia state at confrontation"
    )

    log.add_source(
        claim="Ahdia is emotionally exposed_desperate at chapter 13",
        source_file="CHARACTER_STATE_INDEX.yaml",
        source_section="characters.ahdia.emotional_progression"
    )

    log.set_output(
        content={
            "dialogue": "You don't understand. I was trying to help.",
            "emotional_register": "defensive, guilt-ridden"
        },
        confidence="high"
    )

    # Validate
    validation = log.validate()

    print("Result:")
    print(validation)

    if validation.status.value == "rejected":
        print("\n✓ Correctly REJECTED - missing mode declaration")
    else:
        print("\n✗ Should have been rejected for missing mode!")

    return validation.status.value == "rejected"


def main():
    """Run all workflow tests."""
    print("\n" + "#" * 70)
    print("# GO SQUAD AGENT WORKFLOW TESTS")
    print("#" * 70 + "\n")

    results = {}

    # Test 1: Valid Status Tracker workflow
    results["valid_workflow"] = simulate_status_tracker_workflow()

    # Test 2: Out-of-lane attempt
    results["out_of_lane_rejected"] = simulate_out_of_lane_attempt()

    # Test 3: Character Steward missing mode
    results["missing_mode_rejected"] = simulate_character_steward_without_mode()

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    all_passed = True
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("All tests passed! Process log system working correctly.")
    else:
        print("Some tests failed. Review output above.")

    return all_passed


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
