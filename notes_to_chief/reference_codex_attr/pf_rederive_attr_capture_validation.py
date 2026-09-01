#!/usr/bin/env python3
"""Re-derive the ActorAttr/CSkillAttr A5 CAPTURE validation delta.

This program reads the pinned GameClient image, the pinned A2 comparator inputs,
and the baseline plus 2026-08-30 CAPTURE inventories.  It writes only aggregate
counts, mismatch field ordinals, paths, and SHA-256 provenance.  It never emits
capture payload values, raw bytes, or hexdumps.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Iterable


sys.dont_write_bytecode = True

SOURCE = "CAPTURE"
REPORT_VERSION = "PF_ATTR_FIELD_VALIDATION_DELTA_V1"
EXPECTED_IMAGE_SIZE = 14_759_424
EXPECTED_IMAGE_SHA256 = (
    "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
)

EXPECTED_SUPPORT_HASHES = {
    "PF_INPUT_INVENTORY.tsv": (
        "729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1"
    ),
    "PF_CAPTURE_DELTA_20260830.inventory.tsv": (
        "8a85dd1fff3d608ef0f0777331f9235152d2353e67adc76f4ae6275f8bfe6a3e"
    ),
    "PF_A2_SERIALIZER_SLOT34_DELTA.tsv": (
        "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334"
    ),
    "PF_A2_ACTOR_CODEC_CORRECTION.tsv": (
        "db705474aeb4e66050d67f28f14acb85b6a0a5fa9def86baadfc9f02ba07ec29"
    ),
    "PF_A2_BASIC_CODEC_CORRECTION.tsv": (
        "b0313135b57ff36637158361734ed4bd1f16d59bdda84384b92b02258ee8edec"
    ),
    "pf_extract_capture_branch_shapes_20260830.py": (
        "423bc4aa64f800dc53da729a0e4320198dc149d9d0837debaf8e5feb46b4e498"
    ),
    "pf_validate_capture_fields.py": (
        "0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8"
    ),
}

EXPECTED_IMAGE_SPANS = {
    "BasicAttr_corrected_codec": (
        0x00064AF0,
        0x00064D83,
        "d0c15b74a36077df30a0e60dbeb8441e878c08b82587c1ea55365ab2ebd70020",
    ),
    "ActorAttr_codec": (
        0x00065630,
        0x00066079,
        "f9ea39f3a6bc80e6d29d4aae3efa79c1d5ff855d70109319578cba86d5f9aabc",
    ),
    "CSkillAttr_codec": (
        0x003514B0,
        0x00351681,
        "9227cc6009fff2f20c79a3b19c395f9623d87f68a4ee3462e541aed62aa7e906",
    ),
}

# Filled with the measured immutable-inventory census after the first complete
# derivation.  These checks are deliberately aggregate-only.
EXPECTED_METRICS = {
    "ActorAttr.baseline_physical": 69,
    "ActorAttr.delta_physical": 266,
    "ActorAttr.combined_physical": 335,
    "ActorAttr.delta_claim_unique": 201,
    "ActorAttr.mismatches": 0,
    "CSkillAttr.combined_physical": 10,
    "CSkillAttr.baseline_physical": 0,
    "CSkillAttr.delta_physical": 10,
    "CSkillAttr.delta_claim_unique": 2,
    "CSkillAttr.mismatches": 0,
    "ActorAttr.baseline_observed_orders": 19,
    "ActorAttr.delta_claim_unique_observed_orders": 60,
    "CSkillAttr.delta_claim_unique_observed_orders": 6,
    "CSkillAttr.combined_record_count_zero": 5,
    "CSkillAttr.combined_record_count_nonzero": 5,
    "CSkillAttr.delta_claim_unique_record_count_zero": 1,
    "CSkillAttr.delta_claim_unique_record_count_nonzero": 1,
}

EXPECTED_UNREGISTERED_FILES = 24
# Filled after the first metadata-only enumeration.  The unregistered files are
# not parsed and never contribute to accepted validation counts.
EXPECTED_UNREGISTERED_MANIFEST = (
    "46acdeebec044cdeee21a7f3d2c234b2d2f4038d1ac6788df5b52889ae97de4a"
)

UPDATE_ATTR_ID = sum(
    (index + 1) * ord(character)
    for index, character in enumerate("UpdateAttrVital")
) & 0xFFFF
ACTOR_ATTR_ID = sum(
    (index + 1) * ord(character)
    for index, character in enumerate("ActorAttr")
) & 0xFFFF
CSKILL_ATTR_ID = sum(
    (index + 1) * ord(character)
    for index, character in enumerate("CSkillAttr")
) & 0xFFFF

FIXED_WIDTHS = {
    0x05: 1,
    0x0B: 1,
    0x12: 2,
    0x14: 4,
    0x19: 4,
    0x26: 4,
    0x2A: 4,
    0x32: 8,
}
STRING_TAGS = {0x44, 0x48}
RAW_BYTE_RUN_RE = re.compile(
    r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"
)


class ValidationError(RuntimeError):
    pass


@dataclass(frozen=True)
class PrimitiveSpec:
    order: int
    tag: int
    offset: int
    length_label: str
    mask_word: str = "ALWAYS"
    mask_bit: int = 0
    nested_gate: bool = False

    @property
    def field_key(self) -> str:
        suffix = ""
        if self.mask_word != "ALWAYS":
            suffix = f":b0x{self.mask_bit:08X}"
        return (
            f"ActorAttr@0x{self.offset:X}.{self.length_label}#R{suffix}"
        )


@dataclass(frozen=True)
class ParseResult:
    status: str
    end: int
    observed_orders: frozenset[int]
    mismatch_order: str = ""
    mismatch_reason: str = ""
    record_count_zero: bool | None = None


@dataclass(frozen=True)
class ClassObservation:
    class_name: str
    direction: str
    population: str
    dedup_class: str
    relative_path: str
    capture_file_sha256: str
    block_ordinal: int
    block_sha256: str
    entry_ordinal: int
    entry_payload_sha256: str
    result: ParseResult


@dataclass(frozen=True)
class WrapperIssue:
    direction: str
    population: str
    dedup_class: str
    relative_path: str
    capture_file_sha256: str
    block_ordinal: int
    block_sha256: str
    mismatch_order: str
    mismatch_reason: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().lower()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tsv_text(headers: list[str], rows: list[list[str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return stream.getvalue()


def load_module(path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValidationError(f"could not load helper: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def verify_lock(lock_path: Path) -> str:
    if not lock_path.is_file():
        raise ValidationError("LOCK_GAME.txt missing")
    first_line = lock_path.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    if first_line.lstrip("\ufeff").startswith("HELD"):
        raise ValidationError("LOCK_GAME is HELD; whole-capture scan refused")
    if not first_line.lstrip("\ufeff").startswith("RELEASED"):
        raise ValidationError("LOCK_GAME has an unrecognized first line")
    return first_line.lstrip("\ufeff")


def verify_support_hashes(external: Path) -> dict[str, str]:
    actual: dict[str, str] = {}
    for name, expected in EXPECTED_SUPPORT_HASHES.items():
        path = external / name
        digest = sha256_file(path)
        if digest != expected:
            raise ValidationError(f"pinned supporting input changed: {name}")
        actual[name] = digest
    return actual


def verify_image(image_path: Path) -> tuple[str, dict[str, str]]:
    stat = image_path.stat()
    digest = sha256_file(image_path)
    if stat.st_size != EXPECTED_IMAGE_SIZE:
        raise ValidationError("GameClient.local.bin size changed")
    if digest != EXPECTED_IMAGE_SHA256:
        raise ValidationError("GameClient.local.bin SHA-256 changed")
    image = image_path.read_bytes()
    spans: dict[str, str] = {}
    for name, (start, end, expected) in EXPECTED_IMAGE_SPANS.items():
        actual = sha256_bytes(image[start:end])
        if actual != expected:
            raise ValidationError(f"pinned IMAGE span changed: {name}")
        spans[name] = actual
    return digest, spans


def actor_specs() -> tuple[PrimitiveSpec, ...]:
    specs = [
        PrimitiveSpec(3, 0x0B, 0x20, "1"),
        PrimitiveSpec(4, 0x32, 0x18, "8"),
        PrimitiveSpec(5, 0x12, 0x70, "2"),
    ]
    basic_fields = (
        (6, 0x48, 0x28, "var", 0x00000001),
        (7, 0x12, 0x5E, "2", 0x00000002),
        (8, 0x14, 0x44, "4", 0x00000004),
        (9, 0x14, 0x48, "4", 0x00000008),
        (10, 0x14, 0x4C, "4", 0x00000010),
        (11, 0x14, 0x50, "4", 0x00000020),
        (12, 0x2A, 0x54, "4", 0x00000040),
        (13, 0x2A, 0x58, "4", 0x00000080),
        (14, 0x12, 0x5C, "2", 0x00000100),
        (15, 0x32, 0x60, "8", 0x00000200),
        (16, 0x14, 0x68, "4", 0x00000400),
        (17, 0x14, 0x6C, "4", 0x00000800),
    )
    specs.extend(
        PrimitiveSpec(order, tag, offset, length, "BASIC", mask)
        for order, tag, offset, length, mask in basic_fields
    )
    specs.extend(
        (
            PrimitiveSpec(18, 0x32, 0x1B4, "8"),
            PrimitiveSpec(19, 0x05, 0x1BC, "1"),
        )
    )
    low_fields = (
        (20, 0x19, 0x8C, "4", 0x00000001, False),
        (21, 0x19, 0x90, "4", 0x00000002, False),
        (22, 0x26, 0x78, "4", 0x00000004, True),
        (23, 0x19, 0x7C, "4", 0x00000008, True),
        (24, 0x12, 0x80, "2", 0x00000010, True),
        (25, 0x12, 0x82, "2", 0x00000020, True),
        (26, 0x12, 0x84, "2", 0x00000040, True),
        (27, 0x12, 0x86, "2", 0x00000080, True),
        (28, 0x12, 0x88, "2", 0x00000100, True),
        (29, 0x12, 0x8A, "2", 0x00000200, True),
        (30, 0x32, 0xA0, "8", 0x00000400, True),
        (31, 0x32, 0xA8, "8", 0x00000800, True),
        (32, 0x48, 0xB0, "var", 0x00001000, True),
        (33, 0x0B, 0x99, "1", 0x00002000, True),
        (34, 0x0B, 0x9A, "1", 0x00004000, True),
        (35, 0x12, 0x13E, "2", 0x00008000, True),
        (36, 0x12, 0x13C, "2", 0x00010000, True),
        (37, 0x44, 0x148, "var", 0x00020000, True),
        (38, 0x12, 0x182, "2", 0x00040000, True),
        (39, 0x12, 0x184, "2", 0x00080000, True),
        (40, 0x12, 0x186, "2", 0x00100000, True),
        (41, 0x12, 0x188, "2", 0x00200000, True),
        (42, 0x12, 0x18A, "2", 0x00400000, True),
        (43, 0x0B, 0x18C, "1", 0x00800000, True),
        (44, 0x48, 0x164, "var", 0x01000000, False),
        (45, 0x0B, 0x180, "1", 0x02000000, False),
        (46, 0x0B, 0x98, "1", 0x04000000, False),
        (47, 0x19, 0x94, "4", 0x04000000, False),
        (48, 0x32, 0x140, "8", 0x08000000, False),
        (49, 0x0B, 0x9B, "1", 0x08000000, False),
        (50, 0x48, 0xCC, "var", 0x10000000, True),
        (51, 0x32, 0x198, "8", 0x20000000, False),
        (52, 0x32, 0x190, "8", 0x40000000, False),
    )
    specs.extend(
        PrimitiveSpec(order, tag, offset, length, "ACTOR_LOW", mask, nested)
        for order, tag, offset, length, mask, nested in low_fields
    )
    high_fields = (
        (53, 0x0B, 0x1A0, "1", 0x00000001, False),
        (54, 0x12, 0x1A2, "2", 0x00000002, False),
        (55, 0x12, 0x1A4, "2", 0x00000004, False),
        (56, 0x48, 0xE8, "var", 0x00000008, False),
        (57, 0x48, 0x104, "var", 0x00000010, False),
        (58, 0x48, 0x120, "var", 0x00000020, False),
        (59, 0x14, 0x1A8, "4", 0x00000040, False),
        (60, 0x14, 0x1AC, "4", 0x00000080, False),
        (61, 0x12, 0x1B0, "2", 0x00000100, True),
        (62, 0x0B, 0x1B2, "1", 0x00000200, True),
    )
    specs.extend(
        PrimitiveSpec(order, tag, offset, length, "ACTOR_HIGH", mask, nested)
        for order, tag, offset, length, mask, nested in high_fields
    )
    result = tuple(specs)
    if tuple(spec.order for spec in result) != tuple(range(3, 63)):
        raise ValidationError("internal ActorAttr order is not contiguous")
    return result


ACTOR_SPECS = actor_specs()
ACTOR_SPEC_BY_ORDER = {spec.order: spec for spec in ACTOR_SPECS}


def verify_schema_inputs(external: Path) -> None:
    rows = read_tsv(external / "PF_A2_SERIALIZER_SLOT34_DELTA.tsv")
    actor_rows = {
        int(row["new_order"]): row
        for row in rows
        if row["action"] == "ADD_CORRECTED_SLOT34_ROW"
        and row["message"] == "ActorAttr"
        and row["direction(W/R)"] == "R"
        and row["new_order"].isdigit()
        and 3 <= int(row["new_order"]) <= 62
    }
    if set(actor_rows) != set(range(3, 63)):
        raise ValidationError("A2 ActorAttr primitive-order census changed")
    for spec in ACTOR_SPECS:
        row = actor_rows[spec.order]
        expected_tag = f"0x{spec.tag:02X}"
        if row["new_tag"] != expected_tag:
            raise ValidationError(f"A2 ActorAttr tag changed at order {spec.order}")
        if spec.order == 18:
            if row["new_len"] != "8":
                raise ValidationError("A2 ActorAttr mask width changed")
        else:
            expected_offset = f"+0x{spec.offset:X}"
            if row["new_field_offset"] != expected_offset:
                raise ValidationError(
                    f"A2 ActorAttr offset changed at order {spec.order}"
                )

    basic_corrections = read_tsv(external / "PF_A2_BASIC_CODEC_CORRECTION.tsv")
    basic_r = {
        int(row["offset"], 16): int(row["mask_bit"], 16)
        for row in basic_corrections
        if row["direction"] == "R"
    }
    if basic_r != {
        0x5C: 0x00000100,
        0x60: 0x00000200,
        0x68: 0x00000400,
        0x6C: 0x00000800,
    }:
        raise ValidationError("BasicAttr high-mask correction set changed")

    actor_corrections = read_tsv(external / "PF_A2_ACTOR_CODEC_CORRECTION.tsv")
    expected_nested = set(range(22, 44)) | {50, 61, 62}
    for direction in ("R", "W"):
        nested_orders = {
            int(row["composed_order"])
            for row in actor_corrections
            if row["direction"] == direction
            and "NESTED_GROUP_GATE" in row["delta_action"]
        }
        if nested_orders != expected_nested:
            raise ValidationError(
                f"ActorAttr nested-gate correction set changed for {direction}"
            )
        mask_storage = [
            row
            for row in actor_corrections
            if row["direction"] == direction
            and row["delta_action"] == "CORRECT_MASK_STORAGE_LOCATION"
        ]
        if len(mask_storage) != 1 or mask_storage[0]["composed_order"] != "18":
            raise ValidationError(
                f"ActorAttr mask-storage correction changed for {direction}"
            )


def load_pinned_inputs(
    root: Path,
    external: Path,
    helper: ModuleType,
) -> tuple[list[object], list[object], list[object], list[object]]:
    """Load only the two frozen manifests and enumerate later files as metadata.

    The upstream helper deliberately fail-closes when new files appear.  A5 must
    retain the frozen checkpoint counts, so later files are hashed and reported
    as an explicit inventory blocker but their text/payload is never opened by
    the parser.
    """

    baseline_rows = [
        row
        for row in read_tsv(external / "PF_INPUT_INVENTORY.tsv")
        if row.get("source") == SOURCE
    ]
    delta_rows = read_tsv(
        external / "PF_CAPTURE_DELTA_20260830.inventory.tsv"
    )
    if len(baseline_rows) != helper.EXPECTED_CAPTURE_INVENTORY_FILES:
        raise ValidationError("baseline CAPTURE inventory count changed")
    if sum(int(row["size"]) for row in baseline_rows) != helper.EXPECTED_CAPTURE_INVENTORY_BYTES:
        raise ValidationError("baseline CAPTURE inventory byte count changed")
    if len(delta_rows) != helper.EXPECTED_DELTA_FILES:
        raise ValidationError("delta CAPTURE inventory count changed")
    if sum(int(row["size"]) for row in delta_rows) != helper.EXPECTED_DELTA_BYTES:
        raise ValidationError("delta CAPTURE inventory byte count changed")

    fresh = helper.enumerate_capture_paths(root)

    def materialize(rows: list[dict[str, str]]) -> list[object]:
        result: list[object] = []
        seen: set[str] = set()
        for row in rows:
            relative_path = row["relative_path"]
            key = relative_path.casefold()
            if key in seen:
                raise ValidationError(
                    f"duplicate path in pinned inventory: {relative_path}"
                )
            seen.add(key)
            path = fresh.get(key)
            if path is None:
                raise ValidationError(
                    f"pinned CAPTURE input missing: {relative_path}"
                )
            result.append(
                helper.CaptureInput(
                    relative_path=relative_path,
                    path=path,
                    size=int(row["size"]),
                    sha256=row["sha256"].lower(),
                )
            )
        return result

    baseline_all = materialize(baseline_rows)
    delta_all = materialize(delta_rows)
    baseline_keys = {item.relative_path.casefold() for item in baseline_all}
    delta_keys = {item.relative_path.casefold() for item in delta_all}
    if baseline_keys & delta_keys:
        raise ValidationError("baseline/delta pinned path overlap")

    baseline_text = [
        item for item in baseline_all if item.path.suffix.casefold() == ".txt"
    ]
    delta_text = [
        item for item in delta_all if item.path.suffix.casefold() == ".txt"
    ]
    if len(baseline_text) != helper.EXPECTED_BASELINE_TEXT_FILES:
        raise ValidationError("baseline text-file count changed")
    if sum(item.size for item in baseline_text) != helper.EXPECTED_BASELINE_TEXT_BYTES:
        raise ValidationError("baseline text byte count changed")
    if helper.manifest_sha256(baseline_text) != helper.EXPECTED_BASELINE_TEXT_MANIFEST:
        raise ValidationError("baseline text manifest changed")
    if helper.manifest_sha256(delta_all) != helper.EXPECTED_DELTA_MANIFEST:
        raise ValidationError("delta all-file manifest changed")
    if len(delta_text) != helper.EXPECTED_DELTA_TEXT_FILES:
        raise ValidationError("delta text-file count changed")
    if sum(item.size for item in delta_text) != helper.EXPECTED_DELTA_TEXT_BYTES:
        raise ValidationError("delta text byte count changed")
    if helper.manifest_sha256(delta_text) != helper.EXPECTED_DELTA_TEXT_MANIFEST:
        raise ValidationError("delta text manifest changed")

    registered = baseline_keys | delta_keys
    unregistered: list[object] = []
    for key in sorted(set(fresh) - registered):
        path = fresh[key]
        relative_path = path.relative_to(root).as_posix()
        unregistered.append(
            helper.CaptureInput(
                relative_path=relative_path,
                path=path,
                size=path.stat().st_size,
                sha256=sha256_file(path),
            )
        )
    if len(unregistered) != EXPECTED_UNREGISTERED_FILES:
        raise ValidationError(
            f"unregistered CAPTURE file count changed: {len(unregistered)}"
        )
    unregistered_manifest = helper.manifest_sha256(unregistered)
    if EXPECTED_UNREGISTERED_MANIFEST and unregistered_manifest != EXPECTED_UNREGISTERED_MANIFEST:
        raise ValidationError(
            "unregistered CAPTURE manifest changed: " + unregistered_manifest
        )
    return baseline_text, delta_all, delta_text, unregistered


def consume_primitive(
    data: bytes,
    position: int,
    tag: int,
    order: str,
) -> tuple[int, int | None, str, str]:
    if position >= len(data):
        return position, None, order, "TRUNCATED_TAG"
    if data[position] != tag:
        return position, None, order, "TAG"
    if tag in FIXED_WIDTHS:
        width = FIXED_WIDTHS[tag]
        end = position + 1 + width
        if end > len(data):
            return position, None, order, "TRUNCATED_VALUE"
        value = int.from_bytes(data[position + 1 : end], "little")
        return end, value, "", ""
    if tag in STRING_TAGS:
        if position + 5 > len(data):
            return position, None, order, "TRUNCATED_STRING_LENGTH"
        byte_length = int.from_bytes(data[position + 1 : position + 5], "little")
        end = position + 5 + byte_length
        if end > len(data):
            return position, None, order, "TRUNCATED_STRING_PAYLOAD"
        return end, None, "", ""
    raise ValidationError(f"unsupported primitive tag 0x{tag:02X}")


def parse_actor(payload: bytes) -> ParseResult:
    position = 0
    observed: set[int] = set()

    for order in (3, 4):
        spec = ACTOR_SPEC_BY_ORDER[order]
        position, _value, mismatch_order, reason = consume_primitive(
            payload, position, spec.tag, str(order)
        )
        if reason:
            return ParseResult(
                "MISMATCH", position, frozenset(observed), mismatch_order, reason
            )
        observed.add(order)

    basic_mask_spec = ACTOR_SPEC_BY_ORDER[5]
    position, basic_mask, mismatch_order, reason = consume_primitive(
        payload, position, basic_mask_spec.tag, "5"
    )
    if reason or basic_mask is None:
        return ParseResult(
            "MISMATCH", position, frozenset(observed), mismatch_order, reason
        )
    observed.add(5)

    for order in range(6, 18):
        spec = ACTOR_SPEC_BY_ORDER[order]
        if not basic_mask & spec.mask_bit:
            continue
        position, _value, mismatch_order, reason = consume_primitive(
            payload, position, spec.tag, str(order)
        )
        if reason:
            return ParseResult(
                "MISMATCH", position, frozenset(observed), mismatch_order, reason
            )
        observed.add(order)

    actor_mask_spec = ACTOR_SPEC_BY_ORDER[18]
    position, actor_mask, mismatch_order, reason = consume_primitive(
        payload, position, actor_mask_spec.tag, "18"
    )
    if reason or actor_mask is None:
        return ParseResult(
            "MISMATCH", position, frozenset(observed), mismatch_order, reason
        )
    observed.add(18)

    group_gate_spec = ACTOR_SPEC_BY_ORDER[19]
    position, group_gate, mismatch_order, reason = consume_primitive(
        payload, position, group_gate_spec.tag, "19"
    )
    if reason or group_gate is None:
        return ParseResult(
            "MISMATCH", position, frozenset(observed), mismatch_order, reason
        )
    observed.add(19)

    actor_low = actor_mask & 0xFFFFFFFF
    actor_high = (actor_mask >> 32) & 0xFFFFFFFF
    for order in range(20, 63):
        spec = ACTOR_SPEC_BY_ORDER[order]
        mask = actor_low if spec.mask_word == "ACTOR_LOW" else actor_high
        if not mask & spec.mask_bit:
            continue
        if spec.nested_gate and group_gate == 0:
            continue
        position, _value, mismatch_order, reason = consume_primitive(
            payload, position, spec.tag, str(order)
        )
        if reason:
            return ParseResult(
                "MISMATCH", position, frozenset(observed), mismatch_order, reason
            )
        observed.add(order)

    if position != len(payload):
        return ParseResult(
            "MISMATCH",
            position,
            frozenset(observed),
            "END",
            "TRAILING_BYTES",
        )
    return ParseResult("MATCH", position, frozenset(observed))


def parse_cskill(payload: bytes) -> ParseResult:
    position = 0
    observed: set[int] = set()
    prefix = ((1, 0x0B), (2, 0x32), (3, 0x12))
    values: dict[int, int | None] = {}
    for order, tag in prefix:
        position, value, mismatch_order, reason = consume_primitive(
            payload, position, tag, str(order)
        )
        if reason:
            return ParseResult(
                "MISMATCH", position, frozenset(observed), mismatch_order, reason
            )
        observed.add(order)
        values[order] = value
    record_count = values[3]
    if record_count is None:
        raise ValidationError("CSkillAttr record count was not decoded")
    if record_count > len(payload):
        return ParseResult(
            "MISMATCH",
            position,
            frozenset(observed),
            "3",
            "COUNT_EXCEEDS_REMAINING_BYTES",
            False,
        )
    for _record_index in range(record_count):
        for order, tag in ((4, 0x12), (5, 0x12), (6, 0x14)):
            position, _value, mismatch_order, reason = consume_primitive(
                payload, position, tag, str(order)
            )
            if reason:
                return ParseResult(
                    "MISMATCH",
                    position,
                    frozenset(observed),
                    mismatch_order,
                    reason,
                    record_count == 0,
                )
            observed.add(order)
    if position != len(payload):
        return ParseResult(
            "MISMATCH",
            position,
            frozenset(observed),
            "END",
            "TRAILING_BYTES",
            record_count == 0,
        )
    return ParseResult(
        "MATCH",
        position,
        frozenset(observed),
        record_count_zero=(record_count == 0),
    )


def parse_update_region(
    region: bytes,
    direction: str,
    population: str,
    dedup_class: str,
    relative_path: str,
    capture_file_sha256: str,
    block_ordinal: int,
    block_sha256: str,
) -> tuple[list[ClassObservation], WrapperIssue | None]:
    position, count, mismatch_order, reason = consume_primitive(
        region, 0, 0x12, "wrapper.count"
    )
    if reason or count is None:
        return [], WrapperIssue(
            direction,
            population,
            dedup_class,
            relative_path,
            capture_file_sha256,
            block_ordinal,
            block_sha256,
            mismatch_order,
            reason,
        )
    observations: list[ClassObservation] = []
    for entry_ordinal in range(1, count + 1):
        position, type_id, mismatch_order, reason = consume_primitive(
            region, position, 0x12, f"wrapper.entry_{entry_ordinal}.type"
        )
        if reason or type_id is None:
            return observations, WrapperIssue(
                direction,
                population,
                dedup_class,
                relative_path,
                capture_file_sha256,
                block_ordinal,
                block_sha256,
                mismatch_order,
                reason,
            )
        position, payload_length, mismatch_order, reason = consume_primitive(
            region, position, 0x14, f"wrapper.entry_{entry_ordinal}.length"
        )
        if reason or payload_length is None:
            return observations, WrapperIssue(
                direction,
                population,
                dedup_class,
                relative_path,
                capture_file_sha256,
                block_ordinal,
                block_sha256,
                mismatch_order,
                reason,
            )
        end = position + payload_length
        if end > len(region):
            return observations, WrapperIssue(
                direction,
                population,
                dedup_class,
                relative_path,
                capture_file_sha256,
                block_ordinal,
                block_sha256,
                f"wrapper.entry_{entry_ordinal}.payload",
                "TRUNCATED_PAYLOAD",
            )
        payload = region[position:end]
        position = end
        if type_id == ACTOR_ATTR_ID:
            class_name = "ActorAttr"
            result = parse_actor(payload)
        elif type_id == CSKILL_ATTR_ID:
            class_name = "CSkillAttr"
            result = parse_cskill(payload)
        else:
            continue
        observations.append(
            ClassObservation(
                class_name=class_name,
                direction=direction,
                population=population,
                dedup_class=dedup_class,
                relative_path=relative_path,
                capture_file_sha256=capture_file_sha256,
                block_ordinal=block_ordinal,
                block_sha256=block_sha256,
                entry_ordinal=entry_ordinal,
                entry_payload_sha256=sha256_bytes(payload),
                result=result,
            )
        )
    if position != len(region):
        return observations, WrapperIssue(
            direction,
            population,
            dedup_class,
            relative_path,
            capture_file_sha256,
            block_ordinal,
            block_sha256,
            "wrapper.end",
            "TRAILING_BYTES",
        )
    return observations, None


def evidence_manifest(observations: Iterable[ClassObservation]) -> str:
    digest = hashlib.sha256()
    for item in sorted(
        observations,
        key=lambda value: (
            value.relative_path,
            value.block_ordinal,
            value.entry_ordinal,
        ),
    ):
        fields = (
            item.class_name,
            item.direction,
            item.relative_path,
            item.capture_file_sha256,
            str(item.block_ordinal),
            item.block_sha256,
            str(item.entry_ordinal),
            item.entry_payload_sha256,
            item.result.status,
            item.result.mismatch_order,
            item.result.mismatch_reason,
        )
        digest.update("\0".join(fields).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest().lower()


def scan_inputs(
    baseline_text: list[object],
    delta_text: list[object],
    helper: ModuleType,
    validator: ModuleType,
) -> tuple[list[ClassObservation], list[WrapperIssue], dict[str, int]]:
    baseline_content_keys: set[str] = set()
    observations: list[ClassObservation] = []
    issues: list[WrapperIssue] = []
    block_counts: Counter[str] = Counter()
    strict_counts: Counter[str] = Counter()

    for item in baseline_text:
        text = item.path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = validator.extract_pc_blocks(text)
        if errors:
            raise ValidationError(
                f"baseline block extraction errors: {dict(errors)}"
            )
        for ordinal, (kind, data) in enumerate(blocks, 1):
            block_counts[f"baseline.{kind}"] += 1
            key = helper.content_key(kind, data)
            baseline_content_keys.add(key)
            branch = helper.strict_branch(
                kind,
                data,
                item.relative_path,
                item.sha256,
                ordinal,
                key,
                "BASELINE_PHYSICAL",
                {UPDATE_ATTR_ID},
            )
            if branch is None:
                continue
            strict_counts["baseline"] += 1
            parsed, issue = parse_update_region(
                data[branch.region_offset : branch.tail_offset],
                branch.direction,
                "BASELINE_PHYSICAL",
                "BASELINE_PHYSICAL",
                item.relative_path,
                item.sha256,
                ordinal,
                branch.block_sha256,
            )
            observations.extend(parsed)
            if issue is not None:
                issues.append(issue)

    delta_seen_new_keys: set[str] = set()
    for item in delta_text:
        text = item.path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = validator.extract_pc_blocks(text)
        if errors:
            raise ValidationError(f"delta block extraction errors: {dict(errors)}")
        for ordinal, (kind, data) in enumerate(blocks, 1):
            block_counts[f"delta.{kind}"] += 1
            key = helper.content_key(kind, data)
            if key in baseline_content_keys:
                dedup_class = "DUPLICATE_BASELINE"
            elif key in delta_seen_new_keys:
                dedup_class = "DUPLICATE_DELTA"
            else:
                dedup_class = "CLAIM_UNIQUE"
                delta_seen_new_keys.add(key)
            branch = helper.strict_branch(
                kind,
                data,
                item.relative_path,
                item.sha256,
                ordinal,
                key,
                dedup_class,
                {UPDATE_ATTR_ID},
            )
            if branch is None:
                continue
            strict_counts["delta"] += 1
            parsed, issue = parse_update_region(
                data[branch.region_offset : branch.tail_offset],
                branch.direction,
                "DELTA_PHYSICAL",
                dedup_class,
                item.relative_path,
                item.sha256,
                ordinal,
                branch.block_sha256,
            )
            observations.extend(parsed)
            if issue is not None:
                issues.append(issue)

    metrics = dict(block_counts)
    metrics.update({f"strict.{key}": value for key, value in strict_counts.items()})
    return observations, issues, metrics


def population_observations(
    all_observations: list[ClassObservation],
    class_name: str,
    population: str,
) -> list[ClassObservation]:
    matching = [item for item in all_observations if item.class_name == class_name]
    if population == "BASELINE_PHYSICAL":
        return [item for item in matching if item.population == population]
    if population == "DELTA_PHYSICAL":
        return [item for item in matching if item.population == population]
    if population == "COMBINED_PHYSICAL":
        return matching
    if population == "DELTA_CLAIM_UNIQUE":
        return [
            item
            for item in matching
            if item.population == "DELTA_PHYSICAL"
            and item.dedup_class == "CLAIM_UNIQUE"
        ]
    raise ValidationError(f"unknown population {population}")


def stable_key(*parts: str) -> str:
    digest = hashlib.sha256()
    digest.update(REPORT_VERSION.encode("ascii"))
    for part in parts:
        digest.update(b"\0")
        digest.update(part.encode("utf-8"))
    return digest.hexdigest().lower()


def build_outputs(
    observations: list[ClassObservation],
    wrapper_issues: list[WrapperIssue],
    unregistered: list[object],
    scan_metrics: dict[str, int],
    support_hashes: dict[str, str],
    span_hashes: dict[str, str],
    image_sha256: str,
    helper: ModuleType,
) -> tuple[str, str, dict[str, int]]:
    populations = (
        "BASELINE_PHYSICAL",
        "DELTA_PHYSICAL",
        "COMBINED_PHYSICAL",
        "DELTA_CLAIM_UNIQUE",
    )
    class_schema_orders = {
        "ActorAttr": set(range(3, 63)),
        "CSkillAttr": set(range(1, 7)),
    }
    headers = [
        "validation_key",
        "row_kind",
        "schema_class",
        "direction(W/R)",
        "population",
        "observed_instances",
        "matched_instances",
        "mismatched_instances",
        "schema_primitive_orders",
        "observed_primitive_orders",
        "unobserved_primitive_orders",
        "mismatch_field_order",
        "mismatch_reason",
        "mismatch_point_instances",
        "record_count_zero_instances",
        "record_count_nonzero_instances",
        "duplicate_rejected_baseline",
        "duplicate_rejected_delta",
        "capture_file_count",
        "evidence_manifest_sha256",
        "first_evidence_relative_path",
        "first_capture_file_sha256",
        "first_block_ordinal",
        "dedup_policy",
        "comparator_basis",
        "source",
    ]
    rows: list[list[str]] = []
    metrics: dict[str, int] = {}
    markdown_rows: list[str] = []

    for class_name in ("ActorAttr", "CSkillAttr"):
        all_class = [item for item in observations if item.class_name == class_name]
        directions = sorted({item.direction for item in all_class}) or ["R"]
        for direction in directions:
            direction_items = [item for item in all_class if item.direction == direction]
            for population in populations:
                selected = population_observations(
                    direction_items, class_name, population
                )
                matched = [item for item in selected if item.result.status == "MATCH"]
                mismatched = [
                    item for item in selected if item.result.status == "MISMATCH"
                ]
                observed_orders = set().union(
                    *(item.result.observed_orders for item in selected)
                ) if selected else set()
                schema_orders = class_schema_orders[class_name]
                unobserved = sorted(schema_orders - observed_orders)
                zero_records = sum(
                    item.result.record_count_zero is True for item in selected
                )
                nonzero_records = sum(
                    item.result.record_count_zero is False for item in selected
                )
                rejected_baseline = sum(
                    item.dedup_class == "DUPLICATE_BASELINE"
                    for item in selected
                )
                rejected_delta = sum(
                    item.dedup_class == "DUPLICATE_DELTA" for item in selected
                )
                evidence = sorted(
                    selected,
                    key=lambda value: (
                        value.relative_path,
                        value.block_ordinal,
                        value.entry_ordinal,
                    ),
                )
                first = evidence[0] if evidence else None
                comparator = (
                    "PF_A2_SERIALIZER_SLOT34_DELTA.tsv+"
                    "PF_A2_BASIC_CODEC_CORRECTION.tsv+"
                    "PF_A2_ACTOR_CODEC_CORRECTION.tsv"
                    if class_name == "ActorAttr"
                    else "CSkillAttr IMAGE codec span"
                )
                summary_key = stable_key(
                    "SUMMARY", class_name, direction, population
                )
                rows.append(
                    [
                        summary_key,
                        "SUMMARY",
                        class_name,
                        direction,
                        population,
                        str(len(selected)),
                        str(len(matched)),
                        str(len(mismatched)),
                        str(len(schema_orders)),
                        str(len(observed_orders)),
                        ",".join(str(value) for value in unobserved),
                        "",
                        "",
                        "0",
                        str(zero_records) if class_name == "CSkillAttr" else "",
                        str(nonzero_records) if class_name == "CSkillAttr" else "",
                        str(rejected_baseline),
                        str(rejected_delta),
                        str(len({item.relative_path for item in selected})),
                        evidence_manifest(selected),
                        first.relative_path if first else "",
                        first.capture_file_sha256 if first else "",
                        str(first.block_ordinal) if first else "",
                        (
                            "physical_keeps_repeats"
                            if population != "DELTA_CLAIM_UNIQUE"
                            else "whole_block_sha256_reject_baseline_then_prior_delta"
                        ),
                        comparator,
                        SOURCE,
                    ]
                )
                point_counts = Counter(
                    (item.result.mismatch_order, item.result.mismatch_reason)
                    for item in mismatched
                )
                for (field_order, reason), point_count in sorted(point_counts.items()):
                    point_items = [
                        item
                        for item in mismatched
                        if item.result.mismatch_order == field_order
                        and item.result.mismatch_reason == reason
                    ]
                    first_point = sorted(
                        point_items,
                        key=lambda value: (
                            value.relative_path,
                            value.block_ordinal,
                            value.entry_ordinal,
                        ),
                    )[0]
                    rows.append(
                        [
                            stable_key(
                                "MISMATCH",
                                class_name,
                                direction,
                                population,
                                field_order,
                                reason,
                            ),
                            "MISMATCH",
                            class_name,
                            direction,
                            population,
                            "",
                            "",
                            "",
                            str(len(schema_orders)),
                            "",
                            "",
                            field_order,
                            reason,
                            str(point_count),
                            "",
                            "",
                            "",
                            "",
                            str(len({item.relative_path for item in point_items})),
                            evidence_manifest(point_items),
                            first_point.relative_path,
                            first_point.capture_file_sha256,
                            str(first_point.block_ordinal),
                            "same_as_parent_summary_row",
                            comparator,
                            SOURCE,
                        ]
                    )
                markdown_rows.append(
                    "| {0} | {1} | {2} | {3} | {4} | {5}/{6} |".format(
                        class_name,
                        direction,
                        population,
                        len(selected),
                        len(mismatched),
                        len(observed_orders),
                        len(schema_orders),
                    )
                )

            baseline = population_observations(
                direction_items, class_name, "BASELINE_PHYSICAL"
            )
            delta = population_observations(
                direction_items, class_name, "DELTA_PHYSICAL"
            )
            combined = population_observations(
                direction_items, class_name, "COMBINED_PHYSICAL"
            )
            claim_unique = population_observations(
                direction_items, class_name, "DELTA_CLAIM_UNIQUE"
            )
            metrics[f"{class_name}.baseline_physical"] = len(baseline)
            metrics[f"{class_name}.delta_physical"] = len(delta)
            metrics[f"{class_name}.combined_physical"] = len(combined)
            metrics[f"{class_name}.delta_claim_unique"] = len(claim_unique)
            metrics[f"{class_name}.mismatches"] = sum(
                item.result.status == "MISMATCH" for item in combined
            )
            if class_name == "ActorAttr":
                metrics["ActorAttr.baseline_observed_orders"] = len(
                    set().union(
                        *(item.result.observed_orders for item in baseline)
                    ) if baseline else set()
                )
                metrics["ActorAttr.delta_claim_unique_observed_orders"] = len(
                    set().union(
                        *(item.result.observed_orders for item in claim_unique)
                    ) if claim_unique else set()
                )
            else:
                metrics["CSkillAttr.delta_claim_unique_observed_orders"] = len(
                    set().union(
                        *(item.result.observed_orders for item in claim_unique)
                    ) if claim_unique else set()
                )
                metrics["CSkillAttr.combined_record_count_zero"] = sum(
                    item.result.record_count_zero is True for item in combined
                )
                metrics["CSkillAttr.combined_record_count_nonzero"] = sum(
                    item.result.record_count_zero is False for item in combined
                )
                metrics[
                    "CSkillAttr.delta_claim_unique_record_count_zero"
                ] = sum(
                    item.result.record_count_zero is True for item in claim_unique
                )
                metrics[
                    "CSkillAttr.delta_claim_unique_record_count_nonzero"
                ] = sum(
                    item.result.record_count_zero is False for item in claim_unique
                )

    unregistered_manifest = helper.manifest_sha256(unregistered)
    first_unregistered = sorted(
        unregistered,
        key=lambda value: (value.relative_path.casefold(), value.relative_path),
    )[0]
    rows.append(
        [
            stable_key("INVENTORY_BLOCKER", unregistered_manifest),
            "INVENTORY_BLOCKER",
            "UNREGISTERED_INPUTS",
            "",
            "EXCLUDED_UNREGISTERED",
            str(len(unregistered)),
            "",
            "",
            "",
            "",
            "",
            "",
            "NOT_IN_PINNED_MANIFESTS",
            "",
            "",
            "",
            "",
            "",
            str(len(unregistered)),
            unregistered_manifest,
            first_unregistered.relative_path,
            first_unregistered.sha256,
            "",
            "metadata_only_not_parsed",
            "outside both accepted pinned inventories",
            SOURCE,
        ]
    )

    metrics["wrapper_mismatches"] = len(wrapper_issues)
    metrics["unregistered_excluded_files"] = len(unregistered)
    metrics.update(scan_metrics)
    for key, expected in EXPECTED_METRICS.items():
        actual = metrics.get(key)
        if actual != expected:
            raise ValidationError(
                f"immutable CAPTURE metric changed: {key}={actual} expected={expected}"
            )
    if metrics["wrapper_mismatches"] != 0:
        raise ValidationError("UpdateAttr wrapper mismatch requires explicit publication")

    output_tsv = tsv_text(headers, rows)
    total_mismatches = sum(
        value
        for key, value in metrics.items()
        if key.endswith(".mismatches")
    ) + metrics["wrapper_mismatches"]
    heading = (
        f"# ALERT: {total_mismatches} static-versus-CAPTURE mismatches\n"
        if total_mismatches
        else "# PF Attr field validation delta\n"
    )
    support_lines = "\n".join(
        f"- `{name}` SHA-256 `{digest}`"
        for name, digest in sorted(support_hashes.items())
    )
    span_lines = "\n".join(
        f"- `{name}` SHA-256 `{digest}`"
        for name, digest in sorted(span_hashes.items())
    )
    unregistered_lines = "\n".join(
        f"- `{item.relative_path}` size `{item.size}` SHA-256 `{item.sha256}`"
        for item in sorted(
            unregistered,
            key=lambda value: (
                value.relative_path.casefold(),
                value.relative_path,
            ),
        )
    )
    output_md = f"""{heading}
