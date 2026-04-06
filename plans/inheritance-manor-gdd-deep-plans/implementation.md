# Inheritance Manor Deep Plans Implementation

<!-- markdownlint-disable MD001 MD022 MD024 MD031 MD032 MD040 -->

## Goal
Create the full deep-planning document packet for The Inheritance Manor so the Yorkz project can move from canonical design into implementation-ready planning without inventing gameplay architecture that the repository has not committed to yet.

## Prerequisites
Make sure that the user is currently on the `docs/inheritance-manor-gdd-deep-plans` branch before beginning implementation.
If not, move them to the correct branch. If the branch does not exist, create it from `main`.

### Project Type, Dependencies, and Validation Commands

- Project type: documentation-first game design and architecture repository.
- Primary deliverables in this plan: Markdown planning docs and JSON-facing planning rules.
- Required tools: `git`, `rg`, and a connected neurodivergent-memory MCP server.
- Deliberately excluded from this PR: gameplay runtime code, framework selection, package manifests, and speculative client implementation.
- Canonical design authority: `docs/GDD/Master Game Design Document –  The Inheritance Manor.md`.
- Near-term scope authority: `docs/initial drafts/manor-campaign-synopsis.json`.
- Gameplay namespace: `project_id: yorkz`.
- Campaign identifier: `inheritance-manor-prologue-v1`.

Run these commands before each stop point:

```powershell
git status --short
git diff --check
rg "inheritance-manor-prologue-v1|project_id: yorkz|bounded ambiguity|authored|runtime" plans/inheritance-manor-gdd-deep-plans docs/GDD "docs/initial drafts"
```

### Memory Anchors For This Thread

- Canonical GDD decision anchor: `memory_357`
- Active implementation-document task thread: `memory_367`
- Documentation-first implementation constraint: `memory_368`

For every step below, write at least one `practical_execution` memory describing what changed and why, and one `logical_analysis` memory whenever the step settles a reusable principle. Connect new memories back to `memory_357`, `memory_367`, and `memory_368` when relevant.

### Step-by-Step Instructions

#### Step 1: Lock Source Alignment And Planning Entry Points
- [ ] Checkout the branch for this documentation PR.
- [ ] If the branch does not exist, create it from `main` using `git checkout -b docs/inheritance-manor-gdd-deep-plans`.
- [ ] Replace `plans/inheritance-manor-gdd-deep-plans/README.md` with the exact content below:

````md
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
````

- [ ] Create `plans/inheritance-manor-gdd-deep-plans/01-gdd-gap-analysis.md` with the exact content below:

````md
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
| Memory architecture | MCP server is canonical world-state layer | Same, with project_id yorkz and snapshot notes | Plan around explicit MCP-driven state, not prompt-only story state |
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
- `04-systems-memory-model.md` must define retrieval and write rules against explicit memory categories.
- `05-npc-relationship-design.md` must prioritize Thomas, the detective, the lawyer, and minimal implied night staff.
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
````

- [ ] Write a `practical_execution` memory summarizing the README and gap-analysis changes, why the packet starts with source alignment, and how this protects the GDD from drift.
- [ ] If you settle any additional durable design rule while writing Step 1, store a linked `logical_analysis` memory and connect it to `memory_357`, `memory_367`, and `memory_368`.

##### Step 1 Verification Checklist
- [ ] `git diff --check` returns no whitespace or conflict-marker issues.
- [ ] `rg "implementation.md|01-gdd-gap-analysis" plans/inheritance-manor-gdd-deep-plans/README.md` finds both entries.
- [ ] `rg "Settled Decisions|NEEDS CLARIFICATION|Bounded Ambiguity" plans/inheritance-manor-gdd-deep-plans/01-gdd-gap-analysis.md` returns the expected headings.
- [ ] A new memory write exists for the step and is connected to the task-thread memory.

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

#### Step 2: Author The Vertical-Slice Narrative, World, And NPC Docs
- [ ] Create `plans/inheritance-manor-gdd-deep-plans/02-narrative-story-structure.md` with the exact content below:

````md
# Narrative Story Structure

## Purpose

Define the playable narrative ladder for the MVP so the first implementation slice has a concrete beginning, escalation path, and morning-after endpoint.

## Slice Boundary

- Start: the inheritance notice and the decision pressure around the estate.
- End: the morning after the first night shift.
- Promise: the player leaves the slice with the manor established as real, uncanny, and personally invested in them.

## Narrative Design Goals

1. Establish modern-Earth plausibility before overt uncanny pressure.
2. Make the manor feel administratively ordinary by day and socially impossible by night.
3. Teach the inside-versus-outside safety rule through fiction, not tutorial copy.
4. End with strong unresolved pressure to continue.

## Phase Ladder

| Phase ID | Label | Player Goal | Narrative Output |
| --- | --- | --- | --- |
| `letter` | The Letter | Understand what has been inherited and decide whether to engage | Inheritance premise, emotional reluctance, curiosity, obligation |
| `decision` | Keep Or Sell | Commit to a stance on the estate | Player tone baseline and practical motivation |
| `arrival` | Arrival At The Manor | Reach the estate under legal or investigative pressure | Detective and lawyer framing, key handoff, first physical orientation |
| `interior-day` | Day Investigation | Explore the safe-seeming manor and absorb contradictions | Day-state room reads, mundane traces of absent staff, first clue anchors |
| `first-shift` | First Shift | Survive the transition into the shifted manor | Thomas appears, outside becomes unsafe, house rules become real |
| `morning-after` | Morning After | Reconcile what happened enough to continue | Unresolved theory, persistent relationship shift, recap-worthy state |

## Beat Sheet

### Beat 1: Inheritance Notice

- The player receives notice that they have inherited the estate.
- The letter must imply history without explaining it.
- The player is allowed to emotionally resist the premise.

### Beat 2: Sell-Or-Keep Friction

- The player expresses an initial stance on the estate.
- This choice shapes tone, not final scope.
- A missing worker, contractor, or intermediary escalates the situation into an on-site requirement.

### Beat 3: Authority Framing

- The detective grounds the situation in modern reality, suspicion, and missing-person pressure.
- The lawyer grounds the situation in ownership, paperwork, and mundane legitimacy.
- At least one authority figure must be materially present before the player is fully alone in the manor.

### Beat 4: Daylight Orientation

- The player enters the Great Hall and receives keys.
- The manor appears pristine and functional.
- Early exploration emphasizes discomfort, absence, and administrative realism rather than overt horror.

### Beat 5: First Contradictory Signals

- The Great Library or Master Bedroom reveals evidence that the manor carries personal familiarity not shared by the player.
- The player should encounter at least one contradiction that cannot be fully dismissed but does not yet break the day frame.

### Beat 6: Shift Trigger

- The player crosses an authored threshold such as waiting too long, opening a specific object, or choosing to stay the night.
- The manor transitions from day to night through an authored event, not a vague fade.
- The transcript must make clear that the same space now means something different.

### Beat 7: Thomas And The House Rules

- Thomas appears as the emotional anchor of the night layer.
- He treats the player as someone returning, not a trespasser.
- Through Thomas and the house itself, the player learns that being outside at night is dangerous.

### Beat 8: Exterior Pressure

- The player attempts, considers, or witnesses the danger of the outside boundary.
- The narrative reinforces that the manor is oppressive but currently safer than leaving.

### Beat 9: Unsettling Familiarity

- Thomas or a related night-space interaction implies a prior household relationship the player cannot verify.
- This implication should feel sincere, not manipulative in a simple villain sense.

### Beat 10: Morning After

- The day layer returns or partially returns.
- The player retains enough evidence, emotion, or contradiction that the night cannot be dismissed as a simple dream.
- The slice ends with one strong unresolved conclusion and a reason to continue investigating.

## Mystery Ladder

