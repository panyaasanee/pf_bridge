#!/usr/bin/env python3
"""Build and verify the immutable-local PF V2 checkpoint manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import tempfile
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = OUT_DIR / "PF_V2_MANIFEST.md"
IMAGE_PATH = OUT_DIR.parent.parent / "GameClient" / "GameClient.local.bin"
IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
V1_MANIFEST_SHA256 = "1b8a89ec20c528bd0eb5e69adc5add90bf6b8249f35fcfa7ce2ba23f80117f1c"
ALLOWED_SOURCES = {"IMAGE", "DUMP", "CAPTURE", "DATA"}
KEY_COLUMNS = ("delta_key", "dedup_key", "root_key", "status_key", "validation_key")

V1_PINS = {
    "PF_PROTOCOL_REGISTRY.tsv": "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d",
    "PF_PROTOCOL_REGISTRY.md": "ad2e6474fa3208c5ae757dae79a9e34f9a86afd6ec70a2a94c33167dcf014aa6",
    "PF_SERIALIZER_FIELDS.tsv": "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123",
    "PF_SERIALIZER_FIELDS.md": "1d069b20871b3081f013e88e128f78d790c1133838a565f6f11dab078859139a",
    "PF_TAG_CENSUS.tsv": "63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a",
    "pf_extract_protocol.py": "0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e",
    "PF_EXTERNAL_REPORT.md": "302aabd0882f3a06e2ff0efe322409feddac553b7f92e5e36611d3dc4c784a95",
    "PF_INPUT_INVENTORY.tsv": "729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1",
    "PF_INPUT_INVENTORY.md": "e5585c43cfee3fda85ab0c71ca28f83bc1951f09edab237b2486f4099c465d2c",
    "pf_inventory_inputs.py": "82b096c9d5fc137b3bfcdb4c7021b6fb0a5d40bcb02a562c7b4d101c7c821ec0",
    "PF_PROTOCOL_PRIORITY.tsv": "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55",
    "PF_PROTOCOL_PRIORITY.md": "d9653552db79911f0e2e3756dffb354e3197a39ee3baebdadb568cb08df8bb63",
    "pf_build_priority.py": "77c1e0effa3cdb9d89ab3b2f3e1ff40f598eecedae5a50367e5ba7e007fbaa5b",
    "PF_FIELD_VALIDATION.tsv": "080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3",
    "PF_FIELD_VALIDATION.md": "39c8fa913316b674636ae684cde2fc1b4d77a7bc1dd57016a1e4636e03636ff1",
    "pf_validate_capture_fields.py": "0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8",
    "PF_RUNTIME_CLASSMAP.tsv": "c53a6eaf23911765ebabd5e86ccaecf827ffdd88a1f514fc3f0f3ea2c3484985",
    "PF_RUNTIME_CLASSMAP.md": "9f2db6244a7c2e33f6f64bd480ae4f45a9659fbdf2452d45601a847d47dc54ea",
    "pf_extract_dump_rtti.py": "54b7bcfecf598007ea468309481f8e41ff64e4139026a0ee200984b03ad82a2b",
    "PF_DATA_EVIDENCE.tsv": "fbcd7bf14fd33c7340c6fd70f4a0aa5f1a6f7719c429335540383eab1ccf5b1f",
    "PF_DATA_EVIDENCE.md": "91b8d611f82d23dfd68009229c772aacc91a48d2b879fbe7d808016f7e1102b2",
    "pf_extract_data_evidence.py": "e8ae936403b548ed1b6a7791bca8f63b9abb8f4bc025c46ded24ce489fe9fe49",
    "PF_ERRATUM_TWO_IMAGES.md": "8785b715e69399162dbedd786c63ad914f87c1f1f4dab5ceb08cc73b60244a7e",
    "PF_DUMP_REQUEST.md": "5fce70adf071120f8c7cd9739ac52b835d5e4ee9c0f70995dc295fca8199201d",
    "PF_HANDOFF_V1.md": "a2affa88576c6d9dc5a8899c26581cfa92e3c4adc4a645aa7234903622916f60",
    "pf_build_v1_manifest.py": "a142e09e803a5b74fa708db2bc88dd2d3f9b2b4ecc7db23e81bca9d081812917",
}

EXPECTED_FILES = {
    "00_SEARCH_HERE_FIRST.md",
    "PF_A1_SERIALIZER_SLOT34_DELTA.tsv",
    "PF_A2_A3_STRING_WIRE_CORRECTION.md",
    "PF_A2_POOL_46BAA0_READER_DELTA.tsv",
    "PF_A2_POOL_46F4D0_DELTA.tsv",
    "PF_A2_POOL_638690_DELTA.tsv",
    "PF_A2_POOL_661FA0_DELTA.tsv",
    "PF_A2_POST_V1_STATIC_DELTA.tsv",
    "PF_A2_SERIALIZER_SLOT34_DELTA.tsv",
    "PF_A2_STRING_WIRE_TAG_DELTA.tsv",
    "PF_A3_SERIALIZER_SLOT34_DELTA.tsv",
    "PF_A3_TAG_CENSUS_DELTA.tsv",
    "PF_A6_VTABLE_CANDIDATE_DELTA.md",
    "PF_A6_VTABLE_CANDIDATE_DELTA.tsv",
    "pf_build_pool_46baa0_reader_delta.py",
    "pf_build_pool_46f4d0_closure.py",
    "pf_build_pool_638690_closure.py",
    "pf_build_pool_661fa0_closure.py",
    "pf_build_post_v1_static_closure.py",
    "pf_build_priority.py",
    "pf_build_serializer_slot34_correction.py",
    "pf_build_string_tag_correction.py",
    "pf_build_target_652a30_nonwire.py",
    "pf_build_targets_694790_6b3440_nonwire.py",
    "pf_build_v1_manifest.py",
    "pf_build_v2_effective_status.py",
    "pf_build_v2_manifest.py",
    "PF_CAPTURE_BRANCH_SHAPES_20260830.md",
    "PF_CAPTURE_BRANCH_SHAPES_20260830.tsv",
    "PF_CAPTURE_DELTA_20260830.inventory.tsv",
    "PF_CAPTURE_DELTA_20260830.md",
    "pf_capture_delta_20260830.py",
    "PF_CAPTURE_DELTA_20260830.validation.tsv",
    "PF_DATA_EVIDENCE.md",
    "PF_DATA_EVIDENCE.tsv",
    "PF_DUMP_REQUEST.md",
    "PF_ERRATUM_TWO_IMAGES.md",
    "PF_EXTERNAL_REPORT.md",
    "pf_extract_capture_branch_shapes_20260830.py",
    "pf_extract_data_evidence.py",
    "pf_extract_dump_rtti.py",
    "pf_extract_dump_vtable_candidates.py",
    "pf_extract_protocol.py",
    "PF_FIELD_VALIDATION.md",
    "PF_FIELD_VALIDATION.tsv",
    "PF_HANDOFF_V1.md",
    "PF_INPUT_INVENTORY.md",
    "PF_INPUT_INVENTORY.tsv",
    "pf_inventory_inputs.py",
    "PF_POOL_46BAA0_BLOCKER.md",
    "PF_POOL_46F4D0_CLOSURE.md",
    "PF_POOL_638690_CLOSURE.md",
    "PF_POOL_661FA0_CLOSURE.md",
    "PF_POST_V1_PRIORITY_DELTA.tsv",
    "PF_POST_V1_STATIC_CLOSURE.md",
    "PF_PRIORITY_POOL_46F4D0_DELTA.tsv",
    "PF_PRIORITY_POOL_638690_DELTA.tsv",
    "PF_PRIORITY_POOL_661FA0_DELTA.tsv",
    "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv",
    "PF_PROTOCOL_PRIORITY.md",
    "PF_PROTOCOL_PRIORITY.tsv",
    "PF_PROTOCOL_REGISTRY.md",
    "PF_PROTOCOL_REGISTRY.tsv",
    "PF_RUNTIME_CLASSMAP.md",
    "PF_RUNTIME_CLASSMAP.tsv",
    "PF_SERIALIZER_FIELDS.md",
    "PF_SERIALIZER_FIELDS.tsv",
    "PF_SERIALIZER_SLOT34_CORRECTION.md",
    "PF_SERIALIZER_SLOT34_ROOTS.tsv",
    "PF_TAG_CENSUS.tsv",
    "PF_TARGET_652A30_A2_DELTA.tsv",
    "PF_TARGET_652A30_NONWIRE.md",
    "PF_TARGETS_694790_6B3440_A2_DELTA.tsv",
    "PF_TARGETS_694790_6B3440_NONWIRE.md",
    "PF_V1_MANIFEST.md",
    "PF_V2_EFFECTIVE_STATUS.md",
    "PF_V2_FIELD_VALIDATION.md",
    "PF_V2_FIELD_VALIDATION.tsv",
    "PF_V2_HANDOFF.md",
    "PF_V2_MANIFEST.md",
    "PF_V2_P1_OPEN.tsv",
    "pf_validate_capture_fields.py",
    "pf_validate_v2_effective_capture.py",
}


class ManifestError(RuntimeError):
    pass


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(name: str) -> tuple[list[str], list[dict[str, str]]]:
    path = OUT_DIR / name
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ManifestError(f"missing TSV header: {name}")
        fields = list(reader.fieldnames)
        rows = [dict(row) for row in reader]
    return fields, rows


def require_text(name: str, snippets: Sequence[str]) -> str:
    text = (OUT_DIR / name).read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            raise ManifestError(f"missing expected text in {name}: {snippet}")
    return text


def verify_namespace(*, manifest_may_be_absent: bool, ignored: set[str] | None = None) -> None:
    ignored = ignored or set()
    entries = [path for path in OUT_DIR.iterdir() if path.name not in ignored]
    directories = sorted(path.name for path in entries if path.is_dir())
    if directories:
        raise ManifestError(f"unexpected directories: {directories}")
    nonfiles = sorted(path.name for path in entries if not path.is_file())
    if nonfiles:
        raise ManifestError(f"unexpected non-files: {nonfiles}")
    actual = {path.name for path in entries}
    accepted = [EXPECTED_FILES]
    if manifest_may_be_absent:
        accepted.append(EXPECTED_FILES - {MANIFEST_PATH.name})
    if actual not in accepted:
        missing = sorted(EXPECTED_FILES - actual)
        extra = sorted(actual - EXPECTED_FILES)
        raise ManifestError(f"namespace mismatch: missing={missing} extra={extra}")


def verify_image_and_v1() -> None:
    if IMAGE_PATH.stat().st_size != IMAGE_SIZE:
        raise ManifestError("pinned image size changed")
    if sha256_path(IMAGE_PATH) != IMAGE_SHA256:
        raise ManifestError("pinned image SHA-256 changed")
    if sha256_path(OUT_DIR / "PF_V1_MANIFEST.md") != V1_MANIFEST_SHA256:
        raise ManifestError("V1 manifest changed")
    for name, expected in V1_PINS.items():
        actual = sha256_path(OUT_DIR / name)
        if actual != expected:
            raise ManifestError(f"V1 artifact changed: {name}: {actual}")


def audit_tsvs() -> dict[str, tuple[int, Counter[str]]]:
    census: dict[str, tuple[int, Counter[str]]] = {}
    for name in sorted(item for item in EXPECTED_FILES if item.endswith(".tsv")):
        fields, rows = read_tsv(name)
        if "source" not in fields:
            raise ManifestError(f"TSV missing source column: {name}")
        source_counts = Counter(row["source"] for row in rows)
        if not source_counts or not set(source_counts).issubset(ALLOWED_SOURCES):
            raise ManifestError(f"invalid/empty TSV sources: {name}: {source_counts}")
        row_tuples = [tuple(row[field] for field in fields) for row in rows]
        if len(row_tuples) != len(set(row_tuples)):
            raise ManifestError(f"exact duplicate TSV row: {name}")
        for key in KEY_COLUMNS:
            if key not in fields:
                continue
            values = [row[key] for row in rows]
            if any(not value for value in values) or len(values) != len(set(values)):
                raise ManifestError(f"invalid/duplicate {key}: {name}")
        for action_column in ("action", "delta_action"):
            if action_column not in fields:
                continue
            for row in rows:
                value = row[action_column].upper()
                if "UNCHANGED" in value or "COPIED" in value:
                    raise ManifestError(f"duplicative delta action: {name}: {value}")
        census[name] = (len(rows), source_counts)
    return census


def audit_no_raw_output_columns() -> None:
    v2_proprietary_tsvs = (
        "PF_CAPTURE_DELTA_20260830.inventory.tsv",
        "PF_CAPTURE_DELTA_20260830.validation.tsv",
        "PF_CAPTURE_BRANCH_SHAPES_20260830.tsv",
        "PF_V2_FIELD_VALIDATION.tsv",
        "PF_A6_VTABLE_CANDIDATE_DELTA.tsv",
    )
    forbidden = {"raw_bytes", "payload", "payload_hex", "packet_hex", "hexdump", "field_value", "byte_value"}
    for name in v2_proprietary_tsvs:
        fields, _rows = read_tsv(name)
        overlap = forbidden & {field.lower() for field in fields}
        if overlap:
            raise ManifestError(f"raw proprietary output column: {name}: {sorted(overlap)}")
    forbidden_suffixes = {".dmp", ".bin", ".cap", ".pcap", ".pcapng"}
    emitted = {Path(name).suffix.lower() for name in EXPECTED_FILES}
    if emitted & forbidden_suffixes:
        raise ManifestError("proprietary binary included in output namespace")


def audit_overlay_targets() -> None:
    """Prove that applying V2 deltas will not replace/remove one row twice."""
    owners: dict[tuple[str, int], str] = {}

    _fields, string_rows = read_tsv("PF_A2_STRING_WIRE_TAG_DELTA.tsv")
    for row in string_rows:
        key = ("PF_SERIALIZER_FIELDS.tsv", int(row["base_row_number"]))
        if key in owners:
            raise ManifestError(f"cross-overlay base target duplicate: {key}")
        owners[key] = "PF_A2_STRING_WIRE_TAG_DELTA.tsv"

    names = (
        "PF_A2_POST_V1_STATIC_DELTA.tsv",
        "PF_A2_POOL_638690_DELTA.tsv",
        "PF_A2_POOL_661FA0_DELTA.tsv",
        "PF_A2_POOL_46F4D0_DELTA.tsv",
        "PF_A2_POOL_46BAA0_READER_DELTA.tsv",
        "PF_A2_SERIALIZER_SLOT34_DELTA.tsv",
        "PF_TARGET_652A30_A2_DELTA.tsv",
        "PF_TARGETS_694790_6B3440_A2_DELTA.tsv",
    )
    for name in names:
        _fields, rows = read_tsv(name)
        for row in rows:
            base_file = row.get("base_file", "")
            if base_file not in {
                "PF_SERIALIZER_FIELDS.tsv",
                "PF_A2_SERIALIZER_SLOT34_DELTA.tsv",
            }:
                continue
            key = (base_file, int(row["base_line"]))
            if key in owners:
                raise ManifestError(
                    f"cross-overlay base target duplicate: {key}: {owners[key]} / {name}"
                )
            owners[key] = name


def audit_priority() -> None:
    _fields, rows = read_tsv("PF_V2_P1_OPEN.tsv")
    if len(rows) != 115:
        raise ManifestError(f"P1 OPEN count changed: {len(rows)}")
    if any(
        row["priority"] != "1"
        or row["effective_structural_status"] != "OPEN"
        or row["source"] != "IMAGE"
        or row["row_semantics"] != "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW"
        for row in rows
    ):
        raise ManifestError("invalid P1 derived status row")
    if len({row["message"] for row in rows}) != 115:
        raise ManifestError("duplicate P1 OPEN message")
    require_text(
        "PF_V2_EFFECTIVE_STATUS.md",
        (
            "Priority 1: **250/365 CLOSED**",
            "Priority 2: **7/16 CLOSED**",
            "Priority 3: **68/138 CLOSED**",
            "Overall: **325/519 CLOSED**",
            "mismatch 386 instances ที่ 3 field locations / 4 field+reason points",
        ),
    )


def audit_effective_a2_a3() -> tuple[int, tuple[int, int], tuple[int, int, int]]:
    _base_fields, base_rows = read_tsv("PF_SERIALIZER_FIELDS.tsv")
    if len(base_rows) != 6931:
        raise ManifestError("V1 A2 row count changed")

    generic_names = (
        "PF_A2_POST_V1_STATIC_DELTA.tsv",
        "PF_A2_POOL_638690_DELTA.tsv",
        "PF_A2_POOL_661FA0_DELTA.tsv",
        "PF_A2_POOL_46F4D0_DELTA.tsv",
        "PF_A2_POOL_46BAA0_READER_DELTA.tsv",
        "PF_TARGET_652A30_A2_DELTA.tsv",
        "PF_TARGETS_694790_6B3440_A2_DELTA.tsv",
    )
    base_removals = 0
    overlay_removals = 0
    for name in generic_names:
        _fields, rows = read_tsv(name)
        for row in rows:
            if not row["action"].startswith("REMOVE"):
                continue
            if row["base_file"] == "PF_SERIALIZER_FIELDS.tsv":
                base_removals += 1
            elif row["base_file"] == "PF_A2_SERIALIZER_SLOT34_DELTA.tsv":
                overlay_removals += 1
            else:
                raise ManifestError(f"unexpected A2 removal base: {name}: {row['base_file']}")

    _fields, slot_rows = read_tsv("PF_A2_SERIALIZER_SLOT34_DELTA.tsv")
    wrong_slot_removals = sum(row["action"] == "REMOVE_WRONG_SLOT_ROW" for row in slot_rows)
    canonical_additions = sum(
        row["action"] in {"ADD_CORRECTED_SLOT34_ROW", "ADD_ANALYSIS_BLOCKER_ROW"}
        for row in slot_rows
    )
    candidate_counts = Counter(
        row["schema_variant"]
        for row in slot_rows
        if row["action"] == "ADD_AMBIGUOUS_CANDIDATE_ROW"
    )
    effective = len(base_rows) - base_removals - wrong_slot_removals + canonical_additions - overlay_removals
    variants = tuple(sorted(effective + count for count in candidate_counts.values()))
    if effective != 8795 or variants != (8821, 8825):
        raise ManifestError(f"effective A2 census changed: {effective}, {variants}")

    _fields, tag_rows = read_tsv("PF_TAG_CENSUS.tsv")
    _fields, string_tag_rows = read_tsv("PF_A3_TAG_CENSUS_DELTA.tsv")
    _fields, slot_tag_rows = read_tsv("PF_A3_SERIALIZER_SLOT34_DELTA.tsv")
    effective_frequency = sum(int(row["frequency_in_A2"]) for row in tag_rows)
    effective_frequency += sum(int(row["frequency_in_A2"]) for row in string_tag_rows)
    effective_frequency += sum(
        int(row["slot34_increment"])
        for row in slot_tag_rows
        if row["action"] == "CHANGED_FREQUENCY"
    )
    candidate_frequency = Counter()
    for row in slot_tag_rows:
        if row["action"] == "CANDIDATE_ALTERNATIVE":
            candidate_frequency[row["schema_variant"]] += int(row["slot34_increment"])
    frequency_variants = tuple(
        sorted(effective_frequency + value for value in candidate_frequency.values())
    )
    if effective_frequency != 4081 or frequency_variants != (4095, 4097):
        raise ManifestError(
            f"effective A3 frequency changed: {effective_frequency}, {frequency_variants}"
        )
    return effective, variants, (effective_frequency, *frequency_variants)


def audit_a5() -> tuple[int, int, int, int]:
    _fields, rows = read_tsv("PF_V2_FIELD_VALIDATION.tsv")
    parse_success = sum(int(row["parse_success_instances"]) for row in rows)
    static_open = sum(int(row["static_open_instances"]) for row in rows)
    not_applied = sum(int(row["schema_not_applied_instances"]) for row in rows)
    mismatch = sum(int(row["mismatch_instances"]) for row in rows)
    mismatch_points = sum(
        len(
            [
                item
                for item in row["mismatch_field_identity_reason_count"].split(" | ")
                if item and item != "NONE"
            ]
        )
        for row in rows
    )
    if (len(rows), parse_success, static_open, not_applied, mismatch, mismatch_points) != (
        66,
        22965,
        78532,
        0,
        386,
        4,
    ):
        raise ManifestError(
            "A5 census changed: "
            f"rows={len(rows)} pass={parse_success} open={static_open} "
            f"not_applied={not_applied} mismatch={mismatch}/{mismatch_points}"
        )
    require_text(
        "PF_V2_FIELD_VALIDATION.md",
        (
            "# 🔴 A5 V2 พบ static/capture mismatch",
            "[MEASURED][CAPTURE] ตัวเลขทั้งหมดด้านล่างมาจาก corpus และ effective schema ที่ pin hash ไว้",
            "inventoried paths: 2154",
            "exact-content duplicate paths rejected before claim counting: 645",
            "V1 rows: 6931; effective canonical rows: 8795",
            "mismatch: 386 instances / 3 field locations / 4 field+reason points",
            "unique full-file SHA-256 contents hashed and de-duplicated at one canonical path each: 1509",
            "canonical non-text contents skipped by the packet-text parser: 561",
            "text contents with no recognized packet blocks and therefore no frames: 556",
        ),
    )
    return parse_success, static_open, mismatch, mismatch_points


def audit_capture_and_a6() -> None:
    _fields, branch_rows = read_tsv("PF_CAPTURE_BRANCH_SHAPES_20260830.tsv")
    if len(branch_rows) != 67 or any(
        row["delta_status"] != "ADDED_NEW_LENGTH" or row["source"] != "CAPTURE"
        for row in branch_rows
    ):
        raise ManifestError("capture branch-shape census changed")
    _fields, a6_rows = read_tsv("PF_A6_VTABLE_CANDIDATE_DELTA.tsv")
    if len(a6_rows) != 134 or any(
        row["record_kind"] != "REJECTED_NOT_VTABLE"
        or row["strict_vtable_va"] != "UNKNOWN"
        or row["class_name"] != "UNKNOWN"
        or row["source"] != "DUMP"
        for row in a6_rows
    ):
        raise ManifestError("A6 rejection census changed")


def audit_all(*, manifest_may_be_absent: bool, ignored: set[str] | None = None) -> dict[str, tuple[int, Counter[str]]]:
    verify_namespace(manifest_may_be_absent=manifest_may_be_absent, ignored=ignored)
    verify_image_and_v1()
    for name in sorted(EXPECTED_FILES - {MANIFEST_PATH.name}):
        (OUT_DIR / name).read_text(encoding="utf-8")
    census = audit_tsvs()
    audit_no_raw_output_columns()
    audit_overlay_targets()
    audit_priority()
    audit_effective_a2_a3()
    audit_a5()
    audit_capture_and_a6()
    _fields, registry_rows = read_tsv("PF_PROTOCOL_REGISTRY.tsv")
    _fields, a1_delta_rows = read_tsv("PF_A1_SERIALIZER_SLOT34_DELTA.tsv")
    if len(registry_rows) != 519 or len(a1_delta_rows) != 59:
        raise ManifestError("A1 logical/delta census changed")
    return census


def build_manifest(census: Mapping[str, tuple[int, Counter[str]]]) -> str:
    lines = [
        "# PF V2 final local manifest and audit",
        "",
        "🔴 **A5 V2 พบ 3 field locations / 4 field+reason points / 386 instances** ระหว่าง IMAGE schema กับ CAPTURE; ไม่ได้แก้ตาราง IMAGE ให้เข้ากับสายจริง",
        "",
        "## Audit result",
        "",
        "- result: `PASS`",
        "- pinned GameClient.local.bin: `PASS` (14,759,424 bytes)",
        "- immutable V1 manifest + 26 artifacts: `PASS`",
        "- exact external namespace: `PASS`",
        "- UTF-8 decode: `PASS`",
        "- allowed TSV sources: `IMAGE | DUMP | CAPTURE | DATA`",
        "- exact duplicate TSV rows: `0`",
        "- duplicate delta/dedup/root/status/validation keys: `0`",
        "- cross-overlay base-row targets: `0` duplicates",
        "- V2 `UNCHANGED`/`COPIED` delta rows: `0`",
        "- proprietary raw dump/capture output columns or binary files: `0`",
        "",
        "## Effective checkpoint",
        "",
        "| measure | result |",
        "|---|---:|",
        "| Priority 1 IMAGE-static | 250/365 CLOSED; 115 OPEN |",
        "| Priority 2 IMAGE-static | 7/16 CLOSED; 9 OPEN |",
        "| Priority 3 IMAGE-static | 68/138 CLOSED; 70 OPEN |",
        "| Overall IMAGE-static | 325/519 CLOSED; 194 OPEN |",
        "| effective canonical A2 | 8,795 rows |",
        "| ItemAttr candidate alternatives | 8,821 base **or** 8,825 derived; never merged |",
        "| effective A3 frequency | 4,081; alternatives 4,095 or 4,097 |",
        "| A5 unique capture contents | 1,509 of 2,154 paths; 645 duplicates rejected |",
        "| A5 parse/static-open/mismatch | 22,965 / 78,532 / 386 (3 field locations / 4 field+reason points) |",
        "| A6 strict RTTI class/vtable | 0; 134 candidates rejected |",
        "",
        "## Duplicate-control conclusion",
        "",
        "V2 เป็น overlay ไม่ใช่สำเนาตารางเต็ม: `CHANGED` แทนที่แถวฐาน, `REMOVE*` ลบเป้าหมาย, `ADD*` เพิ่มแถวใหม่ และ derived status index ไม่นับเป็น evidence table อีกชุด. Capture path ที่เนื้อหาซ้ำ 645 paths ถูกตัดก่อนนับ canonical claims.",
        "",
        "## Delivery boundary",
        "",
        "ชุดนี้อยู่ local-only ใต้ `pf_bridge/external` และถูก repository ignore; ผู้ที่เข้าถึงโฟลเดอร์บนเครื่องนี้อ่านได้ครบ แต่ clean clone/remote ไม่ได้รับ V2 โดยอัตโนมัติ. ไม่มี client/server runtime, server code, workflow หรือ queue ถูกแก้หรือรันใน checkpoint นี้.",
        "",
        "## Artifact hashes",
        "",
        "`PF_V2_MANIFEST.md` ไม่ hash ตัวเอง. ทุกไฟล์อื่นใน exact namespace อยู่ด้านล่าง",
        "",
        "| file | bytes | SHA-256 | TSV rows | source counts |",
        "|---|---:|---|---:|---|",
    ]
    for name in sorted(EXPECTED_FILES - {MANIFEST_PATH.name}):
        path = OUT_DIR / name
        if name in census:
            row_count, sources = census[name]
            source_text = ", ".join(f"{source}={sources[source]}" for source in sorted(sources))
            row_text = str(row_count)
        else:
            row_text = "—"
            source_text = "—"
        lines.append(
            f"| `{name}` | {path.stat().st_size} | `{sha256_path(path).upper()}` | {row_text} | `{source_text}` |"
        )
    lines.extend(
        (
            "",
            "## Reproduction",
            "",
            "Run `py -3 -B pf_build_v2_manifest.py --check` after all component generators pass `--check`. The manifest is the final write of the checkpoint.",
            "",
        )
    )
    return "\n".join(lines)


def artifact_fingerprints() -> dict[str, tuple[int, str]]:
    return {
        name: ((OUT_DIR / name).stat().st_size, sha256_path(OUT_DIR / name))
        for name in EXPECTED_FILES - {MANIFEST_PATH.name}
    }


def atomic_publish(text: str) -> None:
    before = artifact_fingerprints()
    image_before = (IMAGE_PATH.stat().st_size, sha256_path(IMAGE_PATH))
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=OUT_DIR,
            prefix=".PF_V2_MANIFEST.md.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        audit_all(manifest_may_be_absent=True, ignored={temporary.name})
        if artifact_fingerprints() != before:
            raise ManifestError("artifact changed during manifest build")
        if (IMAGE_PATH.stat().st_size, sha256_path(IMAGE_PATH)) != image_before:
            raise ManifestError("pinned image changed during manifest build")
        os.replace(temporary, MANIFEST_PATH)
        temporary = None
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    census = audit_all(manifest_may_be_absent=not args.check)
    expected = build_manifest(census)
    if args.check:
        if not MANIFEST_PATH.exists() or MANIFEST_PATH.read_text(encoding="utf-8") != expected:
            raise ManifestError("PF_V2_MANIFEST.md differs from re-derived manifest")
        print(
            "check ok: namespace=83 hashed_artifacts=82 P1=250/365 "
            "A2=8795 A5_mismatch=386/4 duplicate_rows=0"
        )
        return 0
    atomic_publish(expected)
    audit_all(manifest_may_be_absent=False)
    if MANIFEST_PATH.read_text(encoding="utf-8") != expected:
        raise ManifestError("published manifest mismatch")
    print(f"PF_V2_MANIFEST.md {sha256_path(MANIFEST_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
