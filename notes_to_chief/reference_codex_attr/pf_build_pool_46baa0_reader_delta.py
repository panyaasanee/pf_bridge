#!/usr/bin/env python3
"""Build the fail-closed IMAGE reader-only overlay for pool 0x0046BAA0.

The generator changes exactly three V1 A2 reader rows.  It never edits V1,
never changes a writer row, and never emits a Priority delta.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import struct
import sys
import tempfile
from io import StringIO
from pathlib import Path
from types import ModuleType
from typing import Iterable, Mapping, Sequence


IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
EXTRACTOR_SHA256 = "0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e"
A2_SHA256 = "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
PRIORITY_SHA256 = "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"
SLOT34_A1_SHA256 = "a9036fa31739f5d91a5639f81116d0bcf6fc5ffbc656acbc77da5da8fe4f44db"
SLOT34_A2_SHA256 = "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334"
F4_A2_SHA256 = "21c6ca53f12a1d4d299e971d0868aa871b1953eebabfed295af906c2b2c4315e"
F4_PRIORITY_SHA256 = "32a59e143052f827f8134bba890f28d63444c447943e6679521dade7ff7e9fd1"

EXTRACTOR_NAME = "pf_extract_protocol.py"
A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
PRIORITY_NAME = "PF_PROTOCOL_PRIORITY.tsv"
SLOT34_A1_NAME = "PF_A1_SERIALIZER_SLOT34_DELTA.tsv"
SLOT34_A2_NAME = "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
F4_A2_NAME = "PF_A2_POOL_46F4D0_DELTA.tsv"
F4_PRIORITY_NAME = "PF_PRIORITY_POOL_46F4D0_DELTA.tsv"
OUTPUT_NAME = "PF_A2_POOL_46BAA0_READER_DELTA.tsv"
REPORT_NAME = "PF_POOL_46BAA0_BLOCKER.md"

POOL_HELPER = 0x0046BAA0
POOL_CTOR = 0x0046B410
POOL_VTABLE = 0x00F0EBB0
POOL_SERIALIZER = 0x0046BD30
DERIVED_VTABLE = 0x00F4A188
DERIVED_SERIALIZER = 0x00766C90

SPAN_PINS = (
    ("pool_helper", 0x0046BAA0, 0x0046BBAB, "8a996a4e9c1bf3bdfd81d1711fbf99dba817ee21d0a48bc3200978f3ca4d8924"),
    ("pool_ctor", 0x0046B410, 0x0046B497, "5a5d9aba90e35eea8119d252751058561c125ff68e54c3416a8bef6230872ddc"),
    ("base_serializer", 0x0046BD30, 0x0046BEA1, "b21137bde28452c08f8fa6a2eda18accf9c2d51b9b7d82a1b6997986feba86c1"),
    ("derived_serializer", 0x00766C90, 0x00766CC8, "2e530374f093af280c441ae3e23f97eedbd8b7a02d8b0598fe1b5bba2488b771"),
    ("generic_clone", 0x004636F0, 0x0046370C, "bdf5d7855a7bddbd4871e0a464283c178de0d5c28387aa2aa1c78b1ab5cfc752"),
    ("item_binding_root", 0x005EABD0, 0x005EAC8C, "1d0b7c857719202e760b647dd54a20a8d921559ca41bf85cde799c571f26e88a"),
    ("trade_root", 0x00664BA0, 0x00664D27, "92cfcdb8536fcbe50c1af4388116bf21a45540284266dceeebf3725736becec9"),
    ("guild_root", 0x00673970, 0x00673AE3, "15b78afa4b396223471ab19091dd0d6e1f9fa16b05ab0819a1cd212fd3794759"),
    ("guild_clone", 0x00673AF0, 0x00673BA2, "f9ad87e3c42588f0346590203d22ab2215fe4004f8344250cb19327833b3da56"),
)
SPAN_BY_NAME = {name: (start, end, digest) for name, start, end, digest in SPAN_PINS}

ROOTS = (
    {
        "message": "ItemBindingLockVitalRes", "base_line": 963,
        "root": "item_binding_root", "member": 0x18, "helper_call": 0x005EAC54,
        "new_copy": (0x005EAC5C, "edi"), "store": (0x005EAC6B, "edi", "esi"),
        "reload": (0x005EAC79, "ecx", "esi"), "vtable": (0x005EAC7C, "edx", "ecx"),
        "slot": (0x005EAC7E, "eax", "edx"), "mode_push": 0x005EAC81,
        "reader_call": (0x005EAC84, "eax"), "gate": "DECODED_PRESENCE_FLAG!=0",
    },
    {
        "message": "TradeItemResultVital", "base_line": 2587,
        "root": "trade_root", "member": 0x1C, "helper_call": 0x00664C66,
        "new_copy": (0x00664C6E, "ebx"), "store": (0x00664C7D, "ebx", "esi"),
        "reload": (0x00664C8B, "esi", "esi"), "vtable": (0x00664C8E, "edx", "esi"),
        "slot": (0x00664C90, "eax", "edx"), "mode_push": 0x00664C93,
        "reader_call": (0x00664C98, "eax"), "gate": "DECODED_PRESENCE_FLAG!=0",
    },
    {
        "message": "GCGSSS_GuildStorageResultVital", "base_line": 3837,
        "root": "guild_root", "member": 0x2C, "helper_call": 0x00673AA5,
        "new_copy": (0x00673AAD, "ebx"), "store": (0x00673ABC, "ebx", "esi"),
        "reload": (0x00673ACA, "esi", "esi"), "vtable": (0x00673AD1, "edx", "esi"),
        "slot": (0x00673AD3, "eax", "edx"), "mode_push": 0x00673AD6,
        "reader_call": (0x00673ADB, "eax"), "gate": "DECODED_MASK_BIT_0X02_SET",
    },
)
TARGETS = tuple(spec["message"] for spec in ROOTS)

A2_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line", "base_row_key",
    "message", "direction(W/R)", "old_order", "old_tag", "old_field_offset", "old_len",
    "new_wire_order", "new_tag", "new_field_offset", "new_len", "new_gate_condition",
    "resolution", "evidence_ticket", "evidence_span_start", "evidence_span_end",
    "evidence_span_sha256", "evidence_file_off", "source",
)


class ProofError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_hash(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise ProofError(f"missing pinned input: {label}")
    actual = sha256_path(path)
    if actual != expected:
        raise ProofError(f"{label} SHA-256 mismatch: expected {expected}, got {actual}")


def load_protocol(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("pf_pool_46baa0_reader_protocol_pin", path)
    if spec is None or spec.loader is None:
        raise ProofError("cannot load pinned protocol extractor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_tsv(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ProofError(f"missing TSV header: {path.name}")
        return list(reader.fieldnames), [(line, dict(row)) for line, row in enumerate(reader, 2)]


def canonical_row_key(fields: Sequence[str], row: Mapping[str, str]) -> str:
    payload = json.dumps([row[name] for name in fields], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def delta_key(parts: Iterable[str]) -> str:
    return sha256_bytes("\x1f".join(parts).encode("utf-8"))


def write_tsv(rows: Sequence[Mapping[str, str]]) -> str:
    handle = StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=list(A2_COLUMNS), delimiter="\t", lineterminator="\n", extrasaction="raise")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue()


def atomic_write(path: Path, content: str) -> None:
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=path.parent, delete=False) as handle:
            temp_name = handle.name
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name is not None and os.path.exists(temp_name):
            os.unlink(temp_name)


def span_bytes(image, start_va: int, end_va: int) -> bytes:
    start = image.va_to_off(start_va)
    end = image.va_to_off(end_va)
    if start is None or end is None or end <= start:
        raise ProofError(f"unmapped span 0x{start_va:08X}..0x{end_va:08X}")
    return bytes(image.data[start:end])


def u32(image, va: int) -> int:
    off = image.va_to_off(va)
    if off is None:
        raise ProofError(f"unmapped u32 0x{va:08X}")
    return struct.unpack_from("<I", image.data, off)[0]


def decode_at(proto: ModuleType, image, va: int, end_va: int):
    limit = image.va_to_off(end_va)
    if limit is None:
        raise ProofError(f"unmapped decode limit 0x{end_va:08X}")
    return proto.decode_instruction(image, va, limit)


def expect_call(proto: ModuleType, image, va: int, end_va: int, target: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "call" or ins.target != target:
        raise ProofError(f"expected CALL 0x{target:08X} at 0x{va:08X}, got {ins}")


def expect_call_reg(proto: ModuleType, image, va: int, end_va: int, reg: str) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "call_indirect" or ins.src is None or ins.src.kind != "reg" or ins.src.reg != reg:
        raise ProofError(f"expected indirect CALL {reg} at 0x{va:08X}, got {ins}")


def expect_mov_mem_to_reg(proto: ModuleType, image, va: int, end_va: int, dst: str, base: str, disp: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if (ins.kind != "mov" or ins.dst is None or ins.dst.kind != "reg" or ins.dst.reg != dst or
            ins.src is None or ins.src.kind != "mem" or ins.src.base != base or
            ins.src.index is not None or ins.src.disp != disp or ins.src.absolute is not None):
        raise ProofError(f"unexpected MOV at 0x{va:08X}: {ins}")


def expect_mov_reg_to_mem(proto: ModuleType, image, va: int, end_va: int, src: str, base: str, disp: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if (ins.kind != "mov" or ins.src is None or ins.src.kind != "reg" or ins.src.reg != src or
            ins.dst is None or ins.dst.kind != "mem" or ins.dst.base != base or
            ins.dst.index is not None or ins.dst.disp != disp or ins.dst.absolute is not None):
        raise ProofError(f"unexpected MOV at 0x{va:08X}: {ins}")


def expect_mov_reg_to_reg(proto: ModuleType, image, va: int, end_va: int, dst: str, src: str) -> None:
    ins = decode_at(proto, image, va, end_va)
    if (ins.kind != "mov" or ins.dst is None or ins.dst.kind != "reg" or ins.dst.reg != dst or
            ins.src is None or ins.src.kind != "reg" or ins.src.reg != src):
        raise ProofError(f"unexpected register MOV at 0x{va:08X}: {ins}")


def expect_push_zero(proto: ModuleType, image, va: int, end_va: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "push" or ins.src is None or ins.src.kind != "imm" or ins.src.imm != 0:
        raise ProofError(f"expected PUSH 0 at 0x{va:08X}, got {ins}")


def verify_span_pins(image) -> None:
    for name, start, end, expected in SPAN_PINS:
        actual = sha256_bytes(span_bytes(image, start, end))
        if actual != expected:
            raise ProofError(f"span {name} mismatch: expected {expected}, got {actual}")


def verify_pool_identity(proto: ModuleType, image) -> None:
    helper_end = SPAN_BY_NAME["pool_helper"][1]
    ctor_end = SPAN_BY_NAME["pool_ctor"][1]
    expect_call(proto, image, 0x0046BB04, helper_end, POOL_CTOR)
    expect_call(proto, image, 0x0046BB82, helper_end, POOL_CTOR)
    ctor_store = decode_at(proto, image, 0x0046B440, ctor_end)
    if (ctor_store.kind != "mov" or ctor_store.dst is None or ctor_store.dst.kind != "mem" or
            ctor_store.dst.base != "esi" or ctor_store.dst.disp != 0 or ctor_store.src is None or
            ctor_store.src.kind != "imm" or ctor_store.src.imm != POOL_VTABLE):
        raise ProofError(f"base constructor vtable store mismatch: {ctor_store}")
    if u32(image, POOL_VTABLE + 0x34) != POOL_SERIALIZER:
        raise ProofError("base ItemAttr +0x34 serializer mismatch")
    if u32(image, DERIVED_VTABLE + 0x34) != DERIVED_SERIALIZER:
        raise ProofError("derived ItemAttr +0x34 serializer mismatch")


def verify_root(proto: ModuleType, image, spec: Mapping[str, object]) -> None:
    _start, end, _digest = SPAN_BY_NAME[str(spec["root"])]
    expect_call(proto, image, int(spec["helper_call"]), end, POOL_HELPER)
    copy_va, copy_dst = spec["new_copy"]
    expect_mov_reg_to_reg(proto, image, int(copy_va), end, str(copy_dst), "eax")
    store_va, store_src, store_base = spec["store"]
    expect_mov_reg_to_mem(proto, image, int(store_va), end, str(store_src), str(store_base), int(spec["member"]))
    reload_va, reload_dst, reload_base = spec["reload"]
    expect_mov_mem_to_reg(proto, image, int(reload_va), end, str(reload_dst), str(reload_base), int(spec["member"]))
    vtable_va, vtable_dst, vtable_base = spec["vtable"]
    expect_mov_mem_to_reg(proto, image, int(vtable_va), end, str(vtable_dst), str(vtable_base), 0)
    slot_va, slot_dst, slot_base = spec["slot"]
    expect_mov_mem_to_reg(proto, image, int(slot_va), end, str(slot_dst), str(slot_base), 0x34)
    expect_push_zero(proto, image, int(spec["mode_push"]), end)
    call_va, call_reg = spec["reader_call"]
    expect_call_reg(proto, image, int(call_va), end, str(call_reg))


def verify_dynamic_identity_overlay(path: Path) -> None:
    fields, rows = read_tsv(path)
    required = {"name", "action", "corrected_candidates", "source"}
    if not required <= set(fields):
        raise ProofError("slot-34 A1 delta schema mismatch")
    matches = [row for _line, row in rows if row["name"] == "ItemAttr"]
    expected = (
        "vtable=0x00F0EBB0,serializer=0x0046BD30,pointer_file_off=0x00B0CFE4|"
        "vtable=0x00F4A188,serializer=0x00766C90,pointer_file_off=0x00B485BC"
    )
    if len(matches) != 1 or matches[0]["action"] != "CHANGED_TO_AMBIGUOUS" or matches[0]["corrected_candidates"] != expected or matches[0]["source"] != "IMAGE":
        raise ProofError("ItemAttr dynamic identity evidence mismatch")


def verify_priority_open(path: Path) -> None:
    fields, rows = read_tsv(path)
    required = {"message", "priority", "serializer_status", "structural_status", "source"}
    if not required <= set(fields):
        raise ProofError("priority schema mismatch")
    selected = {row["message"]: row for _line, row in rows if row["message"] in TARGETS}
    if set(selected) != set(TARGETS):
        raise ProofError("priority target census mismatch")
    for message, row in selected.items():
        if row["priority"] != "1" or row["serializer_status"] != "OPEN" or row["structural_status"] != "OPEN" or row["source"] != "IMAGE":
            raise ProofError(f"priority base state mismatch for {message}")


def select_base_row(fields: Sequence[str], rows: Sequence[tuple[int, dict[str, str]]], spec: Mapping[str, object], image) -> tuple[int, dict[str, str]]:
    member = int(spec["member"])
    tag = f"CALL_UNCLASSIFIED:INDIRECT(DEREF(DEREF(DEREF(OBJ+0x{member:X}))+0x34))"
    reader_va, _reg = spec["reader_call"]
    off = image.va_to_off(int(reader_va))
    wanted_off = f"0x{off:08X}" if off is not None else "UNMAPPED"
    matches = [
        (line, row) for line, row in rows
        if line == int(spec["base_line"]) and row["message"] == spec["message"] and
        row["direction(W/R)"] == "R" and row["file_off_claim"] == wanted_off and row["tag"] == tag
    ]
    if len(matches) != 1:
        raise ProofError(f"base A2 selection mismatch for {spec['message']}: {len(matches)}")
    line, row = matches[0]
    if row["field_offset"] != "UNKNOWN(indirect_call_not_proven_serializer_slot)" or row["source"] != "IMAGE":
        raise ProofError(f"base A2 state mismatch for {spec['message']}")
    return line, row


def build_delta(image, fields: Sequence[str], rows: Sequence[tuple[int, dict[str, str]]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for spec in ROOTS:
        line, row = select_base_row(fields, rows, spec, image)
        key = canonical_row_key(fields, row)
        start, end, digest = SPAN_BY_NAME[str(spec["root"])]
        output.append({
            "delta_key": delta_key((A2_NAME, str(line), key, "CHANGED")),
            "action": "CHANGED",
            "change_type": "RESOLVE_FIXED_READER_POOL_VTABLE_PLUS_34_SUBCALL",
            "base_file": A2_NAME,
            "base_line": str(line),
            "base_row_key": key,
            "message": str(spec["message"]),
            "direction(W/R)": "R",
            "old_order": row["order"],
            "old_tag": row["tag"],
            "old_field_offset": row["field_offset"],
            "old_len": row["len"],
            "new_wire_order": row["order"],
            "new_tag": f"SUBCALL:0x{POOL_SERIALIZER:08X}",
            "new_field_offset": f"DEREF(+0x{int(spec['member']):X})",
            "new_len": "N/A",
            "new_gate_condition": str(spec["gate"]),
            "resolution": "READER_HELPER_RESULT_FIXED_BASE_ITEMATTR_SUBCALL;WRITER_UNTOUCHED_DYNAMIC_IDENTITY",
            "evidence_ticket": "POOL_46BAA0_READER",
            "evidence_span_start": f"0x{start:08X}",
            "evidence_span_end": f"0x{end:08X}",
            "evidence_span_sha256": digest,
            "evidence_file_off": row["file_off_claim"],
            "source": "IMAGE",
        })
    output.sort(key=lambda row: int(row["base_line"]))
    if len(output) != 3 or any(row["action"] != "CHANGED" or row["direction(W/R)"] != "R" or row["source"] != "IMAGE" for row in output):
        raise ProofError("reader delta census mismatch")
    if {int(row["base_line"]) for row in output} != {963, 2587, 3837}:
        raise ProofError("reader delta base-line mismatch")
    if len({row["delta_key"] for row in output}) != 3 or len({row["base_row_key"] for row in output}) != 3:
        raise ProofError("duplicate delta/base key")
    if any(row["new_tag"] != "SUBCALL:0x0046BD30" for row in output):
        raise ProofError("unexpected reader target")
    return output


def overlay_census(external: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        (path.name, sha256_path(path))
        for path in sorted(external.glob("*DELTA.tsv"))
        if path.name != OUTPUT_NAME
    )


def validate_no_overlap(external: Path, delta: Sequence[Mapping[str, str]]) -> None:
    wanted = {(row["base_file"], row["base_row_key"]) for row in delta}
    wanted_lines = {int(row["base_line"]) for row in delta}
    for path in sorted(external.glob("*DELTA.tsv")):
        if path.name == OUTPUT_NAME:
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            fields = set(reader.fieldnames or ())
            for row in reader:
                if {"base_file", "base_row_key"} <= fields and (row["base_file"], row["base_row_key"]) in wanted:
                    raise ProofError(f"existing overlay base-key overlap: {path.name}")
                if path.name == "PF_A2_STRING_WIRE_TAG_DELTA.tsv" and "base_row_number" in fields and int(row["base_row_number"]) in wanted_lines:
                    raise ProofError("string overlay base-line overlap")


def validate_no_priority_delta(external: Path) -> None:
    stale = sorted(path.name for path in external.glob("PF_PRIORITY_POOL_46BAA0*.tsv"))
    if stale:
        raise ProofError(f"forbidden Priority output exists: {stale}")


def report_text(a2_sha256: str) -> str:
    return f"""# PF pool 0x0046BAA0 reader-only correction and fail-closed blocker

