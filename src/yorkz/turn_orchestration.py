from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from yorkz.memory_system import MemoryRecord, MemorySystem


WRITE_CATEGORIES = {
    "decision",
    "clue",
    "relationship_delta",
    "phase_transition",
    "recap",
    "loop_telemetry",
}


def _normalize_token(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned


def _word_tokens(value: str) -> set[str]:
    return {
        token
        for token in (_normalize_token(value).split("_"))
        if token
    }


@dataclass(slots=True)
class TurnInput:
    session_id: str
    project_id: str
    lineage_id: str
    player_command: str
    phase_hint: str | None = None
    location_hint: str | None = None
    recap_requested: bool = False

    def __post_init__(self) -> None:
        if not self.session_id.strip():
            raise ValueError("session_id is required.")
        if not self.project_id.strip():
            raise ValueError("project_id is required.")
        if not self.lineage_id.strip():
            raise ValueError("lineage_id is required.")
        if not self.player_command.strip():
            raise ValueError("player_command is required.")


@dataclass(slots=True)
class WriteIntent:
    category: str
    record_id: str
    district: str
    content: str
    tags: list[str]

    def __post_init__(self) -> None:
        if self.category not in WRITE_CATEGORIES:
            raise ValueError(f"Unsupported write category '{self.category}'.")


@dataclass(slots=True)
class TurnOutput:
    transcript_text: str
    affordances: list[str]
    current_phase_id: str
    current_location_id: str
    memory_write_summary: list[str]
    recap_trigger: bool
    write_intents: list[WriteIntent]
    recap_inputs: list[str]
    audit_trace: dict[str, Any] = field(default_factory=dict)


class TurnOrchestrator:
    """Framework-neutral turn orchestrator for the text-first runtime contract."""

    def __init__(self, *, memory_store: MemorySystem, project_id: str) -> None:
        if memory_store.project_id != project_id:
            raise ValueError(
                "TurnOrchestrator memory_store.project_id "
                f"'{memory_store.project_id}' does not match project_id '{project_id}'."
            )
        self._memory_store = memory_store
        self._project_id = project_id

    def process_turn(self, turn_input: TurnInput) -> TurnOutput:
        if turn_input.project_id != self._project_id:
            raise ValueError(
                f"Turn project_id '{turn_input.project_id}' does not match orchestrator project_id '{self._project_id}'."
            )

        authored_records, runtime_records = self._resolve_retrieval_context(
            lineage_id=turn_input.lineage_id,
        )
        current_phase_id = self._resolve_phase_id(runtime_records, turn_input.phase_hint)
        current_location_id = self._resolve_location_id(runtime_records, turn_input.location_hint)
        recap_inputs = self._resolve_recap_inputs(runtime_records, turn_input.recap_requested)

        turn_index = len(runtime_records) + 1
        write_intents = self._build_write_intents(
            turn_input=turn_input,
            turn_index=turn_index,
            current_phase_id=current_phase_id,
            current_location_id=current_location_id,
            runtime_records=runtime_records,
        )
        recap_trigger = turn_input.recap_requested or any(
            intent.category == "recap" for intent in write_intents
        )

        summary = [
            f"{intent.category}:{intent.record_id}"
            for intent in write_intents
        ]
        transcript = self._compose_transcript(
            turn_input.player_command,
            current_phase_id,
            current_location_id,
            write_intents,
            recap_trigger,
        )

        return TurnOutput(
            transcript_text=transcript,
            affordances=["inspect", "talk", "move", "wait", "recap"],
            current_phase_id=current_phase_id,
            current_location_id=current_location_id,
            memory_write_summary=summary,
            recap_trigger=recap_trigger,
            write_intents=write_intents,
            recap_inputs=recap_inputs,
            audit_trace={
                "authored_record_ids": sorted(record.record_id for record in authored_records),
                "runtime_record_ids": sorted(record.record_id for record in runtime_records),
                "lineage_id": turn_input.lineage_id,
            },
        )

    def _resolve_retrieval_context(self, *, lineage_id: str) -> tuple[list[MemoryRecord], list[MemoryRecord]]:
        authored_records = [
            record
            for record in self._memory_store.records.values()
            if record.memory_type == "authored" and record.project_id == self._project_id
        ]
        runtime_records = [
            record
            for record in self._memory_store.records.values()
            if (
                record.memory_type == "runtime"
                and record.project_id == self._project_id
                and record.lineage_id == lineage_id
            )
        ]
        return authored_records, runtime_records

    def _resolve_phase_id(self, runtime_records: list[MemoryRecord], phase_hint: str | None) -> str:
        for record in reversed(runtime_records):
            phase_tag = next((tag for tag in record.tags if tag.startswith("phase:")), None)
            if phase_tag:
                return phase_tag.split(":", 1)[1]
        if phase_hint:
            return phase_hint
        authored_phase_ids = sorted(
            record.record_id
            for record in self._memory_store.records.values()
            if record.memory_type == "authored" and record.record_id.startswith("phase_")
        )
        if authored_phase_ids:
            return authored_phase_ids[0]
        return "phase_unknown"

    def _resolve_location_id(self, runtime_records: list[MemoryRecord], location_hint: str | None) -> str:
        for record in reversed(runtime_records):
            location_tag = next((tag for tag in record.tags if tag.startswith("location:")), None)
            if location_tag:
                return location_tag.split(":", 1)[1]
        if location_hint:
            return location_hint
        authored_location_ids = sorted(
            record.record_id
            for record in self._memory_store.records.values()
            if record.memory_type == "authored" and record.record_id.startswith("loc_")
        )
        if authored_location_ids:
            return authored_location_ids[0]
        return "location_unknown"

    def _resolve_recap_inputs(self, runtime_records: list[MemoryRecord], recap_requested: bool) -> list[str]:
        if not recap_requested:
            return []
        important = []
        for record in runtime_records:
            if any(
                tag.startswith("kind:")
                and tag in {
                    "kind:decision",
                    "kind:clue",
                    "kind:relationship_delta",
                    "kind:phase_transition",
                    "kind:recap",
                }
                for tag in record.tags
            ):
                important.append(record.record_id)
        return important[-5:]

    def _classify_categories(
        self,
        *,
        player_command: str,
        recap_requested: bool,
        runtime_records: list[MemoryRecord],
    ) -> list[str]:
        command_tokens = _word_tokens(player_command)
        categories: list[str] = []

        if command_tokens.intersection({"look", "inspect", "search", "investigate"}):
            categories.append("clue")
        if command_tokens.intersection({"talk", "ask", "comfort", "threaten"}):
            categories.append("relationship_delta")
        if command_tokens.intersection({"move", "go", "enter", "leave", "take", "use"}):
            categories.append("decision")
        if command_tokens.intersection({"wait", "sleep", "night", "morning"}):
            categories.append("phase_transition")

        if recap_requested or "recap" in command_tokens:
            categories.append("recap")

        if self._is_repeated_command(player_command, runtime_records):
            categories.append("loop_telemetry")

        if not categories:
            categories.append("decision")
        return sorted(set(categories))

    def _is_repeated_command(self, player_command: str, runtime_records: list[MemoryRecord]) -> bool:
        normalized = player_command.strip().lower()
        normalized_token = _normalize_token(normalized)
        for record in reversed(runtime_records):
            existing_token_tag = next(
                (tag for tag in record.tags if tag.startswith("command_token:")),
                None,
            )
            if existing_token_tag:
                existing_token = existing_token_tag.split(":", 1)[1]
                if existing_token == normalized_token:
                    return True
                continue
            if "command=" in record.content:
                existing = record.content.split("command=", 1)[1].split(";", 1)[0].strip().lower()
                if existing == normalized:
                    return True
        return False

    def _compose_transcript(
        self,
        player_command: str,
        current_phase_id: str,
        current_location_id: str,
        write_intents: list[WriteIntent],
        recap_trigger: bool,
    ) -> str:
        categories = ", ".join(intent.category for intent in write_intents)
        recap_text = "Recap prepared from stored state." if recap_trigger else "Recap not requested."
        return (
            f"Processed command '{player_command.strip()}'. "
            f"Phase={current_phase_id}; Location={current_location_id}. "
            f"Write intents: {categories}. {recap_text}"
        )

    def _build_write_intents(
        self,
        *,
        turn_input: TurnInput,
        turn_index: int,
        current_phase_id: str,
        current_location_id: str,
        runtime_records: list[MemoryRecord],
    ) -> list[WriteIntent]:
        categories = self._classify_categories(
            player_command=turn_input.player_command,
            recap_requested=turn_input.recap_requested,
            runtime_records=runtime_records,
        )
        lineage_slug = _normalize_token(turn_input.lineage_id)
        command_token = _normalize_token(turn_input.player_command)
        intents = []
        for category in categories:
            record_id = f"runtime_{lineage_slug}_turn_{turn_index}_{category}"
            tags = [
                "topic:inheritance-manor",
                "scope:project",
                f"kind:{category}",
                "layer:implementation",
                f"phase:{current_phase_id}",
                f"location:{current_location_id}",
                f"campaign:{_normalize_token(self._project_id)}",
                f"command_token:{command_token}",
            ]
            intents.append(
                WriteIntent(
                    category=category,
                    record_id=record_id,
                    district="practical_execution",
                    content=f"lineage={turn_input.lineage_id}; command={turn_input.player_command.strip()}; category={category}",
                    tags=tags,
                )
            )
        return intents