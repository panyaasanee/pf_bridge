#!/usr/bin/env python3
"""Re-derive the bounded actor relation/interaction graph from the pinned IMAGE.

The artifact is intentionally neutral: it records client-local decision surfaces,
not an original-server role policy and not a replacement-server design.  It never
runs the client, server, dump, or capture.  It uses a pinned Capstone decoder for
the instruction-start check and the Python standard library otherwise.  Console
output is forced through ASCII with backslash replacement.
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
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

try:
    import capstone
except ImportError:  # Reported deterministically by the decoder guard.
    capstone = None


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
TSV_PATH = OUT_DIR / "PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv"
REPORT_PATH = OUT_DIR / "PF_ACTOR_RELATION_INTERACTION_GRAPH.md"
PAIR_PATH = OUT_DIR / "PF_ACTOR_RELATION_INTERACTION_GRAPH.pair.json"
LOCK_PATH = OUT_DIR / ".PF_ACTOR_RELATION_INTERACTION_GRAPH.lock"
STAGE_PREFIXES = (
    ".PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv.",
    ".PF_ACTOR_RELATION_INTERACTION_GRAPH.md.",
    ".PF_ACTOR_RELATION_INTERACTION_GRAPH.pair.json.",
)

ROLE_PATH = OUT_DIR / "PF_ATTR_ROLE_DISCRIMINATOR.tsv"
QME_PATH = OUT_DIR / "PF_QUEST_MARK_EVENT_CENSUS.tsv"
MCMJ_PATH = OUT_DIR / "PF_MONSTER_COLOR_MECHANISM_JOIN.tsv"
REGISTRY_PATH = OUT_DIR / "PF_PROTOCOL_REGISTRY.tsv"

SOURCE = "IMAGE"
SOURCE_FILE = "PF_ROOT://GameClient/GameClient.local.bin"
IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
CAPSTONE_VERSION = "5.0.6"

PRIOR_PINS = {
    ROLE_PATH: (42_626, "3e8d99dd9fd9c8717e27d3ec8d43e2599a6037fc366e58637aff3a5cc8d5ec73"),
    QME_PATH: (29_193, "40127e6410c1aa6405efada640c60b72663eb9e35537c8011cdeede47d0a0b35"),
    MCMJ_PATH: (13_134, "dfaf5f31380c3ce6a0cfffd6b8778e1a28154b6438f5f404067b402c3d324190"),
    REGISTRY_PATH: (89_506, "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d"),
}

GENERAL_REGISTRATION = 0x005FACE0
REGISTRATION_SINGLETON = 0x005FB420
EXPECTED_GENERAL_REGISTRATION_COUNT = 140
EXPECTED_GENERAL_REGISTRATION_DIGEST = (
    "9f352999fc90400dcba1bda7899c4486eeff3f29ed8b57b7a0ba716f27622a01"
)
EXPECTED_EVENT19_REGISTRATION = (0x00615B7A, 0x19, 0x56, 0x00615B70)
EXPECTED_EVENT19_SITE_DIGEST = (
    "70db49876ca7df2198a6f856a7f8ec2db9f2dba92bc10158791be6b0eee01db1"
)

RELATION_TARGET = 0x0043C380
RELATION_E8_SITES = (
    0x00444018,
    0x00444152,
    0x00445DBD,
    0x0044988D,
    0x0044F1D3,
    0x0044F510,
    0x0044F81D,
    0x0051E44F,
    0x0051EC2F,
    0x0051F3B3,
    0x0051FBC2,
    0x005213A5,
    0x00521D1D,
    0x00522AEB,
    0x00523554,
    0x005359A2,
    0x005BC3F3,
    0x005CB04F,
    0x005CB3CA,
    0x005CB65D,
    0x005CB900,
    0x005CBA4B,
    0x005CCE1C,
    0x005CE765,
    0x00616802,
    0x00619790,
    0x006EC52B,
    0x00735839,
    0x00750AE1,
    0x007513EC,
    0x00769AC8,
)

EXPECTED_GRAPH_KEYS = (
    "ARIG-IMG-001",
    "ARIG-IMG-002",
    "ARIG-IMG-003",
    "ARIG-IMG-004",
    "ARIG-IMG-005",
    "ARIG-IMG-006",
    "ARIG-IMG-007",
    "ARIG-IMG-008",
    "ARIG-IMG-009",
    "ARIG-IMG-010",
    "ARIG-IMG-011",
    "ARIG-IMG-012",
    "ARIG-IMG-013",
    "ARIG-IMG-014",
    "ARIG-IMG-015",
    "ARIG-IMG-016",
    "ARIG-IMG-017",
    "ARIG-IMG-018",
    "ARIG-IMG-019",
    "ARIG-IMG-020",
    "ARIG-IMG-021",
    "ARIG-IMG-022",
    "ARIG-IMG-023",
    "ARIG-IMG-024",
    "ARIG-IMG-025",
    "ARIG-IMG-026",
    "ARIG-IMG-027",
    "ARIG-IMG-028",
    "ARIG-IMG-029",
    "ARIG-IMG-030",
    "ARIG-IMG-031",
    "ARIG-IMG-032",
    "ARIG-IMG-033",
    "ARIG-IMG-034",
    "ARIG-IMG-035",
    "ARIG-IMG-036",
    "ARIG-IMG-037",
    "ARIG-IMG-038",
    "ARIG-IMG-039",
    "ARIG-IMG-040",
    "ARIG-IMG-041",
    "ARIG-IMG-042",
)

EXPECTED_ROW_KINDS = (
    "GENERAL_EVENT19_REGISTRATION_SUBSET",
    "GENERAL_EVENT19_TYPED_TARGET_PRODUCER_201",
    "GENERAL_EVENT19_TYPED_TARGET_PRODUCER_205",
    "EVENT19_QUERY_RESULT_GATE",
    "EVENT19_DISTANCE_OR_APPROACH_BRANCH",
    "NPC_CONVERSATION_INBOUND_QUESTMODULE_FORWARD",
    "NPC_CONVERSATION_QUEST_UI",
    "CHOOSE_NPC_REGISTERED_ROUTINE_BOUNDARY",
    "RELATION_CONSTANT_FALSE_RESULT_SURFACE",
    "RELATION_COMPARATOR_RESULT_SURFACE",
    "RELATION_CONSTANT_TRUE_RESULT_SURFACE",
    "RELATION_CALLSITE_COLOR_STYLE",
    "RELATION_CALLSITE_COLOR_STYLE",
    "RELATION_CALLSITE_TALK_INTERACT",
    "RELATION_CALLSITE_TARGET_PRESENTATION",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_TALK_INTERACT",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_TARGET_PRESENTATION",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_TARGET_PRESENTATION",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_COLOR_STYLE",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_TALK_INTERACT",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_UNRESOLVED",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_ENEMY_TARGET_TARGET_STATE",
    "RELATION_CALLSITE_TALK_INTERACT",
)

EXPECTED_EVIDENCE_LAYERS = (
    "STATIC_NATIVE", "STATIC_NATIVE", "STATIC_NATIVE", "STATIC_NATIVE",
    "STATIC_NATIVE", "WIRE_CODEC", "UI_NATIVE", "WIRE_CODEC",
    *("STATIC_NATIVE",) * 34,
)

EXPECTED_CLASSES = (
    "QuestModule", "UNKNOWN", "UNKNOWN", "CNetNPC", "CNetNPC",
    "NPCConversation", "QuestModule", "ChooseNPC", "UNKNOWN", "UNKNOWN",
    "UNKNOWN", "CNetNPC", "CNetNPC", "UNKNOWN", "UNKNOWN", "UNKNOWN",
    "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN",
    "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN",
    "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN",
    "UNKNOWN", "UNKNOWN", "CNetNPC", "UNKNOWN", "UNKNOWN", "UNKNOWN",
    "UNKNOWN", "UNKNOWN",
)

EXPECTED_SEMANTIC_STATUSES = (
    "PROVEN_EXACT", "PROVEN_EXACT", "PROVEN_EXACT", "PROVEN_EXACT",
    "PROVEN_ROLE_ONLY", "PROVEN_EXACT", "PROVEN_EXACT", "PROVEN_EXACT",
    "PROVEN_EXACT", "PROVEN_EXACT", "PROVEN_EXACT",
    "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY",
    "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY",
    "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY",
    "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY",
    "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY",
    "UNRESOLVED", "PROVEN_ROLE_ONLY", "UNRESOLVED", "UNRESOLVED",
    "UNRESOLVED", "UNRESOLVED", "UNRESOLVED", "UNRESOLVED", "UNRESOLVED",
    "UNRESOLVED", "PROVEN_ROLE_ONLY", "UNRESOLVED", "UNRESOLVED",
    "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY", "PROVEN_ROLE_ONLY",
)

EXPECTED_MEASUREMENT_LABELS = (
    *("MEASURED",) * 42,
)

RELATION_SITE_CATEGORIES = {
    "talk_interact": (
        0x00445DBD, 0x0044F81D, 0x00619790, 0x00769AC8,
    ),
    "target_presentation": (
        0x0044988D, 0x0051FBC2, 0x00523554,
    ),
    "enemy_target_target_state": (
        0x0044F1D3, 0x0044F510, 0x0051E44F, 0x0051EC2F,
        0x0051F3B3, 0x005213A5, 0x00521D1D, 0x00522AEB,
        0x00750AE1, 0x007513EC,
    ),
    "color_style": (
        0x00444018, 0x00444152, 0x005BC3F3,
    ),
    "unresolved": (
        0x005359A2, 0x005CB04F, 0x005CB3CA, 0x005CB65D,
        0x005CB900, 0x005CBA4B, 0x005CCE1C, 0x005CE765,
        0x00616802, 0x006EC52B, 0x00735839,
    ),
}

EXACT_SITE_CLASSES = {
    0x00444018: "CNetNPC",
    0x00444152: "CNetNPC",
    0x00619790: "CNetNPC",
}

PAIR_DOMAIN = b"PF_ACTOR_RELATION_INTERACTION_GRAPH_PAIR_V1\x00"
ROW_DOMAIN = b"PF_ACTOR_RELATION_INTERACTION_GRAPH_ROW_V1\x00"


@dataclass(frozen=True)
class Section:
    name: str
    va: int
    virtual_size: int
    file_off: int
    raw_size: int
    executable: bool


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    sha256: str


EXPECTED_SECTIONS = (
    (".text", 0x00401000, 0x00838A2C, 0x00000400, 0x00838C00, True),
    (".code", 0x00C3A000, 0x000002E1, 0x00839000, 0x00000400, True),
    (".rdata", 0x00C3B000, 0x003DE38E, 0x00839400, 0x003DE400, False),
    (".data", 0x0101A000, 0x00081F70, 0x00C17800, 0x00011E00, False),
    (".rsrc", 0x0109C000, 0x00058998, 0x00C29600, 0x00058A00, False),
    (".reloc", 0x010F5000, 0x001915F0, 0x00C82000, 0x00191600, False),
)


SPANS = {
    "event19_registration": Span(0x00615B70, 0x00615B7F, "d119691b5c71207afe26aaa968865b747ba2443ffa76b237bd786644992c8285"),
    "event19_producer_201": Span(0x0044F236, 0x0044F281, "6b0e718e439be5a5f6470f2037f4ddb2ba1c42c30e46451499a23c21d131d278"),
    "event19_producer_205": Span(0x0044F741, 0x0044F78D, "4ab3b057c6aed54a0e102ce38dece6df403ff3992546dfd698870f9dd725b62d"),
    "event19_query_gate": Span(0x006197D2, 0x0061980E, "e485e3e075366d2cac57c59b81365d668b71b7b2fd0ccf0eaf4ab4ce6731a5b1"),
    "event19_distance_approach": Span(0x00619814, 0x00619AAA, "190638e02377cb60f1f80df93fc6f037a391e67eada9d03e85f099b1b510ed36"),
    "approach_branch_a": Span(0x006198EE, 0x00619940, "52dc7ba9657f75b29000a0b57c54a62e183a59aa3106dc88ac09df09b7146217"),
    "approach_branch_b": Span(0x00619A11, 0x00619A71, "c1f64e9d0cc1174e81d351863e0fbc119b4f844778f95fb6641f291fe2ea62dc"),
    "npc_conversation_handler": Span(0x00623090, 0x006230E2, "d9f7fda8c6c686daa677259d5fd0d653c0500ec0b14278840d99919e170a45a7"),
    "npc_conversation_dispatcher": Span(0x0061A99D, 0x0061AA83, "78cf02536650b931ea70ce5b6053b5e784b901acedada5a94e52f82a49d19858"),
    "quest_module_literal": Span(0x00F0BAE8, 0x00F0BAF4, "49a0b3a878479a69db20fb201afeea02443ca015fb066cd76a2eb282d57548cd"),
    "quest_ui_model_new": Span(0x00F25580, 0x00F255B6, "dec8c04a69476255f32e6c649b9139aa0eda07d4de805b3417419c1c70e419eb"),
    "quest_ui_model_old": Span(0x00F25600, 0x00F2562E, "989e83416135edaa0657d9a5b8870e72b874e7690cf312cb83fc83cc6ecead5b"),
    "init_quest_list_literal": Span(0x00F336B4, 0x00F336D0, "5420c9eba89250560ecf78e581c614d8d2b06f0cafe7ef5608a0d46d2c92f72d"),
    "choose_npc_handler": Span(0x00710440, 0x00710445, "f4c6d7ae520f88aecb3ea65952e885437fa4a6ce4b5c3439a161d1c5d8e42863"),
    "relation_predicate": Span(0x0043C380, 0x0043C63C, "1d99f8557252742914c4f7358853aac06f0b54603f78a4b4d073aaea2afcbd89"),
    "relation_false_return": Span(0x0043C48F, 0x0043C4AA, "d1ef09f32a40306a40adc19ca057c91c751d3a336668f7ee288fb7d80c088ad5"),
    "relation_comparator_return": Span(0x0043C5C9, 0x0043C5FF, "916a45082cc44a28219206b05729cb14f80575f054a56ca7acf1cb14a159f3a1"),
    "relation_true_return": Span(0x0043C5FF, 0x0043C615, "ccdc50cf950a04b04e58cad64634d4be7e12e850b385af9c66387af4aceabce9"),
    "cnetnpc_vtable_32_entries": Span(0x00F0DF58, 0x00F0DFD8, "9305c765da3e4af1a3e7082d6ad49aa49741bd2115f66e8119387890a452319e"),
    "cnetnpc_template_helper": Span(0x0045BF40, 0x0045C15D, "afb5662a3f1a81c98de8ed77d82262747b8563ce25be88d041c8dea89e52fb72"),
    "relation_call_00444018": Span(0x00443F50, 0x004443C5, "ee845ee6ef6337ea41ae57a5a4df8af5a8a8ac00e458ea1ce3e587aff1f9cdf9"),
    "relation_call_00444152": Span(0x00443F50, 0x004443C5, "ee845ee6ef6337ea41ae57a5a4df8af5a8a8ac00e458ea1ce3e587aff1f9cdf9"),
    "relation_call_00445dbd": Span(0x00445D45, 0x00445E6C, "4a6ba29f0a21a55b2c8e3408408e34f4b79be64fd367bfeae17606ed2781f8a8"),
    "relation_call_0044988d": Span(0x00449820, 0x004498CF, "880614494d173809e17129c9fbc6ddbd14950d1e4380e02aa5e3a4370f802f0a"),
    "relation_call_0044f1d3": Span(0x0044F0F2, 0x0044F4A7, "53e64dee1138fdbfa683472bc86fc93a97fe8494cee056e782a0ca590567b017"),
    "relation_call_0044f510": Span(0x0044F502, 0x0044F55B, "dea391118207a9af119bc0efa9fd15f38071afdc16ba30edc8405f7a3a767817"),
    "relation_call_0044f81d": Span(0x0044F7F6, 0x0044FAAA, "051705d247b1fbaf207024cd231d02b256eccf5da86042c3a6adf3a233c901b5"),
    "relation_call_0051e44f": Span(0x0051E42B, 0x0051E473, "95d52cd1caa86872658ebbcc9ef2ff3598b0d8fd5b869ee06288e13df11885c6"),
    "relation_call_0051ec2f": Span(0x0051EC0A, 0x0051EC53, "95ae6615a3e0fbf9deeace06fc4db254e51d84b1348b8d68688c029f82337259"),
    "relation_call_0051f3b3": Span(0x0051F392, 0x0051F408, "fe94bac38987434ba3a47b31c71d00591db7a246446841a859b3c56540363297"),
    "relation_call_0051fbc2": Span(0x0051FB78, 0x0051FBDE, "2866e16b2045cbf2a81cd481ad5e161da0d4d47c0e82ff1f7a7740476ff2a941"),
    "relation_call_005213a5": Span(0x00521384, 0x005213FA, "dcb4c6fab0aa89aa0f387e2da9a32f7db8118d52ee0ff366a7e8fded0a7c6872"),
    "relation_call_00521d1d": Span(0x00521CF8, 0x00521D41, "391dbf8f3ac07da119fc8a25072b18f8cea960b83eead998f79d6a252b83db69"),
    "relation_call_00522aeb": Span(0x00522AC6, 0x00522B1E, "8ada1d461b262bd988415a824e38694e3720a02ecd2110fc54582d0f0e18df52"),
    "relation_call_00523554": Span(0x0052350A, 0x00523570, "b9a6b510b1081c273dc4674b9af5a6cfbe4b1c02f987f9e4142979225d399b9d"),
    "relation_call_005359a2": Span(0x0053595C, 0x00535C04, "85b673da335d2e6e3c30ef7613976cfafe432bc3056bc3f61a5e96913090298a"),
    "relation_call_005bc3f3": Span(0x005BC3DA, 0x005BC4DA, "fc454d3202c127cfe401eb98b33952f6736a24f6b08f56ed2829306c4dc81b8e"),
    "relation_call_005cb04f": Span(0x005CB03A, 0x005CB0DC, "b3053a15c716963f27d4348ef93abe9123c05a0d8065d48f4e9dcfc792e6b7fd"),
    "relation_call_005cb3ca": Span(0x005CB3C9, 0x005CB46D, "eaf7752a7ef9545634154b08e13e201dfa664eb02bf1c9a383a1d761dd3244f7"),
    "relation_call_005cb65d": Span(0x005CB65C, 0x005CB72D, "5a60d6bd41ab5dc426831fb41daa822f702e4e0dc55c6085c707f8ce7290bae2"),
    "relation_call_005cb900": Span(0x005CB8FF, 0x005CB97B, "dd414f42399e8b7543e44c0bd16723dc67615ae65e7819a3a90ff4e9adf139dc"),
    "relation_call_005cba4b": Span(0x005CBA4A, 0x005CBAC6, "84e97ed19436f0f4ac03695bbc6c331dc606f70e79979d7ec1623550fc43b489"),
    "relation_call_005cce1c": Span(0x005CCE1B, 0x005CCE90, "df15c302889a38be0c429cae92b279a5b03182c8576c2d3ccfbd2c66621518f2"),
    "relation_call_005ce765": Span(0x005CE764, 0x005CE7FF, "5c942e8f631d1b4b81af5e7c23abeadd7a19defc087dcc78e6f470dc6afcadc2"),
    "relation_call_00616802": Span(0x00616790, 0x00616827, "4008a0568145fd75ae18286dd1582ceabe8393b98fa4f7b78648827b68075cc2"),
    "relation_call_00619790": Span(0x00619777, 0x006197D2, "5aa039fe2b8e8a6dce5c6c01e7abf03b9bc82f4507475bdfcd29a5b94b82ef45"),
    "relation_call_006ec52b": Span(0x006EC4EB, 0x006EC66E, "012a97bcb1bcc08e016ede4c30170330cbb398b717f7ee1e43d8d13c85aa3ab5"),
    "relation_call_00735839": Span(0x007357FD, 0x00735A34, "be3373627febe5b74838dbcac45feac13b4f10db537076a9dec0cf5fb536140a"),
    "relation_call_00750ae1": Span(0x00750AE0, 0x00750B52, "0c4d83e8f0791769bb4bb1dcd86782de1c855a0e2a9f2ad6bbf40b08a35d125c"),
    "relation_call_007513ec": Span(0x007513EB, 0x0075145D, "4915f04c80d82967fa8dd93d162fae9728186b5ff6dd4387eef69c4cb596191c"),
    "relation_call_00769ac8": Span(0x00769AAB, 0x00769DB1, "c7faf93229a47413dfd08b2360f9f7f445467acb6e9fa265db8b0079825b7c9b"),
}


FIELDNAMES = (
    "graph_key",
    "row_kind",
    "decision_surface",
    "evidence_layer",
    "applies_to_class",
    "input_or_condition",
    "exact_observation",
    "semantic_status",
    "measurement_label",
    "measurement_method",
    "control",
    "negative_scope",
    "span_start_va",
    "span_end_va",
    "file_off_start",
    "file_off_end",
    "span_sha256",
    "support_spans",
    "site_count",
    "site_list",
    "site_digest",
    "prior_reference",
    "prior_artifact_sha256",
    "prior_claim_digest",
    "source",
    "source_file",
    "source_size",
    "source_sha256",
    "nonclaim",
    "blocker",
    "required_next_evidence",
    "claim_sha256",
    "evidence_key",
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_lines(lines: Sequence[str]) -> str:
    return sha256(("\n".join(lines) + "\n").encode("ascii"))


def read_pinned(path: Path, expected_size: int, expected_sha256: str) -> bytes:
    raw = path.read_bytes()
    if len(raw) != expected_size or sha256(raw) != expected_sha256:
        raise RuntimeError(f"pinned input mismatch: {path.name}")
    return raw


def parse_pe(image: bytes) -> tuple[Section, ...]:
    if image[:2] != b"MZ":
        raise RuntimeError("image DOS signature mismatch")
    pe_off = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_off : pe_off + 4] != b"PE\x00\x00":
        raise RuntimeError("image PE signature mismatch")
    section_count = struct.unpack_from("<H", image, pe_off + 6)[0]
    optional_size = struct.unpack_from("<H", image, pe_off + 20)[0]
    optional = pe_off + 24
    if struct.unpack_from("<H", image, optional)[0] != 0x10B:
        raise RuntimeError("image is not PE32")
    if struct.unpack_from("<I", image, optional + 28)[0] != 0x00400000:
        raise RuntimeError("image base mismatch")
    section_table = optional + optional_size
    sections: list[Section] = []
    for index in range(section_count):
        off = section_table + index * 40
        name = image[off : off + 8].split(b"\x00", 1)[0].decode("ascii")
        virtual_size, relative_va, raw_size, raw_off = struct.unpack_from(
            "<IIII", image, off + 8
        )
        characteristics = struct.unpack_from("<I", image, off + 36)[0]
        sections.append(
            Section(
                name,
                0x00400000 + relative_va,
                virtual_size,
                raw_off,
                raw_size,
                bool(characteristics & 0x20000000),
            )
        )
    actual = tuple(
        (s.name, s.va, s.virtual_size, s.file_off, s.raw_size, s.executable)
        for s in sections
    )
    if actual != EXPECTED_SECTIONS:
        raise RuntimeError("PE section layout mismatch")
    return tuple(sections)


def va_to_offset(sections: Sequence[Section], va: int, length: int = 1) -> int:
    for section in sections:
        backed = min(section.virtual_size, section.raw_size)
        if section.va <= va and va + length <= section.va + backed:
            return section.file_off + va - section.va
    raise RuntimeError(f"VA is not file-backed: 0x{va:08X}")


def file_offset_to_va(sections: Sequence[Section], off: int) -> int | None:
    for section in sections:
        backed = min(section.virtual_size, section.raw_size)
        if section.file_off <= off < section.file_off + backed:
            return section.va + off - section.file_off
    return None


def span_bytes(
    image: bytes, sections: Sequence[Section], name: str
) -> tuple[bytes, int, int]:
    spec = SPANS[name]
    start = va_to_offset(sections, spec.start, spec.end - spec.start)
    end = start + spec.end - spec.start
    raw = image[start:end]
    if sha256(raw) != spec.sha256:
        raise RuntimeError(f"span hash mismatch: {name}")
    return raw, start, end


def expect_bytes(
    image: bytes, sections: Sequence[Section], va: int, expected_hex: str
) -> None:
    expected = bytes.fromhex(expected_hex)
    off = va_to_offset(sections, va, len(expected))
    if image[off : off + len(expected)] != expected:
        raise RuntimeError(f"instruction-shape guard failed at 0x{va:08X}")


def direct_relative_sites(
    image: bytes, sections: Sequence[Section], target: int, opcode: int = 0xE8
) -> list[int]:
    sites: list[int] = []
    for section in sections:
        if not section.executable:
            continue
        backed = min(section.virtual_size, section.raw_size)
        raw = image[section.file_off : section.file_off + backed]
        for index in range(len(raw) - 4):
            if raw[index] != opcode:
                continue
            relative = struct.unpack_from("<i", raw, index + 1)[0]
            if section.va + index + 5 + relative == target:
                sites.append(section.va + index)
    return sorted(sites)


def decoder_validate_relation_sites(
    image: bytes, sections: Sequence[Section]
) -> tuple[tuple[int, ...], dict[int, str]]:
    if capstone is None:
        raise RuntimeError(
            "Capstone is required for instruction-start validation; expected version "
            + CAPSTONE_VERSION
        )
    if getattr(capstone, "__version__", None) != CAPSTONE_VERSION:
        raise RuntimeError(
            "Capstone version mismatch: expected %s got %s"
            % (CAPSTONE_VERSION, getattr(capstone, "__version__", "UNKNOWN"))
        )
    text = next(section for section in sections if section.name == ".text")
    raw = image[text.file_off : text.file_off + text.raw_size]
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    decoder.skipdata = True
    wanted = set(RELATION_E8_SITES)
    last_wanted = max(wanted)
    decoded: dict[int, str] = {}
    for address, size, mnemonic, _operand in decoder.disasm_lite(raw, text.va):
        if address > last_wanted and len(decoded) == len(wanted):
            break
        if address not in wanted:
            continue
        relative_off = address - text.va
        call_raw = raw[relative_off : relative_off + size]
        if size != 5 or mnemonic != "call" or call_raw[0] != 0xE8:
            raise RuntimeError(
                "relation site is not decoded as five-byte E8 call: 0x%08X"
                % address
            )
        relative = struct.unpack_from("<i", call_raw, 1)[0]
        target = address + 5 + relative
        if target != RELATION_TARGET:
            raise RuntimeError(
                "decoded relation target mismatch at 0x%08X" % address
            )
        decoded[address] = (
            "site=0x%08X;size=5;opcode=E8;target=0x%08X;"
            "decoder=capstone-%s;mode=x86-32;anchor=0x%08X;skipdata=1"
            % (
                address,
                target,
                CAPSTONE_VERSION,
                text.va,
            )
        )
    decoded_sites = tuple(sorted(decoded))
    if decoded_sites != RELATION_E8_SITES:
        missing = sorted(wanted - set(decoded_sites))
        raise RuntimeError(
            "Capstone instruction-start relation-site mismatch; missing="
            + ",".join("0x%08X" % value for value in missing)
        )
    return decoded_sites, decoded


def dword_refs(image: bytes, sections: Sequence[Section], value: int) -> list[int]:
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
    image: bytes, sections: Sequence[Section], target: int
) -> list[tuple[int, int, int, int]]:
    text = next(section for section in sections if section.name == ".text")
    raw = image[text.file_off : text.file_off + text.raw_size]
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
        object_push = raw[index + immediate_len]
        if not 0x50 <= object_push <= 0x57:
            continue
        singleton_call = index + immediate_len + 1
        if raw[singleton_call] != 0xE8:
            continue
        relative = struct.unpack_from("<i", raw, singleton_call + 1)[0]
        if text.va + singleton_call + 5 + relative != REGISTRATION_SINGLETON:
            continue
        if raw[singleton_call + 5 : singleton_call + 7] != b"\x8B\xC8":
            continue
        registration_call = singleton_call + 7
        if raw[registration_call] != 0xE8:
            continue
        relative = struct.unpack_from("<i", raw, registration_call + 1)[0]
        if text.va + registration_call + 5 + relative != target:
            continue
        rows.append(
            (
                text.va + registration_call,
                kind,
                object_push,
                text.va + index,
            )
        )
    return rows


def canonical_row_digest(row: Mapping[str, str]) -> str:
    return sha256(
        json.dumps(
            dict(row), sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    )


def load_tsv(path: Path) -> list[dict[str, str]]:
    size, digest = PRIOR_PINS[path]
    raw = read_pinned(path, size, digest)
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise RuntimeError(f"prior artifact has no rows: {path.name}")
    return rows


@dataclass(frozen=True)
class PriorClaim:
    token: str
    artifact_sha256: str
    claim_digest: str


def select_prior(
    rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]],
    path: Path,
    key_column: str,
    key: str,
    *,
    expected_evidence_key: str = "",
    expected_claim_digest: str = "",
) -> PriorClaim:
    matches = [row for row in rows_by_path[path] if row.get(key_column) == key]
    if len(matches) != 1:
        raise RuntimeError(f"prior row missing or duplicated: {path.name}:{key}")
    row = matches[0]
    if row.get("source") != SOURCE:
        raise RuntimeError(f"prior row source drift: {path.name}:{key}")
    evidence_key = row.get("evidence_key", "")
    if expected_evidence_key and evidence_key != expected_evidence_key:
        raise RuntimeError(f"prior evidence key drift: {path.name}:{key}")
    claim_digest = row.get("claim_sha256", "") or canonical_row_digest(row)
    if expected_claim_digest and claim_digest != expected_claim_digest:
        raise RuntimeError(f"prior claim digest drift: {path.name}:{key}")
    artifact_sha = PRIOR_PINS[path][1]
    evidence_suffix = f"@{evidence_key}" if evidence_key else ""
    return PriorClaim(
        f"{path.name}:{key}{evidence_suffix}", artifact_sha, claim_digest
    )


def join_prior(claims: Sequence[PriorClaim]) -> tuple[str, str, str]:
    if not claims:
        return "N/A", "N/A", "N/A"
    return (
        ";".join(claim.token for claim in claims),
        ";".join(claim.artifact_sha256 for claim in claims),
        ";".join(claim.claim_digest for claim in claims),
    )


def format_span(
    image: bytes, sections: Sequence[Section], name: str
) -> str:
    _, start, end = span_bytes(image, sections, name)
    spec = SPANS[name]
    return (
        f"{name}=VA:0x{spec.start:08X}..0x{spec.end:08X}"
        f"@file:0x{start:08X}..0x{end:08X}@sha256:{spec.sha256}"
    )


def make_row(
    image: bytes,
    sections: Sequence[Section],
    *,
    graph_key: str,
    row_kind: str,
    decision_surface: str,
    evidence_layer: str,
    applies_to_class: str,
    input_or_condition: str,
    exact_observation: str,
    semantic_status: str,
    measurement_method: str,
    control: str,
    negative_scope: str,
    primary_span: str,
    support_spans: Sequence[str] = (),
    site_lines: Sequence[str] = (),
    prior_claims: Sequence[PriorClaim] = (),
    nonclaim: str,
    blocker: str,
    required_next_evidence: str,
    measurement_label: str = "MEASURED",
) -> dict[str, str]:
    spec = SPANS[primary_span]
    _, start, end = span_bytes(image, sections, primary_span)
    prior_reference, prior_artifact_sha, prior_claim_digest = join_prior(prior_claims)
    site_list = "||".join(site_lines) if site_lines else "N/A"
    site_digest = digest_lines(site_lines) if site_lines else "N/A"
    row = {
        "graph_key": graph_key,
        "row_kind": row_kind,
        "decision_surface": decision_surface,
        "evidence_layer": evidence_layer,
        "applies_to_class": applies_to_class,
        "input_or_condition": input_or_condition,
        "exact_observation": exact_observation,
        "semantic_status": semantic_status,
        "measurement_label": measurement_label,
        "measurement_method": measurement_method,
        "control": control,
        "negative_scope": negative_scope,
        "span_start_va": f"0x{spec.start:08X}",
        "span_end_va": f"0x{spec.end:08X}",
        "file_off_start": f"0x{start:08X}",
        "file_off_end": f"0x{end:08X}",
        "span_sha256": spec.sha256,
        "support_spans": ";".join(
            format_span(image, sections, name) for name in support_spans
        ),
        "site_count": str(len(site_lines)),
        "site_list": site_list,
        "site_digest": site_digest,
        "prior_reference": prior_reference,
        "prior_artifact_sha256": prior_artifact_sha,
        "prior_claim_digest": prior_claim_digest,
        "source": SOURCE,
        "source_file": SOURCE_FILE,
        "source_size": str(IMAGE_SIZE),
        "source_sha256": IMAGE_SHA256,
        "nonclaim": nonclaim,
        "blocker": blocker,
        "required_next_evidence": "PROPOSED: " + required_next_evidence,
        "claim_sha256": "",
        "evidence_key": "",
    }
    claim_fields = {
        key: value for key, value in row.items() if key not in {"claim_sha256", "evidence_key"}
    }
    row["claim_sha256"] = canonical_row_digest(claim_fields)
    row["evidence_key"] = sha256(
        ROW_DOMAIN
        + row["claim_sha256"].encode("ascii")
        + b"\x00"
        + row["span_sha256"].encode("ascii")
        + b"\x00"
        + IMAGE_SHA256.encode("ascii")
    )
    return row


def verify_static_anchors(image: bytes, sections: Sequence[Section]) -> dict[str, object]:
    for name in SPANS:
        span_bytes(image, sections, name)

    quest_module_literal, _, _ = span_bytes(image, sections, "quest_module_literal")
    if quest_module_literal != b"QuestModule\x00":
        raise RuntimeError("QuestModule literal content drift")

    # Exact writes/calls in the two kind-0x19 producer bodies.
    expect_bytes(image, sections, 0x0044F25E, "C744247019000000")
    expect_bytes(image, sections, 0x0044F266, "C744247401020000")
    expect_bytes(image, sections, 0x0044F26E, "89B42490000000")
    expect_bytes(image, sections, 0x0044F27C, "E8EFA91A00")
    expect_bytes(image, sections, 0x0044F763, "C744247019000000")
    expect_bytes(image, sections, 0x0044F76B, "C744247405020000")
    expect_bytes(image, sections, 0x0044F773, "899C2490000000")
    expect_bytes(image, sections, 0x0044F788, "E8E3A41A00")

    # Query result and distance/approach anchors.
    expect_bytes(image, sections, 0x006197E8, "C744243412000000")
    expect_bytes(image, sections, 0x00619804, "E85707FEFF")
    expect_bytes(image, sections, 0x00619809, "807C243800")
    expect_bytes(image, sections, 0x006198E8, "0F8685010000")
    expect_bytes(image, sections, 0x006198EE, "BA50000000")
    expect_bytes(image, sections, 0x0061992B, "E860BDE5FF")
    expect_bytes(image, sections, 0x0061993B, "E8B0AAE6FF")
    expect_bytes(image, sections, 0x00619A11, "BA50000000")
    expect_bytes(image, sections, 0x00619A54, "E837BCE5FF")
    expect_bytes(image, sections, 0x00619A6C, "E87FA9E6FF")

    # NPCConversation handler, UI branch, and registered ChooseNPC routine.
    expect_bytes(image, sections, 0x0062309D, "68E8BAF000")
    expect_bytes(image, sections, 0x006230D5, "57E87578FFFF")
    expect_bytes(image, sections, 0x0061A9A6, "E8456D0000")
    expect_bytes(image, sections, 0x0061A9C3, "8B4618898780000000")
    expect_bytes(image, sections, 0x0061A9CC, "8B4E1C898F84000000")
    expect_bytes(image, sections, 0x0061AA06, "688055F200")
    expect_bytes(image, sections, 0x0061AA0D, "680056F200")
    expect_bytes(image, sections, 0x0061AA35, "68B436F300")
    expect_bytes(image, sections, 0x0061AA46, "8B178B9210020000")
    expect_bytes(image, sections, 0x00710440, "B001C20400")

    # Final result-producer surfaces; their upstream meanings remain separate.
    expect_bytes(image, sections, 0x0043C4A3, "32C0E96B010000")
    expect_bytes(image, sections, 0x0043C5D9, "E882EFFCFF")
    expect_bytes(image, sections, 0x0043C5E0, "E86B570600")
    expect_bytes(image, sections, 0x0043C5FB, "8AC3EB16")
    expect_bytes(image, sections, 0x0043C613, "B001")

    general = registration_census(image, sections, GENERAL_REGISTRATION)
    general_lines = [
        f"call=0x{call:08X};kind=0x{kind:08X};object_push=0x{push:02X};start=0x{start:08X}"
        for call, kind, push, start in general
    ]
    if len(general) != EXPECTED_GENERAL_REGISTRATION_COUNT:
        raise RuntimeError("general registration count drift")
    if digest_lines(general_lines) != EXPECTED_GENERAL_REGISTRATION_DIGEST:
        raise RuntimeError("general registration digest drift")
    event19 = [row for row in general if row[1] == 0x19]
    if event19 != [EXPECTED_EVENT19_REGISTRATION]:
        raise RuntimeError("kind-0x19 direct registration subset drift")
    event19_lines = [
        f"call=0x{call:08X};kind=0x{kind:08X};object_push=0x{push:02X};start=0x{start:08X}"
        for call, kind, push, start in event19
    ]
    if digest_lines(event19_lines) != EXPECTED_EVENT19_SITE_DIGEST:
        raise RuntimeError("kind-0x19 registration subset digest drift")
    if direct_relative_sites(image, sections, GENERAL_REGISTRATION) != [
        row[0] for row in general
    ]:
        raise RuntimeError("general registration instruction pattern misses E8 site")
    if direct_relative_sites(image, sections, GENERAL_REGISTRATION, 0xE9):
        raise RuntimeError("general registration gained direct E9 site")
    if dword_refs(image, sections, GENERAL_REGISTRATION):
        raise RuntimeError("general registration gained absolute pointer carrier")

    relation_sites = direct_relative_sites(image, sections, RELATION_TARGET)
    if tuple(relation_sites) != RELATION_E8_SITES:
        raise RuntimeError("relation E8+rel32 byte-pattern site list drift")
    decoded_relation_sites, relation_decoder_lines = decoder_validate_relation_sites(
        image, sections
    )
    if tuple(relation_sites) != decoded_relation_sites:
        raise RuntimeError("raw and decoder-validated relation-site sets differ")
    return {
        "general_lines": general_lines,
        "event19_lines": event19_lines,
        "relation_sites": relation_sites,
        "relation_decoder_lines": relation_decoder_lines,
    }


def build_prior_claims() -> tuple[dict[str, PriorClaim], Mapping[Path, Sequence[Mapping[str, str]]]]:
    rows_by_path = {path: load_tsv(path) for path in PRIOR_PINS}
    claims = {
        "role_action_gate": select_prior(
            rows_by_path,
            ROLE_PATH,
            "discriminator_id",
            "CNETNPC_INTERACTION_ACTION_GATE",
            expected_evidence_key="d9d1012a4b996401b1f14587604449f9081430ad7286b581d9ffcaf516327448",
            expected_claim_digest="bcb17acf39008af97f104d92b1d6a39e421b22cfcadc26a370773960f608da85",
        ),
        "role_choose_npc": select_prior(
            rows_by_path,
            ROLE_PATH,
            "discriminator_id",
            "CNETNPC_INTERACTION_CHOOSE_NPC_GENERIC",
            expected_evidence_key="0bebc744fed9e742d325455efd0288a015b26f374968b0845430c5d2e533f092",
            expected_claim_digest="86173101641aaf549337c32264c7285c1fe469b20d9f4b57842941b510227562",
        ),
        "role_relation_false_target": select_prior(
            rows_by_path,
            ROLE_PATH,
            "discriminator_id",
            "RELATION_FALSE_ENEMY_TARGET",
            expected_evidence_key="999e42753f0aaef474f037f7d3762d84463f0904a7d8795d819a5d506d48a40b",
            expected_claim_digest="b6f7f71d87b6031d151ad7eeea93d8f7931e6615c36f48cc07edfa9198528c27",
        ),
        "role_targetvital_kind": select_prior(
            rows_by_path,
            ROLE_PATH,
            "discriminator_id",
            "TARGETVITAL_RELATION_KIND",
            expected_evidence_key="4cd0f3fbfa5ef9e7a44abcebdd78f3960df27f4edf40c741db0089cc26ef2048",
            expected_claim_digest="f5bc4aa98d44bd92b432e67c793447677e8819d3270e8c80c14e38d8ac9282f9",
        ),
        "role_ai_combat_loader": select_prior(
            rows_by_path,
            ROLE_PATH,
            "discriminator_id",
            "MOBS_N_AI_COMBAT_LOADER_ONLY",
            expected_evidence_key="79aaf702be5511c126d3e8d81cdcd142d10a98dc0be245bb62c98bdfd2eb8493",
            expected_claim_digest="ea8e6e288d7eeaf32245780a6ebd3701ee0e849d5dabcd3c3717bd1def9f0690",
        ),
        "role_enemy_copy": select_prior(
            rows_by_path,
            ROLE_PATH,
            "discriminator_id",
            "MOBS_N_ENEMY_LOADED_COPY",
            expected_evidence_key="f3a1559d4670a8948d47efcf7fdc0f8060cd55b959485f65bc87dd5c44ebdac2",
            expected_claim_digest="f4dd1757709720a4a9e0e81da0449912fd7f26a897423a47a99046f9c6a2978b",
        ),
        "qme_general_census": select_prior(
            rows_by_path,
            QME_PATH,
            "event_key",
            "QME-IMG-017",
            expected_evidence_key="8be3f62040f283114adc9cbffad880b30f7400e855ca2b2dce2e3df4b0b74da1",
            expected_claim_digest="bfe3ea2d88269f381c60ac3656a7b358e1ee9a4e0310f77fda29d377c5c37a2d",
        ),
        "qme_quest_module_binding": select_prior(
            rows_by_path,
            QME_PATH,
            "event_key",
            "QME-IMG-007",
            expected_evidence_key="aeb9b33c61c0dfdb02c624271d203c41cae68ca87b75185609eafdce6b5088f2",
            expected_claim_digest="c6a8c8f2d9fa39c71b6eb8757167ce739622e0ba394e6a44a3972a3ea15d9e5b",
        ),
        "mcmj_comparator": select_prior(
            rows_by_path, MCMJ_PATH, "join_key", "MCMJ-IMG-003",
            expected_evidence_key="702d95f394c62daf7af0a8bb24e0953c7cbe9eff486aa6fb77c9b573820c95d0",
        ),
        "mcmj_fallback": select_prior(
            rows_by_path, MCMJ_PATH, "join_key", "MCMJ-IMG-004",
            expected_evidence_key="6c5d1647a4ab5d48f53802b77739ac1ab7743523bf3e891b2892afcdeaaeb86f",
        ),
        "mcmj_selector_positive": select_prior(
            rows_by_path, MCMJ_PATH, "join_key", "MCMJ-IMG-005",
            expected_evidence_key="f7f8ae0de74a2b7a002e379c8cce2285694ead5a5ccc5bad1be3802c473c7c08",
        ),
        "mcmj_selector_nonpositive": select_prior(
            rows_by_path, MCMJ_PATH, "join_key", "MCMJ-IMG-006",
            expected_evidence_key="ef8e7c95c07bf8560bae924518ef6f9b1567fa83f9c5adab3d1bcd811cb6fbb0",
        ),
        "registry_choose_npc": select_prior(
            rows_by_path, REGISTRY_PATH, "name", "ChooseNPC"
        ),
        "registry_npc_conversation": select_prior(
            rows_by_path, REGISTRY_PATH, "name", "NPCConversation"
        ),
    }
    return claims, rows_by_path


def build_rows(
    image: bytes,
    sections: Sequence[Section],
    facts: Mapping[str, object],
    prior: Mapping[str, PriorClaim],
) -> list[dict[str, str]]:
    event19_lines = list(facts["event19_lines"])
    relation_sites = list(facts["relation_sites"])
    relation_decoder_lines = dict(facts["relation_decoder_lines"])
    category_by_site: dict[int, str] = {}
    for category, sites in RELATION_SITE_CATEGORIES.items():
        for site in sites:
            if site in category_by_site:
                raise RuntimeError(f"relation site categorized twice: 0x{site:08X}")
            category_by_site[site] = category
    if set(category_by_site) != set(relation_sites):
        raise RuntimeError("relation category partition does not cover exact E8 site set")

    relation_site_lines: dict[int, str] = {}
    for site in relation_sites:
        off = va_to_offset(sections, site, 5)
        call_raw = image[off : off + 5]
        relation_site_lines[site] = (
            f"category={category_by_site[site]};file=0x{off:08X};"
            f"call_sha256={sha256(call_raw)};{relation_decoder_lines[site]}"
        )
    partition_lines = [relation_site_lines[site] for site in relation_sites]
    partition_digest = digest_lines(partition_lines)

    rows = [
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-001",
            row_kind="GENERAL_EVENT19_REGISTRATION_SUBSET",
            decision_surface="general_event_kind_0x19_registration",
            evidence_layer="STATIC_NATIVE",
            applies_to_class="QuestModule",
            input_or_condition="direct immediate general-registration shape with kind=0x19",
            exact_observation="The general channel has one direct kind-0x19 registration site at 0x00615B7A in the QuestModule registration surface.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Reuse the pinned QME-IMG-017 140-site direct-registration control, independently filter the identical instruction-shape census for kind 0x19, verify the exact registration span/call, and cite QME-IMG-007 for the inherited QuestModule class/vtable ownership.",
            control=f"general_direct_registrations={EXPECTED_GENERAL_REGISTRATION_COUNT};general_digest={EXPECTED_GENERAL_REGISTRATION_DIGEST};QME-IMG-017;class_provenance=QME-IMG-007",
            negative_scope="The uniqueness statement covers direct immediate registration shapes and E8 calls only. Dynamic or register-built registration is excluded.",
            primary_span="event19_registration",
            site_lines=event19_lines,
            prior_claims=(prior["qme_general_census"], prior["qme_quest_module_binding"]),
            nonclaim="Kind 0x19 is not assigned a global gameplay name by this registration fact. QuestModule identity is inherited only from pinned QME-IMG-007 and is not independently broadened.",
            blocker="Dynamic/register-built registration and the complete subscriber behavior remain outside this census.",
            required_next_evidence="A typed handler/dataflow proof before assigning a broader semantic name.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-002",
            row_kind="GENERAL_EVENT19_TYPED_TARGET_PRODUCER_201",
            decision_surface="general_event_kind_0x19_target_producer_0x201",
            evidence_layer="STATIC_NATIVE",
            applies_to_class="UNKNOWN",
            input_or_condition="audited producer A dispatches general event kind 0x19",
            exact_observation="Producer A writes event +0x10=0x19, writes +0x14=0x201, copies target identity to +0x20/+0x24, stores the target actor pointer at +0x30, and dispatches through local actor owner +0x130.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Pinned producer span plus exact event-field stores and direct general-dispatch call anchors.",
            control="ARIG-IMG-001 owns the direct registration subset; this row owns only producer A's typed event layout.",
            negative_scope="One exact producer body; no other producer or subscriber is excluded.",
            primary_span="event19_producer_201",
            prior_claims=(prior["qme_general_census"],),
            nonclaim="Numeric value 0x201 is not assigned a gameplay name, and the target actor's concrete class is UNKNOWN.",
            blocker="The receiving subscriber's interpretation of +0x14=0x201 is not proved.",
            required_next_evidence="Typed subscriber branch consuming kind 0x19 with +0x14=0x201.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-003",
            row_kind="GENERAL_EVENT19_TYPED_TARGET_PRODUCER_205",
            decision_surface="general_event_kind_0x19_target_producer_0x205",
            evidence_layer="STATIC_NATIVE",
            applies_to_class="UNKNOWN",
            input_or_condition="audited producer B dispatches general event kind 0x19",
            exact_observation="Producer B writes event +0x10=0x19, writes +0x14=0x205, copies target identity to +0x20/+0x24, stores the target actor pointer at +0x30, and dispatches through local actor owner +0x130.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Pinned producer span plus exact event-field stores and direct general-dispatch call anchors.",
            control="ARIG-IMG-001 owns the direct registration subset; this row owns only producer B's typed event layout.",
            negative_scope="One exact producer body; no other producer or subscriber is excluded.",
            primary_span="event19_producer_205",
            prior_claims=(prior["qme_general_census"],),
            nonclaim="Numeric value 0x205 is not assigned a gameplay name, and the target actor's concrete class is UNKNOWN.",
            blocker="The receiving subscriber's interpretation of +0x14=0x205 is not proved.",
            required_next_evidence="Typed subscriber branch consuming kind 0x19 with +0x14=0x205.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-004",
            row_kind="EVENT19_QUERY_RESULT_GATE",
            decision_surface="CNetNPC_interaction_query_gate",
            evidence_layer="STATIC_NATIVE",
            applies_to_class="CNetNPC",
            input_or_condition="prior CNetNPC relation/NPCAttr gate passes; query event kind=0x12 returns event +0x14 nonzero",
            exact_observation="After the prior CNetNPC interaction gate, this path constructs a query event, writes +0x10=0x12, dispatches it through the target CNetNPC owner at +0x130, and requires the returned byte at event +0x14 to be nonzero before continuing toward distance handling.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Pinned span hash plus exact constructor, immediate store, query-dispatch call, owner-base, and result-byte comparison anchors.",
            control="CNETNPC_INTERACTION_ACTION_GATE is cited as the preceding canonical gate and is not copied.",
            negative_scope="Necessary only on this audited interaction route; not a universal talkability or attackability predicate.",
            primary_span="event19_query_gate",
            prior_claims=(prior["role_action_gate"],),
            nonclaim="Event kind 0x12 is not assigned a global gameplay name, and a nonzero result does not prove that the original server will send a conversation response.",
            blocker="The exact subscriber that sets event +0x14 and its original policy inputs are not closed here.",
            required_next_evidence="Typed subscriber result producer or a source-separated live trace of this query result for controlled actor roles.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-005",
            row_kind="EVENT19_DISTANCE_OR_APPROACH_BRANCH",
            decision_surface="CNetNPC_near_send_or_approach_attachment",
            evidence_layer="STATIC_NATIVE",
            applies_to_class="CNetNPC",
            input_or_condition="event19 query result passes; real-position distance is within threshold or exceeds threshold",
            exact_observation="After the query gate, two native position lanes compute distance. Within threshold control reaches the already-canonical ChooseNPC send. Beyond threshold each lane requests a 0x50-byte object, initializes it through 0x00475690, and attaches the result through 0x004843F0.",
            semantic_status="PROVEN_ROLE_ONLY",
            measurement_method="Pinned whole decision span and two approach-branch hashes; exact threshold branch, allocation-size, initializer-call, and attachment-call anchors.",
            control="The near ChooseNPC identity/send fact is cited from CNETNPC_INTERACTION_CHOOSE_NPC_GENERIC rather than copied as new evidence.",
            negative_scope="The allocated object's class and completion behavior are outside these spans; no universal interaction-distance policy is claimed.",
            primary_span="event19_distance_approach",
            support_spans=("approach_branch_a", "approach_branch_b"),
            prior_claims=(prior["role_choose_npc"],),
            nonclaim="Allocation size 0x50 is not a class identity. This does not prove that every beyond-threshold path later sends ChooseNPC or that approaching makes a target non-attackable.",
            blocker="The approach object's RTTI/vtable and completion callback are UNKNOWN.",
            required_next_evidence="Resolve the 0x00475690 object type and follow its completion callback to a same-target ChooseNPC or cancellation edge.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-006",
            row_kind="NPC_CONVERSATION_INBOUND_QUESTMODULE_FORWARD",
            decision_surface="NPCConversation_registered_handler_to_QuestModule",
            evidence_layer="WIRE_CODEC",
            applies_to_class="NPCConversation",
            input_or_condition="registered NPCConversation handler receives a message and resolves QuestModule",
            exact_observation="The registered NPCConversation handler resolves QuestModule through local actor +0x130, validates the resolved object, and forwards the inbound message to 0x0061A950.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Registry-row reference plus pinned handler hash, exact QuestModule ASCII literal span/content, and exact module-lookup, validation, and forward-call anchors.",
            control="NPCConversation registry mapping is cited; no UI-layer fact is included in this WIRE_CODEC row.",
            negative_scope="One registered inbound handler body only.",
            primary_span="npc_conversation_handler",
            support_spans=("quest_module_literal",),
            prior_claims=(prior["registry_npc_conversation"],),
            nonclaim="This does not prove that every ChooseNPC yields NPCConversation or what original-server condition emits this response.",
            blocker="ChooseNPC-to-NPCConversation original response policy is not established by these audited IMAGE surfaces.",
            required_next_evidence="Source-separated original trace linking one ChooseNPC target to an NPCConversation response.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-007",
            row_kind="NPC_CONVERSATION_QUEST_UI",
            decision_surface="NPCConversation_dispatch_to_QuestModule_UI",
            evidence_layer="UI_NATIVE",
            applies_to_class="QuestModule",
            input_or_condition="dispatcher cast through getter 0x006216F0 succeeds",
            exact_observation="The dispatcher copies message +0x18/+0x1C to QuestModule +0x80/+0x84, chooses Quest_NPC_Conversation_New or Quest_NPC_Conversation, and calls UI vslot +0x210 with InitQuestList.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Pinned dispatcher hash, exact QuestModule ASCII literal span/content, exact cast/copy/model-pointer/vslot anchors, and three UTF-16 literal hashes.",
            control="ARIG-IMG-006 owns the registered inbound forwarding edge; this row begins at the UI dispatcher.",
            negative_scope="One quest-conversation UI dispatcher path; not a census of service pages.",
            primary_span="npc_conversation_dispatcher",
            support_spans=("quest_module_literal", "quest_ui_model_new", "quest_ui_model_old", "init_quest_list_literal"),
            prior_claims=(prior["registry_npc_conversation"],),
            nonclaim="The UI composition does not prove that every NPCConversation uses the same model or reveal original service-page policy.",
            blocker="The message fields' complete server-side content policy is not established by these audited IMAGE surfaces.",
            required_next_evidence="Source-separated original response samples joined by message identity, without merging evidence layers.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-008",
            row_kind="CHOOSE_NPC_REGISTERED_ROUTINE_BOUNDARY",
            decision_surface="ChooseNPC_registered_handler_boundary",
            evidence_layer="WIRE_CODEC",
            applies_to_class="ChooseNPC",
            input_or_condition="PF_PROTOCOL_REGISTRY maps ChooseNPC handler slot to 0x00710440",
            exact_observation="The registered ChooseNPC routine at 0x00710440 consists only of mov al,1 followed by ret 4. It contains no UI or service side effect; the proved quest UI route is a separate inbound NPCConversation path.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Pin the exact ChooseNPC registry row, hash the five-byte routine, and verify the complete routine byte sequence.",
            control="ChooseNPC registry row is referenced instead of republished as a new registry claim.",
            negative_scope="Only this registered five-byte routine body; other send orchestration and server response handlers are outside the negative.",
            primary_span="choose_npc_handler",
            prior_claims=(prior["registry_choose_npc"],),
            nonclaim="A constant-true registered routine does not mean ChooseNPC is accepted by the original server and does not classify the target as NPC, monster, or dummy.",
            blocker="Original response policy is not encoded in this routine.",
            required_next_evidence="Source-separated original wire/runtime evidence for the response family produced after ChooseNPC.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-009",
            row_kind="RELATION_CONSTANT_FALSE_RESULT_SURFACE",
            decision_surface="relation_predicate_final_result_producer",
            evidence_layer="STATIC_NATIVE",
            applies_to_class="UNKNOWN",
            input_or_condition="control reaches cleanup surface 0x0043C48F",
            exact_observation="This final result-producer surface cleans up its temporary object, executes xor al,al, and joins the common function return with result 0.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Pinned branch-surface hash plus exact cleanup, xor-al, and common-return jump anchors inside the full relation predicate.",
            control="MCMJ-IMG-004 already establishes that earlier overrides exist before the fallback; this row adds only the final result surface.",
            negative_scope="No upstream condition is semantically named by this row.",
            primary_span="relation_false_return",
            support_spans=("relation_predicate",),
            prior_claims=(prior["mcmj_fallback"], prior["role_relation_false_target"]),
            nonclaim="Result 0 is not globally named hostile, monster, or attackable. Two prior target-selection callers consume false, but that is not a universal law.",
            blocker="The exact upstream branch predicates and per-caller meaning must be kept contextual.",
            required_next_evidence="Use decoder-validated per-callsite context; do not collapse all callers into one role label.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-010",
            row_kind="RELATION_COMPARATOR_RESULT_SURFACE",
            decision_surface="relation_predicate_final_result_producer",
            evidence_layer="STATIC_NATIVE",
            applies_to_class="UNKNOWN",
            input_or_condition="all earlier relation overrides fall through to the +0x68 comparator path",
            exact_observation="This indexed final surface calls the prior-proved +0x68 comparator, preserves its AL result across cleanup, restores AL, and joins the common return. Comparator semantics remain owned by MCMJ-IMG-003/004.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Pinned final-surface hash and call/preserve/restore anchors; prior comparator/fallback claims are referenced and not re-owned.",
            control="MCMJ-IMG-003 and MCMJ-IMG-004 own comparator boolean and argument binding.",
            negative_scope="This is one fallback result surface, not the whole relation predicate or an unconditional faction rule.",
            primary_span="relation_comparator_return",
            support_spans=("relation_predicate",),
            prior_claims=(prior["mcmj_comparator"], prior["mcmj_fallback"]),
            nonclaim="The row does not rename comparator true/false as NPC/monster and does not independently restate FACTION semantics.",
            blocker="Earlier exits can bypass this comparator, and live +0x68 inputs are runtime facts.",
            required_next_evidence="Per-callsite branch tracing or source-separated runtime evidence proving the taken surface and both +0x68 values.",
        ),
        make_row(
            image,
            sections,
            graph_key="ARIG-IMG-011",
            row_kind="RELATION_CONSTANT_TRUE_RESULT_SURFACE",
            decision_surface="relation_predicate_final_result_producer",
            evidence_layer="STATIC_NATIVE",
            applies_to_class="UNKNOWN",
            input_or_condition="control reaches cleanup surface 0x0043C5FF",
            exact_observation="This final result-producer surface cleans up its temporary object, executes mov al,1, and falls into the common function return with result 1.",
            semantic_status="PROVEN_EXACT",
            measurement_method="Pinned branch-surface hash plus exact cleanup and mov-al-1 anchors inside the full relation predicate.",
            control="MCMJ-IMG-004 records the fallback boundary and explicitly warns that earlier exits exist.",
            negative_scope="No upstream condition is semantically named by this row.",
            primary_span="relation_true_return",
            support_spans=("relation_predicate",),
            prior_claims=(prior["mcmj_fallback"],),
            nonclaim="Result 1 is not globally named friendly, NPC, or talkable; downstream callers use relation context differently.",
            blocker="The exact upstream branch predicates and per-caller meaning must be kept contextual.",
            required_next_evidence="Use decoder-validated per-callsite context; do not collapse all callers into one role label.",
        ),
    ]

    category_observations = {
        "talk_interact": "The decoder-validated call is in a bounded talk/interact-adjacent surrounding-output family.",
        "target_presentation": "The decoder-validated call is in a bounded target-presentation surrounding-output family.",
        "enemy_target_target_state": "The decoder-validated call is in a bounded enemy-target or target-state surrounding-output family.",
        "color_style": "The decoder-validated call is in a bounded color/style/nameboard surrounding-output family.",
        "unresolved": "The decoder-validated call has no safe named surrounding-output family in this bounded audit and remains UNRESOLVED.",
    }
    for ordinal, site in enumerate(relation_sites, start=12):
        category = category_by_site[site]
        if site == 0x00444018:
            site_prior = (prior["mcmj_selector_positive"],)
        elif site == 0x00444152:
            site_prior = (prior["mcmj_selector_nonpositive"],)
        elif site in {0x0051F3B3, 0x005213A5}:
            site_prior = (prior["role_relation_false_target"],)
        elif site in {0x0051FBC2, 0x00523554}:
            site_prior = (prior["role_targetvital_kind"],)
        elif site == 0x00619790:
            site_prior = (prior["role_action_gate"],)
        else:
            site_prior = (prior["mcmj_fallback"],)
        category_lines = [
            relation_site_lines[value]
            for value in relation_sites
            if category_by_site[value] == category
        ]
        semantic_status = "UNRESOLVED" if category == "unresolved" else "PROVEN_ROLE_ONLY"
        rows.append(
            make_row(
                image,
                sections,
                graph_key=f"ARIG-IMG-{ordinal:03d}",
                row_kind=f"RELATION_CALLSITE_{category.upper()}",
                decision_surface=f"relation_callsite_0x{site:08X}",
                evidence_layer="STATIC_NATIVE",
                applies_to_class=EXACT_SITE_CLASSES.get(site, "UNKNOWN"),
                input_or_condition=f"instruction-start E8 call at 0x{site:08X} resolves to 0x0043C380",
                exact_observation=category_observations[category],
                semantic_status=semantic_status,
                measurement_method="Whole file-backed executable-section E8+rel32 byte-pattern census followed by an actual Capstone 5.0.6 x86-32 skipdata linear sweep anchored at .text 0x00401000 proves the call boundary/target. An independent manual static-disassembly review of this exact pinned local window assigns only the bounded surrounding-output family; the generator revalidates the reviewed exact per-key category map and partition digest but does not infer the family name. Site and partition digests are SHA256 of ASCII lines joined by LF with one terminal LF.",
                control=f"decoder=capstone-{CAPSTONE_VERSION};decoder_mode=x86-32;decoder_anchor=0x00401000;skipdata=1;all_count=31;classification=independent_manual_static_review;partition_digest={partition_digest};category={category};category_count={len(category_lines)};category_digest={digest_lines(category_lines)}",
                negative_scope="Direct E8 sites and the named bounded local output family only; no CFG/runtime reachability or completeness for indirect, dynamic, alias, or tail-call routes.",
                primary_span=f"relation_call_{site:08x}",
                support_spans=("relation_predicate",),
                site_lines=(relation_site_lines[site],),
                prior_claims=site_prior,
                nonclaim="The category is not a relation-domain or actor-role label and does not name true/false as NPC, monster, friendly, hostile, talkable, or attackable.",
                blocker=(
                    "Typed receiver and downstream result remain unresolved."
                    if category == "unresolved"
                    else "Original-server input assignment and per-call runtime branch remain open."
                ),
                required_next_evidence=(
                    "Exact typed receiver plus downstream consumer proof for this site."
                    if category == "unresolved"
                    else "Source-separated runtime branch/input evidence only if original policy is required."
                ),
            )
        )

    return rows


def validate_rows(rows: Sequence[Mapping[str, str]], prior_rows: Mapping[Path, Sequence[Mapping[str, str]]]) -> None:
    if not rows:
        raise RuntimeError("no output rows")
    if any(tuple(row) != FIELDNAMES for row in rows):
        raise RuntimeError("output schema/order drift")
    if tuple(row["graph_key"] for row in rows) != EXPECTED_GRAPH_KEYS:
        raise RuntimeError("output graph-key set/order drift")
    exact_mappings = (
        ("row_kind", EXPECTED_ROW_KINDS, "output row-kind mapping drift"),
        ("evidence_layer", EXPECTED_EVIDENCE_LAYERS, "output evidence-layer mapping drift"),
        ("applies_to_class", EXPECTED_CLASSES, "output class mapping drift"),
        ("semantic_status", EXPECTED_SEMANTIC_STATUSES, "output semantic-status mapping drift"),
        ("measurement_label", EXPECTED_MEASUREMENT_LABELS, "output measurement-label mapping drift"),
    )
    for field, expected, error in exact_mappings:
        if tuple(row[field] for row in rows) != expected:
            raise RuntimeError(error)
    if len({row["graph_key"] for row in rows}) != len(rows):
        raise RuntimeError("duplicate graph key")
    if len({row["claim_sha256"] for row in rows}) != len(rows):
        raise RuntimeError("duplicate claim digest")
    if len({row["evidence_key"] for row in rows}) != len(rows):
        raise RuntimeError("duplicate evidence key")
    allowed_layers = {"STATIC_NATIVE", "LUA_BRIDGE", "UI_NATIVE", "WIRE_CODEC"}
    allowed_measurements = {"MEASURED"}
    prior_evidence = {
        row.get("evidence_key", "")
        for prior in prior_rows.values()
        for row in prior
        if row.get("evidence_key")
    }
    prior_claims = {
        row.get("claim_sha256", "")
        for prior in prior_rows.values()
        for row in prior
        if row.get("claim_sha256")
    }
    prior_key_columns = {
        ROLE_PATH: "discriminator_id",
        QME_PATH: "event_key",
        MCMJ_PATH: "join_key",
        REGISTRY_PATH: "name",
    }
    valid_prior_triplets: set[tuple[str, str, str]] = set()
    for path, prior in prior_rows.items():
        key_column = prior_key_columns[path]
        for prior_row in prior:
            key = prior_row.get(key_column, "")
            if not key:
                raise RuntimeError("prior row lacks its pinned key column")
            prior_evidence_key = prior_row.get("evidence_key", "")
            suffix = "@" + prior_evidence_key if prior_evidence_key else ""
            token = "%s:%s%s" % (path.name, key, suffix)
            digest = prior_row.get("claim_sha256", "") or canonical_row_digest(
                prior_row
            )
            valid_prior_triplets.add((token, PRIOR_PINS[path][1], digest))
    for row in rows:
        if row["source"] != SOURCE:
            raise RuntimeError("mixed or invalid source")
        if row["evidence_layer"] not in allowed_layers:
            raise RuntimeError("invalid evidence layer")
        if row["measurement_label"] not in allowed_measurements:
            raise RuntimeError("measurement label drift")
        if not row["required_next_evidence"].startswith("PROPOSED: "):
            raise RuntimeError("required-next-evidence proposal label drift")
        if not row["applies_to_class"]:
            raise RuntimeError("empty applies_to_class")
        if row["prior_reference"] == "N/A" or row["prior_claim_digest"] == "N/A":
            raise RuntimeError("row lacks prior reference/digest")
        references = row["prior_reference"].split(";")
        artifact_hashes = row["prior_artifact_sha256"].split(";")
        digests = row["prior_claim_digest"].split(";")
        if not (len(references) == len(artifact_hashes) == len(digests)):
            raise RuntimeError("prior reference/hash/digest cardinality mismatch")
        if not all(
            len(value) == 64 and all(c in "0123456789abcdef" for c in value)
            for value in artifact_hashes
        ):
            raise RuntimeError("prior artifact hash format drift")
        if not all(len(value) == 64 and all(c in "0123456789abcdef" for c in value) for value in digests):
            raise RuntimeError("prior claim digest format drift")
        if not all(
            triplet in valid_prior_triplets
            for triplet in zip(references, artifact_hashes, digests)
        ):
            raise RuntimeError("prior citation tuple is absent from pinned inputs")
        if row["site_list"] == "N/A":
            if row["site_count"] != "0" or row["site_digest"] != "N/A":
                raise RuntimeError("empty site metadata mismatch")
        else:
            lines = row["site_list"].split("||")
            if int(row["site_count"]) != len(lines):
                raise RuntimeError("site count mismatch")
            if digest_lines(lines) != row["site_digest"]:
                raise RuntimeError("site list digest mismatch")
        claim_fields = {
            key: value for key, value in row.items() if key not in {"claim_sha256", "evidence_key"}
        }
        if canonical_row_digest(claim_fields) != row["claim_sha256"]:
            raise RuntimeError("claim digest mismatch")
        expected_evidence = sha256(
            ROW_DOMAIN
            + row["claim_sha256"].encode("ascii")
            + b"\x00"
            + row["span_sha256"].encode("ascii")
            + b"\x00"
            + IMAGE_SHA256.encode("ascii")
        )
        if row["evidence_key"] != expected_evidence:
            raise RuntimeError("evidence key mismatch")
        if row["evidence_key"] in prior_evidence:
            raise RuntimeError("evidence key duplicates prior artifact")
        if row["claim_sha256"] in prior_claims:
            raise RuntimeError("claim digest duplicates prior artifact")


def render_tsv(rows: Sequence[Mapping[str, str]]) -> bytes:
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
    return stream.getvalue().encode("ascii")


def render_report(rows: Sequence[Mapping[str, str]], tsv_sha256: str) -> bytes:
    counts = Counter(row["evidence_layer"] for row in rows)
    measurement_counts = Counter(row["measurement_label"] for row in rows)
    callsite_rows = [
        row for row in rows if row["row_kind"].startswith("RELATION_CALLSITE_")
    ]
    callsite_categories = Counter(
        row["row_kind"].removeprefix("RELATION_CALLSITE_").lower()
        for row in callsite_rows
    )
    partition_digest = digest_lines([row["site_list"] for row in callsite_rows])
    report = f"""# PF Actor Relation Interaction Graph

