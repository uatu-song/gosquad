#!/usr/bin/env python3
"""
TTRPG Dungeon Master v5 - Optimized Data Architecture + Full Book 2 Mechanics

NEW IN V5:
- Optimized JSON-based data loading (10-20x faster)
- Eidolon influence tracking (fear/anger amplification)
- Investigation progress system (evidence quality, convergence)
- Public opinion tracker (Kain polling, Go Squad reputation)
- Ahdia power/baseline tracker (cellular degradation)
- Key events timeline (canonical beats)
- Resource tracking (funding, equipment, locations)

CONTINUES FROM V4:
- Complicity/Defiance tracking
- Character progression
- Canon integration
- Consequence bleed

Usage: python3 ttrpg_dm_v5.py [save_file]
"""

import json
import os
import random
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path


# ============================================================================
# CONSTANTS
# ============================================================================

# Institutional role definitions (from v4)
INSTITUTIONAL_ROLES = {
    "Ben": {
        "institution": "Former Military Intelligence / CADENS",
        "power": "Access to classified evidence, military tactics knowledge",
        "vulnerability": "Conservative faith in institutions eroding"
    },
    "Tess": {
        "institution": "Police Chief's Daughter",
        "power": "Access to police records via father",
        "vulnerability": "Father's betrayal, family vs justice"
    },
    "Ruth": {
        "institution": "CADENS Liaison",
        "power": "Bridge between organization and Go Squad",
        "vulnerability": "Protecting Ahdia means hiding from CADENS"
    },
    "Leah": {
        "institution": "White Moderate / Privileged Civilian",
        "power": "Can infiltrate elite spaces, less police scrutiny",
        "vulnerability": "Silence = complicity, learning to speak up"
    }
}

COMPLICITY_COSTS = [
    "Followed orders that harmed others (+1 Complicity)",
    "Stayed silent when should have spoken (+1 Complicity)",
    "Chose career/safety over conscience (+1 Complicity)",
    "Protected institution over people (+1 Complicity)",
    "Used institutional power for personal gain (+1 Complicity)",
    "Looked away from injustice (+1 Complicity)"
]

DEFIANCE_COSTS = [
    "Leaked information to resistance (+1 Defiance)",
    "Deliberately delayed harmful operation (+1 Defiance)",
    "Warned targets of incoming threat (+1 Defiance)",
    "Operated outside institutional authority (+1 Defiance)",
    "Chose people over career advancement (+1 Defiance)",
    "Publicly challenged institutional power (+1 Defiance)"
]


# ============================================================================
# V5 NEW CLASSES
# ============================================================================

class CanonLoaderV5:
    """Optimized three-tier data loading system"""

    def __init__(self, json_path: Optional[str] = None):
        if json_path is None:
            # Default path relative to this script
            json_path = Path(__file__).parent.parent / "Reference_Documents" / "TTRPG_DATA_REFERENCE.json"

        self.json_path = Path(json_path)

        # Tier 1: Always loaded (compact JSON)
        self.compact_data = self._load_json_reference()

        # Tier 2: Extracted facts (canonical checks)
        self.canon_facts = self._extract_canon_facts()

        # Tier 3: Lazy-loaded (on demand)
        self.story_bible_cache = {}
        self.chapter_cache = {}

    def _load_json_reference(self) -> Dict:
        """Load compact TTRPG_DATA_REFERENCE.json"""
        if not self.json_path.exists():
            print(f"⚠ Warning: {self.json_path} not found, using empty data")
            return {}

        try:
            with open(self.json_path, 'r') as f:
                data = json.load(f)
                print(f"✓ Loaded compact data from {self.json_path.name}")
                return data
        except Exception as e:
            print(f"✗ Error loading JSON: {e}")
            return {}

    def _extract_canon_facts(self) -> Dict:
        """Extract only critical facts from CANON.md"""
        facts = {}

        canon_path = Path(__file__).parent.parent / "Reference_Documents" / "CANON.md"

        if not canon_path.exists():
            return facts

        try:
            with open(canon_path, 'r') as f:
                content = f.read()

            # Extract specific facts using regex
            patterns = {
                "tess_no_kill": r"Tess.*NOT.*kill",
                "isaiah_police": r"Isaiah.*killed.*police",
                "ahdia_no_rewind": r"FREEZE.*ACCELERATE.*NO REWIND",
                "treatment_providers": r"Ruth.*Ryu.*only",
                "webb_kills": r"Webb.*kills.*Isaiah.*Leta"
            }

            for key, pattern in patterns.items():
                if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                    facts[key] = True

            print(f"✓ Extracted {len(facts)} canon facts")

        except Exception as e:
            print(f"⚠ Warning: Could not extract canon facts: {e}")

        return facts

    def get_character(self, name: str) -> Optional[Dict]:
        """Get character from compact data (fast)"""
        return self.compact_data.get("characters_compact", {}).get(name)

    def get_all_characters(self) -> Dict[str, Dict]:
        """Get all characters from compact data"""
        return self.compact_data.get("characters_compact", {})

    def get_month_summary(self, month: int) -> Optional[Dict]:
        """Get month summary from compact data (fast)"""
        summaries = self.compact_data.get("book_2_synopsis", {}).get("month_summaries", {})

        # Try exact match first
        if str(month) in summaries:
            return summaries[str(month)]

        # Try ranges
        for key, value in summaries.items():
            if "-" in key:
                try:
                    start, end = map(int, key.split("-"))
                    if start <= month <= end:
                        return value
                except:
                    pass

        return None

    def get_investigation(self, inv_key: str) -> Optional[Dict]:
        """Get investigation data (fast)"""
        return self.compact_data.get("investigations_compact", {}).get(inv_key)

    def get_all_investigations(self) -> Dict[str, Dict]:
        """Get all investigations"""
        return self.compact_data.get("investigations_compact", {})

    def get_key_events(self, month: int) -> List[str]:
        """Get key events for specific month (fast)"""
        timeline = self.compact_data.get("key_events_timeline", {})

        month_key = f"month_{month}"
        return timeline.get(month_key, [])

    def get_mechanics_reference(self, system: str) -> Optional[Dict]:
        """Get mechanics reference (fast)"""
        return self.compact_data.get("mechanics_reference", {}).get(system)

    def check_canon_fact(self, query: str) -> Optional[str]:
        """Fast canon checking against extracted facts"""
        query_lower = query.lower()

        # Tess canon
        if "tess" in query_lower and "kill" in query_lower:
            if self.canon_facts.get("tess_no_kill"):
                if "isaiah" in query_lower:
                    return "✗ CANON VIOLATION: Tess does NOT kill Isaiah. Isaiah was killed by POLICE."
                return "✓ CANON: Tess does NOT kill anyone. She investigates killings."

        # Isaiah canon
        if "isaiah" in query_lower:
            if "police" in query_lower and self.canon_facts.get("isaiah_police"):
                return "✓ CANON: Isaiah Bennett killed by police (Officer Webb). Chief Whitford complicit."

        # Ahdia powers
        if "ahdia" in query_lower and "rewind" in query_lower:
            if self.canon_facts.get("ahdia_no_rewind"):
                return "✗ CANON VIOLATION: Ahdia CANNOT rewind time. Only FREEZE/ACCELERATE."

        # Treatment
        if "treatment" in query_lower:
            if self.canon_facts.get("treatment_providers"):
                return "✓ CANON: Treatment only Ruth + Ryu. CADENS facility required. Prevents transcendence (not death)."

        # Webb
        if "webb" in query_lower:
            if self.canon_facts.get("webb_kills"):
                return "✓ CANON: Officer Webb kills Isaiah (pre-Book 2) and Leta (Month 11). Exonerated both times."

        return None


