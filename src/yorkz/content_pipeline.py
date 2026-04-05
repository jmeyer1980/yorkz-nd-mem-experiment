from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .memory_system import AUTHORED_ID_PREFIXES, MemorySystem, SnapshotPackage


INHERITANCE_MANOR_CAMPAIGN_TAG = "campaign:inheritance_manor"
PROLOGUE_FIRST_NIGHT_SLICE_TAG = "slice:prologue_first_night"
DEFAULT_DEDUPE_POLICY = "content_plus_tags"
CANONICAL_PROLOGUE_SNAPSHOT_RELATIVE_PATH = (
    Path("campaigns") / "inheritance-manor" / "prologue-snapshot.json"
)
REQUIRED_ENTRY_IDS = {
    "camp_inheritance_manor_prologue_first_night",
    "phase_letter",
    "phase_decision",
    "phase_arrival",
    "phase_interior_day",
    "phase_first_shift",
    "phase_morning_after",
    "loc_great_hall_day",
    "loc_great_hall_night",
    "loc_master_bedroom_day",
    "loc_master_bedroom_night",
    "loc_guest_bedroom_1_day",
    "loc_guest_bedroom_1_night",
    "loc_great_library_day",
    "loc_great_library_night",
    "loc_exterior_front_day",
    "loc_exterior_front_night",
    "npc_thomas_core",
    "npc_detective_core",
    "npc_lawyer_core",
    "rel_thomas_player_baseline",
    "rel_detective_player_baseline",
    "rel_lawyer_player_baseline",
    "hook_inheritance_notice",
    "hook_missing_intermediary",
    "hook_first_shift_trigger",
    "rule_outside_unsafe_at_night",
    "rule_safety_lies_inside",
    "rule_bounded_ambiguity",
    "clue_letter_signature_mismatch",
    "clue_ledger_missing_transfer",
    "clue_muddy_shoeprint",
    "recap_first_shift_template",
    "recap_morning_after_template",
}


def _path_has_relative_suffix(path: Path, suffix: Path) -> bool:
    if len(path.parts) < len(suffix.parts):
        return False
    normalized_path = tuple(part.lower() for part in path.parts[-len(suffix.parts) :])
    normalized_suffix = tuple(part.lower() for part in suffix.parts)
    return normalized_path == normalized_suffix


def _required_district_for_entry(record_id: str) -> str:
    prefix = record_id.split("_", 1)[0]
    if prefix in {"camp", "npc", "rel", "clue", "recap"}:
        return "logical_analysis"
    if prefix in {"phase", "hook"}:
        return "practical_execution"
    if prefix == "rule":
        return "vigilant_monitoring"
    if record_id == "loc_exterior_front_night":
        return "vigilant_monitoring"
    return "logical_analysis"


def _required_tags_for_entry(record_id: str) -> set[str]:
    if record_id == "camp_inheritance_manor_prologue_first_night":
        return {"phase:campaign_metadata", "mechanic:authored_snapshot"}

    prefix, remainder = record_id.split("_", 1)
    if prefix == "phase":
        return {f"phase:{remainder}"}
    if prefix == "loc":
        location, state = remainder.rsplit("_", 1)
        return {f"location:{location}", f"state:{state}"}
    if prefix == "npc":
        name, _role = remainder.rsplit("_", 1)
        return {f"npc:{name}"}
    if prefix == "rel":
        relationship_name = remainder.removesuffix("_baseline")
        npc_name = relationship_name.split("_", 1)[0]
        return {f"relationship:{relationship_name}", f"npc:{npc_name}"}
    if prefix == "hook":
        hook_expectations = {
            "hook_inheritance_notice": {"phase:letter", "mystery:inheritance_notice"},
            "hook_missing_intermediary": {
                "phase:interior_day",
                "mystery:missing_intermediary",
            },
            "hook_first_shift_trigger": {
                "phase:first_shift",
                "mechanic:day_night_cycle",
            },
        }
        return hook_expectations.get(record_id, set())
    if prefix == "rule":
        rule_expectations = {
            "rule_outside_unsafe_at_night": {"state:night", "mechanic:day_night_cycle"},
            "rule_safety_lies_inside": {"state:night", "mechanic:safe_room_logic"},
            "rule_bounded_ambiguity": {
                "mechanic:bounded_ambiguity",
                "mystery:interpretation_pressure",
            },
        }
        return rule_expectations.get(record_id, set())
    if prefix == "clue":
        clue_expectations = {
            "clue_letter_signature_mismatch": {"phase:letter", "mystery:signature_mismatch"},
            "clue_ledger_missing_transfer": {
                "location:great_library",
                "mystery:missing_intermediary",
            },
            "clue_muddy_shoeprint": {"location:exterior_front", "mystery:exterior_breach"},
        }
        return clue_expectations.get(record_id, set())
    if prefix == "recap":
        recap_expectations = {
            "recap_first_shift_template": {"phase:first_shift", "mechanic:recap"},
            "recap_morning_after_template": {"phase:morning_after", "mechanic:recap"},
        }
        return recap_expectations.get(record_id, set())
    return set()


@dataclass(slots=True)
class SnapshotValidationReport:
    entry_count: int
    connection_count: int
    category_counts: dict[str, int]
    errors: list[str]

    def require_valid(self) -> None:
        if not self.errors:
            return
        details = "\n- ".join(self.errors)
        raise ValueError(f"Invalid authored snapshot:\n- {details}")


def load_snapshot_file(path: str | Path) -> SnapshotPackage:
    snapshot_path = Path(path)
    with snapshot_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return SnapshotPackage.from_dict(data)


