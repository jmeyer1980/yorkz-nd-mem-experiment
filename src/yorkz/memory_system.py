from __future__ import annotations

import math
import re
from collections import Counter, deque
from dataclasses import dataclass, field
from typing import Any, Protocol


CANONICAL_TAG_PREFIXES = ("topic", "scope", "kind", "layer")
GAME_TAG_PREFIXES = (
    "campaign",
    "slice",
    "phase",
    "location",
    "state",
    "npc",
    "relationship",
    "mystery",
    "mechanic",
)
ALLOWED_DISTRICTS = {
    "logical_analysis",
    "emotional_processing",
    "practical_execution",
    "vigilant_monitoring",
    "creative_synthesis",
}
ALLOWED_MEMORY_TYPES = {"authored", "runtime"}
ALLOWED_EPISTEMIC_STATUSES = {"draft", "validated", "outdated"}
AUTHORED_ID_PREFIXES = {
    "camp": "campaign metadata",
    "phase": "phase anchors",
    "loc": "rooms and room-state anchors",
    "npc": "characters",
    "hook": "plot hooks",
    "clue": "clue anchors",
    "rule": "authored world rules",
    "rel": "relationship baselines",
    "recap": "recap templates",
}
TOKEN_RE = re.compile(r"[a-z0-9_]+")


def _normalize_token(token: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", token.lower()).strip("_")
    if not cleaned:
        raise ValueError("Deterministic ID parts must contain letters or numbers.")
    return cleaned


def make_authored_id(prefix: str, *parts: str) -> str:
    normalized_prefix = _normalize_token(prefix)
    if normalized_prefix not in AUTHORED_ID_PREFIXES:
        raise ValueError(
            f"Unknown authored prefix '{prefix}'. Expected one of: {', '.join(sorted(AUTHORED_ID_PREFIXES))}."
        )
    normalized_parts = [_normalize_token(part) for part in parts]
    if not normalized_parts:
        raise ValueError("At least one deterministic ID part is required.")
    return "_".join([normalized_prefix, *normalized_parts])


def canonical_tag_map(tags: list[str]) -> dict[str, set[str]]:
    grouped: dict[str, set[str]] = {prefix: set() for prefix in CANONICAL_TAG_PREFIXES}
    for tag in tags:
        if ":" not in tag:
            continue
        prefix, value = tag.split(":", 1)
        if prefix in grouped and value:
            grouped[prefix].add(value)
    return grouped


def validate_tags(tags: list[str]) -> None:
    if not tags:
        raise ValueError("Every memory must carry canonical and project tags.")

    missing = [
        prefix for prefix, values in canonical_tag_map(tags).items() if not values
    ]
    if missing:
        raise ValueError(
            f"Missing canonical tag families: {', '.join(sorted(missing))}."
        )

    has_game_scope = False
    for tag in tags:
        if ":" not in tag:
            continue
        prefix, value = tag.split(":", 1)
        if prefix in GAME_TAG_PREFIXES and value:
            has_game_scope = True
            break
    if not has_game_scope:
        raise ValueError(
            "Every memory must include at least one game-facing retrieval tag."
        )


def tokenize(value: str) -> list[str]:
    return TOKEN_RE.findall(value.lower())


@dataclass(slots=True)
class MemoryRecord:
    record_id: str
    content: str
    district: str
    tags: list[str]
    project_id: str
    memory_type: str = "runtime"
    emotional_valence: float | None = None
    intensity: float | None = None
    epistemic_status: str = "validated"
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.district not in ALLOWED_DISTRICTS:
            raise ValueError(f"Unsupported district '{self.district}'.")
        if self.memory_type not in ALLOWED_MEMORY_TYPES:
            raise ValueError(f"Unsupported memory_type '{self.memory_type}'.")
        if self.epistemic_status not in ALLOWED_EPISTEMIC_STATUSES:
            raise ValueError(
                f"Unsupported epistemic_status '{self.epistemic_status}'."
            )
        if not self.record_id:
            raise ValueError("Every memory needs a record_id.")
        if not self.project_id:
            raise ValueError("Every memory needs a project_id.")
        if not self.content.strip():
            raise ValueError("Memory content must not be empty.")
        validate_tags(self.tags)
        if self.memory_type == "authored":
            prefix = self.record_id.split("_", 1)[0]
            if prefix not in AUTHORED_ID_PREFIXES:
                raise ValueError(
                    "Authored memories must use a deterministic domain prefix."
                )
        if self.emotional_valence is not None and not -1.0 <= self.emotional_valence <= 1.0:
            raise ValueError("emotional_valence must be between -1 and 1.")
        if self.intensity is not None and not 0.0 <= self.intensity <= 1.0:
            raise ValueError("intensity must be between 0 and 1.")

    @property
    def search_document(self) -> str:
        return " ".join([self.record_id, self.content, *self.tags])

    def to_memory_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "content": self.content,
            "district": self.district,
            "tags": list(self.tags),
            "project_id": self.project_id,
            "epistemic_status": self.epistemic_status,
        }
        if self.emotional_valence is not None:
            payload["emotional_valence"] = self.emotional_valence
        if self.intensity is not None:
            payload["intensity"] = self.intensity
        return payload

    def to_snapshot_entry(self) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "id": self.record_id,
            "content": self.content,
            "district": self.district,
            "tags": list(self.tags),
            "project_id": self.project_id,
            "epistemic_status": self.epistemic_status,
            "memory_type": self.memory_type,
        }
        if self.emotional_valence is not None:
            entry["emotional_valence"] = self.emotional_valence
        if self.intensity is not None:
            entry["intensity"] = self.intensity
        if self.source_ids:
            entry["source_ids"] = list(self.source_ids)
        return entry

    @classmethod
    def from_snapshot_entry(cls, entry: dict[str, Any]) -> "MemoryRecord":
        return cls(
            record_id=entry["id"],
            content=entry["content"],
            district=entry["district"],
            tags=list(entry["tags"]),
            project_id=entry["project_id"],
            memory_type=entry.get("memory_type", "authored"),
            emotional_valence=entry.get("emotional_valence"),
            intensity=entry.get("intensity"),
            epistemic_status=entry.get("epistemic_status", "validated"),
            source_ids=tuple(entry.get("source_ids", ())),
        )


