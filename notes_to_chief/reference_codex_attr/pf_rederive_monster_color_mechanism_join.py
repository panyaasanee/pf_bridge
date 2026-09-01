#!/usr/bin/env python3
"""Re-derive the FACTION/relation to CNetNPC name-style mechanism join.

This is a static, read-only derivation over the pinned original client IMAGE and
original DATA.  It never runs the client, server, dumps, or captures.  Decoded
CONSTDATA remains in memory.  The emitted TSV keeps one evidence source per row
and references, rather than copies, existing PF_MONSTER_COLOR_GATE facts.

Only the Python standard library is used.  Console output is ASCII only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import lzma
import os
import struct
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
CONSTDATA_PATH = PF_ROOT / "GameClient" / "Data" / "B_CONSTDATA_TH.pc_"
FONT_STYLE_PATH = (
    PF_ROOT / "GameClient" / "Data" / "GUI" / "Model" / "BigFontStyle.fsl"
)
PRIOR_GATE_PATH = OUT_DIR / "PF_MONSTER_COLOR_GATE.tsv"
TSV_PATH = OUT_DIR / "PF_MONSTER_COLOR_MECHANISM_JOIN.tsv"
REPORT_PATH = OUT_DIR / "PF_MONSTER_COLOR_MECHANISM_JOIN.md"
LOCK_TARGET_PATH = Path(__file__).resolve()

IMAGE_SOURCE = "PF_ROOT://GameClient/GameClient.local.bin"
CONSTDATA_SOURCE = "PF_ROOT://GameClient/Data/B_CONSTDATA_TH.pc_"

IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
CONSTDATA_SIZE = 426_944
CONSTDATA_SHA256 = "496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8"
CONSTDATA_DECODED_SIZE = 8_443_000
CONSTDATA_DECODED_SHA256 = (
    "496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d"
)
FONT_STYLE_SIZE = 28_144
FONT_STYLE_SHA256 = (
    "77798599c203d36e11282633d4a91ac098b0e1e03aa2482fede6fcfca161fc10"
)
PRIOR_GATE_SIZE = 110_234
PRIOR_GATE_SHA256 = (
    "8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0"
)

PAIR_DOMAIN = b"PF_MONSTER_COLOR_MECHANISM_JOIN_PAIR_V1\x00"
PAIR_PLACEHOLDER = "0" * 64
TSV_SHA_PLACEHOLDER = "f" * 64
PAIR_LINE_PREFIX = "- Pair generation SHA256: `"
TSV_LINE_PREFIX = "- TSV SHA256: `"

IMAGE_BASE = 0x00400000

# name, VA, VirtualSize, raw file offset, SizeOfRawData
EXPECTED_SECTIONS = (
    (".text", 0x00401000, 0x00838A2C, 0x00000400, 0x00838C00),
    (".code", 0x00C3A000, 0x000002E1, 0x00839000, 0x00000400),
    (".rdata", 0x00C3B000, 0x003DE38E, 0x00839400, 0x003DE400),
    (".data", 0x0101A000, 0x00081F70, 0x00C17800, 0x00011E00),
    (".rsrc", 0x0109C000, 0x00058998, 0x00C29600, 0x00058A00),
    (".reloc", 0x010F5000, 0x001915F0, 0x00C82000, 0x00191600),
)

# End VAs are exclusive.  These hashes pin the manually interpreted x86 spans;
# the generator checks structural anchors but does not claim symbolic execution.
SPANS: dict[str, tuple[int, int, str]] = {
    "singleton_getter": (
        0x0040B560,
        0x0040B5C7,
        "35ffcc889e7582c4b36b0dee5ea0b98fc021bb1c9f662c283fd06cb1ebadd506",
    ),
    "manager_constructor": (
        0x004A4B00,
        0x004A4C40,
        "9966a6d6d18e298868259407af2ceed9aabf13a6933b7fee7501f40debea0d85",
    ),
    "faction_loader": (
        0x004A2BF0,
        0x004A2E56,
        "432d0120f2bdbbeadf2ad9601b0074fb3a66eadcf2449071defb2549a31f7b4a",
    ),
    "faction_record_constructor": (
        0x004A1FF0,
        0x004A2011,
        "aff500211a46040e30f4e9043d58ef39c1c0e095ad0e030ac96843f0b599cc7c",
    ),
    "token_parser": (
        0x00435C30,
        0x00435D80,
        "de0f0fbd18efb8da88cb7e575730d9cef24334025b592868b4793edcf50c1c0f",
    ),
    "numeric_token_helper": (
        0x00431990,
        0x004319AC,
        "c27dd5efdd4b6ed373b2209de72dc421a46bf6e6655829e7c7730fc577054f8c",
    ),
    "set_insert": (
        0x0043A570,
        0x0043A660,
        "9a2ecf708dc35bd6c05d1bb022cd0b485228d3fd64196fc8fcc09dc1e9d85aaf",
    ),
    "set_find": (
        0x0043A660,
        0x0043A6E9,
        "16e5b28ca94a0964b244ba305cb3ebcb504e655744f4f0f8d7ff6ba0ba286420",
    ),
    "faction_comparator": (
        0x004A1D50,
        0x004A1E14,
        "cbc9d0ab90ed7828534a86c10f42322b09555a5034f71ef7ac14e0cd8e64cac5",
    ),
    "relation_predicate_full": (
        0x0043C380,
        0x0043C63C,
        "1d99f8557252742914c4f7358853aac06f0b54603f78a4b4d073aaea2afcbd89",
    ),
    "relation_fallback": (
        0x0043C5C9,
        0x0043C5FF,
        "916a45082cc44a28219206b05729cb14f80575f054a56ca7acf1cb14a159f3a1",
    ),
    "selector_positive_relation_lane": (
        0x00443FFB,
        0x00444040,
        "6474623ff6e5708a436516d50fa830e85b7b4c9122b331bb195d21d3f06ee6ca",
    ),
    "selector_primary": (
        0x00443F50,
        0x0044427F,
        "b4de36611b4d6693844bc6de7aab4f47fbe7f3be80ee7c8ce052275fc9bdd546",
    ),
    "selector_nonpositive_lane": (
        0x00444151,
        0x0044427F,
        "bcf00fe7d1175305f0029b22ea7ce9e1e63bd765e9464a795dbbf40c1d01e6fd",
    ),
    "selector_common_style_sink": (
        0x00444270,
        0x0044427F,
        "fd9d2925a9cb9280d60e2d8c5465444abdb2ed438b0769c9ddb2f4c2ff302d0e",
    ),
}

LITERALS = {
    "FACTION": (0x00F152E8, "FACTION"),
    "n_ID": (0x00F0C958, "n_ID"),
    "s_ENEMY": (0x00F1527C, "s_ENEMY"),
    "delimiter": (0x00F1528C, ";\t\t"),
}

PRIOR_REFERENCES = {
    "MCG-IMG-025": "ee873e584b31215b2bd872784efacb3d72d9280d37e5cde439d4f913fc8d6f36",
    "MCG-IMG-030": "e0f7eb4cdc83679959adcacfacf222122c169fed803586c6b951906b4dda031e",
    "MCG-IMG-031": "7782bb41255484f1ba482a911f2f3800744d3434f9f3c8fd6c566053635ad1a6",
    "MCG-IMG-032": "6a20794931b4d0d8cb70ad9d1cf45cbb2ab8f87a2badadb08cb7e7f4480ed23c",
    "MCG-IMG-033": "0ff5dd0011ac742373f643770fa72031c9adb657f11fe9c272e2cd2ca6f9b935",
    "MCG-IMG-045": "61c77d4a1ae4530008e9042db6799600def4c3b405e342f6db97e758920e4964",
    "MCG-IMG-051": "5eb4fb255371e1f0697518f50069695fb2d3d90bcb70a144456c814e2a4dc89a",
    "MCG-IMG-052": "3da1d093ad7df399f38b54f9dd02f38906e19da3a6035de72481fe3772286cf8",
    "MCG-IMG-053": "1a2981dff0a1a5a1927b9efe0c35ed5ae3d1a3ba75dc1b9e5e4d009a6d7ecadb",
    "MCG-IMG-054": "05aec8e3de35ba77ead5cb5ce006660b72e22a211a07014df48fa848901d164d",
    "MCG-IMG-055": "7a676f4fe8acf4748105ff6b5dffb337997b7dde695c414d60e4cf823d7e56e2",
    "MCG-IMG-057": "c57eb03ef90d339cea95ffa47bcc6f519b726b7e7629666d6bbdb922920b9706",
    "MCG-IMG-058": "3a4a5aef9ed8a22cc9671e57e3c422a13b12f6bbdc3cec9667bd5d92ed3126d3",
    "MCG-DATA-001": "7e247e4ca3b7c6b1f81c7aeddd46e8feb0e50d30c68214861de20029d04782d1",
    "MCG-DATA-006": "b204ce72068ec5b55d8425681dd9ca7fa2987e74be1de900e725090519fc5812",
    "MCG-DATA-007": "c8f8ef6a1e8d049f96e8005b609fd717391bee844e2ae9ba0da25aa020b6847f",
    "MCG-DATA-008": "01cddd7bccb4f3d1b98c31d3131d92c914d552c870845591edb43c459e0579e3",
}

FIELDNAMES = (
    "join_key",
    "row_kind",
    "subject",
    "input_or_key",
    "condition",
    "output",
    "semantic_status",
    "producer_va",
    "consumer_va",
    "span_start_va",
    "span_end_va",
    "file_off_start",
    "file_off_end",
    "decoded_off_start",
    "decoded_off_end",
    "span_sha256",
    "support_spans",
    "prior_reference",
    "source",
    "source_file",
    "source_locator",
    "source_size",
    "source_sha256",
    "image_sha256",
    "pair_generation_sha256",
    "nonclaim",
    "blocker",
    "required_next_evidence",
    "evidence_key",
)


@dataclass(frozen=True)
class Section:
    name: str
    va: int
    virtual_size: int
    raw_offset: int
    raw_size: int


@dataclass(frozen=True)
class FactionTable:
    index: int
    start: int
    end: int
    serialized_size: int
    version: int
    flags: int | str
    columns: tuple[tuple[str, int, int, int], ...]
    rows: tuple[tuple[int, str, int, int], ...]


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def ascii_safe(value: object) -> str:
    return str(value).encode("ascii", "backslashreplace").decode("ascii")


def read_pinned(path: Path, expected_size: int, expected_sha256: str) -> bytes:
    raw = path.read_bytes()
    if len(raw) != expected_size:
        raise RuntimeError(
            f"size mismatch for {path}: expected {expected_size}, got {len(raw)}"
        )
    actual = sha256_bytes(raw)
    if actual != expected_sha256:
        raise RuntimeError(
            f"sha256 mismatch for {path}: expected {expected_sha256}, got {actual}"
        )
    return raw


def parse_pe_sections(image: bytes) -> tuple[Section, ...]:
    if image[:2] != b"MZ":
        raise RuntimeError("missing MZ signature")
    pe_offset = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_offset : pe_offset + 4] != b"PE\x00\x00":
        raise RuntimeError("missing PE signature")
    number_of_sections = struct.unpack_from("<H", image, pe_offset + 6)[0]
    optional_size = struct.unpack_from("<H", image, pe_offset + 20)[0]
    optional_offset = pe_offset + 24
    if struct.unpack_from("<H", image, optional_offset)[0] != 0x10B:
        raise RuntimeError("expected PE32 optional header")
    if struct.unpack_from("<I", image, optional_offset + 28)[0] != IMAGE_BASE:
        raise RuntimeError("unexpected image base")
    section_offset = optional_offset + optional_size
    result: list[Section] = []
    for index in range(number_of_sections):
        offset = section_offset + index * 40
        name = image[offset : offset + 8].split(b"\x00", 1)[0].decode("ascii")
        virtual_size, rva, raw_size, raw_offset = struct.unpack_from(
            "<IIII", image, offset + 8
        )
        result.append(
            Section(name, IMAGE_BASE + rva, virtual_size, raw_offset, raw_size)
        )
    actual = tuple(
        (s.name, s.va, s.virtual_size, s.raw_offset, s.raw_size) for s in result
    )
    if actual != EXPECTED_SECTIONS:
        raise RuntimeError("PE section table mismatch")
    return tuple(result)


def va_to_offset(va: int, sections: Sequence[Section]) -> int:
    for section in sections:
        delta = va - section.va
        if 0 <= delta < section.raw_size:
            return section.raw_offset + delta
    if IMAGE_BASE <= va < min(section.va for section in sections):
        return va - IMAGE_BASE
    raise RuntimeError(f"VA is not file-backed: 0x{va:08X}")


def span_locator(
    name: str, sections: Sequence[Section]
) -> tuple[str, str, str, str, str]:
    start, end, digest = SPANS[name]
    file_start = va_to_offset(start, sections)
    file_end = file_start + end - start
    return (
        f"0x{start:08X}",
        f"0x{end:08X}",
        f"0x{file_start:08X}",
        f"0x{file_end:08X}",
        digest,
    )


def support_locator(name: str, sections: Sequence[Section]) -> str:
    start, end, digest = SPANS[name]
    file_start = va_to_offset(start, sections)
    file_end = file_start + end - start
    return (
        f"{name}=VA:0x{start:08X}..0x{end:08X}"
        f"@file:0x{file_start:08X}..0x{file_end:08X}@sha256:{digest}"
    )


def verify_spans(image: bytes, sections: Sequence[Section]) -> None:
    for name, (start, end, expected) in SPANS.items():
        start_offset = va_to_offset(start, sections)
        end_offset = start_offset + end - start
        if not (0 <= start_offset < end_offset <= len(image)):
            raise RuntimeError(f"span outside image: {name}")
        actual = sha256_bytes(image[start_offset:end_offset])
        if actual != expected:
            raise RuntimeError(
                f"span hash mismatch for {name}: expected {expected}, got {actual}"
            )


def read_utf16z(image: bytes, va: int, sections: Sequence[Section]) -> str:
    offset = va_to_offset(va, sections)
    cursor = offset
    while cursor + 2 <= len(image) and image[cursor : cursor + 2] != b"\x00\x00":
        cursor += 2
    if cursor + 2 > len(image):
        raise RuntimeError(f"unterminated UTF-16 string at 0x{va:08X}")
    return image[offset:cursor].decode("utf-16le")


def direct_call_target(image: bytes, site_va: int, sections: Sequence[Section]) -> int:
    offset = va_to_offset(site_va, sections)
    if image[offset] != 0xE8:
        raise RuntimeError(f"expected E8 direct call at 0x{site_va:08X}")
    relative = struct.unpack_from("<i", image, offset + 1)[0]
    return site_va + 5 + relative


def direct_call_census(
    image: bytes, target_va: int, sections: Sequence[Section]
) -> tuple[int, ...]:
    sites: list[int] = []
    for section in sections:
        size = min(section.virtual_size, section.raw_size)
        raw = image[section.raw_offset : section.raw_offset + size]
        for index in range(0, max(0, len(raw) - 4)):
            if raw[index] != 0xE8:
                continue
            relative = struct.unpack_from("<i", raw, index + 1)[0]
            site = section.va + index
            if site + 5 + relative == target_va:
                sites.append(site)
    return tuple(sites)


def resolve_import(
    image: bytes, target_iat_va: int, sections: Sequence[Section]
) -> tuple[str, str]:
    pe_offset = struct.unpack_from("<I", image, 0x3C)[0]
    optional_offset = pe_offset + 24
    import_rva, import_size = struct.unpack_from("<II", image, optional_offset + 104)
    descriptor_offset = va_to_offset(IMAGE_BASE + import_rva, sections)
    descriptor_end = descriptor_offset + import_size
    while descriptor_offset + 20 <= descriptor_end:
        original, timestamp, forwarder, name_rva, first_thunk = struct.unpack_from(
            "<IIIII", image, descriptor_offset
        )
        if original == timestamp == forwarder == name_rva == first_thunk == 0:
            break
        dll_offset = va_to_offset(IMAGE_BASE + name_rva, sections)
        dll_end = image.find(b"\x00", dll_offset)
        dll_name = image[dll_offset:dll_end].decode("ascii")
        lookup_rva = original or first_thunk
        index = 0
        while True:
            thunk_offset = va_to_offset(IMAGE_BASE + lookup_rva, sections) + index * 4
            thunk = struct.unpack_from("<I", image, thunk_offset)[0]
            if thunk == 0:
                break
            iat_va = IMAGE_BASE + first_thunk + index * 4
            if iat_va == target_iat_va:
                if thunk & 0x80000000:
                    return dll_name, f"ordinal_{thunk & 0xFFFF}"
                name_offset = va_to_offset(IMAGE_BASE + thunk, sections) + 2
                name_end = image.find(b"\x00", name_offset)
                return dll_name, image[name_offset:name_end].decode("ascii")
            index += 1
        descriptor_offset += 20
    raise RuntimeError(f"IAT entry not found: 0x{target_iat_va:08X}")


def verify_static_anchors(image: bytes, sections: Sequence[Section]) -> None:
    for label, (va, expected) in LITERALS.items():
        actual = read_utf16z(image, va, sections)
        if actual != expected:
            raise RuntimeError(
                f"literal mismatch for {label}: expected {expected!r}, got {actual!r}"
            )

    unique_calls = {
        0x004A1D50: (0x0043C5E0,),
        0x004A2BB0: (0x004A4C23,),
        0x004A4B00: (0x0040B5A0,),
        0x00443F50: (0x004446A7,),
    }
    for target, expected_sites in unique_calls.items():
        actual_sites = direct_call_census(image, target, sections)
        if actual_sites != expected_sites:
            raise RuntimeError(
                f"direct-call census mismatch for 0x{target:08X}: "
                f"expected {expected_sites!r}, got {actual_sites!r}"
            )

    expected_calls = {
        0x0043C5D9: 0x0040B560,
        0x0043C5E0: 0x004A1D50,
        0x004A1D66: 0x005F8400,
        0x004A1DC0: 0x0043A660,
        0x004A4C23: 0x004A2BB0,
        0x004A2D56: 0x004A1FF0,
        0x004A2DF8: 0x00435C30,
        0x004A2E1E: 0x00431990,
        0x004A2E3B: 0x0043A570,
        0x00444018: 0x0043C380,
        0x00444152: 0x0043C380,
    }
    for site, target in expected_calls.items():
        actual = direct_call_target(image, site, sections)
        if actual != target:
            raise RuntimeError(
                f"call target mismatch at 0x{site:08X}: "
                f"expected 0x{target:08X}, got 0x{actual:08X}"
            )

    dll_name, import_name = resolve_import(image, 0x00C3B52C, sections)
    if dll_name.lower() != "msvcr90.dll" or import_name != "_wtoi":
        raise RuntimeError(
            f"numeric conversion import mismatch: {dll_name}!{import_name}"
        )

    # Structural immediates that keep the manager object identity and +0x24 map
    # binding from becoming prose-only claims.
    def u32_at(va: int) -> int:
        return struct.unpack_from("<I", image, va_to_offset(va, sections))[0]

    if u32_at(0x0040B594) != 0x0102D5A0 or u32_at(0x0040B5B3) != 0x0102D5A0:
        raise RuntimeError("singleton address immediate mismatch")
    if u32_at(0x004A2C1E) != 0x00F152E8:
        raise RuntimeError("FACTION literal immediate mismatch")
    if u32_at(0x004A2D19) != 0x00F0C958:
        raise RuntimeError("n_ID literal immediate mismatch")
    if u32_at(0x004A2DC4) != 0x00F1527C:
        raise RuntimeError("s_ENEMY literal immediate mismatch")
    if u32_at(0x004A2CCF) != 0x00F1528C:
        raise RuntimeError("delimiter literal immediate mismatch")
    numeric_call_offset = va_to_offset(0x004319A0, sections)
    if (
        image[numeric_call_offset] != 0xFF
        or image[numeric_call_offset + 1] != 0x15
        or u32_at(0x004319A2) != 0x00C3B52C
    ):
        raise RuntimeError("numeric helper _wtoi indirect-call anchor mismatch")


def decode_pcz(raw: bytes) -> bytes:
    if len(raw) < 13 or raw[:4] != b"$pcz":
        raise RuntimeError("CONSTDATA is not a $pcz/raw-LZMA asset")
    expected_size = struct.unpack_from("<I", raw, 4)[0]
    prop = raw[8]
    if prop >= 9 * 5 * 5:
        raise RuntimeError("invalid LZMA property byte")
    lc = prop % 9
    rest = prop // 9
    lp = rest % 5
    pb = rest // 5
    dictionary = struct.unpack_from("<I", raw, 9)[0]
    if dictionary == 0:
        raise RuntimeError("zero LZMA dictionary")
    decoder = lzma.LZMADecompressor(
        format=lzma.FORMAT_RAW,
        filters=[
            {
                "id": lzma.FILTER_LZMA1,
                "lc": lc,
                "lp": lp,
                "pb": pb,
                "dict_size": dictionary,
            }
        ],
    )
    decoded = decoder.decompress(raw[13:], max_length=expected_size + 1)
    if len(decoded) != expected_size:
        raise RuntimeError(
            f"decoded size mismatch: expected {expected_size}, got {len(decoded)}"
        )
    if len(decoded) != CONSTDATA_DECODED_SIZE:
        raise RuntimeError("pinned decoded CONSTDATA size mismatch")
    actual = sha256_bytes(decoded)
    if actual != CONSTDATA_DECODED_SHA256:
        raise RuntimeError(
            f"decoded CONSTDATA hash mismatch: expected {CONSTDATA_DECODED_SHA256}, got {actual}"
        )
    return decoded


def parse_faction_table(decoded: bytes) -> FactionTable:
    def u32(position: int) -> tuple[int, int]:
        if position + 4 > len(decoded):
            raise RuntimeError(f"u32 past decoded EOF at 0x{position:X}")
        return struct.unpack_from("<I", decoded, position)[0], position + 4

    def utf16(position: int, byte_length: int) -> tuple[str, int]:
        end = position + byte_length
        if end > len(decoded) or byte_length % 2:
            raise RuntimeError(f"invalid UTF-16 span at 0x{position:X}")
        return decoded[position:end].decode("utf-16le"), end

    position = 0
    table_count, position = u32(position)
    if table_count != 120:
        raise RuntimeError(f"CONSTDATA table count mismatch: {table_count}")
    faction: FactionTable | None = None
    for index in range(table_count):
        start = position
        name_length, position = u32(position)
        name, position = utf16(position, name_length)
        serialized_size, position = u32(position)
        version, position = u32(position)
        flags_position = position
        flags_value, position = u32(position)
        column_count, position = u32(position)
        flags: int | str = flags_value
        if column_count > 512:
            position = flags_position
            linked_length, position = u32(position)
            flags, position = utf16(position, linked_length)
            column_count, position = u32(position)
        if column_count > 512:
            raise RuntimeError(f"implausible column count in table {index}")
        columns: list[tuple[str, int, int, int]] = []
        for _ in range(column_count):
            column_name_length, position = u32(position)
            column_name, position = utf16(position, column_name_length)
            column_type, position = u32(position)
            column_size, position = u32(position)
            column_offset, position = u32(position)
            columns.append(
                (column_name, column_type, column_size, column_offset)
            )
        row_count, position = u32(position)
        retained_rows: list[tuple[int, str, int, int]] = []
        for _ in range(row_count):
            row_start = position
            values: list[int | float | str] = []
            for column_name, column_type, column_size, _ in columns:
                if column_type == 3:
                    value_length, position = u32(position)
                    value, position = utf16(position, value_length)
                else:
                    end = position + column_size
                    if end > len(decoded):
                        raise RuntimeError(
                            f"row past decoded EOF at 0x{position:X}: {column_name}"
                        )
                    raw_value = decoded[position:end]
                    position = end
                    if column_type == 2 and column_size == 4:
                        value = struct.unpack("<f", raw_value)[0]
                    elif column_size in (1, 2, 4, 8):
                        value = int.from_bytes(raw_value, "little")
                    else:
                        # Retain only a digest-like marker for unused opaque columns.
                        value = f"opaque_size_{column_size}"
                values.append(value)
            if name == "FACTION":
                if len(values) != 2 or not isinstance(values[0], int) or not isinstance(values[1], str):
                    raise RuntimeError("FACTION row shape mismatch")
                retained_rows.append((values[0], values[1], row_start, position))
        if name == "FACTION":
            if faction is not None:
                raise RuntimeError("duplicate FACTION table")
            faction = FactionTable(
                index,
                start,
                position,
                serialized_size,
                version,
                flags,
                tuple(columns),
                tuple(retained_rows),
            )
    if position != 0x0080D3E6 or len(decoded) - position != 146:
        raise RuntimeError(
            f"decoded table traversal mismatch: end=0x{position:X} trailing={len(decoded)-position}"
        )
    if faction is None:
        raise RuntimeError("FACTION table not found")
    if (
        faction.index != 85
        or faction.start != 0x007C5046
        or faction.end != 0x007C52C0
        or faction.serialized_size != 37
        or faction.version != 5
        or faction.flags != 0
        or faction.columns
        != (("n_ID", 0, 4, 0), ("s_ENEMY", 3, 4, 4))
        or len(faction.rows) != 38
    ):
        raise RuntimeError("FACTION table metadata mismatch")
    if sha256_bytes(decoded[faction.start : faction.end]) != (
        "29593eef0e789a0503b19ffa161d26e531d9b7fbebf0a2bcd7c02f1001c04604"
    ):
        raise RuntimeError("FACTION table span hash mismatch")
    by_id = {row[0]: row for row in faction.rows}
    if len(by_id) != 38:
        raise RuntimeError("FACTION n_ID is not unique")
    expected_rows = {
        1: (
            "6;11;12;17;18;26",
            0x007C50A2,
            0x007C50CA,
            "552f61e15b7c77814f67665ba52001be59a9deb3152459ec78a935475e8eba1c",
        ),
        6: (
            "1;2;3;12;13;18",
            0x007C50FA,
            0x007C511E,
            "3df69f3b31c904528edd631f1ecab572dd0a293f0a3117af01f3e9a7ce898f4b",
        ),
    }
    for faction_id, (enemies, start, end, digest) in expected_rows.items():
        actual_id, actual_enemies, actual_start, actual_end = by_id[faction_id]
        if (
            actual_id != faction_id
            or actual_enemies != enemies
            or actual_start != start
            or actual_end != end
            or sha256_bytes(decoded[start:end]) != digest
        ):
            raise RuntimeError(f"FACTION row {faction_id} mismatch")
    return faction


def verify_palette() -> dict[int, tuple[str, str]]:
    raw = read_pinned(FONT_STYLE_PATH, FONT_STYLE_SIZE, FONT_STYLE_SHA256)
    root = ET.fromstring(raw)
    children = list(root)
    if root.tag != "FontStyleList" or len(children) != 186:
        raise RuntimeError("BigFontStyle root/count mismatch")
    ids = [int(child.attrib["ID"]) for child in children]
    if ids != list(range(1, 187)):
        raise RuntimeError("BigFontStyle ordered ID census mismatch")
    actual = {
        int(child.attrib["ID"]): (
            child.attrib.get("FontColor", ""),
            child.attrib.get("OutlineEffectColor", ""),
        )
        for child in children
    }
    expected = {
        56: ("(255, 62, 255, 255)", "(136, 2, 5, 255)"),
        61: ("(255, 100, 100, 255)", "(150, 0, 0, 255)"),
        62: ("(255, 159, 113, 255)", "(91, 30, 0, 255)"),
        63: ("(179, 179, 179, 255)", "(60, 60, 60, 255)"),
    }
    for style_id, pair in expected.items():
        if actual.get(style_id) != pair:
            raise RuntimeError(f"BigFontStyle ID {style_id} mismatch")
    return expected


def verify_prior_gate() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    raw = read_pinned(PRIOR_GATE_PATH, PRIOR_GATE_SIZE, PRIOR_GATE_SHA256)
    with io.StringIO(raw.decode("utf-8"), newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 66:
        raise RuntimeError(f"prior gate row count mismatch: {len(rows)}")
    by_key = {row["gate_key"]: row for row in rows}
    if len(by_key) != len(rows):
        raise RuntimeError("prior gate contains duplicate gate_key")
    for gate_key, evidence_key in PRIOR_REFERENCES.items():
        row = by_key.get(gate_key)
        if row is None or row.get("evidence_key") != evidence_key:
            raise RuntimeError(f"prior gate reference mismatch: {gate_key}")
        expected_source = "DATA" if gate_key.startswith("MCG-DATA-") else "IMAGE"
        if row.get("source") != expected_source:
            raise RuntimeError(f"prior gate source mismatch: {gate_key}")
    return rows, by_key


def ref(*gate_keys: str) -> str:
    return ";".join(f"{key}@{PRIOR_REFERENCES[key]}" for key in gate_keys)


def row_evidence_key(row: Mapping[str, str]) -> str:
    parts = ["PF_MONSTER_COLOR_MECHANISM_JOIN_V1"]
    # Publication generation is deliberately excluded: republishing the same
    # eight facts must not manufacture new evidence identities.
    parts.extend(
        row[name]
        for name in FIELDNAMES
        if name not in {"pair_generation_sha256", "evidence_key"}
    )
    return sha256_bytes("\x00".join(parts).encode("utf-8"))


def make_image_row(
    sections: Sequence[Section],
    *,
    join_key: str,
    row_kind: str,
    subject: str,
    input_or_key: str,
    condition: str,
    output: str,
    producer_va: str,
    consumer_va: str,
    primary_span: str,
    support: Sequence[str] = (),
    prior_reference: str = "",
    nonclaim: str = "",
    blocker: str = "",
    required_next_evidence: str = "",
) -> dict[str, str]:
    start_va, end_va, start_off, end_off, digest = span_locator(
        primary_span, sections
    )
    row = {
        "join_key": join_key,
        "row_kind": row_kind,
        "subject": subject,
        "input_or_key": input_or_key,
        "condition": condition,
        "output": output,
        "semantic_status": "PROVEN_EXACT",
        "producer_va": producer_va,
        "consumer_va": consumer_va,
        "span_start_va": start_va,
        "span_end_va": end_va,
        "file_off_start": start_off,
        "file_off_end": end_off,
        "decoded_off_start": "",
        "decoded_off_end": "",
        "span_sha256": digest,
        "support_spans": ";".join(support_locator(name, sections) for name in support),
        "prior_reference": prior_reference,
        "source": "IMAGE",
        "source_file": IMAGE_SOURCE,
        "source_locator": (
            f"VA:{start_va}..{end_va};file:{start_off}..{end_off};span={primary_span}"
        ),
        "source_size": str(IMAGE_SIZE),
        "source_sha256": IMAGE_SHA256,
        "image_sha256": IMAGE_SHA256,
        "pair_generation_sha256": PAIR_PLACEHOLDER,
        "nonclaim": nonclaim,
        "blocker": blocker,
        "required_next_evidence": required_next_evidence,
        "evidence_key": "",
    }
    row["evidence_key"] = row_evidence_key(row)
    return row


def make_data_row(
    *,
    join_key: str,
    faction_id: int,
    enemies: str,
    start: int,
    end: int,
    digest: str,
    nonclaim: str,
) -> dict[str, str]:
    row = {
        "join_key": join_key,
        "row_kind": "FACTION_DATA_ROW",
        "subject": "FACTION.s_ENEMY",
        "input_or_key": f"n_ID={faction_id}",
        "condition": f"decoded_FACTION_row_key_equals_{faction_id}",
        "output": f"s_ENEMY={enemies}",
        "semantic_status": "PROVEN_EXACT",
        "producer_va": "",
        "consumer_va": "",
        "span_start_va": "",
        "span_end_va": "",
        "file_off_start": "",
        "file_off_end": "",
        "decoded_off_start": f"0x{start:08X}",
        "decoded_off_end": f"0x{end:08X}",
        "span_sha256": digest,
        "support_spans": (
            "FACTION_table=decoded:0x007C5046..0x007C52C0"
            "@sha256:29593eef0e789a0503b19ffa161d26e531d9b7fbebf0a2bcd7c02f1001c04604"
        ),
        "prior_reference": "",
        "source": "DATA",
        "source_file": CONSTDATA_SOURCE,
        "source_locator": (
            f"decoded_in_memory:0x{start:08X}..0x{end:08X};"
            "table_index=85;table=FACTION;columns=n_ID,s_ENEMY"
        ),
        "source_size": str(CONSTDATA_SIZE),
        "source_sha256": CONSTDATA_SHA256,
        "image_sha256": "",
        "pair_generation_sha256": PAIR_PLACEHOLDER,
        "nonclaim": nonclaim,
        "blocker": "",
        "required_next_evidence": "",
        "evidence_key": "",
    }
    row["evidence_key"] = row_evidence_key(row)
    return row


def build_rows(
    sections: Sequence[Section], faction: FactionTable
) -> list[dict[str, str]]:
    by_id = {row[0]: row for row in faction.rows}
    rows = [
        make_image_row(
            sections,
            join_key="MCMJ-IMG-001",
            row_kind="FACTION_MANAGER_BINDING",
            subject="FACTION_manager_singleton",
            input_or_key="singleton_va=0x0102D5A0;manager_map_offset=0x24",
            condition=(
                "singleton_first_use_calls_0x004A4B00;constructor_initializes_plus_0x24_map;"
                "same_this_calls_0x004A2BB0;comparator_reads_same_this_plus_0x24"
            ),
            output="FACTION_loader_and_0x004A1D50_share_one_manager_map_at_plus_0x24",
            producer_va="0x0040B5A0;0x004A4C23;0x004A2D9D",
            consumer_va="0x004A1D57",
            primary_span="manager_constructor",
            support=("singleton_getter", "faction_loader", "faction_comparator"),
            nonclaim=(
                "This is IMAGE object/map identity. It does not prove that startup loading "
                "succeeded in any live process or that a particular DATA row exists."
            ),
            required_next_evidence=(
                "Runtime observation is required only to prove live loader success and map contents."
            ),
        ),
        make_image_row(
            sections,
            join_key="MCMJ-IMG-002",
            row_kind="FACTION_LOADER_SEMANTICS",
            subject="FACTION_table_loader",
            input_or_key="table=FACTION;key=n_ID;value=s_ENEMY;delimiter=semicolon_tab_tab",
            condition=(
                "record_has_n_ID;record_has_s_ENEMY;token_parser_returns_entries;"
                "numeric_token_helper_calls_MSVCR90.dll!_wtoi;converted_value_nonzero"
            ),
            output="n_ID_keys_outer_map_and_each_nonzero_s_ENEMY_token_is_inserted_into_row_set",
            producer_va="0x004A2C1D;0x004A2D18;0x004A2DC3;0x004A2DF8;0x004A2E1E",
            consumer_va="0x004A2DAD;0x004A2E3B",
            primary_span="faction_loader",
            support=(
                "faction_record_constructor",
                "token_parser",
                "numeric_token_helper",
                "set_insert",
            ),
            nonclaim=(
                "This names loader behavior from IMAGE literals and control flow. It does not "
                "assert any shipped row value; DATA rows are separate evidence."
            ),
        ),
        make_image_row(
            sections,
            join_key="MCMJ-IMG-003",
            row_kind="FACTION_COMPARATOR_SEMANTICS",
            subject="function_0x004A1D50",
            input_or_key="arg1=faction_row_key;arg2=candidate_relation_id",
            condition="manager_plus_0x24_lookup_then_record_set_lookup",
            output=(
                "returns_false_iff_arg1_row_exists_with_nonnull_record_and_arg2_is_found_in_its_set;"
                "returns_true_for_missing_row_null_record_or_set_miss"
            ),
            producer_va="0x004A1D66;0x004A1DC0",
            consumer_va="0x004A1DF2;0x004A1E0B",
            primary_span="faction_comparator",
            support=("set_find",),
            nonclaim=(
                "The boolean is a low-level membership-negation result. This row does not by "
                "itself name true friendly or false hostile outside its proven callers."
            ),
        ),
        make_image_row(
            sections,
            join_key="MCMJ-IMG-004",
            row_kind="RELATION_FALLBACK_ARGUMENT_BINDING",
            subject="relation_predicate_0x0043C380_fallback",
            input_or_key=(
                "local_resolved_attribute_plus_0x68;target_resolved_attribute_plus_0x68"
            ),
            condition=(
                "execution_reaches_0x0043C5C9_after_all_earlier_relation_overrides;"
                "target_value_pushed_then_local_value_pushed"
            ),
            output="0x004A1D50_is_called_as_arg1_local_plus_0x68_arg2_target_plus_0x68",
            producer_va="0x0043C5CD;0x0043C5D4;0x0043C5D7;0x0043C5D8",
            consumer_va="0x0043C5E0",
            primary_span="relation_fallback",
            support=("relation_predicate_full", "faction_comparator"),
            nonclaim=(
                "This is a conditional fallback, not the whole relation predicate. Earlier "
                "exits and overrides can return without consulting FACTION. This artifact does "
                "not independently re-prove which server wire field populates either runtime slot."
            ),
            blocker=(
                "A faction pair alone is not an unconditional predictor unless the earlier "
                "0x0043C380 branches and live slot values are also known."
            ),
            required_next_evidence=(
                "Runtime correlate the two resolved +0x68 values and the taken relation branch "
                "for the same local player and target actor."
            ),
        ),
        make_image_row(
            sections,
            join_key="MCMJ-IMG-005",
            row_kind="RELATION_TO_STYLE_JOIN",
            subject="CNetNPC_name_style_selector_0x00443F50",
            input_or_key="signed_positive_actor_identity;relation_predicate_result=false",
            condition=(
                "identity_high_dword_greater_than_zero_or_high_zero_with_low_nonzero;"
                "0x0043C380_result_false;selector_and_controller_gates_pass"
            ),
            output=(
                "the_same_relation_result_reaches_push_FontStyleID_56_then_the_common_"
                "controller_vslot_plus_0x34_style_sink"
            ),
            producer_va="0x00444018;0x00444035;0x00444039",
            consumer_va="0x00444272;0x009F1A70",
            primary_span="selector_positive_relation_lane",
            support=(
                "relation_fallback",
                "faction_comparator",
                "selector_common_style_sink",
            ),
            prior_reference=ref(
                "MCG-IMG-025",
                "MCG-IMG-045",
                "MCG-IMG-051",
                "MCG-IMG-052",
                "MCG-IMG-053",
                "MCG-IMG-054",
                "MCG-IMG-055",
                "MCG-IMG-057",
                "MCG-IMG-058",
            ),
            nonclaim=(
                "[MEASURED][IMAGE] The new fact is the upstream comparator-to-selector join. "
                "The existing style "
                "sink, UILabel, registry, and renderer facts are referenced, not copied. False "
                "can also arise from earlier relation branches, so Style56 is not unique proof "
                "that FACTION membership caused the result. This row does not prove that the "
                "fallback ran, or that Style56 was requested, applied, or rendered in SCENE-005; "
                "it therefore does not establish the measured cause of SCENE-005."
            ),
            blocker=(
                "SCENE-005 cause is OPEN. Live loader success, fallback/result, selector call "
                "gates, requested and applied ID, registry node lookup, draw traversal, and "
                "framebuffer pixels remain runtime facts."
            ),
            required_next_evidence=(
                "One same-actor SCENE-005 trace proving fallback, relation result, requested "
                "FontStyleID, applied UILabel FontStyleID/style pointer, draw dispatch, and pixels."
            ),
        ),
        make_image_row(
            sections,
            join_key="MCMJ-IMG-006",
            row_kind="SELECTOR_LANE_BOUNDARY",
            subject="CNetNPC_selector_styles_61_62_63",
            input_or_key="signed_nonpositive_actor_identity_lane_in_audited_selector",
            condition=(
                "identity_high_dword_negative_or_identity_pair_zero;relation_false;"
                "then_death_offensive_unnamed_bit_and_local_state_conditions_select_subbranches"
            ),
            output=(
                "within_this_selector_path_Style63_is_one_gray_branch_Style61_is_offensive_or_"
                "latched_branch_and_Style62_is_clear_branch;FACTION_membership_alone_does_not_"
                "select_61_62_or_63"
            ),
            producer_va="0x00444151;0x0044419F;0x00444234;0x00444263;0x00444270",
            consumer_va="0x0044427D;0x009F1A70",
            primary_span="selector_nonpositive_lane",
            support=("selector_primary", "selector_common_style_sink"),
            prior_reference=ref(
                "MCG-IMG-030",
                "MCG-IMG-031",
                "MCG-IMG-032",
                "MCG-IMG-033",
                "MCG-IMG-045",
            ),
            nonclaim=(
                "The signed-nonpositive requirement is limited to the audited 0x00443F50 "
                "selector path. Style63 and Style61 have additional causes in that path."
            ),
            blocker=(
                "Static IMAGE does not establish a safe original-server actor identity/state "
                "carrier that enters this lane while preserving object registry/lifecycle."
            ),
            required_next_evidence=(
                "Prove the original actor-entry identity policy and same-actor runtime transitions "
                "for death, offensive state, unnamed bit 0x100, and local-state gates."
            ),
        ),
    ]

    faction_1 = by_id[1]
    faction_6 = by_id[6]
    rows.extend(
        [
            make_data_row(
                join_key="MCMJ-DATA-001",
                faction_id=1,
                enemies=faction_1[1],
                start=faction_1[2],
                end=faction_1[3],
                digest=(
                    "552f61e15b7c77814f67665ba52001be59a9deb3152459ec78a935475e8eba1c"
                ),
                nonclaim=(
                    "This is a DATA row value. It does not prove the loader ran, that live local "
                    "slot +0x68 equals 1, or that relation execution reached its FACTION fallback."
                ),
            ),
            make_data_row(
                join_key="MCMJ-DATA-002",
                faction_id=6,
                enemies=faction_6[1],
                start=faction_6[2],
                end=faction_6[3],
                digest=(
                    "3df69f3b31c904528edd631f1ecab572dd0a293f0a3117af01f3e9a7ce898f4b"
                ),
                nonclaim=(
                    "This proves reverse membership 6->1 in DATA. The audited call direction for "
                    "a local faction 1 and target faction 6 is row 1, not row 6."
                ),
            ),
        ]
    )
    return rows


def validate_rows(
    rows: Sequence[dict[str, str]],
    prior_rows: Sequence[dict[str, str]],
    expected_pair_generation: str,
) -> None:
    if len(rows) != 8:
        raise RuntimeError(f"row count mismatch: {len(rows)}")
    if [row["join_key"] for row in rows] != [
        "MCMJ-IMG-001",
        "MCMJ-IMG-002",
        "MCMJ-IMG-003",
        "MCMJ-IMG-004",
        "MCMJ-IMG-005",
        "MCMJ-IMG-006",
        "MCMJ-DATA-001",
        "MCMJ-DATA-002",
    ]:
        raise RuntimeError("row ordering mismatch")
    if any(set(row) != set(FIELDNAMES) for row in rows):
        raise RuntimeError("row schema mismatch")
    if any("\t" in value or "\r" in value or "\n" in value for row in rows for value in row.values()):
        raise RuntimeError("TSV value contains a control separator")
    if len({row["join_key"] for row in rows}) != len(rows):
        raise RuntimeError("duplicate join_key")
    if len({row["evidence_key"] for row in rows}) != len(rows):
        raise RuntimeError("duplicate evidence_key")
    for row in rows:
        if row["pair_generation_sha256"] != expected_pair_generation:
            raise RuntimeError(
                f"pair generation mismatch in row: {row['join_key']}"
            )
        expected_key = row_evidence_key({**row, "evidence_key": ""})
        if row["evidence_key"] != expected_key:
            raise RuntimeError(f"unstable evidence_key: {row['join_key']}")
        if row["source"] == "IMAGE":
            if (
                row["source_file"] != IMAGE_SOURCE
                or row["source_size"] != str(IMAGE_SIZE)
                or row["source_sha256"] != IMAGE_SHA256
                or row["image_sha256"] != IMAGE_SHA256
                or not row["span_start_va"]
                or not row["file_off_start"]
                or row["decoded_off_start"]
                or row["decoded_off_end"]
            ):
                raise RuntimeError(f"IMAGE provenance mismatch: {row['join_key']}")
        elif row["source"] == "DATA":
            if (
                row["source_file"] != CONSTDATA_SOURCE
                or row["source_size"] != str(CONSTDATA_SIZE)
                or row["source_sha256"] != CONSTDATA_SHA256
                or row["image_sha256"]
                or row["span_start_va"]
                or row["file_off_start"]
                or not row["decoded_off_start"]
            ):
                raise RuntimeError(f"DATA provenance mismatch: {row['join_key']}")
        else:
            raise RuntimeError(f"invalid source: {row['source']}")
        for item in filter(None, row["prior_reference"].split(";")):
            if "@" not in item:
                raise RuntimeError(f"malformed prior reference: {item}")
            gate_key, evidence_key = item.split("@", 1)
            if PRIOR_REFERENCES.get(gate_key) != evidence_key:
                raise RuntimeError(f"unknown prior reference: {item}")

    prior_evidence_keys = {row["evidence_key"] for row in prior_rows}
    if {row["evidence_key"] for row in rows} & prior_evidence_keys:
        raise RuntimeError("new evidence_key duplicates PF_MONSTER_COLOR_GATE")

    # Exact claim-copy guards.  A new join may cite an old fact but must not
    # reproduce the old row as if it were newly derived evidence.
    prior_full_claims = {
        (
            row.get("source", ""),
            row.get("row_kind", ""),
            row.get("input_field", ""),
            row.get("condition", ""),
            row.get("output", ""),
        )
        for row in prior_rows
    }
    prior_core_claims = {
        (row.get("source", ""), row.get("condition", ""), row.get("output", ""))
        for row in prior_rows
    }
    for row in rows:
        full = (
            row["source"],
            row["row_kind"],
            row["input_or_key"],
            row["condition"],
            row["output"],
        )
        core = (row["source"], row["condition"], row["output"])
        if full in prior_full_claims or core in prior_core_claims:
            raise RuntimeError(
                f"row duplicates prior claim instead of referencing it: {row['join_key']}"
            )


def render_tsv(rows: Sequence[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=FIELDNAMES,
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def pair_generation_digest(tsv_template: bytes, report_template: bytes) -> str:
    """Hash the complete normalized two-file publication.

    The templates contain fixed placeholders at the publication-only fields,
    breaking the otherwise circular relationship between the pair marker, the
    final TSV hash printed in Markdown, and the full output bytes.
    """

    digest = hashlib.sha256()
    digest.update(PAIR_DOMAIN)
    for label, raw in ((b"TSV\x00", tsv_template), (b"MD\x00", report_template)):
        digest.update(label)
        digest.update(struct.pack("<Q", len(raw)))
        digest.update(raw)
    return digest.hexdigest()


def parse_published_tsv(raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("published TSV is not UTF-8") from exc
    with io.StringIO(text, newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != FIELDNAMES:
            raise RuntimeError("published TSV header mismatch")
        rows = list(reader)
    if len(rows) != 8:
        raise RuntimeError(f"published TSV row count mismatch: {len(rows)}")
    return rows


def report_marker_value(text: str, prefix: str) -> str:
    matches = [line for line in text.splitlines() if line.startswith(prefix)]
    if len(matches) != 1 or not matches[0].endswith("`."):
        raise RuntimeError(f"report marker census mismatch: {prefix}")
    value = matches[0][len(prefix) : -2]
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise RuntimeError(f"report marker is not lowercase SHA256: {prefix}")
    return value


def verify_causal_wording(report_text: str) -> None:
    compact = " ".join(report_text.split())
    required = (
        "## [COMPOSITION][IMAGE+DATA] Result",
        "**[MEASURED][IMAGE] Mechanism join.**",
        "**[MEASURED][DATA] Membership and palette.**",
        "**[COMPOSITION][IMAGE+DATA] Conditional Style56 explanation.**",
        "sufficient static/data explanation for a Style56 request",
        "not** the measured cause of",
        "cause remains **OPEN**",
        "fallback, relation result, requested ID, applied ID, and resulting pixels",
        "**[OPEN][RUNTIME]**",
    )
    for marker in required:
        if marker not in compact:
            raise RuntimeError(f"required causal wording marker missing: {marker}")
    forbidden = (
        "present pink cause " + "is static-closed enough to diagnose",
        "measured cause of SCENE-005 is closed",
    )
    lowered = compact.lower()
    for phrase in forbidden:
        if phrase.lower() in lowered:
            raise RuntimeError(f"forbidden causal wording present: {phrase}")


def verify_published_pair(
    tsv_raw: bytes,
    report_raw: bytes,
    *,
    expected_pair_generation: str | None = None,
) -> str:
    """Fail closed on a mixed, partial, or internally inconsistent pair."""

    rows = parse_published_tsv(tsv_raw)
    pair_values = {row["pair_generation_sha256"] for row in rows}
    if len(pair_values) != 1:
        raise RuntimeError("TSV contains mixed pair generations")
    pair_generation = next(iter(pair_values))
    if (
        len(pair_generation) != 64
        or any(char not in "0123456789abcdef" for char in pair_generation)
        or pair_generation == PAIR_PLACEHOLDER
    ):
        raise RuntimeError("TSV pair generation is invalid")
    if expected_pair_generation is not None and pair_generation != expected_pair_generation:
        raise RuntimeError(
            "published pair generation differs from the re-derived generation"
        )

    try:
        report_text = report_raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise RuntimeError("published Markdown is not ASCII") from exc
    verify_causal_wording(report_text)
    report_pair = report_marker_value(report_text, PAIR_LINE_PREFIX)
    report_tsv_sha = report_marker_value(report_text, TSV_LINE_PREFIX)
    actual_tsv_sha = sha256_bytes(tsv_raw)
    if report_pair != pair_generation:
        raise RuntimeError("TSV and Markdown carry different pair generations")
    if report_tsv_sha != actual_tsv_sha:
        raise RuntimeError("Markdown TSV hash does not match the published TSV")

    normalized_rows = [dict(row) for row in rows]
    for row in normalized_rows:
        row["pair_generation_sha256"] = PAIR_PLACEHOLDER
    normalized_tsv = render_tsv(normalized_rows)

    pair_line = f"{PAIR_LINE_PREFIX}{pair_generation}`."
    pair_placeholder_line = f"{PAIR_LINE_PREFIX}{PAIR_PLACEHOLDER}`."
    tsv_line = f"{TSV_LINE_PREFIX}{report_tsv_sha}`."
    tsv_placeholder_line = f"{TSV_LINE_PREFIX}{TSV_SHA_PLACEHOLDER}`."
    if report_text.count(pair_line) != 1 or report_text.count(tsv_line) != 1:
        raise RuntimeError("published Markdown marker replacement is ambiguous")
    normalized_report_text = report_text.replace(
        pair_line, pair_placeholder_line, 1
    ).replace(tsv_line, tsv_placeholder_line, 1)
    normalized_report = normalized_report_text.encode("ascii")
    recomputed = pair_generation_digest(normalized_tsv, normalized_report)
    if recomputed != pair_generation:
        raise RuntimeError("normalized full TSV+Markdown pair digest mismatch")
    return pair_generation


def build_publication_pair(
    rows_with_placeholder: Sequence[dict[str, str]],
    prior_rows: Sequence[dict[str, str]],
) -> tuple[list[dict[str, str]], bytes, bytes, str]:
    validate_rows(rows_with_placeholder, prior_rows, PAIR_PLACEHOLDER)
    tsv_template = render_tsv(rows_with_placeholder)
    report_template = render_report(
        rows_with_placeholder,
        TSV_SHA_PLACEHOLDER,
        PAIR_PLACEHOLDER,
    )
    pair_generation = pair_generation_digest(tsv_template, report_template)

    rows = [dict(row) for row in rows_with_placeholder]
    for row in rows:
        row["pair_generation_sha256"] = pair_generation
    validate_rows(rows, prior_rows, pair_generation)
    tsv_raw = render_tsv(rows)
    report_raw = render_report(rows, sha256_bytes(tsv_raw), pair_generation)
    verified = verify_published_pair(
        tsv_raw, report_raw, expected_pair_generation=pair_generation
    )
    if verified != pair_generation:
        raise RuntimeError("internal pair verification mismatch")
    return rows, tsv_raw, report_raw, pair_generation


def output_stat_signature(path: Path) -> tuple[int, int, int, int, int]:
    stat = path.stat()
    return (
        stat.st_dev,
        stat.st_ino,
        stat.st_size,
        stat.st_mtime_ns,
        stat.st_ctime_ns,
    )


def stable_read_published_pair() -> tuple[bytes, bytes]:
    """Read both outputs twice, in opposite order, under the publication lock."""

    paths = (TSV_PATH, REPORT_PATH)
    if any(not path.is_file() for path in paths):
        missing = ",".join(path.name for path in paths if not path.is_file())
        raise RuntimeError(f"missing generated output: {missing}")
    before = tuple(output_stat_signature(path) for path in paths)
    first_tsv = TSV_PATH.read_bytes()
    first_report = REPORT_PATH.read_bytes()
    middle = tuple(output_stat_signature(path) for path in paths)
    second_report = REPORT_PATH.read_bytes()
    second_tsv = TSV_PATH.read_bytes()
    after = tuple(output_stat_signature(path) for path in paths)
    if (
        before != middle
        or middle != after
        or first_tsv != second_tsv
        or first_report != second_report
    ):
        raise RuntimeError("published output pair changed during stable reread")
    return first_tsv, first_report


@contextmanager
def exclusive_publication_lock(timeout_seconds: float = 10.0) -> Iterator[None]:
    """Lock byte zero of this owned generator without creating a fourth file."""

    handle = LOCK_TARGET_PATH.open("r+b", buffering=0)
    locked = False
    deadline = time.monotonic() + timeout_seconds
    try:
        if os.name == "nt":
            import msvcrt

            while True:
                try:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    locked = True
                    break
                except OSError as exc:
                    if time.monotonic() >= deadline:
                        raise RuntimeError(
                            "exclusive publication lock timeout"
                        ) from exc
                    time.sleep(0.05)
        else:
            import fcntl

            while True:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    locked = True
                    break
                except OSError as exc:
                    if time.monotonic() >= deadline:
                        raise RuntimeError(
                            "exclusive publication lock timeout"
                        ) from exc
                    time.sleep(0.05)
        yield
    finally:
        try:
            if locked:
                if os.name == "nt":
                    import msvcrt

                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()


def stage_output(path: Path, raw: bytes) -> Path:
    descriptor, staged_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".stage", dir=path.parent
    )
    staged_path = Path(staged_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if staged_path.read_bytes() != raw:
            raise RuntimeError(f"staged output verification failed: {path.name}")
        return staged_path
    except Exception:
        try:
            staged_path.unlink(missing_ok=True)
        finally:
            raise


def publish_output_pair(tsv_raw: bytes, report_raw: bytes, pair_generation: str) -> None:
    """Stage both files, verify the pair, then atomically replace each target."""

    staged_tsv: Path | None = None
    staged_report: Path | None = None
    try:
        staged_tsv = stage_output(TSV_PATH, tsv_raw)
        staged_report = stage_output(REPORT_PATH, report_raw)
        verify_published_pair(
            staged_tsv.read_bytes(),
            staged_report.read_bytes(),
            expected_pair_generation=pair_generation,
        )

        # Each replace is atomic.  A process failure between the two replacements
        # is intentionally detectable as a generation/hash mismatch, never as a
        # silently accepted pair.  Cooperative readers hold the same lock.
        os.replace(staged_tsv, TSV_PATH)
        staged_tsv = None
        os.replace(staged_report, REPORT_PATH)
        staged_report = None

        actual_tsv, actual_report = stable_read_published_pair()
        verify_published_pair(
            actual_tsv,
            actual_report,
            expected_pair_generation=pair_generation,
        )
        if actual_tsv != tsv_raw or actual_report != report_raw:
            raise RuntimeError("post-publication exact-byte verification failed")
    finally:
        if staged_tsv is not None:
            staged_tsv.unlink(missing_ok=True)
        if staged_report is not None:
            staged_report.unlink(missing_ok=True)


def render_report(
    rows: Sequence[dict[str, str]],
    tsv_sha256: str,
    pair_generation_sha256: str,
) -> bytes:
    refs = {key: f"{key}@{value}" for key, value in PRIOR_REFERENCES.items()}
    image_rows = sum(row["source"] == "IMAGE" for row in rows)
    data_rows = sum(row["source"] == "DATA" for row in rows)
    report = f"""# PF Monster Color Mechanism Join