[MEASURED] Offline read-only A5 validation.  All result rows have
`source=CAPTURE`; IMAGE/A2 material is only the comparator and is not copied as
a CAPTURE fact.

## Result

| schema | dir | population | instances | mismatches | observed primitive orders |
|---|---:|---|---:|---:|---:|
{chr(10).join(markdown_rows)}

- UpdateAttr wrapper mismatches: `{metrics['wrapper_mismatches']}`.
- ActorAttr corrected Basic high-mask gates are applied at composed orders
  `14-17`.
- ActorAttr corrected nested `+0x1BC` gate is applied at composed orders
  `22-43`, `50`, `61`, and `62`.
- ActorAttr mask storage is treated as the paired object fields at `+0x1B4`
  and `+0x1B8`, never as the old stack-temporary claim.
- CSkillAttr is parsed as its inherited DBAttribute prefix, one record-count
  primitive, and repeated three-primitive records.

## Physical versus claim-unique

`BASELINE_PHYSICAL`, `DELTA_PHYSICAL`, and `COMBINED_PHYSICAL` retain repeated
frames.  `DELTA_CLAIM_UNIQUE` hashes the entire decompressed/PC block, rejects
anything already present in the baseline, then rejects later duplicates in the
delta.  The two populations are kept separate; claim-unique counts do not
replace physical validation counts.

