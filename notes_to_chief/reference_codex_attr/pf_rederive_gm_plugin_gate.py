#!/usr/bin/env python3
"""Re-derive the bounded GameMaster plug-in gate from GameClient.local.bin.

This tool is deliberately dependency-free.  It validates the exact PE image,
imports, strings, vtable cells, and code-span hashes before emitting any claim.
It never executes the client or a DLL and never emits source bytes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import struct
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
GUI_MODEL_DIR = PF_ROOT / "GameClient" / "Data" / "GUI" / "Model"
GM_PROJECT_PATH = GUI_MODEL_DIR / "GMUI.project"
GM_MODEL_PATH = GUI_MODEL_DIR / "GMUI_1.model"
TSV_PATH = OUT_DIR / "PF_GM_PLUGIN_GATE.tsv"
MD_PATH = OUT_DIR / "PF_GM_PLUGIN_GATE.md"
PAIR_PATH = OUT_DIR / "PF_GM_PLUGIN_GATE.pair.json"
LOCK_PATH = OUT_DIR / ".pf_rederive_gm_plugin_gate.lock"

EXPECTED_IMAGE_SIZE = 14_759_424
EXPECTED_IMAGE_SHA256 = (
    "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
)
EXPECTED_GM_PROJECT_SIZE = 148
EXPECTED_GM_PROJECT_SHA256 = (
    "392f17ba4aba1342ed1e0ec8133e1f2f074b94081fa1ee41bf718021746c0632"
)
EXPECTED_GM_MODEL_SIZE = 25_434
EXPECTED_GM_MODEL_SHA256 = (
    "ffd7e5d1c44ffe36b5bacc2857aa049ae6cbea69e11f62541bd0632162bbc69f"
)
EXPECTED_GUI_MODEL_COUNT = 534
EXPECTED_GATE_IDS = tuple(
    [f"GM-IMG-{index:03d}" for index in range(1, 18)]
    + [f"GM-DATA-{index:03d}" for index in range(1, 3)]
)
EXPECTED_IMAGE_ROW_COUNT = 17
EXPECTED_DATA_ROW_COUNT = 2
PASS_SCOPE = (
    "pinned_image_data_spans_direct_slot4_return_slices_exact_gate_id_set_atomic_pair_integrity;"
    "manual_context_is_hash_anchored_not_symbolic_dataflow"
)
EXPECTED_STRUCTURED_ROW_MUTATION_GUARD_CASES = 12
EXPECTED_GATE_ID_MUTATION_GUARD_CASES = 3


@dataclass(frozen=True)
class Section:
    name: str
    virtual_address: int
    virtual_size: int
    raw_offset: int
    raw_size: int
    characteristics: int


@dataclass(frozen=True)
class ApplicationMemberCensus:
    direct_displacement_occurrences: int
    true_member_references: int
    unrelated_displacement_occurrences: int
    read_references: int
    write_references: int
    class_counts: tuple[tuple[str, int], ...]
    slot_call_counts: tuple[tuple[int, int], ...]
    manually_classified_alias_stores_or_returns: int


@dataclass(frozen=True)
class AfterSlot8Census:
    fallback_region_va: int
    fallback_region_bytes: int
    pinned_cell_count: int
    pinned_cell_offsets: tuple[int, ...]
    adjacent_string_va: int
    adjacent_string_value: str
    adjacent_string_bytes_with_terminator: int
    executable_raw_reference_count: int
    text_raw_reference_count: int
    exact_push_imm32_pattern_count: int
    other_executable_section_reference_count: int


@dataclass(frozen=True)
class Slot4ReturnCensus:
    direct_call_count: int
    dispatcher_argument_uses: int
    empty_predicate_argument_uses: int
    inline_utf16_compare_uses: int
    immediate_alias_stores: int
    immediate_alias_returns: int
    immediate_deallocator_calls: int


@dataclass(frozen=True)
class ImageCensus:
    application_member: ApplicationMemberCensus
    after_slot8: AfterSlot8Census
    slot4_return: Slot4ReturnCensus
    direct_slot8_rel32_branch_count: int


class PE32:
    def __init__(self, data: bytes) -> None:
        self.data = data
        if data[:2] != b"MZ":
            raise ValueError("missing MZ header")
        self.pe_offset = self.u32(0x3C)
        if data[self.pe_offset : self.pe_offset + 4] != b"PE\0\0":
            raise ValueError("missing PE signature")
        coff = self.pe_offset + 4
        self.section_count = self.u16(coff + 2)
        optional_size = self.u16(coff + 16)
        optional = coff + 20
        if self.u16(optional) != 0x10B:
            raise ValueError("image is not PE32")
        self.image_base = self.u32(optional + 28)
        self.size_of_headers = self.u32(optional + 60)
        number_of_directories = self.u32(optional + 92)
        if number_of_directories < 2:
            raise ValueError("PE import directory is absent")
        directory = optional + 96
        self.import_rva = self.u32(directory + 8)
        self.import_size = self.u32(directory + 12)
        section_table = optional + optional_size
        sections: list[Section] = []
        for index in range(self.section_count):
            entry = section_table + index * 40
            raw_name = data[entry : entry + 8].split(b"\0", 1)[0]
            sections.append(
                Section(
                    raw_name.decode("ascii"),
                    self.u32(entry + 12),
                    self.u32(entry + 8),
                    self.u32(entry + 20),
                    self.u32(entry + 16),
                    self.u32(entry + 36),
                )
            )
        self.sections = tuple(sections)

    def u16(self, offset: int) -> int:
        return struct.unpack_from("<H", self.data, offset)[0]

    def u32(self, offset: int) -> int:
        return struct.unpack_from("<I", self.data, offset)[0]

    def rva_to_offset(self, rva: int) -> int:
        if 0 <= rva < self.size_of_headers:
            return rva
        for section in self.sections:
            extent = max(section.virtual_size, section.raw_size)
            if section.virtual_address <= rva < section.virtual_address + extent:
                delta = rva - section.virtual_address
                if delta >= section.raw_size:
                    raise ValueError(f"RVA 0x{rva:08X} is not backed by file bytes")
                return section.raw_offset + delta
        raise ValueError(f"RVA 0x{rva:08X} is outside mapped sections")

    def va_to_offset(self, va: int) -> int:
        return self.rva_to_offset(va - self.image_base)

    def c_string(self, va: int) -> str:
        start = self.va_to_offset(va)
        end = self.data.index(b"\0", start)
        return self.data[start:end].decode("ascii")

    def w_string(self, va: int) -> str:
        start = self.va_to_offset(va)
        cursor = start
        chunks: list[bytes] = []
        while self.data[cursor : cursor + 2] != b"\0\0":
            chunks.append(self.data[cursor : cursor + 2])
            cursor += 2
        return b"".join(chunks).decode("utf-16le")

    def import_map(self) -> dict[int, tuple[str, str]]:
        imports: dict[int, tuple[str, str]] = {}
        descriptor = self.rva_to_offset(self.import_rva)
        while True:
            original_thunk, stamp, forwarder, name_rva, first_thunk = struct.unpack_from(
                "<IIIII", self.data, descriptor
            )
            if not any((original_thunk, stamp, forwarder, name_rva, first_thunk)):
                break
            dll = self.read_rva_c_string(name_rva)
            lookup_rva = original_thunk or first_thunk
            index = 0
            while True:
                thunk = self.u32(self.rva_to_offset(lookup_rva + index * 4))
                if thunk == 0:
                    break
                if thunk & 0x80000000:
                    symbol = f"ordinal_{thunk & 0xFFFF}"
                else:
                    symbol = self.read_rva_c_string(thunk + 2)
                iat_va = self.image_base + first_thunk + index * 4
                imports[iat_va] = (dll, symbol)
                index += 1
            descriptor += 20
        return imports

    def read_rva_c_string(self, rva: int) -> str:
        start = self.rva_to_offset(rva)
        end = self.data.index(b"\0", start)
        return self.data[start:end].decode("ascii")


SPAN_SPECS: dict[str, tuple[int, int, str]] = {
    "loader": (
        0x00406720,
        0x00406791,
        "120604819103b24b0563d1d68c568a98be3bdc5d547451697cc8f6bf4dbb6894",
    ),
    "init_call": (
        0x0040A461,
        0x0040A474,
        "1d709f19a2ca069dc156f73cc0d1450bffe7092198c4265832b4dd1f523ffd5a",
    ),
    "cleanup": (
        0x0040A597,
        0x0040A5C1,
        "784e572c86b189632b041d7394adcd635f23bda915728dc478711588dae4fa18",
    ),
    "show_gate": (
        0x0053B19C,
        0x0053B1D9,
        "dd3da82a11a7f17bf53ae742e9a9e71da47541fdb1c6150be1009c8f326d61fc",
    ),
    "state_query": (
        0x0044A3B0,
        0x0044A45D,
        "755bd9a1ebbb74267afd4143c3df2032065b152e0082bffcfc4fe3993fce386e",
    ),
    "state_adapter": (
        0x00726D30,
        0x00726D62,
        "bba473c432f5bedf3f6f2d281c4450e304601faa44e7999b29b1b31898159e48",
    ),
    "click_gate": (
        0x0053BC51,
        0x0053BC96,
        "0fbd32d41059ee8370a1e89aeb30c7c5c8bea1ec73688e9a14363759e1a86338",
    ),
    "dispatcher": (
        0x00AA0710,
        0x00AA0799,
        "62fd9c6fdb6a85443ec6f2657495caf2c26f1ea580b432195c26f89b171a2d99",
    ),
    "empty_predicate": (
        0x008946C0,
        0x008946EA,
        "b0bbaf964a64e41c6abf2c8a2c691cfaa40f9d7cad2ec118aeab871a9cb8ac93",
    ),
    "factory": (
        0x007280D0,
        0x007281B8,
        "e6209b9021e4e3c689c3b8b75c18b8b1c60840e8761229ab6d4b4e37eb98de34",
    ),
    "gmui_request": (
        0x00726DF0,
        0x00726E28,
        "02f7d73b8034852ca07d2082e79190f63c664ae92666743d5f42754952f06a85",
    ),
    "fallback_getter": (
        0x009F17E0,
        0x009F17E3,
        "4bc724f3b1d0caf4fe369c18cba3102e6c4ea057f63fe1587e3973134a7f755e",
    ),
    "fallback_slot0": (
        0x00407E10,
        0x00407E33,
        "efc0f5f31a2d5b2b35a626228a37dda56bd4b888675e73acb5e405136ffcadfc",
    ),
    "fallback_slot8": (
        0x00403C00,
        0x00403C1D,
        "041a5e36bb84c648f777132572e6334f3aaa10303ca7fde12eda54320826b63a",
    ),
    "fallback_vtable": (
        0x00F09AF0,
        0x00F09AFC,
        "0b5e81ca6e86d94434719015a4a1adcc20006f7c7e4260ff5e4a6c819e1ddf0a",
    ),
    "fallback_after_slot8_string": (
        0x00F09AFC,
        0x00F09B06,
        "e2cd87d16d16dc584b6724475c92210ed323de9c4c7d07dbb50fc0bbc5983e09",
    ),
    "fallback_vtable_slots": (
        0x00F09AF0,
        0x00F09AF8,
        "267a315e964a3246de4c74926c7c4944e140a4d07f902d7cc60d647d18df5c27",
    ),
    "slot0_call_route": (
        0x0042753D,
        0x00427575,
        "bba7b6580cd45d3fb973c5d15c036a5c7cce1c0db7d874d8a5c5b3db3221808b",
    ),
    "slot4_dispatch_route": (
        0x0042C695,
        0x0042C6DF,
        "0a910ddb367e4f7cbe592062c8744e7fcd4e45706fbc7346355d95df489ea9c5",
    ),
    "loader_export_store": (
        0x0040674A,
        0x00406762,
        "d47977bd69397d700653cb0f574f142a84a17b757c498908d3aee592f864ace7",
    ),
    "loader_fallback_store": (
        0x0040676B,
        0x00406787,
        "f5be7ee21874ecc01afcb823e3a0cb537a241e10d9625f205d56311a6b4fdb96",
    ),
    "direct_cleanup": (
        0x0040A597,
        0x0040A5B0,
        "2a97b0ff405b7899ebb9312be67a6eefdeae80c0f41dc3c7ec19d9681557b49e",
    ),
    "constructor_pointer_zero": (
        0x0040AC22,
        0x0040AC3A,
        "99e5899c072d3c0e32bdb477b5473c12d08606d1291c7009c888e1be06f5fb8b",
    ),
    "resolver_setup": (
        0x00408563,
        0x004085F0,
        "a68dc4c1ec6aef9515d47e7dc6088d98b5a87bef2afd800754639f17580f1cf7",
    ),
    "gui_model_resolver": (
        0x00A91070,
        0x00A91356,
        "01ae46123661da6c96e954170480cf32d2b933bc8dfc6a1b90e6ab39b72deba3",
    ),
    "dll_string": (
        0x00F09C88,
        0x00F09CA6,
        "227e313647d01c08d2de6092540e4dd15f8faf9b53a2f2afb10366e819aa63da",
    ),
    "export_string": (
        0x00F09C74,
        0x00F09C85,
        "2918771318875f7b6188d0eb9a5cd1ab392ba7a1a92882af5431f5b608306a97",
    ),
    "key_string": (
        0x00F461EC,
        0x00F46202,
        "8cd981c57aff6459967b713667022dd41a3494058d6c731a36c0e142b64328cb",
    ),
}


# Exact instruction bytes at every true application-member reference.  The
# .text-wide little-endian 0x7C8 census has one additional occurrence at
# 0x00675FC0, but that is the displacement inside LEA [ESP+0x7C8] and is
# deliberately pinned as an unrelated stack local below.
APP_MEMBER_REFS: dict[int, tuple[str, bytes]] = {
    0x00406723: ("R", bytes.fromhex("83bec807000000")),
    0x0040675C: ("W", bytes.fromhex("8986c8070000")),
    0x00406762: ("R", bytes.fromhex("83bec807000000")),
    0x0040677F: ("W", bytes.fromhex("8986c8070000")),
    0x00406789: ("W", bytes.fromhex("8986c8070000")),
    0x0040A597: ("R", bytes.fromhex("8b86c8070000")),
    0x0040A5AA: ("W", bytes.fromhex("899ec8070000")),
    0x0040AC2E: ("W", bytes.fromhex("899ec8070000")),
    0x0042753D: ("R", bytes.fromhex("83b8c807000000")),
    0x0042755F: ("R", bytes.fromhex("8b89c8070000")),
    0x0042C6BB: ("R", bytes.fromhex("8b8ac8070000")),
    0x0053B1A1: ("R", bytes.fromhex("83b8c807000000")),
    0x0053BC6E: ("R", bytes.fromhex("8b88c8070000")),
    0x007280F6: ("R", bytes.fromhex("8b88c8070000")),
    0x00728122: ("R", bytes.fromhex("8b89c8070000")),
}

# Manual semantic classification is kept separate from the exact byte pins
# above.  It closes copied-alias production only for this direct-displacement
# census; it deliberately says nothing about a split-address construction.
APP_MEMBER_REF_CLASSES: dict[int, str] = {
    0x00406723: "guard_read",
    0x0040675C: "plugin_return_write",
    0x00406762: "guard_read",
    0x0040677F: "fallback_return_write",
    0x00406789: "allocation_failure_zero_write",
    0x0040A597: "scalar_delete_read",
    0x0040A5AA: "cleanup_zero_write",
    0x0040AC2E: "constructor_zero_write",
    0x0042753D: "guard_read",
    0x0042755F: "slot0_call_read",
    0x0042C6BB: "slot4_call_read",
    0x0053B1A1: "guard_read",
    0x0053BC6E: "slot4_call_read",
    0x007280F6: "slot4_call_read",
    0x00728122: "slot4_call_read",
}

# This is an explicitly manual semantic bucket, not a symbolic dataflow rule.
# No current pinned reference is assigned either class.
MANUAL_ALIAS_PRODUCING_CLASSES = frozenset(
    {"copied_interface_alias_store", "copied_interface_alias_return"}
)

# These are immediate-field VAs, not instruction starts.  Every occurrence is
# required to be the operand of an exact PUSH imm32 (opcode 0x68 immediately
# before it), and every other executable section must have zero occurrences.
EXPECTED_AFTER_SLOT8_STRING_IMMEDIATE_VAS = {
    0x00403DDE,
    0x004F4DA8,
    0x004F4E3F,
    0x004F4F6A,
    0x004F5002,
    0x004F512A,
    0x004F51C2,
    0x004F52EA,
    0x004F5382,
    0x004F54AA,
    0x004F5542,
    0x004FF8B9,
    0x0054CD61,
    0x005555D0,
    0x0055565D,
    0x005556E9,
    0x0055D7CB,
    0x0055D81E,
    0x0055D86E,
    0x0055D8BD,
    0x0055F085,
    0x00594788,
    0x005ABC95,
    0x005AD2B4,
    0x005ADCE4,
    0x005ADF59,
    0x005B5E7E,
    0x005B5F59,
    0x005B600C,
    0x005CBF61,
    0x005CBFDE,
    0x0067E6C3,
    0x0070E735,
}

EXPECTED_7C8_DISPLACEMENT_VAS = {
    0x00406725,
    0x0040675E,
    0x00406764,
    0x00406781,
    0x0040678B,
    0x0040A599,
    0x0040A5AC,
    0x0040AC30,
    0x0042753F,
    0x00427561,
    0x0042C6BD,
    0x0053B1A3,
    0x0053BC70,
    0x00675FC0,
    0x007280F8,
    0x00728124,
}

INTERFACE_CALLS: dict[int, tuple[int, bytes, bytes]] = {
    # call VA: (vtable-target load VA, exact target-load bytes, exact call bytes)
    0x00427573: (0x00427567, bytes.fromhex("8b12"), bytes.fromhex("ffd2")),
    0x0042C6D2: (0x0042C6C3, bytes.fromhex("8b5004"), bytes.fromhex("ffd2")),
    0x0053BC89: (0x0053BC7A, bytes.fromhex("8b4204"), bytes.fromhex("ffd0")),
    0x00728109: (0x00728106, bytes.fromhex("8b4204"), bytes.fromhex("ffd0")),
    0x00728131: (0x0072812A, bytes.fromhex("8b4204"), bytes.fromhex("ffd0")),
}

# Complete immediate EAX-consumer slices for the four slot +0x04 calls in the
# mechanically closed direct application-member call set.  The category names
# are manual/hash-anchored interpretation; the addresses, bytes, and count are
# checked mechanically.  These slices deliberately do not claim symbolic
# behavior inside callees reached after the immediate use.
SLOT4_RETURN_USE_SLICES: dict[int, tuple[str, bytes]] = {
    0x0042C6D2: (
        "dispatcher_argument",
        bytes.fromhex("ffd250b908070901e831406700"),
    ),
    0x0053BC89: (
        "dispatcher_argument",
        bytes.fromhex("ffd050b908070901e87a4a5600"),
    ),
    0x00728109: (
        "empty_predicate_argument",
        bytes.fromhex("ffd050e8afc5160083c40484c00f8587000000"),
    ),
    0x00728131: (
        "inline_utf16_compare",
        bytes.fromhex(
            "ffd0668b08663b0e751e6685c97415668b4802663b4e02750f83c00483c604"
            "6685c975de33c0eb051bc083d8ff"
        ),
    ),
}

SLOT8_BODY_INSTRUCTIONS: dict[int, bytes] = {
    0x00403C00: bytes.fromhex("5156"),
    0x00403C02: bytes.fromhex("8b74240c"),
    0x00403C06: bytes.fromhex("8bce"),
    0x00403C08: bytes.fromhex("c744240400000000"),
    0x00403C10: bytes.fromhex("ff1578b4c300"),
    0x00403C16: bytes.fromhex("8bc6"),
    0x00403C18: bytes.fromhex("5e59"),
    0x00403C1A: bytes.fromhex("c20400"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def span_label(name: str, pe: PE32) -> str:
    start, end, digest = SPAN_SPECS[name]
    return (
        f"{name}=0x{start:08X}..0x{end:08X}"
        f"@file:0x{pe.va_to_offset(start):08X}..0x{pe.va_to_offset(end):08X}"
        f"@sha256:{digest}"
    )


def decode_vtable_target_load(instruction: bytes) -> tuple[int, int]:
    """Return (non-negative vtable displacement, destination register)."""
    if len(instruction) < 2 or instruction[0] != 0x8B:
        raise ValueError("interface target load is not MOV r32,[r32+disp]")
    modrm = instruction[1]
    mode = modrm >> 6
    destination_register = (modrm >> 3) & 7
    base_register = modrm & 7
    if mode == 0 and base_register != 5 and len(instruction) == 2:
        displacement = 0
    elif mode == 1 and len(instruction) == 3:
        displacement = struct.unpack("<b", instruction[2:3])[0]
    else:
        raise ValueError(
            "interface target load uses an unsupported addressing form: "
            f"{instruction.hex()}"
        )
    if displacement < 0:
        raise ValueError(f"negative interface vtable displacement: {displacement}")
    return displacement, destination_register


def decode_indirect_call_register(instruction: bytes) -> int:
    if len(instruction) != 2 or instruction[0] != 0xFF:
        raise ValueError("interface call is not a two-byte indirect register call")
    modrm = instruction[1]
    if modrm >> 6 != 3 or (modrm >> 3) & 7 != 2:
        raise ValueError(f"interface call opcode mismatch: {instruction.hex()}")
    return modrm & 7


def decode_pinned_member_access(instruction: bytes) -> str:
    """Mechanically classify the exact supported x86 member-reference forms."""
    if len(instruction) < 2:
        raise ValueError("truncated application+0x7C8 instruction")
    opcode = instruction[0]
    modrm = instruction[1]
    if modrm >> 6 == 3:
        raise ValueError("application+0x7C8 instruction unexpectedly uses register mode")
    if opcode == 0x8B:
        return "R"
    if opcode == 0x89:
        return "W"
    if opcode == 0x83 and ((modrm >> 3) & 7) == 7:
        return "R"
    raise ValueError(
        "unsupported application+0x7C8 access opcode: "
        f"{instruction.hex()}"
    )


def verify_application_member_census(data: bytes, pe: PE32) -> ApplicationMemberCensus:
    if set(APP_MEMBER_REF_CLASSES) != set(APP_MEMBER_REFS):
        raise ValueError("application+0x7C8 semantic-class key census mismatch")
    decoded_modes: dict[int, str] = {}
    for va, (declared_mode, expected) in APP_MEMBER_REFS.items():
        start = pe.va_to_offset(va)
        actual = data[start : start + len(expected)]
        if actual != expected:
            raise ValueError(
                f"application+0x7C8 reference mismatch at 0x{va:08X}: "
                f"expected {expected.hex()}, got {actual.hex()}"
            )
        decoded_mode = decode_pinned_member_access(actual)
        if decoded_mode != declared_mode:
            raise ValueError(
                f"application+0x7C8 declared/decoded mode mismatch at 0x{va:08X}"
            )
        decoded_modes[va] = decoded_mode
    read_count = sum(mode == "R" for mode in decoded_modes.values())
    write_count = sum(mode == "W" for mode in decoded_modes.values())
    if read_count != 10:
        raise ValueError("application+0x7C8 read census mismatch")
    if write_count != 5:
        raise ValueError("application+0x7C8 write census mismatch")
    class_counts: dict[str, int] = {}
    for va, semantic_class in APP_MEMBER_REF_CLASSES.items():
        mode = decoded_modes[va]
        expected_mode = "R" if semantic_class.endswith("_read") else "W"
        if mode != expected_mode:
            raise ValueError(
                f"application+0x7C8 semantic-class mode mismatch at 0x{va:08X}"
            )
        class_counts[semantic_class] = class_counts.get(semantic_class, 0) + 1
    expected_class_counts = {
        "guard_read": 4,
        "scalar_delete_read": 1,
        "slot0_call_read": 1,
        "slot4_call_read": 4,
        "plugin_return_write": 1,
        "fallback_return_write": 1,
        "allocation_failure_zero_write": 1,
        "cleanup_zero_write": 1,
        "constructor_zero_write": 1,
    }
    if class_counts != expected_class_counts:
        raise ValueError(
            "application+0x7C8 semantic-class census mismatch: "
            f"expected={expected_class_counts!r} observed={class_counts!r}"
        )
    manual_alias_count = sum(
        semantic_class in MANUAL_ALIAS_PRODUCING_CLASSES
        for semantic_class in APP_MEMBER_REF_CLASSES.values()
    )
    if manual_alias_count != 0:
        raise ValueError(
            "manual application+0x7C8 copied-alias classification changed: "
            f"observed={manual_alias_count}"
        )

    needle = struct.pack("<I", 0x7C8)
    executable_sections = [
        section for section in pe.sections
        if section.characteristics & 0x20000000
    ]
    text_sections = [section for section in executable_sections if section.name == ".text"]
    if len(text_sections) != 1:
        raise ValueError("expected exactly one executable .text section")
    observed_by_section: dict[str, set[int]] = {}
    for section in executable_sections:
        raw = data[section.raw_offset : section.raw_offset + section.raw_size]
        observed: set[int] = set()
        cursor = 0
        while True:
            index = raw.find(needle, cursor)
            if index < 0:
                break
            observed.add(pe.image_base + section.virtual_address + index)
            cursor = index + 1
        if section.name in observed_by_section:
            raise ValueError(f"duplicate executable section name: {section.name}")
        observed_by_section[section.name] = observed
    text_observed = observed_by_section.get(".text", set())
    if text_observed != EXPECTED_7C8_DISPLACEMENT_VAS:
        raise ValueError(
            "application+0x7C8 .text displacement census mismatch: "
            f"expected={sorted(EXPECTED_7C8_DISPLACEMENT_VAS)!r} "
            f"observed={sorted(text_observed)!r}"
        )
    unexpected_exec = {
        name: sorted(observed)
        for name, observed in observed_by_section.items()
        if name != ".text" and observed
    }
    if unexpected_exec:
        raise ValueError(
            "application+0x7C8 displacement found outside .text: "
            f"{unexpected_exec!r}"
        )
    unrelated = bytes.fromhex("8d8c24c8070000")
    unrelated_start = pe.va_to_offset(0x00675FBD)
    if data[unrelated_start : unrelated_start + len(unrelated)] != unrelated:
        raise ValueError("unrelated ESP+0x7C8 stack-local guard mismatch")

    slot_counts: dict[int, int] = {}
    for call_va, (target_load_va, expected_load, expected_call) in INTERFACE_CALLS.items():
        load_start = pe.va_to_offset(target_load_va)
        actual_load = data[load_start : load_start + len(expected_load)]
        if actual_load != expected_load:
            raise ValueError(
                f"interface vtable target load mismatch at 0x{target_load_va:08X}"
            )
        call_start = pe.va_to_offset(call_va)
        actual_call = data[call_start : call_start + len(expected_call)]
        if actual_call != expected_call:
            raise ValueError(f"interface call instruction mismatch at 0x{call_va:08X}")
        slot, target_register = decode_vtable_target_load(actual_load)
        call_register = decode_indirect_call_register(actual_call)
        if target_register != call_register:
            raise ValueError(
                f"interface target/call register mismatch at 0x{call_va:08X}: "
                f"target={target_register} call={call_register}"
            )
        slot_counts[slot] = slot_counts.get(slot, 0) + 1
    if slot_counts != {0x00: 1, 0x04: 4}:
        raise ValueError(f"interface slot call census mismatch: {slot_counts!r}")
    classified_call_reads = {
        va for va, semantic_class in APP_MEMBER_REF_CLASSES.items()
        if semantic_class in {"slot0_call_read", "slot4_call_read"}
    }
    expected_call_reads = {0x0042755F, 0x0042C6BB, 0x0053BC6E, 0x007280F6, 0x00728122}
    if classified_call_reads != expected_call_reads:
        raise ValueError(
            "application+0x7C8 classified call-read census mismatch: "
            f"expected={sorted(expected_call_reads)!r} "
            f"observed={sorted(classified_call_reads)!r}"
        )
    member_displacement_vas: set[int] = set()
    for va, (_mode, expected) in APP_MEMBER_REFS.items():
        displacement_index = expected.find(needle)
        if displacement_index < 0 or expected.find(needle, displacement_index + 1) >= 0:
            raise ValueError(
                f"application+0x7C8 instruction displacement ambiguity at 0x{va:08X}"
            )
        member_displacement_vas.add(va + displacement_index)
    unrelated_displacements = text_observed - member_displacement_vas
    if unrelated_displacements != {0x00675FC0}:
        raise ValueError(
            "application+0x7C8 unrelated displacement census mismatch: "
            f"observed={sorted(unrelated_displacements)!r}"
        )
    return ApplicationMemberCensus(
        direct_displacement_occurrences=len(text_observed),
        true_member_references=len(APP_MEMBER_REFS),
        unrelated_displacement_occurrences=len(unrelated_displacements),
        read_references=read_count,
        write_references=write_count,
        class_counts=tuple(sorted(class_counts.items())),
        slot_call_counts=tuple(sorted(slot_counts.items())),
        manually_classified_alias_stores_or_returns=manual_alias_count,
    )


def verify_slot4_return_census(
    data: bytes,
    pe: PE32,
    application_member: ApplicationMemberCensus,
) -> Slot4ReturnCensus:
    slot_counts = dict(application_member.slot_call_counts)
    expected_call_vas = {
        call_va
        for call_va, (target_load_va, expected_load, _expected_call) in INTERFACE_CALLS.items()
        if decode_vtable_target_load(expected_load)[0] == 0x04
    }
    if slot_counts.get(0x04) != len(expected_call_vas):
        raise ValueError("slot +0x04 call/return-use census cardinality mismatch")
    if set(SLOT4_RETURN_USE_SLICES) != expected_call_vas:
        raise ValueError("slot +0x04 return-use slice key census mismatch")

    class_counts: dict[str, int] = {}
    for call_va, (semantic_class, expected) in SLOT4_RETURN_USE_SLICES.items():
        start = pe.va_to_offset(call_va)
        actual = data[start : start + len(expected)]
        if actual != expected:
            raise ValueError(
                f"slot +0x04 return-use slice mismatch at 0x{call_va:08X}: "
                f"expected={expected.hex()} actual={actual.hex()}"
            )
        class_counts[semantic_class] = class_counts.get(semantic_class, 0) + 1
    expected_classes = {
        "dispatcher_argument": 2,
        "empty_predicate_argument": 1,
        "inline_utf16_compare": 1,
    }
    if class_counts != expected_classes:
        raise ValueError(
            "slot +0x04 return-use class census mismatch: "
            f"expected={expected_classes!r} observed={class_counts!r}"
        )
    return Slot4ReturnCensus(
        direct_call_count=len(SLOT4_RETURN_USE_SLICES),
        dispatcher_argument_uses=class_counts["dispatcher_argument"],
        empty_predicate_argument_uses=class_counts["empty_predicate_argument"],
        inline_utf16_compare_uses=class_counts["inline_utf16_compare"],
        immediate_alias_stores=0,
        immediate_alias_returns=0,
        immediate_deallocator_calls=0,
    )


def verify_image() -> tuple[
    bytes,
    PE32,
    dict[int, tuple[str, str]],
    ImageCensus,
]:
    data = IMAGE_PATH.read_bytes()
    if len(data) != EXPECTED_IMAGE_SIZE:
        raise ValueError(
            f"image size mismatch: expected {EXPECTED_IMAGE_SIZE}, got {len(data)}"
        )
    digest = sha256(data)
    if digest != EXPECTED_IMAGE_SHA256:
        raise ValueError(
            f"image hash mismatch: expected {EXPECTED_IMAGE_SHA256}, got {digest}"
        )
    pe = PE32(data)
    if pe.image_base != 0x00400000:
        raise ValueError(f"unexpected image base 0x{pe.image_base:08X}")
    for name, (start, end, expected) in SPAN_SPECS.items():
        actual = sha256(data[pe.va_to_offset(start) : pe.va_to_offset(end)])
        if actual != expected:
            raise ValueError(f"span {name} mismatch: expected {expected}, got {actual}")
    if pe.w_string(0x00F09C88) != "GameMaster.dll":
        raise ValueError("GameMaster.dll literal mismatch")
    if pe.c_string(0x00F09C74) != "CreateGameMaster":
        raise ValueError("CreateGameMaster literal mismatch")
    if pe.w_string(0x00F461EC) != "GMUI_BASIC":
        raise ValueError("GMUI_BASIC literal mismatch")
    after_slot8_string = pe.w_string(0x00F09AFC)
    if after_slot8_string != "%s%s":
        raise ValueError("post-slot8 UTF-16 format literal mismatch")
    if pe.c_string(0x00F091DC) != ".\\Data\\GUI\\Model\\":
        raise ValueError("GUI model base-path literal mismatch")
    if pe.w_string(0x00F874D8) != "%s\\%s.model":
        raise ValueError("GUI model resolver format literal mismatch")
    vtable_offset = pe.va_to_offset(0x00F09AF0)
    vtable = struct.unpack_from("<III", data, vtable_offset)
    if vtable != (0x00407E10, 0x009F17E0, 0x00403C00):
        raise ValueError(f"fallback vtable mismatch: {vtable!r}")
    slot8_pointer = struct.pack("<I", 0x00403C00)
    slot8_pointer_offsets: list[int] = []
    cursor = 0
    while True:
        cursor = data.find(slot8_pointer, cursor)
        if cursor < 0:
            break
        slot8_pointer_offsets.append(cursor)
        cursor += 1
    expected_slot8_pointer_offset = pe.va_to_offset(0x00F09AF8)
    if slot8_pointer_offsets != [expected_slot8_pointer_offset]:
        raise ValueError(
            "fallback slot +0x08 target pointer census mismatch: "
            f"expected={[expected_slot8_pointer_offset]!r} "
            f"observed={slot8_pointer_offsets!r}"
        )
    after_slot8_string_pointer = struct.pack("<I", 0x00F09AFC)
    after_slot8_refs_by_section: dict[str, set[int]] = {}
    push_imm32_pattern_count = 0
    for section in pe.sections:
        if not section.characteristics & 0x20000000:
            continue
        raw = data[section.raw_offset : section.raw_offset + section.raw_size]
        observed: set[int] = set()
        cursor = 0
        while True:
            cursor = raw.find(after_slot8_string_pointer, cursor)
            if cursor < 0:
                break
            immediate_va = pe.image_base + section.virtual_address + cursor
            observed.add(immediate_va)
            if cursor == 0 or raw[cursor - 1] != 0x68:
                raise ValueError(
                    "post-slot8 string reference is not PUSH imm32 at "
                    f"0x{immediate_va:08X}"
                )
            push_imm32_pattern_count += 1
            cursor += 1
        if section.name in after_slot8_refs_by_section:
            raise ValueError(f"duplicate executable section name: {section.name}")
        after_slot8_refs_by_section[section.name] = observed
    text_after_slot8_refs = after_slot8_refs_by_section.get(".text", set())
    if text_after_slot8_refs != EXPECTED_AFTER_SLOT8_STRING_IMMEDIATE_VAS:
        raise ValueError(
            "post-slot8 string PUSH-immediate census mismatch: "
            f"expected={sorted(EXPECTED_AFTER_SLOT8_STRING_IMMEDIATE_VAS)!r} "
            f"observed={sorted(text_after_slot8_refs)!r}"
        )
    unexpected_after_slot8_refs = {
        name: sorted(observed)
        for name, observed in after_slot8_refs_by_section.items()
        if name != ".text" and observed
    }
    if unexpected_after_slot8_refs:
        raise ValueError(
            "post-slot8 string reference found outside .text: "
            f"{unexpected_after_slot8_refs!r}"
        )
    executable_after_slot8_reference_count = sum(
        len(observed) for observed in after_slot8_refs_by_section.values()
    )
    other_exec_after_slot8_reference_count = sum(
        len(observed)
        for name, observed in after_slot8_refs_by_section.items()
        if name != ".text"
    )
    if executable_after_slot8_reference_count != 33:
        raise ValueError("post-slot8 executable raw-reference count mismatch")
    if push_imm32_pattern_count != executable_after_slot8_reference_count:
        raise ValueError("post-slot8 PUSH-imm32 pattern count mismatch")
    if other_exec_after_slot8_reference_count != 0:
        raise ValueError("post-slot8 other-executable-section count mismatch")
    for instruction_va, expected_instruction in SLOT8_BODY_INSTRUCTIONS.items():
        instruction_offset = pe.va_to_offset(instruction_va)
        actual_instruction = data[
            instruction_offset : instruction_offset + len(expected_instruction)
        ]
        if actual_instruction != expected_instruction:
            raise ValueError(
                f"fallback slot +0x08 body mismatch at 0x{instruction_va:08X}: "
                f"expected={expected_instruction.hex()} actual={actual_instruction.hex()}"
            )
    direct_slot8_rel32_branches: list[tuple[int, str]] = []
    for section in pe.sections:
        if not section.characteristics & 0x20000000:
            continue
        raw = data[section.raw_offset : section.raw_offset + section.raw_size]
        for index in range(len(raw) - 4):
            opcode = raw[index]
            if opcode not in (0xE8, 0xE9):
                continue
            branch_va = pe.image_base + section.virtual_address + index
            displacement = struct.unpack_from("<i", raw, index + 1)[0]
            if (branch_va + 5 + displacement) & 0xFFFFFFFF == 0x00403C00:
                kind = "call" if opcode == 0xE8 else "tail_jump"
                direct_slot8_rel32_branches.append((branch_va, kind))
    if direct_slot8_rel32_branches:
        raise ValueError(
            "unexpected direct rel32 branch to fallback slot +0x08 target: "
            f"{direct_slot8_rel32_branches!r}"
        )
    application_member_census = verify_application_member_census(data, pe)
    slot4_return_census = verify_slot4_return_census(
        data, pe, application_member_census
    )
    imports = pe.import_map()
    expected_imports = {
        0x00C3B1C0: ("KERNEL32.dll", "LoadLibraryW"),
        0x00C3B1BC: ("KERNEL32.dll", "GetProcAddress"),
        0x00C3B23C: ("KERNEL32.dll", "FreeLibrary"),
        0x00C3B4BC: ("MSVCR90.dll", "??2@YAPAXI@Z"),
        0x00C3B478: (
            "MSVCP90.dll",
            "??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ",
        ),
        0x00C3B82C: ("MSVCR90.dll", "??3@YAXPAX@Z"),
    }
    for va, expected in expected_imports.items():
        actual = imports.get(va)
        if actual != expected:
            raise ValueError(
                f"import 0x{va:08X} mismatch: expected {expected!r}, got {actual!r}"
            )
    image_census = ImageCensus(
        application_member=application_member_census,
        after_slot8=AfterSlot8Census(
            fallback_region_va=0x00F09AF0,
            fallback_region_bytes=len(vtable) * 4,
            pinned_cell_count=len(vtable),
            pinned_cell_offsets=tuple(index * 4 for index in range(len(vtable))),
            adjacent_string_va=0x00F09AFC,
            adjacent_string_value=after_slot8_string,
            adjacent_string_bytes_with_terminator=(len(after_slot8_string) + 1) * 2,
            executable_raw_reference_count=executable_after_slot8_reference_count,
            text_raw_reference_count=len(text_after_slot8_refs),
            exact_push_imm32_pattern_count=push_imm32_pattern_count,
            other_executable_section_reference_count=(
                other_exec_after_slot8_reference_count
            ),
        ),
        slot4_return=slot4_return_census,
        direct_slot8_rel32_branch_count=len(direct_slot8_rel32_branches),
    )
    if image_census.after_slot8.fallback_region_bytes != 12:
        raise ValueError("fallback three-cell region byte count mismatch")
    if image_census.after_slot8.pinned_cell_offsets != (0x00, 0x04, 0x08):
        raise ValueError("fallback pinned-cell offset census mismatch")
    if image_census.after_slot8.adjacent_string_bytes_with_terminator != 10:
        raise ValueError("post-slot8 UTF-16 byte length mismatch")
    return data, pe, imports, image_census


def verify_data() -> dict[str, object]:
    project = GM_PROJECT_PATH.read_bytes()
    model = GM_MODEL_PATH.read_bytes()
    if len(project) != EXPECTED_GM_PROJECT_SIZE:
        raise ValueError(
            f"GMUI.project size mismatch: expected {EXPECTED_GM_PROJECT_SIZE}, "
            f"got {len(project)}"
        )
    if sha256(project) != EXPECTED_GM_PROJECT_SHA256:
        raise ValueError("GMUI.project hash mismatch")
    if len(model) != EXPECTED_GM_MODEL_SIZE:
        raise ValueError(
            f"GMUI_1.model size mismatch: expected {EXPECTED_GM_MODEL_SIZE}, "
            f"got {len(model)}"
        )
    if sha256(model) != EXPECTED_GM_MODEL_SHA256:
        raise ValueError("GMUI_1.model hash mismatch")

    project_root = ET.fromstring(project.decode("utf-8"))
    if project_root.tag != "Project" or project_root.get("Name") != "GMUI":
        raise ValueError("GMUI.project root mismatch")
    project_models = [node.get("Name") for node in project_root.findall("./Models/Model")]
    if project_models != ["GMUI_1"]:
        raise ValueError(f"GMUI.project model census mismatch: {project_models!r}")

    model_root = ET.fromstring(model.decode("utf-8"))
    windows = [
        node for node in model_root.findall("./SourceData/BigUIStandardWindow")
        if node.get("ID") == "GMUI_1"
    ]
    tabs = [
        node for node in model_root.iter("UITabPage")
        if node.get("ID") == "GMUI_BASIC"
    ]
    if len(windows) != 1 or len(tabs) != 1:
        raise ValueError(
            f"GMUI_1.model control census mismatch: windows={len(windows)} "
            f"tabs={len(tabs)}"
        )

    subdirectories = sorted(path for path in GUI_MODEL_DIR.rglob("*") if path.is_dir())
    if subdirectories:
        raise ValueError(
            "GUI model corpus gained subdirectories: "
            f"{[str(path.relative_to(GUI_MODEL_DIR)) for path in subdirectories]!r}"
        )
    model_files = sorted(
        path for path in GUI_MODEL_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() == ".model"
    )
    if len(model_files) != EXPECTED_GUI_MODEL_COUNT:
        raise ValueError(
            f"GUI model file census mismatch: expected {EXPECTED_GUI_MODEL_COUNT}, "
            f"got {len(model_files)}"
        )
    control_hits = [path for path in model_files if b"GMUI_BASIC" in path.read_bytes()]
    if control_hits != [GM_MODEL_PATH]:
        raise ValueError(
            "GMUI_BASIC model-file census mismatch: "
            f"{[path.name for path in control_hits]!r}"
        )
    gmui_basic_models = [
        path for path in model_files
        if path.name.casefold() == "gmui_basic.model"
    ]
    if gmui_basic_models:
        raise ValueError(
            "unexpected GMUI_BASIC.model case variant: "
            f"{[path.name for path in gmui_basic_models]!r}"
        )
    return {
        "project": project,
        "model": model,
        "model_count": len(model_files),
        "subdirectory_count": len(subdirectories),
        "gmui_basic_model_count": len(gmui_basic_models),
    }


def gm_img_015_fields(census: ApplicationMemberCensus) -> dict[str, str]:
    classes = dict(census.class_counts)
    slots = dict(census.slot_call_counts)
    inline_calls = sum(slots.values())
    exact_static_fact = (
        "[MECHANICAL] Direct displacement occurrences="
        f"{census.direct_displacement_occurrences}; true member refs="
        f"{census.true_member_references}; unrelated occurrences="
        f"{census.unrelated_displacement_occurrences}; reads={census.read_references}; "
        f"writes={census.write_references}; decoded inline virtual calls={inline_calls} "
        f"(slot +0x00={slots[0x00]}, slot +0x04={slots[0x04]}). "
        "[MANUAL_HASH_ANCHORED] Contextual classification of the exact pinned slices is "
        f"guards={classes['guard_read']}, scalar-delete cleanup="
        f"{classes['scalar_delete_read']}, constructor-zero writes="
        f"{classes['constructor_zero_write']}, plug-in-return writes="
        f"{classes['plugin_return_write']}, fallback-return writes="
        f"{classes['fallback_return_write']}, allocation-failure-zero writes="
        f"{classes['allocation_failure_zero_write']}, cleanup-zero writes="
        f"{classes['cleanup_zero_write']}, and copied interface alias stores/returns="
        f"{census.manually_classified_alias_stores_or_returns}. The export return is stored "
        "directly to application+0x7C8; the fallback allocation receives only its pinned "
        "vtable write before the same member store."
    )
    required_interface_fact = "; ".join(
        (
            f"mechanical_displacement_occurrences={census.direct_displacement_occurrences}",
            f"mechanical_true_member_refs={census.true_member_references}",
            f"mechanical_unrelated_occurrences={census.unrelated_displacement_occurrences}",
            f"mechanical_reads={census.read_references}",
            f"mechanical_writes={census.write_references}",
            f"mechanical_inline_virtual_calls={inline_calls}",
            f"mechanical_slot_+0x00_calls={slots[0x00]}",
            f"mechanical_slot_+0x04_calls={slots[0x04]}",
            f"manual_guard_reads={classes['guard_read']}",
            f"manual_scalar_delete_reads={classes['scalar_delete_read']}",
            (
                "manual_alias_stores_or_returns="
                f"{census.manually_classified_alias_stores_or_returns}"
            ),
        )
    )
    return {
        "exact_static_fact": exact_static_fact,
        "semantic_status": (
            "MECHANICAL_COUNTS_PROVEN_EXACT_CONTEXT_MANUAL_HASH_ANCHORED"
        ),
        "required_interface_fact": required_interface_fact,
        "nonclaim": (
            "The generator mechanically verifies the raw occurrence census, exact pinned bytes, "
            "read/write pins, and vtable target/call-register decoding. It does not perform symbolic "
            "dataflow: guard/delete/write-role/no-alias labels are manual contextual interpretation "
            "anchored to those exact slices. This closes copied-alias production only for the pinned "
            "direct references, not pointer arithmetic, split-address construction, or an alias "
            "retained inside the missing DLL or another callee."
        ),
    }


def gm_img_016_fields(census: AfterSlot8Census) -> dict[str, str]:
    offsets = ",".join(f"+0x{offset:02X}" for offset in census.pinned_cell_offsets)
    exact_static_fact = (
        f"[MECHANICAL] Fallback cell-region bytes={census.fallback_region_bytes}; "
        f"pinned cells={census.pinned_cell_count}; offsets={offsets}. The adjacent bytes at "
        f"+0x{census.fallback_region_bytes:02X} decode as UTF-16 "
        f"{census.adjacent_string_value} plus terminator "
        f"({census.adjacent_string_bytes_with_terminator} bytes). Across executable sections, "
        f"raw address refs={census.executable_raw_reference_count}; .text refs="
        f"{census.text_raw_reference_count}; exact PUSH-imm32 byte-pattern refs="
        f"{census.exact_push_imm32_pattern_count}; other executable-section refs="
        f"{census.other_executable_section_reference_count}."
    )
    required_interface_fact = "; ".join(
        (
            f"fallback_region_bytes={census.fallback_region_bytes}",
            f"pinned_cells={census.pinned_cell_count}",
            f"pinned_cell_offsets={offsets}",
            f"adjacent_string_va=0x{census.adjacent_string_va:08X}",
            f"adjacent_string=UTF16_{census.adjacent_string_value}",
            (
                "adjacent_string_bytes_with_terminator="
                f"{census.adjacent_string_bytes_with_terminator}"
            ),
            f"executable_raw_refs={census.executable_raw_reference_count}",
            f"text_raw_refs={census.text_raw_reference_count}",
            f"exact_push_imm32_patterns={census.exact_push_imm32_pattern_count}",
            (
                "other_executable_section_refs="
                f"{census.other_executable_section_reference_count}"
            ),
        )
    )
    return {
        "exact_static_fact": exact_static_fact,
        "semantic_status": "PROVEN_EXACT_STRUCTURED_BYTE_AND_PUSH_PATTERN_CENSUS",
        "required_interface_fact": required_interface_fact,
        "nonclaim": (
            "This mechanically proves the concrete three-cell-region/string adjacency and raw "
            "reference patterns. It does not independently prove a source-level vtable length, "
            "instruction reachability/execution, exclude deliberate dual use of adjacent bytes, "
            "show that the absent DLL exposed no private methods, or close a split-address route."
        ),
    }


def gm_img_017_fields(census: Slot4ReturnCensus) -> dict[str, str]:
    exact_static_fact = (
        f"[MECHANICAL] The closed direct-member set has slot +0x04 calls="
        f"{census.direct_call_count}, each with an exact pinned immediate EAX-consumer slice. "
        "[MANUAL_HASH_ANCHORED] Those slices classify as dispatcher arguments="
        f"{census.dispatcher_argument_uses}, empty-predicate arguments="
        f"{census.empty_predicate_argument_uses}, and inline UTF-16 compares="
        f"{census.inline_utf16_compare_uses}; immediate alias stores="
        f"{census.immediate_alias_stores}, immediate alias returns="
        f"{census.immediate_alias_returns}, and immediate deallocator calls="
        f"{census.immediate_deallocator_calls}. The factory invokes the getter twice: "
        "once for the null/empty test and again for the exact comparison."
    )
    required_interface_fact = "; ".join(
        (
            f"mechanical_slot_+0x04_return_slices={census.direct_call_count}",
            f"manual_dispatcher_arguments={census.dispatcher_argument_uses}",
            (
                "manual_empty_predicate_arguments="
                f"{census.empty_predicate_argument_uses}"
            ),
            f"manual_inline_UTF16_compares={census.inline_utf16_compare_uses}",
            f"manual_immediate_alias_stores={census.immediate_alias_stores}",
            f"manual_immediate_alias_returns={census.immediate_alias_returns}",
            (
                "manual_immediate_deallocator_calls="
                f"{census.immediate_deallocator_calls}"
            ),
        )
    )
    return {
        "exact_static_fact": exact_static_fact,
        "semantic_status": (
            "MECHANICAL_SLICES_PROVEN_EXACT_CONTEXT_MANUAL_HASH_ANCHORED"
        ),
        "required_interface_fact": required_interface_fact,
        "nonclaim": (
            "This closes only the immediate uses of returns from the four directly proven slot "
            "+0x04 calls. It does not symbolically prove that dispatcher/lookup/factory callees "
            "cannot retain or transform the string, establish the original DLL's allocation or "
            "ownership policy, establish pointer constness or downstream mutability, or close a "
            "copied/split-address interface route. A writable process-lifetime UTF-16 buffer is "
            "hardened compatible policy, not a measured original return."
        ),
    }


def parse_required_fact(value: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for entry in value.split("; "):
        key, separator, item = entry.partition("=")
        if not separator or not key or key in parsed:
            raise ValueError(f"malformed required_interface_fact entry: {entry!r}")
        parsed[key] = item
    return parsed


def validate_structured_row_integrity(
    rows: list[dict[str, str]], image_census: ImageCensus
) -> None:
    indexed = {row["gate_id"]: row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError("duplicate gate_id before structured-row validation")
    for gate_id, expected_fields in (
        ("GM-IMG-015", gm_img_015_fields(image_census.application_member)),
        ("GM-IMG-016", gm_img_016_fields(image_census.after_slot8)),
        ("GM-IMG-017", gm_img_017_fields(image_census.slot4_return)),
    ):
        row = indexed.get(gate_id)
        if row is None:
            raise ValueError(f"missing structured row: {gate_id}")
        if row["source"] != "IMAGE":
            raise ValueError(f"structured row source mismatch: {gate_id}")
        for field, expected in expected_fields.items():
            if row[field] != expected:
                raise ValueError(f"structured row {gate_id} field mismatch: {field}")

    app = image_census.application_member
    classes = dict(app.class_counts)
    slots = dict(app.slot_call_counts)
    row_015 = indexed["GM-IMG-015"]
    required_015 = parse_required_fact(row_015["required_interface_fact"])
    expected_required_015 = {
        "mechanical_displacement_occurrences": str(app.direct_displacement_occurrences),
        "mechanical_true_member_refs": str(app.true_member_references),
        "mechanical_unrelated_occurrences": str(app.unrelated_displacement_occurrences),
        "mechanical_reads": str(app.read_references),
        "mechanical_writes": str(app.write_references),
        "mechanical_inline_virtual_calls": str(sum(slots.values())),
        "mechanical_slot_+0x00_calls": str(slots[0x00]),
        "mechanical_slot_+0x04_calls": str(slots[0x04]),
        "manual_guard_reads": str(classes["guard_read"]),
        "manual_scalar_delete_reads": str(classes["scalar_delete_read"]),
        "manual_alias_stores_or_returns": str(
            app.manually_classified_alias_stores_or_returns
        ),
    }
    if required_015 != expected_required_015:
        raise ValueError("GM-IMG-015 required-interface census does not match verifier")
    fragments_015 = (
        f"true member refs={app.true_member_references}",
        f"reads={app.read_references}",
        f"writes={app.write_references}",
        f"slot +0x00={slots[0x00]}",
        f"slot +0x04={slots[0x04]}",
        f"guards={classes['guard_read']}",
        f"scalar-delete cleanup={classes['scalar_delete_read']}",
        (
            "copied interface alias stores/returns="
            f"{app.manually_classified_alias_stores_or_returns}"
        ),
    )
    if any(fragment not in row_015["exact_static_fact"] for fragment in fragments_015):
        raise ValueError("GM-IMG-015 prose census does not match verifier")

    adjacency = image_census.after_slot8
    row_016 = indexed["GM-IMG-016"]
    required_016 = parse_required_fact(row_016["required_interface_fact"])
    offsets = ",".join(f"+0x{offset:02X}" for offset in adjacency.pinned_cell_offsets)
    expected_required_016 = {
        "fallback_region_bytes": str(adjacency.fallback_region_bytes),
        "pinned_cells": str(adjacency.pinned_cell_count),
        "pinned_cell_offsets": offsets,
        "adjacent_string_va": f"0x{adjacency.adjacent_string_va:08X}",
        "adjacent_string": f"UTF16_{adjacency.adjacent_string_value}",
        "adjacent_string_bytes_with_terminator": str(
            adjacency.adjacent_string_bytes_with_terminator
        ),
        "executable_raw_refs": str(adjacency.executable_raw_reference_count),
        "text_raw_refs": str(adjacency.text_raw_reference_count),
        "exact_push_imm32_patterns": str(adjacency.exact_push_imm32_pattern_count),
        "other_executable_section_refs": str(
            adjacency.other_executable_section_reference_count
        ),
    }
    if required_016 != expected_required_016:
        raise ValueError("GM-IMG-016 required-interface census does not match verifier")
    fragments_016 = (
        f"Fallback cell-region bytes={adjacency.fallback_region_bytes}",
        f"pinned cells={adjacency.pinned_cell_count}",
        f"raw address refs={adjacency.executable_raw_reference_count}",
        f".text refs={adjacency.text_raw_reference_count}",
        f"exact PUSH-imm32 byte-pattern refs={adjacency.exact_push_imm32_pattern_count}",
        (
            "other executable-section refs="
            f"{adjacency.other_executable_section_reference_count}"
        ),
    )
    if any(fragment not in row_016["exact_static_fact"] for fragment in fragments_016):
        raise ValueError("GM-IMG-016 prose census does not match verifier")

    slot4_return = image_census.slot4_return
    row_017 = indexed["GM-IMG-017"]
    required_017 = parse_required_fact(row_017["required_interface_fact"])
    expected_required_017 = {
        "mechanical_slot_+0x04_return_slices": str(slot4_return.direct_call_count),
        "manual_dispatcher_arguments": str(slot4_return.dispatcher_argument_uses),
        "manual_empty_predicate_arguments": str(
            slot4_return.empty_predicate_argument_uses
        ),
        "manual_inline_UTF16_compares": str(slot4_return.inline_utf16_compare_uses),
        "manual_immediate_alias_stores": str(slot4_return.immediate_alias_stores),
        "manual_immediate_alias_returns": str(slot4_return.immediate_alias_returns),
        "manual_immediate_deallocator_calls": str(
            slot4_return.immediate_deallocator_calls
        ),
    }
    if required_017 != expected_required_017:
        raise ValueError("GM-IMG-017 required-interface census does not match verifier")
    fragments_017 = (
        f"slot +0x04 calls={slot4_return.direct_call_count}",
        f"dispatcher arguments={slot4_return.dispatcher_argument_uses}",
        f"empty-predicate arguments={slot4_return.empty_predicate_argument_uses}",
        f"inline UTF-16 compares={slot4_return.inline_utf16_compare_uses}",
        f"immediate alias stores={slot4_return.immediate_alias_stores}",
        f"immediate alias returns={slot4_return.immediate_alias_returns}",
        f"immediate deallocator calls={slot4_return.immediate_deallocator_calls}",
    )
    if any(fragment not in row_017["exact_static_fact"] for fragment in fragments_017):
        raise ValueError("GM-IMG-017 prose census does not match verifier")


def verify_structured_row_mutation_guards(
    rows: list[dict[str, str]], image_census: ImageCensus
) -> None:
    app = image_census.application_member
    slots = dict(app.slot_call_counts)
    adjacency = image_census.after_slot8
    slot4_return = image_census.slot4_return
    mutation_specs = (
        (
            "GM-IMG-015",
            "exact_static_fact",
            f"true member refs={app.true_member_references}",
            f"true member refs={app.true_member_references - 1}",
        ),
        (
            "GM-IMG-015",
            "exact_static_fact",
            f"reads={app.read_references}",
            f"reads={app.read_references - 1}",
        ),
        (
            "GM-IMG-015",
            "exact_static_fact",
            f"writes={app.write_references}",
            f"writes={app.write_references - 1}",
        ),
        (
            "GM-IMG-015",
            "exact_static_fact",
            f"slot +0x00={slots[0x00]}",
            f"slot +0x00={slots[0x00] - 1}",
        ),
        (
            "GM-IMG-015",
            "exact_static_fact",
            f"slot +0x04={slots[0x04]}",
            f"slot +0x04={slots[0x04] - 1}",
        ),
        (
            "GM-IMG-015",
            "required_interface_fact",
            f"mechanical_slot_+0x04_calls={slots[0x04]}",
            f"mechanical_slot_+0x04_calls={slots[0x04] - 1}",
        ),
        (
            "GM-IMG-016",
            "exact_static_fact",
            f"raw address refs={adjacency.executable_raw_reference_count}",
            f"raw address refs={adjacency.executable_raw_reference_count - 1}",
        ),
        (
            "GM-IMG-016",
            "required_interface_fact",
            f"executable_raw_refs={adjacency.executable_raw_reference_count}",
            f"executable_raw_refs={adjacency.executable_raw_reference_count - 1}",
        ),
        (
            "GM-IMG-017",
            "exact_static_fact",
            f"slot +0x04 calls={slot4_return.direct_call_count}",
            f"slot +0x04 calls={slot4_return.direct_call_count - 1}",
        ),
        (
            "GM-IMG-017",
            "exact_static_fact",
            f"dispatcher arguments={slot4_return.dispatcher_argument_uses}",
            f"dispatcher arguments={slot4_return.dispatcher_argument_uses - 1}",
        ),
        (
            "GM-IMG-017",
            "required_interface_fact",
            f"manual_immediate_alias_stores={slot4_return.immediate_alias_stores}",
            f"manual_immediate_alias_stores={slot4_return.immediate_alias_stores + 1}",
        ),
        (
            "GM-IMG-017",
            "required_interface_fact",
            (
                "manual_immediate_deallocator_calls="
                f"{slot4_return.immediate_deallocator_calls}"
            ),
            (
                "manual_immediate_deallocator_calls="
                f"{slot4_return.immediate_deallocator_calls + 1}"
            ),
        ),
    )
    if len(mutation_specs) != EXPECTED_STRUCTURED_ROW_MUTATION_GUARD_CASES:
        raise ValueError("structured-row mutation-guard case census mismatch")
    for gate_id, field, old, new in mutation_specs:
        mutated = [dict(row) for row in rows]
        target = next(row for row in mutated if row["gate_id"] == gate_id)
        if old not in target[field]:
            raise ValueError(f"mutation-guard source token missing: {gate_id}/{field}")
        target[field] = target[field].replace(old, new, 1)
        try:
            validate_structured_row_integrity(mutated, image_census)
        except ValueError:
            continue
        raise ValueError(f"structured-row mutation escaped guard: {gate_id}/{field}")


def validate_gate_id_set(rows: list[dict[str, str]]) -> None:
    actual = tuple(row["gate_id"] for row in rows)
    if actual != EXPECTED_GATE_IDS:
        raise ValueError(
            "GM exact ordered gate-ID set mismatch: "
            f"expected={','.join(EXPECTED_GATE_IDS)} actual={','.join(actual)}"
        )


def verify_gate_id_mutation_guards(rows: list[dict[str, str]]) -> None:
    mutations: list[list[dict[str, str]]] = []

    renamed = [dict(row) for row in rows]
    renamed[-3]["gate_id"] = "GM-IMG-018"
    mutations.append(renamed)

    missing = [dict(row) for row in rows[:-1]]
    mutations.append(missing)

    reordered = [dict(row) for row in rows]
    reordered[0], reordered[1] = reordered[1], reordered[0]
    mutations.append(reordered)

    if len(mutations) != EXPECTED_GATE_ID_MUTATION_GUARD_CASES:
        raise ValueError("gate-ID mutation-guard case census mismatch")
    for index, mutated in enumerate(mutations, start=1):
        try:
            validate_gate_id_set(mutated)
        except ValueError:
            continue
        raise ValueError(f"gate-ID mutation escaped guard: case={index}")


def make_rows(
    pe: PE32,
    data_evidence: dict[str, object],
    image_census: ImageCensus,
) -> list[dict[str, str]]:
    gm_015_fields = gm_img_015_fields(image_census.application_member)
    gm_016_fields = gm_img_016_fields(image_census.after_slot8)
    gm_017_fields = gm_img_017_fields(image_census.slot4_return)
    specs = [
        {
            "gate_id": "GM-IMG-001",
            "phase": "PLUGIN_LOAD",
            "subject": "GameMaster.dll/CreateGameMaster",
            "exact_static_fact": (
                "Application init calls LoadLibraryW with exact UTF-16 GameMaster.dll; "
                "on success it resolves exact ASCII CreateGameMaster, calls the export "
                "with zero explicit arguments, and stores EAX at application+0x7C8."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": (
                "export=CreateGameMaster; return=non-null interface pointer; owner=application+0x7C8"
            ),
            "span": "loader",
            "support": ["init_call", "dll_string", "export_string"],
            "nonclaim": "Does not recover the original DLL implementation or prove it is present on disk.",
            "blocker": "ORIGINAL_PLUGIN_IMPLEMENTATION_NOT_IN_PINNED_EVIDENCE",
            "next": "Compatible implementation requires the used ABI surface below plus runtime validation.",
        },
        {
            "gate_id": "GM-IMG-002",
            "phase": "FALLBACK",
            "subject": "application+0x7C8 fallback object",
            "exact_static_fact": (
                "If the library, export, or returned object is absent, the loader allocates 4 bytes "
                "through imported MSVCR90 operator new, assigns vtable 0x00F09AF0, and stores it at "
                "application+0x7C8 when that allocation succeeds; allocation failure stores NULL."
            ),
            "semantic_status": "PROVEN_EXACT_CONDITIONAL",
            "required_interface_fact": (
                "fallback_vtable=0x00F09AF0; allocation_size=4; non_null_only_on_allocation_success"
            ),
            "span": "loader",
            "support": ["fallback_vtable"],
            "nonclaim": (
                "A non-null application+0x7C8 does not prove the real plug-in loaded; IMAGE alone "
                "does not prove fallback allocation succeeded in a particular run."
            ),
            "blocker": "SUCCESSFULLY_ALLOCATED_FALLBACK_CAN_PASS_VISIBILITY_CHECK",
            "next": "Distinguish fallback from a real interface by the key getter result.",
        },
        {
            "gate_id": "GM-IMG-003",
            "phase": "FALLBACK",
            "subject": "fallback vtable slot +0x04",
            "exact_static_fact": (
                "Fallback vtable slot +0x04 points to 0x009F17E0, whose complete body returns NULL."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": "vtable_slot=+0x04; return_type=pointer; fallback_return=NULL",
            "span": "fallback_getter",
            "support": ["fallback_vtable"],
            "nonclaim": "The source-level method name and original DLL implementation are unknown.",
            "blocker": "NULL_WINDOW_KEY",
            "next": "Use the complete slot census and DATA model binding below for a compatible implementation.",
        },
        {
            "gate_id": "GM-IMG-004",
            "phase": "BUTTON_VISIBILITY",
            "subject": "GM button show path",
            "exact_static_fact": (
                "The show path checks only application+0x7C8 for non-null, then queries the local "
                "CMyActor module state; a successfully allocated non-null fallback can therefore "
                "coexist with a visible button."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": "visibility_requires_non_null_application_plus_0x7C8",
            "span": "show_gate",
            "support": ["state_query", "state_adapter"],
            "nonclaim": "Visibility does not prove that clicking can create a window.",
            "blocker": "VISIBILITY_AND_CLICKABILITY_USE_DIFFERENT_CONDITIONS",
            "next": "Use the click path and dispatcher result as the functional gate.",
        },
        {
            "gate_id": "GM-IMG-005",
            "phase": "MODULE_STATE",
            "subject": "GMModule_Client query type 0x25",
            "exact_static_fact": (
                "CMyActor queries module registry type 0x25; the GMModule_Client adapter accepts "
                "that type and copies GMModule_Client+0x19 into the query result used by both show and click gates."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": "click_state_byte=GMModule_Client+0x19; query_type=0x25",
            "span": "state_query",
            "support": ["state_adapter"],
            "nonclaim": "This byte alone cannot supply the missing window key.",
            "blocker": "STATE_BYTE_IS_NECESSARY_BUT_NOT_SUFFICIENT",
            "next": "Keep module state and plug-in interface evidence separate.",
        },
        {
            "gate_id": "GM-IMG-006",
            "phase": "BUTTON_CLICK",
            "subject": "application+0x7C8 vtable slot +0x04",
            "exact_static_fact": (
                "After local-player and GMModule_Client+0x19 gates pass, click calls interface vtable "
                "slot +0x04 and passes its return as the first logical argument to the UI dispatcher. "
                "The three prior pushes are dispatcher arguments retained across the zero-argument getter call."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": "slot_+0x04=thiscall_zero_explicit_args; return=wide_string_pointer",
            "span": "click_gate",
            "support": ["slot4_dispatch_route", "dispatcher", "factory"],
            "nonclaim": "Static code does not establish the returned pointer's allocation or ownership policy.",
            "blocker": "FALLBACK_SLOT_RETURNS_NULL",
            "next": (
                "As hardened compatible policy, return a writable process-lifetime NUL-terminated "
                "UTF-16 GUI model basename; direct IMAGE callers only prove immediate reads."
            ),
        },
        {
            "gate_id": "GM-IMG-007",
            "phase": "UI_DISPATCH",
            "subject": "UI key empty predicate",
            "exact_static_fact": (
                "The dispatcher first calls 0x008946C0; that predicate returns true for NULL or an "
                "empty UTF-16 string, and the dispatcher then returns NULL before lookup or factory creation."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": "key_must_be_non_null_and_non_empty_UTF16",
            "span": "dispatcher",
            "support": ["empty_predicate"],
            "nonclaim": "A non-empty key is necessary but does not by itself prove a matching factory.",
            "blocker": "EMPTY_KEY_SHORT_CIRCUITS_BEFORE_FACTORY",
            "next": "Match the key against the registered GMModule_Client factory condition.",
        },
        {
            "gate_id": "GM-IMG-008",
            "phase": "GM_FACTORY",
            "subject": "GMModule_Client factory slot +0x48",
            "exact_static_fact": (
                "Factory 0x007280D0 re-reads interface slot +0x04, rejects NULL/empty, compares the "
                "returned UTF-16 text exactly with the requested key, and only on equality allocates "
                "0xEC bytes, calls constructor 0x0059D740, and assigns vtable 0x00F46258."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": "getter_model_basename_must_equal_requested_factory_key_exactly",
            "span": "factory",
            "support": ["empty_predicate"],
            "nonclaim": "This row does not prove which request key reaches this factory at runtime.",
            "blocker": "REQUEST_TO_FACTORY_RUNTIME_BINDING_NOT_OBSERVED",
            "next": "Join only at report level with the source-separated DATA model declaration below.",
        },
        {
            "gate_id": "GM-IMG-009",
            "phase": "PANEL_CHILD_LOOKUP",
            "subject": "GMUI_BASIC",
            "exact_static_fact": (
                "After the built-in GM panel is constructed, panel vtable slot +0x60 at 0x00726DF0 "
                "uses the sole IMAGE xref to UTF-16 GMUI_BASIC as a child/tab lookup. This literal "
                "occurrence is not evidence of what the missing plug-in getter returned."
            ),
            "semantic_status": "PROVEN_EXACT_PANEL_CHILD_LITERAL",
            "required_interface_fact": (
                "panel_child_id=GMUI_BASIC; getter_return_remains_unknown_in_IMAGE"
            ),
            "span": "gmui_request",
            "support": ["key_string", "factory"],
            "nonclaim": (
                "This lookup does not prove that the original DLL returned any particular model basename."
            ),
            "blocker": "NONE_FOR_CHILD_ID",
            "next": (
                "Compose only outside this IMAGE row with DATA to propose a compatible basename; "
                "do not claim the original DLL return."
            ),
        },
        {
            "gate_id": "GM-IMG-010",
            "phase": "OWNERSHIP_CLEANUP",
            "subject": "application+0x7C8 and library handle +0x7CC",
            "exact_static_fact": (
                "Application cleanup passes application+0x7C8 directly to imported MSVCR90 operator "
                "delete without a virtual-destructor call, clears the pointer, and then passes +0x7CC "
                "to FreeLibrary when non-null."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": "returned_object_memory_must_be_safe_for_application_MSVCR90_delete",
            "span": "cleanup",
            "support": ["loader"],
            "nonclaim": "The original DLL's allocation strategy and source-level destructor contract are unknown.",
            "blocker": "CROSS_MODULE_ALLOCATION_COMPATIBILITY_REQUIRED",
            "next": "Any compatibility implementation must validate clean shutdown as well as window creation.",
        },
        {
            "gate_id": "GM-IMG-011",
            "phase": "INTERFACE_CENSUS",
            "subject": "application+0x7C8 direct executable-section use census",
            "exact_static_fact": (
                "The direct .text 0x7C8 displacement census contains 16 occurrences: 15 true "
                "application-member references (10 reads, 5 writes) and one unrelated ESP+0x7C8 "
                "stack local; every other executable section has zero raw 0x7C8 displacement hits. "
                "The pinned direct routes contain five virtual calls: slot +0x00 once and slot "
                "+0x04 four times."
            ),
            "semantic_status": "PROVEN_EXACT_BOUNDED_CENSUS",
            "required_interface_fact": "required_slots=+0x00,+0x04; call_counts=1,4",
            "span": "slot0_call_route",
            "support": ["loader", "cleanup", "slot4_dispatch_route", "click_gate", "factory"],
            "nonclaim": (
                "This direct-displacement census alone does not prove absence of calls through a "
                "copied alias or split-address construction; GM-IMG-015 separately classifies every "
                "direct producer/consumer but still does not close split-address construction."
            ),
            "blocker": "NO_SPLIT_ADDRESS_DATAFLOW_CENSUS",
            "next": (
                "A bounded compatible implementation must provide the two directly proven slots; "
                "runtime validation remains required for any unseen split-address or external alias use."
            ),
        },
        {
            "gate_id": "GM-IMG-012",
            "phase": "INTERFACE_ABI",
            "subject": "interface vtable slot +0x00",
            "exact_static_fact": (
                "Slot +0x00 is called with ECX=this and two stack output-pointer arguments; the "
                "fallback callee returns with ret 8, returns the first pointer in EAX, writes -1 "
                "to its first dword, initializes its +4 subobject, and does not use the second pointer."
            ),
            "semantic_status": "PROVEN_EXACT_ABI_UNKNOWN_SEMANTIC",
            "required_interface_fact": "slot_+0x00=thiscall_two_pointer_args_ret8; fallback_behavior_reusable",
            "span": "fallback_slot0",
            "support": ["fallback_vtable_slots", "slot0_call_route"],
            "nonclaim": "The semantic names and full layouts of both output objects remain UNKNOWN.",
            "blocker": "OUTPUT_SEMANTICS_UNKNOWN_BUT_FALLBACK_BEHAVIOR_EXACT",
            "next": "A compatible DLL can preserve the exact fallback behavior for this reachable slot.",
        },
        {
            "gate_id": "GM-IMG-013",
            "phase": "GUI_MODEL_RESOLUTION",
            "subject": "slot +0x04 key to GUI model path",
            "exact_static_fact": (
                "The resolver is initialized with exact ASCII base path .\\Data\\GUI\\Model\\ "
                "and formats UTF-16 %s\\%s.model from that base plus the slot +0x04 key. This "
                "consumer therefore treats the getter value as a GUI model basename; IMAGE does "
                "not forbid the same text from also naming a control elsewhere."
            ),
            "semantic_status": "PROVEN_EXACT",
            "required_interface_fact": "slot_+0x04_returns_GUI_model_basename",
            "span": "gui_model_resolver",
            "support": ["resolver_setup", "slot4_dispatch_route"],
            "nonclaim": "IMAGE alone does not identify which on-disk model basename belongs to the missing DLL.",
            "blocker": "MODEL_BASENAME_REQUIRES_SOURCE_SEPARATE_DATA",
            "next": "Use GM-DATA-001 and GM-DATA-002 without merging their source into this row.",
        },
        {
            "gate_id": "GM-IMG-014",
            "phase": "INTERFACE_ABI",
            "subject": "fallback vtable slot +0x08",
            "exact_static_fact": (
                "The third fallback vtable cell at +0x08 points to 0x00403C00. Its complete body "
                "takes one stack-passed destination pointer (which may be a source-level hidden sret "
                "buffer) for an MSVCP90 std::basic_string<wchar_t>, default-constructs that destination "
                "through the pinned MSVCP90 import, returns the same pointer in EAX, and returns with "
                "ret 4. The 0x00403C00 pointer occurs only in this vtable cell, no executable section "
                "contains a direct E8/E9 rel32 branch to it, and none of the five pinned direct "
                "application+0x7C8 virtual-call routes uses slot +0x08."
            ),
            "semantic_status": "PROVEN_EXACT_ABI_NO_PINNED_ROUTE",
            "required_interface_fact": (
                "slot_+0x08=one_stack_wstring_destination_pointer_ret4; possible_hidden_sret; "
                "fallback_default_constructs_empty_wstring; direct_E8_E9_rel32_branch_count=0"
            ),
            "span": "fallback_slot8",
            "support": ["fallback_vtable"],
            "nonclaim": (
                "The source-level method name and whether the pointer is explicit or hidden sret are "
                "unknown. GM-IMG-015 closes client-produced aliases only for the pinned direct-member "
                "routes; it does not prove absence of split-address construction or an alias retained "
                "inside an external callee."
            ),
            "blocker": "NO_PINNED_CALL_ROUTE_FOR_SLOT8",
            "next": (
                "Treat the exact fallback behavior as ABI hardening for a compatible three-cell "
                "prefix; do not claim slot +0x08 is required to open the GM window without "
                "split-address, external-alias, or runtime evidence."
            ),
        },
        {
            "gate_id": "GM-IMG-015",
            "phase": "INTERFACE_DIRECT_DATAFLOW",
            "subject": "application+0x7C8 direct producer/consumer closure",
            **gm_015_fields,
            "span": "loader_export_store",
            "support": [
                "loader_fallback_store",
                "direct_cleanup",
                "constructor_pointer_zero",
                "slot0_call_route",
                "slot4_dispatch_route",
                "show_gate",
                "click_gate",
                "factory",
            ],
            "blocker": "SPLIT_ADDRESS_OR_EXTERNAL_ALIAS_REMAINS_UNPROVEN",
            "next": (
                "No additional client slot is required by the direct routes; retain slot +0x08 only "
                "as exact fallback-compatible hardening and validate the window plus clean shutdown."
            ),
        },
        {
            "gate_id": "GM-IMG-016",
            "phase": "FALLBACK_LAYOUT_BOUNDARY",
            "subject": "bytes immediately after fallback slot +0x08",
            **gm_016_fields,
            "span": "fallback_after_slot8_string",
            "support": ["fallback_vtable"],
            "blocker": "ORIGINAL_DLL_INTERFACE_LENGTH_UNKNOWN",
            "next": (
                "Implement the exact three-cell fallback-compatible prefix; treat any longer original "
                "interface as unproven and require runtime validation rather than inventing extra slots."
            ),
        },
        {
            "gate_id": "GM-IMG-017",
            "phase": "SLOT4_RETURN_DIRECT_LIFETIME",
            "subject": "direct slot +0x04 return consumers",
            **gm_017_fields,
            "span": "factory",
            "support": [
                "slot4_dispatch_route",
                "click_gate",
                "dispatcher",
                "empty_predicate",
            ],
            "blocker": "DOWNSTREAM_RETENTION_AND_ORIGINAL_OWNERSHIP_UNPROVEN",
            "next": (
                "As hardened compatible policy, a getter may return a writable process-lifetime "
                "NUL-terminated UTF-16 buffer; runtime must still validate the chosen DATA basename, "
                "window creation, downstream mutability/retention, and cleanup."
            ),
        },
    ]

    rows: list[dict[str, str]] = []
    for spec in specs:
        start, end, digest = SPAN_SPECS[spec["span"]]
        support = ";".join(span_label(name, pe) for name in spec["support"])
        key_material = "|".join(
            (
                spec["gate_id"],
                spec["phase"],
                spec["subject"],
                spec["exact_static_fact"],
                digest,
                support,
                "IMAGE",
            )
        )
        rows.append(
            {
                "gate_id": spec["gate_id"],
                "phase": spec["phase"],
                "subject": spec["subject"],
                "exact_static_fact": spec["exact_static_fact"],
                "semantic_status": spec["semantic_status"],
                "required_interface_fact": spec["required_interface_fact"],
                "evidence_span_start": f"0x{start:08X}",
                "evidence_span_end": f"0x{end:08X}",
                "evidence_span_start_file_offset": f"0x{pe.va_to_offset(start):08X}",
                "evidence_span_end_file_offset": f"0x{pe.va_to_offset(end):08X}",
                "evidence_span_sha256": digest,
                "support_spans": support,
                "evidence_key": hashlib.sha256(key_material.encode("utf-8")).hexdigest(),
                "source": "IMAGE",
                "source_path": "GameClient/GameClient.local.bin",
                "source_size": str(EXPECTED_IMAGE_SIZE),
                "source_sha256": EXPECTED_IMAGE_SHA256,
                "nonclaim": spec["nonclaim"],
                "blocker": spec["blocker"],
                "required_next_evidence": spec["next"],
                "image_sha256": EXPECTED_IMAGE_SHA256,
            }
        )

    data_specs = [
        {
            "gate_id": "GM-DATA-001",
            "phase": "GUI_MODEL_DECLARATION",
            "subject": "GMUI.project",
            "exact_static_fact": (
                "The GMUI project declares exactly one model with Name=GMUI_1."
            ),
            "semantic_status": "PROVEN_EXACT_DATA",
            "required_interface_fact": "DATA_ONLY_declared_model_basename=GMUI_1",
            "start": "XML:/Project/Models/Model",
            "end": "XML:@Name=GMUI_1",
            "digest": EXPECTED_GM_PROJECT_SHA256,
            "support": "project_name=GMUI;declared_models=1",
            "path": "GameClient/Data/GUI/Model/GMUI.project",
            "size": EXPECTED_GM_PROJECT_SIZE,
            "nonclaim": "DATA does not reveal the missing original DLL or observe its runtime return value.",
            "blocker": "NONE_FOR_MODEL_DECLARATION",
            "next": (
                "Join only outside this DATA row with the IMAGE resolver to form a labelled "
                "compatible proposal; DATA alone does not prove an interface return."
            ),
        },
        {
            "gate_id": "GM-DATA-002",
            "phase": "GUI_MODEL_STRUCTURE",
            "subject": "GMUI_1.model",
            "exact_static_fact": (
                "The model has exactly one top-level BigUIStandardWindow ID=GMUI_1 and exactly one "
                "UITabPage ID=GMUI_BASIC. Across 534 GUI .model files, this is the sole file containing "
                "the exact GMUI_BASIC token; the corpus has no subdirectory and no case variant of "
                "GMUI_BASIC.model."
            ),
            "semantic_status": "PROVEN_EXACT_DATA_CENSUS",
            "required_interface_fact": "model_root=GMUI_1;panel_child=GMUI_BASIC",
            "start": "XML:/UIControlData/SourceData/BigUIStandardWindow",
            "end": "XML://UITabPage[@ID='GMUI_BASIC']",
            "digest": EXPECTED_GM_MODEL_SHA256,
            "support": (
                f"gui_model_files={data_evidence['model_count']};"
                f"gui_model_subdirectories={data_evidence['subdirectory_count']};"
                f"GMUI_BASIC_model_hits=1;"
                f"GMUI_BASIC_dot_model_files={data_evidence['gmui_basic_model_count']}"
            ),
            "path": "GameClient/Data/GUI/Model/GMUI_1.model",
            "size": EXPECTED_GM_MODEL_SIZE,
            "nonclaim": "DATA structure alone does not prove the original DLL allocation or ABI.",
            "blocker": "NONE_FOR_MODEL_TO_CHILD_BINDING",
            "next": (
                "A separately labelled IMAGE+DATA composition may propose GMUI_1; runtime evidence "
                "must then test it without treating DATA as the original DLL contract."
            ),
        },
    ]
    for spec in data_specs:
        key_material = "|".join(
            (
                spec["gate_id"],
                spec["phase"],
                spec["subject"],
                spec["exact_static_fact"],
                spec["digest"],
                spec["support"],
                "DATA",
            )
        )
        rows.append(
            {
                "gate_id": spec["gate_id"],
                "phase": spec["phase"],
                "subject": spec["subject"],
                "exact_static_fact": spec["exact_static_fact"],
                "semantic_status": spec["semantic_status"],
                "required_interface_fact": spec["required_interface_fact"],
                "evidence_span_start": spec["start"],
                "evidence_span_end": spec["end"],
                "evidence_span_start_file_offset": "",
                "evidence_span_end_file_offset": "",
                "evidence_span_sha256": spec["digest"],
                "support_spans": spec["support"],
                "evidence_key": hashlib.sha256(key_material.encode("utf-8")).hexdigest(),
                "source": "DATA",
                "source_path": spec["path"],
                "source_size": str(spec["size"]),
                "source_sha256": spec["digest"],
                "nonclaim": spec["nonclaim"],
                "blocker": spec["blocker"],
                "required_next_evidence": spec["next"],
                "image_sha256": "",
            }
        )
    validate_gate_id_set(rows)
    verify_gate_id_mutation_guards(rows)
    if len({row["evidence_key"] for row in rows}) != len(rows):
        raise ValueError("duplicate evidence_key")
    if {row["source"] for row in rows} != {"IMAGE", "DATA"}:
        raise ValueError("GM table source census mismatch")
    if sum(row["source"] == "IMAGE" for row in rows) != EXPECTED_IMAGE_ROW_COUNT:
        raise ValueError("GM IMAGE row census mismatch")
    if sum(row["source"] == "DATA" for row in rows) != EXPECTED_DATA_ROW_COUNT:
        raise ValueError("GM DATA row census mismatch")
    validate_structured_row_integrity(rows, image_census)
    verify_structured_row_mutation_guards(rows, image_census)
    return rows


FIELDNAMES = [
    "gate_id",
    "phase",
    "subject",
    "exact_static_fact",
    "semantic_status",
    "required_interface_fact",
    "evidence_span_start",
    "evidence_span_end",
    "evidence_span_start_file_offset",
    "evidence_span_end_file_offset",
    "evidence_span_sha256",
    "support_spans",
    "evidence_key",
    "source",
    "source_path",
    "source_size",
    "source_sha256",
    "nonclaim",
    "blocker",
    "required_next_evidence",
    "image_sha256",
]


def render_tsv(rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=FIELDNAMES,
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def render_md(rows: list[dict[str, str]], tsv_digest: str) -> bytes:
    evidence = {row["gate_id"]: row["evidence_key"] for row in rows}
    indexed = {row["gate_id"]: row for row in rows}
    gm_015 = parse_required_fact(indexed["GM-IMG-015"]["required_interface_fact"])
    gm_016 = parse_required_fact(indexed["GM-IMG-016"]["required_interface_fact"])
    gm_017 = parse_required_fact(indexed["GM-IMG-017"]["required_interface_fact"])
    image_rows = sum(row["source"] == "IMAGE" for row in rows)
    data_rows = sum(row["source"] == "DATA" for row in rows)
    text = f"""# PF GM plug-in gate — bounded IMAGE + DATA checkpoint

