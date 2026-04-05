from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from yorkz.memory_system import MemoryRecord, MemorySystem, SearchFilters, SnapshotPackage, make_authored_id


def build_tags(*extra: str) -> list[str]:
    return [
        "topic:inheritance-manor",
        "scope:project",
        "kind:reference",
        "layer:architecture",
        *extra,
    ]


def test_authored_record_requires_deterministic_prefix() -> None:
    with pytest.raises(ValueError):
        MemoryRecord(
            record_id="room_great_hall",
            content="Invalid authored id.",
            district="logical_analysis",
            tags=build_tags("campaign:inheritance_manor"),
            project_id="yorkz",
            memory_type="authored",
        )


def test_missing_canonical_tags_is_rejected() -> None:
    with pytest.raises(ValueError):
        MemoryRecord(
            record_id=make_authored_id("npc", "thomas", "core"),
            content="Thomas baseline anchor.",
            district="logical_analysis",
            tags=["topic:inheritance-manor", "kind:reference"],
            project_id="yorkz",
            memory_type="authored",
        )


def test_missing_game_facing_tags_is_rejected() -> None:
    with pytest.raises(ValueError):
        MemoryRecord(
            record_id=make_authored_id("npc", "thomas", "core"),
            content="Thomas baseline anchor.",
            district="logical_analysis",
            tags=[
                "topic:inheritance-manor",
                "scope:project",
                "kind:reference",
                "layer:architecture",
            ],
            project_id="yorkz",
            memory_type="authored",
        )


def test_authored_runtime_split_cannot_be_overwritten() -> None:
    store = MemorySystem(project_id="yorkz")
    authored = MemoryRecord(
        record_id=make_authored_id("loc", "great_hall", "day"),
        content="Great Hall daylight anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "state:day", "location:great_hall"),
        project_id="yorkz",
        memory_type="authored",
    )
    store.upsert(authored)

    with pytest.raises(ValueError):
        store.upsert(
            MemoryRecord(
                record_id=authored.record_id,
                content="A mutable runtime note should not replace authored state.",
                district="practical_execution",
                tags=build_tags("kind:state", "campaign:inheritance_manor"),
                project_id="yorkz",
                memory_type="runtime",
            )
        )


def test_search_uses_bm25_and_filters() -> None:
    store = MemorySystem(project_id="yorkz")
    store.upsert(
        MemoryRecord(
            record_id=make_authored_id("clue", "library", "ledger"),
            content="Library ledger clue about the missing intermediary and payments.",
            district="logical_analysis",
            tags=build_tags("campaign:inheritance_manor", "location:great_library", "kind:reference"),
            project_id="yorkz",
            memory_type="authored",
        )
    )
    store.upsert(
        MemoryRecord(
            record_id="runtime_theory_1",
            content="The detective suspects the lawyer is hiding the intermediary transfer.",
            district="creative_synthesis",
            tags=build_tags("kind:state", "npc:detective", "relationship:suspicion"),
            project_id="yorkz",
            memory_type="runtime",
            intensity=0.8,
        )
    )

    results = store.search(
        "missing intermediary ledger",
        filters=SearchFilters(district="logical_analysis"),
    )

    assert [result.record.record_id for result in results] == ["clue_library_ledger"]


def test_connections_and_traversal_are_bidirectional() -> None:
    store = MemorySystem(project_id="yorkz")
    room = MemoryRecord(
        record_id=make_authored_id("loc", "great_hall", "day"),
        content="Great Hall daylight anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "state:day", "location:great_hall"),
        project_id="yorkz",
        memory_type="authored",
    )
    npc = MemoryRecord(
        record_id=make_authored_id("npc", "thomas", "core"),
        content="Thomas baseline anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "npc:thomas"),
        project_id="yorkz",
        memory_type="authored",
    )
    clue = MemoryRecord(
        record_id=make_authored_id("clue", "front", "muddy_shoeprint"),
        content="Fresh mud outside the front entrance.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "location:exterior_front"),
        project_id="yorkz",
        memory_type="authored",
    )
    for record in (room, npc, clue):
        store.upsert(record)
    store.connect(room.record_id, npc.record_id)
    store.connect(npc.record_id, clue.record_id)

    assert store.traverse(room.record_id, max_depth=2) == [
        room.record_id,
        npc.record_id,
        clue.record_id,
    ]


