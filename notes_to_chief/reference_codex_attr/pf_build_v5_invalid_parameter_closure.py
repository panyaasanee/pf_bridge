#!/usr/bin/env python3
"""Build the V5 IMAGE-only invalid-parameter non-wire closure component.

This builder is deliberately additive.  It proves ten exact callsites in two
serializers independently, emits removals for only their twenty exact V1 A2
rows, and chains two proposed Priority-1 closures from the frozen V4 OPEN
index.  An import name alone is never treated as a non-wire proof.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import dataclasses
import ctypes
import csv
import hashlib
import io
import json
import os
import re
import secrets
import shutil
import tempfile
import types
from collections import Counter
from dataclasses import dataclass
from ctypes import wintypes
from pathlib import Path
from typing import Mapping, Sequence


OUT = Path(__file__).resolve().parent
IMAGE = OUT.parents[1] / "GameClient" / "GameClient.local.bin"
IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
V4_MANIFEST_NAME = "PF_V4_MANIFEST.md"
V4_MANIFEST_SHA256 = "80c55db4f60739f0b1c8086cc28e568025678ce70056a9f045c3f9484443c8f3"
V4_MANIFEST_ROWS = 120
LOCK_NAME = ".PF_V5_INVALID_PARAMETER_PUBLISH.lock"
TX_PREFIX = ".PF_V5_INVALID_PARAMETER_TXN."

A2_OUT = OUT / "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv"
PRIORITY_OUT = OUT / "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv"
REPORT_OUT = OUT / "PF_V5_INVALID_PARAMETER_CLOSURE.md"
OWNED_OUTPUTS = (A2_OUT, PRIORITY_OUT, REPORT_OUT)
OWNED_NAMES = {path.name for path in OWNED_OUTPUTS}

PINNED_COMPONENTS = {
    "00_SEARCH_HERE_FIRST.md": "3c04c81025a9e7fe7f3866fc879ba3b2d0d2ea1379de445fbd379cd191d0575d",
    "PF_V4_P1_OPEN.tsv": "d612cd73c66f0e3717cd899c4f594118e2c57d8a215d6b1802b6da009e046123",
    "PF_V4_EFFECTIVE_STATUS.md": "15fa03ab107476cc8680b8c71385fde1161d74b23891785eaaba60b7fa6280b7",
    "PF_SERIALIZER_FIELDS.tsv": "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123",
    "PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv": "f0797f48bfa9115d237bd6e2ebab50e69334c8a05303f66f57bf5ea9b05274dd",
    "PF_A2_ITERATOR_HELPERS_NONWIRE_DELTA.tsv": "2916eeb565581e75cd1142920435087a19da3e15861427b4cd9f976854d25985",
    "PF_TARGET_652A30_A2_DELTA.tsv": "217f7f9854df7412ca942d755c0ed858130954f93c8384185af9719415720592",
    "PF_ITERATOR_HELPERS_NONWIRE.md": "6bd86eecea52b65159f1ce3b15f9417a059be93e6ddf1c78d1a17e9623ca7cab",
    "PF_TARGET_652A30_NONWIRE.md": "638383f97e8263839d79f566252738f79484ee53deeb34690f3dc3281d9d1994",
    "pf_extract_protocol.py": "0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e",
    "pf_validate_v2_effective_capture.py": "7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9",
    "pf_validate_v3_effective_capture.py": "3d145407c9a6e4236eefe829c9fb9eb0757bf53cce9ac9cb136f201f594a360b",
    "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv": "10b54ee781ad0147d5bd18c0171b88132d9fd61dc39e0adf6fa4055bc7b7890d",
    "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv": "b81c7a5590d60c44f10e4171a722feb680e0e83865e6c5c033121e9dccffbe00",
}

DAILY_A2_NAME = "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv"
COMPOSITION_A2_NAME = "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv"
V4_A2_OVERLAY_NAMES = (DAILY_A2_NAME, COMPOSITION_A2_NAME)
UNKNOWN_REASON_RE = re.compile(r"UNKNOWN\(([^)]+)\)")
REPORT_LABELS = (
    "[MEASURED][IMAGE]", "[MEASURED][OUTPUT-AUDIT]",
    "[PROPOSED][LOCAL]", "[PROPOSED][DERIVED]",
    "[NONCLAIM][LOCAL]", "[REPRODUCTION][LOCAL]", "[DECLARED-SCOPE]",
)

MANIFEST_ROW_RE = re.compile(
    r"^\| `([^`]+)` \| ([0-9]+) \| `([0-9A-Fa-f]{64})` \|", re.MULTILINE
)
VA_TO_FILE_DELTA = 0x00400C00
INVALID_IAT = 0x00C3B4C0
INVALID_CALL_BYTES = bytes.fromhex("ff15c0b4c300")
INVALID_CALL_SHA256 = "00ce047cf99a16facf7d68cb5e783c88fa394c8355e8a315a275a4a815f051cf"
INVALID_TAG = "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
INVALID_UNKNOWN = "UNKNOWN(invalid_parameter_import_call_wire_effect_unproved)"
EVIDENCE_TICKET = "STATIC-V5-INVALID-PARAMETER-SERVER-ITEMMALL"

A2_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line",
    "base_row_key", "base_delta_key", "message", "direction(W/R)",
    "old_order", "old_tag", "old_field_offset", "old_len",
    "new_wire_order", "new_tag", "new_field_offset", "new_len",
    "new_gate_condition", "resolution", "evidence_ticket",
    "evidence_span_start", "evidence_span_end", "evidence_span_sha256",
    "evidence_file_off", "source",
)

PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "priority",
    "old_registry_identity_status", "new_registry_identity_status",
    "old_registry_identity_missing", "new_registry_identity_missing",
    "old_serializer_status", "new_serializer_status",
    "old_serializer_blockers", "new_serializer_blockers",
    "old_structural_status", "new_structural_status",
    "old_blocker", "new_blocker", "evidence_ticket", "closure_scope",
    "source",
)


class BuildError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_row_key(fields: Sequence[str], row: Mapping[str, str]) -> str:
    raw = json.dumps(
        [row[name] for name in fields], ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(raw)


def make_delta_key(parts: Sequence[str]) -> str:
    return sha256_bytes("\x1f".join(parts).encode("ascii"))


def read_tsv(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise BuildError(f"bad or duplicate TSV header: {path.name}")
        fields = list(reader.fieldnames)
        rows: list[tuple[int, dict[str, str]]] = []
        for line, raw in enumerate(reader, start=2):
            if None in raw or any(value is None for value in raw.values()):
                raise BuildError(f"malformed TSV row: {path.name}:{line}")
            rows.append((line, dict(raw)))
    return fields, rows


def format_tsv(fields: Sequence[str], rows: Sequence[Mapping[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=list(fields), delimiter="\t", lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def parse_v4_manifest() -> dict[str, tuple[int, str]]:
    manifest = OUT / V4_MANIFEST_NAME
    if not manifest.is_file() or sha256_path(manifest) != V4_MANIFEST_SHA256:
        raise BuildError("frozen V4 manifest identity changed")
    entries = MANIFEST_ROW_RE.findall(manifest.read_text(encoding="utf-8"))
    if len(entries) != V4_MANIFEST_ROWS:
        raise BuildError(f"V4 manifest row census changed: {len(entries)}")
    result: dict[str, tuple[int, str]] = {}
    for name, size_text, digest in entries:
        if name in result:
            raise BuildError(f"duplicate V4 manifest entry: {name}")
        result[name] = (int(size_text), digest.lower())
    if V4_MANIFEST_NAME in result or OWNED_NAMES.intersection(result):
        raise BuildError("V4 manifest unexpectedly contains V5-owned output")
    return result


def verify_inputs() -> dict[str, str]:
    entries = parse_v4_manifest()
    measured = {V4_MANIFEST_NAME: V4_MANIFEST_SHA256}
    for name, (expected_size, expected_hash) in entries.items():
        path = OUT / name
        if not path.is_file() or path.stat().st_size != expected_size:
            raise BuildError(f"V4 component missing/size drift: {name}")
        actual = sha256_path(path)
        if actual != expected_hash:
            raise BuildError(f"V4 component hash drift: {name}: {actual}")
        measured[name] = actual
    for name, expected in PINNED_COMPONENTS.items():
        entry = entries.get(name)
        if entry is None or entry[1] != expected:
            raise BuildError(f"required V4 component pin changed: {name}")
    if not IMAGE.is_file() or IMAGE.stat().st_size != IMAGE_SIZE:
        raise BuildError("pinned GameClient.local.bin size changed")
    image_hash = sha256_path(IMAGE)
    if image_hash != IMAGE_SHA256:
        raise BuildError(f"pinned GameClient.local.bin hash changed: {image_hash}")
    measured[IMAGE.name] = image_hash
    if (OUT / "PF_V5_FIELD_VALIDATION.tsv").exists():
        raise BuildError("forbidden duplicate A5 TSV exists")
    return measured


def load_decoder() -> types.ModuleType:
    path = OUT / "pf_extract_protocol.py"
    if sha256_path(path) != PINNED_COMPONENTS[path.name]:
        raise BuildError("pinned decoder source changed")
    source = path.read_bytes()
    name = "_pf_v5_pinned_extract_protocol_0bb792bb"
    if name in sys.modules:
        raise BuildError("pinned decoder module-name collision")
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[name] = module
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def load_v3_replay_modules() -> tuple[types.ModuleType, types.ModuleType]:
    """Load the frozen V2/V3 A2 replay without importing or writing bytecode."""
    v2_path = OUT / "pf_validate_v2_effective_capture.py"
    v3_path = OUT / "pf_validate_v3_effective_capture.py"
    for path in (v2_path, v3_path):
        expected = PINNED_COMPONENTS[path.name]
        if not path.is_file() or sha256_path(path) != expected:
            raise BuildError(f"pinned replay source changed: {path.name}")
    v2_name = "_pf_v5_pinned_v2_replay_7a9c0801"
    v3_name = "_pf_v5_pinned_v3_replay_3d145407"
    canonical_v2 = "pf_validate_v2_effective_capture"
    if any(name in sys.modules for name in (v2_name, v3_name, canonical_v2)):
        raise BuildError("pinned replay module-name collision")

    v2 = types.ModuleType(v2_name)
    v2.__file__ = str(v2_path)
    v2.__package__ = ""
    v3 = types.ModuleType(v3_name)
    v3.__file__ = str(v3_path)
    v3.__package__ = ""
    sys.modules[v2_name] = v2
    try:
        exec(compile(v2_path.read_bytes(), str(v2_path), "exec"), v2.__dict__)
        sys.modules[canonical_v2] = v2
        sys.modules[v3_name] = v3
        try:
            exec(compile(v3_path.read_bytes(), str(v3_path), "exec"), v3.__dict__)
        finally:
            sys.modules.pop(canonical_v2, None)
    except BaseException:
        sys.modules.pop(v2_name, None)
        sys.modules.pop(v3_name, None)
        raise
    return v2, v3


def source_row(path: Path, line: int) -> tuple[list[str], dict[str, str]]:
    fields, rows = read_tsv(path)
    matches = [row for row_line, row in rows if row_line == line]
    if len(matches) != 1:
        raise BuildError(f"missing exact source row: {path.name}:{line}")
    return fields, matches[0]


def clone_effective(effective: Mapping[tuple[str, str], Sequence[object]]) -> dict:
    return {semantic: list(rows) for semantic, rows in effective.items()}


def measure_effective(v2: types.ModuleType, effective: Mapping[tuple[str, str], Sequence[object]]) -> dict[str, int]:
    flat = [value for rows in effective.values() for value in rows]
    numeric = Counter(
        value.tag for value in flat if v2.NUMERIC_TAG_RE.fullmatch(value.tag)
    )
    return {
        "a2_rows": len(flat),
        "a2_unknown": sum(
            value.tag == "UNKNOWN"
            or bool(UNKNOWN_REASON_RE.search(str(value.field_offset)))
            for value in flat
        ),
        "generic_unknown": sum(
            value.tag.startswith(("CALL_UNCLASSIFIED:", "JUMP_UNCLASSIFIED:"))
            for value in flat
        ),
        "direct_invalid": sum(value.tag == INVALID_TAG for value in flat),
        "a3": sum(numeric.values()),
    }


def replay_v4_effective_a2(
    v2: types.ModuleType, v3: types.ModuleType, v4_metrics: Mapping[str, int]
) -> tuple[dict, dict[str, int]]:
    """Rebuild V4 A2 from the frozen base and every ordered pre-V5 overlay."""
    try:
        _registry, effective, _candidates, counts, v3_per_file = v3.apply_v3_removals(OUT)
    except v2.ValidationError as exc:
        raise BuildError(f"frozen V2/V3 A2 replay rejected inputs: {exc}") from exc
    if counts.get("effective_rows") != 8671:
        raise BuildError(f"frozen V3 effective-row census drift: {counts}")

    index: dict[tuple[str, str, str], tuple[tuple[str, str], object]] = {}
    for semantic, rows in effective.items():
        for value in rows:
            lookup = (semantic[0], semantic[1], value.evidence_key)
            if lookup in index:
                raise BuildError(f"duplicate V3 effective evidence key: {lookup}")
            index[lookup] = (semantic, value)

    seen_keys: set[str] = set()
    seen_targets: set[tuple[str, str, str]] = set()
    overlay_counts: Counter[str] = Counter()
    overlay_rows_total = 0
    for name in V4_A2_OVERLAY_NAMES:
        fields, rows = read_tsv(OUT / name)
        required = {
            "delta_key", "action", "base_file", "base_line", "base_row_key",
            "base_delta_key", "message", "direction(W/R)", "old_order",
            "old_tag", "old_field_offset", "old_len", "source",
        }
        if not required.issubset(fields):
            raise BuildError(f"V4 A2 overlay schema drift: {name}")
        overlay_rows_total += len(rows)
        for _line, row in rows:
            if row["source"] != "IMAGE":
                raise BuildError(f"mixed source in V4 A2 overlay: {name}")
            if not row["delta_key"] or row["delta_key"] == "N/A" or row["delta_key"] in seen_keys:
                raise BuildError(f"duplicate/empty V4 A2 delta key: {name}")
            seen_keys.add(row["delta_key"])
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            if "N/A" in target or target in seen_targets:
                raise BuildError(f"duplicate/invalid V4 A2 target: {name}:{target}")
            seen_targets.add(target)

            try:
                base_line = int(row["base_line"])
            except ValueError as exc:
                raise BuildError(f"non-numeric V4 A2 base line: {name}") from exc
            source_fields, base = source_row(OUT / row["base_file"], base_line)
            if canonical_row_key(source_fields, base) != row["base_row_key"]:
                raise BuildError(f"V4 A2 source identity drift: {name}:{base_line}")
            if base.get("source") != "IMAGE":
                raise BuildError(f"V4 A2 predecessor source drift: {name}:{base_line}")
            if row["base_file"] == "PF_SERIALIZER_FIELDS.tsv":
                if row["base_delta_key"] != "N/A":
                    raise BuildError(f"V4 V1 target has a delta predecessor: {name}")
                evidence_key = row["base_row_key"]
            elif row["base_file"] == "PF_A2_SERIALIZER_SLOT34_DELTA.tsv":
                evidence_key = row["base_delta_key"]
                if not evidence_key or evidence_key == "N/A" or base.get("delta_key") != evidence_key:
                    raise BuildError(f"V4 slot34 predecessor identity drift: {name}")
            else:
                raise BuildError(f"unsupported V4 A2 predecessor: {row['base_file']}")

            lookup = (row["message"], row["direction(W/R)"], evidence_key)
            match = index.get(lookup)
            if match is None:
                raise BuildError(f"V4 A2 target is not still effective: {name}:{lookup}")
            semantic, old = match
            if (
                old.wire_order, old.tag, old.field_offset, old.length
            ) != (
                row["old_order"], row["old_tag"], row["old_field_offset"], row["old_len"]
            ):
                raise BuildError(f"V4 A2 old-row contract mismatch: {name}:{lookup}")
            effective[semantic].remove(old)
            del index[lookup]
            action = row["action"]
            if action == "CHANGED":
                needed = {
                    "new_wire_order", "new_tag", "new_field_offset", "new_len",
                    "new_gate_condition", "child_message", "child_effective_rows",
                    "child_effective_unknown_rows",
                }
                if not needed.issubset(fields):
                    raise BuildError(f"V4 composition schema drift: {name}")
                child_rows = effective[(row["child_message"], row["direction(W/R)"])]
                child_unknown = sum(
                    value.tag == "UNKNOWN"
                    or bool(UNKNOWN_REASON_RE.search(str(value.field_offset)))
                    for value in child_rows
                )
                if (
                    len(child_rows) != int(row["child_effective_rows"])
                    or child_unknown != int(row["child_effective_unknown_rows"])
                ):
                    raise BuildError(f"V4 child reference census drift: {name}:{lookup}")
                replacement = dataclasses.replace(
                    old,
                    field_identity=old.field_identity + ";V4REF:" + row["delta_key"],
                    wire_order=row["new_wire_order"], tag=row["new_tag"],
                    length=row["new_len"], field_offset=row["new_field_offset"],
                    gate_condition=row["new_gate_condition"],
                    provenance="V4_STATIC_EMBEDDED_CHILD_REFERENCE",
                    evidence_key=row["delta_key"],
                )
                effective[semantic].append(replacement)
                replacement_lookup = (semantic[0], semantic[1], replacement.evidence_key)
                if replacement_lookup in index:
                    raise BuildError(f"V4 replacement evidence key collision: {replacement_lookup}")
                index[replacement_lookup] = (semantic, replacement)
            elif not action.startswith("REMOVE"):
                raise BuildError(f"unsupported V4 A2 action: {name}:{action}")
            overlay_counts[name] += 1

    if len(seen_keys) != overlay_rows_total or len(seen_targets) != overlay_rows_total:
        raise BuildError("V4 overlay replay left unaccounted delta keys/targets")
    for rows in effective.values():
        rows.sort(key=lambda value: value.sequence)
    try:
        v2.validate_effective_tag_census(OUT, effective)
    except v2.ValidationError as exc:
        raise BuildError(f"V4 replay A3 census failed: {exc}") from exc
    measured = measure_effective(v2, effective)
    expected = {
        key: v4_metrics[key]
        for key in ("a2_rows", "a2_unknown", "generic_unknown", "direct_invalid", "a3")
    }
    if measured != expected:
        raise BuildError(f"independent V4 effective A2 replay drift: {measured} != {expected}")
    measured.update({
        "v3_overlay_files": len(v3_per_file),
        "v3_overlay_directives": sum(v3_per_file.values()),
        "v4_overlay_files": len(overlay_counts),
        "v4_overlay_directives": sum(overlay_counts.values()),
        "v4_overlay_targets_accounted": len(seen_targets),
    })
    return effective, measured


def blocker_reasons(value: object) -> tuple[str, ...]:
    reasons: set[str] = set()
    critical = (
        str(value.tag), str(value.field_offset), str(value.length),
        str(value.gate_condition),
    )
    for text in critical:
        reasons.update(UNKNOWN_REASON_RE.findall(text))
    tag = str(value.tag)
    if tag == "UNKNOWN":
        reasons.add("unknown_tag")
    if tag.startswith(("CALL_UNCLASSIFIED:", "JUMP_UNCLASSIFIED:")):
        reasons.add("unclassified_control_transfer")
    if tag == INVALID_TAG:
        reasons.add("invalid_parameter_call_effect_unproved")
    for token in ("UNPROVED", "UNRESOLVED", "AMBIGUOUS"):
        if any(token in text.upper() for text in critical):
            reasons.add(token.lower())
    return tuple(sorted(reasons))


def is_nonempty_proven_wire(value: object) -> bool:
    if blocker_reasons(value):
        return False
    if str(value.tag) in {"EMPTY", "PURE_READONLY_CHAIN_PLUS_04_CONTAINS_PREDICATE"}:
        return False
    return str(value.length) not in {"", "0", "N/A"}


def apply_v5_removals(
    v2: types.ModuleType,
    effective_v4: Mapping[tuple[str, str], Sequence[object]],
    a2_rows: Sequence[Mapping[str, str]],
) -> tuple[dict, dict[str, dict[str, dict[str, int]]], dict[str, int]]:
    effective = clone_effective(effective_v4)
    index: dict[tuple[str, str, str], tuple[tuple[str, str], object]] = {}
    for semantic, rows in effective.items():
        for value in rows:
            lookup = (semantic[0], semantic[1], value.evidence_key)
            if lookup in index:
                raise BuildError(f"duplicate V4 effective evidence key before V5: {lookup}")
            index[lookup] = (semantic, value)

    declared_targets: set[tuple[str, str, str]] = set()
    applied_targets: set[tuple[str, str, str]] = set()
    applied_keys: set[str] = set()
    removed_by_semantic: Counter[tuple[str, str]] = Counter()
    removed_values: list[object] = []
    for row in a2_rows:
        if row["source"] != "IMAGE" or row["action"] != "REMOVE_NONWIRE_ROW":
            raise BuildError("V5 replay received a non-IMAGE/non-removal row")
        target = (row["base_file"], row["base_line"], row["base_row_key"])
        if target in declared_targets or row["delta_key"] in applied_keys:
            raise BuildError(f"duplicate V5 replay target/key: {target}")
        declared_targets.add(target)
        applied_keys.add(row["delta_key"])
        if row["base_file"] != "PF_SERIALIZER_FIELDS.tsv" or row["base_delta_key"] != "N/A":
            raise BuildError(f"V5 replay target is not an exact V1 row: {target}")
        source_fields, base = source_row(OUT / row["base_file"], int(row["base_line"]))
        if canonical_row_key(source_fields, base) != row["base_row_key"]:
            raise BuildError(f"V5 replay source identity drift: {target}")
        lookup = (row["message"], row["direction(W/R)"], row["base_row_key"])
        match = index.get(lookup)
        if match is None:
            raise BuildError(f"V5 target is not uniquely still effective: {lookup}")
        semantic, old = match
        if (
            old.wire_order, old.tag, old.field_offset, old.length
        ) != (
            row["old_order"], row["old_tag"], row["old_field_offset"], row["old_len"]
        ):
            raise BuildError(f"V5 replay old-row contract mismatch: {lookup}")
        effective[semantic].remove(old)
        del index[lookup]
        applied_targets.add(target)
        removed_by_semantic[semantic] += 1
        removed_values.append(old)

    if declared_targets != applied_targets or len(applied_keys) != len(a2_rows):
        raise BuildError("V5 replay left unaccounted delta targets")
    if any(value.tag != INVALID_TAG or not blocker_reasons(value) for value in removed_values):
        raise BuildError("V5 replay removed a row outside the proven blocker class")
    for rows in effective.values():
        rows.sort(key=lambda value: value.sequence)
    try:
        v2.validate_effective_tag_census(OUT, effective)
    except v2.ValidationError as exc:
        raise BuildError(f"post-V5 replay A3 census failed: {exc}") from exc

    closure: dict[str, dict[str, dict[str, int]]] = {}
    for message in sorted(PRIORITY_PINS):
        closure[message] = {}
        for direction in ("W", "R"):
            semantic = (message, direction)
            rows = effective.get(semantic)
            if rows is None:
                raise BuildError(f"post-V5 semantic bucket missing: {semantic}")
            blockers = [value for value in rows if blocker_reasons(value)]
            proven = [value for value in rows if is_nonempty_proven_wire(value)]
            expected_delta_rows = sum(
                row["message"] == message and row["direction(W/R)"] == direction
                for row in a2_rows
            )
            applied = removed_by_semantic[semantic]
            if applied != expected_delta_rows or expected_delta_rows == 0:
                raise BuildError(
                    f"unaccounted V5 delta targets for {message}/{direction}: "
                    f"declared={expected_delta_rows} applied={applied}"
                )
            if blockers:
                detail = sorted({reason for value in blockers for reason in blocker_reasons(value)})
                raise BuildError(
                    f"residual serializer/structural blockers for {message}/{direction}: "
                    f"rows={len(blockers)} reasons={detail}"
                )
            if not proven:
                raise BuildError(f"no non-empty proven wire row remains: {message}/{direction}")
            closure[message][direction] = {
                "rows_after": len(rows),
                "removed": applied,
                "residual_blockers": len(blockers),
                "proven_wire_rows": len(proven),
            }
    final_metrics = measure_effective(v2, effective)
    return effective, closure, final_metrics


@dataclass(frozen=True)
class FunctionPin:
    message: str
    start_va: int
    end_va: int
    file_off: int
    sha256: str
    cfg_nodes: int
    cfg_edges: int
    covered_bytes: int
    direct_calls: int
    indirect_calls: int
    w_entry: int
    r_entry: int
    mode_branch: int
    this_reg: str
    this_definition: int
    writer_stream_reg: str
    writer_stream_definition: int
    reader_stream_reg: str
    reader_stream_definition: int
    b0_call: int
    b0_receiver: int
    tree_call: int
    tree_receiver: int
    invalid_sites: tuple[int, ...]


FUNCTIONS = (
    FunctionPin(
        "ServerAddedInfoVital", 0x005EBCF0, 0x005EBE33, 0x001EB0F0,
        "f3608dd2456f8577a585e35164b6990d465abb1ffd73697ff7f103e4cbd34960",
        109, 118, 323, 8, 5, 0x005EBD0D, 0x005EBDB5, 0x005EBD07,
        "ebx", 0x005EBCFC, "ecx", 0x005EBD11, "edi", 0x005EBDB5,
        0x005EBD9E, 0x005EBD9A, 0x005EBE1C, 0x005EBE16,
        (0x005EBD3E, 0x005EBD50, 0x005EBD5D, 0x005EBD7A, 0x005EBD85),
    ),
    FunctionPin(
        "ItemMallUpdatePersonalDataVital", 0x006B0D20, 0x006B0FBC, 0x002B0120,
        "142b0ecac21efcf62367aec12d0dfab558c0bdd66428b8f2922a6b89367cd664",
        193, 212, 536, 18, 5, 0x006B0D36, 0x006B0E57, 0x006B0D30,
        "edi", 0x006B0D2C, "ebx", 0x006B0D36, "esi", 0x006B0E57,
        0x006B0E40, 0x006B0E3C, 0x006B0F27, 0x006B0F20,
        (0x006B0DE2, 0x006B0DF6, 0x006B0E03, 0x006B0E1C, 0x006B0E27),
    ),
)


@dataclass(frozen=True)
class GuardPin:
    call_va: int
    condition: str
    window_va: int
    window_hex: str
    window_sha256: str


GUARDS = (
    GuardPin(0x005EBD3E, "NULL_OR_UNEXPECTED_NODE_GUARD", 0x005EBD36, "85f674043bf07406ff15c0b4c300", "aecc6aa81e414c6522b5c37aa5e8364302902296d7baf4d7f8a7ed7f39e0f1c0"),
    GuardPin(0x005EBD50, "NULL_NODE_GUARD", 0x005EBD4C, "85f6755dff15c0b4c300", "868bcb2426a7086b41810ac69269ab06c3cb0412bf2bbfff4031e364a04c4315"),
    GuardPin(0x005EBD5D, "NODE_BOUNDARY_EQUALITY_GUARD", 0x005EBD58, "3b78187506ff15c0b4c300", "bd10d03f2383a2e06e1b3f41df2c2422248ab4b53b9c65b8f0e9ac7f8f326c2b"),
    GuardPin(0x005EBD7A, "NULL_NODE_GUARD", 0x005EBD76, "85f67537ff15c0b4c300", "527c476e67825fdcd959be795013af1b15ee5fa3b2334b1a63e34b159d6addc6"),
    GuardPin(0x005EBD85, "NODE_BOUNDARY_EQUALITY_GUARD", 0x005EBD80, "3b7e187506ff15c0b4c300", "9b8b78c956e485cb381f1c0848ed3da745b7c14f51a9eaaf72add6261874cd8f"),
    GuardPin(0x006B0DE2, "NULL_OR_UNEXPECTED_NODE_GUARD", 0x006B0DDA, "85f674043bf07406ff15c0b4c300", "aecc6aa81e414c6522b5c37aa5e8364302902296d7baf4d7f8a7ed7f39e0f1c0"),
    GuardPin(0x006B0DF6, "NULL_NODE_GUARD", 0x006B0DF2, "85f67559ff15c0b4c300", "7cc6dc1936d93920ddcd3ae44c737c6499908c332cb929486ad5b982df6704f7"),
    GuardPin(0x006B0E03, "NODE_BOUNDARY_EQUALITY_GUARD", 0x006B0DFE, "3b68187506ff15c0b4c300", "071ba0b21aae381f038fe119ea3ae707f0e6082a6fa9066e875c355b1a936694"),
    GuardPin(0x006B0E1C, "NULL_NODE_GUARD", 0x006B0E18, "85f67537ff15c0b4c300", "527c476e67825fdcd959be795013af1b15ee5fa3b2334b1a63e34b159d6addc6"),
    GuardPin(0x006B0E27, "NODE_BOUNDARY_EQUALITY_GUARD", 0x006B0E22, "3b6e187506ff15c0b4c300", "b70f86eb14db6247191d77f9112da8b22f8edb4fe53ade005c423cb00335a829"),
)

GUARD_BY_SITE = {pin.call_va: pin for pin in GUARDS}
if len(GUARD_BY_SITE) != len(GUARDS):
    raise BuildError("duplicate static guard pin")


ROW_PINS = {
    966: ("1c9574b34ce501cff81d63c68ebfbd437b0c2ae76d95d63245d98117619804cd", "ServerAddedInfoVital", "R", 0x005EBD3E),
    967: ("5e4682e2355b11554e4a3c52b24355bb4dde629a9199d2dcf4f1c97cd24db93f", "ServerAddedInfoVital", "W", 0x005EBD3E),
    968: ("bb4a94fe2830fea38f6e50b74feac0512a3f5c6b7f65e684fb533d376cc34e7c", "ServerAddedInfoVital", "R", 0x005EBD50),
    969: ("b8ee6bd091e971922517ea255bf2e03e1a9ffbea52b84575e10b37359c08a8e7", "ServerAddedInfoVital", "W", 0x005EBD50),
    970: ("f4ea8f28086822f2ceb550a964274c8f572b08dbed9b56d48d62f5872de8202f", "ServerAddedInfoVital", "R", 0x005EBD5D),
    971: ("154a3bd92502928e8fc9256e35df6a9cb132a993b0a6b6ff72016b27924bfc10", "ServerAddedInfoVital", "W", 0x005EBD5D),
    973: ("daeee979ab174ab1d5a2eef1cd7d3e26efe013222250a68cf0542fc87902795b", "ServerAddedInfoVital", "R", 0x005EBD7A),
    974: ("1c65fafbade6b1a73c6eb1d8f9a2294150d62c40caa2fba3d62fc0bacce53a61", "ServerAddedInfoVital", "W", 0x005EBD7A),
    975: ("3e87140b63ddad1d51636508a7b162e422a96547cd8b2c559e7b3774b28410ce", "ServerAddedInfoVital", "R", 0x005EBD85),
    976: ("4e7928b241062204685c200ee8ac0547a068671a4bcab63ee40d5c35964e3967", "ServerAddedInfoVital", "W", 0x005EBD85),
    4671: ("8288ee585f0ccc83cad46f68c9b4f4d8e0ffb76b529da350c59397b1ff713851", "ItemMallUpdatePersonalDataVital", "R", 0x006B0DE2),
    4672: ("86c0843a7bcdc0147f0bb5a1f22048ed2ea2e2e3dd98ef0acf78313d17acd2f7", "ItemMallUpdatePersonalDataVital", "W", 0x006B0DE2),
    4673: ("3b5368e926d8d0d655833df15b3d5eef5814abea299de0467cdbfb3671e340b6", "ItemMallUpdatePersonalDataVital", "R", 0x006B0DF6),
    4674: ("4d8dfa4b972a903ce4abd91aa8ed4b025de64444b0ec3ccd7bb0f562eb6a23e7", "ItemMallUpdatePersonalDataVital", "W", 0x006B0DF6),
    4675: ("1a1ed91687b676612e6b353310fcfff8fdd3ebdb5af49ef63addf81f5218e2c6", "ItemMallUpdatePersonalDataVital", "R", 0x006B0E03),
    4676: ("20e41a1f38f0123dd1899237bf49a85c8622245b32d55624e4dd10c626fcf419", "ItemMallUpdatePersonalDataVital", "W", 0x006B0E03),
    4678: ("23438aea223bff7a6236e585fb254b14209d02f2c7a54a6a722c9db1d2aef5f0", "ItemMallUpdatePersonalDataVital", "R", 0x006B0E1C),
    4679: ("9ee40578c4088d943109ec27d22d04474056b4a374270182746f0027d350bfe5", "ItemMallUpdatePersonalDataVital", "W", 0x006B0E1C),
    4680: ("9ce95f0024e4aa9c4ebde9ec7fc1180b75903faa80aa52e67aba101a0634ac1e", "ItemMallUpdatePersonalDataVital", "R", 0x006B0E27),
    4681: ("6bb7967499a0ecda78964d6f7669dc4f5cd3a3391d7469af857f4af058e61fff", "ItemMallUpdatePersonalDataVital", "W", 0x006B0E27),
}

PRIORITY_PINS = {
    "ItemMallUpdatePersonalDataVital": (77, "f678e9548a3031e2604dffca4e88f2119134673ecea2a64bd91dfa52ab1b8eca", "fd8c6030e96788145cda663ce2323b22785448db18a047e8161b296214a4543e"),
    "ServerAddedInfoVital": (96, "4e6216c17279b981968c78c17e09dca2d65222c931b1e48ee64f9370a2b14f69", "1152946cae5a93209a40373a511024050285265def9cc2783602575b2cfb19a3"),
}

HELPER_SPANS = (
    ("stack_local_link_state", 0x00B0BF70, 0x00B0BFDC, 0x0070B370, "4e1374fd126457c82d11bf3e6efa0fda845bb85e2c2a985ed67c4eff3f4eb7e6"),
    ("ordered_tree", 0x00652A30, 0x00652B1F, 0x00251E30, "fc953d5b6890f65b63eaa8c90dd5cf8afb97fbbcc787da643fd58d14482675f8"),
    ("ordered_tree_insert", 0x00652550, 0x0065292F, 0x00251950, "868ba1b4f464944d421e4f1f19e1893641874ce64a67221c247e2fba78c75a03"),
    ("ordered_tree_advance", 0x00767170, 0x007671F4, 0x00366570, "cf948a67e84ac3e0a9d0db0909efebefb9a7364c7550adb552c9b23353e48de8"),
)


def raw_at(image: bytes, va: int, size: int) -> bytes:
    off = va - VA_TO_FILE_DELTA
    if off < 0 or off + size > len(image):
        raise BuildError(f"IMAGE VA outside pinned raw mapping: 0x{va:08X}")
    return image[off:off + size]


def require_bytes(image: bytes, va: int, encoded: str, label: str) -> None:
    expected = bytes.fromhex(encoded)
    actual = raw_at(image, va, len(expected))
    if actual != expected:
        raise BuildError(f"{label} byte drift at 0x{va:08X}: {actual.hex()}")


def reachable(decoded: object, start: int) -> frozenset[int]:
    if start not in decoded.instructions:
        return frozenset()
    seen: set[int] = set()
    work = [start]
    while work:
        node = work.pop()
        if node in seen or node not in decoded.instructions:
            continue
        seen.add(node)
        work.extend(decoded.successors.get(node, ()))
    return frozenset(seen)


def dominators(decoded: object) -> dict[int, frozenset[int]]:
    nodes = set(decoded.instructions)
    entry = decoded.span.start_va
    values: dict[int, set[int]] = {
        node: ({entry} if node == entry else set(nodes)) for node in nodes
    }
    changed = True
    while changed:
        changed = False
        for node in sorted(nodes - {entry}):
            predecessors = [p for p in decoded.predecessors.get(node, ()) if p in nodes]
            if not predecessors:
                updated = {node}
            else:
                updated = set(values[predecessors[0]])
                for predecessor in predecessors[1:]:
                    updated.intersection_update(values[predecessor])
                updated.add(node)
            if updated != values[node]:
                values[node] = updated
                changed = True
    return {node: frozenset(group) for node, group in values.items()}


def require_single_definition(
    analyzer: object, function_va: int, register: str, use_va: int,
    expected_va: int, label: str,
) -> None:
    actual = analyzer._reaching_definitions(function_va, register).get(use_va, frozenset())
    if actual != frozenset((expected_va,)):
        raise BuildError(f"{label} reaching definition drift at 0x{use_va:08X}: {actual}")


def require_entry_stack_formal(
    analyzer: object, decoded: object, function_va: int, site: int,
    register: str, expected_relative: int, label: str,
) -> None:
    ins = decoded.instructions.get(site)
    if not (
        ins is not None and ins.kind == "mov" and ins.dst is not None
        and ins.dst.kind == "reg" and ins.dst.reg == register
        and ins.src is not None and ins.src.kind == "mem" and ins.src.base == "esp"
        and ins.src.index is None and ins.src.absolute is None
    ):
        raise BuildError(f"{label} instruction drift at 0x{site:08X}")
    depths = analyzer._stack_depths(function_va).get(site, frozenset())
    if len(depths) != 1 or None in depths:
        raise BuildError(f"{label} stack-depth ambiguity at 0x{site:08X}: {depths}")
    depth = next(iter(depths))
    if ins.src.disp - depth != expected_relative:
        raise BuildError(f"{label} is not entry+0x{expected_relative:X}")


def verify_helper_graph(image: bytes, decoder: types.ModuleType, decoded_image: object) -> dict[str, int]:
    for role, start, end, off, expected_hash in HELPER_SPANS:
        if start - VA_TO_FILE_DELTA != off:
            raise BuildError(f"helper file mapping drift: {role}")
        raw = raw_at(image, start, end - start)
        if sha256_bytes(raw) != expected_hash:
            raise BuildError(f"helper span hash drift: {role}")
    b0 = decoder.FunctionSpan(0x00B0BF70, 0x00B0BFDC, 0x0070B370, 0x0070B3DC, HELPER_SPANS[0][4])
    b0_decoded = decoder.decode_function(decoded_image, b0)
    b0_calls = [ins for ins in b0_decoded.instructions.values() if ins.kind in ("call", "call_indirect")]
    b0_returns = [ins for ins in b0_decoded.instructions.values() if ins.kind == "ret"]
    if (
        len(b0_decoded.instructions) != 44 or b0_decoded.errors
        or sum(ins.size for ins in b0_decoded.instructions.values()) != 108
        or len(b0_calls) != 2 or any(ins.kind != "call_indirect" for ins in b0_calls)
        or len(b0_returns) != 3
    ):
        raise BuildError("0x00B0BF70 executed helper CFG drift")
    tree_raw = raw_at(image, 0x00652A30, 0xEF)
    direct: dict[int, int] = {}
    for index in range(len(tree_raw) - 4):
        if tree_raw[index] != 0xE8:
            continue
        site = 0x00652A30 + index
        displacement = int.from_bytes(tree_raw[index + 1:index + 5], "little", signed=True)
        direct[site] = site + 5 + displacement
    expected_direct = {
        0x00652AA0: 0x00652550,
        0x00652AC3: 0x00767170,
        0x00652AE5: 0x00652550,
    }
    if direct != expected_direct:
        raise BuildError(f"0x00652A30 child-call set drift: {direct}")
    require_bytes(image, 0x00652A8B, INVALID_CALL_BYTES.hex(), "tree helper guard")
    return {"helper_spans": len(HELPER_SPANS), "b0_nodes": 44, "tree_child_calls": len(direct)}


def verify_serializer_proof() -> tuple[dict[str, dict[str, int]], dict[int, FunctionPin]]:
    image = IMAGE.read_bytes()
    if len(image) != IMAGE_SIZE or sha256_bytes(image) != IMAGE_SHA256:
        raise BuildError("IMAGE changed before proof")
    decoder = load_decoder()
    decoded_image = decoder.Image(IMAGE)
    if decoded_image.data != image or decoded_image.sha256 != IMAGE_SHA256:
        raise BuildError("guarded decoder IMAGE identity drift")
    symbol = decoded_image.imports_by_iat.get(INVALID_IAT)
    expected_symbol = (
        "MSVCR90.dll", "_invalid_parameter_noinfo", 0x008398C0,
        0x00C112DC, 0x00C118B4, 0x00C1647C, 0x00C15C62,
    )
    actual_symbol = None if symbol is None else (
        symbol.dll, symbol.name, symbol.iat_off, symbol.descriptor_off,
        symbol.lookup_off, symbol.dll_name_off, symbol.symbol_name_off,
    )
    if actual_symbol != expected_symbol:
        raise BuildError(f"exact invalid-parameter import identity drift: {actual_symbol}")
    if sha256_bytes(INVALID_CALL_BYTES) != INVALID_CALL_SHA256:
        raise BuildError("invalid-call opcode hash constant drift")

    analyzer = decoder.SerializerAnalyzer(decoded_image, [])
    metrics: dict[str, dict[str, int]] = {}
    owners: dict[int, FunctionPin] = {}
    all_sites: set[int] = set()
    for pin in FUNCTIONS:
        if pin.start_va - VA_TO_FILE_DELTA != pin.file_off:
            raise BuildError(f"serializer file mapping drift: {pin.message}")
        raw = raw_at(image, pin.start_va, pin.end_va - pin.start_va)
        if sha256_bytes(raw) != pin.sha256:
            raise BuildError(f"serializer span hash drift: {pin.message}")
        span = decoder.FunctionSpan(
            pin.start_va, pin.end_va, pin.file_off,
            pin.file_off + pin.end_va - pin.start_va, pin.sha256,
        )
        decoded = decoder.decode_function(decoded_image, span)
        analyzer.span_cache[pin.start_va] = span
        analyzer.decode_cache[pin.start_va] = decoded
        nodes = len(decoded.instructions)
        edges = sum(len(group) for group in decoded.successors.values())
        covered = sum(ins.size for ins in decoded.instructions.values())
        direct_calls = sum(ins.kind == "call" for ins in decoded.instructions.values())
        indirect_calls = sum(ins.kind == "call_indirect" for ins in decoded.instructions.values())
        returns = [ins for ins in decoded.instructions.values() if ins.kind == "ret"]
        if (
            decoded.errors or nodes != pin.cfg_nodes or edges != pin.cfg_edges
            or covered != pin.covered_bytes or direct_calls != pin.direct_calls
            or indirect_calls != pin.indirect_calls or len(returns) != 1
            or returns[0].raw != bytes.fromhex("c20800")
        ):
            raise BuildError(
                f"executed serializer CFG drift: {pin.message}: "
                f"nodes={nodes} edges={edges} covered={covered} direct={direct_calls} "
                f"indirect={indirect_calls} errors={decoded.errors} returns={len(returns)}"
            )
        mode = decoded.instructions.get(pin.mode_branch)
        if not (
            mode is not None and mode.kind == "jcc" and mode.target == pin.r_entry
            and mode.next_va == pin.w_entry
        ):
            raise BuildError(f"mode split CFG drift: {pin.message}")
        w_nodes = reachable(decoded, pin.w_entry)
        r_nodes = reachable(decoded, pin.r_entry)
        dom = dominators(decoded)
        exact_sites = {
            ins.va for ins in decoded.instructions.values()
            if ins.kind == "call_indirect" and ins.src is not None
            and ins.src.kind == "mem" and ins.src.base is None
            and ins.src.index is None and ins.src.absolute == INVALID_IAT
            and ins.raw == INVALID_CALL_BYTES
        }
        if exact_sites != set(pin.invalid_sites) or len(exact_sites) != 5:
            raise BuildError(f"exact invalid callsite census drift: {pin.message}: {exact_sites}")
        require_entry_stack_formal(
            analyzer, decoded, pin.start_va, pin.writer_stream_definition,
            pin.writer_stream_reg, 4, f"{pin.message} writer stream",
        )
        require_entry_stack_formal(
            analyzer, decoded, pin.start_va, pin.reader_stream_definition,
            pin.reader_stream_reg, 4, f"{pin.message} reader stream",
        )
        this_def = decoded.instructions.get(pin.this_definition)
        if not (
            this_def is not None and this_def.kind == "mov"
            and this_def.dst is not None and this_def.dst.kind == "reg"
            and this_def.dst.reg == pin.this_reg
            and this_def.src is not None and this_def.src.kind == "reg"
            and this_def.src.reg == "ecx"
        ):
            raise BuildError(f"this-root definition drift: {pin.message}")
        for site in pin.invalid_sites:
            owners[site] = pin
            all_sites.add(site)
            guard = GUARD_BY_SITE.get(site)
            if guard is None:
                raise BuildError(f"missing guard pin at 0x{site:08X}")
            window = bytes.fromhex(guard.window_hex)
            if raw_at(image, guard.window_va, len(window)) != window:
                raise BuildError(f"guard window drift at 0x{site:08X}")
            if sha256_bytes(window) != guard.window_sha256:
                raise BuildError(f"guard window hash drift at 0x{site:08X}")
            if site not in w_nodes or site in r_nodes or pin.w_entry not in dom.get(site, ()):
                raise BuildError(f"W-only dominated path proof failed at 0x{site:08X}")
            require_single_definition(
                analyzer, pin.start_va, pin.this_reg, site,
                pin.this_definition, f"{pin.message} this-root",
            )
            if pin.message == "ItemMallUpdatePersonalDataVital":
                require_single_definition(
                    analyzer, pin.start_va, pin.writer_stream_reg, site,
                    pin.writer_stream_definition, f"{pin.message} writer stream",
                )
            depths = analyzer._stack_depths(pin.start_va)
            if depths.get(site, frozenset()) != frozenset((44,)):
                raise BuildError(f"guard call stack depth drift at 0x{site:08X}: {depths.get(site)}")
            ins = decoded.instructions[site]
            if depths.get(ins.next_va, frozenset()) != frozenset((44,)):
                raise BuildError(f"guard call is not stack-neutral at 0x{site:08X}")
            if ins.src.base is not None or ins.src.index is not None:
                raise BuildError(f"guard call unexpectedly receives a register operand at 0x{site:08X}")

        # Pin the already-accepted non-wire helper boundaries that leave these
        # ten exact guard rows as the only effective blockers for both messages.
        b0_call = decoded.instructions.get(pin.b0_call)
        b0_receiver = decoded.instructions.get(pin.b0_receiver)
        if not (
            b0_call is not None and b0_call.kind == "call" and b0_call.target == 0x00B0BF70
            and b0_receiver is not None and b0_receiver.kind == "lea"
            and b0_receiver.dst is not None and b0_receiver.dst.kind == "reg"
            and b0_receiver.dst.reg == "ecx" and b0_receiver.next_va == pin.b0_call
            and b0_receiver.src is not None and b0_receiver.src.kind == "mem"
            and b0_receiver.src.base == "esp" and b0_receiver.src.disp == 0x10
        ):
            raise BuildError(f"stack-local helper receiver drift: {pin.message}")
        tree_call = decoded.instructions.get(pin.tree_call)
        tree_receiver = decoded.instructions.get(pin.tree_receiver)
        if not (
            tree_call is not None and tree_call.kind == "call" and tree_call.target == 0x00652A30
            and tree_receiver is not None and tree_receiver.kind == "mov"
            and tree_receiver.dst is not None and tree_receiver.dst.kind == "reg"
            and tree_receiver.dst.reg == "ecx" and tree_receiver.next_va < pin.tree_call
        ):
            raise BuildError(f"ordered-tree helper call/receiver drift: {pin.message}")
        expected_member = 0x14 if pin.message == "ServerAddedInfoVital" else 0x1C
        member_update = 0x005EBDD7 if pin.message == "ServerAddedInfoVital" else 0x006B0EDE
        member_final = 0x005EBDDA if pin.message == "ServerAddedInfoVital" else member_update
        update = decoded.instructions.get(member_update)
        if not (
            update is not None and update.kind == "add" and update.dst is not None
            and update.dst.kind == "reg" and update.dst.reg == pin.this_reg
            and update.src is not None and update.src.kind == "imm"
            and update.src.imm == expected_member
        ):
            raise BuildError(f"this-derived tree member drift: {pin.message}")
        if member_final != member_update:
            bridge = decoded.instructions.get(member_final)
            if not (
                bridge is not None and bridge.kind == "lea"
                and bridge.dst is not None and bridge.dst.kind == "reg"
                and bridge.dst.reg == pin.this_reg
                and bridge.src is not None and bridge.src.kind == "mem"
                and bridge.src.base == pin.this_reg and bridge.src.index is None
                and bridge.src.absolute is None and bridge.src.disp == 0
            ):
                raise BuildError(f"tree-member identity LEA drift: {pin.message}")
            require_single_definition(
                analyzer, pin.start_va, pin.this_reg, member_final,
                member_update, f"{pin.message} tree member bridge",
            )
        require_single_definition(
            analyzer, pin.start_va, pin.this_reg, pin.tree_receiver,
            member_final, f"{pin.message} tree member",
        )
        if not (
            tree_receiver.src is not None and tree_receiver.src.kind == "reg"
            and tree_receiver.src.reg == pin.this_reg
        ):
            raise BuildError(f"tree receiver source drift: {pin.message}")
        require_single_definition(
            analyzer, pin.start_va, "ecx", pin.tree_call,
            pin.tree_receiver, f"{pin.message} tree receiver at call",
        )
        if pin.message == "ItemMallUpdatePersonalDataVital":
            # The conservative V1 span contains one internal alignment gap and
            # a later next-function tail.  Neither is silently counted as part
            # of the executed serializer CFG.
            require_bytes(image, 0x006B0DCA, "8d9b00000000", "ItemMall alignment NOP gap")
            if any(0x006B0DCA <= site < 0x006B0DD0 for site in decoded.instructions):
                raise BuildError("ItemMall decoder entered the alignment NOP gap")
            if any(
                0x006B0DCA <= target < 0x006B0DD0
                for targets in decoded.successors.values() for target in targets
            ):
                raise BuildError("ItemMall CFG has an edge into the alignment NOP gap")
            for gap_va in range(0x006B0DCA, 0x006B0DD0):
                if image.find(gap_va.to_bytes(4, "little")) >= 0:
                    raise BuildError(f"ItemMall alignment gap dword xref at 0x{gap_va:08X}")
            ret = returns[0]
            if ret.va != 0x006B0F3B or decoded.successors.get(ret.va) != ():
                raise BuildError("ItemMall reachable return boundary drift")
            if any(site >= 0x006B0F3E for site in decoded.instructions):
                raise BuildError("ItemMall decoder crossed the ret boundary")
            require_bytes(image, 0x006B0F3E, "cccc", "ItemMall unreachable tail separator")
        metrics[pin.message] = {
            "nodes": nodes, "edges": edges, "covered": covered,
            "direct_calls": direct_calls, "indirect_calls": indirect_calls,
            "invalid_sites": len(exact_sites), "stack_depth": 44,
        }
    if all_sites != set(GUARD_BY_SITE) or len(all_sites) != 10:
        raise BuildError("global exact callsite/guard census drift")
    helper_metrics = verify_helper_graph(image, decoder, decoded_image)
    metrics["helpers"] = helper_metrics
    return metrics, owners


def scan_prior_a2_targets(
    entries: Mapping[str, tuple[int, str]], candidate_sites: set[int],
) -> tuple[set[tuple[str, str, str]], dict[str, int]]:
    """Read every V4-manifest A2 removal/change overlay and reject overlap."""
    targets: set[tuple[str, str, str]] = set()
    owners: dict[tuple[str, str, str], str] = {}
    directive_rows = 0
    base_target_rows = 0
    legacy_string_targets = 0
    add_semantic_targets: set[tuple[str, ...]] = set()
    named_a2_deltas = {
        name for name in entries
        if (
            (name.startswith("PF_A2_") and name.endswith("_DELTA.tsv"))
            or re.fullmatch(r"PF_TARGETS?_.+_A2_DELTA\.tsv", name) is not None
        )
    }
    candidate_offsets = {f"0x{site - VA_TO_FILE_DELTA:08X}" for site in candidate_sites}
    candidate_lines = {str(line) for line in ROW_PINS}
    candidate_messages = {pin.message for pin in FUNCTIONS}
    for name in sorted(named_a2_deltas, key=str.casefold):
        fields, rows = read_tsv(OUT / name)
        directive_rows += len(rows)
        required = {
            "base_file", "base_line", "base_row_key", "old_tag", "direction(W/R)"
        }
        if not required.issubset(fields):
            legacy_required = {
                "dedup_key", "base_row_number", "message", "direction(W/R)",
                "original_call_file_off", "source",
            }
            if name != "PF_A2_STRING_WIRE_TAG_DELTA.tsv" or not legacy_required.issubset(fields):
                raise BuildError(f"unrecognized prior A2 delta schema: {name}")
            for line, row in rows:
                legacy_string_targets += 1
                if row["source"] != "IMAGE" or not row["dedup_key"]:
                    raise BuildError(f"legacy A2 target provenance drift: {name}:{line}")
                if (
                    row["base_row_number"] in candidate_lines
                    or (
                        row["message"] in candidate_messages
                        and row["original_call_file_off"] in candidate_offsets
                    )
                ):
                    raise BuildError(f"candidate overlaps legacy A2 target: {name}:{line}")
            continue
        for line, row in rows:
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            evidence_off = row.get("evidence_file_off", row.get("new_file_off_claim", ""))
            if (
                evidence_off in candidate_offsets
                and row.get("message") in candidate_messages
            ):
                raise BuildError(
                    f"candidate callsite already appears in prior A2 delta: {name}:{line}"
                )
            if target == ("N/A", "N/A", "N/A"):
                semantic_fields = (
                    "message", "schema_variant", "direction(W/R)", "new_order",
                    "new_tag", "new_field_offset", "new_len", "new_gate_condition",
                )
                if not set(semantic_fields).issubset(fields):
                    raise BuildError(f"A2 N/A target lacks semantic identity: {name}:{line}")
                semantic = tuple(row[field] for field in semantic_fields)
                if semantic in add_semantic_targets:
                    raise BuildError(f"duplicate A2 ADD semantic target: {name}:{line}")
                add_semantic_targets.add(semantic)
                continue
            if not all(target) or "N/A" in target:
                raise BuildError(f"malformed prior A2 target: {name}:{line}")
            if target in targets:
                raise BuildError(
                    f"pre-existing duplicate A2 target: {target}: "
                    f"{owners[target]} and {name}:{line}"
                )
            targets.add(target)
            owners[target] = f"{name}:{line}"
            base_target_rows += 1
    if (
        not named_a2_deltas or directive_rows == 0 or base_target_rows == 0
        or legacy_string_targets == 0 or not add_semantic_targets
        or directive_rows
        != base_target_rows + legacy_string_targets + len(add_semantic_targets)
    ):
        raise BuildError("no prior A2 overlay census was discovered")
    return targets, {
        "files": len(named_a2_deltas),
        "directives": directive_rows,
        "base_targets": base_target_rows,
        "add_semantic_targets": len(add_semantic_targets),
        "legacy_string_targets": legacy_string_targets,
    }


def scan_global_provenance(
    entries: Mapping[str, tuple[int, str]],
) -> tuple[set[str], set[tuple[str, str, str]]]:
    keys: set[str] = set()
    targets: set[tuple[str, str, str]] = set()
    key_owner: dict[str, str] = {}
    target_owner: dict[tuple[str, str, str], str] = {}
    for name in sorted(entries, key=str.casefold):
        if not name.lower().endswith(".tsv"):
            continue
        fields, rows = read_tsv(OUT / name)
        for line, row in rows:
            for column in ("delta_key", "dedup_key"):
                if column not in fields:
                    continue
                key = row[column]
                if not key or key == "N/A":
                    continue
                if key in keys:
                    raise BuildError(
                        f"pre-existing duplicate provenance key {key}: "
                        f"{key_owner[key]} and {name}:{line}"
                    )
                keys.add(key)
                key_owner[key] = f"{name}:{line}"
            required = {"base_file", "base_line", "base_row_key"}
            if not required.issubset(fields):
                continue
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            if not all(target) or "N/A" in target:
                continue
            if target in targets:
                raise BuildError(
                    f"pre-existing duplicate base target {target}: "
                    f"{target_owner[target]} and {name}:{line}"
                )
            targets.add(target)
            target_owner[target] = f"{name}:{line}"
    return keys, targets


def build_a2_delta(
    owners: Mapping[int, FunctionPin], prior_targets: set[tuple[str, str, str]],
) -> list[dict[str, str]]:
    fields, rows = read_tsv(OUT / "PF_SERIALIZER_FIELDS.tsv")
    expected_fields = [
        "message", "direction(W/R)", "order", "tag", "field_offset", "len",
        "gate_condition", "span_start", "span_end", "span_sha256",
        "file_off_claim", "source",
    ]
    if fields != expected_fields:
        raise BuildError("PF_SERIALIZER_FIELDS.tsv schema drift")
    by_line = {line: row for line, row in rows}
    output: list[dict[str, str]] = []
    for line in sorted(ROW_PINS):
        expected_key, message, direction, site = ROW_PINS[line]
        row = by_line.get(line)
        if row is None:
            raise BuildError(f"missing V1 A2 row at line {line}")
        row_key = canonical_row_key(fields, row)
        owner = owners.get(site)
        if owner is None or owner.message != message:
            raise BuildError(f"callsite owner drift for V1 line {line}")
        expected = (
            row_key, row["message"], row["direction(W/R)"], row["tag"],
            row["field_offset"], row["len"], row["file_off_claim"], row["source"],
        )
        wanted = (
            expected_key, message, direction, INVALID_TAG, INVALID_UNKNOWN, "N/A",
            f"0x{site - VA_TO_FILE_DELTA:08X}", "IMAGE",
        )
        if expected != wanted:
            raise BuildError(f"exact V1 row identity/content drift at line {line}: {expected}")
        if (
            row["span_start"] != f"0x{owner.start_va:08X}"
            or row["span_end"] != f"0x{owner.end_va:08X}"
            or row["span_sha256"] != owner.sha256
        ):
            raise BuildError(f"V1 evidence span drift at line {line}")
        gate_fragment = (
            f"exact_direct_iat_call@0x{site:08X} "
            f"file_off=0x{site - VA_TO_FILE_DELTA:08X} "
            f"function=0x{owner.start_va:08X} iat=0x00C3B4C0 bytes=FF15C0B4C300"
        )
        import_fragment = (
            "exact_direct_iat_import iat=0x00C3B4C0 iat_file_off=0x008398C0 "
            "descriptor_file_off=0x00C112DC lookup_file_off=0x00C118B4 "
            "dll_name_file_off=0x00C1647C symbol_name_file_off=0x00C15C62 "
            "dll=MSVCR90.dll symbol=_invalid_parameter_noinfo"
        )
        if gate_fragment not in row["gate_condition"] or import_fragment not in row["gate_condition"]:
            raise BuildError(f"V1 exact gate provenance drift at line {line}")
        target = ("PF_SERIALIZER_FIELDS.tsv", str(line), row_key)
        if target in prior_targets:
            raise BuildError(f"V1 row is already handled by an older A2 delta: {target}")
        guard = GUARD_BY_SITE[site]
        values = {
            "action": "REMOVE_NONWIRE_ROW",
            "change_type": "V5_GUARDED_INVALID_PARAMETER_NONWIRE",
            "base_file": "PF_SERIALIZER_FIELDS.tsv",
            "base_line": str(line),
            "base_row_key": row_key,
            "base_delta_key": "N/A",
            "message": message,
            "direction(W/R)": direction,
            "old_order": row["order"],
            "old_tag": row["tag"],
            "old_field_offset": row["field_offset"],
            "old_len": row["len"],
            "new_wire_order": "N/A",
            "new_tag": "N/A",
            "new_field_offset": "N/A",
            "new_len": "N/A",
            "new_gate_condition": "N/A",
            "resolution": (
                "PROVEN_NONWIRE;" + guard.condition
                + ";EXACT_DIRECT_IAT_CALL;ZERO_ARGUMENT_STACK_NEUTRAL"
                + ";EXECUTED_W_ONLY_CFG;SINGLETON_THIS_AND_STREAM_DEFINITIONS"
                + ";NO_STREAM_ALIAS;PINNED_HELPER_BOUNDARIES"
            ),
            "evidence_ticket": EVIDENCE_TICKET,
            "evidence_span_start": f"0x{owner.start_va:08X}",
            "evidence_span_end": f"0x{owner.end_va:08X}",
            "evidence_span_sha256": owner.sha256,
            "evidence_file_off": f"0x{site - VA_TO_FILE_DELTA:08X}",
            "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(
            ("A2", values["action"], values["base_file"], values["base_line"], row_key)
        )
        output.append(values)
    if (
        len(output) != 20
        or len({row["delta_key"] for row in output}) != 20
        or len({(row["base_file"], row["base_line"], row["base_row_key"]) for row in output}) != 20
        or sum(row["direction(W/R)"] == "W" for row in output) != 10
        or sum(row["direction(W/R)"] == "R" for row in output) != 10
        or len({row["evidence_file_off"] for row in output}) != 10
        or any(row["source"] != "IMAGE" or row["action"] != "REMOVE_NONWIRE_ROW" for row in output)
    ):
        raise BuildError("V5 A2 output census/layer contract failed")
    return output


def build_priority_delta(
    closure: Mapping[str, Mapping[str, Mapping[str, int]]]
) -> list[dict[str, str]]:
    fields, rows = read_tsv(OUT / "PF_V4_P1_OPEN.tsv")
    by_line = {line: row for line, row in rows}
    output: list[dict[str, str]] = []
    for message in sorted(PRIORITY_PINS):
        proof = closure.get(message)
        if proof is None or set(proof) != {"W", "R"}:
            raise BuildError(f"missing replay closure proof: {message}")
        for direction in ("W", "R"):
            measured = proof[direction]
            if (
                measured.get("removed", 0) <= 0
                or measured.get("residual_blockers") != 0
                or measured.get("proven_wire_rows", 0) <= 0
            ):
                raise BuildError(
                    f"replay closure precondition failed: {message}/{direction}:{measured}"
                )
        line, expected_row_key, expected_status_key = PRIORITY_PINS[message]
        row = by_line.get(line)
        if row is None or row.get("message") != message:
            raise BuildError(f"missing V4 P1 predecessor: {message}")
        row_key = canonical_row_key(fields, row)
        if row_key != expected_row_key or row.get("status_key") != expected_status_key:
            raise BuildError(f"V4 P1 predecessor identity drift: {message}")
        if (
            row.get("priority") != "1" or row.get("source") != "IMAGE"
            or row.get("effective_registry_identity_status") != "KNOWN"
            or row.get("effective_registry_identity_missing") != "N/A"
            or row.get("effective_serializer_status") != "OPEN"
            or row.get("effective_structural_status") != "OPEN"
            or row.get("primary_blocker_group") != "CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED"
            or row.get("effective_blocker") != "invalid_parameter_import_call_wire_effect_unproved"
        ):
            raise BuildError(f"V4 P1 predecessor status drift: {message}")
        values = {
            "action": "CHANGED",
            "base_file": "PF_V4_P1_OPEN.tsv",
            "base_line": str(line),
            "base_row_key": row_key,
            "base_delta_key": expected_status_key,
            "message": message,
            "priority": "1",
            "old_registry_identity_status": row["effective_registry_identity_status"],
            "new_registry_identity_status": row["effective_registry_identity_status"],
            "old_registry_identity_missing": row["effective_registry_identity_missing"],
            "new_registry_identity_missing": row["effective_registry_identity_missing"],
            "old_serializer_status": row["effective_serializer_status"],
            "new_serializer_status": "CLOSED",
            "old_serializer_blockers": row["effective_blocker"],
            "new_serializer_blockers": "N/A",
            "old_structural_status": row["effective_structural_status"],
            "new_structural_status": "CLOSED",
            "old_blocker": row["effective_blocker"],
            "new_blocker": "N/A",
            "evidence_ticket": EVIDENCE_TICKET,
            "closure_scope": (
                "STATIC_WIRE_STRUCTURE_ONLY;EXACT_TEN_CALLSITES;"
                "PER_SITE_CFG_DATAFLOW;FULL_V4_A2_REPLAY;ZERO_RESIDUAL_BLOCKERS;"
                "NONEMPTY_WIRE_ROWS_REMAIN;NO_IMPORT_NAME_GENERALIZATION;V4_STATUS_CHAINED"
            ),
            "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(
            ("PRIORITY", values["action"], values["base_file"], values["base_line"], row_key)
        )
        output.append(values)
    if (
        len(output) != 2 or len({row["delta_key"] for row in output}) != 2
        or any(
            row["source"] != "IMAGE" or row["action"] != "CHANGED"
            or row["new_serializer_status"] != "CLOSED"
            or row["new_structural_status"] != "CLOSED"
            for row in output
        )
    ):
        raise BuildError("V5 Priority output census/layer contract failed")
    return output


def parse_v4_metrics() -> dict[str, int]:
    text = (OUT / "PF_V4_EFFECTIVE_STATUS.md").read_text(encoding="utf-8")
    patterns = {
        "p1_closed": r"Priority 1: \*\*(\d+)/\d+ CLOSED\*\*",
        "p1_total": r"Priority 1: \*\*\d+/(\d+) CLOSED\*\*",
        "p1_open": r"Priority 1: .*?OPEN (\d+)",
        "overall_closed": r"Overall: \*\*(\d+)/\d+ CLOSED\*\*",
        "overall_total": r"Overall: \*\*\d+/(\d+) CLOSED\*\*",
        "overall_open": r"Overall: .*?OPEN (\d+)",
        "a2_rows": r"Stored/reference A2 rows: \*\*(\d+)\*\*",
        "a2_unknown": r"Stored/reference A2 rows: .*?UNKNOWN (\d+)",
        "generic_unknown": r"generic CALL/JUMP UNKNOWN (\d+)",
        "direct_invalid": r"direct invalid-parameter UNKNOWN (\d+)",
        "a3": r"A3 numeric-tag frequency remains \*\*(\d+)\*\*",
    }
    result: dict[str, int] = {}
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if len(matches) != 1:
            raise BuildError(f"V4 metric parse drift: {name}: {matches}")
        result[name] = int(matches[0])
    if (
        result["p1_closed"] + result["p1_open"] != result["p1_total"]
        or result["overall_closed"] + result["overall_open"] != result["overall_total"]
    ):
        raise BuildError("V4 metric arithmetic is inconsistent")
    return result


def audit_outputs(
    a2_rows: Sequence[Mapping[str, str]],
    priority_rows: Sequence[Mapping[str, str]],
    entries: Mapping[str, tuple[int, str]],
    prior_a2_targets: set[tuple[str, str, str]],
    prior_a2_stats: Mapping[str, int],
) -> dict[str, int]:
    existing_keys, existing_targets = scan_global_provenance(entries)
    new_rows = [*a2_rows, *priority_rows]
    new_keys = [row["delta_key"] for row in new_rows]
    new_targets = [
        (row["base_file"], row["base_line"], row["base_row_key"])
        for row in new_rows
    ]
    if len(new_keys) != len(set(new_keys)) or existing_keys.intersection(new_keys):
        raise BuildError("new/global provenance-key overlap")
    if len(new_targets) != len(set(new_targets)) or existing_targets.intersection(new_targets):
        raise BuildError("new/global base-target overlap")
    a2_targets = {
        (row["base_file"], row["base_line"], row["base_row_key"])
        for row in a2_rows
    }
    if prior_a2_targets.intersection(a2_targets):
        raise BuildError("V5 A2 target overlaps a prior A2 delta")
    forbidden_actions = {"ADD", "COPY", "UNCHANGED"}
    if any(
        any(token in row.get("action", "") for token in forbidden_actions)
        for row in new_rows
    ):
        raise BuildError("V5 component contains an ADD/COPY/UNCHANGED action")
    if any("FIELD_VALIDATION.tsv" in name for name in OWNED_NAMES):
        raise BuildError("V5 component attempted to create an A5 TSV")
    protected_target_universe = (
        len(existing_targets) + prior_a2_stats["add_semantic_targets"]
    )
    return {
        "existing_keys": len(existing_keys),
        "existing_targets": len(existing_targets),
        "existing_add_semantic_targets": prior_a2_stats["add_semantic_targets"],
        "protected_target_universe": protected_target_universe,
        "new_keys": len(new_keys),
        "new_targets": len(new_targets),
    }


def derived_projection(
    v4: Mapping[str, int], final_a2: Mapping[str, int], closure_count: int
) -> dict[str, int]:
    """Combine replay-measured A2 with proposed status transitions."""
    projected = {
        "p1_closed": v4["p1_closed"] + closure_count,
        "p1_total": v4["p1_total"],
        "p1_open": v4["p1_open"] - closure_count,
        "overall_closed": v4["overall_closed"] + closure_count,
        "overall_total": v4["overall_total"],
        "overall_open": v4["overall_open"] - closure_count,
        "a2_rows": final_a2["a2_rows"],
        "a2_unknown": final_a2["a2_unknown"],
        "generic_unknown": final_a2["generic_unknown"],
        "direct_invalid": final_a2["direct_invalid"],
        "a3": final_a2["a3"],
    }
    if (
        projected["p1_closed"] + projected["p1_open"] != projected["p1_total"]
        or projected["overall_closed"] + projected["overall_open"] != projected["overall_total"]
        or min(projected.values()) < 0
    ):
        raise BuildError("replay-derived V5 projection failed")
    return projected


def build_report(
    metrics: Mapping[str, Mapping[str, int]],
    prior: Mapping[str, int],
    audit: Mapping[str, int],
    v4: Mapping[str, int],
    projected: Mapping[str, int],
    replay: Mapping[str, int],
    closure: Mapping[str, Mapping[str, Mapping[str, int]]],
) -> bytes:
    lines = [
        "# PF V5 invalid-parameter non-wire closure component",
        "",
        "[MEASURED][IMAGE] Ten physical guard callsites in two pinned serializers pass exact per-site IMAGE proof. The import name is not used as a global classification rule.",
        "",
        "[PROPOSED][LOCAL] This additive component removes exactly 20 still-effective V1 analysis rows and chains exactly two P1 closures from PF_V4_P1_OPEN.tsv. It does not replace the V4 checkpoint until a later integration layer applies it.",
        "",
        "## Exact IMAGE and import identity",
        "",
        f"- [MEASURED][IMAGE] GameClient.local.bin: {IMAGE_SIZE} bytes / SHA-256 `{IMAGE_SHA256}`.",
        "- [MEASURED][IMAGE] IAT `0x00C3B4C0` / file offset `0x008398C0` resolves from descriptor `0x00C112DC`, lookup `0x00C118B4`, DLL-name `0x00C1647C`, symbol-name `0x00C15C62` to `MSVCR90.dll!_invalid_parameter_noinfo`.",
        f"- [MEASURED][IMAGE] Every selected instruction is exact `FF 15 C0 B4 C3 00`; instruction SHA-256 `{INVALID_CALL_SHA256}`.",
        "",
        "## Executed CFG and non-alias proof",
        "",
        "| claim | message | span | nodes | edges | covered bytes | direct calls | indirect calls | selected guards | stack depth | source |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for pin in FUNCTIONS:
        value = metrics[pin.message]
        lines.append(
            f"| [MEASURED][IMAGE] | `{pin.message}` | `0x{pin.start_va:08X}-0x{pin.end_va:08X}` / `{pin.sha256}` | "
            f"{value['nodes']} | {value['edges']} | {value['covered']} | {value['direct_calls']} | "
            f"{value['indirect_calls']} | {value['invalid_sites']} | {value['stack_depth']} | IMAGE |"
        )
    lines.extend([
        "",
        "[MEASURED][IMAGE] Each selected guard is reachable only from the write-mode successor, is dominated by that successor, and is unreachable from the read-mode successor. Reaching-definition analysis pins the object root at every call. ItemMall also pins the live writer stream register to entry+4 at every call; Server passes entry+4 to its wire primitive before the guards, while each guard itself has only the absolute IAT operand. Every guard enters and exits at the stable local-frame depth 44, so no stream or stack argument is passed.",
        "",
        "[MEASURED][IMAGE] The ItemMall V1 span is intentionally conservative: executed coverage excludes the six-byte alignment NOP gap `0x006B0DCA-0x006B0DD0` (no CFG edge or dword xref enters it) and stops at `ret 8` at `0x006B0F3B`; the `0x006B0F3E+` bytes are a separated next-function tail. Those bytes are not claimed as executed serializer CFG.",
        "",
        "| claim | callsite | file offset | message | guard | window SHA-256 | result | source |",
        "|---|---:|---:|---|---|---|---|---|",
    ])
    for guard in GUARDS:
        owner = next(pin for pin in FUNCTIONS if guard.call_va in pin.invalid_sites)
        lines.append(
            f"| [MEASURED][IMAGE] | `0x{guard.call_va:08X}` | `0x{guard.call_va - VA_TO_FILE_DELTA:08X}` | "
            f"`{owner.message}` | `{guard.condition}` | `{guard.window_sha256}` | PROVEN_NONWIRE | IMAGE |"
        )
    lines.extend([
        "",
        "## Helper boundary pins",
        "",
        "[MEASURED][IMAGE] Both callers retain the earlier accepted stack-local `0x00B0BF70` helper and this-derived `0x00652A30` ordered-tree helper proofs. V5 re-hashes those bodies plus `0x00652550` and `0x00767170`, rechecks exact caller receiver origins, and re-derives the three fixed child calls. It does not copy or re-emit their already-closed rows.",
        "",
        "## Full effective-A2 replay gate",
        "",
        f"- [MEASURED][IMAGE] Reconstructed frozen V4 effective A2 from the base plus the ordered V2/V3 replay and both V4 overlays: V3 component files/directives {replay['v3_overlay_files']}/{replay['v3_overlay_directives']}; V4 component files/directives {replay['v4_overlay_files']}/{replay['v4_overlay_directives']}; V4 targets accounted {replay['v4_overlay_targets_accounted']}; effective rows {replay['a2_rows']}.",
        "- [MEASURED][IMAGE] The 20 V5 directives were then applied by exact still-effective evidence key. Every declared target was consumed exactly once; no cardinality subtraction was used to obtain the post-V5 A2 census.",
        "",
        "| claim | message | direction | removals applied | residual blocker rows | non-empty proven wire rows | effective rows after | source |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ])
    for message in sorted(closure):
        for direction in ("W", "R"):
            value = closure[message][direction]
            lines.append(
                f"| [MEASURED][IMAGE] | `{message}` | {direction} | {value['removed']} | "
                f"{value['residual_blockers']} | {value['proven_wire_rows']} | "
                f"{value['rows_after']} | IMAGE |"
            )
    lines.extend([
        "",
        "## Duplicate and layer audit",
        "",
        f"- [MEASURED][OUTPUT-AUDIT] Prior A2 overlays scanned from the exact V4 manifest: {prior['files']} files / {prior['directives']} directives = {prior['base_targets']} full base targets + {prior['add_semantic_targets']} ADD semantic targets + {prior['legacy_string_targets']} legacy string-correction targets; overlap with the 20 proposed targets and ten callsite semantics: 0.",
        f"- [MEASURED][OUTPUT-AUDIT] Existing provenance keys: {audit['existing_keys']}; existing full base targets: {audit['existing_targets']}; ADD semantic targets: {audit['existing_add_semantic_targets']}; protected full+ADD target universe: {audit['protected_target_universe']}; new keys/targets: {audit['new_keys']}/{audit['new_targets']}; overlap: 0.",
        "- [MEASURED][OUTPUT-AUDIT] A2 actions: REMOVE_NONWIRE_ROW=20; Priority actions: CHANGED=2; ADD/COPY/UNCHANGED/A1/A3/A5 rows=0. Every TSV row has source=IMAGE.",
        "",
        "## Effective projection if integrated after V4",
        "",
        "[PROPOSED][DERIVED] A2 values below come from the full in-memory replay after exact removals. Priority values apply the two replay-gated transitions to the frozen V4 status but remain proposed until an integration checkpoint publishes them.",
        "",
        "| claim | item | pinned V4 | projected after this component |",
        "|---|---|---:|---:|",
        f"| [PROPOSED][DERIVED] | P1 CLOSED / total | {v4['p1_closed']}/{v4['p1_total']} | {projected['p1_closed']}/{projected['p1_total']} |",
        f"| [PROPOSED][DERIVED] | P1 OPEN | {v4['p1_open']} | {projected['p1_open']} |",
        f"| [PROPOSED][DERIVED] | overall CLOSED / total | {v4['overall_closed']}/{v4['overall_total']} | {projected['overall_closed']}/{projected['overall_total']} |",
        f"| [PROPOSED][DERIVED] | overall OPEN | {v4['overall_open']} | {projected['overall_open']} |",
        f"| [PROPOSED][DERIVED] | stored/reference A2 | {v4['a2_rows']} | {projected['a2_rows']} |",
        f"| [PROPOSED][DERIVED] | A2 UNKNOWN | {v4['a2_unknown']} | {projected['a2_unknown']} |",
        f"| [PROPOSED][DERIVED] | direct invalid-parameter UNKNOWN | {v4['direct_invalid']} | {projected['direct_invalid']} |",
        f"| [PROPOSED][DERIVED] | generic CALL/JUMP UNKNOWN | {v4['generic_unknown']} | {projected['generic_unknown']} |",
        f"| [PROPOSED][DERIVED] | A3 numeric-tag frequency | {v4['a3']} | {projected['a3']} |",
        "",
        "## Nonclaims and stop rule",
        "",
        "- [NONCLAIM][LOCAL] No gameplay meaning, server behavior, capture agreement, dump identity, runtime observation, field value, or import-wide classification is claimed.",
        "- [NONCLAIM][LOCAL] No other `_invalid_parameter_noinfo` call is closed. A future site must repeat the same per-function CFG, reaching-definition, path, stack, and non-alias proof.",
        "- [NONCLAIM][LOCAL] No raw DUMP or CAPTURE byte is read or emitted. No A5 TSV is copied. V1 and V4 remain immutable.",
        "",
        "## Reproduction and scope",
        "",
        "[REPRODUCTION][LOCAL] Run `py -3 -B pf_build_v5_invalid_parameter_closure.py --self-test-publication`, then `--self-test-replay-mutation`, `--audit-only`, normal publication, and `--check`.",
        "",
        "[DECLARED-SCOPE] Local-only under pf_bridge/external. Read GameClient.local.bin and frozen external artifacts only. Do not run the client or server and do not write workflow, queue, lease, Git, V4, capture, dump, data, or GameClient files.",
        "",
    ])
    text = "\n".join(lines)
    try:
        return text.encode("ascii")
    except UnicodeEncodeError as exc:
        raise BuildError("report is not cp874-safe ASCII") from exc


def audit_report_labels(report: bytes) -> None:
    text = report.decode("ascii")
    lines = text.splitlines()
    section = ""
    section_labels = {
        "Exact IMAGE and import identity": "[MEASURED][IMAGE]",
        "Executed CFG and non-alias proof": "[MEASURED][IMAGE]",
        "Helper boundary pins": "[MEASURED][IMAGE]",
        "Full effective-A2 replay gate": "[MEASURED][IMAGE]",
        "Duplicate and layer audit": "[MEASURED][OUTPUT-AUDIT]",
        "Effective projection if integrated after V4": "[PROPOSED][DERIVED]",
        "Nonclaims and stop rule": "[NONCLAIM][LOCAL]",
    }
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            section = stripped[3:]
            if section not in {*section_labels, "Reproduction and scope"}:
                raise BuildError(f"unknown report claim section: {section}")
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("|") and (
            stripped.startswith("|---") or stripped.startswith("| claim |")
        ):
            continue
        if not section:
            if "Ten physical guard callsites" in line:
                expected = "[MEASURED][IMAGE]"
            elif "This additive component removes" in line:
                expected = "[PROPOSED][LOCAL]"
            else:
                raise BuildError(f"unknown report summary claim: {line[:160]}")
        elif section == "Reproduction and scope":
            if "Run `py -3 -B" in line:
                expected = "[REPRODUCTION][LOCAL]"
            elif "Local-only under pf_bridge/external" in line:
                expected = "[DECLARED-SCOPE]"
            else:
                raise BuildError(f"unknown reproduction/scope claim: {line[:160]}")
        else:
            expected = section_labels[section]
        actual = [label for label in REPORT_LABELS if label in line]
        if actual != [expected]:
            raise BuildError(
                f"report claim label mismatch: expected={expected} actual={actual}: "
                f"{line[:120]}"
            )

    required_classes = set(REPORT_LABELS)
    present_classes = {
        label for label in REPORT_LABELS if any(label in line for line in lines)
    }
    if present_classes != required_classes:
        raise BuildError(
            f"report label class census drift: {sorted(present_classes)} != "
            f"{sorted(required_classes)}"
        )


def report_label_guard_selftest(report: bytes) -> None:
    audit_report_labels(report)
    text = report.decode("ascii")
    source_lines = text.splitlines()
    labelled = [
        (index, line) for index, line in enumerate(source_lines)
        if not line.strip().startswith("#")
        and any(label in line for label in REPORT_LABELS)
    ]
    if not labelled:
        raise BuildError("report label self-test found no labelled claim lines")
    for index, original in labelled:
        lines = list(source_lines)
        mutated_line = original
        source_labels = [label for label in REPORT_LABELS if label in original]
        if len(source_labels) != 1:
            raise BuildError(f"report label self-test source class drift: {original[:120]}")
        source_label = source_labels[0]
        for label in REPORT_LABELS:
            mutated_line = mutated_line.replace(label, "")
        lines[index] = mutated_line
        mutated = ("\n".join(lines) + "\n").encode("ascii")
        try:
            audit_report_labels(mutated)
        except BuildError:
            pass
        else:
            raise BuildError(
                f"report label guard accepted unlabelled line mutation: {original[:120]}"
            )
        for wrong_label in REPORT_LABELS:
            if wrong_label == source_label:
                continue
            lines = list(source_lines)
            lines[index] = original.replace(source_label, wrong_label, 1)
            substituted = ("\n".join(lines) + "\n").encode("ascii")
            try:
                audit_report_labels(substituted)
            except BuildError:
                pass
            else:
                raise BuildError(
                    "report label guard accepted class-laundered line: "
                    f"{source_label}->{wrong_label}: {original[:100]}"
                )


def build() -> tuple[dict[Path, bytes], dict[str, int], dict[str, int]]:
    before = verify_inputs()
    entries = parse_v4_manifest()
    metrics, owners = verify_serializer_proof()
    candidate_sites = set(owners)
    prior_targets, prior_stats = scan_prior_a2_targets(entries, candidate_sites)
    a2_rows = build_a2_delta(owners, prior_targets)
    v4 = parse_v4_metrics()
    v2, v3 = load_v3_replay_modules()
    effective_v4, replay = replay_v4_effective_a2(v2, v3, v4)
    _effective_v5, closure, final_a2 = apply_v5_removals(v2, effective_v4, a2_rows)
    priority_rows = build_priority_delta(closure)
    audit = audit_outputs(
        a2_rows, priority_rows, entries, prior_targets, prior_stats
    )
    projected = derived_projection(v4, final_a2, len(priority_rows))
    report = build_report(
        metrics, prior_stats, audit, v4, projected, replay, closure
    )
    report_label_guard_selftest(report)
    outputs = {
        A2_OUT: format_tsv(A2_COLUMNS, a2_rows),
        PRIORITY_OUT: format_tsv(PRIORITY_COLUMNS, priority_rows),
        REPORT_OUT: report,
    }
    if set(outputs) != set(OWNED_OUTPUTS):
        raise BuildError("publication target boundary changed")
    after = verify_inputs()
    if before != after:
        raise BuildError("pinned inputs changed during V5 derivation")
    return outputs, projected, {
        "prior_a2_files": prior_stats["files"],
        "prior_a2_directives": prior_stats["directives"],
        "prior_a2_targets": prior_stats["base_targets"],
        "prior_a2_add_semantics": prior_stats["add_semantic_targets"],
        "v3_replay_directives": replay["v3_overlay_directives"],
        "v4_replay_directives": replay["v4_overlay_directives"],
        "v5_replay_applied": sum(
            value["removed"]
            for message in closure.values()
            for value in message.values()
        ),
        **audit,
    }


def lock_payload(token: str) -> bytes:
    return f"token={token}\npid={os.getpid()}\n".encode("ascii")


GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
DELETE_ACCESS = 0x00010000
FILE_SHARE_READ = 0x00000001
CREATE_NEW = 1
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_BEGIN = 0
FILE_DISPOSITION_INFO_CLASS = 4
ERROR_FILE_EXISTS = 80
ERROR_ALREADY_EXISTS = 183
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


class FileDispositionInfo(ctypes.Structure):
    _fields_ = [("DeleteFile", ctypes.c_ubyte)]


KERNEL32 = ctypes.WinDLL("kernel32", use_last_error=True)
KERNEL32.CreateFileW.argtypes = (
    wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
    wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
)
KERNEL32.CreateFileW.restype = wintypes.HANDLE
KERNEL32.WriteFile.argtypes = (
    wintypes.HANDLE, wintypes.LPCVOID, wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID,
)
KERNEL32.WriteFile.restype = wintypes.BOOL
KERNEL32.ReadFile.argtypes = (
    wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID,
)
KERNEL32.ReadFile.restype = wintypes.BOOL
KERNEL32.SetFilePointerEx.argtypes = (
    wintypes.HANDLE, ctypes.c_longlong, ctypes.POINTER(ctypes.c_longlong), wintypes.DWORD,
)
KERNEL32.SetFilePointerEx.restype = wintypes.BOOL
KERNEL32.FlushFileBuffers.argtypes = (wintypes.HANDLE,)
KERNEL32.FlushFileBuffers.restype = wintypes.BOOL
KERNEL32.SetFileInformationByHandle.argtypes = (
    wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
)
KERNEL32.SetFileInformationByHandle.restype = wintypes.BOOL
KERNEL32.CloseHandle.argtypes = (wintypes.HANDLE,)
KERNEL32.CloseHandle.restype = wintypes.BOOL


def win_failure(operation: str) -> BuildError:
    return BuildError(f"{operation} failed: winerror={ctypes.get_last_error()}")


def create_lock_handle(lock: Path, token: str):
    handle = KERNEL32.CreateFileW(
        str(lock), GENERIC_READ | GENERIC_WRITE | DELETE_ACCESS,
        FILE_SHARE_READ, None, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, None,
    )
    if handle == INVALID_HANDLE_VALUE:
        error = ctypes.get_last_error()
        if error in {ERROR_FILE_EXISTS, ERROR_ALREADY_EXISTS}:
            raise BuildError(f"publication lock exists: {lock.name}")
        raise win_failure("CreateFileW publication lock")
    data = lock_payload(token)
    buffer = ctypes.create_string_buffer(data)
    written = wintypes.DWORD()
    if not KERNEL32.WriteFile(handle, buffer, len(data), ctypes.byref(written), None):
        KERNEL32.CloseHandle(handle)
        raise win_failure("WriteFile publication lock")
    if written.value != len(data):
        KERNEL32.CloseHandle(handle)
        raise BuildError("short publication lock write")
    if not KERNEL32.FlushFileBuffers(handle):
        KERNEL32.CloseHandle(handle)
        raise win_failure("FlushFileBuffers publication lock")
    return handle


def read_lock_handle(handle, expected_size: int) -> bytes:
    if not KERNEL32.SetFilePointerEx(handle, 0, None, FILE_BEGIN):
        raise win_failure("SetFilePointerEx publication lock")
    buffer = ctypes.create_string_buffer(expected_size + 1)
    read = wintypes.DWORD()
    if not KERNEL32.ReadFile(handle, buffer, expected_size + 1, ctypes.byref(read), None):
        raise win_failure("ReadFile publication lock")
    return bytes(buffer.raw[:read.value])


def assert_lock_owner(handle, token: str) -> None:
    expected = lock_payload(token)
    if read_lock_handle(handle, len(expected)) != expected:
        raise BuildError("publication lock ownership token changed")


def mark_lock_delete_on_close(handle) -> None:
    disposition = FileDispositionInfo(ctypes.c_ubyte(1))
    if not KERNEL32.SetFileInformationByHandle(
        handle, FILE_DISPOSITION_INFO_CLASS, ctypes.byref(disposition),
        ctypes.sizeof(disposition),
    ):
        raise win_failure("SetFileInformationByHandle(FileDispositionInfo)")


def close_lock_handle(handle) -> None:
    if not KERNEL32.CloseHandle(handle):
        raise win_failure("CloseHandle publication lock")


def write_journal(path: Path, payload: Mapping[str, object]) -> None:
    data = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    temporary = path.with_name(path.name + ".next")
    if temporary.exists():
        raise BuildError(f"stale journal stage exists: {temporary.name}")
    with temporary.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    if path.read_bytes() != data:
        raise BuildError("journal readback mismatch")


def publication_residue(root: Path) -> list[str]:
    names = [path.name for path in root.glob(TX_PREFIX + "*")]
    lock = root / LOCK_NAME
    if lock.exists():
        names.append(lock.name)
    return sorted(names)


def publish_transaction(
    root: Path,
    outputs: Mapping[Path, bytes],
    verify_callback,
    hook=None,
) -> None:
    lock = root / LOCK_NAME
    token = secrets.token_hex(24)
    handle = create_lock_handle(lock, token)
    tx: Path | None = None
    committed = False
    handle_open = True
    try:
        assert_lock_owner(handle, token)
        if hook is not None:
            hook("after_lock", None, lock, token)
        tx = Path(tempfile.mkdtemp(prefix=TX_PREFIX, dir=root))
        staged: dict[Path, Path] = {}
        backups: dict[Path, Path] = {}
        originals: dict[Path, bytes | None] = {}
        for target, data in outputs.items():
            if target.parent.resolve() != root.resolve() or target.name not in OWNED_NAMES:
                raise BuildError(f"publication target outside owned boundary: {target}")
            stage = tx / (target.name + ".stage")
            with stage.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            if stage.read_bytes() != data:
                raise BuildError(f"staged readback mismatch: {target.name}")
            staged[target] = stage
            if target.exists():
                originals[target] = target.read_bytes()
                backup = tx / (target.name + ".backup")
                shutil.copyfile(target, backup)
                with backup.open("r+b") as stream:
                    stream.flush()
                    os.fsync(stream.fileno())
                if backup.read_bytes() != originals[target]:
                    raise BuildError(f"backup readback mismatch: {target.name}")
                backups[target] = backup
            else:
                originals[target] = None
        verify_callback()
        assert_lock_owner(handle, token)
        journal = tx / "journal.json"
        state: dict[str, object] = {
            "token": token,
            "status": "STAGED",
            "targets": [path.name for path in outputs],
            "attempted": [],
            "replaced": [],
            "original_sha256": {
                path.name: (sha256_bytes(data) if data is not None else "ABSENT")
                for path, data in originals.items()
            },
        }
        write_journal(journal, state)
        attempted: list[Path] = []
        try:
            for target in outputs:
                # Pre-journal the attempted target.  A BaseException after
                # os.replace must still make this exact target recoverable.
                attempted.append(target)
                state["status"] = "REPLACING"
                state["attempted"] = [path.name for path in attempted]
                write_journal(journal, state)
                assert_lock_owner(handle, token)
                os.replace(staged[target], target)
                if hook is not None:
                    hook("after_replace", target, lock, token)
                state["replaced"] = [*state["replaced"], target.name]  # type: ignore[misc]
                write_journal(journal, state)
            for target, data in outputs.items():
                if target.read_bytes() != data:
                    raise BuildError(f"post-publish readback mismatch: {target.name}")
            verify_callback()
            assert_lock_owner(handle, token)
            state["status"] = "COMMITTED"
            write_journal(journal, state)
            committed = True
        except BaseException as failure:
            errors: list[str] = []
            for target in reversed(attempted):
                try:
                    original = originals[target]
                    if original is None:
                        target.unlink(missing_ok=True)
                    else:
                        backup = backups.get(target)
                        if backup is None or not backup.is_file():
                            raise BuildError(f"rollback backup missing: {target.name}")
                        # Copy instead of consuming the backup so uncertain
                        # recovery retains the exact original and journal.
                        shutil.copyfile(backup, target)
                        with target.open("r+b") as stream:
                            stream.flush()
                            os.fsync(stream.fileno())
                    if original is None:
                        if target.exists():
                            raise BuildError(f"rollback failed to remove: {target.name}")
                    elif not target.is_file() or target.read_bytes() != original:
                        raise BuildError(f"rollback readback mismatch: {target.name}")
                except BaseException as exc:
                    errors.append(f"{target.name}:{type(exc).__name__}")
            try:
                state["status"] = (
                    "ROLLBACK_INCOMPLETE" if errors else "ROLLED_BACK_AFTER_FAILURE"
                )
                state["rollback_errors"] = errors
                write_journal(journal, state)
            except BaseException as exc:
                errors.append(f"journal:{type(exc).__name__}")
            if errors:
                raise BuildError(
                    "rollback incomplete; lock/transaction retained: " + ",".join(errors)
                ) from failure
            raise
        if hook is not None:
            hook("after_commit", None, lock, token)
    finally:
        try:
            if committed:
                assert_lock_owner(handle, token)
                if tx is None or not tx.is_dir():
                    raise BuildError("committed transaction directory disappeared")
                shutil.rmtree(tx)
                tx = None
                assert_lock_owner(handle, token)
                # Delete this exact held inode on close.  Never unlink a lock
                # pathname after a separate ownership check (TOCTOU).
                mark_lock_delete_on_close(handle)
                close_lock_handle(handle)
                handle_open = False
                if lock.exists():
                    raise BuildError("publication lock release failed")
        finally:
            if handle_open:
                close_lock_handle(handle)


def publish(outputs: Mapping[Path, bytes]) -> None:
    publish_transaction(OUT, outputs, verify_inputs)


class InjectedPublicationAbort(BaseException):
    pass


def publication_self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="pf_v5_invalid_publication_selftest_") as temporary:
        test_root = Path(temporary)

        interrupt_root = test_root / "interrupt"
        interrupt_root.mkdir()
        first = interrupt_root / "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv"
        second = interrupt_root / "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv"
        first.write_bytes(b"old-first")

        def interrupt_hook(event, target, _lock, _token) -> None:
            if event == "after_replace" and target == first:
                raise InjectedPublicationAbort("after replace")

        try:
            publish_transaction(
                interrupt_root, {first: b"new-first", second: b"new-second"},
                lambda: None, interrupt_hook,
            )
        except InjectedPublicationAbort:
            pass
        else:
            raise BuildError("interrupt-after-replace injection did not fire")
        transactions = list(interrupt_root.glob(TX_PREFIX + "*"))
        if (
            first.read_bytes() != b"old-first" or second.exists()
            or not (interrupt_root / LOCK_NAME).is_file() or len(transactions) != 1
        ):
            raise BuildError("interrupt rollback/recovery-state contract failed")
        journal = json.loads((transactions[0] / "journal.json").read_text(encoding="ascii"))
        if journal.get("status") != "ROLLED_BACK_AFTER_FAILURE" or journal.get("attempted") != [first.name]:
            raise BuildError("interrupt recovery journal contract failed")

        held_root = test_root / "held"
        held_root.mkdir()
        held_target = held_root / "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv"
        replacement = held_root / "replacement.lock"
        replacement.write_bytes(b"foreign replacement")
        blocked = {"unlink": False, "replace": False}

        def held_hook(event, _target, lock, _token) -> None:
            if event != "after_lock":
                return
            try:
                os.unlink(lock)
            except OSError:
                blocked["unlink"] = True
            else:
                raise BuildError("second actor unlinked held publication lock")
            try:
                os.replace(replacement, lock)
            except OSError:
                blocked["replace"] = True
            else:
                raise BuildError("second actor replaced held publication lock")

        publish_transaction(held_root, {held_target: b"new"}, lambda: None, held_hook)
        if (
            held_target.read_bytes() != b"new" or not all(blocked.values())
            or (held_root / LOCK_NAME).exists()
            or replacement.read_bytes() != b"foreign replacement"
            or publication_residue(held_root)
        ):
            raise BuildError("held-handle atomic-release contract failed")

        foreign_root = test_root / "foreign"
        foreign_root.mkdir()
        foreign_target = foreign_root / "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv"
        foreign_target.write_bytes(b"old")
        foreign_lock = foreign_root / LOCK_NAME
        foreign_bytes = b"token=PREEXISTING_FOREIGN\npid=0\n"
        foreign_lock.write_bytes(foreign_bytes)
        try:
            publish_transaction(foreign_root, {foreign_target: b"new"}, lambda: None)
        except BuildError as exc:
            if "publication lock exists" not in str(exc):
                raise
        else:
            raise BuildError("pre-existing foreign lock was not rejected")
        if (
            foreign_target.read_bytes() != b"old"
            or foreign_lock.read_bytes() != foreign_bytes
            or list(foreign_root.glob(TX_PREFIX + "*"))
        ):
            raise BuildError("pre-existing foreign lock was modified")

        success_root = test_root / "success"
        success_root.mkdir()
        success_target = success_root / "PF_V5_INVALID_PARAMETER_CLOSURE.md"
        publish_transaction(success_root, {success_target: b"new"}, lambda: None)
        if success_target.read_bytes() != b"new" or publication_residue(success_root):
            raise BuildError("successful publication cleanup contract failed")


def replay_mutation_self_test() -> None:
    """Prove closure is rejected if status stays stale but A2 gains one blocker."""
    verify_inputs()
    entries = parse_v4_manifest()
    _metrics, owners = verify_serializer_proof()
    prior_targets, _prior_stats = scan_prior_a2_targets(entries, set(owners))
    a2_rows = build_a2_delta(owners, prior_targets)
    v4 = parse_v4_metrics()
    v2, v3 = load_v3_replay_modules()
    effective_v4, _replay = replay_v4_effective_a2(v2, v3, v4)

    _normal, normal_closure, _normal_metrics = apply_v5_removals(
        v2, effective_v4, a2_rows
    )
    if any(
        values[direction]["residual_blockers"] != 0
        for values in normal_closure.values()
        for direction in ("W", "R")
    ):
        raise BuildError("normal replay unexpectedly retained a blocker")

    mutated = clone_effective(effective_v4)
    semantic = ("ServerAddedInfoVital", "W")
    templates = [value for value in mutated[semantic] if value.tag == INVALID_TAG]
    if len(templates) != 5:
        raise BuildError(f"mutation template census drift: {len(templates)}")
    template = templates[0]
    synthetic_key = sha256_bytes(
        b"SELFTEST_SYNTHETIC_UNACCOUNTED_INVALID_PARAMETER_ROW"
    )
    if any(
        value.evidence_key == synthetic_key
        for rows in mutated.values()
        for value in rows
    ):
        raise BuildError("synthetic mutation evidence key unexpectedly exists")
    synthetic = dataclasses.replace(
        template,
        sequence=max(value.sequence for value in mutated[semantic]) + 1,
        field_identity=template.field_identity + ";SELFTEST_UNACCOUNTED",
        wire_order="SELFTEST_UNACCOUNTED",
        evidence_key=synthetic_key,
        provenance="SELFTEST_SYNTHETIC_MUTATION",
    )
    mutated[semantic].append(synthetic)
    try:
        apply_v5_removals(v2, mutated, a2_rows)
    except BuildError as exc:
        if "residual serializer/structural blockers" not in str(exc):
            raise BuildError(f"mutation failed for the wrong reason: {exc}") from exc
    else:
        raise BuildError(
            "full-replay closure accepted a synthetic unique invalid-parameter row"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--audit-only", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test-publication", action="store_true")
    mode.add_argument("--self-test-replay-mutation", action="store_true")
    args = parser.parse_args()
    if args.self_test_publication:
        publication_self_test()
        print("publication self-test PASS: interrupt rollback, held lock, foreign lock, success cleanup")
        return 0
    if args.self_test_replay_mutation:
        replay_mutation_self_test()
        print(
            "replay mutation self-test PASS: stale V4 status plus one unique "
            "invalid-parameter A2 row was rejected"
        )
        return 0
    residue_before = publication_residue(OUT)
    if residue_before:
        raise BuildError("stale V5 publication recovery state: " + ",".join(residue_before))
    outputs, projected, audit = build()
    if args.audit_only:
        for path, data in outputs.items():
            print(f"PREVIEW {path.name} {sha256_bytes(data)}")
    elif args.check:
        for path, data in outputs.items():
            if not path.is_file() or path.read_bytes() != data:
                raise BuildError(f"check mismatch: {path.name}")
    else:
        publish(outputs)
        residue_after = publication_residue(OUT)
        if residue_after:
            raise BuildError("publication residue remains: " + ",".join(residue_after))
        for path in outputs:
            print(f"{path.name} {sha256_path(path)}")
    print(
        "PASS V5 invalid-parameter component "
        f"A2={projected['a2_rows']} UNKNOWN={projected['a2_unknown']} "
        f"direct_invalid={projected['direct_invalid']} P1={projected['p1_closed']}/"
        f"{projected['p1_total']} OPEN={projected['p1_open']} "
        f"prior_A2_directives={audit['prior_a2_directives']} "
        f"prior_A2_targets={audit['prior_a2_targets']} overlap=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