## คำตอบสั้น

- **[ORIGINAL EVIDENCE: IMAGE]** เมื่อ fallback allocation 4 ไบต์สำเร็จ `application+0x7C8` เป็น object ที่ไม่ใช่ NULL และผ่าน pointer gate ของปุ่มได้; ถ้า allocation ล้มเหลว loader เก็บ NULL (`GM-IMG-002`).
- **[ORIGINAL EVIDENCE: IMAGE]** เมื่อคลิก client เรียก vtable slot `+0x04`; fallback slot นี้คืน `NULL` แล้ว dispatcher หยุดก่อนสร้างหน้าต่าง (`GM-IMG-003`, `GM-IMG-006`, `GM-IMG-007`).
- **[ORIGINAL EVIDENCE: IMAGE]** direct executable-section census ปิด {gm_015['mechanical_true_member_refs']} member refs (read {gm_015['mechanical_reads']} / write {gm_015['mechanical_writes']}) และ pinned direct routes มี call slot `+0x00` {gm_015['mechanical_slot_+0x00_calls']} จุดกับ `+0x04` {gm_015['mechanical_slot_+0x04_calls']} จุด. **[MANUAL_HASH_ANCHORED]** การจำแนกบริบทของ slices ที่ pin ไว้พบ copied-alias store/return {gm_015['manual_alias_stores_or_returns']} จุด; นี่ไม่ใช่ symbolic dataflow proof และขอบเขต split-address/pointer arithmetic กับ alias ภายใน external callee ยังเปิด (`GM-IMG-011`, `GM-IMG-015`).
- **[ORIGINAL EVIDENCE: IMAGE]** direct slot `+0x04` return slicesครบ {gm_017['mechanical_slot_+0x04_return_slices']} จุด: ส่งเป็น dispatcher argument {gm_017['manual_dispatcher_arguments']} จุด, empty-predicate argument {gm_017['manual_empty_predicate_arguments']} จุด และ inline UTF-16 compare {gm_017['manual_inline_UTF16_compares']} จุด; immediate alias store/return/deallocator เป็น {gm_017['manual_immediate_alias_stores']}/{gm_017['manual_immediate_alias_returns']}/{gm_017['manual_immediate_deallocator_calls']}. การจำแนก consumer เป็น **[MANUAL_HASH_ANCHORED]** และไม่ปิด retention ภายใน downstream calleeหรือ original ownership (`GM-IMG-017`).
- **[ORIGINAL EVIDENCE: IMAGE]** fallback vtable มี cell ที่ `+0x08`: รับ stack-passed destination pointer ของ MSVCP90 `std::basic_string<wchar_t>` (อาจเป็น hidden sret), default-construct เป็นสตริงว่าง, คืน pointer เดิม และ `ret 4`; pointer เป้าหมายมีเพียง cell นี้, ไม่มี direct `E8/E9` rel32 branch และ direct `application+0x7C8` routes ที่ pin ไว้ไม่เรียกช่องนี้. หลัง {gm_016['fallback_region_bytes']}-byte cell region ที่ `+0x0C` เป็น UTF-16 `%s%s` ซึ่งมี exact raw PUSH-imm32 patterns {gm_016['exact_push_imm32_patterns']} จุด จึงปิด concrete byte adjacency แต่ไม่อ้าง instruction execution, source-level vtable length หรือว่า DLL เดิมไม่มี private method อื่น (`GM-IMG-014`, `GM-IMG-016`).
- **[ORIGINAL EVIDENCE: IMAGE]** resolver ใช้ค่าคืน slot `+0x04` เป็น **GUI model basename** เพื่อประกอบ `.\\Data\\GUI\\Model\\<key>.model`; literal `GMUI_BASIC` ที่ EXE อ้างตรงเพียงจุดเดียวถูกใช้เป็น child/tab lookupหลัง panel ถูกสร้างแล้ว แต่ข้อเท็จจริงนี้ไม่บอกค่าคืนของ DLL เดิม (`GM-IMG-009`, `GM-IMG-013`).
- **[ORIGINAL EVIDENCE: DATA]** `GMUI.project` ประกาศ model `GMUI_1`; `GMUI_1.model` มี root `GMUI_1` และ child `GMUI_BASIC` (`GM-DATA-001`, `GM-DATA-002`).
- **[RECONSTRUCTED POLICY — PROPOSED, NOT EXECUTED]** candidate สำหรับ compatibility กับ DATA ที่มีอยู่คือ slot `+0x04` คืน pointer ไปยัง writable process-lifetime UTF-16 buffer ที่บรรจุ `GMUI_1`; corpus ไม่มี `GMUI_BASIC.model`. นี่ไม่ห้ามว่า DLL เดิมอาจเคยคืนข้อความอื่นหรือแม้แต่ `GMUI_BASIC` ผ่านกลไกที่ไม่มีอยู่ในหลักฐานปัจจุบัน และยังไม่อ้างว่าเคยเห็นค่าคืน, constness, mutability หรือ lifetime ของ DLL เดิม.

