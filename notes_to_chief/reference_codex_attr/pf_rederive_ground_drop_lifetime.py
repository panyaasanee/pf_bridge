#!/usr/bin/env python3
"""Re-derive the bounded ground-drop lifetime model from pinned local evidence.

The IMAGE lane validates exact PE spans and structural joins.  The CAPTURE lane
validates only metadata lines, counts, timing, and file hashes; it never emits
packet bytes.  Current emulator code is verified separately and never promoted
to a TSV source row.  The Markdown report is the only place that composes the
three layers, with explicit nonclaims.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import lzma
import os
import re
import struct
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
TRANSPORT_TSV_PATH = OUT_DIR / "PF_GROUND_DROP_TRANSPORT.tsv"
TRANSPORT_MD_PATH = OUT_DIR / "PF_GROUND_DROP_TRANSPORT.md"
CAPTURE_DIR = PF_ROOT / "GameClient" / "capture_pexile_20260830_151429"
CAPTURE_LIVE_PATH = CAPTURE_DIR / "capture_v141" / "GAME_LIVE.txt"
CAPTURE_CONSOLE_PATH = CAPTURE_DIR / "server_console_live.out.txt"
ATTENDED_NOTE_PATH = (
    PF_ROOT
    / "pf_bridge"
    / "notes_to_chief"
    / "consumed"
    / (
        "20260830_1554_GT143-GT132-GT149-RESULT-label-life-0.2s-is-the-real-"
        "blocker-drops-exist-set103-never-shipped.md"
    )
)
TSV_PATH = OUT_DIR / "PF_GROUND_DROP_LIFETIME.tsv"
MD_PATH = OUT_DIR / "PF_GROUND_DROP_LIFETIME.md"
LOCK_PATH = OUT_DIR / ".pf_rederive_ground_drop_lifetime.lock"
SERVER_ROOT = PF_ROOT / "Pirate Force ServerProject"
V141_PATH = SERVER_ROOT / "current" / "pf_login_game_server_v141.py"
RUNTIME_PATH = SERVER_ROOT / "src" / "pirateforce_foundation" / "runtime.py"
MOB_LOOT_PATH = SERVER_ROOT / "src" / "pirateforce_foundation" / "mob_loot.py"
DROP_PRESENCE_PATH = (
    SERVER_ROOT / "src" / "pirateforce_foundation" / "mob_drop_presence.py"
)
FIELD_DROP_TABLES_PATH = (
    SERVER_ROOT / "src" / "pirateforce_foundation" / "field_drop_tables.py"
)
GAMEDATA_TABLE_ROOT = PF_ROOT / "pf_bridge" / "gamedata" / "tables"
EQUIPMENT_DATA_PATH = GAMEDATA_TABLE_ROOT / "CONSTDATA_TH__EQUIPMENT_BASE.tsv"
CONSUMABLE_DATA_PATH = GAMEDATA_TABLE_ROOT / "CONSTDATA_TH__ITEM_CONSUMABLES.tsv"
MISC_DATA_PATH = GAMEDATA_TABLE_ROOT / "CONSTDATA_TH__ITEM_MISC.tsv"
DROP_ASSET_ROOT = PF_ROOT / "GameClient" / "Data" / "GC" / "F"

EXPECTED_IMAGE_SIZE = 14_759_424
EXPECTED_IMAGE_SHA256 = (
    "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
)
EXPECTED_TRANSPORT_TSV_SHA256 = (
    "9e2396795ee32287f1f9b82f22fb8f394464d2b0a25375d07108ee138c73907b"
)
EXPECTED_TRANSPORT_MD_SHA256 = (
    "e2b1b90efcd63cfb6878f47937a466424d872809599a04718c75e6d7940c38c5"
)
EXPECTED_CAPTURE_LIVE_SIZE = 247_711
EXPECTED_CAPTURE_LIVE_LINES = 2_958
EXPECTED_CAPTURE_LIVE_SHA256 = (
    "ded232875f237e154b2c1ad9b3bab152b3aeb657728bd2da347cdd102cba110c"
)
EXPECTED_CAPTURE_CONSOLE_SIZE = 2_467_886
EXPECTED_CAPTURE_CONSOLE_LINES = 32_260
EXPECTED_CAPTURE_CONSOLE_SHA256 = (
    "a2544e736dc7ba6f8ab132d30d270c13acca71e6f61a4c615643dc8c17fa17bb"
)
EXPECTED_ATTENDED_NOTE_SIZE = 15_215
EXPECTED_ATTENDED_NOTE_SHA256 = (
    "042462792ee7477ccd22ba45964d53fd3b54b21d598772c2d6b32850dd5c1d1e"
)
SERVERPROJECT_SNAPSHOT_COMMIT = (
    "8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa"
)
SERVERPROJECT_SNAPSHOT_COMMIT_TIME = "2026-09-01T07:50:38Z"
SERVERPROJECT_SNAPSHOT_PINS = {
    V141_PATH: (
        382_913,
        "2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22",
        (
            b"def make_runtime_res_empty_exact()",
            b"pc += u8tag(0x0B, 0)  # RuntimeRes extension fields absent",
        ),
    ),
    RUNTIME_PATH: (
        472_447,
        "d683299d86853896304cf92ea0e0a738d1dfb5a2647d68b32a3a1c179e31efe5",
        (b"self.mob_loot_cell = mob_loot.DropLedgerCell()",),
    ),
    MOB_LOOT_PATH: (
        140_483,
        "2bcf102f468d05ba8e877ecce0b9db0cf70fdaead40b31682325f069bd15aa91",
        (
            b"class DropLedgerCell:",
            b"self._lock = threading.Lock()",
            b"def _sweep_locked(self, now: float) -> tuple:",
            b"self._sweep_locked(now)",
            b"def lifetime_seconds(self) -> float:",
            b"def time_left(self, drop_key: int) -> float:",
        ),
    ),
    DROP_PRESENCE_PATH: (
        37_087,
        "21b4db22f97cdb57f56783341625e8ea0526f330b4e4695486234d398f1a573e",
        (b"def sustain_a_kill(", b"frames = mob_loot.refresh_frames(legacy, ledger)"),
    ),
    FIELD_DROP_TABLES_PATH: (
        8_874,
        "0a072121eb97a3529b689f81e38193450ca1b907b49f5926ca7ccb842508ed71",
        (b"# item id -> (table_code, low_id, display_name, drop_model_type)", b"ITEMS = {"),
    ),
}

DATA_TABLE_PINS = {
    22: (
        EQUIPMENT_DATA_PATH,
        156_208,
        "dc39d8b338f78870ac32741b8bd1ddbe5a4696b137378fcfe739721fb6924c97",
    ),
    24: (
        CONSUMABLE_DATA_PATH,
        191_388,
        "04586d54730fee23b7120ec03d7e7b5b17345d23fe4c1d946e7e71222e698e29",
    ),
    26: (
        MISC_DATA_PATH,
        249_729,
        "8cd1774d42230938d429f8fe849f1073467489daac9ac265689bfa70302d5292",
    ),
}

TOKEN_BY_TYPE = (
    "item",
    "weapon",
    "armor",
    "fittings",
    "money",
    "buff",
    "pandora",
    "crystal_r",
    "crystal_b",
    "crystal_g",
    "DROP_ENERGY",
    "DROP_LIFE",
    "holloween01",
)

# This is a scope pin for the current reconstructed replacement roster, not an
# original-game evidence source.  Each emitted DATA row below contains only the
# selected table row's own facts; the report performs the cross-layer composition.
EXPECTED_CURRENT_ROSTER = {
    2200201: (22, 201, 1), 2200222: (22, 222, 1),
    2200401: (22, 401, 1), 2200422: (22, 422, 1),
    2200601: (22, 601, 1), 2200622: (22, 622, 1),
    2200801: (22, 801, 1), 2200822: (22, 822, 1),
    2201001: (22, 1001, 1), 2201022: (22, 1022, 1),
    2201201: (22, 1201, 1), 2201222: (22, 1222, 1),
    2204001: (22, 4001, 2), 2204026: (22, 4026, 2),
    2204201: (22, 4201, 2), 2204226: (22, 4226, 2),
    2204401: (22, 4401, 2), 2204426: (22, 4426, 2),
    2204601: (22, 4601, 2), 2204621: (22, 4621, 2),
    2204801: (22, 4801, 2), 2204821: (22, 4821, 2),
    2205001: (22, 5001, 3), 2205020: (22, 5020, 3),
    2205201: (22, 5201, 3), 2205220: (22, 5220, 3),
    2205401: (22, 5401, 3), 2205420: (22, 5420, 3),
    2205601: (22, 5601, 3), 2205620: (22, 5620, 3),
    2400046: (24, 46, 11), 2400047: (24, 47, 10),
    2400519: (24, 519, 0), 2400522: (24, 522, 0),
    2400525: (24, 525, 0), 2406957: (24, 6957, 0),
    2406958: (24, 6958, 0), 2406959: (24, 6959, 0),
    2414034: (24, 14034, 0), 2414064: (24, 14064, 0),
    2600091: (26, 91, 0), 2600701: (26, 701, 0),
    2600751: (26, 751, 0),
}

PACKAGE_ASSET_PINS = {
    "item.ni_": (1_954, "816e640f35ab60b3a8bef472a80164134a57456b6fdb6a2341eb7267e99e4244"),
    "weapon.ni_": (2_572, "92a1e9146db75cd79eae887da173e5d0ccbc1744ec48e599352fed137f0dfeba"),
    "armor.ni_": (1_769, "49dda1ebdfa03aba85651426fb1fb2180dd7103b9d5433e028a6e23e332b4cf2"),
    "fittings.ni_": (2_090, "0f173a580030ffac3a683532d5695cf9eb02360b53a01114a21bafe079fd990b"),
    "money.ni_": (1_703, "f75849d9326de9e97ca11f875a0ea3c4111c08cec5a2b1c6eb816a2e8747ef10"),
    "buff.ni_": (1_871, "767d99ca12592ea248a610dc85bd6794d13bb9cb7a32fa401b708a167e8c3426"),
    "pandora.ni_": (2_110, "0567ee6d4c01adee546b63b1a774410b4443d9e813f4e4b3198ff6caccdc653d"),
    "crystal_r.ni_": (1_231, "1c8ebea3ee4fa0f6aa170403046117e07775ccb80eac9e76228242fc96bfda81"),
    "crystal_b.ni_": (1_231, "5edb85134598f3e4a957f113284db80180883a76e75391407adc47089a014d42"),
    "crystal_g.ni_": (1_231, "566675ed5e380db28d711fd32a2e501ee4efceb453865a59c7541d54bf2e6d3d"),
    "drop_energy.ni_": (4_064, "5a4670e01417f0f807e6b06afbf152221052d6c6d264fa2727d7ee782cba833f"),
    "drop_life.ni_": (5_984, "ab46221da09e4eba60a6ff9c38846fe89b5147d60caaa0d874d44da7f1c50031"),
    "holloween01.ni_": (3_348, "7aaaeb307f762b17498ef0a32860e5a9192c6c278c29b8ecffdc03d05a967df3"),
}

# Decoded facts are independently pinned so a compressed-file hash match alone
# cannot silently change the parser result.  Counts are over the serialized
# block graph reachable from the sole footer root by NiNode/NiBillboardNode
# child references; they are not runtime/render observations.
PACKAGE_NIF_STRUCTURE_PINS = {
    "item.ni_": (4_178, "064094b68c41f6293923fd28fe540a0d58a97dd869ae588938ec14499cf5d204", 17, 1, 0, 1, 0, 2, 0, 2, 2, 2, 2),
    "weapon.ni_": (6_260, "a86442370271df3ae01083df0dd7fc05624a574492bce22b033a77397a656715", 17, 1, 0, 1, 0, 2, 0, 2, 2, 2, 2),
    "armor.ni_": (4_539, "bef88f6ea9e912c58314890bba26edd4913bf518ffac2eef7dc61977e332cc9f", 17, 1, 0, 1, 0, 2, 0, 2, 2, 2, 2),
    "fittings.ni_": (7_028, "3643041500b5c19cddf72260a97ccb20c644c114d2fff0d5aac7826180112b4f", 17, 1, 0, 1, 0, 2, 0, 2, 2, 2, 2),
    "money.ni_": (4_596, "c4af53c2b9377fd82820b8e539e4d51ab54243d5e2681b4646f2404e9ab13277", 21, 1, 0, 2, 0, 2, 0, 2, 2, 2, 2),
    "buff.ni_": (5_584, "4d9dc1a0379152724a35b571e5614bf1417d6acf4a01086b646380d7f168ac4a", 21, 1, 0, 2, 0, 2, 0, 2, 2, 2, 2),
    "pandora.ni_": (5_757, "86501fc2c5f5790181de95784fd4c2f3ea4b7a6565480b41798ab301832f5a61", 17, 1, 0, 1, 0, 2, 0, 2, 2, 2, 2),
    "crystal_r.ni_": (3_128, "569e61611f713dfbbde5a4b87c0bed9ff4ef14b713c7e70fc5c44554858e6579", 17, 1, 0, 1, 0, 2, 0, 2, 2, 2, 2),
    "crystal_b.ni_": (3_128, "482d3d0ca5d806284ba7c570c7c5e24d83e137ad131eae0148823f8e24235fc8", 17, 1, 0, 1, 0, 2, 0, 2, 2, 2, 2),
    "crystal_g.ni_": (3_128, "63f6e8b935e0c822b970cb3c069bfb753052127c90b2bba643b7414c68597104", 17, 1, 0, 1, 0, 2, 0, 2, 2, 2, 2),
    "drop_energy.ni_": (12_536, "ec6b0848d00a707df29bf616970c73a54c28d21cd9bb691c2e20b80e1e1785b6", 120, 1, 0, 5, 2, 6, 1, 6, 6, 6, 6),
    "drop_life.ni_": (17_579, "bef64649623a3aa7534e97358c266628a287d0d2ee3da4a9a2780dd7081c8f51", 130, 1, 0, 6, 2, 7, 1, 7, 7, 7, 7),
    "holloween01.ni_": (5_959, "c32b072cab6bdd3112fc470c4204699238f0caf37e881ad4bec4bb5f4847c541", 13, 1, 0, 2, 0, 1, 0, 1, 1, 1, 1),
}


@dataclass(frozen=True)
class Section:
    name: str
    virtual_address: int
    virtual_size: int
    raw_offset: int
    raw_size: int


class PE32:
    def __init__(self, data: bytes) -> None:
        self.data = data
        if data[:2] != b"MZ":
            raise ValueError("missing MZ header")
        self.pe_offset = self.u32_offset(0x3C)
        if data[self.pe_offset : self.pe_offset + 4] != b"PE\0\0":
            raise ValueError("missing PE signature")
        coff = self.pe_offset + 4
        self.section_count = self.u16_offset(coff + 2)
        optional_size = self.u16_offset(coff + 16)
        optional = coff + 20
        if self.u16_offset(optional) != 0x10B:
            raise ValueError("image is not PE32")
        self.optional_offset = optional
        self.image_base = self.u32_offset(optional + 28)
        self.size_of_headers = self.u32_offset(optional + 60)
        self.entrypoint_rva = self.u32_offset(optional + 16)
        self.import_rva = self.u32_offset(optional + 104)
        self.import_size = self.u32_offset(optional + 108)
        self.com_descriptor_rva = self.u32_offset(optional + 96 + 14 * 8)
        self.com_descriptor_size = self.u32_offset(optional + 100 + 14 * 8)
        section_table = optional + optional_size
        sections: list[Section] = []
        for index in range(self.section_count):
            entry = section_table + index * 40
            raw_name = data[entry : entry + 8].split(b"\0", 1)[0]
            sections.append(
                Section(
                    raw_name.decode("ascii"),
                    self.u32_offset(entry + 12),
                    self.u32_offset(entry + 8),
                    self.u32_offset(entry + 20),
                    self.u32_offset(entry + 16),
                )
            )
        self.sections = tuple(sections)

    def u16_offset(self, offset: int) -> int:
        return struct.unpack_from("<H", self.data, offset)[0]

    def u32_offset(self, offset: int) -> int:
        return struct.unpack_from("<I", self.data, offset)[0]

    def rva_to_offset(self, rva: int) -> int:
        if 0 <= rva < self.size_of_headers:
            return rva
        for section in self.sections:
            extent = max(section.virtual_size, section.raw_size)
            if section.virtual_address <= rva < section.virtual_address + extent:
                delta = rva - section.virtual_address
                if delta >= section.raw_size:
                    raise ValueError(f"RVA 0x{rva:08X} is not file-backed")
                return section.raw_offset + delta
        raise ValueError(f"RVA 0x{rva:08X} is outside mapped sections")

    def va_to_offset(self, va: int) -> int:
        return self.rva_to_offset(va - self.image_base)

    def u32(self, va: int) -> int:
        return self.u32_offset(self.va_to_offset(va))

    def f32(self, va: int) -> float:
        return struct.unpack_from("<f", self.data, self.va_to_offset(va))[0]

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

    def span(self, start_va: int, end_va: int) -> bytes:
        start = self.va_to_offset(start_va)
        end = self.va_to_offset(end_va)
        if end <= start:
            raise ValueError("invalid VA span")
        return self.data[start:end]

    def import_name_at_iat(self, iat_va: int) -> str:
        """Resolve one PE32 IAT cell to its imported symbol name."""
        if self.import_rva == 0 or self.import_size < 20:
            raise ValueError("missing import directory")
        descriptor = self.rva_to_offset(self.import_rva)
        descriptor_end = descriptor + self.import_size
        while descriptor + 20 <= descriptor_end:
            original_first_thunk = self.u32_offset(descriptor)
            name_rva = self.u32_offset(descriptor + 12)
            first_thunk = self.u32_offset(descriptor + 16)
            if not (original_first_thunk or name_rva or first_thunk):
                break
            lookup_rva = original_first_thunk or first_thunk
            index = 0
            while True:
                lookup = self.u32_offset(self.rva_to_offset(lookup_rva + index * 4))
                if lookup == 0:
                    break
                cell_va = self.image_base + first_thunk + index * 4
                if cell_va == iat_va:
                    if lookup & 0x80000000:
                        raise ValueError(f"IAT 0x{iat_va:08X} imports by ordinal")
                    name_offset = self.rva_to_offset(lookup) + 2
                    name_end = self.data.index(b"\0", name_offset)
                    return self.data[name_offset:name_end].decode("ascii")
                index += 1
            descriptor += 20
        raise ValueError(f"IAT cell not found: 0x{iat_va:08X}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


SPAN_SPECS: dict[str, tuple[int, int, str]] = {
    "name_id": (
        0x0089B220,
        0x0089B27D,
        "a9d3a77ec6b70a2f15327cc34310a5fea6f6911ab2d70055e3515f6f6e22dfba",
    ),
    "gscn_register": (
        0x00BEE050,
        0x00BEE068,
        "9ab505714bc94c7c89a26bf45058ef3c46a54adf02a176a5ceb8bf270ecd3de3",
    ),
    "gscn_vtable": (
        0x00F2FFC0,
        0x00F2FFE0,
        "2777420d88b90bd0cb7d82182f1d4e1734827f7ef7608c75c640c53be30e94d3",
    ),
    "gscn_ctor": (
        0x005E3720,
        0x005E37AD,
        "9865e2a746720025a6df41edb1854b7d7206c2da410aa9ae916d26c296d1b011",
    ),
    "gscn_codec": (
        0x005E3EE0,
        0x005E404E,
        "ea5a21f39f095780b3f83fec2d465f3fe435f6b0ffc04a1e67107ffad489ea60",
    ),
    "gscn_handler": (
        0x005E4060,
        0x005E41CD,
        "85ff71ffceff5345f94facc9b7fa1c39c8efd2e429248d112cdba578d3df944e",
    ),
    "typed_bridge": (
        0x005F53A0,
        0x005F5456,
        "77136c150b0e557ad4facea096191de0fb9f23e9c30ee5c550c8fa6594b33894",
    ),
    "pool_factory": (
        0x005E3D70,
        0x005E3EE0,
        "d71350bc21f8e5956d34b16b359947e2f5a723aff36ed9c9662f3aa8ea1efb22",
    ),
    "terrain_factory_codec_prefix": (
        0x005F82C0,
        0x005F85B0,
        "680e050c1c8fb6316045ff1eb484321bbdb021822181df73cdd8187d3bc929df",
    ),
    "terrain_codec": (
        0x005F85B0,
        0x005F8869,
        "ce0a58f72c5798f1d5263ebdb5ee449659ed04e2974f63f77657ea968a4f1b5b",
    ),
    "reconcile": (
        0x006AF970,
        0x006B03E3,
        "e5eb9e1fdae15544773c7e94fa6ff6aaa6990650cbb05f20e39a009941575663",
    ),
    "wrapper_factory": (
        0x006AF720,
        0x006AF8C0,
        "baf5da9cfa369316144e775492316ae327d9bb5c4ce503e14b60609962c9e132",
    ),
    "module_vtable": (
        0x00F3DD38,
        0x00F3DD84,
        "e6540cd1d07c1df5de7850f7797f91f9627c80692ead030cd48891b3344954a6",
    ),
    "module_ctor": (
        0x006B0730,
        0x006B07AB,
        "58d075ac14d37ece3c7cbf23cf43a48412a7fb9e6537846c28d86b8e01962f94",
    ),
    "module_click": (
        0x006B03F0,
        0x006B069B,
        "a393f3d41b7f389fac31bc82a7cf4e78367d0413a5427d5dfe91d762b9685827",
    ),
    "module_dtor": (
        0x006B06A0,
        0x006B0730,
        "67d53fc315fe26ec83eb7d7038d61efdb124c80ba6404619a29fa805054e7de1",
    ),
    "dropobj_vtable": (
        0x00F30FAC,
        0x00F30FDC,
        "d5e4811779c1c30cbbe0c912b7e3000bc4c10d2d1c40c6d406e3be61666637ff",
    ),
    "dropobj_ctor": (
        0x005F49C0,
        0x005F4AEA,
        "f4dd4e94aa07f0a1307c1ae992d3811167d2ceb3460a8f69e2da7be42eb14cf9",
    ),
    "dropobj_init": (
        0x005F41E0,
        0x005F4897,
        "d8011e41a99fef62e6c311e804b715b20f3187dc57128276e35b947a7510f105",
    ),
    "dropobj_refresh": (
        0x005F48A0,
        0x005F48DF,
        "ef2920f53ff2027342043aeaa9ea05b0668c0b9f4c9c3fd368e06533618c5ed7",
    ),
    "dropobj_label_toggle": (
        0x005F48E0,
        0x005F4926,
        "9d90683cef76debd6a0da466a377d4f6ab1cbee6b98752c45fa1135b0fdda499",
    ),
    "dropobj_update": (
        0x005F4C00,
        0x005F4DEE,
        "7b14d16ca60fc6917328cc9a59f8c8f7ab6e13052eac3764c69dae45d41c06c2",
    ),
    "dropobj_dtor": (
        0x005F5060,
        0x005F5164,
        "17b1a602e280f3c0de6f2288ff5cd683b1cd47eb05c2db0aea109c4454ab024b",
    ),
    "dropobj_delete_dtor": (
        0x005F5170,
        0x005F51CE,
        "9ed9b950da3809f83e2cf9afa98ebe97aab0da9fae341ff90d5058468edba4e2",
    ),
    "all_label_refresh": (
        0x006AF8C0,
        0x006AF954,
        "f0a4c2e524f8e2732bd88a29ea715c0b178412ab1a02428a01c2fcc48966a4d8",
    ),
    "label_action": (
        0x005CFE2A,
        0x005CFE70,
        "de6d322803f866bd5fbfaf28625f447281dd26d6b4d260f3b8e5343345fd92d1",
    ),
    "dropmodel_field_gate": (
        0x005F426D,
        0x005F42B9,
        "8ca63cf136e534c198d532aef7ef93bd77e0549491c8f44f52d989792db336d9",
    ),
    "drop_fall_fx": (
        0x005F42B9,
        0x005F433C,
        "ddb02919c9bffb57f59bba52bc6039bb92804d02d0540cfe7771ef51f08dc019",
    ),
    "drop_tag_fx": (
        0x005F433C,
        0x005F44F3,
        "f4ad679ee841f32ed6c02f195a662e8a65a63c3b5853bb8694b3bf5c3c20dd5a",
    ),
    "drop_nif_path_load": (
        0x005F44F3,
        0x005F45F7,
        "40de45ab23d34b131f8cd30ae7ee3c3dff1238715c9e4719a2493ff02213f6fb",
    ),
    "drop_loader": (
        0x00B1B6C0,
        0x00B1B7A9,
        "bb3c6bc134370f5874a362436c91a1df398f2f87535eca93c0b28a9b35ff5c22",
    ),
    "drop_resource_open": (
        0x008AD740,
        0x008AD7E5,
        "1371bf938235634999d4a7e620eb786a2ebfcb09989046bccd2af617712e1706",
    ),
    "resolver_install": (
        0x0040AF9C,
        0x0040AFB0,
        "2c32966749423e1158c563e64dc915f93ef1fb0dafff3adb4125b44de08ba753",
    ),
    "path_open_dispatch": (
        0x00790EC0,
        0x00790EC6,
        "e25db57c37ed4f23f974998c5093448021de3f46eab7e07966098db4b78ff05a",
    ),
    "path_open_setter": (
        0x00790F00,
        0x00790F18,
        "51849672a9869c43837ef5c7c36e799ce618fa95b97703626eee592f8592b7b9",
    ),
    "stream_file_bridge": (
        0x008AD3D0,
        0x008AD412,
        "3619d1405a5011cdeb72d81a09685549c2c07bd9b2d286049f92d8c2c424de41",
    ),
    "nistream_vtable": (
        0x00F5B598,
        0x00F5B5F0,
        "8fa5b70c50ac26e37affc488fd8120d3098cec16d21a069909b172df105bb0ab",
    ),
    "nistream_ctor_prefix": (
        0x008B10C0,
        0x008B1180,
        "fb71309c57bed927ea392e05fb3221e79f85f2cddd88be71f6cf472648b41e22",
    ),
    "nistream_parser_prefix": (
        0x008B0CC0,
        0x008B0D6A,
        "624ddd8e80d9e872bf663b015b1def574873f61fee684d9ca124e398775a05e9",
    ),
    "custom_file_ctor": (
        0x00B01FE0,
        0x00B02169,
        "3683f8252e4153816ec2920296bbb20fb1653a4350dd7819a5922cc00978d1b8",
    ),
    "mode_jump_table": (
        0x00B0216C,
        0x00B02184,
        "36f00f96fbf2d937646122859ff07a3af360b23cb373051c90cd27070998e016",
    ),
    "custom_open_callback": (
        0x00B02300,
        0x00B023B0,
        "d742dd309c8371eab42ee866e8bc57af00d49f45d5424ac70f29f1d202834e3c",
    ),
    "wrapper_store": (
        0x00B024F0,
        0x00B0253B,
        "30c79ead7dfdf986f28ce7f46879e65a1a39756ba9a67f902902c2d30d105c6f",
    ),
    "pcz_decode_wrapper": (
        0x00B7A5C0,
        0x00B7A62C,
        "041725fb948bb5db4e114c854f77f62038d665583976c2f438477a3a395a95ec",
    ),
    "extension_rewrite": (
        0x00B7A780,
        0x00B7A8D2,
        "83c779a1d4de676178a114f6dfffd451921dea99011ee89fffc7949b79cd7537",
    ),
    "packaged_read_decode": (
        0x00B7A930,
        0x00B7AA4B,
        "c5582e4c0612a87d80beb4a970c9d3fe1502ee20a05ed954dae107eb23c57af1",
    ),
    "lzma_decode_core": (
        0x00A268B0,
        0x00A269EC,
        "28b93684824e3950bbfa016bc37d016f22b68985495246ce92a2565ebef328a1",
    ),
    "ninode_ctor": (
        0x008B3360,
        0x008B342F,
        "097fa9b35ae537cc3e233426052eb07e9b0b8e9c12051e8082bd6e9c1ac1e15b",
    ),
    "ninode_rtti_init": (
        0x00C13FB0,
        0x00C13FC5,
        "e2fb498ac2f0b924a57706b6cbf8288e9f3bcbb0b3f47b39001615cfdcdb5e05",
    ),
    "drop_type_filter": (
        0x00877740,
        0x0087777B,
        "38ae18cd3fe7f47ff4498394feefb7dbf4f3272851b4d8d9dec314216f2daf4c",
    ),
    "drop_xyz_activation": (
        0x005F4650,
        0x005F46C4,
        "1df43b3aea0ac59fdde8bbaae1d3d5b3e4b89a6eb401fec97ec24dc3c87c8bb9",
    ),
    "drop_nameboard": (
        0x005F46C4,
        0x005F4863,
        "51414c46b13fa18b3a6bafc9fdc20e9e210ef2732d3c8acd2635724d2d7548da",
    ),
    "dropmodel_token_table": (
        0x010255E4,
        0x0102561C,
        "0694e6bf360899b557bbcaeb318cd880653b1100595547d39b167d162f210f29",
    ),
    "pe_entry_stub": (
        0x00B83122,
        0x00B83128,
        "10d5f6435c5ee634c1b5f924eef15d6e0a64515170ecec4511ce1b9e5add3774",
    ),
    "cli_header": (
        0x00F95528,
        0x00F95570,
        "f3679e32caf1f5d99028021d1c1674ce9a849a16800668909a40dd74dd35c0eb",
    ),
    "managed_entry": (
        0x00B38225,
        0x00B3822F,
        "19398f5af7688c1dd8ab7039498402628e868a63a530c5d6a61a50b63ca51e57",
    ),
    "crt_to_winmain": (
        0x00B38088,
        0x00B380A5,
        "1ca038d7f56a23eb8742d150d386e41d86759d70470d83059751ac998b210384",
    ),
    "winmain_to_app_init": (
        0x00A2A28A,
        0x00A2A2B4,
        "163048a67869aaece7b1256a0deaf55bfaf743b54ec0df8f9275296c51262a7b",
    ),
    "app_init_install": (
        0x0040AE70,
        0x0040AFB0,
        "e6108170282f061dd09005353e430f732dd7333b99d1ed9c62d26b11fbde8f24",
    ),
    "app_init_object_return": (
        0x0040B0E1,
        0x0040B270,
        "963266a212c5f5af45b931b94c75481ce633df8e9ee7d176de17df6284696080",
    ),
    "world_register": (
        0x00B0E4A0,
        0x00B0E7BB,
        "834233a43232a312f64ab8fb95a08e133acc75e2f993203c7a320fe42b5449c0",
    ),
    "dropobj_world_bind": (
        0x005F4110,
        0x005F4175,
        "3bb4c223bff4effdc7c552b3eab5a9a339c37d7108f71ffbf9add7035050abd6",
    ),
    "scene_graph_bind": (
        0x00B1DA60,
        0x00B1DA8B,
        "08b8627629ab340d0422c96435d047f44161a810f4054b466d4e99056806c90c",
    ),
    "scene_graph_traverse": (
        0x00B1D8D0,
        0x00B1DA55,
        "5ea2a7e5a2f3ed67313a5b5ed5ec32ec7c4253332c57fd57b95d5c97d2ffd80c",
    ),
    "scene_activate": (
        0x00B1CD30,
        0x00B1CDE9,
        "4f085422ed84f84eaf72d2f4f6dfb548fd9feca702429cf485d03a2e9b169603",
    ),
    "scene_node_getter": (
        0x008F7730,
        0x008F7734,
        "ef9cb0387790b6d8dd04c53a8d88d9f74cbc72289d3efab4dcc86f7bf84c2850",
    ),
}


def span_label(name: str, pe: PE32) -> str:
    start, end, digest = SPAN_SPECS[name]
    return (
        f"0x{start:08X}..0x{end:08X}"
        f"@file_off=0x{pe.va_to_offset(start):08X}..0x{pe.va_to_offset(end):08X}"
        f"@sha256={digest}"
    )


def weighted_name_id(name: str) -> int:
    total = 0
    for index, byte in enumerate(name.encode("ascii"), start=1):
        signed = byte if byte < 0x80 else byte - 0x100
        total += signed * index
    return total & 0xFFFF


def call_target(pe: PE32, call_va: int) -> int:
    offset = pe.va_to_offset(call_va)
    if pe.data[offset] != 0xE8:
        raise ValueError(f"0x{call_va:08X} is not a direct call")
    relative = struct.unpack_from("<i", pe.data, offset + 1)[0]
    return (call_va + 5 + relative) & 0xFFFFFFFF


def direct_calls_in_span(pe: PE32, start_va: int, end_va: int) -> dict[int, int]:
    calls: dict[int, int] = {}
    data = pe.span(start_va, end_va)
    for index in range(0, len(data) - 4):
        if data[index] != 0xE8:
            continue
        source = start_va + index
        relative = struct.unpack_from("<i", data, index + 1)[0]
        calls[source] = (source + 5 + relative) & 0xFFFFFFFF
    return calls


def require_direct_call(pe: PE32, call_va: int, target_va: int) -> None:
    actual = call_target(pe, call_va)
    if actual != target_va:
        raise ValueError(
            f"call mismatch at 0x{call_va:08X}: 0x{actual:08X} != 0x{target_va:08X}"
        )


def require_instruction(pe: PE32, va: int, expected: bytes, label: str) -> None:
    """Fail closed when one decisive instruction sequence changes."""
    offset = pe.va_to_offset(va)
    actual = pe.data[offset : offset + len(expected)]
    if actual != expected:
        raise ValueError(f"instruction mismatch: {label} at 0x{va:08X}")


def require_short_branch(
    pe: PE32,
    va: int,
    opcode: int,
    target_va: int,
    label: str,
) -> None:
    """Verify an exact rel8 conditional edge, not merely its enclosing span."""
    offset = pe.va_to_offset(va)
    if pe.data[offset] != opcode:
        raise ValueError(f"branch opcode mismatch: {label} at 0x{va:08X}")
    relative = struct.unpack_from("<b", pe.data, offset + 1)[0]
    actual = (va + 2 + relative) & 0xFFFFFFFF
    if actual != target_va:
        raise ValueError(
            f"branch target mismatch: {label} at 0x{va:08X}: "
            f"0x{actual:08X} != 0x{target_va:08X}"
        )


def require_rel32_jump(pe: PE32, va: int, target_va: int, label: str) -> None:
    offset = pe.va_to_offset(va)
    if pe.data[offset] != 0xE9:
        raise ValueError(f"jump opcode mismatch: {label} at 0x{va:08X}")
    relative = struct.unpack_from("<i", pe.data, offset + 1)[0]
    actual = (va + 5 + relative) & 0xFFFFFFFF
    if actual != target_va:
        raise ValueError(
            f"jump target mismatch: {label} at 0x{va:08X}: "
            f"0x{actual:08X} != 0x{target_va:08X}"
        )


def absolute_u32_occurrences(pe: PE32, value: int) -> tuple[tuple[str, int], ...]:
    """Whole-image file-backed-section byte census of one absolute u32."""
    needle = struct.pack("<I", value)
    found: list[tuple[str, int]] = []
    for section in pe.sections:
        raw = pe.data[section.raw_offset : section.raw_offset + section.raw_size]
        cursor = 0
        while True:
            index = raw.find(needle, cursor)
            if index < 0:
                break
            found.append(
                (
                    section.name,
                    pe.image_base + section.virtual_address + index,
                )
            )
            cursor = index + 1
    return tuple(found)


def direct_call_xrefs(pe: PE32, target_va: int) -> tuple[tuple[str, int], ...]:
    """Whole-image file-backed-section byte-pattern census of E8 rel32 targets."""
    found: list[tuple[str, int]] = []
    for section in pe.sections:
        raw = pe.data[section.raw_offset : section.raw_offset + section.raw_size]
        for index in range(0, max(0, len(raw) - 4)):
            if raw[index] != 0xE8:
                continue
            source = pe.image_base + section.virtual_address + index
            relative = struct.unpack_from("<i", raw, index + 1)[0]
            if (source + 5 + relative) & 0xFFFFFFFF == target_va:
                found.append((section.name, source))
    return tuple(found)


def managed_entry_method(pe: PE32) -> dict[str, int | str]:
    """Parse the CLI header and ECMA-335 tables needed for the entry MethodDef."""
    if pe.com_descriptor_size < 0x48 or pe.com_descriptor_rva == 0:
        raise ValueError("missing CLI header")
    cli = pe.rva_to_offset(pe.com_descriptor_rva)
    if pe.u32_offset(cli) != 0x48:
        raise ValueError("unexpected CLI header size")
    metadata_rva = pe.u32_offset(cli + 8)
    metadata_size = pe.u32_offset(cli + 12)
    cli_flags = pe.u32_offset(cli + 16)
    token = pe.u32_offset(cli + 20)
    if token >> 24 != 0x06 or (token & 0x00FFFFFF) == 0:
        raise ValueError("CLI entry token is not a MethodDef")

    root = pe.rva_to_offset(metadata_rva)
    if pe.data[root : root + 4] != b"BSJB":
        raise ValueError("missing CLI metadata signature")
    version_length = pe.u32_offset(root + 12)
    cursor = root + 16 + version_length
    _metadata_flags, stream_count = struct.unpack_from("<HH", pe.data, cursor)
    cursor += 4
    streams: dict[str, tuple[int, int]] = {}
    for _ in range(stream_count):
        stream_offset, stream_size = struct.unpack_from("<II", pe.data, cursor)
        cursor += 8
        name_end = pe.data.index(b"\0", cursor)
        name = pe.data[cursor:name_end].decode("ascii")
        cursor += ((name_end - cursor + 1 + 3) // 4) * 4
        streams[name] = (root + stream_offset, stream_size)
    if "#~" not in streams or "#Strings" not in streams:
        raise ValueError("required CLI metadata streams missing")

    tables, tables_size = streams["#~"]
    strings, strings_size = streams["#Strings"]
    heap_sizes = pe.data[tables + 6]
    valid = struct.unpack_from("<Q", pe.data, tables + 8)[0]
    cursor = tables + 24
    row_counts = [0] * 64
    for table in range(64):
        if valid & (1 << table):
            row_counts[table] = pe.u32_offset(cursor)
            cursor += 4

    string_size = 4 if heap_sizes & 0x01 else 2
    guid_size = 4 if heap_sizes & 0x02 else 2
    blob_size = 4 if heap_sizes & 0x04 else 2

    def index_size(table: int) -> int:
        return 2 if row_counts[table] < 0x10000 else 4

    def coded_size(tables_used: tuple[int, ...], tag_bits: int) -> int:
        maximum = max((row_counts[table] for table in tables_used), default=0)
        return 2 if maximum < (1 << (16 - tag_bits)) else 4

    row_sizes = {
        0: 2 + string_size + guid_size * 3,
        1: coded_size((0, 26, 35, 1), 2) + string_size * 2,
        2: 4 + string_size * 2 + coded_size((2, 1, 27), 2)
        + index_size(4) + index_size(6),
        3: index_size(4),
        4: 2 + string_size + blob_size,
        5: index_size(6),
        6: 4 + 2 + 2 + string_size + blob_size + index_size(8),
    }
    table_offsets: dict[int, int] = {}
    for table in range(7):
        if row_counts[table]:
            table_offsets[table] = cursor
            cursor += row_counts[table] * row_sizes[table]
    if cursor > tables + tables_size:
        raise ValueError("CLI metadata table prefix exceeds stream")

    rid = token & 0x00FFFFFF
    if rid > row_counts[6] or 6 not in table_offsets:
        raise ValueError("CLI entry MethodDef RID is out of range")
    method = table_offsets[6] + (rid - 1) * row_sizes[6]
    method_rva = pe.u32_offset(method)
    impl_flags, method_flags = struct.unpack_from("<HH", pe.data, method + 4)
    name_index_offset = method + 8
    name_index = int.from_bytes(
        pe.data[name_index_offset : name_index_offset + string_size], "little"
    )

    def metadata_string(index: int) -> str:
        if index < 0 or index >= strings_size:
            raise ValueError("CLI string index out of range")
        start = strings + index
        end = pe.data.index(b"\0", start, strings + strings_size)
        return pe.data[start:end].decode("utf-8")

    owner = ""
    if row_counts[2] and 2 in table_offsets:
        typedef_size = row_sizes[2]
        method_index_offset = (
            4 + string_size * 2 + coded_size((2, 1, 27), 2) + index_size(4)
        )
        owner_rid = 0
        for type_rid in range(1, row_counts[2] + 1):
            entry = table_offsets[2] + (type_rid - 1) * typedef_size
            first_method = int.from_bytes(
                pe.data[
                    entry + method_index_offset :
                    entry + method_index_offset + index_size(6)
                ],
                "little",
            )
            next_method = row_counts[6] + 1
            if type_rid < row_counts[2]:
                following = entry + typedef_size
                next_method = int.from_bytes(
                    pe.data[
                        following + method_index_offset :
                        following + method_index_offset + index_size(6)
                    ],
                    "little",
                )
            if first_method <= rid < next_method:
                owner_rid = type_rid
                owner_name_index = int.from_bytes(
                    pe.data[entry + 4 : entry + 4 + string_size], "little"
                )
                owner = metadata_string(owner_name_index)
                break
        if owner_rid == 0:
            raise ValueError("CLI entry MethodDef owner not found")

    return {
        "token": token,
        "rva": method_rva,
        "va": pe.image_base + method_rva,
        "impl_flags": impl_flags,
        "flags": method_flags,
        "name": metadata_string(name_index),
        "owner": owner,
        "cli_flags": cli_flags,
        "metadata_rva": metadata_rva,
        "metadata_size": metadata_size,
    }


@dataclass(frozen=True)
class NifStructure:
    decoded_size: int
    decoded_sha256: str
    block_count: int
    root_count: int
    root_index: int
    reachable_ninode: int
    reachable_billboard: int
    reachable_nimesh: int
    reachable_particle: int
    reachable_nimesh_material_refs: int
    reachable_nimesh_texturing_refs: int
    reachable_nimesh_base_source_refs: int
    reachable_nimesh_external_dds_refs: int


def decode_pcz(raw: bytes) -> bytes:
    if len(raw) < 13 or raw[:4] != b"$pcz":
        raise ValueError("packaged asset lacks $pcz header")
    declared_size = struct.unpack_from("<I", raw, 4)[0]
    prop = raw[8]
    lc = prop % 9
    remainder = prop // 9
    lp = remainder % 5
    pb = remainder // 5
    if pb > 4:
        raise ValueError("invalid LZMA properties")
    dictionary_size = struct.unpack_from("<I", raw, 9)[0]
    decoded = lzma.decompress(
        raw[13:],
        format=lzma.FORMAT_RAW,
        filters=[
            {
                "id": lzma.FILTER_LZMA1,
                "dict_size": dictionary_size,
                "lc": lc,
                "lp": lp,
                "pb": pb,
            }
        ],
    )
    if len(decoded) != declared_size:
        raise ValueError("$pcz declared decoded size mismatch")
    return decoded


def parse_nif_structure(decoded: bytes) -> NifStructure:
    cursor = decoded.index(b"\n") + 1
    header = decoded[:cursor].decode("ascii")
    if header != "Gamebryo File Format, Version 30.1.0.2\n":
        raise ValueError("unexpected NIF header")

    def take_u16() -> int:
        nonlocal cursor
        value = struct.unpack_from("<H", decoded, cursor)[0]
        cursor += 2
        return value

    def take_u32() -> int:
        nonlocal cursor
        value = struct.unpack_from("<I", decoded, cursor)[0]
        cursor += 4
        return value

    version = take_u32()
    endian = decoded[cursor]
    cursor += 1
    user_version = take_u32()
    block_count = take_u32()
    if (version, endian, user_version) != (0x1E010002, 1, 0):
        raise ValueError("unexpected NIF version tuple")
    header_extra_size = take_u32()
    cursor += header_extra_size
    block_type_count = take_u16()
    block_types: list[str] = []
    for _ in range(block_type_count):
        length = take_u32()
        block_types.append(decoded[cursor : cursor + length].decode("ascii"))
        cursor += length
    block_type_indices = [take_u16() for _ in range(block_count)]
    if any(index >= block_type_count for index in block_type_indices):
        raise ValueError("NIF block type index out of range")
    block_sizes = [take_u32() for _ in range(block_count)]
    string_count = take_u32()
    _maximum_string_length = take_u32()
    strings: list[bytes] = []
    for _ in range(string_count):
        length = take_u32()
        if cursor + length > len(decoded):
            raise ValueError("NIF string table entry exceeds decoded file")
        strings.append(decoded[cursor : cursor + length])
        cursor += length
    group_count = take_u32()
    cursor += group_count * 4
    if cursor > len(decoded):
        raise ValueError("NIF header tables exceed decoded file")

    block_starts: list[int] = []
    for size in block_sizes:
        block_starts.append(cursor)
        cursor += size
    if cursor + 4 > len(decoded):
        raise ValueError("NIF block area exceeds decoded file")
    root_count = take_u32()
    roots: list[int] = []
    for _ in range(root_count):
        roots.append(struct.unpack_from("<i", decoded, cursor)[0])
        cursor += 4
    if cursor != len(decoded):
        raise ValueError("NIF parser did not consume the decoded file exactly")
    if root_count != 1 or len(roots) != 1:
        raise ValueError("audited NIF does not have exactly one footer root")
    root_index = roots[0]
    if not 0 <= root_index < block_count:
        raise ValueError("NIF footer root index out of range")
    names = [block_types[index] for index in block_type_indices]
    if names[root_index] != "NiNode":
        raise ValueError("NIF footer root is not NiNode")

    def object_net_end(index: int) -> int:
        start = block_starts[index]
        end = start + block_sizes[index]
        local = start

        def local_u32() -> int:
            nonlocal local
            if local + 4 > end:
                raise ValueError("NIF node field exceeds block")
            value = struct.unpack_from("<I", decoded, local)[0]
            local += 4
            return value

        name_index = local_u32()
        if name_index != 0xFFFFFFFF and name_index >= string_count:
            raise ValueError("NIF object name string index out of range")
        extra_count = local_u32()
        if local + extra_count * 4 + 4 > end:
            raise ValueError("NIF object extra-data array exceeds block")
        extra_refs = tuple(
            struct.unpack_from("<i", decoded, local + ref_index * 4)[0]
            for ref_index in range(extra_count)
        )
        if any(ref < -1 or ref >= block_count for ref in extra_refs):
            raise ValueError("NIF object extra-data reference out of range")
        local += extra_count * 4
        controller_ref = struct.unpack_from("<i", decoded, local)[0]
        if controller_ref < -1 or controller_ref >= block_count:
            raise ValueError("NIF object controller reference out of range")
        local += 4
        return local

    def av_object_fields(index: int) -> tuple[tuple[int, ...], int]:
        end = block_starts[index] + block_sizes[index]
        local = object_net_end(index)
        local += 2 + 12 + 36 + 4  # flags, translation, rotation, scale
        if local + 4 > end:
            raise ValueError("NIF AVObject transform exceeds block")
        property_count = struct.unpack_from("<I", decoded, local)[0]
        local += 4
        if local + property_count * 4 + 4 > end:
            raise ValueError("NIF AVObject property array exceeds block")
        properties = tuple(
            struct.unpack_from("<i", decoded, local + ref_index * 4)[0]
            for ref_index in range(property_count)
        )
        if any(ref < -1 or ref >= block_count for ref in properties):
            raise ValueError("NIF AVObject property reference out of range")
        local += property_count * 4
        collision_ref = struct.unpack_from("<i", decoded, local)[0]
        if collision_ref < -1 or collision_ref >= block_count:
            raise ValueError("NIF AVObject collision reference out of range")
        local += 4
        return properties, local

    def node_children(index: int) -> tuple[int, ...]:
        end = block_starts[index] + block_sizes[index]
        _properties, local = av_object_fields(index)
        if local + 4 > end:
            raise ValueError("NIF node child count exceeds block")
        child_count = struct.unpack_from("<I", decoded, local)[0]
        local += 4
        if local + child_count * 4 > end:
            raise ValueError("NIF node child array exceeds block")
        children = tuple(
            struct.unpack_from("<i", decoded, local + index * 4)[0]
            for index in range(child_count)
        )
        if any(child < -1 or child >= block_count for child in children):
            raise ValueError("NIF node child index out of range")
        return children

    reachable: set[int] = set()
    pending = [root_index]
    while pending:
        index = pending.pop()
        if index < 0 or index in reachable:
            continue
        reachable.add(index)
        if names[index] in {"NiNode", "NiBillboardNode"}:
            pending.extend(node_children(index))
    counts = Counter(names[index] for index in reachable)
    material_refs = 0
    texturing_refs = 0
    base_source_refs = 0
    external_dds_refs = 0
    for index in sorted(reachable):
        if names[index] != "NiMesh":
            continue
        properties, _after_collision = av_object_fields(index)
        property_types = [names[ref] for ref in properties if ref >= 0]
        mesh_material_refs = property_types.count("NiMaterialProperty")
        mesh_texturing = [
            ref
            for ref in properties
            if ref >= 0 and names[ref] == "NiTexturingProperty"
        ]
        if mesh_material_refs != 1 or len(mesh_texturing) != 1:
            raise ValueError(
                "reachable NiMesh does not have exactly one material and "
                "texturing property reference"
            )
        material_refs += mesh_material_refs
        texturing_refs += len(mesh_texturing)
        texturing_index = mesh_texturing[0]
        texturing_end = block_starts[texturing_index] + block_sizes[texturing_index]
        local = object_net_end(texturing_index)
        if local + 2 + 4 + 1 + 4 > texturing_end:
            raise ValueError("NIF texturing-property base descriptor exceeds block")
        local += 2  # property flags
        texture_slot_count = struct.unpack_from("<I", decoded, local)[0]
        local += 4
        if texture_slot_count != 9:
            raise ValueError("unexpected NIF texturing-property slot count")
        has_base_texture = decoded[local]
        local += 1
        if has_base_texture != 1:
            raise ValueError("reachable NiMesh lacks a base texture descriptor")
        source_index = struct.unpack_from("<i", decoded, local)[0]
        if not 0 <= source_index < block_count:
            raise ValueError("NIF base texture source reference out of range")
        if names[source_index] != "NiSourceTexture":
            raise ValueError("NIF base texture does not reference NiSourceTexture")
        base_source_refs += 1

        source_end = block_starts[source_index] + block_sizes[source_index]
        source_local = object_net_end(source_index)
        if source_local + 1 + 4 > source_end:
            raise ValueError("NIF source-texture external record exceeds block")
        use_external = decoded[source_local]
        source_local += 1
        if use_external != 1:
            raise ValueError("reachable NiMesh base texture is not external")
        file_name_index = struct.unpack_from("<I", decoded, source_local)[0]
        if file_name_index >= string_count:
            raise ValueError("NIF source-texture filename index out of range")
        if not strings[file_name_index].lower().endswith(b".dds"):
            raise ValueError("reachable NiMesh base texture is not a DDS reference")
        external_dds_refs += 1
    return NifStructure(
        decoded_size=len(decoded),
        decoded_sha256=sha256(decoded),
        block_count=block_count,
        root_count=root_count,
        root_index=root_index,
        reachable_ninode=counts["NiNode"],
        reachable_billboard=counts["NiBillboardNode"],
        reachable_nimesh=counts["NiMesh"],
        reachable_particle=counts["NiPSMeshParticleSystem"],
        reachable_nimesh_material_refs=material_refs,
        reachable_nimesh_texturing_refs=texturing_refs,
        reachable_nimesh_base_source_refs=base_source_refs,
        reachable_nimesh_external_dds_refs=external_dds_refs,
    )


def verify_image() -> tuple[bytes, PE32]:
    data = IMAGE_PATH.read_bytes()
    if len(data) != EXPECTED_IMAGE_SIZE:
        raise ValueError("image size mismatch")
    if sha256(data) != EXPECTED_IMAGE_SHA256:
        raise ValueError("image SHA-256 mismatch")
    pe = PE32(data)
    if pe.image_base != 0x00400000:
        raise ValueError("unexpected image base")

    for name, (start, end, expected) in SPAN_SPECS.items():
        actual = sha256(pe.span(start, end))
        if actual != expected:
            raise ValueError(f"span mismatch: {name}")

    expected_ascii = {
        0x00F2FFF8: "GSCN_RunTimeProtocolRes",
        0x00F0BAD0: "DropThingModule_Client",
        0x0101FFA4: ".?AVTerrainThing@@",
        0x0101FFC0: ".?AVTerrainThingPool@@",
        0x0101C220: ".?AVDropThingGameObj@@",
    }
    if tuple(expected_ascii.items()) != (
        (0x00F2FFF8, "GSCN_RunTimeProtocolRes"),
        (0x00F0BAD0, "DropThingModule_Client"),
        (0x0101FFA4, ".?AVTerrainThing@@"),
        (0x0101FFC0, ".?AVTerrainThingPool@@"),
        (0x0101C220, ".?AVDropThingGameObj@@"),
    ):
        raise ValueError("ASCII anchor census drift")
    for va, expected in expected_ascii.items():
        if pe.c_string(va) != expected:
            raise ValueError(f"ASCII string mismatch at 0x{va:08X}")
    resolver_ascii = {
        0x00F0CDBC: "rb",
        0x00F0CDB8: "wb",
        0x00F09D34: "r",
        0x00F4BFD8: "w",
        0x00F4BFD4: "a",
        0x00F4BFD0: "ab",
        0x00F0D368: ".nif",
        0x00F724EC: ".tga",
        0x00F5AAE4: ".dds",
        0x00FBBDCC: ".kf",
        0x00F7254C: ".bmp",
        0x00FBBDC4: ".dof",
        0x00FBBDC0: ".sp",
        0x00F7DC70: ".jpg",
        0x00F5B4EC: "Cannot open file.",
        0x00F5B7BC: "NiNode",
    }
    for va, expected in resolver_ascii.items():
        if pe.c_string(va) != expected:
            raise ValueError(f"resolver ASCII string mismatch at 0x{va:08X}")
    expected_utf16 = {
        0x00F0C294: "s_NAME",
        0x00F30F88: "n_DROPMODEL_TYPE",
        0x00F0C190: "n_QUALITY",
        0x00F0C27C: "s_TAG_EXTRA",
        0x00F30EE8: ".\\Data\\GC\\F\\",
    }
    if tuple(expected_utf16.items()) != (
        (0x00F0C294, "s_NAME"),
        (0x00F30F88, "n_DROPMODEL_TYPE"),
        (0x00F0C190, "n_QUALITY"),
        (0x00F0C27C, "s_TAG_EXTRA"),
        (0x00F30EE8, ".\\Data\\GC\\F\\"),
    ):
        raise ValueError("UTF-16 anchor census drift")
    for va, expected in expected_utf16.items():
        if pe.w_string(va) != expected:
            raise ValueError(f"UTF-16 string mismatch at 0x{va:08X}")

    if weighted_name_id("GSCN_RunTimeProtocolRes") != 0x6E9D:
        raise ValueError("GSCN_RunTimeProtocolRes ID mismatch")
    if weighted_name_id("DropThingModule_Client") != 0x651A:
        raise ValueError("DropThingModule_Client ID mismatch")

    gscn_vtable = tuple(pe.u32(0x00F2FFC0 + index * 4) for index in range(8))
    expected_gscn_vtable = (
        0x005E37B0,
        0x005E3C00,
        0x00401B20,
        0x0051DF20,
        0x005E37C0,
        0x005E3EA0,
        0x005E3EE0,
        0x005E4060,
    )
    if gscn_vtable != expected_gscn_vtable:
        raise ValueError("GSCN_RunTimeProtocolRes vtable mismatch")
    if pe.u32(0x00F313C4) != 0x005F81D0:
        raise ValueError("TerrainThing vtable mismatch")
    if pe.u32(0x00F313D4) != 0x005F8900:
        raise ValueError("TerrainThingPool vtable mismatch")

    expected_calls = {
        0x005E40D5: 0x005F53A0,
        0x005F5428: 0x006AF970,
        0x006AFDE9: 0x005F4C00,
        0x006AFF64: 0x00B0EE40,
        0x006AFF84: 0x005E0D40,
        0x006B014F: 0x006AF720,
        0x006B01A0: 0x005F41E0,
        0x006B01BB: 0x00B0E4A0,
        0x006B0211: 0x00708E20,
        0x006B034F: 0x00B0EE40,
        0x006B0368: 0x005E0D40,
        0x006B0653: 0x005DD800,
        0x005CFE6B: 0x006AF8C0,
        0x006AF915: 0x005F48E0,
        0x006AF92A: 0x005F48A0,
        0x005F4276: 0x00892DD0,
        0x005F4291: 0x00891EE0,
        0x005F4576: 0x00B1B6C0,
        0x00B1B72C: 0x008AD740,
        0x00B1B753: 0x00877740,
    }
    if len(expected_calls) != 20 or set(expected_calls) != {
        0x005E40D5,
        0x005F5428,
        0x006AFDE9,
        0x006AFF64,
        0x006AFF84,
        0x006B014F,
        0x006B01A0,
        0x006B01BB,
        0x006B0211,
        0x006B034F,
        0x006B0368,
        0x006B0653,
        0x005CFE6B,
        0x006AF915,
        0x006AF92A,
        0x005F4276,
        0x005F4291,
        0x005F4576,
        0x00B1B72C,
        0x00B1B753,
    }:
        raise ValueError("direct-call anchor census drift")
    for source, target in expected_calls.items():
        require_direct_call(pe, source, target)

    resolver_calls = {
        0x0040AFA1: 0x00790F00,
        0x008AD75C: 0x00793FA0,
        0x008AD76B: 0x0092EAE0,
        0x008AD77A: 0x00790EC0,
        0x00B020E5: 0x00B7A930,
        0x00B02364: 0x00B01FE0,
        0x00B7A61B: 0x00A268B0,
        0x00B7A951: 0x00B7A780,
        0x00B7A9EC: 0x00B7A5C0,
        0x00B7AA26: 0x00B7A5C0,
        0x008B33A6: 0x008EA240,
        0x00C13FBF: 0x008B5830,
    }
    for source, target in resolver_calls.items():
        require_direct_call(pe, source, target)

    if pe.u32(0x0040AF9D) != 0x00B02300:
        raise ValueError("installer-callsite callback immediate mismatch")
    if pe.u32(0x00790EC2) != 0x01027B8C:
        raise ValueError("resource-open dispatch slot mismatch")
    if pe.u32(0x00790F06) != 0x01027B8C or pe.u32(0x00790F13) != 0x01027B8C:
        raise ValueError("resource-open setter slot mismatch")
    expected_mode_targets = (
        0x00B02071,
        0x00B02077,
        0x00B0209F,
        0x00B02081,
        0x00B0208B,
        0x00B02095,
    )
    actual_mode_targets = tuple(
        pe.u32(0x00B0216C + index * 4) for index in range(6)
    )
    if actual_mode_targets != expected_mode_targets:
        raise ValueError("custom-file mode jump table mismatch")
    if pe.u32(0x00B0211C) != 0x00C3B618:
        raise ValueError("loose-file fallback IAT target mismatch")
    if pe.u32(0x00B7A7E4) != 0x00C3B518:
        raise ValueError("case-insensitive extension comparator IAT mismatch")
    if pe.u32(0x00B7A5D4) != 0x7A637024:
        raise ValueError("$pcz magic comparison mismatch")
    if pe.u32(0x00F5B59C) != 0x008AD3D0:
        raise ValueError("NiStream file bridge vtable target mismatch")
    if pe.u32(0x00F5B5EC) != 0x008B0CC0:
        raise ValueError("NiStream parser vtable target mismatch")
    if pe.u32(0x008B10C7) != 0x00F5B598:
        raise ValueError("NiStream constructor vtable mismatch")
    if pe.u32(0x00F30FD4) != 0x00B024F0:
        raise ValueError("DropThingGameObj node-store vtable target mismatch")
    if pe.u32(0x008B3375) != 0x00F5B700:
        raise ValueError("NiNode constructor vtable mismatch")

    expected_imports = {
        0x00C3B518: "_stricmp",
        0x00C3B568: "strncpy_s",
        0x00C3B5E4: "_splitpath_s",
        0x00C3B618: "_fsopen",
        0x00C3B1B0: "InterlockedIncrement",
        0x00C3B1B4: "InterlockedDecrement",
    }
    for iat_va, expected_name in expected_imports.items():
        actual_name = pe.import_name_at_iat(iat_va)
        if actual_name != expected_name:
            raise ValueError(
                f"IAT name mismatch at 0x{iat_va:08X}: "
                f"{actual_name!r} != {expected_name!r}"
            )

    # GDL-IMG-018 decisive stack/CFG assertions. The installer callsite passes
    # a non-NULL callback immediate to the setter, whose non-NULL path writes
    # the dispatch slot. Runtime reachability, ordering, and later overwrite
    # are intentionally not inferred. 0x008AD740 pushes callback args
    # right-to-left as (path, 0, 0x8000, 0); 0x00B02300 forwards those four
    # args into 0x00B01FE0. Its second ctor arg is mode.
    require_instruction(
        pe, 0x0040AF9C, bytes.fromhex("680023b000"), "callback push"
    )
    require_instruction(
        pe, 0x00790F00, bytes.fromhex("8b442404"), "setter callback argument load"
    )
    require_instruction(
        pe,
        0x00790F0E,
        bytes.fromhex("85c07405"),
        "setter non-NULL callback branch",
    )
    require_instruction(
        pe,
        0x00790F12,
        bytes.fromhex("a38c7b0201c3"),
        "setter callback argument write to dispatch slot",
    )
    require_instruction(
        pe,
        0x008AD770,
        bytes.fromhex("6a0068008000006a0056"),
        "resource-open argument order",
    )
    require_instruction(
        pe, 0x00790EC0, bytes.fromhex("ff258c7b0201"), "dispatch through slot"
    )
    require_instruction(
        pe,
        0x00B0234E,
        bytes.fromhex("8b5424308b4c242c528b54242c518b4c242c52518bc8"),
        "callback constructor-argument forwarding",
    )
    require_instruction(
        pe, 0x00B0203A, bytes.fromhex("8b44242c"), "mode argument load"
    )
    require_instruction(
        pe, 0x00B02060, bytes.fromhex("b9bccdf000"), "mode-zero rb literal"
    )
    require_instruction(
        pe,
        0x00B0206A,
        bytes.fromhex("ff24856c21b000"),
        "mode jump-table dispatch",
    )
    require_instruction(
        pe,
        0x00B020D5,
        bytes.fromhex("8b7c24308b6c2428"),
        "buffer size and original-path argument loads",
    )
    require_instruction(
        pe, 0x00B020DD, bytes.fromhex("3bc3"), "rb comparison result test"
    )
    require_short_branch(
        pe, 0x00B020DF, 0x75, 0x00B0210E, "non-rb skips packaged reader"
    )
    require_instruction(
        pe, 0x00B0210A, bytes.fromhex("3ac3"), "packaged result null test"
    )
    require_short_branch(
        pe, 0x00B0210C, 0x75, 0x00B02151, "packaged success skips fallback"
    )
    require_instruction(
        pe,
        0x00B02112,
        bytes.fromhex("8b5424346a205255ff1518b6c300"),
        "fallback uses original path and selected mode",
    )
    require_instruction(
        pe, 0x00B7A930, bytes.fromhex("8b442404"), "packaged reader input path"
    )
    require_instruction(
        pe,
        0x00B7A93F,
        bytes.fromhex("8be98d7d04"),
        "private mutable path buffer selection",
    )
    require_instruction(
        pe, 0x00B7A950, bytes.fromhex("57"), "private path passed to rewriter"
    )
    require_short_branch(
        pe, 0x00B7A95B, 0x75, 0x00B7A967, "rewrite success reaches packaged open"
    )
    require_instruction(
        pe,
        0x00B7A794,
        bytes.fromhex("578bbc240c01000085ff7518"),
        "rewriter argument load into original mutable path register",
    )
    require_instruction(
        pe,
        0x00B7A7E2,
        bytes.fromhex("8b3518b5c300"),
        "case-insensitive comparator load",
    )
    # _splitpath_s receives the private mutable path in EDI and the local
    # 0x100-byte extension buffer. After successful return, push ESI shifts
    # that same local from [esp+4] to [esp+8]; the comparator receives it as
    # string1 and the pinned .nif literal as string2. A zero result branches
    # to the original-path length scan and, for length > 1, the final-byte
    # rewrite. These assertions mechanically tie the literal, comparator,
    # branch edge, and rewrite rather than merely co-locating them in a span.
    require_instruction(
        pe,
        0x00B7A7B8,
        bytes.fromhex("68000100008d44240850"),
        "splitpath extension-size and output-buffer arguments",
    )
    require_instruction(
        pe,
        0x00B7A7C2,
        bytes.fromhex("6a006a006a006a006a006a0057"),
        "splitpath unused outputs and private-path argument",
    )
    require_instruction(
        pe,
        0x00B7A7CF,
        bytes.fromhex("c644242800"),
        "splitpath extension-buffer terminator initialization",
    )
    require_instruction(
        pe,
        0x00B7A7D4,
        bytes.fromhex("ff15e4b5c300"),
        "splitpath import call",
    )
    require_instruction(
        pe,
        0x00B7A7DA,
        bytes.fromhex("83c42485c075bf56"),
        "splitpath cleanup success edge and stack shift",
    )
    require_instruction(
        pe,
        0x00B7A7E8,
        bytes.fromhex("8d4c24086868d3f00051ffd683c40885c0"),
        "extension-buffer and .nif arguments to comparator",
    )
    require_instruction(
        pe,
        0x00B7A7F9,
        bytes.fromhex("0f84a2000000"),
        ".nif allowlist match reaches last-character rewrite",
    )
    require_instruction(
        pe,
        0x00B7A8A1,
        bytes.fromhex("8bc78d5001"),
        "matched-extension branch selects original mutable path",
    )
    require_instruction(
        pe,
        0x00B7A8AD,
        bytes.fromhex("2bc283f801"),
        "original-path final-character length gate",
    )
    require_short_branch(
        pe,
        0x00B7A8B2,
        0x7E,
        0x00B7A8B9,
        "path length at most one skips final-character rewrite",
    )
    require_instruction(
        pe,
        0x00B7A8B4,
        bytes.fromhex("c64407ff5f"),
        "last path character becomes underscore",
    )

    # GDL-IMG-019 decisive decoder/parser assertions.
    require_instruction(
        pe,
        0x00B7A5C3,
        bytes.fromhex("85c0741e8b1185d2741883fa087c1381382470637a750b"),
        "$pcz pointer length and magic guards",
    )
    require_instruction(
        pe,
        0x00B7A5DA,
        bytes.fromhex("8b0e85c9750b8b5004891632c083c40cc3"),
        "$pcz declared-size probe returns false",
    )
    require_instruction(
        pe,
        0x00B7A5EB,
        bytes.fromhex("6804bd0201894c24088d4c240c516a0183c2f36a0589542410"),
        "decoder allocator finish-mode payload-length and property-size args",
    )
    require_instruction(
        pe,
        0x00B7A604,
        bytes.fromhex("8d5008528d4c24145183c00d50"),
        "decoder property and payload pointers",
    )
    require_instruction(
        pe,
        0x00B7AA2B,
        bytes.fromhex("83c40885db7409"),
        "second decoder status is not tested",
    )
    require_instruction(
        pe,
        0x00B7AA3B,
        bytes.fromhex("8b8598010000"),
        "allocated output pointer returned after second call",
    )
    require_short_branch(
        pe, 0x00B1B733, 0x75, 0x00B1B73D, "parser success reaches collection"
    )
    require_instruction(
        pe,
        0x00B1B73D,
        bytes.fromhex("8b8424700100008b0885c9750433c0eb0a6848d20801"),
        "single parsed collection entry and NiNode RTTI argument",
    )
    require_instruction(
        pe,
        0x008AD3F4,
        bytes.fromhex("8b068b50548bce89be98010000ffd2"),
        "NiStream parser vtable call",
    )

    # GDL-IMG-020 decisive retain/type-boundary assertions. The constructor
    # zeros are only a transient default before parsing can populate children.
    require_instruction(
        pe,
        0x00B024F2,
        bytes.fromhex("8b7c240c8bd985ff7507"),
        "node-store NULL guard",
    )
    require_instruction(
        pe, 0x00B02504, bytes.fromhex("8b73783bf7"), "retained node compare"
    )
    require_instruction(
        pe,
        0x00B02526,
        bytes.fromhex("897b7883c70457"),
        "retained node replacement and refcount address",
    )
    require_instruction(
        pe,
        0x008B336D,
        bytes.fromhex("8dbeac000000"),
        "NiNode child-container address",
    )
    require_instruction(
        pe,
        0x008B3379,
        bytes.fromhex("33c933c066894f0a"),
        "NiNode transient child-container zero A",
    )
    require_instruction(
        pe,
        0x008B3385,
        bytes.fromhex("66894708"),
        "NiNode transient child-container zero B",
    )
    require_instruction(
        pe,
        0x008B1171,
        bytes.fromhex("899e5c010000"),
        "NiStream parsed-collection transient zero",
    )

    # GDL-IMG-021 mechanically parses the PE/CLI entry MethodDef and pins the
    # native call/branch chain into normal application initialization.  This is
    # static normal-path reachability, not a claim that a particular process ran.
    if pe.entrypoint_rva != 0x00783122:
        raise ValueError("PE entrypoint RVA mismatch")
    require_instruction(
        pe, 0x00B83122, bytes.fromhex("ff251cbbc300"), "CLR entry stub"
    )
    if pe.import_name_at_iat(0x00C3BB1C) != "_CorExeMain":
        raise ValueError("CLR entry import mismatch")
    entry = managed_entry_method(pe)
    expected_entry = {
        "token": 0x060000BA,
        "rva": 0x00738225,
        "va": 0x00B38225,
        "impl_flags": 0x0085,
        "flags": 0x6016,
        "name": "_WinMainCRTStartup",
        "owner": "<Module>",
        "cli_flags": 0,
        "metadata_rva": 0x00BBC5B8,
        "metadata_size": 0x0000FFF8,
    }
    if entry != expected_entry:
        raise ValueError(f"managed entry MethodDef mismatch: {entry!r}")
    require_direct_call(pe, 0x00B38225, 0x00B387D8)
    require_rel32_jump(
        pe, 0x00B3822A, 0x00B37F65, "managed entry to CRT startup"
    )
    require_direct_call(pe, 0x00B380A0, 0x00A2A180)
    require_direct_call(pe, 0x00A2A299, 0x0040AE70)
    require_instruction(
        pe,
        0x0040AED1,
        bytes.fromhex("84c00f8591000000"),
        "first application-init success edge",
    )
    require_instruction(
        pe, 0x0040AF4D, bytes.fromhex("85c0"), "first failure-dialog result test"
    )
    require_short_branch(
        pe, 0x0040AF4F, 0x75, 0x0040AF63, "first failure-dialog exit edge"
    )
    require_instruction(
        pe,
        0x0040AF63,
        bytes.fromhex("33c0e9ea020000"),
        "first application-init failure returns zero",
    )
    require_instruction(
        pe,
        0x0040AF79,
        bytes.fromhex("5384c07518"),
        "second application-init success edge",
    )
    require_instruction(
        pe,
        0x0040AF8F,
        bytes.fromhex("33c0e9be020000"),
        "second application-init failure returns zero",
    )
    require_instruction(
        pe,
        0x0040AF96,
        bytes.fromhex("ff1544bbc300680023b000"),
        "CoInitialize then resource callback argument",
    )
    require_direct_call(pe, 0x0040AFA1, 0x00790F00)
    require_direct_call(pe, 0x0040B0FD, 0x00790E70)
    require_direct_call(pe, 0x0040B137, 0x0040AAD0)
    require_instruction(
        pe, 0x0040B252, bytes.fromhex("8bc6"), "application object return"
    )
    require_instruction(
        pe,
        0x00A2A29E,
        bytes.fromhex("8bf05d3bf3750f"),
        "WinMain application-object non-NULL continuation",
    )
    slot_occurrences = absolute_u32_occurrences(pe, 0x01027B8C)
    if slot_occurrences != (
        (".text", 0x00790EC2),
        (".text", 0x00790F06),
        (".text", 0x00790F13),
    ):
        raise ValueError(f"whole-image dispatch-slot census drift: {slot_occurrences!r}")
    callback_occurrences = absolute_u32_occurrences(pe, 0x00B02300)
    if callback_occurrences != ((".text", 0x0040AF9D),):
        raise ValueError(
            f"whole-image resource-callback immediate census drift: "
            f"{callback_occurrences!r}"
        )
    setter_call_xrefs = direct_call_xrefs(pe, 0x00790F00)
    if setter_call_xrefs != ((".text", 0x0040AFA1),):
        raise ValueError(
            f"whole-image resource-setter E8 census drift: {setter_call_xrefs!r}"
        )

    # GDL-IMG-022 follows the accepted model root through DropThing storage,
    # world registration, root validation, recursive NiNode child traversal,
    # and activation.  None of these instructions observes a framebuffer.
    if (
        pe.u32(0x00F30FBC),
        pe.u32(0x00F30FC8),
        pe.u32(0x00F30FD4),
    ) != (0x008F7730, 0x005F4110, 0x00B024F0):
        raise ValueError("DropThing scene vtable targets mismatch")
    require_instruction(
        pe,
        0x005F46B4,
        bytes.fromhex("8b86840000008b16508b42288bceffd0"),
        "wrapper model passed through node-store vslot",
    )
    require_instruction(
        pe, 0x008F7730, bytes.fromhex("8b4178c3"), "retained scene-root getter"
    )
    require_instruction(
        pe,
        0x00B0E4D8,
        bytes.fromhex("8b068b50108bceffd285c0"),
        "world registration requires non-NULL scene root",
    )
    require_instruction(
        pe,
        0x00B0E5C7,
        bytes.fromhex("8b068b501c8d8bd800000051538bceffd2"),
        "world registration invokes object bind vslot",
    )
    require_direct_call(pe, 0x005F411E, 0x00B023F0)
    require_direct_call(pe, 0x005F412E, 0x00B1DA60)
    require_direct_call(pe, 0x005F4154, 0x00B1C900)
    require_direct_call(pe, 0x005F4161, 0x00B1CD30)
    require_direct_call(pe, 0x00B1DA80, 0x00B1D8D0)
    require_instruction(
        pe,
        0x00B1D98F,
        bytes.fromhex("6848d208018bcee8a59dd5ff"),
        "recursive traversal NiNode type filter",
    )
    require_instruction(
        pe,
        0x00B1D9A5,
        bytes.fromhex("0fb787b600000033c933f6"),
        "recursive traversal child-count load",
    )
    require_instruction(
        pe,
        0x00B1D9CE,
        bytes.fromhex("8b87b00000008b0488508bcbe8f1feffff"),
        "recursive traversal child-array load and self-call",
    )

    handler = pe.span(0x005E4060, 0x005E41CD)
    if b"\x8B\x4E\x20" not in handler:
        raise ValueError("handler no longer loads message +0x20")
    ctor = pe.span(0x005E3720, 0x005E37AD)
    ctor_zero_fields = (b"\x89\x7E\x1C", b"\x89\x7E\x20", b"\x89\x7E\x24")
    if ctor_zero_fields != (
        b"\x89\x7E\x1C",
        b"\x89\x7E\x20",
        b"\x89\x7E\x24",
    ):
        raise ValueError("constructor zero-field census drift")
    for field_zero in ctor_zero_fields:
        if field_zero not in ctor:
            raise ValueError("GSCN constructor zero-field mismatch")
    codec = pe.span(0x005E3EE0, 0x005E404E)
    if b"\xF6\xC3\x08" not in codec:
        raise ValueError("GSCN codec mask-bit-0x08 test missing")
    reconcile = pe.span(0x006AF970, 0x006B03E3)
    if b"\x83\x79\x2C\x00" not in reconcile:
        raise ValueError("TerrainThingPool count-zero predicate missing")
    if struct.pack("<I", 0x0102234C) not in reconcile:
        raise ValueError("2500-range constant reference missing")
    if pe.u32(0x0102234C) != 2500:
        raise ValueError("2500-range constant mismatch")
    if pe.f32(0x010226FC) != 150.0:
        raise ValueError("pickup range constant mismatch")

    if pe.u32(0x010255E4) != len(TOKEN_BY_TYPE):
        raise ValueError("drop-model token count mismatch")
    token_pointers = tuple(
        pe.u32(0x010255E8 + index * 4)
        for index in range(len(TOKEN_BY_TYPE))
    )
    token_names = tuple(pe.c_string(pointer) for pointer in token_pointers)
    if token_names != TOKEN_BY_TYPE:
        raise ValueError(f"drop-model token table mismatch: {token_names!r}")
    if pe.c_string(0x00F0D368) != ".nif":
        raise ValueError("drop-model extension mismatch")
    expected_hard_gate = bytes.fromhex("83be84000000007559")
    hard_gate_offset = pe.va_to_offset(0x005F45EE)
    if pe.data[hard_gate_offset : hard_gate_offset + len(expected_hard_gate)] != expected_hard_gate:
        raise ValueError("wrapper+0x84 hard-gate bytes mismatch")
    expected_table_load = bytes.fromhex("8b0c95e8550201")
    table_load_offset = pe.va_to_offset(0x005F4506)
    if pe.data[table_load_offset : table_load_offset + len(expected_table_load)] != expected_table_load:
        raise ValueError("direct drop-model token-table load mismatch")

    click_calls = direct_calls_in_span(pe, 0x006B0639, 0x006B0658)
    if click_calls.get(0x006B0653) != 0x005DD800:
        raise ValueError("pickup enqueue join mismatch")
    forbidden_delete_targets = {0x00B0EE40, 0x005E0D40, 0x005E0560}
    if forbidden_delete_targets != {0x00B0EE40, 0x005E0D40, 0x005E0560}:
        raise ValueError("known direct-delete target census drift")
    if forbidden_delete_targets.intersection(click_calls.values()):
        raise ValueError("pickup branch gained a local delete call")

    label_span_names = (
        "label_action",
        "all_label_refresh",
        "dropobj_label_toggle",
        "dropobj_refresh",
    )
    if label_span_names != (
        "label_action",
        "all_label_refresh",
        "dropobj_label_toggle",
        "dropobj_refresh",
    ):
        raise ValueError("label visibility span census drift")
    label_calls: dict[str, dict[int, int]] = {}
    for span_name in label_span_names:
        start, end, _digest = SPAN_SPECS[span_name]
        label_calls[span_name] = direct_calls_in_span(pe, start, end)
    toggle_calls = label_calls["all_label_refresh"]
    if toggle_calls.get(0x006AF915) != 0x005F48E0:
        raise ValueError("label visibility toggle join mismatch")
    for span_name, calls in label_calls.items():
        if forbidden_delete_targets.intersection(calls.values()):
            raise ValueError(
                f"label visibility span gained a known direct delete call: {span_name}"
            )
    if struct.pack("<I", 0x010907E5) not in pe.span(0x005CFE2A, 0x005CFE70):
        raise ValueError("label action global reference missing")
    return data, pe


def read_pinned(path: Path, size: int, digest: str) -> bytes:
    data = path.read_bytes()
    if len(data) != size:
        raise ValueError(f"size mismatch: {path.name}")
    if sha256(data) != digest:
        raise ValueError(f"SHA-256 mismatch: {path.name}")
    return data


def git_read(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(SERVER_ROOT), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        error = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"Git read failed for {args!r}: {error}")
    return completed.stdout


def verify_serverproject_snapshot_identity() -> None:
    metadata = git_read(
        "show",
        "-s",
        "--format=%H%n%cI",
        SERVERPROJECT_SNAPSHOT_COMMIT,
    ).decode("ascii").splitlines()
    expected = [
        SERVERPROJECT_SNAPSHOT_COMMIT,
        SERVERPROJECT_SNAPSHOT_COMMIT_TIME,
    ]
    if metadata != expected:
        raise ValueError(
            "ServerProject snapshot identity mismatch: "
            f"expected={expected!r} actual={metadata!r}"
        )


def read_serverproject_snapshot(path: Path, size: int, digest: str) -> bytes:
    relative = path.relative_to(SERVER_ROOT).as_posix()
    data = git_read("show", f"{SERVERPROJECT_SNAPSHOT_COMMIT}:{relative}")
    if len(data) != size:
        raise ValueError(f"snapshot size mismatch: {relative}")
    if sha256(data) != digest:
        raise ValueError(f"snapshot SHA-256 mismatch: {relative}")
    return data


def observe_serverproject_head() -> str:
    return git_read("rev-parse", "HEAD").decode("ascii").strip()


def worktree_matches_serverproject_snapshot() -> bool:
    for path, (size, digest, _needles) in SERVERPROJECT_SNAPSHOT_PINS.items():
        try:
            data = path.read_bytes()
        except OSError:
            return False
        if len(data) != size or sha256(data) != digest:
            return False
    return True


def verify_serverproject_snapshot() -> dict[str, bytes]:
    verify_serverproject_snapshot_identity()
    expected_paths = {
        V141_PATH,
        RUNTIME_PATH,
        MOB_LOOT_PATH,
        DROP_PRESENCE_PATH,
        FIELD_DROP_TABLES_PATH,
    }
    if set(SERVERPROJECT_SNAPSHOT_PINS) != expected_paths:
        raise ValueError("ServerProject snapshot pin key census drift")
    expected_needles = {
        V141_PATH: (
            b"def make_runtime_res_empty_exact()",
            b"pc += u8tag(0x0B, 0)  # RuntimeRes extension fields absent",
        ),
        RUNTIME_PATH: (
            b"self.mob_loot_cell = mob_loot.DropLedgerCell()",
        ),
        MOB_LOOT_PATH: (
            b"class DropLedgerCell:",
            b"self._lock = threading.Lock()",
            b"def _sweep_locked(self, now: float) -> tuple:",
            b"self._sweep_locked(now)",
            b"def lifetime_seconds(self) -> float:",
            b"def time_left(self, drop_key: int) -> float:",
        ),
        DROP_PRESENCE_PATH: (
            b"def sustain_a_kill(",
            b"frames = mob_loot.refresh_frames(legacy, ledger)",
        ),
        FIELD_DROP_TABLES_PATH: (
            b"# item id -> (table_code, low_id, display_name, drop_model_type)",
            b"ITEMS = {",
        ),
    }
    if set(expected_needles) != expected_paths:
        raise ValueError("ServerProject snapshot needle key census drift")
    verified: dict[str, bytes] = {}
    for path, (size, digest, needles) in SERVERPROJECT_SNAPSHOT_PINS.items():
        if tuple(needles) != expected_needles[path]:
            raise ValueError(f"snapshot needle census drift: {path.name}")
        data = read_serverproject_snapshot(path, size, digest)
        for needle in needles:
            if needle not in data:
                raise ValueError(f"snapshot semantic pin missing: {path.name}")
        if path == RUNTIME_PATH:
            assignment = b"self.mob_loot_cell = mob_loot.DropLedgerCell()"
            if data.count(assignment) != 1:
                raise ValueError("snapshot runtime DropLedgerCell owner census drift")
        verified[str(path)] = data
    if set(verified) != {str(path) for path in expected_paths}:
        raise ValueError("ServerProject snapshot verification census drift")
    return verified


def verify_snapshot_roster(snapshot_code: dict[str, bytes]) -> None:
    source = snapshot_code[str(FIELD_DROP_TABLES_PATH)].decode("utf-8")
    tree = ast.parse(source, filename=str(FIELD_DROP_TABLES_PATH))
    item_value = None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "ITEMS" for target in node.targets):
            item_value = ast.literal_eval(node.value)
            break
    if not isinstance(item_value, dict):
        raise ValueError("field_drop_tables ITEMS assignment missing")
    actual = {
        int(full_id): (int(value[0]), int(value[1]), int(value[3]))
        for full_id, value in item_value.items()
    }
    if actual != EXPECTED_CURRENT_ROSTER:
        raise ValueError(
            "current reconstructed drop roster drift: "
            f"expected={EXPECTED_CURRENT_ROSTER!r} actual={actual!r}"
        )


def verify_data_inputs() -> tuple[
    dict[int, dict[int, tuple[dict[str, str], int]]],
    dict[str, bytes],
    dict[str, NifStructure],
]:
    tables: dict[int, dict[int, tuple[dict[str, str], int]]] = {}
    raw_inputs: dict[str, bytes] = {}
    structures: dict[str, NifStructure] = {}
    for table_code, (path, size, digest) in sorted(DATA_TABLE_PINS.items()):
        raw = read_pinned(path, size, digest)
        raw_inputs[str(path)] = raw
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8")), delimiter="\t")
        required = {"n_ID", "n_DROPMODEL_TYPE"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"DATA schema mismatch: {path.name}")
        indexed: dict[int, tuple[dict[str, str], int]] = {}
        for line_number, row in enumerate(reader, start=2):
            key = int(row["n_ID"])
            if key in indexed:
                raise ValueError(f"duplicate DATA n_ID: {path.name}:{key}")
            indexed[key] = (row, line_number)
        tables[table_code] = indexed

    for full_id, (table_code, low_id, expected_type) in EXPECTED_CURRENT_ROSTER.items():
        row_and_line = tables.get(table_code, {}).get(low_id)
        if row_and_line is None:
            raise ValueError(f"current roster DATA row missing: {full_id}")
        row, _line = row_and_line
        if int(row["n_DROPMODEL_TYPE"]) != expected_type:
            raise ValueError(
                f"current roster drop-model mismatch: {full_id}: "
                f"expected {expected_type}, got {row['n_DROPMODEL_TYPE']}"
            )

    for asset_name, (size, digest) in PACKAGE_ASSET_PINS.items():
        path = DROP_ASSET_ROOT / asset_name
        raw = read_pinned(path, size, digest)
        raw_inputs[str(path)] = raw
        structure = parse_nif_structure(decode_pcz(raw))
        expected = NifStructure(*PACKAGE_NIF_STRUCTURE_PINS[asset_name])
        if structure != expected:
            raise ValueError(
                f"decoded NIF structure mismatch: {asset_name}: "
                f"expected={expected!r} actual={structure!r}"
            )
        structures[asset_name] = structure
    if set(structures) != set(PACKAGE_ASSET_PINS):
        raise ValueError("decoded NIF structure census drift")
    return tables, raw_inputs, structures


def verify_transport_reference() -> dict[str, str]:
    tsv = read_pinned(
        TRANSPORT_TSV_PATH,
        26_924,
        EXPECTED_TRANSPORT_TSV_SHA256,
    )
    read_pinned(TRANSPORT_MD_PATH, 2_779, EXPECTED_TRANSPORT_MD_SHA256)
    reader = csv.DictReader(io.StringIO(tsv.decode("utf-8")), delimiter="\t")
    selected: dict[str, dict[str, str]] = {}
    for row in reader:
        transport_id = row.get("transport_id", "")
        if transport_id in {"GDT-IMG-002", "GDT-IMG-008", "GDT-IMG-009"}:
            selected[transport_id] = row
    if set(selected) != {"GDT-IMG-002", "GDT-IMG-008", "GDT-IMG-009"}:
        raise ValueError("missing canonical ground-drop reference rows")
    expected_subjects = {
        "GDT-IMG-002": "PickupTerrainThing object",
        "GDT-IMG-008": "FightingDropModule_Client",
        "GDT-IMG-009": "FightingDropNotify",
    }
    for selector, subject in expected_subjects.items():
        row = selected[selector]
        if row.get("source") != "IMAGE" or row.get("subject") != subject:
            raise ValueError(f"canonical reference drift: {selector}")
    return {
        selector: selected[selector]["evidence_key"] for selector in sorted(selected)
    }


LIVE_DROP_RE = re.compile(
    r"^(?P<time>\S+) SENT label=MOB_LOOT_DROP frame_bytes=(?P<size>\d+) "
    r"delay=0\.00 late_ms=(?P<late>\d+\.\d+)$"
)
LIVE_HEARTBEAT_RE = re.compile(
    r"^(?P<time>\S+) HEARTBEAT seq=(?P<seq>\d+) pc_len=14$"
)
CONSOLE_DROP_RE = re.compile(
    r"^\[G>\] MOB_LOOT_DROP \((?P<size>\d+) bytes; late=(?P<late>\d+\.\d+) ms\)$"
)
CONSOLE_EMPTY_RE = re.compile(
    r"^\[HB>\] exact empty RuntimeRes v4 #(?P<seq>\d+)$"
)

CAPTURE_PAIR_SPECS = (
    {
        "evidence_id": "GDL-CAP-001",
        "live_drop_line": 1081,
        "live_heartbeat_line": 1087,
        "console_drop_line": 9833,
        "console_empty_line": 9841,
        "frame_bytes": 54,
        "heartbeat_seq": 355,
        "delta_ms": 1907,
    },
    {
        "evidence_id": "GDL-CAP-002",
        "live_drop_line": 1951,
        "live_heartbeat_line": 1955,
        "console_drop_line": 24912,
        "console_empty_line": 24918,
        "frame_bytes": 54,
        "heartbeat_seq": 630,
        "delta_ms": 719,
    },
    {
        "evidence_id": "GDL-CAP-003",
        "live_drop_line": 2161,
        "live_heartbeat_line": 2167,
        "console_drop_line": 30769,
        "console_empty_line": 30779,
        "frame_bytes": 82,
        "heartbeat_seq": 694,
        "delta_ms": 99,
    },
)


def verify_capture() -> tuple[bytes, bytes, bytes, list[dict[str, int | str]]]:
    live_data = read_pinned(
        CAPTURE_LIVE_PATH,
        EXPECTED_CAPTURE_LIVE_SIZE,
        EXPECTED_CAPTURE_LIVE_SHA256,
    )
    console_data = read_pinned(
        CAPTURE_CONSOLE_PATH,
        EXPECTED_CAPTURE_CONSOLE_SIZE,
        EXPECTED_CAPTURE_CONSOLE_SHA256,
    )
    note_data = read_pinned(
        ATTENDED_NOTE_PATH,
        EXPECTED_ATTENDED_NOTE_SIZE,
        EXPECTED_ATTENDED_NOTE_SHA256,
    )
    live_lines = live_data.decode("utf-8").splitlines()
    console_lines = console_data.decode("utf-8").splitlines()
    if len(live_lines) != EXPECTED_CAPTURE_LIVE_LINES:
        raise ValueError("GAME_LIVE line count mismatch")
    if len(console_lines) != EXPECTED_CAPTURE_CONSOLE_LINES:
        raise ValueError("primary console line count mismatch")

    expected_live_drop_lines = {
        int(spec["live_drop_line"]) for spec in CAPTURE_PAIR_SPECS
    }
    observed_live_drop_lines = {
        index for index, line in enumerate(live_lines, start=1)
        if LIVE_DROP_RE.fullmatch(line)
    }
    if observed_live_drop_lines != expected_live_drop_lines:
        raise ValueError(
            "complete GAME_LIVE MOB_LOOT_DROP census mismatch: "
            f"expected={sorted(expected_live_drop_lines)!r} "
            f"observed={sorted(observed_live_drop_lines)!r}"
        )
    expected_console_drop_lines = {
        int(spec["console_drop_line"]) for spec in CAPTURE_PAIR_SPECS
    }
    observed_console_drop_lines = {
        index for index, line in enumerate(console_lines, start=1)
        if CONSOLE_DROP_RE.fullmatch(line)
    }
    if observed_console_drop_lines != expected_console_drop_lines:
        raise ValueError(
            "complete console MOB_LOOT_DROP census mismatch: "
            f"expected={sorted(expected_console_drop_lines)!r} "
            f"observed={sorted(observed_console_drop_lines)!r}"
        )

    observations: list[dict[str, int | str]] = []
    for spec in CAPTURE_PAIR_SPECS:
        live_drop = live_lines[int(spec["live_drop_line"]) - 1]
        live_heartbeat = live_lines[int(spec["live_heartbeat_line"]) - 1]
        console_drop = console_lines[int(spec["console_drop_line"]) - 1]
        console_empty = console_lines[int(spec["console_empty_line"]) - 1]
        drop_match = LIVE_DROP_RE.fullmatch(live_drop)
        heartbeat_match = LIVE_HEARTBEAT_RE.fullmatch(live_heartbeat)
        console_drop_match = CONSOLE_DROP_RE.fullmatch(console_drop)
        console_empty_match = CONSOLE_EMPTY_RE.fullmatch(console_empty)
        if not all((drop_match, heartbeat_match, console_drop_match, console_empty_match)):
            raise ValueError(f"capture locator mismatch: {spec['evidence_id']}")
        assert drop_match is not None
        assert heartbeat_match is not None
        assert console_drop_match is not None
        assert console_empty_match is not None
        if int(drop_match.group("size")) != spec["frame_bytes"]:
            raise ValueError("live frame-size mismatch")
        if int(console_drop_match.group("size")) != spec["frame_bytes"]:
            raise ValueError("console frame-size mismatch")
        if int(heartbeat_match.group("seq")) != spec["heartbeat_seq"]:
            raise ValueError("live heartbeat sequence mismatch")
        if int(console_empty_match.group("seq")) != spec["heartbeat_seq"]:
            raise ValueError("console heartbeat sequence mismatch")
        first_later_heartbeat = next(
            (
                index
                for index in range(int(spec["live_drop_line"]) + 1, len(live_lines) + 1)
                if LIVE_HEARTBEAT_RE.fullmatch(live_lines[index - 1])
            ),
            None,
        )
        if first_later_heartbeat != spec["live_heartbeat_line"]:
            raise ValueError("first post-drop heartbeat locator mismatch")
        drop_time = datetime.fromisoformat(drop_match.group("time"))
        heartbeat_time = datetime.fromisoformat(heartbeat_match.group("time"))
        delta_ms = round((heartbeat_time - drop_time).total_seconds() * 1000)
        if delta_ms != spec["delta_ms"]:
            raise ValueError("capture elapsed-time mismatch")
        observations.append(dict(spec))
    return live_data, console_data, note_data, observations


FIELDNAMES = [
    "evidence_id",
    "row_kind",
    "topic",
    "subject",
    "direction",
    "semantic_status",
    "exact_observation",
    "value_or_layout",
    "owner_container",
    "storage_key",
    "removal_effect",
    "evidence_file",
    "evidence_locator",
    "evidence_span_start",
    "evidence_span_end",
    "evidence_span_start_file_offset",
    "evidence_span_end_file_offset",
    "evidence_span_sha256",
    "support_spans",
    "evidence_key",
    "semantic_fingerprint",
    "evidence_grade",
    "measurement_label",
    "method",
    "control",
    "source",
    "source_size",
    "source_sha256",
    "reference_artifact",
    "reference_sha256",
    "reference_selector",
    "nonclaim",
    "image_sha256",
]


def make_image_row(
    pe: PE32,
    evidence_id: str,
    topic: str,
    subject: str,
    direction: str,
    semantic_status: str,
    exact_observation: str,
    value_or_layout: str,
    owner_container: str,
    storage_key: str,
    removal_effect: str,
    primary_span: str,
    support: tuple[str, ...],
    nonclaim: str,
) -> dict[str, str]:
    start, end, digest = SPAN_SPECS[primary_span]
    row = {
        "evidence_id": evidence_id,
        "row_kind": "NEW_IMAGE_EVIDENCE",
        "topic": topic,
        "subject": subject,
        "direction": direction,
        "semantic_status": semantic_status,
        "exact_observation": exact_observation,
        "value_or_layout": value_or_layout,
        "owner_container": owner_container,
        "storage_key": storage_key,
        "removal_effect": removal_effect,
        "evidence_file": "PF_ROOT://GameClient/GameClient.local.bin",
        "evidence_locator": primary_span,
        "evidence_span_start": f"0x{start:08X}",
        "evidence_span_end": f"0x{end:08X}",
        "evidence_span_start_file_offset": f"0x{pe.va_to_offset(start):08X}",
        "evidence_span_end_file_offset": f"0x{pe.va_to_offset(end):08X}",
        "evidence_span_sha256": digest,
        "support_spans": ";".join(span_label(name, pe) for name in support),
        "evidence_key": "",
        "semantic_fingerprint": "",
        "evidence_grade": "A",
        "measurement_label": "MEASURED",
        "method": "STATIC_IMAGE_HASHED_SPAN_AND_CONTROL_FLOW",
        "control": "PINNED_IMAGE_SHA256;EXACT_PRIMARY_AND_SUPPORT_SPAN_SHA256",
        "source": "IMAGE",
        "source_size": str(EXPECTED_IMAGE_SIZE),
        "source_sha256": EXPECTED_IMAGE_SHA256,
        "reference_artifact": "",
        "reference_sha256": "",
        "reference_selector": "",
        "nonclaim": nonclaim,
        "image_sha256": EXPECTED_IMAGE_SHA256,
    }
    row["evidence_key"] = evidence_key(row)
    row["semantic_fingerprint"] = semantic_fingerprint(row)
    return row


def evidence_key(row: dict[str, str]) -> str:
    material = "\x1f".join(
        row.get(name, "")
        for name in (
            "evidence_id",
            "row_kind",
            "topic",
            "subject",
            "semantic_status",
            "exact_observation",
            "evidence_span_sha256",
            "source",
            "source_sha256",
            "reference_selector",
        )
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def semantic_fingerprint(row: dict[str, str]) -> str:
    """Fingerprint claim semantics while deliberately excluding evidence_id."""
    material = "\x1f".join(
        row.get(name, "")
        for name in (
            "row_kind",
            "topic",
            "subject",
            "direction",
            "semantic_status",
            "exact_observation",
            "value_or_layout",
            "owner_container",
            "storage_key",
            "removal_effect",
            "source",
            "evidence_grade",
            "measurement_label",
        )
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def make_rows(
    pe: PE32,
    canonical_keys: dict[str, str],
    capture_observations: list[dict[str, int | str]],
    data_tables: dict[int, dict[int, tuple[dict[str, str], int]]],
    asset_structures: dict[str, NifStructure],
) -> list[dict[str, str]]:
    image_specs = (
        (
            "GDL-IMG-001",
            "INBOUND_IDENTITY",
            "GSCN_RunTimeProtocolRes",
            "S2C",
            "PROVEN_EXACT",
            "The registration name computes to runtime ID 0x6E9D; vtable +0x1C is handler 0x005E4060.",
            "runtime_id=0x6E9D;vtable=0x00F2FFC0;handler=0x005E4060",
            "protocol dispatcher",
            "runtime type ID",
            "NONE",
            "gscn_register",
            ("name_id", "gscn_vtable", "gscn_handler"),
            "The runtime type ID is not promoted to a top-level wire opcode.",
        ),
        (
            "GDL-IMG-002",
            "INBOUND_POOL_FIELD",
            "GSCN_RunTimeProtocolRes+0x20",
            "S2C",
            "PROVEN_EXACT",
            "Constructor leaves +0x20 NULL; codec mask bit 0x08 controls allocation of TerrainThingPool; the handler passes +0x20 to the typed bridge.",
            "outer_mask_bit=0x08;field_offset=+0x20;type=TerrainThingPool*",
            "GSCN_RunTimeProtocolRes",
            "field +0x20",
            "NULL is preserved into reconcile when the outer bit is absent",
            "gscn_codec",
            ("gscn_ctor", "gscn_handler", "pool_factory"),
            "A top-level mask of zero does not itself prove delivery or an on-screen effect.",
        ),
        (
            "GDL-IMG-003",
            "TYPED_DISPATCH",
            "TerrainThingPool to DropThingModule_Client",
            "LOCAL",
            "PROVEN_EXACT",
            "Handler call 0x005E40D5 reaches bridge 0x005F53A0; the bridge resolves DropThingModule_Client and its sole direct reconcile call is 0x006AF970.",
            "handler->bridge(+0x20)->DropThingModule_Client::reconcile",
            "DropThingModule_Client",
            "module runtime ID 0x651A",
            "NONE",
            "typed_bridge",
            ("gscn_handler", "reconcile"),
            "This typed path does not select either FightingDrop reflection descriptor.",
        ),
        (
            "GDL-IMG-004",
            "POOL_CODEC",
            "TerrainThingPool/TerrainThing",
            "S2C",
            "PROVEN_EXACT",
            "The pool codec reads a u16 count, then keyed TerrainThing records and inserts them into the decoded pool map.",
            "pool map=+0x10 sentinel=+0x28 count=+0x2C; element key=+0x10/u32 always; mask=+0x28/u8; bit0x02:+0x14/u32;bit0x04:+0x18/u16;bit0x08:+0x1B/u8;bit0x10:+0x1C,+0x20,+0x24/f32 XYZ;bit0x20:+0x1A/u8",
            "TerrainThingPool",
            "TerrainThing+0x10 u32",
            "NONE",
            "terrain_codec",
            ("terrain_factory_codec_prefix", "pool_factory"),
            "Only offsets, widths, masks, and XYZ are named; other field semantics remain unknown.",
        ),
        (
            "GDL-IMG-005",
            "OWNER_STORAGE",
            "DropThingModule_Client live map",
            "LOCAL",
            "PROVEN_EXACT",
            "The module owns its live wrapper map at +0x18; decoded pool keys are the reconciliation identity used for lookup, insert, update, and erase.",
            "module map=+0x18 sentinel=+0x30 count=+0x34; wrapper TerrainThing ref=+0x7C",
            "DropThingModule_Client",
            "TerrainThing+0x10 u32",
            "map erase is keyed by the same runtime key",
            "reconcile",
            ("module_ctor", "wrapper_factory", "dropobj_ctor"),
            "The key is a runtime object identity; it is not proven to be an item-template ID.",
        ),
        (
            "GDL-IMG-006",
            "CREATE_RENDER",
            "new DropThingGameObj",
            "LOCAL",
            "PROVEN_EXACT",
            "A new key allocates a wrapper, initializes it from TerrainThing, registers it with the world, and inserts it into the module map; the wrapper retains render/nameboard resources.",
            "new key: 0x006AF720 -> 0x005F41E0 -> world register 0x00B0E4A0 -> map insert 0x00708E20; refs +0x7C/+0x80/+0x84/+0x88/+0x8C",
            "DropThingModule_Client live map and world",
            "TerrainThing+0x10 u32",
            "NONE",
            "reconcile",
            ("wrapper_factory", "dropobj_init", "dropobj_vtable"),
            "Static construction does not prove that every data lookup yields visible geometry or a label.",
        ),
        (
            "GDL-IMG-007",
            "RECONCILE_NULL",
            "NULL TerrainThingPool",
            "LOCAL",
            "PROVEN_EXACT",
            "A NULL pool enters the full-removal loop: each live wrapper is unregistered from the world and erased from the module map.",
            "input=NULL",
            "DropThingModule_Client live map",
            "all current keys",
            "REMOVE_ALL: world unregister 0x00B0EE40 then map erase 0x005E0D40",
            "reconcile",
            ("gscn_ctor", "gscn_codec", "typed_bridge"),
            "This is a client-side static predicate, not a claim that a particular capture reached it.",
        ),
        (
            "GDL-IMG-008",
            "RECONCILE_EMPTY",
            "non-NULL empty TerrainThingPool",
            "LOCAL",
            "PROVEN_EXACT",
            "When the pool pointer is non-NULL but pool count +0x2C is zero, reconcile returns through the epilogue without mutating the live map.",
            "input!=NULL;count=0",
            "DropThingModule_Client live map",
            "no keys",
            "PRESERVE_ALL",
            "reconcile",
            ("terrain_codec", "typed_bridge"),
            "A non-NULL empty pool is distinct from an absent +0x20 field that leaves a NULL pointer.",
        ),
        (
            "GDL-IMG-009",
            "RECONCILE_OMISSION",
            "nonempty TerrainThingPool authoritative snapshot",
            "LOCAL",
            "PROVEN_EXACT",
            "For a nonempty pool, a current live-map key omitted from the incoming pool is unregistered and erased.",
            "input!=NULL;count>0;existing_key not in incoming keys",
            "DropThingModule_Client live map",
            "TerrainThing+0x10 u32",
            "REMOVE_OMITTED: world unregister 0x00B0EE40 then map erase 0x005E0D40",
            "reconcile",
            ("terrain_codec",),
            "This does not define server-side expiry policy; it defines the client snapshot consequence.",
        ),
        (
            "GDL-IMG-010",
            "RECONCILE_RANGE",
            "range-pruned ground object",
            "LOCAL",
            "PROVEN_EXACT_BOUNDED",
            "Reconcile references integer threshold 2500, squares it, and can remove an object outside that distance unless the audited bypass flag applies.",
            "range=2500;distance_squared_threshold=6250000",
            "DropThingModule_Client live map",
            "TerrainThing+0x10 u32",
            "REMOVE_OUT_OF_RANGE under the proven predicate",
            "reconcile",
            ("dropobj_update",),
            "The bypass flag semantic name and every possible coordinate space remain unproven.",
        ),
        (
            "GDL-IMG-011",
            "RECONCILE_UPDATE",
            "matching live key",
            "LOCAL",
            "PROVEN_EXACT",
            "A matching incoming/live key calls wrapper update 0x005F4C00 instead of constructing a second wrapper.",
            "existing_key==incoming_key",
            "DropThingModule_Client live map",
            "TerrainThing+0x10 u32",
            "UPDATE_IN_PLACE",
            "reconcile",
            ("dropobj_update",),
            "This does not prove which optional incoming fields are dirty in a particular frame.",
        ),
        (
            "GDL-IMG-012",
            "NO_CLOCK_EXPIRY_IN_NAMED_SPANS",
            "typed ground-drop lifetime path",
            "LOCAL",
            "MANUAL_HASH_ANCHORED_BOUNDED_NEGATIVE",
            "Manual static inspection found no clock/time API reference, clock comparison, or elapsed-time delete predicate in the named typed codec, handler, bridge, reconciler, initializer, wrapper-update, and destructor spans. The checker pins every named span hash but does not automate this semantic absence test.",
            "manual_static_observation=NOT_FOUND_IN_NAMED_SPANS;checker_scope=EXACT_SPAN_HASH_ANCHORS_ONLY",
            "DropThingModule_Client live map",
            "TerrainThing+0x10 u32",
            "MANUALLY_NOT_OBSERVED_IN_HASH_PINNED_SPANS",
            "reconcile",
            ("terrain_codec", "gscn_handler", "typed_bridge", "dropobj_init", "dropobj_update", "dropobj_dtor", "module_dtor"),
            "This is a manual static observation anchored by exact hashes, not an automated timer/xref census. Opaque TerrainThing fields remain semantically unknown; it does not prove absence of a serialized TTL/timestamp field, an indirect consumer, an unrelated timer, or original-server lifetime policy.",
        ),
        (
            "GDL-IMG-013",
            "PICKUP_DIRECT_DELETE_NEGATIVE",
            "audited pickup producer subspan",
            "C2S",
            "BOUNDED_NEGATIVE_WITH_CANONICAL_REFERENCE",
            "Within 0x006B0639..0x006B0658, no direct E8 call targets the three pinned unregister/map-erase functions. Key-copy and enqueue producer facts remain canonical GDT-IMG-002 and are not re-proved here.",
            "direct_E8_delete_targets=0;canonical_producer=GDT-IMG-002",
            "DropThingModule_Client live map",
            "TerrainThing+0x10 u32",
            "NO_DIRECT_KNOWN_DELETE_CALL_IN_AUDITED_SUBSPAN",
            "module_click",
            (),
            "This does not exclude indirect calls, tail jumps, helper side effects, or deletion elsewhere in the pickup lifecycle; server acceptance and later omission are also unproven.",
        ),
        (
            "GDL-IMG-014",
            "LABEL_ONLY_TOGGLE",
            "action selector 0x5B label visibility path",
            "LOCAL",
            "PROVEN_EXACT_BOUNDED",
            "The direct state mutation visible in the named action/refresh spans changes bit 0 of the label scene-node word at +0x18. A direct-E8 census of those spans finds no call to the three pinned known unregister/map-erase targets.",
            "action_selector=0x5B;label_node_flag=+0x18 bit0",
            "DropThingGameObj label scene node",
            "all current wrappers",
            "NO_DIRECT_E8_TO_THREE_PINNED_DELETE_TARGETS",
            "label_action",
            ("all_label_refresh", "dropobj_label_toggle", "dropobj_refresh"),
            "Indirect calls and helper side effects in the same path remain unresolved, so this row does not exclude indirect deletion or prove label visibility is the only total effect. No semantic hotkey/action name is inferred from nearby strings; hiding a label alone is not object deletion.",
        ),
        (
            "GDL-IMG-015",
            "CLEAR_AND_DESTRUCTION",
            "module event clear and DropThingGameObj destructor",
            "LOCAL",
            "PROVEN_EXACT",
            "Module event kind 0x0A clears the map on a separate callback path; wrapper destruction releases retained references +0x7C/+0x80/+0x84/+0x88/+0x8C, and module destruction tears down its map.",
            "event_kind=0x0A;wrapper refs=+0x7C,+0x80,+0x84,+0x88,+0x8C",
            "DropThingModule_Client and DropThingGameObj",
            "all map keys or one wrapper",
            "CLEAR_EVENT_OR_DESTRUCTOR_RELEASE",
            "module_click",
            ("dropobj_dtor", "dropobj_delete_dtor", "module_dtor"),
            "Event kind 0x0A is not assigned a gameplay name by this static artifact.",
        ),
        (
            "GDL-IMG-016",
            "RENDER_LOOKUP",
            "DropThingGameObj item-data/nameboard initialization",
            "LOCAL",
            "PROVEN_EXACT_BOUNDED",
            "Initialization uses TerrainThing+0x14 to look up data and reads s_NAME, n_DROPMODEL_TYPE, n_QUALITY, and s_TAG_EXTRA for presentation; lookup failure can return false while the reconcile caller continues.",
            "item/data key=TerrainThing+0x14;presentation keys=s_NAME,n_DROPMODEL_TYPE,n_QUALITY,s_TAG_EXTRA",
            "DropThingGameObj",
            "TerrainThing+0x10 runtime key plus +0x14 data key",
            "FAILED_INIT_CAN_LEAVE_A_REGISTERED_BUT_BLANK_WRAPPER",
            "dropobj_init",
            ("reconcile", "dropobj_ctor"),
            "The server need not send a literal name/model string on this path, but valid +0x14 data resolution is still required for visible presentation.",
        ),
        (
            "GDL-IMG-017",
            "EXACT_MODEL_SELECTOR_AND_GATE",
            "TerrainThing item-data row to DropThingGameObj model resource",
            "LOCAL",
            "PROVEN_EXACT_CONDITIONAL",
            "TerrainThing+0x14 resolves the local item row; n_DROPMODEL_TYPE is accepted directly only in 0..12 and indexes the 13-token table. The client builds .\\Data\\GC\\F\\<token>.nif, calls the resource loader and type filter, and stores the result at wrapper+0x84. A NULL +0x84 returns false before XYZ and nameboard; non-NULL continues through XYZ/activation and only then creates the nameboard.",
            "0=item;1=weapon;2=armor;3=fittings;4=money;5=buff;6=pandora;7=crystal_r;8=crystal_b;9=crystal_g;10=DROP_ENERGY;11=DROP_LIFE;12=holloween01;requested_path=.\\Data\\GC\\F\\<token>.nif;model_ref=wrapper+0x84",
            "DropThingGameObj",
            "TerrainThing+0x14 item/data key; n_DROPMODEL_TYPE direct index",
            "+0x84 NULL => init false before XYZ/nameboard; non-NULL => activate then nameboard",
            "dropmodel_field_gate",
            (
                "dropmodel_token_table",
                "drop_nif_path_load",
                "drop_loader",
                "drop_resource_open",
                "drop_type_filter",
                "drop_xyz_activation",
                "drop_nameboard",
                "drop_fall_fx",
                "drop_tag_fx",
            ),
            "Type 0 is a valid direct selector for item.nif, not an absence marker. A nameboard created by this exact block proves only that +0x84 was non-NULL at that point; it does not prove visible geometry, pixels, clickability, original-server lifetime, or the packaged .nif-to-.ni_ resolution step. Fall/tag FX are separate retained references and their disappearance is not wrapper/model deletion.",
        ),
        (
            "GDL-IMG-018",
            "PACKAGED_RESOURCE_RESOLUTION",
            ".nif request to packaged .ni_ with loose-file fallback",
            "LOCAL",
            "PROVEN_EXACT_STATIC_CONDITIONAL",
            "At installer callsite 0x0040AF9C, the instructions pass callback 0x00B02300 to setter 0x00790F00; on this non-NULL argument path the setter writes file-open dispatch slot 0x01027B8C. This static derivation does not prove that the callsite executes before the resource request or that no later write replaces the slot, so runtime callback installation is unknown. Conditional on that slot holding 0x00B02300 when 0x008AD740 dispatches, mode 0 selects rb and first calls the packaged reader. _splitpath_s writes the extension buffer passed as string1 to _stricmp while literal .nif is string2; equality branches to a length-gated overwrite of only the original private path's final character, producing .ni_. If that packaged branch returns NULL, _fsopen receives the untouched original .nif path.",
            "installer_callsite=0x0040AF9C;setter=0x00790F00;dispatch_slot=0x01027B8C;callback_argument=0x00B02300;runtime_callback_installation=UNKNOWN;mode=0->rb;compare=_stricmp(splitpath_extension,.nif);rewrite=.nif->.ni_;precedence=packaged_first_then_original_loose_nif",
            "global file-open callback and custom file wrapper",
            "caller path plus private mutable path copy",
            "PACKAGED_NULL_FALLS_BACK_TO_ORIGINAL_PATH",
            "resolver_install",
            (
                "path_open_setter",
                "path_open_dispatch",
                "drop_resource_open",
                "custom_open_callback",
                "custom_file_ctor",
                "mode_jump_table",
                "extension_rewrite",
                "packaged_read_decode",
            ),
            "This proves the setter write semantics and the callback's bounded internal route, conditional on the slot containing 0x00B02300 at dispatch. Runtime installer reachability, ordering before this request, later slot overwrite, every game file-open path, cache policy, filesystem presence, a successful open/decode in a particular run, and visible geometry remain unproved.",
        ),
        (
            "GDL-IMG-019",
            "PACKAGED_RESOURCE_DECODE_AND_PARSE",
            ".ni_ $pcz payload through NiStream",
            "LOCAL",
            "PROVEN_EXACT_CONDITIONAL",
            "The packaged reader loads the transformed file whole. Decoder wrapper 0x00B7A5C0 requires a non-NULL input, length at least 8, and little-endian $pcz magic; a zero output length triggers a declared-size probe from header +4. The decode call uses five property bytes at +8 and payload at +0x0D through a nine-argument LzmaDecode-shaped core. The second decoder Boolean is not tested before the allocated buffer is returned; downstream file validity, NiStream parsing, parsed-collection entry presence, and an RTTI walk to NiNode must still succeed before 0x00B1B6C0 returns non-NULL.",
            "header=$pcz;declared_size=+4;properties=+8/5_bytes;payload=+0x0D;decode_core=0x00A268B0;second_decode_status=ignored;parser=0x008B0CC0;required_entry=first_qualifying_parsed_collection_entry_whose_RTTI_walks_to_NiNode",
            "custom packaged-file buffer and NiStream",
            "transformed .ni_ path then qualifying parsed collection entry",
            "ANY_LATER_FILE_PARSE_OR_NINODE_GATE_FAILURE_RETURNS_NULL",
            "pcz_decode_wrapper",
            (
                "packaged_read_decode",
                "lzma_decode_core",
                "drop_resource_open",
                "stream_file_bridge",
                "nistream_vtable",
                "nistream_ctor_prefix",
                "nistream_parser_prefix",
                "drop_loader",
                "drop_type_filter",
            ),
            "The core has the exact LzmaDecode-shaped argument layout, but stripped symbols do not prove a library build/version. This IMAGE row does not establish an asset-specific runtime decode. A non-null qualifying parsed collection entry whose RTTI walks to NiNode does not prove geometry or pixels.",
        ),
        (
            "GDL-IMG-020",
            "NONNULL_MODEL_CEILING",
            "wrapper+0x84 qualifying parsed NiNode entry",
            "LOCAL",
            "MANUAL_BOUNDED_SEMANTIC_REVIEW",
            "The loader dereferences one parsed collection entry and accepts it only when its RTTI walk reaches NiNode. DropThingGameObj vtable +0x28 reaches 0x00B024F0, whose mechanically asserted path rejects NULL then replaces/refcounts its retained node. Manual bounded semantic review of the exact hash-pinned loader, type-filter, and node-store acceptance spans found no explicit descendant or geometry-type predicate before retained success; that absence was not mechanically proved. Separately, the NiNode constructor transiently initializes its +0xAC child container with the u16 fields at container +8 and +0x0A equal to zero before parsing can populate it; this proves no post-parse child count.",
            "stream_collection=+0x15C:one_dereferenced_entry;required_entry=first_qualifying_parsed_collection_entry_whose_RTTI_walks_to_NiNode;dropobj_vfunc+0x28=0x00B024F0;retained_node=base+0x78;descendant_geometry_predicate_review=MANUAL_BOUNDED_OVER_EXACT_HASHED_SPANS;NiNode_ctor_transient_child_container=+0xAC:u16(+8)=0,u16(+0x0A)=0;post_parse_child_count=UNPROVEN",
            "NiStream parsed collection, qualifying NiNode entry, and DropThingGameObj",
            "wrapper+0x84 model ref plus retained scene-node ref",
            "MANUAL_BOUNDED_NO_EXPLICIT_DESCENDANT_OR_GEOMETRY_PREDICATE_FOUND_IN_NAMED_SPANS",
            "ninode_ctor",
            (
                "ninode_rtti_init",
                "drop_loader",
                "drop_type_filter",
                "dropobj_vtable",
                "drop_xyz_activation",
                "wrapper_store",
            ),
            "A non-null qualifying parsed collection entry whose RTTI walks to NiNode does not prove geometry or pixels. Constructor-time zero initialization is transient and does not prove that any successfully parsed asset is zero-child. The predicate absence is a manual bounded review, not an automated census: indirect predicates, helper side effects, or overlooked predicates within or beyond the named spans remain possible. This IMAGE row does not establish asset-specific runtime loading; hidden or culled children, materials, textures, renderer submission, and camera placement remain unresolved.",
        ),
        (
            "GDL-IMG-021",
            "NORMAL_BOOTSTRAP_RESOURCE_CALLBACK_INSTALL",
            "PE/CLI/CRT normal successful application bootstrap",
            "LOCAL",
            "MANUAL_BOUNDED_STATIC_NORMAL_BOOTSTRAP_REACHABILITY",
            "The PE entry stub imports _CorExeMain. Structured CLI metadata parsing resolves entry token 0x060000BA to <Module>._WinMainCRTStartup at 0x00B38225; mechanically asserted native calls reach application initialization 0x0040AE70. Manual bounded CFG review over the exact hash-pinned entry/CRT/application-init spans finds that the fall-through successful continuation installs callback 0x00B02300 through setter 0x00790F00 before the later application-object allocation/construction and non-NULL return continuation. Separately, a mechanical whole-image file-backed-section byte census finds exactly three encoded absolute references to slot 0x01027B8C: dispatch at 0x00790EC2 and the setter's default/callback writes at 0x00790F06/0x00790F13. Callback 0x00B02300 appears as an absolute immediate once, at 0x0040AF9D, and the setter has exactly one whole-image direct-E8 caller, 0x0040AFA1.",
            "pe_entry_rva=0x00783122;cli_entry_token=0x060000BA;managed_entry_va=0x00B38225;app_init=0x0040AE70;installer=0x0040AF9C;setter=0x00790F00;callback=0x00B02300;slot=0x01027B8C;normal_success_order=MANUAL_BOUNDED_HASH_ANCHORED;encoded_slot_refs=3;direct_setter_E8_xrefs=1",
            "normal successful client application bootstrap and global resource-open dispatch",
            "global slot 0x01027B8C",
            "NONE",
            "app_init_install",
            (
                "pe_entry_stub",
                "cli_header",
                "managed_entry",
                "crt_to_winmain",
                "winmain_to_app_init",
                "app_init_object_return",
                "path_open_setter",
                "path_open_dispatch",
                "custom_open_callback",
            ),
            "The normal-success dominance/ordering statement is a manual bounded review anchored by exact spans, not a mechanically complete instruction-decoder CFG proof, and it does not claim that a particular process executed. Abnormal/external entry, computed or aliased writes, self-modification, injected code, and runtime memory corruption remain outside the whole-image encoded-reference census. It does not prove that a particular asset request succeeded.",
        ),
        (
            "GDL-IMG-022",
            "WORLD_SCENE_GRAPH_REGISTRATION",
            "DropThingGameObj retained model root and recursive scene traversal",
            "LOCAL",
            "PROVEN_EXACT_STATIC_SCENE_PIPELINE",
            "After the model gate, wrapper+0x84 is passed through DropThingGameObj vslot +0x28 to 0x00B024F0, which retains it at base+0x78. World registration 0x00B0E4A0 invokes vslot +0x10 and rejects a NULL root; for DropThingGameObj that getter is 0x008F7730 and returns base+0x78. Registration then invokes DropThingGameObj vslot +0x1C at 0x005F4110. That bind path validates the root, calls 0x00B1DA60, and activates state through 0x00B1C900/0x00B1CD30. The pinned traversal at 0x00B1D8D0 type-filters to NiNode, reads child count +0xB6 and child array +0xB0, and recursively visits each child.",
            "model_candidate=wrapper+0x84;retained_scene_root=base+0x78;getter_vslot=+0x10;world_bind_vslot=+0x1C;node_store_vslot=+0x28;NiNode_child_count=+0xB6/u16;NiNode_child_array=+0xB0;recursive_call=0x00B1D9DA",
            "DropThingGameObj and world scene graph",
            "TerrainThing runtime key through registered wrapper",
            "Reverse lifetime boundary remains the separately proven world-unregister-before-map-erase and destructor reference release paths.",
            "world_register",
            (
                "drop_xyz_activation",
                "dropobj_vtable",
                "wrapper_store",
                "scene_node_getter",
                "dropobj_world_bind",
                "scene_graph_bind",
                "scene_graph_traverse",
                "scene_activate",
                "reconcile",
                "dropobj_dtor",
            ),
            "This is a static object/world/scene-graph path. It does not prove that a particular runtime parse reached it, that a retained NiNode has geometry, that a serialized NiMesh was instantiated or submitted to a renderer, or that materials, textures, culling, camera, device, framebuffer, and visible pixels succeeded.",
        ),
    )
    rows = [make_image_row(pe, *spec) for spec in image_specs]
    image_method_controls = {
        "GDL-IMG-012": (
            "STATIC_IMAGE_HASHED_SPANS_WITH_MANUAL_BOUNDED_SEMANTIC_REVIEW",
            "PINNED_IMAGE_SHA256;EXACT_SPAN_SHA256;MANUAL_TIMER_XREF_CENSUS",
        ),
        "GDL-IMG-013": (
            "STATIC_IMAGE_CFG_AND_DIRECT_CALL_TARGET_CENSUS",
            "PINNED_IMAGE_SHA256;EXACT_SPAN_SHA256;DIRECT_E8_TARGET_ASSERTIONS",
        ),
        "GDL-IMG-018": (
            "STATIC_IMAGE_CFG_STACK_CALL_AND_IAT_ASSERTIONS",
            "PINNED_IMAGE_SHA256;EXACT_SPAN_SHA256;ASSERTED_INSTALLER_CALLSITE_AND_SETTER_WRITE;RUNTIME_REACHABILITY_ORDER_OVERWRITE_UNKNOWN;ASSERTED_STACK_ARGS;ASSERTED_CFG_EDGES;ASSERTED_CALL_TARGETS;ASSERTED_IAT_NAMES;ASSERTED_SPLITPATH_EXTENSION_BUFFER_TO_STRICMP_NIF_ARGUMENT_AND_REWRITE_EDGE",
        ),
        "GDL-IMG-019": (
            "STATIC_IMAGE_CFG_DECODE_VTABLE_AND_RETURN_USE_ASSERTIONS",
            "PINNED_IMAGE_SHA256;EXACT_SPAN_SHA256;ASSERTED_DECODE_ARGS;ASSERTED_RETURN_USE;ASSERTED_VTABLE_TARGETS;ASSERTED_RTTI_ENTRY",
        ),
        "GDL-IMG-020": (
            "STATIC_IMAGE_POSITIVE_ASSERTIONS_PLUS_MANUAL_BOUNDED_SEMANTIC_REVIEW",
            "PINNED_IMAGE_SHA256;EXACT_SPAN_SHA256;ASSERTED_COLLECTION_ENTRY;ASSERTED_RTTI_TARGET;ASSERTED_RETAIN_PATH;TRANSIENT_CTOR_ZERO_ONLY;MANUAL_BOUNDED_DESCENDANT_GEOMETRY_PREDICATE_REVIEW;NO_AUTOMATED_ABSENCE_CENSUS;INDIRECT_OR_OVERLOOKED_PREDICATES_REMAIN_POSSIBLE",
        ),
        "GDL-IMG-021": (
            "STATIC_PE_CLI_ASSERTIONS_WHOLE_IMAGE_CENSUS_AND_MANUAL_BOUNDED_CFG_REVIEW",
            "PINNED_IMAGE_SHA256;PARSED_PE_ENTRY_AND_CLI_METHODDEF;EXACT_ENTRY_CRT_APPINIT_CALLS_AND_BRANCHES;MANUAL_BOUNDED_HASH_ANCHORED_NORMAL_SUCCESS_ORDER_REVIEW;WHOLE_IMAGE_FILE_BACKED_U32_SLOT_AND_CALLBACK_CENSUS;WHOLE_IMAGE_E8_SETTER_XREF_CENSUS;RUNTIME_EXECUTION_NOT_CLAIMED;COMPUTED_ALIAS_DYNAMIC_WRITES_NOT_EXCLUDED",
        ),
        "GDL-IMG-022": (
            "STATIC_IMAGE_VTABLE_CFG_AND_RECURSIVE_CHILD_TRAVERSAL_ASSERTIONS",
            "PINNED_IMAGE_SHA256;EXACT_SPAN_SHA256;ASSERTED_MODEL_STORE_ROOT_GETTER_WORLD_REGISTER_AND_BIND_VSLOTS;ASSERTED_NINODE_CHILD_COUNT_ARRAY_AND_RECURSIVE_CALL;NO_RENDERER_OR_PIXEL_CLAIM",
        ),
    }
    for row in rows:
        override = image_method_controls.get(row["evidence_id"])
        if override is not None:
            row["method"], row["control"] = override
        if row["evidence_id"] in {"GDL-IMG-020", "GDL-IMG-021"}:
            row["measurement_label"] = "MANUAL_BOUNDED"
        row["semantic_fingerprint"] = semantic_fingerprint(row)
    pickup_extension = next(
        row for row in rows if row["evidence_id"] == "GDL-IMG-013"
    )
    pickup_extension["row_kind"] = "BOUNDED_IMAGE_EXTENSION"
    pickup_extension["reference_artifact"] = "PF_GROUND_DROP_TRANSPORT.tsv"
    pickup_extension["reference_sha256"] = EXPECTED_TRANSPORT_TSV_SHA256
    pickup_extension["reference_selector"] = "GDT-IMG-002"
    pickup_extension["evidence_key"] = evidence_key(pickup_extension)
    pickup_extension["semantic_fingerprint"] = semantic_fingerprint(pickup_extension)

    reference_row = {
        "evidence_id": "GDL-CREF-001",
        "row_kind": "CANONICAL_REFERENCE",
        "topic": "FALSE_LEAD",
        "subject": "FightingDropModule_Client/FightingDropNotify",
        "direction": "N/A",
        "semantic_status": "CUSTOM_REFLECTION_ONLY_FALSE_LEAD_FOR_THIS_TYPED_PATH",
        "exact_observation": (
            "Canonical rows GDT-IMG-008 and GDT-IMG-009 establish custom-reflection "
            "metadata only; the exact inbound path in this artifact selects "
            "GSCN_RunTimeProtocolRes+0x20 TerrainThingPool instead."
        ),
        "value_or_layout": "reference-only;no copied transport rows",
        "owner_container": "N/A",
        "storage_key": "N/A",
        "removal_effect": "NONE",
        "evidence_file": "N/A_CANONICAL_REFERENCE",
        "evidence_locator": "GDT-IMG-008;GDT-IMG-009",
        "evidence_span_start": "",
        "evidence_span_end": "",
        "evidence_span_start_file_offset": "",
        "evidence_span_end_file_offset": "",
        "evidence_span_sha256": "",
        "support_spans": span_label("typed_bridge", pe),
        "evidence_key": "",
        "semantic_fingerprint": "",
        "evidence_grade": "A",
        "measurement_label": "REFERENCE",
        "method": "CANONICAL_ARTIFACT_REFERENCE_PLUS_STATIC_TYPED_PATH",
        "control": "PINNED_TRANSPORT_TSV_SHA256;PINNED_IMAGE_SHA256;TYPED_BRIDGE_SPAN_SHA256",
        "source": "IMAGE",
        "source_size": str(EXPECTED_IMAGE_SIZE),
        "source_sha256": EXPECTED_IMAGE_SHA256,
        "reference_artifact": "PF_GROUND_DROP_TRANSPORT.tsv",
        "reference_sha256": EXPECTED_TRANSPORT_TSV_SHA256,
        "reference_selector": "GDT-IMG-008;GDT-IMG-009",
        "nonclaim": (
            "This rejects FightingDrop as the concrete surface for the proven typed path; "
            "it does not prove the classes are globally unused."
        ),
        "image_sha256": EXPECTED_IMAGE_SHA256,
    }
    reference_row["evidence_key"] = evidence_key(reference_row)
    reference_row["semantic_fingerprint"] = semantic_fingerprint(reference_row)
    rows.append(reference_row)

    table_partition = Counter()
    selector_histogram = Counter()
    data_locators: list[str] = []
    for full_id, (table_code, low_id, expected_type) in sorted(
        EXPECTED_CURRENT_ROSTER.items()
    ):
        data_row, line_number = data_tables[table_code][low_id]
        actual_type = int(data_row["n_DROPMODEL_TYPE"])
        if actual_type != expected_type:
            raise ValueError(f"DATA changed after verification: {full_id}")
        table_partition[table_code] += 1
        selector_histogram[actual_type] += 1
        data_locators.append(
            f"table={table_code}:n_ID={low_id}:line={line_number}:audit_full_id={full_id}"
        )
    if table_partition != Counter({22: 30, 24: 10, 26: 3}):
        raise ValueError(f"external-audit DATA partition drift: {table_partition!r}")
    if selector_histogram != Counter({0: 11, 1: 12, 2: 10, 3: 8, 10: 1, 11: 1}):
        raise ValueError(f"external-audit selector histogram drift: {selector_histogram!r}")

    data_manifest_material = "\n".join(
        f"{table_code}:{path.name}:{size}:{digest}"
        for table_code, (path, size, digest) in sorted(DATA_TABLE_PINS.items())
    ).encode("ascii")
    data_manifest_digest = sha256(data_manifest_material)
    data_census_row = {
        "evidence_id": "GDL-DATA-001",
        "row_kind": "DATA_EXTERNAL_AUDIT_SET",
        "topic": "DROP_MODEL_SELECTOR_VALUES",
        "subject": "externally specified 43-ID DATA audit set",
        "direction": "LOCAL_DATA",
        "semantic_status": "PROVEN_EXACT_DATA_CENSUS",
        "exact_observation": (
            "All rows named by the externally specified 43-ID audit set exist in the "
            "three pinned DATA tables. Within that set, the table partition is "
            "22:30,24:10,26:3 and the raw n_DROPMODEL_TYPE value histogram is "
            "0:11,1:12,2:10,3:8,10:1,11:1."
        ),
        "value_or_layout": (
            "rows=43;unique_audit_ids=43;table_partition=22:30,24:10,26:3;"
            "selector_histogram=0:11,1:12,2:10,3:8,10:1,11:1"
        ),
        "owner_container": "CONSTDATA item tables",
        "storage_key": "n_ID within each table",
        "removal_effect": "NONE",
        "evidence_file": ";".join(
            f"PF_ROOT://pf_bridge/gamedata/tables/{path.name}"
            for _code, (path, _size, _digest) in sorted(DATA_TABLE_PINS.items())
        ),
        "evidence_locator": ";".join(data_locators),
        "evidence_span_start": "",
        "evidence_span_end": "",
        "evidence_span_start_file_offset": "",
        "evidence_span_end_file_offset": "",
        "evidence_span_sha256": "",
        "support_spans": "",
        "evidence_key": "",
        "semantic_fingerprint": "",
        "evidence_grade": "A",
        "measurement_label": "MEASURED",
        "method": "PINNED_DATA_ROW_LOOKUP_AND_VALUE_CENSUS",
        "control": "THREE_PINNED_TABLE_SIZE_SHA256;EXTERNALLY_SPECIFIED_43_ID_SET;EXACT_ROW_LOCATORS",
        "source": "DATA",
        "source_size": str(sum(size for _path, size, _digest in DATA_TABLE_PINS.values())),
        "source_sha256": data_manifest_digest,
        "reference_artifact": "",
        "reference_sha256": "",
        "reference_selector": "",
        "nonclaim": (
            "This row reports only DATA values for an externally supplied audit set. It "
            "does not claim why those IDs were selected, that they exhaust any table, or "
            "that an original or reconstructed server issued them."
        ),
        "image_sha256": "",
    }
    data_census_row["evidence_key"] = evidence_key(data_census_row)
    data_census_row["semantic_fingerprint"] = semantic_fingerprint(data_census_row)
    rows.append(data_census_row)

    asset_manifest_material = "\n".join(
        f"{name}:{size}:{digest}"
        for name, (size, digest) in PACKAGE_ASSET_PINS.items()
    ).encode("ascii")
    asset_manifest_digest = sha256(asset_manifest_material)
    asset_row = {
        "evidence_id": "GDL-DATA-002",
        "row_kind": "DATA_PACKAGE_FILE_AUDIT",
        "topic": "PACKAGED_DROP_MODEL_FILES",
        "subject": "externally specified 13-file .ni_ audit set",
        "direction": "LOCAL_DATA",
        "semantic_status": "PROVEN_EXACT_DATA_INVENTORY",
        "exact_observation": (
            "Every path in the externally specified 13-file audit set exists under "
            "GameClient/Data/GC/F with its pinned byte size and SHA-256: item.ni_, "
            "weapon.ni_, armor.ni_, fittings.ni_, money.ni_, buff.ni_, pandora.ni_, "
            "crystal_r.ni_, crystal_b.ni_, crystal_g.ni_, drop_energy.ni_, "
            "drop_life.ni_, and holloween01.ni_."
        ),
        "value_or_layout": "audited_asset_count=13;extension=.ni_;size_and_sha256_pinned=true",
        "owner_container": "GameClient/Data/GC/F",
        "storage_key": "filename stem",
        "removal_effect": "NONE",
        "evidence_file": "PF_ROOT://GameClient/Data/GC/F/",
        "evidence_locator": ";".join(PACKAGE_ASSET_PINS),
        "evidence_span_start": "",
        "evidence_span_end": "",
        "evidence_span_start_file_offset": "",
        "evidence_span_end_file_offset": "",
        "evidence_span_sha256": "",
        "support_spans": "",
        "evidence_key": "",
        "semantic_fingerprint": "",
        "evidence_grade": "A",
        "measurement_label": "MEASURED",
        "method": "PINNED_FILE_EXISTENCE_SIZE_AND_SHA256_AUDIT",
        "control": "EXTERNALLY_SPECIFIED_13_PATH_SET;EXACT_FILE_SIZE_SHA256",
        "source": "DATA",
        "source_size": str(sum(size for size, _digest in PACKAGE_ASSET_PINS.values())),
        "source_sha256": asset_manifest_digest,
        "reference_artifact": "",
        "reference_sha256": "",
        "reference_selector": "",
        "nonclaim": (
            "This is not a complete directory census and does not decode, parse, classify, "
            "or render any audited file."
        ),
        "image_sha256": "",
    }
    asset_row["evidence_key"] = evidence_key(asset_row)
    asset_row["semantic_fingerprint"] = semantic_fingerprint(asset_row)
    rows.append(asset_row)

    decoded_total = sum(
        structure.decoded_size for structure in asset_structures.values()
    )
    block_total = sum(
        structure.block_count for structure in asset_structures.values()
    )
    ninode_total = sum(
        structure.reachable_ninode for structure in asset_structures.values()
    )
    billboard_total = sum(
        structure.reachable_billboard for structure in asset_structures.values()
    )
    nimesh_total = sum(
        structure.reachable_nimesh for structure in asset_structures.values()
    )
    particle_total = sum(
        structure.reachable_particle for structure in asset_structures.values()
    )
    material_ref_total = sum(
        structure.reachable_nimesh_material_refs
        for structure in asset_structures.values()
    )
    texturing_ref_total = sum(
        structure.reachable_nimesh_texturing_refs
        for structure in asset_structures.values()
    )
    base_source_ref_total = sum(
        structure.reachable_nimesh_base_source_refs
        for structure in asset_structures.values()
    )
    external_dds_ref_total = sum(
        structure.reachable_nimesh_external_dds_refs
        for structure in asset_structures.values()
    )
    nimesh_counts = tuple(
        structure.reachable_nimesh for structure in asset_structures.values()
    )
    if (
        len(asset_structures),
        decoded_total,
        block_total,
        ninode_total,
        billboard_total,
        nimesh_total,
        particle_total,
        material_ref_total,
        texturing_ref_total,
        base_source_ref_total,
        external_dds_ref_total,
        min(nimesh_counts),
        max(nimesh_counts),
    ) != (13, 83_400, 441, 25, 4, 34, 2, 34, 34, 34, 34, 1, 7):
        raise ValueError("decoded NIF aggregate census drift")
    structure_locators = []
    for name, structure in asset_structures.items():
        compressed_size, compressed_digest = PACKAGE_ASSET_PINS[name]
        structure_locators.append(
            f"{name}:compressed_size={compressed_size}:"
            f"compressed_sha256={compressed_digest}:"
            f"decoded_size={structure.decoded_size}:"
            f"decoded_sha256={structure.decoded_sha256}:"
            f"blocks={structure.block_count}:root_count={structure.root_count}:"
            f"root_index={structure.root_index}:"
            f"reachable_NiNode={structure.reachable_ninode}:"
            f"reachable_NiBillboardNode={structure.reachable_billboard}:"
            f"reachable_NiMesh={structure.reachable_nimesh}:"
            f"reachable_NiPSMeshParticleSystem={structure.reachable_particle}:"
            f"NiMesh_material_refs={structure.reachable_nimesh_material_refs}:"
            f"NiMesh_texturing_refs={structure.reachable_nimesh_texturing_refs}:"
            f"base_NiSourceTexture_refs="
            f"{structure.reachable_nimesh_base_source_refs}:"
            f"external_DDS_string_refs="
            f"{structure.reachable_nimesh_external_dds_refs}"
        )
    structure_row = {
        "evidence_id": "GDL-DATA-003",
        "row_kind": "DATA_PACKAGE_STRUCTURE_AUDIT",
        "topic": "PACKAGED_DROP_MODEL_SERIALIZED_GRAPH",
        "subject": "externally specified 13-file .ni_ audit set",
        "direction": "LOCAL_DATA",
        "semantic_status": "PROVEN_EXACT_DECODED_DATA_STRUCTURE_CENSUS",
        "exact_observation": (
            "All 13 pinned $pcz files decode with their five-byte raw-LZMA1 "
            "properties to the pinned decoded size and SHA-256, then parse as "
            "Gamebryo 30.1.0.2 block streams with exact whole-file consumption. "
            "Each footer has root_count=1 and root_index=0, whose block type is "
            "NiNode. Following serialized NiNode/NiBillboardNode child references "
            "from that root reaches at least one exact NiMesh block in 13/13 files. "
            "Across the audited set the reachable census is NiNode=25, "
            "NiBillboardNode=4, NiMesh=34, NiPSMeshParticleSystem=2. Every one "
            "of the 34 root-reachable NiMesh blocks directly references exactly "
            "one NiMaterialProperty and one NiTexturingProperty. Each referenced "
            "texturing property's base descriptor links to an external "
            "NiSourceTexture whose string-table entry ends in .dds (34/34)."
        ),
        "value_or_layout": (
            "audited_assets=13;compressed_bytes=31158;decoded_bytes=83400;"
            "blocks=441;roots=13;root_index_zero=13;root_type_NiNode=13;"
            "assets_with_reachable_NiMesh=13;reachable_NiMesh_min=1;"
            "reachable_NiMesh_max=7;reachable_NiNode=25;"
            "reachable_NiBillboardNode=4;reachable_NiMesh=34;"
            "reachable_NiPSMeshParticleSystem=2;NiMesh_material_refs=34;"
            "NiMesh_texturing_refs=34;base_NiSourceTexture_refs=34;"
            "external_DDS_string_refs=34"
        ),
        "owner_container": "GameClient/Data/GC/F serialized asset files",
        "storage_key": (
            "footer root, child, NiMesh property, base-source, and string-table refs"
        ),
        "removal_effect": "NONE",
        "evidence_file": "PF_ROOT://GameClient/Data/GC/F/",
        "evidence_locator": ";".join(structure_locators),
        "evidence_span_start": "",
        "evidence_span_end": "",
        "evidence_span_start_file_offset": "",
        "evidence_span_end_file_offset": "",
        "evidence_span_sha256": "",
        "support_spans": "",
        "evidence_key": "",
        "semantic_fingerprint": "",
        "evidence_grade": "A",
        "measurement_label": "MEASURED",
        "method": (
            "PINNED_PCZ_RAW_LZMA_DECODE_NIF_GRAPH_PROPERTY_AND_TEXTURE_REF_PARSE"
        ),
        "control": (
            "THIRTEEN_PINNED_COMPRESSED_SIZE_SHA256;DECLARED_DECODED_SIZE;"
            "FIVE_BYTE_LZMA1_PROPERTY_PARSE;PINNED_DECODED_SIZE_SHA256;"
            "EXACT_NIF_HEADER_VERSION_ENDIAN;BLOCK_TYPE_INDEX_AND_SIZE_BOUNDS;"
            "EXACT_WHOLE_FILE_CONSUMPTION;FOOTER_ROOT_AND_RECURSIVE_CHILD_CENSUS;"
            "NIMESH_PROPERTY_REF_TYPE_AND_EXACTLY_ONE_EACH_ASSERTIONS;"
            "BASE_TEXTURE_DESCRIPTOR_TO_NISOURCETEXTURE_ASSERTIONS;"
            "EXTERNAL_FLAG_STRING_INDEX_AND_DDS_SUFFIX_ASSERTIONS;"
            "PER_FILE_EXPECTED_STRUCTURE_PIN"
        ),
        "source": "DATA",
        "source_size": str(
            sum(size for size, _digest in PACKAGE_ASSET_PINS.values())
        ),
        "source_sha256": asset_manifest_digest,
        "reference_artifact": "",
        "reference_sha256": "",
        "reference_selector": "",
        "nonclaim": (
            "Serialized root-reachable NiMesh blocks do not prove that a client "
            "opened, decoded, parsed, instantiated, attached, culled, submitted, "
            "or drew the file in any run. Serialized property/source references "
            "do not prove that the referenced DDS files exist, open, decode, bind, "
            "or sample successfully; nor do they prove material completeness, "
            "camera visibility, framebuffer output, or pixels."
        ),
        "image_sha256": "",
    }
    structure_row["evidence_key"] = evidence_key(structure_row)
    structure_row["semantic_fingerprint"] = semantic_fingerprint(structure_row)
    rows.append(structure_row)

    for observation in capture_observations:
        evidence_id = str(observation["evidence_id"])
        delta_ms = int(observation["delta_ms"])
        frame_bytes = int(observation["frame_bytes"])
        live_drop_line = int(observation["live_drop_line"])
        live_heartbeat_line = int(observation["live_heartbeat_line"])
        console_drop_line = int(observation["console_drop_line"])
        console_empty_line = int(observation["console_empty_line"])
        heartbeat_seq = int(observation["heartbeat_seq"])
        row = {
            "evidence_id": evidence_id,
            "row_kind": "CAPTURE_OBSERVATION",
            "topic": "DROP_THEN_EMPTY_RUNTIME_RESPONSE",
            "subject": f"MOB_LOOT_DROP then heartbeat #{heartbeat_seq}",
            "direction": "S2C",
            "semantic_status": "OBSERVED_EXACT_CAPTURE_ORDER_AND_TIMING",
            "exact_observation": (
                f"GAME_LIVE records a server-labelled {frame_bytes}-byte MOB_LOOT_DROP "
                f"at line {live_drop_line}, then heartbeat #{heartbeat_seq} at line "
                f"{live_heartbeat_line}, {delta_ms} ms later; the pinned primary console "
                f"labels that heartbeat as exact empty RuntimeRes v4 at line "
                f"{console_empty_line}."
            ),
            "value_or_layout": f"frame_bytes={frame_bytes};elapsed_ms={delta_ms}",
            "owner_container": "N/A_CAPTURE_ONLY",
            "storage_key": "N/A_CAPTURE_ONLY",
            "removal_effect": "NOT_ESTABLISHED_BY_CAPTURE",
            "evidence_file": (
                "PF_ROOT://GameClient/capture_pexile_20260830_151429/"
                "capture_v141/GAME_LIVE.txt"
            ),
            "evidence_locator": (
                f"GAME_LIVE:L{live_drop_line}->L{live_heartbeat_line};"
                f"server_console_live.out.txt:L{console_drop_line}->L{console_empty_line}"
            ),
            "evidence_span_start": "",
            "evidence_span_end": "",
            "evidence_span_start_file_offset": "",
            "evidence_span_end_file_offset": "",
            "evidence_span_sha256": "",
            "support_spans": (
                "server_console_live.out.txt"
                f"@size={EXPECTED_CAPTURE_CONSOLE_SIZE}"
                f"@lines={EXPECTED_CAPTURE_CONSOLE_LINES}"
                f"@sha256={EXPECTED_CAPTURE_CONSOLE_SHA256};"
                "attended_note"
                f"@size={EXPECTED_ATTENDED_NOTE_SIZE}"
                f"@sha256={EXPECTED_ATTENDED_NOTE_SHA256}"
            ),
            "evidence_key": "",
            "semantic_fingerprint": "",
            "evidence_grade": "B",
            "measurement_label": "MEASURED",
            "method": "PINNED_CAPTURE_LOG_ORDER_SIZE_AND_TIMESTAMP_CENSUS",
            "control": "PINNED_GAME_LIVE_SHA256;PINNED_CONSOLE_SHA256;PINNED_ATTENDED_NOTE_SHA256;FIRST_LATER_HEARTBEAT_ASSERTION",
            "source": "CAPTURE",
            "source_size": str(EXPECTED_CAPTURE_LIVE_SIZE),
            "source_sha256": EXPECTED_CAPTURE_LIVE_SHA256,
            "reference_artifact": "",
            "reference_sha256": "",
            "reference_selector": "",
            "nonclaim": (
                "This CAPTURE row does not claim client-memory clear, object deletion, "
                "label disappearance, delivery success, or original-server behavior."
            ),
            "image_sha256": "",
        }
        row["evidence_key"] = evidence_key(row)
        row["semantic_fingerprint"] = semantic_fingerprint(row)
        rows.append(row)

    if canonical_keys != {
        "GDT-IMG-002": "0f2e29c0178ce320607ef0c70012c4b960536fbcf81936a46510018c879b7036",
        "GDT-IMG-008": "c777325f1fecf9b41460aabdfb497970e36cac7f37626c08fefbea5120bf1a7b",
        "GDT-IMG-009": "03de64e671eca49d5f0be4e3eb35b46c576ac30ee5c3d34d846316cb71d09e30",
    }:
        raise ValueError("canonical ground-drop evidence-key drift")
    if len(rows) != 29:
        raise ValueError("row census mismatch")
    if len({row["evidence_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate evidence_id")
    if len({row["evidence_key"] for row in rows}) != len(rows):
        raise ValueError("duplicate evidence_key")
    fingerprints = {row["semantic_fingerprint"] for row in rows}
    if "" in fingerprints:
        raise ValueError("blank semantic_fingerprint")
    if len(fingerprints) != len(rows):
        raise ValueError("semantic duplicate row")
    for row in rows:
        renamed = dict(row)
        renamed["evidence_id"] = f"RENAMED-{row['evidence_id']}"
        if semantic_fingerprint(renamed) != row["semantic_fingerprint"]:
            raise ValueError("semantic_fingerprint must exclude evidence_id")
    if {row["evidence_grade"] for row in rows} != {"A", "B"}:
        raise ValueError("unexpected evidence-grade census")
    if {row["measurement_label"] for row in rows} != {
        "MANUAL_BOUNDED",
        "MEASURED",
        "REFERENCE",
    }:
        raise ValueError("unexpected measurement-label census")
    expected_resolver_methods = {
        "GDL-IMG-018": (
            "MEASURED",
            "STATIC_IMAGE_CFG_STACK_CALL_AND_IAT_ASSERTIONS",
        ),
        "GDL-IMG-019": (
            "MEASURED",
            "STATIC_IMAGE_CFG_DECODE_VTABLE_AND_RETURN_USE_ASSERTIONS",
        ),
        "GDL-IMG-020": (
            "MANUAL_BOUNDED",
            "STATIC_IMAGE_POSITIVE_ASSERTIONS_PLUS_MANUAL_BOUNDED_SEMANTIC_REVIEW",
        ),
        "GDL-IMG-021": (
            "MANUAL_BOUNDED",
            "STATIC_PE_CLI_ASSERTIONS_WHOLE_IMAGE_CENSUS_AND_MANUAL_BOUNDED_CFG_REVIEW",
        ),
        "GDL-IMG-022": (
            "MEASURED",
            "STATIC_IMAGE_VTABLE_CFG_AND_RECURSIVE_CHILD_TRAVERSAL_ASSERTIONS",
        ),
    }
    for evidence_id, (expected_label, expected_method) in expected_resolver_methods.items():
        row = next(row for row in rows if row["evidence_id"] == evidence_id)
        if (
            row["evidence_grade"] != "A"
            or row["measurement_label"] != expected_label
            or row["method"] != expected_method
            or not row["control"]
        ):
            raise ValueError(f"resolver evidence-label drift: {evidence_id}")
    resolver_installation = next(
        row for row in rows if row["evidence_id"] == "GDL-IMG-018"
    )
    resolver_claim = "\n".join(
        resolver_installation[name]
        for name in ("semantic_status", "exact_observation", "value_or_layout", "nonclaim")
    )
    if any(
        forbidden in resolver_claim.lower()
        for forbidden in ("startup installs", "callback installed", "installed callback")
    ):
        raise ValueError("resolver row overclaims runtime callback installation")
    if "runtime_callback_installation=UNKNOWN" not in resolver_claim:
        raise ValueError("resolver row must retain unknown runtime installation")
    manual_ceiling = next(row for row in rows if row["evidence_id"] == "GDL-IMG-020")
    manual_ceiling_claim = "\n".join(
        manual_ceiling[name]
        for name in ("semantic_status", "exact_observation", "method", "control", "nonclaim")
    )
    for required in (
        "MANUAL_BOUNDED",
        "indirect predicates",
        "overlooked predicates",
    ):
        if required not in manual_ceiling_claim:
            raise ValueError(f"manual bounded NiNode ceiling missing {required!r}")
    for row in (row for row in rows if row["source"] == "DATA"):
        claim_text = "\n".join(
            row[name]
            for name in (
                "row_kind",
                "subject",
                "exact_observation",
                "value_or_layout",
                "nonclaim",
            )
        )
        forbidden_data_mixes = (
            "IMAGE",
            "CURRENT CODE",
            "current-replacement",
            "all_selector_stems_present",
        )
        if any(token in claim_text for token in forbidden_data_mixes):
            raise ValueError(f"DATA row mixes another source layer: {row['evidence_id']}")
        if row["image_sha256"] or row["reference_artifact"] or row["reference_selector"]:
            raise ValueError(f"DATA row carries cross-layer references: {row['evidence_id']}")
    if sum(row["source"] == "IMAGE" for row in rows) != 23:
        raise ValueError("IMAGE row census mismatch")
    if sum(row["source"] == "DATA" for row in rows) != 3:
        raise ValueError("DATA row census mismatch")
    if sum(row["source"] == "CAPTURE" for row in rows) != 3:
        raise ValueError("CAPTURE row census mismatch")
    if {row["source"] for row in rows} != {"IMAGE", "DATA", "CAPTURE"}:
        raise ValueError("unexpected source layer")
    return rows


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
    image_rows = sum(row["source"] == "IMAGE" for row in rows)
    data_rows = sum(row["source"] == "DATA" for row in rows)
    capture_rows = sum(row["source"] == "CAPTURE" for row in rows)
    deltas = [
        row["value_or_layout"].split("elapsed_ms=", 1)[1]
        for row in rows
        if row["source"] == "CAPTURE"
    ]
    ids_by_type: dict[int, list[int]] = {}
    for full_id, (_table_code, _low_id, drop_type) in sorted(
        EXPECTED_CURRENT_ROSTER.items()
    ):
        ids_by_type.setdefault(drop_type, []).append(full_id)
    roster_lines = []
    for drop_type, item_ids in sorted(ids_by_type.items()):
        token = TOKEN_BY_TYPE[drop_type]
        roster_lines.append(
            f"| {drop_type} | `{token}` | `{token}.nif` | {len(item_ids)} | "
            f"{', '.join(str(item_id) for item_id in item_ids)} |"
        )
    roster_table = "\n".join(roster_lines)
    package_structure_observation = next(
        row["exact_observation"]
        for row in rows
        if row["evidence_id"] == "GDL-DATA-003"
    )
    text = f"""# PF ground-drop lifetime and reconciliation

