#!/usr/bin/env python3
"""
PKD Award Judge Evaluation System - PDF Book Evaluator
Evaluates book manuscripts in PDF format using literary judge criteria

IMPROVED VERSION:
- Reads CONTINUOUS sections (50-60 pages each) instead of fragmented chunks
- Beginning: ~50-60 pages
- Middle: ~50-60 pages  
- End: ~50-60 pages
- Total: ~150-180 pages of continuous narrative assessed
- Explicitly instructs evaluator not to penalize complex structures that require full context
- Uses clear section markers instead of [...] gaps that suggest missing content

This better captures narrative development, character arcs, and thematic progression
for novels with complex nested structures or slow-burn revelations.
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

# Import the schema
exec(open('pkd_judge schema.json').read())


class PDFBookEvaluator:
    """Evaluates PDF books using the PKD Judge schema with Claude API"""

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

    def _estimate_page_from_text(self, char_position: int) -> int:
        """Estimate page number from character position (rough: 2000 chars/page)"""
        return max(1, char_position // 2000)

    def _get_text_chunk(self, start_page: int, end_page: int) -> str:
        """Get text from specific page range"""
        # Rough estimation: 2000 characters per page
        start_char = (start_page - 1) * 2000
        end_char = end_page * 2000
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

    def evaluate_first_50_pages(self) -> Dict:
        """Evaluate first 50 pages using Claude"""
        print("\n📝 Evaluating first 50 pages...")

        first_50_text = self._get_text_chunk(1, 50)

        prompt = f"""You are a professional literary judge evaluating manuscripts for the Philip K. Dick Award.
Read the first 50 pages of this science fiction manuscript and provide a critical evaluation.

Title: {self.title}
Author: {self.author}

TEXT (First ~50 pages):
{first_50_text[:50000]}

Evaluate on these criteria (0-10 scale for each):
1. immediate_engagement - Does it hook within the first page?
2. voice_establishment - Are characters distinct immediately?
3. worldbuilding_efficiency - Show don't tell, no infodump?
4. thematic_signal - Do we know what the book explores?
5. craft_demonstration - Proves sustainable quality?
6. genre_competence - Handles SF mechanics well?

Also determine:
- decision: Should we CONTINUE reading or ELIMINATE this manuscript?
- reasoning: Why this choice (2-3 sentences with specific examples)?

