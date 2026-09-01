#!/usr/bin/env python3
"""Build the additive A2/A3 string wire-tag correction.

This generator leaves the frozen V1 files untouched.  It emits only the rows whose
base A2 tag stopped at the string helper's payload boundary, plus the two missing
tag-census rows.  All claims are re-derived from the pinned IMAGE and pinned V1
tables on every run.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import tempfile
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
FIELDS_PATH = OUT_DIR / "PF_SERIALIZER_FIELDS.tsv"
PRIORITY_PATH = OUT_DIR / "PF_PROTOCOL_PRIORITY.tsv"
TAG_CENSUS_PATH = OUT_DIR / "PF_TAG_CENSUS.tsv"

DELTA_PATH = OUT_DIR / "PF_A2_STRING_WIRE_TAG_DELTA.tsv"
TAG_DELTA_PATH = OUT_DIR / "PF_A3_TAG_CENSUS_DELTA.tsv"
REPORT_PATH = OUT_DIR / "PF_A2_A3_STRING_WIRE_CORRECTION.md"

PINNED_SHA256 = {
    IMAGE_PATH: "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623",
    FIELDS_PATH: "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123",
    PRIORITY_PATH: "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55",
    TAG_CENSUS_PATH: "63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a",
}

OLD_STRING8 = "UNTAGGED_STRING8_LEN32LE"
OLD_WSTRING16 = "UNTAGGED_WSTRING16LE_LEN32LE"


HELPERS: dict[tuple[str, str], dict[str, object]] = {
    (OLD_STRING8, "W"): {
        "tag": "0x44",
        "tag_value": 0x44,
        "kind": "string8",
        "helper_va": 0x0089A6D0,
        "helper_file_off": 0x00499AD0,
        "helper_end_va": 0x0089A733,
        "helper_end_file_off": 0x00499B33,
        "helper_sha256": "a0674fb3366720314e20ef5f5dbfa010330b12a73ed4e56e6c43e9d310dce9f1",
        "tag_instruction_va": 0x0089A6F1,
        "tag_instruction_file_off": 0x00499AF1,
    },
    (OLD_STRING8, "R"): {
        "tag": "0x44",
        "tag_value": 0x44,
        "kind": "string8",
        "helper_va": 0x0089A740,
        "helper_file_off": 0x00499B40,
        "helper_end_va": 0x0089A806,
        "helper_end_file_off": 0x00499C06,
        "helper_sha256": "90c8c73b3b3c7158af57e374c694730763ab28292130b4f128a4754dec54e76a",
        "tag_instruction_va": 0x0089A75C,
        "tag_instruction_file_off": 0x00499B5C,
    },
    (OLD_WSTRING16, "W"): {
        "tag": "0x48",
        "tag_value": 0x48,
        "kind": "wstring16le",
        "helper_va": 0x0089A810,
        "helper_file_off": 0x00499C10,
        "helper_end_va": 0x0089A875,
        "helper_end_file_off": 0x00499C75,
        "helper_sha256": "08d6f27f030f3e0f1a32873d296c7f2c35a9d67f547607cf95c2900a60ffdad4",
        "tag_instruction_va": 0x0089A833,
        "tag_instruction_file_off": 0x00499C33,
    },
    (OLD_WSTRING16, "R"): {
        "tag": "0x48",
        "tag_value": 0x48,
        "kind": "wstring16le",
        "helper_va": 0x0089A880,
        "helper_file_off": 0x00499C80,
        "helper_end_va": 0x0089A95E,
        "helper_end_file_off": 0x00499D5E,
        "helper_sha256": "2f564cb5d4f68d035d9e60fa1a4a5334b0875262420851f463f3f904e22ad978",
        "tag_instruction_va": 0x0089A89C,
        "tag_instruction_file_off": 0x00499C9C,
    },
}

CALL_RE = re.compile(
    r"string_wire_call@(0x[0-9A-Fa-f]{8}) file_off=(0x[0-9A-Fa-f]{8})"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_pins() -> dict[Path, str]:
    observed = {path: sha256_file(path) for path in PINNED_SHA256}
    for path, expected in PINNED_SHA256.items():
        actual = observed[path]
        if actual != expected:
            raise RuntimeError(
                f"input hash mismatch: {path.name}: expected {expected}, got {actual}"
            )
    return observed


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fmt_va(value: int) -> str:
    return f"0x{value:08X}"


def row_key(row: Mapping[str, str]) -> str:
    stable = "\x1f".join(
        (
            row["message"],
            row["direction(W/R)"],
            row["order"],
            row["file_off_claim"],
            row["tag"],
        )
    )
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()


def tag_key(tag: str) -> str:
    return hashlib.sha256(f"A3_TAG\x1f{tag}".encode("ascii")).hexdigest()


def verify_helper_image(image: bytes) -> None:
    for proof in HELPERS.values():
        start = int(proof["helper_file_off"])
        end = int(proof["helper_end_file_off"])
        if not (0 <= start < end <= len(image)):
            raise RuntimeError("helper span is outside the pinned image")
        actual_hash = hashlib.sha256(image[start:end]).hexdigest()
        if actual_hash != proof["helper_sha256"]:
            raise RuntimeError(
                f"helper hash mismatch at {fmt_va(int(proof['helper_va']))}: {actual_hash}"
            )

        tag_off = int(proof["tag_instruction_file_off"])
        tag_va = int(proof["tag_instruction_va"])
        helper_va = int(proof["helper_va"])
        if tag_va - helper_va != tag_off - start:
            raise RuntimeError("tag instruction VA/file-offset relation is inconsistent")
        if not (start <= tag_off and tag_off + 2 <= end):
            raise RuntimeError("tag instruction is outside its helper span")

        # x86 PUSH imm8: verify the instruction without emitting proprietary bytes.
        if image[tag_off] != 0x6A or image[tag_off + 1] != proof["tag_value"]:
            raise RuntimeError(
                f"tag instruction mismatch at {fmt_va(tag_va)}"
            )


def proof_tokens(proof: Mapping[str, object], direction: str) -> tuple[str, ...]:
    return (
        f"string_wire_helper target={fmt_va(int(proof['helper_va']))}",
        f"target_file_off={fmt_va(int(proof['helper_file_off']))}",
        f"proof_end={fmt_va(int(proof['helper_end_va']))}",
        f"proof_end_file_off={fmt_va(int(proof['helper_end_file_off']))}",
        f"proof_sha256={proof['helper_sha256']}",
        f"direction={direction}",
        f"kind=basic_string<{'char' if proof['kind'] == 'string8' else 'wchar_t'}>",
        "length_prefix=uint32le payload=N_bytes",
    )


def build_delta_rows(
    base_rows: Sequence[dict[str, str]], priority: Mapping[str, int]
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for base_row_number, row in enumerate(base_rows, start=2):
        old_tag = row["tag"]
        if old_tag not in (OLD_STRING8, OLD_WSTRING16):
            continue
        direction = row["direction(W/R)"]
        if row["source"] != "IMAGE":
            raise RuntimeError(f"mixed/non-IMAGE source on base row {base_row_number}")
        proof = HELPERS.get((old_tag, direction))
        if proof is None:
            raise RuntimeError(f"unexpected string direction on base row {base_row_number}")

        gate = row["gate_condition"]
        for token in proof_tokens(proof, direction):
            if token not in gate:
                raise RuntimeError(
                    f"missing helper proof token on base row {base_row_number}: {token}"
                )
        calls = CALL_RE.findall(gate)
        if len(calls) != 1:
            raise RuntimeError(
                f"expected one string helper call on base row {base_row_number}, got {len(calls)}"
            )
        call_va, call_file_off = calls[0]
        if call_file_off.upper() != row["file_off_claim"].upper():
            raise RuntimeError(f"call/file claim mismatch on base row {base_row_number}")
        if row["len"] != "4+N_bytes":
            raise RuntimeError(f"unexpected old payload length on base row {base_row_number}")
        if row["message"] not in priority:
            raise RuntimeError(f"missing priority for {row['message']}")

        output.append(
            {
                "dedup_key": row_key(row),
                "delta_action": "CHANGED",
                "base_row_number": str(base_row_number),
                "message": row["message"],
                "direction(W/R)": direction,
                "order": row["order"],
                "field_offset": row["field_offset"],
                "original_tag": old_tag,
                "corrected_tag": str(proof["tag"]),
                "original_payload_len": row["len"],
                "corrected_full_wire_len": "5+N_bytes",
                "string_kind": str(proof["kind"]),
                "length_prefix": "uint32le_byte_count",
                "original_call_va": call_va.upper().replace("X", "x"),
                "original_call_file_off": call_file_off.upper().replace("X", "x"),
                "base_span_start": row["span_start"],
                "base_span_end": row["span_end"],
                "base_span_sha256": row["span_sha256"],
                "helper_va": fmt_va(int(proof["helper_va"])),
                "helper_file_off": fmt_va(int(proof["helper_file_off"])),
                "helper_span_end_va": fmt_va(int(proof["helper_end_va"])),
                "helper_span_end_file_off": fmt_va(int(proof["helper_end_file_off"])),
                "helper_span_sha256": str(proof["helper_sha256"]),
                "tag_instruction_va": fmt_va(int(proof["tag_instruction_va"])),
                "tag_instruction_file_off": fmt_va(
                    int(proof["tag_instruction_file_off"])
                ),
                "tag_instruction_semantics": f"push_{proof['tag']}",
                "priority": str(priority[row["message"]]),
                "source": "IMAGE",
            }
        )
    return output


def format_example(row: Mapping[str, str]) -> str:
    return (
        f"{row['message']}:{row['direction(W/R)']}:{row['order']}"
        f"@file_off={row['original_call_file_off']}"
    )


def build_tag_rows(delta_rows: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for tag, kind, old_tag in (
        ("0x44", "string8", OLD_STRING8),
        ("0x48", "wstring16le", OLD_WSTRING16),
    ):
        rows = [row for row in delta_rows if row["original_tag"] == old_tag]
        examples = [format_example(row) for row in rows[:3]]
        write = HELPERS[(old_tag, "W")]
        read = HELPERS[(old_tag, "R")]
        result.append(
            {
                "dedup_key": tag_key(tag),
                "delta_action": "ADDED",
                "tag": tag,
                "len": "5+N_bytes",
                "len_status_for_tag": "VARIABLE",
                "frequency_in_A2": str(len(rows)),
                "proven_semantics": (
                    f"{kind}; uint32le byte count; N payload bytes; "
                    "tag included in full wire length"
                ),
                "example_1": examples[0],
                "example_2": examples[1],
                "example_3": examples[2],
                "write_helper_va": fmt_va(int(write["helper_va"])),
                "write_helper_file_off": fmt_va(int(write["helper_file_off"])),
                "write_helper_span_end_va": fmt_va(int(write["helper_end_va"])),
                "write_helper_span_sha256": str(write["helper_sha256"]),
                "read_helper_va": fmt_va(int(read["helper_va"])),
                "read_helper_file_off": fmt_va(int(read["helper_file_off"])),
                "read_helper_span_end_va": fmt_va(int(read["helper_end_va"])),
                "read_helper_span_sha256": str(read["helper_sha256"]),
                "tag_instruction_write_va": fmt_va(
                    int(write["tag_instruction_va"])
                ),
                "tag_instruction_write_file_off": fmt_va(
                    int(write["tag_instruction_file_off"])
                ),
                "tag_instruction_read_va": fmt_va(int(read["tag_instruction_va"])),
                "tag_instruction_read_file_off": fmt_va(
                    int(read["tag_instruction_file_off"])
                ),
                "source": "IMAGE",
            }
        )
    return result


def assert_expected_counts(
    delta_rows: Sequence[dict[str, str]], tag_rows: Sequence[dict[str, str]]
) -> None:
    if len(delta_rows) != 408:
        raise RuntimeError(f"expected 408 A2 delta rows, got {len(delta_rows)}")
    keys = [row["dedup_key"] for row in delta_rows]
    if len(set(keys)) != 408:
        raise RuntimeError("A2 delta dedup keys are not unique")
    if len({row["message"] for row in delta_rows}) != 101:
        raise RuntimeError("expected 101 affected messages")

    tag_counts = Counter(row["original_tag"] for row in delta_rows)
    if tag_counts != Counter({OLD_STRING8: 60, OLD_WSTRING16: 348}):
        raise RuntimeError(f"unexpected string row census: {tag_counts}")
    direction_counts = Counter(row["direction(W/R)"] for row in delta_rows)
    if direction_counts != Counter({"W": 204, "R": 204}):
        raise RuntimeError(f"unexpected direction census: {direction_counts}")

    p1_rows = [row for row in delta_rows if row["priority"] == "1"]
    if len(p1_rows) != 384 or len({row["message"] for row in p1_rows}) != 92:
        raise RuntimeError("expected Priority-1 census of 384 rows / 92 messages")
    p3_rows = [row for row in delta_rows if row["priority"] == "3"]
    if len(p3_rows) != 24 or len({row["message"] for row in p3_rows}) != 9:
        raise RuntimeError("expected Priority-3 census of 24 rows / 9 messages")

    if len(tag_rows) != 2 or len({row["dedup_key"] for row in tag_rows}) != 2:
        raise RuntimeError("expected two unique A3 delta rows")
    if {row["tag"] for row in tag_rows} != {"0x44", "0x48"}:
        raise RuntimeError("unexpected A3 tag set")


def atomic_write_tsv(path: Path, rows: Sequence[Mapping[str, str]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to emit empty TSV: {path.name}")
    fieldnames = list(rows[0].keys())
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            writer = csv.DictWriter(
                handle,
                fieldnames=fieldnames,
                delimiter="\t",
                lineterminator="\n",
                extrasaction="raise",
            )
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        if temp_name is not None:
            try:
                Path(temp_name).unlink(missing_ok=True)
            except OSError:
                pass
        raise


def render_tsv(rows: Sequence[Mapping[str, str]]) -> str:
    if not rows:
        raise RuntimeError("refusing to render empty TSV")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=list(rows[0].keys()),
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def atomic_write_text(path: Path, text: str) -> None:
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="",
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
    except BaseException:
        if temp_name is not None:
            try:
                Path(temp_name).unlink(missing_ok=True)
            except OSError:
                pass
        raise


def report_text() -> str:
    return f"""# A2/A3 string wire-tag correction (additive overlay)