This is a deterministic, source-separated extension of `PF_GROUND_DROP_TRANSPORT.tsv`. `GDL-IMG-013` references canonical `GDT-IMG-002` and adds only a bounded direct-call negative; it does not duplicate the pickup producer claim. The separate canonical-reference row pins the two FightingDrop reflection findings.

- Image: `GameClient.local.bin`, {EXPECTED_IMAGE_SIZE} bytes, SHA-256 `{EXPECTED_IMAGE_SHA256}`
- ServerProject comparison snapshot: commit `{SERVERPROJECT_SNAPSHOT_COMMIT}` at `{SERVERPROJECT_SNAPSHOT_COMMIT_TIME}`; the five files used below are independently size/SHA-256/text pinned by this checker
- Rows: {len(rows)} (`IMAGE` {image_rows}; `DATA` {data_rows}; `CAPTURE` {capture_rows})
- TSV SHA-256: `{tsv_digest}`
- Prior transport artifact SHA-256: `{EXPECTED_TRANSPORT_TSV_SHA256}`
- Every row carries explicit `evidence_grade`, `measurement_label`, `method`, and `control` fields. IMAGE resolver rows `GDL-IMG-018`, `GDL-IMG-019`, and `GDL-IMG-022` are `[A][MEASURED]` static proofs with executable instruction/CFG/stack/IAT/vtable/RTTI controls. `GDL-IMG-020` and the normal-success ordering portion of `GDL-IMG-021` are `[A][MANUAL_BOUNDED]` over exact hash-pinned spans; `GDL-IMG-021` additionally contains mechanically parsed PE/CLI metadata and whole-image byte censuses. None is a runtime observation.

