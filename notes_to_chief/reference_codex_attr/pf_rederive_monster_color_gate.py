#!/usr/bin/env python3
"""Re-derive the RuntimeRes actor-entry to CNetNPC name-color gate.

The generator is intentionally additive.  It does not copy the fourteen rows in
PF_ATTR_NAME_COLOR_SELECTOR.tsv.  It verifies those rows as a pinned canonical
input and emits actor-entry bridge, same-instance registry/selector/nameboard
reachability, distinct-record boundary, padding-blocker, and DATA palette facts.

Only the Python standard library is used.  Console output is ASCII only.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import os
import struct
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
FONT_STYLE_PATH = (
    PF_ROOT / "GameClient" / "Data" / "GUI" / "Model" / "BigFontStyle.fsl"
)
SELECTOR_PATH = OUT_DIR / "PF_ATTR_NAME_COLOR_SELECTOR.tsv"
TSV_PATH = OUT_DIR / "PF_MONSTER_COLOR_GATE.tsv"
REPORT_PATH = OUT_DIR / "PF_MONSTER_COLOR_GATE.md"
PAIR_PATH = OUT_DIR / "PF_MONSTER_COLOR_GATE.pair.json"
LOCK_PATH = OUT_DIR / ".pf_rederive_monster_color_gate.lock"
PROJECT_ROOT = PF_ROOT / "Pirate Force ServerProject"
PROJECT_SNAPSHOT_COMMIT = "8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa"
PROJECT_SNAPSHOT_COMMIT_TIME = "2026-09-01T07:50:38Z"
SERVER_PATH = PROJECT_ROOT / "current" / "pf_login_game_server_v141.py"
FOUNDATION_ROOT = (
    PROJECT_ROOT / "src" / "pirateforce_foundation"
)
POPULATION_PATH = FOUNDATION_ROOT / "population.py"
FIELD_MOBS_PATH = FOUNDATION_ROOT / "field_mobs.py"
WORLD_POPULATION_PATH = FOUNDATION_ROOT / "world_population.py"
RUNTIME_PATH = FOUNDATION_ROOT / "runtime.py"

# These project files are not original-game evidence.  They are pinned only so
# the separate RECONSTRUCTED POLICY section cannot silently describe a moving
# replacement-server tree.  The TSV remains IMAGE/DATA-only.
PROJECT_SOURCE_PIN_ROWS = {
    "current/pf_login_game_server_v141.py": (382913, "2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22"),
    "src/pirateforce_foundation/population.py": (11593, "df7bedb387963b67c0e4438479b057e8023a2a63efa1016000994982de18d52f"),
    "src/pirateforce_foundation/field_mobs.py": (103451, "67c0467493f1bac36e374d24f86c5257001f1a57456b8ea77f739d7126008ecf"),
    "src/pirateforce_foundation/world_population.py": (58851, "83d05df46cd26ae6fa38790650e8b20d9cd74ae4e04c369603ef2c18649c276b"),
    "src/pirateforce_foundation/runtime.py": (472447, "d683299d86853896304cf92ea0e0a738d1dfb5a2647d68b32a3a1c179e31efe5"),
    "src/pirateforce_foundation/world_population_bg0002.py": (16070, "6cfb88b3907d3ccf5bd1d4bfa61046ed388dd8eee4d7b8606736181ccbf6d81e"),
    "src/pirateforce_foundation/world_population_bg0003.py": (16605, "6e1493196a56de95b20e38dc6b265d46e1709ac39f344c922748b373a4e93227"),
    "src/pirateforce_foundation/world_population_bg0004.py": (17276, "3c2f2c54eed1f3fa839b2cf8987229882fa7c719c4221823a7d194ae7183a13d"),
    "src/pirateforce_foundation/world_population_bg0005.py": (16840, "d8cab6c03a4a26712460d269cdabd5430920b9815a2f008f05d94208d752b1d0"),
    "src/pirateforce_foundation/world_population_bg0006.py": (16770, "26739708c69b3ad6fbeba47c307586d5fcaaa3f3ae647cd155974f0c2bbc72aa"),
    "src/pirateforce_foundation/world_population_bg0007.py": (16614, "b13ffaae75aa009a2f0f84bcb14a3d634c24bb8c848c954635b35e42b4ba911c"),
    "src/pirateforce_foundation/world_population_bg0008.py": (16425, "40ab39cbcb5ee41d3463af06cb5cc769205d9f2a0e24101d5e171a12192ab77f"),
    "src/pirateforce_foundation/world_population_bg0009.py": (16658, "3505923e3c8c42bda5beb4eaea81b2adb7bff76d588e58e2e0f5aca16cb8e4f1"),
    "src/pirateforce_foundation/world_population_bg0010.py": (18034, "1ef31e71cdff6e34a71dc6e4fb9d5df8e2191f78d67a1693304236c169bed2f6"),
    "src/pirateforce_foundation/world_population_bg0011.py": (17651, "73bb6dafd2accc83db077e600cb6c62468dc109fdf1a304269cb54a3af78aab5"),
    "src/pirateforce_foundation/world_population_bg0015.py": (23368, "2dcfe6f10779990d06b46b99d44912675ac2cd27d79625b9c880b794d119db7a"),
    "src/pirateforce_foundation/world_population_bg4001.py": (18038, "7827b52eaea764e0bfa60c0b53968d53b76d528a5daaa7e2d9deedb19ae7ba30"),
    "src/pirateforce_foundation/field_mob_hostile_bg0015.py": (12025, "7bb93cd07842bf5882a27ebe134df0247865ddc0b607fb3e4caf0b0434ff429b"),
    "src/pirateforce_foundation/mob_combat.py": (94868, "c552f817d663d3055fd57bc491d12676e9bc18444f6c38bb4c6a2249633ba432"),
    "src/pirateforce_foundation/mob_death.py": (152904, "7c0daee1e1532b18c2e2bdeb83fbc4bb65d91394c716409e599369f9f87f614e"),
    "src/pirateforce_foundation/world_face_frame.py": (13636, "91676e1246ad29fd949204f48ee770f20d1198a4cd24eaa3c1772387fa117341"),
    "src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py": (13020, "a12fa913ca1719bb9e636ca013289f80190de8cb43e7cf2e1b95b5e8b224746c"),
    "src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene14.py": (19803, "4afb657eeebc85b831a7a0efb41374448ff85115244263ce937e7248183aca08"),
    "src/pirateforce_foundation/mob_diag_multi_object.py": (28624, "a7ba4516207fa40b01cc2f9d5c706a14898ac43f793eef5c91b55df16a84de6f"),
    "src/pirateforce_foundation/hostile_hp_link_hypothesis.py": (113432, "61083bc352572de95c04d3716c2370640ddf6e7618b1df613c53fa9c4efa69b0"),
    "src/pirateforce_foundation/npc_hostile_hypothesis.py": (43882, "907065ac755fc12096429e94005f2fa461f43032816c01e9349ffa9f7e0fbb67"),
    "src/pirateforce_foundation/npc_hp_link_hypothesis.py": (96239, "dcf16989a169dc17476b9437238bc3eec131c8ff4d9b4486e3dea3b8aef718a7"),
    "src/pirateforce_foundation/remote_player_hypothesis.py": (73936, "6240850e80f980f0525d104730bd74fe9dc9022621c614b91a1ecd94fbf128e7"),
    "src/pirateforce_foundation/runtimeres_death_hypothesis.py": (63786, "bedb883cb86e0e826e692eb7e4ce693aa7075ec729f3bfde69090d7700c1581f"),
    "src/pirateforce_foundation/scenario.py": (6918, "f04a6985c5ec47fe929b1c0117e97437dcca91a274ded643c59a003b856da898"),
    "src/pirateforce_foundation/scene_object.py": (3267, "39532ceb30a9b02f22ef85b2f0140e4498daa5c561ae772c179a2f6aca5a6d1b"),
    "src/pirateforce_foundation/scene2_prison_exile_tables.py": (50901, "de3bec46727ac42ce62dbc9feb2c601d0ff19eaf47f5f5c4841e9158a9349652"),
    "src/pirateforce_foundation/world_bg0003_identity.py": (29707, "2b3b8360b3af9d43c75bc377e91510ec3c4a65df42108b071bd2ef32425d52ec"),
    "src/pirateforce_foundation/world_bg0004_identity.py": (36624, "e1d6a3fb5e9b256f66fe6e6afe9a2cdaf132be13062d8aa790a7635b87888015"),
    "src/pirateforce_foundation/world_bg0005_identity.py": (35845, "e002892551943b4db480ac15730028b65005ae9815834df09e352d88d2f06ccd"),
    "src/pirateforce_foundation/world_bg0006_identity.py": (29697, "ef15e14419a18f8701c79e37871eb64bf4938ea1802645ccf7ba5be716309dc8"),
    "src/pirateforce_foundation/world_bg0007_identity.py": (29627, "cae680de67e4b8dcc3d446fb5f420d9f29c2032f0f6fbb5911da12bdeb9e1025"),
    "src/pirateforce_foundation/world_bg0008_identity.py": (29193, "7595d1f1733d8dbdc83cedaf2c4519334d5387e5b0b9cab9b876aea44e0a73ad"),
    "src/pirateforce_foundation/world_bg0009_identity.py": (29728, "51fac307f011f175d047e7c082f8c3f339adadd1ef6805e73f72017df02a7620"),
    "src/pirateforce_foundation/world_bg0010_identity.py": (33301, "e121dfe67fae2d8b27d28d52a4fc3071c75602e7d856e466f5f292a56b06eac4"),
    "src/pirateforce_foundation/world_bg0011_identity.py": (29284, "e3f7a2a858fb10df55bfcd378d48e7d1546d45325383bdbf8d5874b13b14dd76"),
    "src/pirateforce_foundation/world_bg0015_identity.py": (40179, "8bdd75dbdcc979e07e528419d53b270972bada53e247fe9fd076832d729616d7"),
    "src/pirateforce_foundation/world_bg4001_identity.py": (28516, "55a5d387245b212a3aaa8ffcdc7f2fc81e64f4d15fd314dfa43ecf1839b9b297"),
    "src/pirateforce_foundation/lane_hooks/lane_a_scene_census.py": (27566, "ce1d1406c3974dc0c4b638993d9fae54c50d300f0fbc54a56c9122e8ffddc16c"),
    "src/pirateforce_foundation/world_population_handoff.py": (87210, "220ff05daadabf0f49f6852658b3e08b73862733e3d113961f0fdcd3587d8490"),
    "src/pirateforce_foundation/mob_scene_recompose.py": (74941, "b71b018b6b0bd3efe59e51896586ab497040accb4337b3cecdf161c48fc64083"),
    "src/pirateforce_foundation/diag_multi_object_wiring.py": (36922, "fc0ec460054f662887f972d62cfc791b2c6403f7e3ec0734409c7edbae85efc5"),
    "src/pirateforce_foundation/world_scene_travel.py": (52356, "c7134da3654760711c322276c288f18ce76f0f441a6ce8e0b78e7a8af922b6fc"),
    "src/pirateforce_foundation/field_mob_tables_bg0002.py": (11886, "17493653e5cc4f37bdfea35685de1a28fd34d134a13d713c708dfd8499d2d356"),
    "src/pirateforce_foundation/field_mob_ai_tables.py": (6528, "acd5a66f71c429f6ba90c288b79c02ac44a2052d9c20537e20b82d63594e2f12"),
    "scenarios/world_scene_registry_001.json": (190179, "89544e1833b00332dbb2cd9b89fb4a62f7cf796575199a820075f22e5e6a5447"),
}
PROJECT_SOURCE_PINS = {
    PROJECT_ROOT / Path(relative): pin
    for relative, pin in PROJECT_SOURCE_PIN_ROWS.items()
}

# Direct call-site census under src/pirateforce_foundation.  Line numbers are
# deliberately pinned: an added, removed or moved direct writer requires a new
# review rather than silently inheriting this report's conclusion.
# relative path, line, class, active route, identity origin, carrier span(s)
REACHABLE_WRITER_CENSUS = (
    ("world_population.py", 707, "SHIPPED", "runtime.py:8170", "population.py:46 P", "668-710"),
    ("world_population_bg0002.py", 199, "SHIPPED", "runtime.py:7691", "scene2_prison_exile_tables.py:411 P", "183-202"),
    ("world_population_bg0003.py", 203, "SHIPPED", "lane handoff", "world_bg0003_identity.py:346 P", "187-206"),
    ("world_population_bg0004.py", 201, "SHIPPED", "lane handoff", "world_bg0004_identity.py:388 P", "185-204"),
    ("world_population_bg0005.py", 205, "SHIPPED", "lane handoff", "world_bg0005_identity.py:401 P", "189-208"),
    ("world_population_bg0006.py", 204, "SHIPPED", "lane handoff", "world_bg0006_identity.py:327 P", "188-207"),
    ("world_population_bg0007.py", 204, "SHIPPED", "lane handoff", "world_bg0007_identity.py:347 P", "188-207"),
    ("world_population_bg0008.py", 199, "SHIPPED", "lane handoff", "world_bg0008_identity.py:332 P", "183-202"),
    ("world_population_bg0009.py", 204, "SHIPPED", "lane handoff", "world_bg0009_identity.py:349 P", "188-207"),
    ("world_population_bg0010.py", 219, "SHIPPED", "lane handoff", "world_bg0010_identity.py:359 P", "203-222"),
    ("world_population_bg0011.py", 219, "SHIPPED", "lane handoff", "world_bg0011_identity.py:357 P", "203-222"),
    ("world_population_bg0015.py", 289, "SHIPPED", "lane handoff", "world_bg0015_identity.py:461 P", "273-292"),
    ("world_population_bg4001.py", 224, "SHIPPED", "lane handoff", "world_bg4001_identity.py:365 P", "208-227"),
    ("field_mobs.py", 1708, "SHIPPED", "hostile entry users", "field_mobs.py:321 P", "1617-1625;1703-1711"),
    ("mob_combat.py", 1323, "SHIPPED", "runtime.py:4228/4356", "field_mobs.py:321 P", "1311-1324"),
    ("mob_death.py", 1622, "SHIPPED", "runtime.py:4517/4654/4664", "field_mobs.py:321 P", "1373-1375;1612-1623"),
    ("world_face_frame.py", 213, "SHIPPED", "runtime.py:7271", "world_face_frame.py:197 P", "197-213"),
    ("lane_hooks/lane_a_choose_npc_scene14.py", 333, "SHIPPED", "runtime.py:7157", "Bg0015Placement/FieldMob P", "309-335"),
    ("mob_diag_multi_object.py", 464, "OPERATOR_CONDITIONAL_DIAGNOSTIC", "runtime.py:8366", "FieldMob P; D3=0x432D", "451-468"),
)

# Literal make_remote_actor_entry calls which are intentionally outside the
# 19-site flagless/reachable census.
EXCLUDED_WRITER_CENSUS = (
    ("field_mob_hostile_bg0015.py", 205, "proof/helper composer"),
    ("hostile_hp_link_hypothesis.py", 1260, "hypothesis"),
    ("npc_hostile_hypothesis.py", 520, "hypothesis"),
    ("npc_hp_link_hypothesis.py", 1085, "hypothesis"),
    ("population.py", 224, "explicit population scenario"),
    ("population.py", 287, "explicit population scenario"),
    ("remote_player_hypothesis.py", 876, "hypothesis with variable actor type"),
    ("runtimeres_death_hypothesis.py", 729, "hypothesis"),
    ("scenario.py", 121, "explicit scenario"),
    ("scene_object.py", 34, "explicit scene-load scenario"),
    (
        "lane_hooks/lane_a_choose_npc_scene1.py",
        238,
        "safety-net responder explicitly gated by production_allowed=False",
    ),
)

FORMULA_ANCHORS = (
    ("population.py", 46),
    ("field_mobs.py", 321),
    ("scene2_prison_exile_tables.py", 411),
    ("world_bg0003_identity.py", 346),
    ("world_bg0004_identity.py", 388),
    ("world_bg0005_identity.py", 401),
    ("world_bg0006_identity.py", 327),
    ("world_bg0007_identity.py", 347),
    ("world_bg0008_identity.py", 332),
    ("world_bg0009_identity.py", 349),
    ("world_bg0010_identity.py", 359),
    ("world_bg0011_identity.py", 357),
    ("world_bg0015_identity.py", 461),
    ("world_bg4001_identity.py", 365),
)

IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
FONT_STYLE_SIZE = 28_144
FONT_STYLE_SHA256 = (
    "77798599c203d36e11282633d4a91ac098b0e1e03aa2482fede6fcfca161fc10"
)
SELECTOR_ROW_COUNT = 14
SELECTOR_SHA256 = (
    "d15864a21a7a124a23f6dffad174a55d376045a25a04814bbe6dc5f5632af82d"
)

IMAGE_SOURCE = "PF_ROOT://GameClient/GameClient.local.bin"
FONT_STYLE_SOURCE = "PF_ROOT://GameClient/Data/GUI/Model/BigFontStyle.fsl"

# Name, VA, VirtualSize, PointerToRawData, SizeOfRawData. These are all six
# measured PE32 section-table entries. A raw-byte census scans only the
# file-backed portion min(VirtualSize, SizeOfRawData), excluding file-alignment
# padding and the virtual zero-fill tail.
SECTIONS = (
    (".text", 0x00401000, 0x00838A2C, 0x00000400, 0x00838C00),
    (".code", 0x00C3A000, 0x000002E1, 0x00839000, 0x00000400),
    (".rdata", 0x00C3B000, 0x003DE38E, 0x00839400, 0x003DE400),
    (".data", 0x0101A000, 0x00081F70, 0x00C17800, 0x00011E00),
    (".rsrc", 0x0109C000, 0x00058998, 0x00C29600, 0x00058A00),
    (".reloc", 0x010F5000, 0x001915F0, 0x00C82000, 0x00191600),
)
IMAGE_BASE = 0x00400000

SPANS: dict[str, tuple[int, int, str]] = {
    "CreateActorDataEx_rtti": (
        0x0101F4E0,
        0x0101F500,
        "7534a38ab259b419c96ff58036d2fd904026ba15088184992c8f745002e6eddb",
    ),
    "CNetNPC_rtti": (
        0x0101B138,
        0x0101B158,
        "5a3e0eda74f052b92a3e6852628d533170e9b7cd68b4b4741ea217232871332a",
    ),
    "CNetNPC_type_node_ctor": (
        0x0040B9D0,
        0x0040BA55,
        "28e9ff89b3382dee547e683053b532aee70a4c4a43d2fda6ab4e04af2e9cfccf",
    ),
    "CNetNPC_type_node_anchor": (
        0x00BCEEF0,
        0x00BCEF06,
        "4ba953befb859cef1e863e3767bacd7def1df7e7120e621dc1fb70804855779b",
    ),
    "CNetNPC_vtable_prefix": (
        0x00F0DF58,
        0x00F0DF70,
        "6ed88211dbd508b3f83528d8793cff034ca9785c60eb59b1dc7a37e5e7562864",
    ),
    "CNetNPC_vtable_core": (
        0x00F0DF58,
        0x00F0DFA0,
        "cadaff2c7870f3dba10ff668dba9950510dc35a6a7707c02c2d44ca394b552b1",
    ),
    "CNetNPC_copy_full": (
        0x0045D200,
        0x0045D485,
        "f3859d6de337bf53fbcdd31e0d0620dbecf573c89941eafc6072134e37eeddd5",
    ),
    "bridge_copy_notify": (
        0x0045D223,
        0x0045D24F,
        "5be4e2292962fb4a2fab2b948f27f29bdc6724227e8f36f041b0b47b58641952",
    ),
    "actor_entry_codec_prefix": (
        0x005E21D0,
        0x005E23B5,
        "44efb796eb00d2fcc6b07783dd101d172b8a2a230f85c490611cc46aa3a8d067",
    ),
    "actor_entry_qword_write": (
        0x005E2232,
        0x005E2241,
        "c5b029e73de2771155c1ed667e4e4146f3814c0c19e890ef67d56cccc3d6bd82",
    ),
    "actor_entry_qword_read": (
        0x005E2301,
        0x005E231B,
        "141fb4a23a7a047b7c843b3f3a28f80e34317d589b78cc0123c0a8fc98105ba1",
    ),
    "runtime_res_handler": (
        0x005E4060,
        0x005E41CD,
        "85ff71ffceff5345f94facc9b7fa1c39c8efd2e429248d112cdba578d3df944e",
    ),
    "actor_reconcile": (
        0x00446F30,
        0x004470E5,
        "c47bc46a06d6ffe95bee17b572f9ccb7e03442cdd27f04807c1161c03642d880",
    ),
    "reconcile_identity_factory": (
        0x00446F7D,
        0x00446FA8,
        "035bbcee2d2b435afe3ad9b615740505b9b11d417afdda2f102ba6b7c6e6bc51",
    ),
    "actor_factory": (
        0x00446990,
        0x00446B2C,
        "5f68239f8661419da2ea9bea4e4a2cb9bcdcaa37fe6e4cd53b701116aeeb697d",
    ),
    "singleton_getter": (
        0x00402A20,
        0x00402A87,
        "5823a612986173266ba33447188d218b81c3267341ad708020bba0873fc07022",
    ),
    "manager_tick_callsite": (
        0x0040618F,
        0x004061A2,
        "5a5bd87a3e7ac4c92b15ba3bd53e8c08d644f02c0b6c3a08336ad06abca19b83",
    ),
    "factory_register_path": (
        0x00446A92,
        0x00446AAD,
        "f0ac76309c6253d77451cafef5ce6d49ec41b62ba557e6a2d29dd64b913b5e0d",
    ),
    "registry_insert": (
        0x00446090,
        0x00446167,
        "29363c8a004ff33f261bd245b90b13451b0775b69671c233555295c7312526b9",
    ),
    "registry_tree_insert": (
        0x005FC970,
        0x005FCA61,
        "c97047a3030806658ac26a4bf9569114ebbd63ff3da2b3c34d121c088b56b1a3",
    ),
    "registry_tree_emplace": (
        0x005FC720,
        0x005FC910,
        "eca55f1ac2c3d6b7c248b15a01163bc677c5bb043c29001ee550ca33bd16bc74",
    ),
    "registry_node_copy": (
        0x006F40D0,
        0x006F416A,
        "033e7517eb14fbb1d6f9baf21c0b5b8149b578ab3c1207d0a33fb6e17ecea2a1",
    ),
    "manager_tick_iteration": (
        0x00445480,
        0x0044551A,
        "d360a258a7311af7df247f785940755d62ffb0724d37c4703967a45f3ede1d41",
    ),
    "actor_update_selector_call": (
        0x00444400,
        0x004446E9,
        "5e250c409a77ebf70e71cb6f83b9ee01cbc71b3ab355f34a8c22153a75074a5f",
    ),
    "factory_entry_to_init": (
        0x00446A92,
        0x00446AB7,
        "91f895eb32baec3ded957be23738ce3005674057d331818161b6b74f17face3f",
    ),
    "CNetNPC_vtable_through_nameboard": (
        0x00F0DF58,
        0x00F0DFD8,
        "9305c765da3e4af1a3e7082d6ad49aa49741bd2115f66e8119387890a452319e",
    ),
    "CNetNPC_nameboard_create": (
        0x0045C560,
        0x0045C613,
        "cdbc017c51623beb9d8a283ed855daded612f7aaa99a000ed042bbbe88f2a432",
    ),
    "CNetNPC_selector_readiness": (
        0x0045C500,
        0x0045C559,
        "c9a7b330450cd605065f7eabe2bb1fb7eaee6be496192e27be340b104434d768",
    ),
    "NPC_nameboard_controller_ctor_prefix": (
        0x005BB3A0,
        0x005BB440,
        "6c4c3a20c444d0b1d11a514e04b8e722cae66d5e53fb31dd47475ce4f7098885",
    ),
    "NPC_nameboard_backpointer": (
        0x005BABC0,
        0x005BABCE,
        "43e5a91a24711c3d52bab4281496eacdf431781a6f3caa8d42e47eea7d208099",
    ),
    "NPC_nameboard_vtable": (
        0x00F2CD48,
        0x00F2CD88,
        "a1deb3b7ea4894b6549a826f1a297732b96d6be324f76a68360139676ba1b278",
    ),
    "NPC_nameboard_bind_label": (
        0x005BE6C0,
        0x005BE763,
        "5ff40efc33482a3fbe65610cd8ab75587bd5f1d42233178446f848954cd6124c",
    ),
    "NPC_controller_style_store": (
        0x009F1A70,
        0x009F1A7A,
        "6d731f768f8834c3595c479205dc6991ea8b4b940958f6be330f60aa9373eef1",
    ),
    "NPC_LABEL_NAME_style_apply": (
        0x005BDA47,
        0x005BDA95,
        "f9e3b664c61f6350eae791d53192f3ba5df3bd3f627e0684696416865bc5a837",
    ),
    "CNetNPC_model_callback": (
        0x0045CD80,
        0x0045CEBE,
        "65738c3af3cbfadb8f870bf2ff93e9b64354bb88f1e6394d107e0bf15e7f8b9c",
    ),
    "common_model_callback": (
        0x00444730,
        0x0044497B,
        "bff91e77c4570c959170e89cd65d96b175eb6a1728b26ac465bdc14da04f5a33",
    ),
    "CNetNPC_init_full": (
        0x0045D200,
        0x0045D485,
        "f3859d6de337bf53fbcdd31e0d0620dbecf573c89941eafc6072134e37eeddd5",
    ),
    "common_actor_update": (
        0x00443480,
        0x004437BD,
        "2a98965ec11ec731ae76dc63fa3c3d2adc5cd9528328e0cad37bd2f3be008c2f",
    ),
    "registry_state_sweep": (
        0x004462F0,
        0x004463C3,
        "3d56fcd9cd7299381761dfea58aff0b8b57cd570e6a30d908faccd19fe79a648",
    ),
    "registry_queued_erase": (
        0x004463D0,
        0x00446517,
        "7b77c2af7329311d9d17b5e18c34a7e1729e1318677fb714e56f3e2f2c9f52a9",
    ),
    "manager_frame_update": (
        0x00446750,
        0x0044680B,
        "35a15297378ef5c7f22927b40fbaf0f59b8268e98659521fa3eb05163045b408",
    ),
    "registry_full_clear": (
        0x00446810,
        0x0044687D,
        "94e852c1a4cd351a19863233b17924cafba94c17ec6133f75b23c37753927e4b",
    ),
    "NPC_nameboard_update": (
        0x005BD8E0,
        0x005BDF20,
        "e5a09bce53d19c44bed8679dd2437a953bdee14d226dafe8133848240b523c2c",
    ),
    "UILabel_rtti": (
        0x0101ED3C,
        0x0101ED58,
        "6f03306c4c274e3a4155a1e1c63f4cde4a6c7d6c8bf900fa5280528f39740570",
    ),
    "UILabel_reflection_ctor": (
        0x0041E720,
        0x0041E7A5,
        "67b220740ad171558bc38a90466fe15cca55e324d6c74dde51570007b478249d",
    ),
    "UILabel_type_token_init": (
        0x00C1ACE0,
        0x00C1AD17,
        "9b1768db0bafbb78337fccfe1d44b801843c96d55e27c1258c305a623babaf98",
    ),
    "UILabel_type_token_getter": (
        0x00AA7010,
        0x00AA7016,
        "92d1fa475468027dc55276e1c42ec29e4d1c46407b751c5af4322596640f29b9",
    ),
    "UILabel_pool_ctor_1": (
        0x00A9C610,
        0x00A9C744,
        "0c261e7a59b17453cbd0f250697eab882b4b43b7aeff3961b0a98635162799ca",
    ),
    "UILabel_pool_ctor_2": (
        0x00A9C750,
        0x00A9C884,
        "a635b7213a036fa159952410e1c5e2302802aa9746a780168831685543735f9c",
    ),
    "UILabel_vtable_style_window": (
        0x00F89898,
        0x00F898A8,
        "58701c0775e353cac88fd019be2bfb31c6bb62b4d4e4070410397538ac950ce7",
    ),
    "UILabel_vtable_draw_window": (
        0x00F89794,
        0x00F897A0,
        "4539bf1dd66e22aaea3cf62a05e439f84d4cd4813dd1b0c511c04a66dd4031a1",
    ),
    "UILabel_vtable_2_style_window": (
        0x00F89AE0,
        0x00F89AF0,
        "58701c0775e353cac88fd019be2bfb31c6bb62b4d4e4070410397538ac950ce7",
    ),
    "UILabel_vtable_2_draw_window": (
        0x00F899DC,
        0x00F899E8,
        "4539bf1dd66e22aaea3cf62a05e439f84d4cd4813dd1b0c511c04a66dd4031a1",
    ),
    "UILabel_FontStyleID_parser": (
        0x00AA488F,
        0x00AA4929,
        "a1f7e93fbd3fd7854a3d7a61242fe3e6c529f71302d90fe0043c34cb541c9c7f",
    ),
    "UILabel_style_setter": (
        0x00AA37D0,
        0x00AA3803,
        "5e601c36a7b2c8fcbcaf78352fd95801efacc226a84e7aa21acb901dd5bb184f",
    ),
    "UIFontStyle_lookup": (
        0x00A9F590,
        0x00A9F632,
        "acd17503b54d0a52e93b64fa876cfefd423974f0ba9101e7d95fdf5c1939c221",
    ),
    "UILabel_style_apply": (
        0x00AA6EF0,
        0x00AA6FB1,
        "a6b026c15ee279d73214df730782e02d41846e20cc556a2a27b93728520459e4",
    ),
    "UIText_component_config": (
        0x00A8ACF0,
        0x00A8AD6A,
        "f44e7eb6c3346449b1b4ef669039c8ac16e1323fe353859bcee7fc7d15cda86f",
    ),
    "UILabel_draw": (
        0x00AA71A0,
        0x00AA71CF,
        "849374acce7ce45d247f27da82424d48becb662d47ea3cb3c2a73d5bf6fa82a6",
    ),
    "UIText_component_render": (
        0x00A8AF50,
        0x00A8B2F2,
        "cd117d2b54142d869dc452b62e2c1a04faa15123560b681d05643fa460a4f559",
    ),
    "record_ctor": (
        0x005DF130,
        0x005DF20B,
        "0839aee52f8fbc1df274a6a95941c809e10ea8a602495a0460851e460c5d4265",
    ),
    "record_codec": (
        0x005DFF60,
        0x005E01C6,
        "de9de2a04f4ac3ec8e6c07550336eea2be18954143c5c0de1823a4a2171e3f8a",
    ),
    "dbattribute_identity_codec": (
        0x00467790,
        0x004677E6,
        "f95dd971c9d227c509e5537eaacec944d7b502649ef0248d4581c16f25709119",
    ),
    "basicattr_codec_prefix": (
        0x004656F0,
        0x00465716,
        "dcaae3e1105d712442c3018237158b591b86d36d103b7c1f6129103cb735f037",
    ),
    "allocator_thunks": (
        0x0088D020,
        0x0088D035,
        "cb0cb67d4c1da3d3b8afd9938976ebbb1ba86c9c0725fe5a459cbe52798361fb",
    ),
    "selector_full": (
        0x00443F50,
        0x004443C5,
        "ee845ee6ef6337ea41ae57a5a4df8af5a8a8ac00e458ea1ce3e587aff1f9cdf9",
    ),
    "signed_gate": (
        0x00443FFB,
        0x00444017,
        "f74eb23ff300cc9632fda77748e493bcfe20da994003c99a3ce9506107e37c69",
    ),
    "typed_color_tail": (
        0x0044421C,
        0x0044427F,
        "49b926d10639fdcba5e5c7a5d9e2df3905624fc8004fcb7f4d6a2a8ece4b134f",
    ),
    "death_predicate": (
        0x0043BD70,
        0x0043BD9D,
        "1df3c62b4bbe0aab1ebf1404320a7b2466ef20390db060e67ba183a1178127aa",
    ),
    "field18_rebuild": (
        0x004B362C,
        0x004B3769,
        "312352c08f0d7384e4ede179e50270f4e1fd2ca8f468ba3827c94b011bdaf906",
    ),
    "outbound_fields": (
        0x004B45CB,
        0x004B46C3,
        "457e522d2348aa42ce38cb5d69d286e70ab99d426dcb02d780f6b2efa563001d",
    ),
    "voice_producer": (
        0x004B3E10,
        0x004B3EC1,
        "0be319eb6f954edee1b6566160782e8498be256bf393e5ebb1ffce9a378f5183",
    ),
    "sin_producer": (
        0x004C2D77,
        0x004C2DF9,
        "f43f65bab8ea984420afdf329809a396e8ac58c090afa67884720fd6c4bb5fa0",
    ),
    "class_producer": (
        0x004BEA45,
        0x004BEA98,
        "57b62395d96d39cef44ac3009db58d52f17e3d201ff8639dbec976af738c626b",
    ),
    "CMyActor_ctor": (
        0x00464BE0,
        0x00464E38,
        "c588dfb9eadcecda1c9ff53daeb652a5b49914ca31f78e34ba56e24074866476",
    ),
    "CMyActor_codec": (
        0x00466230,
        0x00466C79,
        "f9ea39f3a6bc80e6d29d4aae3efa79c1d5ff855d70109319578cba86d5f9aabc",
    ),
    "CMyActor_99_setter": (
        0x004AE350,
        0x004AE374,
        "b73b7794187c8f5ceac298a47c37f5dfec10f6874f29c87712943fdc3f00d772",
    ),
    "CMyActor_8C_setter": (
        0x004AE380,
        0x004AE3A4,
        "c9c327249e01eab03bb83cbb84c160f1c70fd75ff5556935b0d25c44a873c9a2",
    ),
    "CMyActor_9A_setter": (
        0x004AE470,
        0x004AE494,
        "304cfb380d237ba7212e1e2540f4f3ff4f074e5ea2bfa11a9a653d1cec45b01d",
    ),
    "sin_ui_handler": (
        0x00503F60,
        0x005041A0,
        "c9a3f851aca2465c1b28a66b9c1f1273c51662cc99b6e3344f484cff5e33c8b3",
    ),
    "class_package_builder": (
        0x004BC580,
        0x004BCB4E,
        "4c4f120b7eecc549dcefe42011c85e531cac48f4168d0181d65695ce3956510e",
    ),
    "common_actor_ctor": (
        0x00443180,
        0x00443450,
        "274a44e8b1ac932c548cbe10b9144696e988d9b1e8eb9c640322e2fe80f10a31",
    ),
    "hit_bit_writer": (
        0x00750896,
        0x007508D7,
        "f5542fcf64ed9b84d74a30f2688c3b4641bedbf553674455b3d20ad76e605cf4",
    ),
    "missile_bit_writer": (
        0x007511A6,
        0x007511E7,
        "ebf888481cf1d605f5d7819dd93f783b0b1d47b2401ae90fc25c728a7ff738da",
    ),
    "bit_selector": (
        0x00444238,
        0x00444270,
        "ed634e6768954ffd17c9886a39ae092326e5b802847b278a87d6a0b18664b035",
    ),
    "ai_offensive": (
        0x0045C160,
        0x0045C1CB,
        "df448a78deaee5e0aa2535bfbb3585ec098ff5f952cf2fc98f79e195d62a363e",
    ),
    "style_startup_required_call": (
        0x0040A2E7,
        0x0040A2F6,
        "b761d6d7cb8ecaa0c82d121355249fb52259a441219024ab37570899959c5f34",
    ),
    "BigFontStyle_startup_call": (
        0x0040867A,
        0x004086EB,
        "a2b196468a90351f66fbbe95aef1727e96689ad3e429eca62e2cc62fa17a76a0",
    ),
    "UIFontStyle_registry_loader": (
        0x00A9F860,
        0x00A9FA74,
        "8f9704e5a4c1f0681375d79ac5342f1da5910ecc1e229e7860f78895fe1e4c24",
    ),
    "UIFontStyle_property_parser": (
        0x00A9DAE0,
        0x00A9DD9B,
        "5f974da52ed482920db7a92285d6e61e6a40594d864a6d659791054db46525ef",
    ),
    "rgba_u8_normalized_parser": (
        0x0053F5E0,
        0x0053F7AC,
        "b9e671dce7a39a3e746142e78e94b064bab287e3cdb9be5771b23fa958185809",
    ),
    "rgba_property_wrapper": (
        0x0053F7B0,
        0x0053F7E8,
        "0551bb9c71a1c1ffceeba6b28b221e734a0bfdc050e86ff8563f12bdec851c83",
    ),
    "FontColor_literal": (
        0x00F23608,
        0x00F2361C,
        "145b1c7d22b6ba179c351ee5cd560a961c86bdbcedfe45561feaf6462e499f55",
    ),
    "OutlineEffectColor_literal": (
        0x00F89EF0,
        0x00F89F16,
        "72e5ddf4d54d1a6549ef93e5a22e09dd920c195d1fe8ec0c361900f6cef7ee97",
    ),
    "FontStyleID_literal": (
        0x00F8A4DC,
        0x00F8A4F4,
        "e10133c28cc34408e4cc4a66eacbceb47022e958b4da940c75e20384fad67c1a",
    ),
    "FontStyle_literal": (
        0x00F89FB8,
        0x00F89FCC,
        "a9b7a80026f9ae3644bcd3593bcf123876a988c918b96b583abd958ae6a56e63",
    ),
    "UILabel_embedded_style_getter": (
        0x006CEDF0,
        0x006CEDF7,
        "a8ad62edba740bfbe13316ed525c94d88c3b120e447816c97b16e4fe494817dd",
    ),
    "UILabel_FontColor_setter": (
        0x006D0F40,
        0x006D0FB1,
        "ee498266c47a808ed32824391b9ee6650765b85c80b752c9c02018b1bbdcb320",
    ),
    "UILabel_OutlineEffectColor_setter": (
        0x006D0CF0,
        0x006D0D37,
        "b4e239417c7779d63e80d4ebc48bb5788e75cbdf8bb546d278c63e9588961f7f",
    ),
    "wide_int_default_wrapper": (
        0x00894700,
        0x00894718,
        "7bbb3cce47e58d3fcbd4fb2b4563087334957ec54301feecde3bc1fbb97b3885",
    ),
    "CNetNPC_slot38_ready_zero": (
        0x0045B770,
        0x0045B892,
        "63ea934b2b0b76b5a56d7fce1cdfc4b204310ab179035629a645152681185428",
    ),
    "actor_model_state_ready_store": (
        0x00442340,
        0x0044264C,
        "28b616acdda313d434ddac21e5e538d4f564802c0ec8755efbbc50eb92032ce1",
    ),
}

EXPECTED_PALETTE = {
    56: {
        "FontColor": "(255, 62, 255, 255)",
        "OutlineEffectColor": "(136, 2, 5, 255)",
        "label": "magenta_or_pink",
    },
    57: {
        "FontColor": "(83, 255, 83, 255)",
        "OutlineEffectColor": "(3, 122, 78, 255)",
        "label": "green",
    },
    58: {
        "FontColor": "(140, 198, 255, 255)",
        "OutlineEffectColor": "(0, 0, 213, 255)",
        "label": "light_blue",
    },
    59: {
        "FontColor": "(0, 255, 255, 255)",
        "OutlineEffectColor": "(80, 80, 80, 255)",
        "label": "cyan",
    },
    60: {
        "FontColor": "(255, 255, 0, 255)",
        "OutlineEffectColor": "(80, 80, 80, 255)",
        "label": "yellow",
    },
    61: {
        "FontColor": "(255, 100, 100, 255)",
        "OutlineEffectColor": "(150, 0, 0, 255)",
        "label": "red_or_pink_red",
    },
    62: {
        "FontColor": "(255, 159, 113, 255)",
        "OutlineEffectColor": "(91, 30, 0, 255)",
        "label": "orange_or_salmon",
    },
    63: {
        "FontColor": "(179, 179, 179, 255)",
        "OutlineEffectColor": "(60, 60, 60, 255)",
        "label": "gray",
    },
}
EXPECTED_FONT_STYLE_ROOT = "FontStyleList"
EXPECTED_FONT_STYLE_IDS = tuple(range(1, 187))

CANONICAL_KEYS = {
    "positive_style_56": "d00cd399a763ceb0d1352b74c00093e7e8957722c3caea18c62f2ce088458f38",
    "positive_style_58": "4595bc30de5d39c8ba20a81c18c30fb00f300adbd7b73001eb8aa732d6a52d77",
    "positive_style_59": "e44ecaf6446911638551ef9bad89d7d04259d1f0c59ea3c74b0ae0508b48a156",
    "positive_style_57": "89486c0e6d4867c07052ce6ef8e1d5a80e45333c51c585a83ae23e72f8218f9a",
    "yellow_relation": "a299acc3fee844cc2bfa7d7fe4b7b0b73bdfc34b9ea9fcefc48fe93f514fb796",
    "gray_death": "1adabd3b46ed07a4e0500abc36ca7c0dd61927ca47cbde445cff42d5ae0f8ab0",
    "red_offensive": "fb36b6970fed082995253f8c5519b4340b00e22336e6c903defc0a11de99e9de",
    "red_latched": "7d88cf227898eb80cfb2d8d50efe0f9716111f635af7e59b23987710a6e26363",
    "orange_clear": "92ee8a575194915205c42c2545c65fdbe034186ff29e3ead0c58595fae969da2",
}

EXPECTED_LITERAL_ANCHORS = (
    (0x00F15E14, "n_MODEL_SAVE"),
    (0x00F1DB1C, "Update_Sin_Result"),
    (0x00F1DB04, "7SINS_TEXT"),
    (0x00F0C958, "n_ID"),
    (0x00F0DF28, "AI_WANDER"),
    (0x00F0DF10, "n_OFFESIVE"),
    (0x00F2CFD4, "NameBoard_Player"),
    (0x00F0C794, "LABEL_NAME"),
    (0x00F0DABC, "board01"),
)

EXPECTED_CALL_ANCHORS = (
    (0x004656FF, 0x00467790),
    (0x005E223C, 0x0089A600),
    (0x005E2316, 0x0089A640),
    (0x005E4085, 0x00446F30),
    (0x005DFF8E, 0x0089A600),
    (0x005E0081, 0x0089A640),
    (0x005DFFA8, 0x0089A600),
    (0x005E009B, 0x0089A640),
    (0x005DFFB7, 0x0089A600),
    (0x005E00AA, 0x0089A640),
    (0x005DFFC6, 0x0089A600),
    (0x005E00B9, 0x0089A640),
    (0x005E407E, 0x00402A20),
    (0x00406196, 0x00402A20),
    (0x0040619D, 0x00445480),
    (0x00446FA3, 0x00446990),
    (0x00446AA8, 0x00446090),
    (0x00446132, 0x005FC970),
    (0x005FC9F3, 0x005FC720),
    (0x005FC79F, 0x006F40D0),
    (0x004454F4, 0x00444400),
    (0x004446A7, 0x00443F50),
    (0x0045C5A4, 0x005BB3A0),
    (0x0045C5FA, 0x005BABC0),
    (0x0040A2E9, 0x00408530),
    (0x004086E6, 0x00A9F860),
    (0x00A9F8ED, 0x00419A60),
    (0x00A9F982, 0x00894700),
    (0x00A9F9BE, 0x00A9D6B0),
    (0x00A9F9D5, 0x006BC410),
    (0x00A9FA01, 0x006BC410),
    (0x00A9FA11, 0x00A9DAE0),
    (0x0045B7D6, 0x00442340),
    (0x00A9DC16, 0x0053F7B0),
    (0x00A9DCEC, 0x0053F7B0),
    (0x0053F7DA, 0x0053F5E0),
    (0x00AA48C9, 0x00894700),
    (0x00AA490D, 0x00A9DAE0),
    (0x00AA37EE, 0x00A9F590),
    (0x00AA6F3E, 0x00A8ACF0),
)

EXPECTED_PORT_ROYAL_IDENTITIES = (0x1001, 0x1002, 0x1003, 0x1004, 0x1005, 0x1006)
EXPECTED_ORDERED_EVIDENCE_KEY_DIGEST = (
    "da15334224f67520c4401da4f8e83f8d31dc176db6e6821c444534c05fe1c082"
)
MANUAL_HASH_STATUS = "PROVEN_EXACT_MANUAL_HASH_ANCHORED"
MECHANICAL_CENSUS_STATUS = "PROVEN_EXACT_MECHANICAL_CENSUS"
MANUAL_HASH_NONCLAIM = (
    "The predicate, branch polarity, pointer/dataflow, queue element, and call-argument "
    "semantics are manual x86 interpretation anchored to the pinned spans and byte checks; "
    "generator PASS does not symbolically derive them."
)

EXPECTED_ROW_MANIFEST = (
    ("MCG-IMG-001", "TYPE_IDENTITY", ""),
    ("MCG-IMG-002", "TYPE_FACTORY", ""),
    ("MCG-IMG-003", "VTABLE_BRIDGE", ""),
    ("MCG-IMG-004", "ACTOR_ENTRY_WIRE_WRITE", ""),
    ("MCG-IMG-005", "ACTOR_ENTRY_WIRE_READ", ""),
    ("MCG-IMG-006", "RUNTIMERES_DISPATCH", ""),
    ("MCG-IMG-007", "ACTOR_ENTRY_IDENTITY_LOOKUP", ""),
    ("MCG-IMG-008", "FACTORY_POINTER_FLOW", ""),
    ("MCG-IMG-009", "BRIDGE_COPY", ""),
    ("MCG-IMG-010", "BRIDGE_COPY", ""),
    ("MCG-IMG-011", "SIGNED_IDENTITY_GATE", ""),
    ("MCG-IMG-012", "SIGNED_IDENTITY_GATE", ""),
    ("MCG-IMG-013", "SEPARATE_ATTR_IDENTITY", ""),
    ("MCG-IMG-014", "SEPARATE_ATTR_CHAIN", ""),
    ("MCG-IMG-015", "NON_ALIAS_BOUNDARY", ""),
    ("MCG-IMG-016", "SEPARATE_RECORD_TYPE", ""),
    ("MCG-IMG-017", "SEPARATE_RECORD_DEFAULT", ""),
    ("MCG-IMG-018", "SEPARATE_RECORD_WIRE_READ", ""),
    ("MCG-IMG-019", "SEPARATE_RECORD_WIRE_READ", ""),
    ("MCG-IMG-020", "SEPARATE_RECORD_WIRE_READ", ""),
    ("MCG-IMG-021", "SEPARATE_RECORD_WIRE_READ", ""),
    ("MCG-IMG-022", "SEPARATE_RECORD_PADDING_BLOCKER", ""),
    ("MCG-IMG-023", "SEPARATE_RECORD_ALLOCATOR_BOUNDARY", ""),
    ("MCG-IMG-024", "RECORD_SEPARATION", ""),
    ("MCG-IMG-025", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["positive_style_56"]),
    ("MCG-IMG-026", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["positive_style_58"]),
    ("MCG-IMG-027", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["positive_style_59"]),
    ("MCG-IMG-028", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["positive_style_57"]),
    ("MCG-IMG-029", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["yellow_relation"]),
    ("MCG-IMG-030", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["gray_death"]),
    ("MCG-IMG-031", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["red_offensive"]),
    ("MCG-IMG-032", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["red_latched"]),
    ("MCG-IMG-033", "TYPED_SELECTOR_CROSSWALK", CANONICAL_KEYS["orange_clear"]),
    ("MCG-IMG-034", "DEATH_PREDICATE", ""),
    ("MCG-IMG-035", "RUNTIME_BIT_INIT", ""),
    ("MCG-IMG-036", "RUNTIME_BIT_WRITER", ""),
    ("MCG-IMG-037", "RUNTIME_BIT_WRITER", ""),
    (
        "MCG-IMG-038",
        "RUNTIME_BIT_CONSUME_CLEAR",
        CANONICAL_KEYS["red_latched"] + ";" + CANONICAL_KEYS["orange_clear"],
    ),
    ("MCG-IMG-039", "SINGLETON_MANAGER_JOIN", ""),
    ("MCG-IMG-040", "FACTORY_REGISTRY_JOIN", ""),
    ("MCG-IMG-041", "REGISTRY_NODE_LAYOUT", ""),
    ("MCG-IMG-042", "MANAGER_TICK_DISPATCH", ""),
    ("MCG-IMG-043", "SAME_RECEIVER_SELECTOR_CALL", ""),
    ("MCG-IMG-044", "NAMEBOARD_CONTROLLER_BIND", ""),
    ("MCG-IMG-045", "CONTROLLER_STYLE_STORE", ""),
    ("MCG-IMG-046", "MODEL_READY_BIT_PRODUCER", ""),
    ("MCG-IMG-047", "NAMEBOARD_READY_BYTE", ""),
    ("MCG-IMG-048", "DELAYED_READY_LATCH", ""),
    ("MCG-IMG-049", "DISTANCE_SELECTOR_GATE", ""),
    ("MCG-IMG-050", "REGISTRY_LIFETIME_REMOVAL", ""),
    ("MCG-IMG-051", "LABEL_FONTSTYLE_SETTER", ""),
    ("MCG-IMG-052", "LABEL_FONTSTYLE_APPLY", ""),
    ("MCG-IMG-053", "LABEL_RENDER_CEILING", ""),
    ("MCG-IMG-054", "STYLE_REGISTRY_STARTUP_WIRING", ""),
    ("MCG-IMG-055", "STYLE_REGISTRY_CHILD_LOAD", ""),
    ("MCG-IMG-056", "NAMEBOARD_READY_ZERO_PATH", ""),
    ("MCG-IMG-057", "FONTSTYLE_COLOR_PROPERTY_ANCHORS", ""),
    ("MCG-IMG-058", "FONTSTYLE_COLOR_PARSE_APPLY", ""),
    ("MCG-DATA-001", "DATA_PALETTE", ""),
    ("MCG-DATA-002", "DATA_PALETTE", ""),
    ("MCG-DATA-003", "DATA_PALETTE", ""),
    ("MCG-DATA-004", "DATA_PALETTE", ""),
    ("MCG-DATA-005", "DATA_PALETTE", ""),
    ("MCG-DATA-006", "DATA_PALETTE", ""),
    ("MCG-DATA-007", "DATA_PALETTE", ""),
    ("MCG-DATA-008", "DATA_PALETTE", ""),
)

FIELDNAMES = (
    "gate_key",
    "row_kind",
    "owner_type",
    "applies_to_class",
    "input_field",
    "runtime_field",
    "condition",
    "output",
    "semantic_status",
    "producer_va",
    "consumer_va",
    "span_start_va",
    "span_end_va",
    "file_off_start",
    "file_off_end",
    "span_sha256",
    "support_spans",
    "canonical_selector_keys",
    "current_server_emit_status",
    "source",
    "source_file",
    "source_locator",
    "source_sha256",
    "nonclaim",
    "blocker",
    "required_next_evidence",
    "evidence_key",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path: Path, expected_size: int, expected_sha256: str) -> str:
    if not path.is_file():
        raise RuntimeError(f"missing pinned input: {path.name}")
    actual_size = path.stat().st_size
    if actual_size != expected_size:
        raise RuntimeError(
            f"input size mismatch: {path.name}: expected {expected_size}, got {actual_size}"
        )
    actual_hash = sha256_file(path)
    if actual_hash != expected_sha256:
        raise RuntimeError(
            f"input hash mismatch: {path.name}: expected {expected_sha256}, got {actual_hash}"
        )
    return actual_hash


def va_to_offset(va: int) -> int:
    for _, section_va, virtual_size, raw_offset, raw_size in SECTIONS:
        file_backed_size = min(virtual_size, raw_size)
        if section_va <= va < section_va + file_backed_size:
            return raw_offset + (va - section_va)
    raise RuntimeError(f"VA outside pinned file-backed section bytes: 0x{va:08X}")


def rva_to_offset(rva: int) -> int:
    return va_to_offset(IMAGE_BASE + rva)


def fmt_va(value: int) -> str:
    return f"0x{value:08X}"


def verify_pe_section_table(image: bytes) -> None:
    pe_offset = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_offset : pe_offset + 4] != b"PE\x00\x00":
        raise RuntimeError("invalid PE signature for section census")
    section_count = struct.unpack_from("<H", image, pe_offset + 6)[0]
    optional_size = struct.unpack_from("<H", image, pe_offset + 20)[0]
    if section_count != len(SECTIONS) or section_count != 6:
        raise RuntimeError(
            f"PE section-count mismatch: expected 6, got {section_count}"
        )
    table_offset = pe_offset + 24 + optional_size
    observed = []
    for index in range(section_count):
        entry_offset = table_offset + index * 40
        name = image[entry_offset : entry_offset + 8].split(b"\x00", 1)[0].decode(
            "ascii"
        )
        virtual_size, rva, raw_size, raw_offset = struct.unpack_from(
            "<IIII", image, entry_offset + 8
        )
        observed.append(
            (name, IMAGE_BASE + rva, virtual_size, raw_offset, raw_size)
        )
    if tuple(observed) != SECTIONS:
        raise RuntimeError("exact six-section PE table drift")
    previous_raw_end = 0
    for name, _, virtual_size, raw_offset, raw_size in SECTIONS:
        raw_end = raw_offset + raw_size
        if (
            virtual_size <= 0
            or raw_size <= 0
            or raw_offset < previous_raw_end
            or raw_end > len(image)
        ):
            raise RuntimeError(f"invalid pinned raw bounds for section {name}")
        previous_raw_end = raw_end
    if previous_raw_end != len(image):
        raise RuntimeError("final PE raw section does not end at pinned image size")


def read_c_string(image: bytes, va: int) -> str:
    start = va_to_offset(va)
    end = image.find(b"\x00", start)
    if end < 0:
        raise RuntimeError(f"unterminated ASCII string at 0x{va:08X}")
    return image[start:end].decode("ascii")


def read_w_string(image: bytes, va: int) -> str:
    start = va_to_offset(va)
    cursor = start
    while cursor + 1 < len(image) and image[cursor : cursor + 2] != b"\x00\x00":
        cursor += 2
    if cursor + 1 >= len(image):
        raise RuntimeError(f"unterminated UTF-16 string at 0x{va:08X}")
    return image[start:cursor].decode("utf-16le")


def rel32_call_target(image: bytes, call_va: int) -> int:
    offset = va_to_offset(call_va)
    if image[offset] != 0xE8:
        raise RuntimeError(f"expected rel32 call at 0x{call_va:08X}")
    relative = struct.unpack_from("<i", image, offset + 1)[0]
    return call_va + 5 + relative


def raw_rel32_call_sites(image: bytes, target_va: int) -> tuple[int, ...]:
    """Census E8+rel32 at every file-backed byte position in all six sections."""

    sites: list[int] = []
    verify_pe_section_table(image)
    for _, section_va, virtual_size, raw_offset, raw_size in SECTIONS:
        file_backed_size = min(virtual_size, raw_size)
        section = image[raw_offset : raw_offset + file_backed_size]
        cursor = 0
        while True:
            index = section.find(b"\xE8", cursor)
            if index < 0 or index + 5 > len(section):
                break
            call_va = section_va + index
            relative = struct.unpack_from("<i", section, index + 1)[0]
            if call_va + 5 + relative == target_va:
                sites.append(call_va)
            cursor = index + 1
    return tuple(sites)


def resolve_import(image: bytes, target_iat_va: int) -> tuple[str, str]:
    pe_offset = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_offset : pe_offset + 4] != b"PE\x00\x00":
        raise RuntimeError("invalid PE signature")
    optional_offset = pe_offset + 24
    if struct.unpack_from("<H", image, optional_offset)[0] != 0x10B:
        raise RuntimeError("expected PE32 optional header")
    if struct.unpack_from("<I", image, optional_offset + 28)[0] != IMAGE_BASE:
        raise RuntimeError("unexpected image base")
    import_rva, import_size = struct.unpack_from("<II", image, optional_offset + 104)
    descriptor_offset = rva_to_offset(import_rva)
    descriptor_end = descriptor_offset + import_size
    while descriptor_offset + 20 <= descriptor_end:
        original, timestamp, forwarder, name_rva, first_thunk = struct.unpack_from(
            "<IIIII", image, descriptor_offset
        )
        if original == timestamp == forwarder == name_rva == first_thunk == 0:
            break
        dll_start = rva_to_offset(name_rva)
        dll_end = image.find(b"\x00", dll_start)
        dll_name = image[dll_start:dll_end].decode("ascii")
        lookup_rva = original or first_thunk
        index = 0
        while True:
            thunk = struct.unpack_from("<I", image, rva_to_offset(lookup_rva) + index * 4)[0]
            if thunk == 0:
                break
            iat_va = IMAGE_BASE + first_thunk + index * 4
            if iat_va == target_iat_va:
                if thunk & 0x80000000:
                    return dll_name, f"ordinal_{thunk & 0xFFFF}"
                name_offset = rva_to_offset(thunk) + 2
                name_end = image.find(b"\x00", name_offset)
                return dll_name, image[name_offset:name_end].decode("ascii")
            index += 1
        descriptor_offset += 20
    raise RuntimeError(f"IAT entry not found: 0x{target_iat_va:08X}")


def verify_spans(image: bytes) -> None:
    verify_pe_section_table(image)
    for name, (start_va, end_va, expected_hash) in SPANS.items():
        start_offset = va_to_offset(start_va)
        end_offset = start_offset + (end_va - start_va)
        if not (0 <= start_offset < end_offset <= len(image)):
            raise RuntimeError(f"span outside image: {name}")
        actual_hash = sha256_bytes(image[start_offset:end_offset])
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"span hash mismatch: {name}: expected {expected_hash}, got {actual_hash}"
            )


def verify_static_anchors(image: bytes) -> dict[str, object]:
    if read_c_string(image, 0x0101F4E8) != ".?AVCreateActorDataEx@@":
        raise RuntimeError("CreateActorDataEx RTTI mismatch")
    if read_c_string(image, 0x0101B140) != ".?AVCNetNPC@@":
        raise RuntimeError("CNetNPC RTTI mismatch")
    if read_c_string(image, 0x0101ED44) != ".?AVUILabel@@":
        raise RuntimeError("UILabel RTTI mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x00F0DF68))[0] != 0x0045D200:
        raise RuntimeError("CNetNPC vtable +0x10 mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x00F0DF94))[0] != 0x0043BD70:
        raise RuntimeError("CNetNPC vtable +0x3C mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x00F0DFD4))[0] != 0x0045C560:
        raise RuntimeError("CNetNPC vtable +0x7C nameboard creator mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x00F0DFB0))[0] != 0x0045CD80:
        raise RuntimeError("CNetNPC vtable +0x58 model callback mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x00402A73))[0] != 0x0102C6C0:
        raise RuntimeError("actor-manager singleton getter result mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x005BB419))[0] != 0x00F2CD48:
        raise RuntimeError("NPC nameboard controller constructor vtable mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x00F2CD5C))[0] != 0x005BE6C0:
        raise RuntimeError("NPC nameboard controller +0x14 binder mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x00F2CD7C))[0] != 0x009F1A70:
        raise RuntimeError("NPC nameboard controller +0x34 style store mismatch")
    ui_label_vtable_bases = (0x00F89760, 0x00F899A8)
    ui_label_slot_targets = {
            0xD8: 0x006D0F40,
            0x34: 0x00AA70F0,
            0x38: 0x00AA71A0,
            0x138: 0x004021F0,
            0x13C: 0x00AA37D0,
            0x140: 0x006CEDF0,
            0x144: 0x00AA6EF0,
            0x224: 0x006D0CF0,
            0x240: 0x00AA6FF0,
    }
    for base in ui_label_vtable_bases:
        for displacement, expected_target in ui_label_slot_targets.items():
            actual_target = struct.unpack_from(
                "<I", image, va_to_offset(base + displacement)
            )[0]
            if actual_target != expected_target:
                raise RuntimeError(
                    f"UILabel vtable 0x{base:08X} +0x{displacement:X} mismatch"
                )

    style_path_literal = read_c_string(image, 0x00F091F0)
    if style_path_literal != ".\\Data\\GUI\\Model\\BigFontStyle.fsl":
        raise RuntimeError("BigFontStyle path literal mismatch")
    style_id_attribute = read_w_string(image, 0x00F44BC4)
    if style_id_attribute != "ID":
        raise RuntimeError("FontStyle ID attribute literal mismatch")
    if image[va_to_offset(0x004086E1)] != 0xB9:
        raise RuntimeError("style-manager ECX immediate opcode mismatch")
    style_manager_va = struct.unpack_from(
        "<I", image, va_to_offset(0x004086E2)
    )[0]
    if style_manager_va != 0x01090708:
        raise RuntimeError("style-manager address mismatch")
    style_loader_va = rel32_call_target(image, 0x004086E6)
    if style_loader_va != 0x00A9F860:
        raise RuntimeError("BigFontStyle loader call target mismatch")
    style_loader_call_sites = raw_rel32_call_sites(image, style_loader_va)
    if style_loader_call_sites != (0x004086E6,):
        raise RuntimeError(
            "BigFontStyle loader raw-rel32 census mismatch: "
            f"{','.join(fmt_va(value) for value in style_loader_call_sites)}"
        )
    style_outer_init_va = rel32_call_target(image, 0x0040A2E9)
    if style_outer_init_va != 0x00408530:
        raise RuntimeError("style outer-init call target mismatch")
    style_outer_init_call_sites = raw_rel32_call_sites(image, style_outer_init_va)
    if style_outer_init_call_sites != (0x0040A2E9,):
        raise RuntimeError(
            "style outer-init raw-rel32 census mismatch: "
            f"{','.join(fmt_va(value) for value in style_outer_init_call_sites)}"
        )
    cnetnpc_slot38_target = struct.unpack_from(
        "<I", image, va_to_offset(0x00F0DF90)
    )[0]
    if cnetnpc_slot38_target != 0x0045B770:
        raise RuntimeError("CNetNPC vtable +0x38 mismatch")
    ready_zero_call_target = rel32_call_target(image, 0x0045B7D6)
    if ready_zero_call_target != 0x00442340:
        raise RuntimeError("CNetNPC +0x38 readiness call target mismatch")
    if image[va_to_offset(0x00A9F98E) : va_to_offset(0x00A9F98E) + 4] != bytes.fromhex(
        "85c07f13"
    ):
        raise RuntimeError("FontStyle signed-positive ID branch mismatch")
    style_id_lower_exclusive = 0
    style_id_accept_relation = "signed_greater_than"

    font_color_property_va = 0x00F23608
    outline_color_property_va = 0x00F89EF0
    label_fontstyle_id_property_va = 0x00F8A4DC
    embedded_fontstyle_property_va = 0x00F89FB8
    font_color_property = read_w_string(image, font_color_property_va)
    outline_color_property = read_w_string(image, outline_color_property_va)
    label_fontstyle_id_property = read_w_string(
        image, label_fontstyle_id_property_va
    )
    embedded_fontstyle_property = read_w_string(
        image, embedded_fontstyle_property_va
    )
    if (
        font_color_property != "FontColor"
        or outline_color_property != "OutlineEffectColor"
        or label_fontstyle_id_property != "FontStyleID"
        or embedded_fontstyle_property != "FontStyle"
    ):
        raise RuntimeError("FontStyle color/property literal mismatch")

    style_property_parser_va = rel32_call_target(image, 0x00A9FA11)
    if style_property_parser_va != 0x00A9DAE0:
        raise RuntimeError("registry FontStyle property parser target mismatch")
    style_property_parser_call_sites = raw_rel32_call_sites(
        image, style_property_parser_va
    )
    if style_property_parser_call_sites != (0x00A9FA11, 0x00AA490D):
        raise RuntimeError(
            "FontStyle property parser whole-image raw-rel32 census mismatch: "
            f"{','.join(fmt_va(value) for value in style_property_parser_call_sites)}"
        )

    rgba_property_wrapper_va = rel32_call_target(image, 0x00A9DC16)
    if (
        rgba_property_wrapper_va != 0x0053F7B0
        or rel32_call_target(image, 0x00A9DCEC) != rgba_property_wrapper_va
    ):
        raise RuntimeError("FontStyle color property-wrapper target mismatch")
    rgba_normalized_parser_va = rel32_call_target(image, 0x0053F7DA)
    if rgba_normalized_parser_va != 0x0053F5E0:
        raise RuntimeError("RGBA normalized parser target mismatch")
    rgba_divisor_va = 0x00F0C630
    rgba_divisor = struct.unpack_from("<d", image, va_to_offset(rgba_divisor_va))[0]
    if rgba_divisor != 255.0:
        raise RuntimeError("RGBA normalization divisor mismatch")

    label_numeric_conversion_va = rel32_call_target(image, 0x00AA48C9)
    if label_numeric_conversion_va != 0x00894700:
        raise RuntimeError("UILabel FontStyleID numeric conversion target mismatch")
    label_empty_sentinel_va = 0x00F0930C
    if read_w_string(image, label_empty_sentinel_va) != "":
        raise RuntimeError("UILabel empty-string sentinel mismatch")
    label_zero_dispatch_va = 0x00AA48DC
    label_zero_dispatch_id = 0
    label_style_lookup_va = rel32_call_target(image, 0x00AA37EE)
    if label_style_lookup_va != 0x00A9F590:
        raise RuntimeError("UILabel requested-style lookup target mismatch")
    label_embedded_style_getter_va = ui_label_slot_targets[0x140]
    label_style_apply_va = ui_label_slot_targets[0x144]
    label_font_color_setter_va = ui_label_slot_targets[0xD8]
    label_outline_color_setter_va = ui_label_slot_targets[0x224]

    byte_anchors = (
        # registry local value = {key low, key high, actor pointer}
        (0x00446110, bytes.fromhex("8954241c89442420897c2424")),
        # node constructor copies value+0/+4/+8 to node+0x10/+0x14/+0x18
        (0x006F4130, bytes.fromhex("8b08894e108b50048956148b4808894e18")),
        # tick reads node+0x18 and calls the actor updater
        (0x004454ED, bytes.fromhex("8b4d1885c97405e807efffff")),
        # updater preserves the receiver and reads that actor's +0x254 controller
        (0x00444404, bytes.fromhex("8bf18b8e5402000085c9")),
        # updater passes the preserved actor as selector ECX
        (0x004446A5, bytes.fromhex("8bcee8a4f8ffff")),
        # selector invocation readiness gates and the producer of +0x260
        (0x00444693, bytes.fromhex(
            "80be5802000000742880be6002000000741f8bcee8a4f8ffff"
        )),
        (0x0045C52C, bytes.fromhex(
            "80be60020000007520f6467040741ab801000000018664020000"
            "83be640200000a7e06888660020000"
        )),
        # controller back-pointer and style-id store
        (0x005BABC0, bytes.fromhex("8b44240485c07403894130c20400")),
        (0x009F1A70, bytes.fromhex("8b442404894134c20400")),
        # UI update reads controller+0x50 LABEL_NAME and controller+0x34 style
        (0x005BDA47, bytes.fromhex(
            "8b4e5085c90f84650400008b1598310901f6827807000020750a837e4400"
            "0f86bb0300008b018b90380100008b7e34ffd23bc774198b4e508b018b90"
            "3c01000057ffd2"
        )),
        # CNetNPC model callback wrapper and common callback ready-bit producer.
        (0x0045CDA8, bytes.fromhex("8b44244450e87e79feff")),
        (0x00444756, bytes.fromhex(
            "8b5c242485db0f84030200008b73488974242485f6740a8d460450"
            "ff15b0b1c300c744241c0000000085f60f84bb010000837e08000f84"
        )),
        (0x004447B7, bytes.fromhex("89b78000000083c60456ff15b0b1c300")),
        (0x004448B4, bytes.fromhex("834f7040")),
        # Nameboard creation sets +0x258, then the common updater refreshes it.
        (0x0045D3D5, bytes.fromhex(
            "8b865c03000085c07440f680840000000275378b068b507c8bceffd284c0742a"
        )),
        (0x0045D418, bytes.fromhex("c6865802000001")),
        (0x0044376D, bytes.fromhex(
            "833d60250301067429f74610004000007409c6865802000000eb17"
            "8b868000000085c0750432c0eb038a4074888658020000"
        )),
        # Squared 10000/5000 thresholds and readiness-gated selector receiver.
        (0x0044458A, bytes.fromhex(
            "a8017528f30f2a0d48230201f30f5ac9660f28d183c801f20f59d1"
            "660f5acaa3502d0301f30f110d4c2d0301a8027528f30f2a0d40230201"
            "f30f5ac9660f28d183c802f20f59d1660f5acaa3502d0301"
            "f30f110d482d0301f30f5a154c2d0301f30f5ac8660f2fca7663"
        )),
        (0x00444657, bytes.fromhex(
            "f30f5a0d482d0301f30f5ac0660f2fc17610d944240c51d91c2455"
            "8bcee83791ffff8b865402000085c074108b401085c07409b9feff0000"
            "6621481880be5802000000742880be6002000000741f8bce"
        )),
        # State==3 skips erase; stale generations enqueue actor pointers.
        (0x00446342, bytes.fromhex(
            "8b4b1880b9d4000000038d4c241874238bebe8576f020055568d542428"
            "528bcfe869271f008b5c241c8b742418eba38b06ebc2"
        )),
        (0x0044702F, bytes.fromhex(
            "8b87d00000003b45040f84800000008b178b028bcfffd0506804cb0201"
            "e85f8244000fb6c083c408f7d81bc023c7755f"
        )),
        (0x0044705F, bytes.fromhex(
            "8b4d388d752c85c9750833c0eb0c8b36eba88b46142bc1c1f8028b5e10"
            "8bd32bd1c1fa023bd0730a893b83c304895e10eb1f3bcb7606ff15c0b4c300"
            "8b068d4c24245153508d542424528bcee820f81a00"
        )),
        (0x004467EA, bytes.fromhex("8bcee8dffbffff")),
        # LABEL_NAME is dynamically cast through the UILabel type token.
        (0x005BE739, bytes.fromhex(
            "8b178b028bcfffd050e8c9884e0050e8630b2d000fb6c083c408f7d8"
            "1bc023c7eb0233c08b4e20"
        )),
        # BigFontStyle literal-to-manager loader wiring, loop predicate, and calls.
        (0x0040A2E7, bytes.fromhex("8bcee842e2ffff84c00f84f0feffff")),
        (0x0040867A, bytes.fromhex("68f091f000")),
        (0x004086E1, bytes.fromhex("b908070901e875716900")),
        (0x00A9F8ED, bytes.fromhex("e86ea197ff")),
        (0x00A9F953, bytes.fromhex("6a0068c44bf400")),
        (0x00A9F982, bytes.fromhex("e8794ddfff83c4088944247085c07f13")),
        (0x00A9F9A5, bytes.fromhex("6a78e874d6deff")),
        (0x00A9F9CE, bytes.fromhex("8bcec644246c02e836cac1ff")),
        (0x00A9F9FA, bytes.fromhex("8d442470508bcee80acac1ff8b006a00")),
        (0x00A9FA0A, bytes.fromhex("8d4c2434518bc8e8cae0ffff")),
        # Present FontStyleID with empty/sentinel text bypasses _wtoi and
        # converges on the vslot+0x13C dispatch with an explicit zero argument.
        (0x00AA48AF, bytes.fromhex(
            "8bf857e809fedeff83c40484c0751e81ff0c93f00074166a0057"
            "e832fedeff8b1383c408508b823c010000eb498b1333c0508b82"
            "3c010000eb3c"
        )),
        # CNetNPC slot +0x38 conditionally requests state byte zero.
        (0x0045B79F, bytes.fromhex(
            "803dc11d0201008bf10f84c80000008b865c03000085c00f84ba000000"
        )),
        (0x0045B7D0, bytes.fromhex("6a016a008bcee8656bfeff")),
        (0x0044237B, bytes.fromhex(
            "8bd98b8b80000000895c242085c90f84930200008a41748b9424b80000003ac2"
        )),
        (0x004424AC, bytes.fromhex("8a9424b8000000889358020000")),
    )
    for va, expected in byte_anchors:
        start = va_to_offset(va)
        if image[start : start + len(expected)] != expected:
            raise RuntimeError(f"same-instance byte anchor mismatch at 0x{va:08X}")

    if len(EXPECTED_LITERAL_ANCHORS) != 9 or len(
        {va for va, _ in EXPECTED_LITERAL_ANCHORS}
    ) != 9:
        raise RuntimeError("literal-anchor manifest cardinality drift")
    for va, expected in EXPECTED_LITERAL_ANCHORS:
        actual = read_w_string(image, va)
        if actual != expected:
            raise RuntimeError(
                f"wide literal mismatch at 0x{va:08X}: expected {expected}, got {actual}"
            )

    if len(EXPECTED_CALL_ANCHORS) != 40 or len(
        {call_va for call_va, _ in EXPECTED_CALL_ANCHORS}
    ) != 40:
        raise RuntimeError("call-anchor manifest cardinality drift")
    for call_va, target_va in EXPECTED_CALL_ANCHORS:
        actual_target = rel32_call_target(image, call_va)
        if actual_target != target_va:
            raise RuntimeError(
                f"codec call mismatch at 0x{call_va:08X}: "
                f"expected 0x{target_va:08X}, got 0x{actual_target:08X}"
            )

    if struct.unpack_from("<I", image, va_to_offset(0x00BCEEF1))[0] != 0x0102D938:
        raise RuntimeError("CNetNPC type-node global anchor mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x0040BA0C))[0] != 0x0101B138:
        raise RuntimeError("CNetNPC type-node RTTI anchor mismatch")
    if struct.unpack_from("<I", image, va_to_offset(0x0040BA3C))[0] != 0x00000368:
        raise RuntimeError("CNetNPC registered size mismatch")
    actor_type_4_target = struct.unpack_from(
        "<I", image, va_to_offset(0x00446B34)
    )[0]
    if actor_type_4_target != 0x00446A3D:
        raise RuntimeError("actor type 4 factory jump target mismatch")
    if rel32_call_target(image, 0x00446A53) != 0x00444F00:
        raise RuntimeError("CNetNPC factory call mismatch")

    dll_name, import_name = resolve_import(image, 0x00C3B87C)
    if dll_name.lower() != "msvcr90.dll" or import_name != "malloc":
        raise RuntimeError(
            f"allocator import mismatch: {dll_name}!{import_name}"
        )
    id_dll_name, id_import_name = resolve_import(image, 0x00C3B52C)
    if id_dll_name.lower() != "msvcr90.dll" or id_import_name != "_wtoi":
        raise RuntimeError(
            f"FontStyle ID conversion import mismatch: {id_dll_name}!{id_import_name}"
        )

    return {
        "style_path_literal": style_path_literal,
        "style_path_literal_va": 0x00F091F0,
        "style_id_attribute": style_id_attribute,
        "style_id_attribute_va": 0x00F44BC4,
        "style_manager_va": style_manager_va,
        "style_loader_va": style_loader_va,
        "style_loader_call_sites": style_loader_call_sites,
        "style_outer_init_va": style_outer_init_va,
        "style_outer_init_call_sites": style_outer_init_call_sites,
        "style_id_conversion_import": f"{id_dll_name}!{id_import_name}",
        "style_id_lower_exclusive": style_id_lower_exclusive,
        "style_id_accept_relation": style_id_accept_relation,
        "font_color_property": font_color_property,
        "font_color_property_va": font_color_property_va,
        "outline_color_property": outline_color_property,
        "outline_color_property_va": outline_color_property_va,
        "label_fontstyle_id_property": label_fontstyle_id_property,
        "label_fontstyle_id_property_va": label_fontstyle_id_property_va,
        "embedded_fontstyle_property": embedded_fontstyle_property,
        "embedded_fontstyle_property_va": embedded_fontstyle_property_va,
        "style_property_parser_va": style_property_parser_va,
        "style_property_parser_call_sites": style_property_parser_call_sites,
        "rgba_property_wrapper_va": rgba_property_wrapper_va,
        "rgba_normalized_parser_va": rgba_normalized_parser_va,
        "rgba_divisor_va": rgba_divisor_va,
        "rgba_divisor": rgba_divisor,
        "label_numeric_conversion_va": label_numeric_conversion_va,
        "label_empty_sentinel_va": label_empty_sentinel_va,
        "label_zero_dispatch_va": label_zero_dispatch_va,
        "label_zero_dispatch_id": label_zero_dispatch_id,
        "label_embedded_style_getter_va": label_embedded_style_getter_va,
        "label_style_lookup_va": label_style_lookup_va,
        "label_style_apply_va": label_style_apply_va,
        "label_font_color_setter_va": label_font_color_setter_va,
        "label_outline_color_setter_va": label_outline_color_setter_va,
        "pe_section_count": len(SECTIONS),
        "pe_section_names": tuple(section[0] for section in SECTIONS),
        "pe_section_file_backed_bounds": tuple(
            (
                name,
                section_va,
                section_va + min(virtual_size, raw_size),
                raw_offset,
                raw_offset + min(virtual_size, raw_size),
            )
            for name, section_va, virtual_size, raw_offset, raw_size in SECTIONS
        ),
        "cnetnpc_slot38_target": cnetnpc_slot38_target,
        "ready_zero_call_target": ready_zero_call_target,
        "ready_zero_requested_byte": 0,
    }


def read_selector_rows() -> list[dict[str, str]]:
    if sha256_file(SELECTOR_PATH) != SELECTOR_SHA256:
        raise RuntimeError("PF_ATTR_NAME_COLOR_SELECTOR.tsv hash mismatch")
    with SELECTOR_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != SELECTOR_ROW_COUNT:
        raise RuntimeError(
            f"expected {SELECTOR_ROW_COUNT} canonical selector rows, got {len(rows)}"
        )
    keys = [row["selector_key"] for row in rows]
    if len(set(keys)) != SELECTOR_ROW_COUNT:
        raise RuntimeError("duplicate selector_key in canonical selector table")
    missing = sorted(set(CANONICAL_KEYS.values()) - set(keys))
    if missing:
        raise RuntimeError(f"missing canonical selector keys: {','.join(missing)}")
    if any(row["source"] != "IMAGE" for row in rows):
        raise RuntimeError("canonical selector table contains non-IMAGE row")
    return rows


def run_project_git(*args: str) -> bytes:
    """Read exact repository data without consulting or mutating the worktree."""

    completed = subprocess.run(
        ["git", "-C", str(PROJECT_ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"project Git read failed ({' '.join(args)}): {detail}")
    return completed.stdout


def observe_checkout_head() -> str:
    return run_project_git("rev-parse", "HEAD").decode("ascii").strip()


def read_project_snapshot() -> dict[str, bytes]:
    """Return project bytes from the named commit, never moving checkout bytes."""

    resolved = run_project_git(
        "rev-parse", f"{PROJECT_SNAPSHOT_COMMIT}^{{commit}}"
    ).decode("ascii").strip()
    if resolved != PROJECT_SNAPSHOT_COMMIT:
        raise RuntimeError(
            "project snapshot commit resolution drift: "
            f"expected {PROJECT_SNAPSHOT_COMMIT}, got {resolved}"
        )
    commit_time = run_project_git(
        "show", "-s", "--format=%cI", PROJECT_SNAPSHOT_COMMIT
    ).decode("ascii").strip()
    if commit_time != PROJECT_SNAPSHOT_COMMIT_TIME:
        raise RuntimeError(
            "project snapshot commit-time drift: "
            f"expected {PROJECT_SNAPSHOT_COMMIT_TIME}, got {commit_time}"
        )
    archive = run_project_git(
        "archive",
        "--format=tar",
        PROJECT_SNAPSHOT_COMMIT,
        "--",
        "current/pf_login_game_server_v141.py",
        "src/pirateforce_foundation",
        "scenarios/world_scene_registry_001.json",
    )
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as handle:
        for member in handle.getmembers():
            if not member.isfile():
                continue
            extracted = handle.extractfile(member)
            if extracted is None:
                raise RuntimeError(f"project snapshot member unreadable: {member.name}")
            files[member.name] = extracted.read()
    return files


def verify_project_server_boundary() -> dict[str, str]:
    """Verify the exact-commit RECONSTRUCTED POLICY snapshot used only in the MD."""

    expected_paths = {
        PROJECT_ROOT / Path(relative) for relative in PROJECT_SOURCE_PIN_ROWS
    }
    if set(PROJECT_SOURCE_PINS) != expected_paths:
        raise RuntimeError("replacement-source pin key census drift")
    snapshot_files = read_project_snapshot()
    sources: dict[Path, bytes] = {}
    mismatches: list[str] = []
    for relative, (expected_size, expected_hash) in PROJECT_SOURCE_PIN_ROWS.items():
        path = PROJECT_ROOT / Path(relative)
        source = snapshot_files.get(relative)
        if source is None:
            mismatches.append(f"missing {relative} from pinned commit")
            continue
        actual_hash = sha256_bytes(source)
        if len(source) != expected_size or actual_hash != expected_hash:
            mismatches.append(
                f"{relative} "
                f"expected={expected_size}/{expected_hash} "
                f"actual={len(source)}/{actual_hash}"
            )
        sources[path] = source
    if mismatches:
        raise RuntimeError(
            "pinned-commit replacement source mismatch:\n" + "\n".join(mismatches)
        )
    if set(sources) != expected_paths:
        raise RuntimeError("replacement-source verification census drift")

    # Read every Foundation Python blob from the exact commit for the direct-call
    # census.  The snapshot is independent of a concurrently advancing checkout.
    foundation_snapshot: dict[str, tuple[int, str]] = {}
    direct_calls: list[tuple[str, int]] = []
    foundation_prefix = "src/pirateforce_foundation/"
    foundation_files = sorted(
        (name, raw)
        for name, raw in snapshot_files.items()
        if name.startswith(foundation_prefix) and name.endswith(".py")
    )
    for name, raw_tree_file in foundation_files:
        relative = name[len(foundation_prefix):]
        foundation_snapshot[relative] = (
            len(raw_tree_file), sha256_bytes(raw_tree_file)
        )
        tree = ast.parse(raw_tree_file.decode("utf-8"), filename=relative)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            function_name = None
            if isinstance(node.func, ast.Attribute):
                function_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                function_name = node.func.id
            if function_name == "make_remote_actor_entry":
                direct_calls.append((relative, node.lineno))
    direct_calls.sort()
    expected_direct_calls = sorted(
        (relative, line)
        for relative, line, *_rest in (
            REACHABLE_WRITER_CENSUS + EXCLUDED_WRITER_CENSUS
        )
    )
    if direct_calls != expected_direct_calls:
        raise RuntimeError(
            "Foundation make_remote_actor_entry direct-call census drift: "
            f"expected {expected_direct_calls!r}, got {direct_calls!r}"
        )
    if len(REACHABLE_WRITER_CENSUS) != 19:
        raise RuntimeError("reachable actor-type-4 writer census is not 19")
    if sum(row[2] == "SHIPPED" for row in REACHABLE_WRITER_CENSUS) != 18:
        raise RuntimeError("shipped writer census is not 18")
    if sum(
        row[2] == "OPERATOR_CONDITIONAL_DIAGNOSTIC"
        for row in REACHABLE_WRITER_CENSUS
    ) != 1:
        raise RuntimeError("operator-conditional diagnostic writer census is not 1")
    if len(EXCLUDED_WRITER_CENSUS) != 11:
        raise RuntimeError("excluded writer census is not 11")

    def project_bytes(relative: str) -> bytes:
        return sources[PROJECT_ROOT / Path(relative)]

    def foundation_text(relative: str) -> str:
        return project_bytes(
            f"src/pirateforce_foundation/{relative}"
        ).decode("utf-8")

    def pinned_line(relative: str, line_number: int) -> str:
        lines = foundation_text(relative).splitlines()
        if not (1 <= line_number <= len(lines)):
            raise RuntimeError(
                f"source line outside file: {relative}:{line_number}"
            )
        return lines[line_number - 1].strip()

    for relative, line_number in FORMULA_ANCHORS:
        if pinned_line(relative, line_number) != (
            "return 0x2000 + self.placement_index + 1"
        ):
            raise RuntimeError(
                f"placement identity formula drift: {relative}:{line_number}"
            )
    if pinned_line("world_face_frame.py", 197) != "aid = 0x2000 + idx + 1":
        raise RuntimeError("world-face placement identity formula drift")
    if pinned_line("mob_diag_multi_object.py", 239) != "DIAG_PLACEMENT_BASE = 9000":
        raise RuntimeError("diagnostic placement base drift")
    if 0x2000 + 9000 + 4 + 1 != 0x432D:
        raise RuntimeError("diagnostic D3 identity arithmetic drift")
    if "_diag_mob(4)" not in pinned_line("mob_diag_multi_object.py", 436):
        raise RuntimeError("diagnostic D3 slot drift")

    raw = sources[SERVER_PATH]
    text = raw.decode("utf-8")

    def region(start_marker: str, end_marker: str) -> tuple[int, int]:
        start = text.index(start_marker)
        end = text.index(end_marker, start)
        return start, end

    def one_line(needle: str, start: int = 0, end: int | None = None) -> int:
        search_end = len(text) if end is None else end
        positions: list[int] = []
        cursor = start
        while True:
            position = text.find(needle, cursor, search_end)
            if position < 0:
                break
            positions.append(position)
            cursor = position + 1
        if len(positions) != 1:
            raise RuntimeError(
                f"expected one server-source anchor for {needle!r}, got {len(positions)}"
            )
        return text.count("\n", 0, positions[0]) + 1

    qword_start, qword_end = region("def qwordtag(", "\ndef f32tag(")
    npc_start, npc_end = region("def make_npc_attr(", "\ndef make_remote_movement_attr(")
    entry_start, entry_end = region(
        "def make_remote_actor_entry(", "\ndef make_runtime_remote_actors("
    )
    population_start, population_end = region(
        "def make_port_royal_npc_single_packets(", "\n\ndef "
    )
    qword_pack_line = one_line(
        'struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)', qword_start, qword_end
    )
    npc_identity_line = one_line(
        "+ qwordtag(0x32, actor_identity)", npc_start, npc_end
    )
    actor_entry_identity_line = one_line(
        "out += qwordtag(0x32, actor_identity)", entry_start, entry_end
    )
    npc_builder_line = one_line(
        "(NPC_ATTR, make_npc_attr(template_id, actor_identity, 1, 0))",
        population_start, population_end,
    )
    actor_builder_line = one_line(
        "entry = make_remote_actor_entry(4, actor_identity, attrs)",
        population_start, population_end,
    )
    if EXPECTED_PORT_ROYAL_IDENTITIES != (
        0x1001, 0x1002, 0x1003, 0x1004, 0x1005, 0x1006
    ):
        raise RuntimeError("Port Royal identity manifest value/cardinality drift")
    port_royal_identity_lines = {
        value: one_line(f"(0x{value:04X},", population_start, population_end)
        for value in EXPECTED_PORT_ROYAL_IDENTITIES
    }
    if tuple(port_royal_identity_lines) != EXPECTED_PORT_ROYAL_IDENTITIES:
        raise RuntimeError("Port Royal identity example manifest drift")

    # Prove the pinned-snapshot CHitResult producer is not merely a dormant helper.
    chit_result_producer_line = 1201
    runtime_action_line = 4306
    if pinned_line("mob_combat.py", chit_result_producer_line) != (
        "payload = encode_chit_result(legacy, performer_identity, [entry])"
    ):
        raise RuntimeError("current CHitResult producer anchor drift")
    if "\"MOB_COMBAT_ANNOUNCE\", step.announce_pc" not in pinned_line(
        "runtime.py", runtime_action_line
    ):
        raise RuntimeError("current CHitResult runtime action anchor drift")

    def literal_assignment(relative: str, name: str):
        tree = ast.parse(foundation_text(relative), filename=relative)
        matches = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                if any(
                    isinstance(target, ast.Name) and target.id == name
                    for target in node.targets
                ):
                    matches.append(node.value)
            elif (
                isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == name
            ):
                matches.append(node.value)
        if len(matches) != 1:
            raise RuntimeError(
                f"expected one literal assignment {relative}:{name}"
            )
        return ast.literal_eval(matches[0])

    generated_rows = literal_assignment(
        "field_mob_tables_bg0002.py", "HOSTILE_PLACEMENTS"
    )
    ai_rows = literal_assignment("field_mob_ai_tables.py", "AI_WANDER_ROWS")
    refused_by_scene = literal_assignment(
        "field_mobs.py", "OWNER_REFUSED_PLACEMENTS"
    )
    generated_ai = Counter(row[9] for row in generated_rows)
    refused = set(refused_by_scene["Bg0002"])
    live_rows = tuple(row for row in generated_rows if row[0] not in refused)
    live_ai = Counter(row[9] for row in live_rows)
    if generated_ai != Counter({16: 12, 11: 5}):
        raise RuntimeError("Bg0002 generated AI_WANDER census drift")
    if live_ai != Counter({16: 12}):
        raise RuntimeError("Bg0002 post-owner-filter live AI_WANDER census drift")
    if ai_rows[16][2] != 0 or ai_rows[11][2] != 1:
        raise RuntimeError("AI_WANDER n_OFFESIVE anchors drift")

    # Lines in lane_a_scene_census still say scenes 4/10 are closed, while the
    # pinned registry says both are now open.  Record, do not repair, that debt.
    if "Scene 4's registry row stays ``login_entry_allowed:" not in pinned_line(
        "lane_hooks/lane_a_scene_census.py", 181
    ):
        raise RuntimeError("scene-4 stale-comment anchor drift")
    if "Scene 10's registry row stays ``login_entry_allowed: false``" not in pinned_line(
        "lane_hooks/lane_a_scene_census.py", 195
    ):
        raise RuntimeError("scene-10 stale-comment anchor drift")
    registry = json.loads(
        project_bytes("scenarios/world_scene_registry_001.json").decode("utf-8")
    )
    registry_open = {
        row["n_id"]: row.get("login_entry_allowed")
        for row in registry["destinations"] if row["n_id"] in (4, 10)
    }
    if registry_open != {4: True, 10: True}:
        raise RuntimeError("scene-4/10 registry-open check drift")

    manifest_lines = [
        f"{relative}\t{size}\t{digest}"
        for relative, (size, digest) in sorted(foundation_snapshot.items())
    ]
    pin_lines = [
        f"{relative}\t{size}\t{digest}"
        for relative, (size, digest) in sorted(PROJECT_SOURCE_PIN_ROWS.items())
    ]
    return {
        "snapshot_commit": PROJECT_SNAPSHOT_COMMIT,
        "snapshot_commit_time": PROJECT_SNAPSHOT_COMMIT_TIME,
        "size": str(len(raw)),
        "sha256": sha256_bytes(raw),
        "qword_pack_line": str(qword_pack_line),
        "npc_identity_line": str(npc_identity_line),
        "actor_entry_identity_line": str(actor_entry_identity_line),
        "npc_builder_line": str(npc_builder_line),
        "actor_builder_line": str(actor_builder_line),
        "positive_examples": (
            f"0x{EXPECTED_PORT_ROYAL_IDENTITIES[0]:04X}.."
            f"0x{EXPECTED_PORT_ROYAL_IDENTITIES[-1]:04X}"
        ),
        "population_size": str(len(sources[POPULATION_PATH])),
        "population_sha256": sha256_bytes(sources[POPULATION_PATH]),
        "field_mobs_size": str(len(sources[FIELD_MOBS_PATH])),
        "field_mobs_sha256": sha256_bytes(sources[FIELD_MOBS_PATH]),
        "world_population_size": str(len(sources[WORLD_POPULATION_PATH])),
        "world_population_sha256": sha256_bytes(sources[WORLD_POPULATION_PATH]),
        "runtime_size": str(len(sources[RUNTIME_PATH])),
        "runtime_sha256": sha256_bytes(sources[RUNTIME_PATH]),
        "chit_result_producer_line": str(chit_result_producer_line),
        "runtime_action_line": str(runtime_action_line),
        "foundation_snapshot": json.dumps(
            foundation_snapshot, sort_keys=True, separators=(",", ":")
        ),
        "foundation_file_count": str(len(foundation_snapshot)),
        "foundation_manifest_sha256": sha256_bytes(
            "\n".join(manifest_lines).encode("utf-8")
        ),
        "project_pin_count": str(len(PROJECT_SOURCE_PIN_ROWS)),
        "project_pin_manifest_sha256": sha256_bytes(
            "\n".join(pin_lines).encode("utf-8")
        ),
        "generated_bg0002_count": str(len(generated_rows)),
        "live_bg0002_count": str(len(live_rows)),
    }


def parse_palette() -> tuple[
    dict[int, dict[str, str]], dict[int, int], dict[str, object]
]:
    tree = ET.parse(FONT_STYLE_PATH)
    root = tree.getroot()
    if root.tag != EXPECTED_FONT_STYLE_ROOT:
        raise RuntimeError(
            f"BigFontStyle root mismatch: expected {EXPECTED_FONT_STYLE_ROOT}, got {root.tag}"
        )
    style_elements = root.findall("FontStyle")
    all_style_ids = tuple(int(element.attrib["ID"]) for element in style_elements)
    if all_style_ids != EXPECTED_FONT_STYLE_IDS:
        raise RuntimeError("BigFontStyle exact ordered ID census mismatch")
    if len(set(all_style_ids)) != len(all_style_ids):
        raise RuntimeError("BigFontStyle contains duplicate IDs")
    observed: dict[int, dict[str, str]] = {}
    for element in style_elements:
        style_id = int(element.attrib["ID"])
        if style_id in EXPECTED_PALETTE:
            observed[style_id] = {
                "FontColor": element.attrib.get("FontColor", ""),
                "OutlineEffectColor": element.attrib.get(
                    "OutlineEffectColor", ""
                ),
            }
    if set(observed) != set(EXPECTED_PALETTE):
        raise RuntimeError("required FontStyle IDs are missing")
    for style_id, expected in EXPECTED_PALETTE.items():
        for attribute in ("FontColor", "OutlineEffectColor"):
            if observed[style_id][attribute] != expected[attribute]:
                raise RuntimeError(
                    f"FontStyle {style_id} {attribute} mismatch"
                )

    line_numbers: dict[int, int] = {}
    lines = FONT_STYLE_PATH.read_text(encoding="utf-8").splitlines()
    for style_id in EXPECTED_PALETTE:
        marker = f'FontStyle ID="{style_id}"'
        matches = [
            line_number
            for line_number, line in enumerate(lines, start=1)
            if marker in line
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"expected one DATA line for FontStyle {style_id}, got {len(matches)}"
            )
        line_numbers[style_id] = matches[0]
    return observed, line_numbers, {
        "root_tag": root.tag,
        "style_count": len(all_style_ids),
        "minimum_style_id": min(all_style_ids),
        "maximum_style_id": max(all_style_ids),
        "ordered_style_ids": all_style_ids,
        "required_palette_ids": tuple(sorted(EXPECTED_PALETTE)),
        "required_palette": observed,
    }


def parse_rgba_text(value: str) -> tuple[int, int, int, int]:
    parsed = ast.literal_eval(value)
    if (
        not isinstance(parsed, tuple)
        or len(parsed) != 4
        or any(not isinstance(component, int) for component in parsed)
        or any(not 0 <= component <= 255 for component in parsed)
    ):
        raise RuntimeError(f"invalid pinned RGBA tuple: {value}")
    return parsed


def normalized_float32_rgba(value: str, divisor: float) -> str:
    if divisor != 255.0:
        raise RuntimeError("unsupported RGBA normalization divisor")
    components = []
    for component in parse_rgba_text(value):
        normalized = max(0.0, min(1.0, float(component) / divisor))
        rounded = struct.unpack("<f", struct.pack("<f", normalized))[0]
        components.append(format(rounded, ".9g"))
    return "(" + ", ".join(components) + ")"


def span_columns(span_name: str) -> dict[str, str]:
    start_va, end_va, span_hash = SPANS[span_name]
    start_offset = va_to_offset(start_va)
    end_offset = start_offset + (end_va - start_va)
    return {
        "span_start_va": fmt_va(start_va),
        "span_end_va": fmt_va(end_va),
        "file_off_start": fmt_va(start_offset),
        "file_off_end": fmt_va(end_offset),
        "span_sha256": span_hash,
    }


def support_text(span_names: Iterable[str]) -> str:
    parts = []
    for name in span_names:
        start_va, end_va, span_hash = SPANS[name]
        start_offset = va_to_offset(start_va)
        end_offset = start_offset + (end_va - start_va)
        parts.append(
            f"{name}=VA:{fmt_va(start_va)}..{fmt_va(end_va)}"
            f"@file:{fmt_va(start_offset)}..{fmt_va(end_offset)}"
            f"@sha256:{span_hash}"
        )
    return ";".join(parts)


def evidence_key(row: Mapping[str, str]) -> str:
    values = [row[name] for name in FIELDNAMES if name != "evidence_key"]
    return hashlib.sha256("\x1f".join(values).encode("utf-8")).hexdigest()


def make_image_row(
    gate_key: str,
    row_kind: str,
    owner_type: str,
    applies_to_class: str,
    input_field: str,
    runtime_field: str,
    condition: str,
    output: str,
    semantic_status: str,
    producer_va: str,
    consumer_va: str,
    span_name: str,
    support: Sequence[str] = (),
    canonical_keys: Sequence[str] = (),
    server_status: str = "NOT_APPLICABLE",
    nonclaim: str = "",
    blocker: str = "",
    required_next_evidence: str = "",
) -> dict[str, str]:
    row = {
        "gate_key": gate_key,
        "row_kind": row_kind,
        "owner_type": owner_type,
        "applies_to_class": applies_to_class,
        "input_field": input_field,
        "runtime_field": runtime_field,
        "condition": condition,
        "output": output,
        "semantic_status": semantic_status,
        "producer_va": producer_va,
        "consumer_va": consumer_va,
        **span_columns(span_name),
        "support_spans": support_text(support),
        "canonical_selector_keys": ";".join(canonical_keys),
        "current_server_emit_status": server_status,
        "source": "IMAGE",
        "source_file": IMAGE_SOURCE,
        "source_locator": "",
        "source_sha256": IMAGE_SHA256,
        "nonclaim": "[MEASURED]" + (f" {nonclaim}" if nonclaim else ""),
        "blocker": blocker,
        "required_next_evidence": required_next_evidence,
        "evidence_key": "",
    }
    row["evidence_key"] = evidence_key(row)
    return row


def make_data_row(
    gate_key: str,
    style_id: int,
    observed: Mapping[str, str],
    line_number: int,
) -> dict[str, str]:
    expected = EXPECTED_PALETTE[style_id]
    row = {
        "gate_key": gate_key,
        "row_kind": "DATA_PALETTE",
        "owner_type": "BigFontStyle.FontStyle",
        "applies_to_class": "UILabel_FontStyleID",
        "input_field": f"FontStyle.ID={style_id}",
        "runtime_field": "FontColor;OutlineEffectColor",
        "condition": f"FontStyle.ID={style_id}",
        "output": (
            f"label={expected['label']};FontColor={observed['FontColor']};"
            f"OutlineEffectColor={observed['OutlineEffectColor']}"
        ),
        "semantic_status": "PROVEN_EXACT",
        "producer_va": "",
        "consumer_va": "",
        "span_start_va": "",
        "span_end_va": "",
        "file_off_start": "",
        "file_off_end": "",
        "span_sha256": "",
        "support_spans": "",
        "canonical_selector_keys": "",
        "current_server_emit_status": "NOT_APPLICABLE",
        "source": "DATA",
        "source_file": FONT_STYLE_SOURCE,
        "source_locator": f"line={line_number};FontStyle.ID={style_id}",
        "source_sha256": FONT_STYLE_SHA256,
        "nonclaim": (
            "[MEASURED] The human color label is descriptive; the RGBA tuples are exact."
        ),
        "blocker": "",
        "required_next_evidence": "",
        "evidence_key": "",
    }
    row["evidence_key"] = evidence_key(row)
    return row


def build_rows(
    palette: Mapping[int, Mapping[str, str]],
    line_numbers: Mapping[int, int],
    selector_rows: Sequence[Mapping[str, str]],
    image_facts: Mapping[str, object],
    palette_facts: Mapping[str, object],
) -> list[dict[str, str]]:
    server_boundary = "SEE_MD_SEPARATE_PROJECT_CHECK_NOT_TSV_EVIDENCE"
    rows: list[dict[str, str]] = []
    selector_by_key = {row["selector_key"]: row for row in selector_rows}
    style_path_literal = str(image_facts["style_path_literal"])
    style_path_literal_va = int(image_facts["style_path_literal_va"])
    style_id_attribute = str(image_facts["style_id_attribute"])
    style_id_attribute_va = int(image_facts["style_id_attribute_va"])
    style_manager_va = int(image_facts["style_manager_va"])
    style_loader_va = int(image_facts["style_loader_va"])
    style_loader_call_sites = tuple(
        int(value) for value in image_facts["style_loader_call_sites"]
    )
    style_outer_init_va = int(image_facts["style_outer_init_va"])
    style_outer_init_call_sites = tuple(
        int(value) for value in image_facts["style_outer_init_call_sites"]
    )
    style_id_conversion_import = str(image_facts["style_id_conversion_import"])
    style_id_lower_exclusive = int(image_facts["style_id_lower_exclusive"])
    style_id_accept_relation = str(image_facts["style_id_accept_relation"])
    cnetnpc_slot38_target = int(image_facts["cnetnpc_slot38_target"])
    ready_zero_call_target = int(image_facts["ready_zero_call_target"])
    ready_zero_requested_byte = int(image_facts["ready_zero_requested_byte"])
    font_color_property = str(image_facts["font_color_property"])
    font_color_property_va = int(image_facts["font_color_property_va"])
    outline_color_property = str(image_facts["outline_color_property"])
    outline_color_property_va = int(image_facts["outline_color_property_va"])
    label_fontstyle_id_property = str(image_facts["label_fontstyle_id_property"])
    label_fontstyle_id_property_va = int(
        image_facts["label_fontstyle_id_property_va"]
    )
    embedded_fontstyle_property = str(image_facts["embedded_fontstyle_property"])
    embedded_fontstyle_property_va = int(
        image_facts["embedded_fontstyle_property_va"]
    )
    style_property_parser_va = int(image_facts["style_property_parser_va"])
    style_property_parser_call_sites = tuple(
        int(value) for value in image_facts["style_property_parser_call_sites"]
    )
    rgba_property_wrapper_va = int(image_facts["rgba_property_wrapper_va"])
    rgba_normalized_parser_va = int(image_facts["rgba_normalized_parser_va"])
    rgba_divisor_va = int(image_facts["rgba_divisor_va"])
    rgba_divisor = float(image_facts["rgba_divisor"])
    label_numeric_conversion_va = int(image_facts["label_numeric_conversion_va"])
    label_empty_sentinel_va = int(image_facts["label_empty_sentinel_va"])
    label_zero_dispatch_va = int(image_facts["label_zero_dispatch_va"])
    label_zero_dispatch_id = int(image_facts["label_zero_dispatch_id"])
    label_embedded_style_getter_va = int(
        image_facts["label_embedded_style_getter_va"]
    )
    label_style_lookup_va = int(image_facts["label_style_lookup_va"])
    label_style_apply_va = int(image_facts["label_style_apply_va"])
    label_font_color_setter_va = int(image_facts["label_font_color_setter_va"])
    label_outline_color_setter_va = int(
        image_facts["label_outline_color_setter_va"]
    )
    pe_section_count = int(image_facts["pe_section_count"])
    pe_section_names = tuple(str(value) for value in image_facts["pe_section_names"])
    pe_section_file_backed_bounds = tuple(
        (str(name), int(va_start), int(va_end), int(raw_start), int(raw_end))
        for name, va_start, va_end, raw_start, raw_end
        in image_facts["pe_section_file_backed_bounds"]
    )
    expected_section_bounds = tuple(
        (
            name,
            section_va,
            section_va + min(virtual_size, raw_size),
            raw_offset,
            raw_offset + min(virtual_size, raw_size),
        )
        for name, section_va, virtual_size, raw_offset, raw_size in SECTIONS
    )
    pe_section_bounds_text = ",".join(
        f"{name}:VA{fmt_va(va_start)}..{fmt_va(va_end)}"
        f"@file{fmt_va(raw_start)}..{fmt_va(raw_end)}"
        for name, va_start, va_end, raw_start, raw_end
        in pe_section_file_backed_bounds
    )
    palette_ids = tuple(int(value) for value in palette_facts["ordered_style_ids"])
    required_palette_ids = tuple(
        int(value) for value in palette_facts["required_palette_ids"]
    )
    if (
        style_loader_call_sites != (0x004086E6,)
        or style_outer_init_call_sites != (0x0040A2E9,)
        or style_id_lower_exclusive != 0
        or style_id_accept_relation != "signed_greater_than"
        or font_color_property != "FontColor"
        or outline_color_property != "OutlineEffectColor"
        or label_fontstyle_id_property != "FontStyleID"
        or embedded_fontstyle_property != "FontStyle"
        or style_property_parser_call_sites != (0x00A9FA11, 0x00AA490D)
        or rgba_divisor != 255.0
        or label_zero_dispatch_id != 0
        or pe_section_count != 6
        or pe_section_names != (".text", ".code", ".rdata", ".data", ".rsrc", ".reloc")
        or pe_section_file_backed_bounds != expected_section_bounds
        or palette_ids != EXPECTED_FONT_STYLE_IDS
        or required_palette_ids != tuple(sorted(EXPECTED_PALETTE))
    ):
        raise RuntimeError("verified style facts changed before row construction")

    def add(
        key: str,
        kind: str,
        owner: str,
        applies: str,
        input_field: str,
        runtime_field: str,
        condition: str,
        output: str,
        status: str,
        producer: str,
        consumer: str,
        span: str,
        *,
        support: Sequence[str] = (),
        canonical: Sequence[str] = (),
        server: str = "NOT_APPLICABLE",
        nonclaim: str = "",
        blocker: str = "",
        next_evidence: str = "",
    ) -> None:
        rows.append(
            make_image_row(
                key,
                kind,
                owner,
                applies,
                input_field,
                runtime_field,
                condition,
                output,
                status,
                producer,
                consumer,
                span,
                support=support,
                canonical_keys=canonical,
                server_status=server,
                nonclaim=nonclaim,
                blocker=blocker,
                required_next_evidence=next_evidence,
            )
        )

    add(
        "MCG-IMG-001", "TYPE_IDENTITY", "CNetNPC", "CNetNPC",
        "RTTI_descriptor_0x0101B138", "", "decorated_RTTI_name_is_exact",
        "class=CNetNPC", "PROVEN_EXACT", "", "", "CNetNPC_rtti",
    )
    add(
        "MCG-IMG-002", "TYPE_FACTORY", "actor_type_factory", "CNetNPC",
        "actor_entry+0x10_u8=4", "factory_branch_0x00446A3D",
        "jump_table_index_actor_type_minus_2_equals_2",
        "CNetNPC_type_node_0x0102D938_factory_call", "PROVEN_EXACT",
        "0x004469C8", "0x00446A53", "actor_factory",
        support=("CNetNPC_rtti", "CNetNPC_type_node_ctor", "CNetNPC_type_node_anchor"),
        nonclaim="This proves actor type 4 builds CNetNPC; it does not name actor type 4 monster.",
    )
    add(
        "MCG-IMG-003", "VTABLE_BRIDGE", "CNetNPC", "CNetNPC",
        "vtable_0x00F0DF58_slot_0x10", "initializer_0x0045D200",
        "dword_at_vtable_plus_0x10_equals_0x0045D200", "typed_CNetNPC_initializer",
        "PROVEN_EXACT", "0x00F0DF68", "0x0045D200", "CNetNPC_vtable_prefix",
        support=("CNetNPC_rtti",),
    )
    add(
        "MCG-IMG-004", "ACTOR_ENTRY_WIRE_WRITE", "RuntimeResActorEntry_structural",
        "GSCN_RunTimeProtocolRes.actor_entry", "record+0x18..0x1F",
        "wire_order=2;tag=0x32;len=8", "serializer_WRITE_branch",
        "one_complete_qword", "PROVEN_EXACT", "0x005E2232", "0x0089A600",
        "actor_entry_qword_write", support=("actor_entry_codec_prefix",),
        server=server_boundary,
        nonclaim="The concrete C++ RTTI name of this structural record is not established.",
    )
    add(
        "MCG-IMG-005", "ACTOR_ENTRY_WIRE_READ", "RuntimeResActorEntry_structural",
        "GSCN_RunTimeProtocolRes.actor_entry", "wire_order=2;tag=0x32;len=8",
        "record+0x18_low_dword;record+0x1C_high_dword", "serializer_READ_branch",
        "all_eight_bytes_populated", "PROVEN_EXACT", "0x0089A640", "0x005E230C",
        "actor_entry_qword_read", support=("actor_entry_codec_prefix",),
        server=server_boundary,
        nonclaim="This qword is the actor-entry identity, not the inherited BasicAttr identity.",
    )
    add(
        "MCG-IMG-006", "RUNTIMERES_DISPATCH", "GSCN_RunTimeProtocolRes",
        "actor_entry_collection", "response+0x1C_object;+0x10_list_head",
        "actor_reconcile_0x00446F30", "derived_actor_collection_present",
        "collection_list_passed_to_reconcile", "PROVEN_EXACT", "0x005E4073",
        "0x005E4085", "runtime_res_handler",
        support=("actor_entry_codec_prefix", "actor_reconcile"), server=server_boundary,
    )
    add(
        "MCG-IMG-007", "ACTOR_ENTRY_IDENTITY_LOOKUP", "actor_reconcile",
        "RuntimeResActorEntry_structural", "record+0x18_low;record+0x1C_high",
        "actor_registry_lookup_arguments", "list_node_payload_record_is_nonnull",
        "same_qword_keys_lookup_and_spawn_decision", "PROVEN_EXACT", "0x00446F87",
        "0x00446F91", "reconcile_identity_factory", support=("actor_reconcile",),
        server=server_boundary,
    )
    add(
        "MCG-IMG-008", "FACTORY_POINTER_FLOW", "actor_factory",
        "CNetNPC_when_actor_type_4", "same_pointer_to_RuntimeResActorEntry",
        "CNetNPC_vslot_0x10_argument", "identity_lookup_miss_and_actor_type_4",
        "same_record_pointer_reaches_initializer", "PROVEN_EXACT", "0x00446A92",
        "0x00446AB5", "factory_entry_to_init",
        support=("actor_factory", "reconcile_identity_factory", "CNetNPC_type_node_ctor"),
        server=server_boundary,
    )
    for key, source_field, runtime_field, producer, consumer in (
        ("MCG-IMG-009", "actor_entry+0x18_low_dword", "CNetNPC+0x78_low_dword", "0x0045D23B", "0x0045D241"),
        ("MCG-IMG-010", "actor_entry+0x1C_high_dword", "CNetNPC+0x7C_high_dword", "0x0045D23E", "0x0045D244"),
    ):
        add(
            key, "BRIDGE_COPY", "RuntimeResActorEntry_structural", "CNetNPC",
            source_field, runtime_field,
            "CNetNPC_vslot_0x10_receives_same_actor_entry_pointer", "raw_dword_copy",
            "PROVEN_EXACT", producer, consumer, "bridge_copy_notify",
            support=("factory_entry_to_init", "actor_entry_qword_read", "CNetNPC_vtable_prefix"),
            server=server_boundary,
            nonclaim="This copy does not read BasicAttr or CreateActorDataEx.",
        )
    add(
        "MCG-IMG-011", "SIGNED_IDENTITY_GATE", "selector_receiver_structural", "selector_receiver",
        "actor+0x78_low;actor+0x7C_signed_high", "positive_selector_lane",
        "signed_high>0_OR_signed_high==0_AND_unsigned_low>0", "positive",
        "PROVEN_EXACT", "0x00443FFB", "0x00444017", "signed_gate",
        support=("selector_full",), server=server_boundary,
        nonclaim=(
            "Positive identity selects a family of styles inside this selector; it does not "
            "guarantee style 56. This standalone gate row does not carry the receiver-class "
            "join; MCG-IMG-025..033 and MCG-IMG-039..045 carry that separate proof."
        ),
    )
    add(
        "MCG-IMG-012", "SIGNED_IDENTITY_GATE", "selector_receiver_structural", "selector_receiver",
        "actor+0x78_low;actor+0x7C_signed_high", "nonpositive_selector_lane",
        "signed_high<0_OR_both_dwords_zero", "nonpositive", "PROVEN_EXACT",
        "0x00443FFB", "0x00444151", "signed_gate",
        support=("selector_full",), server=server_boundary,
        nonclaim=(
            "This standalone row is only the exact selector-local signed gate; the exact "
            "conditional RuntimeRes same-instance call path is recorded separately."
        ),
    )
    add(
        "MCG-IMG-013", "SEPARATE_ATTR_IDENTITY", "DBAttribute_inherited_by_BasicAttr",
        "BasicAttr_or_derived_attr_object", "attr+0x20_mask_bit_0x01",
        "attr+0x18/+0x1C_qword;tag=0x32;len=8", "base_attr_codec_mask_bit_set",
        "attribute_local_identity_qword", "PROVEN_EXACT", "0x00467790", "0x004677DD",
        "dbattribute_identity_codec", support=("basicattr_codec_prefix",),
        nonclaim="The identical numeric value may be sent in both places, but this is a different object and wire subcodec from the actor-entry qword.",
    )
    add(
        "MCG-IMG-014", "SEPARATE_ATTR_CHAIN", "BasicAttr",
        "BasicAttr_and_derived_ActorAttr_or_NPCAttr", "BasicAttr_serializer_receiver",
        "DBAttribute_identity_subcodec_0x00467790", "BasicAttr_serializer_entry",
        "calls_distinct_attribute_identity_codec_before_BasicAttr_mask", "PROVEN_EXACT",
        "0x004656F0", "0x004656FF", "basicattr_codec_prefix",
        support=("dbattribute_identity_codec",),
        nonclaim="This row does not make BasicAttr identity the actor runtime identity.",
    )
    add(
        "MCG-IMG-015", "NON_ALIAS_BOUNDARY", "CNetNPC_initializer", "CNetNPC",
        "actor_entry_identity_vs_BasicAttr_identity", "actor+0x78/+0x7C",
        "initializer_copies_actor_entry_pair_before_attr_bind_call_0x005DF080",
        "actor_entry_pair_is_stored_at_CNetNPC_plus_0x78_plus_0x7C", "PROVEN_EXACT", "0x0045D23B",
        "0x0045D24A", "bridge_copy_notify",
        support=("actor_entry_qword_read", "dbattribute_identity_codec"),
        nonclaim="No equality or inequality between the two qword values is asserted.",
    )
    add(
        "MCG-IMG-016", "SEPARATE_RECORD_TYPE", "CreateActorDataEx", "CreateActorDataEx",
        "RTTI_descriptor_0x0101F4E0", "", "decorated_RTTI_name_is_exact",
        "class=CreateActorDataEx", "PROVEN_EXACT", "", "", "CreateActorDataEx_rtti",
        nonclaim="CreateActorDataEx is not the RuntimeRes actor-entry record proved above.",
    )
    add(
        "MCG-IMG-017", "SEPARATE_RECORD_DEFAULT", "CreateActorDataEx", "CreateActorDataEx",
        "+0x18;+0x19;+0x1A;+0x1C", "", "fresh_object_constructor",
        "+0x18=0xFF;+0x19=0;+0x1A=0;+0x1C=0", "PROVEN_EXACT",
        "0x005DF1BC;0x005DF1C0;0x005DF1C3;0x005DF1C6", "", "record_ctor",
        nonclaim="The constructor does not establish CreateActorDataEx+0x1B.",
    )
    for index, wire_order, offset, tag, call_va in (
        (18, 10, 0x18, 0x0B, 0x005E0081),
        (19, 12, 0x19, 0x0B, 0x005E009B),
        (20, 13, 0x1A, 0x0B, 0x005E00AA),
        (21, 14, 0x1C, 0x19, 0x005E00B9),
    ):
        length = 4 if offset == 0x1C else 1
        add(
            f"MCG-IMG-{index:03d}", "SEPARATE_RECORD_WIRE_READ", "CreateActorDataEx",
            "CreateActorDataEx", f"wire_order={wire_order};tag=0x{tag:02X};len={length}",
            f"CreateActorDataEx+0x{offset:02X}", "codec_READ_branch", "field_populated",
            "PROVEN_EXACT", "0x0089A640", f"0x{call_va:08X}", "record_codec",
            nonclaim="This field is not an input to the proven RuntimeRes actor-entry-to-CNetNPC bridge.",
        )
    add(
        "MCG-IMG-022", "SEPARATE_RECORD_PADDING_BLOCKER", "CreateActorDataEx",
        "CreateActorDataEx", "+0x1B",
        "low_dword_byte_3_if_someone_reinterprets_+0x18_as_dword",
        "no_ctor_store_and_no_codec_field_in_complete_pinned_spans", "UNESTABLISHED",
        "PROVEN_BOUNDED_NEGATIVE", "0x005DF130;0x005DFF60", "", "record_codec",
        support=("record_ctor",),
        nonclaim="This blocker applies only to CreateActorDataEx reconstruction; RuntimeRes actor-entry READ writes all eight qword bytes including its own +0x1B.",
        blocker="CreateActorDataEx+0x1B is not established by its constructor or codec.",
        next_evidence="A complete CreateActorDataEx producer store or a separately proved zero-fill guarantee.",
    )
    add(
        "MCG-IMG-023", "SEPARATE_RECORD_ALLOCATOR_BOUNDARY",
        "CreateActorDataEx_allocation_path", "CreateActorDataEx",
        "malloc_and_placement_thunks", "CreateActorDataEx+0x1B_initial_storage",
        "malloc_import_or_placement_pointer_return", "no_zero_fill_contract",
        "PROVEN_BOUNDED_NEGATIVE", "0x0088D020", "0x0088D035", "allocator_thunks",
        support=("record_ctor",), nonclaim="This is not proof that every observed byte is nonzero.",
        blocker="A zero value for CreateActorDataEx+0x1B cannot be assumed.",
        next_evidence="An exact zeroing caller or producer store for the relevant object.",
    )
    add(
        "MCG-IMG-024", "RECORD_SEPARATION", "RuntimeResActorEntry_vs_CreateActorDataEx",
        "CNetNPC_runtime_spawn_path", "two_distinct_codecs_0x005E21D0_and_0x005DFF60",
        "CNetNPC+0x78/+0x7C",
        "RuntimeRes_handler_to_reconcile_to_factory_to_CNetNPC_initializer",
        "RuntimeRes_actor_entry_qword_populates_CNetNPC_identity_fields", "PROVEN_EXACT", "0x005E230C",
        "0x0045D244", "actor_entry_qword_read",
        support=("runtime_res_handler", "actor_reconcile", "factory_entry_to_init", "bridge_copy_notify", "record_codec"),
        nonclaim=(
            "CreateActorDataEx field meanings and its +0x1B blocker do not govern this "
            "RuntimeRes-to-CNetNPC storage path. This storage row alone does not carry the "
            "registry/selector edge proved separately by MCG-IMG-039..045."
        ),
    )

    crosswalks = (
        (25, 56, "positive_style_56", "0x00444039", "selector_full",
         "Positive identity alone does not prove the relationship predicate is false."),
        (26, 58, "positive_style_58", "0x00444071", "selector_full", ""),
        (27, 59, "positive_style_59", "0x00444113", "selector_full", ""),
        (28, 57, "positive_style_57", "0x0044414A", "selector_full", ""),
        (29, 60, "yellow_relation", "0x0044417E", "selector_full", ""),
        (30, 63, "gray_death", "0x0044419F", "selector_full",
         "FontStyleID 63 also has canonical causes other than this death predicate."),
        (31, 61, "red_offensive", "0x00444234", "typed_color_tail",
         "This path does not read n_AGGRO and style 61 has other causes."),
        (32, 61, "red_latched", "0x00444263", "typed_color_tail",
         "The unnamed runtime bit is not named aggro or hostile."),
        (33, 62, "orange_clear", "0x00444270", "typed_color_tail", ""),
    )
    for index, style_id, canonical_name, consumer, span, local_nonclaim in crosswalks:
        canonical_key = CANONICAL_KEYS[canonical_name]
        canonical_row = selector_by_key[canonical_key]
        support = [
            "actor_entry_qword_read", "factory_entry_to_init", "bridge_copy_notify",
            "singleton_getter", "manager_tick_callsite", "factory_register_path",
            "registry_insert", "registry_tree_insert", "registry_tree_emplace",
            "registry_node_copy", "manager_tick_iteration", "actor_update_selector_call",
            "CNetNPC_vtable_through_nameboard", "CNetNPC_nameboard_create",
            "CNetNPC_selector_readiness",
            "NPC_nameboard_controller_ctor_prefix", "NPC_nameboard_backpointer",
            "NPC_nameboard_vtable", "NPC_nameboard_bind_label",
            "NPC_controller_style_store", "NPC_LABEL_NAME_style_apply", "signed_gate",
        ]
        if canonical_name == "gray_death":
            support.append("death_predicate")
        if canonical_name == "red_offensive":
            support.append("ai_offensive")
        if canonical_name in {"red_latched", "orange_clear"}:
            support.append("bit_selector")
        nonclaim_parts = [
            "The IMAGE path is conditional on registry retention, controller allocation/binding, "
            "actor+0x254 nonnull, actor+0x258 and actor+0x260 nonzero, and control flow reaching "
            "the selector call; it does not prove those gates pass for every frame.",
            "It does not prove original-server identity policy, live predicate values, delivery, "
            "or a rendered screen color.",
            "The canonical standalone row's former owner-class uncertainty is closed only for "
            "this RuntimeRes-spawned type-4 CNetNPC join.",
            local_nonclaim,
        ]
        add(
            f"MCG-IMG-{index:03d}", "TYPED_SELECTOR_CROSSWALK",
            "RuntimeRes_spawned_CNetNPC_same_instance",
            "CNetNPC_with_bound_NPC_nameboard_controller",
            "RuntimeRes_actor_entry_identity_to_same_CNetNPC_selector_receiver;"
            + canonical_row["condition"],
            f"FontStyleID={style_id}",
            f"same_instance_runtime_actor_reaches_{canonical_name}_when_all_call_and_selector_gates_hold",
            f"reaches_canonical_{canonical_name}",
            "PROVEN_EXACT", "0x005E230C", consumer, span,
            support=tuple(support), canonical=(canonical_key,), server=server_boundary,
            nonclaim=" ".join(value for value in nonclaim_parts if value),
        )

    add(
        "MCG-IMG-034", "DEATH_PREDICATE", "shared_actor_predicate",
        "CNetNPC_vtable_slot_0x3C", "BasicAttr+0x44;BasicAttr+0x58",
        "boolean_death_state", "current_HP==0_AND_ordered_float_at_0x58<=0", "true",
        "PROVEN_EXACT", "0x0043BD70", "0x0043BD9C", "death_predicate",
        support=("CNetNPC_vtable_core",),
        nonclaim=(
            "This shared predicate does not classify monster versus NPC and does not "
            "by itself prove selector invocation or style emission; the joined death-to-style "
            "path is the separate typed crosswalk MCG-IMG-030."
        ),
    )
    add(
        "MCG-IMG-035", "RUNTIME_BIT_INIT", "common_actor", "CNetNPC_inherited_runtime_state",
        "actor+0x70_dword", "actor+0x70_bit_0x100", "common_actor_construction",
        "cleared_by_whole_dword_zero", "PROVEN_EXACT", "0x00443199", "",
        "common_actor_ctor", nonclaim="No gameplay noun is assigned to bit 0x100.",
    )
    for index, owner, producer, consumer, span in (
        (36, "CHitResult_resolved_target_actor", "0x00750896", "0x007508D0", "hit_bit_writer"),
        (37, "CMissileHitResult_resolved_target_actor", "0x007511A6", "0x007511E0", "missile_bit_writer"),
    ):
        add(
            f"MCG-IMG-{index:03d}", "RUNTIME_BIT_WRITER", owner,
            "generic_actor_target;typed_CNetNPC_not_proven_at_writer",
            "hit_entry_target_identity;source_actor", "target_actor+0x70_bit_0x100",
            "target_exists;target+0x10_bit0x10000_set;target_identity_high_signed_negative;source_casts_to_CMyActor",
            "set", "PROVEN_ROLE_ONLY", producer, consumer, span,
            nonclaim="This writer does not prove the target is CNetNPC and does not name the bit aggro.",
        )
    add(
        "MCG-IMG-038", "RUNTIME_BIT_CONSUME_CLEAR", "CNetNPC_runtime_actor", "CNetNPC",
        "actor+0x70_bit_0x100", "actor+0x70_bit_0x100",
        "bit_set_AND_either_local_vslot_0x3C_or_0x40_true",
        "clear_without_new_style_emit_in_this_branch", "PROVEN_EXACT", "0x00444238",
        "0x00444267", "bit_selector",
        canonical=(CANONICAL_KEYS["red_latched"], CANONICAL_KEYS["orange_clear"]),
        nonclaim="The clear path does not prove the gameplay noun of the bit.",
    )

    add(
        "MCG-IMG-039", "SINGLETON_MANAGER_JOIN", "actor_manager_singleton",
        "RuntimeRes_reconcile_and_periodic_actor_tick",
        "direct_calls_0x005E407E_and_0x00406196_to_0x00402A20",
        "singleton_address_0x0102C6C0",
        "getter_returns_the_same_absolute_manager_address_to_both_callers",
        "same_manager_receiver_for_reconcile_0x00446F30_and_tick_0x00445480",
        "PROVEN_EXACT", "0x005E407E;0x00406196", "0x00402A72",
        "singleton_getter",
        support=("runtime_res_handler", "manager_tick_callsite", "manager_tick_iteration"),
        nonclaim="This row joins manager identity; it does not assert that every actor survives registry removal.",
    )
    add(
        "MCG-IMG-040", "FACTORY_REGISTRY_JOIN", "actor_factory", "spawned_CNetNPC",
        "factory_actor_pointer_ESI_and_actor_entry_identity_qword",
        "manager_plus_0x0C_registry_insert_arguments",
        "RuntimeRes_lookup_miss_calls_factory_with_registration_flag_1",
        "same_spawned_actor_pointer_and_entry_key_pass_to_0x00446090",
        "PROVEN_EXACT", "0x00446F9C;0x00446A9A", "0x00446AA8",
        "factory_register_path",
        support=("reconcile_identity_factory", "actor_factory", "registry_insert"),
        nonclaim="Allocation or initializer failure is not claimed to produce a usable visible actor.",
    )
    add(
        "MCG-IMG-041", "REGISTRY_NODE_LAYOUT", "actor_manager_plus_0x0C_tree",
        "registered_actor_tree_node",
        "insert_value_key_low_key_high_actor_pointer",
        "node_plus_0x10_key_low;plus_0x14_key_high;plus_0x18_actor_pointer",
        "tree_insert_reaches_node_constructor_0x006F40D0",
        "exact_value_copy_and_actor_reference_retain",
        "PROVEN_EXACT", "0x00446110;0x006F4130", "0x006F4145",
        "registry_node_copy",
        support=("registry_insert", "registry_tree_insert", "registry_tree_emplace"),
        nonclaim="This proves the direct insertion path and node layout, not an exhaustive registry lifetime policy.",
    )
    add(
        "MCG-IMG-042", "MANAGER_TICK_DISPATCH", "actor_manager_plus_0x0C_tree",
        "registered_actor_pointer",
        "tree_node_plus_0x18_actor_pointer", "call_receiver_ECX",
        "periodic_tick_iterates_a_non_sentinel_node_and_actor_pointer_is_nonnull",
        "same_node_payload_pointer_calls_actor_updater_0x00444400",
        "PROVEN_EXACT", "0x004454ED", "0x004454F4",
        "manager_tick_iteration",
        support=("singleton_getter", "manager_tick_callsite", "registry_node_copy"),
        nonclaim="This is a conditional dispatch edge; scheduling frequency and runtime retention remain outside the row.",
    )
    add(
        "MCG-IMG-043", "SAME_RECEIVER_SELECTOR_CALL", "registered_CNetNPC_actor",
        "selector_receiver",
        "updater_ECX_actor_pointer", "selector_ECX_same_actor_pointer",
        "updater_preserves_ESI_equals_ECX_and_reaches_actor_plus_0x258_plus_0x260_gates",
        "0x004446A5_moves_ESI_to_ECX_then_direct_calls_0x00443F50",
        "PROVEN_EXACT", "0x00444404", "0x004446A7",
        "actor_update_selector_call",
        support=("manager_tick_iteration", "selector_full", "CNetNPC_selector_readiness"),
        nonclaim="The exact pointer edge does not assert that +0x258/+0x260 or earlier updater gates pass on every frame.",
    )
    add(
        "MCG-IMG-044", "NAMEBOARD_CONTROLLER_BIND", "CNetNPC", "NPC_nameboard_controller",
        "same_CNetNPC_actor_pointer", "actor_plus_0x254_controller;controller_plus_0x30_actor;controller_plus_0x50_LABEL_NAME",
        "CNetNPC_vslot_0x7C_create_succeeds_and_controller_binder_resolves_children",
        "controller_vtable_0x00F2CD48_is_owned_by_same_actor_and_binds_LABEL_NAME",
        "PROVEN_EXACT", "0x0045D3EA;0x0045C583", "0x005BE760",
        "CNetNPC_nameboard_create",
        support=("CNetNPC_vtable_through_nameboard", "NPC_nameboard_controller_ctor_prefix",
                 "NPC_nameboard_backpointer", "NPC_nameboard_vtable", "NPC_nameboard_bind_label"),
        nonclaim="Allocation/binding failure remains a runtime gate; no successful screen render is asserted.",
    )
    add(
        "MCG-IMG-045", "CONTROLLER_STYLE_STORE", "NPC_nameboard_controller",
        "same_CNetNPC_nameboard_style_state",
        "selector_selected_FontStyleID", "controller_plus_0x34",
        "selector_loads_same_actor_plus_0x254_and_dispatches_controller_vslot_plus_0x34",
        "0x009F1A70_stores_the_selected_id_at_controller_plus_0x34",
        "PROVEN_EXACT", "0x0044401D;0x00444272", "0x009F1A74",
        "NPC_controller_style_store",
        support=("selector_full", "NPC_nameboard_vtable", "NPC_nameboard_bind_label",
                 "NPC_LABEL_NAME_style_apply", "actor_update_selector_call"),
        nonclaim="The store is exact; visible UI refresh and the observed color remain runtime questions.",
    )
    add(
        "MCG-IMG-046", "MODEL_READY_BIT_PRODUCER", "CNetNPC_model_callback",
        "same_CNetNPC_actor",
        "CNetNPC_vtable_plus_0x58_callback_argument",
        "actor_plus_0x80_model_pointer;actor_plus_0x70_bit_0x40",
        "callback_invoked_with_nonnull_argument;argument_plus_0x48_nonnull;"
        "dereferenced_resource_plus_0x08_nonnull;normal_callback_flow_completes",
        "installs_argument_plus_0x48_at_actor_plus_0x80_and_sets_bit_0x40",
        MANUAL_HASH_STATUS, "0x0045CDAD;0x004447B7;0x004448B4", "0x0045C535",
        "common_model_callback",
        support=("CNetNPC_vtable_through_nameboard", "CNetNPC_model_callback",
                 "CNetNPC_selector_readiness", "common_actor_ctor"),
        nonclaim=(
            "IMAGE proves the conditional callback body and CNetNPC wrapper, not that a live "
            "resource request schedules or completes the callback. Null callback/resource gates "
            "leave bit 0x40 clear; the bit is readiness state, not visible geometry or pixels. "
            + MANUAL_HASH_NONCLAIM
        ),
    )
    add(
        "MCG-IMG-047", "NAMEBOARD_READY_BYTE", "common_actor_and_CNetNPC_init",
        "same_CNetNPC_actor",
        "nameboard_create_result;actor_plus_0x10_bit_0x4000;actor_plus_0x80_plus_0x74",
        "actor_plus_0x258_byte",
        "init_sets_one_after_allowed_vslot_0x7C_success;each_non_mode_6_common_update_"
        "then_forces_zero_for_bit_0x4000_or_copies_model_plus_0x74_with_null_as_zero",
        "dynamic_readiness_byte_not_a_permanent_init_latch",
        MANUAL_HASH_STATUS, "0x0045D418;0x0044377F;0x00443799", "0x00444693",
        "common_actor_update",
        support=("CNetNPC_init_full", "CNetNPC_nameboard_create",
                 "CNetNPC_model_callback", "common_model_callback"),
        nonclaim=(
            "Global mode 6 skips the refresh and preserves the prior byte. Controller creation, "
            "model presence, and model+0x74 are runtime gates; +0x258 alone is not a render result. "
            + MANUAL_HASH_NONCLAIM
        ),
    )
    add(
        "MCG-IMG-048", "DELAYED_READY_LATCH", "CNetNPC_update",
        "same_CNetNPC_actor",
        "actor_plus_0x70_bit_0x40;actor_plus_0x264_counter",
        "actor_plus_0x260_byte",
        "starting_from_constructor_zero;plus_0x260_still_zero;bit_0x40_set;"
        "eleven_qualifying_CNetNPC_update_calls",
        "increments_plus_0x264_and_latches_plus_0x260_to_one_when_counter_exceeds_10",
        MANUAL_HASH_STATUS, "0x0045C53B;0x0045C540", "0x0045C54F;0x0044469C",
        "CNetNPC_selector_readiness",
        support=("common_actor_ctor", "CNetNPC_model_callback", "common_model_callback"),
        nonclaim=(
            "A clear bit 0x40 pauses rather than resets +0x264; +0x260 is not cleared in this "
            "update body. Scheduling frequency, callback completion, and time to the eleventh "
            "qualifying update remain runtime facts. " + MANUAL_HASH_NONCLAIM
        ),
    )
    add(
        "MCG-IMG-049", "DISTANCE_SELECTOR_GATE", "registered_CNetNPC_actor",
        "same_CNetNPC_actor_and_nameboard_controller",
        "reference_vector_from_app_plus_0x17C_else_app_plus_0x08;actor_position_xyz",
        "squared_distance;controller_subobject_plus_0x18_bit_1;selector_control_flow",
        "actor_plus_0x254_nonnull;controller_plus_0x10_nonnull;CNetNPC_takes_"
        "non_special_type_branch;distance_squared_ordered_against_cached_thresholds",
        "greater_than_10000_squared_returns_before_selector;within_10000_squared_continues;"
        "greater_than_5000_squared_calls_0x0043D7B0_then_converges;both_readiness_bytes_"
        "must_be_nonzero_before_0x00443F50",
        MANUAL_HASH_STATUS, "0x004444B7;0x004444EB", "0x004446A7",
        "actor_update_selector_call",
        support=("NPC_nameboard_controller_ctor_prefix", "CNetNPC_selector_readiness"),
        nonclaim=(
            "10000 and 5000 are exact image integers converted to float and squared; their "
            "world unit is unnamed and must not be reported as meters. Live reference selection, "
            "positions, floating-point ordering, distance, and readiness values remain runtime gates. "
            + MANUAL_HASH_NONCLAIM
        ),
    )
    add(
        "MCG-IMG-050", "REGISTRY_LIFETIME_REMOVAL", "actor_manager_plus_0x0C_tree",
        "registered_CNetNPC_membership",
        "actor_plus_0xD4_state;actor_plus_0xD0_reconcile_generation;"
        "actor_plus_0x78_plus_0x7C_identity;manager_clear_invocation",
        "tree_membership_and_future_tick_eligibility",
        "state_sweep_or_reconcile_or_full_clear_path_is_invoked",
        "state_sweep_erases_valid_actor_nodes_when_plus_0xD4_is_not_3_and_retains_"
        "state_3;reconcile_queues_non_special_actor_pointers_whose_plus_0xD0_misses_"
        "the_incremented_manager_generation;post_vslot_0x18_pass_resolves_each_queued_"
        "actor_plus_0x78_plus_0x7C_and_erases_the_matching_node;full_clear_erases_all_nodes",
        MANUAL_HASH_STATUS, "0x00446345;0x0044702F;0x00447087;0x00446825",
        "0x00638AD0;0x004464A6;0x00638A80",
        "registry_queued_erase",
        support=("registry_state_sweep", "actor_reconcile", "manager_frame_update",
                 "registry_full_clear", "registry_node_copy", "manager_tick_iteration"),
        nonclaim=(
            "The reconcile queue contains actor pointers, not qword keys; the erase consumer "
            "derives the key from each actor+0x78/+0x7C. Registry erase proves loss of manager "
            "membership and future tick eligibility, not immediate actor destruction or pixels. "
            "Which removal path runs and when is runtime/scene state. "
            + MANUAL_HASH_NONCLAIM
        ),
    )
    add(
        "MCG-IMG-051", "LABEL_FONTSTYLE_SETTER", "NPC_nameboard_controller_LABEL_NAME",
        "UILabel_interface",
        "controller_plus_0x50_cast_LABEL_NAME;controller_plus_0x34_FontStyleID",
        "UILabel_plus_0x90_FontStyleID",
        "LABEL_NAME_lookup_dynamic_casts_through_type_token_built_from_UILabel_RTTI;"
        "nameboard_visibility_gate_passes;UILabel_vslot_0x138_value_differs_from_controller_plus_0x34",
        "dispatches_UILabel_vslot_0x13C;the_two_pinned_UILabel_pool_vtables_resolve_"
        "that_slot_to_0x00AA37D0_which_stores_the_numeric_ID",
        MANUAL_HASH_STATUS, "0x005BE742;0x005BDA6B;0x005BDA81", "0x00AA37E8",
        "NPC_nameboard_update",
        support=("NPC_nameboard_bind_label", "UILabel_rtti", "UILabel_reflection_ctor",
                 "UILabel_type_token_init", "UILabel_type_token_getter",
                 "UILabel_pool_ctor_1", "UILabel_pool_ctor_2",
                 "UILabel_vtable_style_window", "UILabel_vtable_2_style_window",
                 "UILabel_FontStyleID_parser", "UILabel_style_setter"),
        nonclaim=(
            "A failed LABEL_NAME lookup/cast leaves controller+0x50 null. This row proves the "
            "interface/property path and pinned pool-vtable targets; it does not prove which "
            "concrete vptr a live model instance carries or that a numeric ID changed pixels. "
            + MANUAL_HASH_NONCLAIM
        ),
    )
    add(
        "MCG-IMG-052", "LABEL_FONTSTYLE_APPLY", "UILabel_FontStyleID_setter",
        "UILabel_and_text_component_state",
        "requested_positive_FontStyleID", "style_registry_node_plus_0x10;UILabel_style_fields;"
        "UILabel_plus_0x198_text_component_plus_0x10_handle_and_dirty_flags",
        "0x00AA37D0_runs_for_a_changed_ID;global_style_registry_lookup_returns_style_pointer_or_null",
        "stores_ID_before_lookup;nonnull_style_applies_fields_and_configures_text_component;"
        "null_style_returns_without_applying_style_even_though_Label_plus_0x90_keeps_the_ID",
        MANUAL_HASH_STATUS, "0x00AA37E8;0x00A9F590", "0x00AA6F3E;0x00A8AD4F",
        "UILabel_style_apply",
        support=("UILabel_style_setter", "UIFontStyle_lookup", "UIText_component_config",
                 "UILabel_vtable_style_window", "UILabel_vtable_2_style_window"),
        nonclaim=(
            "This is a state/resource preparation path, not pixel proof. A missing live registry "
            "entry is a concrete failure: the label ID is updated, the null style is a no-op, and "
            "the nameboard mismatch test can then skip retrying the same ID on later updates. "
            + MANUAL_HASH_NONCLAIM
        ),
        blocker=(
            "IMAGE now establishes the startup loader and positive-ID insertion path, but not "
            "successful live parse/allocation or live style-registry nodes 56 through 63."
        ),
        next_evidence=(
            "Runtime trace loader outcome, selected ID, registry lookup result, style pointer, "
            "and resulting text-component handle/dirty state."
        ),
    )
    add(
        "MCG-IMG-053", "LABEL_RENDER_CEILING", "UILabel_draw_and_text_component",
        "LABEL_NAME_render_submission_path",
        "UILabel_plus_0x198_text_component;visibility_and_component_render_state",
        "indirect_renderer_setup_and_per_line_vslot_0x3C_glyph_calls",
        "frame_traversal_dispatches_UILabel_vslot_0x38;UILabel_visibility_vslot_0x10C_"
        "passes;optional_plus_0x19C_handle_gate_passes;text_component_plus_0x94_clear;"
        "plus_0x10_nonnull;plus_0x40_nonzero;size_and_line_gates_pass",
        "0x00AA71A0_tail_dispatches_0x00A8AF50_which_reaches_global_renderer_vslot_0x20_"
        "and_per_line_object_vslot_0x3C_calls_with_position_glyph_and_color_arguments",
        MANUAL_HASH_STATUS, "0x00AA71C8;0x00A8B16D", "0x00A8B201;0x00A8B287;0x00A8B2B9",
        "UIText_component_render",
        support=("UILabel_draw", "UILabel_vtable_draw_window", "UILabel_vtable_2_draw_window",
                 "UIText_component_config", "UILabel_style_apply", "NPC_nameboard_update"),
        nonclaim=(
            "The indirect calls are the bounded static submission ceiling. IMAGE alone does not "
            "prove frame traversal for this LABEL_NAME instance, concrete renderer receiver/vtable, "
            "visibility/culling/scissor/alpha outcome, device success, or any final framebuffer pixel. "
            + MANUAL_HASH_NONCLAIM
        ),
        blocker="Concrete renderer dispatch and rendered pixels are not closed by these IMAGE spans.",
        next_evidence="Runtime correlate controller+0x34, label+0x90, style pointer, draw dispatch, renderer calls, and an observed frame for the same actor.",
    )
    add(
        "MCG-IMG-054", "STYLE_REGISTRY_STARTUP_WIRING",
        f"global_style_manager_{fmt_va(style_manager_va)}",
        "BigFontStyle_resource_loader_wiring",
        f"ASCII_path@{fmt_va(style_path_literal_va)}={style_path_literal};"
        f"wide_attribute@{fmt_va(style_id_attribute_va)}={style_id_attribute}",
        f"outer_init={fmt_va(style_outer_init_va)};loader={fmt_va(style_loader_va)};"
        f"manager={fmt_va(style_manager_va)}",
        "exact_literal_and_manager_immediate_match;whole_image_all_six_PE_section_"
        "file_backed_raw_E8_rel32_census_has_one_site_for_each_named_target",
        f"outer_init_call={fmt_va(style_outer_init_call_sites[0])};"
        f"loader_call={fmt_va(style_loader_call_sites[0])};"
        f"scanned_PE_sections={pe_section_count};raw_rel32_count_outer="
        f"{len(style_outer_init_call_sites)};raw_rel32_count_loader="
        f"{len(style_loader_call_sites)}",
        MECHANICAL_CENSUS_STATUS,
        f"{fmt_va(style_outer_init_call_sites[0])};{fmt_va(style_loader_call_sites[0])}",
        f"{fmt_va(style_outer_init_va)};{fmt_va(style_loader_va)}",
        "BigFontStyle_startup_call",
        support=("style_startup_required_call", "UIFontStyle_registry_loader"),
        nonclaim=(
            "This row is a mechanical literal/immediate/direct-call byte census over all six "
            "exact PE section-table file-backed intervals only. It does "
            "not interpret call ordering, branch polarity, loader behavior, startup success, "
            "live tree contents, requested/applied style equality, or pixels."
        ),
    )
    add(
        "MCG-IMG-055", "STYLE_REGISTRY_CHILD_LOAD",
        f"global_style_manager_{fmt_va(style_manager_va)}",
        "positive_ID_FontStyle_children",
        f"path_argument_from_{fmt_va(style_loader_call_sites[0])};child_attribute_"
        f"{style_id_attribute};conversion={style_id_conversion_import}",
        "manager_plus_0xE4_keyed_tree;node_plus_0x10_style_pointer",
        "loader_body_runs;document_parse_returns_nonzero;child_ID_string_is_nonempty;"
        f"converted_ID_is_{style_id_accept_relation}_{style_id_lower_exclusive};"
        "allocation_and_following_control_flow_complete",
        "clears_prior_style_tree_then_for_each_accepted_child_allocates_0x78_bytes;"
        "calls_0x00A9D6B0;inserts_or_resolves_the_integer_key_via_0x006BC410;"
        "stores_the_style_pointer;calls_0x00A9DAE0_with_the_same_child;returns_AL_1_"
        "after_iteration",
        MANUAL_HASH_STATUS,
        "0x00A9F8ED;0x00A9F982;0x00A9F9BE;0x00A9F9D5;0x00A9FA01;0x00A9FA11",
        "0x00A9FA5D;0x00A9F590",
        "UIFontStyle_registry_loader",
        support=("BigFontStyle_startup_call", "wide_int_default_wrapper", "UIFontStyle_lookup"),
        nonclaim=(
            "The child-loop and branch meanings are manual x86 interpretation. The loader's "
            "return value is not tested by the outer resource routine at 0x00408530, and the "
            "startup caller's later AL test therefore does not prove this inner load succeeded. "
            "Neither the call chain nor DATA file contents prove a live node, applied style, or "
            "pixel. " + MANUAL_HASH_NONCLAIM
        ),
        blocker=(
            "Successful live parse/allocation and live keyed nodes for requested styles remain "
            "runtime facts despite the exact static loader path."
        ),
        next_evidence=(
            "Runtime observe the 0x00A9F860 return, manager tree count, and lookups for IDs 56 "
            "through 63 in the same process generation."
        ),
    )
    add(
        "MCG-IMG-056", "NAMEBOARD_READY_ZERO_PATH", "CNetNPC_vtable_slot_plus_0x38",
        "same_CNetNPC_actor",
        f"conditional_slot_target={fmt_va(cnetnpc_slot38_target)};requested_model_state_byte="
        f"{ready_zero_requested_byte}",
        "actor_plus_0x258_byte",
        "CNetNPC_slot_plus_0x38_is_invoked;global_0x01021DC1_is_nonzero;"
        "actor_plus_0x35C_is_nonnull;imported_gate_returns_nonnull;actor_plus_0x80_is_"
        "nonnull;model_plus_0x74_differs_from_requested_zero",
        f"calls_{fmt_va(ready_zero_call_target)}_with_first_argument_zero_then_stores_zero_"
        "at_same_actor_plus_0x258",
        MANUAL_HASH_STATUS,
        "0x0045B7D0;0x0044238F",
        "0x004424B3;0x00444693",
        "CNetNPC_slot38_ready_zero",
        support=("CNetNPC_vtable_core", "actor_model_state_ready_store",
                 "common_actor_update", "actor_update_selector_call"),
        nonclaim=(
            "IMAGE does not name the event represented by CNetNPC vtable slot +0x38, prove any "
            "network Attr/relation/combat/death message invokes it, or prove it runs for a live "
            "monster. If model+0x74 is already zero, the shared routine returns before this store; "
            "common update remains the separately proved copy path. " + MANUAL_HASH_NONCLAIM
        ),
        blocker=(
            "The trigger/event semantics and live invocation of CNetNPC slot +0x38 remain open."
        ),
        next_evidence=(
            "Trace a typed caller or runtime invocation of CNetNPC slot +0x38 and record model+0x74 "
            "and actor+0x258 before/after for the same actor."
        ),
    )
    add(
        "MCG-IMG-057", "FONTSTYLE_COLOR_PROPERTY_ANCHORS",
        f"UIFontStyle_parser_{fmt_va(style_property_parser_va)}",
        "registry_style_children_and_UILabel_embedded_style",
        f"wide_{font_color_property}@{fmt_va(font_color_property_va)};"
        f"wide_{outline_color_property}@{fmt_va(outline_color_property_va)};"
        f"wide_{label_fontstyle_id_property}@{fmt_va(label_fontstyle_id_property_va)};"
        f"wide_{embedded_fontstyle_property}@{fmt_va(embedded_fontstyle_property_va)}",
        f"UILabel_vslot_0x140={fmt_va(label_embedded_style_getter_va)};"
        f"vslot_0xD8={fmt_va(label_font_color_setter_va)};"
        f"vslot_0x224={fmt_va(label_outline_color_setter_va)}",
        "whole_image_all_six_PE_section_file_backed_E8_rel32_census_for_the_property_parser;"
        "both_pinned_UILabel_vtables_match_the_named_slots",
        f"scanned_PE_sections={pe_section_count};section_names="
        f"{','.join(pe_section_names)};file_backed_bounds={pe_section_bounds_text};"
        f"property_parser_direct_call_count={len(style_property_parser_call_sites)};"
        "direct_call_sites="
        + ",".join(fmt_va(value) for value in style_property_parser_call_sites),
        MECHANICAL_CENSUS_STATUS,
        ";".join(fmt_va(value) for value in style_property_parser_call_sites),
        fmt_va(style_property_parser_va),
        "UIFontStyle_property_parser",
        support=(
            "FontColor_literal", "OutlineEffectColor_literal",
            "FontStyleID_literal", "FontStyle_literal",
            "UILabel_embedded_style_getter", "UILabel_vtable_style_window",
            "UILabel_vtable_2_style_window", "UILabel_FontColor_setter",
            "UILabel_OutlineEffectColor_setter",
        ),
        nonclaim=(
            "This row is a mechanical literal/vtable/direct-call census only. The census scans "
            "every byte position whose five-byte E8+rel32 encoding fits within each section's "
            "min(VirtualSize,SizeOfRawData) file-backed interval across all six exact PE "
            "section-table entries (.text,.code,.rdata,.data,.rsrc,.reloc), resolving to "
            f"{fmt_va(style_property_parser_va)}; it does not treat linear disassembly as a "
            "negative. It does not interpret either caller, parse components, join DATA values, "
            "prove a live style node, or prove pixels."
        ),
    )
    add(
        "MCG-IMG-058", "FONTSTYLE_COLOR_PARSE_APPLY", "UIFontStyle",
        "conditionally_resolved_UILabel_style",
        f"{font_color_property};{outline_color_property};numeric_"
        f"{label_fontstyle_id_property};embedded_{embedded_fontstyle_property}",
        "UIFontStyle_plus_0x30..0x3C;UIFontStyle_plus_0x4C..0x58;"
        "UILabel_color_state",
        f"{fmt_va(style_property_parser_va)}_receives_a_style_XML_node_with_the_named_"
        f"properties;for_the_nonempty_nonsentinel_{label_fontstyle_id_property}_text_route_"
        f"{fmt_va(label_style_lookup_va)}_returns_"
        f"nonnull;{fmt_va(label_style_apply_va)}_receives_that_style_pointer",
        f"each_ordered_integer_component_is_converted_through_{style_id_conversion_import}_"
        f"then_divided_by_{rgba_divisor:g}_from_{fmt_va(rgba_divisor_va)}_and_clamped_"
        "to_[0,1];FontColor_is_stored_at_style_plus_0x30..0x3C_and_passed_to_"
        f"UILabel_vslot_0xD8_{fmt_va(label_font_color_setter_va)};OutlineEffectColor_"
        "is_stored_at_style_plus_0x4C..0x58_and_passed_to_"
        f"UILabel_vslot_0x224_{fmt_va(label_outline_color_setter_va)};present_empty_or_"
        f"sentinel_{fmt_va(label_empty_sentinel_va)}_FontStyleID_text_bypasses_"
        f"{fmt_va(label_numeric_conversion_va)}_and_dispatches_ID_{label_zero_dispatch_id}_"
        f"at_{fmt_va(label_zero_dispatch_va)}",
        MANUAL_HASH_STATUS,
        f"{fmt_va(rgba_property_wrapper_va)};{fmt_va(rgba_normalized_parser_va)};"
        f"{fmt_va(label_numeric_conversion_va)};{fmt_va(label_style_lookup_va)}",
        f"{fmt_va(label_style_apply_va)};{fmt_va(label_font_color_setter_va)};"
        f"{fmt_va(label_outline_color_setter_va)}",
        "UIFontStyle_property_parser",
        support=(
            "rgba_property_wrapper", "rgba_u8_normalized_parser",
            "UILabel_FontStyleID_parser", "UILabel_embedded_style_getter",
            "UILabel_style_setter", "UIFontStyle_lookup", "UILabel_style_apply",
            "UILabel_FontColor_setter", "UILabel_OutlineEffectColor_setter",
            "UIFontStyle_registry_loader",
        ),
        nonclaim=(
            f"The block at 0x00AA488F is the UILabel numeric {label_fontstyle_id_property} "
            f"branch with an embedded-{embedded_fontstyle_property} fallback; it is not the RGB "
            f"property parser. A present-but-empty string or the empty sentinel "
            f"{fmt_va(label_empty_sentinel_va)} bypasses {fmt_va(label_numeric_conversion_va)} "
            f"and dispatches ID {label_zero_dispatch_id} at {fmt_va(label_zero_dispatch_va)}. "
            f"The nonempty, nonsentinel lane reaches {fmt_va(label_numeric_conversion_va)}; "
            "IMAGE proves no digit validator, so arbitrary nonempty text (e.g. abc) may reach "
            "_wtoi and yield 0. "
            f"Registry colors are parsed by {fmt_va(style_property_parser_va)}. "
            "Actual per-ID tuples remain separate DATA facts and are not IMAGE facts. Loader "
            "success, lookup success for a live requested ID, frame traversal, and rendered pixels "
            "remain runtime conditions. " + MANUAL_HASH_NONCLAIM
        ),
        blocker=(
            "The conditional static property-to-UILabel route is closed; live registry contents "
            "and final pixels are still runtime facts."
        ),
        next_evidence=(
            "Runtime correlate requested label+0x90 ID, nonnull registry style pointer, the two "
            "color setter calls, and a rendered frame for the same actor."
        ),
    )

    for index, style_id in enumerate(sorted(EXPECTED_PALETTE), start=1):
        rows.append(
            make_data_row(
                f"MCG-DATA-{index:03d}", style_id, palette[style_id], line_numbers[style_id]
            )
        )
    return rows


def validate_rows(
    rows: Sequence[Mapping[str, str]], selector_rows: Sequence[Mapping[str, str]]
) -> None:
    if len(rows) != 66:
        raise RuntimeError(f"expected 66 output rows, got {len(rows)}")
    if Counter(row["source"] for row in rows) != Counter({"IMAGE": 58, "DATA": 8}):
        raise RuntimeError("unexpected source census")
    if any(not row["nonclaim"].startswith("[MEASURED]") for row in rows):
        raise RuntimeError("factual IMAGE/DATA row lost explicit [MEASURED] label")

    actual_manifest = tuple(
        (row["gate_key"], row["row_kind"], row["canonical_selector_keys"])
        for row in rows
    )
    if len(EXPECTED_ROW_MANIFEST) != 66:
        raise RuntimeError("expected-row manifest cardinality drift")
    if actual_manifest != EXPECTED_ROW_MANIFEST:
        raise RuntimeError("exact gate-key/row-kind/canonical-reference manifest drift")

    gate_keys = [row["gate_key"] for row in rows]
    if len(set(gate_keys)) != len(gate_keys):
        raise RuntimeError("duplicate gate_key")
    evidence_keys = [row["evidence_key"] for row in rows]
    if len(set(evidence_keys)) != len(evidence_keys):
        raise RuntimeError("duplicate evidence_key")
    for row in rows:
        if set(row) != set(FIELDNAMES):
            raise RuntimeError(f"column mismatch on {row['gate_key']}")
        if row["source"] not in {"IMAGE", "DATA"}:
            raise RuntimeError(f"invalid source on {row['gate_key']}")
        if row["source"] == "IMAGE":
            if row["source_file"] != IMAGE_SOURCE or row["source_sha256"] != IMAGE_SHA256:
                raise RuntimeError(f"mixed IMAGE source on {row['gate_key']}")
            if row["source_locator"]:
                raise RuntimeError(f"unexpected DATA locator on {row['gate_key']}")
        else:
            if (
                row["source_file"] != FONT_STYLE_SOURCE
                or row["source_sha256"] != FONT_STYLE_SHA256
            ):
                raise RuntimeError(f"mixed DATA source on {row['gate_key']}")
            if any(
                row[column]
                for column in (
                    "producer_va",
                    "consumer_va",
                    "span_start_va",
                    "span_end_va",
                    "file_off_start",
                    "file_off_end",
                    "span_sha256",
                    "support_spans",
                    "canonical_selector_keys",
                )
            ):
                raise RuntimeError(f"mixed IMAGE evidence on {row['gate_key']}")
        expected_key = evidence_key({**row, "evidence_key": ""})
        if row["evidence_key"] != expected_key:
            raise RuntimeError(f"unstable evidence_key on {row['gate_key']}")

    ordered_evidence_digest = sha256_bytes("\n".join(evidence_keys).encode("ascii"))
    if ordered_evidence_digest != EXPECTED_ORDERED_EVIDENCE_KEY_DIGEST:
        raise RuntimeError(
            "exact ordered evidence-row content digest drift: "
            f"expected {EXPECTED_ORDERED_EVIDENCE_KEY_DIGEST}, got {ordered_evidence_digest}"
        )

    selector_by_key = {row["selector_key"]: row for row in selector_rows}
    selector_keys = set(selector_by_key)
    selector_conditions = {
        (row["condition"], f"FontStyleID={row['output_fontstyle_id']}")
        for row in selector_rows
    }
    if selector_keys & set(evidence_keys):
        raise RuntimeError("new evidence_key duplicates canonical selector_key")
    for row in rows:
        references = [
            value for value in row["canonical_selector_keys"].split(";") if value
        ]
        if any(value not in selector_keys for value in references):
            raise RuntimeError(f"unknown canonical selector reference on {row['gate_key']}")
        if (row["condition"], row["output"]) in selector_conditions:
            raise RuntimeError(f"canonical selector row copied by {row['gate_key']}")

    crosswalk_rows = [
        row for row in rows
        if row["row_kind"] == "TYPED_SELECTOR_CROSSWALK"
    ]
    if len(crosswalk_rows) != 9:
        raise RuntimeError("expected nine typed selector crosswalk rows")
    if any(not row["canonical_selector_keys"] for row in crosswalk_rows):
        raise RuntimeError("typed selector crosswalk lacks canonical reference")
    if any(row["semantic_status"] != "PROVEN_EXACT" for row in crosswalk_rows):
        raise RuntimeError("typed selector crosswalk lost exact conditional status")
    if any(row["blocker"] or row["required_next_evidence"] for row in crosswalk_rows):
        raise RuntimeError("closed typed selector crosswalk regained a static blocker")
    if any(
        not row["output"].startswith("reaches_canonical_")
        or row["owner_type"] != "RuntimeRes_spawned_CNetNPC_same_instance"
        or row["applies_to_class"] != "CNetNPC_with_bound_NPC_nameboard_controller"
        for row in crosswalk_rows
    ):
        raise RuntimeError("typed selector crosswalk lost the same-instance join")
    typed_tail_keys = {
        CANONICAL_KEYS["red_offensive"],
        CANONICAL_KEYS["red_latched"],
        CANONICAL_KEYS["orange_clear"],
    }
    untyped_keys = {
        CANONICAL_KEYS["positive_style_56"],
        CANONICAL_KEYS["positive_style_58"],
        CANONICAL_KEYS["positive_style_59"],
        CANONICAL_KEYS["positive_style_57"],
        CANONICAL_KEYS["yellow_relation"],
        CANONICAL_KEYS["gray_death"],
    }
    input_prefix = (
        "RuntimeRes_actor_entry_identity_to_same_CNetNPC_selector_receiver;"
    )
    join_support = {
        "singleton_getter", "factory_register_path", "registry_insert",
        "registry_node_copy", "manager_tick_iteration", "actor_update_selector_call",
        "CNetNPC_nameboard_create", "NPC_nameboard_backpointer",
        "NPC_nameboard_vtable", "NPC_nameboard_bind_label",
        "NPC_controller_style_store", "NPC_LABEL_NAME_style_apply",
    }
    for row in crosswalk_rows:
        references = row["canonical_selector_keys"].split(";")
        if len(references) != 1:
            raise RuntimeError(
                f"selector crosswalk reference cardinality drift on {row['gate_key']}"
            )
        reference = references[0]
        canonical = selector_by_key[reference]
        expected_input = input_prefix + canonical["condition"]
        if row["input_field"] != expected_input:
            raise RuntimeError(
                f"selector crosswalk prerequisite drift on {row['gate_key']}"
            )
        if row["runtime_field"] != f"FontStyleID={canonical['output_fontstyle_id']}":
            raise RuntimeError(
                f"selector crosswalk output drift on {row['gate_key']}"
            )
        canonical_name = next(
            name for name, key in CANONICAL_KEYS.items() if key == reference
        )
        if row["condition"] != (
            f"same_instance_runtime_actor_reaches_{canonical_name}_"
            "when_all_call_and_selector_gates_hold"
        ):
            raise RuntimeError(f"selector crosswalk condition drift on {row['gate_key']}")
        if row["output"] != f"reaches_canonical_{canonical_name}":
            raise RuntimeError(f"selector crosswalk conclusion drift on {row['gate_key']}")
        if any(name not in row["support_spans"] for name in join_support):
            raise RuntimeError(f"same-instance support span dropped on {row['gate_key']}")
        if any(
            value not in row["nonclaim"]
            for value in ("actor+0x254", "actor+0x258", "actor+0x260", "rendered screen color")
        ):
            raise RuntimeError(f"runtime gate/nonclaim dropped on {row['gate_key']}")
        expected_owner = (
            "typed_CNetNPC" if reference in typed_tail_keys
            else "untyped_dynamic_controller"
        )
        if canonical["selector_lane"] != expected_owner:
            raise RuntimeError(f"canonical owner-class boundary drift on {row['gate_key']}")
    if set(row["canonical_selector_keys"] for row in crosswalk_rows) != untyped_keys | typed_tail_keys:
        raise RuntimeError("typed selector crosswalk key set drift")
    if sum(row["output"].startswith("reaches_canonical_") for row in rows) != 9:
        raise RuntimeError("exact conditional RuntimeRes-to-selector integration count drift")

    join_rows = [
        row for row in rows
        if row["gate_key"] in {f"MCG-IMG-{index:03d}" for index in range(39, 46)}
    ]
    if len(join_rows) != 7 or any(
        row["source"] != "IMAGE" or row["semantic_status"] != "PROVEN_EXACT"
        or row["blocker"] or row["required_next_evidence"]
        for row in join_rows
    ):
        raise RuntimeError("same-instance join row contract drift")
    manual_rows = [
        row for row in rows
        if row["gate_key"] in (
            {f"MCG-IMG-{index:03d}" for index in range(46, 54)}
            | {"MCG-IMG-055", "MCG-IMG-056", "MCG-IMG-058"}
        )
    ]
    if len(manual_rows) != 11 or any(
        row["source"] != "IMAGE"
        or row["semantic_status"] != MANUAL_HASH_STATUS
        or MANUAL_HASH_NONCLAIM not in row["nonclaim"]
        for row in manual_rows
    ):
        raise RuntimeError("manual/hash-anchored row method boundary drift")
    mechanical_rows = [
        row for row in rows if row["semantic_status"] == MECHANICAL_CENSUS_STATUS
    ]
    if (
        len(mechanical_rows) != 2
        or {row["gate_key"] for row in mechanical_rows}
        != {"MCG-IMG-054", "MCG-IMG-057"}
        or any("mechanical" not in row["nonclaim"] for row in mechanical_rows)
        or any(row["blocker"] for row in mechanical_rows)
        or any(row["required_next_evidence"] for row in mechanical_rows)
    ):
        raise RuntimeError("mechanical style-wiring row boundary drift")
    property_census_row = next(
        row for row in rows if row["gate_key"] == "MCG-IMG-057"
    )
    required_property_census_fragments = (
        "whole_image_all_six_PE_section_file_backed_E8_rel32_census",
        "scanned_PE_sections=6",
        "section_names=.text,.code,.rdata,.data,.rsrc,.reloc",
        "property_parser_direct_call_count=2",
        "direct_call_sites=0x00A9FA11,0x00AA490D",
        "min(VirtualSize,SizeOfRawData)",
    )
    if any(
        fragment not in "\n".join(property_census_row.values())
        for fragment in required_property_census_fragments
    ):
        raise RuntimeError("all-six-section property-parser census contract drift")
    parse_apply_row = next(
        row for row in rows if row["gate_key"] == "MCG-IMG-058"
    )
    required_parse_apply_fragments = (
        "present-but-empty",
        "0x00F0930C",
        "bypasses 0x00894700",
        "dispatches ID 0 at 0x00AA48DC",
        "The nonempty, nonsentinel lane reaches 0x00894700",
        "IMAGE proves no digit validator",
        "arbitrary nonempty text (e.g. abc) may reach _wtoi and yield 0",
    )
    if any(
        fragment not in "\n".join(parse_apply_row.values())
        for fragment in required_parse_apply_fragments
    ):
        raise RuntimeError("UILabel empty/sentinel numeric-path contract drift")
    if any("UNPROVEN_same_instance" in value for row in rows for value in row.values()):
        raise RuntimeError("withdrawn same-instance blocker text returned")


def render_tsv(rows: Sequence[Mapping[str, str]]) -> str:
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
    return stream.getvalue()


def render_report(
    rows: Sequence[Mapping[str, str]],
    server: Mapping[str, str],
    image_facts: Mapping[str, object],
    palette_facts: Mapping[str, object],
) -> str:
    kinds = Counter(row["row_kind"] for row in rows)
    evidence_hash = hashlib.sha256(
        "\n".join(row["evidence_key"] for row in rows).encode("ascii")
    ).hexdigest()
    writer_table = "\n".join(
        f"| `{relative}` | {line} | {category} | {route} | {identity} | {carriers} |"
        for relative, line, category, route, identity, carriers
        in REACHABLE_WRITER_CENSUS
    )
    excluded_table = "\n".join(
        f"| `{relative}` | {line} | {reason} |"
        for relative, line, reason in EXCLUDED_WRITER_CENSUS
    )
    style_path_literal = str(image_facts["style_path_literal"])
    style_path_literal_va = int(image_facts["style_path_literal_va"])
    style_id_attribute = str(image_facts["style_id_attribute"])
    style_id_attribute_va = int(image_facts["style_id_attribute_va"])
    style_manager_va = int(image_facts["style_manager_va"])
    style_loader_va = int(image_facts["style_loader_va"])
    style_loader_call_sites = tuple(
        int(value) for value in image_facts["style_loader_call_sites"]
    )
    style_outer_init_va = int(image_facts["style_outer_init_va"])
    style_outer_init_call_sites = tuple(
        int(value) for value in image_facts["style_outer_init_call_sites"]
    )
    style_id_conversion_import = str(image_facts["style_id_conversion_import"])
    style_id_lower_exclusive = int(image_facts["style_id_lower_exclusive"])
    style_id_accept_relation = str(image_facts["style_id_accept_relation"])
    cnetnpc_slot38_target = int(image_facts["cnetnpc_slot38_target"])
    ready_zero_call_target = int(image_facts["ready_zero_call_target"])
    ready_zero_requested_byte = int(image_facts["ready_zero_requested_byte"])
    font_color_property = str(image_facts["font_color_property"])
    font_color_property_va = int(image_facts["font_color_property_va"])
    outline_color_property = str(image_facts["outline_color_property"])
    outline_color_property_va = int(image_facts["outline_color_property_va"])
    label_fontstyle_id_property = str(image_facts["label_fontstyle_id_property"])
    label_fontstyle_id_property_va = int(
        image_facts["label_fontstyle_id_property_va"]
    )
    embedded_fontstyle_property = str(image_facts["embedded_fontstyle_property"])
    embedded_fontstyle_property_va = int(
        image_facts["embedded_fontstyle_property_va"]
    )
    style_property_parser_va = int(image_facts["style_property_parser_va"])
    style_property_parser_call_sites = tuple(
        int(value) for value in image_facts["style_property_parser_call_sites"]
    )
    rgba_property_wrapper_va = int(image_facts["rgba_property_wrapper_va"])
    rgba_normalized_parser_va = int(image_facts["rgba_normalized_parser_va"])
    rgba_divisor_va = int(image_facts["rgba_divisor_va"])
    rgba_divisor = float(image_facts["rgba_divisor"])
    label_numeric_conversion_va = int(image_facts["label_numeric_conversion_va"])
    label_empty_sentinel_va = int(image_facts["label_empty_sentinel_va"])
    label_zero_dispatch_va = int(image_facts["label_zero_dispatch_va"])
    label_zero_dispatch_id = int(image_facts["label_zero_dispatch_id"])
    label_embedded_style_getter_va = int(
        image_facts["label_embedded_style_getter_va"]
    )
    label_style_lookup_va = int(image_facts["label_style_lookup_va"])
    label_style_apply_va = int(image_facts["label_style_apply_va"])
    label_font_color_setter_va = int(image_facts["label_font_color_setter_va"])
    label_outline_color_setter_va = int(
        image_facts["label_outline_color_setter_va"]
    )
    pe_section_count = int(image_facts["pe_section_count"])
    pe_section_names = tuple(str(value) for value in image_facts["pe_section_names"])
    pe_section_file_backed_bounds = tuple(
        (str(name), int(va_start), int(va_end), int(raw_start), int(raw_end))
        for name, va_start, va_end, raw_start, raw_end
        in image_facts["pe_section_file_backed_bounds"]
    )
    expected_section_bounds = tuple(
        (
            name,
            section_va,
            section_va + min(virtual_size, raw_size),
            raw_offset,
            raw_offset + min(virtual_size, raw_size),
        )
        for name, section_va, virtual_size, raw_offset, raw_size in SECTIONS
    )
    palette_root = str(palette_facts["root_tag"])
    palette_count = int(palette_facts["style_count"])
    palette_minimum = int(palette_facts["minimum_style_id"])
    palette_maximum = int(palette_facts["maximum_style_id"])
    palette_ids = tuple(int(value) for value in palette_facts["ordered_style_ids"])
    required_palette_ids = tuple(
        int(value) for value in palette_facts["required_palette_ids"]
    )
    required_palette = {
        int(style_id): {
            str(attribute): str(value)
            for attribute, value in dict(attributes).items()
        }
        for style_id, attributes in dict(palette_facts["required_palette"]).items()
    }
    if (
        style_loader_call_sites != (0x004086E6,)
        or style_outer_init_call_sites != (0x0040A2E9,)
        or style_id_lower_exclusive != 0
        or style_id_accept_relation != "signed_greater_than"
        or font_color_property != "FontColor"
        or outline_color_property != "OutlineEffectColor"
        or label_fontstyle_id_property != "FontStyleID"
        or embedded_fontstyle_property != "FontStyle"
        or style_property_parser_call_sites != (0x00A9FA11, 0x00AA490D)
        or rgba_divisor != 255.0
        or label_zero_dispatch_id != 0
        or pe_section_count != 6
        or pe_section_names != (".text", ".code", ".rdata", ".data", ".rsrc", ".reloc")
        or pe_section_file_backed_bounds != expected_section_bounds
        or palette_ids != EXPECTED_FONT_STYLE_IDS
        or required_palette_ids != tuple(sorted(EXPECTED_PALETTE))
        or required_palette != {
            style_id: {
                "FontColor": values["FontColor"],
                "OutlineEffectColor": values["OutlineEffectColor"],
            }
            for style_id, values in EXPECTED_PALETTE.items()
        }
    ):
        raise RuntimeError("verified style facts changed before report construction")

    palette_table = "\n".join(
        f"| {style_id} | {required_palette[style_id]['FontColor']} | "
        f"{required_palette[style_id]['OutlineEffectColor']} | "
        f"{EXPECTED_PALETTE[style_id]['label'].replace('_', ' ')} |"
        for style_id in required_palette_ids
    )
    re191_table = "\n".join(
        f"| {style_id} | {required_palette[style_id]['FontColor']} | "
        f"{normalized_float32_rgba(required_palette[style_id]['FontColor'], rgba_divisor)} | "
        f"{required_palette[style_id]['OutlineEffectColor']} | "
        f"{normalized_float32_rgba(required_palette[style_id]['OutlineEffectColor'], rgba_divisor)} |"
        for style_id in (61, 62, 63)
    )
    property_parser_span = span_columns("UIFontStyle_property_parser")
    normalized_parser_span = span_columns("rgba_u8_normalized_parser")
    pe_section_bounds_text = ", ".join(
        f"`{name}` VA {fmt_va(va_start)}..{fmt_va(va_end)}, "
        f"file {fmt_va(raw_start)}..{fmt_va(raw_end)}"
        for name, va_start, va_end, raw_start, raw_end
        in pe_section_file_backed_bounds
    )
    return f"""# Monster name-color gate: RuntimeRes actor entry to CNetNPC

