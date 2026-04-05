# Systems Memory Model

## Purpose

Define the explicit memory-state model that lets The Inheritance Manor behave as a world that remembers, instead of as a prompt-only story shell.

## System Goals

1. Keep authored content and runtime mutation separate.
2. Make retrieval deterministic enough for scene assembly.
3. Preserve relationship, clue, and recap continuity across long pauses.
4. Treat repetition and distillation as visible narrative systems.

## Canonical State Split

### Authored Snapshot Content

This data ships with the campaign and should be importable into the memory server as baseline world state.

- room definitions
- day and night state anchors
- baseline NPC identities and roles
- initial plot hooks
- authored clue anchors
- campaign metadata and transition rules

### Runtime State

This data emerges during play and must never overwrite baseline authored content.

- player decisions
- inventory changes
- relationship movement
- clue discoveries
- recap summaries
- loop telemetry
- distilled theories and insights

## District Usage

| District | Use In This Project |
| --- | --- |
| `logical_analysis` | room topology, facts, contradictions, investigation state |
| `emotional_processing` | trust, fear, comfort, guilt, emotional residue |
| `practical_execution` | objectives, inventory, open hooks, current slice state |
| `vigilant_monitoring` | safety boundaries, exterior danger, missing-person pressure |
| `creative_synthesis` | theories, symbolic associations, distilled insight nodes |

## Canonical Tag Families

Use both neurodivergent-memory canonical tags and game-facing retrieval tags.

### Canonical Planning Tags

- `topic:inheritance-manor`
- `scope:project`
- `kind:reference`
- `kind:state`
- `kind:decision`
- `layer:architecture`
- `layer:implementation`
- `layer:debugging`

### Game-Facing Retrieval Tags

- `campaign:inheritance_manor`
- `slice:prologue_first_night`
- `phase:letter`
- `phase:decision`
- `phase:arrival`
- `phase:interior_day`
- `phase:first_shift`
- `phase:morning_after`
- `location:great_hall`
- `location:great_library`
- `location:master_bedroom`
- `location:guest_bedroom_1`
- `location:exterior_front`
- `state:day`
- `state:night`
- `npc:thomas`
- `npc:detective`
- `npc:lawyer`
- `relationship:trust`
- `relationship:openness`
- `relationship:suspicion`
- `relationship:belonging`
- `mystery:ordinary_inheritance`
- `mystery:missing_person_pressure`
- `mystery:personal_contradiction`
- `mystery:house_reality_shift`
- `mystery:staff_familiarity`
- `mystery:exterior_danger`
- `mechanic:day_night_cycle`
- `mechanic:distillation`
- `mechanic:loop_response`

## Deterministic ID Strategy

Use stable domain-prefixed IDs in authored content.

### Required prefixes

- `camp_` for campaign metadata
- `phase_` for authored phase anchors
- `loc_` for rooms and room-state anchors
- `npc_` for characters
- `hook_` for plot hooks
- `clue_` for clue anchors
- `rule_` for authored world rules
- `rel_` for authored relationship baselines
- `recap_` for authored recap templates

### Examples

- `camp_inheritance_manor_prologue_v1`
- `phase_first_shift`
- `loc_great_hall_day`
- `loc_great_hall_night`
- `npc_thomas_core`
- `hook_missing_intermediary`
- `rel_thomas_trust_baseline`
- `rule_outside_unsafe_at_night`

## Relationship Delta Pattern

Author relationship baselines as stable reference nodes and store runtime changes as separate delta memories.

### Authored examples

- `rel_thomas_trust_baseline`
- `rel_detective_suspicion_baseline`
- `rel_lawyer_openness_baseline`

### Runtime delta guidance

- Tag deltas with both the NPC and the relationship axis.
- Write a delta when a trigger behavior from the relationship design doc materially changes tone, access, or interpretation.
- Keep authored baselines immutable and let playthrough deltas express movement.

Example runtime tags:

- `npc:thomas`
- `relationship:trust`
- `phase:first_shift`
- `kind:state`

## Retrieval Priorities

When assembling a scene, retrieve in this order:

1. campaign and slice anchors
2. current phase anchor
3. current room state anchor
4. present NPC anchors
5. unresolved clue anchors for the room
6. relationship deltas relevant to present NPCs
7. recap and loop telemetry relevant to repeated behavior

## Write Rules

### Always write

- major player decisions
- meaningful relationship shifts
- clue discovery
- state transitions between day and night
- recap summaries after significant beats

### Write conditionally

- loop telemetry after repeated ineffective actions
- distilled theories after repeated or incompatible evidence
- emotional residue after unusually charged scenes

Relationship deltas count as meaningful when the player behavior matches the trigger patterns already defined for trust, openness, suspicion, or belonging.

## Distillation Rules

Create a distilled insight when at least one of these is true:

1. the player encounters the same contradiction in two different rooms,
2. an NPC account and a physical clue remain sincerely incompatible,
3. the player repeats a theory-driving behavior enough that the game should respond with new synthesis.

Distilled insights should live in `creative_synthesis` and link back to their source memories.

## Loop Telemetry Policy

Loop handling must stay diegetic.

Possible responses:

- Thomas notices the repetition.
- A hallway or door changes its emphasis.
- The recap system summarizes what the player is circling.
- The manor advances a small beat instead of hard-stalling.

## Recap Node Requirements

Each major scene cluster should be able to produce a recap node that answers:

- where the player is in the phase ladder,
- what the most recent clue was,
- which NPC currently matters most,
- which authority figure the player currently aligns with most,
- whether the estate currently reads to the player as threat, inheritance, or obligation,
- what immediate danger or uncertainty remains,
- what the current player objective feels like in fiction.

## Validation Rules

1. No authored node may depend on runtime-only state to exist.
2. No runtime node may replace the canonical authored identity of a room or NPC.
3. Every authored node must carry deterministic IDs and stable tags.
4. Every recap node must be reproducible from stored state, not hidden prompt context.

## Verification Checklist

- Authored and runtime state are separate.
- Tags cover locations, NPCs, slice, state, and mechanics.
- Deterministic IDs use domain prefixes.
- Distillation and loop telemetry are treated as first-class systems.
- Recap requirements are explicit.