## Exact client contract from IMAGE

The concrete inbound surface is `GSCN_RunTimeProtocolRes` (`runtime ID 0x6E9D`). Its optional field `+0x20`, selected by outer presence-mask bit `0x08`, is a `TerrainThingPool*`. The handler passes that pointer through a typed bridge to `DropThingModule_Client::reconcile`.

The client owns live ground objects in the module map at `+0x18`, keyed by `TerrainThing+0x10` (`u32`). New keys allocate/register/insert a `DropThingGameObj`; matching keys update in place. Presentation resolves local game data using `TerrainThing+0x14` and the keys `s_NAME`, `n_DROPMODEL_TYPE`, `n_QUALITY`, and `s_TAG_EXTRA`. No literal item name or model filename is carried on this wire path.

### Exact model selector, resource gate, and nameboard order

IMAGE now closes the local selector chain. `n_DROPMODEL_TYPE` is accepted directly only in `0..12`; there is no subtraction or remap. It indexes this exact token table:

`0=item, 1=weapon, 2=armor, 3=fittings, 4=money, 5=buff, 6=pandora, 7=crystal_r, 8=crystal_b, 9=crystal_g, 10=DROP_ENERGY, 11=DROP_LIFE, 12=holloween01`.

The client composes `.\\Data\\GC\\F\\<token>.nif`, calls the resource-open and type-filter path, and stores the result at `DropThingGameObj+0x84`. **Type 0 is valid and requests `item.nif`; it does not mean “no model.”** If `+0x84` is `NULL`, initialization returns false before XYZ placement and before the nameboard block. If non-NULL, the client applies XYZ/activation first and only then builds the nameboard.

