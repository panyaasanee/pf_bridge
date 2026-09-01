#!/usr/bin/env python3
"""Build the IMAGE-only 0x00652A30 non-wire removal overlay.

The frozen V1 A2 table and the additive slot-0x34 correction are inputs.  The
script never changes them.  It verifies the complete helper body, its fixed
support calls, every in-scope caller span and the exact caller reaching
definitions before emitting base-row-keyed removal directives.
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
SLOT34_A2_SHA256 = "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334"
PRIORITY_SHA256 = "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"
SLOT34_PRIORITY_SHA256 = "00ef0f3cb632b40ba168ce79bbd656fc7a6936a55f3b3e185c6e63b32c39ec5d"

A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
SLOT34_A2_NAME = "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
PRIORITY_NAME = "PF_PROTOCOL_PRIORITY.tsv"
SLOT34_PRIORITY_NAME = "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv"
OUTPUT_NAME = "PF_TARGET_652A30_A2_DELTA.tsv"
REPORT_NAME = "PF_TARGET_652A30_NONWIRE.md"
EVIDENCE_TICKET = "STATIC-TARGET-652A30"
TARGET_TAG = "CALL_UNCLASSIFIED:0x00652A30"
VA_TO_FILE_DELTA = 0x00400C00

P1_MESSAGES = (
    "ServerAddedInfoVital",
    "GSSS_GuildDataVitalRes",
    "GSSS_GSInitialGuildDataVital",
    "ItemMallUpdatePersonalDataVital",
    "ItemMallIMSDataRes",
    "CHitParadeVital",
)
SLOT34_MESSAGES = ("CCooldownAttr", "DailyActivityState")
ALL_MESSAGES = P1_MESSAGES + SLOT34_MESSAGES


@dataclass(frozen=True)
class SpanPin:
    role: str
    start_va: int
    end_va: int
    file_off: int
    sha256: str


SPAN_PINS = (
    SpanPin("ordered_tree_lookup_insert", 0x00652A30, 0x00652B1F, 0x00251E30, "fc953d5b6890f65b63eaa8c90dd5cf8afb97fbbcc787da643fd58d14482675f8"),
    SpanPin("ordered_tree_insert_rebalance", 0x00652550, 0x0065292F, 0x00251950, "868ba1b4f464944d421e4f1f19e1893641874ce64a67221c247e2fba78c75a03"),
    SpanPin("ordered_tree_iterator_advance", 0x00767170, 0x007671F4, 0x00366570, "cf948a67e84ac3e0a9d0db0909efebefb9a7364c7550adb552c9b23353e48de8"),
    SpanPin("ServerAddedInfoVital_serializer", 0x005EBCF0, 0x005EBE33, 0x001EB0F0, "f3608dd2456f8577a585e35164b6990d465abb1ffd73697ff7f103e4cbd34960"),
    SpanPin("guild_shared_serializer", 0x0066A320, 0x0066A708, 0x00269720, "382d44de2e5bcdcfcba329d8a9a8a720f07276d1f49b819a7ce228fd99ca1abd"),
    SpanPin("ItemMallUpdatePersonalDataVital_serializer", 0x006B0D20, 0x006B0FBC, 0x002B0120, "142b0ecac21efcf62367aec12d0dfab558c0bdd66428b8f2922a6b89367cd664"),
    SpanPin("ItemMallIMSDataRes_serializer", 0x006BBFD0, 0x006BC31C, 0x002BB3D0, "50847a94f2ee128fac0e442bfaeea35688fd77c8d3b72ea5e80793a3c23475db"),
    SpanPin("CHitParadeVital_serializer", 0x00716220, 0x007163F8, 0x00315620, "7cbbd7d8212c9102e8e026592559fb33c4322e8ff214b0f0a5ec906e39feac5c"),
    SpanPin("CCooldownAttr_serializer", 0x006C9DC0, 0x006C9F4A, 0x002C91C0, "4d40cadb26437db551ef308732c53a30eddc7429174ee53cb966cbf474a5bd0d"),
    SpanPin("DailyActivityState_serializer", 0x0069CB20, 0x0069CC63, 0x0029BF20, "28f27bb1158748030e9876e896e729d3b6fe1d18a988f7e90ed1d7b0745e31ca"),
)


@dataclass(frozen=True)
class CallerPin:
    role: str
    messages: tuple[str, ...]
    call_va: int
    call_file_off: int
    member: str
    stream_formal: str
    mode_formal: str
    byte_pins: tuple[tuple[int, str, str], ...]


CALLER_PINS = (
    CallerPin(
        "ServerAddedInfoVital_serializer", ("ServerAddedInfoVital",),
        0x005EBE1C, 0x001EB21C, "this+0x14", "entry+0x4", "entry+0x8",
        (
            (0x005EBCFC, "8bd9", "this_to_ebx"),
            (0x005EBD07, "0f84a8000000", "zero_mode_to_read_branch"),
            (0x005EBDB5, "8b7c243c", "stream_formal_to_edi"),
            (0x005EBDD7, "83c314", "tree_member_this_plus_14"),
            (0x005EBE16, "8bcb", "tree_member_to_target_ecx"),
            (0x005EBE1C, "e80f6c0600", "direct_target_call"),
        ),
    ),
    CallerPin(
        "guild_shared_serializer", ("GSSS_GuildDataVitalRes", "GSSS_GSInitialGuildDataVital"),
        0x0066A6F1, 0x00269AF1, "this+0x40", "entry+0x4", "entry+0x8",
        (
            (0x0066A32C, "8bf1", "this_to_esi"),
            (0x0066A32E, "0f84f6010000", "zero_mode_to_read_branch"),
            (0x0066A530, "8d5e40", "tree_member_this_plus_40"),
            (0x0066A53E, "8b7c2434", "stream_formal_to_edi"),
            (0x0066A6EB, "8bcb", "tree_member_to_target_ecx"),
            (0x0066A6F1, "e83a83feff", "direct_target_call"),
        ),
    ),
    CallerPin(
        "ItemMallUpdatePersonalDataVital_serializer", ("ItemMallUpdatePersonalDataVital",),
        0x006B0F27, 0x002B0327, "this+0x1C", "entry+0x4", "entry+0x8",
        (
            (0x006B0D2C, "8bf9", "this_to_edi"),
            (0x006B0D30, "0f8421010000", "zero_mode_to_read_branch"),
            (0x006B0E57, "8b742434", "stream_formal_to_esi"),
            (0x006B0EDE, "83c71c", "tree_member_this_plus_1c"),
            (0x006B0F20, "8bcf", "tree_member_to_target_ecx"),
            (0x006B0F27, "e8041bfaff", "direct_target_call"),
        ),
    ),
    CallerPin(
        "ItemMallIMSDataRes_serializer", ("ItemMallIMSDataRes",),
        0x006BC27D, 0x002BB67D, "this+0x70", "entry+0x4", "entry+0x8",
        (
            (0x006BBFDB, "8b74242c", "stream_formal_to_esi"),
            (0x006BBFE0, "8bf9", "this_to_edi"),
            (0x006BBFE4, "0f84de010000", "zero_mode_to_read_branch"),
            (0x006BC231, "8d6f70", "tree_member_this_plus_70"),
            (0x006BC277, "8bcd", "tree_member_to_target_ecx"),
            (0x006BC27D, "e8ae67f9ff", "direct_target_call"),
        ),
    ),
    CallerPin(
        "CHitParadeVital_serializer", ("CHitParadeVital",),
        0x007163E1, 0x003157E1, "this+0x284", "entry+0x4", "entry+0x8",
        (
            (0x00716224, "8b5c2428", "mode_formal_to_ebx"),
            (0x0071622B, "8bf1", "this_to_esi"),
            (0x00716231, "0f84f9000000", "zero_mode_to_read_branch"),
            (0x00716330, "8b7c2434", "stream_formal_to_edi"),
            (0x00716367, "81c684020000", "tree_member_this_plus_284"),
            (0x007163DB, "8bce", "tree_member_to_target_ecx"),
            (0x007163E1, "e84ac6f3ff", "direct_target_call"),
        ),
    ),
    CallerPin(
        "CCooldownAttr_serializer", ("CCooldownAttr",),
        0x006C9F33, 0x002C9333, "this+0x2C", "entry+0x4", "entry+0x8",
        (
            (0x006C9DC4, "8b5c2428", "mode_formal_to_ebx"),
            (0x006C9DCB, "8b7c2430", "stream_formal_to_edi"),
            (0x006C9DD1, "8bf1", "this_to_esi"),
            (0x006C9DD8, "83c62c", "tree_member_this_plus_2c"),
            (0x006C9DDD, "0f84c1000000", "zero_mode_to_read_branch"),
            (0x006C9F27, "8bce", "tree_member_to_target_ecx"),
            (0x006C9F33, "e8f88af8ff", "direct_target_call"),
        ),
    ),
    CallerPin(
        "DailyActivityState_serializer", ("DailyActivityState",),
        0x0069CC4C, 0x0029C04C, "this+0x28", "entry+0x4", "entry+0x8",
        (
            (0x0069CB24, "8b5c2424", "mode_formal_to_ebx"),
            (0x0069CB2B, "8b7c242c", "stream_formal_to_edi"),
            (0x0069CB30, "8be9", "this_to_ebp"),
            (0x0069CB40, "0f84a9000000", "zero_mode_to_read_branch"),
            (0x0069CC0C, "8d5d28", "tree_member_this_plus_28"),
            (0x0069CC4A, "8bcb", "tree_member_to_target_ecx"),
            (0x0069CC4C, "e8df5dfbff", "direct_target_call"),
        ),
    ),
)


BRANCH_PINS = (
    (0x00652A4D, "751f", 0x00652A6E, 0x00652A4F),
    (0x00652A5F, "7404", 0x00652A65, 0x00652A61),
    (0x00652A63, "eb03", 0x00652A68, 0),
    (0x00652A6C, "74e3", 0x00652A51, 0x00652A6E),
    (0x00652A7C, "7452", 0x00652AD0, 0x00652A7E),
    (0x00652A85, "7404", 0x00652A8B, 0x00652A87),
    (0x00652A89, "7406", 0x00652A91, 0x00652A8B),
    (0x00652A97, "752a", 0x00652AC3, 0x00652A99),
    (0x00652AD5, "7d31", 0x00652B08, 0x00652AD7),
)
BLOCK_STARTS = (
    0x00652A30, 0x00652A4F, 0x00652A51, 0x00652A61,
    0x00652A65, 0x00652A68, 0x00652A6E, 0x00652A7E,
    0x00652A87, 0x00652A8B, 0x00652A91, 0x00652A99,
    0x00652AC3, 0x00652AD0, 0x00652AD7, 0x00652B08,
)
TARGET_DIRECT_CALLS = {
    0x00652AA0: 0x00652550,
    0x00652AC3: 0x00767170,
    0x00652AE5: 0x00652550,
}

A2_DELTA_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line",
    "base_row_key", "base_delta_key", "message", "direction(W/R)",
    "old_order", "old_tag", "old_field_offset", "old_len",
    "new_wire_order", "new_tag", "new_field_offset", "new_len",
    "new_gate_condition", "resolution", "evidence_ticket",
    "evidence_span_start", "evidence_span_end", "evidence_span_sha256",
    "evidence_file_off", "source",
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
        [row[name] for name in fieldnames], ensure_ascii=False, separators=(",", ":")
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


def tsv_text(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
    handle = StringIO(newline="")
    writer = csv.DictWriter(
        handle, fieldnames=list(columns), delimiter="\t", lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue()


def atomic_write_text(path: Path, text: str) -> None:
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temp_name = handle.name
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name is not None and os.path.exists(temp_name):
            os.unlink(temp_name)


def bytes_at(image: bytes, va: int, size: int) -> bytes:
    off = va - VA_TO_FILE_DELTA
    if off < 0 or off + size > len(image):
        raise RuntimeError(f"VA outside pinned IMAGE: 0x{va:08X}")
    return image[off:off + size]


def require_bytes(image: bytes, va: int, expected_hex: str, label: str) -> None:
    expected = bytes.fromhex(expected_hex)
    actual = bytes_at(image, va, len(expected))
    if actual != expected:
        raise RuntimeError(
            f"{label} bytes drift at 0x{va:08X}: expected {expected.hex()}, got {actual.hex()}"
        )


def verify_invalid_parameter_import(image: bytes) -> None:
    """Resolve the one target-body IAT call from the PE import directory."""
    if image[:2] != b"MZ":
        raise RuntimeError("missing MZ signature")
    pe_off = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_off:pe_off + 4] != b"PE\0\0":
        raise RuntimeError("missing PE signature")
    coff = pe_off + 4
    section_count = struct.unpack_from("<H", image, coff + 2)[0]
    optional_size = struct.unpack_from("<H", image, coff + 16)[0]
    optional = coff + 20
    if struct.unpack_from("<H", image, optional)[0] != 0x10B:
        raise RuntimeError("expected PE32 optional header")
    image_base = struct.unpack_from("<I", image, optional + 28)[0]
    size_of_headers = struct.unpack_from("<I", image, optional + 60)[0]
    section_table = optional + optional_size
    sections: list[tuple[int, int, int, int]] = []
    for index in range(section_count):
        off = section_table + index * 40
        virtual_size, virtual_address, raw_size, raw_pointer = struct.unpack_from(
            "<IIII", image, off + 8
        )
        sections.append((virtual_address, virtual_size, raw_pointer, raw_size))

    def rva_to_off(rva: int) -> int:
        if 0 <= rva < size_of_headers:
            return rva
        for section_rva, virtual_size, raw_pointer, raw_size in sections:
            delta = rva - section_rva
            if 0 <= delta < raw_size and delta < max(virtual_size, raw_size):
                return raw_pointer + delta
        raise RuntimeError(f"cannot map RVA 0x{rva:08X}")

    import_rva, import_size = struct.unpack_from("<II", image, optional + 104)
    if not import_rva or not import_size:
        raise RuntimeError("missing PE import directory")
    found: tuple[str, str, int, int, int, int] | None = None
    descriptor_rva = import_rva
    while True:
        descriptor_off = rva_to_off(descriptor_rva)
        original_thunk, timestamp, forwarder, name_rva, first_thunk = struct.unpack_from(
            "<IIIII", image, descriptor_off
        )
        if (original_thunk, timestamp, forwarder, name_rva, first_thunk) == (0, 0, 0, 0, 0):
            break
        dll_off = rva_to_off(name_rva)
        dll_end = image.find(b"\0", dll_off)
        dll = image[dll_off:dll_end].decode("ascii", "strict")
        lookup_base = original_thunk or first_thunk
        index = 0
        while True:
            lookup_off = rva_to_off(lookup_base + index * 4)
            thunk = struct.unpack_from("<I", image, lookup_off)[0]
            if not thunk:
                break
            iat_rva = first_thunk + index * 4
            iat_va = image_base + iat_rva
            if iat_va == 0x00C3B4C0:
                if thunk & 0x80000000:
                    raise RuntimeError("invalid_parameter import unexpectedly ordinal")
                hint_name_off = rva_to_off(thunk)
                symbol_off = hint_name_off + 2
                symbol_end = image.find(b"\0", symbol_off)
                symbol = image[symbol_off:symbol_end].decode("ascii", "strict")
                found = (dll, symbol, rva_to_off(iat_rva), descriptor_off, lookup_off, symbol_off)
            index += 1
        descriptor_rva += 20
    expected = (
        "MSVCR90.dll", "_invalid_parameter_noinfo", 0x008398C0,
        0x00C112DC, 0x00C118B4, 0x00C15C62,
    )
    if found != expected:
        raise RuntimeError(f"IAT 0x00C3B4C0 import drift: {found} != {expected}")


def verify_image(image: bytes) -> None:
    if sha256_bytes(image) != IMAGE_SHA256:
        raise RuntimeError("pinned GameClient.local.bin SHA-256 mismatch")
    for pin in SPAN_PINS:
        if pin.start_va - VA_TO_FILE_DELTA != pin.file_off:
            raise RuntimeError(f"VA/file mapping drift for {pin.role}")
        body = image[pin.file_off:pin.file_off + (pin.end_va - pin.start_va)]
        if sha256_bytes(body) != pin.sha256:
            raise RuntimeError(f"IMAGE span drift: {pin.role}")

    # Complete CFG edge/return pins for the 239-byte helper.
    for site, encoded, target, fallthrough in BRANCH_PINS:
        require_bytes(image, site, encoded, "target CFG branch")
        raw = bytes.fromhex(encoded)
        displacement = struct.unpack("b", raw[1:2])[0]
        actual_target = site + len(raw) + displacement
        if actual_target != target:
            raise RuntimeError(f"target CFG edge drift at 0x{site:08X}")
        if fallthrough and site + len(raw) != fallthrough:
            raise RuntimeError(f"target CFG fallthrough drift at 0x{site:08X}")
    for site in (0x00652AC0, 0x00652B05, 0x00652B1C):
        require_bytes(image, site, "c20800", "target ret 8")

    target = bytes_at(image, 0x00652A30, 0xEF)
    rel_calls: dict[int, int] = {}
    for index in range(len(target) - 4):
        if target[index] != 0xE8:
            continue
        site = 0x00652A30 + index
        rel_calls[site] = site + 5 + struct.unpack_from("<i", target, index + 1)[0]
    if rel_calls != TARGET_DIRECT_CALLS:
        raise RuntimeError(f"target direct-call set drift: {rel_calls}")
    require_bytes(image, 0x00652A8B, "ff15c0b4c300", "_invalid_parameter_noinfo call")
    if target.count(bytes.fromhex("ff15c0b4c300")) != 1:
        raise RuntimeError("target exact-import call census drift")
    verify_invalid_parameter_import(image)
    if 0x0089A600 in rel_calls.values() or 0x0089A640 in rel_calls.values():
        raise RuntimeError("wire primitive unexpectedly reached from target")
    for site in (0x00652AB3, 0x00652AB6, 0x00652ABA, 0x00652AF8, 0x00652AFB, 0x00652AFF, 0x00652B0E, 0x00652B12, 0x00652B16):
        # Result writes are fully covered by the body hash; pin their starts so
        # an accidental re-interpretation cannot silently move them.
        if bytes_at(image, site, 1)[0] not in (0x89, 0xC6):
            raise RuntimeError(f"target result-write pin drift at 0x{site:08X}")

    for caller in CALLER_PINS:
        for va, encoded, label in caller.byte_pins:
            require_bytes(image, va, encoded, f"{caller.role}:{label}")
        call = bytes_at(image, caller.call_va, 5)
        if call[0] != 0xE8:
            raise RuntimeError(f"missing direct target call: {caller.role}")
        target_va = caller.call_va + 5 + struct.unpack_from("<i", call, 1)[0]
        if target_va != 0x00652A30:
            raise RuntimeError(f"caller target drift: {caller.role}")
        if caller.call_va - VA_TO_FILE_DELTA != caller.call_file_off:
            raise RuntimeError(f"caller file-offset drift: {caller.role}")


def caller_for_message(message: str) -> CallerPin:
    matches = [pin for pin in CALLER_PINS if message in pin.messages]
    if len(matches) != 1:
        raise RuntimeError(f"caller mapping drift for {message}: {len(matches)}")
    return matches[0]


def build_delta(
    base_fields: Sequence[str], base_rows: Sequence[tuple[int, dict[str, str]]],
    slot_fields: Sequence[str], slot_rows: Sequence[tuple[int, dict[str, str]]],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []

    base_hits = [(line, row) for line, row in base_rows if row.get("tag") == TARGET_TAG]
    expected_base = {
        983: ("ServerAddedInfoVital", "R"),
        984: ("ServerAddedInfoVital", "W"),
        3039: ("GSSS_GuildDataVitalRes", "W"),
        3205: ("GSSS_GuildDataVitalRes", "R"),
        3332: ("GSSS_GSInitialGuildDataVital", "W"),
        3498: ("GSSS_GSInitialGuildDataVital", "R"),
        4693: ("ItemMallUpdatePersonalDataVital", "R"),
        4694: ("ItemMallUpdatePersonalDataVital", "W"),
        4862: ("ItemMallIMSDataRes", "W"),
        5000: ("ItemMallIMSDataRes", "R"),
        6005: ("CHitParadeVital", "R"),
        6006: ("CHitParadeVital", "W"),
    }
    actual_base = {line: (row["message"], row["direction(W/R)"]) for line, row in base_hits}
    if actual_base != expected_base:
        raise RuntimeError(f"V1 target-row census drift: {actual_base}")

    for line, row in base_hits:
        if row["source"] != "IMAGE" or row["field_offset"] != "UNKNOWN(direct_call_not_proven_serializer)":
            raise RuntimeError(f"V1 target evidence drift at line {line}")
        caller = caller_for_message(row["message"])
        if row["span_start"] != f"0x{next(p for p in SPAN_PINS if p.role == caller.role).start_va:08X}":
            raise RuntimeError(f"V1 caller span start drift at line {line}")
        if row["span_sha256"] != next(p for p in SPAN_PINS if p.role == caller.role).sha256:
            raise RuntimeError(f"V1 caller span hash drift at line {line}")
        if row["file_off_claim"] != f"0x{caller.call_file_off:08X}":
            raise RuntimeError(f"V1 callsite drift at line {line}")
        row_key = canonical_row_key(base_fields, row)
        values = {
            "action": "REMOVE_NONWIRE_ROW",
            "change_type": "NONWIRE_ORDERED_TREE_INSERT_AFTER_STREAM_READ",
            "base_file": A2_NAME,
            "base_line": str(line),
            "base_row_key": row_key,
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
            "resolution": "ORDERED_TREE_INSERT_NO_STREAM_FORMAL;CALLER_STACK_KEY_AND_RESULT",
            "evidence_ticket": EVIDENCE_TICKET,
            "evidence_span_start": f"0x{next(p for p in SPAN_PINS if p.role == caller.role).start_va:08X}",
            "evidence_span_end": f"0x{next(p for p in SPAN_PINS if p.role == caller.role).end_va:08X}",
            "evidence_span_sha256": next(p for p in SPAN_PINS if p.role == caller.role).sha256,
            "evidence_file_off": f"0x{caller.call_file_off:08X}",
            "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(("A2", values["action"], values["base_file"], values["base_line"], row_key))
        output.append(values)

    slot_hits = [(line, row) for line, row in slot_rows if row.get("new_tag") == TARGET_TAG]
    expected_slot = {
        669: ("CCooldownAttr", "R"),
        670: ("CCooldownAttr", "W"),
        1003: ("DailyActivityState", "R"),
        1004: ("DailyActivityState", "W"),
    }
    actual_slot = {line: (row["message"], row["direction(W/R)"]) for line, row in slot_hits}
    if actual_slot != expected_slot:
        raise RuntimeError(f"slot34 target-row census drift: {actual_slot}")

    for line, row in slot_hits:
        if row["action"] != "ADD_CORRECTED_SLOT34_ROW" or row["source"] != "IMAGE":
            raise RuntimeError(f"slot34 target evidence drift at line {line}")
        if row["new_field_offset"] != "UNKNOWN(direct_call_not_proven_serializer)":
            raise RuntimeError(f"slot34 target blocker drift at line {line}")
        caller = caller_for_message(row["message"])
        span = next(p for p in SPAN_PINS if p.role == caller.role)
        if row["new_span_start"] != f"0x{span.start_va:08X}" or row["new_span_sha256"] != span.sha256:
            raise RuntimeError(f"slot34 caller span drift at line {line}")
        if row["new_file_off_claim"] != f"0x{caller.call_file_off:08X}":
            raise RuntimeError(f"slot34 callsite drift at line {line}")
        row_key = canonical_row_key(slot_fields, row)
        values = {
            "action": "REMOVE_OVERLAY_NONWIRE_ROW",
            "change_type": "NONWIRE_ORDERED_TREE_INSERT_AFTER_STREAM_READ",
            "base_file": SLOT34_A2_NAME,
            "base_line": str(line),
            "base_row_key": row_key,
            "base_delta_key": row["delta_key"],
            "message": row["message"],
            "direction(W/R)": row["direction(W/R)"],
            "old_order": row["new_order"],
            "old_tag": row["new_tag"],
            "old_field_offset": row["new_field_offset"],
            "old_len": row["new_len"],
            "new_wire_order": "N/A",
            "new_tag": "N/A",
            "new_field_offset": "N/A",
            "new_len": "N/A",
            "new_gate_condition": "N/A",
            "resolution": "ORDERED_TREE_INSERT_NO_STREAM_FORMAL;CALLER_STACK_KEY_AND_RESULT",
            "evidence_ticket": EVIDENCE_TICKET,
            "evidence_span_start": f"0x{span.start_va:08X}",
            "evidence_span_end": f"0x{span.end_va:08X}",
            "evidence_span_sha256": span.sha256,
            "evidence_file_off": f"0x{caller.call_file_off:08X}",
            "source": "IMAGE",
        }
        values["delta_key"] = make_delta_key(("A2", values["action"], values["base_file"], values["base_line"], row_key))
        output.append(values)

    output.sort(key=lambda row: (row["base_file"], int(row["base_line"])))
    if len(output) != 16:
        raise RuntimeError(f"expected 16 removal directives, got {len(output)}")
    if len({row["delta_key"] for row in output}) != 16:
        raise RuntimeError("duplicate delta_key")
    identities = {(row["base_file"], row["base_line"], row["base_row_key"]) for row in output}
    if len(identities) != 16:
        raise RuntimeError("duplicate base-row target")
    if any(row["source"] != "IMAGE" for row in output):
        raise RuntimeError("mixed evidence source")
    if any("UNCHANGED" in "\t".join(row.values()) or "COPIED" in "\t".join(row.values()) for row in output):
        raise RuntimeError("unchanged/copied output is forbidden")
    return output


def verify_cross_overlay(external: Path, delta: Sequence[Mapping[str, str]]) -> None:
    wanted = {(row["base_file"], row["base_line"], row["base_row_key"]) for row in delta}
    overlaps: list[str] = []
    for path in sorted(external.glob("*DELTA.tsv")):
        if path.name == OUTPUT_NAME:
            continue
        fields, rows = read_tsv_with_lines(path)
        if not {"base_file", "base_line", "base_row_key"}.issubset(fields):
            continue
        for line, row in rows:
            identity = (row["base_file"], row["base_line"], row["base_row_key"])
            if identity in wanted:
                overlaps.append(f"{path.name}:{line}:{identity[0]}:{identity[1]}")
    if overlaps:
        raise RuntimeError("cross-overlay base-row overlap: " + " | ".join(overlaps))

    # Effective source census: before this removal overlay, the target exists
    # only in frozen V1 and the slot34 additive correction.
    occurrences: dict[str, int] = {}
    for path in sorted(external.glob("*.tsv")):
        if path.name == OUTPUT_NAME:
            continue
        fields, rows = read_tsv_with_lines(path)
        count = 0
        if "tag" in fields:
            count += sum(row.get("tag") == TARGET_TAG for _line, row in rows)
        if "new_tag" in fields:
            count += sum(row.get("new_tag") == TARGET_TAG for _line, row in rows)
        if count:
            occurrences[path.name] = count
    expected = {A2_NAME: 12, SLOT34_A2_NAME: 4}
    if occurrences != expected:
        raise RuntimeError(f"effective target occurrence census drift: {occurrences}")


def priority_residuals(external: Path) -> list[tuple[str, str, str]]:
    fields, rows = read_tsv_with_lines(external / PRIORITY_NAME)
    by_message = {row["message"]: row for _line, row in rows}
    slot_fields, slot_rows = read_tsv_with_lines(external / SLOT34_PRIORITY_NAME)
    slot_by_message = {row["message"]: row for _line, row in slot_rows if row["message"] in SLOT34_MESSAGES}
    if set(slot_by_message) != set(SLOT34_MESSAGES):
        raise RuntimeError("slot34 priority rows for target messages drift")

    result: list[tuple[str, str, str]] = []
    for message in P1_MESSAGES:
        row = by_message[message]
        if row["priority"] != "1" or row["serializer_status"] != "OPEN":
            raise RuntimeError(f"P1 status drift for {message}")
        blockers = [part.strip() for part in row["serializer_blockers"].split("|")]
        if "direct_call_not_proven_serializer" not in blockers:
            raise RuntimeError(f"target blocker missing for {message}")
        residual = [part for part in blockers if part != "direct_call_not_proven_serializer"]
        if not residual:
            raise RuntimeError(f"target removal would close {message}; Priority delta required")
        result.append((message, "1", " | ".join(residual)))

    for message in SLOT34_MESSAGES:
        row = slot_by_message[message]
        if row["new_serializer_status"] != "OPEN" or row["new_structural_status"] != "OPEN":
            raise RuntimeError(f"slot34 effective status drift for {message}")
        blockers = [part.strip() for part in row["new_serializer_blockers"].split("|")]
        if "direct_call_not_proven_serializer" not in blockers:
            raise RuntimeError(f"slot34 target blocker missing for {message}")
        residual = [part for part in blockers if part != "direct_call_not_proven_serializer"]
        if not residual:
            raise RuntimeError(f"target removal would close {message}; Priority delta required")
        result.append((message, "3", " | ".join(residual)))
    return result


def report_text(delta: Sequence[Mapping[str, str]], residuals: Sequence[tuple[str, str, str]]) -> str:
    lines = [
        "# PF static closure for target 0x00652A30",
        "",
        "[MEASURED] IMAGE-only additive correction. Frozen V1 and the slot-0x34 correction remain untouched.",
        "",
        "## Outcome",
        "",
        "- Removed **16 effective A2 analysis artifacts**: 12 frozen-V1 rows plus 4 rows added by the slot-0x34 correction.",
        "- The 16 directives contain **0 unchanged copies**, **0 duplicate base rows**, and **0 cross-overlay base-row overlaps**.",
        "- No Priority delta is emitted. All six affected Priority-1 messages and both affected Priority-3 Attr messages retain other blockers and remain `OPEN`.",
        "- `0x00652A30` is an ordered-tree lookup/insert helper reached only after the read branch has already consumed key/value bytes into caller stack locals. It is not a wire primitive.",
        "- No semantic claim is made for any tree key or value. Their widths and nearby message names do not establish meaning.",
        "",
        "## Duplicate and layer accounting",
        "",
        "| input layer | removal action | rows | W | R | unchanged copied | duplicate/cross-overlap | source |",
        "|---|---|---:|---:|---:|---:|---:|---|",
        "| frozen V1 A2 | `REMOVE_NONWIRE_ROW` | 12 | 6 | 6 | 0 | 0 | IMAGE |",
        "| slot-0x34 A2 overlay | `REMOVE_OVERLAY_NONWIRE_ROW` | 4 | 2 | 2 | 0 | 0 | IMAGE |",
        "",
        "The W rows are path-insensitive duplicates of a call that exists only below the zero-mode/read branch. The R rows name a real call, but that call mutates an ordered-tree member after the stream primitives have returned; it does not itself read or write the stream.",
        "",
        "## Exact helper boundary and call set",
        "",
        "| role | start VA | end VA (exclusive) | bytes | file offset | SHA-256 |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for pin in SPAN_PINS[:3]:
        lines.append(f"| {pin.role} | `0x{pin.start_va:08X}` | `0x{pin.end_va:08X}` | {pin.end_va-pin.start_va} | `0x{pin.file_off:08X}` | `{pin.sha256}` |")
    lines += [
        "",
        "The complete 239-byte target decodes into the pinned 16-block CFG below and has three `ret 8` exits (`0x00652AC0`, `0x00652B05`, `0x00652B1C`). Its complete direct-call set is `0x00652AA0 -> 0x00652550`, `0x00652AC3 -> 0x00767170`, and `0x00652AE5 -> 0x00652550`; the only exact imported call in the body is `0x00652A8B -> [0x00C3B4C0]` (`_invalid_parameter_noinfo`). No call reaches wire primitive `0x0089A600` or `0x0089A640`.",
        "",
        "Structurally, the helper walks children at node `+0x00/+0x08`, compares the caller-stack key with node `+0x0C`, checks the sentinel byte at `+0x15`, inserts/rebalances through fixed helper `0x00652550`, advances through `0x00767170`, and writes only the caller-provided result object at `+0/+4/+8` plus the ordered-tree state. This is structure, not a key/value semantic label.",
        "",
        "## Exact CFG branches",
        "",
        "| site | taken | fallthrough |",
        "|---:|---:|---:|",
    ]
    for site, _encoded, target, fallthrough in BRANCH_PINS:
        fall = "N/A" if not fallthrough else f"`0x{fallthrough:08X}`"
        lines.append(f"| `0x{site:08X}` | `0x{target:08X}` | {fall} |")
    lines += [
        "",
        "Basic-block starts: " + ", ".join(f"`0x{va:08X}`" for va in BLOCK_STARTS) + ".",
        "",
        "## Caller provenance and stream separation",
        "",
        "Every serializer uses stream formal `entry+0x4` and mode formal `entry+0x8`. The target receives neither formal: `ECX` is the member below, arg1 is a caller-stack result object, and arg2 is a caller-stack key/value object populated after primitive reads.",
        "",
        "| caller/messages | span | target call | target ECX | stream reaching definition | source |",
        "|---|---|---:|---|---|---|",
    ]
    for caller in CALLER_PINS:
        pin = next(p for p in SPAN_PINS if p.role == caller.role)
        messages = ", ".join(f"`{m}`" for m in caller.messages)
        lines.append(
            f"| {messages} | `0x{pin.start_va:08X}-0x{pin.end_va:08X}` / `{pin.sha256}` | "
            f"`0x{caller.call_va:08X}` | `{caller.member}` | stream `{caller.stream_formal}`, mode `{caller.mode_formal}` | IMAGE |"
        )
    lines += [
        "",
        "The two corrected Attr callers follow the same convention: `CCooldownAttr` parses `(i16,f32)` before inserting into `this+0x2C`; `DailyActivityState` parses `(u32,u8)` before inserting into `this+0x28`. Those are raw widths only, not meanings.",
        "",
        "## Priority status after removing only this target",
        "",
        "| message | priority | status | residual blockers (0x00652A30 removed) |",
        "|---|---:|---|---|",
    ]
    for message, priority, blockers in residuals:
        lines.append(f"| `{message}` | {priority} | OPEN | `{blockers}` |")
    lines += [
        "",
        "## Nonclaims and stop rule",
        "",
        "- No tree key/value meaning, gameplay meaning, runtime behavior, capture agreement, or server behavior is claimed.",
        "- No other blocker is removed merely because it appears in the same serializer.",
        "- Stop at this exact helper and its seven proven callers. Resume only if another effective A2 layer adds a new `0x00652A30` row or if independent evidence resolves one of the listed residual blockers.",
        "",
    ]
    return "\n".join(lines)


def build(external: Path) -> tuple[str, str]:
    image_path = external.parent.parent / "GameClient" / "GameClient.local.bin"
    require_hash(image_path, IMAGE_SHA256, "IMAGE")
    require_hash(external / A2_NAME, A2_SHA256, "V1 A2")
    require_hash(external / SLOT34_A2_NAME, SLOT34_A2_SHA256, "slot34 A2")
    require_hash(external / PRIORITY_NAME, PRIORITY_SHA256, "V1 Priority")
    require_hash(external / SLOT34_PRIORITY_NAME, SLOT34_PRIORITY_SHA256, "slot34 Priority")
    image = image_path.read_bytes()
    verify_image(image)
    base_fields, base_rows = read_tsv_with_lines(external / A2_NAME)
    slot_fields, slot_rows = read_tsv_with_lines(external / SLOT34_A2_NAME)
    delta = build_delta(base_fields, base_rows, slot_fields, slot_rows)
    verify_cross_overlay(external, delta)
    residuals = priority_residuals(external)
    return tsv_text(A2_DELTA_COLUMNS, delta), report_text(delta, residuals)


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
                raise RuntimeError(f"missing output: {path}")
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                raise RuntimeError(f"output drift: {path.name}")
        print("PASS target 0x00652A30: 16 unique non-wire removals; cross-overlay overlap 0; Priority delta 0")
        return 0
    for path, text in outputs.items():
        atomic_write_text(path, text)
    print("WROTE target 0x00652A30: 16 unique non-wire removals; cross-overlay overlap 0; Priority delta 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