## [COMPOSITION][IMAGE+DATA] Result

**[MEASURED][IMAGE] Mechanism join.** The static join is closed: the `FACTION`
membership comparator is an upstream input to the same CNetNPC name-style
selector and controller/UILabel renderer path.  It is not a separate color
renderer.

**[MEASURED][DATA] Membership and palette.** The shipped DATA row keyed by `1`
contains `6` in `s_ENEMY`.  Existing source-separated palette evidence
{refs['MCG-DATA-001']} defines Style56 as FontColor `(255, 62, 255, 255)` with
outline `(136, 2, 5, 255)`, descriptively magenta/pink.

**[COMPOSITION][IMAGE+DATA] Conditional Style56 explanation.** For live local
value `1` and target value `6`, if `0x0043C380` reaches its FACTION fallback,
the IMAGE call direction is `(local, target)`, `0x004A1D50` returns false for
that DATA membership hit, and a signed-positive target identity makes the
audited selector request FontStyleID **56**.  This conditional
`(1,6) + fallback + positive identity` composition is a sufficient static/data
explanation for a Style56 request.  It is **not** the measured cause of
`SCENE-005`.  That cause remains **OPEN** until one same-actor trace proves the
fallback, relation result, requested ID, applied ID, and resulting pixels.

The composition does **not** make `(1,6)` an unconditional screen-color rule.
The relation function has earlier exits and overrides, loading must succeed,
selector and UI gates must pass, and final pixels are runtime facts.

