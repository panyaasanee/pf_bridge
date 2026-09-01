#!/usr/bin/env python3
"""Build the IMAGE-only serializer-slot correction overlay for Attr classes.

V1 is immutable.  This generator re-derives the complete +0x18/+0x34
capability partition, removes only the affected V1 A2 rows, emits corrected
+0x34 rows, and keeps ItemAttr's two schemas separate.  It never rewrites the
base tables.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import io
import json
import os
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pf_extract_protocol as proto


OUT_DIR = Path(__file__).resolve().parent
PF_ROOT = OUT_DIR.parent.parent
IMAGE_PATH = PF_ROOT / "GameClient" / "GameClient.local.bin"

A1_PATH = OUT_DIR / "PF_PROTOCOL_REGISTRY.tsv"
A2_PATH = OUT_DIR / "PF_SERIALIZER_FIELDS.tsv"
A3_PATH = OUT_DIR / "PF_TAG_CENSUS.tsv"
PRIORITY_PATH = OUT_DIR / "PF_PROTOCOL_PRIORITY.tsv"
STRING_A2_DELTA_PATH = OUT_DIR / "PF_A2_STRING_WIRE_TAG_DELTA.tsv"
STRING_A3_DELTA_PATH = OUT_DIR / "PF_A3_TAG_CENSUS_DELTA.tsv"
POST_V1_PRIORITY_PATH = OUT_DIR / "PF_POST_V1_PRIORITY_DELTA.tsv"
PROTO_PATH = OUT_DIR / "pf_extract_protocol.py"

A1_DELTA_PATH = OUT_DIR / "PF_A1_SERIALIZER_SLOT34_DELTA.tsv"
A2_DELTA_PATH = OUT_DIR / "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
A3_DELTA_PATH = OUT_DIR / "PF_A3_SERIALIZER_SLOT34_DELTA.tsv"
PRIORITY_DELTA_PATH = OUT_DIR / "PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv"
ROOTS_PATH = OUT_DIR / "PF_SERIALIZER_SLOT34_ROOTS.tsv"
REPORT_PATH = OUT_DIR / "PF_SERIALIZER_SLOT34_CORRECTION.md"

PINNED_SHA256 = {
    IMAGE_PATH: "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623",
    A1_PATH: "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d",
    A2_PATH: "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123",
    A3_PATH: "63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a",
    PRIORITY_PATH: "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55",
    STRING_A2_DELTA_PATH: "e1f4f987c31f53d4dd87845aab01857c8415a8dbcd750af12df9c4cde208b3a2",
    STRING_A3_DELTA_PATH: "84f05381d34e81f117fa2c2e6a2bc82afe31932112c055c3ef8de1c8642fef53",
    POST_V1_PRIORITY_PATH: "69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51",
    PROTO_PATH: "0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e",
}

CHANGED_NAMES = frozenset(
    {
        "AvatarAttr", "BasicAttr", "ActorAttr", "NPCAttr", "MovementAttr",
        "DBAttribute", "InstanceRefreshAttr", "BackpackAttr",
        "ItemBagAttr_Equiped", "CollectionBagAttr", "ExpressBagAttr",
        "ItemBagAttr", "ItemVaryAttr", "UnlimitBagAttr", "QuestAttr",
        "QuestMiscAttr", "DailyQuestAttr", "ActorMailData",
        "ActorCommunityProperty", "VowLockData", "CBuffAttr",
        "DailyRewardAttr", "DailyRewardBagAttr", "CGuildStorageAttr",
        "CrystalSlotAttr", "CrystalPlateAttr", "StorageAttr",
        "ActorGatheringInfoAttr", "DailyActivityState", "WinePotAttr",
        "WineCellarAttr", "WineFormulaLearningAttr",
        "CollectableBookTypeAttr", "CollectionPieceAttr", "CollectionBookAttr",
        "ItemMallBagAttr", "ItemMallGiftItem", "CCooldownAttr",
        "CollectionObjPointAttr", "CollectionEffectData", "CVehicleAttr",
        "ActorExpressData", "ExpressCountAttr", "SummonedPetAttr", "PetsData",
        "PetsMergingData", "ActorLearnedPetsSkillData", "CAchievementsAttr",
        "ResidentEffectAttr", "UserSettingServer",
        "ActorTreasureHuntExcavatingInfoAttr", "NavigationExAttr",
        "NPCAppearAttr", "SystemGiftAttr", "CSkillAttr", "StallActorAttr",
    }
)
SAME_TARGET_SLOT_PROVENANCE_NAMES = frozenset({"Attribute", "FightAttr"})
AMBIGUOUS_NAME = "ItemAttr"
CORRECTION_NAMES = CHANGED_NAMES | SAME_TARGET_SLOT_PROVENANCE_NAMES | {AMBIGUOUS_NAME}

EXPECTED_PARTITION = Counter(
    {
        "DIFFERENT_SLOT18_RW_SLOT34_NONE": 343,
        "DIFFERENT_SLOT18_NONE_SLOT34_RW": 56,
        "DIFFERENT_NEITHER": 101,
        "SAME_NEITHER": 2,
    }
)

ITEMATTR_CANDIDATES = (
    (0x00F0EBB0, 0x00B0CFE4, 0x0046BD30),
    (0x00F4A188, 0x00B485BC, 0x00766C90),
)

# These roots legitimately remain OPEN because their primitive tag/length
# arguments are runtime expressions.  The stock V1 analyzer emits the UNKNOWN
# events correctly, then its numeric-only coverage assertion rejects them.  A
# narrowly guarded wrapper below counts those already-emitted sites for coverage
# and immediately restores their UNKNOWN tag; it does not promote a value.
EXPECTED_ANALYSIS_BLOCKERS = frozenset({"VowLockData", "CBuffAttr"})
NONIMMEDIATE_PRIMITIVE_SITES = frozenset(
    {0x00649DE8, 0x0064A32B, 0x0064A342, 0x0064A359, 0x0064A370}
)
EXACT_ADDITIONAL_SPANS = frozenset({0x007206E0})

SLOT34_ANCHOR_SPANS = (
    (
        "generic_attr_carrier", 0x00463DE0, 0x00463FA2,
        "888c2fac20948b7896ed105f46b84e94d01c9442f6535df9be36e6baa2335fc3",
    ),
    (
        "factory_initializer", 0x005F89F0, 0x005F8BDF,
        "72d19d0a6395fcdcf9839982b9788453a5e2e1df223b72e7de722fae00dc5316",
    ),
)

OLD_STRING_TAGS = {
    "UNTAGGED_STRING8_LEN32LE": "0x44",
    "UNTAGGED_WSTRING16LE_LEN32LE": "0x48",
}


A1_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "name",
    "vtable_va", "old_serializer_slot", "old_serializer_va",
    "old_serializer_pointer_file_off", "corrected_serializer_slot",
    "corrected_serializer_va", "corrected_serializer_pointer_file_off",
    "corrected_candidates", "old_slot_capabilities",
    "corrected_slot_capabilities", "classification", "value_changed", "source",
)

A2_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "message",
    "schema_variant", "direction(W/R)", "old_order", "old_tag",
    "old_field_offset", "old_len", "new_order", "new_tag",
    "new_field_offset", "new_len", "new_gate_condition", "new_span_start",
    "new_span_end", "new_span_sha256", "new_file_off_claim", "resolution", "source",
)

A3_COLUMNS = (
    "delta_key", "action", "schema_variant", "count_semantics", "tag",
    "frequency_before", "slot34_increment", "effective_frequency", "lengths",
    "proven_semantics", "example_1", "example_2", "example_3", "source",
)

PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key", "message",
    "priority", "old_registry_identity_status", "new_registry_identity_status",
    "old_registry_identity_missing", "new_registry_identity_missing",
    "old_serializer_status", "new_serializer_status", "old_serializer_blockers",
    "new_serializer_blockers", "old_structural_status",
    "new_structural_status", "old_blocker", "new_blocker", "evidence_ticket",
    "closure_scope", "source",
)

ROOT_COLUMNS = (
    "root_key", "name", "schema_variant", "base_registry_line", "vtable_va",
    "old_serializer_pointer_file_off", "old_serializer_va",
    "corrected_serializer_pointer_file_off", "corrected_serializer_va",
    "span_start", "span_end", "file_off", "length", "span_sha256", "source",
)


class CorrectionError(RuntimeError):
    pass


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_pins(label: str = "input") -> None:
    for path, expected in PINNED_SHA256.items():
        actual = sha256_path(path)
        if actual != expected:
            raise CorrectionError(
                f"{label} hash mismatch for {path.name}: expected {expected}, got {actual}"
            )


def read_tsv_with_lines(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise CorrectionError(f"missing TSV header: {path.name}")
        return list(reader.fieldnames), [
            (line, dict(row)) for line, row in enumerate(reader, start=2)
        ]


def canonical_row_key(fieldnames: Sequence[str], row: Mapping[str, str]) -> str:
    payload = json.dumps(
        [row[name] for name in fieldnames], ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def delta_key(parts: Iterable[str]) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def fmt_va(value: int | None) -> str:
    return "UNKNOWN" if value is None else f"0x{value:08X}"


def format_tsv(columns: Sequence[str], rows: Sequence[Mapping[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=list(columns), delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def atomic_publish(outputs: Mapping[Path, str]) -> None:
    originals = {
        path: path.read_bytes() if path.exists() else None for path in outputs
    }
    staged: dict[Path, Path] = {}
    committed: list[Path] = []
    try:
        for target, text in outputs.items():
            fd, raw = tempfile.mkstemp(
                prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
            )
            temp = Path(raw)
            staged[target] = temp
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
        for target in outputs:
            os.replace(staged.pop(target), target)
            committed.append(target)
    except BaseException as exc:
        for temp in staged.values():
            temp.unlink(missing_ok=True)
        errors: list[str] = []
        for target in reversed(committed):
            try:
                original = originals[target]
                if original is None:
                    target.unlink(missing_ok=True)
                    continue
                fd, raw = tempfile.mkstemp(
                    prefix=f".{target.name}.", suffix=".rollback", dir=target.parent
                )
                temp = Path(raw)
                with os.fdopen(fd, "wb") as handle:
                    handle.write(original)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temp, target)
            except BaseException as rollback_exc:
                errors.append(f"{target.name}:{type(rollback_exc).__name__}")
        if errors:
            raise CorrectionError("rollback incomplete: " + ",".join(errors)) from exc
        raise


def capabilities_text(values: frozenset[str]) -> str:
    return "NONE" if not values else "|".join(sorted(values))


def bounded_entry_span(image: proto.Image, va: int) -> proto.FunctionSpan:
    broad = proto.find_function_span(image, va)
    if broad is None:
        raise CorrectionError(f"unmapped function 0x{va:08X}")
    decoded = proto.decode_function(image, broad)
    if decoded.errors:
        raise CorrectionError(f"decode error in broad span 0x{va:08X}")
    reachable = proto._reachable_nodes(decoded, va)
    if not reachable or va not in reachable:
        raise CorrectionError(f"empty entry CFG 0x{va:08X}")
    end_va = max(decoded.instructions[node].next_va for node in reachable)
    size = end_va - va
    start_off = image.va_range_to_off(va, size)
    if start_off is None:
        raise CorrectionError(f"entry CFG crosses mapped section at 0x{va:08X}")
    body = image.data[start_off : start_off + size]
    return proto.FunctionSpan(
        va, end_va, start_off, start_off + size, hashlib.sha256(body).hexdigest()
    )


class CorrectedAnalyzer(proto.SerializerAnalyzer):
    def __init__(
        self,
        image: proto.Image,
        registry: list[proto.RegistryRow],
        exact_roots: Iterable[int],
    ):
        super().__init__(image, registry)
        roots = frozenset(exact_roots)
        self.root_vas = self.root_vas | roots
        for va in roots:
            self.span_cache[va] = bounded_entry_span(image, va)
        self._coverage_patch_active = False

    @staticmethod
    def _restore_nonimmediate_events(
        events: tuple[proto.WireEvent, ...],
    ) -> tuple[proto.WireEvent, ...]:
        restored = []
        for event in events:
            children = CorrectedAnalyzer._restore_nonimmediate_events(event.children)
            if (
                event.site_va in NONIMMEDIATE_PRIMITIVE_SITES
                and event.tag == "0xFF"
                and event.reason == "primitive_tag_or_len_not_immediate"
            ):
                event = dataclasses.replace(event, tag="UNKNOWN", children=children)
            elif children != event.children:
                event = dataclasses.replace(event, children=children)
            restored.append(event)
        return tuple(restored)

    def extract_events(self, *args: object, **kwargs: object) -> tuple[proto.WireEvent, ...]:
        if self._coverage_patch_active:
            return super().extract_events(*args, **kwargs)
        original_wire_event = proto.WireEvent
        promoted_sites: Counter[int] = Counter()

        def coverage_wire_event(*event_args: object, **event_kwargs: object) -> proto.WireEvent:
            event = original_wire_event(*event_args, **event_kwargs)
            if (
                event.site_va in NONIMMEDIATE_PRIMITIVE_SITES
                and event.tag == "UNKNOWN"
                and event.reason == "primitive_tag_or_len_not_immediate"
            ):
                promoted_sites[event.site_va] += 1
                return dataclasses.replace(event, tag="0xFF")
            return event

        self._coverage_patch_active = True
        proto.WireEvent = coverage_wire_event  # type: ignore[assignment]
        try:
            events = super().extract_events(*args, **kwargs)
        finally:
            proto.WireEvent = original_wire_event
            self._coverage_patch_active = False
        restored = self._restore_nonimmediate_events(events)
        remaining = {
            event.site_va
            for event in self._walk_events(restored)
            if event.tag == "0xFF"
        }
        if remaining:
            raise CorrectionError(
                "coverage-only sentinel leaked at "
                + ",".join(fmt_va(site) for site in sorted(remaining))
            )
        return restored

    @staticmethod
    def _walk_events(
        events: tuple[proto.WireEvent, ...],
    ) -> Iterable[proto.WireEvent]:
        for event in events:
            yield event
            yield from CorrectedAnalyzer._walk_events(event.children)


def executable_slot(image: proto.Image, vtable_va: int, slot: int) -> tuple[int, int]:
    pointer_off = image.va_range_to_off(vtable_va + slot, 4)
    if pointer_off is None:
        raise CorrectionError(
            f"vtable slot outside mapped section: 0x{vtable_va:08X}+0x{slot:X}"
        )
    value = image.u32_off(pointer_off)
    if not image.executable_va(value):
        raise CorrectionError(
            f"non-executable slot: 0x{vtable_va:08X}+0x{slot:X}=0x{value:08X}"
        )
    return value, pointer_off


def readable_slot(image: proto.Image, vtable_va: int, slot: int) -> tuple[int, int]:
    pointer_off = image.va_range_to_off(vtable_va + slot, 4)
    if pointer_off is None:
        raise CorrectionError(
            f"vtable slot outside mapped section: 0x{vtable_va:08X}+0x{slot:X}"
        )
    return image.u32_off(pointer_off), pointer_off


def partition_registry(
    image: proto.Image,
    registry: list[proto.RegistryRow],
    analyzer: proto.SerializerAnalyzer,
) -> tuple[Counter[str], dict[str, tuple[int, int, int, int, frozenset[str], frozenset[str]]]]:
    counts: Counter[str] = Counter()
    measured: dict[
        str, tuple[int, int, int, int, frozenset[str], frozenset[str]]
    ] = {}
    for row in registry:
        if row.vtable_va is None or row.serializer_va is None:
            continue
        old_va, old_off = readable_slot(image, row.vtable_va, 0x18)
        new_va, new_off = readable_slot(image, row.vtable_va, 0x34)
        old_caps = analyzer.capabilities(old_va) if image.executable_va(old_va) else frozenset()
        new_caps = analyzer.capabilities(new_va) if image.executable_va(new_va) else frozenset()
        if old_va == new_va and not old_caps and not new_caps:
            category = "SAME_NEITHER"
        elif old_va != new_va and old_caps == frozenset(("R", "W")) and not new_caps:
            category = "DIFFERENT_SLOT18_RW_SLOT34_NONE"
        elif old_va != new_va and not old_caps and new_caps == frozenset(("R", "W")):
            category = "DIFFERENT_SLOT18_NONE_SLOT34_RW"
        elif old_va != new_va and not old_caps and not new_caps:
            category = "DIFFERENT_NEITHER"
        else:
            raise CorrectionError(
                f"unclassified slot capability shape for {row.name}: "
                f"{fmt_va(old_va)} {old_caps} -> {fmt_va(new_va)} {new_caps}"
            )
        counts[category] += 1
        measured[row.name] = (old_va, old_off, new_va, new_off, old_caps, new_caps)
    if counts != EXPECTED_PARTITION:
        raise CorrectionError(f"whole-registry capability partition changed: {counts}")
    changed = {
        name for name, values in measured.items()
        if not values[4] and values[5] == frozenset(("R", "W"))
    }
    same = {
        name for name, values in measured.items()
        if values[0] == values[2] and not values[4] and not values[5]
    }
    if changed != CHANGED_NAMES or same != SAME_TARGET_SLOT_PROVENANCE_NAMES:
        raise CorrectionError(
            f"slot correction name census changed: changed={sorted(changed ^ CHANGED_NAMES)} "
            f"same={sorted(same ^ SAME_TARGET_SLOT_PROVENANCE_NAMES)}"
        )
    return counts, measured


def verify_slot34_anchor(image: proto.Image) -> None:
    spans: dict[str, proto.FunctionSpan] = {}
    for name, start_va, end_va, expected_hash in SLOT34_ANCHOR_SPANS:
        start_off = image.va_range_to_off(start_va, end_va - start_va)
        if start_off is None:
            raise CorrectionError(f"slot34 anchor unmapped: {name}")
        body = image.data[start_off : start_off + end_va - start_va]
        actual = hashlib.sha256(body).hexdigest()
        if actual != expected_hash:
            raise CorrectionError(f"slot34 anchor hash changed: {name}")
        spans[name] = proto.FunctionSpan(
            start_va, end_va, start_off, start_off + len(body), actual
        )
    carrier = proto.decode_function(image, spans["generic_attr_carrier"])
    if carrier.errors:
        raise CorrectionError("generic Attr carrier decode changed")
    resolver = proto.RegisterResolver(carrier)
    measured_sites = set()
    slot18_sites = set()
    for ins in carrier.instructions.values():
        if ins.kind != "call_indirect" or ins.src is None:
            continue
        target = resolver.operand_before(
            ins.va, ins.src, dereference=(ins.src.kind == "mem")
        )
        if proto.is_proven_vtable_slot_target(target, 0x34):
            if len(proto.recover_call_pushes(carrier, ins.va, 2)) != 1:
                raise CorrectionError(
                    f"slot34 carrier argument paths changed at {fmt_va(ins.va)}"
                )
            measured_sites.add(ins.va)
        if proto.is_proven_vtable_slot_target(target, 0x18):
            slot18_sites.add(ins.va)
    if measured_sites != {0x00463EB7, 0x00463F7E} or slot18_sites:
        raise CorrectionError(
            f"generic Attr carrier slot call census changed: +34={measured_sites} "
            f"+18={slot18_sites}"
        )


def validate_itemattr(
    image: proto.Image, registry_by_name: Mapping[str, proto.RegistryRow]
) -> None:
    row = registry_by_name[AMBIGUOUS_NAME]
    if row.vtable_va is not None or row.serializer_va != 0x0043BB80:
        raise CorrectionError("ItemAttr V1 ambiguity shape changed")
    candidates = proto._vtable_candidates_for_getter(image, row.getter_va)
    got = []
    for vtable_va, _getter_pointer_off in candidates:
        serializer_va, pointer_off = executable_slot(image, vtable_va, 0x34)
        got.append((vtable_va, pointer_off, serializer_va))
    if tuple(got) != ITEMATTR_CANDIDATES:
        raise CorrectionError(f"ItemAttr +0x34 candidate census changed: {got!r}")


def transformed_field(row: proto.FieldRow) -> proto.FieldRow:
    corrected = OLD_STRING_TAGS.get(row.tag)
    if corrected is None:
        return row
    if row.length != "4+N_bytes":
        raise CorrectionError(f"unexpected string helper length in {row.message}")
    return dataclasses.replace(row, tag=corrected, length="5+N_bytes")


def blocker_reasons(rows: Sequence[proto.FieldRow]) -> set[str]:
    reasons: set[str] = set()
    for row in rows:
        if row.reason:
            reasons.add(row.reason)
        elif row.tag == "UNKNOWN" or "UNKNOWN(" in row.field_offset:
            matches = re.findall(r"UNKNOWN\(([^)]+)\)", row.field_offset)
            reasons.update(matches or ("unclassified static field",))
    return reasons


def synthetic_blocker_rows(name: str, reason: str) -> list[proto.FieldRow]:
    return [
        proto.FieldRow(
            message=name,
            direction=direction,
            order=1,
            tag="UNKNOWN",
            field_offset=f"UNKNOWN({reason})",
            length="N/A",
            gate_condition="ALWAYS",
            span_start=None,
            span_end=None,
            span_sha256="UNKNOWN",
            file_off_claim=None,
            reason=reason,
        )
        for direction in ("W", "R")
    ]


def build_corrected_fields(
    image: proto.Image,
    registry: list[proto.RegistryRow],
    measured: Mapping[str, tuple[int, int, int, int, frozenset[str], frozenset[str]]],
) -> tuple[
    dict[str, list[proto.FieldRow]],
    dict[str, dict[str, list[proto.FieldRow]]],
    dict[str, proto.FunctionSpan],
]:
    corrected_registry = [
        dataclasses.replace(row, serializer_va=measured[row.name][2])
        if row.name in CHANGED_NAMES
        else dataclasses.replace(
            row,
            serializer_va=None,
            serializer_pointer_offs=tuple(item[1] for item in ITEMATTR_CANDIDATES),
            reason=(row.reason + ";" if row.reason else "")
            + "serializer_slot34_candidates=2",
        )
        if row.name == AMBIGUOUS_NAME
        else row
        for row in registry
    ]
    exact_roots = {measured[name][2] for name in CHANGED_NAMES}
    exact_roots.update(item[2] for item in ITEMATTR_CANDIDATES)
    analyzer = CorrectedAnalyzer(image, corrected_registry, exact_roots)
    for va in EXACT_ADDITIONAL_SPANS:
        analyzer.span_cache[va] = bounded_entry_span(image, va)
    exact_span_vas = exact_roots | EXACT_ADDITIONAL_SPANS
    spans = {fmt_va(va): analyzer.span(va) for va in sorted(exact_span_vas)}
    singleton: dict[str, list[proto.FieldRow]] = {}
    for name in sorted(CHANGED_NAMES):
        root = measured[name][2]
        events = analyzer.extract_events(root)
        rows = [transformed_field(item) for item in proto.flatten_events(name, events, image)]
        if not rows:
            raise CorrectionError(f"corrected field set is empty for {name}")
        singleton[name] = rows
    observed_blockers = {
        name
        for name, rows in singleton.items()
        if "primitive_tag_or_len_not_immediate" in blocker_reasons(rows)
    }
    if observed_blockers != EXPECTED_ANALYSIS_BLOCKERS:
        raise CorrectionError(
            f"slot34 extraction blocker census changed: {sorted(observed_blockers)}"
        )
    singleton_rows = sum(len(rows) for rows in singleton.values())
    singleton_numeric = sum(
        bool(re.fullmatch(r"0x[0-9A-F]{2}", row.tag))
        for rows in singleton.values()
        for row in rows
    )
    if (singleton_rows, singleton_numeric) != (2138, 890):
        raise CorrectionError(
            "corrected singleton field census changed: "
            f"rows={singleton_rows} numeric={singleton_numeric}"
        )
    normalized_singleton = proto.build_fields_tsv(
        [
            field
            for registry_row in registry
            if registry_row.name in singleton
            for field in singleton[registry_row.name]
        ]
    ).encode("utf-8")
    if (
        len(normalized_singleton),
        hashlib.sha256(normalized_singleton).hexdigest(),
    ) != (
        4_909_953,
        "01cc57dbcf73aef2859eb85e2de47e8d40c4bd32a99b9783a63b53f9e260a06e",
    ):
        raise CorrectionError("normalized corrected singleton oracle changed")

    candidates: dict[str, dict[str, list[proto.FieldRow]]] = {AMBIGUOUS_NAME: {}}
    for vtable_va, _pointer_off, serializer_va in ITEMATTR_CANDIDATES:
        variant = f"VTABLE_{fmt_va(vtable_va)}"
        candidate_registry = [
            dataclasses.replace(
                row,
                serializer_va=serializer_va,
                serializer_pointer_offs=(_pointer_off,),
                reason=(row.reason + ";" if row.reason else "")
                + f"isolated_candidate_vtable={fmt_va(vtable_va)}",
            )
            if row.name == AMBIGUOUS_NAME
            else row
            for row in corrected_registry
        ]
        candidate_analyzer = CorrectedAnalyzer(
            image, candidate_registry, (serializer_va,)
        )
        events = candidate_analyzer.extract_events(serializer_va)
        rows = [
            transformed_field(item)
            for item in proto.flatten_events(AMBIGUOUS_NAME, events, image)
        ]
        if not rows:
            raise CorrectionError(f"ItemAttr candidate field set is empty: {variant}")
        numeric = sum(bool(re.fullmatch(r"0x[0-9A-F]{2}", row.tag)) for row in rows)
        expected = (26, 14) if vtable_va == 0x00F0EBB0 else (30, 16)
        if (len(rows), numeric) != expected:
            raise CorrectionError(
                f"ItemAttr candidate census changed: {variant} "
                f"rows={len(rows)} numeric={numeric}"
            )
        candidate_hash = hashlib.sha256(
            proto.build_fields_tsv(
                [
                    dataclasses.replace(
                        row, message=f"{AMBIGUOUS_NAME}@vtable={fmt_va(vtable_va)}"
                    )
                    for row in rows
                ]
            ).encode("utf-8")
        ).hexdigest()
        expected_hash = (
            "47a662d3f9bc942548b12976d9e82ea255a526f630adaa81645b057f90639664"
            if vtable_va == 0x00F0EBB0
            else "3b4bee5bff50c4d1dd29fc02c4513ab051799b38dc8d0fe5d59e1e105d62b712"
        )
        if candidate_hash != expected_hash:
            raise CorrectionError(
                f"ItemAttr candidate oracle changed: {variant}: {candidate_hash}"
            )
        candidates[AMBIGUOUS_NAME][variant] = rows
    return singleton, candidates, {key: value for key, value in spans.items() if value}


def build_a1_delta(
    a1_fields: Sequence[str],
    a1_rows: Sequence[tuple[int, dict[str, str]]],
    measured: Mapping[str, tuple[int, int, int, int, frozenset[str], frozenset[str]]],
) -> list[dict[str, str]]:
    by_name = {row["name"]: (line, row) for line, row in a1_rows}
    output: list[dict[str, str]] = []
    for name in sorted(CORRECTION_NAMES):
        line, base = by_name[name]
        base_key = canonical_row_key(a1_fields, base)
        if base["source"] != "IMAGE":
            raise CorrectionError(f"non-IMAGE V1 registry row for {name}")
        if name == AMBIGUOUS_NAME:
            action = "CHANGED_TO_AMBIGUOUS"
            vtable = "UNKNOWN"
            old_va = int(base["serializer_va"], 16)
            old_off = base["file_off_serializer_ptr"]
            new_va = None
            new_off = "|".join(fmt_va(item[1]) for item in ITEMATTR_CANDIDATES)
            candidates = "|".join(
                f"vtable={fmt_va(vt)},serializer={fmt_va(ser)},pointer_file_off={fmt_va(off)}"
                for vt, off, ser in ITEMATTR_CANDIDATES
            )
            old_caps = "NONE"
            new_caps = "R|W(each_candidate;not_singleton)"
            classification = "SLOT34_TWO_CANDIDATES_NO_SINGLETON"
            changed = "YES"
        else:
            old_va, old_pointer_off, new_va_value, new_pointer_off, old_cap_set, new_cap_set = measured[name]
            action = (
                "CORRECTED_SLOT_PROVENANCE_SAME_TARGET"
                if name in SAME_TARGET_SLOT_PROVENANCE_NAMES
                else "CHANGED"
            )
            vtable = base["vtable_va"]
            old_off = fmt_va(old_pointer_off)
            new_va = new_va_value
            new_off = fmt_va(new_pointer_off)
            candidates = "N/A"
            old_caps = capabilities_text(old_cap_set)
            new_caps = capabilities_text(new_cap_set)
            classification = (
                "SAME_TARGET_BOTH_NONWIRE"
                if name in SAME_TARGET_SLOT_PROVENANCE_NAMES
                else "SLOT18_NONWIRE_SLOT34_RW"
            )
            changed = "NO" if old_va == new_va_value else "YES"
        row = {
            "delta_key": delta_key(("A1_SLOT34", name, action, base_key)),
            "action": action,
            "base_file": A1_PATH.name,
            "base_line": str(line),
            "base_row_key": base_key,
            "name": name,
            "vtable_va": vtable,
            "old_serializer_slot": "+0x18",
            "old_serializer_va": fmt_va(old_va),
            "old_serializer_pointer_file_off": old_off,
            "corrected_serializer_slot": "+0x34",
            "corrected_serializer_va": fmt_va(new_va),
            "corrected_serializer_pointer_file_off": new_off,
            "corrected_candidates": candidates,
            "old_slot_capabilities": old_caps,
            "corrected_slot_capabilities": new_caps,
            "classification": classification,
            "value_changed": changed,
            "source": "IMAGE",
        }
        output.append(row)
    return output


def build_root_rows(
    image: proto.Image,
    a1_rows: Sequence[tuple[int, dict[str, str]]],
    measured: Mapping[str, tuple[int, int, int, int, frozenset[str], frozenset[str]]],
    spans: Mapping[str, proto.FunctionSpan],
) -> list[dict[str, str]]:
    base_lines = {row["name"]: line for line, row in a1_rows}
    output: list[dict[str, str]] = []
    for name in CHANGED_NAMES:
        old_va, old_off, new_va, new_off, _old_caps, _new_caps = measured[name]
        span = spans[fmt_va(new_va)]
        vtable = next(
            row["vtable_va"] for _line, row in a1_rows if row["name"] == name
        )
        output.append(
            {
                "root_key": delta_key(("SLOT34_ROOT", name, vtable, fmt_va(new_va))),
                "name": name,
                "schema_variant": "SINGLETON_SLOT34",
                "base_registry_line": str(base_lines[name]),
                "vtable_va": vtable,
                "old_serializer_pointer_file_off": fmt_va(old_off),
                "old_serializer_va": fmt_va(old_va),
                "corrected_serializer_pointer_file_off": fmt_va(new_off),
                "corrected_serializer_va": fmt_va(new_va),
                "span_start": fmt_va(span.start_va),
                "span_end": fmt_va(span.end_va),
                "file_off": fmt_va(span.start_off),
                "length": str(span.end_va - span.start_va),
                "span_sha256": span.sha256,
                "source": "IMAGE",
            }
        )
    for vtable_va, new_off, new_va in ITEMATTR_CANDIDATES:
        old_va, old_off = readable_slot(image, vtable_va, 0x18)
        if old_va != 0x0043BB80:
            raise CorrectionError("ItemAttr candidate old slot changed")
        span = spans[fmt_va(new_va)]
        variant = f"VTABLE_{fmt_va(vtable_va)}"
        output.append(
            {
                "root_key": delta_key(
                    ("SLOT34_ROOT", AMBIGUOUS_NAME, variant, fmt_va(new_va))
                ),
                "name": AMBIGUOUS_NAME,
                "schema_variant": variant + ";CANDIDATE_ONLY_NOT_SINGLETON",
                "base_registry_line": str(base_lines[AMBIGUOUS_NAME]),
                "vtable_va": fmt_va(vtable_va),
                "old_serializer_pointer_file_off": fmt_va(old_off),
                "old_serializer_va": fmt_va(old_va),
                "corrected_serializer_pointer_file_off": fmt_va(new_off),
                "corrected_serializer_va": fmt_va(new_va),
                "span_start": fmt_va(span.start_va),
                "span_end": fmt_va(span.end_va),
                "file_off": fmt_va(span.start_off),
                "length": str(span.end_va - span.start_va),
                "span_sha256": span.sha256,
                "source": "IMAGE",
            }
        )
    order = {row["name"]: index for index, (_line, row) in enumerate(a1_rows)}
    output.sort(
        key=lambda row: (
            1 if row["name"] == AMBIGUOUS_NAME else 0,
            order[row["name"]],
            row["vtable_va"],
        )
    )
    if len(output) != 58 or len({row["root_key"] for row in output}) != 58:
        raise CorrectionError("slot34 root manifest census changed")
    oracle_columns = (
        "line", "name", "vtable_va", "old_ptr_off", "old_va", "new_ptr_off",
        "new_va", "span_start", "span_end", "file_off", "length", "sha256",
    )
    oracle_rows = []
    for row in output:
        oracle_name = row["name"]
        if row["name"] == AMBIGUOUS_NAME:
            oracle_name += f"@vtable={row['vtable_va']}"
        oracle_rows.append(
            {
                "line": row["base_registry_line"],
                "name": oracle_name,
                "vtable_va": row["vtable_va"],
                "old_ptr_off": row["old_serializer_pointer_file_off"],
                "old_va": row["old_serializer_va"],
                "new_ptr_off": row["corrected_serializer_pointer_file_off"],
                "new_va": row["corrected_serializer_va"],
                "span_start": row["span_start"],
                "span_end": row["span_end"],
                "file_off": row["file_off"],
                "length": row["length"],
                "sha256": row["span_sha256"],
            }
        )
    oracle = format_tsv(oracle_columns, oracle_rows).encode("utf-8")
    if (
        len(oracle), hashlib.sha256(oracle).hexdigest()
    ) != (
        10_374,
        "530349ddb7e0cc62cfbc58fc3b9991b33982ce062a680fcc6a659233585024ae",
    ):
        raise CorrectionError("exact bounded root oracle changed")
    return output


def new_field_dict(
    action: str,
    field: proto.FieldRow,
    schema_variant: str,
    resolution: str,
) -> dict[str, str]:
    key = delta_key(
        (
            "A2_SLOT34", action, field.message, schema_variant, field.direction,
            str(field.order), field.tag, field.field_offset,
            fmt_va(field.file_off_claim), fmt_va(field.span_start),
        )
    )
    return {
        "delta_key": key,
        "action": action,
        "base_file": "N/A",
        "base_line": "N/A",
        "base_row_key": "N/A",
        "message": field.message,
        "schema_variant": schema_variant,
        "direction(W/R)": field.direction,
        "old_order": "N/A",
        "old_tag": "N/A",
        "old_field_offset": "N/A",
        "old_len": "N/A",
        "new_order": str(field.order),
        "new_tag": field.tag,
        "new_field_offset": field.field_offset,
        "new_len": field.length,
        "new_gate_condition": field.gate_condition,
        "new_span_start": fmt_va(field.span_start),
        "new_span_end": fmt_va(field.span_end),
        "new_span_sha256": field.span_sha256,
        "new_file_off_claim": fmt_va(field.file_off_claim),
        "resolution": resolution,
        "source": "IMAGE",
    }


def build_a2_delta(
    a2_fields: Sequence[str],
    a2_rows: Sequence[tuple[int, dict[str, str]]],
    singleton: Mapping[str, Sequence[proto.FieldRow]],
    candidates: Mapping[str, Mapping[str, Sequence[proto.FieldRow]]],
) -> list[dict[str, str]]:
    replace_names = CHANGED_NAMES | {AMBIGUOUS_NAME}
    output: list[dict[str, str]] = []
    removal_count = 0
    for line, base in a2_rows:
        if base["message"] not in replace_names:
            continue
        if base["source"] != "IMAGE":
            raise CorrectionError(f"non-IMAGE V1 A2 row at {line}")
        base_key = canonical_row_key(a2_fields, base)
        output.append(
            {
                "delta_key": delta_key(("A2_SLOT34_REMOVE", base_key)),
                "action": "REMOVE_WRONG_SLOT_ROW",
                "base_file": A2_PATH.name,
                "base_line": str(line),
                "base_row_key": base_key,
                "message": base["message"],
                "schema_variant": "V1_SLOT18",
                "direction(W/R)": base["direction(W/R)"],
                "old_order": base["order"],
                "old_tag": base["tag"],
                "old_field_offset": base["field_offset"],
                "old_len": base["len"],
                "new_order": "N/A",
                "new_tag": "N/A",
                "new_field_offset": "N/A",
                "new_len": "N/A",
                "new_gate_condition": "N/A",
                "new_span_start": "N/A",
                "new_span_end": "N/A",
                "new_span_sha256": "N/A",
                "new_file_off_claim": "N/A",
                "resolution": "V1_USED_NON_SERIALIZER_SLOT_0x18",
                "source": "IMAGE",
            }
        )
        removal_count += 1
    if removal_count != 114:
        raise CorrectionError(f"V1 A2 slot-removal census changed: {removal_count}")

    for name in sorted(singleton):
        for field in singleton[name]:
            action = (
                "ADD_ANALYSIS_BLOCKER_ROW"
                if name in EXPECTED_ANALYSIS_BLOCKERS
                else "ADD_CORRECTED_SLOT34_ROW"
            )
            output.append(
                new_field_dict(
                    action,
                    field,
                    "SINGLETON_SLOT34",
                    "SLOT34_SINGLETON" if action != "ADD_ANALYSIS_BLOCKER_ROW"
                    else "SLOT34_IDENTITY_KNOWN_ANALYZER_FAIL_CLOSED",
                )
            )
    for name, variants in candidates.items():
        for variant, fields in sorted(variants.items()):
            for field in fields:
                output.append(
                    new_field_dict(
                        "ADD_AMBIGUOUS_CANDIDATE_ROW",
                        field,
                        variant,
                        "CANDIDATE_ONLY_NOT_SINGLETON_DO_NOT_MERGE",
                    )
                )
    return output


def current_a3_frequencies(
    a3_rows: Sequence[tuple[int, dict[str, str]]],
    string_a3_rows: Sequence[tuple[int, dict[str, str]]],
) -> tuple[dict[str, int], dict[str, str]]:
    frequencies: dict[str, int] = {}
    semantics: dict[str, str] = {}
    for _line, row in a3_rows:
        frequencies[row["tag"]] = int(row["frequency_in_A2"])
        semantics[row["tag"]] = row["proven_semantics"]
    for _line, row in string_a3_rows:
        if row["delta_action"] != "ADDED" or row["tag"] in frequencies:
            raise CorrectionError("string A3 delta shape changed")
        frequencies[row["tag"]] = int(row["frequency_in_A2"])
        semantics[row["tag"]] = row["proven_semantics"]
    return frequencies, semantics


def build_a3_delta(
    singleton: Mapping[str, Sequence[proto.FieldRow]],
    candidates: Mapping[str, Mapping[str, Sequence[proto.FieldRow]]],
    frequencies: Mapping[str, int],
    semantics: Mapping[str, str],
) -> list[dict[str, str]]:
    by_tag: dict[str, list[proto.FieldRow]] = defaultdict(list)
    for _name, rows in singleton.items():
        for row in rows:
            if re.fullmatch(r"0x[0-9A-F]{2}", row.tag):
                by_tag[row.tag].append(row)
    output: list[dict[str, str]] = []
    for tag, rows in sorted(by_tag.items()):
        before = frequencies.get(tag, 0)
        examples = [
            f"{row.message}:{row.direction}:{row.order}@file_off={fmt_va(row.file_off_claim)}"
            for row in rows[:3]
        ]
        output.append(
            {
                "delta_key": delta_key(("A3_SLOT34", tag, str(len(rows)))),
                "action": "CHANGED_FREQUENCY" if tag in frequencies else "ADDED",
                "schema_variant": "SINGLETON_56",
                "count_semantics": "ADD_TO_EFFECTIVE_BASE",
                "tag": tag,
                "frequency_before": str(before),
                "slot34_increment": str(len(rows)),
                "effective_frequency": str(before + len(rows)),
                "lengths": "|".join(sorted({row.length for row in rows})),
                "proven_semantics": semantics.get(tag, "UNKNOWN"),
                "example_1": examples[0] if examples else "N/A",
                "example_2": examples[1] if len(examples) > 1 else "N/A",
                "example_3": examples[2] if len(examples) > 2 else "N/A",
                "source": "IMAGE",
            }
        )
    singleton_effective = {
        row["tag"]: int(row["effective_frequency"]) for row in output
    }
    singleton_effective.update(
        {
            tag: count
            for tag, count in frequencies.items()
            if tag not in singleton_effective
        }
    )
    for _name, variants in candidates.items():
        for variant, fields in sorted(variants.items()):
            variant_tags: dict[str, list[proto.FieldRow]] = defaultdict(list)
            for field in fields:
                if re.fullmatch(r"0x[0-9A-F]{2}", field.tag):
                    variant_tags[field.tag].append(field)
            for tag, rows in sorted(variant_tags.items()):
                before = singleton_effective.get(tag, frequencies.get(tag, 0))
                examples = [
                    f"{row.message}:{row.direction}:{row.order}@file_off={fmt_va(row.file_off_claim)}"
                    for row in rows[:3]
                ]
                output.append(
                    {
                        "delta_key": delta_key(
                            ("A3_SLOT34_CANDIDATE", variant, tag, str(len(rows)))
                        ),
                        "action": "CANDIDATE_ALTERNATIVE",
                        "schema_variant": variant,
                        "count_semantics": "DO_NOT_ADD_TO_SINGLETON;ALTERNATIVE_ONLY",
                        "tag": tag,
                        "frequency_before": str(before),
                        "slot34_increment": str(len(rows)),
                        "effective_frequency": str(before + len(rows)),
                        "lengths": "|".join(sorted({row.length for row in rows})),
                        "proven_semantics": semantics.get(tag, "UNKNOWN"),
                        "example_1": examples[0] if examples else "N/A",
                        "example_2": examples[1] if len(examples) > 1 else "N/A",
                        "example_3": examples[2] if len(examples) > 2 else "N/A",
                        "source": "IMAGE",
                    }
                )
    return output


def build_priority_delta(
    priority_fields: Sequence[str],
    priority_rows: Sequence[tuple[int, dict[str, str]]],
    singleton: Mapping[str, Sequence[proto.FieldRow]],
    candidates: Mapping[str, Mapping[str, Sequence[proto.FieldRow]]],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    by_name = {row["message"]: (line, row) for line, row in priority_rows}
    for name in sorted(CHANGED_NAMES | {AMBIGUOUS_NAME}):
        line, base = by_name[name]
        if name == AMBIGUOUS_NAME:
            candidate_reason_sets = {
                variant: blocker_reasons(rows)
                for variant, rows in candidates[AMBIGUOUS_NAME].items()
            }
            measured_sets = list(candidate_reason_sets.values())
            if not measured_sets or any(item != measured_sets[0] for item in measured_sets[1:]):
                raise CorrectionError(
                    "ItemAttr candidate blocker sets diverged; keep them explicit"
                )
            expected_item_blockers = {
                "atomic_target_object_alias_unproved",
                "direct_call_not_proven_serializer",
                "dynamic_vtable_plus_0x04_target_unresolved",
                "indirect_call_not_proven_serializer_slot",
                "indirect_serializer_direction_unresolved",
            }
            if measured_sets[0] != expected_item_blockers:
                raise CorrectionError("ItemAttr candidate blocker census changed")
            reasons = measured_sets[0] | {"registry_serializer_slot34_ambiguous"}
        else:
            reasons = blocker_reasons(singleton[name])
        identity_missing = (
            ["vtable", "serializer"] if name == AMBIGUOUS_NAME else []
        )
        new_registry_status = "OPEN" if identity_missing else "KNOWN"
        new_registry_missing = " | ".join(identity_missing) if identity_missing else "N/A"
        new_serializer = "OPEN" if reasons else "CLOSED"
        new_serializer_blockers = " | ".join(sorted(reasons)) if reasons else "N/A"
        combined = [f"registry {item} UNKNOWN" for item in identity_missing] + sorted(reasons)
        new_structural = "OPEN" if combined else "CLOSED"
        new_blocker = " | ".join(combined) if combined else "N/A"
        changed = (
            base["registry_identity_status"] != new_registry_status
            or base["registry_identity_missing"] != new_registry_missing
            or base["serializer_status"] != new_serializer
            or base["serializer_blockers"] != new_serializer_blockers
            or base["structural_status"] != new_structural
            or base["blocker"] != new_blocker
        )
        if not changed:
            continue
        base_key = canonical_row_key(priority_fields, base)
        output.append(
            {
                "delta_key": delta_key(("PRIORITY_SLOT34", name, base_key)),
                "action": "CHANGED",
                "base_file": PRIORITY_PATH.name,
                "base_line": str(line),
                "base_row_key": base_key,
                "message": name,
                "priority": base["priority"],
                "old_registry_identity_status": base["registry_identity_status"],
                "new_registry_identity_status": new_registry_status,
                "old_registry_identity_missing": base["registry_identity_missing"],
                "new_registry_identity_missing": new_registry_missing,
                "old_serializer_status": base["serializer_status"],
                "new_serializer_status": new_serializer,
                "old_serializer_blockers": base["serializer_blockers"],
                "new_serializer_blockers": new_serializer_blockers,
                "old_structural_status": base["structural_status"],
                "new_structural_status": new_structural,
                "old_blocker": base["blocker"],
                "new_blocker": new_blocker,
                "evidence_ticket": "SLOT34-CORRECTION",
                "closure_scope": "STATIC_WIRE_STRUCTURE_ONLY;V1_IMMUTABLE",
                "source": "IMAGE",
            }
        )
    return output


def validate_deltas(
    a1: Sequence[Mapping[str, str]],
    a2: Sequence[Mapping[str, str]],
    a3: Sequence[Mapping[str, str]],
    priority: Sequence[Mapping[str, str]],
    roots: Sequence[Mapping[str, str]],
    post_v1_priority_rows: Sequence[tuple[int, dict[str, str]]],
) -> None:
    if len(a1) != 59:
        raise CorrectionError(f"A1 correction census changed: {len(a1)}")
    if Counter(row["action"] for row in a1) != Counter(
        {
            "CHANGED": 56,
            "CORRECTED_SLOT_PROVENANCE_SAME_TARGET": 2,
            "CHANGED_TO_AMBIGUOUS": 1,
        }
    ):
        raise CorrectionError("A1 action census changed")
    if Counter(row["action"] for row in a2)["REMOVE_WRONG_SLOT_ROW"] != 114:
        raise CorrectionError("A2 removal census changed")
    if Counter(row["action"] for row in a2) != Counter(
        {
            "REMOVE_WRONG_SLOT_ROW": 114,
            "ADD_CORRECTED_SLOT34_ROW": 2059,
            "ADD_ANALYSIS_BLOCKER_ROW": 79,
            "ADD_AMBIGUOUS_CANDIDATE_ROW": 56,
        }
    ):
        raise CorrectionError("A2 action census changed")
    if Counter(
        row["old_tag"]
        for row in a2
        if row["action"] == "REMOVE_WRONG_SLOT_ROW"
    ) != Counter({"EMPTY": 96, "CALL_UNCLASSIFIED:0x0046D7A0": 18}):
        raise CorrectionError("A2 removed-slot row shape changed")
    if Counter(row["action"] for row in a3) != Counter(
        {"CHANGED_FREQUENCY": 12, "CANDIDATE_ALTERNATIVE": 11}
    ):
        raise CorrectionError("A3 singleton/candidate action census changed")
    if len(priority) != 37 or any(row["action"] != "CHANGED" for row in priority):
        raise CorrectionError("priority correction census changed")
    for rows in (a1, a2, a3, priority, roots):
        if any(row["source"] != "IMAGE" for row in rows):
            raise CorrectionError("non-IMAGE row in slot correction")
        key_name = "root_key" if rows is roots else "delta_key"
        keys = [row[key_name] for row in rows]
        if len(keys) != len(set(keys)):
            raise CorrectionError("duplicate delta key in slot correction")
        if any(row.get("action") in {"UNCHANGED", "COPIED"} for row in rows):
            raise CorrectionError("unchanged/copied output is forbidden")
    removal_keys = [
        row["base_row_key"] for row in a2 if row["action"] == "REMOVE_WRONG_SLOT_ROW"
    ]
    if len(removal_keys) != len(set(removal_keys)):
        raise CorrectionError("duplicate A2 base removal key")
    old_semantics = {
        (
            row["message"], row["direction(W/R)"], row["old_tag"],
            row["old_field_offset"], row["old_len"],
        )
        for row in a2
        if row["action"] == "REMOVE_WRONG_SLOT_ROW"
    }
    new_semantics = {
        (
            row["message"], row["direction(W/R)"], row["new_tag"],
            row["new_field_offset"], row["new_len"],
        )
        for row in a2
        if row["action"] != "REMOVE_WRONG_SLOT_ROW"
    }
    if old_semantics & new_semantics:
        raise CorrectionError("A2 correction copied an old slot semantic row")
    post_messages = {row["message"] for _line, row in post_v1_priority_rows}
    overlap = post_messages & {row["message"] for row in priority}
    if overlap:
        raise CorrectionError(f"post-V1 priority overlay overlap: {sorted(overlap)}")


def report_text(
    partition: Counter[str],
    a1: Sequence[Mapping[str, str]],
    a2: Sequence[Mapping[str, str]],
    a3: Sequence[Mapping[str, str]],
    priority: Sequence[Mapping[str, str]],
    roots: Sequence[Mapping[str, str]],
    singleton: Mapping[str, Sequence[proto.FieldRow]],
) -> str:
    p1_changes = [row for row in priority if row["priority"] == "1"]
    p1_closed_to_open = [
        row for row in p1_changes
        if row["old_structural_status"] == "CLOSED"
        and row["new_structural_status"] == "OPEN"
    ]
    priority_rows = [
        f"| `{row['message']}` | `{row['old_serializer_status']}/{row['old_structural_status']}` | "
        f"`{row['new_serializer_status']}/{row['new_structural_status']}` | `{row['new_blocker']}` |"
        for row in p1_changes
    ]
    action_counts = Counter(row["action"] for row in a2)
    lines = [
        "# PF serializer slot +0x34 correction",
        "",
        "[MEASURED] IMAGE-only additive correction. Frozen V1 remains untouched.",
        "",
        "## Result",
        "",
        "The V1 registry treated vtable `+0x18` as the serializer slot for every registration. "
        "The whole 502-row known-vtable census proves a second family: 56 rows have no W/R "
        "capability at `+0x18` and both W/R capabilities at `+0x34`.",
        "",
        f"- A1 slot-provenance corrections: {len(a1)} (56 changed targets, 2 same-target provenance corrections, 1 ambiguous ItemAttr).",
        f"- Exact bounded serializer roots: {len(roots)} (56 singleton rows plus 2 isolated ItemAttr candidates).",
        f"- A2 directives: {len(a2)}; " + ", ".join(f"{key}={value}" for key, value in sorted(action_counts.items())),
        f"- A3 frequency rows: {len(a3)}; ambiguous ItemAttr candidates are separate alternatives and are excluded from singleton frequencies.",
        f"- Priority rows changed: {len(priority)}; P1 CLOSED->OPEN corrections: {len(p1_closed_to_open)}.",
        "- Unchanged rows copied as new output: 0. Exact duplicate delta keys: 0. "
        "Old-slot/new-slot semantic-row overlap: 0.",
        "",
        "## Whole-registry capability partition",
        "",
        *[f"- `{name}`: {count}" for name, count in sorted(partition.items())],
        "",
        "The slot identity is anchored by the generic Attr carrier "
        "`[0x00463DE0,0x00463FA2)` (sha256 "
        "`888c2fac20948b7896ed105f46b84e94d01c9442f6535df9be36e6baa2335fc3`), "
        "which has exactly two vtable `+0x34` indirect call sites with one recovered "
        "two-argument path each and no vtable `+0x18` call. The factory initializer "
        "`[0x005F89F0,0x005F8BDF)` is pinned at sha256 "
        "`72d19d0a6395fcdcf9839982b9788453a5e2e1df223b72e7de722fae00dc5316`.",
        "",
        "## Priority-1 truth corrections",
        "",
        "| message | old serializer/structural | corrected serializer/structural | corrected blocker |",
        "|---|---|---|---|",
        *priority_rows,
        "",
        "`ItemAttr` has two exact +0x34 candidates and therefore remains OPEN. Its candidate schemas "
        "are kept in separate `schema_variant` rows and are never merged into one asserted table.",
        "",
        "## Fail-closed analysis boundary",
        "",
        *[
            f"- `{name}`: `{ ' | '.join(sorted(blocker_reasons(singleton[name]))) }`"
            for name in sorted(EXPECTED_ANALYSIS_BLOCKERS)
        ],
        "",
        "## Evidence boundary",
        "",
        "- Every TSV row is `source=IMAGE`; no DUMP, CAPTURE, or DATA fact is mixed in.",
        "- No raw dump/capture byte is emitted.",
        "- A1 describes identity and slot provenance; A2 describes wire structure; candidate-only "
        "rows are not singleton facts and do not contribute to A3 or closure counts.",
        "- The two same-target rows correct slot provenance only. They are not counted as newly "
        "discovered values.",
        "",
        "## Reproduction",
        "",
        "Run `py -3 pf_build_serializer_slot34_correction.py --check`. It pins every input, "
        "re-derives the full capability partition and bounded entry CFGs, verifies base-row keys, "
        "and compares every output byte-for-byte.",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    verify_pins()
    image = proto.Image(IMAGE_PATH)
    registry = proto.scan_registry(image)
    if len(registry) != 519:
        raise CorrectionError(f"registry census changed: {len(registry)}")
    proto.validate_registry_acceptance(image, registry)
    verify_slot34_anchor(image)
    registry_by_name = {row.name: row for row in registry}
    validate_itemattr(image, registry_by_name)
    base_analyzer = proto.SerializerAnalyzer(image, registry)
    partition, measured = partition_registry(image, registry, base_analyzer)

    singleton, candidates, spans = build_corrected_fields(
        image, registry, measured
    )
    a1_fields, a1_rows = read_tsv_with_lines(A1_PATH)
    a2_fields, a2_rows = read_tsv_with_lines(A2_PATH)
    a3_fields, a3_rows = read_tsv_with_lines(A3_PATH)
    priority_fields, priority_rows = read_tsv_with_lines(PRIORITY_PATH)
    _string_a3_fields, string_a3_rows = read_tsv_with_lines(STRING_A3_DELTA_PATH)
    _post_fields, post_rows = read_tsv_with_lines(POST_V1_PRIORITY_PATH)

    a1_delta = build_a1_delta(a1_fields, a1_rows, measured)
    root_rows = build_root_rows(image, a1_rows, measured, spans)
    a2_delta = build_a2_delta(a2_fields, a2_rows, singleton, candidates)
    frequencies, semantics = current_a3_frequencies(a3_rows, string_a3_rows)
    a3_delta = build_a3_delta(singleton, candidates, frequencies, semantics)
    priority_delta = build_priority_delta(
        priority_fields, priority_rows, singleton, candidates
    )
    validate_deltas(
        a1_delta, a2_delta, a3_delta, priority_delta, root_rows, post_rows
    )

    outputs = {
        A1_DELTA_PATH: format_tsv(A1_COLUMNS, a1_delta),
        A2_DELTA_PATH: format_tsv(A2_COLUMNS, a2_delta),
        A3_DELTA_PATH: format_tsv(A3_COLUMNS, a3_delta),
        PRIORITY_DELTA_PATH: format_tsv(PRIORITY_COLUMNS, priority_delta),
        ROOTS_PATH: format_tsv(ROOT_COLUMNS, root_rows),
        REPORT_PATH: report_text(
            partition, a1_delta, a2_delta, a3_delta, priority_delta, root_rows, singleton
        ),
    }
    verify_pins("prepublish")
    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                raise CorrectionError(f"check mismatch: {path.name}")
        print(
            "check ok: A1=%d A2=%d A3=%d Priority=%d"
            % (len(a1_delta), len(a2_delta), len(a3_delta), len(priority_delta))
        )
        return 0
    atomic_publish(outputs)
    print(
        "wrote: A1=%d A2=%d A3=%d Priority=%d"
        % (len(a1_delta), len(a2_delta), len(a3_delta), len(priority_delta))
    )
    for path in outputs:
        print(f"{path.name} {sha256_path(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
