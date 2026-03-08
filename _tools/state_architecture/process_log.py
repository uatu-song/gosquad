#!/usr/bin/env python3
"""
Go Squad Process Log System

Process logs are the audit trail for all agent operations.
They enforce lane discipline and enable validation.

Usage:
    from process_log import ProcessLog, ProcessLogEntry

    # Create a process log for an operation
    log = ProcessLog(
        agent_role="status_tracker",
        task_id="check_ahdia_knowledge_ch13"
    )

    # Log queries made
    log.add_query(
        query="get_character_state('ahdia', 13)",
        target="archivist",
        response_summary="Retrieved chapter 13 state"
    )

    # Declare domain
    log.declare_domain(
        task_description="Verify Ahdia's knowledge state at chapter 13",
        justification="Knowledge tracking is Status Tracker's domain"
    )

    # Add source attribution
    log.add_source(
        claim="Ahdia knows about exile_island at chapter 13",
        source_file="7_characters/arcs/CHARACTER_STATE_INDEX.yaml",
        source_section="knowledge_tracking.exile_island.awareness.ch13"
    )

    # Set output
    log.set_output(
        content={"knows_exile_island": True},
        confidence="high"
    )

    # Validate and get result
    result = log.validate()
"""

import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Literal
from enum import Enum


class AgentRole(Enum):
    """Valid Go Squad agent roles."""
    ARCHIVIST = "archivist"
    STATUS_TRACKER = "status_tracker"
    THEME_GUARDIAN = "theme_guardian"
    TIMELINE_KEEPER = "timeline_keeper"
    SCENE_CHOREOGRAPHER = "scene_choreographer"
    READER_PROXY = "reader_proxy"
    PACING_MONITOR = "pacing_monitor"
    TECHNICAL_CONSULTANT = "technical_consultant"
    INTIMACY_COORDINATOR = "intimacy_coordinator"
    OUTLINE_ASSISTANT = "outline_assistant"
    PRODUCTION_DESIGNER = "production_designer"
    CHARACTER_STEWARD = "character_steward"


class AgentMode(Enum):
    """Character Steward modes."""
    EXPLORATION = "exploration"
    PERFORMANCE = "performance"
    NOT_APPLICABLE = "n/a"


class ValidationStatus(Enum):
    """Process log validation outcomes."""
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"


@dataclass
class QueryEntry:
    """A single query made during the operation."""
    query: str
    target_agent: str
    response_summary: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SourceAttribution:
    """Source attribution for a claim."""
    claim: str
    source_file: str
    source_section: Optional[str] = None
    source_line: Optional[int] = None


@dataclass
class DeferralEntry:
    """Item deferred to another specialist."""
    item: str
    deferred_to: str
    reason: str


@dataclass
class StateChangeProposal:
    """Proposed state change requiring confirmation."""
    state_type: str
    entity_id: str
    change: str
    requires_confirmation: bool = True


@dataclass
class ValidationResult:
    """Result of process log validation."""
    status: ValidationStatus
    issues: List[str]
    warnings: List[str]

    def __str__(self):
        result = f"Status: {self.status.value.upper()}"
        if self.issues:
            result += f"\nIssues ({len(self.issues)}):"
            for issue in self.issues:
                result += f"\n  - {issue}"
        if self.warnings:
            result += f"\nWarnings ({len(self.warnings)}):"
            for warning in self.warnings:
                result += f"\n  - {warning}"
        return result