[MEASURED] `source=IMAGE`. V1 and every existing overlay remain immutable.

## Result

The additive A2 overlay publishes exactly **3 CHANGED reader rows** and no
other row:

| message/member | V1 line | reader call | result |
|---|---:|---:|---|
| `ItemBindingLockVitalRes +0x18` | 963 | `0x005EAC84` | `SUBCALL:0x0046BD30` |
| `TradeItemResultVital +0x1C` | 2587 | `0x00664C98` | `SUBCALL:0x0046BD30` |
| `GCGSSS_GuildStorageResultVital +0x2C` | 3837 | `0x00673ADB` | `SUBCALL:0x0046BD30` |

A2 delta sha256: `{a2_sha256}`. Unchanged rows copied: **0**. Writer rows
changed: **0**. Duplicate delta keys: **0**. Duplicate base keys: **0**.
Existing-overlay base-key overlap: **0**. Every emitted row is
`source=IMAGE`.

No Priority delta is emitted. `ItemBindingLockVitalRes`,
`TradeItemResultVital`, and `GCGSSS_GuildStorageResultVital` all remain
**OPEN**. Closed-count change: **0**.

## Why the reader is fixed

- Pool helper `0x0046BAA0..0x0046BBAB`: file offset `0x0006AEA0`,
  267 bytes, 87 reachable instructions, sha256
  `8a996a4e9c1bf3bdfd81d1711fbf99dba817ee21d0a48bc3200978f3ca4d8924`.
