# Go Squad Agent System

Multi-agent templates for AI-assisted fiction production.

## Directory Structure

```
_tools/agents/
├── README.md
├── templates/
│   ├── production_crew/
│   │   ├── set_designer.yaml
│   │   ├── status_tracker.yaml        ✓ Tested
│   │   ├── theme_guardian.yaml
│   │   ├── timeline_keeper.yaml
│   │   ├── scene_choreographer.yaml
│   │   ├── reader_proxy.yaml
│   │   ├── archivist.yaml
│   │   ├── pacing_monitor.yaml
│   │   ├── technical_consultant.yaml
│   │   ├── intimacy_coordinator.yaml
│   │   ├── outline_assistant.yaml
│   │   ├── production_designer.yaml
│   │   └── character_steward.yaml     ✓ Tested (consultation flow)
│   └── meta/
│       └── enforcer.md                ✓ NEW - Process validation gate
```

## Using Templates

### Manual Mode (No API Required)

1. Open the template file
2. Copy the `system_prompt` section
3. Paste into a Claude session (Claude.ai, Claude Code, API playground)
4. Provide your task
5. Validate the process log in the response

### Automated Mode (Requires API)

```python
# Future orchestrator.py usage
from orchestrator import GoSquadOrchestrator

orch = GoSquadOrchestrator()
result = orch.run_agent(
    role="status_tracker",
    task="Update Ahdia's emotional state after Chapter 5",
    context={"chapter": 5, "character": "ahdia"}
)
```

## Template Structure

Each template YAML contains:

| Section | Purpose |
|---------|---------|
| `system_prompt` | Full prompt for manual/automated use |
| `role_definition` | Machine-readable role spec |
| `state_access` | What files the agent can read/write |
| `process_log_requirements` | Validation rules (if detailed) |

## Production Crew Roles (12)

| # | Role | Domain | Template |
|---|------|--------|----------|
| 1 | Set Designer | Spatial reality, environments | ✓ |
| 2 | Status Tracker | Character state (physical, emotional, knowledge) | ✓ Tested |
| 3 | Theme Guardian | Thematic consistency, artistic vision | ✓ |
| 4 | Timeline Keeper | Chronological accuracy | ✓ |
| 5 | Scene Choreographer | Movement and blocking | ✓ |
| 6 | Reader Proxy | Audience knowledge, dramatic irony | ✓ |
| 7 | Archivist | Retrieval and indexing (read-only) | ✓ |
| 8 | Pacing Monitor | Tension curves and rhythm | ✓ |
| 9 | Technical Consultant | Subject matter expertise (rotating) | ✓ |
| 10 | Intimacy Coordinator | Sensitive content, agent dynamics | ✓ |
| 11 | Outline Assistant | Story structure, planning documents | ✓ |
| 12 | Production Designer | Objects, costumes, vehicles, tech | ✓ |

## Performance Cast

| Role | Domain | Template |
|------|--------|----------|
| Character Steward | Character embodiment (one per major character) | ✓ Tested (Ahdia) |

## Meta-Agents

Meta-agents operate on the system itself, not on story content.

| Role | Domain | Template | Status |
|------|--------|----------|--------|
| **Enforcer** | Process validation | `meta/enforcer.md` | ✓ NEW |

### Enforcer

The Enforcer is the **gate** between agent output and Director review. No agent output proceeds without validation.

**Validates:**
- Query log present and appropriate to task
- Domain declaration present and accurate
- Source attribution for all factual claims
- Deferrals made when out-of-lane content encountered
- Mode declared (for Character Stewards)

**Outputs:**
- `APPROVED` - Output proceeds to Director
- `REJECTED + reason` - Agent must redo
- `FLAGGED + concern` - Director reviews before accepting

## Validated Consultation Flow

Tested: Status Tracker → Character Steward

```
Status Tracker output:
  DEFERRED ITEMS:
    → character_steward: How this emotional state manifests in behavior
      Reason: Behavioral choices are Character Steward domain

Character Steward receives:
  DEFERRAL RECEIVED:
    From: status_tracker
    Item: "How this emotional state manifests in behavior"
    State provided: [state data passed along]
```

**Key finding:** Consultation chains are valid. Character Steward may further consult Theme Guardian ("Does this serve the arc?"). Process logs track the full chain.

## Validation Rules

The **Enforcer** meta-agent validates process logs before output reaches Director.

**REJECT if:**
- Query log empty when queries needed
- Domain declaration missing
- Source attribution missing for facts
- Task outside declared domain
- (Character Steward) Mode not declared

**FLAG if:**
- All sources from memory
- Complex operation with no deferrals
- Low confidence without explanation

See `templates/meta/enforcer.md` for full validation protocol.

## Quick Test

```bash
# Extract any agent's system prompt
python3 -c "
import yaml
with open('templates/production_crew/status_tracker.yaml') as f:
    print(yaml.safe_load(f)['system_prompt'])
"
```

## Manuscript Build Tool

```bash
# Generate DOCX from chapter .txt files (renumbered, formatted for Dabblewriter)
cd 6_manuscript/book_2/
python3 build_docx.py
```

Output: `Book2_Manuscript.docx` — 20 chapters, renumbered sequentially, italics converted, scene breaks as `*   *   *`, STRUCT comments stripped, Times New Roman 12pt.

Rebuild after any prose edits to keep DOCX current.

## Next Steps

1. **API Orchestrator** - `orchestrator.py` to load templates, inject state, call API
2. **Director CLI** - `director_cli.py` for task initiation and gate review
3. **More Character Stewards** - Templates for other major characters
