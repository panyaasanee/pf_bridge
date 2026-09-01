#!/usr/bin/env python3
"""Deterministically re-derive the static QuestIconBoard lifecycle artifact.

This script reads the committed GameClient image and pinned, source-separated
reference artifacts.  It never runs the client, server, dumps, or captures.
It emits no raw proprietary byte sequence: only addresses, layouts, counts,
claims, and SHA-256 digests.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import struct
import sys
import tempfile
from typing import Any, Iterable, Mapping


IMAGE_NAME = "GameClient.local.bin"
IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"

SELECTOR_NAME = "PF_ATTR_QUEST_MARK_SELECTOR.tsv"
SELECTOR_SHA256 = "3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0"
SELECTOR_ROW_COUNT = 10
SELECTOR_REFERENCE_SET_SHA256 = "a1b636459217b7ff720be475e5dfb4a1d63b2e12816b4bd1c3a213fbc401cd48"

EVENT_NAME = "PF_QUEST_MARK_EVENT_CENSUS.tsv"
EVENT_SHA256 = "40127e6410c1aa6405efada640c60b72663eb9e35537c8011cdeede47d0a0b35"
EVENT_PAIR_SHA256 = "6a513a67f9e349150933fccf2ea7468538332b3f2553d0a6e8b0206475376dd3"
EVENT_REFERENCE_SET_SHA256 = "81e85bd46d3fed51e914c49b62a28f5f11a591b356c41c9e22a0090df426922a"
EVENT_REFERENCE_KEYS = {
    "QME-IMG-002": "6f02802cc1a27963b05fa99bdd728d5aeb9d62123f4127f63b25595891aaf514",
    "QME-IMG-003": "c3b5362cd18c56d8f81aa2d55125cfdafccda82ac6d7750dbcf7865eb17da44b",
    "QME-IMG-005": "7ac26b8ad88f926cf2cf3d50d935edd61ac7e44cfeb75dd12601386ef3d7f6dd",
    "QME-IMG-006": "5bd7beeb2d75b7e2fe4cf70be660f0bdb37ce5eb6067456c7464de959e6723a1",
    "QME-IMG-007": "aeb9b33c61c0dfdb02c624271d203c41cae68ca87b75185609eafdce6b5088f2",
    "QME-IMG-009": "b09bdbbd6d4f3950289ddda24db1a0c614a2afc37ddc825395f64132b1ca4dc6",
    "QME-IMG-010": "e02f04f5c635f95d9949b13e5bd7041f6e28ff7c1712ac18fe302296d35abc9c",
    "QME-IMG-015": "567860bdeff1e1b557f947b0b0ef0dad873f2599a0137e3e386a19b5ba90ceef",
    "QME-IMG-016": "3bec0468cf60ef54ac95da9ca8679eed0eb99d9d4464cad28d69fd1e4d25fdb4",
    "QME-IMG-017": "8be3f62040f283114adc9cbffad880b30f7400e855ca2b2dce2e3df4b0b74da1",
    "QME-IMG-018": "f03ad0a59d548d4e314cc116a7d19b4b377b4dd9edb55484a639a76a06003838",
    "QME-IMG-020": "993dde804583a012fc0a24ba92dad7ccf51a4c9e4c95f80233d435fe49129a1f",
}

RESOURCE_NAME = "PF_QUEST_MARK_RESOURCE_RESOLVER.tsv"
RESOURCE_SHA256 = "de491977008f1b3a0ab75da4a45bbba9cd35504350ecfbff95cfbec69a8641ab"
RESOURCE_MD_NAME = "PF_QUEST_MARK_RESOURCE_RESOLVER.md"
RESOURCE_MD_SHA256 = "f39f41cc91a5f6a7f1748933853e7d7ef0db393008588abf6fa73927421b71cc"
RESOURCE_PAIR_SHA256 = "c9c9e96ee67762cdaab18bf12d6cf22c1a4cf82c83270f50562a849c90985304"
RESOURCE_ROUTE_KEY = "79839063b5f2dad4f09c2c9022857ca6842763281547d762147f6939ccbb77cb"

GROUND_DROP_NAME = "PF_GROUND_DROP_LIFETIME.tsv"
GROUND_DROP_SHA256 = "b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710"
GROUND_DROP_REFERENCE_ID = "GDL-IMG-015"
GROUND_DROP_REFERENCE_KEY = "b014e9c7797a1d24b5c13eef598b7374223af5b548fe3efda538a43cd65a7d09"

TSV_NAME = "PF_QUEST_MARK_LIFECYCLE.tsv"
MD_NAME = "PF_QUEST_MARK_LIFECYCLE.md"
PAIR_PLACEHOLDER = "__PAIR_ID__"
SOURCE_URI = "PF_ROOT://GameClient/GameClient.local.bin"


COLUMNS = [
    "evidence_id",
    "row_kind",
    "lifecycle_stage",
    "subject",
    "semantic_status",
    "exact_observation",
    "value_or_layout",
    "evidence_file",
    "evidence_span_start",
    "evidence_span_end",
    "evidence_span_start_file_offset",
    "evidence_span_end_file_offset",
    "evidence_span_sha256",
    "support_spans",
    "evidence_key",
    "claim_sha256",
    "evidence_grade",
    "measurement_label",
    "method",
    "control",
    "source",
    "source_size",
    "source_sha256",
    "reference_artifact",
    "reference_sha256",
    "reference_keys",
    "nonclaim",
    "blocker",
    "required_next_evidence",
    "image_sha256",
    "pair_id",
]


SPAN_DEFS: list[dict[str, Any]] = [
    {
        "id": "QML-IMG-001",
        "stage": "OWNER_INITIAL_STATE",
        "subject": "CNetNPC board pointer and selector-cache seed",
        "start": 0x0045CC46,
        "end": 0x0045CCBC,
        "offset_start": 0x0005C046,
        "offset_end": 0x0005C0BC,
        "sha256": "d4ab65efec8b1ce51300eb86891c0c63b5bc3fa4ef3d83ae2d135959616493cf",
        "status": "PROVEN_EXACT",
        "observation": (
            "The CNetNPC constructor initializes owner slot +0x360 to null, "
            "retains that null after a defensive release path, and seeds byte "
            "+0x364 with 9 before the object is returned."
        ),
        "layout": "CNetNPC+0x360=QuestIconBoard_ref_or_null;CNetNPC+0x364=u8_selector_cache_seed_9",
        "support": "",
        "reference": "selector",
        "nonclaim": "This does not assign gameplay meaning to selector value 9 beyond its measured initial-cache role.",
        "blocker": "Runtime duration of the seed state is not measured.",
        "next": "Source-separated runtime trace of one CNetNPC construction and first selector refresh.",
    },
    {
        "id": "QML-IMG-002",
        "stage": "CREATION_POOL_ACQUIRE",
        "subject": "0x34-byte QuestIconBoard pool acquisition",
        "start": 0x0045C740,
        "end": 0x0045C84B,
        "offset_start": 0x0005BB40,
        "offset_end": 0x0005BC4B,
        "sha256": "4fa5650c70976b02eaf327df857c7a002de2b1583c3905abf7f210112aadf8a9",
        "status": "PROVEN_EXACT",
        "observation": (
            "The pool acquisition path removes an available entry or allocates "
            "0x34 bytes, invokes 0x0045B9E0 on both construction branches, marks "
            "the returned pool object active at +0x04, and updates pool counters."
        ),
        "layout": "allocation_size=0x34;constructor=0x0045B9E0;pool_head=0x0102D960;active_byte=+0x04",
        "support": "direct_E8_ctor_hits=0x0045C7A4,0x0045C822",
        "reference": "",
        "nonclaim": "This does not prove how many pool instances are alive at runtime.",
        "blocker": "Live pool occupancy is runtime-only.",
        "next": "DUMP-sourced instance census or client-observable allocation trace.",
    },
    {
        "id": "QML-IMG-003",
        "stage": "CREATION_CONSTRUCTOR",
        "subject": "QuestIconBoard derived constructor",
        "start": 0x0045B9E0,
        "end": 0x0045BA29,
        "offset_start": 0x0005ADE0,
        "offset_end": 0x0005AE29,
        "sha256": "14a7809766fbaa343ced9d11d7c3b3e24ad6133c64188094d43bb14d811c3703",
        "status": "PROVEN_EXACT",
        "observation": (
            "The derived constructor invokes base constructor 0x005BADE0, "
            "installs vtable 0x00F0DEE4, and initializes derived retained member "
            "+0x30 to null."
        ),
        "layout": "vtable=0x00F0DEE4;derived_retained_member=+0x30=null;base_ctor=0x005BADE0",
        "support": "base_ctor=0x005BADE0..0x005BAE19",
        "reference": "",
        "nonclaim": "The static constructor does not prove that model or scene resources load successfully.",
        "blocker": "Resource and scene outcomes are downstream.",
        "next": "Use the canonical resource resolver plus source-separated runtime evidence.",
    },
    {
        "id": "QML-IMG-004",
        "stage": "TYPE_AND_DISPATCH",
        "subject": "QuestIconBoard vtable lifecycle slots",
        "start": 0x00F0DEE4,
        "end": 0x00F0DF10,
        "offset_start": 0x00B0C2E4,
        "offset_end": 0x00B0C310,
        "sha256": "79a1fb8920895dc1003535e7de437efed33cd9b5fb60343087d28854e78628d6",
        "status": "PROVEN_EXACT",
        "observation": (
            "The 11-entry vtable binds deleting destructor +0x04 to 0x0045C4A0, "
            "model-init +0x14 to 0x00607C00, submission +0x18 to 0x005BB170, "
            "update dispatch +0x1C to 0x005BAC80, flag setter +0x20 to "
            "0x0045BA30, and dimension accessors +0x24/+0x28 to "
            "0x0045BA40/0x0045BA80."
        ),
        "layout": "vtable_slots=11;+04=dtor;+14=model_init;+18=submission;+1C=update_dispatch;+20=flag_setter;+24/+28=dimensions",
        "support": "",
        "reference": "selector",
        "nonclaim": "The project class label is a typed static label; this row does not claim RTTI recovery.",
        "blocker": "Final renderer semantics are beyond this vtable.",
        "next": "Client-observable render trace if pixel-level presentation is required.",
    },
    {
        "id": "QML-IMG-005",
        "stage": "ATTACH_AND_BIND",
        "subject": "CNetNPC ownership replacement and model-init dispatch",
        "start": 0x0045D430,
        "end": 0x0045D471,
        "offset_start": 0x0005C830,
        "offset_end": 0x0005C871,
        "sha256": "298c8c31efc2fb052c5be6c35b57b4bb71fd04d8e2d663aca847bace92ea2f29",
        "status": "PROVEN_EXACT",
        "observation": (
            "CNetNPC replaces +0x360 with the factory result using release-old "
            "and retain-new discipline, then calls the board vtable +0x14 method "
            "with the pinned model argument when the new board is non-null."
        ),
        "layout": "owner_slot=CNetNPC+0x360;release_old=0x0088D060;retain_new=0x0088D050;dispatch=vtable+0x14",
        "support": "direct_E8_pool_factory_hit=0x0045D42B",
        "reference": "selector",
        "nonclaim": "The model argument's resource-resolution and decode meaning is delegated, not re-derived here.",
        "blocker": "Static control flow does not prove successful runtime model construction.",
        "next": "Canonical resource-resolver artifact and client-observable bind evidence.",
    },
    {
        "id": "QML-IMG-006",
        "stage": "PER_NPC_UPDATE_ENTRY",
        "subject": "CNetNPC virtual update board gate",
        "start": 0x0045C500,
        "end": 0x0045C52C,
        "offset_start": 0x0005B900,
        "offset_end": 0x0005B92C,
        "sha256": "11d7f2a6cc9b38bcd175b7d5d4acaec1768c7148f85e4d9b38adcecbed331c62",
        "status": "PROVEN_EXACT",
        "observation": (
            "After the base update, the CNetNPC virtual update calls the board "
            "path only when owner slot +0x360 and board root +0x10 are both non-null."
        ),
        "layout": "entry=0x0045C500;owner_gate=+0x360!=null;root_gate=board+0x10!=null;callee=0x0045BB90",
        "support": "direct_E8_board_update_hit=0x0045C527",
        "reference": "",
        "nonclaim": "This is not the QuestNPCModule 1000 ms refresh timer; it is the typed CNetNPC update path.",
        "blocker": "Actual invocation frequency is not measured in IMAGE evidence.",
        "next": "Source-separated runtime call-frequency trace if timing is required.",
    },
    {
        "id": "QML-IMG-007",
        "stage": "VISIBILITY_GATE_AND_SPATIAL_UPDATE",
        "subject": "board-root bit gate and CNetNPC spatial forwarding",
        "start": 0x0045BB90,
        "end": 0x0045BC7A,
        "offset_start": 0x0005AF90,
        "offset_end": 0x0005B07A,
        "sha256": "743790a6cee4f19b9dfaa9f484d4a5cca403b2674c0b6fdf4be6b55e3f84786e",
        "status": "PROVEN_EXACT",
        "observation": (
            "The typed board path stops when the board or root is null or root "
            "+0x18 bit 0 is set.  Otherwise it computes squared distance from the "
            "CNetNPC position to the selected global position, forwards the root "
            "and distance to 0x0043D7B0, then dispatches board vtable +0x1C."
        ),
        "layout": "root=board+0x10;eligibility_gate=(root+0x18)&1==0;spatial_helper=0x0043D7B0;tail_dispatch=vtable+0x1C",
        "support": "direct_E8_spatial_helper_hit=0x0045BC62",
        "reference": "selector",
        "nonclaim": "Bit 0 is an update-eligibility gate here; this row does not rename it visible or hidden.",
        "blocker": "Pixel visibility and occlusion are not measured.",
        "next": "Client-observable frame evidence paired with root-state tracing.",
    },
    {
        "id": "QML-IMG-008",
        "stage": "ROOT_MANAGER_TRANSITION_CALLBACK",
        "subject": "CNetNPC vslot +0x58 board-root manager admission",
        "start": 0x0045CDB2,
        "end": 0x0045CDF2,
        "offset_start": 0x0005C1B2,
        "offset_end": 0x0005C1F2,
        "sha256": "2fcbd5cf8b7886228aa6bf36755789ba166f698c11b830a934480f7ea0a30c24",
        "status": "PROVEN_EFFECT_TRIGGER_OPEN",
        "observation": (
            "Within the typed CNetNPC vtable +0x58 callback, a non-null board "
            "root is passed to global manager method 0x00B0E9A0 when the manager "
            "chain exists, after which root +0x18 bit 0 is set."
        ),
        "layout": "typed_callback=CNetNPC_vtable+0x58;root=board+0x10;manager_call=0x00B0E9A0;post_effect=(root+0x18)|=1",
        "support": "manager_admission=0x00B0E9A0..0x00B0EAA9",
        "reference": "selector",
        "nonclaim": "The callback's engine-level scene or generation event name is not proven.",
        "blocker": "The callback trigger identity is opaque without symbols or runtime trace.",
        "next": "Instrumented callback trace across a scene or generation transition.",
    },
    {
        "id": "QML-IMG-009",
        "stage": "ROOT_MANAGER_ADMISSION",
        "subject": "global root-manager admission boundary",
        "start": 0x00B0E9A0,
        "end": 0x00B0EAA9,
        "offset_start": 0x0070DDA0,
        "offset_end": 0x0070DEA9,
        "sha256": "c4592d7a252b213f0cb1d4f16813158327d1681fb418173c329fbe2940f9b455",
        "status": "PROVEN_TO_CONTAINER_BOUNDARY",
        "observation": (
            "The manager rejects a null root, checks its +0x4C index, returns "
            "false for an already-present entry, otherwise calls insertion helper "
            "0x00B0E170 and then root-state helpers 0x008AC390 and 0x008AC5B0."
        ),
        "layout": "manager_index=+0x4C;insert_helper=0x00B0E170;post_helpers=0x008AC390,0x008AC5B0",
        "support": "",
        "reference": "",
        "nonclaim": "This does not prove final renderer registration or a player-visible frame.",
        "blocker": "Downstream renderer/GPU ownership is not traversed in this bounded lifecycle artifact.",
        "next": "Typed downstream renderer trace or client-observable frame evidence.",
    },
    {
        "id": "QML-IMG-010",
        "stage": "REMOVAL_FORWARDER",
        "subject": "board-root manager withdrawal forwarder",
        "start": 0x005BB150,
        "end": 0x005BB16C,
        "offset_start": 0x001BA550,
        "offset_end": 0x001BA56C,
        "sha256": "b180fe92a5592b8b39a34908a42c5c7ef9b7e58dc494b3047d26d63520e34d8e",
        "status": "PROVEN_EXACT",
        "observation": (
            "Given a non-null board root at +0x10, the base-board withdrawal "
            "forwarder passes that root to global manager method 0x00B0F030."
        ),
        "layout": "root=board+0x10;global_chain=0x01093198->+0x2C0->+0x0C;manager_call=0x00B0F030",
        "support": "direct_E8_manager_withdrawal_hit=0x005BB166",
        "reference": "",
        "nonclaim": "This row names the measured direction, not the engine's original symbol.",
        "blocker": "Whether every scene transition reaches this forwarder is not proven.",
        "next": "Runtime transition trace covering creation, scene change, and destruction.",
    },
    {
        "id": "QML-IMG-011",
        "stage": "ROOT_MANAGER_WITHDRAWAL",
        "subject": "global root-manager erase boundary",
        "start": 0x00B0F030,
        "end": 0x00B0F0B1,
        "offset_start": 0x0070E430,
        "offset_end": 0x0070E4B1,
        "sha256": "d2799c04f86419c0c6e391ee71c7e30c1b8d11e4d444b134bd3356999dd692cc",
        "status": "PROVEN_TO_CONTAINER_BOUNDARY",
        "observation": (
            "The manager retains the supplied root during the operation, passes "
            "it into +0x4C removal helper 0x00B0EC90, then balances the temporary "
            "reference before returning."
        ),
        "layout": "manager_index=+0x4C;removal_helper=0x00B0EC90;temporary_ref=balanced",
        "support": "",
        "reference": "",
        "nonclaim": "The static path does not prove when an on-screen image disappears.",
        "blocker": "Presentation timing is runtime-only.",
        "next": "Client-observable removal evidence synchronized to this call.",
    },
    {
        "id": "QML-IMG-012",
        "stage": "OWNER_DETACH_OR_TRANSFER",
        "subject": "CNetNPC teardown helper for +0x360",
        "start": 0x0045CEC0,
        "end": 0x0045CF57,
        "offset_start": 0x0005C2C0,
        "offset_end": 0x0005C357,
        "sha256": "d0c5b310d9a5750cfc10f651caf46105a3d0da16456256032fc812f4024eae5d",
        "status": "PROVEN_EXACT_BRANCH_EFFECTS",
        "observation": (
            "The owner teardown helper first withdraws a non-null board root. "
            "When the global mode check is false and a holder exists, it swaps the "
            "board reference into holder +0x38, clears the CNetNPC slot, and sends "
            "the holder to a manager callback; otherwise it releases and clears "
            "the CNetNPC slot."
        ),
        "layout": "owner_slot_ptr=argument;holder_member=+0x38;withdraw=0x005BB150;release=0x0088D060;clear=0",
        "support": "root_withdrawal=0x005BB150..0x005BB16C",
        "reference": "",
        "nonclaim": "The global mode and holder are not assigned scene-generation names.",
        "blocker": "The exact transition that selects transfer versus release is opaque.",
        "next": "Runtime branch trace with manager and holder identities.",
    },
    {
        "id": "QML-IMG-013",
        "stage": "OWNER_DESTRUCTION",
        "subject": "CNetNPC destructor ordering",
        "start": 0x0045CF60,
        "end": 0x0045CFF5,
        "offset_start": 0x0005C360,
        "offset_end": 0x0005C3F5,
        "sha256": "51485167a43478715b8b893fb7d711409300ea2d3eb93e95a96aa20b08cdbedc",
        "status": "PROVEN_EXACT",
        "observation": (
            "CNetNPC destruction invokes the +0x360 teardown helper before base "
            "destruction, then releases any residual +0x360 reference, tears down "
            "+0x338, and calls the CNetNPC base destructor."
        ),
        "layout": "teardown_helper=0x0045CEC0;residual_board_release=0x0088D060;base_dtor=0x00442E00",
        "support": "direct_E8_teardown_hit=0x0045CF9E",
        "reference": "",
        "nonclaim": "Destructor reachability for every runtime removal scenario is not proven.",
        "blocker": "Runtime lifecycle coverage is absent.",
        "next": "Trace explicit NPC removal, map leave, reconnect, and process shutdown separately.",
    },
    {
        "id": "QML-IMG-014",
        "stage": "BOARD_DERIVED_DESTRUCTION",
        "subject": "QuestIconBoard derived destructor",
        "start": 0x0045BAD0,
        "end": 0x0045BB32,
        "offset_start": 0x0005AED0,
        "offset_end": 0x0005AF32,
        "sha256": "1e9e87d04bf0e662ae433d93f35a89b70d207c762fc690617fb42684840454a2",
        "status": "PROVEN_EXACT",
        "observation": (
            "The derived destructor restores vtable 0x00F0DEE4, releases retained "
            "member +0x30 when non-null, and calls base destructor 0x005BAFE0."
        ),
        "layout": "derived_member=+0x30;release=0x0088D060;base_dtor=0x005BAFE0",
        "support": "",
        "reference": "",
        "nonclaim": "The identity of the +0x30 retained object is not assigned here.",
        "blocker": "No RTTI or runtime object identity is used for +0x30.",
        "next": "DUMP-sourced class identity, kept separate as source=DUMP.",
    },
    {
        "id": "QML-IMG-015",
        "stage": "BOARD_BASE_DESTRUCTION",
        "subject": "base-board owned-member teardown",
        "start": 0x005BAFE0,
        "end": 0x005BB146,
        "offset_start": 0x001BA3E0,
        "offset_end": 0x001BA546,
        "sha256": "0e4b9970c38d994640cdd8c113df5ed3017494eb330970e47b029e094a029493",
        "status": "PROVEN_EXACT",
        "observation": (
            "The base destructor releases and clears refcounted members +0x14, "
            "+0x10, +0x18, and +0x1C, invokes the virtual deleting destructor on "
            "+0x20 and clears it, then runs the lower base teardown."
        ),
        "layout": "ref_members=+0x10,+0x14,+0x18,+0x1C;owned_virtual_member=+0x20;lower_base=0x0088D280",
        "support": "",
        "reference": "",
        "nonclaim": "Member class names are not guessed from nearby strings.",
        "blocker": "Runtime class identities of retained members remain open.",
        "next": "DUMP RTTI map with source=DUMP if member identities are needed.",
    },
    {
        "id": "QML-IMG-016",
        "stage": "UPDATE_TO_SUBMISSION_DISPATCH",
        "subject": "one-shot base-board submission gate",
        "start": 0x005BAC80,
        "end": 0x005BAC9D,
        "offset_start": 0x001BA080,
        "offset_end": 0x001BA09D,
        "sha256": "520f5eb44d9ee85e2f4c51061ec59130459e125e2ea7c5394eb292e3bca10eab",
        "status": "PROVEN_EXACT",
        "observation": (
            "When byte +0x28 is non-zero, the base-board update dispatcher calls "
            "virtual +0x18 and then virtual +0x20 with false.  The QuestIconBoard "
            "vtable resolves these to 0x005BB170 and 0x0045BA30, so the flag is "
            "cleared after the gated submission call."
        ),
        "layout": "gate=board+0x28!=0;submit=vtable+0x18;clear=vtable+0x20(false)",
        "support": "QuestIconBoard_vtable=0x00F0DEE4..0x00F0DF10;submission=0x005BB170..0x005BB1C4",
        "reference": "",
        "nonclaim": "The original semantic name of byte +0x28 is not proven.",
        "blocker": "The complete producer census for setting +0x28 true is outside this bounded lifecycle lane.",
        "next": "Typed producer census or runtime write trace for board +0x28.",
    },
    {
        "id": "QML-IMG-017",
        "stage": "RENDER_SUBMISSION_CEILING",
        "subject": "inherited board submission boundary",
        "start": 0x005BB170,
        "end": 0x005BB1C4,
        "offset_start": 0x001BA570,
        "offset_end": 0x001BA5C4,
        "sha256": "ba3236aa8ec56e5a48896b70a1c6d5974ecad6224ed7832ca1aa02e8163f628b",
        "status": "PROVEN_TO_SUBMISSION_BOUNDARY",
        "observation": (
            "The inherited QuestIconBoard vtable +0x18 target reads position-like "
            "components through model member +0x20 vtable +0xB4, converts them to "
            "integers, and passes +0x20, +0x1C, the two integers, and flag 1 to "
            "global manager call 0x00A9E6C0."
        ),
        "layout": "model=board+0x20;context=board+0x1C;model_query=vtable+0xB4;manager_call=0x00A9E6C0",
        "support": "QuestIconBoard_vtable=0x00F0DEE4..0x00F0DF10;direct_E8_submission_hit=0x005BB1B9",
        "reference": "selector",
        "nonclaim": "This is the static submission ceiling; it does not prove final renderer/GPU work or visible pixels.",
        "blocker": "Downstream dynamic manager dispatch and client-observable presentation are unmeasured.",
        "next": "Source-separated render trace and screenshot/capture evidence without exporting proprietary bytes.",
    },
]


EXPECTED_VTABLE = [
    0x0045BAC0,
    0x0045C4A0,
    0x00401B20,
    0x009F17E0,
    0x0073D360,
    0x00607C00,
    0x005BB170,
    0x005BAC80,
    0x0045BA30,
    0x0045BA40,
    0x0045BA80,
]

EXPECTED_DIRECT_E8: dict[int, list[int]] = {
    0x0045C740: [0x0045D42B],
    0x0045B9E0: [0x0045C7A4, 0x0045C822],
    0x0045BB90: [0x0045C527],
    0x0045CEC0: [0x0045CF9E],
    0x00B0F030: [0x005BB166],
}


def fail(message: str) -> "NoReturn":  # type: ignore[name-defined]
    raise SystemExit("ERROR: " + message.encode("ascii", "backslashreplace").decode("ascii"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(payload.encode("ascii"))


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_pe(data: bytes) -> tuple[int, list[dict[str, int]]]:
    if len(data) < 0x100 or data[:2] != b"MZ":
        fail("input is not a valid PE image")
    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    if data[pe_offset : pe_offset + 4] != b"PE\x00\x00":
        fail("PE signature missing")
    coff = pe_offset + 4
    section_count = struct.unpack_from("<H", data, coff + 2)[0]
    optional_size = struct.unpack_from("<H", data, coff + 16)[0]
    optional = coff + 20
    if struct.unpack_from("<H", data, optional)[0] != 0x10B:
        fail("expected 32-bit PE optional header")
    image_base = struct.unpack_from("<I", data, optional + 28)[0]
    section_table = optional + optional_size
    sections: list[dict[str, int]] = []
    for index in range(section_count):
        cursor = section_table + index * 40
        virtual_size, virtual_address, raw_size, raw_offset = struct.unpack_from("<IIII", data, cursor + 8)
        characteristics = struct.unpack_from("<I", data, cursor + 36)[0]
        sections.append(
            {
                "virtual_size": virtual_size,
                "virtual_address": virtual_address,
                "raw_size": raw_size,
                "raw_offset": raw_offset,
                "characteristics": characteristics,
            }
        )
    return image_base, sections


def va_to_offset(va: int, image_base: int, sections: Iterable[dict[str, int]]) -> int:
    rva = va - image_base
    for section in sections:
        start = section["virtual_address"]
        width = max(section["virtual_size"], section["raw_size"])
        if start <= rva < start + width:
            delta = rva - start
            if delta >= section["raw_size"]:
                fail(f"VA 0x{va:08X} is not backed by file bytes")
            return section["raw_offset"] + delta
    fail(f"VA 0x{va:08X} is outside mapped sections")


def direct_e8_hits(data: bytes, image_base: int, sections: Iterable[dict[str, int]], target: int) -> list[int]:
    hits: list[int] = []
    for section in sections:
        if not section["characteristics"] & 0x20000000:
            continue
        raw_start = section["raw_offset"]
        raw_end = raw_start + section["raw_size"]
        cursor = raw_start
        while True:
            found = data.find(b"\xE8", cursor, raw_end)
            if found < 0 or found + 5 > raw_end:
                break
            call_va = image_base + section["virtual_address"] + found - raw_start
            relative = struct.unpack_from("<i", data, found + 1)[0]
            if call_va + 5 + relative == target:
                hits.append(call_va)
            cursor = found + 1
    return hits


def validate_image(path: Path) -> tuple[bytes, int, list[dict[str, int]]]:
    if not path.is_file():
        fail(f"image missing: {path}")
    data = path.read_bytes()
    if len(data) != IMAGE_SIZE:
        fail(f"image size mismatch: expected {IMAGE_SIZE}, got {len(data)}")
    digest = sha256_bytes(data)
    if digest != IMAGE_SHA256:
        fail(f"image SHA-256 mismatch: {digest}")
    image_base, sections = parse_pe(data)
    if image_base != 0x00400000:
        fail(f"unexpected image base: 0x{image_base:08X}")
    for definition in SPAN_DEFS:
        start_offset = va_to_offset(definition["start"], image_base, sections)
        end_offset = start_offset + definition["end"] - definition["start"]
        if start_offset != definition["offset_start"] or end_offset != definition["offset_end"]:
            fail(f"offset mismatch for {definition['id']}")
        span_digest = sha256_bytes(data[start_offset:end_offset])
        if span_digest != definition["sha256"]:
            fail(f"span hash mismatch for {definition['id']}: {span_digest}")
    vtable_offset = va_to_offset(0x00F0DEE4, image_base, sections)
    vtable = list(struct.unpack_from("<11I", data, vtable_offset))
    if vtable != EXPECTED_VTABLE:
        fail("QuestIconBoard vtable slot guard failed")
    cnetnpc_vtable_offset = va_to_offset(0x00F0DF58, image_base, sections)
    if struct.unpack_from("<I", data, cnetnpc_vtable_offset + 0x18)[0] != 0x0045C500:
        fail("CNetNPC update-slot guard failed")
    if struct.unpack_from("<I", data, cnetnpc_vtable_offset + 0x58)[0] != 0x0045CD80:
        fail("CNetNPC root-manager callback-slot guard failed")
    for target, expected_hits in EXPECTED_DIRECT_E8.items():
        actual_hits = direct_e8_hits(data, image_base, sections, target)
        if actual_hits != expected_hits:
            fail(
                f"raw executable-section E8 census mismatch for target 0x{target:08X}: "
                f"expected {[f'0x{x:08X}' for x in expected_hits]}, got {[f'0x{x:08X}' for x in actual_hits]}"
            )
    return data, image_base, sections


def validate_selector(path: Path) -> tuple[list[tuple[str, str]], str]:
    if not path.is_file():
        fail(f"mandatory selector artifact missing: {path}")
    raw = path.read_bytes()
    digest = sha256_bytes(raw)
    if digest != SELECTOR_SHA256:
        fail(f"selector artifact SHA-256 mismatch: {digest}")
    rows = read_tsv(path)
    if len(rows) != SELECTOR_ROW_COUNT:
        fail(f"selector row count mismatch: expected {SELECTOR_ROW_COUNT}, got {len(rows)}")
    pairs: list[tuple[str, str]] = []
    required_support = {
        "QuestIconBoard_attach": "90bab35b89efac61fa95c9ffa2af894a4fc439fdfae48bdc3ed75c516104ec5c",
        "CNetNPC_selector_setter": "f808c0d68b1a782d3441e118a25a94ee73e1f4aea37824b06fd2e2c6fb112bc5",
        "QuestNPCModule_refresh": "4008a0568145fd75ae18286dd1582ceabe8393b98fa4f7b78648827b68075cc2",
        "QuestNPCModule_timer": "f7af7da39992f2de9d62166cf403665be42b6308fa76790531b3228e292a0ead",
        "QuestIconBoard_model_init": "17ff775c9cd0c9fce6613a22b26992cc35182df11d22570f0e902db4654638ea",
    }
    for row in rows:
        if row.get("source") != "IMAGE" or row.get("image_sha256") != IMAGE_SHA256:
            fail("selector artifact contains a non-IMAGE or mismatched-image row")
        support = row.get("support_spans", "")
        for label, span_hash in required_support.items():
            if f"{label}=" not in support or f"@{span_hash}" not in support:
                fail(f"selector support reference missing or mistyped: {label}")
        selector_key = row.get("selector_key", "")
        evidence_key = row.get("evidence_key", "")
        if not re.fullmatch(r"[0-9a-f]{64}", selector_key) or not re.fullmatch(r"[0-9a-f]{64}", evidence_key):
            fail("selector artifact key format mismatch")
        pairs.append((selector_key, evidence_key))
    payload = "\n".join(f"{selector}\t{evidence}" for selector, evidence in pairs) + "\n"
    set_digest = sha256_bytes(payload.encode("ascii"))
    if set_digest != SELECTOR_REFERENCE_SET_SHA256:
        fail(f"selector reference-set SHA-256 mismatch: {set_digest}")
    return pairs, set_digest


def validate_ground_drop(path: Path) -> tuple[str, str]:
    if not path.is_file():
        fail(f"mandatory event-kind reuse reference missing: {path}")
    digest = sha256_bytes(path.read_bytes())
    if digest != GROUND_DROP_SHA256:
        fail(f"ground-drop reference SHA-256 mismatch: {digest}")
    matches = [row for row in read_tsv(path) if row.get("evidence_id") == GROUND_DROP_REFERENCE_ID]
    if len(matches) != 1:
        fail(f"expected exactly one {GROUND_DROP_REFERENCE_ID} row")
    row = matches[0]
    if row.get("source") != "IMAGE" or row.get("evidence_key") != GROUND_DROP_REFERENCE_KEY:
        fail(f"{GROUND_DROP_REFERENCE_ID} source/key guard failed")
    if "Event kind 0x0A is not assigned a gameplay name" not in row.get("nonclaim", ""):
        fail(f"{GROUND_DROP_REFERENCE_ID} nonclaim guard failed")
    return digest, row["evidence_key"]


def validate_event_census(path: Path) -> tuple[list[tuple[str, str]], str]:
    if not path.is_file():
        fail(f"mandatory event census missing: {path}")
    digest = sha256_bytes(path.read_bytes())
    if digest != EVENT_SHA256:
        fail(f"event census SHA-256 mismatch: {digest}")
    rows = read_tsv(path)
    by_key = {row.get("event_key", ""): row for row in rows}
    if len(by_key) != len(rows):
        fail("event census contains duplicate or empty event_key")
    pairs: list[tuple[str, str]] = []
    for event_key, expected_evidence_key in EVENT_REFERENCE_KEYS.items():
        row = by_key.get(event_key)
        if row is None:
            fail(f"event reference row missing: {event_key}")
        if row.get("source") != "IMAGE" or row.get("source_sha256") != IMAGE_SHA256:
            fail(f"event reference source guard failed: {event_key}")
        if row.get("artifact_pair_sha256") != EVENT_PAIR_SHA256:
            fail(f"event reference pair guard failed: {event_key}")
        if row.get("evidence_key") != expected_evidence_key:
            fail(f"event reference evidence key mismatch: {event_key}")
        pairs.append((event_key, expected_evidence_key))
    payload = "\n".join(f"{event}\t{evidence}" for event, evidence in pairs) + "\n"
    set_digest = sha256_bytes(payload.encode("ascii"))
    if set_digest != EVENT_REFERENCE_SET_SHA256:
        fail(f"event reference-set SHA-256 mismatch: {set_digest}")
    return pairs, set_digest


def validate_resource_resolver(tsv_path: Path, md_path: Path) -> tuple[str, str]:
    if not tsv_path.is_file() or not md_path.is_file():
        fail("mandatory resource resolver pair is missing")
    tsv_digest = sha256_bytes(tsv_path.read_bytes())
    md_digest = sha256_bytes(md_path.read_bytes())
    if tsv_digest != RESOURCE_SHA256:
        fail(f"resource resolver TSV SHA-256 mismatch: {tsv_digest}")
    if md_digest != RESOURCE_MD_SHA256:
        fail(f"resource resolver MD SHA-256 mismatch: {md_digest}")
    matches = [row for row in read_tsv(tsv_path) if row.get("resolver_key") == RESOURCE_ROUTE_KEY]
    if len(matches) != 1:
        fail("expected exactly one canonical IMAGE route-bound resolver row")
    row = matches[0]
    if row.get("source") != "IMAGE" or row.get("source_sha256") != IMAGE_SHA256:
        fail("resource resolver IMAGE source guard failed")
    if row.get("artifact_pair_sha256") != RESOURCE_PAIR_SHA256:
        fail("resource resolver pair guard failed")
    if row.get("semantic_status") != "BOUNDED_OPEN_RUNTIME":
        fail("resource resolver semantic-status guard failed")
    if row.get("measurement_label") != "COMPOSED_BOUND":
        fail("resource resolver measurement-label guard failed")
    if not row.get("method") or not row.get("control"):
        fail("resource resolver method/control guard failed")
    for field in ("runtime_open_status", "runtime_bind_status", "runtime_pixels_status"):
        if row.get(field) != "OPEN":
            fail(f"resource resolver {field} must remain OPEN")
    return tsv_digest, md_digest


def reference_fields(kind: str, selector_set_digest: str) -> tuple[str, str, str]:
    if kind == "selector":
        return (
            SELECTOR_NAME,
            SELECTOR_SHA256,
            f"all_{SELECTOR_ROW_COUNT}_selector_key_evidence_key_pairs@sha256={selector_set_digest}",
        )
    return "", "", ""


def build_rows(selector_set_digest: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for definition in SPAN_DEFS:
        reference_artifact, reference_sha256, reference_keys = reference_fields(
            definition["reference"], selector_set_digest
        )
        claim_material = {
            "id": definition["id"],
            "stage": definition["stage"],
            "subject": definition["subject"],
            "status": definition["status"],
            "observation": definition["observation"],
            "layout": definition["layout"],
            "nonclaim": definition["nonclaim"],
        }
        claim_sha = canonical_sha(claim_material)
        evidence_key = canonical_sha(
            {
                "source": "IMAGE",
                "source_sha256": IMAGE_SHA256,
                "span_start": f"0x{definition['start']:08X}",
                "span_end": f"0x{definition['end']:08X}",
                "span_sha256": definition["sha256"],
                "claim_sha256": claim_sha,
            }
        )
        rows.append(
            {
                "evidence_id": definition["id"],
                "row_kind": "NEW_IMAGE_EVIDENCE",
                "lifecycle_stage": definition["stage"],
                "subject": definition["subject"],
                "semantic_status": definition["status"],
                "exact_observation": definition["observation"],
                "value_or_layout": definition["layout"],
                "evidence_file": SOURCE_URI,
                "evidence_span_start": f"0x{definition['start']:08X}",
                "evidence_span_end": f"0x{definition['end']:08X}",
                "evidence_span_start_file_offset": f"0x{definition['offset_start']:08X}",
                "evidence_span_end_file_offset": f"0x{definition['offset_end']:08X}",
                "evidence_span_sha256": definition["sha256"],
                "support_spans": definition["support"],
                "evidence_key": evidence_key,
                "claim_sha256": claim_sha,
                "evidence_grade": "A",
                "measurement_label": "MEASURED",
                "method": "STATIC_IMAGE_HASHED_SPAN_AND_TYPED_CONTROL_FLOW",
                "control": "PINNED_IMAGE_SHA256;EXACT_SPAN_SHA256;RAW_EXECUTABLE_SECTION_E8_CENSUS_WHERE_DECLARED",
                "source": "IMAGE",
                "source_size": str(IMAGE_SIZE),
                "source_sha256": IMAGE_SHA256,
                "reference_artifact": reference_artifact,
                "reference_sha256": reference_sha256,
                "reference_keys": reference_keys,
                "nonclaim": definition["nonclaim"],
                "blocker": definition["blocker"],
                "required_next_evidence": definition["next"],
                "image_sha256": IMAGE_SHA256,
                "pair_id": PAIR_PLACEHOLDER,
            }
        )
    if len({row["evidence_id"] for row in rows}) != len(rows):
        fail("duplicate evidence_id")
    if len({row["evidence_key"] for row in rows}) != len(rows):
        fail("duplicate evidence_key")
    if any(row["source"] not in {"IMAGE", "DATA", "DUMP", "CAPTURE"} for row in rows):
        fail("invalid source label")
    if any(row["source"] != "IMAGE" for row in rows):
        fail("this bounded artifact must contain IMAGE rows only")
    return rows


def render_tsv(rows: list[dict[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def md_escape(value: str) -> str:
    return value.replace("|", "\\|")


def render_md(
    rows: list[dict[str, str]],
    selector_pairs: list[tuple[str, str]],
    selector_set_digest: str,
    event_pairs: list[tuple[str, str]],
    event_set_digest: str,
    resource_tsv_digest: str,
    resource_md_digest: str,
    ground_drop_digest: str,
    ground_drop_key: str,
) -> str:
    stage_lines = "\n".join(
        f"| {row['evidence_id']} | {md_escape(row['lifecycle_stage'])} | {md_escape(row['semantic_status'])} | "
        f"{row['evidence_span_start']}..{row['evidence_span_end']} | {row['evidence_span_sha256']} |"
        for row in rows
    )
    selector_lines = "\n".join(
        f"| {index} | `{selector}` | `{evidence}` |"
        for index, (selector, evidence) in enumerate(selector_pairs, 1)
    )
    event_lines = "\n".join(
        f"| `{event}` | `{evidence}` |"
        for event, evidence in event_pairs
    )
    evidence_keys_digest = sha256_bytes(
        ("\n".join(row["evidence_key"] for row in rows) + "\n").encode("ascii")
    )
    return f"""# PF Quest-Mark Lifecycle

