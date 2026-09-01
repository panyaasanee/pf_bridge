#!/usr/bin/env python3
"""Re-derive the bounded P0-5 combat lethal-tail IMAGE delta.

This generator reads only the pinned original client image and pinned prior
artifacts.  It publishes only new lifecycle refinements; prior claims are cited
by exact row identity, artifact hash, and claim digest rather than copied.
It never runs the client, server, dump, or capture.  Console output is ASCII.
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
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
TSV_PATH = OUT_DIR / "PF_COMBAT_LETHAL_TAIL_DELTA.tsv"
REPORT_PATH = OUT_DIR / "PF_COMBAT_LETHAL_TAIL_DELTA.md"
PAIR_PATH = OUT_DIR / "PF_COMBAT_LETHAL_TAIL_DELTA.pair.json"
LOCK_PATH = OUT_DIR / ".PF_COMBAT_LETHAL_TAIL_DELTA.lock"
STAGE_PREFIXES = (
    ".PF_COMBAT_LETHAL_TAIL_DELTA.tsv.",
    ".PF_COMBAT_LETHAL_TAIL_DELTA.md.",
    ".PF_COMBAT_LETHAL_TAIL_DELTA.pair.json.",
)

SOURCE = "IMAGE"
SOURCE_FILE = "PF_ROOT://GameClient/GameClient.local.bin"
IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"

COMBAT_PATH = OUT_DIR / "PF_COMBAT_LIFECYCLE.tsv"
GROUND_PATH = OUT_DIR / "PF_GROUND_DROP_LIFETIME.tsv"
COLOR_PATH = OUT_DIR / "PF_MONSTER_COLOR_GATE.tsv"
ROLE_PATH = OUT_DIR / "PF_ATTR_ROLE_DISCRIMINATOR.tsv"
RELATION_PATH = OUT_DIR / "PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv"
QUEST_EVENT_PATH = OUT_DIR / "PF_QUEST_MARK_EVENT_CENSUS.tsv"
ATTR_PATH = OUT_DIR / "PF_ATTR_FIELD_SEMANTICS.tsv"
FACTPACK_PATH = OUT_DIR.parent / "FACTPACK_R102_DYING_COUNTDOWN_UI_FIELD_STATIC.md"

PRIOR_PINS = {
    COMBAT_PATH: (
        41_063,
        "305b7bdc12e9b638e3c3f37f996af8bb0e2d1877241aaf171885b8fae106b658",
    ),
    GROUND_PATH: (
        61_979,
        "b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710",
    ),
    COLOR_PATH: (
        110_234,
        "8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0",
    ),
    ROLE_PATH: (
        42_626,
        "3e8d99dd9fd9c8717e27d3ec8d43e2599a6037fc366e58637aff3a5cc8d5ec73",
    ),
    RELATION_PATH: (
        104_190,
        "0192050fab1df86346a8aac069a3f0f3fbe90620589879a89890461780e812ad",
    ),
    QUEST_EVENT_PATH: (
        29_193,
        "40127e6410c1aa6405efada640c60b72663eb9e35537c8011cdeede47d0a0b35",
    ),
    ATTR_PATH: (
        1_339_980,
        "1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f",
    ),
}
FACTPACK_SIZE = 24_321
FACTPACK_SHA256 = "642dc3ba52c00e93798d0434d618def1b8fe4d95172470187746e74d3b67c0cd"

DROP_DIRECT_TARGETS = (
    0x005F53A0,
    0x006AF970,
    0x005F41E0,
    0x00B0E4A0,
    0x00B0EE40,
    0x006B03F0,
)
PANEL_DIRECT_TARGETS = (
    0x0051F150,
    0x0051F2F0,
    0x0051F920,
    0x0051E890,
)

ROW_DOMAIN = b"PF_COMBAT_LETHAL_TAIL_DELTA_ROW_V1\x00"
PAIR_DOMAIN = b"PF_COMBAT_LETHAL_TAIL_DELTA_PAIR_V1\x00"


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


EXPECTED_SECTIONS = (
    (".text", 0x00401000, 0x00838A2C, 0x00000400, 0x00838C00, True),
    (".code", 0x00C3A000, 0x000002E1, 0x00839000, 0x00000400, True),
    (".rdata", 0x00C3B000, 0x003DE38E, 0x00839400, 0x003DE400, False),
    (".data", 0x0101A000, 0x00081F70, 0x00C17800, 0x00011E00, False),
    (".rsrc", 0x0109C000, 0x00058998, 0x00C29600, 0x00058A00, False),
    (".reloc", 0x010F5000, 0x001915F0, 0x00C82000, 0x00191600, False),
)

SPANS = {
    "runtime_actor_then_terrain": Span(
        0x005E4073,
        0x005E40DA,
        "cac54b8320f1869f55310ff7bca0d274859052c3febb79a8295ee308ed0f6624",
    ),
    "typed_terrain_bridge": Span(
        0x005F53A0,
        0x005F5456,
        "77136c150b0e557ad4facea096191de0fb9f23e9c30ee5c550c8fa6594b33894",
    ),
    "death_sync": Span(
        0x004437C0,
        0x00443A9A,
        "85d294b84843e0bd46256e0257cf5d51be0415081739d82b0b4c254975ee9592",
    ),
    "target_clear_order": Span(
        0x00443A01,
        0x00443A7A,
        "abcb7fb1a09b752faaac0376f40552f1da6b1daed206d7b7d5975d023401443e",
    ),
    "target_setter": Span(
        0x0043E1D0,
        0x0043E279,
        "420c25a873d3d1cc07a64aa4420a43cc56ff54992d75027126ba049c78a79101",
    ),
    "myactor_singleton_store": Span(
        0x0044CB7D,
        0x0044CB83,
        "125666cd9ccb90677ad63c0e0b9b417e1ce37e2e66a39b0f8cad10f48d3b30c4",
    ),
    "relation_predicate": Span(
        0x0043C380,
        0x0043C63C,
        "1d99f8557252742914c4f7358853aac06f0b54603f78a4b4d073aaea2afcbd89",
    ),
    "actorattr_vtable": Span(
        0x00F0E7A0,
        0x00F0E7E0,
        "36511ad596f0cd6db58929c6b9b58a7615399a04745293336fa2461c97632b10",
    ),
    "actorattr_ctor_zero": Span(
        0x00464DD0,
        0x00464DDC,
        "a514bf35a432735c1525305813ebf9f5a6f126c2f9046cbf87abf7215ca1ecd5",
    ),
    "actorattr_copy_field": Span(
        0x0046517C,
        0x00465194,
        "4aaeee33f169982be071c408e80ebca539f807734d16e6e07b71652701e2cc2f",
    ),
    "actorattr_copy": Span(
        0x00464F30,
        0x0046520E,
        "48b18bc342646c53235ecabb466a177e3b41b61e72ba50b2ad5e5be8c62faf8f",
    ),
    "actorattr_merge_field": Span(
        0x0046610B,
        0x00466130,
        "f4de98ccc1c179bf5caa54a5574dd4ccb96bc32af621167896fe98d3079caba0",
    ),
    "actorattr_merge": Span(
        0x00465E60,
        0x0046622C,
        "ae42593007f32d954a25990b2599aaabcc040dd20a4c3c27e87cb18464ab0cb5",
    ),
    "actorattr_receive_field": Span(
        0x00466B18,
        0x00466B36,
        "2956feaf58f7003f72bff55bc1c947d3731d506177742f76995824cdd427d099",
    ),
    "actorattr_codec": Span(
        0x00466230,
        0x00466C6F,
        "ff1bf8f6b8beb33d6c070d4bbb2d37f8d83aaa93545a38397bf58f8acf72a5ed",
    ),
    "npcattr_vtable": Span(
        0x00F0E7E0,
        0x00F0E820,
        "90cb44125268805342fd3c818d340310acc37b309b96e5614f89cfaea7fd57df",
    ),
    "npcattr_ctor_zero": Span(
        0x00465265,
        0x0046527A,
        "84e86105408dde76cde2960bd9f87bc34734b8f33ca10f91ead4926545c13ad1",
    ),
    "npcattr_copy_field": Span(
        0x004653B1,
        0x004653C9,
        "84bbf7f66fed8cdc01b4a2e900eaa7dd8daf2c35566a8678d62a82a3323abf5f",
    ),
    "npcattr_copy": Span(
        0x00465340,
        0x004653FF,
        "6c11a0df6ee0124862a5d7f3703ef794a45be4c51bd33e66cb3c64322f4d7a09",
    ),
    "npcattr_merge_field": Span(
        0x00466E2B,
        0x00466E69,
        "d05a240b569ac1dd6d4919d1641d800318a3f71d86017080f05fa185ab99366e",
    ),
    "npcattr_merge": Span(
        0x00466DC0,
        0x00466EA7,
        "2c9f05ba5accac3a6b2743aed456a7754eca7d10b2382231c68019a782461c4e",
    ),
    "npcattr_receive_field": Span(
        0x00466FE2,
        0x00466FF9,
        "f398128e3053f5d33a1d8a3eba7a8dd20463d50f03e461645a966057d43996a5",
    ),
    "npcattr_codec": Span(
        0x00466EB0,
        0x0046702D,
        "da9a2c2a30f4d131d0d3018a9daaa1b4a97bdd2b41145ff6d607a3baa29253ff",
    ),
    "receive_helper": Span(
        0x0089A640,
        0x0089A6C6,
        "4b58ff55a1e7fdd1640f7be47db6a44a41d1e83093bd8dd271c5c0d1dab3ca51",
    ),
    "chit_handler": Span(
        0x00750770,
        0x00750EC0,
        "151e5425155d5a5df6f1944f88fa2c041c6ea74dc8a69c8f907a54a807b5af70",
    ),
    "chit_target_side_effect": Span(
        0x00750AAE,
        0x00750C57,
        "30dd3701f8eed185cb9112cad7da1c9cd7d32e91f6a8efbe075795aef21605ae",
    ),
    "actor_entry_update": Span(
        0x004446F0,
        0x00444730,
        "e4e5b3719b24f7ee32791e4a419ff37942031610691f25c4d943cae9f1ae4508",
    ),
    "observer_fanout": Span(
        0x005DF080,
        0x005DF0D2,
        "a65ec5fa355580de5e39950da766201907c42ee56b9e8477c9a4874c94e82644",
    ),
    "observer_dispatcher": Span(
        0x0059D270,
        0x0059D314,
        "6f6b214321f63f0490fd69dec2366a05b500c3ab6ffe38beb161fdea6e672022",
    ),
    "observer_wrapper": Span(
        0x0059D760,
        0x0059D7BB,
        "66ced8e6addc5bae12791a3c4309bf15e0b24e8641410db9ca889c4c6bbeb8a7",
    ),
    "dead_predicate": Span(
        0x0043BD70,
        0x0043BD9D,
        "1df3c62b4bbe0aab1ebf1404320a7b2466ef20390db060e67ba183a1178127aa",
    ),
    "dying_predicate": Span(
        0x0043BDA0,
        0x0043BDD2,
        "04e08d24980faf23e0bcb7d9e6f1e69dfdba704abfedf6a8531ceeedbb5e8866",
    ),
    "basicattr_codec": Span(
        0x004656F0,
        0x00465983,
        "d0c15b74a36077df30a0e60dbeb8441e878c08b82587c1ea55365ab2ebd70020",
    ),
    "dead_ctor": Span(
        0x00472810,
        0x00472834,
        "54877d3101b779ba1b83e283cbe94f8db9799905fc7a1157a1ada2e3f249c0a7",
    ),
    "dead_vtable": Span(
        0x00F0F048,
        0x00F0F05C,
        "6432481111b7c85c0ffee8b9eb6f512e9955b0110e9a7c9c01875b4687eb7bda",
    ),
    "queue_wrapper": Span(
        0x004843C0,
        0x004843EA,
        "72a328e5a239691f2441ea0a78f7d63cbc06b941b7322ec22d43bbd3d57c8cd8",
    ),
    "manager_add": Span(
        0x004A0C90,
        0x004A0D78,
        "24b4ae5879bec87d31b0b836486646378be01684b0a22c754db0331d25127f6a",
    ),
    "queue_update": Span(
        0x004A0B50,
        0x004A0C5C,
        "b40a715681350369522dfabdbce85ef8fef622b8f924cb25933edba735652c87",
    ),
    "promote_start": Span(
        0x004A09C0,
        0x004A0A98,
        "90047f3e8afae6e07826afdaaeb6b390b7e078f07ae5d61063b3c87baaee3638",
    ),
    "dead_start": Span(
        0x004765C0,
        0x00476763,
        "e771b911d0ba2019364b3cda8e6a7ba5c54e2a0a21cf3ae6d0cba1b4f8ed7658",
    ),
    "dead_update": Span(
        0x00472850,
        0x004728F3,
        "e04385a8cd54b800add22c4c8c5cc751b4243e19d208d684acdb8af2b6350999",
    ),
    "die_literal": Span(
        0x00F0F060,
        0x00F0F076,
        "2df025844462e0ac2c9038f01a12f22a6a70cbe4b4592a4e5db9cb8a443cfeaa",
    ),
    "cnetnpc_model_callback_gate": Span(
        0x00444730,
        0x0044497B,
        "bff91e77c4570c959170e89cd65d96b175eb6a1728b26ac465bdc14da04f5a33",
    ),
}

FIELDNAMES = (
    "delta_id",
    "row_kind",
    "phase",
    "applies_to_class",
    "predecessor",
    "successor",
    "order_relation",
    "trigger_or_condition",
    "exact_observation",
    "semantic_status",
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

EXPECTED_IDS = tuple(f"LT-IMG-{number:03d}" for number in range(1, 16))
EXPECTED_KINDS = (
    "INTRA_RESPONSE_ORDER",
    "BOUNDED_DIRECT_EDGE_NEGATIVE",
    "TARGET_CLEAR_ORDER",
    "RUNTIME_TARGET_CLEAR",
    "TYPED_FIELD_SEPARATION",
    "TYPED_FIELD_SEPARATION",
    "HIT_TARGET_SIDE_EFFECT",
    "BOUNDED_DIRECT_EDGE_NEGATIVE",
    "OBSERVER_BEFORE_DEATH",
    "DEAD_TASK_CONSTRUCTION",
    "TASK_MANAGER_PROGRESS",
    "EVENT_BEFORE_POSE_GATE",
    "MODEL_READINESS_GATE",
    "DEAD_TASK_PERSISTENCE",
    "TIMER_AUTHORITY_BOUNDARY",
)
EXPECTED_STATUSES = (
    "PROVEN_EXACT",
    "PROVEN_EXACT_BOUNDED",
    "PROVEN_EXACT",
    "PROVEN_EXACT",
    "PROVEN_EXACT_BOUNDED",
    "PROVEN_EXACT_BOUNDED",
    "PROVEN_EXACT_BOUNDED",
    "PROVEN_EXACT_BOUNDED",
    "PROVEN_EXACT",
    "PROVEN_EXACT",
    "PROVEN_EXACT",
    "PROVEN_EXACT",
    "PROVEN_EXACT",
    "PROVEN_EXACT_BOUNDED",
    "PARTIAL",
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_lines(lines: Sequence[str]) -> str:
    return sha256(("\n".join(lines) + "\n").encode("ascii"))


def canonical_row_digest(row: Mapping[str, str]) -> str:
    return sha256(
        json.dumps(
            dict(row), sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    )


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


def expect_dwords(
    image: bytes, sections: Sequence[Section], va: int, expected: Sequence[int]
) -> None:
    off = va_to_offset(sections, va, 4 * len(expected))
    actual = struct.unpack_from(f"<{len(expected)}I", image, off)
    if tuple(actual) != tuple(expected):
        raise RuntimeError(f"dword guard failed at 0x{va:08X}")


def expect_utf16(
    image: bytes, sections: Sequence[Section], va: int, expected: str
) -> None:
    encoded = (expected + "\x00").encode("utf-16le")
    off = va_to_offset(sections, va, len(encoded))
    if image[off : off + len(encoded)] != encoded:
        raise RuntimeError(f"UTF-16 guard failed at 0x{va:08X}")


def call_target(
    image: bytes, sections: Sequence[Section], site: int
) -> int:
    off = va_to_offset(sections, site, 5)
    if image[off] != 0xE8:
        raise RuntimeError(f"direct call opcode missing at 0x{site:08X}")
    return (site + 5 + struct.unpack_from("<i", image, off + 1)[0]) & 0xFFFFFFFF


def expect_call(
    image: bytes, sections: Sequence[Section], site: int, target: int
) -> None:
    if call_target(image, sections, site) != target:
        raise RuntimeError(f"direct call target drift at 0x{site:08X}")


def raw_e8_lines(
    image: bytes, sections: Sequence[Section], span_name: str
) -> list[str]:
    raw, _, _ = span_bytes(image, sections, span_name)
    start = SPANS[span_name].start
    lines: list[str] = []
    for index in range(len(raw) - 4):
        if raw[index] != 0xE8:
            continue
        site = start + index
        relative = struct.unpack_from("<i", raw, index + 1)[0]
        target = (site + 5 + relative) & 0xFFFFFFFF
        lines.append(f"0x{site:08X}->0x{target:08X}")
    return lines


def format_span(
    image: bytes, sections: Sequence[Section], name: str
) -> str:
    _, start, end = span_bytes(image, sections, name)
    spec = SPANS[name]
    return (
        f"{name}=VA:0x{spec.start:08X}..0x{spec.end:08X}"
        f"@file:0x{start:08X}..0x{end:08X}@sha256:{spec.sha256}"
    )


def load_tsv(path: Path) -> list[dict[str, str]]:
    size, digest = PRIOR_PINS[path]
    raw = read_pinned(path, size, digest)
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise RuntimeError(f"prior artifact has no rows: {path.name}")
    return rows


def prior_row_digest(row: Mapping[str, str]) -> str:
    for field in ("claim_sha256", "semantic_fingerprint"):
        value = row.get(field, "")
        if len(value) == 64 and all(ch in "0123456789abcdef" for ch in value):
            return value
    return canonical_row_digest(row)


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
    if row.get("source") != SOURCE:
        raise RuntimeError(f"prior row source drift: {path.name}:{key}")
    evidence_key = row.get("evidence_key", "")
    suffix = f"@{evidence_key}" if evidence_key else ""
    return PriorClaim(
        f"{path.name}:{key}{suffix}",
        PRIOR_PINS[path][1],
        prior_row_digest(row),
    )


def factpack_prior() -> PriorClaim:
    raw = read_pinned(FACTPACK_PATH, FACTPACK_SIZE, FACTPACK_SHA256)
    markers = (
        b'"basicattr_0x58_frame_delta_decrementers": 0',
        b"BasicAttr.f32[+0x58]",
        b"0x464B0E",
        b"0x4656A3",
        b"0x4658E8",
    )
    if not all(marker in raw for marker in markers):
        raise RuntimeError("FACTPACK R102 marker drift")
    claim = b"\n".join(markers) + b"\n"
    return PriorClaim(
        f"{FACTPACK_PATH.name}:bounded_basicattr_0x58_writer_census",
        FACTPACK_SHA256,
        sha256(claim),
    )


def join_prior(claims: Sequence[PriorClaim]) -> tuple[str, str, str]:
    if not claims:
        return "N/A", "N/A", "N/A"
    return (
        ";".join(claim.token for claim in claims),
        ";".join(claim.artifact_sha256 for claim in claims),
        ";".join(claim.claim_digest for claim in claims),
    )


def verify_static_anchors(
    image: bytes, sections: Sequence[Section]
) -> dict[str, object]:
    for name in SPANS:
        span_bytes(image, sections, name)

    expect_call(image, sections, 0x005E4085, 0x00446F30)
    expect_call(image, sections, 0x005E40D5, 0x005F53A0)

    death_calls = raw_e8_lines(image, sections, "death_sync")
    if len(death_calls) != 26:
        raise RuntimeError("death-sync raw E8 census count drift")
    if digest_lines(death_calls) != "e5a796c75b0e64e25a1e87032c5f0be71ffa27d82d72218dbc68643ca2ec5ff7":
        raise RuntimeError("death-sync raw E8 census digest drift")
    death_targets = {int(line.rsplit("0x", 1)[1], 16) for line in death_calls}
    if death_targets.intersection(DROP_DIRECT_TARGETS):
        raise RuntimeError("death-sync acquired a direct typed-drop edge")

    expect_bytes(image, sections, 0x0044CB7D, "8935c42e0301")
    expect_bytes(image, sections, 0x0044399B, "8b7e3085ff7425")
    expect_bytes(
        image,
        sections,
        0x004439BB,
        "f7d81bc023c70f85c0000000",
    )
    expect_bytes(
        image,
        sections,
        0x00443A0B,
        "8b56788b81c80000008bb9cc0000008b767c3bc275663bfe75626a006a00",
    )
    expect_call(image, sections, 0x00443A29, 0x0043E1D0)
    expect_call(image, sections, 0x00443A38, 0x00A9EF00)
    expect_bytes(image, sections, 0x00443A3D, "8bf085f67444")
    expect_utf16(image, sections, 0x00F0D2A8, "Main_Panel_Target_Enemy_New")
    expect_utf16(image, sections, 0x00F0D470, "TargetIsDead")
    expect_bytes(
        image,
        sections,
        0x0043E224,
        "8b0dc42e0301c78108040000000000008b15c42e0301c7820c04000000000000",
    )
    expect_bytes(
        image,
        sections,
        0x0043E264,
        "8b4c241089aec8000000898ecc000000",
    )
    expect_bytes(image, sections, 0x0043E202, "8bf885ff741c")
    expect_call(image, sections, 0x0043E24F, 0x00A9EF00)
    expect_bytes(image, sections, 0x0043E254, "85c0740c")

    expect_dwords(
        image,
        sections,
        0x00F0E7A0,
        (
            0x004649A0,
            0x004673F0,
            0x00401B20,
            0x00464E50,
            0x00464E40,
            0x004675E0,
            0x0043BB80,
            0x00463710,
            0x0043BB70,
            0x00464F30,
            0x00465990,
            0x004659B0,
            0x00465E60,
            0x00466230,
            0x00469760,
            0x004CD2F0,
        ),
    )
    expect_dwords(
        image,
        sections,
        0x00F0E7E0,
        (
            0x004652B0,
            0x00467450,
            0x00401B20,
            0x004652D0,
            0x004652C0,
            0x00467600,
            0x0043BB80,
            0x00463710,
            0x0043BB70,
            0x00465340,
            0x00466C80,
            0x00466CA0,
            0x00466DC0,
            0x00466EB0,
            0x004697B0,
            0x004CD2F0,
        ),
    )
    expect_call(image, sections, 0x00466B31, 0x0089A640)
    expect_call(image, sections, 0x00466FF4, 0x0089A640)

    for site, target in (
        (0x00750AE1, 0x0043C380),
        (0x00750B20, 0x0043CDC0),
        (0x00750B33, 0x0043E010),
        (0x00750B40, 0x0043CDA0),
        (0x00750B4D, 0x0043CDC0),
        (0x00750BA9, 0x0043CDC0),
        (0x00750BBC, 0x0043E1D0),
        (0x00750BC9, 0x0043CDA0),
        (0x00750BD6, 0x0043CDC0),
        (0x00750C3E, 0x00AA0710),
    ):
        expect_call(image, sections, site, target)
    expect_utf16(image, sections, 0x00F0D87C, "TargetEnemyIsFocused")

    chit_calls = raw_e8_lines(image, sections, "chit_handler")
    if len(chit_calls) != 50:
        raise RuntimeError("CHitResult raw E8 census count drift")
    if digest_lines(chit_calls) != "c2a0e69244a75766518a24409337ff8fa892020d0e7f47a6a9f416ada8d47ddd":
        raise RuntimeError("CHitResult raw E8 census digest drift")
    chit_targets = {int(line.rsplit("0x", 1)[1], 16) for line in chit_calls}
    if chit_targets.intersection(PANEL_DIRECT_TARGETS):
        raise RuntimeError("CHitResult acquired a direct target-panel refresh edge")

    expect_call(image, sections, 0x004446FE, 0x005DF080)
    expect_call(image, sections, 0x00444705, 0x004437C0)

    expect_bytes(
        image,
        sections,
        0x0047281D,
        "c70648f0f000c6462000c7461005000080",
    )
    expect_dwords(
        image,
        sections,
        0x00F0F048,
        (0x00472840, 0x00487FA0, 0x004765C0, 0x00472850, 0x00476770),
    )
    expect_call(image, sections, 0x004438BD, 0x004843C0)
    expect_call(image, sections, 0x004439D1, 0x00442D50)
    expect_bytes(image, sections, 0x004439E2, "85c0740a")
    expect_call(image, sections, 0x004439E9, 0x00472810)
    expect_call(image, sections, 0x004439FC, 0x004843C0)
    expect_bytes(image, sections, 0x004843C0, "8b44240485c0741f")
    expect_call(image, sections, 0x004843D7, 0x004A0C90)
    expect_call(image, sections, 0x004843E2, 0x004A0C90)
    expect_call(image, sections, 0x004A0D6E, 0x004A0B50)
    expect_call(image, sections, 0x004A0B83, 0x004A09C0)
    expect_bytes(
        image,
        sections,
        0x004A0A2E,
        "385e1d755d8b4e043bcb7440",
    )
    expect_bytes(
        image,
        sections,
        0x004A0A7A,
        "8b46143bc3740f8bc8894610895e14",
    )
    expect_bytes(image, sections, 0x0047666B, "833dc42e030100744e")
    expect_call(image, sections, 0x004766A9, 0x005F9C70)
    expect_bytes(image, sections, 0x004766FE, "f64670407418")
    expect_bytes(image, sections, 0x00472898, "807f2000751ef64670407418")
    expect_utf16(image, sections, 0x00F0F060, "_F_DIE_000")

    return {
        "death_calls": death_calls,
        "chit_calls": chit_calls,
        "death_call_digest": digest_lines(death_calls),
        "chit_call_digest": digest_lines(chit_calls),
    }


def build_prior_claims() -> tuple[
    dict[str, PriorClaim], Mapping[Path, Sequence[Mapping[str, str]]]
]:
    rows_by_path = {path: load_tsv(path) for path in PRIOR_PINS}
    prior = {
        "cl_hit_identity": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-006"),
        "cl_hit_direct_negative": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-012"),
        "cl_actor_entry": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-013"),
        "cl_dying": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-017"),
        "cl_dead": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-018"),
        "cl_dead_animation": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-019"),
        "cl_target_dead": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-020"),
        "cl_panel_refresh": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-022"),
        "cl_arrival_open": select_prior(rows_by_path, COMBAT_PATH, "lifecycle_id", "CL-IMG-025"),
        "gdl_pool": select_prior(rows_by_path, GROUND_PATH, "evidence_id", "GDL-IMG-002"),
        "gdl_dispatch": select_prior(rows_by_path, GROUND_PATH, "evidence_id", "GDL-IMG-003"),
        "gdl_owner": select_prior(rows_by_path, GROUND_PATH, "evidence_id", "GDL-IMG-005"),
        "gdl_create": select_prior(rows_by_path, GROUND_PATH, "evidence_id", "GDL-IMG-006"),
        "gdl_clear": select_prior(rows_by_path, GROUND_PATH, "evidence_id", "GDL-IMG-015"),
        "mcg_runtime": select_prior(rows_by_path, COLOR_PATH, "gate_key", "MCG-IMG-006"),
        "mcg_ready": select_prior(rows_by_path, COLOR_PATH, "gate_key", "MCG-IMG-046"),
        "role_target": select_prior(rows_by_path, ROLE_PATH, "discriminator_id", "RELATION_FALSE_ENEMY_TARGET"),
        "arig_chit": select_prior(rows_by_path, RELATION_PATH, "graph_key", "ARIG-IMG-040"),
        "qme_general": select_prior(rows_by_path, QUEST_EVENT_PATH, "event_key", "QME-IMG-018"),
        "actorattr_r": select_prior(rows_by_path, ATTR_PATH, "field_key", "ActorAttr@0x198.8#R:b0x20000000"),
        "actorattr_w": select_prior(rows_by_path, ATTR_PATH, "field_key", "ActorAttr@0x198.8#W:b0x20000000"),
        "npcattr_r": select_prior(rows_by_path, ATTR_PATH, "field_key", "NPCAttr@0xA8.8#R:b0x00000010"),
        "npcattr_w": select_prior(rows_by_path, ATTR_PATH, "field_key", "NPCAttr@0xA8.8#W:b0x00000010"),
        "factpack_timer": factpack_prior(),
    }
    return prior, rows_by_path


def make_row(
    image: bytes,
    sections: Sequence[Section],
    *,
    delta_id: str,
    row_kind: str,
    phase: str,
    applies_to_class: str,
    predecessor: str,
    successor: str,
    order_relation: str,
    trigger_or_condition: str,
    exact_observation: str,
    semantic_status: str,
    measurement_method: str,
    control: str,
    negative_scope: str,
    primary_span: str,
    support_spans: Sequence[str],
    site_lines: Sequence[str],
    prior_claims: Sequence[PriorClaim],
    nonclaim: str,
    blocker: str,
    required_next_evidence: str,
) -> dict[str, str]:
    spec = SPANS[primary_span]
    _, start, end = span_bytes(image, sections, primary_span)
    prior_reference, prior_artifact_sha, prior_claim_digest = join_prior(prior_claims)
    row = {
        "delta_id": delta_id,
        "row_kind": row_kind,
        "phase": phase,
        "applies_to_class": applies_to_class,
        "predecessor": predecessor,
        "successor": successor,
        "order_relation": order_relation,
        "trigger_or_condition": trigger_or_condition,
        "exact_observation": exact_observation,
        "semantic_status": semantic_status,
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
        "site_list": "||".join(site_lines) if site_lines else "N/A",
        "site_digest": digest_lines(site_lines) if site_lines else "N/A",
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


def build_rows(
    image: bytes,
    sections: Sequence[Section],
    facts: Mapping[str, object],
    prior: Mapping[str, PriorClaim],
) -> list[dict[str, str]]:
    death_calls = list(facts["death_calls"])
    chit_calls = list(facts["chit_calls"])
    rows = [
        make_row(
            image,
            sections,
            delta_id="LT-IMG-001",
            row_kind="INTRA_RESPONSE_ORDER",
            phase="RUNTIME_ACTOR_THEN_TERRAIN",
            applies_to_class="GSCN_RunTimeProtocolRes",
            predecessor="actor entry collection at response+0x1C",
            successor="TerrainThingPool at response+0x20",
            order_relation="CALL_RETURNS_BEFORE_NEXT_CALL",
            trigger_or_condition="both guarded handler lanes are reached in one invocation",
            exact_observation=(
                "Call 0x005E4085 to actor reconcile 0x00446F30 completes before "
                "call 0x005E40D5 to typed terrain bridge 0x005F53A0. Actor/death "
                "reconciliation therefore precedes terrain/drop reconciliation inside "
                "one RuntimeRes handler invocation."
            ),
            semantic_status="PROVEN_EXACT",
            measurement_method="EXACT_FOCUSED_SPAN_AND_REL32_CALL_TARGETS",
            control="two fixed callsites; exclusive focused span hash",
            negative_scope="N/A",
            primary_span="runtime_actor_then_terrain",
            support_spans=("typed_terrain_bridge", "death_sync"),
            site_lines=(
                "0x005E4085->0x00446F30 actor_reconcile",
                "0x005E40D5->0x005F53A0 terrain_bridge",
            ),
            prior_claims=(
                prior["cl_actor_entry"],
                prior["gdl_pool"],
                prior["gdl_dispatch"],
                prior["mcg_runtime"],
            ),
            nonclaim=(
                "This does not prove that the original server co-emitted both optional "
                "fields, used one RuntimeRes, or used any particular cadence."
            ),
            blocker="Original-server lethal-tail emission policy is not present in IMAGE.",
            required_next_evidence=(
                "source-separated original RuntimeRes sequence containing actor and terrain "
                "members, if original packet grouping is required."
            ),
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-002",
            row_kind="BOUNDED_DIRECT_EDGE_NEGATIVE",
            phase="DEATH_SYNC_TO_TYPED_DROP",
            applies_to_class="CNetActor death-sync body",
            predecessor="dead-state synchronization",
            successor="known typed terrain/drop functions",
            order_relation="NO_DIRECT_E8_TARGET_IN_FROZEN_SPAN",
            trigger_or_condition="complete raw E8+rel32 byte-pattern census of death-sync span",
            exact_observation=(
                "The exact death-sync span contains 26 raw E8+rel32 encodings. None targets "
                "0x005F53A0, 0x006AF970, 0x005F41E0, 0x00B0E4A0, 0x00B0EE40, "
                "or 0x006B03F0."
            ),
            semantic_status="PROVEN_EXACT_BOUNDED",
            measurement_method="WHOLE_SPAN_RAW_E8_REL32_CENSUS",
            control=(
                "count=26;ordered_digest="
                + str(facts["death_call_digest"])
                + ";target_set=6"
            ),
            negative_scope=(
                "0x004437C0..0x00443A9A direct E8 encodings versus six pinned typed "
                "terrain/drop targets"
            ),
            primary_span="death_sync",
            support_spans=("typed_terrain_bridge",),
            site_lines=death_calls,
            prior_claims=(
                prior["cl_target_dead"],
                prior["gdl_dispatch"],
                prior["gdl_owner"],
                prior["gdl_create"],
                prior["gdl_clear"],
            ),
            nonclaim=(
                "Indirect, virtual, tail, alias, and transitive paths remain open. This does "
                "not exclude the later terrain lane in the enclosing RuntimeRes handler."
            ),
            blocker="No direct death-to-drop edge exists in the bounded body; transitive ownership remains open.",
            required_next_evidence=(
                "a proved transitive producer chain or original lethal RuntimeRes showing "
                "the terrain member."
            ),
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-003",
            row_kind="TARGET_CLEAR_ORDER",
            phase="DEAD_CURRENT_TARGET",
            applies_to_class="CMyActor current-target state",
            predecessor="reached target subpath after actor+0x30 exclusion guard",
            successor="optional TargetIsDead event to Main_Panel_Target_Enemy_New",
            order_relation="IDENTITY_CLEAR_BEFORE_OPTIONAL_PANEL_EVENT",
            trigger_or_condition=(
                "actor+0x30 guard does not take its exclusion branch; CMyActor singleton "
                "is nonnull; dead actor +0x78/+0x7C equals current-target qword"
            ),
            exact_observation=(
                "On the reached subpath after the actor+0x30 exclusion guard, the death "
                "path requires a nonnull CMyActor singleton and compares the dead actor "
                "qword at +0x78/+0x7C with current target +0xC8/+0xCC. On equality it "
                "pushes qword zero to 0x0043E1D0. It then looks up "
                "Main_Panel_Target_Enemy_New; only a nonnull lookup result constructs "
                "TargetIsDead and invokes vslot +0x210. The clear therefore precedes the "
                "optional panel event."
            ),
            semantic_status="PROVEN_EXACT",
            measurement_method="EXACT_TYPED_OPERAND_AND_CONTROL_FLOW_AUDIT",
            control=(
                "actor+0x30 exclusion branch; fixed singleton global; qword compare; "
                "zero arguments; panel-result null guard; fixed call and literals"
            ),
            negative_scope="N/A",
            primary_span="target_clear_order",
            support_spans=("target_setter", "myactor_singleton_store"),
            site_lines=(
                "0x0044399B actor_plus_0x30_exclusion_guard",
                "0x00443A29->0x0043E1D0 qword_zero_target_setter",
                "0x00443A3F panel_lookup_null_guard",
                "0x00443A78->INDIRECT_VSLOT_0x210 TargetIsDead",
            ),
            prior_claims=(prior["cl_target_dead"], prior["role_target"]),
            nonclaim=(
                "Panel presence, the panel vslot implementation, and original-server "
                "timing are not established by this row."
            ),
            blocker="Original arrival timing of the lethal actor entry remains open.",
            required_next_evidence="original CHitResult and actor-entry arrival order.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-004",
            row_kind="RUNTIME_TARGET_CLEAR",
            phase="CMYACTOR_TARGET_SETTER",
            applies_to_class="CMyActor",
            predecessor="target qword changes",
            successor="CMyActor+0xC8/+0xCC stores new qword",
            order_relation="CONDITIONAL_SIDE_EFFECTS_BEFORE_UNCONDITIONAL_STORE",
            trigger_or_condition=(
                "incoming qword differs from current qword; death call uses CMyActor "
                "singleton with arguments 0,0"
            ),
            exact_observation=(
                "Setter 0x0043E1D0 detaches prior-target side effects only when prior-target "
                "resolution succeeds. On the singleton path it zeros CMyActor +0x408/+0x40C, "
                "and it invokes enemy-panel vslot +0x20C only when panel lookup is nonnull. "
                "The final stores of its two arguments at +0xC8/+0xCC are unconditional on "
                "those two optional operations. Thus the death-path arguments 0,0 are an "
                "actual runtime current-target identity clear."
            ),
            semantic_status="PROVEN_EXACT",
            measurement_method="EXACT_TYPED_SETTER_DATAFLOW",
            control=(
                "fixed CMyActor singleton; prior-target and panel-result null guards; "
                "explicit final object-relative stores"
            ),
            negative_scope="N/A",
            primary_span="target_setter",
            support_spans=("target_clear_order", "myactor_singleton_store"),
            site_lines=(
                "0x0043E204 prior_target_resolution_null_guard",
                "0x0043E254 panel_lookup_null_guard",
                "0x0043E268 final_qword_store",
                "0x00443A29->0x0043E1D0 args=0,0",
            ),
            prior_claims=(prior["role_target"], prior["cl_target_dead"]),
            nonclaim=(
                "Prior-target resolution and panel presence are not assumed. The semantic "
                "name of panel vslot +0x20C is not asserted. The runtime slots are not "
                "serialized ActorAttr or NPCAttr fields."
            ),
            blocker="None for the bounded runtime clear; serialized target-field producers remain separate.",
            required_next_evidence="none for the bounded CMyActor target-clear claim.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-005",
            row_kind="TYPED_FIELD_SEPARATION",
            phase="ACTORATTR_TARGET_QWORD",
            applies_to_class="ActorAttr",
            predecessor="ActorAttr+0x198 qword lifecycle",
            successor="separate CMyActor runtime-target clear",
            order_relation="DISTINCT_TYPED_STORAGE",
            trigger_or_condition="ActorAttr mask +0x1B4 bit 0x20000000 on receive",
            exact_observation=(
                "ActorAttr+0x198 is a separate typed qword: its constructor zeros it, copy "
                "and Merge move it, and the ActorAttr codec reads it under mask "
                "0x20000000. Manual typed-base audit of the death clear and CMyActor setter "
                "finds no ActorAttr+0x198 store there."
            ),
            semantic_status="PROVEN_EXACT_BOUNDED",
            measurement_method="VTABLE_BOUND_TYPED_WRITER_CENSUS_AND_CROSS_SPAN_AUDIT",
            control="ActorAttr vtable slots +0x24/+0x30/+0x34; ctor/copy/Merge/READ spans",
            negative_scope="target-clear and setter spans only; no whole-program arbitrary-alias absence",
            primary_span="actorattr_codec",
            support_spans=(
                "actorattr_vtable",
                "actorattr_ctor_zero",
                "actorattr_copy_field",
                "actorattr_copy",
                "actorattr_merge_field",
                "actorattr_merge",
                "actorattr_receive_field",
                "receive_helper",
                "target_clear_order",
                "target_setter",
            ),
            site_lines=("0x00466B31->0x0089A640 tag=0x32 len=8 field=ActorAttr+0x198",),
            prior_claims=(
                prior["actorattr_r"],
                prior["actorattr_w"],
                prior["cl_target_dead"],
            ),
            nonclaim=(
                "The original nonzero producer and complete concrete owner census remain "
                "open; no global arbitrary-alias absence is claimed."
            ),
            blocker="Original nonzero ActorAttr+0x198 producer is not identified.",
            required_next_evidence="typed original producer or independently varied source-separated observation.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-006",
            row_kind="TYPED_FIELD_SEPARATION",
            phase="NPCATTR_HP_ENEMY_QWORD",
            applies_to_class="NPCAttr",
            predecessor="NPCAttr+0xA8 qword lifecycle",
            successor="separate CMyActor runtime-target clear",
            order_relation="DISTINCT_TYPED_STORAGE",
            trigger_or_condition="NPCAttr mask +0xBC bit 0x10 on receive",
            exact_observation=(
                "NPCAttr+0xA8 is a separate typed qword: its constructor zeros it, copy and "
                "Merge move it, and the NPCAttr codec reads it under mask 0x10. Manual "
                "typed-base audit of the death clear and CMyActor setter finds no "
                "NPCAttr+0xA8 store there."
            ),
            semantic_status="PROVEN_EXACT_BOUNDED",
            measurement_method="VTABLE_BOUND_TYPED_WRITER_CENSUS_AND_CROSS_SPAN_AUDIT",
            control="NPCAttr vtable slots +0x24/+0x30/+0x34; ctor/copy/Merge/READ spans",
            negative_scope="target-clear and setter spans only; no whole-program arbitrary-alias absence",
            primary_span="npcattr_codec",
            support_spans=(
                "npcattr_vtable",
                "npcattr_ctor_zero",
                "npcattr_copy_field",
                "npcattr_copy",
                "npcattr_merge_field",
                "npcattr_merge",
                "npcattr_receive_field",
                "receive_helper",
                "target_clear_order",
                "target_setter",
            ),
            site_lines=("0x00466FF4->0x0089A640 tag=0x32 len=8 field=NPCAttr+0xA8",),
            prior_claims=(
                prior["npcattr_r"],
                prior["npcattr_w"],
                prior["cl_target_dead"],
            ),
            nonclaim=(
                "The original nonzero producer and complete concrete owner census remain "
                "open; no global arbitrary-alias absence is claimed."
            ),
            blocker="Original nonzero NPCAttr+0xA8 producer is not identified.",
            required_next_evidence="typed original producer or independently varied source-separated observation.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-007",
            row_kind="HIT_TARGET_SIDE_EFFECT",
            phase="CHITRESULT_TARGET_STATE",
            applies_to_class="CHitResult handler and CMyActor",
            predecessor="resolved CHitResult target qword",
            successor="target-state setters and TargetEnemyIsFocused panel event",
            order_relation="CONDITIONAL_SIDE_EFFECT_SEQUENCE",
            trigger_or_condition=(
                "target nonnull; CMyActor singleton matches handler actor; saved object "
                "nonnull; saved+0x24 bit 0x40000 set; relation predicate branch"
            ),
            exact_observation=(
                "Under the numeric structural guards, CHitResult calls relation predicate "
                "0x0043C380, compares CHit target +0x18/+0x1C with one of the CMyActor "
                "target qwords, clears old target state, selects setter 0x0043E010 or "
                "0x0043E1D0, applies 0x0043CDA0(0) then 0x0043CDC0(1), and one branch "
                "sends TargetEnemyIsFocused to Main_Panel_Target_Enemy_New with actor "
                "+0x78/+0x7C."
            ),
            semantic_status="PROVEN_EXACT_BOUNDED",
            measurement_method="MANUAL_TYPED_X86_AUDIT_WITH_HASH_AND_CALL_GUARDS",
            control="exact side-effect span; fixed direct targets; exact UTF-16 event/panel literals",
            negative_scope="bounded handler branch only",
            primary_span="chit_target_side_effect",
            support_spans=("chit_handler", "relation_predicate", "target_setter"),
            site_lines=(
                "0x00750AE1->0x0043C380 relation_predicate",
                "0x00750B33->0x0043E010 target_setter_branch_A",
                "0x00750BBC->0x0043E1D0 target_setter_branch_B",
                "0x00750C3E->0x00AA0710 TargetEnemyIsFocused",
            ),
            prior_claims=(
                prior["cl_hit_identity"],
                prior["arig_chit"],
                prior["role_target"],
            ),
            nonclaim=(
                "No gameplay name is assigned to bit 0x40000, predicate polarity, or either "
                "relation branch. This is not an HP write or original-server policy."
            ),
            blocker="Runtime branch choice and original-server CHitResult field policy remain open.",
            required_next_evidence="source-separated original CHitResult instances covering both branches.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-008",
            row_kind="BOUNDED_DIRECT_EDGE_NEGATIVE",
            phase="CHITRESULT_TO_TARGET_PANEL_REFRESH",
            applies_to_class="CHitResult handler",
            predecessor="CHitResult handler",
            successor="known target panel open/name/HP refresh functions",
            order_relation="NO_DIRECT_E8_TARGET_IN_FROZEN_SPAN",
            trigger_or_condition="complete raw E8+rel32 byte-pattern census of full handler",
            exact_observation=(
                "The full handler contains 50 raw E8+rel32 byte-pattern candidates. None "
                "targets 0x0051F150, 0x0051F2F0, 0x0051F920, or 0x0051E890. A separate "
                "manual instruction audit of the same pinned body found no non-stack "
                "+0x44/+0x48 operand."
            ),
            semantic_status="PROVEN_EXACT_BOUNDED",
            measurement_method="WHOLE_SPAN_RAW_E8_CENSUS_PLUS_MANUAL_OPERAND_AUDIT",
            control=(
                "raw_count=50;raw_ordered_digest="
                + str(facts["chit_call_digest"])
                + ";manual_body_instruction_count=585"
            ),
            negative_scope=(
                "0x00750770..0x00750EC0 direct E8 encodings versus four pinned target-panel "
                "functions; non-stack +0x44/+0x48 manual operand audit"
            ),
            primary_span="chit_handler",
            support_spans=("chit_target_side_effect",),
            site_lines=chit_calls,
            prior_claims=(
                prior["cl_hit_direct_negative"],
                prior["cl_panel_refresh"],
                prior["cl_arrival_open"],
            ),
            nonclaim=(
                "Indirect, virtual, alias, and transitive refresh remain open. LT-IMG-007 "
                "proves target-state side effects and is not contradicted by this direct-edge negative."
            ),
            blocker="The observer or transitive route that refreshes name/HP is not bound.",
            required_next_evidence="a proved observer-vector member or transitive call chain to the refresh consumers.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-009",
            row_kind="OBSERVER_BEFORE_DEATH",
            phase="ACTOR_ENTRY_APPLY",
            applies_to_class="known actor entry update",
            predecessor="non-null actor-entry payload",
            successor="death synchronization",
            order_relation="OBSERVER_FANOUT_RETURNS_BEFORE_DEATH_SYNC",
            trigger_or_condition="actor-entry argument +0 is nonzero",
            exact_observation=(
                "The known-actor entry method calls observer fanout 0x005DF080 first and "
                "death sync 0x004437C0 second. The fanout iterates its vector in index order "
                "and invokes observer vslot +0x38 before death predicates and target clear run."
            ),
            semantic_status="PROVEN_EXACT",
            measurement_method="EXACT_REL32_ORDER_AND_FANOUT_BODY",
            control="two ordered direct calls plus exact fanout span",
            negative_scope="N/A",
            primary_span="actor_entry_update",
            support_spans=(
                "observer_fanout",
                "death_sync",
                "observer_dispatcher",
                "observer_wrapper",
            ),
            site_lines=(
                "0x004446FE->0x005DF080 observer_fanout",
                "0x00444705->0x004437C0 death_sync",
            ),
            prior_claims=(
                prior["cl_actor_entry"],
                prior["cl_panel_refresh"],
                prior["cl_arrival_open"],
            ),
            nonclaim=(
                "No proof binds 0x0059D270 or 0x0059D760 as a live member of this fanout "
                "vector. Therefore the exact name/HP observer and CHitResult-versus-actor-entry "
                "arrival order remain unknown."
            ),
            blocker="Observer vector membership and cross-message arrival order are unproved.",
            required_next_evidence="typed observer registration or an original ordered message sequence.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-010",
            row_kind="DEAD_TASK_CONSTRUCTION",
            phase="DEAD_TASK_ENQUEUE",
            applies_to_class="CActorTask_Dead",
            predecessor="reached creation subpath after actor+0x30 exclusion guard",
            successor="actor task manager +0x20 lane",
            order_relation="GUARDED_ALLOCATE_CONSTRUCT_THEN_QUEUE",
            trigger_or_condition=(
                "dead predicate true; actor+0x30 guard does not take its exclusion branch; "
                "0x24-byte allocation succeeds"
            ),
            exact_observation=(
                "On the reached subpath after the actor+0x30 exclusion guard, death sync "
                "requests a 0x24-byte allocation. Only a nonnull allocation is passed to "
                "CActorTask_Dead constructor, which stores vtable 0x00F0F048, clears latch "
                "+0x20, and sets flags 0x80000005. The returned pointer, including null on "
                "allocation failure, is passed to wrapper 0x004843C0; the wrapper returns "
                "immediately on null. For the constructed task, flag 0x40000000 is clear, "
                "so the wrapper selects the owner+0x20 task-manager lane."
            ),
            semantic_status="PROVEN_EXACT",
            measurement_method="CTOR_VTABLE_FLAGS_AND_ORDERED_CALL_CHAIN",
            control=(
                "actor+0x30 exclusion branch; allocator call/result guard; exact ctor bytes; "
                "vtable five dwords; wrapper null and lane branches"
            ),
            negative_scope="N/A",
            primary_span="dead_ctor",
            support_spans=("dead_vtable", "death_sync", "queue_wrapper", "manager_add"),
            site_lines=(
                "0x0044399B actor_plus_0x30_exclusion_guard",
                "0x004439D1->0x00442D50 allocate_0x24",
                "0x004439E2 allocation_result_null_guard",
                "0x004439E9->0x00472810 dead_ctor",
                "0x004439FC->0x004843C0 queue_wrapper",
                "0x004843C4 wrapper_argument_null_guard",
                "0x004843E2->0x004A0C90 manager_plus_0x20",
            ),
            prior_claims=(prior["cl_dead"], prior["cl_dead_animation"]),
            nonclaim=(
                "This does not assert that the actor+0x30 guard passes or allocation succeeds "
                "in a live instance, and does not prove original-server hold time or cadence."
            ),
            blocker="Original timer transition remains open, not task construction.",
            required_next_evidence="none for the bounded guarded construction and queue route.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-011",
            row_kind="TASK_MANAGER_PROGRESS",
            phase="DEAD_TASK_PROMOTION",
            applies_to_class="actor task manager",
            predecessor="mode-0 pending task at manager+0x14",
            successor="current task at +0x10 and start callback",
            order_relation="PENDING_PROMOTION_AFTER_ORDINARY_QUEUE_EMPTY",
            trigger_or_condition=(
                "manager +0x1C/+0x1D/+0x1E clear; current +0x10 null; ordinary linked "
                "queue head +0x04 null; pending +0x14 contains the dead task"
            ),
            exact_observation=(
                "Mode 0 stores the incoming task at pending +0x14. Manager flags +0x1C or "
                "+0x1D defer immediate update; +0x1E destroys an incoming task. Otherwise "
                "manager_add calls queue_update, and with current +0x10 null queue_update "
                "calls promote/start 0x004A09C0. That routine gives the ordinary linked "
                "queue at +0x04 priority; only when +0x04 is empty does it move pending "
                "+0x14 to current +0x10 and invoke its start vslot +0x08. Thus current null "
                "alone is insufficient for immediate dead-task start."
            ),
            semantic_status="PROVEN_EXACT",
            measurement_method="TASK_MANAGER_BRANCH_AND_CALL_CHAIN_AUDIT",
            control=(
                "exact manager/add/update/promote spans; fixed direct calls; +0x04 priority "
                "branch and +0x14-to-+0x10 stores"
            ),
            negative_scope="N/A",
            primary_span="manager_add",
            support_spans=("queue_wrapper", "queue_update", "promote_start", "dead_ctor"),
            site_lines=(
                "0x004A0D6E->0x004A0B50 queue_update",
                "0x004A0B83->0x004A09C0 promote_start_when_current_null",
                "0x004A0A33 ordinary_linked_queue_head_plus_0x04",
                "0x004A0A7A pending_plus_0x14_only_after_queue_empty",
            ),
            prior_claims=(prior["cl_dead"], prior["cl_dead_animation"]),
            nonclaim=(
                "This does not prove that a live actor has all manager flags clear, that "
                "the ordinary +0x04 queue is empty, or that resource readiness is satisfied."
            ),
            blocker="Live task-manager flags, +0x04 queue state, and model readiness are not observed in IMAGE.",
            required_next_evidence="source-separated runtime observation only if live flag state is required.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-012",
            row_kind="EVENT_BEFORE_POSE_GATE",
            phase="DEAD_TASK_START",
            applies_to_class="CActorTask_Dead",
            predecessor="dead-task start",
            successor="_F_DIE_000 pose request",
            order_relation="CONDITIONAL_GENERAL_EVENT_BEFORE_MODEL_BIT_TEST",
            trigger_or_condition=(
                "dead-task start has a valid actor; CMyActor singleton at 0x01032EC4 is nonnull"
            ),
            exact_observation=(
                "CActorTask_Dead start tests the CMyActor singleton. When it is nonnull, the "
                "task calls general dispatcher 0x005F9C70 before testing actor+0x70 bit "
                "0x40 and before requesting _F_DIE_000. When the singleton is null, the "
                "dispatcher block is skipped, but control continues to the later actor/model "
                "checks and pose bit gate."
            ),
            semantic_status="PROVEN_EXACT",
            measurement_method="ORDERED_CONTROL_FLOW_AND_GENERAL_DISPATCH_BINDING",
            control=(
                "exact singleton null branch; fixed direct dispatcher call precedes exact "
                "bit-test and UTF-16 pose literal"
            ),
            negative_scope="N/A",
            primary_span="dead_start",
            support_spans=("die_literal",),
            site_lines=(
                "0x0047666B CMyActor_singleton_null_guard",
                "0x004766A9->0x005F9C70 before_bit_test_at_0x004766FE",
                "0x004766C2 singleton_null_join_before_pose_checks",
            ),
            prior_claims=(prior["cl_dead_animation"], prior["qme_general"]),
            nonclaim=(
                "The live listener set and exact visible message are not identified. Event "
                "dispatch is not guaranteed when the singleton is null, and is not proof "
                "that a particular UI announcement appears."
            ),
            blocker="Live general-listener membership is unmeasured.",
            required_next_evidence="typed listener registration only if the visible announcement must be named.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-013",
            row_kind="MODEL_READINESS_GATE",
            phase="DEAD_POSE_START_AND_RETRY",
            applies_to_class="CActorTask_Dead with CNetNPC actor",
            predecessor="dead-task start or update",
            successor="_F_DIE_000 behavior request",
            order_relation="POSE_REQUIRES_ACTOR_STATE_BIT_0x40",
            trigger_or_condition="actor+0x70 bit 0x40 set and task latch +0x20 clear",
            exact_observation=(
                "Both dead-task start and update gate _F_DIE_000 on actor+0x70 bit 0x40; "
                "update retries while latch +0x20 is clear. The separately pinned CNetNPC "
                "model callback sets bit 0x40 only after its callback/resource gates complete."
            ),
            semantic_status="PROVEN_EXACT",
            measurement_method="TWO_TASK_METHODS_PLUS_TYPED_BIT_PRODUCER",
            control="dead vtable; start/update bit tests; pose literal; pinned CNetNPC callback",
            negative_scope="N/A",
            primary_span="dead_start",
            support_spans=(
                "dead_update",
                "dead_vtable",
                "die_literal",
                "cnetnpc_model_callback_gate",
            ),
            site_lines=(
                "0x004766FE actor+0x70 bit0x40 start_gate",
                "0x0047289E actor+0x70 bit0x40 update_retry_gate",
            ),
            prior_claims=(prior["cl_dead_animation"], prior["mcg_ready"]),
            nonclaim=(
                "IMAGE proves conditional callback and task bodies, not that a live model "
                "request schedules or completes the callback before the lethal update."
            ),
            blocker="Live model callback completion relative to lethal actor-entry arrival is unmeasured.",
            required_next_evidence="source-separated model-ready/task trace if live scheduling must be proved.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-014",
            row_kind="DEAD_TASK_PERSISTENCE",
            phase="DEAD_TASK_UPDATE",
            applies_to_class="CActorTask_Dead",
            predecessor="actor dead predicate remains true",
            successor="task remains active",
            order_relation="NO_TASK_COMPLETE_BIT_WHILE_ISDEAD_TRUE",
            trigger_or_condition="actor exists and vslot +0x3C returns true",
            exact_observation=(
                "When the actor dead predicate remains true, dead-task update can request "
                "the pose and run its per-frame helpers without setting task flag bit 0x08. "
                "When the predicate becomes false or the actor is unavailable, it ORs bit "
                "0x08 to complete the task. The bounded update body performs no actor-map erase."
            ),
            semantic_status="PROVEN_EXACT_BOUNDED",
            measurement_method="EXACT_UPDATE_BRANCH_AND_LOCAL_SIDE_EFFECT_AUDIT",
            control="dead-update full span; IsDead virtual slot; task flag +0x10 bit0x08",
            negative_scope="CActorTask_Dead update body only",
            primary_span="dead_update",
            support_spans=("dead_vtable", "dead_predicate", "die_literal"),
            site_lines=(),
            prior_claims=(prior["cl_dead"], prior["cl_dead_animation"]),
            nonclaim=(
                "Actor removal may occur in another reconciliation or world path. This row "
                "does not define authentic corpse lifetime or despawn policy."
            ),
            blocker="Authentic actor removal/despawn carrier and timing remain open.",
            required_next_evidence="original actor omission/removal sequence or a proved transitive removal path.",
        ),
        make_row(
            image,
            sections,
            delta_id="LT-IMG-015",
            row_kind="TIMER_AUTHORITY_BOUNDARY",
            phase="DYING_TO_DEAD_TIMER",
            applies_to_class="BasicAttr on audited actor path",
            predecessor="HP zero and BasicAttr+0x58 greater than zero",
            successor="HP zero and BasicAttr+0x58 less than or equal to zero",
            order_relation="LATER_FIELD_SNAPSHOT_REQUIRED_ON_PROVED_PATH",
            trigger_or_condition="mutually exclusive dying/dead predicates",
            exact_observation=(
                "The pinned R102 IMAGE census found the bounded BasicAttr+0x58 writers to be "
                "constructor, copy, Merge, and wire load, with zero local frame-delta "
                "decrementers. Combined with the mutually exclusive timer>0 DYING and "
                "timer<=0 DEAD predicates, the proved path needs a later write/snapshot to "
                "cross the boundary; IMAGE does not determine original hold duration."
            ),
            semantic_status="PARTIAL",
            measurement_method="PINNED_PRIOR_WRITER_CENSUS_PLUS_EXACT_PREDICATE_SYNTHESIS",
            control="FACTPACK R102 exact hash/markers; dying/dead predicate and BasicAttr codec spans",
            negative_scope="bounded known BasicAttr writer census; arbitrary alias writers are not globally excluded",
            primary_span="dead_predicate",
            support_spans=("dying_predicate", "basicattr_codec", "death_sync"),
            site_lines=(),
            prior_claims=(prior["factpack_timer"], prior["cl_dying"], prior["cl_dead"]),
            nonclaim=(
                "This does not prove the original server used two packets, a particular timer "
                "value, or any hold duration. A still-unidentified aliased writer remains possible."
            ),
            blocker=(
                "No eligible original actor-entry sequence is supplied or established by "
                "the cited inputs."
            ),
            required_next_evidence=(
                "a source-separated original lethal actor-entry sequence with timer values "
                "and arrival times."
            ),
        ),
    ]
    return rows


KEY_COLUMNS = {
    COMBAT_PATH: "lifecycle_id",
    GROUND_PATH: "evidence_id",
    COLOR_PATH: "gate_key",
    ROLE_PATH: "discriminator_id",
    RELATION_PATH: "graph_key",
    QUEST_EVENT_PATH: "event_key",
    ATTR_PATH: "field_key",
}


def prior_triplets(
    rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]],
) -> set[tuple[str, str, str]]:
    result: set[tuple[str, str, str]] = set()
    for path, rows in rows_by_path.items():
        key_column = KEY_COLUMNS[path]
        artifact_sha = PRIOR_PINS[path][1]
        for row in rows:
            key = row.get(key_column, "")
            if not key:
                continue
            suffix = f"@{row.get('evidence_key', '')}" if row.get("evidence_key") else ""
            result.add(
                (
                    f"{path.name}:{key}{suffix}",
                    artifact_sha,
                    prior_row_digest(row),
                )
            )
    timer = factpack_prior()
    result.add((timer.token, timer.artifact_sha256, timer.claim_digest))
    return result


def validate_rows(
    rows: Sequence[Mapping[str, str]],
    rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]],
) -> None:
    if tuple(row.get("delta_id", "") for row in rows) != EXPECTED_IDS:
        raise ValueError("ordered delta-id set mismatch")
    if tuple(row.get("row_kind", "") for row in rows) != EXPECTED_KINDS:
        raise ValueError("ordered row-kind set mismatch")
    if tuple(row.get("semantic_status", "") for row in rows) != EXPECTED_STATUSES:
        raise ValueError("ordered semantic-status set mismatch")
    if any(tuple(row.keys()) != FIELDNAMES for row in rows):
        raise ValueError("row field set/order mismatch")
    if any(row["source"] != SOURCE for row in rows):
        raise ValueError("every row must have source=IMAGE")
    if any(row["source_file"] != SOURCE_FILE for row in rows):
        raise ValueError("source-file pin mismatch")
    if any(row["source_size"] != str(IMAGE_SIZE) for row in rows):
        raise ValueError("source-size pin mismatch")
    if any(row["source_sha256"] != IMAGE_SHA256 for row in rows):
        raise ValueError("source-hash pin mismatch")
    if any(not row["required_next_evidence"].startswith("PROPOSED: ") for row in rows):
        raise ValueError("required-next-evidence label missing")
    if any(row["delta_id"].startswith("CL-") for row in rows):
        raise ValueError("canonical PF_COMBAT_LIFECYCLE row copied into delta")

    claims = [row["claim_sha256"] for row in rows]
    evidence = [row["evidence_key"] for row in rows]
    if len(set(claims)) != len(rows):
        raise ValueError("duplicate delta claim_sha256")
    if len(set(evidence)) != len(rows):
        raise ValueError("duplicate delta evidence_key")

    valid_prior = prior_triplets(rows_by_path)
    prior_claims = {triplet[2] for triplet in valid_prior}
    prior_evidence = {
        row.get("evidence_key", "")
        for prior_rows in rows_by_path.values()
        for row in prior_rows
        if row.get("evidence_key")
    }
    if set(claims).intersection(prior_claims):
        raise ValueError("delta duplicates a prior canonical claim digest")
    if set(evidence).intersection(prior_evidence):
        raise ValueError("delta duplicates a prior canonical evidence key")

    for row in rows:
        claim_fields = {
            key: value
            for key, value in row.items()
            if key not in {"claim_sha256", "evidence_key"}
        }
        if row["claim_sha256"] != canonical_row_digest(claim_fields):
            raise ValueError(f"claim digest mismatch: {row['delta_id']}")
        expected_evidence = sha256(
            ROW_DOMAIN
            + row["claim_sha256"].encode("ascii")
            + b"\x00"
            + row["span_sha256"].encode("ascii")
            + b"\x00"
            + IMAGE_SHA256.encode("ascii")
        )
        if row["evidence_key"] != expected_evidence:
            raise ValueError(f"evidence-key mismatch: {row['delta_id']}")

        count = int(row["site_count"])
        if count:
            sites = row["site_list"].split("||")
            if len(sites) != count or row["site_digest"] != digest_lines(sites):
                raise ValueError(f"site census mismatch: {row['delta_id']}")
        elif row["site_list"] != "N/A" or row["site_digest"] != "N/A":
            raise ValueError(f"empty-site encoding mismatch: {row['delta_id']}")

        tokens = row["prior_reference"].split(";")
        artifact_hashes = row["prior_artifact_sha256"].split(";")
        claim_hashes = row["prior_claim_digest"].split(";")
        if not (len(tokens) == len(artifact_hashes) == len(claim_hashes)):
            raise ValueError(f"prior tuple width mismatch: {row['delta_id']}")
        if any(
            triplet not in valid_prior
            for triplet in zip(tokens, artifact_hashes, claim_hashes)
        ):
            raise ValueError(f"prior tuple pin mismatch: {row['delta_id']}")


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
    return stream.getvalue().encode("utf-8")


def claim_set_digest(rows: Sequence[Mapping[str, str]]) -> str:
    return digest_lines(
        [
            f"{row['delta_id']}:{row['claim_sha256']}:{row['evidence_key']}"
            for row in rows
        ]
    )


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_report(rows: Sequence[Mapping[str, str]], tsv: bytes) -> bytes:
    lines = [
        "# PF combat lethal-tail delta (IMAGE only)",
        "",
        "This is a delta-only re-derivation over pinned canonical artifacts. It does not copy ",
        "or replace any `PF_COMBAT_LIFECYCLE.tsv` row. Every delta row cites one or more ",
        "prior rows by exact row identity, prior artifact SHA-256, and prior claim digest.",
        "",
        "## Result",
        "",
        f"- Rows: {len(rows)}/{len(EXPECTED_IDS)}; every row has `source=IMAGE`.",
        f"- IMAGE: `{SOURCE_FILE}`, size `{IMAGE_SIZE}`, SHA-256 `{IMAGE_SHA256}`.",
        f"- TSV SHA-256: `{sha256(tsv)}`.",
        f"- Ordered claim-set SHA-256: `{claim_set_digest(rows)}`.",
        "- Publication unit: TSV + Markdown, with the pair marker published last.",
        "",
        "## New bounded claims",
        "",
        "| delta_id | kind | status | exact bounded result | blocker |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                md_cell(row[column])
                for column in (
                    "delta_id",
                    "row_kind",
                    "semantic_status",
                    "exact_observation",
                    "blocker",
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Closures added by this delta",
            "",
            "- Within one RuntimeRes handler invocation, actor/death reconciliation returns before the typed terrain/drop lane is called.",
            "- The death-sync body has no direct E8 edge to the six pinned typed terrain/drop functions; indirect and transitive paths stay open.",
            "- On the reached guarded subpath, a dead actor that is the current CMyActor target is cleared before the optional `TargetIsDead` panel event; a null panel lookup suppresses the event, not the clear.",
            "- CMyActor current-target storage is distinct from the typed ActorAttr+0x198 and NPCAttr+0xA8 qwords; their original nonzero producers remain open.",
            "- CHitResult has bounded target-state side effects, but no direct edge to the four pinned name/HP/open refresh consumers in its full handler.",
            "- Actor-entry observer fanout returns before death sync; observer membership and cross-message arrival order remain unknown.",
            "- Dead-task construction requires the actor+0x30 exclusion guard to pass and allocation to succeed; a null allocation reaches the null-safe wrapper without construction.",
            "- Pending dead-task promotion requires current +0x10 null and the higher-priority ordinary linked queue +0x04 empty; current null alone is insufficient.",
            "- The general event precedes the pose gate only when the CMyActor singleton is nonnull; a null singleton skips that dispatcher block while the later pose path continues.",
            "- The dead task retries the pose behind model bit 0x40 and remains active while IsDead is true.",
            "- The timer boundary still has no proved local decrementer in the pinned R102 writer census; no eligible original actor-entry sequence is supplied or established by the cited inputs, so original hold duration and emission policy remain unknown.",
            "",
            "## Critical nonclaims",
            "",
            "- No claim is made about original-server co-emission, packet cadence, timer value, or hold duration.",
            "- No claim binds the pinned dispatcher/wrapper as a member of the actor-entry observer vector.",
            "- CHitResult-versus-actor-entry arrival order remains UNKNOWN.",
            "- Actor removal, authentic corpse duration, terrain omission, and drop creation ownership remain open.",
            "- The original nonzero producers for ActorAttr+0x198 and NPCAttr+0xA8 remain open; no whole-program arbitrary-alias absence is claimed.",
            "- Direct-edge negatives do not exclude indirect, virtual, tail, alias, or transitive paths.",
            "- The semantic names of bit 0x40000, the relation predicate polarity, and panel vslots are not guessed.",
            "- `CFightMsgVital` was deliberately not followed in this bounded delta.",
            "- No current replacement-server code/runtime/capture/dump was used as evidence in these IMAGE rows or read by this generator.",
            "",
            "## Prior canonical pins",
            "",
        ]
    )
    for path in sorted(PRIOR_PINS, key=lambda item: item.name):
        lines.append(f"- `{path.name}`: `{PRIOR_PINS[path][1]}`")
    lines.extend(
        [
            f"- `{FACTPACK_PATH.name}`: `{FACTPACK_SHA256}`",
            "",
            "## Evidence keys",
            "",
        ]
    )
    for row in rows:
        lines.append(f"- `{row['delta_id']}`: `{row['evidence_key']}`")
    lines.extend(
        [
            "",
            "## Deterministic verification",
            "",
            "```powershell",
            "py -3 pf_rederive_combat_lethal_tail_delta.py --check",
            "py -3 pf_rederive_combat_lethal_tail_delta.py --self-test",
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
    rows: Sequence[Mapping[str, str]], tsv: bytes, report: bytes
) -> dict[str, object]:
    return {
        "schema": "PF_COMBAT_LETHAL_TAIL_DELTA_PAIR_V1",
        "generation_sha256": generation_digest(tsv, report),
        "row_count": len(rows),
        "source_counts": {"IMAGE": len(rows)},
        "delta_ids": [row["delta_id"] for row in rows],
        "claim_set_sha256": claim_set_digest(rows),
        "image": {
            "path": SOURCE_FILE,
            "size": IMAGE_SIZE,
            "sha256": IMAGE_SHA256,
        },
        "files": {
            TSV_PATH.name: {"size": len(tsv), "sha256": sha256(tsv)},
            REPORT_PATH.name: {"size": len(report), "sha256": sha256(report)},
        },
        "publication_order": [TSV_PATH.name, REPORT_PATH.name, PAIR_PATH.name],
        "marker_published_last": True,
    }


def render_pair(
    rows: Sequence[Mapping[str, str]], tsv: bytes, report: bytes
) -> bytes:
    return (
        json.dumps(
            pair_payload(rows, tsv, report),
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("ascii")


def validate_rendered(
    rows: Sequence[Mapping[str, str]],
    rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]],
    tsv: bytes,
    report: bytes,
    pair: bytes,
) -> None:
    validate_rows(rows, rows_by_path)
    reader = csv.DictReader(io.StringIO(tsv.decode("utf-8"), newline=""), delimiter="\t")
    parsed = list(reader)
    if tuple(reader.fieldnames or ()) != FIELDNAMES or parsed != list(rows):
        raise ValueError("rendered TSV differs from validated rows")

    text = report.decode("utf-8")
    required = (
        f"Rows: {len(rows)}/{len(EXPECTED_IDS)}; every row has `source=IMAGE`.",
        f"TSV SHA-256: `{sha256(tsv)}`.",
        f"Ordered claim-set SHA-256: `{claim_set_digest(rows)}`.",
        "CHitResult-versus-actor-entry arrival order remains UNKNOWN.",
        "`CFightMsgVital` was deliberately not followed",
        "No current replacement-server code/runtime/capture/dump was used as evidence in these IMAGE rows or read by this generator.",
    )
    if any(fragment not in text for fragment in required):
        raise ValueError("rendered report integrity wording missing")
    for row in rows:
        if f"- `{row['delta_id']}`: `{row['evidence_key']}`" not in text:
            raise ValueError(f"report evidence row missing: {row['delta_id']}")

    parsed_pair = json.loads(pair.decode("ascii"))
    if parsed_pair != pair_payload(rows, tsv, report):
        raise ValueError("pair marker content mismatch")
    if pair != render_pair(rows, tsv, report):
        raise ValueError("pair marker is not canonical deterministic JSON")


def assert_no_lock_or_debris(*, allow_current_lock: bool) -> None:
    if not allow_current_lock and LOCK_PATH.exists():
        raise ValueError(f"publisher lock present: {LOCK_PATH.name}")
    debris = [
        path.name
        for path in OUT_DIR.iterdir()
        if path.is_file() and path.name.startswith(STAGE_PREFIXES)
    ]
    if debris:
        raise ValueError("staged publication debris present: " + ",".join(sorted(debris)))


def acquire_lock() -> int:
    try:
        fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError(f"publisher lock already exists: {LOCK_PATH.name}") from exc
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


def stage_file(destination: Path, content: bytes) -> Path:
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.staged")
    fd: int | None = None
    try:
        fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as handle:
            fd = None
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if temporary.read_bytes() != content:
            raise ValueError(f"staged-file verification failed: {destination.name}")
        return temporary
    except Exception:
        if fd is not None:
            os.close(fd)
        temporary.unlink(missing_ok=True)
        raise


def stable_installed_read() -> tuple[bytes, bytes, bytes]:
    if not PAIR_PATH.is_file():
        raise ValueError(f"missing output: {PAIR_PATH.name}")
    marker_before = PAIR_PATH.read_bytes()
    if not TSV_PATH.is_file() or not REPORT_PATH.is_file():
        raise ValueError("paired output missing")
    tsv = TSV_PATH.read_bytes()
    report = REPORT_PATH.read_bytes()
    marker_after = PAIR_PATH.read_bytes()
    if marker_before != marker_after:
        raise ValueError("pair marker changed during stable read")
    return tsv, report, marker_after


def check_installed(
    rows: Sequence[Mapping[str, str]],
    rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]],
    expected_tsv: bytes,
    expected_report: bytes,
    expected_pair: bytes,
) -> None:
    actual_tsv, actual_report, actual_pair = stable_installed_read()
    if actual_tsv != expected_tsv:
        raise ValueError("installed TSV differs from deterministic re-derivation")
    if actual_report != expected_report:
        raise ValueError("installed report differs from deterministic re-derivation")
    if actual_pair != expected_pair:
        raise ValueError("installed pair marker differs from deterministic re-derivation")
    validate_rendered(rows, rows_by_path, actual_tsv, actual_report, actual_pair)


def derive_all() -> tuple[
    bytes,
    list[dict[str, str]],
    Mapping[Path, Sequence[Mapping[str, str]]],
    bytes,
    bytes,
    bytes,
]:
    image = read_pinned(IMAGE_PATH, IMAGE_SIZE, IMAGE_SHA256)
    sections = parse_pe(image)
    facts = verify_static_anchors(image, sections)
    prior, rows_by_path = build_prior_claims()
    rows = build_rows(image, sections, facts, prior)
    validate_rows(rows, rows_by_path)
    tsv = render_tsv(rows)
    report = render_report(rows, tsv)
    pair = render_pair(rows, tsv, report)
    validate_rendered(rows, rows_by_path, tsv, report, pair)
    return image, rows, rows_by_path, tsv, report, pair


def verify_image_unchanged(before: bytes) -> None:
    after = read_pinned(IMAGE_PATH, IMAGE_SIZE, IMAGE_SHA256)
    if after != before:
        raise ValueError("IMAGE changed during re-derivation")


def expect_validation_failure(
    rows: Sequence[Mapping[str, str]],
    rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]],
    expected_fragment: str,
) -> None:
    try:
        validate_rows(rows, rows_by_path)
    except ValueError as exc:
        if expected_fragment not in str(exc):
            raise ValueError(
                f"self-test failed with wrong guard: expected={expected_fragment} actual={exc}"
            ) from exc
    else:
        raise ValueError(f"self-test mutation survived: {expected_fragment}")


def run_self_test(
    rows: Sequence[Mapping[str, str]],
    rows_by_path: Mapping[Path, Sequence[Mapping[str, str]]],
    tsv: bytes,
    report: bytes,
    pair: bytes,
) -> int:
    cases = 0

    mutated = [dict(row) for row in rows]
    mutated[0]["source"] = "DUMP"
    expect_validation_failure(mutated, rows_by_path, "source=IMAGE")
    cases += 1

    mutated = [dict(row) for row in rows]
    mutated[0]["row_kind"] = "OTHER"
    expect_validation_failure(mutated, rows_by_path, "row-kind")
    cases += 1

    mutated = [dict(row) for row in rows]
    mutated[1]["claim_sha256"] = mutated[0]["claim_sha256"]
    mutated[1]["evidence_key"] = mutated[0]["evidence_key"]
    expect_validation_failure(mutated, rows_by_path, "duplicate delta claim")
    cases += 1

    mutated = [dict(row) for row in rows]
    mutated[0]["prior_claim_digest"] = "0" * 64
    expect_validation_failure(mutated, rows_by_path, "claim digest mismatch")
    cases += 1

    expect_validation_failure(list(rows[:-1]), rows_by_path, "delta-id set")
    cases += 1

    mutated = [dict(row) for row in rows]
    mutated[0]["site_list"] += "||0x00000000->0x00000000"
    expect_validation_failure(mutated, rows_by_path, "claim digest mismatch")
    cases += 1

    altered_pair = bytearray(pair)
    altered_pair[-2] = ord(" ")
    try:
        validate_rendered(rows, rows_by_path, tsv, report, bytes(altered_pair))
    except (ValueError, json.JSONDecodeError):
        cases += 1
    else:
        raise ValueError("self-test pair mutation survived")

    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    lock_fd: int | None = None
    staged: dict[Path, Path] = {}
    if args.check or args.self_test:
        assert_no_lock_or_debris(allow_current_lock=False)
    else:
        lock_fd = acquire_lock()  # O_EXCL publisher lock precedes IMAGE read.
        assert_no_lock_or_debris(allow_current_lock=True)

    try:
        image, rows, rows_by_path, tsv, report, pair = derive_all()
        if args.self_test:
            mutation_cases = run_self_test(rows, rows_by_path, tsv, report, pair)
            mode_name = "self-test"
        elif args.check:
            check_installed(rows, rows_by_path, tsv, report, pair)
            mutation_cases = 0
            mode_name = "check"
        else:
            staged[TSV_PATH] = stage_file(TSV_PATH, tsv)
            staged[REPORT_PATH] = stage_file(REPORT_PATH, report)
            staged[PAIR_PATH] = stage_file(PAIR_PATH, pair)
            validate_rendered(
                rows,
                rows_by_path,
                staged[TSV_PATH].read_bytes(),
                staged[REPORT_PATH].read_bytes(),
                staged[PAIR_PATH].read_bytes(),
            )
            verify_image_unchanged(image)
            os.replace(staged[TSV_PATH], TSV_PATH)
            os.replace(staged[REPORT_PATH], REPORT_PATH)
            os.replace(staged[PAIR_PATH], PAIR_PATH)  # marker is last
            check_installed(rows, rows_by_path, tsv, report, pair)
            mutation_cases = 0
            mode_name = "publish"
        verify_image_unchanged(image)
        result_lines = (
            f"mode={mode_name}",
            f"rows={len(rows)}",
            f"source_IMAGE_rows={sum(row['source'] == SOURCE for row in rows)}",
            f"claim_set_sha256={claim_set_digest(rows)}",
            f"image_size={len(image)}",
            f"image_sha256={sha256(image)}",
            f"tsv_size={len(tsv)}",
            f"tsv_sha256={sha256(tsv)}",
            f"md_size={len(report)}",
            f"md_sha256={sha256(report)}",
            f"pair_size={len(pair)}",
            f"pair_sha256={sha256(pair)}",
            f"generation_sha256={generation_digest(tsv, report)}",
            f"self_test_mutation_cases={mutation_cases}",
        )
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)
        if lock_fd is not None:
            release_lock(lock_fd)

    for line in result_lines:
        print(line)
    print("status=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        safe = str(exc).encode("ascii", "backslashreplace").decode("ascii")
        print(f"status=FAIL error={type(exc).__name__}: {safe}", file=sys.stderr)
        raise SystemExit(1)
