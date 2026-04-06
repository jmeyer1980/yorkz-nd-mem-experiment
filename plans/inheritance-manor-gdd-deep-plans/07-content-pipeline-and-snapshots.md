# Content Pipeline And Snapshots

## Purpose

Define how authored campaign content becomes importable memory-server state for The Inheritance Manor without collapsing authored baseline, runtime mutation, and recap output into one file shape.

## Target Artifact

The first authored campaign snapshot must ultimately live at:

- `campaigns/inheritance-manor/prologue-snapshot.json`

The current draft scaffold:

- `docs/initial drafts/draft-inheritance-manor-memories.json`

exists only as an authoring signal and must not be treated as production-ready snapshot content.

## Authoring Workflow

1. Define snapshot schema and deterministic ID strategy.
2. Author the baseline campaign metadata node.
3. Author the six playable phase anchors.
4. Author room day/night anchors for the MVP room set.
5. Author NPC identity and role anchors.
6. Author relationship baseline anchors.
7. Author plot-hook and rule anchors.
8. Author the minimal initial clue chain.
9. Author recap template anchors for major phase transitions.
10. Validate the snapshot before runtime import.

## Required Authored Categories

| Category | Required In MVP | Notes |
| --- | --- | --- |
| Campaign metadata | Yes | Includes campaign_id, project_id, slice tags, phase order |
| Phase anchors | Yes | Letter, decision, arrival, interior-day, first-shift, morning-after |
| Room anchors | Yes | Great Hall, Master Bedroom, Guest Bedroom 1, Great Library, Exterior Front |
| Room state anchors | Yes | Separate day and night records for rooms where both matter |
| NPC anchors | Yes | Thomas, detective, lawyer |
| Plot hooks | Yes | Inheritance notice, missing intermediary, first-shift trigger |
| Rule anchors | Yes | Outside unsafe at night, safety lies inside, bounded ambiguity constraints |
| Clue anchors | Yes | Minimal contradiction chain |
| Relationship baselines | Yes | Starting stance definitions for Thomas, detective, lawyer |
| Recap template anchors | Yes | Morning-after and other major phase-transition recap scaffolds |
| Runtime nodes | No | Must not be baked into the authored snapshot |

## Snapshot Shape

Use a top-level object with explicit authored intent.

```json
{
  "campaign_id": "inheritance-manor-prologue-v1",
  "project_id": "yorkz",
  "kind": "campaign_snapshot",
  "version": "0.1.0",
  "preserve_ids": true,
  "merge_connections": true,
  "dedupe": "content_plus_tags",
  "entries": []
}
```

## Minimum Snapshot Entry Example

```json
{
  "id": "loc_great_hall_day",
  "content": "Great Hall daytime anchor for The Inheritance Manor. Function: orientation, key handoff, legal threshold, and first interior impression of the estate as administratively real.",
  "district": "logical_analysis",
  "tags": [
    "topic:inheritance-manor",
    "scope:project",
    "kind:reference",
    "layer:architecture",
    "campaign:inheritance_manor",
    "slice:prologue_first_night",
    "location:great_hall",
    "state:day"
  ],
  "project_id": "yorkz",
  "epistemic_status": "validated"
}
```

## Authoring Rules

1. Every authored entry must have a stable ID.
2. Every authored entry must include `project_id: yorkz`.
3. No authored entry may include player-specific outcomes.
4. Connections should express reusable world structure, not playthrough history.
5. Runtime systems may extend authored state, but never silently mutate the authored baseline.

Phase progression may live in campaign metadata, but the MVP should still author explicit phase anchors so retrieval can target the current ladder step by stable ID and tag.

## Import Contract

At campaign start, import the snapshot with:

- `preserve_ids=true`
- `merge_connections=true`
- dedupe policy `content_plus_tags`

These settings preserve authored anchors and make later retrieval by stable IDs practical.

## Runtime Boundary

The following records must only appear after play begins:

- player inventory changes
- relationship deltas
- loop counters
- recap summaries
- distilled theories
- scene outcome summaries

## Validation Checklist Before Import

- Every authored entry uses deterministic IDs.
- Every authored entry includes canonical tags and game-facing tags.
- The snapshot includes all MVP rooms and all three core NPC anchors.
- The rule anchor for outside danger at night exists.
- No runtime-only records are present.

## Seed Pack Definition For The Empty Draft File

Before runtime work begins, the project must author at minimum:

1. one campaign metadata node,
2. six phase anchors for the playable ladder,
3. five room anchors for the MVP room set,
4. corresponding day/night room-state anchors where needed,
5. three NPC anchors,
6. three relationship baseline anchors,
7. two or more plot-hook anchors,
8. one outside-danger rule anchor,
9. one first-shift trigger anchor,
10. a minimal three-step clue chain,
11. recap template anchors for at least the first-shift and morning-after transitions.

## Verification Checklist

- The production snapshot path is named.
- The empty draft file is treated as a gap, not a completed artifact.
- Import settings match the synopsis.
- Seed-pack minimums are explicit.
- Runtime-only data is excluded from the authored snapshot.