`GDL-IMG-017` owns that selector and hard-gate result. `GDL-IMG-018` proves the setter and callback route conditionally. `GDL-IMG-021` now provides the missing **normal successful static bootstrap** join: parsed PE/CLI metadata resolves entry token `0x060000BA` to `<Module>._WinMainCRTStartup`, mechanically asserted native calls reach application initialization, and manual bounded CFG review over the exact pinned spans finds its fall-through successful continuation installing callback `0x00B02300` before later application-object construction and the non-NULL return continuation. A whole-image file-backed byte census mechanically finds exactly three encoded absolute slot references—the dispatch and two setter writes—and exactly one direct `E8` caller of the setter. The ordering statement is hash-anchored manual review rather than a complete instruction-decoder CFG proof, and none of this is evidence that a particular process executed; computed/aliased/dynamic writes and abnormal/external entry remain outside the census. On the proved callback route, mode-0 `rb` tries a private-copy rewrite from `.nif` to `.ni_` first and falls back to `_fsopen` with the untouched original `.nif` only when the packaged branch returns `NULL`. Mechanically pinned stack dataflow shows `_splitpath_s`'s extension output passed as `_stricmp` string1 and literal `.nif` as string2; equality reaches the length-gated final-character rewrite.

The packaged reader requires `$pcz`, takes the declared output size from header `+4`, then passes five property bytes at `+8` and compressed payload at `+0x0D` to a nine-argument `LzmaDecode`-shaped core. Its second decoder Boolean is ignored before returning the allocated buffer, so later file-validity and NiStream parser checks remain essential. `0x00B1B6C0` then returns non-NULL only for the first qualifying parsed collection entry whose RTTI walks to `NiNode`.

