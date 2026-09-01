#!/usr/bin/env python3
"""Re-derive the bounded CNetNPC quest-mark event-kind 0x0A census.

The script reads only the pinned client image and two pinned IMAGE-derived
reference TSVs.  Generation publishes PF_QUEST_MARK_EVENT_CENSUS.tsv/.md beside
this script.  ``--check`` is strictly read-only and verifies the complete pair.
Console output is deliberately ASCII-only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import struct
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
TSV_PATH = OUT_DIR / "PF_QUEST_MARK_EVENT_CENSUS.tsv"
REPORT_PATH = OUT_DIR / "PF_QUEST_MARK_EVENT_CENSUS.md"
SELECTOR_PATH = OUT_DIR / "PF_ATTR_QUEST_MARK_SELECTOR.tsv"
GROUND_DROP_PATH = OUT_DIR / "PF_GROUND_DROP_LIFETIME.tsv"
LOCK_PATH = OUT_DIR / ".pf_rederive_quest_mark_event_census.lock"

EXPECTED_IMAGE_SIZE = 14_759_424
EXPECTED_IMAGE_SHA256 = (
    "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
)
EXPECTED_SELECTOR_SIZE = 52_137
EXPECTED_SELECTOR_SHA256 = (
    "3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0"
)
EXPECTED_GROUND_DROP_SIZE = 61_979
EXPECTED_GROUND_DROP_SHA256 = (
    "b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710"
)
SELECTOR_REFERENCE_KEY = (
    "664c81eb05a59bb0661d3390d9f08a7c4f7401360e4bf3840678e4fa10a6f515"
)
GROUND_DROP_REFERENCE_KEY = (
    "b014e9c7797a1d24b5c13eef598b7374223af5b548fe3efda538a43cd65a7d09"
)

SOURCE = "IMAGE"
SOURCE_FILE = "PF_ROOT://GameClient/GameClient.local.bin"
PAIR_PLACEHOLDER = "0" * 64

QUERY_DISPATCHER = 0x005F9F60
GENERAL_DISPATCHER = 0x005F9C70
QUERY_REGISTRATION = 0x005FAE30
GENERAL_REGISTRATION = 0x005FACE0
REGISTRATION_SINGLETON = 0x005FB420
QUERY_PRODUCER = 0x00449F30

EXPECTED_QUERY_REGISTRATION_COUNT = 55
EXPECTED_QUERY_REGISTRATION_DIGEST = (
    "8a5db14dcd8318aa520b3a66122a6ccbf2237fe62b2ad0b4c72ed1dfe81d130c"
)
EXPECTED_GENERAL_REGISTRATION_COUNT = 140
EXPECTED_GENERAL_REGISTRATION_DIGEST = (
    "9f352999fc90400dcba1bda7899c4486eeff3f29ed8b57b7a0ba716f27622a01"
)
EXPECTED_QUERY_DISPATCH_CALL_COUNT = 126
EXPECTED_QUERY_DISPATCH_CALL_DIGEST = (
    "9ff939517c73aeea7578fbbbd3a90041c53eea2bd7cefa9a872bf917b29785f0"
)
EXPECTED_QUERY_IMMEDIATE_COUNT = 123
EXPECTED_QUERY_IMMEDIATE_DIGEST = (
    "db9a9da851738471b617808d60c79442b7dfaeadd80369f48b30510f9780c792"
)
EXPECTED_QUERY_PRODUCER_CALLER_COUNT = 5
EXPECTED_QUERY_PRODUCER_CALLER_DIGEST = (
    "f5f75023e92b381d6182318fbfd4a68f8bff117e7598f7c7e664e91b76093df1"
)
EXPECTED_GENERAL_KIND0A_SITE_DIGEST = (
    "3d14a76ce8a92869740e149e55470b1c53b2900abee06770e4167c7da25d12fd"
)
EXPECTED_GENERAL_VTABLE_DIGEST = (
    "2fb32e37aba1a42cfa8a599e5f5461687032bacf7a120d42194fa95483139b1b"
)
EXPECTED_MANUAL_QUERY_CONTROL_DIGEST = (
    "27745cd957024d2d4e2dc66293d876069fd42b00ec5c454071b19aeefc3a796c"
)


@dataclass(frozen=True)
class Section:
    name: str
    va: int
    file_off: int
    virtual_size: int
    raw_size: int


@dataclass(frozen=True)
class SpanSpec:
    start: int
    end: int
    sha256: str


FIELDNAMES = (
    "event_key",
    "row_kind",
    "channel",
    "receiver_or_owner",
    "event_kind",
    "field_or_slot",
    "operation",
    "semantic_status",
    "measurement_label",
    "exact_observation",
    "census_scope",
    "census_count",
    "census_digest",
    "span_start_va",
    "span_end_va",
    "file_off_start",
    "file_off_end",
    "span_sha256",
    "support_spans",
    "reference_artifact",
    "reference_sha256",
    "reference_keys",
    "source",
    "source_file",
    "source_size",
    "source_sha256",
    "nonclaim",
    "blocker",
    "required_next_evidence",
    "artifact_pair_sha256",
    "claim_sha256",
    "evidence_key",
)


# End VAs are exclusive.  The whole-image guard and every span hash must agree.
SPANS: Mapping[str, SpanSpec] = {
    "event_ctor_fields": SpanSpec(0x005F8D43, 0x005F8D84, "e323b02cb58d9177021389b7979707b3c0b395b79f0c553c94226f00fd178b67"),
    "query_producer_seed_dispatch": SpanSpec(0x00449F65, 0x00449FB2, "bdb0c1ea808213b606ae11a03077caa3f19634abf452d8c83ef4b9e3e61f2105"),
    "query_producer_read_destroy": SpanSpec(0x00449FB2, 0x00449FD9, "be082bdd71752f0ef7af66e492e0323692fb3489d919b1cc06078d3c9899331a"),
    "caller_5250": SpanSpec(0x005250AC, 0x005250BA, "44121e7b9bab1c1a781c7de635a0cf75b4e11f56e3c0e5d9e4909cf3db58269a"),
    "caller_5286": SpanSpec(0x00528684, 0x0052869A, "ff801d12334fb4d05a201ad24871ea62f11621808ae03253efd225d456df8089"),
    "caller_52c2": SpanSpec(0x0052C252, 0x0052C26A, "78a5c0c5c417098b93a82ea122d3405f148db4d4faa516596a6304530cd90e7d"),
    "caller_52e9": SpanSpec(0x0052E923, 0x0052E93A, "127c73cf7bf323d68d6bde2582bb4784e72c7a88c7645464d48a28cfc609432f"),
    "cnetnpc_call": SpanSpec(0x006167C1, 0x006167D6, "0a5e60bc2cba49956fa2592f9e40339d0598f4810c3f690ad5a652cf02a459c5"),
    "query_registration": SpanSpec(0x00615BE0, 0x00615C30, "03506f8b0fdff5c778c2c39b838339f037f8b42262b915fbf6ade250f5777d94"),
    "quest_vtable_query_bind": SpanSpec(0x00F33454, 0x00F33468, "ae0b8656f2331265530a2f951b5934c7ff21e4483396aa589d1f31a349334208"),
    "quest_query_writer": SpanSpec(0x0061A8D9, 0x0061A8F9, "23760a6bf4f48487b1402ee8be1ea47eecc508e8ff8f42e6d1eea1027a1c19af"),
    "query_dispatcher": SpanSpec(0x005F9F60, 0x005FA011, "0159308f02b759596a41e8aabed34c1d6779940c4208ba03b8e01c8195044296"),
    "query_unique_immediate": SpanSpec(0x00449FA1, 0x00449FB2, "ce6035e5baf5dcc4eabf6d82c1f54d1df920b0f2c467fd671e064b1bbf39abe7"),
    "dynamic_5002": SpanSpec(0x0050023F, 0x00500313, "51702ba32490e2a7654b5c7e3f82329969d011ad40392044e377866a2f6c5ec9"),
    "dynamic_6e2c": SpanSpec(0x006E2BF0, 0x006E2D25, "8fa57f017cfcb58be2f07c49baf09389ceb096d9fb68b83f8b8196ef48d2ee97"),
    "dynamic_75b0": SpanSpec(0x0075B003, 0x0075B177, "c784a300e49d3e8f0630379c34be71927fb613be5069f6e8b1e607495b705ef0"),
    "module_add": SpanSpec(0x005FB824, 0x005FB8F1, "601816c0f3b27df99ec15a05cad3556bf23eb032516c9c7373d890ef9861c98c"),
    "module_unregister": SpanSpec(0x005FB607, 0x005FB795, "641b1014666172cf4dd224e25e100365e0d7b9130270f11571b39a02e3fac013"),
    "general_quest_registration": SpanSpec(0x00615B40, 0x00615BDB, "0c032a900d640e57d5a441ff38e45cbf44b8e3c8b089ac71dca1c30995aa9cf6"),
    "general_shared_registration": SpanSpec(0x006E4600, 0x006E4623, "32be57dcdfcfb572d2b207759e7d5d1f10e1d0c4c7ce7a681c891394ac81b123"),
    "general_6ecc_registration": SpanSpec(0x006ECC30, 0x006ECC53, "22d705a0ac05f1d11b879b01fcc621244458f65f797ab2e60fcbcf69d8c0c23d"),
    "general_6f9c_registration": SpanSpec(0x006F9C30, 0x006F9C80, "801d5400833469b57ee3e700da821a42426e8feb6bdf49e15e58b49c95a64c2b"),
    "general_70f2_registration": SpanSpec(0x0070F2D0, 0x0070F302, "135cce1eccf83c304a52abe04aa5ed7a047f4ab99432b6003ba6f5322953d916"),
    "general_7304_registration": SpanSpec(0x00730470, 0x007304C0, "3320c21b46ff7ca8014090c0422bae5e7a1455fd2b8b65d9e00ee2db4dd2e167"),
    "general_73e7_registration": SpanSpec(0x0073E7B0, 0x0073E7E2, "fca3126afd2f3feff76c343e8d2663116aa2e9c508ee7ecd75aa42b82d6b3da8"),
    "general_7424_registration": SpanSpec(0x00742480, 0x007424C1, "2a130b8ea1b53235a1789cbfe77f5f9e2a107971bc7b76f1cca69b95ecc88df9"),
    "general_dispatcher": SpanSpec(0x005F9C70, 0x005F9D05, "39f8721e4ebaf8bec765520e35c6e5cc350cf9cc9e2e88163142cf08e3e7e603"),
    "ground_drop_vtable_bind": SpanSpec(0x00F3DD5C, 0x00F3DD7C, "6fad45f0236af30741f4dcb57669b2033917de313357a1a28459b9f35f29acc5"),
    "general_kind0a_producer": SpanSpec(0x005F6D08, 0x005F6D5E, "545e60a77701c14bd5dde30a104b2cd9e95e50b6e660acb4e9546f6517d278e7"),
    "query_registry_insert": SpanSpec(0x005FAE30, 0x005FAF77, "749b645653080d3cf860a084f27e5b5c2ce273eb4ed87879f2d385ff62dbb2f2"),
    "general_vtable_00f33420": SpanSpec(0x00F33444, 0x00F33464, "575e6c2fe7e841af59974745ad9e8e503f53c6308a9511a13b960cfeae5b6616"),
    "general_vtable_00f3c2c8": SpanSpec(0x00F3C2EC, 0x00F3C30C, "c9f22993cba4d07d32842c6a40d07a0e6abd1b2c1b965872d70e6e53918d03cd"),
    "general_vtable_00f3dd38": SpanSpec(0x00F3DD5C, 0x00F3DD7C, "6fad45f0236af30741f4dcb57669b2033917de313357a1a28459b9f35f29acc5"),
    "general_vtable_00f40d20": SpanSpec(0x00F40D44, 0x00F40D64, "29572f46096b8818459b9d8807b7552438d649d5f63f32077f309f2bb7fd9957"),
    "general_vtable_00f46738": SpanSpec(0x00F4675C, 0x00F4677C, "69b0fc81fead79937776ef732e925570d619244fec033519185b2de82abef313"),
    "general_vtable_00f411a8": SpanSpec(0x00F411CC, 0x00F411EC, "3e8a5bdb5c66429d961fa5daa2a127817f3ccec0e6714696d2e94a64e3338f93"),
    "general_vtable_00f420a8": SpanSpec(0x00F420CC, 0x00F420EC, "ded78c8a96ba92350cfb8ef10c13ab553db403c43b4fcfc079a3e8ef61a5b638"),
    "general_vtable_00f43268": SpanSpec(0x00F4328C, 0x00F432AC, "a1fdb66974af3b3cbc5b913419f32bd4d8534b1176edc5fc37a32d0e62c85027"),
    "general_vtable_00f46ec8": SpanSpec(0x00F46EEC, 0x00F46F0C, "2ac6b3f53228af242c9620dbdee71b2c5164b1fdd19514c0d186ba9febf0cbf5"),
    "general_vtable_00f47958": SpanSpec(0x00F4797C, 0x00F4799C, "cf75be1bbc1a38a1e3bbd6d9d23aa00fc2d2e0312395afecde1e2744dbf0362e"),
    "general_vtable_00f47bf8": SpanSpec(0x00F47C1C, 0x00F47C3C, "eb63e1c2e74a5ba4a2995281294001a4cc7a16f6d85ed81b45c182d6950f43cb"),
}


GENERAL_VTABLE_BINDINGS = (
    (0x00F33420, 0x00615B40, 0x00619680),
    (0x00F3C2C8, 0x006E4600, 0x0069AA00),
    (0x00F3DD38, 0x006E4600, 0x006B03F0),
    (0x00F40D20, 0x006E4600, 0x006E5AC0),
    (0x00F46738, 0x006E4600, 0x0073D360),
    (0x00F411A8, 0x006ECC30, 0x006ED880),
    (0x00F420A8, 0x006F9C30, 0x006FC2F0),
    (0x00F43268, 0x0070F2D0, 0x0070F390),
    (0x00F46EC8, 0x00730470, 0x007318C0),
    (0x00F47958, 0x0073E7B0, 0x0073E900),
    (0x00F47BF8, 0x00742480, 0x00744620),
)

GENERAL_REGISTRATION_REFS = {
    0x00615B40: (0x00F33444,),
    0x006E4600: (0x00F3C2EC, 0x00F3DD5C, 0x00F40D44, 0x00F4675C),
    0x006ECC30: (0x00F411CC,),
    0x006F9C30: (0x00F420CC,),
    0x0070F2D0: (0x00F4328C,),
    0x00730470: (0x00F46EEC,),
    0x0073E7B0: (0x00F4797C,),
    0x00742480: (0x00F47C1C,),
}

GENERAL_KIND0A_CALL_SITES = (
    0x00615B89,
    0x006E460D,
    0x006ECC3D,
    0x006F9C3D,
    0x0070F2DD,
    0x0073048C,
    0x0073E7BD,
    0x007424BA,
)

QUERY_DYNAMIC_CONTROLS = (
    (0x005002D5, "0x00000032..0x0000003B", "dynamic_5002"),
    (0x006E2CEB, "0x00000035", "dynamic_6e2c"),
    (0x0075B054, "0x00000034", "dynamic_75b0"),
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_lines(lines: Sequence[str]) -> str:
    return sha256(("\n".join(lines) + "\n").encode("ascii"))


def parse_pe(image: bytes) -> tuple[int, tuple[Section, ...]]:
    if image[:2] != b"MZ":
        raise RuntimeError("image DOS signature mismatch")
    pe_off = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_off : pe_off + 4] != b"PE\0\0":
        raise RuntimeError("image PE signature mismatch")
    file_header = pe_off + 4
    section_count = struct.unpack_from("<H", image, file_header + 2)[0]
    optional_size = struct.unpack_from("<H", image, file_header + 16)[0]
    optional = file_header + 20
    if struct.unpack_from("<H", image, optional)[0] != 0x10B:
        raise RuntimeError("expected PE32 optional header")
    image_base = struct.unpack_from("<I", image, optional + 28)[0]
    table = optional + optional_size
    sections: list[Section] = []
    for index in range(section_count):
        off = table + index * 40
        name = image[off : off + 8].split(b"\0", 1)[0].decode("ascii")
        virtual_size, rva, raw_size, raw_off = struct.unpack_from(
            "<IIII", image, off + 8
        )
        sections.append(
            Section(name, image_base + rva, raw_off, virtual_size, raw_size)
        )
    if not any(section.name == ".text" for section in sections):
        raise RuntimeError("image has no .text section")
    return image_base, tuple(sections)


def va_to_offset(sections: Sequence[Section], va: int, length: int = 1) -> int:
    for section in sections:
        delta = va - section.va
        if delta >= 0 and delta + length <= section.raw_size:
            return section.file_off + delta
    raise RuntimeError(f"VA is not backed by raw image data: 0x{va:08X}")


def file_offset_to_va(sections: Sequence[Section], file_off: int) -> int | None:
    for section in sections:
        delta = file_off - section.file_off
        if 0 <= delta < section.raw_size:
            return section.va + delta
    return None


def read_u32(image: bytes, sections: Sequence[Section], va: int) -> int:
    return struct.unpack_from("<I", image, va_to_offset(sections, va, 4))[0]


def span_bytes(
    image: bytes, sections: Sequence[Section], spec: SpanSpec
) -> tuple[bytes, int, int]:
    if spec.end <= spec.start:
        raise RuntimeError("invalid span")
    start_off = va_to_offset(sections, spec.start, spec.end - spec.start)
    end_off = start_off + spec.end - spec.start
    raw = image[start_off:end_off]
    if sha256(raw) != spec.sha256:
        raise RuntimeError(f"span hash guard failed at 0x{spec.start:08X}")
    return raw, start_off, end_off


def expect_bytes(
    image: bytes, sections: Sequence[Section], va: int, expected_hex: str
) -> None:
    expected = bytes.fromhex(expected_hex)
    off = va_to_offset(sections, va, len(expected))
    if image[off : off + len(expected)] != expected:
        raise RuntimeError(f"instruction-shape guard failed at 0x{va:08X}")


def format_span(
    name: str, image: bytes, sections: Sequence[Section]
) -> str:
    spec = SPANS[name]
    _, start_off, end_off = span_bytes(image, sections, spec)
    return (
        f"{name}=0x{spec.start:08X}..0x{spec.end:08X}"
        f"@file_off=0x{start_off:08X}..0x{end_off:08X}"
        f"@sha256={spec.sha256}"
    )


def direct_relative_sites(
    raw: bytes, text_va: int, target: int, opcode: int
) -> list[int]:
    sites: list[int] = []
    for index in range(len(raw) - 4):
        if raw[index] != opcode:
            continue
        relative = struct.unpack_from("<i", raw, index + 1)[0]
        if text_va + index + 5 + relative == target:
            sites.append(text_va + index)
    return sites


def dword_refs(
    image: bytes, sections: Sequence[Section], value: int
) -> list[int]:
    needle = struct.pack("<I", value)
    refs: list[int] = []
    start = 0
    while True:
        found = image.find(needle, start)
        if found < 0:
            break
        mapped = file_offset_to_va(sections, found)
        if mapped is not None:
            refs.append(mapped)
        start = found + 1
    return refs


def registration_census(
    raw: bytes, text_va: int, target: int
) -> list[tuple[int, int, int, int]]:
    """Return (call VA, kind immediate, pushed-register opcode, pattern VA)."""
    rows: list[tuple[int, int, int, int]] = []
    for index in range(len(raw) - 20):
        if raw[index] == 0x6A:
            kind = raw[index + 1]
            immediate_len = 2
        elif raw[index] == 0x68:
            kind = struct.unpack_from("<I", raw, index + 1)[0]
            immediate_len = 5
        else:
            continue
        pushed_object = raw[index + immediate_len]
        if not 0x50 <= pushed_object <= 0x57:
            continue
        singleton_call = index + immediate_len + 1
        if raw[singleton_call] != 0xE8:
            continue
        relative = struct.unpack_from("<i", raw, singleton_call + 1)[0]
        if text_va + singleton_call + 5 + relative != REGISTRATION_SINGLETON:
            continue
        if raw[singleton_call + 5 : singleton_call + 7] != b"\x8B\xC8":
            continue
        registration_call = singleton_call + 7
        if raw[registration_call] != 0xE8:
            continue
        relative = struct.unpack_from("<i", raw, registration_call + 1)[0]
        if text_va + registration_call + 5 + relative != target:
            continue
        rows.append(
            (
                text_va + registration_call,
                kind,
                pushed_object,
                text_va + index,
            )
        )
    return rows


def query_immediate_census(
    raw: bytes, text_va: int, call_sites: Sequence[int]
) -> list[tuple[int, int, int, int, int]]:
    """Pinned instruction-shape census, excluding three separately traced flows."""
    manual = {site for site, _, _ in QUERY_DYNAMIC_CONTROLS}
    rows: list[tuple[int, int, int, int, int]] = []
    for call_site in call_sites:
        if call_site in manual:
            continue
        call_off = call_site - text_va
        candidates: list[tuple[int, int, int, int]] = []
        for index in range(max(0, call_off - 160), call_off):
            if index + 8 <= call_off and raw[index : index + 3] == b"\xC7\x44\x24":
                candidates.append(
                    (
                        text_va + index,
                        raw[index + 3],
                        struct.unpack_from("<I", raw, index + 4)[0],
                        8,
                    )
                )
            if index + 11 <= call_off and raw[index : index + 3] == b"\xC7\x84\x24":
                candidates.append(
                    (
                        text_va + index,
                        struct.unpack_from("<I", raw, index + 3)[0],
                        struct.unpack_from("<I", raw, index + 7)[0],
                        11,
                    )
                )
        if not candidates:
            raise RuntimeError(
                f"query dispatch instruction-shape site unclassified: 0x{call_site:08X}"
            )
        store_va, stack_disp, immediate, length = max(candidates)
        rows.append((call_site, store_va, stack_disp, immediate, length))
    return rows


def read_reference_rows(
    path: Path, expected_size: int, expected_sha256: str
) -> tuple[bytes, list[dict[str, str]]]:
    raw = path.read_bytes()
    if len(raw) != expected_size or sha256(raw) != expected_sha256:
        raise RuntimeError(f"reference artifact guard failed: {path.name}")
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise RuntimeError(f"reference artifact has no rows: {path.name}")
    return raw, rows


def validate_references() -> tuple[set[str], set[str]]:
    _, selector_rows = read_reference_rows(
        SELECTOR_PATH, EXPECTED_SELECTOR_SIZE, EXPECTED_SELECTOR_SHA256
    )
    selector_matches = [
        row
        for row in selector_rows
        if row.get("evidence_key") == SELECTOR_REFERENCE_KEY
    ]
    if len(selector_matches) != 1:
        raise RuntimeError("selector reference key missing or duplicated")
    selector_row = selector_matches[0]
    if selector_row.get("source") != SOURCE or selector_row.get("input_selector") != "0":
        raise RuntimeError("selector reference row identity drift")

    _, ground_rows = read_reference_rows(
        GROUND_DROP_PATH, EXPECTED_GROUND_DROP_SIZE, EXPECTED_GROUND_DROP_SHA256
    )
    ground_matches = [
        row
        for row in ground_rows
        if row.get("evidence_key") == GROUND_DROP_REFERENCE_KEY
    ]
    if len(ground_matches) != 1:
        raise RuntimeError("ground-drop reference key missing or duplicated")
    ground_row = ground_matches[0]
    if ground_row.get("source") != SOURCE or ground_row.get("evidence_id") != "GDL-IMG-015":
        raise RuntimeError("ground-drop reference row identity drift")
    if ground_row.get("nonclaim") != (
        "Event kind 0x0A is not assigned a gameplay name by this static artifact."
    ):
        raise RuntimeError("ground-drop 0x0A nonclaim drift")
    return (
        {row.get("evidence_key", "") for row in selector_rows},
        {row.get("evidence_key", "") for row in ground_rows},
    )


def make_row(
    image: bytes,
    sections: Sequence[Section],
    *,
    event_key: str,
    row_kind: str,
    channel: str,
    receiver_or_owner: str,
    event_kind: str,
    field_or_slot: str,
    operation: str,
    semantic_status: str,
    exact_observation: str,
    census_scope: str,
    census_count: str,
    census_digest: str,
    primary_span: str,
    support_span_names: Sequence[str] = (),
    reference_artifact: str = "",
    reference_sha256: str = "",
    reference_keys: str = "",
    nonclaim: str,
    blocker: str,
    required_next_evidence: str,
) -> dict[str, str]:
    spec = SPANS[primary_span]
    _, start_off, end_off = span_bytes(image, sections, spec)
    row = {
        "event_key": event_key,
        "row_kind": row_kind,
        "channel": channel,
        "receiver_or_owner": receiver_or_owner,
        "event_kind": event_kind,
        "field_or_slot": field_or_slot,
        "operation": operation,
        "semantic_status": semantic_status,
        "measurement_label": "MEASURED",
        "exact_observation": exact_observation,
        "census_scope": census_scope,
        "census_count": census_count,
        "census_digest": census_digest,
        "span_start_va": f"0x{spec.start:08X}",
        "span_end_va": f"0x{spec.end:08X}",
        "file_off_start": f"0x{start_off:08X}",
        "file_off_end": f"0x{end_off:08X}",
        "span_sha256": spec.sha256,
        "support_spans": ";".join(
            format_span(name, image, sections) for name in support_span_names
        ),
        "reference_artifact": reference_artifact,
        "reference_sha256": reference_sha256,
        "reference_keys": reference_keys,
        "source": SOURCE,
        "source_file": SOURCE_FILE,
        "source_size": str(EXPECTED_IMAGE_SIZE),
        "source_sha256": EXPECTED_IMAGE_SHA256,
        "nonclaim": nonclaim,
        "blocker": blocker,
        "required_next_evidence": required_next_evidence,
        "artifact_pair_sha256": PAIR_PLACEHOLDER,
        "claim_sha256": "",
        "evidence_key": "",
    }
    claim_fields = {
        key: value
        for key, value in row.items()
        if key not in {"artifact_pair_sha256", "claim_sha256", "evidence_key"}
    }
    row["claim_sha256"] = sha256(
        json.dumps(
            claim_fields, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    )
    row["evidence_key"] = sha256(
        (
            "PF_QUEST_MARK_EVENT_CENSUS_V1\0"
            + row["claim_sha256"]
            + "\0"
            + row["span_sha256"]
            + "\0"
            + EXPECTED_IMAGE_SHA256
        ).encode("ascii")
    )
    return row


def derive(
    image: bytes,
) -> tuple[list[dict[str, str]], dict[str, object], set[str], set[str]]:
    _, sections = parse_pe(image)
    text = next(section for section in sections if section.name == ".text")
    text_raw = image[text.file_off : text.file_off + text.raw_size]

    for spec in SPANS.values():
        span_bytes(image, sections, spec)

    selector_keys, ground_keys = validate_references()

    query_regs = registration_census(text_raw, text.va, QUERY_REGISTRATION)
    query_reg_lines = [
        f"call=0x{call:08X};kind=0x{kind:08X};object_push=0x{push:02X};start=0x{start:08X}"
        for call, kind, push, start in query_regs
    ]
    if (
        len(query_regs) != EXPECTED_QUERY_REGISTRATION_COUNT
        or digest_lines(query_reg_lines) != EXPECTED_QUERY_REGISTRATION_DIGEST
    ):
        raise RuntimeError("query registration census drift")
    if [row for row in query_regs if row[1] == 0x0A] != [
        (0x00615BFC, 0x0A, 0x56, 0x00615BF2)
    ]:
        raise RuntimeError("query kind-0x0A registration uniqueness drift")
    if direct_relative_sites(text_raw, text.va, QUERY_REGISTRATION, 0xE8) != [
        row[0] for row in query_regs
    ]:
        raise RuntimeError("query registration pattern misses a direct call")
    if direct_relative_sites(text_raw, text.va, QUERY_REGISTRATION, 0xE9):
        raise RuntimeError("query registration gained a direct tail jump")
    if dword_refs(image, sections, QUERY_REGISTRATION):
        raise RuntimeError("query registration gained an absolute pointer carrier")

    general_regs = registration_census(text_raw, text.va, GENERAL_REGISTRATION)
    general_reg_lines = [
        f"call=0x{call:08X};kind=0x{kind:08X};object_push=0x{push:02X};start=0x{start:08X}"
        for call, kind, push, start in general_regs
    ]
    if (
        len(general_regs) != EXPECTED_GENERAL_REGISTRATION_COUNT
        or digest_lines(general_reg_lines) != EXPECTED_GENERAL_REGISTRATION_DIGEST
    ):
        raise RuntimeError("general registration census drift")
    general_kind0a_sites = tuple(
        row[0] for row in general_regs if row[1] == 0x0A
    )
    if general_kind0a_sites != GENERAL_KIND0A_CALL_SITES:
        raise RuntimeError("general kind-0x0A registration-site drift")
    if digest_lines([f"0x{site:08X}" for site in general_kind0a_sites]) != (
        EXPECTED_GENERAL_KIND0A_SITE_DIGEST
    ):
        raise RuntimeError("general kind-0x0A registration digest drift")
    if direct_relative_sites(text_raw, text.va, GENERAL_REGISTRATION, 0xE8) != [
        row[0] for row in general_regs
    ]:
        raise RuntimeError("general registration pattern misses a direct call")
    if direct_relative_sites(text_raw, text.va, GENERAL_REGISTRATION, 0xE9):
        raise RuntimeError("general registration gained a direct tail jump")
    if dword_refs(image, sections, GENERAL_REGISTRATION):
        raise RuntimeError("general registration gained an absolute pointer carrier")

    for vtable, registration_func, handler in GENERAL_VTABLE_BINDINGS:
        if read_u32(image, sections, vtable + 0x24) != registration_func:
            raise RuntimeError(f"general registration vtable drift: 0x{vtable:08X}")
        if read_u32(image, sections, vtable + 0x40) != handler:
            raise RuntimeError(f"general handler vtable drift: 0x{vtable:08X}")
    general_vtable_lines = [
        f"vtable=0x{vtable:08X};register_func=0x{registration:08X};handler=0x{handler:08X}"
        for vtable, registration, handler in sorted(GENERAL_VTABLE_BINDINGS)
    ]
    if digest_lines(general_vtable_lines) != EXPECTED_GENERAL_VTABLE_DIGEST:
        raise RuntimeError("general vtable census digest drift")
    for registration_func, expected_refs in GENERAL_REGISTRATION_REFS.items():
        if tuple(dword_refs(image, sections, registration_func)) != expected_refs:
            raise RuntimeError(
                f"general registration function reference drift: 0x{registration_func:08X}"
            )

    if read_u32(image, sections, 0x00F33454) != 0x00615BE0:
        raise RuntimeError("QuestModule query registration slot drift")
    if read_u32(image, sections, 0x00F33464) != 0x0061A8C0:
        raise RuntimeError("QuestModule query handler slot drift")
    if dword_refs(image, sections, 0x00615BE0) != [0x00F33454]:
        raise RuntimeError("QuestModule query registration vtable-owner drift")
    if dword_refs(image, sections, 0x0061A8C0) != [0x00F33464]:
        raise RuntimeError("QuestModule query handler vtable-owner drift")

    query_dispatch_calls = direct_relative_sites(
        text_raw, text.va, QUERY_DISPATCHER, 0xE8
    )
    if (
        len(query_dispatch_calls) != EXPECTED_QUERY_DISPATCH_CALL_COUNT
        or digest_lines([f"0x{site:08X}" for site in query_dispatch_calls])
        != EXPECTED_QUERY_DISPATCH_CALL_DIGEST
    ):
        raise RuntimeError("query dispatcher direct-call census drift")
    if direct_relative_sites(text_raw, text.va, QUERY_DISPATCHER, 0xE9):
        raise RuntimeError("query dispatcher gained a direct tail jump")
    if dword_refs(image, sections, QUERY_DISPATCHER):
        raise RuntimeError("query dispatcher gained an absolute pointer carrier")

    immediate_rows = query_immediate_census(
        text_raw, text.va, query_dispatch_calls
    )
    immediate_lines = [
        f"call=0x{call:08X};store=0x{store:08X};stack_disp=0x{disp:08X};imm=0x{immediate:08X};len={length}"
        for call, store, disp, immediate, length in immediate_rows
    ]
    if (
        len(immediate_rows) != EXPECTED_QUERY_IMMEDIATE_COUNT
        or digest_lines(immediate_lines) != EXPECTED_QUERY_IMMEDIATE_DIGEST
    ):
        raise RuntimeError("query immediate-kind instruction-shape census drift")
    if [row for row in immediate_rows if row[3] == 0x0A] != [
        (0x00449FAD, 0x00449FA1, 0x20, 0x0A, 8)
    ]:
        raise RuntimeError("query immediate kind-0x0A producer uniqueness drift")

    manual_lines = [
        f"call=0x{site:08X};kind={kind}" for site, kind, _ in QUERY_DYNAMIC_CONTROLS
    ]
    if digest_lines(manual_lines) != EXPECTED_MANUAL_QUERY_CONTROL_DIGEST:
        raise RuntimeError("manual query control digest drift")
    if sorted(site for site, _, _ in QUERY_DYNAMIC_CONTROLS) != sorted(
        set(query_dispatch_calls) - {row[0] for row in immediate_rows}
    ):
        raise RuntimeError("query manual-control partition drift")
    expect_bytes(image, sections, 0x0050024C, "8D7E32")
    expect_bytes(image, sections, 0x00500309, "4683FE0A")
    expect_bytes(image, sections, 0x006E2BF5, "837B1035")
    expect_bytes(image, sections, 0x006E2CE4, "53")
    expect_bytes(image, sections, 0x0075B003, "BF34000000")
    expect_bytes(image, sections, 0x0075B046, "89BC2438010000")

    producer_callers = direct_relative_sites(text_raw, text.va, QUERY_PRODUCER, 0xE8)
    if (
        len(producer_callers) != EXPECTED_QUERY_PRODUCER_CALLER_COUNT
        or digest_lines([f"0x{site:08X}" for site in producer_callers])
        != EXPECTED_QUERY_PRODUCER_CALLER_DIGEST
    ):
        raise RuntimeError("query producer caller census drift")
    if producer_callers != [
        0x005250B5,
        0x00528695,
        0x0052C265,
        0x0052E935,
        0x006167D1,
    ]:
        raise RuntimeError("query producer caller identity drift")
    if direct_relative_sites(text_raw, text.va, QUERY_PRODUCER, 0xE9):
        raise RuntimeError("query producer gained a direct tail jump")
    if dword_refs(image, sections, QUERY_PRODUCER):
        raise RuntimeError("query producer gained an absolute pointer carrier")

    expect_bytes(image, sections, 0x00449FAD, "E8AEFF1A00")
    expect_bytes(image, sections, 0x00615BFC, "E82F52FEFF")
    expect_bytes(image, sections, 0x0061A8F2, "894618")
    expect_bytes(image, sections, 0x005F6D2D, "C744241C0A000000")
    expect_bytes(image, sections, 0x005F6D39, "E8322F0000")

    selector_ref = "PF_ATTR_QUEST_MARK_SELECTOR.tsv"
    ground_ref = "PF_GROUND_DROP_LIFETIME.tsv"
    selector_hash = EXPECTED_SELECTOR_SHA256
    ground_hash = EXPECTED_GROUND_DROP_SHA256
    static_ceiling = (
        "Mapped executable .text direct E8/E9 targets, immediate registration shapes, "
        "and image-resident raw vtable pointers only; computed control transfers and "
        "runtime-only registration remain outside the census."
    )

    rows = [
        make_row(
            image,
            sections,
            event_key="QME-IMG-001",
            row_kind="EVENT_LAYOUT_INIT",
            channel="SHARED_EVENT_OBJECT",
            receiver_or_owner="event constructor 0x005F8D20",
            event_kind="N/A",
            field_or_slot="+0x10,+0x14,+0x18,+0x20,+0x24,+0x28,+0x2C",
            operation="ZERO_INITIALIZE",
            semantic_status="PROVEN_EXACT",
            exact_observation="The constructor zeros kind +0x10, byte +0x14, dword +0x18, and dwords +0x20/+0x24/+0x28/+0x2C before dispatch-specific producers fill them.",
            census_scope="Pinned constructor slice.",
            census_count="7 initialized fields",
            census_digest="",
            primary_span="event_ctor_fields",
            nonclaim="The common layout does not give numeric event kinds a global gameplay meaning.",
            blocker="",
            required_next_evidence="None for these initialization writes.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-002",
            row_kind="QUERY_PRODUCER",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="producer 0x00449F30; caller-provided root +0x130",
            event_kind="0x0000000A",
            field_or_slot="event +0x18,+0x20,+0x24 and +0x10",
            operation="SEED_THEN_SYNCHRONOUS_DISPATCH",
            semantic_status="PROVEN_EXACT",
            exact_observation="The producer constructs a stack event, stores argument1 at +0x18, argument2 at +0x20, argument3 at +0x24, stores kind 0x0A at +0x10, and calls 0x005F9F60 with that event pointer.",
            census_scope="One exact producer body on the pinned image.",
            census_count="1 producer body",
            census_digest="",
            primary_span="query_producer_seed_dispatch",
            support_span_names=("event_ctor_fields",),
            reference_artifact=selector_ref,
            reference_sha256=selector_hash,
            reference_keys=SELECTOR_REFERENCE_KEY,
            nonclaim="This row does not copy or reinterpret any selector row and does not name 0x0A globally.",
            blocker="",
            required_next_evidence="None for the stack-field seed and direct dispatch edge.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-003",
            row_kind="QUERY_RESULT_LIFETIME",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="producer 0x00449F30",
            event_kind="0x0000000A",
            field_or_slot="event +0x18 low byte",
            operation="READ_AFTER_DISPATCH_THEN_DESTROY",
            semantic_status="PROVEN_EXACT",
            exact_observation="After 0x005F9F60 returns true, the producer reads the low byte of event +0x18, destroys the stack event, and returns that byte; the false branch also destroys the event and returns zero.",
            census_scope="Pinned post-dispatch slice.",
            census_count="2 destruction branches; 1 result read",
            census_digest="",
            primary_span="query_producer_read_destroy",
            nonclaim="No asynchronous retention is observed on this producer path, but transitive retention inside an invoked listener is not disproved by IMAGE alone.",
            blocker="Runtime reentrancy and transitive retention are unmeasured.",
            required_next_evidence="Runtime instrumentation only if reentrancy or retention must be excluded beyond the direct path.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-004",
            row_kind="QUERY_PRODUCER_CALLER_CENSUS",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="direct callers of 0x00449F30",
            event_kind="0x0000000A by callee",
            field_or_slot="call target",
            operation="DIRECT_CALL_CENSUS",
            semantic_status="PROVEN_BOUNDED",
            exact_observation="The mapped executable .text contains five direct E8 callers of 0x00449F30 at 0x005250B5, 0x00528695, 0x0052C265, 0x0052E935, and 0x006167D1; no direct E9 or absolute dword carrier for the target exists in the image.",
            census_scope=static_ceiling,
            census_count="5 direct E8; 0 direct E9; 0 absolute dword refs",
            census_digest=EXPECTED_QUERY_PRODUCER_CALLER_DIGEST,
            primary_span="caller_5250",
            support_span_names=("caller_5286", "caller_52c2", "caller_52e9", "cnetnpc_call"),
            nonclaim="The four non-CNetNPC callers are not assigned class or gameplay names here.",
            blocker="Computed target formation without a static carrier remains outside the bounded census.",
            required_next_evidence="A whole-program indirect-call proof is required to make a global caller claim.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-005",
            row_kind="CNETNPC_QUERY_BINDING",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="CNetNPC refresh path from referenced selector row",
            event_kind="0x0000000A by 0x00449F30",
            field_or_slot="+0x18=NPCAttr+0x78 u16; +0x20=actor+0x78; +0x24=actor+0x7C",
            operation="CALL_WITH_THREE_ARGUMENTS",
            semantic_status="PROVEN_EXACT",
            exact_observation="The CNetNPC path zero-extends NPCAttr +0x78, passes it as producer argument1, and passes actor dwords +0x78/+0x7C as arguments2/3 before the direct call at 0x006167D1.",
            census_scope="Exact CNetNPC caller slice; selector behavior remains owned by the referenced artifact.",
            census_count="1 CNetNPC call site",
            census_digest="",
            primary_span="cnetnpc_call",
            reference_artifact=selector_ref,
            reference_sha256=selector_hash,
            reference_keys=SELECTOR_REFERENCE_KEY,
            nonclaim="This row does not duplicate selector rows or assign semantic names to actor +0x78/+0x7C.",
            blocker="",
            required_next_evidence="None for the argument-to-event-field binding.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-006",
            row_kind="QUERY_REGISTRATION_CENSUS",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="direct registration API 0x005FAE30",
            event_kind="0x0000000A",
            field_or_slot="registration virtual slot +0x34",
            operation="DIRECT_REGISTRATION_CENSUS",
            semantic_status="PROVEN_BOUNDED",
            exact_observation="All 55 direct registration calls match the pinned push-kind/push-object/singleton/call shape. Exactly one registers kind 0x0A: call 0x00615BFC in function 0x00615BE0. No direct E9 or absolute dword carrier for 0x005FAE30 exists.",
            census_scope=static_ceiling,
            census_count="55 direct registrations; 1 kind-0x0A site",
            census_digest=EXPECTED_QUERY_REGISTRATION_DIGEST,
            primary_span="query_registration",
            reference_artifact=selector_ref,
            reference_sha256=selector_hash,
            reference_keys=SELECTOR_REFERENCE_KEY,
            nonclaim="This is not a process-lifetime or runtime-injected listener census.",
            blocker="Computed registration calls and runtime-only listeners remain outside the static image census.",
            required_next_evidence="Instrument registry mutation if runtime injection must be excluded.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-007",
            row_kind="QUEST_QUERY_VTABLE_BINDING",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="QuestModule per referenced selector row; vtable 0x00F33420",
            event_kind="0x0000000A",
            field_or_slot="vtable +0x34=0x00615BE0; +0x44=0x0061A8C0",
            operation="BIND_REGISTRATION_TO_HANDLER",
            semantic_status="PROVEN_EXACT",
            exact_observation="The sole image dword reference to query registration function 0x00615BE0 is vtable slot +0x34 at 0x00F33454; the sole image dword reference to query handler 0x0061A8C0 is slot +0x44 at 0x00F33464 of the same vtable.",
            census_scope="Image-resident raw dword references to the two exact functions.",
            census_count="1 vtable owner",
            census_digest="",
            primary_span="quest_vtable_query_bind",
            reference_artifact=selector_ref,
            reference_sha256=selector_hash,
            reference_keys=SELECTOR_REFERENCE_KEY,
            nonclaim="The class label is inherited only from the pinned selector reference; this row does not re-derive or broaden it.",
            blocker="Runtime-generated vtables are not represented by raw image dword references.",
            required_next_evidence="Runtime class-map evidence only if dynamic vtables must be excluded.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-008",
            row_kind="QUERY_REGISTRY_INSERT",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="registration API 0x005FAE30",
            event_kind="caller-provided registration key",
            field_or_slot="registration singleton +0x20 map",
            operation="INSERT_LISTENER_RECORD",
            semantic_status="PROVEN_EXACT",
            exact_observation="The query registration API advances to singleton +0x20, locates or creates the keyed record, and records/retains the supplied listener in that channel's registration structure.",
            census_scope="Pinned registration function body.",
            census_count="1 registration API",
            census_digest="",
            primary_span="query_registry_insert",
            nonclaim="The exact runtime vector population at a later instant is not observed by IMAGE.",
            blocker="Runtime registry contents are unavailable in this IMAGE-only lane.",
            required_next_evidence="Runtime registry snapshot only if live ordering/content must be measured.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-009",
            row_kind="QUEST_QUERY_WRITER",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="QuestModule query handler 0x0061A8C0",
            event_kind="0x0000000A",
            field_or_slot="event +0x18 dword",
            operation="OVERWRITE_WITH_ZERO_EXTENDED_SELECTOR",
            semantic_status="PROVEN_EXACT",
            exact_observation="For kind 0x0A the handler passes event +0x18/+0x20/+0x24 to 0x00619E00, zero-extends AL, overwrites the full dword at event +0x18, and returns true.",
            census_scope="Event-only subspan of the referenced QuestModule handler; selector computation remains in the reference artifact.",
            census_count="1 direct +0x18 writer in the sole static query subscriber",
            census_digest="",
            primary_span="quest_query_writer",
            reference_artifact=selector_ref,
            reference_sha256=selector_hash,
            reference_keys=SELECTOR_REFERENCE_KEY,
            nonclaim="No selector meaning is duplicated here; selector 0 is not called hidden.",
            blocker="",
            required_next_evidence="None for this exact write; runtime presentation remains a separate evidence layer.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-010",
            row_kind="QUERY_DISPATCH_ORDER",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="dispatcher 0x005F9F60",
            event_kind="event +0x10 lookup key",
            field_or_slot="dispatcher owner +0xA0 map; listener vtable +0x44",
            operation="ITERATE_ALL_IN_VECTOR_STORAGE_ORDER",
            semantic_status="PROVEN_EXACT",
            exact_observation="The dispatcher looks up event +0x10 in owner +0xA0, iterates listener vector indices from zero upward, invokes vtable +0x44 on the same event pointer, ORs successful returns, and does not stop after a true return.",
            census_scope="Pinned dispatcher body.",
            census_count="all current vector entries",
            census_digest="",
            primary_span="query_dispatcher",
            nonclaim="If an unmeasured later listener writes +0x18, the last such writer in current vector storage order would win; insertion-time chronology is not claimed.",
            blocker="Runtime registry contents and reentrant mutation are unmeasured.",
            required_next_evidence="Runtime registry trace only if live ordering or reentrancy must be closed.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-011",
            row_kind="QUERY_DISPATCH_TARGET_CENSUS",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="direct callers of 0x005F9F60",
            event_kind="0x0000000A unique in pinned immediate-shape partition",
            field_or_slot="event +0x10 producer store",
            operation="DIRECT_CALL_AND_KIND_PARTITION_CENSUS",
            semantic_status="PROVEN_BOUNDED",
            exact_observation="The .text direct-target census has 126 E8 calls: 123 match the pinned immediate stack-kind shape and three are separately control-traced. Only call 0x00449FAD has immediate kind 0x0A; the three other flows are bounded to 0x32..0x3B, 0x35, and 0x34. No direct E9 or absolute dword carrier for 0x005F9F60 exists.",
            census_scope=static_ceiling,
            census_count="126 direct E8; 123 immediate-shape; 3 manual controls; 1 kind-0x0A producer",
            census_digest=f"calls={EXPECTED_QUERY_DISPATCH_CALL_DIGEST};immediate={EXPECTED_QUERY_IMMEDIATE_DIGEST};manual={EXPECTED_MANUAL_QUERY_CONTROL_DIGEST}",
            primary_span="query_unique_immediate",
            support_span_names=("dynamic_5002", "dynamic_6e2c", "dynamic_75b0"),
            nonclaim="The 123-row classifier is an explicitly pinned instruction-shape census, not a semantic decoder for every other numeric kind.",
            blocker="Computed control transfers with no static target carrier remain outside the census.",
            required_next_evidence="Whole-program indirect-call proof to upgrade from bounded to global.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-012",
            row_kind="QUERY_NON0A_CONTROL",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="loop producer at 0x005002D5",
            event_kind="0x00000032..0x0000003B",
            field_or_slot="event +0x10 from EDI",
            operation="REGISTER_DERIVED_KIND_CONTROL",
            semantic_status="PROVEN_EXACT",
            exact_observation="ESI starts at zero, EDI is set to ESI+0x32, EDI is stored as the event kind, and the loop increments ESI while ESI<10; this direct dispatcher call cannot produce 0x0A on the traced path.",
            census_scope="Pinned local control-flow slice.",
            census_count="10 values",
            census_digest="",
            primary_span="dynamic_5002",
            nonclaim="No gameplay names are assigned to 0x32..0x3B.",
            blocker="",
            required_next_evidence="None for exclusion from kind 0x0A.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-013",
            row_kind="QUERY_NON0A_CONTROL",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="forwarder at 0x006E2CEB",
            event_kind="0x00000035",
            field_or_slot="incoming event +0x10",
            operation="FORWARD_PRECHECKED_EVENT",
            semantic_status="PROVEN_EXACT",
            exact_observation="The function rejects unless incoming event +0x10 equals 0x35, then later forwards that same EBX event pointer to 0x005F9F60; this call cannot carry 0x0A on the traced path.",
            census_scope="Pinned function control-flow slice.",
            census_count="1 forwarded kind",
            census_digest="",
            primary_span="dynamic_6e2c",
            nonclaim="No gameplay name is assigned to 0x35.",
            blocker="",
            required_next_evidence="None for exclusion from kind 0x0A.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-014",
            row_kind="QUERY_NON0A_CONTROL",
            channel="RETURN_VALUE_CHANNEL",
            receiver_or_owner="loop producer at 0x0075B054",
            event_kind="0x00000034",
            field_or_slot="event +0x10 from EDI",
            operation="REGISTER_HELD_KIND_CONTROL",
            semantic_status="PROVEN_EXACT",
            exact_observation="EDI is initialized to 0x34 before the event loop and stored at event +0x10 before the direct dispatch call; the traced loop preserves EDI, excluding 0x0A at this site.",
            census_scope="Pinned local control-flow slice.",
            census_count="1 held kind",
            census_digest="",
            primary_span="dynamic_75b0",
            nonclaim="No gameplay name is assigned to 0x34.",
            blocker="",
            required_next_evidence="None for exclusion from kind 0x0A.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-015",
            row_kind="MODULE_ADD_BOUNDARY",
            channel="BOTH_MODULE_CHANNELS",
            receiver_or_owner="module manager add path 0x005FB800",
            event_kind="N/A",
            field_or_slot="module vtable +0x10 identity; setup slots +0x3C,+0x30,+0x20,+0x24,+0x34,+0x28",
            operation="REJECT_DUPLICATE_ID_THEN_REGISTER",
            semantic_status="PROVEN_EXACT",
            exact_observation="Before insertion the manager compares the incoming module's vtable +0x10 identity against current modules and returns on equality. For a new module it inserts/retains it and calls setup slots in order +0x3C,+0x30,+0x20,+0x24,+0x34,+0x28; general registration therefore precedes query registration.",
            census_scope="One manager add implementation.",
            census_count="at most one active module per equal +0x10 identity in this manager",
            census_digest="",
            primary_span="module_add",
            nonclaim="This is not process-wide singleton proof and does not exclude another manager instance or runtime mutation.",
            blocker="Manager-instance multiplicity is not measured at runtime.",
            required_next_evidence="Runtime manager census only if process-wide uniqueness is required.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-016",
            row_kind="MODULE_REMOVE_BOUNDARY",
            channel="BOTH_MODULE_CHANNELS",
            receiver_or_owner="module manager removal path 0x005FB5D0",
            event_kind="registered keys for removed module",
            field_or_slot="general owner +0x80 and query owner +0xA0",
            operation="UNREGISTER_LISTENER_FROM_BOTH_CHANNELS",
            semantic_status="PROVEN_EXACT",
            exact_observation="Removal walks the module's registration records, calls 0x005FA860 for general-channel entries and 0x005FA950 for query-channel entries, bounding the static listener lifetime to manager add/remove orchestration.",
            census_scope="Pinned manager removal function.",
            census_count="2 channel cleanup loops",
            census_digest="",
            primary_span="module_unregister",
            nonclaim="Crash-time or abnormal teardown behavior is not observed.",
            blocker="Abnormal runtime teardown remains unmeasured.",
            required_next_evidence="Runtime teardown trace only if abnormal lifetime must be closed.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-017",
            row_kind="GENERAL_REGISTRATION_CONTROL_CENSUS",
            channel="GENERAL_NOTIFICATION_CHANNEL",
            receiver_or_owner="direct registration API 0x005FACE0",
            event_kind="0x0000000A",
            field_or_slot="registration slot +0x24; handler slot +0x40",
            operation="CROSS_CHANNEL_NUMERIC_REUSE_CENSUS",
            semantic_status="PROVEN_BOUNDED",
            exact_observation="The general channel has 140 direct registrations and eight kind-0x0A registration sites. Image dword references bind those eight functions to 11 distinct vtables and 11 +0x40 handlers. This population is separate from the sole +0x44 query subscriber.",
            census_scope=static_ceiling,
            census_count="140 direct registrations; 8 kind-0x0A sites; 11 vtable owners",
            census_digest=f"registrations={EXPECTED_GENERAL_REGISTRATION_DIGEST};kind0a_sites={EXPECTED_GENERAL_KIND0A_SITE_DIGEST};vtables={EXPECTED_GENERAL_VTABLE_DIGEST}",
            primary_span="general_quest_registration",
            support_span_names=(
                "general_shared_registration",
                "general_6ecc_registration",
                "general_6f9c_registration",
                "general_70f2_registration",
                "general_7304_registration",
                "general_73e7_registration",
                "general_7424_registration",
                "general_vtable_00f33420",
                "general_vtable_00f3c2c8",
                "general_vtable_00f3dd38",
                "general_vtable_00f40d20",
                "general_vtable_00f411a8",
                "general_vtable_00f420a8",
                "general_vtable_00f43268",
                "general_vtable_00f46738",
                "general_vtable_00f46ec8",
                "general_vtable_00f47958",
                "general_vtable_00f47bf8",
            ),
            reference_artifact=ground_ref,
            reference_sha256=ground_hash,
            reference_keys=GROUND_DROP_REFERENCE_KEY,
            nonclaim="Numeric 0x0A is not assigned a global gameplay name; unknown vtable owners are not guessed from nearby strings.",
            blocker="Computed registrations and runtime-only vtables remain outside the image census.",
            required_next_evidence="Runtime registration trace to upgrade from bounded static to live exhaustive.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-018",
            row_kind="GENERAL_DISPATCH_CONTROL",
            channel="GENERAL_NOTIFICATION_CHANNEL",
            receiver_or_owner="dispatcher 0x005F9C70",
            event_kind="event +0x10 lookup key",
            field_or_slot="dispatcher owner +0x80 map; listener vtable +0x40",
            operation="ITERATE_GENERAL_LISTENERS",
            semantic_status="PROVEN_EXACT",
            exact_observation="The general dispatcher looks up event +0x10 in owner +0x80, iterates the current vector, and invokes listener vtable +0x40. It is structurally distinct from query owner +0xA0 / vtable +0x44 and has no query-result aggregation.",
            census_scope="Pinned general dispatcher body.",
            census_count="all current general-vector entries",
            census_digest="",
            primary_span="general_dispatcher",
            nonclaim="Shared numeric keys do not join the two registries, handlers, or lifecycles.",
            blocker="Live vector contents are unmeasured.",
            required_next_evidence="Runtime registry snapshot only if live order is required.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-019",
            row_kind="GENERAL_KIND0A_PRODUCER_CONTROL",
            channel="GENERAL_NOTIFICATION_CHANNEL",
            receiver_or_owner="producer slice containing call 0x005F6D39",
            event_kind="0x0000000A",
            field_or_slot="event +0x10; separate payload at +0x30",
            operation="SYNCHRONOUS_GENERAL_DISPATCH",
            semantic_status="PROVEN_EXACT",
            exact_observation="This separate producer constructs a general-channel event, stores kind 0x0A, stores its argument in a later event field, and calls 0x005F9C70 rather than the query dispatcher.",
            census_scope="One exact cross-channel producer control; not a full general-producer census.",
            census_count="1 measured general producer",
            census_digest="",
            primary_span="general_kind0a_producer",
            reference_artifact=ground_ref,
            reference_sha256=ground_hash,
            reference_keys=GROUND_DROP_REFERENCE_KEY,
            nonclaim="This row does not claim that the producer's payload or every general subscriber has quest meaning.",
            blocker="Full general-channel producer census is outside the CNetNPC query-path closure.",
            required_next_evidence="A separately scoped general-channel producer census if every notification producer is required.",
        ),
        make_row(
            image,
            sections,
            event_key="QME-IMG-020",
            row_kind="GROUND_DROP_CROSS_CONTROL_BINDING",
            channel="GENERAL_NOTIFICATION_CHANNEL",
            receiver_or_owner="vtable 0x00F3DD38; DropThing label only via GDL-IMG-015",
            event_kind="0x0000000A",
            field_or_slot="vtable +0x24=0x006E4600; +0x40=0x006B03F0",
            operation="BIND_GENERAL_REGISTRATION_TO_CONTROL_HANDLER",
            semantic_status="PROVEN_EXACT",
            exact_observation="One of the 11 general-channel vtables binds shared registration function 0x006E4600 at +0x24 and handler 0x006B03F0 at +0x40. GDL-IMG-015 independently identifies that handler's kind-0x0A clear behavior.",
            census_scope="New vtable/channel binding plus exact reference to the existing ground-drop row.",
            census_count="1 referenced cross-domain control",
            census_digest="",
            primary_span="ground_drop_vtable_bind",
            support_span_names=("general_shared_registration",),
            reference_artifact=ground_ref,
            reference_sha256=ground_hash,
            reference_keys=GROUND_DROP_REFERENCE_KEY,
            nonclaim="The GDL-IMG-015 evidence row is cited, not copied; 0x0A is not named globally and this lifecycle is not joined to QuestIconBoard.",
            blocker="",
            required_next_evidence="None for channel separation; runtime behavior remains source-separated.",
        ),
    ]

    metadata: dict[str, object] = {
        "query_registration_count": len(query_regs),
        "query_kind0a_registration_count": len(
            [row for row in query_regs if row[1] == 0x0A]
        ),
        "general_registration_count": len(general_regs),
        "general_kind0a_registration_count": len(general_kind0a_sites),
        "general_kind0a_vtable_count": len(GENERAL_VTABLE_BINDINGS),
        "query_dispatch_call_count": len(query_dispatch_calls),
        "query_immediate_count": len(immediate_rows),
        "query_manual_control_count": len(QUERY_DYNAMIC_CONTROLS),
        "query_producer_caller_count": len(producer_callers),
        "general_vtable_lines": general_vtable_lines,
    }
    return rows, metadata, selector_keys, ground_keys


def validate_rows(
    rows: Sequence[Mapping[str, str]],
    selector_keys: set[str],
    ground_keys: set[str],
) -> None:
    if len(rows) != 20:
        raise RuntimeError("row count drift")
    if any(tuple(row.keys()) != FIELDNAMES for row in rows):
        raise RuntimeError("row schema/order drift")
    for row in rows:
        if row["source"] != SOURCE or row["source_sha256"] != EXPECTED_IMAGE_SHA256:
            raise RuntimeError("row source-layer drift")
        if row["measurement_label"] != "MEASURED":
            raise RuntimeError("measured/open separation drift")
        for key in ("claim_sha256", "evidence_key", "span_sha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", row[key]):
                raise RuntimeError(f"malformed {key}")
        if row["artifact_pair_sha256"] != PAIR_PLACEHOLDER:
            raise RuntimeError("pair placeholder drift")
    for field in ("event_key", "claim_sha256", "evidence_key"):
        values = [row[field] for row in rows]
        if len(values) != len(set(values)):
            raise RuntimeError(f"duplicate {field}")
    primary = [
        (row["source"], row["span_start_va"], row["span_end_va"], row["span_sha256"])
        for row in rows
    ]
    if len(primary) != len(set(primary)):
        raise RuntimeError("duplicate primary evidence span")
    new_keys = {row["evidence_key"] for row in rows}
    if new_keys & selector_keys:
        raise RuntimeError("selector evidence row duplicated")
    if new_keys & ground_keys:
        raise RuntimeError("ground-drop evidence row duplicated")

    allowed_references = {
        "": ("", ""),
        "PF_ATTR_QUEST_MARK_SELECTOR.tsv": (
            EXPECTED_SELECTOR_SHA256,
            SELECTOR_REFERENCE_KEY,
        ),
        "PF_GROUND_DROP_LIFETIME.tsv": (
            EXPECTED_GROUND_DROP_SHA256,
            GROUND_DROP_REFERENCE_KEY,
        ),
    }
    for row in rows:
        artifact = row["reference_artifact"]
        if artifact not in allowed_references:
            raise RuntimeError("unknown reference artifact")
        expected_hash, expected_key = allowed_references[artifact]
        if row["reference_sha256"] != expected_hash:
            raise RuntimeError("reference hash/key separation drift")
        if row["reference_keys"] != expected_key:
            raise RuntimeError("reference key drift")

    combined_text = "\n".join("\t".join(row.values()) for row in rows).lower()
    forbidden = ("selector 0 hidden", "selector0 hidden", "0x0a quest event")
    if any(term in combined_text for term in forbidden):
        raise RuntimeError("forbidden semantic overclaim")


def render_tsv(rows: Sequence[Mapping[str, str]]) -> bytes:
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


def render_report(
    rows: Sequence[Mapping[str, str]], metadata: Mapping[str, object]
) -> bytes:
    pair = PAIR_PLACEHOLDER
    general_vtables = "\n".join(
        f"- `{line}`" for line in metadata["general_vtable_lines"]  # type: ignore[index]
    )
    row_lines = "\n".join(
        f"| {row['event_key']} | {row['channel']} | {row['row_kind']} | {row['semantic_status']} | {row['span_start_va']}..{row['span_end_va']} |"
        for row in rows
    )
    report = f"""# PF Quest-Mark Event Census