- Both helper arms call base constructor `0x0046B410` at `0x0046BB04`
  and `0x0046BB82`.
- Constructor `0x0046B410..0x0046B497`: file offset `0x0006A810`,
  sha256 `5a5d9aba90e35eea8119d252751058561c125ff68e54c3416a8bef6230872ddc`.
  It stores vtable `0x00F0EBB0` at `0x0046B440`.
- Vtable `0x00F0EBB0 +0x34 -> 0x0046BD30`. The serializer span is
  `0x0046BD30..0x0046BEA1`, sha256
  `b21137bde28452c08f8fa6a2eda18accf9c2d51b9b7d82a1b6997986feba86c1`.

Each corrected site is after that exact helper result is stored into the same
member and reloaded for a reader-mode-zero call through slot `+0x34`. The
nested serializer is referenced, not flattened.

## Why the messages remain OPEN

Exact blocker: `BLOCKED_WRITE_DYNAMIC_IDENTITY`. The writer sites do not call
the pool helper; they dispatch a pre-existing `ItemAttr*` through slot
`+0x34`. The IMAGE has at least two exact targets:

| candidate | vtable | serializer | serializer sha256 |
|---|---:|---:|---|
| base `ItemAttr` | `0x00F0EBB0` | `0x0046BD30` | `b21137bde28452c08f8fa6a2eda18accf9c2d51b9b7d82a1b6997986feba86c1` |
| derived `ItemAttr` | `0x00F4A188` | `0x00766C90` | `2e530374f093af280c441ae3e23f97eedbd8b7a02d8b0598fe1b5bba2488b771` |