[MEASURED] Counts, addresses, offsets, and hashes below are re-derived from the pinned IMAGE and frozen V1 tables by this generator.

## Result

The 408 V1 A2 rows labelled `UNTAGGED_STRING8_LEN32LE` or
`UNTAGGED_WSTRING16LE_LEN32LE` stop at a helper payload boundary.  The exact
write/read helpers in the pinned IMAGE also emit or consume a one-byte wire tag:
`0x44` for string8 and `0x48` for wstring16le.  Therefore the full field shape is
`tag(1) + uint32le byte_count(4) + payload(N)`, or `5+N_bytes`.

This is an IMAGE-only representation correction.  No dump, capture, or data claim
is mixed into these rows, and no raw proprietary bytes are reproduced here.  The
frozen V1 tables remain unchanged.

## Non-duplicating outputs

| Output | Added rows | Logical changes | Unchanged rows copied | Duplicate rows rejected |
|---|---:|---:|---:|---:|
| `PF_A2_STRING_WIRE_TAG_DELTA.tsv` | 408 | 408 | 0 | 0 |
| `PF_A3_TAG_CENSUS_DELTA.tsv` | 2 | 0 | 0 (11 V1 tag rows remain by reference) | 0 |

Every A2 delta row has a stable SHA-256 `dedup_key` over its V1 row identity
(`message`, direction, order, call file offset, and original tag).  Apply each row
as a correction overlay; do not append it as an additional serializer field.  The
A3 delta contains only the two missing tags, not a copy of the 11-row V1 census.

