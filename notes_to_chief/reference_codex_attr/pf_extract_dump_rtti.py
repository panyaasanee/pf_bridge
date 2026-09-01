#!/usr/bin/env python3
"""Extract dump-native x86 MSVC RTTI without exporting memory bytes.

Only address/name/structure/count/SHA metadata is written.  IMAGE bytes and
IMAGE class mappings are deliberately not used to fill gaps in DUMP evidence.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import io
import os
import re
import struct
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


SOURCE = "DUMP"
MINIDUMP_SIGNATURE = b"MDMP"
MINIDUMP_WITH_DATA_SEGS_FLAG = 0x1
MODULE_LIST_STREAM = 4
MEMORY_LIST_STREAM = 5
REQUIRED_STREAM_TYPES = {3, 4, 5, 6, 7, 15}
EXPECTED_DUMPS = {
    "GameClient.local.bin_1.41.01_69151_20260816_040609.dmp": {
        "size": 13_258_352,
        "sha256": "daf63c7d13dc7ca601776cc7e4abbf02aa2e367f91ea420b3b05aaa8af7bffdc",
        "threads": 43,
        "modules": 101,
        "memory_ranges": 335,
        "type_descriptors": 3121,
        "distinct_aligned_values": 1_669_258,
        "mapped_vtable_slots": 26_231,
        "mapped_col_first_entry": 944,
        "col_signature_zero": 68,
        "proven_chains": 0,
    },
    "GameClient.local.bin_1.41.01_69151_20260816_042854.dmp": {
        "size": 13_266_299,
        "sha256": "f982d47b6cec71171ccd2129ee9ce955a0cca05a9d5b606b0c97d5dd28169904",
        "threads": 48,
        "modules": 101,
        "memory_ranges": 339,
        "type_descriptors": 3121,
        "distinct_aligned_values": 1_669_373,
        "mapped_vtable_slots": 26_244,
        "mapped_col_first_entry": 949,
        "col_signature_zero": 66,
        "proven_chains": 0,
    },
}
EXPECTED_OUTPUT_ROWS = 6244
TYPE_NAME_RE = re.compile(rb"\.\?A[UV][\x21-\x7E]{1,240}@@")
RAW_BYTE_RUN_RE = re.compile(
    r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"
)


class DumpError(RuntimeError):
    pass


@dataclass(frozen=True)
class MemoryRange:
    start_va: int
    size: int
    file_off: int

    @property
    def end_va(self) -> int:
        return self.start_va + self.size


@dataclass(frozen=True)
class Module:
    base_va: int
    size: int
    name: str

    @property
    def end_va(self) -> int:
        return self.base_va + self.size


@dataclass(frozen=True)
class TypeDescriptor:
    va: int
    file_off: int
    type_info_vtable_va: int
    decorated_name: str


@dataclass(frozen=True)
class VtableProof:
    vtable_va: int
    vtable_file_off: int
    class_name: str
    type_descriptor_va: int
    object_offset: int
    instance_file_offsets: tuple[int, ...]


@dataclass(frozen=True)
class DumpAnalysis:
    path: Path
    sha256: str
    stream_count: int
    thread_count: int
    module_count: int
    memory_range_count: int
    type_descriptors: tuple[TypeDescriptor, ...]
    vtable_proofs: tuple[VtableProof, ...]
    stage_counts: dict[str, int]


class AddressSpace:
    def __init__(self, data: bytes, ranges: list[MemoryRange]):
        self.data = data
        self.ranges = tuple(sorted(ranges, key=lambda value: value.start_va))
        self.starts = tuple(value.start_va for value in self.ranges)
        prefix_cover_indices = []
        furthest_index = 0
        furthest_end = -1
        for index, memory_range in enumerate(self.ranges):
            if memory_range.end_va > furthest_end:
                furthest_end = memory_range.end_va
                furthest_index = index
            prefix_cover_indices.append(furthest_index)
        self.prefix_cover_indices = tuple(prefix_cover_indices)
        for index, current in enumerate(self.ranges):
            for previous in reversed(self.ranges[:index]):
                overlap_start = max(previous.start_va, current.start_va)
                overlap_end = min(previous.end_va, current.end_va)
                if overlap_start >= overlap_end:
                    continue
                previous_off = previous.file_off + overlap_start - previous.start_va
                current_off = current.file_off + overlap_start - current.start_va
                overlap_size = overlap_end - overlap_start
                if (
                    data[previous_off : previous_off + overlap_size]
                    != data[current_off : current_off + overlap_size]
                ):
                    raise DumpError("conflicting overlapping minidump memory ranges")

    def range_for(self, va: int, size: int) -> MemoryRange | None:
        if va < 0 or size <= 0:
            return None
        index = bisect.bisect_right(self.starts, va) - 1
        if index >= 0:
            memory_range = self.ranges[self.prefix_cover_indices[index]]
            if memory_range.start_va <= va and va + size <= memory_range.end_va:
                return memory_range
        return None

    def read(self, va: int, size: int) -> bytes | None:
        memory_range = self.range_for(va, size)
        if memory_range is None:
            return None
        offset = memory_range.file_off + va - memory_range.start_va
        return self.data[offset : offset + size]

    def file_off(self, va: int, size: int = 1) -> int | None:
        memory_range = self.range_for(va, size)
        if memory_range is None:
            return None
        return memory_range.file_off + va - memory_range.start_va

    def contiguous_from(self, va: int, limit: int) -> bytes | None:
        memory_range = self.range_for(va, 1)
        if memory_range is None:
            return None
        size = min(limit, memory_range.end_va - va)
        return self.read(va, size)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def read_minidump_string(data: bytes, rva: int) -> str:
    if rva < 0 or rva + 4 > len(data):
        raise DumpError("minidump string RVA is outside the file")
    byte_length = struct.unpack_from("<I", data, rva)[0]
    end = rva + 4 + byte_length
    if byte_length % 2 or end > len(data):
        raise DumpError("invalid minidump UTF-16 string")
    return data[rva + 4 : end].decode("utf-16le", errors="strict")


def module_contains(modules: tuple[Module, ...], va: int) -> bool:
    return any(module.base_va <= va < module.end_va for module in modules)


def exact_type_descriptor_at(
    address_space: AddressSpace,
    modules: tuple[Module, ...],
    va: int,
) -> TypeDescriptor | None:
    header = address_space.read(va, 9)
    if header is None:
        return None
    type_info_vtable_va, spare = struct.unpack_from("<II", header, 0)
    if spare != 0 or not module_contains(modules, type_info_vtable_va):
        return None
    candidate = address_space.contiguous_from(va + 8, 247)
    if candidate is None:
        return None
    terminator = candidate.find(b"\x00")
    if terminator < 0:
        return None
    decorated = candidate[:terminator]
    if TYPE_NAME_RE.fullmatch(decorated) is None:
        return None
    try:
        decorated_name = decorated.decode("ascii", errors="strict")
    except UnicodeDecodeError:
        return None
    file_off = address_space.file_off(va, 8 + terminator + 1)
    if file_off is None:
        return None
    return TypeDescriptor(
        va=va,
        file_off=file_off,
        type_info_vtable_va=type_info_vtable_va,
        decorated_name=decorated_name,
    )


def scan_type_descriptors(
    address_space: AddressSpace, modules: tuple[Module, ...]
) -> tuple[TypeDescriptor, ...]:
    result: dict[int, TypeDescriptor] = {}
    for memory_range in address_space.ranges:
        block = address_space.data[
            memory_range.file_off : memory_range.file_off + memory_range.size
        ]
        for match in re.finditer(rb"\.\?A[UV]", block):
            if match.start() < 8:
                continue
            va = memory_range.start_va + match.start() - 8
            descriptor = exact_type_descriptor_at(address_space, modules, va)
            if descriptor is not None:
                result[va] = descriptor
    return tuple(result[va] for va in sorted(result))


def aligned_values(
    address_space: AddressSpace,
) -> tuple[Counter[int], dict[int, list[int]]]:
    counts: Counter[int] = Counter()
    # Locations are retained only for values which later prove to be vtables;
    # the second return value is populated by collect_value_locations().
    for memory_range in address_space.ranges:
        block = memoryview(address_space.data)[
            memory_range.file_off : memory_range.file_off + memory_range.size
        ]
        shift = (-memory_range.start_va) & 3
        usable = (len(block) - shift) // 4 * 4
        counts.update(
            value
            for (value,) in struct.iter_unpack(
                "<I", block[shift : shift + usable]
            )
        )
    return counts, {}


def validate_hierarchy(
    address_space: AddressSpace,
    type_descriptor_va: int,
    hierarchy_va: int,
) -> bool:
    hierarchy = address_space.read(hierarchy_va, 16)
    if hierarchy is None:
        return False
    signature, _attributes, base_count, base_array_va = struct.unpack(
        "<IIII", hierarchy
    )
    if signature != 0 or not (1 <= base_count <= 64):
        return False
    base_array = address_space.read(base_array_va, base_count * 4)
    if base_array is None:
        return False
    base_vas = struct.unpack("<%dI" % base_count, base_array)
    base_descriptors = [address_space.read(value, 28) for value in base_vas]
    if any(value is None for value in base_descriptors):
        return False
    self_descriptor = base_descriptors[0]
    assert self_descriptor is not None
    self_type_va, contained_bases = struct.unpack_from("<II", self_descriptor)
    self_hierarchy_va = struct.unpack_from("<I", self_descriptor, 24)[0]
    return (
        self_type_va == type_descriptor_va
        and contained_bases < base_count
        and self_hierarchy_va == hierarchy_va
    )


def collect_value_locations(
    address_space: AddressSpace, wanted: set[int]
) -> dict[int, tuple[int, ...]]:
    result: dict[int, list[int]] = {value: [] for value in wanted}
    if not wanted:
        return {}
    for memory_range in address_space.ranges:
        block = memoryview(address_space.data)[
            memory_range.file_off : memory_range.file_off + memory_range.size
        ]
        shift = (-memory_range.start_va) & 3
        usable = (len(block) - shift) // 4 * 4
        for index, (value,) in enumerate(
            struct.iter_unpack("<I", block[shift : shift + usable])
        ):
            if value in result:
                result[value].append(memory_range.file_off + shift + index * 4)
    return {value: tuple(offsets) for value, offsets in result.items()}


def prove_vtables(
    address_space: AddressSpace,
    modules: tuple[Module, ...],
    type_descriptors: tuple[TypeDescriptor, ...],
) -> tuple[tuple[VtableProof, ...], dict[str, int]]:
    value_counts, _unused = aligned_values(address_space)
    descriptor_by_va = {value.va: value for value in type_descriptors}
    stages = Counter({"distinct_aligned_values": len(value_counts)})
    preliminary: dict[int, tuple[TypeDescriptor, int]] = {}
    for candidate_vtable_va in value_counts:
        if candidate_vtable_va < 4:
            continue
        table_record = address_space.read(candidate_vtable_va - 4, 8)
        if table_record is None:
            continue
        stages["mapped_vtable_slots"] += 1
        locator_va, first_entry_va = struct.unpack("<II", table_record)
        locator = address_space.read(locator_va, 20)
        if locator is None or not module_contains(modules, first_entry_va):
            continue
        stages["mapped_col_first_entry"] += 1
        (
            signature,
            object_offset,
            _constructor_offset,
            type_descriptor_va,
            hierarchy_va,
        ) = struct.unpack("<IIIII", locator)
        if signature != 0:
            continue
        stages["col_signature_zero"] += 1
        descriptor = descriptor_by_va.get(type_descriptor_va)
        if descriptor is None:
            continue
        stages["exact_type_descriptor"] += 1
        if not validate_hierarchy(
            address_space, type_descriptor_va, hierarchy_va
        ):
            continue
        stages["exact_hierarchy"] += 1
        preliminary[candidate_vtable_va] = (descriptor, object_offset)
    locations = collect_value_locations(address_space, set(preliminary))
    proofs = tuple(
        VtableProof(
            vtable_va=vtable_va,
            vtable_file_off=address_space.file_off(vtable_va, 4)
            if address_space.file_off(vtable_va, 4) is not None
            else -1,
            class_name=descriptor.decorated_name,
            type_descriptor_va=descriptor.va,
            object_offset=object_offset,
            instance_file_offsets=locations[vtable_va],
        )
        for vtable_va, (descriptor, object_offset) in sorted(preliminary.items())
    )
    stages["proven_chains"] = len(proofs)
    stages["proven_pointer_occurrences"] = sum(
        len(value.instance_file_offsets) for value in proofs
    )
    return proofs, dict(stages)


def parse_dump(path: Path) -> DumpAnalysis:
    expected = EXPECTED_DUMPS[path.name]
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest().lower()
    if len(data) != expected["size"] or digest != expected["sha256"]:
        raise DumpError(f"dump identity mismatch: {path.name}")
    if len(data) < 32:
        raise DumpError("truncated minidump header")
    signature, _version, stream_count, directory_rva, _checksum, _timestamp, flags = (
        struct.unpack_from("<4sIIIIIQ", data, 0)
    )
    if signature != MINIDUMP_SIGNATURE or flags != MINIDUMP_WITH_DATA_SEGS_FLAG:
        raise DumpError("unexpected minidump signature or flags")
    if directory_rva + stream_count * 12 > len(data):
        raise DumpError("minidump stream directory is truncated")
    stream_locations: dict[int, tuple[int, int]] = {}
    stream_types = []
    for index in range(stream_count):
        stream_type, size, rva = struct.unpack_from(
            "<III", data, directory_rva + index * 12
        )
        stream_types.append(stream_type)
        if stream_type == 0:
            continue
        if stream_type in stream_locations or rva + size > len(data):
            raise DumpError("duplicate or out-of-file minidump stream")
        stream_locations[stream_type] = (size, rva)
    if not REQUIRED_STREAM_TYPES <= set(stream_types):
        raise DumpError("required minidump streams are missing")

    thread_size, thread_rva = stream_locations[3]
    thread_count = struct.unpack_from("<I", data, thread_rva)[0]
    if thread_size < 4 + thread_count * 48:
        raise DumpError("thread list stream is truncated")

    module_size, module_rva = stream_locations[MODULE_LIST_STREAM]
    module_count = struct.unpack_from("<I", data, module_rva)[0]
    if module_size < 4 + module_count * 108:
        raise DumpError("module list stream is truncated")
    modules = []
    for index in range(module_count):
        offset = module_rva + 4 + index * 108
        base_va, size = struct.unpack_from("<QI", data, offset)
        name_rva = struct.unpack_from("<I", data, offset + 20)[0]
        modules.append(
            Module(
                base_va=base_va,
                size=size,
                name=read_minidump_string(data, name_rva),
            )
        )
    modules_tuple = tuple(sorted(modules, key=lambda value: value.base_va))

    memory_size, memory_rva = stream_locations[MEMORY_LIST_STREAM]
    memory_count = struct.unpack_from("<I", data, memory_rva)[0]
    if memory_size < 4 + memory_count * 16:
        raise DumpError("memory list stream is truncated")
    ranges = []
    for index in range(memory_count):
        offset = memory_rva + 4 + index * 16
        start_va, size, file_off = struct.unpack_from("<QII", data, offset)
        if size <= 0 or file_off + size > len(data):
            raise DumpError("invalid minidump memory descriptor")
        ranges.append(MemoryRange(start_va=start_va, size=size, file_off=file_off))
    address_space = AddressSpace(data, ranges)
    type_descriptors = scan_type_descriptors(address_space, modules_tuple)
    vtable_proofs, stage_counts = prove_vtables(
        address_space, modules_tuple, type_descriptors
    )
    analysis = DumpAnalysis(
        path=path,
        sha256=digest,
        stream_count=stream_count,
        thread_count=thread_count,
        module_count=module_count,
        memory_range_count=memory_count,
        type_descriptors=type_descriptors,
        vtable_proofs=vtable_proofs,
        stage_counts=stage_counts,
    )
    validate_analysis(analysis)
    return analysis


def validate_analysis(analysis: DumpAnalysis) -> None:
    expected = EXPECTED_DUMPS[analysis.path.name]
    measured = {
        "threads": analysis.thread_count,
        "modules": analysis.module_count,
        "memory_ranges": analysis.memory_range_count,
        "type_descriptors": len(analysis.type_descriptors),
        "distinct_aligned_values": analysis.stage_counts.get(
            "distinct_aligned_values", 0
        ),
        "mapped_vtable_slots": analysis.stage_counts.get(
            "mapped_vtable_slots", 0
        ),
        "mapped_col_first_entry": analysis.stage_counts.get(
            "mapped_col_first_entry", 0
        ),
        "col_signature_zero": analysis.stage_counts.get(
            "col_signature_zero", 0
        ),
        "proven_chains": len(analysis.vtable_proofs),
    }
    expected_measured = {key: expected[key] for key in measured}
    if measured != expected_measured:
        changed = {
            key: (expected_measured[key], measured[key])
            for key in measured
            if measured[key] != expected_measured[key]
        }
        raise DumpError(f"{analysis.path.name} structural census changed: {changed}")
    if analysis.stream_count != 8:
        raise DumpError("minidump stream count changed")
    if len({value.va for value in analysis.type_descriptors}) != len(
        analysis.type_descriptors
    ):
        raise DumpError("duplicate TypeDescriptor VA")
    if any(
        TYPE_NAME_RE.fullmatch(value.decorated_name.encode("ascii")) is None
        for value in analysis.type_descriptors
    ):
        raise DumpError("invalid exact RTTI decorated name")


def validate_rtti_mutation_regressions() -> None:
    base = 0x1000
    fixture = bytearray(0x700)
    struct.pack_into("<I", fixture, 0x00, 0x1104)
    struct.pack_into("<II", fixture, 0x100, 0x1200, 0x5000)
    struct.pack_into("<IIIII", fixture, 0x200, 0, 0, 0, 0x1300, 0x1400)
    name = b".?AVFixture@@\x00"
    struct.pack_into("<II", fixture, 0x300, 0x5010, 0)
    fixture[0x308 : 0x308 + len(name)] = name
    struct.pack_into("<IIII", fixture, 0x400, 0, 0, 1, 0x1500)
    struct.pack_into("<I", fixture, 0x500, 0x1600)
    struct.pack_into("<II", fixture, 0x600, 0x1300, 0)
    struct.pack_into("<I", fixture, 0x618, 0x1400)
    modules = (Module(0x5000, 0x1000, "fixture"),)

    def measure(payload: bytes) -> tuple[int, int]:
        space = AddressSpace(payload, [MemoryRange(base, len(payload), 0)])
        descriptors = scan_type_descriptors(space, modules)
        proofs, _stages = prove_vtables(space, modules, descriptors)
        return len(descriptors), len(proofs)

    if measure(bytes(fixture)) != (1, 1):
        raise DumpError("synthetic exact RTTI positive regression failed")
    bad_signature = bytearray(fixture)
    struct.pack_into("<I", bad_signature, 0x200, 1)
    if measure(bytes(bad_signature)) != (1, 0):
        raise DumpError("COL signature mutation was unexpectedly accepted")
    bad_name = bytearray(fixture)
    bad_name[0x308] = ord("X")
    if measure(bytes(bad_name)) != (0, 0):
        raise DumpError("TypeDescriptor name mutation was unexpectedly accepted")
    bad_hierarchy = bytearray(fixture)
    struct.pack_into("<I", bad_hierarchy, 0x400, 1)
    if measure(bytes(bad_hierarchy)) != (1, 0):
        raise DumpError("hierarchy signature mutation was unexpectedly accepted")


def tsv_text(headers: list[str], rows: list[list[str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return stream.getvalue()


OUTPUT_HEADERS = [
    "record_kind",
    "vtable_va",
    "class_name",
    "type_descriptor_name",
    "instance_count",
    "type_descriptor_va",
    "type_descriptor_count",
    "type_info_vtable_va",
    "object_offset",
    "dump_name",
    "dump_sha256",
    "dump_file_offset",
    "instance_file_offsets",
    "rtti_status",
    "source",
]


def build_output_rows(analyses: list[DumpAnalysis]) -> list[list[str]]:
    rows = []
    for analysis in analyses:
        rows.append(
            [
                "SUMMARY",
                "UNKNOWN",
                "UNKNOWN",
                "UNKNOWN",
                "0",
                "UNKNOWN",
                str(len(analysis.type_descriptors)),
                "UNKNOWN",
                "UNKNOWN",
                analysis.path.name,
                analysis.sha256,
                "UNKNOWN",
                "UNKNOWN",
                "NO_COMPLETE_DUMP_NATIVE_VTABLE_RTTI_CHAIN",
                SOURCE,
            ]
        )
        for descriptor in analysis.type_descriptors:
            rows.append(
                [
                    "TYPE_DESCRIPTOR_UNBOUND",
                    "UNKNOWN",
                    "UNKNOWN",
                    descriptor.decorated_name,
                    "0",
                    "0x%08X" % descriptor.va,
                    "1",
                    "0x%08X" % descriptor.type_info_vtable_va,
                    "UNKNOWN",
                    analysis.path.name,
                    analysis.sha256,
                    "0x%08X" % descriptor.file_off,
                    "UNKNOWN",
                    "TYPE_DESCRIPTOR_PRESENT_COL_OR_HIERARCHY_NOT_CAPTURED",
                    SOURCE,
                ]
            )
        for proof in analysis.vtable_proofs:
            rows.append(
                [
                    "VTABLE_CLASS",
                    "0x%08X" % proof.vtable_va,
                    proof.class_name,
                    proof.class_name,
                    str(len(proof.instance_file_offsets)),
                    "0x%08X" % proof.type_descriptor_va,
                    "1",
                    "UNKNOWN",
                    "0x%08X" % proof.object_offset,
                    analysis.path.name,
                    analysis.sha256,
                    "0x%08X" % proof.vtable_file_off,
                    "|".join("0x%08X" % value for value in proof.instance_file_offsets),
                    "EXACT_DUMP_NATIVE_X86_MSVC_RTTI_CHAIN",
                    SOURCE,
                ]
            )
    return rows


def validate_output(
    output_tsv: str, analyses: list[DumpAnalysis], expected_rows: list[list[str]]
) -> None:
    parsed = list(csv.DictReader(io.StringIO(output_tsv), delimiter="\t"))
    if len(parsed) != EXPECTED_OUTPUT_ROWS or list(parsed[0]) != OUTPUT_HEADERS:
        raise DumpError("A6 output row/header census changed")
    if Counter(row["source"] for row in parsed) != Counter(
        {SOURCE: EXPECTED_OUTPUT_ROWS}
    ):
        raise DumpError("A6 output violates source=DUMP")
    expected_dicts = [dict(zip(OUTPUT_HEADERS, row)) for row in expected_rows]
    if parsed != expected_dicts:
        raise DumpError("A6 output differs from exact in-memory evidence rows")
    if Counter(row["record_kind"] for row in parsed) != Counter(
        {"TYPE_DESCRIPTOR_UNBOUND": 6242, "SUMMARY": 2}
    ):
        raise DumpError("A6 record-kind census changed")
    if any(
        row["record_kind"] != "VTABLE_CLASS"
        and (
            row["vtable_va"] != "UNKNOWN"
            or row["class_name"] != "UNKNOWN"
        )
        for row in parsed
    ):
        raise DumpError("A6 unbound record gained a vtable/class claim")
    if any(
        row["record_kind"] == "TYPE_DESCRIPTOR_UNBOUND"
        and int(row["instance_count"]) != 0
        for row in parsed
    ):
        raise DumpError("A6 unbound TypeDescriptor gained an instance claim")
    if RAW_BYTE_RUN_RE.search(output_tsv):
        raise DumpError("A6 TSV raw-byte export guard fired")


def validate_output_mutation_regressions(
    output_tsv: str, analyses: list[DumpAnalysis], expected_rows: list[list[str]]
) -> None:
    rows = list(csv.DictReader(io.StringIO(output_tsv), delimiter="\t"))
    mutations = (
        (0, "source", "IMAGE"),
        (0, "vtable_va", "0x00001000"),
        (1, "class_name", rows[1]["type_descriptor_name"]),
        (1, "instance_count", "1"),
        (1, "dump_file_offset", "0x00000000"),
    )
    for row_index, column, value in mutations:
        mutated = [dict(row) for row in rows]
        mutated[row_index][column] = value
        text = tsv_text(
            OUTPUT_HEADERS,
            [[row[column_name] for column_name in OUTPUT_HEADERS] for row in mutated],
        )
        try:
            validate_output(text, analyses, expected_rows)
        except DumpError:
            pass
        else:
            raise DumpError(f"A6 {column} mutation was unexpectedly accepted")
    raw_mutation = output_tsv + "00 11 22 33 44 55 66 77\n"
    try:
        validate_output(raw_mutation, analyses, expected_rows)
    except DumpError:
        pass
    else:
        raise DumpError("A6 raw-byte mutation was unexpectedly accepted")


def build_markdown(analyses: list[DumpAnalysis]) -> str:
    lines = [
        "# PF runtime class map",
        "",
        "A6 อ่าน minidump ทั้งสองแบบ read-only และส่งออกเฉพาะ address/name/structure/count/SHA metadata; ไม่มี raw dump byte, memory value หรือ hexdump ในผลลัพธ์",
        "",
        "## Result",
        "",
        "- complete dump-native `vtable[-4] -> Complete Object Locator -> hierarchy -> TypeDescriptor` chain: 0",
        "- จึงไม่มีแถวใดที่อนุญาตให้ผูก `vtable_va` กับ `class_name` จาก DUMP ล้วน; ไม่ใช้ IMAGE หรือความใกล้ของสตริงเติมชื่อ",
            "- TypeDescriptor ที่ตรวจโครงสร้างได้ยังถูกรักษาเป็น `TYPE_DESCRIPTOR_UNBOUND` พร้อม `type_descriptor_name`/VA/file offset จริงจาก DUMP และ `instance_count=0`; `class_name` ยังคง `UNKNOWN` เพราะชื่อนั้นยังไม่ถูกผูกกับ vtable",
        "",
        "## Per dump",
        "",
        "| dump | SHA-256 | threads | modules | memory ranges | exact TypeDescriptors | mapped candidate slots | COL+first-entry mapped | COL signature zero | proven chains |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for analysis in analyses:
        lines.append(
            "| `%s` | `%s` | %d | %d | %d | %d | %d | %d | %d | %d |"
            % (
                analysis.path.name,
                analysis.sha256,
                analysis.thread_count,
                analysis.module_count,
                analysis.memory_range_count,
                len(analysis.type_descriptors),
                analysis.stage_counts.get("mapped_vtable_slots", 0),
                analysis.stage_counts.get("mapped_col_first_entry", 0),
                analysis.stage_counts.get("col_signature_zero", 0),
                len(analysis.vtable_proofs),
            )
        )
    lines.extend(
        [
            "",
            "## Why names remain unbound",
            "",
            "ทั้งสองไฟล์เป็น `MiniDumpWithDataSegs` (`flags=0x1`) ที่มี MemoryList แบบเลือกช่วง: พบ TypeDescriptor ในช่วงที่ถูกเก็บ แต่ทุก candidate ที่ผ่าน COL signature ยังขาด TypeDescriptor/hierarchy/base-array linkage อย่างน้อยหนึ่งช่วงภายใน memory ของ dump จึงหยุดก่อนผูกชื่อเสมอ นี่เป็น operational evidence ของ snapshot สองไฟล์นี้ ไม่ใช่คำอ้างว่า executable ไม่มี RTTI",
            "",
            "## TSV contract",
            "",
            "- ทุกแถว `source=DUMP` และอ้าง dump เดียว",
            "- `VTABLE_CLASS` จะเกิดได้เฉพาะ full x86 MSVC RTTI chain ภายใน dump เดียว; รอบนี้มี 0 แถว",
            "- `TYPE_DESCRIPTOR_UNBOUND` เก็บ exact decorated RTTI name ใน `type_descriptor_name` แต่ `vtable_va=UNKNOWN`, `class_name=UNKNOWN` และ `instance_count=0`",
            "- `SUMMARY` หนึ่งแถวต่อ dump บันทึกผลลบโดยไม่สร้างชื่อหรือ vtable สมมุติ",
            "",
        ]
    )
    output = "\n".join(lines)
    if RAW_BYTE_RUN_RE.search(output):
        raise DumpError("A6 Markdown raw-byte export guard fired")
    return output


def atomic_publish(outputs: dict[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, text in outputs.items():
            fd, raw_temp = tempfile.mkstemp(
                prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
            )
            temporary = Path(raw_temp)
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            staged.append((temporary, destination))
        for temporary, destination in staged:
            os.replace(temporary, destination)
    finally:
        for temporary, _destination in staged:
            if temporary.exists():
                temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game-client",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "GameClient",
    )
    parser.add_argument(
        "--external", type=Path, default=Path(__file__).resolve().parent
    )
    args = parser.parse_args()
    root = args.game_client.resolve()
    external = args.external.resolve()
    paths = [root / name for name in EXPECTED_DUMPS]
    before = {path: sha256_file(path) for path in paths}
    if before != {
        path: EXPECTED_DUMPS[path.name]["sha256"] for path in paths
    }:
        raise DumpError("A6 input hash mismatch before analysis")
    validate_rtti_mutation_regressions()
    analyses = [parse_dump(path) for path in paths]
    rows = build_output_rows(analyses)
    output_tsv = tsv_text(OUTPUT_HEADERS, rows)
    validate_output(output_tsv, analyses, rows)
    validate_output_mutation_regressions(output_tsv, analyses, rows)
    output_md = build_markdown(analyses)
    after = {path: sha256_file(path) for path in paths}
    if after != before:
        raise DumpError("A6 dump input changed during analysis")
    atomic_publish(
        {
            external / "PF_RUNTIME_CLASSMAP.tsv": output_tsv,
            external / "PF_RUNTIME_CLASSMAP.md": output_md,
        }
    )
    print(
        "dump_count=%d type_descriptors=%d proven_vtable_class_chains=%d rows=%d"
        % (
            len(analyses),
            sum(len(value.type_descriptors) for value in analyses),
            sum(len(value.vtable_proofs) for value in analyses),
            len(rows),
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DumpError as exc:
        raise SystemExit(f"ERROR: {exc}")
