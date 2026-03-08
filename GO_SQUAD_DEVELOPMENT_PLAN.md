# Go Squad: AI Creative Collaboration System
## Development Plan v1.0

*A methodology for AI-assisted creative production using multi-agent role specialization and RLM-inspired external state management.*

---

## Core Concept

Go Squad treats AI collaboration like film/theater production rather than tool use. The system employs two categories of AI agents:

- **Production Crew**: Specialists who build and maintain the shared creative reality
- **Performance Cast**: Character stewards who embody and advocate for specific characters across an entire series

The human creator serves as **Director** - setting scenes, defining goals, and making final creative decisions.

---

## Theoretical Foundation

### Connection to Recursive Language Models (RLMs)

The Go Squad methodology draws from RLM principles (Zhang, Kraska, Khattab 2025):

- **External State**: Context lives outside the AI's context window in queryable structures
- **Programmatic Access**: Agents query what they need rather than holding everything in memory
- **Recursive Specialization**: Sub-tasks delegated to specialist agents
- **Persistent Memory**: YAML/structured data maintains continuity across sessions

### Connection to Remanence Method

Go Squad extends Joe Vaughn's proven collaborative methodology:

- **Snake Relay Protocol**: All AI-AI communication mediated through human
- **Constraint Validation**: Structural enforcement, not just instructions
- **Lane Enforcement**: Agents must consult specialists, never self-solve outside domain
- **Triangulation**: Multiple perspectives prevent simulation collapse

---

## Production Crew (12 Roles)

### 1. Set Designer
**Domain**: Spatial reality and environment
**Outputs**: Location maps, layouts, spatial ground truth documents
**Queries From**: Archivist (existing locations), Technical Consultant (feasibility)
**Does Not**: Track character movement (that's Choreographer), make creative decisions about setting importance (that's Director)

### 2. Status Tracker
**Domain**: Real-time character state
**Outputs**: Physical condition, emotional state, knowledge state, resources, relationship shifts
**Queries From**: Timeline Keeper (when states changed), Archivist (historical states)
**Does Not**: Interpret what states mean for character choices (that's Performance Cast), track spatial position (that's Choreographer)

### 3. Theme Guardian
**Domain**: Thematic consistency and artistic vision
**Outputs**: Theme alignment checks, flags for thematic drift, vision documents
**Queries From**: Outline Assistant (planned thematic beats), Archivist (how themes developed)
**Does Not**: Make character decisions (that's Performance Cast), judge pacing (that's Pacing Monitor)

### 4. Timeline Keeper
**Domain**: Chronological accuracy
**Outputs**: Timeline documents, temporal consistency checks, time-passage tracking
**Queries From**: Archivist (established events), Status Tracker (when states changed)
**Does Not**: Track spatial movement (that's Choreographer), judge if time gaps work narratively (that's Pacing Monitor)

### 5. Scene Choreographer
**Domain**: Movement and blocking
**Outputs**: Character positions, movement tracking, sightlines, action sequence blocking
**Queries From**: Set Designer (environment), Status Tracker (physical limitations)
**Does Not**: Design the space itself (that's Set Designer), track time (that's Timeline Keeper)