Status: **OPEN overall; the bounded IMAGE census below is complete for the stated direct/static scope.**

## Outcome first

- On image SHA-256 `{EXPECTED_IMAGE_SHA256}`, the return-value/query channel has **{metadata['query_registration_count']}** direct registration sites. Exactly **{metadata['query_kind0a_registration_count']}** is kind `0x0A`: `0x00615BFC` in the QuestModule registration function referenced by `PF_ATTR_QUEST_MARK_SELECTOR.tsv` / evidence key `{SELECTOR_REFERENCE_KEY}`.
- Query dispatcher `0x005F9F60` uses owner map `+0xA0` and listener vtable slot `+0x44`. Its direct-target census has **{metadata['query_dispatch_call_count']}** calls: **{metadata['query_immediate_count']}** pinned immediate-kind shapes plus **{metadata['query_manual_control_count']}** separately traced non-`0x0A` controls. The only immediate `0x0A` producer is `0x00449F30` / dispatch call `0x00449FAD`.
- Producer `0x00449F30` has **{metadata['query_producer_caller_count']}** direct callers. The CNetNPC caller at `0x006167D1` seeds event `+0x18` from `NPCAttr+0x78` and `+0x20/+0x24` from actor `+0x78/+0x7C`.
- QuestModule handler `0x0061A8C0` receives the query callback through vtable `+0x44`; its `0x0A` branch calls the referenced selector computation, zero-extends AL, and overwrites the full dword at event `+0x18`. The query dispatcher continues after a true return, so an additional later listener could overwrite the result in principle. Within the pinned direct/static census there is only this one query-channel `0x0A` vtable owner.
- Numeric kind `0x0A` is **not globally a quest event**. The separate general-notification channel has **{metadata['general_kind0a_registration_count']}** direct kind-`0x0A` registration sites bound through shared functions to **{metadata['general_kind0a_vtable_count']}** image vtables. General dispatcher `0x005F9C70` uses owner map `+0x80` and vtable slot `+0x40`. `GDL-IMG-015` / evidence key `{GROUND_DROP_REFERENCE_KEY}` independently establishes kind-`0x0A` clear behavior at handler `0x006B03F0`; this artifact adds only the channel/vtable binding and does not copy that row.