## Affected census

- A2 delta: 408 unique rows across 101 unique messages.
- string8 / `0x44`: 60 rows (30 W, 30 R).
- wstring16le / `0x48`: 348 rows (174 W, 174 R).
- Priority 1: 384 rows across 92 messages.
- Priority 3: 24 rows across 9 messages.
- Priority 2: 0 rows.

## Exact IMAGE proof

| Kind/direction | Helper VA | Helper file offset | Helper end VA | Tag instruction VA | Tag instruction file offset | Span SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| string8 W (`0x44`) | 0x0089A6D0 | 0x00499AD0 | 0x0089A733 | 0x0089A6F1 | 0x00499AF1 | a0674fb3366720314e20ef5f5dbfa010330b12a73ed4e56e6c43e9d310dce9f1 |
| string8 R (`0x44`) | 0x0089A740 | 0x00499B40 | 0x0089A806 | 0x0089A75C | 0x00499B5C | 90c8c73b3b3c7158af57e374c694730763ab28292130b4f128a4754dec54e76a |
| wstring16le W (`0x48`) | 0x0089A810 | 0x00499C10 | 0x0089A875 | 0x0089A833 | 0x00499C33 | 08d6f27f030f3e0f1a32873d296c7f2c35a9d67f547607cf95c2900a60ffdad4 |
| wstring16le R (`0x48`) | 0x0089A880 | 0x00499C80 | 0x0089A95E | 0x0089A89C | 0x00499C9C | 2f564cb5d4f68d035d9e60fa1a4a5334b0875262420851f463f3f904e22ad978 |

