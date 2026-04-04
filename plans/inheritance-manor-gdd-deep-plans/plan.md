---
goal: Re-evaluate The Inheritance Manor deep-planning direction using the newer campaign synopsis and authored-memory draft signal
version: 1.1
date_created: 2026-04-04
last_updated: 2026-04-04
owner: TBD
status: Planned
tags: [design, architecture, process, roadmap, documentation]
---

<!-- markdownlint-disable MD036 MD060 -->

# Introduction

![Status: Planned](https://img.shields.io/badge/status-Planned-blue)

This plan defines a documentation-only PR that revises the original deep-planning direction using two newer source artifacts: the prologue synopsis JSON and the currently empty authored-memory draft JSON. The intent is no longer to treat every future planning packet as equal-priority. The next planning pass should instead lock the project around one concrete vertical slice, make authored-versus-runtime memory boundaries explicit, and leave later campaign expansion as a follow-on once the first slice is internally coherent.

## Session Start State

- Workspace is still documentation-first and contains no gameplay implementation code.
- The master concept document remains `docs/GDD/Master Game Design Document –  The Inheritance Manor.md`.
- A planning folder already exists at `plans/inheritance-manor-gdd-deep-plans/` with `plan.md` and `README.md`.
- `docs/initial drafts/manor-campaign-synopsis.json` now resolves several previously open planning assumptions.
- `docs/initial drafts/draft-inheritance-manor-memories.json` exists but is empty, which is a planning gap rather than a tooling error.
- The repo already includes neurodivergent-memory workflow scaffolding under `.github/`, so the planning revision should keep rationale-first, memory-aware documentation habits.

## Branch

- **Recommended branch:** `docs/inheritance-manor-gdd-deep-plans`

## Goal

- Produce a single PR that updates the deep-planning direction so the next authoring pass is anchored on the prologue and first-night vertical slice, with clear source alignment, authored-memory seed expectations, and commit-sized document sequencing.

## Description

- The deliverable is not engine code.
- The deliverable is a revised planning artifact that explains what the synopsis has now settled, what remains ambiguous, and which document sequence should come next.
- Every planned document should remain independently readable, cross-linked, and explicit about assumptions, interfaces with other docs, and open questions.

## Context Map

### Files To Modify In This Planning PR

| File | Purpose | Changes Needed |
|------|---------|----------------|
| `plans/inheritance-manor-gdd-deep-plans/README.md` | Index for the planning set | Add the newer draft inputs and revised document order |
| `plans/inheritance-manor-gdd-deep-plans/plan.md` | Master execution plan for the planning PR | Re-scope priorities, revise commit ordering, and record clarified assumptions |

### Files That Drive This Revision

| File | Relationship |
|------|--------------|
| `docs/GDD/Master Game Design Document –  The Inheritance Manor.md` | Canonical creative seed and full-campaign source |
| `docs/initial drafts/manor-campaign-synopsis.json` | Newer prologue-focused synopsis that concretizes near-term planning boundaries |
| `docs/initial drafts/draft-inheritance-manor-memories.json` | Empty authored-memory draft indicating that seed-memory planning has not started |

### Planned Follow-On Documents Affected By This Revision

| File | Revised Role |
|------|--------------|
| `plans/inheritance-manor-gdd-deep-plans/01-gdd-gap-analysis.md` | Compare the master GDD and synopsis, then lock the vertical-slice scope and unresolved deltas |
| `plans/inheritance-manor-gdd-deep-plans/02-narrative-story-structure.md` | Expand prologue and first-night beats first; defer deeper act detail to placeholders where needed |
| `plans/inheritance-manor-gdd-deep-plans/03-world-location-design.md` | Focus on the vertical-slice rooms, day/night transitions, and clue path |
| `plans/inheritance-manor-gdd-deep-plans/04-systems-memory-model.md` | Define the memory and retrieval model needed for the first slice, including authored versus runtime boundaries |
| `plans/inheritance-manor-gdd-deep-plans/05-npc-relationship-design.md` | Focus first on Thomas, the detective, the lawyer, and any minimum viable night staff |
| `plans/inheritance-manor-gdd-deep-plans/06-technical-architecture.md` | Follow after slice requirements are explicit instead of driving the planning prematurely |
| `plans/inheritance-manor-gdd-deep-plans/07-content-pipeline-and-snapshots.md` | Move earlier in practical importance because the authored-memory seed file is empty |
| `plans/inheritance-manor-gdd-deep-plans/08-mvp-roadmap.md` | Convert the validated prologue slice into milestone exits and backlog boundaries |

## 1. Requirements & Constraints

- **REQ-001**: Treat the output as a planning-only task. Do not implement game code.
- **REQ-002**: Save the master planning artifact to `plans/inheritance-manor-gdd-deep-plans/plan.md`.
- **REQ-003**: Frame the work as a single PR composed of multiple commits.
- **REQ-004**: Re-evaluate the current plan using both the master GDD and `docs/initial drafts/manor-campaign-synopsis.json`.
- **REQ-005**: Treat an empty `docs/initial drafts/draft-inheritance-manor-memories.json` file as a planning signal, not as an error.
- **REQ-006**: Each implementation step must name files, describe the work, and include document-verifiable checks.
- **REQ-007**: Use a pragmatic number of commits; avoid an oversized task list.
- **REQ-008**: Mark unresolved ambiguities with `[NEEDS CLARIFICATION]` instead of silently deciding them.
- **REQ-009**: Planning must still account for narrative/story structure, world/location design, systems/memory model, NPC/relationship design, technical architecture, content pipeline/campaign snapshots, and MVP/production roadmap.
- **REQ-010**: The revised current slice must become more concrete than the prior plan and explicitly reflect the synopsis.
- **CON-001**: The repository contains no gameplay implementation code, so file plans must remain documentation-first.
- **CON-002**: The GDD still implies broader full-campaign ambitions, but the synopsis only concretizes the prologue and first night.
- **CON-003**: The neurodivergent-memory server is part of the product premise, so planning cannot treat persistence as an afterthought or a generic save system.
- **CON-004**: Stop at roughly 80% confidence; avoid speculative overdesign where the source documents are still exploratory.
- **GUD-001**: Favor independently readable docs with cross-links over one monolith.
- **GUD-002**: Capture the why behind every planning slice, not just the proposed output.
- **PAT-001**: Use the MCP host/client/server split as the baseline mental model for AI Game Master integration.
- **PAT-002**: Separate authored campaign snapshots from runtime save, recap, and relationship history early.
- **PAT-003**: Use the synopsis as the authoritative source for near-term vertical-slice details unless it conflicts with a stronger GDD requirement.

## 2. Research Findings

- The master GDD still works as the broad concept source, but the synopsis is materially more concrete for the first playable slice.
- The synopsis resolves the immediate campaign boundary as `prologue-arrival` plus `first-night`, which should now drive the next planning pass instead of trying to spec the whole campaign evenly.
- The synopsis moves ontological truth from fully open-ended to **bounded ambiguity**: the manor is real, night reality follows consistent rules, and staff memories are sincere from their point of view.
- The synopsis resolves the earlier identity-model ambiguity toward `shared_identity_shifted_presentation`, so the plan no longer needs to treat day and night staff as equally likely to be separate entities.
- The synopsis keeps the client framework decision deferred while still making transcript, recap, keyboard-only play, and accessibility explicit. This supports keeping architecture later in the commit order.
- The synopsis explicitly separates `snapshot_contains` from `runtime_state_contains`, which means the content-pipeline and systems docs should move earlier in importance.
- `docs/initial drafts/draft-inheritance-manor-memories.json` is empty. That indicates the authored memory seed pack has not been defined yet, so the plan should prioritize memory-node categories, starter tags, and stable authored IDs before assuming the snapshot path is ready.
- One new ambiguity surfaced in the synopsis: `mcp_integration.memory_server_project_id` is set to `neurodivergent-memory` rather than a Yorkz or campaign-specific namespace. This is workable for a prototype but should be explicitly reviewed before implementation.

## 3. Source Delta Summary

| Topic | GDD Position | Synopsis Position | Planning Decision |
|------|--------------|------------------|-------------------|
| Near-term scope | Broad full-campaign framing | Prologue plus first night only | Prioritize vertical-slice docs before full-campaign expansion |
| Ontological truth | Open candidate examples | Bounded ambiguity with constraints and candidate frames | Keep ambiguity, but document the boundaries as settled |
| Staff identity model | Open to interpretation | Shared identity with shifted presentation | Treat this as the default planning assumption |
| Snapshot/runtime split | High-level snapshot concept | Explicit authored versus runtime lists | Move memory-seed and content-pipeline design earlier |
| Client choice | CLI or minimalist web | Text-first, framework deferred | Keep framework decision deferred and define requirements first |
| Authored memory seed | Implied by snapshot idea | Not present; draft file empty | Treat missing seed data as a first-order planning gap |

## 4. Recommended Planning Output

| Doc | Primary Outcome |
|-----|-----------------|
| `01-gdd-gap-analysis.md` | Maps GDD coverage against the synopsis, records settled deltas, and defines `[NEEDS CLARIFICATION]` boundaries |
| `02-narrative-story-structure.md` | Defines the prologue and first-night narrative ladder, reveal order, and bounded ambiguity rules |
| `03-world-location-design.md` | Defines the MVP room set, day/night contrasts, gating, and clue distribution |
| `05-npc-relationship-design.md` | Defines the vertical-slice cast, relationship pressures, and day/night presentation effects |
| `04-systems-memory-model.md` | Defines state primitives, retrieval rules, tags, distillation mechanics, recap inputs, and runtime mutation rules |
| `07-content-pipeline-and-snapshots.md` | Defines authored snapshot schema, seed-memory categories, stable IDs, and runtime/export boundaries |
| `06-technical-architecture.md` | Defines client responsibilities, AI Game Master boundaries, MCP sessions, and auditability after slice requirements are concrete |
| `08-mvp-roadmap.md` | Defines milestone exits anchored to the validated prologue-first-night slice |

## 5. Implementation Steps

### Implementation Phase 1

- **GOAL-001**: Align the GDD and synopsis, then turn their differences into explicit planning guardrails instead of hidden assumptions.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Update `plans/inheritance-manor-gdd-deep-plans/README.md` and create `plans/inheritance-manor-gdd-deep-plans/01-gdd-gap-analysis.md` as the source-alignment entry point. |  |  |
| TASK-002 | Record which assumptions are now settled by the synopsis: prologue scope, bounded ambiguity, shared staff identity model, deferred framework choice, and snapshot/runtime split. |  |  |
| TASK-003 | Record remaining `[NEEDS CLARIFICATION]` items instead of silently carrying forward older uncertainty. |  |  |

**Commit suggestion:** `docs: align gdd and synopsis for vertical slice planning`

**Files created or updated**

- `plans/inheritance-manor-gdd-deep-plans/README.md`
- `plans/inheritance-manor-gdd-deep-plans/01-gdd-gap-analysis.md`
- `plans/inheritance-manor-gdd-deep-plans/plan.md`

**What this step does**

- Makes the synopsis an explicit planning source instead of an informal side note.
- Prevents the next pass from re-arguing already settled decisions.
- Creates one place to see what is concrete versus still open.

**How to verify**

- The gap-analysis doc names both source files and compares them directly.
- Every newly settled assumption is marked as settled rather than left as a question.
- Every remaining ambiguity is tagged `[NEEDS CLARIFICATION]` with a pragmatic default when possible.

### Implementation Phase 2

- **GOAL-002**: Produce the content-facing planning docs for the prologue and first-night slice before expanding later acts.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-004 | Create `plans/inheritance-manor-gdd-deep-plans/02-narrative-story-structure.md` focused on `prologue-arrival` and `first-night`, including reveal cadence, mystery ladder, and exit conditions. |  |  |
| TASK-005 | Create `plans/inheritance-manor-gdd-deep-plans/03-world-location-design.md` focused on the MVP room set, day/night state changes, and clue placement for the first slice. |  |  |
| TASK-006 | Create `plans/inheritance-manor-gdd-deep-plans/05-npc-relationship-design.md` focused on Thomas, the detective, the lawyer, and the minimum viable night-staff presence implied by the slice. |  |  |

**Commit suggestion:** `docs: define prologue and first-night content slice`

**Files created or updated**

- `plans/inheritance-manor-gdd-deep-plans/02-narrative-story-structure.md`
- `plans/inheritance-manor-gdd-deep-plans/03-world-location-design.md`
- `plans/inheritance-manor-gdd-deep-plans/05-npc-relationship-design.md`
- `plans/inheritance-manor-gdd-deep-plans/01-gdd-gap-analysis.md`

**What this step does**

- Converts the synopsis into an authorable playable slice.
- Keeps later-act planning from consuming attention before the first loop is concrete.
- Ensures story, space, and character docs agree on one slice before systems work deepens.

**How to verify**

- The narrative doc ends at the morning-after boundary of the first night.
- The world doc defines only the rooms and transitions needed for the slice plus clearly marked future placeholders.
- The NPC doc distinguishes day and night presentation while preserving shared identity as the default model.

### Implementation Phase 3

- **GOAL-003**: Define the memory-driven rules and authored snapshot seed needed to make the vertical slice executable later.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-007 | Create `plans/inheritance-manor-gdd-deep-plans/04-systems-memory-model.md` to define memory categories, canonical tags, retrieval priorities, distillation triggers, recap inputs, and loop-response rules for the slice. |  |  |
| TASK-008 | Create `plans/inheritance-manor-gdd-deep-plans/07-content-pipeline-and-snapshots.md` to define what authored snapshot data must exist before runtime play begins and what must only emerge at runtime. |  |  |
| TASK-009 | Explicitly define the authored seed-memory pack that is currently missing from `docs/initial drafts/draft-inheritance-manor-memories.json`, including stable IDs or another deterministic authoring strategy. |  |  |

**Commit suggestion:** `docs: specify memory rules and authored snapshot seed`

**Files created or updated**

- `plans/inheritance-manor-gdd-deep-plans/04-systems-memory-model.md`
- `plans/inheritance-manor-gdd-deep-plans/07-content-pipeline-and-snapshots.md`
- `plans/inheritance-manor-gdd-deep-plans/03-world-location-design.md`
- `plans/inheritance-manor-gdd-deep-plans/05-npc-relationship-design.md`

**What this step does**

- Fixes the biggest newly exposed planning gap: there is a snapshot concept but no authored memory seed specification yet.
- Prevents future narrative docs from relying on undefined persistence behavior.
- Clarifies which records are durable authored content versus mutable playthrough state.

**How to verify**

- The systems doc names the minimum categories of memories required to run the vertical slice.
- The snapshot doc includes an authored-versus-runtime table and a seed-memory authoring checklist.
- The plan no longer assumes that an empty draft memory JSON is acceptable for implementation readiness.

### Implementation Phase 4

- **GOAL-004**: Finish the planning set with architecture and roadmap decisions that are now driven by explicit slice requirements.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-010 | Create `plans/inheritance-manor-gdd-deep-plans/06-technical-architecture.md` after the slice, memory rules, and snapshot requirements are explicit. |  |  |
| TASK-011 | Create `plans/inheritance-manor-gdd-deep-plans/08-mvp-roadmap.md` to turn the validated slice into milestone exits, then separate slice-complete work from later campaign expansion. |  |  |
| TASK-012 | Reconcile all planning docs with the original GDD, updating the gap-analysis and README so the set reads as one coherent system. |  |  |

**Commit suggestion:** `docs: close planning set with architecture and roadmap`

**Files created or updated**

- `plans/inheritance-manor-gdd-deep-plans/06-technical-architecture.md`
- `plans/inheritance-manor-gdd-deep-plans/08-mvp-roadmap.md`
- `plans/inheritance-manor-gdd-deep-plans/01-gdd-gap-analysis.md`
- `plans/inheritance-manor-gdd-deep-plans/README.md`

**What this step does**

- Prevents architecture from outrunning content needs.
- Converts the synopsis-backed slice into milestone criteria the team can actually execute against later.
- Leaves the planning set internally coherent and easier to hand off.

**How to verify**

- The architecture doc clearly separates client, AI Game Master, and memory server responsibilities while preserving a deferred framework choice.
- The roadmap doc makes prologue-plus-first-night the MVP gate rather than a vague full-manor aspiration.
- The final README and gap-analysis doc point to every planning packet and identify what remains backlog versus current slice.

## 6. Alternatives

- **ALT-001**: Keep the earlier equal-priority packet sequence. Rejected because the synopsis now makes one vertical slice concrete enough to deserve priority.
- **ALT-002**: Ignore the empty draft memory JSON until implementation starts. Rejected because that would preserve an avoidable blind spot in snapshot and persistence planning.
- **ALT-003**: Let technical architecture drive the next pass before slice docs are expanded. Rejected because the synopsis now provides content and systems specifics that should define architecture requirements, not the reverse.

## 7. Dependencies

- **DEP-001**: `docs/GDD/Master Game Design Document –  The Inheritance Manor.md` remains the source creative document for full-campaign intent.
- **DEP-002**: `docs/initial drafts/manor-campaign-synopsis.json` is the source of truth for the immediate vertical-slice details.
- **DEP-003**: `docs/initial drafts/draft-inheritance-manor-memories.json` signals missing authored seed work that the next planning pass must account for.
- **DEP-004**: neurodivergent-memory project constraints around canonical tags, ID-first retrieval, and import/snapshot semantics.

## 8. Files

- **FILE-001**: `plans/inheritance-manor-gdd-deep-plans/README.md`.
- **FILE-002**: `plans/inheritance-manor-gdd-deep-plans/plan.md`.
- **FILE-003**: `docs/GDD/Master Game Design Document –  The Inheritance Manor.md`.
- **FILE-004**: `docs/initial drafts/manor-campaign-synopsis.json`.
- **FILE-005**: `docs/initial drafts/draft-inheritance-manor-memories.json`.
- **FILE-006**: `plans/inheritance-manor-gdd-deep-plans/01-gdd-gap-analysis.md`.
- **FILE-007**: `plans/inheritance-manor-gdd-deep-plans/02-narrative-story-structure.md`.
- **FILE-008**: `plans/inheritance-manor-gdd-deep-plans/03-world-location-design.md`.
- **FILE-009**: `plans/inheritance-manor-gdd-deep-plans/04-systems-memory-model.md`.
- **FILE-010**: `plans/inheritance-manor-gdd-deep-plans/05-npc-relationship-design.md`.
- **FILE-011**: `plans/inheritance-manor-gdd-deep-plans/06-technical-architecture.md`.
- **FILE-012**: `plans/inheritance-manor-gdd-deep-plans/07-content-pipeline-and-snapshots.md`.
- **FILE-013**: `plans/inheritance-manor-gdd-deep-plans/08-mvp-roadmap.md`.

## 9. Testing

- **TEST-001**: Verify the revised plan explicitly compares the master GDD and synopsis rather than relying on only one source.
- **TEST-002**: Verify the next-slice document order now prioritizes the prologue and first-night vertical slice.
- **TEST-003**: Verify the plan explicitly treats the empty draft memory JSON as a planning gap that must be addressed.
- **TEST-004**: Verify each commit boundary leaves the planning set reviewable on its own.
- **TEST-005**: Verify the architecture and roadmap steps remain downstream of slice definition instead of preceding it.

## 10. Risks & Assumptions

- **RISK-001**: Even with bounded ambiguity, over-specifying the manor's true nature too early could still collapse later story flexibility.
- **RISK-002**: The empty authored-memory draft could tempt later work to improvise snapshot contents ad hoc, causing schema drift and inconsistent retrieval rules.
- **RISK-003**: `mcp_integration.memory_server_project_id` currently points to `neurodivergent-memory`; if that is not the intended long-term namespace, later content import logic could drift from project expectations.
- **RISK-004**: If architecture planning starts before the slice docs are explicit, framework arguments could displace more important content and persistence decisions.
- **ASSUMPTION-001**: The synopsis is intended to refine the next planning pass rather than replace the master GDD entirely.
- **ASSUMPTION-002**: The MVP remains desktop-first and text-first.
- **ASSUMPTION-003**: The immediate design objective is a coherent prologue-plus-first-night slice, not full-campaign readiness.

## 11. Open Questions

- **Q-001**: `[NEEDS CLARIFICATION]` Should `mcp_integration.memory_server_project_id` remain `neurodivergent-memory` for the campaign snapshot flow, or should it move to a Yorkz or campaign-specific namespace before implementation planning?
- **Q-002**: `[NEEDS CLARIFICATION]` Does the MVP need both the lawyer path and the detective path fully playable in the first slice, or may one path be the canonical first implementation path while the other remains a planned branch?
- **Q-003**: `[NEEDS CLARIFICATION]` What minimum authored memory-node set must exist in the seed snapshot: only rooms and key NPCs, or also starter clues, relationship anchors, and initial recap hooks?
- **Q-004**: `[NEEDS CLARIFICATION]` How much Acts II and III scaffolding should be written in the next pass: interface-level placeholders only, or a lightweight future-state map for continuity?

## 12. Related Specifications / Further Reading

- `docs/GDD/Master Game Design Document –  The Inheritance Manor.md`
- `docs/initial drafts/manor-campaign-synopsis.json`
- `docs/initial drafts/draft-inheritance-manor-memories.json`
