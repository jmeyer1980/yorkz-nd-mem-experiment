# Master Game Design Document – "The Inheritance Manor"

## Overview

"The Inheritance Manor" is a narrative-first psychological thriller RPG built for a text-first interface and powered by the neurodivergent-memory MCP server. The project combines interactive fiction structure, AI Game Master orchestration, and a persistent memory graph so the manor can react to the player as a place that remembers, reinterprets, and pressures them over time.

This document is the master design reference for the project. It consolidates the broader concept work from the original GDD with the more concrete prologue synopsis work completed on 2026-04-04, so future planning and implementation can rely on one canonical source instead of competing drafts.

## Vision

The core fantasy is not winning fights or clearing rooms. The fantasy is inheriting a beautiful estate that gradually reveals itself as a living system of memory, ritual, and emotional pressure. The player should feel that the manor is not merely haunted, but invested in them.

The project aims to deliver:

- A slow-burn psychological thriller with strong continuity and low mechanical friction.
- A dual-reality manor where day and night states transform the meaning of the same locations.
- An AI-driven play loop where memory retrieval and state mutation are part of the fiction, not an invisible backend convenience.
- A structure that supports long pauses between sessions through recap, explicit thread tracking, and durable state.

## Design Pillars

- **Memory as reality:** The world responds to what has been done, repeated, avoided, or emotionally charged.
- **Two overlapping worlds:** Day and night versions of the estate should feel spatially related but narratively distinct.
- **Consequences over combat:** Tension comes from trust, investigation, contradiction, and survival pressure rather than build optimization or damage output.
- **Bounded ambiguity:** The story should preserve mystery without feeling arbitrary; uncertainty must have rules.
- **Neurodivergent-friendly play:** The game should make it easier to resume play, retain context, and notice open loops.

## Audience and Platform

The primary audience is players who enjoy interactive fiction, narrative-heavy RPGs, psychological horror, and mystery games that rely on atmosphere more than spectacle. Secondary audiences include AI-native players, experimental narrative designers, and neurodivergent players interested in systems that mirror associative memory and emotional carryover.

The MVP targets desktop, text-first play. The client should support keyboard-only input, transcript scrollback, recap commands, and accessible presentation. The framework remains intentionally undecided at this stage; the requirement is text-first usability, not a specific UI stack.

## Master Scope Decision

The full campaign still spans a prologue and three acts, but the current design and implementation anchor is one validated vertical slice:

- **Prologue – The Letter and Arrival**
- **Act I opening – First Night / First Shift**

That slice is the MVP. Everything else in this document should support that choice by distinguishing what must be authored now from what can remain extensible for later acts and future campaigns.

## High-Level Concept

The player inherits a well-maintained country estate in modern-day Earth and is forced into contact with it by legal obligation, curiosity, or police scrutiny. By day, the estate appears pristine, mundane, and administratively grounded. By night, the house shifts: staff appear who behave as though the player belongs there, interior spaces acquire emotional and symbolic density, and the grounds outside become actively dangerous.

The player is caught between incompatible explanations:

- the estate is normal and they are under stress,
- the estate is supernatural and has history with them,
- or reality itself has been bent by a memory structure tied to the manor.

The game should not rush to collapse those possibilities into one answer during the prologue. The player must feel the pressure of multiple plausible frames while still learning that the night world follows consistent rules.

## Unique Selling Points

- **Memory-driven narrative engine:** The neurodivergent-memory MCP server is the canonical world model, not just a save layer.
- **Dual-reality manor:** The same floorplan supports multiple realities, allowing emotional and narrative transformation without abandoning spatial coherence.
- **Relationship persistence:** NPCs react not only to the player's major decisions but to tone, loops, avoidance, trust, and emerging habits.
- **Campaign portability:** Authored content can ship as snapshots, enabling future expansions and community-authored scenarios.
- **Recap-first continuity:** The design assumes long-lived play and return-after-absence as normal behavior.

## Narrative Premise

