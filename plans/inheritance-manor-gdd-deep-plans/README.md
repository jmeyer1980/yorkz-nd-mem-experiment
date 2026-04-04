# Inheritance Manor Deep Plans

This folder is the planning spine for turning the master GDD into a document set that is concrete enough for later design and implementation work without writing gameplay code yet.

Current source inputs:

- `docs/GDD/Master Game Design Document –  The Inheritance Manor.md`: canonical concept and full-campaign source.
- `docs/initial drafts/manor-campaign-synopsis.json`: newer prologue-focused synopsis that resolves several earlier planning assumptions.
- `docs/initial drafts/draft-inheritance-manor-memories.json`: currently empty draft authored-memory file; treated as a planning signal that seed-memory design still needs definition.
- `plan.md`: revised single-PR, commit-oriented planning plan.
- `implementation.md`: copy-paste-ready execution guide for authoring the deep-planning packet.

Revised next document sequence:

1. `01-gdd-gap-analysis.md`: compare the master GDD against the synopsis and lock the prologue/first-night planning boundary.
2. `02-narrative-story-structure.md`: expand the prologue and first-night beats, mystery ladder, and bounded ambiguity rules.
3. `03-world-location-design.md`: define the vertical-slice rooms, day/night contrasts, and clue placement for the first playable loop.
4. `05-npc-relationship-design.md`: define the MVP cast and relationship consequences for the first slice.
5. `04-systems-memory-model.md`: define retrieval, tagging, distillation, and runtime state rules.
6. `07-content-pipeline-and-snapshots.md`: define authored snapshot boundaries and the missing seed-memory pack.
7. `06-technical-architecture.md`: define AI Game Master, client, and MCP boundaries after the slice requirements are explicit.
8. `08-mvp-roadmap.md`: convert the validated slice into milestone sequencing.

Suggested branch name for the planning PR: `docs/inheritance-manor-gdd-deep-plans`
