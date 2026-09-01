#!/usr/bin/env python3
"""Build the additive post-V1 IMAGE-only static-closure overlay.

This generator never edits the frozen V1 artifacts.  It pins the shipped image,
the two V1 source tables, and the three post-V1 static result notes; verifies the
eight cited image spans; then writes only the two delta TSVs and their report.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import struct
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
A2_SHA256 = "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
PRIORITY_SHA256 = "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"

A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
PRIORITY_NAME = "PF_PROTOCOL_PRIORITY.tsv"
A2_DELTA_NAME = "PF_A2_POST_V1_STATIC_DELTA.tsv"
PRIORITY_DELTA_NAME = "PF_POST_V1_PRIORITY_DELTA.tsv"
REPORT_NAME = "PF_POST_V1_STATIC_CLOSURE.md"

TARGETS = ("CTracePathVital", "GM_RunGMCommandVital", "TeleportVital")
TICKETS = {
    "CTracePathVital": "RE-119",
    "GM_RunGMCommandVital": "RE-088",
    "TeleportVital": "RE-090",
}

RESULT_NOTES = {
    "RE-119": (
        Path("notes_to_chief")
        / "20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md",
        "89986128551a0728fc74aa159d9792f508acee46edb1224d583a263e49b5ab22",
    ),
    "RE-088": (
        Path("archive")
        / "notes_to_chief_2026-08"
        / "20260826_1811_RE-088-RESULT-GM-COMMAND-WIRE-PINNED.md",
        "17f55d3bbcbac891870c487f8e87f029679cae4388e7ae25db6d0bcb15c61565",
    ),
    "RE-090": (
        Path("archive")
        / "notes_to_chief_2026-08"
        / "20260826_2346_RE-090-RESULT-TELEPORT-FORCEPOS-WARP-FIELDS-PINNED.md",
        "6c6b898be4220df7a84a42799e121cc1db143dbd5543bd420a50b1e93973a2a0",
    ),
}


@dataclass(frozen=True)
class SpanPin:
    message: str
    start_va: int
    end_va: int
    sha256: str
    role: str


SPAN_PINS = (
    SpanPin(
        "CTracePathVital",
        0x006EBD50,
        0x006EBE64,
        "1940cd4500e3218d701abafa56a82ca6a45b1147143e21e4ad2d97ae27724f28",
        "writer_container",
    ),
    SpanPin(
        "CTracePathVital",
        0x006EC050,
        0x006EC0FC,
        "e2e745981e5b98273fce8e9f2b5158c1af41e4ed329398d8f90568ddbb7bb4a3",
        "reader_and_wrapper",
    ),
    SpanPin(
        "CTracePathVital",
        0x006EB960,
        0x006EBA88,
        "b95745c2130cb09405d30553e0c236b440b3058acab5de779ce67e6a39e19ba8",
        "shared_record_codec",
    ),
    SpanPin(
        "GM_RunGMCommandVital",
        0x00729E10,
        0x00729EB7,
        "541d82f511ba87d444587da9f217ee7eb436431c21e7cfca6dd026d19a8c8554",
        "outer_codec",
    ),
    SpanPin(
        "GM_RunGMCommandVital",
        0x00726C20,
        0x00726CB1,
        "aa3c7c8d2d92eeee48508da2c26d78e360c612aaa2b682dfb608d7b08493559d",
        "nested_codec",
    ),
    SpanPin(
        "TeleportVital",
        0x005EB470,
        0x005EB609,
        "fbe813dbd1f9b94d87ee3c101867e8b12aaa36d69c08e68068c8ff06df990487",
        "top_level_codec",
    ),
    SpanPin(
        "TeleportVital",
        0x005DF250,
        0x005DF2F9,
        "ec9a5421ad5304372e440ecbb35184d6e93624444a262b3058569a724df0b5ef",
        "target_codec",
    ),
    SpanPin(
        "TeleportVital",
        0x005DEF10,
        0x005DEFE9,
        "105bad91394ee1dc636ef80cfe3444c293a4114d5f371fafe3ebc76ccc049c93",
        "auxiliary_codec",
    ),
)


# The 16 existing A2 numeric rows that RE-119 refines.  Values are
# (record-local wire order, tag, normalized record offset, width, gate).
CTRACE_FIELD_REFINEMENTS = {
    ("W", "0x002EAD7E"): ("1", "0x08", "RECORD+0x16", "1", "ALWAYS"),
    ("W", "0x002EAD8D"): ("2", "0x0F", "RECORD+0x10", "2", "ALWAYS"),
    ("W", "0x002EAD9C"): ("3", "0x0F", "RECORD+0x12", "2", "ALWAYS"),
    ("W", "0x002EADAB"): ("4", "0x0F", "RECORD+0x14", "2", "ALWAYS"),
    ("W", "0x002EADB7"): ("5", "0x14", "RECORD+0x00", "4", "ALWAYS"),
    ("W", "0x002EADCD"): ("6", "0x14", "RECORD+0x04", "4", "kind==2"),
    ("W", "0x002EADDC"): ("7", "0x14", "RECORD+0x08", "4", "kind==2"),
    ("W", "0x002EADFA"): ("6_ALT", "0x14", "RECORD+0x0C", "4", "kind==1"),
    ("R", "0x002EAE05"): ("1", "0x08", "RECORD+0x16", "1", "ALWAYS"),
    ("R", "0x002EAE14"): ("2", "0x0F", "RECORD+0x10", "2", "ALWAYS"),
    ("R", "0x002EAE23"): ("3", "0x0F", "RECORD+0x12", "2", "ALWAYS"),
    ("R", "0x002EAE32"): ("4", "0x0F", "RECORD+0x14", "2", "ALWAYS"),
    ("R", "0x002EAE3E"): ("5", "0x14", "RECORD+0x00", "4", "ALWAYS"),
    ("R", "0x002EAE54"): ("6", "0x14", "RECORD+0x04", "4", "kind==2"),
    ("R", "0x002EAE63"): ("7", "0x14", "RECORD+0x08", "4", "kind==2"),
    ("R", "0x002EAE7D"): ("6_ALT", "0x14", "RECORD+0x0C", "4", "kind==1"),
}

A2_DELTA_COLUMNS = (
    "delta_key",
    "action",
    "change_type",
    "base_file",
    "base_line",
    "base_row_key",
    "message",
    "direction(W/R)",
    "old_order",
    "old_tag",
    "old_field_offset",
    "old_len",
    "new_wire_order",
    "new_tag",
    "new_field_offset",
    "new_len",
    "new_gate_condition",
    "resolution",
    "evidence_ticket",
    "evidence_span_start",
    "evidence_span_end",
    "evidence_span_sha256",
    "evidence_file_off",
    "source",
)

PRIORITY_DELTA_COLUMNS = (
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
    "evidence_ticket",
    "closure_scope",
    "source",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256_path(path)
    if actual != expected:
        raise RuntimeError(f"{label} SHA-256 mismatch: expected {expected}, got {actual}")


def canonical_row_key(fieldnames: Sequence[str], row: Mapping[str, str]) -> str:
    payload = json.dumps(
        [row[name] for name in fieldnames],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def make_delta_key(parts: Iterable[str]) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return sha256_bytes(payload)


def read_tsv_with_lines(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise RuntimeError(f"missing TSV header: {path}")
        fieldnames = list(reader.fieldnames)
        rows = [(line_no, dict(row)) for line_no, row in enumerate(reader, start=2)]
    return fieldnames, rows


def write_tsv_text(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
    from io import StringIO

    handle = StringIO(newline="")
    writer = csv.DictWriter(
        handle,
        fieldnames=list(columns),
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue()


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        temp_name = None
    finally:
        if temp_name is not None:
            Path(temp_name).unlink(missing_ok=True)


class PeImage:
    def __init__(self, data: bytes) -> None:
        self.data = data
        if len(data) < 0x100 or data[:2] != b"MZ":
            raise RuntimeError("not an MZ image")
        pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
        if data[pe_offset : pe_offset + 4] != b"PE\0\0":
            raise RuntimeError("missing PE signature")
        coff = pe_offset + 4
        section_count = struct.unpack_from("<H", data, coff + 2)[0]
        optional_size = struct.unpack_from("<H", data, coff + 16)[0]
        optional = coff + 20
        magic = struct.unpack_from("<H", data, optional)[0]
        if magic != 0x10B:
            raise RuntimeError(f"expected PE32 optional header, got 0x{magic:04X}")
        self.image_base = struct.unpack_from("<I", data, optional + 28)[0]
        section_table = optional + optional_size
        self.sections: list[tuple[str, int, int, int, int]] = []
        for index in range(section_count):
            off = section_table + index * 40
            name = data[off : off + 8].split(b"\0", 1)[0].decode("ascii", "replace")
            virtual_size, virtual_address, raw_size, raw_pointer = struct.unpack_from(
                "<IIII", data, off + 8
            )
            self.sections.append(
                (name, virtual_address, virtual_size, raw_pointer, raw_size)
            )

    def va_slice(self, start_va: int, end_va: int) -> tuple[int, bytes]:
        if end_va <= start_va:
            raise RuntimeError("invalid empty/reversed VA span")
        start_rva = start_va - self.image_base
        length = end_va - start_va
        for name, section_rva, virtual_size, raw_pointer, raw_size in self.sections:
            delta = start_rva - section_rva
            if delta < 0:
                continue
            if delta + length > raw_size:
                continue
            if delta + length > max(virtual_size, raw_size):
                continue
            file_off = raw_pointer + delta
            end_off = file_off + length
            if end_off > len(self.data):
                raise RuntimeError(f"mapped span exceeds file in section {name}")
            return file_off, self.data[file_off:end_off]
        raise RuntimeError(f"cannot map VA span 0x{start_va:08X}-0x{end_va:08X}")


def verify_span_pins(image_path: Path) -> list[tuple[SpanPin, int]]:
    pe = PeImage(image_path.read_bytes())
    if pe.image_base != 0x00400000:
        raise RuntimeError(f"unexpected ImageBase: 0x{pe.image_base:08X}")
    verified: list[tuple[SpanPin, int]] = []
    for pin in SPAN_PINS:
        file_off, data = pe.va_slice(pin.start_va, pin.end_va)
        actual = sha256_bytes(data)
        if actual != pin.sha256:
            raise RuntimeError(
                f"span SHA mismatch {pin.message} 0x{pin.start_va:08X}: "
                f"expected {pin.sha256}, got {actual}"
            )
        verified.append((pin, file_off))
    return verified


def nonwire_resolution(message: str, tag: str) -> str | None:
    if message == "CTracePathVital":
        if tag.startswith("PE_IMPORT_INVALID_PARAMETER_NOINFO"):
            return "FAIL_FAST_INVALID_PARAMETER_BRANCH_NO_STREAM_EFFECT"
        if tag == "CALL_UNCLASSIFIED:0x006F8B10":
            return "VECTOR_APPEND_NO_STREAM_EFFECT"
        return None
    if message == "GM_RunGMCommandVital":
        if tag == "CALL_UNCLASSIFIED:0x007286E0":
            return "OBJECT_POOL_ALLOCATION_NO_STREAM_EFFECT"
        if tag == "DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04":
            return "REFCOUNT_DECREMENT_NO_STREAM_EFFECT"
        if tag == "ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C":
            return "REFCOUNT_INCREMENT_NO_STREAM_EFFECT"
        return None
    if message == "TeleportVital":
        if tag in {
            "CALL_UNCLASSIFIED:0x004B1C40",
            "CALL_UNCLASSIFIED:0x005EA810",
        }:
            return "OBJECT_POOL_ALLOCATION_NO_STREAM_EFFECT"
        if tag == "DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04":
            return "REFCOUNT_DECREMENT_NO_STREAM_EFFECT"
        if tag == "ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C":
            return "REFCOUNT_INCREMENT_NO_STREAM_EFFECT"
        return None
    return None


def compact_span_for_row(row: Mapping[str, str]) -> tuple[str, str, str]:
    return row["span_start"], row["span_end"], row["span_sha256"]


def build_a2_delta(
    fieldnames: Sequence[str], rows: Sequence[tuple[int, dict[str, str]]]
) -> list[dict[str, str]]:
    delta: list[dict[str, str]] = []
    removal_counts = {target: 0 for target in TARGETS}
    refinement_seen: set[tuple[str, str]] = set()

    for line_no, row in rows:
        message = row["message"]
        if message not in TARGETS:
            continue
        if row["source"] != "IMAGE":
            raise RuntimeError(f"target base row is not IMAGE at {A2_NAME}:{line_no}")
        row_key = canonical_row_key(fieldnames, row)
        direction = row["direction(W/R)"]
        resolution = nonwire_resolution(message, row["tag"])
        if resolution is not None:
            start, end, span_hash = compact_span_for_row(row)
            values = {
                "action": "REMOVE_NONWIRE_ROW",
                "change_type": "NONWIRE_LIFECYCLE_OR_CONTAINER_ARTIFACT",
                "base_file": A2_NAME,
                "base_line": str(line_no),
                "base_row_key": row_key,
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
                "resolution": resolution,
                "evidence_ticket": TICKETS[message],
                "evidence_span_start": start,
                "evidence_span_end": end,
                "evidence_span_sha256": span_hash,
                "evidence_file_off": row["file_off_claim"],
                "source": "IMAGE",
            }
            values["delta_key"] = make_delta_key(
                (
                    "A2",
                    values["action"],
                    message,
                    direction,
                    str(line_no),
                    row_key,
                )
            )
            delta.append(values)
            removal_counts[message] += 1

        refinement_key = (direction, row["file_off_claim"])
        refinement = CTRACE_FIELD_REFINEMENTS.get(refinement_key)
        if message == "CTracePathVital" and refinement is not None:
            new_order, new_tag, new_offset, new_len, new_gate = refinement
            if row["tag"] != new_tag or row["len"] != new_len:
                raise RuntimeError(
                    f"CTrace row drift at {A2_NAME}:{line_no}: "
                    f"expected {new_tag}/{new_len}, got {row['tag']}/{row['len']}"
                )
            if row["span_start"] != "0x006EB960" or row["span_end"] != "0x006EBA88":
                raise RuntimeError(f"CTrace record span drift at {A2_NAME}:{line_no}")
            if row["span_sha256"] != SPAN_PINS[2].sha256:
                raise RuntimeError(f"CTrace record SHA drift at {A2_NAME}:{line_no}")
            values = {
                "action": "CHANGED",
                "change_type": "RECORD_OFFSET_AND_DISCRIMINATOR_GATE_REFINEMENT",
                "base_file": A2_NAME,
                "base_line": str(line_no),
                "base_row_key": row_key,
                "message": message,
                "direction(W/R)": direction,
                "old_order": row["order"],
                "old_tag": row["tag"],
                "old_field_offset": row["field_offset"],
                "old_len": row["len"],
                "new_wire_order": new_order,
                "new_tag": new_tag,
                "new_field_offset": new_offset,
                "new_len": new_len,
                "new_gate_condition": new_gate,
                "resolution": "RE119_DISCRIMINATED_RECORD_LAYOUT",
                "evidence_ticket": "RE-119",
                "evidence_span_start": row["span_start"],
                "evidence_span_end": row["span_end"],
                "evidence_span_sha256": row["span_sha256"],
                "evidence_file_off": row["file_off_claim"],
                "source": "IMAGE",
            }
            values["delta_key"] = make_delta_key(
                (
                    "A2",
                    values["action"],
                    message,
                    direction,
                    str(line_no),
                    row_key,
                    new_order,
                    new_gate,
                )
            )
            delta.append(values)
            refinement_seen.add(refinement_key)

    expected_removals = {
        "CTracePathVital": 8,
        "GM_RunGMCommandVital": 6,
        "TeleportVital": 12,
    }
    if removal_counts != expected_removals:
        raise RuntimeError(
            f"unexpected nonwire removal counts: {removal_counts} != {expected_removals}"
        )
    if refinement_seen != set(CTRACE_FIELD_REFINEMENTS):
        missing = sorted(set(CTRACE_FIELD_REFINEMENTS) - refinement_seen)
        extra = sorted(refinement_seen - set(CTRACE_FIELD_REFINEMENTS))
        raise RuntimeError(f"CTrace refinement drift; missing={missing}, extra={extra}")
    if len(delta) != 42:
        raise RuntimeError(f"expected 42 A2 delta rows, got {len(delta)}")
    if sum(row["action"] == "CHANGED" for row in delta) != 16:
        raise RuntimeError("expected 16 changed A2 rows")
    if sum(row["action"] == "REMOVE_NONWIRE_ROW" for row in delta) != 26:
        raise RuntimeError("expected 26 nonwire-removal A2 rows")
    if len({row["delta_key"] for row in delta}) != len(delta):
        raise RuntimeError("duplicate A2 delta_key")
    if len({(row["base_line"], row["base_row_key"]) for row in delta}) != len(delta):
        raise RuntimeError("one base A2 row was targeted more than once")
    delta.sort(
        key=lambda row: (
            row["message"],
            0 if row["direction(W/R)"] == "W" else 1,
            int(row["base_line"]),
            row["action"],
        )
    )
    return delta


def build_priority_delta(
    fieldnames: Sequence[str], rows: Sequence[tuple[int, dict[str, str]]]
) -> tuple[list[dict[str, str]], dict[str, int]]:
    p1_rows = [row for _, row in rows if row["priority"] == "1"]
    base_closed = sum(
        row["registry_identity_status"] == "KNOWN"
        and row["serializer_status"] == "CLOSED"
        and row["structural_status"] == "CLOSED"
        for row in p1_rows
    )
    counts = {
        "base_total": len(p1_rows),
        "base_closed": base_closed,
        "base_open": len(p1_rows) - base_closed,
        "new_closed": base_closed + len(TARGETS),
        "new_open": len(p1_rows) - base_closed - len(TARGETS),
    }
    expected_counts = {
        "base_total": 365,
        "base_closed": 241,
        "base_open": 124,
        "new_closed": 244,
        "new_open": 121,
    }
    if counts != expected_counts:
        raise RuntimeError(f"Priority-1 count drift: {counts} != {expected_counts}")

    found: dict[str, tuple[int, dict[str, str]]] = {}
    for line_no, row in rows:
        if row["message"] in TARGETS:
            if row["message"] in found:
                raise RuntimeError(f"duplicate priority base message: {row['message']}")
            found[row["message"]] = (line_no, row)
    if set(found) != set(TARGETS):
        raise RuntimeError(f"missing priority targets: {sorted(set(TARGETS) - set(found))}")

    output: list[dict[str, str]] = []
    for message in TARGETS:
        line_no, row = found[message]
        if row["source"] != "IMAGE":
            raise RuntimeError(f"priority target is not IMAGE: {message}")
        if row["priority"] != "1":
            raise RuntimeError(f"priority target is not P1: {message}")
        if row["registry_identity_status"] != "KNOWN":
            raise RuntimeError(f"priority target identity is not KNOWN: {message}")
        if row["serializer_status"] != "OPEN" or row["structural_status"] != "OPEN":
            raise RuntimeError(f"priority target is not OPEN/OPEN: {message}")
        row_key = canonical_row_key(fieldnames, row)
        values = {
            "action": "CHANGED",
            "base_file": PRIORITY_NAME,
            "base_line": str(line_no),
            "base_row_key": row_key,
            "message": message,
            "priority": "1",
            "old_serializer_status": "OPEN",
            "new_serializer_status": "CLOSED",
            "old_structural_status": "OPEN",
            "new_structural_status": "CLOSED",
            "old_blocker": row["blocker"],
            "new_blocker": "N/A",
            "evidence_ticket": TICKETS[message],
            "closure_scope": "STATIC_WIRE_STRUCTURE_ONLY;RUNTIME_SEMANTICS_NOT_PROMOTED",
            "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(
            (
                "PRIORITY",
                values["action"],
                message,
                str(line_no),
                row_key,
                "CLOSED",
            )
        )
        output.append(values)
    if len(output) != 3 or len({row["delta_key"] for row in output}) != 3:
        raise RuntimeError("priority delta cardinality/dedup failure")
    return output, counts


def validate_post_overlay_closure(
    rows: Sequence[tuple[int, dict[str, str]]],
    delta: Sequence[Mapping[str, str]],
) -> None:
    """Apply the delta logically and fail if any target wire blocker remains."""
    by_line = {int(row["base_line"]): row for row in delta}
    unresolved: list[str] = []
    remaining_counts = {message: 0 for message in TARGETS}
    for line_no, base in rows:
        message = base["message"]
        if message not in TARGETS:
            continue
        overlay = by_line.get(line_no)
        if overlay is not None and overlay["action"] == "REMOVE_NONWIRE_ROW":
            continue
        if overlay is not None and overlay["action"] == "CHANGED":
            tag = overlay["new_tag"]
            field_offset = overlay["new_field_offset"]
        else:
            tag = base["tag"]
            field_offset = base["field_offset"]
        remaining_counts[message] += 1
        blocker_tag = tag == "UNKNOWN" or tag.startswith(
            (
                "CALL_UNCLASSIFIED:",
                "JUMP_UNCLASSIFIED:",
                "DYNAMIC_",
                "ATOMIC_",
                "PE_IMPORT_",
            )
        )
        if blocker_tag or "UNKNOWN(" in field_offset:
            unresolved.append(
                f"{message}:{line_no}:{tag}:{field_offset}"
            )
    if any(count == 0 for count in remaining_counts.values()):
        raise RuntimeError(
            f"post-overlay target lost all wire rows: {remaining_counts}"
        )
    if unresolved:
        raise RuntimeError(
            "post-overlay target still has unresolved wire rows: "
            + " | ".join(unresolved)
        )


def validate_post_overlay_guard_control(
    rows: Sequence[tuple[int, dict[str, str]]],
    delta: Sequence[Mapping[str, str]],
) -> None:
    """Independent tag-only and field-only mutations must each fail red."""
    sample = next(row for _line, row in rows if row["message"] == "TeleportVital")
    synthetic_line = max(line for line, _row in rows) + 1

    mutations: list[tuple[str, dict[str, str]]] = []
    tag_only = dict(sample)
    tag_only["order"] = "999998"
    tag_only["tag"] = "UNKNOWN"
    tag_only["field_offset"] = "+0x14"
    mutations.append(("unknown_tag_only", tag_only))

    field_only = dict(sample)
    field_only["order"] = "999999"
    field_only["tag"] = "0x08"
    field_only["field_offset"] = "PHI(+0x14,UNKNOWN(synthetic_field_only))"
    mutations.append(("unknown_field_only", field_only))

    for label, mutation in mutations:
        try:
            validate_post_overlay_closure(
                tuple(rows) + ((synthetic_line, mutation),), delta
            )
        except RuntimeError:
            continue
        raise RuntimeError(
            f"synthetic {label} unresolved-row mutation was unexpectedly accepted"
        )


def report_text(
    a2_delta: Sequence[Mapping[str, str]],
    priority_delta: Sequence[Mapping[str, str]],
    counts: Mapping[str, int],
    verified_spans: Sequence[tuple[SpanPin, int]],
    a2_delta_hash: str,
    priority_delta_hash: str,
) -> str:
    span_lines = []
    for pin, file_off in verified_spans:
        span_lines.append(
            f"| {pin.message} | {pin.role} | `0x{pin.start_va:08X}` | "
            f"`0x{pin.end_va:08X}` | `0x{file_off:08X}` | `{pin.sha256}` |"
        )
    return "\n".join(
        [
            "# PF post-V1 static closure overlay",
            "",
            "[MEASURED] Every changed/removed row and span hash below is re-derived from the pinned IMAGE and frozen V1 tables by this generator.",
            "",
            "This is an additive, IMAGE-only overlay on the frozen V1 tables. It does not rewrite "
            "`PF_SERIALIZER_FIELDS.tsv` or `PF_PROTOCOL_PRIORITY.tsv`, and it does not copy unchanged rows.",
            "",
            "## Outcome",
            "",
            f"- Priority 1 static closure moves from {counts['base_closed']}/{counts['base_total']} "
            f"to **{counts['new_closed']}/{counts['base_total']}**; remaining open: "
            f"**{counts['new_open']}**.",
            "- The three changed messages are `CTracePathVital` (RE-119), "
            "`GM_RunGMCommandVital` (RE-088), and `TeleportVital` (RE-090).",
            "- All facts in both TSVs have `source=IMAGE`. No DUMP, CAPTURE, or DATA fact is joined "
            "into any row.",
            "",
            "## Duplicate-control accounting",
            "",
            "| table | added | changed | remove-nonwire directives | unchanged copied | duplicate rejected |",
            "|---|---:|---:|---:|---:|---:|",
            "| A2 delta | 0 | 16 | 26 | 0 | 0 |",
            "| Priority delta | 0 | 3 | 0 | 0 | 0 |",
            "| Combined | 0 | 19 | 26 | 0 | 0 |",
            "",
            "Every delta row carries the original V1 line number plus a SHA-256 `base_row_key` "
            "over the complete original row. `delta_key` is independently deterministic and unique. "
            "The 42 A2 rows target 42 distinct base rows; the priority overlay changes three existing "
            "message rows and does not add duplicate messages.",
            "",
            "## A2 changes",
            "",
            "- `CTracePathVital`: remove seven invalid-parameter fail-fast artifacts and one vector-append "
            "artifact from the wire-field census. Refine the 16 existing W/R record rows to the "
            "discriminated layout: `u8 +0x16`, signed-width `i16 +0x10/+0x12/+0x14`, raw32 `+0x00`, "
            "raw32 `+0x04/+0x08` only for `kind==2`, and raw32 `+0x0C` only for `kind==1`.",
            "- `GM_RunGMCommandVital`: remove two pool-allocation and four reference-count artifacts. "
            "The already-present outer presence plus nested `u32,u32,u8,wstring,wstring` rows are not "
            "copied into this delta.",
            "- `TeleportVital`: remove four pool-allocation and eight reference-count artifacts. The "
            "already-present target/auxiliary/scalar fields are not copied into this delta.",
            "",
            "The separate `PF_A2_STRING_WIRE_TAG_DELTA.tsv` supersedes the old `UNTAGGED_*` wording "
            "for the exact string helpers (wire tags `0x44`/`0x48`). This overlay does not duplicate "
            "those string-tag rows.",
            "",
            "## Verified IMAGE spans",
            "",
            "| message | role | start VA | end VA (exclusive) | file offset | SHA-256 |",
            "|---|---|---:|---:|---:|---|",
            *span_lines,
            "",
            "## Evidence and output pins",
            "",
            f"- image SHA-256: `{IMAGE_SHA256}`",
            f"- frozen A2 SHA-256: `{A2_SHA256}`",
            f"- frozen priority SHA-256: `{PRIORITY_SHA256}`",
            f"- `{A2_DELTA_NAME}` SHA-256: `{a2_delta_hash}`",
            f"- `{PRIORITY_DELTA_NAME}` SHA-256: `{priority_delta_hash}`",
            "- RE-119 result SHA-256: "
            f"`{RESULT_NOTES['RE-119'][1]}`",
            "- RE-088 result SHA-256: "
            f"`{RESULT_NOTES['RE-088'][1]}`",
            "- RE-090 result SHA-256: "
            f"`{RESULT_NOTES['RE-090'][1]}`",
            "",
            "## Semantic bounds / nonclaims",
            "",
            "1. `CTracePathVital` tag `0x14` remains raw 32-bit, not proven float. Only the signed "
            "16-bit triplet is converted to float by the consumer. Request value 743 remains "
            "semantically unresolved.",
            "2. GM scalar, string, and result-byte meanings remain unknown. Structural closure does not "
            "prove a live command trigger or natural network direction.",
            "3. Teleport flags and auxiliary-object meanings remain unknown. Pool/refcount calls are "
            "nonwire; that does not establish gameplay semantics or natural direction.",
            "4. These three messages remain unvalidated by original live capture where the V1 capture "
            "ledger says not observed/static-open. Static closure is not the same as runtime validation "
            "or implementation readiness.",
            "5. This overlay does not modify server code, GameClient, V1 artifacts, queue/workflow files, "
            "or any DUMP/CAPTURE/DATA output.",
            "",
            "## Reproduction",
            "",
            f"Run `py -3 -B {Path(__file__).name}` from any directory. The generator verifies all input "
            "hashes and span hashes, enforces exact row counts and unique keys, logically applies the "
            "overlay and rejects residual UNKNOWN tags and field offsets with independent mutation controls, "
            "writes each file by atomic replace, and "
            "contains no wall-clock value, so repeated runs are byte-deterministic.",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    workspace = here.parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", type=Path, default=here)
    parser.add_argument(
        "--image",
        type=Path,
        default=workspace / "GameClient" / "GameClient.local.bin",
    )
    parser.add_argument("--bridge", type=Path, default=here.parent)
    parser.add_argument(
        "--check",
        action="store_true",
        help="derive in memory and require byte-identical existing outputs",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    external = args.external.resolve()
    image = args.image.resolve()
    bridge = args.bridge.resolve()
    a2_path = external / A2_NAME
    priority_path = external / PRIORITY_NAME

    protected = {
        image: (IMAGE_SHA256, "GameClient image"),
        a2_path: (A2_SHA256, "frozen A2"),
        priority_path: (PRIORITY_SHA256, "frozen priority"),
    }
    for ticket, (relative, expected_hash) in RESULT_NOTES.items():
        protected[bridge / relative] = (expected_hash, f"{ticket} result note")
    for path, (expected_hash, label) in protected.items():
        require_hash(path, expected_hash, label)

    verified_spans = verify_span_pins(image)
    a2_fields, a2_rows = read_tsv_with_lines(a2_path)
    priority_fields, priority_rows = read_tsv_with_lines(priority_path)
    a2_delta = build_a2_delta(a2_fields, a2_rows)
    validate_post_overlay_closure(a2_rows, a2_delta)
    validate_post_overlay_guard_control(a2_rows, a2_delta)
    priority_delta, counts = build_priority_delta(priority_fields, priority_rows)

    if any(row["source"] != "IMAGE" for row in a2_delta):
        raise RuntimeError("non-IMAGE row in A2 delta")
    if any(row["source"] != "IMAGE" for row in priority_delta):
        raise RuntimeError("non-IMAGE row in priority delta")

    a2_text = write_tsv_text(A2_DELTA_COLUMNS, a2_delta)
    priority_text = write_tsv_text(PRIORITY_DELTA_COLUMNS, priority_delta)
    a2_hash = sha256_bytes(a2_text.encode("utf-8"))
    priority_hash = sha256_bytes(priority_text.encode("utf-8"))
    report = report_text(
        a2_delta,
        priority_delta,
        counts,
        verified_spans,
        a2_hash,
        priority_hash,
    )

    # Close the read-only input window before replacing any deliverable.
    for path, (expected_hash, label) in protected.items():
        require_hash(path, expected_hash, label + " before publish")

    outputs = {
        external / A2_DELTA_NAME: a2_text,
        external / PRIORITY_DELTA_NAME: priority_text,
        external / REPORT_NAME: report,
    }
    if args.check:
        for path, expected_text in outputs.items():
            if not path.is_file():
                raise RuntimeError(f"check output missing: {path.name}")
            if path.read_text(encoding="utf-8") != expected_text:
                raise RuntimeError(f"check output differs: {path.name}")
    else:
        for path, text in outputs.items():
            atomic_write_text(path, text)

    print("PASS post-V1 static closure overlay mode=%s" % ("check" if args.check else "publish"))
    print("a2_rows=42 changed=16 removed_nonwire=26 added=0")
    print("priority_rows=3 changed=3 added=0")
    print("unchanged_copied=0 duplicate_rejected=0")
    print("priority1_closed=244 priority1_total=365 priority1_open=121")
    print(f"a2_delta_sha256={a2_hash}")
    print(f"priority_delta_sha256={priority_hash}")
    print(f"report_sha256={sha256_bytes(report.encode('utf-8'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
