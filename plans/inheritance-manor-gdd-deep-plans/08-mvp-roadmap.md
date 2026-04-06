# MVP Roadmap

## Purpose

Turn the validated prologue-plus-first-night slice into milestone exits that are concrete enough to execute and review.

## MVP Definition

The MVP is complete when a player can:

- receive the inheritance premise,
- arrive at the manor through a coherent grounded route,
- meet at least one day authority frame,
- explore the MVP room set,
- survive the first shift,
- meet Thomas in the shifted manor,
- learn that outside is unsafe at night,
- and reach morning with unresolved pressure to continue.

## Milestones

### Milestone 0: Planning Packet Complete

Exit criteria:

- deep-planning docs 01 through 08 exist,
- the packet is internally consistent,
- authored snapshot boundaries are explicit,
- the repository has an implementation-ready planning baseline.

Primary evidence:

- `plans/inheritance-manor-gdd-deep-plans/*.md` form a coherent packet,
- the roadmap does not expand MVP scope beyond prologue plus first night.

Validation expectations:

- cross-check the roadmap against the gap-analysis, systems, snapshot, and architecture docs,
- confirm that no milestone assumes a locked client framework or post-MVP campaign content,
- verify that authored-versus-runtime separation is named before any runtime milestone.

### Milestone 1: Memory System Foundation

Exit criteria:

- the memory-system contract supports authored and runtime records without allowing one to overwrite the other,
- deterministic authored IDs and canonical tag validation are enforced,
- retrieval supports room, phase, NPC, and district-oriented queries,
- snapshot import/export primitives and graph traversal exist for later content and runtime use.

Primary evidence:

- `src/yorkz/memory_system.py` implements the core record, search, traversal, and snapshot behavior,
- `tests/test_memory_system.py` covers authored/runtime protection, search, traversal, and snapshot round-trips.

Validation expectations:

- run `pytest tests/test_memory_system.py` and keep the suite green,
- confirm authored records cannot be replaced by runtime records,
- confirm snapshot round-trips preserve authored records and expected connections.

### Milestone 2: Content Pipeline And Snapshot Readiness

Exit criteria:

- deterministic ID strategy is implemented in authored content,
- the authored snapshot schema exists as a canonical file contract,
- the seed-memory pack covers the MVP rooms, rules, hooks, clues, and NPC anchors,
- authored import validation rejects malformed or runtime-only content,
- production snapshot loading is separated from draft authoring references.

Primary evidence:

- `campaigns/inheritance-manor/prologue-snapshot.json` is the required canonical authored seed-pack path for Milestone 2 once the content pipeline lands,
- `docs/initial drafts/draft-inheritance-manor-memories.json` remains a planning mirror rather than the runtime import target,
- content-pipeline code provides validation, loading, and export support for authored snapshot content against that canonical artifact.

Validation expectations:

- verify the canonical seed pack contains the MVP categories required by the systems and snapshot docs,
- validate snapshot loading and authored export behavior through targeted tests,
- confirm runtime-only entries are rejected during authored import.

### Milestone 3: Technical Architecture Contract

Exit criteria:

- the three-layer split between client, AI Game Master, and memory server is explicit,
- the player-facing client contract stays text-first and keyboard-operable without locking a framework,
- the AI Game Master is defined as an orchestration layer over explicit memory state,
- MCP integration rules are auditable through explicit retrieval order, write rules, and runtime lineage scope.

Primary evidence:

- `plans/inheritance-manor-gdd-deep-plans/06-technical-architecture.md` names the layer boundaries, runtime flow, and validation surfaces,
- architecture decisions preserve authored/runtime separation and active-lineage filtering.

Validation expectations:

- confirm the architecture doc does not smuggle in prompt-only truth or hidden state,
- confirm runtime scoping, auditability, and authored import constraints are spelled out,
- confirm the repository remains documentation-first until milestone 1 and milestone 2 inputs are stable.

### Milestone 4: Playable Vertical Slice

Exit criteria:

- inheritance setup is playable,
- arrival flow works,
- daytime exploration works,
- first-night shift fires reliably,
- Thomas functions as the emotional anchor,
- outside-danger boundary is taught in fiction,
- morning-after endpoint closes the slice cleanly,
- the integrated runtime preserves relationship, clue, and recap continuity across the slice.

Primary evidence:

- the runtime stack can execute a complete prologue-plus-first-night run,
- recap and continuity outputs are drawn from stored state rather than hand-waved prompt context.

Validation expectations:

- complete a representative playable pass from inheritance notice through morning after,
- confirm day/night transitions, relationship deltas, clue persistence, and recap outputs survive the slice,
- confirm the integrated system still respects authored/runtime boundaries.

## Milestone Sequencing

| Milestone | Depends on | Current scope | Linked issue thread |
| --- | --- | --- | --- |
| 0. Planning Packet Complete | none | canonical planning baseline | planning packet |
| 1. Memory System Foundation | Milestone 0 | storage, search, traversal, snapshot primitives | issue #9 |
| 2. Content Pipeline And Snapshot Readiness | Milestone 1 | canonical seed pack, authored validation, import/export discipline | issue #10 |
| 3. Technical Architecture Contract | Milestone 0, Milestone 1, Milestone 2 | layer boundaries, client contract, auditable MCP orchestration rules | issue #11 |
| 4. Playable Vertical Slice | Milestone 1, Milestone 2, Milestone 3 | integrated prologue-plus-first-night runtime | future slice implementation |

Documentation-first rule:

- The repository should not treat milestone 4 as active implementation work until milestone 1, milestone 2, and milestone 3 have all cleared their validation gates.
- Framework selection remains deferred until the technical-architecture contract and authored content inputs are stable enough to protect the runtime from churn.

## Backlog After MVP

- additional rooms beyond the MVP set,
- broader night staff roster,
- deeper detective and lawyer branching,
- Acts II and III content,
- campaign-authoring tools and snapshot packaging improvements.

## Primary Risks

| Risk | Mitigation |
| --- | --- |
| Architecture debate delays content progress | Keep framework choice deferred until snapshot and orchestrator contracts are explicit |
| Snapshot drift contaminates runtime state | Validate authored/runtime separation before runtime coding |
| Narrative ambiguity becomes confusion | Preserve bounded ambiguity rules and clear clue progression |
| Long-session continuity fails | Build recap as a first-class output from stored state |

## Review Order

1. Confirm planning packet consistency.
2. Confirm memory-system gates pass on the active base branch.
3. Confirm snapshot schema, seed-pack readiness, and authored import validation.
4. Confirm architecture contracts and documentation-first stop conditions.
5. Begin vertical-slice runtime implementation only after the above are stable.

## Milestone Gate Checks

### Gate 0: Planning complete

- `rg "MVP Roadmap|Documentation Before Runtime|authored|runtime" plans/inheritance-manor-gdd-deep-plans docs/GDD`
- manual consistency review across docs 01 through 08.

### Gate 1: Memory-system complete

- `pytest tests/test_memory_system.py`
- verify authored/runtime overwrite protection and snapshot round-trip behavior.

### Gate 2: Content-pipeline complete

- validate the canonical authored snapshot and confirm required MVP anchors exist,
- run the snapshot-focused tests once the content-pipeline implementation lands on the active branch.

### Gate 3: Architecture contract complete

- confirm the architecture doc still defers framework choice,
- confirm retrieval order, runtime lineage, and explicit write rules are spelled out.

### Gate 4: Vertical-slice complete

- execute an end-to-end playable pass,
- verify recap continuity, relationship persistence, clue progression, and the inside-versus-outside safety rule.

## Verification Checklist

- Milestones are ordered from planning to playable slice.
- Milestone names and sequencing match the real implementation slices: memory system, content pipeline, architecture, then playable slice.
- Gating criteria for each milestone are concrete enough to test or manually verify.
- Validation expectations exist for every milestone.
- The roadmap does not pretend later acts are part of the MVP.
- Risks map to concrete mitigations.
- The review order reinforces planning before runtime.