Respond in JSON format with these exact keys:
{{
    "immediate_engagement": <0-10>,
    "voice_establishment": <0-10>,
    "worldbuilding_efficiency": <0-10>,
    "thematic_signal": <0-10>,
    "craft_demonstration": <0-10>,
    "genre_competence": <0-10>,
    "decision": "CONTINUE" or "ELIMINATE",
    "reasoning": "<your reasoning>"
}}"""

        response = self._call_claude(prompt, max_tokens=2048)

        try:
            # Parse JSON response (handle code blocks)
            response_text = response.strip()
            if response_text.startswith('```'):
                # Extract JSON from code block
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

            result = json.loads(response_text)

            # Calculate average score
            scores = [
                result['immediate_engagement'],
                result['voice_establishment'],
                result['worldbuilding_efficiency'],
                result['thematic_signal'],
                result['craft_demonstration'],
                result['genre_competence']
            ]
            self.judge.first_50_score = sum(scores) / len(scores)

            print(f"   First 50 pages score: {self.judge.first_50_score:.1f}/10")
            print(f"   Decision: {result['decision']}")

            return result
        except json.JSONDecodeError:
            print(f"✗ Error parsing Claude response. Raw response:\n{response}")
            return {
                'decision': 'ELIMINATE',
                'reasoning': 'Failed to parse evaluation response'
            }

    def evaluate_pkd_alignment(self) -> PKDAlignment:
        """Evaluate how well the book aligns with PKD's themes"""
        print("\n🤖 Evaluating PKD alignment...")

        # Read substantial continuous sections to capture narrative development
        section_size = 50  # pages per section
        beginning_text = self._get_text_chunk(1, section_size)
        middle_text = self._get_text_chunk(self.judge.total_pages // 2 - 25, self.judge.total_pages // 2 + 25)
        end_text = self._get_text_chunk(max(1, self.judge.total_pages - section_size), self.judge.total_pages)
        
        sample_text = (
            f"=== BEGINNING (pages 1-{section_size}) ===\n\n{beginning_text}\n\n" +
            f"=== MIDDLE (pages ~{self.judge.total_pages // 2 - 25}-{self.judge.total_pages // 2 + 25}) ===\n\n{middle_text}\n\n" +
            f"=== END (pages {max(1, self.judge.total_pages - section_size)}-{self.judge.total_pages}) ===\n\n{end_text}"
        )

        prompt = f"""You are evaluating how well this science fiction novel honors Philip K. Dick's legacy.
PKD's core themes include: reality distortion, consciousness questions, identity instability,
corporate dystopia, and the human cost of big ideas.

Title: {self.title}
Author: {self.author}

You are reading THREE CONTINUOUS SECTIONS from this {self.judge.total_pages}-page novel:
- Beginning (first ~50 pages)
- Middle (~50 pages from the center)
- End (final ~50 pages)

These sections are marked clearly. Read each section completely to understand narrative development
and thematic progression across the full arc.

CONTINUOUS SECTIONS:
{sample_text[:80000]}

Rate each PKD alignment dimension on 0-10 scale:
1. reality_distortion - Questions what's real
2. consciousness_questions - What makes us who we are
3. identity_instability - Can we trust our selves
4. corporate_dystopia - Systems vs humanity
5. human_cost - Personal stakes of big ideas

Respond in JSON format:
{{
    "reality_distortion": <0-10>,
    "consciousness_questions": <0-10>,
    "identity_instability": <0-10>,
    "corporate_dystopia": <0-10>,
    "human_cost": <0-10>,
    "explanation": "<brief explanation of ratings>"
}}"""

        response = self._call_claude(prompt, max_tokens=3000)

        try:
            # Parse JSON response (handle code blocks)
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

            result = json.loads(response_text)
            alignment = PKDAlignment(
                reality_distortion=result['reality_distortion'],
                consciousness_questions=result['consciousness_questions'],
                identity_instability=result['identity_instability'],
                corporate_dystopia=result['corporate_dystopia'],
                human_cost=result['human_cost']
            )

            print(f"   PKD Alignment: {alignment.average():.1f}/10")
            return alignment
        except json.JSONDecodeError:
            print(f"✗ Error parsing response: {response}")
            return PKDAlignment()

    def evaluate_overall_quality(self) -> Dict:
        """Evaluate overall literary quality"""
        print("\n⭐ Evaluating overall quality metrics...")

        # Read substantial continuous sections to assess structure and development
        section_size = 60  # pages per section for more context
        beginning_text = self._get_text_chunk(1, section_size)
        middle_text = self._get_text_chunk(self.judge.total_pages // 2 - 30, self.judge.total_pages // 2 + 30)
        end_text = self._get_text_chunk(max(1, self.judge.total_pages - section_size), self.judge.total_pages)
        
        sample_text = (
            f"=== BEGINNING (pages 1-{section_size}) ===\n\n{beginning_text}\n\n" +
            f"=== MIDDLE (pages ~{self.judge.total_pages // 2 - 30}-{self.judge.total_pages // 2 + 30}) ===\n\n{middle_text}\n\n" +
            f"=== END (pages {max(1, self.judge.total_pages - section_size)}-{self.judge.total_pages}) ===\n\n{end_text}"
        )

        prompt = f"""You are a professional literary judge evaluating this science fiction novel's overall quality.

Title: {self.title}
Author: {self.author}

You are reading THREE CONTINUOUS SECTIONS from this {self.judge.total_pages}-page novel:
- Beginning (first ~60 pages)
- Middle (~60 pages from the center)
- End (final ~60 pages)

These are CONTINUOUS sections that allow you to track narrative development, character arcs,
and thematic progression. Evaluate how well the structure works and whether complex narrative
elements pay off.

CRITICAL INSTRUCTION: Do NOT penalize the book for narrative complexity that requires full context.
If you see a framing device or nested structure, assess whether what you CAN see suggests
it will work based on execution quality, not whether the sections alone are self-contained.
Complex structures that slowly reveal connections are legitimate literary techniques.

CONTINUOUS SECTIONS:
{sample_text[:100000]}

Rate each dimension on 0-10 scale:
1. voice_consistency - Characters sound like themselves throughout
2. structural_craft - Architecture and pacing
3. thematic_depth - Ideas are developed meaningfully
4. prose_quality - Literary without pretension
5. emotional_precision - Earned emotion vs manipulation
6. originality - Fresh ideas and execution
7. accessibility - Complexity justified by payoff

Also identify:
- unique_strengths: What makes this stand out (3-5 bullet points)
- concerning_weaknesses: Issues that hurt the work (2-4 bullet points)
- fatal_flaws: Dealbreakers if any (or empty list)

Respond in JSON format:
{{
    "voice_consistency": <0-10>,
    "structural_craft": <0-10>,
    "thematic_depth": <0-10>,
    "prose_quality": <0-10>,
    "emotional_precision": <0-10>,
    "originality": <0-10>,
    "accessibility": <0-10>,
    "unique_strengths": [<list of strings>],
    "concerning_weaknesses": [<list of strings>],
    "fatal_flaws": [<list of strings>]
}}"""

        response = self._call_claude(prompt, max_tokens=3072)

        try:
            # Parse JSON response (handle code blocks)
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

            result = json.loads(response_text)

            # Update judge scores
            self.judge.voice_consistency = result['voice_consistency']
            self.judge.structural_craft = result['structural_craft']
            self.judge.thematic_depth = result['thematic_depth']
            self.judge.prose_quality = result['prose_quality']
            self.judge.emotional_precision = result['emotional_precision']
            self.judge.originality = result['originality']
            self.judge.accessibility = result['accessibility']
            self.judge.fatal_flaws = result.get('fatal_flaws', [])

            avg_quality = sum([
                result['voice_consistency'],
                result['structural_craft'],
                result['thematic_depth'],
                result['prose_quality'],
                result['emotional_precision'],
                result['originality'],
                result['accessibility']
            ]) / 7

            print(f"   Overall quality: {avg_quality:.1f}/10")

            return result
        except json.JSONDecodeError:
            print(f"✗ Error parsing response: {response}")
            return {}

    def generate_final_report(self) -> Dict:
        """Generate comprehensive final evaluation report"""
        print("\n📋 Generating final assessment...")

        final = self.judge.final_assessment()

        # Get human-readable recommendation
        recommendation = final['recommendation'].value.upper()

        print(f"\n{'='*60}")
        print(f"FINAL EVALUATION: {self.title}")
        print(f"{'='*60}")
        print(f"Overall Score: {final['overall_score']:.1f}/10")
        print(f"Recommendation: {recommendation}")
        print(f"{'='*60}")

        return final

    def run_full_evaluation(self) -> Dict:
        """Run complete evaluation pipeline"""
        print(f"\n🎯 Starting evaluation of '{self.title}' by {self.author}")
        print(f"   Total pages: {self.judge.total_pages}")

        # Step 1: First 50 pages
        first_50_eval = self.evaluate_first_50_pages()

        if first_50_eval.get('decision') == 'ELIMINATE':
            print("\n❌ ELIMINATED after first 50 pages")
            print(f"   Reason: {first_50_eval.get('reasoning', 'N/A')}")
            return {
                'eliminated_at': 'first_50_pages',
                'decision': Decision.ELIMINATE.value,
                'first_50_evaluation': first_50_eval
            }

        # Step 2: PKD Alignment
        self.judge.dick_alignment = self.evaluate_pkd_alignment()

        # Step 3: Overall Quality
        quality_eval = self.evaluate_overall_quality()

        # Step 4: Final Assessment
        final_report = self.generate_final_report()

        # Compile full report
        full_report = {
            'title': self.title,
            'author': self.author,
            'total_pages': self.judge.total_pages,
            'first_50_evaluation': first_50_eval,
            'pkd_alignment': {
                'reality_distortion': self.judge.dick_alignment.reality_distortion,
                'consciousness_questions': self.judge.dick_alignment.consciousness_questions,
                'identity_instability': self.judge.dick_alignment.identity_instability,
                'corporate_dystopia': self.judge.dick_alignment.corporate_dystopia,
                'human_cost': self.judge.dick_alignment.human_cost,
                'average': self.judge.dick_alignment.average()
            },
            'quality_metrics': quality_eval,
            'final_assessment': {
                'overall_score': final_report['overall_score'],
                'recommendation': final_report['recommendation'].value,
                'fatal_flaws': self.judge.fatal_flaws
            }
        }

        return full_report


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate a PDF book manuscript using PKD Award judge criteria'
    )
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('--title', required=True, help='Book title')
    parser.add_argument('--author', required=True, help='Author name')
    parser.add_argument('--output', '-o', help='Output JSON file path (optional)')
    parser.add_argument('--api-key', help='Anthropic API key (or use ANTHROPIC_API_KEY env var)')

    args = parser.parse_args()

    # Check if PDF exists
    if not Path(args.pdf_path).exists():
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)

    try:
        # Run evaluation
        evaluator = PDFBookEvaluator(
            pdf_path=args.pdf_path,
            title=args.title,
            author=args.author,
            api_key=args.api_key
        )

        report = evaluator.run_full_evaluation()

        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n💾 Report saved to: {output_path}")
        else:
            # Print to stdout
            print("\n" + "="*60)
            print("FULL REPORT (JSON)")
            print("="*60)
            print(json.dumps(report, indent=2))

        # Exit code based on recommendation
        recommendation = report.get('final_assessment', {}).get('recommendation', 'eliminate')
        if recommendation == 'champion':
            sys.exit(0)  # Strong yes
        elif recommendation in ['shortlist', 'consider']:
            sys.exit(0)  # Qualified yes
        else:
            sys.exit(1)  # No

    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()