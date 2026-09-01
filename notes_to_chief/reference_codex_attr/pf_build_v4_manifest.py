#!/usr/bin/env python3
"""Build and verify the duplicate-safe PF V4 local checkpoint.

V4 is an additive overlay over the exact frozen V3 namespace.  The manifest is
the commit marker.  Publication is Windows-only and uses an owned kernel handle
whose share mode prevents another process from unlinking or replacing the lock
while the transaction is live.  ``--check`` and ``--audit-only`` never publish.
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType, ModuleType
from typing import Iterator, Mapping, Sequence


# This must precede every local import.  Child checks also receive -B and the
# environment switch.  A cache directory is therefore residue, never output.
sys.dont_write_bytecode = True

OUT_DIR = Path(__file__).resolve().parent
INDEX_PATH = OUT_DIR / "00_SEARCH_HERE_FIRST.md"
HANDOFF_PATH = OUT_DIR / "PF_V4_HANDOFF.md"
MANIFEST_PATH = OUT_DIR / "PF_V4_MANIFEST.md"
V3_MANIFEST_PATH = OUT_DIR / "PF_V3_MANIFEST.md"
LOCK_PATH = OUT_DIR / ".PF_V4_MANIFEST_PUBLISH.lock"
TRANSACTION_PREFIX = ".PF_V4_MANIFEST_TXN."
IMAGE_PATH = OUT_DIR.parent.parent / "GameClient" / "GameClient.local.bin"

IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
V3_MANIFEST_SIZE = 16_871
V3_MANIFEST_SHA256 = "dc87eedc65ed5e07ce4673742b6a0d20304140bb177e617c6af8b3846bd0b50e"
V3_INDEX_SIZE = 11_466
V3_INDEX_SHA256 = "52be24d7b410d87aef2ba4a4aec962e4314cbf554d12a78327fdd55d82626008"
V3_MANIFEST_ROWS = 99
V3_TABLE_RE = re.compile(
    r"^\| `([^`]+)` \| (\d+) \| `([0-9A-F]{64})` \|", re.MULTILINE
)

CANONICAL_A5_TSV = "PF_V2_FIELD_VALIDATION.tsv"
CANONICAL_A5_SHA256 = "10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806"
DERIVED_STATUS_SEMANTICS = "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW"
STATUS_FILES = ("PF_V2_P1_OPEN.tsv", "PF_V3_P1_OPEN.tsv", "PF_V4_P1_OPEN.tsv")
ALLOWED_SOURCES = {"IMAGE", "DUMP", "CAPTURE", "DATA"}
OWNED_KEY_COLUMNS = {
    "delta_key", "dedup_key", "root_key", "status_key", "validation_key", "classmap_key",
}
REFERENCE_KEY_COLUMNS = {
    "base_row_key", "base_delta_key", "effective_schema_key", "child_priority_delta_key",
}
EXPECTED_HISTORICAL_STATUS_BASE_REFS = {
    "bb2509e7781ece1030897b75cea40b1e324635e30e7926a9c38ed49057bcdf00",
    "8b5e55e9abec890359065409783812e8d4c85313456ad74ea65e1d7fc9ce7341",
}

# Publication stays disabled until the root reviewer supplies the final status
# and validator hashes.  Read-only --audit-only is intentionally available in
# the meantime.  Flip only together with those reviewed pins.
PUBLICATION_RELEASED = True

V4_COMPONENT_FILES = {
    "pf_build_daily_activity_closure.py",
    "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv",
    "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv",
    "PF_DAILY_ACTIVITY_CLOSURE.md",
    "pf_build_embedded_child_composition.py",
    "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv",
    "PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv",
    "PF_EMBEDDED_CHILD_COMPOSITION.md",
    "pf_build_static_type_info_classmap.py",
    "PF_STATIC_TYPE_INFO_CLASSMAP.tsv",
    "PF_STATIC_TYPE_INFO_CLASSMAP.md",
    "pf_build_v4_effective_status.py",
    "PF_A1_STATIC_TYPE_INFO_DELTA.tsv",
    "PF_PRIORITY_STATIC_TYPE_INFO_DELTA.tsv",
    "PF_V4_P1_OPEN.tsv",
    "PF_V4_EFFECTIVE_STATUS.md",
    "pf_validate_v4_effective_capture.py",
    "PF_V4_FIELD_VALIDATION.md",
}
V4_INTEGRATION_FILES = {
    "pf_build_v4_manifest.py", HANDOFF_PATH.name, MANIFEST_PATH.name,
}
V4_FILES = V4_COMPONENT_FILES | V4_INTEGRATION_FILES
PUBLISHED_OUTPUTS = (HANDOFF_PATH.name, INDEX_PATH.name, MANIFEST_PATH.name)

# Exact commit marker and generated products of the immediately preceding V4
# publication.  Corrective publication may replace only this authenticated
# triple (or an already-current derivation); arbitrary stale integration bytes
# are never accepted merely because the namespace is complete.
PRIOR_V4_INTEGRATION_PINS = {
    HANDOFF_PATH.name: (4_443, "6725099c76fdcc9402291b082d3ac233e4e9e6b2dcac5230ef46740daf9300cf"),
    INDEX_PATH.name: (13_393, "3bf7487c83ca9d290d140654c145436004a48432d4ca2a2b5712fa9ff820de96"),
    MANIFEST_PATH.name: (20_110, "3a3281175b2e5e9efb6b2e191d2d6809ef7a9a80e0aa1e2a707899cd198889c1"),
}

# The composition pins below are frozen after held-handle review.  Status and
# validator pins are provisional while PUBLICATION_RELEASED is False.
REVIEWED_V4_PINS = {
    "pf_build_daily_activity_closure.py": "e58f4da41e6f82c9a3c182961019394ebab4b8034e1d39f2c8c92b272a35d09d",
    "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv": "10b54ee781ad0147d5bd18c0171b88132d9fd61dc39e0adf6fa4055bc7b7890d",
    "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv": "395b1776d3351304612ceb36eade9003b929fb8bb914986b4873f0737e60a5e3",
    "PF_DAILY_ACTIVITY_CLOSURE.md": "7a58caf4efb025c0703fa4a583785cb0d7d61269d4d92ddf18118da299bfc75e",
    "pf_build_embedded_child_composition.py": "a8963458bc15fa13e7a60adf79fc75ae5183937af88ffa9a05602fbc9f8f7bba",
    "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv": "b81c7a5590d60c44f10e4171a722feb680e0e83865e6c5c033121e9dccffbe00",
    "PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv": "048216205e1a99a1b4561bf643e1ad80bcf1a29283a4b526ee048654fac82d44",
    "PF_EMBEDDED_CHILD_COMPOSITION.md": "4801b0412a164a53b524d96ddcb7800a56c59ad8447e83f4a3d11f88cfc0bd69",
    "pf_build_static_type_info_classmap.py": "e25a45a13ad9b010ede4b155f219f791585e93a7637e27ae51348050f231c276",
    "PF_STATIC_TYPE_INFO_CLASSMAP.tsv": "b5de29afb7c7af3c5b785130fdf368b4e1d089d0945441671201880f4429dea2",
    "PF_STATIC_TYPE_INFO_CLASSMAP.md": "b26f4060b6644c9653de37db0db0bf87afbcc8e8d7d9fc98f705723db221c8e2",
    "pf_build_v4_effective_status.py": "65245b5d33af0a9d5cbcad44c1f7876b2126bd47769dbacc7130e188a560d5e8",
    "PF_A1_STATIC_TYPE_INFO_DELTA.tsv": "f63b8c9bd868a66b76e1180d969c42a5f6aaa30fc31c2334a9f5ba000ee9ad4e",
    "PF_PRIORITY_STATIC_TYPE_INFO_DELTA.tsv": "07a5bd1a2319231778a4159e19eb782c842f04a882fefc4718a49f303f901b2c",
    "PF_V4_P1_OPEN.tsv": "d612cd73c66f0e3717cd899c4f594118e2c57d8a215d6b1802b6da009e046123",
    "PF_V4_EFFECTIVE_STATUS.md": "15fa03ab107476cc8680b8c71385fde1161d74b23891785eaaba60b7fa6280b7",
    "pf_validate_v4_effective_capture.py": "d2e517b4457af2a0f7983d3b60ad88232fad69af392f8287adbe54bef0d2839a",
    "PF_V4_FIELD_VALIDATION.md": "4345387b12cbbe048ee3c3a78c43c15d22f680a5082a25bb8de30359aee75ef7",
}

COMPONENT_CHECKS = (
    (
        "pf_build_daily_activity_closure.py",
        ("--check", "--external", str(OUT_DIR)),
        "PASS DailyActivityState:",
    ),
    (
        "pf_build_embedded_child_composition.py",
        ("--check", "--external", str(OUT_DIR), "--image", str(IMAGE_PATH)),
        "PASS embedded-child composition mode=check",
    ),
    (
        "pf_build_static_type_info_classmap.py",
        ("--check", "--image", str(IMAGE_PATH)),
        "mode=check",
    ),
    ("pf_build_v4_effective_status.py", ("--check",), "PASS V4 P1=255/365"),
    (
        "pf_validate_v4_effective_capture.py",
        ("--check", "--external", str(OUT_DIR), "--game-client", str(IMAGE_PATH.parent)),
        "mismatch=386 mismatch_points=4",
    ),
)

A2_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "direction(W/R)", "old_order", "old_tag",
    "old_field_offset", "old_len", "new_wire_order", "new_tag", "new_field_offset",
    "new_len", "new_gate_condition", "resolution", "evidence_ticket",
    "evidence_span_start", "evidence_span_end", "evidence_span_sha256",
    "evidence_file_off", "source",
)
COMPOSITION_A2_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "direction(W/R)", "old_order", "old_tag",
    "old_field_offset", "old_len", "new_wire_order", "new_tag", "new_field_offset",
    "new_len", "new_gate_condition", "resolution", "child_message", "child_receiver",
    "child_vtable_va", "child_slot", "child_serializer_va", "child_effective_rows",
    "child_effective_unknown_rows", "evidence_ticket", "evidence_span_start",
    "evidence_span_end", "evidence_span_sha256", "evidence_file_off", "source",
)
PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "base_delta_key",
    "message", "priority", "old_registry_identity_status", "new_registry_identity_status",
    "old_registry_identity_missing", "new_registry_identity_missing",
    "old_serializer_status", "new_serializer_status", "old_serializer_blockers",
    "new_serializer_blockers", "old_structural_status", "new_structural_status",
    "old_blocker", "new_blocker", "evidence_ticket", "closure_scope", "source",
)
COMPOSITION_PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "base_delta_key",
    "message", "priority", "old_registry_identity_status", "new_registry_identity_status",
    "old_registry_identity_missing", "new_registry_identity_missing",
    "old_serializer_status", "new_serializer_status", "old_serializer_blockers",
    "new_serializer_blockers", "old_structural_status", "new_structural_status",
    "old_blocker", "new_blocker", "old_primary_blocker_group", "new_primary_blocker_group",
    "child_message", "child_priority_file", "child_priority_delta_key",
    "child_priority_file_sha256", "evidence_ticket", "closure_scope", "source",
)
CLASSMAP_COLUMNS = (
    "classmap_key", "registry_name", "class_name", "decorated_name", "identity_kind",
    "vtable_va", "vtable_file_off", "registry_getter_va", "getter_pointer_file_off",
    "descriptor_getter_va", "descriptor_getter_target_va", "descriptor_va",
    "descriptor_file_off", "descriptor_reference_count", "type_descriptor_va",
    "type_descriptor_file_off", "class_name_file_off", "initializer_start",
    "initializer_end", "initializer_file_off", "initializer_span_sha256",
    "base_descriptor_chain", "source",
)
A1_STATIC_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "base_delta_key",
    "registry_name", "old_vtable_va", "new_base_class_name", "new_base_class_vtable_va",
    "retained_derived_classes", "retained_derived_vtables", "serializer_identity_status",
    "serializer_candidates", "serializer_selection", "canonical_a2_action", "classmap_file",
    "classmap_keys", "proof_kind", "resolution", "source",
)
STATIC_PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "base_delta_key",
    "message", "priority", "old_registry_identity_status", "new_registry_identity_status",
    "old_registry_identity_missing", "new_registry_identity_missing",
    "old_serializer_status", "new_serializer_status", "old_serializer_blockers",
    "new_serializer_blockers", "old_structural_status", "new_structural_status",
    "old_blocker", "new_blocker", "old_registry_identity_proof_kind",
    "new_registry_identity_proof_kind", "retained_polymorphism_nonclaim",
    "evidence_ticket", "closure_scope", "source",
)
STATUS_COLUMNS = (
    "status_key", "message", "priority", "matched_groups", "matched_keywords",
    "base_line", "base_registry_identity_status", "effective_registry_identity_status",
    "effective_registry_identity_missing", "base_serializer_status",
    "effective_serializer_status", "base_structural_status", "effective_structural_status",
    "primary_blocker_group", "effective_blocker", "applied_overlay_chain",
    "row_semantics", "source",
)
A5_COLUMNS = (
    "validation_key", "message", "direction(W/R)", "schema_variant", "effective_schema_key",
    "observed_frames", "observed_instances", "baseline_observed_instances",
    "new_observed_instances", "parse_success_frames", "parse_success_instances",
    "baseline_parse_success_instances", "new_parse_success_instances", "static_open_frames",
    "static_open_instances", "baseline_static_open_instances", "new_static_open_instances",
    "static_open_reason_count", "schema_not_applied_frames", "schema_not_applied_instances",
    "baseline_schema_not_applied_instances", "new_schema_not_applied_instances",
    "schema_not_applied_reason_count", "mismatch_frames", "mismatch_instances",
    "baseline_mismatch_instances", "new_mismatch_instances",
    "mismatch_field_identity_reason_count", "record_instances_observed",
    "record_branch_coverage", "capture_file_count", "status", "content_dedup_scope", "source",
)
EXACT_SCHEMAS = {
    "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv": A2_COLUMNS,
    "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv": PRIORITY_COLUMNS,
    "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv": COMPOSITION_A2_COLUMNS,
    "PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv": COMPOSITION_PRIORITY_COLUMNS,
    "PF_STATIC_TYPE_INFO_CLASSMAP.tsv": CLASSMAP_COLUMNS,
    "PF_A1_STATIC_TYPE_INFO_DELTA.tsv": A1_STATIC_COLUMNS,
    "PF_PRIORITY_STATIC_TYPE_INFO_DELTA.tsv": STATIC_PRIORITY_COLUMNS,
    "PF_V4_P1_OPEN.tsv": STATUS_COLUMNS,
    CANONICAL_A5_TSV: A5_COLUMNS,
}
EXACT_SOURCE_SETS = {
    name: {"IMAGE"} for name in (
        "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv",
        "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv",
        "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv",
        "PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv",
        "PF_STATIC_TYPE_INFO_CLASSMAP.tsv",
        "PF_A1_STATIC_TYPE_INFO_DELTA.tsv",
        "PF_PRIORITY_STATIC_TYPE_INFO_DELTA.tsv",
        "PF_V4_P1_OPEN.tsv",
    )
}
EXACT_SOURCE_SETS[CANONICAL_A5_TSV] = {"CAPTURE"}

EXPECTED_A5 = {
    "rows": 66,
    "parse_success": 22_965,
    "static_open": 78_532,
    "schema_not_applied": 0,
    "mismatch": 386,
    "mismatch_points": 4,
    "field_locations": 3,
}
EXPECTED_ITEM_VARIANTS = {
    ("ItemAttr", "R", "VTABLE_0x00F0EBB0"): 13,
    ("ItemAttr", "W", "VTABLE_0x00F0EBB0"): 13,
    ("ItemAttr", "R", "VTABLE_0x00F4A188"): 15,
    ("ItemAttr", "W", "VTABLE_0x00F4A188"): 15,
}
EXPECTED_PLAN_CENSUS = {"APPLICABLE": 624, "STATIC_OPEN": 368, "SCHEMA_NOT_APPLIED": 46}

RAW_BYTE_PATTERNS = (
    re.compile(r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"),
    re.compile(r"(?:\\x[0-9A-Fa-f]{2}){4,}"),
    re.compile(r"(?:0x[0-9A-Fa-f]{2}\s*,\s*){7,}0x[0-9A-Fa-f]{2}\b"),
    re.compile(r"data:[^\s]*;base64,", re.IGNORECASE),
    re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{96,}={0,2}(?![A-Za-z0-9+/])"),
)

V3_INDEX_MARKER = (
    "<!-- PF_V4_FROZEN_V3_INDEX_BEGIN "
    f"bytes={V3_INDEX_SIZE} sha256={V3_INDEX_SHA256} -->"
).encode("ascii")


class ManifestError(RuntimeError):
    pass


@dataclass(frozen=True)
class Snapshot:
    expected: frozenset[str]
    files: Mapping[str, bytes]
    identities: Mapping[str, tuple[int, int]]
    v3_hashes: Mapping[str, tuple[int, str]]
    image_fingerprint: tuple[int, str]

    def text(self, name: str) -> str:
        try:
            value = self.files[name].decode("utf-8", errors="strict")
        except (KeyError, UnicodeError) as exc:
            raise ManifestError(f"missing/non-UTF-8 snapshot artifact: {name}") from exc
        if "\x00" in value:
            raise ManifestError(f"NUL in textual artifact: {name}")
        return value


@dataclass(frozen=True)
class TsvArtifact:
    fields: tuple[str, ...]
    rows: tuple[dict[str, str], ...]
    raw_lines: tuple[str, ...]


@dataclass(frozen=True)
class TsvAudit:
    tables: Mapping[str, TsvArtifact]
    census: Mapping[str, tuple[int, Counter[str]]]
    delta_dedup_count: int
    base_target_count: int
    base_delta_ref_count: int
    repeated_lines: int
    repeated_occurrences: int
    repeated_extras: int
    inherited_v4_rows: int
    total_rows: int
    a2_add_semantic_count: int
    a2_add_semantic_duplicate_groups: int


@dataclass(frozen=True)
class Audit:
    snapshot: Snapshot
    tsv: TsvAudit
    a5: Mapping[str, int]
    effective: Mapping[str, int]
    frozen_v3_index: bytes
    final_handoff: bytes
    final_index: bytes


@dataclass
class HeldWindowsLock:
    fd: int
    payload: bytes
    path: Path
    retain: bool = False


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def image_fingerprint() -> tuple[int, str]:
    data = IMAGE_PATH.read_bytes()
    return len(data), sha256_bytes(data)


def file_identity(path: Path) -> tuple[int, int]:
    stat = path.stat(follow_symlinks=False)
    return int(stat.st_dev), int(stat.st_ino)


def read_stable_file(path: Path) -> tuple[bytes, tuple[int, int]]:
    before = path.stat(follow_symlinks=False)
    if path.is_symlink() or path.resolve().parent != OUT_DIR:
        raise ManifestError(f"symlink/reparse/nonlocal output: {path.name}")
    data = path.read_bytes()
    after = path.stat(follow_symlinks=False)
    before_state = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    after_state = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if before_state != after_state or len(data) != after.st_size:
        raise ManifestError(f"artifact changed while read: {path.name}")
    return data, (int(after.st_dev), int(after.st_ino))


def parse_v3_hashes(data: bytes) -> dict[str, tuple[int, str]]:
    if (len(data), sha256_bytes(data)) != (V3_MANIFEST_SIZE, V3_MANIFEST_SHA256):
        raise ManifestError("frozen V3 manifest changed")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ManifestError("frozen V3 manifest is not UTF-8") from exc
    found = V3_TABLE_RE.findall(text)
    if len(found) != V3_MANIFEST_ROWS or len({name.casefold() for name, _s, _h in found}) != V3_MANIFEST_ROWS:
        raise ManifestError(f"V3 manifest table census/uniqueness changed: {len(found)}")
    rows = {name: (int(size), digest.lower()) for name, size, digest in found}
    if rows.get(INDEX_PATH.name) != (V3_INDEX_SIZE, V3_INDEX_SHA256):
        raise ManifestError("frozen V3 index table pin changed")
    for name in rows:
        if Path(name).name != name or "/" in name or "\\" in name:
            raise ManifestError(f"non-local V3 manifest member: {name}")
    return rows


def expected_files(v3_hashes: Mapping[str, tuple[int, str]]) -> set[str]:
    expected = set(v3_hashes) | {V3_MANIFEST_PATH.name} | V4_FILES
    if len(expected) != 121:
        raise ManifestError(f"V4 exact namespace census changed: {len(expected)} != 121")
    if len(expected) != len({name.casefold() for name in expected}):
        raise ManifestError("case-insensitive output namespace collision")
    if {"PF_V3_FIELD_VALIDATION.tsv", "PF_V4_FIELD_VALIDATION.tsv"} & expected:
        raise ManifestError("unchanged A5 TSV copy entered V3/V4 namespace")
    return expected


def verify_namespace(
    expected: set[str] | frozenset[str], *, allow_unpublished: bool,
    transients: frozenset[str],
) -> None:
    for name in transients:
        if Path(name).name != name:
            raise ManifestError(f"invalid transient namespace: {name}")
        if name != LOCK_PATH.name and not name.startswith(TRANSACTION_PREFIX):
            raise ManifestError(f"unrecognised active transient: {name}")
    entries = list(OUT_DIR.iterdir())
    actual = {path.name for path in entries}
    if len(actual) != len({name.casefold() for name in actual}):
        raise ManifestError("case-insensitive live namespace collision")
    for path in entries:
        if path.is_symlink() or path.resolve().parent != OUT_DIR:
            raise ManifestError(f"symlink/reparse/nonlocal output: {path.name}")
        if path.name in transients - {LOCK_PATH.name}:
            if not path.is_dir():
                raise ManifestError(f"transaction transient is not a directory: {path.name}")
        elif not path.is_file():
            raise ManifestError(f"unexpected directory/non-file: {path.name}")
    accepted = {frozenset(set(expected) | set(transients))}
    if allow_unpublished:
        accepted.add(frozenset((set(expected) - {HANDOFF_PATH.name, MANIFEST_PATH.name}) | set(transients)))
    if frozenset(actual) not in accepted:
        closest = min(accepted, key=lambda item: len(item ^ actual))
        raise ManifestError(
            f"namespace mismatch: missing={sorted(closest-actual)} extra={sorted(actual-closest)}"
        )


def take_snapshot(*, allow_unpublished: bool, transients: frozenset[str]) -> Snapshot:
    v3_data, v3_identity = read_stable_file(V3_MANIFEST_PATH)
    v3_hashes = parse_v3_hashes(v3_data)
    expected = frozenset(expected_files(v3_hashes))
    verify_namespace(expected, allow_unpublished=allow_unpublished, transients=transients)
    files: dict[str, bytes] = {V3_MANIFEST_PATH.name: v3_data}
    identities: dict[str, tuple[int, int]] = {V3_MANIFEST_PATH.name: v3_identity}
    for name in sorted(expected - {V3_MANIFEST_PATH.name}):
        path = OUT_DIR / name
        if allow_unpublished and name in {HANDOFF_PATH.name, MANIFEST_PATH.name} and not path.exists():
            continue
        data, identity = read_stable_file(path)
        files[name], identities[name] = data, identity
    snapshot = Snapshot(
        expected=frozenset(expected),
        files=MappingProxyType(files),
        identities=MappingProxyType(identities),
        v3_hashes=MappingProxyType(v3_hashes),
        image_fingerprint=image_fingerprint(),
    )
    assert_snapshot_current(snapshot, transients=transients)
    return snapshot


def assert_snapshot_current(snapshot: Snapshot, *, transients: frozenset[str]) -> None:
    absent = {HANDOFF_PATH.name, MANIFEST_PATH.name} - set(snapshot.files)
    allow_unpublished = absent == {HANDOFF_PATH.name, MANIFEST_PATH.name}
    if absent and not allow_unpublished:
        raise ManifestError(f"partial integration snapshot: {sorted(absent)}")
    verify_namespace(snapshot.expected, allow_unpublished=allow_unpublished, transients=transients)
    for name in sorted(snapshot.expected):
        path = OUT_DIR / name
        if name not in snapshot.files:
            if path.exists():
                raise ManifestError(f"CAS absent artifact appeared: {name}")
            continue
        data, identity = read_stable_file(path)
        if data != snapshot.files[name] or identity != snapshot.identities[name]:
            raise ManifestError(f"CAS artifact bytes/identity changed: {name}")
    if image_fingerprint() != snapshot.image_fingerprint:
        raise ManifestError("CAS pinned image changed")


def load_local_module(module_name: str, path: Path, expected_hash: str) -> ModuleType:
    if sha256_bytes(path.read_bytes()) != expected_hash:
        raise ManifestError(f"module pin changed before import: {path.name}")
    cached = sys.modules.get(module_name)
    if cached is not None:
        return cached
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ManifestError(f"cannot construct module spec: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    return module


def frozen_v3_index(snapshot: Snapshot) -> bytes:
    module_name = "_pf_frozen_v3_manifest_" + snapshot.v3_hashes["pf_build_v3_manifest.py"][1][:16]
    module = load_local_module(
        module_name,
        OUT_DIR / "pf_build_v3_manifest.py",
        snapshot.v3_hashes["pf_build_v3_manifest.py"][1],
    )
    expected_a5 = {
        "rows": 66, "parse_success": 22_965, "static_open": 78_532,
        "schema_not_applied": 0, "mismatch": 386, "mismatch_points": 4,
        "field_locations": 3,
    }
    data = module.build_index(expected_a5, 95).encode("utf-8")
    if (len(data), sha256_bytes(data)) != (V3_INDEX_SIZE, V3_INDEX_SHA256):
        raise ManifestError("reconstructed complete V3 index bytes changed")
    return data


def verify_inputs(snapshot: Snapshot) -> bytes:
    if snapshot.image_fingerprint != (IMAGE_SIZE, IMAGE_SHA256):
        raise ManifestError("pinned client image changed")
    for name, (size, digest) in snapshot.v3_hashes.items():
        if name == INDEX_PATH.name:
            continue
        data = snapshot.files[name]
        if (len(data), sha256_bytes(data)) != (size, digest):
            raise ManifestError(f"frozen V3 artifact changed: {name}")
    for name, digest in REVIEWED_V4_PINS.items():
        data = snapshot.files.get(name)
        if data is None or sha256_bytes(data) != digest:
            actual = "MISSING" if data is None else sha256_bytes(data)
            raise ManifestError(f"reviewed V4 pin changed: {name}: {actual} != {digest}")
    frozen = frozen_v3_index(snapshot)
    if HANDOFF_PATH.name not in snapshot.files and snapshot.files[INDEX_PATH.name] != frozen:
        raise ManifestError("pre-publication index is not the exact frozen V3 index")
    return frozen


def read_tsv(snapshot: Snapshot, name: str) -> TsvArtifact:
    text = snapshot.text(name)
    try:
        parsed = list(csv.reader(io.StringIO(text, newline=""), delimiter="\t", strict=True))
    except csv.Error as exc:
        raise ManifestError(f"malformed TSV quoting: {name}") from exc
    if not parsed or not parsed[0] or any(not field for field in parsed[0]):
        raise ManifestError(f"empty/blank TSV header: {name}")
    fields = tuple(parsed[0])
    if len(fields) != len(set(fields)):
        raise ManifestError(f"duplicate TSV header: {name}")
    rows: list[dict[str, str]] = []
    for line, cells in enumerate(parsed[1:], start=2):
        if len(cells) != len(fields):
            raise ManifestError(f"TSV cell-count mismatch: {name}:{line}")
        rows.append(dict(zip(fields, cells, strict=True)))
    raw_lines = tuple(text.splitlines()[1:])
    if len(raw_lines) != len(rows) or any(not line for line in raw_lines):
        raise ManifestError(f"multiline/blank physical TSV row is forbidden: {name}")
    return TsvArtifact(fields, tuple(rows), raw_lines)


def normalise_status_reference(row: Mapping[str, str]) -> dict[str, str]:
    result = dict(row)
    if "applied_overlay" in result:
        result["applied_overlay_chain"] = result.pop("applied_overlay")
    return result


def audit_tsvs(snapshot: Snapshot) -> TsvAudit:
    tables: dict[str, TsvArtifact] = {}
    census: dict[str, tuple[int, Counter[str]]] = {}
    owners: dict[tuple[str, str], list[tuple[str, dict[str, str]]]] = defaultdict(list)
    cross_namespace: dict[str, str] = {}
    raw_occurrences: dict[str, list[tuple[str, int, dict[str, str]]]] = defaultdict(list)
    delta_dedup_values: list[str] = []
    base_targets: list[tuple[str, str, str]] = []
    base_delta_refs: list[str] = []
    total_rows = 0

    for name in sorted(item for item in snapshot.expected if item.endswith(".tsv")):
        table = read_tsv(snapshot, name)
        tables[name] = table
        fields, rows = table.fields, table.rows
        total_rows += len(rows)
        if "source" not in fields:
            raise ManifestError(f"TSV missing source column: {name}")
        if name in EXACT_SCHEMAS and fields != EXACT_SCHEMAS[name]:
            raise ManifestError(f"exact TSV schema changed: {name}")
        unknown_keys = {
            field for field in fields if field.endswith("_key")
        } - OWNED_KEY_COLUMNS - REFERENCE_KEY_COLUMNS
        if unknown_keys:
            raise ManifestError(f"unclassified key namespace: {name}: {sorted(unknown_keys)}")
        sources = Counter(row["source"] for row in rows)
        if not sources or not set(sources).issubset(ALLOWED_SOURCES):
            raise ManifestError(f"invalid/empty TSV source layer: {name}: {dict(sources)}")
        if name in EXACT_SOURCE_SETS and set(sources) != EXACT_SOURCE_SETS[name]:
            raise ManifestError(f"exact V4 evidence layer changed: {name}: {dict(sources)}")
        tuples = [tuple(row[field] for field in fields) for row in rows]
        if len(tuples) != len(set(tuples)):
            raise ManifestError(f"exact duplicate row within TSV: {name}")
        for line, (row, raw_line) in enumerate(zip(rows, table.raw_lines, strict=True), start=2):
            raw_occurrences[raw_line].append((name, line, row))
            for action_column in ("action", "delta_action"):
                action = row.get(action_column, "").upper()
                if any(token in action for token in ("UNCHANGED", "COPIED")):
                    raise ManifestError(f"duplicative delta action: {name}:{line}:{action}")
            if {"base_file", "base_line", "base_row_key"}.issubset(fields):
                target = (row["base_file"], row["base_line"], row["base_row_key"])
                populated = [value not in {"", "N/A"} for value in target]
                if any(populated) and not all(populated):
                    raise ManifestError(f"partial base target: {name}:{line}")
                if all(populated):
                    base_targets.append(target)
            reference = row.get("base_delta_key")
            if reference not in {None, "", "N/A"}:
                if re.fullmatch(r"[0-9a-f]{64}", reference) is None:
                    raise ManifestError(f"malformed base_delta_key: {name}:{line}")
                base_delta_refs.append(reference)
        for key in OWNED_KEY_COLUMNS:
            if key not in fields:
                continue
            values = [row[key] for row in rows]
            # Historical dedup/root namespaces are canonical strings, not all
            # SHA-256 values (A6 includes a hash|VA identity).  Ownership is
            # defined by non-empty, non-N/A exact strings plus global collision
            # checks; the overlay delta/base-reference hashes are constrained by
            # their component builders.
            if any(value in {"", "N/A"} for value in values):
                raise ManifestError(f"empty/N-A owned {key}: {name}")
            if len(values) != len(set(values)):
                raise ManifestError(f"duplicate local {key}: {name}")
            if key in {"delta_key", "dedup_key"}:
                delta_dedup_values.extend(values)
            for row in rows:
                value = row[key]
                prior_namespace = cross_namespace.setdefault(value, key)
                if prior_namespace != key:
                    raise ManifestError(f"cross-namespace key collision: {prior_namespace}/{key}:{value}")
                owners[(key, value)].append((name, row))
        census[name] = (len(rows), sources)

    if len(tables) != 46:
        raise ManifestError(f"global TSV file census changed: {len(tables)} != 46")
    if total_rows != 21_918:
        raise ManifestError(f"global TSV data-row census changed: {total_rows}")
    if len(delta_dedup_values) != 3_404 or len(set(delta_dedup_values)) != 3_404:
        raise ManifestError(
            f"global delta_key+dedup_key union changed/collided: "
            f"occurrences={len(delta_dedup_values)} unique={len(set(delta_dedup_values))}"
        )
    if len(base_targets) != 576 or len(set(base_targets)) != 576:
        raise ManifestError(
            f"full base-target census/collision changed: occurrences={len(base_targets)} "
            f"unique={len(set(base_targets))}"
        )
    if len(base_delta_refs) != 69 or len(set(base_delta_refs)) != 69:
        raise ManifestError(
            f"base_delta_key reference census/collision changed: occurrences={len(base_delta_refs)} "
            f"unique={len(set(base_delta_refs))}"
        )
    delta_values = {
        value for (key, value) in owners if key == "delta_key"
    }
    status_values = {
        value for (key, value) in owners if key == "status_key"
    }
    historical_refs = set(base_delta_refs) - delta_values
    if historical_refs != EXPECTED_HISTORICAL_STATUS_BASE_REFS or not historical_refs <= status_values:
        raise ManifestError(f"historical status-key base references changed: {sorted(historical_refs)}")

    for (key, value), occurrences in owners.items():
        if len(occurrences) == 1:
            continue
        files = [name for name, _row in occurrences]
        if (
            key != "status_key"
            or len(files) not in {2, 3}
            or len(files) != len(set(files))
            or not set(files) <= set(STATUS_FILES)
            or any(
                row.get("row_semantics") != DERIVED_STATUS_SEMANTICS
                or row.get("source") != "IMAGE"
                for _name, row in occurrences
            )
            or any(
                normalise_status_reference(row) != normalise_status_reference(occurrences[0][1])
                for _name, row in occurrences[1:]
            )
        ):
            raise ManifestError(f"unauthorised global {key} duplicate: {value}:{files}")

    status_multiplicity = Counter(
        len(occurrences) for (key, _value), occurrences in owners.items() if key == "status_key"
    )
    if status_multiplicity != Counter({3: 92, 2: 18, 1: 24}):
        raise ManifestError(f"historical status-key multiplicity changed: {dict(status_multiplicity)}")

    repeated = {line: items for line, items in raw_occurrences.items() if len(items) > 1}
    repeated_occurrences = sum(len(items) for items in repeated.values())
    repeated_extras = sum(len(items) - 1 for items in repeated.values())
    if (len(repeated), repeated_occurrences, repeated_extras) != (110, 312, 202):
        raise ManifestError(
            "cross-file exact-row census changed: "
            f"distinct={len(repeated)} occurrences={repeated_occurrences} extras={repeated_extras}"
        )
    topology = Counter(len(items) for items in repeated.values())
    if topology != Counter({3: 92, 2: 18}):
        raise ManifestError(f"cross-file status-row topology changed: {dict(topology)}")
    for line, occurrences in repeated.items():
        files = {name for name, _line, _row in occurrences}
        if not files <= set(STATUS_FILES) or len(files) != len(occurrences):
            raise ManifestError(f"cross-file exact fact row repeated outside status snapshots: {sorted(files)}")
        for name, physical_line, row in occurrences:
            if row.get("row_semantics") != DERIVED_STATUS_SEMANTICS or row.get("source") != "IMAGE":
                raise ManifestError(f"unlabelled repeated status reference: {name}:{physical_line}")
    status_line_sets = {
        name: set(tables[name].raw_lines) for name in STATUS_FILES
    }
    intersections = {
        (STATUS_FILES[0], STATUS_FILES[1]): len(status_line_sets[STATUS_FILES[0]] & status_line_sets[STATUS_FILES[1]]),
        (STATUS_FILES[1], STATUS_FILES[2]): len(status_line_sets[STATUS_FILES[1]] & status_line_sets[STATUS_FILES[2]]),
        (STATUS_FILES[0], STATUS_FILES[2]): len(status_line_sets[STATUS_FILES[0]] & status_line_sets[STATUS_FILES[2]]),
    }
    expected_intersections = {
        (STATUS_FILES[0], STATUS_FILES[1]): 95,
        (STATUS_FILES[1], STATUS_FILES[2]): 107,
        (STATUS_FILES[0], STATUS_FILES[2]): 92,
    }
    if intersections != expected_intersections:
        raise ManifestError(f"derived-status pair intersections changed: {intersections}")

    # Bounded semantic-identity guard for the one historical A2 ADD schema.
    # It deliberately does not invent identity rules for removals, changes,
    # priorities, status rows, or unrelated tabular schemas.
    add_rows = [
        (name, row)
        for name, table in tables.items()
        for row in table.rows
        if row.get("action", "").startswith("ADD_")
    ]
    add_files = Counter(name for name, _row in add_rows)
    add_actions = Counter(row["action"] for _name, row in add_rows)
    if add_files != Counter({"PF_A2_SERIALIZER_SLOT34_DELTA.tsv": 2_194}):
        raise ManifestError(f"bounded A2 ADD file/census changed: {dict(add_files)}")
    if add_actions != Counter({
        "ADD_CORRECTED_SLOT34_ROW": 2_059,
        "ADD_ANALYSIS_BLOCKER_ROW": 79,
        "ADD_AMBIGUOUS_CANDIDATE_ROW": 56,
    }):
        raise ManifestError(f"bounded A2 ADD action census changed: {dict(add_actions)}")
    semantic_columns = (
        "message", "schema_variant", "direction(W/R)", "new_order", "new_tag",
        "new_field_offset", "new_len", "new_gate_condition",
    )
    slot_table = tables["PF_A2_SERIALIZER_SLOT34_DELTA.tsv"]
    if not set(semantic_columns).issubset(slot_table.fields):
        raise ManifestError("bounded A2 ADD semantic tuple columns changed")
    semantic_counts = Counter(
        tuple(row[column] for column in semantic_columns) for _name, row in add_rows
    )
    semantic_duplicate_groups = sum(count > 1 for count in semantic_counts.values())
    if len(semantic_counts) != 2_194 or semantic_duplicate_groups != 0:
        raise ManifestError(
            "bounded A2 ADD semantic duplicate detected: "
            f"facts={len(add_rows)} unique={len(semantic_counts)} "
            f"duplicate_groups={semantic_duplicate_groups}"
        )
    classmap_values = [
        row["classmap_key"] for row in tables["PF_STATIC_TYPE_INFO_CLASSMAP.tsv"].rows
    ]
    if len(classmap_values) != 4 or len(set(classmap_values)) != 4:
        raise ManifestError("classmap key census/collision changed")

    return TsvAudit(
        tables=MappingProxyType(tables), census=MappingProxyType(census),
        delta_dedup_count=len(delta_dedup_values), base_target_count=len(base_targets),
        base_delta_ref_count=len(base_delta_refs), repeated_lines=len(repeated),
        repeated_occurrences=repeated_occurrences, repeated_extras=repeated_extras,
        inherited_v4_rows=intersections[(STATUS_FILES[1], STATUS_FILES[2])],
        total_rows=total_rows,
        a2_add_semantic_count=len(add_rows),
        a2_add_semantic_duplicate_groups=semantic_duplicate_groups,
    )


def raw_byte_guard(name: str, text: str) -> None:
    if any(pattern.search(text) for pattern in RAW_BYTE_PATTERNS):
        raise ManifestError(f"raw/opaque byte representation in output: {name}")


def audit_no_raw_proprietary(snapshot: Snapshot) -> None:
    forbidden_columns = {
        "raw_bytes", "payload", "payload_hex", "packet_hex", "hexdump",
        "field_value", "byte_value", "raw_base64", "payload_base64",
    }
    guarded: set[str] = {CANONICAL_A5_TSV}
    for name in sorted(item for item in snapshot.expected if item.endswith(".tsv")):
        table = read_tsv(snapshot, name)
        if {row["source"] for row in table.rows} & {"CAPTURE", "DUMP"}:
            overlap = forbidden_columns & {field.lower() for field in table.fields}
            if overlap:
                raise ManifestError(f"raw proprietary output column: {name}:{sorted(overlap)}")
            guarded.add(name)
    guarded.update(name for name in V4_COMPONENT_FILES if name.endswith(".md"))
    guarded.add(INDEX_PATH.name)
    for name in sorted(guarded & set(snapshot.files)):
        raw_byte_guard(name, snapshot.text(name))
    forbidden_suffixes = {".dmp", ".bin", ".cap", ".pcap", ".pcapng"}
    if {Path(name).suffix.lower() for name in snapshot.expected} & forbidden_suffixes:
        raise ManifestError("proprietary binary entered output namespace")


def audit_exact_duplicate_files(files: Mapping[str, bytes]) -> int:
    digest_groups: dict[tuple[int, str], list[str]] = defaultdict(list)
    for name, data in files.items():
        digest_groups[(len(data), sha256_bytes(data))].append(name)
    duplicates: list[list[str]] = []
    for names in digest_groups.values():
        if len(names) > 1:
            first = files[names[0]]
            equal = [name for name in names if files[name] == first]
            if len(equal) > 1:
                duplicates.append(equal)
    if duplicates:
        raise ManifestError(f"exact duplicate artifact files: {duplicates}")
    return 0


def run_component_checks() -> None:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for name, arguments, marker in COMPONENT_CHECKS:
        result = subprocess.run(
            [sys.executable, "-B", str(OUT_DIR / name), *arguments],
            cwd=OUT_DIR,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=900,
            check=False,
        )
        try:
            output = result.stdout.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise ManifestError(f"non-UTF-8 component output: {name}") from exc
        if result.returncode != 0 or marker not in output:
            tail = "\n".join(output.splitlines()[-20:])
            raise ManifestError(
                f"required component --check failed: {name}: rc={result.returncode}\n{tail}"
            )
        print(f"component integrity PASS: {name}", flush=True)


def audit_static_identity(tsv: TsvAudit) -> None:
    classmap = tsv.tables["PF_STATIC_TYPE_INFO_CLASSMAP.tsv"].rows
    identities = {
        (row["registry_name"], row["class_name"], row["identity_kind"], row["vtable_va"])
        for row in classmap
    }
    expected = {
        ("ItemAttr", "ItemAttr", "EXACT_REGISTRY_CLASS", "0x00F0EBB0"),
        ("ItemAttr", "StallItem", "POLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER", "0x00F4A188"),
        ("VitalData", "VitalData", "EXACT_REGISTRY_CLASS", "0x00F0B930"),
        ("VitalData", "Channel_MessageVtial", "POLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER", "0x00F375FC"),
    }
    if identities != expected:
        raise ManifestError(f"static identity variants collapsed/drifted: {identities}")
    a1 = tsv.tables["PF_A1_STATIC_TYPE_INFO_DELTA.tsv"].rows
    if len(a1) != 2 or {row["registry_name"] for row in a1} != {"ItemAttr", "VitalData"}:
        raise ManifestError("A1 static identity row set changed")
    if any(
        row["action"] != "CHANGED_STATIC_TYPE_IDENTITY"
        or row["canonical_a2_action"] != "NO_CHANGE"
        or row["source"] != "IMAGE"
        for row in a1
    ):
        raise ManifestError("static A1 identity attempted to activate/copy canonical A2")
    by_name = {row["registry_name"]: row for row in a1}
    if (
        by_name["ItemAttr"]["serializer_selection"] != "WITHHELD_NOT_SINGLETON"
        or by_name["ItemAttr"]["new_base_class_vtable_va"] != "0x00F0EBB0"
        or by_name["VitalData"]["serializer_identity_status"] != "UNKNOWN"
        or by_name["VitalData"]["serializer_selection"] != "WITHHELD"
        or by_name["VitalData"]["new_base_class_vtable_va"] != "0x00F0B930"
    ):
        raise ManifestError("ItemAttr/VitalData serializer-withholding boundary changed")
    priority = tsv.tables["PF_PRIORITY_STATIC_TYPE_INFO_DELTA.tsv"].rows
    priority_by_name = {row["message"]: row for row in priority}
    if len(priority) != 2 or set(priority_by_name) != {"ItemAttr", "VitalData"}:
        raise ManifestError("static identity priority row set changed")
    if any(row["new_structural_status"] != "OPEN" for row in priority):
        raise ManifestError("static identity unexpectedly activated a structural closure")
    if priority_by_name["VitalData"]["new_registry_identity_proof_kind"] != "EXACT_BASE_VTABLE_SERIALIZER_OPEN":
        raise ManifestError("VitalData serializer-open ceiling changed")
    for name in ("PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv", "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv"):
        if any(row["message"] in {"ItemAttr", "VitalData"} for row in tsv.tables[name].rows):
            raise ManifestError("static identity improperly activated a V4 A2 row")


def audit_composition_references(tsv: TsvAudit) -> None:
    rows = tsv.tables["PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv"].rows
    actions = Counter(row["action"] for row in rows)
    if actions != Counter({"CHANGED": 4, "REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW": 2}):
        raise ManifestError(f"composition action census changed: {dict(actions)}")
    changed = [row for row in rows if row["action"] == "CHANGED"]
    if any(
        row["new_tag"] != "STATIC_EMBEDDED_CHILD_REF"
        or row["child_receiver"] != "this+0x18"
        or row["child_slot"] != "+0x34"
        or row["new_gate_condition"] != "DIRECTION_FORWARDED"
        for row in changed
    ):
        raise ManifestError("composition reference-only contract changed")
    if Counter((row["child_message"], row["direction(W/R)"]) for row in changed) != Counter({
        ("DailyActivityState", "R"): 1, ("DailyActivityState", "W"): 1,
        ("CGuildStorageAttr", "R"): 1, ("CGuildStorageAttr", "W"): 1,
    }):
        raise ManifestError("composition child/direction reference identities changed")
    priority_rows = tsv.tables["PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv"].rows
    if len(priority_rows) != 2 or any(row["action"] != "CHANGED" for row in priority_rows):
        raise ManifestError("composition priority-reference census changed")
    for row in priority_rows:
        dependency = row["child_priority_file"]
        expected_hash = row["child_priority_file_sha256"]
        if dependency not in tsv.tables or sha256_bytes((OUT_DIR / dependency).read_bytes()) != expected_hash:
            raise ManifestError(f"composition child priority hash binding changed: {dependency}")
        matches = [
            item for item in tsv.tables[dependency].rows
            if item.get("delta_key") == row["child_priority_delta_key"]
        ]
        if len(matches) != 1:
            raise ManifestError(f"composition child priority reference is not unique: {dependency}")


def audit_effective_outputs(snapshot: Snapshot, tsv: TsvAudit) -> dict[str, int]:
    status_hash = REVIEWED_V4_PINS["pf_build_v4_effective_status.py"]
    status = load_local_module(
        "_pf_v4_status_" + status_hash[:16], OUT_DIR / "pf_build_v4_effective_status.py", status_hash
    )
    outputs, measured, groups, inherited = status.build()
    by_name = {path.name: data for path, data in outputs.items()}
    for name in (
        "PF_A1_STATIC_TYPE_INFO_DELTA.tsv", "PF_PRIORITY_STATIC_TYPE_INFO_DELTA.tsv",
        "PF_V4_P1_OPEN.tsv", "PF_V4_EFFECTIVE_STATUS.md",
    ):
        if by_name.get(name) != snapshot.files[name]:
            raise ManifestError(f"actual V4 status output differs from full re-derivation: {name}")
    expected_measured = {
        "rows": 8_657, "unknown": 3_963, "generic": 1_312, "direct_invalid": 881,
        "a3": 4_081, "plan_applicable": 624, "plan_static_open": 368,
        "plan_not_applied": 46,
    }
    if any(measured.get(key) != value for key, value in expected_measured.items()):
        raise ManifestError(f"V4 effective status census changed: {measured}")
    if dict(groups) != {
        "CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED": 14,
        "DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED": 79,
        "OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED": 7,
        "REGISTRY_IDENTITY_UNRESOLVED": 10,
    }:
        raise ManifestError(f"V4 P1 blocker groups changed: {dict(groups)}")
    if inherited != 107 or inherited != tsv.inherited_v4_rows:
        raise ManifestError(f"V3->V4 derived reference census changed: {inherited}")

    validator_hash = REVIEWED_V4_PINS["pf_validate_v4_effective_capture.py"]
    validator = load_local_module(
        "_pf_v4_validator_" + validator_hash[:16],
        OUT_DIR / "pf_validate_v4_effective_capture.py", validator_hash,
    )
    validator.verify_classmap_boundary(OUT_DIR)
    registry, stored, candidates, _counts, references, details = validator.apply_daily_and_composition(OUT_DIR)
    candidate_counts = {
        key: len(rows) for key, rows in candidates.items() if key[0] == "ItemAttr"
    }
    if candidate_counts != EXPECTED_ITEM_VARIANTS:
        raise ManifestError(f"ItemAttr direction/variant alternatives collapsed: {candidate_counts}")
    logical, expansion = validator.expand_logical_references(stored, references)
    stored_rows = validator.total_rows(stored)
    stored_unknown = validator.total_unknown(stored)
    logical_rows = validator.total_rows(logical)
    logical_unknown = validator.total_unknown(logical)
    if (stored_rows, stored_unknown, logical_rows, logical_unknown) != (8_657, 3_963, 8_721, 3_999):
        raise ManifestError(
            "stored/logical reference expansion census changed: "
            f"{stored_rows}/{stored_unknown}/{logical_rows}/{logical_unknown}"
        )
    expected_details = {
        "daily_removed": 12, "composition_changed": 4, "composition_removed": 2,
        "stored_rows": 8_657, "stored_unknown": 3_963, "stored_numeric": 4_081,
    }
    if details != expected_details or len(references) != 4 or len(expansion) != 4:
        raise ManifestError("embedded-child references were copied, dropped, or multiplied")
    _id_to_name, plans = validator.v2.build_schema_plans(registry, logical, candidates)
    plan_census = dict(Counter(plan.state for plan in plans.values()))
    if plan_census != EXPECTED_PLAN_CENSUS:
        raise ManifestError(f"logical validation plan census changed: {plan_census}")
    audit_static_identity(tsv)
    audit_composition_references(tsv)
    return {
        **expected_measured,
        "stored_rows": stored_rows,
        "stored_unknown": stored_unknown,
        "logical_rows": logical_rows,
        "logical_unknown": logical_unknown,
        "composition_references": len(references),
        "composition_removals": 2,
        "inherited_v4": inherited,
    }


def audit_a5(snapshot: Snapshot, tsv: TsvAudit) -> dict[str, int]:
    versioned = sorted(
        name for name in snapshot.expected if re.fullmatch(r"PF_V\d+_FIELD_VALIDATION\.tsv", name)
    )
    if versioned != [CANONICAL_A5_TSV]:
        raise ManifestError(f"versioned A5 TSV singleton changed: {versioned}")
    if sha256_bytes(snapshot.files[CANONICAL_A5_TSV]) != CANONICAL_A5_SHA256:
        raise ManifestError("canonical V2 A5 TSV identity changed")
    rows = tsv.tables[CANONICAL_A5_TSV].rows
    points: set[tuple[str, str, str, str]] = set()
    locations: set[tuple[str, str, str]] = set()
    for row in rows:
        for item in row["mismatch_field_identity_reason_count"].split(" | "):
            if item in {"", "NONE"}:
                continue
            parts = item.rsplit("~", 2)
            if len(parts) != 3 or not parts[2].isdigit() or int(parts[2]) <= 0:
                raise ManifestError("malformed A5 mismatch identity/reason/count")
            identity, reason, _count = parts
            location = (row["message"], row["direction(W/R)"], identity)
            point = (*location, reason)
            if point in points:
                raise ManifestError("duplicate A5 mismatch identity/reason")
            locations.add(location)
            points.add(point)
    measured = {
        "rows": len(rows),
        "parse_success": sum(int(row["parse_success_instances"]) for row in rows),
        "static_open": sum(int(row["static_open_instances"]) for row in rows),
        "schema_not_applied": sum(int(row["schema_not_applied_instances"]) for row in rows),
        "mismatch": sum(int(row["mismatch_instances"]) for row in rows),
        "mismatch_points": len(points),
        "field_locations": len(locations),
    }
    if measured != EXPECTED_A5:
        raise ManifestError(f"A5 measured census changed: {measured}")
    report = snapshot.text("PF_V4_FIELD_VALIDATION.md")
    snippets = (
        "386 mismatch instances at 3 field locations and 4 field+reason points",
        "stored/reference A2 rows=8657", "validation rows=8721",
        "zero observations for all 8 V4-touched message/direction keys",
        "no `PF_V4_FIELD_VALIDATION.tsv`",
    )
    if any(snippet not in report for snippet in snippets):
        raise ManifestError("V4 A5 report lost a required red/reference-only control")
    return measured


CLAIM_LABELS = (
    "[MEASURED][CAPTURE]",
    "[MEASURED][IMAGE]",
    "[MEASURED][OUTPUT-AUDIT]",
    "[PROPOSED][LOCAL]",
    "[DECLARED-SCOPE]",
)


def claim_label_census(name: str, text: str, *, first_label: str) -> Counter[str]:
    census: Counter[str] = Counter()
    actionable = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        content = re.sub(r"^(?:#{1,6}|[-*+]|\d+\.)\s+", "", stripped)
        labels = [label for label in CLAIM_LABELS if label in content]
        if len(labels) != 1 or not content.startswith(labels[0]):
            raise ManifestError(
                f"unlabelled/mixed actionable V4 claim: {name}:{line_number}:{stripped}"
            )
        census[labels[0]] += 1
        actionable += 1
    first = text.splitlines()[0]
    first_content = re.sub(r"^(?:#{1,6}|[-*+]|\d+\.)\s+", "", first.strip())
    if not first_content.startswith(first_label):
        raise ManifestError(f"opening V4 claim has wrong evidence label: {name}")
    if actionable != sum(census.values()) or set(census) != set(CLAIM_LABELS):
        raise ManifestError(f"V4 claim-label layer census incomplete: {name}:{dict(census)}")
    return census


def build_handoff(audit: Audit) -> bytes:
    a5, effective, tsv = audit.a5, audit.effective, audit.tsv
    lines = [
        f"# [MEASURED][CAPTURE] 🔴 A5 ยัง mismatch {a5['mismatch']} instances / {a5['field_locations']} field locations / {a5['mismatch_points']} field+reason points",
        "",
        "[MEASURED][IMAGE] V4 เป็น local IMAGE-static overlay ต่อจาก V3; full pinned V1→V2→V3→V4 overlay replay ถูก derive ใหม่ครบและเทียบผลลัพธ์แบบ byte-exact.",
        "",
        "[MEASURED][CAPTURE] CAPTURE replay ยังคงจุดแดงเดิมและไม่ถูก rewrite เป็น IMAGE fact; conformance strict gate ยังต้องล้มเหลวที่ mismatch ชุดนี้.",
        "",
        "## [MEASURED][IMAGE] V3 → V4 ที่เปลี่ยนจริง",
        "",
        "- [MEASURED][IMAGE] DailyActivityState ลบ non-wire UNKNOWN 12 แถว (6 R + 6 W); Priority 3 ปิดเพิ่ม 1 message.",
        "- [MEASURED][IMAGE] embedded-child composition ปล่อย 4 reference rows และ 2 removals เท่านั้น; ไม่ copy 64 logical child rows ลง A2. ActorActivity_UpdateDailyActivityStateVital ปิดเพิ่ม 1 P1; DBSS_GuildStorageInitialVital ยัง OPEN.",
        "- [MEASURED][IMAGE] static type identity ยืนยัน ItemAttr/VitalData base vtable และ retained derived class แต่เพิ่ม A2 = 0, closure = 0; serializer selection ของทั้งคู่ยัง withheld ตามขอบเขตด้านล่าง.",
        "- [MEASURED][IMAGE] Full pinned overlay replay วัด P1 255/365 CLOSED, P2 8/16, P3 71/138, overall 334/519; P1 OPEN 110.",
        f"- [MEASURED][IMAGE] canonical stored/reference A2 = {effective['stored_rows']:,}; logical validation-only expansion = {effective['logical_rows']:,}. expanded child fields อยู่ในหน่วยความจำเท่านั้น.",
        "",
        "## [MEASURED][OUTPUT-AUDIT] Duplicate accounting — อะไรซ้ำได้และซ้ำไม่ได้",
        "",
        f"- [MEASURED][OUTPUT-AUDIT] Full namespace census = 121 files / 46 TSV / {tsv.total_rows:,} TSV data rows; exact duplicate files = 0; exact duplicate rows ภายใน TSV = 0.",
        f"- [MEASURED][OUTPUT-AUDIT] `delta_key` + `dedup_key` = {tsv.delta_dedup_count:,} occurrences / {tsv.delta_dedup_count:,} unique; full `(base_file,base_line,base_row_key)` = {tsv.base_target_count} / {tsv.base_target_count} unique; non-N/A `base_delta_key` references = {tsv.base_delta_ref_count} / {tsv.base_delta_ref_count} unique; classmap keys = 4.",
        f"- [MEASURED][OUTPUT-AUDIT] raw row ที่ซ้ำข้ามไฟล์มีเฉพาะ derived status snapshots: {tsv.repeated_lines} distinct / {tsv.repeated_occurrences} occurrences / {tsv.repeated_extras} extras. V2∩V3=95, V3∩V4=107, V2∩V4=92; ทุกแถวติด `NOT_A_NEW_EVIDENCE_ROW` จึงเป็น historical reference ไม่ใช่ fact row ใหม่.",
        f"- [MEASURED][OUTPUT-AUDIT] Bounded A2 ADD semantic census ใช้ tuple `(message,schema_variant,direction,new_order,new_tag,new_field_offset,new_len,new_gate_condition)`: {tsv.a2_add_semantic_count:,}/{tsv.a2_add_semantic_count:,} unique, duplicate groups {tsv.a2_add_semantic_duplicate_groups}. ขอบเขตนี้ครอบเฉพาะ `PF_A2_SERIALIZER_SLOT34_DELTA.tsv` และไม่สร้าง universal semantic identity ให้ TSV schema อื่น; CHANGED/REMOVE overlays ยังใช้ full base-target uniqueness ด้านบน.",
        "- [MEASURED][OUTPUT-AUDIT] A5 TSV มี canonical singleton เดียวคือ `PF_V2_FIELD_VALIDATION.tsv`; V3/V4 มีรายงาน MD แต่ไม่มี TSV สำเนา.",
        "",
        "## [MEASURED][IMAGE] Composition และ schema boundary",
        "",
        "- [MEASURED][IMAGE] composition = 4 CHANGED references + 2 directionally-impossible removals; `ADD`, `UNCHANGED`, `COPIED` = 0 และ materialized child fields = 0.",
        "- [MEASURED][IMAGE] ItemAttr alternatives คงแยก: `0x00F0EBB0` = 13 R + 13 W และ `0x00F4A188` = 15 R + 15 W. `canonical_a2_action=NO_CHANGE`; ไม่มีการเลือก/merge 26-row กับ 30-row schema.",
        "- [MEASURED][IMAGE] VitalData base `0x00F0B930` และ Channel_MessageVtial derived `0x00F375FC` เป็น identity proof เท่านั้น; serializer ยัง UNKNOWN/WITHHELD และไม่ activate A2/A5 schema.",
        "- [MEASURED][IMAGE] A5 logical plan = 624 APPLICABLE / 368 STATIC_OPEN / 46 SCHEMA_NOT_APPLIED.",
        "- [MEASURED][CAPTURE] 8 V4-touched message+direction keys มี capture observations = 0 ตาม pinned corpus; ผลศูนย์นี้ไม่ขยายไปยัง session อื่น.",
        "",
        "## [PROPOSED][LOCAL] ลำดับใช้ไฟล์",
        "",
        "1. [PROPOSED][LOCAL] อ่าน `PF_V4_MANIFEST.md` สำหรับ commit marker, exact namespace/hashes และ executable guards.",
        "2. [PROPOSED][LOCAL] อ่าน `PF_V4_EFFECTIVE_STATUS.md` + `PF_V4_P1_OPEN.tsv` สำหรับ current IMAGE-static derived status.",
        "3. [PROPOSED][LOCAL] อ่าน `PF_V4_FIELD_VALIDATION.md` + canonical `PF_V2_FIELD_VALIDATION.tsv` สำหรับ CAPTURE replay และ red mismatch.",
        "4. [PROPOSED][LOCAL] Compose Daily/composition/classmap outputs ตาม action/reference; ห้าม append TSV ตรง ๆ.",
        "5. [PROPOSED][LOCAL] ใช้ V3 เป็น immutable predecessor; V4 index ฝัง V3 index เดิมครบทุกไบต์หลัง marker.",
        "",
        "[PROPOSED][LOCAL] Reproduce ด้วย `py -3 -B pf_build_v4_manifest.py --check`; คำสั่งนี้เรียก component `--check` ทั้ง 5 ตัวและตรวจ image hash ก่อน/หลัง, exact bytes, duplicate topology, A2 ADD semantic tuple และ canonical A5 singleton.",
        "",
        "[DECLARED-SCOPE] Local-only ใต้ `pf_bridge\\external`; ไม่มี server/client runtime, workflow, queue, lease, Git หรือ GameClient file ถูกแก้หรือรัน และไม่มี raw dump/capture bytes ถูกเผยแพร่.",
        "",
    ]
    data = "\n".join(lines).encode("utf-8")
    claim_label_census(
        HANDOFF_PATH.name, data.decode("utf-8"), first_label="[MEASURED][CAPTURE]"
    )
    raw_byte_guard(HANDOFF_PATH.name, data.decode("utf-8"))
    return data


def build_index(audit: Audit) -> bytes:
    a5, effective, tsv = audit.a5, audit.effective, audit.tsv
    prefix_lines = [
        '# [PROPOSED][LOCAL] 🔴 อ่านไฟล์นี้ก่อนจะ "ไปถอด" อะไรใหม่จากไบนารี',
        "",
        "## [MEASURED][IMAGE] 🔴 V4 checkpoint ปัจจุบัน — duplicate-safe reference composition",
        "",
        f"[MEASURED][CAPTURE] **A5 ยัง mismatch {a5['mismatch']} instances / {a5['field_locations']} field locations / {a5['mismatch_points']} field+reason points**; CAPTURE result นี้ไม่ถูก rewrite เป็น IMAGE fact.",
        "",
        "[MEASURED][IMAGE] Full pinned V1→V2→V3→V4 overlay replay ผ่านและ current IMAGE-static status คือ P1 255/365 CLOSED, OPEN 110.",
        "",
        "[PROPOSED][LOCAL] ลำดับอ่าน:",
        "",
        "1. [PROPOSED][LOCAL] `PF_V4_MANIFEST.md` — commit marker, hashes และ executable duplicate guards",
        "2. [PROPOSED][LOCAL] `PF_V4_HANDOFF.md` — V3→V4 delta และกฎ reference-only composition",
        "3. [PROPOSED][LOCAL] `PF_V4_FIELD_VALIDATION.md` + canonical `PF_V2_FIELD_VALIDATION.tsv` — red CAPTURE replay; ไม่มี V4 TSV สำเนา",
        "4. [PROPOSED][LOCAL] `PF_V4_EFFECTIVE_STATUS.md` / `PF_V4_P1_OPEN.tsv` — current IMAGE-static derived status",
        "5. [PROPOSED][LOCAL] Daily / embedded-child / static-type artifacts — compose ตาม action; ห้าม append ทุก TSV ตรง ๆ",
        "",
        f"[MEASURED][IMAGE] V4 stored/reference A2 {effective['stored_rows']:,} rows; logical validation-only {effective['logical_rows']:,}. Composition มี 4 refs + 2 removals และไม่ copy child fields.",
        "",
        f"[MEASURED][OUTPUT-AUDIT] Full namespace census = 121 files / 46 TSV / {tsv.total_rows:,} TSV data rows; exact files 0, within-TSV rows 0, delta+dedup keys {tsv.delta_dedup_count:,} unique, base targets {tsv.base_target_count} unique. Status snapshots ซ้ำโดยตั้งใจ {tsv.repeated_lines} distinct/{tsv.repeated_occurrences} occurrences และทุกแถวเป็น `NOT_A_NEW_EVIDENCE_ROW`.",
        "",
        f"[MEASURED][OUTPUT-AUDIT] Bounded A2 ADD tuple `(message,schema_variant,direction,new_order,new_tag,new_field_offset,new_len,new_gate_condition)` = {tsv.a2_add_semantic_count:,}/{tsv.a2_add_semantic_count:,} unique, duplicate groups {tsv.a2_add_semantic_duplicate_groups}; guard นี้ไม่กำหนด universal identity ให้ schema อื่น.",
        "",
        "[MEASURED][IMAGE] ItemAttr 13R+13W และ 15R+15W คงเป็น alternatives; VitalData serializer ยัง withheld. Static identity ไม่ activate A2/A5.",
        "",
        "[DECLARED-SCOPE] Local-only ใต้ `pf_bridge\\external`; ไม่มี server/client runtime, workflow, queue, lease หรือ Git ถูกแก้/รัน.",
        "",
        "[PROPOSED][LOCAL] Reproduce ด้วย `py -3 -B pf_build_v4_manifest.py --check`.",
        "",
        "## [MEASURED][OUTPUT-AUDIT] 🔒 Frozen V3 index — ข้อความหลัง marker นี้คือ V3 index เดิมครบทุกไบต์",
        "",
    ]
    prefix_text = "\n".join(prefix_lines)
    claim_label_census(INDEX_PATH.name, prefix_text, first_label="[PROPOSED][LOCAL]")
    prefix = prefix_text.encode("utf-8") + V3_INDEX_MARKER + b"\n"
    data = prefix + audit.frozen_v3_index
    tail = data.split(V3_INDEX_MARKER + b"\n", 1)
    if len(tail) != 2 or tail[1] != audit.frozen_v3_index:
        raise ManifestError("V4 index did not embed complete V3 bytes verbatim after marker")
    if (len(tail[1]), sha256_bytes(tail[1])) != (V3_INDEX_SIZE, V3_INDEX_SHA256):
        raise ManifestError("embedded V3 index tail pin changed")
    raw_byte_guard(INDEX_PATH.name, data.decode("utf-8", errors="strict"))
    return data


def audit_all(
    *, allow_unpublished: bool, require_final: bool, transients: frozenset[str],
) -> Audit:
    snapshot = take_snapshot(allow_unpublished=allow_unpublished, transients=transients)
    frozen = verify_inputs(snapshot)
    for name in sorted(snapshot.files):
        snapshot.text(name)
    audit_exact_duplicate_files(snapshot.files)
    tsv = audit_tsvs(snapshot)
    audit_no_raw_proprietary(snapshot)
    run_component_checks()
    effective = audit_effective_outputs(snapshot, tsv)
    a5 = audit_a5(snapshot, tsv)
    provisional = Audit(snapshot, tsv, a5, effective, frozen, b"", b"")
    handoff = build_handoff(provisional)
    with_handoff = Audit(snapshot, tsv, a5, effective, frozen, handoff, b"")
    index = build_index(with_handoff)
    audit = Audit(snapshot, tsv, a5, effective, frozen, handoff, index)
    if require_final:
        if snapshot.files.get(HANDOFF_PATH.name) != handoff:
            raise ManifestError("PF_V4_HANDOFF.md differs byte-for-byte from derived handoff")
        if snapshot.files.get(INDEX_PATH.name) != index:
            raise ManifestError("00_SEARCH_HERE_FIRST.md differs byte-for-byte from derived V4 index")
        if MANIFEST_PATH.name not in snapshot.files:
            raise ManifestError("PF_V4_MANIFEST.md is absent")
    else:
        has_integration = HANDOFF_PATH.name in snapshot.files
        if has_integration:
            current_derivation = (
                snapshot.files[HANDOFF_PATH.name] == handoff
                and snapshot.files[INDEX_PATH.name] == index
            )
            authenticated_predecessor = all(
                (len(snapshot.files[name]), sha256_bytes(snapshot.files[name])) == pin
                for name, pin in PRIOR_V4_INTEGRATION_PINS.items()
            )
            if not current_derivation and not authenticated_predecessor:
                raise ManifestError(
                    "existing integration outputs are neither the current derivation "
                    "nor the exact authenticated predecessor checkpoint"
                )
        elif snapshot.files[INDEX_PATH.name] != frozen:
            raise ManifestError("unpublished integration does not retain exact V3 index")
    prospective = dict(snapshot.files)
    prospective[HANDOFF_PATH.name] = handoff
    prospective[INDEX_PATH.name] = index
    prospective.pop(MANIFEST_PATH.name, None)
    audit_exact_duplicate_files(prospective)
    assert_snapshot_current(snapshot, transients=transients)
    return audit


def artifact_bytes(audit: Audit, name: str) -> bytes:
    if name == HANDOFF_PATH.name:
        return audit.final_handoff
    if name == INDEX_PATH.name:
        return audit.final_index
    try:
        return audit.snapshot.files[name]
    except KeyError as exc:
        raise ManifestError(f"prospective artifact missing: {name}") from exc


def build_manifest(audit: Audit) -> bytes:
    a5, effective, tsv, snapshot = audit.a5, audit.effective, audit.tsv, audit.snapshot
    handoff_labels = claim_label_census(
        HANDOFF_PATH.name, audit.final_handoff.decode("utf-8"),
        first_label="[MEASURED][CAPTURE]",
    )
    index_prefix = audit.final_index.split(V3_INDEX_MARKER + b"\n", 1)[0].decode("utf-8")
    index_labels = claim_label_census(
        INDEX_PATH.name, index_prefix, first_label="[PROPOSED][LOCAL]",
    )
    label_text = lambda values: ", ".join(
        f"{label}={values[label]}" for label in CLAIM_LABELS
    )
    lines = [
        "# PF V4 final local manifest and duplicate audit",
        "",
        f"🔴 **A5 V4 ยัง mismatch {a5['mismatch']} instances / {a5['field_locations']} field locations / {a5['mismatch_points']} field+reason points**; canonical TSV ยังคงเป็น V2 และ conformance ยังแดง.",
        "",
        "## Measured integrity and duplicate audit",
        "",
        "- [MEASURED] artifact integrity/reproduction: `PASS`; capture conformance: `FAIL` (386 mismatches preserved)",
        "- [MEASURED] all five component `--check` gates passed; status and validation products were fully re-derived and byte-compared",
        "- [MEASURED] exact frozen V3 manifest namespace is preserved except the intentionally superseded search index; no directory, cache, lock, journal, or unknown transient is accepted",
        "- [MEASURED] client image size/SHA-256 matched before and after every complete audit and postcommit re-derivation",
        "- [MEASURED] Windows publication lock is a held CreateFileW CREATE_NEW handle with READ-only sharing; unlink/replace is denied until handle-owned disposition and close",
        "- [MEASURED] publication stages handoff/index/manifest, fsyncs PREPARED journal before replacement, installs manifest last, catches BaseException, verifies file identity during rollback, and retains foreign/uncertain state",
        "- [MEASURED] exact duplicate artifact files: `0`; exact duplicate rows within each TSV: `0`",
        f"- [MEASURED][OUTPUT-AUDIT] full namespace census: `121 files / 46 TSV / {tsv.total_rows} TSV data rows`",
        f"- [MEASURED] global delta_key+dedup_key: `{tsv.delta_dedup_count}` occurrences / `{tsv.delta_dedup_count}` unique; unauthorised collisions: `0`",
        f"- [MEASURED] full base targets: `{tsv.base_target_count}` occurrences / `{tsv.base_target_count}` unique; non-N/A base_delta_key references: `{tsv.base_delta_ref_count}` / `{tsv.base_delta_ref_count}` unique; classmap keys: `4`",
        f"- [MEASURED][OUTPUT-AUDIT] bounded A2 ADD semantic tuple `(message,schema_variant,direction,new_order,new_tag,new_field_offset,new_len,new_gate_condition)`: `{tsv.a2_add_semantic_count}/{tsv.a2_add_semantic_count}` unique; duplicate groups `{tsv.a2_add_semantic_duplicate_groups}`; applies only to PF_A2_SERIALIZER_SLOT34_DELTA.tsv, not unrelated schemas; CHANGED/REMOVE overlays retain the full base-target guard",
        f"- [MEASURED] allowed cross-file derived-status rows: `{tsv.repeated_lines}` distinct / `{tsv.repeated_occurrences}` occurrences / `{tsv.repeated_extras}` extras; V2∩V3=95, V3∩V4=107, V2∩V4=92",
        "- [MEASURED] every allowed repeated row is confined to V2/V3/V4 status snapshots and labelled DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW",
        f"- [MEASURED][OUTPUT-AUDIT] actionable-claim labels: handoff `{label_text(handoff_labels)}`; current V4 index prefix `{label_text(index_labels)}`; mixed/unlabelled claims `0`; frozen V3 tail excluded from relabelling",
        "- [MEASURED] canonical A5 schema/hash singleton is PF_V2_FIELD_VALIDATION.tsv; PF_V3_FIELD_VALIDATION.tsv and PF_V4_FIELD_VALIDATION.tsv are forbidden",
        "- [MEASURED] CAPTURE/DUMP source/schema and raw/opaque byte-text guards passed; proprietary binary outputs: `0`",
        "",
        "## Effective V4 checkpoint",
        "",
        "| measured item | result |",
        "|---|---:|",
        "| Priority 1 IMAGE-static | 255/365 CLOSED; 110 OPEN |",
        "| Priority 2 IMAGE-static | 8/16 CLOSED; 8 OPEN |",
        "| Priority 3 IMAGE-static | 71/138 CLOSED; 67 OPEN |",
        "| Overall IMAGE-static | 334/519 CLOSED; 185 OPEN |",
        f"| stored/reference canonical A2 | {effective['stored_rows']:,} rows; UNKNOWN {effective['stored_unknown']:,} |",
        f"| logical validation-only A2 | {effective['logical_rows']:,} rows; UNKNOWN {effective['logical_unknown']:,} |",
        "| embedded-child composition | 4 references + 2 removals; ADD/UNCHANGED/COPIED=0; materialized child fields=0 |",
        "| ItemAttr base alternative | 13 R + 13 W = 26 at 0x00F0EBB0 |",
        "| ItemAttr StallItem alternative | 15 R + 15 W = 30 at 0x00F4A188 |",
        "| static identity activation | A1 canonical_a2_action=NO_CHANGE; VitalData serializer WITHHELD; A2/A5 activation=0 |",
        "| schema plans | 624 applicable / 368 static-open / 46 not applied |",
        f"| A5 parse / static-open / not-applied / mismatch | {a5['parse_success']:,} / {a5['static_open']:,} / {a5['schema_not_applied']:,} / {a5['mismatch']:,} |",
        "",
        "## Immutable index composition",
        "",
        f"The V4 prefix is followed by a marker and the complete frozen V3 index bytes verbatim: bytes `{V3_INDEX_SIZE}`, SHA-256 `{V3_INDEX_SHA256}`. The tail is reconstructed only from the V3-pinned builder and checked independently; it is never inherited from mutable current index bytes.",
        "",
        "## Delivery scope",
        "",
        "[DECLARED-SCOPE] Local-only under pf_bridge/external. No server/client runtime, workflow, queue, lease, Git, or GameClient file is changed or run. No dump/capture raw bytes are emitted.",
        "",
        "## Artifact hashes",
        "",
        "PF_V4_MANIFEST.md does not hash itself. Every other row comes from the one audited byte snapshot, except the staged deterministic handoff/index bytes shown before commit.",
        "",
        f"- frozen V3 manifest SHA-256: `{V3_MANIFEST_SHA256}`",
        f"- complete embedded V3 index SHA-256: `{V3_INDEX_SHA256}`",
        f"- pinned client image: `{IMAGE_SIZE}` bytes / `{IMAGE_SHA256}`",
        "",
        "| file | bytes | SHA-256 | TSV rows | source counts |",
        "|---|---:|---|---:|---|",
    ]
    for name in sorted(snapshot.expected - {MANIFEST_PATH.name}):
        data = artifact_bytes(audit, name)
        if name in tsv.census:
            row_count, sources = tsv.census[name]
            row_text = str(row_count)
            source_text = ", ".join(f"{source}={sources[source]}" for source in sorted(sources))
        else:
            row_text, source_text = "—", "—"
        lines.append(
            f"| `{name}` | {len(data)} | `{sha256_bytes(data).upper()}` | {row_text} | `{source_text}` |"
        )
    lines.extend((
        "", "## Reproduction and red conformance gate", "",
        "Run `py -3 -B pf_build_v4_manifest.py --check`; it is read-only with respect to integration outputs and requires all five component --check gates. A stale lock/cache/journal/transaction path, namespace drift, hash drift, duplicate fact row, or reference/variant collapse fails closed.",
        "",
        f"A5 ordinary --check is integrity, not conformance success. `py -3 -B pf_validate_v4_effective_capture.py --check --fail-on-mismatch` must remain nonzero for {a5['mismatch']} mismatches / {a5['mismatch_points']} field+reason points.",
        "",
    ))
    data = "\n".join(lines).encode("utf-8")
    raw_byte_guard(MANIFEST_PATH.name, data.decode("utf-8"))
    return data


def prospective_files(audit: Audit, manifest: bytes) -> dict[str, bytes]:
    files = {
        name: artifact_bytes(audit, name)
        for name in audit.snapshot.expected - {MANIFEST_PATH.name}
    }
    files[MANIFEST_PATH.name] = manifest
    if set(files) != set(audit.snapshot.expected):
        raise ManifestError("prospective V4 namespace is incomplete")
    audit_exact_duplicate_files(files)
    return files


def verify_existing_integration_checkpoint(audit: Audit, manifest: bytes) -> None:
    snapshot = audit.snapshot
    if HANDOFF_PATH.name not in snapshot.files:
        return
    current = {
        HANDOFF_PATH.name: audit.final_handoff,
        INDEX_PATH.name: audit.final_index,
        MANIFEST_PATH.name: manifest,
    }
    if all(snapshot.files.get(name) == data for name, data in current.items()):
        return
    if all(
        name in snapshot.files
        and (len(snapshot.files[name]), sha256_bytes(snapshot.files[name])) == pin
        for name, pin in PRIOR_V4_INTEGRATION_PINS.items()
    ):
        return
    raise ManifestError(
        "complete integration namespace is neither the exact current checkpoint "
        "nor the authenticated predecessor triple"
    )


def windows_kernel32():
    if os.name != "nt":
        raise ManifestError("publication is unsupported outside Windows; --check remains read-only")
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.argtypes = (
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    )
    kernel32.CreateFileW.restype = wintypes.HANDLE
    kernel32.SetFileInformationByHandle.argtypes = (
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
    )
    kernel32.SetFileInformationByHandle.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


class FileDispositionInfo(ctypes.Structure):
    # FILE_DISPOSITION_INFO uses Win32 BOOLEAN (one byte), not BOOL.
    _fields_ = (("DeleteFile", ctypes.c_ubyte),)


def acquire_windows_lock(path: Path) -> HeldWindowsLock:
    import msvcrt

    kernel32 = windows_kernel32()
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    DELETE = 0x00010000
    FILE_SHARE_READ = 0x00000001
    CREATE_NEW = 1
    FILE_ATTRIBUTE_NORMAL = 0x00000080
    handle = kernel32.CreateFileW(
        str(path), GENERIC_READ | GENERIC_WRITE | DELETE, FILE_SHARE_READ,
        None, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, None,
    )
    invalid = ctypes.c_void_p(-1).value
    if handle == invalid:
        error = ctypes.get_last_error()
        if error in {80, 183}:
            raise ManifestError(f"active/stale publication lock exists: {path.name}; no takeover")
        raise ManifestError(f"CreateFileW publication lock failed: winerror={error}")
    try:
        fd = msvcrt.open_osfhandle(int(handle), os.O_RDWR | os.O_BINARY)
    except BaseException:
        kernel32.CloseHandle(handle)
        raise
    payload = json.dumps(
        {"pid": os.getpid(), "scope": "PF_V4_MANIFEST", "token": os.urandom(16).hex()},
        sort_keys=True,
    ).encode("ascii") + b"\n"
    try:
        os.write(fd, payload)
        os.fsync(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        if os.read(fd, len(payload) + 1) != payload:
            raise ManifestError("publication lock handle readback failed")
    except BaseException:
        os.close(fd)
        raise
    return HeldWindowsLock(fd=fd, payload=payload, path=path)


def assert_held_windows_lock(held: HeldWindowsLock) -> None:
    try:
        os.lseek(held.fd, 0, os.SEEK_SET)
        data = os.read(held.fd, len(held.payload) + 1)
    except OSError as exc:
        held.retain = True
        raise ManifestError("publication lock handle is no longer readable") from exc
    if data != held.payload:
        held.retain = True
        raise ManifestError("publication lock handle payload changed")


def release_windows_lock(held: HeldWindowsLock) -> None:
    import msvcrt

    if held.retain:
        os.close(held.fd)
        return
    assert_held_windows_lock(held)
    kernel32 = windows_kernel32()
    handle = msvcrt.get_osfhandle(held.fd)
    disposition = FileDispositionInfo(1)
    if not kernel32.SetFileInformationByHandle(
        handle, 4, ctypes.byref(disposition), ctypes.sizeof(disposition)
    ):
        error = ctypes.get_last_error()
        held.retain = True
        os.close(held.fd)
        raise ManifestError(f"handle-owned lock disposition failed: winerror={error}")
    os.close(held.fd)
    if held.path.exists():
        raise ManifestError("owned lock release did not remove pathname; foreign path retained")


@contextmanager
def exclusive_publication_lock() -> Iterator[HeldWindowsLock]:
    held = acquire_windows_lock(LOCK_PATH)
    try:
        yield held
    except BaseException:
        raise
    finally:
        release_windows_lock(held)


def windows_lock_self_test() -> None:
    if os.name != "nt":
        raise ManifestError("Windows held-handle lock self-test is unavailable")
    with tempfile.TemporaryDirectory(prefix="pf_v4_manifest_lock_selftest_") as raw:
        root = Path(raw)
        lock_path = root / "owned.lock"
        challenger = root / "challenger.lock"
        challenger.write_bytes(b"foreign\n")
        held = acquire_windows_lock(lock_path)
        try:
            try:
                lock_path.unlink()
            except OSError:
                pass
            else:
                held.retain = True
                raise ManifestError("held lock unexpectedly permitted pathname unlink")
            try:
                os.replace(challenger, lock_path)
            except OSError:
                pass
            else:
                held.retain = True
                raise ManifestError("held lock unexpectedly permitted pathname replacement")
            assert_held_windows_lock(held)
            if challenger.read_bytes() != b"foreign\n":
                held.retain = True
                raise ManifestError("failed replacement changed foreign challenger")
        finally:
            release_windows_lock(held)
        if lock_path.exists() or challenger.read_bytes() != b"foreign\n":
            raise ManifestError("handle-owned release self-test failed")
        stale = root / "stale.lock"
        stale.write_bytes(b"stale\n")
        try:
            acquire_windows_lock(stale)
        except ManifestError:
            pass
        else:
            raise ManifestError("CREATE_NEW lock accepted a stale/foreign pathname")


def write_exclusive(path: Path, data: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_BINARY, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def append_journal(path: Path, event: Mapping[str, object]) -> None:
    with path.open("ab") as handle:
        handle.write(json.dumps(event, sort_keys=True).encode("ascii") + b"\n")
        handle.flush()
        os.fsync(handle.fileno())


def cleanup_transaction(directory: Path, known_paths: Sequence[Path]) -> None:
    if directory.resolve().parent != OUT_DIR or not directory.name.startswith(TRANSACTION_PREFIX):
        raise ManifestError("refusing cleanup outside exact V4 transaction directory")
    actual, allowed = set(directory.iterdir()), set(known_paths)
    if actual - allowed or any(path.is_symlink() or not path.is_file() for path in actual):
        raise ManifestError("unknown transaction content retained for manual recovery")
    for path in known_paths:
        if path.exists():
            path.unlink()
    directory.rmdir()


def rollback_destination(
    name: str, before: Snapshot, destination: Path, backup: Path,
    staged_identity: tuple[int, int],
) -> None:
    if destination.exists() and file_identity(destination) == staged_identity:
        if name in before.files:
            if not backup.exists():
                raise ManifestError(f"rollback backup missing: {name}")
            os.replace(backup, destination)
            if destination.read_bytes() != before.files[name]:
                raise ManifestError(f"rollback byte verification failed: {name}")
        else:
            destination.unlink()
        return
    if name in before.files:
        if (
            destination.exists()
            and file_identity(destination) == before.identities[name]
            and destination.read_bytes() == before.files[name]
        ):
            return
    elif not destination.exists():
        return
    raise ManifestError(f"rollback encountered foreign/uncertain destination identity: {name}")


def publish_transaction(audit: Audit, manifest: bytes, held: HeldWindowsLock) -> None:
    before = audit.snapshot
    outputs = {
        HANDOFF_PATH.name: audit.final_handoff,
        INDEX_PATH.name: audit.final_index,
        MANIFEST_PATH.name: manifest,
    }
    transaction = Path(tempfile.mkdtemp(prefix=TRANSACTION_PREFIX, dir=OUT_DIR))
    if transaction.resolve().parent != OUT_DIR:
        held.retain = True
        raise ManifestError("transaction directory escaped output root")
    transients = frozenset({LOCK_PATH.name, transaction.name})
    journal = transaction / "journal.jsonl"
    staged = {name: transaction / f"{index}.new" for index, name in enumerate(outputs)}
    backups = {name: transaction / f"{index}.old" for index, name in enumerate(outputs)}
    known_paths = [*staged.values(), *backups.values(), journal]
    staged_identities: dict[str, tuple[int, int]] = {}
    attempted: list[str] = []
    try:
        for name, data in outputs.items():
            write_exclusive(staged[name], data)
            staged_identities[name] = file_identity(staged[name])
            if name in before.files:
                write_exclusive(backups[name], before.files[name])
        write_exclusive(journal, b"")
        append_journal(journal, {
            "event": "PREPARED",
            "manifest_last": MANIFEST_PATH.name,
            "destinations": [
                {
                    "name": name,
                    "existed": name in before.files,
                    "old_sha256": sha256_bytes(before.files[name]) if name in before.files else None,
                    "new_sha256": sha256_bytes(data),
                    "staged": staged[name].name,
                    "backup": backups[name].name,
                }
                for name, data in outputs.items()
            ],
        })
        assert_held_windows_lock(held)
        assert_snapshot_current(before, transients=transients)
        for name in PUBLISHED_OUTPUTS:
            append_journal(journal, {"event": "REPLACE_INTENT", "name": name})
            attempted.append(name)
            os.replace(staged[name], OUT_DIR / name)
            append_journal(journal, {"event": "REPLACE_DONE", "name": name})

        after = audit_all(allow_unpublished=False, require_final=True, transients=transients)
        for name in before.expected - set(PUBLISHED_OUTPUTS):
            if after.snapshot.files[name] != before.files[name]:
                raise ManifestError(f"nonpublished artifact changed across commit: {name}")
        if after.snapshot.image_fingerprint != before.image_fingerprint:
            raise ManifestError("client image changed across commit")
        rederived_manifest = build_manifest(after)
        prospective_files(after, rederived_manifest)
        if rederived_manifest != manifest:
            raise ManifestError("postcommit re-derived manifest differs from staged manifest")
        for name, data in outputs.items():
            if after.snapshot.files[name] != data:
                raise ManifestError(f"postcommit exact-byte readback mismatch: {name}")
        assert_snapshot_current(after.snapshot, transients=transients)
        assert_held_windows_lock(held)
        append_journal(journal, {
            "event": "FINAL_REDERIVATION_PASS", "manifest_sha256": sha256_bytes(rederived_manifest),
        })
    except BaseException as original_error:
        try:
            for name in reversed(attempted):
                append_journal(journal, {"event": "ROLLBACK_INTENT", "name": name})
                rollback_destination(
                    name, before, OUT_DIR / name, backups[name], staged_identities[name]
                )
            cleanup_transaction(transaction, known_paths)
        except BaseException as rollback_error:
            held.retain = True
            raise ManifestError(
                f"publication failed; rollback/cleanup incomplete; retained {transaction.name} "
                f"and {LOCK_PATH.name}: {rollback_error}"
            ) from original_error
        raise
    else:
        try:
            assert_held_windows_lock(held)
            cleanup_transaction(transaction, known_paths)
        except BaseException as cleanup_error:
            held.retain = True
            raise ManifestError(
                f"checkpoint re-derived but transaction cleanup failed; retained "
                f"{transaction.name} and {LOCK_PATH.name}"
            ) from cleanup_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="read-only exact published checkpoint check")
    modes.add_argument("--audit-only", action="store_true", help="read-only prepublication/full audit")
    modes.add_argument("--self-test", action="store_true", help="exercise held Windows lock controls")
    args = parser.parse_args()
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

    if args.self_test:
        windows_lock_self_test()
        print("self-test PASS: held lock denies unlink/replace and releases by owned handle")
        return 0

    if args.check or args.audit_only:
        transients = frozenset()
        audit = audit_all(
            allow_unpublished=args.audit_only, require_final=args.check, transients=transients
        )
        manifest = build_manifest(audit)
        verify_existing_integration_checkpoint(audit, manifest)
        files = prospective_files(audit, manifest)
        handoff_labels = claim_label_census(
            HANDOFF_PATH.name, audit.final_handoff.decode("utf-8"),
            first_label="[MEASURED][CAPTURE]",
        )
        index_labels = claim_label_census(
            INDEX_PATH.name,
            audit.final_index.split(V3_INDEX_MARKER + b"\n", 1)[0].decode("utf-8"),
            first_label="[PROPOSED][LOCAL]",
        )
        if args.check and audit.snapshot.files.get(MANIFEST_PATH.name) != manifest:
            raise ManifestError("PF_V4_MANIFEST.md differs byte-for-byte from re-derived manifest")
        assert_snapshot_current(audit.snapshot, transients=transients)
        print(
            "check ok" if args.check else "audit ok",
            f"namespace={len(files)} exact_file_duplicates=0 within_tsv_duplicates=0",
            f"delta_dedup={audit.tsv.delta_dedup_count} base_targets={audit.tsv.base_target_count}",
            f"status_repeats={audit.tsv.repeated_lines}/{audit.tsv.repeated_occurrences}/{audit.tsv.repeated_extras}",
            f"a2_add_semantic={audit.tsv.a2_add_semantic_count}/{audit.tsv.a2_add_semantic_duplicate_groups}",
            f"claim_labels={sum(handoff_labels.values())}/{sum(index_labels.values())}",
            f"stored={audit.effective['stored_rows']} logical={audit.effective['logical_rows']}",
            f"manifest_sha256={sha256_bytes(manifest)}",
        )
        return 0

    if not PUBLICATION_RELEASED:
        raise ManifestError(
            "publication is held pending final reviewed status/validator hashes; use --audit-only"
        )
    windows_lock_self_test()
    success = ""
    with exclusive_publication_lock() as held:
        transients = frozenset({LOCK_PATH.name})
        audit = audit_all(allow_unpublished=True, require_final=False, transients=transients)
        manifest = build_manifest(audit)
        verify_existing_integration_checkpoint(audit, manifest)
        prospective_files(audit, manifest)
        assert_held_windows_lock(held)
        publish_transaction(audit, manifest, held)
        success = f"PF_V4_MANIFEST.md {sha256_bytes(manifest)}"
    print(success)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestError as exc:
        raise SystemExit(f"ERROR: {exc}")
