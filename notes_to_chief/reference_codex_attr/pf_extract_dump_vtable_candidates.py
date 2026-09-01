#!/usr/bin/env python3
"""Audit broad dump RTTI/vtable hits without promoting rejected hits.

The immutable V1 A6 extractor measured 68 + 66 aligned pointer values which
reached a mapped, signature-zero COL-like record and a first entry inside a
loaded module. None passed the complete strict binding. This additive audit
keeps one metadata-only DUMP row for every broad hit and names every failed
strict predicate. Only a hit passing all predicates may receive
record_kind=VTABLE_CANDIDATE_CLASS_UNKNOWN and a strict_vtable_va.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import struct
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

sys.dont_write_bytecode = True

import pf_extract_dump_rtti as v1


SOURCE = "DUMP"
BASE_A6_TSV_SHA256 = (
    "c53a6eaf23911765ebabd5e86ccaecf827ffdd88a1f514fc3f0f3ea2c3484985"
)
BASE_A6_SCRIPT_SHA256 = (
    "54b7bcfecf598007ea468309481f8e41ff64e4139026a0ee200984b03ad82a2b"
)
EXPECTED_BROAD_HITS = {
    "GameClient.local.bin_1.41.01_69151_20260816_040609.dmp": 68,
    "GameClient.local.bin_1.41.01_69151_20260816_042854.dmp": 66,
}
EXPECTED_STRICT_HITS = {
    "GameClient.local.bin_1.41.01_69151_20260816_040609.dmp": 0,
    "GameClient.local.bin_1.41.01_69151_20260816_042854.dmp": 0,
}
RAW_BYTE_RUN_RE = re.compile(
    r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"
)


class CandidateError(RuntimeError):
    pass


@dataclass(frozen=True)
class BroadDecision:
    dump_name: str
    dump_sha256: str
    broad_pointer_value: int
    broad_pointer_dump_file_offset: int
    pointer_occurrence_file_offsets: tuple[int, ...]
    locator_va: int
    locator_dump_file_offset: int
    locator_signature: int
    locator_object_offset: int
    locator_constructor_displacement: int
    locator_type_descriptor_va: int
    locator_hierarchy_va: int
    first_entry_va: int
    broad_pointer_module: str
    locator_module: str
    type_descriptor_module: str
    hierarchy_module: str
    first_entry_module: str
    type_descriptor_name: str
    rejection_reasons: tuple[str, ...]

    @property
    def accepted(self) -> bool:
        return not self.rejection_reasons


@dataclass(frozen=True)
class ScanResult:
    decisions: tuple[BroadDecision, ...]
    type_descriptor_count: int
    distinct_aligned_values: int
    mapped_table_slots: int
    mapped_locators: int
    mapped_locator_first_entry: int
    signature_zero_locators: int
    broad_signature_zero_first_entry_hits: int


REJECTION_ORDER = (
    "BROAD_POINTER_NOT_ALIGNED",
    "LOCATOR_VA_NOT_ALIGNED",
    "TYPE_DESCRIPTOR_VA_NOT_ALIGNED",
    "HIERARCHY_VA_NOT_ALIGNED",
    "BROAD_POINTER_OUTSIDE_LOADED_MODULE",
    "LOCATOR_OUTSIDE_LOADED_MODULE",
    "TYPE_DESCRIPTOR_OUTSIDE_LOADED_MODULE",
    "HIERARCHY_OUTSIDE_LOADED_MODULE",
    "RTTI_ADDRESSES_NOT_IN_SAME_LOADED_MODULE",
    "FIRST_ENTRY_OUTSIDE_LOADED_MODULE",
    "TYPE_DESCRIPTOR_NOT_EXACT_OR_NOT_CAPTURED",
    "HIERARCHY_CHAIN_INVALID_OR_NOT_CAPTURED",
)


HEADERS = [
    "record_kind",
    "strict_vtable_va",
    "class_name",
    "instance_count",
    "count_semantics",
    "broad_pointer_value",
    "pointer_occurrence_count",
    "pointer_occurrence_dump_file_offsets",
    "broad_pointer_dump_file_offset",
    "dump_name",
    "dump_sha256",
    "locator_va",
    "locator_dump_file_offset",
    "broad_pointer_module",
    "locator_module",
    "type_descriptor_module",
    "hierarchy_module",
    "first_entry_module",
    "type_descriptor_name",
    "primary_rejection_reason",
    "all_rejection_reasons",
    "dedup_key",
    "source",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def module_for(modules: tuple[v1.Module, ...], va: int) -> v1.Module | None:
    for module in modules:
        if module.base_va <= va < module.end_va:
            return module
    return None


def module_label(module: v1.Module | None) -> str:
    if module is None:
        return "UNKNOWN"
    leaf = module.name.replace("\\", "/").rsplit("/", 1)[-1]
    return "%s@0x%08X+0x%X" % (leaf, module.base_va, module.size)


def read_dump_space(
    path: Path,
) -> tuple[str, v1.AddressSpace, tuple[v1.Module, ...]]:
    expected = v1.EXPECTED_DUMPS.get(path.name)
    if expected is None:
        raise CandidateError("dump is not in the pinned A6 input set: " + path.name)
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest().lower()
    if len(data) != expected["size"] or digest != expected["sha256"]:
        raise CandidateError("dump identity mismatch: " + path.name)
    if len(data) < 32:
        raise CandidateError("truncated minidump header: " + path.name)
    signature, _version, stream_count, directory_rva, _checksum, _timestamp, flags = (
        struct.unpack_from("<4sIIIIIQ", data, 0)
    )
    if signature != v1.MINIDUMP_SIGNATURE:
        raise CandidateError("unexpected minidump signature: " + path.name)
    if flags != v1.MINIDUMP_WITH_DATA_SEGS_FLAG:
        raise CandidateError("unexpected minidump flags: " + path.name)
    if directory_rva + stream_count * 12 > len(data):
        raise CandidateError("truncated minidump directory: " + path.name)
    streams: dict[int, tuple[int, int]] = {}
    for index in range(stream_count):
        stream_type, size, rva = struct.unpack_from(
            "<III", data, directory_rva + index * 12
        )
        if stream_type and stream_type not in streams:
            streams[stream_type] = (size, rva)
    if v1.MODULE_LIST_STREAM not in streams or v1.MEMORY_LIST_STREAM not in streams:
        raise CandidateError("required minidump stream absent: " + path.name)

    module_size, module_rva = streams[v1.MODULE_LIST_STREAM]
    if module_rva + 4 > len(data):
        raise CandidateError("truncated module-list header: " + path.name)
    module_count = struct.unpack_from("<I", data, module_rva)[0]
    if module_size < 4 + module_count * 108:
        raise CandidateError("truncated module list: " + path.name)
    modules: list[v1.Module] = []
    for index in range(module_count):
        offset = module_rva + 4 + index * 108
        if offset + 108 > len(data):
            raise CandidateError("module record outside dump: " + path.name)
        base_va, size = struct.unpack_from("<QI", data, offset)
        name_rva = struct.unpack_from("<I", data, offset + 20)[0]
        modules.append(
            v1.Module(
                base_va=base_va,
                size=size,
                name=v1.read_minidump_string(data, name_rva),
            )
        )
    if module_count != expected["modules"]:
        raise CandidateError("pinned module census changed: " + path.name)

    memory_size, memory_rva = streams[v1.MEMORY_LIST_STREAM]
    if memory_rva + 4 > len(data):
        raise CandidateError("truncated memory-list header: " + path.name)
    memory_count = struct.unpack_from("<I", data, memory_rva)[0]
    if memory_size < 4 + memory_count * 16:
        raise CandidateError("truncated memory list: " + path.name)
    ranges: list[v1.MemoryRange] = []
    for index in range(memory_count):
        offset = memory_rva + 4 + index * 16
        if offset + 16 > len(data):
            raise CandidateError("memory descriptor outside dump: " + path.name)
        start_va, size, file_off = struct.unpack_from("<QII", data, offset)
        if not size or file_off + size > len(data):
            raise CandidateError("invalid memory descriptor: " + path.name)
        ranges.append(
            v1.MemoryRange(start_va=start_va, size=size, file_off=file_off)
        )
    if memory_count != expected["memory_ranges"]:
        raise CandidateError("pinned memory-range census changed: " + path.name)
    return (
        digest,
        v1.AddressSpace(data, ranges),
        tuple(sorted(modules, key=lambda value: value.base_va)),
    )


def strict_rejection_reasons(
    *,
    broad_pointer_value: int,
    locator_va: int,
    type_descriptor_va: int,
    hierarchy_va: int,
    first_entry_va: int,
    address_space: v1.AddressSpace,
    modules: tuple[v1.Module, ...],
    descriptor_by_va: dict[int, v1.TypeDescriptor],
) -> tuple[str, ...]:
    candidate_module = module_for(modules, broad_pointer_value)
    locator_module = module_for(modules, locator_va)
    type_module = module_for(modules, type_descriptor_va)
    hierarchy_module = module_for(modules, hierarchy_va)
    first_entry_module = module_for(modules, first_entry_va)
    failed: set[str] = set()
    if broad_pointer_value & 3:
        failed.add("BROAD_POINTER_NOT_ALIGNED")
    if locator_va & 3:
        failed.add("LOCATOR_VA_NOT_ALIGNED")
    if type_descriptor_va & 3:
        failed.add("TYPE_DESCRIPTOR_VA_NOT_ALIGNED")
    if hierarchy_va & 3:
        failed.add("HIERARCHY_VA_NOT_ALIGNED")
    if candidate_module is None:
        failed.add("BROAD_POINTER_OUTSIDE_LOADED_MODULE")
    if locator_module is None:
        failed.add("LOCATOR_OUTSIDE_LOADED_MODULE")
    if type_module is None:
        failed.add("TYPE_DESCRIPTOR_OUTSIDE_LOADED_MODULE")
    if hierarchy_module is None:
        failed.add("HIERARCHY_OUTSIDE_LOADED_MODULE")
    structural_modules = (
        candidate_module,
        locator_module,
        type_module,
        hierarchy_module,
    )
    if any(value is None for value in structural_modules) or len(
        {value.base_va for value in structural_modules if value is not None}
    ) != 1:
        failed.add("RTTI_ADDRESSES_NOT_IN_SAME_LOADED_MODULE")
    if first_entry_module is None:
        failed.add("FIRST_ENTRY_OUTSIDE_LOADED_MODULE")
    descriptor = descriptor_by_va.get(type_descriptor_va)
    if descriptor is None:
        failed.add("TYPE_DESCRIPTOR_NOT_EXACT_OR_NOT_CAPTURED")
    if descriptor is None or not v1.validate_hierarchy(
        address_space, type_descriptor_va, hierarchy_va
    ):
        failed.add("HIERARCHY_CHAIN_INVALID_OR_NOT_CAPTURED")
    unknown = failed.difference(REJECTION_ORDER)
    if unknown:
        raise CandidateError("unnamed strict rejection predicate: " + repr(unknown))
    return tuple(reason for reason in REJECTION_ORDER if reason in failed)


def scan_core(
    *,
    dump_name: str,
    dump_sha256: str,
    address_space: v1.AddressSpace,
    modules: tuple[v1.Module, ...],
) -> ScanResult:
    value_counts, _unused = v1.aligned_values(address_space)
    descriptors = v1.scan_type_descriptors(address_space, modules)
    descriptor_by_va = {value.va: value for value in descriptors}
    if len(descriptor_by_va) != len(descriptors):
        raise CandidateError("duplicate exact TypeDescriptor address")
    stages: Counter[str] = Counter()
    preliminary: list[tuple[int, tuple[object, ...]]] = []
    for broad_pointer_value in sorted(value_counts):
        if broad_pointer_value < 4:
            continue
        table_record = address_space.read(broad_pointer_value - 4, 8)
        if table_record is None:
            continue
        stages["mapped_table_slots"] += 1
        locator_va, first_entry_va = struct.unpack("<II", table_record)
        locator = address_space.read(locator_va, 20)
        if locator is None:
            continue
        stages["mapped_locators"] += 1
        first_entry_module = module_for(modules, first_entry_va)
        if first_entry_module is not None:
            stages["mapped_locator_first_entry"] += 1
        (
            locator_signature,
            object_offset,
            constructor_displacement,
            type_descriptor_va,
            hierarchy_va,
        ) = struct.unpack("<IIIII", locator)
        if locator_signature != 0:
            continue
        stages["signature_zero_locators"] += 1
        # The immutable A6 broad census included only signature-zero locator
        # records whose first vtable entry was inside a loaded module.
        if first_entry_module is None:
            continue
        stages["broad_signature_zero_first_entry_hits"] += 1
        reasons = strict_rejection_reasons(
            broad_pointer_value=broad_pointer_value,
            locator_va=locator_va,
            type_descriptor_va=type_descriptor_va,
            hierarchy_va=hierarchy_va,
            first_entry_va=first_entry_va,
            address_space=address_space,
            modules=modules,
            descriptor_by_va=descriptor_by_va,
        )
        preliminary.append(
            (
                broad_pointer_value,
                (
                    locator_va,
                    first_entry_va,
                    locator_signature,
                    object_offset,
                    constructor_displacement,
                    type_descriptor_va,
                    hierarchy_va,
                    *reasons,
                ),
            )
        )

    locations = v1.collect_value_locations(
        address_space, {value for value, _metadata in preliminary}
    )
    decisions: list[BroadDecision] = []
    for broad_pointer_value, metadata in preliminary:
        (
            locator_va,
            first_entry_va,
            locator_signature,
            object_offset,
            constructor_displacement,
            type_descriptor_va,
            hierarchy_va,
            *reason_values,
        ) = metadata
        reasons = tuple(str(value) for value in reason_values)
        pointer_offsets = locations.get(broad_pointer_value, ())
        if len(pointer_offsets) != value_counts[broad_pointer_value] or not pointer_offsets:
            raise CandidateError("broad pointer occurrence census mismatch")
        broad_file_off = address_space.file_off(broad_pointer_value, 4)
        locator_file_off = address_space.file_off(locator_va, 20)
        if broad_file_off is None or locator_file_off is None:
            raise CandidateError("broad hit lost a mapped structure offset")
        descriptor = descriptor_by_va.get(type_descriptor_va)
        decisions.append(
            BroadDecision(
                dump_name=dump_name,
                dump_sha256=dump_sha256,
                broad_pointer_value=broad_pointer_value,
                broad_pointer_dump_file_offset=broad_file_off,
                pointer_occurrence_file_offsets=pointer_offsets,
                locator_va=int(locator_va),
                locator_dump_file_offset=locator_file_off,
                locator_signature=int(locator_signature),
                locator_object_offset=int(object_offset),
                locator_constructor_displacement=int(constructor_displacement),
                locator_type_descriptor_va=int(type_descriptor_va),
                locator_hierarchy_va=int(hierarchy_va),
                first_entry_va=int(first_entry_va),
                broad_pointer_module=module_label(
                    module_for(modules, broad_pointer_value)
                ),
                locator_module=module_label(module_for(modules, int(locator_va))),
                type_descriptor_module=module_label(
                    module_for(modules, int(type_descriptor_va))
                ),
                hierarchy_module=module_label(
                    module_for(modules, int(hierarchy_va))
                ),
                first_entry_module=module_label(
                    module_for(modules, int(first_entry_va))
                ),
                type_descriptor_name=(
                    descriptor.decorated_name if descriptor is not None else "UNKNOWN"
                ),
                rejection_reasons=reasons,
            )
        )
    return ScanResult(
        decisions=tuple(decisions),
        type_descriptor_count=len(descriptors),
        distinct_aligned_values=len(value_counts),
        mapped_table_slots=stages["mapped_table_slots"],
        mapped_locators=stages["mapped_locators"],
        mapped_locator_first_entry=stages["mapped_locator_first_entry"],
        signature_zero_locators=stages["signature_zero_locators"],
        broad_signature_zero_first_entry_hits=stages[
            "broad_signature_zero_first_entry_hits"
        ],
    )


def synthetic_control_payload() -> tuple[bytes, tuple[v1.Module, ...]]:
    base = 0x1000
    fixture = bytearray(0x1000)
    # An aligned occurrence of the candidate vtable pointer.
    struct.pack_into("<I", fixture, 0x000, 0x1104)
    # vtable[-4] = COL; vtable[0] = first function entry.
    struct.pack_into("<II", fixture, 0x100, 0x1200, 0x1800)
    # x86 CompleteObjectLocator.
    struct.pack_into("<IIIII", fixture, 0x200, 0, 0, 0, 0x1300, 0x1400)
    # Exact TypeDescriptor.
    name = b".?AVStrictControl@@\x00"
    struct.pack_into("<II", fixture, 0x300, 0x1810, 0)
    fixture[0x308 : 0x308 + len(name)] = name
    # CompleteClassHierarchyDescriptor -> base-class array -> self descriptor.
    struct.pack_into("<IIII", fixture, 0x400, 0, 0, 1, 0x1500)
    struct.pack_into("<I", fixture, 0x500, 0x1600)
    struct.pack_into("<II", fixture, 0x600, 0x1300, 0)
    struct.pack_into("<I", fixture, 0x618, 0x1400)
    return bytes(fixture), (v1.Module(base, len(fixture), "strict-control"),)


def run_synthetic_controls() -> None:
    base = 0x1000
    positive, modules = synthetic_control_payload()

    def measure(payload: bytes) -> ScanResult:
        space = v1.AddressSpace(
            payload, [v1.MemoryRange(start_va=base, size=len(payload), file_off=0)]
        )
        return scan_core(
            dump_name="SYNTHETIC_NOT_EXPORTED",
            dump_sha256=hashlib.sha256(payload).hexdigest(),
            address_space=space,
            modules=modules,
        )

    result = measure(positive)
    if len(result.decisions) != 1 or sum(
        decision.accepted for decision in result.decisions
    ) != 1:
        raise CandidateError("strict synthetic positive did not produce exactly 1 row")

    bad_signature = bytearray(positive)
    struct.pack_into("<I", bad_signature, 0x200, 1)
    result = measure(bytes(bad_signature))
    if sum(decision.accepted for decision in result.decisions) != 0:
        raise CandidateError("signature mutation was accepted")

    bad_type_module = bytearray(positive)
    struct.pack_into("<I", bad_type_module, 0x20C, 0x3000)
    result = measure(bytes(bad_type_module))
    if sum(decision.accepted for decision in result.decisions) != 0:
        raise CandidateError("outside-module TypeDescriptor mutation was accepted")
    if not result.decisions or "TYPE_DESCRIPTOR_OUTSIDE_LOADED_MODULE" not in (
        result.decisions[0].rejection_reasons
    ):
        raise CandidateError("outside-module TypeDescriptor mutation lacked reason")

    bad_first_entry = bytearray(positive)
    struct.pack_into("<I", bad_first_entry, 0x104, 0x3000)
    result = measure(bytes(bad_first_entry))
    if sum(decision.accepted for decision in result.decisions) != 0:
        raise CandidateError("outside-module first-entry mutation was accepted")


def existing_strict_keys(base_tsv: Path) -> set[str]:
    if sha256_file(base_tsv) != BASE_A6_TSV_SHA256:
        raise CandidateError("immutable V1 A6 TSV hash mismatch")
    keys: set[str] = set()
    with base_tsv.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            if row["vtable_va"] != "UNKNOWN":
                keys.add(row["dump_sha256"] + "|" + row["vtable_va"].upper())
    return keys


def build_tsv(
    decisions: tuple[BroadDecision, ...], existing: set[str]
) -> tuple[str, dict[str, int]]:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(HEADERS)
    seen: set[str] = set()
    counts = {"audit_added": 0, "strict_added": 0, "duplicate": 0}
    for decision in decisions:
        dedup_key = "%s|0x%08X" % (
            decision.dump_sha256,
            decision.broad_pointer_value,
        )
        if dedup_key in seen:
            counts["duplicate"] += 1
            continue
        seen.add(dedup_key)
        strict_key = "%s|0X%08X" % (
            decision.dump_sha256,
            decision.broad_pointer_value,
        )
        if decision.accepted and strict_key in existing:
            counts["duplicate"] += 1
            continue
        if decision.accepted:
            record_kind = "VTABLE_CANDIDATE_CLASS_UNKNOWN"
            strict_vtable_va = "0x%08X" % decision.broad_pointer_value
            instance_count = str(len(decision.pointer_occurrence_file_offsets))
            primary_reason = "NONE"
            all_reasons = "NONE"
            counts["strict_added"] += 1
        else:
            record_kind = "REJECTED_NOT_VTABLE"
            strict_vtable_va = "UNKNOWN"
            instance_count = "0"
            primary_reason = decision.rejection_reasons[0]
            all_reasons = "|".join(decision.rejection_reasons)
            counts["audit_added"] += 1
        writer.writerow(
            [
                record_kind,
                strict_vtable_va,
                "UNKNOWN",
                instance_count,
                (
                    "STRICT_CANDIDATE_POINTER_OCCURRENCES"
                    if decision.accepted
                    else "REJECTED_BROAD_HIT_INSTANCE_COUNT_FORCED_ZERO"
                ),
                "0x%08X" % decision.broad_pointer_value,
                str(len(decision.pointer_occurrence_file_offsets)),
                "|".join(
                    "0x%08X" % value
                    for value in decision.pointer_occurrence_file_offsets
                ),
                "0x%08X" % decision.broad_pointer_dump_file_offset,
                decision.dump_name,
                decision.dump_sha256,
                "0x%08X" % decision.locator_va,
                "0x%08X" % decision.locator_dump_file_offset,
                decision.broad_pointer_module,
                decision.locator_module,
                decision.type_descriptor_module,
                decision.hierarchy_module,
                decision.first_entry_module,
                decision.type_descriptor_name,
                primary_reason,
                all_reasons,
                dedup_key,
                SOURCE,
            ]
        )
    text = output.getvalue()
    if RAW_BYTE_RUN_RE.search(text):
        raise CandidateError("raw-byte export guard fired for A6 audit TSV")
    parsed = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    if len(parsed) != counts["audit_added"] + counts["strict_added"]:
        raise CandidateError("A6 audit output row census mismatch")
    if any(row["source"] != SOURCE for row in parsed):
        raise CandidateError("A6 audit source-layer violation")
    if len({row["dedup_key"] for row in parsed}) != len(parsed):
        raise CandidateError("duplicate A6 audit output key")
    forbidden_unvalidated_words = {
        "locator_signature",
        "locator_object_offset",
        "locator_constructor_displacement",
        "locator_type_descriptor_va",
        "locator_hierarchy_va",
        "first_entry_va",
    }
    if forbidden_unvalidated_words.intersection(parsed[0]):
        raise CandidateError("unvalidated dump words leaked into A6 audit schema")
    for row in parsed:
        if row["record_kind"] == "REJECTED_NOT_VTABLE" and (
            row["strict_vtable_va"] != "UNKNOWN"
            or row["class_name"] != "UNKNOWN"
            or row["instance_count"] != "0"
            or row["primary_rejection_reason"] == "NONE"
        ):
            raise CandidateError("rejected broad hit was promoted")
    return text, counts


def build_markdown(
    *,
    decisions: tuple[BroadDecision, ...],
    scans: dict[str, ScanResult],
    tsv_text: str,
    counts: dict[str, int],
    extractor_sha256: str,
) -> str:
    primary = Counter(
        decision.rejection_reasons[0]
        for decision in decisions
        if not decision.accepted
    )
    all_predicates = Counter(
        reason
        for decision in decisions
        for reason in decision.rejection_reasons
    )
    strict = sum(decision.accepted for decision in decisions)
    rejected = len(decisions) - strict
    lines = [
        "# A6 broad-hit rejection audit delta",
        "",
        "[MEASURED] This is a DUMP-only additive audit over the immutable V1 A6 outputs. It preserves every broad signature-zero hit as metadata but does not promote a rejected hit to a vtable.",
        "",
        "## Result and duplicate control",
        "",
        "- broad signature-zero + in-module-first-entry rows: %d" % len(decisions),
        "- strict accepted candidates: %d" % strict,
        "- evidence-rejected broad hits: %d" % rejected,
        "- audit_added: %d" % counts["audit_added"],
        "- strict_added: %d" % counts["strict_added"],
        "- duplicate: %d" % counts["duplicate"],
        "- immutable base A6 TSV SHA-256: %s" % BASE_A6_TSV_SHA256,
        "- immutable base A6 extractor SHA-256: %s" % BASE_A6_SCRIPT_SHA256,
        "- this audit extractor SHA-256: %s" % extractor_sha256,
        "- audit TSV SHA-256: %s"
        % hashlib.sha256(tsv_text.encode("utf-8")).hexdigest(),
        "",
        "The 134 TSV rows are new rejection-audit records, not duplicate class-map rows. Every rejected row forces `strict_vtable_va=UNKNOWN`, `class_name=UNKNOWN`, and `instance_count=0`; its separate pointer-occurrence fields are a search census, not a live-object count. Unvalidated 32-bit words from rejected locator-shaped records are withheld rather than exported as if they were proven structure fields.",
        "",
        "## Per dump",
        "",
    ]
    for dump_name in sorted(scans):
        scan = scans[dump_name]
        accepted = sum(decision.accepted for decision in scan.decisions)
        digest = scan.decisions[0].dump_sha256
        lines.append(
            "- %s: sha256=%s, broad=%d, strict=%d, rejected=%d, type_descriptors=%d, distinct_aligned_values=%d, mapped_table_slots=%d, mapped_locator_first_entry=%d"
            % (
                dump_name,
                digest,
                len(scan.decisions),
                accepted,
                len(scan.decisions) - accepted,
                scan.type_descriptor_count,
                scan.distinct_aligned_values,
                scan.mapped_table_slots,
                scan.mapped_locator_first_entry,
            )
        )
    lines.extend(
        [
            "",
            "## Primary rejection partition",
            "",
            "Primary reasons are ordered deterministically; their counts partition all %d rejected rows." % rejected,
            "",
        ]
    )
    for reason in REJECTION_ORDER:
        if primary[reason]:
            lines.append("- %s: %d" % (reason, primary[reason]))
    lines.extend(
        [
            "- partition total: %d" % sum(primary.values()),
            "",
            "## All failed-predicate counts",
            "",
            "A row may fail more than one predicate, so this section is not a partition.",
            "",
        ]
    )
    for reason in REJECTION_ORDER:
        lines.append("- %s: %d" % (reason, all_predicates[reason]))
    lines.extend(
        [
            "",
            "## Strict acceptance contract",
            "",
            "A strict candidate must use aligned candidate/COL/TypeDescriptor/hierarchy addresses; all four addresses must lie inside the same loaded module; the first table entry must lie inside a loaded module; the TypeDescriptor must be exact; and the hierarchy/base-array/self-descriptor chain must validate inside the same dump snapshot. The class remains `UNKNOWN` in this candidate delta.",
            "",
            "The refactored scan core has a synthetic full-chain positive control that must accept exactly one candidate. Signature, outside-module TypeDescriptor, and outside-module first-entry mutations must each accept zero. These controls prove that the zero strict count in the real dumps is not a vacuous acceptance path.",
            "",
            "## Evidence boundary",
            "",
            "The broad rows are locator-shaped search hits only. They cannot be used as vtable addresses, class identities, or object-instance counts. Candidate pointer addresses, dump offsets, module-membership labels, rejection reasons, counts, names, and SHA-256 values are retained; unvalidated locator scalar words are not exported. No IMAGE inference, nearby-string heuristic, raw dump byte, or hexdump is exported. Every TSV row has exactly one evidence layer: `source=DUMP`.",
            "",
        ]
    )
    output = "\n".join(lines)
    if RAW_BYTE_RUN_RE.search(output):
        raise CandidateError("raw-byte export guard fired for A6 audit report")
    return output


def atomic_publish(outputs: dict[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, text in outputs.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            fd, raw_temp = tempfile.mkstemp(
                prefix=".%s." % destination.name,
                suffix=".tmp",
                dir=destination.parent,
            )
            temporary = Path(raw_temp)
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
                stream.write(text)
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
        "--output-dir", type=Path, default=Path(__file__).resolve().parent
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="derive in memory and require byte-identical existing outputs",
    )
    args = parser.parse_args()
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    base_tsv = script_dir / "PF_RUNTIME_CLASSMAP.tsv"
    base_script = script_dir / "pf_extract_dump_rtti.py"
    if sha256_file(base_script) != BASE_A6_SCRIPT_SHA256:
        raise CandidateError("immutable V1 A6 extractor hash mismatch")
    pinned_before = {
        base_tsv: sha256_file(base_tsv),
        base_script: sha256_file(base_script),
    }
    existing = existing_strict_keys(base_tsv)
    run_synthetic_controls()

    scans: dict[str, ScanResult] = {}
    decisions: list[BroadDecision] = []
    dump_paths = [
        args.game_client / dump_name for dump_name in sorted(EXPECTED_BROAD_HITS)
    ]
    dump_hashes_before = {path: sha256_file(path) for path in dump_paths}
    for dump_name, dump_path in zip(sorted(EXPECTED_BROAD_HITS), dump_paths):
        digest, address_space, modules = read_dump_space(dump_path)
        scan = scan_core(
            dump_name=dump_name,
            dump_sha256=digest,
            address_space=address_space,
            modules=modules,
        )
        scans[dump_name] = scan
        broad = len(scan.decisions)
        strict = sum(decision.accepted for decision in scan.decisions)
        structural = {
            "type_descriptors": scan.type_descriptor_count,
            "distinct_aligned_values": scan.distinct_aligned_values,
            "mapped_vtable_slots": scan.mapped_table_slots,
            "mapped_col_first_entry": scan.mapped_locator_first_entry,
        }
        expected_structural = {
            key: v1.EXPECTED_DUMPS[dump_name][key] for key in structural
        }
        if structural != expected_structural:
            raise CandidateError(
                "%s pinned structural census changed: %r"
                % (dump_name, {key: (expected_structural[key], structural[key]) for key in structural if expected_structural[key] != structural[key]})
            )
        if broad != EXPECTED_BROAD_HITS[dump_name]:
            raise CandidateError(
                "%s broad census changed: expected %d got %d"
                % (dump_name, EXPECTED_BROAD_HITS[dump_name], broad)
            )
        if strict != EXPECTED_STRICT_HITS[dump_name]:
            raise CandidateError(
                "%s strict census changed: expected %d got %d"
                % (dump_name, EXPECTED_STRICT_HITS[dump_name], strict)
            )
        if any(not decision.rejection_reasons for decision in scan.decisions) != bool(
            EXPECTED_STRICT_HITS[dump_name]
        ):
            raise CandidateError("real-dump acceptance/rejection partition mismatch")
        decisions.extend(scan.decisions)

    if len(decisions) != 134:
        raise CandidateError("combined broad-hit audit must contain 134 decisions")
    if any(not decision.rejection_reasons for decision in decisions):
        raise CandidateError("a real broad hit was unexpectedly promoted")
    tsv, counts = build_tsv(tuple(decisions), existing)
    if counts != {"audit_added": 134, "strict_added": 0, "duplicate": 0}:
        raise CandidateError("unexpected A6 audit deduplication counts: " + repr(counts))
    report = build_markdown(
        decisions=tuple(decisions),
        scans=scans,
        tsv_text=tsv,
        counts=counts,
        extractor_sha256=sha256_file(script_path),
    )
    pinned_after = {path: sha256_file(path) for path in pinned_before}
    dump_hashes_after = {path: sha256_file(path) for path in dump_paths}
    if pinned_before != pinned_after:
        raise CandidateError("immutable V1 A6 input changed during extraction")
    if dump_hashes_before != dump_hashes_after:
        raise CandidateError("pinned dump changed during extraction")
    outputs = {
        args.output_dir / "PF_A6_VTABLE_CANDIDATE_DELTA.tsv": tsv,
        args.output_dir / "PF_A6_VTABLE_CANDIDATE_DELTA.md": report,
    }
    if args.check:
        for path, expected_text in outputs.items():
            if not path.is_file():
                raise CandidateError("check output missing: " + path.name)
            if path.read_text(encoding="utf-8") != expected_text:
                raise CandidateError("check output differs: " + path.name)
    else:
        atomic_publish(outputs)
    print(
        "a6_vtable_audit broad=134 strict=0 audit_added=134 strict_added=0 "
        "duplicate=0 mode=%s" % ("check" if args.check else "publish")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