**[UNPINNED OPERATIONAL INVENTORY — NOT IMAGE/DATA EVIDENCE]** ใบสั่งงานระบุว่า inventory ปัจจุบันไม่พบ `GameMaster.dll`; generator นี้ไม่ได้ enumerate หรือ hash inventory ดังกล่าว จึงอาจ stale และต้องตรวจซ้ำใน runtime lane. หาก inventory นั้นยังจริง อาการ “เห็นปุ่มแต่คลิกไม่เปิด” จึงเพียงสอดคล้องกับเส้น fallback ที่ allocation สำเร็จ; artifact นี้ไม่ยก inventory หรือ screen observation เป็น IMAGE/DATA fact.

## คำแก้จาก checkpoint ก่อน

- **ถอน:** `GMUI_BASIC` ใน artifact รุ่นก่อนเคยถูกเสนอจาก literal xref เป็น candidate น้ำหนักสูงของค่าคืน slot `+0x04`; xref นั้นพิสูจน์เพียง child/tab lookup จึงไม่ใช่หลักฐานของค่าคืน DLL.
- **แก้:** `GMUI_BASIC` คือ ID ของ tab/control ภายใน panel. DATA ปัจจุบันผูก panel นี้กับ model `GMUI_1` และไม่มี `GMUI_BASIC.model`; `GMUI_1` จึงเป็น compatible proposal ไม่ใช่ measured original return.
- **เพิ่ม:** direct executable-section member-reference census, direct producer/consumer closure, direct slot `+0x04` return-lifetime slices, ABI ของ slot `+0x00` และ fallback slot `+0x08`, byte boundary หลัง slot `+0x08`, GUI-model resolver และ recursive DATA model census 534 ไฟล์/0 subdirectory.

