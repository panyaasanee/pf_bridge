#!/usr/bin/env python3
"""Validate IMAGE-derived A2 field sequences against captured PC byte blocks.

The output is aggregate CAPTURE evidence only.  It never emits captured values,
payload bytes, or hexdumps.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path


SOURCE = "CAPTURE"
EXPECTED_PROTOCOL_COUNT = 519
EXPECTED_CAPTURE_FILE_COUNT = 1772
EXPECTED_CAPTURE_BYTES = 595_134_426
EXPECTED_CAPTURE_TEXT_FILES = 918
EXPECTED_FILES_WITH_BLOCKS = 277
EXPECTED_PC_BLOCKS = 10_462
EXPECTED_DECOMPRESSED_BLOCKS = 41_432
EXPECTED_OUTER_INSTANCES = 51_894
EXPECTED_NESTED_DECLARED = 13_220
EXPECTED_NESTED_REACHED = 12_785
EXPECTED_NESTED_UNRESOLVED = 435
EXPECTED_PASS_INSTANCES = 11_904
EXPECTED_STATIC_OPEN_INSTANCES = 52_775
EXPECTED_MISMATCH_INSTANCES = 0
EXPECTED_VALIDATED_NESTED_FRAMES = 11_427
EXPECTED_STATIC_OPEN_NESTED_FRAMES = 881
EXPECTED_MISMATCH_NESTED_FRAMES = 0
EXPECTED_NO_RUNTIME_TAIL_FRAMES = 1_939
EXPECTED_RUNTIME_ZERO_TAIL_FRAMES = 9_481
EXPECTED_FRAMING_UNRESOLVED_FRAMES = 0
EXPECTED_OBSERVED_OUTPUT_ROWS = 58
EXPECTED_OUTPUT_STATUSES = {
    "NOT_OBSERVED": 980,
    "VALIDATED": 37,
    "A2_STATIC_OPEN": 21,
}
PC_MARKER_RE = re.compile(r"^(PC|DECOMPRESSED) ([0-9]+)$")
HEXDUMP_RE = re.compile(r"^([0-9A-Fa-f]{8})  (.*?)  \|")
RAW_BYTE_RUN_RE = re.compile(r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)")
STRING_TAGS = {
    "UNTAGGED_STRING8_LEN32LE": 0x44,
    "UNTAGGED_WSTRING16LE_LEN32LE": 0x48,
}
ZERO_LENGTH_NONWIRE_TAGS = {
    "EMPTY",
    "PURE_READONLY_CHAIN_PLUS_04_CONTAINS_PREDICATE",
}
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
class SchemaField:
    order: int
    tag: str
    length: str


@dataclass(frozen=True)
class SchemaResult:
    status: str
    end: int
    field_index: int = 0
    reason: str = ""


@dataclass
class MessageAggregate:
    observed_instances: int = 0
    pass_instances: int = 0
    static_open_instances: int = 0
    mismatch_instances: int = 0
    observed_frames: set[str] = field(default_factory=set)
    pass_frames: set[str] = field(default_factory=set)
    static_open_frames: set[str] = field(default_factory=set)
    mismatch_frames: set[str] = field(default_factory=set)
    capture_files: set[str] = field(default_factory=set)
    mismatch_points: Counter[tuple[int, str]] = field(default_factory=Counter)


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
    nested_unresolved_after_open: int = 0
    unknown_message_id_instances: int = 0
    no_runtime_tail_frames: int = 0
    runtime_zero_tail_frames: int = 0
    framing_unresolved_frames: int = 0
    validated_nested_frames: set[str] = field(default_factory=set)
    static_open_nested_frames: set[str] = field(default_factory=set)
    mismatch_nested_frames: set[str] = field(default_factory=set)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def protocol_id(name: str) -> int:
    return sum((index + 1) * ord(character) for index, character in enumerate(name)) & 0xFFFF


def enumerate_capture_paths(root: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for directory in root.rglob("capture_*"):
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                paths[relative.casefold()] = path
    return paths


def load_capture_inputs(root: Path, inventory_path: Path) -> list[CaptureInput]:
    inventory = read_tsv(inventory_path)
    if not inventory or "source" not in inventory[0]:
        raise ValidationError("PF_INPUT_INVENTORY.tsv lacks source")
    rows = [row for row in inventory if row["source"] == SOURCE]
    if len(rows) != EXPECTED_CAPTURE_FILE_COUNT:
        raise ValidationError(
            f"capture inventory rows {len(rows)} != {EXPECTED_CAPTURE_FILE_COUNT}"
        )
    if sum(int(row["size"]) for row in rows) != EXPECTED_CAPTURE_BYTES:
        raise ValidationError("capture inventory byte census changed")
    fresh = enumerate_capture_paths(root)
    inventory_keys = {row["relative_path"].casefold() for row in rows}
    if set(fresh) != inventory_keys:
        raise ValidationError("fresh capture path set differs from input inventory")
    result = []
    for row in rows:
        relative = row["relative_path"]
        path = fresh[relative.casefold()]
        result.append(
            CaptureInput(
                relative_path=relative,
                path=path,
                size=int(row["size"]),
                sha256=row["sha256"].lower(),
            )
        )
    return result


def verify_capture_inputs(inputs: list[CaptureInput]) -> None:
    for item in inputs:
        stat = item.path.stat()
        if stat.st_size != item.size or sha256_file(item.path) != item.sha256:
            raise ValidationError(f"capture input changed: {item.relative_path}")


# Embedded image VAs are 6-8 hex digits; numeric tags (0x2A) and small member
# offsets (+0x14) are 2-3 digits and are deliberately NOT matched.
FIELD_OFFSET_VA_PATTERN = re.compile(r"0x[0-9A-Fa-f]{6,8}")

# The only closed (message, order) pairs whose W/R legs legitimately differ
# byte-for-byte, because the two legs embed direction-specific VAs (subcall
# targets, stack anchors: e.g. TargetPosVital SUBCALL:0x005F3490 W vs
# SUBCALL:0x005F34D0 R).  Measured once against the pristine deliverable
# (PF_SERIALIZER_FIELDS.tsv sha256 99282BDF...B5C123): exactly these 40
# pairs; every other closed pair mirrors exactly.  A pair not listed here
# must match byte-for-byte, so a one-leg edit of an embedded VA cannot be
# laundered by VA normalization.
VA_DEPENDENT_MIRROR_PAIRS = frozenset(
    (message, order)
    for message, orders in (
        ("ActionItemVital", (8, 9, 10, 11, 17, 18, 19, 20)),
        ("ActionPickVital", (8, 9, 10, 11, 15, 16, 17, 18)),
        ("ActionVital", (7, 8, 9, 10)),
        ("CKnockdownVital", (4, 5, 6, 7)),
        ("ForcePos", (1, 2, 3, 4)),
        ("RunFxSetVital", (2, 3, 4, 5)),
        ("TargetPosVital", (1, 2, 3, 4)),
        ("TriggerVital", (3, 4, 5, 6)),
    )
    for order in orders
)
# Frozen census of the pristine deliverable, same philosophy as the
# EXPECTED_* pins above: a mutation that flips a message into or out of
# static_open (e.g. field_offset "+0x14" -> "UNKNOWN(+0x99)") changes these
# counts and must turn the run red instead of silently shrinking the
# mirror-guarded set.
EXPECTED_STATIC_OPEN_MESSAGES = 181
EXPECTED_CLOSED_MIRROR_PAIRS = 859
# sha256 of "\n".join(sorted(static_open)): the counts above freeze only the
# CARDINALITY of the two sets; this digest freezes the MEMBERSHIP, so a
# coordinated swap that flips one message out of static_open and an
# equal-pair-count message in (keeping 181 and 859 both true) still goes red.
EXPECTED_STATIC_OPEN_MEMBERSHIP_SHA256 = (
    "99c561abd709626de6d18b227c40fba0853cb73a53ba2cbae4a6b1773498e13b"
)


def normalize_leg_value(value: str) -> str:
    return FIELD_OFFSET_VA_PATTERN.sub("VA", value)


def validate_field_offset_mirror(
    field_rows: list[dict[str, str]],
    static_open: set[str],
) -> None:
    """Reject one-leg corruption of A2 evidence columns on closed messages.

    Measured invariant on the pristine A2 table (2026-08-24, 6,931 rows):
    every message not in static_open has identical W and R order sets
    (338 messages, 859 pairs), and for each pair field_offset, tag,
    span_start and span_end mirror byte-for-byte except for the 40
    VA_DEPENDENT_MIRROR_PAIRS, which mirror after VA normalization; len and
    span_sha256 mirror byte-for-byte on all 859 pairs.  A mutation applied
    to a single leg (the GT-047 job-3 case: TargetPosVital:W:1 field_offset
    +0x14 -> +0x99) breaks the mirror and is refused before any capture
    frame is parsed.  Not guarded here: gate_condition and file_off_claim
    (their legs legitimately differ beyond VA structure), symmetric
    both-leg mutations, and embedded-VA edits inside the 40 pinned pairs;
    span content integrity is independently bound by span_sha256 (raw
    mirror here, image verification by GT-054).
    """
    if len(static_open) != EXPECTED_STATIC_OPEN_MESSAGES:
        raise ValidationError(
            "static-open message census is %d, expected %d"
            % (len(static_open), EXPECTED_STATIC_OPEN_MESSAGES)
        )
    membership_digest = hashlib.sha256(
        "\n".join(sorted(static_open)).encode("utf-8")
    ).hexdigest()
    if membership_digest != EXPECTED_STATIC_OPEN_MEMBERSHIP_SHA256:
        raise ValidationError(
            "static-open membership digest mismatch: %s" % membership_digest
        )
    closed_orders: dict[str, dict[str, set[int]]] = defaultdict(
        lambda: defaultdict(set)
    )
    legs: dict[tuple[str, int], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in field_rows:
        message = row["message"]
        if message in static_open:
            continue
        direction = row["direction(W/R)"]
        order = int(row["order"])
        closed_orders[message][direction].add(order)
        legs[(message, order)][direction] = row
    for message, directions in closed_orders.items():
        if directions["W"] != directions["R"]:
            raise ValidationError(
                f"W/R order sets differ for closed message {message}"
            )
    pair_count = 0
    for (message, order), directions in legs.items():
        w_row = directions.get("W")
        r_row = directions.get("R")
        if w_row is None or r_row is None:
            continue
        pair_count += 1
        va_dependent = (message, order) in VA_DEPENDENT_MIRROR_PAIRS
        for column in ("field_offset", "tag", "span_start", "span_end"):
            w_value = w_row[column]
            r_value = r_row[column]
            if w_value == r_value:
                continue
            if va_dependent and normalize_leg_value(
                w_value
            ) == normalize_leg_value(r_value):
                continue
            raise ValidationError(
                f"W/R {column} mirror broken for {message} order {order}"
            )
        for column in ("len", "span_sha256"):
            if w_row[column] != r_row[column]:
                raise ValidationError(
                    f"W/R {column} mirror broken for {message} order {order}"
                )
    if pair_count != EXPECTED_CLOSED_MIRROR_PAIRS:
        raise ValidationError(
            "closed mirror pair census is %d, expected %d"
            % (pair_count, EXPECTED_CLOSED_MIRROR_PAIRS)
        )


def build_schemas(
    registry_rows: list[dict[str, str]],
    field_rows: list[dict[str, str]],
    tag_census_rows: list[dict[str, str]],
) -> tuple[
    dict[int, str],
    dict[tuple[str, str], list[SchemaField]],
    set[str],
]:
    if len(registry_rows) != EXPECTED_PROTOCOL_COUNT:
        raise ValidationError("registry census is not 519")
    if Counter(row.get("source", "") for row in registry_rows) != Counter(
        {"IMAGE": len(registry_rows)}
    ):
        raise ValidationError("registry does not contain only source=IMAGE")
    if Counter(row.get("source", "") for row in field_rows) != Counter(
        {"IMAGE": len(field_rows)}
    ):
        raise ValidationError("A2 does not contain only source=IMAGE")
    if Counter(row.get("source", "") for row in tag_census_rows) != Counter(
        {"IMAGE": len(tag_census_rows)}
    ):
        raise ValidationError("A3 does not contain only source=IMAGE")
    numeric_census: dict[str, tuple[int, int]] = {}
    for row in tag_census_rows:
        tag = row["tag"]
        if not re.fullmatch(r"0x[0-9A-F]{2}", tag):
            continue
        if tag in numeric_census:
            raise ValidationError(f"duplicate A3 numeric tag {tag}")
        if row["len_status_for_tag"] != "FIXED" or not row["len"].isdigit():
            raise ValidationError(f"A3 numeric tag {tag} lacks a fixed length")
        numeric_census[tag] = (
            int(row["len"]),
            int(row["frequency_in_A2"]),
        )
    numeric_frequencies: Counter[str] = Counter()
    id_to_name: dict[int, str] = {}
    for row in registry_rows:
        message_id = protocol_id(row["name"])
        if message_id in id_to_name:
            raise ValidationError(
                f"protocol ID collision: {row['name']} / {id_to_name[message_id]}"
            )
        id_to_name[message_id] = row["name"]
    schemas: dict[tuple[str, str], list[SchemaField]] = defaultdict(list)
    static_open: set[str] = set()
    for row in field_rows:
        direction = row["direction(W/R)"]
        if direction not in ("W", "R"):
            raise ValidationError("invalid A2 direction")
        schemas[(row["message"], direction)].append(
            SchemaField(
                order=int(row["order"]), tag=row["tag"], length=row["len"]
            )
        )
        tag = row["tag"]
        length = row["len"]
        if re.fullmatch(r"0x[0-9A-F]{2}", tag):
            numeric_frequencies[tag] += 1
            expected = numeric_census.get(tag)
            if expected is None or not row["len"].isdigit():
                raise ValidationError(
                    f"A2 numeric tag {tag} lacks an A3 length oracle"
                )
            if int(length) != expected[0]:
                raise ValidationError(
                    f"A2/A3 length mismatch for {tag}: "
                    f"{length} != {expected[0]}"
                )
        elif tag in STRING_TAGS:
            if length != "4+N_bytes":
                raise ValidationError(f"A2 string tag {tag} has length {length}")
        elif tag in ZERO_LENGTH_NONWIRE_TAGS:
            if length != "0":
                raise ValidationError(f"A2 zero-byte tag {tag} has length {length}")
        elif length != "N/A":
            raise ValidationError(f"A2 non-wire tag {tag} has length {length}")
        if row["tag"] == "UNKNOWN" or "UNKNOWN(" in row["field_offset"]:
            static_open.add(row["message"])
    for key, fields in schemas.items():
        fields.sort(key=lambda value: value.order)
        orders = [value.order for value in fields]
        if orders != list(range(1, len(fields) + 1)):
            raise ValidationError(f"non-contiguous A2 order for {key}")
    if {row["name"] for row in registry_rows} != {name for name, _direction in schemas}:
        raise ValidationError("registry/A2 message sets differ")
    if {
        tag: numeric_frequencies[tag] for tag in numeric_census
    } != {
        tag: frequency for tag, (_length, frequency) in numeric_census.items()
    }:
        raise ValidationError("A2/A3 numeric frequency census differs")
    validate_field_offset_mirror(field_rows, static_open)
    return id_to_name, schemas, static_open


def parse_schema(
    data: bytes,
    start: int,
    fields: list[SchemaField],
    is_static_open: bool,
) -> SchemaResult:
    if is_static_open:
        return SchemaResult("STATIC_OPEN", start)
    position = start
    for schema_field in fields:
        tag = schema_field.tag
        if tag in ZERO_LENGTH_NONWIRE_TAGS or tag.startswith("SUBCALL:"):
            continue
        if re.fullmatch(r"0x[0-9A-F]{2}", tag):
            if not schema_field.length.isdigit():
                raise ValidationError(
                    f"numeric A2 field {tag} has non-fixed length {schema_field.length}"
                )
            if position >= len(data):
                return SchemaResult(
                    "MISMATCH", position, schema_field.order, "TRUNCATED_TAG"
                )
            expected_tag = int(tag, 16)
            if data[position] != expected_tag:
                return SchemaResult(
                    "MISMATCH", position, schema_field.order, "TAG"
                )
            end = position + 1 + int(schema_field.length)
            if end > len(data):
                return SchemaResult(
                    "MISMATCH", position, schema_field.order, "TRUNCATED_VALUE"
                )
            position = end
            continue
        if tag in STRING_TAGS:
            if position >= len(data):
                return SchemaResult(
                    "MISMATCH", position, schema_field.order, "TRUNCATED_STRING_TAG"
                )
            if data[position] != STRING_TAGS[tag]:
                return SchemaResult(
                    "MISMATCH", position, schema_field.order, "STRING_TAG"
                )
            if position + 5 > len(data):
                return SchemaResult(
                    "MISMATCH", position, schema_field.order, "TRUNCATED_STRING_LENGTH"
                )
            byte_length = int.from_bytes(data[position + 1 : position + 5], "little")
            if tag == "UNTAGGED_WSTRING16LE_LEN32LE" and byte_length % 2:
                return SchemaResult(
                    "MISMATCH", position, schema_field.order, "ODD_UTF16_BYTE_LENGTH"
                )
            end = position + 5 + byte_length
            if end > len(data):
                return SchemaResult(
                    "MISMATCH", position, schema_field.order, "TRUNCATED_STRING_PAYLOAD"
                )
            position = end
            continue
        raise ValidationError(f"unsupported closed A2 tag {tag}")
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
            if not tokens or any(not re.fullmatch(r"[0-9A-Fa-f]{2}", token) for token in tokens):
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
    elif outcome.status == "STATIC_OPEN":
        aggregate.static_open_instances += 1
        aggregate.static_open_frames.add(frame_key)
    elif outcome.status == "MISMATCH":
        aggregate.mismatch_instances += 1
        aggregate.mismatch_frames.add(frame_key)
        aggregate.mismatch_points[(outcome.field_index, outcome.reason)] += 1
    else:
        raise ValidationError(f"unexpected schema outcome {outcome.status}")


def parse_capture_frame(
    data: bytes,
    direction: str,
    frame_key: str,
    file_key: str,
    id_to_name: dict[int, str],
    schemas: dict[tuple[str, str], list[SchemaField]],
    static_open: set[str],
    aggregates: dict[tuple[str, str], MessageAggregate],
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
    outer_result = parse_schema(
        data,
        3,
        schemas[(outer_name, direction)],
        outer_name in static_open,
    )
    record_outcome(
        aggregates[(outer_name, direction)], frame_key, file_key, outer_result
    )

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
        if position + 5 > len(data) or data[position] != 0x12 or data[position + 3] != 0x0B:
            counts.block_errors["VITAL_WRAPPER_STRUCTURE"] += 1
            counts.nested_unresolved_after_open += vital_count - vital_index
            stopped = True
            break
        vital_id = int.from_bytes(data[position + 1 : position + 3], "little")
        vital_name = id_to_name.get(vital_id)
        if vital_name is None:
            counts.unknown_message_id_instances += 1
            counts.nested_unresolved_after_open += vital_count - vital_index
            stopped = True
            break
        position += 5
        counts.nested_reached_instances += 1
        result = parse_schema(
            data,
            position,
            schemas[(vital_name, direction)],
            vital_name in static_open,
        )
        record_outcome(
            aggregates[(vital_name, direction)], frame_key, file_key, result
        )
        if result.status == "PASS":
            counts.validated_nested_frames.add(frame_key)
            position = result.end
            continue
        if result.status == "STATIC_OPEN":
            counts.static_open_nested_frames.add(frame_key)
        else:
            counts.mismatch_nested_frames.add(frame_key)
        counts.nested_unresolved_after_open += vital_count - vital_index - 1
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
        # This is outer framing beyond the nested A2 message, so it is reported
        # separately and is never converted into a nested-field mismatch.
        counts.framing_unresolved_frames += 1


def validate_parser_regressions() -> None:
    fields = [
        SchemaField(1, "0x26", "4"),
        SchemaField(2, "0x1F", "4"),
        SchemaField(3, "UNTAGGED_STRING8_LEN32LE", "4+N_bytes"),
        SchemaField(4, "0x12", "2"),
    ]
    good = bytes(
        (
            0x26,
            1,
            2,
            3,
            4,
            0x1F,
            5,
            6,
            7,
            8,
            0x44,
            2,
            0,
            0,
            0,
            65,
            66,
            0x12,
            3,
            0,
        )
    )
    passed = parse_schema(good, 0, fields, False)
    if passed.status != "PASS" or passed.end != len(good):
        raise ValidationError("parser positive regression failed")
    mutated = bytearray(good)
    mutated[5] = 0x26
    rejected = parse_schema(bytes(mutated), 0, fields, False)
    if (rejected.status, rejected.field_index, rejected.reason) != (
        "MISMATCH",
        2,
        "TAG",
    ):
        raise ValidationError("parser 0x1F mutation was not rejected at field 2")
    string_mutation = bytearray(good)
    string_mutation[10] = 0x48
    rejected_string = parse_schema(bytes(string_mutation), 0, fields, False)
    if (rejected_string.status, rejected_string.field_index, rejected_string.reason) != (
        "MISMATCH",
        3,
        "STRING_TAG",
    ):
        raise ValidationError("parser string mutation was not rejected at field 3")
    truncated = parse_schema(good[:-1], 0, fields, False)
    if (truncated.status, truncated.field_index) != ("MISMATCH", 4):
        raise ValidationError("parser truncation mutation was not rejected at field 4")
    if parse_schema(good, 0, fields, True).status != "STATIC_OPEN":
        raise ValidationError("static-open regression failed")
    zero_fields = [
        SchemaField(1, "EMPTY", "0"),
        SchemaField(
            2, "PURE_READONLY_CHAIN_PLUS_04_CONTAINS_PREDICATE", "0"
        ),
    ]
    zero_result = parse_schema(b"", 0, zero_fields, False)
    if zero_result.status != "PASS" or zero_result.end != 0:
        raise ValidationError("zero-length non-wire regression failed")


def validate_schema_mutation_regressions(
    registry_rows: list[dict[str, str]],
    field_rows: list[dict[str, str]],
    tag_census_rows: list[dict[str, str]],
) -> None:
    mutated_fields = [dict(row) for row in field_rows]
    field_26 = next(row for row in mutated_fields if row["tag"] == "0x26")
    field_26["len"] = "8"
    try:
        build_schemas(registry_rows, mutated_fields, tag_census_rows)
    except ValidationError:
        pass
    else:
        raise ValidationError("A2 0x26 length mutation was unexpectedly accepted")

    mutated_census = [dict(row) for row in tag_census_rows]
    census_1f = next(row for row in mutated_census if row["tag"] == "0x1F")
    census_1f["len"] = "8"
    try:
        build_schemas(registry_rows, field_rows, mutated_census)
    except ValidationError:
        pass
    else:
        raise ValidationError("A3 0x1F length mutation was unexpectedly accepted")

    length_mutations = (
        ("UNTAGGED_STRING8_LEN32LE", "0"),
        ("UNTAGGED_WSTRING16LE_LEN32LE", "999"),
        ("EMPTY", "999"),
        ("PURE_READONLY_CHAIN_PLUS_04_CONTAINS_PREDICATE", "N/A"),
    )
    for tag, bad_length in length_mutations:
        mutated = [dict(row) for row in field_rows]
        target = next(row for row in mutated if row["tag"] == tag)
        target["len"] = bad_length
        try:
            build_schemas(registry_rows, mutated, tag_census_rows)
        except ValidationError:
            pass
        else:
            raise ValidationError(
                f"A2 {tag} length mutation was unexpectedly accepted"
            )

    mutated_subcall = [dict(row) for row in field_rows]
    subcall = next(row for row in mutated_subcall if row["tag"].startswith("SUBCALL:"))
    subcall["len"] = "0"
    try:
        build_schemas(registry_rows, mutated_subcall, tag_census_rows)
    except ValidationError:
        pass
    else:
        raise ValidationError("A2 SUBCALL length mutation was unexpectedly accepted")

    # GT-047 job 3: the exact mutation the 2026-08-23 tester run proved was
    # silently accepted (TargetPosVital:W:1 field_offset +0x14 -> +0x99).
    # The fixture value is asserted first so silent drift of the deliverable
    # cannot turn this self-test into a no-op.
    mutated_offset = [dict(row) for row in field_rows]
    target_pos_w1 = next(
        row
        for row in mutated_offset
        if row["message"] == "TargetPosVital"
        and row["direction(W/R)"] == "W"
        and row["order"] == "1"
    )
    if target_pos_w1["field_offset"] != "+0x14":
        raise ValidationError(
            "A2 TargetPosVital:W:1 fixture drifted from +0x14"
        )
    target_pos_w1["field_offset"] = "+0x99"
    try:
        build_schemas(registry_rows, mutated_offset, tag_census_rows)
    except ValidationError:
        pass
    else:
        raise ValidationError(
            "A2 W-leg field_offset mutation was unexpectedly accepted"
        )

    mutated_offset_r = [dict(row) for row in field_rows]
    target_pos_r5 = next(
        row
        for row in mutated_offset_r
        if row["message"] == "TargetPosVital"
        and row["direction(W/R)"] == "R"
        and row["order"] == "5"
    )
    if target_pos_r5["field_offset"] != "+0x20":
        raise ValidationError(
            "A2 TargetPosVital:R:5 fixture drifted from +0x20"
        )
    target_pos_r5["field_offset"] = "+0x77"
    try:
        build_schemas(registry_rows, mutated_offset_r, tag_census_rows)
    except ValidationError:
        pass
    else:
        raise ValidationError(
            "A2 R-leg field_offset mutation was unexpectedly accepted"
        )

    # A field_offset corruption that embeds "UNKNOWN(" must not evade the
    # mirror by silently flipping the message into the static_open skip set.
    mutated_flip = [dict(row) for row in field_rows]
    flip_row = next(
        row
        for row in mutated_flip
        if row["message"] == "TargetPosVital"
        and row["direction(W/R)"] == "W"
        and row["order"] == "1"
    )
    flip_row["field_offset"] = "UNKNOWN(+0x99)"
    try:
        build_schemas(registry_rows, mutated_flip, tag_census_rows)
    except ValidationError:
        pass
    else:
        raise ValidationError(
            "A2 static-open flip mutation was unexpectedly accepted"
        )

    # One-leg edit of an embedded VA on a pair NOT in
    # VA_DEPENDENT_MIRROR_PAIRS must be caught by the raw comparison.
    mutated_va = [dict(row) for row in field_rows]
    relive_w1 = next(
        row
        for row in mutated_va
        if row["message"] == "ReliveVital"
        and row["direction(W/R)"] == "W"
        and row["order"] == "1"
    )
    if relive_w1["field_offset"] != "STACK@0x005E5F80+0x14":
        raise ValidationError(
            "A2 ReliveVital:W:1 fixture drifted from STACK@0x005E5F80+0x14"
        )
    relive_w1["field_offset"] = "STACK@0x00DEADBE+0x14"
    try:
        build_schemas(registry_rows, mutated_va, tag_census_rows)
    except ValidationError:
        pass
    else:
        raise ValidationError(
            "A2 one-leg embedded-VA mutation was unexpectedly accepted"
        )

    # One-leg span_sha256 tamper must be caught by the raw mirror.
    mutated_span = [dict(row) for row in field_rows]
    span_row = next(
        row
        for row in mutated_span
        if row["message"] == "TargetPosVital"
        and row["direction(W/R)"] == "W"
        and row["order"] == "1"
    )
    span_row["span_sha256"] = "0" * 64
    try:
        build_schemas(registry_rows, mutated_span, tag_census_rows)
    except ValidationError:
        pass
    else:
        raise ValidationError(
            "A2 one-leg span_sha256 mutation was unexpectedly accepted"
        )

    # Membership swap: flip Activity_BasicVital (1 unresolved pair) OUT of
    # static_open and Attribute (1 closed pair) IN.  Both census counts stay
    # at 181/859; only the membership digest can catch this.
    mutated_membership = [dict(row) for row in field_rows]
    basic_rows = [
        row
        for row in mutated_membership
        if row["message"] == "Activity_BasicVital"
    ]
    if len(basic_rows) != 2 or not all(
        "UNKNOWN(" in row["field_offset"] for row in basic_rows
    ):
        raise ValidationError("A2 Activity_BasicVital fixture drifted")
    for row in basic_rows:
        row["tag"] = "EMPTY"
        row["field_offset"] = "N/A"
        row["len"] = "0"
    attribute_w1 = next(
        row
        for row in mutated_membership
        if row["message"] == "Attribute" and row["direction(W/R)"] == "W"
    )
    if attribute_w1["field_offset"] != "N/A":
        raise ValidationError("A2 Attribute:W:1 fixture drifted from N/A")
    attribute_w1["field_offset"] = "UNKNOWN(+0x99)"
    try:
        build_schemas(registry_rows, mutated_membership, tag_census_rows)
    except ValidationError:
        pass
    else:
        raise ValidationError(
            "A2 static-open membership swap was unexpectedly accepted"
        )


def run_count_values(
    counts: RunCounts,
    aggregates: dict[tuple[str, str], MessageAggregate],
) -> dict[str, int]:
    return {
        "capture_text_files": counts.capture_text_files,
        "files_with_blocks": len(counts.files_with_blocks),
        "pc_blocks": counts.pc_blocks,
        "decompressed_blocks": counts.decompressed_blocks,
        "block_errors": sum(counts.block_errors.values()),
        "outer_instances": counts.outer_instances,
        "nested_declared": counts.nested_declared_instances,
        "nested_reached": counts.nested_reached_instances,
        "nested_unresolved": counts.nested_unresolved_after_open,
        "unknown_message_ids": counts.unknown_message_id_instances,
        "no_runtime_tail_frames": counts.no_runtime_tail_frames,
        "runtime_zero_tail_frames": counts.runtime_zero_tail_frames,
        "framing_unresolved_frames": counts.framing_unresolved_frames,
        "validated_nested_frames": len(counts.validated_nested_frames),
        "static_open_nested_frames": len(counts.static_open_nested_frames),
        "mismatch_nested_frames": len(counts.mismatch_nested_frames),
        "pass_instances": sum(value.pass_instances for value in aggregates.values()),
        "static_open_instances": sum(
            value.static_open_instances for value in aggregates.values()
        ),
        "mismatch_instances": sum(
            value.mismatch_instances for value in aggregates.values()
        ),
    }


EXPECTED_RUN_COUNTS = {
    "capture_text_files": EXPECTED_CAPTURE_TEXT_FILES,
    "files_with_blocks": EXPECTED_FILES_WITH_BLOCKS,
    "pc_blocks": EXPECTED_PC_BLOCKS,
    "decompressed_blocks": EXPECTED_DECOMPRESSED_BLOCKS,
    "block_errors": 0,
    "outer_instances": EXPECTED_OUTER_INSTANCES,
    "nested_declared": EXPECTED_NESTED_DECLARED,
    "nested_reached": EXPECTED_NESTED_REACHED,
    "nested_unresolved": EXPECTED_NESTED_UNRESOLVED,
    "unknown_message_ids": 0,
    "no_runtime_tail_frames": EXPECTED_NO_RUNTIME_TAIL_FRAMES,
    "runtime_zero_tail_frames": EXPECTED_RUNTIME_ZERO_TAIL_FRAMES,
    "framing_unresolved_frames": EXPECTED_FRAMING_UNRESOLVED_FRAMES,
    "validated_nested_frames": EXPECTED_VALIDATED_NESTED_FRAMES,
    "static_open_nested_frames": EXPECTED_STATIC_OPEN_NESTED_FRAMES,
    "mismatch_nested_frames": EXPECTED_MISMATCH_NESTED_FRAMES,
    "pass_instances": EXPECTED_PASS_INSTANCES,
    "static_open_instances": EXPECTED_STATIC_OPEN_INSTANCES,
    "mismatch_instances": EXPECTED_MISMATCH_INSTANCES,
}


def validate_run_counts_values(values: dict[str, int]) -> None:
    if values["pc_blocks"] + values["decompressed_blocks"] != values["outer_instances"]:
        raise ValidationError("A5 direction/outer accounting does not balance")
    if values["nested_reached"] + values["nested_unresolved"] != values["nested_declared"]:
        raise ValidationError("A5 nested accounting does not balance")
    if values != EXPECTED_RUN_COUNTS:
        changed = {
            key: (EXPECTED_RUN_COUNTS[key], values.get(key))
            for key in EXPECTED_RUN_COUNTS
            if values.get(key) != EXPECTED_RUN_COUNTS[key]
        }
        raise ValidationError(f"A5 frozen semantic census changed: {changed}")


def validate_run_counts(
    counts: RunCounts,
    aggregates: dict[tuple[str, str], MessageAggregate],
) -> None:
    values = run_count_values(counts, aggregates)
    validate_run_counts_values(values)
    for label, key in (
        ("direction", "pc_blocks"),
        ("message ID", "unknown_message_ids"),
        ("envelope", "block_errors"),
        ("outer", "outer_instances"),
        ("nested", "nested_declared"),
        ("tail", "runtime_zero_tail_frames"),
        ("mismatch", "mismatch_instances"),
    ):
        mutated = dict(values)
        mutated[key] += 1
        try:
            validate_run_counts_values(mutated)
        except ValidationError:
            pass
        else:
            raise ValidationError(
                f"A5 {label} census mutation was unexpectedly accepted"
            )


def tsv_text(headers: list[str], rows: list[list[str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return stream.getvalue()


def output_status(aggregate: MessageAggregate) -> str:
    if aggregate.observed_instances == 0:
        return "NOT_OBSERVED"
    if aggregate.mismatch_instances:
        return "MISMATCH"
    if aggregate.static_open_instances:
        return "A2_STATIC_OPEN"
    return "VALIDATED"


def build_outputs(
    registry_rows: list[dict[str, str]],
    aggregates: dict[tuple[str, str], MessageAggregate],
    counts: RunCounts,
    capture_inputs: list[CaptureInput],
    registry_sha256: str,
    fields_sha256: str,
    tag_census_sha256: str,
    inventory_sha256: str,
) -> tuple[str, str]:
    rows: list[list[str]] = []
    for registry_row in registry_rows:
        name = registry_row["name"]
        for direction in ("W", "R"):
            aggregate = aggregates[(name, direction)]
            point_text = " | ".join(
                f"{index}:{reason}:{occurrences}"
                for (index, reason), occurrences in sorted(
                    aggregate.mismatch_points.items()
                )
            )
            rows.append(
                [
                    name,
                    direction,
                    str(len(aggregate.observed_frames)),
                    str(aggregate.observed_instances),
                    str(len(aggregate.pass_frames)),
                    str(aggregate.pass_instances),
                    str(len(aggregate.static_open_frames)),
                    str(aggregate.static_open_instances),
                    str(len(aggregate.mismatch_frames)),
                    str(aggregate.mismatch_instances),
                    point_text or "NONE",
                    str(len(aggregate.capture_files)),
                    output_status(aggregate),
                    SOURCE,
                ]
            )
    headers = [
        "message",
        "direction(W/R)",
        "observed_frames",
        "observed_instances",
        "parse_success_frames",
        "parse_success_instances",
        "a2_static_open_frames",
        "a2_static_open_instances",
        "mismatch_frames",
        "mismatch_instances",
        "mismatch_field_index_reason_count",
        "capture_file_count",
        "status",
        "source",
    ]
    output_tsv = tsv_text(headers, rows)
    validate_output_tsv(output_tsv, registry_rows, aggregates)
    validate_output_mutation_regressions(output_tsv, registry_rows, aggregates)

    mismatch_instances = sum(
        aggregate.mismatch_instances for aggregate in aggregates.values()
    )
    mismatch_points = {
        (name, direction, field_index, reason)
        for (name, direction), aggregate in aggregates.items()
        for field_index, reason in aggregate.mismatch_points
    }
    pass_instances = sum(aggregate.pass_instances for aggregate in aggregates.values())
    static_open_instances = sum(
        aggregate.static_open_instances for aggregate in aggregates.values()
    )
    observed_rows = [
        (name, direction, aggregate)
        for (name, direction), aggregate in aggregates.items()
        if aggregate.observed_instances
    ]
    lines: list[str] = []
    if mismatch_points:
        lines.extend(
            [
                "# 🔴 พบ A5 static/capture mismatch",
                "",
                f"พบ {len(mismatch_points)} จุด ({mismatch_instances} instance) รายละเอียด field index อยู่ใน TSV; ตาราง A2 ไม่ถูกแก้ให้เข้ากับ capture",
                "",
            ]
        )
    else:
        lines.extend(["# PF field validation", ""])
    lines.extend(
        [
            "ผลนี้เป็น `source=CAPTURE` แยกจากตาราง A2 `source=IMAGE` และไม่ส่งออก payload, ค่า field หรือ hexdump แม้แต่ไบต์เดียว",
            "",
            "## Coverage",
            "",
            f"- capture files hashed/scanned: {len(capture_inputs)} ({sum(item.size for item in capture_inputs)} bytes)",
            f"- text files inspected for PC blocks: {counts.capture_text_files}",
            f"- files containing blocks: {len(counts.files_with_blocks)}",
            f"- PC blocks: {counts.pc_blocks}; DECOMPRESSED blocks: {counts.decompressed_blocks}; total: {counts.pc_blocks + counts.decompressed_blocks}",
            f"- capture block/envelope errors: {sum(counts.block_errors.values())}",
            f"- outer message instances: {counts.outer_instances}",
            f"- nested instances declared by collection counts: {counts.nested_declared_instances}",
            f"- nested instances reached without heuristic scanning: {counts.nested_reached_instances}",
            f"- nested instances after a static-open boundary and therefore deliberately not guessed: {counts.nested_unresolved_after_open}",
            "",
            "## A2 comparison",
            "",
            f"- parse success: {pass_instances} message instances",
            f"- A2 static-open (not counted as mismatch): {static_open_instances} message instances",
            f"- mismatch: {mismatch_instances} instances, {len(mismatch_points)} distinct message/direction/field/reason point(s)",
            f"- nested frames with at least one successful validation: {len(counts.validated_nested_frames)}",
            f"- nested frames reaching a static-open message: {len(counts.static_open_nested_frames)}",
            f"- nested frames with a field mismatch: {len(counts.mismatch_nested_frames)}",
            "",
            "## Framing kept separate from A2 fields",
            "",
            f"- collection ended with no extra tail: {counts.no_runtime_tail_frames} frame(s)",
            f"- `GSCN_RunTimeProtocolRes` collection ended with its exact zero derived change-mask: {counts.runtime_zero_tail_frames} frame(s)",
            f"- other outer framing left unresolved: {counts.framing_unresolved_frames} frame(s)",
            "- The runtime-response change-mask follows the complete VitalData collection. It is not assigned to the last nested message and therefore cannot create a false A2 mismatch.",
            "",
            "## Observed messages",
            "",
            "| message | dir | frames | instances | pass | static-open | mismatch |",
            "|---|:---:|---:|---:|---:|---:|---:|",
        ]
    )
    for name, direction, aggregate in sorted(observed_rows):
        lines.append(
            "| `%s` | %s | %d | %d | %d | %d | %d |"
            % (
                name,
                direction,
                len(aggregate.observed_frames),
                aggregate.observed_instances,
                aggregate.pass_instances,
                aggregate.static_open_instances,
                aggregate.mismatch_instances,
            )
        )
    lines.extend(
        [
            "",
            "## Evidence bindings",
            "",
            f"- PF_INPUT_INVENTORY.tsv SHA-256: `{inventory_sha256}`",
            f"- PF_PROTOCOL_REGISTRY.tsv SHA-256: `{registry_sha256}`",
            f"- PF_SERIALIZER_FIELDS.tsv SHA-256: `{fields_sha256}`",
            f"- PF_TAG_CENSUS.tsv SHA-256: `{tag_census_sha256}`",
            "- Direction mapping: `DECOMPRESSED` = client serializer W; `PC` = client serializer R.",
            "- Message IDs are resolved with the collision-free 16-bit registry-name algorithm over the frozen 519-name census; no proximity/string guess is used.",
            "- `UNTAGGED_*_LEN32LE` A2 rows are validated through their stream primitive tags (`0x44` string8, `0x48` wstring16) plus uint32 byte length, without exporting the length or contents.",
            "",
        ]
    )
    output_md = "\n".join(lines)
    if RAW_BYTE_RUN_RE.search(output_md):
        raise ValidationError("A5 Markdown raw-byte export guard fired")
    return output_tsv, output_md


def validate_output_tsv(
    output_tsv: str,
    registry_rows: list[dict[str, str]],
    aggregates: dict[tuple[str, str], MessageAggregate],
) -> None:
    parsed = list(csv.DictReader(io.StringIO(output_tsv), delimiter="\t"))
    expected_headers = [
        "message",
        "direction(W/R)",
        "observed_frames",
        "observed_instances",
        "parse_success_frames",
        "parse_success_instances",
        "a2_static_open_frames",
        "a2_static_open_instances",
        "mismatch_frames",
        "mismatch_instances",
        "mismatch_field_index_reason_count",
        "capture_file_count",
        "status",
        "source",
    ]
    if len(parsed) != EXPECTED_PROTOCOL_COUNT * 2:
        raise ValidationError("A5 output must contain 519 x 2 direction rows")
    if list(parsed[0]) != expected_headers:
        raise ValidationError("A5 output header contract changed")
    if Counter(row["source"] for row in parsed) != Counter(
        {SOURCE: EXPECTED_PROTOCOL_COUNT * 2}
    ):
        raise ValidationError("A5 output violates source=CAPTURE")
    expected_keys = {
        (row["name"], direction)
        for row in registry_rows
        for direction in ("W", "R")
    }
    measured_keys = {
        (row["message"], row["direction(W/R)"]) for row in parsed
    }
    if len(measured_keys) != len(parsed) or measured_keys != expected_keys:
        raise ValidationError("A5 output message/direction key set changed")
    numeric_columns = [
        "observed_frames",
        "observed_instances",
        "parse_success_frames",
        "parse_success_instances",
        "a2_static_open_frames",
        "a2_static_open_instances",
        "mismatch_frames",
        "mismatch_instances",
        "capture_file_count",
    ]
    for row in parsed:
        try:
            values = {column: int(row[column]) for column in numeric_columns}
        except ValueError as exc:
            raise ValidationError("A5 output contains a non-integer count") from exc
        if any(value < 0 for value in values.values()):
            raise ValidationError("A5 output contains a negative count")
        observed_instances = values["observed_instances"]
        if observed_instances != (
            values["parse_success_instances"]
            + values["a2_static_open_instances"]
            + values["mismatch_instances"]
        ):
            raise ValidationError(
                f"A5 instance accounting differs for {row['message']} "
                f"{row['direction(W/R)']}"
            )
        for frame_column, instance_column in (
            ("observed_frames", "observed_instances"),
            ("parse_success_frames", "parse_success_instances"),
            ("a2_static_open_frames", "a2_static_open_instances"),
            ("mismatch_frames", "mismatch_instances"),
        ):
            if values[frame_column] > values[instance_column]:
                raise ValidationError("A5 frame count exceeds instance count")
        if values["capture_file_count"] > values["observed_frames"]:
            raise ValidationError("A5 capture file count exceeds observed frames")
        expected_status = (
            "NOT_OBSERVED"
            if observed_instances == 0
            else "MISMATCH"
            if values["mismatch_instances"]
            else "A2_STATIC_OPEN"
            if values["a2_static_open_instances"]
            else "VALIDATED"
        )
        if row["status"] != expected_status:
            raise ValidationError("A5 output status is inconsistent with counts")
        point_text = row["mismatch_field_index_reason_count"]
        if values["mismatch_instances"] == 0:
            if point_text != "NONE":
                raise ValidationError("A5 zero-mismatch row contains mismatch points")
        else:
            point_total = 0
            for point in point_text.split(" | "):
                match = re.fullmatch(r"([1-9][0-9]*):([A-Z0-9_]+):([1-9][0-9]*)", point)
                if match is None:
                    raise ValidationError("A5 mismatch point encoding is invalid")
                point_total += int(match.group(3))
            if point_total != values["mismatch_instances"]:
                raise ValidationError("A5 mismatch point counts do not balance")

        aggregate = aggregates[(row["message"], row["direction(W/R)"])]
        expected_values = {
            "observed_frames": len(aggregate.observed_frames),
            "observed_instances": aggregate.observed_instances,
            "parse_success_frames": len(aggregate.pass_frames),
            "parse_success_instances": aggregate.pass_instances,
            "a2_static_open_frames": len(aggregate.static_open_frames),
            "a2_static_open_instances": aggregate.static_open_instances,
            "mismatch_frames": len(aggregate.mismatch_frames),
            "mismatch_instances": aggregate.mismatch_instances,
            "capture_file_count": len(aggregate.capture_files),
        }
        if values != expected_values:
            raise ValidationError("A5 output differs from in-memory aggregate")
        expected_points = " | ".join(
            f"{index}:{reason}:{occurrences}"
            for (index, reason), occurrences in sorted(
                aggregate.mismatch_points.items()
            )
        ) or "NONE"
        if point_text != expected_points:
            raise ValidationError("A5 mismatch detail differs from aggregate")

    status_counts = Counter(row["status"] for row in parsed)
    if dict(status_counts) != EXPECTED_OUTPUT_STATUSES:
        raise ValidationError(f"A5 output status census changed: {dict(status_counts)}")
    if sum(int(row["observed_instances"]) > 0 for row in parsed) != EXPECTED_OBSERVED_OUTPUT_ROWS:
        raise ValidationError("A5 observed output-row census changed")
    global_counts = {
        "pass": sum(int(row["parse_success_instances"]) for row in parsed),
        "static_open": sum(int(row["a2_static_open_instances"]) for row in parsed),
        "mismatch": sum(int(row["mismatch_instances"]) for row in parsed),
    }
    if global_counts != {
        "pass": EXPECTED_PASS_INSTANCES,
        "static_open": EXPECTED_STATIC_OPEN_INSTANCES,
        "mismatch": EXPECTED_MISMATCH_INSTANCES,
    }:
        raise ValidationError(f"A5 output outcome census changed: {global_counts}")
    if RAW_BYTE_RUN_RE.search(output_tsv):
        raise ValidationError("A5 TSV raw-byte export guard fired")


def validate_output_mutation_regressions(
    output_tsv: str,
    registry_rows: list[dict[str, str]],
    aggregates: dict[tuple[str, str], MessageAggregate],
) -> None:
    rows = list(csv.DictReader(io.StringIO(output_tsv), delimiter="\t"))
    if not rows:
        raise ValidationError("A5 output mutation fixture is empty")
    headers = list(rows[0])
    observed_index = next(
        index for index, row in enumerate(rows) if int(row["observed_instances"]) > 0
    )
    mutations: list[tuple[str, int, str, str]] = [
        ("source", 0, "source", "IMAGE"),
        ("direction", 0, "direction(W/R)", "X"),
        (
            "observed count",
            observed_index,
            "observed_instances",
            str(int(rows[observed_index]["observed_instances"]) + 1),
        ),
        ("status", observed_index, "status", "NOT_OBSERVED"),
        (
            "mismatch point",
            observed_index,
            "mismatch_field_index_reason_count",
            "1:TAG:1",
        ),
    ]
    for label, row_index, column, value in mutations:
        mutated = [dict(row) for row in rows]
        mutated[row_index][column] = value
        mutated_text = tsv_text(
            headers, [[row[key] for key in headers] for row in mutated]
        )
        try:
            validate_output_tsv(mutated_text, registry_rows, aggregates)
        except ValidationError:
            pass
        else:
            raise ValidationError(f"A5 {label} mutation was unexpectedly accepted")
    raw_mutation = output_tsv + "00 11 22 33 44 55 66 77\n"
    try:
        validate_output_tsv(raw_mutation, registry_rows, aggregates)
    except ValidationError:
        pass
    else:
        raise ValidationError("A5 raw-byte mutation was unexpectedly accepted")


def atomic_publish(outputs: dict[Path, str]) -> None:
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
    args = parser.parse_args()
    root = args.game_client.resolve()
    external = args.external.resolve()
    registry_path = external / "PF_PROTOCOL_REGISTRY.tsv"
    fields_path = external / "PF_SERIALIZER_FIELDS.tsv"
    tag_census_path = external / "PF_TAG_CENSUS.tsv"
    inventory_path = external / "PF_INPUT_INVENTORY.tsv"
    derived_before = {
        path: sha256_file(path)
        for path in (registry_path, fields_path, tag_census_path, inventory_path)
    }
    registry_rows = read_tsv(registry_path)
    field_rows = read_tsv(fields_path)
    tag_census_rows = read_tsv(tag_census_path)
    id_to_name, schemas, static_open = build_schemas(
        registry_rows, field_rows, tag_census_rows
    )
    validate_parser_regressions()
    validate_schema_mutation_regressions(
        registry_rows, field_rows, tag_census_rows
    )
    capture_inputs = load_capture_inputs(root, inventory_path)
    verify_capture_inputs(capture_inputs)

    aggregates: dict[tuple[str, str], MessageAggregate] = defaultdict(
        MessageAggregate
    )
    counts = RunCounts()
    for item in capture_inputs:
        if item.path.suffix.casefold() != ".txt":
            continue
        counts.capture_text_files += 1
        text = item.path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = extract_pc_blocks(text)
        counts.block_errors.update(errors)
        if blocks:
            counts.files_with_blocks.add(item.relative_path)
        for ordinal, (kind, data) in enumerate(blocks, 1):
            if kind == "PC":
                direction = "R"
                counts.pc_blocks += 1
            else:
                direction = "W"
                counts.decompressed_blocks += 1
            frame_key = f"{item.relative_path}:{ordinal}"
            parse_capture_frame(
                data,
                direction,
                frame_key,
                item.relative_path,
                id_to_name,
                schemas,
                static_open,
                aggregates,
                counts,
            )

    validate_run_counts(counts, aggregates)
    output_tsv, output_md = build_outputs(
        registry_rows,
        aggregates,
        counts,
        capture_inputs,
        derived_before[registry_path],
        derived_before[fields_path],
        derived_before[tag_census_path],
        derived_before[inventory_path],
    )

    # A second independent path census and hash pass closes the read-only window
    # before either generated artifact is published.
    capture_inputs_after = load_capture_inputs(root, inventory_path)
    if capture_inputs_after != capture_inputs:
        raise ValidationError("capture input list changed during A5")
    verify_capture_inputs(capture_inputs_after)
    derived_after = {
        path: sha256_file(path)
        for path in (registry_path, fields_path, tag_census_path, inventory_path)
    }
    if derived_after != derived_before:
        raise ValidationError("A1/A2/A3/inventory changed during A5")
    atomic_publish(
        {
            external / "PF_FIELD_VALIDATION.tsv": output_tsv,
            external / "PF_FIELD_VALIDATION.md": output_md,
        }
    )
    mismatch_instances = sum(
        aggregate.mismatch_instances for aggregate in aggregates.values()
    )
    print(
        "capture_files=%d blocks=%d nested_declared=%d nested_reached=%d "
        "pass=%d static_open=%d mismatch=%d unresolved_after_open=%d"
        % (
            len(capture_inputs),
            counts.pc_blocks + counts.decompressed_blocks,
            counts.nested_declared_instances,
            counts.nested_reached_instances,
            sum(value.pass_instances for value in aggregates.values()),
            sum(value.static_open_instances for value in aggregates.values()),
            mismatch_instances,
            counts.nested_unresolved_after_open,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        raise SystemExit(f"ERROR: {exc}")