## [MEASURED] Result

This artifact re-derives {len(rows)} additive rows:
{sum(row["source"] == "IMAGE" for row in rows)} IMAGE rows and
{sum(row["source"] == "DATA" for row in rows)} DATA rows. Rows MCG-IMG-054 and
MCG-IMG-057 carry status `{MECHANICAL_CENSUS_STATUS}` and contain only
mechanically verified literal/immediate/vtable/direct-call facts. Rows
MCG-IMG-046..053, MCG-IMG-055..056, and MCG-IMG-058 carry status
`{MANUAL_HASH_STATUS}`: their
predicate, branch-polarity, queue/dataflow and render-argument descriptions are
manual x86 interpretation anchored to exact pinned spans and byte checks. The
bounded conditional static path described by that manual review is:

RuntimeRes actor-entry wire qword -> record+0x18/+0x1C -> actor reconcile ->
actor type 4 factory -> CNetNPC vslot+0x10 -> CNetNPC+0x78/+0x7C -> same
manager registry node+0x18 -> same actor updater -> selector receiver -> that
actor's bound NPC nameboard controller -> controller+0x34 FontStyleID ->
typed LABEL_NAME UILabel interface -> label+0x90 ID -> style-registry lookup ->
style/text-component application -> conditional indirect glyph-render calls.