| Layer | Early Signal | Confirmation Window |
| --- | --- | --- |
| Ordinary inheritance | Legal documents, keys, lawyer presence | Arrival |
| Missing-person pressure | Detective suspicion, absent intermediary | Arrival through day investigation |
| Personal contradiction | Familiar objects, impossible emotional resonance | Day investigation |
| House reality shift | Authored environmental transition | First shift |
| Staff familiarity | Thomas recognizes the player | First shift |
| Exterior danger | Night boundary pressure | First shift |

## Bounded Ambiguity Rules

1. Do not explain the manor's true ontology in the prologue.
2. Do show that the night layer follows stable rules.
3. Do allow multiple plausible explanatory frames to coexist.
4. Do not invalidate the staff's sincerity.
5. Do ensure every mystery beat still advances comprehension, not confusion.

## Branching Policy

- The player's tone toward the estate may vary.
- The detective and lawyer emphasis may vary.
- The implementation may prioritize one arrival route first, but both perspectives must remain compatible with the shared data model.
- The night shift is mandatory for the MVP and cannot be skipped by an early exit path.

## Morning-After Output Requirements

At slice end, runtime state should be able to answer:

- Which authority figure the player aligned with most strongly.
- Whether the player treated the estate as threat, inheritance, or obligation.
- Which first clue chain the player advanced.
- How Thomas currently reads the player's trust stance.
- Which recap summary should appear first when the player resumes.

## Verification Checklist

- The narrative ladder ends at morning after.
- The detective, lawyer, and Thomas each have explicit narrative functions.
- The shift is authored as an event, not implied as a background toggle.
- The exterior boundary is taught through story action.
- Bounded ambiguity rules are stated as constraints, not mood notes.
````

- [ ] Create `plans/inheritance-manor-gdd-deep-plans/03-world-location-design.md` with the exact content below:

````md
# World Location Design

## Purpose

Define the MVP room set and their day-night functional differences so the first playable slice has coherent spatial logic, clue placement, and survival pressure.

## MVP Room Set

1. Great Hall
2. Master Bedroom
3. Guest Bedroom 1
4. Great Library
5. Exterior Front

All other manor spaces remain valid future content, but they are not required for the first playable loop.

## Spatial Design Principles

1. Reuse the same floorplan across day and night whenever possible.
2. Change narrative function, emotional charge, and available affordances between layers.
3. Keep travel understandable enough that the player forms a mental map.
4. Treat the exterior as a real boundary, not decorative flavor.

## Adjacency Baseline

| From | To | Day | Night |
| --- | --- | --- | --- |
| Exterior Front | Great Hall | Open arrival route | Entry possible, exit unsafe |
| Great Hall | Great Library | Open | Open, more emotionally charged |
| Great Hall | Master Bedroom | Open after key handoff | Open, now personally destabilizing |
| Great Hall | Guest Bedroom 1 | Open | Open, temporary refuge option |

## Room Specifications

### Great Hall

| Property | Day | Night |
| --- | --- | --- |
| Core role | Orientation, keys, legal threshold | Social threshold, house rules, Thomas gatekeeping |
| Mood | Immaculate, reserved, administrative | Warm but uncanny, ceremonially expectant |
| Required interactions | Receive access, meet authority framing, choose first exploration direction | Meet Thomas, receive first safety framing, feel the house recognize the player |
| Clue function | Establish absence and recent use | Establish prior belonging and ritual familiarity |

Mandatory notes:

- This is the first interior room the player fully occupies.
- It must clearly support both day authority presence and night staff presence.
- It anchors the player's sense that the manor is the same place in both states.

### Master Bedroom

| Property | Day | Night |
| --- | --- | --- |
| Core role | Ownership discomfort, inheritance intimacy | Personal destabilization, implied prior life |
| Mood | Staged, preserved, slightly too orderly | Lived-in memory pressure, emotionally charged familiarity |
| Required interactions | Inspect inherited personal space, locate one contradiction | Discover evidence that the manor believes the room already belongs to the player |
| Clue function | Physical object evidence | Emotional evidence and deeper contradiction |

Mandatory notes:

- This room should make legal ownership feel different from emotional ownership.
- Night-state details should imply memory or habit without fully explaining it.

