#!/usr/bin/env python3
"""Build a pure-CAPTURE, content-deduplicated opaque-length delta.

The TSV intentionally emits only numeric identifiers observed in captures,
opaque-region lengths/offsets, counts, and SHA-256 metadata.  It never emits
capture payload values, raw bytes, hexdumps, IMAGE-resolved names, or an
IMAGE-derived interpretation of bytes inside the opaque region.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType


# Keep this report lane limited to its three explicitly owned files even when
# the extractor is imported for audit.
sys.dont_write_bytecode = True


SOURCE = "CAPTURE"
REPORT_VERSION = "PF_CAPTURE_BRANCH_SHAPES_20260830_V3_PURE_CAPTURE_LENGTH_DELTA"
RUNTIME_RESPONSE_NAME = "GSCN_RunTimeProtocolRes"
RUNTIME_RESPONSE_ID = 0x6E9D
RUNTIME_REQUEST_NAME = "GSCN_RunTimeProtocolReq"
RUNTIME_REQUEST_ID = 0x6E6F

# These thirteen names are the frozen IMAGE-side selection set.  Selection and
# mapping are discussed only in the Markdown report; no IMAGE status is copied
# into the CAPTURE-only TSV.
TARGET_MESSAGES = (
    "CLearnSkillResultVital",
    "CTracePathVital",
    "CreateActorVital",
    "GSCN_LoginProtocol",
    "GetWorldInfoVital",
    "ItemOperateVitalRes",
    "NPCConversation",
    "SelectActorVital",
    "TeleportVital",
    "TradeCmdVital",
    "TradeZoomVital",
    "UpdateAttrVital",
    "UserSetting_UpdateServerSettingVital",
)
EXPECTED_STRICT_MESSAGES = (
    "CLearnSkillResultVital",
    "CTracePathVital",
    "ItemOperateVitalRes",
    "NPCConversation",
    "SelectActorVital",
    "TradeZoomVital",
    "UpdateAttrVital",
)
EXPECTED_NON_STRICT_MESSAGES = (
    "CreateActorVital",
    "GSCN_LoginProtocol",
    "GetWorldInfoVital",
    "TeleportVital",
    "TradeCmdVital",
    "UserSetting_UpdateServerSettingVital",
)

EXPECTED_HASHES = {
    "PF_INPUT_INVENTORY.tsv": "729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1",
    "PF_PROTOCOL_REGISTRY.tsv": "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d",
    "PF_SERIALIZER_FIELDS.tsv": "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123",
    "PF_TAG_CENSUS.tsv": "63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a",
    "PF_DUMP_REQUEST.md": "5fce70adf071120f8c7cd9739ac52b835d5e4ee9c0f70995dc295fca8199201d",
    "PF_FIELD_VALIDATION.tsv": "080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3",
    "pf_validate_capture_fields.py": "0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8",
}

EXPECTED_CAPTURE_INVENTORY_FILES = 1_772
EXPECTED_CAPTURE_INVENTORY_BYTES = 595_134_426
EXPECTED_BASELINE_TEXT_FILES = 918
EXPECTED_BASELINE_TEXT_BYTES = 98_590_688
EXPECTED_BASELINE_TEXT_MANIFEST = (
    "95f574e49b20957a025fd9d98dcfd888a51a76e2393ea169f99d147e3d69d447"
)
EXPECTED_DELTA_FILES = 382
EXPECTED_DELTA_BYTES = 76_247_171
EXPECTED_DELTA_MANIFEST = (
    "e738fd72565a2dc4747dc31168091c98eabaf63acd87b522b3fd2b11a328f516"
)
EXPECTED_DELTA_TEXT_FILES = 353
EXPECTED_DELTA_TEXT_BYTES = 68_690_435
EXPECTED_DELTA_TEXT_MANIFEST = (
    "7a2aa6b8b073e6b87d5949e53d8ff1aea790bc9da398e55e1beee9422ae4904c"
)
EXPECTED_DELTA_JPG_FILES = 29
EXPECTED_DELTA_PC_BLOCKS = 5_211
EXPECTED_DELTA_DECOMPRESSED_BLOCKS = 20_183
EXPECTED_DELTA_BLOCKS = 25_394

RAW_BYTE_RUN_RE = re.compile(
    r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"
)
FORBIDDEN_TSV_HEADER_TERMS = (
    "a2",
    "closure",
    "declared",
    "envelope",
    "field",
    "image",
    "message",
    "name",
    "priority",
    "sequence",
    "serializer",
    "static",
    "tag",
    "width",
)


class ExtractionError(RuntimeError):
    pass


@dataclass(frozen=True)
class CaptureInput:
    relative_path: str
    path: Path
    size: int
    sha256: str


@dataclass(frozen=True)
class BranchObservation:
    outer_id: int
    nested_id: int
    capture_kind: str
    direction: str
    region_length: int
    relative_path: str
    capture_file_sha256: str
    block_ordinal: int
    block_sha256: str
    region_sha256: str
    content_key: str
    dedup_class: str
    region_offset: int
    tail_offset: int

    @property
    def shape_key(self) -> tuple[int, int, str, str, int]:
        return (
            self.outer_id,
            self.nested_id,
            self.capture_kind,
            self.direction,
            self.region_length,
        )


@dataclass
class ShapeAggregate:
    outer_id: int
    nested_id: int
    capture_kind: str
    direction: str
    region_length: int
    baseline_instances: int = 0
    delta_observed_instances: int = 0
    claim_unique: list[BranchObservation] = field(default_factory=list)
    duplicate_rejected_baseline: int = 0
    duplicate_rejected_delta: int = 0


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().lower()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def protocol_id(name: str) -> int:
    return sum(
        (index + 1) * ord(character)
        for index, character in enumerate(name)
    ) & 0xFFFF


def enumerate_capture_paths(root: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for directory in sorted(root.rglob("capture_*")):
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            key = relative.casefold()
            prior = paths.get(key)
            if prior is not None and prior != path:
                raise ExtractionError(f"case-fold capture-path collision: {relative}")
            paths[key] = path
    return paths


def manifest_sha256(inputs: list[CaptureInput]) -> str:
    digest = hashlib.sha256()
    for item in sorted(
        inputs,
        key=lambda value: (value.relative_path.casefold(), value.relative_path),
    ):
        digest.update(item.relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(item.size).encode("ascii"))
        digest.update(b"\0")
        digest.update(item.sha256.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest().lower()


def snapshot_inputs(inputs: list[CaptureInput]) -> tuple[tuple[str, int, str], ...]:
    snapshot: list[tuple[str, int, str]] = []
    for item in sorted(inputs, key=lambda value: value.relative_path):
        stat = item.path.stat()
        actual_hash = sha256_file(item.path)
        if stat.st_size != item.size or actual_hash != item.sha256:
            raise ExtractionError(f"capture input changed: {item.relative_path}")
        snapshot.append((item.relative_path, stat.st_size, actual_hash))
    return tuple(snapshot)


def load_inputs(
    root: Path,
    inventory_path: Path,
) -> tuple[list[CaptureInput], list[CaptureInput], list[CaptureInput]]:
    rows = read_tsv(inventory_path)
    capture_rows = [row for row in rows if row.get("source") == SOURCE]
    if len(capture_rows) != EXPECTED_CAPTURE_INVENTORY_FILES:
        raise ExtractionError("CAPTURE input-inventory census changed")
    if sum(int(row["size"]) for row in capture_rows) != EXPECTED_CAPTURE_INVENTORY_BYTES:
        raise ExtractionError("CAPTURE input-inventory byte census changed")

    fresh = enumerate_capture_paths(root)
    baseline_keys = {row["relative_path"].casefold() for row in capture_rows}
    if len(baseline_keys) != len(capture_rows):
        raise ExtractionError("duplicate CAPTURE paths in input inventory")
    missing = sorted(baseline_keys - set(fresh))
    if missing:
        raise ExtractionError(f"baseline capture path missing: {missing[0]}")

    baseline_text: list[CaptureInput] = []
    for row in capture_rows:
        relative = row["relative_path"]
        if Path(relative).suffix.casefold() != ".txt":
            continue
        baseline_text.append(
            CaptureInput(
                relative_path=relative,
                path=fresh[relative.casefold()],
                size=int(row["size"]),
                sha256=row["sha256"].lower(),
            )
        )
    if len(baseline_text) != EXPECTED_BASELINE_TEXT_FILES:
        raise ExtractionError("baseline CAPTURE text-file census changed")
    if sum(item.size for item in baseline_text) != EXPECTED_BASELINE_TEXT_BYTES:
        raise ExtractionError("baseline CAPTURE text byte census changed")
    if manifest_sha256(baseline_text) != EXPECTED_BASELINE_TEXT_MANIFEST:
        raise ExtractionError("baseline CAPTURE text manifest changed")

    delta: list[CaptureInput] = []
    for key in sorted(set(fresh) - baseline_keys):
        path = fresh[key]
        relative = path.relative_to(root).as_posix()
        size = path.stat().st_size
        delta.append(
            CaptureInput(
                relative_path=relative,
                path=path,
                size=size,
                sha256=sha256_file(path),
            )
        )
    if len(delta) != EXPECTED_DELTA_FILES:
        raise ExtractionError(f"delta file census changed: {len(delta)}")
    if sum(item.size for item in delta) != EXPECTED_DELTA_BYTES:
        raise ExtractionError("delta byte census changed")
    if manifest_sha256(delta) != EXPECTED_DELTA_MANIFEST:
        raise ExtractionError("delta manifest changed")
    delta_text = [
        item for item in delta if item.path.suffix.casefold() == ".txt"
    ]
    delta_jpg = [
        item for item in delta if item.path.suffix.casefold() == ".jpg"
    ]
    if len(delta_text) != EXPECTED_DELTA_TEXT_FILES:
        raise ExtractionError("delta text-file census changed")
    if sum(item.size for item in delta_text) != EXPECTED_DELTA_TEXT_BYTES:
        raise ExtractionError("delta text byte census changed")
    if manifest_sha256(delta_text) != EXPECTED_DELTA_TEXT_MANIFEST:
        raise ExtractionError("delta text manifest changed")
    if len(delta_jpg) != EXPECTED_DELTA_JPG_FILES:
        raise ExtractionError("delta JPG-file census changed")
    if len(delta_text) + len(delta_jpg) != len(delta):
        raise ExtractionError("unexpected file type in capture delta")
    return baseline_text, delta, delta_text


def load_validator(path: Path) -> ModuleType:
    module_name = "pf_validate_capture_fields_pinned_20260830"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ExtractionError("could not load pinned GT-047/A5 parser")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def content_key(kind: str, data: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(b"PF_CAPTURE_BLOCK_V1\0")
    digest.update(kind.encode("ascii"))
    digest.update(b"\0")
    digest.update(data)
    return digest.hexdigest().lower()


def strict_branch(
    kind: str,
    data: bytes,
    relative_path: str,
    capture_file_sha256: str,
    block_ordinal: int,
    block_content_key: str,
    dedup_class: str,
    target_ids: set[int],
) -> BranchObservation | None:
    # Exact isolation requires the response envelope, one nested vital, a complete
    # known wrapper, and the final response-only runtime zero tail.  The pinned A5
    # parser does not prove the same tail boundary for request envelopes, so a Req
    # observation must remain unresolved rather than laundering its final 0B00 as
    # response framing.
    if len(data) < 22:
        return None
    if data[0] != 0x12:
        return None
    outer_id = int.from_bytes(data[1:3], "little")
    if outer_id != RUNTIME_RESPONSE_ID:
        return None
    if data[3] != 0x14 or data[8] != 0x08 or data[10] != 0x0B:
        return None
    if not data[11] & 0x02 or data[12] != 0x12:
        return None
    if int.from_bytes(data[13:15], "little") != 1:
        return None
    if data[15] != 0x12 or data[18] != 0x0B:
        return None
    if data[-2:] != bytes((0x0B, 0x00)):
        return None
    nested_id = int.from_bytes(data[16:18], "little")
    if nested_id not in target_ids:
        return None
    region_offset = 20
    tail_offset = len(data) - 2
    region = data[region_offset:tail_offset]
    direction = "R" if kind == "PC" else "W"
    return BranchObservation(
        outer_id=outer_id,
        nested_id=nested_id,
        capture_kind=kind,
        direction=direction,
        region_length=len(region),
        relative_path=relative_path,
        capture_file_sha256=capture_file_sha256,
        block_ordinal=block_ordinal,
        block_sha256=sha256_bytes(data),
        region_sha256=sha256_bytes(region),
        content_key=block_content_key,
        dedup_class=dedup_class,
        region_offset=region_offset,
        tail_offset=tail_offset,
    )


def shape_dedup_key(shape_key: tuple[int, int, str, str, int]) -> str:
    outer_id, nested_id, capture_kind, direction, region_length = shape_key
    digest = hashlib.sha256()
    digest.update(REPORT_VERSION.encode("ascii"))
    digest.update(b"\0")
    digest.update(f"0x{outer_id:04X}".encode("ascii"))
    digest.update(b"\0")
    digest.update(f"0x{nested_id:04X}".encode("ascii"))
    digest.update(b"\0")
    digest.update(capture_kind.encode("ascii"))
    digest.update(b"\0")
    digest.update(direction.encode("ascii"))
    digest.update(b"\0")
    digest.update(str(region_length).encode("ascii"))
    return digest.hexdigest().lower()


def evidence_manifest(observations: list[BranchObservation]) -> str:
    digest = hashlib.sha256()
    for item in sorted(
        observations,
        key=lambda value: (value.relative_path, value.block_ordinal),
    ):
        fields = (
            item.relative_path,
            item.capture_file_sha256,
            str(item.block_ordinal),
            item.block_sha256,
            item.region_sha256,
        )
        digest.update("\0".join(fields).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest().lower()


def tsv_text(headers: list[str], rows: list[list[str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return stream.getvalue()


def build_reports(
    baseline_text: list[CaptureInput],
    delta_all: list[CaptureInput],
    delta_text: list[CaptureInput],
    validator: ModuleType,
    id_to_name: dict[int, str],
    schemas: dict[tuple[str, str], list[object]],
    static_open: set[str],
    target_ids: set[int],
) -> tuple[str, str, dict[str, int | str | tuple[str, ...]]]:
    baseline_content_keys: set[str] = set()
    baseline_shape_counts: Counter[tuple[int, int, str, str, int]] = Counter()
    baseline_block_counts: Counter[str] = Counter()
    baseline_errors: Counter[str] = Counter()

    for item in baseline_text:
        text = item.path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = validator.extract_pc_blocks(text)
        baseline_errors.update(errors)
        for ordinal, (kind, data) in enumerate(blocks, 1):
            key = content_key(kind, data)
            baseline_content_keys.add(key)
            baseline_block_counts[kind] += 1
            observation = strict_branch(
                kind,
                data,
                item.relative_path,
                item.sha256,
                ordinal,
                key,
                "BASELINE",
                target_ids,
            )
            if observation is not None:
                baseline_shape_counts[observation.shape_key] += 1
    if baseline_errors:
        raise ExtractionError(f"baseline block extraction errors: {dict(baseline_errors)}")

    delta_seen_new_keys: set[str] = set()
    delta_observations: list[BranchObservation] = []
    delta_errors: Counter[str] = Counter()
    delta_block_counts: Counter[str] = Counter()
    duplicate_rejected_baseline_all = 0
    duplicate_rejected_delta_all = 0
    claim_unique_all = 0

    # The pinned A5/GT-047 path is used only for the cross-layer selection audit
    # summarized in Markdown.  Its results never populate a TSV column.
    audit_aggregates = defaultdict(validator.MessageAggregate)
    audit_counts = validator.RunCounts()

    for item in delta_text:
        text = item.path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = validator.extract_pc_blocks(text)
        delta_errors.update(errors)
        for ordinal, (kind, data) in enumerate(blocks, 1):
            delta_block_counts[kind] += 1
            direction = "R" if kind == "PC" else "W"
            frame_key = f"{item.relative_path}:{ordinal}"
            validator.parse_capture_frame(
                data,
                direction,
                frame_key,
                item.relative_path,
                id_to_name,
                schemas,
                static_open,
                audit_aggregates,
                audit_counts,
            )
            key = content_key(kind, data)
            if key in baseline_content_keys:
                dedup_class = "DUPLICATE_BASELINE"
                duplicate_rejected_baseline_all += 1
            elif key in delta_seen_new_keys:
                dedup_class = "DUPLICATE_DELTA"
                duplicate_rejected_delta_all += 1
            else:
                dedup_class = "CLAIM_UNIQUE"
                delta_seen_new_keys.add(key)
                claim_unique_all += 1
            observation = strict_branch(
                kind,
                data,
                item.relative_path,
                item.sha256,
                ordinal,
                key,
                dedup_class,
                target_ids,
            )
            if observation is not None:
                delta_observations.append(observation)

    if delta_errors:
        raise ExtractionError(f"delta block extraction errors: {dict(delta_errors)}")
    if delta_block_counts != Counter(
        {"PC": EXPECTED_DELTA_PC_BLOCKS, "DECOMPRESSED": EXPECTED_DELTA_DECOMPRESSED_BLOCKS}
    ):
        raise ExtractionError(f"delta block census changed: {dict(delta_block_counts)}")
    if sum(delta_block_counts.values()) != EXPECTED_DELTA_BLOCKS:
        raise ExtractionError("delta block total changed")
    if audit_counts.unknown_message_id_instances:
        raise ExtractionError("delta selection audit found an unknown message ID")
    if audit_counts.block_errors:
        raise ExtractionError(
            f"delta selection audit found envelope errors: {dict(audit_counts.block_errors)}"
        )

    observed_targets = tuple(
        sorted(
            name
            for name in TARGET_MESSAGES
            if sum(
                audit_aggregates[(name, direction)].observed_instances
                for direction in ("W", "R")
            )
            > 0
        )
    )
    if observed_targets != tuple(sorted(TARGET_MESSAGES)):
        raise ExtractionError(f"delta target observation set changed: {observed_targets}")
    strict_ids = tuple(sorted({item.nested_id for item in delta_observations}))
    expected_strict_ids = tuple(sorted(protocol_id(name) for name in EXPECTED_STRICT_MESSAGES))
    if strict_ids != expected_strict_ids:
        raise ExtractionError(f"strict branch numeric-ID set changed: {strict_ids}")
    strict_names = tuple(sorted(id_to_name[item] for item in strict_ids))
    non_strict = tuple(sorted(set(observed_targets) - set(strict_names)))
    if non_strict != tuple(sorted(EXPECTED_NON_STRICT_MESSAGES)):
        raise ExtractionError(f"non-strict target set changed: {non_strict}")

    aggregates: dict[tuple[int, int, str, str, int], ShapeAggregate] = {}
    for observation in delta_observations:
        aggregate = aggregates.get(observation.shape_key)
        if aggregate is None:
            aggregate = ShapeAggregate(
                outer_id=observation.outer_id,
                nested_id=observation.nested_id,
                capture_kind=observation.capture_kind,
                direction=observation.direction,
                region_length=observation.region_length,
                baseline_instances=baseline_shape_counts[observation.shape_key],
            )
            aggregates[observation.shape_key] = aggregate
        aggregate.delta_observed_instances += 1
        if observation.dedup_class == "CLAIM_UNIQUE":
            aggregate.claim_unique.append(observation)
        elif observation.dedup_class == "DUPLICATE_BASELINE":
            aggregate.duplicate_rejected_baseline += 1
        elif observation.dedup_class == "DUPLICATE_DELTA":
            aggregate.duplicate_rejected_delta += 1
        else:
            raise ExtractionError(f"unknown dedup class {observation.dedup_class}")

    headers = [
        "outer_protocol_id",
        "nested_protocol_id",
        "capture_kind",
        "direction(W/R)",
        "opaque_region_length",
        "delta_status",
        "baseline_capture_instances",
        "delta_observed_instances",
        "claim_unique_instances",
        "duplicate_rejected_baseline",
        "duplicate_rejected_delta",
        "capture_file_count",
        "first_opaque_region_offset_in_block",
        "first_tail_offset_in_block",
        "first_evidence_relative_path",
        "first_capture_file_sha256",
        "first_block_ordinal",
        "first_block_sha256",
        "first_opaque_region_sha256",
        "evidence_manifest_sha256",
        "dedup_key",
        "source",
    ]
    rows: list[list[str]] = []
    published = [
        value
        for value in aggregates.values()
        if value.baseline_instances == 0 and value.claim_unique
    ]
    published.sort(
        key=lambda value: (
            value.outer_id,
            value.nested_id,
            value.capture_kind,
            value.direction,
            value.region_length,
        )
    )
    for aggregate in published:
        evidence = sorted(
            aggregate.claim_unique,
            key=lambda value: (value.relative_path, value.block_ordinal),
        )
        first = evidence[0]
        rows.append(
            [
                f"0x{aggregate.outer_id:04X}",
                f"0x{aggregate.nested_id:04X}",
                aggregate.capture_kind,
                aggregate.direction,
                str(aggregate.region_length),
                "ADDED_NEW_LENGTH",
                str(aggregate.baseline_instances),
                str(aggregate.delta_observed_instances),
                str(len(evidence)),
                str(aggregate.duplicate_rejected_baseline),
                str(aggregate.duplicate_rejected_delta),
                str(len({item.relative_path for item in evidence})),
                f"0x{first.region_offset:08X}",
                f"0x{first.tail_offset:08X}",
                first.relative_path,
                first.capture_file_sha256,
                str(first.block_ordinal),
                first.block_sha256,
                first.region_sha256,
                evidence_manifest(evidence),
                shape_dedup_key(first.shape_key),
                SOURCE,
            ]
        )
    output_tsv = tsv_text(headers, rows)

    existing_reobserved = [
        value for value in aggregates.values() if value.baseline_instances > 0
    ]
    strict_delta_by_numeric_key: dict[
        tuple[int, int, str, str], list[BranchObservation]
    ] = defaultdict(list)
    for observation in delta_observations:
        strict_delta_by_numeric_key[
            (
                observation.outer_id,
                observation.nested_id,
                observation.capture_kind,
                observation.direction,
            )
        ].append(observation)
    capture_table_lines = [
        "| outer ID | nested ID | capture kind | direction | strict instances | claim-unique instances | new lengths published | existing lengths reobserved |",
        "|---:|---:|---|---:|---:|---:|---:|---:|",
    ]
    for key in sorted(strict_delta_by_numeric_key):
        outer_id, nested_id, capture_kind, direction = key
        observations = strict_delta_by_numeric_key[key]
        new_lengths = [
            value
            for value in published
            if value.outer_id == outer_id
            and value.nested_id == nested_id
            and value.capture_kind == capture_kind
            and value.direction == direction
        ]
        old_lengths = [
            value
            for value in existing_reobserved
            if value.outer_id == outer_id
            and value.nested_id == nested_id
            and value.capture_kind == capture_kind
            and value.direction == direction
        ]
        capture_table_lines.append(
            "| `0x%04X` | `0x%04X` | `%s` | %s | %d | %d | %d | %d |"
            % (
                outer_id,
                nested_id,
                capture_kind,
                direction,
                len(observations),
                sum(item.dedup_class == "CLAIM_UNIQUE" for item in observations),
                len(new_lengths),
                len(old_lengths),
            )
        )

    image_mapping_lines = [
        "| IMAGE-resolved name | IMAGE protocol ID |",
        "|---|---:|",
    ]
    image_mapping_lines.extend(
        f"| `{name}` | `0x{protocol_id(name):04X}` |" for name in TARGET_MESSAGES
    )
    strict_id_list = ", ".join(f"`0x{item:04X}`" for item in strict_ids)
    non_strict_list = ", ".join(f"`{name}`" for name in non_strict)
    pinned_lines = "\n".join(
        f"- `{name}`: `{digest}`" for name, digest in EXPECTED_HASHES.items()
    )
    output_md = f"""# PF CAPTURE opaque-length delta — 2026-08-30