## Scope and result

This is an additive, IMAGE-only P0-4 artifact. It uses a neutral actor
relation/interaction title because the audited client decisions do not prove one
universal monster flag.

P0-4 has two different questions:

1. **Audited client-local IMAGE mechanisms.** This artifact closes the bounded
   surfaces listed below: kind-0x19 registration and its two typed target
   producers, the CNetNPC query-result gate, near-send versus approach attachment,
   the separately layered NPCConversation inbound/UI route, the ChooseNPC
   registered routine boundary, and the relation function's final result
   surfaces plus 31 per-site direct-call rows.
2. **Original-server assignment policy.** This remains **OPEN**. These audited
   IMAGE surfaces do not establish how the original server chose relation inputs,
   NPCAttr flags, parsed MOBS values, conversation responses, or attack eligibility.
   Those inputs must not be inferred from the client-local mechanisms.

## New measured and manually reviewed IMAGE facts

- `ARIG-IMG-001`: the canonical general-registration control remains 140 direct
  registrations with digest `{EXPECTED_GENERAL_REGISTRATION_DIGEST}`. Filtering
  that same instruction-shape census yields exactly one direct kind-0x19 site,
  `0x00615B7A`, with subset digest `{EXPECTED_EVENT19_SITE_DIGEST}`.
