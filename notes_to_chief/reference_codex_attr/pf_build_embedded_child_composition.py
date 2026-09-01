#!/usr/bin/env python3
"""Build the duplicate-safe IMAGE embedded-child composition overlay."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import shutil
import struct
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, replace
from io import StringIO
from pathlib import Path
from typing import Iterable, Mapping, Sequence

sys.dont_write_bytecode = True


IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
IMAGE_SIZE = 14759424

PINNED = {
    "PF_PROTOCOL_PRIORITY.tsv": "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55",
    "PF_POST_V1_PRIORITY_DELTA.tsv": "69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51",
    "PF_PRIORITY_POOL_638690_DELTA.tsv": "cc585d983dd1ca155ea1cfcfc59116897b59d2ce2455dc96f1d4097e9d7afdd5",
    "PF_PRIORITY_POOL_661FA0_DELTA.tsv": "3ba436e9b4876a1575a6d5544f49bb462896e2c6ae4191e085eacb56788ef880",
    "PF_PRIORITY_POOL_46F4D0_DELTA.tsv": "32a59e143052f827f8134bba890f28d63444c447943e6679521dade7ff7e9fd1",
    "PF_PRIORITY_COMPILER_TARGET_6564_DELTA.tsv": "390d974c153fa9e3498f0a8f2fa79a08848d88acde466061abfeecf3b9125d07",
    "PF_SERIALIZER_FIELDS.tsv": "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123",
    "PF_A2_SERIALIZER_SLOT34_DELTA.tsv": "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334",
    "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv": "00ef0f3cb632b40ba168ce79bbd656fc7a6936a55f3b3e185c6e63b32c39ec5d",
    "PF_TARGET_652A30_A2_DELTA.tsv": "217f7f9854df7412ca942d755c0ed858130954f93c8384185af9719415720592",
    "PF_V3_P1_OPEN.tsv": "37eb9ca4ebc25f0fdcd4e9e56d8458c031beee9b98640cb95a84be3a8a7553c6",
    "PF_V3_MANIFEST.md": "dc87eedc65ed5e07ce4673742b6a0d20304140bb177e617c6af8b3846bd0b50e",
    "pf_validate_v2_effective_capture.py": "7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9",
    "pf_validate_v3_effective_capture.py": "3d145407c9a6e4236eefe829c9fb9eb0757bf53cce9ac9cb136f201f594a360b",
    "pf_build_daily_activity_closure.py": "e58f4da41e6f82c9a3c182961019394ebab4b8034e1d39f2c8c92b272a35d09d",
    "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv": "10b54ee781ad0147d5bd18c0171b88132d9fd61dc39e0adf6fa4055bc7b7890d",
    "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv": "395b1776d3351304612ceb36eade9003b929fb8bb914986b4873f0737e60a5e3",
    "PF_DAILY_ACTIVITY_CLOSURE.md": "7a58caf4efb025c0703fa4a583785cb0d7d61269d4d92ddf18118da299bfc75e",
}

A2_OUTPUT = "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv"
PRIORITY_OUTPUT = "PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv"
REPORT_OUTPUT = "PF_EMBEDDED_CHILD_COMPOSITION.md"
OWNED_OUTPUTS = {A2_OUTPUT, PRIORITY_OUTPUT, REPORT_OUTPUT}
LOCK_NAME = ".PF_EMBEDDED_CHILD_COMPOSITION.lock"
TX_PREFIX = ".PF_EMBEDDED_CHILD_COMPOSITION_TXN."

DAILY_PRIORITY_KEY = "9cbe29103227dbf46f8f7fd5c3c5c82f5ed3b340f12ca98d1ecc802500e5b9b9"
GUILD_PRIORITY_KEY = "d7ea6be68e2656adab63669736997bfbf9053cddf3bcfc2f05d0c7d9d9ad0d68"
DAILY_PRIORITY_ROW_KEY = "97ca8fd70f21a421c0d753cb5560aa0367cb580858a13e1ebfde41d88b95e41e"
GUILD_PRIORITY_ROW_KEY = "eb11cfdadc9ab64b400243f198f34268ec9e74fef403dd83af0d7c90d896f8e0"
GUILD_BLOCKERS = (
    "atomic_target_object_alias_unproved | direct_call_not_proven_serializer | "
    "dynamic_vtable_plus_0x04_target_unresolved | "
    "indirect_call_not_proven_serializer_slot | "
    "indirect_serializer_direction_unresolved | "
    "invalid_parameter_import_call_wire_effect_unproved | "
    "invalid_parameter_singleton_register_call_wire_effect_unproved | "
    "mutable_pointer_slot_traversal_alias_unproved"
)

V3_PRIORITY_OVERLAYS = (
    "PF_POST_V1_PRIORITY_DELTA.tsv",
    "PF_PRIORITY_POOL_638690_DELTA.tsv",
    "PF_PRIORITY_POOL_661FA0_DELTA.tsv",
    "PF_PRIORITY_POOL_46F4D0_DELTA.tsv",
    "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv",
    "PF_PRIORITY_COMPILER_TARGET_6564_DELTA.tsv",
)

BLOCKER_GROUPS = (
    "CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED",
    "DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED",
    "INDIRECT_JUMP_TARGET_UNRESOLVED",
    "OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED",
    "REGISTRY_IDENTITY_UNRESOLVED",
)

EXPECTED_METRICS = {
    "p1_closed": 255,
    "p1_total": 365,
    "p2_closed": 8,
    "p2_total": 16,
    "p3_closed": 71,
    "p3_total": 138,
    "overall_closed": 334,
    "overall_total": 519,
    "a2_stored_rows": 8657,
    "a2_reference_rows": 4,
    "a2_unknown_rows": 3963,
    "a2_generic_call_jump_unknown": 1312,
    "a2_direct_invalid_parameter_unknown": 881,
    "a2_delta_rows": 6,
    "a2_changed_references": 4,
    "a2_directional_removals": 2,
    "daily_child_rows_r": 6,
    "daily_child_rows_w": 6,
    "daily_child_unknown": 0,
    "group_call_effect": 14,
    "group_dynamic": 78,
    "group_indirect_jump": 0,
    "group_object_graph": 7,
    "group_registry_identity": 11,
}


@dataclass(frozen=True)
class SpanPin:
    role: str
    start: int
    end: int
    sha256: str
    expected_off: int


SPANS = (
    SpanPin("actor_parent_ctor", 0x006A0FE0, 0x006A1044, "518da7bf9b8cd319022ad373e9b5f208679dcbaf4133426fef3babeb9ed10024", 0x002A03E0),
    SpanPin("daily_child_ctor", 0x0069CCF0, 0x0069CD56, "423f46497dba4785787b7174bf6b571677e6ff6443e2c4b280867022f54dc64f", 0x0029C0F0),
    SpanPin("daily_child_vtable", 0x00F3C510, 0x00F3C548, "6e7c3bac1c80aba92afb3d6ecdab7b740971fd7b02efe2fc876c628b163a8f7d", 0x00B3A910),
    SpanPin("actor_parent_serializer", 0x0069F700, 0x0069F716, "25accf437e846ede788f403ada721771b2629f1f2adb393f4bee3d0bc2f6c9c7", 0x0029EB00),
    SpanPin("dbss_parent_ctor", 0x00672940, 0x006729A4, "ed42b5893e95f369ce9f2e22ae28ffe1a412d96d3a14a1ac5246e729fae43a34", 0x00271D40),
    SpanPin("guild_child_ctor", 0x006720F0, 0x00672106, "58072a2d6fa0328e9e3201ab5fbaa60a6c847c56ecccb2267aaeda4eb553b1c6", 0x002714F0),
    SpanPin("guild_child_vtable", 0x00F39108, 0x00F39140, "6c910b23ab9e924cab8669b9e6d53129ddfc47a7558300d77a604cdeea3f2ff9", 0x00B37508),
    SpanPin("dbss_parent_serializer", 0x006723D0, 0x00672491, "3429135c0f917857db707bb8f6fdf362cbef42f4ff1d22f75e64aae919cec588", 0x002717D0),
    SpanPin("guild_child_serializer", 0x00469FA0, 0x00469FD8, "828554cb9ece35a2316ffc9e8bf44be3b2ef033bd189cb9b15400ecd3b48c63f", 0x000693A0),
)


@dataclass(frozen=True)
class BaseTarget:
    line: int
    row_key: str
    message: str
    direction: str
    order: str
    action: str
    new_order: str
    child: str
    child_vtable: int
    child_target: int
    child_rows: int
    child_unknown: int


TARGETS = (
    BaseTarget(3871, "cb43e706bacbb15759eca90294117726fe7d844e86faf6b1ab8ae4df145bf137", "DBSS_GuildStorageInitialVital", "R", "1", "REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW", "N/A", "CGuildStorageAttr", 0x00F39108, 0x00469FA0, 26, 18),
    BaseTarget(3872, "771ddb7e4fa86cf605a643f6cbdf03e352adfc11a1c72cac64a31b2258263f65", "DBSS_GuildStorageInitialVital", "W", "1", "CHANGED", "1", "CGuildStorageAttr", 0x00F39108, 0x00469FA0, 26, 18),
    BaseTarget(3873, "87cc968b127ced6878e568a6cda14906068d03bce18f9e1720240ae37c2ad36b", "DBSS_GuildStorageInitialVital", "R", "2", "CHANGED", "1", "CGuildStorageAttr", 0x00F39108, 0x00469FA0, 26, 18),
    BaseTarget(3874, "903f74b75ba99d786676ab53482a2852f9b33da6bce535fef1bd878049ee9d74", "DBSS_GuildStorageInitialVital", "W", "2", "REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW", "N/A", "CGuildStorageAttr", 0x00F39108, 0x00469FA0, 26, 18),
    BaseTarget(4415, "c96bd6187e4784d419e50e8e199afeeea6787959fc0a31257d469dddb8c6276c", "ActorActivity_UpdateDailyActivityStateVital", "R", "1", "CHANGED", "1", "DailyActivityState", 0x00F3C510, 0x0069CB20, 6, 0),
    BaseTarget(4416, "06578973ca2a71328082ed79589785334933ed33da3b70cc14b800eac086fc0b", "ActorActivity_UpdateDailyActivityStateVital", "W", "1", "CHANGED", "1", "DailyActivityState", 0x00F3C510, 0x0069CB20, 6, 0),
)

A2_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line",
    "base_row_key", "base_delta_key", "message", "direction(W/R)",
    "old_order", "old_tag", "old_field_offset", "old_len",
    "new_wire_order", "new_tag", "new_field_offset", "new_len",
    "new_gate_condition", "resolution", "child_message", "child_receiver",
    "child_vtable_va", "child_slot", "child_serializer_va",
    "child_effective_rows", "child_effective_unknown_rows", "evidence_ticket",
    "evidence_span_start", "evidence_span_end", "evidence_span_sha256",
    "evidence_file_off", "source",
)

PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "priority", "old_registry_identity_status",
    "new_registry_identity_status", "old_registry_identity_missing",
    "new_registry_identity_missing", "old_serializer_status",
    "new_serializer_status", "old_serializer_blockers",
    "new_serializer_blockers", "old_structural_status",
    "new_structural_status", "old_blocker", "new_blocker",
    "old_primary_blocker_group", "new_primary_blocker_group",
    "child_message", "child_priority_file", "child_priority_delta_key",
    "child_priority_file_sha256", "evidence_ticket", "closure_scope", "source",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_hash(path: Path, expected: str, label: str) -> str:
    if not path.is_file():
        raise RuntimeError(f"missing {label}: {path.name}")
    actual = sha256_path(path)
    if actual != expected:
        raise RuntimeError(f"{label} SHA-256 mismatch: expected {expected}, got {actual}")
    return actual


def row_key(fieldnames: Sequence[str], row: Mapping[str, str]) -> str:
    payload = json.dumps(
        [row[name] for name in fieldnames],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def delta_key(parts: Iterable[str]) -> str:
    return sha256_bytes("\x1f".join(parts).encode("ascii"))


def read_tsv(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise RuntimeError(f"missing TSV header: {path.name}")
        fields = list(reader.fieldnames)
        if any(name is None or not name.strip() for name in fields):
            raise RuntimeError(f"empty TSV header: {path.name}")
        if len(fields) != len(set(fields)):
            raise RuntimeError(f"duplicate TSV header: {path.name}")
        rows: list[tuple[int, dict[str, str]]] = []
        for line_no, raw in enumerate(reader, start=2):
            if (
                None in raw
                or len(raw) != len(fields)
                or set(raw) != set(fields)
                or any(value is None for value in raw.values())
            ):
                raise RuntimeError(f"malformed TSV row: {path.name}:{line_no}")
            rows.append((line_no, dict(raw)))
    return fields, rows


def tsv_text(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
    out = StringIO(newline="")
    writer = csv.DictWriter(
        out,
        fieldnames=list(columns),
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


class PeImage:
    def __init__(self, data: bytes) -> None:
        self.data = data
        if len(data) != IMAGE_SIZE or data[:2] != b"MZ":
            raise RuntimeError("image size/signature mismatch")
        pe = struct.unpack_from("<I", data, 0x3C)[0]
        if data[pe:pe + 4] != b"PE\0\0":
            raise RuntimeError("image PE signature mismatch")
        coff = pe + 4
        count = struct.unpack_from("<H", data, coff + 2)[0]
        opt_size = struct.unpack_from("<H", data, coff + 16)[0]
        opt = coff + 20
        if struct.unpack_from("<H", data, opt)[0] != 0x10B:
            raise RuntimeError("image is not PE32")
        self.base = struct.unpack_from("<I", data, opt + 28)[0]
        table = opt + opt_size
        self.sections: list[tuple[int, int, int, int]] = []
        for index in range(count):
            off = table + index * 40
            vsize, rva, raw_size, raw = struct.unpack_from("<IIII", data, off + 8)
            self.sections.append((rva, vsize, raw, raw_size))

    def slice(self, start: int, end: int) -> tuple[int, bytes]:
        if end <= start:
            raise RuntimeError("invalid VA span")
        rva = start - self.base
        length = end - start
        for section_rva, vsize, raw, raw_size in self.sections:
            delta = rva - section_rva
            if delta < 0 or delta + length > raw_size or delta + length > max(vsize, raw_size):
                continue
            file_off = raw + delta
            return file_off, self.data[file_off:file_off + length]
        raise RuntimeError(f"unmapped VA span 0x{start:08X}-0x{end:08X}")


def verify_image(image_path: Path) -> tuple[PeImage, dict[str, tuple[int, bytes]]]:
    require_hash(image_path, IMAGE_SHA256, "GameClient image")
    image = PeImage(image_path.read_bytes())
    if image.base != 0x00400000:
        raise RuntimeError("unexpected image base")
    verified: dict[str, tuple[int, bytes]] = {}
    for pin in SPANS:
        off, data = image.slice(pin.start, pin.end)
        if off != pin.expected_off or sha256_bytes(data) != pin.sha256:
            raise RuntimeError(f"IMAGE span mismatch: {pin.role}")
        verified[pin.role] = (off, data)

    composition = (
        ("actor", "actor_parent_ctor", 0x0069CCF0, "daily_child_ctor", 0x00F3C510, "daily_child_vtable", 0x0069CB20),
        ("dbss", "dbss_parent_ctor", 0x006720F0, "guild_child_ctor", 0x00F39108, "guild_child_vtable", 0x00469FA0),
    )
    for label, parent_role, child_ctor, child_role, vtable, vtable_role, target in composition:
        parent_start = next(pin.start for pin in SPANS if pin.role == parent_role)
        parent = verified[parent_role][1]
        calls = []
        for index in range(len(parent) - 4):
            if parent[index] == 0xE8:
                destination = parent_start + index + 5 + struct.unpack_from("<i", parent, index + 1)[0]
                if destination == child_ctor:
                    calls.append(index)
        if len(calls) != 1:
            raise RuntimeError(f"{label} child constructor call mismatch")
        if not any(parent[index] == 0x8D and parent[index + 2] == 0x18 for index in range(max(0, calls[0] - 16), calls[0] - 1)):
            raise RuntimeError(f"{label} this+0x18 receiver setup mismatch")
        child = verified[child_role][1]
        if child.count(struct.pack("<I", vtable)) != 1:
            raise RuntimeError(f"{label} child vtable constructor assignment mismatch")
        vtable_bytes = verified[vtable_role][1]
        if len(vtable_bytes) != 0x38 or struct.unpack_from("<I", vtable_bytes, 0x34)[0] != target:
            raise RuntimeError(f"{label} vtable +0x34 target mismatch")
    return image, verified


def verify_pins(external: Path, image: Path) -> dict[str, str]:
    measured = {"GameClient.local.bin": require_hash(image, IMAGE_SHA256, "GameClient image")}
    for name, expected in PINNED.items():
        measured[name] = require_hash(external / name, expected, name)
    return measured


def load_v3_validator(external: Path) -> object:
    module_path = external / "pf_validate_v3_effective_capture.py"
    if str(external) not in sys.path:
        sys.path.insert(0, str(external))
    spec = importlib.util.spec_from_file_location(
        "_pf_embedded_child_v3_validator", module_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned V3 validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.verify_v2_module()
    module.v2.verify_pinned_inputs(external, False)
    module.verify_new_inputs(external, False)
    return module


def subcall_is_flattened(field: object, fields: Sequence[object]) -> bool:
    target = str(field.tag).split(":", 1)[1]
    for candidate in fields:
        if candidate.sequence <= field.sequence:
            continue
        searchable = " ".join(
            (
                str(candidate.field_offset),
                str(candidate.origin_field_offset),
                str(candidate.gate_condition),
                str(candidate.origin_gate_condition),
            )
        )
        if target in searchable and not str(candidate.tag).startswith("SUBCALL:"):
            return True
    return False


def canonical_field_open_reasons(
    field: object, fields: Sequence[object], v2: object
) -> tuple[str, ...]:
    """Canonical full closure predicate used by the pinned Daily builder."""
    reasons: set[str] = set()
    tag = str(field.tag)
    offset = str(field.field_offset)
    length = str(field.length)
    order = str(field.wire_order)
    gate = str(field.gate_condition)

    def unknown(value: str) -> bool:
        return not value or value == "UNKNOWN" or "UNKNOWN(" in value

    if unknown(tag):
        reasons.add("UNKNOWN_TAG")
    elif not (
        v2.NUMERIC_TAG_RE.fullmatch(tag)
        or tag in v2.ZERO_LENGTH_TAGS
        or tag in v2.STRING_TAGS
        or tag.startswith("SUBCALL:")
    ):
        reasons.add("UNSUPPORTED_TAG")
    if unknown(offset):
        reasons.add("UNKNOWN_OFFSET")
    if unknown(length):
        reasons.add("UNKNOWN_LENGTH")
    elif v2.NUMERIC_TAG_RE.fullmatch(tag) and not length.isdigit():
        reasons.add("INVALID_NUMERIC_LENGTH")
    if not (order.isdigit() or v2.ALT_ORDER_RE.fullmatch(order)):
        reasons.add("UNKNOWN_OR_UNSUPPORTED_ORDER")
    if unknown(gate):
        reasons.add("UNKNOWN_GATE")
    if v2.KIND_GATE_RE.fullmatch(gate) is not None:
        reasons.add("KIND_GATE_OUTSIDE_CTRACE")
    if gate.startswith("test@") and " mask=" in gate:
        reasons.add("UNEXECUTED_MASK_GATE")
    if ("!=NULL" in gate or "DECODED_" in gate) and tag.startswith("SUBCALL:"):
        reasons.add("UNEXECUTED_PRESENCE_GATE")
    if tag.startswith("SUBCALL:") and not subcall_is_flattened(field, fields):
        reasons.add("UNFLATTENED_SUBCALL")
    return tuple(sorted(reasons))


def verify_daily_predicate_mutations(
    residual: Mapping[str, Sequence[object]], v2: object
) -> None:
    for direction in ("W", "R"):
        for field in residual[direction]:
            if canonical_field_open_reasons(field, residual[direction], v2):
                raise RuntimeError("unmutated Daily residual fails canonical closure predicate")
    all_fields = [field for direction in ("W", "R") for field in residual[direction]]
    numeric = next(
        field for field in all_fields if v2.NUMERIC_TAG_RE.fullmatch(str(field.tag))
    )
    mutations = (
        replace(numeric, tag="UNKNOWN(test_mutation)"),
        replace(numeric, field_offset="UNKNOWN(test_mutation)"),
        replace(numeric, length="UNKNOWN(test_mutation)"),
        replace(numeric, wire_order="UNKNOWN(test_mutation)"),
        replace(numeric, gate_condition="UNKNOWN(test_mutation)"),
    )
    if any(
        not canonical_field_open_reasons(value, (value,), v2)
        for value in mutations
    ):
        raise RuntimeError("Daily canonical closure mutation escaped")
    marker = next(field for field in all_fields if str(field.tag).startswith("SUBCALL:"))
    if "UNFLATTENED_SUBCALL" not in canonical_field_open_reasons(
        marker, (marker,), v2
    ):
        raise RuntimeError("Daily unflattened-subcall mutation escaped")


def remove_exact_effective_field(
    effective: dict[tuple[str, str], list[object]],
    row: Mapping[str, str],
    evidence_key: str,
) -> object:
    semantic = (row["message"], row["direction(W/R)"])
    matches = [
        value for value in effective[semantic] if value.evidence_key == evidence_key
    ]
    if len(matches) != 1:
        raise RuntimeError(f"effective A2 target is not unique: {semantic}:{evidence_key}")
    value = matches[0]
    expected = (
        row["old_order"], row["old_tag"], row["old_field_offset"], row["old_len"]
    )
    actual = (value.wire_order, value.tag, value.field_offset, value.length)
    if expected != actual:
        raise RuntimeError(f"effective A2 old-row mismatch: {semantic}:{expected}!={actual}")
    effective[semantic].remove(value)
    return value


def replay_status_metrics(
    external: Path, priority_rows: Sequence[Mapping[str, str]]
) -> tuple[dict[str, int], Counter[str]]:
    base_fields, base_rows = read_tsv(external / "PF_PROTOCOL_PRIORITY.tsv")
    if len(base_rows) != 519:
        raise RuntimeError("priority base census drift")
    states: dict[str, dict[str, str]] = {}
    loaded: dict[str, tuple[list[str], list[tuple[int, dict[str, str]]]]] = {
        "PF_PROTOCOL_PRIORITY.tsv": (base_fields, base_rows)
    }
    for line, row in base_rows:
        message = row["message"]
        if message in states or row["source"] != "IMAGE":
            raise RuntimeError("priority base duplicate/mixed source")
        states[message] = {
            "priority": row["priority"],
            "registry_identity_status": row["registry_identity_status"],
            "registry_identity_missing": row["registry_identity_missing"],
            "serializer_status": row["serializer_status"],
            "serializer_blockers": row["serializer_blockers"],
            "structural_status": row["structural_status"],
            "blocker": row["blocker"],
            "last_file": "PF_PROTOCOL_PRIORITY.tsv",
            "last_line": str(line),
            "last_key": row_key(base_fields, row),
        }

    def apply_overlay(name: str) -> None:
        fields, rows = read_tsv(external / name)
        local: set[str] = set()
        for line, row in rows:
            message = row["message"]
            if message not in states or message in local:
                raise RuntimeError(f"invalid status overlay message: {name}:{message}")
            local.add(message)
            state = states[message]
            ref_name = row["base_file"]
            if ref_name not in loaded:
                raise RuntimeError(f"unknown status predecessor: {name}:{ref_name}")
            ref_fields, ref_rows = loaded[ref_name]
            ref_line = int(row["base_line"])
            hits = [ref for item_line, ref in ref_rows if item_line == ref_line]
            if len(hits) != 1:
                raise RuntimeError(f"missing status predecessor line: {name}:{ref_line}")
            ref = hits[0]
            ref_key = row_key(ref_fields, ref)
            if (
                row["action"] != "CHANGED"
                or row["source"] != "IMAGE"
                or row["base_row_key"] != ref_key
                or ref["message"] != message
                or state["last_file"] != ref_name
                or state["last_line"] != row["base_line"]
                or state["last_key"] != ref_key
            ):
                raise RuntimeError(f"status predecessor chain mismatch: {name}:{message}")
            if ref_name == "PF_PROTOCOL_PRIORITY.tsv":
                if row.get("base_delta_key", "N/A") != "N/A":
                    raise RuntimeError(f"unexpected V1 base delta key: {name}:{message}")
            elif row.get("base_delta_key") != ref.get("delta_key"):
                raise RuntimeError(f"status predecessor delta-key mismatch: {name}:{message}")
            comparisons = (
                ("priority", "priority"),
                ("old_serializer_status", "serializer_status"),
                ("old_structural_status", "structural_status"),
                ("old_blocker", "blocker"),
            )
            if "old_registry_identity_status" in row:
                comparisons += (("old_registry_identity_status", "registry_identity_status"),)
            if "old_registry_identity_missing" in row:
                comparisons += (("old_registry_identity_missing", "registry_identity_missing"),)
            if "old_serializer_blockers" in row:
                comparisons += (("old_serializer_blockers", "serializer_blockers"),)
            for row_name, state_name in comparisons:
                if row[row_name] != state[state_name]:
                    raise RuntimeError(f"old status value mismatch: {name}:{message}:{row_name}")
            state["serializer_status"] = row["new_serializer_status"]
            state["structural_status"] = row["new_structural_status"]
            state["blocker"] = row["new_blocker"]
            if "new_registry_identity_status" in row:
                state["registry_identity_status"] = row["new_registry_identity_status"]
                state["registry_identity_missing"] = row["new_registry_identity_missing"]
            if "new_serializer_blockers" in row:
                state["serializer_blockers"] = row["new_serializer_blockers"]
            state["last_file"] = name
            state["last_line"] = str(line)
            state["last_key"] = row_key(fields, row)
        loaded[name] = (fields, rows)

    for name in V3_PRIORITY_OVERLAYS:
        apply_overlay(name)

    open_fields, open_rows = read_tsv(external / "PF_V3_P1_OPEN.tsv")
    del open_fields
    open_by_message = {row["message"]: row for _line, row in open_rows}
    if len(open_by_message) != len(open_rows):
        raise RuntimeError("duplicate V3 P1 OPEN message")
    state_open = {
        message for message, state in states.items()
        if state["priority"] == "1" and state["structural_status"] == "OPEN"
    }
    if state_open != set(open_by_message):
        raise RuntimeError("V3 P1 OPEN index/state replay mismatch")
    groups = Counter(row["primary_blocker_group"] for row in open_by_message.values())

    # Daily is a normal evidence transition chained from the slot34 overlay.
    apply_overlay("PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv")

    # Composition rows use the exact derived V3 OPEN row as predecessor.
    open_fields, open_rows_again = read_tsv(external / "PF_V3_P1_OPEN.tsv")
    open_by_line = {line: row for line, row in open_rows_again}
    for row in priority_rows:
        message = row["message"]
        line = int(row["base_line"])
        base = open_by_line.get(line)
        if (
            base is None
            or row["base_file"] != "PF_V3_P1_OPEN.tsv"
            or row["base_row_key"] != row_key(open_fields, base)
            or row["base_delta_key"] != base["status_key"]
            or base["message"] != message
            or row["source"] != "IMAGE"
        ):
            raise RuntimeError(f"composition status predecessor mismatch: {message}")
        state = states[message]
        comparisons = (
            (row["old_registry_identity_status"], base["effective_registry_identity_status"]),
            (row["old_registry_identity_missing"], base["effective_registry_identity_missing"]),
            (row["old_serializer_status"], base["effective_serializer_status"]),
            (row["old_structural_status"], base["effective_structural_status"]),
            (row["old_blocker"], base["effective_blocker"]),
        )
        if any(left != right for left, right in comparisons):
            raise RuntimeError(f"composition status old-value mismatch: {message}")
        old_group = base["primary_blocker_group"]
        groups[old_group] -= 1
        if row["new_structural_status"] == "OPEN":
            groups[row["new_primary_blocker_group"]] += 1
        state["serializer_status"] = row["new_serializer_status"]
        state["serializer_blockers"] = row["new_serializer_blockers"]
        state["structural_status"] = row["new_structural_status"]
        state["blocker"] = row["new_blocker"]

    counts: dict[str, int] = {}
    for priority in (1, 2, 3):
        selected = [state for state in states.values() if state["priority"] == str(priority)]
        counts[f"p{priority}_total"] = len(selected)
        counts[f"p{priority}_closed"] = sum(
            state["structural_status"] == "CLOSED" for state in selected
        )
    counts["overall_total"] = len(states)
    counts["overall_closed"] = sum(
        state["structural_status"] == "CLOSED" for state in states.values()
    )
    if sum(groups.values()) != counts["p1_total"] - counts["p1_closed"]:
        raise RuntimeError("P1 blocker group/open count mismatch")
    if any(groups[group] < 0 for group in BLOCKER_GROUPS):
        raise RuntimeError("negative P1 blocker group count")
    return counts, groups


def recompute_effective_metrics(
    external: Path,
    v3: object,
    effective_v3: Mapping[tuple[str, str], Sequence[object]],
    a2_rows: Sequence[Mapping[str, str]],
    priority_rows: Sequence[Mapping[str, str]],
) -> dict[str, int]:
    effective: dict[tuple[str, str], list[object]] = {
        key: list(values) for key, values in effective_v3.items()
    }
    _daily_fields, daily_rows = read_tsv(
        external / "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv"
    )
    for _line, row in daily_rows:
        if row["action"] != "REMOVE_OVERLAY_NONWIRE_ROW" or row["source"] != "IMAGE":
            raise RuntimeError("invalid Daily A2 action/source")
        remove_exact_effective_field(effective, row, row["base_delta_key"])

    for row in a2_rows:
        value = remove_exact_effective_field(effective, row, row["base_row_key"])
        if row["action"] == "CHANGED":
            changed = replace(
                value,
                field_identity=f"DELTA:{row['delta_key']};ORDER:{row['new_wire_order']}",
                wire_order=row["new_wire_order"],
                tag=row["new_tag"],
                length=row["new_len"],
                field_offset=row["new_field_offset"],
                gate_condition=row["new_gate_condition"],
                provenance="EMBEDDED_CHILD_COMPOSITION",
                evidence_key=row["delta_key"],
            )
            semantic = (row["message"], row["direction(W/R)"])
            effective[semantic].append(changed)
            effective[semantic].sort(key=lambda item: item.sequence)
        elif row["action"] != "REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW":
            raise RuntimeError("unsupported composition A2 action")

    all_fields = [value for values in effective.values() for value in values]
    metrics, groups = replay_status_metrics(external, priority_rows)
    metrics.update(
        {
            "a2_stored_rows": len(all_fields),
            "a2_reference_rows": sum(
                value.tag == "STATIC_EMBEDDED_CHILD_REF" for value in all_fields
            ),
            "a2_unknown_rows": sum(
                value.tag == "UNKNOWN" or "UNKNOWN" in value.field_offset
                for value in all_fields
            ),
            "a2_generic_call_jump_unknown": sum(
                value.tag.startswith(("CALL_UNCLASSIFIED:", "JUMP_UNCLASSIFIED:"))
                and (value.tag == "UNKNOWN" or "UNKNOWN" in value.field_offset)
                for value in all_fields
            ),
            "a2_direct_invalid_parameter_unknown": sum(
                value.tag == "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
                and "UNKNOWN" in value.field_offset
                for value in all_fields
            ),
            "a2_delta_rows": len(a2_rows),
            "a2_changed_references": sum(
                row["action"] == "CHANGED" for row in a2_rows
            ),
            "a2_directional_removals": sum(
                row["action"] == "REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW"
                for row in a2_rows
            ),
            "daily_child_rows_r": int(next(
                row["child_effective_rows"] for row in a2_rows
                if row["child_message"] == "DailyActivityState"
                and row["direction(W/R)"] == "R"
            )),
            "daily_child_rows_w": int(next(
                row["child_effective_rows"] for row in a2_rows
                if row["child_message"] == "DailyActivityState"
                and row["direction(W/R)"] == "W"
            )),
            "daily_child_unknown": max(
                int(row["child_effective_unknown_rows"])
                for row in a2_rows
                if row["child_message"] == "DailyActivityState"
            ),
            "group_call_effect": groups["CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED"],
            "group_dynamic": groups["DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED"],
            "group_indirect_jump": groups["INDIRECT_JUMP_TARGET_UNRESOLVED"],
            "group_object_graph": groups["OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED"],
            "group_registry_identity": groups["REGISTRY_IDENTITY_UNRESOLVED"],
        }
    )
    if metrics != EXPECTED_METRICS:
        differences = {
            key: (EXPECTED_METRICS.get(key), metrics.get(key))
            for key in sorted(set(EXPECTED_METRICS) | set(metrics))
            if EXPECTED_METRICS.get(key) != metrics.get(key)
        }
        raise RuntimeError(f"effective projection mismatch: {differences}")
    return metrics


def verify_daily_effective_child(
    external: Path,
    v3: object,
    effective_v3: Mapping[tuple[str, str], Sequence[object]],
) -> None:
    slot_fields, slot_rows = read_tsv(external / "PF_A2_SERIALIZER_SLOT34_DELTA.tsv")
    del slot_fields
    daily_fields, daily_rows = read_tsv(external / "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv")
    del daily_fields
    prior_fields, prior_rows = read_tsv(external / "PF_TARGET_652A30_A2_DELTA.tsv")
    del prior_fields
    added = {
        row["delta_key"]: row
        for _line, row in slot_rows
        if row["message"] == "DailyActivityState" and row["action"] == "ADD_CORRECTED_SLOT34_ROW"
    }
    if len(added) != 26:
        raise RuntimeError("DailyActivityState slot34 input is not 13R+13W")
    removed: set[str] = set()
    for source_name, rows in (
        ("PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv", daily_rows),
        ("PF_TARGET_652A30_A2_DELTA.tsv", prior_rows),
    ):
        selected = [row for _line, row in rows if row["message"] == "DailyActivityState"]
        expected = 12 if source_name.startswith("PF_A2_DAILY") else 2
        if len(selected) != expected:
            raise RuntimeError(f"unexpected DailyActivityState removal count in {source_name}")
        for row in selected:
            if row["source"] != "IMAGE" or row["action"] != "REMOVE_OVERLAY_NONWIRE_ROW":
                raise RuntimeError(f"invalid DailyActivityState dependency row in {source_name}")
            key = row["base_delta_key"]
            if key not in added or key in removed:
                raise RuntimeError(f"DailyActivityState dependency key mismatch in {source_name}")
            if row["base_row_key"] != row_key(list(added[key].keys()), added[key]):
                raise RuntimeError(f"DailyActivityState dependency row hash mismatch in {source_name}")
            removed.add(key)
    effective_raw = [row for key, row in added.items() if key not in removed]
    counts = {direction: sum(row["direction(W/R)"] == direction for row in effective_raw) for direction in ("R", "W")}
    if counts != {"R": 6, "W": 6}:
        raise RuntimeError(f"DailyActivityState effective child row count mismatch: {counts}")
    for row in effective_raw:
        if row["source"] != "IMAGE" or "UNKNOWN" in row["new_field_offset"] or row["new_tag"] == "UNKNOWN":
            raise RuntimeError("DailyActivityState effective child retains UNKNOWN")

    # Rebuild the canonical V3 effective child, apply only the new Daily
    # removals, and use the exact full predicate from the pinned Daily builder.
    effective_machine: dict[tuple[str, str], list[object]] = {
        key: list(values) for key, values in effective_v3.items()
    }
    for _line, delta in daily_rows:
        remove_exact_effective_field(
            effective_machine, delta, delta["base_delta_key"]
        )
    residual = {
        direction: effective_machine[("DailyActivityState", direction)]
        for direction in ("W", "R")
    }
    if {direction: len(values) for direction, values in residual.items()} != {
        "W": 6,
        "R": 6,
    }:
        raise RuntimeError("DailyActivityState canonical residual census mismatch")
    if any(all(value.tag == "EMPTY" for value in values) for values in residual.values()):
        raise RuntimeError("DailyActivityState residual direction is empty-only")
    verify_daily_predicate_mutations(residual, v3.v2)

    priority_fields, priority_rows = read_tsv(external / "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv")
    selected = [row for _line, row in priority_rows if row["message"] == "DailyActivityState"]
    if len(selected) != 1:
        raise RuntimeError("DailyActivityState priority dependency cardinality mismatch")
    row = selected[0]
    if (
        row_key(priority_fields, row) != DAILY_PRIORITY_ROW_KEY
        or row["delta_key"] != DAILY_PRIORITY_KEY
        or row["base_file"] != "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv"
        or row["base_line"] != "15"
        or row["base_row_key"] != "c18d6d65a771b97b112ca8f1d7062c4d204bf8cb9bb87a6a22794737a8b6af13"
        or row["base_delta_key"] != "c4d24d899578ad584b3b13e3f81f4aa051f77f9380ea0c893929080434f8e017"
        or row["priority"] != "3"
        or row["old_serializer_status"] != "OPEN"
        or row["new_serializer_status"] != "CLOSED"
        or row["old_structural_status"] != "OPEN"
        or row["new_structural_status"] != "CLOSED"
        or row["new_serializer_blockers"] != "N/A"
        or row["new_blocker"] != "N/A"
        or row["source"] != "IMAGE"
    ):
        raise RuntimeError("DailyActivityState priority dependency mismatch")


def verify_guild_child(external: Path) -> None:
    _fields, rows = read_tsv(external / "PF_A2_SERIALIZER_SLOT34_DELTA.tsv")
    child = [row for _line, row in rows if row["message"] == "CGuildStorageAttr" and row["action"] == "ADD_CORRECTED_SLOT34_ROW"]
    counts = {direction: sum(row["direction(W/R)"] == direction for row in child) for direction in ("R", "W")}
    if counts != {"R": 26, "W": 26}:
        raise RuntimeError(f"CGuildStorageAttr child row count mismatch: {counts}")
    unknown = {
        direction: sum(
            row["direction(W/R)"] == direction
            and ("UNKNOWN" in row["new_field_offset"] or row["new_tag"] == "UNKNOWN")
            for row in child
        )
        for direction in ("R", "W")
    }
    if unknown != {"R": 18, "W": 18}:
        raise RuntimeError(f"CGuildStorageAttr child UNKNOWN count mismatch: {unknown}")
    priority_fields, priority = read_tsv(external / "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv")
    selected = [row for _line, row in priority if row["message"] == "CGuildStorageAttr"]
    if len(selected) != 1:
        raise RuntimeError("CGuildStorageAttr priority dependency cardinality mismatch")
    row = selected[0]
    if (
        row_key(priority_fields, row) != GUILD_PRIORITY_ROW_KEY
        or row["delta_key"] != GUILD_PRIORITY_KEY
        or row["base_file"] != "PF_PROTOCOL_PRIORITY.tsv"
        or row["base_line"] != "209"
        or row["base_row_key"] != "6695d6b2ee5e33bc81e62ccb0f825bba1cdef96314cbe19fb844912ef96235ec"
        or row["priority"] != "3"
        or row["new_serializer_status"] != "OPEN"
        or row["new_structural_status"] != "OPEN"
        or row["new_serializer_blockers"] != GUILD_BLOCKERS
        or row["new_blocker"] != GUILD_BLOCKERS
        or row["source"] != "IMAGE"
    ):
        raise RuntimeError("CGuildStorageAttr priority dependency mismatch")


def verify_no_prior_target(external: Path) -> None:
    expected = {(str(target.line), target.row_key) for target in TARGETS}
    collisions: list[str] = []
    for path in sorted(external.glob("*.tsv")):
        if path.name in OWNED_OUTPUTS:
            continue
        fields, rows = read_tsv(path)
        needed = {"base_file", "base_line", "base_row_key"}
        if not needed.issubset(fields):
            continue
        for line_no, row in rows:
            if row["base_file"] == "PF_SERIALIZER_FIELDS.tsv" and (row["base_line"], row["base_row_key"]) in expected:
                collisions.append(f"{path.name}:{line_no}")
    if collisions:
        raise RuntimeError("duplicate prior A2 target: " + ",".join(collisions))


def build_a2(external: Path) -> list[dict[str, str]]:
    fields, rows = read_tsv(external / "PF_SERIALIZER_FIELDS.tsv")
    by_line = {line: row for line, row in rows}
    output: list[dict[str, str]] = []
    for target in TARGETS:
        base = by_line.get(target.line)
        if base is None or row_key(fields, base) != target.row_key:
            raise RuntimeError(f"base A2 row mismatch at line {target.line}")
        if (
            base["message"] != target.message
            or base["direction(W/R)"] != target.direction
            or base["order"] != target.order
            or base["source"] != "IMAGE"
            or not base["tag"].startswith("JUMP_UNCLASSIFIED:INDIRECT")
            or "indirect_jump_not_proven_serializer" not in base["field_offset"]
        ):
            raise RuntimeError(f"base A2 fact drift at line {target.line}")
        changed = target.action == "CHANGED"
        values = {
            "action": target.action,
            "change_type": "STATIC_EMBEDDED_CHILD_COMPOSITION" if changed else "DIRECTIONALLY_IMPOSSIBLE_COARSE_ROW",
            "base_file": "PF_SERIALIZER_FIELDS.tsv",
            "base_line": str(target.line),
            "base_row_key": target.row_key,
            "base_delta_key": "N/A",
            "message": target.message,
            "direction(W/R)": target.direction,
            "old_order": base["order"],
            "old_tag": base["tag"],
            "old_field_offset": base["field_offset"],
            "old_len": base["len"],
            "new_wire_order": target.new_order,
            "new_tag": "STATIC_EMBEDDED_CHILD_REF" if changed else "N/A",
            "new_field_offset": "this+0x18" if changed else "N/A",
            "new_len": "N/A",
            "new_gate_condition": "DIRECTION_FORWARDED" if changed else "N/A",
            "resolution": "VTABLE_SLOT_0x34_STATIC_TARGET" if changed else "EXACT_PARENT_DIRECTION_BRANCH",
            "child_message": target.child,
            "child_receiver": "this+0x18",
            "child_vtable_va": f"0x{target.child_vtable:08X}",
            "child_slot": "+0x34",
            "child_serializer_va": f"0x{target.child_target:08X}",
            "child_effective_rows": str(target.child_rows),
            "child_effective_unknown_rows": str(target.child_unknown),
            "evidence_ticket": "STATIC-EMBEDDED-CHILD-COMPOSITION",
            "evidence_span_start": base["span_start"],
            "evidence_span_end": base["span_end"],
            "evidence_span_sha256": base["span_sha256"],
            "evidence_file_off": base["file_off_claim"],
            "source": "IMAGE",
        }
        values["delta_key"] = delta_key(("A2", target.action, target.row_key, target.child, target.direction, target.new_order))
        output.append(values)
    if len(output) != 6 or len({row["delta_key"] for row in output}) != 6:
        raise RuntimeError("A2 delta cardinality/key mismatch")
    if sum(row["action"] == "CHANGED" for row in output) != 4 or sum(row["action"].startswith("REMOVE") for row in output) != 2:
        raise RuntimeError("A2 delta action count mismatch")
    if any(row["message"] in {"DailyActivityState", "CGuildStorageAttr"} for row in output):
        raise RuntimeError("child field row was copied into parent delta")
    return output


def build_priority(external: Path) -> list[dict[str, str]]:
    fields, rows = read_tsv(external / "PF_V3_P1_OPEN.tsv")
    expected = {
        "ActorActivity_UpdateDailyActivityStateVital": (5, "fa02a0f1e1715fc6f8f9b999f2be6345a3b639223265b2c378f8b1991b919a35", "bb2509e7781ece1030897b75cea40b1e324635e30e7926a9c38ed49057bcdf00"),
        "DBSS_GuildStorageInitialVital": (36, "18cfc456c917108f28edaeec3409ea3d7c908663df063e830e0413cbc47e4411", "8b5e55e9abec890359065409783812e8d4c85313456ad74ea65e1d7fc9ce7341"),
    }
    by_message = {row["message"]: (line, row) for line, row in rows if row["message"] in expected}
    output: list[dict[str, str]] = []
    for message in expected:
        line, expected_row_key, status_key = expected[message]
        actual_line, base = by_message.get(message, (0, {}))
        if actual_line != line or row_key(fields, base) != expected_row_key or base.get("status_key") != status_key:
            raise RuntimeError(f"priority predecessor mismatch: {message}")
        if base["source"] != "IMAGE" or base["priority"] != "1" or base["effective_structural_status"] != "OPEN":
            raise RuntimeError(f"priority predecessor state drift: {message}")
        actor = message.startswith("ActorActivity_")
        child = "DailyActivityState" if actor else "CGuildStorageAttr"
        child_file = "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv" if actor else "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv"
        child_key = DAILY_PRIORITY_KEY if actor else GUILD_PRIORITY_KEY
        child_hash = PINNED[child_file]
        new_status = "CLOSED" if actor else "OPEN"
        new_blocker = "N/A" if actor else GUILD_BLOCKERS
        new_group = "N/A" if actor else "DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED"
        values = {
            "action": "CHANGED",
            "base_file": "PF_V3_P1_OPEN.tsv",
            "base_line": str(line),
            "base_row_key": expected_row_key,
            "base_delta_key": status_key,
            "message": message,
            "priority": "1",
            "old_registry_identity_status": base["effective_registry_identity_status"],
            "new_registry_identity_status": base["effective_registry_identity_status"],
            "old_registry_identity_missing": base["effective_registry_identity_missing"],
            "new_registry_identity_missing": base["effective_registry_identity_missing"],
            "old_serializer_status": base["effective_serializer_status"],
            "new_serializer_status": new_status,
            "old_serializer_blockers": base["effective_blocker"],
            "new_serializer_blockers": new_blocker,
            "old_structural_status": base["effective_structural_status"],
            "new_structural_status": new_status,
            "old_blocker": base["effective_blocker"],
            "new_blocker": new_blocker,
            "old_primary_blocker_group": base["primary_blocker_group"],
            "new_primary_blocker_group": new_group,
            "child_message": child,
            "child_priority_file": child_file,
            "child_priority_delta_key": child_key,
            "child_priority_file_sha256": child_hash,
            "evidence_ticket": "STATIC-EMBEDDED-CHILD-COMPOSITION",
            "closure_scope": "STATIC_WIRE_STRUCTURE_ONLY;EMBEDDED_CHILD_REFERENCE_ONLY;NO_CHILD_ROWS_COPIED;V3_IMMUTABLE",
            "source": "IMAGE",
        }
        values["delta_key"] = delta_key(("PRIORITY", message, status_key, child_key, new_status, new_group))
        output.append(values)
    if len(output) != 2 or len({row["delta_key"] for row in output}) != 2:
        raise RuntimeError("priority delta cardinality/key mismatch")
    return output


def report_text(
    a2_hash: str,
    priority_hash: str,
    script_hash: str,
    metrics: Mapping[str, int],
) -> str:
    span_lines = [
        f"| {pin.role} | `0x{pin.start:08X}` | `0x{pin.end:08X}` | `0x{pin.expected_off:08X}` | `{pin.sha256}` |"
        for pin in SPANS
    ]
    return "\n".join([
        "# PF embedded-child composition closure",
        "",
        "[MEASURED] This IMAGE-only additive overlay resolves two parent serializers through exact this+0x18 constructor composition and exact child-vtable slot +0x34 targets.",
        "",
        "## Outcome",
        "",
        f"- ActorActivity_UpdateDailyActivityStateVital: both coarse R/W indirect-jump rows become references to DailyActivityState. The pinned effective child has {metrics['daily_child_rows_r']} R + {metrics['daily_child_rows_w']} W rows and {metrics['daily_child_unknown']} UNKNOWN. Parent status changes OPEN to CLOSED.",
        "- DBSS_GuildStorageInitialVital: the E4 branch is W and the F3 branch is R. Two impossible coarse-direction rows are removed; the two valid rows become references to CGuildStorageAttr.",
        "- DBSS remains OPEN. Its old indirect-jump blocker is replaced by the pinned CGuildStorageAttr blocker set; the primary group is DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED.",
        f"- The A2 delta contains {metrics['a2_changed_references']} changed references and {metrics['a2_directional_removals']} removals. It contains zero child field rows and zero unchanged copied rows.",
        "",
        "## Duplicate control",
        "",
        "All six targets are exact frozen V1 line/full-row-hash pairs. The generator scans every pre-existing TSV for those pairs before publication and fails on any prior target. The child tables are dependencies referenced by hash and delta key, not materialized again.",
        "",
        "## Effective projection after Daily plus composition",
        "",
        f"- P1: {metrics['p1_closed']}/{metrics['p1_total']} CLOSED, {metrics['p1_total'] - metrics['p1_closed']} OPEN. P2: {metrics['p2_closed']}/{metrics['p2_total']} CLOSED. P3: {metrics['p3_closed']}/{metrics['p3_total']} CLOSED. Overall: {metrics['overall_closed']}/{metrics['overall_total']} CLOSED.",
        f"- Stored canonical A2 rows: {metrics['a2_stored_rows']}. Embedded-child reference rows: {metrics['a2_reference_rows']}. UNKNOWN A2 rows: {metrics['a2_unknown_rows']}. Generic CALL/JUMP UNKNOWN: {metrics['a2_generic_call_jump_unknown']}. Direct invalid-parameter UNKNOWN: {metrics['a2_direct_invalid_parameter_unknown']}.",
        f"- P1 blocker groups: call/effect {metrics['group_call_effect']}, dynamic {metrics['group_dynamic']}, indirect jump {metrics['group_indirect_jump']}, object/graph {metrics['group_object_graph']}, registry identity {metrics['group_registry_identity']}.",
        "",
        "## Verified IMAGE spans",
        "",
        "| role | start VA | end VA exclusive | file offset | SHA-256 |",
        "|---|---:|---:|---:|---|",
        *span_lines,
        "",
        "## Pins",
        "",
        f"- image SHA-256 before/after: `{IMAGE_SHA256}`",
        f"- Daily A2 dependency: `{PINNED['PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv']}`",
        f"- Daily priority dependency: `{PINNED['PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv']}`",
        f"- slot34 A2 dependency: `{PINNED['PF_A2_SERIALIZER_SLOT34_DELTA.tsv']}`",
        f"- V3 status predecessor: `{PINNED['PF_V3_P1_OPEN.tsv']}`",
        f"- `{A2_OUTPUT}`: `{a2_hash}`",
        f"- `{PRIORITY_OUTPUT}`: `{priority_hash}`",
        f"- generator: `{script_hash}`",
        "",
        "## Bounds",
        "",
        "This proves static embedded-child identity and the exact slot target only. It does not copy child fields, claim runtime capture validation, name an UNKNOWN runtime class, or resolve CGuildStorageAttr internal dynamic calls. No server, runtime, dump, capture, workflow, queue, Git, or GameClient file is changed.",
        "",
        "## Reproduction",
        "",
        f"Run `py -3 -B {Path(__file__).name} --audit-only`, then `--self-test`, the normal publish, and `--check`. The self-test injects KeyboardInterrupt after target-to-backup, proves a second actor cannot unlink/replace a held lock, and preserves a pre-existing foreign lock. Windows publication holds a CREATE_NEW kernel handle with READ-only sharing through the transaction; success marks FileDispositionInfo on that same handle, while failure closes without disposition and leaves lock/recovery. No pathname check-then-unlink is used. Daily closure uses the canonical full tag/offset/length/order/gate/unflattened-subcall predicate with built-in mutations.",
        "",
    ])


class HeldWindowsLock:
    """Windows lock owned by an open kernel handle, never by path re-check."""

    def __init__(self, path: Path, handle: int, kernel32: object) -> None:
        self.path = path
        self.handle = handle
        self.kernel32 = kernel32
        self.closed = False

    @classmethod
    def acquire(cls, path: Path) -> "HeldWindowsLock":
        if os.name != "nt":
            raise RuntimeError("publication requires Windows held-handle locking")
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateFileW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        )
        kernel32.CreateFileW.restype = wintypes.HANDLE
        kernel32.WriteFile.argtypes = (
            wintypes.HANDLE,
            wintypes.LPCVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        )
        kernel32.WriteFile.restype = wintypes.BOOL
        kernel32.FlushFileBuffers.argtypes = (wintypes.HANDLE,)
        kernel32.FlushFileBuffers.restype = wintypes.BOOL
        kernel32.SetFileInformationByHandle.argtypes = (
            wintypes.HANDLE,
            ctypes.c_int,
            wintypes.LPVOID,
            wintypes.DWORD,
        )
        kernel32.SetFileInformationByHandle.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        kernel32.CloseHandle.restype = wintypes.BOOL

        generic_read = 0x80000000
        generic_write = 0x40000000
        delete_access = 0x00010000
        file_share_read = 0x00000001
        create_new = 1
        file_attribute_normal = 0x00000080
        handle = kernel32.CreateFileW(
            str(path),
            generic_read | generic_write | delete_access,
            file_share_read,
            None,
            create_new,
            file_attribute_normal,
            None,
        )
        invalid = ctypes.c_void_p(-1).value
        if handle == invalid:
            error = ctypes.get_last_error()
            if error in (80, 183):
                raise RuntimeError(f"publication lock exists: {path.name}")
            raise OSError(error, f"CreateFileW CREATE_NEW failed: {path.name}")

        lock = cls(path, handle, kernel32)
        token = (
            f"owner=embedded-child-composition pid={os.getpid()} "
            f"nonce={os.urandom(16).hex()}\n"
        ).encode("ascii")
        buffer = ctypes.create_string_buffer(token)
        written = wintypes.DWORD(0)
        try:
            if not kernel32.WriteFile(
                handle, buffer, len(token), ctypes.byref(written), None
            ) or written.value != len(token):
                raise OSError(ctypes.get_last_error(), "lock WriteFile failed")
            if not kernel32.FlushFileBuffers(handle):
                raise OSError(ctypes.get_last_error(), "lock FlushFileBuffers failed")
        except BaseException:
            lock.close_preserve()
            raise
        return lock

    def close_preserve(self) -> None:
        if self.closed:
            return
        self.kernel32.CloseHandle(self.handle)
        self.closed = True

    def release_success(self) -> None:
        if self.closed:
            raise RuntimeError("lock handle already closed")
        import ctypes

        class FileDispositionInfo(ctypes.Structure):
            _fields_ = (("DeleteFile", ctypes.c_ubyte),)

        disposition = FileDispositionInfo(1)
        # FILE_INFO_BY_HANDLE_CLASS.FileDispositionInfo == 4.
        if not self.kernel32.SetFileInformationByHandle(
            self.handle,
            4,
            ctypes.byref(disposition),
            ctypes.sizeof(disposition),
        ):
            error = ctypes.get_last_error()
            self.close_preserve()
            raise OSError(error, "SetFileInformationByHandle(FileDispositionInfo) failed")
        if not self.kernel32.CloseHandle(self.handle):
            self.closed = True
            raise OSError(ctypes.get_last_error(), "lock CloseHandle failed")
        self.closed = True


def write_stage(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def publish_transaction(
    external: Path,
    outputs: Mapping[str, bytes],
    verify_inputs,
    *,
    inject_interrupt_after_backup: bool = False,
    lock_name: str = LOCK_NAME,
    tx_prefix: str = TX_PREFIX,
) -> None:
    lock = HeldWindowsLock.acquire(external / lock_name)
    tx_dir: Path | None = None
    success = False
    try:
        tx_dir = Path(tempfile.mkdtemp(prefix=tx_prefix, dir=external))
        staged: dict[str, Path] = {}
        for name, data in outputs.items():
            stage = tx_dir / (name + ".stage")
            write_stage(stage, data)
            staged[name] = stage
        verify_inputs()
        backups: dict[str, Path] = {}
        installed: list[str] = []
        try:
            for name in outputs:
                target = external / name
                backup = tx_dir / (name + ".backup")
                if target.exists():
                    # Journal the recovery path before the destructive move so
                    # an asynchronous BaseException in the next instruction
                    # still leaves rollback enough information.
                    backups[name] = backup
                    os.replace(target, backup)
                    if inject_interrupt_after_backup and len(backups) == 1:
                        raise KeyboardInterrupt(
                            "injected interrupt after target-to-backup"
                        )
                # Journal installation before replace for the same asynchronous
                # interruption boundary. A pre-marked but absent target is safe.
                installed.append(name)
                os.replace(staged[name], target)
            for name, data in outputs.items():
                target = external / name
                if target.read_bytes() != data:
                    raise RuntimeError(f"post-publish readback mismatch: {name}")
            verify_inputs()
        except BaseException as original:
            # The held handle prevents lock-path replacement throughout this
            # rollback. Any second interruption leaves the transaction tree.
            rollback_errors: list[str] = []
            for name in reversed(tuple(outputs)):
                target = external / name
                backup = backups.get(name)
                try:
                    if name in installed and target.exists():
                        target.unlink()
                    if backup is not None and backup.exists():
                        if target.exists():
                            raise RuntimeError("rollback target unexpectedly exists")
                        os.replace(backup, target)
                except BaseException as rollback_error:
                    rollback_errors.append(f"{name}:{rollback_error!r}")
            if rollback_errors:
                raise RuntimeError(
                    f"rollback failed; recovery preserved at {tx_dir}: "
                    + " | ".join(rollback_errors)
                ) from original
            raise
        # Success cleanup occurs while the unreplaceable handle is still held.
        if tx_dir.exists():
            shutil.rmtree(tx_dir)
        tx_dir = None
        lock.release_success()
        success = True
    except BaseException:
        # No disposition on any failure: the path remains as a fail-closed
        # recovery marker, and any transaction tree is deliberately preserved.
        lock.close_preserve()
        raise
    finally:
        if not success and not lock.closed:
            lock.close_preserve()


def transaction_adversarial_self_test(
    external: Path, outputs: Mapping[str, bytes], verify_inputs
) -> None:
    before = {
        name: (external / name).read_bytes()
        for name in outputs
        if (external / name).is_file()
    }
    if set(before) != set(outputs):
        raise RuntimeError("transaction self-test requires all owned outputs")
    nonce = os.urandom(8).hex()
    interrupt_lock_name = (
        f".PF_EMBEDDED_CHILD_COMPOSITION_SELFTEST_INTERRUPT.{nonce}.lock"
    )
    interrupt_tx_prefix = (
        f".PF_EMBEDDED_CHILD_COMPOSITION_SELFTEST_TXN.{nonce}."
    )
    interrupt_lock = external / interrupt_lock_name
    created_tx: list[Path] = []
    try:
        publish_transaction(
            external,
            outputs,
            verify_inputs,
            inject_interrupt_after_backup=True,
            lock_name=interrupt_lock_name,
            tx_prefix=interrupt_tx_prefix,
        )
    except KeyboardInterrupt as error:
        if str(error) != "injected interrupt after target-to-backup":
            raise
    else:
        raise RuntimeError("injected BaseException did not escape publication")
    after_interrupt = {name: (external / name).read_bytes() for name in outputs}
    if before != after_interrupt:
        raise RuntimeError("interrupt rollback changed an owned output")
    created_tx = [
        path for path in external.iterdir()
        if path.name.startswith(interrupt_tx_prefix)
    ]
    if not interrupt_lock.is_file() or len(created_tx) != 1:
        raise RuntimeError("failed publication did not preserve lock/recovery")
    # The harness owns these randomized failure sentinels and removes them only
    # after proving the publisher preserved them.
    shutil.rmtree(created_tx[0])
    interrupt_lock.unlink()

    held_path = external / (
        f".PF_EMBEDDED_CHILD_COMPOSITION_SELFTEST_HELD.{nonce}.lock"
    )
    replacement = external / (
        f".PF_EMBEDDED_CHILD_COMPOSITION_SELFTEST_REPLACE.{nonce}.tmp"
    )
    held = HeldWindowsLock.acquire(held_path)
    try:
        try:
            os.unlink(held_path)
        except OSError:
            pass
        else:
            raise RuntimeError("second actor unlinked a held lock")
        with replacement.open("xb") as handle:
            handle.write(b"replacement-self-test\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.replace(replacement, held_path)
        except OSError:
            pass
        else:
            raise RuntimeError("second actor replaced a held lock")
        if not replacement.is_file():
            raise RuntimeError("replace source disappeared during held-lock test")
        held.release_success()
        if held_path.exists() or replacement.read_bytes() != b"replacement-self-test\n":
            raise RuntimeError("handle release removed the wrong file identity")
    finally:
        held.close_preserve()
        replacement.unlink(missing_ok=True)
        if held_path.exists():
            held_path.unlink()

    # A pre-existing foreign lock must be rejected and left byte-identical.
    foreign = external / (
        f".PF_EMBEDDED_CHILD_COMPOSITION_SELFTEST_FOREIGN.{nonce}.lock"
    )
    foreign_token = b"foreign-lock-self-test\n"
    with foreign.open("xb") as handle:
        handle.write(foreign_token)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        try:
            HeldWindowsLock.acquire(foreign)
        except RuntimeError as error:
            if "publication lock exists" not in str(error):
                raise
        else:
            raise RuntimeError("pre-existing foreign lock was not rejected")
        if foreign.read_bytes() != foreign_token:
            raise RuntimeError("pre-existing foreign lock changed")
        if before != {name: (external / name).read_bytes() for name in outputs}:
            raise RuntimeError("lock self-tests changed an owned output")
    finally:
        if foreign.exists() and foreign.read_bytes() == foreign_token:
            foreign.unlink()

    residue = [
        path.name for path in external.iterdir()
        if nonce in path.name
    ]
    if residue:
        raise RuntimeError(f"lock self-test residue: {residue}")


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    workspace = here.parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", type=Path, default=here)
    parser.add_argument("--image", type=Path, default=workspace / "GameClient" / "GameClient.local.bin")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--audit-only", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    external = args.external.resolve()
    image_path = args.image.resolve()
    if not external.is_dir():
        raise RuntimeError("external directory missing")

    hashes_before = verify_pins(external, image_path)
    _image, _spans = verify_image(image_path)
    v3 = load_v3_validator(external)
    (
        _registry_rows,
        effective_v3,
        _candidate_schemas,
        v3_counts,
        _per_file_removals,
    ) = v3.apply_v3_removals(external)
    if v3_counts.get("effective_rows") != 8671:
        raise RuntimeError("pinned V3 effective A2 census drift")
    verify_daily_effective_child(external, v3, effective_v3)
    verify_guild_child(external)
    verify_no_prior_target(external)
    a2_rows = build_a2(external)
    priority_rows = build_priority(external)
    if any(row["source"] != "IMAGE" for row in a2_rows + priority_rows):
        raise RuntimeError("non-IMAGE output row")

    a2 = tsv_text(A2_COLUMNS, a2_rows)
    priority = tsv_text(PRIORITY_COLUMNS, priority_rows)
    metrics = recompute_effective_metrics(
        external, v3, effective_v3, a2_rows, priority_rows
    )
    script_hash = sha256_path(Path(__file__).resolve())
    report = report_text(
        sha256_bytes(a2.encode("utf-8")),
        sha256_bytes(priority.encode("utf-8")),
        script_hash,
        metrics,
    )
    outputs = {
        A2_OUTPUT: a2.encode("utf-8"),
        PRIORITY_OUTPUT: priority.encode("utf-8"),
        REPORT_OUTPUT: report.encode("utf-8"),
    }
    for name, data in outputs.items():
        data.decode("ascii")
        if b"\r" in data:
            raise RuntimeError(f"non-canonical newline in {name}")

    def reverify() -> None:
        verify_pins(external, image_path)

    if args.audit_only:
        mode = "audit-only"
    elif args.self_test:
        transaction_adversarial_self_test(external, outputs, reverify)
        mode = "self-test"
    elif args.check:
        for name, data in outputs.items():
            path = external / name
            if not path.is_file() or path.read_bytes() != data:
                raise RuntimeError(f"check output mismatch: {name}")
        mode = "check"
    else:
        publish_transaction(external, outputs, reverify)
        mode = "publish"

    hashes_after = verify_pins(external, image_path)
    if hashes_before != hashes_after:
        raise RuntimeError("protected input changed during run")
    print(f"PASS embedded-child composition mode={mode}")
    print(
        "a2_rows=%d changed=%d removed_directionally_impossible=%d "
        "child_rows_copied=%d"
        % (
            metrics["a2_delta_rows"],
            metrics["a2_changed_references"],
            metrics["a2_directional_removals"],
            metrics["a2_delta_rows"]
            - metrics["a2_changed_references"]
            - metrics["a2_directional_removals"],
        )
    )
    actor_status = next(
        row["new_structural_status"] for row in priority_rows
        if row["message"] == "ActorActivity_UpdateDailyActivityStateVital"
    )
    dbss_status = next(
        row["new_structural_status"] for row in priority_rows
        if row["message"] == "DBSS_GuildStorageInitialVital"
    )
    print(
        f"priority_rows={len(priority_rows)} actor={actor_status} dbss={dbss_status}"
    )
    print(
        "p1_closed=%d/%d p1_open=%d p2_closed=%d/%d p3_closed=%d/%d "
        "overall_closed=%d/%d"
        % (
            metrics["p1_closed"],
            metrics["p1_total"],
            metrics["p1_total"] - metrics["p1_closed"],
            metrics["p2_closed"],
            metrics["p2_total"],
            metrics["p3_closed"],
            metrics["p3_total"],
            metrics["overall_closed"],
            metrics["overall_total"],
        )
    )
    print(
        "a2_stored=%d a2_references=%d unknown=%d generic_call_jump=%d "
        "direct_invalid=%d"
        % (
            metrics["a2_stored_rows"],
            metrics["a2_reference_rows"],
            metrics["a2_unknown_rows"],
            metrics["a2_generic_call_jump_unknown"],
            metrics["a2_direct_invalid_parameter_unknown"],
        )
    )
    print(
        "groups_call=%d groups_dynamic=%d groups_indirect=%d "
        "groups_object=%d groups_registry=%d"
        % (
            metrics["group_call_effect"],
            metrics["group_dynamic"],
            metrics["group_indirect_jump"],
            metrics["group_object_graph"],
            metrics["group_registry_identity"],
        )
    )
    print(f"image_sha256_before={hashes_before['GameClient.local.bin']}")
    print(f"image_sha256_after={hashes_after['GameClient.local.bin']}")
    print(f"a2_sha256={sha256_bytes(outputs[A2_OUTPUT])}")
    print(f"priority_sha256={sha256_bytes(outputs[PRIORITY_OUTPUT])}")
    print(f"report_sha256={sha256_bytes(outputs[REPORT_OUTPUT])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