[MEASURED] Every path, count, offset, numeric ID, length, and hash below is re-derived from the pinned CAPTURE corpus by this generator.

## Result

This additive report publishes **{len(rows)} pure-CAPTURE rows**. Every row is a numeric response-envelope/nested-ID/capture-kind/direction/opaque-region-length combination absent from the frozen CAPTURE baseline. **No baseline-existing length is repeated in the TSV.**

The rows are observed, exactly bounded opaque regions. They are not byte interpretations, full IMAGE serializer closures, A2 changes, or assertions about unobserved branches.

## Evidence-layer separation

### IMAGE selection context — Markdown context only

The following IMAGE mapping defines the bounded candidate set. These names are context only and are deliberately absent from every TSV row.

{chr(10).join(image_mapping_lines)}

The pinned IMAGE/A2 selection audit observed all thirteen mapped candidates somewhere in the new capture text. Exact response-only numeric isolation succeeded for IDs {strict_id_list}. The IMAGE-resolved candidates not strictly isolated were {non_strict_list}. This paragraph does not convert a CAPTURE observation into an IMAGE fact.

### CAPTURE-only observations and duplicate census

- New capture delta: {len(delta_all)} files / {sum(item.size for item in delta_all)} bytes; {len(delta_text)} text files were parsed.
- Extracted blocks: {sum(delta_block_counts.values())} total (`PC`={delta_block_counts['PC']}, `DECOMPRESSED`={delta_block_counts['DECOMPRESSED']}); extraction errors=0.
- Full-block content dedup across the complete delta: claim-unique={claim_unique_all}; duplicate rejected against baseline={duplicate_rejected_baseline_all}; duplicate rejected within delta={duplicate_rejected_delta_all}.
- Strict selected response-branch instances={len(delta_observations)}; strict claim-unique instances={sum(item.dedup_class == 'CLAIM_UNIQUE' for item in delta_observations)}.
- New opaque lengths published={len(rows)}; published claim-unique instances={sum(len(value.claim_unique) for value in published)}.
- Baseline-existing opaque-length keys reobserved={len(existing_reobserved)}; their delta instances={sum(value.delta_observed_instances for value in existing_reobserved)}; their claim-unique instances={sum(len(value.claim_unique) for value in existing_reobserved)}. These reobservations are census-only and do not appear in the TSV.