**[MANUAL_BOUNDED][IMAGE A]** Semantic review of the exact hash-pinned loader, type-filter, and wrapper-retain acceptance spans found no explicit descendant or geometry-type predicate before retained success; this absence was not mechanically proved. Indirect predicates, helper side effects, or overlooked predicates within or beyond the named spans remain possible. The `NiNode` constructor does transiently zero its child-container fields, but parsing may subsequently populate them; this derivation proves no post-parse child count and does not claim that a successfully parsed asset can validly remain zero-child. **A non-null qualifying parsed collection entry whose RTTI walks to NiNode does not prove geometry or pixels.** Hidden/culling state, materials, textures, renderer submission, camera placement, and actual pixels remain outside this static ceiling. The fall effect at `+0x8C` and the `s_TAG_EXTRA` effect at `+0x88` are separate resources; an FX or label disappearing is not proof that the wrapper or model object was deleted.

`GDL-IMG-022` closes the next static object/scene join. The accepted `wrapper+0x84` candidate is stored through DropThingGameObj vslot `+0x28` and retained at base `+0x78`; world registration calls vslot `+0x10`, rejects a NULL root, then invokes DropThingGameObj vslot `+0x1C`. Its bind path validates the same root, walks the scene graph recursively using NiNode child count `+0xB6` and child array `+0xB0`, and reaches state-activation calls. Existing IMAGE rows independently show that omission/range/full-clear removal calls world unregister before map erase and that destruction releases the retained references. This establishes a static registered scene-graph lifecycle, not renderer/device/framebuffer submission or pixels.