This is exact only under the named call gates. It does not say every spawned
CNetNPC reaches the selector or pixels: registry retention, controller allocation/
binding, live resource callback, actor+0x254, actor+0x258, actor+0x260, distance,
live selector predicates, style-registry population, UI traversal, visibility,
renderer dispatch, delivery, and device/framebuffer outcome remain runtime
conditions. Original-server identity policy and rendered screen color remain open.
Generator PASS is an integrity result; it does not symbolically derive or independently
prove the manual instruction semantics in MCG-IMG-046..053, MCG-IMG-055..056,
or MCG-IMG-058.

The output copies none of the 14 canonical rows in
PF_ATTR_NAME_COLOR_SELECTOR.tsv. Nine PROVEN_EXACT typed conditional
crosswalk rows reference canonical selector keys and add the same-instance
RuntimeRes/CNetNPC/controller path. Exact conditional RuntimeRes-to-selector
integration rows: 9. Canonical rows copied: 0. Canonical selector SHA-256:
{SELECTOR_SHA256}.

## [MEASURED] Critical correction: the governing record is not CreateActorDataEx

The previous draft conflated two different records because both expose offsets
+0x18/+0x1C. Fresh IMAGE re-derivation proves that RuntimeRes CNetNPC spawn
uses the actor-entry record serialized at 0x005E21D0, not CreateActorDataEx
serialized at 0x005DFF60.

