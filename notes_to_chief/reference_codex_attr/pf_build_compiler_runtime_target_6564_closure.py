#!/usr/bin/env python3
"""Build the reviewed IMAGE-only compiler/container non-wire overlays.

This generator is deliberately additive.  It never edits a frozen table.  It
selects only effective source rows, proves their exact IMAGE provenance, rejects
base-row overlap with every older overlay, and writes removal/status directives.

The invalid-parameter scope is intentionally narrow: only guard calls inside the
five pinned serializers that also reach the fully pinned 0x006564E0/0x00656C50/
0x006FDB40 container graph are eligible.  CBuffConditionState additionally reaches
the separately pinned 0x00656690 recursive node-delete graph.  The remaining exact
import rows retain their prior blocker; an import name by itself is not a global
non-wire proof.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import struct
import sys
import tempfile
import types
from collections import deque
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable, Mapping, Sequence


IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
A2_SHA256 = "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
SLOT34_A2_SHA256 = "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334"
POST_V1_SHA256 = "96e5a476baad2b0ceda79b2ef47bc5a85189551f76003139e1be4cd034f5afc2"
PRIORITY_SHA256 = "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"
SLOT34_PRIORITY_SHA256 = "00ef0f3cb632b40ba168ce79bbd656fc7a6936a55f3b3e185c6e63b32c39ec5d"
DECODER_SHA256 = "0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e"
V2_VALIDATOR_SHA256 = "7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9"
POST_PRIORITY_SHA256 = "69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51"
PRIORITY_POOL_638690_SHA256 = "cc585d983dd1ca155ea1cfcfc59116897b59d2ce2455dc96f1d4097e9d7afdd5"
PRIORITY_POOL_661FA0_SHA256 = "3ba436e9b4876a1575a6d5544f49bb462896e2c6ae4191e085eacb56788ef880"
PRIORITY_POOL_46F4D0_SHA256 = "32a59e143052f827f8134bba890f28d63444c447943e6679521dade7ff7e9fd1"

A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
SLOT34_A2_NAME = "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
POST_V1_NAME = "PF_A2_POST_V1_STATIC_DELTA.tsv"
PRIORITY_NAME = "PF_PROTOCOL_PRIORITY.tsv"
SLOT34_PRIORITY_NAME = "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv"
INVALID_OUTPUT_NAME = "PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv"
TARGET_OUTPUT_NAME = "PF_A2_TARGETS_6564E0_656C50_6FDB40_NONWIRE_DELTA.tsv"
DELETE_TARGET_OUTPUT_NAME = "PF_A2_TARGET_656690_NONWIRE_DELTA.tsv"
PRIORITY_OUTPUT_NAME = "PF_PRIORITY_COMPILER_TARGET_6564_DELTA.tsv"
REPORT_NAME = "PF_COMPILER_RUNTIME_TARGET_6564_CLOSURE.md"
DECODER_NAME = "pf_extract_protocol.py"
V2_VALIDATOR_NAME = "pf_validate_v2_effective_capture.py"
PUBLISH_LOCK_NAME = ".PF_V3_COMPILER_PUBLISH.lock"
ACCEPTANCE_MANIFEST_NAME = "PF_V3_MANIFEST.md"
PRIOR_A2_OVERLAY_NAMES = (
    "PF_A2_STRING_WIRE_TAG_DELTA.tsv",
    POST_V1_NAME,
    "PF_A2_POOL_638690_DELTA.tsv",
    "PF_A2_POOL_661FA0_DELTA.tsv",
    "PF_A2_POOL_46F4D0_DELTA.tsv",
    "PF_A2_POOL_46BAA0_READER_DELTA.tsv",
    "PF_TARGET_652A30_A2_DELTA.tsv",
    "PF_TARGETS_694790_6B3440_A2_DELTA.tsv",
    SLOT34_A2_NAME,
)
PRIOR_PRIORITY_OVERLAY_SHA256 = {
    "PF_POST_V1_PRIORITY_DELTA.tsv": POST_PRIORITY_SHA256,
    "PF_PRIORITY_POOL_638690_DELTA.tsv": PRIORITY_POOL_638690_SHA256,
    "PF_PRIORITY_POOL_661FA0_DELTA.tsv": PRIORITY_POOL_661FA0_SHA256,
    "PF_PRIORITY_POOL_46F4D0_DELTA.tsv": PRIORITY_POOL_46F4D0_SHA256,
    SLOT34_PRIORITY_NAME: SLOT34_PRIORITY_SHA256,
}
OWN_OUTPUTS = frozenset(
    (INVALID_OUTPUT_NAME, TARGET_OUTPUT_NAME, DELETE_TARGET_OUTPUT_NAME,
     PRIORITY_OUTPUT_NAME, REPORT_NAME)
)

INVALID_TAG = "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
TARGET_TAGS = frozenset(
    (
        "CALL_UNCLASSIFIED:0x006564E0",
        "CALL_UNCLASSIFIED:0x00656C50",
        "CALL_UNCLASSIFIED:0x006FDB40",
    )
)
DELETE_TARGET_TAG = "CALL_UNCLASSIFIED:0x00656690"
EVIDENCE_TICKET = "STATIC-GUARDED-CONTAINER-6564-6FDB"
INVALID_MESSAGES = frozenset(
    (
        "ActorLearnedPetsSkillData",
        "CBuffConditionState",
        "CollectionEffectData",
        "CollectionObj_UpdateCollectEffectVital",
        "NPCAppearAttr",
        "WineFormulaLearningAttr",
        "Winemaking_UpdateLearnedFormulaVital",
    )
)

A2_DELTA_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line",
    "base_row_key", "base_delta_key", "message", "direction(W/R)",
    "old_order", "old_tag", "old_field_offset", "old_len",
    "new_wire_order", "new_tag", "new_field_offset", "new_len",
    "new_gate_condition", "resolution", "evidence_ticket",
    "evidence_span_start", "evidence_span_end", "evidence_span_sha256",
    "evidence_file_off", "source",
)

PRIORITY_DELTA_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "priority",
    "old_registry_identity_status", "new_registry_identity_status",
    "old_registry_identity_missing", "new_registry_identity_missing",
    "old_serializer_status", "new_serializer_status",
    "old_serializer_blockers", "new_serializer_blockers",
    "old_structural_status", "new_structural_status",
    "old_blocker", "new_blocker", "evidence_ticket", "closure_scope",
    "source",
)

VA_TO_FILE_DELTA = 0x00400C00
INVALID_IAT = 0x00C3B4C0
INVALID_CALL_BYTES = bytes.fromhex("FF15C0B4C300")
WIRE_PRIMITIVES = (0x0089A600, 0x0089A640)
EXPECTED_WHOLE_IMAGE_E8_PATTERN_COUNTS = {0x0089A600: 1350, 0x0089A640: 1350}


@dataclass(frozen=True)
class SpanPin:
    role: str
    start_va: int
    end_va: int
    sha256: str
    cfg_nodes: int

    @property
    def file_off(self) -> int:
        return self.start_va - VA_TO_FILE_DELTA


GRAPH_SPANS = (
    SpanPin("exception_copy", 0x00401030, 0x0040108F, "e8a0c69b0a0053ea46a9877c9e1dca61a8671b5c692b5b3d979026bc4a5d4bc6", 27),
    SpanPin("container_helper_6564E0", 0x006564E0, 0x0065654C, "94ba7836493b15264a81c5dc0024c1a3f3aee209e800a0b8fa3e0fcebf9fb1da", 44),
    SpanPin("link_assign_6565D0", 0x006565D0, 0x00656622, "0dcc90fdbe7788bf7bac5c3ca2050050ae5ac97f4fa1e74f8f088af6c25a1186", 30),
    SpanPin("recursive_node_delete_656690", 0x00656690, 0x006566C5, "0f6f28adcef1a035e5f1d8a955aebae23136ad1cb70a657eb30242c0e055a7f2", 23),
    SpanPin("node_allocate_6566D0", 0x006566D0, 0x0065670B, "50408a0ab90885dac0d223000ec5d08d25b9cb67e86692058c31c15b4b26ccdb", 18),
    SpanPin("container_helper_656C50", 0x00656C50, 0x00656D43, "efd14b2106dae6cf5c1f8261d0f010c05bbb8c62e65cef4eb509d17a93a9556a", 97),
    SpanPin("link_walk_6FD510", 0x006FD510, 0x006FD594, "bbe2c604df326e192c3b31e68f8fe502494d84d04d56184c633c30ec137e3f19", 52),
    SpanPin("link_assign_6FD600", 0x006FD600, 0x006FD64E, "7ff8c78f5ad1120d6ecba4f07ca7b6add55fe62f91ab19f9e10e2d7ba9039306", 30),
    SpanPin("container_insert_6FD760", 0x006FD760, 0x006FD94F, "0f1ee407d8acd21fc881daad2a7af48615d4574868d1b73116828a979bfc6e68", 168),
    SpanPin("container_helper_6FDB40", 0x006FDB40, 0x006FDC33, "c10312a3c3ef4689c8488902d74f1bebaa8f7a81f7ca870e1b1a96bafbdc0f01", 97),
    SpanPin("operator_delete_thunk", 0x00B37952, 0x00B37958, "dac5c7df4ee9addc4293b8459a55d2bc3eb5864debafc857fb97c01fbbb07cf8", 1),
    SpanPin("operator_new_thunk", 0x00B37980, 0x00B37986, "026db59c9509fd5984356ee06312c76482b74741604ce391ee977c41473b76e4", 1),
    SpanPin("cxx_throw_thunk", 0x00B37998, 0x00B3799E, "16bf8ff4ff7050398899b806680db04f97c42d1b2f69ba2f4eed563eae73ba16", 1),
)


@dataclass(frozen=True)
class SerializerPin:
    role: str
    messages: tuple[str, ...]
    start_va: int
    end_va: int
    sha256: str
    cfg_nodes: int
    invalid_sites: tuple[int, ...]
    container_calls: tuple[tuple[int, int], ...]

    @property
    def file_off(self) -> int:
        return self.start_va - VA_TO_FILE_DELTA


SERIALIZER_PINS = (
    SerializerPin(
        "ActorLearnedPetsSkillData", ("ActorLearnedPetsSkillData",),
        0x006FDF60, 0x006FE058,
        "357587a20115fd3ad22ff55a74dca38b4c6a3d96f69eed10ba79078b45502068",
        87,
        (0x006FDFB6, 0x006FDFCA, 0x006FDFD9),
        ((0x006FDFF6, 0x006564E0), (0x006FE041, 0x006FDB40)),
    ),
    SerializerPin(
        "CBuffConditionState", ("CBuffConditionState",),
        0x00656D50, 0x00656F78,
        "61c60d54d3f48380c611981a0e8338c7ecb01c689499498a3d7d46c0c4aec917",
        193,
        (0x00656DAE, 0x00656DBC, 0x00656DC7, 0x00656E2E, 0x00656E40, 0x00656E4B),
        ((0x00656DE2, 0x006564E0), (0x00656E66, 0x006564E0),
         (0x00656E85, 0x00656690), (0x00656EAC, 0x00656690),
         (0x00656F0D, 0x00656C50), (0x00656F5C, 0x00656C50)),
    ),
    SerializerPin(
        "CollectionEffectData_shared", ("CollectionEffectData", "WineFormulaLearningAttr"),
        0x006A4DB0, 0x006A4EA8,
        "cc2032c193ffecffb950bc809b7106f78bdfa4d2824614cc58d86e380ef70fb5",
        87,
        (0x006A4E06, 0x006A4E1A, 0x006A4E29),
        ((0x006A4E46, 0x006564E0), (0x006A4E91, 0x00656C50)),
    ),
    SerializerPin(
        "CollectionObj_shared", ("CollectionObj_UpdateCollectEffectVital", "Winemaking_UpdateLearnedFormulaVital"),
        0x006A75A0, 0x006A7693,
        "8b8ebeaa44a48eb1ca94ee43673e1549db2ee126f2ab537ed403a44c0fc9f525",
        84,
        (0x006A75EE, 0x006A7600, 0x006A760B),
        ((0x006A7626, 0x006564E0), (0x006A767C, 0x00656C50)),
    ),
    SerializerPin(
        "NPCAppearAttr", ("NPCAppearAttr",),
        0x00737FD0, 0x007380CE,
        "865dcf2144c2c8a86126bbae7e3ed3e1478a0d062194e4d1a6b5f52c2eaa2930",
        89,
        (0x00738026, 0x0073803A, 0x00738049),
        ((0x00738066, 0x006564E0), (0x007380B7, 0x006FDB40)),
    ),
)


@dataclass(frozen=True)
class GuardPin:
    call_va: int
    condition: str
    byte_pins: tuple[tuple[int, str], ...]


def _three_guard_pins(first: int, second: int, third: int) -> tuple[GuardPin, ...]:
    """Return pins for the repeated NULL/identity/equality guard shape."""
    return (
        GuardPin(first, "NULL_OR_UNEXPECTED_NODE_GUARD", (
            (first - 8, "85f6"), (first - 6, "7404"),
            (first - 4, "3bf0"), (first - 2, "7406"),
        )),
        GuardPin(second, "NULL_NODE_GUARD", ((second - 4, "85f6"), (second - 2, "7537"))),
        GuardPin(third, "NODE_BOUNDARY_EQUALITY_GUARD", ((third - 5, "3b4e18"), (third - 2, "7506"))),
    )


GUARD_PINS = (
    *_three_guard_pins(0x006FDFB6, 0x006FDFCA, 0x006FDFD9),
    GuardPin(0x00656DAE, "NULL_OR_UNEXPECTED_NODE_GUARD", ((0x00656DA6, "85f6"), (0x00656DA8, "7404"), (0x00656DAA, "3bf0"), (0x00656DAC, "7406"))),
    GuardPin(0x00656DBC, "NULL_NODE_GUARD", ((0x00656DB8, "85f6"), (0x00656DBA, "7535"))),
    GuardPin(0x00656DC7, "NODE_BOUNDARY_EQUALITY_GUARD", ((0x00656DC2, "3b5e18"), (0x00656DC5, "7506"))),
    GuardPin(0x00656E2E, "NULL_OR_UNEXPECTED_NODE_GUARD", ((0x00656E26, "85f6"), (0x00656E28, "7404"), (0x00656E2A, "3bf0"), (0x00656E2C, "7406"))),
    GuardPin(0x00656E40, "NULL_NODE_GUARD", ((0x00656E3C, "85f6"), (0x00656E3E, "7535"))),
    GuardPin(0x00656E4B, "NODE_BOUNDARY_EQUALITY_GUARD", ((0x00656E46, "3b5e18"), (0x00656E49, "7506"))),
    *_three_guard_pins(0x006A4E06, 0x006A4E1A, 0x006A4E29),
    GuardPin(0x006A75EE, "NULL_OR_UNEXPECTED_NODE_GUARD", ((0x006A75E6, "85f6"), (0x006A75E8, "7404"), (0x006A75EA, "3bf0"), (0x006A75EC, "7406"))),
    GuardPin(0x006A7600, "NULL_NODE_GUARD", ((0x006A75FC, "85f6"), (0x006A75FE, "7535"))),
    GuardPin(0x006A760B, "NODE_BOUNDARY_EQUALITY_GUARD", ((0x006A7606, "3b6e18"), (0x006A7609, "7506"))),
    *_three_guard_pins(0x00738026, 0x0073803A, 0x00738049),
)


EXPECTED_RAW_E8_PATTERNS = {
    0x006566A7: 0x00656690,
    0x006566AF: 0x00B37952,
    0x006566D2: 0x00B37980,
    0x00656CC2: 0x006FD760,
    0x00656CE5: 0x006FD510,
    0x00656D09: 0x006FD760,
    0x006FD7B2: 0x00401030,
    0x006FD7C9: 0x00B37998,
    0x006FD7DF: 0x006566D0,
    # 0x006FD7E5 is an E8 byte inside another decoded instruction.  It is
    # intentionally retained in the raw-pattern census, not called a call.
    0x006FD7E5: 0xBB881F75,
    0x006FD875: 0x006FD600,
    0x006FD893: 0x006565D0,
    0x006FD8C1: 0x006565D0,
    0x006FDBB2: 0x006FD760,
    0x006FDBD5: 0x006FD510,
    0x006FDBF9: 0x006FD760,
}

DIRECT_CALLS = {site: target for site, target in EXPECTED_RAW_E8_PATTERNS.items() if site != 0x006FD7E5}

EXACT_BYTE_PINS = (
    (0x00401058, "ff1528b8c300"), (0x00401074, "ff159cb4c300"),
    (0x006564E7, "8b3dc0b4c300"), (0x006564EF, "ffd7"), (0x006564FA, "ffd7"),
    (0x00656CAD, "ff15c0b4c300"),
    # CBuffConditionState reaches 0x00656690 with arg1 loaded from the two
    # container node slots (+0x38/+0x58 then +0x04) and ECX set to the two
    # embedded container subobjects (+0x20/+0x40), never from the stream formal.
    (0x00656E79, "8b4d388b51048d7520528bcee806f8ffff"),
    (0x00656EA0, "8b45588b48048d7d40518bcfe8dff7ffff"),
    (0x006FD517, "8b3dc0b4c300"), (0x006FD51F, "ffd7"), (0x006FD536, "ffd7"),
    (0x006FD79B, "ff1580b4c300"),
    (0x006FDB9D, "ff15c0b4c300"),
    (0x00B37952, "ff252cb8c300"),
    (0x00B37980, "ff25bcb4c300"), (0x00B37998, "ff25c4b4c300"),
)

EXPECTED_IMPORTS = {
    0x00C3B480: ("MSVCP90.dll", "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@PBD@Z"),
    0x00C3B49C: ("MSVCP90.dll", "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@ABV01@@Z"),
    0x00C3B4BC: ("MSVCR90.dll", "??2@YAPAXI@Z"),
    0x00C3B4C0: ("MSVCR90.dll", "_invalid_parameter_noinfo"),
    0x00C3B4C4: ("MSVCR90.dll", "_CxxThrowException"),
    0x00C3B828: ("MSVCR90.dll", "??0exception@std@@QAE@XZ"),
    0x00C3B82C: ("MSVCR90.dll", "??3@YAXPAX@Z"),
}

# Exact executed CFG call census.  Ordinary control-flow jumps are excluded;
# indirect entries record the operand proven by the guarded decoder.
EXPECTED_CFG_CALLS: dict[int, tuple[str, int | str]] = {
    0x00401058: ("CALL_IAT", 0x00C3B828),
    0x00401074: ("CALL_IAT", 0x00C3B49C),
    0x006564EF: ("CALL_REG", "edi"),
    0x006564FA: ("CALL_REG", "edi"),
    0x006566A7: ("CALL", 0x00656690),
    0x006566AF: ("CALL", 0x00B37952),
    0x006566D2: ("CALL", 0x00B37980),
    0x00656CAD: ("CALL_IAT", 0x00C3B4C0),
    0x00656CC2: ("CALL", 0x006FD760),
    0x00656CE5: ("CALL", 0x006FD510),
    0x00656D09: ("CALL", 0x006FD760),
    0x006FD51F: ("CALL_REG", "edi"),
    0x006FD536: ("CALL_REG", "edi"),
    0x006FD79B: ("CALL_IAT", 0x00C3B480),
    0x006FD7B2: ("CALL", 0x00401030),
    0x006FD7C9: ("CALL", 0x00B37998),
    0x006FD7DF: ("CALL", 0x006566D0),
    0x006FD875: ("CALL", 0x006FD600),
    0x006FD893: ("CALL", 0x006565D0),
    0x006FD8C1: ("CALL", 0x006565D0),
    0x006FDB9D: ("CALL_IAT", 0x00C3B4C0),
    0x006FDBB2: ("CALL", 0x006FD760),
    0x006FDBD5: ("CALL", 0x006FD510),
    0x006FDBF9: ("CALL", 0x006FD760),
    0x00B37952: ("JMP_IAT", 0x00C3B82C),
    0x00B37980: ("JMP_IAT", 0x00C3B4BC),
    0x00B37998: ("JMP_IAT", 0x00C3B4C4),
}

EXPECTED_REGISTER_IAT_REACHING = {
    0x006564EF: ("edi", 0x006564E7, INVALID_IAT),
    0x006564FA: ("edi", 0x006564E7, INVALID_IAT),
    0x006FD51F: ("edi", 0x006FD517, INVALID_IAT),
    0x006FD536: ("edi", 0x006FD517, INVALID_IAT),
}


@dataclass(frozen=True)
class ArgDefPin:
    push_va: int
    register: str
    definition_va: int
    origin: str


@dataclass(frozen=True)
class DataflowPin:
    call_va: int
    target_va: int
    window_va: int
    window_hex: str
    ecx_definition_va: int
    ecx_origin: str
    container_register: str | None = None
    container_definition_va: int | None = None
    args: tuple[ArgDefPin, ...] = ()


TARGET_DATAFLOW_PINS = (
    DataflowPin(0x006FDFF6, 0x006564E0, 0x006FDFF2, "8d4c2410e8e584f5ff", 0x006FDFF2, "STACK_LOCAL"),
    DataflowPin(
        0x006FE041, 0x006FDB40, 0x006FE035,
        "8d442424508d4c2414518bcfe8fafaffff", 0x006FE03F,
        "THIS_DERIVED_CONTAINER", "edi", 0x006FE022,
        (ArgDefPin(0x006FE039, "eax", 0x006FE035, "NONSTREAM_ENTRY_FORMAL_SLOT"),
         ArgDefPin(0x006FE03E, "ecx", 0x006FE03A, "STACK_LOCAL")),
    ),
    DataflowPin(0x00656DE2, 0x006564E0, 0x00656DDE, "8d4c2414e8f9f6ffff", 0x00656DDE, "STACK_LOCAL"),
    DataflowPin(0x00656E66, 0x006564E0, 0x00656E62, "8d4c2414e875f6ffff", 0x00656E62, "STACK_LOCAL"),
    DataflowPin(
        0x00656E85, 0x00656690, 0x00656E79,
        "8b4d388b51048d7520528bcee806f8ffff", 0x00656E83,
        "THIS_DERIVED_CONTAINER", "esi", 0x00656E7F,
        (ArgDefPin(0x00656E82, "edx", 0x00656E7C, "CONTAINER_NODE"),),
    ),
    DataflowPin(
        0x00656EAC, 0x00656690, 0x00656EA0,
        "8b45588b48048d7d40518bcfe8dff7ffff", 0x00656EAA,
        "THIS_DERIVED_CONTAINER", "edi", 0x00656EA6,
        (ArgDefPin(0x00656EA9, "ecx", 0x00656EA3, "CONTAINER_NODE"),),
    ),
    DataflowPin(
        0x00656F0D, 0x00656C50, 0x00656F01,
        "8d542410528d442418508bcee83efdffff", 0x00656F0B,
        "THIS_DERIVED_CONTAINER", "esi", 0x00656E7F,
        (ArgDefPin(0x00656F05, "edx", 0x00656F01, "STACK_LOCAL"),
         ArgDefPin(0x00656F0A, "eax", 0x00656F06, "STACK_LOCAL")),
    ),
    DataflowPin(
        0x00656F5C, 0x00656C50, 0x00656F50,
        "8d442410508d4c2418518bcfe8effcffff", 0x00656F5A,
        "THIS_DERIVED_CONTAINER", "edi", 0x00656EA6,
        (ArgDefPin(0x00656F54, "eax", 0x00656F50, "STACK_LOCAL"),
         ArgDefPin(0x00656F59, "ecx", 0x00656F55, "STACK_LOCAL")),
    ),
    DataflowPin(0x006A4E46, 0x006564E0, 0x006A4E42, "8d4c2410e89516fbff", 0x006A4E42, "STACK_LOCAL"),
    DataflowPin(
        0x006A4E91, 0x00656C50, 0x006A4E85,
        "8d442424508d4c2414518bcfe8ba1dfbff", 0x006A4E8F,
        "THIS_DERIVED_CONTAINER", "edi", 0x006A4E72,
        (ArgDefPin(0x006A4E89, "eax", 0x006A4E85, "NONSTREAM_ENTRY_FORMAL_SLOT"),
         ArgDefPin(0x006A4E8E, "ecx", 0x006A4E8A, "STACK_LOCAL")),
    ),
    DataflowPin(0x006A7626, 0x006564E0, 0x006A7622, "8d4c2410e8b5eefaff", 0x006A7622, "STACK_LOCAL"),
    DataflowPin(
        0x006A767C, 0x00656C50, 0x006A7670,
        "8d44242c508d4c241c518bcfe8cff5faff", 0x006A767A,
        "THIS_DERIVED_CONTAINER", "edi", 0x006A765A,
        (ArgDefPin(0x006A7674, "eax", 0x006A7670, "NONSTREAM_ENTRY_FORMAL_SLOT"),
         ArgDefPin(0x006A7679, "ecx", 0x006A7675, "STACK_LOCAL")),
    ),
    DataflowPin(0x00738066, 0x006564E0, 0x00738062, "8d4c2410e875e4f1ff", 0x00738062, "STACK_LOCAL"),
    DataflowPin(
        0x007380B7, 0x006FDB40, 0x007380AB,
        "8d442420508d4c2414518bcfe8845afcff", 0x007380B5,
        "THIS_DERIVED_CONTAINER", "edi", 0x00738094,
        (ArgDefPin(0x007380AF, "eax", 0x007380AB, "REUSED_STREAM_SLOT_AFTER_KILL_AND_WIRE_READ"),
         ArgDefPin(0x007380B4, "ecx", 0x007380B0, "STACK_LOCAL")),
    ),
)

# These exact loads bind each serializer's stream formal separately from the
# target mutable formals.  All target argument windows below exclude the bound
# stream register and use only stack locals or this-derived container state.
STREAM_FORMAL_BYTE_PINS = (
    (0x006FDF69, "8b6c2418", "ebp", "ActorLearnedPetsSkillData:stream=EBP:entry+0x4"),
    (0x00656D64, "8b742424", "esi", "CBuffConditionState:write_stream=ESI:entry+0x4"),
    (0x00656EC3, "8b6c242c", "ebp", "CBuffConditionState:read_stream=EBP:entry+0x4"),
    (0x006A4DB9, "8b6c2418", "ebp", "CollectionEffectData_shared:stream=EBP:entry+0x4"),
    (0x006A75BF, "8b4c2430", "ecx", "CollectionObj_shared:write_stream=ECX:entry+0x4"),
    (0x006A7639, "8b5c242c", "ebx", "CollectionObj_shared:read_stream=EBX:entry+0x4"),
    (0x00737FD9, "8b6c2418", "ebp", "NPCAppearAttr:stream=EBP:entry+0x4"),
)

CONTAINER_ROOTS = {
    0x006FE022: ("edi", 0x006FDF71),
    0x00656E7F: ("ebp", 0x00656D5C),
    0x00656EA6: ("ebp", 0x00656D5C),
    0x006A4E72: ("edi", 0x006A4DC1),
    0x006A765A: ("edi", 0x006A75AC),
    0x00738094: ("edi", 0x00737FE1),
}

NODE_ARG_BASES = {
    0x00656E7C: ("ecx", 0x00656E79),
    0x00656EA3: ("eax", 0x00656EA0),
}

BASE_PRIORITY_MESSAGES = frozenset(
    ("CBuffConditionState", "CollectionObj_UpdateCollectEffectVital", "Winemaking_UpdateLearnedFormulaVital")
)
CHAIN_PRIORITY_MESSAGES = INVALID_MESSAGES - BASE_PRIORITY_MESSAGES
EXPECTED_PRIORITY_LINES = {
    "CBuffConditionState": (PRIORITY_NAME, 170),
    "CollectionObj_UpdateCollectEffectVital": (PRIORITY_NAME, 358),
    "Winemaking_UpdateLearnedFormulaVital": (PRIORITY_NAME, 297),
    "ActorLearnedPetsSkillData": (SLOT34_PRIORITY_NAME, 3),
    "CollectionEffectData": (SLOT34_PRIORITY_NAME, 13),
    "NPCAppearAttr": (SLOT34_PRIORITY_NAME, 26),
    "WineFormulaLearningAttr": (SLOT34_PRIORITY_NAME, 38),
}


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


def atomic_write_bytes(path: Path, data: bytes) -> None:
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name is not None and os.path.exists(temp_name):
            os.unlink(temp_name)


def acquire_publish_lock(parent: Path) -> tuple[Path, bytes]:
    """Acquire the fail-closed publisher lock; a stale hard-kill lock blocks."""
    path = parent / PUBLISH_LOCK_NAME
    token = f"pid={os.getpid()};owner={Path(__file__).name}\n".encode("ascii")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        descriptor = os.open(path, flags, 0o600)
    except FileExistsError as exc:
        raise RuntimeError(
            f"compiler publisher lock exists (active or stale): {path.name}; "
            f"do not publish until ownership is resolved"
        ) from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(token)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        if path.exists():
            path.unlink()
        raise
    if path.read_bytes() != token:
        raise RuntimeError("publisher lock read-back drift")
    return path, token


def release_publish_lock(path: Path, token: bytes) -> None:
    if not path.exists() or path.read_bytes() != token:
        raise RuntimeError("publisher lock ownership changed; lock left in place")
    path.unlink()


def publish_outputs_transaction(outputs: Mapping[Path, bytes]) -> None:
    """Stage and verify the complete owned output set, then replace with rollback."""
    ordered = list(outputs.items())
    names = [path.name for path, _data in ordered]
    if set(names) != OWN_OUTPUTS or len(names) != len(OWN_OUTPUTS):
        raise RuntimeError(f"publish output-set drift: {names}")
    if names[-1] != REPORT_NAME:
        raise RuntimeError("report must be the last published consumer artifact")
    parents = {path.parent.resolve() for path, _data in ordered}
    if len(parents) != 1:
        raise RuntimeError("publish paths escape the one external directory")
    parent = next(iter(parents))
    if any(path.resolve().parent != parent for path, _data in ordered):
        raise RuntimeError("publish path resolution drift")

    staged: dict[Path, Path] = {}
    old_bytes: dict[Path, bytes | None] = {}
    replaced: list[Path] = []
    lock_path, lock_token = acquire_publish_lock(parent)
    try:
        for path, data in ordered:
            old_bytes[path] = path.read_bytes() if path.exists() else None
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=parent, prefix=f".{path.name}.stage.",
                suffix=".tmp", delete=False,
            ) as handle:
                stage = Path(handle.name)
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            staged[path] = stage

        for path, data in ordered:
            stage = staged[path]
            staged_bytes = stage.read_bytes()
            if staged_bytes != data or sha256_bytes(staged_bytes) != sha256_bytes(data):
                raise RuntimeError(f"staged output verification failed: {path.name}")

        for path, _data in ordered:
            # Journal the target first.  An interrupt after replace but before
            # bookkeeping must still cause this path to be restored.
            replaced.append(path)
            os.replace(staged[path], path)

        for path, data in ordered:
            final = path.read_bytes()
            if final != data or sha256_bytes(final) != sha256_bytes(data):
                raise RuntimeError(f"published output verification failed: {path.name}")
    except BaseException as exc:
        rollback_errors: list[str] = []
        for path in reversed(replaced):
            try:
                previous = old_bytes[path]
                if previous is None:
                    if path.exists():
                        path.unlink()
                else:
                    atomic_write_bytes(path, previous)
                    if path.read_bytes() != previous:
                        raise RuntimeError("restored bytes differ")
            except BaseException as rollback_exc:
                rollback_errors.append(f"{path.name}: {rollback_exc}")
        if rollback_errors:
            raise RuntimeError(
                f"publish failed ({exc}); rollback also failed: {rollback_errors}"
            ) from exc
        raise
    finally:
        for stage in staged.values():
            if stage.exists():
                stage.unlink()
        release_publish_lock(lock_path, lock_token)


def bytes_at_va(image: bytes, va: int, size: int) -> bytes:
    off = va - VA_TO_FILE_DELTA
    if off < 0 or off + size > len(image):
        raise RuntimeError(f"VA outside pinned .text mapping: 0x{va:08X}")
    return image[off:off + size]


def require_bytes(image: bytes, va: int, expected_hex: str, label: str) -> None:
    expected = bytes.fromhex(expected_hex)
    actual = bytes_at_va(image, va, len(expected))
    if actual != expected:
        raise RuntimeError(
            f"{label} bytes drift at 0x{va:08X}: expected {expected.hex()}, got {actual.hex()}"
        )


@dataclass(frozen=True)
class Section:
    name: str
    va: int
    raw_ptr: int
    raw_size: int


@dataclass(frozen=True)
class ImportPin:
    dll: str
    symbol: str
    iat_off: int
    descriptor_off: int
    lookup_off: int
    dll_name_off: int
    symbol_name_off: int


def parse_pe(image: bytes) -> tuple[int, list[Section], dict[int, ImportPin]]:
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
    raw_sections: list[tuple[str, int, int, int, int]] = []
    sections: list[Section] = []
    for index in range(section_count):
        off = section_table + index * 40
        name = image[off:off + 8].rstrip(b"\0").decode("latin1")
        virtual_size, rva, raw_size, raw_ptr = struct.unpack_from("<IIII", image, off + 8)
        raw_sections.append((name, rva, virtual_size, raw_ptr, raw_size))
        sections.append(Section(name, image_base + rva, raw_ptr, raw_size))

    def rva_to_off(rva: int) -> int:
        if 0 <= rva < size_of_headers:
            return rva
        for _name, section_rva, virtual_size, raw_ptr, raw_size in raw_sections:
            delta = rva - section_rva
            if 0 <= delta < raw_size and delta < max(virtual_size, raw_size):
                return raw_ptr + delta
        raise RuntimeError(f"cannot map RVA 0x{rva:08X}")

    import_rva, import_size = struct.unpack_from("<II", image, optional + 104)
    if not import_rva or not import_size:
        raise RuntimeError("missing PE import directory")
    imports: dict[int, ImportPin] = {}
    descriptor_rva = import_rva
    while True:
        descriptor_off = rva_to_off(descriptor_rva)
        original, timestamp, forwarder, name_rva, first_thunk = struct.unpack_from(
            "<IIIII", image, descriptor_off
        )
        if not any((original, timestamp, forwarder, name_rva, first_thunk)):
            break
        dll_name_off = rva_to_off(name_rva)
        dll_end = image.find(b"\0", dll_name_off)
        dll = image[dll_name_off:dll_end].decode("ascii", "strict")
        lookup_base = original or first_thunk
        index = 0
        while True:
            lookup_off = rva_to_off(lookup_base + index * 4)
            thunk = struct.unpack_from("<I", image, lookup_off)[0]
            if not thunk:
                break
            if not (thunk & 0x80000000):
                symbol_name_off = rva_to_off(thunk) + 2
                symbol_end = image.find(b"\0", symbol_name_off)
                symbol = image[symbol_name_off:symbol_end].decode("ascii", "strict")
                iat_rva = first_thunk + index * 4
                iat_va = image_base + iat_rva
                imports[iat_va] = ImportPin(
                    dll, symbol, rva_to_off(iat_rva), descriptor_off, lookup_off,
                    dll_name_off, symbol_name_off,
                )
            index += 1
        descriptor_rva += 20
    return image_base, sections, imports


def verify_imports(imports: Mapping[int, ImportPin]) -> None:
    for iat_va, expected in EXPECTED_IMPORTS.items():
        pin = imports.get(iat_va)
        if pin is None or (pin.dll, pin.symbol) != expected:
            raise RuntimeError(f"import drift at IAT 0x{iat_va:08X}: {pin}")
    invalid = imports[INVALID_IAT]
    expected_offsets = (0x008398C0, 0x00C112DC, 0x00C118B4, 0x00C1647C, 0x00C15C62)
    actual_offsets = (
        invalid.iat_off, invalid.descriptor_off, invalid.lookup_off,
        invalid.dll_name_off, invalid.symbol_name_off,
    )
    if actual_offsets != expected_offsets:
        raise RuntimeError(f"invalid-parameter import provenance drift: {actual_offsets}")


def rel32_target(image: bytes, va: int) -> int:
    raw = bytes_at_va(image, va, 5)
    if raw[0] != 0xE8:
        raise RuntimeError(f"missing E8 at 0x{va:08X}")
    return (va + 5 + struct.unpack_from("<i", raw, 1)[0]) & 0xFFFFFFFF


def verify_graph(image: bytes, sections: Sequence[Section]) -> dict[str, int]:
    graph_ranges: list[tuple[int, int, int, int]] = []
    raw_e8: dict[int, int] = {}
    for pin in GRAPH_SPANS:
        raw = bytes_at_va(image, pin.start_va, pin.end_va - pin.start_va)
        if sha256_bytes(raw) != pin.sha256:
            raise RuntimeError(f"graph span drift: {pin.role}")
        graph_ranges.append((pin.start_va, pin.end_va, pin.file_off, pin.file_off + len(raw)))
        for index in range(len(raw) - 4):
            if raw[index] == 0xE8:
                site = pin.start_va + index
                raw_e8[site] = (site + 5 + struct.unpack_from("<i", raw, index + 1)[0]) & 0xFFFFFFFF
    if raw_e8 != EXPECTED_RAW_E8_PATTERNS:
        raise RuntimeError(f"graph raw E8 pattern census drift: {raw_e8}")
    for site, target in DIRECT_CALLS.items():
        if rel32_target(image, site) != target:
            raise RuntimeError(f"graph direct call drift at 0x{site:08X}")
    for va, encoded in EXACT_BYTE_PINS:
        require_bytes(image, va, encoded, "graph fixed call/import")

    whole_counts: dict[int, int] = {}
    graph_e8_counts: dict[int, int] = {}
    graph_literal_counts: dict[int, int] = {}
    for target in WIRE_PRIMITIVES:
        count = 0
        graph_count = 0
        for section in sections:
            start = section.raw_ptr
            end = section.raw_ptr + section.raw_size
            for off in range(start, end - 4):
                if image[off] != 0xE8:
                    continue
                site_va = section.va + (off - start)
                got = (site_va + 5 + struct.unpack_from("<i", image, off + 1)[0]) & 0xFFFFFFFF
                if got != target:
                    continue
                count += 1
                if any(lo <= site_va < hi for lo, hi, _fo, _fe in graph_ranges):
                    graph_count += 1
        literal = struct.pack("<I", target)
        literal_count = 0
        for _lo, _hi, file_lo, file_hi in graph_ranges:
            data = image[file_lo:file_hi]
            cursor = 0
            while True:
                found = data.find(literal, cursor)
                if found < 0:
                    break
                literal_count += 1
                cursor = found + 1
        whole_counts[target] = count
        graph_e8_counts[target] = graph_count
        graph_literal_counts[target] = literal_count
    if whole_counts != EXPECTED_WHOLE_IMAGE_E8_PATTERN_COUNTS:
        raise RuntimeError(f"whole IMAGE E8 pattern census drift: {whole_counts}")
    if any(graph_e8_counts.values()) or any(graph_literal_counts.values()):
        raise RuntimeError(
            f"wire primitive byte-pattern reached graph: E8={graph_e8_counts} literal={graph_literal_counts}"
        )
    return {
        "e8_89a600": whole_counts[0x0089A600],
        "e8_89a640": whole_counts[0x0089A640],
        "graph_e8_intersection": sum(graph_e8_counts.values()),
        "graph_literal_intersection": sum(graph_literal_counts.values()),
    }


def serializer_for_message(message: str) -> SerializerPin:
    found = [pin for pin in SERIALIZER_PINS if message in pin.messages]
    if len(found) != 1:
        raise RuntimeError(f"serializer pin mapping drift for {message}: {len(found)}")
    return found[0]


def parse_gate_call(gate: str) -> tuple[int, int, int]:
    pattern = re.compile(
        r"^exact_direct_iat_call@(0x[0-9A-F]{8}) file_off=(0x[0-9A-F]{8}) "
        r"function=(0x[0-9A-F]{8}) iat=0x00C3B4C0 bytes=FF15C0B4C300 AND "
        r"exact_direct_iat_import iat=0x00C3B4C0 iat_file_off=0x008398C0 "
        r"descriptor_file_off=0x00C112DC lookup_file_off=0x00C118B4 "
        r"dll_name_file_off=0x00C1647C symbol_name_file_off=0x00C15C62 "
        r"dll=MSVCR90\.dll symbol=_invalid_parameter_noinfo call_bytes=FF15C0B4C300 "
        r"operation=PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL wire_effect=unproved "
        r"basis=exact_call_bytes_and_pe_import$"
    )
    match = pattern.fullmatch(gate)
    if match is None:
        raise RuntimeError("exact direct-IAT gate provenance drift")
    return tuple(int(value, 16) for value in match.groups())  # type: ignore[return-value]


def verify_serializer_proof(image: bytes) -> dict[int, GuardPin]:
    guard_by_site = {pin.call_va: pin for pin in GUARD_PINS}
    expected_sites = {site for span in SERIALIZER_PINS for site in span.invalid_sites}
    if set(guard_by_site) != expected_sites or len(guard_by_site) != 18:
        raise RuntimeError("guard pin census drift")
    for span in SERIALIZER_PINS:
        raw = bytes_at_va(image, span.start_va, span.end_va - span.start_va)
        if sha256_bytes(raw) != span.sha256:
            raise RuntimeError(f"serializer span drift: {span.role}")
        for site in span.invalid_sites:
            require_bytes(image, site, INVALID_CALL_BYTES.hex(), "guarded invalid-parameter call")
        for site, target in span.container_calls:
            if rel32_target(image, site) != target:
                raise RuntimeError(f"serializer/container graph call drift at 0x{site:08X}")
    for guard in GUARD_PINS:
        for va, encoded in guard.byte_pins:
            require_bytes(image, va, encoded, f"guard:{guard.condition}")
    return guard_by_site


def load_guarded_decoder(external: Path) -> types.ModuleType:
    """Execute only the hash-pinned, standard-library IMAGE decoder.

    Importing by source bytes keeps this audit independent of stale bytecode and
    makes the executed decoder itself part of the fail-closed evidence boundary.
    """
    path = external / DECODER_NAME
    require_hash(path, DECODER_SHA256, "guarded decoder")
    source = path.read_bytes()
    module_name = "_pf_pinned_extract_protocol_0bb792bb"
    if module_name in sys.modules:
        raise RuntimeError("guarded decoder module-name collision")
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[module_name] = module
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    return module


def load_pinned_v2_validator(external: Path) -> types.ModuleType:
    """Load the frozen effective-V2 replay engine from exact source bytes."""
    path = external / V2_VALIDATOR_NAME
    require_hash(path, V2_VALIDATOR_SHA256, "effective-V2 validator")
    source = path.read_bytes()
    module_name = "_pf_pinned_v2_effective_capture_7a9c0801"
    if module_name in sys.modules:
        raise RuntimeError("effective-V2 validator module-name collision")
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[module_name] = module
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    return module


def _decoder_span(decoder: types.ModuleType, image: object, pin: SpanPin | SerializerPin) -> object:
    start_off = image.va_range_to_off(pin.start_va, pin.end_va - pin.start_va)
    if start_off is None or start_off != pin.file_off:
        raise RuntimeError(f"guarded decoder span mapping drift: {pin.role}")
    return decoder.FunctionSpan(
        pin.start_va, pin.end_va, start_off,
        start_off + (pin.end_va - pin.start_va), pin.sha256,
    )


def _only_reaching_definition(
    analyzer: object, function_va: int, register: str, use_va: int, expected_va: int,
    label: str,
) -> None:
    definitions = analyzer._reaching_definitions(function_va, register).get(
        use_va, frozenset()
    )
    if definitions != frozenset((expected_va,)):
        raise RuntimeError(
            f"{label} reaching-definition drift at 0x{use_va:08X}: {definitions}"
        )


def _require_reg(operand: object, register: str, label: str) -> None:
    if operand is None or operand.kind != "reg" or operand.reg != register:
        raise RuntimeError(f"{label}: expected register {register}, got {operand}")


def _require_stack_local_lea(
    analyzer: object, decoded: object, function_va: int, definition_va: int,
    register: str, label: str,
) -> int:
    entry_relative = _stack_lea_entry_relative(
        analyzer, decoded, function_va, definition_va, register, label
    )
    if entry_relative >= 0:
        raise RuntimeError(
            f"{label}: LEA is not a stack local at 0x{definition_va:08X}; "
            f"entry-relative={entry_relative:+d}"
        )
    return entry_relative


def _stack_lea_entry_relative(
    analyzer: object, decoded: object, function_va: int, definition_va: int,
    register: str, label: str,
) -> int:
    ins = decoded.instructions.get(definition_va)
    if ins is None or ins.kind != "lea":
        raise RuntimeError(f"{label}: missing LEA definition at 0x{definition_va:08X}")
    _require_reg(ins.dst, register, label)
    if (
        ins.src is None or ins.src.kind != "mem" or ins.src.base != "esp"
        or ins.src.index is not None or ins.src.absolute is not None
    ):
        raise RuntimeError(f"{label}: non-stack LEA at 0x{definition_va:08X}")
    depths = analyzer._stack_depths(function_va).get(definition_va, frozenset())
    if len(depths) != 1 or None in depths:
        raise RuntimeError(f"{label}: ambiguous stack depth at 0x{definition_va:08X}: {depths}")
    depth = next(iter(depths))
    assert depth is not None
    return ins.src.disp - depth


def _dominators(decoded: object) -> dict[int, frozenset[int]]:
    nodes = set(decoded.instructions)
    entry = decoded.span.start_va
    result: dict[int, set[int]] = {
        node: ({entry} if node == entry else set(nodes)) for node in nodes
    }
    changed = True
    while changed:
        changed = False
        for node in sorted(nodes - {entry}):
            predecessors = [
                pred for pred in decoded.predecessors.get(node, ()) if pred in nodes
            ]
            if not predecessors:
                updated = {node}
            else:
                common = set(result[predecessors[0]])
                for predecessor in predecessors[1:]:
                    common.intersection_update(result[predecessor])
                updated = {node} | common
            if updated != result[node]:
                result[node] = updated
                changed = True
    return {node: frozenset(values) for node, values in result.items()}


def verify_executed_cfg_and_dataflow(
    external: Path, image_path: Path, image_bytes: bytes,
) -> dict[str, int]:
    """Run the pinned CFG/reaching-definition proofs, not just byte assertions."""
    decoder = load_guarded_decoder(external)
    if decoder.WRITE_VA != 0x0089A600 or decoder.READ_VA != 0x0089A640:
        raise RuntimeError("guarded decoder wire primitive identity drift")
    decoded_image = decoder.Image(image_path)
    if decoded_image.data != image_bytes or decoded_image.sha256 != IMAGE_SHA256:
        raise RuntimeError("guarded decoder IMAGE identity drift")
    analyzer = decoder.SerializerAnalyzer(decoded_image, [])

    graph_decodes: dict[int, object] = {}
    actual_calls: dict[int, tuple[str, int | str]] = {}
    for pin in GRAPH_SPANS:
        span = _decoder_span(decoder, decoded_image, pin)
        decoded = decoder.decode_function(decoded_image, span)
        if len(decoded.instructions) != pin.cfg_nodes or decoded.errors:
            raise RuntimeError(
                f"executed graph CFG drift for {pin.role}: "
                f"nodes={len(decoded.instructions)} errors={decoded.errors}"
            )
        analyzer.span_cache[pin.start_va] = span
        analyzer.decode_cache[pin.start_va] = decoded
        graph_decodes[pin.start_va] = decoded
        for ins in decoded.instructions.values():
            if ins.kind == "call":
                if ins.target is None:
                    raise RuntimeError(f"direct call lacks target at 0x{ins.va:08X}")
                actual_calls[ins.va] = ("CALL", ins.target)
            elif ins.kind in ("call_indirect", "jmp_indirect"):
                prefix = "CALL" if ins.kind == "call_indirect" else "JMP"
                if (
                    ins.src is not None and ins.src.kind == "mem"
                    and ins.src.base is None and ins.src.index is None
                    and ins.src.absolute is not None
                ):
                    actual_calls[ins.va] = (prefix + "_IAT", ins.src.absolute)
                elif ins.src is not None and ins.src.kind == "reg" and ins.src.reg is not None:
                    actual_calls[ins.va] = (prefix + "_REG", ins.src.reg)
                else:
                    actual_calls[ins.va] = (prefix + "_UNRESOLVED", repr(ins.src))
    if actual_calls != EXPECTED_CFG_CALLS:
        raise RuntimeError(f"executed graph call census drift: {actual_calls}")

    for call_va, (register, definition_va, iat_va) in EXPECTED_REGISTER_IAT_REACHING.items():
        owners = [
            pin for pin in GRAPH_SPANS if pin.start_va <= call_va < pin.end_va
        ]
        if len(owners) != 1:
            raise RuntimeError(f"register-IAT call owner drift at 0x{call_va:08X}")
        owner = owners[0]
        decoded = graph_decodes[owner.start_va]
        call = decoded.instructions.get(call_va)
        definition = decoded.instructions.get(definition_va)
        if call is None or not analyzer._is_exact_register_indirect_call(call, register):
            raise RuntimeError(f"non-exact register call at 0x{call_va:08X}")
        _only_reaching_definition(
            analyzer, owner.start_va, register, call_va, definition_va,
            "register-IAT call",
        )
        if definition is None or not analyzer._is_exact_iat_register_load(
            definition, register, iat_va
        ):
            raise RuntimeError(f"non-exact IAT load at 0x{definition_va:08X}")
        symbol = decoded_image.imports_by_iat.get(iat_va)
        if symbol is None or (symbol.dll, symbol.name) != EXPECTED_IMPORTS[iat_va]:
            raise RuntimeError(f"register-IAT symbol drift at 0x{iat_va:08X}")

    serializer_decodes: dict[int, object] = {}
    actual_invalid_sites: set[int] = set()
    actual_target_calls: set[tuple[int, int]] = set()
    target_vas = set(TARGET_TAGS)
    target_numbers = {
        int(tag.rsplit(":", 1)[1], 16) for tag in target_vas
    } | {0x00656690}
    for pin in SERIALIZER_PINS:
        span = _decoder_span(decoder, decoded_image, pin)
        decoded = decoder.decode_function(decoded_image, span)
        if len(decoded.instructions) != pin.cfg_nodes or decoded.errors:
            raise RuntimeError(
                f"executed serializer CFG drift for {pin.role}: "
                f"nodes={len(decoded.instructions)} errors={decoded.errors}"
            )
        analyzer.span_cache[pin.start_va] = span
        analyzer.decode_cache[pin.start_va] = decoded
        serializer_decodes[pin.start_va] = decoded
        for site in pin.invalid_sites:
            ins = decoded.instructions.get(site)
            if not (
                ins is not None and ins.kind == "call_indirect"
                and ins.src is not None and ins.src.kind == "mem"
                and ins.src.base is None and ins.src.index is None
                and ins.src.absolute == INVALID_IAT and ins.raw == INVALID_CALL_BYTES
            ):
                raise RuntimeError(f"invalid tag is not an exact direct IAT call at 0x{site:08X}")
            actual_invalid_sites.add(site)
        for ins in decoded.instructions.values():
            if ins.kind == "call" and ins.target in target_numbers:
                actual_target_calls.add((ins.va, ins.target))
    expected_invalid_sites = {
        site for pin in SERIALIZER_PINS for site in pin.invalid_sites
    }
    expected_target_calls = {
        pair for pin in SERIALIZER_PINS for pair in pin.container_calls
    }
    pinned_dataflow_calls = {
        (pin.call_va, pin.target_va) for pin in TARGET_DATAFLOW_PINS
    }
    if actual_invalid_sites != expected_invalid_sites or len(actual_invalid_sites) != 18:
        raise RuntimeError("executed invalid-call census drift")
    if actual_target_calls != expected_target_calls or len(actual_target_calls) != 14:
        raise RuntimeError(f"executed target-call census drift: {actual_target_calls}")
    if pinned_dataflow_calls != expected_target_calls or len(pinned_dataflow_calls) != 14:
        raise RuntimeError("target dataflow-pin census does not cover exact caller set")

    formal_sites: set[int] = set()
    for site, encoded, register, label in STREAM_FORMAL_BYTE_PINS:
        owners = [pin for pin in SERIALIZER_PINS if pin.start_va <= site < pin.end_va]
        if len(owners) != 1:
            raise RuntimeError(f"stream-formal owner drift at 0x{site:08X}")
        owner = owners[0]
        decoded = serializer_decodes[owner.start_va]
        ins = decoded.instructions.get(site)
        require_bytes(image_bytes, site, encoded, "stream formal")
        if ins is None or ins.kind != "mov":
            raise RuntimeError(f"stream formal is not MOV at 0x{site:08X}")
        _require_reg(ins.dst, register, label)
        if (
            ins.src is None or ins.src.kind != "mem" or ins.src.base != "esp"
            or ins.src.index is not None or ins.src.absolute is not None
        ):
            raise RuntimeError(f"stream formal source drift at 0x{site:08X}")
        depths = analyzer._stack_depths(owner.start_va).get(site, frozenset())
        if len(depths) != 1 or None in depths:
            raise RuntimeError(f"stream formal stack-depth ambiguity at 0x{site:08X}: {depths}")
        depth = next(iter(depths))
        assert depth is not None
        if ins.src.disp - depth != 4:
            raise RuntimeError(f"stream formal is not entry stack +4 at 0x{site:08X}")
        formal_sites.add(site)

    for pin in TARGET_DATAFLOW_PINS:
        owners = [
            owner for owner in SERIALIZER_PINS
            if owner.start_va <= pin.call_va < owner.end_va
        ]
        if len(owners) != 1:
            raise RuntimeError(f"target-call owner drift at 0x{pin.call_va:08X}")
        owner = owners[0]
        decoded = serializer_decodes[owner.start_va]
        call = decoded.instructions.get(pin.call_va)
        require_bytes(image_bytes, pin.window_va, pin.window_hex, "target dataflow window")
        if not (
            call is not None and call.kind == "call" and call.target == pin.target_va
            and call.raw[:1] == b"\xE8" and len(call.raw) == 5
        ):
            raise RuntimeError(f"target call drift at 0x{pin.call_va:08X}")
        _only_reaching_definition(
            analyzer, owner.start_va, "ecx", pin.call_va,
            pin.ecx_definition_va, "target mutable ECX",
        )
        if pin.ecx_origin == "STACK_LOCAL":
            _require_stack_local_lea(
                analyzer, decoded, owner.start_va, pin.ecx_definition_va,
                "ecx", "target ECX stack local",
            )
        elif pin.ecx_origin == "THIS_DERIVED_CONTAINER":
            if pin.container_register is None or pin.container_definition_va is None:
                raise RuntimeError(f"missing container origin pin at 0x{pin.call_va:08X}")
            ecx_definition = decoded.instructions.get(pin.ecx_definition_va)
            if ecx_definition is None or ecx_definition.kind != "mov":
                raise RuntimeError(f"container ECX definition drift at 0x{pin.ecx_definition_va:08X}")
            _require_reg(ecx_definition.dst, "ecx", "container ECX destination")
            _require_reg(ecx_definition.src, pin.container_register, "container ECX source")
            _only_reaching_definition(
                analyzer, owner.start_va, pin.container_register,
                pin.ecx_definition_va, pin.container_definition_va,
                "container register",
            )
            root = CONTAINER_ROOTS.get(pin.container_definition_va)
            if root is None:
                raise RuntimeError(f"unregistered container definition at 0x{pin.container_definition_va:08X}")
            root_register, root_va = root
            container_definition = decoded.instructions.get(pin.container_definition_va)
            root_definition = decoded.instructions.get(root_va)
            if root_definition is None or root_definition.kind != "mov":
                raise RuntimeError(f"this-root definition drift at 0x{root_va:08X}")
            _require_reg(root_definition.dst, root_register, "this-root destination")
            _require_reg(root_definition.src, "ecx", "this-root entry formal")
            if container_definition is None:
                raise RuntimeError(f"missing container definition at 0x{pin.container_definition_va:08X}")
            if container_definition.kind == "lea":
                _require_reg(container_definition.dst, pin.container_register, "container LEA destination")
                if (
                    container_definition.src is None
                    or container_definition.src.kind != "mem"
                    or container_definition.src.base != root_register
                    or container_definition.src.index is not None
                    or container_definition.src.absolute is not None
                    or container_definition.src.disp <= 0
                ):
                    raise RuntimeError(f"container LEA origin drift at 0x{pin.container_definition_va:08X}")
                _only_reaching_definition(
                    analyzer, owner.start_va, root_register,
                    pin.container_definition_va, root_va, "container LEA this-root",
                )
            elif container_definition.kind == "add":
                _require_reg(container_definition.dst, pin.container_register, "container ADD destination")
                if (
                    container_definition.src is None
                    or container_definition.src.kind != "imm"
                    or container_definition.src.imm is None
                    or container_definition.src.imm <= 0
                    or root_register != pin.container_register
                ):
                    raise RuntimeError(f"container ADD origin drift at 0x{pin.container_definition_va:08X}")
                _only_reaching_definition(
                    analyzer, owner.start_va, pin.container_register,
                    pin.container_definition_va, root_va, "container ADD this-root",
                )
            else:
                raise RuntimeError(f"unsupported container definition at 0x{pin.container_definition_va:08X}")
        else:
            raise RuntimeError(f"unknown ECX origin at 0x{pin.call_va:08X}")

        for argument in pin.args:
            push = decoded.instructions.get(argument.push_va)
            if push is None or push.kind != "push":
                raise RuntimeError(f"target argument is not PUSH at 0x{argument.push_va:08X}")
            _require_reg(push.src, argument.register, "target argument register")
            _only_reaching_definition(
                analyzer, owner.start_va, argument.register, argument.push_va,
                argument.definition_va, "target argument",
            )
            if argument.origin == "STACK_LOCAL":
                _require_stack_local_lea(
                    analyzer, decoded, owner.start_va, argument.definition_va,
                    argument.register, "target argument stack local",
                )
            elif argument.origin == "NONSTREAM_ENTRY_FORMAL_SLOT":
                entry_relative = _stack_lea_entry_relative(
                    analyzer, decoded, owner.start_va, argument.definition_va,
                    argument.register, "target non-stream entry-formal slot",
                )
                if entry_relative != 8:
                    raise RuntimeError(
                        f"non-stream formal slot drift at 0x{argument.definition_va:08X}: "
                        f"entry-relative={entry_relative:+d}"
                    )
            elif argument.origin == "REUSED_STREAM_SLOT_AFTER_KILL_AND_WIRE_READ":
                if (
                    owner.start_va != 0x00737FD0
                    or argument.definition_va != 0x007380AB
                    or pin.call_va != 0x007380B7
                ):
                    raise RuntimeError("unexpected reused stream-slot proof identity")
                entry_relative = _stack_lea_entry_relative(
                    analyzer, decoded, owner.start_va, argument.definition_va,
                    argument.register, "reused stream-slot target argument",
                )
                if entry_relative != 4:
                    raise RuntimeError("reused stream-slot address is not entry +4")
                dominators = _dominators(decoded)
                required_dominators = {0x00737FD9, 0x007380A2, 0x007380A6}
                if not required_dominators.issubset(dominators.get(pin.call_va, frozenset())):
                    raise RuntimeError(
                        f"stream-slot kill/read do not dominate target: "
                        f"{dominators.get(pin.call_va, frozenset())}"
                    )
                post_read_chain = (
                    0x007380A6, 0x007380AB, 0x007380AF, 0x007380B0,
                    0x007380B4, 0x007380B5, 0x007380B7,
                )
                for left, right in zip(post_read_chain, post_read_chain[1:]):
                    if decoded.successors.get(left) != (right,):
                        raise RuntimeError(
                            f"reused stream-slot post-read CFG drift: "
                            f"0x{left:08X}->0x{right:08X}"
                        )
                    if decoded.predecessors.get(right) != (left,):
                        raise RuntimeError(
                            f"reused stream-slot alternate path at 0x{right:08X}"
                        )

                zero = decoded.instructions.get(0x0073807A)
                kill = decoded.instructions.get(0x007380A2)
                if zero is None or zero.kind != "xor" or zero.raw != bytes.fromhex("33DB"):
                    raise RuntimeError("reused stream-slot zero definition drift")
                _require_reg(zero.dst, "ebx", "reused stream-slot zero destination")
                _require_reg(zero.src, "ebx", "reused stream-slot zero source")
                if kill is None or kill.kind != "mov":
                    raise RuntimeError("reused stream-slot kill store drift")
                _require_reg(kill.src, "ebx", "reused stream-slot kill value")
                if (
                    kill.dst is None or kill.dst.kind != "mem"
                    or kill.dst.base != "esp" or kill.dst.index is not None
                    or kill.dst.absolute is not None
                ):
                    raise RuntimeError("reused stream-slot kill destination drift")
                kill_depths = analyzer._stack_depths(owner.start_va).get(
                    kill.va, frozenset()
                )
                if len(kill_depths) != 1 or None in kill_depths:
                    raise RuntimeError("reused stream-slot kill depth ambiguity")
                kill_depth = next(iter(kill_depths))
                assert kill_depth is not None
                if kill.dst.disp - kill_depth != 4:
                    raise RuntimeError("kill store does not overwrite entry stream slot")
                _only_reaching_definition(
                    analyzer, owner.start_va, "ebx", kill.va,
                    0x0073807A, "reused stream-slot zero",
                )

                wire_pointer = decoded.instructions.get(0x00738099)
                wire_push = decoded.instructions.get(0x0073809D)
                wire_ecx = decoded.instructions.get(0x007380A0)
                wire_call = decoded.instructions.get(0x007380A6)
                wire_entry_relative = _stack_lea_entry_relative(
                    analyzer, decoded, owner.start_va, 0x00738099, "edx",
                    "reused stream-slot wire-output pointer",
                )
                if wire_entry_relative != 4:
                    raise RuntimeError("wire output does not reuse entry stream slot")
                if wire_push is None or wire_push.kind != "push":
                    raise RuntimeError("missing reused stream-slot wire pointer PUSH")
                _require_reg(wire_push.src, "edx", "wire-output pointer push")
                _only_reaching_definition(
                    analyzer, owner.start_va, "edx", wire_push.va,
                    0x00738099, "wire-output pointer",
                )
                if wire_ecx is None or wire_ecx.kind != "mov":
                    raise RuntimeError("wire stream ECX definition drift")
                _require_reg(wire_ecx.dst, "ecx", "wire stream ECX destination")
                _require_reg(wire_ecx.src, "ebp", "wire stream ECX source")
                _only_reaching_definition(
                    analyzer, owner.start_va, "ecx", 0x007380A6,
                    0x007380A0, "wire stream ECX",
                )
                _only_reaching_definition(
                    analyzer, owner.start_va, "ebp", 0x007380A0,
                    0x00737FD9, "preserved stream register",
                )
                _only_reaching_definition(
                    analyzer, owner.start_va, "ebp", pin.call_va,
                    0x00737FD9, "stream register after slot reuse",
                )
                if not (
                    wire_call is not None and wire_call.kind == "call"
                    and wire_call.target == 0x0089A640
                    and wire_call.raw[:1] == b"\xE8" and len(wire_call.raw) == 5
                ):
                    raise RuntimeError("reused stream-slot wire-read call drift")
            elif argument.origin == "CONTAINER_NODE":
                base_pin = NODE_ARG_BASES.get(argument.definition_va)
                if base_pin is None:
                    raise RuntimeError(f"missing node-base pin at 0x{argument.definition_va:08X}")
                base_register, base_definition_va = base_pin
                definition = decoded.instructions.get(argument.definition_va)
                if definition is None or definition.kind != "mov":
                    raise RuntimeError(f"node argument definition drift at 0x{argument.definition_va:08X}")
                _require_reg(definition.dst, argument.register, "node argument destination")
                if (
                    definition.src is None or definition.src.kind != "mem"
                    or definition.src.base != base_register
                    or definition.src.index is not None
                    or definition.src.absolute is not None
                    or definition.src.disp != 4
                ):
                    raise RuntimeError(f"node argument memory origin drift at 0x{argument.definition_va:08X}")
                _only_reaching_definition(
                    analyzer, owner.start_va, base_register,
                    argument.definition_va, base_definition_va, "node-base register",
                )
                base_definition = decoded.instructions.get(base_definition_va)
                if base_definition is None or base_definition.kind != "mov":
                    raise RuntimeError(f"node-base definition drift at 0x{base_definition_va:08X}")
                _require_reg(base_definition.dst, base_register, "node-base destination")
                if (
                    base_definition.src is None or base_definition.src.kind != "mem"
                    or base_definition.src.base != "ebp"
                    or base_definition.src.index is not None
                    or base_definition.src.absolute is not None
                    or base_definition.src.disp <= 0
                ):
                    raise RuntimeError(f"node-base is not this-derived at 0x{base_definition_va:08X}")
                _only_reaching_definition(
                    analyzer, owner.start_va, "ebp", base_definition_va,
                    0x00656D5C, "node-base this-root",
                )
            else:
                raise RuntimeError(f"unknown target argument origin at 0x{argument.push_va:08X}")

        mutable_definitions = {
            pin.ecx_definition_va,
            *(argument.definition_va for argument in pin.args),
        }
        if mutable_definitions & formal_sites:
            raise RuntimeError(f"stream/mutable definition alias at 0x{pin.call_va:08X}")

    if len(TARGET_DATAFLOW_PINS) != 14 or len(formal_sites) != 7:
        raise RuntimeError("target/formal proof census drift")
    return {
        "graph_spans": len(GRAPH_SPANS),
        "graph_cfg_nodes": sum(len(decoded.instructions) for decoded in graph_decodes.values()),
        "graph_call_sites": len(actual_calls),
        "register_iat_sites": len(EXPECTED_REGISTER_IAT_REACHING),
        "serializer_spans": len(SERIALIZER_PINS),
        "serializer_cfg_nodes": sum(
            len(decoded.instructions) for decoded in serializer_decodes.values()
        ),
        "invalid_call_sites": len(actual_invalid_sites),
        "target_call_sites": len(actual_target_calls),
        "stream_formals": len(formal_sites),
    }


def existing_base_identities(external: Path) -> dict[tuple[str, str, str], list[str]]:
    result: dict[tuple[str, str, str], list[str]] = {}
    for name in PRIOR_A2_OVERLAY_NAMES:
        path = external / name
        fields, rows = read_tsv_with_lines(path)
        if not {"base_file", "base_line", "base_row_key"}.issubset(fields):
            continue
        for line, row in rows:
            identity = (row["base_file"], row["base_line"], row["base_row_key"])
            if identity[0] == "N/A" or identity[1] == "N/A" or identity[2] == "N/A":
                continue
            result.setdefault(identity, []).append(f"{path.name}:{line}")
    return result


def existing_provenance_keys(external: Path) -> dict[str, list[str]]:
    """Census prior overlay key namespaces so new provenance cannot collide."""
    result: dict[str, list[str]] = {}
    names = tuple(dict.fromkeys((*PRIOR_A2_OVERLAY_NAMES, *PRIOR_PRIORITY_OVERLAY_SHA256)))
    for name in names:
        path = external / name
        fields, rows = read_tsv_with_lines(path)
        key_columns = [name for name in ("delta_key", "dedup_key") if name in fields]
        for line, row in rows:
            for column in key_columns:
                value = row[column]
                if value and value != "N/A":
                    result.setdefault(value, []).append(
                        f"{path.name}:{line}:{column}"
                    )
    return result


def make_a2_remove(
    *, base_file: str, line: int, fields: Sequence[str], row: Mapping[str, str],
    slot: bool, change_type: str, resolution: str,
) -> dict[str, str]:
    row_key = canonical_row_key(fields, row)
    old_order = row["new_order"] if slot else row["order"]
    old_tag = row["new_tag"] if slot else row["tag"]
    old_offset = row["new_field_offset"] if slot else row["field_offset"]
    old_len = row["new_len"] if slot else row["len"]
    span_start = row["new_span_start"] if slot else row["span_start"]
    span_end = row["new_span_end"] if slot else row["span_end"]
    span_hash = row["new_span_sha256"] if slot else row["span_sha256"]
    file_off = row["new_file_off_claim"] if slot else row["file_off_claim"]
    action = "REMOVE_OVERLAY_NONWIRE_ROW" if slot else "REMOVE_NONWIRE_ROW"
    values = {
        "action": action,
        "change_type": change_type,
        "base_file": base_file,
        "base_line": str(line),
        "base_row_key": row_key,
        "base_delta_key": row["delta_key"] if slot else "N/A",
        "message": row["message"],
        "direction(W/R)": row["direction(W/R)"],
        "old_order": old_order,
        "old_tag": old_tag,
        "old_field_offset": old_offset,
        "old_len": old_len,
        "new_wire_order": "N/A",
        "new_tag": "N/A",
        "new_field_offset": "N/A",
        "new_len": "N/A",
        "new_gate_condition": "N/A",
        "resolution": resolution,
        "evidence_ticket": EVIDENCE_TICKET,
        "evidence_span_start": span_start,
        "evidence_span_end": span_end,
        "evidence_span_sha256": span_hash,
        "evidence_file_off": file_off,
        "source": "IMAGE",
    }
    values["delta_key"] = make_delta_key(
        ("A2", action, base_file, str(line), row_key, change_type)
    )
    return values


def verify_delta_unique(rows: Sequence[Mapping[str, str]], label: str) -> None:
    keys = [row["delta_key"] for row in rows]
    identities = [(row["base_file"], row["base_line"], row["base_row_key"]) for row in rows]
    semantic = [
        (row["message"], row["direction(W/R)"], row["old_order"],
         row["old_tag"], row["evidence_file_off"])
        for row in rows
    ]
    if len(keys) != len(set(keys)):
        raise RuntimeError(f"{label}: duplicate delta_key")
    if len(identities) != len(set(identities)):
        raise RuntimeError(f"{label}: duplicate base-row identity")
    if len(semantic) != len(set(semantic)):
        raise RuntimeError(f"{label}: duplicate effective semantic row")
    if any(row["source"] != "IMAGE" for row in rows):
        raise RuntimeError(f"{label}: mixed evidence source")
    if any(row["action"] not in ("REMOVE_NONWIRE_ROW", "REMOVE_OVERLAY_NONWIRE_ROW") for row in rows):
        raise RuntimeError(f"{label}: unchanged/copied row is forbidden")


def build_a2_deltas(
    external: Path, image: bytes, guard_by_site: Mapping[int, GuardPin],
) -> tuple[
    list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, int]
]:
    base_fields, base_rows = read_tsv_with_lines(external / A2_NAME)
    slot_fields, slot_rows = read_tsv_with_lines(external / SLOT34_A2_NAME)
    old_identities = existing_base_identities(external)

    invalid_rows: list[dict[str, str]] = []
    target_rows: list[dict[str, str]] = []
    delete_target_rows: list[dict[str, str]] = []
    invalid_raw_v1 = 0
    invalid_effective_v1 = 0
    invalid_raw_slot = 0

    for line, row in base_rows:
        if row.get("tag") == INVALID_TAG:
            invalid_raw_v1 += 1
            row_key = canonical_row_key(base_fields, row)
            identity = (A2_NAME, str(line), row_key)
            if identity in old_identities:
                continue
            invalid_effective_v1 += 1
            if row["message"] not in INVALID_MESSAGES:
                continue
            if row["source"] != "IMAGE" or row["field_offset"] != "UNKNOWN(invalid_parameter_import_call_wire_effect_unproved)" or row["len"] != "N/A":
                raise RuntimeError(f"V1 invalid row provenance drift at line {line}")
            call_va, file_off, function_va = parse_gate_call(row["gate_condition"])
            serializer = serializer_for_message(row["message"])
            if call_va not in serializer.invalid_sites or function_va != serializer.start_va:
                raise RuntimeError(f"V1 invalid row outside reviewed serializer graph at line {line}")
            if file_off != call_va - VA_TO_FILE_DELTA or row["file_off_claim"] != f"0x{file_off:08X}":
                raise RuntimeError(f"V1 invalid callsite/file mapping drift at line {line}")
            if row["span_start"] != f"0x{serializer.start_va:08X}" or row["span_end"] != f"0x{serializer.end_va:08X}" or row["span_sha256"] != serializer.sha256:
                raise RuntimeError(f"V1 invalid serializer span drift at line {line}")
            guard = guard_by_site[call_va]
            invalid_rows.append(make_a2_remove(
                base_file=A2_NAME, line=line, fields=base_fields, row=row, slot=False,
                change_type="GUARDED_ZERO_ARGUMENT_COMPILER_RUNTIME_NONWIRE",
                resolution=f"{guard.condition};EXACT_ZERO_ARGUMENT_DIRECT_IAT_CALL;EXECUTED_SERIALIZER_CFG;PINNED_CONTAINER_GRAPH",
            ))
        if row.get("tag") in TARGET_TAGS:
            if row["source"] != "IMAGE" or row["field_offset"] != "UNKNOWN(direct_call_not_proven_serializer)":
                raise RuntimeError(f"V1 target row provenance drift at line {line}")
            call_off = int(row["file_off_claim"], 16)
            call_va = call_off + VA_TO_FILE_DELTA
            target_va = rel32_target(image, call_va)
            if row["tag"] != f"CALL_UNCLASSIFIED:0x{target_va:08X}":
                raise RuntimeError(f"V1 target/call mismatch at line {line}")
            serializer = serializer_for_message(row["message"])
            if (call_va, target_va) not in serializer.container_calls:
                raise RuntimeError(f"V1 target row outside executed serializer graph at line {line}")
            identity = (A2_NAME, str(line), canonical_row_key(base_fields, row))
            if identity in old_identities:
                raise RuntimeError(f"V1 target row already handled: line {line} {old_identities[identity]}")
            target_rows.append(make_a2_remove(
                base_file=A2_NAME, line=line, fields=base_fields, row=row, slot=False,
                change_type="FIXED_CONTAINER_HELPER_GRAPH_NONWIRE",
                resolution="EXECUTED_CFG_REACHING_DEFINITION;STACK_LOCAL_OR_THIS_DERIVED_DISJOINT_FROM_STREAM_FORMAL",
            ))
        if row.get("tag") == DELETE_TARGET_TAG:
            if row["source"] != "IMAGE" or row["field_offset"] != "UNKNOWN(direct_call_not_proven_serializer)":
                raise RuntimeError(f"V1 delete-target row provenance drift at line {line}")
            if row["message"] != "CBuffConditionState":
                raise RuntimeError(f"unexpected delete-target message at line {line}")
            call_off = int(row["file_off_claim"], 16)
            call_va = call_off + VA_TO_FILE_DELTA
            if rel32_target(image, call_va) != 0x00656690:
                raise RuntimeError(f"V1 delete-target/call mismatch at line {line}")
            serializer = serializer_for_message(row["message"])
            if (call_va, 0x00656690) not in serializer.container_calls:
                raise RuntimeError(f"V1 delete-target outside pinned serializer graph at line {line}")
            identity = (A2_NAME, str(line), canonical_row_key(base_fields, row))
            if identity in old_identities:
                raise RuntimeError(f"V1 delete-target row already handled: line {line} {old_identities[identity]}")
            delete_target_rows.append(make_a2_remove(
                base_file=A2_NAME, line=line, fields=base_fields, row=row, slot=False,
                change_type="RECURSIVE_NODE_DELETE_HELPER_NONWIRE",
                resolution="SELF_RECURSION_AND_EXACT_OPERATOR_DELETE_THUNK;EXECUTED_CFG_REACHING_DEFINITION;THIS_DERIVED_NODE_DISJOINT_FROM_STREAM_FORMAL",
            ))

    for line, row in slot_rows:
        if row.get("new_tag") == INVALID_TAG:
            invalid_raw_slot += 1
            if row["message"] not in INVALID_MESSAGES:
                continue
            identity = (SLOT34_A2_NAME, str(line), canonical_row_key(slot_fields, row))
            if identity in old_identities:
                raise RuntimeError(f"slot34 invalid row already handled: line {line} {old_identities[identity]}")
            if row["action"] != "ADD_CORRECTED_SLOT34_ROW" or row["source"] != "IMAGE" or row["new_field_offset"] != "UNKNOWN(invalid_parameter_import_call_wire_effect_unproved)" or row["new_len"] != "N/A":
                raise RuntimeError(f"slot34 invalid row provenance drift at line {line}")
            call_va, file_off, function_va = parse_gate_call(row["new_gate_condition"])
            serializer = serializer_for_message(row["message"])
            if call_va not in serializer.invalid_sites or function_va != serializer.start_va:
                raise RuntimeError(f"slot34 invalid row outside reviewed serializer graph at line {line}")
            if file_off != call_va - VA_TO_FILE_DELTA or row["new_file_off_claim"] != f"0x{file_off:08X}":
                raise RuntimeError(f"slot34 invalid callsite/file mapping drift at line {line}")
            if row["new_span_start"] != f"0x{serializer.start_va:08X}" or row["new_span_end"] != f"0x{serializer.end_va:08X}" or row["new_span_sha256"] != serializer.sha256:
                raise RuntimeError(f"slot34 invalid serializer span drift at line {line}")
            guard = guard_by_site[call_va]
            invalid_rows.append(make_a2_remove(
                base_file=SLOT34_A2_NAME, line=line, fields=slot_fields, row=row, slot=True,
                change_type="GUARDED_ZERO_ARGUMENT_COMPILER_RUNTIME_NONWIRE",
                resolution=f"{guard.condition};EXACT_ZERO_ARGUMENT_DIRECT_IAT_CALL;EXECUTED_SERIALIZER_CFG;PINNED_CONTAINER_GRAPH",
            ))
        if row.get("new_tag") in TARGET_TAGS:
            if row["action"] != "ADD_CORRECTED_SLOT34_ROW" or row["source"] != "IMAGE" or row["new_field_offset"] != "UNKNOWN(direct_call_not_proven_serializer)":
                raise RuntimeError(f"slot34 target row provenance drift at line {line}")
            call_off = int(row["new_file_off_claim"], 16)
            call_va = call_off + VA_TO_FILE_DELTA
            target_va = rel32_target(image, call_va)
            if row["new_tag"] != f"CALL_UNCLASSIFIED:0x{target_va:08X}":
                raise RuntimeError(f"slot34 target/call mismatch at line {line}")
            serializer = serializer_for_message(row["message"])
            if (call_va, target_va) not in serializer.container_calls:
                raise RuntimeError(f"slot34 target row outside executed serializer graph at line {line}")
            identity = (SLOT34_A2_NAME, str(line), canonical_row_key(slot_fields, row))
            if identity in old_identities:
                raise RuntimeError(f"slot34 target row already handled: line {line} {old_identities[identity]}")
            target_rows.append(make_a2_remove(
                base_file=SLOT34_A2_NAME, line=line, fields=slot_fields, row=row, slot=True,
                change_type="FIXED_CONTAINER_HELPER_GRAPH_NONWIRE",
                resolution="EXECUTED_CFG_REACHING_DEFINITION;STACK_LOCAL_OR_THIS_DERIVED_DISJOINT_FROM_STREAM_FORMAL",
            ))
        if row.get("new_tag") == DELETE_TARGET_TAG:
            raise RuntimeError(f"unexpected slot34 delete-target row at line {line}")

    # The raw V1 census is 638, but three CTracePathVital rows were already
    # removed by PF_A2_POST_V1_STATIC_DELTA.  They must never be emitted again.
    expected_prior_overlap = {
        (A2_NAME, "5493"), (A2_NAME, "5494"), (A2_NAME, "5495")
    }
    seen_prior_overlap = {
        (base_file, line)
        for (base_file, line, _key), refs in old_identities.items()
        if base_file == A2_NAME and line in {"5493", "5494", "5495"}
        and any(ref.startswith(POST_V1_NAME + ":") for ref in refs)
    }
    if seen_prior_overlap != expected_prior_overlap:
        raise RuntimeError(f"prior invalid-row removal census drift: {seen_prior_overlap}")
    counts = {
        "invalid_raw_v1": invalid_raw_v1,
        "invalid_effective_v1": invalid_effective_v1,
        "invalid_raw_slot": invalid_raw_slot,
        "invalid_emitted_v1": sum(row["base_file"] == A2_NAME for row in invalid_rows),
        "invalid_emitted_slot": sum(row["base_file"] == SLOT34_A2_NAME for row in invalid_rows),
        "invalid_emitted_w": sum(row["direction(W/R)"] == "W" for row in invalid_rows),
        "invalid_emitted_r": sum(row["direction(W/R)"] == "R" for row in invalid_rows),
        "target_emitted_v1": sum(row["base_file"] == A2_NAME for row in target_rows),
        "target_emitted_slot": sum(row["base_file"] == SLOT34_A2_NAME for row in target_rows),
        "delete_target_emitted_v1": len(delete_target_rows),
    }
    expected_counts = {
        "invalid_raw_v1": 638, "invalid_effective_v1": 635, "invalid_raw_slot": 296,
        "invalid_emitted_v1": 24, "invalid_emitted_slot": 24,
        "invalid_emitted_w": 24, "invalid_emitted_r": 24,
        "target_emitted_v1": 16, "target_emitted_slot": 16,
        "delete_target_emitted_v1": 4,
    }
    if counts != expected_counts:
        raise RuntimeError(f"A2 reviewed-scope census drift: {counts}")
    invalid_rows.sort(key=lambda row: (row["base_file"], int(row["base_line"])))
    target_rows.sort(key=lambda row: (row["base_file"], int(row["base_line"])))
    delete_target_rows.sort(key=lambda row: (row["base_file"], int(row["base_line"])))
    verify_delta_unique(invalid_rows, "invalid delta")
    verify_delta_unique(target_rows, "target delta")
    verify_delta_unique(delete_target_rows, "delete-target delta")
    all_identities = [
        (row["base_file"], row["base_line"], row["base_row_key"])
        for row in (*invalid_rows, *target_rows, *delete_target_rows)
    ]
    if len(all_identities) != len(set(all_identities)):
        raise RuntimeError("invalid/target overlay cross-duplicate")
    all_semantic = [
        (row["message"], row["direction(W/R)"], row["old_order"],
         row["old_tag"], row["evidence_file_off"])
        for row in (*invalid_rows, *target_rows, *delete_target_rows)
    ]
    if len(all_semantic) != len(set(all_semantic)):
        raise RuntimeError("invalid/target overlay cross-semantic duplicate")
    if any(identity in old_identities for identity in all_identities):
        raise RuntimeError("new A2 overlay overlaps an older overlay")
    return invalid_rows, target_rows, delete_target_rows, counts


def replay_final_a2_for_priority(
    external: Path, v2_validator: types.ModuleType,
    removal_rows: Sequence[Mapping[str, str]],
) -> dict[str, int]:
    """Replay effective V2, apply this exact overlay in memory, then gate CLOSED."""
    inputs_before = v2_validator.verify_pinned_inputs(external, False)
    _registry, effective, _candidates, v2_counts = (
        v2_validator.apply_effective_overlays(external)
    )
    removals_applied = 0
    seen_targets: set[tuple[str, str, str]] = set()
    for row in removal_rows:
        target = (row["base_file"], row["base_line"], row["base_row_key"])
        if target in seen_targets:
            raise RuntimeError(f"effective replay duplicate removal target: {target}")
        seen_targets.add(target)
        if row["source"] != "IMAGE" or not row["action"].startswith("REMOVE"):
            raise RuntimeError("effective replay received non-removal/mixed-source row")
        if row["base_file"] == A2_NAME:
            if row["base_delta_key"] != "N/A":
                raise RuntimeError("V1 effective replay row has a foreign base_delta_key")
            evidence_key = row["base_row_key"]
        elif row["base_file"] == SLOT34_A2_NAME:
            if row["base_delta_key"] == "N/A":
                raise RuntimeError("slot34 effective replay row lacks base_delta_key")
            evidence_key = row["base_delta_key"]
        else:
            raise RuntimeError(f"effective replay unexpected base file: {row['base_file']}")
        bucket = effective[(row["message"], row["direction(W/R)"])]
        candidates = [
            (index, field_value)
            for index, field_value in enumerate(bucket)
            if field_value.evidence_key == evidence_key
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                f"effective replay target cardinality drift: {row['message']}:"
                f"{row['direction(W/R)']}:{evidence_key}:{len(candidates)}"
            )
        index, field_value = candidates[0]
        expected_old = (
            row["old_order"], row["old_tag"], row["old_field_offset"], row["old_len"]
        )
        actual_old = (
            field_value.wire_order, field_value.tag,
            field_value.field_offset, field_value.length,
        )
        if actual_old != expected_old:
            raise RuntimeError(
                f"effective replay old-row contract drift: {row['message']}:"
                f"{row['direction(W/R)']}:{actual_old}!={expected_old}"
            )
        del bucket[index]
        removals_applied += 1
    if removals_applied != 84 or len(seen_targets) != 84:
        raise RuntimeError(
            f"effective replay removal census drift: {removals_applied}/{len(seen_targets)}"
        )

    unknown_total = 0
    nonempty_min: int | None = None
    for message in sorted(INVALID_MESSAGES):
        fields = [
            field_value
            for direction in ("W", "R")
            for field_value in effective[(message, direction)]
        ]
        reasons: set[str] = set()
        for field_value in fields:
            matches = re.findall(
                r"UNKNOWN\(([^()]*)\)", str(field_value.field_offset)
            )
            reasons.update(reason for reason in matches if reason)
            if field_value.tag == "UNKNOWN" and not matches:
                reasons.add("unknown_tag")
        nonempty = sum(field_value.tag != "EMPTY" for field_value in fields)
        unknown_total += len(reasons)
        nonempty_min = nonempty if nonempty_min is None else min(nonempty_min, nonempty)
        if reasons or nonempty <= 0:
            raise RuntimeError(
                f"Priority CLOSED rejected by final effective A2 replay: {message}: "
                f"UNKNOWN={sorted(reasons)} nonempty={nonempty}"
            )
    inputs_after = v2_validator.verify_pinned_inputs(external, False)
    if inputs_after != inputs_before:
        raise RuntimeError("effective-V2 pinned inputs changed during Priority replay")
    return {
        "v2_effective_rows": int(v2_counts["effective_rows"]),
        "proposed_removed": removals_applied,
        "closed_messages": len(INVALID_MESSAGES),
        "unknown_residual": unknown_total,
        "minimum_nonempty": 0 if nonempty_min is None else nonempty_min,
    }


def build_priority_delta(
    external: Path, v2_validator: types.ModuleType,
    invalid_rows: Sequence[Mapping[str, str]],
    target_rows: Sequence[Mapping[str, str]],
    delete_target_rows: Sequence[Mapping[str, str]],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    replay = replay_final_a2_for_priority(
        external, v2_validator,
        (*invalid_rows, *target_rows, *delete_target_rows),
    )
    base_fields, base_rows = read_tsv_with_lines(external / PRIORITY_NAME)
    slot_fields, slot_rows = read_tsv_with_lines(external / SLOT34_PRIORITY_NAME)
    output: list[dict[str, str]] = []
    for message in sorted(INVALID_MESSAGES):
        expected_file, expected_line = EXPECTED_PRIORITY_LINES[message]
        if message in BASE_PRIORITY_MESSAGES:
            candidates = [(line, row) for line, row in base_rows if row["message"] == message]
            if len(candidates) != 1:
                raise RuntimeError(f"base Priority row mapping drift for {message}")
            line, row = candidates[0]
            if line != expected_line or row["serializer_status"] != "OPEN" or row["structural_status"] != "OPEN":
                raise RuntimeError(f"base Priority status drift for {message}")
            expected_blocker = "direct_call_not_proven_serializer | invalid_parameter_import_call_wire_effect_unproved"
            if row["serializer_blockers"] != expected_blocker or row["blocker"] != expected_blocker:
                raise RuntimeError(f"base Priority blocker drift for {message}")
            row_key = canonical_row_key(base_fields, row)
            values = {
                "action": "CHANGED", "base_file": PRIORITY_NAME,
                "base_line": str(line), "base_row_key": row_key,
                "base_delta_key": "N/A", "message": message, "priority": row["priority"],
                "old_registry_identity_status": row["registry_identity_status"],
                "new_registry_identity_status": row["registry_identity_status"],
                "old_registry_identity_missing": row["registry_identity_missing"],
                "new_registry_identity_missing": row["registry_identity_missing"],
                "old_serializer_status": row["serializer_status"],
                "new_serializer_status": "CLOSED",
                "old_serializer_blockers": row["serializer_blockers"],
                "new_serializer_blockers": "N/A",
                "old_structural_status": row["structural_status"],
                "new_structural_status": "CLOSED",
                "old_blocker": row["blocker"], "new_blocker": "N/A",
                "evidence_ticket": EVIDENCE_TICKET,
                "closure_scope": "STATIC_WIRE_STRUCTURE_ONLY;REVIEWED_GUARD_SITES_ONLY;EXECUTED_CFG_REACHING_DEFINITION;V1_IMMUTABLE",
                "source": "IMAGE",
            }
        else:
            candidates = [(line, row) for line, row in slot_rows if row["message"] == message]
            if len(candidates) != 1:
                raise RuntimeError(f"slot34 Priority row mapping drift for {message}")
            line, row = candidates[0]
            if line != expected_line or row["new_serializer_status"] != "OPEN" or row["new_structural_status"] != "OPEN":
                raise RuntimeError(f"slot34 Priority status drift for {message}")
            expected_blocker = "direct_call_not_proven_serializer | invalid_parameter_import_call_wire_effect_unproved"
            if row["new_serializer_blockers"] != expected_blocker or row["new_blocker"] != expected_blocker:
                raise RuntimeError(f"slot34 Priority blocker drift for {message}")
            row_key = canonical_row_key(slot_fields, row)
            values = {
                "action": "CHANGED", "base_file": SLOT34_PRIORITY_NAME,
                "base_line": str(line), "base_row_key": row_key,
                "base_delta_key": row["delta_key"], "message": message,
                "priority": row["priority"],
                "old_registry_identity_status": row["new_registry_identity_status"],
                "new_registry_identity_status": row["new_registry_identity_status"],
                "old_registry_identity_missing": row["new_registry_identity_missing"],
                "new_registry_identity_missing": row["new_registry_identity_missing"],
                "old_serializer_status": row["new_serializer_status"],
                "new_serializer_status": "CLOSED",
                "old_serializer_blockers": row["new_serializer_blockers"],
                "new_serializer_blockers": "N/A",
                "old_structural_status": row["new_structural_status"],
                "new_structural_status": "CLOSED",
                "old_blocker": row["new_blocker"], "new_blocker": "N/A",
                "evidence_ticket": EVIDENCE_TICKET,
                "closure_scope": "STATIC_WIRE_STRUCTURE_ONLY;REVIEWED_GUARD_SITES_ONLY;EXECUTED_CFG_REACHING_DEFINITION;SLOT34_CHAINED;V1_IMMUTABLE",
                "source": "IMAGE",
            }
        if values["base_file"] != expected_file:
            raise RuntimeError(f"Priority base-file drift for {message}")
        values["delta_key"] = make_delta_key(
            ("PRIORITY", values["action"], values["base_file"], values["base_line"], row_key)
        )
        output.append(values)
    output.sort(key=lambda row: (int(row["priority"]), row["message"]))
    if len(output) != 7 or len({row["delta_key"] for row in output}) != 7:
        raise RuntimeError("Priority delta census/duplicate drift")
    if any(row["source"] != "IMAGE" or row["action"] != "CHANGED" for row in output):
        raise RuntimeError("Priority unchanged copy or mixed source")
    if {row["message"] for row in output} != INVALID_MESSAGES:
        raise RuntimeError("Priority message set drift")
    return output, replay


def report_text(
    invalid_rows: Sequence[Mapping[str, str]], target_rows: Sequence[Mapping[str, str]],
    delete_target_rows: Sequence[Mapping[str, str]],
    priority_rows: Sequence[Mapping[str, str]], counts: Mapping[str, int],
    negative: Mapping[str, int], executed: Mapping[str, int],
    priority_replay: Mapping[str, int],
) -> str:
    lines = [
        "# PF reviewed compiler-runtime and container-helper closure",
        "",
        "[MEASURED] IMAGE-only additive correction. Frozen V1 and every earlier overlay remain unchanged.",
        "",
        "## Outcome",
        "",
        f"- Removed **{len(invalid_rows)} guarded compiler-runtime analysis rows**: 24 frozen-V1 plus 24 slot-0x34 rows, W 24/R 24.",
        f"- Removed **{len(target_rows)} fixed container-helper rows**: 16 frozen-V1 plus 16 slot-0x34 rows.",
        f"- Removed **{len(delete_target_rows)} recursive node-delete helper rows** in a separate overlay. This target self-recurses and reaches only the exact `operator delete` import thunk.",
        f"- Emitted **{len(priority_rows)} changed Priority rows** and **0 unchanged copies**. The seven reviewed messages move from OPEN to CLOSED.",
        "- The invalid-parameter removal is intentionally not global. Of 638 raw frozen-V1 rows, three were already removed by `PF_A2_POST_V1_STATIC_DELTA.tsv`; 635 remain effective before this overlay. Together with 296 slot-0x34 rows that is 931 effective rows, but only the 48 rows whose 18 exact call sites pass the pinned per-site guard/container proof are removed here.",
        "- W/R rows are path-insensitive analysis rows. Their presence does not assert that each guard call executes in both modes.",
        "",
        "## Publication and acceptance boundary",
        "",
        f"Normal publication holds the exclusive O_EXCL lock `{PUBLISH_LOCK_NAME}`, stages and byte-verifies the complete five-file compiler set, journals each destination before replacement, rolls back on a caught failure, verifies every final byte, and writes this report last within that set. A hard kill intentionally leaves the lock stale so a later compiler publisher fails closed.",
        "",
        f"This five-file transaction is not the V3 acceptance marker. Root owns `{ACCEPTANCE_MANIFEST_NAME}` and must write it last only after all same-generation A2/Priority/status/validation artifacts pass their hash checks. Consumers must reject V3 whenever `{ACCEPTANCE_MANIFEST_NAME}` is absent or any manifest hash check fails.",
        "",
        "## Duplicate accounting",
        "",
        "| category | raw/source rows | already removed | emitted | unchanged copied | exact/key/semantic duplicate | source |",
        "|---|---:|---:|---:|---:|---:|---|",
        "| invalid import, frozen V1 | 638 | 3 | 24 | 0 | 0 | IMAGE |",
        "| invalid import, slot-0x34 | 296 | 0 | 24 | 0 | 0 | IMAGE |",
        "| three fixed targets, frozen V1 | 16 | 0 | 16 | 0 | 0 | IMAGE |",
        "| three fixed targets, slot-0x34 | 16 | 0 | 16 | 0 | 0 | IMAGE |",
        "| recursive node-delete target 0x00656690, frozen V1 | 4 | 0 | 4 | 0 | 0 | IMAGE |",
        "| Priority effective changes | 7 | 0 | 7 | 0 | 0 | IMAGE |",
        "",
        "The three excluded frozen-V1 rows are exactly `CTracePathVital` lines 5493-5495. Re-emitting them would be duplicated output; the generator requires their existing base-row-keyed removal and excludes them.",
        "",
        "## Exact import and per-site guard proof",
        "",
        "All 18 eligible sites are executed-decoder-confirmed exact direct `FF 15 C0 B4 C3 00` calls. PE import metadata resolves IAT `0x00C3B4C0` / file offset `0x008398C0` to `MSVCR90.dll!_invalid_parameter_noinfo` with descriptor `0x00C112DC`, lookup `0x00C118B4`, DLL name `0x00C1647C`, and symbol name `0x00C15C62`. Register-indirect and unknown targets are excluded.",
        "",
        "The imported operation has no parameters. Each eligible call is additionally pinned behind a local null/identity/boundary guard in one of the five serializers below; no stream formal is passed to the call. The same pinned serializer reaches one or more of the fully closed container helpers. This per-site conjunction, not the import name alone, is the removal proof.",
        "",
        "| serializer/messages | span | exact guard sites | fixed container calls | source |",
        "|---|---|---|---|---|",
    ]
    for pin in SERIALIZER_PINS:
        messages = ", ".join(f"`{message}`" for message in pin.messages)
        guards = ", ".join(f"`0x{site:08X}`" for site in pin.invalid_sites)
        calls = ", ".join(f"`0x{site:08X}->0x{target:08X}`" for site, target in pin.container_calls)
        lines.append(
            f"| {messages} | `0x{pin.start_va:08X}-0x{pin.end_va:08X}` / `{pin.sha256}` | {guards} | {calls} | IMAGE |"
        )
    lines += [
        "",
        "## Fixed container graph",
        "",
        "| role | span | bytes | file offset | executed CFG nodes | SHA-256 | source |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for pin in GRAPH_SPANS:
        lines.append(
            f"| {pin.role} | `0x{pin.start_va:08X}-0x{pin.end_va:08X}` | {pin.end_va-pin.start_va} | `0x{pin.file_off:08X}` | {pin.cfg_nodes} | `{pin.sha256}` | IMAGE |"
        )
    lines += [
        "",
        "The transitive fixed call graph contains only the executed nodes above and fixed imports/tail thunks for `basic_string<char>` construction/copy, `std::exception` construction, `operator new`, `operator delete`, `_CxxThrowException`, and the guarded `_invalid_parameter_noinfo` operation. Target `0x00656690` has a complete 23-node CFG, self-recurses at `0x006566A7`, and calls the exact `MSVCR90.dll!operator delete(void*)` thunk at `0x006566AF -> 0x00B37952 -> [0x00C3B82C]`. Its two CBuff callers are pinned at `0x00656E85` and `0x00656EAC`: arg1 comes from the two this-derived container node slots (`[EBP+0x38/+0x58]+0x04`) and ECX is the embedded container subobject (`EBP+0x20/+0x40`), not the stream formal. All register-indirect calls in the graph have singleton reaching definitions at exact IAT loads; no unresolved indirect target remains in this graph.",
        "",
        "### Executed CFG and non-alias gates",
        "",
        f"The hash-pinned `{DECODER_NAME}` source was executed against the pinned IMAGE. It decoded {executed['graph_spans']} graph spans / {executed['graph_cfg_nodes']} CFG nodes and {executed['serializer_spans']} serializer spans / {executed['serializer_cfg_nodes']} CFG nodes with zero decode errors. The exact graph census is {executed['graph_call_sites']} direct/indirect call or tail-jump sites; {executed['register_iat_sites']} register-indirect sites have singleton reaching IAT definitions.",
        "",
        f"For all {executed['target_call_sites']} physical container/delete target callsites, the audit binds ECX and every pushed mutable argument to an exact singleton reaching definition. Stack-address arguments resolve to negative entry-relative locals or to the distinct entry `+0x08` non-stream slot. The one apparent exception is `NPCAppearAttr`: its read path reuses entry `+0x04`, but stream capture `0x00737FD9`, zero-kill store `0x007380A2`, and exact wire-read call `0x007380A6` all dominate target `0x007380B7`; EBP retains the singleton stream definition while the old stack-slot value is killed and replaced. Container and heap-node arguments trace to the entry `this` formal through exact MOV/LEA/ADD chains. Separately, all {executed['stream_formals']} stream loads resolve to entry stack `+0x04`. This executed kill/reaching-definition boundary, not primitive/literal absence alone, is the target-removal proof.",
        "",
        "### Negative byte-pattern census",
        "",
        f"A whole raw-backed IMAGE byte-pattern census finds {negative['e8_89a600']} `E8 rel32` patterns targeting `0x0089A600` and {negative['e8_89a640']} targeting `0x0089A640`. These are raw patterns, not all instruction claims. Intersection with the {executed['graph_spans']} executed graph spans is **{negative['graph_e8_intersection']}**. A separate little-endian literal census for both primitive VAs inside those spans is **{negative['graph_literal_intersection']}**. The negative claim therefore comes from a whole-IMAGE pattern census plus exact span intersection, not from linear-disassembler failure.",
        "",
        "## Priority changes",
        "",
        f"The generator executes hash-pinned `{V2_VALIDATOR_NAME}` (`{V2_VALIDATOR_SHA256}`) to replay all {priority_replay['v2_effective_rows']} effective V2 A2 rows, applies exactly {priority_replay['proposed_removed']} proposed rows in memory by effective evidence key, and rechecks every pinned V2 input before and after. A Priority close is emitted only because all {priority_replay['closed_messages']} reviewed messages have zero remaining UNKNOWN reasons and at least one non-EMPTY effective tag (measured minimum {priority_replay['minimum_nonempty']}). Raw-table blocker strings are not the closure gate.",
        "",
        "| message | priority | effective base | old | new | source |",
        "|---|---:|---|---|---|---|",
    ]
    for row in priority_rows:
        base = f"`{row['base_file']}:{row['base_line']}`"
        if row["base_delta_key"] != "N/A":
            base += f" / delta `{row['base_delta_key']}`"
        lines.append(
            f"| `{row['message']}` | {row['priority']} | {base} | {row['old_serializer_status']} | {row['new_serializer_status']} | IMAGE |"
        )
    lines += [
        "",
        "## Nonclaims and stop rule",
        "",
        "- No container key/value meaning, gameplay meaning, runtime behavior, capture agreement, or server behavior is claimed.",
        "- The other 883 effective direct-IAT invalid-parameter rows remain unresolved. This report does not generalize from 18 reviewed sites to them.",
        "- No register-indirect invalid-parameter row and no generic/unknown call target is removed.",
        "- Resume only with a new per-site guard/path/non-alias proof or an independently reviewed proof that safely covers a wider exact set.",
        "",
    ]
    return "\n".join(lines)


def build(external: Path) -> dict[Path, bytes]:
    image_path = external.parent.parent / "GameClient" / "GameClient.local.bin"
    require_hash(image_path, IMAGE_SHA256, "IMAGE")
    require_hash(external / A2_NAME, A2_SHA256, "V1 A2")
    require_hash(external / SLOT34_A2_NAME, SLOT34_A2_SHA256, "slot34 A2")
    require_hash(external / POST_V1_NAME, POST_V1_SHA256, "post-V1 A2")
    require_hash(external / PRIORITY_NAME, PRIORITY_SHA256, "V1 Priority")
    require_hash(external / SLOT34_PRIORITY_NAME, SLOT34_PRIORITY_SHA256, "slot34 Priority")
    for name, digest in PRIOR_PRIORITY_OVERLAY_SHA256.items():
        require_hash(external / name, digest, f"prior Priority overlay {name}")
    v2_validator = load_pinned_v2_validator(external)
    v2_inputs_before = v2_validator.verify_pinned_inputs(external, False)
    image = image_path.read_bytes()
    if sha256_bytes(image) != IMAGE_SHA256:
        raise RuntimeError("pinned IMAGE hash drift")
    image_base, sections, imports = parse_pe(image)
    if image_base != 0x00400000:
        raise RuntimeError(f"IMAGE base drift: 0x{image_base:08X}")
    verify_imports(imports)
    negative = verify_graph(image, sections)
    guard_by_site = verify_serializer_proof(image)
    executed = verify_executed_cfg_and_dataflow(external, image_path, image)
    invalid_rows, target_rows, delete_target_rows, counts = build_a2_deltas(
        external, image, guard_by_site
    )
    priority_rows, priority_replay = build_priority_delta(
        external, v2_validator, invalid_rows, target_rows, delete_target_rows
    )
    new_keys = [
        row["delta_key"]
        for row in (*invalid_rows, *target_rows, *delete_target_rows, *priority_rows)
    ]
    if len(new_keys) != len(set(new_keys)):
        raise RuntimeError("new A2/Priority provenance-key collision")
    prior_keys = existing_provenance_keys(external)
    collisions = {key: prior_keys[key] for key in new_keys if key in prior_keys}
    if collisions:
        raise RuntimeError(f"new provenance key collides with older overlay: {collisions}")
    if v2_validator.verify_pinned_inputs(external, False) != v2_inputs_before:
        raise RuntimeError("effective-V2 pinned inputs changed during complete build")
    report = report_text(
        invalid_rows, target_rows, delete_target_rows, priority_rows, counts,
        negative, executed, priority_replay,
    )
    return {
        external / INVALID_OUTPUT_NAME: tsv_text(A2_DELTA_COLUMNS, invalid_rows).encode("utf-8"),
        external / TARGET_OUTPUT_NAME: tsv_text(A2_DELTA_COLUMNS, target_rows).encode("utf-8"),
        external / DELETE_TARGET_OUTPUT_NAME: tsv_text(A2_DELTA_COLUMNS, delete_target_rows).encode("utf-8"),
        external / PRIORITY_OUTPUT_NAME: tsv_text(PRIORITY_DELTA_COLUMNS, priority_rows).encode("utf-8"),
        external / REPORT_NAME: report.encode("utf-8"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify existing outputs byte-for-byte")
    parser.add_argument("--audit-only", action="store_true", help="run all proofs without publishing outputs")
    parser.add_argument("--external", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    if args.check and args.audit_only:
        raise RuntimeError("--check and --audit-only are mutually exclusive")
    external = args.external.resolve()
    outputs = build(external)
    if args.audit_only:
        print("PASS audit-only guarded compiler/container scope: invalid 48; targets 32+4; priority 7; writes 0")
        return 0
    if args.check:
        for path, expected in outputs.items():
            if not path.exists():
                raise RuntimeError(f"missing output: {path}")
            actual = path.read_bytes()
            if actual != expected:
                raise RuntimeError(f"byte output drift: {path.name}")
        print("PASS guarded compiler/container scope: invalid 48; targets 32+4; priority 7; duplicate 0")
        return 0
    publish_outputs_transaction(outputs)
    print("WROTE guarded compiler/container scope: invalid 48; targets 32+4; priority 7; duplicate 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