- `ARIG-IMG-002` and `ARIG-IMG-003` separately record the two kind-0x19
  producer bodies. Both carry target identity and target pointer fields; numeric
  values 0x201 and 0x205 remain unnamed and the target class is UNKNOWN.
- `ARIG-IMG-004`: one typed CNetNPC interaction route additionally requires a
  synchronous query result byte at event +0x14 to be nonzero.
- `ARIG-IMG-005`: after that gate, native distance logic either reaches the
  already-canonical ChooseNPC send or attaches an UNKNOWN 0x50-byte approach
  object. Allocation size is not a class identity.
- `ARIG-IMG-006` is WIRE_CODEC only: the registered NPCConversation handler
  resolves QuestModule and forwards the inbound message. `ARIG-IMG-007` is
  UI_NATIVE only: it copies message +0x18/+0x1C to module +0x80/+0x84, chooses one
  of two quest-conversation UI models, and calls vslot +0x210 with InitQuestList.
  The composition is stated here; the TSV does not mix those evidence layers.
- `ARIG-IMG-008`: the registered ChooseNPC routine is only `mov al,1; ret 4`; no
  UI/service side effect exists inside that five-byte routine.
- `ARIG-IMG-009..011`: the relation predicate has final result surfaces returning
  constant 0, the prior-owned +0x68 comparator result, or constant 1. These rows
  index result production only and do not rename either boolean.
