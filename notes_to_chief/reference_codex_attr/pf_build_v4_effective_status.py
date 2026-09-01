#!/usr/bin/env python3
"""Build the duplicate-safe V4 IMAGE-static effective status checkpoint."""

from __future__ import annotations

import argparse
import ctypes
import csv
import dataclasses
import hashlib
import io
import json
import os
import re
import secrets
import shutil
import tempfile
from collections import Counter
from ctypes import wintypes
from pathlib import Path
from typing import Mapping, Sequence

import pf_build_v3_effective_status as status_v3
import pf_validate_v3_effective_capture as field_v3


OUT = Path(__file__).resolve().parent
IMAGE = OUT.parents[1] / "GameClient" / "GameClient.local.bin"
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
LOCK_NAME = ".PF_V4_EFFECTIVE_STATUS_PUBLISH.lock"
TX_PREFIX = ".PF_V4_EFFECTIVE_STATUS_TXN."

A1_OUT = OUT / "PF_A1_STATIC_TYPE_INFO_DELTA.tsv"
PRIORITY_OUT = OUT / "PF_PRIORITY_STATIC_TYPE_INFO_DELTA.tsv"
OPEN_OUT = OUT / "PF_V4_P1_OPEN.tsv"
REPORT_OUT = OUT / "PF_V4_EFFECTIVE_STATUS.md"
OWNED = {path.name for path in (A1_OUT, PRIORITY_OUT, OPEN_OUT, REPORT_OUT)}

PINNED = {
    "PF_V3_MANIFEST.md": "dc87eedc65ed5e07ce4673742b6a0d20304140bb177e617c6af8b3846bd0b50e",
    "pf_build_v3_effective_status.py": "aff946ac806826b5516203d582672d88577c9f99c3e96c72fc191232bda000b9",
    "pf_validate_v3_effective_capture.py": "3d145407c9a6e4236eefe829c9fb9eb0757bf53cce9ac9cb136f201f594a360b",
    "pf_validate_v2_effective_capture.py": "7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9",
    "PF_STATIC_TYPE_INFO_CLASSMAP.tsv": "b5de29afb7c7af3c5b785130fdf368b4e1d089d0945441671201880f4429dea2",
    "PF_STATIC_TYPE_INFO_CLASSMAP.md": "b26f4060b6644c9653de37db0db0bf87afbcc8e8d7d9fc98f705723db221c8e2",
    "pf_build_static_type_info_classmap.py": "e25a45a13ad9b010ede4b155f219f791585e93a7637e27ae51348050f231c276",
    "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv": "10b54ee781ad0147d5bd18c0171b88132d9fd61dc39e0adf6fa4055bc7b7890d",
    "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv": "395b1776d3351304612ceb36eade9003b929fb8bb914986b4873f0737e60a5e3",
    "PF_DAILY_ACTIVITY_CLOSURE.md": "7a58caf4efb025c0703fa4a583785cb0d7d61269d4d92ddf18118da299bfc75e",
    "pf_build_daily_activity_closure.py": "e58f4da41e6f82c9a3c182961019394ebab4b8034e1d39f2c8c92b272a35d09d",
    "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv": "b81c7a5590d60c44f10e4171a722feb680e0e83865e6c5c033121e9dccffbe00",
    "PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv": "048216205e1a99a1b4561bf643e1ad80bcf1a29283a4b526ee048654fac82d44",
    "PF_EMBEDDED_CHILD_COMPOSITION.md": "4801b0412a164a53b524d96ddcb7800a56c59ad8447e83f4a3d11f88cfc0bd69",
    "pf_build_embedded_child_composition.py": "a8963458bc15fa13e7a60adf79fc75ae5183937af88ffa9a05602fbc9f8f7bba",
    "PF_V2_FIELD_VALIDATION.tsv": "10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806",
    "PF_V3_FIELD_VALIDATION.md": "d0cb385e21297ef8b052895759ece527161c958ab3fb64217aa564e63d1aed59",
}

BASE_PRIORITY = OUT / "PF_PROTOCOL_PRIORITY.tsv"
V3_OVERLAYS = tuple(status_v3.OVERLAYS)
DAILY_PRIORITY = OUT / "PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv"
COMPOSITION_PRIORITY = OUT / "PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv"
V3_OPEN = OUT / "PF_V3_P1_OPEN.tsv"
DAILY_A2 = OUT / "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv"
COMPOSITION_A2 = OUT / "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv"

A1_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "base_delta_key", "registry_name", "old_vtable_va", "new_base_class_name",
    "new_base_class_vtable_va", "retained_derived_classes",
    "retained_derived_vtables", "serializer_identity_status",
    "serializer_candidates", "serializer_selection", "canonical_a2_action",
    "classmap_file", "classmap_keys", "proof_kind", "resolution", "source",
)

PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "priority", "old_registry_identity_status",
    "new_registry_identity_status", "old_registry_identity_missing",
    "new_registry_identity_missing", "old_serializer_status",
    "new_serializer_status", "old_serializer_blockers",
    "new_serializer_blockers", "old_structural_status",
    "new_structural_status", "old_blocker", "new_blocker",
    "old_registry_identity_proof_kind", "new_registry_identity_proof_kind",
    "retained_polymorphism_nonclaim", "evidence_ticket", "closure_scope", "source",
)

