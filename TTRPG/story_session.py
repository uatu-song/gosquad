#!/usr/bin/env python3
"""
Non-Interactive Story Session Runner
Allows running story sessions through Claude Code without interactive terminal
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from core.narrative_engine import NarrativeEngine


def print_divider(char="=", width=70):
    print(f"\n{char*width}\n")


def print_section_header(title, width=70):
    print(f"\n{'─'*width}")
    print(f"  {title}")
    print(f"{'─'*width}\n")


class StorySession:
    """Non-interactive story session manager"""

    def __init__(self, campaign_file: str = "default_campaign.json"):
        self.engine = NarrativeEngine(campaign_file)
        self.campaign_file = campaign_file

    def run_prompt(self, prompt: str) -> str:
        """Process a single story prompt and return formatted output"""
        output = []

        output.append("="*70)
        output.append("GENERATING SCENE")
        output.append("="*70)
        output.append(f"\nProcessing: \"{prompt}\"\n")

        try:
            # Generate scene from prompt
            response = self.engine.process_prompt(prompt)

            # Show narration
            output.append(response['narration'])

            # Show suggested checks
            if response['checks']:
                output.append("\n" + "─"*70)
                output.append("\n**Actions to resolve:**")
                for i, check in enumerate(response['checks'], 1):
                    char_name = self.engine.story_gen._get_character_context(check['character'])['name']
                    output.append(f"  {i}. {char_name} must make a {check['skill']} check ({check['difficulty']})")

                output.append("\n" + "─"*70)
                output.append("\n**Executing checks automatically...**\n")

                # Execute checks automatically
                results = self.engine.execute_checks(response['scene'])

                for result in results:
                    output.append(result['narration'])
                    output.append("\n" + "─"*70)

                # Show suggestions
                output.append("\n**Story continues...**")
                suggestions = self.engine.get_continuation_suggestions()
                output.append("\nIdeas for what to do next:")
                for i, sug in enumerate(suggestions[:3], 1):
                    output.append(f"  {i}. {sug}")
            else:
                # Pure narrative scene
                output.append("\n" + "─"*70)
                output.append("\n**This is a narrative scene. The story unfolds without mechanical resolution.**")
                output.append("\nIdeas for what to do next:")
                suggestions = self.engine.get_continuation_suggestions()
                for i, sug in enumerate(suggestions[:3], 1):
                    output.append(f"  {i}. {sug}")

        except Exception as e:
            output.append(f"\n✗ Error: {e}")
            output.append("Try rephrasing your prompt.")

        output.append("\n" + "="*70)
        return "\n".join(output)

    def get_status(self, character_id: str = None) -> str:
        """Get character or campaign status"""
        output = []

        if character_id:
            output.append("="*70)
            output.append(f"CHARACTER STATUS: {character_id.upper()}")
            output.append("="*70)

            status = self.engine.get_character_status(character_id)
            if 'error' in status:
                output.append(f"\nError: {status['error']}")
            else:
                output.append(f"\nHealth: {status['health']}")
                output.append(f"Stamina: {status['stamina']}")
                if 'temporal' in status:
                    output.append(f"\nTemporal Resources:")
                    output.append(f"  TC: {status['temporal']['tc']}/100")
                    output.append(f"  TS: {status['temporal']['ts']}/100")
                    output.append(f"  TIP: {status['temporal']['tip']}/100")
        else:
            output.append("="*70)
            output.append("CAMPAIGN STATUS")
            output.append("="*70)
            output.append(f"\n{self.engine.get_campaign_status()}")

            output.append(f"\nPending consequences:")
            applicable = self.engine.campaign.consequences.get_applicable(
                self.engine.campaign.timeline.current_month
            )
            if applicable:
                for i, cons in enumerate(applicable[:5], 1):
                    output.append(f"  {i}. {cons['description']}")
            else:
                output.append("  None")

        output.append("\n" + "="*70)
        return "\n".join(output)

    def get_context(self) -> str:
        """Get current story context"""
        output = []
        output.append("="*70)
        output.append("CURRENT CONTEXT")
        output.append("="*70)

        ctx = self.engine.context
        chars = ', '.join(ctx['characters_present']) if ctx['characters_present'] else 'None'
        output.append(f"\nCharacters present: {chars}")
        output.append(f"Location: {ctx['location'] or 'Unknown'}")
        output.append(f"Tension level: {ctx['tension_level']}")
        output.append(f"\nRecent events:")
        for event in ctx['recent_events'][-5:]:
            output.append(f"  - {event}")

        output.append("\n" + "="*70)
        return "\n".join(output)

    def advance_month(self) -> str:
        """Advance campaign timeline"""
        new_month = self.engine.advance_month()
        output = []
        output.append(f"\n✓ Advanced to Month {new_month}")
        output.append(self.engine.get_campaign_status())
        return "\n".join(output)

    def save(self, filename: str = None) -> str:
        """Save session"""
        saved_path = self.engine.save_session(filename)
        if filename:
            return f"✓ Session saved to {saved_path}\n✓ Campaign state auto-saved"
        else:
            return f"✓ Campaign state saved to {saved_path}"

    def get_suggestions(self) -> str:
        """Get continuation suggestions"""
        output = []
        output.append("="*70)
        output.append("WHAT HAPPENS NEXT?")
        output.append("="*70)

        suggestions = self.engine.get_continuation_suggestions()
        for i, sug in enumerate(suggestions, 1):
            output.append(f"  {i}. {sug}")
        output.append("\nOr describe your own action!")

        output.append("\n" + "="*70)
        return "\n".join(output)


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Story Session Runner")
    parser.add_argument('--campaign', '-c', default='default_campaign.json',
                       help='Campaign file to use')
    parser.add_argument('--prompt', '-p', help='Story prompt to process')
    parser.add_argument('--status', '-s', nargs='?', const='',
                       help='Show status (optionally for specific character)')
    parser.add_argument('--context', action='store_true',
                       help='Show current context')
    parser.add_argument('--advance', action='store_true',
                       help='Advance to next month')
    parser.add_argument('--save', nargs='?', const='',
                       help='Save session (optionally to specific file)')
    parser.add_argument('--suggestions', action='store_true',
                       help='Get story suggestions')

    args = parser.parse_args()

    # Initialize session
    session = StorySession(args.campaign)

    # Process command
    if args.prompt:
        print(session.run_prompt(args.prompt))
    elif args.status is not None:
        print(session.get_status(args.status if args.status else None))
    elif args.context:
        print(session.get_context())
    elif args.advance:
        print(session.advance_month())
    elif args.save is not None:
        print(session.save(args.save if args.save else None))
    elif args.suggestions:
        print(session.get_suggestions())
    else:
        # Show help if no command given
        print("="*70)
        print("STORY SESSION - Available Commands")
        print("="*70)
        print("\nUsage:")
        print("  python3 story_session.py --prompt 'Your story prompt'")
        print("  python3 story_session.py --status [character_id]")
        print("  python3 story_session.py --context")
        print("  python3 story_session.py --advance")
        print("  python3 story_session.py --save [filename]")
        print("  python3 story_session.py --suggestions")
        print("\nOptions:")
        print("  --campaign, -c  Specify campaign file (default: default_campaign.json)")
        print("\nExamples:")
        print("  python3 story_session.py -p 'Ahdia meets Ahdia-Prime'")
        print("  python3 story_session.py --status ahdia_bacchus")
        print("  python3 story_session.py --campaign my_campaign.json -p 'Combat breaks out'")
        print("="*70)


if __name__ == '__main__':
    main()
