#!/usr/bin/env python3
"""
Go Squad Director CLI

Lightweight interface for directing the multi-agent system.
Works in manual mode - you copy prompts to Claude sessions,
paste results back for validation.

Usage:
    python3 director_cli.py                    # Interactive mode
    python3 director_cli.py prompt status_tracker
    python3 director_cli.py validate           # Paste process log
    python3 director_cli.py scene <chapter>    # Set up scene workflow
"""

import argparse
import yaml
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR / "templates" / "production_crew"
STATE_DIR = SCRIPT_DIR.parent / "state_architecture"
CHARACTERS_DIR = SCRIPT_DIR.parent.parent / "7_characters" / "arcs"
STORY_BIBLES_DIR = SCRIPT_DIR.parent.parent / "5_story_bibles"

# Agent roles
PRODUCTION_CREW = [
    "set_designer", "status_tracker", "theme_guardian", "timeline_keeper",
    "scene_choreographer", "reader_proxy", "archivist", "pacing_monitor",
    "technical_consultant", "intimacy_coordinator", "outline_assistant",
    "production_designer"
]

PERFORMANCE_CAST = ["character_steward"]


def load_template(role: str) -> dict:
    """Load an agent template."""
    template_path = TEMPLATES_DIR / f"{role}.yaml"
    if not template_path.exists():
        print(f"Error: Template not found: {template_path}")
        sys.exit(1)

    with open(template_path) as f:
        return yaml.safe_load(f)


def extract_prompt(role: str) -> str:
    """Extract system prompt from template."""
    template = load_template(role)
    return template.get("system_prompt", "")


def print_prompt(role: str):
    """Print the system prompt for copy-paste."""
    prompt = extract_prompt(role)

    print("=" * 70)
    print(f"AGENT: {role.upper()}")
    print("=" * 70)
    print("Copy everything below this line into a Claude session:")
    print("-" * 70)
    print(prompt)
    print("-" * 70)
    print("\nThen provide your task to the agent.")


def validate_process_log(log_text: str) -> dict:
    """
    Validate a process log against Go Squad protocol.

    Returns dict with:
        status: APPROVED / REJECTED / FLAGGED
        issues: list of blocking issues
        warnings: list of non-blocking warnings
    """
    issues = []
    warnings = []

    # Check for required sections
    required_sections = [
        ("PROCESS LOG", "Process log header missing"),
        ("Agent:", "Agent declaration missing"),
        ("Task:", "Task declaration missing"),
        ("DOMAIN DECLARATION:", "Domain declaration section missing"),
        ("In domain:", "Domain assertion missing"),
    ]

    for marker, error in required_sections:
        if marker not in log_text:
            issues.append(error)

    # Check for query log (required for most tasks)
    if "QUERY LOG:" in log_text:
        # Check if query log has content
        query_section = log_text.split("QUERY LOG:")[1].split("\n\n")[0] if "QUERY LOG:" in log_text else ""
        if "(no queries made)" in query_section.lower() or "→" not in query_section:
            warnings.append("Query log appears empty - verify queries were made if needed")
    else:
        issues.append("Query log section missing")

    # Check for source attribution
    if "SOURCE ATTRIBUTION:" not in log_text:
        issues.append("Source attribution section missing")
    else:
        source_section = log_text.split("SOURCE ATTRIBUTION:")[1].split("\n\n")[0] if "SOURCE ATTRIBUTION:" in log_text else ""
        if "Source:" not in source_section:
            warnings.append("No sources cited - is output based on memory alone?")

    # Check for deferred items section
    if "DEFERRED ITEMS:" not in log_text:
        warnings.append("Deferred items section missing - did agent defer appropriately?")

    # Check for output section
    if "OUTPUT:" not in log_text:
        issues.append("Output section missing")

    # Check for confidence declaration
    if "Confidence:" not in log_text:
        warnings.append("Confidence level not declared")

    # Character Steward specific: mode declaration
    # Check if this IS a character steward log (not just mentioning one in deferrals)
    agent_line = [line for line in log_text.split('\n') if line.strip().startswith('Agent:')]
    if agent_line and 'character_steward' in agent_line[0].lower():
        if "Mode:" not in log_text:
            issues.append("Character Steward must declare Mode (EXPLORATION/PERFORMANCE)")
        elif "EXPLORATION" not in log_text and "PERFORMANCE" not in log_text:
            issues.append("Character Steward mode must be EXPLORATION or PERFORMANCE")

    # Determine status
    if issues:
        status = "REJECTED"
    elif warnings:
        status = "FLAGGED"
    else:
        status = "APPROVED"

    return {
        "status": status,
        "issues": issues,
        "warnings": warnings
    }