## Direction and boolean proof

- **[MEASURED][IMAGE]** `MCMJ-IMG-004`: local actor is the `this` receiver; target actor is the
  stack argument.  The fallback resolves each actor's attribute object, reads
  `+0x68`, pushes target then local, and calls the manager as
  `arg1=local+0x68, arg2=target+0x68`.
- **[MEASURED][IMAGE]** `MCMJ-IMG-003`: the comparator returns false only when the row keyed by
  arg1 exists, its record is nonnull, and arg2 is present in that row's set.
- **[MEASURED][DATA]** `MCMJ-DATA-001`: row 1 is exactly `6;11;12;17;18;26`.
- **[MEASURED][DATA]** `MCMJ-DATA-002`: row 6 also contains 1, but that reverse row is not the
  row selected by the audited `(local=1,target=6)` call direction.

These are separate rows because IMAGE control flow and DATA values are separate
evidence layers.  **[COMPOSITION][IMAGE+DATA]** The conditional conclusion above
is their explicit composition, not a mixed-source TSV row and not measured
SCENE-005 causation.

## Selector and renderer join

**[MEASURED][IMAGE]** `MCMJ-IMG-005` adds only the missing upstream edge: the exact result of
`0x0043C380` is consumed inside `0x00443F50`; false in the signed-positive
identity lane pushes ID 56 and reaches the common controller vslot `+0x34`
sink.  The downstream controller store, `LABEL_NAME`/UILabel setter, style
registry, color apply, and renderer ceiling are not copied as new facts.  They
are referenced by their prior keys:

