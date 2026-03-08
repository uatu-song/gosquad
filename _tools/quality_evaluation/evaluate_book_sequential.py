#!/usr/bin/env python3
"""
PKD Award Judge Evaluation System - Sequential Reading with Memory

METHODOLOGY:
- Divides book into sequential sections (~70 pages each)
- Evaluates each section in order, building understanding progressively
- Carries forward context from previous sections (like real reading)
- Final synthesis considers the complete narrative arc
- Actually reads the ENTIRE manuscript

This approach mirrors how real judges read: sequentially, forming impressions
as the narrative develops, tracking how themes deepen and plot threads converge.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import PyPDF2
from dataclasses import asdict
import anthropic
import os
import time

# Import the schema
exec(open('pkd_judge schema.json').read())


class SequentialBookEvaluator:
    """Evaluates PDF books by reading sequentially with memory"""

    def __init__(self, pdf_path: str, title: str, author: str, api_key: Optional[str] = None):
        self.pdf_path = pdf_path
        self.title = title
        self.author = author
        self.judge = PKDJudgeEvaluation(pdf_path, title, author)

        # Initialize Anthropic client
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or provided")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"

        # Extract text from PDF
        self.full_text = self._extract_pdf_text()
        self.judge.total_pages = self._count_pages()

        # Track reading progress
        self.section_evaluations = []
        self.reading_memory = []

    def _extract_pdf_text(self) -> str:
        """Extract all text from PDF"""
        print(f"📖 Extracting text from {self.pdf_path}...")
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = []
                for page_num, page in enumerate(reader.pages):
                    text.append(page.extract_text())
                    if (page_num + 1) % 10 == 0:
                        print(f"   Extracted {page_num + 1} pages...")

                full_text = '\n\n'.join(text)
                print(f"✓ Extracted {len(reader.pages)} pages, {len(full_text)} characters")
                return full_text
        except Exception as e:
            print(f"✗ Error extracting PDF: {e}")
            raise

    def _count_pages(self) -> int:
        """Count total pages in PDF"""
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return len(reader.pages)

    def _get_text_chunk(self, start_page: int, end_page: int) -> str:
        """Get text from specific page range"""
        # Rough estimation: 1500 characters per page
        start_char = (start_page - 1) * 1500
        end_char = min(end_page * 1500, len(self.full_text))
        return self.full_text[start_char:end_char]

    def _call_claude(self, prompt: str, max_tokens: int = 4096) -> str:
        """Call Claude API with given prompt"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"✗ Error calling Claude API: {e}")
            return f"ERROR: {str(e)}"

    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from Claude response, handling code blocks"""
        response_text = response.strip()
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            json_lines = []
            in_json = False
            for line in lines:
                if line.strip().startswith('```'):
                    if in_json:
                        break
                    in_json = True
                    continue
                if in_json:
                    json_lines.append(line)
            response_text = '\n'.join(json_lines)

        return json.loads(response_text)

    def _create_sections(self, pages_per_section: int = 70) -> List[Dict]:
        """Divide book into sequential sections"""
        sections = []
        current_page = 1
        section_num = 1

        while current_page <= self.judge.total_pages:
            end_page = min(current_page + pages_per_section - 1, self.judge.total_pages)
            sections.append({
                'number': section_num,
                'start_page': current_page,
                'end_page': end_page,
                'text': self._get_text_chunk(current_page, end_page)
            })
            current_page = end_page + 1
            section_num += 1

        return sections

    def evaluate_section(self, section: Dict, previous_memory: List[str]) -> Dict:
        """Evaluate a section with memory from previous sections"""
        section_num = section['number']
        start_page = section['start_page']
        end_page = section['end_page']
        text = section['text']

        print(f"\n📖 Reading Section {section_num}: Pages {start_page}-{end_page}")

        # Build context from previous sections
        context = ""
        if previous_memory:
            context = "MEMORY FROM PREVIOUS SECTIONS:\n\n"
            for i, memory in enumerate(previous_memory, 1):
                context += f"Section {i} Summary:\n{memory}\n\n"
            context += "=" * 60 + "\n\n"

        prompt = f"""You are a professional literary judge reading this science fiction manuscript sequentially.