def print_validation_result(result: dict):
    """Print validation result."""
    print("\n" + "=" * 70)
    print(f"VALIDATION: {result['status']}")
    print("=" * 70)

    if result['issues']:
        print("\nBLOCKING ISSUES:")
        for issue in result['issues']:
            print(f"  ✗ {issue}")

    if result['warnings']:
        print("\nWARNINGS (review recommended):")
        for warning in result['warnings']:
            print(f"  ⚠ {warning}")

    if result['status'] == "APPROVED":
        print("\n✓ Process log validates. Output can be accepted.")
    elif result['status'] == "FLAGGED":
        print("\n⚠ Process log has warnings. Director should review before accepting.")
    else:
        print("\n✗ Process log rejected. Agent must revise and resubmit.")


def interactive_validate():
    """Interactive validation - paste process log."""
    # Check if input is piped
    if not sys.stdin.isatty():
        # Read all piped input
        log_text = sys.stdin.read()
    else:
        print("Paste the process log below. Enter a blank line when done:")
        print("-" * 70)

        lines = []
        while True:
            try:
                line = input()
                if line == "":
                    # Check if we have content
                    if lines:
                        break
                lines.append(line)
            except EOFError:
                break

        log_text = "\n".join(lines)

    result = validate_process_log(log_text)
    print_validation_result(result)
    return result


def scene_setup(chapter: int):
    """Set up workflow for a scene."""
    print("=" * 70)
    print(f"SCENE SETUP: Chapter {chapter}")
    print("=" * 70)

    # Load chapter structure if exists
    structure_path = STORY_BIBLES_DIR / "book_2" / f"Chapter_{chapter}_STRUCTURE.md"
    if structure_path.exists():
        print(f"\n✓ Structure file found: {structure_path}")
    else:
        print(f"\n⚠ No structure file: {structure_path}")

    # Load timeline
    state_index = CHARACTERS_DIR / "CHARACTER_STATE_INDEX.yaml"
    if state_index.exists():
        with open(state_index) as f:
            state = yaml.safe_load(f)

        timeline = state.get("timeline", {})
        ch_key = f"ch{chapter}"
        if ch_key in timeline:
            ch_info = timeline[ch_key]
            print(f"\nTimeline: Month {ch_info.get('month')}, Event: {ch_info.get('event')}")

    print("\n" + "-" * 70)
    print("RECOMMENDED WORKFLOW:")
    print("-" * 70)
    print("""
1. PREPARATION
   - Archivist: "What do we have on Chapter {chapter}?"
   - Status Tracker: "What are character states at Chapter {chapter}?"
   - Timeline Keeper: "What's the temporal context?"

2. SCENE DEVELOPMENT
   - Set Designer: Define/verify location
   - Scene Choreographer: Block character positions
   - Character Steward(s): Develop character actions (EXPLORATION mode)

3. THEMATIC CHECK
   - Theme Guardian: "Does this serve the arc?"
   - Pacing Monitor: "Is the rhythm right?"

4. PROSE GENERATION
   - Character Steward(s): Generate prose (PERFORMANCE mode)
   - Reader Proxy: "What does reader know at this point?"

5. VALIDATION
   - All process logs validated
   - State changes confirmed by Director
   - Output accepted into manuscript
""".format(chapter=chapter))

    print("-" * 70)
    print("\nWhich agent do you want to start with?")
    print("Options: " + ", ".join(PRODUCTION_CREW[:6]))
    print("         " + ", ".join(PRODUCTION_CREW[6:]))
    print("         character_steward")


