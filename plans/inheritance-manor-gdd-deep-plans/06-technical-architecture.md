# Technical Architecture

## Purpose

Define the framework-neutral runtime architecture for The Inheritance Manor after the vertical-slice content, memory rules, and authored snapshot boundaries are explicit.

## Architectural Rule

Keep the repository documentation-first until the authored seed pack and milestone gates are satisfied. The implementation architecture must preserve a thin, replaceable player-facing client; make the AI Game Master the only layer that interprets content rules and turn flow; treat the memory server as the canonical state authority for authored and runtime records; and preserve auditability through explicit prompts, retrieval order, and write rules.

## Proposed Repository Structure For Later Implementation

The repository should remain planning- and documentation-first for now, with later implementation organized around three runtime layers:

- a client layer for player interaction and presentation,
- an AI Game Master layer for orchestration and narrative rule enforcement,
- a memory layer that stores authored and runtime records as the canonical state authority.
## Three-Layer Model

### Layer 1: Client

The client is a text-first interaction surface for the player.

Responsibilities:

- render transcript output, room descriptions, recap summaries, and choice prompts,
- capture player input and accessibility preferences,
- display session state such as current phase, location, and recent recap,
- avoid embedding game truth or hidden world rules.

Non-responsibilities:

- direct narrative arbitration,
- direct authored-state mutation,
- interpretation of contradiction rules, loop telemetry, or distillation thresholds.

### Layer 2: AI Game Master

The AI Game Master is the orchestration layer that turns authored content plus runtime memory into the next playable response.

Responsibilities:

- assemble scene context using the retrieval priorities from `04-systems-memory-model.md`,
- enforce narrative and safety rules from the phase, world, and NPC planning docs,
- decide when a player action causes phase advancement, clue discovery, relationship deltas, loop response, or recap creation,
- translate stable state into transcript and interaction output for the client,
- write runtime changes back through explicit memory operations.

Non-responsibilities:

- becoming the long-term source of truth for world state,
- silently inventing authored content missing from the snapshot,
- allowing prompt-only memory to replace stored recap or relationship state.

### Layer 3: Memory Server

The memory server stores both the authored campaign snapshot and runtime playthrough mutation.

Responsibilities:

- preserve authored IDs, tags, district placement, and connections,
- isolate runtime records by playthrough or session lineage so one run cannot pollute another run's retrieval context,
- store runtime deltas for relationships, clues, recap summaries, and loop telemetry,
- support deterministic retrieval by project, tag, district, and stable IDs,
- expose write, connect, retrieval, and validation operations that the AI Game Master can audit.

Non-responsibilities:

- formatting player-facing transcript output,
- resolving ambiguous player intent,
- choosing UI behavior.

## Runtime Flow

1. Import the authored snapshot for `project_id: yorkz` before the first playable session.
2. Load campaign, phase, room, NPC, rule, and relationship anchors using the retrieval order defined in the systems doc.
3. Accept a player action from the client.
4. Let the AI Game Master classify the action against current phase goals, room state, clue conditions, and relationship triggers.
5. Write any resulting runtime deltas to the memory server.
6. Render transcript output, updated affordances, and recap-ready state back to the client.
7. Repeat until the session reaches a recap or save boundary.

## Interface Contracts

### Client To AI Game Master Contract

Minimum turn input:

- `session_id`
- `project_id`
- current player input text
- optional accessibility preferences
- optional last-seen recap ID or current phase hint

Minimum turn output:

- transcript text
- available actions or input affordance guidance
- current phase ID
- current location tag or anchor ID
- memory-write summary for audit tooling
- recap trigger flag when applicable

### AI Game Master To Memory Server Contract

Required reads:

- campaign metadata node
- current phase anchor
- current room state anchor
- present NPC anchors
- unresolved clue anchors for the current context
- relationship baselines plus relevant deltas
- recap and loop telemetry nodes when repetition or resume context matters

Required runtime scoping:

- every mutable runtime record must carry a canonical `lineage_id` field in addition to `project_id`; `lineage_id` is the stable string identifier for the active playthrough/session lineage defined in `04-systems-memory-model.md`,
- `lineage_id` is the contract-level runtime scope key; tags or ID prefixes may be added for convenience, but they are not a substitute for the `lineage_id` field and must not be the only lineage representation,
- authored anchors remain shared and are not filtered by `lineage_id`, but runtime retrieval must filter by both `project_id` and `lineage_id = active_lineage_id` unless a recap, comparison, or audit flow explicitly asks for historical runs,
- recap generation and session resume must use `lineage_id = active_lineage_id` as the default boundary and only widen scope when the prompt or API call explicitly requests cross-lineage history.

Required writes:

- major player-decision nodes
- relationship deltas
- clue discovery nodes
- phase-transition nodes
- day/night state-transition nodes
- loop telemetry nodes
- recap nodes
- objective or obligation changes when the current slice meaningfully shifts
- distilled insight nodes when distillation rules are met

### Snapshot Import Contract

The initial import path must honor the authored snapshot rules defined in `07-content-pipeline-and-snapshots.md`:

- preserve authored IDs,
- keep `project_id: yorkz` on all authored entries,
- merge declared connections,
- reject runtime-only records in authored import content.

## Prompt And Tooling Policy

1. Prompts may interpret authored content, but must not redefine authored canon during play.
2. The AI Game Master should use explicit retrieval and write steps instead of relying on hidden conversation memory.
3. Any rule that affects continuity must map back to a stored node, tag family, or documented phase rule.
4. Tool usage should stay bounded and explainable: retrieve relevant anchors, write explicit deltas, connect related runtime nodes when the system model requires it.
5. Recap generation must be reproducible from stored state and not depend on unstored prompt residue.

## Framework Decision Policy

The client framework remains deferred.

Current decision:

- commit only to a text-first, keyboard-operable client contract,
- allow CLI, terminal UI, or lightweight web client implementation later,
- do not let framework preference alter the underlying turn contract, memory model, or authored snapshot shape.

This keeps the architecture stable while the repository is still proving the campaign slice, authored seed pack, and AI Game Master interaction loop.

## Testing Surfaces

### Documentation Validation

- heading and keyword checks for planning docs,
- snapshot schema checklist validation,
- cross-document consistency review between narrative, world, NPC, systems, and roadmap docs.

### Snapshot Validation

- every authored node has a deterministic ID,
- every authored node carries `project_id: yorkz`,
- required MVP categories exist before runtime import,
- runtime-only records are rejected during authored import.

### AI Game Master Validation

- scene assembly follows retrieval priority order,
- rule enforcement respects day/night boundaries and outside danger rules,
- runtime retrieval is filtered to the active playthrough lineage,
- recap output can be regenerated from stored state,
- repeated ineffective actions trigger loop-telemetry-aware responses instead of flat retries.

### Client Validation

- transcript and interaction affordances are readable in a text-first interface,
- current phase and room context remain visible without hidden UI state,
- a session can resume from recap-ready stored memory without ad hoc reconstruction.

## Verification Checklist

- The three-layer architecture is explicit.
- Client, AI Game Master, and memory server responsibilities are separated.
- Interface contracts define minimum reads, writes, and turn payloads.
- Prompt and tooling policy preserves auditability.
- The framework decision remains deferred while the client contract stays explicit.
- Testing surfaces cover documentation, snapshot import, orchestration, and client behavior.