## สัญญา ABI ที่ IMAGE บังคับเท่าที่พิสูจน์แล้ว

| ขอบเขต | ข้อเท็จจริง |
|---|---|
| loader | `LoadLibraryW(L\"GameMaster.dll\")` → `GetProcAddress(\"CreateGameMaster\")` → เรียก export แบบไม่มี argument ชัดแจ้ง → เก็บ pointer ที่ `application+0x7C8` |
| directly proven slots | pinned direct routes มี slot `+0x00` {gm_015['mechanical_slot_+0x00_calls']} จุดและ slot `+0x04` {gm_015['mechanical_slot_+0x04_calls']} จุด; manual contextual reading ของ direct {gm_015['mechanical_true_member_refs']}-reference set พบ copied-alias store/return {gm_015['manual_alias_stores_or_returns']} จุด แต่ split-address/external-alias ยังไม่ปิด |
| slot `+0x00` | `ECX=this`, stack output pointers 2 ตัว, callee `ret 8`, EAX คืน pointer แรก; fallback เขียน dword แรกเป็น `-1` และ init subobject `+4`; semantic ของ outputs ยัง UNKNOWN |
| slot `+0x04` | `ECX=this`, ไม่มี explicit argument, plain `ret`, EAX เป็น pointer ไปยังข้อความ UTF-16 แบบ NUL-terminatedที่ direct callers อ่านทันที; IMAGE ไม่พิสูจน์ constness, mutability หรือ lifetime. Direct caller slicesไม่ store/return/free ค่านี้และ factoryเรียก getterซ้ำสำหรับ empty-checkกับ exact compare แต่ downstream retention/original ownershipยังเปิด |
| fallback slot `+0x08` | stack destination pointer 1 ตัว (explicit หรือ hidden sret ยังแยกไม่ได้), `ret 4`; default-construct MSVCP90 `std::basic_string<wchar_t>` แล้วคืน pointer เดิม; direct pinned routes ไม่เรียกช่องนี้; หลัง {gm_016['fallback_region_bytes']}-byte region เริ่ม referenced UTF-16 `%s%s` และ raw PUSH pattern census={gm_016['exact_push_imm32_patterns']}, แต่ execution/split-address/external-alias reachability ยังเปิด |
| เงื่อนไขผ่าน dispatcher | pointer ต้องไม่เป็น NULL และข้อความต้องไม่ว่าง |
| เงื่อนไขผ่าน GM factory | GUI model basename จาก slot `+0x04` ต้องเท่ากับ requested key แบบ UTF-16 exact comparison |
| compatible DATA binding — PROPOSED | คืน pointer ไปยัง writable process-lifetime UTF-16 buffer ที่บรรจุ `GMUI_1` → resolver โหลด `Data\\GUI\\Model\\GMUI_1.model` → panel ภายในมี `GMUI_BASIC`; ไม่ใช่ค่าดั้งเดิมหรือ lifetime ที่วัดแล้ว |
| object ที่ factory สร้าง | ขนาด `0xEC`, constructor `0x0059D740`, vtable `0x00F46258` |
| cleanup | application ใช้ imported `MSVCR90 operator delete(void*)` กับ pointer โดยตรง แล้ว `FreeLibrary`; ไม่มี virtual-destructor call ในช่วงที่พิสูจน์ |