Baseline text census: `{helper.EXPECTED_BASELINE_TEXT_FILES}` files / `{helper.EXPECTED_BASELINE_TEXT_BYTES}` bytes; manifest `{helper.EXPECTED_BASELINE_TEXT_MANIFEST}`.

Delta text census: `{helper.EXPECTED_DELTA_TEXT_FILES}` files / `{helper.EXPECTED_DELTA_TEXT_BYTES}` bytes; manifest `{helper.EXPECTED_DELTA_TEXT_MANIFEST}`.

## Current-inventory blocker

Exactly `{len(unregistered)}` files currently under `capture_*` are absent from
both pinned manifests.  They are excluded from every accepted validation count.
This run reads only their filesystem metadata and SHA-256; it does not open their
text through the packet parser.  Combined metadata manifest:
`{unregistered_manifest}`.

{unregistered_lines}

## Comparator boundary

- `GameClient.local.bin` SHA-256 `{image_sha256}`.
{span_lines}

Comparator/supporting files pinned before and after the scan:

{support_lines}

## Proprietary-data boundary

No raw CAPTURE byte, payload value, or hexdump is emitted.  The TSV contains
only structural counts, mismatch field ordinals/reasons, relative provenance
paths, and SHA-256 identifiers.  File and block hashes are provenance, not
payload publication.

