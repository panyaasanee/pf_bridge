#!/usr/bin/env python3
"""Replay A5 against the V4 logical embedded-child schema.

The stored A2 view remains reference based.  For validation only, this module
expands the four exact embedded-child references in memory, then replays the
content-deduplicated capture corpus.  It publishes only the V4 Markdown report;
when the aggregate TSV is unchanged, the byte-identical V2 TSV remains the one
canonical table.
"""

from __future__ import annotations

import argparse
import ctypes
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from ctypes import wintypes
from dataclasses import replace
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pf_validate_v3_effective_capture as v3


v2 = v3.v2

V3_MODULE_SHA256 = "3d145407c9a6e4236eefe829c9fb9eb0757bf53cce9ac9cb136f201f594a360b"
PINNED_COMPONENTS = {
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
}

DAILY_A2 = "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv"
COMPOSITION_A2 = "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv"
CANONICAL_TSV = "PF_V2_FIELD_VALIDATION.tsv"
FORBIDDEN_TSV = "PF_V4_FIELD_VALIDATION.tsv"
OUTPUT_MD = "PF_V4_FIELD_VALIDATION.md"
PUBLISH_LOCK = ".PF_V4_FIELD_VALIDATION_PUBLISH.lock"
CANONICAL_TSV_SHA256 = "10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806"
EXPECTED_OUTPUT_MD_SHA256 = "4345387b12cbbe048ee3c3a78c43c15d22f680a5082a25bb8de30359aee75ef7"

EXPECTED_STORED_ROWS = 8657
EXPECTED_STORED_UNKNOWN = 3963
EXPECTED_LOGICAL_ROWS = 8721
EXPECTED_LOGICAL_UNKNOWN = 3999
EXPECTED_STORED_A3_NUMERIC = 4081
EXPECTED_PLAN_CENSUS = {
    "APPLICABLE": 624,
    "SCHEMA_NOT_APPLIED": 46,
    "STATIC_OPEN": 368,
}
EXPECTED_ITEM_VARIANTS = {
    "VTABLE_0x00F0EBB0": 26,
    "VTABLE_0x00F4A188": 30,
}

DAILY_REQUIRED = {
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "direction(W/R)", "old_order", "old_tag",
    "old_field_offset", "old_len", "source",
}
COMPOSITION_REQUIRED = DAILY_REQUIRED | {
    "new_wire_order", "new_tag", "new_field_offset", "new_len",
    "new_gate_condition", "child_message", "child_receiver", "child_vtable_va",
    "child_slot", "child_serializer_va", "child_effective_rows",
    "child_effective_unknown_rows",
}

TOP_OBJECT_OFFSET_RE = re.compile(r"^\+0x([0-9A-Fa-f]+)$")
INNER_OBJECT_OFFSET_RE = re.compile(r"OBJ\+0x([0-9A-Fa-f]+)")