def test_distillation_creates_logical_record_and_connection() -> None:
    store = MemorySystem(project_id="yorkz")
    source = MemoryRecord(
        record_id="runtime_emotion_1",
        content="Thomas reacts with visible fear whenever the front doors are mentioned.",
        district="emotional_processing",
        tags=build_tags("kind:state", "npc:thomas", "mystery:exterior_danger"),
        project_id="yorkz",
        memory_type="runtime",
        emotional_valence=-0.7,
        intensity=0.9,
    )
    store.upsert(source)

    distilled = store.distill_emotional_memory(
        source.record_id,
        distilled_id="runtime_distilled_1",
        content="Thomas treats the exterior as a danger trigger rather than a neutral exit.",
        tags=build_tags("kind:insight", "npc:thomas", "mystery:exterior_danger"),
    )

    assert distilled.district == "logical_analysis"
    assert distilled.source_ids == (source.record_id,)
    assert store.traverse(source.record_id, max_depth=1) == [source.record_id, distilled.record_id]


def test_snapshot_roundtrip_keeps_authored_entries_and_connections() -> None:
    store = MemorySystem(project_id="yorkz")
    room = MemoryRecord(
        record_id=make_authored_id("loc", "great_library", "night"),
        content="Night-time library anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "location:great_library", "state:night"),
        project_id="yorkz",
        memory_type="authored",
    )
    rule = MemoryRecord(
        record_id=make_authored_id("rule", "outside", "unsafe", "at", "night"),
        content="Outside is unsafe at night.",
        district="vigilant_monitoring",
        tags=build_tags("campaign:inheritance_manor", "state:night", "mechanic:day_night_cycle"),
        project_id="yorkz",
        memory_type="authored",
    )
    runtime = MemoryRecord(
        record_id="runtime_choice_1",
        content="Player chose to stay inside.",
        district="practical_execution",
        tags=build_tags("kind:state", "phase:first_shift"),
        project_id="yorkz",
        memory_type="runtime",
    )
    for record in (room, rule, runtime):
        store.upsert(record)
    store.connect(room.record_id, rule.record_id)
    store.connect(rule.record_id, runtime.record_id)

    snapshot = store.export_snapshot(campaign_id="inheritance-manor-prologue-v1")
    restored = MemorySystem(project_id="yorkz")
    restored.import_snapshot(SnapshotPackage.from_dict(snapshot.to_dict()))

    assert sorted(restored.records) == [room.record_id, rule.record_id]
    assert restored.traverse(room.record_id, max_depth=1) == [room.record_id, rule.record_id]


def test_directed_snapshot_roundtrip_preserves_edge_direction() -> None:
    store = MemorySystem(project_id="yorkz")
    source = MemoryRecord(
        record_id=make_authored_id("hook", "first", "shift", "trigger"),
        content="First-shift trigger anchor.",
        district="practical_execution",
        tags=build_tags("campaign:inheritance_manor", "phase:first_shift", "kind:decision"),
        project_id="yorkz",
        memory_type="authored",
    )
    target = MemoryRecord(
        record_id=make_authored_id("rule", "outside", "unsafe", "at", "night"),
        content="Outside is unsafe at night.",
        district="vigilant_monitoring",
        tags=build_tags("campaign:inheritance_manor", "state:night", "mechanic:day_night_cycle"),
        project_id="yorkz",
        memory_type="authored",
    )
    for record in (source, target):
        store.upsert(record)
    store.connect(target.record_id, source.record_id, bidirectional=False)

    snapshot = store.export_snapshot(campaign_id="inheritance-manor-prologue-v1")
    restored = MemorySystem(project_id="yorkz")
    restored.import_snapshot(SnapshotPackage.from_dict(snapshot.to_dict()))

    assert restored.traverse(target.record_id, max_depth=1) == [target.record_id, source.record_id]
    assert restored.traverse(source.record_id, max_depth=1) == [source.record_id]