- selector/style edge: {refs['MCG-IMG-025']}
- controller style store: {refs['MCG-IMG-045']}
- UILabel/style apply/render: {refs['MCG-IMG-051']}, {refs['MCG-IMG-052']}, {refs['MCG-IMG-053']}
- BigFontStyle startup/load/color parse: {refs['MCG-IMG-054']}, {refs['MCG-IMG-055']}, {refs['MCG-IMG-057']}, {refs['MCG-IMG-058']}

## Why faction alone is not enough for orange/red/gray

**[MEASURED][IMAGE]** Within the audited `0x00443F50` selector path, IDs 61, 62, and 63 occur after
entry into the signed-nonpositive identity lane and depend on additional death,
offensive, unnamed bit `0x100`, linked-actor, and local-state conditions.  The
exact pre-existing branch references are {refs['MCG-IMG-030']},
{refs['MCG-IMG-031']}, {refs['MCG-IMG-032']}, and {refs['MCG-IMG-033']}.

**[MEASURED][DATA]** Their source-separated palette references are:

- Style61: {refs['MCG-DATA-006']}, descriptive label `red_or_pink_red`, exact
  FontColor `(255, 100, 100, 255)`.
- Style62: {refs['MCG-DATA-007']}, descriptive label `orange_or_salmon`, exact
  FontColor `(255, 159, 113, 255)`.