### Guest Bedroom 1

| Property | Day | Night |
| --- | --- | --- |
| Core role | Ordinary fallback room | Temporary refuge and contrast with the Master Bedroom |
| Mood | Neutral, functional | Safer but still uncanny |
| Required interactions | Optional exploration or practical staging | Reinforce that not every interior space carries the same personal weight |
| Clue function | Low clue density | Opportunity for pacing, recovery, or side detail |

Mandatory notes:

- This room exists to prevent the slice from feeling like every location is maximally charged at all times.
- It can serve as a temporary calm node during the first night.

### Great Library

| Property | Day | Night |
| --- | --- | --- |
| Core role | Investigation, records, estate history | Contradictory evidence, journals, memory artifacts |
| Mood | Scholarly, orderly, plausible | Dense, intimate, suggestive of private history |
| Required interactions | Discover the first nontrivial clue chain | Reinterpret earlier evidence through the night frame |
| Clue function | Start or advance the main clue chain | Deepen contradiction and theory formation |

Mandatory notes:

- This room should be the clearest bridge between day investigation and night reinterpretation.
- It is the preferred location for the first distillation-worthy contradiction.

### Exterior Front

| Property | Day | Night |
| --- | --- | --- |
| Core role | Arrival and departure fantasy | Threat boundary and survival pressure |
| Mood | Open, plausible, transitional | Hostile, barred, predatory |
| Required interactions | Establish a believable route of entry | Teach that leaving the house is unsafe |
| Clue function | Grounds the real-world frame | Shows that the manor's rules extend beyond interior mood |

Mandatory notes:

- Day should imply escape remains possible.
- Night should prove that escape is not currently safe.
- The threat should function as pressure, not cheap punishment.

## Clue Path For The MVP

1. Great Hall: receive keys and register the house as administratively real.
2. Great Library: uncover the first contradiction or documentary anomaly.
3. Master Bedroom: encounter intimate evidence that the contradiction may be personal.
4. Great Hall at night: Thomas reframes the contradiction as household memory.
5. Exterior Front at night: danger forces the player to accept that the house is currently the safer space.

## Future-Room Placeholder Policy

Future rooms may be named and lightly described, but they must not introduce mechanics, clues, or relationship dependencies required to complete the MVP.

## Verification Checklist

- Only the MVP rooms are required content.
- Every room has a distinct day and night function.
- The Great Library and Master Bedroom support the main contradiction path.
- The Exterior Front teaches the safety boundary.
- Guest Bedroom 1 provides pacing relief rather than redundant exposition.
````

- [ ] Create `plans/inheritance-manor-gdd-deep-plans/05-npc-relationship-design.md` with the exact content below:

````md
# NPC Relationship Design

## Purpose

Define the core relationship model for the MVP cast so narrative pressure, trust shifts, and layered identity remain consistent across day and night states.

## Relationship Design Principles

1. Relationships persist across presentation layers.
2. Trust should influence tone, access, and interpretation before it influences explicit branching.
3. Every major NPC should pressure a different interpretation of the manor.
4. The player's behavior matters even when the game does not surface a visible meter.

## Core Cast

### Thomas

| Field | Value |
| --- | --- |
| Role | Butler |
| Day presence | Absent |
| Night presence | Primary |
| Core function | Emotional anchor, guide, gatekeeper |
| Relationship pitch | Treats the player as someone returning home after an unexplained absence |
| Pressure style | Warm certainty that becomes more unsettling the longer it holds |

Thomas should:

- Welcome the player sincerely.
- Reinforce inside-as-safety.
- Offer interpretation without solving the full mystery.
- React strongly to rejection, avoidance, or trust.

### Detective

| Field | Value |
| --- | --- |
| Role | Police detective |
| Day presence | Primary |
| Night presence | Absent |
| Core function | External pressure, missing-person framing, modern reality anchor |
| Relationship pitch | Treats the player as a person of interest and possible unreliable narrator |
| Pressure style | Skeptical, procedural, persistent |

