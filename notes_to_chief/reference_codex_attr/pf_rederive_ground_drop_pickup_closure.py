#!/usr/bin/env python3
"""Re-derive the bounded P0-6 ground-drop/pickup closure.

The generator is source-separated: IMAGE rows come only from the pinned
original client image and content-addressed IMAGE artifacts; CAPTURE rows come
only from a metadata/census pass over capture_* files.  It never emits capture
payload bytes and never reads or runs replacement-server code.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import struct
import sys
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
GAME_CLIENT_ROOT = PF_ROOT / "GameClient"
IMAGE_PATH = GAME_CLIENT_ROOT / "GameClient.local.bin"
GAME_LOCK_PATH = OUT_DIR.parent / "LOCK_GAME.txt"
TSV_PATH = OUT_DIR / "PF_GROUND_DROP_PICKUP_CLOSURE.tsv"
REPORT_PATH = OUT_DIR / "PF_GROUND_DROP_PICKUP_CLOSURE.md"
PAIR_PATH = OUT_DIR / "PF_GROUND_DROP_PICKUP_CLOSURE.pair.json"
LOCK_PATH = OUT_DIR / ".PF_GROUND_DROP_PICKUP_CLOSURE.lock"
STAGE_PREFIXES = (
    ".PF_GROUND_DROP_PICKUP_CLOSURE.tsv.",
    ".PF_GROUND_DROP_PICKUP_CLOSURE.md.",
    ".PF_GROUND_DROP_PICKUP_CLOSURE.pair.json.",
)

SOURCE_IMAGE = "IMAGE"
SOURCE_CAPTURE = "CAPTURE"
IMAGE_SOURCE_FILE = "PF_ROOT://GameClient/GameClient.local.bin"
CAPTURE_SOURCE_FILE = "PF_ROOT://GameClient/**/capture_*/**/*"
IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"

GDT_PATH = OUT_DIR / "PF_GROUND_DROP_TRANSPORT.tsv"
GDL_PATH = OUT_DIR / "PF_GROUND_DROP_LIFETIME.tsv"
VALIDATOR_PATH = OUT_DIR / "pf_validate_capture_fields.py"
REGISTRY_PATH = OUT_DIR / "PF_PROTOCOL_REGISTRY.tsv"
FIELDS_PATH = OUT_DIR / "PF_SERIALIZER_FIELDS.tsv"
TAG_PATH = OUT_DIR / "PF_TAG_CENSUS.tsv"
INVENTORY_PATH = OUT_DIR / "PF_INPUT_INVENTORY.tsv"
FIELD_VALIDATION_PATH = OUT_DIR / "PF_FIELD_VALIDATION.tsv"
URGENT_PATH = (
    OUT_DIR.parent
    / "notes_to_chief"
    / "CODEX_URGENT_20260901_2040_P05-CORPSE-DROP-STATE-SCOPE.md"
)

INPUT_PINS = {
    GDT_PATH: (26_924, "9e2396795ee32287f1f9b82f22fb8f394464d2b0a25375d07108ee138c73907b"),
    GDL_PATH: (61_979, "b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710"),
    VALIDATOR_PATH: (47_884, "0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8"),
    REGISTRY_PATH: (89_506, "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d"),
    FIELDS_PATH: (25_195_473, "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"),
    TAG_PATH: (1_985, "63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a"),
    INVENTORY_PATH: (364_080, "729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1"),
    FIELD_VALIDATION_PATH: (72_849, "080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3"),
    URGENT_PATH: (9_289, "8b8904aed010ff49566b8af6bfb99898358e80b1f78f8fe2c014f58ea847aa8b"),
}

CURRENT_CAPTURE_FILES = 2_227
CURRENT_CAPTURE_BYTES = 699_015_496
CURRENT_CAPTURE_MANIFEST = "b8284a566d9993f52540dea52e82896b0d8eb499b9aa83ceb74084a0e671db3c"
CURRENT_TEXT_FILES = 1_337
CURRENT_BLOCKS = 81_954
CURRENT_NESTED_DECLARED = 31_071
CURRENT_NESTED_REACHED = 30_334
FROZEN_CAPTURE_FILES = 1_772
FROZEN_CAPTURE_BYTES = 595_134_426
TAIL_EVENT_MANIFEST = "abaedb66ed9a2bbf8fae8ab872b92ef4d8b20736a23d7159b2d7f0300fb2b7be"
ALL_UNRESOLVED_LOCATOR_MANIFEST = "23b8427bdf1ab56089dba2fa0a7c2f81d6a9f25b3a391ee03eecbebc665a7878"
PATH_CAPTURE_V_CLASS = "PATH_CLASSIFIED_CAPTURE_V_PREFIX"
AUTHORITATIVE_CAPTURE_PROVENANCE_LEDGER = None
FORBIDDEN_UNLEDGERED_PROVENANCE_CLAIMS = (
    "are REPLACEMENT provenance",
    "current REPLACEMENT corpus",
    "ORIGINAL=0",
    "UNKNOWN=0",
    "eligible_original_exchange_count=",
    "confirmed_nonempty_original=",
    "exact_reached_pickup_replacement=",
)
CAPTURE_FULL_ROW_TEMPLATE_SHA256 = {
    "GDP-CAP-001": "8411bc0ed4a2006d82da09b4183289b4a52b08ad7777fe49f53b93e0c1cd0f7d",
    "GDP-CAP-002": "a3204db31d0ee59e533933776ed25ad136236ef55e32672fbd6c5a11b80d696b",
    "GDP-CAP-003": "9f4a650819ff73bf593d717b4e729a6d48bd9f87385cdedc22bb7e9e004b246f",
    "GDP-CAP-004": "862758f7e8e1b1a365c4c6ef5f16a16208dbc593b3fb2567413e9dcaa97a013e",
    "GDP-CAP-005": "69fb8ecbd739b9230fb0df8197b9dfe32683ddc9835c4d48ad1dcbe2bc7863fc",
    "GDP-CAP-006": "816afb8ab15931b953d5e98abf5d86fa34bca4a2035b1be90b10447f19ceaac1",
    "GDP-CAP-007": "69b8c70fa872949b0753d868e2ba19da46f356e1b9738f360c77687371a6c2db",
}
EXPECTED_REPORT_SHA256 = "52981a6ad0c505f5d62d2430d54f41e074ae43b26fbfe3b6521ed1d2dae39b8f"
TRUNCATED_DERIVED_MASK_LOCATORS = (
    (
        "capture_gt010_20260818_015927/capture_v141/GAME_20260818_020106_955833_62358.txt",
        "22afd705194e15b97dc1ed3605487e667f268d5ba8671bb01a99c9a05dd5e3bf",
        6,
        "6ddeeb879f8c7871a4655ed4f16a1955220e6e73136d4a8ad6087e49f48624e3",
    ),
    (
        "capture_gt101_20260827_143419/capture_v141/GAME_20260827_143641_602267_55866.txt",
        "104abb1e6e9a793ecfa2cabfbdcccf73eaef39a6c75526264b94ef420227d7f5",
        8,
        "c6b19acb5786889cc2e18f03586b3b597b1a72301c7f873322f27bbb1e6f9e22",
    ),
    (
        "capture_gt107_20260827_172426/capture_v141/GAME_20260827_173114_446035_53082.txt",
        "7bac8141e3d073100687c8bda9a34600981fc8e344f67c3dbbc2bbb58ee0a31e",
        8,
        "0ec871048ab41aa2131feddf6faf6c5f39f2bc90bb5b954c3b5c68897ac31ba8",
    ),
)

TARGET_NAMES = (
    "PickupTerrainThing",
    "DropThingModule_Client",
    "FightingDropModule_Client",
    "FightingDropNotify",
)

ROW_DOMAIN = b"PF_GROUND_DROP_PICKUP_CLOSURE_ROW_V1\x00"
PAIR_DOMAIN = b"PF_GROUND_DROP_PICKUP_CLOSURE_PAIR_V1\x00"


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


@dataclass(frozen=True)
class PriorClaim:
    token: str
    artifact_sha256: str
    claim_digest: str


@dataclass(frozen=True)
class CaptureFacts:
    file_count: int
    byte_count: int
    manifest_sha256: str
    text_files: int
    blocks: int
    nested_declared: int
    nested_reached: int
    target_stats: Mapping[tuple[str, str], tuple[int, int, int]]
    runtime_res_absent: int
    runtime_res_count_zero: int
    runtime_res_nonempty: int
    runtime_res_uncertain: int
    runtime_res_truncated_mask: int
    runtime_res_nonempty_files: int
    runtime_res_unique_frames: int
    runtime_res_event_manifest: str
    runtime_res_uncertain_manifest: str
    runtime_res_pool_count_one: int
    runtime_res_pool_count_two: int
    runtime_res_outer00_absent: int
    runtime_res_outer00_nonempty: int
    runtime_res_outer02_absent: int
    runtime_res_outer02_uncertain: int
    runtime_res_sequence_add: int
    runtime_res_sequence_add_omit: int
    runtime_res_sequence_same_set: int
    runtime_res_one_entry_swaps: int
    c2s_outer_blocks: int
    c2s_gameplay_outer_blocks: int
    c2s_login_outer_blocks: int
    c2s_no_nested_blocks: int
    c2s_nested_declared: int
    c2s_nested_reached: int
    c2s_nested_fail_closed: int
    c2s_pickup_reached: int


@dataclass(frozen=True)
class TailCensus:
    absent: int
    count_zero: int
    nonempty: int
    uncertain: int
    truncated_mask: int
    nonempty_files: int
    unique_frames: int
    event_manifest: str
    uncertain_manifest: str
    pool_count_one: int
    pool_count_two: int
    outer00_absent: int
    outer00_nonempty: int
    outer02_absent: int
    outer02_uncertain: int
    sequence_add: int
    sequence_add_omit: int
    sequence_same_set: int
    one_entry_swaps: int
    c2s_outer_blocks: int
    c2s_gameplay_outer_blocks: int
    c2s_login_outer_blocks: int
    c2s_no_nested_blocks: int
    c2s_nested_declared: int
    c2s_nested_reached: int
    c2s_nested_fail_closed: int
    c2s_pickup_reached: int


EXPECTED_SECTIONS = (
    (".text", 0x00401000, 0x00838A2C, 0x00000400, 0x00838C00, True),
    (".code", 0x00C3A000, 0x000002E1, 0x00839000, 0x00000400, True),
    (".rdata", 0x00C3B000, 0x003DE38E, 0x00839400, 0x003DE400, False),
    (".data", 0x0101A000, 0x00081F70, 0x00C17800, 0x00011E00, False),
    (".rsrc", 0x0109C000, 0x00058998, 0x00C29600, 0x00058A00, False),
    (".reloc", 0x010F5000, 0x001915F0, 0x00C82000, 0x00191600, False),
)

SPANS = {
    "descriptor_init": Span(0x00BF0380, 0x00BF03B7, "b71cbe6bbca3fec65257d7b1c22df72e6e85846ac5b82612dfcfe894e468d57f"),
    "type_descriptor": Span(0x0101C218, 0x0101C237, "ec0854ba307eced6b96e3e152c38ad236a64b5dccf04545caa64da3e25d3e633"),
    "dropobj_vtable": Span(0x00F30FAC, 0x00F30FDC, "d5e4811779c1c30cbbe0c912b7e3000bc4c10d2d1c40c6d406e3be61666637ff"),
    "type_getter": Span(0x005F4B90, 0x005F4B96, "b544508e2ae4e2cdd4f5f0fb865605a53fc8114b89bf2df92e5a4bfa8c933400"),
    "type_chain_helper": Span(0x0088F2B0, 0x0088F2D1, "00076eb0d61b7763ba58709f657437f455e6c6a2e3da83b3005bef0b847a61e9"),
    "click_type_gate": Span(0x006B043F, 0x006B046A, "f965ee31d581e5c182c06dae44f6fa43f2f096d0ac3dabcb8bb9ee3ae38e032c"),
    "dropobj_retain": Span(0x005F41E0, 0x005F4259, "96535cd88b3d79525fc3d7b2547150c2ee09c183e21b8fdb9c6dd934252a4a3c"),
    "pickup_emit": Span(0x006B062D, 0x006B0658, "517634cd1d2f5ad97cbecbcfa091caa476d3a21bbac7341a134f119ed2a3542d"),
    "full_click": Span(0x006B03F0, 0x006B069B, "a393f3d41b7f389fac31bc82a7cf4e78367d0413a5427d5dfe91d762b9685827"),
    "reconcile": Span(0x006AF970, 0x006B03E3, "e5eb9e1fdae15544773c7e94fa6ff6aaa6990650cbb05f20e39a009941575663"),
    "pickup_getid": Span(0x005E46A0, 0x005E46A7, "d3fc621e95d5e98c081cab3e22ab7d424901e8fb0cb3d7d2be5f90d9fe6919b1"),
    "nested_writer": Span(0x005F38F0, 0x005F39DE, "4a928b3ea6671d915c1f72fb399b7a39e335790c0af045e8f6d46c164ffdb5f7"),
    "gameplay_getid": Span(0x005E36F0, 0x005E36F7, "0671aa9bd241d5acf0555f0e9e2f969d2f385d0821cd4ec0bb1df4affd86450f"),
    "login_getid": Span(0x005E3710, 0x005E3717, "96ec6ab10267b8616954b00022bef2f66a184d589bdf0e08871ff7ee121a30d0"),
    "request_serializer": Span(0x005F4070, 0x005F4110, "27a079028e76685564ac37c0ff27c38996837970fe347e6be54474cf8c19c60a"),
    "outer_writer": Span(0x00C3A0A0, 0x00C3A103, "e1843bba51c3375a03ee2a6b64b893f82a44afd63682bb7e5c96824e3bf217f0"),
    "serialize_driver": Span(0x00A8CC30, 0x00A8CCE0, "c77c78397f008024b5cefeeb01574af6ede045694debc6d5d842d213e7c1513c"),
    "transform_repack": Span(0x00A8C8D0, 0x00A8C987, "7483b19ac8f5c72f9a0c102ad6e38b904be1b330d9eddaaa92841dba502fc975"),
    "buffer_rewrite": Span(0x00B743B0, 0x00B74400, "41d0f05e451a79988125d8d0954690fe8fdb9905f88eb78cd17e5c676e00ac56"),
    "chunk_send": Span(0x00A8CB30, 0x00A8CC23, "b14dbf1ba5f3b852039ea930172114fb8fd2688d3ac7518ee3584b9ce6cc5c80"),
    "send_thunk": Span(0x00B378E6, 0x00B378EC, "588966721d3d648af5cceaa75351f3827ef9387f489f7eb2eae8771807a1be25"),
}

FIELDNAMES = (
    "closure_id",
    "row_kind",
    "phase",
    "subject",
    "direction",
    "semantic_status",
    "exact_observation",
    "value_or_layout",
    "evidence_mode",
    "span_start_va",
    "span_end_va",
    "file_off_start",
    "file_off_end",
    "span_sha256",
    "support_spans",
    "direct_assertions",
    "prior_reference",
    "prior_artifact_sha256",
    "prior_claim_digest",
    "capture_file_count",
    "capture_total_bytes",
    "capture_manifest_sha256",
    "capture_text_file_count",
    "capture_block_count",
    "source",
    "provenance",
    "source_file",
    "source_size",
    "source_sha256",
    "nonclaim",
    "blocker",
    "required_next_evidence",
    "claim_sha256",
    "evidence_key",
)

EXPECTED_IDS = (
    "GDP-IMG-001",
    "GDP-IMG-002",
    "GDP-IMG-003",
    "GDP-IMG-004",
    "GDP-IMG-005",
    "GDP-IMG-006",
    "GDP-IMG-007",
    "GDP-IMG-008",
    "GDP-CAP-001",
    "GDP-CAP-002",
    "GDP-CAP-003",
    "GDP-CAP-004",
    "GDP-CAP-005",
    "GDP-CAP-006",
    "GDP-CAP-007",
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_digest(row: Mapping[str, str]) -> str:
    return sha256(
        json.dumps(dict(row), sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    )


def digest_lines(lines: Sequence[str]) -> str:
    return sha256(("\n".join(lines) + "\n").encode("utf-8"))


def read_pinned(path: Path, expected_size: int, expected_sha256: str) -> bytes:
    raw = path.read_bytes()
    if len(raw) != expected_size or sha256(raw) != expected_sha256:
        raise RuntimeError(f"pinned input mismatch: {path.name}")
    return raw


def assert_game_lock_released() -> str:
    first = GAME_LOCK_PATH.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    if first.startswith("HELD"):
        raise RuntimeError("LOCK_GAME is HELD; heavy capture/IMAGE scan refused")
    if not first.startswith("RELEASED"):
        raise RuntimeError("LOCK_GAME state is neither HELD nor RELEASED")
    return first


def parse_pe(image: bytes) -> tuple[Section, ...]:
    if image[:2] != b"MZ":
        raise RuntimeError("image DOS signature mismatch")
    pe_off = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_off : pe_off + 4] != b"PE\x00\x00":
        raise RuntimeError("image PE signature mismatch")
    count = struct.unpack_from("<H", image, pe_off + 6)[0]
    optional_size = struct.unpack_from("<H", image, pe_off + 20)[0]
    optional = pe_off + 24
    if struct.unpack_from("<H", image, optional)[0] != 0x10B:
        raise RuntimeError("image is not PE32")
    if struct.unpack_from("<I", image, optional + 28)[0] != 0x00400000:
        raise RuntimeError("image base mismatch")
    table = optional + optional_size
    sections: list[Section] = []
    for index in range(count):
        off = table + index * 40
        name = image[off : off + 8].split(b"\x00", 1)[0].decode("ascii")
        virtual_size, rva, raw_size, raw_off = struct.unpack_from("<IIII", image, off + 8)
        characteristics = struct.unpack_from("<I", image, off + 36)[0]
        sections.append(
            Section(name, 0x00400000 + rva, virtual_size, raw_off, raw_size, bool(characteristics & 0x20000000))
        )
    actual = tuple((s.name, s.va, s.virtual_size, s.file_off, s.raw_size, s.executable) for s in sections)
    if actual != EXPECTED_SECTIONS:
        raise RuntimeError("PE section layout mismatch")
    return tuple(sections)


def va_to_offset(sections: Sequence[Section], va: int, length: int = 1) -> int:
    for section in sections:
        backed = min(section.virtual_size, section.raw_size)
        if section.va <= va and va + length <= section.va + backed:
            return section.file_off + va - section.va
    raise RuntimeError(f"VA is not file-backed: 0x{va:08X}")


def span_bytes(image: bytes, sections: Sequence[Section], name: str) -> tuple[bytes, int, int]:
    spec = SPANS[name]
    start = va_to_offset(sections, spec.start, spec.end - spec.start)
    end = start + spec.end - spec.start
    raw = image[start:end]
    if sha256(raw) != spec.sha256:
        raise RuntimeError(f"span hash mismatch: {name}")
    return raw, start, end


def format_span(image: bytes, sections: Sequence[Section], name: str) -> str:
    _raw, start, end = span_bytes(image, sections, name)
    spec = SPANS[name]
    return (
        f"{name}=VA:0x{spec.start:08X}..0x{spec.end:08X}"
        f"@file:0x{start:08X}..0x{end:08X}@sha256:{spec.sha256}"
    )


def expect_bytes(image: bytes, sections: Sequence[Section], va: int, expected_hex: str) -> None:
    expected = bytes.fromhex(expected_hex)
    off = va_to_offset(sections, va, len(expected))
    if image[off : off + len(expected)] != expected:
        raise RuntimeError(f"instruction-shape guard failed at 0x{va:08X}")


def expect_dwords(image: bytes, sections: Sequence[Section], va: int, expected: Sequence[int]) -> None:
    off = va_to_offset(sections, va, 4 * len(expected))
    actual = struct.unpack_from("<" + "I" * len(expected), image, off)
    if actual != tuple(expected):
        raise RuntimeError(f"dword shape guard failed at 0x{va:08X}")


def call_target(image: bytes, sections: Sequence[Section], site: int) -> int:
    off = va_to_offset(sections, site, 5)
    if image[off] != 0xE8:
        raise RuntimeError(f"expected direct E8 call at 0x{site:08X}")
    relative = struct.unpack_from("<i", image, off + 1)[0]
    return (site + 5 + relative) & 0xFFFFFFFF


def expect_call(image: bytes, sections: Sequence[Section], site: int, target: int) -> None:
    if call_target(image, sections, site) != target:
        raise RuntimeError(f"direct call target drift at 0x{site:08X}")


def raw_e8_lines(image: bytes, sections: Sequence[Section], span_name: str) -> list[str]:
    raw, _start_off, _end_off = span_bytes(image, sections, span_name)
    start = SPANS[span_name].start
    lines: list[str] = []
    for index in range(len(raw) - 4):
        if raw[index] != 0xE8:
            continue
        relative = struct.unpack_from("<i", raw, index + 1)[0]
        site = start + index
        target = (site + 5 + relative) & 0xFFFFFFFF
        lines.append(f"0x{site:08X}->0x{target:08X}")
    return lines


def read_cstring(image: bytes, offset: int) -> str:
    end = image.index(b"\x00", offset)
    return image[offset:end].decode("ascii")


def resolve_imports(image: bytes, sections: Sequence[Section]) -> dict[int, tuple[str, str]]:
    pe_off = struct.unpack_from("<I", image, 0x3C)[0]
    optional = pe_off + 24
    image_base = struct.unpack_from("<I", image, optional + 28)[0]
    import_rva, import_size = struct.unpack_from("<II", image, optional + 104)
    if not import_rva or not import_size:
        raise RuntimeError("PE import directory missing")
    descriptor_off = va_to_offset(sections, image_base + import_rva, 20)
    result: dict[int, tuple[str, str]] = {}
    index = 0
    while True:
        off = descriptor_off + index * 20
        original_first_thunk, _stamp, _forwarder, name_rva, first_thunk = struct.unpack_from("<IIIII", image, off)
        if not any((original_first_thunk, name_rva, first_thunk)):
            break
        dll = read_cstring(image, va_to_offset(sections, image_base + name_rva)).lower()
        name_table_rva = original_first_thunk or first_thunk
        thunk_index = 0
        while True:
            value = struct.unpack_from("<I", image, va_to_offset(sections, image_base + name_table_rva + thunk_index * 4, 4))[0]
            if value == 0:
                break
            if value & 0x80000000:
                symbol = f"ordinal_{value & 0xFFFF}"
            else:
                hint_name = va_to_offset(sections, image_base + value, 3)
                symbol = read_cstring(image, hint_name + 2)
            result[image_base + first_thunk + thunk_index * 4] = (dll, symbol)
            thunk_index += 1
        index += 1
    return result


def load_tsv_pinned(path: Path) -> list[dict[str, str]]:
    size, digest = INPUT_PINS[path]
    raw = read_pinned(path, size, digest)
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise RuntimeError(f"pinned TSV has no rows: {path.name}")
    return rows


def prior_row_digest(row: Mapping[str, str]) -> str:
    for field in ("claim_sha256", "semantic_fingerprint"):
        value = row.get(field, "")
        if len(value) == 64 and all(ch in "0123456789abcdef" for ch in value):
            return value
    return canonical_digest(row)


def select_prior(
    rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]],
    path: Path,
    key_column: str,
    key: str,
) -> PriorClaim:
    matches = [row for row in rows_by_path[path] if row.get(key_column) == key]
    if len(matches) != 1:
        raise RuntimeError(f"prior row missing or duplicated: {path.name}:{key}")
    row = matches[0]
    if row.get("source") != SOURCE_IMAGE:
        raise RuntimeError(f"prior row source drift: {path.name}:{key}")
    evidence_key = row.get("evidence_key", "")
    suffix = f"@{evidence_key}" if evidence_key else ""
    return PriorClaim(
        token=f"{path.name}:{key}{suffix}",
        artifact_sha256=INPUT_PINS[path][1],
        claim_digest=prior_row_digest(row),
    )


def join_prior(claims: Sequence[PriorClaim]) -> tuple[str, str, str]:
    if not claims:
        return "N/A", "N/A", "N/A"
    return (
        ";".join(claim.token for claim in claims),
        ";".join(claim.artifact_sha256 for claim in claims),
        ";".join(claim.claim_digest for claim in claims),
    )


def build_prior_claims() -> tuple[
    dict[str, PriorClaim], Mapping[Path, Sequence[Mapping[str, str]]]
]:
    rows_by_path: dict[Path, Sequence[Mapping[str, str]]] = {
        GDT_PATH: load_tsv_pinned(GDT_PATH),
        GDL_PATH: load_tsv_pinned(GDL_PATH),
    }
    prior = {
        "gdt_pickup_id": select_prior(rows_by_path, GDT_PATH, "transport_id", "GDT-IMG-001"),
        "gdt_pickup_producer": select_prior(rows_by_path, GDT_PATH, "transport_id", "GDT-IMG-002"),
        "gdt_gameplay_outer": select_prior(rows_by_path, GDT_PATH, "transport_id", "GDT-IMG-004"),
        "gdt_login_outer": select_prior(rows_by_path, GDT_PATH, "transport_id", "GDT-IMG-005"),
        "gdt_nested_writer": select_prior(rows_by_path, GDT_PATH, "transport_id", "GDT-IMG-006"),
        "gdt_transport": select_prior(rows_by_path, GDT_PATH, "transport_id", "GDT-IMG-007"),
        "gdt_fighting_module": select_prior(rows_by_path, GDT_PATH, "transport_id", "GDT-IMG-008"),
        "gdt_fighting_notify": select_prior(rows_by_path, GDT_PATH, "transport_id", "GDT-IMG-009"),
        "gdl_inbound": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-001"),
        "gdl_dispatch": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-003"),
        "gdl_pool_codec": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-004"),
        "gdl_owner": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-005"),
        "gdl_null": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-007"),
        "gdl_empty": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-008"),
        "gdl_omission": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-009"),
        "gdl_range": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-010"),
        "gdl_pickup_negative": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-013"),
        "gdl_clear": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-IMG-015"),
        "gdl_false_lead": select_prior(rows_by_path, GDL_PATH, "evidence_id", "GDL-CREF-001"),
    }
    return prior, rows_by_path


def verify_prior_semantics(rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]]) -> None:
    gdt = {row["transport_id"]: row for row in rows_by_path[GDT_PATH]}
    gdl = {row["evidence_id"]: row for row in rows_by_path[GDL_PATH]}
    required_gdt = {
        "GDT-IMG-001": ("0x4543", "NOT_ESTABLISHED_BY_IMAGE"),
        "GDT-IMG-004": ("0x6E6F", "NOT_ESTABLISHED_BY_IMAGE"),
        "GDT-IMG-005": ("0x453A", "NOT_ESTABLISHED_BY_IMAGE"),
    }
    for key, (runtime_id, wire_status) in required_gdt.items():
        row = gdt[key]
        if row["runtime_id"] != runtime_id or row["wire_opcode_status"] != wire_status:
            raise RuntimeError(f"canonical discriminator ceiling drift: {key}")
    if "nested runtime type ID" not in gdt["GDT-IMG-006"]["nonclaim"]:
        raise RuntimeError("canonical nested-ID classification drift")
    if "buffer encoding rather than socket transmission" not in gdt["GDT-IMG-007"]["nonclaim"]:
        raise RuntimeError("canonical transport ceiling drift")
    expected_topics = {
        "GDL-IMG-007": "RECONCILE_NULL",
        "GDL-IMG-008": "RECONCILE_EMPTY",
        "GDL-IMG-009": "RECONCILE_OMISSION",
        "GDL-IMG-010": "RECONCILE_RANGE",
        "GDL-IMG-013": "PICKUP_DIRECT_DELETE_NEGATIVE",
        "GDL-IMG-015": "CLEAR_AND_DESTRUCTION",
        "GDL-CREF-001": "FALSE_LEAD",
    }
    for key, topic in expected_topics.items():
        if gdl[key]["topic"] != topic:
            raise RuntimeError(f"canonical GDL selector drift: {key}")


def verify_static_anchors(image: bytes, sections: Sequence[Section]) -> dict[str, object]:
    for name in SPANS:
        span_bytes(image, sections, name)

    type_name_off = va_to_offset(sections, 0x0101C220)
    if read_cstring(image, type_name_off) != ".?AVDropThingGameObj@@":
        raise RuntimeError("DropThingGameObj TypeDescriptor name drift")
    expect_call(image, sections, 0x00BF0391, 0x00B023E0)
    expect_call(image, sections, 0x00BF039C, 0x0088F2E0)
    expect_dwords(
        image,
        sections,
        0x00F30FAC,
        (
            0x005F4B90,
            0x005F5170,
            0x00401B20,
            0x009F17E0,
            0x008F7730,
            0x005F4AF0,
            0x00B1C8C0,
            0x005F4110,
            0x00B1D310,
            0x00B02400,
            0x00B024F0,
            0x0073D360,
        ),
    )
    expect_call(image, sections, 0x006B0453, 0x005F4B90)
    expect_call(image, sections, 0x006B0459, 0x0088F2B0)

    expect_call(image, sections, 0x006B0639, 0x005E8F90)
    expect_call(image, sections, 0x006B064C, 0x004011A0)
    expect_call(image, sections, 0x006B0653, 0x005DD800)
    pickup_calls = raw_e8_lines(image, sections, "pickup_emit")
    if len(pickup_calls) != 3 or digest_lines(pickup_calls) != "cf7b8fe30d9c125659ccb63a7c47d5f0c020b0327c40abe9d978c6ed0a874b4a":
        raise RuntimeError("pickup successful-subpath direct-call census drift")
    delete_targets = {0x00B0EE40, 0x005E0D40, 0x005E0560}
    if {int(line.rsplit("0x", 1)[1], 16) for line in pickup_calls}.intersection(delete_targets):
        raise RuntimeError("pickup successful subpath acquired a direct delete edge")

    expect_call(image, sections, 0x005F40AA, 0x005F38F0)
    for site in (0x00C3A0CC, 0x00C3A0DB, 0x00C3A0EA):
        expect_call(image, sections, site, 0x0089A600)
    expect_call(image, sections, 0x00A8CC77, 0x00C3A0A0)
    expect_call(image, sections, 0x00A8CC83, 0x00A8C8D0)
    expect_call(image, sections, 0x00A8CC9C, 0x00A8CB30)
    expect_call(image, sections, 0x00A8C924, 0x00B743B0)
    expect_call(image, sections, 0x00A8CBDB, 0x00B378E6)
    expect_bytes(image, sections, 0x00B378E6, "ff2574bac300")
    expect_bytes(image, sections, 0x00A8CB56, "81fff83f0000")
    expect_bytes(image, sections, 0x00A8CB86, "81caac3e255f")

    calls_expected = {
        "serialize_driver": (5, "55d7340e9dd9acc31622048fd5c0c68cf40751204a7ae51d0eef2094ba76482b"),
        "transform_repack": (4, "1e28831c992a264564accd06ec124e8ed4bdd0741060d909bfa8c01b2e9a6ee3"),
        "chunk_send": (8, "3080200f326f3be970a4856eab05cc0a3f9e3b8bfd348cb539b65bba32d2598c"),
    }
    call_census: dict[str, list[str]] = {}
    for name, (count, digest) in calls_expected.items():
        lines = raw_e8_lines(image, sections, name)
        if len(lines) != count or digest_lines(lines) != digest:
            raise RuntimeError(f"transport call census drift: {name}")
        call_census[name] = lines

    imports = resolve_imports(image, sections)
    if imports.get(0x00C3BA74) != ("ws2_32.dll", "ordinal_19"):
        raise RuntimeError("IAT 0x00C3BA74 is not WS2_32.dll ordinal 19 (send)")
    return {"pickup_calls": pickup_calls, "call_census": call_census}


def load_validator():
    read_pinned(VALIDATOR_PATH, *INPUT_PINS[VALIDATOR_PATH])
    spec = importlib.util.spec_from_file_location("pf_ground_drop_capture_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned capture validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    prior_dont_write_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior_dont_write_bytecode
    return module


def capture_manifest(records: Sequence[tuple[str, int, str]]) -> str:
    text = "\n".join(f"{rel}\t{size}\t{file_sha}" for rel, size, file_sha in records)
    return sha256(text.encode("utf-8"))


def has_capture_v_prefix_path(relative_path: str) -> bool:
    return any(part.casefold().startswith("capture_v") for part in Path(relative_path).parts)


def verify_frozen_validation(validator) -> None:
    inventory_rows = [
        row for row in validator.read_tsv(INVENTORY_PATH) if row.get("source") == SOURCE_CAPTURE
    ]
    if len(inventory_rows) != FROZEN_CAPTURE_FILES:
        raise RuntimeError("frozen capture inventory row count drift")
    if sum(int(row["size"]) for row in inventory_rows) != FROZEN_CAPTURE_BYTES:
        raise RuntimeError("frozen capture inventory byte count drift")

    rows = validator.read_tsv(FIELD_VALIDATION_PATH)
    keyed = {(row["message"], row["direction(W/R)"]): row for row in rows}
    expected = {
        ("GSCN_RunTimeProtocolReq", "W"): (40_747, 126),
        ("GSCN_RunTimeProtocolRes", "R"): (10_073, 134),
    }
    for key, (frames, files) in expected.items():
        row = keyed.get(key)
        if row is None or int(row["observed_frames"]) != frames or int(row["capture_file_count"]) != files:
            raise RuntimeError(f"frozen PF_FIELD_VALIDATION selector drift: {key}")


def parse_closed_nested_tail(
    data: bytes,
    direction: str,
    id_to_name: Mapping[int, str],
    schemas,
    static_open: set[str],
) -> tuple[int | None, int, int, int]:
    """Return tail position, declared, reached, and PickupTerrainThing reached."""
    if len(data) < 12 or data[0] != 0x12 or data[3] != 0x14 or data[8] != 0x08 or data[10] != 0x0B:
        raise RuntimeError("tail census encountered invalid outer base")
    outer_mask = data[11]
    if outer_mask not in (0x00, 0x02):
        raise RuntimeError(f"tail census outer mask drift: 0x{outer_mask:02X}")
    if outer_mask == 0:
        return 12, 0, 0, 0
    if len(data) < 15 or data[12] != 0x12:
        raise RuntimeError("tail census vital-count structure drift")
    declared = int.from_bytes(data[13:15], "little")
    position = 15
    reached = 0
    pickup_reached = 0
    for _index in range(declared):
        if position + 5 > len(data) or data[position] != 0x12 or data[position + 3] != 0x0B:
            return None, declared, reached, pickup_reached
        vital_id = int.from_bytes(data[position + 1 : position + 3], "little")
        vital_name = id_to_name.get(vital_id)
        if vital_name is None:
            return None, declared, reached, pickup_reached
        position += 5
        reached += 1
        if vital_name == "PickupTerrainThing":
            pickup_reached += 1
        result = validator_parse_schema(data, position, schemas[(vital_name, direction)], vital_name in static_open)
        if result.status != "PASS":
            return None, declared, reached, pickup_reached
        position = result.end
    return position, declared, reached, pickup_reached


_VALIDATOR_FOR_TAIL = None


def validator_parse_schema(data: bytes, position: int, schema, is_static_open: bool):
    if _VALIDATOR_FOR_TAIL is None:
        raise RuntimeError("tail validator not installed")
    return _VALIDATOR_FOR_TAIL.parse_schema(data, position, schema, is_static_open)


def consume_tagged(data: bytes, position: int, tag: int, length: int) -> tuple[bytes, int]:
    end = position + 1 + length
    if end > len(data) or data[position] != tag:
        raise RuntimeError("TerrainThingPool tagged-field structure drift")
    return data[position + 1 : end], end


def parse_terrain_pool(data: bytes, position: int) -> tuple[tuple[int, ...], int]:
    raw_count, position = consume_tagged(data, position, 0x12, 2)
    count = int.from_bytes(raw_count, "little")
    keys: list[int] = []
    for _index in range(count):
        raw_key, position = consume_tagged(data, position, 0x14, 4)
        keys.append(int.from_bytes(raw_key, "little"))
        raw_mask, position = consume_tagged(data, position, 0x0B, 1)
        mask = raw_mask[0]
        if mask & ~0x3E:
            raise RuntimeError("TerrainThing record acquired unknown mask bit")
        optional = (
            (0x02, ((0x14, 4),)),
            (0x04, ((0x0F, 2),)),
            (0x08, ((0x05, 1),)),
            (0x10, ((0x2A, 4), (0x2A, 4), (0x2A, 4))),
            (0x20, ((0x08, 1),)),
        )
        for bit, fields in optional:
            if not mask & bit:
                continue
            for tag, length in fields:
                _raw, position = consume_tagged(data, position, tag, length)
    if len(set(keys)) != len(keys):
        raise RuntimeError("TerrainThingPool contains duplicate runtime keys")
    return tuple(sorted(keys)), position


def parse_terrain_pool_exact(data: bytes, position: int) -> tuple[int, ...]:
    keys, end = parse_terrain_pool(data, position)
    if end != len(data):
        raise RuntimeError("confirmed TerrainThingPool did not consume exact frame tail")
    return keys


def derive_tail_census(
    validator,
    fresh: Mapping[str, Path],
    file_shas: Mapping[str, str],
    id_to_name: Mapping[int, str],
    schemas,
    static_open: set[str],
) -> TailCensus:
    global _VALIDATOR_FOR_TAIL
    _VALIDATOR_FOR_TAIL = validator
    runtime_res_id = validator.protocol_id("GSCN_RunTimeProtocolRes")
    gameplay_req_id = validator.protocol_id("GSCN_RunTimeProtocolReq")
    login_id = validator.protocol_id("GSCN_LoginProtocol")
    if (runtime_res_id, gameplay_req_id, login_id) != (0x6E9D, 0x6E6F, 0x453A):
        raise RuntimeError("runtime outer discriminator formula drift")

    absent = count_zero = nonempty = uncertain = truncated = 0
    pool_count_one = pool_count_two = 0
    outer00_absent = outer00_nonempty = 0
    outer02_absent = outer02_uncertain = 0
    event_lines: list[str] = []
    uncertain_lines: list[str] = []
    truncated_locators: list[tuple[str, str, int, str]] = []
    nonempty_files: set[str] = set()
    unique_frame_hashes: set[str] = set()
    sequence_events: dict[str, list[tuple[int, str, frozenset[int] | None]]] = defaultdict(list)
    c2s_outer = c2s_gameplay = c2s_login = c2s_no_nested = 0
    c2s_declared = c2s_reached = c2s_pickup = 0

    for key, path in sorted(fresh.items()):
        if path.suffix.casefold() != ".txt":
            continue
        rel = path.relative_to(GAME_CLIENT_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = validator.extract_pc_blocks(text)
        if errors:
            raise RuntimeError(f"tail census block extraction drift: {rel}")
        for ordinal, (kind, data) in enumerate(blocks, 1):
            if len(data) < 3 or data[0] != 0x12:
                continue
            outer_id = int.from_bytes(data[1:3], "little")
            if kind == "DECOMPRESSED" and outer_id in (gameplay_req_id, login_id):
                c2s_outer += 1
                if outer_id == gameplay_req_id:
                    c2s_gameplay += 1
                else:
                    c2s_login += 1
                _tail, declared, reached, pickup_reached = parse_closed_nested_tail(
                    data, "W", id_to_name, schemas, static_open
                )
                if data[11] == 0:
                    c2s_no_nested += 1
                c2s_declared += declared
                c2s_reached += reached
                c2s_pickup += pickup_reached
                if not has_capture_v_prefix_path(rel):
                    raise RuntimeError(f"C2S outer path lacks capture_v* classification component: {rel}")
                continue
            if kind != "PC" or outer_id != runtime_res_id:
                continue

            frame_sha = sha256(data)
            tail, _declared, _reached, _pickup = parse_closed_nested_tail(
                data, "R", id_to_name, schemas, static_open
            )
            if tail is None:
                uncertain += 1
                if data[11] == 0:
                    raise RuntimeError("outer-mask 0 unexpectedly has an uncertain tail")
                outer02_uncertain += 1
                sequence_events[rel].append((ordinal, "UNCERTAIN", None))
                uncertain_lines.append(
                    f"{rel}\t{file_shas[key]}\t{ordinal}\t{frame_sha}\tSTATIC_OPEN_OR_UNREACHED_TAIL"
                )
                continue
            if tail + 2 > len(data) or data[tail] != 0x0B:
                uncertain += 1
                truncated += 1
                if data[11] == 0:
                    raise RuntimeError("outer-mask 0 unexpectedly has a truncated derived mask")
                outer02_uncertain += 1
                sequence_events[rel].append((ordinal, "UNCERTAIN", None))
                uncertain_lines.append(
                    f"{rel}\t{file_shas[key]}\t{ordinal}\t{frame_sha}\tTRUNCATED_DERIVED_MASK"
                )
                truncated_locators.append((rel, file_shas[key], ordinal, frame_sha))
                continue
            derived_mask = data[tail + 1]
            if derived_mask & ~0x0F:
                uncertain += 1
                if data[11] == 0:
                    raise RuntimeError("outer-mask 0 acquired unknown derived-mask bits")
                outer02_uncertain += 1
                sequence_events[rel].append((ordinal, "UNCERTAIN", None))
                uncertain_lines.append(
                    f"{rel}\t{file_shas[key]}\t{ordinal}\t{frame_sha}\tUNKNOWN_DERIVED_FIELD"
                )
                continue
            if not derived_mask & 0x08:
                absent += 1
                if data[11] == 0:
                    outer00_absent += 1
                else:
                    outer02_absent += 1
                sequence_events[rel].append((ordinal, "ABSENT", frozenset()))
                continue
            if derived_mask & 0x07:
                uncertain += 1
                if data[11] == 0:
                    raise RuntimeError("outer-mask 0 acquired earlier derived fields before pool")
                outer02_uncertain += 1
                sequence_events[rel].append((ordinal, "UNCERTAIN", None))
                uncertain_lines.append(
                    f"{rel}\t{file_shas[key]}\t{ordinal}\t{frame_sha}\tEARLIER_OR_UNKNOWN_DERIVED_FIELD"
                )
                continue
            keys = parse_terrain_pool_exact(data, tail + 2)
            if not keys:
                count_zero += 1
                sequence_events[rel].append((ordinal, "COUNT_ZERO", frozenset()))
                continue
            nonempty += 1
            if data[11] == 0:
                outer00_nonempty += 1
            else:
                raise RuntimeError("confirmed nonempty TerrainThingPool unexpectedly followed outer-mask 2")
            if len(keys) == 1:
                pool_count_one += 1
            elif len(keys) == 2:
                pool_count_two += 1
            else:
                raise RuntimeError("confirmed nonempty pool record-count drift")
            if not has_capture_v_prefix_path(rel):
                raise RuntimeError("confirmed nonempty pool path lacks capture_v* component")
            key_bytes = b"".join(struct.pack("<I", value) for value in keys)
            keyset_sha = sha256(key_bytes)
            line = (
                f"{rel}\t{file_shas[key]}\t{ordinal}\t{frame_sha}\t{PATH_CAPTURE_V_CLASS}\t"
                f"{len(keys)}\t{keyset_sha}"
            )
            event_lines.append(line)
            nonempty_files.add(rel)
            unique_frame_hashes.add(frame_sha)
            sequence_events[rel].append((ordinal, "NONEMPTY", frozenset(keys)))

    event_manifest = sha256(("\n".join(sorted(event_lines)) + "\n").encode("utf-8"))
    uncertain_manifest = sha256(("\n".join(sorted(uncertain_lines)) + "\n").encode("utf-8"))
    if tuple(sorted(truncated_locators)) != tuple(sorted(TRUNCATED_DERIVED_MASK_LOCATORS)):
        raise RuntimeError("truncated derived-mask locator set drift")
    sequence_add = sequence_add_omit = sequence_same = swaps = 0
    for file_events in sequence_events.values():
        previous: frozenset[int] = frozenset()
        known = True
        for _ordinal, event_kind, current in sorted(file_events):
            if event_kind == "UNCERTAIN":
                known = False
                continue
            if event_kind == "ABSENT":
                previous = frozenset()
                known = True
                continue
            if event_kind == "COUNT_ZERO":
                continue
            if event_kind != "NONEMPTY" or current is None:
                raise RuntimeError("unknown tail sequence event")
            if not known:
                raise RuntimeError("nonempty event follows uncertain state without reset")
            added = current - previous
            omitted = previous - current
            if current == previous:
                sequence_same += 1
            elif added and omitted:
                sequence_add_omit += 1
                if len(current) == len(previous) == 1:
                    swaps += 1
            elif added:
                sequence_add += 1
            else:
                raise RuntimeError("nonempty sequence contains omit-only transition")
            previous = current

    expected = (
        absent,
        count_zero,
        nonempty,
        uncertain,
        truncated,
        len(nonempty_files),
        len(unique_frame_hashes),
        event_manifest,
        uncertain_manifest,
        pool_count_one,
        pool_count_two,
        outer00_absent,
        outer00_nonempty,
        outer02_absent,
        outer02_uncertain,
        sequence_add,
        sequence_add_omit,
        sequence_same,
        swaps,
        c2s_outer,
        c2s_gameplay,
        c2s_login,
        c2s_no_nested,
        c2s_declared,
        c2s_reached,
        c2s_declared - c2s_reached,
        c2s_pickup,
    )
    required = (
        14_536,
        0,
        23,
        729,
        3,
        11,
        19,
        TAIL_EVENT_MANIFEST,
        ALL_UNRESOLVED_LOCATOR_MANIFEST,
        22,
        1,
        602,
        23,
        13_934,
        729,
        13,
        10,
        0,
        10,
        65_610,
        64_979,
        631,
        58_412,
        15_350,
        14_615,
        735,
        0,
    )
    if expected != required:
        raise RuntimeError(f"current ground-tail census drift: {expected}")
    return TailCensus(
        absent=absent,
        count_zero=count_zero,
        nonempty=nonempty,
        uncertain=uncertain,
        truncated_mask=truncated,
        nonempty_files=len(nonempty_files),
        unique_frames=len(unique_frame_hashes),
        event_manifest=event_manifest,
        uncertain_manifest=uncertain_manifest,
        pool_count_one=pool_count_one,
        pool_count_two=pool_count_two,
        outer00_absent=outer00_absent,
        outer00_nonempty=outer00_nonempty,
        outer02_absent=outer02_absent,
        outer02_uncertain=outer02_uncertain,
        sequence_add=sequence_add,
        sequence_add_omit=sequence_add_omit,
        sequence_same_set=sequence_same,
        one_entry_swaps=swaps,
        c2s_outer_blocks=c2s_outer,
        c2s_gameplay_outer_blocks=c2s_gameplay,
        c2s_login_outer_blocks=c2s_login,
        c2s_no_nested_blocks=c2s_no_nested,
        c2s_nested_declared=c2s_declared,
        c2s_nested_reached=c2s_reached,
        c2s_nested_fail_closed=c2s_declared - c2s_reached,
        c2s_pickup_reached=c2s_pickup,
    )


def derive_capture_facts(validator) -> CaptureFacts:
    registry_rows = validator.read_tsv(REGISTRY_PATH)
    field_rows = validator.read_tsv(FIELDS_PATH)
    tag_rows = validator.read_tsv(TAG_PATH)
    id_to_name, schemas, static_open = validator.build_schemas(registry_rows, field_rows, tag_rows)

    fresh = validator.enumerate_capture_paths(GAME_CLIENT_ROOT)
    pre_state = {
        key: (
            path.relative_to(GAME_CLIENT_ROOT).as_posix(),
            path.stat().st_size,
            path.stat().st_mtime_ns,
        )
        for key, path in fresh.items()
    }
    records: list[tuple[str, int, str]] = []
    file_shas: dict[str, str] = {}
    for key, path in sorted(fresh.items()):
        rel = path.relative_to(GAME_CLIENT_ROOT).as_posix()
        file_sha = sha256_file(path)
        file_shas[key] = file_sha
        records.append((rel, path.stat().st_size, file_sha))
    file_count = len(records)
    byte_count = sum(size for _rel, size, _sha in records)
    manifest = capture_manifest(records)
    if (file_count, byte_count, manifest) != (
        CURRENT_CAPTURE_FILES,
        CURRENT_CAPTURE_BYTES,
        CURRENT_CAPTURE_MANIFEST,
    ):
        raise RuntimeError(
            f"current capture manifest drift: files={file_count} bytes={byte_count} sha256={manifest}"
        )

    aggregates = defaultdict(validator.MessageAggregate)
    counts = validator.RunCounts()
    for _key, path in sorted(fresh.items()):
        if path.suffix.casefold() != ".txt":
            continue
        counts.capture_text_files += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = validator.extract_pc_blocks(text)
        counts.block_errors.update(errors)
        rel = path.relative_to(GAME_CLIENT_ROOT).as_posix()
        if blocks:
            counts.files_with_blocks.add(rel)
        for ordinal, (kind, data) in enumerate(blocks, 1):
            if kind == "PC":
                direction = "R"
                counts.pc_blocks += 1
            else:
                direction = "W"
                counts.decompressed_blocks += 1
            validator.parse_capture_frame(
                data,
                direction,
                f"{rel}:{ordinal}",
                rel,
                id_to_name,
                schemas,
                static_open,
                aggregates,
                counts,
            )

    blocks = counts.pc_blocks + counts.decompressed_blocks
    if (
        counts.capture_text_files != CURRENT_TEXT_FILES
        or blocks != CURRENT_BLOCKS
        or counts.nested_declared_instances != CURRENT_NESTED_DECLARED
        or counts.nested_reached_instances != CURRENT_NESTED_REACHED
        or counts.unknown_message_id_instances != 0
        or sum(counts.block_errors.values()) != 0
    ):
        raise RuntimeError("current capture parse census drift")

    target_stats: dict[tuple[str, str], tuple[int, int, int]] = {}
    for name in TARGET_NAMES + ("GSCN_RunTimeProtocolReq", "GSCN_RunTimeProtocolRes"):
        for direction in ("W", "R"):
            aggregate = aggregates[(name, direction)]
            target_stats[(name, direction)] = (
                len(aggregate.observed_frames),
                aggregate.observed_instances,
                len(aggregate.capture_files),
            )
    for name in TARGET_NAMES:
        if target_stats[(name, "W")] != (0, 0, 0) or target_stats[(name, "R")] != (0, 0, 0):
            raise RuntimeError(f"target-family capture zero census drift: {name}")
    if target_stats[("GSCN_RunTimeProtocolReq", "W")] != (64_979, 64_979, 195):
        raise RuntimeError("current RuntimeProtocolReq W census drift")
    if target_stats[("GSCN_RunTimeProtocolReq", "R")] != (0, 0, 0):
        raise RuntimeError("current RuntimeProtocolReq R census drift")
    if target_stats[("GSCN_RunTimeProtocolRes", "R")] != (15_288, 15_288, 206):
        raise RuntimeError("current RuntimeProtocolRes R census drift")
    if target_stats[("GSCN_RunTimeProtocolRes", "W")] != (0, 0, 0):
        raise RuntimeError("current RuntimeProtocolRes W census drift")

    tail = derive_tail_census(
        validator, fresh, file_shas, id_to_name, schemas, static_open
    )

    fresh_after = validator.enumerate_capture_paths(GAME_CLIENT_ROOT)
    post_state = {
        key: (
            path.relative_to(GAME_CLIENT_ROOT).as_posix(),
            path.stat().st_size,
            path.stat().st_mtime_ns,
        )
        for key, path in fresh_after.items()
    }
    if pre_state != post_state:
        raise RuntimeError("capture path/size/mtime snapshot changed during read-only census")

    return CaptureFacts(
        file_count=file_count,
        byte_count=byte_count,
        manifest_sha256=manifest,
        text_files=counts.capture_text_files,
        blocks=blocks,
        nested_declared=counts.nested_declared_instances,
        nested_reached=counts.nested_reached_instances,
        target_stats=target_stats,
        runtime_res_absent=tail.absent,
        runtime_res_count_zero=tail.count_zero,
        runtime_res_nonempty=tail.nonempty,
        runtime_res_uncertain=tail.uncertain,
        runtime_res_truncated_mask=tail.truncated_mask,
        runtime_res_nonempty_files=tail.nonempty_files,
        runtime_res_unique_frames=tail.unique_frames,
        runtime_res_event_manifest=tail.event_manifest,
        runtime_res_uncertain_manifest=tail.uncertain_manifest,
        runtime_res_pool_count_one=tail.pool_count_one,
        runtime_res_pool_count_two=tail.pool_count_two,
        runtime_res_outer00_absent=tail.outer00_absent,
        runtime_res_outer00_nonempty=tail.outer00_nonempty,
        runtime_res_outer02_absent=tail.outer02_absent,
        runtime_res_outer02_uncertain=tail.outer02_uncertain,
        runtime_res_sequence_add=tail.sequence_add,
        runtime_res_sequence_add_omit=tail.sequence_add_omit,
        runtime_res_sequence_same_set=tail.sequence_same_set,
        runtime_res_one_entry_swaps=tail.one_entry_swaps,
        c2s_outer_blocks=tail.c2s_outer_blocks,
        c2s_gameplay_outer_blocks=tail.c2s_gameplay_outer_blocks,
        c2s_login_outer_blocks=tail.c2s_login_outer_blocks,
        c2s_no_nested_blocks=tail.c2s_no_nested_blocks,
        c2s_nested_declared=tail.c2s_nested_declared,
        c2s_nested_reached=tail.c2s_nested_reached,
        c2s_nested_fail_closed=tail.c2s_nested_fail_closed,
        c2s_pickup_reached=tail.c2s_pickup_reached,
    )


def capture_validation_prior(validator) -> PriorClaim:
    rows = validator.read_tsv(FIELD_VALIDATION_PATH)
    wanted = {
        ("GSCN_RunTimeProtocolReq", "W"),
        ("GSCN_RunTimeProtocolRes", "R"),
        *((name, direction) for name in TARGET_NAMES for direction in ("W", "R")),
    }
    selected = [
        row
        for row in rows
        if (row.get("message"), row.get("direction(W/R)")) in wanted
    ]
    if len(selected) != len(wanted) or any(row.get("source") != SOURCE_CAPTURE for row in selected):
        raise RuntimeError("frozen PF_FIELD_VALIDATION reference selection drift")
    ordered = sorted(selected, key=lambda row: (row["message"], row["direction(W/R)"]))
    digest = sha256(
        json.dumps(ordered, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    )
    selector = ",".join(f"{row['message']}:{row['direction(W/R)']}" for row in ordered)
    return PriorClaim(
        token=f"{FIELD_VALIDATION_PATH.name}:{selector}",
        artifact_sha256=INPUT_PINS[FIELD_VALIDATION_PATH][1],
        claim_digest=digest,
    )


def make_image_row(
    image: bytes,
    sections: Sequence[Section],
    *,
    closure_id: str,
    row_kind: str,
    phase: str,
    subject: str,
    direction: str,
    semantic_status: str,
    exact_observation: str,
    value_or_layout: str,
    evidence_mode: str,
    primary_span: str | None,
    support_spans: Sequence[str],
    direct_assertions: Sequence[str],
    prior_claims: Sequence[PriorClaim],
    nonclaim: str,
    blocker: str,
    required_next_evidence: str,
) -> dict[str, str]:
    if primary_span is None:
        start_va = end_va = start_off = end_off = span_sha = "N/A_CANONICAL_REFERENCE"
    else:
        _raw, start, end = span_bytes(image, sections, primary_span)
        spec = SPANS[primary_span]
        start_va = f"0x{spec.start:08X}"
        end_va = f"0x{spec.end:08X}"
        start_off = f"0x{start:08X}"
        end_off = f"0x{end:08X}"
        span_sha = spec.sha256
    prior_reference, prior_artifact, prior_digest = join_prior(prior_claims)
    row = {
        "closure_id": closure_id,
        "row_kind": row_kind,
        "phase": phase,
        "subject": subject,
        "direction": direction,
        "semantic_status": semantic_status,
        "exact_observation": exact_observation,
        "value_or_layout": value_or_layout,
        "evidence_mode": evidence_mode,
        "span_start_va": start_va,
        "span_end_va": end_va,
        "file_off_start": start_off,
        "file_off_end": end_off,
        "span_sha256": span_sha,
        "support_spans": ";".join(format_span(image, sections, name) for name in support_spans) if support_spans else "N/A",
        "direct_assertions": "||".join(direct_assertions) if direct_assertions else "N/A",
        "prior_reference": prior_reference,
        "prior_artifact_sha256": prior_artifact,
        "prior_claim_digest": prior_digest,
        "capture_file_count": "N/A",
        "capture_total_bytes": "N/A",
        "capture_manifest_sha256": "N/A",
        "capture_text_file_count": "N/A",
        "capture_block_count": "N/A",
        "source": SOURCE_IMAGE,
        "provenance": "ORIGINAL_IMAGE",
        "source_file": IMAGE_SOURCE_FILE,
        "source_size": str(IMAGE_SIZE),
        "source_sha256": IMAGE_SHA256,
        "nonclaim": nonclaim,
        "blocker": blocker,
        "required_next_evidence": "PROPOSED: " + required_next_evidence,
        "claim_sha256": "",
        "evidence_key": "",
    }
    row["claim_sha256"] = canonical_digest({key: value for key, value in row.items() if key not in {"claim_sha256", "evidence_key"}})
    row["evidence_key"] = sha256(
        ROW_DOMAIN
        + row["claim_sha256"].encode("ascii")
        + b"\x00"
        + row["span_sha256"].encode("ascii")
        + b"\x00"
        + IMAGE_SHA256.encode("ascii")
    )
    return row


def make_capture_row(
    facts: CaptureFacts,
    *,
    closure_id: str,
    row_kind: str,
    phase: str,
    subject: str,
    direction: str,
    semantic_status: str,
    exact_observation: str,
    value_or_layout: str,
    evidence_mode: str,
    provenance: str,
    prior_claims: Sequence[PriorClaim],
    nonclaim: str,
    blocker: str,
    required_next_evidence: str,
) -> dict[str, str]:
    prior_reference, prior_artifact, prior_digest = join_prior(prior_claims)
    row = {
        "closure_id": closure_id,
        "row_kind": row_kind,
        "phase": phase,
        "subject": subject,
        "direction": direction,
        "semantic_status": semantic_status,
        "exact_observation": exact_observation,
        "value_or_layout": value_or_layout,
        "evidence_mode": evidence_mode,
        "span_start_va": "N/A_CAPTURE_METADATA_ONLY",
        "span_end_va": "N/A_CAPTURE_METADATA_ONLY",
        "file_off_start": "N/A_CAPTURE_METADATA_ONLY",
        "file_off_end": "N/A_CAPTURE_METADATA_ONLY",
        "span_sha256": "N/A_CAPTURE_METADATA_ONLY",
        "support_spans": "N/A_CAPTURE_METADATA_ONLY",
        "direct_assertions": "N/A_CAPTURE_METADATA_ONLY",
        "prior_reference": prior_reference,
        "prior_artifact_sha256": prior_artifact,
        "prior_claim_digest": prior_digest,
        "capture_file_count": str(facts.file_count),
        "capture_total_bytes": str(facts.byte_count),
        "capture_manifest_sha256": facts.manifest_sha256,
        "capture_text_file_count": str(facts.text_files),
        "capture_block_count": str(facts.blocks),
        "source": SOURCE_CAPTURE,
        "provenance": provenance,
        "source_file": CAPTURE_SOURCE_FILE,
        "source_size": str(facts.byte_count),
        "source_sha256": facts.manifest_sha256,
        "nonclaim": nonclaim,
        "blocker": blocker,
        "required_next_evidence": "PROPOSED: " + required_next_evidence,
        "claim_sha256": "",
        "evidence_key": "",
    }
    row["claim_sha256"] = canonical_digest({key: value for key, value in row.items() if key not in {"claim_sha256", "evidence_key"}})
    row["evidence_key"] = sha256(
        ROW_DOMAIN
        + row["claim_sha256"].encode("ascii")
        + b"\x00"
        + facts.manifest_sha256.encode("ascii")
    )
    return row


def build_rows(
    image: bytes,
    sections: Sequence[Section],
    static: Mapping[str, object],
    facts: CaptureFacts,
    prior: Mapping[str, PriorClaim],
    frozen_prior: PriorClaim,
) -> list[dict[str, str]]:
    pickup_calls = tuple(static["pickup_calls"])
    rows = [
        make_image_row(
            image,
            sections,
            closure_id="GDP-IMG-001",
            row_kind="TYPED_OBJECT_GATE",
            phase="PICKUP_CLICK",
            subject="DropThingGameObj is-a gate",
            direction="LOCAL",
            semantic_status="PROVEN_EXACT_CONDITIONAL",
            exact_observation=(
                "The static initializer binds MSVC TypeDescriptor .?AVDropThingGameObj@@ at 0x0101C218 "
                "to custom descriptor 0x010823E8. DropThingGameObj vtable slot +0x00 returns that descriptor. "
                "The click path obtains the clicked object's descriptor and 0x0088F2B0 walks descriptor +0x04 "
                "parents against 0x010823E8; only a successful is-a result retains the object pointer."
            ),
            value_or_layout="TypeDescriptor=0x0101C218;custom_descriptor=0x010823E8;vtable=0x00F30FAC;is_a=0x0088F2B0",
            evidence_mode="NEW_IMAGE_EVIDENCE",
            primary_span="click_type_gate",
            support_spans=("descriptor_init", "type_descriptor", "dropobj_vtable", "type_getter", "type_chain_helper"),
            direct_assertions=("0x006B0453->0x005F4B90", "0x006B0459->0x0088F2B0"),
            prior_claims=(),
            nonclaim="The is-a walk accepts a derived class whose descriptor parent chain reaches DropThingGameObj; this row does not require exact dynamic-class equality.",
            blocker="NONE_FOR_BOUNDED_STATIC_CLAIM",
            required_next_evidence="Same-build runtime observation only if the dynamic class of a particular click must be identified.",
        ),
        make_image_row(
            image,
            sections,
            closure_id="GDP-IMG-002",
            row_kind="TYPED_KEY_JOIN",
            phase="PICKUP_EMISSION",
            subject="TerrainThing runtime identity",
            direction="C2S",
            semantic_status="PROVEN_EXACT_CONDITIONAL",
            exact_observation=(
                "On the reached action/type/range/allocation-success subpath, the retained typed object supplies "
                "[DropThingGameObj+0x7C]->TerrainThing+0x10 and the client stores that exact u32 into "
                "PickupTerrainThing+0x14. Canonical GDL rows independently bind TerrainThing+0x10 as the "
                "DropThingModule_Client reconciliation/map key."
            ),
            value_or_layout="PickupTerrainThing+0x14 == [DropThingGameObj+0x7C]->TerrainThing+0x10 == reconciliation/map key",
            evidence_mode="NEW_IMAGE_JOIN_PLUS_CANONICAL_REFERENCES",
            primary_span="pickup_emit",
            support_spans=("dropobj_retain", "reconcile"),
            direct_assertions=pickup_calls,
            prior_claims=(prior["gdt_pickup_producer"], prior["gdl_pool_codec"], prior["gdl_owner"]),
            nonclaim=(
                "TerrainThing+0x10 is a runtime object identity, not a proved item-template ID. The equality is "
                "conditional on the reached click/type/range path and successful request allocation; a derived "
                "DropThingGameObj class is accepted by the preceding is-a gate."
            ),
            blocker="LIVE_SERVER_ACCEPTANCE_AND_RESULTING_REMOVAL_NOT_ESTABLISHED",
            required_next_evidence="Eligible original C2S pickup followed by authoritative S2C state change, preserving source separation.",
        ),
        make_image_row(
            image,
            sections,
            closure_id="GDP-IMG-003",
            row_kind="LOGICAL_NESTED_DISCRIMINATOR",
            phase="NESTED_SERIALIZATION",
            subject="PickupTerrainThing runtime type",
            direction="C2S",
            semantic_status="PROVEN_EXACT_STATIC_SUCCESS_PATH",
            exact_observation=(
                "The nested-list writer calls each nested object's vtable +0x10 GetId and writes that u16 with "
                "tag 0x12 before invoking vtable +0x18 serializer. With the canonical successful PickupTerrainThing "
                "ID assignment and getter, 0x4543 is the nested logical runtime discriminator."
            ),
            value_or_layout="nested_type_discriminator=0x4543;field_tag=0x12;width=2;payload_serializer=PickupTerrainThing vtable+0x18",
            evidence_mode="IMAGE_REFINEMENT_WITH_CANONICAL_ID_PIN",
            primary_span="nested_writer",
            support_spans=("pickup_getid",),
            direct_assertions=("0x005F3972->0x0089A600", "nested GetId=vtable+0x10", "nested serializer=vtable+0x18"),
            prior_claims=(prior["gdt_pickup_id"], prior["gdt_nested_writer"]),
            nonclaim="0x4543 is not established as a top-level semantic packet opcode and is not proved to survive the later buffer rewrite as a literal socket byte sequence.",
            blocker="FINAL_SOCKET_LITERAL_AND_ORIGINAL_WIRE_OCCURRENCE_OPEN",
            required_next_evidence="Eligible original wire observation tied to the same logical object if literal final-wire occurrence is required.",
        ),
        make_image_row(
            image,
            sections,
            closure_id="GDP-IMG-004",
            row_kind="LOGICAL_OUTER_DISCRIMINATOR",
            phase="OUTER_SERIALIZATION",
            subject="gameplay versus login outer protocol",
            direction="C2S",
            semantic_status="PROVEN_EXACT_STATIC_SUCCESS_PATH",
            exact_observation=(
                "The outer writer calls vtable +0x10 GetId, writes the returned u16 with tag 0x12, writes the "
                "remaining outer fields, then calls vtable +0x18 serializer. Canonical successful IDs therefore "
                "classify 0x6E6F as the gameplay GSCN_RunTimeProtocolReq logical outer discriminator; login uses "
                "the distinct GSCN_LoginProtocol logical outer discriminator 0x453A."
            ),
            value_or_layout="gameplay_outer=0x6E6F;login_outer=0x453A;outer_id_tag=0x12;width=2",
            evidence_mode="IMAGE_REFINEMENT_WITH_CANONICAL_ID_PINS",
            primary_span="outer_writer",
            support_spans=("gameplay_getid", "login_getid", "request_serializer"),
            direct_assertions=("0x00C3A0CC->0x0089A600", "0x00C3A0DB->0x0089A600", "0x00C3A0EA->0x0089A600", "0x005F40AA->0x005F38F0"),
            prior_claims=(prior["gdt_gameplay_outer"], prior["gdt_login_outer"], prior["gdt_transport"]),
            nonclaim="Neither 0x6E6F nor 0x453A is established as a final top-level semantic socket opcode or as an unchanged post-transform literal.",
            blocker="FINAL_SOCKET_LITERAL_AND_LIVE_PHASE_SELECTION_OPEN",
            required_next_evidence="Original wire evidence with phase and transform boundaries if final literal or live selection is required.",
        ),
        make_image_row(
            image,
            sections,
            closure_id="GDP-IMG-005",
            row_kind="SOCKET_TRANSPORT_EXTENSION",
            phase="SERIALIZE_TRANSFORM_CHUNK_SEND",
            subject="logical outer object to WS2_32 send",
            direction="C2S",
            semantic_status="PROVEN_EXACT_STATIC_SOCKET_PATH",
            exact_observation=(
                "0x00A8CC30 calls logical writer 0x00C3A0A0, transform/repack 0x00A8C8D0, then chunk/send "
                "0x00A8CB30. The transform calls buffer-rewriter 0x00B743B0. The sender limits each payload chunk "
                "to at most 0x3FF8, and its flag-1 branch prepends eight transport bytes beginning with constant "
                "0x5F253EAC before thunk 0x00B378E6 jumps through IAT 0x00C3BA74 to the "
                "WS2_32.dll ordinal-19 `send` import."
            ),
            value_or_layout="0x00A8CC30->0x00A8C8D0->0x00A8CB30->0x00B378E6->IAT0x00C3BA74=WS2_32.dll.ordinal19(send);max_chunk=0x3FF8;flag1_prefix_magic=0x5F253EAC",
            evidence_mode="NEW_IMAGE_EVIDENCE",
            primary_span="serialize_driver",
            support_spans=("outer_writer", "transform_repack", "buffer_rewrite", "chunk_send", "send_thunk"),
            direct_assertions=(
                "0x00A8CC77->0x00C3A0A0",
                "0x00A8CC83->0x00A8C8D0",
                "0x00A8CC9C->0x00A8CB30",
                "0x00A8C924->0x00B743B0",
                "0x00A8CBDB->0x00B378E6",
                "0x00B378E6->IAT[0x00C3BA74]=WS2_32.dll ordinal19(send)",
            ),
            prior_claims=(prior["gdt_transport"],),
            nonclaim="0x5F253EAC is transport framing, not a semantic opcode. Because 0x00B743B0 rewrites the serialized buffer, this row does not claim that 0x4543, 0x6E6F, or 0x453A remain unchanged as final socket literals.",
            blocker="FINAL_SOCKET_BYTE_MAPPING_OPEN_AFTER_BUFFER_REWRITE",
            required_next_evidence="Source-separated original wire observation plus a proven transform decode if final literal mapping is needed.",
        ),
        make_image_row(
            image,
            sections,
            closure_id="GDP-IMG-006",
            row_kind="PICKUP_LOCAL_REMOVAL_NEGATIVE",
            phase="SUCCESSFUL_REQUEST_ALLOCATION_SUBPATH",
            subject="pickup request emission versus local ground-object deletion",
            direction="C2S",
            semantic_status="PROVEN_EXACT_BOUNDED_NEGATIVE",
            exact_observation=(
                "The reached allocation-success subpath 0x006B062D..0x006B0658 has exactly three direct E8 calls: "
                "request factory, wrapper/ownership helper, and nested enqueue. None targets the three pinned known "
                "unregister/map-delete functions. Successful request emission therefore performs no proved direct "
                "local unregister or module-map erase; a later authoritative S2C removal remains required/open."
            ),
            value_or_layout="direct_E8_count=3;forbidden_targets=0x00B0EE40,0x005E0D40,0x005E0560;matches=0",
            evidence_mode="NEW_NARROW_IMAGE_CENSUS_PLUS_CANONICAL_REFERENCE",
            primary_span="pickup_emit",
            support_spans=("full_click",),
            direct_assertions=pickup_calls,
            prior_claims=(prior["gdt_pickup_producer"], prior["gdl_pickup_negative"]),
            nonclaim="This bounded direct-call census does not exclude indirect, virtual, tail, helper, callback, server-driven, or later lifecycle removal; it does not prove server acceptance.",
            blocker="AUTHORITATIVE_POST_PICKUP_S2C_REMOVAL_CARRIER_OPEN",
            required_next_evidence="Original accepted pickup exchange with the following omission/full-clear/remove carrier and ordering.",
        ),
        make_image_row(
            image,
            sections,
            closure_id="GDP-IMG-007",
            row_kind="CANONICAL_COMPOSITION_REFERENCE",
            phase="REMOVAL_MATRIX",
            subject="DropThingModule_Client canonical disappearance predicates",
            direction="S2C_OR_LOCAL",
            semantic_status="CANONICAL_REFERENCE_SET_VERIFIED",
            exact_observation=(
                "This row content-addresses the existing GDL removal-matrix rows for NULL input, non-NULL empty "
                "input, nonempty omission, range pruning, and separate kind-0x0A clear/destruction. Their claims are "
                "not copied or reissued here."
            ),
            value_or_layout="selectors=GDL-IMG-007;GDL-IMG-008;GDL-IMG-009;GDL-IMG-010;GDL-IMG-015",
            evidence_mode="CANONICAL_COMPOSITION_ONLY",
            primary_span=None,
            support_spans=(),
            direct_assertions=(),
            prior_claims=(prior["gdl_null"], prior["gdl_empty"], prior["gdl_omission"], prior["gdl_range"], prior["gdl_clear"]),
            nonclaim="No new expiry policy, removal carrier, event name, or copied canonical IMAGE claim is introduced by this reference-only composition row.",
            blocker="ORIGINAL_SERVER_ISSUANCE_ORDER_EXPIRY_AND_POST_PICKUP_SELECTION_OPEN",
            required_next_evidence="Original source-separated S2C sequence selecting one canonical client predicate after pickup and at natural expiry.",
        ),
        make_image_row(
            image,
            sections,
            closure_id="GDP-IMG-008",
            row_kind="CANONICAL_FALSE_LEAD_REFERENCE",
            phase="TYPED_CARRIER_CLASSIFICATION",
            subject="FightingDropModule_Client and FightingDropNotify",
            direction="N/A",
            semantic_status="REFERENCE_ONLY_FALSE_LEAD_FOR_PROVED_TYPED_PATH",
            exact_observation=(
                "Content-addressed canonical rows classify FightingDropModule_Client and FightingDropNotify as "
                "custom-reflection surfaces that are not selected by the proved GSCN_RunTimeProtocolRes+0x20 "
                "TerrainThingPool typed path. No FightingDrop fact is reissued here."
            ),
            value_or_layout="selectors=GDT-IMG-008;GDT-IMG-009;GDL-CREF-001",
            evidence_mode="CANONICAL_REFERENCE_ONLY",
            primary_span=None,
            support_spans=(),
            direct_assertions=(),
            prior_claims=(prior["gdt_fighting_module"], prior["gdt_fighting_notify"], prior["gdl_false_lead"]),
            nonclaim="The reference rejects FightingDrop only for this exact typed carrier; it does not prove either class globally unused.",
            blocker="NONE_FOR_BOUNDED_FALSE_LEAD_CLASSIFICATION",
            required_next_evidence="A separately bound concrete FightingDrop wire getter/vtable/serializer or producer/receiver chain if global use must be established.",
        ),
        make_capture_row(
            facts,
            closure_id="GDP-CAP-001",
            row_kind="CURRENT_CORPUS_MANIFEST",
            phase="CAPTURE_CENSUS",
            subject="all capture_* files below GameClient",
            direction="MIXED",
            semantic_status="OBSERVED_EXACT_CURRENT_CORPUS_METADATA",
            exact_observation="The current read-only census contains 2,227 unique files totaling 699,015,496 bytes; 1,337 .txt files decoded as UTF-8 with replacement contain 81,954 validated PC/DECOMPRESSED blocks.",
            value_or_layout=(
                "manifest_sha256=b8284a566d9993f52540dea52e82896b0d8eb499b9aa83ceb74084a0e671db3c;"
                "sort=casefold_relative_path_key;record=original_case_posix_relpath<TAB>decimal_size<TAB>lowercase_file_sha256;"
                "join=LF_no_header_no_trailing_LF;encoding=UTF-8"
            ),
            evidence_mode="CAPTURE_METADATA_AND_PARSED_BLOCK_CENSUS",
            provenance="CURRENT_MIXED_CORPUS",
            prior_claims=(),
            nonclaim="The manifest includes all file types, but only .txt files are parsed. No capture payload or raw byte is emitted by this artifact.",
            blocker="NONE_FOR_CURRENT_CORPUS_CENSUS",
            required_next_evidence="Re-run only if the capture tree changes; any change is fail-closed manifest drift.",
        ),
        make_capture_row(
            facts,
            closure_id="GDP-CAP-002",
            row_kind="TARGET_FAMILY_ZERO_CENSUS",
            phase="GROUND_DROP_PICKUP_TARGETS",
            subject="PickupTerrainThing/DropThingModule_Client/FightingDrop*",
            direction="W_AND_R",
            semantic_status="NOT_OBSERVED_IN_CURRENT_CORPUS",
            exact_observation="PickupTerrainThing, DropThingModule_Client, FightingDropModule_Client, and FightingDropNotify each have W=0 frames/instances/files and R=0 frames/instances/files in the current parsed corpus.",
            value_or_layout="four_target_names*two_directions=8 zero cells",
            evidence_mode="CAPTURE_PARSED_LOGICAL_MESSAGE_CENSUS",
            provenance="CURRENT_MIXED_CORPUS",
            prior_claims=(),
            nonclaim="Zero named instances does not prove the logical object can never appear; it records only this exact current corpus and cannot resolve objects hidden inside A2-static-open outer frames.",
            blocker="NO_ELIGIBLE_NAMED_PICKUP_OR_REMOVAL_INSTANCE",
            required_next_evidence="Original same-build capture containing a typed pickup and the following ground-state response.",
        ),
        make_capture_row(
            facts,
            closure_id="GDP-CAP-003",
            row_kind="OUTER_TRAFFIC_CENSUS",
            phase="RUNTIME_PROTOCOL_OUTERS",
            subject="GSCN_RunTimeProtocolReq/Res",
            direction="C2S_AND_S2C",
            semantic_status="OBSERVED_OUTER_ONLY_A2_STATIC_OPEN",
            exact_observation="Current corpus observes GSCN_RunTimeProtocolReq W=64,979 frames/instances in 195 files and GSCN_RunTimeProtocolRes R=15,288 frames/instances in 206 files; opposite directions are zero.",
            value_or_layout="Req:W=64979/64979/195,R=0/0/0;Res:R=15288/15288/206,W=0/0/0;nested_declared=31071;nested_reached=30334",
            evidence_mode="CAPTURE_PARSED_OUTER_CENSUS",
            provenance="CURRENT_MIXED_CORPUS",
            prior_claims=(),
            nonclaim="Both outer families remain A2 static-open for the relevant nested attribution; their counts do not identify a ground-drop creation, omission, removal, expiry, or pickup member.",
            blocker="NESTED_MEMBER_ATTRIBUTION_OPEN",
            required_next_evidence="Closed nested schema or an eligible source-separated capture whose typed member is independently identified.",
        ),
        make_capture_row(
            facts,
            closure_id="GDP-CAP-004",
            row_kind="RUNTIME_RES_TERRAIN_POOL_TAIL_CENSUS",
            phase="S2C_DERIVED_TERRAIN_POOL",
            subject="GSCN_RunTimeProtocolRes derived TerrainThingPool tail",
            direction="S2C",
            semantic_status="OBSERVED_EXACT_WITH_FAIL_CLOSED_TAIL",
            exact_observation=(
                "Of 15,288 RuntimeRes R frames, the derived TerrainThingPool bit 0x08 is absent in 14,536, present "
                "with count zero in 0, present nonempty in 23 (22 count-one and one count-two), and unresolved "
                "in 729; 3 of the unresolved frames truncate before the derived mask. Outer mask 0x00 contains "
                "602 absent and all 23 nonempty frames; outer mask 0x02 contains 13,934 absent and all 729 unresolved."
            ),
            value_or_layout=(
                f"absent=14536;count_zero=0;nonempty=23;count1=22;count2=1;uncertain=729;truncated_mask=3;"
                f"outer00_absent=602;outer00_nonempty=23;outer02_absent=13934;outer02_uncertain=729;"
                f"uncertain_locator_manifest_sha256={facts.runtime_res_uncertain_manifest};"
                "uncertain_manifest_record=relative_path<TAB>file_sha256<TAB>block_ordinal<TAB>frame_sha256<TAB>reason;"
                "sort=lexicographic;join=LF_with_final_LF;encoding=UTF-8"
            ),
            evidence_mode="CAPTURE_EXACT_CLOSED_TAIL_PARSE_FAIL_CLOSED",
            provenance="CURRENT_MIXED_CORPUS",
            prior_claims=(),
            nonclaim="The 729 unresolved tails are not searched or resynchronized, and this row does not convert any captured omission into a client-deletion or original-server-policy claim.",
            blocker="729_TAILS_UNRESOLVED_AND_ORIGINAL_POLICY_OPEN",
            required_next_evidence="Closed schemas for the 726 stopped tails plus complete same-build frames for the three truncated derived masks.",
        ),
        make_capture_row(
            facts,
            closure_id="GDP-CAP-005",
            row_kind="PATH_CLASSIFIED_TERRAIN_POOL_SEQUENCE_CENSUS",
            phase="S2C_KEYSET_SEQUENCE",
            subject="confirmed nonempty TerrainThingPool frame/keyset metadata",
            direction="S2C",
            semantic_status="OBSERVED_EXACT_PATH_CLASSIFIED_SEQUENCE_PROVENANCE_OPEN",
            exact_observation=(
                "All 23 confirmed nonempty frames have a capture path component whose name starts with capture_v, "
                "across 11 files and 19 unique complete-frame hashes; 22 carry one record and one carries two "
                "records. Their file/block order, record counts, and hashed keysets are content-addressed without "
                "emitting any runtime key. This filename classification is not authoritative server provenance."
            ),
            value_or_layout=(
                f"event_manifest_sha256={facts.runtime_res_event_manifest};events=23;files=11;unique_frames=19;"
                "count1=22;count2=1;path_classification=PATH_CLASSIFIED_CAPTURE_V_PREFIX;"
                "authoritative_provenance=NOT_ESTABLISHED;"
                "manifest_record=relative_path<TAB>file_sha256<TAB>block_ordinal<TAB>frame_sha256<TAB>path_classification<TAB>record_count<TAB>keyset_sha256;"
                "sort=lexicographic;join=LF_with_final_LF;encoding=UTF-8"
            ),
            evidence_mode="CAPTURE_METADATA_HASHED_KEYSET_SEQUENCE",
            provenance=PATH_CAPTURE_V_CLASS,
            prior_claims=(),
            nonclaim="CAPTURE proves path text, frame order, categories, record counts, and hashed keysets only. A capture_v* path component does not prove replacement or original server provenance, and omission-causes-deletion remains the separately sourced IMAGE claim GDL-IMG-009.",
            blocker="AUTHORITATIVE_CAPTURE_PROVENANCE_LEDGER_NOT_PINNED",
            required_next_evidence="A content-addressed authoritative capture-to-server provenance ledger plus an independently typed pickup/removal ordering.",
        ),
        make_capture_row(
            facts,
            closure_id="GDP-CAP-006",
            row_kind="C2S_CLOSED_NESTED_REACH_CENSUS",
            phase="GAMEPLAY_AND_LOGIN_OUTER_NESTED_COLLECTION",
            subject="PickupTerrainThing among exactly reached C2S nested objects",
            direction="C2S",
            semantic_status="ZERO_IN_EXACT_REACHED_SUBSET_GLOBAL_ABSENCE_OPEN",
            exact_observation=(
                "The current path-classified capture_v* subset has 65,610 eligible C2S outer blocks: 64,979 "
                "gameplay 0x6E6F and 631 login 0x453A. 58,412 have outer bit 0x02 clear/no nested collection. Nested declared "
                "instances total 15,350; 14,615 wrappers/type IDs are exactly reached, traversal advances only "
                "across PASS CLOSED W schemas, and 735 later declared members remain unreached after the first "
                "fail-closed stop. PickupTerrainThing is 0 of 14,615 exactly reached wrappers/type IDs. The path "
                "classification is not authoritative server provenance."
            ),
            value_or_layout="outer=65610;gameplay=64979;login=631;no_nested=58412;declared=15350;reached=14615;fail_closed=735;PickupTerrainThing_reached=0;path_classification=PATH_CLASSIFIED_CAPTURE_V_PREFIX;authoritative_provenance=NOT_ESTABLISHED",
            evidence_mode="CAPTURE_CLOSED_SCHEMA_NESTED_TRAVERSAL",
            provenance=PATH_CAPTURE_V_CLASS,
            prior_claims=(),
            nonclaim="The 735 unresolved declared members prevent a global absence claim; zero of 14,615 exactly reached does not prove PickupTerrainThing absent from all 65,610 outer blocks, and capture_v* does not establish original-versus-replacement provenance.",
            blocker="735_C2S_MEMBERS_FAIL_CLOSED_AND_AUTHORITATIVE_PROVENANCE_OPEN",
            required_next_evidence="Close the first-open schemas and pin an authoritative provenance ledger or an independently authenticated original typed PickupTerrainThing exchange.",
        ),
        make_capture_row(
            facts,
            closure_id="GDP-CAP-007",
            row_kind="ORIGINAL_EXCHANGE_CEILING",
            phase="PICKUP_TO_AUTHORITATIVE_REMOVAL",
            subject="authoritatively qualified original pickup/removal exchange",
            direction="C2S_THEN_S2C",
            semantic_status="ZERO_ESTABLISHED_EXCHANGES_CARRIER_OPEN",
            exact_observation=(
                "Zero C2S pickup plus S2C omission/removal exchanges are qualified by a pinned authoritative "
                "ORIGINAL-provenance ledger, because no such ledger is pinned; this is a qualification ceiling, "
                "not proof that original traffic is absent. No exact omission/removal carrier is proved by CAPTURE. "
                "Existing PF_FIELD_VALIDATION.tsv is frozen to the older 1,772-file/595,134,426-byte inventory, "
                "not the current 2,227-file corpus."
            ),
            value_or_layout="authoritatively_qualified_original_exchange_count=0;authoritative_provenance_ledger=NOT_PINNED;exact_capture_removal_carrier=NOT_PROVEN;frozen_files=1772;current_files=2227",
            evidence_mode="CAPTURE_CEILING_PLUS_CONTENT_ADDRESSED_FROZEN_REFERENCE",
            provenance="CURRENT_MIXED_CORPUS",
            prior_claims=(frozen_prior,),
            nonclaim="Filename labels, client-observable disappearance, and outer traffic alone do not establish server provenance, an original message/vital/opcode, or an authoritative removal carrier.",
            blocker="AUTHORITATIVE_PROVENANCE_PICKUP_ACCEPTANCE_REMOVAL_ORDER_AND_EXPIRY_OPEN",
            required_next_evidence="A provenance-ledger-qualified original same-build C2S pickup followed by a typed S2C snapshot/full-clear/omit/remove sequence.",
        ),
    ]
    return rows


def valid_prior_tuples(prior: Mapping[str, PriorClaim], frozen_prior: PriorClaim) -> set[tuple[str, str, str]]:
    return {
        (claim.token, claim.artifact_sha256, claim.claim_digest)
        for claim in tuple(prior.values()) + (frozen_prior,)
    }


def expected_evidence_key(row: Mapping[str, str]) -> str:
    tail = row["source_sha256"]
    if row["source"] == SOURCE_IMAGE:
        return sha256(
            ROW_DOMAIN
            + row["claim_sha256"].encode("ascii")
            + b"\x00"
            + row["span_sha256"].encode("ascii")
            + b"\x00"
            + tail.encode("ascii")
        )
    return sha256(
        ROW_DOMAIN
        + row["claim_sha256"].encode("ascii")
        + b"\x00"
        + tail.encode("ascii")
    )


def semantic_row_digest(row: Mapping[str, str]) -> str:
    return canonical_digest(
        {
            key: value
            for key, value in row.items()
            if key not in {"closure_id", "claim_sha256", "evidence_key"}
        }
    )


def capture_full_row_template_digest(row: Mapping[str, str]) -> str:
    return canonical_digest(
        {
            key: value
            for key, value in row.items()
            if key not in {"claim_sha256", "evidence_key"}
        }
    )


def reject_positive_unledgered_provenance_claim(text: str, label: str) -> None:
    if AUTHORITATIVE_CAPTURE_PROVENANCE_LEDGER is not None:
        return
    normalized = " ".join(text.casefold().split())
    compact = re.sub(r"[^a-z0-9]+", "", normalized)
    positive_phrase = re.search(
        r"\b(?:all|these|the)?\s*(?:frames|events|captures)?\s*(?:are|is|from)\s+"
        r"(?:a\s+)?(?:replacement|original)\s+(?:server\s+)?provenance\b",
        normalized,
    )
    count_semantic = re.search(
        r"(?:replacement|original|unknown)(?:count)?\d+",
        compact,
    )
    legacy_semantic = any(
        token in compact
        for token in (
            "confirmednonemptyoriginal0",
            "exactreachedpickupreplacement0",
            "eligibleoriginalexchangecount0",
        )
    )
    if positive_phrase or count_semantic or legacy_semantic:
        raise ValueError(f"unledgered positive provenance/count semantics: {label}")


def validate_capture_provenance_ceiling(row: Mapping[str, str]) -> None:
    if row["source"] != SOURCE_CAPTURE or AUTHORITATIVE_CAPTURE_PROVENANCE_LEDGER is not None:
        return
    if row["provenance"] in {"REPLACEMENT", "ORIGINAL"}:
        raise ValueError(f"authoritative CAPTURE provenance asserted without ledger: {row['closure_id']}")
    claim_surface = "||".join(row[field] for field in FIELDNAMES)
    reject_positive_unledgered_provenance_claim(claim_surface, row["closure_id"])
    if any(token in claim_surface for token in FORBIDDEN_UNLEDGERED_PROVENANCE_CLAIMS):
        raise ValueError(f"CAPTURE provenance/count claim lacks authoritative ledger: {row['closure_id']}")
    expected_template = CAPTURE_FULL_ROW_TEMPLATE_SHA256.get(row["closure_id"])
    if expected_template is None or capture_full_row_template_digest(row) != expected_template:
        raise ValueError(f"CAPTURE full-row structural template drift: {row['closure_id']}")


def validate_rows(
    rows: Sequence[Mapping[str, str]],
    prior: Mapping[str, PriorClaim],
    frozen_prior: PriorClaim,
) -> None:
    if tuple(row.get("closure_id") for row in rows) != EXPECTED_IDS:
        raise ValueError("closure-id set/order mismatch")
    if any(tuple(row.keys()) != FIELDNAMES for row in rows):
        raise ValueError("row schema/order mismatch")
    if len({row["closure_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate closure id")
    if len({row["claim_sha256"] for row in rows}) != len(rows):
        raise ValueError("duplicate closure claim")
    if len({row["evidence_key"] for row in rows}) != len(rows):
        raise ValueError("duplicate evidence key")

    valid_image_prior = {
        (claim.token, claim.artifact_sha256, claim.claim_digest) for claim in prior.values()
    }
    frozen_capture_prior = (
        frozen_prior.token,
        frozen_prior.artifact_sha256,
        frozen_prior.claim_digest,
    )
    expected_capture_provenance = {
        "GDP-CAP-001": "CURRENT_MIXED_CORPUS",
        "GDP-CAP-002": "CURRENT_MIXED_CORPUS",
        "GDP-CAP-003": "CURRENT_MIXED_CORPUS",
        "GDP-CAP-004": "CURRENT_MIXED_CORPUS",
        "GDP-CAP-005": PATH_CAPTURE_V_CLASS,
        "GDP-CAP-006": PATH_CAPTURE_V_CLASS,
        "GDP-CAP-007": "CURRENT_MIXED_CORPUS",
    }
    for row in rows:
        source = row["source"]
        if source not in {SOURCE_IMAGE, SOURCE_CAPTURE}:
            raise ValueError(f"invalid source: {row['closure_id']}")
        if "ServerProject" in row["source_file"] or "current/" in row["source_file"]:
            raise ValueError(f"current server source forbidden: {row['closure_id']}")
        if source == SOURCE_IMAGE:
            if row["provenance"] != "ORIGINAL_IMAGE":
                raise ValueError(f"IMAGE provenance label mismatch: {row['closure_id']}")
            if row["source_file"] != IMAGE_SOURCE_FILE or row["source_size"] != str(IMAGE_SIZE) or row["source_sha256"] != IMAGE_SHA256:
                raise ValueError(f"IMAGE provenance mismatch: {row['closure_id']}")
            if any(row[field] != "N/A" for field in (
                "capture_file_count",
                "capture_total_bytes",
                "capture_manifest_sha256",
                "capture_text_file_count",
                "capture_block_count",
            )):
                raise ValueError(f"IMAGE row mixes CAPTURE metadata: {row['closure_id']}")
            if row["evidence_mode"].startswith("CANONICAL_"):
                if row["span_sha256"] != "N/A_CANONICAL_REFERENCE":
                    raise ValueError(f"canonical reference reissues IMAGE span: {row['closure_id']}")
            elif len(row["span_sha256"]) != 64:
                raise ValueError(f"IMAGE evidence span missing: {row['closure_id']}")
        else:
            if row["provenance"] != expected_capture_provenance[row["closure_id"]]:
                raise ValueError(f"CAPTURE provenance label mismatch: {row['closure_id']}")
            if row["source_file"] != CAPTURE_SOURCE_FILE:
                raise ValueError(f"CAPTURE source scope mismatch: {row['closure_id']}")
            if (
                row["source_size"] != str(CURRENT_CAPTURE_BYTES)
                or row["source_sha256"] != CURRENT_CAPTURE_MANIFEST
                or row["capture_file_count"] != str(CURRENT_CAPTURE_FILES)
                or row["capture_total_bytes"] != str(CURRENT_CAPTURE_BYTES)
                or row["capture_manifest_sha256"] != CURRENT_CAPTURE_MANIFEST
                or row["capture_text_file_count"] != str(CURRENT_TEXT_FILES)
                or row["capture_block_count"] != str(CURRENT_BLOCKS)
            ):
                raise ValueError(f"CAPTURE census provenance mismatch: {row['closure_id']}")
            if any("CAPTURE_METADATA_ONLY" not in row[field] for field in (
                "span_start_va",
                "span_end_va",
                "file_off_start",
                "file_off_end",
                "span_sha256",
                "support_spans",
                "direct_assertions",
            )):
                raise ValueError(f"CAPTURE row exposes/mixes IMAGE span: {row['closure_id']}")
            validate_capture_provenance_ceiling(row)

        claim_fields = {
            key: value for key, value in row.items() if key not in {"claim_sha256", "evidence_key"}
        }
        if row["claim_sha256"] != canonical_digest(claim_fields):
            raise ValueError(f"claim digest mismatch: {row['closure_id']}")
        if row["evidence_key"] != expected_evidence_key(row):
            raise ValueError(f"evidence key mismatch: {row['closure_id']}")
        if not row["required_next_evidence"].startswith("PROPOSED: "):
            raise ValueError(f"required-next-evidence label missing: {row['closure_id']}")

        refs = row["prior_reference"].split(";")
        artifacts = row["prior_artifact_sha256"].split(";")
        digests = row["prior_claim_digest"].split(";")
        if not (len(refs) == len(artifacts) == len(digests)):
            raise ValueError(f"prior tuple width mismatch: {row['closure_id']}")
        triplets = list(zip(refs, artifacts, digests))
        if source == SOURCE_IMAGE:
            if refs != ["N/A"] and any(triplet not in valid_image_prior for triplet in triplets):
                raise ValueError(f"IMAGE prior reference pin mismatch: {row['closure_id']}")
        elif row["closure_id"] == "GDP-CAP-007":
            if triplets != [frozen_capture_prior]:
                raise ValueError("CAPTURE frozen prior reference pin mismatch: GDP-CAP-007")
        elif refs != ["N/A"]:
            raise ValueError(f"CAPTURE row acquired cross-layer prior: {row['closure_id']}")

    if sum(row["source"] == SOURCE_IMAGE for row in rows) != 8:
        raise ValueError("IMAGE row count mismatch")
    if sum(row["source"] == SOURCE_CAPTURE for row in rows) != 7:
        raise ValueError("CAPTURE row count mismatch")
    if len({semantic_row_digest(row) for row in rows}) != len(rows):
        raise ValueError("duplicate semantic output row")


def render_tsv(rows: Sequence[Mapping[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDNAMES, delimiter="\t", lineterminator="\n", extrasaction="raise")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def claim_set_digest(rows: Sequence[Mapping[str, str]]) -> str:
    return digest_lines(
        [f"{row['closure_id']}:{row['claim_sha256']}:{row['evidence_key']}" for row in rows]
    )


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_report(rows: Sequence[Mapping[str, str]], facts: CaptureFacts, tsv: bytes) -> bytes:
    lines = [
        "# PF ground-drop / pickup closure",
        "",
        "This standalone P0-6 artifact closes the exact typed identity and bounded client transport path while preserving the runtime/policy ceilings. `source=IMAGE` and `source=CAPTURE` facts remain separate in every TSV row. No ServerProject/code row appears. A capture_v* filename component is reported only as a path classification and is not treated as server provenance.",
        "",
        "## Outcome",
        "",
        f"- Rows: {len(rows)} (IMAGE 8, CAPTURE 7).",
        f"- IMAGE: `{IMAGE_SOURCE_FILE}`, size `{IMAGE_SIZE}`, SHA-256 `{IMAGE_SHA256}`.",
        f"- Current CAPTURE corpus: `{CURRENT_CAPTURE_FILES}` files, `{CURRENT_CAPTURE_BYTES}` bytes, manifest `{CURRENT_CAPTURE_MANIFEST}`.",
        f"- Parsed CAPTURE text/block census: `{CURRENT_TEXT_FILES}` text files / `{CURRENT_BLOCKS}` PC+DECOMPRESSED blocks.",
        f"- TSV SHA-256: `{sha256(tsv)}`.",
        f"- Ordered claim-set SHA-256: `{claim_set_digest(rows)}`.",
        "",
        "## Exact typed closure (IMAGE)",
        "",
        "- The click path proves a DropThingGameObj is-a gate from the named MSVC TypeDescriptor through the custom descriptor parent chain. Derived classes are accepted.",
        "- On the reached action/type/range/allocation-success path: `PickupTerrainThing+0x14 == [DropThingGameObj+0x7C]->TerrainThing+0x10 == DropThingModule_Client reconciliation/map key`.",
        "- `0x4543` is the nested logical PickupTerrainThing runtime discriminator. `0x6E6F` is the gameplay outer logical discriminator. Login remains the distinct outer `0x453A`.",
        "- These values are logical runtime discriminators, not established top-level semantic opcodes.",
        "- The static path extends through serialize -> transform/repack -> chunks of at most `0x3FF8` -> the `WS2_32.dll` ordinal-19 `send` import.",
        "- `0x5F253EAC` is transport framing. Because `0x00B743B0` rewrites the buffer, no final socket literal is claimed for the logical discriminators.",
        "- The successful pickup-emission subpath has no direct edge to the three pinned known unregister/map-delete functions. Later authoritative S2C removal remains required/open.",
        "",
        "## Canonical removal matrix (references only)",
        "",
        "The matrix is composed only by content-addressing `GDL-IMG-007`, `GDL-IMG-008`, `GDL-IMG-009`, `GDL-IMG-010`, and `GDL-IMG-015` in pinned `PF_GROUND_DROP_LIFETIME.tsv`. Their IMAGE claims are not copied into new TSV evidence rows. The same rule is used for the FightingDrop false-lead classification (`GDT-IMG-008`, `GDT-IMG-009`, `GDL-CREF-001`).",
        "",
        "## Current capture ceiling (CAPTURE)",
        "",
        "- All four named target families (`PickupTerrainThing`, `DropThingModule_Client`, `FightingDropModule_Client`, `FightingDropNotify`) are W0/R0 in the broad current validator census.",
        "- RuntimeRes R has 15,288 frames: 14,536 with derived TerrainThingPool bit 0x08 absent, zero present-count-zero, 23 present-nonempty, and 729 fail-closed unresolved. The 23 nonempty frames are 22 count-one plus one count-two, in 11 files/19 unique complete-frame hashes; every path has a capture_v* component, but authoritative server provenance is not established.",
        f"- The nonempty-event metadata manifest is `{facts.runtime_res_event_manifest}`. Its records contain path/hash/ordinal/path-classification/count/keyset-hash only; runtime keys and payload bytes are not emitted. `PATH_CLASSIFIED_CAPTURE_V_PREFIX` records a filename property, not source truth.",
        f"- The all-729 unresolved-locator manifest is `{facts.runtime_res_uncertain_manifest}` over UTF-8 lines `relative_path<TAB>file_sha256<TAB>block_ordinal<TAB>frame_sha256<TAB>reason`, sorted lexicographically and joined with LF plus final LF. It contains 726 stopped tails and the three exact truncated-derived-mask locators listed below.",
        "- The capture_v*-path-classified gameplay/login C2S subset totals 65,610 outer blocks (64,979 gameplay, 631 login); 58,412 have no nested collection. Of 15,350 declared nested instances, 14,615 wrappers/type IDs are reached; traversal advances only across PASS CLOSED schemas, leaving 735 later declarations behind the first fail-closed stop. PickupTerrainThing is 0/14,615 reached wrappers/type IDs, not globally absent. The path label does not establish replacement or original provenance.",
        "- Zero pickup-to-authoritative-removal exchanges are qualified by a pinned authoritative ORIGINAL-provenance ledger because no such ledger is pinned; this does not prove original exchanges absent. No exact CAPTURE omission/removal carrier is proved.",
        "- Existing `PF_FIELD_VALIDATION.tsv` is frozen to 1,772 files / 595,134,426 bytes. It is not a current-2,227-file validation, and its generator has no `--check` option.",
        "- No proprietary capture payload or raw byte is emitted. The current manifest records only path, size, and file SHA-256.",
        "",
        "### Three truncated-derived-mask locators (CAPTURE metadata only)",
        "",
    ]
    for relative_path, file_sha, ordinal, frame_sha in TRUNCATED_DERIVED_MASK_LOCATORS:
        lines.append(
            f"- `{relative_path}` | file SHA-256 `{file_sha}` | block `{ordinal}` | frame SHA-256 `{frame_sha}`"
        )
    lines.extend(
        [
        "",
        "## IMAGE + CAPTURE analytical composition (not a TSV evidence row)",
        "",
        "Applying the separately sourced canonical IMAGE reconciliation rules (`GDL-IMG-007`, `GDL-IMG-008`, `GDL-IMG-009`) as an explicit analytical convention to the ordered CAPTURE metadata—state scoped per file; unresolved invalidates state; bit-absent resets; count-zero preserves—classifies the 23 confirmed nonempty events as ADD=13, ADD+OMIT=10, same-set update=0, with 10 one-entry swaps. This composition is not presented as a CAPTURE-only state-transition fact and does not prove original-server policy.",
        "",
        "## OPEN end-to-end gates",
        "",
        "- Production caller/transaction ownership and server acceptance of a pickup are not proved by IMAGE or current CAPTURE.",
        "- Last-item all-clear is OPEN. A non-NULL count-zero TerrainThingPool is canonically PRESERVE, so it cannot be renamed or guessed as clear.",
        "- Original issuance carrier, co-order, expiry duration/policy, and post-pickup removal carrier are OPEN.",
        "- Original-versus-replacement timing, shared-world ownership, scene ownership, retry policy, and final socket-byte literals are OPEN.",
        "- Client-local direct deletion on the pickup-emission subpath is not proved; indirect/virtual/tail/callback/later lifecycle paths remain possible.",
        "",
        "## RECONSTRUCTED current-server comparison (not TSV evidence)",
        "",
        f"The pinned urgent note `{URGENT_PATH.name}` (SHA-256 `{INPUT_PINS[URGENT_PATH][1]}`) reports that the current reconstructed implementation has scene-less drop-ledger ownership and no production pickup transaction/removal publisher. This comparison is labelled RECONSTRUCTED and is not used as IMAGE or CAPTURE evidence. The generator reads the pinned note, not ServerProject code.",
        "",
        "## Source-separated rows",
        "",
        "| closure_id | source | status | exact bounded result | blocker |",
        "|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(md_cell(row[column]) for column in ("closure_id", "source", "semantic_status", "exact_observation", "blocker"))
            + " |"
        )
    lines.extend(
        [
            "",
            "## Pinned canonical inputs",
            "",
            f"- `PF_GROUND_DROP_TRANSPORT.tsv`: `{INPUT_PINS[GDT_PATH][1]}`",
            f"- `PF_GROUND_DROP_LIFETIME.tsv`: `{INPUT_PINS[GDL_PATH][1]}`",
            f"- `PF_FIELD_VALIDATION.tsv` (frozen corpus only): `{INPUT_PINS[FIELD_VALIDATION_PATH][1]}`",
            f"- `pf_validate_capture_fields.py`: `{INPUT_PINS[VALIDATOR_PATH][1]}`",
            "",
            "## Deterministic verification",
            "",
            "```powershell",
            "py -3 pf_rederive_ground_drop_pickup_closure.py --check",
            "py -3 pf_rederive_ground_drop_pickup_closure.py --self-test",
            "```",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def generation_digest(tsv: bytes, report: bytes) -> str:
    return sha256(
        PAIR_DOMAIN
        + len(tsv).to_bytes(8, "little")
        + tsv
        + len(report).to_bytes(8, "little")
        + report
    )


def pair_payload(
    rows: Sequence[Mapping[str, str]],
    facts: CaptureFacts,
    tsv: bytes,
    report: bytes,
    generator_raw: bytes,
) -> dict[str, object]:
    return {
        "schema": "PF_GROUND_DROP_PICKUP_CLOSURE_PAIR_V1",
        "generation_sha256": generation_digest(tsv, report),
        "row_count": len(rows),
        "source_counts": {
            SOURCE_IMAGE: sum(row["source"] == SOURCE_IMAGE for row in rows),
            SOURCE_CAPTURE: sum(row["source"] == SOURCE_CAPTURE for row in rows),
        },
        "closure_ids": [row["closure_id"] for row in rows],
        "claim_set_sha256": claim_set_digest(rows),
        "generator": {
            "path": Path(__file__).name,
            "size": len(generator_raw),
            "sha256": sha256(generator_raw),
        },
        "image": {"path": IMAGE_SOURCE_FILE, "size": IMAGE_SIZE, "sha256": IMAGE_SHA256},
        "capture_corpus": {
            "scope": CAPTURE_SOURCE_FILE,
            "authoritative_server_provenance_ledger": AUTHORITATIVE_CAPTURE_PROVENANCE_LEDGER,
            "path_classification": {
                "label": PATH_CAPTURE_V_CLASS,
                "definition": "at least one relative-path component starts with capture_v (case-insensitive)",
                "is_authoritative_server_provenance": False,
            },
            "files": CURRENT_CAPTURE_FILES,
            "bytes": CURRENT_CAPTURE_BYTES,
            "manifest_sha256": CURRENT_CAPTURE_MANIFEST,
            "text_files": CURRENT_TEXT_FILES,
            "blocks": CURRENT_BLOCKS,
            "runtime_res_tail": {
                "bit08_absent": facts.runtime_res_absent,
                "present_count_zero": facts.runtime_res_count_zero,
                "present_nonempty": facts.runtime_res_nonempty,
                "uncertain": facts.runtime_res_uncertain,
                "truncated_derived_mask": facts.runtime_res_truncated_mask,
                "event_manifest_sha256": facts.runtime_res_event_manifest,
                "uncertain_locator_manifest_sha256": facts.runtime_res_uncertain_manifest,
            },
            "c2s_closed_nested": {
                "outer_blocks": facts.c2s_outer_blocks,
                "gameplay_outer_blocks": facts.c2s_gameplay_outer_blocks,
                "login_outer_blocks": facts.c2s_login_outer_blocks,
                "no_nested_blocks": facts.c2s_no_nested_blocks,
                "declared": facts.c2s_nested_declared,
                "reached": facts.c2s_nested_reached,
                "fail_closed": facts.c2s_nested_fail_closed,
                "pickup_reached": facts.c2s_pickup_reached,
            },
        },
        "canonical_inputs": {
            path.name: {"size": size, "sha256": digest}
            for path, (size, digest) in sorted(INPUT_PINS.items(), key=lambda item: item[0].name)
        },
        "files": {
            TSV_PATH.name: {"size": len(tsv), "sha256": sha256(tsv)},
            REPORT_PATH.name: {"size": len(report), "sha256": sha256(report)},
        },
        "publication_order": [TSV_PATH.name, REPORT_PATH.name, PAIR_PATH.name],
        "marker_published_last": True,
    }


def render_pair(
    rows: Sequence[Mapping[str, str]],
    facts: CaptureFacts,
    tsv: bytes,
    report: bytes,
    generator_raw: bytes,
) -> bytes:
    return (
        json.dumps(
            pair_payload(rows, facts, tsv, report, generator_raw),
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("ascii")


@dataclass(frozen=True)
class DerivedBundle:
    generator_raw: bytes
    image: bytes
    sections: tuple[Section, ...]
    facts: CaptureFacts
    prior: Mapping[str, PriorClaim]
    frozen_prior: PriorClaim
    rows: tuple[Mapping[str, str], ...]
    tsv: bytes
    report: bytes
    pair: bytes


def stable_image_read() -> bytes:
    before = IMAGE_PATH.stat()
    image = read_pinned(IMAGE_PATH, IMAGE_SIZE, IMAGE_SHA256)
    after = IMAGE_PATH.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError("client IMAGE changed during pinned read")
    return image


def validate_rendered(
    rows: Sequence[Mapping[str, str]],
    facts: CaptureFacts,
    tsv: bytes,
    report: bytes,
    pair: bytes,
    generator_raw: bytes,
) -> None:
    with io.StringIO(tsv.decode("utf-8"), newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        parsed_rows = list(reader)
        if tuple(reader.fieldnames or ()) != FIELDNAMES:
            raise ValueError("rendered TSV header mismatch")
    if parsed_rows != [dict(row) for row in rows]:
        raise ValueError("rendered TSV row mismatch")
    report_text = report.decode("utf-8")
    if "source=CAPTURE" not in report_text or "source=IMAGE" not in report_text:
        raise ValueError("report source-separation statement missing")
    reject_positive_unledgered_provenance_claim(report_text, "report")
    if AUTHORITATIVE_CAPTURE_PROVENANCE_LEDGER is None and any(
        token in report_text for token in FORBIDDEN_UNLEDGERED_PROVENANCE_CLAIMS
    ):
        raise ValueError("report contains an authoritative provenance/count claim without a pinned ledger")
    if sha256(report) != EXPECTED_REPORT_SHA256:
        raise ValueError("report structural template hash drift")
    payload = json.loads(pair.decode("ascii"))
    if payload != pair_payload(rows, facts, tsv, report, generator_raw):
        raise ValueError("pair marker payload mismatch")
    if payload["generation_sha256"] != generation_digest(tsv, report):
        raise ValueError("pair generation digest mismatch")


def derive_bundle() -> DerivedBundle:
    assert_game_lock_released()
    generator_path = Path(__file__).resolve()
    generator_before = generator_path.stat()
    generator_raw = generator_path.read_bytes()
    for path, (size, digest) in sorted(INPUT_PINS.items(), key=lambda item: str(item[0])):
        read_pinned(path, size, digest)

    image = stable_image_read()
    sections = parse_pe(image)
    static = verify_static_anchors(image, sections)
    prior, rows_by_path = build_prior_claims()
    verify_prior_semantics(rows_by_path)

    validator = load_validator()
    verify_frozen_validation(validator)
    facts = derive_capture_facts(validator)
    frozen_prior = capture_validation_prior(validator)
    rows = tuple(build_rows(image, sections, static, facts, prior, frozen_prior))
    validate_rows(rows, prior, frozen_prior)
    tsv = render_tsv(rows)
    report = render_report(rows, facts, tsv)
    generator_after = generator_path.stat()
    if (
        generator_before.st_size,
        generator_before.st_mtime_ns,
        generator_raw,
    ) != (
        generator_after.st_size,
        generator_after.st_mtime_ns,
        generator_path.read_bytes(),
    ):
        raise RuntimeError("generator changed during derivation")
    for path, (size, digest) in sorted(INPUT_PINS.items(), key=lambda item: str(item[0])):
        read_pinned(path, size, digest)
    if stable_image_read() != image:
        raise RuntimeError("client IMAGE changed across derivation")
    pair = render_pair(rows, facts, tsv, report, generator_raw)
    validate_rendered(rows, facts, tsv, report, pair, generator_raw)
    return DerivedBundle(
        generator_raw, image, sections, facts, prior, frozen_prior, rows, tsv, report, pair
    )


def stage_debris() -> tuple[Path, ...]:
    return tuple(
        sorted(
            (
                path
                for path in OUT_DIR.iterdir()
                if any(path.name.startswith(prefix) for prefix in STAGE_PREFIXES)
            ),
            key=lambda path: path.name.casefold(),
        )
    )


def assert_no_stage_debris() -> None:
    debris = stage_debris()
    if debris:
        raise RuntimeError("staged publication debris exists: " + ",".join(path.name for path in debris))


@contextmanager
def publisher_lock():
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
    try:
        descriptor = os.open(str(LOCK_PATH), flags, 0o600)
    except FileExistsError as exc:
        raise RuntimeError(f"publisher lock already exists: {LOCK_PATH.name}") from exc
    try:
        payload = memoryview(f"pid={os.getpid()}\n".encode("ascii"))
        while payload:
            written = os.write(descriptor, payload)
            if written <= 0:
                raise OSError("publisher lock write made no progress")
            payload = payload[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        yield
    finally:
        if descriptor >= 0:
            try:
                os.close(descriptor)
            except OSError:
                pass
        try:
            LOCK_PATH.unlink()
        except FileNotFoundError:
            pass


def write_exclusive(path: Path, data: bytes) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
    descriptor = os.open(str(path), flags, 0o600)
    try:
        remaining = memoryview(data)
        while remaining:
            written = os.write(descriptor, remaining)
            if written <= 0:
                raise OSError("exclusive staged write made no progress")
            remaining = remaining[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish_bundle(bundle: DerivedBundle) -> None:
    assert_no_stage_debris()
    targets = (
        (TSV_PATH, bundle.tsv),
        (REPORT_PATH, bundle.report),
        (PAIR_PATH, bundle.pair),
    )
    stages = tuple(
        OUT_DIR / f".{target.name}.{os.getpid()}.stage" for target, _data in targets
    )
    try:
        for stage, (_target, data) in zip(stages, targets):
            write_exclusive(stage, data)
        for stage, (target, _data) in zip(stages[:-1], targets[:-1]):
            os.replace(stage, target)
        os.replace(stages[-1], targets[-1][0])
    finally:
        for stage in stages:
            try:
                stage.unlink()
            except FileNotFoundError:
                pass
    assert_no_stage_debris()


def stable_file_bytes(path: Path) -> bytes:
    before = path.stat()
    first = path.read_bytes()
    middle = path.stat()
    second = path.read_bytes()
    after = path.stat()
    states = {
        (before.st_size, before.st_mtime_ns),
        (middle.st_size, middle.st_mtime_ns),
        (after.st_size, after.st_mtime_ns),
    }
    if len(states) != 1 or first != second:
        raise RuntimeError(f"published artifact changed during stable read: {path.name}")
    return first


def check_published(bundle: DerivedBundle) -> None:
    assert_no_stage_debris()
    expected = {
        TSV_PATH: bundle.tsv,
        REPORT_PATH: bundle.report,
        PAIR_PATH: bundle.pair,
    }
    for path, raw in expected.items():
        if not path.is_file():
            raise RuntimeError(f"published artifact missing: {path.name}")
        if stable_file_bytes(path) != raw:
            raise RuntimeError(f"published artifact drift: {path.name}")
    validate_rendered(
        bundle.rows,
        bundle.facts,
        bundle.tsv,
        bundle.report,
        bundle.pair,
        bundle.generator_raw,
    )


def reseal_row(row: dict[str, str]) -> None:
    row["claim_sha256"] = canonical_digest(
        {key: value for key, value in row.items() if key not in {"claim_sha256", "evidence_key"}}
    )
    row["evidence_key"] = expected_evidence_key(row)


def expect_failure(label: str, action) -> str:
    try:
        action()
    except Exception:
        return label
    raise AssertionError(f"fail-closed mutation unexpectedly passed: {label}")


def self_test(bundle: DerivedBundle) -> tuple[str, ...]:
    passed: list[str] = []

    bad_image = bytearray(bundle.image)
    bad_image[0] ^= 0x01
    passed.append(expect_failure("image_signature", lambda: parse_pe(bytes(bad_image))))

    bad_image = bytearray(bundle.image)
    pickup_off = va_to_offset(bundle.sections, SPANS["pickup_emit"].start)
    bad_image[pickup_off] ^= 0x01
    passed.append(
        expect_failure(
            "image_span_hash",
            lambda: span_bytes(bytes(bad_image), bundle.sections, "pickup_emit"),
        )
    )

    bad_image = bytearray(bundle.image)
    call_off = va_to_offset(bundle.sections, 0x00A8CBDB)
    bad_image[call_off] = 0x90
    passed.append(
        expect_failure(
            "transport_call_edge",
            lambda: expect_call(bytes(bad_image), bundle.sections, 0x00A8CBDB, 0x00B378E6),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[1]["closure_id"] = bad_rows[0]["closure_id"]
    reseal_row(bad_rows[1])
    passed.append(
        expect_failure(
            "closure_id_order",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[0]["source"] = "DUMP"
    reseal_row(bad_rows[0])
    passed.append(
        expect_failure(
            "source_enum",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[0]["capture_file_count"] = "0"
    reseal_row(bad_rows[0])
    passed.append(
        expect_failure(
            "image_capture_mix",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    cap005_index = next(
        index for index, row in enumerate(bundle.rows) if row["closure_id"] == "GDP-CAP-005"
    )
    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[cap005_index]["provenance"] = "CURRENT_MIXED_CORPUS"
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "capture_provenance",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[cap005_index]["subject"] = "original_count=0"
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "full_row_subject_hiding_place",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[cap005_index]["direct_assertions"] += "||MUTATED_STRUCTURAL_FIELD"
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "full_row_machine_field_hiding_place",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[cap005_index]["exact_observation"] += " All frames are REPLACEMENT provenance."
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "unledgered_replacement_claim",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[cap005_index]["exact_observation"] += " All frames are replacement provenance."
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "unledgered_lowercase_replacement_claim",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[cap005_index]["exact_observation"] += " Frames are from original provenance."
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "unledgered_paraphrased_original_claim",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[cap005_index]["value_or_layout"] += ";ORIGINAL=0"
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "unledgered_original_count",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[cap005_index]["value_or_layout"] += ";replacement_count=23;original_count=0"
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "unledgered_paraphrased_counts",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    image_prior = next(iter(bundle.prior.values()))
    bad_rows[cap005_index]["prior_reference"] = image_prior.token
    bad_rows[cap005_index]["prior_artifact_sha256"] = image_prior.artifact_sha256
    bad_rows[cap005_index]["prior_claim_digest"] = image_prior.claim_digest
    reseal_row(bad_rows[cap005_index])
    passed.append(
        expect_failure(
            "cross_layer_prior",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[1]["prior_claim_digest"] = "0" * 64
    reseal_row(bad_rows[1])
    passed.append(
        expect_failure(
            "prior_claim_pin",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    bad_rows[0]["evidence_key"] = "0" * 64
    passed.append(
        expect_failure(
            "evidence_key",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    bad_rows = copy.deepcopy(list(bundle.rows))
    preserved_id = bad_rows[1]["closure_id"]
    bad_rows[1] = copy.deepcopy(bad_rows[0])
    bad_rows[1]["closure_id"] = preserved_id
    reseal_row(bad_rows[1])
    passed.append(
        expect_failure(
            "duplicate_semantic_output",
            lambda: validate_rows(bad_rows, bundle.prior, bundle.frozen_prior),
        )
    )

    passed.append(
        expect_failure(
            "pool_wrong_tag",
            lambda: parse_terrain_pool_exact(b"\x14\x00\x00", 0),
        )
    )
    duplicate_pool = (
        b"\x12\x02\x00"
        b"\x14\x01\x00\x00\x00\x0b\x00"
        b"\x14\x01\x00\x00\x00\x0b\x00"
    )
    passed.append(
        expect_failure(
            "pool_duplicate_key",
            lambda: parse_terrain_pool_exact(duplicate_pool, 0),
        )
    )
    unknown_mask_pool = b"\x12\x01\x00\x14\x01\x00\x00\x00\x0b\x01"
    passed.append(
        expect_failure(
            "pool_unknown_mask",
            lambda: parse_terrain_pool_exact(unknown_mask_pool, 0),
        )
    )
    trailing_pool = b"\x12\x00\x00\xff"
    passed.append(
        expect_failure(
            "pool_trailing_no_resync",
            lambda: parse_terrain_pool_exact(trailing_pool, 0),
        )
    )

    synthetic_open_outer = (
        b"\x12\x6f\x6e\x14\x00\x00\x00\x00\x08\x00\x0b\x02"
        b"\x12\x01\x00\x12\x34\x12\x0b\x00"
    )

    def require_static_open_tail() -> None:
        result = parse_closed_nested_tail(
            synthetic_open_outer,
            "W",
            {0x1234: "SyntheticOpen"},
            {("SyntheticOpen", "W"): ()},
            {"SyntheticOpen"},
        )
        if result[0] is None:
            raise RuntimeError("synthetic static-open member stopped traversal")

    passed.append(expect_failure("static_open_stop", require_static_open_tail))

    passed.append(
        expect_failure(
            "rendered_tsv",
            lambda: validate_rendered(
                bundle.rows,
                bundle.facts,
                bundle.tsv + b"x",
                bundle.report,
                bundle.pair,
                bundle.generator_raw,
            ),
        )
    )
    bad_payload = json.loads(bundle.pair.decode("ascii"))
    bad_payload["row_count"] += 1
    bad_pair = (json.dumps(bad_payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode("ascii")
    passed.append(
        expect_failure(
            "pair_marker",
            lambda: validate_rendered(
                bundle.rows,
                bundle.facts,
                bundle.tsv,
                bundle.report,
                bad_pair,
                bundle.generator_raw,
            ),
        )
    )
    unledgered_report = bundle.report + b"\nAll observed frames are REPLACEMENT provenance.\n"
    unledgered_pair = render_pair(
        bundle.rows,
        bundle.facts,
        bundle.tsv,
        unledgered_report,
        bundle.generator_raw,
    )
    passed.append(
        expect_failure(
            "report_unledgered_provenance_claim",
            lambda: validate_rendered(
                bundle.rows,
                bundle.facts,
                bundle.tsv,
                unledgered_report,
                unledgered_pair,
                bundle.generator_raw,
            ),
        )
    )
    passed.append(
        expect_failure(
            "report_generation_pair",
            lambda: validate_rendered(
                bundle.rows,
                bundle.facts,
                bundle.tsv,
                bundle.report + b"\n",
                bundle.pair,
                bundle.generator_raw,
            ),
        )
    )
    if len(passed) < 7:
        raise AssertionError("self-test mutation census below required floor")
    return tuple(passed)


def result_payload(status: str, bundle: DerivedBundle, mutations: Sequence[str] = ()) -> dict[str, object]:
    payload: dict[str, object] = {
        "status": status,
        "row_count": len(bundle.rows),
        "source_counts": {
            SOURCE_IMAGE: sum(row["source"] == SOURCE_IMAGE for row in bundle.rows),
            SOURCE_CAPTURE: sum(row["source"] == SOURCE_CAPTURE for row in bundle.rows),
        },
        "generation_sha256": generation_digest(bundle.tsv, bundle.report),
        "claim_set_sha256": claim_set_digest(bundle.rows),
        "files": {
            TSV_PATH.name: {"size": len(bundle.tsv), "sha256": sha256(bundle.tsv)},
            REPORT_PATH.name: {"size": len(bundle.report), "sha256": sha256(bundle.report)},
            PAIR_PATH.name: {"size": len(bundle.pair), "sha256": sha256(bundle.pair)},
        },
    }
    if mutations:
        payload["fail_closed_mutations"] = list(mutations)
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="derive and compare all published bytes")
    mode.add_argument("--self-test", action="store_true", help="derive and run fail-closed mutations")
    args = parser.parse_args(argv)

    try:
        with publisher_lock():
            assert_no_stage_debris()
            bundle = derive_bundle()
            if args.check:
                check_published(bundle)
                result = result_payload("PASS", bundle)
            elif args.self_test:
                mutations = self_test(bundle)
                assert_no_stage_debris()
                result = result_payload("PASS_SELF_TEST", bundle, mutations)
            else:
                publish_bundle(bundle)
                check_published(bundle)
                result = result_payload("PUBLISHED", bundle)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