- `ARIG-IMG-012..042`: {len(callsite_rows)} file-backed executable-section
  E8+rel32 byte-pattern sites resolve to 0x0043C380. All 31 raw sites were
  independently validated by the generator itself as instruction-start
  `call 0x0043C380` in a pinned Capstone {CAPSTONE_VERSION} x86-32 skipdata linear
  sweep anchored at `.text` 0x00401000. Every site has its own exact trusted local
  span/hash, source, layer, class-or-UNKNOWN, prior digest, and nonclaim. Partition
  digest `{partition_digest}` uses
  `SHA256(ASCII site lines joined by LF plus one terminal LF)`.
  The surrounding-output family is a separately described manual-review component
  of the measured row: independent static-disassembly review covers each pinned
  local span, while the generator validates the frozen per-key category/status map
  but does not infer those labels.

| Bounded surrounding-output family | Sites | Meaning ceiling |
|---|---:|---|
| talk/interact-adjacent | {callsite_categories['talk_interact']} | not talkable/role |
| target presentation | {callsite_categories['target_presentation']} | not actor class |
| enemy target / target state | {callsite_categories['enemy_target_target_state']} | not universal hostility |
| color/style/nameboard | {callsite_categories['color_style']} | not role or rendered pixels |
| unresolved | {callsite_categories['unresolved']} | UNRESOLVED |