The exact incoming actor-entry field order is:

1. record+0x10: one byte, tag 0x0B, actor type.
2. record+0x18..+0x1F: one complete qword, tag 0x32, length 8. Its low
   dword is record+0x18; its high dword is record+0x1C.
3. one-byte Attr count, followed by each Attr id and Attr serializer.

On the READ branch, 0x005E230C..0x005E2316 passes length 8 and record+0x18
to 0x0089A640. Therefore every byte through record+0x1F, including that
record's +0x1B, is populated by the qword field.

## [MEASURED] Exact IMAGE pointer flow

- 0x005E4060 reads the RuntimeRes derived object at +0x1C, takes its list
  head at +0x10, and makes the direct actor-reconcile call from this handler
  to 0x00446F30. No whole-image sole-caller claim is made.
- 0x00446F87/0x00446F8A read the same entry's +0x18/+0x1C pair for the
  actor-registry lookup.
- On an unknown identity, 0x00446F9C..0x00446FA3 calls the factory.
- The factory reads actor type from the same record at +0x10. Type 4 selects
  the CNetNPC type node, whose registration is tied to RTTI .?AVCNetNPC@@.
- 0x00446A92..0x00446AB5 passes the same pointer-to-record to the new
  actor's vtable slot +0x10.
- CNetNPC slot +0x10 is 0x0045D200. 0x0045D23B..0x0045D244 copies
  actor-entry +0x18/+0x1C into CNetNPC +0x78/+0x7C.