The generator re-hashes every helper span, verifies each tag instruction at the
listed VA/file offset, and verifies that every selected A2 row pins the expected
helper target, span end, SHA-256, direction, string kind, and length-prefix form.

## Pinned inputs

| Input | SHA-256 |
|---|---|
| `GameClient.local.bin` | {PINNED_SHA256[IMAGE_PATH]} |
| `PF_SERIALIZER_FIELDS.tsv` | {PINNED_SHA256[FIELDS_PATH]} |
| `PF_PROTOCOL_PRIORITY.tsv` | {PINNED_SHA256[PRIORITY_PATH]} |
| `PF_TAG_CENSUS.tsv` | {PINNED_SHA256[TAG_CENSUS_PATH]} |

`source=IMAGE` applies to every TSV row in this overlay.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="derive in memory and require byte-identical existing outputs",
    )
    args = parser.parse_args()
    before = verify_pins()
    image = IMAGE_PATH.read_bytes()
    verify_helper_image(image)

    base_rows = read_tsv(FIELDS_PATH)
    if len(base_rows) != 6931:
        raise RuntimeError(f"expected 6931 V1 A2 rows, got {len(base_rows)}")

    priority_rows = read_tsv(PRIORITY_PATH)
    if len(priority_rows) != 519:
        raise RuntimeError(f"expected 519 priority rows, got {len(priority_rows)}")
    priority: dict[str, int] = {}
    for row in priority_rows:
        message = row["message"]
        if message in priority:
            raise RuntimeError(f"duplicate priority message: {message}")
        if row["source"] != "IMAGE":
            raise RuntimeError(f"non-IMAGE priority row: {message}")
        priority[message] = int(row["priority"])

    base_tag_rows = read_tsv(TAG_CENSUS_PATH)
    if len(base_tag_rows) != 11:
        raise RuntimeError(f"expected 11 V1 A3 rows, got {len(base_tag_rows)}")
    base_tags = [row["tag"] for row in base_tag_rows]
    if len(set(base_tags)) != 11:
        raise RuntimeError("duplicate tag in V1 census")
    if "0x44" in base_tags or "0x48" in base_tags:
        raise RuntimeError("A3 delta tags already exist in the pinned V1 census")

    delta_rows = build_delta_rows(base_rows, priority)
    tag_rows = build_tag_rows(delta_rows)
    assert_expected_counts(delta_rows, tag_rows)

    before_publish = verify_pins()
    if before != before_publish:
        raise RuntimeError("pinned inputs changed during analysis")

    outputs = {
        DELTA_PATH: render_tsv(delta_rows),
        TAG_DELTA_PATH: render_tsv(tag_rows),
        REPORT_PATH: report_text(),
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

    after_operation = verify_pins()
    if before != after_operation:
        raise RuntimeError("pinned inputs changed during output operation")

    print("A2/A3 string wire-tag correction: PASS mode=%s" % ("check" if args.check else "publish"))
    print("A2 rows: 408; messages: 101; duplicate_rejected: 0")
    print("string8 rows: 60; wstring16le rows: 348")
    print("Priority-1 rows/messages: 384/92")
    print("A3 rows added: 2; V1 rows copied: 0")
    for path in (DELTA_PATH, TAG_DELTA_PATH, REPORT_PATH):
        print(f"{path.name}: {sha256_file(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