The five manually reviewed categories describe only bounded surrounding output.
They are not relation-domain labels. The 31-site mechanical call census is not a
CFG/runtime census and excludes indirect calls, dynamic targets, aliases, and
tail-call routes. A prior manual consumer audit of MOBS +0x48 / BasicAttr +0x6C is
deliberately not published as a TSV negative because this re-deriver does not
reproduce its function-body/alias coverage.

## What remains non-implementable

- `NPCAttr +0x7A` remains a bounded gate in one CNetNPC route. Its original
  producer/policy and universal role meaning are not proved.
- `BasicAttr +0x6C` retains the prior `LOADED_COPIED_ONLY` ceiling. This artifact
  publishes no new deterministic consumer census for it.
- MOBS `n_AI_COMBAT` retains the prior `LOADER_ONLY` ceiling. This artifact
  publishes no new deterministic parsed-MOBS +0x48 consumer negative.
- The 0x50-byte approach object's class/completion callback is UNKNOWN.
- ChooseNPC-to-NPCConversation original response policy is not established by
  these audited IMAGE surfaces.

Eleven same-IMAGE direct-callsite contexts remain UNRESOLVED with exact
next-evidence requests. This IMAGE artifact does not own checkpoint sequencing or
apply the master anti-stall policy; canonical checkpoint authority must make that
operational decision. The bounded evidence verdict is:

