from __future__ import annotations

import pytest

from yorkz.memory_system import MemoryRecord, MemorySystem, make_authored_id
from yorkz.turn_orchestration import TurnInput, TurnOrchestrator


def _tags(*extra: str) -> list[str]:
    return [
        "topic:inheritance-manor",
        "scope:project",
        "kind:reference",
        "layer:architecture",
        "campaign:inheritance_manor",
        *extra,
    ]


def _build_store() -> MemorySystem:
    store = MemorySystem(project_id="yorkz")
    store.upsert(
        MemoryRecord(
            record_id=make_authored_id("phase", "arrival"),
            content="Arrival phase anchor.",
            district="logical_analysis",
            tags=_tags("phase:arrival"),
            project_id="yorkz",
            memory_type="authored",
        )
    )
    store.upsert(
        MemoryRecord(
            record_id=make_authored_id("loc", "great_hall", "day"),
            content="Great Hall day anchor.",
            district="logical_analysis",
            tags=_tags("location:great_hall", "state:day"),
            project_id="yorkz",
            memory_type="authored",
        )
    )
    return store


def test_turn_contract_rejects_empty_lineage_id() -> None:
    with pytest.raises(ValueError):
        TurnInput(
            session_id="s1",
            project_id="yorkz",
            lineage_id="",
            player_command="inspect desk",
        )


def test_runtime_retrieval_is_lineage_scoped() -> None:
    store = _build_store()
    store.upsert(
        MemoryRecord(
            record_id="runtime_a_1",
            content="lineage=lineage-a; command=inspect desk; category=clue",
            district="practical_execution",
            tags=_tags("kind:clue", "phase:arrival", "location:great_hall"),
            project_id="yorkz",
            memory_type="runtime",
            lineage_id="lineage-a",
        )
    )
    store.upsert(
        MemoryRecord(
            record_id="runtime_b_1",
            content="lineage=lineage-b; command=inspect desk; category=clue",
            district="practical_execution",
            tags=_tags("kind:clue", "phase:arrival", "location:great_hall"),
            project_id="yorkz",
            memory_type="runtime",
            lineage_id="lineage-b",
        )
    )

    orchestrator = TurnOrchestrator(memory_store=store, project_id="yorkz")
    output = orchestrator.process_turn(
        TurnInput(
            session_id="s1",
            project_id="yorkz",
            lineage_id="lineage-a",
            player_command="inspect desk",
        )
    )

    assert "runtime_a_1" in output.audit_trace["runtime_record_ids"]
    assert "runtime_b_1" not in output.audit_trace["runtime_record_ids"]
    assert output.audit_trace["lineage_id"] == "lineage-a"


def test_orchestrator_rejects_turn_input_for_other_project() -> None:
    store = _build_store()
    orchestrator = TurnOrchestrator(memory_store=store, project_id="yorkz")

    with pytest.raises(ValueError):
        orchestrator.process_turn(
            TurnInput(
                session_id="s1",
                project_id="not-yorkz",
                lineage_id="lineage-a",
                player_command="inspect desk",
            )
        )


def test_write_intents_are_deterministic_for_same_state() -> None:
    store = _build_store()
    orchestrator = TurnOrchestrator(memory_store=store, project_id="yorkz")

    turn_input = TurnInput(
        session_id="s1",
        project_id="yorkz",
        lineage_id="lineage-a",
        player_command="inspect desk",
    )
    first = orchestrator.process_turn(turn_input)
    second = orchestrator.process_turn(turn_input)

    assert [intent.record_id for intent in first.write_intents] == [
        intent.record_id for intent in second.write_intents
    ]
    assert [intent.category for intent in first.write_intents] == [
        intent.category for intent in second.write_intents
    ]


def test_recap_inputs_are_sourced_from_stored_runtime_state() -> None:
    store = _build_store()
    store.upsert(
        MemoryRecord(
            record_id="runtime_a_decision_1",
            content="lineage=lineage-a; command=go library; category=decision",
            district="practical_execution",
            tags=_tags("kind:decision", "phase:arrival", "location:great_hall"),
            project_id="yorkz",
            memory_type="runtime",
            lineage_id="lineage-a",
        )
    )
    store.upsert(
        MemoryRecord(
            record_id="runtime_a_clue_1",
            content="lineage=lineage-a; command=inspect portrait; category=clue",
            district="practical_execution",
            tags=_tags("kind:clue", "phase:arrival", "location:great_hall"),
            project_id="yorkz",
            memory_type="runtime",
            lineage_id="lineage-a",
        )
    )
    store.upsert(
        MemoryRecord(
            record_id="runtime_b_decision_1",
            content="lineage=lineage-b; command=go outside; category=decision",
            district="practical_execution",
            tags=_tags("kind:decision", "phase:arrival", "location:exterior_front"),
            project_id="yorkz",
            memory_type="runtime",
            lineage_id="lineage-b",
        )
    )

    orchestrator = TurnOrchestrator(memory_store=store, project_id="yorkz")
    output = orchestrator.process_turn(
        TurnInput(
            session_id="s1",
            project_id="yorkz",
            lineage_id="lineage-a",
            player_command="recap",
            recap_requested=True,
        )
    )

    assert output.recap_trigger is True
    assert set(output.recap_inputs) == {"runtime_a_decision_1", "runtime_a_clue_1"}
    assert "runtime_b_decision_1" not in output.recap_inputs


def test_classification_uses_whole_word_tokens() -> None:
    store = _build_store()
    orchestrator = TurnOrchestrator(memory_store=store, project_id="yorkz")

    output = orchestrator.process_turn(
        TurnInput(
            session_id="s1",
            project_id="yorkz",
            lineage_id="lineage-a",
            player_command="gorgeous weather",
        )
    )

    assert [intent.category for intent in output.write_intents] == ["decision"]


def test_write_intents_use_campaign_from_authored_tags_not_project_id() -> None:
    store = _build_store()
    orchestrator = TurnOrchestrator(memory_store=store, project_id="yorkz")

    output = orchestrator.process_turn(
        TurnInput(
            session_id="s1",
            project_id="yorkz",
            lineage_id="lineage-a",
            player_command="inspect desk",
        )
    )

    assert any("campaign:inheritance_manor" in intent.tags for intent in output.write_intents)
    assert all("campaign:yorkz" not in intent.tags for intent in output.write_intents)


def test_phase_and_location_defaults_are_normalized() -> None:
    store = _build_store()
    orchestrator = TurnOrchestrator(memory_store=store, project_id="yorkz")

    output = orchestrator.process_turn(
        TurnInput(
            session_id="s1",
            project_id="yorkz",
            lineage_id="lineage-a",
            player_command="wait",
        )
    )

    assert output.current_phase_id == "arrival"
    assert output.current_location_id == "great_hall"
    assert all("phase:phase_arrival" not in intent.tags for intent in output.write_intents)
    assert all("location:loc_great_hall_day" not in intent.tags for intent in output.write_intents)


def test_turn_input_campaign_id_overrides_authored_campaign_tag() -> None:
    store = _build_store()
    orchestrator = TurnOrchestrator(memory_store=store, project_id="yorkz")

    output = orchestrator.process_turn(
        TurnInput(
            session_id="s1",
            project_id="yorkz",
            lineage_id="lineage-a",
            player_command="inspect desk",
            campaign_id="inheritance-manor-prologue-v1",
        )
    )

    assert any("campaign:inheritance_manor_prologue_v1" in intent.tags for intent in output.write_intents)