## Event object and lifetime

`0x00449F30` constructs a stack event, seeds `+0x18/+0x20/+0x24`, stores kind `0x0A` at `+0x10`, and synchronously calls the query dispatcher. If any handler returns true, it reads the low byte at `+0x18`; both true and false paths destroy the stack event before return.

The module add path rejects another module with an equal vtable `+0x10` identity in that manager. For a new module it calls general registration slot `+0x24` before query registration slot `+0x34`. The removal path unregisters the module from both owner `+0x80` and owner `+0xA0` maps. These are manager-local static boundaries, not process-wide or crash-time guarantees.

## Channel partition

| Property | Return-value/query channel | General-notification channel |
|---|---|---|
| registration API | `0x005FAE30` | `0x005FACE0` |
| manager lookup map | `+0xA0` | `+0x80` |
| listener virtual slot | `+0x44` | `+0x40` |
| dispatch API | `0x005F9F60` | `0x005F9C70` |
| kind-`0x0A` direct registration sites | 1 | 8 |
| kind-`0x0A` image vtable owners | 1 | 11 |
| CNetNPC query result writer | QuestModule `0x0061A8C0` writes `+0x18` | not in this registry/vector |

The general-channel vtable identities are retained as addresses unless an existing pinned reference supplies a class label:

{general_vtables}

