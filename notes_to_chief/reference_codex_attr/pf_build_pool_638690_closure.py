#!/usr/bin/env python3
"""Build the fail-closed IMAGE overlay for the 0x00638690 object pool.

The generator is deliberately additive.  It never edits V1 and emits only
base-keyed CHANGED/REMOVE directives for four explicitly named messages.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import struct
import tempfile
from collections import Counter, deque
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable, Mapping, Sequence


IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
A1_SHA256 = "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d"
A2_SHA256 = "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
PRIORITY_SHA256 = "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"
POST_V1_PRIORITY_SHA256 = "69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51"

A1_NAME = "PF_PROTOCOL_REGISTRY.tsv"
A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
PRIORITY_NAME = "PF_PROTOCOL_PRIORITY.tsv"
POST_V1_PRIORITY_NAME = "PF_POST_V1_PRIORITY_DELTA.tsv"
A2_DELTA_NAME = "PF_A2_POOL_638690_DELTA.tsv"
PRIORITY_DELTA_NAME = "PF_PRIORITY_POOL_638690_DELTA.tsv"
REPORT_NAME = "PF_POOL_638690_CLOSURE.md"

POOL_HELPER = 0x00638690
POOL_VTABLE = 0x00F3568C
POOL_SERIALIZER = 0x00637FC0
POOL_DESTRUCTOR = 0x00638370
REF_INCREMENT = 0x0088D050
REF_DECREMENT = 0x0088D060
POOL_GLOBAL = 0x0102FB94
POOL_TYPE_TOKEN = 0x00F0A90C

WIRE_PRIMITIVES = frozenset((0x0089A600, 0x0089A640, 0x0089A810, 0x0089A880))


@dataclass(frozen=True)
class SpanPin:
    name: str
    start_va: int
    end_va: int
    sha256: str


SPAN_PINS = (
    SpanPin("pool_helper", 0x00638690, 0x006387D9, "cc56e669d0f3c5c714f2f00780b946c7ab9930407d0d8a324380dc3fbbcfecbd"),
    SpanPin("pool_ctor", 0x00637BF0, 0x00637CA5, "79197e61451c762758c8430e863cc6bf8752f48179226e92b9ac0a1da894d58d"),
    SpanPin("pool_base_serializer", 0x00637CC0, 0x00637E05, "7037b86c221f423f84e056820a7b72d7772d27b4b36acb0cd409c54dea05586b"),
    SpanPin("pool_serializer", 0x00637FC0, 0x00638035, "66073191421eb2b758f27584a3d4ea96a2712ce1011725f73de1c792a373e240"),
    SpanPin("pool_dtor", 0x00638370, 0x006383CE, "7b848f45d7cb2a79f793fd3b600058c820da42c27afcd59299095f1bd2605f3a"),
    SpanPin("pool_base_dtor", 0x00637830, 0x006378B3, "5fe2bc775355de8b676f44c55f693a45786ef5bff4f795e1ad98453c67557d0c"),
    SpanPin("base_object_dtor", 0x0088D280, 0x0088D2F0, "d914c8eaef424f2988c6b76b6954acbb9247bd4309a2c8f0e09439cc64f1104a"),
    SpanPin("pool_lock", 0x0088D5B0, 0x0088D5BA, "281bb0603facf9b7c61c87c0241b74e59ff6488057f979782e4d08ea4e4e9ee8"),
    SpanPin("pool_unlock", 0x0049DA40, 0x0049DA4A, "91f8bd361459e6514e2c53ca4bac3bd9d76baddaf75ee1b1562afecee8d96366"),
    SpanPin("ref_increment", 0x0088D050, 0x0088D05B, "6da78a1acc15d9fd5f7b2d620253debf8d8465136165dfb1eae35914b2442845"),
    SpanPin("ref_decrement", 0x0088D060, 0x0088D082, "d3b546ac50ded491a6c5a196138b9691f23d8499298e728925f1afb1f0e7734c"),
    SpanPin("root_member_48", 0x006448A0, 0x0064498F, "645560a112bc5938b11bea612cf90299958cc15b57fe1adb30fffddfde8231cf"),
    SpanPin("root_member_2c", 0x00644A50, 0x00644B29, "c90a027c309ab7e20f0f9b63840ef4149774ccccb9ac2aff7d43e3ef1150f1ca"),
    SpanPin("root_member_34", 0x00644C10, 0x00644D51, "78fcc7ddb3cca5009ff13cac567977efaef2825c20e260c6ea3fe61f4954ee83"),
    SpanPin("friend_ctor", 0x0063A520, 0x0063A597, "e9e6a203585c02cbdf8e805b19cf35eabf680220a3e85811ffd86fd0dd949160"),
    SpanPin("black_ctor", 0x0063A6F0, 0x0063A76A, "edf2754cfb2fccbf9ce7bc494190e4a3f04595938f700809028bf89f31eb8853"),
    SpanPin("soul_ctor", 0x0063ACC0, 0x0063AD20, "ec455072d2af97c49825fbe3d238f3ed2ab37862737c5acb9668b26a98955755"),
    SpanPin("reply_ctor", 0x0063B090, 0x0063B108, "3eed3f080f625de9ff60c84901ed364882df95fa98248a0d136f545192caf38b"),
    SpanPin("member_48_dtor", 0x0063A790, 0x0063A800, "bed8ddbfb4922d02aa7d3cff41dc88b8bf625301c168011665930a61f5c58c4e"),
    SpanPin("member_2c_dtor", 0x0063AD40, 0x0063ADA2, "89e19dd8d7688854dd17144ae558dc10c38a8fd67d6c13d5b4e2e8349229d2ff"),
    SpanPin("member_34_dtor", 0x0063B140, 0x0063B1A2, "825a5dfde31183f5aec70584c845b08146b337c51c8a31e92babe74f407f5ef4"),
    SpanPin("friend_wrapper_dtor", 0x0063B9B0, 0x0063BA0E, "2be14d3c0f4a2fb5e59ba43b456b3d27f9494dc4cb7347717f2c78b6bfb7884f"),
    SpanPin("black_wrapper_dtor", 0x0063BB90, 0x0063BBEE, "4b56e149996b856fe4d1d1d57bd7471866ffe377da15ba0c01c8064af37a9f90"),
    SpanPin("soul_wrapper_dtor", 0x0063C070, 0x0063C0CE, "9ee439ed4a3ec7db833836143d19cea9d4188d6290ef89bc409d63ff8b3ceac3"),
    SpanPin("reply_wrapper_dtor", 0x0063C3D0, 0x0063C42E, "4031476420e50b40da95585cac3ef45c78f63e7e11ef3942e59b975698eda554"),
    SpanPin("pool_vtable_prefix", 0x00F3568C, 0x00F356A4, "c63c641d579e046481fce29c3c61d5356abe89ba227e60a4cb87e656e7580325"),
)
SPAN_BY_NAME = {span.name: span for span in SPAN_PINS}


@dataclass(frozen=True)
class RootSpec:
    root_name: str
    root_va: int
    member_offset: int
    object_reg: str
    stream_reg: str
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
    reader_vtable_load: int
    reader_slot_load: int
    reader_mode_push: int
    reader_stream_push: int
    reader_call: int


ROOTS = {
    "root_member_48": RootSpec(
        "root_member_48", 0x006448A0, 0x48, "esi", "edi",
        0x00644912, 0x00644915, 0x00644917, 0x0064491A, 0x0064491B, 0x0064491C,
        0x00644945, 0x00644947, 0x0064494C, 0x00644951, 0x00644956, 0x00644959,
        0x0064495B, 0x00644963, 0x00644968, 0x0064496F, 0x00644971, 0x00644976,
        0x0064497D, 0x0064497F, 0x00644982, 0x00644986, 0x00644987,
    ),
    "root_member_2c": RootSpec(
        "root_member_2c", 0x00644A50, 0x2C, "esi", "edi",
        0x00644AAC, 0x00644AAF, 0x00644AB1, 0x00644AB4, 0x00644AB5, 0x00644AB6,
        0x00644ADF, 0x00644AE1, 0x00644AE6, 0x00644AEB, 0x00644AF0, 0x00644AF3,
        0x00644AF5, 0x00644AFD, 0x00644B02, 0x00644B09, 0x00644B0B, 0x00644B10,
        0x00644B17, 0x00644B19, 0x00644B1C, 0x00644B20, 0x00644B21,
    ),
    "root_member_34": RootSpec(
        "root_member_34", 0x00644C10, 0x34, "edi", "esi",
        0x00644CD4, 0x00644CD7, 0x00644CD9, 0x00644CDC, 0x00644CDD, 0x00644CDE,
        0x00644D07, 0x00644D09, 0x00644D0E, 0x00644D13, 0x00644D18, 0x00644D1B,
        0x00644D1D, 0x00644D25, 0x00644D2A, 0x00644D31, 0x00644D33, 0x00644D38,
        0x00644D3F, 0x00644D41, 0x00644D44, 0x00644D48, 0x00644D49,
    ),
}


@dataclass(frozen=True)
class MessageSpec:
    message: str
    root_name: str
    message_vtable: int
    ctor_zero_seed: int
    ctor_vtable_store: int
    ctor_member_store: int
    ctor_object_reg: str
    zero_reg: str
    member_dtor_load: int
    member_dtor_decrement: int
    wrapper_dtor: int
    member_dtor: int


MESSAGES = (
    MessageSpec("Community_AddFriendVital", "root_member_48", 0x00F35C2C, 0x0063A549, 0x0063A570, 0x0063A580, "esi", "ebx", 0x0063A7B8, 0x0063A7C7, 0x0063B9B0, 0x0063A790),
    MessageSpec("Community_AddBlackListVital", "root_member_48", 0x00F35CB0, 0x0063A719, 0x0063A740, 0x0063A750, "esi", "ebx", 0x0063A7B8, 0x0063A7C7, 0x0063BB90, 0x0063A790),
    MessageSpec("Community_RequestSoulMateMatchVital", "root_member_2c", 0x00F35DE4, 0x0063ACE3, 0x0063AD03, 0x0063AD0D, "eax", "ecx", 0x0063AD68, 0x0063AD77, 0x0063C070, 0x0063AD40),
    MessageSpec("Community_ReplyPenpalLetterVital", "root_member_34", 0x00F35EC0, 0x0063B0B3, 0x0063B0D3, 0x0063B0E6, "eax", "ecx", 0x0063B168, 0x0063B177, 0x0063C3D0, 0x0063B140),
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


@dataclass(frozen=True)
class Section:
    va: int
    raw_size: int
    raw_ptr: int


@dataclass(frozen=True)
class ImportSymbol:
    dll: str
    name: str


class PeImage:
    def __init__(self, data: bytes, *, enforce_identity: bool = True):
        self.data = data
        if enforce_identity:
            if len(data) != IMAGE_SIZE:
                raise ProofError(f"image size mismatch: expected {IMAGE_SIZE}, got {len(data)}")
            if sha256_bytes(data) != IMAGE_SHA256:
                raise ProofError("image SHA-256 mismatch")
        if data[:2] != b"MZ":
            raise ProofError("missing MZ signature")
        pe = struct.unpack_from("<I", data, 0x3C)[0]
        if data[pe : pe + 4] != b"PE\x00\x00":
            raise ProofError("missing PE signature")
        coff = pe + 4
        section_count = struct.unpack_from("<H", data, coff + 2)[0]
        optional_size = struct.unpack_from("<H", data, coff + 16)[0]
        optional = coff + 20
        if struct.unpack_from("<H", data, optional)[0] != 0x10B:
            raise ProofError("expected PE32 image")
        self.image_base = struct.unpack_from("<I", data, optional + 28)[0]
        table = optional + optional_size
        sections: list[Section] = []
        for index in range(section_count):
            off = table + index * 40
            _virtual_size, rva, raw_size, raw_ptr = struct.unpack_from("<IIII", data, off + 8)
            sections.append(Section(self.image_base + rva, raw_size, raw_ptr))
        self.sections = tuple(sections)
        self.imports = self._parse_imports(optional)

    def va_to_off(self, va: int) -> int:
        for section in self.sections:
            if section.va <= va < section.va + section.raw_size:
                return section.raw_ptr + va - section.va
        raise ProofError(f"unmapped VA 0x{va:08X}")

    def u8(self, va: int) -> int:
        return self.data[self.va_to_off(va)]

    def u32(self, va: int) -> int:
        return struct.unpack_from("<I", self.data, self.va_to_off(va))[0]

    def span(self, start_va: int, end_va: int) -> bytes:
        start = self.va_to_off(start_va)
        end = self.va_to_off(end_va - 1) + 1
        if end - start != end_va - start_va:
            raise ProofError("span crosses a non-contiguous PE mapping")
        return self.data[start:end]

    def _ascii(self, off: int) -> str:
        end = self.data.find(b"\x00", off, min(off + 1025, len(self.data)))
        if end < 0:
            raise ProofError("unterminated import string")
        return self.data[off:end].decode("ascii")

    def _parse_imports(self, optional: int) -> dict[int, ImportSymbol]:
        import_rva, import_size = struct.unpack_from("<II", self.data, optional + 104)
        directory_off = self.va_to_off(self.image_base + import_rva)
        result: dict[int, ImportSymbol] = {}
        for descriptor_index in range(import_size // 20):
            off = directory_off + descriptor_index * 20
            original, _timestamp, _forwarder, name_rva, first_thunk = struct.unpack_from("<IIIII", self.data, off)
            if not any((original, name_rva, first_thunk)):
                return result
            dll = self._ascii(self.va_to_off(self.image_base + name_rva))
            lookup = original or first_thunk
            for thunk_index in range(65536):
                value = struct.unpack_from("<I", self.data, self.va_to_off(self.image_base + lookup + thunk_index * 4))[0]
                if value == 0:
                    break
                if value & 0x80000000:
                    continue
                name_off = self.va_to_off(self.image_base + value) + 2
                iat_va = self.image_base + first_thunk + thunk_index * 4
                result[iat_va] = ImportSymbol(dll, self._ascii(name_off))
            else:
                raise ProofError("unterminated import thunk table")
        raise ProofError("unterminated import descriptor table")


REG32 = ("eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi")
PREFIX_BYTES = frozenset((0xF0, 0xF2, 0xF3, 0x2E, 0x36, 0x3E, 0x26, 0x64, 0x65, 0x66, 0x67))
NO_MODRM_0F = frozenset((0x05, 0x06, 0x07, 0x08, 0x09, 0x0B, 0x0E, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x37, 0x77, 0xA0, 0xA1, 0xA2, 0xA8, 0xA9, 0xAA, *range(0xC8, 0xD0)))
IMM8_0F = frozenset((0x0F, 0x70, 0x71, 0x72, 0x73, 0xA4, 0xAC, 0xBA, 0xC2, 0xC4, 0xC5, 0xC6))
MODRM_ONE_BYTE = frozenset(
    (*range(0x00, 0x04), *range(0x08, 0x0C), *range(0x10, 0x14), *range(0x18, 0x1C),
     *range(0x20, 0x24), *range(0x28, 0x2C), *range(0x30, 0x34), *range(0x38, 0x3C),
     0x62, 0x63, 0x69, 0x6B, *range(0x80, 0x90), 0xC0, 0xC1, 0xC4, 0xC5, 0xC6,
     0xC7, *range(0xD0, 0xD4), *range(0xD8, 0xE0), 0xF6, 0xF7, 0xFE, 0xFF)
)


@dataclass(frozen=True)
class Operand:
    kind: str
    reg: str | None = None
    imm: int | None = None
    base: str | None = None
    index: str | None = None
    scale: int = 1
    disp: int = 0
    absolute: int | None = None


@dataclass(frozen=True)
class Instruction:
    va: int
    size: int
    kind: str
    dst: Operand | None = None
    src: Operand | None = None
    target: int | None = None

    @property
    def next_va(self) -> int:
        return self.va + self.size


def _signed(data: bytes, off: int, size: int) -> int:
    return int.from_bytes(data[off : off + size], "little", signed=True)


def _unsigned(data: bytes, off: int, size: int) -> int:
    return int.from_bytes(data[off : off + size], "little", signed=False)


def _parse_modrm(data: bytes, cursor: int, address16: bool) -> tuple[int, int, Operand, Operand]:
    modrm = data[cursor]
    cursor += 1
    mod, reg, rm = modrm >> 6, (modrm >> 3) & 7, modrm & 7
    reg_op = Operand("reg", reg=REG32[reg])
    if mod == 3:
        return cursor, reg, reg_op, Operand("reg", reg=REG32[rm])
    if address16:
        if mod == 0 and rm == 6:
            absolute = _unsigned(data, cursor, 2)
            return cursor + 2, reg, reg_op, Operand("mem", absolute=absolute)
        size = 1 if mod == 1 else 2 if mod == 2 else 0
        disp = _signed(data, cursor, size) if size else 0
        return cursor + size, reg, reg_op, Operand("mem", disp=disp)
    base = index = None
    scale, absolute, disp = 1, None, 0
    if rm == 4:
        sib = data[cursor]
        cursor += 1
        scale = 1 << (sib >> 6)
        index_id, base_id = (sib >> 3) & 7, sib & 7
        if index_id != 4:
            index = REG32[index_id]
        if mod == 0 and base_id == 5:
            absolute = _unsigned(data, cursor, 4)
            cursor += 4
        else:
            base = REG32[base_id]
    elif mod == 0 and rm == 5:
        absolute = _unsigned(data, cursor, 4)
        cursor += 4
    else:
        base = REG32[rm]
    if mod == 1:
        disp = _signed(data, cursor, 1)
        cursor += 1
    elif mod == 2:
        disp = _signed(data, cursor, 4)
        cursor += 4
    return cursor, reg, reg_op, Operand("mem", base=base, index=index, scale=scale, disp=disp, absolute=absolute)


def decode_instruction(image: PeImage, va: int) -> Instruction:
    data = image.data
    off = image.va_to_off(va)
    cursor = off
    operand16 = address16 = False
    while data[cursor] in PREFIX_BYTES:
        operand16 |= data[cursor] == 0x66
        address16 |= data[cursor] == 0x67
        cursor += 1
    op = data[cursor]
    cursor += 1
    op_size, addr_size = (2 if operand16 else 4), (2 if address16 else 4)
    two = None
    modrm_reg = None
    reg_op = rm_op = None
    imm_size = rel_size = 0
    if op == 0x0F:
        two = data[cursor]
        cursor += 1
        if two in (0x38, 0x3A):
            cursor += 1
            has_modrm = True
            if two == 0x3A:
                imm_size = 1
        elif 0x80 <= two <= 0x8F:
            has_modrm = False
            rel_size = op_size
        else:
            has_modrm = two not in NO_MODRM_0F
            if two in IMM8_0F:
                imm_size = 1
    else:
        has_modrm = op in MODRM_ONE_BYTE
        if op in (0x04, 0x0C, 0x14, 0x1C, 0x24, 0x2C, 0x34, 0x3C, 0x6A, 0x80, 0x82, 0x83, 0xC0, 0xC1, 0xC6, 0xCD):
            imm_size = 1
        elif op in (0x05, 0x0D, 0x15, 0x1D, 0x25, 0x2D, 0x35, 0x3D, 0x68, 0x69, 0x81, 0xA9):
            imm_size = op_size
        elif op == 0x6B:
            imm_size = 1
        elif 0x70 <= op <= 0x7F:
            rel_size = 1
        elif 0xA0 <= op <= 0xA3:
            imm_size = addr_size
        elif op == 0xA8:
            imm_size = 1
        elif 0xB0 <= op <= 0xB7:
            imm_size = 1
        elif 0xB8 <= op <= 0xBF:
            imm_size = op_size
        elif op in (0xC2, 0xCA):
            imm_size = 2
        elif op == 0xC7:
            imm_size = op_size
        elif op == 0xC8:
            imm_size = 3
        elif 0xE0 <= op <= 0xE3:
            rel_size = 1
        elif op in (0xE8, 0xE9):
            rel_size = op_size
        elif op == 0xEB:
            rel_size = 1
    if has_modrm:
        cursor, modrm_reg, reg_op, rm_op = _parse_modrm(data, cursor, address16)
        if op == 0xF6 and modrm_reg in (0, 1):
            imm_size = 1
        elif op == 0xF7 and modrm_reg in (0, 1):
            imm_size = op_size
    immediate_off = cursor
    cursor += imm_size + rel_size
    size = cursor - off
    if not 1 <= size <= 15:
        raise ProofError(f"bad instruction length at 0x{va:08X}")
    kind, dst, src, target = "other", None, None, None
    if op == 0xE8:
        kind = "call"
        target = (va + size + _signed(data, immediate_off, rel_size)) & 0xFFFFFFFF
    elif op in (0xE9, 0xEB):
        kind = "jmp"
        target = (va + size + _signed(data, immediate_off, rel_size)) & 0xFFFFFFFF
    elif 0x70 <= op <= 0x7F or (op == 0x0F and two is not None and 0x80 <= two <= 0x8F):
        kind = "jcc"
        target = (va + size + _signed(data, immediate_off, rel_size)) & 0xFFFFFFFF
    elif op in (0xC3, 0xCB, 0xC2, 0xCA):
        kind = "ret"
    elif op == 0xFF and modrm_reg == 2:
        kind, src = "call_indirect", rm_op
    elif op == 0xFF and modrm_reg in (4, 5):
        kind, src = "jmp_indirect", rm_op
    elif 0x50 <= op <= 0x57:
        kind, src = "push", Operand("reg", reg=REG32[op - 0x50])
    elif op in (0x68, 0x6A):
        kind, src = "push", Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif op == 0x8B:
        kind, dst, src = "mov", reg_op, rm_op
    elif op == 0x89:
        kind, dst, src = "mov", rm_op, reg_op
    elif op == 0xC7 and modrm_reg == 0:
        kind, dst, src = "mov", rm_op, Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif 0xB8 <= op <= 0xBF:
        kind = "mov"
        dst = Operand("reg", reg=REG32[op - 0xB8])
        src = Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif op in (0x31, 0x33):
        kind, dst, src = "xor", (rm_op if op == 0x31 else reg_op), (reg_op if op == 0x31 else rm_op)
    elif op in (0x39, 0x3B):
        kind, dst, src = "cmp", (rm_op if op == 0x39 else reg_op), (reg_op if op == 0x39 else rm_op)
    return Instruction(va, size, kind, dst, src, target)


@dataclass(frozen=True)
class CfgResult:
    instructions: Mapping[int, Instruction]
    direct_calls: Counter[int]
    indirect_calls: Counter[int]
    register_calls: Counter[str]
    returns: tuple[int, ...]


def decode_cfg(image: PeImage, start_va: int, end_va: int) -> CfgResult:
    work = deque((start_va,))
    instructions: dict[int, Instruction] = {}
    while work:
        va = work.popleft()
        if va in instructions:
            continue
        if not start_va <= va < end_va:
            raise ProofError(f"CFG edge outside 0x{start_va:08X}..0x{end_va:08X}: 0x{va:08X}")
        ins = decode_instruction(image, va)
        if ins.next_va > end_va:
            raise ProofError(f"instruction crosses span end at 0x{va:08X}")
        instructions[va] = ins
        if ins.kind in ("ret", "jmp_indirect"):
            successors: tuple[int, ...] = ()
        elif ins.kind == "jmp":
            successors = (ins.target,) if ins.target is not None else ()
        elif ins.kind == "jcc":
            successors = (ins.next_va, ins.target) if ins.target is not None else (ins.next_va,)
        else:
            successors = (ins.next_va,) if ins.next_va < end_va else ()
        work.extend(successors)
    direct: Counter[int] = Counter()
    indirect: Counter[int] = Counter()
    register: Counter[str] = Counter()
    returns = []
    for ins in instructions.values():
        if ins.kind == "call" and ins.target is not None:
            direct[ins.target] += 1
        elif ins.kind == "call_indirect" and ins.src is not None:
            if ins.src.absolute is not None:
                indirect[ins.src.absolute] += 1
            elif ins.src.reg is not None:
                register[ins.src.reg] += 1
            else:
                raise ProofError(f"unclassified indirect call at 0x{ins.va:08X}")
        elif ins.kind == "ret":
            returns.append(ins.va)
    if not returns:
        raise ProofError(f"CFG has no return: 0x{start_va:08X}")
    return CfgResult(instructions, direct, indirect, register, tuple(sorted(returns)))


def expect_operand(actual: Operand | None, expected: Operand, label: str) -> None:
    if actual != expected:
        raise ProofError(f"{label}: expected {expected}, got {actual}")


def expect_mov_mem_to_reg(image: PeImage, va: int, dst: str, base: str, disp: int) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    expect_operand(ins.dst, Operand("reg", reg=dst), f"MOV dst 0x{va:08X}")
    expect_operand(ins.src, Operand("mem", base=base, disp=disp), f"MOV src 0x{va:08X}")


def expect_mov_reg_to_mem(image: PeImage, va: int, src: str, base: str, disp: int) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    expect_operand(ins.dst, Operand("mem", base=base, disp=disp), f"MOV dst 0x{va:08X}")
    expect_operand(ins.src, Operand("reg", reg=src), f"MOV src 0x{va:08X}")


def expect_mov_reg_to_reg(image: PeImage, va: int, dst: str, src: str) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    expect_operand(ins.dst, Operand("reg", reg=dst), f"MOV dst 0x{va:08X}")
    expect_operand(ins.src, Operand("reg", reg=src), f"MOV src 0x{va:08X}")


def expect_mov_imm_to_mem(image: PeImage, va: int, value: int, base: str, disp: int) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "mov":
        raise ProofError(f"expected MOV at 0x{va:08X}")
    expect_operand(ins.dst, Operand("mem", base=base, disp=disp), f"MOV dst 0x{va:08X}")
    expect_operand(ins.src, Operand("imm", imm=value), f"MOV src 0x{va:08X}")


def expect_xor_zero(image: PeImage, va: int, reg: str) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "xor":
        raise ProofError(f"expected XOR at 0x{va:08X}")
    expect_operand(ins.dst, Operand("reg", reg=reg), f"XOR dst 0x{va:08X}")
    expect_operand(ins.src, Operand("reg", reg=reg), f"XOR src 0x{va:08X}")


def expect_call(image: PeImage, va: int, target: int) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "call" or ins.target != target:
        raise ProofError(f"call at 0x{va:08X}: expected 0x{target:08X}, got {ins}")


def expect_call_reg(image: PeImage, va: int, reg: str) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "call_indirect":
        raise ProofError(f"expected indirect call at 0x{va:08X}")
    expect_operand(ins.src, Operand("reg", reg=reg), f"call target 0x{va:08X}")


def expect_push_reg(image: PeImage, va: int, reg: str) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "push":
        raise ProofError(f"expected PUSH at 0x{va:08X}")
    expect_operand(ins.src, Operand("reg", reg=reg), f"PUSH operand 0x{va:08X}")


def expect_push_imm(image: PeImage, va: int, value: int) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "push":
        raise ProofError(f"expected PUSH at 0x{va:08X}")
    expect_operand(ins.src, Operand("imm", imm=value), f"PUSH operand 0x{va:08X}")


def expect_cmp_regs(image: PeImage, va: int, left: str, right: str) -> None:
    ins = decode_instruction(image, va)
    if ins.kind != "cmp":
        raise ProofError(f"expected CMP at 0x{va:08X}")
    expect_operand(ins.dst, Operand("reg", reg=left), f"CMP left 0x{va:08X}")
    expect_operand(ins.src, Operand("reg", reg=right), f"CMP right 0x{va:08X}")


def verify_span_pins(image: PeImage) -> dict[str, int]:
    offsets: dict[str, int] = {}
    for pin in SPAN_PINS:
        actual = sha256_bytes(image.span(pin.start_va, pin.end_va))
        if actual != pin.sha256:
            raise ProofError(f"span {pin.name} mismatch: expected {pin.sha256}, got {actual}")
        offsets[pin.name] = image.va_to_off(pin.start_va)
    return offsets


def verify_import(image: PeImage, iat_va: int, dll: str, name: str) -> None:
    symbol = image.imports.get(iat_va)
    if symbol != ImportSymbol(dll, name):
        raise ProofError(f"IAT 0x{iat_va:08X}: expected {dll}!{name}, got {symbol}")


def verify_vtable(image: PeImage) -> None:
    expected = {0x00: 0x00637F40, 0x04: POOL_DESTRUCTOR, 0x14: POOL_SERIALIZER}
    for offset, value in expected.items():
        actual = image.u32(POOL_VTABLE + offset)
        if actual != value:
            raise ProofError(f"pool vtable +0x{offset:02X}: expected 0x{value:08X}, got 0x{actual:08X}")
    refs = []
    needle = struct.pack("<I", POOL_VTABLE)
    cursor = 0
    while True:
        found = image.data.find(needle, cursor)
        if found < 0:
            break
        refs.append(found)
        cursor = found + 1
    expected_refs = [image.va_to_off(0x0063870E), image.va_to_off(0x0063879E)]
    if refs != expected_refs:
        raise ProofError(f"pool vtable reference census mismatch: {refs}")


def verify_nonwire_cfg(image: PeImage) -> dict[str, int]:
    expected = {
        "pool_dtor": (Counter({0x00637830: 1, 0x0088D5B0: 1, 0x0049DA40: 1}), Counter({0x00C3B4A4: 1}), Counter()),
        "pool_base_dtor": (Counter({0x0088D280: 1}), Counter({0x00C3B488: 4}), Counter()),
        "base_object_dtor": (Counter(), Counter({0x00C3B8F8: 1}), Counter()),
        "pool_lock": (Counter(), Counter({0x00C3B16C: 1}), Counter()),
        "pool_unlock": (Counter(), Counter({0x00C3B168: 1}), Counter()),
    }
    counts: dict[str, int] = {}
    for name, (direct, indirect, register) in expected.items():
        pin = SPAN_BY_NAME[name]
        cfg = decode_cfg(image, pin.start_va, pin.end_va)
        if cfg.direct_calls != direct or cfg.indirect_calls != indirect or cfg.register_calls != register:
            raise ProofError(f"{name} call graph mismatch: {cfg}")
        if set(cfg.direct_calls) & WIRE_PRIMITIVES:
            raise ProofError(f"wire primitive reached from {name}")
        counts[name] = len(cfg.instructions)
    verify_import(image, 0x00C3B4A4, "MSVCR90.dll", "free")
    verify_import(image, 0x00C3B488, "MSVCP90.dll", "??1?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ")
    verify_import(image, 0x00C3B8F8, "USER32.dll", "MessageBoxW")
    verify_import(image, 0x00C3B16C, "KERNEL32.dll", "EnterCriticalSection")
    verify_import(image, 0x00C3B168, "KERNEL32.dll", "LeaveCriticalSection")
    return counts


def verify_pool_helper(image: PeImage) -> int:
    pin = SPAN_BY_NAME["pool_helper"]
    cfg = decode_cfg(image, pin.start_va, pin.end_va)
    expected_direct = Counter({
        0x0088D5B0: 1, 0x0049DA40: 1, 0x0088D020: 1, 0x00637BF0: 2,
        0x004160F0: 1, 0x00B37998: 1, 0x0088F350: 1, 0x0088D030: 1,
    })
    if cfg.direct_calls != expected_direct or cfg.indirect_calls or cfg.register_calls:
        raise ProofError(f"pool helper call graph mismatch: {cfg}")
    if set(cfg.direct_calls) & WIRE_PRIMITIVES:
        raise ProofError("pool helper reaches a wire primitive")
    # Both successful construction arms write the same vtable before producing
    # EAX.  The remaining zero arms throw or fault before the sole return.
    expect_mov_imm_to_mem(image, 0x0063870C, POOL_VTABLE, "esi", 0)
    expect_mov_imm_to_mem(image, 0x0063879C, POOL_VTABLE, "esi", 0)
    expect_mov_reg_to_reg(image, 0x00638774, "eax", "esi")
    expect_mov_reg_to_reg(image, 0x006387B7, "eax", "esi")
    if cfg.returns != (0x006387D6,):
        raise ProofError(f"unexpected pool helper return set: {cfg.returns}")
    return len(cfg.instructions)


def verify_pool_serializer(image: PeImage) -> dict[str, int]:
    base = SPAN_BY_NAME["pool_base_serializer"]
    derived = SPAN_BY_NAME["pool_serializer"]
    base_cfg = decode_cfg(image, base.start_va, base.end_va)
    derived_cfg = decode_cfg(image, derived.start_va, derived.end_va)
    if base_cfg.indirect_calls or base_cfg.register_calls:
        raise ProofError("pool base serializer has an unresolved indirect call")
    if not set(base_cfg.direct_calls).issubset(WIRE_PRIMITIVES):
        raise ProofError(f"pool base serializer has unexpected calls: {base_cfg.direct_calls}")
    expected_derived = Counter({0x00637CC0: 1, 0x0089A600: 3, 0x0089A640: 3})
    if derived_cfg.direct_calls != expected_derived or derived_cfg.indirect_calls or derived_cfg.register_calls:
        raise ProofError(f"pool serializer call graph mismatch: {derived_cfg}")
    if not ({0x0089A600, 0x0089A640, 0x0089A810, 0x0089A880} <= set(base_cfg.direct_calls) | set(derived_cfg.direct_calls)):
        raise ProofError("pool serializer does not prove both numeric and string W/R primitives")
    return {"pool_base_serializer": len(base_cfg.instructions), "pool_serializer": len(derived_cfg.instructions)}


def verify_root(image: PeImage, root: RootSpec) -> int:
    pin = SPAN_BY_NAME[root.root_name]
    cfg = decode_cfg(image, pin.start_va, pin.end_va)
    expect_mov_mem_to_reg(image, root.writer_member_load, "ecx", root.object_reg, root.member_offset)
    expect_mov_mem_to_reg(image, root.writer_vtable_load, "edx", "ecx", 0)
    expect_mov_mem_to_reg(image, root.writer_slot_load, "eax", "edx", 0x14)
    expect_push_reg(image, root.writer_mode_push, "ebx")
    expect_push_reg(image, root.writer_stream_push, root.stream_reg)
    expect_call_reg(image, root.writer_call, "eax")
    expect_push_imm(image, root.reader_helper_push_zero, 0)
    expect_push_imm(image, root.reader_helper_push_token, POOL_TYPE_TOKEN)
    helper_load = decode_instruction(image, root.reader_helper_pool_load)
    if helper_load.kind != "mov" or helper_load.dst != Operand("reg", reg="ecx") or helper_load.src != Operand("imm", imm=POOL_GLOBAL):
        raise ProofError(f"pool-this load mismatch at 0x{root.reader_helper_pool_load:08X}: {helper_load}")
    expect_call(image, root.reader_helper_call, POOL_HELPER)
    expect_mov_mem_to_reg(image, root.reader_old_load, "ecx", root.object_reg, root.member_offset)
    expect_mov_reg_to_reg(image, root.reader_new_copy, "ebx", "eax")
    expect_cmp_regs(image, root.reader_compare, "ecx", "ebx")
    expect_call(image, root.reader_decrement, REF_DECREMENT)
    expect_mov_reg_to_mem(image, root.reader_store, "ebx", root.object_reg, root.member_offset)
    expect_mov_reg_to_reg(image, root.reader_increment_this, "ecx", "ebx")
    expect_call(image, root.reader_increment, REF_INCREMENT)
    expect_mov_mem_to_reg(image, root.reader_reload, root.object_reg, root.object_reg, root.member_offset)
    expect_mov_mem_to_reg(image, root.reader_vtable_load, "edx", root.object_reg, 0)
    expect_mov_mem_to_reg(image, root.reader_slot_load, "eax", "edx", 0x14)
    expect_push_imm(image, root.reader_mode_push, 0)
    expect_push_reg(image, root.reader_stream_push, root.stream_reg)
    expect_call_reg(image, root.reader_call, "eax")
    if cfg.register_calls != Counter({"eax": 2}):
        raise ProofError(f"unexpected root register calls in {root.root_name}: {cfg.register_calls}")
    return len(cfg.instructions)


def verify_message_provenance(image: PeImage, spec: MessageSpec) -> None:
    root = ROOTS[spec.root_name]
    expect_xor_zero(image, spec.ctor_zero_seed, spec.zero_reg)
    expect_mov_imm_to_mem(image, spec.ctor_vtable_store, spec.message_vtable, spec.ctor_object_reg, 0)
    expect_mov_reg_to_mem(image, spec.ctor_member_store, spec.zero_reg, spec.ctor_object_reg, root.member_offset)
    expect_mov_mem_to_reg(image, spec.member_dtor_load, "ecx", "esi", root.member_offset)
    expect_call(image, spec.member_dtor_decrement, REF_DECREMENT)
    if image.u32(spec.message_vtable + 4) != spec.wrapper_dtor:
        raise ProofError(f"{spec.message}: wrapper destructor vtable slot mismatch")
    expect_call(image, spec.wrapper_dtor + 3, spec.member_dtor)
    needle = struct.pack("<I", spec.message_vtable)
    refs = []
    cursor = 0
    while True:
        found = image.data.find(needle, cursor)
        if found < 0:
            break
        refs.append(found)
        cursor = found + 1
    expected_ref = image.va_to_off(spec.ctor_vtable_store) + decode_instruction(image, spec.ctor_vtable_store).size - 4
    if refs != [expected_ref]:
        raise ProofError(f"{spec.message}: constructor vtable reference census mismatch")


def verify_registry(a1_path: Path) -> None:
    fields, rows = read_tsv_with_lines(a1_path)
    required = {"name", "vtable_va", "serializer_va", "source"}
    if not required <= set(fields):
        raise ProofError("A1 registry schema mismatch")
    selected = {row["name"]: row for _line, row in rows if row["name"] in MESSAGE_BY_NAME}
    if set(selected) != set(TARGET_NAMES):
        raise ProofError("A1 target census mismatch")
    for message, spec in MESSAGE_BY_NAME.items():
        row = selected[message]
        root = ROOTS[spec.root_name]
        if row["vtable_va"] != f"0x{spec.message_vtable:08X}" or row["serializer_va"] != f"0x{root.root_va:08X}" or row["source"] != "IMAGE":
            raise ProofError(f"A1 mapping mismatch for {message}")


def verify_post_v1_priority_overlay(path: Path) -> None:
    fields, rows = read_tsv_with_lines(path)
    required = {"base_file", "base_row_key", "message", "action", "new_serializer_status", "new_structural_status", "source"}
    if not required <= set(fields):
        raise ProofError("post-V1 priority overlay schema mismatch")
    if any(row["message"] in MESSAGE_BY_NAME for _line, row in rows):
        raise ProofError("post-V1 priority overlay already touches a pool target")
    if any(row["base_file"] != PRIORITY_NAME or row["action"] != "CHANGED" or row["source"] != "IMAGE" for _line, row in rows):
        raise ProofError("post-V1 priority overlay contains an unexpected directive")


def run_mutation_guards(image: PeImage) -> None:
    def mutated(va: int, mutate) -> PeImage:
        data = bytearray(image.data)
        off = image.va_to_off(va)
        mutate(data, off)
        return PeImage(bytes(data), enforce_identity=False)

    controls = []
    controls.append(("vtable_slot", mutated(POOL_VTABLE + 0x14, lambda data, off: struct.pack_into("<I", data, off, POOL_SERIALIZER + 1)), verify_vtable))
    controls.append(("root_member_store", mutated(ROOTS["root_member_48"].reader_store + 2, lambda data, off: data.__setitem__(off, 0x4C)), lambda candidate: verify_root(candidate, ROOTS["root_member_48"])))
    controls.append(("root_helper_target", mutated(ROOTS["root_member_2c"].reader_helper_call + 1, lambda data, off: data.__setitem__(off, (data[off] + 1) & 0xFF)), lambda candidate: verify_root(candidate, ROOTS["root_member_2c"])))
    controls.append(("destructor_call_target", mutated(0x00638373 + 1, lambda data, off: struct.pack_into("<i", data, off, 0x0089A600 - (0x00638373 + 5))), verify_nonwire_cfg))
    for label, candidate, verifier in controls:
        try:
            verifier(candidate)
        except ProofError:
            continue
        raise ProofError(f"negative mutation unexpectedly accepted: {label}")


def expected_tag(root: RootSpec) -> str:
    return f"CALL_UNCLASSIFIED:INDIRECT(DEREF(DEREF(DEREF(OBJ+0x{root.member_offset:X}))+0x14))"


def select_a2_row(rows: Sequence[tuple[int, dict[str, str]]], message: str, direction: str, file_off: int, tag: str) -> tuple[int, dict[str, str]]:
    file_text = f"0x{file_off:08X}"
    matches = [(line, row) for line, row in rows if row["message"] == message and row["direction(W/R)"] == direction and row["file_off_claim"] == file_text and row["tag"] == tag]
    if len(matches) != 1:
        raise ProofError(f"A2 selection {message}/{direction}/{file_text}/{tag}: {len(matches)} rows")
    return matches[0]


def root_file_off(image: PeImage, va: int) -> int:
    return image.va_to_off(va)


def build_a2_delta(image: PeImage, fields: Sequence[str], rows: Sequence[tuple[int, dict[str, str]]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for spec in MESSAGES:
        root = ROOTS[spec.root_name]
        pin = SPAN_BY_NAME[root.root_name]
        span_values = (f"0x{pin.start_va:08X}", f"0x{pin.end_va:08X}", pin.sha256)
        indirect_tag = expected_tag(root)
        sites = (
            (root.writer_call, "W", "CHANGED", "RESOLVE_FIXED_VTABLE_SUBCALL", "WRITER_MEMBER_FIXED_POOL_SUBCALL"),
            (root.writer_call, "R", "REMOVE_NONWIRE_ROW", "DIRECTION_CROSS_PRODUCT_ARTIFACT", "WRITER_SITE_NOT_READER"),
            (root.reader_call, "R", "CHANGED", "RESOLVE_FIXED_VTABLE_SUBCALL", "READER_HELPER_RESULT_FIXED_POOL_SUBCALL"),
            (root.reader_call, "W", "REMOVE_NONWIRE_ROW", "DIRECTION_CROSS_PRODUCT_ARTIFACT", "READER_SITE_NOT_WRITER"),
        )
        for call_va, direction, action, change_type, resolution in sites:
            line, row = select_a2_row(rows, spec.message, direction, root_file_off(image, call_va), indirect_tag)
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
                "evidence_ticket": "POOL_638690",
                "evidence_span_start": span_values[0],
                "evidence_span_end": span_values[1],
                "evidence_span_sha256": span_values[2],
                "evidence_file_off": f"0x{root_file_off(image, call_va):08X}",
                "source": "IMAGE",
            })
        lifecycle = (
            (root.reader_helper_call, "CALL_UNCLASSIFIED:0x00638690", "OBJECT_POOL_ACQUIRE_NO_STREAM_ALIAS"),
            (root.reader_decrement, "DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04", "FIXED_POOL_DESTRUCTOR_FULL_CFG_NONWIRE"),
            (root.reader_increment, "ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C", "FIXED_NEW_OBJECT_REFCOUNT_INCREMENT_NONWIRE"),
        )
        for call_va, tag, resolution in lifecycle:
            for direction in ("R", "W"):
                line, row = select_a2_row(rows, spec.message, direction, root_file_off(image, call_va), tag)
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
                    "evidence_ticket": "POOL_638690",
                    "evidence_span_start": span_values[0],
                    "evidence_span_end": span_values[1],
                    "evidence_span_sha256": span_values[2],
                    "evidence_file_off": f"0x{root_file_off(image, call_va):08X}",
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
        row_key = canonical_row_key(fields, row)
        output.append({
            "delta_key": make_delta_key((PRIORITY_NAME, str(line), row_key, "CHANGED")),
            "action": "CHANGED", "base_file": PRIORITY_NAME, "base_line": str(line), "base_row_key": row_key,
            "message": message, "priority": "1", "old_serializer_status": "OPEN", "new_serializer_status": "CLOSED",
            "old_structural_status": "OPEN", "new_structural_status": "CLOSED", "old_blocker": row["blocker"], "new_blocker": "N/A",
            "evidence_ticket": "POOL_638690",
            "closure_scope": "FIXED_POOL_VTABLE_SUBCALL_RESOLVED;LIFECYCLE_ROWS_REMOVED;NESTED_SERIALIZER_REFERENCED_NOT_FLATTENED",
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
        keys = [row["delta_key"] for row in rows]
        base_keys = [row["base_row_key"] for row in rows]
        if len(keys) != len(set(keys)) or len(base_keys) != len(set(base_keys)):
            raise ProofError("duplicate delta/base key")
    if set(row["message"] for row in priority_delta) != set(TARGET_NAMES):
        raise ProofError("priority target set mismatch")


def validate_no_existing_overlap(external_dir: Path, a2_delta: Sequence[Mapping[str, str]], priority_delta: Sequence[Mapping[str, str]]) -> None:
    ours = {A2_DELTA_NAME, PRIORITY_DELTA_NAME}
    wanted = {
        (row["base_file"], row["base_row_key"])
        for row in (*a2_delta, *priority_delta)
    }
    for path in sorted(external_dir.glob("*DELTA.tsv")):
        if path.name in ours:
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if reader.fieldnames is None or not {"base_file", "base_row_key"} <= set(reader.fieldnames):
                continue
            for row in reader:
                key = (row["base_file"], row["base_row_key"])
                if key in wanted:
                    raise ProofError(f"existing overlay overlap: {path.name} {key}")


def validate_post_overlay_closure(a2_rows: Sequence[tuple[int, dict[str, str]]], delta: Sequence[Mapping[str, str]]) -> None:
    directives = {row["base_row_key"]: row for row in delta}
    for _line, row in a2_rows:
        if row["message"] not in MESSAGE_BY_NAME:
            continue
        key = canonical_row_key(list(row.keys()), row)
        directive = directives.get(key)
        if directive is not None and directive["action"] == "REMOVE_NONWIRE_ROW":
            continue
        tag = directive["new_tag"] if directive is not None and directive["action"] == "CHANGED" else row["tag"]
        field = directive["new_field_offset"] if directive is not None and directive["action"] == "CHANGED" else row["field_offset"]
        if "UNKNOWN(" in tag or "UNKNOWN(" in field or tag.startswith("CALL_UNCLASSIFIED:") or tag.startswith("DYNAMIC_") or tag.startswith("ATOMIC_"):
            raise ProofError(f"residual unresolved target row: {row['message']} {tag} {field}")


def validate_residual_mutation_guard(a2_fields: Sequence[str], a2_rows: Sequence[tuple[int, dict[str, str]]], delta: Sequence[Mapping[str, str]]) -> None:
    synthetic = {name: "N/A" for name in a2_fields}
    synthetic.update({
        "message": TARGET_NAMES[0], "direction(W/R)": "R", "order": "999",
        "tag": "CALL_UNCLASSIFIED:0x00000001", "field_offset": "UNKNOWN(synthetic_guard)",
        "len": "N/A", "gate_condition": "ALWAYS", "span_start": "0x00000000",
        "span_end": "0x00000001", "span_sha256": "0" * 64, "file_off_claim": "0x00000000", "source": "IMAGE",
    })
    try:
        validate_post_overlay_closure((*a2_rows, (10**9, synthetic)), delta)
    except ProofError:
        return
    raise ProofError("synthetic unresolved target row unexpectedly accepted")


def report_text(offsets: Mapping[str, int], cfg_counts: Mapping[str, int]) -> str:
    root_rows = []
    for spec in MESSAGES:
        root = ROOTS[spec.root_name]
        pin = SPAN_BY_NAME[spec.root_name]
        root_rows.append(
            f"| `{spec.message}` | `+0x{root.member_offset:X}` | `0x{root.root_va:08X}..0x{pin.end_va:08X}` | "
            f"`{pin.sha256}` | `0x{root.writer_call:08X}` | `0x{root.reader_call:08X}` |"
        )
    cfg_rows = []
    for name in ("pool_dtor", "pool_base_dtor", "base_object_dtor", "pool_lock", "pool_unlock"):
        pin = SPAN_BY_NAME[name]
        cfg_rows.append(f"| `{name}` | {cfg_counts[name]} | `0x{pin.start_va:08X}..0x{pin.end_va:08X}` | `{pin.sha256}` |")
    return "\n".join((
        "# PF pool 0x00638690 closure overlay",
        "",
        "[MEASURED] IMAGE-only additive result. V1 remains immutable.",
        "",
        "## Result",
        "",
        "The four requested Priority-1 messages are structurally CLOSED in this isolated overlay:",
        "",
        *[f"- `{name}`" for name in TARGET_NAMES],
        "",
        "Isolated priority effect: **+4 CLOSED**. This report intentionally does not state a combined project headline because other independent overlays may be applied before or after it.",
        "",
        "The A2 overlay contains 40 exact V1 directives: 8 `CHANGED` indirect rows become `SUBCALL:0x00637FC0`; 32 rows are removed (8 cross-direction artifacts and 24 pool/refcount lifecycle artifacts). The priority overlay contains 4 exact V1 `OPEN -> CLOSED` directives. Unchanged rows copied: 0. Duplicate delta keys: 0. Existing-overlay base-key overlap: 0. The current post-V1 priority overlay is pinned at sha256 `69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51` and touches none of these four base rows.",
        "",
        "## Serializer roots and call sites",
        "",
        "| message | member | exact root span | span sha256 | W subcall | R subcall |",
        "|---|---:|---|---|---:|---:|",
        *root_rows,
        "",
        "Each writer site loads the member, then its vtable and slot `+0x14`, and passes the root stream plus the writer mode. Each reader site calls `0x00638690`, stores that exact result back to the same member, then reloads the member and calls the same vtable slot with reader mode zero. The V1 cross-product row for the opposite direction at each site is therefore removed, not re-labelled.",
        "",
        "## Fixed pool identity",
        "",
        f"- Helper span: `0x00638690..0x006387D9`, file offset `0x{offsets['pool_helper']:08X}`, sha256 `{SPAN_BY_NAME['pool_helper'].sha256}`.",
        "- Its two successful construction arms write vtable `0x00F3568C` at `0x0063870C` and `0x0063879C`. The only function return is `0x006387D6`; zero-allocation paths throw or fault before it.",
        f"- Vtable prefix: file offset `0x{offsets['pool_vtable_prefix']:08X}`, sha256 `{SPAN_BY_NAME['pool_vtable_prefix'].sha256}`; slot `+0x04 = 0x00638370`, slot `+0x14 = 0x00637FC0`.",
        f"- Slot `+0x14` span: `0x00637FC0..0x00638035`, sha256 `{SPAN_BY_NAME['pool_serializer'].sha256}`. It calls base serializer `0x00637CC0` and proves both write/read primitive families; the base span is sha256 `{SPAN_BY_NAME['pool_base_serializer'].sha256}`.",
        "",
        "The root call passes only pool-this `0x0102FB94` and constants `0x00F0A90C`/zero. The helper has no wire-primitive call and does not receive the root stream register. Its direct calls are lock/unlock, allocation, construction, accounting, and a non-returning exception path. Therefore the helper row is lifecycle, not a wire field.",
        "",
        "## Member provenance and atomic identity",
        "",
        "The four concrete constructors write their message vtables and zero the exact members `+0x48`, `+0x48`, `+0x2C`, and `+0x34`. Each matching message destructor loads that same member and calls `0x0088D060`. In the reader root, EAX from `0x00638690` is copied to EBX, compared with the old member, the old object is decremented if different, EBX is stored to the member, and that same EBX is incremented. The subsequent subcall reloads the same member. This proves old/new identity rather than inferring it from proximity or naming.",
        "",
        "## Destructor full reachable CFG",
        "",
        "| function | reachable instructions | exact span | sha256 |",
        "|---|---:|---|---|",
        *cfg_rows,
        "",
        "The complete reachable chain is fixed to the pool destructor, four `basic_string<wchar_t>` destructors, base-object cleanup (its sole diagnostic leaf is `USER32!MessageBoxW`), `EnterCriticalSection`, `LeaveCriticalSection`, and `MSVCR90!free`. It has no stream formal, no stream alias from the caller, no unresolved register call, and no wire primitive. Thus the dynamic decrement row resolves to a nonwire destructor, while the increment helper is the already pinned `InterlockedIncrement` at `0x0088D050`.",
        "",
        "## Boundaries",
        "",
        "- `source=IMAGE` on every row; no DUMP, CAPTURE, or DATA fact is mixed into this overlay.",
        "- Closure means the indirect serializer target and lifecycle effects are statically resolved. The nested serializer is referenced as a subcall; its child fields are not duplicated or flattened into parent offsets here.",
        "- This result does not claim a runtime RTTI class name or capture validation.",
        "- No raw client, dump, or capture bytes are emitted.",
        "",
        "## Reproduction",
        "",
        "Run `py -3 pf_build_pool_638690_closure.py --check`. It re-hashes the image and V1 inputs, verifies all pinned spans/imports/CFGs and registry roots, checks existing-overlay overlap, applies a residual-UNKNOWN guard, and runs independent mutations of the vtable slot, member store, helper target, and destructor call target.",
        "",
    ))


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_image = script_dir.parent.parent / "GameClient" / "GameClient.local.bin"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, default=default_image)
    parser.add_argument("--external-dir", type=Path, default=script_dir)
    parser.add_argument("--check", action="store_true", help="verify that existing outputs are byte-identical")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    external_dir = args.external_dir.resolve()
    image_path = args.image.resolve()
    a1_path, a2_path, priority_path = (external_dir / A1_NAME, external_dir / A2_NAME, external_dir / PRIORITY_NAME)
    post_v1_priority_path = external_dir / POST_V1_PRIORITY_NAME
    fixed_inputs = {
        image_path: IMAGE_SHA256,
        a1_path: A1_SHA256,
        a2_path: A2_SHA256,
        priority_path: PRIORITY_SHA256,
        post_v1_priority_path: POST_V1_PRIORITY_SHA256,
    }
    for path, expected in fixed_inputs.items():
        require_hash(path, expected, path.name)
    dynamic_inputs = {
        path: sha256_path(path)
        for path in external_dir.glob("*DELTA.tsv")
        if path.name not in {A2_DELTA_NAME, PRIORITY_DELTA_NAME, POST_V1_PRIORITY_NAME}
    }
    image = PeImage(image_path.read_bytes())
    offsets = verify_span_pins(image)
    verify_vtable(image)
    verify_import(image, 0x00C3B1B0, "KERNEL32.dll", "InterlockedIncrement")
    verify_import(image, 0x00C3B1B4, "KERNEL32.dll", "InterlockedDecrement")
    cfg_counts = verify_nonwire_cfg(image)
    cfg_counts["pool_helper"] = verify_pool_helper(image)
    cfg_counts.update(verify_pool_serializer(image))
    for root in ROOTS.values():
        cfg_counts[root.root_name] = verify_root(image, root)
    for spec in MESSAGES:
        verify_message_provenance(image, spec)
    verify_registry(a1_path)
    verify_post_v1_priority_overlay(post_v1_priority_path)
    run_mutation_guards(image)

    a2_fields, a2_rows = read_tsv_with_lines(a2_path)
    priority_fields, priority_rows = read_tsv_with_lines(priority_path)
    a2_delta = build_a2_delta(image, a2_fields, a2_rows)
    priority_delta = build_priority_delta(priority_fields, priority_rows)
    validate_delta(a2_delta, priority_delta)
    validate_no_existing_overlap(external_dir, a2_delta, priority_delta)
    validate_post_overlay_closure(a2_rows, a2_delta)
    validate_residual_mutation_guard(a2_fields, a2_rows, a2_delta)

    outputs = {
        external_dir / A2_DELTA_NAME: write_tsv_text(A2_DELTA_COLUMNS, a2_delta),
        external_dir / PRIORITY_DELTA_NAME: write_tsv_text(PRIORITY_DELTA_COLUMNS, priority_delta),
        external_dir / REPORT_NAME: report_text(offsets, cfg_counts),
    }
    for path, expected in fixed_inputs.items():
        require_hash(path, expected, f"prepublish {path.name}")
    for path, expected in dynamic_inputs.items():
        require_hash(path, expected, f"prepublish {path.name}")
    if args.check:
        for path, text in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                raise ProofError(f"check mismatch: {path}")
        print("check ok: 40 A2 directives, 4 priority directives, isolated +4 CLOSED")
        return 0
    for path, text in outputs.items():
        atomic_write_text(path, text)
    print("wrote:")
    for path in outputs:
        print(f"  {path.name} {sha256_path(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
