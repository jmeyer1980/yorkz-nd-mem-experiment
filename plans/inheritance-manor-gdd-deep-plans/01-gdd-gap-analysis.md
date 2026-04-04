# GDD Gap Analysis

## Purpose

This document compares the canonical master GDD and the newer prologue synopsis so the Yorkz project can move forward with one explicit vertical-slice planning baseline instead of carrying multiple partially authoritative sources.

## Source Hierarchy

1. `docs/GDD/Master Game Design Document –  The Inheritance Manor.md` is the canonical creative and systems brief.
2. `docs/initial drafts/manor-campaign-synopsis.json` is the authority for near-term vertical-slice detail unless it conflicts with a stronger master-GDD rule.
3. `DEVELOPMENT_PLAN.md` is the implementation derivative of the canonical design, not a peer design authority.
4. `plans/inheritance-manor-gdd-deep-plans/*.md` are execution-facing planning packets derived from the sources above.

## Comparison Summary

| Topic | Master GDD | Synopsis | Planning Decision |
| --- | --- | --- | --- |
| Near-term scope | Full campaign framed as prologue plus three acts | Explicitly concrete only through prologue and first night | Treat prologue plus first night as the only current implementation slice |
| Ontology | Multiple candidate explanations stay open early | Bounded ambiguity with fixed constraints | Preserve uncertainty, but stop treating the ontology as unconstrained |
| Staff identity | Shared identity with shifted presentation is stated as the intended model | Same model named directly | Treat shared identity with shifted presentation as settled |
| Client framework | Deferred in favor of text-first UX | Deferred in favor of text-first UX | Keep framework choice downstream of content and memory contracts |
| Memory architecture | MCP server is canonical world-state layer | Same, with project_id: yorkz and snapshot notes | Plan around explicit MCP-driven state, not prompt-only story state |
| Snapshot/runtime split | Named conceptually | Broken into explicit authored and runtime categories | Move snapshot/schema planning earlier in importance |
| MVP locations | Great Hall, Master Bedroom, one Guest Bedroom, Great Library, Exterior Front | Same minimum slice implied through narrative and systems focus | Treat this as the locked room set for the first playable loop |

## Settled Decisions

### Decision 1: Canonical Scope

The active MVP is the prologue and first night only. Later acts remain part of the long-term campaign, but they are not equal-priority planning targets for the current document packet.

### Decision 2: Bounded Ambiguity

The manor is real, the night state follows consistent rules, and the staff are sincere from their own frame of reality. The prologue must preserve multiple explanatory frames without pretending anything could happen arbitrarily.

### Decision 3: Shared Identity Across Layers

Day and night presentations are different expressions of the same underlying identities. Relationship design must persist across layers even when presentation changes.

### Decision 4: Documentation Before Runtime

This repository is still documentation-first. The correct next action is to author the deep-planning packet, not to fabricate runtime code around unresolved schema questions.

### Decision 5: Authored And Runtime State Must Separate Early

Authored snapshot content, runtime playthrough state, recap material, and loop telemetry must not collapse into one undifferentiated store shape. This is a durable system rule, not an implementation detail.

## Implications For The Planning Packet

- `02-narrative-story-structure.md` must stop at the morning-after boundary.
- `03-world-location-design.md` must describe only the MVP rooms as required content and treat all other spaces as backlog placeholders.
- `05-npc-relationship-design.md` must prioritize Thomas, the detective, the lawyer, and minimal implied night staff.
- `04-systems-memory-model.md` must define retrieval and write rules against explicit memory categories.
- `07-content-pipeline-and-snapshots.md` must define the authored seed-memory pack because the current draft JSON is empty.
- `06-technical-architecture.md` must remain framework-neutral while still specifying component contracts.

## [NEEDS CLARIFICATION] Items

| Topic | Current Default | Why It Needs Clarification |
| --- | --- | --- |
| Daytime entry path priority | Support both detective and lawyer presence, but allow one path to be the first implemented route | The design supports multiple grounded entry frames, but the first playable branch may need a canonical implementation order |
| Seed-memory minimum | Rooms, NPC anchors, initial plot hooks, state tags, and a minimal clue chain | The snapshot authoring workload needs a minimum viable boundary before code begins |
| Later-act scaffolding depth | Interface-level placeholders only | Full later-act detailing would dilute the current vertical-slice focus |
| Distillation threshold | Distill after repeated evidence, recurring emotional charge, or incompatible narratives | The exact trigger count and storage format should be specified in the systems doc |

## Planning Guardrails

1. Do not add gameplay framework commitments in this packet.
2. Do not re-open scope beyond prologue plus first night.
3. Do not allow the synopsis to overrule the master GDD on established high-level principles.
4. Do not treat the empty authored-memory JSON as acceptable project readiness.
5. Do not separate narrative planning from memory-system planning; the premise depends on their interaction.

## Output Order

1. Narrative and story structure
2. World and room design
3. NPC relationship design
4. Systems and memory model
5. Content pipeline and snapshot schema
6. Technical architecture
7. MVP roadmap

## Verification Checklist

- The canonical master GDD is named as the design source of truth.
- The synopsis is treated as a near-term refinement source, not a competing canon.
- Every settled decision is stated positively rather than implied.
- Every unresolved item is explicitly tagged `[NEEDS CLARIFICATION]`.
- The document packet order matches the README.