The detective should:

- Keep the player accountable to the missing-person thread.
- Make ordinary explanations feel socially and legally relevant.
- Frame suspicious behavior as a real-world risk.

### Lawyer

| Field | Value |
| --- | --- |
| Role | Estate lawyer |
| Day presence | Supporting |
| Night presence | Absent |
| Core function | Legal legitimacy, inheritance procedure, administrative grounding |
| Relationship pitch | Professional neutral party facilitating transfer of ownership |
| Pressure style | Restrained, practical, uncomfortable with emotional irregularity |

The lawyer should:

- Make ownership feel materially real.
- Provide keys, documents, and procedural context.
- Contrast with the detective by pressing obligation rather than suspicion.

### Minimum Viable Night Staff

The first slice may imply one or two additional night-staff presences, but they should remain secondary to Thomas. Their function is to make the manor feel inhabited, not to dilute the first-night emotional anchor.

## Shared Identity Model

The project uses `shared_identity_shifted_presentation`.

That means:

- day and night are not separate casts,
- relationship history must not reset when the layer changes,
- the player can notice contradictions in presentation without the design treating them as distinct unrelated people.

## Relationship Axes

| Axis | Meaning | Used By |
| --- | --- | --- |
| trust | Does the NPC believe the player is acting in good faith | Thomas, detective |
| openness | How much the NPC is willing to say directly | Thomas, lawyer |
| suspicion | How much the NPC treats the player as dangerous, evasive, or unreliable | Detective |
| belonging | How strongly the manor-side cast treats the player as part of the household | Thomas, night staff |

## Trigger Behaviors

### Raise Trust

- Asking grounded questions instead of lashing out.
- Following safety guidance after the first shift.
- Sharing discoveries without obvious manipulation.

### Lower Trust

- Dismissing NPCs as liars without evidence.
- Repeating self-destructive actions after a warning.
- Treating the house and staff with contempt during vulnerable beats.

### Raise Suspicion

- Contradicting prior statements.
- Refusing obvious questions from authorities.
- Acting as though the player already knows parts of the manor they should not know.

## Data Recommendations

Use stable relationship handles in planning and later implementation:

- `npc:thomas`
- `npc:detective`
- `npc:lawyer`
- `relationship:trust`
- `relationship:openness`
- `relationship:suspicion`
- `relationship:belonging`

## Scene-Level Outcomes Required For The MVP

- The player must be able to leave the day phase with a stronger alignment toward either the detective or the lawyer.
- The player must complete the first night with a clear Thomas relationship tone.
- The player must feel that Thomas's familiarity is sincere and unnerving at the same time.

## Verification Checklist

- Thomas, detective, and lawyer each apply different narrative pressure.
- Relationship axes are reusable rather than one-scene notes.
- The shared identity model is stated explicitly.
- Thomas remains the primary emotional anchor of the first night.
- Additional night staff remain subordinate to the MVP focus.
````

- [ ] Write a `practical_execution` memory describing the created narrative, world, and NPC docs and why this packet sequence keeps story, space, and character aligned before systems detail expands.
- [ ] If any durable interpretation rule becomes clearer during Step 2, store a linked `logical_analysis` memory and connect it back to the task thread.

##### Step 2 Verification Checklist
- [ ] `git diff --check` returns no issues.
- [ ] `rg "Phase Ladder|Mystery Ladder|Morning-After Output Requirements" plans/inheritance-manor-gdd-deep-plans/02-narrative-story-structure.md` returns the expected headings.
- [ ] `rg "MVP Room Set|Clue Path For The MVP|Exterior Front" plans/inheritance-manor-gdd-deep-plans/03-world-location-design.md` returns the expected headings.
- [ ] `rg "Shared Identity Model|Relationship Axes|Thomas" plans/inheritance-manor-gdd-deep-plans/05-npc-relationship-design.md` returns the expected headings.
- [ ] Step memory writes are stored and connected.

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