def test_snapshot_import_honors_dedupe_and_preserve_id_flags() -> None:
    existing_room = MemoryRecord(
        record_id=make_authored_id("loc", "great_hall", "day"),
        content="Great Hall daylight anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "state:day", "location:great_hall"),
        project_id="yorkz",
        memory_type="authored",
    )

    dedupe_store = MemorySystem(project_id="yorkz")
    dedupe_store.upsert(existing_room)
    dedupe_snapshot = SnapshotPackage(
        campaign_id="inheritance-manor-prologue-v1",
        project_id="yorkz",
        preserve_ids=True,
        dedupe="content_plus_tags",
        entries=[
            MemoryRecord(
                record_id=make_authored_id("loc", "great_hall", "day", "duplicate"),
                content=existing_room.content,
                district=existing_room.district,
                tags=list(existing_room.tags),
                project_id="yorkz",
                memory_type="authored",
            )
        ],
    )
    dedupe_store.import_snapshot(dedupe_snapshot)

    assert sorted(dedupe_store.records) == [existing_room.record_id]

    preserve_store = MemorySystem(project_id="yorkz")
    preserve_store.upsert(existing_room)
    preserve_snapshot = SnapshotPackage(
        campaign_id="inheritance-manor-prologue-v1",
        project_id="yorkz",
        preserve_ids=False,
        dedupe="none",
        entries=[
            MemoryRecord(
                record_id=existing_room.record_id,
                content="Duplicate Great Hall anchor copied for test import.",
                district="logical_analysis",
                tags=build_tags("campaign:inheritance_manor", "state:day", "location:great_hall"),
                project_id="yorkz",
                memory_type="authored",
            )
        ],
    )
    preserve_store.import_snapshot(preserve_snapshot)

    assert sorted(preserve_store.records) == [
        existing_room.record_id,
        f"{existing_room.record_id}_copy_1",
    ]


def test_snapshot_dedupe_does_not_collapse_authored_onto_runtime() -> None:
    store = MemorySystem(project_id="yorkz")
    runtime_record = MemoryRecord(
        record_id="runtime_room_note_1",
        content="Great Hall daylight anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "state:day", "location:great_hall"),
        project_id="yorkz",
        memory_type="runtime",
    )
    authored_record = MemoryRecord(
        record_id=make_authored_id("loc", "great_hall", "day"),
        content=runtime_record.content,
        district=runtime_record.district,
        tags=list(runtime_record.tags),
        project_id="yorkz",
        memory_type="authored",
    )
    store.upsert(runtime_record)

    store.import_snapshot(
        SnapshotPackage(
            campaign_id="inheritance-manor-prologue-v1",
            project_id="yorkz",
            preserve_ids=True,
            dedupe="content_plus_tags",
            entries=[authored_record],
        )
    )

    assert sorted(store.records) == [authored_record.record_id, runtime_record.record_id]


def test_stats_count_one_way_connections() -> None:
    store = MemorySystem(project_id="yorkz")
    room = MemoryRecord(
        record_id=make_authored_id("loc", "great_hall", "day"),
        content="Great Hall daylight anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "state:day", "location:great_hall"),
        project_id="yorkz",
        memory_type="authored",
    )
    hook = MemoryRecord(
        record_id=make_authored_id("hook", "missing", "intermediary"),
        content="The intermediary has vanished.",
        district="practical_execution",
        tags=build_tags("campaign:inheritance_manor", "kind:decision", "mystery:missing_person_pressure"),
        project_id="yorkz",
        memory_type="authored",
    )
    for record in (room, hook):
        store.upsert(record)

    store.connect(room.record_id, hook.record_id, bidirectional=False)

    assert store.stats().connection_count == 1


@dataclass
class FakeGateway:
    stored_payloads: list[dict] = field(default_factory=list)
    connected_pairs: list[tuple[str, str, bool]] = field(default_factory=list)
    imported_payloads: list[dict] = field(default_factory=list)

    def store_memory(self, payload: dict) -> str:
        self.stored_payloads.append(payload)
        return f"remote_{len(self.stored_payloads)}"

    def connect_memories(self, memory_id_1: str, memory_id_2: str, *, bidirectional: bool = True) -> None:
        self.connected_pairs.append((memory_id_1, memory_id_2, bidirectional))

    def import_memories(self, payload: dict) -> dict:
        self.imported_payloads.append(payload)
        return {"imported": len(payload["entries"])}


def test_gateway_sync_and_snapshot_import_contract() -> None:
    store = MemorySystem(project_id="yorkz")
    room = MemoryRecord(
        record_id=make_authored_id("loc", "great_hall", "day"),
        content="Great Hall daylight anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "state:day", "location:great_hall"),
        project_id="yorkz",
        memory_type="authored",
    )
    npc = MemoryRecord(
        record_id=make_authored_id("npc", "thomas", "core"),
        content="Thomas baseline anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "npc:thomas"),
        project_id="yorkz",
        memory_type="authored",
    )
    for record in (room, npc):
        store.upsert(record)
    store.connect(room.record_id, npc.record_id)

    gateway = FakeGateway()
    synced = store.sync_to_gateway(gateway)
    imported = store.import_authored_snapshot_to_gateway(
        gateway,
        campaign_id="inheritance-manor-prologue-v1",
    )

    assert synced == {
        room.record_id: "remote_1",
        npc.record_id: "remote_2",
    }
    assert gateway.connected_pairs == [("remote_1", "remote_2", True)]
    assert imported == {"imported": 2}
    assert gateway.imported_payloads[0]["preserve_ids"] is True