OPEN_COLUMNS = status_v3.OPEN_COLUMNS
UNKNOWN_RE = re.compile(r"UNKNOWN\(([^()]*)\)")
MANIFEST_ROW_RE = re.compile(
    r"^\| `([^`]+)` \| ([0-9]+) \| `([0-9A-Fa-f]{64})` \|", re.MULTILINE
)
HISTORICAL_INDEX_NAME = "00_SEARCH_HERE_FIRST.md"
HISTORICAL_INDEX_SIZE = 11466
HISTORICAL_INDEX_SHA256 = "52be24d7b410d87aef2ba4a4aec962e4314cbf554d12a78327fdd55d82626008"


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
    data = json.dumps(
        [row[name] for name in fields], ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(data)


def delta_key(parts: Sequence[str]) -> str:
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


def format_tsv(fields: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=list(fields), delimiter="\t", lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def verify_v3_manifest() -> dict[str, str]:
    path = OUT / "PF_V3_MANIFEST.md"
    text = path.read_text(encoding="utf-8")
    entries = MANIFEST_ROW_RE.findall(text)
    if len(entries) != 99:
        raise BuildError(f"V3 manifest artifact census changed: {len(entries)}")
    if len({name for name, _size, _digest in entries}) != len(entries):
        raise BuildError("V3 manifest contains duplicate artifact names")
    measured: dict[str, str] = {}
    historical_exemptions: list[str] = []
    verified_current = 0
    for name, size_text, expected in entries:
        if name == HISTORICAL_INDEX_NAME:
            historical_exemptions.append(name)
            if (
                int(size_text) != HISTORICAL_INDEX_SIZE
                or expected.lower() != HISTORICAL_INDEX_SHA256
            ):
                raise BuildError("V3 historical index predecessor identity changed")
            # The pinned V3 manifest is the evidence for this predecessor.
            # Current index bytes are a mutable search surface and are not an
            # input to status derivation, so V4 may legitimately replace them.
            measured[f"V3_HISTORICAL:{name}"] = (
                f"{HISTORICAL_INDEX_SIZE}:{HISTORICAL_INDEX_SHA256}"
            )
            continue
        artifact = OUT / name
        if not artifact.is_file():
            raise BuildError(f"missing V3 artifact: {name}")
        actual = sha256_path(artifact)
        if actual != expected.lower():
            raise BuildError(f"V3 artifact changed: {name}")
        measured[f"V3:{name}"] = actual
        verified_current += 1
    if historical_exemptions != [HISTORICAL_INDEX_NAME] or verified_current != 98:
        raise BuildError(
            "V3 manifest exemption boundary changed: "
            f"historical={historical_exemptions} current={verified_current}"
        )
    return measured


def verify_inputs() -> dict[str, str]:
    measured = verify_v3_manifest()
    for name, expected in PINNED.items():
        path = OUT / name
        if not path.is_file():
            raise BuildError(f"missing pinned input: {name}")
        actual = sha256_path(path)
        if actual != expected:
            raise BuildError(f"pinned input changed: {name}: {actual}")
        measured[name] = actual
    image_hash = sha256_path(IMAGE)
    if image_hash != IMAGE_SHA256:
        raise BuildError(f"pinned IMAGE changed: {image_hash}")
    measured[IMAGE.name] = image_hash
    if (OUT / "PF_V4_FIELD_VALIDATION.tsv").exists():
        raise BuildError("unchanged A5 TSV was duplicated as PF_V4_FIELD_VALIDATION.tsv")
    return measured


def existing_delta_keys(excluded: set[str]) -> set[str]:
    result: set[str] = set()
    owners: dict[str, str] = {}
    for path in sorted(OUT.glob("*.tsv"), key=lambda item: item.name.casefold()):
        if path.name in excluded or path.name in OWNED:
            continue
        fields, rows = read_tsv(path)
        for column in ("delta_key", "dedup_key"):
            if column not in fields:
                continue
            for line, row in rows:
                key = row[column]
                if not key or key == "N/A":
                    continue
                if key in result:
                    raise BuildError(f"pre-existing duplicate provenance key: {key}")
                result.add(key)
                owners[key] = f"{path.name}:{line}"
    return result


def prior_targets(kind: str, excluded: set[str]) -> set[tuple[str, str, str]]:
    result: set[tuple[str, str, str]] = set()
    for path in sorted(OUT.glob("*.tsv"), key=lambda item: item.name.casefold()):
        if path.name in excluded or path.name in OWNED:
            continue
        fields, rows = read_tsv(path)
        required = {"base_file", "base_line", "base_row_key"}
        if not required.issubset(fields):
            continue
        if kind == "A2" and not {"old_tag", "direction(W/R)"}.issubset(fields):
            continue
        if kind == "A1" and "registry_name" not in fields and "name" not in fields:
            continue
        if kind == "PRIORITY" and "priority" not in fields:
            continue
        for _line, row in rows:
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            if not all(target) or "N/A" in target:
                continue
            if target in result:
                raise BuildError(f"pre-existing duplicate {kind} base target: {target}")
            result.add(target)
    return result


def one_row(path: Path, predicate) -> tuple[list[str], int, dict[str, str]]:
    fields, rows = read_tsv(path)
    matches = [(line, row) for line, row in rows if predicate(row)]
    if len(matches) != 1:
        raise BuildError(f"expected one predecessor in {path.name}, got {len(matches)}")
    line, row = matches[0]
    return fields, line, row


def build_a1() -> list[dict[str, str]]:
    class_fields, class_rows = read_tsv(OUT / "PF_STATIC_TYPE_INFO_CLASSMAP.tsv")
    if len(class_rows) != 4 or any(row["source"] != "IMAGE" for _line, row in class_rows):
        raise BuildError("static classmap must contain four IMAGE rows")
    by_registry: dict[str, list[dict[str, str]]] = {}
    for _line, row in class_rows:
        by_registry.setdefault(row["registry_name"], []).append(row)
    if set(by_registry) != {"ItemAttr", "VitalData"}:
        raise BuildError("static classmap registry set changed")
    item_exact = next(row for row in by_registry["ItemAttr"] if row["identity_kind"] == "EXACT_REGISTRY_CLASS")
    item_derived = next(row for row in by_registry["ItemAttr"] if row["identity_kind"].startswith("POLYMORPHIC_"))
    vital_exact = next(row for row in by_registry["VitalData"] if row["identity_kind"] == "EXACT_REGISTRY_CLASS")
    vital_derived = next(row for row in by_registry["VitalData"] if row["identity_kind"].startswith("POLYMORPHIC_"))
    expected = (
        item_exact["class_name"], item_exact["vtable_va"],
        item_derived["class_name"], item_derived["vtable_va"],
        vital_exact["class_name"], vital_exact["vtable_va"],
        vital_derived["class_name"], vital_derived["vtable_va"],
    )
    if expected != (
        "ItemAttr", "0x00F0EBB0", "StallItem", "0x00F4A188",
        "VitalData", "0x00F0B930", "Channel_MessageVtial", "0x00F375FC",
    ):
        raise BuildError(f"static classmap identities changed: {expected}")

    item_fields, item_line, item_base = one_row(
        OUT / "PF_A1_SERIALIZER_SLOT34_DELTA.tsv", lambda row: row.get("name") == "ItemAttr"
    )
    vital_fields, vital_line, vital_base = one_row(
        OUT / "PF_PROTOCOL_REGISTRY.tsv", lambda row: row.get("name") == "VitalData"
    )
    if (
        item_base["classification"] != "SLOT34_TWO_CANDIDATES_NO_SINGLETON"
        or item_base["corrected_candidates"]
        != "vtable=0x00F0EBB0,serializer=0x0046BD30,pointer_file_off=0x00B0CFE4|vtable=0x00F4A188,serializer=0x00766C90,pointer_file_off=0x00B485BC"
    ):
        raise BuildError("ItemAttr slot34 candidate family changed")
    if vital_base["vtable_va"] != "UNKNOWN" or vital_base["serializer_va"] != "UNKNOWN":
        raise BuildError("VitalData V1 predecessor changed")

    rows: list[dict[str, str]] = []
    specs = (
        (
            "ItemAttr", "PF_A1_SERIALIZER_SLOT34_DELTA.tsv", item_fields, item_line,
            item_base, item_base["delta_key"], "UNKNOWN", "ItemAttr", "0x00F0EBB0",
            "StallItem", "0x00F4A188", "KNOWN_POLYMORPHIC_SET",
            "0x0046BD30|0x00766C90", "WITHHELD_NOT_SINGLETON", "NO_CHANGE",
            (item_exact["classmap_key"], item_derived["classmap_key"]),
            "EXACT_BASE_CLASS_AND_RETAINED_DERIVED",
            "BASE_IDENTITY_KNOWN;POLYMORPHIC_SERIALIZER_SET_RETAINED",
        ),
        (
            "VitalData", "PF_PROTOCOL_REGISTRY.tsv", vital_fields, vital_line,
            vital_base, "N/A", "UNKNOWN", "VitalData", "0x00F0B930",
            "Channel_MessageVtial", "0x00F375FC", "UNKNOWN",
            "UNKNOWN", "WITHHELD", "NO_CHANGE",
            (vital_exact["classmap_key"], vital_derived["classmap_key"]),
            "EXACT_BASE_CLASS_AND_RETAINED_DERIVED",
            "BASE_IDENTITY_KNOWN;SERIALIZER_STILL_UNKNOWN",
        ),
    )
    for (
        name, base_file, fields, line, base, base_delta, old_vtable, base_class,
        base_vtable, derived, derived_vtable, serializer_status, candidates,
        selection, a2_action, class_keys, proof, resolution,
    ) in specs:
        base_key = canonical_row_key(fields, base)
        values = {
            "action": "CHANGED_STATIC_TYPE_IDENTITY",
            "base_file": base_file,
            "base_line": str(line),
            "base_row_key": base_key,
            "base_delta_key": base_delta,
            "registry_name": name,
            "old_vtable_va": old_vtable,
            "new_base_class_name": base_class,
            "new_base_class_vtable_va": base_vtable,
            "retained_derived_classes": derived,
            "retained_derived_vtables": derived_vtable,
            "serializer_identity_status": serializer_status,
            "serializer_candidates": candidates,
            "serializer_selection": selection,
            "canonical_a2_action": a2_action,
            "classmap_file": "PF_STATIC_TYPE_INFO_CLASSMAP.tsv",
            "classmap_keys": "|".join(class_keys),
            "proof_kind": proof,
            "resolution": resolution,
            "source": "IMAGE",
        }
        values["delta_key"] = delta_key(("A1_STATIC_TYPE_INFO", name, base_key, *class_keys))
        rows.append(values)
    return rows


def state_from_priority_row(row: Mapping[str, str]) -> dict[str, object]:
    return {
        "message": row["message"], "priority": row["priority"],
        "matched_groups": row["matched_groups"], "matched_keywords": row["matched_keywords"],
        "registry_identity_status": row["registry_identity_status"],
        "registry_identity_missing": row["registry_identity_missing"],
        "serializer_status": row["serializer_status"],
        "serializer_blockers": row["serializer_blockers"],
        "structural_status": row["structural_status"], "blocker": row["blocker"],
        "base_registry_identity_status": row["registry_identity_status"],
        "base_serializer_status": row["serializer_status"],
        "base_structural_status": row["structural_status"],
        "chain": ["BASE_ONLY"], "last_ref_file": BASE_PRIORITY.name,
        "last_ref_line": "", "last_ref_key": "", "last_delta_key": "N/A",
    }


def build_static_priority() -> list[dict[str, str]]:
    item_fields, item_line, item = one_row(
        OUT / "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv",
        lambda row: row.get("message") == "ItemAttr",
    )
    vital_fields, vital_line, vital = one_row(
        BASE_PRIORITY, lambda row: row.get("message") == "VitalData"
    )
    genuine = (
        "atomic_target_object_alias_unproved | direct_call_not_proven_serializer | "
        "dynamic_vtable_plus_0x04_target_unresolved | "
        "indirect_call_not_proven_serializer_slot | indirect_serializer_direction_unresolved"
    )
    specs = (
        (
            "ItemAttr", "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv", item_fields,
            item_line, item, item["delta_key"], item["new_registry_identity_status"],
            "KNOWN", item["new_registry_identity_missing"], "N/A",
            item["new_serializer_status"], "OPEN", item["new_serializer_blockers"],
            genuine, item["new_structural_status"], "OPEN", item["new_blocker"],
            genuine, "OPEN_UNRESOLVED", "KNOWN_AS_POLYMORPHIC_SET",
            "ItemAttr and StallItem remain separate; no 26-row or 30-row candidate is selected or copied",
        ),
        (
            "VitalData", BASE_PRIORITY.name, vital_fields, vital_line, vital, "N/A",
            vital["registry_identity_status"], "OPEN", vital["registry_identity_missing"],
            "serializer", vital["serializer_status"], "OPEN", vital["serializer_blockers"],
            "registry_serializer_unresolved", vital["structural_status"], "OPEN",
            vital["blocker"], "registry serializer UNKNOWN | registry_serializer_unresolved",
            "OPEN_UNRESOLVED", "EXACT_BASE_VTABLE_SERIALIZER_OPEN",
            "Channel_MessageVtial remains a separate derived class; no serializer identity is inferred",
        ),
    )
    rows: list[dict[str, str]] = []
    for spec in specs:
        (
            message, base_file, fields, line, base, base_delta, old_reg, new_reg,
            old_missing, new_missing, old_ser, new_ser, old_ser_block, new_ser_block,
            old_struct, new_struct, old_block, new_block, old_proof, new_proof, nonclaim,
        ) = spec
        base_key = canonical_row_key(fields, base)
        values = {
            "action": "CHANGED", "base_file": base_file, "base_line": str(line),
            "base_row_key": base_key, "base_delta_key": base_delta,
            "message": message, "priority": "1",
            "old_registry_identity_status": old_reg,
            "new_registry_identity_status": new_reg,
            "old_registry_identity_missing": old_missing,
            "new_registry_identity_missing": new_missing,
            "old_serializer_status": old_ser, "new_serializer_status": new_ser,
            "old_serializer_blockers": old_ser_block,
            "new_serializer_blockers": new_ser_block,
            "old_structural_status": old_struct, "new_structural_status": new_struct,
            "old_blocker": old_block, "new_blocker": new_block,
            "old_registry_identity_proof_kind": old_proof,
            "new_registry_identity_proof_kind": new_proof,
            "retained_polymorphism_nonclaim": nonclaim,
            "evidence_ticket": "STATIC-TYPE-INFO-CLASSMAP",
            "closure_scope": "REGISTRY_IDENTITY_ONLY;NO_STRUCTURAL_CLOSURE;NO_A2_ACTIVATION;V3_IMMUTABLE",
            "source": "IMAGE",
        }
        values["delta_key"] = delta_key((
            "PRIORITY_STATIC_TYPE_INFO", message, base_key, new_reg, new_missing,
            new_ser_block, new_block,
        ))
        rows.append(values)
    return rows


def effective_blockers(fields: Sequence[object]) -> tuple[str, ...]:
    reasons: set[str] = set()
    for value in fields:
        reasons.update(UNKNOWN_RE.findall(str(value.field_offset)))
        if value.tag == "UNKNOWN" and not UNKNOWN_RE.findall(str(value.field_offset)):
            reasons.add("unknown_tag")
    return tuple(sorted(reasons))


def source_row(path: Path, line: int) -> tuple[list[str], dict[str, str]]:
    fields, rows = read_tsv(path)
    matches = [row for row_line, row in rows if row_line == line]
    if len(matches) != 1:
        raise BuildError(f"missing source row: {path.name}:{line}")
    return fields, matches[0]


def apply_v4_a2() -> tuple[dict, dict, dict[str, int], dict[str, tuple[str, ...]]]:
    registry, effective, candidates, counts, _per_file = field_v3.apply_v3_removals(OUT)
    if counts.get("effective_rows") != 8671:
        raise BuildError(f"V3 effective A2 drift: {counts}")
    numeric_before = Counter(
        value.tag for rows in effective.values() for value in rows
        if field_v3.v2.NUMERIC_TAG_RE.fullmatch(value.tag)
    )
    prior = prior_targets("A2", {DAILY_A2.name, COMPOSITION_A2.name})
    seen_targets: set[tuple[str, str, str]] = set()
    seen_keys: set[str] = set()
    prior_keys = existing_delta_keys({DAILY_A2.name, COMPOSITION_A2.name})
    index: dict[tuple[str, str, str], tuple[tuple[str, str], object]] = {}
    for semantic, rows in effective.items():
        for value in rows:
            key = (semantic[0], semantic[1], value.evidence_key)
            if key in index:
                raise BuildError(f"duplicate effective A2 evidence key: {key}")
            index[key] = (semantic, value)
    child_unknown_by_key: dict[str, int] = {}
    file_counts: Counter[str] = Counter()
    for path in (DAILY_A2, COMPOSITION_A2):
        fields, rows = read_tsv(path)
        expected = 12 if path == DAILY_A2 else 6
        if len(rows) != expected:
            raise BuildError(f"A2 overlay row count changed: {path.name}:{len(rows)}")
        for _line, row in rows:
            if row.get("source") != "IMAGE":
                raise BuildError(f"mixed source in A2 overlay: {path.name}")
            if row["delta_key"] in prior_keys or row["delta_key"] in seen_keys:
                raise BuildError(f"duplicate A2 delta key: {row['delta_key']}")
            seen_keys.add(row["delta_key"])
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            if target in prior or target in seen_targets:
                raise BuildError(f"duplicate A2 base target: {target}")
            seen_targets.add(target)
            source_fields, base = source_row(OUT / row["base_file"], int(row["base_line"]))
            if canonical_row_key(source_fields, base) != row["base_row_key"]:
                raise BuildError(f"A2 base key mismatch: {path.name}:{row['base_line']}")
            if base.get("source") != "IMAGE":
                raise BuildError("A2 base source is not IMAGE")
            if row["base_file"] == "PF_SERIALIZER_FIELDS.tsv":
                evidence_key = row["base_row_key"]
                if row["base_delta_key"] != "N/A":
                    raise BuildError("V1 A2 target has a delta predecessor")
            elif row["base_file"] == "PF_A2_SERIALIZER_SLOT34_DELTA.tsv":
                evidence_key = row["base_delta_key"]
                if base.get("delta_key") != evidence_key:
                    raise BuildError("slot34 A2 predecessor key mismatch")
            else:
                raise BuildError(f"unsupported V4 A2 base: {row['base_file']}")
            lookup = (row["message"], row["direction(W/R)"], evidence_key)
            match = index.get(lookup)
            if match is None:
                raise BuildError(f"V4 A2 target is not still effective: {lookup}")
            semantic, old = match
            old_values = (old.wire_order, old.tag, old.field_offset, old.length)
            expected_old = (
                row["old_order"], row["old_tag"], row["old_field_offset"], row["old_len"]
            )
            if old_values != expected_old:
                raise BuildError(f"V4 A2 old-row mismatch: {lookup}")
            effective[semantic].remove(old)
            del index[lookup]
            if row["action"] == "CHANGED":
                child_fields = effective[(row["child_message"], row["direction(W/R)"])]
                child_unknown = sum(
                    value.tag == "UNKNOWN" or "UNKNOWN(" in value.field_offset
                    for value in child_fields
                )
                if (
                    len(child_fields) != int(row["child_effective_rows"])
                    or child_unknown != int(row["child_effective_unknown_rows"])
                ):
                    raise BuildError(
                        f"child reference census is not re-derived: {row['message']}:"
                        f"{row['direction(W/R)']}->{row['child_message']}"
                    )
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
                index[(semantic[0], semantic[1], replacement.evidence_key)] = (semantic, replacement)
                child_unknown_by_key[replacement.evidence_key] = child_unknown
            elif not row["action"].startswith("REMOVE"):
                raise BuildError(f"unsupported V4 A2 action: {row['action']}")
            file_counts[path.name] += 1
    if dict(file_counts) != {DAILY_A2.name: 12, COMPOSITION_A2.name: 6}:
        raise BuildError(f"V4 A2 overlay census changed: {dict(file_counts)}")
    for rows in effective.values():
        rows.sort(key=lambda value: value.sequence)
    field_v3.v2.validate_effective_tag_census(OUT, effective)
    numeric_after = Counter(
        value.tag for rows in effective.values() for value in rows
        if field_v3.v2.NUMERIC_TAG_RE.fullmatch(value.tag)
    )
    if numeric_after != numeric_before or sum(numeric_after.values()) != 4081:
        raise BuildError("A3 numeric frequency changed")
    flat = [value for rows in effective.values() for value in rows]
    measured = {
        "rows": len(flat),
        "unknown": sum(value.tag == "UNKNOWN" or "UNKNOWN(" in value.field_offset for value in flat),
        "generic": sum(value.tag.startswith(("CALL_UNCLASSIFIED:", "JUMP_UNCLASSIFIED:")) for value in flat),
        "direct_invalid": sum(value.tag == "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL" for value in flat),
        "a3": sum(numeric_after.values()),
    }
    if measured != {"rows": 8657, "unknown": 3963, "generic": 1312, "direct_invalid": 881, "a3": 4081}:
        raise BuildError(f"V4 effective A2 census mismatch: {measured}")
    planning: dict[tuple[str, str], list[object]] = {}
    for semantic, rows in effective.items():
        planning[semantic] = []
        for value in rows:
            if value.tag != "STATIC_EMBEDDED_CHILD_REF":
                planning[semantic].append(value)
                continue
            child_unknown = child_unknown_by_key[value.evidence_key]
            planning[semantic].append(dataclasses.replace(
                value,
                tag="EMPTY" if child_unknown == 0 else "UNKNOWN",
                length="0" if child_unknown == 0 else "N/A",
                field_offset="N/A" if child_unknown == 0 else "UNKNOWN(child_schema_static_open)",
            ))
    _ids, plans = field_v3.v2.build_schema_plans(registry, planning, candidates)
    measured["plan_applicable"] = sum(plan.state == "APPLICABLE" for plan in plans.values())
    measured["plan_static_open"] = sum(plan.state == "STATIC_OPEN" for plan in plans.values())
    measured["plan_not_applied"] = sum(plan.state == "SCHEMA_NOT_APPLIED" for plan in plans.values())
    if (measured["plan_applicable"], measured["plan_static_open"], measured["plan_not_applied"]) != (624, 368, 46):
        raise BuildError(f"V4 schema plan census mismatch: {measured}")
    residuals = {
        message: effective_blockers([
            value for direction in ("W", "R") for value in effective[(message, direction)]
        ])
        for message in {"DailyActivityState", "ActorActivity_UpdateDailyActivityStateVital", "DBSS_GuildStorageInitialVital"}
    }
    return effective, candidates, measured, residuals


def status_counts(states: Mapping[str, Mapping[str, object]]) -> dict[int, tuple[int, int]]:
    result = {}
    for priority in (1, 2, 3):
        selected = [row for row in states.values() if int(row["priority"]) == priority]
        result[priority] = (
            sum(row["structural_status"] == "CLOSED" for row in selected), len(selected)
        )
    return result


def build_checkpoint_rows(states: Mapping[str, Mapping[str, object]], base_lines: Mapping[str, int]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for message in sorted(states):
        state = states[message]
        if state["priority"] != "1" or state["structural_status"] != "OPEN":
            continue
        group = status_v3.primary_blocker_group(state)  # type: ignore[arg-type]
        chain = " -> ".join(state["chain"])  # type: ignore[arg-type]
        key_parts = [
            message, str(state["registry_identity_status"]), str(state["serializer_status"]),
            str(state["structural_status"]), group, str(state["blocker"]), chain,
        ]
        rows.append({
            "status_key": sha256_bytes("\x1f".join(key_parts).encode("utf-8")),
            "message": message, "priority": "1",
            "matched_groups": str(state["matched_groups"]),
            "matched_keywords": str(state["matched_keywords"]),
            "base_line": str(base_lines[message]),
            "base_registry_identity_status": str(state["base_registry_identity_status"]),
            "effective_registry_identity_status": str(state["registry_identity_status"]),
            "effective_registry_identity_missing": str(state["registry_identity_missing"]),
            "base_serializer_status": str(state["base_serializer_status"]),
            "effective_serializer_status": str(state["serializer_status"]),
            "base_structural_status": str(state["base_structural_status"]),
            "effective_structural_status": str(state["structural_status"]),
            "primary_blocker_group": group, "effective_blocker": str(state["blocker"]),
            "applied_overlay_chain": chain,
            "row_semantics": "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW",
            "source": "IMAGE",
        })
    return rows


def replay_status(static_rows: list[dict[str, str]], residuals: Mapping[str, tuple[str, ...]]) -> tuple[list[dict[str, str]], Counter[str], int]:
    base_fields, base_rows = read_tsv(BASE_PRIORITY)
    if len(base_rows) != 519:
        raise BuildError("V1 priority row count changed")
    states: dict[str, dict[str, object]] = {}
    base_lines: dict[str, int] = {}
    loaded: dict[str, tuple[list[str], list[tuple[int, dict[str, str]]]]] = {
        BASE_PRIORITY.name: (base_fields, base_rows)
    }
    for line, row in base_rows:
        if row["message"] in states or row["source"] != "IMAGE":
            raise BuildError("invalid V1 priority identity/source")
        state = state_from_priority_row(row)
        state["last_ref_line"] = str(line)
        state["last_ref_key"] = canonical_row_key(base_fields, row)
        states[row["message"]] = state
        base_lines[row["message"]] = line
    if status_counts(states) != {1: (241, 365), 2: (12, 16), 3: (84, 138)}:
        raise BuildError("V1 priority counts changed")

    seen_keys: set[str] = set()
    seen_targets: set[tuple[str, str, str]] = set()

    def apply(path_name: str, fields: list[str], rows: list[tuple[int, dict[str, str]]], derived_base: bool = False) -> None:
        loaded[path_name] = (fields, rows)
        local_messages: set[str] = set()
        for line, row in rows:
            message = row["message"]
            if message not in states or message in local_messages:
                raise BuildError(f"bad/duplicate status message: {path_name}:{message}")
            local_messages.add(message)
            if row["source"] != "IMAGE" or row["action"] != "CHANGED":
                raise BuildError(f"bad status action/source: {path_name}:{line}")
            if row["delta_key"] in seen_keys:
                raise BuildError(f"duplicate status delta key: {row['delta_key']}")
            seen_keys.add(row["delta_key"])
            ref_file = row["base_file"]
            if ref_file not in loaded:
                raise BuildError(f"unknown status predecessor: {path_name}:{ref_file}")
            ref_fields, ref_rows = loaded[ref_file]
            ref_matches = [ref for ref_line, ref in ref_rows if str(ref_line) == row["base_line"]]
            if len(ref_matches) != 1:
                raise BuildError(f"missing status predecessor line: {path_name}:{message}")
            ref = ref_matches[0]
            if canonical_row_key(ref_fields, ref) != row["base_row_key"] or ref.get("message") != message:
                raise BuildError(f"status predecessor key/message mismatch: {path_name}:{message}")
            target = (ref_file, row["base_line"], row["base_row_key"])
            if target in seen_targets:
                raise BuildError(f"duplicate status predecessor target: {target}")
            seen_targets.add(target)
            state = states[message]
            is_v3_index = ref_file == V3_OPEN.name
            if is_v3_index:
                if not derived_base:
                    raise BuildError("V3 derived index used outside composition overlay")
                if row.get("base_delta_key") != ref["status_key"]:
                    raise BuildError("V3 status_key predecessor mismatch")
                expected_ref = (
                    ref["effective_registry_identity_status"], ref["effective_registry_identity_missing"],
                    ref["effective_serializer_status"], ref["effective_structural_status"],
                    ref["effective_blocker"], ref["applied_overlay_chain"],
                )
                actual_ref = (
                    state["registry_identity_status"], state["registry_identity_missing"],
                    state["serializer_status"], state["structural_status"], state["blocker"],
                    " -> ".join(state["chain"]),
                )
                if expected_ref != actual_ref:
                    raise BuildError(f"V3 derived predecessor semantic mismatch: {message}")
            else:
                if (
                    state["last_ref_file"] != ref_file
                    or state["last_ref_line"] != row["base_line"]
                    or state["last_ref_key"] != row["base_row_key"]
                ):
                    raise BuildError(f"status overlay is not chained: {path_name}:{message}")
                if ref_file == BASE_PRIORITY.name:
                    if row.get("base_delta_key", "N/A") != "N/A":
                        raise BuildError("V1 priority predecessor has non-N/A delta key")
                elif "base_delta_key" in row and row["base_delta_key"] != ref.get("delta_key"):
                    raise BuildError(f"status predecessor delta key mismatch: {path_name}:{message}")
            comparisons = (
                ("priority", "priority"),
                ("old_registry_identity_status", "registry_identity_status"),
                ("old_registry_identity_missing", "registry_identity_missing"),
                ("old_serializer_status", "serializer_status"),
                ("old_serializer_blockers", "serializer_blockers"),
                ("old_structural_status", "structural_status"),
                ("old_blocker", "blocker"),
            )
            for row_name, state_name in comparisons:
                if row_name in row and row[row_name] != state[state_name]:
                    raise BuildError(f"old status mismatch: {path_name}:{message}:{row_name}")
            state["registry_identity_status"] = row.get("new_registry_identity_status", state["registry_identity_status"])
            state["registry_identity_missing"] = row.get("new_registry_identity_missing", state["registry_identity_missing"])
            state["serializer_status"] = row["new_serializer_status"]
            state["serializer_blockers"] = row.get("new_serializer_blockers", row["new_blocker"])
            state["structural_status"] = row["new_structural_status"]
            state["blocker"] = row["new_blocker"]
            state["chain"].append(path_name)  # type: ignore[union-attr]
            state["last_ref_file"] = path_name
            state["last_ref_line"] = str(line)
            state["last_ref_key"] = canonical_row_key(fields, row)
            state["last_delta_key"] = row["delta_key"]

    for path in V3_OVERLAYS:
        fields, rows = read_tsv(path)
        apply(path.name, fields, rows)
    if status_counts(states) != {1: (254, 365), 2: (8, 16), 3: (70, 138)}:
        raise BuildError("V3 priority replay mismatch")
    # V3 deliberately emits no status-delta copies for eight touched messages
    # that remain OPEN.  Their blocker strings and chain marker are derived from
    # final V3 A2.  Bind that metadata to the pinned V3 derived index before
    # checking byte identity; structural transitions above still come only from
    # the replayed evidence-bearing priority overlays.
    v3_fields, v3_loaded_rows = read_tsv(V3_OPEN)
    if len(v3_loaded_rows) != 111:
        raise BuildError("V3 derived OPEN row count changed")
    for _line, row in v3_loaded_rows:
        state = states[row["message"]]
        if (
            state["priority"] != "1"
            or state["structural_status"] != "OPEN"
            or state["registry_identity_status"] != row["effective_registry_identity_status"]
            or state["registry_identity_missing"] != row["effective_registry_identity_missing"]
        ):
            raise BuildError(f"V3 derived checkpoint contradicts replay: {row['message']}")
        state["serializer_status"] = row["effective_serializer_status"]
        if "DERIVED_EFFECTIVE_A2(" in row["applied_overlay_chain"]:
            state["serializer_blockers"] = row["effective_blocker"]
        state["structural_status"] = row["effective_structural_status"]
        state["blocker"] = row["effective_blocker"]
        state["chain"] = row["applied_overlay_chain"].split(" -> ")
    v3_rows = build_checkpoint_rows(states, base_lines)
    v3_text = format_tsv(OPEN_COLUMNS, v3_rows).encode("utf-8")
    if V3_OPEN.read_bytes() != v3_text:
        raise BuildError("V3 derived OPEN index does not match status replay")
    loaded[V3_OPEN.name] = (v3_fields, v3_loaded_rows)

    fields, rows = read_tsv(DAILY_PRIORITY)
    apply(DAILY_PRIORITY.name, fields, rows)
    fields, rows = read_tsv(COMPOSITION_PRIORITY)
    apply(COMPOSITION_PRIORITY.name, fields, rows, derived_base=True)
    apply(PRIORITY_OUT.name, list(PRIORITY_COLUMNS), list(enumerate(static_rows, start=2)))
    final_counts = status_counts(states)
    expected_counts = {1: (255, 365), 2: (8, 16), 3: (71, 138)}
    if final_counts != expected_counts:
        raise BuildError(f"V4 priority counts mismatch: {final_counts}")
    if residuals["DailyActivityState"] or residuals["ActorActivity_UpdateDailyActivityStateVital"]:
        raise BuildError(f"claimed closure retains A2 blockers: {residuals}")
    final_rows = build_checkpoint_rows(states, base_lines)
    if len(final_rows) != 110:
        raise BuildError(f"V4 P1 OPEN count mismatch: {len(final_rows)}")
    groups = Counter(row["primary_blocker_group"] for row in final_rows)
    expected_groups = Counter({
        "CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED": 14,
        "DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED": 79,
        "INDIRECT_JUMP_TARGET_UNRESOLVED": 0,
        "OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED": 7,
        "REGISTRY_IDENTITY_UNRESOLVED": 10,
    })
    if groups != +expected_groups:
        raise BuildError(f"V4 P1 blocker groups mismatch: {dict(groups)}")
    old_by_message = {row["message"]: row for row in v3_rows}
    inherited = sum(old_by_message.get(row["message"]) == row for row in final_rows)
    if inherited != 107:
        raise BuildError(f"V4 inherited derived-row census changed: {inherited}")
    return final_rows, groups, inherited


def audit_generated_keys(a1: list[dict[str, str]], priority: list[dict[str, str]]) -> None:
    new = [row["delta_key"] for row in a1 + priority]
    if len(new) != len(set(new)):
        raise BuildError("generated A1/priority delta key collision")
    prior = existing_delta_keys(set())
    if prior & set(new):
        raise BuildError("generated delta key repeats prior output")
    for kind, rows in (("A1", a1), ("PRIORITY", priority)):
        prior_refs = prior_targets(kind, set())
        targets = {(row["base_file"], row["base_line"], row["base_row_key"]) for row in rows}
        if len(targets) != len(rows) or prior_refs & targets:
            raise BuildError(f"generated {kind} base target overlaps prior output")
    if any(row["source"] != "IMAGE" for row in a1 + priority):
        raise BuildError("generated mixed-source row")


def report_text(measured: Mapping[str, int], groups: Mapping[str, int], inherited: int) -> str:
    return "\n".join([
        "# PF V4 effective IMAGE-static priority status",
        "",
        "[MEASURED][IMAGE] V4 replays all 519 priority states through V3, DailyActivityState, embedded-child composition, and the static type-identity delta. CAPTURE, DUMP, and DATA remain separate evidence layers.",
        "",
        "## Effective result",
        "",
        "- Priority 1: **255/365 CLOSED** (69.86%); OPEN 110",
        "- Priority 2: **8/16 CLOSED** (50.00%); OPEN 8",
        "- Priority 3: **71/138 CLOSED** (51.45%); OPEN 67",
        "- Overall: **334/519 CLOSED** (64.35%); OPEN 185",
        "- New structural closures: `DailyActivityState` (P3) and `ActorActivity_UpdateDailyActivityStateVital` (P1).",
        "",
        "## Effective A2 and duplicate control",
        "",
        f"- Stored/reference A2 rows: **{measured['rows']}**; UNKNOWN {measured['unknown']}; generic CALL/JUMP UNKNOWN {measured['generic']}; direct invalid-parameter UNKNOWN {measured['direct_invalid']}.",
        f"- A3 numeric-tag frequency remains **{measured['a3']}**.",
        "- Daily removes 12 still-effective rows. Composition removes two directionally impossible rows and replaces four coarse rows with physical child-schema references.",
        "- The reference overlay avoids materializing 76 V3 child rows (52 guild plus 24 daily). After the Daily removals, those references resolve to 64 current child rows; none is copied into parent A2.",
        "- New A2 delta-key overlap: 0; new A2 base-target overlap: 0; unchanged/copied child rows: 0.",
        "",
        "## Static registry identity",
        "",
        "- ItemAttr base identity is exact at vtable `0x00F0EBB0`; the StallItem `0x00F4A188` polymorphic variant remains separate. Serializer family `{0x0046BD30,0x00766C90}` is known as a set, but neither the 26-row nor the 30-row schema is selected, merged, or copied.",
        "- VitalData base identity is exact at vtable `0x00F0B930`; Channel_MessageVtial remains an exact retained derived class. Its serializer remains UNKNOWN.",
        "- These two A1 identity rows produce zero structural closures. ItemAttr moves from registry blocker to dynamic blocker; VitalData remains a registry blocker narrowed to serializer only.",
        "",
        "## Priority-1 OPEN primary blocker groups",
        "",
        "| primary group | messages |",
        "|---|---:|",
        f"| `CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED` | {groups.get('CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED', 0)} |",
        f"| `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED` | {groups.get('DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED', 0)} |",
        f"| `INDIRECT_JUMP_TARGET_UNRESOLVED` | {groups.get('INDIRECT_JUMP_TARGET_UNRESOLVED', 0)} |",
        f"| `OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED` | {groups.get('OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED', 0)} |",
        f"| `REGISTRY_IDENTITY_UNRESOLVED` | {groups.get('REGISTRY_IDENTITY_UNRESOLVED', 0)} |",
        "",
        f"- The OPEN index has 110 rows. {inherited} rows are byte-identical derived references from V3 and are explicitly not new evidence; three OPEN rows changed and one V3 OPEN row closed.",
        "",
        "## A5 boundary",
        "",
        f"- Schema plans: APPLICABLE {measured['plan_applicable']} / STATIC_OPEN {measured['plan_static_open']} / SCHEMA_NOT_APPLIED {measured['plan_not_applied']}.",
        "- A5 aggregate remains 22,965 parse-pass / 78,532 static-open / 0 schema-not-applied / 386 mismatch. The canonical TSV remains `PF_V2_FIELD_VALIDATION.tsv`; no duplicate V4 field-validation TSV is emitted.",
        "- The existing 386 CAPTURE mismatches remain red and are not rewritten into IMAGE facts.",
        "",
        "## Reproduction and scope",
        "",
        "Run `py -3 -B pf_build_v4_effective_status.py --audit-only`, then normal publication, then `--check`. The normal mode uses an exclusive lock, staged transaction, journal-before-replace, rollback, input re-hash, and byte-exact readback.",
        "",
        "No server/runtime/dump/capture/workflow/queue/Git file is written or run. All emitted TSV rows use `source=IMAGE`.",
        "",
    ])


def build() -> tuple[dict[Path, bytes], dict[str, int], Counter[str], int]:
    before = verify_inputs()
    a1 = build_a1()
    static_priority = build_static_priority()
    audit_generated_keys(a1, static_priority)
    _effective, _candidates, measured, residuals = apply_v4_a2()
    open_rows, groups, inherited = replay_status(static_priority, residuals)
    if len({row["status_key"] for row in open_rows}) != len(open_rows):
        raise BuildError("duplicate V4 status key")
    outputs = {
        A1_OUT: format_tsv(A1_COLUMNS, a1).encode("utf-8"),
        PRIORITY_OUT: format_tsv(PRIORITY_COLUMNS, static_priority).encode("utf-8"),
        OPEN_OUT: format_tsv(OPEN_COLUMNS, open_rows).encode("utf-8"),
        REPORT_OUT: report_text(measured, groups, inherited).encode("ascii"),
    }
    after = verify_inputs()
    if before != after:
        raise BuildError("pinned inputs changed during V4 derivation")
    return outputs, measured, groups, inherited


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
        str(lock),
        GENERIC_READ | GENERIC_WRITE | DELETE_ACCESS,
        FILE_SHARE_READ,
        None,
        CREATE_NEW,
        FILE_ATTRIBUTE_NORMAL,
        None,
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
    return bytes(buffer.raw[: read.value])


def assert_lock_owner(handle, token: str) -> None:
    expected = lock_payload(token)
    if read_lock_handle(handle, len(expected)) != expected:
        raise BuildError("publication lock ownership token changed")


def mark_lock_delete_on_close(handle) -> None:
    disposition = FileDispositionInfo(ctypes.c_ubyte(1))
    if not KERNEL32.SetFileInformationByHandle(
        handle,
        FILE_DISPOSITION_INFO_CLASS,
        ctypes.byref(disposition),
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
            if target.parent.resolve() != root.resolve():
                raise BuildError(f"publication target outside root: {target}")
            stage = tx / (target.name + ".stage")
            with stage.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            staged[target] = stage
            if target.exists():
                originals[target] = target.read_bytes()
                backup = tx / (target.name + ".backup")
                shutil.copyfile(target, backup)
                with backup.open("r+b") as stream:
                    os.fsync(stream.fileno())
                if backup.read_bytes() != target.read_bytes():
                    raise BuildError(f"backup readback mismatch: {target.name}")
                backups[target] = backup
            else:
                originals[target] = None
        verify_callback()
        assert_lock_owner(handle, token)
        journal = tx / "journal.json"
        journal_state: dict[str, object] = {
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
        write_journal(journal, journal_state)
        attempted: list[Path] = []
        try:
            for target in outputs:
                # Mark and fsync the target before replacement.  Recovery must
                # include this target even if BaseException lands immediately
                # after os.replace and before any following Python statement.
                attempted.append(target)
                journal_state["status"] = "REPLACING"
                journal_state["attempted"] = [path.name for path in attempted]
                write_journal(journal, journal_state)
                assert_lock_owner(handle, token)
                os.replace(staged[target], target)
                if hook is not None:
                    hook("after_replace", target, lock, token)
                journal_state["replaced"] = [
                    *journal_state["replaced"], target.name  # type: ignore[misc]
                ]
                write_journal(journal, journal_state)
            for target, data in outputs.items():
                if target.read_bytes() != data:
                    raise BuildError(f"post-publish readback mismatch: {target.name}")
            verify_callback()
            assert_lock_owner(handle, token)
            journal_state["status"] = "COMMITTED"
            write_journal(journal, journal_state)
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
                        # Copy, do not consume, the backup.  A failed operation
                        # retains the exact recovery material and journal.
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
                journal_state["status"] = (
                    "ROLLBACK_INCOMPLETE" if errors else "ROLLED_BACK_AFTER_FAILURE"
                )
                journal_state["rollback_errors"] = errors
                write_journal(journal, journal_state)
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
                # The Windows handle denies delete/write sharing for its whole
                # lifetime.  Mark this exact owned inode delete-on-close; never
                # unlink a pathname that another actor could have replaced.
                assert_lock_owner(handle, token)
                if tx is None or not tx.is_dir():
                    raise BuildError("committed transaction directory disappeared")
                shutil.rmtree(tx)
                tx = None
                assert_lock_owner(handle, token)
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
    with tempfile.TemporaryDirectory(prefix="pf_v4_publication_selftest_") as temporary:
        test_root = Path(temporary)

        interrupt_root = test_root / "interrupt"
        interrupt_root.mkdir()
        first = interrupt_root / "first.out"
        second = interrupt_root / "second.out"
        first.write_bytes(b"old-first")

        def interrupt_hook(event, target, _lock, _token) -> None:
            if event == "after_replace" and target == first:
                raise InjectedPublicationAbort("after replace")

        try:
            publish_transaction(
                interrupt_root,
                {first: b"new-first", second: b"new-second"},
                lambda: None,
                interrupt_hook,
            )
        except InjectedPublicationAbort:
            pass
        else:
            raise BuildError("interrupt-after-replace injection did not fire")
        interrupt_tx = list(interrupt_root.glob(TX_PREFIX + "*"))
        if (
            first.read_bytes() != b"old-first"
            or second.exists()
            or not (interrupt_root / LOCK_NAME).is_file()
            or len(interrupt_tx) != 1
        ):
            raise BuildError("interrupt-after-replace rollback/residue contract failed")
        journal = json.loads((interrupt_tx[0] / "journal.json").read_text(encoding="ascii"))
        if journal.get("status") != "ROLLED_BACK_AFTER_FAILURE" or journal.get("attempted") != ["first.out"]:
            raise BuildError("interrupt recovery journal contract failed")

        held_root = test_root / "held"
        held_root.mkdir()
        held_target = held_root / "only.out"
        replacement = held_root / "replacement.lock"
        replacement.write_bytes(b"foreign replacement")
        second_actor = {"unlink_blocked": False, "replace_blocked": False}

        def held_hook(event, _target, lock, _token) -> None:
            if event != "after_lock":
                return
            try:
                os.unlink(lock)
            except OSError:
                second_actor["unlink_blocked"] = True
            else:
                raise BuildError("second actor unlinked held publication lock")
            try:
                os.replace(replacement, lock)
            except OSError:
                second_actor["replace_blocked"] = True
            else:
                raise BuildError("second actor replaced held publication lock")

        publish_transaction(
            held_root, {held_target: b"new"}, lambda: None, held_hook
        )
        if (
            held_target.read_bytes() != b"new"
            or not all(second_actor.values())
            or (held_root / LOCK_NAME).exists()
            or replacement.read_bytes() != b"foreign replacement"
            or publication_residue(held_root)
        ):
            raise BuildError("held-handle atomic release contract failed")

        foreign_root = test_root / "preexisting_foreign"
        foreign_root.mkdir()
        foreign_target = foreign_root / "only.out"
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
        success_target = success_root / "only.out"
        publish_transaction(success_root, {success_target: b"new"}, lambda: None)
        if success_target.read_bytes() != b"new" or publication_residue(success_root):
            raise BuildError("successful publication cleanup contract failed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--audit-only", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test-publication", action="store_true")
    args = parser.parse_args()
    if args.self_test_publication:
        publication_self_test()
        print("publication self-test PASS: interrupt rollback, held lock, foreign preexistence, success cleanup")
        return 0
    residue_before = publication_residue(OUT)
    if residue_before:
        raise BuildError("stale V4 publication recovery state: " + ",".join(residue_before))
    outputs, measured, groups, inherited = build()
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
        "PASS V4 P1=255/365 OPEN=110 overall=334/519 "
        f"A2={measured['rows']} UNKNOWN={measured['unknown']} A3={measured['a3']} "
        f"inherited_status_refs={inherited} groups={dict(groups)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        raise SystemExit(f"ERROR: {exc}")
