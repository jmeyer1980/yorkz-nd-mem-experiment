from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from yorkz.memory_system import MemoryRecord, MemorySystem, SnapshotPackage
from yorkz.turn_orchestration import TurnInput, TurnOrchestrator


DEFAULT_SNAPSHOT_PATH = (
    Path(__file__).resolve().parents[2]
    / "campaigns"
    / "inheritance-manor"
    / "prologue-snapshot.json"
)


def _normalize_token(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned


def _word_tokens(value: str) -> set[str]:
    return {token for token in _normalize_token(value).split("_") if token}


SEQUENCE_RE = re.compile(r"_(?:turn|slice)_(\d+)_")


def _runtime_sequence(record_id: str) -> int:
    match = SEQUENCE_RE.search(record_id)
    if match:
        return int(match.group(1))
    return 0


@dataclass(slots=True)
class SliceTurnResult:
    phase_id: str
    location_id: str
    transcript: str
    recap_triggered: bool
    recap_inputs: list[str]
    discovered_clues: list[str]
    relationship_deltas: list[str]


class PlayableVerticalSliceRuntime:
    """Deterministic vertical-slice runtime that materializes turn outputs to runtime memory."""

    def __init__(
        self,
        *,
        memory_store: MemorySystem,
        project_id: str,
        campaign_id: str,
    ) -> None:
        if memory_store.project_id != project_id:
            raise ValueError(
                "PlayableVerticalSliceRuntime memory_store.project_id "
                f"'{memory_store.project_id}' does not match project_id '{project_id}'."
            )
        self._memory_store = memory_store
        self._project_id = project_id
        self._campaign_id = _normalize_token(campaign_id)
        self._orchestrator = TurnOrchestrator(
            memory_store=memory_store,
            project_id=project_id,
        )

    @classmethod
    def from_snapshot_file(
        cls,
        *,
        snapshot_path: Path | None = None,
        project_id: str = "yorkz",
    ) -> "PlayableVerticalSliceRuntime":
        resolved_path = snapshot_path or DEFAULT_SNAPSHOT_PATH
        data = json.loads(resolved_path.read_text(encoding="utf-8"))
        package = SnapshotPackage.from_dict(data)
        store = MemorySystem(project_id=project_id)
        store.import_snapshot(package)
        return cls(
            memory_store=store,
            project_id=project_id,
            campaign_id=package.campaign_id,
        )

    @property
    def memory_store(self) -> MemorySystem:
        return self._memory_store

    def play_turn(
        self,
        *,
        session_id: str,
        lineage_id: str,
        player_command: str,
        recap_requested: bool = False,
    ) -> SliceTurnResult:
        current_phase = self._current_phase(lineage_id)
        current_location = self._current_location(lineage_id)

        orchestrator_output = self._orchestrator.process_turn(
            TurnInput(
                session_id=session_id,
                project_id=self._project_id,
                lineage_id=lineage_id,
                player_command=player_command,
                campaign_id=self._campaign_id,
                phase_hint=current_phase,
                location_hint=current_location,
                recap_requested=recap_requested,
            )
        )
        for intent in orchestrator_output.write_intents:
            self._memory_store.upsert(
                MemoryRecord(
                    record_id=intent.record_id,
                    content=intent.content,
                    district=intent.district,
                    tags=list(intent.tags),
                    project_id=self._project_id,
                    memory_type="runtime",
                    lineage_id=lineage_id,
                )
            )

        next_phase, next_location, recap_triggered = self._apply_story_progression(
            lineage_id=lineage_id,
            player_command=player_command,
            current_phase=current_phase,
            current_location=current_location,
            recap_requested=recap_requested,
        )

        self._write_state_marker(
            lineage_id=lineage_id,
            marker_type="phase",
            marker_value=next_phase,
            phase_id=next_phase,
            location_id=next_location,
            district="practical_execution",
        )
        self._write_state_marker(
            lineage_id=lineage_id,
            marker_type="location",
            marker_value=next_location,
            phase_id=next_phase,
            location_id=next_location,
            district="practical_execution",
        )

        clue_ids = self._maybe_add_clues(
            lineage_id=lineage_id,
            player_command=player_command,
            phase_id=next_phase,
            location_id=next_location,
        )
        relationship_ids = self._maybe_add_relationship_deltas(
            lineage_id=lineage_id,
            player_command=player_command,
            phase_id=next_phase,
            location_id=next_location,
        )

        recap_inputs = self._collect_recap_inputs(lineage_id)
        if recap_triggered:
            self._write_runtime_record(
                lineage_id=lineage_id,
                purpose="recap",
                district="creative_synthesis",
                content=(
                    f"Recap for lineage={lineage_id}: phase={next_phase}; location={next_location}; "
                    f"recent_events={', '.join(recap_inputs) if recap_inputs else 'none'}"
                ),
                tags=self._runtime_tags(
                    kind="recap",
                    phase_id=next_phase,
                    location_id=next_location,
                    extra=["recap:morning_after"],
                ),
            )

        transcript = self._compose_slice_transcript(
            command=player_command,
            phase_id=next_phase,
            location_id=next_location,
            clue_ids=clue_ids,
            relationship_ids=relationship_ids,
            recap_triggered=recap_triggered,
        )
        return SliceTurnResult(
            phase_id=next_phase,
            location_id=next_location,
            transcript=transcript,
            recap_triggered=recap_triggered,
            recap_inputs=recap_inputs,
            discovered_clues=self._discovered_clues(lineage_id),
            relationship_deltas=self._relationship_delta_keys(lineage_id),
        )

    def _apply_story_progression(
        self,
        *,
        lineage_id: str,
        player_command: str,
        current_phase: str,
        current_location: str,
        recap_requested: bool,
    ) -> tuple[str, str, bool]:
        tokens = _word_tokens(player_command)
        phase = current_phase
        location = current_location
        recap_triggered = recap_requested

        if current_phase == "letter" and tokens.intersection(
            {"keep", "sell", "accept", "inheritance"}
        ):
            phase = "decision"
        if current_phase in {"letter", "decision"} and tokens.intersection(
            {"arrive", "travel", "follow", "manor"}
        ):
            phase = "arrival"
            location = "great_hall"
        if current_phase == "arrival" and tokens.intersection(
            {"inspect", "explore", "search", "library", "bedroom", "hall"}
        ):
            phase = "interior_day"
            if "library" in tokens:
                location = "great_library"
            elif "bedroom" in tokens:
                location = "master_bedroom"
            else:
                location = "great_hall"
        if current_phase == "interior_day" and tokens.intersection(
            {"wait", "night", "sleep", "stay"}
        ):
            phase = "first_shift"
            location = "great_hall"
        if current_phase == "first_shift" and tokens.intersection(
            {"outside", "door", "leave"}
        ):
            location = "exterior_front"
        if current_phase == "first_shift" and tokens.intersection(
            {"morning", "dawn", "sunrise"}
        ):
            phase = "morning_after"
            location = "great_hall"
            recap_triggered = True

        if phase != current_phase:
            self._write_runtime_record(
                lineage_id=lineage_id,
                purpose="phase_transition",
                district="practical_execution",
                content=(
                    f"Phase transition for lineage={lineage_id}: {current_phase} -> {phase}; "
                    f"command={player_command.strip()}"
                ),
                tags=self._runtime_tags(
                    kind="phase_transition",
                    phase_id=phase,
                    location_id=location,
                    extra=[f"state:from_{current_phase}", f"state:to_{phase}"],
                ),
            )

        return phase, location, recap_triggered

    def _maybe_add_clues(
        self,
        *,
        lineage_id: str,
        player_command: str,
        phase_id: str,
        location_id: str,
    ) -> list[str]:
        tokens = _word_tokens(player_command)
        clues: list[tuple[str, str]] = []
        if tokens.intersection({"letter", "seal"}):
            clues.append(
                (
                    "letter_irregular_seal",
                    "Inheritance notice seal pattern conflicts with archive expectations.",
                )
            )
        if tokens.intersection({"library", "ledger"}):
            clues.append(
                (
                    "library_ledger_gap",
                    "Great Library ledger shows a transfer gap around the missing intermediary.",
                )
            )
        if tokens.intersection({"outside", "muddy", "shoeprint"}):
            clues.append(
                (
                    "front_muddy_shoeprint",
                    "Fresh muddy shoeprints appear at the exterior boundary despite day records.",
                )
            )

        added_ids: list[str] = []
        discovered = set(self._discovered_clues(lineage_id))
        for clue_key, clue_text in clues:
            if clue_key in discovered:
                continue
            record = self._write_runtime_record(
                lineage_id=lineage_id,
                purpose=f"clue_{clue_key}",
                district="logical_analysis",
                content=f"Clue discovery ({clue_key}): {clue_text}",
                tags=self._runtime_tags(
                    kind="clue",
                    phase_id=phase_id,
                    location_id=location_id,
                    extra=[f"clue:{clue_key}"],
                ),
            )
            added_ids.append(record.record_id)
        return added_ids

    def _maybe_add_relationship_deltas(
        self,
        *,
        lineage_id: str,
        player_command: str,
        phase_id: str,
        location_id: str,
    ) -> list[str]:
        tokens = _word_tokens(player_command)
        deltas: list[tuple[str, str]] = []
        if "detective" in tokens:
            deltas.append(
                (
                    "player_detective",
                    "Detective alignment strengthened through cooperation.",
                )
            )
        if "lawyer" in tokens:
            deltas.append(
                (
                    "player_lawyer",
                    "Lawyer trust increased after legal cooperation.",
                )
            )
        if "thomas" in tokens or phase_id == "first_shift":
            deltas.append(
                (
                    "player_thomas",
                    "Thomas familiarity deepened during first-shift contact.",
                )
            )

        added_ids: list[str] = []
        discovered = set(self._relationship_delta_keys(lineage_id))
        for relationship_key, relationship_text in deltas:
            if relationship_key in discovered:
                continue
            record = self._write_runtime_record(
                lineage_id=lineage_id,
                purpose=f"relationship_{relationship_key}",
                district="emotional_processing",
                content=(
                    f"Relationship delta ({relationship_key}): {relationship_text} "
                    f"phase={phase_id}; location={location_id}"
                ),
                tags=self._runtime_tags(
                    kind="relationship_delta",
                    phase_id=phase_id,
                    location_id=location_id,
                    extra=[f"relationship:{relationship_key}"],
                ),
            )
            added_ids.append(record.record_id)
            discovered.add(relationship_key)
        return added_ids

    def _compose_slice_transcript(
        self,
        *,
        command: str,
        phase_id: str,
        location_id: str,
        clue_ids: list[str],
        relationship_ids: list[str],
        recap_triggered: bool,
    ) -> str:
        clue_text = ", ".join(clue_ids) if clue_ids else "none"
        relationship_text = ", ".join(relationship_ids) if relationship_ids else "none"
        recap_text = "Recap generated from stored state." if recap_triggered else "Recap pending."
        return (
            f"Command '{command.strip()}' resolved. "
            f"Phase={phase_id}; Location={location_id}; "
            f"Clues={clue_text}; Relationship deltas={relationship_text}. {recap_text}"
        )

    def _current_phase(self, lineage_id: str) -> str:
        for record in reversed(self._lineage_runtime_records(lineage_id)):
            marker_tag = next(
                (tag for tag in record.tags if tag.startswith("phase_state:")),
                None,
            )
            if marker_tag:
                return marker_tag.split(":", 1)[1]
        return "letter"

    def _current_location(self, lineage_id: str) -> str:
        for record in reversed(self._lineage_runtime_records(lineage_id)):
            marker_tag = next(
                (tag for tag in record.tags if tag.startswith("location_state:")),
                None,
            )
            if marker_tag:
                return marker_tag.split(":", 1)[1]
        return "great_hall"

    def _collect_recap_inputs(self, lineage_id: str) -> list[str]:
        important: list[str] = []
        for record in self._lineage_runtime_records(lineage_id):
            if any(
                tag
                in {
                    "kind:decision",
                    "kind:clue",
                    "kind:relationship_delta",
                    "kind:phase_transition",
                    "kind:recap",
                }
                for tag in record.tags
            ):
                important.append(record.record_id)
        return important[-6:]

    def _relationship_delta_keys(self, lineage_id: str) -> list[str]:
        keys = set()
        for record in self._lineage_runtime_records(lineage_id):
            for tag in record.tags:
                if tag.startswith("relationship:"):
                    keys.add(tag.split(":", 1)[1])
        return sorted(keys)

    def _discovered_clues(self, lineage_id: str) -> list[str]:
        clues = set()
        for record in self._lineage_runtime_records(lineage_id):
            for tag in record.tags:
                if tag.startswith("clue:"):
                    clues.add(tag.split(":", 1)[1])
        return sorted(clues)

    def _runtime_tags(
        self,
        *,
        kind: str,
        phase_id: str,
        location_id: str,
        extra: list[str] | None = None,
    ) -> list[str]:
        tags = [
            "topic:inheritance-manor",
            "scope:project",
            f"kind:{kind}",
            "layer:implementation",
            f"campaign:{self._campaign_id}",
            f"phase:{phase_id}",
            f"location:{location_id}",
        ]
        if extra:
            tags.extend(extra)
        return tags

    def _write_state_marker(
        self,
        *,
        lineage_id: str,
        marker_type: str,
        marker_value: str,
        phase_id: str,
        location_id: str,
        district: str,
    ) -> None:
        self._write_runtime_record(
            lineage_id=lineage_id,
            purpose=f"{marker_type}_{marker_value}",
            district=district,
            content=(
                f"State marker for lineage={lineage_id}: {marker_type}={marker_value}; "
                f"phase={phase_id}; location={location_id}"
            ),
            tags=self._runtime_tags(
                kind="state",
                phase_id=phase_id,
                location_id=location_id,
                extra=[f"{marker_type}_state:{marker_value}"],
            ),
        )

    def _write_runtime_record(
        self,
        *,
        lineage_id: str,
        purpose: str,
        district: str,
        content: str,
        tags: list[str],
    ) -> MemoryRecord:
        runtime_count = len(self._lineage_runtime_records(lineage_id)) + 1
        lineage_slug = _normalize_token(lineage_id)
        purpose_slug = _normalize_token(purpose)
        record_id = f"runtime_{lineage_slug}_slice_{runtime_count}_{purpose_slug}"
        record = MemoryRecord(
            record_id=record_id,
            content=content,
            district=district,
            tags=tags,
            project_id=self._project_id,
            memory_type="runtime",
            lineage_id=lineage_id,
        )
        self._memory_store.upsert(record)
        return record

    def _lineage_runtime_records(self, lineage_id: str) -> list[MemoryRecord]:
        return [
            record
            for record in sorted(
                self._memory_store.records.values(),
                key=lambda item: (_runtime_sequence(item.record_id), item.record_id),
            )
            if (
                record.memory_type == "runtime"
                and record.project_id == self._project_id
                and record.lineage_id == lineage_id
            )
        ]