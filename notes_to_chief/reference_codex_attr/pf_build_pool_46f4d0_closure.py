#!/usr/bin/env python3
"""Build the fail-closed IMAGE overlay for the 0x0046F4D0 object pool.

This generator is additive: it never edits V1 and emits only exact,
base-keyed directives for four named Priority-1 messages.
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
from collections import Counter, deque
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from types import ModuleType
from typing import Iterable, Mapping, Sequence


IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
EXTRACTOR_SHA256 = "0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e"
A1_SHA256 = "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d"
A2_SHA256 = "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
PRIORITY_SHA256 = "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"
POST_V1_PRIORITY_SHA256 = "69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51"
STRING_DELTA_SHA256 = "e1f4f987c31f53d4dd87845aab01857c8415a8dbcd750af12df9c4cde208b3a2"

A1_NAME = "PF_PROTOCOL_REGISTRY.tsv"
A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
PRIORITY_NAME = "PF_PROTOCOL_PRIORITY.tsv"
POST_V1_PRIORITY_NAME = "PF_POST_V1_PRIORITY_DELTA.tsv"
STRING_DELTA_NAME = "PF_A2_STRING_WIRE_TAG_DELTA.tsv"
EXTRACTOR_NAME = "pf_extract_protocol.py"
A2_DELTA_NAME = "PF_A2_POOL_46F4D0_DELTA.tsv"
PRIORITY_DELTA_NAME = "PF_PRIORITY_POOL_46F4D0_DELTA.tsv"
REPORT_NAME = "PF_POOL_46F4D0_CLOSURE.md"

POOL_HELPER = 0x0046F4D0
POOL_CTOR = 0x0046F3F0
POOL_VTABLE = 0x00F0ECB8
POOL_SERIALIZER = 0x0046F180
POOL_DESTRUCTOR = 0x0046F470
POOL_GLOBAL = 0x01031420
POOL_TYPE_TOKEN = 0x00F0A90C
REF_INCREMENT = 0x0088D050
REF_DECREMENT = 0x0088D060
WIRE_PRIMITIVES = frozenset((0x0089A600, 0x0089A640, 0x0089A810, 0x0089A880))


@dataclass(frozen=True)
class SpanPin:
    name: str
    start_va: int
    end_va: int
    sha256: str


SPAN_PINS = (
    SpanPin("pool_helper", 0x0046F4D0, 0x0046F5DB, "b9308abc49969ded9194d369823de1f29207ca8addcfe22f838a4b3d1ea45885"),
    SpanPin("pool_ctor", 0x0046F3F0, 0x0046F469, "de13f1abba13b83ca153793431e5ffb549f81104d5d313e499446d8d22c9cb91"),
    SpanPin("pool_vtable_prefix", 0x00F0ECB8, 0x00F0ED00, "f69f74e9624dfbd29c87dd0cb42e634089206d35bce160f1e790b4f94af81d21"),
    SpanPin("pool_serializer", 0x0046F180, 0x0046F3E9, "29e38267ab54c852e3f1338c2fb833e3b9d1a41903544a390489c264c09fa813"),
    SpanPin("pool_dtor_wrapper", 0x0046F470, 0x0046F4CE, "4eb3bcb521cfe05fb54757eb8a09618a10391b40e0a155a57c384ab9572dae73"),
    SpanPin("pool_core_dtor", 0x0046EB90, 0x0046EBFB, "702f8bbb5461c9eb701fa57af5db226e39956af0bd3ec1e3f438e2c5a10d9dd4"),
    SpanPin("pool_member_a_dtor", 0x0046E5E0, 0x0046E672, "a1bd5c2b118f0c290d9e0ab7893512bc06c29c61c959f78ff69b4d3ed57c61cc"),
    SpanPin("pool_member_b_dtor", 0x0074D4D0, 0x0074D54C, "6e3583aad8fa052d6571b934300827fa052fa26e8a43c9e1bb428c50d972a476"),
    SpanPin("pool_base_dtor", 0x00467690, 0x0046769B, "5080e93eb23cb770d9314ad49aacd9944f615c8f0522480e1a575261af3a7756"),
    SpanPin("base_object_dtor", 0x0088D280, 0x0088D2F0, "d914c8eaef424f2988c6b76b6954acbb9247bd4309a2c8f0e09439cc64f1104a"),
    SpanPin("lock", 0x0088D5B0, 0x0088D5BA, "281bb0603facf9b7c61c87c0241b74e59ff6488057f979782e4d08ea4e4e9ee8"),
    SpanPin("unlock", 0x0049DA40, 0x0049DA4A, "91f8bd361459e6514e2c53ca4bac3bd9d76baddaf75ee1b1562afecee8d96366"),
    SpanPin("ref_increment", 0x0088D050, 0x0088D05B, "6da78a1acc15d9fd5f7b2d620253debf8d8465136165dfb1eae35914b2442845"),
    SpanPin("ref_decrement", 0x0088D060, 0x0088D082, "d3b546ac50ded491a6c5a196138b9691f23d8499298e728925f1afb1f0e7734c"),
    SpanPin("actor_root", 0x005EAC90, 0x005EADCA, "04c9bf8a126dbea9013a9578688f6d4b07dfdef13537da0cffe48f3c6da7168e"),
    SpanPin("storage_root", 0x00699820, 0x00699904, "3e473b3e5a0e1ba60ca67a2ff8f2f2913e47fa2de3ccd91e5db923f8bc0b9c0b"),
    SpanPin("itemmall_root", 0x006B9C80, 0x006B9D1D, "2d5e2820834ad57bdf4e26ef71364cffb255bb99b709f9d2fb3682f3ad4e27ec"),
    SpanPin("collection_root", 0x006E1120, 0x006E11C4, "5f8071ac25254d83f9403fd96253ab2bfc22d7cf5c93a4e94d3f5e7be13ca226"),
    SpanPin("actor_ctor", 0x005E66A0, 0x005E6722, "9a17e0954c938445ca06328d4a643c4c8b756b9f2154db294d96ca1971b9c56c"),
    SpanPin("storage_ctor", 0x006991C0, 0x0069923B, "0a03a815021024dc4b07ece5c8489c3551c5870c691a2378516e561ed7a96b78"),
    SpanPin("itemmall_ctor", 0x006B8830, 0x006B88A4, "0b54f6d14fa8deddd1e035a74eeea9f7a58318316b9f53f470b15ce8a4b96797"),
    SpanPin("collection_ctor", 0x006E0810, 0x006E0863, "95f46fde3d8bdfbc146fda24a4664206f72c07efbfe8426053b2ffd779f5dbed"),
    SpanPin("actor_dtor_wrapper", 0x005EA570, 0x005EA5CE, "0a9228bd63bc8e37a5a12af11d45802fae06663524a38cf0ca6fe1d29f3cb55a"),
    SpanPin("storage_dtor_wrapper", 0x00699530, 0x0069958E, "4efbb5894da09e05bb5ed6d1c3b890d42e913e01bd320325c0ca90c9c2e47755"),
    SpanPin("itemmall_dtor_wrapper", 0x006B9280, 0x006B92DE, "334d969458259488249f25cc582f5edb3ca804aebcdbf799f443527aaeff86b5"),
    SpanPin("collection_dtor_wrapper", 0x006E0A90, 0x006E0AEE, "2f408069c2175f83da1d42f1bc29df772539786cfb9e67ddb47d3d50cc827b9c"),
    SpanPin("actor_core_dtor", 0x005E6750, 0x005E67D0, "96aaeedf1c33c052f6c2c2e5ea0079fb3ed1e6a82b39e0c09867cdbeca3dbde7"),
    SpanPin("storage_core_dtor", 0x00699260, 0x006992E0, "77f1b0d7772513bebfec625d33d386d94f02dcb2e6952990ffa742000c603f33"),
    SpanPin("itemmall_core_dtor", 0x006B88D0, 0x006B8950, "d5706225e6e1bd2cefb217dca30176bde743fabddf7445f420b3ce2855f01ad9"),
    SpanPin("collection_core_dtor", 0x006FF030, 0x006FF092, "5c11cba24fc76beb3e79c512a9cbd348b463878bc1803ae78cd3193ca860b430"),
)
SPAN_BY_NAME = {pin.name: pin for pin in SPAN_PINS}


@dataclass(frozen=True)
class RootSpec:
    root_name: str
    root_va: int
    member_offset: int
    object_reg: str
    writer_stream_reg: str
    reader_stream_reg: str
    writer_member_load: int
    writer_vtable_load: int
    writer_slot_load: int
    writer_mode_push: int
    writer_stream_push: int
    writer_call: int
    reader_helper_push_zero: int
    reader_helper_push_token: int
    reader_helper_pool_load: int
    reader_helper_call: int
    reader_old_load: int
    reader_new_copy: int
    reader_compare: int
    reader_decrement: int
    reader_store: int
    reader_increment_this: int
    reader_increment: int
    reader_reload: int
    reader_reload_reg: str
    reader_vtable_load: int
    reader_slot_load: int
    reader_mode_push: int
    reader_this_move: int | None
    reader_stream_push: int
    reader_call: int


ROOTS = {
    "actor_root": RootSpec(
        "actor_root", 0x005EAC90, 0x20, "esi", "edi", "edi",
        0x005EACE9, 0x005EACF4, 0x005EACF6, 0x005EACF9, 0x005EACFA, 0x005EACFB,
        0x005EAD4A, 0x005EAD4C, 0x005EAD51, 0x005EAD56, 0x005EAD5B, 0x005EAD5E,
        0x005EAD60, 0x005EAD68, 0x005EAD6D, 0x005EAD74, 0x005EAD76, 0x005EAD7B,
        "esi", 0x005EAD7E, 0x005EAD80, 0x005EAD83, 0x005EAD85, 0x005EAD87, 0x005EAD88,
    ),
    "storage_root": RootSpec(
        "storage_root", 0x00699820, 0x1C, "esi", "edi", "ebx",
        0x0069986A, 0x00699875, 0x00699877, 0x0069987A, 0x0069987B, 0x0069987C,
        0x006998C0, 0x006998C2, 0x006998C7, 0x006998CC, 0x006998D1, 0x006998D4,
        0x006998D6, 0x006998DE, 0x006998E3, 0x006998EA, 0x006998EC, 0x006998F1,
        "ecx", 0x006998F4, 0x006998F6, 0x006998F9, None, 0x006998FB, 0x006998FC,
    ),
    "itemmall_root": RootSpec(
        "itemmall_root", 0x006B9C80, 0x14, "esi", "edi", "ebx",
        0x006B9CAC, 0x006B9CB3, 0x006B9CB5, 0x006B9CB8, 0x006B9CB9, 0x006B9CBA,
        0x006B9CD9, 0x006B9CDB, 0x006B9CE0, 0x006B9CE5, 0x006B9CEA, 0x006B9CED,
        0x006B9CEF, 0x006B9CF7, 0x006B9CFC, 0x006B9D03, 0x006B9D05, 0x006B9D0A,
        "ecx", 0x006B9D0D, 0x006B9D0F, 0x006B9D12, None, 0x006B9D14, 0x006B9D15,
    ),
    "collection_root": RootSpec(
        "collection_root", 0x006E1120, 0x14, "esi", "edi", "ebx",
        0x006E1153, 0x006E1156, 0x006E1158, 0x006E115B, 0x006E115C, 0x006E115D,
        0x006E117C, 0x006E117E, 0x006E1183, 0x006E1188, 0x006E118D, 0x006E1190,
        0x006E1192, 0x006E119A, 0x006E119F, 0x006E11A6, 0x006E11A8, 0x006E11AD,
        "ecx", 0x006E11B4, 0x006E11B6, 0x006E11B9, None, 0x006E11BB, 0x006E11BC,
    ),
}


@dataclass(frozen=True)
class MessageSpec:
    message: str
    root_name: str
    message_vtable: int
    ctor_vtable_store: int
    ctor_member_store: int
    ctor_object_reg: str
    zero_reg: str
    wrapper_dtor: int
    wrapper_core_call: int
    core_dtor: int
    core_member_load: int
    core_member_decrement: int


MESSAGES = (
    MessageSpec("ActorInspectVital", "actor_root", 0x00F30494, 0x005E66DD, 0x005E66E7, "esi", "ebx", 0x005EA570, 0x005EA573, 0x005E6750, 0x005E677E, 0x005E678D),
    MessageSpec("StorageResultVital", "storage_root", 0x00F3C194, 0x00699200, 0x0069920A, "esi", "ebx", 0x00699530, 0x00699533, 0x00699260, 0x0069928E, 0x0069929D),
    MessageSpec("ItemMallBagUpdate", "itemmall_root", 0x00F3E3F8, 0x006B8870, 0x006B887A, "esi", "ebx", 0x006B9280, 0x006B9283, 0x006B88D0, 0x006B88FE, 0x006B890D),
    MessageSpec("CollectionObj_UpdateCollectionObjBagVital", "collection_root", 0x00F40800, 0x006E084A, 0x006E0850, "eax", "ecx", 0x006E0A90, 0x006E0A93, 0x006FF030, 0x006FF058, 0x006FF067),
)
MESSAGE_BY_NAME = {spec.message: spec for spec in MESSAGES}
TARGET_NAMES = tuple(spec.message for spec in MESSAGES)

A2_DELTA_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line", "base_row_key",
    "message", "direction(W/R)", "old_order", "old_tag", "old_field_offset", "old_len",
    "new_wire_order", "new_tag", "new_field_offset", "new_len", "new_gate_condition",
    "resolution", "evidence_ticket", "evidence_span_start", "evidence_span_end",
    "evidence_span_sha256", "evidence_file_off", "source",
)
PRIORITY_DELTA_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "message", "priority",
    "old_serializer_status", "new_serializer_status", "old_structural_status",
    "new_structural_status", "old_blocker", "new_blocker", "evidence_ticket",
    "closure_scope", "source",
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
    actual = sha256_path(path)
    if actual != expected:
        raise ProofError(f"{label} SHA-256 mismatch: expected {expected}, got {actual}")


def load_protocol(path: Path) -> ModuleType:
    require_hash(path, EXTRACTOR_SHA256, EXTRACTOR_NAME)
    spec = importlib.util.spec_from_file_location("pf_pool_46f4d0_protocol_pin", path)
    if spec is None or spec.loader is None:
        raise ProofError("cannot load pinned protocol extractor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def canonical_row_key(fieldnames: Sequence[str], row: Mapping[str, str]) -> str:
    payload = json.dumps([row[name] for name in fieldnames], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def make_delta_key(parts: Iterable[str]) -> str:
    return sha256_bytes("\x1f".join(parts).encode("utf-8"))


def read_tsv_with_lines(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ProofError(f"missing TSV header: {path}")
        return list(reader.fieldnames), [(line_no, dict(row)) for line_no, row in enumerate(reader, 2)]


def write_tsv_text(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
    handle = StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=list(columns), delimiter="\t", lineterminator="\n", extrasaction="raise")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue()


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    start_off = image.va_to_off(start_va)
    end_off = image.va_to_off(end_va)
    if start_off is None or end_off is None or end_off <= start_off:
        raise ProofError(f"unmapped span 0x{start_va:08X}..0x{end_va:08X}")
    return bytes(image.data[start_off:end_off])


def verify_span_pins(image) -> dict[str, int]:
    offsets = {}
    for pin in SPAN_PINS:
        actual = sha256_bytes(span_bytes(image, pin.start_va, pin.end_va))
        if actual != pin.sha256:
            raise ProofError(f"span {pin.name} mismatch: expected {pin.sha256}, got {actual}")
        off = image.va_to_off(pin.start_va)
        if off is None:
            raise ProofError(f"unmapped span start {pin.name}")
        offsets[pin.name] = off
    return offsets


def u32(image, va: int) -> int:
    off = image.va_to_off(va)
    if off is None:
        raise ProofError(f"unmapped u32 at 0x{va:08X}")
    return struct.unpack_from("<I", image.data, off)[0]


def decode_at(proto: ModuleType, image, va: int, end_va: int):
    limit = image.va_to_off(end_va)
    if limit is None:
        raise ProofError(f"unmapped decode limit 0x{end_va:08X}")
    return proto.decode_instruction(image, va, limit)


def require_operand(op, *, kind: str, reg: str | None = None, base: str | None = None, disp: int = 0, absolute: int | None = None, imm: int | None = None, label: str) -> None:
    if op is None or op.kind != kind:
        raise ProofError(f"{label}: expected {kind}, got {op}")
    if kind == "reg" and op.reg != reg:
        raise ProofError(f"{label}: expected register {reg}, got {op}")
    if kind == "imm" and op.imm != imm:
        raise ProofError(f"{label}: expected immediate 0x{imm or 0:08X}, got {op}")
    if kind == "mem" and (op.base != base or op.index is not None or op.disp != disp or op.absolute != absolute):
        raise ProofError(f"{label}: unexpected memory operand {op}")


def expect_mov_mem_to_reg(proto: ModuleType, image, va: int, end_va: int, dst: str, base: str, disp: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    require_operand(ins.dst, kind="reg", reg=dst, label=f"MOV dst 0x{va:08X}")
    require_operand(ins.src, kind="mem", base=base, disp=disp, absolute=None, label=f"MOV src 0x{va:08X}")


def expect_mov_reg_to_mem(proto: ModuleType, image, va: int, end_va: int, src: str, base: str, disp: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    require_operand(ins.dst, kind="mem", base=base, disp=disp, absolute=None, label=f"MOV dst 0x{va:08X}")
    require_operand(ins.src, kind="reg", reg=src, label=f"MOV src 0x{va:08X}")


def expect_mov_imm_to_mem(proto: ModuleType, image, va: int, end_va: int, value: int, base: str, disp: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    require_operand(ins.dst, kind="mem", base=base, disp=disp, absolute=None, label=f"MOV dst 0x{va:08X}")
    require_operand(ins.src, kind="imm", imm=value, label=f"MOV src 0x{va:08X}")


def expect_mov_reg_to_reg(proto: ModuleType, image, va: int, end_va: int, dst: str, src: str) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    require_operand(ins.dst, kind="reg", reg=dst, label=f"MOV dst 0x{va:08X}")
    require_operand(ins.src, kind="reg", reg=src, label=f"MOV src 0x{va:08X}")


def expect_mov_imm_to_reg(proto: ModuleType, image, va: int, end_va: int, dst: str, value: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    require_operand(ins.dst, kind="reg", reg=dst, label=f"MOV dst 0x{va:08X}")
    require_operand(ins.src, kind="imm", imm=value, label=f"MOV src 0x{va:08X}")


def expect_call(proto: ModuleType, image, va: int, end_va: int, target: int) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "call" or ins.target != target:
        raise ProofError(f"expected CALL 0x{target:08X} at 0x{va:08X}, got {ins}")


def expect_call_reg(proto: ModuleType, image, va: int, end_va: int, reg: str) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "call_indirect":
        raise ProofError(f"expected indirect CALL at 0x{va:08X}")
    require_operand(ins.src, kind="reg", reg=reg, label=f"CALL operand 0x{va:08X}")


def expect_push(proto: ModuleType, image, va: int, end_va: int, *, reg: str | None = None, imm: int | None = None) -> None:
    ins = decode_at(proto, image, va, end_va)
    if ins.kind != "push":
        raise ProofError(f"expected PUSH at 0x{va:08X}")
    if reg is not None:
        require_operand(ins.src, kind="reg", reg=reg, label=f"PUSH operand 0x{va:08X}")
    else:
        require_operand(ins.src, kind="imm", imm=imm, label=f"PUSH operand 0x{va:08X}")


def expect_cmp_regs(proto: ModuleType, image, va: int, end_va: int, left: str, right: str) -> None:
    ins = decode_at(proto, image, va, end_va)
    # The pinned V1 decoder intentionally does not assign semantic operands to
    # opcode 0x3B.  Keep this assertion independent and exact for the two forms
    # used by these roots.
    expected = {
        ("ecx", "ebx"): bytes.fromhex("3BCB"),
        ("ecx", "edi"): bytes.fromhex("3BCF"),
    }.get((left, right))
    if expected is None or ins.raw != expected:
        raise ProofError(f"expected CMP {left},{right} at 0x{va:08X}, got {ins.raw.hex()}")


def decode_pin(proto: ModuleType, image, pin: SpanPin):
    start_off = image.va_to_off(pin.start_va)
    end_off = image.va_to_off(pin.end_va)
    if start_off is None or end_off is None:
        raise ProofError(f"unmapped function pin {pin.name}")
    span = proto.FunctionSpan(pin.start_va, pin.end_va, start_off, end_off, pin.sha256)
    return proto.decode_function(image, span)


def call_census(decoded) -> tuple[Counter, list, list[int]]:
    direct = Counter()
    indirect = []
    returns = []
    for ins in decoded.instructions.values():
        if ins.kind == "call":
            direct[ins.target] += 1
        elif ins.kind == "call_indirect":
            indirect.append(ins)
        elif ins.kind == "ret":
            returns.append(ins.va)
    return direct, indirect, sorted(returns)


def verify_import(image, iat_va: int, dll: str, name: str) -> None:
    symbol = image.imports_by_iat.get(iat_va)
    if symbol is None or symbol.dll != dll or symbol.name != name:
        raise ProofError(f"IAT 0x{iat_va:08X}: expected {dll}!{name}, got {symbol}")


def verify_pool_identity(proto: ModuleType, image) -> dict[str, int]:
    expected_vtable = {0x00: 0x0046EC00, 0x04: POOL_DESTRUCTOR, 0x18: 0x0046E0A0, 0x34: POOL_SERIALIZER}
    for offset, expected in expected_vtable.items():
        actual = u32(image, POOL_VTABLE + offset)
        if actual != expected:
            raise ProofError(f"pool vtable +0x{offset:02X}: expected 0x{expected:08X}, got 0x{actual:08X}")

    needle = struct.pack("<I", POOL_VTABLE)
    refs = []
    cursor = 0
    while True:
        found = image.data.find(needle, cursor)
        if found < 0:
            break
        refs.append(found)
        cursor = found + 1
    expected_refs = [image.va_to_off(0x0046EBB8) + 2, image.va_to_off(0x0046F434) + 2]
    if refs != expected_refs:
        raise ProofError(f"pool vtable reference census mismatch: {refs}")

    helper = decode_pin(proto, image, SPAN_BY_NAME["pool_helper"])
    direct, indirect, returns = call_census(helper)
    expected_direct = Counter({
        0x0088D5B0: 1, 0x0049DA40: 1, 0x0088D020: 1, POOL_CTOR: 2,
        0x004160F0: 1, 0x00B37998: 1, 0x0088F350: 1, 0x0088D030: 1,
    })
    if helper.errors or direct != expected_direct or indirect or returns != [0x0046F59E, 0x0046F5D8]:
        raise ProofError(f"pool helper CFG mismatch: errors={helper.errors}, direct={direct}, indirect={indirect}, returns={returns}")

    ctor = decode_pin(proto, image, SPAN_BY_NAME["pool_ctor"])
    ctor_direct, ctor_indirect, ctor_returns = call_census(ctor)
    if ctor.errors or ctor_direct != Counter({0x00467650: 1, 0x0066A9D0: 1, 0x0046EA70: 1}) or ctor_indirect or ctor_returns != [0x0046F468]:
        raise ProofError("pool constructor CFG mismatch")
    expect_mov_reg_to_reg(proto, image, 0x0046F532, 0x0046F5DB, "ecx", "eax")
    expect_call(proto, image, 0x0046F534, 0x0046F5DB, POOL_CTOR)
    expect_mov_reg_to_reg(proto, image, 0x0046F5B0, 0x0046F5DB, "ecx", "eax")
    expect_call(proto, image, 0x0046F5B2, 0x0046F5DB, POOL_CTOR)
    expect_mov_imm_to_mem(proto, image, 0x0046F434, 0x0046F469, POOL_VTABLE, "esi", 0)
    expect_mov_reg_to_reg(proto, image, 0x0046F58A, 0x0046F5DB, "eax", "edi")
    return {"helper_instructions": len(helper.instructions), "ctor_instructions": len(ctor.instructions)}


EXPECTED_TEARDOWN_NODES = frozenset({
    0x00401030, 0x00467690, 0x00469E90, 0x0046D1B0, 0x0046D2B0, 0x0046D320,
    0x0046D370, 0x0046D3E0, 0x0046DB00, 0x0046E1B0, 0x0046E5E0, 0x0046EB90,
    0x0046F470, 0x004936D0, 0x0049DA50, 0x00524610, 0x005D2180, 0x006380D0,
    0x00638A80, 0x00638AD0, 0x00639260, 0x0074D4D0, 0x0088D280,
})
TEARDOWN_STOP_CALLS = frozenset({
    0x004024F0, 0x0049DA40, 0x0088D050, 0x0088D060, 0x0088D5B0,
    0x00B37952, 0x00B37998,
})
TEARDOWN_ABSOLUTE_INDIRECT = {
    0x00401058: 0x00C3B828,
    0x00401074: 0x00C3B49C,
    0x0046DB3C: 0x00C3B480,
    0x0046F4BF: 0x00C3B4A4,
    0x00638B0C: 0x00C3B480,
    0x0088D2CB: 0x00C3B8F8,
}
TEARDOWN_REGISTER_INDIRECT = {
    0x0046D2BF: "edi", 0x0046D2CA: "edi",
    0x0046E1D2: "ebp", 0x0046E1EF: "ebp", 0x0046E24A: "ebp",
    0x005D218F: "edi", 0x005D219A: "edi",
    0x00639282: "ebp", 0x0063929F: "ebp", 0x006392FA: "ebp",
}


def verify_teardown_graph(proto: ModuleType, image) -> int:
    verify_import(image, 0x00C3B4A4, "MSVCR90.dll", "free")
    verify_import(image, 0x00C3B4C0, "MSVCR90.dll", "_invalid_parameter_noinfo")
    verify_import(image, 0x00C3B480, "MSVCP90.dll", "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@PBD@Z")
    verify_import(image, 0x00C3B828, "MSVCR90.dll", "??0exception@std@@QAE@XZ")
    verify_import(image, 0x00C3B49C, "MSVCP90.dll", "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@ABV01@@Z")
    verify_import(image, 0x00C3B82C, "MSVCR90.dll", "??3@YAXPAX@Z")
    verify_import(image, 0x00C3B8F8, "USER32.dll", "MessageBoxW")
    verify_import(image, 0x00C3B168, "KERNEL32.dll", "LeaveCriticalSection")
    verify_import(image, 0x00C3B16C, "KERNEL32.dll", "EnterCriticalSection")
    verify_import(image, 0x00C3B1B0, "KERNEL32.dll", "InterlockedIncrement")
    verify_import(image, 0x00C3B1B4, "KERNEL32.dll", "InterlockedDecrement")
    verify_import(image, 0x00C3B87C, "MSVCR90.dll", "malloc")
    verify_import(image, 0x00C3B4C4, "MSVCR90.dll", "_CxxThrowException")
    verify_import(image, 0x00C3B19C, "KERNEL32.dll", "InterlockedExchangeAdd")

    queue = deque((POOL_DESTRUCTOR, 0x0088D280))
    seen = set()
    indirect_sites = {}
    while queue:
        start = queue.popleft()
        if start in seen:
            continue
        seen.add(start)
        span = proto.find_function_span(image, start)
        if span is None or span.start_va != start:
            raise ProofError(f"teardown function boundary unresolved at 0x{start:08X}")
        decoded = proto.decode_function(image, span)
        allowed_error = start == 0x00467690 and decoded.errors == ("edge_outside_span@0x00467696->0x0088D280",)
        if decoded.errors and not allowed_error:
            raise ProofError(f"teardown CFG error at 0x{start:08X}: {decoded.errors}")
        for ins in decoded.instructions.values():
            if ins.kind == "call":
                if ins.target in WIRE_PRIMITIVES:
                    raise ProofError(f"wire primitive reached from teardown at 0x{ins.va:08X}")
                if ins.target not in TEARDOWN_STOP_CALLS and ins.target is not None and image.executable_va(ins.target):
                    queue.append(ins.target)
            elif ins.kind == "call_indirect":
                indirect_sites[ins.va] = ins.src
    if frozenset(seen) != EXPECTED_TEARDOWN_NODES:
        raise ProofError(f"teardown node census mismatch: {sorted(seen)}")
    if set(indirect_sites) != set(TEARDOWN_ABSOLUTE_INDIRECT) | set(TEARDOWN_REGISTER_INDIRECT):
        raise ProofError(f"teardown indirect-call site census mismatch: {sorted(indirect_sites)}")
    for va, absolute in TEARDOWN_ABSOLUTE_INDIRECT.items():
        require_operand(indirect_sites[va], kind="mem", base=None, disp=0, absolute=absolute, label=f"teardown indirect 0x{va:08X}")
    for va, reg in TEARDOWN_REGISTER_INDIRECT.items():
        require_operand(indirect_sites[va], kind="reg", reg=reg, label=f"teardown indirect 0x{va:08X}")
    # The register-indirect sites above are fixed to _invalid_parameter_noinfo by
    # these exact absolute loads; span hashes and the site census prevent aliasing.
    for va, reg in ((0x0046E1B5, "ebp"), (0x00639265, "ebp"), (0x005D2187, "edi"), (0x0046D2B7, "edi")):
        ins = decode_at(proto, image, va, proto.find_function_span(image, va).end_va)
        if ins.kind != "mov":
            raise ProofError(f"expected invalid-parameter load at 0x{va:08X}")
        require_operand(ins.dst, kind="reg", reg=reg, label=f"invalid-parameter dst 0x{va:08X}")
        require_operand(ins.src, kind="mem", base=None, disp=0, absolute=0x00C3B4C0, label=f"invalid-parameter src 0x{va:08X}")
    # Verify the two tail thunks used by teardown/helper error paths.
    if span_bytes(image, 0x00B37952, 0x00B37958) != bytes.fromhex("FF252CB8C300"):
        raise ProofError("operator-delete tail thunk mismatch")
    if span_bytes(image, 0x00B37998, 0x00B3799E) != bytes.fromhex("FF25C4B4C300"):
        raise ProofError("throw tail thunk mismatch")
    return len(seen)


def verify_root(proto: ModuleType, image, root: RootSpec) -> int:
    pin = SPAN_BY_NAME[root.root_name]
    decoded = decode_pin(proto, image, pin)
    direct, indirect, _returns = call_census(decoded)
    writer_count = 4 if root.root_name == "actor_root" else 3 if root.root_name == "storage_root" else 1
    reader_count = writer_count
    expected_direct = Counter({0x0089A600: writer_count, 0x0089A640: reader_count, POOL_HELPER: 1, REF_DECREMENT: 1, REF_INCREMENT: 1})
    if decoded.errors or direct != expected_direct:
        raise ProofError(f"root direct-call census mismatch for {root.root_name}: {direct}, errors={decoded.errors}")
    if [(ins.va, ins.src.kind, ins.src.reg) for ins in sorted(indirect, key=lambda item: item.va)] != [
        (root.writer_call, "reg", "eax"), (root.reader_call, "reg", "eax")
    ]:
        raise ProofError(f"root indirect-call census mismatch for {root.root_name}")

    expect_mov_mem_to_reg(proto, image, root.writer_member_load, pin.end_va, "ecx", root.object_reg, root.member_offset)
    expect_mov_mem_to_reg(proto, image, root.writer_vtable_load, pin.end_va, "edx", "ecx", 0)
    expect_mov_mem_to_reg(proto, image, root.writer_slot_load, pin.end_va, "eax", "edx", 0x34)
    expect_push(proto, image, root.writer_mode_push, pin.end_va, reg="ebx")
    expect_push(proto, image, root.writer_stream_push, pin.end_va, reg=root.writer_stream_reg)
    expect_call_reg(proto, image, root.writer_call, pin.end_va, "eax")

    expect_push(proto, image, root.reader_helper_push_zero, pin.end_va, imm=0)
    expect_push(proto, image, root.reader_helper_push_token, pin.end_va, imm=POOL_TYPE_TOKEN)
    expect_mov_imm_to_reg(proto, image, root.reader_helper_pool_load, pin.end_va, "ecx", POOL_GLOBAL)
    expect_call(proto, image, root.reader_helper_call, pin.end_va, POOL_HELPER)
    expect_mov_mem_to_reg(proto, image, root.reader_old_load, pin.end_va, "ecx", root.object_reg, root.member_offset)
    new_reg = "ebx" if root.root_name == "actor_root" else "edi"
    expect_mov_reg_to_reg(proto, image, root.reader_new_copy, pin.end_va, new_reg, "eax")
    expect_cmp_regs(proto, image, root.reader_compare, pin.end_va, "ecx", new_reg)
    expect_call(proto, image, root.reader_decrement, pin.end_va, REF_DECREMENT)
    expect_mov_reg_to_mem(proto, image, root.reader_store, pin.end_va, new_reg, root.object_reg, root.member_offset)
    expect_mov_reg_to_reg(proto, image, root.reader_increment_this, pin.end_va, "ecx", new_reg)
    expect_call(proto, image, root.reader_increment, pin.end_va, REF_INCREMENT)
    expect_mov_mem_to_reg(proto, image, root.reader_reload, pin.end_va, root.reader_reload_reg, root.object_reg, root.member_offset)
    expect_mov_mem_to_reg(proto, image, root.reader_vtable_load, pin.end_va, "edx", root.reader_reload_reg, 0)
    expect_mov_mem_to_reg(proto, image, root.reader_slot_load, pin.end_va, "eax", "edx", 0x34)
    expect_push(proto, image, root.reader_mode_push, pin.end_va, imm=0)
    if root.reader_this_move is not None:
        expect_mov_reg_to_reg(proto, image, root.reader_this_move, pin.end_va, "ecx", root.reader_reload_reg)
    expect_push(proto, image, root.reader_stream_push, pin.end_va, reg=root.reader_stream_reg)
    expect_call_reg(proto, image, root.reader_call, pin.end_va, "eax")
    return len(decoded.instructions)


def verify_message_provenance(proto: ModuleType, image, spec: MessageSpec) -> None:
    root = ROOTS[spec.root_name]
    ctor_pin = SPAN_BY_NAME[spec.root_name.replace("root", "ctor")]
    core_pin = SPAN_BY_NAME[spec.root_name.replace("root", "core_dtor")]
    wrapper_pin = SPAN_BY_NAME[spec.root_name.replace("root", "dtor_wrapper")]
    expect_mov_imm_to_mem(proto, image, spec.ctor_vtable_store, ctor_pin.end_va, spec.message_vtable, spec.ctor_object_reg, 0)
    expect_mov_reg_to_mem(proto, image, spec.ctor_member_store, ctor_pin.end_va, spec.zero_reg, spec.ctor_object_reg, root.member_offset)
    expect_call(proto, image, spec.wrapper_core_call, wrapper_pin.end_va, spec.core_dtor)
    expect_mov_mem_to_reg(proto, image, spec.core_member_load, core_pin.end_va, "ecx", "esi", root.member_offset)
    expect_call(proto, image, spec.core_member_decrement, core_pin.end_va, REF_DECREMENT)
    if u32(image, spec.message_vtable + 4) != spec.wrapper_dtor or u32(image, spec.message_vtable + 0x18) != root.root_va:
        raise ProofError(f"message vtable mapping mismatch for {spec.message}")
    needle = struct.pack("<I", spec.message_vtable)
    refs = []
    cursor = 0
    while True:
        found = image.data.find(needle, cursor)
        if found < 0:
            break
        refs.append(found)
        cursor = found + 1
    sites = [spec.ctor_vtable_store]
    if spec.message != "CollectionObj_UpdateCollectionObjBagVital":
        sites.append(spec.core_dtor + 0x28)
    expected = []
    for va in sites:
        ins = decode_at(proto, image, va, (ctor_pin if va == spec.ctor_vtable_store else core_pin).end_va)
        expected.append(image.va_to_off(va) + ins.size - 4)
    if refs != sorted(expected):
        raise ProofError(f"message vtable reference census mismatch for {spec.message}: {refs}")


def verify_registry(path: Path) -> None:
    fields, rows = read_tsv_with_lines(path)
    required = {"name", "vtable_va", "serializer_va", "source"}
    if not required <= set(fields):
        raise ProofError("A1 registry schema mismatch")
    selected = {row["name"]: row for _line, row in rows if row["name"] in MESSAGE_BY_NAME}
    if set(selected) != set(TARGET_NAMES):
        raise ProofError("A1 target census mismatch")
    for name, spec in MESSAGE_BY_NAME.items():
        root = ROOTS[spec.root_name]
        row = selected[name]
        if row["vtable_va"] != f"0x{spec.message_vtable:08X}" or row["serializer_va"] != f"0x{root.root_va:08X}" or row["source"] != "IMAGE":
            raise ProofError(f"A1 mapping mismatch for {name}")


def verify_post_v1_priority_overlay(path: Path) -> None:
    fields, rows = read_tsv_with_lines(path)
    required = {"base_file", "base_row_key", "message", "action", "new_serializer_status", "new_structural_status", "source"}
    if not required <= set(fields):
        raise ProofError("post-V1 priority overlay schema mismatch")
    if any(row["message"] in MESSAGE_BY_NAME for _line, row in rows):
        raise ProofError("post-V1 priority overlay already touches a pool target")
    if any(row["base_file"] != PRIORITY_NAME or row["action"] != "CHANGED" or row["source"] != "IMAGE" for _line, row in rows):
        raise ProofError("post-V1 priority overlay contains an unexpected directive")


def expected_tag(root: RootSpec) -> str:
    return f"CALL_UNCLASSIFIED:INDIRECT(DEREF(DEREF(DEREF(OBJ+0x{root.member_offset:X}))+0x34))"


def select_a2_row(rows: Sequence[tuple[int, dict[str, str]]], message: str, direction: str, file_off: int, tag: str) -> tuple[int, dict[str, str]]:
    wanted_off = f"0x{file_off:08X}"
    matches = [(line, row) for line, row in rows if row["message"] == message and row["direction(W/R)"] == direction and row["file_off_claim"] == wanted_off and row["tag"] == tag]
    if len(matches) != 1:
        raise ProofError(f"A2 selection {message}/{direction}/{wanted_off}/{tag}: {len(matches)} rows")
    return matches[0]


def build_a2_delta(image, fields: Sequence[str], rows: Sequence[tuple[int, dict[str, str]]]) -> list[dict[str, str]]:
    output = []
    for spec in MESSAGES:
        root = ROOTS[spec.root_name]
        pin = SPAN_BY_NAME[root.root_name]
        indirect_tag = expected_tag(root)
        sites = (
            (root.writer_call, "W", "CHANGED", "RESOLVE_FIXED_VTABLE_PLUS_34_SUBCALL", "WRITER_MEMBER_FIXED_POOL_SUBCALL"),
            (root.writer_call, "R", "REMOVE_NONWIRE_ROW", "DIRECTION_CROSS_PRODUCT_ARTIFACT", "WRITER_SITE_NOT_READER"),
            (root.reader_call, "R", "CHANGED", "RESOLVE_FIXED_VTABLE_PLUS_34_SUBCALL", "READER_HELPER_RESULT_FIXED_POOL_SUBCALL"),
            (root.reader_call, "W", "REMOVE_NONWIRE_ROW", "DIRECTION_CROSS_PRODUCT_ARTIFACT", "READER_SITE_NOT_WRITER"),
        )
        for call_va, direction, action, change_type, resolution in sites:
            off = image.va_to_off(call_va)
            if off is None:
                raise ProofError("unmapped root call site")
            line, row = select_a2_row(rows, spec.message, direction, off, indirect_tag)
            changed = action == "CHANGED"
            output.append({
                "delta_key": make_delta_key((A2_NAME, str(line), canonical_row_key(fields, row), action)),
                "action": action,
                "change_type": change_type,
                "base_file": A2_NAME,
                "base_line": str(line),
                "base_row_key": canonical_row_key(fields, row),
                "message": spec.message,
                "direction(W/R)": direction,
                "old_order": row["order"],
                "old_tag": row["tag"],
                "old_field_offset": row["field_offset"],
                "old_len": row["len"],
                "new_wire_order": row["order"] if changed else "N/A",
                "new_tag": f"SUBCALL:0x{POOL_SERIALIZER:08X}" if changed else "N/A",
                "new_field_offset": f"DEREF(+0x{root.member_offset:X})" if changed else "N/A",
                "new_len": "N/A",
                "new_gate_condition": (f"+0x{root.member_offset:X}!=NULL" if direction == "W" else "DECODED_PRESENCE_FLAG!=0") if changed else "N/A",
                "resolution": resolution,
                "evidence_ticket": "POOL_46F4D0",
                "evidence_span_start": f"0x{pin.start_va:08X}",
                "evidence_span_end": f"0x{pin.end_va:08X}",
                "evidence_span_sha256": pin.sha256,
                "evidence_file_off": f"0x{off:08X}",
                "source": "IMAGE",
            })
        lifecycle = (
            (root.reader_helper_call, f"CALL_UNCLASSIFIED:0x{POOL_HELPER:08X}", "OBJECT_POOL_ACQUIRE_FIXED_VTABLE_NO_STREAM_ALIAS"),
            (root.reader_decrement, "DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04", "FIXED_POOL_REFCOUNT_DECREMENT_TEARDOWN_NONWIRE"),
            (root.reader_increment, "ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C", "FIXED_NEW_OBJECT_REFCOUNT_INCREMENT_NONWIRE"),
        )
        for call_va, tag, resolution in lifecycle:
            off = image.va_to_off(call_va)
            if off is None:
                raise ProofError("unmapped lifecycle call site")
            for direction in ("R", "W"):
                line, row = select_a2_row(rows, spec.message, direction, off, tag)
                output.append({
                    "delta_key": make_delta_key((A2_NAME, str(line), canonical_row_key(fields, row), "REMOVE_NONWIRE_ROW")),
                    "action": "REMOVE_NONWIRE_ROW",
                    "change_type": "NONWIRE_LIFECYCLE_OR_POOL_ARTIFACT",
                    "base_file": A2_NAME,
                    "base_line": str(line),
                    "base_row_key": canonical_row_key(fields, row),
                    "message": spec.message,
                    "direction(W/R)": direction,
                    "old_order": row["order"],
                    "old_tag": row["tag"],
                    "old_field_offset": row["field_offset"],
                    "old_len": row["len"],
                    "new_wire_order": "N/A", "new_tag": "N/A", "new_field_offset": "N/A", "new_len": "N/A", "new_gate_condition": "N/A",
                    "resolution": resolution,
                    "evidence_ticket": "POOL_46F4D0",
                    "evidence_span_start": f"0x{pin.start_va:08X}",
                    "evidence_span_end": f"0x{pin.end_va:08X}",
                    "evidence_span_sha256": pin.sha256,
                    "evidence_file_off": f"0x{off:08X}",
                    "source": "IMAGE",
                })
    output.sort(key=lambda row: (row["message"], int(row["base_line"])))
    return output


def build_priority_delta(fields: Sequence[str], rows: Sequence[tuple[int, dict[str, str]]]) -> list[dict[str, str]]:
    output = []
    for message in TARGET_NAMES:
        matches = [(line, row) for line, row in rows if row["message"] == message]
        if len(matches) != 1:
            raise ProofError(f"priority selection {message}: {len(matches)} rows")
        line, row = matches[0]
        if row["priority"] != "1" or row["serializer_status"] != "OPEN" or row["structural_status"] != "OPEN" or row["source"] != "IMAGE":
            raise ProofError(f"priority base state mismatch for {message}")
        key = canonical_row_key(fields, row)
        output.append({
            "delta_key": make_delta_key((PRIORITY_NAME, str(line), key, "CHANGED")),
            "action": "CHANGED", "base_file": PRIORITY_NAME, "base_line": str(line), "base_row_key": key,
            "message": message, "priority": "1", "old_serializer_status": "OPEN", "new_serializer_status": "CLOSED",
            "old_structural_status": "OPEN", "new_structural_status": "CLOSED", "old_blocker": row["blocker"], "new_blocker": "N/A",
            "evidence_ticket": "POOL_46F4D0",
            "closure_scope": "FIXED_POOL_VTABLE_PLUS_0X34_SUBCALL_RESOLVED;LIFECYCLE_ROWS_REMOVED;NESTED_SERIALIZER_REFERENCED_NOT_FLATTENED",
            "source": "IMAGE",
        })
    return output


def validate_delta(a2_delta: Sequence[Mapping[str, str]], priority_delta: Sequence[Mapping[str, str]]) -> None:
    if len(a2_delta) != 40 or Counter(row["action"] for row in a2_delta) != Counter({"REMOVE_NONWIRE_ROW": 32, "CHANGED": 8}):
        raise ProofError("A2 delta census mismatch")
    if len(priority_delta) != 4 or any(row["action"] != "CHANGED" for row in priority_delta):
        raise ProofError("priority delta census mismatch")
    for rows in (a2_delta, priority_delta):
        if any(row["source"] != "IMAGE" for row in rows):
            raise ProofError("non-IMAGE row in IMAGE overlay")
        if len({row["delta_key"] for row in rows}) != len(rows) or len({row["base_row_key"] for row in rows}) != len(rows):
            raise ProofError("duplicate delta/base key")
    if set(row["message"] for row in priority_delta) != set(TARGET_NAMES):
        raise ProofError("priority target set mismatch")


def overlay_census(external_dir: Path) -> tuple[tuple[str, str], ...]:
    own = {A2_DELTA_NAME, PRIORITY_DELTA_NAME}
    return tuple((path.name, sha256_path(path)) for path in sorted(external_dir.glob("*DELTA.tsv")) if path.name not in own)


def validate_no_existing_overlap(external_dir: Path, a2_delta: Sequence[Mapping[str, str]], priority_delta: Sequence[Mapping[str, str]]) -> None:
    own = {A2_DELTA_NAME, PRIORITY_DELTA_NAME}
    wanted = {(row["base_file"], row["base_row_key"]) for row in (*a2_delta, *priority_delta)}
    for path in sorted(external_dir.glob("*DELTA.tsv")):
        if path.name in own:
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if reader.fieldnames is None or not {"base_file", "base_row_key"} <= set(reader.fieldnames):
                continue
            for row in reader:
                if (row["base_file"], row["base_row_key"]) in wanted:
                    raise ProofError(f"existing overlay overlap: {path.name} {(row['base_file'], row['base_row_key'])}")


def validate_string_overlay(path: Path, a2_delta: Sequence[Mapping[str, str]]) -> None:
    fields, rows = read_tsv_with_lines(path)
    required = {"base_row_number", "message", "delta_action", "source"}
    if not required <= set(fields):
        raise ProofError("string correction schema mismatch")
    string_lines = {int(row["base_row_number"]) for _line, row in rows}
    our_lines = {int(row["base_line"]) for row in a2_delta}
    if string_lines & our_lines or any(row["message"] in MESSAGE_BY_NAME for _line, row in rows):
        raise ProofError("string correction overlaps pool A2 directives")
    if any(row["delta_action"] != "CHANGED" or row["source"] != "IMAGE" for _line, row in rows):
        raise ProofError("string correction contains unexpected directive")


def validate_post_overlay_closure(a2_fields: Sequence[str], a2_rows: Sequence[tuple[int, dict[str, str]]], delta: Sequence[Mapping[str, str]]) -> None:
    directives = {row["base_row_key"]: row for row in delta}
    for _line, row in a2_rows:
        if row["message"] not in MESSAGE_BY_NAME:
            continue
        key = canonical_row_key(a2_fields, row)
        directive = directives.get(key)
        if directive is not None and directive["action"] == "REMOVE_NONWIRE_ROW":
            continue
        tag = directive["new_tag"] if directive is not None and directive["action"] == "CHANGED" else row["tag"]
        field = directive["new_field_offset"] if directive is not None and directive["action"] == "CHANGED" else row["field_offset"]
        if "UNKNOWN(" in tag or "UNKNOWN(" in field or tag.startswith("CALL_UNCLASSIFIED:") or tag.startswith("DYNAMIC_") or tag.startswith("ATOMIC_"):
            raise ProofError(f"residual unresolved target row: {row['message']} {tag} {field}")


class MutatedImage:
    def __init__(self, base, data: bytes):
        self._base = base
        self.data = data
        self.imports_by_iat = base.imports_by_iat

    def __getattr__(self, name):
        return getattr(self._base, name)

    def va_to_off(self, va: int):
        return self._base.va_to_off(va)


def run_mutation_guards(proto: ModuleType, image) -> None:
    def mutate_u32(va: int, value: int):
        data = bytearray(image.data)
        off = image.va_to_off(va)
        if off is None:
            raise ProofError("mutation VA unmapped")
        struct.pack_into("<I", data, off, value)
        return MutatedImage(image, bytes(data))

    def mutate_byte(va: int, value: int):
        data = bytearray(image.data)
        off = image.va_to_off(va)
        if off is None:
            raise ProofError("mutation VA unmapped")
        data[off] = value
        return MutatedImage(image, bytes(data))

    controls = (
        ("vtable_slot", mutate_u32(POOL_VTABLE + 0x34, POOL_SERIALIZER + 1), lambda candidate: verify_pool_identity(proto, candidate)),
        ("helper_ctor_target", mutate_byte(0x0046F535, (image.data[image.va_to_off(0x0046F535)] + 1) & 0xFF), lambda candidate: verify_pool_identity(proto, candidate)),
        ("root_slot_disp", mutate_byte(0x005EACF8, 0x30), lambda candidate: verify_root(proto, candidate, ROOTS["actor_root"])),
    )
    for label, candidate, verifier in controls:
        try:
            verifier(candidate)
        except ProofError:
            continue
        raise ProofError(f"negative mutation unexpectedly accepted: {label}")


def report_text(root_counts: Mapping[str, int], pool_counts: Mapping[str, int], teardown_nodes: int) -> str:
    root_rows = []
    for spec in MESSAGES:
        root = ROOTS[spec.root_name]
        pin = SPAN_BY_NAME[root.root_name]
        root_rows.append(
            f"| `{spec.message}` | `+0x{root.member_offset:X}` | `0x{pin.start_va:08X}..0x{pin.end_va:08X}` | `{pin.sha256}` | `0x{root.writer_call:08X}` | `0x{root.reader_call:08X}` |"
        )
    return "\n".join((
        "# PF pool 0x0046F4D0 closure overlay",
        "",
        "[MEASURED] IMAGE-only additive result. V1 remains immutable.",
        "",
        "## Result",
        "",
        "The four requested Priority-1 messages are structurally CLOSED in this isolated overlay:",
        "",
        *[f"- `{name}`" for name in TARGET_NAMES],
        "",
        "Isolated priority effect: **+4 CLOSED**. No combined project headline is claimed here because independent overlays may be applied in either order.",
        "",
        "The A2 overlay contains 40 exact V1 directives: 8 `CHANGED` indirect rows become `SUBCALL:0x0046F180`; 32 rows are removed (8 cross-direction artifacts and 24 pool/refcount lifecycle artifacts). The priority overlay contains 4 exact V1 `OPEN -> CLOSED` directives. Unchanged rows copied: 0. Duplicate delta keys: 0. Duplicate base keys: 0. Existing-overlay base-key overlap: 0.",
        "",
        f"The current post-V1 priority overlay is pinned at sha256 `{POST_V1_PRIORITY_SHA256}` and touches none of these four base rows. The string-wire correction is pinned at sha256 `{STRING_DELTA_SHA256}` and has zero base-key overlap with these A2 directives; its rows are not duplicated here.",
        "",
        "## Fixed pool identity",
        "",
        f"- Helper `0x{POOL_HELPER:08X}` has {pool_counts['helper_instructions']} reachable instructions in exact span `0x0046F4D0..0x0046F5DB` (sha256 `b9308abc49969ded9194d369823de1f29207ca8addcfe22f838a4b3d1ea45885`). Both allocation/reuse arms call constructor `0x{POOL_CTOR:08X}`; the constructor has {pool_counts['ctor_instructions']} reachable instructions and stores vtable `0x{POOL_VTABLE:08X}`.",
        f"- Vtable `0x{POOL_VTABLE:08X}` has destructor slot `+0x04 -> 0x{POOL_DESTRUCTOR:08X}` and serializer slot `+0x34 -> 0x{POOL_SERIALIZER:08X}`. The serializer body is pinned at `0x0046F180..0x0046F3E9`, sha256 `29e38267ab54c852e3f1338c2fb833e3b9d1a41903544a390489c264c09fa813`.",
        f"- The exact teardown walk contains {teardown_nodes} internal CFG nodes. It reaches no wire primitive. Every indirect call is either a pinned non-wire import or a register loaded from `_invalid_parameter_noinfo`; refcount recursion is stopped at the separately pinned `InterlockedDecrement` helper because no stream alias is passed.",
        "",
        "## Serializer roots and call sites",
        "",
        "| message | member | exact root span | span sha256 | W subcall | R subcall |",
        "|---|---:|---|---|---:|---:|",
        *root_rows,
        "",
        "Each writer path loads the member, its vtable, and slot `+0x34`, then passes the root stream and writer mode. Each reader path calls `0x0046F4D0`, stores that exact result into the same member, increments its reference, reloads the member, and calls the same `+0x34` slot with reader mode zero. Constructors initialize each member to null; the corresponding destructor path decrements that same member. All four message-vtable reference censuses and vtable-to-root mappings are exact.",
        "",
        "Root reachable-instruction counts: " + ", ".join(f"`{name}`={root_counts[name]}" for name in sorted(root_counts)) + ".",
        "",
        "## Evidence boundary",
        "",
        "This closes static wire structure only. `0x0046F180` is referenced as a nested serializer and is not flattened into these four message rows. Runtime semantics, current object contents, and capture agreement are not promoted. Every emitted TSV row is `source=IMAGE`; no DUMP, CAPTURE, or DATA fact is mixed into the overlay.",
        "",
        "Publication is atomic per file, not as a multi-file set. The final V2 manifest remains the set-level commit point.",
        "",
        "## Reproduction",
        "",
        "```powershell",
        "py -3 pf_build_pool_46f4d0_closure.py --check",
        "```",
        "",
    ))


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", type=Path, default=here.parent.parent / "GameClient" / "GameClient.local.bin")
    parser.add_argument("--external", type=Path, default=here)
    parser.add_argument("--check", action="store_true", help="verify current outputs without writing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    external = args.external.resolve()
    client = args.client.resolve()
    extractor_path = external / EXTRACTOR_NAME
    a1_path = external / A1_NAME
    a2_path = external / A2_NAME
    priority_path = external / PRIORITY_NAME
    post_priority_path = external / POST_V1_PRIORITY_NAME
    string_delta_path = external / STRING_DELTA_NAME

    pinned = (
        (client, IMAGE_SHA256, "GameClient.local.bin"),
        (extractor_path, EXTRACTOR_SHA256, EXTRACTOR_NAME),
        (a1_path, A1_SHA256, A1_NAME),
        (a2_path, A2_SHA256, A2_NAME),
        (priority_path, PRIORITY_SHA256, PRIORITY_NAME),
        (post_priority_path, POST_V1_PRIORITY_SHA256, POST_V1_PRIORITY_NAME),
        (string_delta_path, STRING_DELTA_SHA256, STRING_DELTA_NAME),
    )
    for path, expected, label in pinned:
        require_hash(path, expected, label)
    if client.stat().st_size != IMAGE_SIZE:
        raise ProofError(f"image size mismatch: expected {IMAGE_SIZE}, got {client.stat().st_size}")
    protocol = load_protocol(extractor_path)
    image = protocol.Image(client)
    overlay_before = overlay_census(external)

    offsets = verify_span_pins(image)
    pool_counts = verify_pool_identity(protocol, image)
    teardown_nodes = verify_teardown_graph(protocol, image)
    root_counts = {name: verify_root(protocol, image, root) for name, root in ROOTS.items()}
    for message in MESSAGES:
        verify_message_provenance(protocol, image, message)
    verify_registry(a1_path)
    verify_post_v1_priority_overlay(post_priority_path)
    run_mutation_guards(protocol, image)

    a2_fields, a2_rows = read_tsv_with_lines(a2_path)
    priority_fields, priority_rows = read_tsv_with_lines(priority_path)
    a2_delta = build_a2_delta(image, a2_fields, a2_rows)
    priority_delta = build_priority_delta(priority_fields, priority_rows)
    validate_delta(a2_delta, priority_delta)
    validate_string_overlay(string_delta_path, a2_delta)
    validate_no_existing_overlap(external, a2_delta, priority_delta)
    validate_post_overlay_closure(a2_fields, a2_rows, a2_delta)

    contents = {
        A2_DELTA_NAME: write_tsv_text(A2_DELTA_COLUMNS, a2_delta),
        PRIORITY_DELTA_NAME: write_tsv_text(PRIORITY_DELTA_COLUMNS, priority_delta),
        REPORT_NAME: report_text(root_counts, pool_counts, teardown_nodes),
    }

    # Re-pin every input and the complete pre-existing overlay census before any
    # publication. This prevents a concurrent writer from producing a mixed proof.
    for path, expected, label in pinned:
        require_hash(path, expected, label)
    if overlay_census(external) != overlay_before:
        raise ProofError("overlay census changed during generation")
    validate_no_existing_overlap(external, a2_delta, priority_delta)

    if args.check:
        for name, expected in contents.items():
            path = external / name
            if not path.is_file():
                raise ProofError(f"missing output in --check mode: {name}")
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                raise ProofError(f"stale output in --check mode: {name}")
    else:
        for name, content in contents.items():
            atomic_write_text(external / name, content)
        for name, expected in contents.items():
            if (external / name).read_text(encoding="utf-8") != expected:
                raise ProofError(f"post-publication verification failed: {name}")

    result = {
        "mode": "check" if args.check else "publish",
        "a2_rows": len(a2_delta),
        "a2_changed": Counter(row["action"] for row in a2_delta)["CHANGED"],
        "a2_removed": Counter(row["action"] for row in a2_delta)["REMOVE_NONWIRE_ROW"],
        "priority_rows": len(priority_delta),
        "teardown_nodes": teardown_nodes,
        "outputs": {name: sha256_bytes(content.encode("utf-8")) for name, content in contents.items()},
        "source": "IMAGE",
        "span_offsets": offsets,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProofError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