`BOUNDED_STATIC_GRAPH / ORIGINAL_POLICY_OPEN`

## Evidence discipline

- Rows: {len(rows)}; source IMAGE: {sum(row['source'] == 'IMAGE' for row in rows)}.
- Layers: STATIC_NATIVE={counts['STATIC_NATIVE']}, LUA_BRIDGE={counts['LUA_BRIDGE']}, UI_NATIVE={counts['UI_NATIVE']}, WIRE_CODEC={counts['WIRE_CODEC']}.
- Measurement labels: MEASURED={measurement_counts['MEASURED']}; the 31 callsite
  rows name `classification=independent_manual_static_review` in their controls.
- Every row has one source, an exact class or UNKNOWN, measurement method, control,
  negative scope, VA/file span, SHA-256, prior reference, and prior claim digest.
- Prior facts are cited rather than copied. For prior artifacts without an embedded
  `claim_sha256`, `prior_claim_digest` is SHA-256 of the selected complete TSV row
  serialized as sorted compact ASCII JSON.
- TSV SHA256: `{tsv_sha256}`.
- Image size: {IMAGE_SIZE}; image SHA256 before/after: `{IMAGE_SHA256}`.

## Re-derive

```powershell
py -3 pf_rederive_actor_relation_interaction_graph.py --check
py -3 pf_rederive_actor_relation_interaction_graph.py --self-test
```