### [CLIENT-OBSERVED][B, measured elsewhere] / [COMPOSITE][D] GT-045 inference

The previously recorded uninstrumented GT-045 client observation was a label/dust with no visible item model; this generator does not re-observe or re-grade its screen evidence. The cross-layer inference is conditional: **if** that observed label came from this exact IMAGE-proved nameboard block, then `+0x84` was non-NULL and held a qualifying parsed collection entry whose RTTI walked to `NiNode`. That `[D]` composition does not convert “no visible model” into an IMAGE fact and does not distinguish descendants, culling, materials/textures, renderer submission, or camera placement. Control missing from GT-045: same-run branch/memory telemetry at the loader, RTTI result, and wrapper field.

### Source-separated DATA audits and report-only composition

`GDL-DATA-001` reports only the raw table rows and values for an externally specified 43-ID audit set: partition `22:30`, `24:10`, `26:3`; `n_DROPMODEL_TYPE` histogram `0:11`, `1:12`, `2:10`, `3:8`, `10:1`, `11:1`. It does not state why those IDs were selected. `GDL-DATA-002` reports only existence, size, and SHA-256 for an externally specified 13-file `.ni_` audit set; it is not a complete directory census and makes no IMAGE-token claim.

**[MEASURED][DATA]** `GDL-DATA-003` adds a deterministic decompressor/parser census over exactly those pinned files: {package_structure_observation} This is serialized-file structure only. It does not prove a runtime open/decode/parse, instantiated geometry, renderer submission, or pixels.

