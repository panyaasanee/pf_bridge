#!/usr/bin/env python3
"""Replay captures against the effective V3 A2 after new non-wire removals.

The validator reuses the frozen V2 parser and content-deduplicated corpus.  It
adds only exact base-row-keyed removals, keeps IMAGE and CAPTURE evidence in
separate rows, and exports aggregate counts only (never capture bytes/paths).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence

import pf_validate_v2_effective_capture as v2


V2_MODULE_SHA256 = "7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9"
NEW_A2_NAMES = (
    "PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv",
    "PF_A2_TARGETS_6564E0_656C50_6FDB40_NONWIRE_DELTA.tsv",
    "PF_A2_TARGET_656690_NONWIRE_DELTA.tsv",
    "PF_A2_ITERATOR_HELPERS_NONWIRE_DELTA.tsv",
)
NEW_A2_SHA256 = {
    "PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv": "f0797f48bfa9115d237bd6e2ebab50e69334c8a05303f66f57bf5ea9b05274dd",
    "PF_A2_TARGETS_6564E0_656C50_6FDB40_NONWIRE_DELTA.tsv": "8c0e3fdd5f0119b5b18eb77aae567f224f2ccebf82033b420e69cb52c542cf02",
    "PF_A2_TARGET_656690_NONWIRE_DELTA.tsv": "f93ca7af682d393abc19628d6291c0f7dd0b04132011a9550b2e4175a1708799",
    "PF_A2_ITERATOR_HELPERS_NONWIRE_DELTA.tsv": "2916eeb565581e75cd1142920435087a19da3e15861427b4cd9f976854d25985",
}
EXPECTED_NEW_REMOVALS = 124
EXPECTED_NEW_SLOT_REMOVALS = 40
EXPECTED_NEW_PER_FILE_REMOVALS = {
    "PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv": 48,
    "PF_A2_TARGETS_6564E0_656C50_6FDB40_NONWIRE_DELTA.tsv": 32,
    "PF_A2_TARGET_656690_NONWIRE_DELTA.tsv": 4,
    "PF_A2_ITERATOR_HELPERS_NONWIRE_DELTA.tsv": 40,
}
EXPECTED_OVERLAY_COUNTS: dict[str, int] = {
    "base_rows": 6931,
    "effective_rows": 8671,
    "generic_changed": 35,
    "generic_removed": 284,
    "slot_added_canonical": 2090,
    "slot_candidates": 56,
    "slot_overlay_removed": 48,
    "slot_removed": 114,
    "string_changed": 408,
    "v3_new_removed": 124,
    "v3_new_slot34_removed": 40,
    "v3_new_v1_removed": 84,
}
EXPECTED_PLAN_CENSUS: dict[str, int] = {
    "APPLICABLE": 620,
    "SCHEMA_NOT_APPLIED": 46,
    "STATIC_OPEN": 372,
}
EXPECTED_RUN_COUNTS: dict[str, int] = {
    "baseline_decompressed_blocks": 41430,
    "baseline_mismatch": 271,
    "baseline_observed_rows": 58,
    "baseline_parse_success": 11903,
    "baseline_pc_blocks": 10462,
    "baseline_schema_not_applied": 0,
    "baseline_static_open": 52501,
    "block_errors": 0,
    "decompressed_blocks": 61611,
    "duplicate_rejected_decompressed_blocks": 4,
    "duplicate_rejected_mismatch": 0,
    "duplicate_rejected_observed_rows": 3,
    "duplicate_rejected_parse_success": 4,
    "duplicate_rejected_pc_blocks": 0,
    "duplicate_rejected_schema_not_applied": 0,
    "duplicate_rejected_static_open": 4,
    "files_with_blocks": 392,
    "framing_unresolved": 0,
    "mismatch": 386,
    "nested_declared": 25228,
    "nested_reached": 24599,
    "nested_unresolved_mismatch": 426,
    "nested_unresolved_not_applied": 0,
    "nested_unresolved_static_open": 203,
    "new_decompressed_blocks": 20181,
    "new_mismatch": 115,
    "new_observed_rows": 50,
    "new_parse_success": 11062,
    "new_pc_blocks": 5211,
    "new_schema_not_applied": 0,
    "new_static_open": 26031,
    "no_runtime_tail": 5542,
    "observed_rows": 66,
    "outer_instances": 77284,
    "parse_success": 22965,
    "pc_blocks": 15673,
    "runtime_zero_tail": 13879,
    "schema_not_applied": 0,
    "static_open": 78532,
    "unique_text_files": 948,
    "unknown_message_ids": 0,
}
EXPECTED_MISMATCH_POINTS: dict[tuple[str, str, str, str], int] = {
    (
        "TeleportVital", "R",
        "BASE:0de634db4db1ff42639f6ded73ce9bfbab8b6a4b50e3ec32c36860dfeb0eb21e;DELTA:88ee2c5ddeac7aff9f0fc73b0eb32f2a77ad060215c59ae11b12d2d364e17563;ORDER:20",
        "STRING_TAG",
    ): 190,
    (
        "TeleportVital", "W",
        "BASE:a9a17c82ae3d6f93644f407b6284ec736cead8f6652e010c5852e4900abed0fa;ORDER:4",
        "TAG",
    ): 188,
    (
        "TradeCmdVital", "W",
        "BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5",
        "TAG",
    ): 6,
    (
        "TradeCmdVital", "W",
        "BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5",
        "TRUNCATED_TAG",
    ): 2,
}
EXPECTED_OUTPUT_SHA256: dict[str, str] = {
    "PF_V2_FIELD_VALIDATION.tsv": "10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806",
    "PF_V3_FIELD_VALIDATION.md": "d0cb385e21297ef8b052895759ece527161c958ab3fb64217aa564e63d1aed59",
}
CANONICAL_TSV = "PF_V2_FIELD_VALIDATION.tsv"
FORBIDDEN_DUPLICATE_TSV = "PF_V3_FIELD_VALIDATION.tsv"
OUTPUT_MD = "PF_V3_FIELD_VALIDATION.md"

V2_A2_OVERLAY_NAMES = (
    "PF_A2_STRING_WIRE_TAG_DELTA.tsv",
    "PF_A2_POST_V1_STATIC_DELTA.tsv",
    "PF_A2_SERIALIZER_SLOT34_DELTA.tsv",
    "PF_A2_POOL_638690_DELTA.tsv",
    "PF_A2_POOL_661FA0_DELTA.tsv",
    "PF_A2_POOL_46F4D0_DELTA.tsv",
    "PF_A2_POOL_46BAA0_READER_DELTA.tsv",
    "PF_TARGET_652A30_A2_DELTA.tsv",
    "PF_TARGETS_694790_6B3440_A2_DELTA.tsv",
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_v2_module() -> None:
    if sha256_path(Path(v2.__file__).resolve()) != V2_MODULE_SHA256:
        raise v2.ValidationError("frozen V2 validator module changed")


def verify_new_inputs(
    external: Path, preview_unpinned: bool
) -> dict[str, str]:
    measured: dict[str, str] = {}
    for name in NEW_A2_NAMES:
        path = external / name
        if not path.exists():
            raise v2.ValidationError(f"missing V3 input: {name}")
        actual = sha256_path(path)
        measured[name] = actual
        expected = NEW_A2_SHA256[name]
        if expected == "__PIN_AFTER_PREVIEW__":
            if not preview_unpinned:
                raise v2.ValidationError(f"unfrozen V3 input: {name}")
        elif actual != expected:
            raise v2.ValidationError(
                f"pinned V3 input changed: {name}: expected {expected}, got {actual}"
            )
    return measured


def prior_a2_targets(external: Path) -> set[tuple[str, str, str]]:
    result: set[tuple[str, str, str]] = set()
    for name in V2_A2_OVERLAY_NAMES:
        headers, rows = v2.read_tsv(external / name)
        if not {"base_file", "base_line", "base_row_key"}.issubset(headers):
            continue
        for row in rows:
            if row["base_file"] == "N/A" or row["base_row_key"] == "N/A":
                continue
            result.add((row["base_file"], row["base_line"], row["base_row_key"]))
    return result


def prior_a2_provenance_keys(external: Path) -> set[str]:
    result: set[str] = set()
    owners: dict[str, str] = {}
    for name in V2_A2_OVERLAY_NAMES:
        headers, rows = v2.read_tsv(external / name)
        for key_column in ("delta_key", "dedup_key"):
            if key_column not in headers:
                continue
            for row in rows:
                value = row[key_column]
                if not value or value == "N/A":
                    continue
                if value in result:
                    raise v2.ValidationError(
                        f"duplicate pre-V3 provenance key: {value}: {owners[value]}/{name}"
                    )
                previous = owners.setdefault(value, name)
                if previous != name:
                    raise v2.ValidationError(
                        f"pre-V3 provenance key collision: {value}: {previous}/{name}"
                    )
                result.add(value)
    return result


def apply_v3_removals(
    external: Path,
) -> tuple[
    list[dict[str, str]],
    dict[tuple[str, str], list[v2.EffectiveField]],
    dict[tuple[str, str, str], list[v2.EffectiveField]],
    dict[str, int],
    dict[str, int],
]:
    registry, effective, candidates, counts = v2.apply_effective_overlays(external)
    prior_targets = prior_a2_targets(external)
    prior_keys = prior_a2_provenance_keys(external)
    seen_targets: set[tuple[str, str, str]] = set()
    seen_delta_keys: set[str] = set()
    per_file: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    removed_fields: list[v2.EffectiveField] = []

    source_tables: dict[str, tuple[list[str], dict[int, dict[str, str]]]] = {}
    for source_name in ("PF_SERIALIZER_FIELDS.tsv", "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"):
        source_headers, source_rows = v2.read_tsv(external / source_name)
        source_tables[source_name] = (
            source_headers,
            {line: row for line, row in enumerate(source_rows, start=2)},
        )

    index: dict[tuple[str, str, str], tuple[tuple[str, str], v2.EffectiveField]] = {}
    for semantic_key, fields in effective.items():
        message, direction = semantic_key
        for field_value in fields:
            key = (message, direction, field_value.evidence_key)
            if key in index:
                raise v2.ValidationError(f"duplicate effective evidence key: {key}")
            index[key] = (semantic_key, field_value)

    for name in NEW_A2_NAMES:
        headers, rows = v2.read_tsv(external / name)
        required = {
            "delta_key", "action", "base_file", "base_line", "base_row_key",
            "base_delta_key", "message", "direction(W/R)", "old_order",
            "old_tag", "old_field_offset", "old_len", "source",
        }
        if not required.issubset(headers):
            raise v2.ValidationError(
                f"{name} missing columns: {sorted(required - set(headers))}"
            )
        for row in rows:
            if row["source"] != "IMAGE" or row["action"] not in {
                "REMOVE_NONWIRE_ROW", "REMOVE_OVERLAY_NONWIRE_ROW"
            }:
                raise v2.ValidationError(f"unsupported V3 row action/source: {name}")
            if row["delta_key"] in seen_delta_keys:
                raise v2.ValidationError(f"duplicate V3 delta_key: {name}")
            if row["delta_key"] in prior_keys:
                raise v2.ValidationError(
                    f"V3 delta_key repeats pre-V3 provenance: {name}:{row['delta_key']}"
                )
            seen_delta_keys.add(row["delta_key"])
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            if target in prior_targets:
                raise v2.ValidationError(
                    f"V3 row duplicates a previously delivered A2 target: {name}:{target}"
                )
            if target in seen_targets:
                raise v2.ValidationError(f"duplicate V3 A2 target: {name}:{target}")
            seen_targets.add(target)

            source_headers, source_by_line = source_tables.get(
                row["base_file"], ([], {})
            )
            try:
                declared_line = int(row["base_line"])
            except ValueError as exc:
                raise v2.ValidationError(
                    f"non-numeric V3 base_line: {name}:{row['base_line']}"
                ) from exc
            source_row = source_by_line.get(declared_line)
            if source_row is None:
                raise v2.ValidationError(
                    f"V3 declared base line is absent: {name}:{row['base_file']}:{declared_line}"
                )
            declared_key = v2.canonical_row_key(source_headers, source_row)
            if declared_key != row["base_row_key"]:
                raise v2.ValidationError(
                    f"V3 base_line/key mismatch: {name}:{row['base_file']}:{declared_line}"
                )

            if row["base_file"] == "PF_SERIALIZER_FIELDS.tsv":
                if row["action"] != "REMOVE_NONWIRE_ROW" or row["base_delta_key"] != "N/A":
                    raise v2.ValidationError(f"invalid V1 removal binding: {name}")
                evidence_key = row["base_row_key"]
                source_counts["v1"] += 1
            elif row["base_file"] == "PF_A2_SERIALIZER_SLOT34_DELTA.tsv":
                if row["action"] != "REMOVE_OVERLAY_NONWIRE_ROW":
                    raise v2.ValidationError(f"invalid slot34 removal binding: {name}")
                if not row["base_delta_key"] or row["base_delta_key"] == "N/A":
                    raise v2.ValidationError(f"missing slot34 base_delta_key: {name}")
                if source_row.get("delta_key") != row["base_delta_key"]:
                    raise v2.ValidationError(
                        f"slot34 declared line/delta-key mismatch: {name}:{declared_line}"
                    )
                evidence_key = row["base_delta_key"]
                source_counts["slot34"] += 1
            else:
                raise v2.ValidationError(
                    f"V3 removal targets unsupported base: {name}:{row['base_file']}"
                )

            lookup = (row["message"], row["direction(W/R)"], evidence_key)
            match = index.get(lookup)
            if match is None:
                raise v2.ValidationError(f"V3 target is not effective/unique: {name}:{lookup}")
            semantic_key, field_value = match
            expected_old = (
                row["old_order"], row["old_tag"], row["old_field_offset"], row["old_len"]
            )
            actual_old = (
                field_value.wire_order, field_value.tag,
                field_value.field_offset, field_value.length,
            )
            if expected_old != actual_old:
                raise v2.ValidationError(
                    f"V3 old-row contract mismatch: {name}:{lookup}: "
                    f"{expected_old} != {actual_old}"
                )
            effective[semantic_key].remove(field_value)
            del index[lookup]
            removed_fields.append(field_value)
            per_file[name] += 1

    total = len(removed_fields)
    if len(seen_targets) != total or len(seen_delta_keys) != total:
        raise v2.ValidationError("V3 removal uniqueness invariant failed")
    if total != EXPECTED_NEW_REMOVALS:
        raise v2.ValidationError(
            f"V3 removal count changed: {total} != {EXPECTED_NEW_REMOVALS}"
        )
    if source_counts["slot34"] != EXPECTED_NEW_SLOT_REMOVALS:
        raise v2.ValidationError(
            f"V3 slot removal count changed: {source_counts['slot34']}"
        )
    if dict(per_file) != EXPECTED_NEW_PER_FILE_REMOVALS:
        raise v2.ValidationError(f"V3 per-file removal census changed: {dict(per_file)}")

    for fields in effective.values():
        fields.sort(key=lambda value: value.sequence)
    v2.validate_effective_tag_census(external, effective)
    counts = dict(counts)
    counts["generic_removed"] += total
    counts["slot_overlay_removed"] += source_counts["slot34"]
    counts["slot_added_canonical"] -= source_counts["slot34"]
    counts["effective_rows"] -= total
    counts["v3_new_removed"] = total
    counts["v3_new_v1_removed"] = source_counts["v1"]
    counts["v3_new_slot34_removed"] = source_counts["slot34"]
    return registry, effective, candidates, counts, dict(per_file)


def build_v3_report(
    output_md: str,
    new_hashes: Mapping[str, str],
    per_file: Mapping[str, int],
) -> str:
    text = output_md
    text = text.replace("A5 V2", "A5 V3")
    text = text.replace("effective V2 A2", "effective V3 A2")
    text = text.replace("# PF V2 effective field validation", "# PF V3 effective field validation")
    text = text.replace("V2 validation", "V3 validation")
    text = text.replace(
        "- observed message/direction rows emitted: ",
        "- observed message/direction rows re-derived (canonical V2 TSV reused, not re-emitted): ",
    )
    text = text.replace(
        "Run `py -3 -B pf_validate_v2_effective_capture.py --check`",
        "Run `py -3 -B pf_validate_v3_effective_capture.py --check`",
    )
    insertion = [
        "",
        "## V3 net-new removal inputs",
        "",
        *[
            f"- `{name}` rows={per_file[name]}; SHA-256 `{new_hashes[name]}`"
            for name in NEW_A2_NAMES
        ],
        "- All rows are `source=IMAGE` removals. No unchanged row is copied, and no V3 base target overlaps a previously delivered A2 overlay.",
        "- The re-derived aggregate TSV is byte-for-byte identical to `PF_V2_FIELD_VALIDATION.tsv`; V3 deliberately emits no `PF_V3_FIELD_VALIDATION.tsv` duplicate. The pinned V2 TSV remains canonical.",
        f"- Frozen V2 validator module SHA-256: `{V2_MODULE_SHA256}`.",
        "",
    ]
    marker = f"- `GameClient.local.bin` size/SHA-256:"
    if marker not in text:
        raise v2.ValidationError("cannot insert V3 exact input bindings")
    text = text.replace(marker, "\n".join(insertion) + marker, 1)
    if v2.RAW_BYTE_RUN_RE.search(text):
        raise v2.ValidationError("raw capture-byte V3 report guard fired")
    return text


def atomic_publish(outputs: Mapping[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    backups: dict[Path, Path | None] = {}
    originals: dict[Path, bytes | None] = {}
    published: list[Path] = []

    def cleanup(paths: Sequence[Path]) -> list[str]:
        errors: list[str] = []
        for path in paths:
            try:
                if path.exists():
                    path.unlink()
            except BaseException as exc:
                errors.append(f"{path.name}: {type(exc).__name__}")
        return errors

    try:
        for destination, text in outputs.items():
            fd, raw_temp = tempfile.mkstemp(
                prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
            )
            temp = Path(raw_temp)
            staged.append((temp, destination))
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            if destination.exists():
                originals[destination] = destination.read_bytes()
                backup_fd, backup_name = tempfile.mkstemp(
                    prefix=f".{destination.name}.", suffix=".rollback",
                    dir=destination.parent,
                )
                os.close(backup_fd)
                backup = Path(backup_name)
                backups[destination] = backup
                shutil.copyfile(destination, backup)
            else:
                originals[destination] = None
                backups[destination] = None
        for temp, destination in staged:
            published.append(destination)
            os.replace(temp, destination)
        for destination, expected_text in outputs.items():
            if destination.read_bytes() != expected_text.encode("utf-8"):
                raise v2.ValidationError(
                    f"post-publish read-back mismatch: {destination.name}"
                )
    except BaseException as failure:
        rollback_errors: list[str] = []
        for destination in reversed(published):
            try:
                backup = backups.get(destination)
                if backup is None:
                    if destination.exists():
                        destination.unlink()
                elif backup.exists():
                    os.replace(backup, destination)
                else:
                    raise v2.ValidationError(f"rollback backup missing: {destination.name}")
                original = originals[destination]
                if original is None:
                    if destination.exists():
                        raise v2.ValidationError(
                            f"rollback failed to remove new target: {destination.name}"
                        )
                elif not destination.exists() or destination.read_bytes() != original:
                    raise v2.ValidationError(f"rollback read-back mismatch: {destination.name}")
            except BaseException as exc:
                rollback_errors.append(f"{destination.name}: {type(exc).__name__}")
        if rollback_errors:
            raise v2.ValidationError(
                "publication failed and rollback is incomplete; backups/temps retained: "
                + "; ".join(rollback_errors)
            ) from failure
        cleanup_errors = cleanup(
            [temp for temp, _destination in staged]
            + [backup for backup in backups.values() if backup is not None]
        )
        if cleanup_errors:
            raise v2.ValidationError(
                "publication rolled back; recovery cleanup incomplete: "
                + "; ".join(cleanup_errors)
            ) from failure
        raise

    cleanup_errors = cleanup(
        [temp for temp, _destination in staged]
        + [backup for backup in backups.values() if backup is not None]
    )
    if cleanup_errors:
        raise v2.ValidationError(
            "outputs committed and verified; cleanup incomplete (no rollback attempted): "
            + "; ".join(cleanup_errors)
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--game-client", type=Path,
        default=Path(__file__).resolve().parents[2] / "GameClient",
    )
    parser.add_argument(
        "--external", type=Path, default=Path(__file__).resolve().parent
    )
    parser.add_argument("--preview-unpinned", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--fail-on-mismatch", action="store_true")
    args = parser.parse_args()
    if args.preview_unpinned and args.check:
        raise v2.ValidationError("--preview-unpinned and --check are mutually exclusive")
    if args.fail_on_mismatch and not args.check:
        raise v2.ValidationError("--fail-on-mismatch requires --check")

    external = args.external.resolve()
    game_client = args.game_client.resolve()
    verify_v2_module()
    image_path = game_client / "GameClient.local.bin"
    if (
        image_path.stat().st_size != v2.EXPECTED_IMAGE_SIZE
        or v2.sha256_file(image_path) != v2.EXPECTED_IMAGE_SHA256
    ):
        raise v2.ValidationError("pinned client image changed")
    old_hashes_before = v2.verify_pinned_inputs(external, False)
    new_hashes_before = verify_new_inputs(external, args.preview_unpinned)

    registry, effective, candidates, overlay_counts, per_file = apply_v3_removals(external)
    v2.validate_ctrace_container_contract(external)
    id_to_name, plans = v2.build_schema_plans(registry, effective, candidates)
    plan_census = dict(Counter(plan.state for plan in plans.values()))
    if not args.preview_unpinned:
        if not EXPECTED_OVERLAY_COUNTS or overlay_counts != EXPECTED_OVERLAY_COUNTS:
            raise v2.ValidationError(f"V3 effective overlay census changed: {overlay_counts}")
        if not EXPECTED_PLAN_CENSUS or plan_census != EXPECTED_PLAN_CENSUS:
            raise v2.ValidationError(f"V3 schema-plan census changed: {plan_census}")
    v2.validate_parser_controls(plans)

    all_inputs, canonical_inputs, baseline_hashes, corpus_digest = v2.load_capture_inventory(
        game_client,
        external / "PF_INPUT_INVENTORY.tsv",
        external / "PF_CAPTURE_DELTA_20260830.inventory.tsv",
    )
    if corpus_digest != v2.EXPECTED_CORPUS_DIGEST:
        raise v2.ValidationError("canonical capture-corpus digest changed")
    baseline_inputs = [item for item in canonical_inputs if item.sha256 in baseline_hashes]
    new_inputs = [item for item in canonical_inputs if item.sha256 not in baseline_hashes]
    if len(baseline_inputs) != 1_189 or len(new_inputs) != 320:
        raise v2.ValidationError("baseline/new canonical partition changed")
    baseline_aggregates, baseline_counts = v2.run_capture_validation(
        baseline_inputs, id_to_name, plans
    )
    new_aggregates, new_counts = v2.run_capture_validation(new_inputs, id_to_name, plans)
    canonical_paths = {item.relative_path.casefold() for item in canonical_inputs}
    duplicate_inputs = [
        item for item in all_inputs if item.relative_path.casefold() not in canonical_paths
    ]
    duplicate_aggregates, duplicate_counts = v2.run_capture_validation(
        duplicate_inputs, id_to_name, plans
    )
    aggregates = v2.merge_aggregates(baseline_aggregates, new_aggregates)
    counts = v2.merge_run_counts(baseline_counts, new_counts)
    v2.validate_ctrace_capture_boundary(aggregates)
    values = v2.outcome_counts(aggregates, counts)
    baseline_values = v2.outcome_counts(baseline_aggregates, baseline_counts)
    new_values = v2.outcome_counts(new_aggregates, new_counts)
    for prefix, subset in (("baseline", baseline_values), ("new", new_values)):
        for name in (
            "parse_success", "static_open", "schema_not_applied", "mismatch",
            "observed_rows", "pc_blocks", "decompressed_blocks",
        ):
            values[f"{prefix}_{name}"] = subset[name]
    duplicate_values = v2.outcome_counts(duplicate_aggregates, duplicate_counts)
    for name in (
        "parse_success", "static_open", "schema_not_applied", "mismatch",
        "observed_rows", "pc_blocks", "decompressed_blocks",
    ):
        values[f"duplicate_rejected_{name}"] = duplicate_values[name]
    mismatch_points = v2.measured_mismatch_points(aggregates)
    if not args.preview_unpinned:
        if not EXPECTED_RUN_COUNTS or values != EXPECTED_RUN_COUNTS:
            raise v2.ValidationError(f"V3 validation run census changed: {values}")
        if mismatch_points != EXPECTED_MISMATCH_POINTS:
            raise v2.ValidationError(f"V3 mismatch-point census changed: {mismatch_points}")

    output_tsv, output_md = v2.build_outputs(
        aggregates, baseline_aggregates, new_aggregates, counts,
        duplicate_aggregates, duplicate_counts, plans, corpus_digest,
        all_inputs, canonical_inputs, old_hashes_before, overlay_counts,
    )
    output_md = build_v3_report(output_md, new_hashes_before, per_file)
    v2.validate_output_mutations(
        output_tsv, aggregates, baseline_aggregates, new_aggregates, plans,
        corpus_digest,
    )

    v2.verify_capture_snapshot(game_client, all_inputs)
    old_hashes_after = v2.verify_pinned_inputs(external, False)
    new_hashes_after = verify_new_inputs(external, args.preview_unpinned)
    if old_hashes_after != old_hashes_before or new_hashes_after != new_hashes_before:
        raise v2.ValidationError("V3 inputs changed during validation")
    verify_v2_module()
    if (
        image_path.stat().st_size != v2.EXPECTED_IMAGE_SIZE
        or v2.sha256_file(image_path) != v2.EXPECTED_IMAGE_SHA256
    ):
        raise v2.ValidationError("client image changed during V3 validation")

    output_hashes = {
        CANONICAL_TSV: v2.sha256_text(output_tsv),
        OUTPUT_MD: v2.sha256_text(output_md),
    }
    if args.preview_unpinned:
        print("NEW_INPUT_SHA256=" + json.dumps(new_hashes_before, sort_keys=True))
        print("RUN_COUNTS=" + json.dumps(values, sort_keys=True))
        print(
            "MISMATCH_POINTS=" + json.dumps(
                {"|".join(key): value for key, value in mismatch_points.items()},
                sort_keys=True,
            )
        )
        print("OUTPUT_SHA256=" + json.dumps(output_hashes, sort_keys=True))
        print("OVERLAY_COUNTS=" + json.dumps(overlay_counts, sort_keys=True))
        print("PLAN_CENSUS=" + json.dumps(plan_census, sort_keys=True))
        print("PER_FILE_REMOVALS=" + json.dumps(per_file, sort_keys=True))
        return 0
    if output_hashes != EXPECTED_OUTPUT_SHA256:
        raise v2.ValidationError(f"V3 validation output hash changed: {output_hashes}")
    canonical_path = external / CANONICAL_TSV
    duplicate_path = external / FORBIDDEN_DUPLICATE_TSV
    if duplicate_path.exists():
        raise v2.ValidationError(
            f"duplicated V3 aggregate TSV must not exist: {FORBIDDEN_DUPLICATE_TSV}"
        )
    if canonical_path.read_bytes() != output_tsv.encode("utf-8"):
        raise v2.ValidationError(
            "V3 aggregate is no longer byte-identical to canonical V2 TSV; "
            "a real V3 delta/output design is required"
        )
    destinations = {external / OUTPUT_MD: output_md}
    if args.check:
        for path, expected_text in destinations.items():
            if not path.exists() or path.read_bytes() != expected_text.encode("utf-8"):
                raise v2.ValidationError(f"published V3 output differs: {path.name}")
    else:
        atomic_publish(destinations)
    if args.fail_on_mismatch and values["mismatch"]:
        raise v2.ValidationError(
            f"capture conformance failed: mismatch={values['mismatch']} "
            f"field_reason_points={len(mismatch_points)}"
        )
    print(
        "unique_contents=%d duplicate_paths=%d pass=%d static_open=%d "
        "schema_not_applied=%d mismatch=%d mismatch_points=%d"
        % (
            len(canonical_inputs), len(all_inputs) - len(canonical_inputs),
            values["parse_success"], values["static_open"],
            values["schema_not_applied"], values["mismatch"], len(mismatch_points),
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except v2.ValidationError as exc:
        raise SystemExit(f"ERROR: {exc}")
