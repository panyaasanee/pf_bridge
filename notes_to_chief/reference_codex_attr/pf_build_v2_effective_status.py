#!/usr/bin/env python3
"""Build the deduplicated effective IMAGE-static Priority-1 OPEN status for PF v2.

V1 and every evidence overlay remain immutable.  This generator applies only
message-keyed status changes, emits no field rows, and publishes only the
effective Priority-1 rows that are still OPEN.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import tempfile
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
BASE_PATH = OUT_DIR / "PF_PROTOCOL_PRIORITY.tsv"
OVERLAYS = (
    OUT_DIR / "PF_POST_V1_PRIORITY_DELTA.tsv",
    OUT_DIR / "PF_PRIORITY_POOL_638690_DELTA.tsv",
    OUT_DIR / "PF_PRIORITY_POOL_661FA0_DELTA.tsv",
    OUT_DIR / "PF_PRIORITY_POOL_46F4D0_DELTA.tsv",
    OUT_DIR / "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv",
)
OPEN_PATH = OUT_DIR / "PF_V2_P1_OPEN.tsv"
REPORT_PATH = OUT_DIR / "PF_V2_EFFECTIVE_STATUS.md"

PINNED_SHA256 = {
    BASE_PATH: "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55",
    OVERLAYS[0]: "69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51",
    OVERLAYS[1]: "cc585d983dd1ca155ea1cfcfc59116897b59d2ce2455dc96f1d4097e9d7afdd5",
    OVERLAYS[2]: "3ba436e9b4876a1575a6d5544f49bb462896e2c6ae4191e085eacb56788ef880",
    OVERLAYS[3]: "32a59e143052f827f8134bba890f28d63444c447943e6679521dade7ff7e9fd1",
    OVERLAYS[4]: "00ef0f3cb632b40ba168ce79bbd656fc7a6936a55f3b3e185c6e63b32c39ec5d",
}

EXPECTED_BASE = {1: (241, 365), 2: (12, 16), 3: (84, 138)}
EXPECTED_FINAL = {1: (250, 365), 2: (7, 16), 3: (68, 138)}

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
    "applied_overlay",
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


def verify_pins() -> None:
    for path, expected in PINNED_SHA256.items():
        actual = sha256_path(path)
        if actual != expected:
            raise StatusError(
                f"pinned input changed: {path.name}: expected {expected}, got {actual}"
            )


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


def build() -> tuple[list[dict[str, str]], str]:
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
            "applied_overlay": "BASE_ONLY",
            "base_registry_identity_status": row["registry_identity_status"],
            "base_serializer_status": row["serializer_status"],
            "base_structural_status": row["structural_status"],
        }
        base_keys[message] = canonical_row_key(base_fields, row)
        base_lines[message] = line

    baseline_counts: dict[int, tuple[int, int]] = {}
    for priority in (1, 2, 3):
        rows = [state for state in states.values() if int(state["priority"]) == priority]
        baseline_counts[priority] = (
            sum(state["structural_status"] == "CLOSED" for state in rows),
            len(rows),
        )
    if baseline_counts != EXPECTED_BASE:
        raise StatusError(f"base count mismatch: {baseline_counts}")

    touched: dict[str, str] = {}
    overlay_counts: Counter[str] = Counter()
    for path in OVERLAYS:
        _fields, rows = read_tsv(path)
        local_messages: set[str] = set()
        local_delta_keys: set[str] = set()
        local_base_keys: set[str] = set()
        for _line, row in rows:
            required = {
                "delta_key",
                "action",
                "base_file",
                "base_line",
                "base_row_key",
                "message",
                "priority",
                "old_serializer_status",
                "new_serializer_status",
                "old_structural_status",
                "new_structural_status",
                "old_blocker",
                "new_blocker",
                "source",
            }
            missing = required - row.keys()
            if missing:
                raise StatusError(f"{path.name} missing columns: {sorted(missing)}")
            message = row["message"]
            if message not in states:
                raise StatusError(f"unknown overlay message: {path.name}: {message}")
            if row["action"] != "CHANGED" or row["source"] != "IMAGE":
                raise StatusError(f"invalid overlay action/source: {path.name}: {message}")
            if row["base_file"] != BASE_PATH.name:
                raise StatusError(f"invalid base_file: {path.name}: {message}")
            if int(row["base_line"]) != base_lines[message]:
                raise StatusError(f"base_line mismatch: {path.name}: {message}")
            if row["base_row_key"] != base_keys[message]:
                raise StatusError(f"base_row_key mismatch: {path.name}: {message}")
            state = states[message]
            if row["priority"] != state["priority"]:
                raise StatusError(f"priority mismatch: {path.name}: {message}")
            if row["old_serializer_status"] != state["base_serializer_status"]:
                raise StatusError(f"old serializer mismatch: {path.name}: {message}")
            if row["old_structural_status"] != state["base_structural_status"]:
                raise StatusError(f"old structural mismatch: {path.name}: {message}")
            base_row = next(row0 for _line0, row0 in base_rows if row0["message"] == message)
            if row["old_blocker"] != base_row["blocker"]:
                raise StatusError(f"old blocker mismatch: {path.name}: {message}")
            if message in touched:
                raise StatusError(
                    f"cross-overlay duplicate message: {message}: {touched[message]} / {path.name}"
                )
            if message in local_messages or row["delta_key"] in local_delta_keys:
                raise StatusError(f"within-overlay duplicate: {path.name}: {message}")
            if row["base_row_key"] in local_base_keys:
                raise StatusError(f"within-overlay duplicate base row: {path.name}: {message}")
            local_messages.add(message)
            local_delta_keys.add(row["delta_key"])
            local_base_keys.add(row["base_row_key"])
            touched[message] = path.name
            overlay_counts[path.name] += 1

            state["serializer_status"] = row["new_serializer_status"]
            state["structural_status"] = row["new_structural_status"]
            state["blocker"] = row["new_blocker"]
            if "new_serializer_blockers" in row:
                state["serializer_blockers"] = row["new_serializer_blockers"]
            if "new_registry_identity_status" in row:
                state["registry_identity_status"] = row["new_registry_identity_status"]
                state["registry_identity_missing"] = row["new_registry_identity_missing"]
            state["applied_overlay"] = path.name

    if sum(overlay_counts.values()) != 52:
        raise StatusError(f"overlay row count changed: {dict(overlay_counts)}")

    final_counts: dict[int, tuple[int, int]] = {}
    for priority in (1, 2, 3):
        rows = [state for state in states.values() if int(state["priority"]) == priority]
        final_counts[priority] = (
            sum(state["structural_status"] == "CLOSED" for state in rows),
            len(rows),
        )
    if final_counts != EXPECTED_FINAL:
        raise StatusError(f"effective count mismatch: {final_counts}")

    open_rows: list[dict[str, str]] = []
    for message in sorted(states):
        state = states[message]
        if state["priority"] != "1" or state["structural_status"] != "OPEN":
            continue
        group = primary_blocker_group(state)
        key_parts = [
            message,
            state["registry_identity_status"],
            state["serializer_status"],
            state["structural_status"],
            group,
            state["blocker"],
            state["applied_overlay"],
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
                "applied_overlay": state["applied_overlay"],
                "row_semantics": "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW",
                "source": "IMAGE",
            }
        )

    if len(open_rows) != 115:
        raise StatusError(f"P1 OPEN row count changed: {len(open_rows)}")
    if len({row["status_key"] for row in open_rows}) != len(open_rows):
        raise StatusError("duplicate status_key")
    if len({row["message"] for row in open_rows}) != len(open_rows):
        raise StatusError("duplicate P1 OPEN message")

    groups = Counter(row["primary_blocker_group"] for row in open_rows)
    overall_closed = sum(count for count, _total in final_counts.values())
    report_lines = [
        "# PF v2 effective IMAGE-static priority status",
        "",
        "[MEASURED][IMAGE] ดัชนีนี้คำนวณจาก V1 และ IMAGE overlay ที่ pin hash แล้ว ไม่ใช่ตารางหลักฐานใหม่ และไม่คัดลอก field row เดิม",
        "",
        "🔴 ผล CAPTURE เป็นคนละชั้นหลักฐาน: `PF_V2_FIELD_VALIDATION.tsv` พบ mismatch 386 instances ที่ 3 field locations / 4 field+reason points; ห้ามตีความ 250 CLOSED ด้านล่างว่าได้รับการยืนยันจากสายจริงทั้งหมด",
        "",
        "## Effective IMAGE-static structural result",
        "",
        f"- Priority 1: **{final_counts[1][0]}/{final_counts[1][1]} CLOSED** ({final_counts[1][0] / final_counts[1][1] * 100:.2f}%); OPEN {final_counts[1][1] - final_counts[1][0]}",
        f"- Priority 2: **{final_counts[2][0]}/{final_counts[2][1]} CLOSED** ({final_counts[2][0] / final_counts[2][1] * 100:.2f}%); OPEN {final_counts[2][1] - final_counts[2][0]}",
        f"- Priority 3: **{final_counts[3][0]}/{final_counts[3][1]} CLOSED** ({final_counts[3][0] / final_counts[3][1] * 100:.2f}%); OPEN {final_counts[3][1] - final_counts[3][0]}",
        f"- Overall: **{overall_closed}/519 CLOSED** ({overall_closed / 519 * 100:.2f}%); OPEN {519 - overall_closed}",
        "",
        "## Overlay accounting",
        "",
        "| overlay | changed status rows |",
        "|---|---:|",
        *[f"| `{path.name}` | {overlay_counts[path.name]} |" for path in OVERLAYS],
        "",
        "- V1 structural CLOSED: 337/519.",
        "- post-V1 plus three proven pools: +15 CLOSED.",
        "- serializer-slot +0x34 truth correction: -27 structural CLOSED.",
        "- effective structural CLOSED: 325/519.",
        "- `PF_A2_POOL_46BAA0_READER_DELTA.tsv` changes three reader rows only; its dynamic writer identities remain OPEN, so it changes no priority status.",
        "- `PF_TARGET_652A30_A2_DELTA.tsv` and `PF_TARGETS_694790_6B3440_A2_DELTA.tsv` remove non-wire A2 rows only; they change no priority status.",
        "",
        "## Priority-1 OPEN primary blocker groups",
        "",
        "| primary group | messages |",
        "|---|---:|",
        *[f"| `{name}` | {groups[name]} |" for name in sorted(groups)],
        "",
        "Exact names and complete blocker strings are in `PF_V2_P1_OPEN.tsv`.",
        "",
        "## Duplicate-control contract",
        "",
        "- Base messages: 519 unique.",
        "- Priority overlay rows: 52; duplicate messages within/across overlays: 0.",
        "- `delta_key` and `base_row_key` duplicates within each overlay: 0.",
        "- Every overlay base line/hash/status matches the immutable V1 row.",
        "- Output rows: 115 OPEN-only derived status rows; CLOSED rows and A1/A2/A3 fields are not copied.",
        "- `row_semantics=DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW` prevents this view from being counted as another evidence table.",
        "- Every TSV row in this derived status view remains `source=IMAGE`; no DUMP, CAPTURE, or DATA layer is joined.",
        "- CAPTURE mismatch counts are reported separately and never used to overwrite IMAGE status rows.",
        "",
        "## Reproduction",
        "",
        "Run `py -3 -B pf_build_v2_effective_status.py --check` to re-hash every input, re-apply all status deltas, and compare both outputs byte-for-byte.",
        "",
    ]
    return open_rows, "\n".join(report_lines)


def atomic_publish(outputs: Mapping[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
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
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
                staged.append((Path(handle.name), path))
        verify_pins()
        for temporary, target in staged:
            os.replace(temporary, target)
    finally:
        for temporary, _target in staged:
            if temporary.exists():
                temporary.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    verify_pins()
    rows, report = build()
    outputs = {
        OPEN_PATH: format_tsv(OPEN_COLUMNS, rows),
        REPORT_PATH: report,
    }
    verify_pins()
    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                raise StatusError(f"check mismatch: {path.name}")
        print("check ok: P1 CLOSED=250/365 OPEN=115 overall CLOSED=325/519")
        return 0
    atomic_publish(outputs)
    for path in outputs:
        print(f"{path.name} {sha256_path(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