`--check` rebuilds exact bytes in memory, verifies every pinned input/span/anchor,
validates exact per-key row-kind/layer/class/status/measurement maps plus the
source/prior/duplicate/site-list guards, rejects an observed publication lock, and
rejects precisely named artifact-stage debris before/after checking a stable
marker-before/files-twice/marker-after committed snapshot without writing outputs.
`--self-test` mutates the listed source, allowed-but-wrong layer, unsupported class,
status, reviewed category, measurement label, prior digest, site list, row-set,
claim/evidence uniqueness, and candidate/rendered pair cases in memory. It does not
validate committed files; that is the role of `--check`.
"""
    return report.encode("ascii")


def render_pair_marker(outputs: Mapping[Path, bytes]) -> bytes:
    digest = hashlib.sha256(PAIR_DOMAIN)
    files: list[dict[str, object]] = []
    for path in (TSV_PATH, REPORT_PATH):
        raw = outputs[path]
        name = path.name.encode("ascii")
        digest.update(len(name).to_bytes(4, "little"))
        digest.update(name)
        digest.update(len(raw).to_bytes(8, "little"))
        digest.update(raw)
        files.append({"name": path.name, "size": len(raw), "sha256": sha256(raw)})
    marker = {
        "schema": 1,
        "commit_rule": "marker-before/files-twice/marker-after; exact bytes and hashes",
        "generation_sha256": digest.hexdigest(),
        "files": files,
    }
    return (json.dumps(marker, indent=2, sort_keys=True) + "\n").encode("ascii")


def verify_pair_bytes(
    outputs: Mapping[Path, bytes], marker: bytes
) -> str:
    try:
        decoded = json.loads(marker.decode("ascii"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("pair marker decode failed") from exc
    expected = render_pair_marker(outputs)
    if marker != expected:
        raise RuntimeError("pair marker does not name exact output bytes")
    if decoded.get("schema") != 1:
        raise RuntimeError("pair marker schema drift")
    generation = decoded.get("generation_sha256", "")
    if not isinstance(generation, str) or len(generation) != 64:
        raise RuntimeError("pair generation digest invalid")
    return generation


def read_committed_pair(
    expected_outputs: Mapping[Path, bytes],
    expected_marker: bytes,
    *,
    require_no_publisher: bool = False,
) -> dict[Path, bytes]:
    if require_no_publisher and LOCK_PATH.exists():
        raise RuntimeError("publication lock exists during committed check")
    if not PAIR_PATH.is_file():
        raise RuntimeError(f"pair marker missing: {PAIR_PATH.name}")
    marker_before = PAIR_PATH.read_bytes()
    first = {path: path.read_bytes() for path in (TSV_PATH, REPORT_PATH)}
    second = {path: path.read_bytes() for path in (TSV_PATH, REPORT_PATH)}
    marker_after = PAIR_PATH.read_bytes()
    if marker_before != marker_after or marker_after != expected_marker:
        raise RuntimeError("pair marker changed or names a different generation")
    if first != second:
        raise RuntimeError("output pair changed during stable read")
    for path, expected in expected_outputs.items():
        if second[path] != expected:
            raise RuntimeError(f"exact output differs: {path.name}")
    verify_pair_bytes(second, marker_after)
    if require_no_publisher and LOCK_PATH.exists():
        raise RuntimeError("publication lock appeared during committed check")
    return second


def acquire_lock() -> int:
    try:
        descriptor = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise RuntimeError(
            f"output lock exists; inspect before removal: {LOCK_PATH.name}"
        ) from exc
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
        os.fsync(descriptor)
    except Exception:
        os.close(descriptor)
        LOCK_PATH.unlink(missing_ok=True)
        raise
    return descriptor


def reject_stage_debris(context: str) -> None:
    debris = sorted(
        path.name
        for path in OUT_DIR.iterdir()
        if path.is_file()
        and path.name.endswith(".stage")
        and any(path.name.startswith(prefix) for prefix in STAGE_PREFIXES)
    )
    if debris:
        raise RuntimeError(
            "publication stage debris exists %s: %s"
            % (context, ",".join(debris))
        )


def release_lock(descriptor: int) -> None:
    os.close(descriptor)
    LOCK_PATH.unlink()


def stage_bytes(path: Path, raw: bytes) -> Path:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".stage", dir=path.parent
    )
    staged = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if staged.read_bytes() != raw:
            raise RuntimeError(f"staged byte check failed: {path.name}")
        return staged
    except Exception:
        staged.unlink(missing_ok=True)
        raise


def publish(outputs: Mapping[Path, bytes], marker: bytes) -> None:
    staged: dict[Path, Path] = {}
    try:
        for path in (TSV_PATH, REPORT_PATH):
            staged[path] = stage_bytes(path, outputs[path])
        staged[PAIR_PATH] = stage_bytes(PAIR_PATH, marker)
        staged_outputs = {
            path: staged[path].read_bytes() for path in (TSV_PATH, REPORT_PATH)
        }
        verify_pair_bytes(staged_outputs, staged[PAIR_PATH].read_bytes())
        for path in (TSV_PATH, REPORT_PATH, PAIR_PATH):
            os.replace(staged[path], path)
            del staged[path]
        read_committed_pair(outputs, marker)
    finally:
        for path in staged.values():
            path.unlink(missing_ok=True)


def expect_failure(label: str, function, expected_error: str | None = None) -> None:
    try:
        function()
    except RuntimeError as exc:
        if expected_error is not None and expected_error not in str(exc):
            raise RuntimeError(
                f"self-test mutation reached wrong guard: {label}: {exc}"
            ) from exc
        return
    raise RuntimeError(f"self-test mutation was accepted: {label}")


def run_self_test(
    rows: Sequence[Mapping[str, str]],
    prior_rows: Mapping[Path, Sequence[Mapping[str, str]]],
    outputs: Mapping[Path, bytes],
    marker: bytes,
) -> None:
    validate_rows(rows, prior_rows)

    def rehash(row: dict[str, str]) -> None:
        claim_fields = {
            key: value
            for key, value in row.items()
            if key not in {"claim_sha256", "evidence_key"}
        }
        row["claim_sha256"] = canonical_row_digest(claim_fields)
        row["evidence_key"] = sha256(
            ROW_DOMAIN
            + row["claim_sha256"].encode("ascii")
            + b"\x00"
            + row["span_sha256"].encode("ascii")
            + b"\x00"
            + IMAGE_SHA256.encode("ascii")
        )

    def mutated(index: int, field: str, value: str) -> list[dict[str, str]]:
        copy = [dict(row) for row in rows]
        copy[index][field] = value
        rehash(copy[index])
        return copy

    expect_failure(
        "source",
        lambda: validate_rows(mutated(0, "source", "DATA"), prior_rows),
        "mixed or invalid source",
    )
    expect_failure(
        "allowed_but_wrong_layer",
        lambda: validate_rows(mutated(0, "evidence_layer", "WIRE_CODEC"), prior_rows),
        "output evidence-layer mapping drift",
    )
    expect_failure(
        "unsupported_class",
        lambda: validate_rows(mutated(35, "applies_to_class", "CNetNPC"), prior_rows),
        "output class mapping drift",
    )
    expect_failure(
        "allowed_but_wrong_status",
        lambda: validate_rows(mutated(26, "semantic_status", "PROVEN_EXACT"), prior_rows),
        "output semantic-status mapping drift",
    )
    expect_failure(
        "reviewed_category",
        lambda: validate_rows(
            mutated(26, "row_kind", "RELATION_CALLSITE_TALK_INTERACT"),
            prior_rows,
        ),
        "output row-kind mapping drift",
    )
    expect_failure(
        "manual_measurement_label",
        lambda: validate_rows(mutated(11, "measurement_label", "PROPOSED"), prior_rows),
        "output measurement-label mapping drift",
    )
    bad_prior = rows[0]["prior_claim_digest"][:-1] + (
        "0" if rows[0]["prior_claim_digest"][-1] != "0" else "1"
    )
    expect_failure(
        "prior_digest",
        lambda: validate_rows(mutated(0, "prior_claim_digest", bad_prior), prior_rows),
        "prior citation tuple is absent from pinned inputs",
    )
    expect_failure(
        "site_list",
        lambda: validate_rows(
            mutated(0, "site_list", rows[0]["site_list"] + ";injected"),
            prior_rows,
        ),
        "site list digest mismatch",
    )
    expect_failure(
        "missing_graph_row",
        lambda: validate_rows(list(rows[:-1]), prior_rows),
        "output graph-key set/order drift",
    )
    duplicate_claim_rows = [dict(row) for row in rows]
    duplicate_claim_rows[1]["claim_sha256"] = duplicate_claim_rows[0]["claim_sha256"]
    expect_failure(
        "duplicate_claim_digest",
        lambda: validate_rows(duplicate_claim_rows, prior_rows),
        "duplicate claim digest",
    )
    duplicate_evidence_rows = [dict(row) for row in rows]
    duplicate_evidence_rows[1]["evidence_key"] = duplicate_evidence_rows[0]["evidence_key"]
    expect_failure(
        "duplicate_evidence_key",
        lambda: validate_rows(duplicate_evidence_rows, prior_rows),
        "duplicate evidence key",
    )
    broken_outputs = dict(outputs)
    broken_outputs[TSV_PATH] = outputs[TSV_PATH] + b"X"
    expect_failure(
        "mixed_pair", lambda: verify_pair_bytes(broken_outputs, marker)
    )


def derive_all() -> tuple[
    list[dict[str, str]],
    Mapping[Path, Sequence[Mapping[str, str]]],
    dict[Path, bytes],
    bytes,
    str,
]:
    image = read_pinned(IMAGE_PATH, IMAGE_SIZE, IMAGE_SHA256)
    sections = parse_pe(image)
    facts = verify_static_anchors(image, sections)
    prior, prior_rows = build_prior_claims()
    rows = build_rows(image, sections, facts, prior)
    validate_rows(rows, prior_rows)
    tsv_raw = render_tsv(rows)
    report_raw = render_report(rows, sha256(tsv_raw))
    outputs = {TSV_PATH: tsv_raw, REPORT_PATH: report_raw}
    marker = render_pair_marker(outputs)
    generation = verify_pair_bytes(outputs, marker)
    return rows, prior_rows, outputs, marker, generation


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="ascii", errors="backslashreplace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="ascii", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify exact committed outputs")
    mode.add_argument("--self-test", action="store_true", help="run in-memory mutation guards")
    args = parser.parse_args()

    if args.check and LOCK_PATH.exists():
        raise RuntimeError("publication lock exists before committed check")
    lock = None if (args.check or args.self_test) else acquire_lock()
    try:
        if args.check:
            reject_stage_debris("before committed check")
        elif lock is not None:
            reject_stage_debris("before publish derivation")
        before = sha256(read_pinned(IMAGE_PATH, IMAGE_SIZE, IMAGE_SHA256))
        rows, prior_rows, outputs, marker, generation = derive_all()
        if args.self_test:
            run_self_test(rows, prior_rows, outputs, marker)
            action = "self-test"
        elif args.check:
            read_committed_pair(outputs, marker, require_no_publisher=True)
            action = "check"
        else:
            publish(outputs, marker)
            reject_stage_debris("after publish")
            action = "publish"
        after = sha256(read_pinned(IMAGE_PATH, IMAGE_SIZE, IMAGE_SHA256))
        if before != after or before != IMAGE_SHA256:
            raise RuntimeError("image changed during derivation")
        if args.check:
            read_committed_pair(outputs, marker, require_no_publisher=True)
            reject_stage_debris("after committed check")
    finally:
        if lock is not None:
            release_lock(lock)
    counts = Counter(row["evidence_layer"] for row in rows)
    print(
        "PF_ACTOR_RELATION_INTERACTION_GRAPH: PASS "
        f"mode={action} rows={len(rows)} source_IMAGE={len(rows)} "
        f"static_native={counts['STATIC_NATIVE']} lua_bridge={counts['LUA_BRIDGE']} "
        f"ui_native={counts['UI_NATIVE']} wire_codec={counts['WIRE_CODEC']} "
        f"generation={generation} tsv_sha256={sha256(outputs[TSV_PATH])} "
        f"md_sha256={sha256(outputs[REPORT_PATH])} "
        f"image_sha256_before={before} image_sha256_after={after}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"PF_ACTOR_RELATION_INTERACTION_GRAPH: FAIL {exc}")
        raise SystemExit(1)
