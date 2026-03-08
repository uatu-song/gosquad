#!/usr/bin/env python3
"""
Generate Perspective Engine Visualization
==========================================
Generates a standalone HTML visualization from CHARACTER_STATE_INDEX.yaml
and TIMELINE_DATA.js.

Usage:
    python generate_visualization.py
    python generate_visualization.py --output ../book2_perspective.html
"""

import json
import re
from pathlib import Path
from engine import PerspectiveEngine


def generate_html(engine: PerspectiveEngine, template_path: Path) -> str:
    """Generate HTML with injected data from engine"""

    # Read template
    with open(template_path, 'r') as f:
        template = f.read()

    # Build character config from actual data
    character_config = {}
    icons = {
        'ahdia': '⚡', 'ruth': '💚', 'tess': '🌑', 'ben': '🛡️',
        'leah': '⚔️', 'leta': '📡', 'victor': '🔗', 'korede': '👁️',
        'ryu': '💉', 'eidolon': '😱', 'kain': '🏛️', 'bellatrix': '🎭'
    }
    colors = {
        'ahdia': '#58a6ff', 'ruth': '#f0883e', 'tess': '#a371f7',
        'ben': '#3fb950', 'leah': '#f778ba', 'leta': '#ffd33d',
        'victor': '#79c0ff', 'korede': '#56d4dd', 'ryu': '#8b949e',
        'eidolon': '#f85149', 'kain': '#da3633', 'bellatrix': '#d2a8ff'
    }
    groups = {
        'ahdia': 'protagonist', 'ruth': 'protagonist', 'tess': 'protagonist',
        'ben': 'protagonist', 'leah': 'protagonist', 'leta': 'protagonist',
        'victor': 'protagonist', 'korede': 'protagonist', 'ryu': 'supporting',
        'eidolon': 'antagonist', 'kain': 'antagonist', 'bellatrix': 'antagonist'
    }

    for char_id, char_data in engine.characters.items():
        meta = char_data.get('meta', {})
        full_name = meta.get('full_name', char_id.title())

        character_config[char_id] = {
            'name': full_name,
            'icon': icons.get(char_id, '●'),
            'color': colors.get(char_id, '#8b949e'),
            'group': groups.get(char_id, 'supporting')
        }

    # Build timeline from engine data
    timeline_data = {}
    for ch_key, ch_data in engine.timeline.items():
        ch_num = int(ch_key.replace('ch', ''))
        event_name = ch_data.get('event', '').replace('_', ' ').title()
        timeline_data[ch_num] = {
            'month': ch_data.get('month', 1),
            'event': event_name,
            'type': 'action'  # Default, could be enhanced
        }

    # Build character events from chapter_states and threads
    character_events = {}
    for char_id, char_data in engine.characters.items():
        events = []

        # Get from chapter_states
        chapter_states = char_data.get('chapter_states', {})
        for ch_key, state in chapter_states.items():
            ch_num = int(ch_key.replace('ch', ''))
            actions = state.get('key_actions', [])
            emotional = state.get('emotional', '')

            text = ', '.join(actions[:2]) if actions else emotional
            event_type = 'action' if actions else 'emotional'

            # Check for revelations
            learns = state.get('learns', [])
            if learns:
                event_type = 'revelation'
                if not text:
                    text = f"Learns: {learns[0]}"

            if text:
                events.append({
                    'ch': ch_num,
                    'type': event_type,
                    'text': text
                })

        # Fill gaps from threads
        threads = char_data.get('threads', {})
        existing_chapters = {e['ch'] for e in events}

        for thread_name, thread_data in threads.items():
            gates = thread_data.get('gates', {})
            for ch_key, gate in gates.items():
                ch_num = int(ch_key.replace('ch', ''))
                if ch_num not in existing_chapters:
                    state_desc = gate.get('state', '')
                    trigger = gate.get('trigger', '')
                    text = trigger if trigger else state_desc
                    if text:
                        text = text.replace('_', ' ')
                        events.append({
                            'ch': ch_num,
                            'type': 'action',
                            'text': text
                        })
                        existing_chapters.add(ch_num)

        # Sort by chapter
        events.sort(key=lambda e: e['ch'])
        character_events[char_id] = events

    # Build secrets from knowledge_tracking
    secrets_data = {}
    for secret_id, secret_data in engine.knowledge_tracking.items():
        aware_by_chapter = {}
        for ch_key, knowers in secret_data.get('awareness', {}).items():
            ch_num = int(ch_key.replace('ch', ''))
            aware_by_chapter[ch_num] = knowers

        secrets_data[secret_id] = {
            'name': secret_data.get('description', secret_id.replace('_', ' ').title()),
            'holder': secret_data.get('secret_holder', ''),
            'reveal_ch': secret_data.get('reveal_chapter'),
            'aware': aware_by_chapter
        }

    # Build overlaps
    overlaps_data = []
    for overlap in engine._overlaps:
        overlaps_data.append({
            'ch': overlap.chapter,
            'title': overlap.title,
            'chars': overlap.characters,
            'type': overlap.overlap_type
        })

    # Generate JavaScript data block
    js_data = f"""
// ═══════════════════════════════════════
// AUTO-GENERATED DATA FROM CHARACTER_STATE_INDEX.yaml
// Generated by generate_visualization.py
// ═══════════════════════════════════════

const CHARACTERS = {json.dumps(character_config, indent=4)};

const TIMELINE = {json.dumps(timeline_data, indent=4)};

const CHARACTER_EVENTS = {json.dumps(character_events, indent=4)};

const SECRETS = {json.dumps(secrets_data, indent=4)};

const OVERLAPS = {json.dumps(overlaps_data, indent=4)};
"""

    # Find and replace the data section in template
    # Look for the data section marker
    start_marker = '// ═══════════════════════════════════════\n// DATA'
    end_marker = 'const OVERLAPS = ['

    start_idx = template.find(start_marker)
    if start_idx == -1:
        raise ValueError("Could not find DATA section start marker in template")

    # Find end of OVERLAPS array
    end_idx = template.find(end_marker, start_idx)
    if end_idx == -1:
        raise ValueError("Could not find OVERLAPS marker in template")

    # Find the closing of OVERLAPS array
    bracket_count = 0
    i = end_idx + len(end_marker)
    while i < len(template):
        if template[i] == '[':
            bracket_count += 1
        elif template[i] == ']':
            if bracket_count == 0:
                end_idx = i + 2  # Include ]; and newline
                break
            bracket_count -= 1
        i += 1

    # Replace the section
    template = template[:start_idx] + js_data.strip() + template[end_idx:]

    return template


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate Perspective Engine visualization')
    parser.add_argument('--output', '-o', default=None,
                        help='Output HTML file path')

    args = parser.parse_args()

    # Load engine
    engine = PerspectiveEngine().load()

    # Get paths
    script_dir = Path(__file__).parent
    template_path = script_dir / 'visualization.html'

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = engine.repo_root / 'book2_perspective_engine.html'

    # Generate
    html = generate_html(engine, template_path)

    # Write output
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✅ Generated: {output_path}")
    print(f"   Characters: {len(engine.characters)}")
    print(f"   Chapters: 24")
    print(f"   Overlaps: {len(engine._overlaps)}")
    print(f"   Secrets tracked: {len(engine.knowledge_tracking)}")


if __name__ == '__main__':
    main()