- RuntimeRes reconcile and the periodic actor tick both receive the exact
  singleton address 0x0102C6C0 from getter 0x00402A20.
- Factory registration builds the value {{identity low, identity high,
  CNetNPC pointer}}. 0x006F4130..0x006F413E copies it to tree-node
  +0x10/+0x14/+0x18 and retains the actor pointer.
- Tick 0x00445480 reads the same node+0x18 pointer and calls 0x00444400 with
  it as ECX. The updater preserves ESI=ECX, then 0x004446A5 restores ECX=ESI
  and directly calls selector 0x00443F50.
- CNetNPC slot +0x7C creates controller vtable 0x00F2CD48, stores it at that
  actor+0x254, stores the actor back-pointer at controller+0x30, and binds
  LABEL_NAME at controller+0x50. Selector slot +0x34 resolves to 0x009F1A70,
  which stores the chosen FontStyleID at controller+0x34; the UI update reads
  +0x50 and +0x34 together.

This closes the bounded conditional same-instance selector/nameboard path. No
CreateActorVital alias is needed. The readiness, distance, lifetime and UILabel
consumers are pinned below; their live values remain conditions, not universal
runtime guarantees.

## [MEASURED] Exact readiness and distance gates

- CNetNPC vtable `+0x58` is `0x0045CD80`; its wrapper passes the callback
  argument directly to `0x00444730`. The common callback requires a nonnull
  argument, nonnull `argument+0x48`, and nonnull resource `+0x08`. On normal
  flow it installs `argument+0x48` at actor+0x80 and sets actor+0x70 bit 0x40
  at `0x004448B4`. IMAGE closes the conditional producer, not callback
  scheduling or resource completion.