class ProcessLog:
    """
    Process log for a single agent operation.

    Every agent output must include a process log for validation.
    The log captures: queries made, domain declaration, sources,
    deferrals, mode (for Character Stewards), and the output itself.
    """

    def __init__(
        self,
        agent_role: str,
        task_id: str,
        mode: Optional[str] = None
    ):
        """
        Initialize a process log.

        Args:
            agent_role: The agent's role (from AgentRole enum)
            task_id: Unique identifier for this operation
            mode: For Character Stewards only - 'exploration' or 'performance'
        """
        self.meta = {
            "agent_role": agent_role,
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "mode": mode if agent_role == "character_steward" else "n/a"
        }

        self.query_log: List[QueryEntry] = []
        self.domain_declaration: Optional[Dict[str, Any]] = None
        self.source_attributions: List[SourceAttribution] = []
        self.deferred_items: List[DeferralEntry] = []
        self.state_changes_proposed: List[StateChangeProposal] = []
        self.output: Optional[Dict[str, Any]] = None

    def add_query(
        self,
        query: str,
        target: str,
        response_summary: str
    ) -> None:
        """
        Log a query made to another agent or data source.

        Args:
            query: The query made (e.g., "get_character_state('ahdia', 13)")
            target: Who was queried (e.g., "archivist", "status_tracker")
            response_summary: Brief summary of response
        """
        self.query_log.append(QueryEntry(
            query=query,
            target_agent=target,
            response_summary=response_summary
        ))

    def declare_domain(
        self,
        task_description: str,
        justification: str
    ) -> None:
        """
        Declare that this task is within the agent's domain.

        Args:
            task_description: What the agent is doing
            justification: Why this is in the agent's lane
        """
        # Get domain description from role
        domain_descriptions = {
            "archivist": "Retrieval and indexing - rapid retrieval of established content",
            "status_tracker": "Real-time character state - physical, emotional, knowledge",
            "theme_guardian": "Thematic consistency and artistic vision",
            "timeline_keeper": "Chronological accuracy - when things happen",
            "scene_choreographer": "Movement and blocking - character positions",
            "reader_proxy": "Audience knowledge and experience - dramatic irony",
            "pacing_monitor": "Tension curves and rhythm",
            "technical_consultant": "Subject matter expertise (rotating)",
            "intimacy_coordinator": "Sensitive content and agent dynamics",
            "outline_assistant": "Story structure and planning documents",
            "production_designer": "Physical objects, costumes, vehicles, tech",
            "character_steward": "Character embodiment across series"
        }

        role = self.meta["agent_role"]
        self.domain_declaration = {
            "my_domain": domain_descriptions.get(role, "Unknown domain"),
            "task_description": task_description,
            "task_within_domain": True,  # Agent declares this
            "justification": justification
        }

    def add_source(
        self,
        claim: str,
        source_file: str,
        source_section: Optional[str] = None,
        source_line: Optional[int] = None
    ) -> None:
        """
        Add source attribution for a claim in the output.

        Args:
            claim: The factual claim being made
            source_file: Path to source file
            source_section: Section within file (optional)
            source_line: Line number (optional)
        """
        self.source_attributions.append(SourceAttribution(
            claim=claim,
            source_file=source_file,
            source_section=source_section,
            source_line=source_line
        ))

    def add_deferral(
        self,
        item: str,
        deferred_to: str,
        reason: str
    ) -> None:
        """
        Log that an item was deferred to another specialist.

        Args:
            item: What was encountered
            deferred_to: Which agent role should handle it
            reason: Why it's outside this agent's domain
        """
        self.deferred_items.append(DeferralEntry(
            item=item,
            deferred_to=deferred_to,
            reason=reason
        ))

    def propose_state_change(
        self,
        state_type: str,
        entity_id: str,
        change: str,
        requires_confirmation: bool = True
    ) -> None:
        """
        Propose a state change (requires Director confirmation).

        Args:
            state_type: Type of state being changed (e.g., "character_knowledge")
            entity_id: What entity is affected (e.g., "ahdia")
            change: Description of the change
            requires_confirmation: Whether Director must confirm
        """
        self.state_changes_proposed.append(StateChangeProposal(
            state_type=state_type,
            entity_id=entity_id,
            change=change,
            requires_confirmation=requires_confirmation
        ))

    def set_output(
        self,
        content: Any,
        confidence: Literal["high", "medium", "low"] = "high",
        caveats: Optional[List[str]] = None
    ) -> None:
        """
        Set the operation's output.

        Args:
            content: The actual work product
            confidence: Confidence level in the output
            caveats: Any caveats or limitations
        """
        self.output = {
            "content": content,
            "confidence": confidence,
            "caveats": caveats or []
        }

    def validate(self) -> ValidationResult:
        """
        Validate this process log against Go Squad protocol.

        Returns:
            ValidationResult with status and any issues
        """
        return GateValidator.validate(self)

    def to_dict(self) -> Dict[str, Any]:
        """Export process log as dictionary."""
        return {
            "meta": self.meta,
            "query_log": [
                {
                    "query": q.query,
                    "target_agent": q.target_agent,
                    "response_summary": q.response_summary,
                    "timestamp": q.timestamp
                }
                for q in self.query_log
            ],
            "domain_declaration": self.domain_declaration,
            "source_attributions": [
                {
                    "claim": s.claim,
                    "source_file": s.source_file,
                    "source_section": s.source_section,
                    "source_line": s.source_line
                }
                for s in self.source_attributions
            ],
            "deferred_items": [
                {
                    "item": d.item,
                    "deferred_to": d.deferred_to,
                    "reason": d.reason
                }
                for d in self.deferred_items
            ],
            "state_changes_proposed": [
                {
                    "state_type": s.state_type,
                    "entity_id": s.entity_id,
                    "change": s.change,
                    "requires_confirmation": s.requires_confirmation
                }
                for s in self.state_changes_proposed
            ],
            "output": self.output
        }

    def to_json(self, indent: int = 2) -> str:
        """Export process log as JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def __str__(self) -> str:
        """Human-readable summary."""
        lines = [
            "=" * 60,
            "PROCESS LOG",
            "=" * 60,
            f"Agent: {self.meta['agent_role']}",
            f"Task: {self.meta['task_id']}",
            f"Timestamp: {self.meta['timestamp']}",
        ]

        if self.meta['mode'] != "n/a":
            lines.append(f"Mode: {self.meta['mode']}")

        lines.append("")
        lines.append("QUERY LOG:")
        if self.query_log:
            for q in self.query_log:
                lines.append(f"  → {q.target_agent}: {q.query}")
                lines.append(f"    Response: {q.response_summary}")
        else:
            lines.append("  (no queries made)")

        lines.append("")
        lines.append("DOMAIN DECLARATION:")
        if self.domain_declaration:
            lines.append(f"  Domain: {self.domain_declaration['my_domain']}")
            lines.append(f"  Task: {self.domain_declaration['task_description']}")
            lines.append(f"  In domain: {self.domain_declaration['task_within_domain']}")
            lines.append(f"  Justification: {self.domain_declaration['justification']}")
        else:
            lines.append("  (not declared)")

        lines.append("")
        lines.append("SOURCE ATTRIBUTIONS:")
        if self.source_attributions:
            for s in self.source_attributions:
                lines.append(f"  Claim: {s.claim}")
                lines.append(f"    Source: {s.source_file}")
                if s.source_section:
                    lines.append(f"    Section: {s.source_section}")
        else:
            lines.append("  (no sources cited)")

        lines.append("")
        lines.append("DEFERRED ITEMS:")
        if self.deferred_items:
            for d in self.deferred_items:
                lines.append(f"  → {d.deferred_to}: {d.item}")
                lines.append(f"    Reason: {d.reason}")
        else:
            lines.append("  (nothing deferred)")

        if self.state_changes_proposed:
            lines.append("")
            lines.append("STATE CHANGES PROPOSED:")
            for s in self.state_changes_proposed:
                lines.append(f"  {s.state_type}.{s.entity_id}: {s.change}")
                lines.append(f"    Requires confirmation: {s.requires_confirmation}")

        lines.append("")
        lines.append("OUTPUT:")
        if self.output:
            lines.append(f"  Confidence: {self.output['confidence']}")
            if self.output['caveats']:
                lines.append(f"  Caveats: {', '.join(self.output['caveats'])}")
            lines.append(f"  Content: {json.dumps(self.output['content'], indent=4)}")
        else:
            lines.append("  (no output set)")

        lines.append("=" * 60)
        return "\n".join(lines)


class GateValidator:
    """
    Validates process logs against Go Squad protocol.

    The gate isn't "is this output good?" The gate is
    "did you follow protocol to produce this output?"
    """

    # Tasks that typically require queries
    QUERY_REQUIRED_TASKS = [
        "character_state",
        "knowledge_check",
        "canon_verification",
        "timeline_check",
        "location_lookup",
        "object_lookup",
        "relationship_check"
    ]

    # Domain boundaries - what each role can do
    DOMAIN_BOUNDARIES = {
        "archivist": [
            "retrieve", "index", "search", "lookup", "cross_reference"
        ],
        "status_tracker": [
            "character_state", "knowledge_check", "physical_state",
            "emotional_state", "relationship_state", "knowledge", "who_knows",
            "character", "state", "check"
        ],
        "theme_guardian": [
            "theme_check", "vision_alignment", "drift_detection"
        ],
        "timeline_keeper": [
            "timeline_check", "temporal_consistency", "event_order"
        ],
        "scene_choreographer": [
            "blocking", "movement", "position", "sightline"
        ],
        "reader_proxy": [
            "reader_knowledge", "dramatic_irony", "revelation_tracking"
        ],
        "pacing_monitor": [
            "tension_tracking", "rhythm", "emotional_register"
        ],
        "technical_consultant": [
            "authenticity", "procedure", "realism"
        ],
        "intimacy_coordinator": [
            "content_guidance", "sensitive_content", "relational_health"
        ],
        "outline_assistant": [
            "structure", "beat_sheet", "planning"
        ],
        "production_designer": [
            "object_design", "tech_spec", "costume", "vehicle"
        ],
        "character_steward": [
            "character_choice", "dialogue", "behavior", "voice"
        ]
    }

    @classmethod
    def validate(cls, log: ProcessLog) -> ValidationResult:
        """
        Validate a process log.

        Args:
            log: The process log to validate

        Returns:
            ValidationResult with status and issues
        """
        issues: List[str] = []
        warnings: List[str] = []

        # Rule 1: Domain declaration required
        if not log.domain_declaration:
            issues.append("MISSING: Domain declaration not provided")
        elif not log.domain_declaration.get("task_within_domain", False):
            issues.append("OUT_OF_LANE: Agent declared task outside domain")
        else:
            # Check if task matches role's domain
            role = log.meta["agent_role"]
            task = log.domain_declaration.get("task_description", "").lower()

            if role in cls.DOMAIN_BOUNDARIES:
                keywords = cls.DOMAIN_BOUNDARIES[role]
                if not any(kw in task for kw in keywords):
                    warnings.append(
                        f"SUSPICIOUS: Task '{task}' may not match {role} domain"
                    )

        # Rule 2: Query log should not be empty for most tasks
        task_id = log.meta.get("task_id", "")
        needs_query = any(
            keyword in task_id.lower()
            for keyword in cls.QUERY_REQUIRED_TASKS
        )

        if needs_query and not log.query_log:
            issues.append(
                "MISSING: Query log empty but task type typically requires queries"
            )

        # Rule 3: Source attribution for output
        if log.output and not log.source_attributions:
            # Check if output contains factual claims
            output_content = log.output.get("content", "")
            if isinstance(output_content, dict) or isinstance(output_content, list):
                issues.append(
                    "MISSING: No source attribution for output with factual content"
                )
            else:
                warnings.append(
                    "SUSPICIOUS: No sources cited - is output based on memory alone?"
                )

        # Rule 4: Character Steward mode declaration
        if log.meta["agent_role"] == "character_steward":
            if log.meta.get("mode") in [None, "n/a"]:
                issues.append(
                    "MISSING: Character Steward must declare exploration/performance mode"
                )

        # Rule 5: Complex operations should have deferrals
        # (If many queries to different agents, complexity is high)
        unique_targets = set(q.target_agent for q in log.query_log)
        if len(unique_targets) > 3 and not log.deferred_items:
            warnings.append(
                "SUSPICIOUS: Complex operation (4+ agent types queried) with no deferrals"
            )

        # Rule 6: Self-answering queries
        role = log.meta["agent_role"]
        self_answers = [
            q for q in log.query_log
            if q.target_agent == role
        ]
        if self_answers:
            warnings.append(
                f"SUSPICIOUS: {len(self_answers)} queries answered by self"
            )

        # Rule 7: Output required
        if not log.output:
            issues.append("MISSING: No output set")

        # Determine status
        if issues:
            status = ValidationStatus.REJECTED
        elif warnings:
            status = ValidationStatus.FLAGGED
        else:
            status = ValidationStatus.APPROVED

        return ValidationResult(
            status=status,
            issues=issues,
            warnings=warnings
        )


class ConsultationLog:
    """
    Logs AI-AI consultations between agents.

    When Agent A queries Agent B, both sides are logged.
    The consultation chain is visible in process logs.
    """

    def __init__(self):
        self.consultations: List[Dict[str, Any]] = []

    def log_consultation(
        self,
        requester_role: str,
        requester_task_id: str,
        responder_role: str,
        query: str,
        response_summary: str,
        response_sources: List[str]
    ) -> str:
        """
        Log a consultation between agents.

        Args:
            requester_role: Role of requesting agent
            requester_task_id: Task ID of requesting operation
            responder_role: Role of responding agent
            query: What was asked
            response_summary: Summary of response
            response_sources: Files/sections consulted

        Returns:
            Consultation ID for reference
        """
        consultation_id = f"consult_{len(self.consultations) + 1}"

        self.consultations.append({
            "consultation_id": consultation_id,
            "timestamp": datetime.now().isoformat(),
            "requester": {
                "role": requester_role,
                "task_id": requester_task_id
            },
            "responder": {
                "role": responder_role
            },
            "query": query,
            "response_summary": response_summary,
            "response_sources": response_sources
        })

        return consultation_id

    def get_chain(self, task_id: str) -> List[Dict[str, Any]]:
        """Get all consultations for a task."""
        return [
            c for c in self.consultations
            if c["requester"]["task_id"] == task_id
        ]

    def to_dict(self) -> List[Dict[str, Any]]:
        """Export as dictionary."""
        return self.consultations


# Global consultation log (singleton for session)
_consultation_log: Optional[ConsultationLog] = None

def get_consultation_log() -> ConsultationLog:
    """Get or create the global consultation log."""
    global _consultation_log
    if _consultation_log is None:
        _consultation_log = ConsultationLog()
    return _consultation_log


# ========================================
# CLI for testing
# ========================================

def main():
    """Demo/test the process log system."""
    import argparse

    parser = argparse.ArgumentParser(description="Process Log System Demo")
    parser.add_argument(
        '--demo',
        choices=['valid', 'missing_query', 'missing_domain', 'missing_source'],
        default='valid',
        help='Demo scenario to run'
    )

    args = parser.parse_args()

    if args.demo == 'valid':
        # Valid process log
        log = ProcessLog(
            agent_role="status_tracker",
            task_id="knowledge_check_ahdia_exile_ch13"
        )

        log.add_query(
            query="who_knows('exile_island', 13)",
            target="archivist",
            response_summary="Retrieved awareness list for chapter 13"
        )

        log.declare_domain(
            task_description="Verify who knows about exile_island at chapter 13",
            justification="Knowledge tracking is Status Tracker's core function"
        )

        log.add_source(
            claim="Team learns about exile_island at chapter 13",
            source_file="7_characters/arcs/CHARACTER_STATE_INDEX.yaml",
            source_section="knowledge_tracking.exile_island.awareness.ch13"
        )

        log.set_output(
            content={
                "knowledge_item": "exile_island",
                "chapter": 13,
                "who_knows": ["ahdia", "ryu", "ruth", "ben", "tess", "victor", "leah"]
            },
            confidence="high"
        )

    elif args.demo == 'missing_query':
        # Missing query log
        log = ProcessLog(
            agent_role="status_tracker",
            task_id="knowledge_check_ahdia_exile_ch13"
        )

        log.declare_domain(
            task_description="Verify who knows about exile_island at chapter 13",
            justification="Knowledge tracking is Status Tracker's core function"
        )

        # No queries made!

        log.set_output(
            content={"who_knows": ["ahdia", "ryu"]},  # Incomplete/wrong
            confidence="high"
        )

    elif args.demo == 'missing_domain':
        # Missing domain declaration
        log = ProcessLog(
            agent_role="status_tracker",
            task_id="knowledge_check_ahdia_exile_ch13"
        )

        log.add_query(
            query="who_knows('exile_island', 13)",
            target="archivist",
            response_summary="Retrieved awareness list"
        )

        # No domain declaration!

        log.set_output(
            content={"who_knows": ["ahdia", "ryu", "team"]},
            confidence="high"
        )

    elif args.demo == 'missing_source':
        # Missing source attribution
        log = ProcessLog(
            agent_role="status_tracker",
            task_id="knowledge_check_ahdia_exile_ch13"
        )

        log.add_query(
            query="who_knows('exile_island', 13)",
            target="archivist",
            response_summary="Retrieved awareness list"
        )

        log.declare_domain(
            task_description="Verify who knows about exile_island at chapter 13",
            justification="Knowledge tracking is Status Tracker's core function"
        )

        # No source attribution!

        log.set_output(
            content={"who_knows": ["ahdia", "ryu", "team"]},
            confidence="high"
        )

    # Print process log
    print(log)

    # Validate
    print("\n" + "=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)
    result = log.validate()
    print(result)


if __name__ == '__main__':
    main()
