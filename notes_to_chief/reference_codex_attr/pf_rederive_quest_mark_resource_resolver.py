#!/usr/bin/env python3
"""Re-derive the bounded quest-mark resource resolver from pinned IMAGE and DATA.

The two evidence layers remain separate in the TSV.  Cross-source composition is
reported only in the Markdown.  No client, server, dump, capture, or texture is
executed; shipped $pcz assets are decoded only in memory for structural guards.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import lzma
import os
import re
import struct
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"
DATA_DIR = PF_ROOT / "GameClient" / "Data" / "GUI" / "Main"
SELECTOR_PATH = OUT_DIR / "PF_ATTR_QUEST_MARK_SELECTOR.tsv"
DATA_BINDINGS_PATH = OUT_DIR / "PF_ATTR_DATA_BINDINGS.tsv"
GROUND_DROP_PATH = OUT_DIR / "PF_GROUND_DROP_LIFETIME.tsv"
TSV_PATH = OUT_DIR / "PF_QUEST_MARK_RESOURCE_RESOLVER.tsv"
REPORT_PATH = OUT_DIR / "PF_QUEST_MARK_RESOURCE_RESOLVER.md"
LOCK_PATH = OUT_DIR / ".pf_rederive_quest_mark_resource_resolver.lock"

EXPECTED_IMAGE_SIZE = 14_759_424
EXPECTED_IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
EXPECTED_SELECTOR_SIZE = 52_137
EXPECTED_SELECTOR_SHA256 = "3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0"
EXPECTED_DATA_BINDINGS_SIZE = 53_723
EXPECTED_DATA_BINDINGS_SHA256 = "67e7550a09b00a5243f4c084ff486d29e420c6d0687704a092f157dbce219cb2"
EXPECTED_GROUND_DROP_SIZE = 61_979
EXPECTED_GROUND_DROP_SHA256 = "b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710"

SOURCE_IMAGE_FILE = "PF_ROOT://GameClient/GameClient.local.bin"
PAIR_PLACEHOLDER = "0" * 64


@dataclass(frozen=True)
class Section:
    name: str
    va: int
    file_off: int
    mapped_len: int
    virtual_size: int
    raw_size: int


@dataclass(frozen=True)
class SelectorSpec:
    selector: int
    literal: str
    literal_va: int
    selector_key: str
    selector_evidence_key: str
    selector_claim_sha256: str
    packaged_leaf: str
    binding_key: str
    binding_evidence_key: str
    raw_size: int
    raw_sha256: str


SELECTORS = (
    SelectorSpec(1, "%sQuest_begin.tga", 0x00F31F78,
        "5464435ef50cdb99c6bdae1894455461970957c2294f7d1b23e7f12b1ab11439",
        "43c0f31d521b1e3e8126f272bef7652b596f133bb50e7c070505860727e4f582",
        "5da927c2ab7c456f7dccb5c0315a01e63294ff5516902cc2fe85df972e630cfa",
        "quest_begin.tg_", "cafb2520283d0f126467616fa6c825bb7c01c4644fbd66a894e73e4088b6fcff",
        "cd368d14728b0a12064285591c843aa29118ea2694cd6c930939125d62a3eaec", 5370,
        "459d1b04e53c09d8dd485440ad54dab5f8c5cac2b5dc1483125414cf3d816ae6"),
    SelectorSpec(2, "%squest_again.tga", 0x00F31F54,
        "9eefcfa3f4c47b1c8aec68e788ec30b3e71cb7547953e905f602125738b74ea3",
        "81df723f5fe9e1e5fd99b71092f13cc66e39e230e87b20c80e6ca24d1b670f61",
        "351db507eaee5c7b8230134003ef61af2ef2d5fbb8660dd67e00ad3fc21e0094",
        "quest_again.tg_", "824e85b3e9bd48f38cf270935e6bc856e3f4ecc8ebf21b645f8e8edd900676a4",
        "f6e3af9662ec8ab3d95aeaad1f3bee86fce53f567a7dc1d633ebb7a95e28cfa3", 5465,
        "ef2b10104a37eb1c0667a156d97dab63432b92615e4a70071a612dafc6a9aeb8"),
    SelectorSpec(3, "%sQuest_end.tga", 0x00F31F34,
        "8e0a307d7d14bbd2a66916938320d9e2b4ed96d57e81e538a723137268663ede",
        "f956d7f3a3718008ee17893c5d1ce9a8fe4da065091d82da38ba9f75224f2635",
        "077964ef2d6ca30b0081176b55c7ba55283be453b8cc0ebe09a38ce63f6d6756",
        "quest_end.tg_", "13f10092531071176183fae1b48179fa75de20b677bacd58eba307b0ddce6be5",
        "76e8a7f4285b46c5cc8960d0d884938f8a60cbc1f22d36e972e72929f333c2bd", 5479,
        "68e2bc42b8428ad9d48279c7265d84ac75e30adddc585efe046136fda1b318f1"),
    SelectorSpec(4, "%squest_againend.tga", 0x00F31F08,
        "ce7016e63d533dd7ac87809df14e1cc8aa2e727178b8c1f6180e970551d83b13",
        "e708724848d2f8a19b73a460df044a75d4e80a3655b51ad4969f2c2d6fec211d",
        "1049ac55869ce05e365bf4e0a2408abcbeb0ff008b5e4112ecfb194692d55e64",
        "quest_againend.tg_", "373c936c3c81fced05eb54cd79b35dbfb5e56f26e5020e9adeac0f9192bf25d4",
        "0655794f9ee830ba4558322b8dee262ed840f512b7de45bbebf6a8ad3178ba03", 5694,
        "81f6e68a284c5798512a29abf70efabcfefe9f50773b61aef13fb7956519f30b"),
    SelectorSpec(5, "%sQuest_ing.tga", 0x00F31EE8,
        "a23f05a8298f622f2942b57f14d26f8ed8c6e61af066157b0f6b538415edf43e",
        "f1ac606313187059e89f403fbb3cc58018d26eb91d95d5e8e6d0d9eff691cbf9",
        "7d492fdbdebd3af1ba6375b9ea27e003e7a45921c5aebc8f87d44ebb3694df11",
        "quest_ing.tg_", "42144a1519d1ec4a47d7770616df066321c21445f2ca5cdbd9ef495732e8cc7d",
        "593b96f37bc9a04ce1252d0b46b29a3e75c0c331ac7960f614eb7000c8d2dbc5", 3002,
        "a9bacc11c967bb2aa764a5772884c96180281d00f7f98c1577ba5d80731603e0"),
    SelectorSpec(6, "%squest_low.tga", 0x00F31EC8,
        "68c906aabaca780c17e7d796e56d965ad34a2c09debbc5cd53d38a6bbf9cea05",
        "cdd4087ccccaed21693b68865c37c9241b5320843fb20fc0e9d7ee33afd88aa4",
        "842c24dcce19f7bb1ff2a7ad6eac2f2184040753c0572fab36a923ae97686883",
        "quest_low.tg_", "c4768580ecabee30fb1f83c580a1ccb603e2c7cc69bdeb098ada97efb8283354",
        "b156717dc180f3a0c8cd881e795a132c83de9e1f9d7f658cb10a73194608a237", 2783,
        "9bcac71fcf6140ae9be13012bd4d901557c6cbd599ddc67bf3530897f2a40fb0"),
    SelectorSpec(7, "%squest_dungeon.tga", 0x00F31EA0,
        "719515671edf8347af6ced4ca86a7ec94c9aa29ef0f502fa4d8a609507023bd2",
        "d84ad8e45794ecad59c855239a03f8954edfec285bc448c8c7c1f58dc6cc9872",
        "3cca4d2f1ae15541ae3cab4dfe9b58268338c8e0a6aed3ca2f3f074d18a055b2",
        "quest_dungeon.tg_", "33828f1478af1c5fa71fa7c223d48ad255e38d9a71fc97572ced4e27cd57bc54",
        "d399bf0cecb2f424e32a4529cc019b4b171ddfda88a5efa3617299511d801d80", 6417,
        "9533f8d1eec914c3bc5620eab8c7146f46beedc0a4e301fb2a893f72c590bffe"),
    SelectorSpec(8, "%sQuest_SpBegin.tga", 0x00F31E78,
        "2e2a66518ed5fab2335da6e58e8e98b361edbc21610d05336816c76e080e1e4a",
        "503bae7ab8c6535a0fb6ba10efb245957f4d4ab1b87a1560b793953eab983fbe",
        "6d63573f39a10c316bdf1f2d49904a81fd4c5332c8baf56a3997d74f256e70c0",
        "quest_spbegin.tg_", "da8718aa9503f74dee9e71ac8e4ca37fe8e2dce66e98e2ba188a52ce1f9d7a4c",
        "38fb9c9f9e49d17302130e3219dcebf4fe60582cb80d7159a99f2dced7ba5933", 5407,
        "758a97882e7581ec3ccb8a47f52ebd6780a6613509a1db9aed0c66ccb2b63cec"),
)

SPECIAL_LEAF = "quest_splend.tga.tg_"
SPECIAL_SIZE = 5608
SPECIAL_SHA256 = "32c578abcce2dbf8b39bcfcc9153a6b2cff8908b1ad6bca29c2983366281462e"
SPECIAL_DECODED_SIZE = 16_428
SPECIAL_DECODED_SHA256 = "907238162d8d02676be8e09c9ba48d1964a3bfbc34b911cab917c88ec77782a9"
SPECIAL_HEADER_SHA256 = "33038d7dd1b7f3fda5899c6422c2e7944c6f288e836bcb62ae5c3c17a641d046"

GDL_REFS = {
    "GDL-IMG-018": (
        "8397845c5926ffec7261a4f40c40a77d8699d001e45299a64f188681fd9ab989",
        "0x0040AF9C", "0x0040AFB0",
        "2c32966749423e1158c563e64dc915f93ef1fb0dafff3adb4125b44de08ba753",
    ),
    "GDL-IMG-019": (
        "81179e8b43544e4ea785214563ee11c071d4d4c7c0d4b0607dd2bd387e081247",
        "0x00B7A5C0", "0x00B7A62C",
        "041725fb948bb5db4e114c854f77f62038d665583976c2f438477a3a395a95ec",
    ),
}

# End VAs are exclusive.
SPANS = {
    "texture_manager": (0x00A9F350, 0x00A9F58C, "14cefd11594ebb2899d06b0ef770c495ea1cf72b7a2bcc12ce208deddc418a80"),
    "resource_loader": (0x00AC7930, 0x00AC7AE6, "aef62b9753b998b551ce92048f7ef598fb2d29449d4a839a00ecf6eda11524b0"),
    "hook_installer": (0x0040AF9C, 0x0040AFB0, "2c32966749423e1158c563e64dc915f93ef1fb0dafff3adb4125b44de08ba753"),
    "tga_compare": (0x00B7A7FF, 0x00B7A816, "ec5c40a81c23bb22155d980f48199ffc778ce470f1d22735126bff4f433d6d70"),
    "rewrite_store": (0x00B7A8A1, 0x00B7A8D2, "1b17b5afa32d5c8a57b89bf2fd3fde11d049cd16b952f8c1867ce38b2718e375"),
    "exists_callback": (0x00B01DD0, 0x00B01ECB, "ce3491e3c5b839efd1d54d6fc6e066178bfc0e670e560b5317c4eab0d9a15197"),
    "open_factory": (0x00B02300, 0x00B023B0, "d742dd309c8371eab42ee866e8bc57af00d49f45d5424ac70f29f1d202834e3c"),
    "generic_image": (0x008A21D0, 0x008A2401, "7c2e90f233a2aade00be5d0f09dbf19ae269b245b4ffdb9abe804c20331681c1"),
    "converter_filter_open": (0x00925A80, 0x00925B6D, "613bcfe2fbef5d3034eb785aa249c44301aa223bb093cda3e0d184b2ab919819"),
    "converter_header": (0x00925B70, 0x00925CB2, "828fd505a45432950db14a0e603042b47611a7eb97bae6808019ac9f4c1b93cc"),
    "converter_decode": (0x00925CC0, 0x00925DBE, "25a68df79062f68ab5543e5f1f6afddd7027c114e916a0ee29a5de9f879f0966"),
    "tga_register": (0x00929EB5, 0x00929EFF, "ee1aaa27f16b1542c26c27dcab5c69f2d7c6eda14a070d38b4c8d1f47adcb0ee"),
    "tga_ctor": (0x0092B380, 0x0092B44C, "096bb59aeb290a4ab93bbc79dbe59058fc0ac476b7a49a13a1ec15263beb3c33"),
    "tga_vtable": (0x00F724F4, 0x00F72504, "595f58fb45ebc0af44132cc3b9d9118987b9649c494378ee59fec8c55a99d51e"),
    "tga_filter": (0x0092B340, 0x0092B373, "f9bcac6f52c338a1744110fa382b03e84ec3add6f01db69e4410264b26594f0e"),
    "tga_header": (0x0092B880, 0x0092BBFA, "6976c7db7a69bf45665d28ef1d7011d9391eb35103cbc15d9d7888f678caad0f"),
    "tga_decode": (0x0092BC60, 0x0092BF18, "8b00697b694805bd50dcaabb25664bfd236e0e2dea17501811d0e8f0b671221d"),
}

FIELDNAMES = (
    "resolver_key", "row_kind", "route_order", "source", "subject", "claim",
    "semantic_status", "measurement_label", "method", "control",
    "runtime_open_status", "runtime_bind_status",
    "runtime_pixels_status", "source_file", "source_size", "source_sha256",
    "evidence_locator", "span_start", "span_end", "file_offset_start",
    "file_offset_end", "span_sha256", "support_spans", "reference_artifact",
    "reference_sha256", "reference_keys", "query_original_leaf",
    "query_packaged_leaf", "query_alternate_leaf", "exact_original_match_count",
    "casefold_original_match_count", "exact_packaged_match_count",
    "casefold_packaged_match_count", "casefold_alternate_match_count", "matched_path",
    "decoded_size", "decoded_sha256", "decoded_header_sha256", "decoded_structure",
    "claim_sha256", "evidence_key", "blocker", "required_next_evidence", "nonclaim",
    "artifact_pair_sha256",
)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable_key(domain: str, *parts: object) -> str:
    payload = domain.encode("ascii") + b"\x00"
    payload += b"\x1f".join(str(part).encode("utf-8") for part in parts)
    return sha256(payload)


def fmt_va(value: int) -> str:
    return f"0x{value:08X}"


def parse_pe(image: bytes) -> tuple[int, tuple[Section, ...]]:
    if image[:2] != b"MZ":
        raise RuntimeError("image is not MZ")
    pe_off = struct.unpack_from("<I", image, 0x3C)[0]
    if image[pe_off:pe_off + 4] != b"PE\x00\x00":
        raise RuntimeError("image is not PE")
    count = struct.unpack_from("<H", image, pe_off + 6)[0]
    optional_size = struct.unpack_from("<H", image, pe_off + 20)[0]
    optional_off = pe_off + 24
    if struct.unpack_from("<H", image, optional_off)[0] != 0x10B:
        raise RuntimeError("expected PE32")
    image_base = struct.unpack_from("<I", image, optional_off + 28)[0]
    table_off = optional_off + optional_size
    sections: list[Section] = []
    for index in range(count):
        off = table_off + index * 40
        name = image[off:off + 8].split(b"\x00", 1)[0].decode("ascii")
        virtual_size, rva, raw_size, raw_off = struct.unpack_from("<IIII", image, off + 8)
        mapped_len = min(virtual_size, raw_size)
        if raw_off + mapped_len > len(image):
            raise RuntimeError(f"section exceeds image: {name}")
        sections.append(Section(name, image_base + rva, raw_off, mapped_len, virtual_size, raw_size))
    if tuple(section.name for section in sections) != (".text", ".code", ".rdata", ".data", ".rsrc", ".reloc"):
        raise RuntimeError("PE section set/order drift")
    return image_base, tuple(sections)


def va_to_file(sections: Sequence[Section], va: int, allow_end: bool = False) -> int:
    for section in sections:
        end = section.va + section.mapped_len
        if section.va <= va < end or (allow_end and va == end):
            return section.file_off + va - section.va
    raise RuntimeError(f"VA outside mapped file intervals: {fmt_va(va)}")


def span_fact(image: bytes, sections: Sequence[Section], name: str) -> dict[str, object]:
    start, end, expected = SPANS[name]
    start_off = va_to_file(sections, start)
    end_off = va_to_file(sections, end, allow_end=True)
    actual = sha256(image[start_off:end_off])
    if actual != expected:
        raise RuntimeError(f"span hash drift: {name}")
    return {"name": name, "start": start, "end": end, "start_off": start_off, "end_off": end_off, "sha": actual}


def support_text(*facts: Mapping[str, object]) -> str:
    return ";".join(
        f"{fact['name']}={fmt_va(int(fact['start']))}..{fmt_va(int(fact['end']))}"
        f"@file_off={fmt_va(int(fact['start_off']))}..{fmt_va(int(fact['end_off']))}"
        f"@sha256={fact['sha']}" for fact in facts
    )


def assert_bytes(image: bytes, sections: Sequence[Section], va: int, expected: bytes, label: str) -> None:
    off = va_to_file(sections, va)
    if image[off:off + len(expected)] != expected:
        raise RuntimeError(f"instruction guard drift: {label}")


def assert_rel32(image: bytes, sections: Sequence[Section], site: int, target: int, label: str) -> None:
    off = va_to_file(sections, site)
    if image[off] != 0xE8:
        raise RuntimeError(f"expected E8 call: {label}")
    displacement = struct.unpack_from("<i", image, off + 1)[0]
    actual = (site + 5 + displacement) & 0xFFFFFFFF
    if actual != target:
        raise RuntimeError(f"call target drift: {label}")


def read_utf16z(image: bytes, sections: Sequence[Section], va: int) -> str:
    off = va_to_file(sections, va)
    end = off
    while end + 1 < len(image) and image[end:end + 2] != b"\x00\x00":
        end += 2
    return image[off:end].decode("utf-16le")


def read_pinned_tsv(path: Path, size: int, digest: str) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if len(raw) != size or sha256(raw) != digest:
        raise RuntimeError(f"reference artifact pin drift: {path.name}")
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise RuntimeError(f"empty reference artifact: {path.name}")
    return rows


def decode_pcz(data: bytes) -> bytes:
    if len(data) < 13 or data[:4] != b"$pcz":
        raise RuntimeError("pcz header mismatch")
    expected_size = struct.unpack_from("<I", data, 4)[0]
    props = data[8:13]
    first = props[0]
    if first >= 9 * 5 * 5:
        raise RuntimeError("pcz property mismatch")
    lc = first % 9
    rest = first // 9
    lp = rest % 5
    pb = rest // 5
    dictionary = struct.unpack_from("<I", props, 1)[0]
    if dictionary == 0:
        raise RuntimeError("pcz dictionary is zero")
    decoder = lzma.LZMADecompressor(
        format=lzma.FORMAT_RAW,
        filters=[{"id": lzma.FILTER_LZMA1, "lc": lc, "lp": lp, "pb": pb, "dict_size": dictionary}],
    )
    output = decoder.decompress(data[13:], max_length=expected_size + 1)
    if len(output) != expected_size:
        raise RuntimeError("pcz decoded-size mismatch")
    return output


def tga_structure(decoded: bytes) -> tuple[int, int, int, int, int, int, int, int]:
    if len(decoded) < 18:
        raise RuntimeError("decoded TGA is truncated")
    id_length, cmap_type, image_type = decoded[0], decoded[1], decoded[2]
    width, height = struct.unpack_from("<HH", decoded, 12)
    depth, descriptor = decoded[16], decoded[17]
    return len(decoded), id_length, cmap_type, image_type, width, height, depth, descriptor


def measurement_profile(source: str, row_kind: str) -> tuple[str, str, str]:
    """Return the only accepted measurement contract for a source/row boundary."""
    if row_kind == "REFERENCE_ONLY":
        if source != "IMAGE":
            raise RuntimeError("REFERENCE_ONLY source boundary drift")
        return (
            "REFERENCE",
            "PINNED_REFERENCE_ARTIFACT_SIZE_SHA256_AND_EXACT_KEY_JOIN",
            "REFERENCE_SIZE_SHA256_PIN;REFERENCE_KEY_EXISTENCE;NO_LOCAL_PRIMARY_EVIDENCE;NO_CLAIM_REISSUE;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    if row_kind == "IMAGE_ROUTE_BOUND":
        if source != "IMAGE":
            raise RuntimeError("IMAGE_ROUTE_BOUND source boundary drift")
        return (
            "COMPOSED_BOUND",
            "IMAGE_ONLY_COMPOSITION_OF_HASHED_LOCAL_ROWS_AND_PINNED_REFERENCE_KEYS",
            "SINGLE_SOURCE_IMAGE;ALL_COMPONENT_KEYS_RESOLVE;NO_DATA_FIELDS;NO_RUNTIME_PROMOTION;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    if row_kind == "IMAGE_STRING_CENSUS":
        if source != "IMAGE":
            raise RuntimeError("IMAGE_STRING_CENSUS source boundary drift")
        return (
            "MEASURED",
            "WHOLE_PINNED_IMAGE_EXACT_UTF16LE_LITERAL_CENSUS",
            "PINNED_IMAGE_SIZE_SHA256;FIXED_QUERY_SET;EXACT_ZERO_COUNT_ASSERTIONS;DYNAMIC_CONSTRUCTION_NONCLAIM;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    if source == "IMAGE" and row_kind == "IMAGE_EXTENSION_RULE":
        return (
            "MEASURED",
            "STATIC_IMAGE_HASHED_SPAN_CONTROL_FLOW_AND_OPERAND_ASSERTIONS",
            "PINNED_IMAGE_SIZE_SHA256;EXACT_PRIMARY_AND_SUPPORT_SPAN_SHA256;STRICMP_IAT_LITERAL_AND_REWRITE_STORE_ASSERTIONS;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    if source == "IMAGE" and row_kind == "IMAGE_READER_REGISTRY":
        return (
            "MEASURED",
            "STATIC_IMAGE_HASHED_SPAN_VIRTUAL_DISPATCH_AND_CALL_ASSERTIONS",
            "PINNED_IMAGE_SIZE_SHA256;EXACT_PRIMARY_AND_SUPPORT_SPAN_SHA256;OPEN_DISPATCH_AND_VIRTUAL_SLOT_ASSERTIONS;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    if source == "IMAGE" and row_kind == "IMAGE_TGA_READER":
        return (
            "MEASURED",
            "STATIC_IMAGE_HASHED_SPAN_VTABLE_LITERAL_AND_CONTROL_FLOW_ASSERTIONS",
            "PINNED_IMAGE_SIZE_SHA256;EXACT_PRIMARY_AND_SUPPORT_SPAN_SHA256;TGA_LITERAL_VTABLE_AND_DIRECT_CALL_ASSERTIONS;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    if source == "IMAGE" and row_kind == "IMAGE_STATIC_ROUTE":
        return (
            "MEASURED",
            "STATIC_IMAGE_HASHED_SPAN_AND_EXACT_CONTROL_FLOW_ASSERTIONS",
            "PINNED_IMAGE_SIZE_SHA256;EXACT_PRIMARY_AND_SUPPORT_SPAN_SHA256;DECISIVE_DIRECT_CALL_ASSERTIONS;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    if source == "DATA" and row_kind == "DATA_FILENAME_CENSUS":
        return (
            "MEASURED",
            "IMMEDIATE_DIRECTORY_EXACT_AND_CASEFOLD_FILENAME_CENSUS_WITH_PINNED_FILE_HASH",
            "PINNED_DATA_FILE_SIZE_SHA256;FIXED_ORIGINAL_AND_REPLACEMENT_QUERIES;EXACT_AND_CASEFOLD_COUNT_ASSERTIONS;IN_MEMORY_PCZ_TGA_STRUCTURE_GUARD;NO_PIXEL_OUTPUT;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    if source == "DATA" and row_kind == "DATA_SPECIAL_CONTROL":
        return (
            "MEASURED",
            "IMMEDIATE_DIRECTORY_CENSUS_AND_IN_MEMORY_PCZ_TGA_STRUCTURAL_DECODE",
            "PINNED_DATA_FILE_SIZE_SHA256;FIXED_REPLACEMENT_AND_APPEND_QUERIES;DECODED_SIZE_SHA256_HEADER_SHA256_AND_STRUCTURE_ASSERTIONS;NO_RAW_BYTES_OR_PIXELS;RUNTIME_OPEN_BIND_PIXELS_OPEN",
        )
    raise RuntimeError(f"unmapped measurement boundary: {source}/{row_kind}")


def base_row(**values: object) -> dict[str, str]:
    row = {field: "" for field in FIELDNAMES}
    row.update({key: str(value) for key, value in values.items()})
    label, method, control = measurement_profile(row["source"], row["row_kind"])
    row["measurement_label"] = label
    row["method"] = method
    row["control"] = control
    row["runtime_open_status"] = row.get("runtime_open_status") or "OPEN"
    row["runtime_bind_status"] = row.get("runtime_bind_status") or "OPEN"
    row["runtime_pixels_status"] = row.get("runtime_pixels_status") or "OPEN"
    row["artifact_pair_sha256"] = PAIR_PLACEHOLDER
    row["claim_sha256"] = stable_key(
        "PF_QUEST_MARK_RESOURCE_RESOLVER_CLAIM_V1", row["source"], row["row_kind"],
        row["subject"], row["claim"], row["semantic_status"], row["nonclaim"],
    )
    row["evidence_key"] = stable_key(
        "PF_QUEST_MARK_RESOURCE_RESOLVER_EVIDENCE_V1", row["source"], row["source_file"],
        row["source_sha256"], row["evidence_locator"], row["span_start"], row["span_end"],
        row["span_sha256"], row["matched_path"], row["decoded_sha256"], row["reference_keys"],
        row["measurement_label"], row["method"], row["control"],
    )
    row["resolver_key"] = stable_key(
        "PF_QUEST_MARK_RESOURCE_RESOLVER_ROW_V1", row["row_kind"], row["route_order"],
        row["claim_sha256"], row["evidence_key"],
    )
    return row


def image_row(fact: Mapping[str, object] | None = None, **values: object) -> dict[str, str]:
    defaults: dict[str, object] = {
        "source": "IMAGE", "source_file": SOURCE_IMAGE_FILE,
        "source_size": EXPECTED_IMAGE_SIZE, "source_sha256": EXPECTED_IMAGE_SHA256,
    }
    if fact is not None:
        defaults.update({
            "span_start": fmt_va(int(fact["start"])), "span_end": fmt_va(int(fact["end"])),
            "file_offset_start": fmt_va(int(fact["start_off"])),
            "file_offset_end": fmt_va(int(fact["end_off"])), "span_sha256": fact["sha"],
        })
    defaults.update(values)
    return base_row(**defaults)


def data_row(path: Path, **values: object) -> dict[str, str]:
    raw = path.read_bytes()
    defaults: dict[str, object] = {
        "source": "DATA", "source_file": f"PF_ROOT://GameClient/Data/GUI/Main/{path.name}",
        "source_size": len(raw), "source_sha256": sha256(raw),
    }
    defaults.update(values)
    return base_row(**defaults)


def derive(image: bytes) -> tuple[list[dict[str, str]], dict[str, object]]:
    _, sections = parse_pe(image)
    facts = {name: span_fact(image, sections, name) for name in SPANS}

    selector_rows = read_pinned_tsv(SELECTOR_PATH, EXPECTED_SELECTOR_SIZE, EXPECTED_SELECTOR_SHA256)
    binding_rows = read_pinned_tsv(DATA_BINDINGS_PATH, EXPECTED_DATA_BINDINGS_SIZE, EXPECTED_DATA_BINDINGS_SHA256)
    gdl_rows = read_pinned_tsv(GROUND_DROP_PATH, EXPECTED_GROUND_DROP_SIZE, EXPECTED_GROUND_DROP_SHA256)
    selector_by_key = {row["selector_key"]: row for row in selector_rows}
    binding_by_key = {row["binding_key"]: row for row in binding_rows}
    gdl_by_id = {row["evidence_id"]: row for row in gdl_rows}

    for spec in SELECTORS:
        row = selector_by_key.get(spec.selector_key)
        if row is None or any((
            row["input_selector"] != str(spec.selector), row["image_asset_literal"] != spec.literal,
            row["literal_va"] != fmt_va(spec.literal_va), row["evidence_key"] != spec.selector_evidence_key,
            row["claim_sha256"] != spec.selector_claim_sha256, row["source"] != "IMAGE",
            row["image_sha256"] != EXPECTED_IMAGE_SHA256,
        )):
            raise RuntimeError(f"selector reference drift: {spec.selector}")
        if read_utf16z(image, sections, spec.literal_va) != spec.literal:
            raise RuntimeError(f"selector literal image drift: {spec.selector}")
        binding = binding_by_key.get(spec.binding_key)
        expected_file = f"PF_ROOT://GameClient/Data/GUI/Main/{spec.packaged_leaf}"
        if binding is None or any((
            binding["evidence_file"] != expected_file, binding["evidence_sha256"] != spec.raw_sha256,
            binding["evidence_key"] != spec.binding_evidence_key, binding["source"] != "DATA",
            binding["semantic_status"] != "PROVEN_EXACT",
        )):
            raise RuntimeError(f"DATA binding reference drift: {spec.packaged_leaf}")

    for evidence_id, expected in GDL_REFS.items():
        row = gdl_by_id.get(evidence_id)
        if row is None or any((
            row["evidence_key"] != expected[0], row["evidence_span_start"] != expected[1],
            row["evidence_span_end"] != expected[2], row["evidence_span_sha256"] != expected[3],
            row["source"] != "IMAGE", row["source_sha256"] != EXPECTED_IMAGE_SHA256,
        )):
            raise RuntimeError(f"ground-drop reference drift: {evidence_id}")

    # Decisive direct edges and operands.  These are guards, not emitted bytes.
    assert_rel32(image, sections, 0x00A9F486, 0x00AC7930, "manager->resource loader")
    assert_rel32(image, sections, 0x00AC79A5, 0x00790F20, "resource loader->exists dispatcher")
    assert_rel32(image, sections, 0x00AC7A36, 0x008A21D0, "resource loader->generic image")
    assert_rel32(image, sections, 0x0040AFA1, 0x00790F00, "install open callback")
    assert_rel32(image, sections, 0x0040AFAB, 0x00790F30, "install exists callback")
    assert_rel32(image, sections, 0x00B01E44, 0x00B7A780, "exists->rewrite")
    assert_rel32(image, sections, 0x00925B12, 0x00790EC0, "filter/open dispatcher")
    assert_rel32(image, sections, 0x00925C33, 0x00790EC0, "header/open dispatcher")
    assert_rel32(image, sections, 0x00925D53, 0x00790EC0, "decode/open dispatcher")
    assert_rel32(image, sections, 0x00929ECB, 0x0092B380, "register TGA reader")
    assert_bytes(image, sections, 0x00B7A7E2, bytes.fromhex("8b3518b5c300"), "_stricmp IAT load")
    assert_bytes(image, sections, 0x00B7A803, bytes.fromhex("68ec24f70052ffd6"), ".tga compare")
    assert_bytes(image, sections, 0x00B7A8B4, bytes.fromhex("c64407ff5f"), "last-character underscore rewrite")
    assert_bytes(image, sections, 0x00925AE6, bytes.fromhex("8b018b40048b368d94240701000052ffd0"), "reader filter dispatch")
    assert_bytes(image, sections, 0x00925C56, bytes.fromhex("8b178b520c"), "reader header dispatch")
    assert_bytes(image, sections, 0x00925D6E, bytes.fromhex("8b178b4208"), "reader decode dispatch")
    vtable_off = va_to_file(sections, 0x00F724F4)
    if struct.unpack_from("<4I", image, vtable_off) != (0x0092B450, 0x0092B340, 0x0092BC60, 0x0092B880):
        raise RuntimeError("TGA reader vtable drift")
    if image[va_to_file(sections, 0x00F724E4):va_to_file(sections, 0x00F724E4) + 7] != b".targa\x00":
        raise RuntimeError(".targa literal drift")
    if image[va_to_file(sections, 0x00F724EC):va_to_file(sections, 0x00F724EC) + 5] != b".tga\x00":
        raise RuntimeError(".tga literal drift")

    selector_keys = ";".join(spec.selector_key for spec in SELECTORS)
    rows: list[dict[str, str]] = []
    rows.append(image_row(
        row_kind="REFERENCE_ONLY", route_order="00", subject="eight quest-mark selector literals",
        claim="The eight selector identities and their formatting literals are imported by pinned key; this artifact does not restate their branch predicates.",
        semantic_status="REFERENCE_ONLY", evidence_locator="PF_ATTR_QUEST_MARK_SELECTOR selector keys 1..8",
        reference_artifact="PF_ATTR_QUEST_MARK_SELECTOR.tsv", reference_sha256=EXPECTED_SELECTOR_SHA256,
        reference_keys=selector_keys,
        blocker="None for selector identity; runtime selection remains outside this reference row.",
        required_next_evidence="Use the selector artifact for branch predicates and lifecycle evidence.",
        nonclaim="No selector condition, selector frequency, or runtime selection is newly claimed here.",
    ))
    rows.append(image_row(facts["texture_manager"],
        row_kind="IMAGE_STATIC_ROUTE", route_order="10", subject="texture manager 0x00A9F350",
        claim="The manager normalizes and hashes the requested path, consults its cache, allocates a resource on a miss, calls 0x00AC7930, conditionally tries its configured fallback path, and registers a successful resource.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="texture manager cache/miss/load/fallback/register control flow",
        support_spans=support_text(facts["resource_loader"]),
        blocker="Cache contents, configured fallback path, and branch outcomes are runtime state.",
        required_next_evidence="Source-separated runtime trace of the concrete request and returned resource.",
        nonclaim="Static reachability does not prove that any of the eight requests opened or returned a texture at runtime.",
    ))
    rows.append(image_row(facts["resource_loader"],
        row_kind="IMAGE_STATIC_ROUTE", route_order="20", subject="resource loader 0x00AC7930",
        claim="The resource loader rejects an empty path, asks the exists dispatcher at 0x00790F20, calls generic image loader 0x008A21D0, stores its result at resource+0x10, and requires nonzero virtual +0x48 and +0x4C results before success.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="exists->generic-image->resource validation control flow",
        support_spans=support_text(facts["generic_image"]),
        blocker="The runtime callbacks, generic-loader result, and virtual return values are unobserved.",
        required_next_evidence="Runtime trace keyed to each formatted quest-mark path.",
        nonclaim="This row does not prove a file was present, decoded, uploaded, or bound.",
    ))
    rows.append(image_row(
        row_kind="REFERENCE_ONLY", route_order="30", subject="packaged open/exists callback installation",
        claim="The generic packaged-resource callback installation and transformed-first/original fallback route are imported from GDL-IMG-018; the quest-specific extension member is proved separately below.",
        semantic_status="REFERENCE_ONLY", evidence_locator="GDL-IMG-018",
        reference_artifact="PF_GROUND_DROP_LIFETIME.tsv", reference_sha256=EXPECTED_GROUND_DROP_SHA256,
        reference_keys="GDL-IMG-018;8397845c5926ffec7261a4f40c40a77d8699d001e45299a64f188681fd9ab989",
        blocker="Installer reachability/order and later callback overwrite are not established for the observed runtime.",
        required_next_evidence="Runtime callback-slot trace before the quest resource request.",
        nonclaim="The generic `.nif` example owned by GDL-IMG-018 is not repeated as a quest fact.",
    ))
    rows.append(image_row(facts["tga_compare"],
        row_kind="IMAGE_EXTENSION_RULE", route_order="40", subject="case-insensitive .tga packaged rewrite",
        claim="The extension allowlist compares the split extension to `.tga` with `_stricmp`; on a match the shared success tail overwrites the final path character with `_`, so `.tga` becomes `.tg_` and no suffix is appended.",
        semantic_status="PROVEN_EXACT", evidence_locator=".tga comparison plus shared final-character store",
        support_spans=support_text(facts["rewrite_store"]),
        reference_artifact="PF_GROUND_DROP_LIFETIME.tsv", reference_sha256=EXPECTED_GROUND_DROP_SHA256,
        reference_keys="GDL-IMG-018;8397845c5926ffec7261a4f40c40a77d8699d001e45299a64f188681fd9ab989",
        blocker="Runtime invocation for a concrete quest path remains unobserved.",
        required_next_evidence="Trace the input/output buffer at 0x00B7A780 for one quest-mark request.",
        nonclaim="This exact rule cannot produce a double extension such as `.tga.tg_` from a `.tga` input.",
    ))
    rows.append(image_row(facts["exists_callback"],
        row_kind="IMAGE_STATIC_ROUTE", route_order="50", subject="exists callback 0x00B01DD0",
        claim="The callback copies the original path, rewrites the copy, attempts CreateFileA on the transformed path first, and conditionally retries the untouched original after transformed failure.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="rewrite and transformed-first/original fallback branches",
        support_spans=support_text(facts["hook_installer"], facts["rewrite_store"]),
        reference_artifact="PF_GROUND_DROP_LIFETIME.tsv", reference_sha256=EXPECTED_GROUND_DROP_SHA256,
        reference_keys="GDL-IMG-018;8397845c5926ffec7261a4f40c40a77d8699d001e45299a64f188681fd9ab989",
        blocker="Actual file-open result and callback slot identity are runtime facts.",
        required_next_evidence="Trace callback target, transformed attempt, fallback attempt, and return value.",
        nonclaim="No successful open of a quest texture is asserted.",
    ))
    rows.append(image_row(facts["open_factory"],
        row_kind="IMAGE_STATIC_ROUTE", route_order="60", subject="open callback factory 0x00B02300",
        claim="The installed open factory allocates a stream object, constructs it through 0x00B01FE0, invokes virtual +0x2C, and returns the stream only on success.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="stream allocation/constructor/open-result control flow",
        reference_artifact="PF_GROUND_DROP_LIFETIME.tsv", reference_sha256=EXPECTED_GROUND_DROP_SHA256,
        reference_keys="GDL-IMG-018;8397845c5926ffec7261a4f40c40a77d8699d001e45299a64f188681fd9ab989",
        blocker="Runtime callback state and stream-open result are unobserved.",
        required_next_evidence="Runtime trace of 0x00B02300 and its stream virtual result.",
        nonclaim="This static factory path does not prove the selected asset opened.",
    ))
    rows.append(image_row(
        row_kind="REFERENCE_ONLY", route_order="70", subject="$pcz packaged decode wrapper",
        claim="The generic `$pcz` decode/parse mechanism is imported by key from GDL-IMG-019 and is not duplicated here.",
        semantic_status="REFERENCE_ONLY", evidence_locator="GDL-IMG-019",
        reference_artifact="PF_GROUND_DROP_LIFETIME.tsv", reference_sha256=EXPECTED_GROUND_DROP_SHA256,
        reference_keys="GDL-IMG-019;81179e8b43544e4ea785214563ee11c071d4d4c7c0d4b0607dd2bd387e081247",
        blocker="Asset-specific runtime decode selection and result remain unobserved.",
        required_next_evidence="Runtime trace tying the opened quest path to the decode wrapper and downstream reader.",
        nonclaim="No decoded bytes, pixels, or asset-specific runtime success are emitted or claimed.",
    ))
    rows.append(image_row(facts["generic_image"],
        row_kind="IMAGE_STATIC_ROUTE", route_order="80", subject="generic image loader 0x008A21D0",
        claim="The generic image entry normalizes the source name, creates a texture-source object on the uncached path, records the path/options, and may invoke its virtual load path under global/runtime gates.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="generic image cache/create/path/options/virtual-load control flow",
        blocker="The concrete texture subclass, lazy/eager load branch, and link to the reader-registry instance are not proved for these eight requests.",
        required_next_evidence="Object/vtable trace from 0x008A21D0 return through the renderer's image-converter instance.",
        nonclaim="The independently proved reader registry below is not asserted to have executed for these eight resources.",
    ))
    rows.append(image_row(facts["converter_filter_open"],
        row_kind="IMAGE_READER_REGISTRY", route_order="90", subject="image-converter reader filter/open dispatch",
        claim="The converter splits the requested path extension, iterates reader nodes at object+0x678, calls reader virtual +0x04 as the type filter, and opens an accepted path through dispatcher 0x00790EC0.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="reader-list loop, virtual filter, open dispatcher",
        support_spans=support_text(facts["tga_register"], facts["tga_vtable"]),
        blocker="The constructed converter instance and selected reader at runtime are unobserved.",
        required_next_evidence="Runtime reader-node identity and filter return for a quest `.tga` request.",
        nonclaim="Registry availability does not prove the TGA reader was selected for an actual request.",
    ))
    rows.append(image_row(facts["converter_header"],
        row_kind="IMAGE_READER_REGISTRY", route_order="100", subject="image-converter header/type dispatch",
        claim="A second converter path repeats extension filtering and open, then calls accepted-reader virtual +0x0C for header/type parsing.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="reader filter/open/virtual +0x0C dispatch",
        blocker="Reader identity, input stream, parse return, and later consumer are runtime facts.",
        required_next_evidence="Runtime virtual target and return value for the concrete quest stream.",
        nonclaim="This row proves dispatch structure, not a successful parse of any selected asset.",
    ))
    rows.append(image_row(facts["converter_decode"],
        row_kind="IMAGE_READER_REGISTRY", route_order="110", subject="image-converter decode dispatch",
        claim="A third converter path repeats extension filtering and open, then calls accepted-reader virtual +0x08 and returns its decoded object when nonzero.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="reader filter/open/virtual +0x08 dispatch",
        blocker="Reader identity, decode return, and object lifetime are runtime facts.",
        required_next_evidence="Runtime virtual target, decoded-object identity, and return value for each selected quest stream.",
        nonclaim="No asset-specific decode success or pixel value is claimed.",
    ))
    rows.append(image_row(facts["tga_register"],
        row_kind="IMAGE_TGA_READER", route_order="120", subject="TGA reader registration",
        claim="The image-converter constructor allocates a 0xB0-byte reader, calls constructor 0x0092B380, and inserts the resulting reader into its linked reader list.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="TGA allocation/constructor/list insertion subspan",
        support_spans=support_text(facts["tga_ctor"], facts["tga_vtable"]),
        blocker="Runtime construction of the relevant converter instance is unobserved.",
        required_next_evidence="Runtime converter construction and reader-node census.",
        nonclaim="Registration in constructor code does not prove that the constructor ran in the observed session.",
    ))
    rows.append(image_row(facts["tga_vtable"],
        row_kind="IMAGE_TGA_READER", route_order="130", subject="TGA reader vtable 0x00F724F4",
        claim="The four-entry vtable is destructor 0x0092B450, extension filter 0x0092B340, decode 0x0092BC60, and header/type parser 0x0092B880.",
        semantic_status="PROVEN_EXACT", evidence_locator="four pointer entries",
        support_spans=support_text(facts["tga_filter"], facts["tga_decode"], facts["tga_header"]),
        blocker="None for the static vtable identity; invocation remains runtime-open.",
        required_next_evidence="Runtime virtual-target trace for asset-specific selection.",
        nonclaim="The vtable does not itself prove any asset was decoded.",
    ))
    rows.append(image_row(facts["tga_filter"],
        row_kind="IMAGE_TGA_READER", route_order="140", subject="TGA extension filter 0x0092B340",
        claim="The reader returns accepted for `.tga` or `.targa` according to comparison helper 0x00793EE0 and rejects other extensions.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="two extension comparisons and boolean return",
        blocker="The helper's full locale/case contract and the runtime extension argument are not independently observed here.",
        required_next_evidence="Runtime extension argument and filter return, or a separately pinned proof of helper semantics.",
        nonclaim="This row does not promote the filter helper to a broader filesystem case rule.",
    ))
    rows.append(image_row(facts["tga_header"],
        row_kind="IMAGE_TGA_READER", route_order="150", subject="TGA header/type parser 0x0092B880",
        claim="The TGA parser reads and validates header/type/depth/palette/orientation state and selects unpack paths before returning a parse result.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="TGA header parser control flow",
        blocker="No selected quest stream or runtime parse result is observed.",
        required_next_evidence="Runtime parser entry/return tied to the concrete opened path.",
        nonclaim="No DATA header or pixel fact is imported into this IMAGE row.",
    ))
    rows.append(image_row(facts["tga_decode"],
        row_kind="IMAGE_TGA_READER", route_order="160", subject="TGA decoder 0x0092BC60",
        claim="The TGA decoder allocates image storage and dispatches row decoding according to parsed TGA state.",
        semantic_status="PROVEN_EXACT_STATIC_CONDITIONAL", evidence_locator="TGA allocation and row-decode control flow",
        blocker="No selected quest stream, decoder return, upload, or presentation is observed.",
        required_next_evidence="Runtime decoder return plus downstream texture/upload identity.",
        nonclaim="No proprietary pixel bytes or visible meaning are emitted.",
    ))
    rows.append(image_row(
        row_kind="REFERENCE_ONLY", route_order="170", subject="QuestIconBoard shared texture binder",
        claim="The board's shared manager-result-to-texture-binding lane is imported from the selector artifact support span rather than duplicated.",
        semantic_status="REFERENCE_ONLY", evidence_locator="QuestIconBoard_texture_binder support key",
        reference_artifact="PF_ATTR_QUEST_MARK_SELECTOR.tsv", reference_sha256=EXPECTED_SELECTOR_SHA256,
        reference_keys="88255f4f1c9a1359a4c7bffd2041300066bde82e83160b235ba4f25e79f116e9",
        blocker="Manager return, bind result, and visible presentation are not observed at runtime.",
        required_next_evidence="Runtime trace from the selector call through manager return and binder sink.",
        nonclaim="Static binder reachability does not prove a nonnull texture or on-screen pixels.",
    ))
    rows.append(image_row(
        row_kind="IMAGE_ROUTE_BOUND", route_order="180", subject="quest-mark resource route static ceiling",
        claim="IMAGE proves the selector-to-manager call, exact `.tga` final-character rewrite and transformed-first/original fallback mechanisms, resource-loader/generic-image entry, registered TGA filter/header/decode machinery, and shared binder availability; the asset-specific runtime bridge across those conditional components remains open.",
        semantic_status="BOUNDED_OPEN_RUNTIME", evidence_locator="aggregate of local IMAGE rows and pinned reference keys",
        reference_artifact="PF_ATTR_QUEST_MARK_SELECTOR.tsv;PF_GROUND_DROP_LIFETIME.tsv",
        reference_sha256=f"{EXPECTED_SELECTOR_SHA256};{EXPECTED_GROUND_DROP_SHA256}",
        reference_keys=";".join((selector_keys, "GDL-IMG-018", GDL_REFS["GDL-IMG-018"][0], "GDL-IMG-019", GDL_REFS["GDL-IMG-019"][0], "88255f4f1c9a1359a4c7bffd2041300066bde82e83160b235ba4f25e79f116e9")),
        blocker="No source-separated runtime observation proves concrete open, reader selection, decode success, texture bind, or pixels for any of the eight selectors.",
        required_next_evidence="Per-selector runtime trace: formatted path, rewritten/opened path, callback result, reader vtable, decode result, texture identity, binder result, and client-visible presentation.",
        nonclaim="This aggregate is IMAGE-only; DATA filename matches are composed only in the Markdown and do not elevate runtime status.",
    ))
    splend_needles = ("quest_splend.tga".encode("utf-16le"), "%squest_splend.tga".encode("utf-16le"))
    if any(image.count(needle) for needle in splend_needles):
        raise RuntimeError("special splend selector-string absence drift")
    rows.append(image_row(
        row_kind="IMAGE_STRING_CENSUS", route_order="190", subject="exact UTF-16 quest_splend.tga string census",
        claim="The complete pinned image contains zero exact UTF-16 occurrences of both `quest_splend.tga` and `%squest_splend.tga`.",
        semantic_status="PROVEN_EXACT_BOUNDED_CENSUS", evidence_locator="whole pinned image exact UTF-16 byte-string census",
        blocker="Absence of a literal does not exclude dynamic construction or a nonliteral reference.",
        required_next_evidence="Producer/consumer proof if a dynamic splend route is suspected.",
        nonclaim="This census does not prove the double-extension DATA asset is unreachable by every possible runtime path.",
    ))

    names = sorted(path.name for path in DATA_DIR.iterdir() if path.is_file())
    lower_names = [name.casefold() for name in names]
    data_rows: list[dict[str, str]] = []
    for spec in SELECTORS:
        original_leaf = spec.literal[2:]
        rewritten_leaf = original_leaf[:-1] + "_"
        exact_original = names.count(original_leaf)
        folded_original = lower_names.count(original_leaf.casefold())
        exact_packaged = names.count(rewritten_leaf)
        folded_packaged = lower_names.count(rewritten_leaf.casefold())
        matches = [name for name in names if name.casefold() == rewritten_leaf.casefold()]
        if (exact_original, folded_original, folded_packaged, matches) != (0, 0, 1, [spec.packaged_leaf]):
            raise RuntimeError(f"DATA filename census drift: selector {spec.selector}")
        path = DATA_DIR / spec.packaged_leaf
        raw = path.read_bytes()
        if len(raw) != spec.raw_size or sha256(raw) != spec.raw_sha256:
            raise RuntimeError(f"DATA asset pin drift: {spec.packaged_leaf}")
        decoded = decode_pcz(raw)
        if tga_structure(decoded) != (16_428, 0, 0, 2, 64, 64, 32, 8):
            raise RuntimeError(f"DATA in-memory TGA guard drift: {spec.packaged_leaf}")
        row = data_row(path,
            row_kind="DATA_FILENAME_CENSUS", route_order=str(200 + spec.selector),
            subject=f"selector-{spec.selector} filename candidate",
            claim=f"In Data/GUI/Main, the loose `{original_leaf}` name has zero exact and casefold matches; the replacement candidate `{rewritten_leaf}` has {exact_packaged} exact-case match and one casefold match, uniquely `{spec.packaged_leaf}`.",
            semantic_status="PROVEN_EXACT_DATA_CENSUS", evidence_locator="Data/GUI/Main immediate-file filename census plus pinned file hash",
            reference_artifact="PF_ATTR_DATA_BINDINGS.tsv", reference_sha256=EXPECTED_DATA_BINDINGS_SHA256,
            reference_keys=f"{spec.binding_key};{spec.binding_evidence_key}",
            query_original_leaf=original_leaf, query_packaged_leaf=rewritten_leaf,
            exact_original_match_count=exact_original, casefold_original_match_count=folded_original,
            exact_packaged_match_count=exact_packaged, casefold_packaged_match_count=folded_packaged,
            matched_path=f"PF_ROOT://GameClient/Data/GUI/Main/{spec.packaged_leaf}",
            blocker="DATA filenames alone do not prove the IMAGE rewrite ran, Windows lookup accepted case differences, or the file opened/decoded/bound at runtime.",
            required_next_evidence="Source-separated runtime resolver/open/decode/bind trace.",
            nonclaim="Existing decoded pixel/shape claims stay owned by PF_ATTR_DATA_BINDINGS and are not copied here.",
        )
        rows.append(row)
        data_rows.append(row)

    special_path = DATA_DIR / SPECIAL_LEAF
    special_raw = special_path.read_bytes()
    if len(special_raw) != SPECIAL_SIZE or sha256(special_raw) != SPECIAL_SHA256:
        raise RuntimeError("special DATA asset pin drift")
    special_decoded = decode_pcz(special_raw)
    special_structure = tga_structure(special_decoded)
    if special_structure != (SPECIAL_DECODED_SIZE, 0, 0, 2, 64, 64, 32, 8):
        raise RuntimeError("special DATA decoded structure drift")
    if sha256(special_decoded) != SPECIAL_DECODED_SHA256 or sha256(special_decoded[:18]) != SPECIAL_HEADER_SHA256:
        raise RuntimeError("special DATA decoded hash drift")
    replacement_leaf = "quest_splend.tg_"
    append_leaf = SPECIAL_LEAF
    if lower_names.count(replacement_leaf.casefold()) != 0 or lower_names.count(append_leaf.casefold()) != 1:
        raise RuntimeError("special double-extension census drift")
    rows.append(data_row(special_path,
        row_kind="DATA_SPECIAL_CONTROL", route_order="299", subject="quest_splend double-extension control",
        claim="Data/GUI/Main contains one casefold match for append candidate `quest_splend.tga.tg_` and zero for replacement candidate `quest_splend.tg_`; in-memory `$pcz` decode yields one structurally valid 64x64x32 type-2 TGA.",
        semantic_status="PROVEN_EXACT_DATA_CONTROL", evidence_locator="pinned file, immediate-directory census, and in-memory structural decode",
        query_original_leaf="quest_splend.tga", query_packaged_leaf=replacement_leaf,
        query_alternate_leaf=append_leaf, exact_original_match_count=0,
        casefold_original_match_count=0, exact_packaged_match_count=0,
        casefold_packaged_match_count=0, casefold_alternate_match_count=1,
        matched_path=f"PF_ROOT://GameClient/Data/GUI/Main/{SPECIAL_LEAF}",
        decoded_size=SPECIAL_DECODED_SIZE, decoded_sha256=SPECIAL_DECODED_SHA256,
        decoded_header_sha256=SPECIAL_HEADER_SHA256,
        decoded_structure="TGA image_type=2;width=64;height=64;pixel_depth=32;descriptor=8;color_map_type=0;id_length=0",
        blocker="No IMAGE selector literal/reference or runtime open/bind evidence connects this special asset to QuestIconBoard.",
        required_next_evidence="A source-separated IMAGE producer/consumer path or runtime request naming this asset.",
        nonclaim="No raw packaged bytes, decoded bytes, pixel values, texture meaning, or selector association is emitted or inferred.",
    ))

    metadata = {
        "facts": facts,
        "selector_keys": selector_keys,
        "data_rows": data_rows,
        "route_key": next(row["resolver_key"] for row in rows if row["row_kind"] == "IMAGE_ROUTE_BOUND"),
        "special_key": rows[-1]["resolver_key"],
    }
    validate_rows(rows, selector_rows, binding_rows, gdl_rows)
    return rows, metadata


def validate_rows(
    rows: Sequence[Mapping[str, str]], selector_rows: Sequence[Mapping[str, str]],
    binding_rows: Sequence[Mapping[str, str]], gdl_rows: Sequence[Mapping[str, str]],
) -> None:
    if len(rows) != 29:
        raise RuntimeError(f"unexpected row count: {len(rows)}")
    for field in ("resolver_key", "claim_sha256", "evidence_key"):
        values = [row[field] for row in rows]
        if len(values) != len(set(values)) or any(not re.fullmatch(r"[0-9a-f]{64}", value) for value in values):
            raise RuntimeError(f"duplicate or malformed {field}")
    if len({tuple(row[field] for field in FIELDNAMES if field != "artifact_pair_sha256") for row in rows}) != len(rows):
        raise RuntimeError("duplicate complete row")
    validate_measurement_schema(rows)
    for row in rows:
        if set(row) != set(FIELDNAMES):
            raise RuntimeError("row schema drift")
        if row["source"] not in {"IMAGE", "DATA"}:
            raise RuntimeError("invalid source layer")
        if any("\t" in value or "\r" in value or "\n" in value for value in row.values()):
            raise RuntimeError("unsafe TSV control character")
        if row["source"] == "IMAGE":
            if row["source_file"] != SOURCE_IMAGE_FILE or row["source_sha256"] != EXPECTED_IMAGE_SHA256:
                raise RuntimeError("IMAGE provenance drift")
            if row["matched_path"] or row["decoded_size"] or row["decoded_sha256"]:
                raise RuntimeError("DATA fact leaked into IMAGE row")
        else:
            if not row["source_file"].startswith("PF_ROOT://GameClient/Data/GUI/Main/"):
                raise RuntimeError("DATA provenance drift")
            if any(row[field] for field in ("span_start", "span_end", "file_offset_start", "file_offset_end", "span_sha256", "support_spans")):
                raise RuntimeError("IMAGE span leaked into DATA row")
            if "PF_ATTR_QUEST_MARK_SELECTOR" in row["reference_artifact"] or "PF_GROUND_DROP" in row["reference_artifact"]:
                raise RuntimeError("cross-source reference leaked into DATA row")
        if (row["runtime_open_status"], row["runtime_bind_status"], row["runtime_pixels_status"]) != ("OPEN", "OPEN", "OPEN"):
            raise RuntimeError("runtime result overclaim")
        if row["row_kind"] not in {"REFERENCE_ONLY", "IMAGE_ROUTE_BOUND", "IMAGE_STRING_CENSUS"} and row["source"] == "IMAGE" and not row["span_sha256"]:
            raise RuntimeError("unanchored IMAGE evidence row")
    existing_claims = {row.get("claim_sha256", "") for row in selector_rows}
    existing_evidence = {row.get("evidence_key", "") for row in (*selector_rows, *binding_rows, *gdl_rows)}
    if existing_claims.intersection(row["claim_sha256"] for row in rows):
        raise RuntimeError("selector claim duplicated")
    if existing_evidence.intersection(row["evidence_key"] for row in rows):
        raise RuntimeError("reference evidence key duplicated")
    primary_spans = [(row["span_start"], row["span_end"]) for row in rows if row["span_start"]]
    if len(primary_spans) != len(set(primary_spans)):
        raise RuntimeError("duplicate local primary span")
    reference_primary = {
        (row.get("selector_branch_va", ""), row.get("selector_branch_end", "")) for row in selector_rows
    } | {
        (row.get("evidence_span_start", ""), row.get("evidence_span_end", "")) for row in gdl_rows
    }
    if set(primary_spans).intersection(reference_primary):
        raise RuntimeError("reference-owned primary span duplicated")
    allowed_reference_keys = {
        value for source_rows in (selector_rows, binding_rows, gdl_rows)
        for row in source_rows for value in (
            row.get("selector_key", ""), row.get("binding_key", ""), row.get("evidence_id", ""),
            row.get("evidence_key", ""), row.get("claim_sha256", ""), row.get("evidence_span_sha256", ""),
        ) if value
    }
    allowed_reference_keys.add("88255f4f1c9a1359a4c7bffd2041300066bde82e83160b235ba4f25e79f116e9")
    for row in rows:
        for key in filter(None, row["reference_keys"].split(";")):
            if key not in allowed_reference_keys:
                raise RuntimeError(f"unresolved reference key: {key}")


def validate_measurement_schema(rows: Sequence[Mapping[str, str]]) -> None:
    """Reject unlabeled, cross-layer, or weakened measurement contracts."""
    for row in rows:
        if set(row) != set(FIELDNAMES):
            raise RuntimeError("measurement schema field set drift")
        if not row["measurement_label"] or not row["method"] or not row["control"]:
            raise RuntimeError("empty measurement label/method/control")
        expected = measurement_profile(row["source"], row["row_kind"])
        actual = (row["measurement_label"], row["method"], row["control"])
        if actual != expected:
            raise RuntimeError(f"measurement profile drift: {row['source']}/{row['row_kind']}")
        if row["measurement_label"] == "REFERENCE":
            if row["semantic_status"] != "REFERENCE_ONLY" or not row["reference_artifact"] or not row["reference_keys"]:
                raise RuntimeError("invalid reference measurement row")
            if row["span_sha256"]:
                raise RuntimeError("reference row gained local primary evidence")
        elif row["measurement_label"] == "COMPOSED_BOUND":
            if row["source"] != "IMAGE" or row["row_kind"] != "IMAGE_ROUTE_BOUND":
                raise RuntimeError("invalid composed-bound row")
            if row["semantic_status"] != "BOUNDED_OPEN_RUNTIME":
                raise RuntimeError("composed bound promoted beyond runtime ceiling")
        elif row["measurement_label"] == "MEASURED":
            if row["semantic_status"] in {"REFERENCE_ONLY", "BOUNDED_OPEN_RUNTIME"}:
                raise RuntimeError("measured row carries reference/composition status")
        else:
            raise RuntimeError("unknown measurement label")
        if row["source"] == "IMAGE" and "DIRECTORY" in row["method"]:
            raise RuntimeError("DATA census method leaked into IMAGE row")
        if row["source"] == "DATA" and "STATIC_IMAGE" in row["method"]:
            raise RuntimeError("IMAGE method leaked into DATA row")


def expect_rejected(label: str, action: Callable[[], None]) -> None:
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError(f"mutation was not rejected: {label}")


def run_mutation_checks(image: bytes, rows: Sequence[Mapping[str, str]]) -> int:
    """Exercise evidence-schema and decisive-span guards using memory-only mutations."""
    mutation_count = 0

    def mutated_rows(index: int, field: str, value: str | None) -> list[dict[str, str]]:
        copied = [dict(row) for row in rows]
        if value is None:
            del copied[index][field]
        else:
            copied[index][field] = value
        return copied

    reference_index = next(i for i, row in enumerate(rows) if row["row_kind"] == "REFERENCE_ONLY")
    data_index = next(i for i, row in enumerate(rows) if row["row_kind"] == "DATA_FILENAME_CENSUS")
    route_index = next(i for i, row in enumerate(rows) if row["row_kind"] == "IMAGE_ROUTE_BOUND")
    measured_index = next(i for i, row in enumerate(rows) if row["row_kind"] == "IMAGE_EXTENSION_RULE")
    mutations = (
        ("missing measurement_label field", lambda: validate_measurement_schema(mutated_rows(measured_index, "measurement_label", None))),
        ("blank method", lambda: validate_measurement_schema(mutated_rows(measured_index, "method", ""))),
        ("blank control", lambda: validate_measurement_schema(mutated_rows(measured_index, "control", ""))),
        ("reference promoted to measured", lambda: validate_measurement_schema(mutated_rows(reference_index, "measurement_label", "MEASURED"))),
        ("DATA row assigned IMAGE method", lambda: validate_measurement_schema(mutated_rows(data_index, "method", "STATIC_IMAGE_HASHED_SPAN_AND_EXACT_CONTROL_FLOW_ASSERTIONS"))),
        ("route bound relabeled measured", lambda: validate_measurement_schema(mutated_rows(route_index, "measurement_label", "MEASURED"))),
        ("measured row relabeled reference", lambda: validate_measurement_schema(mutated_rows(measured_index, "measurement_label", "REFERENCE"))),
    )
    for label, action in mutations:
        expect_rejected(label, action)
        mutation_count += 1

    _, sections = parse_pe(image)
    mutated_image = bytearray(image)
    mutation_off = va_to_file(sections, SPANS["tga_compare"][0])
    mutated_image[mutation_off] ^= 0x01
    expect_rejected(
        "decisive .tga comparison span byte",
        lambda: span_fact(bytes(mutated_image), sections, "tga_compare"),
    )
    mutation_count += 1
    return mutation_count


def render_tsv(rows: Sequence[Mapping[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDNAMES, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def render_report(rows: Sequence[Mapping[str, str]], metadata: Mapping[str, object]) -> bytes:
    image_rows = [row for row in rows if row["source"] == "IMAGE"]
    data_rows = [row for row in rows if row["source"] == "DATA"]
    route = next(row for row in rows if row["row_kind"] == "IMAGE_ROUTE_BOUND")
    lines = [
        "# PF Quest-Mark Resource Resolver",
        "",
        f"Artifact pair SHA-256: `{PAIR_PLACEHOLDER}`",
        f"Canonical final IMAGE route key: `{route['resolver_key']}`",
        f"Special DATA control key: `{metadata['special_key']}`",
        "",
        "## Outcome",
        "",
        "The static client route is closed only as a **conditional mechanism**: the eight already-owned selector literals reach the texture manager; `.tga` is compared case-insensitively and rewritten by replacing its last character (`.tga -> .tg_`, never appending); transformed-first/original fallback, the generic image entry, a registered TGA filter/header/decode reader, and the shared board binder all exist in the pinned IMAGE.",
        "",
        "The result is deliberately not called a runtime success. Concrete file open, callback state, reader selection, asset-specific decode return, texture upload/bind, and visible pixels remain `OPEN` for all eight selectors.",
        "",
        f"Rows: {len(rows)} total ({len(image_rows)} IMAGE, {len(data_rows)} DATA). Every TSV row carries exactly one source layer.",
        "",
        "## Pinned inputs",
        "",
        f"- IMAGE: `GameClient.local.bin`, {EXPECTED_IMAGE_SIZE} bytes, SHA-256 `{EXPECTED_IMAGE_SHA256}`.",
        f"- Selector reference: `PF_ATTR_QUEST_MARK_SELECTOR.tsv`, {EXPECTED_SELECTOR_SIZE} bytes, SHA-256 `{EXPECTED_SELECTOR_SHA256}`.",
        f"- DATA binding reference: `PF_ATTR_DATA_BINDINGS.tsv`, {EXPECTED_DATA_BINDINGS_SIZE} bytes, SHA-256 `{EXPECTED_DATA_BINDINGS_SHA256}`.",
        f"- Generic packaged resolver reference: `PF_GROUND_DROP_LIFETIME.tsv`, {EXPECTED_GROUND_DROP_SIZE} bytes, SHA-256 `{EXPECTED_GROUND_DROP_SHA256}`; only `GDL-IMG-018/019` are cited.",
        "",
        "## [COMPOSITION][IMAGE+DATA] Eight selector candidates",
        "",
        "This table is the only cross-source join. It does not create mixed-source TSV rows or elevate runtime status.",
        "",
        "| selector | owned selector key | IMAGE literal | IMAGE replacement candidate | DATA exact-case | DATA casefold | DATA census key |",
        "|---:|---|---|---|---:|---:|---|",
    ]
    census_by_subject = {row["subject"]: row for row in data_rows if row["row_kind"] == "DATA_FILENAME_CENSUS"}
    for spec in SELECTORS:
        row = census_by_subject[f"selector-{spec.selector} filename candidate"]
        replacement = spec.literal[2:-1] + "_"
        lines.append(
            f"| {spec.selector} | `{spec.selector_key}` | `{spec.literal}` | `{replacement}` | "
            f"{row['exact_packaged_match_count']} | {row['casefold_packaged_match_count']} | `{row['resolver_key']}` |"
        )
    lines.extend([
        "",
        "Four formatted candidates retain uppercase spelling while the shipped filenames are lowercase, so their exact-case count is zero but their casefold count is one. That DATA census is not promoted to a runtime filesystem-open result.",
        "",
        "## Special double-extension control",
        "",
        f"`{SPECIAL_LEAF}` is a distinct DATA-only control: {SPECIAL_SIZE} packaged bytes, SHA-256 `{SPECIAL_SHA256}`. It decodes in memory to {SPECIAL_DECODED_SIZE} bytes with SHA-256 `{SPECIAL_DECODED_SHA256}` and a 64x64x32 type-2 TGA structure. No bytes or pixels are emitted.",
        "",
        "The exact IMAGE rewrite would map `quest_splend.tga` to `quest_splend.tg_`; it cannot produce `quest_splend.tga.tg_`. The pinned IMAGE also has zero exact UTF-16 occurrences of `quest_splend.tga` and `%squest_splend.tga`. These facts do **not** exclude dynamic construction or a separate loader path, but no selector association is proved.",
        "",
        "## Exact static boundary",
        "",
        "1. Selector identities, formatter call, and board binder are cited from `PF_ATTR_QUEST_MARK_SELECTOR.tsv`; their predicates are not duplicated.",
        "2. The manager/cache/resource loader and exists/open callback machinery are exact static control flow, conditional on runtime state.",
        "3. `_splitpath_s` plus `_stricmp` admits `.tga`, and the success tail overwrites the last character with `_`.",
        "4. The converter's reader list dispatches virtual +0x04 filter, +0x0C header/type parse, and +0x08 decode. The registered TGA vtable maps those slots to `0x0092B340`, `0x0092B880`, and `0x0092BC60`.",
        "5. The exact runtime bridge from the generic texture-source object to that converter instance is not proved for the eight quest resources; neither is a returned/bound/visible texture.",
        "",
        "## Duplication and source policy",
        "",
        "- Selector branch facts are imported by their eight selector keys and pinned artifact hash.",
        "- Existing DATA pixel/shape rows are imported only by binding/evidence keys; this artifact adds filename-census facts and the missing special control, not duplicate pixel interpretations.",
        "- The generic packaged resolver and `$pcz` wrapper are cited as `GDL-IMG-018/019`; their generic claims are not reissued.",
        "- IMAGE and DATA never share one TSV row. Cross-source inference is confined to explicitly tagged composition prose/table here.",
        "",
        "## Measurement labels, methods, and controls",
        "",
        "Every TSV row has nonempty `measurement_label`, `method`, and `control` fields. Their accepted combinations are fixed by source and row kind, are included in each evidence key, and are enforced by schema plus mutation checks.",
        "",
        "| boundary | measurement_label | reproducible method | required controls |",
        "|---|---|---|---|",
        "| Local IMAGE spans/censuses | `MEASURED` | pinned-image hashed-span/control-flow assertions, virtual-slot/vtable assertions, or whole-image exact UTF-16LE census | image size/hash, exact span hashes, decisive operands/calls, explicit runtime-open ceiling |",
        "| Local DATA filename/special control | `MEASURED` | immediate-directory exact/casefold census and in-memory `$pcz` structural validation | file size/hash, fixed queries/counts, structural hashes, no raw-byte or pixel output |",
        "| Imported selector/resolver/binder facts | `REFERENCE` | pinned artifact size/hash plus exact key join | key existence, no local primary evidence, no claim reissue |",
        "| Aggregate static ceiling | `COMPOSED_BOUND` | IMAGE-only composition of hashed local rows and pinned IMAGE reference keys | single IMAGE source, no DATA fields, all runtime states remain OPEN |",
        "",
        "The `[COMPOSITION][IMAGE+DATA]` table above remains Markdown-only and therefore is not mislabeled as a measured single-source TSV row.",
        "",
        "## Runtime blockers / required evidence",
        "",
        "A source-separated trace must record, per selector: formatted path; rewrite input/output; installed callback targets; transformed and fallback open results; selected reader vtable; header/decode returns; created texture identity; board binder return/state; and client-visible presentation. Until then `runtime_open_status`, `runtime_bind_status`, and `runtime_pixels_status` remain `OPEN` in every row.",
        "",
        "## Reproduction",
        "",
        "Run `py -3 pf_rederive_quest_mark_resource_resolver.py --check` beside these artifacts. Check mode reads all pinned inputs, reconstructs both outputs, verifies their embedded pair key and stable publication state, and performs no writes. Run `--self-test` separately to perform the same read-only published-pair check plus memory-only mutations covering missing/blank labels, wrong source methods, reference/composition promotion, and a decisive IMAGE span byte.",
        "",
    ])
    return "\n".join(lines).encode("utf-8")


def render_outputs(rows: Sequence[Mapping[str, str]], metadata: Mapping[str, object]) -> tuple[Mapping[Path, bytes], str]:
    normalized_tsv = render_tsv(rows)
    normalized_report = render_report(rows, metadata)
    placeholder = PAIR_PLACEHOLDER.encode("ascii")
    if normalized_tsv.count(placeholder) != len(rows) or normalized_report.count(placeholder) != 1:
        raise RuntimeError("pair placeholder count mismatch")
    pair_sha256 = sha256(
        b"PF_QUEST_MARK_RESOURCE_RESOLVER_TSV\x00" + normalized_tsv
        + b"\x00PF_QUEST_MARK_RESOURCE_RESOLVER_MD\x00" + normalized_report
    )
    replacement = pair_sha256.encode("ascii")
    outputs = {
        TSV_PATH: normalized_tsv.replace(placeholder, replacement),
        REPORT_PATH: normalized_report.replace(placeholder, replacement),
    }
    if outputs[TSV_PATH].count(replacement) != len(rows) or outputs[REPORT_PATH].count(replacement) != 1:
        raise RuntimeError("pair key injection mismatch")
    rederived = sha256(
        b"PF_QUEST_MARK_RESOURCE_RESOLVER_TSV\x00" + outputs[TSV_PATH].replace(replacement, placeholder)
        + b"\x00PF_QUEST_MARK_RESOURCE_RESOLVER_MD\x00" + outputs[REPORT_PATH].replace(replacement, placeholder)
    )
    if rederived != pair_sha256:
        raise RuntimeError("pair key self-check failed")
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
                fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
                temp_path = Path(temp_name)
                staged[path] = temp_path
                with os.fdopen(fd, "wb") as handle:
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
            # Each replacement is atomic.  The embedded pair key detects a mixed-generation read.
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
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows or tuple(rows[0]) != FIELDNAMES:
        raise RuntimeError("published TSV schema drift")
    keys = {row["artifact_pair_sha256"] for row in rows}
    if len(keys) != 1:
        raise RuntimeError("mixed TSV pair keys")
    pair_key = next(iter(keys))
    if not re.fullmatch(r"[0-9a-f]{64}", pair_key):
        raise RuntimeError("malformed pair key")
    match = re.search(rb"Artifact pair SHA-256: `([0-9a-f]{64})`", report_raw)
    if match is None or match.group(1).decode("ascii") != pair_key:
        raise RuntimeError("TSV/Markdown pair key disagreement")
    key_raw = pair_key.encode("ascii")
    placeholder = PAIR_PLACEHOLDER.encode("ascii")
    if tsv_raw.count(key_raw) != len(rows) or report_raw.count(key_raw) != 1:
        raise RuntimeError("published pair key occurrence drift")
    actual = sha256(
        b"PF_QUEST_MARK_RESOURCE_RESOLVER_TSV\x00" + tsv_raw.replace(key_raw, placeholder)
        + b"\x00PF_QUEST_MARK_RESOURCE_RESOLVER_MD\x00" + report_raw.replace(key_raw, placeholder)
    )
    if actual != pair_key:
        raise RuntimeError("published pair hash mismatch")
    return pair_key


def read_stable_published_pair() -> Mapping[Path, bytes]:
    if LOCK_PATH.exists():
        raise RuntimeError("publication in progress")
    paths = (TSV_PATH, REPORT_PATH)
    first_stats = {path: path.stat() for path in paths}
    first = {path: path.read_bytes() for path in paths}
    middle_stats = {path: path.stat() for path in paths}
    second = {path: path.read_bytes() for path in paths}
    final_stats = {path: path.stat() for path in paths}
    if LOCK_PATH.exists():
        raise RuntimeError("publication overlapped --check")
    for path in paths:
        signatures = {(stat.st_size, stat.st_mtime_ns) for stat in (first_stats[path], middle_stats[path], final_stats[path])}
        if len(signatures) != 1 or first[path] != second[path]:
            raise RuntimeError(f"unstable published artifact: {path.name}")
    verify_embedded_pair(first[TSV_PATH], first[REPORT_PATH])
    return first


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="ascii", errors="backslashreplace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="ascii", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="verify published outputs without writing")
    modes.add_argument("--self-test", action="store_true", help="run read-only schema/mutation checks")
    args = parser.parse_args()

    before = IMAGE_PATH.stat()
    if before.st_size != EXPECTED_IMAGE_SIZE:
        raise RuntimeError("image size guard failed")
    image = IMAGE_PATH.read_bytes()
    if len(image) != EXPECTED_IMAGE_SIZE or sha256(image) != EXPECTED_IMAGE_SHA256:
        raise RuntimeError("image hash guard failed")
    rows, metadata = derive(image)
    outputs, pair_sha256 = render_outputs(rows, metadata)
    after = IMAGE_PATH.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns) or sha256(IMAGE_PATH.read_bytes()) != EXPECTED_IMAGE_SHA256:
        raise RuntimeError("image changed during derivation")

    mutation_count = run_mutation_checks(image, rows) if args.self_test else 0
    if args.check or args.self_test:
        published = read_stable_published_pair()
        for path, expected in outputs.items():
            if published[path] != expected:
                raise RuntimeError(f"output drift: {path.name}")
        mode = "SELF_TEST" if args.self_test else "CHECK"
        print(f"PASS mode={mode} rows={len(rows)} image_rows={sum(r['source']=='IMAGE' for r in rows)} data_rows={sum(r['source']=='DATA' for r in rows)} mutations={mutation_count} pair_sha256={pair_sha256} route_key={metadata['route_key']}")
        return 0
    publish_pair(outputs)
    print(f"WROTE rows={len(rows)} image_rows={sum(r['source']=='IMAGE' for r in rows)} data_rows={sum(r['source']=='DATA' for r in rows)} pair_sha256={pair_sha256} route_key={metadata['route_key']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        diagnostic = str(exc).encode("ascii", "backslashreplace").decode("ascii")
        print(f"ERROR: {diagnostic}", file=sys.stderr)
        raise SystemExit(1)