- CNetNPC init sets actor+0x258 to one after the guarded nameboard-create
  vslot succeeds. That is not a permanent latch. Except when global mode is 6,
  common update subsequently forces +0x258 to zero when actor+0x10 bit 0x4000
  is set; otherwise it copies byte `[actor+0x80+0x74]`, using zero for a null
  actor+0x80. Mode 6 preserves the previous value by skipping this refresh.
- CNetNPC construction clears +0x260 and +0x264. While +0x260 is zero and bit
  0x40 is set, each CNetNPC update increments dword +0x264. The
  eleventh qualifying update makes the counter exceed ten and latches +0x260 to one.
  Clearing bit 0x40 pauses this body; it does not reset +0x264 here.
- Updater `0x00444400` first requires actor+0x254 and controller+0x10. CNetNPC
  takes the non-special-type branch. The reference vector comes from
  `[app+0x17C]` when nonzero, otherwise `[app+0x08]`; actor position comes from
  `0x0043BCE0`. The code computes squared xyz distance. Greater than
  `10000^2` returns before the selector. At or below `10000^2`, greater than
  `5000^2` calls `0x0043D7B0` and converges with the nearer lane. Both +0x258
  and +0x260 must then be nonzero before `0x004446A7` calls the selector.
  The integers are exact; the world unit is unnamed and is not claimed to be
  meters.