## สัญญาส่งต่อสำหรับทีม — ยังไม่ใช่ผล runtime

- **[ORIGINAL EVIDENCE: IMAGE]** client ใช้ `GetProcAddress` ด้วย ASCII `CreateGameMaster` แบบ exact. **[RECONSTRUCTED POLICY — PROPOSED]** DLL ต้องเป็น 32-bit และควรบังคับ export table ด้วยไฟล์ `.def` ให้มีชื่อ `CreateGameMaster` ตรงตัว ไม่ใช่ `_CreateGameMaster` หรือ `CreateGameMaster@0`.
- **[RECONSTRUCTED POLICY — PROPOSED]** object ที่ factory คืนต้องจัดสรรด้วย allocator ที่เข้ากันได้กับ imported `MSVCR90.dll` scalar delete ของ client. ทางที่แคบและปลอดภัยที่สุดคือ build x86 ด้วย Visual Studio 2008 `/MD` หรือเรียก imported MSVCR90 `operator new` (`??2@YAPAXI@Z`) โดยตรง; ห้ามสมมติว่า `new` จาก modern UCRT/default heap ใช้ข้ามมาลบด้วย MSVCR90 ได้. จึงห้ามคืน static/global objectด้วย.
- **[RECONSTRUCTED POLICY — PROPOSED]** สอง slot ที่ direct routes บังคับคือ `+0x00` และ `+0x04`: slot `+0x00` ใช้ fallback behavior ที่พิสูจน์แล้วได้; slot `+0x04` ควรคืน pointer ไปยัง writable process-lifetime UTF-16 buffer ที่บรรจุ `GMUI_1`. นี่เป็น hardened policy เพราะ IMAGE ปิดเพียง immediate reads และยังไม่ปิด downstream mutability/retention; ไม่ใช่หลักฐานว่า DLL เดิมคืน literal หรือใช้ lifetime แบบใด. เพื่อ harden ต่อ split-address/external-alias route ที่ยังไม่ปิด ควรมี three-cell fallback-compatible prefix รวม `+0x08` และทำ exact fallback behavior ด้วย แต่ห้ามอ้างว่าช่องนี้จำเป็นต่อการเปิดหน้าต่างหรือว่า DLL เดิมไม่มี private method เพิ่ม.
- **[RECONSTRUCTED POLICY — PROPOSED]** object ไม่ควรพึ่ง destructor เพื่อ cleanup เพราะ application ไม่เรียก virtual destructor/release ก่อน delete.
- **[CLIENT-OBSERVED RESULT REQUIRED]** acceptance ยังต้องเห็นปุ่ม → คลิก → หน้าต่าง `GMUI_1` เปิดและเข้าถึง tab `GMUI_BASIC` ได้ รวมทั้งปิดเกม/cleanup โดยไม่ crash ใน runtime ที่ทีมได้รับอนุญาต.
- **[RECONSTRUCTED POLICY — PROPOSED]** ห้าม patch `0x009F17E0` โดยตรง เพราะตารางนี้พิสูจน์เพียงว่าเป็น fallback getter ของ vtable นี้ ไม่ได้พิสูจน์ว่า function body เป็น private ต่อ GM.