## Reproduction

Run `py -3 pf_rederive_attr_capture_validation.py --check`.  The script refuses
to scan while `LOCK_GAME.txt` is HELD, pins the image and every comparator, takes
before/after snapshots of all baseline and delta inputs, and requires
byte-identical outputs.
"""
    return output_tsv, output_md, metrics


def validate_output(output_tsv: str, output_md: str) -> None:
    if RAW_BYTE_RUN_RE.search(output_tsv) or RAW_BYTE_RUN_RE.search(output_md):
        raise ValidationError("raw byte run detected in output")
    parsed = list(csv.DictReader(io.StringIO(output_tsv), delimiter="\t"))
    if not parsed:
        raise ValidationError("empty validation TSV")
    keys = [row["validation_key"] for row in parsed]
    if len(keys) != len(set(keys)):
        raise ValidationError("duplicate validation_key")
    if {row["source"] for row in parsed} != {SOURCE}:
        raise ValidationError("mixed or missing source in validation TSV")
    for row in parsed:
        forbidden = (
            "payload_value",
            "raw_bytes",
            "hexdump",
        )
        if any(term in row for term in forbidden):
            raise ValidationError("forbidden payload column in output")


def atomic_publish(outputs: dict[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, content in outputs.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(
                prefix=f".{destination.name}.",
                suffix=".tmp",
                dir=destination.parent,
            )
            temp = Path(temp_name)
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            staged.append((temp, destination))
        for temp, destination in staged:
            os.replace(temp, destination)
    finally:
        for temp, _destination in staged:
            if temp.exists():
                temp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game-client",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "GameClient",
    )
    parser.add_argument(
        "--external",
        type=Path,
        default=Path(__file__).resolve().parent,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="derive again and require byte-identical existing outputs",
    )
    args = parser.parse_args()
    root = args.game_client.resolve()
    external = args.external.resolve()
    lock_path = external.parent / "LOCK_GAME.txt"
    image_path = root / "GameClient.local.bin"

    lock_state = verify_lock(lock_path)
    support_before = verify_support_hashes(external)
    image_before, span_hashes_before = verify_image(image_path)
    verify_schema_inputs(external)

    helper = load_module(
        external / "pf_extract_capture_branch_shapes_20260830.py",
        "pf_attr_capture_helper_20260831",
    )
    validator = helper.load_validator(external / "pf_validate_capture_fields.py")
    baseline_text, delta_all, delta_text, unregistered = load_pinned_inputs(
        root, external, helper
    )
    baseline_snapshot_before = helper.snapshot_inputs(baseline_text)
    delta_snapshot_before = helper.snapshot_inputs(delta_all)
    unregistered_snapshot_before = helper.snapshot_inputs(unregistered)

    observations, wrapper_issues, scan_metrics = scan_inputs(
        baseline_text, delta_text, helper, validator
    )
    output_tsv, output_md, metrics = build_outputs(
        observations,
        wrapper_issues,
        unregistered,
        scan_metrics,
        support_before,
        span_hashes_before,
        image_before,
        helper,
    )
    validate_output(output_tsv, output_md)

    if helper.snapshot_inputs(baseline_text) != baseline_snapshot_before:
        raise ValidationError("baseline CAPTURE inputs changed during scan")
    if helper.snapshot_inputs(delta_all) != delta_snapshot_before:
        raise ValidationError("delta CAPTURE inputs changed during scan")
    if helper.snapshot_inputs(unregistered) != unregistered_snapshot_before:
        raise ValidationError("unregistered CAPTURE metadata changed during scan")
    support_after = verify_support_hashes(external)
    image_after, span_hashes_after = verify_image(image_path)
    if support_after != support_before:
        raise ValidationError("supporting input changed during scan")
    if image_after != image_before or span_hashes_after != span_hashes_before:
        raise ValidationError("GameClient image changed during scan")

    outputs = {
        external / "PF_ATTR_FIELD_VALIDATION_DELTA.tsv": output_tsv,
        external / "PF_ATTR_FIELD_VALIDATION_DELTA.md": output_md,
    }
    if args.check:
        for path, expected in outputs.items():
            if not path.is_file():
                raise ValidationError(f"missing output for --check: {path.name}")
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                raise ValidationError(f"output drift: {path.name}")
    else:
        atomic_publish(outputs)

    print(f"lock_state={lock_state}")
    print(f"image_sha256_before={image_before}")
    print(f"image_sha256_after={image_after}")
    for key in sorted(EXPECTED_METRICS):
        print(f"{key}={metrics[key]}")
    print(f"wrapper_mismatches={metrics['wrapper_mismatches']}")
    print(f"unregistered_excluded_files={metrics['unregistered_excluded_files']}")
    print(f"unregistered_manifest={helper.manifest_sha256(unregistered)}")
    print(f"output_mode={'check' if args.check else 'publish'}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
