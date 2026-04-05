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

### Milestone 1: Snapshot Foundation

Exit criteria:

- deterministic ID strategy is implemented in authored content,
- the initial snapshot schema exists,
- the seed-memory pack covers the MVP rooms, rules, hooks, and NPCs,
- import validation exists.

### Milestone 2: Memory-Driven Runtime Core

Exit criteria:

- the orchestrator can retrieve authored state by room, phase, and NPC,
- runtime writes preserve authored baseline,
- relationship and clue deltas persist across scenes,
- recap inputs can be generated from stored state.

### Milestone 3: Text-First Client MVP

Exit criteria:

- the client accepts keyboard input,
- transcript scrollback works,
- recap/help affordances exist,
- day-night transitions are legible in presentation.

### Milestone 4: Playable Vertical Slice

Exit criteria:

- inheritance setup is playable,
- arrival flow works,
- daytime exploration works,
- first-night shift fires reliably,
- Thomas functions as the emotional anchor,
- outside-danger boundary is taught in fiction,
- morning-after endpoint closes the slice cleanly.

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
2. Confirm snapshot schema and seed-pack readiness.
3. Confirm architecture contracts.
4. Begin runtime implementation only after the above are stable.

## Verification Checklist

- Milestones are ordered from planning to playable slice.
- The roadmap does not pretend later acts are part of the MVP.
- Risks map to concrete mitigations.
- The review order reinforces planning before runtime.