## Selector reference, without duplication

This artifact does not reproduce the selector table. It references exact selector evidence key `{SELECTOR_REFERENCE_KEY}` from `PF_ATTR_QUEST_MARK_SELECTOR.tsv` (SHA-256 `{EXPECTED_SELECTOR_SHA256}`). In particular, selector `0` is **not called hidden** here: the referenced row says it sets board-root `+0x18` bit-mask `0x1` and does not select or bind a new texture. Client-observable visibility remains outside this IMAGE-only census.

## Measured rows

| key | channel | row kind | status | primary VA span |
|---|---|---|---|---|
{row_lines}

Every TSV row has exactly one source, `IMAGE`, and includes an exact primary VA range, file-offset range, and SHA-256. `reference_keys` joins prior rows without copying their evidence keys or converting their claims into new evidence.

## Open / proposed work (not measured facts)

- **OPEN:** computed control transfers with no static E8/E9/absolute target carrier, runtime-only listener injection, runtime registry order, reentrant mutation, and abnormal teardown are not closed by this bounded static census.
- **OPEN:** the four non-CNetNPC callers of `0x00449F30` and unlabelled general-channel vtables are intentionally not assigned gameplay/class names.
- **OPEN:** client-observable QuestIconBoard presentation is a different source layer and is not inferred here.
- **PROPOSED only if needed:** instrument registration/removal and one `0x0A` query dispatch to capture live vector identities/order. Do not merge that runtime evidence into these IMAGE rows.