Title: {self.title}
Author: {self.author}
Total pages: {self.judge.total_pages}

{context}NOW READING: Section {section_num} (Pages {start_page}-{end_page})

TEXT:
{text}

As you read this section, evaluate:

1. NARRATIVE DEVELOPMENT
   - What happens in this section?
   - How do characters develop or reveal themselves?
   - What thematic ideas emerge or deepen?

2. CRAFT ASSESSMENT (0-10 scale)
   - prose_quality: Is the writing strong and consistent?
   - character_work: Are characters compelling and authentic?
   - pacing: Does the narrative maintain momentum?
   - thematic_depth: Are ideas explored meaningfully?

3. PKD ALIGNMENT (0-10 scale)
   - reality_questions: Questions about what's real
   - consciousness_themes: Explores identity and awareness
   - human_cost: Personal stakes of big ideas
   - corporate_dystopia: Systems vs humanity

4. STRUCTURAL OBSERVATIONS
   - How does this section connect to previous sections (if any)?
   - What narrative threads are developing?
   - What mysteries or questions are raised or answered?

5. JUDGE'S REACTION
   - Are you engaged? Curious? Bored?
   - What works particularly well?
   - What concerns you?

Respond in JSON format:
{{
    "narrative_summary": "<concise summary of what happens>",
    "character_development": "<key character moments>",
    "thematic_work": "<themes explored in this section>",
    "prose_quality": <0-10>,
    "character_work": <0-10>,
    "pacing": <0-10>,
    "thematic_depth": <0-10>,
    "reality_questions": <0-10>,
    "consciousness_themes": <0-10>,
    "human_cost": <0-10>,
    "corporate_dystopia": <0-10>,
    "structural_connections": "<how this connects to previous sections>",
    "strengths": ["<list of what works well>"],
    "concerns": ["<list of issues or weaknesses>"],
    "engagement_level": "<HOOKED|ENGAGED|INTERESTED|NEUTRAL|STRUGGLING>",
    "notable_moments": ["<specific lines or scenes that stand out>"]
}}"""

        response = self._call_claude(prompt, max_tokens=4096)

        try:
            result = self._parse_json_response(response)
            print(f"   Engagement: {result.get('engagement_level', 'N/A')}")
            print(f"   Prose: {result.get('prose_quality', 0):.1f}/10")
            print(f"   Character: {result.get('character_work', 0):.1f}/10")
            return result
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing response: {e}")
            print(f"Raw response: {response[:500]}")
            return {}

    def synthesize_final_evaluation(self, section_evals: List[Dict]) -> Dict:
        """Create final evaluation from all section evaluations"""
        print("\n📋 Synthesizing final evaluation from complete reading...")

        # Compile section summaries
        sections_summary = ""
        for i, eval_data in enumerate(section_evals, 1):
            sections_summary += f"\nSection {i}:\n"
            sections_summary += f"  Narrative: {eval_data.get('narrative_summary', 'N/A')}\n"
            sections_summary += f"  Engagement: {eval_data.get('engagement_level', 'N/A')}\n"
            sections_summary += f"  Strengths: {', '.join(eval_data.get('strengths', [])[:2])}\n"
            sections_summary += f"  Concerns: {', '.join(eval_data.get('concerns', [])[:2])}\n"

        prompt = f"""You are a professional literary judge completing your evaluation of this science fiction novel.

Title: {self.title}
Author: {self.author}
Total pages: {self.judge.total_pages}

You have now read the ENTIRE manuscript sequentially in {len(section_evals)} sections.
Here is your reading journey:

{sections_summary}

Based on your complete reading, provide a final assessment:

1. OVERALL QUALITY METRICS (0-10 scale)
   - voice_consistency: Do characters maintain authentic voices?
   - structural_craft: Does the architecture work?
   - thematic_depth: Are ideas developed meaningfully?
   - prose_quality: Is the writing consistently strong?
   - emotional_precision: Earned emotion vs manipulation?
   - originality: Fresh ideas and execution?
   - accessibility: Is complexity justified by payoff?