- Style63: {refs['MCG-DATA-008']}, descriptive label `gray`, exact FontColor
  `(179, 179, 179, 255)`.

**[MEASURED][IMAGE]** The signed-nonpositive boundary is asserted only for this audited selector; it
is not a global claim about every color path in the client.

## Implementation decision and exact blocker

**[COMPOSITION][IMAGE+DATA]** The conditional `(1,6) + fallback + positive
identity` path is a sufficient static/data explanation for the selector to
request Style56.  It is **not** the measured cause of `SCENE-005`.

**[OPEN][RUNTIME]** The `SCENE-005` cause remains **OPEN** until one same-actor
trace proves the fallback, relation result, requested FontStyleID, applied
UILabel FontStyleID/style pointer, draw dispatch, and resulting pixels.  It is
therefore **not yet safe** to implement the intended orange/red/gray behavior
by changing faction alone.

The narrow remaining blockers are:

1. Prove the original actor-entry identity/state carrier that can enter the
   selector's signed-nonpositive lane without breaking actor registry lookup,
   same-object retention, or lifecycle.
2. Prove same-actor runtime transitions for the death predicate, offensive
   predicate, unnamed bit `0x100`, and local-state gates that distinguish IDs
   61/62/63.
3. In one same-actor `SCENE-005` trace, prove fallback, relation result,
   requested FontStyleID, applied controller `+0x34` and UILabel FontStyleID/style
   pointer, draw dispatch, and observed pixels.  This static task did not run
   client, server, dump, or capture.