{chr(10).join(capture_table_lines)}

`capture_file_count` counts files contributing claim-unique instances to a newly published length. `dedup_key` hashes only the CAPTURE-observable numeric key. Block, opaque-region, file, and evidence-manifest SHA-256 columns support local audit without exporting proprietary values.

## Exact isolation rule

A row is eligible only when a captured block has numeric outer ID `0x{RUNTIME_RESPONSE_ID:04X}`, declares exactly one nested numeric ID from the bounded selection set, exposes the fixed wrapper boundary, and ends at the response-only known runtime-zero tail. The bytes between wrapper and tail remain opaque; only their length, offsets, and SHA-256 are exported. Numeric request outer ID `0x{RUNTIME_REQUEST_ID:04X}` is excluded fail-closed because its tail boundary remains unresolved.

## Selection-audit limitation and nonclaims

The pinned `pf_validate_capture_fields.py` parser is reused for block extraction and the separate IMAGE selection audit. Its known GT-047 `field_offset` mutation limitation does not affect the pure-CAPTURE row key because no field, tag, width, sequence, name, or serializer interpretation is published. This delta does not repair A2 to fit observed traffic and does not close an IMAGE serializer path.

No dump/capture payload value, raw byte, or hexdump is emitted. Output is limited to numeric IDs, opaque lengths/offsets, counts, paths, and SHA-256 metadata.