def write_snapshot_file(package: SnapshotPackage, path: str | Path) -> None:
    snapshot_path = Path(path)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    with snapshot_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(package.to_dict(), handle, indent=2)
        handle.write("\n")


def load_seed_pack(
    path: str | Path,
    *,
    project_id: str = "yorkz",
    require_canonical_path: bool = True,
) -> SnapshotPackage:
    snapshot_path = Path(path)
    if require_canonical_path and not _path_has_relative_suffix(
        snapshot_path,
        CANONICAL_PROLOGUE_SNAPSHOT_RELATIVE_PATH,
    ):
        raise ValueError(
            "Seed-pack loads must use the canonical production snapshot path "
            f"'{CANONICAL_PROLOGUE_SNAPSHOT_RELATIVE_PATH.as_posix()}'."
        )
    package = load_snapshot_file(snapshot_path)
    validate_authored_snapshot(package, project_id=project_id).require_valid()
    return package


def build_memory_system_from_snapshot(package: SnapshotPackage) -> MemorySystem:
    validate_authored_snapshot(package, project_id=package.project_id).require_valid()
    store = MemorySystem(project_id=package.project_id)
    store.import_snapshot(package)
    return store


def export_authored_snapshot_file(
    store: MemorySystem,
    path: str | Path,
    *,
    campaign_id: str,
    version: str = "0.1.0",
) -> SnapshotPackage:
    package = store.export_snapshot(campaign_id=campaign_id, version=version)
    write_snapshot_file(package, path)
    return package


def validate_authored_snapshot(
    package: SnapshotPackage,
    *,
    project_id: str,
    required_campaign_tag: str = INHERITANCE_MANOR_CAMPAIGN_TAG,
    required_slice_tag: str = PROLOGUE_FIRST_NIGHT_SLICE_TAG,
) -> SnapshotValidationReport:
    errors: list[str] = []
    category_counts = {prefix: 0 for prefix in sorted(AUTHORED_ID_PREFIXES)}

    if package.kind != "campaign_snapshot":
        errors.append("Snapshot kind must be 'campaign_snapshot'.")
    if package.project_id != project_id:
        errors.append(
            f"Snapshot project_id '{package.project_id}' does not match expected '{project_id}'."
        )
    if not package.preserve_ids:
        errors.append("Authored snapshots must preserve deterministic IDs.")
    if not package.merge_connections:
        errors.append("Authored snapshots must merge authored connections.")
    if package.dedupe != DEFAULT_DEDUPE_POLICY:
        errors.append(
            f"Authored snapshots must use dedupe policy '{DEFAULT_DEDUPE_POLICY}'."
        )

    entry_ids: list[str] = []
    for entry in package.entries:
        entry_ids.append(entry.record_id)
        prefix = entry.record_id.split("_", 1)[0]
        if prefix in category_counts:
            category_counts[prefix] += 1
        else:
            errors.append(f"Entry '{entry.record_id}' uses unknown authored prefix '{prefix}'.")
        if entry.project_id != project_id:
            errors.append(
                f"Entry '{entry.record_id}' uses project_id '{entry.project_id}' instead of '{project_id}'."
            )
        if entry.memory_type != "authored":
            errors.append(
                f"Entry '{entry.record_id}' must be authored, not '{entry.memory_type}'."
            )
        required_district = _required_district_for_entry(entry.record_id)
        if entry.district != required_district:
            errors.append(
                f"Entry '{entry.record_id}' must use district '{required_district}', not '{entry.district}'."
            )
        if required_campaign_tag not in entry.tags:
            errors.append(
                f"Entry '{entry.record_id}' is missing required tag '{required_campaign_tag}'."
            )
        if required_slice_tag not in entry.tags:
            errors.append(
                f"Entry '{entry.record_id}' is missing required tag '{required_slice_tag}'."
            )
        missing_semantic_tags = sorted(_required_tags_for_entry(entry.record_id) - set(entry.tags))
        if missing_semantic_tags:
            errors.append(
                f"Entry '{entry.record_id}' is missing semantic retrieval tags: {', '.join(missing_semantic_tags)}."
            )

    duplicate_ids = sorted(
        record_id for record_id in set(entry_ids) if entry_ids.count(record_id) > 1
    )
    if duplicate_ids:
        errors.append(f"Snapshot contains duplicate entry ids: {', '.join(duplicate_ids)}.")

    known_ids = set(entry_ids)
    missing_required = sorted(REQUIRED_ENTRY_IDS - known_ids)
    if missing_required:
        errors.append(
            "Snapshot is missing required authored anchors: "
            + ", ".join(missing_required)
            + "."
        )

    missing_connection_ids = sorted(
        {
            endpoint
            for left, right, _bidirectional in package.connections
            for endpoint in (left, right)
            if endpoint not in known_ids
        }
    )
    if missing_connection_ids:
        errors.append(
            "Snapshot connections reference unknown ids: "
            + ", ".join(missing_connection_ids)
            + "."
        )

    return SnapshotValidationReport(
        entry_count=len(package.entries),
        connection_count=len(package.connections),
        category_counts=category_counts,
        errors=errors,
    )


__all__ = [
    "CANONICAL_PROLOGUE_SNAPSHOT_RELATIVE_PATH",
    "DEFAULT_DEDUPE_POLICY",
    "INHERITANCE_MANOR_CAMPAIGN_TAG",
    "PROLOGUE_FIRST_NIGHT_SLICE_TAG",
    "REQUIRED_ENTRY_IDS",
    "SnapshotValidationReport",
    "build_memory_system_from_snapshot",
    "export_authored_snapshot_file",
    "load_seed_pack",
    "load_snapshot_file",
    "validate_authored_snapshot",
    "write_snapshot_file",
]