Pair ID: `{PAIR_PLACEHOLDER}`

## Result

`[MEASURED][IMAGE]` This source-separated static artifact closes the measured `QuestIconBoard` mechanics from pooled wrapper creation through CNetNPC ownership, typed update gating, global root-manager admission/withdrawal boundaries, owner and board destruction, and the inherited submission call. It contains **{len(rows)} rows**, all `source=IMAGE`; no DUMP, CAPTURE, or DATA fact is mixed into any row.

The static render ceiling is exact but narrow: `QML-IMG-016` reaches the board's gated virtual submission, and `QML-IMG-017` reaches global manager call `0x00A9E6C0`. This does **not** prove final renderer/GPU execution or visible pixels.

## Lifecycle flow

1. `QML-IMG-001` seeds CNetNPC with no board and selector-cache byte 9.
2. `QML-IMG-002`/`003` acquire or allocate a 0x34-byte pool object and construct the typed board wrapper.
3. `QML-IMG-004` fixes the typed dispatch table. `QML-IMG-005` installs the refcounted board at CNetNPC +0x360 and invokes model init.
4. Selector cache/lookup, the 1000 ms QuestNPCModule refresh, and selector effects remain canonical in `{SELECTOR_NAME}` and are cited below rather than copied.
5. `QML-IMG-006`/`007` carry the per-CNetNPC update through null gates, root bit-0 eligibility, spatial forwarding, and board update dispatch.
6. `QML-IMG-008`/`009` reach the measured manager-admission boundary. The engine name of the callback that triggers it remains OPEN.
7. `QML-IMG-010`/`011` reach the measured manager-withdrawal boundary; `QML-IMG-012` then transfers or releases/clears the owner reference according to an opaque global-mode branch.
8. `QML-IMG-013`/`014`/`015` establish owner, derived-board, and base-board destruction ordering.
9. `QML-IMG-016`/`017` establish a byte-gated submission call and the final static boundary reached in this artifact.