#### Step 3: Define The Memory Model And Snapshot Pipeline
- [ ] Create `plans/inheritance-manor-gdd-deep-plans/04-systems-memory-model.md` with the exact content below:

````md
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
- `mechanic:day_night_cycle`
- `mechanic:distillation`
- `mechanic:loop_response`

## Deterministic ID Strategy

Use stable domain-prefixed IDs in authored content.

### Required prefixes

- `camp_` for campaign metadata
- `loc_` for rooms and room-state anchors
- `npc_` for characters
- `hook_` for plot hooks
- `clue_` for clue anchors
- `rule_` for authored world rules
- `rel_` for authored relationship baselines
- `recap_` for authored recap templates

### Examples

- `camp_inheritance_manor_prologue_v1`
- `loc_great_hall_day`
- `loc_great_hall_night`
- `npc_thomas_core`
- `hook_missing_intermediary`
- `rule_outside_unsafe_at_night`

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
````

- [ ] Create `plans/inheritance-manor-gdd-deep-plans/07-content-pipeline-and-snapshots.md` with the exact content below:

````md
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
3. Author room day/night anchors for the MVP room set.
4. Author NPC identity and role anchors.
5. Author plot-hook and rule anchors.
6. Author the minimal initial clue chain.
7. Validate the snapshot before runtime import.

## Required Authored Categories

| Category | Required In MVP | Notes |
| --- | --- | --- |
| Campaign metadata | Yes | Includes campaign_id, project_id, slice tags, phase order |
| Room anchors | Yes | Great Hall, Master Bedroom, Guest Bedroom 1, Great Library, Exterior Front |
| Room state anchors | Yes | Separate day and night records for rooms where both matter |
| NPC anchors | Yes | Thomas, detective, lawyer |
| Plot hooks | Yes | Inheritance notice, missing intermediary, first-shift trigger |
| Rule anchors | Yes | Outside unsafe at night, safety lies inside, bounded ambiguity constraints |
| Clue anchors | Yes | Minimal contradiction chain |
| Relationship baselines | Yes | Starting stance definitions for Thomas, detective, lawyer |
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
2. five room anchors for the MVP room set,
3. corresponding day/night room-state anchors where needed,
4. three NPC anchors,
5. three relationship baseline anchors,
6. two or more plot-hook anchors,
7. one outside-danger rule anchor,
8. one first-shift trigger anchor,
9. a minimal three-step clue chain.

## Verification Checklist

- The production snapshot path is named.
- The empty draft file is treated as a gap, not a completed artifact.
- Import settings match the synopsis.
- Seed-pack minimums are explicit.
- Runtime-only data is excluded from the authored snapshot.
````

- [ ] Write a `practical_execution` memory summarizing the systems and snapshot documents and why deterministic IDs, canonical tags, and authored/runtime separation are required before any runtime implementation.
- [ ] Write or update a `logical_analysis` memory if Step 3 locks any durable memory-model principle beyond what is already stored.
- [ ] Connect all new step memories to `memory_368` because this step formalizes the documentation-first constraint into an executable content pipeline.

##### Step 3 Verification Checklist
- [ ] `git diff --check` returns no issues.
- [ ] `rg "Deterministic ID Strategy|Retrieval Priorities|Loop Telemetry Policy" plans/inheritance-manor-gdd-deep-plans/04-systems-memory-model.md` returns the expected headings.
- [ ] `rg "Target Artifact|Snapshot Shape|Seed Pack Definition" plans/inheritance-manor-gdd-deep-plans/07-content-pipeline-and-snapshots.md` returns the expected headings.
- [ ] The snapshot example includes `project_id` set to `yorkz`.
- [ ] Step memory writes are stored and connected.

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

#### Step 4: Close The Packet With Architecture And Roadmap
- [ ] Create `plans/inheritance-manor-gdd-deep-plans/06-technical-architecture.md` with the exact content below:

````md
# Technical Architecture

## Purpose

Define the implementation-facing architecture for the MVP without forcing an early client framework choice.

## Architectural Rule

The AI Game Master must remain an orchestration layer over explicit memory-server state. Critical game truth must not live only in prompt context.

