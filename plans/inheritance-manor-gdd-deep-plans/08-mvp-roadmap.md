# MVP Roadmap

## Purpose

Turn the validated planning packet for The Inheritance Manor into milestone gates that move the project from documentation-first design to a playable prologue-and-first-night vertical slice.

## MVP Definition

For this repository, MVP means:

- the player can enter the prologue and first-night slice,
- the authored snapshot provides the required baseline world state,
- the AI Game Master can retrieve, interpret, and write state against the documented rules,
- the client can present the experience as a coherent text-first session,
- the morning-after boundary produces a recap-ready continuation point.

## Roadmap Principles

1. Complete planning before implementation scaffolding expands.
2. Treat authored snapshot readiness as a hard gate, not a nice-to-have.
3. Validate the memory contract and the game loop before polishing delivery surfaces.
4. Keep backlog expansion out of the MVP critical path.

## Milestone 0: Planning Packet Complete

Goal: finish the documentation packet so later implementation work targets stable contracts.

Exit criteria:

- `01` through `08` planning docs exist and are internally consistent.
- Vertical-slice scope is locked to prologue through the morning after the first shift.
- Authored-versus-runtime state boundaries are explicit.
- Three-layer architecture and deferred framework policy are documented.

Verification:

- Run `git diff --check` with no issues.
- Verify architecture and roadmap headings with targeted `rg` commands.
- Confirm the planning docs still agree on scope, room set, cast, and memory rules.

## Milestone 1: Author The Seed Snapshot Pack

Goal: replace the empty draft memory scaffold with the minimum authored campaign pack required for runtime play.

Exit criteria:

- campaign metadata node exists,
- six phase anchors exist,
- MVP room and room-state anchors exist,
- Thomas, detective, and lawyer anchors exist,
- relationship baseline anchors exist,
- plot hooks, rule anchors, the authored first-shift trigger, recap templates, and the minimal clue chain exist,
- all authored nodes use deterministic IDs and `project_id: yorkz`.

Verification:

- Validate the snapshot against the checklist in `07-content-pipeline-and-snapshots.md`.
- Reject any authored pack containing runtime-only records.
- Confirm the seed pack can be imported without ID drift.

## Milestone 2: Build The Runtime Skeleton

Goal: implement the minimal runtime path that can import authored state, assemble a scene, accept player input, and persist the first deltas.

Exit criteria:

- a thin text-first client can send player turns,
- the AI Game Master can retrieve current scene context deterministically,
- runtime writes persist player decisions, relationship changes, clue changes, phase changes, and day/night transitions,
- runtime storage isolates mutable records by playthrough lineage,
- resume and recap boundaries are represented in stored state.

Verification:

- Run an end-to-end dry session from arrival into the first shift.
- Confirm the AI Game Master uses explicit reads and writes rather than hidden continuity.
- Confirm a resumed session can reconstruct the current slice from stored state.

## Milestone 3: Playable Vertical Slice

Goal: deliver a coherent prologue-plus-first-night experience through the morning-after boundary.

Exit criteria:

- inheritance notice through arrival is playable,
- day investigation covers the MVP room set,
- the first-shift transition is authored and reproducible,
- Thomas and the authority figures produce relationship-sensitive responses,
- outside-at-night danger and bounded ambiguity rules are enforced,
- the morning-after state produces a recap-ready continuation point.

Verification:

- Run scenario checks for keep-or-sell tone variation,
- run clue-path checks across the Great Hall, Great Library, Master Bedroom, Guest Bedroom 1, and Exterior Front,
- run repetition checks to ensure loop telemetry advances the experience.

## Milestone 4: Hardening And Release Readiness

Goal: make the vertical slice dependable enough for sustained iteration and external review.

Exit criteria:

- validation tooling catches malformed snapshot content,
- recap quality is stable across multi-session play,
- prompt and tool traces are auditable enough to explain continuity decisions,
- open defects are reduced below the threshold that blocks narrative review.

Verification:

- Run repeat-session validation with save, resume, and recap flows.
- Review memory writes for tag consistency and improper authored/runtime mixing.
- Confirm the chosen client surface still respects the deferred-framework contract.

## Backlog After MVP

The following work is intentionally outside the MVP critical path:

- later campaign acts beyond the first-night morning-after boundary,
- broader room set expansion beyond the documented MVP rooms,
- additional staff identities beyond the minimum viable cast,
- richer audiovisual presentation or framework-specific polish,
- advanced tooling for analytics, packaging, or content-authoring ergonomics.

## Immediate Execution Sequence

1. Merge or land the planning packet.
2. Author the initial snapshot JSON using the seed-pack rules.
3. Stand up the smallest possible client and AI Game Master loop against the memory server.
4. Validate the playable prologue and first shift before expanding scope.

## Verification Checklist

- Milestone 0 through Milestone 4 are explicit.
- MVP scope is separated from backlog work.
- Snapshot readiness is treated as a gating milestone.
- Validation expectations exist for every milestone.
- The roadmap keeps the repository documentation-first until stable runtime inputs exist.
