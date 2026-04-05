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