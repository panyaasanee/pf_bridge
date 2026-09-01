#!/usr/bin/env python3
"""Build the additive IMAGE-only 0x00661FA0 pool/refcount closure overlay.

The frozen V1 tables are inputs, never outputs.  This generator verifies the
exact IMAGE spans, PE imports, control-flow edges, caller reaching definitions,
fixed pooled-object construction/destruction chain, and base-row identities
before emitting removal/change directives.  It uses only the Python standard
library and never emits image bytes.
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
from io import StringIO
from pathlib import Path
from typing import Iterable, Mapping, Sequence


IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
A2_SHA256 = "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
PRIORITY_SHA256 = "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"
POST_V1_A2_SHA256 = "96e5a476baad2b0ceda79b2ef47bc5a85189551f76003139e1be4cd034f5afc2"
POST_V1_PRIORITY_SHA256 = "69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51"

A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
PRIORITY_NAME = "PF_PROTOCOL_PRIORITY.tsv"
POST_V1_A2_NAME = "PF_A2_POST_V1_STATIC_DELTA.tsv"
POST_V1_PRIORITY_NAME = "PF_POST_V1_PRIORITY_DELTA.tsv"
A2_DELTA_NAME = "PF_A2_POOL_661FA0_DELTA.tsv"
PRIORITY_DELTA_NAME = "PF_PRIORITY_POOL_661FA0_DELTA.tsv"
REPORT_NAME = "PF_POOL_661FA0_CLOSURE.md"

TARGETS = (
    "TradeCmdVital",
    "GCGS_GuildStorageCmdVital",
    "StorageCmdVital",
    "ItemMallBagItemTransfer",
)

EVIDENCE_ID = "STATIC-POOL-661FA0"


@dataclass(frozen=True)
class SpanPin:
    role: str
    start_va: int
    end_va: int
    file_off: int
    sha256: str


SPAN_PINS = (
    SpanPin("pool_allocator", 0x00661FA0, 0x006620AB, 0x002613A0, "8e4b55f86fa64a27fe99ad80d60f308fe7889d4c69e767f3fbc94da5e2db91a8"),
    SpanPin("shared_serializer", 0x00699910, 0x006999EE, 0x00298D10, "6f6d5832976137fa98b15ba81b512f64e30d2570f4d93f5311af9e25071540e8"),
    SpanPin("mall_serializer", 0x006B9EA0, 0x006B9F80, 0x002B92A0, "22698df219264aa44bacdf383f50c4f91fa29067b0383f596df62bfecdc407e5"),
    SpanPin("fixed_object_constructor", 0x005DF300, 0x005DF327, 0x001DE700, "df1047a07df1e04411943d6d6fdf7d5aac8fabb5d3fdd8efdddbaa6d7ecdbbff"),
    SpanPin("fixed_object_deleting_destructor", 0x005DFCA0, 0x005DFCFE, 0x001DF0A0, "63a40c4a1594c32fd9e5f6a8787ed4a7750cf790e482f06c6ee64d00e18854f7"),
    SpanPin("refcount_increment", 0x0088D050, 0x0088D05B, 0x0048C450, "6da78a1acc15d9fd5f7b2d620253debf8d8465136165dfb1eae35914b2442845"),
    SpanPin("refcount_decrement", 0x0088D060, 0x0088D082, 0x0048C460, "d3b546ac50ded491a6c5a196138b9691f23d8499298e728925f1afb1f0e7734c"),
    SpanPin("enter_critical_section_wrapper", 0x0088D5B0, 0x0088D5BA, 0x0048C9B0, "281bb0603facf9b7c61c87c0241b74e59ff6488057f979782e4d08ea4e4e9ee8"),
    SpanPin("leave_critical_section_wrapper", 0x0049DA40, 0x0049DA4A, 0x0009CE40, "91f8bd361459e6514e2c53ca4bac3bd9d76baddaf75ee1b1562afecee8d96366"),
    SpanPin("malloc_thunk", 0x0088D020, 0x0088D026, 0x0048C420, "162556d419434c255a68f63f36f37bea903e3adfe89623720318e28708160b58"),
    SpanPin("recycled_pointer_identity", 0x0088D030, 0x0088D035, 0x0048C430, "99712f5745d56904d51e658eeac81bb39a7a2acb4c8834e9af91b4ef58557a0d"),
    SpanPin("allocation_counter", 0x0088F350, 0x0088F361, 0x0048E750, "0a3399caca8eb23244cf6421ea6ab095933e6187b927739d140fefd8892aeebd"),
    SpanPin("refcount_base_destructor", 0x0088D280, 0x0088D2F0, 0x0048C680, "d914c8eaef424f2988c6b76b6954acbb9247bd4309a2c8f0e09439cc64f1104a"),
    SpanPin("allocation_failure_exception_constructor", 0x004160F0, 0x0041617F, 0x000154F0, "10d12b493a454e4e6cff25218d50705154cfc2e495cbfcab83c05bc6259bba21"),
    SpanPin("cxx_throw_thunk", 0x00B37998, 0x00B3799E, 0x00736D98, "16bf8ff4ff7050398899b806680db04f97c42d1b2f69ba2f4eed563eae73ba16"),
    SpanPin("fixed_pool_sized_cleanup", 0x004FB6A0, 0x004FB6F2, 0x000FAAA0, "42f841be59b2b3527c150aa5e47056f8e3c0fd113a5b08546d1979b359595325"),
    SpanPin("TradeCmdVital_constructor", 0x006645C0, 0x0066463B, 0x002639C0, "7ab8e6d92d9ed20c72c5487aa0d607d1303972e9a7b6b23311e2fc543e1f9cd2"),
    SpanPin("GCGS_GuildStorageCmdVital_constructor", 0x006725F0, 0x0067266B, 0x002719F0, "e9d89c09b1a676938c4dc23f7932425536d1dab1711c3fd72625379280d33980"),
    SpanPin("StorageCmdVital_constructor", 0x006990A0, 0x0069911B, 0x002984A0, "fe18d9ce2eb4d707ec3923e0f96a9dbd0e165a062c16a2f37b95e7ab140c8c9e"),
    SpanPin("ItemMallBagItemTransfer_constructor", 0x006B8950, 0x006B89CC, 0x002B7D50, "dff2e1747a3d586440dbc92100c3bdb564da2db6ec16129896b758f56c81c30b"),
    SpanPin("fixed_vtable_head", 0x00F2FE14, 0x00F2FE1C, 0x00B2E214, "71e27f1ad8c483fcbf8af40c3246d8a1338ebf3cb24f44ccaaed2a91308d2a53"),
)


@dataclass(frozen=True)
class BranchPin:
    function: str
    site: int
    opcode: int
    taken: int
    fallthrough: int | None


BRANCH_PINS = (
    BranchPin("pool_allocator", 0x00661FD6, 0x74, 0x00661FDD, 0x00661FD8),
    BranchPin("pool_allocator", 0x00661FE6, 0x0F85, 0x00662071, 0x00661FEC),
    BranchPin("pool_allocator", 0x00662000, 0x74, 0x0066200D, 0x00662002),
    BranchPin("pool_allocator", 0x0066200B, 0xEB, 0x0066200F, None),
    BranchPin("pool_allocator", 0x00662019, 0x75, 0x00662042, 0x0066201B),
    BranchPin("pool_allocator", 0x0066207E, 0x74, 0x00662089, 0x00662080),
    BranchPin("pool_allocator", 0x00662087, 0xEB, 0x0066208B, None),
    BranchPin("shared_serializer", 0x0069991D, 0x74, 0x00699972, 0x0069991F),
    BranchPin("shared_serializer", 0x0069995F, 0x0F84, 0x006999EA, 0x00699965),
    BranchPin("shared_serializer", 0x006999AC, 0x74, 0x006999EA, 0x006999AE),
    BranchPin("shared_serializer", 0x006999C6, 0x74, 0x006999DF, 0x006999C8),
    BranchPin("shared_serializer", 0x006999CA, 0x74, 0x006999D1, 0x006999CC),
    BranchPin("shared_serializer", 0x006999D6, 0x74, 0x006999DF, 0x006999D8),
    BranchPin("mall_serializer", 0x006B9EAD, 0x74, 0x006B9F02, 0x006B9EAF),
    BranchPin("mall_serializer", 0x006B9EEF, 0x0F84, 0x006B9F7A, 0x006B9EF5),
    BranchPin("mall_serializer", 0x006B9F3C, 0x74, 0x006B9F7A, 0x006B9F3E),
    BranchPin("mall_serializer", 0x006B9F56, 0x74, 0x006B9F6F, 0x006B9F58),
    BranchPin("mall_serializer", 0x006B9F5A, 0x74, 0x006B9F61, 0x006B9F5C),
    BranchPin("mall_serializer", 0x006B9F66, 0x74, 0x006B9F6F, 0x006B9F68),
)


DIRECT_CALL_PINS = {
    # Complete direct-call set in the pool helper.
    0x00661FCD: 0x0088D5B0,
    0x00661FDF: 0x0049DA40,
    0x00661FEE: 0x0088D020,
    0x00662004: 0x005DF300,
    0x0066202E: 0x004160F0,
    0x0066203D: 0x00B37998,
    0x0066204C: 0x0088F350,
    0x00662074: 0x0088D030,
    0x00662082: 0x005DF300,
    # Complete direct-call set in the two serializer bodies.
    0x0069992B: 0x0089A600,
    0x0069993A: 0x0089A600,
    0x00699955: 0x0089A600,
    0x00699967: 0x0074CF90,
    0x0069997E: 0x0089A640,
    0x0069998D: 0x0089A640,
    0x006999A2: 0x0089A640,
    0x006999BA: 0x00661FA0,
    0x006999CC: 0x0088D060,
    0x006999DA: 0x0088D050,
    0x006999E5: 0x0074CF90,
    0x006B9EBB: 0x0089A600,
    0x006B9ECA: 0x0089A600,
    0x006B9EE5: 0x0089A600,
    0x006B9EF7: 0x0074CF90,
    0x006B9F0E: 0x0089A640,
    0x006B9F1D: 0x0089A640,
    0x006B9F32: 0x0089A640,
    0x006B9F4A: 0x00661FA0,
    0x006B9F5C: 0x0088D060,
    0x006B9F6A: 0x0088D050,
    0x006B9F75: 0x0074CF90,
    # Fixed constructor/destructor support chain.
    0x005DFCA9: 0x0088D280,
    0x005DFCC7: 0x0088D5B0,
    0x005DFCE5: 0x0049DA40,
}


@dataclass(frozen=True)
class ImportPin:
    iat_va: int
    iat_file_off: int
    descriptor_file_off: int
    lookup_file_off: int
    dll_file_off: int
    symbol_file_off: int
    dll: str
    symbol: str


IMPORT_PINS = (
    ImportPin(0x00C3B168, 0x00839568, 0x00C11214, 0x00C1155C, 0x00C124EA, 0x00C122CE, "KERNEL32.dll", "LeaveCriticalSection"),
    ImportPin(0x00C3B16C, 0x0083956C, 0x00C11214, 0x00C11560, 0x00C124EA, 0x00C122B6, "KERNEL32.dll", "EnterCriticalSection"),
    ImportPin(0x00C3B19C, 0x0083959C, 0x00C11214, 0x00C11590, 0x00C124EA, 0x00C121A4, "KERNEL32.dll", "InterlockedExchangeAdd"),
    ImportPin(0x00C3B1B0, 0x008395B0, 0x00C11214, 0x00C115A4, 0x00C124EA, 0x00C11FC4, "KERNEL32.dll", "InterlockedIncrement"),
    ImportPin(0x00C3B1B4, 0x008395B4, 0x00C11214, 0x00C115A8, 0x00C124EA, 0x00C11FDC, "KERNEL32.dll", "InterlockedDecrement"),
    ImportPin(0x00C3B8F8, 0x00839CF8, 0x00C11228, 0x00C11CEC, 0x00C126EC, 0x00C124FA, "USER32.dll", "MessageBoxW"),
    ImportPin(0x00C3B43C, 0x0083983C, 0x00C1128C, 0x00C11830, 0x00C15908, 0x00C12F66, "MSVCP90.dll", "??4?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAEAAV01@PBD@Z"),
    ImportPin(0x00C3B478, 0x00839878, 0x00C1128C, 0x00C1186C, 0x00C15908, 0x00C12A86, "MSVCP90.dll", "??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ"),
    ImportPin(0x00C3B480, 0x00839880, 0x00C1128C, 0x00C11874, 0x00C15908, 0x00C129E4, "MSVCP90.dll", "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@PBD@Z"),
    ImportPin(0x00C3B4A4, 0x008398A4, 0x00C112DC, 0x00C11898, 0x00C1647C, 0x00C15C08, "MSVCR90.dll", "free"),
    ImportPin(0x00C3B4C4, 0x008398C4, 0x00C112DC, 0x00C118B8, 0x00C1647C, 0x00C15C7E, "MSVCR90.dll", "_CxxThrowException"),
    ImportPin(0x00C3B87C, 0x00839C7C, 0x00C112DC, 0x00C11C70, 0x00C1647C, 0x00C15BFE, "MSVCR90.dll", "malloc"),
)


# Exact IMAGE code references to the fixed 0x20-byte pool globals.  Data and
# relocation-table occurrences are deliberately excluded from this code census.
POOL_CODE_REFERENCE_FILE_OFFSETS = {
    0x01030238: (
        0x000FAAC8, 0x000FAAD7, 0x001DF0CD, 0x001DF0E1,
        0x00261B2C, 0x00266236, 0x00266304, 0x002731F1,
        0x002977FC, 0x00298DB6, 0x002B9346,
        0x007D3B31, 0x00824D21, 0x00824D43,
    ),
    0x0103023C: (
        0x000FAAB7, 0x000FAADC, 0x001DF0BC, 0x001DF0DB, 0x00824D4E,
    ),
    0x0103024C: (0x000FAAD1, 0x001DF0D6),
}


A2_DELTA_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line",
    "base_row_key", "message", "direction(W/R)", "old_order", "old_tag",
    "old_field_offset", "old_len", "new_wire_order", "new_tag",
    "new_field_offset", "new_len", "new_gate_condition", "resolution",
    "evidence_ticket", "evidence_span_start", "evidence_span_end",
    "evidence_span_sha256", "evidence_file_off", "source",
)

PRIORITY_DELTA_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "message", "priority", "old_serializer_status", "new_serializer_status",
    "old_structural_status", "new_structural_status", "old_blocker",
    "new_blocker", "evidence_ticket", "closure_scope", "source",
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
    return sha256_bytes("\x1f".join(parts).encode("utf-8"))


def read_tsv_with_lines(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise RuntimeError(f"missing TSV header: {path}")
        fields = list(reader.fieldnames)
        rows = [(line, dict(row)) for line, row in enumerate(reader, start=2)]
    return fields, rows


def write_tsv_text(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
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
    def __init__(self, data: bytes | bytearray) -> None:
        self.data = bytes(data)
        if len(self.data) < 0x100 or self.data[:2] != b"MZ":
            raise RuntimeError("not an MZ image")
        self.pe_offset = struct.unpack_from("<I", self.data, 0x3C)[0]
        if self.data[self.pe_offset : self.pe_offset + 4] != b"PE\0\0":
            raise RuntimeError("missing PE signature")
        coff = self.pe_offset + 4
        section_count = struct.unpack_from("<H", self.data, coff + 2)[0]
        optional_size = struct.unpack_from("<H", self.data, coff + 16)[0]
        self.optional = coff + 20
        if struct.unpack_from("<H", self.data, self.optional)[0] != 0x10B:
            raise RuntimeError("expected PE32 optional header")
        self.image_base = struct.unpack_from("<I", self.data, self.optional + 28)[0]
        self.size_of_headers = struct.unpack_from("<I", self.data, self.optional + 60)[0]
        section_table = self.optional + optional_size
        self.sections: list[tuple[str, int, int, int, int]] = []
        for index in range(section_count):
            off = section_table + index * 40
            name = self.data[off : off + 8].split(b"\0", 1)[0].decode("ascii", "replace")
            virtual_size, virtual_address, raw_size, raw_pointer = struct.unpack_from(
                "<IIII", self.data, off + 8
            )
            self.sections.append((name, virtual_address, virtual_size, raw_pointer, raw_size))

    def rva_to_off(self, rva: int) -> int:
        if 0 <= rva < self.size_of_headers:
            return rva
        for name, section_rva, virtual_size, raw_pointer, raw_size in self.sections:
            delta = rva - section_rva
            if delta < 0 or delta >= raw_size or delta >= max(virtual_size, raw_size):
                continue
            off = raw_pointer + delta
            if off >= len(self.data):
                raise RuntimeError(f"RVA maps beyond file in section {name}")
            return off
        raise RuntimeError(f"cannot map RVA 0x{rva:08X}")

    def va_to_off(self, va: int) -> int:
        return self.rva_to_off(va - self.image_base)

    def va_slice(self, start_va: int, end_va: int) -> tuple[int, bytes]:
        if end_va <= start_va:
            raise RuntimeError("invalid VA span")
        off = self.va_to_off(start_va)
        end = off + end_va - start_va
        if end > len(self.data):
            raise RuntimeError("VA span exceeds file")
        return off, self.data[off:end]

    def u8(self, va: int) -> int:
        return self.data[self.va_to_off(va)]

    def u32(self, va: int) -> int:
        return struct.unpack_from("<I", self.data, self.va_to_off(va))[0]

    def i8(self, va: int) -> int:
        return struct.unpack_from("<b", self.data, self.va_to_off(va))[0]

    def i32(self, va: int) -> int:
        return struct.unpack_from("<i", self.data, self.va_to_off(va))[0]

    def cstr_at_rva(self, rva: int) -> tuple[int, str]:
        off = self.rva_to_off(rva)
        end = self.data.find(b"\0", off)
        if end < 0:
            raise RuntimeError("unterminated PE string")
        return off, self.data[off:end].decode("ascii", "strict")


def verify_span_pins(pe: PeImage) -> None:
    if pe.image_base != 0x00400000:
        raise RuntimeError(f"unexpected ImageBase 0x{pe.image_base:08X}")
    for pin in SPAN_PINS:
        off, body = pe.va_slice(pin.start_va, pin.end_va)
        if off != pin.file_off:
            raise RuntimeError(f"{pin.role} file offset drift: 0x{off:08X}")
        actual = sha256_bytes(body)
        if actual != pin.sha256:
            raise RuntimeError(
                f"{pin.role} span SHA mismatch: expected {pin.sha256}, got {actual}"
            )


def expect_rel8(pe: PeImage, site: int, opcode: int, target: int) -> None:
    if pe.u8(site) != opcode:
        raise RuntimeError(f"opcode drift at 0x{site:08X}")
    actual = site + 2 + pe.i8(site + 1)
    if actual != target:
        raise RuntimeError(f"branch target drift at 0x{site:08X}: 0x{actual:08X}")


def expect_branch(pe: PeImage, site: int, opcode: int, target: int) -> int:
    if opcode <= 0xFF:
        expect_rel8(pe, site, opcode, target)
        return 2
    if pe.u8(site) != (opcode >> 8) or pe.u8(site + 1) != (opcode & 0xFF):
        raise RuntimeError(f"near-branch opcode drift at 0x{site:08X}")
    actual = site + 6 + pe.i32(site + 2)
    if actual != target:
        raise RuntimeError(f"near-branch target drift at 0x{site:08X}: 0x{actual:08X}")
    return 6


def expect_rel32_call(pe: PeImage, site: int, target: int) -> None:
    if pe.u8(site) != 0xE8:
        raise RuntimeError(f"call opcode drift at 0x{site:08X}")
    actual = site + 5 + pe.i32(site + 1)
    if actual != target:
        raise RuntimeError(f"call target drift at 0x{site:08X}: 0x{actual:08X}")


def expect_modrm(
    pe: PeImage,
    site: int,
    opcode: int,
    mod: int,
    reg: int,
    rm: int,
    disp8: int | None = None,
) -> None:
    if pe.u8(site) != opcode:
        raise RuntimeError(f"opcode drift at 0x{site:08X}")
    modrm = pe.u8(site + 1)
    actual = (modrm >> 6, (modrm >> 3) & 7, modrm & 7)
    if actual != (mod, reg, rm):
        raise RuntimeError(f"ModRM drift at 0x{site:08X}: {actual}")
    if disp8 is not None:
        if mod != 1 or rm == 4:
            raise RuntimeError("unsupported disp8 assertion form")
        if pe.i8(site + 2) != disp8:
            raise RuntimeError(f"disp8 drift at 0x{site:08X}")


def expect_stack_load(pe: PeImage, site: int, destination_reg: int, disp8: int) -> None:
    if pe.u8(site) != 0x8B:
        raise RuntimeError(f"stack-load opcode drift at 0x{site:08X}")
    modrm = pe.u8(site + 1)
    if (modrm >> 6, (modrm >> 3) & 7, modrm & 7) != (1, destination_reg, 4):
        raise RuntimeError(f"stack-load ModRM drift at 0x{site:08X}")
    if pe.u8(site + 2) != 0x24 or pe.i8(site + 3) != disp8:
        raise RuntimeError(f"stack-load SIB/disp drift at 0x{site:08X}")


def expect_push_imm(pe: PeImage, site: int, value: int) -> None:
    opcode = pe.u8(site)
    if opcode == 0x6A:
        actual = pe.i8(site + 1)
    elif opcode == 0x68:
        actual = pe.u32(site + 1)
    else:
        raise RuntimeError(f"push-immediate opcode drift at 0x{site:08X}")
    if actual != value:
        raise RuntimeError(f"push-immediate value drift at 0x{site:08X}")


def expect_push_reg(pe: PeImage, site: int, reg: int) -> None:
    if pe.u8(site) != 0x50 + reg:
        raise RuntimeError(f"push-register drift at 0x{site:08X}")


def expect_mov_reg_imm(pe: PeImage, site: int, reg: int, value: int) -> None:
    if pe.u8(site) != 0xB8 + reg or pe.u32(site + 1) != value:
        raise RuntimeError(f"mov reg,imm drift at 0x{site:08X}")


def expect_c7_mem_imm32(
    pe: PeImage, site: int, mod: int, rm: int, value: int, disp8: int | None = None
) -> None:
    if pe.u8(site) != 0xC7:
        raise RuntimeError(f"C7 opcode drift at 0x{site:08X}")
    modrm = pe.u8(site + 1)
    if (modrm >> 6, (modrm >> 3) & 7, modrm & 7) != (mod, 0, rm):
        raise RuntimeError(f"C7 ModRM drift at 0x{site:08X}")
    imm_off = site + 2
    if mod == 1:
        if disp8 is None or pe.i8(site + 2) != disp8:
            raise RuntimeError(f"C7 displacement drift at 0x{site:08X}")
        imm_off += 1
    if pe.u32(imm_off) != value:
        raise RuntimeError(f"C7 immediate drift at 0x{site:08X}")


def expect_ff_abs_call(pe: PeImage, site: int, iat_va: int) -> None:
    if pe.u8(site) != 0xFF or pe.u8(site + 1) != 0x15 or pe.u32(site + 2) != iat_va:
        raise RuntimeError(f"absolute indirect call drift at 0x{site:08X}")


def expect_ff_abs_jmp(pe: PeImage, site: int, iat_va: int) -> None:
    if pe.u8(site) != 0xFF or pe.u8(site + 1) != 0x25 or pe.u32(site + 2) != iat_va:
        raise RuntimeError(f"absolute indirect jump drift at 0x{site:08X}")


def expect_ret(pe: PeImage, site: int, pop_bytes: int | None) -> None:
    if pop_bytes is None:
        if pe.u8(site) != 0xC3:
            raise RuntimeError(f"RET drift at 0x{site:08X}")
    else:
        if pe.u8(site) != 0xC2 or struct.unpack_from("<H", pe.data, pe.va_to_off(site + 1))[0] != pop_bytes:
            raise RuntimeError(f"RET imm drift at 0x{site:08X}")


def parse_imports(pe: PeImage) -> dict[int, ImportPin]:
    import_rva, import_size = struct.unpack_from("<II", pe.data, pe.optional + 104)
    if import_rva == 0 or import_size == 0:
        raise RuntimeError("missing PE import directory")
    result: dict[int, ImportPin] = {}
    descriptor_rva = import_rva
    while True:
        descriptor_off = pe.rva_to_off(descriptor_rva)
        original_first_thunk, timestamp, forwarder, name_rva, first_thunk = struct.unpack_from(
            "<IIIII", pe.data, descriptor_off
        )
        if (original_first_thunk, timestamp, forwarder, name_rva, first_thunk) == (0, 0, 0, 0, 0):
            break
        dll_off, dll = pe.cstr_at_rva(name_rva)
        lookup_base = original_first_thunk or first_thunk
        index = 0
        while True:
            lookup_rva = lookup_base + index * 4
            lookup_off = pe.rva_to_off(lookup_rva)
            thunk = struct.unpack_from("<I", pe.data, lookup_off)[0]
            if thunk == 0:
                break
            iat_rva = first_thunk + index * 4
            iat_va = pe.image_base + iat_rva
            iat_off = pe.rva_to_off(iat_rva)
            if thunk & 0x80000000:
                symbol_off = -1
                symbol = f"#{thunk & 0xFFFF}"
            else:
                hint_name_off = pe.rva_to_off(thunk)
                symbol_off = hint_name_off + 2
                end = pe.data.find(b"\0", symbol_off)
                if end < 0:
                    raise RuntimeError("unterminated import symbol")
                symbol = pe.data[symbol_off:end].decode("ascii", "strict")
            result[iat_va] = ImportPin(
                iat_va, iat_off, descriptor_off, lookup_off, dll_off,
                symbol_off, dll, symbol,
            )
            index += 1
        descriptor_rva += 20
    return result


def verify_import_contract(imports: Mapping[int, ImportPin]) -> None:
    for expected in IMPORT_PINS:
        actual = imports.get(expected.iat_va)
        if actual != expected:
            raise RuntimeError(
                f"import drift at IAT 0x{expected.iat_va:08X}: expected {expected}, got {actual}"
            )


def verify_pool_code_reference_census(pe: PeImage) -> None:
    text_sections = [section for section in pe.sections if section[0] == ".text"]
    if len(text_sections) != 1:
        raise RuntimeError(f"expected one .text section, got {len(text_sections)}")
    _name, _rva, _vsize, raw_pointer, raw_size = text_sections[0]
    text = pe.data[raw_pointer : raw_pointer + raw_size]
    for value, expected in POOL_CODE_REFERENCE_FILE_OFFSETS.items():
        needle = struct.pack("<I", value)
        found: list[int] = []
        start = 0
        while True:
            index = text.find(needle, start)
            if index < 0:
                break
            found.append(raw_pointer + index)
            start = index + 1
        if tuple(found) != expected:
            raise RuntimeError(
                f"pool global code-reference drift for 0x{value:08X}: {found} != {expected}"
            )


def verify_key_semantics(pe: PeImage) -> None:
    for branch in BRANCH_PINS:
        width = expect_branch(pe, branch.site, branch.opcode, branch.taken)
        if branch.fallthrough is not None and branch.site + width != branch.fallthrough:
            raise RuntimeError(f"fallthrough pin drift at 0x{branch.site:08X}")
    for site, target in DIRECT_CALL_PINS.items():
        expect_rel32_call(pe, site, target)

    # Pool helper: the empty and recycled paths both invoke the same constructor.
    expect_modrm(pe, 0x00661FC6, 0x8B, 3, 6, 1)  # ESI <- pool ECX
    expect_push_imm(pe, 0x00661FEC, 0x20)
    expect_modrm(pe, 0x00662009, 0x8B, 3, 7, 0)  # EDI <- ctor EAX
    expect_modrm(pe, 0x0066205A, 0x8B, 3, 0, 7)  # return EAX <- EDI
    expect_ret(pe, 0x0066206E, 8)
    expect_push_reg(pe, 0x00662071, 7)  # recycled EDI is second helper arg
    expect_push_imm(pe, 0x00662072, 0x20)
    expect_modrm(pe, 0x00662093, 0x88, 1, 3, 0, 4)  # mark returned EAX pooled/live
    expect_ret(pe, 0x006620A8, 8)

    # Fixed object constructor and vtable slot used by the dynamic decrement.
    expect_modrm(pe, 0x005DF300, 0x8B, 3, 0, 1)  # EAX <- object ECX
    expect_modrm(pe, 0x005DF302, 0x33, 3, 1, 1)  # ECX <- zero
    expect_c7_mem_imm32(pe, 0x005DF313, 0, 0, 0x00F2FE14)
    if pe.u32(0x00F2FE14) != 0x005DED10 or pe.u32(0x00F2FE18) != 0x005DFCA0:
        raise RuntimeError("fixed vtable head drift")
    expect_c7_mem_imm32(pe, 0x005DFCA3, 0, 6, 0x00F2FE14)
    expect_ff_abs_call(pe, 0x005DFCF1, 0x00C3B4A4)

    # Refcount decrement selects [fixed_vtable+4] only at zero.
    expect_modrm(pe, 0x0088D075, 0x8B, 0, 2, 6)  # EDX <- [ESI]
    expect_modrm(pe, 0x0088D077, 0x8B, 1, 0, 2, 4)  # EAX <- [EDX+4]
    expect_push_imm(pe, 0x0088D07A, 1)
    expect_modrm(pe, 0x0088D07C, 0x8B, 3, 1, 6)  # ECX <- ESI
    if pe.u8(0x0088D07E) != 0xFF or pe.u8(0x0088D07F) != 0xD0:
        raise RuntimeError("dynamic deleting-destructor call drift")

    # Pool/release support imports are named, not guessed by address.
    expect_ff_abs_jmp(pe, 0x0088D020, 0x00C3B87C)
    expect_stack_load(pe, 0x0088D030, 0, 8)  # recycled identity returns pointer arg
    expect_ff_abs_call(pe, 0x0088D054, 0x00C3B1B0)
    expect_ff_abs_call(pe, 0x0088D067, 0x00C3B1B4)
    expect_ff_abs_call(pe, 0x0088D5B3, 0x00C3B16C)
    expect_ff_abs_call(pe, 0x0049DA43, 0x00C3B168)
    expect_ff_abs_call(pe, 0x0088F35A, 0x00C3B19C)
    expect_ff_abs_call(pe, 0x0088D2CB, 0x00C3B8F8)
    expect_ff_abs_jmp(pe, 0x00B37998, 0x00C3B4C4)

    caller_contracts = (
        # caller, stream load, helper metadata/pool/call, old/new/store/inc/reload,
        # member displacement
        (
            0x00699917, 0x00699972,
            0x006999AE, 0x006999B0, 0x006999B5, 0x006999BA,
            0x006999BF, 0x006999C2, 0x006999C4, 0x006999C8,
            0x006999D1, 0x006999D4, 0x006999D8, 0x006999DF,
            0x1C,
        ),
        (
            0x006B9EA7, 0x006B9F02,
            0x006B9F3E, 0x006B9F40, 0x006B9F45, 0x006B9F4A,
            0x006B9F4F, 0x006B9F52, 0x006B9F54, 0x006B9F58,
            0x006B9F61, 0x006B9F64, 0x006B9F68, 0x006B9F6F,
            0x18,
        ),
    )
    for contract in caller_contracts:
        (
            entry_save, stream_load,
            push_zero, push_metadata, pool_ecx, helper_call,
            old_load, new_from_eax, compare_old_new, test_old,
            member_store, test_new, new_to_ecx, member_reload,
            member,
        ) = contract
        expect_modrm(pe, entry_save, 0x8B, 3, 6, 1)  # ESI <- message ECX
        expect_stack_load(pe, stream_load, 3, 0x14)  # EBX <- stream formal
        expect_push_imm(pe, push_zero, 0)
        expect_push_imm(pe, push_metadata, 0x00F0A90C)
        expect_mov_reg_imm(pe, pool_ecx, 1, 0x01030238)
        expect_rel32_call(pe, helper_call, 0x00661FA0)
        expect_modrm(pe, old_load, 0x8B, 1, 1, 6, member)  # old ECX
        expect_modrm(pe, new_from_eax, 0x8B, 3, 7, 0)  # new EDI <- EAX
        expect_modrm(pe, compare_old_new, 0x3B, 3, 1, 7)
        expect_modrm(pe, test_old, 0x85, 3, 1, 1)
        expect_modrm(pe, member_store, 0x89, 1, 7, 6, member)  # member <- new
        expect_modrm(pe, test_new, 0x85, 3, 7, 7)
        expect_modrm(pe, new_to_ecx, 0x8B, 3, 1, 7)  # ECX <- new
        expect_modrm(pe, member_reload, 0x8B, 1, 1, 6, member)

    # Constructor base cases: target member starts null and has the target vtable.
    constructors = (
        (0x006645E9, 0x00664600, 0x00F38150, 0x0066460A, 0x1C),
        (0x00672619, 0x00672630, 0x00F3919C, 0x0067263A, 0x1C),
        (0x006990C9, 0x006990E0, 0x00F3C170, 0x006990EA, 0x1C),
        (0x006B8979, 0x006B8990, 0x00F3E41C, 0x006B899A, 0x18),
    )
    for zero_site, vtable_site, vtable, member_site, member in constructors:
        expect_modrm(pe, zero_site, 0x33, 3, 3, 3)  # EBX <- zero
        expect_c7_mem_imm32(pe, vtable_site, 0, 6, vtable)
        expect_modrm(pe, member_site, 0x89, 1, 3, 6, member)  # member <- zero EBX


def verify_semantics(pe: PeImage) -> None:
    verify_span_pins(pe)
    verify_key_semantics(pe)
    verify_import_contract(parse_imports(pe))
    verify_pool_code_reference_census(pe)


def resolution_for_tag(tag: str) -> str | None:
    if tag == "CALL_UNCLASSIFIED:0x00661FA0":
        return "FIXED_0x20_POOL_OBJECT_CONSTRUCTION_NO_STREAM_EFFECT"
    if tag == "DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04":
        return "FIXED_OBJECT_REFCOUNT_DECREMENT_TO_0x005DFCA0_NO_STREAM_EFFECT"
    if tag == "ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C":
        return "FIXED_OBJECT_REFCOUNT_INCREMENT_NO_STREAM_EFFECT"
    return None


def caller_span(message: str) -> SpanPin:
    role = "mall_serializer" if message == "ItemMallBagItemTransfer" else "shared_serializer"
    return next(pin for pin in SPAN_PINS if pin.role == role)


def build_a2_delta(
    fieldnames: Sequence[str], rows: Sequence[tuple[int, dict[str, str]]]
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    counts = {message: 0 for message in TARGETS}
    for line_no, row in rows:
        if row["message"] not in TARGETS:
            continue
        if row["source"] != "IMAGE":
            raise RuntimeError(f"target A2 row is not IMAGE at {A2_NAME}:{line_no}")
        resolution = resolution_for_tag(row["tag"])
        if resolution is None:
            continue
        if not row["field_offset"].startswith("UNKNOWN("):
            raise RuntimeError(f"target blocker field drift at {A2_NAME}:{line_no}")
        row_key = canonical_row_key(fieldnames, row)
        pin = caller_span(row["message"])
        values = {
            "action": "REMOVE_NONWIRE_ROW",
            "change_type": "NONWIRE_FIXED_POOL_OR_REFCOUNT_ARTIFACT",
            "base_file": A2_NAME,
            "base_line": str(line_no),
            "base_row_key": row_key,
            "message": row["message"],
            "direction(W/R)": row["direction(W/R)"],
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
            "evidence_ticket": EVIDENCE_ID,
            "evidence_span_start": f"0x{pin.start_va:08X}",
            "evidence_span_end": f"0x{pin.end_va:08X}",
            "evidence_span_sha256": pin.sha256,
            "evidence_file_off": row["file_off_claim"],
            "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(
            ("A2", values["action"], row["message"], str(line_no), row_key)
        )
        output.append(values)
        counts[row["message"]] += 1

    expected = {message: 6 for message in TARGETS}
    if counts != expected:
        raise RuntimeError(f"target A2 blocker-count drift: {counts} != {expected}")
    if len(output) != 24:
        raise RuntimeError(f"expected 24 A2 directives, got {len(output)}")
    if len({row["delta_key"] for row in output}) != len(output):
        raise RuntimeError("duplicate A2 delta_key")
    if len({(row["base_line"], row["base_row_key"]) for row in output}) != len(output):
        raise RuntimeError("one A2 base row was targeted more than once")
    output.sort(
        key=lambda row: (
            TARGETS.index(row["message"]),
            0 if row["direction(W/R)"] == "W" else 1,
            int(row["base_line"]),
        )
    )
    return output


def validate_a2_overlay_closure(
    rows: Sequence[tuple[int, dict[str, str]]],
    delta: Sequence[Mapping[str, str]],
) -> None:
    if len({row["delta_key"] for row in delta}) != len(delta):
        raise RuntimeError("duplicate A2 delta_key during overlay validation")
    by_line = {int(row["base_line"]): row for row in delta}
    if len(by_line) != len(delta):
        raise RuntimeError("duplicate A2 base line during overlay validation")
    unresolved: list[str] = []
    remaining = {message: 0 for message in TARGETS}
    for line_no, row in rows:
        if row["message"] not in TARGETS:
            continue
        directive = by_line.get(line_no)
        if directive is not None:
            if directive["action"] != "REMOVE_NONWIRE_ROW":
                raise RuntimeError("unexpected A2 action")
            continue
        remaining[row["message"]] += 1
        tag = row["tag"]
        blocker = tag == "UNKNOWN" or tag.startswith(
            ("CALL_UNCLASSIFIED:", "JUMP_UNCLASSIFIED:", "DYNAMIC_", "ATOMIC_", "PE_IMPORT_")
        )
        if blocker or "UNKNOWN(" in row["field_offset"]:
            unresolved.append(f"{row['message']}:{line_no}:{tag}:{row['field_offset']}")
    if any(value == 0 for value in remaining.values()):
        raise RuntimeError(f"overlay removed all wire rows: {remaining}")
    if unresolved:
        raise RuntimeError("residual target blockers: " + " | ".join(unresolved))


def parse_existing_priority_overlay(
    path: Path,
    base_fields: Sequence[str],
    base_rows: Sequence[tuple[int, dict[str, str]]],
) -> set[str]:
    _fields, rows = read_tsv_with_lines(path)
    base_by_line = {line: row for line, row in base_rows}
    changed: set[str] = set()
    for line_no, row in rows:
        if row["action"] != "CHANGED" or row["source"] != "IMAGE":
            raise RuntimeError(f"unexpected prior priority directive at {path.name}:{line_no}")
        base_line = int(row["base_line"])
        base = base_by_line.get(base_line)
        if base is None:
            raise RuntimeError(f"prior priority base line missing: {base_line}")
        if canonical_row_key(base_fields, base) != row["base_row_key"]:
            raise RuntimeError(f"prior priority base-row hash drift: {base_line}")
        if row["message"] != base["message"] or row["new_serializer_status"] != "CLOSED":
            raise RuntimeError(f"prior priority directive drift: {base_line}")
        if row["message"] in changed:
            raise RuntimeError(f"duplicate prior priority target: {row['message']}")
        changed.add(row["message"])
    if len(changed) != 3:
        raise RuntimeError(f"expected three prior closures, got {sorted(changed)}")
    return changed


def build_priority_delta(
    fieldnames: Sequence[str],
    rows: Sequence[tuple[int, dict[str, str]]],
    prior_closed: set[str],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    p1 = [(line, row) for line, row in rows if row["priority"] == "1"]
    v1_closed = {
        row["message"]
        for _line, row in p1
        if row["registry_identity_status"] == "KNOWN"
        and row["serializer_status"] == "CLOSED"
        and row["structural_status"] == "CLOSED"
    }
    if len(p1) != 365 or len(v1_closed) != 241:
        raise RuntimeError(f"V1 Priority-1 drift: total={len(p1)} closed={len(v1_closed)}")
    effective_before = v1_closed | prior_closed
    if len(effective_before) != 244:
        raise RuntimeError(f"post-V1 effective closed drift: {len(effective_before)}")

    found: dict[str, tuple[int, dict[str, str]]] = {}
    for line_no, row in rows:
        if row["message"] in TARGETS:
            if row["message"] in found:
                raise RuntimeError(f"duplicate priority target: {row['message']}")
            found[row["message"]] = (line_no, row)
    if set(found) != set(TARGETS):
        raise RuntimeError(f"missing priority targets: {sorted(set(TARGETS) - set(found))}")

    output: list[dict[str, str]] = []
    for message in TARGETS:
        line_no, row = found[message]
        if message in effective_before:
            raise RuntimeError(f"target already closed before this overlay: {message}")
        if row["source"] != "IMAGE" or row["priority"] != "1":
            raise RuntimeError(f"target source/priority drift: {message}")
        if row["registry_identity_status"] != "KNOWN":
            raise RuntimeError(f"target identity not known: {message}")
        if row["serializer_status"] != "OPEN" or row["structural_status"] != "OPEN":
            raise RuntimeError(f"target is not V1 OPEN/OPEN: {message}")
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
            "evidence_ticket": EVIDENCE_ID,
            "closure_scope": "STATIC_WIRE_STRUCTURE_ONLY;RUNTIME_SEMANTICS_NOT_PROMOTED",
            "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(
            ("PRIORITY", values["action"], message, str(line_no), row_key, "CLOSED")
        )
        output.append(values)

    if len(output) != 4 or len({row["delta_key"] for row in output}) != 4:
        raise RuntimeError("priority delta cardinality/dedup failure")
    counts = {
        "total": 365,
        "v1_closed": 241,
        "before_closed": 244,
        "before_open": 121,
        "after_closed": 248,
        "after_open": 117,
    }
    if len(effective_before | set(TARGETS)) != counts["after_closed"]:
        raise RuntimeError("effective Priority-1 count calculation drift")
    return output, counts


def validate_prior_a2_no_overlap(path: Path, delta: Sequence[Mapping[str, str]]) -> None:
    _fields, prior = read_tsv_with_lines(path)
    prior_targets = {(row["base_line"], row["base_row_key"]) for _line, row in prior}
    current = {(row["base_line"], row["base_row_key"]) for row in delta}
    overlap = prior_targets & current
    if overlap:
        raise RuntimeError(f"A2 directive duplicates prior post-V1 overlay rows: {sorted(overlap)}")


def run_mutation_guards(
    image: bytes,
    a2_rows: Sequence[tuple[int, dict[str, str]]],
    a2_delta: Sequence[Mapping[str, str]],
    imports: Mapping[int, ImportPin],
) -> None:
    # Each claim-specific byte mutation is checked without relying on whole-span SHA.
    mutations = (
        ("fixed_ctor_vtable", 0x005DF315),
        ("shared_helper_call_target", 0x006999BB),
        ("shared_member_store_disp", 0x006999D3),
        ("fixed_vtable_plus_4", 0x00F2FE18),
    )
    base = PeImage(image)
    for label, va in mutations:
        mutated = bytearray(image)
        mutated[base.va_to_off(va)] ^= 1
        try:
            verify_key_semantics(PeImage(mutated))
        except RuntimeError:
            continue
        raise RuntimeError(f"synthetic semantic mutation unexpectedly passed: {label}")

    altered_imports = dict(imports)
    pin = altered_imports[0x00C3B1B4]
    altered_imports[pin.iat_va] = ImportPin(
        pin.iat_va, pin.iat_file_off, pin.descriptor_file_off,
        pin.lookup_file_off, pin.dll_file_off, pin.symbol_file_off,
        pin.dll, "InterlockedIncrement",
    )
    try:
        verify_import_contract(altered_imports)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("synthetic import-name mutation unexpectedly passed")

    try:
        validate_a2_overlay_closure(a2_rows, a2_delta[:-1])
    except RuntimeError:
        pass
    else:
        raise RuntimeError("synthetic missing-directive mutation unexpectedly passed")

    duplicated = list(a2_delta) + [dict(a2_delta[0])]
    try:
        validate_a2_overlay_closure(a2_rows, duplicated)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("synthetic duplicate-directive mutation unexpectedly passed")

    sample_line, sample = next((line, row) for line, row in a2_rows if row["message"] == TARGETS[0])
    synthetic = dict(sample)
    synthetic["order"] = "999999"
    synthetic["tag"] = "CALL_UNCLASSIFIED:0x00661FA0"
    synthetic["field_offset"] = "UNKNOWN(synthetic_residual)"
    try:
        validate_a2_overlay_closure(
            tuple(a2_rows) + ((max(line for line, _row in a2_rows) + 1, synthetic),),
            a2_delta,
        )
    except RuntimeError:
        pass
    else:
        raise RuntimeError(
            f"synthetic residual-blocker mutation unexpectedly passed (sample {sample_line})"
        )


def report_text(
    a2_delta: Sequence[Mapping[str, str]],
    priority_delta: Sequence[Mapping[str, str]],
    counts: Mapping[str, int],
    a2_hash: str,
    priority_hash: str,
) -> str:
    span_lines = [
        f"| {pin.role} | `0x{pin.start_va:08X}` | `0x{pin.end_va:08X}` | "
        f"`0x{pin.file_off:08X}` | `{pin.sha256}` |"
        for pin in SPAN_PINS
    ]
    import_lines = [
        f"| `{pin.dll}!{pin.symbol}` | `0x{pin.iat_va:08X}` | "
        f"`0x{pin.iat_file_off:08X}` | `0x{pin.descriptor_file_off:08X}` | "
        f"`0x{pin.lookup_file_off:08X}` | `0x{pin.dll_file_off:08X}` | "
        f"`0x{pin.symbol_file_off:08X}` |"
        for pin in IMPORT_PINS
    ]
    branch_lines = [
        f"| {pin.function} | `0x{pin.site:08X}` | `0x{pin.taken:08X}` | "
        + (f"`0x{pin.fallthrough:08X}` |" if pin.fallthrough is not None else "N/A |")
        for pin in BRANCH_PINS
    ]
    def call_owner(site: int) -> str:
        if 0x00661FA0 <= site < 0x006620AB:
            return "pool_allocator"
        if 0x00699910 <= site < 0x006999EE:
            return "shared_serializer"
        if 0x006B9EA0 <= site < 0x006B9F80:
            return "mall_serializer"
        if 0x005DFCA0 <= site < 0x005DFCFE:
            return "fixed_deleting_destructor"
        raise RuntimeError(f"unclassified direct-call pin 0x{site:08X}")

    call_lines = [
        f"| {call_owner(site)} | `0x{site:08X}` | `0x{target:08X}` |"
        for site, target in DIRECT_CALL_PINS.items()
    ]
    return "\n".join(
        [
            "# PF 0x00661FA0 fixed-pool closure overlay",
            "",
            "[MEASURED] This additive overlay was re-derived from the pinned IMAGE and frozen V1 rows. It contains no dump, capture, or data-layer fact.",
            "",
            "## Outcome",
            "",
            f"- Removed **{len(a2_delta)}** duplicated A2 analysis artifacts (six per target): the pool helper, old-object decrement, and new-object increment each appeared once under R and once under W in V1 even though they are read-branch lifecycle operations, not wire fields.",
            f"- Closed exactly **{len(priority_delta)}** Priority-1 messages: `TradeCmdVital`, `GCGS_GuildStorageCmdVital`, `StorageCmdVital`, and `ItemMallBagItemTransfer`.",
            f"- Within the explicit overlay chain V1 (241) + the existing post-V1 static delta (3) + this delta (4), Priority 1 moves from **{counts['before_closed']}/{counts['total']}** to **{counts['after_closed']}/{counts['total']}**; open moves from **{counts['before_open']}** to **{counts['after_open']}**.",
            "- That 248/365 number is this overlay chain's measured checkpoint, not a promise that a later independent Attr correction or later manifest will keep the same global headline.",
            "",
            "## Base-before-delta / duplicate accounting",
            "",
            "| table | added | changed | remove-nonwire directives | unchanged copied | duplicate rejected |",
            "|---|---:|---:|---:|---:|---:|",
            "| A2 pool delta | 0 | 0 | 24 | 0 | 0 |",
            "| Priority pool delta | 0 | 4 | 0 | 0 | 0 |",
            "",
            "Every directive names the exact frozen V1 line and canonical row SHA-256. The generator also verifies that none overlaps `PF_A2_POST_V1_STATIC_DELTA.tsv`; no unchanged V1 row is copied.",
            "",
            "## Why 0x00661FA0 is not a serializer",
            "",
            "- The helper's complete CFG is pinned below. Its successful direct-call set is critical-section entry/leave, `malloc`, a fixed constructor, recycled-pointer identity, and an allocation counter. Its allocation-failure path constructs and throws an exception. It has no stream formal and receives only `ECX=0x01030238`, metadata `0x00F0A90C`, and zero at both target call sites.",
            "- Empty-pool and recycled-pool paths both call `0x005DF300`. That constructor hard-codes vtable `0x00F2FE14`; slot `+0x04` is exactly `0x005DFCA0`. The pool-head code-reference census pins all IMAGE code references to `0x01030238/3C/4C`; the only pool-return bodies are the same fixed object's deleting destructor and its size-0x20 exception cleanup.",
            "- In `0x00699910`, `ESI` is the message, the read-path `EBX` is the stream, the helper result becomes `EDI`, old is loaded from `[ESI+0x1C]`, new is stored to `[ESI+0x1C]`, decrement receives old in `ECX`, and increment receives new in `ECX`. `0x006B9EA0` is identical with member `+0x18`. Neither atomic helper can alias the stream reaching definition.",
            "- All four target constructors set the member to null. The only non-null member definition in the two pinned serializer bodies is the fixed helper result. At refcount zero, `0x0088D060` dispatches fixed vtable slot `+0x04` to `0x005DFCA0`; that body performs only base cleanup, pool return, or `free`. Its reachable base cleanup can show `MessageBoxW` on an invalid live-refcount condition but has no stream access.",
            "",
            "This proves that the six V1 UNKNOWN rows per message are lifecycle/control artifacts. It does not change any numeric/tagged wire row already present in V1.",
            "",
            "## Exact CFG branch pins",
            "",
            "| function | branch site | taken target | fallthrough |",
            "|---|---:|---:|---:|",
            *branch_lines,
            "",
            "The pool helper has return sites `0x0066206E` and `0x006620A8`, both `ret 8`. The shared serializer returns at `0x0069996F` and `0x006999ED`; the mall serializer returns at `0x006B9EFF` and `0x006B9F7D`.",
            "",
            "## Exact direct-call pins",
            "",
            "| function | call site | direct target |",
            "|---|---:|---:|",
            *call_lines,
            "",
            "Indirect support calls are separately resolved through the named PE import pins below; the zero-refcount dynamic call is pinned as fixed vtable `0x00F2FE14` slot `+0x04` -> `0x005DFCA0`.",
            "",
            "## IMAGE span pins",
            "",
            "| role | start VA | end VA (exclusive) | file offset | SHA-256 |",
            "|---|---:|---:|---:|---|",
            *span_lines,
            "",
            "## Import pins",
            "",
            "| import | IAT VA | IAT file offset | descriptor file offset | lookup file offset | DLL file offset | symbol file offset |",
            "|---|---:|---:|---:|---:|---:|---:|",
            *import_lines,
            "",
            "The TSV rows remain single-layer `source=IMAGE` facts.",
            "",
            "## Guards and nonclaims",
            "",
            "- `--check` re-derives all rows and compares all three outputs byte-for-byte.",
            "- Independent mutation controls must reject: constructor-vtable drift, helper-call target drift, member-store displacement drift, vtable `+0x04` drift, import-name drift, a missing directive, a duplicate directive, and a synthetic residual blocker.",
            "- Closure means static wire structure only. Runtime behavior, gameplay meaning, capture validation, and dump identity are not promoted.",
            "- No raw proprietary byte sequence is emitted; outputs contain only addresses, structure, counts, and SHA-256 values.",
            "",
            "## Output hashes",
            "",
            f"- `{A2_DELTA_NAME}`: `{a2_hash}`",
            f"- `{PRIORITY_DELTA_NAME}`: `{priority_hash}`",
            "",
            "All TSV rows have `source=IMAGE`.",
            "",
        ]
    )


def build_outputs(
    image_path: Path,
    external_dir: Path,
) -> tuple[dict[str, str], dict[str, str]]:
    inputs = {
        "image": IMAGE_SHA256,
        "a2": A2_SHA256,
        "priority": PRIORITY_SHA256,
        "post_v1_a2": POST_V1_A2_SHA256,
        "post_v1_priority": POST_V1_PRIORITY_SHA256,
    }
    paths = {
        "image": image_path,
        "a2": external_dir / A2_NAME,
        "priority": external_dir / PRIORITY_NAME,
        "post_v1_a2": external_dir / POST_V1_A2_NAME,
        "post_v1_priority": external_dir / POST_V1_PRIORITY_NAME,
    }
    for label, expected in inputs.items():
        require_hash(paths[label], expected, label)

    image = image_path.read_bytes()
    pe = PeImage(image)
    verify_semantics(pe)

    a2_fields, a2_rows = read_tsv_with_lines(paths["a2"])
    priority_fields, priority_rows = read_tsv_with_lines(paths["priority"])
    prior_closed = parse_existing_priority_overlay(
        paths["post_v1_priority"], priority_fields, priority_rows
    )
    a2_delta = build_a2_delta(a2_fields, a2_rows)
    validate_prior_a2_no_overlap(paths["post_v1_a2"], a2_delta)
    validate_a2_overlay_closure(a2_rows, a2_delta)
    priority_delta, counts = build_priority_delta(priority_fields, priority_rows, prior_closed)
    run_mutation_guards(image, a2_rows, a2_delta, parse_imports(pe))

    a2_text = write_tsv_text(A2_DELTA_COLUMNS, a2_delta)
    priority_text = write_tsv_text(PRIORITY_DELTA_COLUMNS, priority_delta)
    a2_hash = sha256_bytes(a2_text.encode("utf-8"))
    priority_hash = sha256_bytes(priority_text.encode("utf-8"))
    report = report_text(a2_delta, priority_delta, counts, a2_hash, priority_hash)
    outputs = {
        A2_DELTA_NAME: a2_text,
        PRIORITY_DELTA_NAME: priority_text,
        REPORT_NAME: report,
    }
    snapshot = {str(path): sha256_path(path) for path in paths.values()}
    return outputs, snapshot


def check_outputs(external_dir: Path, outputs: Mapping[str, str]) -> None:
    mismatches: list[str] = []
    for name, expected in outputs.items():
        path = external_dir / name
        if not path.exists():
            mismatches.append(f"missing {name}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            mismatches.append(f"content drift {name}")
    if mismatches:
        raise RuntimeError("--check failed: " + "; ".join(mismatches))


def main() -> int:
    default_external = Path(__file__).resolve().parent
    default_image = default_external.parents[1] / "GameClient" / "GameClient.local.bin"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external-dir", type=Path, default=default_external)
    parser.add_argument("--image", type=Path, default=default_image)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    external_dir = args.external_dir.resolve()
    image_path = args.image.resolve()
    outputs, snapshot = build_outputs(image_path, external_dir)
    if args.check:
        check_outputs(external_dir, outputs)
        print(
            f"CHECK OK: A2 directives=24 Priority changes=4 effective_P1=248/365 "
            f"outputs={len(outputs)}"
        )
        return 0

    # Rehash every input immediately before publication.
    for path_text, expected in snapshot.items():
        path = Path(path_text)
        actual = sha256_path(path)
        if actual != expected:
            raise RuntimeError(
                f"input changed after derivation and before publish: {path}: {expected} -> {actual}"
            )
    for name, text in outputs.items():
        atomic_write_text(external_dir / name, text)
    check_outputs(external_dir, outputs)
    print(
        f"PUBLISHED: A2 directives=24 Priority changes=4 effective_P1=248/365 "
        f"outputs={len(outputs)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