## Evidence discipline

- New TSV rows: {len(rows)} ({image_rows} IMAGE, {data_rows} DATA).
- Every row has exactly one `source` value.
- IMAGE rows carry file offsets, span hashes, image size, and image SHA256.
- DATA rows carry decoded in-memory offsets and span hashes; decoded bytes are
  never written.
- No new evidence key or exact claim tuple duplicates
  `PF_MONSTER_COLOR_GATE.tsv`; reused facts are cited through `prior_reference`.
- Pair generation SHA256: `{pair_generation_sha256}`.
- TSV SHA256: `{tsv_sha256}`.
- The pair generation covers normalized full TSV and Markdown bytes. Both files
  are staged before per-file atomic replacement under an exclusive byte-range
  lock. A stop between replacements is detectable as a pair/hash mismatch.

## Pinned inputs

| Input | Size | SHA256 |
|---|---:|---|
| GameClient.local.bin | {IMAGE_SIZE} | `{IMAGE_SHA256}` |
| B_CONSTDATA_TH.pc_ | {CONSTDATA_SIZE} | `{CONSTDATA_SHA256}` |
| decoded B_CONSTDATA_TH (memory only) | {CONSTDATA_DECODED_SIZE} | `{CONSTDATA_DECODED_SHA256}` |
| BigFontStyle.fsl | {FONT_STYLE_SIZE} | `{FONT_STYLE_SHA256}` |
| PF_MONSTER_COLOR_GATE.tsv | {PRIOR_GATE_SIZE} | `{PRIOR_GATE_SHA256}` |

