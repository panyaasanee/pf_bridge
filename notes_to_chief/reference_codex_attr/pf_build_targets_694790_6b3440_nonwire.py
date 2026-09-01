#!/usr/bin/env python3
"""Build the IMAGE-only non-wire removal overlay for 0x694790/0x6B3440."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import struct
import tempfile
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable, Mapping, Sequence


IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
A2_SHA256 = "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
SLOT34_A2_SHA256 = "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334"
PRIORITY_SHA256 = "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"
SLOT34_PRIORITY_SHA256 = "00ef0f3cb632b40ba168ce79bbd656fc7a6936a55f3b3e185c6e63b32c39ec5d"

A2_NAME = "PF_SERIALIZER_FIELDS.tsv"
SLOT34_A2_NAME = "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
PRIORITY_NAME = "PF_PROTOCOL_PRIORITY.tsv"
SLOT34_PRIORITY_NAME = "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv"
OUTPUT_NAME = "PF_TARGETS_694790_6B3440_A2_DELTA.tsv"
REPORT_NAME = "PF_TARGETS_694790_6B3440_NONWIRE.md"
TICKET = "STATIC-TARGETS-694790-6B3440"
VA_TO_FILE_DELTA = 0x00400C00
TAGS = (
    "CALL_UNCLASSIFIED:0x00694790",
    "CALL_UNCLASSIFIED:0x006B3440",
)

P1_MESSAGES = (
    "ActorExpressData",
    "Express_InitalizeActorExpressVital",
    "GSCN_LoginProtocol",
    "ItemMallPersonalGiftVital",
    "PartyUpdateVital",
    "PlayerSearchVitalRes",
    "VitalProtocol",
)
P3_MESSAGES = (
    "GSCN_RunTimeProtocolReq",
    "GSCN_RunTimeProtocolRes",
    "LSCN_Protocol",
)
ALL_MESSAGES = P1_MESSAGES + P3_MESSAGES


@dataclass(frozen=True)
class SpanPin:
    role: str
    start: int
    end: int
    off: int
    sha256: str


SPANS = (
    SpanPin("size_increment", 0x00694790, 0x0069481A, 0x00293B90, "62b074c5ba49c9d91c06f56ffb509eb6e609170b0c49bbc9c69c629e621d9f98"),
    SpanPin("node_allocate", 0x006B3440, 0x006B34D2, 0x002B2840, "e03507a26af6b8954d07e08b7d34b82925324f114c95943fa79297352af3e4b3"),
    SpanPin("exception_copy", 0x00401030, 0x0040108F, 0x00000430, "e8a0c69b0a0053ea46a9877c9e1dca61a8671b5c692b5b3d979026bc4a5d4bc6"),
    SpanPin("smart_ref_copy", 0x0069D040, 0x0069D09A, 0x0029C440, "b79870afe41d0111715a239fd6137b54216374300befa0ee0b4e9601e280b2f8"),
    SpanPin("ref_increment", 0x0088D050, 0x0088D05B, 0x0048C450, "6da78a1acc15d9fd5f7b2d620253debf8d8465136165dfb1eae35914b2442845"),
    SpanPin("ref_decrement", 0x0088D060, 0x0088D082, 0x0048C460, "d3b546ac50ded491a6c5a196138b9691f23d8499298e728925f1afb1f0e7734c"),
    SpanPin("operator_new_thunk", 0x00B37980, 0x00B37986, 0x00736D80, "026db59c9509fd5984356ee06312c76482b74741604ce391ee977c41473b76e4"),
    SpanPin("operator_delete_thunk", 0x00B37952, 0x00B37958, 0x00736D52, "dac5c7df4ee9addc4293b8459a55d2bc3eb5864debafc857fb97c01fbbb07cf8"),
    SpanPin("cxx_throw_thunk", 0x00B37998, 0x00B3799E, 0x00736D98, "16bf8ff4ff7050398899b806680db04f97c42d1b2f69ba2f4eed563eae73ba16"),
    SpanPin("shared_serializer", 0x005F3E20, 0x005F406D, 0x001F3220, "bfdf1ada48068e9a3838b51241e164677e0142a6ce0f6d68d547299fe279e217"),
    SpanPin("party_serializer", 0x00627730, 0x00627942, 0x00226B30, "dae58227a8f755839eaa6343699a7782137ea5364f089b403cf02ae63d945935"),
    SpanPin("player_search_serializer", 0x00694820, 0x006949C3, 0x00293C20, "e26789d1ea041e2321860520737dcd564aa2b4eb82b6fac2bfa25837b54d54df"),
    SpanPin("personal_gift_serializer", 0x006B2230, 0x006B23A6, 0x002B1630, "1d05f5d3dd6dbf2e6a86eaebefaba5313146d83ce7d678e29ca7c4fc0fcad6b3"),
    SpanPin("actor_express_serializer", 0x006E3EF0, 0x006E4142, 0x002E32F0, "9d533f91678a951228c059201bf22d160b6a685f2cb4a4aafddc89ed16ecab21"),
    SpanPin("express_initialize_serializer", 0x006E8150, 0x006E82E4, 0x002E7550, "1954451838b7b206d97e228357393475609a4074d88411cf83410de43e8a033d"),
)


@dataclass(frozen=True)
class CallerPin:
    role: str
    messages: tuple[str, ...]
    call_node: int
    call_size: int
    member: str
    stream: str
    mode_branch: tuple[int, str, int] | None
    read_anchor: tuple[int, int]
    pins: tuple[tuple[int, str], ...]


CALLERS = (
    CallerPin(
        "shared_serializer",
        ("GSCN_RunTimeProtocolReq", "GSCN_RunTimeProtocolRes", "GSCN_LoginProtocol", "LSCN_Protocol", "VitalProtocol"),
        0x005F3F75, 0x005F3F81, "owner+0x10; sentinel owner+0x24", "entry+0x4 -> EDI", None,
        (0x005F3E6C, 0x0089A640),
        ((0x005F3E51, "8b7d08"), (0x005F3E5C, "894db4"), (0x005F3F55, "e8f6902900"),
         (0x005F3F5A, "8b7db4"), (0x005F3F5D, "8b5f24"), (0x005F3F63, "83c710"),
         (0x005F3F66, "8d45b8"), (0x005F3F89, "894304"), (0x005F3F8F, "8901"),
         (0x005F3F9A, "e8c1902900")),
    ),
    CallerPin(
        "party_serializer", ("PartyUpdateVital",), 0x006278D9, 0x006278E4,
        "this+0x28; sentinel this+0x3C", "entry+0x4 -> EDI", (0x0062776C, "0f84c5000000", 0x00627837),
        (0x00627837, 0x0089A640),
        ((0x00627757, "8bf1"), (0x00627759, "807c243000"), (0x0062775E, "8b7c242c"),
         (0x0062788D, "8d5e28"), (0x006278CA, "8b7314"), (0x006278D0, "8d542418"),
         (0x006278E9, "897e04"), (0x006278EF, "8938"), (0x006278FF, "e85c572600")),
    ),
    CallerPin(
        "player_search_serializer", ("PlayerSearchVitalRes",), 0x0069496A, 0x00694975,
        "this+0x10; sentinel this+0x24", "entry+0x4 -> ECX on read branch", (0x00694854, "0f849d000000", 0x006948F7),
        (0x00694907, 0x0089A640),
        ((0x00694847, "8bf1"), (0x0069484D, "807c243400"), (0x006948F7, "8b4c2434"),
         (0x00694939, "e812871f00"), (0x00694958, "8b7e24"), (0x0069495E, "83c610"),
         (0x00694961, "8d4c2418"), (0x0069497E, "896f04"), (0x00694984, "8928"),
         (0x00694994, "e8c7861f00")),
    ),
    CallerPin(
        "personal_gift_serializer", ("ItemMallPersonalGiftVital",), 0x006B2359, 0x006B2364,
        "this+0x10; sentinel this+0x24", "entry+0x4 -> ECX on read branch", (0x006B2260, "0f8481000000", 0x006B22E7),
        (0x006B22F8, 0x0089A640),
        ((0x006B2257, "8bd9"), (0x006B2259, "807c243000"), (0x006B22EC, "8b4c2434"),
         (0x006B230E, "83c310"), (0x006B2331, "e81aad1d00"), (0x006B234A, "8b7314"),
         (0x006B2350, "8d442418"), (0x006B2369, "897e04"), (0x006B236F, "8bcd"),
         (0x006B2373, "c7442424ffffffff"), (0x006B237B, "e8e0ac1d00")),
    ),
    CallerPin(
        "actor_express_serializer", ("ActorExpressData",), 0x006E403A, 0x006E4045,
        "this+0x30; sentinel this+0x44", "entry+0x4 -> EBP on read branch", (0x006E3F2A, "0f848e000000", 0x006E3FBE),
        (0x006E3FC4, 0x0089A640),
        ((0x006E3F17, "8bf1"), (0x006E3F1D, "807c243800"), (0x006E3FBE, "8b6c2440"),
         (0x006E400D, "e83e901a00"), (0x006E4028, "8b7e44"), (0x006E402E, "83c630"),
         (0x006E4031, "8d4c2420"), (0x006E404A, "896f04"), (0x006E4052, "8928"),
         (0x006E405C, "e8ff8f1a00")),
    ),
    CallerPin(
        "express_initialize_serializer", ("Express_InitalizeActorExpressVital",), 0x006E8291, 0x006E829C,
        "this+0x28; sentinel this+0x3C", "entry+0x4 -> EDI", (0x006E8190, "747b", 0x006E820D),
        (0x006E820D, 0x0089A640),
        ((0x006E8177, "8bf1"), (0x006E817D, "807c243400"), (0x006E8182, "8b7c2430"),
         (0x006E8269, "e8e24d1a00"), (0x006E827F, "8b7e3c"), (0x006E8285, "83c628"),
         (0x006E8288, "8d4c241c"), (0x006E82A1, "896f04"), (0x006E82A9, "8928"),
         (0x006E82B3, "e8a84d1a00")),
    ),
)

IMPORTS = {
    0x00C3B1B0: ("KERNEL32.dll", "InterlockedIncrement"),
    0x00C3B1B4: ("KERNEL32.dll", "InterlockedDecrement"),
    0x00C3B480: ("MSVCP90.dll", "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@PBD@Z"),
    0x00C3B49C: ("MSVCP90.dll", "??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@ABV01@@Z"),
    0x00C3B4BC: ("MSVCR90.dll", "??2@YAPAXI@Z"),
    0x00C3B4C4: ("MSVCR90.dll", "_CxxThrowException"),
    0x00C3B828: ("MSVCR90.dll", "??0exception@std@@QAE@XZ"),
    0x00C3B82C: ("MSVCR90.dll", "??3@YAXPAX@Z"),
}

A2_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "direction(W/R)", "old_order", "old_tag", "old_field_offset",
    "old_len", "new_wire_order", "new_tag", "new_field_offset", "new_len", "new_gate_condition",
    "resolution", "evidence_ticket", "evidence_span_start", "evidence_span_end",
    "evidence_span_sha256", "evidence_file_off", "source",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_hash(path: Path, expected: str) -> None:
    actual = sha_path(path)
    if actual != expected:
        raise RuntimeError(f"hash drift: {path.name}: {actual}")


def row_key(fields: Sequence[str], row: Mapping[str, str]) -> str:
    return sha(json.dumps([row[k] for k in fields], ensure_ascii=False, separators=(",", ":")).encode())


def delta_key(parts: Iterable[str]) -> str:
    return sha("\x1f".join(parts).encode())


def read_tsv(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames is None:
            raise RuntimeError(f"missing header: {path}")
        fields = list(reader.fieldnames)
        return fields, [(n, dict(r)) for n, r in enumerate(reader, 2)]


def tsv_text(rows: Sequence[Mapping[str, str]]) -> str:
    out = StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=A2_COLUMNS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def atomic_write(path: Path, text: str) -> None:
    temp: str | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=path.parent,
                                         prefix=f".{path.name}.", suffix=".tmp", delete=False) as f:
            temp = f.name
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if temp and os.path.exists(temp):
            os.unlink(temp)


def at(image: bytes, va: int, size: int) -> bytes:
    off = va - VA_TO_FILE_DELTA
    if off < 0 or off + size > len(image):
        raise RuntimeError(f"VA outside image: 0x{va:08X}")
    return image[off:off + size]


def require_bytes(image: bytes, va: int, expected: str) -> None:
    raw = bytes.fromhex(expected)
    if at(image, va, len(raw)) != raw:
        raise RuntimeError(f"byte pin drift at 0x{va:08X}")


def rel_target(image: bytes, site: int) -> int:
    raw = at(image, site, 5)
    if raw[0] != 0xE8:
        raise RuntimeError(f"not a direct call: 0x{site:08X}")
    return site + 5 + struct.unpack_from("<i", raw, 1)[0]


def verify_rel_set(image: bytes, pin: SpanPin, expected: Mapping[int, int]) -> None:
    body = at(image, pin.start, pin.end - pin.start)
    sites = [pin.start + i for i, byte in enumerate(body) if byte == 0xE8]
    actual = {site: rel_target(image, site) for site in sites}
    if actual != dict(expected):
        raise RuntimeError(f"direct-call census drift: {pin.role}: {actual}")


def import_map(image: bytes) -> dict[int, tuple[str, str]]:
    pe = struct.unpack_from("<I", image, 0x3C)[0]
    coff = pe + 4
    count = struct.unpack_from("<H", image, coff + 2)[0]
    optional_size = struct.unpack_from("<H", image, coff + 16)[0]
    optional = coff + 20
    base = struct.unpack_from("<I", image, optional + 28)[0]
    headers = struct.unpack_from("<I", image, optional + 60)[0]
    sections = []
    for i in range(count):
        off = optional + optional_size + i * 40
        vs, va, rs, rp = struct.unpack_from("<IIII", image, off + 8)
        sections.append((va, vs, rp, rs))

    def rva_off(rva: int) -> int:
        if rva < headers:
            return rva
        for va, vs, rp, rs in sections:
            d = rva - va
            if 0 <= d < rs and d < max(vs, rs):
                return rp + d
        raise RuntimeError(f"unmapped RVA 0x{rva:08X}")

    def zstr(off: int) -> str:
        end = image.find(b"\0", off)
        return image[off:end].decode("ascii")

    import_rva = struct.unpack_from("<I", image, optional + 104)[0]
    result: dict[int, tuple[str, str]] = {}
    descriptor = import_rva
    while True:
        off = rva_off(descriptor)
        oft, timestamp, forwarder, name_rva, first_thunk = struct.unpack_from("<IIIII", image, off)
        if not any((oft, timestamp, forwarder, name_rva, first_thunk)):
            break
        dll = zstr(rva_off(name_rva))
        i = 0
        while True:
            thunk = struct.unpack_from("<I", image, rva_off((oft or first_thunk) + i * 4))[0]
            if not thunk:
                break
            if not thunk & 0x80000000:
                result[base + first_thunk + i * 4] = (dll, zstr(rva_off(thunk) + 2))
            i += 1
        descriptor += 20
    return result


def verify_image(image: bytes) -> None:
    if sha(image) != IMAGE_SHA256:
        raise RuntimeError("IMAGE hash drift")
    by_role = {p.role: p for p in SPANS}
    for pin in SPANS:
        if pin.start - VA_TO_FILE_DELTA != pin.off or sha(at(image, pin.start, pin.end - pin.start)) != pin.sha256:
            raise RuntimeError(f"span drift: {pin.role}")

    # Complete helper CFG/call/return and EH pins.
    require_bytes(image, 0x006947C4, "733c")
    require_bytes(image, 0x00694817, "c20400")
    verify_rel_set(image, by_role["size_increment"], {0x006947E6: 0x00401030, 0x006947FD: 0x00B37998})
    require_bytes(image, 0x006947CF, "ff1580b4c300")
    require_bytes(image, 0x006947B4, "8b4118")
    require_bytes(image, 0x006947B7, "8b54245c")
    require_bytes(image, 0x00694802, "03c2894118")

    for va, raw in ((0x006B3483, "7405"), (0x006B348F, "7405"), (0x006B34B9, "c20c00"), (0x006B34D1, "cc")):
        require_bytes(image, va, raw)
    verify_rel_set(image, by_role["node_allocate"], {
        0x006B346D: 0x00B37980, 0x006B349E: 0x0069D040,
        0x006B34C0: 0x00B37952, 0x006B34CC: 0x00B37998,
    })
    for va, raw in ((0x006B346B, "6a0c"), (0x006B3485, "8b45088906"),
                    (0x006B3491, "8b4d0c8908"), (0x006B3496, "8b5510528d460850")):
        require_bytes(image, va, raw)
    verify_rel_set(image, by_role["smart_ref_copy"], {0x0069D085: 0x0088D050})
    for va, raw in ((0x0069D061, "8b442418"), (0x0069D079, "8b4c241c8b098908"),
                    (0x0088D050, "83c10c51ff15b0b1c300c3"),
                    (0x0088D063, "8d460c50ff15b4b1c300"),
                    (0x00B37980, "ff25bcb4c300"), (0x00B37952, "ff252cb8c300"),
                    (0x00B37998, "ff25c4b4c300")):
        require_bytes(image, va, raw)

    imports = import_map(image)
    for iat, expected in IMPORTS.items():
        if imports.get(iat) != expected:
            raise RuntimeError(f"import drift at 0x{iat:08X}: {imports.get(iat)}")
    for va, raw in ((0x00401058, "ff1528b8c300"), (0x00401074, "ff159cb4c300"),
                    (0x0088D054, "ff15b0b1c300"), (0x0088D067, "ff15b4b1c300")):
        require_bytes(image, va, raw)

    for caller in CALLERS:
        for va, raw in caller.pins:
            require_bytes(image, va, raw)
        if rel_target(image, caller.call_node) != 0x006B3440 or rel_target(image, caller.call_size) != 0x00694790:
            raise RuntimeError(f"caller target drift: {caller.role}")
        span = by_role[caller.role]
        node_encoding = at(image, caller.call_node, 5)
        size_encoding = at(image, caller.call_size, 5)
        if at(image, span.start, span.end - span.start).count(node_encoding) != 1:
            raise RuntimeError(f"node call census drift: {caller.role}")
        if at(image, span.start, span.end - span.start).count(size_encoding) != 1:
            raise RuntimeError(f"size call census drift: {caller.role}")
        if rel_target(image, caller.read_anchor[0]) != caller.read_anchor[1]:
            raise RuntimeError(f"read primitive drift: {caller.role}")
        if caller.mode_branch:
            site, raw_hex, target = caller.mode_branch
            require_bytes(image, site, raw_hex)
            raw = bytes.fromhex(raw_hex)
            disp = struct.unpack("b", raw[1:2])[0] if len(raw) == 2 else struct.unpack_from("<i", raw, 2)[0]
            if site + len(raw) + disp != target or caller.call_node <= target:
                raise RuntimeError(f"read-branch provenance drift: {caller.role}")

    helper_calls = {0x00401030, 0x00B37998, 0x00B37980, 0x0069D040, 0x00B37952, 0x0088D050}
    if helper_calls & {0x0089A600, 0x0089A640}:
        raise RuntimeError("wire primitive reached by helper")


def caller_for(message: str) -> CallerPin:
    found = [c for c in CALLERS if message in c.messages]
    if len(found) != 1:
        raise RuntimeError(f"caller map drift: {message}")
    return found[0]


BASE_EXPECTED = {
    133: ("GSCN_RunTimeProtocolReq", "R", TAGS[1]), 134: ("GSCN_RunTimeProtocolReq", "R", TAGS[0]),
    174: ("GSCN_RunTimeProtocolRes", "R", TAGS[1]), 175: ("GSCN_RunTimeProtocolRes", "R", TAGS[0]),
    321: ("GSCN_LoginProtocol", "R", TAGS[1]), 322: ("GSCN_LoginProtocol", "R", TAGS[0]),
    1304: ("LSCN_Protocol", "R", TAGS[1]), 1305: ("LSCN_Protocol", "R", TAGS[0]),
    1441: ("VitalProtocol", "R", TAGS[1]), 1442: ("VitalProtocol", "R", TAGS[0]),
    1871: ("PartyUpdateVital", "W", TAGS[1]), 1872: ("PartyUpdateVital", "W", TAGS[0]),
    1930: ("PartyUpdateVital", "R", TAGS[1]), 1931: ("PartyUpdateVital", "R", TAGS[0]),
    4197: ("PlayerSearchVitalRes", "W", TAGS[1]), 4198: ("PlayerSearchVitalRes", "W", TAGS[0]),
    4226: ("PlayerSearchVitalRes", "R", TAGS[1]), 4227: ("PlayerSearchVitalRes", "R", TAGS[0]),
    4753: ("ItemMallPersonalGiftVital", "W", TAGS[1]), 4754: ("ItemMallPersonalGiftVital", "W", TAGS[0]),
    4774: ("ItemMallPersonalGiftVital", "R", TAGS[1]), 4775: ("ItemMallPersonalGiftVital", "R", TAGS[0]),
    5385: ("Express_InitalizeActorExpressVital", "R", TAGS[1]), 5386: ("Express_InitalizeActorExpressVital", "W", TAGS[1]),
    5387: ("Express_InitalizeActorExpressVital", "R", TAGS[0]), 5388: ("Express_InitalizeActorExpressVital", "W", TAGS[0]),
}
SLOT_EXPECTED = {
    288: ("ActorExpressData", "R", TAGS[1]), 289: ("ActorExpressData", "W", TAGS[1]),
    290: ("ActorExpressData", "R", TAGS[0]), 291: ("ActorExpressData", "W", TAGS[0]),
}


def make_row(fields: Sequence[str], line: int, row: Mapping[str, str], base_file: str,
             action: str, overlay: bool) -> dict[str, str]:
    caller = caller_for(row["message"])
    span = next(p for p in SPANS if p.role == caller.role)
    tag = row["new_tag"] if overlay else row["tag"]
    call = caller.call_size if tag == TAGS[0] else caller.call_node
    values = {
        "action": action,
        "change_type": "NONWIRE_LIST_NODE_AND_SIZE_LIFECYCLE_AFTER_STREAM_READ",
        "base_file": base_file,
        "base_line": str(line),
        "base_row_key": row_key(fields, row),
        "base_delta_key": row["delta_key"] if overlay else "N/A",
        "message": row["message"],
        "direction(W/R)": row["direction(W/R)"],
        "old_order": row["new_order"] if overlay else row["order"],
        "old_tag": tag,
        "old_field_offset": row["new_field_offset"] if overlay else row["field_offset"],
        "old_len": row["new_len"] if overlay else row["len"],
        "new_wire_order": "N/A", "new_tag": "N/A", "new_field_offset": "N/A", "new_len": "N/A",
        "new_gate_condition": "N/A",
        "resolution": "FIXED_12_BYTE_LIST_NODE_AND_SIZE_INCREMENT;NO_STREAM_FORMAL;ZERO_MODE_READ_BRANCH_ONLY",
        "evidence_ticket": TICKET,
        "evidence_span_start": f"0x{span.start:08X}",
        "evidence_span_end": f"0x{span.end:08X}",
        "evidence_span_sha256": span.sha256,
        "evidence_file_off": f"0x{call - VA_TO_FILE_DELTA:08X}",
        "source": "IMAGE",
    }
    values["delta_key"] = delta_key(("A2", action, base_file, str(line), values["base_row_key"]))
    return values


def build_delta(base_fields: Sequence[str], base_rows: Sequence[tuple[int, dict[str, str]]],
                slot_fields: Sequence[str], slot_rows: Sequence[tuple[int, dict[str, str]]]) -> list[dict[str, str]]:
    base_hits = [(n, r) for n, r in base_rows if r.get("tag") in TAGS]
    actual = {n: (r["message"], r["direction(W/R)"], r["tag"]) for n, r in base_hits}
    if actual != BASE_EXPECTED:
        raise RuntimeError(f"V1 census drift: {actual}")
    slot_hits = [(n, r) for n, r in slot_rows if r.get("new_tag") in TAGS]
    slot_actual = {n: (r["message"], r["direction(W/R)"], r["new_tag"]) for n, r in slot_hits}
    if slot_actual != SLOT_EXPECTED:
        raise RuntimeError(f"slot census drift: {slot_actual}")

    output = []
    for n, r in base_hits:
        caller = caller_for(r["message"])
        span = next(p for p in SPANS if p.role == caller.role)
        call = caller.call_size if r["tag"] == TAGS[0] else caller.call_node
        if r["source"] != "IMAGE" or r["field_offset"] != "UNKNOWN(direct_call_not_proven_serializer)":
            raise RuntimeError(f"V1 evidence drift at {n}")
        if r["span_start"] != f"0x{span.start:08X}" or r["span_sha256"] != span.sha256 or r["file_off_claim"] != f"0x{call - VA_TO_FILE_DELTA:08X}":
            raise RuntimeError(f"V1 provenance drift at {n}")
        output.append(make_row(base_fields, n, r, A2_NAME, "REMOVE_NONWIRE_ROW", False))
    for n, r in slot_hits:
        caller = caller_for(r["message"])
        span = next(p for p in SPANS if p.role == caller.role)
        call = caller.call_size if r["new_tag"] == TAGS[0] else caller.call_node
        if r["action"] != "ADD_CORRECTED_SLOT34_ROW" or r["source"] != "IMAGE":
            raise RuntimeError(f"slot evidence drift at {n}")
        if r["new_span_start"] != f"0x{span.start:08X}" or r["new_span_sha256"] != span.sha256 or r["new_file_off_claim"] != f"0x{call - VA_TO_FILE_DELTA:08X}":
            raise RuntimeError(f"slot provenance drift at {n}")
        output.append(make_row(slot_fields, n, r, SLOT34_A2_NAME, "REMOVE_OVERLAY_NONWIRE_ROW", True))
    output.sort(key=lambda r: (r["base_file"], int(r["base_line"])))
    identities = {(r["base_file"], r["base_line"], r["base_row_key"]) for r in output}
    if len(output) != 30 or len(identities) != 30 or len({r["delta_key"] for r in output}) != 30:
        raise RuntimeError("duplicate or incomplete output")
    if any(r["source"] != "IMAGE" for r in output):
        raise RuntimeError("mixed source")
    if any("UNCHANGED" in "\t".join(r.values()) or "COPIED" in "\t".join(r.values()) for r in output):
        raise RuntimeError("unchanged/copied row forbidden")
    return output


def verify_overlays(external: Path, delta: Sequence[Mapping[str, str]]) -> None:
    wanted = {(r["base_file"], r["base_line"], r["base_row_key"]) for r in delta}
    overlap = []
    for path in sorted(external.glob("*DELTA.tsv")):
        if path.name == OUTPUT_NAME:
            continue
        fields, rows = read_tsv(path)
        if not {"base_file", "base_line", "base_row_key"}.issubset(fields):
            continue
        for n, r in rows:
            if (r["base_file"], r["base_line"], r["base_row_key"]) in wanted:
                overlap.append(f"{path.name}:{n}")
    if overlap:
        raise RuntimeError("cross-overlay overlap: " + ", ".join(overlap))

    occurrences: dict[str, int] = {}
    for path in sorted(external.glob("*.tsv")):
        if path.name == OUTPUT_NAME:
            continue
        fields, rows = read_tsv(path)
        count = 0
        if "tag" in fields:
            count += sum(r.get("tag") in TAGS for _, r in rows)
        if "new_tag" in fields:
            count += sum(r.get("new_tag") in TAGS for _, r in rows)
        if count:
            occurrences[path.name] = count
    if occurrences != {A2_NAME: 26, SLOT34_A2_NAME: 4}:
        raise RuntimeError(f"effective census drift: {occurrences}")


def priority_residuals(external: Path) -> list[tuple[str, str, str]]:
    _, base = read_tsv(external / PRIORITY_NAME)
    by_message = {r["message"]: r for _, r in base}
    _, slot = read_tsv(external / SLOT34_PRIORITY_NAME)
    actor = [r for _, r in slot if r["message"] == "ActorExpressData"]
    if len(actor) != 1 or actor[0]["new_serializer_status"] != "OPEN":
        raise RuntimeError("ActorExpressData effective Priority drift")
    result = []
    for message in ALL_MESSAGES:
        if message == "ActorExpressData":
            priority = "1"
            blockers = actor[0]["new_serializer_blockers"]
        else:
            row = by_message[message]
            priority = row["priority"]
            blockers = row["serializer_blockers"]
            if row["serializer_status"] != "OPEN":
                raise RuntimeError(f"Priority status drift: {message}")
        expected_priority = "1" if message in P1_MESSAGES else "3"
        if priority != expected_priority or "direct_call_not_proven_serializer" not in blockers:
            raise RuntimeError(f"Priority/blocker drift: {message}")
        other = [x.strip() for x in blockers.split("|") if x.strip() != "direct_call_not_proven_serializer"]
        if not other:
            raise RuntimeError(f"no residual blocker: {message}")
        result.append((message, priority, " | ".join(other)))
    return result


def report_text(residuals: Sequence[tuple[str, str, str]]) -> str:
    lines = [
        "# IMAGE closure: targets 0x00694790 and 0x006B3440", "",
        "[MEASURED] Additive removal-only correction. Frozen V1 and slot-0x34 inputs are unchanged.", "",
        "## Outcome", "",
        "- Removed **30 effective A2 analysis artifacts**: 26 frozen-V1 rows and 4 slot-0x34 overlay rows.",
        "- Effective census is **10 messages: 7 Priority-1 and 3 Priority-3**. The assignment's earlier 'six P1' count omitted slot-0x34 `ActorExpressData`, whose effective Priority overlay is OPEN.",
        "- Counts are R=20, W=10. The ten W rows are path-insensitive duplicates: each of the five directional serializers has one physical call pair, located only in its pinned zero-mode/read branch.",
        "- The 30 directives have 0 unchanged copies, 0 duplicate base rows, and 0 cross-overlay base-row overlaps. Every row has `source=IMAGE`.",
        "- No Priority delta is emitted. All ten messages remain OPEN because independent blockers remain; the broad direct-call blocker category is not edited by this target-specific overlay.", "",
        "## Proven non-wire structure", "",
        "`0x006B3440` allocates one fixed 12-byte list node, stores its first two caller arguments at node +0/+4, and copies the third smart-reference argument into node +8 through `0x0069D040`. Its normal CFG has block starts 0x006B3440, 0x006B3485, 0x006B348A, 0x006B3491 and 0x006B3496; the separately pinned EH cleanup starts at 0x006B34BC. Calls are exactly operator-new, smart-reference copy, EH operator-delete, and C++ throw; normal return is `ret 12`.", "",
        "`0x00694790` reads only container +0x18 and its one stack argument. Its three-block CFG starts at 0x00694790, 0x006947C6 and 0x00694802: success adds the argument (always 1 at these six callers) to container +0x18; overflow constructs and throws an exception. It returns `ret 4`.", "",
        "The smart-reference support copies the payload pointer and calls the pinned InterlockedIncrement wrapper only when non-null. Each caller then links the node through the sentinel/tail and releases its temporary ownership through the pinned InterlockedDecrement wrapper. Neither target has a stream formal, neither target/support call set reaches wire primitives 0x0089A600 or 0x0089A640, and the PE imports/EH thunks are pinned by address, symbol and full IMAGE span hash.", "",
        "No key/value, actor, party, item, or gameplay semantics are inferred from names or nearby strings.", "",
        "## Caller and effective-row census", "",
        "| caller/messages | span SHA-256 | node/size calls | container member | stream provenance | V1 rows | slot rows |",
        "|---|---|---|---|---|---:|---:|",
    ]
    counts = {
        "shared_serializer": (10, 0), "party_serializer": (4, 0), "player_search_serializer": (4, 0),
        "personal_gift_serializer": (4, 0), "actor_express_serializer": (0, 4),
        "express_initialize_serializer": (4, 0),
    }
    for caller in CALLERS:
        span = next(p for p in SPANS if p.role == caller.role)
        messages = ", ".join(f"`{m}`" for m in caller.messages)
        v1, slot = counts[caller.role]
        lines.append(f"| {messages} | `{span.sha256}` | `0x{caller.call_node:08X}` / `0x{caller.call_size:08X}` | {caller.member} | {caller.stream}; target pair receives list/node args, not stream | {v1} | {slot} |")
    lines += ["", "## Pinned spans", "", "| role | VA span (end exclusive) | bytes | file offset | SHA-256 |", "|---|---|---:|---:|---|"]
    for pin in SPANS:
        lines.append(f"| {pin.role} | `0x{pin.start:08X}-0x{pin.end:08X}` | {pin.end-pin.start} | `0x{pin.off:08X}` | `{pin.sha256}` |")
    lines += ["", "## Residual Priority blockers", "",
              "The table lists blockers other than the broad direct-call category. That category is also left untouched because other direct targets may still contribute to it.", "",
              "| message | priority | effective status | other blockers proving OPEN |", "|---|---:|---|---|"]
    for message, priority, blockers in residuals:
        lines.append(f"| `{message}` | {priority} | OPEN | `{blockers}` |")
    lines += ["", "## Stop rule", "",
              "Stop at these two helpers, their fixed support/EH/import paths, and the six proven caller spans. Resume only if a later effective A2 layer adds one of these exact target tags or independent evidence resolves a remaining blocker.", ""]
    return "\n".join(lines)


def build(external: Path) -> tuple[str, str]:
    image_path = external.parent.parent / "GameClient" / "GameClient.local.bin"
    for path, expected in ((image_path, IMAGE_SHA256), (external / A2_NAME, A2_SHA256),
                           (external / SLOT34_A2_NAME, SLOT34_A2_SHA256),
                           (external / PRIORITY_NAME, PRIORITY_SHA256),
                           (external / SLOT34_PRIORITY_NAME, SLOT34_PRIORITY_SHA256)):
        require_hash(path, expected)
    image = image_path.read_bytes()
    verify_image(image)
    base_fields, base_rows = read_tsv(external / A2_NAME)
    slot_fields, slot_rows = read_tsv(external / SLOT34_A2_NAME)
    delta = build_delta(base_fields, base_rows, slot_fields, slot_rows)
    verify_overlays(external, delta)
    residuals = priority_residuals(external)
    return tsv_text(delta), report_text(residuals)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--external", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    external = args.external.resolve()
    delta, report = build(external)
    outputs = {external / OUTPUT_NAME: delta, external / REPORT_NAME: report}
    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                raise RuntimeError(f"output drift: {path.name}")
        print("PASS targets 0x00694790/0x006B3440: 30 unique non-wire removals; overlap 0; Priority delta 0")
        return 0
    for path, text in outputs.items():
        atomic_write(path, text)
    print("WROTE targets 0x00694790/0x006B3440: 30 unique non-wire removals; overlap 0; Priority delta 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