class V4Error(v2.ValidationError):
    pass


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strict_read_tsv(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    try:
        text = path.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        raise V4Error(f"cannot read strict TSV: {path.name}") from exc
    if "\x00" in text:
        raise V4Error(f"NUL in TSV: {path.name}")
    reader = csv.reader(io.StringIO(text, newline=""), delimiter="\t", strict=True)
    try:
        raw_rows = list(reader)
    except csv.Error as exc:
        raise V4Error(f"malformed TSV quoting: {path.name}") from exc
    if not raw_rows or not raw_rows[0] or any(not value for value in raw_rows[0]):
        raise V4Error(f"missing/blank TSV header: {path.name}")
    headers = raw_rows[0]
    if len(headers) != len(set(headers)):
        raise V4Error(f"duplicate TSV header: {path.name}")
    result: list[tuple[int, dict[str, str]]] = []
    for line, values in enumerate(raw_rows[1:], start=2):
        if len(values) != len(headers):
            raise V4Error(
                f"TSV cell count mismatch: {path.name}:{line}: "
                f"{len(values)} != {len(headers)}"
            )
        result.append((line, dict(zip(headers, values, strict=True))))
    return headers, result


def verify_pinned_components(external: Path) -> dict[str, str]:
    measured: dict[str, str] = {}
    if sha256_path(Path(v3.__file__).resolve()) != V3_MODULE_SHA256:
        raise V4Error("frozen V3 validator module changed")
    for name, expected in PINNED_COMPONENTS.items():
        path = external / name
        if not path.is_file():
            raise V4Error(f"missing pinned V4 component: {name}")
        actual = sha256_path(path)
        if actual != expected:
            raise V4Error(
                f"pinned V4 component changed: {name}: {actual} != {expected}"
            )
        measured[name] = actual
    return measured


def run_component_checks(external: Path, image: Path) -> None:
    commands = (
        (
            "pf_build_daily_activity_closure.py",
            ["--check", "--external", str(external)],
            "PASS DailyActivityState:",
        ),
        (
            "pf_build_embedded_child_composition.py",
            ["--check", "--external", str(external), "--image", str(image)],
            "PASS embedded-child composition mode=check",
        ),
        (
            "pf_build_static_type_info_classmap.py",
            ["--check", "--image", str(image)],
            "mode=check",
        ),
    )
    for name, arguments, marker in commands:
        result = subprocess.run(
            [sys.executable, "-B", str(external / name), *arguments],
            cwd=external,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=300,
            check=False,
        )
        try:
            output = result.stdout.decode("ascii", errors="strict")
        except UnicodeDecodeError as exc:
            raise V4Error(f"non-ASCII component-check output: {name}") from exc
        if result.returncode or marker not in output:
            tail = " | ".join(output.splitlines()[-4:])
            raise V4Error(
                f"component --check failed: {name}: rc={result.returncode}: {tail}"
            )


def unknown_field(field: v2.EffectiveField) -> bool:
    return field.tag == "UNKNOWN" or "UNKNOWN(" in field.field_offset


def total_rows(effective: Mapping[tuple[str, str], Sequence[v2.EffectiveField]]) -> int:
    return sum(len(fields) for fields in effective.values())


def total_unknown(effective: Mapping[tuple[str, str], Sequence[v2.EffectiveField]]) -> int:
    return sum(unknown_field(field) for fields in effective.values() for field in fields)


def prior_targets_and_keys(external: Path) -> tuple[set[tuple[str, str, str]], set[str]]:
    targets = v3.prior_a2_targets(external)
    keys = v3.prior_a2_provenance_keys(external)
    for name in v3.NEW_A2_NAMES:
        headers, rows = strict_read_tsv(external / name)
        if not {"base_file", "base_line", "base_row_key", "delta_key"}.issubset(headers):
            raise V4Error(f"prior V3 TSV schema drift: {name}")
        for _line, row in rows:
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            if target in targets or row["delta_key"] in keys:
                raise V4Error(f"prior V3 duplicate target/key: {name}")
            targets.add(target)
            keys.add(row["delta_key"])
    return targets, keys


def exact_source_row(
    external: Path, cache: dict[str, tuple[list[str], dict[int, dict[str, str]]]],
    row: Mapping[str, str], label: str,
) -> dict[str, str]:
    name = row["base_file"]
    if name not in {"PF_SERIALIZER_FIELDS.tsv", "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"}:
        raise V4Error(f"unsupported V4 base file: {label}:{name}")
    if name not in cache:
        headers, rows = strict_read_tsv(external / name)
        cache[name] = (headers, {line: value for line, value in rows})
    headers, rows_by_line = cache[name]
    try:
        line = int(row["base_line"])
    except ValueError as exc:
        raise V4Error(f"non-numeric base line: {label}") from exc
    source = rows_by_line.get(line)
    if source is None:
        raise V4Error(f"base line absent: {label}:{name}:{line}")
    if v2.canonical_row_key(headers, source) != row["base_row_key"]:
        raise V4Error(f"base target drift: {label}:{name}:{line}")
    return source


def old_contract(field: v2.EffectiveField, row: Mapping[str, str]) -> None:
    declared = (
        row["old_order"], row["old_tag"], row["old_field_offset"], row["old_len"]
    )
    actual = (
        field.wire_order, field.tag, field.field_offset, field.length
    )
    if declared != actual:
        raise V4Error(f"old-row contract drift: {row['message']}:{row['direction(W/R)']}")


def apply_daily_and_composition(
    external: Path,
) -> tuple[
    list[dict[str, str]],
    dict[tuple[str, str], list[v2.EffectiveField]],
    dict[tuple[str, str, str], list[v2.EffectiveField]],
    dict[str, int],
    list[dict[str, str]],
    dict[str, int],
]:
    registry, effective, candidates, counts, _v3_per_file = v3.apply_v3_removals(external)
    prior_targets, prior_keys = prior_targets_and_keys(external)
    source_cache: dict[str, tuple[list[str], dict[int, dict[str, str]]]] = {}
    index: dict[tuple[str, str, str], tuple[tuple[str, str], v2.EffectiveField]] = {}
    for semantic_key, fields in effective.items():
        for field in fields:
            key = (semantic_key[0], semantic_key[1], field.evidence_key)
            if key in index:
                raise V4Error(f"duplicate effective evidence key: {key}")
            index[key] = (semantic_key, field)

    daily_headers, daily_numbered = strict_read_tsv(external / DAILY_A2)
    if not DAILY_REQUIRED.issubset(daily_headers):
        raise V4Error(f"Daily A2 missing columns: {sorted(DAILY_REQUIRED-set(daily_headers))}")
    daily_targets: set[tuple[str, str, str]] = set()
    daily_keys: set[str] = set()
    daily_directions: Counter[str] = Counter()
    for input_line, row in daily_numbered:
        label = f"{DAILY_A2}:{input_line}"
        if (
            row["source"] != "IMAGE"
            or row["action"] != "REMOVE_OVERLAY_NONWIRE_ROW"
            or row["base_file"] != "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
            or row["message"] != "DailyActivityState"
        ):
            raise V4Error(f"Daily action/source boundary changed: {label}")
        target = (row["base_file"], row["base_line"], row["base_row_key"])
        if target in prior_targets or target in daily_targets:
            raise V4Error(f"Daily duplicate/prior base target: {label}")
        if row["delta_key"] in prior_keys or row["delta_key"] in daily_keys:
            raise V4Error(f"Daily duplicate/prior provenance key: {label}")
        source = exact_source_row(external, source_cache, row, label)
        if not row["base_delta_key"] or source.get("delta_key") != row["base_delta_key"]:
            raise V4Error(f"Daily base-delta binding drift: {label}")
        lookup = (row["message"], row["direction(W/R)"], row["base_delta_key"])
        match = index.get(lookup)
        if match is None:
            raise V4Error(f"Daily target is not effective/unique: {label}")
        semantic_key, field = match
        old_contract(field, row)
        effective[semantic_key].remove(field)
        del index[lookup]
        daily_targets.add(target)
        daily_keys.add(row["delta_key"])
        daily_directions[row["direction(W/R)"]] += 1
    if daily_directions != Counter({"R": 6, "W": 6}):
        raise V4Error(f"Daily exact removal census changed: {dict(daily_directions)}")

    comp_headers, comp_numbered = strict_read_tsv(external / COMPOSITION_A2)
    if not COMPOSITION_REQUIRED.issubset(comp_headers):
        raise V4Error(
            f"composition A2 missing columns: {sorted(COMPOSITION_REQUIRED-set(comp_headers))}"
        )
    composition_targets: set[tuple[str, str, str]] = set()
    composition_keys: set[str] = set()
    changed_refs: set[tuple[str, str]] = set()
    action_counts: Counter[str] = Counter()
    reference_rows: list[dict[str, str]] = []
    for input_line, row in comp_numbered:
        label = f"{COMPOSITION_A2}:{input_line}"
        if row["source"] != "IMAGE" or row["base_file"] != "PF_SERIALIZER_FIELDS.tsv":
            raise V4Error(f"composition action/source boundary changed: {label}")
        if row["action"] not in {"CHANGED", "REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW"}:
            raise V4Error(f"composition copied/unsupported row: {label}")
        target = (row["base_file"], row["base_line"], row["base_row_key"])
        if target in prior_targets or target in daily_targets or target in composition_targets:
            raise V4Error(f"composition duplicate/prior base target: {label}")
        if (
            row["delta_key"] in prior_keys
            or row["delta_key"] in daily_keys
            or row["delta_key"] in composition_keys
        ):
            raise V4Error(f"composition duplicate/prior provenance key: {label}")
        source = exact_source_row(external, source_cache, row, label)
        if row["base_delta_key"] != "N/A":
            raise V4Error(f"composition V1 base-delta binding changed: {label}")
        lookup = (row["message"], row["direction(W/R)"], row["base_row_key"])
        match = index.get(lookup)
        if match is None:
            raise V4Error(f"composition target is not effective/unique: {label}")
        semantic_key, field = match
        old_contract(field, row)
        child_fields = effective.get((row["child_message"], row["direction(W/R)"]))
        if child_fields is None:
            raise V4Error(f"composition child absent: {label}")
        derived_child_rows = len(child_fields)
        derived_child_unknown = sum(unknown_field(value) for value in child_fields)
        if (
            int(row["child_effective_rows"]) != derived_child_rows
            or int(row["child_effective_unknown_rows"]) != derived_child_unknown
        ):
            raise V4Error(f"composition child census is not derived/current: {label}")
        effective[semantic_key].remove(field)
        del index[lookup]
        if row["action"] == "CHANGED":
            ref_key = semantic_key
            if ref_key in changed_refs:
                raise V4Error(f"duplicate embedded-child reference: {label}")
            if (
                row["new_tag"] != "STATIC_EMBEDDED_CHILD_REF"
                or row["new_field_offset"] != "this+0x18"
                or row["new_len"] != "N/A"
                or row["new_gate_condition"] != "DIRECTION_FORWARDED"
                or row["child_receiver"] != "this+0x18"
                or row["child_slot"] != "+0x34"
            ):
                raise V4Error(f"embedded-child reference contract drift: {label}")
            new_field = v2.EffectiveField(
                sequence=field.sequence,
                field_identity=(
                    f"BASE:{row['base_row_key']};DELTA:{row['delta_key']};"
                    f"ORDER:{row['old_order']}->WIRE:{row['new_wire_order']}"
                ),
                origin_order=field.origin_order,
                wire_order=row["new_wire_order"],
                tag=row["new_tag"],
                length=row["new_len"],
                field_offset=row["new_field_offset"],
                gate_condition=row["new_gate_condition"],
                origin_field_offset=field.origin_field_offset,
                origin_gate_condition=field.origin_gate_condition,
                provenance=COMPOSITION_A2,
                evidence_key=row["delta_key"],
            )
            effective[semantic_key].append(new_field)
            index[(semantic_key[0], semantic_key[1], new_field.evidence_key)] = (
                semantic_key, new_field
            )
            changed_refs.add(ref_key)
            reference_rows.append(dict(row))
        action_counts[row["action"]] += 1
        composition_targets.add(target)
        composition_keys.add(row["delta_key"])
    if action_counts != Counter({"CHANGED": 4, "REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW": 2}):
        raise V4Error(f"composition exact action census changed: {dict(action_counts)}")

    for fields in effective.values():
        fields.sort(key=lambda value: value.sequence)
    v2.validate_effective_tag_census(external, effective)
    stored_rows = total_rows(effective)
    stored_unknown = total_unknown(effective)
    if (stored_rows, stored_unknown) != (EXPECTED_STORED_ROWS, EXPECTED_STORED_UNKNOWN):
        raise V4Error(
            f"stored V4 census changed: rows={stored_rows} unknown={stored_unknown}"
        )
    numeric_physical = sum(
        bool(v2.NUMERIC_TAG_RE.fullmatch(field.tag))
        for fields in effective.values() for field in fields
    )
    if numeric_physical != EXPECTED_STORED_A3_NUMERIC:
        raise V4Error(f"stored physical A3 frequency changed: {numeric_physical}")

    counts = dict(counts)
    counts["generic_removed"] += len(daily_numbered) + action_counts["REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW"]
    counts["generic_changed"] += action_counts["CHANGED"]
    counts["slot_overlay_removed"] += len(daily_numbered)
    counts["slot_added_canonical"] -= len(daily_numbered)
    counts["effective_rows"] = stored_rows
    counts["v4_daily_removed"] = len(daily_numbered)
    counts["v4_composition_changed"] = action_counts["CHANGED"]
    counts["v4_composition_removed"] = action_counts["REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW"]
    details = {
        "daily_removed": len(daily_numbered),
        "composition_changed": action_counts["CHANGED"],
        "composition_removed": action_counts["REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW"],
        "stored_rows": stored_rows,
        "stored_unknown": stored_unknown,
        "stored_numeric": numeric_physical,
    }
    return registry, effective, candidates, counts, reference_rows, details


def translate_object_offset(value: str) -> str:
    top = TOP_OBJECT_OFFSET_RE.fullmatch(value)
    if top is not None:
        return f"OBJ+0x{int(top.group(1), 16) + 0x18:X}"
    return INNER_OBJECT_OFFSET_RE.sub(
        lambda match: f"OBJ+0x{int(match.group(1), 16) + 0x18:X}", value
    )


def expand_logical_references(
    stored: Mapping[tuple[str, str], list[v2.EffectiveField]],
    reference_rows: Sequence[Mapping[str, str]],
) -> tuple[dict[tuple[str, str], list[v2.EffectiveField]], list[dict[str, str]]]:
    logical = {key: list(fields) for key, fields in stored.items()}
    details: list[dict[str, str]] = []
    for row in reference_rows:
        key = (row["message"], row["direction(W/R)"])
        refs = [field for field in logical[key] if field.evidence_key == row["delta_key"]]
        if len(refs) != 1:
            raise V4Error(f"stored reference is not unique: {key}")
        ref = refs[0]
        children = list(stored[(row["child_message"], row["direction(W/R)"])])
        derived_unknown = sum(unknown_field(field) for field in children)
        target = row["child_serializer_va"]
        if not re.fullmatch(r"0x[0-9A-F]{8}", target):
            raise V4Error(f"non-canonical child target: {key}:{target}")
        replacement: list[v2.EffectiveField] = []
        marker_sequence = ref.sequence * 1000
        marker = v2.EffectiveField(
            sequence=marker_sequence,
            field_identity=f"COMPOSED:{row['delta_key']}:SUBCALL:{target}",
            origin_order=ref.origin_order,
            wire_order=ref.wire_order,
            tag=f"SUBCALL:{target}",
            length="N/A",
            field_offset="OBJ+0x18",
            gate_condition=(
                f"COMPOSED_CHILD_REF child={row['child_message']} receiver=OBJ+0x18 "
                f"vtable={row['child_vtable_va']} slot={row['child_slot']} "
                f"target={target} direction=FORWARDED"
            ),
            origin_field_offset=ref.origin_field_offset,
            origin_gate_condition=ref.origin_gate_condition,
            provenance=COMPOSITION_A2,
            evidence_key=row["delta_key"],
        )
        replacement.append(marker)
        for child_index, child in enumerate(children, start=1):
            evidence_key = hashlib.sha256(
                (row["delta_key"] + "\x1f" + child.evidence_key).encode("ascii")
            ).hexdigest()
            # Do not manufacture the target string used by subcall_is_flattened.
            # The child field keeps its native IMAGE proof text; the separate
            # child identity annotation contains no address and therefore cannot
            # make an unrelated schema look linked merely by relabeling it.
            child_gate = (
                f"{child.gate_condition} AND COMPOSED_PARENT_CHILD={row['child_message']} "
                "PARENT_RECEIVER=OBJ+0x18"
            )
            replacement.append(
                v2.EffectiveField(
                    sequence=marker_sequence + child_index,
                    field_identity=(
                        f"PARENT:{row['delta_key']};CHILD:{child.field_identity}"
                    ),
                    origin_order=child.origin_order,
                    wire_order=child.wire_order,
                    tag=child.tag,
                    length=child.length,
                    field_offset=translate_object_offset(child.field_offset),
                    gate_condition=child_gate,
                    origin_field_offset=translate_object_offset(child.origin_field_offset),
                    origin_gate_condition=child.origin_gate_condition,
                    provenance=f"{COMPOSITION_A2};CHILD={child.provenance}",
                    evidence_key=evidence_key,
                )
            )
        logical[key].remove(ref)
        logical[key].extend(replacement)
        logical[key].sort(key=lambda value: value.sequence)
        native_target_links = []
        for child in children:
            searchable = " ".join(
                (
                    child.field_offset,
                    child.origin_field_offset,
                    child.gate_condition,
                    child.origin_gate_condition,
                )
            )
            if target in searchable and not child.tag.startswith("SUBCALL:"):
                native_target_links.append(child.evidence_key)
        if not native_target_links:
            raise V4Error(f"child schema lacks native exact target provenance: {key}")
        if not v2.subcall_is_flattened(marker, logical[key]):
            raise V4Error(f"composition SUBCALL lacks exact target linkage: {key}")
        linked = [
            field for field in logical[key]
            if field.sequence > marker.sequence
            and target in " ".join(
                (
                    field.field_offset,
                    field.origin_field_offset,
                    field.gate_condition,
                    field.origin_gate_condition,
                )
            )
            and not field.tag.startswith("SUBCALL:")
        ]
        if {field.evidence_key for field in linked} != {
            hashlib.sha256(
                (row["delta_key"] + "\x1f" + evidence_key).encode("ascii")
            ).hexdigest()
            for evidence_key in native_target_links
        }:
            raise V4Error(f"composition native target provenance changed in expansion: {key}")
        details.append(
            {
                "parent": row["message"],
                "direction": row["direction(W/R)"],
                "child": row["child_message"],
                "target": target,
                "child_rows": str(len(children)),
                "child_unknown": str(derived_unknown),
                "native_target_links": str(len(native_target_links)),
            }
        )
    if len(details) != 4:
        raise V4Error(f"logical reference census changed: {len(details)}")
    for key, fields in logical.items():
        evidence = [field.evidence_key for field in fields]
        if len(evidence) != len(set(evidence)):
            raise V4Error(f"duplicate logical evidence reference: {key}")
    logical_rows = total_rows(logical)
    logical_unknown = total_unknown(logical)
    if (logical_rows, logical_unknown) != (EXPECTED_LOGICAL_ROWS, EXPECTED_LOGICAL_UNKNOWN):
        raise V4Error(
            f"logical V4 census changed: rows={logical_rows} unknown={logical_unknown}"
        )
    return logical, details


def verify_classmap_boundary(external: Path) -> None:
    headers, numbered = strict_read_tsv(external / "PF_STATIC_TYPE_INFO_CLASSMAP.tsv")
    required = {"registry_name", "class_name", "identity_kind", "vtable_va", "source"}
    if not required.issubset(headers) or len(numbered) != 4:
        raise V4Error("static type-info classmap schema/census changed")
    rows = [row for _line, row in numbered]
    if Counter(row["source"] for row in rows) != Counter({"IMAGE": 4}):
        raise V4Error("classmap crossed the IMAGE evidence boundary")
    if Counter(row["registry_name"] for row in rows) != Counter({"ItemAttr": 2, "VitalData": 2}):
        raise V4Error("classmap registry identity set changed")
    if Counter(row["identity_kind"] for row in rows) != Counter(
        {"EXACT_REGISTRY_CLASS": 2, "POLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER": 2}
    ):
        raise V4Error("classmap identity-kind boundary changed")


def verify_item_variants(candidates: Mapping[tuple[str, str, str], Sequence[v2.EffectiveField]]) -> None:
    measured: Counter[str] = Counter()
    for (name, _direction, variant), fields in candidates.items():
        if name == "ItemAttr":
            measured[variant] += len(fields)
    if dict(measured) != EXPECTED_ITEM_VARIANTS:
        raise V4Error(f"ItemAttr candidate schemas changed/merged: {dict(measured)}")


def touched_keys(
    external: Path, reference_rows: Sequence[Mapping[str, str]]
) -> set[tuple[str, str]]:
    _headers, daily = strict_read_tsv(external / DAILY_A2)
    result = {(row["message"], row["direction(W/R)"]) for _line, row in daily}
    for row in reference_rows:
        result.add((row["message"], row["direction(W/R)"]))
        result.add((row["child_message"], row["direction(W/R)"]))
    return result


def measure_zero_observations(
    keys: Iterable[tuple[str, str]],
    canonical: Mapping[tuple[str, str], v2.MessageAggregate],
    duplicates: Mapping[tuple[str, str], v2.MessageAggregate],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for message, direction in sorted(keys):
        key = (message, direction)
        canonical_value = canonical.get(key, v2.MessageAggregate())
        duplicate_value = duplicates.get(key, v2.MessageAggregate())
        if canonical_value.observed_instances or duplicate_value.observed_instances:
            raise V4Error(
                "V4-touched message unexpectedly observed in captures: "
                f"{key}:canonical={canonical_value.observed_instances}:"
                f"duplicates={duplicate_value.observed_instances}"
            )
        rows.append(
            {
                "message": message,
                "direction": direction,
                "observed_frames": str(len(canonical_value.observed_frames)),
                "observed_instances": str(canonical_value.observed_instances),
                "reason": (
                    "NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_"
                    "CANONICAL_SHA256_CONTENT_DEDUP_REPLAY"
                ),
            }
        )
    return rows


def report_text(
    values: Mapping[str, int],
    mismatch_points: Mapping[tuple[str, str, str, str], int],
    plan_census: Mapping[str, int],
    details: Mapping[str, int],
    expansion_details: Sequence[Mapping[str, str]],
    logical_numeric: int,
    all_input_count: int,
    canonical_count: int,
    corpus_digest: str,
    component_hashes: Mapping[str, str],
    zero_observation_rows: Sequence[Mapping[str, str]],
) -> str:
    mismatch_locations = {
        (message, direction, identity)
        for message, direction, identity, _reason in mismatch_points
    }
    lines = [
        "# RED: A5 V4 retains static/capture mismatches",
        "",
        f"[MEASURED][CAPTURE] The canonical content-deduplicated replay retains {values['mismatch']} mismatch instances at {len(mismatch_locations)} field locations and {len(mismatch_points)} field+reason points. IMAGE rows were not edited to fit CAPTURE observations.",
        "",
        "| evidence | message | dir | declared field identity | reason | instances |",
        "|---|---|:---:|---|---|---:|",
    ]
    for (message, direction, identity, reason), count in sorted(mismatch_points.items()):
        lines.append(
            f"| MEASURED/CAPTURE | `{message}` | {direction} | `{identity}` | `{reason}` | {count} |"
        )
    lines.extend(
        [
            "",
            "## Replay result",
            "",
            f"- [MEASURED][CAPTURE] Full parser replay against the pinned corpus digest and exact logical-plan census measured parse success={values['parse_success']}; static-open={values['static_open']}; schema-not-applied={values['schema_not_applied']}; mismatch={values['mismatch']}; observed message/direction rows={values['observed_rows']}.",
            f"- [MEASURED][CAPTURE] Full-file SHA-256 inventory/canonical-path control measured {all_input_count} paths; canonical unique contents={canonical_count}; exact-content duplicate paths rejected={all_input_count-canonical_count}; canonical corpus digest=`{corpus_digest}`.",
            f"- [MEASURED][CAPTURE] Fresh aggregate lookups after canonical plus duplicate-path replay measured zero observations for all {len(zero_observation_rows)} V4-touched message/direction keys.",
            "- [MEASURED][CAPTURE] Exact mismatch-point equality against the frozen V3 control measured only TeleportVital R STRING_TAG, TeleportVital W TAG, and TradeCmdVital W TAG/TRUNCATED_TAG; no point was hidden or renumbered.",
            "",
            "| evidence | message | dir | observed frames | observed instances | validator-derived zero-observation reason |",
            "|---|---|:---:|---:|---:|---|",
        ]
    )
    for item in zero_observation_rows:
        lines.append(
            f"| MEASURED/CAPTURE | `{item['message']}` | {item['direction']} | {item['observed_frames']} | {item['observed_instances']} | `{item['reason']}` |"
        )
    lines.extend(
        [
            "",
            "[MEASURED][CAPTURE] Scope control: zero observation means the validator recorded no reached outer or nested registry ID for that message+direction in the canonical SHA-256 content-deduplicated replay. It does not prove absence from other runtime sessions or from bytes beyond an earlier unresolved parse boundary.",
            "",
            "## IMAGE schema views",
            "",
            f"- [MEASURED][IMAGE] Strict base-key/action replay over the pinned V3 effective view measured stored/reference A2 rows={details['stored_rows']}; UNKNOWN rows={details['stored_unknown']}; Daily removals={details['daily_removed']}; composition references changed={details['composition_changed']}; directionally impossible rows removed={details['composition_removed']}.",
            f"- [MEASURED][IMAGE] In-memory expansion with exact parent delta, child identity, serializer-target, and native-target-text controls measured validation rows={EXPECTED_LOGICAL_ROWS}; UNKNOWN rows={EXPECTED_LOGICAL_UNKNOWN}. No expanded child row is written to A2.",
            f"- [MEASURED][IMAGE] The schema planner over that controlled in-memory view measured APPLICABLE={plan_census['APPLICABLE']}; STATIC_OPEN={plan_census['STATIC_OPEN']}; SCHEMA_NOT_APPLIED={plan_census['SCHEMA_NOT_APPLIED']}.",
            f"- [MEASURED][IMAGE] Numeric-tag full-match census measured stored physical A3 frequency={details['stored_numeric']} and expanded validation-only frequency={logical_numeric}; the expanded value is not written to A3.",
            "- [MEASURED][IMAGE] Strict classmap source/schema/hash controls measured IMAGE identity only; exact per-variant field counts keep ItemAttr separate (VTABLE_0x00F0EBB0=26; VTABLE_0x00F4A188=30), and plan equality shows VitalData identity activates no A5 schema.",
            "",
            "| evidence | parent | dir | child | exact serializer target | measured child rows | measured child UNKNOWN | native target links |",
            "|---|---|:---:|---|---:|---:|---:|---:|",
        ]
    )
    for item in sorted(expansion_details, key=lambda value: (value["parent"], value["direction"])):
        lines.append(
            f"| MEASURED/IMAGE | `{item['parent']}` | {item['direction']} | `{item['child']}` | `{item['target']}` | {item['child_rows']} | {item['child_unknown']} | {item['native_target_links']} |"
        )
    lines.extend(
        [
            "",
            "## Duplicate and evidence controls",
            "",
            f"- [MEASURED][CAPTURE] UTF-8 byte-equality plus SHA-256 control measured the generated aggregate identical to `{CANONICAL_TSV}` SHA-256 `{CANONICAL_TSV_SHA256}`; existence control measured no `{FORBIDDEN_TSV}`, so V2 remains canonical.",
            "- [MEASURED][IMAGE] Strict action/source/base-target checks measured only exact CHANGED/removal actions in Daily and composition inputs; row-count and key controls measured zero copied child rows.",
            "- [MEASURED][IMAGE] Pinned component `--check` exit/marker controls passed for Daily, embedded-child composition, and static type-info classmap; before/after SHA-256 control measured the client image unchanged.",
            "- [MEASURED][IMAGE+CAPTURE] Strict source-column and independent-plan/aggregate controls keep IMAGE structure separate from CAPTURE observations; source-census checks measured no DUMP or DATA identity in these rows.",
            "- [MEASURED][CAPTURE] Raw-byte regex plus report-schema control permits counts, names, identities, addresses, and SHA-256 only; it measured no payload, field value, capture path, or hexdump in this output.",
            "",
            "## Pinned V4 components",
            "",
        ]
    )
    for name in sorted(component_hashes):
        lines.append(f"- [MEASURED][IMAGE] `{name}` SHA-256 `{component_hashes[name]}`.")
    lines.extend(
        [
            f"- [MEASURED][IMAGE] `GameClient.local.bin` size={v2.EXPECTED_IMAGE_SIZE}; SHA-256 `{v2.EXPECTED_IMAGE_SHA256}`.",
            f"- [MEASURED][IMAGE] frozen V3 validator SHA-256 `{V3_MODULE_SHA256}`.",
            "",
            "## Reproduction",
            "",
            "[PROPOSED][LOCAL] Run `py -3 -B pf_validate_v4_effective_capture.py --check` for integrity replay. Run the same command with `--fail-on-mismatch` for the deliberately red conformance gate.",
            "",
        ]
    )
    text = "\n".join(lines)
    if v2.RAW_BYTE_RUN_RE.search(text):
        raise V4Error("raw capture-byte report guard fired")
    return text


class FileDispositionInfo(ctypes.Structure):
    _fields_ = [("DeleteFile", ctypes.c_ubyte)]


def windows_kernel32():
    if os.name != "nt":
        raise V4Error("handle-owned publication lock requires Windows")
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
    kernel32.GetFileSizeEx.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_longlong),
    )
    kernel32.GetFileSizeEx.restype = wintypes.BOOL
    kernel32.SetFileInformationByHandle.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
    )
    kernel32.SetFileInformationByHandle.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