## Requested-surface coverage

| Surface | Status | Authority |
|---|---|---|
| creation | CLOSED for static pool/constructor mechanics | `QML-IMG-002..004` |
| attach/bind | CLOSED to refcounted owner install and model-init dispatch; runtime bind result OPEN | `QML-IMG-005`; `{RESOURCE_NAME}` route key `{RESOURCE_ROUTE_KEY}` |
| cache/lookup | CLOSED by canonical reference, not duplicated | `{SELECTOR_NAME}` SHA-256 `{SELECTOR_SHA256}` |
| refresh/timer | CLOSED for the canonical static 1000 ms path by reference; runtime cadence OPEN | selector support keys `QuestNPCModule_refresh` and `QuestNPCModule_timer` |
| per-object update | CLOSED to board dispatch | `QML-IMG-006..007`, `QML-IMG-016` |
| visibility gate | CLOSED only as measured root +0x18 bit-0 update eligibility; pixel visibility OPEN | `QML-IMG-007..009` plus selector reference |
| removal/unregister | CLOSED to manager-container withdrawal and owner clear/transfer | `QML-IMG-010..013` |
| scene/generation transition | measured root-manager effects CLOSED; scene/generation trigger identity OPEN | `QML-IMG-008..012` |
| destruction | CLOSED for measured derived/base release order | `QML-IMG-013..015` |
| render submission | CLOSED to `0x00A9E6C0`; final renderer/GPU/pixels OPEN | `QML-IMG-016..017` |

