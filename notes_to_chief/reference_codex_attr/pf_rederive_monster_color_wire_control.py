#!/usr/bin/env python3
"""Re-derive the bounded CNetNPC name-color wire/control census.

This script reads the frozen GameClient.local.bin image plus pinned, IMAGE-derived
reference TSVs for provenance joins.  It writes the paired TSV/Markdown artifacts
beside itself, or verifies them with --check.  The console output is deliberately
ASCII-only.
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
TSV_PATH = OUT_DIR / "PF_MONSTER_COLOR_WIRE_CONTROL.tsv"
REPORT_PATH = OUT_DIR / "PF_MONSTER_COLOR_WIRE_CONTROL.md"
REFERENCE_GATE_PATH = OUT_DIR / "PF_MONSTER_COLOR_GATE.tsv"
SERIALIZER_FIELDS_PATH = OUT_DIR / "PF_SERIALIZER_FIELDS.tsv"
ATTR_SELECTOR_PATH = OUT_DIR / "PF_ATTR_NAME_COLOR_SELECTOR.tsv"
ATTR_SEMANTICS_PATH = OUT_DIR / "PF_ATTR_FIELD_SEMANTICS.tsv"
COMBAT_LIFECYCLE_PATH = OUT_DIR / "PF_COMBAT_LIFECYCLE.tsv"
LOCK_PATH = OUT_DIR / ".pf_rederive_monster_color_wire_control.lock"

EXPECTED_IMAGE_SIZE = 14_759_424
EXPECTED_IMAGE_SHA256 = (
    "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
)
SOURCE_FILE = "PF_ROOT://GameClient/GameClient.local.bin"
SOURCE = "IMAGE"
DIRECT_STYLE_WIRE_ROW_KIND = "SERVER_CONTROLLABLE_DIRECT_STYLE_WIRE_FIELD"

WRITE_PRIMITIVE = 0x0089A600
READ_PRIMITIVE = 0x0089A640
COLOR_SELECTOR = 0x00443F50
CONTROLLER_STYLE_STORE = 0x009F1A70
UI_STYLE_SETTER = 0x00AA37D0
STYLE_PROPERTY_PARSER = 0x00A9DAE0
FONTSTYLE_ID_LITERAL = 0x00F8A4DC
EMBEDDED_STYLE_LITERAL = 0x00F89FB8

EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
PAIR_PLACEHOLDER = "0" * 64
EXPECTED_SERIALIZER_FIELDS_SIZE = 25_195_473
EXPECTED_SERIALIZER_FIELDS_SHA256 = (
    "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
)
EXPECTED_GATE_SIZE = 110_234
EXPECTED_GATE_SHA256 = (
    "8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0"
)
EXPECTED_ATTR_SELECTOR_SIZE = 37_350
EXPECTED_ATTR_SELECTOR_SHA256 = (
    "d15864a21a7a124a23f6dffad174a55d376045a25a04814bbe6dc5f5632af82d"
)
EXPECTED_ATTR_SEMANTICS_SIZE = 1_339_980
EXPECTED_ATTR_SEMANTICS_SHA256 = (
    "1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f"
)
EXPECTED_COMBAT_LIFECYCLE_SIZE = 41_063
EXPECTED_COMBAT_LIFECYCLE_SHA256 = (
    "305b7bdc12e9b638e3c3f37f996af8bb0e2d1877241aaf171885b8fae106b658"
)


@dataclass(frozen=True)
class Section:
    name: str
    va: int
    file_off: int
    mapped_len: int
    virtual_size: int
    raw_size: int


FIELDNAMES = (
    "control_key",
    "row_kind",
    "control_surface",
    "carrier_or_local_source",
    "wire_direction",
    "object_offset",
    "wire_tag",
    "wire_len",
    "presence_gate",
    "producer_va",
    "consumer_va",
    "condition",
    "exact_observation",
    "server_control_level",
    "semantic_status",
    "census_scope",
    "census_count",
    "census_digest",
    "span_start_va",
    "span_end_va",
    "file_off_start",
    "file_off_end",
    "span_sha256",
    "support_spans",
    "reference_keys",
    "source",
    "source_file",
    "source_sha256",
    "nonclaim",
    "blocker",
    "required_next_evidence",
    "artifact_pair_sha256",
    "claim_sha256",
    "evidence_key",
)


# End addresses are exclusive.  These hashes are the immutable manual-analysis
# anchors.  The generator re-measures every span from the image.
SPANS = {
    "runtime_actor_entry_codec": (
        0x005E21D0,
        0x005E23B5,
        "44efb796eb00d2fcc6b07783dd101d172b8a2a230f85c490611cc46aa3a8d067",
    ),
    "basicattr_codec": (
        0x004656F0,
        0x00465983,
        "d0c15b74a36077df30a0e60dbeb8441e878c08b82587c1ea55365ab2ebd70020",
    ),
    "actorattr_codec": (
        0x00466230,
        0x00466C6F,
        "ff1bf8f6b8beb33d6c070d4bbb2d37f8d83aaa93545a38397bf58f8acf72a5ed",
    ),
    "npcattr_codec": (
        0x00466EB0,
        0x0046702D,
        "da9a2c2a30f4d131d0d3018a9daaa1b4a97bdd2b41145ff6d607a3baa29253ff",
    ),
    "relation_predicate": (
        0x0043C380,
        0x0043C63C,
        "1d99f8557252742914c4f7358853aac06f0b54603f78a4b4d073aaea2afcbd89",
    ),
    "color_selector": (
        0x00443F50,
        0x004443C5,
        "ee845ee6ef6337ea41ae57a5a4df8af5a8a8ac00e458ea1ce3e587aff1f9cdf9",
    ),
    "controller_style_store": (
        0x009F1A70,
        0x009F1A7A,
        "6d731f768f8834c3595c479205dc6991ea8b4b940958f6be330f60aa9373eef1",
    ),
    "npc_label_sink": (
        0x005BDA47,
        0x005BDA95,
        "f9e3b664c61f6350eae791d53192f3ba5df3bd3f627e0684696416865bc5a837",
    ),
    "style_property_parser": (
        0x00A9DAE0,
        0x00A9DD9B,
        "5f974da52ed482920db7a92285d6e61e6a40594d864a6d659791054db46525ef",
    ),
    "label_property_parser": (
        0x00AA488F,
        0x00AA4929,
        "a1f7e93fbd3fd7854a3d7a61242fe3e6c529f71302d90fe0043c34cb541c9c7f",
    ),
    "ui_style_forwarder_1": (
        0x00AB97F0,
        0x00AB9816,
        "abe9496bbb8e1c36d17601ff5f5d9ead2baa676560d7421fe8f728ab3b4c4626",
    ),
    "ui_style_forwarder_2": (
        0x00AB9D40,
        0x00AB9DBE,
        "7c81089be18717a530a95aee3612abe1ccb99278b8436a2b9f66d71b96a7f268",
    ),
    "hit_result_codec": (
        0x00750040,
        0x00750102,
        "ed2ec097d66c3420c3a41d34a517b0630e69fe99a3ca6c2a2f5949661daa6036",
    ),
    "missile_hit_result_codec": (
        0x00750110,
        0x0075022D,
        "9b75ee635320336594e91052b9cd5de651f89ff6898c620e39b806a6401011cf",
    ),
    "hit_vector_write_codec": (
        0x0074F5A0,
        0x0074F6CC,
        "cba53fdadf9e9446bd42ac2b6e6a24842cdac88c11dcee2999586a1f5660e922",
    ),
    "hit_vector_read_codec": (
        0x0074FF60,
        0x00750032,
        "741e938a518b4a4ce7b3b8275a9d5fe3dd7fcc785abb5d3b86b578596cbb01bb",
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
    "common_actor_ctor": (
        0x00443180,
        0x00443450,
        "274a44e8b1ac932c548cbe10b9144696e988d9b1e8eb9c640322e2fe80f10a31",
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
    "death_predicate": (
        0x0043BD70,
        0x0043BD9D,
        "1df3c62b4bbe0aab1ebf1404320a7b2466ef20390db060e67ba183a1178127aa",
    ),
}


EXPECTED_E8_CENSUS = {
    WRITE_PRIMITIVE: (
        1350,
        "88ddff5cd217b6db25fb757e381b02b8af75666aa5e70278ca972acfbb85f09a",
    ),
    READ_PRIMITIVE: (
        1350,
        "9d774988d901db651ab224c7b02a08aa284c6af86c63a52807e37ba73b95261b",
    ),
    CONTROLLER_STYLE_STORE: (0, EMPTY_SHA256),
    COLOR_SELECTOR: (
        1,
        "bea993f8b7ac808aad9daffe2a7b9f64c43d38a73266d1e50110c60e2f47a5ec",
    ),
    STYLE_PROPERTY_PARSER: (
        2,
        "a2908a708546a2e29af7947497fe31dbfc83a0bee8d45f9b716ef6a2ecf16d4f",
    ),
    UI_STYLE_SETTER: (
        2,
        "9d619e0d346cf7237fb7abc6d047ae2b8f47e96c93f3a1d152326f818ade58de",
    ),
}


EXPECTED_DWORD_REFS = {
    FONTSTYLE_ID_LITERAL: (
        (0x00AA4892, 0x00AA48A4, 0x00AA5374),
        "cdde9f8994649036715fca6866aa716b689ce85c0ce95c710117fda015da362f",
    ),
    EMBEDDED_STYLE_LITERAL: (
        (0x00AA4902, 0x00AA5396),
        "9d37a30eb604aa3d0158727a8fdd4279221c5a1b53c636e844c5cecb1bf34fa1",
    ),
    CONTROLLER_STYLE_STORE: (
        (
            0x00F2CCFC,
            0x00F2CD3C,
            0x00F2CD7C,
            0x00F5CB38,
            0x00F6B7C8,
            0x00F721E0,
            0x00F77A9C,
            0x00F77B64,
        ),
        "f6af1986f93731ce3f46ac3e9680e4f5d6ff2e6bd26cac5c91f2959a18efb746",
    ),
}


WIRE_SITES = {
    "actor_entry_type_W": (0x005E222D, WRITE_PRIMITIVE),
    "actor_entry_type_R": (0x005E2307, READ_PRIMITIVE),
    "actor_entry_identity_W": (0x005E223C, WRITE_PRIMITIVE),
    "actor_entry_identity_R": (0x005E2316, READ_PRIMITIVE),
    "basic_hp_W": (0x00465759, WRITE_PRIMITIVE),
    "basic_hp_R": (0x00465893, READ_PRIMITIVE),
    "basic_death_float_W": (0x004657BD, WRITE_PRIMITIVE),
    "basic_death_float_R": (0x004658F7, READ_PRIMITIVE),
    "basic_faction_W": (0x00465820, WRITE_PRIMITIVE),
    "basic_faction_R": (0x0046595A, READ_PRIMITIVE),
    "actor_relation_W": (0x00466595, WRITE_PRIMITIVE),
    "actor_relation_R": (0x00466AB2, READ_PRIMITIVE),
    "actor_category_W": (0x00466657, WRITE_PRIMITIVE),
    "actor_category_R": (0x00466B73, READ_PRIMITIVE),
    "npc_template_W": (0x00466EF6, WRITE_PRIMITIVE),
    "npc_template_R": (0x00466FA2, READ_PRIMITIVE),
    "hit_source_identity_W": (0x00750059, WRITE_PRIMITIVE),
    "hit_source_identity_R": (0x007500B2, READ_PRIMITIVE),
    "missile_source_identity_W": (0x0075012D, WRITE_PRIMITIVE),
    "missile_source_identity_R": (0x007501B1, READ_PRIMITIVE),
    "hit_target_identity_W": (0x0074F62C, WRITE_PRIMITIVE),
    "hit_target_identity_R": (0x0074FFCF, READ_PRIMITIVE),
}


STYLE_PUSH_SITES = {
    0x00443FF2: 55,
    0x00443FE9: 56,
    0x00444039: 56,
    0x0044414A: 57,
    0x00444071: 58,
    0x00444113: 59,
    0x0044417E: 60,
    0x00444210: 61,
    0x00444234: 61,
    0x00444263: 61,
    0x00444270: 62,
    0x0044419F: 63,
    0x00444214: 63,
    0x00444218: 63,
}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def fmt_va(value: int) -> str:
    return f"0x{value:08X}"


def parse_pe(image: bytes) -> tuple[int, tuple[Section, ...]]:
    if image[:2] != b"MZ":
        raise RuntimeError("image is not MZ")
    pe_off = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_off : pe_off + 4] != b"PE\x00\x00":
        raise RuntimeError("image is not PE")
    section_count = struct.unpack_from("<H", image, pe_off + 6)[0]
    optional_size = struct.unpack_from("<H", image, pe_off + 20)[0]
    optional_off = pe_off + 24
    if struct.unpack_from("<H", image, optional_off)[0] != 0x10B:
        raise RuntimeError("expected PE32 optional header")
    image_base = struct.unpack_from("<I", image, optional_off + 28)[0]
    table_off = optional_off + optional_size
    sections: list[Section] = []
    for index in range(section_count):
        off = table_off + index * 40
        name = image[off : off + 8].split(b"\x00", 1)[0].decode("ascii")
        virtual_size, rva, raw_size, raw_off = struct.unpack_from(
            "<IIII", image, off + 8
        )
        mapped_len = min(virtual_size, raw_size)
        if raw_off + mapped_len > len(image):
            raise RuntimeError(f"section {name} exceeds image")
        sections.append(
            Section(
                name=name,
                va=image_base + rva,
                file_off=raw_off,
                mapped_len=mapped_len,
                virtual_size=virtual_size,
                raw_size=raw_size,
            )
        )
    expected_names = (".text", ".code", ".rdata", ".data", ".rsrc", ".reloc")
    if tuple(section.name for section in sections) != expected_names:
        raise RuntimeError("PE section set/order drift")
    return image_base, tuple(sections)


def va_to_file(sections: Sequence[Section], va: int, allow_end: bool = False) -> int:
    for section in sections:
        end = section.va + section.mapped_len
        if section.va <= va < end or (allow_end and va == end):
            return section.file_off + va - section.va
    raise RuntimeError(f"VA outside file-backed mapped intervals: {fmt_va(va)}")


def section_for_va(sections: Sequence[Section], va: int) -> Section:
    for section in sections:
        if section.va <= va < section.va + section.mapped_len:
            return section
    raise RuntimeError(f"no section for {fmt_va(va)}")


def span_fact(
    image: bytes, sections: Sequence[Section], name: str
) -> Mapping[str, object]:
    start, end, expected_hash = SPANS[name]
    start_off = va_to_file(sections, start)
    end_off = va_to_file(sections, end, allow_end=True)
    actual_hash = sha256(image[start_off:end_off])
    if actual_hash != expected_hash:
        raise RuntimeError(f"span hash drift: {name}")
    return {
        "name": name,
        "start": start,
        "end": end,
        "start_off": start_off,
        "end_off": end_off,
        "sha": actual_hash,
    }


def list_digest(values: Iterable[int]) -> str:
    payload = "\n".join(f"{value:08X}" for value in values).encode("ascii")
    return sha256(payload)


def raw_e8_census(
    image: bytes, sections: Sequence[Section], targets: Iterable[int]
) -> Mapping[int, tuple[int, ...]]:
    target_set = set(targets)
    found: dict[int, list[int]] = {target: [] for target in target_set}
    for section in sections:
        begin = section.file_off
        stop = begin + section.mapped_len
        for off in range(begin, stop - 4):
            if image[off] != 0xE8:
                continue
            site_va = section.va + off - begin
            displacement = struct.unpack_from("<i", image, off + 1)[0]
            target = (site_va + 5 + displacement) & 0xFFFFFFFF
            if target in target_set:
                found[target].append(site_va)
    return {target: tuple(values) for target, values in found.items()}


def dword_reference_census(
    image: bytes, sections: Sequence[Section], target: int
) -> tuple[int, ...]:
    needle = struct.pack("<I", target)
    sites: list[int] = []
    for section in sections:
        begin = section.file_off
        stop = begin + section.mapped_len
        cursor = begin
        while True:
            found = image.find(needle, cursor, stop)
            if found < 0:
                break
            sites.append(section.va + found - begin)
            cursor = found + 1
    return tuple(sites)


def direct_target(image: bytes, sections: Sequence[Section], site_va: int) -> int:
    off = va_to_file(sections, site_va)
    if image[off] != 0xE8:
        raise RuntimeError(f"expected raw E8 at {fmt_va(site_va)}")
    return (site_va + 5 + struct.unpack_from("<i", image, off + 1)[0]) & 0xFFFFFFFF


def calls_in_span(
    census: Mapping[int, tuple[int, ...]], target: int, start: int, end: int
) -> tuple[int, ...]:
    return tuple(site for site in census[target] if start <= site < end)


def support_span(fact: Mapping[str, object]) -> str:
    return (
        f"{fact['name']}=VA:{fmt_va(int(fact['start']))}.."
        f"{fmt_va(int(fact['end']))}@file:{fmt_va(int(fact['start_off']))}.."
        f"{fmt_va(int(fact['end_off']))}@sha256:{fact['sha']}"
    )


def canonical_claim(row: Mapping[str, str]) -> str:
    fields = (
        row["row_kind"],
        row["control_surface"],
        row["condition"],
        row["exact_observation"],
        row["server_control_level"],
        row["nonclaim"],
    )
    return sha256("\x1f".join(fields).encode("utf-8"))


def evidence_key(row: Mapping[str, str]) -> str:
    canonical = {
        key: row[key]
        for key in FIELDNAMES
        if key not in ("evidence_key", "artifact_pair_sha256")
    }
    return sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def make_row(
    key: str,
    span: Mapping[str, object],
    **values: str,
) -> dict[str, str]:
    row = {name: "" for name in FIELDNAMES}
    row.update(
        {
            "control_key": key,
            "source": SOURCE,
            "source_file": SOURCE_FILE,
            "source_sha256": EXPECTED_IMAGE_SHA256,
            "span_start_va": fmt_va(int(span["start"])),
            "span_end_va": fmt_va(int(span["end"])),
            "file_off_start": fmt_va(int(span["start_off"])),
            "file_off_end": fmt_va(int(span["end_off"])),
            "span_sha256": str(span["sha"]),
        }
    )
    row.update(values)
    if row["exact_observation"]:
        label = (
            "[MEASURED][IMAGE][OPEN][SYNTHESIS]"
            if row["row_kind"] == "CONTROL_CONCLUSION"
            else "[MEASURED][IMAGE]"
        )
        if not row["exact_observation"].startswith("["):
            row["exact_observation"] = label + " " + row["exact_observation"]
    if row["nonclaim"] and not row["nonclaim"].startswith("["):
        row["nonclaim"] = "[MEASURED][IMAGE][NONCLAIM] " + row["nonclaim"]
    row["claim_sha256"] = canonical_claim(row)
    row["evidence_key"] = evidence_key(row)
    return row


def load_pinned_tsv(
    path: Path,
    expected_size: int,
    expected_sha256: str,
    required_columns: Sequence[str],
) -> list[dict[str, str]]:
    if not path.exists():
        raise RuntimeError(f"required reference is missing: {path.name}")
    raw = path.read_bytes()
    if len(raw) != expected_size or sha256(raw) != expected_sha256:
        raise RuntimeError(f"pinned reference drift: {path.name}")
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise RuntimeError(f"empty pinned reference: {path.name}")
    header = set(rows[0])
    missing = set(required_columns) - header
    if missing:
        raise RuntimeError(f"reference schema drift: {path.name}: {sorted(missing)!r}")
    return rows


def derive_serializer_inventory() -> Mapping[str, object]:
    expected_header = [
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
    ]
    rows = load_pinned_tsv(
        SERIALIZER_FIELDS_PATH,
        EXPECTED_SERIALIZER_FIELDS_SIZE,
        EXPECTED_SERIALIZER_FIELDS_SHA256,
        expected_header,
    )
    if list(rows[0]) != expected_header:
        raise RuntimeError("PF_SERIALIZER_FIELDS.tsv schema drift")
    if len(rows) != 6931:
        raise RuntimeError("PF_SERIALIZER_FIELDS.tsv row-count drift")
    if {row["source"] for row in rows} != {"IMAGE"}:
        raise RuntimeError("PF_SERIALIZER_FIELDS.tsv source drift")
    message_count = len({row["message"] for row in rows})
    empty_rows = [row for row in rows if row["tag"] == "EMPTY"]
    empty_w = sum(row["direction(W/R)"] == "W" for row in empty_rows)
    empty_r = sum(row["direction(W/R)"] == "R" for row in empty_rows)
    direct_tags = {"0x0B", "0x32", "0x14", "0x08", "0x12", "0x0F", "0x2A", "0x19"}
    direct_rows = sum(row["tag"] in direct_tags for row in rows)
    joined_text = "\n".join("\t".join(row.values()) for row in rows).casefold()
    term_matches = {
        term: joined_text.count(term.casefold())
        for term in ("FontStyleID", "FontStyle", "LABEL_NAME")
    }
    expected = {
        "message_count": 519,
        "empty_count": 202,
        "empty_w": 101,
        "empty_r": 101,
        "direct_rows": 2711,
    }
    actual = {
        "message_count": message_count,
        "empty_count": len(empty_rows),
        "empty_w": empty_w,
        "empty_r": empty_r,
        "direct_rows": direct_rows,
    }
    if actual != expected:
        raise RuntimeError(f"PF_SERIALIZER_FIELDS.tsv inventory drift: {actual!r}")
    if any(term_matches.values()):
        raise RuntimeError("style term appeared in PF_SERIALIZER_FIELDS.tsv")
    return {
        **actual,
        "row_count": len(rows),
        "term_matches": term_matches,
        "sha256": EXPECTED_SERIALIZER_FIELDS_SHA256,
        "size": EXPECTED_SERIALIZER_FIELDS_SIZE,
    }


def derive(image: bytes) -> tuple[list[dict[str, str]], Mapping[str, object]]:
    image_base, sections = parse_pe(image)
    if image_base != 0x00400000:
        raise RuntimeError("image base drift")
    facts = {name: span_fact(image, sections, name) for name in SPANS}
    serializer_inventory = derive_serializer_inventory()

    targets = tuple(EXPECTED_E8_CENSUS)
    calls = raw_e8_census(image, sections, targets)
    for target, (expected_count, expected_digest) in EXPECTED_E8_CENSUS.items():
        actual = calls[target]
        if len(actual) != expected_count or list_digest(actual) != expected_digest:
            raise RuntimeError(f"raw E8 census drift for {fmt_va(target)}")
    if calls[COLOR_SELECTOR] != (0x004446A7,):
        raise RuntimeError("selector direct-caller set drift")
    if calls[STYLE_PROPERTY_PARSER] != (0x00A9FA11, 0x00AA490D):
        raise RuntimeError("style-property parser caller set drift")
    if calls[UI_STYLE_SETTER] != (0x00AB97F9, 0x00AB9D4A):
        raise RuntimeError("UI style-setter direct-caller set drift")

    refs: dict[int, tuple[int, ...]] = {}
    for target, (expected_sites, expected_digest) in EXPECTED_DWORD_REFS.items():
        actual = dword_reference_census(image, sections, target)
        if actual != expected_sites or list_digest(actual) != expected_digest:
            raise RuntimeError(f"dword-reference census drift for {fmt_va(target)}")
        refs[target] = actual

    for name, (site, target) in WIRE_SITES.items():
        if direct_target(image, sections, site) != target:
            raise RuntimeError(f"wire site drift: {name}")

    for site, value in STYLE_PUSH_SITES.items():
        off = va_to_file(sections, site)
        if image[off] != 0x6A or image[off + 1] != value:
            raise RuntimeError(f"selector style immediate drift at {fmt_va(site)}")

    primitive_sites = calls[WRITE_PRIMITIVE] + calls[READ_PRIMITIVE]
    style_adjacent: list[tuple[int, int]] = []
    for site in primitive_sites:
        section = section_for_va(sections, site)
        off = va_to_file(sections, site)
        begin = max(section.file_off, off - 64)
        window = image[begin:off]
        for value in range(55, 68):
            short_form = bytes((0x6A, value))
            long_form = b"\x68" + struct.pack("<I", value)
            if short_form in window or long_form in window:
                style_adjacent.append((site, value))
    if style_adjacent:
        raise RuntimeError("style immediate found next to direct wire primitive")

    local_spans = (
        "color_selector",
        "controller_style_store",
        "npc_label_sink",
        "style_property_parser",
        "label_property_parser",
        "ui_style_forwarder_1",
        "ui_style_forwarder_2",
    )
    for name in local_spans:
        start = int(facts[name]["start"])
        end = int(facts[name]["end"])
        if calls_in_span(calls, WRITE_PRIMITIVE, start, end):
            raise RuntimeError(f"WRITE primitive appeared in local style span: {name}")
        if calls_in_span(calls, READ_PRIMITIVE, start, end):
            raise RuntimeError(f"READ primitive appeared in local style span: {name}")

    section_scope = ",".join(
        f"{section.name}:{fmt_va(section.va)}.."
        f"{fmt_va(section.va + section.mapped_len)}@file:"
        f"{fmt_va(section.file_off)}..{fmt_va(section.file_off + section.mapped_len)}"
        for section in sections
    )
    all_primitive_digest = sha256(
        (
            f"W:{list_digest(calls[WRITE_PRIMITIVE])}\n"
            f"R:{list_digest(calls[READ_PRIMITIVE])}"
        ).encode("ascii")
    )
    local_support = ";".join(support_span(facts[name]) for name in local_spans)
    rows: list[dict[str, str]] = []

    rows.append(
        make_row(
            "MWC-IMG-001",
            facts["color_selector"],
            row_kind="WHOLE_IMAGE_DIRECT_E8_PRECALL_LITERAL_NEGATIVE",
            control_surface="FontStyleID_55_through_67_vs_generic_wire_primitives",
            carrier_or_local_source="all direct E8 callers of WRITE/READ",
            wire_direction="W+R",
            producer_va=f"{fmt_va(WRITE_PRIMITIVE)};{fmt_va(READ_PRIMITIVE)}",
            consumer_va=fmt_va(COLOR_SELECTOR),
            condition="64-byte pre-call byte window at every direct primitive caller",
            exact_observation=(
                f"{len(primitive_sites)} direct primitive call sites were scanned; none has "
                "a PUSH imm8 or PUSH imm32 encoding for 55..67 in the preceding 64 bytes"
            ),
            server_control_level="NO_LITERAL_STYLE_IMMEDIATE_ADJACENCY_FOUND",
            semantic_status="PROVEN_EXACT_MECHANICAL_CENSUS",
            census_scope=section_scope,
            census_count=(
                f"WRITE={len(calls[WRITE_PRIMITIVE])};"
                f"READ={len(calls[READ_PRIMITIVE])};"
                f"style_adjacent={len(style_adjacent)}"
            ),
            census_digest=all_primitive_digest,
            support_spans=local_support,
            reference_keys="PF_MONSTER_COLOR_GATE:MCG-IMG-051;PF_MONSTER_COLOR_GATE:MCG-IMG-052",
            nonclaim=(
                "This is not a proof against indirect calls, custom codecs, aliases, "
                "whole-object copies, or transitive dataflow outside the 64-byte windows."
            ),
            blocker="Indirect/custom dataflow is outside this byte-pattern census.",
            required_next_evidence=(
                "A whole-program indirect-call/dataflow proof or an original capture carrying "
                "an explicit style field."
            ),
        )
    )

    rows.append(
        make_row(
            "MWC-IMG-002",
            facts["controller_style_store"],
            row_kind="STYLE_SINK_PRODUCER_CENSUS",
            control_surface="CNetNPC_nameboard_controller_plus_0x34",
            carrier_or_local_source="controller_style_store_and_selector",
            producer_va=fmt_va(COLOR_SELECTOR),
            consumer_va=fmt_va(CONTROLLER_STYLE_STORE),
            condition="whole-image raw E8 and dword-reference census",
            exact_observation=(
                f"controller style store has {len(calls[CONTROLLER_STYLE_STORE])} raw E8 "
                f"direct callers and {len(refs[CONTROLLER_STYLE_STORE])} dword references; "
                f"the selector has {len(calls[COLOR_SELECTOR])} raw E8 caller at 0x004446A7"
            ),
            server_control_level="CLIENT_LOCAL_SELECTOR_OUTPUT",
            semantic_status="PROVEN_EXACT_MECHANICAL_CENSUS",
            census_scope=section_scope,
            census_count=(
                f"style_store_E8={len(calls[CONTROLLER_STYLE_STORE])};"
                f"style_store_dword_refs={len(refs[CONTROLLER_STYLE_STORE])};"
                f"selector_E8={len(calls[COLOR_SELECTOR])}"
            ),
            census_digest=(
                f"style_store_E8={list_digest(calls[CONTROLLER_STYLE_STORE])};"
                f"style_store_refs={list_digest(refs[CONTROLLER_STYLE_STORE])};"
                f"selector_E8={list_digest(calls[COLOR_SELECTOR])}"
            ),
            support_spans=(
                support_span(facts["color_selector"])
                + ";"
                + support_span(facts["npc_label_sink"])
            ),
            reference_keys="PF_MONSTER_COLOR_GATE:MCG-IMG-031;PF_MONSTER_COLOR_GATE:MCG-IMG-051",
            nonclaim=(
                f"The {len(refs[CONTROLLER_STYLE_STORE])} dword references are not all "
                "CNetNPC slots, and a virtual call "
                "cannot be excluded by the E8 negative."
            ),
            blocker="Complete indirect-call target recovery is not part of the bounded census.",
            required_next_evidence="Full vtable-owner census plus indirect-call dataflow.",
        )
    )

    rows.append(
        make_row(
            "MWC-IMG-003",
            facts["label_property_parser"],
            row_kind="PROPERTY_LITERAL_REFERENCE_CENSUS",
            control_surface="FontStyleID_and_embedded_FontStyle_literals",
            carrier_or_local_source="local GUI property parsing",
            producer_va="0x00AA4892;0x00AA48A4;0x00AA5374;0x00AA4902;0x00AA5396",
            consumer_va=f"{fmt_va(STYLE_PROPERTY_PARSER)};{fmt_va(UI_STYLE_SETTER)}",
            condition="whole-image dword-reference and raw E8 target census",
            exact_observation=(
                f"FontStyleID has {len(refs[FONTSTYLE_ID_LITERAL])} dword references and "
                f"embedded FontStyle has {len(refs[EMBEDDED_STYLE_LITERAL])}; "
                f"the style-property parser has {len(calls[STYLE_PROPERTY_PARSER])} direct "
                "callers at 0x00A9FA11 and "
                "0x00AA490D; neither parser span calls WRITE or READ"
            ),
            server_control_level="LITERAL_REFS_RESOLVE_TO_LOCAL_GUI_SITES;OTHER_PATHS_OPEN",
            semantic_status="PROVEN_EXACT_MECHANICAL_CENSUS",
            census_scope=section_scope,
            census_count=(
                f"FontStyleID_refs={len(refs[FONTSTYLE_ID_LITERAL])};"
                f"FontStyle_refs={len(refs[EMBEDDED_STYLE_LITERAL])};"
                f"property_parser_E8={len(calls[STYLE_PROPERTY_PARSER])}"
            ),
            census_digest=(
                f"id_refs={list_digest(refs[FONTSTYLE_ID_LITERAL])};"
                f"style_refs={list_digest(refs[EMBEDDED_STYLE_LITERAL])};"
                f"parser_E8={list_digest(calls[STYLE_PROPERTY_PARSER])}"
            ),
            support_spans=(
                support_span(facts["style_property_parser"])
                + ";"
                + support_span(facts["ui_style_forwarder_1"])
                + ";"
                + support_span(facts["ui_style_forwarder_2"])
            ),
            reference_keys="PF_MONSTER_COLOR_GATE:MCG-IMG-057;PF_MONSTER_COLOR_GATE:MCG-IMG-058",
            nonclaim=(
                "A literal-reference census cannot rule out unnamed binary fields or "
                "runtime-computed aliases."
            ),
            blocker="No complete alias/dataflow proof for unnamed fields.",
            required_next_evidence="Original traffic with an explicit style property or complete alias analysis.",
        )
    )

    rows.append(
        make_row(
            "MWC-IMG-004",
            facts["color_selector"],
            row_kind="LOCAL_STYLE_IMMEDIATE_CENSUS",
            control_surface="FontStyleID_55_through_63",
            carrier_or_local_source="name-color selector immediates",
            producer_va=";".join(fmt_va(site) for site in STYLE_PUSH_SITES),
            consumer_va=fmt_va(CONTROLLER_STYLE_STORE),
            condition="all pinned selector PUSH-immediate sites match",
            exact_observation=(
                f"The selector itself contains {len(STYLE_PUSH_SITES)} pinned immediate "
                "emission sites for "
                "FontStyleID 55..63; these values are local constants, not values read by a "
                "wire primitive in the selector"
            ),
            server_control_level="CLIENT_LOCAL_SELECTOR_OUTPUT",
            semantic_status="PROVEN_EXACT_MANUAL_HASH_ANCHORED",
            census_scope="selector span plus direct primitive negative in same span",
            census_count=(
                f"style_emit_sites={len(STYLE_PUSH_SITES)};"
                f"WRITE_calls={len(calls_in_span(calls, WRITE_PRIMITIVE, int(facts['color_selector']['start']), int(facts['color_selector']['end'])))};"
                f"READ_calls={len(calls_in_span(calls, READ_PRIMITIVE, int(facts['color_selector']['start']), int(facts['color_selector']['end'])))}"
            ),
            census_digest=sha256(
                "\n".join(
                    f"{site:08X}:{value}" for site, value in STYLE_PUSH_SITES.items()
                ).encode("ascii")
            ),
            support_spans=support_span(facts["controller_style_store"]),
            reference_keys=(
                "PF_ATTR_NAME_COLOR_SELECTOR.tsv@sha256:"
                + EXPECTED_ATTR_SELECTOR_SHA256
                + ";PF_MONSTER_COLOR_GATE:MCG-IMG-031..033"
            ),
            nonclaim="The local conditions are not proof that every live object reaches one path.",
            blocker="Live predicate values remain runtime facts.",
            required_next_evidence="Original capture or attended runtime observation for live branch selection.",
        )
    )

    def wire_row(
        key: str,
        span_name: str,
        surface: str,
        carrier: str,
        direction: str,
        offset: str,
        tag: str,
        length: str,
        gate: str,
        producer: str,
        consumer: str,
        observation: str,
        level: str,
        references: str,
        nonclaim: str,
        support: str = "",
    ) -> None:
        rows.append(
            make_row(
                key,
                facts[span_name],
                row_kind="SERVER_CONTROLLABLE_UPSTREAM",
                control_surface=surface,
                carrier_or_local_source=carrier,
                wire_direction=direction,
                object_offset=offset,
                wire_tag=tag,
                wire_len=length,
                presence_gate=gate,
                producer_va=producer,
                consumer_va=consumer,
                condition="pinned direct primitive sites and manually interpreted hashed codec",
                exact_observation=observation,
                server_control_level=level,
                semantic_status="PROVEN_EXACT_MANUAL_HASH_ANCHORED",
                census_scope="named codec span; direct E8 sites verified against whole-image census",
                census_count="",
                census_digest="",
                support_spans=support,
                reference_keys=references,
                nonclaim=nonclaim,
                blocker="Live delivery and predicate outcome are not established by IMAGE alone.",
                required_next_evidence="Original capture or attended runtime join for the intended visible outcome.",
            )
        )

    wire_row(
        "MWC-IMG-006",
        "runtime_actor_entry_codec",
        "actor_type",
        "GSCN_RunTimeProtocolRes actor entry",
        "W+R",
        "+0x10",
        "0x0B",
        "1",
        "always in actor-entry codec",
        "0x005E222D",
        "0x005E2307",
        "Actor-entry type is directly serialized/deserialized; value 4 selects the CNetNPC factory path.",
        "DIRECT_WIRE",
        "PF_MONSTER_COLOR_GATE:MCG-IMG-002",
        "Type 4 proves CNetNPC construction, not the gameplay noun monster.",
    )
    wire_row(
        "MWC-IMG-007",
        "runtime_actor_entry_codec",
        "actor_identity_sign",
        "GSCN_RunTimeProtocolRes actor entry",
        "W+R",
        "+0x18..+0x1F",
        "0x32",
        "8",
        "always in actor-entry codec",
        "0x005E223C",
        "0x005E2316;0x00443FFB",
        (
            "The full qword actor identity is directly carried and copied to the CNetNPC; "
            "its signed high dword selects the positive versus signed-nonpositive color lane."
        ),
        "DIRECT_WIRE_BUT_IDENTITY_INVARIANTS_APPLY",
        "PF_MONSTER_COLOR_GATE:MCG-IMG-004;PF_MONSTER_COLOR_GATE:MCG-IMG-005;PF_MONSTER_COLOR_GATE:MCG-IMG-009",
        "IMAGE does not prove which signed-negative identities the original server assigns or which remain registry-safe.",
        support_span(facts["color_selector"]),
    )
    wire_row(
        "MWC-IMG-008",
        "basicattr_codec",
        "current_HP_operand",
        "BasicAttr",
        "W+R",
        "+0x44",
        "0x14",
        "4",
        "presence mask +0x70 bit 0x0004",
        "0x00465759",
        "0x00465893;0x0043BD70",
        "BasicAttr +0x44 is directly carried and is the integer zero operand of the CNetNPC death predicate.",
        "DIRECT_WIRE",
        "PF_MONSTER_COLOR_GATE:MCG-IMG-034",
        "This row does not claim that setting HP alone makes the predicate true.",
        support_span(facts["death_predicate"]),
    )
    wire_row(
        "MWC-IMG-009",
        "basicattr_codec",
        "death_threshold_float_operand",
        "BasicAttr",
        "W+R",
        "+0x58",
        "0x2A",
        "4",
        "presence mask +0x70 bit 0x0080",
        "0x004657BD",
        "0x004658F7;0x0043BD70",
        "BasicAttr +0x58 is directly carried and is the ordered-float <= 0 operand of the CNetNPC death predicate.",
        "DIRECT_WIRE",
        "PF_ATTR_FIELD_SEMANTICS:e0e2acc3668f95663b384b742add7f392a7310a745b235d4aa1a2ce790d391ce;PF_MONSTER_COLOR_GATE:MCG-IMG-034",
        "The broader gameplay name/unit of +0x58 is not established here.",
        support_span(facts["death_predicate"]),
    )
    wire_row(
        "MWC-IMG-010",
        "basicattr_codec",
        "faction_operand",
        "BasicAttr attached to CNetNPC",
        "W+R",
        "+0x68",
        "0x14",
        "4",
        "presence mask +0x70 bit 0x0400",
        "0x00465820",
        "0x0046595A;0x0043C380",
        "BasicAttr +0x68 is directly carried and is a CNetNPC n_FACTION input consumed by the local relation predicate.",
        "DIRECT_WIRE_PREDICATE_OPERAND",
        "PF_ATTR_FIELD_SEMANTICS:f61d6df70f3ed3ef85bcb8388b482cabe5a6dd406fd3343633e7c7b5e0e44f16;PF_ATTR_FIELD_SEMANTICS:60bd7e9ad7c38843030431c91ddcc090acff9cbcf1a321e20e6983e23f07084e",
        "The predicate is multi-input; no universal friendly/hostile enum label is assigned.",
        support_span(facts["relation_predicate"]),
    )
    wire_row(
        "MWC-IMG-011",
        "actorattr_codec",
        "actor_relation_byte_operand",
        "ActorAttr",
        "W+R",
        "+0x98",
        "0x0B",
        "1",
        "presence mask +0x1B4 bit 0x04000000",
        "0x00466595",
        "0x00466AB2;0x0043C380",
        "ActorAttr +0x98 is directly carried and participates in a local actor relation/name-style predicate.",
        "DIRECT_WIRE_PREDICATE_OPERAND",
        "PF_ATTR_FIELD_SEMANTICS:2360631178e80e06899077a2ab8d4057bfdaea703fb4a378b5b1420a2bd5fb35;PF_ATTR_FIELD_SEMANTICS:47b6d98d7c672f43755081524164ba6e44c242cdaccf2e5d2a2f52cfc9f5a8b9",
        "No global gameplay relation noun or complete value domain is assigned.",
        support_span(facts["relation_predicate"]),
    )
    wire_row(
        "MWC-IMG-012",
        "actorattr_codec",
        "actor_category_byte_operand",
        "ActorAttr",
        "W+R",
        "+0x1A0",
        "0x0B",
        "1",
        "second presence mask +0x1B8 bit 0x00000001",
        "0x00466657",
        "0x00466B73;0x0043C380",
        "ActorAttr +0x1A0 is directly carried and participates in category/relation selection paths.",
        "DIRECT_WIRE_PREDICATE_OPERAND",
        "PF_ATTR_FIELD_SEMANTICS:c44fece3dc4e035ede5b8c8fa4207e033732687cd399171c8b9ede451efc2088;PF_ATTR_FIELD_SEMANTICS:5ab829b217f8f3f6ab5dee26f392a2af2dce06ed4e9252e231e92f27caf6436b",
        "Its exact Navy/Pirate icon use does not establish a universal faction enum for every owner.",
        support_span(facts["relation_predicate"]),
    )
    wire_row(
        "MWC-IMG-013",
        "npcattr_codec",
        "npc_template_id",
        "NPCAttr",
        "W+R",
        "+0x78",
        "0x12",
        "2",
        "presence mask bit 0x01",
        "0x00466EF6",
        "0x00466FA2;0x0045C160",
        (
            "NPCAttr +0x78 is directly carried and selects the local MOBS/AI_WANDER "
            "template used by the n_OFFESIVE predicate."
        ),
        "DIRECT_WIRE_TEMPLATE_KEY_INDIRECT_LOCAL_PROPERTY",
        "PF_ATTR_FIELD_SEMANTICS:1ed5be39d4d0ae52c9d01fbafd9a29433f88a0b2e2033a24bd52b44eac87c919;PF_ATTR_FIELD_SEMANTICS:938c4da20c8677c3d25982c89321fb14adb0a454d6b83de8efafdfa6d8e99a33",
        "n_OFFESIVE itself is client-local table-derived state, not a direct wire field in this codec.",
        support_span(facts["ai_offensive"]),
    )

    rows.append(
        make_row(
            "MWC-IMG-014",
            facts["hit_result_codec"],
            row_kind="SERVER_CONTROLLABLE_INDIRECT_WRITER",
            control_surface="actor_plus_0x70_bit_0x100",
            carrier_or_local_source="CHitResult source and target identity",
            wire_direction="W+R",
            object_offset="packet+0x18 source qword; packet+0x2C vector target qword",
            wire_tag="0x32",
            wire_len="8",
            producer_va="0x00750059;0x0074F62C",
            consumer_va="0x007500B2;0x0074FFCF;0x00750896",
            condition=(
                "target resolves; target gate bit passes; target identity high is signed-negative; "
                "source resolves/casts to local actor"
            ),
            exact_observation=(
                "CHitResult directly carries source/target identities; under the pinned handler "
                "conditions it sets target actor+0x70 bit 0x100, which is later a local "
                "FontStyleID-61 selector operand."
            ),
            server_control_level="INDIRECT_WIRE_TRIGGER_TO_CLIENT_RUNTIME_BIT",
            semantic_status="PROVEN_ROLE_ONLY_MANUAL_HASH_ANCHORED",
            census_scope="packet codec, vector element codecs, and conditional writer",
            support_spans=(
                support_span(facts["hit_vector_write_codec"])
                + ";"
                + support_span(facts["hit_vector_read_codec"])
                + ";"
                + support_span(facts["hit_bit_writer"])
                + ";"
                + support_span(facts["bit_selector"])
            ),
            reference_keys="PF_MONSTER_COLOR_GATE:MCG-IMG-036;PF_COMBAT_LIFECYCLE:CL-IMG-006",
            nonclaim=(
                "The bit is unnamed; this does not prove aggro/hostility, guaranteed CNetNPC "
                "target type, delivery order, or persistent style-61/nameboard output."
            ),
            blocker="Typed target and live handler gates are runtime facts.",
            required_next_evidence="Original CHitResult joined to the exact target and rendered nameboard.",
        )
    )

    rows.append(
        make_row(
            "MWC-IMG-015",
            facts["missile_hit_result_codec"],
            row_kind="SERVER_CONTROLLABLE_INDIRECT_WRITER",
            control_surface="actor_plus_0x70_bit_0x100",
            carrier_or_local_source="CMissileHitResult source and target identity",
            wire_direction="W+R",
            object_offset="packet+0x18 source qword; packet+0x40 vector target qword",
            wire_tag="0x32",
            wire_len="8",
            producer_va="0x0075012D;0x0074F62C",
            consumer_va="0x007501B1;0x0074FFCF;0x007511A6",
            condition=(
                "target resolves; target gate bit passes; target identity high is signed-negative; "
                "source resolves/casts to local actor"
            ),
            exact_observation=(
                "CMissileHitResult directly carries source/target identities; under the pinned "
                "handler conditions it sets the same target actor+0x70 bit 0x100."
            ),
            server_control_level="INDIRECT_WIRE_TRIGGER_TO_CLIENT_RUNTIME_BIT",
            semantic_status="PROVEN_ROLE_ONLY_MANUAL_HASH_ANCHORED",
            census_scope="packet codec, vector element codecs, and conditional writer",
            support_spans=(
                support_span(facts["hit_vector_write_codec"])
                + ";"
                + support_span(facts["hit_vector_read_codec"])
                + ";"
                + support_span(facts["missile_bit_writer"])
                + ";"
                + support_span(facts["bit_selector"])
            ),
            reference_keys="PF_MONSTER_COLOR_GATE:MCG-IMG-037",
            nonclaim="The bit remains unnamed and the writer does not prove a CNetNPC target.",
            blocker="Typed target and live handler gates are runtime facts.",
            required_next_evidence="Original CMissileHitResult joined to the exact target and rendered nameboard.",
        )
    )

    upstream_count = sum(
        row["row_kind"]
        in ("SERVER_CONTROLLABLE_UPSTREAM", "SERVER_CONTROLLABLE_INDIRECT_WRITER")
        for row in rows
    )
    upstream_digest = sha256(
        "\n".join(
            row["control_key"]
            for row in rows
            if row["row_kind"]
            in ("SERVER_CONTROLLABLE_UPSTREAM", "SERVER_CONTROLLABLE_INDIRECT_WRITER")
        ).encode("ascii")
    )
    direct_style_proved_count = sum(
        row["row_kind"] == DIRECT_STYLE_WIRE_ROW_KIND
        and row["semantic_status"].startswith("PROVEN")
        for row in rows
    )
    if direct_style_proved_count != 0:
        raise RuntimeError("direct-style conclusion must be re-audited for newly proved rows")
    pre_conclusion_keys = tuple(row["control_key"] for row in rows)
    rows.append(
        make_row(
            "MWC-IMG-016",
            facts["color_selector"],
            row_kind="CONTROL_CONCLUSION",
            control_surface="CNetNPC_LABEL_NAME_color",
            carrier_or_local_source="identity, relation/faction/category, death, template, hit-state",
            wire_direction="S2C inputs plus client-local selection",
            condition="all selector/nameboard readiness gates and the relevant predicate branch pass",
            exact_observation=(
                "No direct FontStyleID or embedded-style wire field is proved by the audited "
                "literal/immediate, sink, and pinned typed-path surfaces. Direct style-wire "
                "control remains OPEN because variable-loaded operands, custom/indirect paths, "
                f"and {serializer_inventory['empty_count']} EMPTY serializer directions are "
                "not closed. On the audited CNetNPC "
                "paths, the proved controls are upstream inputs and the client selects the final ID."
            ),
            server_control_level="DIRECT_STYLE_WIRE_OPEN;PROVED_UPSTREAM_INPUTS",
            semantic_status="OPEN_BOUNDED_SYNTHESIS",
            census_scope="control_keys=" + ",".join(pre_conclusion_keys),
            census_count=(
                f"direct_style_wire_proved={direct_style_proved_count};"
                f"upstream_control_rows={upstream_count};"
                f"EMPTY={serializer_inventory['empty_count']}"
            ),
            census_digest=upstream_digest,
            support_spans=(
                support_span(facts["relation_predicate"])
                + ";"
                + support_span(facts["death_predicate"])
                + ";"
                + support_span(facts["npc_label_sink"])
            ),
            reference_keys=(
                "PF_MONSTER_COLOR_GATE:MCG-IMG-031..038;"
                "PF_MONSTER_COLOR_GATE:MCG-IMG-051..052;"
                "PF_SERIALIZER_FIELDS.tsv@sha256:"
                + EXPECTED_SERIALIZER_FIELDS_SHA256
            ),
            nonclaim=(
                "This is not a negative whole-program finding. It does not rule out a dynamic "
                "style field, embedded-style structure, alias, custom codec, indirect call, or EMPTY row."
            ),
            blocker=(
                "Direct style-wire dataflow remains open, as do original-server identity policy, "
                "relation domains, complete bit writers, and live readiness/delivery."
            ),
            required_next_evidence=(
                f"Trace all decoded and {serializer_inventory['empty_count']} EMPTY serializer "
                "directions through handlers/aliases "
                "to the style sinks; separately vary one proved upstream input at a time at runtime."
            ),
        )
    )

    if any(row["source"] != SOURCE for row in rows):
        raise RuntimeError("every TSV row must have source=IMAGE")
    keys = [row["control_key"] for row in rows]
    evidence = [row["evidence_key"] for row in rows]
    claims = [row["claim_sha256"] for row in rows]
    if len(keys) != len(set(keys)):
        raise RuntimeError("duplicate control_key")
    if len(evidence) != len(set(evidence)):
        raise RuntimeError("duplicate evidence_key")
    if len(claims) != len(set(claims)):
        raise RuntimeError("duplicate claim_sha256")

    for row in rows:
        row["artifact_pair_sha256"] = PAIR_PLACEHOLDER
        if evidence_key(row) != row["evidence_key"]:
            raise RuntimeError("pair assignment changed evidence key")

    metadata: dict[str, object] = {
        "sections": sections,
        "section_scope": section_scope,
        "calls": calls,
        "refs": refs,
        "primitive_adjacent_count": len(style_adjacent),
        "facts": facts,
        "serializer_inventory": serializer_inventory,
        "direct_style_proved_count": direct_style_proved_count,
        "pair_sha256": PAIR_PLACEHOLDER,
    }
    return rows, metadata


def validate_reference_separation(rows: Sequence[Mapping[str, str]]) -> None:
    old_rows = load_pinned_tsv(
        REFERENCE_GATE_PATH,
        EXPECTED_GATE_SIZE,
        EXPECTED_GATE_SHA256,
        ("gate_key", "evidence_key", "source"),
    )
    selector_rows = load_pinned_tsv(
        ATTR_SELECTOR_PATH,
        EXPECTED_ATTR_SELECTOR_SIZE,
        EXPECTED_ATTR_SELECTOR_SHA256,
        ("selector_key", "evidence_key", "source", "image_sha256"),
    )
    attr_rows = load_pinned_tsv(
        ATTR_SEMANTICS_PATH,
        EXPECTED_ATTR_SEMANTICS_SIZE,
        EXPECTED_ATTR_SEMANTICS_SHA256,
        ("evidence_key", "source", "image_sha256"),
    )
    combat_rows = load_pinned_tsv(
        COMBAT_LIFECYCLE_PATH,
        EXPECTED_COMBAT_LIFECYCLE_SIZE,
        EXPECTED_COMBAT_LIFECYCLE_SHA256,
        ("lifecycle_id", "source", "image_sha256"),
    )
    old_keys = {row.get("gate_key", "") for row in old_rows}
    if "" in old_keys or len(old_keys) != len(old_rows):
        raise RuntimeError("PF_MONSTER_COLOR_GATE.tsv key drift")
    old_by_key = {row["gate_key"]: row for row in old_rows}
    old_evidence = {row.get("evidence_key", "") for row in old_rows if row.get("evidence_key", "")}
    old_claims = {row.get("claim_sha256", "") for row in old_rows if row.get("claim_sha256", "")}
    old_claims.update(
        sha256(
            "\x1f".join(
                (
                    row.get("row_kind", ""),
                    row.get("applies_to_class", ""),
                    row.get("condition", ""),
                    row.get("output", ""),
                    row.get("semantic_status", ""),
                    row.get("nonclaim", ""),
                )
            ).encode("utf-8")
        )
        for row in old_rows
    )
    collisions = {row["evidence_key"] for row in rows} & old_evidence
    if collisions:
        raise RuntimeError("evidence_key duplicates PF_MONSTER_COLOR_GATE")
    claim_collisions = {row["claim_sha256"] for row in rows} & old_claims
    if claim_collisions:
        raise RuntimeError("claim_sha256 duplicates PF_MONSTER_COLOR_GATE")

    selector_source = {row["source"] for row in selector_rows}
    selector_images = {row["image_sha256"] for row in selector_rows}
    if (
        len(selector_rows) != len(STYLE_PUSH_SITES)
        or selector_source != {"IMAGE"}
        or selector_images != {EXPECTED_IMAGE_SHA256}
    ):
        raise RuntimeError("PF_ATTR_NAME_COLOR_SELECTOR.tsv inventory/source drift")
    attr_by_evidence = {row["evidence_key"]: row for row in attr_rows}
    if "" in attr_by_evidence or len(attr_by_evidence) != len(attr_rows):
        raise RuntimeError("PF_ATTR_FIELD_SEMANTICS.tsv evidence-key drift")
    combat_by_id = {row["lifecycle_id"]: row for row in combat_rows}
    if "" in combat_by_id or len(combat_by_id) != len(combat_rows):
        raise RuntimeError("PF_COMBAT_LIFECYCLE.tsv lifecycle-id drift")

    for row in rows:
        for reference in row["reference_keys"].split(";"):
            if reference.startswith("PF_ATTR_NAME_COLOR_SELECTOR.tsv@sha256:"):
                suffix = reference.split(":", 1)[1]
                if suffix != EXPECTED_ATTR_SELECTOR_SHA256:
                    raise RuntimeError("PF_ATTR_NAME_COLOR_SELECTOR.tsv hash reference drift")
                continue
            if reference.startswith("PF_SERIALIZER_FIELDS.tsv@sha256:"):
                suffix = reference.split(":", 1)[1]
                if suffix != EXPECTED_SERIALIZER_FIELDS_SHA256:
                    raise RuntimeError("PF_SERIALIZER_FIELDS.tsv hash reference drift")
                continue
            if reference.startswith("PF_ATTR_FIELD_SEMANTICS:"):
                suffix = reference.split(":", 1)[1]
                match = attr_by_evidence.get(suffix)
                if match is None or match["source"] != "IMAGE" or match["image_sha256"] != EXPECTED_IMAGE_SHA256:
                    raise RuntimeError(f"missing/mistyped PF_ATTR_FIELD_SEMANTICS reference: {suffix}")
                continue
            if reference.startswith("PF_COMBAT_LIFECYCLE:"):
                suffix = reference.split(":", 1)[1]
                match = combat_by_id.get(suffix)
                if match is None or match["source"] != "IMAGE" or match["image_sha256"] != EXPECTED_IMAGE_SHA256:
                    raise RuntimeError(f"missing/mistyped PF_COMBAT_LIFECYCLE reference: {suffix}")
                continue
            if reference.startswith("PF_MONSTER_COLOR_GATE:"):
                suffix = reference.split(":", 1)[1]
                if not suffix:
                    raise RuntimeError("empty PF_MONSTER_COLOR_GATE reference")
                range_match = re.fullmatch(r"(.*?)(\d{3})\.\.(\d{3})", suffix)
                if range_match:
                    prefix, start_text, end_text = range_match.groups()
                    start = int(start_text)
                    end = int(end_text)
                    if not prefix or start > end:
                        raise RuntimeError(f"malformed PF_MONSTER_COLOR_GATE range: {suffix}")
                    referenced = [f"{prefix}{value:03d}" for value in range(start, end + 1)]
                elif ".." in suffix:
                    raise RuntimeError(f"malformed PF_MONSTER_COLOR_GATE range: {suffix}")
                else:
                    referenced = [suffix]
                for gate_key in referenced:
                    if gate_key not in old_by_key:
                        raise RuntimeError(f"missing PF_MONSTER_COLOR_GATE reference: {gate_key}")
                    if gate_key.startswith("MCG-IMG-") and old_by_key[gate_key].get("source") != "IMAGE":
                        raise RuntimeError(f"mistyped PF_MONSTER_COLOR_GATE IMAGE reference: {gate_key}")
                continue
            if reference:
                raise RuntimeError(f"unrecognized external reference: {reference}")


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


def render_report(
    rows: Sequence[Mapping[str, str]], metadata: Mapping[str, object]
) -> bytes:
    calls = metadata["calls"]
    refs = metadata["refs"]
    serializer_inventory = metadata["serializer_inventory"]
    direct_style_proved_count = metadata["direct_style_proved_count"]
    pair_sha256 = metadata["pair_sha256"]
    assert isinstance(calls, Mapping)
    assert isinstance(refs, Mapping)
    assert isinstance(serializer_inventory, Mapping)
    assert isinstance(direct_style_proved_count, int)
    primitive_total = len(calls[WRITE_PRIMITIVE]) + len(calls[READ_PRIMITIVE])
    lines = [
        "# PF Monster Color Wire / Control Census",
        "",
        "## Answer",
        "",
        "[MEASURED][IMAGE][BOUNDED][OPEN] No direct S2C field that supplies "
        "`FontStyleID` or an embedded `FontStyle` to the CNetNPC nameboard is proved by "
        "the audited literal/immediate, direct-E8 sink, and pinned typed-path surfaces. "
        "Direct wire control remains OPEN: variable-loaded fields, embedded structures, "
        "indirect/custom codecs, and undecoded serializer directions remain outside the proof.",
        "",
        "[MEASURED][IMAGE] On the audited CNetNPC path the client selects the final style "
        "ID locally, while the proved server influence is through upstream actor/Attr/event inputs.",
        "",
        "[PROPOSED] Do **not** add a guessed monster `FontStyleID` packet field. The bounded, "
        "evidence-aligned implementation surface is identity, relation/faction/category "
        "operands, death operands, NPC template identity, and conditional hit events.",
        "",
        "## Server-controllable inputs",
        "",
        "| Input | Control | Client-side consequence | Important boundary |",
        "|---|---|---|---|",
        "| [MEASURED][IMAGE] RuntimeRes actor type | Direct wire | type 4 constructs CNetNPC | does not prove gameplay class `monster` |",
        "| [MEASURED][IMAGE] RuntimeRes identity qword | Direct wire, invariant-constrained | signed high dword selects positive/nonpositive selector lane | registry/target identity safety is not proved for arbitrary negative values |",
        "| [MEASURED][IMAGE] BasicAttr +0x68 | Direct wire predicate operand | CNetNPC `n_FACTION` input to local relation logic | predicate has other inputs; no complete enum domain |",
        "| [MEASURED][IMAGE] ActorAttr +0x98 / +0x1A0 | Direct wire predicate operands | affect local relation/category selection | no universal gameplay labels for every value/owner |",
        "| [MEASURED][IMAGE] BasicAttr +0x44 / +0x58 | Direct wire operands | together form the exact CNetNPC death predicate | either operand alone is insufficient |",
        "| [MEASURED][IMAGE] NPCAttr +0x78 | Direct wire template key | chooses local MOBS/AI_WANDER row and therefore local `n_OFFESIVE` | `n_OFFESIVE` is not sent directly |",
        "| [MEASURED][IMAGE] CHitResult / CMissileHitResult identities | Indirect event control | can set unnamed actor bit `0x100`, later used by the local selector | handler gates and typed target must pass; bit is not named aggro |",
        "| [OPEN] Final FontStyleID / embedded style | no direct field proved on audited surfaces | emitted/applied locally on the audited CNetNPC path | variable/embedded/indirect/custom paths remain outside the bounded negative |",
        "",
        "## Bounded negative methodology",
        "",
        f"Image guard: size `{EXPECTED_IMAGE_SIZE}` bytes; SHA-256 `{EXPECTED_IMAGE_SHA256}`.",
        "",
        "The script parses the six PE sections and scans every byte position where a "
        "five-byte `E8 + rel32` encoding fits inside `min(VirtualSize, SizeOfRawData)`. "
        "This is a raw byte-pattern census; it does not infer instruction boundaries and "
        "therefore does not use a linear-disassembly negative.",
        "",
        f"- [MEASURED][IMAGE] Direct WRITE calls: {len(calls[WRITE_PRIMITIVE])}; site-list digest `{list_digest(calls[WRITE_PRIMITIVE])}`.",
        f"- [MEASURED][IMAGE] Direct READ calls: {len(calls[READ_PRIMITIVE])}; site-list digest `{list_digest(calls[READ_PRIMITIVE])}`.",
        f"- [MEASURED][IMAGE] Every one of those {primitive_total} sites was checked for raw `PUSH imm8` and "
        "`PUSH imm32` encodings of literal values 55..67 in the preceding 64-byte, "
        "same-section window: zero candidates.",
        f"- [MEASURED][IMAGE] Direct calls to the controller style store: {len(calls[CONTROLLER_STYLE_STORE])}; digest `{list_digest(calls[CONTROLLER_STYLE_STORE])}`.",
        f"- [MEASURED][IMAGE] Direct calls to the selector: {len(calls[COLOR_SELECTOR])}, exactly `0x004446A7`.",
        f"- [MEASURED][IMAGE] `FontStyleID` literal dword references: {len(refs[FONTSTYLE_ID_LITERAL])}; "
        f"embedded `FontStyle` references: {len(refs[EMBEDDED_STYLE_LITERAL])}. They are "
        "confined to the pinned GUI property/parser sites in this census.",
        "- [MEASURED][IMAGE] The selector, controller store, NPC label sink, style parsers, and the two "
        "direct UI style-setter forwarders contain zero direct WRITE/READ primitive calls.",
        "",
        "[OPEN] This negative excludes only those nearby literal-immediate patterns and the counted "
        "direct E8 edges into the audited sinks. It does not exclude a variable-loaded field, "
        "embedded structure, indirect call, custom codec, alias, whole-object copy, or "
        "transitive dataflow; therefore the global direct-wire question remains OPEN.",
        "",
        "## Pinned serializer-inventory ceiling",
        "",
        f"[MEASURED][IMAGE] The pinned IMAGE-derived serializer inventory "
        f"(SHA-256 `{serializer_inventory['sha256']}`) contains "
        f"{serializer_inventory['message_count']} messages and "
        f"{serializer_inventory['row_count']} rows. Of these, "
        f"{serializer_inventory['direct_rows']} rows use the audited direct primitive tag "
        f"set and {serializer_inventory['empty_count']} rows are EMPTY "
        f"({serializer_inventory['empty_w']} W, {serializer_inventory['empty_r']} R).",
        "",
        "[OPEN] Literal terms `FontStyleID`, `FontStyle`, and `LABEL_NAME` occur zero times "
        "in that pinned table. Term absence is not field or dataflow absence: the EMPTY "
        "directions and variable/embedded/indirect/custom paths still require tracing.",
        "",
        "## Conditional implementation boundary",
        "",
        "[PROPOSED] Claude has enough static evidence for a bounded experiment using the upstream "
        "inputs above. It is not yet evidence-safe to claim a production-complete color "
        "implementation, because arbitrary signed-negative identity policy, exact relation "
        "domains, complete bit writers, delivery order, nameboard readiness, and rendered "
        "outcomes remain unproved runtime facts.",
        "",
        "[PROPOSED] The narrowest next test is to vary one upstream input at a time while preserving "
        "actor registry/target identity and all readiness gates. A guessed direct style "
        "field is specifically unsupported.",
        "",
        "## Provenance and non-duplication",
        "",
        "Every TSV row is `source=IMAGE` and carries a primary VA range, file-offset range, "
        "and span SHA-256. Existing mechanism facts are cited through `reference_keys`. New "
        "claim/evidence keys are unique, but uniqueness does not mean independent evidence: "
        "reference rows and the final control row are joins/syntheses and are not counted as "
        "new independent mechanism proof. The verifier rejects reused gate evidence keys and "
        "missing or malformed gate IDs/ranges.",
        "",
        "[OPEN][DELIVERY] These artifacts are local-only in `pf_bridge/external`, outside "
        "the canonical ServerProject Git worktree, and therefore untracked by that worktree. "
        "Another clone needs owner-approved packaging/ingest through "
        "`PF_CRITICAL_ARTIFACT_AUTHORITY`; availability must not be assumed.",
        "",
        f"Artifact pair SHA-256: `{pair_sha256}`. The same value is present in every TSV row; "
        "a mixed-generation TSV/Markdown pair is therefore detectable.",
        "",
        f"Rows: {len(rows)}. Direct style-wire fields proved: "
        f"{direct_style_proved_count}. Status: OPEN.",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


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
        b"PF_MONSTER_COLOR_WIRE_CONTROL_TSV\x00"
        + normalized_tsv
        + b"\x00PF_MONSTER_COLOR_WIRE_CONTROL_MD\x00"
        + normalized_report
    )
    replacement = pair_sha256.encode("ascii")
    outputs = {
        TSV_PATH: normalized_tsv.replace(placeholder, replacement),
        REPORT_PATH: normalized_report.replace(placeholder, replacement),
    }
    # Re-normalize the finished payloads and prove the injected key covers both
    # complete artifacts rather than only their row identities.
    finished_tsv = outputs[TSV_PATH]
    finished_report = outputs[REPORT_PATH]
    if finished_tsv.count(replacement) != len(rows):
        raise RuntimeError("TSV pair-key injection mismatch")
    if finished_report.count(replacement) != 1:
        raise RuntimeError("Markdown pair-key injection mismatch")
    rederived = sha256(
        b"PF_MONSTER_COLOR_WIRE_CONTROL_TSV\x00"
        + finished_tsv.replace(replacement, placeholder)
        + b"\x00PF_MONSTER_COLOR_WIRE_CONTROL_MD\x00"
        + finished_report.replace(replacement, placeholder)
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
                fd, temp_name = tempfile.mkstemp(
                    prefix=path.name + ".", suffix=".tmp", dir=path.parent
                )
                temp_path = Path(temp_name)
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
        published_rows = list(csv.DictReader(handle, delimiter="\t"))
    if not published_rows or "artifact_pair_sha256" not in published_rows[0]:
        raise RuntimeError("published TSV pair-key schema drift")
    tsv_keys = {row.get("artifact_pair_sha256", "") for row in published_rows}
    if len(tsv_keys) != 1:
        raise RuntimeError("published TSV contains mixed pair keys")
    pair_key = next(iter(tsv_keys))
    if not re.fullmatch(r"[0-9a-f]{64}", pair_key):
        raise RuntimeError("published TSV pair key is malformed")
    report_match = re.search(
        rb"Artifact pair SHA-256: `([0-9a-f]{64})`", report_raw
    )
    if report_match is None or report_match.group(1).decode("ascii") != pair_key:
        raise RuntimeError("published TSV/Markdown pair keys disagree")
    key_raw = pair_key.encode("ascii")
    placeholder = PAIR_PLACEHOLDER.encode("ascii")
    if tsv_raw.count(key_raw) != len(published_rows) or report_raw.count(key_raw) != 1:
        raise RuntimeError("published pair-key occurrence count drift")
    rederived = sha256(
        b"PF_MONSTER_COLOR_WIRE_CONTROL_TSV\x00"
        + tsv_raw.replace(key_raw, placeholder)
        + b"\x00PF_MONSTER_COLOR_WIRE_CONTROL_MD\x00"
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


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="ascii", errors="backslashreplace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="ascii", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify outputs without writing")
    args = parser.parse_args()

    before_stat = IMAGE_PATH.stat()
    if before_stat.st_size != EXPECTED_IMAGE_SIZE:
        raise RuntimeError("image size guard failed")
    image = IMAGE_PATH.read_bytes()
    if len(image) != EXPECTED_IMAGE_SIZE or sha256(image) != EXPECTED_IMAGE_SHA256:
        raise RuntimeError("image hash guard failed")

    rows, metadata = derive(image)
    validate_reference_separation(rows)
    outputs, pair_sha256 = render_outputs(rows, metadata)

    after_stat = IMAGE_PATH.stat()
    if (
        before_stat.st_size != after_stat.st_size
        or before_stat.st_mtime_ns != after_stat.st_mtime_ns
        or sha256(IMAGE_PATH.read_bytes()) != EXPECTED_IMAGE_SHA256
    ):
        raise RuntimeError("image changed during derivation")

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