Concrete failures are therefore statically available: an unscheduled or null
resource callback leaves bit 0x40 clear; bit 0x4000, null actor+0x80, or zero
model+0x74 makes +0x258 zero; fewer than eleven qualifying updates leaves
+0x260 zero; missing controller state or distance greater than `10000^2`
returns before the selector. Whether any one occurs for a live actor is runtime.

An additional conditional same-CNetNPC zero path is now pinned. CNetNPC vtable
slot +0x38 resolves to `{fmt_va(cnetnpc_slot38_target)}`. Under its global,
actor+0x35C and imported-result gates it calls
`{fmt_va(ready_zero_call_target)}` with first argument
{ready_zero_requested_byte}. The shared routine requires actor+0x80 and a
model+0x74 byte different from the requested zero; on that path it stores zero
at the same actor+0x258. If model+0x74 is already zero it returns before this
store. IMAGE does not name the vslot event or connect it to a network Attr,
relation, combat or death message, so this is not called a death transition and
its live invocation remains open. Fixed-displacement writer candidates in
unrelated object layouts are not promoted into CNetNPC writers without a typed
receiver join; alias and whole-object writes remain outside this bounded census.

## [MEASURED] Exact registry lifetime/removal boundary

Registry membership, actor lifetime and rendered pixels are separate states.
The tree node stores the actor pointer at +0x18 and tick dispatches only retained,
valid node payloads.

- Sweep `0x004462F0` compares byte actor+0xD4 with 3. Equality jumps over
  erase; a valid actor node whose byte is **not 3** is advanced past and then
  erased through `0x00638AD0`. The pass also clears the pending vector. No
  gameplay name is assigned to state value 3.
- Reconcile increments manager+0x04. Incoming actors found or created in that
  generation receive the new value at actor+0xD0. During the second tree pass,
  a nonnull actor whose +0xD0 does not match is retained only by the special
  dynamic-type exception for token `0x0102CB04`; otherwise the actor pointer is
  appended to manager vector +0x2C. This is a
  pointer queue, not a qword-key queue.
- Manager frame update `0x00446750` first invokes actor vslot+0x18, then calls
  queued eraser `0x004463D0`. For each queued actor pointer, that eraser reads
  actor+0x78/+0x7C, resolves the matching manager+0x0C tree node, erases it,
  and clears the vector.
- Full clear `0x00446810` erases the whole tree and clears the vector whenever
  that method is invoked.

These paths prove loss of registry membership and therefore future tick
eligibility. They do not by themselves prove immediate actor destruction.
Which sweep/reconcile/clear path runs, and its ordering relative to a frame,
remains live scene state.

## [MEASURED] UILabel state, style application and render ceiling

The LABEL_NAME binder does more than store an untyped child. It looks up the
literal child, obtains its dynamic type, compares it through the token returned
by `0x00AA7010`, and stores the adjusted pointer only on success. Static token
initialization builds global `0x01090A04` from `.?AVUILabel@@`; thus
controller+0x50 is an exact conditional UILabel interface pointer.

Nameboard update requires controller+0x50 and its visibility gate
(`app+0x778` bit 0x20 or controller+0x44 greater than zero). It calls UILabel
vslot+0x138 to read the numeric FontStyleID and compares it with
controller+0x34. On mismatch it dispatches vslot+0x13C. The independent
`FontStyleID` property parser uses the same slot, and both pinned 0x220-byte
UILabel pool vtables resolve +0x138 to `0x004021F0`, +0x13C to `0x00AA37D0`,
and +0x144 to `0x00AA6EF0`.

`0x00AA37D0` stores the requested ID at UILabel+0x90 before looking it up in
the global style tree at `{fmt_va(style_manager_va)}`. A positive found ID returns node+0x10;
nonpositive or absent IDs return null. The setter still dispatches vslot+0x144.
`0x00AA6EF0` is a no-op for null. For a nonnull style it copies style fields,
invokes several UILabel setters, configures the UILabel+0x198 text component,
stores its returned resource handle at component+0x10, and marks component
and label state dirty.

The new mechanical census pins ASCII `{style_path_literal}` at
`{fmt_va(style_path_literal_va)}`, wide attribute name `{style_id_attribute}`
at `{fmt_va(style_id_attribute_va)}`, manager `{fmt_va(style_manager_va)}`, and
exactly one raw E8+rel32 byte-pattern site to loader
`{fmt_va(style_loader_va)}` at `{fmt_va(style_loader_call_sites[0])}` across
all {pe_section_count} exact PE section-table entries, including `.rsrc` and
`.reloc`, using each section's `min(VirtualSize, SizeOfRawData)` file-backed
interval. It likewise finds exactly one raw rel32 site
to outer resource routine `{fmt_va(style_outer_init_va)}` at
`{fmt_va(style_outer_init_call_sites[0])}`. These are mechanical byte facts;
they do not themselves interpret execution or success.

Manual x86 review of the pinned loader span shows it clears manager+0xE4's
keyed tree, parses the supplied document, iterates its children, reads the
`{style_id_attribute}` string, converts through `{style_id_conversion_import}`
and takes the mechanically pinned `{style_id_accept_relation}` branch relative
to {style_id_lower_exclusive}. The accepted path allocates
0x78 bytes, calls `0x00A9D6B0`, inserts/resolves that integer key through
`0x006BC410`, stores the style pointer, and calls `0x00A9DAE0` with the same
child. The DATA document independently has root `{palette_root}` and exactly
{palette_count} unique ordered IDs {palette_minimum}..{palette_maximum}; IDs
{','.join(str(value) for value in required_palette_ids)} therefore meet the
positive-ID condition. That DATA-to-IMAGE composition is stated here, not
mixed into one TSV row.

The inner loader can return zero when document parsing fails, but outer routine
`{fmt_va(style_outer_init_va)}` does not test that inner return before continuing.
Therefore its caller's later AL test does not prove the style load succeeded.
This remaining failure still separates state from pixels: a missing live entry
leaves label+0x90 equal to the requested controller
ID while style application did nothing, and the next nameboard update can skip
a retry of that same ID. The remaining blocker is narrowed to live parse/
allocation/tree state rather than an unknown static registration path.

## [MEASURED] RE-191: exact conditional FontStyle 61/62/63 color route

The premise is corrected rather than repeated: `0x00AA488F` is not the RGB
property parser. It is the UILabel XML branch for numeric
`{label_fontstyle_id_property}` (wide literal `{fmt_va(label_fontstyle_id_property_va)}`).
When that property exists, a retrieved text value that is empty or equals the
empty sentinel `{fmt_va(label_empty_sentinel_va)}` bypasses
`{fmt_va(label_numeric_conversion_va)}` and dispatches explicit ID
{label_zero_dispatch_id} through UILabel vslot+0x13C from
`{fmt_va(label_zero_dispatch_va)}`. The nonempty, nonsentinel lane reaches {fmt_va(label_numeric_conversion_va)}; IMAGE proves no digit validator, so arbitrary nonempty text (e.g. abc) may reach _wtoi and yield 0.
When the property itself is absent, UILabel vslot+0x140 resolves to
`{fmt_va(label_embedded_style_getter_va)}`, returns UILabel+0x1A0, and the same
block calls `{fmt_va(style_property_parser_va)}` for embedded
`{embedded_fontstyle_property}` (wide literal
`{fmt_va(embedded_fontstyle_property_va)}`).

The registry loader independently calls `{fmt_va(style_property_parser_va)}` at
`{fmt_va(style_property_parser_call_sites[0])}` for each accepted positive-ID
child. An all-six-PE-section file-backed raw-byte E8+rel32 census finds exactly
{len(style_property_parser_call_sites)} direct
sites to that target: {', '.join(f'`{fmt_va(value)}`' for value in style_property_parser_call_sites)}.
The scan covers {', '.join(f'`{name}`' for name in pe_section_names)}, including
`.rsrc` and `.reloc`. It checks every byte position whose five-byte E8+rel32
encoding fits within the section's `min(VirtualSize, SizeOfRawData)`
file-backed interval; it is not a negative inferred from linear disassembly.
Exact scanned bounds: {pe_section_bounds_text}. The property-parser span is
`{property_parser_span['span_start_va']}..{property_parser_span['span_end_va']}`,
file `{property_parser_span['file_off_start']}..{property_parser_span['file_off_end']}`,
SHA-256 `{property_parser_span['span_sha256']}`.

Manual x86 interpretation of that pinned span establishes the color semantics.
Wide `{font_color_property}` at `{fmt_va(font_color_property_va)}` is read through
`{fmt_va(rgba_property_wrapper_va)}` and copied to UIFontStyle+0x30..+0x3C.
Wide `{outline_color_property}` at `{fmt_va(outline_color_property_va)}` uses the
same wrapper and is copied to UIFontStyle+0x4C..+0x58. The wrapper reaches
`{fmt_va(rgba_normalized_parser_va)}`; each ordered integer component is converted
through `{style_id_conversion_import}`, divided by exact double {rgba_divisor:g}
at `{fmt_va(rgba_divisor_va)}`, clamped to [0,1], and stored as float32. That
normalizer span is `{normalized_parser_span['span_start_va']}..{normalized_parser_span['span_end_va']}`,
file `{normalized_parser_span['file_off_start']}..{normalized_parser_span['file_off_end']}`,
SHA-256 `{normalized_parser_span['span_sha256']}`.

For a nonnull numeric-ID lookup, `{fmt_va(label_style_apply_va)}` passes
UIFontStyle+0x30 to UILabel vslot+0xD8 ->
`{fmt_va(label_font_color_setter_va)}` and UIFontStyle+0x4C to vslot+0x224 ->
`{fmt_va(label_outline_color_setter_va)}`. Thus the static property-to-UILabel
route is closed conditionally. The exact per-ID tuples below remain DATA facts;
the normalized columns are an explicitly labelled DATA+IMAGE composition, not
new IMAGE rows.

| FontStyleID | DATA FontColor RGBA | conditional normalized float32 | DATA OutlineEffectColor RGBA | conditional normalized float32 |
|---:|---|---|---|---|
{re191_table}

Therefore style 63 is distinct from controls 61 and 62: its DATA FontColor is
exactly `{required_palette[63]['FontColor']}` and outline is
`{required_palette[63]['OutlineEffectColor']}`. This answers
RE-191 at the conditional static resource/property layer. It does not prove the
startup loader succeeded in a live process, that lookup returned a live node,
that the selector path ran for a particular actor, or that any framebuffer pixel
was produced.

The two pinned UILabel vtables resolve draw slot +0x38 to `0x00AA71A0`.
After visibility and optional handle gates, it tail-dispatches text-component
renderer `0x00A8AF50`. That renderer has further handle, line-count, size and
clipping gates, then reaches a global renderer vslot+0x20 call and per-line
object vslot+0x3C calls carrying position, glyph and color arguments. This is
the bounded static submission ceiling. Exact frame traversal for this instance,
concrete renderer receiver/vtable, culling/scissor/alpha, device success and
final framebuffer pixels require runtime evidence.

## [MEASURED] BasicAttr identity is a separate qword

BasicAttr inherits a DBAttribute identity subcodec at 0x00467790. That
subcodec conditionally serializes the Attr object's own +0x18/+0x1C qword
under its own mask byte at attr+0x20.

That is not the actor-entry qword, even when a sender chooses to put the same
numeric value in both places. CNetNPC init copies the actor-entry qword first,
then calls 0x005DF080 to bind the Attr vector. This proves the origin of
CNetNPC +0x78/+0x7C. The separate registry and updater rows prove the
conditional same-object selector invocation; the two qwords remain distinct
wire fields even when a sender chooses equal numeric values.

## [MEASURED] CreateActorDataEx and the +0x1B blocker

CreateActorDataEx remains a real, separately proved IMAGE type:

- its constructor establishes +0x18=0xFF, +0x19=0, +0x1A=0, and +0x1C=0;
- its 0x005DFF60 codec reads three one-byte fields into +0x18, +0x19,
  +0x1A, and one four-byte field into +0x1C;
- neither the complete pinned constructor nor codec establishes +0x1B;
- the visible allocation thunks provide no zero-fill contract.

Thus +0x1B is a genuine blocker only if someone tries to reconstruct a
CreateActorDataEx dword from those three adjacent bytes. It is not a blocker
for RuntimeRes actor identity and does not govern CNetNPC name color.

## [MEASURED] Selector-local signed identity gate and typed conditional style crosswalk

The selector treats receiver+0x7C as the signed high dword and receiver+0x78 as
the unsigned low dword. The gate and its bounded same-instance connection to a
RuntimeRes-spawned type-4 CNetNPC are exact under the invocation/readiness gates.

- Positive: high > 0, or high == 0 and low != 0.
- Nonpositive: high < 0, or both dwords are zero.

When the same-instance path reaches the selector and each listed canonical
condition holds, the crosswalk is:

| Conditional canonical selector condition | FontStyleID | Exact DATA FontColor |
|---|---:|---|
| positive identity and relationship predicate false | 56 | (255, 62, 255, 255) |
| positive identity, relationship true, local lookup succeeds | 58 | (140, 198, 255, 255) |
| positive identity, relationship true, style-58 lookup not selected, later secondary relation query true | 59 | (0, 255, 255, 255) |
| positive identity, positive-lane fallthrough | 57 | (83, 255, 83, 255) |
| nonpositive identity and relationship predicate true | 60 | (255, 255, 0, 255) |
| nonpositive, relationship false, receiver vslot+0x3C false, NPCAttr associated-actor lanes fall through, n_OFFESIVE nonzero | 61 | (255, 100, 100, 255) |
| same prior fallthroughs, n_OFFESIVE zero, bit 0x100 set, local vslots +0x3C/+0x40 both false | 61 | (255, 100, 100, 255) |
| same prior fallthroughs, n_OFFESIVE zero, bit 0x100 clear | 62 | (255, 159, 113, 255) |
| nonpositive, relationship false, CNetNPC vslot+0x3C true | 63 | (179, 179, 179, 255) |