## Evidence rows

| ID | Lifecycle stage | Status | VA span | Span SHA-256 |
|---|---|---|---|---|
{stage_lines}

Evidence-key ordered-set SHA-256: `{evidence_keys_digest}`.

## Canonical selector references

The selector artifact is mandatory and pinned at SHA-256 `{SELECTOR_SHA256}`. Its {len(selector_pairs)} ordered `selector_key`/`evidence_key` pairs hash to `{selector_set_digest}`. These keys are citations only; their selector conditions, event writer path, model-init body, and texture-routing claims are not republished as lifecycle evidence.

| # | selector_key | evidence_key |
|---:|---|---|
{selector_lines}

## Canonical resource-route reference

`{RESOURCE_NAME}` is pinned at SHA-256 `{resource_tsv_digest}`; its paired Markdown is pinned at SHA-256 `{resource_md_digest}`, pair `{RESOURCE_PAIR_SHA256}`. This lifecycle artifact cites only the canonical IMAGE route-bound `resolver_key` `{RESOURCE_ROUTE_KEY}`. Its status is preserved exactly as `BOUNDED_OPEN_RUNTIME`: runtime open, bind, and pixels all remain OPEN. No resource row, DATA control, decoded structure, or resolver claim is copied into this lifecycle table.

## Canonical event-lifetime references