## Three-Layer Model

### Client Layer

Responsibilities:

- accept keyboard-driven input,
- render transcript output,
- expose recap and help affordances,
- surface state transitions clearly,
- remain accessible for long text sessions.

Non-responsibilities:

- storing canonical world truth,
- inventing state outside the orchestrator,
- performing hidden gameplay resolution.

### AI Game Master Layer

Responsibilities:

- parse player intent,
- retrieve the right authored and runtime state,
- assemble scene output,
- trigger state writes,
- drive day-night transitions,
- request recap material from explicit stored state.

Non-responsibilities:

- silently substituting prompt memory for stored state,
- owning the only copy of relationship or clue continuity,
- bypassing authored slice boundaries.

### Memory Server Layer

Responsibilities:

- store authored snapshot baseline,
- store runtime playthrough deltas,
- store recap and loop telemetry,
- support tag and ID-based retrieval,
- support import and future export of campaign state.

## Proposed Repository Structure For Later Implementation

This structure is framework-neutral and exists to keep the system clean once code begins.

```text
src/
  client/
  game_master/
  content/
  memory/
  recap/
  testing/
campaigns/
  inheritance-manor/
tests/
```

## Interface Contracts

### Client To Game Master

Input contract should include:

- raw player command,
- current visible mode if any,
- last known scene reference,
- optional accessibility or recap request flags.

### Game Master To Memory Server

Retrieval contract should support:

- current phase,
- current room,
- active NPCs,
- unresolved clues,
- current threat state,
- relationship deltas and recap context.

Write contract should support:

- scene outcome records,
- phase transitions,
- relationship shifts,
- clue discoveries,
- loop telemetry,
- recap summaries.

## Prompt And Tooling Policy

1. The prompt may contain style, tone, and instruction.
2. The prompt must not be the only place where campaign truth lives.
3. The orchestrator should prefer retrieving explicit state over remembering prior turns implicitly.
4. The recap system should reconstruct context from stored state rather than freeform retelling.

## Framework Decision Policy

The client framework remains deferred.

Acceptable future choices include:

- a terminal-first text client,
- a minimal web client,
- another keyboard-friendly text interface.

The first selection must satisfy the requirements already settled in the master GDD:

- transcript-first reading,
- keyboard-only input,
- recap support,
- accessibility-conscious presentation,
- minimal friction for long sessions.

## Testing Surfaces

When code work begins, the project must be able to test:

- snapshot validation,
- retrieval behavior by room and phase,
- separation of authored and runtime state,
- recap generation inputs,
- loop-response triggers,
- phase-transition correctness.

## Verification Checklist

- The three-layer architecture is explicit.
- Prompt-only truth is rejected as a design approach.
- Client framework choice remains deferred without leaving the contract vague.
- Future repository structure is proposed without pretending it already exists.
- Testing surfaces are named before runtime work begins.
````

- [ ] Create `plans/inheritance-manor-gdd-deep-plans/08-mvp-roadmap.md` with the exact content below:

````md
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
````

- [ ] Write a `practical_execution` memory summarizing the architecture and roadmap docs and why they intentionally translate the current design into milestone exits instead of prematurely choosing a client stack.
- [ ] If this final step crystallizes a durable principle, store a linked `logical_analysis` memory and connect it to the broader Yorkz design thread.
- [ ] Confirm that the final handoff memory for this session names what was completed, what remains, the immediate next slice, and the reason the packet stays documentation-first at this stage.

##### Step 4 Verification Checklist
- [ ] `git diff --check` returns no issues.
- [ ] `rg "Three-Layer Model|Framework Decision Policy|Testing Surfaces" plans/inheritance-manor-gdd-deep-plans/06-technical-architecture.md` returns the expected headings.
- [ ] `rg "Milestone 0|Milestone 4|Backlog After MVP" plans/inheritance-manor-gdd-deep-plans/08-mvp-roadmap.md` returns the expected headings.
- [ ] A final practical memory and handoff memory have been written and connected.

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