**[COMPOSITE][D — SERVERPROJECT SNAPSHOT + DATA + IMAGE]** At pinned ServerProject commit `{SERVERPROJECT_SNAPSHOT_COMMIT}` ({SERVERPROJECT_SNAPSHOT_COMMIT_TIME}), the reconstructed code selects the 43 IDs and its `(table_code, low_id, drop_model_type)` projection is checked against the external DATA audit. Separately, case-insensitive composition of the 13 audited DATA filenames with the IMAGE token table covers the 13 token stems. IMAGE proves the packaged-first `.ni_` route and its normal-success static callback installation; **[MEASURED][DATA]** DATA proves that every audited serialized root graph reaches at least one exact `NiMesh`, and that all 34 reachable meshes carry exact material/texturing/base-source/external-DDS references. None of these joins is emitted inside a DATA row, and the composition still does not prove that a particular runtime request opened, decoded, parsed, instantiated, found or decoded a referenced DDS, submitted, or rendered a file.

The following table is explicitly **COMPOSITE: replacement scope at pinned ServerProject commit `{SERVERPROJECT_SNAPSHOT_COMMIT}` + DATA values + IMAGE selector**. It is not an original-server issuance claim.

| DATA type | IMAGE token | Requested path suffix | Count | Pinned-snapshot-scope full item IDs |
|---:|---|---|---:|---|
{roster_table}