`{EVENT_NAME}` is pinned at SHA-256 `{EVENT_SHA256}`, pair `{EVENT_PAIR_SHA256}`. The {len(event_pairs)} lifecycle-relevant `event_key`/`evidence_key` citations hash to `{event_set_digest}`. They cover the module-local synchronous stack-event lifetime, CNetNPC binding, direct registration and vtable binding, result overwrite/order, manager uniqueness/unregister, and numeric-kind reuse controls. Their event spans and claims are not copied into this lifecycle table.

| event_key | evidence_key |
|---|---|
{event_lines}

The event artifact's exact ceiling is preserved: the stack event lives across the synchronous dispatch and is destroyed on both measured branches; listener lifetime is proven only through manager add/remove. Runtime reentrancy and abnormal teardown remain OPEN.

## Event-kind reuse safety

Numeric event kind `0x0A` is **not** named globally as quest here. `{EVENT_NAME}` keys `QME-IMG-017`, `QME-IMG-018`, and `QME-IMG-020` preserve the separate general-channel/reuse control. `{GROUND_DROP_NAME}` SHA-256 `{ground_drop_digest}`, row `{GROUND_DROP_REFERENCE_ID}`, evidence key `{ground_drop_key}`, independently proves a separate `DropThingModule_Client` callback using the same numeric kind and explicitly declines a gameplay-wide name. Numeric reuse therefore does not join the DropThing and typed CNetNPC/QuestIconBoard lifecycles.