The untouched writer rows are V1 lines 954 (`0x001EA019`), 2576
(`0x0026400B`), and 3818 (`0x00272E01`). No result collapses these candidates.

For Guild Storage, clone `0x00673AF0..0x00673BA2` (sha256
`f9ad87e3c42588f0346590203d22ab2215fe4004f8344250cb19327833b3da56`)
uses fixed pool `0x0046F4D0` for member `+0x28`, but calls generic clone
`0x004636F0` for member `+0x2C`. Generic clone preserves the source dynamic
identity through source-vtable slots `+0x14` and `+0x24`. Thus the fixed
`+0x28` dependency does not close the whole message.

## Pinned roots

| root | exact span | sha256 |
|---|---|---|
| `ItemBindingLockVitalRes` | `0x005EABD0..0x005EAC8C` | `1d0b7c857719202e760b647dd54a20a8d921559ca41bf85cde799c571f26e88a` |
| `TradeItemResultVital` | `0x00664BA0..0x00664D27` | `92cfcdb8536fcbe50c1af4388116bf21a45540284266dceeebf3725736becec9` |
| `GCGSSS_GuildStorageResultVital` | `0x00673970..0x00673AE3` | `15b78afa4b396223471ab19091dd0d6e1f9fa16b05ab0819a1cd212fd3794759` |