The player receives notice that they have inherited an estate known as The Inheritance Manor. The initial choice is whether to sell the property sight unseen or keep it and visit in person. Regardless of that choice, a missing worker, contractor, or intermediary creates legal and investigative pressure that forces the player into physical contact with the estate.

On arrival, the manor is immaculate. The player meets one or more authority figures, most importantly the detective and the estate lawyer, receives access to the property, and begins learning the shape of the house. The daylight world promises bureaucracy, normalcy, and plausible deniability.

At night, the promise changes. The house shifts, staff emerge, exterior danger becomes real, and the player is treated as someone with an intimate prior relationship to the estate. The first night should land three truths simultaneously:

- the manor is not merely metaphorical,
- the player is safer inside than outside,
- and the staff's familiarity is sincere from their point of view.

## Ontological Truth Policy

The project uses **bounded ambiguity** rather than open-ended mystery.

The following statements are design-level truths:

- The manor is physically real in a modern-Earth setting.
- The night state has internally consistent rules even when the player does not understand them.
- The staff's claims about the player are sincere within their frame of reality.
- Later acts may narrow the explanation, but the prologue must not fully canonize a single answer.

Candidate explanatory frames that remain intentionally available early on:

- The manor as a memory construct entangled with the player.
- Branching timelines anchored to the estate.
- An inherited pact binding the estate to the player's psyche.

## Story Structure

The broader campaign structure remains:

- **Prologue – The Letter and Arrival:** establish inheritance, choice pressure, authorities, access, and normalcy.
- **Act I – First Night / First Shift:** reveal the night manor, establish inside-versus-outside safety, and introduce the staff's impossible familiarity.
- **Act II – Investigation and Recognition:** deepen contradictions between day and night accounts, connect missing persons to the estate's older history, and force the player to decide who is trustworthy.
- **Act III – Confrontation and Choice:** collapse the mystery into a player-facing resolution about belonging, refusal, rewriting, or surrender.

For implementation and content planning purposes, the first complete playable milestone ends at the morning after the first shift.

## World Model

The manor and its immediate estate form the core gamespace. The full location set includes:

- Great Hall
- Master Bedroom
- Guest Bedroom 1
- Guest Bedroom 2
- Guest Bedroom 3
- Great Library
- Dining Hall
- Dance Hall
- Kitchens and Staff Areas
- Wine Cellar and Storage Basement
- Greenhouse
- Workshop
- Exterior Grounds

### MVP Location Set

The vertical slice should fully support only the minimum set needed for the prologue and first night:

- Great Hall
- Master Bedroom
- One Guest Bedroom
- Great Library
- Exterior Front / immediate exterior threshold

Additional rooms may be referenced as future content, but they should not be required to make the first slice coherent.

### Reality Layers

#### Daylight Estate

- The estate appears pristine, mundane, and administratively legible.
- Outside is safe.
- Staff are absent, suppressed, or only implied through traces.
- Police, lawyers, and mundane logistics dominate scene framing.

#### Shifted Manor

- Interior layout and emotional texture subtly or overtly shift.
- The staff are present and behave as though the player belongs to the house.
- Outside is dangerous and should be treated as a survival boundary.
- Doors, routines, and NPC guidance should reinforce that safety lies inside.

## Location State Philosophy

Every important room should be authored in at least two states: day and night. The point is not only descriptive contrast. The point is functional contrast.

| Location | Day Function | Night Function |
| --- | --- | --- |
| Great Hall | Orientation, keys, introductions, legal handoff | Social threshold, house rules, Thomas as emotional gatekeeper |
| Master Bedroom | Empty inheritance space, ownership discomfort | Implied prior life, personal familiarity, destabilizing evidence |
| Great Library | Investigation, documents, estate history | Contradictory evidence, journals, memory artifacts |
| Exterior Front | Arrival, safe departure fantasy | Boundary, barred exit, exterior monster pressure |

Future rooms should follow the same model: each location changes both mood and narrative utility between layers.

## Character Model

### Player Role

The player is the heir, but not yet a stable owner. Their role is defined by uncertainty: they possess legal access without emotional or historical certainty. Their central conflicts are:

- pressure from authorities regarding missing persons,
- cognitive dissonance between their memory and the manor's claims,
- and the question of whether trust belongs inside the manor, outside it, or nowhere.

### Identity Model for Staff

The project uses **shared identity with shifted presentation**.

Day and night staff are not designed as wholly separate people. They are the same underlying identities expressed through different layers of access, memory, and presentation. In practice, this means:

- day scenes may suppress or mundane-filter roles,
- night scenes expose deeper familiarity and ritual logic,
- and relationship history must persist across layers even when presentation changes.

### Core MVP Cast

- **Thomas, the Butler:** night-primary emotional anchor, guide, and gatekeeper.
- **The Detective:** day-primary pressure source who grounds the setting in external reality and suspicion.
- **The Lawyer:** day-supporting source of legal context, inheritance procedure, and mundane legitimacy.

Additional night staff should appear only to the degree required to make the manor feel inhabited during the first shift.

## Relationship Design

Relationships are persistent state, not disposable flavor text. Each major NPC should accumulate:

- key interactions,
- trust or distrust movement,
- emotional valence,
- unresolved tension,
- and notable contradictions between the player's account and the NPC's account.

These records should influence dialogue selection, access to information, safe-versus-unsafe guidance, and which endings become plausible later.

## Core Gameplay Loop

The visible player loop is classic interactive fiction:

1. Read the current description and dialogue.
2. Enter a command or choose a suggested action.
3. The AI Game Master interprets the move against the current world and memory state.
4. The game returns a new scene and writes any meaningful state changes to memory.

Underneath that loop, the system must support:

- room and phase state tracking,
- relationship persistence,
- clue accumulation,
- recap generation,
- and loop-aware responses when the player stalls or repeats.

## Systems Design – Memory Graph as World Model

The neurodivergent-memory MCP server is the canonical game-state layer. The AI Game Master should query and mutate it through MCP tools rather than maintaining an opaque parallel state machine.

### District Mapping

- **logical_analysis:** room topology, investigation facts, contradiction tracking, historical records.
- **emotional_processing:** trust shifts, fear, comfort, intimacy, guilt, and emotional residue from scenes.
- **practical_execution:** inventory, tasks, access states, open hooks, and player-facing objectives.
- **vigilant_monitoring:** monsters, unsafe spaces, missing persons, blocked exits, escalating risk.
- **creative_synthesis:** theories, dreams, uncanny associations, and distilled insights.

### Tags as Gameplay Handles

The game should use canonical tags as stable retrieval handles. Important examples include:

- `location:great_hall`
- `state:day`
- `state:night`
- `npc:thomas`
- `mechanic:day_night_cycle`
- `campaign:inheritance_manor`
- `slice:prologue_first_night`

### Snapshot vs Runtime State

The design now makes a hard distinction between authored content and emergent play state.

**Authored snapshot content includes:**

- room definitions and baseline location states,
- baseline NPC identities and roles,
- initial plot hooks,
- day/night rules,
- and authored clue anchors.

**Runtime state includes:**

- player decisions,
- inventory changes,
- relationship histories,
- recap nodes,
- loop telemetry,
- and distilled conclusions unique to a playthrough.

That separation is mandatory for predictable imports, testing, and later campaign authoring.

## Day-Night Shift Design

Time is phase-based rather than clock-driven. The relevant early phases are:

- Letter
- Decision
- Arrival
- Interior Day Investigation
- First Shift
- Morning After

The shift from day to night is a major authored event, not a cosmetic toggle. It should:

- re-prioritize which memories are retrieved,
- change available NPCs,
- alter room affordances,
- escalate exterior risk,
- and reframe the player's immediate objective from curiosity to safe survival and interpretation.

## Items, Clues, and Distillation

Important items are memory nodes with narrative history, not just inventory entries. Keys, journals, photographs, legal packets, and personally charged objects should all be capable of participating in connections and scene recall.

The clue system should support raw observation first and synthesis later. Distillation is an in-fiction mechanic for converting repeated signals into usable understanding. Example outputs include:

- a theory that a locked room is tied to a prior trauma,
- an insight that two incompatible narratives may both be sincere,
- or a recognition that the manor reacts to repetition itself.