def list_agents():
    """List all available agents."""
    print("=" * 70)
    print("GO SQUAD AGENTS")
    print("=" * 70)

    print("\nPRODUCTION CREW (12):")
    for i, role in enumerate(PRODUCTION_CREW, 1):
        template_path = TEMPLATES_DIR / f"{role}.yaml"
        status = "✓" if template_path.exists() else "✗"
        print(f"  {i:2}. {status} {role}")

    print("\nPERFORMANCE CAST:")
    for role in PERFORMANCE_CAST:
        template_path = TEMPLATES_DIR / f"{role}.yaml"
        status = "✓" if template_path.exists() else "✗"
        print(f"      {status} {role}")

    print("\nUsage:")
    print("  python3 director_cli.py prompt <agent_name>")
    print("  python3 director_cli.py validate")
    print("  python3 director_cli.py scene <chapter_number>")


def interactive_mode():
    """Interactive CLI mode."""
    print("=" * 70)
    print("GO SQUAD DIRECTOR CLI")
    print("=" * 70)
    print("\nCommands:")
    print("  prompt <agent>  - Get agent prompt for copy-paste")
    print("  validate        - Validate a process log")
    print("  scene <chapter> - Set up scene workflow")
    print("  list            - List all agents")
    print("  quit            - Exit")
    print()

    while True:
        try:
            cmd = input("director> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not cmd:
            continue

        parts = cmd.split()
        command = parts[0].lower()

        if command == "quit" or command == "exit":
            break
        elif command == "list":
            list_agents()
        elif command == "prompt":
            if len(parts) < 2:
                print("Usage: prompt <agent_name>")
            else:
                agent = parts[1].lower()
                if agent in PRODUCTION_CREW or agent in PERFORMANCE_CAST:
                    print_prompt(agent)
                else:
                    print(f"Unknown agent: {agent}")
                    print(f"Available: {', '.join(PRODUCTION_CREW + PERFORMANCE_CAST)}")
        elif command == "validate":
            interactive_validate()
        elif command == "scene":
            if len(parts) < 2:
                print("Usage: scene <chapter_number>")
            else:
                try:
                    chapter = int(parts[1])
                    scene_setup(chapter)
                except ValueError:
                    print("Chapter must be a number")
        else:
            print(f"Unknown command: {command}")
            print("Commands: prompt, validate, scene, list, quit")


def main():
    parser = argparse.ArgumentParser(
        description="Go Squad Director CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 director_cli.py                     # Interactive mode
  python3 director_cli.py prompt status_tracker
  python3 director_cli.py validate
  python3 director_cli.py scene 5
  python3 director_cli.py list
        """
    )

    parser.add_argument("command", nargs="?", default="interactive",
                       help="Command: prompt, validate, scene, list")
    parser.add_argument("arg", nargs="?", help="Command argument")

    args = parser.parse_args()

    if args.command == "interactive":
        interactive_mode()
    elif args.command == "prompt":
        if not args.arg:
            print("Usage: director_cli.py prompt <agent_name>")
            sys.exit(1)
        agent = args.arg.lower()
        if agent in PRODUCTION_CREW or agent in PERFORMANCE_CAST:
            print_prompt(agent)
        else:
            print(f"Unknown agent: {agent}")
            print(f"Available: {', '.join(PRODUCTION_CREW + PERFORMANCE_CAST)}")
    elif args.command == "validate":
        interactive_validate()
    elif args.command == "scene":
        if not args.arg:
            print("Usage: director_cli.py scene <chapter_number>")
            sys.exit(1)
        try:
            chapter = int(args.arg)
            scene_setup(chapter)
        except ValueError:
            print("Chapter must be a number")
    elif args.command == "list":
        list_agents()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()