@dataclass(slots=True)
class SearchFilters:
    district: str | None = None
    tags: set[str] = field(default_factory=set)
    emotional_valence_min: float | None = None
    emotional_valence_max: float | None = None
    intensity_min: float | None = None
    intensity_max: float | None = None


@dataclass(slots=True)
class SearchResult:
    record: MemoryRecord
    score: float


@dataclass(slots=True)
class MemoryStats:
    total_count: int
    per_district: dict[str, int]
    connection_count: int


@dataclass(slots=True)
class SnapshotPackage:
    campaign_id: str
    project_id: str
    entries: list[MemoryRecord]
    version: str = "0.1.0"
    kind: str = "campaign_snapshot"
    preserve_ids: bool = True
    merge_connections: bool = True
    dedupe: str = "content_plus_tags"
    connections: list[tuple[str, str, bool]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "project_id": self.project_id,
            "kind": self.kind,
            "version": self.version,
            "preserve_ids": self.preserve_ids,
            "merge_connections": self.merge_connections,
            "dedupe": self.dedupe,
            "entries": [entry.to_snapshot_entry() for entry in self.entries],
            "connections": [
                {
                    "from": left,
                    "to": right,
                    "bidirectional": bidirectional,
                }
                for left, right, bidirectional in self.connections
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SnapshotPackage":
        entries = [MemoryRecord.from_snapshot_entry(item) for item in data.get("entries", [])]
        connections: list[tuple[str, str, bool]] = []
        for edge in data.get("connections", []):
            if isinstance(edge, dict):
                connections.append(
                    (edge["from"], edge["to"], edge.get("bidirectional", True))
                )
            elif len(edge) == 3:
                left, right, bidirectional = edge
                connections.append((left, right, bool(bidirectional)))
            else:
                left, right = edge
                connections.append((left, right, True))
        return cls(
            campaign_id=data["campaign_id"],
            project_id=data["project_id"],
            kind=data.get("kind", "campaign_snapshot"),
            version=data.get("version", "0.1.0"),
            preserve_ids=data.get("preserve_ids", True),
            merge_connections=data.get("merge_connections", True),
            dedupe=data.get("dedupe", "content_plus_tags"),
            entries=entries,
            connections=connections,
        )


class NeurodivergentMemoryGateway(Protocol):
    def store_memory(self, payload: dict[str, Any]) -> str: ...

    def connect_memories(self, memory_id_1: str, memory_id_2: str, *, bidirectional: bool = True) -> None: ...

    def import_memories(self, payload: dict[str, Any]) -> dict[str, Any]: ...


class MemorySystem:
    def __init__(self, *, project_id: str) -> None:
        self.project_id = project_id
        self._records: dict[str, MemoryRecord] = {}
        self._connections: dict[str, set[str]] = {}

    @property
    def records(self) -> dict[str, MemoryRecord]:
        return dict(self._records)

    def upsert(self, record: MemoryRecord) -> MemoryRecord:
        if record.project_id != self.project_id:
            raise ValueError(
                f"Memory project_id '{record.project_id}' does not match store project_id '{self.project_id}'."
            )
        existing = self._records.get(record.record_id)
        if existing and existing.memory_type != record.memory_type:
            raise ValueError(
                f"Cannot overwrite {existing.memory_type} memory '{record.record_id}' with {record.memory_type} memory."
            )
        self._records[record.record_id] = record
        self._connections.setdefault(record.record_id, set())
        return record

    def get(self, record_id: str) -> MemoryRecord:
        try:
            return self._records[record_id]
        except KeyError as exc:
            raise KeyError(f"Unknown memory '{record_id}'.") from exc

    def connect(self, memory_id_1: str, memory_id_2: str, *, bidirectional: bool = True) -> None:
        self.get(memory_id_1)
        self.get(memory_id_2)
        self._connections.setdefault(memory_id_1, set()).add(memory_id_2)
        if bidirectional:
            self._connections.setdefault(memory_id_2, set()).add(memory_id_1)

    def traverse(self, start_id: str, *, max_depth: int = 2) -> list[str]:
        self.get(start_id)
        if max_depth < 0:
            raise ValueError("max_depth must be non-negative.")
        visited = {start_id}
        order = [start_id]
        queue = deque([(start_id, 0)])
        while queue:
            current, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for neighbor in sorted(self._connections.get(current, ())):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                order.append(neighbor)
                queue.append((neighbor, depth + 1))
        return order

    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        filters: SearchFilters | None = None,
    ) -> list[SearchResult]:
        filtered_records = [
            record for record in self._records.values() if self._matches_filters(record, filters)
        ]
        if not filtered_records:
            return []

        filtered_lookup = {
            record.record_id: record for record in filtered_records
        }
        scores = self._bm25_scores(query, filtered_records)
        ranked = [
            SearchResult(record=filtered_lookup[record_id], score=score)
            for record_id, score in sorted(
                scores.items(), key=lambda item: (-item[1], item[0])
            )
            if score > 0
        ]
        return ranked[:limit]

    def _matches_filters(self, record: MemoryRecord, filters: SearchFilters | None) -> bool:
        if filters is None:
            return True
        if filters.district and record.district != filters.district:
            return False
        if filters.tags and not filters.tags.issubset(set(record.tags)):
            return False
        if filters.emotional_valence_min is not None:
            if record.emotional_valence is None or record.emotional_valence < filters.emotional_valence_min:
                return False
        if filters.emotional_valence_max is not None:
            if record.emotional_valence is None or record.emotional_valence > filters.emotional_valence_max:
                return False
        if filters.intensity_min is not None:
            if record.intensity is None or record.intensity < filters.intensity_min:
                return False
        if filters.intensity_max is not None:
            if record.intensity is None or record.intensity > filters.intensity_max:
                return False
        return True

    def _bm25_scores(self, query: str, records: list[MemoryRecord]) -> dict[str, float]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return {record.record_id: 0.0 for record in records}

        document_tokens = {
            record.record_id: tokenize(record.search_document) for record in records
        }
        document_lengths = {
            record_id: len(tokens) or 1 for record_id, tokens in document_tokens.items()
        }
        average_length = sum(document_lengths.values()) / len(document_lengths)
        document_frequencies = Counter()
        for tokens in document_tokens.values():
            document_frequencies.update(set(tokens))

        k1 = 1.5
        b = 0.75
        total_docs = len(records)
        scores: dict[str, float] = {}

        for record_id, tokens in document_tokens.items():
            term_frequencies = Counter(tokens)
            score = 0.0
            for token in query_tokens:
                if token not in term_frequencies:
                    continue
                frequency = term_frequencies[token]
                doc_frequency = document_frequencies[token]
                idf = math.log(1 + (total_docs - doc_frequency + 0.5) / (doc_frequency + 0.5))
                numerator = frequency * (k1 + 1)
                denominator = frequency + k1 * (1 - b + b * document_lengths[record_id] / average_length)
                score += idf * numerator / denominator
            scores[record_id] = score
        return scores

    def stats(self) -> MemoryStats:
        per_district = {district: 0 for district in sorted(ALLOWED_DISTRICTS)}
        for record in self._records.values():
            per_district[record.district] += 1
        connection_count = len(
            {
                tuple(sorted((left, right)))
                for left, neighbors in self._connections.items()
                for right in neighbors
                if left != right
            }
        )
        return MemoryStats(
            total_count=len(self._records),
            per_district=per_district,
            connection_count=connection_count,
        )

    def export_snapshot(self, *, campaign_id: str, version: str = "0.1.0") -> SnapshotPackage:
        authored_entries = [
            record for record in self._records.values() if record.memory_type == "authored"
        ]
        connections: list[tuple[str, str, bool]] = []
        seen_bidirectional: set[tuple[str, str]] = set()
        for left, neighbors in self._connections.items():
            for right in neighbors:
                left_record = self._records[left]
                right_record = self._records[right]
                if left_record.memory_type != "authored" or right_record.memory_type != "authored":
                    continue
                if left in self._connections.get(right, set()):
                    pair = tuple(sorted((left, right)))
                    if pair in seen_bidirectional:
                        continue
                    seen_bidirectional.add(pair)
                    connections.append((pair[0], pair[1], True))
                    continue
                connections.append((left, right, False))
        return SnapshotPackage(
            campaign_id=campaign_id,
            project_id=self.project_id,
            version=version,
            entries=sorted(authored_entries, key=lambda record: record.record_id),
            connections=sorted(connections),
        )

    def import_snapshot(self, package: SnapshotPackage) -> None:
        if package.project_id != self.project_id:
            raise ValueError(
                f"Snapshot project_id '{package.project_id}' does not match store project_id '{self.project_id}'."
            )
        if package.dedupe not in {"none", "content_hash", "content_plus_tags"}:
            raise ValueError(f"Unsupported dedupe policy '{package.dedupe}'.")

        imported_id_map: dict[str, str] = {}
        for entry in package.entries:
            duplicate_id = self._find_duplicate(entry, policy=package.dedupe)
            if duplicate_id is not None:
                imported_id_map[entry.record_id] = duplicate_id
                continue

            candidate = entry
            if not package.preserve_ids:
                candidate = self._clone_with_record_id(
                    entry,
                    self._allocate_record_id(entry.record_id),
                )
            self.upsert(candidate)
            imported_id_map[entry.record_id] = candidate.record_id

        if package.merge_connections:
            for left, right, bidirectional in package.connections:
                left_id = imported_id_map[left]
                right_id = imported_id_map[right]
                if left_id == right_id:
                    continue
                self.connect(left_id, right_id, bidirectional=bidirectional)

    def _find_duplicate(self, record: MemoryRecord, *, policy: str) -> str | None:
        if policy == "none":
            return None

        normalized_tags = tuple(sorted(record.tags))
        for existing in self._records.values():
            if existing.project_id != record.project_id:
                continue
            if existing.memory_type != record.memory_type:
                continue
            if existing.district != record.district:
                continue
            if policy == "content_hash" and existing.content == record.content:
                return existing.record_id
            if (
                policy == "content_plus_tags"
                and existing.content == record.content
                and tuple(sorted(existing.tags)) == normalized_tags
            ):
                return existing.record_id
        return None

    def _allocate_record_id(self, base_id: str) -> str:
        if base_id not in self._records:
            return base_id
        suffix = 1
        while True:
            candidate = f"{base_id}_copy_{suffix}"
            if candidate not in self._records:
                return candidate
            suffix += 1

    def _clone_with_record_id(self, record: MemoryRecord, record_id: str) -> MemoryRecord:
        return MemoryRecord(
            record_id=record_id,
            content=record.content,
            district=record.district,
            tags=list(record.tags),
            project_id=record.project_id,
            memory_type=record.memory_type,
            emotional_valence=record.emotional_valence,
            intensity=record.intensity,
            epistemic_status=record.epistemic_status,
            source_ids=record.source_ids,
        )

    def distill_emotional_memory(
        self,
        source_id: str,
        *,
        distilled_id: str,
        content: str,
        tags: list[str],
    ) -> MemoryRecord:
        source = self.get(source_id)
        if source.district != "emotional_processing":
            raise ValueError("Only emotional_processing memories can be distilled.")
        distilled = MemoryRecord(
            record_id=distilled_id,
            content=content,
            district="logical_analysis",
            tags=tags,
            project_id=self.project_id,
            memory_type="runtime",
            intensity=max((source.intensity or 0.0) * 0.5, 0.0),
            emotional_valence=0.0,
            epistemic_status="validated",
            source_ids=(source_id,),
        )
        self.upsert(distilled)
        self.connect(source_id, distilled.record_id)
        return distilled

    def sync_to_gateway(
        self,
        gateway: NeurodivergentMemoryGateway,
        *,
        record_ids: list[str] | None = None,
    ) -> dict[str, str]:
        synced: dict[str, str] = {}
        target_ids = sorted(self._records) if record_ids is None else list(record_ids)
        for record_id in target_ids:
            record = self.get(record_id)
            remote_id = gateway.store_memory(record.to_memory_payload())
            synced[record_id] = remote_id

        seen_edges: set[tuple[str, str]] = set()
        for left in target_ids:
            for right in self._connections.get(left, set()):
                if right not in target_ids:
                    continue
                reverse_exists = left in self._connections.get(right, set())
                if reverse_exists:
                    edge = tuple(sorted((left, right)))
                    if edge in seen_edges:
                        continue
                    seen_edges.add(edge)
                    gateway.connect_memories(synced[edge[0]], synced[edge[1]], bidirectional=True)
                    continue
                edge = (left, right)
                if edge in seen_edges:
                    continue
                seen_edges.add(edge)
                gateway.connect_memories(synced[left], synced[right], bidirectional=False)
        return synced

    def import_authored_snapshot_to_gateway(
        self,
        gateway: NeurodivergentMemoryGateway,
        *,
        campaign_id: str,
        version: str = "0.1.0",
    ) -> dict[str, Any]:
        package = self.export_snapshot(campaign_id=campaign_id, version=version)
        return gateway.import_memories(package.to_dict())