def acquire_publish_lock(parent: Path) -> tuple[Path, bytes, int]:
    lock = parent / PUBLISH_LOCK
    token = os.urandom(24).hex().encode("ascii")
    kernel32 = windows_kernel32()
    generic_read = 0x80000000
    generic_write = 0x40000000
    delete_access = 0x00010000
    file_share_read = 0x00000001
    create_new = 1
    file_attribute_normal = 0x00000080
    invalid_handle = ctypes.c_void_p(-1).value
    handle = kernel32.CreateFileW(
        str(lock),
        generic_read | generic_write | delete_access,
        file_share_read,
        None,
        create_new,
        file_attribute_normal,
        None,
    )
    if handle == invalid_handle:
        error = ctypes.get_last_error()
        if error in {80, 183}:
            raise V4Error(
                f"publish lock already exists; inspect it and do not clear it automatically: {PUBLISH_LOCK}"
            )
        raise V4Error(f"CreateFileW publish-lock failure: winerror={error}")
    try:
        written = wintypes.DWORD(0)
        buffer = ctypes.create_string_buffer(token)
        if not kernel32.WriteFile(
            handle, buffer, len(token), ctypes.byref(written), None
        ) or written.value != len(token):
            raise V4Error(
                f"WriteFile publish-lock failure: winerror={ctypes.get_last_error()}"
            )
        if not kernel32.FlushFileBuffers(handle):
            raise V4Error(
                f"FlushFileBuffers publish-lock failure: winerror={ctypes.get_last_error()}"
            )
        measured_size = ctypes.c_longlong(0)
        if not kernel32.GetFileSizeEx(handle, ctypes.byref(measured_size)):
            raise V4Error(
                f"GetFileSizeEx publish-lock failure: winerror={ctypes.get_last_error()}"
            )
        if measured_size.value != len(token):
            raise V4Error("publish-lock size read-back mismatch")
    except BaseException:
        disposition = FileDispositionInfo(1)
        kernel32.SetFileInformationByHandle(
            handle, 4, ctypes.byref(disposition), ctypes.sizeof(disposition)
        )
        kernel32.CloseHandle(handle)
        raise
    return lock, token, int(handle)


