#!/usr/bin/env python3
"""Re-derive the Pirate Force protocol registry and serializer field census.

This tool intentionally uses only the Python standard library.  It reads the
guarded client image, writes artifacts beside this script, and prints ASCII so
that its console output is encodable by Windows code page 874.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
import struct
import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple


EXPECTED_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
EXPECTED_SIZE = 14_759_424
EXPECTED_IMAGE_BASE = 0x00400000
ONCE_INIT_VA = 0x0089C080
ID_ASSIGN_VA = 0x0089BD00
WRITE_VA = 0x0089A600
READ_VA = 0x0089A640
VTABLE_MARKER_VA = 0x00401B20
EVIDENCE_SOURCES = frozenset({"IMAGE", "DUMP", "CAPTURE", "DATA"})
STATIC_EVIDENCE_SOURCE = "IMAGE"

EXPECTED_SECTIONS = {
    ".text": (0x00401000, 0x00838A2C, 0x00000400, 0x00838C00),
    ".code": (0x00C3A000, 0x000002E1, 0x00839000, 0x00000400),
    ".rdata": (0x00C3B000, 0x003DE38E, 0x00839400, 0x003DE400),
    ".data": (0x0101A000, 0x00081F70, 0x00C17800, 0x00011E00),
}

STACK_NEUTRAL_IMPORTS = {
    (
        "MSVCP90.dll",
        "??0?$basic_string@_WU?$char_traits@_W@std@@"
        "V?$allocator@_W@2@@std@@QAE@XZ",
    ),
    (
        "MSVCP90.dll",
        "??1?$basic_string@_WU?$char_traits@_W@std@@"
        "V?$allocator@_W@2@@std@@QAE@XZ",
    ),
    ("MSVCR90.dll", "_invalid_parameter_noinfo"),
}
EXPECTED_STACK_NEUTRAL_IAT = {
    0x00C3B478: next(
        item for item in STACK_NEUTRAL_IMPORTS if item[1].startswith("??0")
    ),
    0x00C3B488: next(
        item for item in STACK_NEUTRAL_IMPORTS if item[1].startswith("??1")
    ),
    0x00C3B4C0: ("MSVCR90.dll", "_invalid_parameter_noinfo"),
}


class ExtractionError(RuntimeError):
    pass


class StringWireHelper(NamedTuple):
    direction: str
    tag: str
    string_kind: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    required_iats: tuple[int, ...]


STRING_WIRE_HELPERS = {
    0x0089A6D0: StringWireHelper(
        "W",
        "UNTAGGED_STRING8_LEN32LE",
        "basic_string<char>",
        0x00499AD0,
        0x0089A733,
        "a0674fb3366720314e20ef5f5dbfa010330b12a73ed4e56e6c43e9d310dce9f1",
        (0x00C3B470, 0x00C3B494, 0x00C3B504),
    ),
    0x0089A740: StringWireHelper(
        "R",
        "UNTAGGED_STRING8_LEN32LE",
        "basic_string<char>",
        0x00499B40,
        0x0089A806,
        "90c8c73b3b3c7158af57e374c694730763ab28292130b4f128a4754dec54e76a",
        (0x00C3B43C, 0x00C3B504),
    ),
    0x0089A810: StringWireHelper(
        "W",
        "UNTAGGED_WSTRING16LE_LEN32LE",
        "basic_string<wchar_t>",
        0x00499C10,
        0x0089A875,
        "08d6f27f030f3e0f1a32873d296c7f2c35a9d67f547607cf95c2900a60ffdad4",
        (0x00C3B464, 0x00C3B484, 0x00C3B504),
    ),
    0x0089A880: StringWireHelper(
        "R",
        "UNTAGGED_WSTRING16LE_LEN32LE",
        "basic_string<wchar_t>",
        0x00499C80,
        0x0089A95E,
        "2f564cb5d4f68d035d9e60fa1a4a5334b0875262420851f463f3f904e22ad978",
        (0x00C3B47C, 0x00C3B504),
    ),
}

# This duplicate is deliberate: it is an independent fail-closed oracle for
# semantic labels.  STRING_WIRE_HELPERS drives extraction, while this mapping
# prevents a direction/tag/type mutation in that table from validating itself.
EXPECTED_STRING_WIRE_SEMANTICS = {
    0x0089A6D0: (
        "W", "UNTAGGED_STRING8_LEN32LE", "basic_string<char>"
    ),
    0x0089A740: (
        "R", "UNTAGGED_STRING8_LEN32LE", "basic_string<char>"
    ),
    0x0089A810: (
        "W", "UNTAGGED_WSTRING16LE_LEN32LE", "basic_string<wchar_t>"
    ),
    0x0089A880: (
        "R", "UNTAGGED_WSTRING16LE_LEN32LE", "basic_string<wchar_t>"
    ),
}

STRING_WIRE_IMPORTS = {
    0x00C3B43C: (
        "MSVCP90.dll",
        "??4?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@"
        "std@@QAEAAV01@PBD@Z",
    ),
    0x00C3B464: (
        "MSVCP90.dll",
        "?length@?$basic_string@_WU?$char_traits@_W@std@@"
        "V?$allocator@_W@2@@std@@QBEIXZ",
    ),
    0x00C3B470: (
        "MSVCP90.dll",
        "?length@?$basic_string@DU?$char_traits@D@std@@"
        "V?$allocator@D@2@@std@@QBEIXZ",
    ),
    0x00C3B47C: (
        "MSVCP90.dll",
        "??4?$basic_string@_WU?$char_traits@_W@std@@"
        "V?$allocator@_W@2@@std@@QAEAAV01@PB_W@Z",
    ),
    0x00C3B484: (
        "MSVCP90.dll",
        "?c_str@?$basic_string@_WU?$char_traits@_W@std@@"
        "V?$allocator@_W@2@@std@@QBEPB_WXZ",
    ),
    0x00C3B494: (
        "MSVCP90.dll",
        "?c_str@?$basic_string@DU?$char_traits@D@std@@"
        "V?$allocator@D@2@@std@@QBEPBDXZ",
    ),
    0x00C3B504: ("MSVCR90.dll", "memcpy"),
}

STRING_WIRE_KEY_BYTES = (
    (0x00B37B80, 0x00736F80, "FF2504B5C300"),
    (0x0089A6DB, 0x00499ADB, "FF1570B4C300"),
    (0x0089A704, 0x00499B04, "893C1183461404"),
    (0x0089A712, 0x00499B12, "FF1594B4C300"),
    (0x0089A720, 0x00499B20, "E85BD42900"),
    (0x0089A728, 0x00499B28, "017E14"),
    (0x0089A777, 0x00499B77, "8B3C0883C004894618"),
    (0x0089A7AC, 0x00499BAC, "E8CFD32900"),
    (0x0089A7B9, 0x00499BB9, "C6043B00"),
    (0x0089A7BD, 0x00499BBD, "FF153CB4C300"),
    (0x0089A7CC, 0x00499BCC, "017E18"),
    (0x0089A81B, 0x00499C1B, "FF1564B4C300"),
    (0x0089A828, 0x00499C28, "03FF"),
    (0x0089A846, 0x00499C46, "893C1183461404"),
    (0x0089A854, 0x00499C54, "FF1584B4C300"),
    (0x0089A862, 0x00499C62, "E819D32900"),
    (0x0089A86A, 0x00499C6A, "017E14"),
    (0x0089A8B7, 0x00499CB7, "8B3C0883C004894618"),
    (0x0089A8DB, 0x00499CDB, "D1ED"),
    (0x0089A901, 0x00499D01, "E87AD22900"),
    (0x0089A90B, 0x00499D0B, "66890C6B"),
    (0x0089A914, 0x00499D14, "FF157CB4C300"),
    (0x0089A923, 0x00499D23, "017E18"),
)

STRING_WIRE_IAT_CALLS = {
    0x0089A6DB: 0x00C3B470,
    0x0089A712: 0x00C3B494,
    0x0089A7BD: 0x00C3B43C,
    0x0089A81B: 0x00C3B464,
    0x0089A854: 0x00C3B484,
    0x0089A914: 0x00C3B47C,
}

STRING_WIRE_MEMCPY_CALLS = frozenset(
    (0x0089A720, 0x0089A7AC, 0x0089A862, 0x0089A901)
)


class AtomicObjectHelper(NamedTuple):
    tag: str
    reason: str
    length: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    iat_va: int


ATOMIC_OBJECT_HELPERS = {
    0x004A06A0: AtomicObjectHelper(
        "ATOMIC_INTERLOCKED_INCREMENT_ECX",
        "atomic_target_pointer_alias_unproved",
        "N/A",
        0x0009FAA0,
        0x004A06A8,
        "6efc20b380f156abdfe0ec57f2a414abeac1b59880dce5d5bbeab67904883662",
        0x00C3B1B0,
    ),
    0x004A06B0: AtomicObjectHelper(
        "ATOMIC_INTERLOCKED_DECREMENT_ECX",
        "atomic_target_pointer_alias_unproved",
        "N/A",
        0x0009FAB0,
        0x004A06B8,
        "eb2fd2755d06fec1152aad19725862c6b2b1b36922ec909834627d3baa5ef3f9",
        0x00C3B1B4,
    ),
    0x0088D050: AtomicObjectHelper(
        "ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C",
        "atomic_target_object_alias_unproved",
        "N/A",
        0x0048C450,
        0x0088D05B,
        "6da78a1acc15d9fd5f7b2d620253debf8d8465136165dfb1eae35914b2442845",
        0x00C3B1B0,
    ),
    0x0088D060: AtomicObjectHelper(
        "DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04",
        "dynamic_vtable_plus_0x04_target_unresolved",
        "N/A",
        0x0048C460,
        0x0088D082,
        "d3b546ac50ded491a6c5a196138b9691f23d8499298e728925f1afb1f0e7734c",
        0x00C3B1B4,
    ),
}

# Independent mutation oracle; ATOMIC_OBJECT_HELPERS drives extraction.
EXPECTED_ATOMIC_OBJECT_SEMANTICS = {
    0x004A06A0: (
        "ATOMIC_INTERLOCKED_INCREMENT_ECX",
        "atomic_target_pointer_alias_unproved",
        "N/A",
        0x00C3B1B0,
    ),
    0x004A06B0: (
        "ATOMIC_INTERLOCKED_DECREMENT_ECX",
        "atomic_target_pointer_alias_unproved",
        "N/A",
        0x00C3B1B4,
    ),
    0x0088D050: (
        "ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C",
        "atomic_target_object_alias_unproved",
        "N/A",
        0x00C3B1B0,
    ),
    0x0088D060: (
        "DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE_PLUS_04",
        "dynamic_vtable_plus_0x04_target_unresolved",
        "N/A",
        0x00C3B1B4,
    ),
}

ATOMIC_OBJECT_IMPORTS = {
    0x00C3B1B0: ("KERNEL32.dll", "InterlockedIncrement"),
    0x00C3B1B4: ("KERNEL32.dll", "InterlockedDecrement"),
}

ATOMIC_OBJECT_HELPER_BYTES = {
    0x004A06A0: "51FF15B0B1C300C3",
    0x004A06B0: "51FF15B4B1C300C3",
    0x0088D050: "83C10C51FF15B0B1C300C3",
    0x0088D060: (
        "568BF18D460C50FF15B4B1C30085C0750F85F6740B8B168B42046A018BCEFFD05EC3"
    ),
}


class PureChainHelper(NamedTuple):
    tag: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str


PURE_CHAIN_HELPERS = {
    0x0088F2B0: PureChainHelper(
        "PURE_READONLY_CHAIN_PLUS_04_CONTAINS_PREDICATE",
        0x0048E6B0,
        0x0088F2D1,
        "00076eb0d61b7763ba58709f657437f455e6c6a2e3da83b3005bef0b847a61e9",
        "8B44240885C074138B4C24048D6424003BC1740A8B400485C075F532C0C3B001C3",
    ),
}

EXPECTED_PURE_CHAIN_SEMANTICS = {
    0x0088F2B0: (
        "PURE_READONLY_CHAIN_PLUS_04_CONTAINS_PREDICATE",
        0x0048E6B0,
        0x0088F2D1,
        "00076eb0d61b7763ba58709f657437f455e6c6a2e3da83b3005bef0b847a61e9",
    ),
}


class MutableChainHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    iat_va: int


MUTABLE_CHAIN_HELPERS = {
    0x00B0BF70: MutableChainHelper(
        "MUTATING_CHAIN_PLUS_04_HELPER",
        "mutable_chain_target_object_alias_unproved",
        0x0070B370,
        0x00B0BFDC,
        "4e1374fd126457c82d11bf3e6efa0fda845bb85e2c2a985ed67c4eff3f4eb7e6",
        (
            "568BF1833E00578B3DC0B4C3007502FFD78B4604807815007405FFD75F5EC3"
            "8B48088079150075188B0180781500750A8BC88B018078150074F65F894E04"
            "5EC38B400480781500751D8DA424000000008B4E043B4808750E8946048BD0"
            "8B42048078150074EA5F8946045EC3"
        ),
        0x00C3B4C0,
    ),
}

EXPECTED_MUTABLE_CHAIN_SEMANTICS = {
    0x00B0BF70: (
        "MUTATING_CHAIN_PLUS_04_HELPER",
        "mutable_chain_target_object_alias_unproved",
        0x0070B370,
        0x00B0BFDC,
        "4e1374fd126457c82d11bf3e6efa0fda845bb85e2c2a985ed67c4eff3f4eb7e6",
        0x00C3B4C0,
    ),
}


class LockedMutablePointerSlotHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    iat_vas: tuple[int, ...]


LOCKED_MUTABLE_POINTER_SLOT_HELPERS = {
    0x0066AB90: LockedMutablePointerSlotHelper(
        "LOCKED_MUTABLE_POINTER_SLOT_HELPER",
        "locked_mutable_pointer_slot_nested_target_and_alias_unproved",
        0x00269F90,
        0x0066AC2D,
        "a807fe8724451e352fe8cef467c7db8794ddefe54f2c4d9bb76e1608eacf5893",
        (
            "515355568BF18D4E18578BEA894C2410E80B2A22008BFD2B7E1C8BCE8BD7"
            "E8ED6A09008B46102B460CC1F8023BF87206FF15C0B4C3008B460C8B1CB8"
            "85DB752655E8AA5AE3FF55FF157CB8C3008B4C2418FF462083C4088BD8E852"
            "2EE3FF5F5E5D8BC35B59C38B4E10FF4E242BC8C1F9023BF97206FF15C0B4"
            "C3008B038B560C8B4C24108904BAC70300000000FF4620E81B2EE3FF5F5E5D"
            "8BC35B59C3"
        ),
        (0x00C3B4C0, 0x00C3B87C),
    ),
}

# This independent tuple does not drive extraction and catches semantic-table
# mutations separately from the exact body/import validation below.
EXPECTED_LOCKED_MUTABLE_POINTER_SLOT_SEMANTICS = {
    0x0066AB90: (
        "LOCKED_MUTABLE_POINTER_SLOT_HELPER",
        "locked_mutable_pointer_slot_nested_target_and_alias_unproved",
        0x00269F90,
        0x0066AC2D,
        "a807fe8724451e352fe8cef467c7db8794ddefe54f2c4d9bb76e1608eacf5893",
        (0x00C3B4C0, 0x00C3B87C),
    ),
}

LOCKED_MUTABLE_POINTER_SLOT_IMPORTS = {
    0x00C3B168: ("KERNEL32.dll", "LeaveCriticalSection"),
    0x00C3B16C: ("KERNEL32.dll", "EnterCriticalSection"),
    0x00C3B19C: ("KERNEL32.dll", "InterlockedExchangeAdd"),
    0x00C3B4C0: ("MSVCR90.dll", "_invalid_parameter_noinfo"),
    0x00C3B87C: ("MSVCR90.dll", "malloc"),
}

LOCKED_MUTABLE_POINTER_SLOT_SUPPORT = {
    0x0049DA40: (
        0x0009CE40,
        0x0049DA4A,
        "91f8bd361459e6514e2c53ca4bac3bd9d76baddaf75ee1b1562afecee8d96366",
        "8B0150FF1568B1C300C3",
    ),
    0x004A0680: (
        0x0009FA80,
        0x004A0691,
        "91487f19f8025dc0e0626a16e8aeac10cee14522dba680c031aaec84595567a4",
        "8B4424045068749F0701FF159CB1C300C3",
    ),
    0x0088D5B0: (
        0x0048C9B0,
        0x0088D5BA,
        "281bb0603facf9b7c61c87c0241b74e59ff6488057f979782e4d08ea4e4e9ee8",
        "8B0150FF156CB1C300C3",
    ),
}


class CriticalSectionPointerHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    iat_va: int


CRITICAL_SECTION_POINTER_HELPERS = {
    0x0049DA40: CriticalSectionPointerHelper(
        "LEAVE_CRITICAL_SECTION_DEREF_ECX",
        "critical_section_pointer_alias_unproved",
        0x0009CE40,
        0x0049DA4A,
        "91f8bd361459e6514e2c53ca4bac3bd9d76baddaf75ee1b1562afecee8d96366",
        "8B0150FF1568B1C300C3",
        0x00C3B168,
    ),
    0x0088D5B0: CriticalSectionPointerHelper(
        "ENTER_CRITICAL_SECTION_DEREF_ECX",
        "critical_section_pointer_alias_unproved",
        0x0048C9B0,
        0x0088D5BA,
        "281bb0603facf9b7c61c87c0241b74e59ff6488057f979782e4d08ea4e4e9ee8",
        "8B0150FF156CB1C300C3",
        0x00C3B16C,
    ),
}

# Independent mutation oracle; the table above drives row extraction.
EXPECTED_CRITICAL_SECTION_POINTER_SEMANTICS = {
    0x0049DA40: (
        "LEAVE_CRITICAL_SECTION_DEREF_ECX",
        "critical_section_pointer_alias_unproved",
        0x0009CE40,
        0x0049DA4A,
        "91f8bd361459e6514e2c53ca4bac3bd9d76baddaf75ee1b1562afecee8d96366",
        0x00C3B168,
    ),
    0x0088D5B0: (
        "ENTER_CRITICAL_SECTION_DEREF_ECX",
        "critical_section_pointer_alias_unproved",
        0x0048C9B0,
        0x0088D5BA,
        "281bb0603facf9b7c61c87c0241b74e59ff6488057f979782e4d08ea4e4e9ee8",
        0x00C3B16C,
    ),
}

CRITICAL_SECTION_POINTER_IMPORTS = {
    0x00C3B168: ("KERNEL32.dll", "LeaveCriticalSection"),
    0x00C3B16C: ("KERNEL32.dll", "EnterCriticalSection"),
}


class MutableDwordRangeGrowthHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    invalid_iat_va: int
    nested_target_va: int


MUTABLE_DWORD_RANGE_GROWTH_HELPERS = {
    0x007016A0: MutableDwordRangeGrowthHelper(
        "MUTATING_DWORD_RANGE_GROWTH_HELPER",
        "mutable_dword_range_nested_target_and_alias_unproved",
        0x00300AA0,
        0x00701725,
        "9cda4ae539f34f0e182808f7f5ce04d9bfb1b9a5113abcd461ac0d342e12f27f",
        (
            "83EC0C53568BF18B46102B460C8BDAC1F8023BC37769558B2DC0B4C30057C7"
            "442410000000008B4E0C85C9750433C0EB088B46142BC1C1F8028B7E108BD7"
            "2BD1C1FA023BD0730EC7070000000083C704897E10EB1B3BCF7602FFD58B068D"
            "4C24105157508D542420528BCEE8C051EFFF8B46102B460CC1F8023BC376A95F"
            "5D5E5B83C40CC3"
        ),
        0x00C3B4C0,
        0x005F68D0,
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_MUTABLE_DWORD_RANGE_GROWTH_SEMANTICS = {
    0x007016A0: (
        "MUTATING_DWORD_RANGE_GROWTH_HELPER",
        "mutable_dword_range_nested_target_and_alias_unproved",
        0x00300AA0,
        0x00701725,
        "9cda4ae539f34f0e182808f7f5ce04d9bfb1b9a5113abcd461ac0d342e12f27f",
        0x00C3B4C0,
        0x005F68D0,
    ),
}


class MutableDwordSlotOperationHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    invalid_iat_va: int
    nested_target_vas: tuple[int, int]


MUTABLE_DWORD_SLOT_OPERATION_HELPERS = {
    0x00AC6E80: MutableDwordSlotOperationHelper(
        "MUTATING_DWORD_SLOT_OPERATION_HELPER",
        "mutable_dword_slot_nested_targets_and_alias_unproved",
        0x006C6280,
        0x00AC6F00,
        "81aeacd2225d12cf4588aa7d74f8cbb8ace467c13a514286bc8fe1240b1e865b",
        (
            "83EC08568BF18B4E0C5785C9750433C0EB088B46142BC1C1F8028B7E108BD7"
            "2BD1C1FA023BD073318B4C2414C6442408008B442408508B442418518D560852"
            "506A0157E8D8C6BEFF83C41883C704897E105F5E83C408C204003BCF7606FF15"
            "C0B4C3008B4C24148B065157508D542414528BCEE808FEFFFF5F5E83C408C204"
            "00"
        ),
        0x00C3B4C0,
        (0x006B35A0, 0x00AC6D00),
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_MUTABLE_DWORD_SLOT_OPERATION_SEMANTICS = {
    0x00AC6E80: (
        "MUTATING_DWORD_SLOT_OPERATION_HELPER",
        "mutable_dword_slot_nested_targets_and_alias_unproved",
        0x006C6280,
        0x00AC6F00,
        "81aeacd2225d12cf4588aa7d74f8cbb8ace467c13a514286bc8fe1240b1e865b",
        0x00C3B4C0,
        (0x006B35A0, 0x00AC6D00),
    ),
}


class MutablePointerSlotTraversalHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    invalid_iat_va: int


MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS = {
    0x0046D2B0: MutablePointerSlotTraversalHelper(
        "MUTATING_POINTER_SLOT_TRAVERSAL_HELPER",
        "mutable_pointer_slot_traversal_alias_unproved",
        0x0006C6B0,
        0x0046D31C,
        "492e39afb9faf38f4f862abcdaa6278740417a4b1fc1e56d61a6b992421d5cf9",
        (
            "568BF1833E00578B3DC0B4C3007502FFD78B4604807821007405FFD75F5EC38B"
            "48088079210075188B0180782100750A8BC88B018078210074F65F894E045EC3"
            "8B400480782100751D8DA424000000008B4E043B4808750E8946048BD08B4204"
            "8078210074EA5F8946045EC3"
        ),
        0x00C3B4C0,
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_MUTABLE_POINTER_SLOT_TRAVERSAL_SEMANTICS = {
    0x0046D2B0: (
        "MUTATING_POINTER_SLOT_TRAVERSAL_HELPER",
        "mutable_pointer_slot_traversal_alias_unproved",
        0x0006C6B0,
        0x0046D31C,
        "492e39afb9faf38f4f862abcdaa6278740417a4b1fc1e56d61a6b992421d5cf9",
        0x00C3B4C0,
    ),
}


class LockedMutableDwordSlotUpdateHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    invalid_iat_va: int
    nested_target_vas: tuple[int, int, int]


LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS = {
    0x00710FA0: LockedMutableDwordSlotUpdateHelper(
        "LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPER",
        "locked_mutable_dword_slot_nested_target_and_alias_unproved",
        0x003103A0,
        0x0071100F,
        "622a7adac41e33c3df900bf6cd5f4842fd63f646299d3534689b08c26e6fe540",
        (
            "558BEA568BF185ED7460538D5E18578BCBE8FAC517008B7C24142B7E1C8BCE8"
            "BD7E8DA06FFFF8B46102B460CFF4E20C1F8023BF87206FF15C0B4C3008B4E0C"
            "8B14B98955008B46102B460CC1F8023BF87206FF15C0B4C3008B4E0C892CB9FF"
            "46248BCBE838CAD8FF5F5B5E5DC20400"
        ),
        0x00C3B4C0,
        (0x0088D5B0, 0x007016A0, 0x0049DA40),
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_LOCKED_MUTABLE_DWORD_SLOT_UPDATE_SEMANTICS = {
    0x00710FA0: (
        "LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPER",
        "locked_mutable_dword_slot_nested_target_and_alias_unproved",
        0x003103A0,
        0x0071100F,
        "622a7adac41e33c3df900bf6cd5f4842fd63f646299d3534689b08c26e6fe540",
        0x00C3B4C0,
        (0x0088D5B0, 0x007016A0, 0x0049DA40),
    ),
}


class NestedCallCompositionHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    nested_target_vas: tuple[int, int, int]


NESTED_CALL_COMPOSITION_HELPERS = {
    0x005F8DE0: NestedCallCompositionHelper(
        "NESTED_THREE_CALL_COMPOSITION_HELPER",
        "nested_call_composition_targets_and_alias_unproved",
        0x001F81E0,
        0x005F8E04,
        "e8a4be798270bd4fde0b0fa9dd2d676ed260fb28a6b243503df9475189bb5fb3",
        (
            "568BF1E898322A008B4C2408518BC8E82C242A000FB7C0508D4E50E800AAE6"
            "FF5EC20400"
        ),
        (0x0089C080, 0x0089B220, 0x00463800),
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_NESTED_CALL_COMPOSITION_SEMANTICS = {
    0x005F8DE0: (
        "NESTED_THREE_CALL_COMPOSITION_HELPER",
        "nested_call_composition_targets_and_alias_unproved",
        0x001F81E0,
        0x005F8E04,
        "e8a4be798270bd4fde0b0fa9dd2d676ed260fb28a6b243503df9475189bb5fb3",
        (0x0089C080, 0x0089B220, 0x00463800),
    ),
}


class EcxPlus50TailJumpHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    separator_hex: str
    tail_target_va: int


ECX_PLUS_50_TAIL_JUMP_HELPERS = {
    0x005F8C30: EcxPlus50TailJumpHelper(
        "ECX_PLUS_50_TAIL_JUMP_HELPER",
        "ecx_plus_50_tail_target_and_alias_unproved",
        0x001F8030,
        0x005F8C38,
        "4ac9cc919c1940986e14a9fb18344c6507b796d927507d033db5ee9865441066",
        "83C150E9C8ABE6FF",
        "CCCCCCCCCCCCCCCC",
        0x00463800,
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_ECX_PLUS_50_TAIL_JUMP_SEMANTICS = {
    0x005F8C30: (
        "ECX_PLUS_50_TAIL_JUMP_HELPER",
        "ecx_plus_50_tail_target_and_alias_unproved",
        0x001F8030,
        0x005F8C38,
        "4ac9cc919c1940986e14a9fb18344c6507b796d927507d033db5ee9865441066",
        "CCCCCCCCCCCCCCCC",
        0x00463800,
    ),
}


class ExactDirectImportCall(NamedTuple):
    tag: str
    reason: str
    dll: str
    symbol: str
    call_bytes_hex: str


EXACT_DIRECT_IMPORT_CALLS = {
    0x00C3B1B0: ExactDirectImportCall(
        "PE_IMPORT_INTERLOCKED_INCREMENT_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "KERNEL32.dll",
        "InterlockedIncrement",
        "FF15B0B1C300",
    ),
    0x00C3B1B4: ExactDirectImportCall(
        "PE_IMPORT_INTERLOCKED_DECREMENT_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "KERNEL32.dll",
        "InterlockedDecrement",
        "FF15B4B1C300",
    ),
    0x00C3B434: ExactDirectImportCall(
        "PE_IMPORT_WSTRING_POINTER_CONSTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@PB_W@Z",
        "FF1534B4C300",
    ),
    0x00C3B458: ExactDirectImportCall(
        "PE_IMPORT_STRING_DEFAULT_CONSTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@XZ",
        "FF1558B4C300",
    ),
    0x00C3B478: ExactDirectImportCall(
        "PE_IMPORT_WSTRING_DEFAULT_CONSTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ",
        "FF1578B4C300",
    ),
    0x00C3B480: ExactDirectImportCall(
        "PE_IMPORT_STRING_POINTER_CONSTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@PBD@Z",
        "FF1580B4C300",
    ),
    0x00C3B488: ExactDirectImportCall(
        "PE_IMPORT_WSTRING_DESTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??1?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ",
        "FF1588B4C300",
    ),
    0x00C3B48C: ExactDirectImportCall(
        "PE_IMPORT_STRING_COPY_ASSIGNMENT_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??4?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAEAAV01@ABV01@@Z",
        "FF158CB4C300",
    ),
    0x00C3B494: ExactDirectImportCall(
        "PE_IMPORT_STRING_C_STR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "?c_str@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QBEPBDXZ",
        "FF1594B4C300",
    ),
    0x00C3B498: ExactDirectImportCall(
        "PE_IMPORT_STRING_DESTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??1?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@XZ",
        "FF1598B4C300",
    ),
    0x00C3B4C0: ExactDirectImportCall(
        "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL",
        "invalid_parameter_import_call_wire_effect_unproved",
        "MSVCR90.dll",
        "_invalid_parameter_noinfo",
        "FF15C0B4C300",
    ),
    0x00C3B5C0: ExactDirectImportCall(
        "PE_IMPORT_SNWPRINTF_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCR90.dll",
        "_snwprintf",
        "FF15C0B5C300",
    ),
    0x00C3B8F8: ExactDirectImportCall(
        "PE_IMPORT_MESSAGE_BOX_W_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "USER32.dll",
        "MessageBoxW",
        "FF15F8B8C300",
    ),
}

OTHER_EXACT_DIRECT_IMPORT_CALL_IATS = frozenset(
    set(EXACT_DIRECT_IMPORT_CALLS) - {0x00C3B4C0}
)

# Independent mutation oracle; EXACT_DIRECT_IMPORT_CALLS drives extraction.
EXPECTED_EXACT_DIRECT_IMPORT_CALL_SEMANTICS = {
    0x00C3B1B0: (
        "PE_IMPORT_INTERLOCKED_INCREMENT_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "KERNEL32.dll",
        "InterlockedIncrement",
        "FF15B0B1C300",
    ),
    0x00C3B1B4: (
        "PE_IMPORT_INTERLOCKED_DECREMENT_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "KERNEL32.dll",
        "InterlockedDecrement",
        "FF15B4B1C300",
    ),
    0x00C3B434: (
        "PE_IMPORT_WSTRING_POINTER_CONSTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@PB_W@Z",
        "FF1534B4C300",
    ),
    0x00C3B458: (
        "PE_IMPORT_STRING_DEFAULT_CONSTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@XZ",
        "FF1558B4C300",
    ),
    0x00C3B478: (
        "PE_IMPORT_WSTRING_DEFAULT_CONSTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ",
        "FF1578B4C300",
    ),
    0x00C3B480: (
        "PE_IMPORT_STRING_POINTER_CONSTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@PBD@Z",
        "FF1580B4C300",
    ),
    0x00C3B488: (
        "PE_IMPORT_WSTRING_DESTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??1?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ",
        "FF1588B4C300",
    ),
    0x00C3B48C: (
        "PE_IMPORT_STRING_COPY_ASSIGNMENT_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??4?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAEAAV01@ABV01@@Z",
        "FF158CB4C300",
    ),
    0x00C3B494: (
        "PE_IMPORT_STRING_C_STR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "?c_str@?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QBEPBDXZ",
        "FF1594B4C300",
    ),
    0x00C3B498: (
        "PE_IMPORT_STRING_DESTRUCTOR_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCP90.dll",
        "??1?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@XZ",
        "FF1598B4C300",
    ),
    0x00C3B4C0: (
        "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL",
        "invalid_parameter_import_call_wire_effect_unproved",
        "MSVCR90.dll",
        "_invalid_parameter_noinfo",
        "FF15C0B4C300",
    ),
    0x00C3B5C0: (
        "PE_IMPORT_SNWPRINTF_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "MSVCR90.dll",
        "_snwprintf",
        "FF15C0B5C300",
    ),
    0x00C3B8F8: (
        "PE_IMPORT_MESSAGE_BOX_W_DIRECT_CALL",
        "exact_direct_import_call_wire_effect_unproved",
        "USER32.dll",
        "MessageBoxW",
        "FF15F8B8C300",
    ),
}

# Rows, W, R, unique function+call sites, unique messages.
EXPECTED_OTHER_EXACT_DIRECT_IMPORT_CALL_ROW_CENSUS = {
    0x00C3B1B0: (2, 1, 1, 1, 1),
    0x00C3B1B4: (4, 2, 2, 2, 1),
    0x00C3B434: (2, 1, 1, 1, 1),
    0x00C3B458: (6, 3, 3, 1, 3),
    0x00C3B478: (42, 21, 21, 10, 8),
    0x00C3B480: (8, 4, 4, 2, 4),
    0x00C3B488: (24, 12, 12, 5, 6),
    0x00C3B48C: (2, 1, 1, 1, 1),
    0x00C3B494: (8, 4, 4, 4, 2),
    0x00C3B498: (26, 13, 13, 7, 5),
    0x00C3B5C0: (2, 1, 1, 1, 1),
    0x00C3B8F8: (2, 1, 1, 1, 1),
}


class ExactImportThunkCall(NamedTuple):
    tag: str
    reason: str
    start_off: int
    iat_va: int
    dll: str
    symbol: str
    thunk_bytes_hex: str


EXACT_IMPORT_THUNK_CALLS = {
    0x0088D020: ExactImportThunkCall(
        "PE_IMPORT_MALLOC_REL32_THUNK_CALL",
        "exact_import_thunk_call_wire_effect_unproved",
        0x0048C420,
        0x00C3B87C,
        "MSVCR90.dll",
        "malloc",
        "FF257CB8C300",
    ),
    0x00B37998: ExactImportThunkCall(
        "PE_IMPORT_CXX_THROW_EXCEPTION_REL32_THUNK_CALL",
        "exact_import_thunk_call_wire_effect_unproved",
        0x00736D98,
        0x00C3B4C4,
        "MSVCR90.dll",
        "_CxxThrowException",
        "FF25C4B4C300",
    ),
}

# Independent mutation oracle; EXACT_IMPORT_THUNK_CALLS drives extraction.
EXPECTED_EXACT_IMPORT_THUNK_CALL_SEMANTICS = {
    0x0088D020: (
        "PE_IMPORT_MALLOC_REL32_THUNK_CALL",
        "exact_import_thunk_call_wire_effect_unproved",
        0x0048C420,
        0x00C3B87C,
        "MSVCR90.dll",
        "malloc",
        "FF257CB8C300",
    ),
    0x00B37998: (
        "PE_IMPORT_CXX_THROW_EXCEPTION_REL32_THUNK_CALL",
        "exact_import_thunk_call_wire_effect_unproved",
        0x00736D98,
        0x00C3B4C4,
        "MSVCR90.dll",
        "_CxxThrowException",
        "FF25C4B4C300",
    ),
}

# Rows, W, R, unique function+call sites, unique messages.
EXPECTED_EXACT_IMPORT_THUNK_CALL_ROW_CENSUS = {
    0x0088D020: (2, 1, 1, 1, 1),
    0x00B37998: (14, 2, 12, 4, 7),
}


class PeSecurityCookieCheckHelper(NamedTuple):
    tag: str
    reason: str
    start_off: int
    proof_end_va: int
    proof_sha256: str
    body_hex: str
    separator_hex: str
    security_cookie_va: int
    failure_target_va: int


PE_SECURITY_COOKIE_CHECK_HELPERS = {
    0x00B37964: PeSecurityCookieCheckHelper(
        "PE_SECURITY_COOKIE_CHECK_FAILURE_TAIL_HELPER",
        "pe_security_cookie_failure_path_wire_effect_unproved",
        0x00736D64,
        0x00B37973,
        "d31930a6047b3a9a986b1473f701e5b28070d619ab4d14daaa258ab445d25c43",
        "3B0DBCB402017502F3C3E9DF090000",
        "CCCCCCCCCCCCCCCCCCCCCCCCCC",
        0x0102B4BC,
        0x00B38352,
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_PE_SECURITY_COOKIE_CHECK_SEMANTICS = {
    0x00B37964: (
        "PE_SECURITY_COOKIE_CHECK_FAILURE_TAIL_HELPER",
        "pe_security_cookie_failure_path_wire_effect_unproved",
        0x00736D64,
        0x00B37973,
        "d31930a6047b3a9a986b1473f701e5b28070d619ab4d14daaa258ab445d25c43",
        "CCCCCCCCCCCCCCCCCCCCCCCCCC",
        0x0102B4BC,
        0x00B38352,
    ),
}

# Rows, W, R, unique function+call sites, unique messages.
EXPECTED_PE_SECURITY_COOKIE_CHECK_ROW_CENSUS = {
    0x00B37964: (19, 7, 12, 6, 12),
}


class ExactSingletonRegisterImportCall(NamedTuple):
    tag: str
    reason: str
    dll: str
    symbol: str


EXACT_SINGLETON_REGISTER_IMPORT_CALLS = {
    0x00C3B4C0: ExactSingletonRegisterImportCall(
        "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL",
        "invalid_parameter_singleton_register_call_wire_effect_unproved",
        "MSVCR90.dll",
        "_invalid_parameter_noinfo",
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_EXACT_SINGLETON_REGISTER_IMPORT_CALL_SEMANTICS = {
    0x00C3B4C0: (
        "PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REGISTER_CALL",
        "invalid_parameter_singleton_register_call_wire_effect_unproved",
        "MSVCR90.dll",
        "_invalid_parameter_noinfo",
    ),
}


class ExactMultiRegisterImportCall(NamedTuple):
    tag: str
    reason: str
    dll: str
    symbol: str


EXACT_MULTI_REGISTER_IMPORT_CALLS = {
    0x00C3B4C0: ExactMultiRegisterImportCall(
        "PE_IMPORT_INVALID_PARAMETER_NOINFO_MULTI_REGISTER_CALL",
        "invalid_parameter_multi_register_call_wire_effect_unproved",
        "MSVCR90.dll",
        "_invalid_parameter_noinfo",
    ),
}

# Independent mutation oracle; the extraction table above supplies row labels.
EXPECTED_EXACT_MULTI_REGISTER_IMPORT_CALL_SEMANTICS = {
    0x00C3B4C0: (
        "PE_IMPORT_INVALID_PARAMETER_NOINFO_MULTI_REGISTER_CALL",
        "invalid_parameter_multi_register_call_wire_effect_unproved",
        "MSVCR90.dll",
        "_invalid_parameter_noinfo",
    ),
}


@dataclass(frozen=True)
class Section:
    name: str
    va: int
    vsize: int
    raw_ptr: int
    raw_size: int
    characteristics: int

    @property
    def raw_end(self) -> int:
        return self.raw_ptr + self.raw_size

    @property
    def va_end(self) -> int:
        return self.va + self.raw_size


@dataclass(frozen=True)
class ImportSymbol:
    dll: str
    name: str
    iat_va: int
    iat_off: int
    descriptor_off: int
    lookup_off: int
    dll_name_off: int
    symbol_name_off: int


class Image:
    def __init__(self, path: Path):
        self.path = path
        self.data = path.read_bytes()
        self.sha256 = hashlib.sha256(self.data).hexdigest()
        if len(self.data) != EXPECTED_SIZE:
            raise ExtractionError(
                "image size mismatch: expected %d, got %d"
                % (EXPECTED_SIZE, len(self.data))
            )
        if self.sha256 != EXPECTED_SHA256:
            raise ExtractionError(
                "image sha256 mismatch: expected %s, got %s"
                % (EXPECTED_SHA256, self.sha256)
            )
        self.image_base, self.sections = self._parse_pe()
        if self.image_base != EXPECTED_IMAGE_BASE:
            raise ExtractionError(
                "ImageBase mismatch: expected 0x%08X, got 0x%08X"
                % (EXPECTED_IMAGE_BASE, self.image_base)
            )
        by_name = {s.name: s for s in self.sections}
        for name, expected in EXPECTED_SECTIONS.items():
            section = by_name.get(name)
            if section is None:
                raise ExtractionError("missing PE section %s" % name)
            got = (section.va, section.vsize, section.raw_ptr, section.raw_size)
            if got != expected:
                raise ExtractionError(
                    "PE section %s mismatch: expected %r, got %r"
                    % (name, expected, got)
                )
        self.imports_by_iat = self._parse_imports()
        measured_neutral = {
            iat_va: (symbol.dll, symbol.name)
            for iat_va, symbol in self.imports_by_iat.items()
            if (symbol.dll, symbol.name) in STACK_NEUTRAL_IMPORTS
        }
        if measured_neutral != EXPECTED_STACK_NEUTRAL_IAT:
            raise ExtractionError(
                "stack-neutral import census mismatch: %r" % measured_neutral
            )

    def _parse_pe(self) -> tuple[int, list[Section]]:
        data = self.data
        if data[:2] != b"MZ":
            raise ExtractionError("missing MZ signature")
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if data[e_lfanew : e_lfanew + 4] != b"PE\x00\x00":
            raise ExtractionError("missing PE signature")
        coff = e_lfanew + 4
        nsec = struct.unpack_from("<H", data, coff + 2)[0]
        opt_size = struct.unpack_from("<H", data, coff + 16)[0]
        opt = coff + 20
        if struct.unpack_from("<H", data, opt)[0] != 0x10B:
            raise ExtractionError("image is not PE32")
        image_base = struct.unpack_from("<I", data, opt + 28)[0]
        section_table = opt + opt_size
        sections = []
        for index in range(nsec):
            off = section_table + index * 40
            name = data[off : off + 8].rstrip(b"\x00").decode("latin1")
            vsize, rva, raw_size, raw_ptr = struct.unpack_from(
                "<IIII", data, off + 8
            )
            characteristics = struct.unpack_from("<I", data, off + 36)[0]
            sections.append(
                Section(
                    name=name,
                    va=image_base + rva,
                    vsize=vsize,
                    raw_ptr=raw_ptr,
                    raw_size=raw_size,
                    characteristics=characteristics,
                )
            )
        return image_base, sections

    def _ascii_at_off(self, off: int, limit: int = 1024) -> str:
        if not (0 <= off < len(self.data)):
            raise ExtractionError("import string offset is outside image")
        end = self.data.find(b"\x00", off, min(off + limit + 1, len(self.data)))
        if end < 0:
            raise ExtractionError("unterminated import string")
        try:
            return self.data[off:end].decode("ascii")
        except UnicodeDecodeError as exc:
            raise ExtractionError("non-ASCII import string") from exc

    def _parse_imports(self) -> dict[int, ImportSymbol]:
        """Parse named PE32 imports and preserve every supporting file offset."""
        data = self.data
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        coff = e_lfanew + 4
        opt = coff + 20
        directory_count = struct.unpack_from("<I", data, opt + 92)[0]
        if directory_count < 2:
            raise ExtractionError("PE image lacks import directory")
        import_rva, import_size = struct.unpack_from("<II", data, opt + 104)
        directory_va = self.image_base + import_rva
        directory_off = self.va_to_off(directory_va)
        if directory_off is None or import_size < 20:
            raise ExtractionError("PE import directory is unmapped")
        result: dict[int, ImportSymbol] = {}
        max_descriptors = import_size // 20
        terminated = False
        for descriptor_index in range(max_descriptors):
            descriptor_off = directory_off + descriptor_index * 20
            if descriptor_off + 20 > len(data):
                raise ExtractionError("truncated PE import descriptor")
            original, timestamp, forwarder, name_rva, first_thunk = (
                struct.unpack_from("<IIIII", data, descriptor_off)
            )
            if not any((original, timestamp, forwarder, name_rva, first_thunk)):
                terminated = True
                break
            dll_name_off = self.va_to_off(self.image_base + name_rva)
            if dll_name_off is None:
                raise ExtractionError("import DLL name is unmapped")
            dll = self._ascii_at_off(dll_name_off)
            lookup_rva = original or first_thunk
            for thunk_index in range(65536):
                lookup_va = self.image_base + lookup_rva + thunk_index * 4
                lookup_off = self.va_to_off(lookup_va)
                iat_va = self.image_base + first_thunk + thunk_index * 4
                iat_off = self.va_to_off(iat_va)
                if lookup_off is None or iat_off is None:
                    raise ExtractionError("import thunk is unmapped")
                value = struct.unpack_from("<I", data, lookup_off)[0]
                if value == 0:
                    break
                if value & 0x80000000:
                    continue
                hint_name_off = self.va_to_off(self.image_base + value)
                if hint_name_off is None or hint_name_off + 2 >= len(data):
                    raise ExtractionError("import hint/name is unmapped")
                symbol_name_off = hint_name_off + 2
                symbol = ImportSymbol(
                    dll=dll,
                    name=self._ascii_at_off(symbol_name_off),
                    iat_va=iat_va,
                    iat_off=iat_off,
                    descriptor_off=descriptor_off,
                    lookup_off=lookup_off,
                    dll_name_off=dll_name_off,
                    symbol_name_off=symbol_name_off,
                )
                if iat_va in result:
                    raise ExtractionError("duplicate import IAT slot")
                result[iat_va] = symbol
            else:
                raise ExtractionError("unterminated import thunk table")
        if not terminated:
            raise ExtractionError("unterminated PE import descriptor table")
        return result

    def section(self, name: str) -> Section:
        for section in self.sections:
            if section.name == name:
                return section
        raise ExtractionError("missing section %s" % name)

    def va_to_off(self, va: int) -> int | None:
        for section in self.sections:
            if section.va <= va < section.va_end:
                return section.raw_ptr + (va - section.va)
        return None

    def va_range_to_off(self, va: int, size: int) -> int | None:
        """Map a complete raw-backed VA range inside one PE section."""
        if size <= 0:
            return None
        for section in self.sections:
            delta = va - section.va
            if 0 <= delta and delta + size <= section.raw_size:
                return section.raw_ptr + delta
        return None

    def off_to_va(self, off: int) -> int | None:
        for section in self.sections:
            if section.raw_ptr <= off < section.raw_end:
                return section.va + (off - section.raw_ptr)
        return None

    def executable_va(self, va: int) -> bool:
        for section in self.sections:
            if section.va <= va < section.va_end:
                return bool(section.characteristics & 0x20000000)
        return False

    def read_cstring(self, va: int, limit: int = 512) -> str | None:
        off = self.va_to_off(va)
        if off is None:
            return None
        end = self.data.find(b"\x00", off, min(off + limit + 1, len(self.data)))
        if end < 0:
            return None
        try:
            return self.data[off:end].decode("ascii")
        except UnicodeDecodeError:
            return None

    def u32_off(self, off: int) -> int:
        return struct.unpack_from("<I", self.data, off)[0]


@dataclass(frozen=True)
class RegistryRow:
    name: str
    name_va: int
    reg_site_va: int
    id_global_va: int
    getter_va: int | None
    vtable_va: int | None
    serializer_va: int | None
    handler_va: int | None
    file_off_reg: int
    reason: str = ""
    resolution_proof: str = ""
    serializer_pointer_offs: tuple[int, ...] = ()
    handler_pointer_offs: tuple[int, ...] = ()
    serializer_resolution_proof: str = ""
    handler_resolution_proof: str = ""


@dataclass(frozen=True)
class FunctionSpan:
    start_va: int
    end_va: int
    start_off: int
    end_off: int
    sha256: str


@dataclass(frozen=True)
class FieldRow:
    message: str
    direction: str
    order: int
    tag: str
    field_offset: str
    length: str
    gate_condition: str
    span_start: int | None
    span_end: int | None
    span_sha256: str
    file_off_claim: int | None
    reason: str = ""


@dataclass(frozen=True)
class WireEvent:
    site_va: int
    directions: tuple[str, ...]
    tag: str
    field_expr: Expr | None
    length: str
    gate_condition: str
    span: FunctionSpan
    reason: str = ""
    target_va: int | None = None
    children: tuple["WireEvent", ...] = ()


@dataclass(frozen=True)
class ModeBranchProof:
    function_va: int
    formal_offset: int
    formal_width: int
    test_va: int
    test_off: int
    branch_va: int
    branch_off: int
    zero_direction: str
    nonzero_direction: str
    zero_nodes: frozenset[int]
    nonzero_nodes: frozenset[int]
    zero_anchor_va: int
    zero_anchor_off: int
    nonzero_anchor_va: int
    nonzero_anchor_off: int
    zero_anchor_evidence: str = ""
    nonzero_anchor_evidence: str = ""
    predicate_evidence: str = ""


REG32 = ("eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi")
REG8 = ("al", "cl", "dl", "bl", "ah", "ch", "dh", "bh")
LOW8_BY_REG32 = {"eax": "al", "ecx": "cl", "edx": "dl", "ebx": "bl"}
PREFIX_BYTES = frozenset((0xF0, 0xF2, 0xF3, 0x2E, 0x36, 0x3E, 0x26, 0x64, 0x65, 0x66, 0x67))


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

    def key(self) -> tuple:
        return (
            self.kind,
            self.reg,
            self.imm,
            self.base,
            self.index,
            self.scale,
            self.disp,
            self.absolute,
        )


@dataclass(frozen=True)
class Instruction:
    va: int
    off: int
    size: int
    raw: bytes
    kind: str
    dst: Operand | None = None
    src: Operand | None = None
    target: int | None = None
    imm: int | None = None
    condition: str | None = None
    test_mask: int | None = None

    @property
    def next_va(self) -> int:
        return self.va + self.size


@dataclass(frozen=True)
class PushArgument:
    instruction_va: int
    operand: Operand

    def key(self) -> tuple:
        return (self.instruction_va, self.operand.key())


def reg_operand(index: int, byte: bool = False) -> Operand:
    return Operand("reg", reg=(REG8 if byte else REG32)[index & 7])


def base_reg_name(name: str | None) -> str | None:
    if name is None:
        return None
    aliases = {
        "al": "eax", "ah": "eax",
        "cl": "ecx", "ch": "ecx",
        "dl": "edx", "dh": "edx",
        "bl": "ebx", "bh": "ebx",
    }
    return aliases.get(name, name)


def has_operand16_prefix(raw: bytes) -> bool:
    operand16 = False
    for value in raw:
        if value not in PREFIX_BYTES:
            break
        operand16 |= value == 0x66
    return operand16


def _signed(data: bytes, off: int, size: int) -> int:
    return int.from_bytes(data[off : off + size], "little", signed=True)


def _unsigned(data: bytes, off: int, size: int) -> int:
    return int.from_bytes(data[off : off + size], "little", signed=False)


def _parse_modrm(
    data: bytes,
    cursor: int,
    address16: bool,
    byte_operands: bool = False,
) -> tuple[int, int, Operand, Operand]:
    if cursor >= len(data):
        raise ExtractionError("truncated ModRM")
    modrm = data[cursor]
    cursor += 1
    mod = modrm >> 6
    reg = (modrm >> 3) & 7
    rm = modrm & 7
    reg_op = reg_operand(reg, byte_operands)
    if mod == 3:
        return cursor, reg, reg_op, reg_operand(rm, byte_operands)
    if address16:
        # Address-size overrides are not needed for field recovery.  Length is
        # still decoded exactly; the effective address remains explicit/unknown.
        if mod == 0 and rm == 6:
            disp = _unsigned(data, cursor, 2)
            cursor += 2
            rm_op = Operand("mem", absolute=disp)
        elif mod == 1:
            disp = _signed(data, cursor, 1)
            cursor += 1
            rm_op = Operand("mem", disp=disp)
        elif mod == 2:
            disp = _signed(data, cursor, 2)
            cursor += 2
            rm_op = Operand("mem", disp=disp)
        else:
            rm_op = Operand("mem")
        return cursor, reg, reg_op, rm_op

    base = index = None
    scale = 1
    absolute = None
    disp = 0
    if rm == 4:
        sib = data[cursor]
        cursor += 1
        scale = 1 << (sib >> 6)
        index_id = (sib >> 3) & 7
        base_id = sib & 7
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
    return cursor, reg, reg_op, Operand(
        "mem", base=base, index=index, scale=scale, disp=disp, absolute=absolute
    )


MODRM_ONE_BYTE = frozenset(
    list(range(0x00, 0x04))
    + list(range(0x08, 0x0C))
    + list(range(0x10, 0x14))
    + list(range(0x18, 0x1C))
    + list(range(0x20, 0x24))
    + list(range(0x28, 0x2C))
    + list(range(0x30, 0x34))
    + list(range(0x38, 0x3C))
    + [0x62, 0x63, 0x69, 0x6B]
    + list(range(0x80, 0x90))
    + [0xC0, 0xC1, 0xC4, 0xC5, 0xC6, 0xC7]
    + list(range(0xD0, 0xD4))
    + list(range(0xD8, 0xE0))
    + [0xF6, 0xF7, 0xFE, 0xFF]
)


NO_MODRM_0F = frozenset(
    [
        0x05, 0x06, 0x07, 0x08, 0x09, 0x0B, 0x0E,
        0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x37,
        0x77, 0xA0, 0xA1, 0xA2, 0xA8, 0xA9, 0xAA,
    ]
    + list(range(0xC8, 0xD0))
)
IMM8_0F = frozenset([0x0F, 0x70, 0x71, 0x72, 0x73, 0xA4, 0xAC, 0xBA, 0xC2, 0xC4, 0xC5, 0xC6])


def decode_instruction(image: Image, va: int, limit_off: int) -> Instruction:
    data = image.data
    off = image.va_to_off(va)
    if off is None or off >= limit_off:
        raise ExtractionError("instruction VA outside measured span: 0x%08X" % va)
    cursor = off
    operand16 = False
    address16 = False
    prefix_count = 0
    while cursor < limit_off and data[cursor] in PREFIX_BYTES:
        operand16 |= data[cursor] == 0x66
        address16 |= data[cursor] == 0x67
        cursor += 1
        prefix_count += 1
        if prefix_count >= 15:
            raise ExtractionError("too many instruction prefixes at 0x%08X" % va)
    if cursor >= limit_off:
        raise ExtractionError("truncated opcode at 0x%08X" % va)
    opcode_off = cursor
    op = data[cursor]
    cursor += 1
    op_size = 2 if operand16 else 4
    addr_size = 2 if address16 else 4
    two = None
    three = None
    modrm_reg = None
    reg_op = rm_op = None
    imm_size = 0
    rel_size = 0
    has_modrm = False

    if op == 0x0F:
        if cursor >= limit_off:
            raise ExtractionError("truncated 0F opcode at 0x%08X" % va)
        two = data[cursor]
        cursor += 1
        if two in (0x38, 0x3A):
            if cursor >= limit_off:
                raise ExtractionError("truncated three-byte opcode at 0x%08X" % va)
            three = data[cursor]
            cursor += 1
            has_modrm = True
            if two == 0x3A:
                imm_size = 1
        elif 0x80 <= two <= 0x8F:
            rel_size = op_size
        else:
            has_modrm = two not in NO_MODRM_0F
            if two in IMM8_0F:
                imm_size = 1
    else:
        has_modrm = op in MODRM_ONE_BYTE
        if op in (0x04, 0x0C, 0x14, 0x1C, 0x24, 0x2C, 0x34, 0x3C):
            imm_size = 1
        elif op in (0x05, 0x0D, 0x15, 0x1D, 0x25, 0x2D, 0x35, 0x3D):
            imm_size = op_size
        elif op == 0x68:
            imm_size = op_size
        elif op == 0x6A:
            imm_size = 1
        elif op == 0x69:
            imm_size = op_size
        elif op == 0x6B:
            imm_size = 1
        elif 0x70 <= op <= 0x7F:
            rel_size = 1
        elif op in (0x80, 0x82, 0x83):
            imm_size = 1
        elif op == 0x81:
            imm_size = op_size
        elif 0xA0 <= op <= 0xA3:
            imm_size = addr_size
        elif op == 0xA8:
            imm_size = 1
        elif op == 0xA9:
            imm_size = op_size
        elif 0xB0 <= op <= 0xB7:
            imm_size = 1
        elif 0xB8 <= op <= 0xBF:
            imm_size = op_size
        elif op in (0xC0, 0xC1):
            imm_size = 1
        elif op in (0xC2, 0xCA):
            imm_size = 2
        elif op == 0xC6:
            imm_size = 1
        elif op == 0xC7:
            imm_size = op_size
        elif op == 0xC8:
            imm_size = 3
        elif op == 0xCD:
            imm_size = 1
        elif op in (0xD4, 0xD5, 0xE4, 0xE5, 0xE6, 0xE7):
            imm_size = 1
        elif 0xE0 <= op <= 0xE3:
            rel_size = 1
        elif op in (0xE8, 0xE9):
            rel_size = op_size
        elif op == 0xEA:
            imm_size = op_size + 2
        elif op == 0xEB:
            rel_size = 1

    if has_modrm:
        byte_operands = op in (0x00, 0x02, 0x08, 0x0A, 0x10, 0x12, 0x18, 0x1A, 0x20, 0x22, 0x28, 0x2A, 0x30, 0x32, 0x38, 0x3A, 0x80, 0x82, 0x84, 0x86, 0x88, 0x8A, 0xC0, 0xC6, 0xD0, 0xD2, 0xF6, 0xFE)
        cursor, modrm_reg, reg_op, rm_op = _parse_modrm(
            data, cursor, address16, byte_operands=byte_operands
        )
        if op == 0xF6 and modrm_reg in (0, 1):
            imm_size = 1
        elif op == 0xF7 and modrm_reg in (0, 1):
            imm_size = op_size

    immediate_off = cursor
    cursor += imm_size + rel_size
    if cursor > limit_off or cursor - off > 15:
        raise ExtractionError("invalid/truncated instruction at 0x%08X" % va)
    raw = data[off:cursor]
    size = cursor - off
    kind = "other"
    dst = src = None
    target = immediate = test_mask = None
    condition = None

    if op == 0xE8:
        rel = _signed(data, immediate_off, rel_size)
        target = (va + size + rel) & 0xFFFFFFFF
        kind = "call"
    elif op in (0xE9, 0xEB):
        rel = _signed(data, immediate_off, rel_size)
        target = (va + size + rel) & 0xFFFFFFFF
        kind = "jmp"
    elif 0x70 <= op <= 0x7F:
        rel = _signed(data, immediate_off, 1)
        target = (va + size + rel) & 0xFFFFFFFF
        kind = "jcc"
        condition = "z" if op == 0x74 else "nz" if op == 0x75 else "other"
    elif op == 0x0F and two is not None and 0x80 <= two <= 0x8F:
        rel = _signed(data, immediate_off, rel_size)
        target = (va + size + rel) & 0xFFFFFFFF
        kind = "jcc"
        condition = "z" if two == 0x84 else "nz" if two == 0x85 else "other"
    elif op in (0xC3, 0xCB):
        kind = "ret"
        immediate = 0
    elif op in (0xC2, 0xCA):
        kind = "ret"
        immediate = _unsigned(data, immediate_off, 2)
    elif op == 0xCC:
        kind = "trap"
    elif 0x50 <= op <= 0x57:
        kind = "push"
        src = reg_operand(op - 0x50)
    elif op in (0x68, 0x6A):
        kind = "push"
        src = Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif 0x58 <= op <= 0x5F:
        kind = "pop"
        dst = reg_operand(op - 0x58)
    elif op == 0xFF and modrm_reg == 2:
        kind = "call_indirect"
        src = rm_op
    elif op == 0xFF and modrm_reg in (4, 5):
        kind = "jmp_indirect"
        src = rm_op
    elif op == 0xFF and modrm_reg == 6:
        kind = "push"
        src = rm_op
    elif op == 0x8D:
        kind = "lea"
        dst, src = reg_op, rm_op
    elif op in (0x8B, 0x8A):
        kind = "mov"
        dst, src = reg_op, rm_op
    elif op in (0x89, 0x88):
        kind = "mov"
        dst, src = rm_op, reg_op
    elif op in (0xA0, 0xA1):
        kind = "mov"
        dst = reg_operand(0, byte=(op == 0xA0))
        src = Operand("mem", absolute=_unsigned(data, immediate_off, imm_size))
    elif op in (0xA2, 0xA3):
        kind = "mov"
        dst = Operand("mem", absolute=_unsigned(data, immediate_off, imm_size))
        src = reg_operand(0, byte=(op == 0xA2))
    elif 0xB8 <= op <= 0xBF:
        kind = "mov"
        dst = reg_operand(op - 0xB8)
        src = Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif 0xB0 <= op <= 0xB7:
        kind = "mov"
        dst = reg_operand(op - 0xB0, byte=True)
        src = Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif op in (0xC6, 0xC7) and modrm_reg == 0:
        kind = "mov"
        dst = rm_op
        src = Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif op in (0x03, 0x2B, 0x33):
        kind = {0x03: "add", 0x2B: "sub", 0x33: "xor"}[op]
        dst, src = reg_op, rm_op
    elif op in (0x01, 0x29, 0x31):
        kind = {0x01: "add", 0x29: "sub", 0x31: "xor"}[op]
        dst, src = rm_op, reg_op
    elif op in (0x02, 0x0A, 0x22, 0x2A, 0x32):
        kind = {
            0x02: "add", 0x0A: "or", 0x22: "and",
            0x2A: "sub", 0x32: "xor",
        }[op]
        dst, src = reg_op, rm_op
    elif op in (0x00, 0x08, 0x20, 0x28, 0x30):
        kind = {
            0x00: "add", 0x08: "or", 0x20: "and",
            0x28: "sub", 0x30: "xor",
        }[op]
        dst, src = rm_op, reg_op
    elif op in (0x0B, 0x23):
        kind = {0x0B: "or", 0x23: "and"}[op]
        dst, src = reg_op, rm_op
    elif op in (0x09, 0x21):
        kind = {0x09: "or", 0x21: "and"}[op]
        dst, src = rm_op, reg_op
    elif op == 0x1B:
        kind = "unknown_write"
        dst, src = reg_op, rm_op
    elif op in (0x05, 0x0D, 0x25, 0x2D, 0x35):
        kind = {
            0x05: "add", 0x0D: "or", 0x25: "and",
            0x2D: "sub", 0x35: "xor",
        }[op]
        dst = reg_operand(0)
        src = Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif op in (0x69, 0x6B):
        kind = "unknown_write"
        dst, src = reg_op, rm_op
    elif op in (0x81, 0x83) and modrm_reg in (0, 5, 7):
        kind = {0: "add", 5: "sub", 7: "cmp"}[modrm_reg]
        dst = rm_op
        immediate = _signed(data, immediate_off, imm_size)
        src = Operand("imm", imm=immediate)
    elif op in (0x80, 0x82) and modrm_reg == 7:
        kind = "cmp"
        dst = rm_op
        immediate = _unsigned(data, immediate_off, imm_size)
        src = Operand("imm", imm=immediate)
    elif op in (0x81, 0x83) and modrm_reg in (1, 4):
        kind = {1: "or", 4: "and"}[modrm_reg]
        dst = rm_op
        src = Operand("imm", imm=_unsigned(data, immediate_off, imm_size))
    elif op in (0xC1, 0xD1, 0xD3) and modrm_reg in (4, 5, 7):
        kind = {4: "shl", 5: "shr", 7: "sar"}[modrm_reg]
        dst = rm_op
        if op == 0xC1:
            src = Operand("imm", imm=_unsigned(data, immediate_off, 1))
        elif op == 0xD1:
            src = Operand("imm", imm=1)
        else:
            src = reg_operand(1, byte=True)
    elif 0x40 <= op <= 0x47:
        kind = "inc"
        dst = reg_operand(op - 0x40)
    elif 0x48 <= op <= 0x4F:
        kind = "dec"
        dst = reg_operand(op - 0x48)
    elif op == 0xFE and modrm_reg in (0, 1):
        kind = "inc" if modrm_reg == 0 else "dec"
        dst = rm_op
    elif op in (0xF6, 0xF7) and modrm_reg == 0:
        kind = "test"
        dst = rm_op
        test_mask = _unsigned(data, immediate_off, imm_size)
    elif op == 0xF7 and modrm_reg in (2, 3):
        kind = "not" if modrm_reg == 2 else "neg"
        dst = rm_op
    elif op == 0xF7 and modrm_reg in (4, 5, 6, 7):
        kind = "muldiv_wide"
    elif op in (0xA8, 0xA9):
        kind = "test"
        dst = reg_operand(0, byte=(op == 0xA8))
        test_mask = _unsigned(data, immediate_off, imm_size)
    elif op in (0x84, 0x85):
        kind = "test"
        dst, src = rm_op, reg_op
    elif op in (0x38, 0x3A):
        kind = "cmp"
        dst, src = (rm_op, reg_op) if op == 0x38 else (reg_op, rm_op)
    elif op == 0x0F and two is not None and 0x90 <= two <= 0x9F:
        kind = "unknown_write"
        dst = rm_op
    elif op == 0x0F and two in (0xB6, 0xB7, 0xBE, 0xBF):
        kind = "mov"
        dst, src = reg_op, rm_op
    elif op == 0x0F and two in (0x2C, 0x2D, 0xAF):
        kind = "unknown_write"
        dst, src = reg_op, rm_op

    return Instruction(
        va=va,
        off=off,
        size=size,
        raw=raw,
        kind=kind,
        dst=dst,
        src=src,
        target=target,
        imm=immediate,
        condition=condition,
        test_mask=test_mask,
    )


@dataclass
class FunctionDecode:
    span: FunctionSpan
    instructions: dict[int, Instruction]
    successors: dict[int, tuple[int, ...]]
    predecessors: dict[int, tuple[int, ...]]
    errors: tuple[str, ...]


def decode_function(image: Image, span: FunctionSpan) -> FunctionDecode:
    instructions: dict[int, Instruction] = {}
    successors: dict[int, tuple[int, ...]] = {}
    errors = []
    work = [span.start_va]
    queued = {span.start_va}
    while work:
        va = work.pop()
        if va in instructions:
            continue
        if not (span.start_va <= va < span.end_va):
            errors.append("edge_outside_span@0x%08X" % va)
            continue
        try:
            ins = decode_instruction(image, va, span.end_off)
        except ExtractionError as exc:
            errors.append(str(exc))
            continue
        instructions[va] = ins
        if ins.kind in ("ret", "jmp_indirect", "trap"):
            next_nodes: tuple[int, ...] = ()
        elif ins.kind == "jmp":
            next_nodes = (ins.target,) if ins.target is not None else ()
        elif ins.kind == "jcc":
            nodes = [ins.next_va]
            if ins.target is not None:
                nodes.append(ins.target)
            next_nodes = tuple(nodes)
        else:
            next_nodes = (ins.next_va,) if ins.next_va < span.end_va else ()
        successors[va] = next_nodes
        for node in next_nodes:
            if span.start_va <= node < span.end_va and node not in queued:
                queued.add(node)
                work.append(node)
            elif not (span.start_va <= node <= span.end_va):
                errors.append("edge_outside_span@0x%08X->0x%08X" % (va, node))
    pred_lists: dict[int, list[int]] = defaultdict(list)
    for src_va, targets in successors.items():
        for target_va in targets:
            if target_va in instructions:
                pred_lists[target_va].append(src_va)
    predecessors = {
        va: tuple(sorted(pred_lists.get(va, []))) for va in instructions
    }
    return FunctionDecode(
        span=span,
        instructions=instructions,
        successors=successors,
        predecessors=predecessors,
        errors=tuple(sorted(set(errors))),
    )


def recover_call_pushes(
    decoded: FunctionDecode,
    call_va: int,
    count: int,
    max_steps: int = 4096,
) -> tuple[tuple[PushArgument, ...], ...]:
    """Recover call arguments by walking CFG predecessors, not linear bytes.

    The returned operands are in source push order.  A path is rejected if it
    crosses another call or an explicit stack rebalance before collecting the
    requested arguments.  This is what recovers widths hoisted above the W/R
    branch while refusing to borrow pushes from an unrelated path.
    """
    sequences: dict[tuple[tuple, ...], tuple[PushArgument, ...]] = {}
    work: list[tuple[int, tuple[PushArgument, ...]]] = [
        (pred, ()) for pred in decoded.predecessors.get(call_va, ())
    ]
    seen = set()
    steps = 0
    while work and steps < max_steps:
        va, collected = work.pop()
        steps += 1
        state_key = (va, tuple(arg.key() for arg in collected))
        if state_key in seen:
            continue
        seen.add(state_key)
        ins = decoded.instructions.get(va)
        if ins is None:
            continue
        next_collected = collected
        if ins.kind == "push" and ins.src is not None:
            next_collected = collected + (PushArgument(ins.va, ins.src),)
            if len(next_collected) == count:
                ordered = tuple(reversed(next_collected))
                sequences[tuple(arg.key() for arg in ordered)] = ordered
                continue
        elif ins.kind in ("call", "call_indirect", "ret", "pop"):
            continue
        elif (
            ins.kind in ("add", "sub")
            and ins.dst is not None
            and ins.dst.kind == "reg"
            and base_reg_name(ins.dst.reg) == "esp"
        ):
            continue
        for pred in decoded.predecessors.get(va, ()):
            work.append((pred, next_collected))
    return tuple(sequences[key] for key in sorted(sequences))


def recover_tail_mode(decoded: FunctionDecode, jump_va: int) -> frozenset[str] | None:
    """Recover an in-place [esp+8] direction rewrite before a tail jump."""
    found = set()
    work = list(decoded.predecessors.get(jump_va, ()))
    seen = set()
    while work:
        va = work.pop()
        if va in seen:
            continue
        seen.add(va)
        ins = decoded.instructions.get(va)
        if ins is None:
            continue
        if (
            ins.kind == "mov"
            and ins.dst is not None
            and ins.dst.kind == "mem"
            and ins.dst.base == "esp"
            and ins.dst.index is None
            and ins.dst.disp == 8
            and ins.src is not None
            and ins.src.kind == "imm"
            and ins.src.imm in (0, 1)
        ):
            found.add("W" if ins.src.imm == 1 else "R")
            continue
        if ins.kind in ("call", "call_indirect", "ret", "push", "pop"):
            continue
        if (
            ins.kind in ("add", "sub")
            and ins.dst is not None
            and ins.dst.kind == "reg"
            and base_reg_name(ins.dst.reg) == "esp"
        ):
            continue
        work.extend(decoded.predecessors.get(va, ()))
    return frozenset(found) if found else None


Expr = tuple


def expr_unknown(label: str) -> Expr:
    return ("unknown", label)


def expr_add(left: Expr, right: Expr) -> Expr:
    if left[0] == "const" and left[1] == 0:
        return right
    if right[0] == "const" and right[1] == 0:
        return left
    if left[0] == "const" and right[0] == "const":
        return ("const", left[1] + right[1])
    if right[0] == "const" and left[0] == "add" and left[2][0] == "const":
        return ("add", left[1], ("const", left[2][1] + right[1]))
    return ("add", left, right)


def expr_sub(left: Expr, right: Expr) -> Expr:
    if right[0] == "const":
        return expr_add(left, ("const", -right[1]))
    return ("sub", left, right)


def _format_signed_hex(value: int) -> str:
    return ("+0x%X" % value) if value >= 0 else ("-0x%X" % (-value))


def format_expr(expr: Expr) -> str:
    kind = expr[0]
    if kind == "obj":
        return "OBJ"
    if kind == "stack":
        return "STACK" + _format_signed_hex(expr[1])
    if kind == "stack_at":
        return "STACK@0x%08X%s" % (expr[1], _format_signed_hex(expr[2]))
    if kind == "const":
        return "0x%X" % (expr[1] & 0xFFFFFFFF)
    if kind == "reg":
        return "REG(%s)" % expr[1]
    if kind == "abs":
        return "ABS(0x%08X)" % expr[1]
    if kind == "mem":
        return "DEREF(%s)" % format_expr(expr[1])
    if kind == "add":
        left, right = expr[1], expr[2]
        if right[0] == "const":
            return format_expr(left) + _format_signed_hex(right[1])
        return "%s+%s" % (format_expr(left), format_expr(right))
    if kind == "sub":
        return "%s-%s" % (format_expr(expr[1]), format_expr(expr[2]))
    if kind == "mul":
        return "%s*%d" % (format_expr(expr[1]), expr[2])
    if kind in ("and", "or", "shl", "shr", "sar"):
        operator = {"and": "&", "or": "|", "shl": "<<", "shr": ">>", "sar": ">>s"}[kind]
        return "(%s%s%s)" % (
            format_expr(expr[1]), operator, format_expr(expr[2])
        )
    if kind in ("neg", "not"):
        operator = "-" if kind == "neg" else "~"
        return "%s(%s)" % (operator, format_expr(expr[1]))
    if kind == "phi":
        return "PHI(%s)" % "|".join(format_expr(item) for item in expr[1])
    if kind == "ret":
        return "RET(%s)" % (
            "INDIRECT" if expr[1] is None else "0x%08X" % expr[1]
        )
    return "UNKNOWN(%s)" % expr[1]


def substitute_expr(expr: Expr, obj: Expr, function_va: int) -> Expr:
    """Replace a callee's symbolic OBJ/STACK roots with exact call context."""
    kind = expr[0]
    if kind == "obj":
        return obj
    if kind == "stack":
        return ("stack_at", function_va, expr[1])
    if kind in ("mem",):
        return (kind, substitute_expr(expr[1], obj, function_va))
    if kind in ("add", "sub"):
        return (
            kind,
            substitute_expr(expr[1], obj, function_va),
            substitute_expr(expr[2], obj, function_va),
        )
    if kind == "mul":
        return (kind, substitute_expr(expr[1], obj, function_va), expr[2])
    if kind in ("and", "or", "shl", "shr", "sar"):
        return (
            kind,
            substitute_expr(expr[1], obj, function_va),
            substitute_expr(expr[2], obj, function_va),
        )
    if kind in ("neg", "not"):
        return (kind, substitute_expr(expr[1], obj, function_va))
    if kind == "phi":
        return (
            "phi",
            tuple(substitute_expr(item, obj, function_va) for item in expr[1]),
        )
    return expr


def field_offset_from_expr(expr: Expr) -> str:
    if expr == ("obj",):
        return "+0x00"
    if expr[0] == "add" and expr[1] == ("obj",) and expr[2][0] == "const":
        return _format_signed_hex(expr[2][1])
    text = format_expr(expr)
    if text.startswith("DEREF(OBJ"):
        text = text.replace("DEREF(OBJ", "DEREF(", 1)
    return text


class RegisterResolver:
    def __init__(self, decoded: FunctionDecode):
        self.decoded = decoded
        self.memo: dict[tuple[int, str], Expr] = {}
        self.visiting: set[tuple[int, str]] = set()

    def operand_before(self, at_va: int, operand: Operand, dereference: bool = False) -> Expr:
        if operand.kind == "imm":
            return ("const", operand.imm or 0)
        if operand.kind == "reg":
            return self.reg_before(at_va, base_reg_name(operand.reg) or "unknown")
        if operand.kind == "mem":
            address = self.mem_address_before(at_va, operand)
            return ("mem", address) if dereference else address
        return expr_unknown("operand")

    def mem_address_before(self, at_va: int, operand: Operand) -> Expr:
        if operand.absolute is not None:
            result: Expr = ("abs", operand.absolute)
        elif operand.base == "esp":
            result = ("stack", operand.disp)
            if operand.index is not None:
                idx = self.reg_before(at_va, operand.index)
                if operand.scale != 1:
                    idx = ("mul", idx, operand.scale)
                result = expr_add(result, idx)
            return result
        elif operand.base is not None:
            result = self.reg_before(at_va, operand.base)
        else:
            result = ("const", 0)
        if operand.index is not None:
            idx = self.reg_before(at_va, operand.index)
            if operand.scale != 1:
                idx = ("mul", idx, operand.scale)
            result = expr_add(result, idx)
        if operand.disp:
            result = expr_add(result, ("const", operand.disp))
        return result

    def reg_before(self, at_va: int, reg: str) -> Expr:
        reg = base_reg_name(reg) or reg
        key = (at_va, reg)
        if key in self.memo:
            return self.memo[key]
        if key in self.visiting:
            return ("reg", reg)
        self.visiting.add(key)
        values = []
        preds = self.decoded.predecessors.get(at_va, ())
        if not preds:
            value = ("obj",) if reg == "ecx" else ("stack", 0) if reg == "esp" else ("reg", reg)
            values.append(value)
        for pred_va in preds:
            values.append(self._reg_after_instruction(pred_va, reg))
        unique = {repr(value): value for value in values}
        if len(unique) == 1:
            result = next(iter(unique.values()))
        elif unique:
            result = ("phi", tuple(unique[key] for key in sorted(unique)))
        else:
            result = expr_unknown("no_predecessor")
        self.visiting.remove(key)
        self.memo[key] = result
        return result

    def _reg_after_instruction(self, ins_va: int, reg: str) -> Expr:
        ins = self.decoded.instructions[ins_va]
        dst_reg = None
        if ins.dst is not None and ins.dst.kind == "reg":
            dst_reg = base_reg_name(ins.dst.reg)
        if ins.kind == "muldiv_wide" and reg in ("eax", "edx"):
            return expr_unknown("write@0x%08X" % ins.va)
        if ins.kind in ("call", "call_indirect") and reg in ("eax", "ecx", "edx"):
            if reg == "eax":
                return ("ret", ins.target)
            return expr_unknown("call_clobber@0x%08X:%s" % (ins.va, reg))
        if ins.kind not in (
            "lea", "mov", "add", "sub", "xor", "inc", "dec",
            "and", "or", "shl", "shr", "sar", "neg", "not",
            "unknown_write", "pop",
        ):
            return self.reg_before(ins.va, reg)
        if dst_reg != reg:
            return self.reg_before(ins.va, reg)
        if (
            ins.dst is not None
            and (ins.dst.reg in REG8 or has_operand16_prefix(ins.raw))
        ):
            return expr_unknown("partial_write@0x%08X:%s" % (ins.va, reg))
        if ins.kind == "lea" and ins.src is not None and ins.src.kind == "mem":
            return self.mem_address_before(ins.va, ins.src)
        if ins.kind == "mov" and ins.src is not None:
            return self.operand_before(ins.va, ins.src, dereference=(ins.src.kind == "mem"))
        if ins.kind in ("add", "sub") and ins.src is not None:
            prior = self.reg_before(ins.va, reg)
            rhs = self.operand_before(ins.va, ins.src, dereference=(ins.src.kind == "mem"))
            return expr_add(prior, rhs) if ins.kind == "add" else expr_sub(prior, rhs)
        if ins.kind in ("and", "or", "shl", "shr", "sar") and ins.src is not None:
            prior = self.reg_before(ins.va, reg)
            rhs = self.operand_before(
                ins.va, ins.src, dereference=(ins.src.kind == "mem")
            )
            return (ins.kind, prior, rhs)
        if ins.kind in ("neg", "not"):
            return (ins.kind, self.reg_before(ins.va, reg))
        if ins.kind == "unknown_write":
            return expr_unknown("write@0x%08X" % ins.va)
        if ins.kind == "xor" and ins.src is not None and ins.src.kind == "reg" and base_reg_name(ins.src.reg) == reg:
            return ("const", 0)
        if ins.kind == "inc":
            return expr_add(self.reg_before(ins.va, reg), ("const", 1))
        if ins.kind == "dec":
            return expr_add(self.reg_before(ins.va, reg), ("const", -1))
        return expr_unknown("write@0x%08X" % ins.va)


def find_function_span(image: Image, start_va: int) -> FunctionSpan | None:
    start_off = image.va_to_off(start_va)
    if start_off is None or not image.executable_va(start_va):
        return None
    containing = next(
        section
        for section in image.sections
        if section.raw_ptr <= start_off < section.raw_end
    )
    data = image.data
    for off in range(start_off, containing.raw_end - 3):
        if data[off] == 0xC3 and data[off + 1 : off + 4] == b"\xcc\xcc\xcc":
            end_off = off + 1
        elif (
            data[off] == 0xC2
            and off + 6 <= containing.raw_end
            and data[off + 3 : off + 6] == b"\xcc\xcc\xcc"
        ):
            end_off = off + 3
        else:
            continue
        end_va = image.off_to_va(end_off - 1)
        if end_va is None:
            return None
        span_bytes = data[start_off:end_off]
        return FunctionSpan(
            start_va=start_va,
            end_va=end_va + 1,
            start_off=start_off,
            end_off=end_off,
            sha256=hashlib.sha256(span_bytes).hexdigest(),
        )
    return None


def raw_rel32_calls(image: Image, span: FunctionSpan) -> list[tuple[int, int]]:
    """Byte-pattern census of every E8 rel32 occurrence in one measured span."""
    out = []
    for off in find_all(image.data, b"\xe8", span.start_off, span.end_off):
        if off + 5 > span.end_off:
            continue
        call_va = image.off_to_va(off)
        if call_va is None:
            continue
        rel = struct.unpack_from("<i", image.data, off + 1)[0]
        out.append((call_va, rel32_target(call_va, rel)))
    return out


def _reachable_nodes(decoded: FunctionDecode, start_va: int) -> frozenset[int]:
    if start_va not in decoded.instructions:
        return frozenset()
    seen = set()
    work = [start_va]
    while work:
        va = work.pop()
        if va in seen or va not in decoded.instructions:
            continue
        seen.add(va)
        work.extend(decoded.successors.get(va, ()))
    return frozenset(seen)


def build_gate_map(decoded: FunctionDecode) -> dict[int, str]:
    """Map instructions to immediate-mask branch control dependencies."""
    labels: dict[int, list[tuple[int, str]]] = defaultdict(list)
    reach_cache: dict[int, frozenset[int]] = {}

    def reachable(start_va: int) -> frozenset[int]:
        if start_va not in reach_cache:
            reach_cache[start_va] = _reachable_nodes(decoded, start_va)
        return reach_cache[start_va]

    for test in sorted(decoded.instructions.values(), key=lambda ins: ins.va):
        if test.kind != "test" or test.test_mask is None:
            continue
        branch = decoded.instructions.get(test.next_va)
        if (
            branch is None
            or branch.kind != "jcc"
            or branch.condition not in ("z", "nz")
            or branch.target is None
        ):
            continue
        fall_nodes = reachable(branch.next_va)
        jump_nodes = reachable(branch.target)
        fall_only = fall_nodes - jump_nodes
        jump_only = jump_nodes - fall_nodes
        if branch.condition == "z":
            set_nodes, clear_nodes = fall_only, jump_only
        else:
            set_nodes, clear_nodes = jump_only, fall_only
        for node in set_nodes:
            labels[node].append(
                (
                    test.va,
                    "test@0x%08X file_off=0x%08X mask=0x%X set"
                    % (test.va, test.off, test.test_mask),
                )
            )
        for node in clear_nodes:
            labels[node].append(
                (
                    test.va,
                    "test@0x%08X file_off=0x%08X mask=0x%X clear"
                    % (test.va, test.off, test.test_mask),
                )
            )
    return {
        va: " AND ".join(label for _site, label in sorted(items))
        for va, items in labels.items()
    }


def combine_gate(parent: str, child: str) -> str:
    parts = []
    for text in (parent, child):
        if text and text != "ALWAYS" and text not in parts:
            parts.append(text)
    return " AND ".join(parts) if parts else "ALWAYS"


def string_wire_helper_fragment(image: Image, target_va: int) -> str:
    """Return the complete image-linked proof marker for one pinned helper."""
    spec = STRING_WIRE_HELPERS[target_va]
    import_fragments = []
    for iat_va in spec.required_iats:
        symbol = image.imports_by_iat[iat_va]
        import_fragments.append(
            "0x%08X@iat_file_off=0x%08X@descriptor_file_off=0x%08X"
            "@lookup_file_off=0x%08X@dll_name_file_off=0x%08X"
            "@symbol_name_file_off=0x%08X@dll=%s@symbol=%s"
            % (
                iat_va,
                symbol.iat_off,
                symbol.descriptor_off,
                symbol.lookup_off,
                symbol.dll_name_off,
                symbol.symbol_name_off,
                symbol.dll,
                symbol.name,
            )
        )
    return (
        "string_wire_helper target=0x%08X target_file_off=0x%08X "
        "proof_end=0x%08X proof_end_file_off=0x%08X proof_sha256=%s "
        "direction=%s kind=%s length_prefix=uint32le payload=N_bytes "
        "memcpy_thunk=0x00B37B80 memcpy_thunk_file_off=0x00736F80 "
        "memcpy_iat=0x00C3B504 imports=(%s) "
        "basis=exact_helper_bytes_and_pe_imports"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.direction,
            spec.string_kind,
            ";".join(import_fragments),
        )
    )


def atomic_object_helper_fragment(image: Image, target_va: int) -> str:
    """Return image-linked evidence for one exact atomic object helper."""
    spec = ATOMIC_OBJECT_HELPERS[target_va]
    symbol = image.imports_by_iat[spec.iat_va]
    return (
        "atomic_object_helper target=0x%08X target_file_off=0x%08X "
        "proof_end=0x%08X proof_end_file_off=0x%08X proof_sha256=%s "
        "iat=0x%08X iat_file_off=0x%08X "
        "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
        "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
        "dll=%s symbol=%s operation=%s "
        "basis=exact_full_body_and_pe_import"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.iat_va,
            symbol.iat_off,
            symbol.descriptor_off,
            symbol.lookup_off,
            symbol.dll_name_off,
            symbol.symbol_name_off,
            symbol.dll,
            symbol.name,
            spec.tag,
        )
    )


def pure_chain_helper_fragment(target_va: int) -> str:
    """Return exact evidence for the pinned read-only chain predicate."""
    spec = PURE_CHAIN_HELPERS[target_va]
    return (
        "pure_chain_helper target=0x%08X target_file_off=0x%08X "
        "proof_end=0x%08X proof_end_file_off=0x%08X proof_sha256=%s "
        "arguments=stack_plus_04_needle,stack_plus_08_chain_head "
        "step=load_pointer_plus_04 return=bool_al memory_writes=0 calls=0 "
        "basis=exact_full_body"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
        )
    )


def mutable_chain_helper_fragment(image: Image, target_va: int) -> str:
    spec = MUTABLE_CHAIN_HELPERS[target_va]
    symbol = image.imports_by_iat[spec.iat_va]
    return (
        "mutable_chain_helper target=0x%08X target_file_off=0x%08X "
        "proof_end=0x%08X proof_end_file_off=0x%08X proof_sha256=%s "
        "memory_write_sites=0x00B0BFAB,0x00B0BFC8,0x00B0BFD7 "
        "memory_write_shape=object_plus_04 object_alias=unproved "
        "iat=0x%08X iat_file_off=0x%08X "
        "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
        "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
        "dll=%s symbol=%s basis=exact_full_body_and_pe_import"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.iat_va,
            symbol.iat_off,
            symbol.descriptor_off,
            symbol.lookup_off,
            symbol.dll_name_off,
            symbol.symbol_name_off,
            symbol.dll,
            symbol.name,
        )
    )


def locked_mutable_pointer_slot_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = LOCKED_MUTABLE_POINTER_SLOT_HELPERS[target_va]
    invalid = image.imports_by_iat[0x00C3B4C0]
    malloc = image.imports_by_iat[0x00C3B87C]
    enter = image.imports_by_iat[0x00C3B16C]
    leave = image.imports_by_iat[0x00C3B168]
    exchange_add = image.imports_by_iat[0x00C3B19C]
    return (
        "locked_mutable_pointer_slot_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "memory_write_sites=0x0066AC14,0x0066AC17,0x0066ABE1,"
        "0x0066ABF9,0x0066AC1D slot_scale=4 "
        "nested_unresolved_target=0x007016A0 "
        "enter_wrapper=0x0088D5B0 enter_iat=0x%08X "
        "enter_iat_file_off=0x%08X enter_symbol=%s!%s "
        "leave_wrapper=0x0049DA40 leave_iat=0x%08X "
        "leave_iat_file_off=0x%08X leave_symbol=%s!%s "
        "exchange_add_wrapper=0x004A0680 exchange_add_iat=0x%08X "
        "exchange_add_iat_file_off=0x%08X exchange_add_symbol=%s!%s "
        "invalid_iat=0x%08X invalid_iat_file_off=0x%08X "
        "invalid_symbol=%s!%s malloc_iat=0x%08X "
        "malloc_iat_file_off=0x%08X malloc_symbol=%s!%s "
        "object_alias=unproved basis=exact_full_body_support_wrappers_and_pe_imports"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            enter.iat_va,
            enter.iat_off,
            enter.dll,
            enter.name,
            leave.iat_va,
            leave.iat_off,
            leave.dll,
            leave.name,
            exchange_add.iat_va,
            exchange_add.iat_off,
            exchange_add.dll,
            exchange_add.name,
            invalid.iat_va,
            invalid.iat_off,
            invalid.dll,
            invalid.name,
            malloc.iat_va,
            malloc.iat_off,
            malloc.dll,
            malloc.name,
        )
    )


def critical_section_pointer_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = CRITICAL_SECTION_POINTER_HELPERS[target_va]
    symbol = image.imports_by_iat[spec.iat_va]
    return (
        "critical_section_pointer_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "pointer_load=deref_ecx iat=0x%08X iat_file_off=0x%08X "
        "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
        "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
        "dll=%s symbol=%s operation=%s pointer_alias=unproved "
        "basis=exact_full_body_and_pe_import"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.iat_va,
            symbol.iat_off,
            symbol.descriptor_off,
            symbol.lookup_off,
            symbol.dll_name_off,
            symbol.symbol_name_off,
            symbol.dll,
            symbol.name,
            spec.tag,
        )
    )


def mutable_dword_range_growth_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = MUTABLE_DWORD_RANGE_GROWTH_HELPERS[target_va]
    invalid = image.imports_by_iat[spec.invalid_iat_va]
    nested_off = image.va_to_off(spec.nested_target_va)
    if nested_off is None:
        raise ExtractionError("mutable dword range nested target is unmapped")
    return (
        "mutable_dword_range_growth_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "dword_zero_write=0x007016E7 dword_end_write=0x007016F0 "
        "slot_scale=4 nested_unresolved_target=0x%08X "
        "nested_target_file_off=0x%08X invalid_iat=0x%08X "
        "invalid_iat_file_off=0x%08X descriptor_file_off=0x%08X "
        "lookup_file_off=0x%08X dll_name_file_off=0x%08X "
        "symbol_name_file_off=0x%08X invalid_symbol=%s!%s "
        "object_alias=unproved basis=exact_full_body_and_pe_import"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.nested_target_va,
            nested_off,
            spec.invalid_iat_va,
            invalid.iat_off,
            invalid.descriptor_off,
            invalid.lookup_off,
            invalid.dll_name_off,
            invalid.symbol_name_off,
            invalid.dll,
            invalid.name,
        )
    )


def mutable_dword_slot_operation_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = MUTABLE_DWORD_SLOT_OPERATION_HELPERS[target_va]
    invalid = image.imports_by_iat[spec.invalid_iat_va]
    nested_offs = tuple(image.va_to_off(va) for va in spec.nested_target_vas)
    if any(off is None for off in nested_offs):
        raise ExtractionError("mutable dword slot nested target is unmapped")
    return (
        "mutable_dword_slot_operation_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "stack_zero_write=0x00AC6EAC state_end_write=0x00AC6ECE "
        "slot_scale=4 nested_unresolved_targets=0x%08X,0x%08X "
        "nested_target_file_offs=0x%08X,0x%08X invalid_iat=0x%08X "
        "invalid_iat_file_off=0x%08X descriptor_file_off=0x%08X "
        "lookup_file_off=0x%08X dll_name_file_off=0x%08X "
        "symbol_name_file_off=0x%08X invalid_symbol=%s!%s "
        "entry_instruction_count=53 ret4_sites=0x00AC6ED6,0x00AC6EFD "
        "object_alias=unproved basis=bounded_entry_cfg_exact_body_and_pe_import"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.nested_target_vas[0],
            spec.nested_target_vas[1],
            nested_offs[0],
            nested_offs[1],
            spec.invalid_iat_va,
            invalid.iat_off,
            invalid.descriptor_off,
            invalid.lookup_off,
            invalid.dll_name_off,
            invalid.symbol_name_off,
            invalid.dll,
            invalid.name,
        )
    )


def mutable_pointer_slot_traversal_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS[target_va]
    invalid = image.imports_by_iat[spec.invalid_iat_va]
    return (
        "mutable_pointer_slot_traversal_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "state_slot_writes=0x0046D2EB,0x0046D308,0x0046D317 "
        "state_slot=ECX_object+0x04 node_flag_offset=0x21 "
        "invalid_iat_load=0x0046D2B7 invalid_call_sites=0x0046D2BF,0x0046D2CA "
        "invalid_iat=0x%08X invalid_iat_file_off=0x%08X "
        "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
        "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
        "invalid_symbol=%s!%s entry_instruction_count=44 "
        "ret_sites=0x0046D2CE,0x0046D2EF,0x0046D31B "
        "object_alias=unproved basis=exact_full_body_and_pe_import"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.invalid_iat_va,
            invalid.iat_off,
            invalid.descriptor_off,
            invalid.lookup_off,
            invalid.dll_name_off,
            invalid.symbol_name_off,
            invalid.dll,
            invalid.name,
        )
    )


def locked_mutable_dword_slot_update_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS[target_va]
    invalid = image.imports_by_iat[spec.invalid_iat_va]
    nested_offs = tuple(image.va_to_off(va) for va in spec.nested_target_vas)
    if any(off is None for off in nested_offs):
        raise ExtractionError("locked mutable dword slot target is unmapped")
    return (
        "locked_mutable_dword_slot_update_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "nested_targets=0x%08X,0x%08X,0x%08X "
        "nested_target_file_offs=0x%08X,0x%08X,0x%08X "
        "counter_decrement=0x00710FCC output_write=0x00710FE2 "
        "slot_write=0x00710FFB counter_increment=0x00710FFE "
        "invalid_call_sites=0x00710FD6,0x00710FF2 invalid_iat=0x%08X "
        "invalid_iat_file_off=0x%08X descriptor_file_off=0x%08X "
        "lookup_file_off=0x%08X dll_name_file_off=0x%08X "
        "symbol_name_file_off=0x%08X invalid_symbol=%s!%s "
        "entry_instruction_count=42 ret4_site=0x0071100C "
        "object_alias=unproved basis=bounded_entry_cfg_exact_body_and_pe_import"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.nested_target_vas[0],
            spec.nested_target_vas[1],
            spec.nested_target_vas[2],
            nested_offs[0],
            nested_offs[1],
            nested_offs[2],
            spec.invalid_iat_va,
            invalid.iat_off,
            invalid.descriptor_off,
            invalid.lookup_off,
            invalid.dll_name_off,
            invalid.symbol_name_off,
            invalid.dll,
            invalid.name,
        )
    )


def nested_call_composition_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = NESTED_CALL_COMPOSITION_HELPERS[target_va]
    nested_offs = tuple(image.va_to_off(va) for va in spec.nested_target_vas)
    if any(off is None for off in nested_offs):
        raise ExtractionError("nested call composition target is unmapped")
    return (
        "nested_three_call_composition_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "nested_targets=0x%08X,0x%08X,0x%08X "
        "nested_target_file_offs=0x%08X,0x%08X,0x%08X "
        "direct_call_sites=0x005F8DE3,0x005F8DEF,0x005F8DFB "
        "result_zero_extend=0x005F8DF4 member_address=ECX_object+0x50 "
        "entry_instruction_count=13 explicit_mov_memory_writes=0 "
        "ret4_site=0x005F8E01 object_alias=unproved "
        "basis=exact_full_body_and_nested_targets"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.nested_target_vas[0],
            spec.nested_target_vas[1],
            spec.nested_target_vas[2],
            nested_offs[0],
            nested_offs[1],
            nested_offs[2],
        )
    )


def ecx_plus_50_tail_jump_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = ECX_PLUS_50_TAIL_JUMP_HELPERS[target_va]
    tail_target_off = image.va_to_off(spec.tail_target_va)
    if tail_target_off is None:
        raise ExtractionError("ECX+0x50 tail target is unmapped")
    return (
        "ecx_plus_50_tail_jump_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "ecx_adjust_site=0x005F8C30 ecx_adjust=+0x50 "
        "tail_jump_site=0x005F8C33 tail_target=0x%08X "
        "tail_target_file_off=0x%08X separator_start=0x005F8C38 "
        "separator_file_off=0x001F8038 separator_cc_count=8 "
        "entry_instruction_count=2 entry_reachable_instruction_count=2 "
        "object_alias=unproved "
        "basis=exact_entry_prefix_tail_target_and_int3_separator"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.tail_target_va,
            tail_target_off,
        )
    )


def exact_direct_import_call_fragment(image: Image, iat_va: int) -> str:
    spec = EXACT_DIRECT_IMPORT_CALLS[iat_va]
    symbol = image.imports_by_iat[iat_va]
    return (
        "exact_direct_iat_import iat=0x%08X iat_file_off=0x%08X "
        "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
        "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
        "dll=%s symbol=%s call_bytes=%s operation=%s "
        "wire_effect=unproved basis=exact_call_bytes_and_pe_import"
        % (
            iat_va,
            symbol.iat_off,
            symbol.descriptor_off,
            symbol.lookup_off,
            symbol.dll_name_off,
            symbol.symbol_name_off,
            symbol.dll,
            symbol.name,
            spec.call_bytes_hex,
            spec.tag,
        )
    )


def exact_import_thunk_call_fragment(image: Image, target_va: int) -> str:
    spec = EXACT_IMPORT_THUNK_CALLS[target_va]
    symbol = image.imports_by_iat[spec.iat_va]
    return (
        "exact_rel32_iat_thunk target=0x%08X target_file_off=0x%08X "
        "thunk_bytes=%s iat=0x%08X iat_file_off=0x%08X "
        "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
        "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
        "dll=%s symbol=%s operation=%s wire_effect=unproved "
        "basis=exact_rel32_target_unconditional_iat_tail_jump_and_pe_import"
        % (
            target_va,
            spec.start_off,
            spec.thunk_bytes_hex,
            spec.iat_va,
            symbol.iat_off,
            symbol.descriptor_off,
            symbol.lookup_off,
            symbol.dll_name_off,
            symbol.symbol_name_off,
            symbol.dll,
            symbol.name,
            spec.tag,
        )
    )


def pe_security_cookie_check_helper_fragment(
    image: Image, target_va: int
) -> str:
    spec = PE_SECURITY_COOKIE_CHECK_HELPERS[target_va]
    failure_target_off = image.va_to_off(spec.failure_target_va)
    if failure_target_off is None:
        raise ExtractionError("PE security-cookie failure target is unmapped")
    return (
        "pe_security_cookie_check_helper target=0x%08X "
        "target_file_off=0x%08X proof_end=0x%08X "
        "proof_end_file_off=0x%08X proof_sha256=%s "
        "compare_site=0x00B37964 compare_file_off=0x00736D64 "
        "security_cookie_va=0x%08X branch_site=0x00B3796A "
        "branch_file_off=0x00736D6A return_site=0x00B3796C "
        "return_file_off=0x00736D6C failure_tail_site=0x00B3796E "
        "failure_tail_file_off=0x00736D6E failure_target=0x%08X "
        "failure_target_file_off=0x%08X separator_start=0x00B37973 "
        "separator_file_off=0x00736D73 separator_cc_count=13 "
        "coff_size_of_optional_header_file_off=0x0000013C "
        "coff_size_of_optional_header=0xE0 "
        "number_of_rva_and_sizes_file_off=0x0000019C "
        "number_of_rva_and_sizes=16 "
        "load_config_directory_entry_file_off=0x000001F0 "
        "load_config_rva=0x00BBC570 load_config_directory_size=0x40 "
        "load_config_file_off=0x00BBA970 load_config_structure_size=0x48 "
        "security_cookie_field_file_off=0x00BBA9AC "
        "entry_instruction_count=4 failure_path_wire_effect=unproved "
        "basis=exact_bounded_entry_pe_load_config_and_int3_separator"
        % (
            target_va,
            spec.start_off,
            spec.proof_end_va,
            spec.start_off + (spec.proof_end_va - target_va),
            spec.proof_sha256,
            spec.security_cookie_va,
            spec.failure_target_va,
            failure_target_off,
        )
    )


def exact_singleton_register_import_call_fragment(
    image: Image,
    function_va: int,
    call_va: int,
    register: str,
    definition_va: int,
    iat_va: int,
) -> str:
    spec = EXACT_SINGLETON_REGISTER_IMPORT_CALLS[iat_va]
    symbol = image.imports_by_iat[iat_va]
    call_off = image.va_to_off(call_va)
    definition_off = image.va_to_off(definition_va)
    if call_off is None or definition_off is None:
        raise ExtractionError("singleton register import evidence is unmapped")
    register_index = REG32.index(register)
    call_bytes = bytes((0xFF, 0xD0 | register_index))
    definition_bytes = (
        bytes((0x8B, 0x05 | (register_index << 3)))
        + struct.pack("<I", iat_va)
    )
    return (
        "exact_singleton_register_iat_call@0x%08X file_off=0x%08X "
        "function=0x%08X register=%s definition@0x%08X "
        "definition_file_off=0x%08X iat=0x%08X "
        "call_bytes=%s definition_bytes=%s iat_file_off=0x%08X "
        "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
        "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
        "dll=%s symbol=%s operation=%s wire_effect=unproved "
        "basis=singleton_reaching_exact_iat_load"
        % (
            call_va,
            call_off,
            function_va,
            register,
            definition_va,
            definition_off,
            iat_va,
            call_bytes.hex().upper(),
            definition_bytes.hex().upper(),
            symbol.iat_off,
            symbol.descriptor_off,
            symbol.lookup_off,
            symbol.dll_name_off,
            symbol.symbol_name_off,
            symbol.dll,
            symbol.name,
            spec.tag,
        )
    )


def exact_multi_register_import_call_fragment(
    image: Image,
    function_va: int,
    call_va: int,
    register: str,
    definition_vas: tuple[int, ...],
    iat_va: int,
) -> str:
    spec = EXACT_MULTI_REGISTER_IMPORT_CALLS[iat_va]
    symbol = image.imports_by_iat[iat_va]
    call_off = image.va_to_off(call_va)
    definition_offs = tuple(image.va_to_off(va) for va in definition_vas)
    if (
        call_off is None
        or len(definition_vas) < 2
        or any(off is None for off in definition_offs)
    ):
        raise ExtractionError("multi register import evidence is unmapped")
    register_index = REG32.index(register)
    call_bytes = bytes((0xFF, 0xD0 | register_index))
    definition_bytes = (
        bytes((0x8B, 0x05 | (register_index << 3)))
        + struct.pack("<I", iat_va)
    )
    return (
        "exact_multi_register_iat_call@0x%08X file_off=0x%08X "
        "function=0x%08X register=%s definitions=%s "
        "definition_file_offs=%s iat=0x%08X call_bytes=%s "
        "definition_bytes=%s definition_count=%d iat_file_off=0x%08X "
        "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
        "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
        "dll=%s symbol=%s operation=%s wire_effect=unproved "
        "basis=complete_reaching_set_all_exact_same_iat_load"
        % (
            call_va,
            call_off,
            function_va,
            register,
            ",".join("0x%08X" % va for va in definition_vas),
            ",".join("0x%08X" % off for off in definition_offs),
            iat_va,
            call_bytes.hex().upper(),
            definition_bytes.hex().upper(),
            len(definition_vas),
            symbol.iat_off,
            symbol.descriptor_off,
            symbol.lookup_off,
            symbol.dll_name_off,
            symbol.symbol_name_off,
            symbol.dll,
            symbol.name,
            spec.tag,
        )
    )


def expr_contains_unknown(expr: Expr) -> bool:
    kind = expr[0]
    if kind == "unknown":
        return True
    if kind == "mem":
        return expr_contains_unknown(expr[1])
    if kind in ("add", "sub"):
        return expr_contains_unknown(expr[1]) or expr_contains_unknown(expr[2])
    if kind == "mul":
        return expr_contains_unknown(expr[1])
    if kind in ("and", "or", "shl", "shr", "sar"):
        return expr_contains_unknown(expr[1]) or expr_contains_unknown(expr[2])
    if kind in ("neg", "not"):
        return expr_contains_unknown(expr[1])
    if kind == "phi":
        return any(expr_contains_unknown(item) for item in expr[1])
    return False


def is_proven_vtable_slot_target(expr: Expr, slot: int) -> bool:
    """Accept only a dereferenced vtable slot pinned by the task."""
    if expr[0] != "mem":
        return False
    address = expr[1]
    if address[0] != "add":
        return False
    left, right = address[1], address[2]
    if right == ("const", slot) and left[0] == "mem":
        return True
    if left == ("const", slot) and right[0] == "mem":
        return True
    return False


def is_proven_serializer_vtable_target(expr: Expr) -> bool:
    """Accept only load [vtable+0x18], the slot pinned by the task."""
    return is_proven_vtable_slot_target(expr, 0x18)


class SerializerAnalyzer:
    """Conservative recursive serializer walker over the guarded image."""

    def __init__(self, image: Image, registry: list[RegistryRow]):
        self.image = image
        self.root_vas = frozenset(
            row.serializer_va for row in registry if row.serializer_va is not None
        )
        self.span_cache: dict[int, FunctionSpan | None] = {}
        self.decode_cache: dict[int, FunctionDecode | None] = {}
        self.gate_cache: dict[int, dict[int, str]] = {}
        self.capability_cache: dict[int, frozenset[str]] = {}
        self.local_capability_refinement_cache: dict[
            int, tuple[frozenset[str] | None, str]
        ] = {}
        self.stack_depth_cache: dict[
            int, dict[int, frozenset[int | None]]
        ] = {}
        self.stack_neutral_fragment_cache: dict[int, tuple[str, ...]] = {}
        self.stack_neutral_getid_fragment_cache: dict[
            int, tuple[str, ...]
        ] = {}
        self.stack_identity_fragment_cache: dict[int, tuple[str, ...]] = {}
        self.stack_formal_base_fragment_cache: dict[int, tuple[str, ...]] = {}
        self.mode_proof_cache: dict[
            tuple[int, str, int], tuple[ModeBranchProof, ...]
        ] = {}
        self.stream_seed_cache: dict[
            int, tuple[int | None, tuple[tuple[str, int], ...], str]
        ] = {}
        self.reaching_definition_cache: dict[
            tuple[int, str], dict[int, frozenset[int | None]]
        ] = {}
        self.byte_reaching_definition_cache: dict[
            tuple[int, str], dict[int, frozenset[int | None]]
        ] = {}
        self.formal_reaching_definitions: dict[
            tuple[int, int, str], int
        ] = {}
        self.formal_reaching_basis: dict[
            tuple[int, int, str], str
        ] = {}
        self._active_reaching_proof: set[tuple[int, int, str]] | None = None

    def span(self, va: int) -> FunctionSpan | None:
        if va not in self.span_cache:
            self.span_cache[va] = find_function_span(self.image, va)
        return self.span_cache[va]

    def decode(self, va: int) -> FunctionDecode | None:
        if va not in self.decode_cache:
            span = self.span(va)
            self.decode_cache[va] = (
                None if span is None else decode_function(self.image, span)
            )
        return self.decode_cache[va]

    def gates(self, va: int) -> dict[int, str]:
        if va not in self.gate_cache:
            decoded = self.decode(va)
            self.gate_cache[va] = {} if decoded is None else build_gate_map(decoded)
        return self.gate_cache[va]

    def capabilities(
        self,
        va: int,
        trail: frozenset[int] = frozenset(),
        depth: int = 0,
    ) -> frozenset[str]:
        if va == WRITE_VA:
            return frozenset(("W",))
        if va == READ_VA:
            return frozenset(("R",))
        if va in self.capability_cache:
            return self.capability_cache[va]
        if va in trail or depth >= 12:
            return frozenset()
        decoded = self.decode(va)
        if decoded is None:
            return frozenset()
        directions = set()
        next_trail = trail | {va}
        for ins in decoded.instructions.values():
            if ins.kind == "call" and ins.target in (WRITE_VA, READ_VA):
                directions.add("W" if ins.target == WRITE_VA else "R")
                continue
            if ins.kind == "call" and ins.target is not None:
                if (
                    recover_call_pushes(decoded, ins.va, 2)
                    or recover_call_pushes(decoded, ins.va, 1)
                ):
                    directions.update(
                        self.capabilities(ins.target, next_trail, depth + 1)
                    )
            elif (
                ins.kind == "jmp"
                and ins.target is not None
                and not (decoded.span.start_va <= ins.target < decoded.span.end_va)
            ):
                directions.update(
                    self.capabilities(ins.target, next_trail, depth + 1)
                )
        result = frozenset(sorted(directions))
        self.capability_cache[va] = result
        return result

    @staticmethod
    def _arg_expr(resolver: RegisterResolver, arg: PushArgument) -> Expr:
        return resolver.operand_before(
            arg.instruction_va,
            arg.operand,
            dereference=(arg.operand.kind == "mem"),
        )

    @classmethod
    def _mode_restriction(cls, expr: Expr) -> frozenset[str] | None:
        if expr == ("const", 1):
            return frozenset(("W",))
        if expr == ("const", 0):
            return frozenset(("R",))
        if expr and expr[0] == "phi":
            directions = set()
            for option in expr[1]:
                restricted = cls._mode_restriction(option)
                if restricted is None:
                    return None
                directions.update(restricted)
            return frozenset(directions)
        return None

    def _path_mode_directions(
        self,
        resolver: RegisterResolver,
        sequences: tuple[tuple[PushArgument, ...], ...],
    ) -> frozenset[str] | None:
        """Return only directions proved by every recovered mode argument path."""
        directions = set()
        for sequence in sequences:
            restricted = self._mode_restriction(
                self._arg_expr(resolver, sequence[0])
            )
            if restricted is None:
                return None
            directions.update(restricted)
        return frozenset(directions)

    def _normalize_expr(self, va: int, expr: Expr, context: Expr) -> Expr:
        return substitute_expr(expr, context, va)

    @staticmethod
    def _exact_empty(image: Image, span: FunctionSpan) -> bool:
        body = image.data[span.start_off : span.end_off]
        return body in (b"\xc3", b"\xc2\x08\x00")

    @staticmethod
    def _exact_constant_true_wire_empty(
        image: Image, span: FunctionSpan
    ) -> bool:
        body = image.data[span.start_off : span.end_off]
        return body == b"\xb0\x01\xc2\x04\x00"

    @staticmethod
    def _exact_global_predicate_wire_empty(
        image: Image, span: FunctionSpan
    ) -> bool:
        body = image.data[span.start_off : span.end_off]
        return body == b"\x83\x3d\xc4\x2e\x03\x01\x00\x0f\x95\xc0\xc2\x04\x00"

    @staticmethod
    def _exact_argument_value_copier_wire_empty(
        image: Image, span: FunctionSpan
    ) -> bool:
        body = image.data[span.start_off : span.end_off]
        return body == (
            b"\x8b\x44\x24\x04\x8b\x54\x24\x08\x89\x41\x18"
            b"\x89\x51\x1c\xc2\x08\x00"
        )

    @staticmethod
    def _exact_single_argument_value_copier_wire_empty(
        image: Image, span: FunctionSpan
    ) -> bool:
        body = image.data[span.start_off : span.end_off]
        return body == b"\x8b\x44\x24\x04\x89\x41\x14\xc2\x04\x00"

    @staticmethod
    def _exact_conditional_object_init_wire_empty(
        image: Image, span: FunctionSpan
    ) -> bool:
        body = image.data[span.start_off : span.end_off]
        return body == (
            b"\x33\xc0\x39\x05\xc4\x2e\x03\x01\x75\x05\x32\xc0"
            b"\xc2\x04\x00\x89\x41\x58\x89\x41\x5c\xb0\x01\xc2\x04\x00"
        )

    @staticmethod
    def _exact_fpstest_entry_wire_empty(
        image: Image, span: FunctionSpan
    ) -> bool:
        """Accept only the pinned FPSTest span whose entry CFG ends before CC CC.

        The span finder conservatively includes the distinct routine beginning at
        0x0073E900 because only two INT3 bytes separate it from the FPSTest entry.
        Full-span equality keeps that boundary fact fail-closed; the EMPTY claim
        itself is limited to instructions reachable from 0x0073E8B0.
        """
        body = image.data[span.start_off : span.end_off]
        return body == bytes.fromhex(
            "33D23915C42E0301750532C0C20400B00188411888411989511C568B35"
            "E0240201897120391554C60201751EBE02000000393558C602017C113935"
            "70C602017C0988511888411989511C5EC20400CCCC568BF18B4C24088B41"
            "1083F80A743583F80B7508C64619005EC2040083F84C75278B413050E826"
            "4BFEFF83C40485C074178BCEE8B8FEFFFF84C0750C33C088461889461CC6"
            "4619015EC20400"
        )

    def call_abi(
        self, decoded: FunctionDecode, call: Instruction, target_va: int
    ) -> tuple[str, int] | None:
        """Measure stack cleanup instead of inferring ABI from W/R capability."""
        target = self.decode(target_va)
        if target is None:
            return None
        cleanups = {
            ins.imm
            for ins in target.instructions.values()
            if ins.kind == "ret" and ins.imm is not None
        }
        if len(cleanups) == 1:
            cleanup = next(iter(cleanups))
            if cleanup in (4, 8, 12, 16):
                return ("thiscall", cleanup // 4)
        if cleanups == {0}:
            after = decoded.instructions.get(call.next_va)
            if (
                after is not None
                and after.kind == "add"
                and after.dst is not None
                and after.dst.kind == "reg"
                and base_reg_name(after.dst.reg) == "esp"
                and after.src is not None
                and after.src.kind == "imm"
                and after.src.imm in (4, 8, 12, 16)
            ):
                return ("cdecl", after.src.imm // 4)
        return None

    @staticmethod
    def _decoded_cleanup(decoded: FunctionDecode | None) -> int | None:
        if decoded is None:
            return None
        cleanups = {
            ins.imm
            for ins in decoded.instructions.values()
            if ins.kind == "ret" and ins.imm is not None
        }
        return next(iter(cleanups)) if len(cleanups) == 1 else None

    def _function_abi(
        self, decoded: FunctionDecode
    ) -> tuple[str, int] | None:
        cleanup = self._decoded_cleanup(decoded)
        if cleanup in (4, 8, 12, 16):
            return ("thiscall", cleanup // 4)
        return None

    @staticmethod
    def _stack_word_size(ins: Instruction) -> int:
        return 2 if has_operand16_prefix(ins.raw) else 4

    @staticmethod
    def _is_full_width_plain_mov(ins: Instruction) -> bool:
        """Accept only MOV r32,r/m32 or MOV r/m32,r32 opcodes.

        The compact decoder intentionally normalizes MOVZX/MOVSX as ``mov``;
        their narrow source must never seed a full-register formal or stack
        base proof.
        """
        opcode = next(
            (value for value in ins.raw if value not in PREFIX_BYTES), None
        )
        return (
            ins.kind == "mov"
            and opcode in (0x8B, 0x89)
            and not has_operand16_prefix(ins.raw)
        )

    @staticmethod
    def _is_full_width_identity_lea(ins: Instruction) -> bool:
        """Recognize only ``lea r32, [the_same_r32 + 0]``.

        This compiler padding idiom preserves all 32 bits.  Operand-size and
        address-size overrides, indexed forms, absolute addresses, partial
        registers, and nonzero displacements are deliberately excluded.
        """
        opcode = next(
            (value for value in ins.raw if value not in PREFIX_BYTES), None
        )
        return (
            ins.kind == "lea"
            and opcode == 0x8D
            and not has_operand16_prefix(ins.raw)
            and 0x67 not in ins.raw[: ins.raw.index(opcode)]
            and ins.dst is not None
            and ins.dst.kind == "reg"
            and ins.dst.reg not in REG8
            and ins.src is not None
            and ins.src.kind == "mem"
            and ins.src.base == base_reg_name(ins.dst.reg)
            and ins.src.index is None
            and ins.src.absolute is None
            and ins.src.disp == 0
        )

    @staticmethod
    def _is_full_width_zeroing_xor(
        ins: Instruction, reg: str
    ) -> bool:
        """Recognize only the exact two-byte ``xor r32,r32`` zero idiom."""
        return (
            ins.kind == "xor"
            and len(ins.raw) == 2
            and ins.raw[0] in (0x31, 0x33)
            and ins.dst is not None
            and ins.dst.kind == "reg"
            and ins.dst.reg == reg
            and ins.dst.reg not in REG8
            and ins.src is not None
            and ins.src.kind == "reg"
            and ins.src.reg == reg
            and ins.src.reg not in REG8
        )

    def _record_formal_reaching_proof(
        self,
        function_va: int,
        use_va: int,
        reg: str,
        definition_va: int,
        basis: str,
    ) -> None:
        key = (function_va, use_va, reg)
        previous_definition = self.formal_reaching_definitions.get(key)
        previous_basis = self.formal_reaching_basis.get(key)
        if previous_definition not in (None, definition_va) or previous_basis not in (
            None,
            basis,
        ):
            raise ExtractionError("conflicting formal reaching-proof identity")
        self.formal_reaching_definitions[key] = definition_va
        self.formal_reaching_basis[key] = basis
        if self._active_reaching_proof is not None:
            self._active_reaching_proof.add(key)

    @staticmethod
    def _other_has_no_gpr_write(ins: Instruction) -> bool:
        """Recognize the exact non-GPR-writing families left as ``other``.

        Everything else is an unknown GPR clobber for reaching-definition
        dataflow.  The narrow list covers comparisons, memory-only byte
        updates, x87 operations, NOP, and the specific SSE scalar/vector
        families whose destination is never an integer GPR.
        """
        if ins.kind != "other":
            return False
        raw = ins.raw
        opcode_index = next(
            (
                index
                for index, value in enumerate(raw)
                if value not in PREFIX_BYTES
            ),
            None,
        )
        if opcode_index is None:
            return False
        prefixes = frozenset(raw[:opcode_index])
        opcode = raw[opcode_index]
        if opcode in (0x39, 0x3B, 0x3C, 0x3D, 0x90):
            return True
        if 0xD8 <= opcode <= 0xDF:
            # FNSTSW AX (DF E0) is the one x87 encoding in this family that
            # writes an integer-register lane.  Treat it as an opaque GPR
            # clobber rather than allowing a stale full-EAX definition through.
            return not (
                opcode == 0xDF
                and opcode_index + 1 < len(raw)
                and raw[opcode_index + 1] == 0xE0
            )
        if opcode in (0x80, 0x82, 0xFF):
            if opcode_index + 1 >= len(raw):
                return False
            modrm = raw[opcode_index + 1]
            mod = modrm >> 6
            group = (modrm >> 3) & 7
            if opcode in (0x80, 0x82):
                return group == 7 or mod != 3
            return group in (0, 1) and mod != 3
        if opcode == 0x0F and opcode_index + 1 < len(raw):
            second = raw[opcode_index + 1]
            if second == 0x57:
                return True
            if 0xF3 in prefixes and second in (0x10, 0x11, 0x2A, 0x7E):
                return True
            if 0x66 in prefixes and second == 0xD6:
                return True
        return False

    def _stack_neutral_import(
        self, ins: Instruction
    ) -> ImportSymbol | None:
        if (
            ins.kind != "call_indirect"
            or ins.src is None
            or ins.src.kind != "mem"
            or ins.src.absolute is None
        ):
            return None
        symbol = self.image.imports_by_iat.get(ins.src.absolute)
        if symbol is None or (symbol.dll, symbol.name) not in STACK_NEUTRAL_IMPORTS:
            return None
        return symbol

    @staticmethod
    def _is_exact_register_indirect_call(
        ins: Instruction, reg: str
    ) -> bool:
        """Recognize only the unprefixed two-byte ``call r32`` encoding."""
        if reg not in REG32 or reg == "esp":
            return False
        register_index = REG32.index(reg)
        return (
            ins.kind == "call_indirect"
            and ins.src is not None
            and ins.src.kind == "reg"
            and ins.src.reg == reg
            and ins.raw == bytes((0xFF, 0xD0 | register_index))
        )

    @staticmethod
    def _is_exact_iat_register_load(
        ins: Instruction, reg: str, iat_va: int
    ) -> bool:
        """Recognize only unprefixed ``mov r32,[absolute IAT]`` bytes."""
        if reg not in REG32 or reg == "esp":
            return False
        register_index = REG32.index(reg)
        return (
            ins.kind == "mov"
            and ins.dst is not None
            and ins.dst.kind == "reg"
            and ins.dst.reg == reg
            and ins.src is not None
            and ins.src.kind == "mem"
            and ins.src.base is None
            and ins.src.index is None
            and ins.src.absolute == iat_va
            and ins.raw
            == bytes((0x8B, 0x05 | (register_index << 3)))
            + struct.pack("<I", iat_va)
        )

    def _stack_neutral_register_import(
        self, function_va: int, ins: Instruction
    ) -> tuple[ImportSymbol, str, int] | None:
        """Prove ``call r32`` reaches one exact allowlisted IAT load."""
        if (
            ins.src is None
            or ins.src.kind != "reg"
            or ins.src.reg is None
        ):
            return None
        reg = ins.src.reg
        if not self._is_exact_register_indirect_call(ins, reg):
            return None
        definitions = self._reaching_definitions(function_va, reg).get(
            ins.va, frozenset()
        )
        if len(definitions) != 1 or None in definitions:
            return None
        definition_va = next(iter(definitions))
        assert definition_va is not None
        decoded = self.decode(function_va)
        definition = (
            None
            if decoded is None
            else decoded.instructions.get(definition_va)
        )
        if (
            definition is None
            or definition.src is None
            or definition.src.kind != "mem"
            or definition.src.absolute is None
        ):
            return None
        symbol = self.image.imports_by_iat.get(definition.src.absolute)
        if (
            symbol is None
            or (symbol.dll, symbol.name) not in STACK_NEUTRAL_IMPORTS
            or not self._is_exact_iat_register_load(
                definition, reg, symbol.iat_va
            )
        ):
            return None
        return symbol, reg, definition_va

    def _all_same_register_import(
        self, function_va: int, ins: Instruction
    ) -> tuple[ImportSymbol, str, tuple[int, ...]] | None:
        """Prove every reaching definition is an exact same-IAT register load."""
        if (
            ins.src is None
            or ins.src.kind != "reg"
            or ins.src.reg is None
        ):
            return None
        reg = ins.src.reg
        if not self._is_exact_register_indirect_call(ins, reg):
            return None
        definitions = self._reaching_definitions(function_va, reg).get(
            ins.va, frozenset()
        )
        if len(definitions) < 2 or None in definitions:
            return None
        definition_vas = tuple(sorted(definitions))
        decoded = self.decode(function_va)
        if decoded is None:
            return None
        iat_vas = set()
        for definition_va in definition_vas:
            assert definition_va is not None
            definition = decoded.instructions.get(definition_va)
            if (
                definition is None
                or definition.src is None
                or definition.src.kind != "mem"
                or definition.src.absolute is None
                or not self._is_exact_iat_register_load(
                    definition, reg, definition.src.absolute
                )
            ):
                return None
            iat_vas.add(definition.src.absolute)
        if len(iat_vas) != 1:
            return None
        iat_va = next(iter(iat_vas))
        symbol = self.image.imports_by_iat.get(iat_va)
        if (
            symbol is None
            or (symbol.dll, symbol.name) not in STACK_NEUTRAL_IMPORTS
        ):
            return None
        return symbol, reg, definition_vas

    def _stack_neutral_import_for_function(
        self, function_va: int, ins: Instruction
    ) -> tuple[ImportSymbol, str | None, int | None] | None:
        direct = self._stack_neutral_import(ins)
        if direct is not None:
            return direct, None, None
        return self._stack_neutral_register_import(function_va, ins)

    @staticmethod
    def _is_exact_vtable_slot_register_load(
        ins: Instruction, dst_reg: str, slot: int
    ) -> bool:
        """Recognize exact unprefixed ``mov r32,[r32+disp8]`` bytes."""
        if (
            dst_reg not in REG32
            or dst_reg == "esp"
            or ins.dst is None
            or ins.dst.kind != "reg"
            or ins.dst.reg != dst_reg
            or ins.src is None
            or ins.src.kind != "mem"
            or ins.src.base not in REG32
            or ins.src.base == "esp"
            or ins.src.index is not None
            or ins.src.absolute is not None
            or ins.src.disp != slot
            or not (-0x80 <= slot <= 0x7F)
        ):
            return False
        dst_index = REG32.index(dst_reg)
        base_index = REG32.index(ins.src.base)
        return ins.raw == bytes(
            (0x8B, 0x40 | (dst_index << 3) | base_index, slot & 0xFF)
        )

    def _stack_neutral_vtable_getid(
        self, function_va: int, ins: Instruction
    ) -> tuple[str, int] | None:
        """Prove an adjacent exact call through the pinned GetId slot +0x10.

        The task pins vtable +0x10 as the no-argument GetId member.  This
        escape hatch additionally requires an unprefixed ``call r32``, one
        reaching definition, an adjacent exact ``mov r32,[r32+0x10]``, and
        the independently resolved symbolic vtable-slot expression.
        """
        if (
            ins.src is None
            or ins.src.kind != "reg"
            or ins.src.reg is None
        ):
            return None
        reg = ins.src.reg
        if not self._is_exact_register_indirect_call(ins, reg):
            return None
        definitions = self._reaching_definitions(function_va, reg).get(
            ins.va, frozenset()
        )
        if len(definitions) != 1 or None in definitions:
            return None
        definition_va = next(iter(definitions))
        assert definition_va is not None
        decoded = self.decode(function_va)
        if decoded is None:
            return None
        definition = decoded.instructions.get(definition_va)
        if (
            definition is None
            or definition.next_va != ins.va
            or not self._is_exact_vtable_slot_register_load(
                definition, reg, 0x10
            )
        ):
            return None
        target_expr = RegisterResolver(decoded).operand_before(
            ins.va, ins.src
        )
        if not is_proven_vtable_slot_target(target_expr, 0x10):
            return None
        return reg, definition_va

    def _stack_neutral_vtable_getid_fragments(
        self, va: int
    ) -> tuple[str, ...]:
        cached = self.stack_neutral_getid_fragment_cache.get(va)
        if cached is not None:
            return cached
        decoded = self.decode(va)
        if decoded is None:
            return ()
        fragments = []
        for ins in sorted(decoded.instructions.values(), key=lambda item: item.va):
            proof = self._stack_neutral_vtable_getid(va, ins)
            if proof is None:
                continue
            reg, definition_va = proof
            definition_off = self.image.va_to_off(definition_va)
            if definition_off is None:
                raise ExtractionError("GetId vtable definition is unmapped")
            fragments.append(
                "stack_neutral_vtable_getid@0x%08X file_off=0x%08X "
                "function=0x%08X register=%s definition@0x%08X "
                "definition_file_off=0x%08X slot=0x10 cleanup=0 "
                "basis=task_pinned_getid_slot_and_adjacent_exact_load"
                % (
                    ins.va,
                    ins.off,
                    va,
                    reg,
                    definition_va,
                    definition_off,
                )
            )
        result = tuple(fragments)
        self.stack_neutral_getid_fragment_cache[va] = result
        return result

    @staticmethod
    def _is_exact_stack_identity_lea(ins: Instruction) -> bool:
        """Recognize only this image's full-width ``lea esp,[esp+0]`` NOP."""
        return (
            ins.kind == "lea"
            and ins.raw == b"\x8D\xA4\x24\x00\x00\x00\x00"
            and ins.dst is not None
            and ins.dst.kind == "reg"
            and ins.dst.reg == "esp"
            and ins.src is not None
            and ins.src.kind == "mem"
            and ins.src.base == "esp"
            and ins.src.index is None
            and ins.src.absolute is None
            and ins.src.disp == 0
        )

    def _stack_identity_lea_fragments(self, va: int) -> tuple[str, ...]:
        cached = self.stack_identity_fragment_cache.get(va)
        if cached is not None:
            return cached
        decoded = self.decode(va)
        if decoded is None:
            return ()
        result = tuple(
            "stack_identity_lea@0x%08X file_off=0x%08X "
            "function=0x%08X register=esp displacement=0 "
            "basis=exact_full_width_stack_identity"
            % (ins.va, ins.off, va)
            for ins in sorted(
                decoded.instructions.values(), key=lambda item: item.va
            )
            if self._is_exact_stack_identity_lea(ins)
        )
        self.stack_identity_fragment_cache[va] = result
        return result

    def _stack_neutral_import_fragments(self, va: int) -> tuple[str, ...]:
        cached = self.stack_neutral_fragment_cache.get(va)
        if cached is not None:
            return cached
        decoded = self.decode(va)
        if decoded is None:
            return ()
        fragments = []
        for ins in sorted(decoded.instructions.values(), key=lambda item: item.va):
            proof = self._stack_neutral_import_for_function(va, ins)
            if proof is None:
                continue
            symbol, reg, definition_va = proof
            if reg is None:
                fragments.append(
                    "stack_neutral_import@0x%08X file_off=0x%08X "
                    "function=0x%08X iat=0x%08X iat_file_off=0x%08X "
                    "descriptor_file_off=0x%08X lookup_file_off=0x%08X "
                    "dll_name_file_off=0x%08X symbol_name_file_off=0x%08X "
                    "dll=%s symbol=%s cleanup=0"
                    % (
                        ins.va,
                        ins.off,
                        va,
                        symbol.iat_va,
                        symbol.iat_off,
                        symbol.descriptor_off,
                        symbol.lookup_off,
                        symbol.dll_name_off,
                        symbol.symbol_name_off,
                        symbol.dll,
                        symbol.name,
                    )
                )
                continue
            assert definition_va is not None
            definition_off = self.image.va_to_off(definition_va)
            if definition_off is None:
                raise ExtractionError(
                    "register IAT definition is unmapped"
                )
            fragments.append(
                "stack_neutral_register_import@0x%08X file_off=0x%08X "
                "function=0x%08X register=%s definition@0x%08X "
                "definition_file_off=0x%08X iat=0x%08X "
                "iat_file_off=0x%08X descriptor_file_off=0x%08X "
                "lookup_file_off=0x%08X dll_name_file_off=0x%08X "
                "symbol_name_file_off=0x%08X dll=%s symbol=%s cleanup=0 "
                "basis=singleton_reaching_exact_iat_load"
                % (
                    ins.va,
                    ins.off,
                    va,
                    reg,
                    definition_va,
                    definition_off,
                    symbol.iat_va,
                    symbol.iat_off,
                    symbol.descriptor_off,
                    symbol.lookup_off,
                    symbol.dll_name_off,
                    symbol.symbol_name_off,
                    symbol.dll,
                    symbol.name,
                )
            )
        result = tuple(fragments)
        self.stack_neutral_fragment_cache[va] = result
        return result

    def _stack_formal_base_fragments(self, va: int) -> tuple[str, ...]:
        """Record every exact ``mov reg, esp`` entry-stack seed in a function."""
        cached = self.stack_formal_base_fragment_cache.get(va)
        if cached is not None:
            return cached
        decoded = self.decode(va)
        if decoded is None:
            return ()
        depths = self._stack_depths(va)
        fragments = []
        for ins in sorted(decoded.instructions.values(), key=lambda item: item.va):
            if (
                not self._is_full_width_plain_mov(ins)
                or ins.dst is None
                or ins.dst.kind != "reg"
                or ins.dst.reg in REG8
                or base_reg_name(ins.dst.reg) == "esp"
                or ins.src is None
                or ins.src.kind != "reg"
                or base_reg_name(ins.src.reg) != "esp"
            ):
                continue
            site_depths = depths.get(ins.va, frozenset())
            if len(site_depths) != 1 or None in site_depths:
                continue
            depth = next(iter(site_depths))
            assert depth is not None
            delta = -depth
            delta_text = (
                "+0x%X" % delta if delta >= 0 else "-0x%X" % (-delta)
            )
            fragments.append(
                "stack_formal_base@0x%08X file_off=0x%08X "
                "function=0x%08X register=%s source=esp entry_delta=%s"
                % (
                    ins.va,
                    ins.off,
                    va,
                    base_reg_name(ins.dst.reg),
                    delta_text,
                )
            )
        result = tuple(fragments)
        self.stack_formal_base_fragment_cache[va] = result
        return result

    def _stack_after(
        self, function_va: int, depth: int | None, ins: Instruction
    ) -> int | None:
        if depth is None:
            return None
        if ins.kind == "push":
            return depth + self._stack_word_size(ins)
        if ins.kind == "pop":
            return depth - self._stack_word_size(ins)
        if (
            ins.kind in ("add", "sub")
            and ins.dst is not None
            and ins.dst.kind == "reg"
            and base_reg_name(ins.dst.reg) == "esp"
            and ins.src is not None
            and ins.src.kind == "imm"
        ):
            amount = ins.src.imm or 0
            return depth + amount if ins.kind == "sub" else depth - amount
        if self._is_exact_stack_identity_lea(ins):
            return depth
        if ins.kind == "call":
            cleanup = self._decoded_cleanup(self.decode(ins.target or 0))
            return None if cleanup is None else depth - cleanup
        if ins.kind == "call_indirect":
            return (
                depth
                if self._stack_neutral_import_for_function(
                    function_va, ins
                )
                is not None
                or self._stack_neutral_vtable_getid(function_va, ins)
                is not None
                else None
            )
        if (
            ins.dst is not None
            and ins.dst.kind == "reg"
            and base_reg_name(ins.dst.reg) == "esp"
        ):
            return None
        opcode = next(
            (value for value in ins.raw if value not in PREFIX_BYTES), None
        )
        if opcode in (0x60, 0x61, 0x9C, 0x9D, 0xC8, 0xC9):
            return None
        return depth

    def _stack_depths(
        self, va: int
    ) -> dict[int, frozenset[int | None]]:
        if va in self.stack_depth_cache:
            return self.stack_depth_cache[va]
        decoded = self.decode(va)
        if decoded is None:
            self.stack_depth_cache[va] = {}
            return {}
        values: dict[int, set[int | None]] = defaultdict(set)
        values[decoded.span.start_va].add(0)
        work = deque((decoded.span.start_va,))
        queued = {decoded.span.start_va}
        while work:
            site = work.popleft()
            queued.discard(site)
            ins = decoded.instructions[site]
            after_values = {
                self._stack_after(va, depth, ins) for depth in values[site]
            }
            for successor in decoded.successors.get(site, ()):
                if successor not in decoded.instructions:
                    continue
                current = values[successor]
                if None in current:
                    continue
                before = frozenset(current)
                current.update(after_values)
                if None in current or len(current) > 64:
                    current.clear()
                    current.add(None)
                if frozenset(current) != before and successor not in queued:
                    queued.add(successor)
                    work.append(successor)
        result = {site: frozenset(depths) for site, depths in values.items()}
        self.stack_depth_cache[va] = result
        return result

    @staticmethod
    def _writes_register(ins: Instruction, reg: str) -> bool:
        if ins.kind == "muldiv_wide" and reg in ("eax", "edx"):
            return True
        if ins.kind in ("call", "call_indirect") and reg in (
            "eax", "ecx", "edx"
        ):
            return True
        return bool(
            ins.dst is not None
            and ins.dst.kind == "reg"
            and base_reg_name(ins.dst.reg) == reg
            and ins.kind in (
                "lea", "mov", "add", "sub", "xor", "inc", "dec",
                "and", "or", "shl", "shr", "sar", "neg", "not",
                "unknown_write", "pop",
            )
        )

    def _writes_register_for_reaching(
        self, ins: Instruction, reg: str
    ) -> bool:
        return self._writes_register(ins, reg) or (
            ins.kind == "other"
            and not self._other_has_no_gpr_write(ins)
        )

    def _reaching_definitions(
        self, va: int, reg: str
    ) -> dict[int, frozenset[int | None]]:
        """Return all register definitions reaching each instruction entry.

        ``None`` is the undefined entry value.  A loop contributes only the
        definitions actually propagated through its CFG edges; the monotone
        union reaches a finite fixed point and never treats a back-edge as a
        proof failure by itself.
        """
        key = (va, reg)
        if key in self.reaching_definition_cache:
            return self.reaching_definition_cache[key]
        decoded = self.decode(va)
        if decoded is None:
            self.reaching_definition_cache[key] = {}
            return {}
        values: dict[int, set[int | None]] = {
            site: set() for site in decoded.instructions
        }
        entry = decoded.span.start_va
        values[entry].add(None)
        work = deque((entry,))
        queued = {entry}
        while work:
            site = work.popleft()
            queued.discard(site)
            ins = decoded.instructions[site]
            writes = self._writes_register_for_reaching(ins, reg)
            outgoing: set[int | None] = (
                {site} if writes else set(values[site])
            )
            for successor in decoded.successors.get(site, ()):
                if successor not in values:
                    continue
                current = values[successor]
                before = len(current)
                current.update(outgoing)
                if len(current) != before and successor not in queued:
                    queued.add(successor)
                    work.append(successor)
        result = {
            site: frozenset(definitions)
            for site, definitions in values.items()
        }
        self.reaching_definition_cache[key] = result
        return result

    @staticmethod
    def _writes_byte_lane(ins: Instruction, lane: str) -> bool:
        """Return whether an instruction overwrites this exact x86 byte lane.

        A full/16-bit write overlaps both byte lanes of the base register.  A
        byte write overlaps only its named low/high lane.  This deliberately
        does not treat a byte write as a definition of the full GPR.
        """
        base = base_reg_name(lane)
        if ins.kind == "muldiv_wide" and base in ("eax", "edx"):
            return True
        if ins.kind in ("call", "call_indirect") and base in (
            "eax", "ecx", "edx"
        ):
            return True
        if ins.kind not in (
            "lea", "mov", "add", "sub", "xor", "inc", "dec",
            "and", "or", "shl", "shr", "sar", "neg", "not",
            "unknown_write", "pop",
        ):
            return False
        if ins.dst is None or ins.dst.kind != "reg":
            return False
        if ins.dst.reg in REG8:
            return ins.dst.reg == lane
        return base_reg_name(ins.dst.reg) == base

    def _writes_byte_lane_for_reaching(
        self, ins: Instruction, lane: str
    ) -> bool:
        return self._writes_byte_lane(ins, lane) or (
            ins.kind == "other"
            and not self._other_has_no_gpr_write(ins)
        )

    def _byte_reaching_definitions(
        self, va: int, lane: str
    ) -> dict[int, frozenset[int | None]]:
        """Return definitions reaching one exact x86 byte lane.

        Full- and 16-bit writes kill both byte lanes of their base register;
        an 8-bit write kills only the named lane.  ``None`` remains the
        undefined entry value, and opaque ``other`` instructions are treated
        as clobbers unless their exact bytes are on the no-GPR-write allowlist.
        """
        key = (va, lane)
        if key in self.byte_reaching_definition_cache:
            return self.byte_reaching_definition_cache[key]
        decoded = self.decode(va)
        if decoded is None or lane not in REG8:
            self.byte_reaching_definition_cache[key] = {}
            return {}
        values: dict[int, set[int | None]] = {
            site: set() for site in decoded.instructions
        }
        entry = decoded.span.start_va
        values[entry].add(None)
        work = deque((entry,))
        queued = {entry}
        while work:
            site = work.popleft()
            queued.discard(site)
            ins = decoded.instructions[site]
            writes = self._writes_byte_lane_for_reaching(ins, lane)
            outgoing: set[int | None] = (
                {site} if writes else set(values[site])
            )
            for successor in decoded.successors.get(site, ()):
                if successor not in values:
                    continue
                current = values[successor]
                before = len(current)
                current.update(outgoing)
                if len(current) != before and successor not in queued:
                    queued.add(successor)
                    work.append(successor)
        result = {
            site: frozenset(definitions)
            for site, definitions in values.items()
        }
        self.byte_reaching_definition_cache[key] = result
        return result

    def _formal_offsets_for_byte_operand(
        self,
        decoded: FunctionDecode,
        depths: dict[int, frozenset[int | None]],
        at_va: int,
        operand: Operand,
        memo: dict[tuple[int, str], frozenset[int]],
        visiting: frozenset[tuple[int, str]],
    ) -> frozenset[int]:
        if operand.kind == "mem":
            return self._formal_offsets_for_operand(
                decoded, depths, at_va, operand, memo, visiting
            )
        if operand.kind != "reg":
            return frozenset()
        if operand.reg in REG8:
            lane = operand.reg
        else:
            lane = LOW8_BY_REG32.get(base_reg_name(operand.reg) or "")
        if lane is None:
            return frozenset()
        return self._formal_offsets_for_byte_reg(
            decoded, depths, at_va, lane, memo, visiting
        )

    def _formal_offsets_for_byte_reg(
        self,
        decoded: FunctionDecode,
        depths: dict[int, frozenset[int | None]],
        at_va: int,
        lane: str,
        memo: dict[tuple[int, str], frozenset[int]],
        visiting: frozenset[tuple[int, str]],
    ) -> frozenset[int]:
        key = (at_va, lane)
        if key in memo:
            return memo[key]
        if key in visiting:
            return frozenset()
        path_values = []
        next_visiting = visiting | {key}
        for predecessor in decoded.predecessors.get(at_va, ()):
            ins = decoded.instructions[predecessor]
            if self._writes_byte_lane_for_reaching(ins, lane):
                exact_byte_write = (
                    ins.dst is not None
                    and ins.dst.kind == "reg"
                    and ins.dst.reg == lane
                )
                low_lane_full_write = (
                    ins.dst is not None
                    and ins.dst.kind == "reg"
                    and ins.dst.reg not in REG8
                    and LOW8_BY_REG32.get(
                        base_reg_name(ins.dst.reg) or ""
                    ) == lane
                )
                if (
                    ins.kind == "mov"
                    and ins.src is not None
                    and (exact_byte_write or low_lane_full_write)
                ):
                    value = self._formal_offsets_for_byte_operand(
                        decoded,
                        depths,
                        ins.va,
                        ins.src,
                        memo,
                        next_visiting,
                    )
                else:
                    value = frozenset()
            else:
                value = self._formal_offsets_for_byte_reg(
                    decoded,
                    depths,
                    predecessor,
                    lane,
                    memo,
                    next_visiting,
                )
            path_values.append(value)
        if not path_values or any(not value for value in path_values):
            result = frozenset()
        else:
            union = frozenset().union(*path_values)
            result = union if len(union) == 1 else frozenset()
        if not result:
            function_va = decoded.span.start_va
            definitions = self._byte_reaching_definitions(
                function_va, lane
            ).get(at_va, frozenset())
            if len(definitions) == 1 and None not in definitions:
                definition_va = next(iter(definitions))
                definition = decoded.instructions[definition_va]
                destination_base = (
                    None
                    if definition.dst is None
                    or definition.dst.kind != "reg"
                    or definition.dst.reg in REG8
                    else base_reg_name(definition.dst.reg)
                )
                if (
                    self._is_full_width_plain_mov(definition)
                    and destination_base is not None
                    and LOW8_BY_REG32.get(destination_base) == lane
                    and definition.src is not None
                    and definition.src.kind == "mem"
                    and definition.src.base == "esp"
                    and definition.src.index is None
                    and definition.src.absolute is None
                ):
                    reaching_value = self._formal_offsets_for_operand(
                        decoded,
                        depths,
                        definition.va,
                        definition.src,
                        memo,
                        next_visiting,
                    )
                    if reaching_value:
                        result = reaching_value
                        self._record_formal_reaching_proof(
                            function_va,
                            at_va,
                            lane,
                            definition_va,
                            "unique_byte_lane_reaching_definition",
                        )
        memo[key] = result
        return result

    def _formal_offsets_for_operand(
        self,
        decoded: FunctionDecode,
        depths: dict[int, frozenset[int | None]],
        at_va: int,
        operand: Operand,
        memo: dict[tuple[int, str], frozenset[int]],
        visiting: frozenset[tuple[int, str]],
    ) -> frozenset[int]:
        if (
            operand.kind == "mem"
            and operand.base == "esp"
            and operand.index is None
            and operand.absolute is None
        ):
            at_depths = depths.get(at_va, frozenset())
            if len(at_depths) == 1 and None not in at_depths:
                depth = next(iter(at_depths))
                assert depth is not None
                return frozenset((operand.disp - depth,))
            return frozenset()
        if (
            operand.kind == "mem"
            and operand.base is not None
            and operand.base != "esp"
            and operand.index is None
            and operand.absolute is None
        ):
            bases = self._stack_base_offsets_for_reg(
                decoded,
                depths,
                at_va,
                operand.base,
                {},
                frozenset(),
            )
            if len(bases) == 1:
                return frozenset((next(iter(bases)) + operand.disp,))
            return frozenset()
        if operand.kind == "reg":
            if operand.reg in REG8:
                return self._formal_offsets_for_byte_reg(
                    decoded,
                    depths,
                    at_va,
                    operand.reg,
                    memo,
                    visiting,
                )
            return self._formal_offsets_for_reg(
                decoded,
                depths,
                at_va,
                base_reg_name(operand.reg) or "unknown",
                memo,
                visiting,
            )
        return frozenset()

    def _stack_base_offsets_for_reg(
        self,
        decoded: FunctionDecode,
        depths: dict[int, frozenset[int | None]],
        at_va: int,
        reg: str,
        memo: dict[tuple[int, str], frozenset[int]],
        visiting: frozenset[tuple[int, str]],
    ) -> frozenset[int]:
        """Trace an exact GPR copy of the entry stack pointer.

        The only seed is a full-width ``mov reg, esp`` at one measured stack
        depth.  Register copies may preserve that value; arithmetic, LEA,
        partial writes, conflicts, missing paths, and cycles fail closed.
        """
        key = (at_va, reg)
        if key in memo:
            return memo[key]
        if key in visiting:
            return frozenset()
        path_values = []
        next_visiting = visiting | {key}
        for predecessor in decoded.predecessors.get(at_va, ()):
            ins = decoded.instructions[predecessor]
            if self._writes_register(ins, reg):
                if (
                    self._is_full_width_plain_mov(ins)
                    and ins.src is not None
                    and ins.src.kind == "reg"
                    and ins.dst is not None
                    and ins.dst.kind == "reg"
                    and ins.dst.reg not in REG8
                ):
                    source = base_reg_name(ins.src.reg) or "unknown"
                    if source == "esp":
                        site_depths = depths.get(ins.va, frozenset())
                        if len(site_depths) == 1 and None not in site_depths:
                            depth = next(iter(site_depths))
                            assert depth is not None
                            value = frozenset((-depth,))
                        else:
                            value = frozenset()
                    else:
                        value = self._stack_base_offsets_for_reg(
                            decoded,
                            depths,
                            ins.va,
                            source,
                            memo,
                            next_visiting,
                        )
                else:
                    value = frozenset()
            else:
                value = self._stack_base_offsets_for_reg(
                    decoded,
                    depths,
                    predecessor,
                    reg,
                    memo,
                    next_visiting,
                )
            path_values.append(value)
        if not path_values or any(not value for value in path_values):
            result = frozenset()
        else:
            union = frozenset().union(*path_values)
            result = union if len(union) == 1 else frozenset()
        memo[key] = result
        return result

    def _formal_offsets_for_reg(
        self,
        decoded: FunctionDecode,
        depths: dict[int, frozenset[int | None]],
        at_va: int,
        reg: str,
        memo: dict[tuple[int, str], frozenset[int]],
        visiting: frozenset[tuple[int, str]],
    ) -> frozenset[int]:
        key = (at_va, reg)
        if key in memo:
            return memo[key]
        if key in visiting:
            return frozenset()
        path_values = []
        next_visiting = visiting | {key}
        for predecessor in decoded.predecessors.get(at_va, ()):
            ins = decoded.instructions[predecessor]
            if self._writes_register(ins, reg):
                if (
                    self._is_full_width_plain_mov(ins)
                    and ins.src is not None
                    and ins.dst is not None
                    and ins.dst.reg not in REG8
                ):
                    value = self._formal_offsets_for_operand(
                        decoded,
                        depths,
                        ins.va,
                        ins.src,
                        memo,
                        next_visiting,
                    )
                elif self._is_full_width_identity_lea(ins):
                    value = self._formal_offsets_for_reg(
                        decoded,
                        depths,
                        ins.va,
                        reg,
                        memo,
                        next_visiting,
                    )
                    if value:
                        self._record_formal_reaching_proof(
                            decoded.span.start_va,
                            ins.next_va,
                            reg,
                            ins.va,
                            "full_width_identity_lea",
                        )
                else:
                    value = frozenset()
            else:
                value = self._formal_offsets_for_reg(
                    decoded,
                    depths,
                    predecessor,
                    reg,
                    memo,
                    next_visiting,
                )
            path_values.append(value)
        if not path_values or any(not value for value in path_values):
            result = frozenset()
        else:
            union = frozenset().union(*path_values)
            result = union if len(union) == 1 else frozenset()
        if not result:
            function_va = decoded.span.start_va
            definitions = self._reaching_definitions(
                function_va, reg
            ).get(at_va, frozenset())
            if len(definitions) == 1 and None not in definitions:
                definition_va = next(iter(definitions))
                definition = decoded.instructions[definition_va]
                if (
                    (
                        self._is_full_width_plain_mov(definition)
                        or self._is_full_width_identity_lea(definition)
                    )
                    and definition.dst is not None
                    and definition.dst.kind == "reg"
                    and base_reg_name(definition.dst.reg) == reg
                    and definition.dst.reg not in REG8
                    and definition.src is not None
                ):
                    if self._is_full_width_identity_lea(definition):
                        reaching_value = self._formal_offsets_for_reg(
                            decoded,
                            depths,
                            definition.va,
                            reg,
                            memo,
                            next_visiting,
                        )
                        proof_use_va = definition.next_va
                        proof_basis = "full_width_identity_lea"
                    else:
                        reaching_value = self._formal_offsets_for_operand(
                            decoded,
                            depths,
                            definition.va,
                            definition.src,
                            memo,
                            next_visiting,
                        )
                        proof_use_va = at_va
                        proof_basis = "unique_reaching_definition"
                    if reaching_value:
                        result = reaching_value
                        self._record_formal_reaching_proof(
                            function_va,
                            proof_use_va,
                            reg,
                            definition_va,
                            proof_basis,
                        )
        memo[key] = result
        return result

    def _formal_offsets(
        self, va: int, at_va: int, operand: Operand
    ) -> frozenset[int]:
        decoded = self.decode(va)
        if decoded is None:
            return frozenset()
        return self._formal_offsets_for_operand(
            decoded,
            self._stack_depths(va),
            at_va,
            operand,
            {},
            frozenset(),
        )

    def _formal_offsets_with_reaching_proof(
        self, va: int, at_va: int, operand: Operand
    ) -> tuple[frozenset[int], tuple[tuple[int, int, str], ...]]:
        parent = self._active_reaching_proof
        collected: set[tuple[int, int, str]] = set()
        self._active_reaching_proof = collected
        try:
            origins = self._formal_offsets(va, at_va, operand)
        finally:
            self._active_reaching_proof = parent
        if parent is not None:
            parent.update(collected)
        return origins, tuple(sorted(collected))

    def _formal_reaching_fragments(
        self,
        formal_offset: int,
        proof_keys: tuple[tuple[int, int, str], ...],
    ) -> tuple[str, ...]:
        fragments = []
        for function_va, use_va, reg in proof_keys:
            key = (function_va, use_va, reg)
            definition_va = self.formal_reaching_definitions.get(key)
            basis = self.formal_reaching_basis.get(key)
            definition_off = (
                None
                if definition_va is None
                else self.image.va_to_off(definition_va)
            )
            use_off = self.image.va_to_off(use_va)
            if definition_va is None or definition_off is None or use_off is None:
                raise ExtractionError(
                    "formal reaching-definition evidence is unmapped"
                )
            if basis == "unique_reaching_definition":
                fragments.append(
                    "formal_reaching_def@0x%08X file_off=0x%08X "
                    "function=0x%08X register=%s use@0x%08X "
                    "file_off=0x%08X formal=entry+0x%X "
                    "basis=unique_reaching_definition"
                    % (
                        definition_va,
                        definition_off,
                        function_va,
                        reg,
                        use_va,
                        use_off,
                        formal_offset,
                    )
                )
            elif basis == "unique_byte_lane_reaching_definition":
                fragments.append(
                    "formal_byte_reaching_def@0x%08X file_off=0x%08X "
                    "function=0x%08X lane=%s use@0x%08X "
                    "file_off=0x%08X formal=entry+0x%X "
                    "definition_width=32 consumed_width=8 "
                    "source=stack_formal "
                    "basis=unique_byte_lane_reaching_definition"
                    % (
                        definition_va,
                        definition_off,
                        function_va,
                        reg,
                        use_va,
                        use_off,
                        formal_offset,
                    )
                )
            elif basis == "full_width_identity_lea":
                fragments.append(
                    "formal_identity_lea@0x%08X file_off=0x%08X "
                    "function=0x%08X register=%s continuation@0x%08X "
                    "file_off=0x%08X formal=entry+0x%X "
                    "basis=full_width_zero_displacement"
                    % (
                        definition_va,
                        definition_off,
                        function_va,
                        reg,
                        use_va,
                        use_off,
                        formal_offset,
                    )
                )
            else:
                raise ExtractionError("formal reaching-proof basis is missing")
        return tuple(fragments)

    def _formal_reaching_evidence_keys(
        self,
        formal_offset: int,
        proof_keys: tuple[tuple[int, int, str], ...],
    ) -> set[tuple[str, int, int, str, int, int]]:
        result = set()
        for function_va, use_va, reg in proof_keys:
            key = (function_va, use_va, reg)
            definition_va = self.formal_reaching_definitions.get(key)
            basis = self.formal_reaching_basis.get(key)
            if definition_va is None or basis is None:
                raise ExtractionError(
                    "formal reaching-definition key lacks a definition"
                )
            result.add(
                (
                    basis,
                    function_va,
                    use_va,
                    reg,
                    definition_va,
                    formal_offset,
                )
            )
        return result

    def _formal_reaching_fragments_for_operand(
        self,
        va: int,
        at_va: int,
        operand: Operand,
        formal_offset: int,
    ) -> tuple[str, ...]:
        origins, proof_keys = self._formal_offsets_with_reaching_proof(
            va, at_va, operand
        )
        if origins != frozenset((formal_offset,)):
            return ()
        return self._formal_reaching_fragments(formal_offset, proof_keys)

    def _mode_argument_formal_offsets(
        self, va: int, at_va: int, operand: Operand, width: int
    ) -> frozenset[int]:
        """Trace the bytes a target mode predicate will actually consume."""
        decoded = self.decode(va)
        if decoded is None:
            return frozenset()
        if width == 1 and operand.kind == "reg":
            lane = (
                operand.reg
                if operand.reg in REG8
                else LOW8_BY_REG32.get(base_reg_name(operand.reg) or "")
            )
            if lane is not None:
                proof_snapshot = (
                    None
                    if self._active_reaching_proof is None
                    else set(self._active_reaching_proof)
                )
                lane_offsets = self._formal_offsets_for_byte_reg(
                    decoded,
                    self._stack_depths(va),
                    at_va,
                    lane,
                    {},
                    frozenset(),
                )
                if lane_offsets or operand.reg in REG8:
                    return lane_offsets
                if proof_snapshot is not None:
                    assert self._active_reaching_proof is not None
                    self._active_reaching_proof.clear()
                    self._active_reaching_proof.update(proof_snapshot)
                # A proof for the whole r32 is stricter than a proof for its
                # consumed low byte.  This fallback preserves exact full-GPR
                # identity-LEA evidence when lane recursion stops at a loop;
                # partial or otherwise unmodelled writes still fail closed in
                # the full-register tracer.
                if operand.reg in REG32:
                    return self._formal_offsets(va, at_va, operand)
                return frozenset()
        return self._formal_offsets(va, at_va, operand)

    def _mode_argument_formal_offsets_with_reaching_proof(
        self, va: int, at_va: int, operand: Operand, width: int
    ) -> tuple[frozenset[int], tuple[tuple[int, int, str], ...]]:
        parent = self._active_reaching_proof
        collected: set[tuple[int, int, str]] = set()
        self._active_reaching_proof = collected
        try:
            origins = self._mode_argument_formal_offsets(
                va, at_va, operand, width
            )
        finally:
            self._active_reaching_proof = parent
        if parent is not None:
            parent.update(collected)
        return origins, tuple(sorted(collected))

    def _mode_argument_zero_reaching_definition(
        self, va: int, at_va: int, operand: Operand, width: int
    ) -> tuple[str, int] | None:
        """Prove a consumed low byte is zero from one reaching XOR-self.

        For EAX/ECX/EDX/EBX the dataflow is lane-specific.  Registers without
        an addressable low-byte name use the stricter full-GPR dataflow.  No
        multi-definition value meet is attempted even when every definition
        happens to look like a zero idiom.
        """
        proof = self._mode_argument_all_zero_reaching_definitions(
            va, at_va, operand, width
        )
        if proof is None or len(proof[1]) != 1:
            return None
        return proof[0], proof[1][0]

    def _mode_argument_all_zero_reaching_definitions(
        self, va: int, at_va: int, operand: Operand, width: int
    ) -> tuple[str, tuple[int, ...]] | None:
        """Prove every definition reaching a consumed byte is XOR-self zero.

        Undefined entry paths are rejected.  Every member of a multi-site set
        must independently be the exact full-width, two-byte XOR-self idiom
        for the same pushed r32; no generic constant/value lattice is used.
        """
        if (
            width != 1
            or operand.kind != "reg"
            or operand.reg not in REG32
            or operand.reg == "esp"
        ):
            return None
        reg = operand.reg
        lane = LOW8_BY_REG32.get(reg)
        definitions = (
            self._byte_reaching_definitions(va, lane)
            if lane is not None
            else self._reaching_definitions(va, reg)
        ).get(at_va, frozenset())
        if not definitions or None in definitions:
            return None
        decoded = self.decode(va)
        ordered = tuple(sorted(
            definition_va
            for definition_va in definitions
            if definition_va is not None
        ))
        if decoded is None or any(
            definition_va not in decoded.instructions
            or not self._is_full_width_zeroing_xor(
                decoded.instructions[definition_va], reg
            )
            for definition_va in ordered
        ):
            return None
        return reg, ordered

    def _mode_argument_zero_through_identity_lea(
        self, va: int, at_va: int, operand: Operand, width: int
    ) -> tuple[str, int, tuple[int, ...]] | None:
        """Prove zero through exactly one full-width identity LEA.

        The definition reaching the consumed byte must be the sole exact
        ``lea r32,[the_same_r32+0]`` site.  Its own complete reaching set must
        contain no undefined path and every member must be exact full-width
        XOR-self zero for that same register.  Chains of identity operations
        and generic value propagation remain outside this escape hatch.
        """
        if (
            width != 1
            or operand.kind != "reg"
            or operand.reg not in REG32
            or operand.reg == "esp"
        ):
            return None
        reg = operand.reg
        lane = LOW8_BY_REG32.get(reg)
        table = (
            self._byte_reaching_definitions(va, lane)
            if lane is not None
            else self._reaching_definitions(va, reg)
        )
        definitions = table.get(at_va, frozenset())
        if len(definitions) != 1 or None in definitions:
            return None
        identity_va = next(iter(definitions))
        decoded = self.decode(va)
        if (
            decoded is None
            or identity_va not in decoded.instructions
            or not self._is_full_width_identity_lea(
                decoded.instructions[identity_va]
            )
            or decoded.instructions[identity_va].dst is None
            or base_reg_name(
                decoded.instructions[identity_va].dst.reg or ""
            )
            != reg
        ):
            return None
        predecessors = table.get(identity_va, frozenset())
        if not predecessors or None in predecessors:
            return None
        ordered = tuple(sorted(
            predecessor_va
            for predecessor_va in predecessors
            if predecessor_va is not None
        ))
        if any(
            predecessor_va not in decoded.instructions
            or not self._is_full_width_zeroing_xor(
                decoded.instructions[predecessor_va], reg
            )
            for predecessor_va in ordered
        ):
            return None
        return reg, identity_va, ordered

    def _mode_zero_reaching_fragment(
        self,
        function_va: int,
        argument: PushArgument,
        reg: str,
        definition_va: int,
    ) -> str | None:
        definition_off = self.image.va_to_off(definition_va)
        argument_off = self.image.va_to_off(argument.instruction_va)
        if definition_off is None or argument_off is None:
            return None
        return (
            "mode_zero_reaching_def@0x%08X file_off=0x%08X "
            "function=0x%08X register=%s use@0x%08X "
            "file_off=0x%08X consumed_width=1 value=zero "
            "basis=unique_full_width_xor_self "
            "mode_arg@0x%08X file_off=0x%08X value=zero"
            % (
                definition_va,
                definition_off,
                function_va,
                reg,
                argument.instruction_va,
                argument_off,
                argument.instruction_va,
                argument_off,
            )
        )

    def _mode_zero_reaching_set_fragment(
        self,
        function_va: int,
        argument: PushArgument,
        reg: str,
        definition_vas: tuple[int, ...],
    ) -> str | None:
        argument_off = self.image.va_to_off(argument.instruction_va)
        definitions = []
        for definition_va in definition_vas:
            definition_off = self.image.va_to_off(definition_va)
            if definition_off is None:
                return None
            definitions.append(
                "definition@0x%08X file_off=0x%08X"
                % (definition_va, definition_off)
            )
        if argument_off is None or len(definitions) < 2:
            return None
        return (
            "mode_zero_reaching_set function=0x%08X register=%s "
            "use@0x%08X file_off=0x%08X consumed_width=1 value=zero "
            "definition_count=%d definitions=(%s) "
            "basis=all_reaching_full_width_xor_self "
            "mode_arg@0x%08X file_off=0x%08X value=zero"
            % (
                function_va,
                reg,
                argument.instruction_va,
                argument_off,
                len(definitions),
                ",".join(definitions),
                argument.instruction_va,
                argument_off,
            )
        )

    def _mode_zero_identity_lea_fragment(
        self,
        function_va: int,
        argument: PushArgument,
        reg: str,
        identity_va: int,
        definition_vas: tuple[int, ...],
    ) -> str | None:
        argument_off = self.image.va_to_off(argument.instruction_va)
        identity_off = self.image.va_to_off(identity_va)
        definitions = []
        for definition_va in definition_vas:
            definition_off = self.image.va_to_off(definition_va)
            if definition_off is None:
                return None
            definitions.append(
                "definition@0x%08X file_off=0x%08X"
                % (definition_va, definition_off)
            )
        if argument_off is None or identity_off is None or not definitions:
            return None
        return (
            "mode_zero_identity_lea function=0x%08X register=%s "
            "use@0x%08X file_off=0x%08X consumed_width=1 value=zero "
            "identity@0x%08X file_off=0x%08X definition_count=%d "
            "definitions=(%s) "
            "basis=all_reaching_full_width_xor_self_through_exact_"
            "full_width_identity_lea "
            "mode_arg@0x%08X file_off=0x%08X value=zero"
            % (
                function_va,
                reg,
                argument.instruction_va,
                argument_off,
                identity_va,
                identity_off,
                len(definitions),
                ",".join(definitions),
                argument.instruction_va,
                argument_off,
            )
        )

    def _direct_stream_anchors(
        self,
        va: int,
        formal_offset: int,
        directions: frozenset[str] = frozenset(("W", "R")),
    ) -> tuple[tuple[str, int], ...]:
        """Return direct primitives whose ECX is exactly one target formal."""
        decoded = self.decode(va)
        if decoded is None:
            return ()
        expected = frozenset((formal_offset,))
        anchors = []
        for ins in sorted(decoded.instructions.values(), key=lambda item: item.va):
            if ins.kind != "call" or ins.target not in (WRITE_VA, READ_VA):
                continue
            direction = "W" if ins.target == WRITE_VA else "R"
            if direction not in directions:
                continue
            origins = self._formal_offsets(
                va, ins.va, Operand("reg", reg="ecx")
            )
            if origins == expected:
                anchors.append((direction, ins.va))
        return tuple(anchors)

    def _stream_formal_seed(
        self, va: int
    ) -> tuple[int | None, tuple[tuple[str, int], ...], str]:
        """Seed a caller stream only from singleton direct primitive ECX origins.

        Unresolved direct primitives are ignored, but two different singleton
        formals conflict.  Thus one exact anchor is sufficient evidence while a
        measured contradiction fails closed.
        """
        if va in self.stream_seed_cache:
            return self.stream_seed_cache[va]
        decoded = self.decode(va)
        if decoded is None:
            result = (None, (), "caller_stream_function_decode_failed")
            self.stream_seed_cache[va] = result
            return result
        observed: list[tuple[str, int, int]] = []
        for ins in sorted(decoded.instructions.values(), key=lambda item: item.va):
            if ins.kind != "call" or ins.target not in (WRITE_VA, READ_VA):
                continue
            origins = self._formal_offsets(
                va, ins.va, Operand("reg", reg="ecx")
            )
            if len(origins) != 1:
                continue
            direction = "W" if ins.target == WRITE_VA else "R"
            observed.append((direction, ins.va, next(iter(origins))))
        formals = {formal for _direction, _site, formal in observed}
        if not observed:
            result = (None, (), "caller_stream_seed_absent")
        elif len(formals) != 1:
            result = (None, (), "caller_stream_seed_conflict")
        else:
            formal = next(iter(formals))
            anchors = tuple(
                (direction, site)
                for direction, site, value in observed
                if value == formal
            )
            result = (formal, anchors, "")
        self.stream_seed_cache[va] = result
        return result

    def _stream_anchor_fragment(
        self,
        role: str,
        function_va: int,
        direction: str,
        site_va: int,
        formal_label: str,
        formal_offset: int,
    ) -> str:
        off = self.image.va_to_off(site_va)
        primitive = WRITE_VA if direction == "W" else READ_VA
        if off is None:
            raise ExtractionError("stream anchor file offset is unmapped")
        anchor = (
            "%s_stream_anchor_%s@0x%08X file_off=0x%08X "
            "function=0x%08X primitive=0x%08X %s=entry+0x%X"
            % (
                role,
                direction,
                site_va,
                off,
                function_va,
                primitive,
                formal_label,
                formal_offset,
            )
        )
        origins, proof_keys = self._formal_offsets_with_reaching_proof(
            function_va, site_va, Operand("reg", reg="ecx")
        )
        if origins != frozenset((formal_offset,)):
            raise ExtractionError("stream anchor formal proof changed")
        fragments = self._formal_reaching_fragments(
            formal_offset, proof_keys
        )
        return " AND ".join((anchor, *fragments))

    def _stream_formal_discovery_fragment(
        self,
        site_va: int,
        caller_va: int,
        target_va: int,
        caller_formal: int,
        target_formal: int,
        directions: frozenset[str],
    ) -> str:
        off = self.image.va_to_off(site_va)
        if off is None:
            raise ExtractionError("stream formal discovery offset is unmapped")
        return (
            "stream_formal_discovery@0x%08X file_off=0x%08X "
            "caller=0x%08X target=0x%08X caller_formal=entry+0x%X "
            "target_formal=entry+0x%X directions=%s "
            "basis=directional_target_primitive"
            % (
                site_va,
                off,
                caller_va,
                target_va,
                caller_formal,
                target_formal,
                ",".join(sorted(directions)),
            )
        )

    def _discover_direct_stream_formals(
        self,
        caller_va: int,
        call: Instruction,
        abi: tuple[str, int],
        sequences: tuple[tuple[PushArgument, ...], ...],
        directions: frozenset[str],
        allow_nested_target: bool = True,
    ) -> tuple[
        tuple[
            int,
            int,
            tuple[PushArgument, ...],
            tuple[tuple[str, int, str], ...],
        ],
        ...,
    ]:
        """Map a target formal back to one caller formal without a caller seed.

        A candidate exists only when every recovered call path forwards the
        same singleton caller formal and the target formal has a direct ECX
        primitive anchor for every locally feasible direction.
        """
        if call.target is None or not sequences or not directions:
            return ()
        _abi_kind, argument_count = abi
        candidates = []
        for target_formal in range(4, argument_count * 4 + 1, 4):
            source_index = argument_count - (target_formal // 4)
            if not (0 <= source_index < argument_count):
                continue
            selected = tuple(sequence[source_index] for sequence in sequences)
            origins = tuple(
                self._formal_offsets(
                    caller_va, argument.instruction_va, argument.operand
                )
                for argument in selected
            )
            if not origins or any(len(origin) != 1 for origin in origins):
                continue
            caller_formals = {next(iter(origin)) for origin in origins}
            if len(caller_formals) != 1:
                continue
            target_anchors = []
            for direction in sorted(directions):
                matches = self._target_stream_anchors(
                    call.target,
                    target_formal,
                    direction,
                    allow_nested_target,
                )
                if not matches:
                    break
                target_anchors.append(matches[0])
            else:
                candidates.append(
                    (
                        next(iter(caller_formals)),
                        target_formal,
                        selected,
                        tuple(target_anchors),
                    )
                )
        return tuple(candidates)

    def _discover_tail_stream_formals(
        self,
        caller_va: int,
        jump: Instruction,
        directions: frozenset[str],
    ) -> tuple[tuple[int, tuple[tuple[str, int], ...]], ...]:
        """Discover an entry-formal preserved by a zero-depth tail jump."""
        if jump.target is None or not directions:
            return ()
        if self._stack_depths(caller_va).get(jump.va) != frozenset((0,)):
            return ()
        target = self.decode(jump.target)
        if target is None:
            return ()
        abi = self._function_abi(target)
        if abi is None:
            return ()
        _abi_kind, argument_count = abi
        candidates = []
        for target_formal in range(4, argument_count * 4 + 1, 4):
            target_anchors = []
            for direction in sorted(directions):
                matches = self._direct_stream_anchors(
                    jump.target,
                    target_formal,
                    frozenset((direction,)),
                )
                if not matches:
                    break
                target_anchors.append(matches[0])
            else:
                candidates.append((target_formal, tuple(target_anchors)))
        return tuple(candidates)

    def _prove_direct_subcall_stream(
        self,
        caller_va: int,
        inherited_stream_formal: int | None,
        call: Instruction,
        abi: tuple[str, int],
        sequences: tuple[tuple[PushArgument, ...], ...],
        directions: frozenset[str],
        allow_nested_target: bool = True,
    ) -> tuple[int | None, str, str]:
        caller_formal = inherited_stream_formal
        seed_anchors: tuple[tuple[str, int], ...] = ()
        discovered = False
        target_formal: int | None = None
        selected_arguments: tuple[PushArgument, ...] = ()
        target_anchors: tuple[tuple[str, int, str], ...] = ()
        if caller_formal is None:
            caller_formal, seed_anchors, seed_reason = (
                self._stream_formal_seed(caller_va)
            )
            if caller_formal is None:
                if seed_reason != "caller_stream_seed_absent":
                    return None, "", seed_reason
                discovered_candidates = self._discover_direct_stream_formals(
                    caller_va,
                    call,
                    abi,
                    sequences,
                    directions,
                    allow_nested_target,
                )
                if not discovered_candidates:
                    return None, "", "stream_formal_discovery_absent"
                if len(discovered_candidates) != 1:
                    return None, "", "stream_formal_discovery_ambiguous"
                (
                    caller_formal,
                    target_formal,
                    selected_arguments,
                    target_anchors,
                ) = discovered_candidates[0]
                discovered = True
        else:
            seed_anchors = self._direct_stream_anchors(
                caller_va, caller_formal
            )

        _abi_kind, argument_count = abi
        if not discovered:
            candidates: list[tuple[int, tuple[PushArgument, ...]]] = []
            for candidate_formal in range(4, argument_count * 4 + 1, 4):
                source_index = argument_count - (candidate_formal // 4)
                selected = tuple(
                    sequence[source_index] for sequence in sequences
                )
                if all(
                    self._formal_offsets(
                        caller_va, argument.instruction_va, argument.operand
                    )
                    == frozenset((caller_formal,))
                    for argument in selected
                ):
                    candidates.append((candidate_formal, selected))
            if not candidates:
                return None, "", "stream_argument_origin_unproved"
            if len(candidates) != 1:
                return None, "", "stream_argument_origin_ambiguous"
            target_formal, selected_arguments = candidates[0]

            measured_target_anchors = []
            for direction in sorted(directions):
                matches = self._target_stream_anchors(
                    call.target or 0,
                    target_formal,
                    direction,
                    allow_nested_target,
                )
                if not matches:
                    return (
                        None,
                        "",
                        "target_stream_%s_anchor_absent" % direction,
                    )
                measured_target_anchors.append(matches[0])
            target_anchors = tuple(measured_target_anchors)

        call_off = self.image.va_to_off(call.va)
        if call_off is None or call.target is None or target_formal is None:
            return None, "", "stream_call_offset_or_target_unmapped"
        proof = []
        if seed_anchors:
            direction, site = sorted(seed_anchors, key=lambda item: item[1])[0]
            proof.append(
                self._stream_anchor_fragment(
                    "caller",
                    caller_va,
                    direction,
                    site,
                    "caller_formal",
                    caller_formal,
                )
            )
        proof.extend(self._stack_neutral_import_fragments(caller_va))
        proof.extend(self._stack_neutral_vtable_getid_fragments(caller_va))
        proof.extend(self._stack_identity_lea_fragments(caller_va))
        proof.extend(self._stack_formal_base_fragments(caller_va))
        if discovered:
            proof.append(
                self._stream_formal_discovery_fragment(
                    call.va,
                    caller_va,
                    call.target,
                    caller_formal,
                    target_formal,
                    directions,
                )
            )
        proof.append(
            "stream_call@0x%08X file_off=0x%08X caller=0x%08X "
            "target=0x%08X caller_formal=entry+0x%X "
            "target_formal=entry+0x%X"
            % (
                call.va,
                call_off,
                caller_va,
                call.target,
                caller_formal,
                target_formal,
            )
        )
        for argument in sorted(
            set(selected_arguments), key=lambda item: item.instruction_va
        ):
            argument_off = self.image.va_to_off(argument.instruction_va)
            if argument_off is None:
                return None, "", "stream_argument_offset_unmapped"
            proof.append(
                "stream_arg@0x%08X file_off=0x%08X caller=0x%08X "
                "call=0x%08X target=0x%08X caller_formal=entry+0x%X "
                "target_formal=entry+0x%X"
                % (
                    argument.instruction_va,
                    argument_off,
                    caller_va,
                    call.va,
                    call.target,
                    caller_formal,
                    target_formal,
                )
            )
            proof.extend(
                self._formal_reaching_fragments_for_operand(
                    caller_va,
                    argument.instruction_va,
                    argument.operand,
                    caller_formal,
                )
            )
        for direction, site, nested_evidence in target_anchors:
            if nested_evidence:
                proof.append(nested_evidence)
            else:
                proof.append(
                    self._stream_anchor_fragment(
                        "target",
                        call.target,
                        direction,
                        site,
                        "target_formal",
                        target_formal,
                    )
                )
        proof.extend(self._stack_neutral_import_fragments(call.target))
        proof.extend(self._stack_neutral_vtable_getid_fragments(call.target))
        proof.extend(self._stack_identity_lea_fragments(call.target))
        proof.extend(self._stack_formal_base_fragments(call.target))
        return target_formal, " AND ".join(dict.fromkeys(proof)), ""

    def _prove_tail_subcall_stream(
        self,
        caller_va: int,
        inherited_stream_formal: int | None,
        jump: Instruction,
        directions: frozenset[str],
    ) -> tuple[int | None, str, str]:
        caller_formal = inherited_stream_formal
        seed_anchors: tuple[tuple[str, int], ...] = ()
        discovered = False
        target_formal: int | None = None
        target_anchors: tuple[tuple[str, int], ...] = ()
        if caller_formal is None:
            caller_formal, seed_anchors, seed_reason = (
                self._stream_formal_seed(caller_va)
            )
            if caller_formal is None:
                if seed_reason != "caller_stream_seed_absent":
                    return None, "", seed_reason
                discovered_candidates = self._discover_tail_stream_formals(
                    caller_va,
                    jump,
                    directions,
                )
                if not discovered_candidates:
                    return None, "", "tail_stream_formal_discovery_absent"
                if len(discovered_candidates) != 1:
                    return None, "", "tail_stream_formal_discovery_ambiguous"
                target_formal, target_anchors = discovered_candidates[0]
                caller_formal = target_formal
                discovered = True
        else:
            seed_anchors = self._direct_stream_anchors(
                caller_va, caller_formal
            )
        if jump.target is None:
            return None, "", "tail_stream_target_unmapped"
        if not discovered:
            target_formal = caller_formal
            measured_target_anchors = []
            for direction in sorted(directions):
                matches = self._direct_stream_anchors(
                    jump.target, target_formal, frozenset((direction,))
                )
                if not matches:
                    return (
                        None,
                        "",
                        "tail_target_stream_%s_anchor_absent" % direction,
                    )
                measured_target_anchors.append(matches[0])
            target_anchors = tuple(measured_target_anchors)
        jump_off = self.image.va_to_off(jump.va)
        if jump_off is None or target_formal is None:
            return None, "", "tail_stream_jump_offset_unmapped"
        proof = []
        if seed_anchors:
            direction, site = sorted(seed_anchors, key=lambda item: item[1])[0]
            proof.append(
                self._stream_anchor_fragment(
                    "caller",
                    caller_va,
                    direction,
                    site,
                    "caller_formal",
                    caller_formal,
                )
            )
        proof.extend(self._stack_neutral_import_fragments(caller_va))
        proof.extend(self._stack_neutral_vtable_getid_fragments(caller_va))
        proof.extend(self._stack_identity_lea_fragments(caller_va))
        proof.extend(self._stack_formal_base_fragments(caller_va))
        if discovered:
            proof.append(
                self._stream_formal_discovery_fragment(
                    jump.va,
                    caller_va,
                    jump.target,
                    caller_formal,
                    target_formal,
                    directions,
                )
            )
            proof.append(
                "tail_stack_depth@0x%08X file_off=0x%08X "
                "caller=0x%08X depth=0"
                % (jump.va, jump_off, caller_va)
            )
        proof.append(
            "stream_tail@0x%08X file_off=0x%08X caller=0x%08X "
            "target=0x%08X caller_formal=entry+0x%X "
            "target_formal=entry+0x%X mapping=stack_preserved"
            % (
                jump.va,
                jump_off,
                caller_va,
                jump.target,
                caller_formal,
                target_formal,
            )
        )
        for direction, site in target_anchors:
            proof.append(
                self._stream_anchor_fragment(
                    "target",
                    jump.target,
                    direction,
                    site,
                    "target_formal",
                    target_formal,
                )
            )
        proof.extend(self._stack_neutral_import_fragments(jump.target))
        proof.extend(self._stack_neutral_vtable_getid_fragments(jump.target))
        proof.extend(self._stack_identity_lea_fragments(jump.target))
        proof.extend(self._stack_formal_base_fragments(jump.target))
        return target_formal, " AND ".join(dict.fromkeys(proof)), ""

    @staticmethod
    def _flag_branch_after(
        decoded: FunctionDecode, predicate: Instruction
    ) -> Instruction | None:
        site = predicate.next_va
        seen = set()
        while site in decoded.instructions and site not in seen:
            seen.add(site)
            ins = decoded.instructions[site]
            if ins.kind == "jcc":
                return ins if ins.condition in ("z", "nz") else None
            if ins.kind not in ("mov", "lea", "push", "pop", "jmp"):
                if ins.raw not in (b"\x90", b"\x66\x90"):
                    return None
            successors = decoded.successors.get(site, ())
            if len(successors) != 1:
                return None
            site = successors[0]
        return None

    @staticmethod
    def _predicate_width(predicate: Instruction) -> int:
        if any(
            operand is not None
            and operand.kind == "reg"
            and operand.reg in REG8
            for operand in (predicate.dst, predicate.src)
        ):
            return 1
        opcode = next(
            (value for value in predicate.raw if value not in PREFIX_BYTES),
            None,
        )
        if opcode in (0x38, 0x3A, 0x80, 0x82, 0x84, 0xA8, 0xF6):
            return 1
        return 2 if has_operand16_prefix(predicate.raw) else 4

    def _predicate_formal_offsets(
        self, va: int, predicate: Instruction
    ) -> frozenset[int]:
        return self._predicate_formal_offsets_with_zero_proof(
            va, predicate
        )[0]

    def _predicate_zero_reaching_fragment(
        self,
        function_va: int,
        predicate: Instruction,
        lane: str,
        reg: str,
        definition_vas: tuple[int, ...],
    ) -> str | None:
        definitions = []
        for definition_va in definition_vas:
            definition_off = self.image.va_to_off(definition_va)
            if definition_off is None:
                return None
            definitions.append(
                "definition@0x%08X file_off=0x%08X"
                % (definition_va, definition_off)
            )
        if not definitions:
            return None
        return (
            "predicate_zero_reaching function=0x%08X lane=%s register=%s "
            "use@0x%08X file_off=0x%08X consumed_width=1 value=zero "
            "definition_count=%d definitions=(%s) "
            "basis=all_reaching_full_width_xor_self"
            % (
                function_va,
                lane,
                reg,
                predicate.va,
                predicate.off,
                len(definitions),
                ",".join(definitions),
            )
        )

    def _predicate_formal_offsets_with_zero_proof(
        self, va: int, predicate: Instruction
    ) -> tuple[frozenset[int], str]:
        operand = None
        if (
            predicate.kind == "test"
            and predicate.dst is not None
            and predicate.src is not None
            and predicate.dst.key() == predicate.src.key()
        ):
            operand = predicate.dst
        elif (
            predicate.kind == "cmp"
            and predicate.dst is not None
            and predicate.src is not None
            and predicate.src.kind == "imm"
            and predicate.src.imm == 0
        ):
            operand = predicate.dst
        if operand is not None:
            return self._formal_offsets(va, predicate.va, operand), ""
        if (
            predicate.kind != "cmp"
            or predicate.dst is None
            or predicate.src is None
            or self._predicate_width(predicate) != 1
        ):
            return frozenset(), ""
        candidates = []
        low_lanes = frozenset(LOW8_BY_REG32.values())
        for formal_operand, zero_operand in (
            (predicate.dst, predicate.src),
            (predicate.src, predicate.dst),
        ):
            if (
                zero_operand.kind != "reg"
                or zero_operand.reg not in low_lanes
            ):
                continue
            reg = base_reg_name(zero_operand.reg)
            if reg is None:
                continue
            zero_proof = self._mode_argument_all_zero_reaching_definitions(
                va,
                predicate.va,
                Operand("reg", reg=reg),
                1,
            )
            formals = self._formal_offsets(
                va, predicate.va, formal_operand
            )
            if zero_proof is None or len(formals) != 1:
                continue
            fragment = self._predicate_zero_reaching_fragment(
                va,
                predicate,
                zero_operand.reg,
                reg,
                zero_proof[1],
            )
            if fragment is not None:
                candidates.append((formals, fragment))
        unique = {
            (tuple(sorted(formals)), fragment): (formals, fragment)
            for formals, fragment in candidates
        }
        if len(unique) != 1:
            return frozenset(), ""
        return next(iter(unique.values()))

    def _nested_mode_anchor(
        self, function_va: int, call: Instruction
    ) -> tuple[str, str] | None:
        """Prove one branch direction through one direct child primitive.

        This is deliberately one level deep.  The child must have exactly one
        measured capability, and the existing formal-stream proof must map a
        unique caller formal through every recovered argument path to a direct
        primitive ECX anchor in that child.
        """
        if call.kind != "call" or call.target is None:
            return None
        directions = self.capabilities(call.target)
        if len(directions) != 1:
            return None
        direction = next(iter(directions))
        decoded = self.decode(function_va)
        if decoded is None:
            return None
        abi = self.call_abi(decoded, call, call.target)
        if abi is None:
            return None
        sequences = recover_call_pushes(decoded, call.va, abi[1])
        if not sequences:
            return None
        target_formal, proof, reason = self._prove_direct_subcall_stream(
            function_va,
            None,
            call,
            abi,
            sequences,
            directions,
            allow_nested_target=False,
        )
        if target_formal is None or reason:
            return None
        stream_match = re.fullmatch(
            r"stream_call@0x%08X file_off=0x([0-9A-F]{8}) "
            r"caller=0x%08X target=0x%08X "
            r"caller_formal=entry\+0x([0-9A-F]+) "
            r"target_formal=entry\+0x([0-9A-F]+)"
            % (call.va, function_va, call.target),
            next(
                (
                    fragment
                    for fragment in proof.split(" AND ")
                    if fragment.startswith("stream_call@")
                ),
                "",
            ),
        )
        if stream_match is None:
            return None
        call_off = int(stream_match.group(1), 16)
        caller_formal = int(stream_match.group(2), 16)
        measured_target_formal = int(stream_match.group(3), 16)
        if (
            self.image.va_to_off(call.va) != call_off
            or measured_target_formal != target_formal
        ):
            return None
        argument_sites = tuple(
            sorted(
                {
                    (int(site, 16), int(off, 16))
                    for site, off in re.findall(
                        r"stream_arg@0x([0-9A-F]{8}) "
                        r"file_off=0x([0-9A-F]{8}) "
                        r"caller=0x%08X call=0x%08X target=0x%08X "
                        r"caller_formal=entry\+0x%X "
                        r"target_formal=entry\+0x%X"
                        % (
                            function_va,
                            call.va,
                            call.target,
                            caller_formal,
                            target_formal,
                        ),
                        proof,
                    )
                }
            )
        )
        anchor_sites = tuple(
            sorted(
                {
                    (int(site, 16), int(off, 16), int(primitive, 16))
                    for found_direction, site, off, primitive in re.findall(
                        r"target_stream_anchor_([WR])@0x([0-9A-F]{8}) "
                        r"file_off=0x([0-9A-F]{8}) "
                        r"function=0x%08X primitive=0x([0-9A-F]{8}) "
                        r"target_formal=entry\+0x%X"
                        % (call.target, target_formal),
                        proof,
                    )
                    if found_direction == direction
                }
            )
        )
        if not argument_sites or len(anchor_sites) != 1:
            return None
        if any(
            self.image.va_to_off(site) != off
            for site, off in argument_sites
        ) or any(
            self.image.va_to_off(site) != off
            or primitive != (WRITE_VA if direction == "W" else READ_VA)
            for site, off, primitive in anchor_sites
        ):
            return None
        arguments = ",".join(
            "argument@0x%08X file_off=0x%08X" % item
            for item in argument_sites
        )
        anchors = ",".join(
            "primitive@0x%08X file_off=0x%08X target=0x%08X" % item
            for item in anchor_sites
        )
        fragment = (
            "mode_nested_anchor_%s@0x%08X file_off=0x%08X "
            "function=0x%08X target=0x%08X "
            "caller_stream_formal=entry+0x%X "
            "target_stream_formal=entry+0x%X arguments=(%s) "
            "primitives=(%s) stream_proof_sha256=%s "
            "basis=branch_exclusive_single_direction_direct_subcall"
            % (
                direction,
                call.va,
                call_off,
                function_va,
                call.target,
                caller_formal,
                target_formal,
                arguments,
                anchors,
                hashlib.sha256(proof.encode("utf-8")).hexdigest(),
            )
        )
        return direction, fragment

    def _target_stream_anchors(
        self,
        va: int,
        formal_offset: int,
        direction: str,
        allow_nested: bool = True,
    ) -> tuple[tuple[str, int, str], ...]:
        direct = self._direct_stream_anchors(
            va, formal_offset, frozenset((direction,))
        )
        if direct:
            return tuple((item_direction, site, "") for item_direction, site in direct)
        if not allow_nested:
            return ()
        decoded = self.decode(va)
        abi = None if decoded is None else self._function_abi(decoded)
        proof = None if abi is None else self._unique_mode_formal_proof(va, abi)
        if proof is None:
            return ()
        if proof.zero_direction == direction:
            value = "zero"
            site = proof.zero_anchor_va
            evidence = proof.zero_anchor_evidence
        elif proof.nonzero_direction == direction:
            value = "nonzero"
            site = proof.nonzero_anchor_va
            evidence = proof.nonzero_anchor_evidence
        else:
            return ()
        if not evidence:
            return ()
        match = re.fullmatch(
            r"mode_nested_anchor_%s@0x%08X file_off=0x([0-9A-F]{8}) "
            r"function=0x%08X target=0x([0-9A-F]{8}) "
            r"caller_stream_formal=entry\+0x([0-9A-F]+) "
            r"target_stream_formal=entry\+0x([0-9A-F]+) .*"
            % (direction, site, va),
            evidence,
        )
        if match is None or int(match.group(3), 16) != formal_offset:
            return ()
        off = int(match.group(1), 16)
        target = int(match.group(2), 16)
        child_formal = int(match.group(4), 16)
        if self.image.va_to_off(site) != off:
            return ()
        fragment = (
            "target_nested_stream_anchor_%s@0x%08X file_off=0x%08X "
            "function=0x%08X target=0x%08X "
            "target_formal=entry+0x%X child_formal=entry+0x%X "
            "mode_formal=entry+0x%X mode_value=%s "
            "nested_evidence_sha256=%s "
            "basis=direction_selected_branch_exclusive_subcall"
            % (
                direction,
                site,
                off,
                va,
                target,
                formal_offset,
                child_formal,
                proof.formal_offset,
                value,
                hashlib.sha256(evidence.encode("utf-8")).hexdigest(),
            )
        )
        return ((direction, site, fragment),)

    def mode_branch_proofs(
        self, va: int, abi: tuple[str, int]
    ) -> tuple[ModeBranchProof, ...]:
        key = (va, abi[0], abi[1])
        if key in self.mode_proof_cache:
            return self.mode_proof_cache[key]
        decoded = self.decode(va)
        if decoded is None or abi[1] < 1:
            self.mode_proof_cache[key] = ()
            return ()
        valid_formals = {4 * index for index in range(1, abi[1] + 1)}
        proofs = []
        for predicate in sorted(
            decoded.instructions.values(), key=lambda item: item.va
        ):
            branch = self._flag_branch_after(decoded, predicate)
            if branch is None or branch.target is None:
                continue
            formal_offsets, predicate_evidence = (
                self._predicate_formal_offsets_with_zero_proof(
                    va, predicate
                )
            )
            if len(formal_offsets) != 1:
                continue
            formal_offset = next(iter(formal_offsets))
            if formal_offset not in valid_formals:
                continue
            fall_nodes = _reachable_nodes(decoded, branch.next_va)
            jump_nodes = _reachable_nodes(decoded, branch.target)
            fall_only = fall_nodes - jump_nodes
            jump_only = jump_nodes - fall_nodes

            def anchors(
                nodes: frozenset[int],
            ) -> list[tuple[int, str, str]]:
                direct = sorted(
                    (
                        ins.va,
                        "W" if ins.target == WRITE_VA else "R",
                        "",
                    )
                    for ins in decoded.instructions.values()
                    if ins.va in nodes
                    and ins.kind == "call"
                    and ins.target in (WRITE_VA, READ_VA)
                )
                if direct:
                    return direct
                nested = []
                for ins in sorted(
                    decoded.instructions.values(), key=lambda item: item.va
                ):
                    if ins.va not in nodes:
                        continue
                    proof = self._nested_mode_anchor(va, ins)
                    if proof is not None:
                        direction, evidence = proof
                        nested.append((ins.va, direction, evidence))
                return nested if len(nested) == 1 else []

            fall_anchors = anchors(fall_only)
            jump_anchors = anchors(jump_only)
            fall_directions = {item[1] for item in fall_anchors}
            jump_directions = {item[1] for item in jump_anchors}
            if {
                frozenset(fall_directions), frozenset(jump_directions)
            } != {frozenset(("W",)), frozenset(("R",))}:
                continue
            if branch.condition == "z":
                zero_nodes, nonzero_nodes = jump_only, fall_only
                zero_anchors, nonzero_anchors = jump_anchors, fall_anchors
            else:
                zero_nodes, nonzero_nodes = fall_only, jump_only
                zero_anchors, nonzero_anchors = fall_anchors, jump_anchors
            zero_direction = zero_anchors[0][1]
            nonzero_direction = nonzero_anchors[0][1]
            zero_anchor_va = next(
                site for site, direction, _evidence in zero_anchors
                if direction == zero_direction
            )
            nonzero_anchor_va = next(
                site for site, direction, _evidence in nonzero_anchors
                if direction == nonzero_direction
            )
            zero_anchor_evidence = next(
                evidence for _site, direction, evidence in zero_anchors
                if direction == zero_direction
            )
            nonzero_anchor_evidence = next(
                evidence for _site, direction, evidence in nonzero_anchors
                if direction == nonzero_direction
            )
            zero_anchor_off = self.image.va_to_off(zero_anchor_va)
            nonzero_anchor_off = self.image.va_to_off(nonzero_anchor_va)
            if zero_anchor_off is None or nonzero_anchor_off is None:
                continue
            proofs.append(
                ModeBranchProof(
                    function_va=va,
                    formal_offset=formal_offset,
                    formal_width=self._predicate_width(predicate),
                    test_va=predicate.va,
                    test_off=predicate.off,
                    branch_va=branch.va,
                    branch_off=branch.off,
                    zero_direction=zero_direction,
                    nonzero_direction=nonzero_direction,
                    zero_nodes=zero_nodes,
                    nonzero_nodes=nonzero_nodes,
                    zero_anchor_va=zero_anchor_va,
                    zero_anchor_off=zero_anchor_off,
                    nonzero_anchor_va=nonzero_anchor_va,
                    nonzero_anchor_off=nonzero_anchor_off,
                    zero_anchor_evidence=zero_anchor_evidence,
                    nonzero_anchor_evidence=nonzero_anchor_evidence,
                    predicate_evidence=predicate_evidence,
                )
            )
        result = tuple(proofs)
        self.mode_proof_cache[key] = result
        return result

    def _unique_mode_formal_proof(
        self, va: int, abi: tuple[str, int]
    ) -> ModeBranchProof | None:
        proofs = self.mode_branch_proofs(va, abi)
        signatures = {
            (
                proof.formal_offset,
                proof.formal_width,
                proof.zero_direction,
                proof.nonzero_direction,
            )
            for proof in proofs
        }
        if len(signatures) != 1:
            return None
        return min(proofs, key=lambda proof: proof.test_va)

    @classmethod
    def _mode_zero_classes(cls, expr: Expr) -> frozenset[str] | None:
        if expr == ("const", 0):
            return frozenset(("zero",))
        if expr == ("const", 1):
            return frozenset(("nonzero",))
        if expr and expr[0] == "phi":
            classes = set()
            for option in expr[1]:
                resolved = cls._mode_zero_classes(option)
                if resolved is None:
                    return None
                classes.update(resolved)
            return frozenset(classes)
        return None

    @staticmethod
    def _mode_proof_fragment(prefix: str, proof: ModeBranchProof) -> str:
        fragment = (
            "%s_test@0x%08X file_off=0x%08X branch@0x%08X "
            "file_off=0x%08X formal=entry+0x%X zero=%s nonzero=%s width=%d "
            "zero_anchor@0x%08X file_off=0x%08X "
            "nonzero_anchor@0x%08X file_off=0x%08X"
            % (
                prefix,
                proof.test_va,
                proof.test_off,
                proof.branch_va,
                proof.branch_off,
                proof.formal_offset,
                proof.zero_direction,
                proof.nonzero_direction,
                proof.formal_width,
                proof.zero_anchor_va,
                proof.zero_anchor_off,
                proof.nonzero_anchor_va,
                proof.nonzero_anchor_off,
            )
        )
        nested = tuple(
            item
            for item in (
                proof.zero_anchor_evidence,
                proof.nonzero_anchor_evidence,
            )
            if item
        )
        if nested:
            fragment += " nested_anchors=(%s)" % ";".join(nested)
        if proof.predicate_evidence:
            fragment += " predicate_zero=(%s)" % proof.predicate_evidence
        return fragment

    def _caller_mode_classes(
        self,
        caller_va: int,
        caller_abi: tuple[str, int] | None,
        call_site: int,
        argument: PushArgument,
        resolver: RegisterResolver,
        target_width: int,
    ) -> tuple[frozenset[str] | None, tuple[str, ...]]:
        direct = self._mode_zero_classes(self._arg_expr(resolver, argument))
        argument_off = self.image.va_to_off(argument.instruction_va)
        if direct is not None and argument_off is not None:
            evidence = tuple(
                "mode_arg@0x%08X file_off=0x%08X value=%s"
                % (argument.instruction_va, argument_off, value)
                for value in sorted(direct)
            )
            return direct, evidence
        zero_reaching = self._mode_argument_zero_reaching_definition(
            caller_va,
            argument.instruction_va,
            argument.operand,
            target_width,
        )
        if zero_reaching is not None:
            reg, definition_va = zero_reaching
            fragment = self._mode_zero_reaching_fragment(
                caller_va, argument, reg, definition_va
            )
            if fragment is not None:
                return frozenset(("zero",)), (fragment,)
        zero_reaching_set = (
            self._mode_argument_all_zero_reaching_definitions(
                caller_va,
                argument.instruction_va,
                argument.operand,
                target_width,
            )
        )
        if zero_reaching_set is not None and len(zero_reaching_set[1]) > 1:
            reg, definition_vas = zero_reaching_set
            fragment = self._mode_zero_reaching_set_fragment(
                caller_va, argument, reg, definition_vas
            )
            if fragment is not None:
                return frozenset(("zero",)), (fragment,)
        identity_zero = self._mode_argument_zero_through_identity_lea(
            caller_va,
            argument.instruction_va,
            argument.operand,
            target_width,
        )
        if identity_zero is not None:
            reg, identity_va, definition_vas = identity_zero
            fragment = self._mode_zero_identity_lea_fragment(
                caller_va,
                argument,
                reg,
                identity_va,
                definition_vas,
            )
            if fragment is not None:
                return frozenset(("zero",)), (fragment,)
        if caller_abi is None:
            return None, ()
        formal_offsets = self._mode_argument_formal_offsets(
            caller_va,
            argument.instruction_va,
            argument.operand,
            target_width,
        )
        if len(formal_offsets) != 1 or argument_off is None:
            return None, ()
        formal_offset = next(iter(formal_offsets))
        values = set()
        evidence = []
        proofs = tuple(
            proof
            for proof in self.mode_branch_proofs(caller_va, caller_abi)
            if proof.formal_offset == formal_offset
            and proof.formal_width == target_width
        )
        if len(
            {(proof.zero_direction, proof.nonzero_direction) for proof in proofs}
        ) != 1:
            return None, ()
        for proof in proofs:
            if call_site in proof.zero_nodes:
                value = "zero"
            elif call_site in proof.nonzero_nodes:
                value = "nonzero"
            else:
                continue
            values.add(value)
            evidence.append(
                "%s mode_arg@0x%08X file_off=0x%08X value=%s"
                % (
                    self._mode_proof_fragment("caller", proof),
                    argument.instruction_va,
                    argument_off,
                    value,
                )
            )
        if not values:
            return None, ()
        return frozenset(values), tuple(sorted(set(evidence)))

    def _prove_direct_subcall_directions(
        self,
        caller_va: int,
        caller_abi: tuple[str, int] | None,
        resolver: RegisterResolver,
        call: Instruction,
        target_abi: tuple[str, int],
        sequences: tuple[tuple[PushArgument, ...], ...],
    ) -> tuple[frozenset[str] | None, str, str]:
        target_proof = self._unique_mode_formal_proof(
            call.target or 0, target_abi
        )
        if target_proof is None:
            return None, "", "target_mode_formal_unproved"
        source_index = target_abi[1] - target_proof.formal_offset // 4
        if not (0 <= source_index < target_abi[1]):
            return None, "", "target_mode_formal_index_invalid"
        values = set()
        evidence = []
        reaching_fragments = []
        for sequence in sequences:
            mode_origins: frozenset[int] | None = None
            mode_proof_keys: tuple[tuple[int, int, str], ...] = ()
            if target_proof.formal_width == 1:
                mode_origins, mode_proof_keys = (
                    self._mode_argument_formal_offsets_with_reaching_proof(
                        caller_va,
                        sequence[source_index].instruction_va,
                        sequence[source_index].operand,
                        target_proof.formal_width,
                    )
                )
            classes, path_evidence = self._caller_mode_classes(
                caller_va,
                caller_abi,
                call.va,
                sequence[source_index],
                resolver,
                target_proof.formal_width,
            )
            if classes is None:
                if caller_abi is None:
                    return None, "", "caller_mode_value_unproved"
                argument = sequence[source_index]
                argument_off = self.image.va_to_off(argument.instruction_va)
                formal_offsets = (
                    mode_origins
                    if mode_origins is not None
                    else self._mode_argument_formal_offsets(
                        caller_va,
                        argument.instruction_va,
                        argument.operand,
                        target_proof.formal_width,
                    )
                )
                if len(formal_offsets) != 1 or argument_off is None:
                    return None, "", "caller_mode_value_unproved"
                caller_formal = next(iter(formal_offsets))
                caller_proof = self._unique_mode_formal_proof(
                    caller_va, caller_abi
                )
                if (
                    caller_proof is None
                    or caller_proof.formal_offset != caller_formal
                    or caller_proof.formal_width != target_proof.formal_width
                ):
                    return None, "", "caller_mode_value_unproved"
                if (
                    caller_proof.zero_direction,
                    caller_proof.nonzero_direction,
                ) != (
                    target_proof.zero_direction,
                    target_proof.nonzero_direction,
                ):
                    return None, "", "caller_target_mode_mapping_mismatch"
                classes = frozenset(("zero", "nonzero"))
                path_evidence = (
                    "%s mode_arg@0x%08X file_off=0x%08X "
                    "value=formal_forward caller_formal=entry+0x%X "
                    "target_formal=entry+0x%X width=%d mapping=preserved"
                    % (
                        self._mode_proof_fragment("caller", caller_proof),
                        argument.instruction_va,
                        argument_off,
                        caller_formal,
                        target_proof.formal_offset,
                        target_proof.formal_width,
                    ),
                )
            if mode_proof_keys:
                if mode_origins is None or len(mode_origins) != 1:
                    return None, "", "caller_mode_reaching_proof_inconsistent"
                reaching_fragments.extend(
                    self._formal_reaching_fragments(
                        next(iter(mode_origins)), mode_proof_keys
                    )
                )
            values.update(classes)
            evidence.extend(path_evidence)
        directions = {
            target_proof.zero_direction
            if value == "zero"
            else target_proof.nonzero_direction
            for value in values
        }
        call_off = self.image.va_to_off(call.va)
        if call_off is None:
            return None, "", "direction_call_offset_unmapped"
        proof_text = "direction_call@0x%08X file_off=0x%08X %s paths=(%s)" % (
            call.va,
            call_off,
            self._mode_proof_fragment("target", target_proof),
            " OR ".join(sorted(set(evidence))),
        )
        for fragment in sorted(set(reaching_fragments)):
            proof_text = combine_gate(proof_text, fragment)
        return frozenset(directions), proof_text, ""

    def _indirect_mode_formal_source_fragment(
        self,
        caller_va: int,
        argument: PushArgument,
        formal_offset: int,
    ) -> str | None:
        """Pin one indirect-mode push to one exact entry-stack load."""
        decoded = self.decode(caller_va)
        if (
            decoded is None
            or argument.operand.kind != "reg"
            or argument.operand.reg not in REG32
            or argument.operand.reg == "esp"
        ):
            return None
        reg = argument.operand.reg
        use = decoded.instructions.get(argument.instruction_va)
        if (
            use is None
            or use.kind != "push"
            or use.src != argument.operand
            or use.raw != bytes((0x50 | REG32.index(reg),))
        ):
            return None
        definitions = self._reaching_definitions(caller_va, reg).get(
            argument.instruction_va, frozenset()
        )
        if len(definitions) != 1 or None in definitions:
            return None
        definition_va = next(iter(definitions))
        assert definition_va is not None
        definition = decoded.instructions.get(definition_va)
        if (
            definition is None
            or definition.dst is None
            or definition.dst.kind != "reg"
            or definition.dst.reg != reg
            or definition.src is None
            or definition.src.kind != "mem"
            or definition.src.base != "esp"
            or definition.src.index is not None
            or definition.src.absolute is not None
            or not (-0x80 <= definition.src.disp <= 0x7F)
            or definition.raw
            != bytes(
                (
                    0x8B,
                    0x44 | (REG32.index(reg) << 3),
                    0x24,
                    definition.src.disp & 0xFF,
                )
            )
        ):
            return None
        depths = self._stack_depths(caller_va).get(
            definition_va, frozenset()
        )
        if len(depths) != 1 or None in depths:
            return None
        depth = next(iter(depths))
        assert depth is not None
        if definition.src.disp - depth != formal_offset:
            return None
        definition_off = self.image.va_to_off(definition_va)
        use_off = self.image.va_to_off(argument.instruction_va)
        if definition_off is None or use_off is None:
            return None
        return (
            "indirect_mode_formal_source definition@0x%08X "
            "file_off=0x%08X use@0x%08X file_off=0x%08X "
            "function=0x%08X register=%s displacement=0x%X "
            "stack_depth=0x%X formal=entry+0x%X "
            "basis=singleton_reaching_exact_esp_disp8_load"
            % (
                definition_va,
                definition_off,
                argument.instruction_va,
                use_off,
                caller_va,
                reg,
                definition.src.disp,
                depth,
                formal_offset,
            )
        )

    def _prove_indirect_serializer_directions(
        self,
        caller_va: int,
        caller_abi: tuple[str, int] | None,
        resolver: RegisterResolver,
        call: Instruction,
        sequences: tuple[tuple[PushArgument, ...], ...],
    ) -> tuple[frozenset[str] | None, str, str]:
        """Prove mode for the task-pinned indirect serializer slot +0x18.

        Existing literal 0/1 paths retain their narrow result.  The added
        case accepts a caller formal only when one exact byte-mode branch
        proves the call site, every recovered first argument reaches that
        same formal, and every reaching-definition/file-offset fragment can
        be emitted.  The target remains dynamic and is never recursed.
        """
        literal = self._path_mode_directions(resolver, sequences)
        if literal is not None:
            return literal, "", ""
        if caller_abi is None:
            return None, "", "caller_mode_formal_unproved"
        caller_proof = self._unique_mode_formal_proof(
            caller_va, caller_abi
        )
        if caller_proof is None:
            return None, "", "caller_mode_formal_unproved"
        values = set()
        evidence = []
        reaching_fragments = []
        for sequence in sequences:
            argument = sequence[0]
            origins, proof_keys = (
                self._mode_argument_formal_offsets_with_reaching_proof(
                    caller_va,
                    argument.instruction_va,
                    argument.operand,
                    caller_proof.formal_width,
                )
            )
            if origins != frozenset((caller_proof.formal_offset,)):
                return None, "", "caller_mode_argument_origin_unproved"
            source_fragment = self._indirect_mode_formal_source_fragment(
                caller_va, argument, caller_proof.formal_offset
            )
            if source_fragment is None:
                return None, "", "caller_mode_exact_source_unproved"
            classes, path_evidence = self._caller_mode_classes(
                caller_va,
                caller_abi,
                call.va,
                argument,
                resolver,
                caller_proof.formal_width,
            )
            if classes is None:
                return None, "", "caller_mode_value_unproved"
            values.update(classes)
            evidence.extend(path_evidence)
            reaching_fragments.append(source_fragment)
            reaching_fragments.extend(
                self._formal_reaching_fragments(
                    caller_proof.formal_offset, proof_keys
                )
            )
        directions = {
            caller_proof.zero_direction
            if value == "zero"
            else caller_proof.nonzero_direction
            for value in values
        }
        call_off = self.image.va_to_off(call.va)
        if not directions or call_off is None:
            return None, "", "indirect_direction_call_unmapped"
        proof_text = (
            "indirect_direction_call@0x%08X file_off=0x%08X %s "
            "paths=(%s)"
            % (
                call.va,
                call_off,
                self._mode_proof_fragment("caller", caller_proof),
                " OR ".join(sorted(set(evidence))),
            )
        )
        for fragment in self._stack_neutral_vtable_getid_fragments(
            caller_va
        ):
            proof_text = combine_gate(proof_text, fragment)
        for fragment in sorted(set(reaching_fragments)):
            proof_text = combine_gate(proof_text, fragment)
        return frozenset(directions), proof_text, ""

    def _local_capability_refinement(
        self, va: int
    ) -> tuple[frozenset[str] | None, str]:
        """Refine a transitive R/W union from complete known local edges.

        This does not change ``capabilities()``.  It is a call-site escape hatch
        only for a decoded function whose entry is immediately preceded by a
        measured ``ret; int3+`` boundary, has one or more direct primitives all
        in one direction, has no serializer-capable tail jump, and whose every
        known direct serializer child is either a matching singleton or has an
        exact local mode proof for that direction.
        Calls with no known serializer capability remain utilities and do not
        contribute to this deliberately bounded census.
        """
        cached = self.local_capability_refinement_cache.get(va)
        if cached is not None:
            return cached
        raw = self.capabilities(va)
        failed: tuple[frozenset[str] | None, str] = (None, "")
        if len(raw) <= 1:
            self.local_capability_refinement_cache[va] = failed
            return failed
        function_off = self.image.va_to_off(va)
        if function_off is None or function_off <= 0:
            self.local_capability_refinement_cache[va] = failed
            return failed
        int3_start_off = function_off
        cursor = function_off - 1
        while cursor >= 0 and self.image.data[cursor] == 0xCC:
            int3_start_off = cursor
            cursor -= 1
        int3_count = function_off - int3_start_off
        ret_off = cursor
        ret_va = None if ret_off < 0 else self.image.off_to_va(ret_off)
        int3_start_va = self.image.off_to_va(int3_start_off)
        if (
            int3_count < 1
            or ret_va is None
            or int3_start_va is None
            or self.image.data[ret_off] != 0xC3
        ):
            self.local_capability_refinement_cache[va] = failed
            return failed
        entry_boundary = (
            "ret@0x%08X file_off=0x%08X int3_start@0x%08X "
            "file_off=0x%08X int3_count=%d"
            % (ret_va, ret_off, int3_start_va, int3_start_off, int3_count)
        )
        decoded = self.decode(va)
        if (
            decoded is None
            or decoded.errors
            or decoded.span.start_va != va
        ):
            self.local_capability_refinement_cache[va] = failed
            return failed

        primitives: list[tuple[str, int, int]] = []
        children: list[tuple[Instruction, frozenset[str], int]] = []
        for ins in sorted(decoded.instructions.values(), key=lambda item: item.va):
            if ins.kind == "call" and ins.target in (WRITE_VA, READ_VA):
                direction = "W" if ins.target == WRITE_VA else "R"
                primitives.append((direction, ins.va, ins.target))
                continue
            if ins.kind == "jmp" and ins.target is not None and not (
                decoded.span.start_va <= ins.target < decoded.span.end_va
            ):
                tail_caps = self.capabilities(ins.target)
                if tail_caps or ins.target in self.root_vas:
                    self.local_capability_refinement_cache[va] = failed
                    return failed
                continue
            if ins.kind != "call" or ins.target is None:
                continue
            child_raw = self.capabilities(ins.target)
            if not child_raw:
                if ins.target in self.root_vas:
                    self.local_capability_refinement_cache[va] = failed
                    return failed
                continue
            call_off = self.image.va_to_off(ins.va)
            if call_off is None:
                self.local_capability_refinement_cache[va] = failed
                return failed
            children.append((ins, child_raw, call_off))

        primitive_directions = {item[0] for item in primitives}
        if not primitives or len(primitive_directions) != 1 or not children:
            self.local_capability_refinement_cache[va] = failed
            return failed
        refined_direction = next(iter(primitive_directions))
        child_fragments = []
        for ins, child_raw, call_off in children:
            child_label = ",".join(sorted(child_raw))
            if child_raw == frozenset((refined_direction,)):
                child_fragments.append(
                    "subcall@0x%08X file_off=0x%08X target=0x%08X "
                    "raw=%s refined=%s proof=capability_singleton"
                    % (
                        ins.va,
                        call_off,
                        ins.target,
                        child_label,
                        refined_direction,
                    )
                )
                continue
            abi = self.call_abi(decoded, ins, ins.target or 0)
            if abi is None:
                self.local_capability_refinement_cache[va] = failed
                return failed
            sequences = recover_call_pushes(decoded, ins.va, abi[1])
            if not sequences:
                self.local_capability_refinement_cache[va] = failed
                return failed
            proved, proof_text, proof_reason = (
                self._prove_direct_subcall_directions(
                    va,
                    None,
                    RegisterResolver(decoded),
                    ins,
                    abi,
                    sequences,
                )
            )
            if (
                proved != frozenset((refined_direction,))
                or proof_reason
                or not proof_text
            ):
                self.local_capability_refinement_cache[va] = failed
                return failed
            proof_hash = hashlib.sha256(proof_text.encode("ascii")).hexdigest()
            child_fragments.append(
                "subcall@0x%08X file_off=0x%08X target=0x%08X "
                "raw=%s refined=%s abi=%s:%d argument_paths=%d "
                "direction_proof_sha256=%s"
                % (
                    ins.va,
                    call_off,
                    ins.target,
                    child_label,
                    refined_direction,
                    abi[0],
                    abi[1],
                    len(sequences),
                    proof_hash,
                )
            )

        primitive_fragments = []
        for direction, site, target in primitives:
            site_off = self.image.va_to_off(site)
            if site_off is None:
                self.local_capability_refinement_cache[va] = failed
                return failed
            primitive_fragments.append(
                "primitive_%s@0x%08X file_off=0x%08X target=0x%08X"
                % (direction, site, site_off, target)
            )
        fragment = (
            "local_capability_refinement function=0x%08X raw=%s refined=%s "
            "entry_boundary=(%s) direct_primitives=(%s) subcalls=(%s) "
            "basis=complete_known_direct_serializer_edge_census"
            % (
                va,
                ",".join(sorted(raw)),
                refined_direction,
                entry_boundary,
                ";".join(primitive_fragments),
                ";".join(child_fragments),
            )
        )
        result = (frozenset((refined_direction,)), fragment)
        self.local_capability_refinement_cache[va] = result
        return result

    @staticmethod
    def _merge_exprs(expressions: Iterable[Expr]) -> Expr:
        unique = {repr(expr): expr for expr in expressions}
        if len(unique) == 1:
            return next(iter(unique.values()))
        return ("phi", tuple(unique[key] for key in sorted(unique)))

    def extract_events(
        self,
        va: int,
        context: Expr = ("obj",),
        allowed: frozenset[str] = frozenset(("W", "R")),
        inherited_gate: str = "ALWAYS",
        trail: tuple[int, ...] = (),
        depth: int = 0,
        formal_abi: tuple[str, int] | None = None,
        formal_stream_offset: int | None = None,
    ) -> tuple[WireEvent, ...]:
        span = self.span(va)
        decoded = self.decode(va)
        if span is None or decoded is None:
            synthetic = FunctionSpan(va, va, 0, 0, "UNKNOWN")
            return (
                WireEvent(
                    va,
                    tuple(sorted(allowed)),
                    "UNKNOWN",
                    None,
                    "N/A",
                    inherited_gate,
                    synthetic,
                    reason="function_span_not_found",
                ),
            )
        if va in trail or depth >= 12:
            return (
                WireEvent(
                    va,
                    tuple(sorted(allowed)),
                    "UNKNOWN",
                    None,
                    "N/A",
                    inherited_gate,
                    span,
                    reason="recursive_cycle_or_depth_limit",
                ),
            )

        if formal_abi is None:
            formal_abi = self._function_abi(decoded)
        gates = self.gates(va)
        events = []
        handled_decode_errors = set()
        next_trail = trail + (va,)

        for ins in sorted(decoded.instructions.values(), key=lambda item: item.va):
            local_gate = combine_gate(inherited_gate, gates.get(ins.va, "ALWAYS"))
            if (
                ins.kind == "call"
                and ins.target in ECX_PLUS_50_TAIL_JUMP_HELPERS
            ):
                spec = ECX_PLUS_50_TAIL_JUMP_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "ecx_plus_50_tail_jump_call@0x%08X "
                    "file_off=0x%08X function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    ecx_plus_50_tail_jump_helper_fragment(
                        self.image, ins.target
                    ),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if (
                ins.kind == "call"
                and ins.target in NESTED_CALL_COMPOSITION_HELPERS
            ):
                spec = NESTED_CALL_COMPOSITION_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "nested_three_call_composition_call@0x%08X "
                    "file_off=0x%08X function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    nested_call_composition_helper_fragment(
                        self.image, ins.target
                    ),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if (
                ins.kind == "call"
                and ins.target in LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS
            ):
                spec = LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "locked_mutable_dword_slot_update_call@0x%08X "
                    "file_off=0x%08X function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    locked_mutable_dword_slot_update_helper_fragment(
                        self.image, ins.target
                    ),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if (
                ins.kind == "call"
                and ins.target in MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS
            ):
                spec = MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "mutable_pointer_slot_traversal_call@0x%08X "
                    "file_off=0x%08X function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    mutable_pointer_slot_traversal_helper_fragment(
                        self.image, ins.target
                    ),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if (
                ins.kind == "call"
                and ins.target in MUTABLE_DWORD_SLOT_OPERATION_HELPERS
            ):
                spec = MUTABLE_DWORD_SLOT_OPERATION_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "mutable_dword_slot_operation_call@0x%08X "
                    "file_off=0x%08X function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    mutable_dword_slot_operation_helper_fragment(
                        self.image, ins.target
                    ),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if (
                ins.kind == "call"
                and ins.target in MUTABLE_DWORD_RANGE_GROWTH_HELPERS
            ):
                spec = MUTABLE_DWORD_RANGE_GROWTH_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "mutable_dword_range_growth_call@0x%08X "
                    "file_off=0x%08X function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    mutable_dword_range_growth_helper_fragment(
                        self.image, ins.target
                    ),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if (
                ins.kind == "call"
                and ins.target in CRITICAL_SECTION_POINTER_HELPERS
            ):
                spec = CRITICAL_SECTION_POINTER_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "critical_section_pointer_call@0x%08X "
                    "file_off=0x%08X function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    critical_section_pointer_helper_fragment(
                        self.image, ins.target
                    ),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if (
                ins.kind == "call"
                and ins.target in LOCKED_MUTABLE_POINTER_SLOT_HELPERS
            ):
                spec = LOCKED_MUTABLE_POINTER_SLOT_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "locked_mutable_pointer_slot_call@0x%08X "
                    "file_off=0x%08X function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    locked_mutable_pointer_slot_helper_fragment(
                        self.image, ins.target
                    ),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if ins.kind == "call" and ins.target in MUTABLE_CHAIN_HELPERS:
                spec = MUTABLE_CHAIN_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "mutable_chain_call@0x%08X file_off=0x%08X "
                    "function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    mutable_chain_helper_fragment(self.image, ins.target),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if ins.kind == "call" and ins.target in PURE_CHAIN_HELPERS:
                spec = PURE_CHAIN_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "pure_chain_call@0x%08X file_off=0x%08X "
                    "function=0x%08X target=0x%08X "
                    "caller_suffix=movzx_eax_al,add_esp_8"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate, pure_chain_helper_fragment(ins.target)
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        "0",
                        local_gate,
                        span,
                        target_va=ins.target,
                    )
                )
                continue

            if ins.kind == "call" and ins.target in ATOMIC_OBJECT_HELPERS:
                spec = ATOMIC_OBJECT_HELPERS[ins.target]
                local_gate = combine_gate(
                    local_gate,
                    "atomic_object_call@0x%08X file_off=0x%08X "
                    "function=0x%08X target=0x%08X"
                    % (ins.va, ins.off, va, ins.target),
                )
                local_gate = combine_gate(
                    local_gate,
                    atomic_object_helper_fragment(self.image, ins.target),
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        spec.tag,
                        None,
                        spec.length,
                        local_gate,
                        span,
                        reason=spec.reason,
                        target_va=ins.target,
                    )
                )
                continue

            if ins.kind == "call" and ins.target in STRING_WIRE_HELPERS:
                spec = STRING_WIRE_HELPERS[ins.target]
                direction = spec.direction
                if direction not in allowed:
                    continue
                stream_origins, reaching_proof = (
                    self._formal_offsets_with_reaching_proof(
                        va, ins.va, Operand("reg", reg="ecx")
                    )
                )
                expected_stream = formal_stream_offset
                if expected_stream is None:
                    valid_formals = (
                        frozenset()
                        if formal_abi is None
                        else frozenset(
                            range(4, formal_abi[1] * 4 + 1, 4)
                        )
                    )
                    if (
                        len(stream_origins) == 1
                        and stream_origins.issubset(valid_formals)
                    ):
                        expected_stream = next(iter(stream_origins))
                if (
                    expected_stream is None
                    or stream_origins != frozenset((expected_stream,))
                ):
                    observed = (
                        ",".join(
                            "0x%X" % value
                            for value in sorted(stream_origins)
                        )
                        if stream_origins
                        else "NONE"
                    )
                    expected = (
                        "DISCOVER_SINGLETON_FORMAL"
                        if formal_stream_offset is None
                        else "entry+0x%X" % formal_stream_offset
                    )
                    events.append(
                        WireEvent(
                            ins.va,
                            (direction,),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason=(
                                "string_stream_provenance_unresolved "
                                "target=0x%08X expected=%s observed=%s"
                                % (ins.target, expected, observed)
                            ),
                            target_va=ins.target,
                        )
                    )
                    continue
                local_gate = combine_gate(
                    local_gate,
                    "string_wire_call@0x%08X file_off=0x%08X "
                    "function=0x%08X target=0x%08X "
                    "stream_formal=entry+0x%X"
                    % (
                        ins.va,
                        ins.off,
                        va,
                        ins.target,
                        expected_stream,
                    ),
                )
                local_gate = combine_gate(
                    local_gate,
                    string_wire_helper_fragment(self.image, ins.target),
                )
                for fragment in self._formal_reaching_fragments(
                    expected_stream, reaching_proof
                ):
                    local_gate = combine_gate(local_gate, fragment)
                sequences = recover_call_pushes(decoded, ins.va, 1)
                if len(sequences) != 1:
                    events.append(
                        WireEvent(
                            ins.va,
                            (direction,),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="string_argument_paths=%d" % len(sequences),
                            target_va=ins.target,
                        )
                    )
                    continue
                pointer = self._arg_expr(
                    RegisterResolver(decoded), sequences[0][0]
                )
                pointer = self._normalize_expr(va, pointer, context)
                events.append(
                    WireEvent(
                        ins.va,
                        (direction,),
                        spec.tag,
                        pointer,
                        "4+N_bytes",
                        local_gate,
                        span,
                        reason=(
                            "field_pointer_unresolved"
                            if expr_contains_unknown(pointer)
                            else ""
                        ),
                        target_va=ins.target,
                    )
                )
                continue

            if ins.kind == "call" and ins.target in (WRITE_VA, READ_VA):
                direction = "W" if ins.target == WRITE_VA else "R"
                if direction not in allowed:
                    continue
                if formal_stream_offset is not None:
                    stream_origins, reaching_proof = (
                        self._formal_offsets_with_reaching_proof(
                        va, ins.va, Operand("reg", reg="ecx")
                        )
                    )
                    if stream_origins != frozenset((formal_stream_offset,)):
                        observed = (
                            ",".join("0x%X" % value for value in sorted(stream_origins))
                            if stream_origins
                            else "NONE"
                        )
                        events.append(
                            WireEvent(
                                ins.va,
                                (direction,),
                                "UNKNOWN",
                                None,
                                "N/A",
                                local_gate,
                                span,
                                reason=(
                                    "primitive_stream_provenance_unresolved "
                                    "expected=entry+0x%X observed=%s"
                                    % (formal_stream_offset, observed)
                                ),
                            )
                        )
                        continue
                    local_gate = combine_gate(
                        local_gate,
                        "primitive_stream@0x%08X file_off=0x%08X "
                        "function=0x%08X primitive=0x%08X "
                        "stream_formal=entry+0x%X"
                        % (
                            ins.va,
                            ins.off,
                            va,
                            ins.target,
                            formal_stream_offset,
                        ),
                    )
                    for fragment in self._formal_reaching_fragments(
                        formal_stream_offset, reaching_proof
                    ):
                        local_gate = combine_gate(local_gate, fragment)
                sequences = recover_call_pushes(decoded, ins.va, 3)
                if len(sequences) != 1:
                    events.append(
                        WireEvent(
                            ins.va, (direction,), "UNKNOWN", None, "N/A",
                            local_gate, span,
                            reason="primitive_argument_paths=%d" % len(sequences),
                        )
                    )
                    continue
                length_arg, pointer_arg, tag_arg = sequences[0]
                if length_arg.operand.kind != "imm" or tag_arg.operand.kind != "imm":
                    events.append(
                        WireEvent(
                            ins.va, (direction,), "UNKNOWN", None, "N/A",
                            local_gate, span,
                            reason="primitive_tag_or_len_not_immediate",
                        )
                    )
                    continue
                pointer = self._arg_expr(
                    RegisterResolver(decoded), pointer_arg
                )
                pointer = self._normalize_expr(va, pointer, context)
                events.append(
                    WireEvent(
                        ins.va,
                        (direction,),
                        "0x%02X" % (tag_arg.operand.imm or 0),
                        pointer,
                        str(length_arg.operand.imm or 0),
                        local_gate,
                        span,
                        reason=(
                            "field_pointer_unresolved"
                            if expr_contains_unknown(pointer)
                            else ""
                        ),
                    )
                )
                continue

            if ins.kind == "call" and ins.target is not None:
                if ins.target in PE_SECURITY_COOKIE_CHECK_HELPERS:
                    spec = PE_SECURITY_COOKIE_CHECK_HELPERS[ins.target]
                    local_gate = combine_gate(
                        local_gate,
                        "pe_security_cookie_check_call@0x%08X "
                        "file_off=0x%08X function=0x%08X target=0x%08X "
                        "call_bytes=%s"
                        % (
                            ins.va,
                            ins.off,
                            va,
                            ins.target,
                            ins.raw.hex().upper(),
                        ),
                    )
                    local_gate = combine_gate(
                        local_gate,
                        pe_security_cookie_check_helper_fragment(
                            self.image, ins.target
                        ),
                    )
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            spec.tag,
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason=spec.reason,
                            target_va=ins.target,
                        )
                    )
                    continue
                if ins.target in EXACT_IMPORT_THUNK_CALLS:
                    spec = EXACT_IMPORT_THUNK_CALLS[ins.target]
                    local_gate = combine_gate(
                        local_gate,
                        "exact_rel32_import_thunk_call@0x%08X "
                        "file_off=0x%08X function=0x%08X target=0x%08X "
                        "call_bytes=%s"
                        % (
                            ins.va,
                            ins.off,
                            va,
                            ins.target,
                            ins.raw.hex().upper(),
                        ),
                    )
                    local_gate = combine_gate(
                        local_gate,
                        exact_import_thunk_call_fragment(
                            self.image, ins.target
                        ),
                    )
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            spec.tag,
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason=spec.reason,
                            target_va=ins.target,
                        )
                    )
                    continue
                raw_target_caps = self.capabilities(ins.target)
                target_caps = raw_target_caps
                is_candidate = bool(target_caps) or ins.target in self.root_vas
                if not is_candidate:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "CALL_UNCLASSIFIED:0x%08X" % ins.target,
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="direct_call_not_proven_serializer",
                            target_va=ins.target,
                        )
                    )
                    continue
                abi = self.call_abi(decoded, ins, ins.target)
                if abi is None:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="subcall_abi_unresolved target=0x%08X"
                            % ins.target,
                            target_va=ins.target,
                        )
                    )
                    continue
                abi_kind, argument_count = abi
                sequences = recover_call_pushes(decoded, ins.va, argument_count)
                if not sequences:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="subcall_argument_paths=0 target=0x%08X"
                            % ins.target,
                            target_va=ins.target,
                        )
                    )
                    continue
                directions = set(target_caps or allowed)
                local_direction_proved = False
                if len(target_caps) > 1:
                    proved, proof_text, proof_reason = (
                        self._prove_direct_subcall_directions(
                            va,
                            formal_abi,
                            RegisterResolver(decoded),
                            ins,
                            abi,
                            sequences,
                        )
                    )
                    if proved is None:
                        refined_caps: frozenset[str] | None = None
                        refinement_gate = ""
                        if proof_reason == "target_mode_formal_unproved":
                            refined_caps, refinement_gate = (
                                self._local_capability_refinement(ins.target)
                            )
                        if refined_caps is None:
                            events.append(
                                WireEvent(
                                    ins.va,
                                    tuple(sorted(allowed)),
                                    "UNKNOWN",
                                    None,
                                    "N/A",
                                    local_gate,
                                    span,
                                    reason=(
                                        "subcall_direction_unresolved "
                                        "target=0x%08X proof=%s"
                                        % (ins.target, proof_reason)
                                    ),
                                    target_va=ins.target,
                                )
                            )
                            continue
                        target_caps = refined_caps
                        directions = set(refined_caps)
                        local_gate = combine_gate(
                            local_gate, refinement_gate
                        )
                    else:
                        directions.intersection_update(proved)
                        local_gate = combine_gate(local_gate, proof_text)
                    local_direction_proved = True
                directions.intersection_update(allowed)
                if (
                    not directions
                    and len(target_caps) == 1
                    and formal_abi is not None
                ):
                    branch_proof = self._unique_mode_formal_proof(
                        va, formal_abi
                    )
                    if branch_proof is not None:
                        if ins.va in branch_proof.zero_nodes:
                            branch_value = "zero"
                            branch_direction = branch_proof.zero_direction
                        elif ins.va in branch_proof.nonzero_nodes:
                            branch_value = "nonzero"
                            branch_direction = branch_proof.nonzero_direction
                        else:
                            branch_value = ""
                            branch_direction = ""
                        if (
                            branch_direction in target_caps
                            and branch_direction not in allowed
                        ):
                            local_gate = combine_gate(
                                local_gate,
                                (
                                    "infeasible_direction_call@0x%08X "
                                    "file_off=0x%08X branch_value=%s "
                                    "branch_direction=%s allowed=%s %s"
                                    % (
                                        ins.va,
                                        ins.off,
                                        branch_value,
                                        branch_direction,
                                        ",".join(sorted(allowed)),
                                        self._mode_proof_fragment(
                                            "caller", branch_proof
                                        ),
                                    )
                                ),
                            )
                            local_direction_proved = True
                if not directions:
                    if local_direction_proved:
                        events.append(
                            WireEvent(
                                ins.va,
                                (),
                                "DIRECTION_INFEASIBLE",
                                None,
                                "N/A",
                                local_gate,
                                span,
                                reason=(
                                    "subcall_direction_infeasible "
                                    "target=0x%08X"
                                    % ins.target
                                ),
                                target_va=ins.target,
                            )
                        )
                        continue
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="subcall_direction_conflict target=0x%08X"
                            % ins.target,
                            target_va=ins.target,
                        )
                    )
                    continue
                target_stream_formal, stream_proof, stream_reason = (
                    self._prove_direct_subcall_stream(
                        va,
                        formal_stream_offset,
                        ins,
                        abi,
                        sequences,
                        frozenset(directions),
                    )
                )
                if target_stream_formal is None:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(directions)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason=(
                                "subcall_stream_provenance_unresolved "
                                "target=0x%08X proof=%s"
                                % (ins.target, stream_reason)
                            ),
                            target_va=ins.target,
                        )
                    )
                    continue
                local_gate = combine_gate(local_gate, stream_proof)
                if abi_kind == "cdecl":
                    sub_context = self._merge_exprs(
                        self._arg_expr(
                            RegisterResolver(decoded), sequence[-1]
                        )
                        for sequence in sequences
                    )
                    sub_context = self._normalize_expr(va, sub_context, context)
                else:
                    # Context discovery is conditional on a subcall being
                    # accepted.  Keep its cycle-breaking memo isolated so a
                    # newly proved call cannot alter later, unrelated field
                    # expressions through RegisterResolver query order.
                    sub_context = RegisterResolver(decoded).reg_before(
                        ins.va, "ecx"
                    )
                    sub_context = self._normalize_expr(va, sub_context, context)
                child_gate = combine_gate(
                    local_gate,
                    "subcall_path@0x%08X file_off=0x%08X target=0x%08X"
                    % (ins.va, ins.off, ins.target),
                )
                children = self.extract_events(
                    ins.target,
                    context=sub_context,
                    allowed=frozenset(directions),
                    inherited_gate=child_gate,
                    trail=next_trail,
                    depth=depth + 1,
                    formal_abi=abi,
                    formal_stream_offset=target_stream_formal,
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(directions)),
                        "SUBCALL:0x%08X" % ins.target,
                        sub_context,
                        "N/A",
                        local_gate,
                        span,
                        reason=(
                            "subcall_context_unresolved"
                            if expr_contains_unknown(sub_context)
                            else ""
                        ),
                        target_va=ins.target,
                        children=children,
                    )
                )
                continue

            if ins.kind == "call_indirect":
                direct_iat_va = (
                    None
                    if ins.src is None
                    or ins.src.kind != "mem"
                    or ins.src.absolute is None
                    else ins.src.absolute
                )
                if direct_iat_va in EXACT_DIRECT_IMPORT_CALLS:
                    spec = EXACT_DIRECT_IMPORT_CALLS[direct_iat_va]
                    local_gate = combine_gate(
                        local_gate,
                        "exact_direct_iat_call@0x%08X file_off=0x%08X "
                        "function=0x%08X iat=0x%08X bytes=%s"
                        % (
                            ins.va,
                            ins.off,
                            va,
                            direct_iat_va,
                            ins.raw.hex().upper(),
                        ),
                    )
                    local_gate = combine_gate(
                        local_gate,
                        exact_direct_import_call_fragment(
                            self.image, direct_iat_va
                        ),
                    )
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            spec.tag,
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason=spec.reason,
                        )
                    )
                    continue
                register_import_proof = self._stack_neutral_register_import(
                    va, ins
                )
                if (
                    register_import_proof is not None
                    and register_import_proof[0].iat_va
                    in EXACT_SINGLETON_REGISTER_IMPORT_CALLS
                ):
                    symbol, register, definition_va = register_import_proof
                    spec = EXACT_SINGLETON_REGISTER_IMPORT_CALLS[
                        symbol.iat_va
                    ]
                    local_gate = combine_gate(
                        local_gate,
                        exact_singleton_register_import_call_fragment(
                            self.image,
                            va,
                            ins.va,
                            register,
                            definition_va,
                            symbol.iat_va,
                        ),
                    )
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            spec.tag,
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason=spec.reason,
                        )
                    )
                    continue
                multi_register_import_proof = self._all_same_register_import(
                    va, ins
                )
                if (
                    multi_register_import_proof is not None
                    and multi_register_import_proof[0].iat_va
                    in EXACT_MULTI_REGISTER_IMPORT_CALLS
                ):
                    symbol, register, definition_vas = (
                        multi_register_import_proof
                    )
                    spec = EXACT_MULTI_REGISTER_IMPORT_CALLS[symbol.iat_va]
                    local_gate = combine_gate(
                        local_gate,
                        exact_multi_register_import_call_fragment(
                            self.image,
                            va,
                            ins.va,
                            register,
                            definition_vas,
                            symbol.iat_va,
                        ),
                    )
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            spec.tag,
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason=spec.reason,
                        )
                    )
                    continue
                indirect_resolver = RegisterResolver(decoded)
                target_expr = (
                    expr_unknown("indirect_operand")
                    if ins.src is None
                    else indirect_resolver.operand_before(
                        ins.va, ins.src, dereference=(ins.src.kind == "mem")
                    )
                )
                target_text = format_expr(target_expr)
                sequences = recover_call_pushes(decoded, ins.va, 2)
                if not is_proven_serializer_vtable_target(target_expr):
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "CALL_UNCLASSIFIED:INDIRECT(%s)" % target_text,
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="indirect_call_not_proven_serializer_slot",
                        )
                    )
                    continue
                if not sequences:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="indirect_serializer_arguments_unresolved",
                        )
                    )
                    continue
                directions = set(allowed)
                if len(directions) > 1:
                    path_directions, direction_proof, _direction_reason = (
                        self._prove_indirect_serializer_directions(
                            va,
                            formal_abi,
                            indirect_resolver,
                            ins,
                            sequences,
                        )
                    )
                    if path_directions is None:
                        events.append(
                            WireEvent(
                                ins.va,
                                tuple(sorted(allowed)),
                                "UNKNOWN",
                                None,
                                "N/A",
                                local_gate,
                                span,
                                reason="indirect_serializer_direction_unresolved",
                            )
                        )
                        continue
                    directions.intersection_update(path_directions)
                    local_gate = combine_gate(
                        local_gate, direction_proof
                    )
                if not directions:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="indirect_serializer_direction_conflict",
                        )
                    )
                    continue
                sub_context = indirect_resolver.reg_before(
                    ins.va, "ecx"
                )
                sub_context = self._normalize_expr(va, sub_context, context)
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(directions)),
                        "SUBCALL:INDIRECT(%s)" % target_text,
                        sub_context,
                        "N/A",
                        local_gate,
                        span,
                        reason="indirect_subserializer_target",
                    )
                )
                continue

            if ins.kind == "jmp_indirect":
                target_expr = (
                    expr_unknown("indirect_operand")
                    if ins.src is None
                    else RegisterResolver(decoded).operand_before(
                        ins.va, ins.src, dereference=(ins.src.kind == "mem")
                    )
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(allowed)),
                        "JUMP_UNCLASSIFIED:INDIRECT(%s)" % format_expr(target_expr),
                        None,
                        "N/A",
                        local_gate,
                        span,
                        reason="indirect_jump_not_proven_serializer",
                    )
                )
                continue

            if (
                ins.kind == "jmp"
                and ins.target is not None
                and not (span.start_va <= ins.target < span.end_va)
            ):
                target_caps = self.capabilities(ins.target)
                if not target_caps and ins.target not in self.root_vas:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="tail_target_no_serialization_proof=0x%08X"
                            % ins.target,
                            target_va=ins.target,
                        )
                    )
                    continue
                directions = frozenset(set(target_caps or allowed) & set(allowed))
                tail_mode = recover_tail_mode(decoded, ins.va)
                if tail_mode is not None:
                    directions = frozenset(set(directions) & set(tail_mode))
                if not directions:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(allowed)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason="tail_subcall_direction_conflict target=0x%08X"
                            % ins.target,
                            target_va=ins.target,
                        )
                    )
                    continue
                target_stream_formal, stream_proof, stream_reason = (
                    self._prove_tail_subcall_stream(
                        va,
                        formal_stream_offset,
                        ins,
                        directions,
                    )
                )
                if target_stream_formal is None:
                    events.append(
                        WireEvent(
                            ins.va,
                            tuple(sorted(directions)),
                            "UNKNOWN",
                            None,
                            "N/A",
                            local_gate,
                            span,
                            reason=(
                                "tail_subcall_stream_provenance_unresolved "
                                "target=0x%08X proof=%s"
                                % (ins.target, stream_reason)
                            ),
                            target_va=ins.target,
                        )
                    )
                    continue
                local_gate = combine_gate(local_gate, stream_proof)
                sub_context = RegisterResolver(decoded).reg_before(
                    ins.va, "ecx"
                )
                sub_context = self._normalize_expr(va, sub_context, context)
                child_gate = combine_gate(
                    local_gate,
                    "subcall_path@0x%08X file_off=0x%08X target=0x%08X"
                    % (ins.va, ins.off, ins.target),
                )
                children = self.extract_events(
                    ins.target,
                    context=sub_context,
                    allowed=directions,
                    inherited_gate=child_gate,
                    trail=next_trail,
                    depth=depth + 1,
                    formal_abi=formal_abi,
                    formal_stream_offset=target_stream_formal,
                )
                events.append(
                    WireEvent(
                        ins.va,
                        tuple(sorted(directions)),
                        "SUBCALL:0x%08X" % ins.target,
                        sub_context,
                        "N/A",
                        local_gate,
                        span,
                        target_va=ins.target,
                        children=children,
                    )
                )
                handled_decode_errors.add(
                    "edge_outside_span@0x%08X->0x%08X" % (ins.va, ins.target)
                )

        for error in decoded.errors:
            if error in handled_decode_errors:
                continue
            events.append(
                WireEvent(
                    span.start_va,
                    tuple(sorted(allowed)),
                    "UNKNOWN",
                    None,
                    "N/A",
                    inherited_gate,
                    span,
                    reason="decode_error:%s" % error,
                )
            )

        if not events:
            constant_true_wire_empty = self._exact_constant_true_wire_empty(
                self.image, span
            )
            global_predicate_wire_empty = self._exact_global_predicate_wire_empty(
                self.image, span
            )
            argument_value_copier_wire_empty = (
                self._exact_argument_value_copier_wire_empty(self.image, span)
            )
            single_argument_value_copier_wire_empty = (
                self._exact_single_argument_value_copier_wire_empty(
                    self.image, span
                )
            )
            conditional_object_init_wire_empty = (
                self._exact_conditional_object_init_wire_empty(
                    self.image, span
                )
            )
            fpstest_entry_wire_empty = self._exact_fpstest_entry_wire_empty(
                self.image, span
            )
            if (
                self._exact_empty(self.image, span)
                or constant_true_wire_empty
                or global_predicate_wire_empty
                or argument_value_copier_wire_empty
                or single_argument_value_copier_wire_empty
                or conditional_object_init_wire_empty
                or fpstest_entry_wire_empty
            ):
                empty_gate = inherited_gate
                if constant_true_wire_empty:
                    empty_gate = combine_gate(
                        inherited_gate,
                        "wire_empty_constant_true@0x%08X file_off=0x%08X "
                        "bytes=B001C20400 behavior=write_al_1_then_ret_4"
                        % (span.start_va, span.start_off),
                    )
                elif global_predicate_wire_empty:
                    empty_gate = combine_gate(
                        inherited_gate,
                        "wire_empty_global_predicate@0x%08X file_off=0x%08X "
                        "bytes=833DC42E0301000F95C0C20400 "
                        "behavior=cmp_abs_global_zero_setne_al_ret_4"
                        % (span.start_va, span.start_off),
                    )
                elif argument_value_copier_wire_empty:
                    empty_gate = combine_gate(
                        inherited_gate,
                        "wire_empty_argument_value_copier@0x%08X "
                        "file_off=0x%08X "
                        "bytes=8B4424048B54240889411889511CC20800 "
                        "behavior=load_entry_arg_4_8_store_this_18_1C_ret_8"
                        % (span.start_va, span.start_off),
                    )
                elif single_argument_value_copier_wire_empty:
                    empty_gate = combine_gate(
                        inherited_gate,
                        "wire_empty_single_argument_value_copier@0x%08X "
                        "file_off=0x%08X bytes=8B442404894114C20400 "
                        "behavior=load_entry_arg_4_store_this_14_ret_4"
                        % (span.start_va, span.start_off),
                    )
                elif conditional_object_init_wire_empty:
                    empty_gate = combine_gate(
                        inherited_gate,
                        "wire_empty_conditional_object_init@0x%08X "
                        "file_off=0x%08X "
                        "bytes=33C03905C42E0301750532C0C20400"
                        "89415889415CB001C20400 "
                        "behavior=cmp_abs_global_false_or_store_this_58_5C_true_ret_4"
                        % (span.start_va, span.start_off),
                    )
                elif fpstest_entry_wire_empty:
                    empty_gate = combine_gate(
                        inherited_gate,
                        "wire_empty_fpstest_entry@0x%08X file_off=0x%08X "
                        "full_span_sha256=%s reachable_prefix_end=0x0073E8FE "
                        "reachable_prefix_sha256="
                        "1af255ab1fc762a99929747ae18351f35f50623cfc3124c69fe9b9126eb23897 "
                        "separator_file_off=0x0033DCFE bytes=CCCC "
                        "suffix_entry=0x0073E900 suffix_unreachable_from_entry "
                        "behavior=entry_reachable_paths_no_wire_field_suffix_unclaimed"
                        % (span.start_va, span.start_off, span.sha256),
                    )
                events.append(
                    WireEvent(
                        span.start_va,
                        tuple(sorted(allowed)),
                        "EMPTY",
                        None,
                        "0",
                        empty_gate,
                        span,
                    )
                )
            else:
                events.append(
                    WireEvent(
                        span.start_va,
                        tuple(sorted(allowed)),
                        "UNKNOWN",
                        None,
                        "N/A",
                        inherited_gate,
                        span,
                        reason="nonempty_body_unclassified",
                    )
                )
        numeric_re = re.compile(r"0x[0-9A-F]{2}")
        expected_claim_sites = set()
        for ins in decoded.instructions.values():
            if ins.kind == "call" and ins.target in (WRITE_VA, READ_VA):
                direction = "W" if ins.target == WRITE_VA else "R"
                if direction in allowed:
                    expected_claim_sites.add(ins.va)
            elif ins.kind == "call" and ins.target in STRING_WIRE_HELPERS:
                if STRING_WIRE_HELPERS[ins.target].direction in allowed:
                    expected_claim_sites.add(ins.va)
            elif ins.kind in ("call", "call_indirect", "jmp_indirect"):
                expected_claim_sites.add(ins.va)
            elif (
                ins.kind == "jmp"
                and ins.target is not None
                and not (span.start_va <= ins.target < span.end_va)
            ):
                expected_claim_sites.add(ins.va)
        emitted_claim_sites = {event.site_va for event in events}
        missing_claim_sites = expected_claim_sites - emitted_claim_sites
        if missing_claim_sites:
            raise ExtractionError(
                "unclassified call/jump sites at 0x%08X: %s"
                % (
                    va,
                    ",".join("0x%08X" % site for site in sorted(missing_claim_sites)),
                )
            )
        expected_direct = Counter(
            "W" if ins.target == WRITE_VA else "R"
            for ins in decoded.instructions.values()
            if ins.kind == "call"
            and ins.target in (WRITE_VA, READ_VA)
            and ("W" if ins.target == WRITE_VA else "R") in allowed
            and (
                formal_stream_offset is None
                or self._formal_offsets(
                    va, ins.va, Operand("reg", reg="ecx")
                )
                == frozenset((formal_stream_offset,))
            )
        )
        emitted_direct = Counter(
            direction
            for event in events
            if numeric_re.fullmatch(event.tag)
            for direction in event.directions
        )
        if emitted_direct != expected_direct:
            raise ExtractionError(
                "recursive primitive coverage mismatch at 0x%08X: expected %r got %r"
                % (va, expected_direct, emitted_direct)
            )
        return tuple(sorted(events, key=lambda event: (event.site_va, event.tag)))


def flatten_events(
    message: str, events: tuple[WireEvent, ...], image: Image
) -> list[FieldRow]:
    counters = {"W": 0, "R": 0}
    rows = []

    def visit(items: tuple[WireEvent, ...], allowed: frozenset[str]) -> None:
        for event in items:
            directions = [d for d in event.directions if d in allowed]
            for direction in directions:
                counters[direction] += 1
                if event.field_expr is not None:
                    field = field_offset_from_expr(event.field_expr)
                elif event.reason:
                    field = "UNKNOWN(%s)" % event.reason
                else:
                    field = "N/A"
                rows.append(
                    FieldRow(
                        message=message,
                        direction=direction,
                        order=counters[direction],
                        tag=event.tag,
                        field_offset=field,
                        length=event.length,
                        gate_condition=event.gate_condition,
                        span_start=event.span.start_va,
                        span_end=event.span.end_va,
                        span_sha256=event.span.sha256,
                        file_off_claim=image.va_to_off(event.site_va),
                        reason=event.reason,
                    )
                )
            if event.children:
                visit(event.children, frozenset(directions))

    visit(events, frozenset(("W", "R")))
    return rows


def build_field_rows(
    registry: list[RegistryRow], analyzer: SerializerAnalyzer
) -> list[FieldRow]:
    rows = []
    for item in registry:
        if item.serializer_va is None:
            for direction in ("W", "R"):
                rows.append(
                    FieldRow(
                        message=item.name,
                        direction=direction,
                        order=1,
                        tag="UNKNOWN",
                        field_offset="UNKNOWN(registry_serializer_unresolved:%s)"
                        % (item.reason or "no_serializer"),
                        length="N/A",
                        gate_condition="ALWAYS",
                        span_start=None,
                        span_end=None,
                        span_sha256="UNKNOWN",
                        file_off_claim=item.file_off_reg,
                        reason="registry_serializer_unresolved:%s"
                        % (item.reason or "no_serializer"),
                    )
                )
            continue
        events = analyzer.extract_events(item.serializer_va)
        rows.extend(flatten_events(item.name, events, analyzer.image))
    return rows


def hex_or_unknown(value: int | None) -> str:
    return "UNKNOWN" if value is None else "0x%08X" % value


def file_offs_or_unknown(values: Iterable[int]) -> str:
    measured = tuple(values)
    return "UNKNOWN" if not measured else "|".join("0x%08X" % value for value in measured)


def find_all(data: bytes, needle: bytes, start: int = 0, end: int | None = None) -> Iterator[int]:
    if end is None:
        end = len(data)
    cursor = start
    while True:
        off = data.find(needle, cursor, end)
        if off < 0:
            return
        yield off
        cursor = off + 1


def rel32_target(instruction_va: int, rel32: int) -> int:
    return (instruction_va + 5 + rel32) & 0xFFFFFFFF


def _rtti_vtable_name_proof(
    image: Image, name: str, vtable_va: int
) -> str | None:
    """Prove one primary x86 MSVC vftable by its exact RTTI class name.

    This is only an ambiguity escape hatch after the task-pinned getter/marker
    sweep has already produced a candidate.  It accepts a primary Complete
    Object Locator, a structurally mapped hierarchy, and a self base descriptor
    whose TypeDescriptor name is exactly ``.?AV<registry-name>@@``.  String
    proximity and partial-name matching are deliberately absent.
    """
    table_record_off = image.va_range_to_off(vtable_va - 4, 0x24)
    if table_record_off is None:
        return None
    locator_pointer_off = table_record_off
    vtable_off = table_record_off + 4
    locator_va = image.u32_off(locator_pointer_off)
    locator_off = image.va_range_to_off(locator_va, 20)
    if locator_off is None:
        return None
    signature, object_offset, constructor_offset = struct.unpack_from(
        "<III", image.data, locator_off
    )
    if (signature, object_offset, constructor_offset) != (0, 0, 0):
        return None
    type_descriptor_va, hierarchy_va = struct.unpack_from(
        "<II", image.data, locator_off + 12
    )
    expected_name = ".?AV%s@@" % name
    expected_name_bytes = expected_name.encode("ascii") + b"\x00"
    type_descriptor_off = image.va_range_to_off(
        type_descriptor_va, 8 + len(expected_name_bytes)
    )
    hierarchy_off = image.va_range_to_off(hierarchy_va, 16)
    if type_descriptor_off is None or hierarchy_off is None:
        return None
    type_info_vtable_va, spare = struct.unpack_from(
        "<II", image.data, type_descriptor_off
    )
    if image.va_range_to_off(type_info_vtable_va, 4) is None or spare != 0:
        return None
    if (
        image.data[
            type_descriptor_off + 8 : type_descriptor_off
            + 8
            + len(expected_name_bytes)
        ]
        != expected_name_bytes
    ):
        return None
    hierarchy_signature, _attributes, base_count, base_array_va = (
        struct.unpack_from("<IIII", image.data, hierarchy_off)
    )
    if hierarchy_signature != 0 or not (1 <= base_count <= 64):
        return None
    base_array_off = image.va_range_to_off(base_array_va, base_count * 4)
    if base_array_off is None:
        return None
    base_descriptor_vas = struct.unpack_from(
        "<%dI" % base_count, image.data, base_array_off
    )
    base_descriptor_offs = tuple(
        image.va_range_to_off(value, 28) for value in base_descriptor_vas
    )
    if any(value is None for value in base_descriptor_offs):
        return None
    self_base_va = base_descriptor_vas[0]
    self_base_off = base_descriptor_offs[0]
    assert self_base_off is not None
    self_type_va, contained_bases = struct.unpack_from(
        "<II", image.data, self_base_off
    )
    self_hierarchy_va = image.u32_off(self_base_off + 24)
    if (
        self_type_va != type_descriptor_va
        or contained_bases >= base_count
        or self_hierarchy_va != hierarchy_va
    ):
        return None
    return (
        "rtti_vtable_name_match vtable=0x%08X file_off=0x%08X "
        "locator_pointer_file_off=0x%08X locator=0x%08X "
        "locator_file_off=0x%08X type_descriptor=0x%08X "
        "type_descriptor_file_off=0x%08X type_name_file_off=0x%08X "
        "hierarchy=0x%08X hierarchy_file_off=0x%08X "
        "base_array=0x%08X base_array_file_off=0x%08X "
        "self_base=0x%08X self_base_file_off=0x%08X "
        "basis=exact_primary_msvc_x86_col_and_full_class_name"
        % (
            vtable_va,
            vtable_off,
            locator_pointer_off,
            locator_va,
            locator_off,
            type_descriptor_va,
            type_descriptor_off,
            type_descriptor_off + 8,
            hierarchy_va,
            hierarchy_off,
            base_array_va,
            base_array_off,
            self_base_va,
            self_base_off,
        )
    )


def _vtable_getter_pointer_offsets(data_size: int) -> range:
    """Cover every aligned pointer with 16 bytes before and after it."""
    return range(16, data_size - 15, 4)


def _vtable_candidates_for_getter(
    image: Image, getter_va: int
) -> tuple[tuple[int, int], ...]:
    candidates = []
    for pointer_off in _vtable_getter_pointer_offsets(len(image.data)):
        if image.u32_off(pointer_off) != getter_va:
            continue
        if image.u32_off(pointer_off - 8) != VTABLE_MARKER_VA:
            continue
        vtable_off = pointer_off - 16
        vtable_va = image.off_to_va(vtable_off)
        if (
            vtable_va is not None
            and image.va_range_to_off(vtable_va, 0x20) == vtable_off
        ):
            candidates.append((vtable_va, pointer_off))
    return tuple(candidates)


def _validate_eof_vtable_candidate_boundary(image: Image) -> None:
    """Inject one mapped record ending at EOF and require the sweep to see it."""
    getter_va = 0x0046B4A0
    vtable_off = len(image.data) - 0x20
    getter_pointer_off = len(image.data) - 0x10
    vtable_va = image.off_to_va(vtable_off)
    if (
        vtable_va is None
        or image.va_range_to_off(vtable_va, 0x20) != vtable_off
        or getter_pointer_off != len(image.data) - 16
    ):
        raise ExtractionError("A1 EOF vtable mutation range mismatch")
    record = bytearray(0x20)
    struct.pack_into("<I", record, 0x08, VTABLE_MARKER_VA)
    struct.pack_into("<I", record, 0x10, getter_va)
    struct.pack_into("<I", record, 0x18, 0x0043BB80)
    struct.pack_into("<I", record, 0x1C, 0x0046B530)
    mutated_data = bytearray(image.data)
    mutated_data[vtable_off:] = record
    mutated_image = object.__new__(Image)
    mutated_image.data = bytes(mutated_data)
    mutated_image.sections = image.sections
    expected = _vtable_candidates_for_getter(image, getter_va) + (
        (vtable_va, getter_pointer_off),
    )
    if _vtable_candidates_for_getter(mutated_image, getter_va) != expected:
        raise ExtractionError("A1 EOF vtable candidate was not censused")


def _candidate_invariant_executable_slot(
    image: Image,
    candidates: Iterable[tuple[int, int]],
    slot_delta: int,
    label: str,
) -> tuple[int, tuple[int, ...], str] | None:
    """Prove one slot value shared by the complete ambiguous candidate set."""
    measured = tuple(
        (vtable_va, pointer_off + slot_delta, image.u32_off(pointer_off + slot_delta))
        for vtable_va, pointer_off in candidates
    )
    values = {value for _vtable_va, _pointer_off, value in measured}
    if len(measured) < 2 or len(values) != 1:
        return None
    value = next(iter(values))
    if not image.executable_va(value):
        return None
    pointer_offs = tuple(pointer_off for _vtable_va, pointer_off, _value in measured)
    proof = (
        "candidate_invariant_%s candidate_count=%d vtables=%s "
        "pointer_file_offs=%s value=0x%08X "
        "basis=complete_same_section_getter_marker_census"
        % (
            label,
            len(measured),
            "|".join("0x%08X" % vtable_va for vtable_va, _off, _value in measured),
            "|".join("0x%08X" % pointer_off for _va, pointer_off, _value in measured),
            value,
        )
    )
    return value, pointer_offs, proof


def scan_registry(image: Image) -> list[RegistryRow]:
    data = image.data
    text = image.section(".text")
    preliminary = []
    for off in find_all(data, b"\x68", text.raw_ptr, text.raw_end):
        if off + 24 > text.raw_end:
            continue
        if data[off + 5] != 0xE8 or data[off + 10 : off + 12] != b"\x8b\xc8":
            continue
        if data[off + 12] != 0xE8 or data[off + 17 : off + 19] != b"\x66\xa3":
            continue
        if data[off + 23] != 0xC3:
            continue
        site_va = image.off_to_va(off)
        if site_va is None:
            continue
        call1 = rel32_target(site_va + 5, struct.unpack_from("<i", data, off + 6)[0])
        call2 = rel32_target(site_va + 12, struct.unpack_from("<i", data, off + 13)[0])
        if call1 != ONCE_INIT_VA or call2 != ID_ASSIGN_VA:
            continue
        name_va = struct.unpack_from("<I", data, off + 1)[0]
        slot_va = struct.unpack_from("<I", data, off + 19)[0]
        name = image.read_cstring(name_va)
        if not name or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ExtractionError(
                "registration at 0x%08X has unreadable/non-identifier literal 0x%08X"
                % (site_va, name_va)
            )
        preliminary.append((name, name_va, site_va, slot_va, off))

    getter_by_slot: dict[int, list[int]] = defaultdict(list)
    for off in find_all(data, b"\x66\xa1", text.raw_ptr, text.raw_end):
        if off + 7 <= text.raw_end and data[off + 6] == 0xC3:
            slot_va = struct.unpack_from("<I", data, off + 2)[0]
            getter_va = image.off_to_va(off)
            if getter_va is not None:
                getter_by_slot[slot_va].append(getter_va)

    wanted_getters = {
        getter
        for slot_va in {item[3] for item in preliminary}
        for getter in getter_by_slot.get(slot_va, [])
    }
    vtable_by_getter: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for pointer_off in _vtable_getter_pointer_offsets(len(data)):
        getter_va = image.u32_off(pointer_off)
        if getter_va not in wanted_getters:
            continue
        if image.u32_off(pointer_off - 8) != VTABLE_MARKER_VA:
            continue
        vtable_off = pointer_off - 16
        vtable_va = image.off_to_va(vtable_off)
        if (
            vtable_va is not None
            and image.va_range_to_off(vtable_va, 0x20) == vtable_off
        ):
            vtable_by_getter[getter_va].append((vtable_va, pointer_off))

    rows = []
    for name, name_va, site_va, slot_va, reg_off in preliminary:
        getter_hits = getter_by_slot.get(slot_va, [])
        getter_va = getter_hits[0] if len(getter_hits) == 1 else None
        vtable_hits = vtable_by_getter.get(getter_va, []) if getter_va is not None else []
        reason_parts = []
        resolution_proof = ""
        serializer_pointer_offs: tuple[int, ...] = ()
        handler_pointer_offs: tuple[int, ...] = ()
        serializer_resolution_proof = ""
        handler_resolution_proof = ""
        unresolved_candidates: tuple[tuple[int, int], ...] = ()
        if len(getter_hits) != 1:
            reason_parts.append("getter_hits=%d" % len(getter_hits))
        if len(vtable_hits) == 1:
            vtable_va, pointer_off = vtable_hits[0]
        elif len(vtable_hits) > 1:
            rtti_hits = [
                (vtable_va, pointer_off, proof)
                for vtable_va, pointer_off in vtable_hits
                for proof in (
                    _rtti_vtable_name_proof(image, name, vtable_va),
                )
                if proof is not None
            ]
            if len(rtti_hits) == 1:
                vtable_va, pointer_off, resolution_proof = rtti_hits[0]
            else:
                vtable_va = pointer_off = None
                unresolved_candidates = tuple(vtable_hits)
                reason_parts.append("vtable_hits=%d" % len(vtable_hits))
                if rtti_hits:
                    reason_parts.append("rtti_name_hits=%d" % len(rtti_hits))
        else:
            vtable_va = pointer_off = None
            if getter_va is not None:
                reason_parts.append("vtable_hits=0")
        if pointer_off is not None:
            serializer_pointer_offs = (pointer_off + 8,)
            handler_pointer_offs = (pointer_off + 12,)
            serializer_va = image.u32_off(pointer_off + 8)
            handler_va = image.u32_off(pointer_off + 12)
            if not image.executable_va(serializer_va):
                reason_parts.append("serializer_not_executable")
                serializer_va = None
            if not image.executable_va(handler_va):
                reason_parts.append("handler_not_executable")
                handler_va = None
        else:
            vtable_va = serializer_va = handler_va = None
            if unresolved_candidates:
                serializer_pointer_offs = tuple(
                    candidate_pointer_off + 8
                    for _candidate_vtable_va, candidate_pointer_off
                    in unresolved_candidates
                )
                handler_pointer_offs = tuple(
                    candidate_pointer_off + 12
                    for _candidate_vtable_va, candidate_pointer_off
                    in unresolved_candidates
                )
                serializer_invariant = _candidate_invariant_executable_slot(
                    image, unresolved_candidates, 8, "serializer"
                )
                handler_invariant = _candidate_invariant_executable_slot(
                    image, unresolved_candidates, 12, "handler"
                )
                if serializer_invariant is not None:
                    (
                        serializer_va,
                        serializer_pointer_offs,
                        serializer_resolution_proof,
                    ) = serializer_invariant
                if handler_invariant is not None:
                    (
                        handler_va,
                        handler_pointer_offs,
                        handler_resolution_proof,
                    ) = handler_invariant
        rows.append(
            RegistryRow(
                name=name,
                name_va=name_va,
                reg_site_va=site_va,
                id_global_va=slot_va,
                getter_va=getter_va,
                vtable_va=vtable_va,
                serializer_va=serializer_va,
                handler_va=handler_va,
                file_off_reg=reg_off,
                reason=";".join(reason_parts),
                resolution_proof=resolution_proof,
                serializer_pointer_offs=serializer_pointer_offs,
                handler_pointer_offs=handler_pointer_offs,
                serializer_resolution_proof=serializer_resolution_proof,
                handler_resolution_proof=handler_resolution_proof,
            )
        )

    rows.sort(key=lambda row: row.reg_site_va)
    return rows


def format_tsv(header: list[str], rows: Iterable[Iterable[str]]) -> str:
    out = io.StringIO(newline="")
    writer = csv.writer(out, dialect="excel-tab", lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return out.getvalue()


def validate_tsv_source_contract(
    artifact_name: str,
    text: str,
    expected_rows: int,
    expected_source: str,
) -> None:
    if expected_source not in EVIDENCE_SOURCES:
        raise ExtractionError(
            "%s source contract has invalid expected source" % artifact_name
        )
    reader = csv.DictReader(io.StringIO(text), dialect="excel-tab")
    if reader.fieldnames is None or reader.fieldnames.count("source") != 1:
        raise ExtractionError(
            "%s source column is missing or duplicated" % artifact_name
        )
    rows = list(reader)
    if len(rows) != expected_rows:
        raise ExtractionError(
            "%s source contract row count mismatch" % artifact_name
        )
    measured = {row.get("source", "") for row in rows}
    if not measured <= EVIDENCE_SOURCES:
        raise ExtractionError(
            "%s source column contains a value outside the evidence enum"
            % artifact_name
        )
    if measured != {expected_source}:
        raise ExtractionError(
            "%s mixes evidence layers: expected %s, got %s"
            % (artifact_name, expected_source, ",".join(sorted(measured)))
        )


def validate_source_contract_mutation_regressions(
    artifacts: tuple[tuple[str, str, int], ...],
) -> None:
    for artifact_name, text, expected_rows in artifacts:
        lines = text.splitlines()
        if len(lines) != expected_rows + 1 or not lines[0].endswith("\tsource"):
            raise ExtractionError(
                "%s source mutation fixture shape mismatch" % artifact_name
            )
        mutations = (
            "\n".join(
                [lines[0].rsplit("\t", 1)[0]]
                + [line.rsplit("\t", 1)[0] for line in lines[1:]]
            )
            + "\n",
            text.replace("\tIMAGE\n", "\tDUMP\n", 1),
            text.replace("\tIMAGE\n", "\tOTHER\n", 1),
        )
        for mutated in mutations:
            try:
                validate_tsv_source_contract(
                    artifact_name,
                    mutated,
                    expected_rows,
                    STATIC_EVIDENCE_SOURCE,
                )
            except ExtractionError:
                pass
            else:
                raise ExtractionError(
                    "%s source mutation was unexpectedly accepted"
                    % artifact_name
                )


def build_registry_tsv(rows: list[RegistryRow], image: Image) -> str:
    return format_tsv(
        [
            "name",
            "name_va",
            "reg_site_va",
            "id_global_va",
            "getter_va",
            "vtable_va",
            "serializer_va",
            "handler_va",
            "file_off_reg",
            "file_off_name",
            "file_off_getter",
            "file_off_vtable",
            "file_off_serializer_ptr",
            "file_off_handler_ptr",
            "source",
        ],
        (
            [
                row.name,
                "0x%08X" % row.name_va,
                "0x%08X" % row.reg_site_va,
                "0x%08X" % row.id_global_va,
                hex_or_unknown(row.getter_va),
                hex_or_unknown(row.vtable_va),
                hex_or_unknown(row.serializer_va),
                hex_or_unknown(row.handler_va),
                "0x%08X" % row.file_off_reg,
                hex_or_unknown(image.va_to_off(row.name_va)),
                hex_or_unknown(
                    None if row.getter_va is None else image.va_to_off(row.getter_va)
                ),
                hex_or_unknown(
                    None if row.vtable_va is None else image.va_to_off(row.vtable_va)
                ),
                file_offs_or_unknown(row.serializer_pointer_offs),
                file_offs_or_unknown(row.handler_pointer_offs),
                STATIC_EVIDENCE_SOURCE,
            ]
            for row in rows
        ),
    )


def build_registry_md(rows: list[RegistryRow], image: Image) -> str:
    getter_unknown = sum(row.getter_va is None for row in rows)
    vtable_unknown = sum(row.vtable_va is None for row in rows)
    serializer_unknown = sum(row.serializer_va is None for row in rows)
    handler_unknown = sum(row.handler_va is None for row in rows)
    reasons = Counter(row.reason for row in rows if row.reason)
    rtti_resolved = [row for row in rows if row.resolution_proof]
    serializer_invariant = [
        row for row in rows if row.serializer_resolution_proof
    ]
    handler_invariant = [row for row in rows if row.handler_resolution_proof]
    lines = [
        "# PF protocol registry",
        "",
        "ไฟล์นี้สร้างจาก `GameClient.local.bin` โดย `pf_extract_protocol.py` แบบอ่านอย่างเดียว",
        "และไม่ใช้ความใกล้กันของสตริงกับ vtable เป็นหลักฐาน; ทุกแถว TSV ติด `source=IMAGE`",
        "",
        "## วิธีวัด",
        "",
        "- สแกนเฉพาะ `.text` ด้วยรูป 24 ไบต์ `push literal; call 0x89C080; mov ecx,eax; call 0x89BD00; mov word [slot],ax; ret`.",
        "- หา getter จากไบต์ 7 ไบต์ `66 A1 <slot> C3`.",
        "- sweep dword ทั้งไฟล์หา getter และรับ vtable เฉพาะเมื่อ marker ที่ `+0x08` เป็น `0x00401B20` และ getter อยู่ที่ `+0x10`.",
        "- ถ้า getter/marker ให้ vtable หลาย candidate ใช้ RTTI เป็น escape hatch เฉพาะ candidate เดียวที่ `vtable[-4]` ชี้ primary x86 MSVC Complete Object Locator แบบครบโครงสร้าง, ทุกช่วงไบต์ที่อ่านอยู่ครบภายใน PE section เดียว, self BaseClassDescriptor ย้อนกลับ TypeDescriptor เดิม และชื่อเต็มตรง `.?AV<registry-name>@@` ทุกตัวอักษร; ไม่ใช้ชื่อใกล้เคียงหรือระยะห่างของสตริง.",
        "- ถ้า vtable ยังแยกไม่ได้ จะคง vtable เป็น `UNKNOWN`; serializer หรือ handler แยกเป็นค่าที่พิสูจน์ได้เฉพาะเมื่อ slot นั้นมี executable VA ค่าเดียวกันใน candidate getter/marker ครบทั้ง census และ table 0x20 ไบต์ของทุก candidate อยู่ครบใน PE section เดียว โดยบันทึก pointer file offset ทุก candidate.",
        "- อ่าน serializer และ handler จาก `+0x18` และ `+0x1C`; ช่องที่ไม่เป็น executable VA หรือไม่เอกฐานเป็น `UNKNOWN`.",
        "- คอลัมน์ `file_off_*` ระบุตำแหน่งไบต์ของ registration, name, getter, vtable และ pointer slots เพื่อให้ตรวจทุกข้ออ้างจาก image ได้ตรงจุด; หลาย offset ในหนึ่งช่องคั่นด้วย `|`.",
        "",
        "## จำนวน",
        "",
        "- protocol: %d" % len(rows),
        "- getter UNKNOWN: %d" % getter_unknown,
        "- vtable UNKNOWN: %d" % vtable_unknown,
        "- serializer UNKNOWN: %d" % serializer_unknown,
        "- handler UNKNOWN: %d" % handler_unknown,
        "- exact RTTI vtable disambiguation: %d" % len(rtti_resolved),
        "- candidate-invariant serializer: %d" % len(serializer_invariant),
        "- candidate-invariant handler: %d" % len(handler_invariant),
        "- image SHA-256: `%s`" % image.sha256,
    ]
    if rtti_resolved:
        lines.extend(["", "## หลักฐาน RTTI ที่ใช้แก้ความกำกวม", ""])
        for row in rtti_resolved:
            lines.append("- `%s`: `%s`" % (row.name, row.resolution_proof))
    if serializer_invariant or handler_invariant:
        lines.extend(["", "## หลักฐานค่าคงที่ข้าม vtable candidate", ""])
        for row in serializer_invariant:
            lines.append(
                "- `%s` serializer: `%s`"
                % (row.name, row.serializer_resolution_proof)
            )
        for row in handler_invariant:
            lines.append(
                "- `%s` handler: `%s`"
                % (row.name, row.handler_resolution_proof)
            )
    if reasons:
        lines.extend(["", "## เหตุผล UNKNOWN", ""])
        for reason, count in sorted(reasons.items()):
            lines.append("- `%s`: %d" % (reason, count))
    lines.append("")
    return "\n".join(lines)


def build_fields_tsv(rows: list[FieldRow]) -> str:
    return format_tsv(
        [
            "message",
            "direction(W/R)",
            "order",
            "tag",
            "field_offset",
            "len",
            "gate_condition",
            "span_start",
            "span_end",
            "span_sha256",
            "file_off_claim",
            "source",
        ],
        (
            [
                row.message,
                row.direction,
                str(row.order),
                row.tag,
                row.field_offset,
                row.length,
                row.gate_condition,
                hex_or_unknown(row.span_start),
                hex_or_unknown(row.span_end),
                row.span_sha256,
                hex_or_unknown(row.file_off_claim),
                STATIC_EVIDENCE_SOURCE,
            ]
            for row in rows
        ),
    )


def unknown_summary(rows: list[FieldRow]) -> tuple[set[str], Counter[str]]:
    message_reasons: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row.reason:
            message_reasons[row.message].add(row.reason)
    counts: Counter[str] = Counter()
    for reasons in message_reasons.values():
        counts.update(reasons)
    return set(message_reasons), counts


def local_direction_proof_segment(row: FieldRow) -> str | None:
    if row.file_off_claim is None:
        return None
    prefix = "direction_call@0x"
    offset_fragment = " file_off=0x%08X " % row.file_off_claim
    for segment in row.gate_condition.split(" AND "):
        site_text = segment[len(prefix) : len(prefix) + 8]
        if (
            segment.startswith(prefix)
            and len(site_text) == 8
            and all(character in "0123456789ABCDEF" for character in site_text)
            and segment.startswith(offset_fragment, len(prefix) + 8)
        ):
            return segment
    return None


def has_local_direction_proof(row: FieldRow) -> bool:
    return local_direction_proof_segment(row) is not None


def has_local_formal_forward_proof(row: FieldRow) -> bool:
    segment = local_direction_proof_segment(row)
    return segment is not None and "value=formal_forward" in segment


def has_local_stream_proof(row: FieldRow) -> bool:
    if row.file_off_claim is None:
        return False
    return bool(
        re.search(
            r"stream_(?:call|tail)@0x[0-9A-F]{8} "
            r"file_off=0x%08X(?: |$)" % row.file_off_claim,
            row.gate_condition,
        )
    )


def build_fields_md(
    registry: list[RegistryRow], rows: list[FieldRow], image: Image
) -> str:
    unknown_messages, reasons = unknown_summary(rows)
    successful = len(registry) - len(unknown_messages)
    numeric = sum(
        bool(re.fullmatch(r"0x[0-9A-F]{2}", row.tag))
        and row.direction in ("W", "R")
        for row in rows
    )
    subcalls = sum(row.tag.startswith("SUBCALL:") for row in rows)
    unclassified_calls = sum(
        row.tag.startswith(("CALL_UNCLASSIFIED:", "JUMP_UNCLASSIFIED:"))
        for row in rows
    )
    string_helper_rows = sum(
        row.tag in {spec.tag for spec in STRING_WIRE_HELPERS.values()}
        for row in rows
    )
    atomic_increment_unknown_rows = sum(
        row.tag == ATOMIC_OBJECT_HELPERS[0x0088D050].tag for row in rows
    )
    atomic_dynamic_rows = sum(
        row.tag == ATOMIC_OBJECT_HELPERS[0x0088D060].tag for row in rows
    )
    atomic_pointer_rows = sum(
        row.tag
        in {
            ATOMIC_OBJECT_HELPERS[0x004A06A0].tag,
            ATOMIC_OBJECT_HELPERS[0x004A06B0].tag,
        }
        for row in rows
    )
    pure_chain_rows = sum(
        row.tag == PURE_CHAIN_HELPERS[0x0088F2B0].tag for row in rows
    )
    mutable_chain_rows = sum(
        row.tag == MUTABLE_CHAIN_HELPERS[0x00B0BF70].tag for row in rows
    )
    locked_mutable_pointer_slot_rows = sum(
        row.tag
        == LOCKED_MUTABLE_POINTER_SLOT_HELPERS[0x0066AB90].tag
        for row in rows
    )
    critical_section_pointer_rows = sum(
        row.tag in {spec.tag for spec in CRITICAL_SECTION_POINTER_HELPERS.values()}
        for row in rows
    )
    locked_mutable_dword_slot_update_rows = sum(
        row.tag
        == LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS[0x00710FA0].tag
        for row in rows
    )
    nested_call_composition_rows = sum(
        row.tag == "NESTED_THREE_CALL_COMPOSITION_HELPER"
        for row in rows
    )
    ecx_plus_50_tail_jump_rows = sum(
        row.tag == "ECX_PLUS_50_TAIL_JUMP_HELPER" for row in rows
    )
    mutable_pointer_slot_traversal_rows = sum(
        row.tag
        == MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS[0x0046D2B0].tag
        for row in rows
    )
    mutable_dword_slot_operation_rows = sum(
        row.tag
        == MUTABLE_DWORD_SLOT_OPERATION_HELPERS[0x00AC6E80].tag
        for row in rows
    )
    mutable_dword_range_growth_rows = sum(
        row.tag == MUTABLE_DWORD_RANGE_GROWTH_HELPERS[0x007016A0].tag
        for row in rows
    )
    exact_direct_import_call_rows = sum(
        row.tag == EXACT_DIRECT_IMPORT_CALLS[0x00C3B4C0].tag
        for row in rows
    )
    other_exact_direct_import_call_rows = sum(
        row.tag
        in {
            EXACT_DIRECT_IMPORT_CALLS[iat_va].tag
            for iat_va in OTHER_EXACT_DIRECT_IMPORT_CALL_IATS
        }
        for row in rows
    )
    exact_import_thunk_call_rows = sum(
        row.tag in {spec.tag for spec in EXACT_IMPORT_THUNK_CALLS.values()}
        for row in rows
    )
    pe_security_cookie_check_rows = sum(
        row.tag
        in {spec.tag for spec in PE_SECURITY_COOKIE_CHECK_HELPERS.values()}
        for row in rows
    )
    exact_singleton_register_import_call_rows = sum(
        row.tag
        in {
            spec.tag
            for spec in EXACT_SINGLETON_REGISTER_IMPORT_CALLS.values()
        }
        for row in rows
    )
    exact_multi_register_import_call_rows = sum(
        row.tag
        in {spec.tag for spec in EXACT_MULTI_REGISTER_IMPORT_CALLS.values()}
        for row in rows
    )
    direction_proven_subcalls = sum(
        row.tag.startswith("SUBCALL:")
        and has_local_direction_proof(row)
        for row in rows
    )
    formal_forward_subcalls = sum(
        row.tag.startswith("SUBCALL:")
        and has_local_formal_forward_proof(row)
        for row in rows
    )
    stream_proven_subcalls = sum(
        row.tag.startswith("SUBCALL:0x") and has_local_stream_proof(row)
        for row in rows
    )
    stream_unresolved = sum(
        "stream_provenance_unresolved" in row.reason for row in rows
    )
    register_neutral_import_rows = sum(
        "stack_neutral_register_import@" in row.gate_condition
        for row in rows
    )
    neutral_import_rows = sum(
        "stack_neutral_import@" in row.gate_condition
        or "stack_neutral_register_import@" in row.gate_condition
        for row in rows
    )
    stack_identity_rows = sum(
        "stack_identity_lea@" in row.gate_condition for row in rows
    )
    getid_stack_rows = sum(
        "stack_neutral_vtable_getid@" in row.gate_condition
        for row in rows
    )
    indirect_formal_rows = sum(
        "indirect_mode_formal_source " in row.gate_condition
        for row in rows
    )
    local_capability_rows = sum(
        "local_capability_refinement" in row.gate_condition for row in rows
    )
    identity_zero_rows = sum(
        "mode_zero_identity_lea" in row.gate_condition for row in rows
    )
    gates = sum(row.gate_condition != "ALWAYS" for row in rows)
    lines = [
        "# PF serializer fields",
        "",
        "ตารางนี้สร้างจาก control-flow และ call-site ใน image ที่ตรึง hash แล้ว โดยไม่ใช้ตารางฟิลด์เดิมเป็นข้อมูลนำเข้า; ทุกแถว TSV ติด `source=IMAGE`",
        "",
        "## กติกาการวัด",
        "",
        "- ขอบเขตฟังก์ชันเป็น `[span_start, span_end)` จบที่ `ret`/`ret imm` ตัวแรกซึ่งตามด้วย `INT3` อย่างน้อย 3 ไบต์; SHA-256 ครอบคลุมช่วงนั้นพอดี",
        "- แถว tag ตัวเลขมาจาก call ไป `WRITE 0x0089A600` หรือ `READ 0x0089A640` และรับเฉพาะลำดับ push ที่พิสูจน์ได้เอกฐานเป็น `len, pointer, tag`",
        "- ตัวช่วยข้อความรับเฉพาะสี่ target ที่ตรึงครบทั้งช่วงไบต์/แฮช, ABI `thiscall` หนึ่งอาร์กิวเมนต์, import symbol จาก PE, direct thunk `0x00B37B80 -> [0x00C3B504] memcpy` และ semantic key bytes: `0x0089A6D0`/`0x0089A740` เป็น `basic_string<char>` W/R และ `0x0089A810`/`0x0089A880` เป็น `basic_string<wchar_t>` W/R; ทุกกรณีใช้ความยาว 32-bit little-endian ซึ่งนับ payload เป็นไบต์ ตามด้วย raw N bytes และยอมรับ call site เฉพาะเมื่อ ECX ย้อนถึง stream formal เอกฐาน",
        "- atomic object helper รับเฉพาะ full body ตรงทุกไบต์และ PE import ตรงชื่อ: `0x0088D050` พิสูจน์ exact `InterlockedIncrement(ECX+0x0C)` แล้ว return แต่ runtime address ยังผูก object/non-alias กับ stream ไม่ได้ จึงคง `atomic_target_object_alias_unproved`; `0x0088D060` ทำ `InterlockedDecrement(ECX+0x0C)` แล้วเมื่อผลเป็นศูนย์อาจ call runtime target จาก vtable `+0x04` จึงคง `dynamic_vtable_plus_0x04_target_unresolved` และไม่เดา target ทั้งสองกรณี",
        "- direct atomic pointer helpers `0x004A06A0`/`0x004A06B0` รับเฉพาะ body 8 ไบต์ที่เป็น `push ECX; call [InterlockedIncrement/Decrement]; ret` และ PE import ตรงชื่อ; ECX runtime pointer ยังไม่มี non-alias proof จึงคง `atomic_target_pointer_alias_unproved` ทุก call โดยไม่เรียกเป็น refcount หรือ non-wire",
        "- pure chain predicate `0x0088F2B0` รับเฉพาะ full body 33 ไบต์ตรง hash: อ่าน needle จาก stack `+0x04`, chain head จาก `+0x08`, เดิน pointer ที่ node `+0x04` จนเท่ากันหรือเป็น null แล้วคืน AL 1/0; body ไม่มี call และไม่มี memory write ส่วน caller 34 จุดต้องมี exact suffix `movzx eax,al; add esp,8` จึงบันทึกเป็น read-only predicate ที่ไม่สร้าง wire field โดยไม่ตั้งชื่อชนิด node/container",
        "- mutable chain helper `0x00B0BF70` รับ full body 108 ไบต์และ PE import `_invalid_parameter_noinfo` ตรง exact; body อ่าน link/flag ที่ `+0x00/+0x04/+0x08/+0x15` และมี memory write `[ESI+0x04]` ตรงสามจุด แต่ 22 caller sites ยังไม่มี object/non-alias provenance จึงคง `mutable_chain_target_object_alias_unproved` และไม่อ้างว่าเป็น non-wire หรือระบุชนิด container",
        "- locked mutable pointer-slot helper `0x0066AB90` รับ full body 157 ไบต์, direct import `malloc`/`_invalid_parameter_noinfo`, exact wrappers ของ `EnterCriticalSection`/`LeaveCriticalSection`/`InterlockedExchangeAdd` และจุดเขียน slot scale 4 ครบ; nested target `0x007016A0` กับ runtime object/source alias ยังไม่พิสูจน์ semantics เอกฐาน จึงคง `locked_mutable_pointer_slot_nested_target_and_alias_unproved` โดยไม่ตั้งชื่อชนิด container และไม่อ้างว่าเป็น non-wire",
        "- critical-section pointer wrappers `0x0088D5B0`/`0x0049DA40` รับเฉพาะ full body 10 ไบต์ที่เป็น `mov eax,[ecx]; push eax; call [Enter/LeaveCriticalSection]; ret` และ PE import ตรงชื่อ; runtime pointer ที่ `[ECX]` ยังไม่มี non-alias proof จึงคง `critical_section_pointer_alias_unproved` โดยไม่อ้างว่า call เป็น non-wire",
        "- locked mutable dword-slot update helper `0x00710FA0` รับ bounded entry CFG `[0x00710FA0,0x0071100F)` 111 ไบต์/42 instructions ตรง hash, เรียก lock/growth/unlock targets ที่พิสูจน์ไว้, direct `_invalid_parameter_noinfo` สองจุด, ปรับ counter `+0x20/+0x24` และเขียน output/slot; nested semantics กับ runtime aliases ยังไม่เอกฐาน จึงคง `locked_mutable_dword_slot_nested_target_and_alias_unproved` โดยไม่ตั้งชื่อ container หรือประกาศ NONWIRE",
        "- nested three-call composition helper `0x005F8DE0` รับ full body `[0x005F8DE0,0x005F8E04)` 36 ไบต์/13 instructions ตรง hash, มี direct calls เอกฐานไป `0x0089C080`/`0x0089B220`/`0x00463800`, zero-extend ผลลัพธ์ และส่ง address `ECX+0x50` ต่อโดยไม่มี explicit MOV ที่ปลายทางเป็น memory ใน body นี้; semantics ของ nested targets กับ runtime alias ยังไม่เอกฐาน จึงคง `nested_call_composition_targets_and_alias_unproved` โดยไม่ตั้งชื่อ operation หรือประกาศ NONWIRE",
        "- ECX+0x50 tail-jump helper `0x005F8C30` รับเฉพาะ entry-reachable prefix `[0x005F8C30,0x005F8C38)` 8 ไบต์/2 instructions ตรง hash: `add ecx,0x50` แล้ว direct tail jump ไป `0x00463800`; prefix ตามด้วย `CC` 8 ไบต์ที่ file offset `0x001F8038` จึงไม่ลาก routine ถัดไปเข้าคำอ้าง ส่วน tail-target semantics กับ runtime ECX alias ยังไม่เอกฐาน จึงคง `ecx_plus_50_tail_target_and_alias_unproved` โดยไม่ตั้งชื่อ operation หรือประกาศ NONWIRE",
        "- mutable pointer-slot traversal helper `0x0046D2B0` รับ full body 108 ไบต์/44 instructions ตรง hash, โหลด `_invalid_parameter_noinfo` IAT เข้า EDI, call EDI สองจุด และเขียน runtime `[ESI+0x04]` สามแขน; ระบุเฉพาะ pointer/link/flag offsets ตามไบต์และคง `mutable_pointer_slot_traversal_alias_unproved` โดยไม่ตั้งชื่อโครงสร้างข้อมูลหรือประกาศ NONWIRE",
        "- mutable dword-slot operation helper `0x00AC6E80` รับ bounded entry CFG `[0x00AC6E80,0x00AC6F00)` 128 ไบต์/53 instructions ตรง hash, ret 4 สองจุด, direct nested targets `0x006B35A0`/`0x00AC6D00`, direct `_invalid_parameter_noinfo` IAT และ state write `[ESI+0x10]=EDI`; nested semantics กับ runtime object/source alias ยังไม่เอกฐาน จึงคง `mutable_dword_slot_nested_targets_and_alias_unproved` โดยไม่ตั้งชื่อ container หรือประกาศ NONWIRE",
        "- mutable dword-range growth helper `0x007016A0` รับ full body 133 ไบต์ตรง exact, เขียนศูนย์ที่ `[EDI]`, เลื่อน end pointer `[ESI+0x10]`, ใช้ slot scale 4 และเรียก `_invalid_parameter_noinfo` ผ่าน register ที่โหลดจาก IAT; nested target `0x005F68D0` กับ runtime object alias ยังไม่พิสูจน์ semantics เอกฐาน จึงคง `mutable_dword_range_nested_target_and_alias_unproved` โดยไม่เรียก vector/list หรือ non-wire",
        "- direct IAT call `FF 15 C0 B4 C3 00` รับเฉพาะเมื่อ PE import table ยืนยัน `MSVCR90.dll!_invalid_parameter_noinfo` พร้อม file offset ของ call/IAT/descriptor/lookup/name ครบ; การรู้ import operation ยังไม่พิสูจน์ผลต่อ wire path จึงคง `invalid_parameter_import_call_wire_effect_unproved` และไม่ประกาศ NONWIRE",
        "- exact direct PE-import อื่นรับเฉพาะ 12 IAT ใน oracle ที่ระบุ DLL, decorated symbol และ `FF15 <IAT little-endian>` ตายตัว; ทุกแถวตรึง call/IAT/descriptor/lookup/name offsets และแยก tag ตาม operation แต่คง `exact_direct_import_call_wire_effect_unproved` โดยไม่อนุมานจากชื่อ import ว่าเป็น NONWIRE",
        "- rel32 import-thunk call รับเฉพาะ target ที่เป็น exact unconditional `FF25 <IAT little-endian>` 6 ไบต์และ PE import table ยืนยัน DLL/symbol ตาม independent oracle; ปัจจุบันคือ `0x0088D020 -> MSVCR90.dll!malloc` และ `0x00B37998 -> MSVCR90.dll!_CxxThrowException`. ทุกแถวตรึง call/target/thunk/IAT/descriptor/lookup/name offsets แต่คง `exact_import_thunk_call_wire_effect_unproved` โดยไม่ประกาศ NONWIRE จากชื่อ import",
        "- PE SecurityCookie helper `0x00B37964` รับ bounded entry `[0x00B37964,0x00B37973)` 15 ไบต์/4 instructions ตรง hash: เทียบ ECX กับ global `0x0102B4BC`, return เมื่อเท่ากัน หรือตรงไป failure target `0x00B38352`; COFF `SizeOfOptionalHeader=0xE0` ที่ file offset `0x0000013C` และ PE32 `NumberOfRvaAndSizes=16` ที่ `0x0000019C` ยืนยันว่า Load Configuration DataDirectory[10] ที่ `0x000001F0` อยู่ใน optional header จริง ก่อนชี้ field `SecurityCookie` ที่ `0x00BBA9AC` เป็น global เดียวกัน และ entry ตามด้วย `CC` 13 ไบต์. failure-path effect ยังไม่เอกฐาน จึงคง `pe_security_cookie_failure_path_wire_effect_unproved` โดยไม่ประกาศ NONWIRE",
        "- register-indirect `_invalid_parameter_noinfo` รับเฉพาะ exact `call r32` ที่มี reaching definition เดียวและ definition นั้นเป็น unprefixed exact `mov r32,[0x00C3B4C0]`; หลักฐานตรึง call/load bytes และ offsets ครบ แต่ยังคง `invalid_parameter_singleton_register_call_wire_effect_unproved` โดยไม่รวม multiple-definition paths",
        "- multi-definition register-indirect `_invalid_parameter_noinfo` ใช้กฎแยก: complete reaching set ต้องมีอย่างน้อยสอง definitions, ไม่มี undefined path และสมาชิกทุกจุดเป็น exact unprefixed `mov r32,[0x00C3B4C0]` ของ register เดียวกัน; ตรึงสมาชิก/bytes/offsets ทุกจุดและคง `invalid_parameter_multi_register_call_wire_effect_unproved`",
        "- ทุกแถวมี `file_off_claim` ของ call/jump/ret/registration ที่รองรับข้ออ้างนั้นโดยตรง; เปิด image ที่ offset นี้เพื่อตรวจไบต์ซ้ำได้",
        "- `gate_condition=ALWAYS` หมายถึงไม่มี immediate-mask gate, mode-direction proof หรือ ancestor SUBCALL path สำหรับแถวนั้น; หลักฐานที่มีจะบันทึก VA และ file offset ทุก anchor/path",
        "- `SUBCALL:0x...` รับเฉพาะ target คงที่ที่ตามถึง WRITE/READ ได้หรือเป็น serializer ใน A1 และพิสูจน์ stream chain เอกฐานจาก caller formal ผ่าน push/tail ไปยัง target formal และ primitive ECX ของทิศนั้น; ถ้า caller ไม่มี direct primitive seed จะย้อนจาก target formal ที่มี direction-specific primitive anchor ผ่าน call argument ได้เฉพาะเมื่อเหลือคู่ caller/target formal เดียว; tail ต้องมี ABI จำกัดช่วง formal และ stack depth ตรง jump เท่ากับศูนย์; แถวถัดไปจึงตามเข้า target",
        "- memory formal ผ่าน frame register รับเฉพาะ full-width `mov reg, esp` ที่มี stack depth เอกฐาน แล้วคำนวณ entry delta ตรงตัว; register copy ต้องเอกฐานทุก predecessor ส่วน arithmetic, LEA, partial write, conflict, missing path และ cycle ยังคง UNKNOWN; `stack_formal_base` บันทึก instruction/file offset ที่เป็นฐาน",
        "- ถ้า recursive backtrace ติด loop จะใช้ forward reaching-definition fixed point เป็น fallback เฉพาะเมื่อทุก CFG path มี plain 32-bit MOV definition เดียวและ source formal เอกฐาน; entry ที่ยังไม่กำหนด, definition หลายตัว, non-MOV/partial write และ opcode `other` นอก safe no-GPR-write families เป็น clobber; `formal_reaching_def` บันทึก definition/use file offsets ทุก claim",
        "- `SUBCALL:INDIRECT(...)` รับเฉพาะรูปโหลด `[vtable+0x18]` ที่โจทย์ตรึงว่าเป็น serializer slot และมีอาร์กิวเมนต์สองตัว; target จริงยัง UNKNOWN; ทิศจาก caller formal รับเฉพาะ byte branch เอกฐาน, exact mode load จาก `[esp+disp8]`, singleton reaching definition และตำแหน่ง call ในแขน zero/nonzero เดียวกัน โดย `indirect_mode_formal_source` ตรึง load/use/depth/formal offsets",
        "- direct target ที่รองรับทั้ง W/R ต้องพิสูจน์ local formal mode ทุก call site แม้ ancestor จะจำกัด `allowed` เหลือทิศเดียว; รับเฉพาะ intersection ที่พิสูจน์จาก zero/nonzero branch กับ WRITE/READ anchors ตรง และ caller value จาก constant, แขนง formal เดียวกัน หรือ formal forwarding ที่ width/mapping ตรงกัน; target ที่มี capability เอกฐานและอยู่ในแขน direct mode ตรงข้ามกับ `allowed` จะถูกจัดเป็น direction-infeasible และไม่ flatten เป็น UNKNOWN ซ้ำ โดย validator ต้อง re-derive call, branch node, direct anchors และ file offset ครบ",
        "- transitive capability ที่ดูเป็น R/W อาจลดเหลือทิศเดียวเฉพาะใน call-site escape hatch เมื่อ target มีขอบเขต entry แบบ `ret; int3+` ตรงไบต์ก่อนหน้า, decode ไม่มี error, direct primitive ทุกจุดเป็นทิศเดียว, ไม่มี serializer-capable tail และ direct serializer child ทุกจุดเป็น singleton ทิศเดียวกันหรือพิสูจน์ local mode ได้ทิศเดียวกัน; `local_capability_refinement` ตรึง boundary/primitive/child offsets, ABI, argument-path count และ hash ของ direction proof โดยไม่แก้ global capability",
        "- predicate บน byte register เช่น `bl` ตาม provenance เป็น lane 8 บิตแยกจาก full GPR; เมื่อ recursive trace ติด loop รับ fallback จาก unique reaching `mov r32,[esp+disp]` แบบ 32 บิตและ stack depth เอกฐาน (`formal_byte_reaching_def`) หรือจาก formal proof ของ full GPR ที่เข้มกว่า; เส้นหลังรับ exact `lea r32,[r32+0]` พร้อม `formal_identity_lea`; undefined/multiple definition, partial/overlapping write และ opaque GPR clobber จะหยุด ไม่ยก `mov bl` เป็นการนิยาม `ebx` ทั้งตัว",
        "- fallback ค่า mode ศูนย์รับเพิ่มเฉพาะ reaching definition เดียวที่เป็นไบต์ exact `xor r32,r32` สองไบต์โดย register เดียวกัน (`mode_zero_reaching_def`); EAX-EBX ใช้ low-byte lane dataflow ส่วน ESI/EDI/EBP ใช้ full-GPR dataflow ที่เข้มกว่า และ fallback นี้ไม่รวมหลาย definition; direct symbolic path เดิมอาจรวมหลาย CFG paths ได้เฉพาะเมื่อ expression ทุกแขนลดรูปเป็นค่าคงที่เดียวกัน โดยใช้ `mode_arg` ไม่ใช่ marker ของ fallback",
        "- ชุด reaching definition หลายจุดใช้ escape hatch แยก (`mode_zero_reaching_set`) เฉพาะเมื่อไม่มี undefined entry และทุก definition เป็น exact full-width two-byte `xor r32,r32` ของ register เดียวกัน; ตรึงสมาชิกทุกจุดและไม่ใช้ generic constant/value lattice",
        "- ค่า mode ศูนย์อาจข้าม exact full-width `lea r32,[r32+0]` ได้หนึ่งชั้นด้วย `mode_zero_identity_lea` เมื่อ identity site เป็น reaching definition เดียวของ use และ complete reaching set ก่อน identity ไม่มี undefined path โดยทุกสมาชิกเป็น exact full-width XOR-self ของ register เดียวกัน; ไม่ไล่ identity chain และไม่ใช้ generic value lattice",
        "- mode predicate รูป `cmp byte-formal, low8-register` รับค่าเทียบเป็นศูนย์เฉพาะเมื่อทุก reaching definition ของ lane นั้นเป็น exact full-width `xor r32,r32`; `predicate_zero_reaching` ตรึง register/lane/use และ definition ทุกจุด",
        "- wrapper ที่ไม่มี primitive R/W ตรงอาจใช้ `mode_nested_anchor_*` ได้เพียงหนึ่งชั้น เมื่อแต่ละแขนงมี direct child call เอกฐาน, child มี direction เอกฐาน, ABI/argument path ครบ และ formal ของ stream ตามถึง direct primitive ECX anchor ของ child ได้เอกฐาน; `target_nested_stream_anchor_*` ตรึงแขนงที่ direction ของ caller เลือกจริง",
        "- stack-depth ข้าม indirect import ได้เฉพาะ IAT ที่ PE import table ระบุชื่อ exact เป็น `_invalid_parameter_noinfo` หรือ `basic_string<wchar_t>` constructor/destructor ที่ decoration ลงท้าย `QAE@XZ` (ไม่มี stack argument); รองรับทั้ง `call [IAT]` ตรงและ `call r32` ที่ unprefixed reaching set มี definition เดียวเป็น exact `mov r32,[IAT]` ของ register เดียวกัน; `stack_neutral_register_import` ตรึง call/load/IAT/descriptor/lookup/DLL/symbol file offsets ส่วน undefined/multiple definition, รูปไบต์อื่น และ import นอก allowlist ยังทำให้ depth เป็น UNKNOWN",
        "- vtable `+0x10` ที่โจทย์ตรึงเป็น GetId แบบไม่มี stack argument รักษา depth ได้เฉพาะ `call r32` unprefixed ที่ reaching definition เดียวเป็น adjacent exact `mov r32,[r32+0x10]` และ symbolic target ยืนยัน slot เดียวกัน; `stack_neutral_vtable_getid` ตรึง call/load offsets ส่วน prefix, slot อื่น, non-adjacent/ambiguous definition และ depth ที่เสียไปแล้วไม่ผ่าน",
        "- คำสั่งที่เขียน ESP จะรักษา stack depth ได้เพิ่มเฉพาะไบต์ exact `8D A4 24 00 00 00 00` ซึ่ง decode ตรงเป็น full-width `lea esp,[esp+0]`; `stack_identity_lea` ตรึง VA/file offset และ function ส่วน prefix, displacement อื่น, index, register อื่น หรือ depth ที่เสียไปก่อนหน้าไม่ถูกกู้คืน",
        "- mode formal/value ที่ยังพิสูจน์ไม่ได้เป็น `UNKNOWN(subcall_direction_unresolved...)` และไม่ถูกขยายเป็นสองทิศ",
        "- stream ที่ยัง trace แบบ singleton ไม่ได้เป็น `UNKNOWN(subcall_stream_provenance_unresolved...)` และห้าม recurse; `stream_call`/`stream_arg` หรือ `stream_tail`, `stream_formal_discovery`, `tail_stack_depth`, caller/target anchors และ `primitive_stream` บันทึก VA กับ file offset ให้ตรวจซ้ำได้",
        "- descendant ทุกแถวสืบทั้งหลักฐาน stream และ `subcall_path@VA file_off target` ของ ancestor แต่ละชั้น จึงแยก static paths ที่ลงท้าย primitive site เดียวกันได้จาก A2 โดยตรง",
        "- นอกจาก primitive, exact direct-IAT/singleton-register/multi-register import calls, ตัวช่วยข้อความสี่ target, atomic helper สี่ target, pure chain predicate, mutable chain helper, locked mutable pointer-slot helper, critical-section pointer wrappers, locked mutable dword-slot update helper, nested three-call composition helper, ECX+0x50 tail-jump helper, mutable pointer-slot traversal helper, mutable dword-slot operation helper และ mutable dword-range growth helper ที่พิสูจน์รูปปฏิบัติการตามขอบเขตแล้ว direct/indirect call อื่นทุกจุดไม่ถูกข้าม แต่บันทึก `CALL_UNCLASSIFIED` เป็น UNKNOWN พร้อม file offset โดยไม่เดาว่าเป็น utility หรือ serializer",
        "- `order` คือลำดับ static call-site ตาม VA แยก W/R และแทรกผล recurse หลัง SUBCALL; ไม่อ้างเป็น dynamic execution count/order สำหรับ loop หรือแขนงที่กำกวม",
        "- `field_offset` ที่ไม่ใช่ `+0x...` เป็นนิพจน์ symbolic ตามคำสั่งจริง เช่น pointer, stack temporary, loop index หรือค่าคืนจากฟังก์ชัน ไม่ถูกบังคับให้เป็น member offset; top-level query ของแต่ละ event ใช้ resolver แยกกันเพื่อไม่ให้ cycle-breaking memo จาก event ก่อนหน้าเปลี่ยนผล",
        "- `EMPTY` รับ body `ret`/`ret 8` ล้วนและ exact allowlist หกกรณี: constant-return, absolute-global predicate, two-/single-argument value copier, conditional object init และ FPSTest entry-reachable prefix; กรณี FPSTest เทียบ full span 156 bytes ทุกไบต์ แต่จำกัดคำอ้าง EMPTY ไว้ที่ 24 คำสั่งซึ่งเข้าถึงได้จาก entry `0x0073E8B0` และสิ้นสุดก่อนตัวคั่น `CC CC` เท่านั้น ส่วน routine ที่เริ่ม `0x0073E900` ไม่อยู่ในคำอ้างและยังไม่ตีความ ทุกกรณีอ้างเพียงว่าเส้นทางที่ระบุไม่มี wire field พร้อม VA/file offset/full bytes หรือ full-span hash ส่วน body อื่นยัง UNKNOWN",
        "",
        "## จำนวน",
        "",
        "- protocol rows: %d" % len(registry),
        "- A2 rows: %d" % len(rows),
        "- measured numeric W/R fields: %d" % numeric,
        "- exact string wire-helper rows: %d" % string_helper_rows,
        "- exact atomic increment rows blocked by object-alias proof: %d"
        % atomic_increment_unknown_rows,
        "- exact atomic decrement rows blocked at dynamic vtable target: %d"
        % atomic_dynamic_rows,
        "- exact direct atomic pointer rows blocked by alias proof: %d"
        % atomic_pointer_rows,
        "- exact read-only chain predicate rows: %d" % pure_chain_rows,
        "- exact mutable chain rows blocked by object-alias proof: %d"
        % mutable_chain_rows,
        "- exact locked mutable pointer-slot rows blocked by nested-target/alias proof: %d"
        % locked_mutable_pointer_slot_rows,
        "- exact critical-section pointer rows blocked by alias proof: %d"
        % critical_section_pointer_rows,
        "- exact locked mutable dword-slot update rows blocked by nested-target/alias proof: %d"
        % locked_mutable_dword_slot_update_rows,
        "- exact nested three-call composition rows blocked by nested-target/alias proof: %d"
        % nested_call_composition_rows,
        "- exact ECX+0x50 tail-jump rows blocked by tail-target/alias proof: %d"
        % ecx_plus_50_tail_jump_rows,
        "- exact mutable pointer-slot traversal rows blocked by alias proof: %d"
        % mutable_pointer_slot_traversal_rows,
        "- exact mutable dword-slot operation rows blocked by nested-target/alias proof: %d"
        % mutable_dword_slot_operation_rows,
        "- exact mutable dword-range growth rows blocked by nested-target/alias proof: %d"
        % mutable_dword_range_growth_rows,
        "- exact direct `_invalid_parameter_noinfo` IAT rows blocked by wire-effect proof: %d"
        % exact_direct_import_call_rows,
        "- other exact direct PE-import rows blocked by wire-effect proof: %d"
        % other_exact_direct_import_call_rows,
        "- exact rel32 PE-import thunk rows blocked by wire-effect proof: %d"
        % exact_import_thunk_call_rows,
        "- exact PE SecurityCookie check rows blocked by failure-path proof: %d"
        % pe_security_cookie_check_rows,
        "- exact singleton-register `_invalid_parameter_noinfo` rows blocked by wire-effect proof: %d"
        % exact_singleton_register_import_call_rows,
        "- exact multi-register `_invalid_parameter_noinfo` rows blocked by wire-effect proof: %d"
        % exact_multi_register_import_call_rows,
        "- SUBCALL rows: %d" % subcalls,
        "- direction-proven direct SUBCALL rows: %d" % direction_proven_subcalls,
        "- formal-to-formal forwarded SUBCALL rows: %d" % formal_forward_subcalls,
        "- stream-proven direct/tail SUBCALL rows: %d" % stream_proven_subcalls,
        "- rows stopped by unresolved stream provenance: %d" % stream_unresolved,
        "- rows carrying exact stack-neutral import evidence: %d" % neutral_import_rows,
        "- rows carrying register-indirect stack-neutral evidence: %d"
        % register_neutral_import_rows,
        "- rows carrying exact stack-identity LEA evidence: %d"
        % stack_identity_rows,
        "- rows carrying exact GetId vtable stack evidence: %d"
        % getid_stack_rows,
        "- rows carrying indirect formal-mode source evidence: %d"
        % indirect_formal_rows,
        "- rows carrying local capability refinement evidence: %d" % local_capability_rows,
        "- rows carrying identity-LEA zero evidence: %d" % identity_zero_rows,
        "- unclassified CALL/JUMP rows: %d" % unclassified_calls,
        "- rows with gate/path evidence: %d" % gates,
        "- protocol serializers without UNKNOWN: %d" % successful,
        "- protocol serializers with UNKNOWN: %d" % len(unknown_messages),
        "- image SHA-256: `%s`" % image.sha256,
    ]
    if reasons:
        lines.extend(["", "## เหตุผล UNKNOWN", ""])
        for reason, count in sorted(reasons.items()):
            lines.append("- `%s`: %d protocol(s)" % (reason, count))
    lines.append("")
    return "\n".join(lines)


def build_tag_census(rows: list[FieldRow]) -> tuple[str, int]:
    groups: dict[tuple[str, str], list[FieldRow]] = defaultdict(list)
    for row in rows:
        if (
            row.direction in ("W", "R")
            and re.fullmatch(r"0x[0-9A-F]{2}", row.tag)
            and re.fullmatch(r"[0-9]+", row.length)
        ):
            groups[(row.tag, row.length)].append(row)
    census_rows = []
    proven = {"0x2A": "float32", "0x12": "uint16"}
    lengths_by_tag: dict[str, set[str]] = defaultdict(set)
    for tag, length in groups:
        lengths_by_tag[tag].add(length)
    for (tag, length), items in sorted(
        groups.items(), key=lambda item: (int(item[0][0], 16), int(item[0][1]))
    ):
        examples = []
        for item in items:
            text = "%s:%s:%d@file_off=%s" % (
                item.message,
                item.direction,
                item.order,
                hex_or_unknown(item.file_off_claim),
            )
            if text not in examples:
                examples.append(text)
            if len(examples) == 3:
                break
        examples.extend([""] * (3 - len(examples)))
        census_rows.append(
            [
                tag,
                length,
                "FIXED" if len(lengths_by_tag[tag]) == 1 else "VARIABLE",
                str(len(items)),
                proven.get(tag, "UNKNOWN"),
                examples[0],
                examples[1],
                examples[2],
                STATIC_EVIDENCE_SOURCE,
            ]
        )
    return (
        format_tsv(
            [
                "tag",
                "len",
                "len_status_for_tag",
                "frequency_in_A2",
                "proven_semantics",
                "example_1",
                "example_2",
                "example_3",
                "source",
            ],
            census_rows,
        ),
        len(census_rows),
    )


RUNTIME_PROTOCOL_SPILL_BLOCKER_BYTES = (
    # RunTimeProtocol: the original stream formal is spilled at [ebp-0x50],
    # while the address of the adjacent [ebp-0x48] local escapes to a callee
    # before the spill is restored on the loop back-edge.  The complete
    # statically reachable write chain is pinned below; the two remaining
    # disjointness facts depend on runtime-selected object/allocation values.
    (0x005F3E63, 0x001F3263, "897DB0"),
    (0x005F3E98, 0x001F3298, "E8A3672A00"),
    (
        0x005F3EA0,
        0x001F32A0,
        "50E8BAF3FEFF8BC8E853EFFEFF8BF0",
    ),
    (0x005F3EF4, 0x001F32F4, "E847672A00"),
    (0x005F3F52, 0x001F3352, "8975B8E8F6902900"),
    (
        0x005F3F66,
        0x001F3366,
        "8D45B85051538BCFC745FC03000000E8C6F40B00",
    ),
    (0x005F3FA2, 0x001F33A2, "8B7DB0"),
    (0x005E2E31, 0x001E2231, "FFD5"),
    (0x005E2E3F, 0x001E223F, "FFD5"),
    (0x005E2E46, 0x001E2246, "FFD5"),
    (0x005E2E48, 0x001E2248, "8B4E108B118B4214FFD0"),
    (0x006B346B, 0x002B286B, "6A0CE80E454800"),
    (0x006B3485, 0x002B2885, "8B45088906"),
    (0x006B3491, 0x002B2891, "8B4D0C8908"),
    (0x006B3496, 0x002B2896, "8B5510528D460850E89D9BFEFF"),
    (
        0x0069D061,
        0x0029C461,
        "8B4424188944241889442404C744241000000000",
    ),
    (0x0069D079, 0x0029C479, "8B4C241C8B09890885C97405E8C6FF1E00"),
    (0x0088D050, 0x0048C450, "83C10C51FF15B0B1C300C3"),
    (0x00B37980, 0x00736D80, "FF25BCB4C300"),
)


RUNTIME_PROTOCOL_SPILL_BLOCKER_SPANS = (
    (
        0x005E2E00,
        0x001E2200,
        0x005E2E6C,
        0x001E226C,
        "c6d356a1e8ee06128aa2c579cbd80a4777b1f61c7f7e4ae666d618abdd0ed449",
    ),
    (
        0x006B3440,
        0x002B2840,
        0x006B350B,
        0x002B290B,
        "fbda8200f3d283db866f0a4a26f78ec293ec8d79996f0b93e52885d11298c612",
    ),
    (
        0x0069D040,
        0x0029C440,
        0x0069D09A,
        0x0029C49A,
        "b79870afe41d0111715a239fd6137b54216374300befa0ee0b4e9601e280b2f8",
    ),
    (
        0x0088D050,
        0x0048C450,
        0x0088D05B,
        0x0048C45B,
        "6da78a1acc15d9fd5f7b2d620253debf8d8465136165dfb1eae35914b2442845",
    ),
)


RUNTIME_PROTOCOL_SPILL_BLOCKER_IMPORTS = (
    (
        0x00C3B4BC,
        "MSVCR90.dll",
        "??2@YAPAXI@Z",
        0x008398BC,
        0x00C112DC,
        0x00C118B0,
        0x00C1647C,
        0x00C15BEE,
    ),
    (
        0x00C3B1B0,
        "KERNEL32.dll",
        "InterlockedIncrement",
        0x008395B0,
        0x00C11214,
        0x00C115A4,
        0x00C124EA,
        0x00C11FC4,
    ),
)


STATIC_BLOCKER_BYTES = (
    # StartGameRes and GuildStorage: a runtime-selected vtable +0x34 call
    # destroys stack-depth provenance before the later mode-formal load.
    (0x005EF2B0, 0x001EE6B0, "8B40345256FFD0"),
    (0x005EF2FC, 0x001EE6FC, "8B84242C010000"),
    (0x00673D24, 0x00273124, "8B40345257FFD0"),
    (0x00673D36, 0x00273136, "8B542414"),
    # CArena and SearchParty: the member pointer's runtime vtable slot zero
    # is called after the refcount test, before the stream-formal reload.
    (0x00625DFA, 0x002251FA, "8B118B026A01FFD0"),
    (0x00625E08, 0x00225208, "8B7C2424"),
    (0x0063779A, 0x00236B9A, "8B118B026A01FFD0"),
    (0x006377A8, 0x00236BA8, "8B7C2424"),
)


def validate_runtime_protocol_spill_blocker_evidence(image: Image) -> None:
    """Pin the exact in-image part of the RunTimeProtocol spill blocker."""
    for va, expected_off, expected_hex in RUNTIME_PROTOCOL_SPILL_BLOCKER_BYTES:
        actual_off = image.va_to_off(va)
        expected = bytes.fromhex(expected_hex)
        if (
            actual_off != expected_off
            or actual_off is None
            or image.data[actual_off : actual_off + len(expected)] != expected
        ):
            raise ExtractionError(
                "runtime protocol spill blocker byte mismatch at VA 0x%08X" % va
            )

    for start_va, start_off, end_va, end_off, expected_sha256 in (
        RUNTIME_PROTOCOL_SPILL_BLOCKER_SPANS
    ):
        span = find_function_span(image, start_va)
        if (
            span is None
            or span.start_va != start_va
            or span.start_off != start_off
            or span.end_va != end_va
            or span.end_off != end_off
            or hashlib.sha256(
                image.data[span.start_off : span.end_off]
            ).hexdigest()
            != expected_sha256
        ):
            raise ExtractionError(
                "runtime protocol spill blocker span mismatch at VA 0x%08X"
                % start_va
            )

    for expected in RUNTIME_PROTOCOL_SPILL_BLOCKER_IMPORTS:
        iat_va = expected[0]
        symbol = image.imports_by_iat.get(iat_va)
        actual = (
            None
            if symbol is None
            else (
                symbol.iat_va,
                symbol.dll,
                symbol.name,
                symbol.iat_off,
                symbol.descriptor_off,
                symbol.lookup_off,
                symbol.dll_name_off,
                symbol.symbol_name_off,
            )
        )
        if actual != expected:
            raise ExtractionError(
                "runtime protocol spill blocker import mismatch at IAT 0x%08X"
                % iat_va
            )


def validate_static_blocker_report_evidence(
    image: Image, fields: list[FieldRow]
) -> None:
    """Pin the exact bytes and UNKNOWN rows summarized in report section 3.

    These checks intentionally do not promote any row.  They distinguish an
    unresolved runtime-selected target/alias state from a claim that the
    relevant implementation bytes are absent from the image.
    """
    validate_runtime_protocol_spill_blocker_evidence(image)
    for va, expected_off, expected_hex in STATIC_BLOCKER_BYTES:
        actual_off = image.va_to_off(va)
        expected = bytes.fromhex(expected_hex)
        if (
            actual_off != expected_off
            or actual_off is None
            or image.data[actual_off : actual_off + len(expected)] != expected
        ):
            raise ExtractionError(
                "static blocker byte mismatch at VA 0x%08X" % va
            )

    expected_rows = {
        (
            "GSCN_RunTimeProtocolReq",
            "R",
            0x001F3298,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "GSCN_RunTimeProtocolReq",
            "R",
            0x001F32F4,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "GSCN_RunTimeProtocolRes",
            "R",
            0x001F3298,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "GSCN_RunTimeProtocolRes",
            "R",
            0x001F32F4,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "GSCN_LoginProtocol",
            "R",
            0x001F3298,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "GSCN_LoginProtocol",
            "R",
            0x001F32F4,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "LSCN_Protocol",
            "R",
            0x001F3298,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "LSCN_Protocol",
            "R",
            0x001F32F4,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "VitalProtocol",
            "R",
            0x001F3298,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "VitalProtocol",
            "R",
            0x001F32F4,
            "primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE",
        ),
        (
            "StartGameRes",
            "R",
            0x001EE821,
            "subcall_direction_unresolved target=0x005DEF10 proof=caller_mode_value_unproved",
        ),
        (
            "StartGameRes",
            "W",
            0x001EE821,
            "subcall_direction_unresolved target=0x005DEF10 proof=caller_mode_value_unproved",
        ),
        (
            "GSSS_GuildStorageCmdVital",
            "R",
            0x0027313C,
            "subcall_direction_unresolved target=0x0074CF90 proof=caller_mode_value_unproved",
        ),
        (
            "GSSS_GuildStorageCmdVital",
            "W",
            0x0027313C,
            "subcall_direction_unresolved target=0x0074CF90 proof=caller_mode_value_unproved",
        ),
        (
            "CArenaVital",
            "R",
            0x0022526C,
            "subcall_stream_provenance_unresolved target=0x00623220 proof=stream_argument_origin_unproved",
        ),
        (
            "CArenaVital",
            "W",
            0x0022526C,
            "subcall_stream_provenance_unresolved target=0x00623220 proof=stream_argument_origin_unproved",
        ),
        (
            "CSearchPartyVital",
            "R",
            0x00236C0C,
            "subcall_stream_provenance_unresolved target=0x006342C0 proof=stream_argument_origin_unproved",
        ),
        (
            "CSearchPartyVital",
            "W",
            0x00236C0C,
            "subcall_stream_provenance_unresolved target=0x006342C0 proof=stream_argument_origin_unproved",
        ),
    }
    blocker_reasons = {item[3] for item in expected_rows}
    actual_rows = {
        (row.message, row.direction, row.file_off_claim, row.reason)
        for row in fields
        if row.reason in blocker_reasons
    }
    if actual_rows != expected_rows:
        raise ExtractionError("static blocker UNKNOWN-row census mismatch")


def build_report(
    registry: list[RegistryRow],
    fields: list[FieldRow],
    before_hash: str,
    after_hash: str,
) -> str:
    unknown_messages, reasons = unknown_summary(fields)
    successful_messages = len(registry) - len(unknown_messages)
    serializer_by_name = {row.name: row.serializer_va for row in registry}
    successful_unique = {
        serializer_by_name[name]
        for name in serializer_by_name
        if name not in unknown_messages and serializer_by_name[name] is not None
    }
    direction_proven_subcalls = sum(
        row.tag.startswith("SUBCALL:")
        and has_local_direction_proof(row)
        for row in fields
    )
    formal_forward_subcalls = sum(
        row.tag.startswith("SUBCALL:")
        and has_local_formal_forward_proof(row)
        for row in fields
    )
    stream_proven_subcalls = sum(
        row.tag.startswith("SUBCALL:0x") and has_local_stream_proof(row)
        for row in fields
    )
    stream_unresolved = sum(
        "stream_provenance_unresolved" in row.reason for row in fields
    )
    register_neutral_import_rows = sum(
        "stack_neutral_register_import@" in row.gate_condition
        for row in fields
    )
    neutral_import_rows = sum(
        "stack_neutral_import@" in row.gate_condition
        or "stack_neutral_register_import@" in row.gate_condition
        for row in fields
    )
    stack_identity_rows = sum(
        "stack_identity_lea@" in row.gate_condition for row in fields
    )
    getid_stack_rows = sum(
        "stack_neutral_vtable_getid@" in row.gate_condition
        for row in fields
    )
    indirect_formal_rows = sum(
        "indirect_mode_formal_source " in row.gate_condition
        for row in fields
    )
    local_capability_rows = sum(
        "local_capability_refinement" in row.gate_condition for row in fields
    )
    identity_zero_rows = sum(
        "mode_zero_identity_lea" in row.gate_condition for row in fields
    )
    string_helper_rows = sum(
        row.tag in {spec.tag for spec in STRING_WIRE_HELPERS.values()}
        for row in fields
    )
    atomic_increment_unknown_rows = sum(
        row.tag == ATOMIC_OBJECT_HELPERS[0x0088D050].tag for row in fields
    )
    atomic_dynamic_rows = sum(
        row.tag == ATOMIC_OBJECT_HELPERS[0x0088D060].tag for row in fields
    )
    atomic_pointer_rows = sum(
        row.tag
        in {
            ATOMIC_OBJECT_HELPERS[0x004A06A0].tag,
            ATOMIC_OBJECT_HELPERS[0x004A06B0].tag,
        }
        for row in fields
    )
    pure_chain_rows = sum(
        row.tag == PURE_CHAIN_HELPERS[0x0088F2B0].tag for row in fields
    )
    mutable_chain_rows = sum(
        row.tag == MUTABLE_CHAIN_HELPERS[0x00B0BF70].tag for row in fields
    )
    locked_mutable_pointer_slot_rows = sum(
        row.tag
        == LOCKED_MUTABLE_POINTER_SLOT_HELPERS[0x0066AB90].tag
        for row in fields
    )
    critical_section_pointer_rows = sum(
        row.tag in {spec.tag for spec in CRITICAL_SECTION_POINTER_HELPERS.values()}
        for row in fields
    )
    locked_mutable_dword_slot_update_rows = sum(
        row.tag
        == LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS[0x00710FA0].tag
        for row in fields
    )
    nested_call_composition_rows = sum(
        row.tag == "NESTED_THREE_CALL_COMPOSITION_HELPER"
        for row in fields
    )
    ecx_plus_50_tail_jump_rows = sum(
        row.tag == "ECX_PLUS_50_TAIL_JUMP_HELPER" for row in fields
    )
    mutable_pointer_slot_traversal_rows = sum(
        row.tag
        == MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS[0x0046D2B0].tag
        for row in fields
    )
    mutable_dword_slot_operation_rows = sum(
        row.tag
        == MUTABLE_DWORD_SLOT_OPERATION_HELPERS[0x00AC6E80].tag
        for row in fields
    )
    mutable_dword_range_growth_rows = sum(
        row.tag == MUTABLE_DWORD_RANGE_GROWTH_HELPERS[0x007016A0].tag
        for row in fields
    )
    exact_direct_import_call_rows = sum(
        row.tag == EXACT_DIRECT_IMPORT_CALLS[0x00C3B4C0].tag
        for row in fields
    )
    other_exact_direct_import_call_rows = sum(
        row.tag
        in {
            EXACT_DIRECT_IMPORT_CALLS[iat_va].tag
            for iat_va in OTHER_EXACT_DIRECT_IMPORT_CALL_IATS
        }
        for row in fields
    )
    exact_import_thunk_call_rows = sum(
        row.tag in {spec.tag for spec in EXACT_IMPORT_THUNK_CALLS.values()}
        for row in fields
    )
    pe_security_cookie_check_rows = sum(
        row.tag
        in {spec.tag for spec in PE_SECURITY_COOKIE_CHECK_HELPERS.values()}
        for row in fields
    )
    exact_singleton_register_import_call_rows = sum(
        row.tag
        in {
            spec.tag
            for spec in EXACT_SINGLETON_REGISTER_IMPORT_CALLS.values()
        }
        for row in fields
    )
    exact_multi_register_import_call_rows = sum(
        row.tag
        in {spec.tag for spec in EXACT_MULTI_REGISTER_IMPORT_CALLS.values()}
        for row in fields
    )
    rtti_registry_rows = sum(bool(row.resolution_proof) for row in registry)
    invariant_serializer_rows = sum(
        bool(row.serializer_resolution_proof) for row in registry
    )
    invariant_handler_rows = sum(
        bool(row.handler_resolution_proof) for row in registry
    )
    lines = [
        "## 1) จำนวน protocol, serializer ที่ถอดสำเร็จ และ UNKNOWN",
        "",
        "- protocol registration: %d" % len(registry),
        "- evidence source ของ A1-A3 ทุกแถว: `IMAGE`",
        "- protocol serializer ที่ไม่มี UNKNOWN: %d" % successful_messages,
        "- unique serializer VA ที่ไม่มี UNKNOWN: %d" % len(successful_unique),
        "- protocol serializer ที่ยังมี UNKNOWN: %d" % len(unknown_messages),
        "- protocol ที่แก้ vtable กำกวมด้วย exact primary x86 MSVC RTTI: %d"
        % rtti_registry_rows,
        "- protocol ที่พิสูจน์ serializer ค่าเดียวกันใน vtable candidate ครบ census: %d"
        % invariant_serializer_rows,
        "- protocol ที่พิสูจน์ handler ค่าเดียวกันใน vtable candidate ครบ census: %d"
        % invariant_handler_rows,
        "- direct SUBCALL ที่พิสูจน์ทิศจาก formal branch: %d แถว" % direction_proven_subcalls,
        "- ในจำนวนนั้นเป็น formal-to-formal forwarding: %d แถว" % formal_forward_subcalls,
        "- direct/tail SUBCALL ที่พิสูจน์ stream chain ครบ: %d แถว" % stream_proven_subcalls,
        "- แถวที่หยุดเพราะ stream provenance ยังไม่เอกฐาน: %d แถว" % stream_unresolved,
        "- แถวที่ใช้หลักฐาน PE import แบบ stack-neutral: %d แถว" % neutral_import_rows,
        "- ในจำนวนนั้นใช้ exact register-indirect IAT proof: %d แถว"
        % register_neutral_import_rows,
        "- แถวที่บันทึกหลักฐาน exact `lea esp,[esp+0]` stack-identity: %d แถว"
        % stack_identity_rows,
        "- แถวที่บันทึกหลักฐาน GetId vtable `+0x10` แบบ stack-neutral: %d แถว"
        % getid_stack_rows,
        "- แถวที่พิสูจน์ indirect serializer mode จาก caller formal แบบ exact: %d แถว"
        % indirect_formal_rows,
        "- แถวที่ใช้ complete local capability refinement: %d แถว" % local_capability_rows,
        "- แถวที่ใช้ zero proof ผ่าน exact identity LEA: %d แถว" % identity_zero_rows,
        "- แถวข้อความที่พิสูจน์ผ่าน exact string wire helper: %d แถว"
        % string_helper_rows,
        "- แถว exact `InterlockedIncrement(ECX+0x0C)` ที่ยังหยุดเพราะ object/non-alias ไม่เอกฐาน: %d แถว"
        % atomic_increment_unknown_rows,
        "- แถว exact `InterlockedDecrement(ECX+0x0C)` ที่ยังหยุด ณ dynamic vtable `+0x04`: %d แถว"
        % atomic_dynamic_rows,
        "- แถว exact direct `InterlockedIncrement/Decrement(ECX)` ที่ยังหยุดเพราะ pointer non-alias ไม่เอกฐาน: %d แถว"
        % atomic_pointer_rows,
        "- แถว exact read-only chain `+0x04` contains predicate: %d แถว"
        % pure_chain_rows,
        "- แถว exact mutable chain ที่ยังหยุดเพราะ object/non-alias ไม่เอกฐาน: %d แถว"
        % mutable_chain_rows,
        "- แถว exact locked mutable pointer-slot ที่ยังหยุดเพราะ nested target/alias ไม่เอกฐาน: %d แถว"
        % locked_mutable_pointer_slot_rows,
        "- แถว exact Enter/LeaveCriticalSection pointer wrapper ที่ยังหยุดเพราะ alias ไม่เอกฐาน: %d แถว"
        % critical_section_pointer_rows,
        "- แถว exact locked mutable dword-slot update ที่ยังหยุดเพราะ nested target/alias ไม่เอกฐาน: %d แถว"
        % locked_mutable_dword_slot_update_rows,
        "- แถว exact nested three-call composition ที่ยังหยุดเพราะ nested target/alias ไม่เอกฐาน: %d แถว"
        % nested_call_composition_rows,
        "- แถว exact ECX+0x50 tail-jump ที่ยังหยุดเพราะ tail target/alias ไม่เอกฐาน: %d แถว"
        % ecx_plus_50_tail_jump_rows,
        "- แถว exact mutable pointer-slot traversal ที่ยังหยุดเพราะ alias ไม่เอกฐาน: %d แถว"
        % mutable_pointer_slot_traversal_rows,
        "- แถว exact mutable dword-slot operation ที่ยังหยุดเพราะ nested target/alias ไม่เอกฐาน: %d แถว"
        % mutable_dword_slot_operation_rows,
        "- แถว exact mutable dword-range growth ที่ยังหยุดเพราะ nested target/alias ไม่เอกฐาน: %d แถว"
        % mutable_dword_range_growth_rows,
        "- แถว exact direct-IAT `_invalid_parameter_noinfo` ที่ยังหยุดเพราะผลต่อ wire path ไม่เอกฐาน: %d แถว"
        % exact_direct_import_call_rows,
        "- แถว exact direct PE-import อื่นที่ยังหยุดเพราะผลต่อ wire path ไม่เอกฐาน: %d แถว"
        % other_exact_direct_import_call_rows,
        "- แถว exact rel32 PE-import thunk ที่ยังหยุดเพราะผลต่อ wire path ไม่เอกฐาน: %d แถว"
        % exact_import_thunk_call_rows,
        "- แถว exact PE SecurityCookie check ที่ยังหยุดเพราะ failure-path effect ไม่เอกฐาน: %d แถว"
        % pe_security_cookie_check_rows,
        "- แถว exact singleton-register `_invalid_parameter_noinfo` ที่ยังหยุดเพราะผลต่อ wire path ไม่เอกฐาน: %d แถว"
        % exact_singleton_register_import_call_rows,
        "- แถว exact multi-register `_invalid_parameter_noinfo` ที่ทุก reaching definition โหลด IAT เดียวกัน แต่ยังหยุดเพราะผลต่อ wire path ไม่เอกฐาน: %d แถว"
        % exact_multi_register_import_call_rows,
    ]
    if reasons:
        for reason, count in sorted(reasons.items()):
            lines.append("- UNKNOWN `%s`: %d protocol(s)" % (reason, count))
    else:
        lines.append("- UNKNOWN: 0")
    lines.extend(
        [
            "",
            "## 2) hash ของ image ก่อนและหลัง",
            "",
            "- ก่อน: `%s`" % before_hash,
            "- หลัง: `%s`" % after_hash,
            "- ผล: %s" % ("ตรงกัน; image ไม่เปลี่ยน" if before_hash == after_hash else "ไม่ตรงกัน"),
            "",
            "## 3) สิ่งที่ยังไม่รู้",
            "",
            "- protocol ที่ getter/vtable/serializer ไม่เอกฐานยังคงเป็น UNKNOWN; escape hatch ของ vtable รับเฉพาะ candidate เดียวที่มี primary x86 MSVC Complete Object Locator ครบโครงสร้างและ TypeDescriptor ชื่อเต็มตรง registry name โดยมี file offset ทุกชั้น ไม่มีการเลือก candidate จากความใกล้ของสตริง; หาก vtable ยังแยกไม่ได้ serializer/handler จะเลื่อนสถานะได้เฉพาะ slot ที่เป็น executable VA ค่าเดียวกันใน candidate getter/marker ครบทั้ง census และบันทึก pointer file offset ครบทุก candidate โดยไม่อ้างว่า vtable ถูกแก้แล้ว",
            "- indirect subserializer เก็บนิพจน์ target ไว้ แต่ยังไม่มี static target VA จึงไม่ recurse ผ่านจุดนั้น",
            "- call ทุกจุดที่ไม่ผ่านหลักฐาน target/ABI ถูกเก็บเป็น CALL_UNCLASSIFIED; direct-IAT/singleton-register/multi-register `_invalid_parameter_noinfo`, exact direct PE-import อื่นอีก 12 IAT, exact rel32 import thunks `0x0088D020`/`0x00B37998`, PE SecurityCookie helper `0x00B37964`, สี่ string target `0x0089A6D0`, `0x0089A740`, `0x0089A810`, `0x0089A880`, atomic target `0x004A06A0`/`0x004A06B0`/`0x0088D050`/`0x0088D060`, pure predicate `0x0088F2B0`, mutable helper `0x00B0BF70`, locked mutable pointer-slot helper `0x0066AB90`, critical-section wrappers `0x0088D5B0`/`0x0049DA40`, locked mutable dword-slot helper `0x00710FA0`, nested three-call helper `0x005F8DE0`, ECX+0x50 tail-jump helper `0x005F8C30`, mutable pointer-slot traversal helper `0x0046D2B0`, mutable dword-slot helper `0x00AC6E80` และ mutable dword-range helper `0x007016A0` ถูกยกออกจากกลุ่ม generic หลัง exact body/ABI/key bytes/PE imports/Load Configuration ตรงตามกฎของแต่ละกลุ่ม ส่วน target อื่นยังไม่รู้ว่าเป็น wire helper, utility, allocation หรือ lifecycle call",
            "- atomic helper `0x0088D050`/file offset `0x0048C450` จบที่ `0x0088D05B` และพิสูจน์ exact `InterlockedIncrement(ECX+0x0C)` แต่ 116 unique call sites ยังไม่มี ECX object/non-alias provenance ที่แยก runtime address ออกจาก stream/buffer state จึงคง `atomic_target_object_alias_unproved`; `0x0088D060`/`0x0048C460` จบที่ `0x0088D082` ทำ exact decrement แล้ว branch ไป indirect call `0x0088D07E`/`0x0048C47E` ผ่านค่าที่โหลดจาก vtable `+0x04` ณ `0x0088D077`/`0x0048C477`; target/member identity ยัง runtime-selected จึงคง `dynamic_vtable_plus_0x04_target_unresolved` เช่นกัน",
            "- direct atomic target `0x004A06A0`/file offset `0x0009FAA0` และ `0x004A06B0`/`0x0009FAB0` มี body 8 ไบต์ที่ต่างกันเฉพาะ IAT `InterlockedIncrement`/`InterlockedDecrement`; ทั้ง 120 แถวยังไม่มี runtime ECX pointer non-alias proof จึงคง `atomic_target_pointer_alias_unproved` และไม่ถูกนับเป็น wire success",
            "- pure predicate `0x0088F2B0`/file offset `0x0048E6B0` ถูกยกจาก generic UNKNOWN หลังพิสูจน์ full body `[0x0088F2B0,0x0088F2D1)`, zero call/memory-write, stack arguments สองตัว, chain step `[eax+0x04]`, boolean returns และ exact caller suffix ครบ 34 unique sites; ข้ออ้างจำกัดว่า call นี้เป็น read-only predicate ไม่ได้ระบุว่า chain/node เป็นระบบใด",
            "- mutable helper `0x00B0BF70`/file offset `0x0070B370` มี full body `[0x00B0BF70,0x00B0BFDC)` และ write `[ESI+0x04]` ณ `0x00B0BFAB`/`0x0070B3AB`, `0x00B0BFC8`/`0x0070B3C8`, `0x00B0BFD7`/`0x0070B3D7`; แม้ operation shape และ import exact จะรู้ครบ แต่ ESI มาจาก runtime ECX object ที่ยังไม่พิสูจน์ non-alias กับ stream/buffer จึงคง `mutable_chain_target_object_alias_unproved` ทั้ง 70 แถว",
            "- locked mutable pointer-slot helper `0x0066AB90`/file offset `0x00269F90` มี full body `[0x0066AB90,0x0066AC2D)`, direct `malloc`/`_invalid_parameter_noinfo`, exact critical-section/interlocked wrappers และ writes ณ `0x0066AC14`/`0x0026A014`, `0x0066AC17`/`0x0026A017`, `0x0066ABE1`/`0x00269FE1`, `0x0066ABF9`/`0x00269FF9`, `0x0066AC1D`/`0x0026A01D`; nested target `0x007016A0` และ runtime ECX/EDX alias ยังไม่พิสูจน์ semantics เอกฐาน จึงคง `locked_mutable_pointer_slot_nested_target_and_alias_unproved` ทั้ง 58 แถว",
            "- critical-section wrappers `0x0088D5B0`/file offset `0x0048C9B0` และ `0x0049DA40`/`0x0009CE40` มี full body 10 ไบต์ที่ต่างกันเฉพาะ IAT `EnterCriticalSection`/`LeaveCriticalSection`; ทั้ง 64 แถวโหลด pointer จาก runtime `[ECX]` ซึ่งยังไม่มี non-alias proof กับ stream/buffer จึงคง `critical_section_pointer_alias_unproved` และไม่ถูกนับเป็น wire success",
            "- locked mutable dword-slot update helper `0x00710FA0`/file offset `0x003103A0` ใช้ bounded entry CFG `[0x00710FA0,0x0071100F)` 111 ไบต์/42 instructions, call `0x0088D5B0`/`0x007016A0`/`0x0049DA40`, direct `_invalid_parameter_noinfo` ที่ `0x00710FD6`/`0x00710FF2`, decrement `[ESI+0x20]` ที่ `0x00710FCC`, output write `0x00710FE2`, slot write `0x00710FFB` และ increment `[ESI+0x24]` ที่ `0x00710FFE`; nested target semantics กับ aliases ยังไม่เอกฐาน จึงคง `locked_mutable_dword_slot_nested_target_and_alias_unproved` ทั้ง 28 แถว",
            "- nested three-call composition helper `0x005F8DE0`/file offset `0x001F81E0` มี full body `[0x005F8DE0,0x005F8E04)` 36 ไบต์/13 instructions, direct calls `0x005F8DE3 -> 0x0089C080`, `0x005F8DEF -> 0x0089B220`, `0x005F8DFB -> 0x00463800`, zero-extend AX ที่ `0x005F8DF4`, สร้าง address `ECX+0x50` ที่ `0x005F8DF8`, ไม่มี explicit MOV ที่ปลายทางเป็น memory และจบ `ret 4`; nested target semantics กับ runtime object/value alias ยังไม่เอกฐาน จึงคง `nested_call_composition_targets_and_alias_unproved` ทั้ง 28 แถว",
            "- ECX+0x50 tail-jump helper `0x005F8C30`/file offset `0x001F8030` ใช้ entry-reachable prefix `[0x005F8C30,0x005F8C38)` 8 ไบต์/2 instructions: `add ecx,0x50` ที่ entry แล้ว direct tail jump `0x005F8C33 -> 0x00463800`/file offset `0x00062C00`; หลัง prefix เป็น `CC` 8 ไบต์ตั้งแต่ file offset `0x001F8038` จึงไม่รวม routine ถัดไปในคำอ้าง ส่วน tail target semantics กับ runtime ECX/object alias ยังไม่เอกฐาน จึงคง `ecx_plus_50_tail_target_and_alias_unproved` ทั้ง 20 แถว",
            "- mutable pointer-slot traversal helper `0x0046D2B0`/file offset `0x0006C6B0` มี full body `[0x0046D2B0,0x0046D31C)` 108 ไบต์/44 instructions, โหลด `_invalid_parameter_noinfo` จาก IAT `0x00C3B4C0` ณ `0x0046D2B7`, call EDI ที่ `0x0046D2BF`/`0x0046D2CA`, และเขียน `[ESI+0x04]` ที่ `0x0046D2EB`/`0x0046D308`/`0x0046D317`; runtime ECX/ESI object alias ยังไม่เอกฐาน จึงคง `mutable_pointer_slot_traversal_alias_unproved` ทั้ง 29 แถว",
            "- mutable dword-slot operation helper `0x00AC6E80`/file offset `0x006C6280` ใช้ bounded entry CFG `[0x00AC6E80,0x00AC6F00)` 128 ไบต์/53 instructions ตรง hash มี ret 4 ที่ `0x00AC6ED6`/`0x00AC6EFD`, stack-zero write `0x00AC6EAC`, state write `[ESI+0x10]=EDI` ที่ `0x00AC6ECE`, direct `_invalid_parameter_noinfo` และ nested calls ไป `0x006B35A0`/`0x00AC6D00`; nested semantics กับ runtime object/source alias ยังไม่เอกฐาน จึงคง `mutable_dword_slot_nested_targets_and_alias_unproved` ทั้ง 46 แถว",
            "- mutable dword-range growth helper `0x007016A0`/file offset `0x00300AA0` มี full body `[0x007016A0,0x00701725)`, zero write `0x007016E7`/`0x00300AE7`, end-pointer write `0x007016F0`/`0x00300AF0`, register-indirect `_invalid_parameter_noinfo` call `0x007016F9`/`0x00300AF9` และ nested call `0x0070170B`/`0x00300B0B` ไป `0x005F68D0`; nested semantics กับ runtime object alias ยังไม่เอกฐาน จึงคง `mutable_dword_range_nested_target_and_alias_unproved` ทั้ง 32 แถว",
            "- direct-IAT call encoding `FF15C0B4C300` จำนวน 231 unique function+call-site ถูก PE import table ระบุเป็น `MSVCR90.dll!_invalid_parameter_noinfo`; 638 แถว (W 337/R 301) ถูกยกจาก generic โดยคง `invalid_parameter_import_call_wire_effect_unproved` เพราะชื่อ import ไม่ได้พิสูจน์ผลข้างเคียงต่อ stream/buffer path; อีก 177 แถวที่ symbolic target เดียวกันเป็น register-indirect form จึงไม่รวมใน direct-IAT claim และแยกตรวจด้านล่าง",
            "- register-indirect `_invalid_parameter_noinfo` 179 แถว (W 105/R 74) จาก 66 unique sites ผ่าน singleton reaching proof ครบ: exact `call r32` และ exact unprefixed `mov r32,[0x00C3B4C0]`; 167 แถวในจำนวนนี้เคยมี symbolic target ลดรูปเป็น IAT เดียวกัน ส่วนอีก 12 แถวถูกพบจาก instruction/load proof โดยตรง จึงไม่เลือกตามข้อความ tag เดิม; ทั้งหมดคง `invalid_parameter_singleton_register_call_wire_effect_unproved`; 10 แถว/6 sites ที่มี reaching definitions มากกว่าหนึ่งจุดถูกแยกด้วย complete-set proof ด้านล่าง",
            "- register-indirect `_invalid_parameter_noinfo` อีก 10 แถว (W 8/R 2) จาก 6 unique sites มี complete reaching-definition set จุดละ 2 definitions โดยไม่มี undefined path และทุก definition เป็น exact unprefixed `mov r32,[0x00C3B4C0]` ของ register เดียวกับ exact `call r32`; จึงยกออกจาก generic เป็น `invalid_parameter_multi_register_call_wire_effect_unproved` แต่ยังคง UNKNOWN เพราะ import identity ไม่ได้พิสูจน์ผลข้างเคียงต่อ wire path",
            "- exact direct PE-import อื่น 12 IAT รวม 128 แถว (W 64/R 64) จาก 36 unique sites ผ่านรูปไบต์ `FF15 <IAT little-endian>` ตรงทุกจุด และชื่อ DLL/symbol/IAT/descriptor/lookup ถูก re-derive จาก PE import table; แยกเป็น tag ตาม operation แต่ทั้งหมดคง `exact_direct_import_call_wire_effect_unproved` เพราะชื่อ import กับ call target ยังไม่พิสูจน์ผลต่อ stream/buffer path",
            "- exact rel32 import thunks สอง target รวม 16 แถวจาก 5 unique caller sites: `0x0088D020`/file offset `0x0048C420` เป็น `FF257CB8C300` ไป IAT `0x00C3B87C` (`MSVCR90.dll!malloc`) 2 แถว และ `0x00B37998`/`0x00736D98` เป็น `FF25C4B4C300` ไป IAT `0x00C3B4C4` (`MSVCR90.dll!_CxxThrowException`) 14 แถว; call site ทุกจุดเป็น rel32 target ตรงและ PE metadata ถูกตรึง แต่ implementation อยู่นอก image จึงคง `exact_import_thunk_call_wire_effect_unproved`",
            "- PE SecurityCookie helper `0x00B37964`/file offset `0x00736D64` ครอบ bounded entry ถึง `0x00B37973`/`0x00736D73` เป็น `3B0DBCB402017502F3C3E9DF090000`, SHA-256 `d31930a6047b3a9a986b1473f701e5b28070d619ab4d14daaa258ab445d25c43`, แล้วตามด้วย `CC` 13 ไบต์. COFF `SizeOfOptionalHeader=0xE0` ที่ file offset `0x0000013C` และ PE32 `NumberOfRvaAndSizes=16` ที่ `0x0000019C` ยืนยันว่า Load Configuration DataDirectory[10] ที่ `0x000001F0` อยู่ในขอบเขตที่ประกาศ; compare operand `0x0102B4BC` ตรงกับ `SecurityCookie` field ที่ `0x00BBA9AC`; เส้นเท่ากัน return ณ `0x00B3796C`/`0x00736D6C`, เส้นไม่เท่ากัน tail jump ณ `0x00B3796E`/`0x00736D6E` ไป `0x00B38352`/`0x00737752`. call target นี้มี 19 แถว (W 7/R 12) จาก 6 unique sites/12 protocol แต่ failure-path effect ยังไม่เอกฐาน จึงคง `pe_security_cookie_failure_path_wire_effect_unproved`",
            "- indirect call นอก serializer slot `+0x18` ยังไม่ถูกเรียกว่า subserializer แม้รูปอาร์กิวเมนต์จะคล้ายกัน",
            "- subserializer ที่รองรับทั้ง W/R แต่ target formal branch หรือ caller mode value ยังพิสูจน์ไม่ได้จะหยุดเป็น UNKNOWN และไม่ recurse แม้ ancestor จะเหลือทิศเดียว; target capability เอกฐานในแขน local direct/nested ที่พิสูจน์ว่าขัดกับ ancestor จะเป็น direction-infeasible และไม่ถูก flatten เป็นแถวของทิศนั้น โดยต้อง re-derive branch node, anchors, target และ file offset ได้ครบ",
            "- subserializer ที่ยังผูก caller stream formal ผ่าน push/tail ไปยัง target formal และ primitive ECX ของทิศเดียวกันไม่ได้จะหยุดเป็น UNKNOWN; การย้อนจาก target รับเฉพาะคู่ formal เอกฐาน และ tail ต้องวัด stack depth=0; reachability ไป W/R เพียงอย่างเดียวไม่ถือเป็นหลักฐาน stream",
            "- frame-relative formal รับฐานที่พิสูจน์ด้วย full-width `mov reg, esp` ณ stack depth เดียว; LEA ยอมรับเพิ่มเฉพาะ `lea r32,[r32+0]` ที่ไม่มี size override/index/absolute/nonzero displacement ส่วน arithmetic, partial write, conflicting/missing predecessor และ loop cycle ไม่ถูกเดา",
            "- loop fallback รับ unique reaching plain-MOV definition จากทุก CFG path และ exact full-width identity LEA เท่านั้น; undefined entry, multiple definitions และ `other` opcode ที่ไม่อยู่ใน exact no-GPR-write allowlist จะตัด provenance; multi-path arguments ที่บาง path ไม่ส่ง formal เดิมยังเป็น UNKNOWN",
            "- byte-lane loop fallback รับ definition เดียวจากทุก CFG path ที่เป็น full-width `mov r32,[esp+disp]` และ stack depth เอกฐาน หรือ formal proof ของ full GPR ที่เข้มกว่า; `formal_byte_reaching_def` ตรึง definition/use/lane/width และ exact `lea r32,[r32+0]` ตรึงด้วย `formal_identity_lea`; undefined entry, หลาย definition, overlapping/partial write และ opaque GPR clobber ยังคง UNKNOWN",
            "- fallback ของ mode byte ค่า zero รับเฉพาะ reaching definition เอกฐานที่เป็น exact two-byte `xor r32,r32`; `mode_zero_reaching_def` ตรึง definition/use/register/width/value และผูกกับ local direction call; fallback นี้ไม่รวมหลาย definition ส่วน direct symbolic path เดิมรวม CFG paths ได้เมื่อ expression ทุกแขนลดรูปเป็นค่าคงที่เดียวกันและแสดงเพียง `mode_arg`",
            "- multi-definition zero ใช้ `mode_zero_reaching_set` แยกต่างหากเมื่อไม่มี undefined path และสมาชิกทุกจุดเป็น exact full-width two-byte `xor r32,r32` ของ register เดียวกัน; marker ตรึง definition ทุกจุดและไม่รวมค่าชนิดอื่น",
            "- zero ผ่าน identity LEA จำกัดหนึ่งชั้นและรับเฉพาะ exact full-width `lea r32,[r32+0]` ที่เป็น reaching definition เดียว โดย predecessor set ทุกเส้นเป็น XOR-self ของ register เดียวกัน; identity chain, undefined predecessor และ mixed value ยัง UNKNOWN",
            "- register-zero mode predicate รับเฉพาะ `al/cl/dl/bl` ที่ทุก reaching definition เป็น exact full-width XOR-self โดยไม่มี undefined path; high-byte register, mixed definition และ operand ที่ formal ไม่เอกฐานยังคง UNKNOWN",
            "- nested mode/stream escape hatch จำกัดหนึ่งชั้น: branch-exclusive direct child ต้องมี capability เอกฐานและ stream formal ต้องส่งต่อถึง direct primitive anchor ของ child แบบเอกฐาน; หลักฐานตรึง call/argument/primitive offsets และ hash ของ canonical stream proof",
            "- local capability refinement ไม่อ้างว่า transitive W/R union ผิดโดยทั่วไป; รับเฉพาะ target ที่มี `ret; int3+` entry boundary ตรงไบต์ก่อนหน้าและ direct primitive ทุกจุดเป็นทิศเดียว พร้อม known serializer edge ครบทุกจุดพิสูจน์ทิศเดียวกัน ส่วน utility call ที่ capabilities ว่างยังไม่ถูกตีความ",
            "- indirect import อื่นนอก allowlist ชื่อ exact สามรายการยังทำให้ stack depth เป็น UNKNOWN; `call r32` รับเฉพาะ unprefixed singleton reaching definition ที่เป็น exact `mov r32,[IAT]` ของ register เดียวกัน และยังไม่อนุมาน cleanup จากรูป call หรือการไม่มี `add esp`",
            "- virtual call นอก task-pinned GetId slot `+0x10` หรือ GetId ที่ไม่อยู่ในรูป adjacent exact load/call พร้อม singleton reaching definition ยังทำให้ stack depth เป็น UNKNOWN; กฎนี้ไม่ใช้กับ serializer slot `+0x18` และไม่กู้ depth ที่เสียไปแล้ว",
            "- blocker ที่ตรวจถึงจุดหยุดแล้วไม่ใช่หลักฐานว่า implementation bytes หายจาก image: `StartGameRes` สูญ stack provenance ที่ vtable `+0x34` call `0x005EF2B5`/file offset `0x001EE6B5` ก่อน mode load `0x005EF2FC`; `GSSS_GuildStorageCmdVital` สูญที่ call `0x00673D29`/`0x00273129` ก่อน mode load `0x00673D36`. target address และ cleanup ถูกเลือกจาก runtime vtable และยังไม่เป็น singleton จาก static bytes จึงคง `caller_mode_value_unproved`.",
            "- `CArenaVital` และ `CSearchPartyVital` สูญ stream-formal stack provenance หลัง vtable slot-zero calls `0x00625E00`/file offset `0x00225200` และ `0x006377A0`/`0x00236BA0`; static bytes ยังไม่พิสูจน์ว่าค่า member pointer ทุกแหล่งมี target/cleanup เดียว จึงไม่ใช้ runtime object identity ที่ยังไม่เอกฐานเป็นหลักฐาน.",
            "- RunTimeProtocol ห้าชื่อที่ใช้ serializer `0x005F3E20` เก็บ stream formal ที่ `[ebp-0x50]` ณ `0x005F3E63`/file offset `0x001F3263`, แต่ address ของ local ข้างเคียง `[ebp-0x48]` ถูกส่งเข้า call `0x006B3440` ณ `0x005F3F75`/`0x001F3375` ก่อน restore ที่ `0x005F3FA2`/`0x001F33A2`. ไล่ต่อได้ว่า pointer ใน local มาจาก call `0x005E2E00` ณ `0x005F3EA8`/`0x001F32A8`; ฟังก์ชันนั้นมี runtime-selected indirect calls ที่ `0x005E2E31`/`0x001E2231`, `0x005E2E3F`/`0x001E223F`, `0x005E2E46`/`0x001E2246` และ vtable `+0x14` call `0x005E2E50`/`0x001E2250`.",
            "- call `0x006B3440` ใช้ operator-new thunk `0x00B37980` ณ `0x006B346D`/file offset `0x002B286D`; thunk ณ `0x00B37980`/`0x00736D80` กระโดดผ่าน IAT `0x00C3B4BC`/`0x008398BC` ซึ่ง PE import table ระบุ `MSVCR90.dll!??2@YAPAXI@Z` ที่ symbol-name offset `0x00C15BEE`. object 12 ไบต์ที่คืนมาถูกเขียนที่ `0x006B3488`/`0x002B2888`, `0x006B3494`/`0x002B2894` และส่ง `new_object+0x8` เข้า `0x0069D040` ที่ call `0x006B349E`/`0x002B289E`; ที่ `0x0069D07F`/`0x0029C47F` มีการเขียน pointee และ `0x0069D085`/`0x0029C485` เรียก `0x0088D050`, ซึ่งบวก `+0x0C` ณ `0x0088D050`/`0x0048C450` แล้วเรียก IAT `KERNEL32.dll!InterlockedIncrement` `0x00C3B1B0`/`0x008395B0` ณ `0x0088D054`/`0x0048C454`. implementation ของ allocator/import และค่า object จริงอยู่นอก image; จึงยังพิสูจน์ไม่ได้ว่าทุก write ไม่ alias `[ebp-0x50]` และคง primitive calls `0x005F3E98`/`0x001F3298` กับ `0x005F3EF4`/`0x001F32F4` เป็น UNKNOWN.",
            "- การเขียน ESP รูปอื่นนอก exact `8D A4 24 00 00 00 00` ยังทำให้ stack depth เป็น UNKNOWN; stack-identity rule ไม่กู้ depth ที่เป็น UNKNOWN มาก่อนและไม่ขยายเป็น generic LEA arithmetic",
            "- symbolic pointer/stack/loop expressions บอกที่มาของ address ตามคำสั่ง แต่ไม่อ้างว่าเป็น member offset คงที่; resolver ของแต่ละ top-level event แยกจากกันเพื่อไม่ให้ผลขึ้นกับลำดับ query ก่อนหน้า",
            "- order เป็น static call-site order; dynamic order/จำนวนรอบของ loop และแขนงกำกวมยังไม่รู้",
            "- tag ที่ไม่มีหลักฐาน producer/consumer ชนิดข้อมูลยังไม่ทราบ semantics",
            "",
            "## 4) สิ่งที่เกือบเดาแต่หยุดไว้",
            "",
            "- ไม่ตีความทะเบียน 519 รายการว่าเป็น packet เครือข่ายทั้งหมด เพราะมี Attr, Module, Protocol และ Vital ปะปนกัน",
            "- ไม่เลือก vtable จาก RTTI ที่ชื่อเพียงบางส่วนหรือคล้ายกัน หรือโครงสร้างที่ช่วงไบต์ข้าม PE section; รับเฉพาะชื่อเต็ม `.?AV<registry-name>@@`, self BaseClassDescriptor และ candidate เอกฐานจาก getter/marker census เดิม",
            "- ไม่เลือก vtable จากการที่ serializer/handler slot เท่ากัน; ความเท่ากันข้าม candidate พิสูจน์ได้เฉพาะค่าของ slot นั้น ส่วน vtable ยังคง `UNKNOWN`",
            "- ไม่ตั้งชื่อชนิด tag จากขนาด; ระบุชนิดเฉพาะ `0x2A=float32` และ `0x12=uint16` ตามหลักฐานที่ให้มา",
            "- ไม่บังคับค่าที่มาจาก heap/list/stack ให้เป็น offset จาก OBJ และไม่เดา target ของ virtual call",
            "- ไม่ถือ inherited W/R ว่าใช้แทน local call-site proof ได้; formal ของ thiscall/cdecl ต้องมี zero/nonzero branch แยก WRITE/READ anchors ตรงทุก dual-target edge และ formal forwarding ต้องมีต้นทาง/ปลายทางเอกฐานพร้อม width/mapping ที่พิสูจน์ได้",
            "- ไม่ลด target ที่ transitive capabilities เป็น R/W ตาม direct primitive เพียงจุดเดียว; ต้องมี entry boundary แบบ `ret; int3+` และ census direct primitive กับ known serializer child/tail ทั้งฟังก์ชัน พร้อม reject decode error, function-interior target, ทิศขัดกัน และ proof ที่ไม่เอกฐาน",
            "- ไม่ไล่ nested direction anchor แบบไม่จำกัดความลึก และไม่ใช้ capability เอกฐานอย่างเดียวแทน stream provenance; ถ้า child ไม่มี direct primitive ECX anchor หรือมี nested candidate มากกว่าหนึ่งจุดจะหยุดเป็น UNKNOWN",
            "- ไม่ถือว่าการ call target ที่มี W/R อยู่ข้างในแปลว่าส่ง stream เดิม; จุดที่ stack depth สูญหายหลัง SEH/indirect call หรือ target direction ไม่มี primitive ECX anchor ตรงถูกหยุดเป็น UNKNOWN",
            "- ไม่ถือ indirect call ว่า stack-neutral เพียงเพราะไม่มี push ติดหน้า; นอกจาก import allowlist ที่พิสูจน์จาก PE table ยอมรับเฉพาะ task-pinned GetId slot `+0x10` ที่เป็น unprefixed call, adjacent exact load และ singleton reaching definition พร้อม file offsets; slot/รูปอื่นยัง UNKNOWN",
            "- ไม่ถือ LEA ที่เขียน ESP ทุกตัวว่าเป็น no-op; stack depth ข้ามได้เฉพาะรูปไบต์ exact `lea esp,[esp+0]` ที่ validator re-derive ได้ และไม่อนุมานจาก mnemonic เพียงอย่างเดียว",
            "- ไม่ตีความ byte write เป็น full-register value; `mov bl,...` ใช้พิสูจน์ได้เฉพาะ lane ต่ำที่ target ตรวจจริงเท่านั้น",
            "- ไม่ถือ register ใน `cmp` ว่าเป็นศูนย์จากชื่อ idiom หรือ symbolic value อย่างเดียว; ต้องมี `predicate_zero_reaching` ที่ re-derive definition set จาก CFG และไบต์จริงได้ครบ",
            "- ไม่ถือ LEA ทุกตัวเป็น no-op หรือค่าศูนย์; ยอมให้ข้ามเฉพาะ full-width zero-displacement same-register identity หนึ่งจุด และต้องย้อน reaching definitions ก่อน LEA ได้ XOR-self ครบทุก path",
            "- ไม่ตั้งชื่อ helper ว่า string/blob/vector จาก address หรือขนาดเพียงอย่างเดียว; ยกเว้นสี่ string target ที่พิสูจน์จาก full-span hash, exact key bytes, ABI และ PE import names ครบ target อื่นที่ตามถึง primitive ไม่ได้ยังคงเป็น CALL_UNCLASSIFIED",
            "- ไม่เรียก atomic helper ว่า smart pointer/refcount/Release จาก idiom และไม่ประกาศ increment ว่า NONWIRE จาก body เพียงอย่างเดียว; ตารางใช้ชื่อปฏิบัติการที่พิสูจน์ตรงจาก `InterlockedIncrement/Decrement`, runtime address `ECX+0x0C` และ vtable `+0x04` เท่านั้น โดยคง alias/target reason จนกว่าจะมี object provenance เอกฐาน",
            "- ไม่เรียก pure chain predicate ว่า list/set/registry หรือผูกกับชนิด object จากรูป loop; ระบุเพียงการอ่าน pointer `+0x04`, การเทียบกับ needle และค่า boolean ตาม exact bytes",
            "- ไม่เรียก mutable chain helper ว่า iterator/list cleanup จากรูป flag/link และ `_invalid_parameter_noinfo`; ระบุเพียง offset ที่อ่าน/เขียนและ alias blocker ตาม exact bytes",
            "- ไม่เรียก locked mutable pointer-slot helper ว่า vector/list/pool จากรูป pointer arithmetic, lock และ allocator; ระบุเฉพาะ operation shape, exact imports/wrappers, nested target ที่ยังไม่ตีความ และ alias blocker",
            "- ไม่สรุปว่า critical-section wrapper เป็น non-wire เพียงเพราะ import เป็น lock API; จนกว่าจะพิสูจน์ runtime `[ECX]` non-alias ได้ ตารางระบุเฉพาะ dereference, import operation และ alias blocker",
            "- ไม่เรียก mutable dword-range growth helper ว่า vector/list/pool จากการหารระยะด้วย 4, zero-fill และ end-pointer update; nested target `0x005F68D0` กับ alias ยังไม่พิสูจน์ จึงไม่ยกเป็น non-wire",
            "- ไม่เรียก mutable dword-slot operation helper ว่า vector/list/insert จากการหารระยะด้วย 4 และการเลื่อน `[ESI+0x10]`; nested targets สองตัวกับ runtime alias ยังไม่พิสูจน์ จึงไม่ยกเป็น non-wire",
            "- ไม่เรียก mutable pointer-slot traversal helper ว่า tree/map/iterator จากรูป link และ flag `+0x21`; ระบุเฉพาะ offset/call/write ที่ exact และคง runtime object alias เป็น UNKNOWN",
            "- ไม่เรียก locked mutable dword-slot update helper ว่า vector/list/swap จาก lock, slot scale 4 และ counter update; ระบุเฉพาะ bounded CFG/nested calls/writes ที่ exact และคง nested semantics กับ runtime alias เป็น UNKNOWN",
            "- ไม่ตั้งชื่อ nested three-call composition helper ว่า string lookup/convert/member update จากลำดับสาม call, zero-extension และ address `ECX+0x50`; ระบุเฉพาะ full body/call targets/dataflow ที่ exact และคง nested semantics กับ runtime alias เป็น UNKNOWN",
            "- ไม่เรียก ECX+0x50 tail-jump helper ว่า member/container/string wrapper จากการปรับ this-pointer แล้ว jump; ระบุเฉพาะ entry prefix, direct target และตัวคั่น `CC` ที่ exact โดยคง tail-target semantics กับ runtime alias เป็น UNKNOWN และไม่ลาก routine หลังตัวคั่นเข้าคำอ้าง",
            "- ไม่ตัด direct `_invalid_parameter_noinfo` import call ออกจาก UNKNOWN เพียงเพราะเป็น validation API; ตารางระบุ exact import operation แต่คง wire-effect blocker จนกว่าจะมี path/non-alias proof",
            "- ไม่ตัด constructor/destructor/c_str/interlocked/formatting/UI import ออกจาก UNKNOWN เพียงเพราะ PE ระบุชื่อฟังก์ชัน; กฎ direct import พิสูจน์เฉพาะ exact call encoding และ import identity ส่วน argument alias, return use และผลต่อ wire path ยังไม่เอกฐาน",
            "- ไม่ตัด `malloc` หรือ `_CxxThrowException` ออกจาก UNKNOWN เพียงเพราะ rel32 target เป็น unconditional IAT thunk และ PE ระบุชื่อ; กฎ import-thunk พิสูจน์เฉพาะ call target, thunk bytes และ import identity ส่วน implementation/argument alias/ผลต่อ wire path อยู่นอก image",
            "- ไม่ตัด PE SecurityCookie check ออกจาก UNKNOWN เพียงเพราะ success path return และ compare global ตรง Load Configuration; failure tail target `0x00B38352`/file offset `0x00737752` ยังไม่ถูกพิสูจน์ผลต่อ wire path จึงระบุเฉพาะ exact guard shape และคง failure-path blocker",
            "- ไม่รวม register-indirect import call ที่มี reaching definition หลายจุดไว้ใน singleton rule แม้ symbolic target จะลดรูปเป็น IAT เดียวกัน; กฎ multi-register รับเฉพาะ complete reaching set อย่างน้อย 2 จุดโดยไม่มี undefined path และทุกจุดต้องเป็น exact unprefixed `mov` ของ register/IAT เดียวกับ call; definition แบบผสม, register/IAT ไม่ตรง หรือ path ที่ยังไม่มี definition ยังคง generic UNKNOWN",
            "- ไม่ประกาศฟังก์ชันว่า EMPTY เพียงเพราะไม่พบ WRITE/READ; นอกจาก body `ret`/`ret 8` ล้วน รับ exact allowlist ของ constant-return, absolute-global predicate, argument-value copiers, conditional object init และ FPSTest entry CFG เท่านั้น; FPSTest ต้องตรง full span 156 bytes และ re-derive 24 reachable instructions ก่อน `CC CC` โดยห้ามลากคำอ้างไปยัง suffix entry `0x0073E900` ส่วนกฎอื่นยังคงไม่อ่าน stack argument ไม่มี call/tail หรือไม่ dereference ค่า argumentตามชนิด จึงพิสูจน์ได้เพียงว่าไม่มี wire field ในเส้นทางที่ระบุ ไม่ใช่ว่า class/module ไม่มีพฤติกรรมด้านอื่น",
            "",
        ]
    )
    return "\n".join(lines)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def default_image_path() -> Path:
    return Path(__file__).resolve().parents[2] / "GameClient" / "GameClient.local.bin"


def write_utf8(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def validate_registry_acceptance(image: Image, rows: list[RegistryRow]) -> None:
    """Re-derive the complete ambiguous-getter RTTI escape-hatch census."""
    _validate_eof_vtable_candidate_boundary(image)
    for section in image.sections:
        if section.raw_size < 4:
            continue
        edge_va = section.va + section.raw_size - 4
        if (
            image.va_range_to_off(edge_va, 4) != section.raw_end - 4
            or image.va_range_to_off(edge_va, 5) is not None
        ):
            raise ExtractionError("PE same-section VA range acceptance mismatch")
    by_name = {row.name: row for row in rows}
    wanted_getters = {
        row.getter_va for row in rows if row.getter_va is not None
    }
    candidates_by_getter: dict[int, list[tuple[int, int]]] = defaultdict(list)
    pointer_offsets = _vtable_getter_pointer_offsets(len(image.data))
    if (
        pointer_offsets.start != 16
        or pointer_offsets.step != 4
        or not pointer_offsets
        or pointer_offsets[-1] != len(image.data) - 16
    ):
        raise ExtractionError("A1 vtable full-file sweep boundary mismatch")
    for pointer_off in pointer_offsets:
        getter_va = image.u32_off(pointer_off)
        if getter_va not in wanted_getters:
            continue
        if image.u32_off(pointer_off - 8) != VTABLE_MARKER_VA:
            continue
        vtable_off = pointer_off - 16
        vtable_va = image.off_to_va(vtable_off)
        if (
            vtable_va is not None
            and image.va_range_to_off(vtable_va, 0x20) == vtable_off
        ):
            candidates_by_getter[getter_va].append(
                (vtable_va, pointer_off)
            )
    ambiguous = {
        row.name: tuple(candidates_by_getter[row.getter_va])
        for row in rows
        if row.getter_va is not None
        and len(candidates_by_getter[row.getter_va]) > 1
    }
    expected_ambiguous = {
        "ItemAttr": (
            (0x00F0EBB0, 0x00B0CFC0),
            (0x00F4A188, 0x00B48598),
        ),
        "VitalData": (
            (0x00F0B930, 0x00B09D40),
            (0x00F375FC, 0x00B35A0C),
        ),
        "PcThreadRunObject": (
            (0x00F86F04, 0x00B85314),
            (0x00F86F90, 0x00B853A0),
            (0x00F933F8, 0x00B91808),
        ),
    }
    if ambiguous != expected_ambiguous:
        raise ExtractionError("A1 ambiguous vtable candidate census mismatch")
    measured_candidate_slots = {
        name: tuple(
            (
                vtable_va,
                pointer_off,
                image.u32_off(pointer_off + 8),
                pointer_off + 8,
                image.u32_off(pointer_off + 12),
                pointer_off + 12,
            )
            for vtable_va, pointer_off in candidates
        )
        for name, candidates in ambiguous.items()
    }
    expected_candidate_slots = {
        "ItemAttr": (
            (0x00F0EBB0, 0x00B0CFC0, 0x0043BB80, 0x00B0CFC8, 0x0046B530, 0x00B0CFCC),
            (0x00F4A188, 0x00B48598, 0x0043BB80, 0x00B485A0, 0x0046B530, 0x00B485A4),
        ),
        "VitalData": (
            (0x00F0B930, 0x00B09D40, 0x00B3798C, 0x00B09D48, 0x00B3798C, 0x00B09D4C),
            (0x00F375FC, 0x00B35A0C, 0x0065AD40, 0x00B35A14, 0x00B3798C, 0x00B35A18),
        ),
        "PcThreadRunObject": (
            (0x00F86F04, 0x00B85314, 0x008C5AE0, 0x00B8531C, 0x004CD2F0, 0x00B85320),
            (0x00F86F90, 0x00B853A0, 0x008C5AE0, 0x00B853A8, 0x004CD2F0, 0x00B853AC),
            (0x00F933F8, 0x00B91808, 0x008C5AE0, 0x00B91810, 0x004CD2F0, 0x00B91814),
        ),
    }
    if measured_candidate_slots != expected_candidate_slots:
        raise ExtractionError("A1 ambiguous candidate slot census mismatch")
    rtti_matches = {
        name: tuple(
            (vtable_va, pointer_off, proof)
            for vtable_va, pointer_off in candidates
            for proof in (
                _rtti_vtable_name_proof(image, name, vtable_va),
            )
            if proof is not None
        )
        for name, candidates in ambiguous.items()
    }
    pc_proof = _rtti_vtable_name_proof(
        image, "PcThreadRunObject", 0x00F86F04
    )
    pc = by_name.get("PcThreadRunObject")
    item = by_name.get("ItemAttr")
    vital = by_name.get("VitalData")
    item_serializer_invariant = _candidate_invariant_executable_slot(
        image, ambiguous["ItemAttr"], 8, "serializer"
    )
    item_handler_invariant = _candidate_invariant_executable_slot(
        image, ambiguous["ItemAttr"], 12, "handler"
    )
    vital_serializer_invariant = _candidate_invariant_executable_slot(
        image, ambiguous["VitalData"], 8, "serializer"
    )
    vital_handler_invariant = _candidate_invariant_executable_slot(
        image, ambiguous["VitalData"], 12, "handler"
    )
    if (
        pc_proof is None
        or item_serializer_invariant is None
        or item_handler_invariant is None
        or vital_serializer_invariant is not None
        or vital_handler_invariant is None
        or rtti_matches
        != {
            "ItemAttr": (),
            "VitalData": (),
            "PcThreadRunObject": (
                (0x00F86F04, 0x00B85314, pc_proof),
            ),
        }
        or pc is None
        or (
            pc.getter_va,
            pc.vtable_va,
            pc.serializer_va,
            pc.handler_va,
            pc.reason,
            pc.resolution_proof,
        )
        != (
            0x00A8DF80,
            0x00F86F04,
            0x008C5AE0,
            0x004CD2F0,
            "",
            pc_proof,
        )
        or pc.serializer_pointer_offs != (0x00B8531C,)
        or pc.handler_pointer_offs != (0x00B85320,)
        or pc.serializer_resolution_proof
        or pc.handler_resolution_proof
        or item is None
        or item.reason != "vtable_hits=2"
        or item.vtable_va is not None
        or item.serializer_va != 0x0043BB80
        or item.handler_va != 0x0046B530
        or item.resolution_proof
        or item.serializer_pointer_offs != (0x00B0CFC8, 0x00B485A0)
        or item.handler_pointer_offs != (0x00B0CFCC, 0x00B485A4)
        or item.serializer_resolution_proof != item_serializer_invariant[2]
        or item.handler_resolution_proof != item_handler_invariant[2]
        or vital is None
        or vital.reason != "vtable_hits=2"
        or vital.vtable_va is not None
        or vital.serializer_va is not None
        or vital.handler_va != 0x00B3798C
        or vital.resolution_proof
        or vital.serializer_pointer_offs != (0x00B09D48, 0x00B35A14)
        or vital.handler_pointer_offs != (0x00B09D4C, 0x00B35A18)
        or vital.serializer_resolution_proof
        or vital.handler_resolution_proof != vital_handler_invariant[2]
        or {row.name for row in rows if row.resolution_proof}
        != {"PcThreadRunObject"}
        or {row.name for row in rows if row.serializer_resolution_proof}
        != {"ItemAttr"}
        or {row.name for row in rows if row.handler_resolution_proof}
        != {"ItemAttr", "VitalData"}
        or sum(row.getter_va is None for row in rows) != 15
        or sum(row.vtable_va is None for row in rows) != 17
        or sum(row.serializer_va is None for row in rows) != 16
        or sum(row.handler_va is None for row in rows) != 15
    ):
        raise ExtractionError("A1 exact RTTI vtable resolution mismatch")


def validate_string_wire_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    """Fail closed on every byte/import fact used to name four wire helpers."""
    measured_semantics = {
        target_va: (spec.direction, spec.tag, spec.string_kind)
        for target_va, spec in STRING_WIRE_HELPERS.items()
    }
    if measured_semantics != EXPECTED_STRING_WIRE_SEMANTICS:
        raise ExtractionError("string wire helper semantic oracle mismatch")
    if set(STRING_WIRE_IMPORTS) != {
        iat
        for spec in STRING_WIRE_HELPERS.values()
        for iat in spec.required_iats
    }:
        raise ExtractionError("string wire helper import coverage mismatch")
    helper_instructions: dict[int, Instruction] = {}
    for target_va, spec in sorted(STRING_WIRE_HELPERS.items()):
        length = spec.proof_end_va - target_va
        mapped = image.va_range_to_off(target_va, length)
        body = image.data[spec.start_off : spec.start_off + length]
        if (
            length <= 0
            or mapped != spec.start_off
            or image.off_to_va(spec.start_off) != target_va
            or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        ):
            raise ExtractionError(
                "string wire helper span mismatch at 0x%08X" % target_va
            )
        proof_span = FunctionSpan(
            target_va,
            spec.proof_end_va,
            spec.start_off,
            spec.start_off + length,
            spec.proof_sha256,
        )
        decoded = decode_function(image, proof_span)
        if (
            decoded.errors
            or decoded.span != proof_span
            or target_va not in decoded.instructions
            or analyzer._function_abi(decoded) != ("thiscall", 1)
            or analyzer._decoded_cleanup(decoded) != 4
        ):
            raise ExtractionError(
                "string wire helper ABI/decode mismatch at 0x%08X"
                % target_va
            )
        for site_va, ins in decoded.instructions.items():
            if site_va in helper_instructions:
                raise ExtractionError("overlapping string wire helper decode")
            helper_instructions[site_va] = ins
        for iat_va in spec.required_iats:
            symbol = image.imports_by_iat.get(iat_va)
            expected_symbol = STRING_WIRE_IMPORTS.get(iat_va)
            if (
                symbol is None
                or expected_symbol is None
                or (symbol.dll, symbol.name) != expected_symbol
                or image.va_to_off(iat_va) != symbol.iat_off
            ):
                raise ExtractionError(
                    "string wire helper import mismatch at IAT 0x%08X"
                    % iat_va
                )
    for call_va, iat_va in sorted(STRING_WIRE_IAT_CALLS.items()):
        ins = helper_instructions.get(call_va)
        if (
            ins is None
            or ins.kind != "call_indirect"
            or ins.src is None
            or ins.src.kind != "mem"
            or ins.src.absolute != iat_va
        ):
            raise ExtractionError(
                "string wire helper IAT call mismatch at 0x%08X" % call_va
            )
    for call_va in sorted(STRING_WIRE_MEMCPY_CALLS):
        ins = helper_instructions.get(call_va)
        if ins is None or ins.kind != "call" or ins.target != 0x00B37B80:
            raise ExtractionError(
                "string wire helper memcpy call mismatch at 0x%08X" % call_va
            )
    thunk_body = image.data[0x00736F80 : 0x00736F86]
    thunk_span = FunctionSpan(
        0x00B37B80,
        0x00B37B86,
        0x00736F80,
        0x00736F86,
        hashlib.sha256(thunk_body).hexdigest(),
    )
    thunk_decode = decode_function(image, thunk_span)
    thunk = thunk_decode.instructions.get(0x00B37B80)
    if (
        thunk_decode.errors
        or thunk is None
        or thunk.kind != "jmp_indirect"
        or thunk.src is None
        or thunk.src.kind != "mem"
        or thunk.src.absolute != 0x00C3B504
        or thunk.raw != bytes.fromhex("FF2504B5C300")
    ):
        raise ExtractionError("string wire helper memcpy thunk mismatch")
    for va, expected_off, expected_hex in STRING_WIRE_KEY_BYTES:
        expected = bytes.fromhex(expected_hex)
        actual_off = image.va_range_to_off(va, len(expected))
        if (
            actual_off != expected_off
            or image.data[expected_off : expected_off + len(expected)]
            != expected
        ):
            raise ExtractionError(
                "string wire helper key bytes mismatch at 0x%08X" % va
            )


def validate_atomic_object_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    """Prove the two helpers' exact operations without naming object types."""
    measured_semantics = {
        target_va: (spec.tag, spec.reason, spec.length, spec.iat_va)
        for target_va, spec in ATOMIC_OBJECT_HELPERS.items()
    }
    if measured_semantics != EXPECTED_ATOMIC_OBJECT_SEMANTICS:
        raise ExtractionError("atomic object helper semantic oracle mismatch")
    for target_va, spec in sorted(ATOMIC_OBJECT_HELPERS.items()):
        expected_body = bytes.fromhex(ATOMIC_OBJECT_HELPER_BYTES[target_va])
        measured_span = analyzer.span(target_va)
        decoded = analyzer.decode(target_va)
        symbol = image.imports_by_iat.get(spec.iat_va)
        expected_symbol = ATOMIC_OBJECT_IMPORTS.get(spec.iat_va)
        expected_span = FunctionSpan(
            target_va,
            spec.proof_end_va,
            spec.start_off,
            spec.start_off + len(expected_body),
            spec.proof_sha256,
        )
        if (
            spec.proof_end_va - target_va != len(expected_body)
            or image.va_range_to_off(target_va, len(expected_body))
            != spec.start_off
            or image.data[
                spec.start_off : spec.start_off + len(expected_body)
            ]
            != expected_body
            or hashlib.sha256(expected_body).hexdigest()
            != spec.proof_sha256
            or measured_span != expected_span
            or decoded is None
            or decoded.errors
            or decoded.span != expected_span
            or analyzer._decoded_cleanup(decoded) != 0
            or symbol is None
            or expected_symbol is None
            or (symbol.dll, symbol.name) != expected_symbol
            or image.va_to_off(spec.iat_va) != symbol.iat_off
        ):
            raise ExtractionError(
                "atomic object helper definition mismatch at 0x%08X"
                % target_va
            )
        primitive_calls = {
            ins.va
            for ins in decoded.instructions.values()
            if ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
        }
        if primitive_calls:
            raise ExtractionError("atomic object helper reached wire primitive")
    increment = analyzer.decode(0x0088D050)
    decrement = analyzer.decode(0x0088D060)
    increment_import = (
        None if increment is None else increment.instructions.get(0x0088D054)
    )
    decrement_import = (
        None if decrement is None else decrement.instructions.get(0x0088D067)
    )
    dynamic_call = (
        None if decrement is None else decrement.instructions.get(0x0088D07E)
    )
    vtable_load = (
        None if decrement is None else decrement.instructions.get(0x0088D077)
    )
    direct_increment = analyzer.decode(0x004A06A0)
    direct_decrement = analyzer.decode(0x004A06B0)
    direct_increment_import = (
        None
        if direct_increment is None
        else direct_increment.instructions.get(0x004A06A1)
    )
    direct_decrement_import = (
        None
        if direct_decrement is None
        else direct_decrement.instructions.get(0x004A06B1)
    )
    if (
        direct_increment_import is None
        or direct_increment_import.kind != "call_indirect"
        or direct_increment_import.src
        != Operand("mem", absolute=0x00C3B1B0)
        or direct_decrement_import is None
        or direct_decrement_import.kind != "call_indirect"
        or direct_decrement_import.src
        != Operand("mem", absolute=0x00C3B1B4)
        or increment_import is None
        or increment_import.kind != "call_indirect"
        or increment_import.src is None
        or increment_import.src.kind != "mem"
        or increment_import.src.absolute != 0x00C3B1B0
        or decrement_import is None
        or decrement_import.kind != "call_indirect"
        or decrement_import.src is None
        or decrement_import.src.kind != "mem"
        or decrement_import.src.absolute != 0x00C3B1B4
        or vtable_load is None
        or vtable_load.kind != "mov"
        or vtable_load.src is None
        or vtable_load.src.kind != "mem"
        or vtable_load.src.base != "edx"
        or vtable_load.src.disp != 4
        or dynamic_call is None
        or dynamic_call.kind != "call_indirect"
        or dynamic_call.src != Operand("reg", reg="eax")
    ):
        raise ExtractionError("atomic object helper operation shape mismatch")


def validate_pe_security_cookie_check_helper_definitions(
    image: Image,
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.separator_hex,
            spec.security_cookie_va,
            spec.failure_target_va,
        )
        for target_va, spec in PE_SECURITY_COOKIE_CHECK_HELPERS.items()
    }
    if measured_semantics != EXPECTED_PE_SECURITY_COOKIE_CHECK_SEMANTICS:
        raise ExtractionError("PE security-cookie semantic oracle mismatch")

    pe_off = image.u32_off(0x3C)
    size_of_optional_header_off = pe_off + 20
    optional_off = pe_off + 24
    number_of_rva_and_sizes_off = optional_off + 0x5C
    size_of_optional_header = struct.unpack_from(
        "<H", image.data, size_of_optional_header_off
    )[0]
    number_of_rva_and_sizes = image.u32_off(number_of_rva_and_sizes_off)
    load_config_directory_entry_off = optional_off + 96 + (10 * 8)
    load_config_rva = image.u32_off(load_config_directory_entry_off)
    load_config_directory_size = image.u32_off(
        load_config_directory_entry_off + 4
    )
    load_config_va = 0x00400000 + load_config_rva
    load_config_off = image.va_to_off(load_config_va)
    if (
        pe_off != 0x128
        or image.data[pe_off : pe_off + 4] != b"PE\x00\x00"
        or size_of_optional_header_off != 0x13C
        or size_of_optional_header != 0xE0
        or struct.unpack_from("<H", image.data, optional_off)[0] != 0x010B
        or number_of_rva_and_sizes_off != 0x19C
        or number_of_rva_and_sizes != 16
        or load_config_directory_entry_off != 0x1F0
        or image.data[load_config_directory_entry_off : load_config_directory_entry_off + 8]
        != bytes.fromhex("70C5BB0040000000")
        or load_config_rva != 0x00BBC570
        or load_config_directory_size != 0x40
        or load_config_off != 0x00BBA970
        or image.u32_off(load_config_off) != 0x48
        or image.u32_off(load_config_off + 0x3C) != 0x0102B4BC
    ):
        raise ExtractionError("PE security-cookie Load Configuration mismatch")

    for target_va, spec in sorted(PE_SECURITY_COOKIE_CHECK_HELPERS.items()):
        body = bytes.fromhex(spec.body_hex)
        separator = bytes.fromhex(spec.separator_hex)
        end_off = spec.start_off + len(body)
        instructions = tuple(
            decode_instruction(image, va, end_off)
            for va in (0x00B37964, 0x00B3796A, 0x00B3796C, 0x00B3796E)
        )
        if (
            target_va != 0x00B37964
            or spec.proof_end_va != target_va + len(body)
            or image.va_range_to_off(target_va, len(body)) != spec.start_off
            or image.data[spec.start_off:end_off] != body
            or hashlib.sha256(body).hexdigest() != spec.proof_sha256
            or image.data[end_off : end_off + len(separator)] != separator
            or len(separator) != 13
            or instructions[0].raw != bytes.fromhex("3B0DBCB40201")
            or instructions[0].kind != "other"
            or instructions[1].raw != bytes.fromhex("7502")
            or instructions[1].kind != "jcc"
            or instructions[1].target != 0x00B3796E
            or instructions[2].raw != bytes.fromhex("F3C3")
            or instructions[2].kind != "ret"
            or instructions[3].raw != bytes.fromhex("E9DF090000")
            or instructions[3].kind != "jmp"
            or instructions[3].target != spec.failure_target_va
            or spec.security_cookie_va != image.u32_off(load_config_off + 0x3C)
            or image.va_to_off(spec.failure_target_va) != 0x00737752
            or not image.executable_va(spec.failure_target_va)
        ):
            raise ExtractionError(
                "PE security-cookie helper definition mismatch at 0x%08X"
                % target_va
            )


def validate_pe_security_cookie_check_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    if set(EXPECTED_PE_SECURITY_COOKIE_CHECK_ROW_CENSUS) != set(
        PE_SECURITY_COOKIE_CHECK_HELPERS
    ):
        raise ExtractionError("PE security-cookie row oracle mismatch")
    for target_va, spec in sorted(PE_SECURITY_COOKIE_CHECK_HELPERS.items()):
        helper_rows = [row for row in rows if row.tag == spec.tag]
        pattern = re.compile(
            r"(?:^| AND )pe_security_cookie_check_call@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"target=0x%08X call_bytes=([0-9A-F]{10})(?: AND |$)"
            % target_va
        )
        directions = Counter()
        unique_sites = set()
        function_vas = set()
        messages = set()
        for row in helper_rows:
            match = pattern.search(row.gate_condition)
            if match is None:
                raise ExtractionError(
                    "PE security-cookie row lacks call proof"
                )
            call_va, call_off, function_va = (
                int(text, 16) for text in match.groups()[:3]
            )
            call_bytes = bytes.fromhex(match.group(4))
            decoded = analyzer.decode(function_va)
            ins = None if decoded is None else decoded.instructions.get(call_va)
            if (
                decoded is None
                or ins is None
                or ins.kind != "call"
                or ins.target != target_va
                or ins.raw != call_bytes
                or ins.raw[:1] != b"\xE8"
                or ins.off != call_off
                or row.file_off_claim != call_off
                or row.span_start != function_va
                or row.direction not in ("W", "R")
                or row.length != "N/A"
                or row.field_offset != "UNKNOWN(%s)" % spec.reason
                or row.reason != spec.reason
                or pe_security_cookie_check_helper_fragment(
                    image, target_va
                )
                not in row.gate_condition
            ):
                raise ExtractionError(
                    "PE security-cookie row mismatch at 0x%08X" % call_va
                )
            directions[row.direction] += 1
            unique_sites.add((function_va, call_va))
            function_vas.add(function_va)
            messages.add(row.message)
        raw_sites = {
            (function_va, ins.va)
            for function_va in function_vas
            for decoded in (analyzer.decode(function_va),)
            if decoded is not None
            for ins in decoded.instructions.values()
            if ins.kind == "call" and ins.target == target_va
        }
        actual = (
            len(helper_rows),
            directions["W"],
            directions["R"],
            len(unique_sites),
            len(messages),
        )
        if (
            actual != EXPECTED_PE_SECURITY_COOKIE_CHECK_ROW_CENSUS[target_va]
            or raw_sites != unique_sites
            or any(
                row.tag == "CALL_UNCLASSIFIED:0x%08X" % target_va
                for row in rows
            )
        ):
            raise ExtractionError(
                "PE security-cookie row census mismatch at 0x%08X"
                % target_va
            )


def validate_exact_import_thunk_call_definitions(image: Image) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.iat_va,
            spec.dll,
            spec.symbol,
            spec.thunk_bytes_hex,
        )
        for target_va, spec in EXACT_IMPORT_THUNK_CALLS.items()
    }
    if measured_semantics != EXPECTED_EXACT_IMPORT_THUNK_CALL_SEMANTICS:
        raise ExtractionError("exact import thunk semantic oracle mismatch")
    if len({spec.tag for spec in EXACT_IMPORT_THUNK_CALLS.values()}) != len(
        EXACT_IMPORT_THUNK_CALLS
    ):
        raise ExtractionError("exact import thunk tags are not unique")
    for target_va, spec in sorted(EXACT_IMPORT_THUNK_CALLS.items()):
        expected = bytes.fromhex(spec.thunk_bytes_hex)
        target_off = image.va_range_to_off(target_va, len(expected))
        decoded = (
            None
            if target_off is None
            else decode_instruction(image, target_va, target_off + len(expected))
        )
        symbol = image.imports_by_iat.get(spec.iat_va)
        if (
            target_off != spec.start_off
            or image.data[spec.start_off : spec.start_off + len(expected)]
            != expected
            or expected != b"\xFF\x25" + struct.pack("<I", spec.iat_va)
            or decoded is None
            or decoded.kind != "jmp_indirect"
            or decoded.va != target_va
            or decoded.off != spec.start_off
            or decoded.size != 6
            or decoded.raw != expected
            or decoded.src != Operand("mem", absolute=spec.iat_va)
            or symbol is None
            or (symbol.dll, symbol.name) != (spec.dll, spec.symbol)
            or image.va_to_off(spec.iat_va) != symbol.iat_off
        ):
            raise ExtractionError(
                "exact import thunk definition mismatch at 0x%08X"
                % target_va
            )


def validate_exact_import_thunk_call_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    if set(EXPECTED_EXACT_IMPORT_THUNK_CALL_ROW_CENSUS) != set(
        EXACT_IMPORT_THUNK_CALLS
    ):
        raise ExtractionError("exact import thunk row oracle mismatch")
    total_rows = 0
    all_unique_sites = set()
    for target_va, spec in sorted(EXACT_IMPORT_THUNK_CALLS.items()):
        helper_rows = [row for row in rows if row.tag == spec.tag]
        pattern = re.compile(
            r"(?:^| AND )exact_rel32_import_thunk_call@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"target=0x%08X call_bytes=([0-9A-F]{10})(?: AND |$)"
            % target_va
        )
        directions = Counter()
        unique_sites = set()
        function_vas = set()
        messages = set()
        for row in helper_rows:
            match = pattern.search(row.gate_condition)
            if match is None:
                raise ExtractionError(
                    "exact import thunk row lacks call proof"
                )
            call_va, call_off, function_va = (
                int(text, 16) for text in match.groups()[:3]
            )
            call_bytes = bytes.fromhex(match.group(4))
            decoded = analyzer.decode(function_va)
            ins = None if decoded is None else decoded.instructions.get(call_va)
            if (
                decoded is None
                or ins is None
                or ins.kind != "call"
                or ins.target != target_va
                or ins.raw != call_bytes
                or ins.raw[:1] != b"\xE8"
                or ins.off != call_off
                or row.file_off_claim != call_off
                or row.span_start != function_va
                or row.direction not in ("W", "R")
                or row.length != "N/A"
                or row.field_offset != "UNKNOWN(%s)" % spec.reason
                or row.reason != spec.reason
                or exact_import_thunk_call_fragment(image, target_va)
                not in row.gate_condition
            ):
                raise ExtractionError(
                    "exact import thunk row mismatch at 0x%08X" % call_va
                )
            directions[row.direction] += 1
            unique_sites.add((function_va, call_va))
            function_vas.add(function_va)
            messages.add(row.message)
        raw_sites = {
            (function_va, ins.va)
            for function_va in function_vas
            for decoded in (analyzer.decode(function_va),)
            if decoded is not None
            for ins in decoded.instructions.values()
            if ins.kind == "call" and ins.target == target_va
        }
        expected = EXPECTED_EXACT_IMPORT_THUNK_CALL_ROW_CENSUS[target_va]
        actual = (
            len(helper_rows),
            directions["W"],
            directions["R"],
            len(unique_sites),
            len(messages),
        )
        if (
            actual != expected
            or raw_sites != unique_sites
            or any(
                row.tag == "CALL_UNCLASSIFIED:0x%08X" % target_va
                for row in rows
            )
        ):
            raise ExtractionError(
                "exact import thunk row census mismatch at 0x%08X"
                % target_va
            )
        total_rows += len(helper_rows)
        all_unique_sites.update(unique_sites)

    remaining_exact_import_thunks = set()
    for row in rows:
        match = re.fullmatch(
            r"CALL_UNCLASSIFIED:0x([0-9A-F]{8})", row.tag
        )
        if match is None:
            continue
        target_va = int(match.group(1), 16)
        target_off = image.va_range_to_off(target_va, 6)
        if target_off is None or image.data[target_off : target_off + 2] != b"\xFF\x25":
            continue
        iat_va = image.u32_off(target_off + 2)
        if iat_va in image.imports_by_iat:
            remaining_exact_import_thunks.add(target_va)
    if (
        total_rows != 16
        or len(all_unique_sites) != 5
        or remaining_exact_import_thunks
    ):
        raise ExtractionError("exact import thunk complete census mismatch")


def validate_exact_direct_import_call_definitions(image: Image) -> None:
    measured_semantics = {
        iat_va: (
            spec.tag,
            spec.reason,
            spec.dll,
            spec.symbol,
            spec.call_bytes_hex,
        )
        for iat_va, spec in EXACT_DIRECT_IMPORT_CALLS.items()
    }
    if measured_semantics != EXPECTED_EXACT_DIRECT_IMPORT_CALL_SEMANTICS:
        raise ExtractionError("exact direct import semantic oracle mismatch")
    for iat_va, spec in sorted(EXACT_DIRECT_IMPORT_CALLS.items()):
        symbol = image.imports_by_iat.get(iat_va)
        if (
            symbol is None
            or (symbol.dll, symbol.name) != (spec.dll, spec.symbol)
            or image.va_to_off(iat_va) != symbol.iat_off
            or bytes.fromhex(spec.call_bytes_hex)
            != b"\xFF\x15" + struct.pack("<I", iat_va)
        ):
            raise ExtractionError(
                "exact direct import definition mismatch at 0x%08X" % iat_va
            )


def validate_exact_direct_import_call_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    spec = EXACT_DIRECT_IMPORT_CALLS[0x00C3B4C0]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )exact_direct_iat_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"iat=0x00C3B4C0 bytes=FF15C0B4C300(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    function_vas = set()
    messages = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError("exact direct import row lacks call proof")
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call_indirect"
            or ins.src != Operand("mem", absolute=0x00C3B4C0)
            or ins.raw != bytes.fromhex(spec.call_bytes_hex)
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset
            != "UNKNOWN(invalid_parameter_import_call_wire_effect_unproved)"
            or row.reason != spec.reason
            or exact_direct_import_call_fragment(image, 0x00C3B4C0)
            not in row.gate_condition
        ):
            raise ExtractionError(
                "exact direct import row mismatch at 0x%08X" % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
        function_vas.add(function_va)
        messages.add(row.message)
    raw_sites = {
        (function_va, ins.va)
        for function_va in function_vas
        for decoded in (analyzer.decode(function_va),)
        if decoded is not None
        for ins in decoded.instructions.values()
        if ins.kind == "call_indirect"
        and ins.src == Operand("mem", absolute=0x00C3B4C0)
        and ins.raw == bytes.fromhex(spec.call_bytes_hex)
    }
    remaining_symbolic_rows = [
        row
        for row in rows
        if row.tag
        == "CALL_UNCLASSIFIED:INDIRECT(DEREF(ABS(0x00C3B4C0)))"
    ]
    remaining_are_register_indirect = True
    for row in remaining_symbolic_rows:
        call_va = (
            None
            if row.file_off_claim is None
            else image.off_to_va(row.file_off_claim)
        )
        decoded = (
            None
            if row.span_start is None
            else analyzer.decode(row.span_start)
        )
        ins = (
            None
            if decoded is None or call_va is None
            else decoded.instructions.get(call_va)
        )
        if (
            ins is None
            or ins.kind != "call_indirect"
            or ins.src is None
            or ins.src.kind != "reg"
            or ins.src.reg is None
            or not analyzer._is_exact_register_indirect_call(
                ins, ins.src.reg
            )
        ):
            remaining_are_register_indirect = False
            break
    if (
        len(helper_rows) != 638
        or directions != Counter({"W": 337, "R": 301})
        or len(unique_sites) != 231
        or len(messages) != 68
        or raw_sites != unique_sites
        or not remaining_are_register_indirect
    ):
        raise ExtractionError("exact direct import row census mismatch")


def validate_other_exact_direct_import_call_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    if (
        set(EXPECTED_OTHER_EXACT_DIRECT_IMPORT_CALL_ROW_CENSUS)
        != set(OTHER_EXACT_DIRECT_IMPORT_CALL_IATS)
        or len(
            {
                EXACT_DIRECT_IMPORT_CALLS[iat_va].tag
                for iat_va in OTHER_EXACT_DIRECT_IMPORT_CALL_IATS
            }
        )
        != len(OTHER_EXACT_DIRECT_IMPORT_CALL_IATS)
    ):
        raise ExtractionError("other exact direct import census oracle mismatch")
    total_rows = 0
    all_unique_sites = set()
    for iat_va in sorted(OTHER_EXACT_DIRECT_IMPORT_CALL_IATS):
        spec = EXACT_DIRECT_IMPORT_CALLS[iat_va]
        helper_rows = [row for row in rows if row.tag == spec.tag]
        pattern = re.compile(
            r"(?:^| AND )exact_direct_iat_call@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"iat=0x%08X bytes=%s(?: AND |$)"
            % (iat_va, spec.call_bytes_hex)
        )
        directions = Counter()
        unique_sites = set()
        function_vas = set()
        messages = set()
        for row in helper_rows:
            match = pattern.search(row.gate_condition)
            if match is None:
                raise ExtractionError(
                    "other exact direct import row lacks call proof"
                )
            call_va, call_off, function_va = (
                int(text, 16) for text in match.groups()
            )
            decoded = analyzer.decode(function_va)
            ins = None if decoded is None else decoded.instructions.get(call_va)
            if (
                decoded is None
                or ins is None
                or ins.kind != "call_indirect"
                or ins.src != Operand("mem", absolute=iat_va)
                or ins.raw != bytes.fromhex(spec.call_bytes_hex)
                or ins.off != call_off
                or row.file_off_claim != call_off
                or row.span_start != function_va
                or row.direction not in ("W", "R")
                or row.length != "N/A"
                or row.field_offset != "UNKNOWN(%s)" % spec.reason
                or row.reason != spec.reason
                or exact_direct_import_call_fragment(image, iat_va)
                not in row.gate_condition
            ):
                raise ExtractionError(
                    "other exact direct import row mismatch at 0x%08X"
                    % call_va
                )
            directions[row.direction] += 1
            unique_sites.add((function_va, call_va))
            function_vas.add(function_va)
            messages.add(row.message)
        raw_sites = {
            (function_va, ins.va)
            for function_va in function_vas
            for decoded in (analyzer.decode(function_va),)
            if decoded is not None
            for ins in decoded.instructions.values()
            if ins.kind == "call_indirect"
            and ins.src == Operand("mem", absolute=iat_va)
            and ins.raw == bytes.fromhex(spec.call_bytes_hex)
        }
        expected = EXPECTED_OTHER_EXACT_DIRECT_IMPORT_CALL_ROW_CENSUS[iat_va]
        actual = (
            len(helper_rows),
            directions["W"],
            directions["R"],
            len(unique_sites),
            len(messages),
        )
        generic_tag = (
            "CALL_UNCLASSIFIED:INDIRECT(DEREF(ABS(0x%08X)))" % iat_va
        )
        if (
            actual != expected
            or raw_sites != unique_sites
            or any(row.tag == generic_tag for row in rows)
        ):
            raise ExtractionError(
                "other exact direct import row census mismatch at 0x%08X"
                % iat_va
            )
        total_rows += len(helper_rows)
        all_unique_sites.update(unique_sites)
    if total_rows != 128 or len(all_unique_sites) != 36:
        raise ExtractionError("other exact direct import total census mismatch")


def validate_exact_singleton_register_import_call_definitions(
    image: Image,
) -> None:
    measured_semantics = {
        iat_va: (spec.tag, spec.reason, spec.dll, spec.symbol)
        for iat_va, spec in EXACT_SINGLETON_REGISTER_IMPORT_CALLS.items()
    }
    if (
        measured_semantics
        != EXPECTED_EXACT_SINGLETON_REGISTER_IMPORT_CALL_SEMANTICS
    ):
        raise ExtractionError(
            "singleton register import semantic oracle mismatch"
        )
    for iat_va, spec in sorted(
        EXACT_SINGLETON_REGISTER_IMPORT_CALLS.items()
    ):
        symbol = image.imports_by_iat.get(iat_va)
        if (
            symbol is None
            or (symbol.dll, symbol.name) != (spec.dll, spec.symbol)
            or image.va_to_off(iat_va) != symbol.iat_off
        ):
            raise ExtractionError(
                "singleton register import definition mismatch at 0x%08X"
                % iat_va
            )


def validate_exact_singleton_register_import_call_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    spec = EXACT_SINGLETON_REGISTER_IMPORT_CALLS[0x00C3B4C0]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )exact_singleton_register_iat_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
        r"definition@0x([0-9A-F]{8}) definition_file_off=0x([0-9A-F]{8}) "
        r"iat=0x00C3B4C0 call_bytes=([0-9A-F]{4}) "
        r"definition_bytes=([0-9A-F]{12})(?: |$)"
    )
    directions = Counter()
    unique_sites = set()
    function_vas = set()
    messages = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError(
                "singleton register import row lacks call/load proof"
            )
        (
            call_text,
            call_off_text,
            function_text,
            register,
            definition_text,
            definition_off_text,
            call_bytes_text,
            definition_bytes_text,
        ) = match.groups()
        call_va = int(call_text, 16)
        call_off = int(call_off_text, 16)
        function_va = int(function_text, 16)
        definition_va = int(definition_text, 16)
        definition_off = int(definition_off_text, 16)
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        definition = (
            None
            if decoded is None
            else decoded.instructions.get(definition_va)
        )
        symbol = image.imports_by_iat[0x00C3B4C0]
        proof = (
            None
            if ins is None
            else analyzer._stack_neutral_register_import(function_va, ins)
        )
        if (
            decoded is None
            or ins is None
            or definition is None
            or proof != (symbol, register, definition_va)
            or not analyzer._is_exact_register_indirect_call(ins, register)
            or not analyzer._is_exact_iat_register_load(
                definition, register, 0x00C3B4C0
            )
            or ins.raw.hex().upper() != call_bytes_text
            or definition.raw.hex().upper() != definition_bytes_text
            or ins.off != call_off
            or image.va_to_off(definition_va) != definition_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset
            != "UNKNOWN(invalid_parameter_singleton_register_call_wire_effect_unproved)"
            or row.reason != spec.reason
            or exact_singleton_register_import_call_fragment(
                image,
                function_va,
                call_va,
                register,
                definition_va,
                0x00C3B4C0,
            )
            not in row.gate_condition
        ):
            raise ExtractionError(
                "singleton register import row mismatch at 0x%08X" % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
        function_vas.add(function_va)
        messages.add(row.message)
    proved_sites = set()
    for function_va in function_vas:
        decoded = analyzer.decode(function_va)
        if decoded is None:
            continue
        for ins in decoded.instructions.values():
            if ins.kind != "call_indirect":
                continue
            proof = analyzer._stack_neutral_register_import(function_va, ins)
            if proof is not None and proof[0].iat_va == 0x00C3B4C0:
                proved_sites.add((function_va, ins.va))
    if (
        len(helper_rows) != 179
        or directions != Counter({"W": 105, "R": 74})
        or len(unique_sites) != 66
        or len(messages) != 25
        or proved_sites != unique_sites
        or sum(
            row.tag
            == "CALL_UNCLASSIFIED:INDIRECT(DEREF(ABS(0x00C3B4C0)))"
            for row in rows
        )
        != (0 if EXACT_MULTI_REGISTER_IMPORT_CALLS else 10)
    ):
        raise ExtractionError("singleton register import row census mismatch")


def validate_exact_multi_register_import_call_definitions(
    image: Image,
) -> None:
    measured_semantics = {
        iat_va: (spec.tag, spec.reason, spec.dll, spec.symbol)
        for iat_va, spec in EXACT_MULTI_REGISTER_IMPORT_CALLS.items()
    }
    if measured_semantics != EXPECTED_EXACT_MULTI_REGISTER_IMPORT_CALL_SEMANTICS:
        raise ExtractionError("multi register import semantic oracle mismatch")
    for iat_va, spec in sorted(EXACT_MULTI_REGISTER_IMPORT_CALLS.items()):
        symbol = image.imports_by_iat.get(iat_va)
        if (
            symbol is None
            or (symbol.dll, symbol.name) != (spec.dll, spec.symbol)
            or image.va_to_off(iat_va) != symbol.iat_off
        ):
            raise ExtractionError(
                "multi register import definition mismatch at 0x%08X" % iat_va
            )


def validate_exact_multi_register_import_call_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    spec = EXACT_MULTI_REGISTER_IMPORT_CALLS[0x00C3B4C0]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )exact_multi_register_iat_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
        r"definitions=(0x[0-9A-F]{8}(?:,0x[0-9A-F]{8})+) "
        r"definition_file_offs=(0x[0-9A-F]{8}(?:,0x[0-9A-F]{8})+) "
        r"iat=0x00C3B4C0 call_bytes=([0-9A-F]{4}) "
        r"definition_bytes=([0-9A-F]{12}) definition_count=([0-9]+)(?: |$)"
    )
    directions = Counter()
    unique_sites = set()
    function_vas = set()
    messages = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError(
                "multi register import row lacks complete reaching proof"
            )
        (
            call_text,
            call_off_text,
            function_text,
            register,
            definitions_text,
            definition_offs_text,
            call_bytes_text,
            definition_bytes_text,
            definition_count_text,
        ) = match.groups()
        call_va = int(call_text, 16)
        call_off = int(call_off_text, 16)
        function_va = int(function_text, 16)
        definition_vas = tuple(
            int(text, 16) for text in definitions_text.split(",")
        )
        definition_offs = tuple(
            int(text, 16) for text in definition_offs_text.split(",")
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        definitions = (
            ()
            if decoded is None
            else tuple(
                decoded.instructions.get(definition_va)
                for definition_va in definition_vas
            )
        )
        symbol = image.imports_by_iat[0x00C3B4C0]
        proof = (
            None
            if ins is None
            else analyzer._all_same_register_import(function_va, ins)
        )
        if (
            decoded is None
            or ins is None
            or any(definition is None for definition in definitions)
            or proof != (symbol, register, definition_vas)
            or len(definition_vas) != 2
            or len(definition_offs) != len(definition_vas)
            or int(definition_count_text) != len(definition_vas)
            or not analyzer._is_exact_register_indirect_call(ins, register)
            or ins.raw.hex().upper() != call_bytes_text
            or any(
                not analyzer._is_exact_iat_register_load(
                    definition, register, 0x00C3B4C0
                )
                or definition.raw.hex().upper() != definition_bytes_text
                for definition in definitions
                if definition is not None
            )
            or tuple(image.va_to_off(va) for va in definition_vas)
            != definition_offs
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset
            != "UNKNOWN(invalid_parameter_multi_register_call_wire_effect_unproved)"
            or row.reason != spec.reason
            or exact_multi_register_import_call_fragment(
                image,
                function_va,
                call_va,
                register,
                definition_vas,
                0x00C3B4C0,
            )
            not in row.gate_condition
        ):
            raise ExtractionError(
                "multi register import row mismatch at 0x%08X" % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
        function_vas.add(function_va)
        messages.add(row.message)
    proved_sites = set()
    for function_va in function_vas:
        decoded = analyzer.decode(function_va)
        if decoded is None:
            continue
        for ins in decoded.instructions.values():
            if ins.kind != "call_indirect":
                continue
            proof = analyzer._all_same_register_import(function_va, ins)
            if proof is not None and proof[0].iat_va == 0x00C3B4C0:
                proved_sites.add((function_va, ins.va))
    if (
        len(helper_rows) != 10
        or directions != Counter({"W": 8, "R": 2})
        or len(unique_sites) != 6
        or len(messages) != 4
        or proved_sites != unique_sites
        or any(
            row.tag
            == "CALL_UNCLASSIFIED:INDIRECT(DEREF(ABS(0x00C3B4C0)))"
            for row in rows
        )
    ):
        raise ExtractionError("multi register import row census mismatch")



def validate_ecx_plus_50_tail_jump_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.separator_hex,
            spec.tail_target_va,
        )
        for target_va, spec in ECX_PLUS_50_TAIL_JUMP_HELPERS.items()
    }
    if measured_semantics != EXPECTED_ECX_PLUS_50_TAIL_JUMP_SEMANTICS:
        raise ExtractionError("ECX+0x50 tail jump semantic oracle mismatch")
    if not measured_semantics:
        return
    target_va = 0x005F8C30
    spec = ECX_PLUS_50_TAIL_JUMP_HELPERS[target_va]
    body = bytes.fromhex(spec.body_hex)
    separator = bytes.fromhex(spec.separator_hex)
    expected_span = FunctionSpan(
        target_va,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    decoded = decode_function(image, expected_span)
    add_ins = decoded.instructions.get(0x005F8C30)
    jump_ins = decoded.instructions.get(0x005F8C33)
    direct_calls = {
        ins.va: ins.target
        for ins in decoded.instructions.values()
        if ins.kind == "call"
    }
    direct_jumps = {
        ins.va: ins.target
        for ins in decoded.instructions.values()
        if ins.kind == "jmp"
    }
    if (
        len(body) != 8
        or spec.proof_end_va - target_va != len(body)
        or image.va_range_to_off(target_va, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or len(separator) != 8
        or separator != b"\xCC" * 8
        or image.data[
            spec.start_off + len(body) : spec.start_off + len(body) + 8
        ]
        != separator
        or decoded.span != expected_span
        or decoded.errors
        != ("edge_outside_span@0x005F8C33->0x00463800",)
        or len(decoded.instructions) != 2
        or _reachable_nodes(decoded, target_va)
        != frozenset(decoded.instructions)
        or max(ins.next_va for ins in decoded.instructions.values())
        != spec.proof_end_va
        or add_ins is None
        or add_ins.kind != "add"
        or add_ins.raw != b"\x83\xC1\x50"
        or add_ins.dst != Operand("reg", reg="ecx")
        or add_ins.src != Operand("imm", imm=0x50)
        or jump_ins is None
        or jump_ins.kind != "jmp"
        or jump_ins.raw != b"\xE9\xC8\xAB\xE6\xFF"
        or direct_jumps != {0x005F8C33: spec.tail_target_va}
        or direct_calls
        or image.va_to_off(spec.tail_target_va) != 0x00062C00
    ):
        raise ExtractionError("ECX+0x50 tail jump helper definition mismatch")


def validate_ecx_plus_50_tail_jump_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    if not ECX_PLUS_50_TAIL_JUMP_HELPERS:
        return
    target_va = 0x005F8C30
    spec = ECX_PLUS_50_TAIL_JUMP_HELPERS[target_va]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )ecx_plus_50_tail_jump_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x005F8C30(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    messages = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError("ECX+0x50 tail row lacks call proof")
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != target_va
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset != "UNKNOWN(%s)" % spec.reason
            or row.reason != spec.reason
            or ecx_plus_50_tail_jump_helper_fragment(image, target_va)
            not in row.gate_condition
        ):
            raise ExtractionError(
                "ECX+0x50 tail row mismatch at 0x%08X" % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
        messages.add(row.message)
    if (
        len(helper_rows) != 20
        or directions != Counter({"W": 10, "R": 10})
        or len(unique_sites) != 10
        or len(messages) != 8
        or any(row.tag == "CALL_UNCLASSIFIED:0x005F8C30" for row in rows)
    ):
        raise ExtractionError("ECX+0x50 tail row census mismatch")


def validate_nested_call_composition_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.nested_target_vas,
        )
        for target_va, spec in NESTED_CALL_COMPOSITION_HELPERS.items()
    }
    if measured_semantics != EXPECTED_NESTED_CALL_COMPOSITION_SEMANTICS:
        raise ExtractionError(
            "nested call composition semantic oracle mismatch"
        )
    if not measured_semantics:
        return
    target_va = 0x005F8DE0
    spec = NESTED_CALL_COMPOSITION_HELPERS[target_va]
    body = bytes.fromhex(spec.body_hex)
    expected_span = FunctionSpan(
        target_va,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    decoded = decode_function(image, expected_span)
    direct_calls = {
        ins.va: ins.target
        for ins in decoded.instructions.values()
        if ins.kind == "call"
    }
    indirect_calls = {
        ins.va: (ins.src, ins.raw)
        for ins in decoded.instructions.values()
        if ins.kind == "call_indirect"
    }
    explicit_mov_memory_writes = {
        ins.va: (ins.dst, ins.src)
        for ins in decoded.instructions.values()
        if ins.kind == "mov"
        and ins.dst is not None
        and ins.dst.kind == "mem"
    }
    ret_sites = {
        ins.va: ins.imm
        for ins in decoded.instructions.values()
        if ins.kind == "ret"
    }
    result_zero_extend = decoded.instructions.get(0x005F8DF4)
    member_address = decoded.instructions.get(0x005F8DF8)
    if (
        len(body) != 36
        or spec.proof_end_va - target_va != len(body)
        or image.va_range_to_off(target_va, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or analyzer.span(target_va) != expected_span
        or decoded.errors
        or decoded.span != expected_span
        or len(decoded.instructions) != 13
        or _reachable_nodes(decoded, target_va)
        != frozenset(decoded.instructions)
        or max(ins.next_va for ins in decoded.instructions.values())
        != spec.proof_end_va
        or analyzer._decoded_cleanup(decoded) != 4
        or ret_sites != {0x005F8E01: 4}
        or tuple(image.va_to_off(va) for va in spec.nested_target_vas)
        != (0x0049B480, 0x0049A620, 0x00062C00)
        or direct_calls
        != {
            0x005F8DE3: 0x0089C080,
            0x005F8DEF: 0x0089B220,
            0x005F8DFB: 0x00463800,
        }
        or indirect_calls
        or explicit_mov_memory_writes
        or result_zero_extend is None
        or result_zero_extend.raw != b"\x0F\xB7\xC0"
        or member_address is None
        or member_address.raw != b"\x8D\x4E\x50"
        or any(
            ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
            for ins in decoded.instructions.values()
        )
    ):
        raise ExtractionError(
            "nested call composition helper definition mismatch"
        )


def validate_nested_call_composition_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    if not NESTED_CALL_COMPOSITION_HELPERS:
        return
    target_va = 0x005F8DE0
    spec = NESTED_CALL_COMPOSITION_HELPERS[target_va]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )nested_three_call_composition_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x005F8DE0(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    messages = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError(
                "nested call composition row lacks call proof"
            )
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != target_va
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset != "UNKNOWN(%s)" % spec.reason
            or row.reason != spec.reason
            or nested_call_composition_helper_fragment(image, target_va)
            not in row.gate_condition
        ):
            raise ExtractionError(
                "nested call composition row mismatch at 0x%08X" % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
        messages.add(row.message)
    if (
        len(helper_rows) != 28
        or directions != Counter({"W": 14, "R": 14})
        or len(unique_sites) != 14
        or len(messages) != 9
        or any(row.tag == "CALL_UNCLASSIFIED:0x005F8DE0" for row in rows)
    ):
        raise ExtractionError(
            "nested call composition row census mismatch"
        )


def validate_locked_mutable_dword_slot_update_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.invalid_iat_va,
            spec.nested_target_vas,
        )
        for target_va, spec in LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS.items()
    }
    if (
        measured_semantics
        != EXPECTED_LOCKED_MUTABLE_DWORD_SLOT_UPDATE_SEMANTICS
    ):
        raise ExtractionError(
            "locked mutable dword slot update semantic oracle mismatch"
        )
    target_va = 0x00710FA0
    spec = LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS[target_va]
    body = bytes.fromhex(spec.body_hex)
    expected_span = FunctionSpan(
        target_va,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    decoded = decode_function(image, expected_span)
    invalid = image.imports_by_iat.get(spec.invalid_iat_va)
    direct_calls = {
        ins.va: ins.target
        for ins in decoded.instructions.values()
        if ins.kind == "call"
    }
    indirect_calls = {
        ins.va: (ins.src, ins.raw)
        for ins in decoded.instructions.values()
        if ins.kind == "call_indirect"
    }
    mov_writes = {
        ins.va: (ins.dst, ins.src)
        for ins in decoded.instructions.values()
        if ins.kind == "mov"
        and ins.dst is not None
        and ins.dst.kind == "mem"
        and ins.dst.base != "esp"
    }
    ret_sites = {
        ins.va: ins.imm
        for ins in decoded.instructions.values()
        if ins.kind == "ret"
    }
    decrement = decoded.instructions.get(0x00710FCC)
    increment = decoded.instructions.get(0x00710FFE)
    if (
        len(body) != 111
        or spec.proof_end_va - target_va != len(body)
        or image.va_range_to_off(target_va, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or decoded.errors
        or decoded.span != expected_span
        or len(decoded.instructions) != 42
        or _reachable_nodes(decoded, target_va)
        != frozenset(decoded.instructions)
        or max(ins.next_va for ins in decoded.instructions.values())
        != spec.proof_end_va
        or analyzer._decoded_cleanup(decoded) != 4
        or ret_sites != {0x0071100C: 4}
        or invalid is None
        or (invalid.dll, invalid.name)
        != ("MSVCR90.dll", "_invalid_parameter_noinfo")
        or image.va_to_off(spec.invalid_iat_va) != invalid.iat_off
        or tuple(image.va_to_off(va) for va in spec.nested_target_vas)
        != (0x0048C9B0, 0x00300AA0, 0x0009CE40)
        or direct_calls
        != {
            0x00710FB1: 0x0088D5B0,
            0x00710FC1: 0x007016A0,
            0x00711003: 0x0049DA40,
        }
        or indirect_calls
        != {
            0x00710FD6: (
                Operand("mem", absolute=spec.invalid_iat_va),
                b"\xFF\x15\xC0\xB4\xC3\x00",
            ),
            0x00710FF2: (
                Operand("mem", absolute=spec.invalid_iat_va),
                b"\xFF\x15\xC0\xB4\xC3\x00",
            ),
        }
        or mov_writes
        != {
            0x00710FE2: (
                Operand("mem", base="ebp"),
                Operand("reg", reg="edx"),
            ),
            0x00710FFB: (
                Operand("mem", base="ecx", index="edi", scale=4),
                Operand("reg", reg="ebp"),
            ),
        }
        or decrement is None
        or decrement.raw != b"\xFF\x4E\x20"
        or increment is None
        or increment.raw != b"\xFF\x46\x24"
        or any(
            ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
            for ins in decoded.instructions.values()
        )
    ):
        raise ExtractionError(
            "locked mutable dword slot update helper definition mismatch"
        )


def validate_locked_mutable_dword_slot_update_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    target_va = 0x00710FA0
    spec = LOCKED_MUTABLE_DWORD_SLOT_UPDATE_HELPERS[target_va]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )locked_mutable_dword_slot_update_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x00710FA0(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    messages = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError(
                "locked mutable dword slot update row lacks call proof"
            )
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != target_va
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset != "UNKNOWN(%s)" % spec.reason
            or row.reason != spec.reason
            or locked_mutable_dword_slot_update_helper_fragment(
                image, target_va
            )
            not in row.gate_condition
        ):
            raise ExtractionError(
                "locked mutable dword slot update row mismatch at 0x%08X"
                % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
        messages.add(row.message)
    if (
        len(helper_rows) != 28
        or directions != Counter({"W": 14, "R": 14})
        or len(unique_sites) != 11
        or len(messages) != 6
        or any(
            row.tag == "CALL_UNCLASSIFIED:0x00710FA0" for row in rows
        )
    ):
        raise ExtractionError(
            "locked mutable dword slot update row census mismatch"
        )


def validate_mutable_pointer_slot_traversal_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.invalid_iat_va,
        )
        for target_va, spec in MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS.items()
    }
    if (
        measured_semantics
        != EXPECTED_MUTABLE_POINTER_SLOT_TRAVERSAL_SEMANTICS
    ):
        raise ExtractionError(
            "mutable pointer slot traversal semantic oracle mismatch"
        )
    target_va = 0x0046D2B0
    spec = MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS[target_va]
    body = bytes.fromhex(spec.body_hex)
    expected_span = FunctionSpan(
        target_va,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    span = analyzer.span(target_va)
    decoded = analyzer.decode(target_va)
    invalid = image.imports_by_iat.get(spec.invalid_iat_va)
    iat_load = None if decoded is None else decoded.instructions.get(0x0046D2B7)
    indirect_calls = (
        {}
        if decoded is None
        else {
            ins.va: (ins.src, ins.raw)
            for ins in decoded.instructions.values()
            if ins.kind == "call_indirect"
        }
    )
    direct_calls = (
        set()
        if decoded is None
        else {
            ins.va
            for ins in decoded.instructions.values()
            if ins.kind == "call"
        }
    )
    nonstack_mov_writes = (
        {}
        if decoded is None
        else {
            ins.va: (ins.dst, ins.src)
            for ins in decoded.instructions.values()
            if ins.kind == "mov"
            and ins.dst is not None
            and ins.dst.kind == "mem"
            and ins.dst.base != "esp"
        }
    )
    ret_sites = (
        {}
        if decoded is None
        else {
            ins.va: ins.imm
            for ins in decoded.instructions.values()
            if ins.kind == "ret"
        }
    )
    if (
        len(body) != 108
        or spec.proof_end_va - target_va != len(body)
        or image.va_range_to_off(target_va, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or span != expected_span
        or decoded is None
        or decoded.errors
        or decoded.span != expected_span
        or len(decoded.instructions) != 44
        or _reachable_nodes(decoded, target_va)
        != frozenset(decoded.instructions)
        or max(ins.next_va for ins in decoded.instructions.values())
        != spec.proof_end_va
        or analyzer._decoded_cleanup(decoded) != 0
        or ret_sites
        != {0x0046D2CE: 0, 0x0046D2EF: 0, 0x0046D31B: 0}
        or invalid is None
        or (invalid.dll, invalid.name)
        != ("MSVCR90.dll", "_invalid_parameter_noinfo")
        or image.va_to_off(spec.invalid_iat_va) != invalid.iat_off
        or iat_load is None
        or iat_load.kind != "mov"
        or iat_load.dst != Operand("reg", reg="edi")
        or iat_load.src != Operand("mem", absolute=spec.invalid_iat_va)
        or indirect_calls
        != {
            0x0046D2BF: (Operand("reg", reg="edi"), b"\xFF\xD7"),
            0x0046D2CA: (Operand("reg", reg="edi"), b"\xFF\xD7"),
        }
        or direct_calls
        or nonstack_mov_writes
        != {
            0x0046D2EB: (
                Operand("mem", base="esi", disp=4),
                Operand("reg", reg="ecx"),
            ),
            0x0046D308: (
                Operand("mem", base="esi", disp=4),
                Operand("reg", reg="eax"),
            ),
            0x0046D317: (
                Operand("mem", base="esi", disp=4),
                Operand("reg", reg="eax"),
            ),
        }
        or any(
            ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
            for ins in decoded.instructions.values()
        )
    ):
        raise ExtractionError(
            "mutable pointer slot traversal helper definition mismatch"
        )


def validate_mutable_pointer_slot_traversal_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    target_va = 0x0046D2B0
    spec = MUTABLE_POINTER_SLOT_TRAVERSAL_HELPERS[target_va]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )mutable_pointer_slot_traversal_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x0046D2B0(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    messages = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError(
                "mutable pointer slot traversal row lacks call proof"
            )
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != target_va
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset != "UNKNOWN(%s)" % spec.reason
            or row.reason != spec.reason
            or mutable_pointer_slot_traversal_helper_fragment(
                image, target_va
            )
            not in row.gate_condition
        ):
            raise ExtractionError(
                "mutable pointer slot traversal row mismatch at 0x%08X"
                % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
        messages.add(row.message)
    if (
        len(helper_rows) != 29
        or directions != Counter({"W": 15, "R": 14})
        or len(unique_sites) != 10
        or len(messages) != 11
        or any(
            row.tag == "CALL_UNCLASSIFIED:0x0046D2B0" for row in rows
        )
    ):
        raise ExtractionError(
            "mutable pointer slot traversal row census mismatch"
        )


def validate_mutable_dword_slot_operation_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.invalid_iat_va,
            spec.nested_target_vas,
        )
        for target_va, spec in MUTABLE_DWORD_SLOT_OPERATION_HELPERS.items()
    }
    if (
        measured_semantics
        != EXPECTED_MUTABLE_DWORD_SLOT_OPERATION_SEMANTICS
    ):
        raise ExtractionError(
            "mutable dword slot operation semantic oracle mismatch"
        )
    target_va = 0x00AC6E80
    spec = MUTABLE_DWORD_SLOT_OPERATION_HELPERS[target_va]
    body = bytes.fromhex(spec.body_hex)
    expected_span = FunctionSpan(
        target_va,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    decoded = decode_function(image, expected_span)
    invalid = image.imports_by_iat.get(spec.invalid_iat_va)
    invalid_call = decoded.instructions.get(0x00AC6EDD)
    stack_write = decoded.instructions.get(0x00AC6EAC)
    state_write = decoded.instructions.get(0x00AC6ECE)
    direct_calls = {
        ins.va: ins.target
        for ins in decoded.instructions.values()
        if ins.kind == "call"
    }
    nonstack_mov_writes = {
        ins.va
        for ins in decoded.instructions.values()
        if ins.kind == "mov"
        and ins.dst is not None
        and ins.dst.kind == "mem"
        and ins.dst.base != "esp"
    }
    stack_mov_writes = {
        ins.va
        for ins in decoded.instructions.values()
        if ins.kind == "mov"
        and ins.dst is not None
        and ins.dst.kind == "mem"
        and ins.dst.base == "esp"
    }
    ret_sites = {
        ins.va: ins.imm
        for ins in decoded.instructions.values()
        if ins.kind == "ret"
    }
    if (
        len(body) != 128
        or spec.proof_end_va - target_va != len(body)
        or image.va_range_to_off(target_va, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or decoded.errors
        or decoded.span != expected_span
        or len(decoded.instructions) != 53
        or _reachable_nodes(decoded, target_va)
        != frozenset(decoded.instructions)
        or max(ins.next_va for ins in decoded.instructions.values())
        != spec.proof_end_va
        or analyzer._decoded_cleanup(decoded) != 4
        or ret_sites != {0x00AC6ED6: 4, 0x00AC6EFD: 4}
        or invalid is None
        or (invalid.dll, invalid.name)
        != ("MSVCR90.dll", "_invalid_parameter_noinfo")
        or image.va_to_off(spec.invalid_iat_va) != invalid.iat_off
        or tuple(image.va_to_off(va) for va in spec.nested_target_vas)
        != (0x002B29A0, 0x006C6100)
        or direct_calls
        != {0x00AC6EC3: 0x006B35A0, 0x00AC6EF3: 0x00AC6D00}
        or invalid_call is None
        or invalid_call.kind != "call_indirect"
        or invalid_call.src != Operand("mem", absolute=spec.invalid_iat_va)
        or invalid_call.raw != b"\xFF\x15\xC0\xB4\xC3\x00"
        or nonstack_mov_writes != {0x00AC6ECE}
        or stack_mov_writes != {0x00AC6EAC}
        or stack_write is None
        or stack_write.dst != Operand("mem", base="esp", disp=8)
        or stack_write.src != Operand("imm", imm=0)
        or state_write is None
        or state_write.dst != Operand("mem", base="esi", disp=0x10)
        or state_write.src != Operand("reg", reg="edi")
        or any(
            ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
            for ins in decoded.instructions.values()
        )
    ):
        raise ExtractionError(
            "mutable dword slot operation helper definition mismatch"
        )


def validate_mutable_dword_slot_operation_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    target_va = 0x00AC6E80
    spec = MUTABLE_DWORD_SLOT_OPERATION_HELPERS[target_va]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )mutable_dword_slot_operation_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x00AC6E80(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    messages = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError(
                "mutable dword slot operation row lacks call proof"
            )
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != target_va
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset != "UNKNOWN(%s)" % spec.reason
            or row.reason != spec.reason
            or mutable_dword_slot_operation_helper_fragment(
                image, target_va
            )
            not in row.gate_condition
        ):
            raise ExtractionError(
                "mutable dword slot operation row mismatch at 0x%08X"
                % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
        messages.add(row.message)
    if (
        len(helper_rows) != 46
        or directions != Counter({"W": 23, "R": 23})
        or len(unique_sites) != 22
        or len(messages) != 21
        or any(
            row.tag == "CALL_UNCLASSIFIED:0x00AC6E80" for row in rows
        )
    ):
        raise ExtractionError(
            "mutable dword slot operation row census mismatch"
        )


def validate_mutable_dword_range_growth_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.invalid_iat_va,
            spec.nested_target_va,
        )
        for target_va, spec in MUTABLE_DWORD_RANGE_GROWTH_HELPERS.items()
    }
    if measured_semantics != EXPECTED_MUTABLE_DWORD_RANGE_GROWTH_SEMANTICS:
        raise ExtractionError(
            "mutable dword range growth semantic oracle mismatch"
        )
    spec = MUTABLE_DWORD_RANGE_GROWTH_HELPERS[0x007016A0]
    body = bytes.fromhex(spec.body_hex)
    expected_span = FunctionSpan(
        0x007016A0,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    span = analyzer.span(0x007016A0)
    decoded = analyzer.decode(0x007016A0)
    invalid = image.imports_by_iat.get(spec.invalid_iat_va)
    iat_load = (
        None if decoded is None else decoded.instructions.get(0x007016B7)
    )
    invalid_call = (
        None if decoded is None else decoded.instructions.get(0x007016F9)
    )
    nested_call = (
        None if decoded is None else decoded.instructions.get(0x0070170B)
    )
    zero_write = (
        None if decoded is None else decoded.instructions.get(0x007016E7)
    )
    end_write = (
        None if decoded is None else decoded.instructions.get(0x007016F0)
    )
    nonstack_mov_writes = (
        set()
        if decoded is None
        else {
            ins.va
            for ins in decoded.instructions.values()
            if ins.kind == "mov"
            and ins.dst is not None
            and ins.dst.kind == "mem"
            and ins.dst.base != "esp"
        }
    )
    if (
        len(body) != 133
        or spec.proof_end_va - 0x007016A0 != len(body)
        or image.va_range_to_off(0x007016A0, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or span != expected_span
        or decoded is None
        or decoded.errors
        or decoded.span != expected_span
        or analyzer._decoded_cleanup(decoded) != 0
        or invalid is None
        or (invalid.dll, invalid.name)
        != ("MSVCR90.dll", "_invalid_parameter_noinfo")
        or image.va_to_off(spec.invalid_iat_va) != invalid.iat_off
        or image.va_to_off(spec.nested_target_va) != 0x001F5CD0
        or iat_load is None
        or iat_load.kind != "mov"
        or iat_load.dst != Operand("reg", reg="ebp")
        or iat_load.src != Operand("mem", absolute=spec.invalid_iat_va)
        or invalid_call is None
        or invalid_call.kind != "call_indirect"
        or invalid_call.src != Operand("reg", reg="ebp")
        or nested_call is None
        or nested_call.kind != "call"
        or nested_call.target != spec.nested_target_va
        or {
            ins.va: ins.target
            for ins in decoded.instructions.values()
            if ins.kind == "call"
        }
        != {0x0070170B: spec.nested_target_va}
        or nonstack_mov_writes != {0x007016E7, 0x007016F0}
        or zero_write is None
        or zero_write.dst != Operand("mem", base="edi")
        or zero_write.src != Operand("imm", imm=0)
        or end_write is None
        or end_write.dst != Operand("mem", base="esi", disp=0x10)
        or end_write.src != Operand("reg", reg="edi")
        or any(
            ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
            for ins in decoded.instructions.values()
        )
    ):
        raise ExtractionError(
            "mutable dword range growth helper definition mismatch"
        )


def validate_mutable_dword_range_growth_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    spec = MUTABLE_DWORD_RANGE_GROWTH_HELPERS[0x007016A0]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )mutable_dword_range_growth_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x007016A0(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError(
                "mutable dword range growth row lacks call proof"
            )
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != 0x007016A0
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset
            != "UNKNOWN(mutable_dword_range_nested_target_and_alias_unproved)"
            or row.reason != spec.reason
            or mutable_dword_range_growth_helper_fragment(
                image, 0x007016A0
            )
            not in row.gate_condition
        ):
            raise ExtractionError(
                "mutable dword range growth row mismatch at 0x%08X" % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
    if (
        len(helper_rows) != 32
        or directions != Counter({"W": 16, "R": 16})
        or len(unique_sites) != 6
        or any(
            row.tag == "CALL_UNCLASSIFIED:0x007016A0" for row in rows
        )
    ):
        raise ExtractionError("mutable dword range growth row census mismatch")


def validate_critical_section_pointer_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.iat_va,
        )
        for target_va, spec in CRITICAL_SECTION_POINTER_HELPERS.items()
    }
    if measured_semantics != EXPECTED_CRITICAL_SECTION_POINTER_SEMANTICS:
        raise ExtractionError(
            "critical section pointer helper semantic oracle mismatch"
        )
    measured_imports = {
        iat_va: (
            image.imports_by_iat[iat_va].dll,
            image.imports_by_iat[iat_va].name,
        )
        for iat_va in CRITICAL_SECTION_POINTER_IMPORTS
        if iat_va in image.imports_by_iat
    }
    if measured_imports != CRITICAL_SECTION_POINTER_IMPORTS:
        raise ExtractionError("critical section pointer import mismatch")
    for target_va, spec in sorted(CRITICAL_SECTION_POINTER_HELPERS.items()):
        body = bytes.fromhex(spec.body_hex)
        expected_span = FunctionSpan(
            target_va,
            spec.proof_end_va,
            spec.start_off,
            spec.start_off + len(body),
            spec.proof_sha256,
        )
        span = analyzer.span(target_va)
        decoded = analyzer.decode(target_va)
        symbol = image.imports_by_iat.get(spec.iat_va)
        load = (
            None if decoded is None else decoded.instructions.get(target_va)
        )
        push = (
            None if decoded is None else decoded.instructions.get(target_va + 2)
        )
        import_call = (
            None if decoded is None else decoded.instructions.get(target_va + 3)
        )
        ret = (
            None if decoded is None else decoded.instructions.get(target_va + 9)
        )
        if (
            len(body) != 10
            or spec.proof_end_va - target_va != len(body)
            or image.va_range_to_off(target_va, len(body)) != spec.start_off
            or image.data[spec.start_off : spec.start_off + len(body)] != body
            or hashlib.sha256(body).hexdigest() != spec.proof_sha256
            or span != expected_span
            or decoded is None
            or decoded.errors
            or decoded.span != expected_span
            or len(decoded.instructions) != 4
            or analyzer._decoded_cleanup(decoded) != 0
            or symbol is None
            or (symbol.dll, symbol.name)
            != CRITICAL_SECTION_POINTER_IMPORTS[spec.iat_va]
            or image.va_to_off(spec.iat_va) != symbol.iat_off
            or load is None
            or load.kind != "mov"
            or load.dst != Operand("reg", reg="eax")
            or load.src != Operand("mem", base="ecx")
            or push is None
            or push.kind != "push"
            or push.src != Operand("reg", reg="eax")
            or import_call is None
            or import_call.kind != "call_indirect"
            or import_call.src != Operand("mem", absolute=spec.iat_va)
            or ret is None
            or ret.kind != "ret"
            or ret.imm != 0
            or any(
                ins.kind == "mov"
                and ins.dst is not None
                and ins.dst.kind == "mem"
                for ins in decoded.instructions.values()
            )
            or any(
                ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
                for ins in decoded.instructions.values()
            )
        ):
            raise ExtractionError(
                "critical section pointer helper definition mismatch at "
                "0x%08X" % target_va
            )


def validate_critical_section_pointer_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    pattern = re.compile(
        r"(?:^| AND )critical_section_pointer_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x([0-9A-F]{8})(?: AND |$)"
    )
    for target_va, spec in sorted(CRITICAL_SECTION_POINTER_HELPERS.items()):
        helper_rows = [row for row in rows if row.tag == spec.tag]
        directions = Counter()
        unique_sites = set()
        for row in helper_rows:
            match = pattern.search(row.gate_condition)
            if match is None:
                raise ExtractionError(
                    "critical section pointer row lacks call proof"
                )
            call_va, call_off, function_va, measured_target = (
                int(text, 16) for text in match.groups()
            )
            decoded = analyzer.decode(function_va)
            ins = None if decoded is None else decoded.instructions.get(call_va)
            if (
                measured_target != target_va
                or decoded is None
                or ins is None
                or ins.kind != "call"
                or ins.target != target_va
                or ins.off != call_off
                or row.file_off_claim != call_off
                or row.span_start != function_va
                or row.direction not in ("W", "R")
                or row.length != "N/A"
                or row.field_offset
                != "UNKNOWN(critical_section_pointer_alias_unproved)"
                or row.reason != spec.reason
                or critical_section_pointer_helper_fragment(image, target_va)
                not in row.gate_condition
            ):
                raise ExtractionError(
                    "critical section pointer row mismatch at 0x%08X"
                    % call_va
                )
            directions[row.direction] += 1
            unique_sites.add((function_va, call_va))
        if (
            len(helper_rows) != 32
            or directions != Counter({"W": 16, "R": 16})
            or len(unique_sites) != 6
            or any(
                row.tag == "CALL_UNCLASSIFIED:0x%08X" % target_va
                for row in rows
            )
        ):
            raise ExtractionError(
                "critical section pointer row census mismatch at 0x%08X"
                % target_va
            )


def validate_locked_mutable_pointer_slot_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.iat_vas,
        )
        for target_va, spec in LOCKED_MUTABLE_POINTER_SLOT_HELPERS.items()
    }
    if measured_semantics != EXPECTED_LOCKED_MUTABLE_POINTER_SLOT_SEMANTICS:
        raise ExtractionError(
            "locked mutable pointer slot helper semantic oracle mismatch"
        )
    spec = LOCKED_MUTABLE_POINTER_SLOT_HELPERS[0x0066AB90]
    body = bytes.fromhex(spec.body_hex)
    expected_span = FunctionSpan(
        0x0066AB90,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    span = analyzer.span(0x0066AB90)
    decoded = analyzer.decode(0x0066AB90)
    measured_imports = {
        iat_va: (
            image.imports_by_iat[iat_va].dll,
            image.imports_by_iat[iat_va].name,
        )
        for iat_va in LOCKED_MUTABLE_POINTER_SLOT_IMPORTS
        if iat_va in image.imports_by_iat
    }
    if (
        len(body) != 157
        or spec.proof_end_va - 0x0066AB90 != len(body)
        or image.va_range_to_off(0x0066AB90, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or span != expected_span
        or decoded is None
        or decoded.errors
        or decoded.span != expected_span
        or analyzer._decoded_cleanup(decoded) != 0
        or measured_imports != LOCKED_MUTABLE_POINTER_SLOT_IMPORTS
        or any(
            image.va_to_off(iat_va) != image.imports_by_iat[iat_va].iat_off
            for iat_va in LOCKED_MUTABLE_POINTER_SLOT_IMPORTS
        )
    ):
        raise ExtractionError(
            "locked mutable pointer slot helper definition mismatch"
        )
    assert decoded is not None
    expected_direct_calls = {
        0x0066ABA0: 0x0088D5B0,
        0x0066ABAE: 0x007016A0,
        0x0066ABD1: 0x004A0680,
        0x0066ABE9: 0x0049DA40,
        0x0066AC20: 0x0049DA40,
    }
    measured_direct_calls = {
        ins.va: ins.target
        for ins in decoded.instructions.values()
        if ins.kind == "call"
    }
    expected_indirect_calls = {
        0x0066ABC0: 0x00C3B4C0,
        0x0066ABD7: 0x00C3B87C,
        0x0066AC05: 0x00C3B4C0,
    }
    measured_indirect_calls = {
        ins.va: ins.src.absolute
        for ins in decoded.instructions.values()
        if ins.kind == "call_indirect"
        and ins.src is not None
        and ins.src.kind == "mem"
        and ins.src.absolute is not None
    }
    nonstack_mov_writes = {
        ins.va
        for ins in decoded.instructions.values()
        if ins.kind == "mov"
        and ins.dst is not None
        and ins.dst.kind == "mem"
        and ins.dst.base != "esp"
    }
    indexed_write = decoded.instructions.get(0x0066AC14)
    zero_source = decoded.instructions.get(0x0066AC17)
    if (
        measured_direct_calls != expected_direct_calls
        or measured_indirect_calls != expected_indirect_calls
        or nonstack_mov_writes != {0x0066AC14, 0x0066AC17}
        or indexed_write is None
        or indexed_write.dst
        != Operand("mem", base="edx", index="edi", scale=4)
        or indexed_write.src != Operand("reg", reg="eax")
        or zero_source is None
        or zero_source.dst != Operand("mem", base="ebx")
        or zero_source.src != Operand("imm", imm=0)
        or image.data[image.va_to_off(0x0066ABE1) : image.va_to_off(0x0066ABE1) + 3]
        != bytes.fromhex("FF4620")
        or image.data[image.va_to_off(0x0066ABF9) : image.va_to_off(0x0066ABF9) + 3]
        != bytes.fromhex("FF4E24")
        or image.data[image.va_to_off(0x0066AC1D) : image.va_to_off(0x0066AC1D) + 3]
        != bytes.fromhex("FF4620")
        or any(
            ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
            for ins in decoded.instructions.values()
        )
    ):
        raise ExtractionError(
            "locked mutable pointer slot helper operation shape mismatch"
        )
    support_iat_calls = {
        0x0049DA40: (0x0049DA43, 0x00C3B168),
        0x004A0680: (0x004A068A, 0x00C3B19C),
        0x0088D5B0: (0x0088D5B3, 0x00C3B16C),
    }
    for target_va, (start_off, end_va, span_hash, body_hex) in (
        LOCKED_MUTABLE_POINTER_SLOT_SUPPORT.items()
    ):
        support_body = bytes.fromhex(body_hex)
        support_span = FunctionSpan(
            target_va,
            end_va,
            start_off,
            start_off + len(support_body),
            span_hash,
        )
        got_span = analyzer.span(target_va)
        got_decode = analyzer.decode(target_va)
        call_va, iat_va = support_iat_calls[target_va]
        import_call = (
            None if got_decode is None else got_decode.instructions.get(call_va)
        )
        if (
            end_va - target_va != len(support_body)
            or image.va_range_to_off(target_va, len(support_body)) != start_off
            or image.data[start_off : start_off + len(support_body)]
            != support_body
            or hashlib.sha256(support_body).hexdigest() != span_hash
            or got_span != support_span
            or got_decode is None
            or got_decode.errors
            or analyzer._decoded_cleanup(got_decode) != 0
            or import_call is None
            or import_call.kind != "call_indirect"
            or import_call.src != Operand("mem", absolute=iat_va)
            or any(
                ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
                for ins in got_decode.instructions.values()
            )
        ):
            raise ExtractionError(
                "locked mutable pointer slot support wrapper mismatch at "
                "0x%08X" % target_va
            )


def validate_locked_mutable_pointer_slot_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    spec = LOCKED_MUTABLE_POINTER_SLOT_HELPERS[0x0066AB90]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )locked_mutable_pointer_slot_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x0066AB90(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError(
                "locked mutable pointer slot row lacks call proof"
            )
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != 0x0066AB90
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset
            != "UNKNOWN(locked_mutable_pointer_slot_nested_target_and_alias_unproved)"
            or row.reason != spec.reason
            or locked_mutable_pointer_slot_helper_fragment(
                image, 0x0066AB90
            )
            not in row.gate_condition
        ):
            raise ExtractionError(
                "locked mutable pointer slot emitted row mismatch at 0x%08X"
                % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
    if (
        len(helper_rows) != 58
        or directions != Counter({"W": 29, "R": 29})
        or len(unique_sites) != 18
        or any(
            row.tag == "CALL_UNCLASSIFIED:0x0066AB90" for row in rows
        )
    ):
        raise ExtractionError(
            "locked mutable pointer slot helper row census mismatch"
        )


def validate_mutable_chain_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.reason,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
            spec.iat_va,
        )
        for target_va, spec in MUTABLE_CHAIN_HELPERS.items()
    }
    if measured_semantics != EXPECTED_MUTABLE_CHAIN_SEMANTICS:
        raise ExtractionError("mutable chain helper semantic oracle mismatch")
    spec = MUTABLE_CHAIN_HELPERS[0x00B0BF70]
    body = bytes.fromhex(spec.body_hex)
    expected_span = FunctionSpan(
        0x00B0BF70,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    span = analyzer.span(0x00B0BF70)
    decoded = analyzer.decode(0x00B0BF70)
    symbol = image.imports_by_iat.get(spec.iat_va)
    if (
        len(body) != 108
        or spec.proof_end_va - 0x00B0BF70 != len(body)
        or image.va_range_to_off(0x00B0BF70, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or span != expected_span
        or decoded is None
        or decoded.errors
        or decoded.span != expected_span
        or analyzer._decoded_cleanup(decoded) != 0
        or symbol is None
        or (symbol.dll, symbol.name)
        != ("MSVCR90.dll", "_invalid_parameter_noinfo")
        or image.va_to_off(spec.iat_va) != symbol.iat_off
    ):
        raise ExtractionError("mutable chain helper definition mismatch")
    assert decoded is not None
    writes = {
        ins.va
        for ins in decoded.instructions.values()
        if ins.kind == "mov"
        and ins.dst is not None
        and ins.dst.kind == "mem"
    }
    iat_load = decoded.instructions.get(0x00B0BF77)
    iat_calls = {
        ins.va
        for ins in decoded.instructions.values()
        if ins.kind == "call_indirect"
        and ins.src == Operand("reg", reg="edi")
    }
    if (
        writes != {0x00B0BFAB, 0x00B0BFC8, 0x00B0BFD7}
        or any(
            decoded.instructions[site].dst
            != Operand("mem", base="esi", disp=4)
            for site in writes
        )
        or iat_load is None
        or iat_load.kind != "mov"
        or iat_load.dst != Operand("reg", reg="edi")
        or iat_load.src != Operand("mem", absolute=0x00C3B4C0)
        or iat_calls != {0x00B0BF7F, 0x00B0BF8A}
        or any(
            ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
            for ins in decoded.instructions.values()
        )
    ):
        raise ExtractionError("mutable chain helper operation shape mismatch")


def validate_mutable_chain_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    spec = MUTABLE_CHAIN_HELPERS[0x00B0BF70]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )mutable_chain_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x00B0BF70(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError("mutable chain helper row lacks call proof")
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != 0x00B0BF70
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "N/A"
            or row.field_offset
            != "UNKNOWN(mutable_chain_target_object_alias_unproved)"
            or row.reason != spec.reason
            or mutable_chain_helper_fragment(image, 0x00B0BF70)
            not in row.gate_condition
        ):
            raise ExtractionError(
                "mutable chain helper emitted row mismatch at 0x%08X"
                % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
    if (
        len(helper_rows) != 70
        or directions != Counter({"W": 35, "R": 35})
        or len(unique_sites) != 22
        or any(
            row.tag == "CALL_UNCLASSIFIED:0x00B0BF70" for row in rows
        )
    ):
        raise ExtractionError("mutable chain helper row census mismatch")


def validate_pure_chain_helper_definitions(
    image: Image, analyzer: SerializerAnalyzer
) -> None:
    measured_semantics = {
        target_va: (
            spec.tag,
            spec.start_off,
            spec.proof_end_va,
            spec.proof_sha256,
        )
        for target_va, spec in PURE_CHAIN_HELPERS.items()
    }
    if measured_semantics != EXPECTED_PURE_CHAIN_SEMANTICS:
        raise ExtractionError("pure chain helper semantic oracle mismatch")
    spec = PURE_CHAIN_HELPERS[0x0088F2B0]
    body = bytes.fromhex(spec.body_hex)
    expected_span = FunctionSpan(
        0x0088F2B0,
        spec.proof_end_va,
        spec.start_off,
        spec.start_off + len(body),
        spec.proof_sha256,
    )
    span = analyzer.span(0x0088F2B0)
    decoded = analyzer.decode(0x0088F2B0)
    if (
        len(body) != 0x21
        or spec.proof_end_va - 0x0088F2B0 != len(body)
        or image.va_range_to_off(0x0088F2B0, len(body)) != spec.start_off
        or image.data[spec.start_off : spec.start_off + len(body)] != body
        or hashlib.sha256(body).hexdigest() != spec.proof_sha256
        or span != expected_span
        or decoded is None
        or decoded.errors
        or decoded.span != expected_span
        or analyzer._decoded_cleanup(decoded) != 0
        or any(
            ins.kind in ("call", "call_indirect")
            or (ins.dst is not None and ins.dst.kind == "mem")
            for ins in (() if decoded is None else decoded.instructions.values())
        )
    ):
        raise ExtractionError("pure chain helper definition mismatch")
    assert decoded is not None
    head = decoded.instructions.get(0x0088F2B0)
    needle = decoded.instructions.get(0x0088F2B8)
    identity = decoded.instructions.get(0x0088F2BC)
    compare = decoded.instructions.get(0x0088F2C0)
    step = decoded.instructions.get(0x0088F2C4)
    false_value = decoded.instructions.get(0x0088F2CB)
    true_value = decoded.instructions.get(0x0088F2CE)
    if (
        head is None
        or head.kind != "mov"
        or head.dst != Operand("reg", reg="eax")
        or head.src != Operand("mem", base="esp", disp=8)
        or needle is None
        or needle.kind != "mov"
        or needle.dst != Operand("reg", reg="ecx")
        or needle.src != Operand("mem", base="esp", disp=4)
        or identity is None
        or identity.raw != bytes.fromhex("8D642400")
        or compare is None
        or compare.raw != bytes.fromhex("3BC1")
        or step is None
        or step.kind != "mov"
        or step.dst != Operand("reg", reg="eax")
        or step.src != Operand("mem", base="eax", disp=4)
        or false_value is None
        or false_value.raw != bytes.fromhex("32C0")
        or true_value is None
        or true_value.raw != bytes.fromhex("B001")
    ):
        raise ExtractionError("pure chain helper operation shape mismatch")


def validate_pure_chain_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    spec = PURE_CHAIN_HELPERS[0x0088F2B0]
    helper_rows = [row for row in rows if row.tag == spec.tag]
    pattern = re.compile(
        r"(?:^| AND )pure_chain_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x0088F2B0 "
        r"caller_suffix=movzx_eax_al,add_esp_8(?: AND |$)"
    )
    directions = Counter()
    unique_sites = set()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError("pure chain helper row lacks call proof")
        call_va, call_off, function_va = (
            int(text, 16) for text in match.groups()
        )
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != 0x0088F2B0
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.length != "0"
            or row.field_offset != "N/A"
            or row.reason
            or image.data[call_off + 5 : call_off + 11]
            != bytes.fromhex("0FB6C083C408")
            or pure_chain_helper_fragment(0x0088F2B0)
            not in row.gate_condition
        ):
            raise ExtractionError(
                "pure chain helper emitted row mismatch at 0x%08X" % call_va
            )
        directions[row.direction] += 1
        unique_sites.add((function_va, call_va))
    if (
        len(helper_rows) != 76
        or directions != Counter({"W": 38, "R": 38})
        or len(unique_sites) != 34
        or any(
            row.tag == "CALL_UNCLASSIFIED:0x0088F2B0" for row in rows
        )
    ):
        raise ExtractionError("pure chain helper row census mismatch")


def validate_atomic_object_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    helper_tags = {spec.tag for spec in ATOMIC_OBJECT_HELPERS.values()}
    helper_rows = [row for row in rows if row.tag in helper_tags]
    pattern = re.compile(
        r"(?:^| AND )atomic_object_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x([0-9A-F]{8})(?: AND |$)"
    )
    measured = Counter()
    directions = Counter()
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError("atomic object helper row lacks call proof")
        call_va, call_off, function_va, target_va = (
            int(text, 16) for text in match.groups()
        )
        spec = ATOMIC_OBJECT_HELPERS.get(target_va)
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        expected_field = (
            "N/A" if not spec or not spec.reason
            else "UNKNOWN(%s)" % spec.reason
        )
        if (
            spec is None
            or decoded is None
            or ins is None
            or ins.kind != "call"
            or ins.target != target_va
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction not in ("W", "R")
            or row.tag != spec.tag
            or row.length != spec.length
            or row.reason != spec.reason
            or row.field_offset != expected_field
            or atomic_object_helper_fragment(image, target_va)
            not in row.gate_condition
        ):
            raise ExtractionError(
                "atomic object helper emitted row mismatch at 0x%08X"
                % call_va
            )
        measured[target_va] += 1
        directions[(target_va, row.direction)] += 1
    if measured != Counter(
        {
            0x004A06A0: 52,
            0x004A06B0: 68,
            0x0088D050: 271,
            0x0088D060: 279,
        }
    ):
        raise ExtractionError(
            "atomic object helper row census mismatch: %r" % measured
        )
    if directions != Counter(
        {
            (0x004A06A0, "W"): 26,
            (0x004A06A0, "R"): 26,
            (0x004A06B0, "W"): 34,
            (0x004A06B0, "R"): 34,
            (0x0088D050, "W"): 132,
            (0x0088D050, "R"): 139,
            (0x0088D060, "W"): 136,
            (0x0088D060, "R"): 143,
        }
    ):
        raise ExtractionError("atomic object helper direction census mismatch")
    generic_tags = {
        "CALL_UNCLASSIFIED:0x%08X" % target
        for target in ATOMIC_OBJECT_HELPERS
    }
    if any(row.tag in generic_tags for row in rows):
        raise ExtractionError("atomic object helper remains unclassified")


def validate_string_wire_helper_rows(
    image: Image,
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    helper_tags = {spec.tag for spec in STRING_WIRE_HELPERS.values()}
    helper_rows = [row for row in rows if row.tag in helper_tags]
    if not helper_rows:
        raise ExtractionError("string wire helper row census is empty")
    measured = Counter()
    pattern = re.compile(
        r"(?:^| AND )string_wire_call@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x([0-9A-F]{8}) stream_formal=entry\+0x([0-9A-F]+)"
        r"(?: AND |$)"
    )
    for row in helper_rows:
        match = pattern.search(row.gate_condition)
        if match is None:
            raise ExtractionError("string wire helper row lacks call proof")
        call_va, call_off, function_va, target_va, formal_offset = (
            int(text, 16) for text in match.groups()
        )
        spec = STRING_WIRE_HELPERS.get(target_va)
        decoded = analyzer.decode(function_va)
        ins = None if decoded is None else decoded.instructions.get(call_va)
        if (
            spec is None
            or decoded is None
            or decoded.errors
            or ins is None
            or ins.kind != "call"
            or ins.target != target_va
            or ins.off != call_off
            or row.file_off_claim != call_off
            or row.span_start != function_va
            or row.direction != spec.direction
            or row.tag != spec.tag
            or row.length != "4+N_bytes"
            or row.reason
            or "UNKNOWN" in row.field_offset
            or string_wire_helper_fragment(image, target_va)
            not in row.gate_condition
        ):
            raise ExtractionError(
                "string wire helper emitted row mismatch at 0x%08X" % call_va
            )
        origins = analyzer._formal_offsets(
            function_va, call_va, Operand("reg", reg="ecx")
        )
        sequences = recover_call_pushes(decoded, call_va, 1)
        if (
            origins != frozenset((formal_offset,))
            or len(sequences) != 1
        ):
            raise ExtractionError(
                "string wire helper row provenance mismatch at 0x%08X"
                % call_va
            )
        measured[target_va] += 1
    expected_measured = Counter(
        {
            0x0089A6D0: 30,
            0x0089A740: 30,
            0x0089A810: 174,
            0x0089A880: 174,
        }
    )
    if measured != expected_measured:
        raise ExtractionError(
            "string wire helper target census mismatch: %r" % measured
        )
    unclassified = {
        row.tag
        for row in rows
        if row.tag in {
            "CALL_UNCLASSIFIED:0x%08X" % target
            for target in STRING_WIRE_HELPERS
        }
    }
    if unclassified:
        raise ExtractionError(
            "string wire helpers remain unclassified: %r"
            % sorted(unclassified)
        )


def validate_field_acceptance(rows: list[FieldRow]) -> None:
    pickup = [row for row in rows if row.message == "PickupTerrainThing"]
    measured = {
        (row.direction, row.order, row.tag, row.field_offset, row.length)
        for row in pickup
    }
    expected = {
        ("W", 1, "0x14", "+0x14", "4"),
        ("W", 2, "0x08", "+0x18", "1"),
        ("R", 1, "0x14", "+0x14", "4"),
        ("R", 2, "0x08", "+0x18", "1"),
    }
    if measured != expected:
        raise ExtractionError(
            "PickupTerrainThing field acceptance mismatch: %r" % sorted(measured)
        )
    for row in pickup:
        if row.gate_condition != "ALWAYS":
            raise ExtractionError("PickupTerrainThing unexpected gate")

    hit_subcalls = {
        (row.direction, row.tag, row.field_offset, row.file_off_claim)
        for row in rows
        if row.message == "CHitResult"
        and row.tag in ("SUBCALL:0x0074F5A0", "SUBCALL:0x0074FF60")
    }
    expected_hit_subcalls = {
        ("W", "SUBCALL:0x0074F5A0", "+0x2C", 0x0034F49F),
        ("R", "SUBCALL:0x0074FF60", "+0x2C", 0x0034F4F8),
    }
    if hit_subcalls != expected_hit_subcalls:
        raise ExtractionError(
            "CHitResult cdecl ABI acceptance mismatch: %r"
            % sorted(hit_subcalls)
        )
    hit_rows = [
        row
        for row in rows
        if row.message == "CHitResult"
        and row.tag in ("SUBCALL:0x0074F5A0", "SUBCALL:0x0074FF60")
    ]
    if any(
        "stream_call@" not in row.gate_condition
        or "stream_arg@" not in row.gate_condition
        or "target_stream_anchor_%s@" % row.direction not in row.gate_condition
        for row in hit_rows
    ):
        raise ExtractionError("CHitResult stream provenance acceptance mismatch")

    direction_proven_sites = {
        ("TeleportVital", 0x001EA8CB): (
            "W", "SUBCALL:0x005DF250", "target_test@0x005DF250",
            "caller_test@0x005EB481",
        ),
        ("TeleportVital", 0x001EA987): (
            "R", "SUBCALL:0x005DF250", "target_test@0x005DF250",
            "value=zero",
        ),
        ("GSSS_GuildDataVitalRes", 0x00267A56): (
            "W", "SUBCALL:0x0066D460", "target_test@0x0066D489",
            "caller_test@0x0066863F",
        ),
        ("GSSS_GuildDataVitalRes", 0x00267A78): (
            "R", "SUBCALL:0x0066D460", "target_test@0x0066D489",
            "value=zero",
        ),
        ("GSSS_GSInitialGuildDataVital", 0x00267AB6): (
            "W", "SUBCALL:0x0066D460", "target_test@0x0066D489",
            "caller_test@0x0066869F",
        ),
        ("GSSS_GSInitialGuildDataVital", 0x00267AD8): (
            "R", "SUBCALL:0x0066D460", "target_test@0x0066D489",
            "value=zero",
        ),
        ("Community_ReceiveNewMailVital", 0x00243DD7): (
            "W", "SUBCALL:0x00637E10", "target_test@0x00637E27",
            "caller_test@0x006449A1",
        ),
        ("Community_ReceiveNewMailVital", 0x00243E44): (
            "R", "SUBCALL:0x00637E10", "target_test@0x00637E27",
            "value=zero",
        ),
        ("Express_ClientReceiveNewExpressVital", 0x002E74D7): (
            "W", "SUBCALL:0x006E3640", "target_test@0x006E3658",
            "caller_test@0x006E80A1",
        ),
        ("Express_ClientReceiveNewExpressVital", 0x002E7544): (
            "R", "SUBCALL:0x006E3640", "target_test@0x006E3658",
            "value=zero",
        ),
    }
    for (message, claim_off), expected in direction_proven_sites.items():
        hits = [
            row
            for row in rows
            if row.message == message and row.file_off_claim == claim_off
        ]
        direction, tag, target_fragment, value_fragment = expected
        if (
            len(hits) != 1
            or hits[0].direction != direction
            or hits[0].tag != tag
            or hits[0].reason
            or not has_local_direction_proof(hits[0])
            or target_fragment not in hits[0].gate_condition
            or value_fragment not in hits[0].gate_condition
            or "stream_call@" not in hits[0].gate_condition
            or "stream_arg@" not in hits[0].gate_condition
            or "target_stream_anchor_%s@" % direction
            not in hits[0].gate_condition
            or "file_off=" not in hits[0].gate_condition
        ):
            raise ExtractionError(
                "subcall direction proof acceptance mismatch for %s at 0x%08X"
                % (message, claim_off)
            )
    teleport_child_directions = {
        row.direction
        for row in rows
        if row.message == "TeleportVital" and row.span_start == 0x005DF250
    }
    if teleport_child_directions != {"W", "R"}:
        raise ExtractionError("TeleportVital direction-proven recursion mismatch")
    for message in ("GSSS_GuildDataVitalRes", "GSSS_GSInitialGuildDataVital"):
        child_directions = {
            row.direction
            for row in rows
            if row.message == message and row.span_start == 0x0066D460
        }
        if child_directions != {"W", "R"}:
            raise ExtractionError(
                "%s direction-proven cdecl recursion mismatch" % message
            )

    formal_forward_hits = [
        row
        for row in rows
        if row.message == "KnowledgeGuru_NewQuizVital"
        and row.file_off_claim == 0x002A1FFF
    ]
    if (
        {row.direction for row in formal_forward_hits} != {"W", "R"}
        or {row.tag for row in formal_forward_hits}
        != {"SUBCALL:0x0069F980"}
        or any(row.reason for row in formal_forward_hits)
        or any(not has_local_direction_proof(row) for row in formal_forward_hits)
        or any(
            fragment not in row.gate_condition
            for row in formal_forward_hits
            for fragment in (
                "target_test@0x0069F980",
                "caller_test@0x006A2C1B",
                "value=formal_forward",
                "caller_formal=entry+0x8",
                "target_formal=entry+0x8",
                "width=1 mapping=preserved",
            )
        )
    ):
        raise ExtractionError("formal-to-formal mode forwarding acceptance mismatch")

    imported_stack_stream_example = [
        row for row in rows if row.file_off_claim == 0x001DFB6E
    ]
    if (
        not imported_stack_stream_example
        or any(
            row.tag != "SUBCALL:0x005DF420"
            or row.direction != "W"
            or row.reason
            or not has_local_stream_proof(row)
            or "stack_neutral_import@0x005E073E" not in row.gate_condition
            or "iat=0x00C3B4C0" not in row.gate_condition
            or "symbol=_invalid_parameter_noinfo cleanup=0"
            not in row.gate_condition
            for row in imported_stack_stream_example
        )
        or not any(
            "subcall_path@0x005E076E" in row.gate_condition for row in rows
        )
        or any(
            row.direction == "R" and row.file_off_claim == 0x001DFB6E
            for row in rows
        )
        or any(
            row.direction == "R"
            and "subcall_path@0x005E076E" in row.gate_condition
            for row in rows
        )
    ):
        raise ExtractionError("import-neutral stream acceptance mismatch")

    discovery_pattern = (
        r"stream_formal_discovery@0x([0-9A-F]{8}) "
        r"file_off=0x[0-9A-F]{8} caller=0x([0-9A-F]{8}) "
        r"target=0x([0-9A-F]{8}) caller_formal=entry\+0x([0-9A-F]+) "
        r"target_formal=entry\+0x([0-9A-F]+) directions=([WR](?:,[WR])*) "
        r"basis=directional_target_primitive"
    )
    discovered = {
        (
            int(site, 16),
            int(caller, 16),
            int(target, 16),
            int(caller_formal, 16),
            int(target_formal, 16),
            directions,
        )
        for row in rows
        for site, caller, target, caller_formal, target_formal, directions
        in re.findall(discovery_pattern, row.gate_condition)
    }
    expected_discovered = {
        (0x005E36D0, 0x005E36D0, 0x005F4070, 4, 4, "R,W"),
        (0x005E4260, 0x005E4250, 0x005F3490, 4, 8, "W"),
        (0x005E4271, 0x005E4250, 0x005F34D0, 4, 8, "R"),
        (0x005E42D2, 0x005E42C0, 0x00463DE0, 4, 4, "W"),
        (0x005E42DF, 0x005E42C0, 0x00463DE0, 4, 4, "R"),
        (0x005E6B9F, 0x005E6B80, 0x005F3490, 4, 8, "W"),
        (0x005E6BB6, 0x005E6B80, 0x005F34D0, 4, 8, "R"),
        (0x00668523, 0x00668520, 0x006699D0, 4, 4, "R,W"),
        (0x006B8273, 0x006B8270, 0x006B0D20, 4, 4, "R,W"),
        (0x006C0063, 0x006C0060, 0x006BDF60, 4, 4, "R,W"),
        (0x006EC0E0, 0x006EC0D0, 0x006EBD50, 4, 8, "W"),
        (0x006EC0F1, 0x006EC0D0, 0x006EC050, 4, 8, "R"),
        (0x007056A3, 0x007056A0, 0x007022C0, 4, 4, "R,W"),
    }
    if discovered != expected_discovered:
        raise ExtractionError(
            "target-anchored stream discovery acceptance mismatch: %r"
            % sorted(discovered)
        )
    expected_tail_depths = {
        (site, caller)
        for site, caller, _target, _caller_formal, _target_formal, _directions
        in expected_discovered
        if site
        in {
            0x005E36D0,
            0x005E42D2,
            0x005E42DF,
            0x00668523,
            0x006B8273,
            0x006C0063,
            0x007056A3,
        }
    }
    measured_tail_depths = {
        (int(site, 16), int(caller, 16))
        for row in rows
        for site, caller in re.findall(
            r"tail_stack_depth@0x([0-9A-F]{8}) "
            r"file_off=0x[0-9A-F]{8} caller=0x([0-9A-F]{8}) depth=0",
            row.gate_condition,
        )
    }
    if measured_tail_depths != expected_tail_depths:
        raise ExtractionError("target-anchored tail depth acceptance mismatch")
    discovered_claim_offsets = {
        0x001E2AD0,
        0x001E3660,
        0x001E3671,
        0x001E36D2,
        0x001E36DF,
        0x001E5F9F,
        0x001E5FB6,
        0x00267923,
        0x002B7673,
        0x002BF463,
        0x00304AA3,
    }
    if any(
        row.file_off_claim in discovered_claim_offsets and row.tag == "UNKNOWN"
        for row in rows
    ):
        raise ExtractionError("target-anchored stream edge remained UNKNOWN")

    frame_subcalls = [
        row for row in rows if row.file_off_claim == 0x001F3505
    ]
    expected_frame_messages = {
        "GSCN_RunTimeProtocolReq",
        "GSCN_RunTimeProtocolRes",
        "GSCN_LoginProtocol",
        "LSCN_Protocol",
        "VitalProtocol",
    }
    frame_fragment = (
        "stack_formal_base@0x005F3E21 file_off=0x001F3221 "
        "function=0x005F3E20 register=ebp source=esp entry_delta=-0x4"
    )
    if (
        {row.message for row in frame_subcalls} != expected_frame_messages
        or len(frame_subcalls) != 5
        or any(
            row.direction != "R"
            or row.tag != "SUBCALL:0x005F3E20"
            or row.reason
            or frame_fragment not in row.gate_condition
            or "target_stream_anchor_R@0x005F3E6C "
            not in row.gate_condition
            for row in frame_subcalls
        )
    ):
        raise ExtractionError("stack-frame stream subcall acceptance mismatch")
    frame_primitives = [
        row for row in rows if row.file_off_claim == 0x001F326C
    ]
    if (
        {row.message for row in frame_primitives} != expected_frame_messages
        or len(frame_primitives) != 5
        or any(
            row.direction != "R"
            or row.tag != "0x12"
            or row.length != "2"
            or row.span_start != 0x005F3E20
            or row.reason
            or frame_fragment not in row.gate_condition
            for row in frame_primitives
        )
    ):
        raise ExtractionError("stack-frame primitive acceptance mismatch")
    unresolved_frame_primitives = [
        row
        for row in rows
        if row.file_off_claim in (0x001F3298, 0x001F32F4)
        and row.span_start == 0x005F3E20
    ]
    if (
        len(unresolved_frame_primitives) != 10
        or any(
            row.tag != "UNKNOWN"
            or row.reason
            != (
                "primitive_stream_provenance_unresolved "
                "expected=entry+0x4 observed=NONE"
            )
            for row in unresolved_frame_primitives
        )
    ):
        raise ExtractionError("stack-frame fail-closed acceptance mismatch")
    measured_frame_fragments = {
        match
        for row in rows
        for match in re.findall(
            r"stack_formal_base@0x[0-9A-F]{8} "
            r"file_off=0x[0-9A-F]{8} function=0x[0-9A-F]{8} "
            r"register=[a-z]+ source=esp entry_delta=[+-]0x[0-9A-F]+",
            row.gate_condition,
        )
    }
    nested_frame_fragment = (
        "stack_formal_base@0x005E1AD1 file_off=0x001E0ED1 "
        "function=0x005E1AD0 register=ebp source=esp entry_delta=-0x4"
    )
    if measured_frame_fragments != {frame_fragment, nested_frame_fragment}:
        raise ExtractionError("stack-frame evidence census mismatch")

    reaching_pattern = (
        r"formal_reaching_def@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} function=0x[0-9A-F]{8} "
        r"register=[a-z]+ use@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} formal=entry\+0x[0-9A-F]+ "
        r"basis=unique_reaching_definition"
    )
    reaching_fragments = {
        fragment
        for row in rows
        for fragment in re.findall(reaching_pattern, row.gate_condition)
    }
    reaching_example = (
        "formal_reaching_def@0x005F85E2 file_off=0x001F79E2 "
        "function=0x005F85B0 register=ebp use@0x005F86D4 "
        "file_off=0x001F7AD4 formal=entry+0x4 "
        "basis=unique_reaching_definition"
    )
    if len(reaching_fragments) != 264 or reaching_example not in reaching_fragments:
        raise ExtractionError("reaching-definition evidence census mismatch")
    byte_reaching_pattern = (
        r"formal_byte_reaching_def@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} function=0x[0-9A-F]{8} "
        r"lane=[a-z]+ use@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} formal=entry\+0x[0-9A-F]+ "
        r"definition_width=32 consumed_width=8 source=stack_formal "
        r"basis=unique_byte_lane_reaching_definition"
    )
    byte_reaching_occurrences = [
        fragment
        for row in rows
        for fragment in re.findall(byte_reaching_pattern, row.gate_condition)
    ]
    byte_reaching_fragments = set(byte_reaching_occurrences)
    expected_byte_reaching_fragments = {
        "formal_byte_reaching_def@0x0046F609 file_off=0x0006EA09 "
        "function=0x0046F5E0 lane=bl use@0x0046F66A "
        "file_off=0x0006EA6A formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x005E1E37 file_off=0x001E1237 "
        "function=0x005E1E10 lane=bl use@0x005E1E8D "
        "file_off=0x001E128D formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x005ED7D7 file_off=0x001ECBD7 "
        "function=0x005ED7B0 lane=bl use@0x005ED831 "
        "file_off=0x001ECC31 formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x005ED7D7 file_off=0x001ECBD7 "
        "function=0x005ED7B0 lane=bl use@0x005ED84B "
        "file_off=0x001ECC4B formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x005ED7D7 file_off=0x001ECBD7 "
        "function=0x005ED7B0 lane=bl use@0x005ED8AA "
        "file_off=0x001ECCAA formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x00645886 file_off=0x00244C86 "
        "function=0x00645860 lane=bl use@0x006458D0 "
        "file_off=0x00244CD0 formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x00645886 file_off=0x00244C86 "
        "function=0x00645860 lane=bl use@0x0064594A "
        "file_off=0x00244D4A formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x00668CD6 file_off=0x002680D6 "
        "function=0x00668CB0 lane=bl use@0x00668D15 "
        "file_off=0x00268115 formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x006A1236 file_off=0x002A0636 "
        "function=0x006A1210 lane=bl use@0x006A129A "
        "file_off=0x002A069A formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
        "formal_byte_reaching_def@0x00700BF7 file_off=0x002FFFF7 "
        "function=0x00700BD0 lane=bl use@0x00700C5B "
        "file_off=0x0030005B formal=entry+0x8 definition_width=32 "
        "consumed_width=8 source=stack_formal "
        "basis=unique_byte_lane_reaching_definition",
    }
    if (
        len(byte_reaching_occurrences) != 66
        or byte_reaching_fragments != expected_byte_reaching_fragments
    ):
        raise ExtractionError("byte-lane reaching evidence census mismatch")
    zero_reaching_pattern = (
        r"mode_zero_reaching_def@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} function=0x[0-9A-F]{8} "
        r"register=[a-z]+ use@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} consumed_width=1 value=zero "
        r"basis=unique_full_width_xor_self "
        r"mode_arg@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} value=zero"
    )
    zero_reaching_occurrences = [
        fragment
        for row in rows
        for fragment in re.findall(zero_reaching_pattern, row.gate_condition)
    ]
    expected_zero_reaching_fragments = {
        "mode_zero_reaching_def@0x0060176E file_off=0x00200B6E "
        "function=0x006016D0 register=edi use@0x006017B5 "
        "file_off=0x00200BB5 consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x006017B5 file_off=0x00200BB5 value=zero",
        "mode_zero_reaching_def@0x0062431F file_off=0x0022371F "
        "function=0x00624240 register=ebx use@0x006243B0 "
        "file_off=0x002237B0 consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x006243B0 file_off=0x002237B0 value=zero",
        "mode_zero_reaching_def@0x0062507A file_off=0x0022447A "
        "function=0x00624FB0 register=ebp use@0x006250FC "
        "file_off=0x002244FC consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x006250FC file_off=0x002244FC value=zero",
        "mode_zero_reaching_def@0x0066D487 file_off=0x0026C887 "
        "function=0x0066D460 register=ebp use@0x0066DB6A "
        "file_off=0x0026CF6A consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x0066DB6A file_off=0x0026CF6A value=zero",
        "mode_zero_reaching_def@0x0066D487 file_off=0x0026C887 "
        "function=0x0066D460 register=ebp use@0x0066DC3D "
        "file_off=0x0026D03D consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x0066DC3D file_off=0x0026D03D value=zero",
        "mode_zero_reaching_def@0x0066D487 file_off=0x0026C887 "
        "function=0x0066D460 register=ebp use@0x0066DF61 "
        "file_off=0x0026D361 consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x0066DF61 file_off=0x0026D361 value=zero",
        "mode_zero_reaching_def@0x006BA883 file_off=0x002B9C83 "
        "function=0x006BA7B0 register=ebp use@0x006BA8C3 "
        "file_off=0x002B9CC3 consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x006BA8C3 file_off=0x002B9CC3 value=zero",
        "mode_zero_reaching_def@0x006EC06C file_off=0x002EB46C "
        "function=0x006EC050 register=ebx use@0x006EC082 "
        "file_off=0x002EB482 consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x006EC082 file_off=0x002EB482 value=zero",
        "mode_zero_reaching_def@0x00713A36 file_off=0x00312E36 "
        "function=0x00713910 register=ebx use@0x00713A92 "
        "file_off=0x00312E92 consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x00713A92 file_off=0x00312E92 value=zero",
        "mode_zero_reaching_def@0x0073E70C file_off=0x0033DB0C "
        "function=0x0073E6F0 register=edi use@0x0073E720 "
        "file_off=0x0033DB20 consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x0073E720 file_off=0x0033DB20 value=zero",
        "mode_zero_reaching_def@0x0076A882 file_off=0x00369C82 "
        "function=0x0076A740 register=ebp use@0x0076A8DC "
        "file_off=0x00369CDC consumed_width=1 value=zero "
        "basis=unique_full_width_xor_self "
        "mode_arg@0x0076A8DC file_off=0x00369CDC value=zero",
    }
    if (
        len(zero_reaching_occurrences) != 185
        or set(zero_reaching_occurrences)
        != expected_zero_reaching_fragments
    ):
        raise ExtractionError("mode zero reaching evidence census mismatch")
    zero_set_pattern = (
        r"mode_zero_reaching_set function=0x[0-9A-F]{8} "
        r"register=[a-z]+ use@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} consumed_width=1 value=zero "
        r"definition_count=[0-9]+ definitions=\("
        r"definition@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8}"
        r"(?:,definition@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8})+\) "
        r"basis=all_reaching_full_width_xor_self "
        r"mode_arg@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} value=zero"
    )
    zero_set_occurrences = [
        fragment
        for row in rows
        for fragment in re.findall(zero_set_pattern, row.gate_condition)
    ]
    zero_set_example = (
        "mode_zero_reaching_set function=0x007156D0 register=ebx "
        "use@0x00715870 file_off=0x00314C70 consumed_width=1 "
        "value=zero definition_count=2 definitions=("
        "definition@0x007157E6 file_off=0x00314BE6,"
        "definition@0x00715910 file_off=0x00314D10) "
        "basis=all_reaching_full_width_xor_self "
        "mode_arg@0x00715870 file_off=0x00314C70 value=zero"
    )
    if (
        len(zero_set_occurrences) != 23
        or set(zero_set_occurrences) != {zero_set_example}
    ):
        raise ExtractionError("mode zero reaching-set evidence census mismatch")
    identity_pattern = (
        r"formal_identity_lea@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} function=0x[0-9A-F]{8} "
        r"register=[a-z]+ continuation@0x[0-9A-F]{8} "
        r"file_off=0x[0-9A-F]{8} formal=entry\+0x[0-9A-F]+ "
        r"basis=full_width_zero_displacement"
    )
    identity_fragments = {
        fragment
        for row in rows
        for fragment in re.findall(identity_pattern, row.gate_condition)
    }
    identity_example = (
        "formal_identity_lea@0x00755D7A file_off=0x0035517A "
        "function=0x00755D30 register=ebx continuation@0x00755D80 "
        "file_off=0x00355180 formal=entry+0x8 "
        "basis=full_width_zero_displacement"
    )
    byte_identity_example = (
        "formal_identity_lea@0x00700A5A file_off=0x002FFE5A "
        "function=0x007009D0 register=ebx continuation@0x00700A60 "
        "file_off=0x002FFE60 formal=entry+0x8 "
        "basis=full_width_zero_displacement"
    )
    identity_rows = [
        row
        for row in rows
        if row.file_off_claim in (0x003551C8, 0x003551DA, 0x003551E6)
    ]
    if (
        identity_fragments != {identity_example, byte_identity_example}
        or len(identity_rows) != 3
        or {row.message for row in identity_rows}
        != {"CLearnSkillResultVital"}
        or {
            (row.file_off_claim, row.direction, row.tag, row.length)
            for row in identity_rows
        }
        != {
            (0x003551C8, "W", "0x14", "4"),
            (0x003551DA, "W", "0x12", "2"),
            (0x003551E6, "W", "0x14", "4"),
        }
        or any(
            row.reason or identity_example not in row.gate_condition
            for row in identity_rows
        )
    ):
        raise ExtractionError("identity LEA formal acceptance mismatch")
    byte_identity_rows = [
        row
        for row in rows
        if row.message == "Pets_ChangePetEquipmentVital"
        and row.file_off_claim == 0x002FFE7B
    ]
    if (
        len(byte_identity_rows) != 1
        or byte_identity_rows[0].direction != "W"
        or byte_identity_rows[0].tag != "SUBCALL:0x006F3E20"
        or byte_identity_rows[0].reason
        or byte_identity_example not in byte_identity_rows[0].gate_condition
        or not has_local_direction_proof(byte_identity_rows[0])
        or not has_local_stream_proof(byte_identity_rows[0])
    ):
        raise ExtractionError("byte consumer identity-LEA acceptance mismatch")
    isolated_symbolic_rows = [
        row
        for row in rows
        if row.message == "Pets_ChangePetEquipmentVital"
        and row.file_off_claim == 0x002FFFA0
    ]
    isolated_symbolic_tag = (
        "CALL_UNCLASSIFIED:INDIRECT("
        "DEREF(DEREF(DEREF(PHI(OBJ|PHI(OBJ|REG(edi)))+0x3C))+0x10))"
    )
    if (
        len(isolated_symbolic_rows) != 2
        or {row.direction for row in isolated_symbolic_rows} != {"W", "R"}
        or any(
            row.tag != isolated_symbolic_tag
            or row.reason != "indirect_call_not_proven_serializer_slot"
            for row in isolated_symbolic_rows
        )
    ):
        raise ExtractionError("isolated symbolic-query acceptance mismatch")
    loop_write_rows = [
        row for row in rows if row.file_off_claim == 0x001F7AD5
    ]
    loop_read_rows = [
        row for row in rows if row.file_off_claim == 0x001F7BCC
    ]
    if (
        len(loop_write_rows) != 1
        or len(loop_read_rows) != 1
        or loop_write_rows[0].direction != "W"
        or loop_write_rows[0].tag != "SUBCALL:0x005F3490"
        or reaching_example not in loop_write_rows[0].gate_condition
        or loop_read_rows[0].direction != "R"
        or loop_read_rows[0].tag != "SUBCALL:0x005F34D0"
    ):
        raise ExtractionError("loop reaching-definition direction mismatch")
    filtered_singleton_rows = [
        row
        for row in rows
        if row.file_off_claim
        in {
            0x001DE6A0,
            0x001DE6EC,
            0x001F7AD5,
            0x001F7BCC,
            0x00225D8E,
            0x00225E3B,
        }
    ]
    if (
        {
            (row.message, row.direction, row.file_off_claim, row.tag)
            for row in filtered_singleton_rows
        }
        != {
            ("TeleportVital", "W", 0x001DE6A0, "SUBCALL:0x005F3490"),
            ("TeleportVital", "R", 0x001DE6EC, "SUBCALL:0x005F34D0"),
            ("ReliveMarkerVital", "W", 0x001DE6A0, "SUBCALL:0x005F3490"),
            ("ReliveMarkerVital", "R", 0x001DE6EC, "SUBCALL:0x005F34D0"),
            (
                "GSCN_RunTimeProtocolRes",
                "W",
                0x001F7AD5,
                "SUBCALL:0x005F3490",
            ),
            (
                "GSCN_RunTimeProtocolRes",
                "R",
                0x001F7BCC,
                "SUBCALL:0x005F34D0",
            ),
            ("PartyUpdateVital", "W", 0x00225D8E, "SUBCALL:0x005F3490"),
            ("PartyUpdateVital", "R", 0x00225E3B, "SUBCALL:0x005F34D0"),
        }
        or len(filtered_singleton_rows) != 8
        or any(row.reason for row in filtered_singleton_rows)
        or any("subcall_direction_conflict" in row.reason for row in rows)
    ):
        raise ExtractionError("singleton branch filtering mismatch")
    hit_write_rows = [
        row for row in rows if row.file_off_claim == 0x0034EA45
    ]
    hit_read_rows = [
        row for row in rows if row.file_off_claim == 0x0034F3EA
    ]
    expected_hit_messages = {"CHitResult", "CMissileHitResult"}
    if (
        {row.message for row in hit_write_rows} != expected_hit_messages
        or {row.message for row in hit_read_rows} != expected_hit_messages
        or len(hit_write_rows) != 2
        or len(hit_read_rows) != 2
        or any(
            row.direction != "W" or row.tag != "SUBCALL:0x005F3490"
            for row in hit_write_rows
        )
        or any(
            row.direction != "R" or row.tag != "SUBCALL:0x005F34D0"
            for row in hit_read_rows
        )
    ):
        raise ExtractionError("hit-result reaching-definition mismatch")
    guild_loop_rows = [
        row for row in rows if row.file_off_claim == 0x0026CA4D
    ]
    if (
        len(guild_loop_rows) != 2
        or {row.message for row in guild_loop_rows}
        != {"GSSS_GuildDataVitalRes", "GSSS_GSInitialGuildDataVital"}
        or any(
            row.direction != "W" or row.tag != "SUBCALL:0x0066A320"
            for row in guild_loop_rows
        )
    ):
        raise ExtractionError("nested caller-ABI reaching proof mismatch")
    remaining_stream_unknown = [
        row
        for row in rows
        if row.tag == "UNKNOWN"
        and "subcall_stream_provenance_unresolved" in row.reason
    ]
    if (
        len(remaining_stream_unknown) != 4
        or {row.file_off_claim for row in remaining_stream_unknown}
        != {0x0022526C, 0x00236C0C}
    ):
        raise ExtractionError("reaching-definition fail-closed census mismatch")
    promoted_byte_lane_subcalls = {
        (row.message, row.file_off_claim, row.tag)
        for row in rows
        if row.tag.startswith("SUBCALL:")
        and "formal_byte_reaching_def@" in row.gate_condition
        and has_local_direction_proof(row)
    }
    expected_promoted_byte_lane_subcalls = {
        ("InstanceStatisticVital", 0x001ECC4C, "SUBCALL:0x005DF4E0"),
        ("InstanceStatisticVital", 0x001ECCAB, "SUBCALL:0x005E16D0"),
        ("ReArrangeBagReply", 0x0006EA6B, "SUBCALL:0x0046D240"),
        (
            "GCGSSS_GuildStorageVital_ReArrangeResult",
            0x0006EA6B,
            "SUBCALL:0x0046D240",
        ),
        (
            "Community_InitalizeActorCommunityVital",
            0x00244D4B,
            "SUBCALL:0x00637E10",
        ),
        (
            "GSSS_GuildUpdateQuestMemberVital",
            0x00268118,
            "SUBCALL:0x00669F50",
        ),
        (
            "Activity_SendRankingVital",
            0x002A069B,
            "SUBCALL:0x0069BDF0",
        ),
        ("PartyUpdateVital", 0x001E128E, "SUBCALL:0x005DF570"),
        (
            "Pets_SetPetSkillVital",
            0x0030005C,
            "SUBCALL:0x006F3E90",
        ),
    }
    if (
        promoted_byte_lane_subcalls != expected_promoted_byte_lane_subcalls
        or any(
            row.direction != "W" or row.reason
            for row in rows
            if (
                row.message,
                row.file_off_claim,
                row.tag,
            )
            in expected_promoted_byte_lane_subcalls
        )
    ):
        raise ExtractionError("byte-lane direction promotion mismatch")
    promoted_zero_subcalls = {
        (row.message, row.file_off_claim, row.tag)
        for row in rows
        if row.tag.startswith("SUBCALL:")
        and "mode_zero_reaching_def@" in (
            local_direction_proof_segment(row) or ""
        )
    }
    expected_promoted_zero_subcalls = {
        ("TriggerSyncVital", 0x00200BBD, "SUBCALL:0x005FC050"),
        ("CArenaGameDataVital", 0x00224500, "SUBCALL:0x00624240"),
        ("CArenaGameDataVital", 0x002237B4, "SUBCALL:0x00623800"),
        ("GSSS_GuildDataVitalRes", 0x0026CF6E, "SUBCALL:0x0066A320"),
        ("GSSS_GuildDataVitalRes", 0x0026D041, "SUBCALL:0x0066AE60"),
        ("GSSS_GuildDataVitalRes", 0x0026D365, "SUBCALL:0x00669F50"),
        (
            "GSSS_GSInitialGuildDataVital",
            0x0026CF6E,
            "SUBCALL:0x0066A320",
        ),
        (
            "GSSS_GSInitialGuildDataVital",
            0x0026D041,
            "SUBCALL:0x0066AE60",
        ),
        (
            "GSSS_GSInitialGuildDataVital",
            0x0026D365,
            "SUBCALL:0x00669F50",
        ),
        ("ItemMallGashaponDesVital", 0x002B9CCB, "SUBCALL:0x006BB000"),
        ("CTracePathVital", 0x002EB4AF, "SUBCALL:0x006EB960"),
        ("CHitParadeVital", 0x00312E96, "SUBCALL:0x00712F70"),
        ("CHitParadeResVital_JP", 0x00312E96, "SUBCALL:0x00712F70"),
        ("CWebGMVital_GSGC", 0x0033DB32, "SUBCALL:0x0073ADA0"),
        ("StallStartVital", 0x00369CE4, "SUBCALL:0x00766C00"),
    }
    if (
        promoted_zero_subcalls != expected_promoted_zero_subcalls
        or any(
            row.direction != "R" or row.reason
            for row in rows
            if (
                row.message,
                row.file_off_claim,
                row.tag,
            )
            in expected_promoted_zero_subcalls
        )
    ):
        raise ExtractionError("mode zero direction promotion mismatch")
    promoted_zero_set_subcalls = [
        row
        for row in rows
        if row.message == "CHitParadeVital"
        and row.file_off_claim == 0x00314C74
    ]
    if (
        len(promoted_zero_set_subcalls) != 1
        or promoted_zero_set_subcalls[0].direction != "R"
        or promoted_zero_set_subcalls[0].tag != "SUBCALL:0x00713910"
        or promoted_zero_set_subcalls[0].reason
        or zero_set_example
        not in promoted_zero_set_subcalls[0].gate_condition
        or not has_local_direction_proof(promoted_zero_set_subcalls[0])
        or not has_local_stream_proof(promoted_zero_set_subcalls[0])
    ):
        raise ExtractionError("mode zero reaching-set promotion mismatch")

    nested_outer_subcalls = {
        (row.direction, row.file_off_claim, row.tag)
        for row in rows
        if row.message == "GSCN_RunTimeProtocolRes"
        and row.file_off_claim in (0x001E333B, 0x001E33C0)
    }
    if nested_outer_subcalls != {
        ("W", 0x001E333B, "SUBCALL:0x005E1C10"),
        ("R", 0x001E33C0, "SUBCALL:0x005E1C10"),
    }:
        raise ExtractionError("nested mode outer-call promotion mismatch")
    nested_outer_rows = [
        row
        for row in rows
        if row.message == "GSCN_RunTimeProtocolRes"
        and row.file_off_claim in (0x001E333B, 0x001E33C0)
    ]
    if any(
        row.reason
        or not has_local_direction_proof(row)
        or not has_local_stream_proof(row)
        or "target_nested_stream_anchor_%s@" % row.direction
        not in row.gate_condition
        for row in nested_outer_rows
    ):
        raise ExtractionError("nested mode outer-call evidence mismatch")
    nested_child_subcalls = {
        (row.direction, row.file_off_claim, row.tag, row.span_start)
        for row in rows
        if row.message == "GSCN_RunTimeProtocolRes"
        and row.span_start == 0x005E1C10
    }
    if nested_child_subcalls != {
        ("W", 0x001E101C, "SUBCALL:0x005E01D0", 0x005E1C10),
        ("R", 0x001E1029, "SUBCALL:0x005E1AD0", 0x005E1C10),
    }:
        raise ExtractionError("nested mode branch recursion mismatch")
    nested_primitives = {
        (
            row.direction,
            row.file_off_claim,
            row.tag,
            row.length,
            row.span_start,
        )
        for row in rows
        if row.message == "GSCN_RunTimeProtocolRes"
        and row.file_off_claim in (0x001DF5EE, 0x001E0F0E)
    }
    if nested_primitives != {
        ("W", 0x001DF5EE, "0x12", "2", 0x005E01D0),
        ("R", 0x001E0F0E, "0x12", "2", 0x005E1AD0),
    }:
        raise ExtractionError("nested mode primitive recursion mismatch")
    expected_nested_mode_anchors = {
        "mode_nested_anchor_R@0x005E1C29 file_off=0x001E1029 "
        "function=0x005E1C10 target=0x005E1AD0 "
        "caller_stream_formal=entry+0x4 target_stream_formal=entry+0x4 "
        "arguments=(argument@0x005E1C28 file_off=0x001E1028) "
        "primitives=(primitive@0x005E1B0E file_off=0x001E0F0E "
        "target=0x0089A640) "
        "stream_proof_sha256="
        "73339c33ddfbe3d56d56b612e3800fddd33deec802cdd663fa962081abe25b1b "
        "basis=branch_exclusive_single_direction_direct_subcall",
        "mode_nested_anchor_W@0x005E1C1C file_off=0x001E101C "
        "function=0x005E1C10 target=0x005E01D0 "
        "caller_stream_formal=entry+0x4 target_stream_formal=entry+0x4 "
        "arguments=(argument@0x005E1C1B file_off=0x001E101B) "
        "primitives=(primitive@0x005E01EE file_off=0x001DF5EE "
        "target=0x0089A600) "
        "stream_proof_sha256="
        "a40b459ad944d3026e3386dad6dfece117d2bf64105cce5a1377ea1b7ba69cfa "
        "basis=branch_exclusive_single_direction_direct_subcall",
    }
    measured_nested_mode_anchors = {
        match.group(0)
        for row in rows
        for match in re.finditer(
            r"mode_nested_anchor_[WR]@0x[0-9A-F]{8} "
            r"file_off=0x[0-9A-F]{8} function=0x[0-9A-F]{8} "
            r"target=0x[0-9A-F]{8} "
            r"caller_stream_formal=entry\+0x[0-9A-F]+ "
            r"target_stream_formal=entry\+0x[0-9A-F]+ "
            r"arguments=\([^)]*\) primitives=\([^)]*\) "
            r"stream_proof_sha256=[0-9a-f]{64} "
            r"basis=branch_exclusive_single_direction_direct_subcall",
            row.gate_condition,
        )
    }
    if (
        measured_nested_mode_anchors != expected_nested_mode_anchors
        or sum(
            row.gate_condition.count("mode_nested_anchor_") for row in rows
        )
        != 36
    ):
        raise ExtractionError("nested mode anchor census mismatch")
    expected_nested_stream_anchors = {
        "target_nested_stream_anchor_R@0x005E1C29 file_off=0x001E1029 "
        "function=0x005E1C10 target=0x005E1AD0 "
        "target_formal=entry+0x4 child_formal=entry+0x4 "
        "mode_formal=entry+0x8 mode_value=zero "
        "nested_evidence_sha256="
        "4d7e09ad072840f70f48e31490440d425c9248c87542343848559ff21ca857e9 "
        "basis=direction_selected_branch_exclusive_subcall",
        "target_nested_stream_anchor_W@0x005E1C1C file_off=0x001E101C "
        "function=0x005E1C10 target=0x005E01D0 "
        "target_formal=entry+0x4 child_formal=entry+0x4 "
        "mode_formal=entry+0x8 mode_value=nonzero "
        "nested_evidence_sha256="
        "bff27cd0a87b969ed08b9c5e55733551349edb2862f36142e064d8203d1e2740 "
        "basis=direction_selected_branch_exclusive_subcall",
    }
    measured_nested_stream_anchors = {
        match.group(0)
        for row in rows
        for match in re.finditer(
            r"target_nested_stream_anchor_[WR]@0x[0-9A-F]{8} "
            r"file_off=0x[0-9A-F]{8} function=0x[0-9A-F]{8} "
            r"target=0x[0-9A-F]{8} "
            r"target_formal=entry\+0x[0-9A-F]+ "
            r"child_formal=entry\+0x[0-9A-F]+ "
            r"mode_formal=entry\+0x[0-9A-F]+ "
            r"mode_value=(?:zero|nonzero) "
            r"nested_evidence_sha256=[0-9a-f]{64} "
            r"basis=direction_selected_branch_exclusive_subcall",
            row.gate_condition,
        )
    }
    if (
        measured_nested_stream_anchors != expected_nested_stream_anchors
        or sum(
            row.gate_condition.count("target_nested_stream_anchor_")
            for row in rows
        )
        != 18
    ):
        raise ExtractionError("nested stream anchor census mismatch")
    predicate_promoted_subcalls = {
        (row.message, row.direction, row.file_off_claim, row.tag)
        for row in rows
        if row.file_off_claim in (0x002BC6C0, 0x002BCB3F, 0x002C0195)
    }
    if predicate_promoted_subcalls != {
        (
            "ItemMallIMSDataRes",
            "W",
            0x002BC6C0,
            "SUBCALL:0x006BC5D0",
        ),
        (
            "ItemMallIMSDataRes",
            "R",
            0x002BCB3F,
            "SUBCALL:0x006BC5D0",
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "W",
            0x002C0195,
            "SUBCALL:0x006BE1F0",
        ),
    }:
        raise ExtractionError("predicate zero subcall promotion mismatch")
    predicate_promoted_rows = [
        row
        for row in rows
        if row.file_off_claim in (0x002BC6C0, 0x002BCB3F, 0x002C0195)
    ]
    if any(
        row.reason
        or not has_local_direction_proof(row)
        or not has_local_stream_proof(row)
        or "predicate_zero_reaching" not in row.gate_condition
        for row in predicate_promoted_rows
    ):
        raise ExtractionError("predicate zero subcall evidence mismatch")
    predicate_numeric_rows = {
        (
            row.message,
            row.direction,
            row.file_off_claim,
            row.tag,
            row.length,
            row.span_start,
        )
        for row in rows
        if "predicate_zero_reaching" in row.gate_condition
        and re.fullmatch(r"0x[0-9A-F]{2}", row.tag)
    }
    if predicate_numeric_rows != {
        ("ItemMallIMSDataRes", "W", 0x002BB9F0, "0x0F", "2", 0x006BC5D0),
        ("ItemMallIMSDataRes", "W", 0x002BB9FF, "0x14", "4", 0x006BC5D0),
        ("ItemMallIMSDataRes", "W", 0x002BBA35, "0x12", "2", 0x006BC5D0),
        ("ItemMallIMSDataRes", "W", 0x002BBA6A, "0x14", "4", 0x006BC5D0),
        ("ItemMallIMSDataRes", "R", 0x002BBA84, "0x0F", "2", 0x006BC5D0),
        ("ItemMallIMSDataRes", "R", 0x002BBA93, "0x14", "4", 0x006BC5D0),
        ("ItemMallIMSDataRes", "R", 0x002BBABD, "0x12", "2", 0x006BC5D0),
        ("ItemMallIMSDataRes", "R", 0x002BBADF, "0x14", "4", 0x006BC5D0),
        (
            "GSCN_BlackMarketSearchReply",
            "W",
            0x002BD60B,
            "0x32",
            "8",
            0x006BE1F0,
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "W",
            0x002BD61A,
            "0x19",
            "4",
            0x006BE1F0,
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "W",
            0x002BD629,
            "0x14",
            "4",
            0x006BE1F0,
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "W",
            0x002BD64F,
            "0x08",
            "1",
            0x006BE1F0,
        ),
    }:
        raise ExtractionError("predicate zero numeric recursion mismatch")
    refined_outer_subcalls = {
        (row.message, row.direction, row.file_off_claim, row.tag)
        for row in rows
        if row.file_off_claim
        in (0x002EB4E0, 0x002EB4F1, 0x0033DB74, 0x0033DB94)
    }
    if refined_outer_subcalls != {
        ("CTracePathVital", "W", 0x002EB4E0, "SUBCALL:0x006EBD50"),
        ("CTracePathVital", "R", 0x002EB4F1, "SUBCALL:0x006EC050"),
        ("CWebGMVital_GSGC", "W", 0x0033DB74, "SUBCALL:0x0073E240"),
        ("CWebGMVital_GSGC", "R", 0x0033DB94, "SUBCALL:0x0073E6F0"),
    }:
        raise ExtractionError("local capability outer-call promotion mismatch")
    refined_outer_rows = [
        row
        for row in rows
        if row.file_off_claim
        in (0x002EB4E0, 0x002EB4F1, 0x0033DB74, 0x0033DB94)
    ]
    if any(
        row.reason
        or not has_local_stream_proof(row)
        or "local_capability_refinement" not in row.gate_condition
        for row in refined_outer_rows
    ):
        raise ExtractionError("local capability outer-call evidence mismatch")
    refined_numeric_rows = {
        (
            row.message,
            row.direction,
            row.file_off_claim,
            row.tag,
            row.length,
            row.span_start,
        )
        for row in rows
        if "local_capability_refinement" in row.gate_condition
        and re.fullmatch(r"0x[0-9A-F]{2}", row.tag)
    }
    if refined_numeric_rows != {
        ("CTracePathVital", "W", 0x002EB183, "0x12", "2", 0x006EBD50),
        ("CTracePathVital", "W", 0x002EAD7E, "0x08", "1", 0x006EB960),
        ("CTracePathVital", "W", 0x002EAD8D, "0x0F", "2", 0x006EB960),
        ("CTracePathVital", "W", 0x002EAD9C, "0x0F", "2", 0x006EB960),
        ("CTracePathVital", "W", 0x002EADAB, "0x0F", "2", 0x006EB960),
        ("CTracePathVital", "W", 0x002EADB7, "0x14", "4", 0x006EB960),
        ("CTracePathVital", "W", 0x002EADCD, "0x14", "4", 0x006EB960),
        ("CTracePathVital", "W", 0x002EADDC, "0x14", "4", 0x006EB960),
        ("CTracePathVital", "W", 0x002EADFA, "0x14", "4", 0x006EB960),
        ("CTracePathVital", "R", 0x002EB465, "0x12", "2", 0x006EC050),
        ("CTracePathVital", "R", 0x002EAE05, "0x08", "1", 0x006EB960),
        ("CTracePathVital", "R", 0x002EAE14, "0x0F", "2", 0x006EB960),
        ("CTracePathVital", "R", 0x002EAE23, "0x0F", "2", 0x006EB960),
        ("CTracePathVital", "R", 0x002EAE32, "0x0F", "2", 0x006EB960),
        ("CTracePathVital", "R", 0x002EAE3E, "0x14", "4", 0x006EB960),
        ("CTracePathVital", "R", 0x002EAE54, "0x14", "4", 0x006EB960),
        ("CTracePathVital", "R", 0x002EAE63, "0x14", "4", 0x006EB960),
        ("CTracePathVital", "R", 0x002EAE7D, "0x14", "4", 0x006EB960),
        ("CWebGMVital_GSGC", "W", 0x0033D672, "0x12", "2", 0x0073E240),
        ("CWebGMVital_GSGC", "W", 0x0033A1C4, "0x12", "2", 0x0073ADA0),
        ("CWebGMVital_GSGC", "W", 0x0033A1E2, "0x32", "8", 0x0073ADA0),
        ("CWebGMVital_GSGC", "R", 0x0033DB05, "0x12", "2", 0x0073E6F0),
        ("CWebGMVital_GSGC", "R", 0x0033A1F8, "0x12", "2", 0x0073ADA0),
        ("CWebGMVital_GSGC", "R", 0x0033A21F, "0x32", "8", 0x0073ADA0),
    }:
        raise ExtractionError("local capability numeric recursion mismatch")
    if (
        sum(
            row.gate_condition.count("local_capability_refinement")
            for row in rows
        )
        != 48
    ):
        raise ExtractionError("local capability evidence occurrence mismatch")
    identity_promoted_subcalls = {
        (row.message, row.direction, row.file_off_claim, row.tag)
        for row in rows
        if row.tag.startswith("SUBCALL:")
        and "mode_zero_identity_lea" in row.gate_condition
    }
    if identity_promoted_subcalls != {
        ("ReArrangeBagReply", "R", 0x0006EB39, "SUBCALL:0x0046D240"),
        ("NPCConversation", "R", 0x00222439, "SUBCALL:0x00606890"),
        (
            "GCGSSS_GuildStorageVital_ReArrangeResult",
            "R",
            0x0006EB39,
            "SUBCALL:0x0046D240",
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "R",
            0x002C0229,
            "SUBCALL:0x006BE1F0",
        ),
    }:
        raise ExtractionError("identity-LEA zero subcall promotion mismatch")
    identity_promoted_rows = [
        row
        for row in rows
        if row.tag.startswith("SUBCALL:")
        and "mode_zero_identity_lea" in row.gate_condition
    ]
    if any(
        row.reason
        or not has_local_direction_proof(row)
        or not has_local_stream_proof(row)
        for row in identity_promoted_rows
    ):
        raise ExtractionError("identity-LEA zero subcall evidence mismatch")
    identity_numeric_rows = {
        (
            row.message,
            row.direction,
            row.file_off_claim,
            row.tag,
            row.length,
            row.span_start,
        )
        for row in rows
        if "mode_zero_identity_lea" in row.gate_condition
        and re.fullmatch(r"0x[0-9A-F]{2}", row.tag)
    }
    if identity_numeric_rows != {
        ("ReArrangeBagReply", "R", 0x0006C687, "0x32", "8", 0x0046D240),
        ("ReArrangeBagReply", "R", 0x0006C696, "0x0F", "2", 0x0046D240),
        ("ReArrangeBagReply", "R", 0x0006C6A5, "0x0F", "2", 0x0046D240),
        ("NPCConversation", "R", 0x00205CCA, "0x12", "2", 0x00606890),
        ("NPCConversation", "R", 0x00205CD9, "0x08", "1", 0x00606890),
        (
            "GCGSSS_GuildStorageVital_ReArrangeResult",
            "R",
            0x0006C687,
            "0x32",
            "8",
            0x0046D240,
        ),
        (
            "GCGSSS_GuildStorageVital_ReArrangeResult",
            "R",
            0x0006C696,
            "0x0F",
            "2",
            0x0046D240,
        ),
        (
            "GCGSSS_GuildStorageVital_ReArrangeResult",
            "R",
            0x0006C6A5,
            "0x0F",
            "2",
            0x0046D240,
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "R",
            0x002BD671,
            "0x32",
            "8",
            0x006BE1F0,
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "R",
            0x002BD680,
            "0x19",
            "4",
            0x006BE1F0,
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "R",
            0x002BD68F,
            "0x14",
            "4",
            0x006BE1F0,
        ),
        (
            "GSCN_BlackMarketSearchReply",
            "R",
            0x002BD6AF,
            "0x08",
            "1",
            0x006BE1F0,
        ),
    }:
        raise ExtractionError("identity-LEA zero numeric recursion mismatch")
    expected_identity_zero_fragments = {
        "mode_zero_identity_lea function=0x0046F5E0 register=ebx "
        "use@0x0046F731 file_off=0x0006EB31 consumed_width=1 value=zero "
        "identity@0x0046F70A file_off=0x0006EB0A definition_count=1 "
        "definitions=(definition@0x0046F6EE file_off=0x0006EAEE) "
        "basis=all_reaching_full_width_xor_self_through_exact_"
        "full_width_identity_lea "
        "mode_arg@0x0046F731 file_off=0x0006EB31 value=zero",
        "mode_zero_identity_lea function=0x00622F10 register=ebx "
        "use@0x00623031 file_off=0x00222431 consumed_width=1 value=zero "
        "identity@0x0062300A file_off=0x0022240A definition_count=1 "
        "definitions=(definition@0x00622FEB file_off=0x002223EB) "
        "basis=all_reaching_full_width_xor_self_through_exact_"
        "full_width_identity_lea "
        "mode_arg@0x00623031 file_off=0x00222431 value=zero",
        "mode_zero_identity_lea function=0x006C0CE0 register=ebx "
        "use@0x006C0E21 file_off=0x002C0221 consumed_width=1 value=zero "
        "identity@0x006C0DFA file_off=0x002C01FA definition_count=1 "
        "definitions=(definition@0x006C0D07 file_off=0x002C0107) "
        "basis=all_reaching_full_width_xor_self_through_exact_"
        "full_width_identity_lea "
        "mode_arg@0x006C0E21 file_off=0x002C0221 value=zero",
    }
    measured_identity_zero_fragments = {
        match.group(0)
        for row in rows
        for match in re.finditer(
            r"mode_zero_identity_lea function=0x[0-9A-F]{8} "
            r"register=(?:eax|ecx|edx|ebx|ebp|esi|edi) "
            r"use@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} "
            r"consumed_width=1 value=zero "
            r"identity@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} "
            r"definition_count=[0-9]+ definitions=\([^)]*\) "
            r"basis=all_reaching_full_width_xor_self_through_exact_"
            r"full_width_identity_lea "
            r"mode_arg@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} "
            r"value=zero",
            row.gate_condition,
        )
    }
    if (
        measured_identity_zero_fragments
        != expected_identity_zero_fragments
        or sum(
            row.gate_condition.count("mode_zero_identity_lea")
            for row in rows
        )
        != 22
    ):
        raise ExtractionError("identity-LEA zero evidence census mismatch")
    expected_predicate_zero_proofs = {
        "predicate_zero_reaching function=0x006BC5D0 lane=bl "
        "register=ebx use@0x006BC5E0 file_off=0x002BB9E0 "
        "consumed_width=1 value=zero definition_count=1 "
        "definitions=(definition@0x006BC5D8 file_off=0x002BB9D8) "
        "basis=all_reaching_full_width_xor_self",
        "predicate_zero_reaching function=0x006C0CE0 lane=bl "
        "register=ebx use@0x006C0D0B file_off=0x002C010B "
        "consumed_width=1 value=zero definition_count=1 "
        "definitions=(definition@0x006C0D07 file_off=0x002C0107) "
        "basis=all_reaching_full_width_xor_self",
    }
    measured_predicate_zero_proofs = {
        match.group(0)
        for row in rows
        for match in re.finditer(
            r"predicate_zero_reaching function=0x[0-9A-F]{8} "
            r"lane=(?:al|cl|dl|bl) register=(?:eax|ecx|edx|ebx) "
            r"use@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} "
            r"consumed_width=1 value=zero definition_count=[0-9]+ "
            r"definitions=\([^)]*\) "
            r"basis=all_reaching_full_width_xor_self",
            row.gate_condition,
        )
    }
    if (
        measured_predicate_zero_proofs != expected_predicate_zero_proofs
        or sum(
            row.gate_condition.count("predicate_zero_reaching")
            for row in rows
        )
        != 29
    ):
        raise ExtractionError("predicate zero evidence census mismatch")
    stack_identity_promoted_rows = [
        row
        for row in rows
        if row.file_off_claim in (0x00293CD3, 0x00312DCC, 0x00369C36)
        and row.tag.startswith("SUBCALL:")
    ]
    if {
        (row.message, row.direction, row.file_off_claim, row.tag)
        for row in stack_identity_promoted_rows
    } != {
        (
            "PlayerSearchVitalRes",
            "W",
            0x00293CD3,
            "SUBCALL:0x006944E0",
        ),
        (
            "CHitParadeVital",
            "W",
            0x00312DCC,
            "SUBCALL:0x00712F70",
        ),
        (
            "CHitParadeResVital_JP",
            "W",
            0x00312DCC,
            "SUBCALL:0x00712F70",
        ),
        (
            "StallStartVital",
            "W",
            0x00369C36,
            "SUBCALL:0x00766C00",
        ),
    } or any(
        row.reason
        or not has_local_direction_proof(row)
        or not has_local_stream_proof(row)
        or "stack_identity_lea@" not in row.gate_condition
        for row in stack_identity_promoted_rows
    ):
        raise ExtractionError("stack identity LEA promotion mismatch")
    indirect_formal_rows = [
        row
        for row in rows
        if row.file_off_claim in (0x001E281E, 0x001E29B6)
    ]
    if (
        {
            (row.message, row.direction, row.file_off_claim)
            for row in indirect_formal_rows
        }
        != {
            (
                "CNSS_BoardcastToSpecifiedActorVtial",
                "W",
                0x001E281E,
            ),
            (
                "CNSS_BoardcastToAllActorVtial",
                "W",
                0x001E29B6,
            ),
        }
        or len(indirect_formal_rows) != 2
        or any(
            not row.tag.startswith("SUBCALL:INDIRECT(")
            or row.reason != "indirect_subserializer_target"
            or "indirect_direction_call@" not in row.gate_condition
            or "stack_neutral_vtable_getid@" not in row.gate_condition
            or "indirect_mode_formal_source " not in row.gate_condition
            for row in indirect_formal_rows
        )
        or any(
            row.reason == "indirect_serializer_direction_unresolved"
            for row in rows
        )
    ):
        raise ExtractionError(
            "indirect serializer formal-mode forwarding mismatch"
        )
    remaining_caller_mode_unknown = [
        row
        for row in rows
        if row.tag == "UNKNOWN"
        and "caller_mode_value_unproved" in row.reason
    ]
    if (
        len(remaining_caller_mode_unknown) != 4
        or {row.file_off_claim for row in remaining_caller_mode_unknown}
        != {0x001EE821, 0x0027313C}
    ):
        raise ExtractionError("caller mode fail-closed census mismatch")
    expected_constant_true_messages = {
        "AppraisalModule_Client",
        "ArenaModule_Client",
        "BasicModule_Client",
        "CGCGuildModule",
        "CPostProcessModule",
        "CSkillModule",
        "DropThingModule_Client",
        "EquipmentModule",
        "GatheringModule_Client",
        "GeneralUIHandleModule",
        "ItemSynthesisModule_Client",
        "ItemTransformModule_Client",
        "Module",
        "NewsflashModule_Client",
        "SceneObjectMovieModule",
        "SystemGiftModule_Client",
        "TotalCCULog_Module",
        "TreasureHuntModule_Client",
        "UI_MovieModule",
    }
    constant_true_marker = (
        "wire_empty_constant_true@0x00710440 file_off=0x0030F840 "
        "bytes=B001C20400 behavior=write_al_1_then_ret_4"
    )
    constant_true_rows = [
        row for row in rows if constant_true_marker in row.gate_condition
    ]
    if (
        len(constant_true_rows) != 38
        or {row.message for row in constant_true_rows}
        != expected_constant_true_messages
        or any(
            {row.direction for row in constant_true_rows if row.message == name}
            != {"W", "R"}
            or sum(row.message == name for row in constant_true_rows) != 2
            for name in expected_constant_true_messages
        )
        or any(
            row.order != 1
            or row.tag != "EMPTY"
            or row.field_offset != "N/A"
            or row.length != "0"
            or row.gate_condition != constant_true_marker
            or row.span_start != 0x00710440
            or row.span_end != 0x00710445
            or row.span_sha256
            != "f4c6d7ae520f88aecb3ea65952e885437fa4a6ce4b5c3439a161d1c5d8e42863"
            or row.file_off_claim != 0x0030F840
            or row.reason
            for row in constant_true_rows
        )
    ):
        raise ExtractionError("exact constant-true wire-empty census mismatch")
    expected_global_predicate_messages = {
        "AccuseModule_Client",
        "CastEquipmentModule_Client",
        "ChangeEquipLevelModule_Client",
        "ChannelModule_Client",
        "CollectionBookModule_Client",
        "DailyRewardModule_Client",
        "DyeingModule_Client",
        "GMModule_Client",
        "ItemMallModule_Client",
        "NPCTalkModule",
        "NPCVoiceModule",
        "PandoraBoxModule_Client",
        "PartyModule_Client",
        "PlayerSearchModule_Client",
        "SceneSoundEffectModule",
        "StorageModule_Client",
        "TradeModule_Client",
    }
    global_predicate_marker = (
        "wire_empty_global_predicate@0x00697870 file_off=0x00296C70 "
        "bytes=833DC42E0301000F95C0C20400 "
        "behavior=cmp_abs_global_zero_setne_al_ret_4"
    )
    global_predicate_rows = [
        row for row in rows if global_predicate_marker in row.gate_condition
    ]
    if (
        len(global_predicate_rows) != 34
        or {row.message for row in global_predicate_rows}
        != expected_global_predicate_messages
        or any(
            {
                row.direction
                for row in global_predicate_rows
                if row.message == name
            }
            != {"W", "R"}
            or sum(row.message == name for row in global_predicate_rows) != 2
            for name in expected_global_predicate_messages
        )
        or any(
            row.order != 1
            or row.tag != "EMPTY"
            or row.field_offset != "N/A"
            or row.length != "0"
            or row.gate_condition != global_predicate_marker
            or row.span_start != 0x00697870
            or row.span_end != 0x0069787D
            or row.span_sha256
            != "6e9524465aac2983dc71c539ae1b33311ff4b761bd7cbf412133aa9e714fe332"
            or row.file_off_claim != 0x00296C70
            or row.reason
            for row in global_predicate_rows
        )
    ):
        raise ExtractionError("exact global-predicate wire-empty census mismatch")
    expected_argument_copier_messages = {
        "ActorAttr",
        "ActorCommunityProperty",
        "ActorExpressData",
        "ActorLearnedPetsSkillData",
        "ActorMailData",
        "AvatarAttr",
        "BasicAttr",
        "CAchievementsAttr",
        "CBuffAttr",
        "CCooldownAttr",
        "CSkillAttr",
        "CollectableBookTypeAttr",
        "CollectionBookAttr",
        "CollectionEffectData",
        "CollectionObjPointAttr",
        "CollectionPieceAttr",
        "CrystalPlateAttr",
        "CrystalSlotAttr",
        "DBAttribute",
        "DailyActivityState",
        "DailyQuestAttr",
        "DailyRewardAttr",
        "DailyRewardBagAttr",
        "ExpressCountAttr",
        "InstanceRefreshAttr",
        "ItemAttr",
        "ItemMallGiftItem",
        "ItemVaryAttr",
        "MovementAttr",
        "NPCAppearAttr",
        "NPCAttr",
        "NavigationExAttr",
        "PetsData",
        "PetsMergingData",
        "QuestAttr",
        "QuestMiscAttr",
        "ResidentEffectAttr",
        "StallActorAttr",
        "SummonedPetAttr",
        "SystemGiftAttr",
        "UserSettingServer",
        "VowLockData",
        "WineCellarAttr",
        "WineFormulaLearningAttr",
        "WinePotAttr",
    }
    argument_copier_marker = (
        "wire_empty_argument_value_copier@0x0043BB80 "
        "file_off=0x0003AF80 "
        "bytes=8B4424048B54240889411889511CC20800 "
        "behavior=load_entry_arg_4_8_store_this_18_1C_ret_8"
    )
    argument_copier_rows = [
        row for row in rows if argument_copier_marker in row.gate_condition
    ]
    if (
        len(argument_copier_rows) != 90
        or {row.message for row in argument_copier_rows}
        != expected_argument_copier_messages
        or any(
            {
                row.direction
                for row in argument_copier_rows
                if row.message == name
            }
            != {"W", "R"}
            or sum(row.message == name for row in argument_copier_rows) != 2
            for name in expected_argument_copier_messages
        )
        or any(
            row.order != 1
            or row.tag != "EMPTY"
            or row.field_offset != "N/A"
            or row.length != "0"
            or row.gate_condition != argument_copier_marker
            or row.span_start != 0x0043BB80
            or row.span_end != 0x0043BB91
            or row.span_sha256
            != "b625098be0bbf3e36927c8dce2ccf3cf171563fc8f1465a41039974b332c19c0"
            or row.file_off_claim != 0x0003AF80
            or row.reason
            for row in argument_copier_rows
        )
    ):
        raise ExtractionError("exact argument-copier wire-empty census mismatch")
    single_argument_copier_marker = (
        "wire_empty_single_argument_value_copier@0x008C5AE0 "
        "file_off=0x004C4EE0 bytes=8B442404894114C20400 "
        "behavior=load_entry_arg_4_store_this_14_ret_4"
    )
    single_argument_copier_rows = [
        row
        for row in rows
        if single_argument_copier_marker in row.gate_condition
    ]
    if (
        len(single_argument_copier_rows) != 2
        or {row.message for row in single_argument_copier_rows}
        != {"PcThreadRunObject"}
        or {row.direction for row in single_argument_copier_rows}
        != {"W", "R"}
        or any(
            row.order != 1
            or row.tag != "EMPTY"
            or row.field_offset != "N/A"
            or row.length != "0"
            or row.gate_condition != single_argument_copier_marker
            or row.span_start != 0x008C5AE0
            or row.span_end != 0x008C5AEA
            or row.span_sha256
            != "5940df69b60defd9e87bf6c4f1f44706b7d3bc501eab25edf30198be533ee258"
            or row.file_off_claim != 0x004C4EE0
            or row.reason
            for row in single_argument_copier_rows
        )
    ):
        raise ExtractionError(
            "exact single-argument-copier wire-empty census mismatch"
        )
    conditional_object_init_marker = (
        "wire_empty_conditional_object_init@0x006BE320 "
        "file_off=0x002BD720 "
        "bytes=33C03905C42E0301750532C0C20400"
        "89415889415CB001C20400 "
        "behavior=cmp_abs_global_false_or_store_this_58_5C_true_ret_4"
    )
    conditional_object_init_rows = [
        row
        for row in rows
        if conditional_object_init_marker in row.gate_condition
    ]
    if (
        len(conditional_object_init_rows) != 2
        or {row.message for row in conditional_object_init_rows}
        != {"BlackMarketModule_Client"}
        or {row.direction for row in conditional_object_init_rows}
        != {"W", "R"}
        or any(
            row.order != 1
            or row.tag != "EMPTY"
            or row.field_offset != "N/A"
            or row.length != "0"
            or row.gate_condition != conditional_object_init_marker
            or row.span_start != 0x006BE320
            or row.span_end != 0x006BE33A
            or row.span_sha256
            != "c1d31eeef606f03f6523054b76d39576fad461ef8898ba4413011064057a88b2"
            or row.file_off_claim != 0x002BD720
            or row.reason
            for row in conditional_object_init_rows
        )
    ):
        raise ExtractionError(
            "exact conditional-object-init wire-empty census mismatch"
        )
    fpstest_entry_marker = (
        "wire_empty_fpstest_entry@0x0073E8B0 file_off=0x0033DCB0 "
        "full_span_sha256="
        "3f2bc513f207f3db6264f7305f2d46a298a93b34683aa78dc8f19d057cdb22e3 "
        "reachable_prefix_end=0x0073E8FE reachable_prefix_sha256="
        "1af255ab1fc762a99929747ae18351f35f50623cfc3124c69fe9b9126eb23897 "
        "separator_file_off=0x0033DCFE bytes=CCCC "
        "suffix_entry=0x0073E900 suffix_unreachable_from_entry "
        "behavior=entry_reachable_paths_no_wire_field_suffix_unclaimed"
    )
    fpstest_entry_rows = [
        row for row in rows if fpstest_entry_marker in row.gate_condition
    ]
    if (
        len(fpstest_entry_rows) != 2
        or {row.message for row in fpstest_entry_rows}
        != {"FPSTestModule_Client"}
        or {row.direction for row in fpstest_entry_rows} != {"W", "R"}
        or any(
            row.order != 1
            or row.tag != "EMPTY"
            or row.field_offset != "N/A"
            or row.length != "0"
            or row.gate_condition != fpstest_entry_marker
            or row.span_start != 0x0073E8B0
            or row.span_end != 0x0073E94C
            or row.span_sha256
            != "3f2bc513f207f3db6264f7305f2d46a298a93b34683aa78dc8f19d057cdb22e3"
            or row.file_off_claim != 0x0033DCB0
            or row.reason
            for row in fpstest_entry_rows
        )
    ):
        raise ExtractionError("exact FPSTest entry wire-empty census mismatch")
    if (
        len(rows) != 6931
        or sum(bool(re.fullmatch(r"0x[0-9A-F]{2}", row.tag)) for row in rows)
        != 2783
        or sum(row.tag == "UNKNOWN" for row in rows) != 50
    ):
        raise ExtractionError("A2 row census mismatch")


def validate_analysis(
    image: Image,
    registry: list[RegistryRow],
    analyzer: SerializerAnalyzer,
    rows: list[FieldRow],
) -> None:
    """Fail closed if emitted evidence loses a measured call or span invariant."""
    constant_true_span = analyzer.span(0x00710440)
    constant_true_roots = {
        row.name for row in registry if row.serializer_va == 0x00710440
    }
    if (
        constant_true_span is None
        or (
            constant_true_span.start_va,
            constant_true_span.end_va,
            constant_true_span.start_off,
            constant_true_span.end_off,
            constant_true_span.sha256,
        )
        != (
            0x00710440,
            0x00710445,
            0x0030F840,
            0x0030F845,
            "f4c6d7ae520f88aecb3ea65952e885437fa4a6ce4b5c3439a161d1c5d8e42863",
        )
        or image.data[0x0030F840:0x0030F845] != b"\xb0\x01\xc2\x04\x00"
        or constant_true_roots
        != {
            "AppraisalModule_Client",
            "ArenaModule_Client",
            "BasicModule_Client",
            "CGCGuildModule",
            "CPostProcessModule",
            "CSkillModule",
            "DropThingModule_Client",
            "EquipmentModule",
            "GatheringModule_Client",
            "GeneralUIHandleModule",
            "ItemSynthesisModule_Client",
            "ItemTransformModule_Client",
            "Module",
            "NewsflashModule_Client",
            "SceneObjectMovieModule",
            "SystemGiftModule_Client",
            "TotalCCULog_Module",
            "TreasureHuntModule_Client",
            "UI_MovieModule",
        }
    ):
        raise ExtractionError("exact constant-true wire-empty proof mismatch")
    global_predicate_span = analyzer.span(0x00697870)
    global_predicate_roots = {
        row.name for row in registry if row.serializer_va == 0x00697870
    }
    if (
        global_predicate_span is None
        or (
            global_predicate_span.start_va,
            global_predicate_span.end_va,
            global_predicate_span.start_off,
            global_predicate_span.end_off,
            global_predicate_span.sha256,
        )
        != (
            0x00697870,
            0x0069787D,
            0x00296C70,
            0x00296C7D,
            "6e9524465aac2983dc71c539ae1b33311ff4b761bd7cbf412133aa9e714fe332",
        )
        or image.data[0x00296C70:0x00296C7D]
        != b"\x83\x3d\xc4\x2e\x03\x01\x00\x0f\x95\xc0\xc2\x04\x00"
        or global_predicate_roots
        != {
            "AccuseModule_Client",
            "CastEquipmentModule_Client",
            "ChangeEquipLevelModule_Client",
            "ChannelModule_Client",
            "CollectionBookModule_Client",
            "DailyRewardModule_Client",
            "DyeingModule_Client",
            "GMModule_Client",
            "ItemMallModule_Client",
            "NPCTalkModule",
            "NPCVoiceModule",
            "PandoraBoxModule_Client",
            "PartyModule_Client",
            "PlayerSearchModule_Client",
            "SceneSoundEffectModule",
            "StorageModule_Client",
            "TradeModule_Client",
        }
    ):
        raise ExtractionError("exact global-predicate wire-empty proof mismatch")
    argument_copier_span = analyzer.span(0x0043BB80)
    argument_copier_roots = {
        row.name for row in registry if row.serializer_va == 0x0043BB80
    }
    if (
        argument_copier_span is None
        or (
            argument_copier_span.start_va,
            argument_copier_span.end_va,
            argument_copier_span.start_off,
            argument_copier_span.end_off,
            argument_copier_span.sha256,
        )
        != (
            0x0043BB80,
            0x0043BB91,
            0x0003AF80,
            0x0003AF91,
            "b625098be0bbf3e36927c8dce2ccf3cf171563fc8f1465a41039974b332c19c0",
        )
        or image.data[0x0003AF80:0x0003AF91]
        != (
            b"\x8b\x44\x24\x04\x8b\x54\x24\x08\x89\x41\x18"
            b"\x89\x51\x1c\xc2\x08\x00"
        )
        or argument_copier_roots
        != {
            "ActorAttr",
            "ActorCommunityProperty",
            "ActorExpressData",
            "ActorLearnedPetsSkillData",
            "ActorMailData",
            "AvatarAttr",
            "BasicAttr",
            "CAchievementsAttr",
            "CBuffAttr",
            "CCooldownAttr",
            "CSkillAttr",
            "CollectableBookTypeAttr",
            "CollectionBookAttr",
            "CollectionEffectData",
            "CollectionObjPointAttr",
            "CollectionPieceAttr",
            "CrystalPlateAttr",
            "CrystalSlotAttr",
            "DBAttribute",
            "DailyActivityState",
            "DailyQuestAttr",
            "DailyRewardAttr",
            "DailyRewardBagAttr",
            "ExpressCountAttr",
            "InstanceRefreshAttr",
            "ItemAttr",
            "ItemMallGiftItem",
            "ItemVaryAttr",
            "MovementAttr",
            "NPCAppearAttr",
            "NPCAttr",
            "NavigationExAttr",
            "PetsData",
            "PetsMergingData",
            "QuestAttr",
            "QuestMiscAttr",
            "ResidentEffectAttr",
            "StallActorAttr",
            "SummonedPetAttr",
            "SystemGiftAttr",
            "UserSettingServer",
            "VowLockData",
            "WineCellarAttr",
            "WineFormulaLearningAttr",
            "WinePotAttr",
        }
    ):
        raise ExtractionError("exact argument-copier wire-empty proof mismatch")
    single_argument_copier_span = analyzer.span(0x008C5AE0)
    single_argument_copier_roots = {
        row.name for row in registry if row.serializer_va == 0x008C5AE0
    }
    if (
        single_argument_copier_span is None
        or (
            single_argument_copier_span.start_va,
            single_argument_copier_span.end_va,
            single_argument_copier_span.start_off,
            single_argument_copier_span.end_off,
            single_argument_copier_span.sha256,
        )
        != (
            0x008C5AE0,
            0x008C5AEA,
            0x004C4EE0,
            0x004C4EEA,
            "5940df69b60defd9e87bf6c4f1f44706b7d3bc501eab25edf30198be533ee258",
        )
        or image.data[0x004C4EE0:0x004C4EEA]
        != b"\x8b\x44\x24\x04\x89\x41\x14\xc2\x04\x00"
        or single_argument_copier_roots != {"PcThreadRunObject"}
    ):
        raise ExtractionError(
            "exact single-argument-copier wire-empty proof mismatch"
        )
    conditional_object_init_span = analyzer.span(0x006BE320)
    conditional_object_init_roots = {
        row.name for row in registry if row.serializer_va == 0x006BE320
    }
    if (
        conditional_object_init_span is None
        or (
            conditional_object_init_span.start_va,
            conditional_object_init_span.end_va,
            conditional_object_init_span.start_off,
            conditional_object_init_span.end_off,
            conditional_object_init_span.sha256,
        )
        != (
            0x006BE320,
            0x006BE33A,
            0x002BD720,
            0x002BD73A,
            "c1d31eeef606f03f6523054b76d39576fad461ef8898ba4413011064057a88b2",
        )
        or image.data[0x002BD720:0x002BD73A]
        != (
            b"\x33\xc0\x39\x05\xc4\x2e\x03\x01\x75\x05\x32\xc0"
            b"\xc2\x04\x00\x89\x41\x58\x89\x41\x5c\xb0\x01\xc2\x04\x00"
        )
        or conditional_object_init_roots != {"BlackMarketModule_Client"}
    ):
        raise ExtractionError(
            "exact conditional-object-init wire-empty proof mismatch"
        )
    fpstest_entry_span = analyzer.span(0x0073E8B0)
    fpstest_entry_decode = analyzer.decode(0x0073E8B0)
    fpstest_entry_roots = {
        row.name for row in registry if row.serializer_va == 0x0073E8B0
    }
    expected_fpstest_entry_cfg = {
        0x0073E8B0: ("xor", (0x0073E8B2,), None, None),
        0x0073E8B2: ("other", (0x0073E8B8,), None, None),
        0x0073E8B8: (
            "jcc",
            (0x0073E8BA, 0x0073E8BF),
            0x0073E8BF,
            None,
        ),
        0x0073E8BA: ("xor", (0x0073E8BC,), None, None),
        0x0073E8BC: ("ret", (), None, 4),
        0x0073E8BF: ("mov", (0x0073E8C1,), None, None),
        0x0073E8C1: ("mov", (0x0073E8C4,), None, None),
        0x0073E8C4: ("mov", (0x0073E8C7,), None, None),
        0x0073E8C7: ("mov", (0x0073E8CA,), None, None),
        0x0073E8CA: ("push", (0x0073E8CB,), None, None),
        0x0073E8CB: ("mov", (0x0073E8D1,), None, None),
        0x0073E8D1: ("mov", (0x0073E8D4,), None, None),
        0x0073E8D4: ("other", (0x0073E8DA,), None, None),
        0x0073E8DA: (
            "jcc",
            (0x0073E8DC, 0x0073E8FA),
            0x0073E8FA,
            None,
        ),
        0x0073E8DC: ("mov", (0x0073E8E1,), None, None),
        0x0073E8E1: ("other", (0x0073E8E7,), None, None),
        0x0073E8E7: (
            "jcc",
            (0x0073E8E9, 0x0073E8FA),
            0x0073E8FA,
            None,
        ),
        0x0073E8E9: ("other", (0x0073E8EF,), None, None),
        0x0073E8EF: (
            "jcc",
            (0x0073E8F1, 0x0073E8FA),
            0x0073E8FA,
            None,
        ),
        0x0073E8F1: ("mov", (0x0073E8F4,), None, None),
        0x0073E8F4: ("mov", (0x0073E8F7,), None, None),
        0x0073E8F7: ("mov", (0x0073E8FA,), None, None),
        0x0073E8FA: ("pop", (0x0073E8FB,), None, None),
        0x0073E8FB: ("ret", (), None, 4),
    }
    measured_fpstest_entry_cfg = (
        {}
        if fpstest_entry_decode is None
        else {
            va: (
                ins.kind,
                fpstest_entry_decode.successors.get(va, ()),
                ins.target,
                ins.imm,
            )
            for va, ins in fpstest_entry_decode.instructions.items()
        }
    )
    fpstest_stack_memory = (
        []
        if fpstest_entry_decode is None
        else [
            (ins.va, operand.base)
            for ins in fpstest_entry_decode.instructions.values()
            for operand in (ins.dst, ins.src)
            if operand is not None
            and operand.kind == "mem"
            and base_reg_name(operand.base) in {"esp", "ebp"}
        ]
    )
    if (
        fpstest_entry_span is None
        or fpstest_entry_decode is None
        or (
            fpstest_entry_span.start_va,
            fpstest_entry_span.end_va,
            fpstest_entry_span.start_off,
            fpstest_entry_span.end_off,
            fpstest_entry_span.sha256,
        )
        != (
            0x0073E8B0,
            0x0073E94C,
            0x0033DCB0,
            0x0033DD4C,
            "3f2bc513f207f3db6264f7305f2d46a298a93b34683aa78dc8f19d057cdb22e3",
        )
        or not analyzer._exact_fpstest_entry_wire_empty(
            image, fpstest_entry_span
        )
        or hashlib.sha256(image.data[0x0033DCB0:0x0033DCFE]).hexdigest()
        != "1af255ab1fc762a99929747ae18351f35f50623cfc3124c69fe9b9126eb23897"
        or image.data[0x0033DCFE:0x0033DD00] != b"\xCC\xCC"
        or fpstest_entry_decode.errors
        or measured_fpstest_entry_cfg != expected_fpstest_entry_cfg
        or any(
            ins.kind in {"call", "call_indirect", "jmp", "jmp_indirect"}
            for ins in fpstest_entry_decode.instructions.values()
        )
        or fpstest_stack_memory
        or any(
            ins.va >= 0x0073E8FE or ins.next_va > 0x0073E8FE
            for ins in fpstest_entry_decode.instructions.values()
        )
        or any(
            successor >= 0x0073E8FE
            for successors in fpstest_entry_decode.successors.values()
            for successor in successors
        )
        or fpstest_entry_roots != {"FPSTestModule_Client"}
    ):
        raise ExtractionError("exact FPSTest entry wire-empty proof mismatch")
    synthetic_plain_mov = Instruction(
        va=0,
        off=0,
        size=2,
        raw=b"\x8B\xEC",
        kind="mov",
        dst=Operand("reg", reg="ebp"),
        src=Operand("reg", reg="esp"),
    )
    synthetic_narrow_moves = tuple(
        Instruction(
            va=0,
            off=0,
            size=3,
            raw=raw,
            kind="mov",
            dst=Operand("reg", reg="ebp"),
            src=Operand("reg", reg="esp"),
        )
        for raw in (
            b"\x0F\xB6\xEC",
            b"\x0F\xB7\xEC",
            b"\x0F\xBE\xEC",
            b"\x0F\xBF\xEC",
            b"\x66\x8B\xEC",
            b"\x8A\xEC",
        )
    )
    if (
        not analyzer._is_full_width_plain_mov(synthetic_plain_mov)
        or any(
            analyzer._is_full_width_plain_mov(ins)
            for ins in synthetic_narrow_moves
        )
    ):
        raise ExtractionError("full-width plain MOV policy regression")
    synthetic_iat_va = 0x00C3B4C0
    synthetic_iat_load = Instruction(
        va=0x8000,
        off=0,
        size=6,
        raw=b"\x8B\x2D\xC0\xB4\xC3\x00",
        kind="mov",
        dst=Operand("reg", reg="ebp"),
        src=Operand("mem", absolute=synthetic_iat_va),
    )
    synthetic_register_call = Instruction(
        va=0x8006,
        off=6,
        size=2,
        raw=b"\xFF\xD5",
        kind="call_indirect",
        src=Operand("reg", reg="ebp"),
    )
    synthetic_register_import_decode = FunctionDecode(
        FunctionSpan(0x8000, 0x8008, 0, 8, ""),
        {
            synthetic_iat_load.va: synthetic_iat_load,
            synthetic_register_call.va: synthetic_register_call,
        },
        {
            synthetic_iat_load.va: (synthetic_register_call.va,),
            synthetic_register_call.va: (),
        },
        {
            synthetic_iat_load.va: (),
            synthetic_register_call.va: (synthetic_iat_load.va,),
        },
        (),
    )
    synthetic_register_import_analyzer = SerializerAnalyzer(image, [])
    synthetic_register_import_analyzer.decode_cache[0x8000] = (
        synthetic_register_import_decode
    )
    synthetic_register_import_proof = (
        synthetic_register_import_analyzer._stack_neutral_register_import(
            0x8000, synthetic_register_call
        )
    )
    if (
        synthetic_register_import_proof is None
        or synthetic_register_import_proof[0]
        != image.imports_by_iat[synthetic_iat_va]
        or synthetic_register_import_proof[1:] != ("ebp", 0x8000)
        or synthetic_register_import_analyzer._stack_after(
            0x8000, 12, synthetic_register_call
        )
        != 12
    ):
        raise ExtractionError("register-indirect IAT proof regression")
    synthetic_bad_iat_loads = (
        Instruction(
            0x8000,
            0,
            7,
            b"\x66\x8B\x2D\xC0\xB4\xC3\x00",
            "mov",
            dst=Operand("reg", reg="ebp"),
            src=Operand("mem", absolute=synthetic_iat_va),
        ),
        Instruction(
            0x8000,
            0,
            3,
            b"\x8B\x68\x04",
            "mov",
            dst=Operand("reg", reg="ebp"),
            src=Operand("mem", base="eax", disp=4),
        ),
        Instruction(
            0x8000,
            0,
            6,
            b"\x8B\x35\xC0\xB4\xC3\x00",
            "mov",
            dst=Operand("reg", reg="ebp"),
            src=Operand("mem", absolute=synthetic_iat_va),
        ),
    )
    synthetic_bad_register_calls = (
        Instruction(
            0x8006,
            6,
            3,
            b"\x66\xFF\xD5",
            "call_indirect",
            src=Operand("reg", reg="ebp"),
        ),
        Instruction(
            0x8006,
            6,
            2,
            b"\xFF\xD4",
            "call_indirect",
            src=Operand("reg", reg="esp"),
        ),
        Instruction(
            0x8006,
            6,
            2,
            b"\xFF\xD6",
            "call_indirect",
            src=Operand("reg", reg="ebp"),
        ),
    )
    if (
        not analyzer._is_exact_iat_register_load(
            synthetic_iat_load, "ebp", synthetic_iat_va
        )
        or not analyzer._is_exact_register_indirect_call(
            synthetic_register_call, "ebp"
        )
        or any(
            analyzer._is_exact_iat_register_load(
                item, "ebp", synthetic_iat_va
            )
            for item in synthetic_bad_iat_loads
        )
        or any(
            analyzer._is_exact_register_indirect_call(item, item.src.reg)
            for item in synthetic_bad_register_calls
        )
    ):
        raise ExtractionError("exact register-indirect IAT policy regression")
    synthetic_undefined_decode = FunctionDecode(
        FunctionSpan(0x8000, 0x8008, 0, 8, ""),
        synthetic_register_import_decode.instructions,
        {
            synthetic_iat_load.va: (synthetic_register_call.va,),
            synthetic_register_call.va: (),
        },
        {
            synthetic_iat_load.va: (),
            synthetic_register_call.va: (
                synthetic_iat_load.va,
                synthetic_register_import_decode.span.start_va,
            ),
        },
        (),
    )
    synthetic_undefined_analyzer = SerializerAnalyzer(image, [])
    synthetic_undefined_analyzer.decode_cache[0x8000] = synthetic_undefined_decode
    synthetic_undefined_analyzer.reaching_definition_cache[(0x8000, "ebp")] = {
        synthetic_register_call.va: frozenset((None, synthetic_iat_load.va))
    }
    if (
        synthetic_undefined_analyzer._stack_neutral_register_import(
            0x8000, synthetic_register_call
        )
        is not None
        or synthetic_undefined_analyzer._stack_after(
            0x8000, 12, synthetic_register_call
        )
        is not None
    ):
        raise ExtractionError(
            "undefined register-indirect IAT path did not fail closed"
        )
    synthetic_vtable_load = Instruction(
        va=0x8100,
        off=0,
        size=2,
        raw=b"\x8B\x01",
        kind="mov",
        dst=Operand("reg", reg="eax"),
        src=Operand("mem", base="ecx"),
    )
    synthetic_getid_load = Instruction(
        va=0x8102,
        off=2,
        size=3,
        raw=b"\x8B\x50\x10",
        kind="mov",
        dst=Operand("reg", reg="edx"),
        src=Operand("mem", base="eax", disp=0x10),
    )
    synthetic_getid_call = Instruction(
        va=0x8105,
        off=5,
        size=2,
        raw=b"\xFF\xD2",
        kind="call_indirect",
        src=Operand("reg", reg="edx"),
    )
    synthetic_getid_decode = FunctionDecode(
        FunctionSpan(0x8100, 0x8107, 0, 7, ""),
        {
            synthetic_vtable_load.va: synthetic_vtable_load,
            synthetic_getid_load.va: synthetic_getid_load,
            synthetic_getid_call.va: synthetic_getid_call,
        },
        {
            synthetic_vtable_load.va: (synthetic_getid_load.va,),
            synthetic_getid_load.va: (synthetic_getid_call.va,),
            synthetic_getid_call.va: (),
        },
        {
            synthetic_vtable_load.va: (),
            synthetic_getid_load.va: (synthetic_vtable_load.va,),
            synthetic_getid_call.va: (synthetic_getid_load.va,),
        },
        (),
    )
    synthetic_getid_analyzer = SerializerAnalyzer(image, [])
    synthetic_getid_analyzer.decode_cache[0x8100] = synthetic_getid_decode
    synthetic_bad_getid_loads = (
        Instruction(
            0x8102,
            2,
            3,
            b"\x8B\x50\x18",
            "mov",
            dst=Operand("reg", reg="edx"),
            src=Operand("mem", base="eax", disp=0x18),
        ),
        Instruction(
            0x8102,
            2,
            4,
            b"\x66\x8B\x50\x10",
            "mov",
            dst=Operand("reg", reg="edx"),
            src=Operand("mem", base="eax", disp=0x10),
        ),
        Instruction(
            0x8102,
            2,
            4,
            b"\x8B\x54\x08\x10",
            "mov",
            dst=Operand("reg", reg="edx"),
            src=Operand(
                "mem", base="eax", index="ecx", disp=0x10
            ),
        ),
    )
    getid_proof = synthetic_getid_analyzer._stack_neutral_vtable_getid(
        0x8100, synthetic_getid_call
    )
    synthetic_undefined_getid = SerializerAnalyzer(image, [])
    synthetic_undefined_getid.decode_cache[0x8100] = synthetic_getid_decode
    synthetic_undefined_getid.reaching_definition_cache[(0x8100, "edx")] = {
        synthetic_getid_call.va: frozenset((None, synthetic_getid_load.va))
    }
    if (
        getid_proof != ("edx", synthetic_getid_load.va)
        or not analyzer._is_exact_vtable_slot_register_load(
            synthetic_getid_load, "edx", 0x10
        )
        or any(
            analyzer._is_exact_vtable_slot_register_load(
                item, "edx", 0x10
            )
            for item in synthetic_bad_getid_loads
        )
        or synthetic_getid_analyzer._stack_after(
            0x8100, 12, synthetic_getid_call
        )
        != 12
        or synthetic_getid_analyzer._stack_after(
            0x8100, None, synthetic_getid_call
        )
        is not None
        or synthetic_undefined_getid._stack_neutral_vtable_getid(
            0x8100, synthetic_getid_call
        )
        is not None
    ):
        raise ExtractionError("exact GetId vtable stack policy regression")
    synthetic_identity_lea = Instruction(
        va=4,
        off=4,
        size=6,
        raw=b"\x8D\x9B\x00\x00\x00\x00",
        kind="lea",
        dst=Operand("reg", reg="ebx"),
        src=Operand("mem", base="ebx", disp=0),
    )
    synthetic_nonidentity_leas = (
        Instruction(
            4,
            4,
            7,
            b"\x66\x8D\x9B\x00\x00\x00\x00",
            "lea",
            dst=Operand("reg", reg="ebx"),
            src=Operand("mem", base="ebx", disp=0),
        ),
        Instruction(
            4,
            4,
            7,
            b"\x67\x8D\x9B\x00\x00\x00\x00",
            "lea",
            dst=Operand("reg", reg="ebx"),
            src=Operand("mem", base="ebx", disp=0),
        ),
        Instruction(
            4,
            4,
            3,
            b"\x8D\x5B\x01",
            "lea",
            dst=Operand("reg", reg="ebx"),
            src=Operand("mem", base="ebx", disp=1),
        ),
        Instruction(
            4,
            4,
            3,
            b"\x8D\x1C\x03",
            "lea",
            dst=Operand("reg", reg="ebx"),
            src=Operand("mem", base="ebx", index="eax", disp=0),
        ),
    )
    if (
        not analyzer._is_full_width_identity_lea(synthetic_identity_lea)
        or any(
            analyzer._is_full_width_identity_lea(ins)
            for ins in synthetic_nonidentity_leas
        )
    ):
        raise ExtractionError("full-width identity LEA policy regression")
    synthetic_stack_identity = Instruction(
        va=0x9000,
        off=0,
        size=7,
        raw=b"\x8D\xA4\x24\x00\x00\x00\x00",
        kind="lea",
        dst=Operand("reg", reg="esp"),
        src=Operand("mem", base="esp", disp=0),
    )
    synthetic_non_stack_identities = (
        Instruction(
            0x9000,
            0,
            8,
            b"\x66\x8D\xA4\x24\x00\x00\x00\x00",
            "lea",
            dst=Operand("reg", reg="esp"),
            src=Operand("mem", base="esp", disp=0),
        ),
        Instruction(
            0x9000,
            0,
            7,
            b"\x8D\xA4\x24\x04\x00\x00\x00",
            "lea",
            dst=Operand("reg", reg="esp"),
            src=Operand("mem", base="esp", disp=4),
        ),
        Instruction(
            0x9000,
            0,
            7,
            b"\x8D\xAC\x24\x00\x00\x00\x00",
            "lea",
            dst=Operand("reg", reg="ebp"),
            src=Operand("mem", base="esp", disp=0),
        ),
        Instruction(
            0x9000,
            0,
            7,
            b"\x8D\xA4\x04\x00\x00\x00\x00",
            "lea",
            dst=Operand("reg", reg="esp"),
            src=Operand("mem", base="esp", index="eax", disp=0),
        ),
    )
    if (
        not analyzer._is_exact_stack_identity_lea(synthetic_stack_identity)
        or any(
            analyzer._is_exact_stack_identity_lea(ins)
            for ins in synthetic_non_stack_identities
        )
        or analyzer._stack_after(0x9000, 12, synthetic_stack_identity)
        != 12
        or analyzer._stack_after(0x9000, None, synthetic_stack_identity)
        is not None
    ):
        raise ExtractionError("exact stack identity LEA policy regression")
    synthetic_formal_seed = Instruction(
        va=0,
        off=0,
        size=4,
        raw=b"\x8B\x5C\x24\x04",
        kind="mov",
        dst=Operand("reg", reg="ebx"),
        src=Operand("mem", base="esp", disp=4),
    )
    synthetic_identity_use = Instruction(
        va=synthetic_identity_lea.next_va,
        off=synthetic_identity_lea.next_va,
        size=1,
        raw=b"\x90",
        kind="other",
    )
    synthetic_identity_decode = FunctionDecode(
        span=FunctionSpan(0, 11, 0, 11, ""),
        instructions={
            0: synthetic_formal_seed,
            synthetic_identity_lea.va: synthetic_identity_lea,
            synthetic_identity_use.va: synthetic_identity_use,
        },
        successors={
            0: (synthetic_identity_lea.va,),
            synthetic_identity_lea.va: (synthetic_identity_use.va,),
            synthetic_identity_use.va: (),
        },
        predecessors={
            0: (),
            synthetic_identity_lea.va: (0,),
            synthetic_identity_use.va: (synthetic_identity_lea.va,),
        },
        errors=(),
    )
    if analyzer._formal_offsets_for_reg(
        synthetic_identity_decode,
        {site: frozenset((0,)) for site in synthetic_identity_decode.instructions},
        synthetic_identity_use.va,
        "ebx",
        {},
        frozenset(),
    ) != frozenset((4,)):
        raise ExtractionError("identity LEA failed to preserve a formal")
    synthetic_identity_analyzer = SerializerAnalyzer(image, [])
    synthetic_identity_analyzer.decode_cache[0] = synthetic_identity_decode
    identity_byte_origins, identity_byte_proofs = (
        synthetic_identity_analyzer._mode_argument_formal_offsets_with_reaching_proof(
            0,
            synthetic_identity_use.va,
            Operand("reg", reg="ebx"),
            1,
        )
    )
    identity_proof_key = (0, synthetic_identity_use.va, "ebx")
    if (
        identity_byte_origins != frozenset((4,))
        or identity_byte_proofs != (identity_proof_key,)
        or synthetic_identity_analyzer.formal_reaching_definitions.get(
            identity_proof_key
        )
        != synthetic_identity_lea.va
        or synthetic_identity_analyzer.formal_reaching_basis.get(
            identity_proof_key
        )
        != "full_width_identity_lea"
    ):
        raise ExtractionError("byte consumer lost full-GPR identity proof")
    synthetic_narrow = synthetic_narrow_moves[0]
    synthetic_use = Instruction(
        va=synthetic_narrow.next_va,
        off=synthetic_narrow.next_va,
        size=1,
        raw=b"\x90",
        kind="other",
    )
    synthetic_decode = FunctionDecode(
        span=FunctionSpan(0, synthetic_use.next_va, 0, synthetic_use.next_va, ""),
        instructions={0: synthetic_narrow, synthetic_use.va: synthetic_use},
        successors={0: (synthetic_use.va,), synthetic_use.va: ()},
        predecessors={0: (), synthetic_use.va: (0,)},
        errors=(),
    )
    if analyzer._stack_base_offsets_for_reg(
        synthetic_decode,
        {0: frozenset((4,)), synthetic_use.va: frozenset((4,))},
        synthetic_use.va,
        "ebp",
        {},
        frozenset(),
    ):
        raise ExtractionError("narrow MOV fabricated a stack formal base")
    synthetic_safe_other = Instruction(
        va=0,
        off=0,
        size=2,
        raw=b"\x3B\xCF",
        kind="other",
    )
    synthetic_unsafe_others = (
        Instruction(0, 0, 2, b"\x87\xD8", "other"),
        Instruction(0, 0, 2, b"\x0F\xC8", "other"),
        Instruction(0, 0, 2, b"\xDF\xE0", "other"),
    )
    if (
        analyzer._writes_register_for_reaching(
            synthetic_safe_other, "ebp"
        )
        or any(
            not analyzer._writes_register_for_reaching(ins, "ebp")
            for ins in synthetic_unsafe_others
        )
    ):
        raise ExtractionError("opaque reaching-definition clobber regression")

    def synthetic_byte_trace(
        decoded: FunctionDecode, use_va: int, lane: str = "bl"
    ) -> tuple[
        frozenset[int],
        dict[int, frozenset[int | None]],
        SerializerAnalyzer,
    ]:
        synthetic_analyzer = SerializerAnalyzer(image, [])
        function_va = decoded.span.start_va
        synthetic_analyzer.decode_cache[function_va] = decoded
        depths = {
            site: frozenset((0,)) for site in decoded.instructions
        }
        synthetic_analyzer.stack_depth_cache[function_va] = depths
        origins = synthetic_analyzer._formal_offsets_for_byte_reg(
            decoded,
            depths,
            use_va,
            lane,
            {},
            frozenset(),
        )
        definitions = synthetic_analyzer._byte_reaching_definitions(
            function_va, lane
        )
        return origins, definitions, synthetic_analyzer

    loop_seed = Instruction(
        0x1000,
        0,
        4,
        b"\x8B\x5C\x24\x04",
        "mov",
        dst=Operand("reg", reg="ebx"),
        src=Operand("mem", base="esp", disp=4),
    )
    loop_head = Instruction(0x1004, 4, 2, b"\x85\xC0", "test")
    loop_back = Instruction(0x1006, 6, 2, b"\x75\xFC", "jcc")
    loop_use = Instruction(0x1008, 8, 1, b"\x53", "push")
    loop_decode = FunctionDecode(
        FunctionSpan(0x1000, 0x1009, 0, 9, ""),
        {
            loop_seed.va: loop_seed,
            loop_head.va: loop_head,
            loop_back.va: loop_back,
            loop_use.va: loop_use,
        },
        {
            loop_seed.va: (loop_head.va,),
            loop_head.va: (loop_back.va, loop_use.va),
            loop_back.va: (loop_head.va,),
            loop_use.va: (),
        },
        {
            loop_seed.va: (),
            loop_head.va: (loop_seed.va, loop_back.va),
            loop_back.va: (loop_head.va,),
            loop_use.va: (loop_head.va,),
        },
        (),
    )
    loop_origins, loop_definitions, loop_analyzer = synthetic_byte_trace(
        loop_decode, loop_use.va
    )
    if (
        loop_origins != frozenset((4,))
        or loop_definitions.get(loop_use.va) != frozenset((loop_seed.va,))
        or set(loop_analyzer.formal_reaching_definitions.values())
        != {loop_seed.va}
        or set(loop_analyzer.formal_reaching_basis.values())
        != {"unique_byte_lane_reaching_definition"}
    ):
        raise ExtractionError("byte-lane one-definition loop regression")

    undefined_entry = Instruction(0x2000, 0, 2, b"\x74\x04", "jcc")
    undefined_seed = Instruction(
        0x2002,
        2,
        4,
        b"\x8B\x5C\x24\x04",
        "mov",
        dst=Operand("reg", reg="ebx"),
        src=Operand("mem", base="esp", disp=4),
    )
    undefined_use = Instruction(0x2006, 6, 1, b"\x53", "push")
    undefined_decode = FunctionDecode(
        FunctionSpan(0x2000, 0x2007, 0, 7, ""),
        {
            undefined_entry.va: undefined_entry,
            undefined_seed.va: undefined_seed,
            undefined_use.va: undefined_use,
        },
        {
            undefined_entry.va: (undefined_seed.va, undefined_use.va),
            undefined_seed.va: (undefined_use.va,),
            undefined_use.va: (),
        },
        {
            undefined_entry.va: (),
            undefined_seed.va: (undefined_entry.va,),
            undefined_use.va: (undefined_entry.va, undefined_seed.va),
        },
        (),
    )
    undefined_origins, undefined_definitions, _ = synthetic_byte_trace(
        undefined_decode, undefined_use.va
    )
    if (
        undefined_origins
        or undefined_definitions.get(undefined_use.va)
        != frozenset((None, undefined_seed.va))
    ):
        raise ExtractionError("byte-lane undefined-entry regression")

    conflict_entry = Instruction(0x3000, 0, 2, b"\x74\x04", "jcc")
    conflict_left = Instruction(
        0x3002,
        2,
        4,
        b"\x8B\x5C\x24\x04",
        "mov",
        dst=Operand("reg", reg="ebx"),
        src=Operand("mem", base="esp", disp=4),
    )
    conflict_right = Instruction(
        0x3006,
        6,
        4,
        b"\x8B\x5C\x24\x08",
        "mov",
        dst=Operand("reg", reg="ebx"),
        src=Operand("mem", base="esp", disp=8),
    )
    conflict_use = Instruction(0x300A, 10, 1, b"\x53", "push")
    conflict_decode = FunctionDecode(
        FunctionSpan(0x3000, 0x300B, 0, 11, ""),
        {
            conflict_entry.va: conflict_entry,
            conflict_left.va: conflict_left,
            conflict_right.va: conflict_right,
            conflict_use.va: conflict_use,
        },
        {
            conflict_entry.va: (conflict_left.va, conflict_right.va),
            conflict_left.va: (conflict_use.va,),
            conflict_right.va: (conflict_use.va,),
            conflict_use.va: (),
        },
        {
            conflict_entry.va: (),
            conflict_left.va: (conflict_entry.va,),
            conflict_right.va: (conflict_entry.va,),
            conflict_use.va: (conflict_left.va, conflict_right.va),
        },
        (),
    )
    conflict_origins, conflict_definitions, _ = synthetic_byte_trace(
        conflict_decode, conflict_use.va
    )
    if (
        conflict_origins
        or conflict_definitions.get(conflict_use.va)
        != frozenset((conflict_left.va, conflict_right.va))
    ):
        raise ExtractionError("byte-lane conflicting-definition regression")

    clobber_seed = Instruction(
        0x4000,
        0,
        4,
        b"\x8B\x5C\x24\x04",
        "mov",
        dst=Operand("reg", reg="ebx"),
        src=Operand("mem", base="esp", disp=4),
    )
    opaque_clobber = Instruction(0x4004, 4, 2, b"\x87\xD8", "other")
    clobber_use = Instruction(0x4006, 6, 1, b"\x53", "push")
    clobber_decode = FunctionDecode(
        FunctionSpan(0x4000, 0x4007, 0, 7, ""),
        {
            clobber_seed.va: clobber_seed,
            opaque_clobber.va: opaque_clobber,
            clobber_use.va: clobber_use,
        },
        {
            clobber_seed.va: (opaque_clobber.va,),
            opaque_clobber.va: (clobber_use.va,),
            clobber_use.va: (),
        },
        {
            clobber_seed.va: (),
            opaque_clobber.va: (clobber_seed.va,),
            clobber_use.va: (opaque_clobber.va,),
        },
        (),
    )
    clobber_origins, clobber_definitions, _ = synthetic_byte_trace(
        clobber_decode, clobber_use.va
    )
    if (
        clobber_origins
        or clobber_definitions.get(clobber_use.va)
        != frozenset((opaque_clobber.va,))
    ):
        raise ExtractionError("byte-lane opaque-clobber regression")

    partial_seed = Instruction(
        0x5000,
        0,
        4,
        b"\x8B\x5C\x24\x04",
        "mov",
        dst=Operand("reg", reg="ebx"),
        src=Operand("mem", base="esp", disp=4),
    )
    partial_write = Instruction(
        0x5004,
        4,
        4,
        b"\x66\xBB\x00\x00",
        "mov",
        dst=Operand("reg", reg="ebx"),
        src=Operand("imm", imm=0),
    )
    partial_use = Instruction(0x5008, 8, 1, b"\x53", "push")
    partial_decode = FunctionDecode(
        FunctionSpan(0x5000, 0x5009, 0, 9, ""),
        {
            partial_seed.va: partial_seed,
            partial_write.va: partial_write,
            partial_use.va: partial_use,
        },
        {
            partial_seed.va: (partial_write.va,),
            partial_write.va: (partial_use.va,),
            partial_use.va: (),
        },
        {
            partial_seed.va: (),
            partial_write.va: (partial_seed.va,),
            partial_use.va: (partial_write.va,),
        },
        (),
    )
    partial_origins, partial_definitions, _ = synthetic_byte_trace(
        partial_decode, partial_use.va
    )
    if (
        partial_origins
        or partial_definitions.get(partial_use.va)
        != frozenset((partial_write.va,))
    ):
        raise ExtractionError("byte-lane partial-write regression")
    partial_mode_analyzer = SerializerAnalyzer(image, [])
    partial_mode_analyzer.decode_cache[partial_decode.span.start_va] = (
        partial_decode
    )
    if partial_mode_analyzer._mode_argument_formal_offsets(
        partial_decode.span.start_va,
        partial_use.va,
        Operand("reg", reg="ebx"),
        1,
    ):
        raise ExtractionError("full-GPR fallback crossed a partial write")

    synthetic_zero_xor = Instruction(
        0x6000,
        0,
        2,
        b"\x33\xDB",
        "xor",
        dst=Operand("reg", reg="ebx"),
        src=Operand("reg", reg="ebx"),
    )
    synthetic_nonzero_xors = (
        Instruction(
            0x6000,
            0,
            3,
            b"\x66\x33\xDB",
            "xor",
            dst=Operand("reg", reg="ebx"),
            src=Operand("reg", reg="ebx"),
        ),
        Instruction(
            0x6000,
            0,
            2,
            b"\x33\xD9",
            "xor",
            dst=Operand("reg", reg="ebx"),
            src=Operand("reg", reg="ecx"),
        ),
        Instruction(
            0x6000,
            0,
            2,
            b"\x32\xDB",
            "xor",
            dst=Operand("reg", reg="bl"),
            src=Operand("reg", reg="bl"),
        ),
    )
    if (
        not analyzer._is_full_width_zeroing_xor(
            synthetic_zero_xor, "ebx"
        )
        or any(
            analyzer._is_full_width_zeroing_xor(ins, "ebx")
            for ins in synthetic_nonzero_xors
        )
    ):
        raise ExtractionError("full-width XOR-self zero policy regression")

    def synthetic_zero_trace(
        decoded: FunctionDecode, use_va: int, reg: str
    ) -> tuple[str, int] | None:
        synthetic_analyzer = SerializerAnalyzer(image, [])
        function_va = decoded.span.start_va
        synthetic_analyzer.decode_cache[function_va] = decoded
        return synthetic_analyzer._mode_argument_zero_reaching_definition(
            function_va,
            use_va,
            Operand("reg", reg=reg),
            1,
        )

    def synthetic_all_zero_trace(
        decoded: FunctionDecode, use_va: int, reg: str
    ) -> tuple[str, tuple[int, ...]] | None:
        synthetic_analyzer = SerializerAnalyzer(image, [])
        function_va = decoded.span.start_va
        synthetic_analyzer.decode_cache[function_va] = decoded
        return (
            synthetic_analyzer._mode_argument_all_zero_reaching_definitions(
                function_va,
                use_va,
                Operand("reg", reg=reg),
                1,
            )
        )

    zero_loop_head = Instruction(0x6002, 2, 2, b"\x85\xC0", "test")
    zero_loop_back = Instruction(0x6004, 4, 2, b"\x75\xFC", "jcc")
    zero_loop_use = Instruction(0x6006, 6, 1, b"\x53", "push")
    zero_loop_decode = FunctionDecode(
        FunctionSpan(0x6000, 0x6007, 0, 7, ""),
        {
            synthetic_zero_xor.va: synthetic_zero_xor,
            zero_loop_head.va: zero_loop_head,
            zero_loop_back.va: zero_loop_back,
            zero_loop_use.va: zero_loop_use,
        },
        {
            synthetic_zero_xor.va: (zero_loop_head.va,),
            zero_loop_head.va: (zero_loop_back.va, zero_loop_use.va),
            zero_loop_back.va: (zero_loop_head.va,),
            zero_loop_use.va: (),
        },
        {
            synthetic_zero_xor.va: (),
            zero_loop_head.va: (synthetic_zero_xor.va, zero_loop_back.va),
            zero_loop_back.va: (zero_loop_head.va,),
            zero_loop_use.va: (zero_loop_head.va,),
        },
        (),
    )
    if synthetic_zero_trace(
        zero_loop_decode, zero_loop_use.va, "ebx"
    ) != ("ebx", synthetic_zero_xor.va):
        raise ExtractionError("mode zero one-definition loop regression")

    zero_undefined_entry = Instruction(
        0x7000, 0, 2, b"\x74\x02", "jcc"
    )
    zero_undefined_seed = Instruction(
        0x7002,
        2,
        2,
        b"\x33\xDB",
        "xor",
        dst=Operand("reg", reg="ebx"),
        src=Operand("reg", reg="ebx"),
    )
    zero_undefined_use = Instruction(0x7004, 4, 1, b"\x53", "push")
    zero_undefined_decode = FunctionDecode(
        FunctionSpan(0x7000, 0x7005, 0, 5, ""),
        {
            zero_undefined_entry.va: zero_undefined_entry,
            zero_undefined_seed.va: zero_undefined_seed,
            zero_undefined_use.va: zero_undefined_use,
        },
        {
            zero_undefined_entry.va: (
                zero_undefined_seed.va,
                zero_undefined_use.va,
            ),
            zero_undefined_seed.va: (zero_undefined_use.va,),
            zero_undefined_use.va: (),
        },
        {
            zero_undefined_entry.va: (),
            zero_undefined_seed.va: (zero_undefined_entry.va,),
            zero_undefined_use.va: (
                zero_undefined_entry.va,
                zero_undefined_seed.va,
            ),
        },
        (),
    )
    if synthetic_zero_trace(
        zero_undefined_decode, zero_undefined_use.va, "ebx"
    ) is not None:
        raise ExtractionError("mode zero undefined-entry regression")
    if synthetic_all_zero_trace(
        zero_undefined_decode, zero_undefined_use.va, "ebx"
    ) is not None:
        raise ExtractionError("mode zero-set crossed an undefined entry")

    zero_conflict_entry = Instruction(
        0x8000, 0, 2, b"\x74\x02", "jcc"
    )
    zero_conflict_left = Instruction(
        0x8002,
        2,
        2,
        b"\x33\xDB",
        "xor",
        dst=Operand("reg", reg="ebx"),
        src=Operand("reg", reg="ebx"),
    )
    zero_conflict_right = Instruction(
        0x8004,
        4,
        2,
        b"\x33\xDB",
        "xor",
        dst=Operand("reg", reg="ebx"),
        src=Operand("reg", reg="ebx"),
    )
    zero_conflict_use = Instruction(0x8006, 6, 1, b"\x53", "push")
    zero_conflict_decode = FunctionDecode(
        FunctionSpan(0x8000, 0x8007, 0, 7, ""),
        {
            zero_conflict_entry.va: zero_conflict_entry,
            zero_conflict_left.va: zero_conflict_left,
            zero_conflict_right.va: zero_conflict_right,
            zero_conflict_use.va: zero_conflict_use,
        },
        {
            zero_conflict_entry.va: (
                zero_conflict_left.va,
                zero_conflict_right.va,
            ),
            zero_conflict_left.va: (zero_conflict_use.va,),
            zero_conflict_right.va: (zero_conflict_use.va,),
            zero_conflict_use.va: (),
        },
        {
            zero_conflict_entry.va: (),
            zero_conflict_left.va: (zero_conflict_entry.va,),
            zero_conflict_right.va: (zero_conflict_entry.va,),
            zero_conflict_use.va: (
                zero_conflict_left.va,
                zero_conflict_right.va,
            ),
        },
        (),
    )
    if synthetic_zero_trace(
        zero_conflict_decode, zero_conflict_use.va, "ebx"
    ) is not None:
        raise ExtractionError("mode zero multiple-definition regression")
    if synthetic_all_zero_trace(
        zero_conflict_decode, zero_conflict_use.va, "ebx"
    ) != (
        "ebx",
        (zero_conflict_left.va, zero_conflict_right.va),
    ):
        raise ExtractionError("mode zero-set all-definition regression")
    zero_mixed_right = Instruction(
        zero_conflict_right.va,
        zero_conflict_right.off,
        2,
        b"\x33\xD9",
        "xor",
        dst=Operand("reg", reg="ebx"),
        src=Operand("reg", reg="ecx"),
    )
    zero_mixed_decode = FunctionDecode(
        zero_conflict_decode.span,
        {
            zero_conflict_entry.va: zero_conflict_entry,
            zero_conflict_left.va: zero_conflict_left,
            zero_mixed_right.va: zero_mixed_right,
            zero_conflict_use.va: zero_conflict_use,
        },
        zero_conflict_decode.successors,
        zero_conflict_decode.predecessors,
        (),
    )
    if synthetic_all_zero_trace(
        zero_mixed_decode, zero_conflict_use.va, "ebx"
    ) is not None:
        raise ExtractionError("mode zero-set accepted a nonzero definition")
    direct_zero_resolver = RegisterResolver(zero_conflict_decode)
    if (
        direct_zero_resolver.reg_before(
            zero_conflict_use.va, "ebx"
        )
        != ("const", 0)
        or analyzer._mode_zero_classes(
            direct_zero_resolver.reg_before(
                zero_conflict_use.va, "ebx"
            )
        )
        != frozenset(("zero",))
    ):
        raise ExtractionError("direct symbolic zero value-meet regression")

    zero_ebp_seed = Instruction(
        0x9000,
        0,
        2,
        b"\x33\xED",
        "xor",
        dst=Operand("reg", reg="ebp"),
        src=Operand("reg", reg="ebp"),
    )
    zero_ebp_use = Instruction(0x9002, 2, 1, b"\x55", "push")
    zero_ebp_decode = FunctionDecode(
        FunctionSpan(0x9000, 0x9003, 0, 3, ""),
        {zero_ebp_seed.va: zero_ebp_seed, zero_ebp_use.va: zero_ebp_use},
        {zero_ebp_seed.va: (zero_ebp_use.va,), zero_ebp_use.va: ()},
        {zero_ebp_seed.va: (), zero_ebp_use.va: (zero_ebp_seed.va,)},
        (),
    )
    if synthetic_zero_trace(
        zero_ebp_decode, zero_ebp_use.va, "ebp"
    ) != ("ebp", zero_ebp_seed.va):
        raise ExtractionError("mode zero non-byte-register regression")
    direct_zero_rows = [
        row
        for row in rows
        if row.message == "Express_InitalizeActorExpressVital"
        and row.file_off_claim == 0x002E767A
    ]
    direct_zero_function = 0x006E8150
    direct_zero_use = 0x006E8276
    direct_zero_definitions = frozenset((0x006E8219, 0x006E824B))
    direct_zero_decode = analyzer.decode(direct_zero_function)
    if (
        len(direct_zero_rows) != 1
        or direct_zero_rows[0].direction != "R"
        or direct_zero_rows[0].tag != "SUBCALL:0x006E3640"
        or direct_zero_rows[0].reason
        or "mode_arg@0x006E8276 file_off=0x002E7676 value=zero"
        not in direct_zero_rows[0].gate_condition
        or "mode_zero_reaching_def@" in direct_zero_rows[0].gate_condition
        or direct_zero_decode is None
        or analyzer._reaching_definitions(
            direct_zero_function, "ebp"
        ).get(direct_zero_use, frozenset())
        != direct_zero_definitions
        or any(
            not analyzer._is_full_width_zeroing_xor(
                direct_zero_decode.instructions[definition_va], "ebp"
            )
            for definition_va in direct_zero_definitions
        )
        or RegisterResolver(direct_zero_decode).reg_before(
            direct_zero_use, "ebp"
        )
        != ("const", 0)
    ):
        raise ExtractionError("direct symbolic multi-zero acceptance mismatch")
    names = {item.name for item in registry}
    emitted_names = {row.message for row in rows}
    if emitted_names != names:
        raise ExtractionError("A2 message coverage mismatch")

    orders: dict[tuple[str, str], list[int]] = defaultdict(list)
    by_message: dict[str, list[FieldRow]] = defaultdict(list)
    measured_byte_reaching_evidence: set[
        tuple[str, int, int, str, int, int]
    ] = set()
    expected_byte_reaching_evidence: set[
        tuple[str, int, int, str, int, int]
    ] = set()
    measured_zero_reaching_evidence: set[
        tuple[int, int, str, int]
    ] = set()
    expected_zero_reaching_evidence: set[
        tuple[int, int, str, int]
    ] = set()
    measured_zero_set_evidence: set[
        tuple[int, int, str, tuple[int, ...]]
    ] = set()
    expected_zero_set_evidence: set[
        tuple[int, int, str, tuple[int, ...]]
    ] = set()
    measured_nested_mode_anchors: set[str] = set()
    measured_nested_stream_anchors: set[str] = set()
    measured_predicate_zero_proofs: set[str] = set()
    measured_local_capability_refinements: set[str] = set()
    measured_identity_zero_evidence: set[str] = set()
    expected_identity_zero_evidence: set[str] = set()
    measured_register_import_evidence: set[str] = set()
    measured_stack_identity_evidence: set[str] = set()
    measured_getid_stack_evidence: set[str] = set()
    measured_indirect_mode_sources: set[str] = set()
    nested_mode_pattern = (
        r"mode_nested_anchor_([WR])@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x([0-9A-F]{8}) "
        r"caller_stream_formal=entry\+0x([0-9A-F]+) "
        r"target_stream_formal=entry\+0x([0-9A-F]+) "
        r"arguments=\([^)]*\) primitives=\([^)]*\) "
        r"stream_proof_sha256=[0-9a-f]{64} "
        r"basis=branch_exclusive_single_direction_direct_subcall"
    )
    nested_stream_pattern = (
        r"target_nested_stream_anchor_([WR])@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"target=0x([0-9A-F]{8}) "
        r"target_formal=entry\+0x([0-9A-F]+) "
        r"child_formal=entry\+0x([0-9A-F]+) "
        r"mode_formal=entry\+0x([0-9A-F]+) mode_value=(zero|nonzero) "
        r"nested_evidence_sha256=[0-9a-f]{64} "
        r"basis=direction_selected_branch_exclusive_subcall"
    )
    predicate_zero_pattern = (
        r"predicate_zero_reaching function=0x([0-9A-F]{8}) "
        r"lane=(al|cl|dl|bl) register=(eax|ecx|edx|ebx) "
        r"use@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
        r"consumed_width=1 value=zero definition_count=([0-9]+) "
        r"definitions=\(([^)]+)\) "
        r"basis=all_reaching_full_width_xor_self"
    )
    local_capability_pattern = (
        r"local_capability_refinement function=0x([0-9A-F]{8}) "
        r"raw=([RW](?:,[RW])?) refined=([RW]) "
        r"entry_boundary=\(([^)]*)\) "
        r"direct_primitives=\(([^)]*)\) subcalls=\(([^)]*)\) "
        r"basis=complete_known_direct_serializer_edge_census"
    )
    identity_zero_pattern = (
        r"mode_zero_identity_lea function=0x([0-9A-F]{8}) "
        r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
        r"use@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
        r"consumed_width=1 value=zero "
        r"identity@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
        r"definition_count=([0-9]+) definitions=\(([^)]*)\) "
        r"basis=all_reaching_full_width_xor_self_through_exact_"
        r"full_width_identity_lea "
        r"mode_arg@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
        r"value=zero"
    )
    getid_stack_pattern = (
        r"stack_neutral_vtable_getid@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
        r"definition@0x([0-9A-F]{8}) "
        r"definition_file_off=0x([0-9A-F]{8}) slot=0x10 cleanup=0 "
        r"basis=task_pinned_getid_slot_and_adjacent_exact_load"
    )
    indirect_mode_source_pattern = (
        r"indirect_mode_formal_source definition@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) use@0x([0-9A-F]{8}) "
        r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
        r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
        r"displacement=0x([0-9A-F]+) stack_depth=0x([0-9A-F]+) "
        r"formal=entry\+0x([0-9A-F]+) "
        r"basis=singleton_reaching_exact_esp_disp8_load"
    )
    for row in rows:
        orders[(row.message, row.direction)].append(row.order)
        by_message[row.message].append(row)
        if row.file_off_claim is None or not (0 <= row.file_off_claim < len(image.data)):
            raise ExtractionError("A2 row lacks a mapped claim file offset")
        for evidence_va, evidence_off in re.findall(
            r"@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8})",
            row.gate_condition,
        ):
            mapped = image.va_to_off(int(evidence_va, 16))
            if mapped != int(evidence_off, 16):
                raise ExtractionError(
                    "A2 gate evidence offset mismatch at VA 0x%s" % evidence_va
                )
        getid_matches = list(
            re.finditer(getid_stack_pattern, row.gate_condition)
        )
        if len(getid_matches) != row.gate_condition.count(
            "stack_neutral_vtable_getid@"
        ):
            raise ExtractionError("A2 malformed GetId stack evidence")
        for match in getid_matches:
            (
                site_text,
                off_text,
                function_text,
                register,
                definition_text,
                definition_off_text,
            ) = match.groups()
            site = int(site_text, 16)
            off = int(off_text, 16)
            function = int(function_text, 16)
            definition_va = int(definition_text, 16)
            definition_off = int(definition_off_text, 16)
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            if (
                image.va_to_off(site) != off
                or image.va_to_off(definition_va) != definition_off
                or ins is None
                or analyzer._stack_neutral_vtable_getid(function, ins)
                != (register, definition_va)
                or match.group(0)
                not in analyzer._stack_neutral_vtable_getid_fragments(
                    function
                )
            ):
                raise ExtractionError(
                    "A2 GetId stack evidence mismatch at VA 0x%08X" % site
                )
            measured_getid_stack_evidence.add(match.group(0))
        mode_source_matches = list(
            re.finditer(indirect_mode_source_pattern, row.gate_condition)
        )
        if len(mode_source_matches) != row.gate_condition.count(
            "indirect_mode_formal_source "
        ):
            raise ExtractionError("A2 malformed indirect mode source")
        for match in mode_source_matches:
            (
                definition_text,
                definition_off_text,
                use_text,
                use_off_text,
                function_text,
                register,
                displacement_text,
                depth_text,
                formal_text,
            ) = match.groups()
            definition_va = int(definition_text, 16)
            definition_off = int(definition_off_text, 16)
            use_va = int(use_text, 16)
            use_off = int(use_off_text, 16)
            function = int(function_text, 16)
            formal = int(formal_text, 16)
            decoded = analyzer.decode(function)
            use = None if decoded is None else decoded.instructions.get(use_va)
            fragment = (
                None
                if use is None or use.src is None
                else analyzer._indirect_mode_formal_source_fragment(
                    function, PushArgument(use_va, use.src), formal
                )
            )
            if (
                image.va_to_off(definition_va) != definition_off
                or image.va_to_off(use_va) != use_off
                or use is None
                or use.src is None
                or use.src.kind != "reg"
                or use.src.reg != register
                or fragment != match.group(0)
                or int(displacement_text, 16) - int(depth_text, 16)
                != formal
            ):
                raise ExtractionError(
                    "A2 indirect mode source mismatch at VA 0x%08X" % use_va
                )
            measured_indirect_mode_sources.add(match.group(0))
        for match in re.finditer(local_capability_pattern, row.gate_condition):
            (
                function_text,
                raw_text,
                refined_direction,
                entry_boundary_text,
                primitives_text,
                subcalls_text,
            ) = match.groups()
            function = int(function_text, 16)
            decoded = analyzer.decode(function)
            refined, expected_fragment = (
                analyzer._local_capability_refinement(function)
            )
            measured_primitive_edges = {
                (direction, int(site, 16), int(off, 16), int(target, 16))
                for direction, site, off, target in re.findall(
                    r"primitive_([WR])@0x([0-9A-F]{8}) "
                    r"file_off=0x([0-9A-F]{8}) target=0x([0-9A-F]{8})",
                    primitives_text,
                )
            }
            expected_primitive_edges = set()
            if decoded is not None:
                expected_primitive_edges = {
                    (
                        "W" if ins.target == WRITE_VA else "R",
                        ins.va,
                        ins.off,
                        ins.target,
                    )
                    for ins in decoded.instructions.values()
                    if ins.kind == "call"
                    and ins.target in (WRITE_VA, READ_VA)
                }
            measured_child_edges = {
                (int(site, 16), int(off, 16), int(target, 16))
                for site, off, target in re.findall(
                    r"subcall@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
                    r"target=0x([0-9A-F]{8})",
                    subcalls_text,
                )
            }
            expected_child_edges = set()
            if decoded is not None:
                expected_child_edges = {
                    (ins.va, ins.off, ins.target)
                    for ins in decoded.instructions.values()
                    if ins.kind == "call"
                    and ins.target is not None
                    and ins.target not in (WRITE_VA, READ_VA)
                    and bool(analyzer.capabilities(ins.target))
                }
            boundary_match = re.fullmatch(
                r"ret@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
                r"int3_start@0x([0-9A-F]{8}) "
                r"file_off=0x([0-9A-F]{8}) int3_count=([0-9]+)",
                entry_boundary_text,
            )
            boundary_valid = False
            if boundary_match is not None:
                ret_va, ret_off, int3_va, int3_off, int3_count = (
                    int(value, 16 if index < 4 else 10)
                    for index, value in enumerate(boundary_match.groups())
                )
                boundary_valid = (
                    image.va_to_off(ret_va) == ret_off
                    and image.va_to_off(int3_va) == int3_off
                    and ret_off + 1 == int3_off
                    and int3_off + int3_count == image.va_to_off(function)
                    and image.data[ret_off] == 0xC3
                    and image.data[int3_off : int3_off + int3_count]
                    == b"\xCC" * int3_count
                )
            if (
                decoded is None
                or decoded.span.start_va != function
                or raw_text != ",".join(sorted(analyzer.capabilities(function)))
                or refined != frozenset((refined_direction,))
                or expected_fragment != match.group(0)
                or row.direction != refined_direction
                or measured_primitive_edges != expected_primitive_edges
                or measured_child_edges != expected_child_edges
                or not boundary_valid
                or not (
                    re.search(
                        r"subcall_path@0x[0-9A-F]{8} "
                        r"file_off=0x[0-9A-F]{8} target=0x%08X"
                        % function,
                        row.gate_condition,
                    )
                    or re.search(
                        r"stream_call@0x[0-9A-F]{8} "
                        r"file_off=0x[0-9A-F]{8} caller=0x[0-9A-F]{8} "
                        r"target=0x%08X" % function,
                        row.gate_condition,
                    )
                )
            ):
                raise ExtractionError(
                    "A2 local capability refinement mismatch at 0x%08X"
                    % function
                )
            measured_local_capability_refinements.add(match.group(0))
        for match in re.finditer(identity_zero_pattern, row.gate_condition):
            (
                function_text,
                register,
                use_text,
                use_off_text,
                identity_text,
                identity_off_text,
                count_text,
                definitions_text,
                mode_use_text,
                mode_use_off_text,
            ) = match.groups()
            function = int(function_text, 16)
            use = int(use_text, 16)
            use_off = int(use_off_text, 16)
            identity = int(identity_text, 16)
            identity_off = int(identity_off_text, 16)
            definitions = tuple(
                int(definition, 16)
                for definition, _definition_off in re.findall(
                    r"definition@0x([0-9A-F]{8}) "
                    r"file_off=0x([0-9A-F]{8})",
                    definitions_text,
                )
            )
            decoded = analyzer.decode(function)
            use_ins = (
                None if decoded is None else decoded.instructions.get(use)
            )
            proof = analyzer._mode_argument_zero_through_identity_lea(
                function,
                use,
                Operand("reg", reg=register),
                1,
            )
            expected_fragment = analyzer._mode_zero_identity_lea_fragment(
                function,
                PushArgument(use, Operand("reg", reg=register)),
                register,
                identity,
                definitions,
            )
            if (
                proof != (register, identity, definitions)
                or expected_fragment != match.group(0)
                or int(count_text) != len(definitions)
                or not definitions
                or image.va_to_off(use) != use_off
                or image.va_to_off(identity) != identity_off
                or int(mode_use_text, 16) != use
                or int(mode_use_off_text, 16) != use_off
                or use_ins is None
                or use_ins.kind != "push"
                or use_ins.src != Operand("reg", reg=register)
            ):
                raise ExtractionError(
                    "A2 identity-LEA zero evidence mismatch at VA 0x%08X"
                    % use
                )
            measured_identity_zero_evidence.add(match.group(0))
        for match in re.finditer(nested_mode_pattern, row.gate_condition):
            (
                direction,
                site_text,
                off_text,
                function_text,
                target_text,
                caller_formal_text,
                target_formal_text,
            ) = match.groups()
            site = int(site_text, 16)
            off = int(off_text, 16)
            function = int(function_text, 16)
            target = int(target_text, 16)
            caller_formal = int(caller_formal_text, 16)
            target_formal = int(target_formal_text, 16)
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            measured = (
                None
                if ins is None
                else analyzer._nested_mode_anchor(function, ins)
            )
            abi = None if decoded is None else analyzer._function_abi(decoded)
            branch_proof = (
                None
                if abi is None
                else analyzer._unique_mode_formal_proof(function, abi)
            )
            branch_evidence = (
                ""
                if branch_proof is None
                else branch_proof.zero_anchor_evidence
                if branch_proof.zero_direction == direction
                and branch_proof.zero_anchor_va == site
                else branch_proof.nonzero_anchor_evidence
                if branch_proof.nonzero_direction == direction
                and branch_proof.nonzero_anchor_va == site
                else ""
            )
            stream_match = re.search(
                r"caller_stream_formal=entry\+0x([0-9A-F]+) "
                r"target_stream_formal=entry\+0x([0-9A-F]+)",
                match.group(0),
            )
            if (
                image.va_to_off(site) != off
                or ins is None
                or ins.kind != "call"
                or ins.target != target
                or measured != (direction, match.group(0))
                or branch_evidence != match.group(0)
                or stream_match is None
                or int(stream_match.group(1), 16) != caller_formal
                or int(stream_match.group(2), 16) != target_formal
            ):
                raise ExtractionError(
                    "A2 nested mode anchor mismatch at VA 0x%08X" % site
                )
            measured_nested_mode_anchors.add(match.group(0))
        for match in re.finditer(predicate_zero_pattern, row.gate_condition):
            (
                function_text,
                lane,
                reg,
                use_text,
                off_text,
                count_text,
                definitions_text,
            ) = match.groups()
            function = int(function_text, 16)
            use_va = int(use_text, 16)
            use_off = int(off_text, 16)
            count = int(count_text)
            definition_items = tuple(
                (
                    int(definition_va, 16),
                    int(definition_off, 16),
                )
                for definition_va, definition_off in re.findall(
                    r"definition@0x([0-9A-F]{8}) "
                    r"file_off=0x([0-9A-F]{8})",
                    definitions_text,
                )
            )
            definition_vas = tuple(item[0] for item in definition_items)
            decoded = analyzer.decode(function)
            predicate = (
                None if decoded is None else decoded.instructions.get(use_va)
            )
            formals, evidence = (
                (frozenset(), "")
                if predicate is None
                else analyzer._predicate_formal_offsets_with_zero_proof(
                    function, predicate
                )
            )
            zero_proof = analyzer._mode_argument_all_zero_reaching_definitions(
                function,
                use_va,
                Operand("reg", reg=reg),
                1,
            )
            if (
                LOW8_BY_REG32.get(reg) != lane
                or image.va_to_off(use_va) != use_off
                or predicate is None
                or predicate.kind != "cmp"
                or analyzer._predicate_width(predicate) != 1
                or len(formals) != 1
                or evidence != match.group(0)
                or count != len(definition_items)
                or count < 1
                or definition_vas != tuple(sorted(definition_vas))
                or any(
                    image.va_to_off(definition_va) != definition_off
                    for definition_va, definition_off in definition_items
                )
                or zero_proof != (reg, definition_vas)
            ):
                raise ExtractionError(
                    "A2 predicate zero evidence mismatch at VA 0x%08X"
                    % use_va
                )
            measured_predicate_zero_proofs.add(match.group(0))
        neutral_import_pattern = (
            r"stack_neutral_import@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"function=0x([0-9A-F]{8}) iat=0x([0-9A-F]{8}) "
            r"iat_file_off=0x([0-9A-F]{8}) "
            r"descriptor_file_off=0x([0-9A-F]{8}) "
            r"lookup_file_off=0x([0-9A-F]{8}) "
            r"dll_name_file_off=0x([0-9A-F]{8}) "
            r"symbol_name_file_off=0x([0-9A-F]{8}) "
            r"dll=([^ ]+) symbol=([^ ]+) cleanup=0"
        )
        neutral_sites_by_function: dict[int, set[int]] = defaultdict(set)
        for match in re.findall(neutral_import_pattern, row.gate_condition):
            (
                site_text,
                off_text,
                function_text,
                iat_text,
                iat_off_text,
                descriptor_off_text,
                lookup_off_text,
                dll_off_text,
                symbol_off_text,
                dll,
                name,
            ) = match
            site = int(site_text, 16)
            off = int(off_text, 16)
            function = int(function_text, 16)
            iat = int(iat_text, 16)
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            symbol = image.imports_by_iat.get(iat)
            if (
                image.va_to_off(site) != off
                or ins is None
                or analyzer._stack_neutral_import(ins) != symbol
                or symbol is None
                or (symbol.dll, symbol.name) not in STACK_NEUTRAL_IMPORTS
                or (
                    symbol.iat_off,
                    symbol.descriptor_off,
                    symbol.lookup_off,
                    symbol.dll_name_off,
                    symbol.symbol_name_off,
                    symbol.dll,
                    symbol.name,
                )
                != (
                    int(iat_off_text, 16),
                    int(descriptor_off_text, 16),
                    int(lookup_off_text, 16),
                    int(dll_off_text, 16),
                    int(symbol_off_text, 16),
                    dll,
                    name,
                )
                or image._ascii_at_off(symbol.dll_name_off) != dll
                or image._ascii_at_off(symbol.symbol_name_off) != name
            ):
                raise ExtractionError(
                    "A2 stack-neutral import evidence mismatch at VA 0x%08X"
                    % site
                )
            neutral_sites_by_function[function].add(site)
        register_neutral_pattern = (
            r"stack_neutral_register_import@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) "
            r"function=0x([0-9A-F]{8}) "
            r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
            r"definition@0x([0-9A-F]{8}) "
            r"definition_file_off=0x([0-9A-F]{8}) "
            r"iat=0x([0-9A-F]{8}) "
            r"iat_file_off=0x([0-9A-F]{8}) "
            r"descriptor_file_off=0x([0-9A-F]{8}) "
            r"lookup_file_off=0x([0-9A-F]{8}) "
            r"dll_name_file_off=0x([0-9A-F]{8}) "
            r"symbol_name_file_off=0x([0-9A-F]{8}) "
            r"dll=([^ ]+) symbol=([^ ]+) cleanup=0 "
            r"basis=singleton_reaching_exact_iat_load"
        )
        register_matches = list(
            re.finditer(register_neutral_pattern, row.gate_condition)
        )
        if len(register_matches) != row.gate_condition.count(
            "stack_neutral_register_import@"
        ):
            raise ExtractionError(
                "A2 malformed register-indirect import evidence"
            )
        for match in register_matches:
            (
                site_text,
                off_text,
                function_text,
                register,
                definition_text,
                definition_off_text,
                iat_text,
                iat_off_text,
                descriptor_off_text,
                lookup_off_text,
                dll_off_text,
                symbol_off_text,
                dll,
                name,
            ) = match.groups()
            site = int(site_text, 16)
            off = int(off_text, 16)
            function = int(function_text, 16)
            definition_va = int(definition_text, 16)
            definition_off = int(definition_off_text, 16)
            iat = int(iat_text, 16)
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            definition = (
                None
                if decoded is None
                else decoded.instructions.get(definition_va)
            )
            symbol = image.imports_by_iat.get(iat)
            proof = (
                None
                if ins is None
                else analyzer._stack_neutral_register_import(function, ins)
            )
            if (
                image.va_to_off(site) != off
                or image.va_to_off(definition_va) != definition_off
                or ins is None
                or definition is None
                or symbol is None
                or proof != (symbol, register, definition_va)
                or analyzer._reaching_definitions(function, register).get(
                    site, frozenset()
                )
                != frozenset((definition_va,))
                or not analyzer._is_exact_register_indirect_call(
                    ins, register
                )
                or not analyzer._is_exact_iat_register_load(
                    definition, register, iat
                )
                or (symbol.dll, symbol.name) not in STACK_NEUTRAL_IMPORTS
                or (
                    symbol.iat_off,
                    symbol.descriptor_off,
                    symbol.lookup_off,
                    symbol.dll_name_off,
                    symbol.symbol_name_off,
                    symbol.dll,
                    symbol.name,
                )
                != (
                    int(iat_off_text, 16),
                    int(descriptor_off_text, 16),
                    int(lookup_off_text, 16),
                    int(dll_off_text, 16),
                    int(symbol_off_text, 16),
                    dll,
                    name,
                )
                or image._ascii_at_off(symbol.dll_name_off) != dll
                or image._ascii_at_off(symbol.symbol_name_off) != name
                or match.group(0)
                not in analyzer._stack_neutral_import_fragments(function)
            ):
                raise ExtractionError(
                    "A2 register-indirect stack-neutral import evidence "
                    "mismatch at VA 0x%08X" % site
                )
            neutral_sites_by_function[function].add(site)
            measured_register_import_evidence.add(match.group(0))
        stack_identity_pattern = (
            r"stack_identity_lea@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) "
            r"function=0x([0-9A-F]{8}) register=esp displacement=0 "
            r"basis=exact_full_width_stack_identity"
        )
        stack_identity_sites_by_function: dict[int, set[int]] = defaultdict(set)
        stack_identity_matches = list(
            re.finditer(stack_identity_pattern, row.gate_condition)
        )
        if len(stack_identity_matches) != row.gate_condition.count(
            "stack_identity_lea@"
        ):
            raise ExtractionError("A2 malformed stack identity LEA evidence")
        for match in stack_identity_matches:
            site = int(match.group(1), 16)
            off = int(match.group(2), 16)
            function = int(match.group(3), 16)
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            if (
                image.va_to_off(site) != off
                or ins is None
                or not analyzer._is_exact_stack_identity_lea(ins)
                or match.group(0)
                not in analyzer._stack_identity_lea_fragments(function)
            ):
                raise ExtractionError(
                    "A2 stack identity LEA evidence mismatch at VA 0x%08X"
                    % site
                )
            stack_identity_sites_by_function[function].add(site)
            measured_stack_identity_evidence.add(match.group(0))
        formal_base_pattern = (
            r"stack_formal_base@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"register=(eax|ecx|edx|ebx|ebp|esi|edi) source=esp "
            r"entry_delta=([+-])0x([0-9A-F]+)"
        )
        formal_base_sites_by_function: dict[int, set[int]] = defaultdict(set)
        for match in re.findall(formal_base_pattern, row.gate_condition):
            (
                site_text,
                off_text,
                function_text,
                register,
                sign,
                magnitude_text,
            ) = match
            site = int(site_text, 16)
            off = int(off_text, 16)
            function = int(function_text, 16)
            magnitude = int(magnitude_text, 16)
            claimed_delta = magnitude if sign == "+" else -magnitude
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            site_depths = analyzer._stack_depths(function).get(
                site, frozenset()
            )
            if (
                image.va_to_off(site) != off
                or ins is None
                or not analyzer._is_full_width_plain_mov(ins)
                or ins.dst is None
                or ins.dst.kind != "reg"
                or base_reg_name(ins.dst.reg) != register
                or ins.src is None
                or ins.src.kind != "reg"
                or base_reg_name(ins.src.reg) != "esp"
                or len(site_depths) != 1
                or None in site_depths
                or claimed_delta != -next(iter(site_depths))
            ):
                raise ExtractionError(
                    "A2 stack formal base evidence mismatch at VA 0x%08X"
                    % site
                )
            formal_base_sites_by_function[function].add(site)
        reaching_pattern = (
            r"formal_reaching_def@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
            r"use@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"formal=entry\+0x([0-9A-F]+) "
            r"basis=unique_reaching_definition"
        )
        reaching_evidence = set()
        zero_reaching_evidence = set()
        zero_set_evidence = set()
        for match in re.findall(reaching_pattern, row.gate_condition):
            (
                definition_text,
                definition_off_text,
                function_text,
                register,
                use_text,
                use_off_text,
                formal_text,
            ) = match
            definition_va = int(definition_text, 16)
            definition_off = int(definition_off_text, 16)
            function = int(function_text, 16)
            use_va = int(use_text, 16)
            use_off = int(use_off_text, 16)
            formal = int(formal_text, 16)
            decoded = analyzer.decode(function)
            definition = (
                None
                if decoded is None
                else decoded.instructions.get(definition_va)
            )
            if (
                image.va_to_off(definition_va) != definition_off
                or image.va_to_off(use_va) != use_off
                or decoded is None
                or use_va not in decoded.instructions
                or definition is None
                or not analyzer._is_full_width_plain_mov(definition)
                or definition.dst is None
                or definition.dst.kind != "reg"
                or base_reg_name(definition.dst.reg) != register
                or definition.dst.reg in REG8
                or analyzer._reaching_definitions(function, register).get(
                    use_va, frozenset()
                )
                != frozenset((definition_va,))
                or analyzer._formal_offsets(
                    function, use_va, Operand("reg", reg=register)
                )
                != frozenset((formal,))
            ):
                raise ExtractionError(
                    "A2 formal reaching-definition evidence mismatch at "
                    "VA 0x%08X" % definition_va
                )
            reaching_evidence.add(
                (
                    "unique_reaching_definition",
                    function,
                    use_va,
                    register,
                    definition_va,
                    formal,
                )
            )
        byte_reaching_pattern = (
            r"formal_byte_reaching_def@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"lane=(al|cl|dl|bl|ah|ch|dh|bh) "
            r"use@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"formal=entry\+0x([0-9A-F]+) definition_width=32 "
            r"consumed_width=8 source=stack_formal "
            r"basis=unique_byte_lane_reaching_definition"
        )
        for match in re.findall(byte_reaching_pattern, row.gate_condition):
            (
                definition_text,
                definition_off_text,
                function_text,
                lane,
                use_text,
                use_off_text,
                formal_text,
            ) = match
            definition_va = int(definition_text, 16)
            definition_off = int(definition_off_text, 16)
            function = int(function_text, 16)
            use_va = int(use_text, 16)
            use_off = int(use_off_text, 16)
            formal = int(formal_text, 16)
            decoded = analyzer.decode(function)
            definition = (
                None
                if decoded is None
                else decoded.instructions.get(definition_va)
            )
            source_depths = analyzer._stack_depths(function).get(
                definition_va, frozenset()
            )
            destination_base = (
                None
                if definition is None
                or definition.dst is None
                or definition.dst.kind != "reg"
                or definition.dst.reg in REG8
                else base_reg_name(definition.dst.reg)
            )
            source = None if definition is None else definition.src
            if (
                image.va_to_off(definition_va) != definition_off
                or image.va_to_off(use_va) != use_off
                or decoded is None
                or use_va not in decoded.instructions
                or definition is None
                or not analyzer._is_full_width_plain_mov(definition)
                or destination_base is None
                or LOW8_BY_REG32.get(destination_base) != lane
                or source is None
                or source.kind != "mem"
                or source.base != "esp"
                or source.index is not None
                or source.absolute is not None
                or len(source_depths) != 1
                or None in source_depths
                or source.disp - next(iter(source_depths)) != formal
                or analyzer._byte_reaching_definitions(function, lane).get(
                    use_va, frozenset()
                )
                != frozenset((definition_va,))
                or analyzer._mode_argument_formal_offsets(
                    function,
                    use_va,
                    Operand("reg", reg=lane),
                    1,
                )
                != frozenset((formal,))
            ):
                raise ExtractionError(
                    "A2 formal byte-lane reaching evidence mismatch at "
                    "VA 0x%08X" % definition_va
                )
            evidence_key = (
                "unique_byte_lane_reaching_definition",
                function,
                use_va,
                lane,
                definition_va,
                formal,
            )
            reaching_evidence.add(evidence_key)
            measured_byte_reaching_evidence.add(evidence_key)
        zero_reaching_pattern = (
            r"mode_zero_reaching_def@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
            r"use@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"consumed_width=1 value=zero "
            r"basis=unique_full_width_xor_self "
            r"mode_arg@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) value=zero"
        )
        for match in re.findall(zero_reaching_pattern, row.gate_condition):
            (
                definition_text,
                definition_off_text,
                function_text,
                register,
                use_text,
                use_off_text,
                mode_use_text,
                mode_use_off_text,
            ) = match
            definition_va = int(definition_text, 16)
            definition_off = int(definition_off_text, 16)
            function = int(function_text, 16)
            use_va = int(use_text, 16)
            use_off = int(use_off_text, 16)
            mode_use_va = int(mode_use_text, 16)
            mode_use_off = int(mode_use_off_text, 16)
            decoded = analyzer.decode(function)
            definition = (
                None
                if decoded is None
                else decoded.instructions.get(definition_va)
            )
            lane = LOW8_BY_REG32.get(register)
            definitions = (
                analyzer._byte_reaching_definitions(function, lane)
                if lane is not None
                else analyzer._reaching_definitions(function, register)
            ).get(use_va, frozenset())
            if (
                image.va_to_off(definition_va) != definition_off
                or image.va_to_off(use_va) != use_off
                or use_va != mode_use_va
                or use_off != mode_use_off
                or decoded is None
                or use_va not in decoded.instructions
                or definition is None
                or not analyzer._is_full_width_zeroing_xor(
                    definition, register
                )
                or definitions != frozenset((definition_va,))
                or analyzer._mode_argument_zero_reaching_definition(
                    function,
                    use_va,
                    Operand("reg", reg=register),
                    1,
                )
                != (register, definition_va)
            ):
                raise ExtractionError(
                    "A2 mode zero reaching evidence mismatch at VA 0x%08X"
                    % definition_va
                )
            zero_key = (function, use_va, register, definition_va)
            zero_reaching_evidence.add(zero_key)
            measured_zero_reaching_evidence.add(zero_key)
        zero_set_validation_pattern = (
            r"mode_zero_reaching_set function=0x([0-9A-F]{8}) "
            r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
            r"use@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"consumed_width=1 value=zero definition_count=([0-9]+) "
            r"definitions=\(([^)]+)\) "
            r"basis=all_reaching_full_width_xor_self "
            r"mode_arg@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) value=zero"
        )
        for match in re.findall(
            zero_set_validation_pattern, row.gate_condition
        ):
            (
                function_text,
                register,
                use_text,
                use_off_text,
                count_text,
                definitions_text,
                mode_use_text,
                mode_use_off_text,
            ) = match
            function = int(function_text, 16)
            use_va = int(use_text, 16)
            use_off = int(use_off_text, 16)
            mode_use_va = int(mode_use_text, 16)
            mode_use_off = int(mode_use_off_text, 16)
            definition_pairs = tuple(
                (int(definition, 16), int(definition_off, 16))
                for definition, definition_off in re.findall(
                    r"definition@0x([0-9A-F]{8}) "
                    r"file_off=0x([0-9A-F]{8})",
                    definitions_text,
                )
            )
            definition_vas = tuple(
                definition for definition, _off in definition_pairs
            )
            decoded = analyzer.decode(function)
            lane = LOW8_BY_REG32.get(register)
            reaching = (
                analyzer._byte_reaching_definitions(function, lane)
                if lane is not None
                else analyzer._reaching_definitions(function, register)
            ).get(use_va, frozenset())
            if (
                len(definition_pairs) < 2
                or int(count_text) != len(definition_pairs)
                or definition_vas != tuple(sorted(set(definition_vas)))
                or definitions_text
                != ",".join(
                    "definition@0x%08X file_off=0x%08X" % pair
                    for pair in definition_pairs
                )
                or image.va_to_off(use_va) != use_off
                or use_va != mode_use_va
                or use_off != mode_use_off
                or any(
                    image.va_to_off(definition_va) != definition_off
                    for definition_va, definition_off in definition_pairs
                )
                or decoded is None
                or use_va not in decoded.instructions
                or any(
                    definition_va not in decoded.instructions
                    or not analyzer._is_full_width_zeroing_xor(
                        decoded.instructions[definition_va], register
                    )
                    for definition_va in definition_vas
                )
                or reaching != frozenset(definition_vas)
                or analyzer._mode_argument_all_zero_reaching_definitions(
                    function,
                    use_va,
                    Operand("reg", reg=register),
                    1,
                )
                != (register, definition_vas)
            ):
                raise ExtractionError(
                    "A2 mode zero reaching-set evidence mismatch at "
                    "VA 0x%08X" % use_va
                )
            zero_set_key = (
                function,
                use_va,
                register,
                definition_vas,
            )
            zero_set_evidence.add(zero_set_key)
            measured_zero_set_evidence.add(zero_set_key)
        identity_pattern = (
            r"formal_identity_lea@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"register=(eax|ecx|edx|ebx|ebp|esi|edi) "
            r"continuation@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"formal=entry\+0x([0-9A-F]+) "
            r"basis=full_width_zero_displacement"
        )
        for match in re.findall(identity_pattern, row.gate_condition):
            (
                definition_text,
                definition_off_text,
                function_text,
                register,
                continuation_text,
                continuation_off_text,
                formal_text,
            ) = match
            definition_va = int(definition_text, 16)
            definition_off = int(definition_off_text, 16)
            function = int(function_text, 16)
            continuation_va = int(continuation_text, 16)
            continuation_off = int(continuation_off_text, 16)
            formal = int(formal_text, 16)
            decoded = analyzer.decode(function)
            definition = (
                None
                if decoded is None
                else decoded.instructions.get(definition_va)
            )
            if (
                image.va_to_off(definition_va) != definition_off
                or image.va_to_off(continuation_va) != continuation_off
                or decoded is None
                or continuation_va not in decoded.instructions
                or definition is None
                or not analyzer._is_full_width_identity_lea(definition)
                or definition.dst is None
                or definition.dst.kind != "reg"
                or base_reg_name(definition.dst.reg) != register
                or definition.next_va != continuation_va
                or continuation_va
                not in decoded.successors.get(definition_va, ())
                or analyzer._formal_offsets(
                    function,
                    continuation_va,
                    Operand("reg", reg=register),
                )
                != frozenset((formal,))
            ):
                raise ExtractionError(
                    "A2 formal identity-LEA evidence mismatch at VA 0x%08X"
                    % definition_va
                )
            reaching_evidence.add(
                (
                    "full_width_identity_lea",
                    function,
                    continuation_va,
                    register,
                    definition_va,
                    formal,
                )
            )
        for path_va, path_off, target_va in re.findall(
            r"subcall_path@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"target=0x([0-9A-F]{8})",
            row.gate_condition,
        ):
            site = int(path_va, 16)
            off = int(path_off, 16)
            expected_target = int(target_va, 16)
            opcode = image.data[off]
            if opcode in (0xE8, 0xE9):
                relative = struct.unpack_from("<i", image.data, off + 1)[0]
                measured_target = (site + 5 + relative) & 0xFFFFFFFF
            elif opcode == 0xEB:
                relative = struct.unpack_from("<b", image.data, off + 1)[0]
                measured_target = (site + 2 + relative) & 0xFFFFFFFF
            else:
                measured_target = None
            if measured_target != expected_target:
                raise ExtractionError(
                    "A2 subcall path target mismatch at VA 0x%s" % path_va
                )
        stream_edges = set()
        stream_call_pattern = (
            r"stream_call@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"caller=0x([0-9A-F]{8}) target=0x([0-9A-F]{8}) "
            r"caller_formal=entry\+0x([0-9A-F]+) "
            r"target_formal=entry\+0x([0-9A-F]+)"
        )
        stream_arg_pattern = (
            r"stream_arg@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"caller=0x([0-9A-F]{8}) call=0x([0-9A-F]{8}) "
            r"target=0x([0-9A-F]{8}) caller_formal=entry\+0x([0-9A-F]+) "
            r"target_formal=entry\+0x([0-9A-F]+)"
        )
        stream_args = [
            tuple(int(value, 16) for value in match)
            for match in re.findall(stream_arg_pattern, row.gate_condition)
        ]
        for match in re.findall(stream_call_pattern, row.gate_condition):
            site, off, caller, target, caller_formal, target_formal = (
                int(value, 16) for value in match
            )
            decoded = analyzer.decode(caller)
            ins = None if decoded is None else decoded.instructions.get(site)
            if (
                image.va_to_off(site) != off
                or ins is None
                or ins.kind != "call"
                or ins.target != target
            ):
                raise ExtractionError(
                    "A2 stream call target mismatch at VA 0x%08X" % site
                )
            for function in (caller, target):
                expected_neutral_sites = {
                    int(fragment.split("@0x", 1)[1][:8], 16)
                    for fragment in analyzer._stack_neutral_import_fragments(
                        function
                    )
                }
                if not expected_neutral_sites.issubset(
                    neutral_sites_by_function.get(function, set())
                ):
                    raise ExtractionError(
                        "A2 stream call lacks stack-neutral import evidence"
                    )
                expected_stack_identity_sites = {
                    int(fragment.split("@0x", 1)[1][:8], 16)
                    for fragment in analyzer._stack_identity_lea_fragments(
                        function
                    )
                }
                if not expected_stack_identity_sites.issubset(
                    stack_identity_sites_by_function.get(function, set())
                ):
                    raise ExtractionError(
                        "A2 stream call lacks stack identity LEA evidence"
                    )
                expected_formal_base_sites = {
                    int(fragment.split("@0x", 1)[1][:8], 16)
                    for fragment in analyzer._stack_formal_base_fragments(
                        function
                    )
                }
                if not expected_formal_base_sites.issubset(
                    formal_base_sites_by_function.get(function, set())
                ):
                    raise ExtractionError(
                        "A2 stream call lacks stack formal base evidence"
                    )
            abi = analyzer.call_abi(decoded, ins, target)
            if abi is None:
                raise ExtractionError(
                    "A2 stream call ABI mismatch at VA 0x%08X" % site
                )
            argument_count = abi[1]
            sequences = recover_call_pushes(decoded, site, argument_count)
            effective_target_caps = analyzer.capabilities(target)
            refinement_prefix = (
                "local_capability_refinement function=0x%08X " % target
            )
            if refinement_prefix in row.gate_condition:
                refined_target_caps, refinement_fragment = (
                    analyzer._local_capability_refinement(target)
                )
                if (
                    refined_target_caps is None
                    or refinement_fragment not in row.gate_condition
                ):
                    raise ExtractionError(
                        "A2 stream call lacks local capability refinement "
                        "at VA 0x%08X" % site
                    )
                effective_target_caps = refined_target_caps
            if len(effective_target_caps) > 1:
                caller_abis = set()
                measured_function_abi = analyzer._function_abi(decoded)
                if measured_function_abi is not None:
                    caller_abis.add(measured_function_abi)
                for parent_match in re.findall(
                    stream_call_pattern, row.gate_condition
                ):
                    (
                        parent_site,
                        _parent_off,
                        parent_caller,
                        parent_target,
                        _parent_caller_formal,
                        _parent_target_formal,
                    ) = (int(value, 16) for value in parent_match)
                    if parent_target != caller:
                        continue
                    parent_decoded = analyzer.decode(parent_caller)
                    parent_ins = (
                        None
                        if parent_decoded is None
                        else parent_decoded.instructions.get(parent_site)
                    )
                    if parent_ins is None:
                        continue
                    parent_abi = analyzer.call_abi(
                        parent_decoded, parent_ins, caller
                    )
                    if parent_abi is not None:
                        caller_abis.add(parent_abi)
                if len(caller_abis) != 1:
                    raise ExtractionError(
                        "A2 stream call caller ABI is not unique at VA 0x%08X"
                        % site
                    )
                caller_abi = next(iter(caller_abis))
                proved, _proof_text, _proof_reason = (
                    analyzer._prove_direct_subcall_directions(
                        caller,
                        caller_abi,
                        RegisterResolver(decoded),
                        ins,
                        abi,
                        sequences,
                    )
                )
                if proved is None or row.direction not in proved:
                    raise ExtractionError(
                        "A2 stream call direction infeasible at VA 0x%08X"
                        % site
                    )
            source_index = argument_count - (target_formal // 4)
            if not sequences or not (0 <= source_index < argument_count):
                raise ExtractionError(
                    "A2 stream call formal range mismatch at VA 0x%08X" % site
                )
            selected = tuple(sequence[source_index] for sequence in sequences)
            expected_reaching = set()
            for argument in selected:
                origins, proof_keys = (
                    analyzer._formal_offsets_with_reaching_proof(
                    caller, argument.instruction_va, argument.operand
                )
                )
                if origins != frozenset((caller_formal,)):
                    raise ExtractionError(
                        "A2 stream call argument origin mismatch at VA 0x%08X"
                        % site
                    )
                expected_reaching.update(
                    analyzer._formal_reaching_evidence_keys(
                        caller_formal, proof_keys
                    )
                )
            if not expected_reaching.issubset(reaching_evidence):
                raise ExtractionError(
                    "A2 stream argument lacks reaching-definition evidence"
                )
            expected_arg_sites = {argument.instruction_va for argument in selected}
            emitted_arg_sites = {
                arg_site
                for (
                    arg_site,
                    arg_off,
                    arg_caller,
                    arg_call,
                    arg_target,
                    arg_caller_formal,
                    arg_target_formal,
                ) in stream_args
                if (
                    arg_caller,
                    arg_call,
                    arg_target,
                    arg_caller_formal,
                    arg_target_formal,
                )
                == (caller, site, target, caller_formal, target_formal)
                and image.va_to_off(arg_site) == arg_off
            }
            if emitted_arg_sites != expected_arg_sites:
                raise ExtractionError(
                    "A2 stream argument evidence mismatch at VA 0x%08X" % site
                )
            stream_edges.add((site, target))
        stream_tail_pattern = (
            r"stream_tail@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"caller=0x([0-9A-F]{8}) target=0x([0-9A-F]{8}) "
            r"caller_formal=entry\+0x([0-9A-F]+) "
            r"target_formal=entry\+0x([0-9A-F]+) mapping=stack_preserved"
        )
        for match in re.findall(stream_tail_pattern, row.gate_condition):
            site, off, caller, target, caller_formal, target_formal = (
                int(value, 16) for value in match
            )
            decoded = analyzer.decode(caller)
            ins = None if decoded is None else decoded.instructions.get(site)
            if (
                image.va_to_off(site) != off
                or ins is None
                or ins.kind != "jmp"
                or ins.target != target
                or caller_formal != target_formal
            ):
                raise ExtractionError(
                    "A2 tail stream mapping mismatch at VA 0x%08X" % site
                )
            for function in (caller, target):
                expected_neutral_sites = {
                    int(fragment.split("@0x", 1)[1][:8], 16)
                    for fragment in analyzer._stack_neutral_import_fragments(
                        function
                    )
                }
                if not expected_neutral_sites.issubset(
                    neutral_sites_by_function.get(function, set())
                ):
                    raise ExtractionError(
                        "A2 tail stream lacks stack-neutral import evidence"
                    )
                expected_stack_identity_sites = {
                    int(fragment.split("@0x", 1)[1][:8], 16)
                    for fragment in analyzer._stack_identity_lea_fragments(
                        function
                    )
                }
                if not expected_stack_identity_sites.issubset(
                    stack_identity_sites_by_function.get(function, set())
                ):
                    raise ExtractionError(
                        "A2 tail stream lacks stack identity LEA evidence"
                    )
                expected_formal_base_sites = {
                    int(fragment.split("@0x", 1)[1][:8], 16)
                    for fragment in analyzer._stack_formal_base_fragments(
                        function
                    )
                }
                if not expected_formal_base_sites.issubset(
                    formal_base_sites_by_function.get(function, set())
                ):
                    raise ExtractionError(
                        "A2 tail stream lacks stack formal base evidence"
                    )
            stream_edges.add((site, target))
        anchor_pattern = (
            r"(caller|target)_stream_anchor_([WR])@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) function=0x([0-9A-F]{8}) "
            r"primitive=0x([0-9A-F]{8}) "
            r"(caller_formal|target_formal)=entry\+0x([0-9A-F]+)"
        )
        target_anchor_keys = set()
        for (
            _role,
            direction,
            site_text,
            off_text,
            function_text,
            primitive_text,
            _formal_label,
            formal_text,
        ) in re.findall(anchor_pattern, row.gate_condition):
            site = int(site_text, 16)
            off = int(off_text, 16)
            function = int(function_text, 16)
            primitive = int(primitive_text, 16)
            formal = int(formal_text, 16)
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            expected_primitive = WRITE_VA if direction == "W" else READ_VA
            if (
                image.va_to_off(site) != off
                or primitive != expected_primitive
                or ins is None
                or ins.kind != "call"
                or ins.target != primitive
                or analyzer._formal_offsets(
                    function, site, Operand("reg", reg="ecx")
                )
                != frozenset((formal,))
            ):
                raise ExtractionError(
                    "A2 stream anchor mismatch at VA 0x%08X" % site
                )
            anchor_origins, anchor_proof_keys = (
                analyzer._formal_offsets_with_reaching_proof(
                    function, site, Operand("reg", reg="ecx")
                )
            )
            expected_reaching = analyzer._formal_reaching_evidence_keys(
                formal, anchor_proof_keys
            )
            if (
                anchor_origins != frozenset((formal,))
                or not expected_reaching.issubset(reaching_evidence)
            ):
                raise ExtractionError(
                    "A2 stream anchor lacks reaching-definition evidence"
                )
            if _role == "target":
                target_anchor_keys.add((direction, function, formal))
        for match in re.finditer(nested_stream_pattern, row.gate_condition):
            (
                direction,
                site_text,
                off_text,
                function_text,
                target_text,
                formal_text,
                child_formal_text,
                mode_formal_text,
                mode_value,
            ) = match.groups()
            site = int(site_text, 16)
            off = int(off_text, 16)
            function = int(function_text, 16)
            target = int(target_text, 16)
            formal = int(formal_text, 16)
            child_formal = int(child_formal_text, 16)
            mode_formal = int(mode_formal_text, 16)
            candidates = analyzer._target_stream_anchors(
                function, formal, direction
            )
            measured = tuple(
                evidence
                for candidate_direction, candidate_site, evidence in candidates
                if candidate_direction == direction and candidate_site == site
            )
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            abi = None if decoded is None else analyzer._function_abi(decoded)
            mode_proof = (
                None
                if abi is None
                else analyzer._unique_mode_formal_proof(function, abi)
            )
            expected_value = (
                "zero"
                if mode_proof is not None
                and mode_proof.zero_direction == direction
                else "nonzero"
                if mode_proof is not None
                and mode_proof.nonzero_direction == direction
                else None
            )
            nested_evidence = (
                ""
                if mode_proof is None
                else mode_proof.zero_anchor_evidence
                if expected_value == "zero"
                else mode_proof.nonzero_anchor_evidence
                if expected_value == "nonzero"
                else ""
            )
            evidence_formals = re.search(
                r"caller_stream_formal=entry\+0x([0-9A-F]+) "
                r"target_stream_formal=entry\+0x([0-9A-F]+)",
                nested_evidence,
            )
            if (
                image.va_to_off(site) != off
                or ins is None
                or ins.kind != "call"
                or ins.target != target
                or measured != (match.group(0),)
                or mode_proof is None
                or mode_proof.formal_offset != mode_formal
                or expected_value != mode_value
                or evidence_formals is None
                or int(evidence_formals.group(1), 16) != formal
                or int(evidence_formals.group(2), 16) != child_formal
            ):
                raise ExtractionError(
                    "A2 nested stream anchor mismatch at VA 0x%08X" % site
                )
            target_anchor_keys.add((direction, function, formal))
            measured_nested_stream_anchors.add(match.group(0))
        primitive_stream_pattern = (
            r"primitive_stream@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
            r"function=0x([0-9A-F]{8}) primitive=0x([0-9A-F]{8}) "
            r"stream_formal=entry\+0x([0-9A-F]+)"
        )
        for match in re.findall(primitive_stream_pattern, row.gate_condition):
            site, off, function, primitive, formal = (
                int(value, 16) for value in match
            )
            decoded = analyzer.decode(function)
            ins = None if decoded is None else decoded.instructions.get(site)
            if (
                image.va_to_off(site) != off
                or ins is None
                or ins.kind != "call"
                or ins.target != primitive
                or primitive not in (WRITE_VA, READ_VA)
                or analyzer._formal_offsets(
                    function, site, Operand("reg", reg="ecx")
                )
                != frozenset((formal,))
            ):
                raise ExtractionError(
                    "A2 primitive stream mismatch at VA 0x%08X" % site
                )
            primitive_origins, primitive_proof_keys = (
                analyzer._formal_offsets_with_reaching_proof(
                    function, site, Operand("reg", reg="ecx")
                )
            )
            expected_reaching = analyzer._formal_reaching_evidence_keys(
                formal, primitive_proof_keys
            )
            if (
                primitive_origins != frozenset((formal,))
                or not expected_reaching.issubset(reaching_evidence)
            ):
                raise ExtractionError(
                    "A2 primitive stream lacks reaching-definition evidence"
                )
        discovery_pattern = (
            r"stream_formal_discovery@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) caller=0x([0-9A-F]{8}) "
            r"target=0x([0-9A-F]{8}) "
            r"caller_formal=entry\+0x([0-9A-F]+) "
            r"target_formal=entry\+0x([0-9A-F]+) "
            r"directions=([WR](?:,[WR])*) "
            r"basis=directional_target_primitive"
        )
        discovered_tail_depths = set()
        for match in re.findall(discovery_pattern, row.gate_condition):
            (
                site_text,
                off_text,
                caller_text,
                target_text,
                caller_formal_text,
                target_formal_text,
                directions_text,
            ) = match
            site = int(site_text, 16)
            off = int(off_text, 16)
            caller = int(caller_text, 16)
            target = int(target_text, 16)
            caller_formal = int(caller_formal_text, 16)
            target_formal = int(target_formal_text, 16)
            directions = frozenset(directions_text.split(","))
            decoded = analyzer.decode(caller)
            ins = None if decoded is None else decoded.instructions.get(site)
            seed_formal, _seed_anchors, seed_reason = (
                analyzer._stream_formal_seed(caller)
            )
            if (
                image.va_to_off(site) != off
                or ins is None
                or ins.target != target
                or seed_formal is not None
                or seed_reason != "caller_stream_seed_absent"
                or ",".join(sorted(directions)) != directions_text
                or any(
                    (direction, target, target_formal)
                    not in target_anchor_keys
                    for direction in directions
                )
            ):
                raise ExtractionError(
                    "A2 stream formal discovery evidence mismatch at VA 0x%08X"
                    % site
                )
            if ins.kind == "call":
                abi = analyzer.call_abi(decoded, ins, target)
                sequences = (
                    ()
                    if abi is None
                    else recover_call_pushes(decoded, site, abi[1])
                )
                candidates = (
                    ()
                    if abi is None
                    else analyzer._discover_direct_stream_formals(
                        caller, ins, abi, sequences, directions
                    )
                )
                measured = {
                    (candidate_caller, candidate_target)
                    for (
                        candidate_caller,
                        candidate_target,
                        _selected,
                        _anchors,
                    ) in candidates
                }
                if measured != {(caller_formal, target_formal)}:
                    raise ExtractionError(
                        "A2 direct stream formal discovery is not unique at "
                        "VA 0x%08X" % site
                    )
                expected_edge = (
                    site,
                    off,
                    caller,
                    target,
                    caller_formal,
                    target_formal,
                )
                emitted_edges = {
                    tuple(int(value, 16) for value in item)
                    for item in re.findall(
                        stream_call_pattern, row.gate_condition
                    )
                }
                if expected_edge not in emitted_edges:
                    raise ExtractionError(
                        "A2 direct stream discovery lacks stream_call evidence"
                    )
            elif ins.kind == "jmp":
                candidates = analyzer._discover_tail_stream_formals(
                    caller, ins, directions
                )
                measured = {
                    candidate_formal
                    for candidate_formal, _anchors in candidates
                }
                if (
                    measured != {target_formal}
                    or caller_formal != target_formal
                ):
                    raise ExtractionError(
                        "A2 tail stream formal discovery is not unique at "
                        "VA 0x%08X" % site
                    )
                expected_edge = (
                    site,
                    off,
                    caller,
                    target,
                    caller_formal,
                    target_formal,
                )
                emitted_edges = {
                    tuple(int(value, 16) for value in item)
                    for item in re.findall(
                        stream_tail_pattern, row.gate_condition
                    )
                }
                if expected_edge not in emitted_edges:
                    raise ExtractionError(
                        "A2 tail stream discovery lacks stream_tail evidence"
                    )
                discovered_tail_depths.add((site, off, caller))
            else:
                raise ExtractionError(
                    "A2 stream formal discovery is not a direct edge"
                )
        tail_depth_pattern = (
            r"tail_stack_depth@0x([0-9A-F]{8}) "
            r"file_off=0x([0-9A-F]{8}) caller=0x([0-9A-F]{8}) depth=0"
        )
        emitted_tail_depths = {
            tuple(int(value, 16) for value in match)
            for match in re.findall(tail_depth_pattern, row.gate_condition)
        }
        for site, off, caller in emitted_tail_depths:
            if (
                image.va_to_off(site) != off
                or analyzer._stack_depths(caller).get(site)
                != frozenset((0,))
            ):
                raise ExtractionError(
                    "A2 tail stack depth evidence mismatch at VA 0x%08X" % site
                )
        if emitted_tail_depths != discovered_tail_depths:
            raise ExtractionError(
                "A2 tail stack depth evidence lacks formal discovery"
            )
        for match in re.findall(stream_call_pattern, row.gate_condition):
            _site, _off, _caller, target, _caller_formal, target_formal = (
                int(value, 16) for value in match
            )
            if (row.direction, target, target_formal) not in target_anchor_keys:
                raise ExtractionError(
                    "A2 stream call lacks direction-specific target anchor"
                )
        for match in re.findall(stream_tail_pattern, row.gate_condition):
            _site, _off, _caller, target, _caller_formal, target_formal = (
                int(value, 16) for value in match
            )
            if (row.direction, target, target_formal) not in target_anchor_keys:
                raise ExtractionError(
                    "A2 tail stream lacks direction-specific target anchor"
                )
        path_edges = {
            (int(site, 16), int(target, 16))
            for site, _off, target in re.findall(
                r"subcall_path@0x([0-9A-F]{8}) file_off=0x([0-9A-F]{8}) "
                r"target=0x([0-9A-F]{8})",
                row.gate_condition,
            )
        }
        if not path_edges.issubset(stream_edges):
            raise ExtractionError("A2 subcall path lacks stream provenance")
        if row.tag.startswith("SUBCALL:0x"):
            claim_va = image.off_to_va(row.file_off_claim)
            target = int(row.tag.split(":", 1)[1], 16)
            if (claim_va, target) not in stream_edges:
                raise ExtractionError("A2 SUBCALL row lacks local stream provenance")
        if "target_test@" in row.gate_condition and not all(
            fragment in row.gate_condition
            for fragment in (
                "direction_call@", "branch@", "formal=entry+", "zero=", "nonzero=",
                "width=", "zero_anchor@", "nonzero_anchor@", "paths=(",
            )
        ):
            raise ExtractionError("A2 direction proof is missing an evidence link")
        if "value=formal_forward" in row.gate_condition and not all(
            fragment in row.gate_condition
            for fragment in (
                "caller_test@", "caller_formal=entry+",
                "target_formal=entry+", "mapping=preserved",
            )
        ):
            raise ExtractionError("A2 formal forwarding proof is incomplete")
        indirect_direction_segments = [
            segment
            for segment in row.gate_condition.split(" AND ")
            if segment.startswith("indirect_direction_call@")
        ]
        if len(indirect_direction_segments) != row.gate_condition.count(
            "indirect_direction_call@"
        ):
            raise ExtractionError(
                "A2 malformed indirect direction proof segment"
            )
        if indirect_direction_segments:
            caller = row.span_start
            call_va = (
                None
                if row.file_off_claim is None
                else image.off_to_va(row.file_off_claim)
            )
            decoded = None if caller is None else analyzer.decode(caller)
            call = (
                None
                if decoded is None or call_va is None
                else decoded.instructions.get(call_va)
            )
            resolver = None if decoded is None else RegisterResolver(decoded)
            target_expr = (
                None
                if call is None
                or call.src is None
                or resolver is None
                else resolver.operand_before(
                    call.va,
                    call.src,
                    dereference=(call.src.kind == "mem"),
                )
            )
            sequences = (
                ()
                if decoded is None or call is None
                else recover_call_pushes(decoded, call.va, 2)
            )
            proved, canonical_proof, proof_reason = (
                (None, "", "call_unmapped")
                if decoded is None
                or call is None
                or resolver is None
                else analyzer._prove_indirect_serializer_directions(
                    caller,
                    analyzer._function_abi(decoded),
                    resolver,
                    call,
                    sequences,
                )
            )
            canonical_segments = canonical_proof.split(" AND ")
            gate_segments = row.gate_condition.split(" AND ")
            if (
                len(indirect_direction_segments) != 1
                or call is None
                or call_va != call.va
                or call.kind != "call_indirect"
                or target_expr is None
                or not is_proven_serializer_vtable_target(target_expr)
                or not sequences
                or proved != frozenset((row.direction,))
                or proof_reason
                or not canonical_proof
                or indirect_direction_segments[0]
                != canonical_segments[0]
                or any(
                    segment not in gate_segments
                    for segment in canonical_segments
                )
            ):
                raise ExtractionError(
                    "A2 indirect direction proof cannot be re-derived"
                )
        local_proof = local_direction_proof_segment(row)
        if local_proof is not None:
            expected_identity_zero_evidence.update(
                match.group(0)
                for match in re.finditer(
                    identity_zero_pattern, local_proof
                )
            )
        if local_proof is not None and "value=formal_forward" in local_proof:
            proof_pattern = (
                r"%s_test@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} "
                r"branch@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} "
                r"formal=entry\+0x([0-9A-F]+) zero=([WR]) "
                r"nonzero=([WR]) width=([124])"
            )
            target_match = re.search(proof_pattern % "target", local_proof)
            caller_match = re.search(proof_pattern % "caller", local_proof)
            forward_match = re.search(
                r"value=formal_forward caller_formal=entry\+0x([0-9A-F]+) "
                r"target_formal=entry\+0x([0-9A-F]+) width=([124]) "
                r"mapping=preserved",
                local_proof,
            )
            if (
                target_match is None
                or caller_match is None
                or forward_match is None
                or target_match.group(2, 3, 4)
                != caller_match.group(2, 3, 4)
                or (
                    caller_match.group(1),
                    target_match.group(1),
                    target_match.group(4),
                )
                != forward_match.groups()
            ):
                raise ExtractionError(
                    "A2 local formal forwarding mapping is inconsistent"
                )
        if local_proof is not None:
            local_width_match = re.search(
                r"target_test@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} "
                r"branch@0x[0-9A-F]{8} file_off=0x[0-9A-F]{8} "
                r"formal=entry\+0x[0-9A-F]+ zero=([WR]) "
                r"nonzero=([WR]) width=([124])",
                local_proof,
            )
            local_call_match = re.search(
                r"direction_call@0x([0-9A-F]{8}) "
                r"file_off=0x([0-9A-F]{8})",
                local_proof,
            )
            local_mode_sites = {
                int(site, 16)
                for site in re.findall(
                    r"mode_arg@0x([0-9A-F]{8}) "
                    r"file_off=0x[0-9A-F]{8}",
                    local_proof,
                )
            }
            if (
                local_width_match is None
                or local_call_match is None
                or not local_mode_sites
            ):
                raise ExtractionError(
                    "A2 local direction proof cannot be re-derived"
                )
            if int(local_width_match.group(3)) == 1:
                caller = row.span_start
                call_va = int(local_call_match.group(1), 16)
                call_off = int(local_call_match.group(2), 16)
                decoded = (
                    None if caller is None else analyzer.decode(caller)
                )
                call = (
                    None
                    if decoded is None
                    else decoded.instructions.get(call_va)
                )
                target_abi = (
                    None
                    if decoded is None
                    or call is None
                    or call.target is None
                    else analyzer.call_abi(decoded, call, call.target)
                )
                target_proof = (
                    None
                    if call is None
                    or call.target is None
                    or target_abi is None
                    else analyzer._unique_mode_formal_proof(
                        call.target, target_abi
                    )
                )
                source_index = (
                    -1
                    if target_abi is None or target_proof is None
                    else target_abi[1] - target_proof.formal_offset // 4
                )
                sequences = (
                    ()
                    if decoded is None
                    or call is None
                    or target_abi is None
                    else recover_call_pushes(decoded, call.va, target_abi[1])
                )
                if (
                    caller is None
                    or image.va_to_off(call_va) != call_off
                    or call is None
                    or call.kind != "call"
                    or target_proof is None
                    or target_proof.formal_width != 1
                    or not (0 <= source_index < target_abi[1])
                    or not sequences
                ):
                    raise ExtractionError(
                        "A2 byte-lane direction proof cannot be re-derived"
                    )
                if (
                    target_proof.predicate_evidence
                    and (
                        "predicate_zero=(%s)"
                        % target_proof.predicate_evidence
                    )
                    not in local_proof
                ):
                    raise ExtractionError(
                        "A2 target predicate zero evidence is not claim-linked"
                    )
                matched_mode_sites = set()
                local_expected = set()
                local_zero_keys = {
                    (
                        int(function_text, 16),
                        int(use_text, 16),
                        register,
                        int(definition_text, 16),
                    )
                    for (
                        definition_text,
                        _definition_off_text,
                        function_text,
                        register,
                        use_text,
                        _use_off_text,
                        _mode_use_text,
                        _mode_use_off_text,
                    ) in re.findall(zero_reaching_pattern, local_proof)
                }
                local_zero_set_keys = set()
                for set_match in re.findall(
                    zero_set_validation_pattern, local_proof
                ):
                    (
                        function_text,
                        register,
                        use_text,
                        _use_off_text,
                        _count_text,
                        definitions_text,
                        _mode_use_text,
                        _mode_use_off_text,
                    ) = set_match
                    definition_vas = tuple(
                        int(definition, 16)
                        for definition, _definition_off in re.findall(
                            r"definition@0x([0-9A-F]{8}) "
                            r"file_off=0x([0-9A-F]{8})",
                            definitions_text,
                        )
                    )
                    local_zero_set_keys.add(
                        (
                            int(function_text, 16),
                            int(use_text, 16),
                            register,
                            definition_vas,
                        )
                    )
                local_zero_sites = {key[1] for key in local_zero_keys}
                local_zero_set_sites = {
                    key[1] for key in local_zero_set_keys
                }
                derived_local_zero_keys = set()
                derived_local_zero_set_keys = set()
                for sequence in sequences:
                    argument = sequence[source_index]
                    if argument.instruction_va not in local_mode_sites:
                        continue
                    matched_mode_sites.add(argument.instruction_va)
                    origins, proof_keys = (
                        analyzer._mode_argument_formal_offsets_with_reaching_proof(
                            caller,
                            argument.instruction_va,
                            argument.operand,
                            1,
                        )
                    )
                    if proof_keys and len(origins) != 1:
                        raise ExtractionError(
                            "A2 byte-lane mode argument is not singleton"
                        )
                    if proof_keys:
                        local_expected.update(
                            analyzer._formal_reaching_evidence_keys(
                                next(iter(origins)), proof_keys
                            )
                        )
                    if argument.instruction_va in local_zero_sites:
                        zero_reaching = (
                            analyzer._mode_argument_zero_reaching_definition(
                                caller,
                                argument.instruction_va,
                                argument.operand,
                                1,
                            )
                        )
                        if zero_reaching is None:
                            raise ExtractionError(
                                "A2 mode zero argument cannot be re-derived"
                            )
                        register, definition_va = zero_reaching
                        derived_local_zero_keys.add(
                            (
                                caller,
                                argument.instruction_va,
                                register,
                                definition_va,
                            )
                        )
                    if argument.instruction_va in local_zero_set_sites:
                        zero_reaching_set = (
                            analyzer._mode_argument_all_zero_reaching_definitions(
                                caller,
                                argument.instruction_va,
                                argument.operand,
                                1,
                            )
                        )
                        if (
                            zero_reaching_set is None
                            or len(zero_reaching_set[1]) < 2
                        ):
                            raise ExtractionError(
                                "A2 mode zero-set argument cannot be "
                                "re-derived"
                            )
                        register, definition_vas = zero_reaching_set
                        derived_local_zero_set_keys.add(
                            (
                                caller,
                                argument.instruction_va,
                                register,
                                definition_vas,
                            )
                        )
                if (
                    matched_mode_sites != local_mode_sites
                    or not local_expected.issubset(reaching_evidence)
                ):
                    raise ExtractionError(
                        "A2 byte-lane mode argument lacks reaching evidence"
                    )
                if (
                    derived_local_zero_keys != local_zero_keys
                    or not local_zero_keys.issubset(zero_reaching_evidence)
                    or derived_local_zero_set_keys != local_zero_set_keys
                    or not local_zero_set_keys.issubset(
                        zero_set_evidence
                    )
                    or (
                        (local_zero_keys or local_zero_set_keys)
                        and row.direction != local_width_match.group(1)
                    )
                ):
                    raise ExtractionError(
                        "A2 mode zero proof is not locally claim-linked"
                    )
                expected_byte_reaching_evidence.update(
                    key
                    for key in local_expected
                    if key[0] == "unique_byte_lane_reaching_definition"
                )
                expected_zero_reaching_evidence.update(local_zero_keys)
                expected_zero_set_evidence.update(local_zero_set_keys)
        if row.span_sha256 != "UNKNOWN":
            if row.span_start is None or row.span_end is None:
                raise ExtractionError("hashed A2 row has UNKNOWN span")
            start_off = image.va_to_off(row.span_start)
            end_last_off = image.va_to_off(row.span_end - 1)
            if start_off is None or end_last_off is None:
                raise ExtractionError("A2 span is outside mapped image")
            got = hashlib.sha256(
                image.data[start_off : end_last_off + 1]
            ).hexdigest()
            if got != row.span_sha256:
                raise ExtractionError(
                    "A2 span hash mismatch at 0x%08X" % row.span_start
                )
            if not (start_off <= row.file_off_claim < end_last_off + 1):
                raise ExtractionError(
                    "A2 claim offset is outside its measured span at 0x%08X"
                    % row.span_start
                )
    register_import_keys = {
        (
            int(match.group(3), 16),
            int(match.group(1), 16),
            match.group(4),
            int(match.group(5), 16),
            int(match.group(7), 16),
        )
        for evidence in measured_register_import_evidence
        for match in (re.fullmatch(register_neutral_pattern, evidence),)
        if match is not None
    }
    essential_register_import_keys = {
        (0x00627730, 0x006277E6, "ebp", 0x006277DC, 0x00C3B4C0),
        (0x006BD210, 0x006BD453, "ebx", 0x006BD432, 0x00C3B4C0),
        (0x006E8150, 0x006E81DD, "ebp", 0x006E81D3, 0x00C3B4C0),
        (0x006EBD50, 0x006EBDC4, "ebp", 0x006EBDBA, 0x00C3B4C0),
        (0x0073E240, 0x0073E2B3, "ebp", 0x0073E2A9, 0x00C3B4C0),
    }
    if (
        len(measured_register_import_evidence) != 57
        or not essential_register_import_keys.issubset(register_import_keys)
        or sum(
            row.gate_condition.count("stack_neutral_register_import@")
            for row in rows
        )
        != 8882
    ):
        raise ExtractionError(
            "A2 register-indirect stack-neutral import census mismatch"
        )
    stack_identity_keys = {
        (int(match.group(3), 16), int(match.group(1), 16))
        for evidence in measured_stack_identity_evidence
        for match in (re.fullmatch(stack_identity_pattern, evidence),)
        if match is not None
    }
    if (
        stack_identity_keys
        != {
            (0x00623800, 0x00623939),
            (0x00645860, 0x00645989),
            (0x00694820, 0x00694879),
            (0x006BBFD0, 0x006BC119),
            (0x00713910, 0x00713979),
            (0x0076A740, 0x0076A7C9),
        }
        or sum(
            row.gate_condition.count("stack_identity_lea@") for row in rows
        )
        != 286
    ):
        raise ExtractionError("A2 stack identity LEA census mismatch")
    getid_stack_keys = {
        (
            int(match.group(3), 16),
            int(match.group(1), 16),
            match.group(4),
            int(match.group(5), 16),
        )
        for evidence in measured_getid_stack_evidence
        for match in (re.fullmatch(getid_stack_pattern, evidence),)
        if match is not None
    }
    all_getid_stack_keys = {
        (function, ins.va, proof[0], proof[1])
        for function, decoded in analyzer.decode_cache.items()
        if decoded is not None
        for ins in decoded.instructions.values()
        for proof in (
            analyzer._stack_neutral_vtable_getid(function, ins),
        )
        if proof is not None
    }
    if (
        getid_stack_keys
        != {
            (0x005E3320, 0x005E33E1, "edx", 0x005E33DE),
            (0x005E3540, 0x005E3579, "edx", 0x005E3576),
            (0x005F38F0, 0x005F395E, "eax", 0x005F395B),
            (0x005F3E20, 0x005F3F08, "eax", 0x005F3F05),
        }
        or all_getid_stack_keys
        != {
            (0x00463720, 0x0046375D, "edx", 0x0046375A),
            (0x005E3320, 0x005E33E1, "edx", 0x005E33DE),
            (0x005E3540, 0x005E3579, "edx", 0x005E3576),
            (0x005EF160, 0x005EF276, "eax", 0x005EF273),
            (0x005F38F0, 0x005F395E, "eax", 0x005F395B),
            (0x005F3E20, 0x005F3F08, "eax", 0x005F3F05),
        }
        or sum(
            row.gate_condition.count("stack_neutral_vtable_getid@")
            for row in rows
        )
        != 157
    ):
        raise ExtractionError("A2 GetId vtable stack census mismatch")
    indirect_mode_source_keys = {
        (
            int(match.group(5), 16),
            int(match.group(1), 16),
            int(match.group(3), 16),
            match.group(6),
            int(match.group(9), 16),
        )
        for evidence in measured_indirect_mode_sources
        for match in (re.fullmatch(indirect_mode_source_pattern, evidence),)
        if match is not None
    }
    if (
        indirect_mode_source_keys
        != {
            (0x005E3320, 0x005E3413, 0x005E341C, "eax", 0x8),
            (0x005E3540, 0x005E35AB, 0x005E35B4, "eax", 0x8),
        }
        or sum(
            row.gate_condition.count("indirect_mode_formal_source ")
            for row in rows
        )
        != 2
    ):
        raise ExtractionError("A2 indirect mode source census mismatch")
    direct_infeasible_cases = {
        (0x005DF250, "R"): (
            0x005DF2A0,
            0x001DE6A0,
            0x005F3490,
            "nonzero",
            "W",
            0x005DF250,
            0x001DE650,
            0x005DF25F,
            0x001DE65F,
            0x005DF2B5,
            0x001DE6B5,
            0x005DF269,
            0x001DE669,
        ),
        (0x005DF250, "W"): (
            0x005DF2EC,
            0x001DE6EC,
            0x005F34D0,
            "zero",
            "R",
            0x005DF250,
            0x001DE650,
            0x005DF25F,
            0x001DE65F,
            0x005DF2B5,
            0x001DE6B5,
            0x005DF269,
            0x001DE669,
        ),
        (0x005F85B0, "R"): (
            0x005F86D5,
            0x001F7AD5,
            0x005F3490,
            "nonzero",
            "W",
            0x005F85DD,
            0x001F79DD,
            0x005F85E8,
            0x001F79E8,
            0x005F8728,
            0x001F7B28,
            0x005F85FF,
            0x001F79FF,
        ),
        (0x005F85B0, "W"): (
            0x005F87CC,
            0x001F7BCC,
            0x005F34D0,
            "zero",
            "R",
            0x005F85DD,
            0x001F79DD,
            0x005F85E8,
            0x001F79E8,
            0x005F8728,
            0x001F7B28,
            0x005F85FF,
            0x001F79FF,
        ),
        (0x00626900, "R"): (
            0x0062698E,
            0x00225D8E,
            0x005F3490,
            "nonzero",
            "W",
            0x0062690F,
            0x00225D0F,
            0x00626911,
            0x00225D11,
            0x006269CC,
            0x00225DCC,
            0x0062691F,
            0x00225D1F,
        ),
        (0x00626900, "W"): (
            0x00626A3B,
            0x00225E3B,
            0x005F34D0,
            "zero",
            "R",
            0x0062690F,
            0x00225D0F,
            0x00626911,
            0x00225D11,
            0x006269CC,
            0x00225DCC,
            0x0062691F,
            0x00225D1F,
        ),
    }
    measured_direct_infeasible_cases = set()
    for (caller, allowed_direction), expected in sorted(
        direct_infeasible_cases.items()
    ):
        (
            site,
            site_off,
            target,
            branch_value,
            branch_direction,
            test_va,
            test_off,
            branch_va,
            branch_off,
            zero_anchor_va,
            zero_anchor_off,
            nonzero_anchor_va,
            nonzero_anchor_off,
        ) = expected
        decoded = analyzer.decode(caller)
        abi = None if decoded is None else analyzer._function_abi(decoded)
        proof = (
            None
            if abi is None
            else analyzer._unique_mode_formal_proof(caller, abi)
        )
        ins = None if decoded is None else decoded.instructions.get(site)
        events = analyzer.extract_events(
            caller, allowed=frozenset((allowed_direction,))
        )
        matches = [
            event
            for event in events
            if event.site_va == site and event.tag == "DIRECTION_INFEASIBLE"
        ]
        proof_fragment = (
            "" if proof is None else analyzer._mode_proof_fragment("caller", proof)
        )
        marker = (
            "infeasible_direction_call@0x%08X file_off=0x%08X "
            "branch_value=%s branch_direction=%s allowed=%s %s"
            % (
                site,
                site_off,
                branch_value,
                branch_direction,
                allowed_direction,
                proof_fragment,
            )
        )
        expected_nodes = (
            frozenset((site,))
            if branch_value == "zero"
            else frozenset()
        )
        opposite_nodes = (
            frozenset((site,))
            if branch_value == "nonzero"
            else frozenset()
        )
        if (
            decoded is None
            or abi != ("thiscall", 2)
            or ins is None
            or ins.kind != "call"
            or ins.target != target
            or image.va_to_off(site) != site_off
            or analyzer.capabilities(target)
            != frozenset((branch_direction,))
            or proof is None
            or proof.formal_offset != 0x8
            or proof.formal_width != 1
            or proof.test_va != test_va
            or proof.test_off != test_off
            or proof.branch_va != branch_va
            or proof.branch_off != branch_off
            or proof.zero_direction != "R"
            or proof.nonzero_direction != "W"
            or proof.zero_anchor_va != zero_anchor_va
            or proof.zero_anchor_off != zero_anchor_off
            or proof.nonzero_anchor_va != nonzero_anchor_va
            or proof.nonzero_anchor_off != nonzero_anchor_off
            or proof.zero_anchor_evidence
            or proof.nonzero_anchor_evidence
            or (frozenset((site,)) & proof.zero_nodes) != expected_nodes
            or (frozenset((site,)) & proof.nonzero_nodes) != opposite_nodes
            or len(matches) != 1
            or matches[0].directions
            or matches[0].target_va != target
            or matches[0].reason
            != "subcall_direction_infeasible target=0x%08X" % target
            or marker not in matches[0].gate_condition
        ):
            raise ExtractionError(
                "direct singleton infeasible-direction proof mismatch at "
                "VA 0x%08X" % site
            )
        measured_direct_infeasible_cases.add((caller, allowed_direction))
    if measured_direct_infeasible_cases != set(direct_infeasible_cases):
        raise ExtractionError(
            "direct singleton infeasible-direction census mismatch"
        )
    if len(measured_predicate_zero_proofs) != 2:
        raise ExtractionError("A2 predicate zero evidence census mismatch")
    expected_local_capability_functions = {
        0x006EBD50,
        0x006EC050,
        0x0073E240,
        0x0073E6F0,
    }
    measured_local_capability_functions = {
        int(match.group(1), 16)
        for fragment in measured_local_capability_refinements
        for match in (re.fullmatch(local_capability_pattern, fragment),)
        if match is not None
    }
    if (
        len(measured_local_capability_refinements) != 4
        or measured_local_capability_functions
        != expected_local_capability_functions
    ):
        raise ExtractionError("A2 local capability refinement census mismatch")
    if (
        len(measured_identity_zero_evidence) != 3
        or measured_identity_zero_evidence
        != expected_identity_zero_evidence
    ):
        raise ExtractionError(
            "A2 identity-LEA zero evidence is not claim-linked"
        )
    if len(measured_nested_mode_anchors) != 2:
        raise ExtractionError("A2 nested mode evidence census mismatch")
    if len(measured_nested_stream_anchors) != 2:
        raise ExtractionError("A2 nested stream evidence census mismatch")
    if measured_byte_reaching_evidence != expected_byte_reaching_evidence:
        raise ExtractionError(
            "A2 byte-lane reaching evidence is not claim-linked"
        )
    if measured_zero_reaching_evidence != expected_zero_reaching_evidence:
        raise ExtractionError(
            "A2 mode zero reaching evidence is not claim-linked"
        )
    if measured_zero_set_evidence != expected_zero_set_evidence:
        raise ExtractionError(
            "A2 mode zero reaching-set evidence is not claim-linked"
        )
    for key, values in orders.items():
        expected = list(range(1, len(values) + 1))
        if values != expected:
            raise ExtractionError("A2 order is not contiguous for %r" % (key,))

    numeric_re = re.compile(r"0x[0-9A-F]{2}")

    used_vas = {
        row.span_start
        for row in rows
        if row.span_start is not None and row.span_sha256 != "UNKNOWN"
    }
    used_spans = [analyzer.span(va) for va in used_vas]
    if any(span is None for span in used_spans):
        raise ExtractionError("A2 used function lacks a measured span")
    unsafe_other = sorted(
        ins.va
        for va in used_vas
        for ins in analyzer.decode(va).instructions.values()
        if ins.kind == "other" and not analyzer._other_has_no_gpr_write(ins)
    )
    if unsafe_other:
        raise ExtractionError(
            "A2 used span contains an unmodelled GPR-write risk at 0x%08X"
            % unsafe_other[0]
        )
    raw_unique = {
        (site, target)
        for span in used_spans
        for site, target in raw_rel32_calls(image, span)
        if target in (WRITE_VA, READ_VA)
    }
    decoded_unique = {
        (ins.va, ins.target)
        for va in used_vas
        for ins in analyzer.decode(va).instructions.values()
        if ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
    }
    if raw_unique != decoded_unique:
        raise ExtractionError(
            "raw/decoded primitive union mismatch: raw=%d decoded=%d missing=%d"
            % (
                len(raw_unique),
                len(decoded_unique),
                len(raw_unique - decoded_unique),
            )
        )

    for item in registry:
        if item.serializer_va is None:
            continue
        decoded = analyzer.decode(item.serializer_va)
        if decoded is None:
            raise ExtractionError(
                "root serializer span missing at 0x%08X" % item.serializer_va
            )
        expected = Counter(
            "W" if ins.target == WRITE_VA else "R"
            for ins in decoded.instructions.values()
            if ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
        )
        actual = Counter(
            row.direction
            for row in by_message[item.name]
            if row.span_start == item.serializer_va and numeric_re.fullmatch(row.tag)
        )
        if actual != expected:
            raise ExtractionError(
                "direct primitive coverage mismatch for %s: expected %r got %r"
                % (item.name, expected, actual)
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, default=default_image_path())
    parser.add_argument("--inspect-a1", action="store_true")
    parser.add_argument("--inspect-a2", action="store_true")
    args = parser.parse_args(argv)

    image = Image(args.image.resolve())
    print("image_sha256_before=%s" % image.sha256)
    rows = scan_registry(image)
    if len(rows) != 519:
        raise ExtractionError("registration count mismatch: expected 519, got %d" % len(rows))
    validate_registry_acceptance(image, rows)

    by_name = {row.name: row for row in rows}
    pickup = by_name.get("PickupTerrainThing")
    runtime = by_name.get("GSCN_RunTimeProtocolRes")
    expected_pickup = (
        0x00F3093C,
        0x00BEE5E0,
        0x0108202C,
        0x005E46A0,
        0x00F3005C,
        0x005E5E30,
        0x005EF640,
    )
    got_pickup = None if pickup is None else (
        pickup.name_va,
        pickup.reg_site_va,
        pickup.id_global_va,
        pickup.getter_va,
        pickup.vtable_va,
        pickup.serializer_va,
        pickup.handler_va,
    )
    if got_pickup != expected_pickup:
        raise ExtractionError("PickupTerrainThing acceptance mismatch: %r" % (got_pickup,))
    if runtime is None or runtime.vtable_va != 0x00F2FFC0 or runtime.serializer_va != 0x005E3EE0 or runtime.handler_va != 0x005E4060:
        raise ExtractionError("GSCN_RunTimeProtocolRes acceptance mismatch")

    if args.inspect_a1:
        print("protocol_rows=%d" % len(rows))
        print("getter_unknown=%d" % sum(row.getter_va is None for row in rows))
        print("vtable_unknown=%d" % sum(row.vtable_va is None for row in rows))
        print("serializer_unknown=%d" % sum(row.serializer_va is None for row in rows))
        print("handler_unknown=%d" % sum(row.handler_va is None for row in rows))
        after_hash = file_sha256(args.image.resolve())
        if after_hash != image.sha256:
            raise ExtractionError("image hash changed during A1 inspection")
        print("image_sha256_after=%s" % after_hash)
        return 0

    if args.inspect_a2:
        serializers = sorted({row.serializer_va for row in rows if row.serializer_va is not None})
        spans = {va: find_function_span(image, va) for va in serializers}
        missing = [va for va, span in spans.items() if span is None]
        calls = {
            va: raw_rel32_calls(image, span)
            for va, span in spans.items()
            if span is not None
        }
        decodes = {
            va: decode_function(image, span)
            for va, span in spans.items()
            if span is not None
        }
        decoded_primitive_sites = {
            (ins.va, ins.target)
            for _va, decoded in decodes.items()
            for ins in decoded.instructions.values()
            if ins.kind == "call" and ins.target in (WRITE_VA, READ_VA)
        }
        raw_primitive_sites = {
            (site, target)
            for _va, items in calls.items()
            for site, target in items
            if target in (WRITE_VA, READ_VA)
        }
        print("serializer_rows=%d" % sum(row.serializer_va is not None for row in rows))
        print("unique_serializers=%d" % len(serializers))
        print("span_unknown=%d" % len(missing))
        print("raw_write_calls=%d" % sum(target == WRITE_VA for items in calls.values() for _site, target in items))
        print("raw_read_calls=%d" % sum(target == READ_VA for items in calls.values() for _site, target in items))
        print("serializers_with_direct_primitive=%d" % sum(any(target in (WRITE_VA, READ_VA) for _site, target in items) for items in calls.values()))
        print("decode_error_functions=%d" % sum(bool(decoded.errors) for decoded in decodes.values()))
        print("raw_primitive_not_decoded=%d" % len(raw_primitive_sites - decoded_primitive_sites))
        print("decoded_primitive_not_raw=%d" % len(decoded_primitive_sites - raw_primitive_sites))
        push_stats = Counter()
        for _va, decoded in decodes.items():
            for ins in decoded.instructions.values():
                if ins.kind != "call" or ins.target not in (WRITE_VA, READ_VA):
                    continue
                sequences = recover_call_pushes(decoded, ins.va, 3)
                label = "W" if ins.target == WRITE_VA else "R"
                if len(sequences) != 1:
                    push_stats[label + "_sequence_count_" + str(len(sequences))] += 1
                elif (
                    sequences[0][0].operand.kind == "imm"
                    and sequences[0][1].operand.kind != "imm"
                    and sequences[0][2].operand.kind == "imm"
                ):
                    push_stats[label + "_decoded"] += 1
                else:
                    push_stats[label + "_shape_mismatch"] += 1
        for key in sorted(push_stats):
            print("push_%s=%d" % (key.lower(), push_stats[key]))
        expression_stats = Counter()
        expression_examples: dict[str, list[str]] = defaultdict(list)
        for va, decoded in decodes.items():
            resolver = RegisterResolver(decoded)
            for ins in decoded.instructions.values():
                if ins.kind != "call" or ins.target not in (WRITE_VA, READ_VA):
                    continue
                sequences = recover_call_pushes(decoded, ins.va, 3)
                if len(sequences) != 1:
                    continue
                ptr_arg = sequences[0][1]
                expr = resolver.operand_before(
                    ptr_arg.instruction_va,
                    ptr_arg.operand,
                    dereference=(ptr_arg.operand.kind == "mem"),
                )
                field_text = field_offset_from_expr(expr)
                category = (
                    "simple"
                    if re.fullmatch(r"[+-]0x[0-9A-F]+", field_text)
                    else "stack"
                    if field_text.startswith("STACK")
                    else "unknown"
                    if "UNKNOWN" in field_text
                    else "phi"
                    if field_text.startswith("PHI")
                    else "dynamic"
                )
                expression_stats[category] += 1
                if len(expression_examples[category]) < 8:
                    expression_examples[category].append(
                        "0x%08X=%s" % (ins.va, field_text)
                    )
        for key in sorted(expression_stats):
            print("field_expr_%s=%d" % (key, expression_stats[key]))
            print("field_expr_%s_examples=%s" % (key, ",".join(expression_examples[key])))
        if missing:
            print("span_unknown_vas=" + ",".join("0x%08X" % va for va in missing))
        bad_decode = [va for va, decoded in decodes.items() if decoded.errors]
        if bad_decode:
            print("decode_error_vas=" + ",".join("0x%08X" % va for va in bad_decode))
        after_hash = file_sha256(args.image.resolve())
        if after_hash != image.sha256:
            raise ExtractionError("image hash changed during A2 inspection")
        print("image_sha256_after=%s" % after_hash)
        return 0


    analyzer = SerializerAnalyzer(image, rows)
    validate_pe_security_cookie_check_helper_definitions(image)
    validate_exact_import_thunk_call_definitions(image)
    validate_exact_direct_import_call_definitions(image)
    validate_exact_singleton_register_import_call_definitions(image)
    validate_exact_multi_register_import_call_definitions(image)
    validate_ecx_plus_50_tail_jump_helper_definitions(image, analyzer)
    validate_nested_call_composition_helper_definitions(image, analyzer)
    validate_locked_mutable_dword_slot_update_helper_definitions(
        image, analyzer
    )
    validate_mutable_pointer_slot_traversal_helper_definitions(
        image, analyzer
    )
    validate_mutable_dword_slot_operation_helper_definitions(image, analyzer)
    validate_mutable_dword_range_growth_helper_definitions(image, analyzer)
    validate_critical_section_pointer_helper_definitions(image, analyzer)
    validate_locked_mutable_pointer_slot_helper_definitions(image, analyzer)
    validate_mutable_chain_helper_definitions(image, analyzer)
    validate_pure_chain_helper_definitions(image, analyzer)
    validate_atomic_object_helper_definitions(image, analyzer)
    validate_string_wire_helper_definitions(image, analyzer)
    field_rows = build_field_rows(rows, analyzer)
    validate_pe_security_cookie_check_helper_rows(
        image, analyzer, field_rows
    )
    validate_exact_import_thunk_call_rows(image, analyzer, field_rows)
    validate_exact_direct_import_call_rows(image, analyzer, field_rows)
    validate_other_exact_direct_import_call_rows(image, analyzer, field_rows)
    validate_exact_singleton_register_import_call_rows(
        image, analyzer, field_rows
    )
    validate_exact_multi_register_import_call_rows(
        image, analyzer, field_rows
    )
    validate_ecx_plus_50_tail_jump_helper_rows(
        image, analyzer, field_rows
    )
    validate_nested_call_composition_helper_rows(
        image, analyzer, field_rows
    )
    validate_locked_mutable_dword_slot_update_helper_rows(
        image, analyzer, field_rows
    )
    validate_mutable_pointer_slot_traversal_helper_rows(
        image, analyzer, field_rows
    )
    validate_mutable_dword_slot_operation_helper_rows(
        image, analyzer, field_rows
    )
    validate_mutable_dword_range_growth_helper_rows(
        image, analyzer, field_rows
    )
    validate_critical_section_pointer_helper_rows(
        image, analyzer, field_rows
    )
    validate_locked_mutable_pointer_slot_helper_rows(
        image, analyzer, field_rows
    )
    validate_mutable_chain_helper_rows(image, analyzer, field_rows)
    validate_pure_chain_helper_rows(image, analyzer, field_rows)
    validate_atomic_object_helper_rows(image, analyzer, field_rows)
    validate_string_wire_helper_rows(image, analyzer, field_rows)
    validate_field_acceptance(field_rows)
    validate_analysis(image, rows, analyzer, field_rows)
    validate_static_blocker_report_evidence(image, field_rows)
    registry_tsv = build_registry_tsv(rows, image)
    fields_tsv = build_fields_tsv(field_rows)
    census_tsv, census_rows = build_tag_census(field_rows)
    source_artifacts = (
        ("PF_PROTOCOL_REGISTRY.tsv", registry_tsv, len(rows)),
        ("PF_SERIALIZER_FIELDS.tsv", fields_tsv, len(field_rows)),
        ("PF_TAG_CENSUS.tsv", census_tsv, census_rows),
    )
    for artifact_name, artifact_text, artifact_rows in source_artifacts:
        validate_tsv_source_contract(
            artifact_name,
            artifact_text,
            artifact_rows,
            STATIC_EVIDENCE_SOURCE,
        )
    validate_source_contract_mutation_regressions(source_artifacts)

    out_dir = Path(__file__).resolve().parent
    write_utf8(out_dir / "PF_PROTOCOL_REGISTRY.tsv", registry_tsv)
    write_utf8(out_dir / "PF_PROTOCOL_REGISTRY.md", build_registry_md(rows, image))
    write_utf8(out_dir / "PF_SERIALIZER_FIELDS.tsv", fields_tsv)
    write_utf8(out_dir / "PF_SERIALIZER_FIELDS.md", build_fields_md(rows, field_rows, image))
    write_utf8(out_dir / "PF_TAG_CENSUS.tsv", census_tsv)

    after_hash = file_sha256(args.image.resolve())
    if after_hash != image.sha256:
        raise ExtractionError(
            "image hash changed during extraction: before %s, after %s"
            % (image.sha256, after_hash)
        )
    write_utf8(
        out_dir / "PF_EXTERNAL_REPORT.md",
        build_report(rows, field_rows, image.sha256, after_hash),
    )

    unknown_messages, _reasons = unknown_summary(field_rows)
    numeric_fields = sum(
        bool(re.fullmatch(r"0x[0-9A-F]{2}", row.tag)) for row in field_rows
    )
    print("PF_PROTOCOL_REGISTRY.tsv rows=%d" % len(rows))
    print("PF_SERIALIZER_FIELDS.tsv rows=%d" % len(field_rows))
    print("PF_SERIALIZER_FIELDS.numeric_rows=%d" % numeric_fields)
    print("PF_TAG_CENSUS.tsv rows=%d" % census_rows)
    print("serializer_success=%d" % (len(rows) - len(unknown_messages)))
    print("serializer_unknown=%d" % len(unknown_messages))
    print("image_sha256_after=%s" % after_hash)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ExtractionError as exc:
        sys.stderr.write("ERROR: %s\n" % exc)
        raise SystemExit(1)