2. PKD AWARD ALIGNMENT (0-10 scale)
   - reality_distortion: Questions what's real
   - consciousness_questions: What makes us who we are
   - identity_instability: Can we trust ourselves
   - corporate_dystopia: Systems vs humanity
   - human_cost: Personal stakes of big ideas

3. CRITICAL ASSESSMENT
   - unique_strengths: What makes this stand out (3-5 points)
   - concerning_weaknesses: What hurts the work (2-4 points)
   - fatal_flaws: Dealbreakers if any (empty list if none)

4. RECOMMENDATION
   - decision: "CHAMPION" | "SHORTLIST" | "CONSIDER" | "ELIMINATE"
   - reasoning: Why this decision (2-3 sentences)

5. NARRATIVE ARC ASSESSMENT
   - Did the opening promise pay off?
   - Did complex structures work?
   - How did your engagement change from beginning to end?

Respond in JSON format:
{{
    "voice_consistency": <0-10>,
    "structural_craft": <0-10>,
    "thematic_depth": <0-10>,
    "prose_quality": <0-10>,
    "emotional_precision": <0-10>,
    "originality": <0-10>,
    "accessibility": <0-10>,
    "reality_distortion": <0-10>,
    "consciousness_questions": <0-10>,
    "identity_instability": <0-10>,
    "corporate_dystopia": <0-10>,
    "human_cost": <0-10>,
    "unique_strengths": ["<list>"],
    "concerning_weaknesses": ["<list>"],
    "fatal_flaws": ["<list>"],
    "decision": "<CHAMPION|SHORTLIST|CONSIDER|ELIMINATE>",
    "reasoning": "<explanation>",
    "narrative_arc_assessment": "<how the complete story worked>"
}}"""

        response = self._call_claude(prompt, max_tokens=4096)

        try:
            result = self._parse_json_response(response)

            # Update judge with final scores
            self.judge.voice_consistency = result.get('voice_consistency', 0)
            self.judge.structural_craft = result.get('structural_craft', 0)
            self.judge.thematic_depth = result.get('thematic_depth', 0)
            self.judge.prose_quality = result.get('prose_quality', 0)
            self.judge.emotional_precision = result.get('emotional_precision', 0)
            self.judge.originality = result.get('originality', 0)
            self.judge.accessibility = result.get('accessibility', 0)

            self.judge.dick_alignment = PKDAlignment(
                reality_distortion=result.get('reality_distortion', 0),
                consciousness_questions=result.get('consciousness_questions', 0),
                identity_instability=result.get('identity_instability', 0),
                corporate_dystopia=result.get('corporate_dystopia', 0),
                human_cost=result.get('human_cost', 0)
            )

            self.judge.fatal_flaws = result.get('fatal_flaws', [])

            return result
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing final synthesis: {e}")
            return {}

    def run_full_evaluation(self, pages_per_section: int = 70) -> Dict:
        """Run complete sequential evaluation"""
        print(f"\n🎯 Starting sequential evaluation of '{self.title}' by {self.author}")
        print(f"   Total pages: {self.judge.total_pages}")

        # Divide into sections
        sections = self._create_sections(pages_per_section)
        print(f"   Reading in {len(sections)} sections (~{pages_per_section} pages each)")

        # Read each section sequentially
        for i, section in enumerate(sections):
            eval_result = self.evaluate_section(section, self.reading_memory)
            self.section_evaluations.append(eval_result)

            # Add to memory for next section
            memory_entry = f"{eval_result.get('narrative_summary', '')}\n" \
                          f"Themes: {eval_result.get('thematic_work', '')}\n" \
                          f"Engagement: {eval_result.get('engagement_level', '')}"
            self.reading_memory.append(memory_entry)

            # Rate limiting: wait 60 seconds between sections (except after last section)
            if i < len(sections) - 1:
                print(f"   Waiting 60 seconds to respect API rate limits...")
                time.sleep(60)

        # Synthesize final evaluation
        final_eval = self.synthesize_final_evaluation(self.section_evaluations)

        # Calculate overall score
        quality_scores = [
            final_eval.get('voice_consistency', 0),
            final_eval.get('structural_craft', 0),
            final_eval.get('thematic_depth', 0),
            final_eval.get('prose_quality', 0),
            final_eval.get('emotional_precision', 0),
            final_eval.get('originality', 0),
            final_eval.get('accessibility', 0),
            self.judge.dick_alignment.average()
        ]
        overall_score = sum(quality_scores) / len(quality_scores)

        print(f"\n{'='*60}")
        print(f"FINAL EVALUATION: {self.title}")
        print(f"{'='*60}")
        print(f"Overall Score: {overall_score:.1f}/10")
        print(f"PKD Alignment: {self.judge.dick_alignment.average():.1f}/10")
        print(f"Recommendation: {final_eval.get('decision', 'N/A')}")
        print(f"{'='*60}")

        # Compile full report
        full_report = {
            'title': self.title,
            'author': self.author,
            'total_pages': self.judge.total_pages,
            'sections_read': len(sections),
            'section_evaluations': self.section_evaluations,
            'final_assessment': {
                'overall_score': overall_score,
                'quality_metrics': {
                    'voice_consistency': final_eval.get('voice_consistency', 0),
                    'structural_craft': final_eval.get('structural_craft', 0),
                    'thematic_depth': final_eval.get('thematic_depth', 0),
                    'prose_quality': final_eval.get('prose_quality', 0),
                    'emotional_precision': final_eval.get('emotional_precision', 0),
                    'originality': final_eval.get('originality', 0),
                    'accessibility': final_eval.get('accessibility', 0)
                },
                'pkd_alignment': {
                    'reality_distortion': self.judge.dick_alignment.reality_distortion,
                    'consciousness_questions': self.judge.dick_alignment.consciousness_questions,
                    'identity_instability': self.judge.dick_alignment.identity_instability,
                    'corporate_dystopia': self.judge.dick_alignment.corporate_dystopia,
                    'human_cost': self.judge.dick_alignment.human_cost,
                    'average': self.judge.dick_alignment.average()
                },
                'unique_strengths': final_eval.get('unique_strengths', []),
                'concerning_weaknesses': final_eval.get('concerning_weaknesses', []),
                'fatal_flaws': final_eval.get('fatal_flaws', []),
                'recommendation': final_eval.get('decision', 'N/A'),
                'reasoning': final_eval.get('reasoning', ''),
                'narrative_arc_assessment': final_eval.get('narrative_arc_assessment', '')
            }
        }

        return full_report


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate a PDF book manuscript using sequential reading with memory'
    )
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('--title', required=True, help='Book title')
    parser.add_argument('--author', required=True, help='Author name')
    parser.add_argument('--output', '-o', help='Output JSON file path (optional)')
    parser.add_argument('--api-key', help='Anthropic API key (or use ANTHROPIC_API_KEY env var)')
    parser.add_argument('--pages-per-section', type=int, default=70,
                       help='Pages per section (default: 70)')

    args = parser.parse_args()

    # Check if PDF exists
    if not Path(args.pdf_path).exists():
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)

    try:
        # Run evaluation
        evaluator = SequentialBookEvaluator(
            pdf_path=args.pdf_path,
            title=args.title,
            author=args.author,
            api_key=args.api_key
        )

        report = evaluator.run_full_evaluation(pages_per_section=args.pages_per_section)

        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n💾 Report saved to: {output_path}")
        else:
            # Print summary
            print("\n" + "="*60)
            print("EVALUATION SUMMARY")
            print("="*60)
            print(json.dumps(report['final_assessment'], indent=2))

        # Exit code based on recommendation
        recommendation = report.get('final_assessment', {}).get('recommendation', 'ELIMINATE')
        if recommendation == 'CHAMPION':
            sys.exit(0)
        elif recommendation in ['SHORTLIST', 'CONSIDER']:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