class EidolonInfluence:
    """Track fear/anger amplification entity"""

    def __init__(self):
        self.activity_level = 0  # 0-10 scale
        self.current_targets = []  # Locations/groups affected
        self.resistance_practiced = []  # Characters trained in Both/And
        self.amplification_events = []  # History of uses

    def set_activity_level(self, level: int, location: str = "Caledonia"):
        """Set Eidolon activity level"""
        self.activity_level = max(0, min(10, level))
        if location not in self.current_targets:
            self.current_targets.append(location)

    def amplify_emotion(self, base_intensity: int) -> int:
        """Return amplified emotion level"""
        amplified = min(10, base_intensity + self.activity_level)
        return amplified

    def resistance_check(self, character_name: str, difficulty: int = 7) -> Dict[str, Any]:
        """Check if character resists Eidolon manipulation"""
        bonus = 2 if character_name in self.resistance_practiced else 0
        roll = random.randint(1, 10) + bonus
        success = roll >= difficulty

        return {
            "roll": roll,
            "bonus": bonus,
            "difficulty": difficulty,
            "success": success,
            "margin": roll - difficulty
        }

    def train_resistance(self, character_name: str):
        """Train character in Both/And resistance practice"""
        if character_name not in self.resistance_practiced:
            self.resistance_practiced.append(character_name)
            print(f"✓ {character_name} trained in Eidolon resistance (Both/And practice)")

    def record_amplification(self, month: int, location: str, outcome: str):
        """Record an amplification event"""
        self.amplification_events.append({
            "month": month,
            "location": location,
            "outcome": outcome,
            "activity_level": self.activity_level
        })

    def to_dict(self) -> Dict:
        return {
            "activity_level": self.activity_level,
            "current_targets": self.current_targets,
            "resistance_practiced": self.resistance_practiced,
            "amplification_events": self.amplification_events
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'EidolonInfluence':
        eidolon = cls()
        eidolon.activity_level = data.get("activity_level", 0)
        eidolon.current_targets = data.get("current_targets", [])
        eidolon.resistance_practiced = data.get("resistance_practiced", [])
        eidolon.amplification_events = data.get("amplification_events", [])
        return eidolon


class InvestigationTracker:
    """Track multiple converging investigations"""

    def __init__(self, canon_loader: CanonLoaderV5):
        # Load investigations from compact data
        investigations_data = canon_loader.get_all_investigations()

        self.investigations = {}
        for key, data in investigations_data.items():
            # Don't pass data twice - target and lead_investigator are extracted separately
            self.investigations[key] = Investigation(
                key=key,
                target=data.get("target", "Unknown"),
                lead_investigator=self._extract_investigator(key),
                public_leak=data.get("public_leak"),
                evidence_quality=data.get("evidence_quality", "weak"),
                outcome=data.get("outcome")
            )

    def _extract_investigator(self, key: str) -> str:
        """Extract investigator name from key (e.g., 'ben_tank_kain' -> 'Ben')"""
        parts = key.split("_")
        if parts:
            return parts[0].capitalize()
        return "Unknown"

    def get_investigation(self, key: str) -> Optional['Investigation']:
        """Get specific investigation"""
        return self.investigations.get(key)

    def add_evidence(self, inv_key: str, description: str, quality: str, month: int):
        """Add evidence to investigation"""
        if inv_key in self.investigations:
            self.investigations[inv_key].add_evidence(description, quality, month)
            print(f"\n📋 Evidence added to {inv_key}:")
            print(f"   {description} (Quality: {quality})")

    def check_convergence(self, month: int) -> bool:
        """Check if investigations have converged on TRIOMF"""
        if month >= 6:
            # Count investigations with TRIOMF connection
            connected = sum(1 for inv in self.investigations.values()
                          if inv.has_triomf_connection)
            return connected >= 4
        return False

    def get_summary(self) -> str:
        """Get summary of all investigations"""
        lines = []
        for key, inv in self.investigations.items():
            lines.append(f"{key}: {inv.progress}% complete")
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        return {
            key: inv.to_dict()
            for key, inv in self.investigations.items()
        }

    @classmethod
    def from_dict(cls, data: Dict, canon_loader: CanonLoaderV5) -> 'InvestigationTracker':
        tracker = cls(canon_loader)
        # Update with saved data
        for key, inv_data in data.items():
            if key in tracker.investigations:
                tracker.investigations[key] = Investigation.from_dict(inv_data)
        return tracker


class Investigation:
    """Individual investigation tracking"""

    def __init__(self, key: str, target: str, lead_investigator: str, **kwargs):
        self.key = key
        self.target = target
        self.lead_investigator = lead_investigator
        self.evidence_pieces = []
        self.progress = 0  # 0-100%
        self.public_leak_month = kwargs.get("public_leak")
        self.evidence_quality = kwargs.get("evidence_quality", "weak")
        self.outcome = kwargs.get("outcome")
        self.has_triomf_connection = False

    def add_evidence(self, description: str, quality: str, month: int):
        """Add evidence piece"""
        self.evidence_pieces.append({
            "description": description,
            "quality": quality,
            "discovered": month
        })

        # Update progress based on quality
        quality_values = {"weak": 10, "strong": 25, "irrefutable": 40}
        self.progress = min(100, self.progress + quality_values.get(quality, 10))

        # Check for TRIOMF connection
        if "triomf" in description.lower() or "titan strategic" in description.lower():
            self.has_triomf_connection = True

    def to_dict(self) -> Dict:
        return {
            "key": self.key,
            "target": self.target,
            "lead_investigator": self.lead_investigator,
            "evidence_pieces": self.evidence_pieces,
            "progress": self.progress,
            "public_leak_month": self.public_leak_month,
            "evidence_quality": self.evidence_quality,
            "outcome": self.outcome,
            "has_triomf_connection": self.has_triomf_connection
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Investigation':
        inv = cls(
            key=data["key"],
            target=data["target"],
            lead_investigator=data["lead_investigator"]
        )
        inv.evidence_pieces = data.get("evidence_pieces", [])
        inv.progress = data.get("progress", 0)
        inv.public_leak_month = data.get("public_leak_month")
        inv.evidence_quality = data.get("evidence_quality", "weak")
        inv.outcome = data.get("outcome")
        inv.has_triomf_connection = data.get("has_triomf_connection", False)
        return inv


class PublicOpinion:
    """Track Kain polling and Go Squad reputation"""

    def __init__(self):
        self.kain_polling = 8  # Starts at +8 lead
        self.go_squad_reputation = 50  # 0-100 scale
        self.media_events = []

    def update_kain_polling(self, change: int, reason: str, month: int):
        """Update Kain's polling numbers"""
        old_polling = self.kain_polling
        self.kain_polling = max(-20, min(20, self.kain_polling + change))

        self.media_events.append({
            "month": month,
            "type": "polling",
            "change": change,
            "reason": reason,
            "before": old_polling,
            "after": self.kain_polling
        })

        print(f"\n📊 Kain Polling: {old_polling:+d} → {self.kain_polling:+d} ({reason})")

    def update_go_squad_reputation(self, change: int, reason: str, month: int):
        """Update Go Squad reputation"""
        old_rep = self.go_squad_reputation
        self.go_squad_reputation = max(0, min(100, self.go_squad_reputation + change))

        self.media_events.append({
            "month": month,
            "type": "reputation",
            "change": change,
            "reason": reason,
            "before": old_rep,
            "after": self.go_squad_reputation
        })

        print(f"\n📊 Go Squad Reputation: {old_rep} → {self.go_squad_reputation} ({reason})")

    def apply_evidence_leak(self, quality: str, month: int):
        """Evidence leaks affect Kain polling temporarily"""
        impact = {"weak": -1, "strong": -3, "irrefutable": -5}
        change = impact.get(quality, -2)
        self.update_kain_polling(change, f"Evidence leak ({quality})", month)

    def apply_eidolon_reframe(self, month: int):
        """Eidolon reframes narrative, polling recovers"""
        # Recovery based on current position
        if self.kain_polling < 8:
            recovery = min(2, 8 - self.kain_polling)
            self.update_kain_polling(recovery, "Eidolon narrative reframe", month)

    def to_dict(self) -> Dict:
        return {
            "kain_polling": self.kain_polling,
            "go_squad_reputation": self.go_squad_reputation,
            "media_events": self.media_events
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PublicOpinion':
        opinion = cls()
        opinion.kain_polling = data.get("kain_polling", 8)
        opinion.go_squad_reputation = data.get("go_squad_reputation", 50)
        opinion.media_events = data.get("media_events", [])
        return opinion


class AhdiaPowerTracker:
    """Track Ahdia's cellular degradation and power usage"""

    def __init__(self):
        self.baseline_percentage = 100.0  # Starts at 100%
        self.minutes_frozen_this_month = 0.0
        self.total_minutes_frozen = 0.0
        self.treatment_count = 0
        self.next_treatment_month = 2
        self.critical_threshold = 10.0  # Below 10% is critically depleted
        self.power_usage_log = []

    def freeze_time(self, minutes: float, month: int, context: str = "") -> Dict:
        """Track time freeze usage and cost"""
        self.minutes_frozen_this_month += minutes
        self.total_minutes_frozen += minutes

        # Calculate lifespan cost (0.2% baseline per minute avg)
        cost_per_minute = 0.2
        baseline_cost = minutes * cost_per_minute

        old_baseline = self.baseline_percentage
        self.baseline_percentage = max(0, self.baseline_percentage - baseline_cost)

        # Log the usage
        self.power_usage_log.append({
            "month": month,
            "minutes": minutes,
            "context": context,
            "cost": baseline_cost,
            "baseline_after": self.baseline_percentage
        })

        result = {
            "minutes_frozen": minutes,
            "baseline_cost": baseline_cost,
            "baseline_before": old_baseline,
            "baseline_after": self.baseline_percentage,
            "critical": self.baseline_percentage < self.critical_threshold,
            "transcendence_risk": self.baseline_percentage < 1.0
        }

        # Print warning if critical
        if result["critical"]:
            print(f"\n⚠️ CRITICAL: Ahdia baseline at {self.baseline_percentage:.1f}%")

        return result

    def receive_treatment(self, month: int):
        """Ruth/Ryu treatment extends timeline"""
        self.treatment_count += 1
        self.next_treatment_month = month + 2

        print(f"\n💉 Treatment #{self.treatment_count} administered (Month {month})")
        print(f"   Baseline: {self.baseline_percentage:.1f}%")
        print(f"   Next treatment due: Month {self.next_treatment_month}")

    def reset_monthly_counter(self):
        """Reset monthly freeze counter"""
        self.minutes_frozen_this_month = 0.0

    def get_status_summary(self) -> str:
        """Get current status summary"""
        status = f"Baseline: {self.baseline_percentage:.1f}%"
        if self.baseline_percentage < self.critical_threshold:
            status += " (CRITICAL)"
        elif self.baseline_percentage < 30:
            status += " (DANGEROUS)"
        elif self.baseline_percentage < 50:
            status += " (CONCERNING)"

        status += f"\nTotal frozen: {self.total_minutes_frozen:.1f} minutes"
        status += f"\nTreatments: {self.treatment_count}"

        return status

    def to_dict(self) -> Dict:
        return {
            "baseline_percentage": self.baseline_percentage,
            "minutes_frozen_this_month": self.minutes_frozen_this_month,
            "total_minutes_frozen": self.total_minutes_frozen,
            "treatment_count": self.treatment_count,
            "next_treatment_month": self.next_treatment_month,
            "power_usage_log": self.power_usage_log
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'AhdiaPowerTracker':
        tracker = cls()
        tracker.baseline_percentage = data.get("baseline_percentage", 100.0)
        tracker.minutes_frozen_this_month = data.get("minutes_frozen_this_month", 0.0)
        tracker.total_minutes_frozen = data.get("total_minutes_frozen", 0.0)
        tracker.treatment_count = data.get("treatment_count", 0)
        tracker.next_treatment_month = data.get("next_treatment_month", 2)
        tracker.power_usage_log = data.get("power_usage_log", [])
        return tracker


class KeyEventTracker:
    """Track canonical timeline events"""

    def __init__(self, canon_loader: CanonLoaderV5):
        # Load events from compact data
        events_data = canon_loader.compact_data.get("key_events_timeline", {})

        self.events = {}
        self._load_events_from_data(events_data)

    def _load_events_from_data(self, events_data: Dict):
        """Load events from JSON data"""
        for key, value in events_data.items():
            if isinstance(value, list):
                # month_X: [list of events]
                try:
                    month = int(key.split("_")[1]) if "_" in key and len(key.split("_")) > 1 else 0
                except (ValueError, IndexError):
                    month = 0

                for event_desc in value:
                    event_key = self._generate_event_key(event_desc)
                    self.events[event_key] = {
                        "month": month,
                        "description": event_desc,
                        "occurred": False
                    }
            elif isinstance(value, dict):
                # pre_book_2, post_election, etc.
                for event_key, event_desc in value.items():
                    self.events[event_key] = {
                        "month": -1 if "pre" in key else 13,
                        "description": event_desc,
                        "occurred": False
                    }

    def _generate_event_key(self, description: str) -> str:
        """Generate a key from event description"""
        # Extract key words
        words = description.lower().split()[:3]
        return "_".join(w for w in words if len(w) > 3)

    def trigger_event(self, event_key: str, month: int) -> bool:
        """Mark event as occurred"""
        if event_key in self.events:
            self.events[event_key]["occurred"] = True
            self.events[event_key]["actual_month"] = month
            print(f"\n📅 Event Triggered: {self.events[event_key]['description']}")
            return True
        return False

    def get_upcoming_events(self, current_month: int) -> List[Tuple[str, Dict]]:
        """Get events scheduled for current/upcoming months"""
        upcoming = []
        for key, data in self.events.items():
            if not data["occurred"] and data["month"] >= current_month:
                upcoming.append((key, data))
        return sorted(upcoming, key=lambda x: x[1]["month"])

    def to_dict(self) -> Dict:
        return self.events

    @classmethod
    def from_dict(cls, data: Dict, canon_loader: CanonLoaderV5) -> 'KeyEventTracker':
        tracker = cls(canon_loader)
        # Update with saved event states
        for key, event_data in data.items():
            if key in tracker.events:
                tracker.events[key] = event_data
        return tracker


# ============================================================================
# V4 CLASSES (UPDATED FOR V5)
# ============================================================================

class Character:
    """Represents a character with canon data and Complicity/Defiance tracking"""

    def __init__(self, name: str, competency: int = 7, current_state: str = "", canon_data: Optional[Dict] = None):
        self.name = name
        self.competency = competency
        self.current_state = current_state
        self.costs_accumulated = []
        self.limitations = []
        self.canon_data = canon_data

        # V4: Complicity/Defiance tracking
        self.has_institutional_role = name in INSTITUTIONAL_ROLES
        self.institutional_role = INSTITUTIONAL_ROLES.get(name, {})
        self.complicity_track = 0
        self.defiance_track = 0
        self.reckoning_threshold = 10
        self.reckoning_occurred = False
        self.reckoning_choice = None

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "competency": self.competency,
            "current_state": self.current_state,
            "costs_accumulated": self.costs_accumulated,
            "limitations": self.limitations,
            "has_canon": self.canon_data is not None,
            "has_institutional_role": self.has_institutional_role,
            "institutional_role": self.institutional_role,
            "complicity_track": self.complicity_track,
            "defiance_track": self.defiance_track,
            "reckoning_occurred": self.reckoning_occurred,
            "reckoning_choice": self.reckoning_choice
        }

    @classmethod
    def from_dict(cls, data: Dict, canon_loader: Optional[CanonLoaderV5] = None) -> 'Character':
        char = cls(data["name"], data["competency"], data["current_state"])
        char.costs_accumulated = data.get("costs_accumulated", [])
        char.limitations = data.get("limitations", [])
        char.has_institutional_role = data.get("has_institutional_role", False)
        char.institutional_role = data.get("institutional_role", {})
        char.complicity_track = data.get("complicity_track", 0)
        char.defiance_track = data.get("defiance_track", 0)
        char.reckoning_occurred = data.get("reckoning_occurred", False)
        char.reckoning_choice = data.get("reckoning_choice", None)

        # Try to load canon if available
        if canon_loader and data.get("has_canon"):
            char.canon_data = canon_loader.get_character(char.name)

        return char

    def check_reckoning(self) -> Tuple[bool, str]:
        """Check if character has hit reckoning point"""
        if self.reckoning_occurred:
            return (False, "Reckoning already occurred")

        if self.complicity_track >= self.reckoning_threshold:
            return (True, f"Complicity threshold reached ({self.complicity_track}/{self.reckoning_threshold})")

        if self.defiance_track >= self.reckoning_threshold:
            return (True, f"Defiance threshold reached ({self.defiance_track}/{self.reckoning_threshold})")

        difference = abs(self.complicity_track - self.defiance_track)
        if difference > 7:
            dominant = "Complicity" if self.complicity_track > self.defiance_track else "Defiance"
            return (True, f"Tracks imbalanced ({dominant} dominant by {difference})")

        return (False, f"Complicity: {self.complicity_track}, Defiance: {self.defiance_track}")

    def get_trajectory_summary(self) -> str:
        """Get character's current institutional trajectory"""
        if not self.has_institutional_role:
            return "No institutional role"

        if self.reckoning_occurred:
            choices = {
                "defection": "FULL DEFECTION - Quit/betrayed organization",
                "complicity": "FULL COMPLICITY - Became what they fought",
                "gap": "OPERATING IN GAP - Small acts of resistance within system"
            }
            return choices.get(self.reckoning_choice, "Unknown reckoning choice")

        total = self.complicity_track + self.defiance_track
        if total == 0:
            return "No institutional choices made yet"

        complicity_ratio = self.complicity_track / total

        if complicity_ratio > 0.7:
            return f"Trending toward COMPLICITY ({self.complicity_track}C / {self.defiance_track}D)"
        elif complicity_ratio < 0.3:
            return f"Trending toward DEFIANCE ({self.complicity_track}C / {self.defiance_track}D)"
        else:
            return f"BALANCED TENSION ({self.complicity_track}C / {self.defiance_track}D)"


class Scene:
    """Represents a generated scene with TTRPG mechanics"""

    def __init__(self, month: int, character: str, task: str):
        self.month = month
        self.character = character
        self.task = task
        self.timestamp = datetime.now().isoformat()
        self.dice_rolls = {}
        self.outcome = None
        self.cost = None
        self.limitation = None
        self.narrative_beats = []
        self.canon_checks = []
        self.institutional_impact = None

        # V5 additions
        self.eidolon_active = False
        self.evidence_gained = None
        self.ahdia_minutes_burned = 0.0

    def to_dict(self) -> Dict:
        return {
            "month": self.month,
            "character": self.character,
            "task": self.task,
            "timestamp": self.timestamp,
            "dice_rolls": self.dice_rolls,
            "outcome": self.outcome,
            "cost": self.cost,
            "limitation": self.limitation,
            "narrative_beats": self.narrative_beats,
            "canon_checks": self.canon_checks,
            "institutional_impact": self.institutional_impact,
            "eidolon_active": self.eidolon_active,
            "evidence_gained": self.evidence_gained,
            "ahdia_minutes_burned": self.ahdia_minutes_burned
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Scene':
        scene = cls(data["month"], data["character"], data["task"])
        scene.timestamp = data.get("timestamp", "")
        scene.dice_rolls = data.get("dice_rolls", {})
        scene.outcome = data.get("outcome")
        scene.cost = data.get("cost")
        scene.limitation = data.get("limitation")
        scene.narrative_beats = data.get("narrative_beats", [])
        scene.canon_checks = data.get("canon_checks", [])
        scene.institutional_impact = data.get("institutional_impact")
        scene.eidolon_active = data.get("eidolon_active", False)
        scene.evidence_gained = data.get("evidence_gained")
        scene.ahdia_minutes_burned = data.get("ahdia_minutes_burned", 0.0)
        return scene


# ============================================================================
# MAIN DUNGEON MASTER CLASS
# ============================================================================

class DungeonMaster:
    """Main DM class with all v5 systems integrated"""

    def __init__(self, save_file: str = "dm_state_v5.json"):
        self.save_file = save_file
        self.characters: Dict[str, Character] = {}
        self.scenes: List[Scene] = []
        self.current_month = 1
        self.consequence_pool = []

        # V5: New optimized loader
        print("\n" + "="*60)
        print("Initializing TTRPG Dungeon Master v5...")
        print("="*60)

        start_time = datetime.now()
        self.canon_loader = CanonLoaderV5()
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"✓ Canon loaded in {elapsed:.3f}s")

        # V5: New tracking systems
        self.eidolon = EidolonInfluence()
        self.investigations = InvestigationTracker(self.canon_loader)
        self.public_opinion = PublicOpinion()
        self.ahdia_powers = AhdiaPowerTracker()
        self.key_events = KeyEventTracker(self.canon_loader)

        # Load state (or initialize)
        self.load_state()

    def load_state(self):
        """Load persistent state from JSON"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)

                # Load characters
                self.characters = {
                    name: Character.from_dict(char_data, self.canon_loader)
                    for name, char_data in data.get("characters", {}).items()
                }

                # Load scenes
                self.scenes = [Scene.from_dict(scene_data) for scene_data in data.get("scenes", [])]

                # Load basic state
                self.current_month = data.get("current_month", 1)
                self.consequence_pool = data.get("consequence_pool", [])

                # Load v5 systems
                if "eidolon" in data:
                    self.eidolon = EidolonInfluence.from_dict(data["eidolon"])
                if "investigations" in data:
                    self.investigations = InvestigationTracker.from_dict(data["investigations"], self.canon_loader)
                if "public_opinion" in data:
                    self.public_opinion = PublicOpinion.from_dict(data["public_opinion"])
                if "ahdia_powers" in data:
                    self.ahdia_powers = AhdiaPowerTracker.from_dict(data["ahdia_powers"])
                if "key_events" in data:
                    self.key_events = KeyEventTracker.from_dict(data["key_events"], self.canon_loader)

                print(f"\n✓ Loaded state from {self.save_file}")
                print(f"  Characters: {len(self.characters)}")
                print(f"  Scenes: {len(self.scenes)}")
                print(f"  Month: {self.current_month}")
                print(f"  Ahdia baseline: {self.ahdia_powers.baseline_percentage:.1f}%")
                print(f"  Kain polling: {self.public_opinion.kain_polling:+d}")

            except Exception as e:
                print(f"\n✗ Error loading state: {e}")
                print("Starting fresh...")
                self.initialize_default_characters()
        else:
            print(f"\nNo save file found. Starting fresh.")
            self.initialize_default_characters()

    def save_state(self):
        """Save current state to JSON"""
        data = {
            "characters": {name: char.to_dict() for name, char in self.characters.items()},
            "scenes": [scene.to_dict() for scene in self.scenes],
            "current_month": self.current_month,
            "consequence_pool": self.consequence_pool,

            # V5 systems
            "eidolon": self.eidolon.to_dict(),
            "investigations": self.investigations.to_dict(),
            "public_opinion": self.public_opinion.to_dict(),
            "ahdia_powers": self.ahdia_powers.to_dict(),
            "key_events": self.key_events.to_dict(),

            "last_saved": datetime.now().isoformat(),
            "version": "5.0"
        }

        with open(self.save_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\n✓ State saved to {self.save_file}")

    def initialize_default_characters(self):
        """Set up Book 2 characters from compact data"""
        characters_data = self.canon_loader.get_all_characters()

        for name, data in characters_data.items():
            char = Character(
                name=name,
                competency=data.get("competency", 7),
                current_state=data.get("arc", ""),
                canon_data=data
            )

            # Add limitations from canon data
            if "limitation" in data:
                char.limitations = [data["limitation"]]

            self.characters[name] = char

        print(f"\n✓ Initialized {len(self.characters)} characters from compact data")

        # Show institutional roles
        institutional_chars = [name for name, char in self.characters.items() if char.has_institutional_role]
        if institutional_chars:
            print(f"✓ Tracking Complicity/Defiance for: {', '.join(institutional_chars)}")

    def check_canon(self, query: str) -> None:
        """Check and display canon fact"""
        result = self.canon_loader.check_canon_fact(query)
        if result:
            print(f"\n📖 Canon Check: {result}")
        else:
            print(f"\n📖 No canon information found for: {query}")

    def roll_dice(self, character_name: str, difficulty: int = 7) -> Dict[str, Any]:
        """Roll for scene outcome"""
        char = None
        actual_name = None

        for key in self.characters.keys():
            if key.lower() == character_name.lower():
                char = self.characters[key]
                actual_name = key
                break

        if not char:
            return {"error": f"Character {character_name} not found"}

        roll = random.randint(1, 10)
        total = roll + (char.competency - 5)
        success = total >= difficulty

        result = {
            "character": actual_name,
            "roll": roll,
            "competency": char.competency,
            "total": total,
            "difficulty": difficulty,
            "success": success,
            "critical_success": roll == 10,
            "critical_failure": roll == 1,
            "margin": total - difficulty
        }

        return result

    def _parse_institutional_impact(self, cost: str) -> Optional[str]:
        """Parse cost string to determine institutional impact"""
        if "(+1 Complicity)" in cost:
            return "complicity"
        elif "(+1 Defiance)" in cost:
            return "defiance"
        return None

    def _update_institutional_tracks(self, char: Character, cost: str, scene: Scene):
        """Update character's Complicity/Defiance tracks based on cost"""
        if not char.has_institutional_role:
            return

        impact = self._parse_institutional_impact(cost)
        if not impact:
            return

        scene.institutional_impact = impact

        if impact == "complicity":
            char.complicity_track += 1
            print(f"\n⚖️ {char.name} Complicity +1 (now {char.complicity_track})")
        elif impact == "defiance":
            char.defiance_track += 1
            print(f"\n⚖️ {char.name} Defiance +1 (now {char.defiance_track})")

        # Check for reckoning
        at_reckoning, reason = char.check_reckoning()
        if at_reckoning:
            print(f"\n🔥 RECKONING POINT REACHED!")
            print(f"   {reason}")
            print(f"\n   {char.name} must soon choose:")
            print(f"   1. Full Defection (quit/betray organization)")
            print(f"   2. Full Complicity (become what they fought)")
            print(f"   3. Operate in Gap (small acts of resistance within system)")

            self.consequence_pool.append({
                "description": f"{char.name} RECKONING: Must choose institutional path",
                "month": self.current_month + 1,
                "added": datetime.now().isoformat()
            })

    def generate_scene(
        self,
        character_name: str,
        task_description: str,
        month: Optional[int] = None,
        difficulty: int = 7,
        eidolon_active: bool = False
    ) -> Optional[Scene]:
        """Generate a complete scene using v5 integrated systems"""
        if month is None:
            month = self.current_month

        # Case-insensitive character lookup
        actual_name = None
        for key in self.characters.keys():
            if key.lower() == character_name.lower():
                actual_name = key
                break

        if not actual_name:
            print(f"\n✗ Character {character_name} not found")
            print(f"Available: {', '.join(self.characters.keys())}")
            return None

        scene = Scene(month, actual_name, task_description)
        scene.eidolon_active = eidolon_active
        char = self.characters[actual_name]

        print(f"\n{'='*60}")
        print(f"GENERATING SCENE - Month {month}")
        print(f"Character: {actual_name}")
        print(f"Task: {task_description}")
        print(f"Current state: {char.current_state}")

        # Show canon data if available
        if char.canon_data:
            print(f"📖 Canon loaded from compact data")

        # V4: Show institutional status
        if char.has_institutional_role:
            print(f"⚖️ Institutional Role: {char.institutional_role.get('institution', 'Unknown')}")
            print(f"   Trajectory: {char.get_trajectory_summary()}")

        # V5: Show Ahdia power status
        if actual_name == "Ahdia":
            print(f"⚡ Power Status: {self.ahdia_powers.get_status_summary()}")

        # V5: Show Eidolon status
        if eidolon_active:
            print(f"👁️ Eidolon Active (Level {self.eidolon.activity_level}/10)")

        print(f"{'='*60}\n")

        # Canon checks
        canon_warnings = []
        if "rewind" in task_description.lower() and actual_name.lower() == "ahdia":
            warning = "⚠ WARNING: Task mentions 'rewind' but Ahdia CANNOT rewind time!"
            print(f"\n{warning}")
            canon_warnings.append(warning)
            scene.canon_checks.append(warning)

        if "isaiah" in task_description.lower() or "bennett" in task_description.lower():
            if "tess" in actual_name.lower() and ("kill" in task_description.lower() or "murder" in task_description.lower()):
                warning = "⚠ WARNING: Tess does NOT kill Isaiah! Isaiah was killed by POLICE."
                print(f"\n{warning}")
                canon_warnings.append(warning)
                scene.canon_checks.append(warning)

        # Roll for task outcome
        roll_result = self.roll_dice(actual_name, difficulty)
        scene.dice_rolls["task"] = roll_result

        print(f"🎲 TASK ROLL: {roll_result['roll']} + {roll_result['competency']-5} (competency) = {roll_result['total']}")
        print(f"   Difficulty: {difficulty}")
        print(f"   Result: {'SUCCESS' if roll_result['success'] else 'FAILURE'}")
        if roll_result['critical_success']:
            print(f"   ⚡ CRITICAL SUCCESS!")
        if roll_result['critical_failure']:
            print(f"   💀 CRITICAL FAILURE!")

        # Determine outcome
        if roll_result['success']:
            scene.outcome = "success"
            print(f"\n✓ Task Outcome: SUCCESS")
        else:
            scene.outcome = "success_with_complication"
            print(f"\n⚠ Task Outcome: SUCCESS WITH COMPLICATION")

        # Determine cost
        cost_options = self._generate_cost_options(char, task_description, roll_result, month)
        scene.cost = random.choice(cost_options)
        print(f"\n💰 Cost Paid: {scene.cost}")

        # Update institutional tracks
        self._update_institutional_tracks(char, scene.cost, scene)

        # Express limitation
        limitation_shown = random.choice(char.limitations) if char.limitations else "Pushed beyond comfort zone"
        scene.limitation = limitation_shown
        print(f"\n🔒 Limitation Expressed: {limitation_shown}")

        # Check for consequence bleed
        if self.consequence_pool:
            applicable = [c for c in self.consequence_pool if c.get("month", 0) <= month]
            if applicable:
                consequence = random.choice(applicable)
                scene.narrative_beats.append(f"CONSEQUENCE BLEED: {consequence['description']}")
                print(f"\n🔗 Consequence Bleed: {consequence['description']}")
                self.consequence_pool.remove(consequence)

        # Add to scenes
        self.scenes.append(scene)

        print(f"\n{'='*60}")
        print(f"Scene generated successfully!")
        if canon_warnings:
            print(f"\n⚠ Canon warnings: {len(canon_warnings)}")
        print(f"{'='*60}")

        return scene

    def _generate_cost_options(self, char: Character, task: str, roll: Dict, month: int) -> List[str]:
        """Generate appropriate cost options based on character, task, and timeline"""
        costs = []

        # Physical costs
        costs.extend([
            "Physical exhaustion (needs rest afterward)",
            "Minor injury (bruised, strained)"
        ])

        # Emotional costs
        costs.extend([
            "Emotional toll (suppressed feelings surface)",
            "Anxiety spike (coping mechanisms activate)",
            "Depression worsens (isolation deepens)"
        ])

        # Relational costs
        costs.extend([
            "Team trust strained (someone questions judgment)",
            "Missed connection (someone needed them elsewhere)",
            "Relationship friction (good deed creates tension)"
        ])

        # Ahdia-specific costs
        if char.name == "Ahdia":
            costs.extend([
                "Lifespan burned (days/weeks lost)",
                "Powers strain (temporal degradation accelerates)"
            ])

            if month >= 6:
                costs.append("Treatment dependency deepens (Ruth/CADENS required)")
            if month >= 8:
                costs.append("Critically depleted (<10% baseline)")

        # Institutional costs (v4/v5)
        if char.has_institutional_role:
            costs.extend(COMPLICITY_COSTS)
            costs.extend(DEFIANCE_COSTS)

            # Character-specific institutional costs
            if char.name == "Ben" and month >= 4:
                costs.append("Evidence mounting but CADENS blocking release")
                if month >= 8:
                    costs.append("Perfect case built, watching it fail anyway")

            if char.name == "Tess" and month >= 6:
                costs.append("Father's complicity becoming undeniable")
                if month >= 8:
                    costs.append("Truth complete but system protects power")

            if char.name == "Leah" and month >= 5:
                costs.append("Silence = complicity (team trust damaged)")
                if month >= 8:
                    costs.append("Growth painful (two steps forward, one back)")

            if char.name == "Ruth" and month >= 6:
                costs.append("Hiding Ahdia's condition from CADENS (+1 Complicity)")
                if month >= 8:
                    costs.append("Lied to Bourn about treatment records (+1 Complicity)")

        # Tactical costs
        costs.extend([
            "Position exposed (enemies now aware)",
            "Resource depleted (can't do this again soon)"
        ])

        # Critical success/failure adjustments
        if roll.get('critical_success'):
            costs = ["Minimal cost (surprisingly smooth)", "Unexpected bonus (gained more than expected)"]

        if roll.get('critical_failure'):
            costs = [
                "Major injury (needs medical attention)",
                "Psychological break (coping mechanism fails)",
                "Team fracture (serious trust damage)",
                "Mission compromise (objective partially failed)"
            ]

        return costs

    def advance_month(self):
        """Move to next month, reset monthly counters"""
        if self.current_month < 12:
            self.current_month += 1

            # Reset monthly counters
            self.ahdia_powers.reset_monthly_counter()

            # Show upcoming events
            upcoming = self.key_events.get_upcoming_events(self.current_month)
            if upcoming:
                print(f"\n📅 Upcoming Events (Month {self.current_month}):")
                for event_key, event_data in upcoming[:3]:
                    print(f"   - {event_data['description']}")

            print(f"\n⏭ Advanced to Month {self.current_month}")
        else:
            print(f"\n⚠ Already at final month (12)")

    def show_character(self, character_name: str):
        """Display detailed character information"""
        char_key = None
        for key in self.characters.keys():
            if key.lower() == character_name.lower():
                char_key = key
                break

        if not char_key:
            print(f"\n✗ Character {character_name} not found")
            return

        char = self.characters[char_key]
        print(f"\n{'='*60}")
        print(f"CHARACTER: {char.name}")
        print(f"{'='*60}")
        print(f"Competency: {char.competency}/10")
        print(f"Current State: {char.current_state}")

        if char.canon_data:
            print(f"\n📖 Canon Data: Loaded from compact JSON")
            print(f"   Role: {char.canon_data.get('role', 'Unknown')}")
            print(f"   Arc: {char.canon_data.get('arc', 'Unknown')}")

        # Institutional role
        if char.has_institutional_role:
            print(f"\n⚖️ INSTITUTIONAL ROLE:")
            print(f"   Institution: {char.institutional_role.get('institution', 'Unknown')}")
            print(f"   Power: {char.institutional_role.get('power', 'Unknown')}")
            print(f"   Vulnerability: {char.institutional_role.get('vulnerability', 'Unknown')}")
            print(f"\n   TRACKS:")
            print(f"   Complicity: {char.complicity_track}/10")
            print(f"   Defiance: {char.defiance_track}/10")
            print(f"   Trajectory: {char.get_trajectory_summary()}")

            if char.reckoning_occurred:
                print(f"\n   🔥 RECKONING OCCURRED: {char.reckoning_choice.upper()}")

        # Special: Ahdia power status
        if char.name == "Ahdia":
            print(f"\n⚡ POWER STATUS:")
            print(f"   {self.ahdia_powers.get_status_summary()}")

        print(f"\nLimitations:")
        for lim in char.limitations:
            print(f"  - {lim}")

        # Show scenes
        char_scenes = [s for s in self.scenes if s.character == char_key]
        print(f"\nScenes: {len(char_scenes)}")
        if char_scenes:
            print(f"   Recent scenes:")
            for i, scene in enumerate(char_scenes[-3:], 1):
                markers = []
                if scene.institutional_impact == "complicity":
                    markers.append("+C")
                elif scene.institutional_impact == "defiance":
                    markers.append("+D")
                if scene.eidolon_active:
                    markers.append("Eidolon")
                marker_str = f" [{', '.join(markers)}]" if markers else ""
                print(f"   {i}. Month {scene.month}: {scene.task[:50]}{marker_str}...")

    def show_timeline(self):
        """Display scenes organized by month"""
        print(f"\n{'='*60}")
        print(f"BOOK 2 MASTER TIMELINE")
        print(f"{'='*60}")
        print(f"Current Month: {self.current_month}")
        print(f"Total Scenes Generated: {len(self.scenes)}\n")

        for month in range(1, 13):
            month_scenes = [s for s in self.scenes if s.month == month]
            summary = self.canon_loader.get_month_summary(month)

            title = summary.get("title", "") if summary else ""
            print(f"\nMONTH {month}: {title} ({len(month_scenes)} scenes)")

            if summary:
                key_events = summary.get("key_events", [])
                if key_events:
                    print(f"  Canon events: {', '.join(key_events[:2])}...")

            for scene in month_scenes:
                markers = []
                if scene.institutional_impact:
                    markers.append(f"+{scene.institutional_impact[0].upper()}")
                if scene.eidolon_active:
                    markers.append("E")
                marker_str = f" [{','.join(markers)}]" if markers else ""
                print(f"  - {scene.character}: {scene.task[:60]}{marker_str}...")

    def show_v5_status(self):
        """Display all v5 system statuses"""
        print(f"\n{'='*60}")
        print(f"V5 SYSTEMS STATUS - Month {self.current_month}")
        print(f"{'='*60}\n")

        # Ahdia Powers
        print("⚡ AHDIA POWER STATUS:")
        print(f"   {self.ahdia_powers.get_status_summary()}")
        print()

        # Public Opinion
        print("📊 PUBLIC OPINION:")
        print(f"   Kain Polling: {self.public_opinion.kain_polling:+d}")
        print(f"   Go Squad Reputation: {self.public_opinion.go_squad_reputation}/100")
        print()

        # Eidolon
        print("👁️ EIDOLON:")
        print(f"   Activity Level: {self.eidolon.activity_level}/10")
        print(f"   Targets: {', '.join(self.eidolon.current_targets) if self.eidolon.current_targets else 'None'}")
        print(f"   Resistance Trained: {', '.join(self.eidolon.resistance_practiced) if self.eidolon.resistance_practiced else 'None'}")
        print()

        # Investigations
        print("📋 INVESTIGATIONS:")
        convergence = self.investigations.check_convergence(self.current_month)
        print(f"   Convergence: {'YES (Month 6+)' if convergence else 'Not yet'}")
        for key, inv in list(self.investigations.investigations.items())[:4]:
            print(f"   {key}: {inv.progress}%")
        print()

        # Key Events
        upcoming = self.key_events.get_upcoming_events(self.current_month)
        if upcoming:
            print("📅 UPCOMING EVENTS:")
            for event_key, event_data in upcoming[:3]:
                print(f"   Month {event_data['month']}: {event_data['description'][:60]}...")

    def show_context(self):
        """Display complete Book 2 context"""
        print("\n" + "="*80)
        print(" " * 20 + "BOOK 2: PARAGON ANOMALY [DM v5]")
        print("="*80)

        print("\n📖 CORE STRUCTURE:")
        synopsis = self.canon_loader.compact_data.get("book_2_synopsis", {})
        print(f"  Timeline: {synopsis.get('timeline', '12 months')}")
        print(f"  Emotional Arc: {synopsis.get('emotional_arc', 'Unknown')}")
        print(f"  Thematic Arc: {synopsis.get('thematic_arc', 'Unknown')}")
        print(f"  POV: {synopsis.get('pov', 'Unknown')}")
        print(f"  Antagonist: {synopsis.get('antagonist', 'Unknown')}")

        print("\n🆕 V5 FEATURES:")
        print("  - Optimized JSON data loading (10-20x faster)")
        print("  - Eidolon influence tracking")
        print("  - Investigation progress system")
        print("  - Public opinion / polling tracker")
        print("  - Ahdia power / baseline tracker")
        print("  - Key events timeline")
        print("  - Complicity/Defiance mechanics (from v4)")

        print("\n" + "="*80)
        print("CRITICAL CANON REMINDERS")
        print("="*80)
        print("  ✓ Isaiah Bennett: Killed by POLICE (Officer Webb)")
        print("  ✗ Tess does NOT kill anyone - investigates killings")
        print("  ✓ Ahdia: FREEZE/ACCELERATE only (NO REWIND)")
        print("  ✓ Treatment: Ruth+Ryu only, prevents transcendence")
        print("  ✓ Kain: Clone avatar system (functionally immortal)")
        print("  ✓ TRIOMF: All investigations converge here (Month 6)")

        print("\n" + "="*80)
        print(f"DM STATE: Month {self.current_month} | {len(self.scenes)} scenes | v5.0")
        print(f"Ahdia: {self.ahdia_powers.baseline_percentage:.1f}% | Kain: {self.public_opinion.kain_polling:+d}")
        print("="*80 + "\n")

    def interactive_mode(self):
        """Run interactive DM session"""
        self.show_context()

        print("\n" + "="*60)
        print("TTRPG DUNGEON MASTER v5 - Interactive Mode")
        print("="*60)
        print("\nCommands:")
        print("  generate - Generate a new scene")
        print("  character <name> - View character details")
        print("  timeline - View full timeline")
        print("  status - View all v5 system statuses")
        print("  advance - Move to next month")
        print("  check - Check a canon fact")
        print("  context - Show Book 2 context again")
        print("  save - Save current state")
        print("  quit - Exit (auto-saves)")
        print("\nV5 System Commands:")
        print("  eidolon <level> - Set Eidolon activity level")
        print("  evidence <inv_key> <quality> - Add evidence to investigation")
        print("  polling <change> <reason> - Update Kain polling")
        print("  freeze <minutes> <context> - Track Ahdia power use")
        print()

        while True:
            try:
                cmd = input("\nDM> ").strip().lower()

                if cmd in ["quit", "exit"]:
                    self.save_state()
                    print("\nGoodbye!")
                    break

                elif cmd == "save":
                    self.save_state()

                elif cmd == "generate":
                    char_name = input("Character name: ").strip()
                    task = input("Task description: ").strip()
                    month_input = input(f"Month (1-12, default {self.current_month}): ").strip()
                    month = int(month_input) if month_input else self.current_month
                    difficulty_input = input("Difficulty (1-10, default 7): ").strip()
                    difficulty = int(difficulty_input) if difficulty_input else 7
                    eidolon_input = input("Eidolon active? (y/n, default n): ").strip().lower()
                    eidolon_active = eidolon_input == 'y'

                    self.generate_scene(char_name, task, month, difficulty, eidolon_active)
                    self.save_state()

                elif cmd.startswith("character "):
                    char_name = cmd[10:].strip()
                    self.show_character(char_name)

                elif cmd == "timeline":
                    self.show_timeline()

                elif cmd == "status":
                    self.show_v5_status()

                elif cmd == "advance":
                    self.advance_month()
                    self.save_state()

                elif cmd == "check":
                    query = input("Check canon fact: ").strip()
                    self.check_canon(query)

                elif cmd == "context":
                    self.show_context()

                elif cmd.startswith("eidolon "):
                    try:
                        level = int(cmd[8:].strip())
                        self.eidolon.set_activity_level(level)
                        print(f"✓ Eidolon activity set to {level}/10")
                        self.save_state()
                    except ValueError:
                        print("Usage: eidolon <0-10>")

                elif cmd.startswith("evidence "):
                    parts = cmd[9:].split()
                    if len(parts) >= 2:
                        inv_key = parts[0]
                        quality = parts[1]
                        desc = input("Evidence description: ").strip()
                        self.investigations.add_evidence(inv_key, desc, quality, self.current_month)
                        self.save_state()
                    else:
                        print("Usage: evidence <inv_key> <weak|strong|irrefutable>")

                elif cmd.startswith("polling "):
                    parts = cmd[8:].split(maxsplit=1)
                    if len(parts) >= 2:
                        try:
                            change = int(parts[0])
                            reason = parts[1]
                            self.public_opinion.update_kain_polling(change, reason, self.current_month)
                            self.save_state()
                        except ValueError:
                            print("Usage: polling <+/-N> <reason>")
                    else:
                        print("Usage: polling <+/-N> <reason>")

                elif cmd.startswith("freeze "):
                    parts = cmd[7:].split(maxsplit=1)
                    if parts:
                        try:
                            minutes = float(parts[0])
                            context = parts[1] if len(parts) > 1 else ""
                            result = self.ahdia_powers.freeze_time(minutes, self.current_month, context)
                            print(f"\n⚡ Ahdia burned {minutes} minutes")
                            print(f"   Baseline: {result['baseline_before']:.1f}% → {result['baseline_after']:.1f}%")
                            self.save_state()
                        except ValueError:
                            print("Usage: freeze <minutes> [context]")
                    else:
                        print("Usage: freeze <minutes> [context]")

                else:
                    print("Unknown command. Type 'quit' to exit.")

            except KeyboardInterrupt:
                print("\n\nInterrupted. Saving...")
                self.save_state()
                break
            except Exception as e:
                print(f"\nError: {e}")


def main():
    """Main entry point"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="TTRPG Dungeon Master v5")
    parser.add_argument("save_file", nargs="?", default="dm_state_v5.json",
                       help="Campaign save file (default: dm_state_v5.json)")
    parser.add_argument("--command", "-c",
                       help="Run single command and exit (e.g., 'status', 'advance', 'timeline')")

    args = parser.parse_args()

    dm = DungeonMaster(args.save_file)

    # Command-line mode
    if args.command:
        cmd = args.command.strip().lower()

        if cmd == "status":
            dm.show_v5_status()
        elif cmd == "timeline":
            dm.show_timeline()
        elif cmd == "advance":
            dm.advance_month()
            dm.save_state()
        elif cmd == "context":
            dm.show_context()
        elif cmd.startswith("character "):
            char_name = cmd[10:].strip()
            dm.show_character(char_name)
        else:
            print(f"Unknown command: {cmd}")
            print("Available: status, timeline, advance, context, character <name>")
            sys.exit(1)
    else:
        # Interactive mode
        dm.interactive_mode()


if __name__ == "__main__":
    main()