## ขอบเขตที่ยังเปิด

- ไม่รู้ implementation/source ของ DLL เดิม และไม่เห็นค่าคืน runtime เดิม.
- output objects ของ slot `+0x00` ยังไม่มี semantic name; compatible fallback behavior ปิด ABI ได้แต่ไม่ขยายความหมาย.
- semantic name และ split-address/external-alias reachability ของ fallback slot `+0x08` ยัง UNKNOWN แม้ ABI/body และ concrete three-cell-region/string adjacency จะปิดแล้ว.
- direct member-reference census มี {gm_015['mechanical_true_member_refs']} direct refs; no-alias เป็น manual hash-anchored contextual reading ไม่ใช่ symbolic proof และยังไม่ปิด pointer-arithmetic/split-address. runtime clean-shutdown test เป็น guard สำหรับ ABI surface ที่อาจยังไม่เห็น.
- direct slot `+0x04` return-use census ปิดเฉพาะ immediate caller slices; ไม่ใช่ symbolic proof ว่า dispatcher/lookup/factory calleeไม่ retain/transform pointer.
- ยังไม่พิสูจน์ runtime window creation หรือ clean shutdown; artifact นี้เป็น implementation contract สำหรับทีม ไม่ใช่คำกล่าวว่าสำเร็จบนจอแล้ว.

