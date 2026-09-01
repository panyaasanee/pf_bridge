#!/usr/bin/env python3
"""Build the chained, duplicate-safe V3 effective priority status.

V1 and every delivered overlay are immutable inputs.  This generator accepts
an update to a message only when the row names the exact currently-effective
base row (V1 or a previously applied delta).  It emits an OPEN-only derived
index, never another copy of A1/A2/A3 evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence

import pf_validate_v3_effective_capture as field_v3


OUT_DIR = Path(__file__).resolve().parent
BASE_PATH = OUT_DIR / "PF_PROTOCOL_PRIORITY.tsv"
V2_OVERLAYS = (
    OUT_DIR / "PF_POST_V1_PRIORITY_DELTA.tsv",
    OUT_DIR / "PF_PRIORITY_POOL_638690_DELTA.tsv",
    OUT_DIR / "PF_PRIORITY_POOL_661FA0_DELTA.tsv",
    OUT_DIR / "PF_PRIORITY_POOL_46F4D0_DELTA.tsv",
    OUT_DIR / "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv",
)
NEW_OVERLAY = OUT_DIR / "PF_PRIORITY_COMPILER_TARGET_6564_DELTA.tsv"
OVERLAYS = V2_OVERLAYS + (NEW_OVERLAY,)
A2_DELTAS = (
    OUT_DIR / "PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv",
    OUT_DIR / "PF_A2_TARGETS_6564E0_656C50_6FDB40_NONWIRE_DELTA.tsv",
    OUT_DIR / "PF_A2_TARGET_656690_NONWIRE_DELTA.tsv",
    OUT_DIR / "PF_A2_ITERATOR_HELPERS_NONWIRE_DELTA.tsv",
)
OPEN_PATH = OUT_DIR / "PF_V3_P1_OPEN.tsv"
REPORT_PATH = OUT_DIR / "PF_V3_EFFECTIVE_STATUS.md"
FIELD_VALIDATOR_PATH = OUT_DIR / "pf_validate_v3_effective_capture.py"
V2_FIELD_VALIDATOR_PATH = OUT_DIR / "pf_validate_v2_effective_capture.py"

PINNED_SHA256 = {
    BASE_PATH: "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55",
    V2_OVERLAYS[0]: "69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51",
    V2_OVERLAYS[1]: "cc585d983dd1ca155ea1cfcfc59116897b59d2ce2455dc96f1d4097e9d7afdd5",
    V2_OVERLAYS[2]: "3ba436e9b4876a1575a6d5544f49bb462896e2c6ae4191e085eacb56788ef880",
    V2_OVERLAYS[3]: "32a59e143052f827f8134bba890f28d63444c447943e6679521dade7ff7e9fd1",
    V2_OVERLAYS[4]: "00ef0f3cb632b40ba168ce79bbd656fc7a6936a55f3b3e185c6e63b32c39ec5d",
    NEW_OVERLAY: "390d974c153fa9e3498f0a8f2fa79a08848d88acde466061abfeecf3b9125d07",
    A2_DELTAS[0]: "f0797f48bfa9115d237bd6e2ebab50e69334c8a05303f66f57bf5ea9b05274dd",
    A2_DELTAS[1]: "8c0e3fdd5f0119b5b18eb77aae567f224f2ccebf82033b420e69cb52c542cf02",
    A2_DELTAS[2]: "f93ca7af682d393abc19628d6291c0f7dd0b04132011a9550b2e4175a1708799",
    A2_DELTAS[3]: "2916eeb565581e75cd1142920435087a19da3e15861427b4cd9f976854d25985",
    FIELD_VALIDATOR_PATH: "3d145407c9a6e4236eefe829c9fb9eb0757bf53cce9ac9cb136f201f594a360b",
    V2_FIELD_VALIDATOR_PATH: "7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9",
}

EXPECTED_BASE = {1: (241, 365), 2: (12, 16), 3: (84, 138)}
EXPECTED_V2 = {1: (250, 365), 2: (7, 16), 3: (68, 138)}
EXPECTED_FINAL = {1: (254, 365), 2: (8, 16), 3: (70, 138)}
EXPECTED_CLOSURE_MESSAGES = {
    "ActorLearnedPetsSkillData",
    "CBuffConditionState",
    "CollectionEffectData",
    "CollectionObj_UpdateCollectEffectVital",
    "NPCAppearAttr",
    "WineFormulaLearningAttr",
    "Winemaking_UpdateLearnedFormulaVital",
}
EXPECTED_A2_DELTA_ROWS = (48, 32, 4, 40)
EXPECTED_V3_REMOVALS = sum(EXPECTED_A2_DELTA_ROWS)
UNKNOWN_REASON_RE = re.compile(r"UNKNOWN\(([^()]*)\)")

OPEN_COLUMNS = (
    "status_key",
    "message",
    "priority",
    "matched_groups",
    "matched_keywords",
    "base_line",
    "base_registry_identity_status",
    "effective_registry_identity_status",
    "effective_registry_identity_missing",
    "base_serializer_status",
    "effective_serializer_status",
    "base_structural_status",
    "effective_structural_status",
    "primary_blocker_group",
    "effective_blocker",
    "applied_overlay_chain",
    "row_semantics",
    "source",
)


class StatusError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_row_key(fieldnames: Sequence[str], row: Mapping[str, str]) -> str:
    payload = json.dumps(
        [row[name] for name in fieldnames],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def read_tsv(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise StatusError(f"missing TSV header: {path.name}")
        fields = list(reader.fieldnames)
        rows = [(line, dict(row)) for line, row in enumerate(reader, start=2)]
    return fields, rows


def format_tsv(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=list(columns),
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def verify_pins(preview_unpinned: bool) -> dict[str, str]:
    measured: dict[str, str] = {}
    for path, expected in PINNED_SHA256.items():
        if not path.exists():
            raise StatusError(f"missing input: {path.name}")
        actual = sha256_path(path)
        measured[path.name] = actual
        if expected == "__PIN_AFTER_PREVIEW__":
            if not preview_unpinned:
                raise StatusError(f"unfrozen input pin: {path.name}")
        elif actual != expected:
            raise StatusError(
                f"pinned input changed: {path.name}: expected {expected}, got {actual}"
            )
    return measured


def status_counts(states: Mapping[str, Mapping[str, str]]) -> dict[int, tuple[int, int]]:
    result: dict[int, tuple[int, int]] = {}
    for priority in (1, 2, 3):
        selected = [row for row in states.values() if int(row["priority"]) == priority]
        result[priority] = (
            sum(row["structural_status"] == "CLOSED" for row in selected),
            len(selected),
        )
    return result


def primary_blocker_group(state: Mapping[str, str]) -> str:
    blocker = state["blocker"]
    if state["registry_identity_status"] != "KNOWN" or "registry " in blocker:
        return "REGISTRY_IDENTITY_UNRESOLVED"
    if "indirect_jump_not_proven_serializer" in blocker:
        return "INDIRECT_JUMP_TARGET_UNRESOLVED"
    dispatch_tokens = (
        "dynamic_vtable",
        "indirect_call_not_proven_serializer_slot",
        "subcall_direction_unresolved",
        "subcall_stream_provenance_unresolved",
        "ecx_plus_50_tail_target_and_alias_unproved",
    )
    if any(token in blocker for token in dispatch_tokens):
        return "DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED"
    graph_tokens = (
        "atomic_target",
        "mutable_",
        "locked_mutable_",
        "critical_section_pointer_alias_unproved",
    )
    if any(token in blocker for token in graph_tokens):
        return "OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED"
    return "CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED"


def effective_a2_blockers(fields: Sequence[object]) -> tuple[str, ...]:
    """Return canonical blocker reasons from the actually effective A2 rows."""
    reasons: set[str] = set()
    for field_value in fields:
        offset = str(getattr(field_value, "field_offset"))
        matches = UNKNOWN_REASON_RE.findall(offset)
        reasons.update(reason for reason in matches if reason)
        if getattr(field_value, "tag") == "UNKNOWN" and not matches:
            reasons.add("unknown_tag")
    return tuple(sorted(reasons))


def build(
    preview_unpinned: bool,
) -> tuple[list[dict[str, str]], str, dict[str, str]]:
    measured = verify_pins(preview_unpinned)
    v2_inputs_before = field_v3.v2.verify_pinned_inputs(OUT_DIR, False)
    measured.update(
        {f"V2_TRANSITIVE:{name}": digest for name, digest in v2_inputs_before.items()}
    )
    (
        _registry_rows,
        effective_a2,
        _candidate_schemas,
        v3_a2_counts,
        _per_file_removals,
    ) = field_v3.apply_v3_removals(OUT_DIR)
    if v3_a2_counts.get("v3_new_removed") != EXPECTED_V3_REMOVALS:
        raise StatusError(
            f"effective V3 A2 removal count changed: {v3_a2_counts.get('v3_new_removed')}"
        )

    a2_counts: dict[str, int] = {}
    a2_delta_keys: set[str] = set()
    a2_targets: set[tuple[str, str, str]] = set()
    touched_by: dict[str, set[str]] = {}
    for path, expected_rows in zip(A2_DELTAS, EXPECTED_A2_DELTA_ROWS):
        _fields, rows = read_tsv(path)
        if len(rows) != expected_rows:
            raise StatusError(f"A2 delta row count changed: {path.name}:{len(rows)}")
        for _line, row in rows:
            if row.get("source") != "IMAGE" or not row.get("action", "").startswith("REMOVE"):
                raise StatusError(f"non-removal/mixed-source A2 row: {path.name}")
            if row["delta_key"] in a2_delta_keys:
                raise StatusError(f"cross-file duplicate A2 delta_key: {path.name}")
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            if target in a2_targets:
                raise StatusError(f"cross-file duplicate A2 base target: {path.name}")
            a2_delta_keys.add(row["delta_key"])
            a2_targets.add(target)
            touched_by.setdefault(row["message"], set()).add(path.name)
        a2_counts[path.name] = len(rows)
    if len(a2_targets) != EXPECTED_V3_REMOVALS:
        raise StatusError(f"net-new A2 target count changed: {len(a2_targets)}")

    a2_residuals: dict[str, tuple[str, ...]] = {}
    a2_nonempty: dict[str, int] = {}
    for message in touched_by:
        fields = [
            field_value
            for direction in ("W", "R")
            for field_value in effective_a2[(message, direction)]
        ]
        a2_residuals[message] = effective_a2_blockers(fields)
        a2_nonempty[message] = sum(field_value.tag != "EMPTY" for field_value in fields)
    base_fields, base_rows = read_tsv(BASE_PATH)
    if len(base_rows) != 519:
        raise StatusError(f"base row count changed: {len(base_rows)}")
    if len({row["message"] for _line, row in base_rows}) != len(base_rows):
        raise StatusError("duplicate base message")
    if any(row["source"] != "IMAGE" for _line, row in base_rows):
        raise StatusError("base source is not IMAGE-only")

    states: dict[str, dict[str, str]] = {}
    base_keys: dict[str, str] = {}
    base_lines: dict[str, int] = {}
    for line, row in base_rows:
        message = row["message"]
        states[message] = {
            "message": message,
            "priority": row["priority"],
            "matched_groups": row["matched_groups"],
            "matched_keywords": row["matched_keywords"],
            "registry_identity_status": row["registry_identity_status"],
            "registry_identity_missing": row["registry_identity_missing"],
            "serializer_status": row["serializer_status"],
            "serializer_blockers": row["serializer_blockers"],
            "structural_status": row["structural_status"],
            "blocker": row["blocker"],
            "base_registry_identity_status": row["registry_identity_status"],
            "base_serializer_status": row["serializer_status"],
            "base_structural_status": row["structural_status"],
            "chain": ["BASE_ONLY"],
            "last_ref_file": BASE_PATH.name,
            "last_ref_line": str(line),
            "last_ref_key": canonical_row_key(base_fields, row),
            "last_delta_key": "N/A",
        }
        base_keys[message] = states[message]["last_ref_key"]
        base_lines[message] = line
    if status_counts(states) != EXPECTED_BASE:
        raise StatusError(f"base count mismatch: {status_counts(states)}")

    loaded: dict[str, tuple[list[str], list[tuple[int, dict[str, str]]]]] = {
        BASE_PATH.name: (base_fields, base_rows)
    }
    global_delta_keys: set[str] = set()
    global_reference_targets: set[tuple[str, str, str]] = set()
    overlay_counts: Counter[str] = Counter()
    v2_messages: set[str] = set()
    new_messages: set[str] = set()

    for overlay_index, path in enumerate(OVERLAYS):
        fields, rows = read_tsv(path)
        loaded[path.name] = (fields, rows)
        local_messages: set[str] = set()
        for line, row in rows:
            required = {
                "delta_key", "action", "base_file", "base_line",
                "base_row_key", "message", "priority",
                "old_serializer_status", "new_serializer_status",
                "old_structural_status", "new_structural_status",
                "old_blocker", "new_blocker", "source",
            }
            if path == NEW_OVERLAY:
                required.add("base_delta_key")
            missing = required - row.keys()
            if missing:
                raise StatusError(f"{path.name} missing columns: {sorted(missing)}")
            message = row["message"]
            if message not in states:
                raise StatusError(f"unknown overlay message: {path.name}: {message}")
            if row["action"] != "CHANGED" or row["source"] != "IMAGE":
                raise StatusError(f"invalid overlay action/source: {path.name}:{line}")
            if message in local_messages:
                raise StatusError(f"within-overlay duplicate message: {path.name}:{message}")
            if row["delta_key"] in global_delta_keys:
                raise StatusError(f"duplicate delta_key: {path.name}:{line}")
            local_messages.add(message)
            global_delta_keys.add(row["delta_key"])

            ref_file = row["base_file"]
            if ref_file not in loaded:
                raise StatusError(f"forward/unknown status base: {path.name}:{ref_file}")
            ref_fields, ref_rows = loaded[ref_file]
            ref_line = int(row["base_line"])
            ref_matches = [item for item in ref_rows if item[0] == ref_line]
            if len(ref_matches) != 1:
                raise StatusError(f"status base line not found: {path.name}:{ref_file}:{ref_line}")
            _line0, ref_row = ref_matches[0]
            ref_key = canonical_row_key(ref_fields, ref_row)
            if row["base_row_key"] != ref_key:
                raise StatusError(f"status base row key mismatch: {path.name}:{message}")
            if ref_row.get("message") != message:
                raise StatusError(f"status base message mismatch: {path.name}:{message}")
            if ref_file != BASE_PATH.name:
                if not row.get("base_delta_key"):
                    raise StatusError(f"missing chained base_delta_key: {path.name}:{message}")
                if row["base_delta_key"] != ref_row.get("delta_key"):
                    raise StatusError(f"chained base_delta_key mismatch: {path.name}:{message}")
            elif "base_delta_key" in row and row["base_delta_key"] != "N/A":
                raise StatusError(f"V1-based status row has non-N/A base_delta_key: {path.name}:{message}")

            target = (ref_file, row["base_line"], row["base_row_key"])
            if target in global_reference_targets:
                raise StatusError(f"duplicate status base target: {path.name}:{message}")
            global_reference_targets.add(target)

            state = states[message]
            if (
                state["last_ref_file"] != ref_file
                or state["last_ref_line"] != row["base_line"]
                or state["last_ref_key"] != row["base_row_key"]
            ):
                raise StatusError(
                    f"overlay does not chain from effective predecessor: {path.name}:{message}"
                )
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
                    raise StatusError(
                        f"old effective value mismatch: {path.name}:{message}:{row_name}"
                    )

            if path == NEW_OVERLAY:
                derived_closed = not a2_residuals[message] and a2_nonempty[message] > 0
                derived_status = "CLOSED" if derived_closed else "OPEN"
                derived_blocker = (
                    "N/A" if derived_closed else " | ".join(a2_residuals[message])
                )
                if (
                    row["new_serializer_status"] != derived_status
                    or row["new_structural_status"] != derived_status
                    or row["new_blocker"] != derived_blocker
                    or row.get("new_serializer_blockers", derived_blocker)
                    != derived_blocker
                ):
                    raise StatusError(
                        f"Priority row disagrees with recomputed effective A2: "
                        f"{message}: residual={a2_residuals[message]} "
                        f"nonempty={a2_nonempty[message]}"
                    )

            state["serializer_status"] = (
                derived_status if path == NEW_OVERLAY else row["new_serializer_status"]
            )
            state["structural_status"] = (
                derived_status if path == NEW_OVERLAY else row["new_structural_status"]
            )
            state["blocker"] = (
                derived_blocker if path == NEW_OVERLAY else row["new_blocker"]
            )
            if "new_registry_identity_status" in row:
                state["registry_identity_status"] = row["new_registry_identity_status"]
                state["registry_identity_missing"] = row["new_registry_identity_missing"]
            if "new_serializer_blockers" in row:
                state["serializer_blockers"] = (
                    derived_blocker
                    if path == NEW_OVERLAY
                    else row["new_serializer_blockers"]
                )
            state["chain"].append(path.name)
            state["last_ref_file"] = path.name
            state["last_ref_line"] = str(line)
            state["last_ref_key"] = canonical_row_key(fields, row)
            state["last_delta_key"] = row["delta_key"]
            overlay_counts[path.name] += 1
            if overlay_index < len(V2_OVERLAYS):
                v2_messages.add(message)
            else:
                new_messages.add(message)

        if overlay_index == len(V2_OVERLAYS) - 1:
            if status_counts(states) != EXPECTED_V2:
                raise StatusError(f"V2 reproduction mismatch: {status_counts(states)}")

    if sum(overlay_counts[path.name] for path in V2_OVERLAYS) != 52:
        raise StatusError(f"V2 overlay row count changed: {dict(overlay_counts)}")
    if overlay_counts[NEW_OVERLAY.name] != 7 or new_messages != EXPECTED_CLOSURE_MESSAGES:
        raise StatusError(
            f"new priority delta census changed: rows={overlay_counts[NEW_OVERLAY.name]} "
            f"messages={sorted(new_messages)}"
        )
    chained = v2_messages & new_messages
    if chained != {
        "ActorLearnedPetsSkillData", "CollectionEffectData",
        "NPCAppearAttr", "WineFormulaLearningAttr",
    }:
        raise StatusError(f"unexpected chained status messages: {sorted(chained)}")

    # Priority deltas are evidence-bearing status transitions.  Messages whose
    # A2 rows changed but remain OPEN do not need another evidence row; their
    # derived blocker metadata must nevertheless be rebuilt from the final A2,
    # otherwise an old blocker string can survive after its source row was removed.
    recomputed_open: set[str] = set()
    for message in sorted(touched_by):
        state = states[message]
        if state["registry_identity_status"] != "KNOWN":
            raise StatusError(
                f"V3 A2 touched unresolved registry identity; explicit composition required: {message}"
            )
        derived_serializer = (
            "CLOSED" if not a2_residuals[message] and a2_nonempty[message] > 0 else "OPEN"
        )
        derived_structural = derived_serializer
        derived_blocker = "N/A" if derived_structural == "CLOSED" else (
            " | ".join(a2_residuals[message])
            if a2_residuals[message]
            else "empty_serializer_evidence"
        )
        if message in EXPECTED_CLOSURE_MESSAGES:
            if (
                state["serializer_status"] != derived_serializer
                or state["structural_status"] != derived_structural
                or state["serializer_blockers"] != derived_blocker
                or state["blocker"] != derived_blocker
            ):
                raise StatusError(f"closure status differs from final effective A2: {message}")
            continue
        if derived_structural == "CLOSED":
            raise StatusError(f"unaccounted V3 closure lacks a Priority delta: {message}")
        state["serializer_status"] = derived_serializer
        state["structural_status"] = derived_structural
        state["serializer_blockers"] = derived_blocker
        state["blocker"] = derived_blocker
        marker = "DERIVED_EFFECTIVE_A2(" + "+".join(sorted(touched_by[message])) + ")"
        if marker not in state["chain"]:
            state["chain"].append(marker)
        recomputed_open.add(message)

    if status_counts(states) != EXPECTED_FINAL:
        raise StatusError(f"V3 effective count mismatch: {status_counts(states)}")

    open_rows: list[dict[str, str]] = []
    for message in sorted(states):
        state = states[message]
        if state["priority"] != "1" or state["structural_status"] != "OPEN":
            continue
        group = primary_blocker_group(state)
        chain_text = " -> ".join(state["chain"])
        key_parts = [
            message,
            state["registry_identity_status"],
            state["serializer_status"],
            state["structural_status"],
            group,
            state["blocker"],
            chain_text,
        ]
        open_rows.append(
            {
                "status_key": sha256_bytes("\x1f".join(key_parts).encode("utf-8")),
                "message": message,
                "priority": "1",
                "matched_groups": state["matched_groups"],
                "matched_keywords": state["matched_keywords"],
                "base_line": str(base_lines[message]),
                "base_registry_identity_status": state["base_registry_identity_status"],
                "effective_registry_identity_status": state["registry_identity_status"],
                "effective_registry_identity_missing": state["registry_identity_missing"],
                "base_serializer_status": state["base_serializer_status"],
                "effective_serializer_status": state["serializer_status"],
                "base_structural_status": state["base_structural_status"],
                "effective_structural_status": state["structural_status"],
                "primary_blocker_group": group,
                "effective_blocker": state["blocker"],
                "applied_overlay_chain": chain_text,
                "row_semantics": "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW",
                "source": "IMAGE",
            }
        )
    if len(open_rows) != 111:
        raise StatusError(f"P1 OPEN row count changed: {len(open_rows)}")
    if len({row["status_key"] for row in open_rows}) != len(open_rows):
        raise StatusError("duplicate status_key")
    if len({row["message"] for row in open_rows}) != len(open_rows):
        raise StatusError("duplicate P1 OPEN message")

    groups = Counter(row["primary_blocker_group"] for row in open_rows)
    final_counts = status_counts(states)
    overall_closed = sum(count for count, _total in final_counts.values())
    report_lines = [
        "# PF V3 effective IMAGE-static priority status",
        "",
        "[MEASURED][IMAGE] This is a chained effective index. It emits no copied field rows and treats a prior delta as the required base when that delta is the current state.",
        "",
        "CAPTURE remains a separate evidence layer. V3 replay is documented in `PF_V3_FIELD_VALIDATION.md`; its aggregate TSV is byte-identical to canonical `PF_V2_FIELD_VALIDATION.tsv`, so no duplicate V3 TSV is emitted and IMAGE rows are never overwritten.",
        "",
        "## Effective structural result",
        "",
        f"- Priority 1: **{final_counts[1][0]}/{final_counts[1][1]} CLOSED** ({final_counts[1][0] / final_counts[1][1] * 100:.2f}%); OPEN {final_counts[1][1] - final_counts[1][0]}",
        f"- Priority 2: **{final_counts[2][0]}/{final_counts[2][1]} CLOSED** ({final_counts[2][0] / final_counts[2][1] * 100:.2f}%); OPEN {final_counts[2][1] - final_counts[2][0]}",
        f"- Priority 3: **{final_counts[3][0]}/{final_counts[3][1]} CLOSED** ({final_counts[3][0] / final_counts[3][1] * 100:.2f}%); OPEN {final_counts[3][1] - final_counts[3][0]}",
        f"- Overall: **{overall_closed}/519 CLOSED** ({overall_closed / 519 * 100:.2f}%); OPEN {519 - overall_closed}",
        "",
        "## Net-new correction",
        "",
        "- Removed 48 guarded `_invalid_parameter_noinfo` analysis-artifact rows, 36 proven fixed container/helper rows, and 40 proven stack-local link-state-helper rows.",
        "- The proposed global 931-row import cleanup was rejected: import identity alone did not satisfy the existing per-call wire-effect ceiling. The 883 unreviewed effective rows remain unresolved.",
        "- The raw V1 import census also exposed three `CTracePathVital` rows already removed by `PF_A2_POST_V1_STATIC_DELTA.tsv`; the dedup audit rejects them as prior output rather than emitting them again.",
        f"- Net-new A2 removal targets: {EXPECTED_V3_REMOVALS}; duplicate `delta_key`: 0; duplicate/cross-file base-row target: 0; unchanged copies: 0.",
        "- Seven messages close structurally: Priority-1 +4, Priority-2 +1, Priority-3 +2.",
        "- Four of those seven status rows chain from `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv`; using V1 as their base is forbidden and would be duplicate/stale-state output.",
        f"- OPEN blocker metadata was rebuilt from final effective A2 for {len(recomputed_open)} touched messages; no stale removed blocker is copied forward.",
        "",
        "## Priority overlay accounting",
        "",
        "| overlay | changed rows |",
        "|---|---:|",
        *[f"| `{path.name}` | {overlay_counts[path.name]} |" for path in OVERLAYS],
        "",
        f"- Applied rows: {sum(overlay_counts.values())}; distinct messages: {len(v2_messages | new_messages)}; legitimate chained messages: {len(chained)}.",
        "- Cross-file duplicate status base target: 0; duplicate priority `delta_key`: 0.",
        "",
        "## Priority-1 OPEN primary blocker groups",
        "",
        "| primary group | messages |",
        "|---|---:|",
        *[f"| `{name}` | {groups[name]} |" for name in sorted(groups)],
        "",
        "Exact names and complete blocker strings are in `PF_V3_P1_OPEN.tsv`.",
        "",
        "## Duplicate-control contract",
        "",
        "- V1 messages: 519 unique; derived output contains only the 111 Priority-1 messages still OPEN.",
        "- Every status change references the exact canonical row and line that was effective immediately before it.",
        "- A chained row also binds the predecessor `delta_key`; no base row or previous result is copied as new evidence.",
        "- Every row remains `source=IMAGE`; CAPTURE, DUMP, and DATA are not joined into this view.",
        "",
        "## Reproduction",
        "",
        "Run `py -3 -B pf_build_v3_effective_status.py --check` to hash every input, replay the complete status chain, and compare both outputs byte-for-byte.",
        "",
    ]
    v2_inputs_after = field_v3.v2.verify_pinned_inputs(OUT_DIR, False)
    if v2_inputs_after != v2_inputs_before:
        raise StatusError("transitive V2 A2 inputs changed during status derivation")
    return open_rows, "\n".join(report_lines), measured


def atomic_publish(outputs: Mapping[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    backups: dict[Path, Path | None] = {}
    originals: dict[Path, bytes | None] = {}
    published: list[Path] = []

    def cleanup(paths: Sequence[Path]) -> list[str]:
        errors: list[str] = []
        for path in paths:
            try:
                if path.exists():
                    path.unlink()
            except BaseException as exc:
                errors.append(f"{path.name}: {type(exc).__name__}")
        return errors

    try:
        for path, text in outputs.items():
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="",
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                staged.append((Path(handle.name), path))
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            if path.exists():
                originals[path] = path.read_bytes()
                backup_fd, backup_name = tempfile.mkstemp(
                    prefix=f".{path.name}.", suffix=".rollback", dir=path.parent
                )
                os.close(backup_fd)
                backup = Path(backup_name)
                backups[path] = backup
                shutil.copyfile(path, backup)
            else:
                originals[path] = None
                backups[path] = None
        for temporary, target in staged:
            published.append(target)
            os.replace(temporary, target)
        for target, expected_text in outputs.items():
            if target.read_bytes() != expected_text.encode("utf-8"):
                raise StatusError(f"post-publish read-back mismatch: {target.name}")
    except BaseException as failure:
        rollback_errors: list[str] = []
        for target in reversed(published):
            try:
                backup = backups.get(target)
                if backup is None:
                    if target.exists():
                        target.unlink()
                elif backup.exists():
                    os.replace(backup, target)
                else:
                    raise StatusError(f"rollback backup missing: {target.name}")
                original = originals[target]
                if original is None:
                    if target.exists():
                        raise StatusError(f"rollback failed to remove new target: {target.name}")
                elif not target.exists() or target.read_bytes() != original:
                    raise StatusError(f"rollback read-back mismatch: {target.name}")
            except BaseException as exc:
                rollback_errors.append(f"{target.name}: {type(exc).__name__}")
        if rollback_errors:
            # Recovery material must survive a failed rollback.
            raise StatusError(
                "publication failed and rollback is incomplete; backups/temps retained: "
                + "; ".join(rollback_errors)
            ) from failure
        cleanup_errors = cleanup(
            [temporary for temporary, _target in staged]
            + [backup for backup in backups.values() if backup is not None]
        )
        if cleanup_errors:
            raise StatusError(
                "publication rolled back; recovery cleanup incomplete: "
                + "; ".join(cleanup_errors)
            ) from failure
        raise

    # Commit/read-back succeeded. Cleanup is a separate phase: once one backup
    # is removed, a later cleanup failure must never initiate a partial rollback.
    cleanup_errors = cleanup(
        [temporary for temporary, _target in staged]
        + [backup for backup in backups.values() if backup is not None]
    )
    if cleanup_errors:
        raise StatusError(
            "outputs committed and verified; cleanup incomplete (no rollback attempted): "
            + "; ".join(cleanup_errors)
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview-unpinned", action="store_true")
    args = parser.parse_args()
    if args.check and args.preview_unpinned:
        raise StatusError("--check and --preview-unpinned are mutually exclusive")
    rows, report, measured = build(args.preview_unpinned)
    outputs = {
        OPEN_PATH: format_tsv(OPEN_COLUMNS, rows),
        REPORT_PATH: report,
    }
    if args.preview_unpinned:
        print("INPUT_SHA256=" + json.dumps(measured, sort_keys=True))
        print("PREVIEW P1 CLOSED=254/365 OPEN=111 overall CLOSED=332/519")
        return 0
    verify_pins(False)
    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_bytes() != expected.encode("utf-8"):
                raise StatusError(f"check mismatch: {path.name}")
        print("check ok: P1 CLOSED=254/365 OPEN=111 overall CLOSED=332/519")
        return 0
    atomic_publish(outputs)
    verify_pins(False)
    for path in outputs:
        print(f"{path.name} {sha256_path(path)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StatusError as exc:
        raise SystemExit(f"ERROR: {exc}")