## Loop Telemetry as Fiction

Behavioral loops should be treated as narrative material. If the player repeats actions without progress, the house and NPCs should respond diegetically rather than through a blunt systems message.

Possible responses include:

- Thomas gently acknowledging repetition,
- a corridor or door behaving differently on the next attempt,
- escalating unease or dissociation,
- or a subtle time skip that preserves narrative momentum.

The goal is not to punish exploration. The goal is to stop dead loops from feeling like UI failure.

## Campaign Snapshots and Content Packaging

Campaigns should ship as authored snapshot packages compatible with MCP import flows. The current prologue campaign identifier is:

- `campaign_id: inheritance-manor-prologue-v1`

For project scoping, the design now standardizes on:

- `project_id: yorkz`

This avoids colliding gameplay memories with the upstream neurodivergent-memory server's own project history while still allowing the game to depend on that server as infrastructure.

The first authored snapshot should ultimately live at:

- `campaigns/inheritance-manor/prologue-snapshot.json`

The currently empty draft memory JSON should be treated as an authoring scaffold to fill, not as an acceptable long-term state.

## Technical Architecture Overview

The system consists of three layers:

- **Client Layer:** accepts input, renders transcript, and exposes recap/help affordances.
- **AI Game Master Layer:** interprets player input, decides scene outcomes, selects retrieval targets, and writes state changes.
- **Memory Server Layer:** stores canonical world state, authored content, runtime state, loop telemetry, and distilled insights.

The guiding architectural rule is that the AI Game Master stays thin. It should be an orchestration layer that reasons over explicit state rather than hiding critical game truth inside prompt-only context.

## MVP Definition

The MVP is complete when a player can:

- receive the inheritance premise,
- reach the manor through at least one coherent entry flow,
- meet the detective and/or lawyer in a grounded day context,
- explore the MVP room set,
- survive the first night,
- meet Thomas in the shifted manor,
- encounter the inside-versus-outside safety rule,
- and reach morning with at least one strong unresolved conclusion.

That is the threshold for a real vertical slice. Multi-act continuity, additional endings, richer staff rosters, and broader estate coverage are later milestones.

## Production Roadmap

### Phase 1 – Documentation and Authoring Foundations

- finalize the master GDD,
- define the development plan,
- specify the authored snapshot boundaries,
- and scaffold the initial seed-memory pack.

### Phase 2 – Prototype Runtime

- build the text-first client shell,
- implement the AI Game Master orchestration contract,
- connect MCP retrieval and write flows,
- and support transcript plus recap behavior.

### Phase 3 – Vertical Slice

- author the prologue and first-night content,
- populate the MVP rooms and cast,
- support clue distillation,
- and validate the first morning-after endpoint.

### Phase 4 – Expansion

- add the remaining manor spaces,
- deepen staff and authority branches,
- expand acts II and III,
- and formalize campaign authoring tools and templates.

## Risks and Mitigations

- **AI inconsistency across long sessions:** mitigate with explicit memory tags, recap nodes, and authored truth anchors.
- **Narrative drift from over-ambiguity:** mitigate with bounded ambiguity rules and explicit candidate frames.
- **Snapshot/schema drift:** mitigate by separating authored and runtime state before implementation.
- **Framework debates displacing design progress:** mitigate by keeping the framework decision deferred until the client contract is explicit.
- **Player confusion in a highly reactive story:** mitigate with recap, strong room affordances, and clear inside-versus-outside rules.

## Success Criteria

The design is succeeding when the first playable slice demonstrates all of the following:

- the manor feels coherent in both day and night states,
- the player understands that repetition and emotion matter,
- the staff's familiarity is unsettling but legible,
- the memory graph produces visible continuity rather than hidden bookkeeping,
- and the first night ends with pressure to continue rather than confusion about what the game is.

## Closing Note

This document is the canonical creative and systems brief for The Inheritance Manor as of 2026-04-04. Supporting plans may decompose it further, but they should not contradict the decisions recorded here unless this master GDD is updated first.
