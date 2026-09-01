#!/usr/bin/env python3
"""Build the IMAGE-only stack-local link-state-helper removal overlay.

The frozen V1 A2 rows and all prior overlays are inputs only.  This builder
selects the exact Priority-1/object-alias cluster whose helper receiver is an
immediate stack-local LEA, proves both fixed helpers against the pinned image,
and emits removal directives only for the 40 still-untouched V1 rows.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import struct
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable, Mapping, Sequence


IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
A2_SHA256 = "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
P1_OPEN_SHA256 = "a3c5250184efacf1681d95f910833140019a59cc3065f570de32ac307a4a11e5"

A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
P1_OPEN_NAME = "PF_V2_P1_OPEN.tsv"
OUTPUT_NAME = "PF_A2_ITERATOR_HELPERS_NONWIRE_DELTA.tsv"
REPORT_NAME = "PF_ITERATOR_HELPERS_NONWIRE.md"
EVIDENCE_TICKET = "STATIC-LINK-STATE-HELPERS-B0BF70-46D2B0"
VA_TO_FILE_DELTA = 0x00400C00
PRIMARY_GROUP = "OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED"

CHAIN_TAG = "MUTATING_CHAIN_PLUS_04_HELPER"
POINTER_TAG = "MUTATING_POINTER_SLOT_TRAVERSAL_HELPER"
TAG_TARGET = {CHAIN_TAG: 0x00B0BF70, POINTER_TAG: 0x0046D2B0}
TAG_BLOCKER = {
    CHAIN_TAG: "mutable_chain_target_object_alias_unproved",
    POINTER_TAG: "mutable_pointer_slot_traversal_alias_unproved",
}
TAG_REGEX = {
    CHAIN_TAG: re.compile(r"mutable_chain_call@(0x[0-9A-Fa-f]+)"),
    POINTER_TAG: re.compile(
        r"mutable_pointer_slot_traversal_call@(0x[0-9A-Fa-f]+)"
    ),
}


@dataclass(frozen=True)
class SpanPin:
    role: str
    start_va: int
    end_va: int
    file_off: int
    sha256: str


@dataclass(frozen=True)
class HelperPin:
    role: str
    tag: str
    start_va: int
    end_va: int
    file_off: int
    sha256: str
    flag_offset: int
    import_load_va: int
    guard_calls: tuple[int, int]
    writes: tuple[int, int, int]
    returns: tuple[int, int, int]


@dataclass(frozen=True)
class CallerPin:
    tag: str
    site_va: int
    lea_hex: str
    messages: tuple[str, ...]
    row_count: int


HELPERS = (
    HelperPin(
        "chain_plus_04_link_state",
        CHAIN_TAG,
        0x00B0BF70,
        0x00B0BFDC,
        0x0070B370,
        "4e1374fd126457c82d11bf3e6efa0fda845bb85e2c2a985ed67c4eff3f4eb7e6",
        0x15,
        0x00B0BF77,
        (0x00B0BF7F, 0x00B0BF8A),
        (0x00B0BFAB, 0x00B0BFC8, 0x00B0BFD7),
        (0x00B0BF8E, 0x00B0BFAF, 0x00B0BFDB),
    ),
    HelperPin(
        "pointer_slot_link_state",
        POINTER_TAG,
        0x0046D2B0,
        0x0046D31C,
        0x0006C6B0,
        "492e39afb9faf38f4f862abcdaa6278740417a4b1fc1e56d61a6b992421d5cf9",
        0x21,
        0x0046D2B7,
        (0x0046D2BF, 0x0046D2CA),
        (0x0046D2EB, 0x0046D308, 0x0046D317),
        (0x0046D2CE, 0x0046D2EF, 0x0046D31B),
    ),
)

CALLER_SPANS = (
    SpanPin("guild_event_shared", 0x0049F730, 0x004A04BA, 0x0009EB30, "50483292aaf0bff628f4d16be02243afc6a041dd7c016f437fa921ded8bcc4d2"),
    SpanPin("ServerAddedInfoVital", 0x005EBCF0, 0x005EBE33, 0x001EB0F0, "f3608dd2456f8577a585e35164b6990d465abb1ffd73697ff7f103e4cbd34960"),
    SpanPin("CArenaGameDataVital_1", 0x00623800, 0x0062399B, 0x00222C00, "3859758e8fb91d61925d819cc34a82881f58f32a948ce5d4d17d5f38ac83c113"),
    SpanPin("CArenaGameDataVital_2", 0x00624240, 0x00624469, 0x00223640, "883052123472f74639fa2a8d7670c16d10aaaf56d77d31c098b83b00c58468ac"),
    SpanPin("CArenaGameDataVital_3", 0x00624FB0, 0x006251B5, 0x002243B0, "78787fd06ab1944e52cca58702f3a998612e802a3058121a707f7211ac744c9d"),
    SpanPin("ItemMallUpdatePersonalDataVital", 0x006B0D20, 0x006B0FBC, 0x002B0120, "142b0ecac21efcf62367aec12d0dfab558c0bdd66428b8f2922a6b89367cd664"),
    SpanPin("Express_ClientSendExpressVital", 0x006E82F0, 0x006E851D, 0x002E76F0, "2f8702e4ffd7f881c86edb400a2604000e6c8167bb045a2620515a1643227f91"),
    SpanPin("CHitParadeVital_write", 0x007156D0, 0x0071593C, 0x00314AD0, "fa9b70c361e9b9d9e03d4106079dc32cc5417ef73428e4cbb1825d9f11abd995"),
    SpanPin("CHitParadeVital_read", 0x00716220, 0x007163F8, 0x00315620, "7cbbd7d8212c9102e8e026592559fb33c4322e8ff214b0f0a5ec906e39feac5c"),
)

GUILD_MESSAGES = (
    "GSSS_GuildEventVitalReq",
    "GSSS_GuildEventVitalRes",
    "GSSS_GuildUpdateEventVital",
)
CALLERS = (
    CallerPin(CHAIN_TAG, 0x0049F83E, "8d4c241c", GUILD_MESSAGES, 6),
    CallerPin(CHAIN_TAG, 0x0049F954, "8d4c241c", GUILD_MESSAGES, 6),
    CallerPin(CHAIN_TAG, 0x0049FA0E, "8d4c241c", GUILD_MESSAGES, 6),
    CallerPin(CHAIN_TAG, 0x005EBD9E, "8d4c2410", ("ServerAddedInfoVital",), 2),
    CallerPin(CHAIN_TAG, 0x006B0E40, "8d4c2410", ("ItemMallUpdatePersonalDataVital",), 2),
    CallerPin(CHAIN_TAG, 0x007157AC, "8d4c2420", ("CHitParadeVital",), 2),
    CallerPin(CHAIN_TAG, 0x00716316, "8d4c2410", ("CHitParadeVital",), 2),
    CallerPin(POINTER_TAG, 0x0049F8C9, "8d4c241c", GUILD_MESSAGES, 6),
    CallerPin(POINTER_TAG, 0x006238CE, "8d4c2410", ("CArenaGameDataVital",), 2),
    CallerPin(POINTER_TAG, 0x006242F7, "8d4c2418", ("CArenaGameDataVital",), 2),
    CallerPin(POINTER_TAG, 0x00625057, "8d4c2418", ("CArenaGameDataVital",), 2),
    CallerPin(POINTER_TAG, 0x006E83FC, "8d4c2414", ("Express_ClientSendExpressVital",), 2),
)

# Exact V1 rows selected by the P1/object-alias filter.  The tuple is
# (line, message, direction, order, tag, physical helper callsite).
EXPECTED_ROWS = (
    (978, "ServerAddedInfoVital", "R", "6", CHAIN_TAG, 0x005EBD9E),
    (979, "ServerAddedInfoVital", "W", "9", CHAIN_TAG, 0x005EBD9E),
    (1685, "CArenaGameDataVital", "W", "23", POINTER_TAG, 0x006238CE),
    (1688, "CArenaGameDataVital", "W", "26", POINTER_TAG, 0x006242F7),
    (1700, "CArenaGameDataVital", "R", "5", POINTER_TAG, 0x00625057),
    (1701, "CArenaGameDataVital", "W", "38", POINTER_TAG, 0x00625057),
    (1713, "CArenaGameDataVital", "R", "14", POINTER_TAG, 0x006242F7),
    (1725, "CArenaGameDataVital", "R", "26", POINTER_TAG, 0x006238CE),
    (2632, "GSSS_GuildEventVitalReq", "W", "13", CHAIN_TAG, 0x0049F83E),
    (2640, "GSSS_GuildEventVitalReq", "W", "21", POINTER_TAG, 0x0049F8C9),
    (2648, "GSSS_GuildEventVitalReq", "W", "29", CHAIN_TAG, 0x0049F954),
    (2657, "GSSS_GuildEventVitalReq", "W", "38", CHAIN_TAG, 0x0049FA0E),
    (2719, "GSSS_GuildEventVitalReq", "R", "9", CHAIN_TAG, 0x0049F83E),
    (2725, "GSSS_GuildEventVitalReq", "R", "15", POINTER_TAG, 0x0049F8C9),
    (2731, "GSSS_GuildEventVitalReq", "R", "21", CHAIN_TAG, 0x0049F954),
    (2738, "GSSS_GuildEventVitalReq", "R", "28", CHAIN_TAG, 0x0049FA0E),
    (2816, "GSSS_GuildEventVitalRes", "W", "13", CHAIN_TAG, 0x0049F83E),
    (2824, "GSSS_GuildEventVitalRes", "W", "21", POINTER_TAG, 0x0049F8C9),
    (2832, "GSSS_GuildEventVitalRes", "W", "29", CHAIN_TAG, 0x0049F954),
    (2841, "GSSS_GuildEventVitalRes", "W", "38", CHAIN_TAG, 0x0049FA0E),
    (2903, "GSSS_GuildEventVitalRes", "R", "9", CHAIN_TAG, 0x0049F83E),
    (2909, "GSSS_GuildEventVitalRes", "R", "15", POINTER_TAG, 0x0049F8C9),
    (2915, "GSSS_GuildEventVitalRes", "R", "21", CHAIN_TAG, 0x0049F954),
    (2922, "GSSS_GuildEventVitalRes", "R", "28", CHAIN_TAG, 0x0049FA0E),
    (3586, "GSSS_GuildUpdateEventVital", "W", "13", CHAIN_TAG, 0x0049F83E),
    (3594, "GSSS_GuildUpdateEventVital", "W", "21", POINTER_TAG, 0x0049F8C9),
    (3602, "GSSS_GuildUpdateEventVital", "W", "29", CHAIN_TAG, 0x0049F954),
    (3611, "GSSS_GuildUpdateEventVital", "W", "38", CHAIN_TAG, 0x0049FA0E),
    (3673, "GSSS_GuildUpdateEventVital", "R", "9", CHAIN_TAG, 0x0049F83E),
    (3679, "GSSS_GuildUpdateEventVital", "R", "15", POINTER_TAG, 0x0049F8C9),
    (3685, "GSSS_GuildUpdateEventVital", "R", "21", CHAIN_TAG, 0x0049F954),
    (3692, "GSSS_GuildUpdateEventVital", "R", "28", CHAIN_TAG, 0x0049FA0E),
    (4683, "ItemMallUpdatePersonalDataVital", "R", "7", CHAIN_TAG, 0x006B0E40),
    (4684, "ItemMallUpdatePersonalDataVital", "W", "15", CHAIN_TAG, 0x006B0E40),
    (5465, "Express_ClientSendExpressVital", "R", "9", POINTER_TAG, 0x006E83FC),
    (5466, "Express_ClientSendExpressVital", "W", "13", POINTER_TAG, 0x006E83FC),
    (5926, "CHitParadeVital", "W", "34", CHAIN_TAG, 0x007157AC),
    (5952, "CHitParadeVital", "R", "6", CHAIN_TAG, 0x00716316),
    (5953, "CHitParadeVital", "W", "55", CHAIN_TAG, 0x00716316),
    (5962, "CHitParadeVital", "R", "15", CHAIN_TAG, 0x007157AC),
)

MASK_OFFSETS = (22, 36, 44, 54, 69, 98)
EXPECTED_FAMILY = (
    (0x004493B0, 0x79), (0x00454530, 0x49), (0x0046D2B0, 0x21),
    (0x0050B3C0, 0x3D), (0x005247E0, 0x55), (0x00524850, 0x65),
    (0x005625B0, 0x61), (0x0057CEE0, 0x29), (0x005D2180, 0x19),
    (0x005DABB0, 0x4D), (0x006564E0, 0x0F), (0x0065E260, 0x45),
    (0x006835E0, 0x25), (0x006F7AE0, 0x31), (0x0073AEF0, 0x1D),
    (0x0073AF60, 0x35), (0x0073F160, 0x71), (0x007424F0, 0x41),
    (0x00745B20, 0x69), (0x00765540, 0x39), (0x0077ACD0, 0x51),
    (0x00B0BF70, 0x15), (0x00B0C5D0, 0x11), (0x00B1B8C0, 0x2D),
)

WIRE_PRIMITIVE_COUNTS = {0x0089A600: 1350, 0x0089A640: 1350}

A2_DELTA_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line",
    "base_row_key", "base_delta_key", "message", "direction(W/R)",
    "old_order", "old_tag", "old_field_offset", "old_len",
    "new_wire_order", "new_tag", "new_field_offset", "new_len",
    "new_gate_condition", "resolution", "evidence_ticket",
    "evidence_span_start", "evidence_span_end", "evidence_span_sha256",
    "evidence_file_off", "source",
)


class BuildError(RuntimeError):
    pass


@dataclass(frozen=True)
class Section:
    name: str
    rva: int
    virtual_size: int
    raw_off: int
    raw_size: int


@dataclass(frozen=True)
class PEInfo:
    image_base: int
    size_of_headers: int
    sections: tuple[Section, ...]
    import_rva: int
    import_size: int

    def rva_to_off(self, rva: int) -> int:
        if 0 <= rva < self.size_of_headers:
            return rva
        for section in self.sections:
            delta = rva - section.rva
            if 0 <= delta < section.raw_size:
                return section.raw_off + delta
        raise BuildError(f"cannot map RVA 0x{rva:08X}")

    def raw_to_va(self, raw_off: int) -> int | None:
        if 0 <= raw_off < self.size_of_headers:
            return self.image_base + raw_off
        for section in self.sections:
            delta = raw_off - section.raw_off
            if 0 <= delta < section.raw_size:
                return self.image_base + section.rva + delta
        return None


@dataclass(frozen=True)
class DecodedInstruction:
    va: int
    size: int
    kind: str
    successors: tuple[int, ...]
    memory_write: bool = False


@dataclass(frozen=True)
class CfgCensus:
    instruction_nodes: int
    basic_blocks: int
    decode_errors: int
    direct_calls: int
    indirect_calls: int
    guard_calls_dominated: int
    guard_calls_singleton_edi: int
    memory_writes: tuple[int, ...]
    covered_bytes: int


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
        raise BuildError(f"{label} SHA-256 mismatch: expected {expected}, got {actual}")


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
            raise BuildError(f"missing TSV header: {path.name}")
        fields = list(reader.fieldnames)
        rows = [(line, dict(row)) for line, row in enumerate(reader, start=2)]
    return fields, rows


def tsv_text(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
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


def publish_outputs(outputs: Mapping[Path, str]) -> None:
    """Stage and verify every output, then commit all with rollback."""
    staged: dict[Path, str] = {}
    backups: dict[Path, str | None] = {}
    originals: dict[Path, bool] = {path: path.exists() for path in outputs}
    try:
        for path, expected in outputs.items():
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                dir=path.parent,
                prefix=f".{path.name}.stage.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                staged[path] = handle.name
                handle.write(expected)
                handle.flush()
                os.fsync(handle.fileno())
            staged_text = Path(staged[path]).read_text(encoding="utf-8")
            if staged_text != expected:
                raise BuildError(f"staged output verification failed: {path.name}")

        for path in outputs:
            backup_name: str | None = None
            if path.exists():
                with tempfile.NamedTemporaryFile(
                    dir=path.parent,
                    prefix=f".{path.name}.rollback.",
                    suffix=".tmp",
                    delete=False,
                ) as handle:
                    backup_name = handle.name
                os.unlink(backup_name)
                os.replace(path, backup_name)
            backups[path] = backup_name
            os.replace(staged[path], path)
            staged.pop(path)

        for path, expected in outputs.items():
            if path.read_text(encoding="utf-8") != expected:
                raise BuildError(f"published output verification failed: {path.name}")
        for backup in backups.values():
            if backup is not None and os.path.exists(backup):
                os.unlink(backup)
    except Exception:
        for path in reversed(tuple(outputs)):
            backup = backups.get(path)
            if backup is not None and os.path.exists(backup):
                if path.exists():
                    os.unlink(path)
                os.replace(backup, path)
            elif path in backups and not originals[path] and path.exists():
                os.unlink(path)
        raise
    finally:
        for staged_name in staged.values():
            if os.path.exists(staged_name):
                os.unlink(staged_name)
        for backup in backups.values():
            if backup is not None and os.path.exists(backup):
                os.unlink(backup)


def parse_pe(image: bytes) -> PEInfo:
    if image[:2] != b"MZ":
        raise BuildError("missing MZ signature")
    pe_off = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_off:pe_off + 4] != b"PE\0\0":
        raise BuildError("missing PE signature")
    coff = pe_off + 4
    section_count = struct.unpack_from("<H", image, coff + 2)[0]
    optional_size = struct.unpack_from("<H", image, coff + 16)[0]
    optional = coff + 20
    if struct.unpack_from("<H", image, optional)[0] != 0x10B:
        raise BuildError("expected PE32 optional header")
    image_base = struct.unpack_from("<I", image, optional + 28)[0]
    size_of_headers = struct.unpack_from("<I", image, optional + 60)[0]
    import_rva, import_size = struct.unpack_from("<II", image, optional + 104)
    section_table = optional + optional_size
    sections: list[Section] = []
    for index in range(section_count):
        off = section_table + index * 40
        name = image[off:off + 8].split(b"\0", 1)[0].decode("ascii", "strict")
        virtual_size, rva, raw_size, raw_off = struct.unpack_from("<IIII", image, off + 8)
        sections.append(Section(name, rva, virtual_size, raw_off, raw_size))
    return PEInfo(image_base, size_of_headers, tuple(sections), import_rva, import_size)


def bytes_at(image: bytes, va: int, size: int) -> bytes:
    off = va - VA_TO_FILE_DELTA
    if off < 0 or off + size > len(image):
        raise BuildError(f"VA outside pinned IMAGE: 0x{va:08X}")
    return image[off:off + size]


def require_bytes(image: bytes, va: int, expected_hex: str, label: str) -> None:
    expected = bytes.fromhex(expected_hex)
    actual = bytes_at(image, va, len(expected))
    if actual != expected:
        raise BuildError(
            f"{label} bytes drift at 0x{va:08X}: expected {expected.hex()}, got {actual.hex()}"
        )


def verify_invalid_parameter_import(image: bytes, pe: PEInfo) -> None:
    found: tuple[str, str, int, int, int, int, int] | None = None
    descriptor_rva = pe.import_rva
    while True:
        descriptor_off = pe.rva_to_off(descriptor_rva)
        values = struct.unpack_from("<IIIII", image, descriptor_off)
        if values == (0, 0, 0, 0, 0):
            break
        original_thunk, _timestamp, _forwarder, name_rva, first_thunk = values
        dll_off = pe.rva_to_off(name_rva)
        dll_end = image.find(b"\0", dll_off)
        dll = image[dll_off:dll_end].decode("ascii", "strict")
        lookup_base = original_thunk or first_thunk
        index = 0
        while True:
            lookup_off = pe.rva_to_off(lookup_base + index * 4)
            thunk = struct.unpack_from("<I", image, lookup_off)[0]
            if not thunk:
                break
            iat_rva = first_thunk + index * 4
            iat_va = pe.image_base + iat_rva
            if iat_va == 0x00C3B4C0:
                if thunk & 0x80000000:
                    raise BuildError("invalid-parameter import unexpectedly ordinal")
                hint_name_off = pe.rva_to_off(thunk)
                symbol_off = hint_name_off + 2
                symbol_end = image.find(b"\0", symbol_off)
                symbol = image[symbol_off:symbol_end].decode("ascii", "strict")
                found = (
                    dll,
                    symbol,
                    pe.rva_to_off(iat_rva),
                    descriptor_off,
                    lookup_off,
                    dll_off,
                    symbol_off,
                )
            index += 1
        descriptor_rva += 20
    expected = (
        "MSVCR90.dll",
        "_invalid_parameter_noinfo",
        0x008398C0,
        0x00C112DC,
        0x00C118B4,
        0x00C1647C,
        0x00C15C62,
    )
    if found != expected:
        raise BuildError(f"IAT 0x00C3B4C0 import drift: {found} != {expected}")


def decode_helper_instruction(
    image: bytes, helper: HelperPin, va: int
) -> DecodedInstruction:
    """Decode one instruction from the deliberately tiny pinned helper ISA."""
    if not helper.start_va <= va < helper.end_va:
        raise BuildError(f"CFG address outside helper: {helper.role}:0x{va:08X}")
    remaining = bytes_at(image, va, helper.end_va - va)
    opcode = remaining[0]
    if opcode in (0x74, 0x75):
        if len(remaining) < 2:
            raise BuildError(f"truncated short branch: {helper.role}:0x{va:08X}")
        target = va + 2 + struct.unpack("b", remaining[1:2])[0]
        return DecodedInstruction(va, 2, "conditional_branch", (target, va + 2))
    if remaining.startswith(b"\xFF\xD7"):
        return DecodedInstruction(va, 2, "indirect_call_edi", (va + 2,))
    if opcode == 0xC3:
        return DecodedInstruction(va, 1, "return", ())

    patterns: tuple[tuple[bytes, str, bool], ...] = (
        (bytes.fromhex("8b3dc0b4c300"), "iat_load_edi", False),
        (bytes.fromhex("8da42400000000"), "alignment_nop", False),
        (bytes.fromhex(f"8078{helper.flag_offset:02x}00"), "node_flag_read", False),
        (bytes.fromhex(f"8079{helper.flag_offset:02x}00"), "node_flag_read", False),
        (bytes.fromhex("833e00"), "link_state_read", False),
        (bytes.fromhex("8b4604"), "link_state_read", False),
        (bytes.fromhex("8b4808"), "node_read", False),
        (bytes.fromhex("8b4004"), "node_read", False),
        (bytes.fromhex("8b4e04"), "link_state_read", False),
        (bytes.fromhex("3b4808"), "node_read", False),
        (bytes.fromhex("894e04"), "link_state_write", True),
        (bytes.fromhex("894604"), "link_state_write", True),
        (bytes.fromhex("8b4204"), "node_read", False),
        (bytes.fromhex("8bf1"), "ecx_to_esi", False),
        (bytes.fromhex("8b01"), "node_read", False),
        (bytes.fromhex("8bc8"), "register_move", False),
        (bytes.fromhex("8bd0"), "register_move", False),
        (bytes.fromhex("56"), "push_esi", False),
        (bytes.fromhex("57"), "push_edi", False),
        (bytes.fromhex("5e"), "pop_esi", False),
        (bytes.fromhex("5f"), "pop_edi", False),
    )
    for encoded, kind, memory_write in patterns:
        if remaining.startswith(encoded):
            return DecodedInstruction(
                va, len(encoded), kind, (va + len(encoded),), memory_write
            )
    raise BuildError(
        f"helper CFG decode error: {helper.role}:0x{va:08X}:"
        f"{remaining[:8].hex()}"
    )


def decode_helper_cfg(image: bytes, helper: HelperPin) -> CfgCensus:
    pending = [helper.start_va]
    decoded: dict[int, DecodedInstruction] = {}
    block_starts = {helper.start_va}
    errors: list[str] = []
    while pending:
        va = pending.pop()
        if va in decoded:
            continue
        try:
            instruction = decode_helper_instruction(image, helper, va)
        except BuildError as exc:
            errors.append(str(exc))
            continue
        decoded[va] = instruction
        if instruction.kind == "conditional_branch":
            block_starts.update(instruction.successors)
        for successor in instruction.successors:
            if not helper.start_va <= successor < helper.end_va:
                errors.append(
                    f"CFG successor outside helper: {helper.role}:"
                    f"0x{va:08X}->0x{successor:08X}"
                )
            elif successor not in decoded:
                pending.append(successor)

    coverage = [0] * (helper.end_va - helper.start_va)
    for instruction in decoded.values():
        start = instruction.va - helper.start_va
        for index in range(start, start + instruction.size):
            if not 0 <= index < len(coverage) or coverage[index]:
                errors.append(f"CFG coverage overlap/outside: {helper.role}:0x{instruction.va:08X}")
                break
            coverage[index] = 1
    if not all(coverage):
        missing = [index for index, value in enumerate(coverage) if not value]
        errors.append(f"CFG uncovered bytes: {helper.role}:{missing[:8]}")

    # Reaching-definition proof for the mutable base.  STACK_LOCAL_LINK_STATE must
    # dominate every explicit object write.  POP_RESTORED can reach only an
    # exit and cannot flow into a mutable write.
    incoming: dict[int, str] = {helper.start_va: "ENTRY_ECX_UNCOPIED"}
    flow_pending = [helper.start_va]
    while flow_pending:
        va = flow_pending.pop()
        instruction = decoded.get(va)
        if instruction is None:
            continue
        state = incoming[va]
        if instruction.kind == "ecx_to_esi":
            state = "STACK_LOCAL_LINK_STATE"
        elif instruction.kind == "pop_esi":
            state = "POP_RESTORED"
        if instruction.memory_write and state != "STACK_LOCAL_LINK_STATE":
            errors.append(
                f"mutable write lacks stack-local link-state reaching definition: "
                f"{helper.role}:0x{va:08X}:{state}"
            )
        for successor in instruction.successors:
            previous = incoming.get(successor)
            if previous is None:
                incoming[successor] = state
                flow_pending.append(successor)
            elif previous != state:
                errors.append(
                    f"ESI reaching-definition merge conflict: {helper.role}:"
                    f"0x{successor:08X}:{previous}/{state}"
                )

    if [value.va for value in decoded.values() if value.kind == "ecx_to_esi"] != [
        helper.start_va + 1
    ]:
        errors.append(f"ECX-to-ESI definition census drift: {helper.role}")
    if any(
        value.kind == "return"
        and incoming.get(value.va) != "POP_RESTORED"
        for value in decoded.values()
    ):
        errors.append(f"return reached before ESI restore: {helper.role}")

    # EDI proof for both indirect guard calls.  Compute dominators over the
    # decoded CFG, then a separate reaching-definition fixed point.  The IAT
    # load must dominate each call and be its singleton local EDI definition.
    predecessors: dict[int, set[int]] = {va: set() for va in decoded}
    for instruction in decoded.values():
        for successor in instruction.successors:
            if successor in predecessors:
                predecessors[successor].add(instruction.va)
    all_nodes = set(decoded)
    dominators: dict[int, set[int]] = {
        va: ({helper.start_va} if va == helper.start_va else set(all_nodes))
        for va in decoded
    }
    changed = True
    while changed:
        changed = False
        for va in sorted(decoded):
            if va == helper.start_va:
                continue
            preds = predecessors[va]
            incoming_dom = set.intersection(*(dominators[pred] for pred in preds))
            updated = {va} | incoming_dom
            if updated != dominators[va]:
                dominators[va] = updated
                changed = True

    edi_in: dict[int, frozenset[int]] = {
        va: frozenset() for va in decoded
    }
    edi_out: dict[int, frozenset[int]] = {
        va: frozenset() for va in decoded
    }
    changed = True
    while changed:
        changed = False
        for va in sorted(decoded):
            incoming_defs = frozenset(
                definition
                for predecessor in predecessors[va]
                for definition in edi_out[predecessor]
            )
            if va == helper.start_va:
                incoming_defs = frozenset()
            instruction = decoded[va]
            if instruction.kind in {"iat_load_edi", "pop_edi"}:
                outgoing_defs = frozenset({va})
            else:
                outgoing_defs = incoming_defs
            if incoming_defs != edi_in[va] or outgoing_defs != edi_out[va]:
                edi_in[va] = incoming_defs
                edi_out[va] = outgoing_defs
                changed = True

    iat_loads = [value.va for value in decoded.values() if value.kind == "iat_load_edi"]
    guard_calls = [
        value.va for value in decoded.values() if value.kind == "indirect_call_edi"
    ]
    if iat_loads != [helper.import_load_va]:
        errors.append(f"EDI IAT-load census drift: {helper.role}:{iat_loads}")
    dominated_count = sum(
        helper.import_load_va in dominators[site] for site in guard_calls
    )
    singleton_count = sum(
        edi_in[site] == frozenset({helper.import_load_va}) for site in guard_calls
    )
    if dominated_count != 2 or singleton_count != 2:
        errors.append(
            f"EDI guard-call dominance/reaching-def failure: {helper.role}:"
            f"dominated={dominated_count}:singleton={singleton_count}"
        )

    census = CfgCensus(
        instruction_nodes=len(decoded),
        basic_blocks=len(block_starts),
        decode_errors=len(errors),
        direct_calls=sum(value.kind == "direct_call" for value in decoded.values()),
        indirect_calls=sum(value.kind == "indirect_call_edi" for value in decoded.values()),
        guard_calls_dominated=dominated_count,
        guard_calls_singleton_edi=singleton_count,
        memory_writes=tuple(
            sorted(value.va for value in decoded.values() if value.memory_write)
        ),
        covered_bytes=sum(coverage),
    )
    if errors:
        raise BuildError(" | ".join(errors))
    expected = CfgCensus(
        instruction_nodes=44,
        basic_blocks=13,
        decode_errors=0,
        direct_calls=0,
        indirect_calls=2,
        guard_calls_dominated=2,
        guard_calls_singleton_edi=2,
        memory_writes=helper.writes,
        covered_bytes=108,
    )
    if census != expected:
        raise BuildError(f"helper CFG census drift: {helper.role}: {census} != {expected}")
    return census


def verify_helpers(image: bytes, pe: PEInfo) -> dict[int, CfgCensus]:
    if sha256_bytes(image) != IMAGE_SHA256:
        raise BuildError("pinned GameClient.local.bin SHA-256 mismatch")
    verify_invalid_parameter_import(image, pe)
    cfg_census: dict[int, CfgCensus] = {}
    for helper in HELPERS:
        if helper.start_va - VA_TO_FILE_DELTA != helper.file_off:
            raise BuildError(f"helper VA/file mapping drift: {helper.role}")
        body = image[helper.file_off:helper.file_off + helper.end_va - helper.start_va]
        if len(body) != 108 or sha256_bytes(body) != helper.sha256:
            raise BuildError(f"helper span drift: {helper.role}")
        require_bytes(image, helper.import_load_va, "8b3dc0b4c300", f"{helper.role}:IAT load")
        for call in helper.guard_calls:
            require_bytes(image, call, "ffd7", f"{helper.role}:guard call")
        for write in helper.writes:
            if bytes_at(image, write, 3) not in (bytes.fromhex("894e04"), bytes.fromhex("894604")):
                raise BuildError(f"helper write drift: {helper.role}:0x{write:08X}")
        for ret in helper.returns:
            require_bytes(image, ret, "c3", f"{helper.role}:return")
        if b"\xE8" in body:
            raise BuildError(f"unexpected rel32-call opcode byte in helper: {helper.role}")
        if body.count(bytes.fromhex("ffd7")) != 2:
            raise BuildError(f"guard-call census drift: {helper.role}")
        flags = {body[index] for index in MASK_OFFSETS}
        if flags != {helper.flag_offset}:
            raise BuildError(f"node-flag displacement drift: {helper.role}: {flags}")
        cfg_census[helper.start_va] = decode_helper_cfg(image, helper)

        # Executed dataflow boundary: entry ECX is copied once to ESI; no
        # instruction subsequently defines ESI; every non-stack memory write
        # is [ESI+4].  The body reads no caller-stack formal and every return is
        # plain C3, so no stream formal is received by the helper.
        require_bytes(image, helper.start_va + 1, "8bf1", f"{helper.role}:ECX-to-ESI")
        if any(
            bytes_at(image, site, 3) not in (bytes.fromhex("894e04"), bytes.fromhex("894604"))
            for site in cfg_census[helper.start_va].memory_writes
        ):
            raise BuildError(f"non-link-state mutable write: {helper.role}")

    for span in CALLER_SPANS:
        if span.start_va - VA_TO_FILE_DELTA != span.file_off:
            raise BuildError(f"caller VA/file mapping drift: {span.role}")
        body = image[span.file_off:span.file_off + span.end_va - span.start_va]
        if sha256_bytes(body) != span.sha256:
            raise BuildError(f"caller span drift: {span.role}")

    for caller in CALLERS:
        require_bytes(image, caller.site_va - 4, caller.lea_hex, "stack-local ECX definition")
        if not caller.lea_hex.startswith("8d4c24"):
            raise BuildError(f"non-stack-local caller pin: 0x{caller.site_va:08X}")
        call = bytes_at(image, caller.site_va, 5)
        if call[0] != 0xE8:
            raise BuildError(f"missing direct helper call: 0x{caller.site_va:08X}")
        target = caller.site_va + 5 + struct.unpack_from("<i", call, 1)[0]
        if target != TAG_TARGET[caller.tag]:
            raise BuildError(f"helper target drift: 0x{caller.site_va:08X} -> 0x{target:08X}")
    return cfg_census


def verify_masked_family(image: bytes, pe: PEInfo) -> tuple[tuple[int, int], ...]:
    text_sections = [section for section in pe.sections if section.name == ".text"]
    if len(text_sections) != 1:
        raise BuildError(f".text section census drift: {len(text_sections)}")
    text = text_sections[0]
    if (
        text.rva,
        text.virtual_size,
        text.raw_off,
        text.raw_size,
    ) != (0x1000, 0x838A2C, 0x400, 0x838C00):
        raise BuildError(".text boundary drift")
    template = bytes_at(image, 0x00B0BF70, 108)
    prefix = template[:MASK_OFFSETS[0]]
    raw = image[text.raw_off:text.raw_off + text.raw_size]
    hits: list[tuple[int, int]] = []
    cursor = 0
    while True:
        index = raw.find(prefix, cursor)
        if index < 0:
            break
        candidate = raw[index:index + len(template)]
        if len(candidate) == len(template) and all(
            candidate[offset] == template[offset]
            for offset in range(len(template))
            if offset not in MASK_OFFSETS
        ):
            masked_values = {candidate[offset] for offset in MASK_OFFSETS}
            if len(masked_values) != 1:
                raise BuildError(f"nonuniform masked family member at raw 0x{text.raw_off + index:08X}")
            hits.append((pe.image_base + text.rva + index, masked_values.pop()))
        cursor = index + 1
    actual = tuple(hits)
    if actual != EXPECTED_FAMILY:
        raise BuildError(f"masked .text family census drift: {actual}")
    return actual


def find_all(data: bytes, needle: bytes) -> list[int]:
    positions: list[int] = []
    cursor = 0
    while True:
        index = data.find(needle, cursor)
        if index < 0:
            break
        positions.append(index)
        cursor = index + 1
    return positions


def verify_wire_reference_census(image: bytes, pe: PEInfo) -> dict[int, int]:
    helper_ranges = tuple((helper.file_off, helper.file_off + 108) for helper in HELPERS)
    counts: dict[int, int] = {}
    e8_sites = find_all(image[:-4], b"\xE8")
    for target, expected_count in WIRE_PRIMITIVE_COUNTS.items():
        raw_absolute = find_all(image, struct.pack("<I", target))
        if raw_absolute:
            raise BuildError(f"whole-image absolute wire-reference census drift: 0x{target:08X}")
        rel32_hits: list[int] = []
        for raw_off in e8_sites:
            site_va = pe.raw_to_va(raw_off)
            if site_va is None:
                continue
            displacement = struct.unpack_from("<i", image, raw_off + 1)[0]
            if site_va + 5 + displacement == target:
                rel32_hits.append(raw_off)
        if len(rel32_hits) != expected_count:
            raise BuildError(
                f"whole-image rel32 wire-reference census drift for 0x{target:08X}: "
                f"{len(rel32_hits)} != {expected_count}"
            )
        if any(start <= raw_off < end for raw_off in rel32_hits for start, end in helper_ranges):
            raise BuildError(f"wire primitive rel32 pattern intersects helper: 0x{target:08X}")
        counts[target] = len(rel32_hits)
    return counts


def select_rows(
    base_fields: Sequence[str],
    base_rows: Sequence[tuple[int, dict[str, str]]],
    p1_rows: Sequence[tuple[int, dict[str, str]]],
) -> list[tuple[int, dict[str, str], int]]:
    object_alias_messages = {
        row["message"]
        for _line, row in p1_rows
        if row["priority"] == "1"
        and row["effective_structural_status"] == "OPEN"
        and row["primary_blocker_group"] == PRIMARY_GROUP
    }
    if len(object_alias_messages) != 10:
        raise BuildError(f"P1 object-alias group census drift: {len(object_alias_messages)}")

    selected: list[tuple[int, dict[str, str], int]] = []
    for line, row in base_rows:
        tag = row.get("tag", "")
        if tag not in TAG_TARGET or row["message"] not in object_alias_messages:
            continue
        matches = TAG_REGEX[tag].findall(row["gate_condition"])
        if not matches:
            raise BuildError(f"missing helper callsite in selected tag at line {line}")
        site = int(matches[-1], 16)
        if site in {caller.site_va for caller in CALLERS}:
            selected.append((line, row, site))

    actual = tuple(
        (
            line,
            row["message"],
            row["direction(W/R)"],
            row["order"],
            row["tag"],
            site,
        )
        for line, row, site in selected
    )
    if actual != EXPECTED_ROWS:
        raise BuildError(f"exact effective V1 row census drift: {actual}")
    if Counter(row["tag"] for _line, row, _site in selected) != Counter(
        {CHAIN_TAG: 26, POINTER_TAG: 14}
    ):
        raise BuildError("helper-tag row census drift")
    if Counter(row["direction(W/R)"] for _line, row, _site in selected) != Counter(
        {"W": 20, "R": 20}
    ):
        raise BuildError("direction census drift")
    if any(row["source"] != "IMAGE" for _line, row, _site in selected):
        raise BuildError("selected row is not IMAGE")
    if any(
        row["field_offset"]
        not in {
            "UNKNOWN(mutable_chain_target_object_alias_unproved)",
            "UNKNOWN(mutable_pointer_slot_traversal_alias_unproved)",
        }
        or row["len"] != "N/A"
        for _line, row, _site in selected
    ):
        raise BuildError("selected blocker row contract drift")
    if len({canonical_row_key(base_fields, row) for _line, row, _site in selected}) != 40:
        raise BuildError("selected canonical base row is duplicated")

    selected_by_site: dict[int, list[dict[str, str]]] = defaultdict(list)
    for _line, row, site in selected:
        selected_by_site[site].append(row)
    for caller in CALLERS:
        rows = selected_by_site.get(caller.site_va, [])
        if len(rows) != caller.row_count:
            raise BuildError(f"selected row count drift at 0x{caller.site_va:08X}")
        if tuple(sorted({row["message"] for row in rows})) != tuple(sorted(caller.messages)):
            raise BuildError(f"selected message set drift at 0x{caller.site_va:08X}")
        for row in rows:
            if row["file_off_claim"] != f"0x{caller.site_va - VA_TO_FILE_DELTA:08X}":
                raise BuildError(f"selected file-offset claim drift at 0x{caller.site_va:08X}")
            span_matches = [
                span
                for span in CALLER_SPANS
                if row["span_start"] == f"0x{span.start_va:08X}"
                and row["span_end"] == f"0x{span.end_va:08X}"
                and row["span_sha256"] == span.sha256
            ]
            if len(span_matches) != 1:
                raise BuildError(f"selected caller span contract drift at 0x{caller.site_va:08X}")
    return selected


def build_delta(
    base_fields: Sequence[str],
    selected: Sequence[tuple[int, dict[str, str], int]],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for line, row, site in selected:
        base_key = canonical_row_key(base_fields, row)
        values = {
            "action": "REMOVE_NONWIRE_ROW",
            "change_type": "NONWIRE_STACK_LOCAL_LINK_STATE_HELPER",
            "base_file": A2_NAME,
            "base_line": str(line),
            "base_row_key": base_key,
            "base_delta_key": "N/A",
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
            "resolution": (
                "STACK_LOCAL_LINK_STATE_RECEIVER;IMMEDIATE_ECX_LEA;"
                "FIXED_GUARD_IMPORT;NO_WIRE_PRIMITIVE_REFERENCE"
            ),
            "evidence_ticket": EVIDENCE_TICKET,
            "evidence_span_start": row["span_start"],
            "evidence_span_end": row["span_end"],
            "evidence_span_sha256": row["span_sha256"],
            "evidence_file_off": f"0x{site - VA_TO_FILE_DELTA:08X}",
            "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(
            ("A2", values["action"], values["base_file"], values["base_line"], base_key)
        )
        output.append(values)
    output.sort(key=lambda row: int(row["base_line"]))
    if len(output) != 40:
        raise BuildError(f"expected 40 removal directives, got {len(output)}")
    if len({row["delta_key"] for row in output}) != 40:
        raise BuildError("duplicate delta_key")
    identities = {(row["base_file"], row["base_line"], row["base_row_key"]) for row in output}
    if len(identities) != 40:
        raise BuildError("duplicate base-row target")
    if any(row["source"] != "IMAGE" for row in output):
        raise BuildError("mixed evidence source")
    if any(
        "UNCHANGED" in "\t".join(row.values()) or "COPIED" in "\t".join(row.values())
        for row in output
    ):
        raise BuildError("unchanged/copied output is forbidden")
    return output


def verify_cross_overlay(external: Path, delta: Sequence[Mapping[str, str]]) -> None:
    wanted = {(row["base_file"], row["base_line"], row["base_row_key"]) for row in delta}
    wanted_keys = {row["delta_key"] for row in delta}
    callsite_tokens = {
        token
        for caller in CALLERS
        for token in (
            f"0x{caller.site_va:08X}",
            f"0x{caller.site_va - VA_TO_FILE_DELTA:08X}",
        )
    }
    overlaps: list[str] = []
    target_overlaps: list[str] = []
    delta_key_overlaps: list[str] = []
    for path in sorted(external.glob("*DELTA.tsv")):
        if path.name == OUTPUT_NAME:
            continue
        fields, rows = read_tsv_with_lines(path)
        for line, row in rows:
            if {"base_file", "base_line", "base_row_key"}.issubset(fields):
                identity = (row["base_file"], row["base_line"], row["base_row_key"])
                if identity in wanted:
                    overlaps.append(f"{path.name}:{line}")
            if "base_row_number" in fields and row["base_row_number"] in {
                value[1] for value in wanted if value[0] == A2_NAME
            }:
                overlaps.append(f"{path.name}:{line}:base_row_number")
            if row.get("delta_key") in wanted_keys:
                delta_key_overlaps.append(f"{path.name}:{line}")
            found_tokens = {
                token
                for token in callsite_tokens
                if any(token in value for value in row.values())
            }
            if found_tokens:
                target_overlaps.append(f"{path.name}:{line}:{sorted(found_tokens)}")
    if overlaps:
        raise BuildError("cross-overlay base-row overlap: " + " | ".join(overlaps))
    if delta_key_overlaps:
        raise BuildError("cross-overlay delta-key overlap: " + " | ".join(delta_key_overlaps))
    if target_overlaps:
        raise BuildError("cross-overlay physical-target overlap: " + " | ".join(target_overlaps))


def effective_a2_residuals(
    external: Path,
    base_fields: Sequence[str],
    base_rows: Sequence[tuple[int, dict[str, str]]],
    selected: Sequence[tuple[int, dict[str, str], int]],
) -> tuple[list[tuple[str, int, int]], tuple[str, ...]]:
    """Rebuild effective A2 through every prior overlay, then apply this removal.

    Only unresolved-row counts are returned.  Exact OPEN metadata belongs to
    the final V3 status builder and is deliberately not duplicated here.
    """
    base_by_line: dict[int, str] = {}
    effective: dict[str, dict[str, str]] = {}
    for line, row in base_rows:
        key = canonical_row_key(base_fields, row)
        base_by_line[line] = key
        effective[key] = {
            "message": row["message"],
            "direction(W/R)": row["direction(W/R)"],
            "tag": row["tag"],
            "field_offset": row["field_offset"],
            "len": row["len"],
            "source": row["source"],
        }
    additions: dict[str, dict[str, str]] = {}
    removed_addition_keys: set[str] = set()
    applied_prior: set[str] = set()

    for path in sorted(external.glob("*DELTA.tsv")):
        if path.name == OUTPUT_NAME:
            continue
        fields, rows = read_tsv_with_lines(path)
        if path.name == "PF_A2_STRING_WIRE_TAG_DELTA.tsv":
            for _line, row in rows:
                if row["delta_action"] != "CHANGED" or row["source"] != "IMAGE":
                    raise BuildError("string A2 overlay action/source drift")
                base_line = int(row["base_row_number"])
                key = base_by_line.get(base_line)
                state = effective.get(key or "")
                if state is None:
                    raise BuildError(f"string A2 overlay base drift at line {base_line}")
                state["tag"] = row["corrected_tag"]
                state["len"] = row["corrected_full_wire_len"]
                applied_prior.add(path.name)
            continue

        for _line, row in rows:
            action = row.get("action", "")
            base_file = row.get("base_file", "")
            if path.name == "PF_A2_SERIALIZER_SLOT34_DELTA.tsv" and action in {
                "ADD_CORRECTED_SLOT34_ROW",
                "ADD_ANALYSIS_BLOCKER_ROW",
            }:
                if row["source"] != "IMAGE" or not row["delta_key"]:
                    raise BuildError("slot34 A2 addition source/key drift")
                additions[row["delta_key"]] = {
                    "message": row["message"],
                    "direction(W/R)": row["direction(W/R)"],
                    "tag": row["new_tag"],
                    "field_offset": row["new_field_offset"],
                    "len": row["new_len"],
                    "source": row["source"],
                }
                applied_prior.add(path.name)
                continue
            if (
                base_file == "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
                and action == "REMOVE_OVERLAY_NONWIRE_ROW"
            ):
                removed_addition_keys.add(row["base_delta_key"])
                applied_prior.add(path.name)
                continue
            if base_file != A2_NAME:
                continue
            key = row.get("base_row_key", "")
            base_line = int(row.get("base_line", "0"))
            if base_by_line.get(base_line) != key:
                raise BuildError(f"prior A2 overlay base line/key drift: {path.name}:{base_line}")
            if key not in effective:
                raise BuildError(f"prior A2 overlay overlaps a removed base: {path.name}:{base_line}")
            if row.get("source") != "IMAGE":
                raise BuildError(f"prior A2 overlay mixed source: {path.name}:{base_line}")
            if action in {"REMOVE_NONWIRE_ROW", "REMOVE_WRONG_SLOT_ROW"}:
                del effective[key]
            elif action == "CHANGED":
                state = effective[key]
                state["tag"] = row["new_tag"]
                state["field_offset"] = row["new_field_offset"]
                state["len"] = row["new_len"]
            else:
                raise BuildError(f"unsupported prior A2 action: {path.name}:{action}")
            applied_prior.add(path.name)

    for key in removed_addition_keys:
        if key not in additions:
            raise BuildError(f"prior overlay removal names unknown slot34 addition: {key}")
        del additions[key]

    for _line, row, _site in selected:
        key = canonical_row_key(base_fields, row)
        if key not in effective:
            raise BuildError("selected row was not effective before this overlay")
        del effective[key]
    effective.update({f"SLOT34:{key}": value for key, value in additions.items()})

    affected_messages = sorted({row["message"] for _line, row, _site in selected})
    residuals: list[tuple[str, int, int]] = []
    for message in affected_messages:
        unresolved = [
            row
            for row in effective.values()
            if row["message"] == message
            and row["source"] == "IMAGE"
            and row["field_offset"].startswith("UNKNOWN(")
        ]
        write_count = sum(row["direction(W/R)"] == "W" for row in unresolved)
        read_count = sum(row["direction(W/R)"] == "R" for row in unresolved)
        if write_count + read_count == 0:
            raise BuildError(f"A2 transition found for {message}; Priority delta/review required")
        residuals.append((message, write_count, read_count))
    if len(residuals) != 8:
        raise BuildError(f"affected message census drift: {len(residuals)}")
    return residuals, tuple(sorted(applied_prior))


def report_text(
    delta: Sequence[Mapping[str, str]],
    cfg_census: Mapping[int, CfgCensus],
    family: Sequence[tuple[int, int]],
    wire_counts: Mapping[int, int],
    residuals: Sequence[tuple[str, int, int]],
    applied_prior: Sequence[str],
) -> str:
    by_tag = Counter(row["old_tag"] for row in delta)
    lines = [
        "# PF IMAGE closure: stack-local link-state helpers",
        "",
        "[MEASURED][IMAGE] Additive removal overlay only. Frozen V1 and every prior overlay remain untouched.",
        "",
        "## Outcome",
        "",
        "- Removed **40 unique effective V1 A2 analysis rows**: 26 for `0x00B0BF70` and 14 for `0x0046D2B0`.",
        "- The selected cluster has **12 exact physical callsites** (7 + 5), **20 W / 20 R rows**, and **8 unique Priority-1 messages**.",
        "- Duplicate accounting: unchanged/copied rows 0; duplicate base rows 0; duplicate delta keys 0; cross-overlay base/target/delta-key overlaps 0.",
        "- No Priority TSV is emitted. A fresh effective-A2 reconstruction after all prior field overlays finds unresolved rows remaining for every affected message, so this overlay creates no closure transition.",
        "- Scope is intentionally narrower than every row bearing the same tags. Selection requires current V2 Priority-1 OPEN status, primary object/mutable-alias blocker group, an exact pinned callsite, and immediate `lea ecx,[esp+disp8]` immediately before the helper call.",
        "",
        "## Helper proof",
        "",
        "| helper | span | bytes | file offset | SHA-256 | node flag | state writes | source |",
        "|---|---|---:|---:|---|---:|---|---|",
    ]
    for helper in HELPERS:
        writes = ", ".join(f"0x{site:08X}" for site in helper.writes)
        lines.append(
            f"| `{helper.role}` | `0x{helper.start_va:08X}-0x{helper.end_va:08X}` | 108 | "
            f"`0x{helper.file_off:08X}` | `{helper.sha256}` | `+0x{helper.flag_offset:02X}` | `{writes}` | IMAGE |"
        )
    lines += [
        "",
        "The generator recursively decodes the reachable CFG rather than relying on printed byte pins:",
        "",
        "| helper | instruction nodes | basic blocks | covered bytes | decode errors | direct calls | indirect calls | EDI-dominated guards | singleton EDI definitions | mutable writes |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for helper in HELPERS:
        census = cfg_census[helper.start_va]
        lines.append(
            f"| `0x{helper.start_va:08X}` | {census.instruction_nodes} | "
            f"{census.basic_blocks} | {census.covered_bytes} | {census.decode_errors} | "
            f"{census.direct_calls} | {census.indirect_calls} | "
            f"{census.guard_calls_dominated} | {census.guard_calls_singleton_edi} | "
            f"{len(census.memory_writes)} |"
        )
    lines += [
        "",
        "Each complete body has three returns, traverses node links, and writes only the stack-local link-state object's `+0x04` state. Executed dominator and reaching-definition analyses prove that the single EDI load from `[0x00C3B4C0]` dominates both indirect guard calls and is the singleton local EDI definition reaching each call. The pinned PE import table resolves that slot to `MSVCR90.dll!_invalid_parameter_noinfo`.",
        "",
        "Those guard calls are used only as part of the helper proof. This overlay does **not** globally remove any invalid-parameter row.",
        "",
        "## Exact affected callsites",
        "",
        "| target | callsite | file offset | immediate ECX definition | V1 rows | messages | source |",
        "|---:|---:|---:|---|---:|---|---|",
    ]
    for caller in CALLERS:
        target = TAG_TARGET[caller.tag]
        messages = ", ".join(f"`{message}`" for message in caller.messages)
        disp = int(caller.lea_hex[-2:], 16)
        lines.append(
            f"| `0x{target:08X}` | `0x{caller.site_va:08X}` | "
            f"`0x{caller.site_va - VA_TO_FILE_DELTA:08X}` | `lea ecx,[esp+0x{disp:02X}]` | "
            f"{caller.row_count} | {messages} | IMAGE |"
        )
    lines += [
        "",
        "Because the LEA is the instruction immediately before each direct E8 call, there is no intervening ECX clobber. Executed helper dataflow copies entry ECX to ESI once; that definition dominates all three mutable writes, each write uses `[ESI+0x04]`, and ESI is restored by `pop` only on exit paths. The body reads no caller-stack formal and accepts no stack argument (plain `ret` at all exits). Therefore the mutable base is the pinned caller-stack link-state object; the stream formal is not received or used by either helper.",
        "",
        "Callsite `0x0049FAD4` is deliberately excluded. Although it also has an immediate `lea ecx,[esp+0x1C]`, this artifact does not contain a complete entry-relative stack-depth/call-cleanup proof for that site. Its six V1 rows remain untouched.",
        "",
        "## Whole-.text normalized family census",
        "",
        "The 108-byte body was scanned across the complete pinned `.text` raw range (`0x00000400+0x00838C00`). Only six node-flag displacement bytes were masked (body offsets 22, 36, 44, 54, 69, 98). The exact normalized family contains **24** members:",
        "",
        ", ".join(f"`0x{va:08X}(+0x{flag:02X})`" for va, flag in family) + ".",
        "",
        "This family census is a structural identity check only. It does not authorize removals at the other 22 members or at unselected callers.",
        "",
        "## Whole-image wire-reference census",
        "",
        "A raw whole-image byte census (not a linear-disassembler negative) scanned every E8 byte as a mapped rel32 candidate and every little-endian absolute VA pattern:",
        "",
        "| primitive | whole-image rel32 byte candidates | absolute-VA dword hits | hits inside either helper |",
        "|---:|---:|---:|---:|",
        f"| `0x0089A600` | {wire_counts[0x0089A600]} | 0 | 0 |",
        f"| `0x0089A640` | {wire_counts[0x0089A640]} | 0 | 0 |",
        "",
        "The primitives are abundant elsewhere in the same pinned image, but neither their rel32 byte patterns nor their absolute VAs occur in either helper. The only indirect-call target inside each helper is the fixed guard import proved above.",
        "",
        "## Effective A2 residual check after prior overlays",
        "",
        "The reconstruction applied these prior A2 overlays before applying the 40 removals in this file: "
        + ", ".join(f"`{name}`" for name in applied_prior)
        + ".",
        "",
        "| message | unresolved W rows remaining | unresolved R rows remaining | closure transition from this overlay |",
        "|---|---:|---:|---|",
    ]
    for message, write_count, read_count in residuals:
        lines.append(f"| `{message}` | {write_count} | {read_count} | NO |")
    lines += [
        "",
        "Exact effective blocker strings and OPEN metadata are not duplicated here; `pf_build_v3_effective_status.py` recomputes them from the final effective A2 set. If a future rebuild finds zero unresolved rows for any affected message, this generator stops and requires a reviewed status transition instead of emitting one silently.",
        "",
        "## Duplicate/layer accounting",
        "",
        "| action | rows | W | R | unchanged copied | cross-overlay overlap | source |",
        "|---|---:|---:|---:|---:|---:|---|",
        f"| remove `{CHAIN_TAG}` at selected `0x00B0BF70` callers | {by_tag[CHAIN_TAG]} | 13 | 13 | 0 | 0 | IMAGE |",
        f"| remove `{POINTER_TAG}` at selected `0x0046D2B0` callers | {by_tag[POINTER_TAG]} | 7 | 7 | 0 | 0 | IMAGE |",
        "",
        "## Nonclaims and stop rule",
        "",
        "- No node, field, gameplay, capture, runtime, or server semantic is assigned. An iterator interpretation is PROPOSED only and is not used as evidence or as a classification claim.",
        "- No row outside the exact 40 V1 base identities is removed, including `0x0049FAD4`, rows with the same tag in other priority/blocker groups, and slot-0x34 additions.",
        "- Resume this overlay only if an exact selected V1 base row changes or a later overlay targets one of the same base identities/callsites.",
        "",
    ]
    return "\n".join(lines)


def build(external: Path) -> tuple[str, str]:
    image_path = external.parent.parent / "GameClient" / "GameClient.local.bin"
    require_hash(image_path, IMAGE_SHA256, "IMAGE")
    require_hash(external / A2_NAME, A2_SHA256, "V1 A2")
    require_hash(external / P1_OPEN_NAME, P1_OPEN_SHA256, "V2 P1 OPEN")
    image = image_path.read_bytes()
    pe = parse_pe(image)
    cfg_census = verify_helpers(image, pe)
    family = verify_masked_family(image, pe)
    wire_counts = verify_wire_reference_census(image, pe)
    base_fields, base_rows = read_tsv_with_lines(external / A2_NAME)
    _p1_fields, p1_rows = read_tsv_with_lines(external / P1_OPEN_NAME)
    selected = select_rows(base_fields, base_rows, p1_rows)
    delta = build_delta(base_fields, selected)
    verify_cross_overlay(external, delta)
    residuals, applied_prior = effective_a2_residuals(
        external, base_fields, base_rows, selected
    )
    return tsv_text(A2_DELTA_COLUMNS, delta), report_text(
        delta, cfg_census, family, wire_counts, residuals, applied_prior
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify existing outputs byte-for-byte")
    parser.add_argument("--external", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    external = args.external.resolve()
    delta, report = build(external)
    outputs = {external / OUTPUT_NAME: delta, external / REPORT_NAME: report}
    if args.check:
        for path, expected in outputs.items():
            if not path.exists():
                raise BuildError(f"missing output: {path.name}")
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                raise BuildError(f"output drift: {path.name}")
        print(
            "PASS link-state helpers: 40 unique removals; 12 stack-local callsites; "
            "masked family 24; cross-overlay overlap 0; Priority delta 0"
        )
        return 0
    publish_outputs(outputs)
    print(
        "WROTE link-state helpers: 40 unique removals; 12 stack-local callsites; "
        "masked family 24; cross-overlay overlap 0; Priority delta 0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