def test_gateway_sync_preserves_directed_edges() -> None:
    store = MemorySystem(project_id="yorkz")
    source = MemoryRecord(
        record_id=make_authored_id("hook", "first", "shift", "trigger"),
        content="First-shift trigger anchor.",
        district="practical_execution",
        tags=build_tags("campaign:inheritance_manor", "phase:first_shift", "kind:decision"),
        project_id="yorkz",
        memory_type="authored",
    )
    target = MemoryRecord(
        record_id=make_authored_id("rule", "outside", "unsafe", "at", "night"),
        content="Outside is unsafe at night.",
        district="vigilant_monitoring",
        tags=build_tags("campaign:inheritance_manor", "state:night", "mechanic:day_night_cycle"),
        project_id="yorkz",
        memory_type="authored",
    )
    for record in (source, target):
        store.upsert(record)
    store.connect(target.record_id, source.record_id, bidirectional=False)

    gateway = FakeGateway()
    store.sync_to_gateway(gateway)

    assert gateway.connected_pairs == [("remote_2", "remote_1", False)]


def test_gateway_sync_allows_explicit_empty_record_selection() -> None:
    store = MemorySystem(project_id="yorkz")
    store.upsert(
        MemoryRecord(
            record_id=make_authored_id("npc", "thomas", "core"),
            content="Thomas baseline anchor.",
            district="logical_analysis",
            tags=build_tags("campaign:inheritance_manor", "npc:thomas"),
            project_id="yorkz",
            memory_type="authored",
        )
    )

    gateway = FakeGateway()

    assert store.sync_to_gateway(gateway, record_ids=[]) == {}
    assert gateway.stored_payloads == []

def test_lineage_id_is_included_in_snapshot_and_payload() -> None:
    record = MemoryRecord(
        record_id="runtime_session_note_1",
        content="Player examined the cellar door in run 2.",
        district="practical_execution",
        tags=build_tags("kind:state", "phase:first_shift", "location:cellar"),
        project_id="yorkz",
        memory_type="runtime",
        lineage_id="run_2026_prologue_01",
    )

    payload = record.to_memory_payload()
    assert payload["lineage_id"] == "run_2026_prologue_01"

    entry = record.to_snapshot_entry()
    assert entry["lineage_id"] == "run_2026_prologue_01"

    restored = MemoryRecord.from_snapshot_entry({**entry, "id": entry["id"]})
    assert restored.lineage_id == "run_2026_prologue_01"


def test_lineage_id_absent_when_not_set() -> None:
    record = MemoryRecord(
        record_id="runtime_session_note_2",
        content="Player examined the cellar door.",
        district="practical_execution",
        tags=build_tags("kind:state", "phase:first_shift", "location:cellar"),
        project_id="yorkz",
        memory_type="runtime",
    )
    assert "lineage_id" not in record.to_memory_payload()
    assert "lineage_id" not in record.to_snapshot_entry()


def test_import_snapshot_raises_on_unknown_connection_endpoint() -> None:
    known = MemoryRecord(
        record_id=make_authored_id("loc", "great_hall", "day"),
        content="Great Hall daylight anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "state:day", "location:great_hall"),
        project_id="yorkz",
        memory_type="authored",
    )
    package = SnapshotPackage(
        campaign_id="test-snapshot",
        project_id="yorkz",
        preserve_ids=True,
        dedupe="none",
        entries=[known],
        connections=[(known.record_id, "nonexistent_id_xyz", True)],
    )
    store = MemorySystem(project_id="yorkz")
    with pytest.raises(ValueError, match="nonexistent_id_xyz"):
        store.import_snapshot(package)


def test_sync_to_gateway_deduplicates_record_ids() -> None:
    store = MemorySystem(project_id="yorkz")
    record = MemoryRecord(
        record_id=make_authored_id("npc", "thomas", "core"),
        content="Thomas baseline anchor.",
        district="logical_analysis",
        tags=build_tags("campaign:inheritance_manor", "npc:thomas"),
        project_id="yorkz",
        memory_type="authored",
    )
    store.upsert(record)

    gateway = FakeGateway()
    synced = store.sync_to_gateway(
        gateway, record_ids=[record.record_id, record.record_id, record.record_id]
    )

    assert len(gateway.stored_payloads) == 1
    assert synced == {record.record_id: "remote_1"}