def release_publish_lock(lock: Path, token: bytes, handle: int) -> None:
    del token  # Diagnostic bytes are not pathname-deletion authority.
    kernel32 = windows_kernel32()
    disposition = FileDispositionInfo(1)
    if not kernel32.SetFileInformationByHandle(
        handle, 4, ctypes.byref(disposition), ctypes.sizeof(disposition)
    ):
        # Retain the handle and pathname as fail-closed recovery state.
        raise V4Error(
            "handle-owned publish-lock disposition failed; lock retained: "
            f"winerror={ctypes.get_last_error()}"
        )
    if not kernel32.CloseHandle(handle):
        raise V4Error(
            "handle-owned publish-lock close failed: "
            f"winerror={ctypes.get_last_error()}"
        )
    # Never unlink here. If a second actor created a new path after our owned
    # handle closed, it is foreign state and must remain untouched.
    if lock.exists():
        raise V4Error("publish-lock pathname remains or was replaced; foreign state retained")


def cleanup_paths(paths: Sequence[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except BaseException as exc:
            errors.append(f"{path.name}:{type(exc).__name__}")
    return errors


def atomic_publish(
    destination: Path,
    text: str,
    *,
    _after_replace_hook=None,
) -> None:
    lock, token, lock_handle = acquire_publish_lock(destination.parent)
    original: bytes | None = None
    temp: Path | None = None
    backup: Path | None = None
    published = False
    recovery_required = False
    try:
        original = destination.read_bytes() if destination.exists() else None
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
        )
        temp = Path(temp_name)
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        if destination.exists():
            backup_fd, backup_name = tempfile.mkstemp(
                prefix=f".{destination.name}.", suffix=".rollback", dir=destination.parent
            )
            os.close(backup_fd)
            backup = Path(backup_name)
            shutil.copyfile(destination, backup)
            if backup.read_bytes() != original:
                raise V4Error("rollback-backup read-back mismatch")
        # Journal the destination as possibly changed before os.replace.  This
        # closes the BaseException window after the filesystem operation but
        # before Python regains control.
        published = True
        os.replace(temp, destination)
        if _after_replace_hook is not None:
            _after_replace_hook()
        if destination.read_bytes() != text.encode("utf-8"):
            raise V4Error("post-publish read-back mismatch")
    except BaseException as failure:
        if published:
            try:
                if backup is None:
                    destination.unlink(missing_ok=True)
                else:
                    # Restore from a copy so the sole verified backup remains
                    # available if restore/read-back itself fails.
                    shutil.copyfile(backup, destination)
                if original is None:
                    if destination.exists():
                        raise V4Error("rollback failed to remove new output")
                elif destination.read_bytes() != original:
                    raise V4Error("rollback read-back mismatch")
            except BaseException as rollback_error:
                recovery_required = True
                raise V4Error("publication failed and rollback is incomplete") from rollback_error
        cleanup_errors = cleanup_paths(
            [path for path in (temp, backup) if path is not None]
        )
        if cleanup_errors:
            recovery_required = True
            raise V4Error(
                "publication rolled back; recovery cleanup incomplete: "
                + "; ".join(cleanup_errors)
            ) from failure
        raise failure
    else:
        cleanup_errors = cleanup_paths(
            [path for path in (temp, backup) if path is not None]
        )
        if cleanup_errors:
            recovery_required = True
            raise V4Error(
                "output committed and verified; recovery cleanup incomplete: "
                + "; ".join(cleanup_errors)
            )
    finally:
        # A failed rollback/cleanup is explicit recovery state.  Keep the owned
        # lock and every remaining artifact; never erase a foreign/stale lock.
        if not recovery_required:
            release_publish_lock(lock, token, lock_handle)


def validate_atomic_publish_controls() -> None:
    class InjectedInterrupt(BaseException):
        pass

    def interrupt_after_replace() -> None:
        raise InjectedInterrupt("injected after replace")

    with tempfile.TemporaryDirectory(prefix="pf_v4_lock_selftest_") as raw:
        root = Path(raw)
        challenger = root / "challenger.lock"
        challenger.write_bytes(b"foreign")
        lock, token, handle = acquire_publish_lock(root)
        try:
            try:
                acquire_publish_lock(root)
            except V4Error as exc:
                if "already exists" not in str(exc):
                    raise V4Error("second-publisher lock self-test failed closed incorrectly") from exc
            else:
                raise V4Error("second publisher acquired a held lock")
            try:
                lock.unlink()
            except OSError:
                pass
            else:
                raise V4Error("held lock was unlinkable by pathname")
            try:
                os.replace(challenger, lock)
            except OSError:
                pass
            else:
                raise V4Error("held lock was replaceable by a foreign pathname")
            if not challenger.is_file() or challenger.read_bytes() != b"foreign":
                raise V4Error("foreign lock candidate changed during ownership test")
        finally:
            release_publish_lock(lock, token, handle)
        if lock.exists():
            raise V4Error("handle-owned lock release left the owned pathname")
        if challenger.read_bytes() != b"foreign":
            raise V4Error("handle-owned release affected a foreign inode")

    for preexisting in (False, True):
        with tempfile.TemporaryDirectory(prefix="pf_v4_publish_selftest_") as raw:
            root = Path(raw)
            target = root / "report.md"
            if preexisting:
                target.write_bytes(b"before")
            try:
                atomic_publish(
                    target,
                    "after",
                    _after_replace_hook=interrupt_after_replace,
                )
            except InjectedInterrupt:
                pass
            else:
                raise V4Error("atomic publication interrupt self-test did not fire")
            if preexisting:
                if target.read_bytes() != b"before":
                    raise V4Error("interrupt self-test failed to restore prior output")
            elif target.exists():
                raise V4Error("interrupt self-test failed to remove new output")
            residue = [path.name for path in root.iterdir() if path.name != "report.md"]
            if residue:
                raise V4Error(f"interrupt self-test left transaction residue: {residue}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--game-client", type=Path,
        default=Path(__file__).resolve().parents[2] / "GameClient",
    )
    parser.add_argument(
        "--external", type=Path, default=Path(__file__).resolve().parent
    )
    parser.add_argument("--preview-unpinned", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--fail-on-mismatch", action="store_true")
    args = parser.parse_args()
    if args.preview_unpinned and args.check:
        raise V4Error("--preview-unpinned and --check are mutually exclusive")
    if args.fail_on_mismatch and not args.check:
        raise V4Error("--fail-on-mismatch requires --check")

    validate_atomic_publish_controls()

    external = args.external.resolve()
    game_client = args.game_client.resolve()
    image = game_client / "GameClient.local.bin"
    image_before = sha256_path(image)
    if image.stat().st_size != v2.EXPECTED_IMAGE_SIZE or image_before != v2.EXPECTED_IMAGE_SHA256:
        raise V4Error("pinned client image changed")
    old_hashes_before = v2.verify_pinned_inputs(external, False)
    v3_hashes_before = v3.verify_new_inputs(external, False)
    component_hashes_before = verify_pinned_components(external)
    run_component_checks(external, image)
    verify_classmap_boundary(external)

    registry, stored, candidates, overlay_counts, references, details = (
        apply_daily_and_composition(external)
    )
    verify_item_variants(candidates)
    logical, expansion_details = expand_logical_references(stored, references)
    logical_numeric = sum(
        bool(v2.NUMERIC_TAG_RE.fullmatch(field.tag))
        for fields in logical.values() for field in fields
    )
    id_to_name, plans = v2.build_schema_plans(registry, logical, candidates)
    plan_census = dict(Counter(plan.state for plan in plans.values()))
    if plan_census != EXPECTED_PLAN_CENSUS:
        raise V4Error(f"V4 logical schema-plan census changed: {plan_census}")
    v2.validate_parser_controls(plans)

    all_inputs, canonical_inputs, baseline_hashes, corpus_digest = v2.load_capture_inventory(
        game_client,
        external / "PF_INPUT_INVENTORY.tsv",
        external / "PF_CAPTURE_DELTA_20260830.inventory.tsv",
    )
    if corpus_digest != v2.EXPECTED_CORPUS_DIGEST:
        raise V4Error("canonical capture-corpus digest changed")
    baseline_inputs = [item for item in canonical_inputs if item.sha256 in baseline_hashes]
    new_inputs = [item for item in canonical_inputs if item.sha256 not in baseline_hashes]
    if len(baseline_inputs) != 1189 or len(new_inputs) != 320:
        raise V4Error("baseline/new canonical partition changed")
    baseline_aggregates, baseline_counts = v2.run_capture_validation(
        baseline_inputs, id_to_name, plans
    )
    new_aggregates, new_counts = v2.run_capture_validation(new_inputs, id_to_name, plans)
    canonical_paths = {item.relative_path.casefold() for item in canonical_inputs}
    duplicate_inputs = [
        item for item in all_inputs if item.relative_path.casefold() not in canonical_paths
    ]
    duplicate_aggregates, duplicate_counts = v2.run_capture_validation(
        duplicate_inputs, id_to_name, plans
    )
    aggregates = v2.merge_aggregates(baseline_aggregates, new_aggregates)
    counts = v2.merge_run_counts(baseline_counts, new_counts)
    v2.validate_ctrace_capture_boundary(aggregates)
    values = v2.outcome_counts(aggregates, counts)
    baseline_values = v2.outcome_counts(baseline_aggregates, baseline_counts)
    new_values = v2.outcome_counts(new_aggregates, new_counts)
    for prefix, subset in (("baseline", baseline_values), ("new", new_values)):
        for name in (
            "parse_success", "static_open", "schema_not_applied", "mismatch",
            "observed_rows", "pc_blocks", "decompressed_blocks",
        ):
            values[f"{prefix}_{name}"] = subset[name]
    duplicate_values = v2.outcome_counts(duplicate_aggregates, duplicate_counts)
    for name in (
        "parse_success", "static_open", "schema_not_applied", "mismatch",
        "observed_rows", "pc_blocks", "decompressed_blocks",
    ):
        values[f"duplicate_rejected_{name}"] = duplicate_values[name]
    if values != v3.EXPECTED_RUN_COUNTS:
        raise V4Error(f"V4 capture run census changed: {values}")
    mismatch_points = v2.measured_mismatch_points(aggregates)
    if mismatch_points != v3.EXPECTED_MISMATCH_POINTS:
        raise V4Error(f"V4 mismatch-point census changed: {mismatch_points}")
    touched = touched_keys(external, references)
    zero_observation_rows = measure_zero_observations(
        touched,
        aggregates,
        duplicate_aggregates,
    )

    output_tsv, _discarded_v2_md = v2.build_outputs(
        aggregates, baseline_aggregates, new_aggregates, counts,
        duplicate_aggregates, duplicate_counts, plans, corpus_digest,
        all_inputs, canonical_inputs, old_hashes_before, overlay_counts,
    )
    v2.validate_output_mutations(
        output_tsv, aggregates, baseline_aggregates, new_aggregates, plans,
        corpus_digest,
    )
    if v2.sha256_text(output_tsv) != CANONICAL_TSV_SHA256:
        raise V4Error("V4 aggregate is not byte-identical to canonical V2 TSV")
    canonical_path = external / CANONICAL_TSV
    if canonical_path.read_bytes() != output_tsv.encode("utf-8"):
        raise V4Error("canonical V2 TSV bytes changed")
    if (external / FORBIDDEN_TSV).exists():
        raise V4Error(f"duplicated V4 aggregate TSV must not exist: {FORBIDDEN_TSV}")

    output_md = report_text(
        values, mismatch_points, plan_census, details, expansion_details,
        logical_numeric, len(all_inputs), len(canonical_inputs), corpus_digest,
        component_hashes_before, zero_observation_rows,
    )
    output_md_hash = v2.sha256_text(output_md)

    v2.verify_capture_snapshot(game_client, all_inputs)
    old_hashes_after = v2.verify_pinned_inputs(external, False)
    v3_hashes_after = v3.verify_new_inputs(external, False)
    component_hashes_after = verify_pinned_components(external)
    image_after = sha256_path(image)
    if (
        old_hashes_after != old_hashes_before
        or v3_hashes_after != v3_hashes_before
        or component_hashes_after != component_hashes_before
    ):
        raise V4Error("V4 inputs changed during validation")
    if image_after != image_before:
        raise V4Error("client image changed during V4 validation")

    if args.preview_unpinned:
        print("OUTPUT_MD_SHA256=" + output_md_hash)
        print("STORED=" + json.dumps(details, sort_keys=True))
        print(
            "LOGICAL="
            + json.dumps(
                {
                    "rows": total_rows(logical),
                    "unknown": total_unknown(logical),
                    "numeric": logical_numeric,
                    "plans": plan_census,
                },
                sort_keys=True,
            )
        )
        print("TOUCHED_ZERO_OBSERVATIONS=" + str(len(touched)))
        return 0
    if EXPECTED_OUTPUT_MD_SHA256 == "__PIN_AFTER_PREVIEW__":
        raise V4Error("V4 report hash is not pinned")
    if output_md_hash != EXPECTED_OUTPUT_MD_SHA256:
        raise V4Error(
            f"V4 report output hash changed: {output_md_hash} != {EXPECTED_OUTPUT_MD_SHA256}"
        )
    destination = external / OUTPUT_MD
    if args.check:
        if not destination.is_file() or destination.read_bytes() != output_md.encode("utf-8"):
            raise V4Error(f"published V4 output differs: {OUTPUT_MD}")
    else:
        atomic_publish(destination, output_md)
    if args.fail_on_mismatch and values["mismatch"]:
        raise V4Error(
            f"capture conformance failed: mismatch={values['mismatch']} "
            f"field_reason_points={len(mismatch_points)}"
        )
    print(
        "unique_contents=%d duplicate_paths=%d pass=%d static_open=%d "
        "schema_not_applied=%d mismatch=%d mismatch_points=%d"
        % (
            len(canonical_inputs), len(all_inputs) - len(canonical_inputs),
            values["parse_success"], values["static_open"],
            values["schema_not_applied"], values["mismatch"], len(mismatch_points),
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (V4Error, v2.ValidationError) as exc:
        raise SystemExit(f"ERROR: {exc}")