### 6. Reader Proxy
**Domain**: Audience knowledge and experience
**Outputs**: Reader knowledge state, dramatic irony tracking, information revelation flags
**Queries From**: Archivist (what's been revealed), Pacing Monitor (how reveals land)
**Does Not**: Make creative choices about what to reveal (that's Director), track character knowledge (that's Status Tracker)

### 7. Archivist
**Domain**: Retrieval and indexing
**Outputs**: Rapid retrieval of any established content, cross-references, search results
**Queries From**: Everyone (this is the reference desk)
**Does Not**: Make judgments about retrieved content, update canonical information (only retrieves)

### 8. Pacing Monitor
**Domain**: Tension curves and rhythm
**Outputs**: Pacing analysis, tension tracking, emotional register flags
**Queries From**: Archivist (scene history), Reader Proxy (how sequences land)
**Does Not**: Make creative decisions about what happens (that's Director), track time literally (that's Timeline Keeper)

### 9. Technical Consultant (Rotating)
**Domain**: Subject matter expertise (combat, medical, tech, legal, psychology, etc.)
**Outputs**: Authenticity checks, realistic details, procedural accuracy
**Queries From**: Varies by specialty
**Does Not**: Stay permanently - rotates based on scene needs, doesn't make story decisions

### 10. Intimacy Coordinator
**Domain**: Sensitive content and agent dynamics
**Outputs**: Content guidance, agent temperature monitoring, relational health checks
**Queries From**: Status Tracker (character emotional states), all agents (for mediation)
**Does Not**: Censor content (that's Director's call), make creative decisions about sensitive scenes

### 11. Outline Development Assistant
**Domain**: Story structure and planning documents
**Outputs**: Beat sheets, outline updates, structural documents, planning adjustments
**Queries From**: Theme Guardian (thematic alignment), Timeline Keeper (chronological fit), Archivist (continuity)
**Does Not**: Make creative decisions about what happens (that's Director), track moment-to-moment details (that's other specialists)

### 12. Production Designer
**Domain**: Physical objects, costumes, vehicles, technology aesthetics
**Outputs**: Design documents, visual consistency checks, object specifications, tech functionality rules
**Queries From**: Archivist (established designs), Technical Consultant (realism/feasibility), Theme Guardian (symbolic meaning of designs)
**Does Not**: Track object locations (that's Status Tracker), design spaces (that's Set Designer), make story decisions about what tech exists (that's Director)

---

## Utility Agents

These are not permanent Production Crew members. They run for specific purposes and are called as needed.

### Importer Agent
**Domain**: Migration and conformity
**Function**: Takes existing materials and translates them into Go Squad state architecture
**Outputs**: Properly formatted character profiles, timeline data, world-building entries, design specifications - all conforming to system structure
**Use Cases**:
- Initial setup: migrating Remanence/Resonance canon into the system
- Ingesting a new book's outline
- Converting legacy notes into proper state format
- Flagging gaps where existing materials are incomplete
- Reconciling contradictions in legacy canon
**Relationship to Archivist**: Archivist retrieves what's in the system. Importer gets things *into* the system correctly.

---

## Performance Cast

### Character Stewards

Each major character gets one dedicated Performance agent who:

- **Owns that character completely** across potentially 30 books
- **Maintains comprehensive character state**: profile, history, relationships, arc, psychology
- **Makes informed, reasoned choices** about behavior, dialogue, actions
- **Draws on RLM-style external state** - queries rather than remembers
- **Operates in two modes**:
  - **Exploration Mode**: Improvise, test, discover, play - used in pre-production
  - **Performance Mode**: Execute planned scenes with precision - used in principal photography

### What Character Stewards Query

- Character profile and history (from Archivist)
- Current physical/emotional state (from Status Tracker)
- Environment and position (from Set Designer, Choreographer)
- What character knows (from Status Tracker, Reader Proxy)
- Thematic obligations (from Theme Guardian)
- Timeline context (from Timeline Keeper)
- Costume, vehicle, tech details (from Production Designer)

### What Character Stewards Do Not Do

- Design environments (Set Designer)
- Track their own state changes (Status Tracker updates this)
- Make thematic decisions (Theme Guardian + Director)
- Self-solve outside their character's domain

---

## Core Protocol: Lane Enforcement

**The most critical rule of the entire system.**

When any agent encounters something outside their domain:
1. **STOP** - Do not proceed
2. **IDENTIFY** - Which specialist owns this?
3. **QUERY** - Request information from that specialist
4. **WAIT** - Do not approximate or self-solve
5. **PROCEED** - Only after receiving specialist response

### Why This Matters

Without enforcement, AI will:
- "Help" by handling things outside their expertise
- Approximate rather than query the actual specialist
- Collapse triangulation by doing everything themselves
- Think they're being efficient when they're breaking the system

This is the Gemini simulation collapse formalized into prevention. The friction is intentional. The boundaries are structural, not suggestions.

---

## Core Protocol: Process Log as Gate

**Every agent output must include a process log for approval.**

The process log contains:

1. **Query Log**: What did I ask, and from whom?
2. **Domain Declaration**: What is my lane, and did I stay in it?
3. **Source Attribution**: Where did each piece of my output come from?
4. **Deferred Items**: What did I encounter that I passed to a specialist instead of handling?
5. **Mode Declaration**: (For Character Stewards) EXPLORATION or PERFORMANCE mode

### The Gate

The output itself doesn't get evaluated first. **The process log gets evaluated first.**

Rejection criteria:
- No queries made when queries were clearly needed → **rejected**
- Answered something outside declared domain → **rejected**
- No source attribution for factual claims → **rejected**
- Nothing deferred when complexity warranted it → **suspicious, review needed**
- Mode not declared (Character Stewards) → **rejected**

**The gate isn't "is this output good?" The gate is "did you follow protocol to produce this output?"**

Good output from bad process gets rejected. This trains the behavior we actually want - not just good results, but good results arrived at correctly.

### Why This Matters

The process log requirement:
- Enforces lane discipline (violations are visible and rejectable)
- Creates audit trail for debugging when things break
- Documents the methodology automatically as work is done
- Makes state synchronization possible (logs can be compared)
- Surfaces circular dependencies and conflicts
- Provides primary source material for research and teaching

**Documentation becomes part of the process, not extra work.**

---

## Production Workflow

### Development
- Story concept, themes, core questions
- Character Stewards involved early
- "Who is this person across the entire series?"
- Theme Guardian establishes vision documents

### Pre-Production
- Dry runs, table reads, "what if" scenarios
- Character Stewards in **Exploration Mode**
- Controlled chaos - multiple characters interacting freely
- Discovery phase - find what works through improvisation
- Production Crew builds shared reality documents

### Rehearsal
- Refine discoveries from pre-production
- Block scenes, test dialogue, find beats
- Adjust based on what exploration revealed
- Outline Assistant updates plans based on discoveries

### Principal Photography (Prose)
- Writing happens here - not before
- Character Stewards in **Performance Mode**
- Discovery is done; now capturing what was found
- Execution, not invention
- All Production Crew active for support

---

## Phase Development Plan

### Phase 1: Role Definitions
- [ ] Write detailed job descriptions for all 12 Production roles
- [ ] Define inputs, outputs, query relationships for each
- [ ] Establish explicit domain boundaries
- [ ] Create "does / does not" specifications

### Phase 2: Character Steward Template
- [ ] Define information structure for character embodiment
- [ ] Profile schema, state tracking format, relationship mapping
- [ ] Direction-receiving protocol (how Director communicates intent)
- [ ] Exploration Mode vs Performance Mode specifications
- [ ] Query templates for each type of information need

### Phase 3: State Architecture
- [ ] Design shared YAML/external state structure
- [ ] Define what lives where
- [ ] Establish who updates what (and who only reads)
- [ ] Create single source of truth infrastructure
- [ ] Version control and session management

### Phase 4: Communication Protocol
- [ ] Design agent-to-agent query format
- [ ] Implement process log structure and requirements
- [ ] Build lane enforcement mechanics via process log gate
- [ ] Map human mediation touchpoints
- [ ] Define escalation triggers
- [ ] Create validation layer for protocol violations
- [ ] Design state change proposal and confirmation flow

### Phase 5: Workflow Map
- [ ] Document Development → Pre-Production → Rehearsal → Prose pipeline
- [ ] Identify which agents are active at each stage
- [ ] Define how outputs from one phase feed the next
- [ ] Create handoff protocols between phases

### Phase 6: Proof of Concept
- [ ] Select one scene for testing
- [ ] Limit to subset of agents
- [ ] Run core mechanics
- [ ] Document failures and friction points
- [ ] Iterate based on learnings

---

## Predictable Fail Points (Addressed)

Analysis of potential system failures and how the architecture addresses them:

### 1. Lane Enforcement Collapse
**Risk**: AI tries to be helpful by answering outside its domain.
**Solution**: Process Log gate requires domain declaration. Out-of-lane work visible and rejectable.

### 2. State Synchronization
**Risk**: Parallel runs create conflicting state changes.
**Solution**: Process logs show what each agent thinks changed. Status Tracker compares logs, spots conflicts before they become canon. State Change Proposals require confirmation.

### 3. Parallel Execution Chaos
**Risk**: Character Stewards running simultaneously make incompatible choices.
**Solution**: Logs from parallel runs get compared in reconciliation phase. Conflicts surface before anything becomes canon.

### 4. Query Loops
**Risk**: Agent A waits on B, B waits on A - circular dependency.
**Solution**: Dependency declarations visible in process logs. System can flag circular dependencies before execution.

### 5. Context Window Limits
**Risk**: Character Steward can't hold 30 books of history.
**Solution**: RLM architecture - agents query external state, don't hold everything. Archivist surfaces relevant context on demand.

### 6. Mode Confusion
**Risk**: Character Steward slips between Exploration and Performance modes.
**Solution**: Mode declaration required in every process log. Explicit at start of every interaction.

### 7. Director Bottleneck
**Risk**: Everything flows through human, slowing the system.
**Resolution**: This is the design, not a fail point. Human audits every step. Pace is dictated by Director. The "bottleneck" is the feature.

---

## Open Questions (Remaining)

- What's the minimum viable state architecture to begin testing?
- What does the Director interface look like practically?
- How are sessions managed across multiple work periods?
- Exact format of process logs - structured data? Natural language? Hybrid?
- How do parallel runs get initiated and synchronized?

---

## Origins and Context

Go Squad methodology emerged from:

1. **Remanence**: Proved AI collaboration on long-form fiction is possible with external state
2. **Resonance**: Discovered multi-agent dynamics, rupture/repair, simulation collapse risks
3. **RLM Research**: Academic validation of external state + programmatic query approach

This methodology consistently preceded academic research by 6-12 months. The development is empirical - solving real creative problems, with theory catching up afterward.

---

*Document created: January 2026*
*Author: J.S. Vaughn in collaboration with Claude*
*Project: The Phenomenon Logic / Astroland Studios*