Two earlier high-value corrections are now explicit: `2400046` resolves through `ITEM_CONSUMABLES n_ID=46` to type `11` (`DROP_LIFE.nif`), while `2400047` resolves through `ITEM_CONSUMABLES n_ID=47` to type `10` (`DROP_ENERGY.nif`). They are not `ITEM_MISC` type `9/0`.

## Reconciliation matrix

| Incoming `+0x20` state | Exact client consequence |
|---|---|
| field absent, pointer remains `NULL` | unregister and erase every current ground object |
| field present, non-NULL pool, count `0` | return without mutation; preserve every current object |
| field present, nonempty pool | update matching keys, create new keys, and remove current keys omitted from the snapshot |
| live object outside the proven 2500-unit predicate | removable unless the audited bypass flag applies |

Manual static inspection found no clock/time API reference, clock comparison, or elapsed-time delete predicate in the named typed codec/handler/bridge/initializer/update/destructor spans. This is a hash-anchored bounded IMAGE observation: the checker verifies every named span hash, but it does **not** automate the semantic timer/xref absence test. Opaque fields remain unknown, so this does **not** prove absence of a serialized TTL/timestamp field, an indirect consumer, another client subsystem, or original-server lifetime policy.

Canonical `GDT-IMG-002` owns the pickup key-copy/enqueue fact. The new bounded negative here says only that the audited producer subspan has no direct `E8` call to the three pinned unregister/erase functions; it does not exclude indirect/helper deletion or prove the complete pickup lifecycle. The action selector `0x5B` path independently changes label-node visibility without a direct known delete call in its audited spans.

## Reconstructed replacement-code snapshot — separate from IMAGE/DATA/CAPTURE

- **[RECONSTRUCTED POLICY — SNAPSHOT `{SERVERPROJECT_SNAPSHOT_COMMIT}`]** immutable V141 `make_runtime_res_empty_exact` builds two zero masks, so its intended RuntimeRes extension mask is zero (`current/pf_login_game_server_v141.py:2182-2200`, SHA-256 `{SERVERPROJECT_SNAPSHOT_PINS[V141_PATH][1]}`). This is not a CAPTURE fact and V141 must not be edited.
- **[RECONSTRUCTED POLICY — SNAPSHOT `{SERVERPROJECT_SNAPSHOT_COMMIT}`]** the modular runtime owns exactly one `self.mob_loot_cell = DropLedgerCell()`; that cell locks mutations and lazily expires rows. `sustain_a_kill` composes the whole live ledger on a kill. Do not create a second heartbeat ledger (`runtime.py`, `mob_loot.py`, `mob_drop_presence.py` pinned by this checker).
- **[SNAPSHOT PIN REFRESH — NO CLIENT CLAIM]** relative to this artifact's immediately preceding runtime pin, commit `579a6bb49b896726c627c469136748affc387e17` added 32 logout-hypothesis lines to `runtime.py`; none touches the single `DropLedgerCell` ownership anchor or the pinned `mob_loot.py`/`mob_drop_presence.py` lifecycle anchors. At snapshot `{SERVERPROJECT_SNAPSHOT_COMMIT}`, `mob_loot.py` still contains the exact `DropLedgerCell`, lock, lazy-sweep, and whole-ledger anchors used above, plus read-only `lifetime_seconds` and locked `time_left` accessors. This is a read-only ServerProject comparison, not original-client evidence.
- **[RECONSTRUCTED POLICY — SNAPSHOT `{SERVERPROJECT_SNAPSHOT_COMMIT}`]** `field_drop_tables.py` selects exactly 43 item IDs and its `(table_code, low_id, drop_model_type)` projection matches every pinned DATA row. This is only the replacement scope at that snapshot; it is not proof that the original server issued exactly those 43 IDs.
- **[STALE SNAPSHOT WORDING FOUND READ-ONLY]** comments present in that pinned snapshot that say `n_DROPMODEL_TYPE` is “not the switch,” that nothing reads element `+0x14`, or that this roster contains 63 IDs are superseded by the exact IMAGE consumer and the 43-row audit/composition.
- **[RECONSTRUCTED POLICY — OPEN DESIGN AT SNAPSHOT `{SERVERPROJECT_SNAPSHOT_COMMIT}`]** ledger mutation is atomic, but snapshot -> compose -> socket-send is not yet proven totally ordered against pickup, expiry, another kill, or heartbeat. A stale nonempty generation can resurrect a removed key; count-zero preserve alone can leave a lazily expired client object indefinitely.

## Compatible integration contract — PROPOSED, not an instruction to patch V141

1. Reuse the single existing `DropLedgerCell`; do not create a second owner.
2. At the authorized modular adapter seam, serialize kill/pickup/expiry state transition, generation identity, composition, and socket-send order so an older nonempty generation cannot be sent after a newer omission.
3. For ordinary keepalive while drops exist, use a present non-NULL zero-count pool as the no-op/preserve shape; this avoids repeated full-set timer resend and does not snapshot the ledger.
4. On kill, successful pickup, or expiry, publish one ordered nonempty authoritative full-live-set generation; omit removed keys and retain every survivor. If the live set becomes empty, publish one deliberate all-clear. Lazy expiry needs an event/publisher if no later gameplay event would otherwise send the omission.
5. Send the exact item ID and XYZ through the proven TerrainThing fields; do not add a guessed literal model filename or `n_ID_MODEL` wire field. **[MEASURED][DATA]** The audited packaged files already have a pinned serialized root/child/`NiMesh`/material/base-DDS-reference census. Diagnose a blank by recording the resolved DATA row/type/token, packaged-versus-loose branch, runtime decode/parser result, qualifying parsed collection entry and RTTI result, instantiated child/geometry identity, `wrapper+0x84`/retained `+0x78`, world registration, referenced-DDS existence/open/decode/bind state, culling, and renderer/device state separately.
6. Treat lifetime ownership as an explicit reconstruction policy until original-server evidence says more; the IMAGE negative above does not rule out opaque or indirect client lifetime inputs.

## CAPTURE observations (source kept separate)

The complete pinned-session census contains three server-labelled `MOB_LOOT_DROP` log entries. Each is followed by the first later 14-byte heartbeat log at {deltas[0]} ms, {deltas[1]} ms, and {deltas[2]} ms; the primary console labels those heartbeats `exact empty RuntimeRes v4`. CAPTURE proves only logged ordering/timing/size/labels and send-side completion context. It does **not** expose/decode heartbeat bytes or prove mask zero, client delivery, client decode, memory mutation, or screen effect.

### Composite inference — IMAGE + pinned V141 replacement code + CAPTURE

CAPTURE establishes that the send-side logs recorded a 14-byte heartbeat after all three drops. The hash-pinned V141 replacement code at ServerProject snapshot `{SERVERPROJECT_SNAPSHOT_COMMIT}` establishes that its builder intends that heartbeat to carry extension mask zero. IMAGE establishes the conditional consequence: if those same bytes are delivered and decoded by the same-build `GSCN_RunTimeProtocolRes` path, absent bit `0x08` leaves `+0x20` NULL and the reconciler clears all current ground objects. This strongly identifies a dangerous shape, but it is not proof of delivery, decode, memory mutation, the screen event, or absence of every other lifetime mechanism.

Capture pins:

- `GAME_LIVE.txt`: {EXPECTED_CAPTURE_LIVE_SIZE} bytes / {EXPECTED_CAPTURE_LIVE_LINES} lines / SHA-256 `{EXPECTED_CAPTURE_LIVE_SHA256}`
- `server_console_live.out.txt`: {EXPECTED_CAPTURE_CONSOLE_SIZE} bytes / {EXPECTED_CAPTURE_CONSOLE_LINES} lines / SHA-256 `{EXPECTED_CAPTURE_CONSOLE_SHA256}`
- canonical attended note: {EXPECTED_ATTENDED_NOTE_SIZE} bytes / SHA-256 `{EXPECTED_ATTENDED_NOTE_SHA256}`

## FightingDrop classification

`FightingDropModule_Client` and `FightingDropNotify` remain custom-reflection-only findings in `PF_GROUND_DROP_TRANSPORT.tsv` (`GDT-IMG-008`, `GDT-IMG-009`). They are a false lead for this concrete typed inbound path: the exact path selects `GSCN_RunTimeProtocolRes+0x20 TerrainThingPool`. This does not claim the FightingDrop classes are globally unused.

## Provenance and nonclaims

- Every TSV row has exactly one source label: `IMAGE`, `DATA`, or `CAPTURE`; no row mixes evidence layers.
- `semantic_fingerprint` excludes `evidence_id`; generation fails on duplicate claim semantics and self-checks that renaming an ID cannot change the fingerprint.
- No packet, dump, capture, or image raw bytes are copied into either output artifact.
- No client, server, dump, or capture was executed; all inputs were read-only.
- **[MEASURED][DATA]** The 13 explicitly pinned packaged assets were decoded in memory and structurally parsed; outputs contain only audited asset filenames, sizes, hashes, block/root indexes, type names, `.dds` suffix classification, and counts—never proprietary raw bytes or referenced texture names.
- **[MEASURED][DATA]** Serialized root-reachable `NiMesh` and material/texturing/base-source references do not prove referenced-DDS existence, runtime decode/binding, instantiated geometry, renderer submission, or pixels. Likewise, a non-null qualifying parsed collection entry whose RTTI walks to `NiNode` does not by itself prove geometry or pixels.
- No original-server policy is inferred from the emulator's event label `MOB_LOOT_DROP`.
- The five-file ServerProject snapshot at commit `{SERVERPROJECT_SNAPSHOT_COMMIT}` is verified by hash/text pins but is not emitted as an IMAGE/DATA/CAPTURE TSV row and is never original evidence; later commits are outside this artifact until explicitly re-pinned.
- `current/pf_login_game_server_v141.py` is immutable; the proposal leaves the authorized modular publication seam as an explicit design/implementation task for chief/COO.
- Files under `pf_bridge/external` are local-only/Git-ignored by workspace policy; another clone will not receive this trio until owner-approved packaging. This checker does not modify Git.
- `--check` is read-only: it creates neither the output lock nor temporary/output files. It verifies the script's TSV/MD and pinned inputs only; it does not validate append-only notes in `notes_to_chief`. Generation mode alone takes the exclusive output lock.
- Re-run with `py -3 -B pf_rederive_ground_drop_lifetime.py --check` to verify exact outputs and all pinned inputs.
"""
    measured_data_narrative_markers = (
        "`GDL-DATA-003` adds a deterministic decompressor/parser census",
        "all 34 reachable meshes carry exact material/texturing/base-source/",
        "pinned serialized root/child/`NiMesh`/material/base-DDS-reference census",
        "The 13 explicitly pinned packaged assets were decoded in memory",
        "Serialized root-reachable `NiMesh` and material/texturing/base-source",
    )
    for marker in measured_data_narrative_markers:
        matching_lines = [line for line in text.splitlines() if marker in line]
        if len(matching_lines) != 1:
            raise ValueError(f"DATA narrative marker census drift: {marker}")
        if "[MEASURED][DATA]" not in matching_lines[0]:
            raise ValueError(f"unlabelled DATA narrative claim: {marker}")
    return text.encode("utf-8")


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


def atomic_write(path: Path, content: bytes) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    fd: int | None = None
    try:
        fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as stream:
            fd = None
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if fd is not None:
            os.close(fd)
        temporary.unlink(missing_ok=True)
    if path.read_bytes() != content:
        raise ValueError(f"post-write verification failed: {path.name}")


def check_file(path: Path, content: bytes) -> None:
    if not path.is_file():
        raise ValueError(f"missing output: {path.name}")
    actual = path.read_bytes()
    if actual != content:
        raise ValueError(
            f"output mismatch: {path.name}; expected_sha256={sha256(content)} "
            f"actual_sha256={sha256(actual)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify existing outputs instead of writing them",
    )
    args = parser.parse_args()

    # Check mode is deliberately read-only: it creates no lock or temporary
    # file. Generation alone takes the exclusive output lock because it is the
    # only mode that can replace the canonical artifacts.
    lock_fd: int | None = None
    if not args.check:
        lock_fd = acquire_lock()
    try:
        observed_head_before = observe_serverproject_head()
        worktree_matches_snapshot_before = (
            worktree_matches_serverproject_snapshot()
        )
        image_before, pe = verify_image()
        snapshot_code_before = verify_serverproject_snapshot()
        verify_snapshot_roster(snapshot_code_before)
        data_tables, data_inputs_before, asset_structures_before = verify_data_inputs()
        canonical_keys = verify_transport_reference()
        live_before, console_before, note_before, capture_observations = verify_capture()
        rows = make_rows(
            pe,
            canonical_keys,
            capture_observations,
            data_tables,
            asset_structures_before,
        )
        tsv = render_tsv(rows)
        md = render_md(rows, sha256(tsv))

        if args.check:
            check_file(TSV_PATH, tsv)
            check_file(MD_PATH, md)
            mode = "check"
        else:
            atomic_write(TSV_PATH, tsv)
            atomic_write(MD_PATH, md)
            check_file(TSV_PATH, tsv)
            check_file(MD_PATH, md)
            mode = "write"

        image_after, _ = verify_image()
        snapshot_code_after = verify_serverproject_snapshot()
        verify_snapshot_roster(snapshot_code_after)
        (
            _data_tables_after,
            data_inputs_after,
            asset_structures_after,
        ) = verify_data_inputs()
        live_after, console_after, note_after, _ = verify_capture()
        if image_before != image_after:
            raise ValueError("image changed during re-derivation")
        if snapshot_code_before != snapshot_code_after:
            raise ValueError("ServerProject snapshot changed during re-derivation")
        if data_inputs_before != data_inputs_after:
            raise ValueError("DATA input changed during re-derivation")
        if asset_structures_before != asset_structures_after:
            raise ValueError("decoded DATA structure changed during re-derivation")
        if live_before != live_after or console_before != console_after:
            raise ValueError("capture changed during re-derivation")
        if note_before != note_after:
            raise ValueError("attended note changed during re-derivation")
        verify_transport_reference()
        check_file(TSV_PATH, tsv)
        check_file(MD_PATH, md)
        observed_head_after = observe_serverproject_head()
        worktree_matches_snapshot_after = (
            worktree_matches_serverproject_snapshot()
        )
        result_lines = [
            f"mode={mode}",
            f"serverproject_snapshot_commit={SERVERPROJECT_SNAPSHOT_COMMIT}",
            f"serverproject_snapshot_commit_time={SERVERPROJECT_SNAPSHOT_COMMIT_TIME}",
            f"serverproject_observed_head_before={observed_head_before}",
            f"serverproject_observed_head_after={observed_head_after}",
            "serverproject_observed_head_moved_during_run="
            f"{str(observed_head_before != observed_head_after).lower()}",
            "serverproject_worktree_matches_snapshot_before="
            f"{str(worktree_matches_snapshot_before).lower()}",
            "serverproject_worktree_matches_snapshot_after="
            f"{str(worktree_matches_snapshot_after).lower()}",
            f"image_size_before={len(image_before)}",
            f"image_sha256_before={sha256(image_before)}",
            f"image_size_after={len(image_after)}",
            f"image_sha256_after={sha256(image_after)}",
            f"serverproject_snapshot_files={len(snapshot_code_after)}",
            f"image_rows={sum(row['source'] == 'IMAGE' for row in rows)}",
            f"data_rows={sum(row['source'] == 'DATA' for row in rows)}",
            f"capture_rows={sum(row['source'] == 'CAPTURE' for row in rows)}",
            f"rows={len(rows)}",
            f"tsv_size={len(tsv)}",
            f"tsv_sha256={sha256(tsv)}",
            f"md_size={len(md)}",
            f"md_sha256={sha256(md)}",
        ]
    finally:
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
        print(f"status=FAIL error={type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