## Method and ceiling

- Image guard: size `{IMAGE_SIZE}` and SHA-256 `{IMAGE_SHA256}`.
- Every evidence span is mapped from VA through the PE section table and re-hashed.
- Typed dispatch is pinned by the 11 dwords at vtable `0x00F0DEE4`.
- Declared direct-call controls use a raw `E8 rel32` census over executable PE section file ranges. That census proves only exact direct-encoding hits for the named targets; it is not a whole-program absence proof and says nothing about indirect calls, tail jumps, imports, callbacks, or self-modifying/runtime code.
- No raw image, dump, or capture bytes are emitted.
- Publication takes an exclusive transient `O_EXCL` lock, stages and fsyncs both products, then replaces the pair while holding the lock. `--check` creates no lock, temporary file, output, or metadata sidecar; it rejects an active publisher, verifies stable size/mtime/content reads plus the shared pair ID, and compares exact regenerated bytes.

## Remaining blockers

- `[OPEN][IMAGE]` The original engine name and trigger semantics of the CNetNPC vtable +0x58 callback are not recovered.
- `[OPEN][IMAGE]` Root +0x18 bit 0 is proven as an update gate and written by measured paths, but this artifact does not rename it visible/hidden.
- `[OPEN][IMAGE]` The full producer census for setting base-board byte +0x28 true is outside this bounded lane.
- `[OPEN][IMAGE]` Resource open/decode/bind/pixel outcomes remain delegated to `{RESOURCE_NAME}` key `{RESOURCE_ROUTE_KEY}` and remain OPEN there.
- `[OPEN][CAPTURE]` Actual quest-mark presentation, transition timing, and removal timing require source-separated client-observable evidence.
- `[OPEN][IMAGE]` The final renderer/GPU path after `0x00A9E6C0` is not traversed.
- `[OPEN][CAPTURE]` Event reentrancy and abnormal listener teardown are not measured by the static event census.