Style 63 has other canonical causes, so gray is not equivalent to dead.
Style 61 has other canonical causes, so red is not equivalent to n_OFFESIVE or
bit 0x100. The n_OFFESIVE branch does not read n_AGGRO. This table is not proof
that a particular live actor passed the readiness/predicate gates or rendered
the color; it is exact conditional static reachability.

## [MEASURED] Distinct actor and nameboard-controller objects

- `0x00F0DF58` is the CNetNPC actor vtable. Actor slot `+0x3C` at
  `0x00F0DF94` resolves to death predicate `0x0043BD70`.
- `0x00F2CD48` is the NPC nameboard-controller vtable. Controller slot `+0x34`
  at `0x00F2CD7C` resolves to style store `0x009F1A70`.
- These are different objects and different vtables, not pointer-equal objects.
  IMAGE proves their bidirectional binding: actor+0x254=controller and
  controller+0x30=actor. Caller `0x004446A7` supplies the RuntimeRes-created
  CNetNPC as selector receiver; selector reloads that actor's +0x254 controller.

## [MEASURED] Exact DATA palette

| FontStyleID | FontColor RGBA | OutlineEffectColor RGBA | Descriptive label |
|---:|---|---|---|
{palette_table}

RGBA tuples are exact DATA facts. English color labels are descriptive.

## [MEASURED] [RECONSTRUCTED POLICY] Exhaustive pinned-snapshot Foundation writer census

**[MEASURED] [RECONSTRUCTED POLICY]** This section is deliberately not represented as a
TSV evidence row. It combines a separately pinned project-source check
with IMAGE selector facts and the DATA palette. It is not original-server
evidence, not a client-observed render result, and changes no IMAGE/DATA row.

ServerProject snapshot boundary: Git commit
`{server["snapshot_commit"]}`, commit time `{server["snapshot_commit_time"]}`
(`2026-09-01 14:50:38 +07:00`). Later commits are outside this section's
scope; the generator reads this exact commit and does not claim that it remains
the checkout's present state.

Snapshot: current/pf_login_game_server_v141.py, size {server["size"]},
SHA-256 {server["sha256"]}.

- Line {server["qword_pack_line"]} packs qwords as unsigned little-endian <Q.
- Line {server["actor_entry_identity_line"]} writes the
  make_remote_actor_entry actor_identity as tag 0x32 qword.
- The pinned V141 Port Royal builder passes positive examples
  {server["positive_examples"]} to actor type 4 at line
  {server["actor_builder_line"]}.
- It also places the same numeric value in the nested NPCAttr identity at lines
  {server["npc_builder_line"]} and {server["npc_identity_line"]}; that is a
  separate Attr qword and is not the selector source.

The fail-closed AST census finds exactly 30 literal
`make_remote_actor_entry` calls under Foundation: 19 flagless/reachable writer
definitions below and 11 explicitly excluded scenario/hypothesis/helper or
production-gated sites.
Scope count, exactly: **19 Foundation direct writer definitions reachable
without scenario flag (18 default +1 diagnostic conditional), excludes frozen
V141 fallback/scenarios; not 19 simultaneously active.**

`P` means `0x2000 + placement_index + 1`. Every one of the 18 shipped sites
uses P. The diagnostic also uses P; its D3 slot is the special concrete result
`0x2000 + 9000 + 4 + 1 = 0x432D`. At every row, the same identity value is
passed to the outer actor entry and to NPCAttr and optional MovementAttr where
those Attrs exist. This is a pinned-snapshot dataflow result, not proof of the
original server's identity policy.

| Direct writer | Line | Class | Reachability anchor | Identity origin | Same-identity carrier lines |
|---|---:|---|---|---|---|
{writer_table}

Excluded direct calls:

| Direct writer | Line | Why excluded from 19 |
|---|---:|---|
{excluded_table}

The frozen V141 fallback is outside Foundation and is kept separate. A
`build_field_mob_population` helper with no direct runtime caller in the pinned
Foundation census is not
promoted into a live route. The lane handoff route is
`runtime.py -> lane_hooks/lane_a_scene_census.py ->
world_population_handoff.py`; combat/death recomposition is
`runtime.py -> mob_scene_recompose.py`; face and scene-14 ChooseNPC have their
own direct runtime routes; the multi-object diagnostic is gated by operator
configuration. The scene-1 ChooseNPC safety-net responder is also kept outside
the reachable census because its module explicitly declares
`production_allowed = False`.

Two comments at `lane_hooks/lane_a_scene_census.py:181-198` still say scenes 4
and 10 have `login_entry_allowed: false`. The separately pinned registry has
both booleans true, and `scene_is_open_to_players` at lines 367-383 reads that
registry. `world_scene_travel.py:243-256` also says all ten surveyed doors are
open. These are stale comments, not inactive writers and not original evidence.

**[MEASURED] [RECONSTRUCTED POLICY]** For the pinned legacy examples and the snapshot's
nonnegative placement indices, high dword is zero and low dword is nonzero.
The exact conditional crosswalk therefore puts those identities in the
positive selector family whenever the call/readiness gates pass. If the
relationship-false condition also holds, the canonical selector emits
FontStyleID 56 and DATA maps it to magenta
(255, 62, 255, 255). This is not proof that the original server chose these
identities or that the client rendered pink in a particular live frame.
Positive identity alone cannot guarantee pink.

**[MEASURED] [RECONSTRUCTED POLICY]** This is an exact static contract conflict under the
named invocation gates between the exhaustive pinned-snapshot Foundation writer census
and the client selector, not evidence of what the original closed server
emitted. Changing only legacy V141 cannot repair these separately shipped
Foundation composers.

At this pinned snapshot, no single Foundation seam enforces
`outer actor identity == NPCAttr identity == MovementAttr identity`.
`legacy.make_remote_actor_entry` receives already-serialized opaque Attr bytes,
while the override splicers in `runtime.py:323-358`,
`world_population.py:977-1078`, and `mob_scene_recompose.py:674-752` replace
whole entry byte strings without validating their nested identities.

### [PROPOSED] Replacement identity-mapping seam

**[PROPOSED]** The recommended implementation seam has two coupled parts. First, a mapping
candidate must be a session-, scene-, and generation-scoped **bijection** with
`resolve_wire(W) -> P` and `project_wire(P) -> W`; it must prove uniqueness
against the entire outgoing census and be invalidated whenever scene or
generation changes. Second, one typed NPC-style composer must accept the
projected W once and build/validate the same W in the outer entry, NPCAttr, and
optional MovementAttr. Every outbound **actor-identity** reference in CHitResult,
bar, death, recompose, face and conversation paths must call
`project_wire(P) -> W`; inbound actor references must call
`resolve_wire(W) -> P`. Ground-drop elements in the pinned snapshot use their own u32
`drop_key`, and pickup matches that object reference; neither value is actor P
and neither must be remapped. A high-negative W is only a
bounded reconstruction candidate. It must not be hard-coded or described as a
proven original-server identity policy. This is a recommendation about the
replacement, not a claim about original-server architecture.

**[PROPOSED]** Pinned-snapshot seam map: census writers populate outer/NPCAttr/optional
MovementAttr; inbound combat resolves a target before roster lookup; CHitResult,
bar, death, face and recompose project the same active generation; scene or
generation changes invalidate the bijection. The ledger, roster and
`GroundDrop.mob_identity` retain canonical P internally. This is a proposed
replacement design, not original-server evidence.

### [MEASURED] Bg0002 n_OFFESIVE limitation

The pinned generated Bg0002 table contains 17 hostile rows: 12 use
AI_WANDER 16 and 5 Orc Chief rows use AI_WANDER 11. The pinned DATA-derived table
values say AI_WANDER 16 has `n_OFFESIVE=0`, while AI_WANDER 11 has
`n_OFFESIVE=1`. However, the pinned production-configured
`field_mobs.load_roster("Bg0002")` projection filters owner-refused placements
92-96, so its post-filter projection is 12 rows, all AI_WANDER 16. This is a
static project-snapshot projection, not a runtime- or player-observed roster. Do
not call the five Orc Chiefs pinned production-configured combat rows.

**[PROPOSED]** For an AI_WANDER-16 target, a coherent nonpositive identity remains a staged
candidate for orange before hit, red after the runtime bit is set, and gray
after the separately proved death predicate. The same-instance static join is
now proved; runtime still must show that the readiness, relationship, NPCAttr,
bit-writer, death and UI gates pass for the chosen actor. If the five
AI_WANDER-11 Orc Chiefs are ever sent by an alternate producer or reintroduced,
the canonical selector-local branch can emit style 61 at idle; identity change
alone cannot make those five universally orange. That future or alternate-path
constraint must not be hidden by calling them production-configured today.

### [PROPOSED] Bounded runtime stop rules for the mapping candidate

**[PROPOSED]** These are stop rules, not predictions promoted to proof:

1. **STEP-A:** the chosen AI_WANDER-16 target must be orange before attack. If
   it is not orange, stop; do not proceed to interpret later colors.
2. **STEP-B:** require a matched CHitResult whose target identity is the same
   projected W and require the screen to turn red. If either the addressed W or
   the red screen result is absent, stop.
3. Evaluate gray only after a matched corpse/recompose frame addressed to the
   same W carries HP=0 and timer<=0. A gray result before that does not prove
   the death lane.

Each step must retain, rather than assume away, the other IMAGE gates: resolved
target, target+0x10 bit 0x10000, source cast to CMyActor, relationship predicate,
NPCAttr fallthroughs, and the relevant receiver/local vslot predicates.

## [MEASURED] Runtime bit 0x100 boundary

The common actor constructor clears the containing +0x70 dword. Two direct
explicit set writers are proved: CHitResult and CMissileHitResult. Their
targets are not typed as CNetNPC at the writer sites, and no gameplay noun is
assigned to the bit. The typed CNetNPC selector consumes and can clear it.

IMAGE proves that both writers require a resolved target whose identity high
dword is signed-negative, plus their other pinned guards. **[MEASURED]
[RECONSTRUCTED POLICY]** At the pinned snapshot, the replacement combat path is connected:
`mob_combat.py:{server["chit_result_producer_line"]}` composes CHitResult and
`runtime.py:{server["runtime_action_line"]}` queues it as `MOB_COMBAT_ANNOUNCE`.
The pinned snapshot's P identities have high dword zero, so they fail the IMAGE writer's
negative-target gate before the bit can be set. This route statement is about
the replacement; the negative-target requirement is the separate IMAGE fact.

Crucially, this bit affects style 61 versus 62 only after the actor-entry
identity takes the nonpositive lane. A positive actor-entry identity bypasses
that typed tail first.

## [MEASURED] Nonclaims

- No original-server policy for choosing actor identities is claimed.
- Actor type 4 is proved to construct CNetNPC; IMAGE does not rename every type
  4 actor as monster.
- A positive identity is not, by itself, proof of pink; the relationship
  predicate remains part of the style-56 condition.
- BasicAttr identity and actor-entry identity may be numerically equal without
  being the same field or producer.
- CreateActorDataEx field meanings do not transfer to RuntimeRes actor entries.
- The unnamed runtime bit is not called aggro, hostile, or monster state.
- Direct bit writers are not a proof against alias or whole-dword writers.
- Generator PASS does not mechanically prove the manual x86 semantics recorded in
  MCG-IMG-046..053, MCG-IMG-055..056, or MCG-IMG-058.
- CNetNPC vtable slot +0x38 is not assigned a gameplay, combat or death noun.
- The exact startup loader wiring and DATA ID census do not prove a live style
  node, requested-to-applied style transition, or rendered pixel.
- The fail-closed pinned-project census covers direct literal Foundation
  `make_remote_actor_entry` call sites. It does not prove that dynamically
  obtained callables or raw authored frames cannot encode actor type 4.

## [MEASURED] Deterministic census

- Total rows: {len(rows)}
- IMAGE rows: {sum(row["source"] == "IMAGE" for row in rows)}
- DATA rows: {sum(row["source"] == "DATA" for row in rows)}
- Mechanical-census IMAGE rows: 2 (`MCG-IMG-054`, `MCG-IMG-057`)
- Manual/hash-anchored IMAGE rows: 11 (`MCG-IMG-046..053`, `MCG-IMG-055..056`,
  `MCG-IMG-058`)
- BigFontStyle DATA census: root `{palette_root}`, {palette_count} unique ordered
  IDs {palette_minimum}..{palette_maximum}
- Canonical selector rows copied: 0
- Canonical selector rows referenced: 9 PROVEN_EXACT typed conditional crosswalk rows
- Exact conditional RuntimeRes-to-selector integration rows: 9
- Unique evidence keys: {len({row["evidence_key"] for row in rows})}
- Ordered evidence-key digest: {evidence_hash}
- Row kinds: {";".join(f"{key}={kinds[key]}" for key in sorted(kinds))}
- Foundation direct writer calls: 30 (19 reachable, 11 excluded)
- Reachable direct writer definitions: 19 (18 default, 1 diagnostic conditional;
  not simultaneously active)
- Foundation Python snapshot: {server["foundation_file_count"]} files,
  manifest SHA-256 {server["foundation_manifest_sha256"]}
- Separately pinned project inputs: {server["project_pin_count"]} files,
  manifest SHA-256 {server["project_pin_manifest_sha256"]}
- Bg0002 generated/live-after-filter hostile rows:
  {server["generated_bg0002_count"]}/{server["live_bg0002_count"]}

## [MEASURED] Pinned inputs

| Input | Size | SHA-256 |
|---|---:|---|
| GameClient.local.bin | {IMAGE_SIZE} | {IMAGE_SHA256} |
| BigFontStyle.fsl | {FONT_STYLE_SIZE} | {FONT_STYLE_SHA256} |
| PF_ATTR_NAME_COLOR_SELECTOR.tsv | 14 rows | {SELECTOR_SHA256} |
| legacy V141 source | {server["size"]} | {server["sha256"]} |
| population.py | {server["population_size"]} | {server["population_sha256"]} |
| field_mobs.py | {server["field_mobs_size"]} | {server["field_mobs_sha256"]} |
| world_population.py | {server["world_population_size"]} | {server["world_population_sha256"]} |
| runtime.py | {server["runtime_size"]} | {server["runtime_sha256"]} |
| pinned-project pin manifest | {server["project_pin_count"]} files | {server["project_pin_manifest_sha256"]} |
| Foundation Python snapshot | {server["foundation_file_count"]} files | {server["foundation_manifest_sha256"]} |

The exact-commit replacement-server snapshot above is a separately verified project check,
not a TSV evidence source. Generator PASS mechanically verifies pinned input
hashes, exact IMAGE span hashes, enumerated byte/RTTI/type-node/vtable/direct-call
anchors, exact DATA attributes, source separation, row order/content keys,
canonical-selector references, zero copied canonical rows, the two explicit
mechanical-census rows, the eleven explicit manual/hash-anchored status labels and
method nonclaims, the raw rel32 loader/outer-init/property-parser call censuses, the exact ordered
BigFontStyle ID census, all 30 direct Foundation
call sites, all 19 reachable writer-manifest rows, project-source anchors, and
output-pair bytes/hashes. It does not disassemble or symbolically execute the
image. Predicate meaning, branch polarity, pointer/dataflow joins, queue element
type, and render-call argument interpretation are manual review anchored to those
pinned bytes, not conclusions mechanically established by PASS. Runtime readiness
and pixel rendering remain outside both methods.

These files under `pf_bridge/external` are local-only and Git-ignored by the
workspace policy. Another clone will not receive the script/table/report until
owner-approved packaging. Git allowlisting/publication is outside this lane's
authority, so delivery remains local-only. `PF_MONSTER_COLOR_GATE.pair.json` is the commit marker:
the TSV and Markdown are a valid pair only when a marker-before/files/marker-after
read has identical marker bytes and both file size/hash entries match. Publication
stages both files, replaces them, then atomically replaces the marker last. A crash
before that final step is fail-closed and requires a later locked repair; fixed
filenames alone are not an indivisible filesystem object. This generator does not
modify Git.
"""


def validate_report_text(report: str) -> None:
    forbidden = (
        "Typed IMAGE condition after actor type 4 bridge",
        "add the missing typed actor-entry reachability",
        "Exact RuntimeRes-to-selector integration rows: 0",
        "PARTIAL conditional crosswalk",
        "The next edge is open",
        "missing same-instance selector/nameboard join",
        "same-instance selector/nameboard join is later proved",
        "does not prove that caller `0x004446A7` supplies",
        "It verifies the registry node layout",
        "generator verifies the semantics",
        "When that property exists, the branch converts it through",
        "valid-numeric-text",
        "valid_nonempty_nonsentinel",
        "all pinned mapped image sections",
        "whole-mapped-image raw-byte E8+rel32 census",
        "mob_combat.py:1163",
    )
    found = [value for value in forbidden if value in report]
    if found:
        raise RuntimeError(f"report regained withdrawn end-to-end claim: {found}")
    required = (
        "Exact conditional RuntimeRes-to-selector integration rows: 9",
        "PROVEN_EXACT typed conditional",
        "0x00F0DF58",
        "0x00F2CD48",
        "registry node+0x18",
        "actor+0x260",
        "LABEL_NAME",
        "bidirectional binding",
        "same-instance",
        "eleventh qualifying update",
        "pointer queue, not a qword-key queue",
        "state from pixels",
        "bounded static submission ceiling",
        MANUAL_HASH_STATUS,
        MECHANICAL_CENSUS_STATUS,
        ".\\Data\\GUI\\Model\\BigFontStyle.fsl",
        "exactly one raw E8+rel32 byte-pattern site",
        "does not test that inner return",
        "CNetNPC vtable slot +0x38",
        "186 unique ordered IDs 1..186",
        "[MEASURED] RE-191: exact conditional FontStyle 61/62/63 color route",
        "is not the RGB",
        "exactly\n2 direct",
        "all-six-PE-section file-backed raw-byte E8+rel32 census",
        "`.rsrc` and `.reloc`",
        "min(VirtualSize, SizeOfRawData)",
        "empty sentinel `0x00F0930C` bypasses",
        "dispatches explicit ID\n0 through UILabel vslot+0x13C from\n`0x00AA48DC`",
        "The nonempty, nonsentinel lane reaches 0x00894700; IMAGE proves no digit validator, so arbitrary nonempty text (e.g. abc) may reach _wtoi and yield 0.",
        "DATA+IMAGE composition",
        "0x00A9DAE0",
        "0x0053F5E0",
        "0x006D0F40",
        "0x006D0CF0",
        "does not disassemble or symbolically execute",
        "Predicate meaning, branch polarity, pointer/dataflow joins",
        "## [MEASURED] Result",
        "## [MEASURED] Exact DATA palette",
        "## [MEASURED] [RECONSTRUCTED POLICY]",
        "### [PROPOSED] Replacement identity-mapping seam",
        "### [PROPOSED] Bounded runtime stop rules",
        "Git allowlisting/publication is outside this lane's\nauthority, so delivery remains local-only",
    )
    missing = [value for value in required if value not in report]
    if missing:
        raise RuntimeError(f"report lost correction boundary: {missing}")


def acquire_lock() -> int:
    try:
        fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise RuntimeError(
            f"output lock already exists; inspect before removing: {LOCK_PATH.name}"
        ) from exc
    try:
        os.write(fd, f"pid={os.getpid()}\n".encode("ascii"))
        os.fsync(fd)
    except Exception:
        os.close(fd)
        LOCK_PATH.unlink(missing_ok=True)
        raise
    return fd


def release_lock(fd: int) -> None:
    os.close(fd)
    LOCK_PATH.unlink()


def render_pair_marker(outputs: Mapping[Path, bytes]) -> bytes:
    ordered_paths = (TSV_PATH, REPORT_PATH)
    digest = hashlib.sha256()
    files: list[dict[str, object]] = []
    for path in ordered_paths:
        raw = outputs[path]
        name = path.name.encode("ascii")
        digest.update(len(name).to_bytes(4, "little"))
        digest.update(name)
        digest.update(len(raw).to_bytes(8, "little"))
        digest.update(raw)
        files.append(
            {
                "name": path.name,
                "size": len(raw),
                "sha256": sha256_bytes(raw),
            }
        )
    marker = {
        "schema": 1,
        "commit_rule": "marker-before/files-twice/marker-after; exact bytes and hashes",
        "generation_sha256": digest.hexdigest(),
        "files": files,
    }
    return (json.dumps(marker, indent=2, sort_keys=True) + "\n").encode("ascii")


def read_committed_pair(
    expected_outputs: Mapping[Path, bytes], expected_marker: bytes
) -> dict[Path, bytes]:
    if not PAIR_PATH.is_file():
        raise RuntimeError(f"pair marker missing: {PAIR_PATH.name}")
    marker_before = PAIR_PATH.read_bytes()
    first = {path: path.read_bytes() for path in (TSV_PATH, REPORT_PATH)}
    second = {path: path.read_bytes() for path in (TSV_PATH, REPORT_PATH)}
    marker_after = PAIR_PATH.read_bytes()
    if marker_before != marker_after or marker_after != expected_marker:
        raise RuntimeError("pair marker changed or does not name expected generation")
    if first != second:
        raise RuntimeError("output pair changed while taking committed snapshot")
    for path, expected in expected_outputs.items():
        actual = second[path]
        if actual != expected:
            raise RuntimeError(f"byte-identical check differs: {path.name}")
    return second


def atomic_write_bytes(path: Path, raw: bytes) -> None:
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        temp_name = None
    except BaseException:
        if temp_name is not None:
            try:
                Path(temp_name).unlink(missing_ok=True)
            except OSError:
                pass
        raise
    if path.read_bytes() != raw:
        raise RuntimeError(f"post-replace byte check differs: {path.name}")


def verify_pinned_inputs() -> dict[str, str]:
    return {
        "image": verify_file(IMAGE_PATH, IMAGE_SIZE, IMAGE_SHA256),
        "font_style": verify_file(
            FONT_STYLE_PATH, FONT_STYLE_SIZE, FONT_STYLE_SHA256
        ),
        "selector": verify_file(
            SELECTOR_PATH, SELECTOR_PATH.stat().st_size, SELECTOR_SHA256
        ),
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="strict")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="derive in memory and require byte-identical existing outputs",
    )
    args = parser.parse_args()

    checkout_head_before = observe_checkout_head()
    if not args.check and checkout_head_before != PROJECT_SNAPSHOT_COMMIT:
        raise RuntimeError(
            "refusing publish from a checkout beyond the pinned snapshot: "
            f"snapshot={PROJECT_SNAPSHOT_COMMIT} checkout={checkout_head_before}"
        )
    lock_fd: int | None = None
    if not args.check:
        lock_fd = acquire_lock()
    try:
        before = verify_pinned_inputs()
        server_before = verify_project_server_boundary()
        image = IMAGE_PATH.read_bytes()
        if len(image) != IMAGE_SIZE or sha256_bytes(image) != IMAGE_SHA256:
            raise RuntimeError("in-memory image pin mismatch")
        verify_spans(image)
        image_facts = verify_static_anchors(image)
        selector_rows = read_selector_rows()
        palette, line_numbers, palette_facts = parse_palette()
        rows = build_rows(
            palette, line_numbers, selector_rows, image_facts, palette_facts
        )
        validate_rows(rows, selector_rows)

        mid = verify_pinned_inputs()
        server_mid = verify_project_server_boundary()
        if before != mid:
            raise RuntimeError("pinned input changed during derivation")
        if server_before != server_mid:
            raise RuntimeError("replacement-server snapshot changed during derivation")

        report_text = render_report(
            rows, server_before, image_facts, palette_facts
        )
        validate_report_text(report_text)
        outputs = {
            TSV_PATH: render_tsv(rows).encode("utf-8"),
            REPORT_PATH: report_text.encode("utf-8"),
        }
        marker = render_pair_marker(outputs)
        checkout_head_mid = observe_checkout_head()
        if not args.check and checkout_head_mid != checkout_head_before:
            raise RuntimeError(
                "refusing publish because checkout HEAD moved during derivation: "
                f"before={checkout_head_before} mid={checkout_head_mid}"
            )
        if args.check:
            committed = read_committed_pair(outputs, marker)
        else:
            # The marker is the commit point. Readers must ignore fixed filenames
            # unless a marker-before/files/marker-after snapshot validates them.
            for path in (TSV_PATH, REPORT_PATH):
                atomic_write_bytes(path, outputs[path])
            atomic_write_bytes(PAIR_PATH, marker)
            committed = read_committed_pair(outputs, marker)

        after = verify_pinned_inputs()
        server_after = verify_project_server_boundary()
        if before != after:
            raise RuntimeError("pinned input changed during output operation")
        if server_before != server_after:
            raise RuntimeError("replacement-server snapshot changed during output operation")
        committed = read_committed_pair(outputs, marker)
        checkout_head_after = observe_checkout_head()
        if not args.check and checkout_head_after != checkout_head_before:
            raise RuntimeError(
                "checkout HEAD moved during publication: "
                f"before={checkout_head_before} after={checkout_head_after}"
            )

        mode = "check" if args.check else "publish"
        source_counts = Counter(row["source"] for row in rows)
        copied_canonical_count = sum(
            row["gate_key"].startswith("NCS-") for row in rows
        )
        conditional_crosswalk_count = sum(
            row["row_kind"] == "TYPED_SELECTOR_CROSSWALK" for row in rows
        )
        result_lines = [
            f"mode={mode}",
            "output_lock=not_acquired_read_only_check"
            if args.check else "output_lock=acquired_for_publish",
            f"image_size_before={IMAGE_SIZE}",
            f"image_sha256_before={before['image']}",
            f"image_size_after={IMAGE_PATH.stat().st_size}",
            f"image_sha256_after={after['image']}",
            f"legacy_server_sha256={server_after['sha256']}",
            f"foundation_runtime_sha256={server_after['runtime_sha256']}",
            f"project_snapshot_commit={server_after['snapshot_commit']}",
            f"project_snapshot_commit_time={server_after['snapshot_commit_time']}",
            f"checkout_head_before={checkout_head_before}",
            f"checkout_head_after={checkout_head_after}",
            "checkout_relation="
            + (
                "exact_snapshot"
                if checkout_head_before == PROJECT_SNAPSHOT_COMMIT
                and checkout_head_after == PROJECT_SNAPSHOT_COMMIT
                else "drift_from_snapshot"
            ),
            f"project_source_files={server_after['project_pin_count']}",
            f"foundation_direct_writers={len(REACHABLE_WRITER_CENSUS) + len(EXCLUDED_WRITER_CENSUS)} "
            f"reachable={len(REACHABLE_WRITER_CENSUS)} excluded={len(EXCLUDED_WRITER_CENSUS)}",
            f"rows_total={len(rows)} image_rows={source_counts['IMAGE']} "
            f"data_rows={source_counts['DATA']}",
            f"canonical_selector_rows={len(selector_rows)} copied={copied_canonical_count} "
            f"conditional_crosswalk_references={conditional_crosswalk_count}",
            "pass_scope=pinned_input_span_byte_row_output_integrity;not_symbolic_semantic_derivation",
            f"{TSV_PATH.name}: {sha256_bytes(committed[TSV_PATH])}",
            f"{REPORT_PATH.name}: {sha256_bytes(committed[REPORT_PATH])}",
            f"{PAIR_PATH.name}: {sha256_file(PAIR_PATH)}",
        ]
        pass_line = f"monster color gate: PASS mode={mode}"
    finally:
        if lock_fd is not None:
            release_lock(lock_fd)
    for line in result_lines:
        print(line)
    print(pass_line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