## Provenance และ nonclaims

- ทุกแถวใน `PF_GM_PLUGIN_GATE.tsv` มี source เดียว: IMAGE {image_rows} แถว / DATA {data_rows} แถว; ไม่มีแถวใดผสมสองชั้น.
- ไม่ได้รัน GameClient, server, DLL, dump หรือ capture.
- ไม่ได้คัดลอก raw image bytes ลง output; รายงานเฉพาะ VA, file offset, โครงสร้าง, constant และ SHA-256.
- **[DELIVERY BLOCKER — OUTSIDE THIS GENERATOR'S AUTHORITY]** ไฟล์ local-only ชุดนี้รวม pair marker อาจยังไม่ repository-visible; การ allowlist/track/package เป็นคำตัดสินของ chief/owner และ generator นี้ไม่ตรวจหรือแก้ Git. นี่เป็น delivery blocker ไม่ใช่ IMAGE/DATA fact.
- ตารางมี {len(rows)} แถว, gate_id ไม่ซ้ำ {len(rows)}/{len(rows)}, evidence_key ไม่ซ้ำ {len(rows)}/{len(rows)}.
- Exact ordered gate-ID set ถูก pin เป็น `GM-IMG-001..017` ตามด้วย `GM-DATA-001..002`; pair marker `PF_GM_PLUGIN_GATE.pair.json` ผูก SHA-256 ของ TSV/MD กับ row/source counts และถูก publish เป็นไฟล์สุดท้าย.
- Generator PASS scope: `{PASS_SCOPE}`. ตัวตรวจผูก structured census กับค่าทั้งใน TSV/MD และรัน mutation guards; semantic class ของ guard/delete/write-role/no-alias/slot4-return-consumer ยังคงเป็น manual hash-anchored interpretation ไม่ใช่ symbolic dataflow.
- TSV SHA-256: `{tsv_digest}`
- IMAGE SHA-256: `{EXPECTED_IMAGE_SHA256}`
- `GMUI.project` SHA-256: `{EXPECTED_GM_PROJECT_SHA256}`
- `GMUI_1.model` SHA-256: `{EXPECTED_GM_MODEL_SHA256}`

## Evidence keys

"""
    for gate_id in sorted(evidence):
        text += f"- `{gate_id}`: `{evidence[gate_id]}`\n"
    return text.encode("utf-8")


def pair_payload(
    rows: list[dict[str, str]], tsv: bytes, md: bytes
) -> dict[str, object]:
    return {
        "schema": "PF_GM_PLUGIN_GATE_PAIR_V1",
        "gate_ids": list(EXPECTED_GATE_IDS),
        "rows": {
            "total": len(rows),
            "IMAGE": sum(row["source"] == "IMAGE" for row in rows),
            "DATA": sum(row["source"] == "DATA" for row in rows),
        },
        "tsv": {
            "path": TSV_PATH.name,
            "size": len(tsv),
            "sha256": sha256(tsv),
        },
        "md": {
            "path": MD_PATH.name,
            "size": len(md),
            "sha256": sha256(md),
        },
    }


def render_pair_marker(rows: list[dict[str, str]], tsv: bytes, md: bytes) -> bytes:
    return (
        json.dumps(
            pair_payload(rows, tsv, md),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def validate_rendered_artifacts(
    rows: list[dict[str, str]], tsv: bytes, md: bytes, pair: bytes
) -> None:
    validate_gate_id_set(rows)
    reader = csv.DictReader(
        io.StringIO(tsv.decode("utf-8"), newline=""), delimiter="\t"
    )
    parsed_rows = list(reader)
    if reader.fieldnames != FIELDNAMES:
        raise ValueError("rendered TSV field set/order mismatch")
    if parsed_rows != rows:
        raise ValueError("rendered TSV rows differ from validated row objects")

    md_text = md.decode("utf-8")
    required_md_fragments = (
        f"- TSV SHA-256: `{sha256(tsv)}`",
        f"ตารางมี {len(rows)} แถว",
        "Exact ordered gate-ID set ถูก pin เป็น `GM-IMG-001..017` ตามด้วย `GM-DATA-001..002`",
        "[UNPINNED OPERATIONAL INVENTORY — NOT IMAGE/DATA EVIDENCE]",
        "[DELIVERY BLOCKER — OUTSIDE THIS GENERATOR'S AUTHORITY]",
        "writable process-lifetime UTF-16 buffer",
    )
    if any(fragment not in md_text for fragment in required_md_fragments):
        raise ValueError("rendered Markdown required integrity wording missing")
    forbidden_md_fragments = (
        "const wchar_t*",
        "static-lifetime",
        "stable static",
        "คืน `L\"GMUI_1\"`",
    )
    if any(fragment in md_text for fragment in forbidden_md_fragments):
        raise ValueError("rendered Markdown contains superseded lifetime wording")
    for row in rows:
        evidence_line = f"- `{row['gate_id']}`: `{row['evidence_key']}`"
        if evidence_line not in md_text:
            raise ValueError(f"rendered Markdown missing evidence row: {row['gate_id']}")

    try:
        parsed_pair = json.loads(pair.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("pair marker is not canonical UTF-8 JSON") from exc
    if parsed_pair != pair_payload(rows, tsv, md):
        raise ValueError("pair marker does not match TSV/MD hashes or row/source counts")
    if pair != render_pair_marker(rows, tsv, md):
        raise ValueError("pair marker is not in canonical deterministic form")


def acquire_lock() -> int:
    try:
        fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError(
            f"output lock already exists; inspect before removing: {LOCK_PATH.name}"
        ) from exc
    try:
        os.write(fd, f"pid={os.getpid()}\n".encode("ascii"))
    except Exception:
        os.close(fd)
        LOCK_PATH.unlink(missing_ok=True)
        raise
    return fd


def release_lock(fd: int) -> None:
    os.close(fd)
    LOCK_PATH.unlink()


def stage_file(path: Path, content: bytes) -> Path:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.staged")
    fd: int | None = None
    try:
        fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as stream:
            fd = None
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if temporary.read_bytes() != content:
            raise ValueError(f"staged-file verification failed: {path.name}")
        return temporary
    except Exception:
        if fd is not None:
            os.close(fd)
        temporary.unlink(missing_ok=True)
        raise


def publish_staged(staged: dict[Path, Path]) -> None:
    for destination in (TSV_PATH, MD_PATH, PAIR_PATH):
        os.replace(staged[destination], destination)


def cleanup_staged(staged: dict[Path, Path]) -> None:
    for temporary in staged.values():
        temporary.unlink(missing_ok=True)


def read_checked_file(path: Path, content: bytes) -> bytes:
    if not path.is_file():
        raise ValueError(f"missing output: {path}")
    actual = path.read_bytes()
    if actual != content:
        raise ValueError(
            f"output mismatch: {path.name}; expected_sha256={sha256(content)} "
            f"actual_sha256={sha256(actual)}"
        )
    return actual


def check_installed_artifacts(
    rows: list[dict[str, str]], tsv: bytes, md: bytes, pair: bytes
) -> None:
    actual_tsv = read_checked_file(TSV_PATH, tsv)
    actual_md = read_checked_file(MD_PATH, md)
    actual_pair = read_checked_file(PAIR_PATH, pair)
    validate_rendered_artifacts(rows, actual_tsv, actual_md, actual_pair)


def recheck_immutable_inputs(
    image_before: bytes, data_before: dict[str, object]
) -> tuple[bytes, dict[str, object]]:
    image_after, _pe, _imports, _census = verify_image()
    if image_before != image_after or sha256(image_after) != EXPECTED_IMAGE_SHA256:
        raise ValueError("image changed during re-derivation")
    data_after = verify_data()
    if data_before["project"] != data_after["project"]:
        raise ValueError("GMUI.project changed during re-derivation")
    if data_before["model"] != data_after["model"]:
        raise ValueError("GMUI_1.model changed during re-derivation")
    return image_after, data_after


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify existing outputs instead of writing them",
    )
    args = parser.parse_args()

    lock_fd: int | None = None
    staged: dict[Path, Path] = {}
    if not args.check:
        lock_fd = acquire_lock()
    try:
        before, pe, _imports, image_census = verify_image()
        data_before = verify_data()
        rows = make_rows(pe, data_before, image_census)
        tsv = render_tsv(rows)
        md = render_md(rows, sha256(tsv))
        pair = render_pair_marker(rows, tsv, md)
        validate_rendered_artifacts(rows, tsv, md, pair)
        if args.check:
            check_installed_artifacts(rows, tsv, md, pair)
            after, data_after = recheck_immutable_inputs(before, data_before)
            mode = "check"
        else:
            staged[TSV_PATH] = stage_file(TSV_PATH, tsv)
            staged[MD_PATH] = stage_file(MD_PATH, md)
            staged[PAIR_PATH] = stage_file(PAIR_PATH, pair)
            validate_rendered_artifacts(
                rows,
                staged[TSV_PATH].read_bytes(),
                staged[MD_PATH].read_bytes(),
                staged[PAIR_PATH].read_bytes(),
            )
            recheck_immutable_inputs(before, data_before)
            publish_staged(staged)
            check_installed_artifacts(rows, tsv, md, pair)
            after, data_after = recheck_immutable_inputs(before, data_before)
            mode = "write"

        result_lines = [
            f"mode={mode}",
            f"image_size={len(after)}",
            f"image_sha256={sha256(after)}",
            f"gm_project_sha256={sha256(data_after['project'])}",
            f"gm_model_sha256={sha256(data_after['model'])}",
            f"gui_model_count={data_after['model_count']}",
            f"gui_model_subdirectory_count={data_after['subdirectory_count']}",
            f"gmui_basic_model_count={data_after['gmui_basic_model_count']}",
            f"pass_scope={PASS_SCOPE}",
            (
                "structured_row_mutation_guard_cases="
                f"{EXPECTED_STRUCTURED_ROW_MUTATION_GUARD_CASES}"
            ),
            (
                "gate_id_mutation_guard_cases="
                f"{EXPECTED_GATE_ID_MUTATION_GUARD_CASES}"
            ),
            f"rows={len(rows)}",
            f"image_rows={sum(row['source'] == 'IMAGE' for row in rows)}",
            f"data_rows={sum(row['source'] == 'DATA' for row in rows)}",
            f"tsv_size={len(tsv)}",
            f"tsv_sha256={sha256(tsv)}",
            f"md_size={len(md)}",
            f"md_sha256={sha256(md)}",
            f"pair_size={len(pair)}",
            f"pair_sha256={sha256(pair)}",
        ]
    finally:
        cleanup_staged(staged)
        if lock_fd is not None:
            release_lock(lock_fd)
    for line in result_lines:
        print(line)
    print("status=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # fail closed with ASCII console output
        safe_error = str(exc).encode("ascii", "backslashreplace").decode("ascii")
        print(f"status=FAIL error={type(exc).__name__}: {safe_error}", file=sys.stderr)
        raise SystemExit(1)