## Delivery boundary

`pf_bridge/external` is outside the canonical `Pirate Force ServerProject` Git worktree. These files are local-only and untracked there; another clone or executor needs owner-approved packaging or ingest. This is not described as a Git-ignore policy.
"""


def insert_pair_id(tsv_template: str, md_template: str) -> tuple[bytes, bytes, str]:
    if PAIR_PLACEHOLDER not in tsv_template or PAIR_PLACEHOLDER not in md_template:
        fail("pair placeholder missing")
    pair_id = sha256_bytes(tsv_template.encode("utf-8") + b"\x00" + md_template.encode("utf-8"))
    tsv = tsv_template.replace(PAIR_PLACEHOLDER, pair_id).encode("utf-8")
    md = md_template.replace(PAIR_PLACEHOLDER, pair_id).encode("utf-8")
    return tsv, md, pair_id


@contextmanager
def exclusive_publish_lock(lock_path: Path) -> Iterable[None]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        fail(f"publisher lock exists: {lock_path.name}")
    try:
        with os.fdopen(fd, "w", encoding="ascii", newline="\n") as handle:
            handle.write(f"pid={os.getpid()}\n")
            handle.flush()
            os.fsync(handle.fileno())
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def publish_pair(outputs: Mapping[Path, bytes], ordered_paths: tuple[Path, Path], lock_path: Path) -> None:
    staged: dict[Path, Path] = {}
    with exclusive_publish_lock(lock_path):
        try:
            for path in ordered_paths:
                raw = outputs[path]
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
            for path in ordered_paths:
                os.replace(staged.pop(path), path)
        finally:
            for temp_path in staged.values():
                try:
                    temp_path.unlink()
                except FileNotFoundError:
                    pass


def stable_read_pair(tsv_path: Path, md_path: Path, lock_path: Path) -> tuple[bytes, bytes]:
    if lock_path.exists():
        fail("publication in progress")
    paths = (tsv_path, md_path)
    first_stats = {path: path.stat() for path in paths}
    first = {path: path.read_bytes() for path in paths}
    middle_stats = {path: path.stat() for path in paths}
    second = {path: path.read_bytes() for path in paths}
    final_stats = {path: path.stat() for path in paths}
    if lock_path.exists():
        fail("publication overlapped stable read")
    for path in paths:
        signatures = {
            (stat.st_size, stat.st_mtime_ns)
            for stat in (first_stats[path], middle_stats[path], final_stats[path])
        }
        if len(signatures) != 1 or first[path] != second[path]:
            fail(f"unstable published artifact during stable read: {path.name}")
    return first[tsv_path], first[md_path]


def input_signature(path: Path) -> tuple[int, int, str]:
    stat = path.stat()
    return stat.st_size, stat.st_mtime_ns, sha256_bytes(path.read_bytes())


def pair_ids(tsv: bytes, md: bytes) -> tuple[str, str]:
    tsv_match = re.findall(rb"\t([0-9a-f]{64})\n", tsv)
    md_match = re.search(rb"Pair ID: `([0-9a-f]{64})`", md)
    if not tsv_match or md_match is None:
        fail("pair ID missing from output")
    if len(set(tsv_match)) != 1:
        fail("TSV contains multiple pair IDs")
    return tsv_match[0].decode("ascii"), md_match.group(1).decode("ascii")


def resolve_default_image(script_dir: Path) -> Path:
    return script_dir.parents[1] / "GameClient" / IMAGE_NAME


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="ascii", errors="backslashreplace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="ascii", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, help="Path to the pinned GameClient image")
    parser.add_argument("--output-dir", type=Path, help="Directory for TSV and Markdown outputs")
    parser.add_argument("--check", action="store_true", help="Verify exact current outputs without writing")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    output_dir = (args.output_dir or script_dir).resolve()
    image_path = (args.image or resolve_default_image(script_dir)).resolve()
    selector_path = script_dir / SELECTOR_NAME
    event_path = script_dir / EVENT_NAME
    resource_path = script_dir / RESOURCE_NAME
    resource_md_path = script_dir / RESOURCE_MD_NAME
    ground_drop_path = script_dir / GROUND_DROP_NAME

    input_paths = (
        image_path,
        selector_path,
        event_path,
        resource_path,
        resource_md_path,
        ground_drop_path,
    )
    before_inputs = {path: input_signature(path) for path in input_paths}

    validate_image(image_path)
    selector_pairs, selector_set_digest = validate_selector(selector_path)
    event_pairs, event_set_digest = validate_event_census(event_path)
    resource_tsv_digest, resource_md_digest = validate_resource_resolver(
        resource_path, resource_md_path
    )
    ground_drop_digest, ground_drop_key = validate_ground_drop(ground_drop_path)
    rows = build_rows(selector_set_digest)
    tsv_template = render_tsv(rows)
    md_template = render_md(
        rows,
        selector_pairs,
        selector_set_digest,
        event_pairs,
        event_set_digest,
        resource_tsv_digest,
        resource_md_digest,
        ground_drop_digest,
        ground_drop_key,
    )
    expected_tsv, expected_md, pair_id = insert_pair_id(tsv_template, md_template)

    after_inputs = {path: input_signature(path) for path in input_paths}
    if before_inputs != after_inputs:
        fail("an input changed during derivation")

    tsv_path = output_dir / TSV_NAME
    md_path = output_dir / MD_NAME
    lock_path = output_dir / ".pf_rederive_quest_mark_lifecycle.lock"
    if args.check:
        if not tsv_path.is_file() or not md_path.is_file():
            fail("one or both output files are missing")
        actual_tsv, actual_md = stable_read_pair(tsv_path, md_path, lock_path)
        actual_tsv_pair, actual_md_pair = pair_ids(actual_tsv, actual_md)
        if actual_tsv_pair != actual_md_pair or actual_tsv_pair != pair_id:
            fail("mixed-generation or unexpected pair ID")
        if actual_tsv != expected_tsv:
            fail(f"{TSV_NAME} is stale or modified")
        if actual_md != expected_md:
            fail(f"{MD_NAME} is stale or modified")
        print(
            "CHECK PASS "
            f"rows={len(rows)} source_IMAGE={sum(row['source'] == 'IMAGE' for row in rows)} "
            f"pair_id={pair_id} tsv_sha256={sha256_bytes(actual_tsv)} "
            f"md_sha256={sha256_bytes(actual_md)}"
        )
        return 0

    publish_pair(
        {tsv_path: expected_tsv, md_path: expected_md},
        (tsv_path, md_path),
        lock_path,
    )
    actual_tsv, actual_md = stable_read_pair(tsv_path, md_path, lock_path)
    actual_tsv_pair, actual_md_pair = pair_ids(actual_tsv, actual_md)
    if actual_tsv != expected_tsv or actual_md != expected_md:
        fail("post-publication byte verification failed")
    if actual_tsv_pair != pair_id or actual_md_pair != pair_id:
        fail("post-publication pair verification failed")
    print(
        "WRITE PASS "
        f"rows={len(rows)} source_IMAGE={sum(row['source'] == 'IMAGE' for row in rows)} "
        f"pair_id={pair_id} tsv_sha256={sha256_bytes(actual_tsv)} "
        f"md_sha256={sha256_bytes(actual_md)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        raise SystemExit(1)
