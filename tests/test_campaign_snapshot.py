from __future__ import annotations

import json
from pathlib import Path

from yorkz.memory_system import MemoryRecord, SnapshotPackage


SNAPSHOT_PATH = Path("campaigns/inheritance-manor/prologue-snapshot.json")


def _load_snapshot() -> dict:
    return json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))


def test_snapshot_file_exists_and_is_valid_snapshot_package() -> None:
    data = _load_snapshot()
    package = SnapshotPackage.from_dict(data)

    assert package.kind == "campaign_snapshot"
    assert package.project_id == "yorkz"
    assert package.campaign_id == "inheritance-manor-prologue-v1"
    assert package.preserve_ids is True
    assert package.merge_connections is True
    assert package.dedupe == "content_plus_tags"
    assert len(package.entries) >= 25


def test_snapshot_entries_are_authored_and_runtime_free() -> None:
    package = SnapshotPackage.from_dict(_load_snapshot())

    assert package.entries
    for entry in package.entries:
        assert isinstance(entry, MemoryRecord)
        assert entry.memory_type == "authored"
        assert entry.project_id == "yorkz"
        assert entry.record_id.startswith((
            "camp_",
            "phase_",
            "loc_",
            "npc_",
            "hook_",
            "clue_",
            "rule_",
            "rel_",
            "recap_",
        ))


def test_snapshot_includes_required_mvp_category_minimums() -> None:
    package = SnapshotPackage.from_dict(_load_snapshot())
    entries = package.entries

    by_prefix: dict[str, int] = {
        "camp": 0,
        "phase": 0,
        "loc": 0,
        "npc": 0,
        "rel": 0,
        "hook": 0,
        "rule": 0,
        "clue": 0,
        "recap": 0,
    }
    for entry in entries:
        prefix = entry.record_id.split("_", 1)[0]
        if prefix in by_prefix:
            by_prefix[prefix] += 1

    assert by_prefix["camp"] >= 1
    assert by_prefix["phase"] >= 6
    assert by_prefix["loc"] >= 5
    assert by_prefix["npc"] >= 3
    assert by_prefix["rel"] >= 3
    assert by_prefix["hook"] >= 3
    assert by_prefix["rule"] >= 3
    assert by_prefix["clue"] >= 3
    assert by_prefix["recap"] >= 2


def test_snapshot_entries_use_canonical_and_game_tags() -> None:
    package = SnapshotPackage.from_dict(_load_snapshot())

    canonical = ("topic:", "scope:", "kind:", "layer:")
    game_prefixes = (
        "campaign:",
        "slice:",
        "phase:",
        "location:",
        "state:",
        "npc:",
        "relationship:",
        "mystery:",
        "mechanic:",
        "hook:",
        "rule:",
        "clue:",
        "recap:",
    )

    for entry in package.entries:
        tags = entry.tags
        for required_prefix in canonical:
            assert any(tag.startswith(required_prefix) for tag in tags)
        assert any(tag.startswith(prefix) for prefix in game_prefixes for tag in tags)


def test_snapshot_connections_reference_known_entry_ids() -> None:
    package = SnapshotPackage.from_dict(_load_snapshot())

    known_ids = {entry.record_id for entry in package.entries}
    assert package.connections
    for left, right, _bidirectional in package.connections:
        assert left in known_ids
        assert right in known_ids