Pinned image: size 14,759,424, sha256
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

Reproduction:

```powershell
py -3 pf_build_pool_46baa0_reader_delta.py --check
```
"""


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", type=Path, default=here.parent.parent / "GameClient" / "GameClient.local.bin")
    parser.add_argument("--external", type=Path, default=here)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    external = args.external.resolve()
    client = args.client.resolve()
    pinned = (
        (client, IMAGE_SHA256, "GameClient.local.bin"),
        (external / EXTRACTOR_NAME, EXTRACTOR_SHA256, EXTRACTOR_NAME),
        (external / A2_NAME, A2_SHA256, A2_NAME),
        (external / PRIORITY_NAME, PRIORITY_SHA256, PRIORITY_NAME),
        (external / SLOT34_A1_NAME, SLOT34_A1_SHA256, SLOT34_A1_NAME),
        (external / SLOT34_A2_NAME, SLOT34_A2_SHA256, SLOT34_A2_NAME),
        (external / F4_A2_NAME, F4_A2_SHA256, F4_A2_NAME),
        (external / F4_PRIORITY_NAME, F4_PRIORITY_SHA256, F4_PRIORITY_NAME),
    )
    for path, expected, label in pinned:
        require_hash(path, expected, label)
    if client.stat().st_size != IMAGE_SIZE:
        raise ProofError(f"image size mismatch: {client.stat().st_size}")

    protocol = load_protocol(external / EXTRACTOR_NAME)
    image = protocol.Image(client)
    before = overlay_census(external)
    verify_span_pins(image)
    verify_pool_identity(protocol, image)
    for spec in ROOTS:
        verify_root(protocol, image, spec)
    verify_dynamic_identity_overlay(external / SLOT34_A1_NAME)
    verify_priority_open(external / PRIORITY_NAME)

    fields, rows = read_tsv(external / A2_NAME)
    delta = build_delta(image, fields, rows)
    validate_no_overlap(external, delta)
    validate_no_priority_delta(external)
    a2_text = write_tsv(delta)
    report = report_text(sha256_bytes(a2_text.encode("utf-8")))
    contents = {OUTPUT_NAME: a2_text, REPORT_NAME: report}

    # Rehash every input and freeze the complete pre-existing delta census
    # immediately before per-file atomic publication.
    for path, expected, label in pinned:
        require_hash(path, expected, label)
    if overlay_census(external) != before:
        raise ProofError("overlay census changed during generation")
    validate_no_overlap(external, delta)
    validate_no_priority_delta(external)

    if args.check:
        for name, expected in contents.items():
            path = external / name
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                raise ProofError(f"missing or stale output: {name}")
    else:
        for name, content in contents.items():
            atomic_write(external / name, content)
        for name, expected in contents.items():
            if (external / name).read_text(encoding="utf-8") != expected:
                raise ProofError(f"post-publication mismatch: {name}")

    print(json.dumps({
        "mode": "check" if args.check else "publish",
        "a2_rows": len(delta),
        "a2_changed": 3,
        "writer_rows_changed": 0,
        "priority_rows": 0,
        "source": "IMAGE",
        "outputs": {name: sha256_bytes(content.encode("utf-8")) for name, content in contents.items()},
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProofError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