## Re-derive

```powershell
py -3 pf_rederive_monster_color_mechanism_join.py --check
```

`--check` holds the publication lock, reads both outputs twice in opposite
orders, verifies their shared normalized pair generation and TSV hash, then
verifies every pinned input, PE layout, span hash, direct-call anchor, import
name, in-memory CONSTDATA parse, palette reference, prior reference, source
separation, duplicate guards, and exact output bytes without writing.
"""
    return report.encode("ascii")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify inputs and exact generated outputs without writing",
    )
    args = parser.parse_args()

    image = read_pinned(IMAGE_PATH, IMAGE_SIZE, IMAGE_SHA256)
    sections = parse_pe_sections(image)
    verify_spans(image, sections)
    verify_static_anchors(image, sections)

    packed_constdata = read_pinned(
        CONSTDATA_PATH, CONSTDATA_SIZE, CONSTDATA_SHA256
    )
    decoded_constdata = decode_pcz(packed_constdata)
    faction = parse_faction_table(decoded_constdata)
    verify_palette()
    prior_rows, _ = verify_prior_gate()

    rows_with_placeholder = build_rows(sections, faction)
    rows, tsv_raw, report_raw, pair_generation = build_publication_pair(
        rows_with_placeholder, prior_rows
    )

    with exclusive_publication_lock():
        if args.check:
            actual_tsv, actual_report = stable_read_published_pair()
            verify_published_pair(
                actual_tsv,
                actual_report,
                expected_pair_generation=pair_generation,
            )
            if actual_tsv != tsv_raw or actual_report != report_raw:
                raise RuntimeError(
                    "published pair differs from exact re-derived output: "
                    f"expected_tsv={sha256_bytes(tsv_raw)} "
                    f"actual_tsv={sha256_bytes(actual_tsv)} "
                    f"expected_md={sha256_bytes(report_raw)} "
                    f"actual_md={sha256_bytes(actual_report)}"
                )
            mode = "check"
        else:
            publish_output_pair(tsv_raw, report_raw, pair_generation)
            mode = "write"

    print(
        "PF_MONSTER_COLOR_MECHANISM_JOIN: PASS "
        f"mode={mode} rows={len(rows)} image_rows=6 data_rows=2 "
        f"pair_generation={pair_generation} "
        f"tsv_sha256={sha256_bytes(tsv_raw)} "
        f"md_sha256={sha256_bytes(report_raw)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            "PF_MONSTER_COLOR_MECHANISM_JOIN: FAIL " + ascii_safe(exc),
            file=sys.stderr,
        )
        raise SystemExit(1)