## Frozen inputs and integrity

- Baseline CAPTURE text: {len(baseline_text)} files / {sum(item.size for item in baseline_text)} bytes; manifest `{EXPECTED_BASELINE_TEXT_MANIFEST}`.
- New CAPTURE delta: {len(delta_all)} files / {sum(item.size for item in delta_all)} bytes; manifest `{EXPECTED_DELTA_MANIFEST}`.
- New CAPTURE text: {len(delta_text)} files / {sum(item.size for item in delta_text)} bytes; manifest `{EXPECTED_DELTA_TEXT_MANIFEST}`.
- Input files were hashed before parsing and hashed again before publication; both snapshots matched.

Pinned supporting inputs:

{pinned_lines}
"""

    metrics: dict[str, int | str | tuple[str, ...]] = {
        "rows": len(rows),
        "added_shapes": len(rows),
        "existing_shapes": len(existing_reobserved),
        "strict_instances": len(delta_observations),
        "claim_unique_all": claim_unique_all,
        "duplicate_baseline_all": duplicate_rejected_baseline_all,
        "duplicate_delta_all": duplicate_rejected_delta_all,
        "strict_ids": tuple(f"0x{item:04X}" for item in strict_ids),
        "non_strict_messages": non_strict,
    }
    return output_tsv, output_md, metrics


def validate_tsv_headers(headers: list[str]) -> None:
    header_tokens = {
        token
        for header in headers
        for token in re.findall(r"[a-z0-9]+", header.casefold())
    }
    if any(term in header_tokens for term in FORBIDDEN_TSV_HEADER_TERMS):
        raise ExtractionError("TSV schema mixes IMAGE/static-selection fields")


def validate_output(output_tsv: str, output_md: str) -> None:
    reader = csv.DictReader(io.StringIO(output_tsv), delimiter="\t")
    parsed = list(reader)
    if not parsed:
        raise ExtractionError("opaque-length TSV has no rows")
    headers = list(reader.fieldnames or ())
    validate_tsv_headers(headers)
    if any(row.get("source") != SOURCE for row in parsed):
        raise ExtractionError("TSV row source is not CAPTURE")
    if any(row.get("outer_protocol_id") != f"0x{RUNTIME_RESPONSE_ID:04X}" for row in parsed):
        raise ExtractionError("TSV row is not response-ID isolated")
    if any(row.get("delta_status") != "ADDED_NEW_LENGTH" for row in parsed):
        raise ExtractionError("TSV contains a non-additive length status")
    if any(int(row["baseline_capture_instances"]) != 0 for row in parsed):
        raise ExtractionError("TSV repeats a baseline-existing length")
    if len({row["dedup_key"] for row in parsed}) != len(parsed):
        raise ExtractionError("duplicate opaque-length dedup key")
    numeric_keys = {
        (
            row["outer_protocol_id"],
            row["nested_protocol_id"],
            row["capture_kind"],
            row["direction(W/R)"],
            row["opaque_region_length"],
        )
        for row in parsed
    }
    if len(numeric_keys) != len(parsed):
        raise ExtractionError("duplicate CAPTURE-observable numeric key")
    allowed_nested_ids = {f"0x{protocol_id(name):04X}" for name in TARGET_MESSAGES}
    if any(row["nested_protocol_id"] not in allowed_nested_ids for row in parsed):
        raise ExtractionError("TSV contains an out-of-scope numeric nested ID")
    if any(
        (row["capture_kind"], row["direction(W/R)"])
        not in {("PC", "R"), ("DECOMPRESSED", "W")}
        for row in parsed
    ):
        raise ExtractionError("capture-kind/direction pair is inconsistent")
    if any(int(row["claim_unique_instances"]) <= 0 for row in parsed):
        raise ExtractionError("TSV contains a row without claim-unique evidence")
    for row in parsed:
        if int(row["delta_observed_instances"]) != (
            int(row["claim_unique_instances"])
            + int(row["duplicate_rejected_baseline"])
            + int(row["duplicate_rejected_delta"])
        ):
            raise ExtractionError("per-shape dedup accounting does not balance")
    if RAW_BYTE_RUN_RE.search(output_tsv) or RAW_BYTE_RUN_RE.search(output_md):
        raise ExtractionError("raw-byte export guard fired")


def validate_regressions() -> None:
    try:
        validate_tsv_headers(["outer_protocol_id", "message_name", "source"])
    except ExtractionError:
        pass
    else:
        raise ExtractionError("mixed-layer TSV-header negative regression failed")

    nested_name = "CLearnSkillResultVital"
    nested_id = protocol_id(nested_name)
    target_ids = {nested_id}

    def synthetic_branch(outer_id: int) -> bytes:
        data = bytearray(22)
        data[0] = 0x12
        data[1:3] = outer_id.to_bytes(2, "little")
        data[3] = 0x14
        data[8] = 0x08
        data[10] = 0x0B
        data[11] = 0x02
        data[12] = 0x12
        data[13:15] = (1).to_bytes(2, "little")
        data[15] = 0x12
        data[16:18] = nested_id.to_bytes(2, "little")
        data[18] = 0x0B
        data[20:22] = bytes((0x0B, 0x00))
        return bytes(data)

    response = strict_branch(
        "PC", synthetic_branch(RUNTIME_RESPONSE_ID), "synthetic", "0" * 64,
        1, "response", "CLAIM_UNIQUE", target_ids,
    )
    if response is None or response.outer_id != RUNTIME_RESPONSE_ID:
        raise ExtractionError("response-only strict isolation positive regression failed")
    request = strict_branch(
        "PC", synthetic_branch(RUNTIME_REQUEST_ID), "synthetic",
        "0" * 64, 1, "request", "CLAIM_UNIQUE", target_ids,
    )
    if request is not None:
        raise ExtractionError("request-tail laundering negative regression failed")


def atomic_publish(outputs: dict[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, text in outputs.items():
            fd, raw_temp = tempfile.mkstemp(
                prefix=f".{destination.name}.",
                suffix=".tmp",
                dir=destination.parent,
            )
            temp = Path(raw_temp)
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            staged.append((temp, destination))
        for temp, destination in staged:
            os.replace(temp, destination)
    finally:
        for temp, _destination in staged:
            if temp.exists():
                temp.unlink()


def verify_pinned_files(external: Path) -> dict[Path, str]:
    actual: dict[Path, str] = {}
    for name, expected in EXPECTED_HASHES.items():
        path = external / name
        digest = sha256_file(path)
        if digest != expected:
            raise ExtractionError(f"pinned input hash changed: {name}")
        actual[path] = digest
    return actual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game-client",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "GameClient",
    )
    parser.add_argument(
        "--external",
        type=Path,
        default=Path(__file__).resolve().parent,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="derive again and require byte-identical existing outputs",
    )
    args = parser.parse_args()
    root = args.game_client.resolve()
    external = args.external.resolve()

    pinned_before = verify_pinned_files(external)
    inventory_path = external / "PF_INPUT_INVENTORY.tsv"
    baseline_text, delta_all, delta_text = load_inputs(root, inventory_path)
    baseline_before = snapshot_inputs(baseline_text)
    delta_before = snapshot_inputs(delta_all)

    registry_rows = read_tsv(external / "PF_PROTOCOL_REGISTRY.tsv")
    field_rows = read_tsv(external / "PF_SERIALIZER_FIELDS.tsv")
    tag_rows = read_tsv(external / "PF_TAG_CENSUS.tsv")
    validator = load_validator(external / "pf_validate_capture_fields.py")
    id_to_name, schemas, static_open = validator.build_schemas(
        registry_rows,
        field_rows,
        tag_rows,
    )
    if id_to_name.get(RUNTIME_RESPONSE_ID) != RUNTIME_RESPONSE_NAME:
        raise ExtractionError("runtime response ID mapping changed")
    if any(name not in static_open for name in TARGET_MESSAGES):
        raise ExtractionError("IMAGE-side target selection no longer matches A2")
    if any(id_to_name.get(protocol_id(name)) != name for name in TARGET_MESSAGES):
        raise ExtractionError("target protocol ID mapping changed")
    target_ids = {protocol_id(name) for name in TARGET_MESSAGES}
    if len(target_ids) != len(TARGET_MESSAGES):
        raise ExtractionError("target numeric protocol-ID collision")
    validate_regressions()

    output_tsv, output_md, metrics = build_reports(
        baseline_text,
        delta_all,
        delta_text,
        validator,
        id_to_name,
        schemas,
        static_open,
        target_ids,
    )
    validate_output(output_tsv, output_md)

    # Close the read-only window before publishing either artifact.
    if snapshot_inputs(baseline_text) != baseline_before:
        raise ExtractionError("baseline CAPTURE text changed during extraction")
    if snapshot_inputs(delta_all) != delta_before:
        raise ExtractionError("CAPTURE delta changed during extraction")
    pinned_after = verify_pinned_files(external)
    if pinned_after != pinned_before:
        raise ExtractionError("pinned supporting input changed during extraction")

    output_paths = {
        external / "PF_CAPTURE_BRANCH_SHAPES_20260830.tsv": output_tsv,
        external / "PF_CAPTURE_BRANCH_SHAPES_20260830.md": output_md,
    }
    if args.check:
        for path, expected_text in output_paths.items():
            if not path.is_file():
                raise ExtractionError(f"check output missing: {path.name}")
            actual_text = path.read_text(encoding="utf-8")
            if actual_text != expected_text:
                raise ExtractionError(f"check output differs: {path.name}")
    else:
        atomic_publish(output_paths)

    print(
        "rows=%d added=%d existing=%d strict_instances=%d "
        "claim_unique_all=%d duplicate_baseline_all=%d duplicate_delta_all=%d mode=%s"
        % (
            metrics["rows"],
            metrics["added_shapes"],
            metrics["existing_shapes"],
            metrics["strict_instances"],
            metrics["claim_unique_all"],
            metrics["duplicate_baseline_all"],
            metrics["duplicate_delta_all"],
            "check" if args.check else "publish",
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ExtractionError as exc:
        raise SystemExit(f"ERROR: {exc}")
