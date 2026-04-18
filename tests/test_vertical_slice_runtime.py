from __future__ import annotations

from yorkz.vertical_slice_runtime import PlayableVerticalSliceRuntime


def test_full_playable_pass_reaches_morning_after() -> None:
    runtime = PlayableVerticalSliceRuntime.from_snapshot_file()
    lineage_id = "playthrough-alpha"

    runtime.play_turn(
        session_id="session-1",
        lineage_id=lineage_id,
        player_command="inspect letter seal",
    )
    runtime.play_turn(
        session_id="session-1",
        lineage_id=lineage_id,
        player_command="keep inheritance",
    )
    runtime.play_turn(
        session_id="session-1",
        lineage_id=lineage_id,
        player_command="follow detective and arrive at manor",
    )
    runtime.play_turn(
        session_id="session-1",
        lineage_id=lineage_id,
        player_command="inspect library ledger",
    )
    runtime.play_turn(
        session_id="session-1",
        lineage_id=lineage_id,
        player_command="wait for night",
    )
    runtime.play_turn(
        session_id="session-1",
        lineage_id=lineage_id,
        player_command="go outside to inspect muddy shoeprint",
    )
    final_turn = runtime.play_turn(
        session_id="session-1",
        lineage_id=lineage_id,
        player_command="wait until morning",
        recap_requested=True,
    )

    assert final_turn.phase_id == "morning_after"
    assert final_turn.location_id == "great_hall"
    assert final_turn.recap_triggered is True
    assert final_turn.recap_inputs


def test_clue_and_relationship_continuity_survive_day_night_transition() -> None:
    runtime = PlayableVerticalSliceRuntime.from_snapshot_file()
    lineage_id = "playthrough-beta"

    runtime.play_turn(
        session_id="session-2",
        lineage_id=lineage_id,
        player_command="inspect letter seal",
    )
    runtime.play_turn(
        session_id="session-2",
        lineage_id=lineage_id,
        player_command="follow detective and accept inheritance and arrive at manor",
    )
    runtime.play_turn(
        session_id="session-2",
        lineage_id=lineage_id,
        player_command="inspect library ledger",
    )
    runtime.play_turn(
        session_id="session-2",
        lineage_id=lineage_id,
        player_command="stay for night",
    )
    result = runtime.play_turn(
        session_id="session-2",
        lineage_id=lineage_id,
        player_command="talk to thomas before going outside",
    )
    runtime.play_turn(
        session_id="session-2",
        lineage_id=lineage_id,
        player_command="go outside and inspect muddy shoeprint",
    )

    final_turn = runtime.play_turn(
        session_id="session-2",
        lineage_id=lineage_id,
        player_command="wait until morning",
        recap_requested=True,
    )

    assert {
        "letter_irregular_seal",
        "library_ledger_gap",
        "front_muddy_shoeprint",
    }.issubset(set(final_turn.discovered_clues))
    assert "player_thomas" in result.relationship_deltas
    assert "player_detective" in result.relationship_deltas
    assert "player_thomas" in final_turn.relationship_deltas
    assert "player_detective" in final_turn.relationship_deltas


def test_relationship_delta_is_not_duplicated_across_first_shift_turns() -> None:
    runtime = PlayableVerticalSliceRuntime.from_snapshot_file()
    lineage_id = "playthrough-delta"

    runtime.play_turn(
        session_id="session-4",
        lineage_id=lineage_id,
        player_command="accept inheritance and arrive at manor",
    )
    runtime.play_turn(
        session_id="session-4",
        lineage_id=lineage_id,
        player_command="inspect library",
    )
    runtime.play_turn(
        session_id="session-4",
        lineage_id=lineage_id,
        player_command="wait for night",
    )
    runtime.play_turn(
        session_id="session-4",
        lineage_id=lineage_id,
        player_command="talk to thomas",
    )
    runtime.play_turn(
        session_id="session-4",
        lineage_id=lineage_id,
        player_command="go outside",
    )

    relationship_records = [
        record
        for record in runtime.memory_store.records.values()
        if (
            record.memory_type == "runtime"
            and record.lineage_id == lineage_id
            and "relationship:player_thomas" in record.tags
        )
    ]

    assert len(relationship_records) == 1


def test_recap_generated_from_stored_state_only_for_active_lineage() -> None:
    runtime = PlayableVerticalSliceRuntime.from_snapshot_file()

    runtime.play_turn(
        session_id="session-a",
        lineage_id="lineage-a",
        player_command="inspect library ledger",
    )
    runtime.play_turn(
        session_id="session-b",
        lineage_id="lineage-b",
        player_command="inspect letter seal",
    )

    result = runtime.play_turn(
        session_id="session-a",
        lineage_id="lineage-a",
        player_command="recap",
        recap_requested=True,
    )

    assert result.recap_triggered is True
    assert result.recap_inputs
    assert all("lineage_b" not in record_id for record_id in result.recap_inputs)


def test_snapshot_export_keeps_authored_runtime_boundary() -> None:
    runtime = PlayableVerticalSliceRuntime.from_snapshot_file()
    runtime.play_turn(
        session_id="session-3",
        lineage_id="lineage-gamma",
        player_command="inspect letter seal",
    )

    snapshot = runtime.memory_store.export_snapshot(
        campaign_id="inheritance-manor-prologue-v1"
    )

    assert snapshot.entries
    assert all(entry.memory_type == "authored" for entry in snapshot.entries)
    assert all(not entry.record_id.startswith("runtime_") for entry in snapshot.entries)
