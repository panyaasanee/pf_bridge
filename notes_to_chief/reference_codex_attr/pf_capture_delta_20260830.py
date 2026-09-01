#!/usr/bin/env python3
"""Build a non-duplicating A5 delta from the 2026-08-30 capture additions.

The script is intentionally read-only toward GameClient and every frozen v1
artifact.  It publishes only aggregate metadata/evidence under pf_bridge/external:
paths, sizes, hashes, counts, statuses, and mismatch field indexes/reasons.  It
never publishes capture payloads, field values, or hexdumps.
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

# Importing the frozen validator must not create a .pyc beside that input.
sys.dont_write_bytecode = True


SOURCE = "CAPTURE"
BATCH = "20260830"
EXPECTED_BASELINE_CAPTURE_PATHS = 1772
EXPECTED_CURRENT_CAPTURE_PATHS = 2154
EXPECTED_NEW_CAPTURE_PATHS = 382
EXPECTED_IMAGE_SIZE = 14_759_424
EXPECTED_IMAGE_SHA256 = (
    "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
)
EXPECTED_VALIDATOR_SHA256 = (
    "cafa5f69401eaf152f7ae4e646ce76eb3016c3d6b71e76c494819a029877011b"
)
EXPECTED_V1_HASHES = {
    "PF_PROTOCOL_REGISTRY.tsv": (
        "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d"
    ),
    "PF_SERIALIZER_FIELDS.tsv": (
        "99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123"
    ),
    "PF_TAG_CENSUS.tsv": (
        "63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a"
    ),
    "PF_INPUT_INVENTORY.tsv": (
        "729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1"
    ),
    "PF_PROTOCOL_PRIORITY.tsv": (
        "d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55"
    ),
    "PF_FIELD_VALIDATION.tsv": (
        "080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3"
    ),
}
FROZEN_V1_NAMES = frozenset(
    {
        "00_SEARCH_HERE_FIRST.md",
        "pf_build_priority.py",
        "pf_build_v1_manifest.py",
        "PF_DATA_EVIDENCE.md",
        "PF_DATA_EVIDENCE.tsv",
        "PF_DUMP_REQUEST.md",
        "PF_ERRATUM_TWO_IMAGES.md",
        "PF_EXTERNAL_REPORT.md",
        "pf_extract_data_evidence.py",
        "pf_extract_dump_rtti.py",
        "pf_extract_protocol.py",
        "PF_FIELD_VALIDATION.md",
        "PF_FIELD_VALIDATION.tsv",
        "PF_HANDOFF_V1.md",
        "PF_INPUT_INVENTORY.md",
        "PF_INPUT_INVENTORY.tsv",
        "pf_inventory_inputs.py",
        "PF_PROTOCOL_PRIORITY.md",
        "PF_PROTOCOL_PRIORITY.tsv",
        "PF_PROTOCOL_REGISTRY.md",
        "PF_PROTOCOL_REGISTRY.tsv",
        "PF_RUNTIME_CLASSMAP.md",
        "PF_RUNTIME_CLASSMAP.tsv",
        "PF_SERIALIZER_FIELDS.md",
        "PF_SERIALIZER_FIELDS.tsv",
        "PF_TAG_CENSUS.tsv",
        "PF_V1_MANIFEST.md",
        "pf_validate_capture_fields.py",
    }
)
OUTPUT_NAMES = frozenset(
    {
        "PF_CAPTURE_DELTA_20260830.inventory.tsv",
        "PF_CAPTURE_DELTA_20260830.validation.tsv",
        "PF_CAPTURE_DELTA_20260830.md",
        "pf_capture_delta_20260830.py",
    }
)
RAW_BYTE_RUN_RE = re.compile(
    r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"
)


class DeltaError(RuntimeError):
    pass


@dataclass(frozen=True)
class FreshPath:
    relative_path: str
    path: Path


@dataclass(frozen=True)
class NewInput:
    batch_id: str
    relative_path: str
    path: Path
    size: int
    sha256: str
    content_class: str
    canonical_relative_path: str
    claim_eligible: bool
    exclusion_reason: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def stable_key(value: str) -> tuple[str, str]:
    return value.casefold(), value


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tsv_text(headers: list[str], rows: list[list[str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return stream.getvalue()


def load_validator(path: Path) -> ModuleType:
    if sha256_file(path) != EXPECTED_VALIDATOR_SHA256:
        raise DeltaError("GT-047 validator SHA-256 changed")
    spec = importlib.util.spec_from_file_location("pf_gt047_validator_20260830", path)
    if spec is None or spec.loader is None:
        raise DeltaError("cannot load GT-047 validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def enumerate_capture_paths(root: Path) -> dict[str, FreshPath]:
    """Enumerate each file once and reject case-fold path aliases."""
    result: dict[str, FreshPath] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if not any(part.startswith("capture_") for part in relative.parts[:-1]):
            continue
        relative_text = relative.as_posix()
        key = relative_text.casefold()
        previous = result.get(key)
        if previous is not None and previous.relative_path != relative_text:
            raise DeltaError(
                "case-fold collision in current capture paths: "
                f"{previous.relative_path} / {relative_text}"
            )
        result[key] = FreshPath(relative_text, path)
    return result


def load_baseline_rows(inventory_path: Path) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    rows = [row for row in read_tsv(inventory_path) if row.get("source") == SOURCE]
    if len(rows) != EXPECTED_BASELINE_CAPTURE_PATHS:
        raise DeltaError(
            f"baseline capture rows {len(rows)} != {EXPECTED_BASELINE_CAPTURE_PATHS}"
        )
    by_key: dict[str, dict[str, str]] = {}
    for row in rows:
        relative = row["relative_path"]
        key = relative.casefold()
        if key in by_key:
            raise DeltaError(f"duplicate case-fold path in baseline: {relative}")
        if row.get("source") != SOURCE:
            raise DeltaError("baseline source guard failed")
        if not row.get("size", "").isdigit() or not re.fullmatch(
            r"[0-9a-f]{64}", row.get("sha256", "")
        ):
            raise DeltaError(f"invalid baseline size/hash: {relative}")
        by_key[key] = row
    return rows, by_key


def verify_baseline(
    baseline_rows: list[dict[str, str]], fresh: dict[str, FreshPath]
) -> None:
    """One complete size/hash verification pass over all 1,772 baseline paths."""
    for row in baseline_rows:
        relative = row["relative_path"]
        item = fresh.get(relative.casefold())
        if item is None:
            raise DeltaError(f"baseline capture path missing: {relative}")
        if item.relative_path != relative:
            raise DeltaError(f"baseline path spelling/case changed: {relative}")
        before = item.path.stat()
        digest = sha256_file(item.path)
        after = item.path.stat()
        if (
            before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
            or before.st_size != int(row["size"])
            or digest != row["sha256"]
        ):
            raise DeltaError(f"baseline capture changed: {relative}")


def first_hash_new(paths: list[FreshPath]) -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for item in paths:
        before = item.path.stat()
        digest = sha256_file(item.path)
        after = item.path.stat()
        if before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns:
            raise DeltaError(f"new capture changed during first read: {item.relative_path}")
        result[item.relative_path] = (before.st_size, digest)
    return result


def classify_new_inputs(
    paths: list[FreshPath],
    first_hashes: dict[str, tuple[int, str]],
    baseline_rows: list[dict[str, str]],
) -> list[NewInput]:
    baseline_by_hash: dict[str, list[str]] = defaultdict(list)
    for row in baseline_rows:
        baseline_by_hash[row["sha256"]].append(row["relative_path"])
    new_by_hash: dict[str, list[str]] = defaultdict(list)
    for item in paths:
        new_by_hash[first_hashes[item.relative_path][1]].append(item.relative_path)
    for values in baseline_by_hash.values():
        values.sort(key=stable_key)
    for values in new_by_hash.values():
        values.sort(key=stable_key)

    output: list[NewInput] = []
    sorted_paths = sorted(paths, key=lambda item: stable_key(item.relative_path))
    for ordinal, item in enumerate(sorted_paths, 1):
        size, digest = first_hashes[item.relative_path]
        if digest in baseline_by_hash:
            content_class = "DUPLICATE_BASELINE_CONTENT"
            canonical = baseline_by_hash[digest][0]
            eligible = False
            reason = "SHA256_ALREADY_IN_V1"
        else:
            canonical = new_by_hash[digest][0]
            if item.relative_path == canonical:
                content_class = "UNIQUE_NEW_CONTENT"
                eligible = True
                reason = "NONE"
            else:
                content_class = "DUPLICATE_NEW_CONTENT"
                eligible = False
                reason = "NONCANONICAL_SAME_SHA256"
        output.append(
            NewInput(
                batch_id=f"CAPTURE-DELTA-{BATCH}-{ordinal:04d}",
                relative_path=item.relative_path,
                path=item.path,
                size=size,
                sha256=digest,
                content_class=content_class,
                canonical_relative_path=canonical,
                claim_eligible=eligible,
                exclusion_reason=reason,
            )
        )
    return output


def verify_new_second_pass(items: list[NewInput]) -> None:
    """Second independent read of every new path before publication."""
    for item in items:
        before = item.path.stat()
        digest = sha256_file(item.path)
        after = item.path.stat()
        if (
            before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
            or before.st_size != item.size
            or digest != item.sha256
        ):
            raise DeltaError(f"new capture changed during second read: {item.relative_path}")


def snapshot_frozen_external(external: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in sorted(FROZEN_V1_NAMES):
        path = external / name
        if not path.is_file():
            raise DeltaError(f"frozen v1 artifact missing: {name}")
        result[name] = sha256_file(path)
    return result


def verify_v1_hash_pins(external: Path) -> None:
    for name, expected in EXPECTED_V1_HASHES.items():
        path = external / name
        if not path.is_file() or sha256_file(path) != expected:
            raise DeltaError(f"frozen v1 hash mismatch: {name}")


def verify_image(path: Path) -> None:
    if path.stat().st_size != EXPECTED_IMAGE_SIZE:
        raise DeltaError("GameClient.local.bin size changed")
    if sha256_file(path) != EXPECTED_IMAGE_SHA256:
        raise DeltaError("GameClient.local.bin SHA-256 changed")


def bump_direction(counts: object, kind: str) -> str:
    if kind == "PC":
        counts.pc_blocks += 1
        return "R"
    counts.decompressed_blocks += 1
    return "W"


def parse_delta(
    validator: ModuleType,
    inputs: list[NewInput],
    id_to_name: dict[int, str],
    schemas: dict[tuple[str, str], list[object]],
    static_open: set[str],
) -> tuple[
    dict[tuple[str, str], object],
    object,
    dict[tuple[str, str], object],
    object,
    dict[str, tuple[str, int, int]],
]:
    raw_aggregates: dict[tuple[str, str], object] = defaultdict(
        validator.MessageAggregate
    )
    claim_aggregates: dict[tuple[str, str], object] = defaultdict(
        validator.MessageAggregate
    )
    raw_counts = validator.RunCounts()
    claim_counts = validator.RunCounts()
    path_dispositions: dict[str, tuple[str, int, int]] = {}

    for item in inputs:
        if item.path.suffix.casefold() != ".txt":
            path_dispositions[item.relative_path] = ("NOT_TEXT", 0, 0)
            continue
        text = item.path.read_text(encoding="utf-8", errors="replace")
        blocks, errors = validator.extract_pc_blocks(text)
        error_count = sum(errors.values())
        if error_count:
            disposition = "BLOCK_MARKER_OR_ENVELOPE_ERROR"
        elif blocks:
            disposition = "RECOGNIZED_PACKET_BLOCKS"
        else:
            disposition = "NO_RECOGNIZED_PACKET_BLOCKS"
        path_dispositions[item.relative_path] = (
            disposition,
            len(blocks),
            error_count,
        )
        raw_counts.capture_text_files += 1
        raw_counts.block_errors.update(errors)
        if blocks:
            raw_counts.files_with_blocks.add(item.relative_path)
        if item.claim_eligible:
            claim_counts.capture_text_files += 1
            claim_counts.block_errors.update(errors)
            if blocks:
                claim_counts.files_with_blocks.add(item.relative_path)
        for ordinal, (kind, data) in enumerate(blocks, 1):
            direction = bump_direction(raw_counts, kind)
            frame_key = f"{item.relative_path}:{ordinal}"
            validator.parse_capture_frame(
                data,
                direction,
                frame_key,
                item.relative_path,
                id_to_name,
                schemas,
                static_open,
                raw_aggregates,
                raw_counts,
            )
            if item.claim_eligible:
                bump_direction(claim_counts, kind)
                validator.parse_capture_frame(
                    data,
                    direction,
                    frame_key,
                    item.relative_path,
                    id_to_name,
                    schemas,
                    static_open,
                    claim_aggregates,
                    claim_counts,
                )
    if len(path_dispositions) != len(inputs):
        raise DeltaError("capture path disposition census does not balance")
    return (
        claim_aggregates,
        claim_counts,
        raw_aggregates,
        raw_counts,
        path_dispositions,
    )


def generalized_count_guard(counts: object, aggregates: dict[tuple[str, str], object]) -> None:
    if counts.nested_reached_instances + counts.nested_unresolved_after_open != counts.nested_declared_instances:
        raise DeltaError("nested delta accounting does not balance")
    aggregate_instances = sum(value.observed_instances for value in aggregates.values())
    outcomes = sum(
        value.pass_instances + value.static_open_instances + value.mismatch_instances
        for value in aggregates.values()
    )
    if aggregate_instances != outcomes:
        raise DeltaError("delta outcome accounting does not balance")
    for aggregate in aggregates.values():
        if aggregate.observed_instances != (
            aggregate.pass_instances
            + aggregate.static_open_instances
            + aggregate.mismatch_instances
        ):
            raise DeltaError("message outcome accounting does not balance")


def aggregate_status(aggregate: object) -> str:
    if aggregate.observed_instances == 0:
        return "DUPLICATE_ONLY"
    if aggregate.mismatch_instances:
        return "MISMATCH"
    if aggregate.static_open_instances:
        return "SCHEMA_NOT_APPLIED"
    return "MATCHED_PINNED_SCHEMA"


def mismatch_text(aggregate: object) -> str:
    return " | ".join(
        f"{field_index}:{reason}:{occurrences}"
        for (field_index, reason), occurrences in sorted(
            aggregate.mismatch_points.items()
        )
    ) or "NONE"


def build_inventory_tsv(
    inputs: list[NewInput],
    path_dispositions: dict[str, tuple[str, int, int]],
) -> str:
    headers = [
        "batch_id",
        "relative_path",
        "size",
        "sha256",
        "content_class",
        "canonical_relative_path",
        "claim_eligible",
        "exclusion_reason",
        "parse_disposition",
        "recognized_block_count",
        "block_error_count",
        "verification",
        "source",
    ]
    rows = [
        [
            item.batch_id,
            item.relative_path,
            str(item.size),
            item.sha256,
            item.content_class,
            item.canonical_relative_path,
            "YES" if item.claim_eligible else "NO",
            item.exclusion_reason,
            path_dispositions[item.relative_path][0],
            str(path_dispositions[item.relative_path][1]),
            str(path_dispositions[item.relative_path][2]),
            "SIZE_SHA256_VERIFIED_TWICE",
            SOURCE,
        ]
        for item in inputs
    ]
    return tsv_text(headers, rows)


def load_unique_by_message(path: Path, key_name: str) -> dict[str, dict[str, str]]:
    rows = read_tsv(path)
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row[key_name]
        if key in output:
            raise DeltaError(f"duplicate {key_name}: {key}")
        output[key] = row
    return output


def load_v1_validation(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    rows = read_tsv(path)
    output: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        if row.get("source") != SOURCE:
            raise DeltaError("v1 field validation source changed")
        key = (row["message"], row["direction(W/R)"])
        if key in output:
            raise DeltaError(f"duplicate v1 field-validation key: {key}")
        output[key] = row
    if len(output) != 1038:
        raise DeltaError(f"v1 field-validation row count {len(output)} != 1038")
    return output


def build_validation_tsv(
    claim_aggregates: dict[tuple[str, str], object],
    raw_aggregates: dict[tuple[str, str], object],
    v1_validation: dict[tuple[str, str], dict[str, str]],
) -> tuple[str, dict[str, int]]:
    headers = [
        "message",
        "direction(W/R)",
        "v1_capture_status_ref",
        "delta_bookkeeping",
        "claim_observed_frames",
        "claim_observed_instances",
        "claim_schema_match_frames",
        "claim_schema_match_instances",
        "claim_schema_not_applied_frames",
        "claim_schema_not_applied_instances",
        "claim_mismatch_frames",
        "claim_mismatch_instances",
        "claim_mismatch_field_index_reason_count",
        "claim_capture_file_count",
        "claim_capture_outcome",
        "raw_path_observed_frames",
        "raw_path_observed_instances",
        "raw_path_schema_match_instances",
        "raw_path_schema_not_applied_instances",
        "raw_path_mismatch_instances",
        "raw_path_capture_file_count",
        "duplicate_rejected_instances",
        "first_seen_in_capture_delta",
        "source",
    ]
    keys = sorted(
        {
            key
            for key, aggregate in raw_aggregates.items()
            if aggregate.observed_instances
        },
        key=lambda key: (stable_key(key[0]), key[1]),
    )
    rows: list[list[str]] = []
    bookkeeping = Counter()
    for key in keys:
        message, direction = key
        raw = raw_aggregates[key]
        claim = claim_aggregates[key]
        prior = v1_validation.get(key)
        if prior is None:
            raise DeltaError(f"delta message missing join row: {message}/{direction}")
        prior_instances = int(prior["observed_instances"])
        if claim.observed_instances and prior_instances == 0:
            delta_bookkeeping = "ADDED"
        elif claim.observed_instances:
            delta_bookkeeping = "CHANGED"
        else:
            delta_bookkeeping = "UNCHANGED_DUPLICATE_ONLY"
        bookkeeping[delta_bookkeeping] += 1
        duplicate_rejected_instances = raw.observed_instances - claim.observed_instances
        if duplicate_rejected_instances < 0:
            raise DeltaError("claim instance count exceeds raw-path count")
        first_seen = prior_instances == 0 and claim.observed_instances > 0
        rows.append(
            [
                message,
                direction,
                prior["status"],
                delta_bookkeeping,
                str(len(claim.observed_frames)),
                str(claim.observed_instances),
                str(len(claim.pass_frames)),
                str(claim.pass_instances),
                str(len(claim.static_open_frames)),
                str(claim.static_open_instances),
                str(len(claim.mismatch_frames)),
                str(claim.mismatch_instances),
                mismatch_text(claim),
                str(len(claim.capture_files)),
                aggregate_status(claim),
                str(len(raw.observed_frames)),
                str(raw.observed_instances),
                str(raw.pass_instances),
                str(raw.static_open_instances),
                str(raw.mismatch_instances),
                str(len(raw.capture_files)),
                str(duplicate_rejected_instances),
                "YES" if first_seen else "NO",
                SOURCE,
            ]
        )
    bookkeeping["UNCHANGED"] = 1038 - bookkeeping["ADDED"] - bookkeeping["CHANGED"]
    return tsv_text(headers, rows), dict(bookkeeping)


def count_values(counts: object, aggregates: dict[tuple[str, str], object]) -> dict[str, int]:
    return {
        "text_files": counts.capture_text_files,
        "files_with_blocks": len(counts.files_with_blocks),
        "pc_blocks": counts.pc_blocks,
        "decompressed_blocks": counts.decompressed_blocks,
        "block_errors": sum(counts.block_errors.values()),
        "outer_instances": counts.outer_instances,
        "nested_declared": counts.nested_declared_instances,
        "nested_reached": counts.nested_reached_instances,
        "nested_unresolved": counts.nested_unresolved_after_open,
        "unknown_message_ids": counts.unknown_message_id_instances,
        "pass_instances": sum(value.pass_instances for value in aggregates.values()),
        "static_open_instances": sum(
            value.static_open_instances for value in aggregates.values()
        ),
        "mismatch_instances": sum(
            value.mismatch_instances for value in aggregates.values()
        ),
    }


def build_markdown(
    inputs: list[NewInput],
    path_dispositions: dict[str, tuple[str, int, int]],
    claim_aggregates: dict[tuple[str, str], object],
    claim_counts: object,
    raw_aggregates: dict[tuple[str, str], object],
    raw_counts: object,
    v1_validation: dict[tuple[str, str], dict[str, str]],
    bookkeeping: dict[str, int],
) -> str:
    claim_values = count_values(claim_counts, claim_aggregates)
    raw_values = count_values(raw_counts, raw_aggregates)
    duplicate_baseline = sum(
        item.content_class == "DUPLICATE_BASELINE_CONTENT" for item in inputs
    )
    duplicate_new = sum(
        item.content_class == "DUPLICATE_NEW_CONTENT" for item in inputs
    )
    unique_new = sum(item.claim_eligible for item in inputs)
    excluded = duplicate_baseline + duplicate_new
    non_text = sum(item.path.suffix.casefold() != ".txt" for item in inputs)
    claim_text = sum(
        item.claim_eligible and item.path.suffix.casefold() == ".txt" for item in inputs
    )
    raw_dispositions = Counter(
        value[0] for value in path_dispositions.values()
    )
    claim_dispositions = Counter(
        path_dispositions[item.relative_path][0]
        for item in inputs
        if item.claim_eligible
    )
    mismatch_points = {
        (message, direction, index, reason)
        for (message, direction), aggregate in claim_aggregates.items()
        for (index, reason) in aggregate.mismatch_points
    }
    lines: list[str] = []
    if mismatch_points:
        lines.extend(
            [
                "# RED: capture delta contains A2 mismatches",
                "",
                "The mismatches are reported as-is. No IMAGE table was changed to fit capture data.",
                "",
            ]
        )
    else:
        lines.extend(["# PF capture delta 20260830", ""])
    lines.extend(
        [
            "[MEASURED] Path, hash, disposition, frame, and validation counts below are re-derived from the pinned CAPTURE corpus by this generator.",
            "",
            "This is an incremental `source=CAPTURE` batch. It contains no payload values, capture bytes, or hexdumps and does not repeat the 1,772-row v1 inventory or the 1,038-row v1 A5 table.",
            "",
            "## Input and de-duplication",
            "",
            f"- v1 paths verified twice against frozen size/SHA-256: {EXPECTED_BASELINE_CAPTURE_PATHS}",
            f"- current paths: {EXPECTED_CURRENT_CAPTURE_PATHS}; new paths inventoried: {len(inputs)}; missing v1 paths: 0",
            f"- new bytes: {sum(item.size for item in inputs)}",
            f"- unique new content (claim-eligible canonical paths): {unique_new}",
            f"- exact-content duplicates rejected: {excluded} path(s) ({duplicate_baseline} already in v1; {duplicate_new} aliases within this batch)",
            f"- raw new text paths inspected: {raw_values['text_files']}; claim-eligible text paths inspected: {claim_text}; non-text new paths: {non_text}",
            f"- raw path dispositions: recognized blocks={raw_dispositions['RECOGNIZED_PACKET_BLOCKS']}; no recognized blocks={raw_dispositions['NO_RECOGNIZED_PACKET_BLOCKS']}; marker/envelope error={raw_dispositions['BLOCK_MARKER_OR_ENVELOPE_ERROR']}; non-text={raw_dispositions['NOT_TEXT']}",
            f"- claim-eligible dispositions: recognized blocks={claim_dispositions['RECOGNIZED_PACKET_BLOCKS']}; no recognized blocks={claim_dispositions['NO_RECOGNIZED_PACKET_BLOCKS']}; marker/envelope error={claim_dispositions['BLOCK_MARKER_OR_ENVELOPE_ERROR']}; non-text={claim_dispositions['NOT_TEXT']}",
            "- Canonical selection is the lexicographically first relative path for each full-file SHA-256. If the SHA-256 already exists in v1, every new alias is excluded from claim counts.",
            "",
            "## A5 delta: de-duplicated claim counts",
            "",
            f"- files containing parseable blocks: {claim_values['files_with_blocks']}",
            f"- PC blocks: {claim_values['pc_blocks']}; DECOMPRESSED blocks: {claim_values['decompressed_blocks']}",
            f"- matched pinned schema: {claim_values['pass_instances']} message instance(s)",
            f"- schema not applied: {claim_values['static_open_instances']} message instance(s); these are not promoted to matched",
            f"- nested declared/reached/unresolved-after-schema-not-applied: {claim_values['nested_declared']}/{claim_values['nested_reached']}/{claim_values['nested_unresolved']}",
            "- unresolved nested reason: UNRESOLVED_AFTER_SCHEMA_NOT_APPLIED; these trailing instances were not checked for later field mismatches or IDs",
            f"- mismatch: {claim_values['mismatch_instances']} instance(s), {len(mismatch_points)} distinct message/direction/field/reason point(s)",
            f"- block/envelope errors: {claim_values['block_errors']}; unknown message IDs: {claim_values['unknown_message_ids']}",
            "",
            "## Raw-path comparison (duplicates included only for audit)",
            "",
            f"- files containing parseable blocks: {raw_values['files_with_blocks']}",
            f"- PC blocks: {raw_values['pc_blocks']}; DECOMPRESSED blocks: {raw_values['decompressed_blocks']}",
            f"- matched pinned schema: {raw_values['pass_instances']} message instance(s)",
            f"- schema not applied: {raw_values['static_open_instances']} message instance(s)",
            f"- nested declared/reached/unresolved-after-schema-not-applied: {raw_values['nested_declared']}/{raw_values['nested_reached']}/{raw_values['nested_unresolved']}",
            f"- mismatch: {raw_values['mismatch_instances']} message instance(s)",
            f"- duplicate-rejected message instances: {sum(value.observed_instances for value in raw_aggregates.values()) - sum(value.observed_instances for value in claim_aggregates.values())}",
            "",
            "## Delta bookkeeping against v1 A5",
            "",
            f"- ADDED message/direction rows (not observed in v1, claim-observed here): {bookkeeping.get('ADDED', 0)}",
            f"- CHANGED message/direction rows (already observed in v1, more claim evidence here): {bookkeeping.get('CHANGED', 0)}",
            f"- UNCHANGED message/direction rows in the 1,038-key universe: {bookkeeping.get('UNCHANGED', 0)}",
            f"- observed duplicate-only rows rejected from claim evidence: {bookkeeping.get('UNCHANGED_DUPLICATE_ONLY', 0)}",
            "",
            "## Message/direction observations first seen in this CAPTURE delta",
            "",
            "| message | direction | claim instances | raw instances | CAPTURE outcome |",
            "|---|:---:|---:|---:|---|",
        ]
    )
    first_seen_rows = []
    for key, claim in claim_aggregates.items():
        if (
            claim.observed_instances
            and int(v1_validation[key]["observed_instances"]) == 0
        ):
            raw = raw_aggregates[key]
            first_seen_rows.append(
                (key[0], key[1], claim.observed_instances, raw.observed_instances, aggregate_status(claim))
            )
    for message, direction, claim_instances, raw_instances, outcome in sorted(
        first_seen_rows, key=lambda row: (stable_key(row[0]), row[1])
    ):
        lines.append(
            "| `%s` | %s | %d | %d | %s |"
            % (
                message,
                direction,
                claim_instances,
                raw_instances,
                outcome,
            )
        )
    if not first_seen_rows:
        lines.append("| NONE | - | 0 | 0 | - |")
    lines.extend(
        [
            "",
            "This table reports CAPTURE observations only. Priority and serializer closure remain in separate IMAGE-source tables and are not embedded in these rows.",
            "",
            "## Guards and bindings",
            "",
            f"- GT-047 validator SHA-256: `{EXPECTED_VALIDATOR_SHA256}`",
            f"- GameClient.local.bin SHA-256 before/after: `{EXPECTED_IMAGE_SHA256}`",
            f"- v1 input inventory SHA-256: `{EXPECTED_V1_HASHES['PF_INPUT_INVENTORY.tsv']}`",
            f"- v1 field validation SHA-256: `{EXPECTED_V1_HASHES['PF_FIELD_VALIDATION.tsv']}`",
            "- GT-047 parser regression, schema mutation, A2/A3 census, static-open membership, and W/R field-offset mirror guards all passed before parsing.",
            "- Every v1 and new capture path was size/hash checked once before parsing and once again before publication.",
            "- Every frozen external file and the local image were re-hashed after parsing; no frozen artifact changed.",
            "",
        ]
    )
    return "\n".join(lines)


def validate_tsv_outputs(inventory_text: str, validation_text: str) -> None:
    inventory_rows = list(
        csv.DictReader(io.StringIO(inventory_text), delimiter="\t")
    )
    validation_rows = list(
        csv.DictReader(io.StringIO(validation_text), delimiter="\t")
    )
    if len(inventory_rows) != EXPECTED_NEW_CAPTURE_PATHS:
        raise DeltaError("delta inventory row count changed")
    if any(row.get("source") != SOURCE for row in inventory_rows + validation_rows):
        raise DeltaError("delta TSV source-only guard failed")
    batch_ids = [row["batch_id"] for row in inventory_rows]
    path_keys = [row["relative_path"].casefold() for row in inventory_rows]
    validation_keys = [
        (row["message"], row["direction(W/R)"]) for row in validation_rows
    ]
    if len(batch_ids) != len(set(batch_ids)):
        raise DeltaError("duplicate delta batch ID")
    if len(path_keys) != len(set(path_keys)):
        raise DeltaError("duplicate delta case-fold path")
    if len(validation_keys) != len(set(validation_keys)):
        raise DeltaError("duplicate delta message/direction key")
    forbidden_mixed_columns = {
        "priority_ref",
        "structural_status_ref",
        "p1_open_ref",
        "still_static_open",
    }
    if forbidden_mixed_columns.intersection(validation_rows[0] if validation_rows else ()):
        raise DeltaError("IMAGE-derived priority/closure column leaked into CAPTURE TSV")
    dispositions = Counter(row["parse_disposition"] for row in inventory_rows)
    if dispositions != Counter(
        {
            "RECOGNIZED_PACKET_BLOCKS": 117,
            "NO_RECOGNIZED_PACKET_BLOCKS": 236,
            "NOT_TEXT": 29,
        }
    ):
        raise DeltaError(f"capture parse-disposition census changed: {dict(dispositions)}")
    claim_dispositions = Counter(
        row["parse_disposition"]
        for row in inventory_rows
        if row["claim_eligible"] == "YES"
    )
    if claim_dispositions != Counter(
        {
            "RECOGNIZED_PACKET_BLOCKS": 116,
            "NO_RECOGNIZED_PACKET_BLOCKS": 175,
            "NOT_TEXT": 29,
        }
    ):
        raise DeltaError(
            f"claim parse-disposition census changed: {dict(claim_dispositions)}"
        )
    if any(
        row["claim_capture_outcome"] == "MATCHED_PINNED_SCHEMA"
        and int(row["claim_schema_not_applied_instances"])
        for row in validation_rows
    ):
        raise DeltaError("schema-not-applied row was promoted to matched")
    if RAW_BYTE_RUN_RE.search(inventory_text) or RAW_BYTE_RUN_RE.search(validation_text):
        raise DeltaError("raw-byte-run guard fired in TSV")


def validate_output_mutation_regressions(inventory_text: str, validation_text: str) -> None:
    bad_source = validation_text.replace("\tCAPTURE\n", "\tIMAGE\n", 1)
    try:
        validate_tsv_outputs(inventory_text, bad_source)
    except DeltaError:
        pass
    else:
        raise DeltaError("source mutation was unexpectedly accepted")
    lines = validation_text.splitlines()
    if len(lines) > 1:
        duplicate = validation_text + lines[1] + "\n"
        try:
            validate_tsv_outputs(inventory_text, duplicate)
        except DeltaError:
            pass
        else:
            raise DeltaError("key duplication mutation was unexpectedly accepted")
    raw_mutation = validation_text + "00 11 22 33 44 55 66 77\n"
    try:
        validate_tsv_outputs(inventory_text, raw_mutation)
    except DeltaError:
        pass
    else:
        raise DeltaError("raw-byte mutation was unexpectedly accepted")


def atomic_publish(outputs: dict[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, text in outputs.items():
            fd, raw_temp = tempfile.mkstemp(
                prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
            )
            temp = Path(raw_temp)
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
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
    script_external = Path(__file__).resolve().parent
    parser.add_argument("--external", type=Path, default=script_external)
    parser.add_argument(
        "--game-client",
        type=Path,
        default=script_external.parent.parent / "GameClient",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="derive in memory and require byte-identical existing outputs",
    )
    args = parser.parse_args()
    external = args.external.resolve()
    game_client = args.game_client.resolve()
    if external != script_external:
        raise DeltaError("outputs are restricted to the script external directory")

    validator_path = external.parent / "patches" / "gt047" / "pf_validate_capture_fields.py"
    image_path = game_client / "GameClient.local.bin"
    frozen_before = snapshot_frozen_external(external)
    verify_v1_hash_pins(external)
    verify_image(image_path)
    validator = load_validator(validator_path)

    registry_rows = read_tsv(external / "PF_PROTOCOL_REGISTRY.tsv")
    field_rows = read_tsv(external / "PF_SERIALIZER_FIELDS.tsv")
    tag_rows = read_tsv(external / "PF_TAG_CENSUS.tsv")
    id_to_name, schemas, static_open = validator.build_schemas(
        registry_rows, field_rows, tag_rows
    )
    validator.validate_parser_regressions()
    validator.validate_schema_mutation_regressions(
        registry_rows, field_rows, tag_rows
    )

    baseline_rows, baseline_by_key = load_baseline_rows(
        external / "PF_INPUT_INVENTORY.tsv"
    )
    fresh = enumerate_capture_paths(game_client)
    if len(fresh) != EXPECTED_CURRENT_CAPTURE_PATHS:
        raise DeltaError(
            f"current capture paths {len(fresh)} != {EXPECTED_CURRENT_CAPTURE_PATHS}"
        )
    missing = set(baseline_by_key) - set(fresh)
    if missing:
        raise DeltaError(f"missing baseline capture paths: {len(missing)}")
    new_keys = sorted(set(fresh) - set(baseline_by_key))
    if len(new_keys) != EXPECTED_NEW_CAPTURE_PATHS:
        raise DeltaError(f"new capture paths {len(new_keys)} != {EXPECTED_NEW_CAPTURE_PATHS}")
    # A case-fold alias of a baseline path is not allowed to masquerade as new.
    for key in set(fresh) & set(baseline_by_key):
        if fresh[key].relative_path != baseline_by_key[key]["relative_path"]:
            raise DeltaError(f"case-fold alias against baseline: {fresh[key].relative_path}")

    new_paths = [fresh[key] for key in new_keys]
    verify_baseline(baseline_rows, fresh)
    first_hashes = first_hash_new(new_paths)
    inputs = classify_new_inputs(new_paths, first_hashes, baseline_rows)
    if len(inputs) != EXPECTED_NEW_CAPTURE_PATHS:
        raise DeltaError("classified delta input count changed")

    v1_validation = load_v1_validation(external / "PF_FIELD_VALIDATION.tsv")
    (
        claim_aggregates,
        claim_counts,
        raw_aggregates,
        raw_counts,
        path_dispositions,
    ) = parse_delta(validator, inputs, id_to_name, schemas, static_open)
    generalized_count_guard(claim_counts, claim_aggregates)
    generalized_count_guard(raw_counts, raw_aggregates)

    inventory_text = build_inventory_tsv(inputs, path_dispositions)
    validation_text, bookkeeping = build_validation_tsv(
        claim_aggregates,
        raw_aggregates,
        v1_validation,
    )
    markdown_text = build_markdown(
        inputs,
        path_dispositions,
        claim_aggregates,
        claim_counts,
        raw_aggregates,
        raw_counts,
        v1_validation,
        bookkeeping,
    )
    validate_tsv_outputs(inventory_text, validation_text)
    validate_output_mutation_regressions(inventory_text, validation_text)
    if RAW_BYTE_RUN_RE.search(markdown_text):
        raise DeltaError("raw-byte-run guard fired in Markdown")

    # Close the read-only window with a fully independent second pass.
    fresh_after = enumerate_capture_paths(game_client)
    if set(fresh_after) != set(fresh):
        raise DeltaError("capture path set changed during delta run")
    if any(
        fresh_after[key].relative_path != fresh[key].relative_path for key in fresh
    ):
        raise DeltaError("capture path spelling changed during delta run")
    verify_baseline(baseline_rows, fresh_after)
    verify_new_second_pass(inputs)
    verify_image(image_path)
    verify_v1_hash_pins(external)
    frozen_after = snapshot_frozen_external(external)
    if frozen_after != frozen_before:
        raise DeltaError("a frozen external artifact changed during delta run")

    outputs = {
        external / "PF_CAPTURE_DELTA_20260830.inventory.tsv": inventory_text,
        external / "PF_CAPTURE_DELTA_20260830.validation.tsv": validation_text,
        external / "PF_CAPTURE_DELTA_20260830.md": markdown_text,
    }
    if args.check:
        for path, expected_text in outputs.items():
            if not path.is_file():
                raise DeltaError(f"check output missing: {path.name}")
            if path.read_text(encoding="utf-8") != expected_text:
                raise DeltaError(f"check output differs: {path.name}")
    else:
        atomic_publish(outputs)
        # Published bytes must be exactly the validated strings.
        for path, expected_text in outputs.items():
            if path.read_text(encoding="utf-8") != expected_text:
                raise DeltaError(f"published output verification failed: {path.name}")

    claim_values = count_values(claim_counts, claim_aggregates)
    print(
        "new_paths=%d unique_claim_paths=%d duplicate_rejected_paths=%d "
        "claim_matched=%d claim_schema_not_applied=%d claim_mismatch=%d rows=%d mode=%s"
        % (
            len(inputs),
            sum(item.claim_eligible for item in inputs),
            sum(not item.claim_eligible for item in inputs),
            claim_values["pass_instances"],
            claim_values["static_open_instances"],
            claim_values["mismatch_instances"],
            len(read_tsv(external / "PF_CAPTURE_DELTA_20260830.validation.tsv")),
            "check" if args.check else "publish",
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeltaError as exc:
        raise SystemExit(f"ERROR: {exc}")