## Re-derivation and publication

- Pinned image: `PF_ROOT://GameClient/GameClient.local.bin`, size `{EXPECTED_IMAGE_SIZE}`, SHA-256 `{EXPECTED_IMAGE_SHA256}`.
- Pinned selector reference: size `{EXPECTED_SELECTOR_SIZE}`, SHA-256 `{EXPECTED_SELECTOR_SHA256}`, key `{SELECTOR_REFERENCE_KEY}`.
- Pinned cross-domain control: size `{EXPECTED_GROUND_DROP_SIZE}`, SHA-256 `{EXPECTED_GROUND_DROP_SHA256}`, key `{GROUND_DROP_REFERENCE_KEY}` (`GDL-IMG-015`).
- Generation stages both files under an exclusive transient lock, fsyncs them, then replaces the pair. `--check` creates no lock, temporary file, or output and verifies a stable read plus exact regenerated bytes.
- Artifact pair SHA-256: `{pair}`. The same value appears in every TSV row, detecting mixed-generation publication.

Rows: {len(rows)}. Sources: IMAGE={len(rows)}. No DUMP/CAPTURE/DATA rows. No raw client/capture/dump bytes are published.
"""
    return report.encode("utf-8")


def render_outputs(
    rows: Sequence[Mapping[str, str]], metadata: Mapping[str, object]
) -> tuple[Mapping[Path, bytes], str]:
    normalized_tsv = render_tsv(rows)
    normalized_report = render_report(rows, metadata)
    placeholder = PAIR_PLACEHOLDER.encode("ascii")
    if normalized_tsv.count(placeholder) != len(rows):
        raise RuntimeError("TSV pair-placeholder count mismatch")
    if normalized_report.count(placeholder) != 1:
        raise RuntimeError("Markdown pair-placeholder count mismatch")
    pair_sha256 = sha256(
        b"PF_QUEST_MARK_EVENT_CENSUS_TSV\0"
        + normalized_tsv
        + b"\0PF_QUEST_MARK_EVENT_CENSUS_MD\0"
        + normalized_report
    )
    replacement = pair_sha256.encode("ascii")
    outputs = {
        TSV_PATH: normalized_tsv.replace(placeholder, replacement),
        REPORT_PATH: normalized_report.replace(placeholder, replacement),
    }
    if outputs[TSV_PATH].count(replacement) != len(rows):
        raise RuntimeError("TSV pair-key injection mismatch")
    if outputs[REPORT_PATH].count(replacement) != 1:
        raise RuntimeError("Markdown pair-key injection mismatch")
    rederived = sha256(
        b"PF_QUEST_MARK_EVENT_CENSUS_TSV\0"
        + outputs[TSV_PATH].replace(replacement, placeholder)
        + b"\0PF_QUEST_MARK_EVENT_CENSUS_MD\0"
        + outputs[REPORT_PATH].replace(replacement, placeholder)
    )
    if rederived != pair_sha256:
        raise RuntimeError("artifact pair SHA-256 self-check failed")
    return outputs, pair_sha256


@contextmanager
def exclusive_publish_lock() -> Iterable[None]:
    try:
        fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise RuntimeError(f"publisher lock exists: {LOCK_PATH.name}") from exc
    try:
        with os.fdopen(fd, "w", encoding="ascii", newline="\n") as handle:
            handle.write(f"pid={os.getpid()}\n")
            handle.flush()
            os.fsync(handle.fileno())
        yield
    finally:
        try:
            LOCK_PATH.unlink()
        except FileNotFoundError:
            pass


def publish_pair(outputs: Mapping[Path, bytes]) -> None:
    staged: dict[Path, Path] = {}
    with exclusive_publish_lock():
        try:
            for path, raw in outputs.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                fd, temporary = tempfile.mkstemp(
                    prefix=path.name + ".", suffix=".tmp", dir=path.parent
                )
                temp_path = Path(temporary)
                staged[path] = temp_path
                with os.fdopen(fd, "wb") as handle:
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
            for path in (TSV_PATH, REPORT_PATH):
                os.replace(staged.pop(path), path)
        finally:
            for temp_path in staged.values():
                try:
                    temp_path.unlink()
                except FileNotFoundError:
                    pass


def verify_embedded_pair(tsv_raw: bytes, report_raw: bytes) -> str:
    with io.StringIO(tsv_raw.decode("utf-8-sig"), newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows or "artifact_pair_sha256" not in rows[0]:
        raise RuntimeError("published TSV pair-key schema drift")
    keys = {row.get("artifact_pair_sha256", "") for row in rows}
    if len(keys) != 1:
        raise RuntimeError("published TSV contains mixed pair keys")
    pair_key = next(iter(keys))
    if not re.fullmatch(r"[0-9a-f]{64}", pair_key):
        raise RuntimeError("published TSV pair key malformed")
    report_match = re.search(
        rb"Artifact pair SHA-256: `([0-9a-f]{64})`", report_raw
    )
    if report_match is None or report_match.group(1).decode("ascii") != pair_key:
        raise RuntimeError("published TSV/Markdown pair keys disagree")
    key_raw = pair_key.encode("ascii")
    placeholder = PAIR_PLACEHOLDER.encode("ascii")
    if tsv_raw.count(key_raw) != len(rows) or report_raw.count(key_raw) != 1:
        raise RuntimeError("published pair-key occurrence count drift")
    rederived = sha256(
        b"PF_QUEST_MARK_EVENT_CENSUS_TSV\0"
        + tsv_raw.replace(key_raw, placeholder)
        + b"\0PF_QUEST_MARK_EVENT_CENSUS_MD\0"
        + report_raw.replace(key_raw, placeholder)
    )
    if rederived != pair_key:
        raise RuntimeError("published artifact pair SHA-256 mismatch")
    return pair_key


def read_stable_published_pair() -> Mapping[Path, bytes]:
    if LOCK_PATH.exists():
        raise RuntimeError("publication in progress")
    first_stats = {path: path.stat() for path in (TSV_PATH, REPORT_PATH)}
    first = {path: path.read_bytes() for path in (TSV_PATH, REPORT_PATH)}
    middle_stats = {path: path.stat() for path in (TSV_PATH, REPORT_PATH)}
    second = {path: path.read_bytes() for path in (TSV_PATH, REPORT_PATH)}
    final_stats = {path: path.stat() for path in (TSV_PATH, REPORT_PATH)}
    if LOCK_PATH.exists():
        raise RuntimeError("publication overlapped --check")
    for path in (TSV_PATH, REPORT_PATH):
        signatures = {
            (stat.st_size, stat.st_mtime_ns)
            for stat in (first_stats[path], middle_stats[path], final_stats[path])
        }
        if len(signatures) != 1 or first[path] != second[path]:
            raise RuntimeError(f"unstable published artifact during --check: {path.name}")
    verify_embedded_pair(first[TSV_PATH], first[REPORT_PATH])
    return first


def input_signature(path: Path) -> tuple[int, int, str]:
    stat = path.stat()
    raw = path.read_bytes()
    return stat.st_size, stat.st_mtime_ns, sha256(raw)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="ascii", errors="backslashreplace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="ascii", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()

    input_paths = (IMAGE_PATH, SELECTOR_PATH, GROUND_DROP_PATH)
    before = {path: input_signature(path) for path in input_paths}
    if before[IMAGE_PATH][0] != EXPECTED_IMAGE_SIZE or before[IMAGE_PATH][2] != EXPECTED_IMAGE_SHA256:
        raise RuntimeError("image size/hash guard failed")
    image = IMAGE_PATH.read_bytes()
    rows, metadata, selector_keys, ground_keys = derive(image)
    validate_rows(rows, selector_keys, ground_keys)
    outputs, pair_sha256 = render_outputs(rows, metadata)

    after = {path: input_signature(path) for path in input_paths}
    if before != after:
        raise RuntimeError("an input changed during derivation")

    if args.check:
        published = read_stable_published_pair()
        for path, expected in outputs.items():
            if published[path] != expected:
                raise RuntimeError(f"output drift: {path.name}")
        print(
            f"PASS rows={len(rows)} source=IMAGE image_sha256={EXPECTED_IMAGE_SHA256} "
            f"pair_sha256={pair_sha256}"
        )
        return 0

    publish_pair(outputs)
    print(
        f"WROTE rows={len(rows)} source=IMAGE image_sha256={EXPECTED_IMAGE_SHA256} "
        f"pair_sha256={pair_sha256}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        diagnostic = str(exc).encode("ascii", "backslashreplace").decode("ascii")
        print(f"ERROR: {diagnostic}", file=sys.stderr)
        raise SystemExit(1)
