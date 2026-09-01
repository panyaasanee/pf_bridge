#!/usr/bin/env python3
"""Validate the effective V2 A2 overlay against content-deduplicated captures.

The two outputs contain aggregate CAPTURE evidence only.  No capture payload,
field value, raw byte, hexdump, or capture path is exported.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Sequence


SOURCE = "CAPTURE"
IMAGE_SOURCE = "IMAGE"
EXPECTED_PROTOCOL_COUNT = 519
EXPECTED_CAPTURE_PATHS = 2_154
EXPECTED_CAPTURE_BYTES = 671_381_597
EXPECTED_UNIQUE_CONTENTS = 1_509
EXPECTED_DUPLICATE_PATHS = 645
EXPECTED_IMAGE_SIZE = 14_759_424
EXPECTED_IMAGE_SHA256 = (
    "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
)

INPUT_NAMES = (
    "PF_PROTOCOL_REGISTRY.tsv",
    "PF_SERIALIZER_FIELDS.tsv",
    "PF_TAG_CENSUS.tsv",
    "PF_INPUT_INVENTORY.tsv",
    "PF_CAPTURE_DELTA_20260830.inventory.tsv",
    "PF_A2_STRING_WIRE_TAG_DELTA.tsv",
    "PF_A3_TAG_CENSUS_DELTA.tsv",
    "PF_A2_POST_V1_STATIC_DELTA.tsv",
    "PF_A2_SERIALIZER_SLOT34_DELTA.tsv",
    "PF_A3_SERIALIZER_SLOT34_DELTA.tsv",
    "PF_A2_POOL_638690_DELTA.tsv",
    "PF_A2_POOL_661FA0_DELTA.tsv",
    "PF_A2_POOL_46F4D0_DELTA.tsv",
    "PF_A2_POOL_46BAA0_READER_DELTA.tsv",
    "PF_TARGET_652A30_A2_DELTA.tsv",
    "PF_TARGETS_694790_6B3440_A2_DELTA.tsv",
    "pf_validate_capture_fields.py",
    "../notes_to_chief/20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md",
)

# Filled only after a no-write preview has independently re-derived the corpus.
EXPECTED_INPUT_SHA256: dict[str, str] = {
    "../notes_to_chief/20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md": "89986128551a0728fc74aa159d9792f508acee46edb1224d583a263e49b5ab22",
    "PF_A2_POOL_46BAA0_READER_DELTA.tsv": "5099d8e6f09ac978c938f13d5059c2b735764ef7ed651ace28f9682880e317fa",
    "PF_A2_POOL_46F4D0_DELTA.tsv": "21c6ca53f12a1d4d299e971d0868aa871b1953eebabfed295af906c2b2c4315e",
    "PF_A2_POOL_638690_DELTA.tsv": "da2a808073fe61ab962ff641d2597aa47d9177bfbe30eaeefa8e14d1a94b94df",
    "PF_A2_POOL_661FA0_DELTA.tsv": "689d37c6e670402b8e9bff7bac78eeda8093c7a8c3f39c340e145ee6d57bbb4f",
    "PF_A2_POST_V1_STATIC_DELTA.tsv": "96e5a476baad2b0ceda79b2ef47bc5a85189551f76003139e1be4cd034f5afc2",
    "PF_A2_SERIALIZER_SLOT34_DELTA.tsv": "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334",
    "PF_A2_STRING_WIRE_TAG_DELTA.tsv": "e1f4f987c31f53d4dd87845aab01857c8415a8dbcd750af12df9c4cde208b3a2",
    "PF_A3_SERIALIZER_SLOT34_DELTA.tsv": "dd20d6dd263462259f4447357c3796604bce75d1bc9d8e5e200b9bb48b9bad87",
    "PF_A3_TAG_CENSUS_DELTA.tsv": "84f05381d34e81f117fa2c2e6a2bc82afe31932112c055c3ef8de1c8642fef53",
    "PF_CAPTURE_DELTA_20260830.inventory.tsv": "8a85dd1fff3d608ef0f0777331f9235152d2353e67adc76f4ae6275f8bfe6a3e",
    "PF_INPUT_INVENTORY.tsv": "729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1",
    "PF_PROTOCOL_REGISTRY.tsv": "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d",
    "PF_SERIALIZER_FIELDS.tsv": "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123",
    "PF_TAG_CENSUS.tsv": "63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a",
    "PF_TARGET_652A30_A2_DELTA.tsv": "217f7f9854df7412ca942d755c0ed858130954f93c8384185af9719415720592",
    "PF_TARGETS_694790_6B3440_A2_DELTA.tsv": "109c39dc16bf22edc97a607832c448f34aa0e0d7dc8f1dbef33f306e1be44dfe",
    "pf_validate_capture_fields.py": "0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8",
}
EXPECTED_RUN_COUNTS: dict[str, int] = {
    "baseline_decompressed_blocks": 41430,
    "baseline_mismatch": 271,
    "baseline_observed_rows": 58,
    "baseline_parse_success": 11903,
    "baseline_pc_blocks": 10462,
    "baseline_schema_not_applied": 0,
    "baseline_static_open": 52501,
    "block_errors": 0,
    "decompressed_blocks": 61611,
    "duplicate_rejected_decompressed_blocks": 4,
    "duplicate_rejected_mismatch": 0,
    "duplicate_rejected_observed_rows": 3,
    "duplicate_rejected_parse_success": 4,
    "duplicate_rejected_pc_blocks": 0,
    "duplicate_rejected_schema_not_applied": 0,
    "duplicate_rejected_static_open": 4,
    "files_with_blocks": 392,
    "framing_unresolved": 0,
    "mismatch": 386,
    "nested_declared": 25228,
    "nested_reached": 24599,
    "nested_unresolved_mismatch": 426,
    "nested_unresolved_not_applied": 0,
    "nested_unresolved_static_open": 203,
    "new_decompressed_blocks": 20181,
    "new_mismatch": 115,
    "new_observed_rows": 50,
    "new_parse_success": 11062,
    "new_pc_blocks": 5211,
    "new_schema_not_applied": 0,
    "new_static_open": 26031,
    "no_runtime_tail": 5542,
    "observed_rows": 66,
    "outer_instances": 77284,
    "parse_success": 22965,
    "pc_blocks": 15673,
    "runtime_zero_tail": 13879,
    "schema_not_applied": 0,
    "static_open": 78532,
    "unique_text_files": 948,
    "unknown_message_ids": 0,
}
EXPECTED_MISMATCH_POINTS: dict[tuple[str, str, str, str], int] = {
    (
        "TeleportVital",
        "R",
        "BASE:0de634db4db1ff42639f6ded73ce9bfbab8b6a4b50e3ec32c36860dfeb0eb21e;DELTA:88ee2c5ddeac7aff9f0fc73b0eb32f2a77ad060215c59ae11b12d2d364e17563;ORDER:20",
        "STRING_TAG",
    ): 190,
    (
        "TeleportVital",
        "W",
        "BASE:a9a17c82ae3d6f93644f407b6284ec736cead8f6652e010c5852e4900abed0fa;ORDER:4",
        "TAG",
    ): 188,
    (
        "TradeCmdVital",
        "W",
        "BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5",
        "TAG",
    ): 6,
    (
        "TradeCmdVital",
        "W",
        "BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5",
        "TRUNCATED_TAG",
    ): 2,
}

# Independently replayed with the immutable V1 schema over the same
# content-deduplicated corpus.  These are reconciliation pins, not V2 results.
V1_SCHEMA_CONTENT_DEDUP_COUNTS = {
    "parse_success": 22_963,
    "static_open": 78_920,
    "schema_not_applied": 0,
    "mismatch": 0,
}
EXPECTED_OUTPUT_SHA256: dict[str, str] = {
    "PF_V2_FIELD_VALIDATION.md": "3ebe5d7d472dbe72c0ba4436cf49cd661e8351c0136f13b81f8fbc2a921d1fa4",
    "PF_V2_FIELD_VALIDATION.tsv": "10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806",
}
EXPECTED_OVERLAY_COUNTS: dict[str, int] = {
    "base_rows": 6931,
    "effective_rows": 8795,
    "generic_changed": 35,
    "generic_removed": 160,
    "slot_added_canonical": 2130,
    "slot_candidates": 56,
    "slot_overlay_removed": 8,
    "slot_removed": 114,
    "string_changed": 408,
}
EXPECTED_PLAN_CENSUS: dict[str, int] = {
    "APPLICABLE": 606,
    "SCHEMA_NOT_APPLIED": 46,
    "STATIC_OPEN": 386,
}
EXPECTED_CORPUS_DIGEST = "c07c81161349de0ef68285cb8319a40b2aae660bbf8bf5dcf6844775f30877ee"

OUTPUT_TSV = "PF_V2_FIELD_VALIDATION.tsv"
OUTPUT_MD = "PF_V2_FIELD_VALIDATION.md"

PC_MARKER_RE = re.compile(r"^(PC|DECOMPRESSED) ([0-9]+)$")
HEXDUMP_RE = re.compile(r"^([0-9A-Fa-f]{8})  (.*?)  \|")
RAW_BYTE_RUN_RE = re.compile(
    r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"
)
NUMERIC_TAG_RE = re.compile(r"0x[0-9A-F]{2}")
ALT_ORDER_RE = re.compile(r"([1-9][0-9]*)_ALT")
KIND_GATE_RE = re.compile(r"kind==([0-9]+)")
ZERO_LENGTH_TAGS = {
    "EMPTY",
    "PURE_READONLY_CHAIN_PLUS_04_CONTAINS_PREDICATE",
}
STRING_TAGS = {"0x44": "STRING8", "0x48": "WSTRING16"}
RUNTIME_RESPONSE_ID = 0x6E9D


class ValidationError(RuntimeError):
    pass


@dataclass(frozen=True)
class CaptureInput:
    relative_path: str
    path: Path
    size: int
    sha256: str


@dataclass(frozen=True)
class EffectiveField:
    sequence: int
    field_identity: str
    origin_order: str
    wire_order: str
    tag: str
    length: str
    field_offset: str
    gate_condition: str
    origin_field_offset: str
    origin_gate_condition: str
    provenance: str
    evidence_key: str


@dataclass(frozen=True)
class SchemaPlan:
    message: str
    direction: str
    variant: str
    state: str
    blockers: tuple[str, ...]
    fields: tuple[EffectiveField, ...]


@dataclass(frozen=True)
class SchemaResult:
    status: str
    end: int
    field_identity: str = "N/A"
    reason: str = "NONE"
    blockers: tuple[str, ...] = ()
    record_instances: int = 0
    record_kinds: tuple[int, ...] = ()


@dataclass
class MessageAggregate:
    observed_instances: int = 0
    pass_instances: int = 0
    static_open_instances: int = 0
    not_applied_instances: int = 0
    mismatch_instances: int = 0
    observed_frames: set[str] = field(default_factory=set)
    pass_frames: set[str] = field(default_factory=set)
    static_open_frames: set[str] = field(default_factory=set)
    not_applied_frames: set[str] = field(default_factory=set)
    mismatch_frames: set[str] = field(default_factory=set)
    capture_files: set[str] = field(default_factory=set)
    mismatch_points: Counter[tuple[str, str]] = field(default_factory=Counter)
    static_open_reasons: Counter[str] = field(default_factory=Counter)
    not_applied_reasons: Counter[str] = field(default_factory=Counter)
    record_instances_observed: int = 0
    record_kinds: Counter[int] = field(default_factory=Counter)


@dataclass
class RunCounts:
    capture_text_files: int = 0
    files_with_blocks: set[str] = field(default_factory=set)
    pc_blocks: int = 0
    decompressed_blocks: int = 0
    block_errors: Counter[str] = field(default_factory=Counter)
    outer_instances: int = 0
    nested_declared_instances: int = 0
    nested_reached_instances: int = 0
    nested_unresolved_after_static_open: int = 0
    nested_unresolved_after_not_applied: int = 0
    nested_unresolved_after_mismatch: int = 0
    unknown_message_id_instances: int = 0
    no_runtime_tail_frames: int = 0
    runtime_zero_tail_frames: int = 0
    framing_unresolved_frames: int = 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_path_key(value: str) -> tuple[str, str]:
    return value.casefold(), value


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ValidationError(f"missing TSV header: {path.name}")
        return list(reader.fieldnames), [dict(row) for row in reader]


def canonical_row_key(fieldnames: Sequence[str], row: Mapping[str, str]) -> str:
    payload = json.dumps(
        [row[name] for name in fieldnames],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def protocol_id(name: str) -> int:
    return sum((index + 1) * ord(character) for index, character in enumerate(name)) & 0xFFFF


def tsv_text(headers: list[str], rows: list[list[str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return buffer.getvalue()


def enumerate_capture_paths(root: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for directory in root.rglob("capture_*"):
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            folded = relative.casefold()
            if folded in paths and paths[folded] != path:
                raise ValidationError(f"case-folded capture path collision: {relative}")
            paths[folded] = path
    return paths


def load_capture_inventory(
    root: Path, base_inventory: Path, delta_inventory: Path
) -> tuple[list[CaptureInput], list[CaptureInput], set[str], str]:
    _base_headers, base_rows_all = read_tsv(base_inventory)
    _delta_headers, delta_rows = read_tsv(delta_inventory)
    base_rows = [row for row in base_rows_all if row.get("source") == SOURCE]
    if len(base_rows) != 1_772 or len(delta_rows) != 382:
        raise ValidationError("capture inventory partition changed")
    if Counter(row.get("source", "") for row in delta_rows) != Counter(
        {SOURCE: len(delta_rows)}
    ):
        raise ValidationError("capture delta inventory source changed")
    rows = base_rows + delta_rows
    relative_paths = [row["relative_path"] for row in rows]
    if len({value.casefold() for value in relative_paths}) != len(relative_paths):
        raise ValidationError("duplicate inventory relative path")
    if len(rows) != EXPECTED_CAPTURE_PATHS:
        raise ValidationError("capture path census changed")
    if sum(int(row["size"]) for row in rows) != EXPECTED_CAPTURE_BYTES:
        raise ValidationError("capture byte census changed")
    fresh = enumerate_capture_paths(root)
    if set(fresh) != {value.casefold() for value in relative_paths}:
        raise ValidationError("fresh capture path set differs from pinned inventories")

    all_inputs: list[CaptureInput] = []
    for row in sorted(rows, key=lambda item: stable_path_key(item["relative_path"])):
        relative = row["relative_path"]
        path = fresh[relative.casefold()]
        size = int(row["size"])
        expected_hash = row["sha256"].lower()
        stat = path.stat()
        actual_hash = sha256_file(path)
        if stat.st_size != size or actual_hash != expected_hash:
            raise ValidationError(f"capture input changed: {relative}")
        all_inputs.append(CaptureInput(relative, path, size, expected_hash))

    by_hash: dict[str, list[CaptureInput]] = defaultdict(list)
    for item in all_inputs:
        by_hash[item.sha256].append(item)
    if len(by_hash) != EXPECTED_UNIQUE_CONTENTS:
        raise ValidationError("unique capture-content census changed")
    canonical = [
        sorted(items, key=lambda item: stable_path_key(item.relative_path))[0]
        for items in by_hash.values()
    ]
    canonical.sort(key=lambda item: stable_path_key(item.relative_path))
    if len(all_inputs) - len(canonical) != EXPECTED_DUPLICATE_PATHS:
        raise ValidationError("duplicate capture-path census changed")
    inventory_payload = "".join(
        f"{item.relative_path}\t{item.size}\t{item.sha256}\n" for item in all_inputs
    )
    baseline_hashes = {row["sha256"].lower() for row in base_rows}
    if len(baseline_hashes) != 1_189:
        raise ValidationError("baseline unique-content census changed")
    if len(set(by_hash) - baseline_hashes) != 320:
        raise ValidationError("new unique-content census changed")
    return all_inputs, canonical, baseline_hashes, sha256_text(inventory_payload)


def verify_capture_inputs(inputs: Iterable[CaptureInput]) -> None:
    for item in inputs:
        stat = item.path.stat()
        if stat.st_size != item.size or sha256_file(item.path) != item.sha256:
            raise ValidationError(f"capture input changed during validation: {item.relative_path}")


def verify_capture_snapshot(root: Path, inputs: Sequence[CaptureInput]) -> None:
    """Re-enumerate and re-hash the complete capture set at the final boundary."""
    fresh = enumerate_capture_paths(root)
    expected = {item.relative_path.casefold(): item for item in inputs}
    if set(fresh) != set(expected):
        added = sorted(set(fresh) - set(expected))
        removed = sorted(set(expected) - set(fresh))
        raise ValidationError(
            f"capture path set changed during validation: added={added[:3]} removed={removed[:3]}"
        )
    for folded, item in expected.items():
        path = fresh[folded]
        stat = path.stat()
        if stat.st_size != item.size or sha256_file(path) != item.sha256:
            raise ValidationError(
                f"capture input changed during validation: {item.relative_path}"
            )


def verify_pinned_inputs(external: Path, allow_unpinned: bool) -> dict[str, str]:
    measured = {name: sha256_file(external / name) for name in INPUT_NAMES}
    if allow_unpinned:
        return measured
    if EXPECTED_INPUT_SHA256:
        if measured != EXPECTED_INPUT_SHA256:
            changed = sorted(
                name
                for name in set(measured) | set(EXPECTED_INPUT_SHA256)
                if measured.get(name) != EXPECTED_INPUT_SHA256.get(name)
            )
            raise ValidationError(f"pinned V2 validation inputs changed: {changed}")
    elif not allow_unpinned:
        raise ValidationError("input SHA-256 pins have not been frozen")
    return measured


def validate_ctrace_container_contract(external: Path) -> None:
    note_name = (
        "../notes_to_chief/"
        "20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md"
    )
    text = (external / note_name).read_text(encoding="utf-8")
    required = (
        "tag 0x12 / width 2` เป็นจำนวน records",
        "loop stride `0x18`",
        "`kind=2 -> +0/+4/+8`, `kind=1 -> +0/+C`",
    )
    if any(fragment not in text for fragment in required):
        raise ValidationError("RE-119 CTrace container/branch contract changed")


def make_effective_field_from_base(
    row: Mapping[str, str], sequence: int, base_key: str
) -> EffectiveField:
    order = row["order"]
    return EffectiveField(
        sequence=sequence,
        field_identity=f"BASE:{base_key};ORDER:{order}",
        origin_order=order,
        wire_order=order,
        tag=row["tag"],
        length=row["len"],
        field_offset=row["field_offset"],
        gate_condition=row["gate_condition"],
        origin_field_offset=row["field_offset"],
        origin_gate_condition=row["gate_condition"],
        provenance="V1",
        evidence_key=base_key,
    )


def apply_effective_overlays(
    external: Path,
) -> tuple[
    list[dict[str, str]],
    dict[tuple[str, str], list[EffectiveField]],
    dict[tuple[str, str, str], list[EffectiveField]],
    dict[str, int],
]:
    registry_headers, registry_rows = read_tsv(external / "PF_PROTOCOL_REGISTRY.tsv")
    base_headers, base_rows = read_tsv(external / "PF_SERIALIZER_FIELDS.tsv")
    if len(registry_rows) != EXPECTED_PROTOCOL_COUNT:
        raise ValidationError("registry census changed")
    if Counter(row.get("source", "") for row in registry_rows) != Counter(
        {IMAGE_SOURCE: len(registry_rows)}
    ):
        raise ValidationError("registry source boundary changed")
    if Counter(row.get("source", "") for row in base_rows) != Counter(
        {IMAGE_SOURCE: len(base_rows)}
    ):
        raise ValidationError("V1 A2 source boundary changed")
    if len({row["name"] for row in registry_rows}) != EXPECTED_PROTOCOL_COUNT:
        raise ValidationError("duplicate registry name")
    if registry_headers[-1] != "source" or base_headers[-1] != "source":
        raise ValidationError("V1 source column moved or disappeared")

    base_by_key: dict[str, tuple[int, dict[str, str]]] = {}
    base_by_line: dict[int, tuple[str, dict[str, str]]] = {}
    for line, row in enumerate(base_rows, start=2):
        key = canonical_row_key(base_headers, row)
        if key in base_by_key:
            raise ValidationError("duplicate V1 A2 canonical row key")
        base_by_key[key] = (line, row)
        base_by_line[line] = (key, row)

    string_headers, string_rows = read_tsv(
        external / "PF_A2_STRING_WIRE_TAG_DELTA.tsv"
    )
    del string_headers
    if Counter(row.get("source", "") for row in string_rows) != Counter(
        {IMAGE_SOURCE: len(string_rows)}
    ):
        raise ValidationError("string correction source boundary changed")
    string_by_key: dict[str, dict[str, str]] = {}
    for delta in string_rows:
        if delta["delta_action"] != "CHANGED":
            raise ValidationError("string correction copied an unchanged row")
        line = int(delta["base_row_number"])
        key, base = base_by_line.get(line, ("", {}))
        expected = {
            "message": delta["message"],
            "direction(W/R)": delta["direction(W/R)"],
            "order": delta["order"],
            "field_offset": delta["field_offset"],
            "tag": delta["original_tag"],
            "len": delta["original_payload_len"],
        }
        if not base or any(base[name] != value for name, value in expected.items()):
            raise ValidationError(f"string correction base mismatch at line {line}")
        if key in string_by_key:
            raise ValidationError("duplicate string correction base key")
        string_by_key[key] = delta

    generic_names = (
        "PF_A2_POST_V1_STATIC_DELTA.tsv",
        "PF_A2_POOL_638690_DELTA.tsv",
        "PF_A2_POOL_661FA0_DELTA.tsv",
        "PF_A2_POOL_46F4D0_DELTA.tsv",
        "PF_A2_POOL_46BAA0_READER_DELTA.tsv",
        "PF_TARGET_652A30_A2_DELTA.tsv",
        "PF_TARGETS_694790_6B3440_A2_DELTA.tsv",
    )
    generic_by_key: dict[str, tuple[str, dict[str, str]]] = {}
    overlay_action_counts: Counter[str] = Counter()
    target_overlay_removals: list[dict[str, str]] = []
    for name in generic_names:
        _headers, rows = read_tsv(external / name)
        if Counter(row.get("source", "") for row in rows) != Counter(
            {IMAGE_SOURCE: len(rows)}
        ):
            raise ValidationError(f"{name} source boundary changed")
        for delta in rows:
            if delta["action"] == "REMOVE_OVERLAY_NONWIRE_ROW":
                if name not in {
                    "PF_TARGET_652A30_A2_DELTA.tsv",
                    "PF_TARGETS_694790_6B3440_A2_DELTA.tsv",
                }:
                    raise ValidationError("unexpected overlay-on-overlay removal")
                target_overlay_removals.append(delta)
                overlay_action_counts[f"{name}:{delta['action']}"] += 1
                continue
            if delta["action"] not in {"CHANGED", "REMOVE_NONWIRE_ROW"}:
                raise ValidationError(f"{name} contains unsupported/copy action")
            if delta["base_file"] != "PF_SERIALIZER_FIELDS.tsv":
                raise ValidationError(f"{name} targets an unexpected base")
            key = delta["base_row_key"]
            if key in generic_by_key:
                raise ValidationError(f"overlapping generic overlay base key: {key}")
            line, base = base_by_key.get(key, (0, {}))
            if not base or int(delta["base_line"]) != line:
                raise ValidationError(f"{name} base key/line mismatch")
            for old_name, base_name in (
                ("message", "message"),
                ("direction(W/R)", "direction(W/R)"),
                ("old_order", "order"),
                ("old_tag", "tag"),
                ("old_field_offset", "field_offset"),
                ("old_len", "len"),
            ):
                if delta[old_name] != base[base_name]:
                    raise ValidationError(f"{name} old-row contract mismatch")
            generic_by_key[key] = (name, delta)
            overlay_action_counts[f"{name}:{delta['action']}"] += 1

    slot_headers, slot_rows = read_tsv(
        external / "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
    )
    if Counter(row.get("source", "") for row in slot_rows) != Counter(
        {IMAGE_SOURCE: len(slot_rows)}
    ):
        raise ValidationError("slot34 correction source boundary changed")
    slot_remove: dict[str, dict[str, str]] = {}
    slot_add: list[tuple[int, dict[str, str]]] = []
    slot_candidates: list[tuple[int, dict[str, str]]] = []
    slot_rows_by_key = {
        canonical_row_key(slot_headers, row): (line, row)
        for line, row in enumerate(slot_rows, start=2)
    }
    if len(slot_rows_by_key) != len(slot_rows):
        raise ValidationError("duplicate slot34 overlay canonical row key")
    target_slot_delta_keys: set[str] = set()
    for removal in target_overlay_removals:
        if removal["base_file"] != "PF_A2_SERIALIZER_SLOT34_DELTA.tsv":
            raise ValidationError("target overlay removal names an unexpected base")
        line, base = slot_rows_by_key.get(removal["base_row_key"], (0, {}))
        if not base or int(removal["base_line"]) != line:
            raise ValidationError("target slot-overlay key/line mismatch")
        if removal["base_delta_key"] != base["delta_key"]:
            raise ValidationError("target slot-overlay delta-key mismatch")
        for old_name, slot_name in (
            ("message", "message"),
            ("direction(W/R)", "direction(W/R)"),
            ("old_order", "new_order"),
            ("old_tag", "new_tag"),
            ("old_field_offset", "new_field_offset"),
            ("old_len", "new_len"),
        ):
            if removal[old_name] != base[slot_name]:
                raise ValidationError("target slot-overlay old-row contract mismatch")
        if base["delta_key"] in target_slot_delta_keys:
            raise ValidationError("duplicate target slot-overlay removal")
        target_slot_delta_keys.add(base["delta_key"])
    for index, delta in enumerate(slot_rows):
        action = delta["action"]
        overlay_action_counts[f"PF_A2_SERIALIZER_SLOT34_DELTA.tsv:{action}"] += 1
        if action == "REMOVE_WRONG_SLOT_ROW":
            key = delta["base_row_key"]
            line, base = base_by_key.get(key, (0, {}))
            if not base or int(delta["base_line"]) != line:
                raise ValidationError("slot34 removal base mismatch")
            if key in slot_remove:
                raise ValidationError("duplicate slot34 removal")
            slot_remove[key] = delta
        elif action in {"ADD_CORRECTED_SLOT34_ROW", "ADD_ANALYSIS_BLOCKER_ROW"}:
            if delta["schema_variant"] != "SINGLETON_SLOT34":
                raise ValidationError("canonical slot34 row has a non-singleton variant")
            if delta["delta_key"] not in target_slot_delta_keys:
                slot_add.append((index, delta))
        elif action == "ADD_AMBIGUOUS_CANDIDATE_ROW":
            if delta["message"] != "ItemAttr":
                raise ValidationError("non-ItemAttr ambiguous slot34 candidate")
            slot_candidates.append((index, delta))
        else:
            raise ValidationError("slot34 correction contains an unsupported action")

    target_sets = [set(string_by_key), set(generic_by_key), set(slot_remove)]
    for left_index, left in enumerate(target_sets):
        for right in target_sets[left_index + 1 :]:
            overlap = left & right
            if overlap:
                raise ValidationError(f"overlay base-key overlap: {sorted(overlap)[:3]}")

    effective: dict[tuple[str, str], list[EffectiveField]] = defaultdict(list)
    for sequence, base in enumerate(base_rows):
        key = canonical_row_key(base_headers, base)
        if key in slot_remove:
            continue
        generic = generic_by_key.get(key)
        if generic is not None and generic[1]["action"] == "REMOVE_NONWIRE_ROW":
            continue
        field_value = make_effective_field_from_base(base, sequence, key)
        string_delta = string_by_key.get(key)
        if string_delta is not None:
            field_value = EffectiveField(
                **{
                    **field_value.__dict__,
                    "tag": string_delta["corrected_tag"],
                    "length": string_delta["corrected_full_wire_len"],
                    "provenance": "STRING_CORRECTION",
                    "field_identity": (
                        f"BASE:{key};DELTA:{string_delta['dedup_key']};ORDER:{base['order']}"
                    ),
                    "evidence_key": string_delta["dedup_key"],
                }
            )
        if generic is not None:
            name, delta = generic
            wire_order = delta["new_wire_order"]
            identity = (
                f"BASE:{key};DELTA:{delta['delta_key']};"
                f"ORDER:{base['order']}->WIRE:{wire_order}"
            )
            field_value = EffectiveField(
                sequence=sequence,
                field_identity=identity,
                origin_order=base["order"],
                wire_order=wire_order,
                tag=delta["new_tag"],
                length=delta["new_len"],
                field_offset=delta["new_field_offset"],
                gate_condition=delta["new_gate_condition"],
                origin_field_offset=base["field_offset"],
                origin_gate_condition=base["gate_condition"],
                provenance=name,
                evidence_key=delta["delta_key"],
            )
        effective[(base["message"], base["direction(W/R)"])].append(field_value)

    slot_sequence_base = len(base_rows) + 10_000
    for relative_sequence, (_index, delta) in enumerate(slot_add):
        field_value = EffectiveField(
            sequence=slot_sequence_base + relative_sequence,
            field_identity=f"SLOT34:{delta['new_order']}",
            origin_order="N/A",
            wire_order=delta["new_order"],
            tag=delta["new_tag"],
            length=delta["new_len"],
            field_offset=delta["new_field_offset"],
            gate_condition=delta["new_gate_condition"],
            origin_field_offset="N/A",
            origin_gate_condition="N/A",
            provenance=delta["action"],
            evidence_key=delta["delta_key"],
        )
        effective[(delta["message"], delta["direction(W/R)"])].append(field_value)

    candidate_schemas: dict[tuple[str, str, str], list[EffectiveField]] = defaultdict(list)
    for relative_sequence, (_index, delta) in enumerate(slot_candidates):
        field_value = EffectiveField(
            sequence=relative_sequence,
            field_identity=f"{delta['schema_variant']}:{delta['new_order']}",
            origin_order="N/A",
            wire_order=delta["new_order"],
            tag=delta["new_tag"],
            length=delta["new_len"],
            field_offset=delta["new_field_offset"],
            gate_condition=delta["new_gate_condition"],
            origin_field_offset="N/A",
            origin_gate_condition="N/A",
            provenance="AMBIGUOUS_CANDIDATE_ONLY",
            evidence_key=delta["delta_key"],
        )
        candidate_schemas[
            (delta["message"], delta["direction(W/R)"], delta["schema_variant"])
        ].append(field_value)

    names = {row["name"] for row in registry_rows}
    for name in names:
        for direction in ("W", "R"):
            effective.setdefault((name, direction), [])
    for fields in effective.values():
        fields.sort(key=lambda value: value.sequence)
    for fields in candidate_schemas.values():
        fields.sort(key=lambda value: value.sequence)

    validate_effective_tag_census(external, effective)
    counts = {
        "base_rows": len(base_rows),
        "string_changed": len(string_rows),
        "generic_changed": sum(
            count for key, count in overlay_action_counts.items() if key.endswith(":CHANGED")
        ),
        "generic_removed": sum(
            count
            for key, count in overlay_action_counts.items()
            if key.endswith(":REMOVE_NONWIRE_ROW")
            or key.endswith(":REMOVE_OVERLAY_NONWIRE_ROW")
        ),
        "slot_removed": len(slot_remove),
        "slot_added_canonical": len(slot_add),
        "slot_overlay_removed": len(target_slot_delta_keys),
        "slot_candidates": len(slot_candidates),
        "effective_rows": sum(len(rows) for rows in effective.values()),
    }
    return registry_rows, effective, candidate_schemas, counts


def validate_effective_tag_census(
    external: Path, effective: Mapping[tuple[str, str], list[EffectiveField]]
) -> None:
    _tag_headers, base_tag_rows = read_tsv(external / "PF_TAG_CENSUS.tsv")
    _string_headers, string_tag_rows = read_tsv(
        external / "PF_A3_TAG_CENSUS_DELTA.tsv"
    )
    _slot_headers, slot_tag_rows = read_tsv(
        external / "PF_A3_SERIALIZER_SLOT34_DELTA.tsv"
    )
    for rows, label in (
        (base_tag_rows, "V1 A3"),
        (string_tag_rows, "string A3"),
        (slot_tag_rows, "slot34 A3"),
    ):
        if Counter(row.get("source", "") for row in rows) != Counter(
            {IMAGE_SOURCE: len(rows)}
        ):
            raise ValidationError(f"{label} source boundary changed")
    base_numeric = {
        row["tag"]: row
        for row in base_tag_rows
        if NUMERIC_TAG_RE.fullmatch(row["tag"])
    }
    string_numeric = {row["tag"]: row for row in string_tag_rows}
    slot_singleton = {
        row["tag"]: row
        for row in slot_tag_rows
        if row["count_semantics"] == "ADD_TO_EFFECTIVE_BASE"
    }
    measured = Counter(
        field_value.tag
        for fields in effective.values()
        for field_value in fields
        if NUMERIC_TAG_RE.fullmatch(field_value.tag)
    )
    expected: dict[str, int] = {}
    for tag, row in base_numeric.items():
        expected[tag] = int(row["frequency_in_A2"])
    for tag, row in string_numeric.items():
        if row["delta_action"] != "ADDED" or row["len_status_for_tag"] != "VARIABLE":
            raise ValidationError("string A3 delta contract changed")
        expected[tag] = int(row["frequency_in_A2"])
    for tag, row in slot_singleton.items():
        if int(row["frequency_before"]) != expected.get(tag, 0):
            raise ValidationError(f"slot34 A3 base frequency changed for {tag}")
        expected[tag] = int(row["effective_frequency"])
    if dict(measured) != expected:
        difference = {
            tag: (expected.get(tag, 0), measured.get(tag, 0))
            for tag in sorted(set(expected) | set(measured))
            if expected.get(tag, 0) != measured.get(tag, 0)
        }
        raise ValidationError(f"effective A2/A3 frequency mismatch: {difference}")
    length_oracle = {
        tag: row["len"] for tag, row in base_numeric.items()
    } | {tag: row["len"] for tag, row in string_numeric.items()}
    for fields in effective.values():
        for field_value in fields:
            if not NUMERIC_TAG_RE.fullmatch(field_value.tag):
                continue
            expected_length = length_oracle[field_value.tag]
            if field_value.length != expected_length:
                raise ValidationError(
                    f"effective A2/A3 length mismatch: {field_value.tag} "
                    f"{field_value.length} != {expected_length}"
                )


def subcall_is_flattened(field_value: EffectiveField, fields: Sequence[EffectiveField]) -> bool:
    target = field_value.tag.split(":", 1)[1]
    for candidate in fields:
        if candidate.sequence <= field_value.sequence:
            continue
        searchable = " ".join(
            (
                candidate.field_offset,
                candidate.origin_field_offset,
                candidate.gate_condition,
                candidate.origin_gate_condition,
            )
        )
        if target in searchable and not candidate.tag.startswith("SUBCALL:"):
            return True
    return False


def build_schema_plans(
    registry_rows: list[dict[str, str]],
    effective: Mapping[tuple[str, str], list[EffectiveField]],
    candidates: Mapping[tuple[str, str, str], list[EffectiveField]],
) -> tuple[dict[int, str], dict[tuple[str, str], SchemaPlan]]:
    id_to_name: dict[int, str] = {}
    for row in registry_rows:
        message_id = protocol_id(row["name"])
        if message_id in id_to_name:
            raise ValidationError("protocol ID collision")
        id_to_name[message_id] = row["name"]
    item_variants = {
        variant for name, _direction, variant in candidates if name == "ItemAttr"
    }
    if item_variants != {"VTABLE_0x00F0EBB0", "VTABLE_0x00F4A188"}:
        raise ValidationError(f"ItemAttr candidate variants changed: {item_variants}")

    plans: dict[tuple[str, str], SchemaPlan] = {}
    supported_tags = ZERO_LENGTH_TAGS | set(STRING_TAGS)
    for key, fields_list in effective.items():
        fields = tuple(fields_list)
        blockers: set[str] = set()
        static_reasons: set[str] = set()
        if key[0] == "ItemAttr":
            blockers.add("ITEMATTR_CANDIDATE_SCHEMAS_NOT_MERGED")
        for field_value in fields:
            tag = field_value.tag
            if tag == "UNKNOWN" or "UNKNOWN(" in field_value.field_offset:
                static_reasons.add("IMAGE_STATIC_FIELD_UNRESOLVED")
            elif (
                not NUMERIC_TAG_RE.fullmatch(tag)
                and tag not in supported_tags
                and not tag.startswith("SUBCALL:")
            ):
                static_reasons.add("IMAGE_STATIC_TAG_UNRESOLVED")
            if tag.startswith("SUBCALL:") and not subcall_is_flattened(field_value, fields):
                blockers.add("UNFLATTENED_SUBCALL")
            if field_value.wire_order and not (
                field_value.wire_order.isdigit()
                or ALT_ORDER_RE.fullmatch(field_value.wire_order)
            ):
                blockers.add("UNSUPPORTED_DECLARED_ORDER_LABEL")
            kind_gate = KIND_GATE_RE.fullmatch(field_value.gate_condition)
            if kind_gate is not None and key[0] != "CTracePathVital":
                blockers.add("KIND_GATE_OUTSIDE_CTRACE")
            if (
                field_value.gate_condition.startswith("test@")
                and " mask=" in field_value.gate_condition
            ):
                blockers.add("UNEXECUTED_MASK_GATE")
            if (
                ("!=NULL" in field_value.gate_condition or "DECODED_" in field_value.gate_condition)
                and tag.startswith("SUBCALL:")
            ):
                blockers.add("UNEXECUTED_PRESENCE_GATE")
        if static_reasons:
            state = "STATIC_OPEN"
            reasons = tuple(sorted(static_reasons))
        elif blockers:
            state = "SCHEMA_NOT_APPLIED"
            reasons = tuple(sorted(blockers))
        else:
            state = "APPLICABLE"
            reasons = ()
        plans[key] = SchemaPlan(
            message=key[0],
            direction=key[1],
            variant=(
                "CANONICAL_WITHHELD_ITEMATTR_AMBIGUITY"
                if key[0] == "ItemAttr"
                else "CANONICAL_EFFECTIVE_V2"
            ),
            state=state,
            blockers=reasons,
            fields=fields,
        )

    ctrace = [plans[("CTracePathVital", direction)] for direction in ("W", "R")]
    if any(plan.state != "APPLICABLE" for plan in ctrace):
        raise ValidationError("CTrace conditional/gapped plan is not applicable")
    for plan in ctrace:
        labels = {field_value.wire_order for field_value in plan.fields}
        if "6_ALT" not in labels:
            raise ValidationError("CTrace 6_ALT identity was lost")
    for message, direction in (
        ("TeleportVital", "W"),
        ("TeleportVital", "R"),
        ("TradeCmdVital", "W"),
    ):
        if plans[(message, direction)].state != "APPLICABLE":
            raise ValidationError(f"red-probe control is not applicable: {message} {direction}")
    return id_to_name, plans


def schema_plan_key(plan: SchemaPlan) -> str:
    payload = {
        "message": plan.message,
        "direction": plan.direction,
        "variant": plan.variant,
        "state": plan.state,
        "blockers": list(plan.blockers),
        "fields": [
            {
                "sequence": field_value.sequence,
                "identity": field_value.field_identity,
                "origin_order": field_value.origin_order,
                "wire_order": field_value.wire_order,
                "tag": field_value.tag,
                "length": field_value.length,
                "field_offset": field_value.field_offset,
                "gate_condition": field_value.gate_condition,
                "provenance": field_value.provenance,
                "evidence_key": field_value.evidence_key,
            }
            for field_value in plan.fields
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def parse_one_field(
    data: bytes, position: int, field_value: EffectiveField
) -> tuple[SchemaResult, int | None]:
    tag = field_value.tag
    if tag in ZERO_LENGTH_TAGS or tag.startswith("SUBCALL:"):
        return SchemaResult("PASS", position), None
    if tag in STRING_TAGS:
        if position >= len(data):
            return (
                SchemaResult(
                    "MISMATCH", position, field_value.field_identity, "TRUNCATED_STRING_TAG"
                ),
                None,
            )
        if data[position] != int(tag, 16):
            return (
                SchemaResult("MISMATCH", position, field_value.field_identity, "STRING_TAG"),
                None,
            )
        if position + 5 > len(data):
            return (
                SchemaResult(
                    "MISMATCH",
                    position,
                    field_value.field_identity,
                    "TRUNCATED_STRING_LENGTH",
                ),
                None,
            )
        byte_length = int.from_bytes(data[position + 1 : position + 5], "little")
        if tag == "0x48" and byte_length % 2:
            return (
                SchemaResult(
                    "MISMATCH",
                    position,
                    field_value.field_identity,
                    "ODD_UTF16_BYTE_LENGTH",
                ),
                None,
            )
        end = position + 5 + byte_length
        if end > len(data):
            return (
                SchemaResult(
                    "MISMATCH",
                    position,
                    field_value.field_identity,
                    "TRUNCATED_STRING_PAYLOAD",
                ),
                None,
            )
        return SchemaResult("PASS", end), None
    if not NUMERIC_TAG_RE.fullmatch(tag) or not field_value.length.isdigit():
        raise ValidationError(f"applicable schema contains unsupported field: {tag}")
    if position >= len(data):
        return (
            SchemaResult("MISMATCH", position, field_value.field_identity, "TRUNCATED_TAG"),
            None,
        )
    if data[position] != int(tag, 16):
        return (
            SchemaResult("MISMATCH", position, field_value.field_identity, "TAG"),
            None,
        )
    value_length = int(field_value.length)
    end = position + 1 + value_length
    if end > len(data):
        return (
            SchemaResult(
                "MISMATCH", position, field_value.field_identity, "TRUNCATED_VALUE"
            ),
            None,
        )
    scalar = None
    if value_length <= 8:
        scalar = int.from_bytes(data[position + 1 : end], "little")
    return SchemaResult("PASS", end), scalar


def parse_schema(data: bytes, start: int, plan: SchemaPlan) -> SchemaResult:
    if plan.state == "STATIC_OPEN":
        return SchemaResult("STATIC_OPEN", start, blockers=plan.blockers)
    if plan.state == "SCHEMA_NOT_APPLIED":
        return SchemaResult("SCHEMA_NOT_APPLIED", start, blockers=plan.blockers)
    def parse_sequence(
        fields: Sequence[EffectiveField], position: int
    ) -> tuple[SchemaResult, dict[str, int]]:
        context: dict[str, int] = {}
        for field_value in fields:
            kind_match = KIND_GATE_RE.fullmatch(field_value.gate_condition)
            if kind_match is not None:
                if "kind" not in context:
                    return (
                        SchemaResult(
                            "SCHEMA_NOT_APPLIED",
                            start,
                            blockers=("KIND_CONTROLLER_NOT_REACHED",),
                        ),
                        context,
                    )
                if context["kind"] != int(kind_match.group(1)):
                    continue
            outcome, scalar = parse_one_field(data, position, field_value)
            if outcome.status != "PASS":
                return outcome, context
            position = outcome.end
            if (
                plan.message == "CTracePathVital"
                and field_value.field_offset == "RECORD+0x16"
                and field_value.length == "1"
                and scalar is not None
            ):
                context["kind"] = scalar
            if (
                plan.message == "CTracePathVital"
                and field_value.origin_order == "2"
                and field_value.tag == "0x12"
                and scalar is not None
            ):
                context["record_count"] = scalar
        return SchemaResult("PASS", position), context

    if plan.message == "CTracePathVital":
        marker_indexes = [
            index
            for index, field_value in enumerate(plan.fields)
            if field_value.tag == "SUBCALL:0x006EB960"
        ]
        if len(marker_indexes) != 1:
            return SchemaResult(
                "SCHEMA_NOT_APPLIED",
                start,
                blockers=("CTRACE_RECORD_BOUNDARY_UNRESOLVED",),
            )
        marker_index = marker_indexes[0]
        prefix_result, prefix_context = parse_sequence(
            plan.fields[:marker_index], start
        )
        if prefix_result.status != "PASS":
            return prefix_result
        record_count = prefix_context.get("record_count")
        if record_count is None:
            return SchemaResult(
                "SCHEMA_NOT_APPLIED",
                start,
                blockers=("CTRACE_RECORD_COUNT_UNRESOLVED",),
            )
        position = prefix_result.end
        record_fields = plan.fields[marker_index + 1 :]
        record_kinds: list[int] = []
        for _record_ordinal in range(record_count):
            record_result, record_context = parse_sequence(record_fields, position)
            if record_result.status != "PASS":
                return record_result
            position = record_result.end
            if "kind" in record_context:
                record_kinds.append(record_context["kind"])
        return SchemaResult(
            "PASS",
            position,
            record_instances=record_count,
            record_kinds=tuple(record_kinds),
        )

    position = start
    context: dict[str, int] = {}
    for field_value in plan.fields:
        kind_match = KIND_GATE_RE.fullmatch(field_value.gate_condition)
        if kind_match is not None:
            if "kind" not in context:
                return SchemaResult(
                    "SCHEMA_NOT_APPLIED",
                    start,
                    blockers=("KIND_CONTROLLER_NOT_REACHED",),
                )
            if context["kind"] != int(kind_match.group(1)):
                continue
        outcome, scalar = parse_one_field(data, position, field_value)
        if outcome.status != "PASS":
            return outcome
        position = outcome.end
        if (
            plan.message == "CTracePathVital"
            and field_value.field_offset == "RECORD+0x16"
            and field_value.length == "1"
            and scalar is not None
        ):
            context["kind"] = scalar
    return SchemaResult("PASS", position)


def extract_pc_blocks(text: str) -> tuple[list[tuple[str, bytes]], Counter[str]]:
    lines = text.splitlines()
    blocks: list[tuple[str, bytes]] = []
    errors: Counter[str] = Counter()
    index = 0
    while index < len(lines):
        marker = PC_MARKER_RE.match(lines[index])
        if marker is None:
            index += 1
            continue
        kind = marker.group(1)
        claimed_length = int(marker.group(2))
        index += 1
        payload = bytearray()
        expected_offset = 0
        bad_offset = False
        while index < len(lines):
            hexdump = HEXDUMP_RE.match(lines[index])
            if hexdump is None:
                break
            offset = int(hexdump.group(1), 16)
            tokens = hexdump.group(2).split()
            if offset != expected_offset:
                bad_offset = True
            if not tokens or any(
                not re.fullmatch(r"[0-9A-Fa-f]{2}", token) for token in tokens
            ):
                errors["INVALID_HEXDUMP_TOKEN"] += 1
                bad_offset = True
                index += 1
                continue
            payload.extend(int(token, 16) for token in tokens)
            expected_offset = len(payload)
            index += 1
        if bad_offset:
            errors["HEXDUMP_OFFSET"] += 1
        elif len(payload) != claimed_length:
            errors["CLAIMED_LENGTH"] += 1
        else:
            blocks.append((kind, bytes(payload)))
    return blocks, errors


def record_outcome(
    aggregate: MessageAggregate,
    frame_key: str,
    file_key: str,
    outcome: SchemaResult,
) -> None:
    aggregate.observed_instances += 1
    aggregate.observed_frames.add(frame_key)
    aggregate.capture_files.add(file_key)
    if outcome.status == "PASS":
        aggregate.pass_instances += 1
        aggregate.pass_frames.add(frame_key)
        aggregate.record_instances_observed += outcome.record_instances
        aggregate.record_kinds.update(outcome.record_kinds)
    elif outcome.status == "STATIC_OPEN":
        aggregate.static_open_instances += 1
        aggregate.static_open_frames.add(frame_key)
        aggregate.static_open_reasons.update(outcome.blockers)
    elif outcome.status == "SCHEMA_NOT_APPLIED":
        aggregate.not_applied_instances += 1
        aggregate.not_applied_frames.add(frame_key)
        aggregate.not_applied_reasons.update(outcome.blockers)
    elif outcome.status == "MISMATCH":
        aggregate.mismatch_instances += 1
        aggregate.mismatch_frames.add(frame_key)
        aggregate.mismatch_points[(outcome.field_identity, outcome.reason)] += 1
    else:
        raise ValidationError(f"unexpected schema outcome: {outcome.status}")


def parse_capture_frame(
    data: bytes,
    direction: str,
    frame_key: str,
    file_key: str,
    id_to_name: Mapping[int, str],
    plans: Mapping[tuple[str, str], SchemaPlan],
    aggregates: Mapping[tuple[str, str], MessageAggregate],
    counts: RunCounts,
) -> None:
    if len(data) < 12:
        counts.block_errors["TRUNCATED_OUTER_BASE"] += 1
        return
    if data[0] != 0x12:
        counts.block_errors["OUTER_ID_TAG"] += 1
        return
    outer_id = int.from_bytes(data[1:3], "little")
    outer_name = id_to_name.get(outer_id)
    if outer_name is None:
        counts.unknown_message_id_instances += 1
        counts.block_errors["UNKNOWN_OUTER_ID"] += 1
        return
    if data[3] != 0x14 or data[8] != 0x08 or data[10] != 0x0B:
        counts.block_errors["OUTER_BASE_STRUCTURE"] += 1
        return
    counts.outer_instances += 1
    outer_result = parse_schema(data, 3, plans[(outer_name, direction)])
    record_outcome(aggregates[(outer_name, direction)], frame_key, file_key, outer_result)

    outer_mask = data[11]
    if not outer_mask & 0x02:
        return
    if len(data) < 15 or data[12] != 0x12:
        counts.block_errors["VITAL_COUNT_STRUCTURE"] += 1
        return
    vital_count = int.from_bytes(data[13:15], "little")
    counts.nested_declared_instances += vital_count
    position = 15
    stopped = False
    for vital_index in range(vital_count):
        if (
            position + 5 > len(data)
            or data[position] != 0x12
            or data[position + 3] != 0x0B
        ):
            counts.block_errors["VITAL_WRAPPER_STRUCTURE"] += 1
            counts.nested_unresolved_after_mismatch += vital_count - vital_index
            stopped = True
            break
        vital_id = int.from_bytes(data[position + 1 : position + 3], "little")
        vital_name = id_to_name.get(vital_id)
        if vital_name is None:
            counts.unknown_message_id_instances += 1
            counts.nested_unresolved_after_mismatch += vital_count - vital_index
            stopped = True
            break
        position += 5
        counts.nested_reached_instances += 1
        result = parse_schema(data, position, plans[(vital_name, direction)])
        record_outcome(aggregates[(vital_name, direction)], frame_key, file_key, result)
        if result.status == "PASS":
            position = result.end
            continue
        trailing = vital_count - vital_index - 1
        if result.status == "STATIC_OPEN":
            counts.nested_unresolved_after_static_open += trailing
        elif result.status == "SCHEMA_NOT_APPLIED":
            counts.nested_unresolved_after_not_applied += trailing
        else:
            counts.nested_unresolved_after_mismatch += trailing
        stopped = True
        break
    if stopped:
        return
    remaining = data[position:]
    if not remaining:
        counts.no_runtime_tail_frames += 1
    elif outer_id == RUNTIME_RESPONSE_ID and remaining == bytes((0x0B, 0x00)):
        counts.runtime_zero_tail_frames += 1
    else:
        counts.framing_unresolved_frames += 1


def validate_parser_controls(plans: Mapping[tuple[str, str], SchemaPlan]) -> None:
    fields = (
        EffectiveField(1, "V1:1", "1", "1", "SUBCALL:0x006EC050", "N/A", "+0x14", "ALWAYS", "", "", "TEST", "TESTKEY1"),
        EffectiveField(2, "V1:2", "2", "2", "0x12", "2", "COUNT", "ALWAYS", "", "", "TEST", "TESTKEY2"),
        EffectiveField(3, "V1:3", "3", "3", "SUBCALL:0x006EB960", "N/A", "RECORD", "ALWAYS", "", "", "TEST", "TESTKEY3"),
        EffectiveField(4, "V1:4->WIRE:1", "4", "1", "0x08", "1", "RECORD+0x16", "ALWAYS", "", "", "TEST", "TESTKEY4"),
        EffectiveField(5, "V1:9->WIRE:6", "9", "6", "0x14", "4", "RECORD+0x04", "kind==2", "", "", "TEST", "TESTKEY5"),
        EffectiveField(6, "V1:10->WIRE:7", "10", "7", "0x14", "4", "RECORD+0x08", "kind==2", "", "", "TEST", "TESTKEY6"),
        EffectiveField(7, "V1:11->WIRE:6_ALT", "11", "6_ALT", "0x14", "4", "RECORD+0x0C", "kind==1", "", "", "TEST", "TESTKEY7"),
    )
    plan = SchemaPlan("CTracePathVital", "W", "TEST", "APPLICABLE", (), fields)
    empty = bytes((0x12, 0, 0))
    outcome = parse_schema(empty, 0, plan)
    if outcome.status != "PASS" or outcome.end != len(empty):
        raise ValidationError("CTrace zero-record control failed")
    kind_one = bytes((0x12, 1, 0, 0x08, 1, 0x14, 1, 2, 3, 4))
    outcome = parse_schema(kind_one, 0, plan)
    if outcome.status != "PASS" or outcome.end != len(kind_one):
        raise ValidationError("6_ALT kind-one control failed")
    kind_two = bytes((0x12, 1, 0, 0x08, 2, 0x14, 1, 2, 3, 4, 0x14, 5, 6, 7, 8))
    outcome = parse_schema(kind_two, 0, plan)
    if outcome.status != "PASS" or outcome.end != len(kind_two):
        raise ValidationError("gapped kind-two control failed")
    mutated = bytearray(kind_two)
    mutated[10] = 0x12
    outcome = parse_schema(bytes(mutated), 0, plan)
    if (outcome.status, outcome.field_identity, outcome.reason) != (
        "MISMATCH",
        "V1:10->WIRE:7",
        "TAG",
    ):
        raise ValidationError("declared field-identity mutation control failed")
    if plans[("CTracePathVital", "W")].state != "APPLICABLE":
        raise ValidationError("live CTrace W compatibility control failed")


def run_capture_validation(
    canonical_inputs: Sequence[CaptureInput],
    id_to_name: Mapping[int, str],
    plans: Mapping[tuple[str, str], SchemaPlan],
) -> tuple[dict[tuple[str, str], MessageAggregate], RunCounts]:
    aggregates: dict[tuple[str, str], MessageAggregate] = defaultdict(MessageAggregate)
    counts = RunCounts()
    for item in canonical_inputs:
        if item.path.suffix.casefold() != ".txt":
            continue
        counts.capture_text_files += 1
        text = item.path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = extract_pc_blocks(text)
        counts.block_errors.update(errors)
        if blocks:
            counts.files_with_blocks.add(item.sha256)
        for ordinal, (kind, data) in enumerate(blocks, 1):
            if kind == "PC":
                direction = "R"
                counts.pc_blocks += 1
            else:
                direction = "W"
                counts.decompressed_blocks += 1
            frame_key = f"{item.sha256}:{ordinal}"
            parse_capture_frame(
                data,
                direction,
                frame_key,
                item.sha256,
                id_to_name,
                plans,
                aggregates,
                counts,
            )
    return aggregates, counts


def merge_aggregates(
    first: Mapping[tuple[str, str], MessageAggregate],
    second: Mapping[tuple[str, str], MessageAggregate],
) -> dict[tuple[str, str], MessageAggregate]:
    result: dict[tuple[str, str], MessageAggregate] = {}
    for key in set(first) | set(second):
        left = first.get(key, MessageAggregate())
        right = second.get(key, MessageAggregate())
        merged = MessageAggregate(
            observed_instances=left.observed_instances + right.observed_instances,
            pass_instances=left.pass_instances + right.pass_instances,
            static_open_instances=left.static_open_instances + right.static_open_instances,
            not_applied_instances=left.not_applied_instances + right.not_applied_instances,
            mismatch_instances=left.mismatch_instances + right.mismatch_instances,
            observed_frames=left.observed_frames | right.observed_frames,
            pass_frames=left.pass_frames | right.pass_frames,
            static_open_frames=left.static_open_frames | right.static_open_frames,
            not_applied_frames=left.not_applied_frames | right.not_applied_frames,
            mismatch_frames=left.mismatch_frames | right.mismatch_frames,
            capture_files=left.capture_files | right.capture_files,
            mismatch_points=left.mismatch_points + right.mismatch_points,
            static_open_reasons=left.static_open_reasons + right.static_open_reasons,
            not_applied_reasons=left.not_applied_reasons + right.not_applied_reasons,
            record_instances_observed=(
                left.record_instances_observed + right.record_instances_observed
            ),
            record_kinds=left.record_kinds + right.record_kinds,
        )
        result[key] = merged
    return result


def merge_run_counts(first: RunCounts, second: RunCounts) -> RunCounts:
    return RunCounts(
        capture_text_files=first.capture_text_files + second.capture_text_files,
        files_with_blocks=first.files_with_blocks | second.files_with_blocks,
        pc_blocks=first.pc_blocks + second.pc_blocks,
        decompressed_blocks=first.decompressed_blocks + second.decompressed_blocks,
        block_errors=first.block_errors + second.block_errors,
        outer_instances=first.outer_instances + second.outer_instances,
        nested_declared_instances=(
            first.nested_declared_instances + second.nested_declared_instances
        ),
        nested_reached_instances=(
            first.nested_reached_instances + second.nested_reached_instances
        ),
        nested_unresolved_after_static_open=(
            first.nested_unresolved_after_static_open
            + second.nested_unresolved_after_static_open
        ),
        nested_unresolved_after_not_applied=(
            first.nested_unresolved_after_not_applied
            + second.nested_unresolved_after_not_applied
        ),
        nested_unresolved_after_mismatch=(
            first.nested_unresolved_after_mismatch
            + second.nested_unresolved_after_mismatch
        ),
        unknown_message_id_instances=(
            first.unknown_message_id_instances + second.unknown_message_id_instances
        ),
        no_runtime_tail_frames=(
            first.no_runtime_tail_frames + second.no_runtime_tail_frames
        ),
        runtime_zero_tail_frames=(
            first.runtime_zero_tail_frames + second.runtime_zero_tail_frames
        ),
        framing_unresolved_frames=(
            first.framing_unresolved_frames + second.framing_unresolved_frames
        ),
    )


def outcome_counts(
    aggregates: Mapping[tuple[str, str], MessageAggregate], counts: RunCounts
) -> dict[str, int]:
    return {
        "unique_text_files": counts.capture_text_files,
        "files_with_blocks": len(counts.files_with_blocks),
        "pc_blocks": counts.pc_blocks,
        "decompressed_blocks": counts.decompressed_blocks,
        "block_errors": sum(counts.block_errors.values()),
        "outer_instances": counts.outer_instances,
        "nested_declared": counts.nested_declared_instances,
        "nested_reached": counts.nested_reached_instances,
        "nested_unresolved_static_open": counts.nested_unresolved_after_static_open,
        "nested_unresolved_not_applied": counts.nested_unresolved_after_not_applied,
        "nested_unresolved_mismatch": counts.nested_unresolved_after_mismatch,
        "unknown_message_ids": counts.unknown_message_id_instances,
        "parse_success": sum(value.pass_instances for value in aggregates.values()),
        "static_open": sum(value.static_open_instances for value in aggregates.values()),
        "schema_not_applied": sum(
            value.not_applied_instances for value in aggregates.values()
        ),
        "mismatch": sum(value.mismatch_instances for value in aggregates.values()),
        "observed_rows": sum(value.observed_instances > 0 for value in aggregates.values()),
        "no_runtime_tail": counts.no_runtime_tail_frames,
        "runtime_zero_tail": counts.runtime_zero_tail_frames,
        "framing_unresolved": counts.framing_unresolved_frames,
    }


def measured_mismatch_points(
    aggregates: Mapping[tuple[str, str], MessageAggregate]
) -> dict[tuple[str, str, str, str], int]:
    return {
        (message, direction, identity, reason): count
        for (message, direction), aggregate in aggregates.items()
        for (identity, reason), count in aggregate.mismatch_points.items()
    }


def validate_ctrace_capture_boundary(
    aggregates: Mapping[tuple[str, str], MessageAggregate]
) -> None:
    reader = aggregates.get(("CTracePathVital", "R"), MessageAggregate())
    if (
        reader.observed_instances,
        reader.pass_instances,
        reader.static_open_instances,
        reader.not_applied_instances,
        reader.mismatch_instances,
        reader.record_instances_observed,
        dict(reader.record_kinds),
    ) != (1, 1, 0, 0, 0, 0, {}):
        raise ValidationError("CTrace zero-record CAPTURE boundary changed")


def counter_text(counter: Counter[str]) -> str:
    return " | ".join(f"{reason}:{count}" for reason, count in sorted(counter.items())) or "NONE"


def point_text(counter: Counter[tuple[str, str]]) -> str:
    return " | ".join(
        f"{identity}~{reason}~{count}"
        for (identity, reason), count in sorted(counter.items())
    ) or "NONE"


def aggregate_status(aggregate: MessageAggregate) -> str:
    if aggregate.mismatch_instances:
        return "MISMATCH"
    if aggregate.not_applied_instances:
        return "SCHEMA_NOT_APPLIED"
    if aggregate.static_open_instances:
        return "STATIC_OPEN"
    return "VALIDATED"


def record_branch_coverage(message: str, aggregate: MessageAggregate) -> str:
    if message != "CTracePathVital":
        return "N/A"
    if not aggregate.record_kinds:
        return "NONE"
    return " | ".join(
        f"KIND_{kind}:{count}" for kind, count in sorted(aggregate.record_kinds.items())
    )


def build_outputs(
    aggregates: Mapping[tuple[str, str], MessageAggregate],
    baseline_aggregates: Mapping[tuple[str, str], MessageAggregate],
    new_aggregates: Mapping[tuple[str, str], MessageAggregate],
    counts: RunCounts,
    duplicate_aggregates: Mapping[tuple[str, str], MessageAggregate],
    duplicate_counts: RunCounts,
    plans: Mapping[tuple[str, str], SchemaPlan],
    corpus_digest: str,
    all_inputs: Sequence[CaptureInput],
    canonical_inputs: Sequence[CaptureInput],
    input_hashes: Mapping[str, str],
    overlay_counts: Mapping[str, int],
) -> tuple[str, str]:
    headers = [
        "validation_key",
        "message",
        "direction(W/R)",
        "schema_variant",
        "effective_schema_key",
        "observed_frames",
        "observed_instances",
        "baseline_observed_instances",
        "new_observed_instances",
        "parse_success_frames",
        "parse_success_instances",
        "baseline_parse_success_instances",
        "new_parse_success_instances",
        "static_open_frames",
        "static_open_instances",
        "baseline_static_open_instances",
        "new_static_open_instances",
        "static_open_reason_count",
        "schema_not_applied_frames",
        "schema_not_applied_instances",
        "baseline_schema_not_applied_instances",
        "new_schema_not_applied_instances",
        "schema_not_applied_reason_count",
        "mismatch_frames",
        "mismatch_instances",
        "baseline_mismatch_instances",
        "new_mismatch_instances",
        "mismatch_field_identity_reason_count",
        "record_instances_observed",
        "record_branch_coverage",
        "capture_file_count",
        "status",
        "content_dedup_scope",
        "source",
    ]
    rows: list[list[str]] = []
    for (message, direction), aggregate in sorted(aggregates.items()):
        if not aggregate.observed_instances:
            continue
        plan = plans[(message, direction)]
        plan_key = schema_plan_key(plan)
        baseline = baseline_aggregates.get((message, direction), MessageAggregate())
        fresh = new_aggregates.get((message, direction), MessageAggregate())
        key = sha256_text(
            "\x1f".join((message, direction, plan.variant, plan_key, corpus_digest))
        )
        rows.append(
            [
                key,
                message,
                direction,
                plan.variant,
                plan_key,
                str(len(aggregate.observed_frames)),
                str(aggregate.observed_instances),
                str(baseline.observed_instances),
                str(fresh.observed_instances),
                str(len(aggregate.pass_frames)),
                str(aggregate.pass_instances),
                str(baseline.pass_instances),
                str(fresh.pass_instances),
                str(len(aggregate.static_open_frames)),
                str(aggregate.static_open_instances),
                str(baseline.static_open_instances),
                str(fresh.static_open_instances),
                counter_text(aggregate.static_open_reasons),
                str(len(aggregate.not_applied_frames)),
                str(aggregate.not_applied_instances),
                str(baseline.not_applied_instances),
                str(fresh.not_applied_instances),
                counter_text(aggregate.not_applied_reasons),
                str(len(aggregate.mismatch_frames)),
                str(aggregate.mismatch_instances),
                str(baseline.mismatch_instances),
                str(fresh.mismatch_instances),
                point_text(aggregate.mismatch_points),
                str(aggregate.record_instances_observed),
                record_branch_coverage(message, aggregate),
                str(len(aggregate.capture_files)),
                aggregate_status(aggregate),
                "FULL_FILE_SHA256_CANONICAL_PATH_PER_CONTENT",
                SOURCE,
            ]
        )
    output_tsv = tsv_text(headers, rows)
    validate_output_tsv(
        output_tsv, aggregates, baseline_aggregates, new_aggregates, plans, corpus_digest
    )

    values = outcome_counts(aggregates, counts)
    duplicate_values = outcome_counts(duplicate_aggregates, duplicate_counts)
    for prefix, subset in (
        ("baseline", baseline_aggregates),
        ("new", new_aggregates),
    ):
        values[f"{prefix}_parse_success"] = sum(
            aggregate.pass_instances for aggregate in subset.values()
        )
        values[f"{prefix}_static_open"] = sum(
            aggregate.static_open_instances for aggregate in subset.values()
        )
        values[f"{prefix}_schema_not_applied"] = sum(
            aggregate.not_applied_instances for aggregate in subset.values()
        )
        values[f"{prefix}_mismatch"] = sum(
            aggregate.mismatch_instances for aggregate in subset.values()
        )
    mismatch_points = measured_mismatch_points(aggregates)
    mismatch_locations = {
        (message, direction, identity)
        for message, direction, identity, _reason in mismatch_points
    }
    v1_total = sum(V1_SCHEMA_CONTENT_DEDUP_COUNTS.values())
    effective_total = sum(
        values[name]
        for name in ("parse_success", "static_open", "schema_not_applied", "mismatch")
    )
    pass_gain = values["parse_success"] - V1_SCHEMA_CONTENT_DEDUP_COUNTS["parse_success"]
    not_applied_gain = (
        values["schema_not_applied"]
        - V1_SCHEMA_CONTENT_DEDUP_COUNTS["schema_not_applied"]
    )
    mismatch_gain = values["mismatch"] - V1_SCHEMA_CONTENT_DEDUP_COUNTS["mismatch"]
    formerly_open = (
        V1_SCHEMA_CONTENT_DEDUP_COUNTS["static_open"] - values["static_open"]
    )
    if (
        v1_total != effective_total
        or formerly_open != pass_gain + not_applied_gain + mismatch_gain
        or min(pass_gain, not_applied_gain, mismatch_gain, formerly_open) < 0
    ):
        raise ValidationError("V1/effective reconciliation invariant failed")
    plan_census = Counter(plan.state for plan in plans.values())
    lines: list[str] = []
    if mismatch_points:
        lines.extend(
            [
                "# 🔴 A5 V2 พบ static/capture mismatch",
                "",
                "[MEASURED][CAPTURE] ตัวเลขทั้งหมดด้านล่างมาจาก corpus และ effective schema ที่ pin hash ไว้; ข้อเท็จจริง CAPTURE ไม่ถูกเขียนทับเข้า IMAGE rows",
                "",
                f"พบ **{len(mismatch_locations)} field locations / {len(mismatch_points)} field+reason points / {values['mismatch']} instances** หลังใช้ effective V2 A2 กับ capture ที่ de-duplicate ตาม SHA-256 แล้ว ตาราง IMAGE ไม่ถูกแก้ให้เข้ากับข้อมูลสายจริง",
                "",
                "| message | dir | declared field identity | reason | baseline | new | total |",
                "|---|:---:|---|---|---:|---:|---:|",
            ]
        )
        for (message, direction, identity, reason), count in sorted(
            mismatch_points.items()
        ):
            baseline_count = baseline_aggregates.get(
                (message, direction), MessageAggregate()
            ).mismatch_points[(identity, reason)]
            new_count = new_aggregates.get(
                (message, direction), MessageAggregate()
            ).mismatch_points[(identity, reason)]
            lines.append(
                f"| `{message}` | {direction} | `{identity}` | `{reason}` | {baseline_count} | {new_count} | {count} |"
            )
        lines.extend(
            [
                "",
                "`V1:n->WIRE:m` รักษาทั้งหมายเลขแถว field เดิมและ wire-order ที่ overlay ประกาศ; ไม่มีการ renumber หรือสลับ field ให้เข้ากับ capture",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "# PF V2 effective field validation",
                "",
                "[MEASURED][CAPTURE] ตัวเลขทั้งหมดด้านล่างมาจาก corpus และ effective schema ที่ pin hash ไว้; ข้อเท็จจริง CAPTURE ไม่ถูกเขียนทับเข้า IMAGE rows",
                "",
            ]
        )
    lines.extend(
        [
            "ผลนี้เป็น aggregate `source=CAPTURE` เท่านั้น ไม่ส่งออก payload, field value, capture path หรือ hexdump",
            "",
            "## Effective schema result",
            "",
            f"- parse success: {values['parse_success']} instances",
            f"- IMAGE static-open: {values['static_open']} instances",
            f"- schema not safely applicable: {values['schema_not_applied']} instances",
            f"- mismatch: {values['mismatch']} instances / {len(mismatch_locations)} field locations / {len(mismatch_points)} field+reason points",
            f"- baseline canonical claims: pass={values['baseline_parse_success']}; static-open={values['baseline_static_open']}; schema-not-applied={values['baseline_schema_not_applied']}; mismatch={values['baseline_mismatch']}",
            f"- new canonical claims: pass={values['new_parse_success']}; static-open={values['new_static_open']}; schema-not-applied={values['new_schema_not_applied']}; mismatch={values['new_mismatch']}",
            f"- reconciliation invariant: V1-schema content-dedup total {v1_total} = effective {values['parse_success']} pass + {values['static_open']} static-open + {values['schema_not_applied']} schema-not-applied + {values['mismatch']} mismatch; exactly {formerly_open} formerly-open instances became {pass_gain} pass + {not_applied_gain} schema-not-applied + {mismatch_gain} mismatch, with no instance added or dropped.",
            f"- observed message/direction rows emitted: {values['observed_rows']} (unobserved 519 x 2 rows are not copied)",
            f"- full effective plan census: APPLICABLE={plan_census['APPLICABLE']}; STATIC_OPEN={plan_census['STATIC_OPEN']}; SCHEMA_NOT_APPLIED={plan_census['SCHEMA_NOT_APPLIED']}",
            "",
            "## Capture de-duplication",
            "",
            f"- inventoried paths: {len(all_inputs)} ({sum(item.size for item in all_inputs)} bytes)",
            f"- unique full-file SHA-256 contents hashed and de-duplicated at one canonical path each: {len(canonical_inputs)}",
            "- canonical claims split without overlap: baseline=1189 unique contents; new=320 unique contents absent from baseline",
            f"- exact-content duplicate paths rejected before claim counting: {len(all_inputs) - len(canonical_inputs)}",
            f"- duplicate-rejected message instances (audit only, never added to claims): {sum(duplicate_values[name] for name in ('parse_success', 'static_open', 'schema_not_applied', 'mismatch'))} [pass={duplicate_values['parse_success']}; static-open={duplicate_values['static_open']}; schema-not-applied={duplicate_values['schema_not_applied']}; mismatch={duplicate_values['mismatch']}]",
            f"- canonical corpus inventory digest: `{corpus_digest}`",
            f"- canonical non-text contents skipped by the packet-text parser: {len(canonical_inputs) - values['unique_text_files']}",
            f"- unique text contents inspected: {values['unique_text_files']}; text contents with no recognized packet blocks and therefore no frames: {values['unique_text_files'] - values['files_with_blocks']}; text contents contributing packet blocks: {values['files_with_blocks']}",
            f"- PC blocks: {values['pc_blocks']}; DECOMPRESSED blocks: {values['decompressed_blocks']}",
            "- direction mapping is unchanged: `PC=R`, `DECOMPRESSED=W`.",
            f"- block/envelope errors: {values['block_errors']}; unknown message IDs: {values['unknown_message_ids']}",
            "",
            "## Nested framing",
            "",
            f"- declared/reached nested instances: {values['nested_declared']}/{values['nested_reached']}",
            f"- trailing instances deliberately unresolved after static-open / validator blocker / mismatch: {values['nested_unresolved_static_open']} / {values['nested_unresolved_not_applied']} / {values['nested_unresolved_mismatch']}",
            f"- complete collections with no tail / exact runtime zero-mask / other framing unresolved: {values['no_runtime_tail']} / {values['runtime_zero_tail']} / {values['framing_unresolved']}",
            "",
            "## Fail-closed compatibility boundary",
            "",
            "- `SUBCALL` is skipped only when later A2 primitives explicitly flatten the same target in the original/current IMAGE trace. A referenced-but-unflattened nested serializer is `SCHEMA_NOT_APPLIED`, never a synthetic PASS.",
            "- `CTracePathVital` retains base trace sequence, declared gaps, `6_ALT`, and `kind==1/2` gates. Field identities are not normalized.",
            "- CAPTURE observed `CTracePathVital R` once with a valid count field and zero records: message/container pass=1, record_instances_observed=0, record_branch_coverage=NONE. This does **not** validate any record-layout or kind branch.",
            "- `ItemAttr` base/derived candidate schemas remain separate inputs. No canonical candidate is chosen or merged; an observed ItemAttr frame would be fail-closed.",
            "- Static-open, validator compatibility blockers, and actual byte/tag mismatch are counted separately.",
            "",
            "## Effective A2 overlay bookkeeping",
            "",
            f"- V1 rows: {overlay_counts['base_rows']}; effective canonical rows: {overlay_counts['effective_rows']}",
            f"- string CHANGED: {overlay_counts['string_changed']}; other CHANGED: {overlay_counts['generic_changed']}",
            f"- non-wire removals: {overlay_counts['generic_removed']}; wrong-slot removals: {overlay_counts['slot_removed']}",
            f"- slot34 canonical additions retained: {overlay_counts['slot_added_canonical']}; later overlay removals: {overlay_counts['slot_overlay_removed']}; ItemAttr candidate-only rows excluded from canonical: {overlay_counts['slot_candidates']}",
            "- unchanged IMAGE rows are consumed in memory but are not copied to a new A2 output.",
            "",
            "## Exact input bindings",
            "",
        ]
    )
    for name in INPUT_NAMES:
        lines.append(f"- `{name}` SHA-256: `{input_hashes[name]}`")
    lines.extend(
        [
            f"- `GameClient.local.bin` size/SHA-256: {EXPECTED_IMAGE_SIZE} / `{EXPECTED_IMAGE_SHA256}`",
            "",
            "## Reproduction",
            "",
            "Run `py -3 -B pf_validate_v2_effective_capture.py --check` to verify the frozen red report byte-for-byte. Exit 0 means artifact integrity/reproduction passed; it does **not** mean schema conformance because the frozen result contains mismatches. Use `--check --fail-on-mismatch` when a downstream gate must exit nonzero for any observed mismatch.",
            "",
        ]
    )
    output_md = "\n".join(lines)
    if RAW_BYTE_RUN_RE.search(output_tsv) or RAW_BYTE_RUN_RE.search(output_md):
        raise ValidationError("raw capture-byte output guard fired")
    return output_tsv, output_md


def validate_output_tsv(
    text: str,
    aggregates: Mapping[tuple[str, str], MessageAggregate],
    baseline_aggregates: Mapping[tuple[str, str], MessageAggregate],
    new_aggregates: Mapping[tuple[str, str], MessageAggregate],
    plans: Mapping[tuple[str, str], SchemaPlan],
    corpus_digest: str,
) -> None:
    rows = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    if not rows:
        raise ValidationError("V2 validation output is empty")
    if Counter(row["source"] for row in rows) != Counter({SOURCE: len(rows)}):
        raise ValidationError("V2 validation output violates source=CAPTURE")
    if any(row["content_dedup_scope"] != "FULL_FILE_SHA256_CANONICAL_PATH_PER_CONTENT" for row in rows):
        raise ValidationError("V2 validation dedup scope changed")
    keys = [row["validation_key"] for row in rows]
    semantic = [(row["message"], row["direction(W/R)"]) for row in rows]
    if len(set(keys)) != len(keys) or len(set(semantic)) != len(semantic):
        raise ValidationError("duplicate V2 validation output key")
    if len({tuple(row.items()) for row in rows}) != len(rows):
        raise ValidationError("exact duplicate V2 validation output row")
    expected_semantic = {
        key for key, aggregate in aggregates.items() if aggregate.observed_instances
    }
    if set(semantic) != expected_semantic:
        raise ValidationError("V2 validation output observed-row set changed")
    numeric_columns = (
        "observed_frames",
        "observed_instances",
        "baseline_observed_instances",
        "new_observed_instances",
        "parse_success_frames",
        "parse_success_instances",
        "baseline_parse_success_instances",
        "new_parse_success_instances",
        "static_open_frames",
        "static_open_instances",
        "baseline_static_open_instances",
        "new_static_open_instances",
        "schema_not_applied_frames",
        "schema_not_applied_instances",
        "baseline_schema_not_applied_instances",
        "new_schema_not_applied_instances",
        "mismatch_frames",
        "mismatch_instances",
        "baseline_mismatch_instances",
        "new_mismatch_instances",
        "record_instances_observed",
        "capture_file_count",
    )
    for row in rows:
        semantic_key = (row["message"], row["direction(W/R)"])
        aggregate = aggregates[semantic_key]
        baseline = baseline_aggregates.get(semantic_key, MessageAggregate())
        fresh = new_aggregates.get(semantic_key, MessageAggregate())
        values = {name: int(row[name]) for name in numeric_columns}
        if values["observed_instances"] != (
            values["parse_success_instances"]
            + values["static_open_instances"]
            + values["schema_not_applied_instances"]
            + values["mismatch_instances"]
        ):
            raise ValidationError("V2 validation instance accounting differs")
        expected_values = {
            "observed_frames": len(aggregate.observed_frames),
            "observed_instances": aggregate.observed_instances,
            "baseline_observed_instances": baseline.observed_instances,
            "new_observed_instances": fresh.observed_instances,
            "parse_success_frames": len(aggregate.pass_frames),
            "parse_success_instances": aggregate.pass_instances,
            "baseline_parse_success_instances": baseline.pass_instances,
            "new_parse_success_instances": fresh.pass_instances,
            "static_open_frames": len(aggregate.static_open_frames),
            "static_open_instances": aggregate.static_open_instances,
            "baseline_static_open_instances": baseline.static_open_instances,
            "new_static_open_instances": fresh.static_open_instances,
            "schema_not_applied_frames": len(aggregate.not_applied_frames),
            "schema_not_applied_instances": aggregate.not_applied_instances,
            "baseline_schema_not_applied_instances": baseline.not_applied_instances,
            "new_schema_not_applied_instances": fresh.not_applied_instances,
            "mismatch_frames": len(aggregate.mismatch_frames),
            "mismatch_instances": aggregate.mismatch_instances,
            "baseline_mismatch_instances": baseline.mismatch_instances,
            "new_mismatch_instances": fresh.mismatch_instances,
            "record_instances_observed": aggregate.record_instances_observed,
            "capture_file_count": len(aggregate.capture_files),
        }
        if values != expected_values:
            raise ValidationError("V2 validation row differs from aggregate")
        for total_name, baseline_name, new_name in (
            ("observed_instances", "baseline_observed_instances", "new_observed_instances"),
            ("parse_success_instances", "baseline_parse_success_instances", "new_parse_success_instances"),
            ("static_open_instances", "baseline_static_open_instances", "new_static_open_instances"),
            ("schema_not_applied_instances", "baseline_schema_not_applied_instances", "new_schema_not_applied_instances"),
            ("mismatch_instances", "baseline_mismatch_instances", "new_mismatch_instances"),
        ):
            if values[total_name] != values[baseline_name] + values[new_name]:
                raise ValidationError("baseline/new claim split does not balance")
        if row["status"] != aggregate_status(aggregate):
            raise ValidationError("V2 validation status differs from aggregate")
        if row["mismatch_field_identity_reason_count"] != point_text(
            aggregate.mismatch_points
        ):
            raise ValidationError("V2 mismatch detail differs from aggregate")
        if row["static_open_reason_count"] != counter_text(
            aggregate.static_open_reasons
        ):
            raise ValidationError("V2 static-open detail differs from aggregate")
        if row["schema_not_applied_reason_count"] != counter_text(
            aggregate.not_applied_reasons
        ):
            raise ValidationError("V2 blocker detail differs from aggregate")
        if row["record_branch_coverage"] != record_branch_coverage(
            row["message"], aggregate
        ):
            raise ValidationError("V2 record-branch coverage differs from aggregate")
        plan_key = schema_plan_key(plans[semantic_key])
        if row["effective_schema_key"] != plan_key:
            raise ValidationError("effective schema key changed")
        expected_key = sha256_text(
            "\x1f".join(
                (
                    row["message"],
                    row["direction(W/R)"],
                    row["schema_variant"],
                    plan_key,
                    corpus_digest,
                )
            )
        )
        if row["validation_key"] != expected_key:
            raise ValidationError("V2 validation key changed")
    if RAW_BYTE_RUN_RE.search(text):
        raise ValidationError("raw capture-byte TSV guard fired")


def validate_output_mutations(
    output_tsv: str,
    aggregates: Mapping[tuple[str, str], MessageAggregate],
    baseline_aggregates: Mapping[tuple[str, str], MessageAggregate],
    new_aggregates: Mapping[tuple[str, str], MessageAggregate],
    plans: Mapping[tuple[str, str], SchemaPlan],
    corpus_digest: str,
) -> None:
    rows = list(csv.DictReader(io.StringIO(output_tsv), delimiter="\t"))
    headers = list(rows[0])
    mutations = (
        (0, "source", "IMAGE"),
        (0, "validation_key", "0" * 64),
        (0, "effective_schema_key", "0" * 64),
        (0, "observed_instances", str(int(rows[0]["observed_instances"]) + 1)),
        (0, "status", "VALIDATED" if rows[0]["status"] != "VALIDATED" else "MISMATCH"),
        (0, "content_dedup_scope", "PATHS_WITH_DUPLICATES"),
    )
    for row_index, column, replacement in mutations:
        mutated = [dict(row) for row in rows]
        mutated[row_index][column] = replacement
        text = tsv_text(headers, [[row[name] for name in headers] for row in mutated])
        try:
            validate_output_tsv(
                text,
                aggregates,
                baseline_aggregates,
                new_aggregates,
                plans,
                corpus_digest,
            )
        except (ValidationError, ValueError):
            pass
        else:
            raise ValidationError(f"output mutation was accepted: {column}")


def atomic_publish(outputs: Mapping[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, text in outputs.items():
            fd, raw_temp = tempfile.mkstemp(
                prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game-client",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "GameClient",
    )
    parser.add_argument(
        "--external", type=Path, default=Path(__file__).resolve().parent
    )
    parser.add_argument("--preview-unpinned", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--fail-on-mismatch",
        action="store_true",
        help="with --check, return nonzero when the frozen capture result has mismatches",
    )
    args = parser.parse_args()
    if args.preview_unpinned and args.check:
        raise ValidationError("--preview-unpinned and --check are mutually exclusive")
    if args.fail_on_mismatch and not args.check:
        raise ValidationError("--fail-on-mismatch requires --check")
    external = args.external.resolve()
    game_client = args.game_client.resolve()
    image_path = game_client / "GameClient.local.bin"
    if image_path.stat().st_size != EXPECTED_IMAGE_SIZE or sha256_file(image_path) != EXPECTED_IMAGE_SHA256:
        raise ValidationError("pinned client image changed")
    input_hashes_before = verify_pinned_inputs(external, args.preview_unpinned)

    registry_rows, effective, candidates, overlay_counts = apply_effective_overlays(external)
    validate_ctrace_container_contract(external)
    id_to_name, plans = build_schema_plans(registry_rows, effective, candidates)
    plan_census = dict(Counter(plan.state for plan in plans.values()))
    if not args.preview_unpinned:
        if overlay_counts != EXPECTED_OVERLAY_COUNTS:
            raise ValidationError(f"effective overlay census changed: {overlay_counts}")
        if plan_census != EXPECTED_PLAN_CENSUS:
            raise ValidationError(f"effective schema-plan census changed: {plan_census}")
    validate_parser_controls(plans)
    all_inputs, canonical_inputs, baseline_hashes, corpus_digest = load_capture_inventory(
        game_client,
        external / "PF_INPUT_INVENTORY.tsv",
        external / "PF_CAPTURE_DELTA_20260830.inventory.tsv",
    )
    if corpus_digest != EXPECTED_CORPUS_DIGEST:
        raise ValidationError("canonical capture-corpus digest changed")
    baseline_inputs = [
        item for item in canonical_inputs if item.sha256 in baseline_hashes
    ]
    new_inputs = [item for item in canonical_inputs if item.sha256 not in baseline_hashes]
    if len(baseline_inputs) != 1_189 or len(new_inputs) != 320:
        raise ValidationError("baseline/new canonical partition changed")
    baseline_aggregates, baseline_counts = run_capture_validation(
        baseline_inputs, id_to_name, plans
    )
    new_aggregates, new_counts = run_capture_validation(new_inputs, id_to_name, plans)
    canonical_paths = {item.relative_path.casefold() for item in canonical_inputs}
    duplicate_inputs = [
        item for item in all_inputs if item.relative_path.casefold() not in canonical_paths
    ]
    if len(duplicate_inputs) != EXPECTED_DUPLICATE_PATHS:
        raise ValidationError("duplicate-input audit partition changed")
    duplicate_aggregates, duplicate_counts = run_capture_validation(
        duplicate_inputs, id_to_name, plans
    )
    aggregates = merge_aggregates(baseline_aggregates, new_aggregates)
    counts = merge_run_counts(baseline_counts, new_counts)
    validate_ctrace_capture_boundary(aggregates)
    values = outcome_counts(aggregates, counts)
    baseline_values = outcome_counts(baseline_aggregates, baseline_counts)
    new_values = outcome_counts(new_aggregates, new_counts)
    for prefix, subset in (("baseline", baseline_values), ("new", new_values)):
        for name in (
            "parse_success",
            "static_open",
            "schema_not_applied",
            "mismatch",
            "observed_rows",
            "pc_blocks",
            "decompressed_blocks",
        ):
            values[f"{prefix}_{name}"] = subset[name]
    duplicate_values = outcome_counts(duplicate_aggregates, duplicate_counts)
    for name in (
        "parse_success",
        "static_open",
        "schema_not_applied",
        "mismatch",
        "observed_rows",
        "pc_blocks",
        "decompressed_blocks",
    ):
        values[f"duplicate_rejected_{name}"] = duplicate_values[name]
    mismatch_points = measured_mismatch_points(aggregates)
    if EXPECTED_RUN_COUNTS and not args.preview_unpinned:
        if values != EXPECTED_RUN_COUNTS:
            raise ValidationError(f"V2 validation run census changed: {values}")
        if mismatch_points != EXPECTED_MISMATCH_POINTS:
            raise ValidationError(f"V2 mismatch-point census changed: {mismatch_points}")
    elif not args.preview_unpinned:
        raise ValidationError("run-count pins have not been frozen")

    output_tsv, output_md = build_outputs(
        aggregates,
        baseline_aggregates,
        new_aggregates,
        counts,
        duplicate_aggregates,
        duplicate_counts,
        plans,
        corpus_digest,
        all_inputs,
        canonical_inputs,
        input_hashes_before,
        overlay_counts,
    )
    validate_output_mutations(
        output_tsv,
        aggregates,
        baseline_aggregates,
        new_aggregates,
        plans,
        corpus_digest,
    )

    verify_capture_snapshot(game_client, all_inputs)
    input_hashes_after = verify_pinned_inputs(external, args.preview_unpinned)
    if input_hashes_after != input_hashes_before:
        raise ValidationError("pinned input changed during V2 validation")
    if image_path.stat().st_size != EXPECTED_IMAGE_SIZE or sha256_file(image_path) != EXPECTED_IMAGE_SHA256:
        raise ValidationError("client image changed during V2 validation")

    output_hashes = {
        OUTPUT_TSV: sha256_text(output_tsv),
        OUTPUT_MD: sha256_text(output_md),
    }
    if args.preview_unpinned:
        print("INPUT_SHA256=" + json.dumps(input_hashes_before, sort_keys=True))
        print("RUN_COUNTS=" + json.dumps(values, sort_keys=True))
        print(
            "MISMATCH_POINTS="
            + json.dumps(
                {"|".join(key): value for key, value in mismatch_points.items()},
                sort_keys=True,
            )
        )
        print("OUTPUT_SHA256=" + json.dumps(output_hashes, sort_keys=True))
        print("CORPUS_DIGEST=" + corpus_digest)
        print("OVERLAY_COUNTS=" + json.dumps(overlay_counts, sort_keys=True))
        print("PLAN_CENSUS=" + json.dumps(plan_census, sort_keys=True))
        return 0
    if output_hashes != EXPECTED_OUTPUT_SHA256:
        raise ValidationError(f"V2 validation output hash changed: {output_hashes}")
    destinations = {
        external / OUTPUT_TSV: output_tsv,
        external / OUTPUT_MD: output_md,
    }
    if args.check:
        for path, expected_text in destinations.items():
            if not path.exists() or path.read_text(encoding="utf-8") != expected_text:
                raise ValidationError(f"published output differs: {path.name}")
    else:
        atomic_publish(destinations)
    if args.fail_on_mismatch and values["mismatch"]:
        raise ValidationError(
            f"capture conformance failed: mismatch={values['mismatch']} "
            f"field_reason_points={len(mismatch_points)}"
        )
    print(
        "unique_contents=%d duplicate_paths=%d pass=%d static_open=%d "
        "schema_not_applied=%d mismatch=%d mismatch_points=%d"
        % (
            len(canonical_inputs),
            len(all_inputs) - len(canonical_inputs),
            values["parse_success"],
            values["static_open"],
            values["schema_not_applied"],
            values["mismatch"],
            len(mismatch_points),
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        raise SystemExit(f"ERROR: {exc}")
