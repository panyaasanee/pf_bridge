#!/usr/bin/env python3
"""Replay A5 against the exact V5 effective schema and publish Markdown only."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pf_validate_v4_effective_capture as v4


v2 = v4.v2

V4_MODULE_SHA256 = "d2e517b4457af2a0f7983d3b60ad88232fad69af392f8287adbe54bef0d2839a"
PINNED_FILES = {
    "PF_V4_FIELD_VALIDATION.md": "4345387b12cbbe048ee3c3a78c43c15d22f680a5082a25bb8de30359aee75ef7",
    "pf_build_v5_invalid_parameter_closure.py": "3f7c6aa4993aa9fa5f1020c0b14fdc119ab568c7e92249003776111355869d73",
    "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv": "f3d877bbc2f3899d650286df6026d44df6691ef23b78ed3492a45da9c076d277",
    "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv": "0d02afcbbab22506ef74a3cf50d88dd1dd5e7a2c8b85f9333397275a4996114a",
    "PF_V5_INVALID_PARAMETER_CLOSURE.md": "12e5790c149324e971d47aae00dca36a7d369ae58ef45755a9422dc97b7f09ff",
    "pf_build_v5_effective_status.py": "6a465acafe4544bec4f3f00674bcabe8aeb51e76fcbe33b691e8effb8e70cc0e",
    "PF_V5_P1_OPEN.tsv": "9ce1310cce89b6f0c72381ffe684e5c6558b4ad7191d298c958bee4d28fd533e",
    "PF_V5_EFFECTIVE_STATUS.md": "b2606434c86cfb74cae1e96a0116b0091fe6a02fa0e07bbe669cdbb99296c021",
}

V5_A2 = "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv"
CANONICAL_TSV = "PF_V2_FIELD_VALIDATION.tsv"
CANONICAL_TSV_SHA256 = "10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806"
OUTPUT_MD = "PF_V5_FIELD_VALIDATION.md"
FORBIDDEN_TSV_NAMES = (
    "PF_V3_FIELD_VALIDATION.tsv",
    "PF_V4_FIELD_VALIDATION.tsv",
    "PF_V5_FIELD_VALIDATION.tsv",
)
PUBLISH_LOCK = ".PF_V5_FIELD_VALIDATION_PUBLISH.lock"
EXPECTED_OUTPUT_MD_SHA256 = "2829e07c097d9dd170f56c2ffb2a8fd38504d9c799d4017513ba61122e4bac1b"

EXPECTED_STORED_ROWS = 8637
EXPECTED_STORED_UNKNOWN = 3943
EXPECTED_LOGICAL_ROWS = 8701
EXPECTED_LOGICAL_UNKNOWN = 3979
EXPECTED_STORED_NUMERIC = 4081
EXPECTED_LOGICAL_NUMERIC = 4103
EXPECTED_PLAN_CENSUS = {
    "APPLICABLE": 628,
    "SCHEMA_NOT_APPLIED": 46,
    "STATIC_OPEN": 364,
}
EXPECTED_REMOVALS = {
    ("ItemMallUpdatePersonalDataVital", "R"): 5,
    ("ItemMallUpdatePersonalDataVital", "W"): 5,
    ("ServerAddedInfoVital", "R"): 5,
    ("ServerAddedInfoVital", "W"): 5,
}
EXPECTED_TARGET_PLANS = {
    ("ItemMallUpdatePersonalDataVital", "R"): (14, 9),
    ("ItemMallUpdatePersonalDataVital", "W"): (14, 9),
    ("ServerAddedInfoVital", "R"): (8, 3),
    ("ServerAddedInfoVital", "W"): (8, 3),
}
V5_REQUIRED_COLUMNS = {
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "direction(W/R)", "old_order", "old_tag",
    "old_field_offset", "old_len", "source",
}
REPORT_CLASSES = (
    "[MEASURED][CAPTURE]",
    "[MEASURED][IMAGE]",
    "[MEASURED][OUTPUT-AUDIT]",
    "[NONCLAIM][LOCAL]",
    "[PROPOSED][LOCAL]",
    "[REPRODUCTION][LOCAL]",
)
REPORT_CLASS_TOKEN_RE = re.compile(
    r"\[[A-Za-z][A-Za-z0-9_+\-]*\]\[[A-Za-z][A-Za-z0-9_+\-]*\]"
)
REPORT_HEADINGS = (
    "# A5 V5 field validation",
    "## Mismatch detail",
    "## V5 replay result",
    "## V5-touched zero observations",
    "## IMAGE schema impact",
    "## Canonical singleton and controls",
    "## Pinned inputs",
    "## Reproduction",
)
REPORT_TABLE_SCAFFOLD = (
    (
        "| evidence class | message | dir | declared field identity | reason | instances |",
        "|---|---|:---:|---|---|---:|",
    ),
    (
        "| evidence class | message | dir | observed frames | observed instances | validator-derived reason |",
        "|---|---|:---:|---:|---:|---|",
    ),
    (
        "| evidence class | message | dir | V4 plan/fields | V5 plan/fields |",
        "|---|---|:---:|---|---|",
    ),
)
REPORT_CLAIM_GRAMMAR = (
    ("mismatch-summary", "[MEASURED][CAPTURE]", "body"),
    ("layer-separation", "[MEASURED][OUTPUT-AUDIT]", "body"),
    *((f"mismatch-row-{index}", "[MEASURED][CAPTURE]", "table") for index in range(1, 5)),
    ("replay-summary", "[MEASURED][CAPTURE]", "bullet"),
    ("replay-inventory", "[MEASURED][CAPTURE]", "bullet"),
    ("replay-equality", "[MEASURED][CAPTURE]", "bullet"),
    *((f"zero-row-{index}", "[MEASURED][CAPTURE]", "table") for index in range(1, 5)),
    ("zero-scope", "[MEASURED][CAPTURE]", "body"),
    ("zero-nonclaim", "[NONCLAIM][LOCAL]", "body"),
    ("zero-output-scope", "[MEASURED][OUTPUT-AUDIT]", "body"),
    ("image-removals", "[MEASURED][IMAGE]", "bullet"),
    ("image-a2", "[MEASURED][IMAGE]", "bullet"),
    ("image-a3", "[MEASURED][IMAGE]", "bullet"),
    ("image-plans", "[MEASURED][IMAGE]", "bullet"),
    *((f"plan-row-{index}", "[MEASURED][IMAGE]", "table") for index in range(1, 5)),
    ("image-no-other-plan", "[MEASURED][IMAGE]", "bullet"),
    ("canonical-singleton", "[MEASURED][OUTPUT-AUDIT]", "bullet"),
    ("controls-mutations", "[MEASURED][OUTPUT-AUDIT]", "bullet"),
    ("controls-transaction", "[MEASURED][OUTPUT-AUDIT]", "bullet"),
    ("controls-residue", "[MEASURED][OUTPUT-AUDIT]", "bullet"),
    ("controls-layer", "[MEASURED][OUTPUT-AUDIT]", "bullet"),
    ("controls-export", "[MEASURED][OUTPUT-AUDIT]", "bullet"),
    *((f"pin:{name}", "[MEASURED][OUTPUT-AUDIT]", "bullet") for name in sorted(PINNED_FILES)),
    ("pin:v4-validator", "[MEASURED][OUTPUT-AUDIT]", "bullet"),
    ("pin:client-image", "[MEASURED][IMAGE]", "bullet"),
    ("reproduction", "[REPRODUCTION][LOCAL]", "body"),
)
REPORT_EXPECTED_CLAIM_BY_SLOT = {
    slot: (expected_class, placement)
    for slot, expected_class, placement in REPORT_CLAIM_GRAMMAR
}


class V5Error(v2.ValidationError):
    pass


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_pins(external: Path) -> dict[str, str]:
    if sha256_path(Path(v4.__file__).resolve()) != V4_MODULE_SHA256:
        raise V5Error("frozen V4 validator module changed")
    measured: dict[str, str] = {}
    for name, expected in PINNED_FILES.items():
        path = external / name
        if not path.is_file():
            raise V5Error(f"missing pinned V5 dependency: {name}")
        actual = sha256_path(path)
        if actual != expected:
            raise V5Error(f"pinned V5 dependency changed: {name}: {actual} != {expected}")
        measured[name] = actual
    canonical = external / CANONICAL_TSV
    if not canonical.is_file() or sha256_path(canonical) != CANONICAL_TSV_SHA256:
        raise V5Error("canonical V2 field-validation TSV changed")
    for name in FORBIDDEN_TSV_NAMES:
        if (external / name).exists():
            raise V5Error(f"duplicate versioned A5 TSV must not exist: {name}")
    v4.verify_pinned_components(external)
    v4.verify_classmap_boundary(external)
    return measured


def run_dependency_checks(external: Path) -> None:
    commands = (
        (
            "pf_build_v5_invalid_parameter_closure.py",
            ["--check"],
            "PASS V5 invalid-parameter component",
        ),
        (
            "pf_build_v5_effective_status.py",
            ["--check"],
            "P1=257/365 OPEN=108",
        ),
    )
    for name, arguments, marker in commands:
        result = subprocess.run(
            [sys.executable, "-B", str(external / name), *arguments],
            cwd=external,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=300,
            check=False,
        )
        try:
            output = result.stdout.decode("ascii", errors="strict")
        except UnicodeDecodeError as exc:
            raise V5Error(f"non-ASCII dependency-check output: {name}") from exc
        if result.returncode or marker not in output:
            tail = " | ".join(output.splitlines()[-4:])
            raise V5Error(f"dependency --check failed: {name}: rc={result.returncode}: {tail}")


def prior_v4_targets_and_keys(external: Path) -> tuple[set[tuple[str, str, str]], set[str]]:
    targets, keys = v4.prior_targets_and_keys(external)
    for name in (v4.DAILY_A2, v4.COMPOSITION_A2):
        headers, rows = v4.strict_read_tsv(external / name)
        required = {"base_file", "base_line", "base_row_key", "delta_key"}
        if not required.issubset(headers):
            raise V5Error(f"prior V4 TSV schema drift: {name}")
        for _line, row in rows:
            target = (row["base_file"], row["base_line"], row["base_row_key"])
            if target in targets or row["delta_key"] in keys:
                raise V5Error(f"prior V4 duplicate target/key: {name}")
            targets.add(target)
            keys.add(row["delta_key"])
    return targets, keys


def expand_with_expected_census(
    stored: Mapping[tuple[str, str], list[v2.EffectiveField]],
    references: Sequence[Mapping[str, str]],
    expected_rows: int,
    expected_unknown: int,
) -> tuple[dict[tuple[str, str], list[v2.EffectiveField]], list[dict[str, str]]]:
    old_rows = v4.EXPECTED_LOGICAL_ROWS
    old_unknown = v4.EXPECTED_LOGICAL_UNKNOWN
    try:
        v4.EXPECTED_LOGICAL_ROWS = expected_rows
        v4.EXPECTED_LOGICAL_UNKNOWN = expected_unknown
        return v4.expand_logical_references(stored, references)
    finally:
        v4.EXPECTED_LOGICAL_ROWS = old_rows
        v4.EXPECTED_LOGICAL_UNKNOWN = old_unknown


def apply_v5_removals(
    external: Path,
) -> tuple[
    list[dict[str, str]],
    dict[tuple[str, str], list[v2.EffectiveField]],
    dict[tuple[str, str, str], list[v2.EffectiveField]],
    dict[str, int],
    list[dict[str, str]],
    dict[tuple[str, str], list[v2.EffectiveField]],
    list[tuple[tuple[str, str], v2.EffectiveField]],
]:
    registry, stored, candidates, counts, references, _details = (
        v4.apply_daily_and_composition(external)
    )
    baseline_stored = {key: list(fields) for key, fields in stored.items()}
    prior_targets, prior_keys = prior_v4_targets_and_keys(external)
    headers, numbered = v4.strict_read_tsv(external / V5_A2)
    if not V5_REQUIRED_COLUMNS.issubset(headers):
        raise V5Error(f"V5 A2 missing columns: {sorted(V5_REQUIRED_COLUMNS-set(headers))}")
    base_headers, base_numbered = v4.strict_read_tsv(external / "PF_SERIALIZER_FIELDS.tsv")
    base_rows = {line: row for line, row in base_numbered}
    index = {
        (message, direction, field.evidence_key): ((message, direction), field)
        for (message, direction), fields in stored.items()
        for field in fields
    }
    seen_targets: set[tuple[str, str, str]] = set()
    seen_keys: set[str] = set()
    per_key: Counter[tuple[str, str]] = Counter()
    removed: list[tuple[tuple[str, str], v2.EffectiveField]] = []
    for input_line, row in numbered:
        label = f"{V5_A2}:{input_line}"
        if (
            row["source"] != "IMAGE"
            or row["action"] != "REMOVE_NONWIRE_ROW"
            or row["base_file"] != "PF_SERIALIZER_FIELDS.tsv"
            or row["base_delta_key"] != "N/A"
        ):
            raise V5Error(f"V5 action/source/base boundary changed: {label}")
        semantic_key = (row["message"], row["direction(W/R)"])
        if semantic_key not in EXPECTED_REMOVALS:
            raise V5Error(f"unexpected V5 message/direction: {label}:{semantic_key}")
        target = (row["base_file"], row["base_line"], row["base_row_key"])
        if target in prior_targets or target in seen_targets:
            raise V5Error(f"V5 duplicate/prior base target: {label}")
        if row["delta_key"] in prior_keys or row["delta_key"] in seen_keys:
            raise V5Error(f"V5 duplicate/prior provenance key: {label}")
        try:
            base_line = int(row["base_line"])
        except ValueError as exc:
            raise V5Error(f"non-numeric V5 base line: {label}") from exc
        base = base_rows.get(base_line)
        if base is None or v2.canonical_row_key(base_headers, base) != row["base_row_key"]:
            raise V5Error(f"V5 exact base line/key drift: {label}")
        lookup = (row["message"], row["direction(W/R)"], row["base_row_key"])
        match = index.pop(lookup, None)
        if match is None:
            raise V5Error(f"V5 target is not still effective/unique: {label}")
        matched_key, field = match
        v4.old_contract(field, row)
        stored[matched_key].remove(field)
        removed.append((matched_key, field))
        per_key[semantic_key] += 1
        seen_targets.add(target)
        seen_keys.add(row["delta_key"])
    if len(numbered) != 20 or dict(per_key) != EXPECTED_REMOVALS:
        raise V5Error(f"V5 exact removal census changed: rows={len(numbered)} per={dict(per_key)}")
    if len(seen_targets) != 20 or len(seen_keys) != 20:
        raise V5Error("V5 removal uniqueness invariant failed")
    for fields in stored.values():
        fields.sort(key=lambda value: value.sequence)
    v2.validate_effective_tag_census(external, stored)
    if (
        v4.total_rows(stored) != EXPECTED_STORED_ROWS
        or v4.total_unknown(stored) != EXPECTED_STORED_UNKNOWN
    ):
        raise V5Error("V5 stored row/UNKNOWN census changed")
    stored_numeric = sum(
        bool(v2.NUMERIC_TAG_RE.fullmatch(field.tag))
        for fields in stored.values() for field in fields
    )
    if stored_numeric != EXPECTED_STORED_NUMERIC:
        raise V5Error(f"V5 stored A3 numeric census changed: {stored_numeric}")
    counts = dict(counts)
    counts["generic_removed"] += 20
    counts["effective_rows"] = EXPECTED_STORED_ROWS
    counts["v5_removed"] = 20
    return registry, stored, candidates, counts, references, baseline_stored, removed


def validate_plan_changes(
    registry: list[dict[str, str]],
    candidates: Mapping[tuple[str, str, str], list[v2.EffectiveField]],
    baseline_stored: Mapping[tuple[str, str], list[v2.EffectiveField]],
    stored: Mapping[tuple[str, str], list[v2.EffectiveField]],
    references: Sequence[Mapping[str, str]],
    removed: Sequence[tuple[tuple[str, str], v2.EffectiveField]],
) -> tuple[
    dict[int, str],
    dict[tuple[str, str], v2.SchemaPlan],
    dict[tuple[str, str], list[v2.EffectiveField]],
]:
    baseline_logical, _ = expand_with_expected_census(
        baseline_stored, references, v4.EXPECTED_LOGICAL_ROWS, v4.EXPECTED_LOGICAL_UNKNOWN
    )
    logical, _ = expand_with_expected_census(
        stored, references, EXPECTED_LOGICAL_ROWS, EXPECTED_LOGICAL_UNKNOWN
    )
    logical_numeric = sum(
        bool(v2.NUMERIC_TAG_RE.fullmatch(field.tag))
        for fields in logical.values() for field in fields
    )
    if logical_numeric != EXPECTED_LOGICAL_NUMERIC:
        raise V5Error(f"V5 logical numeric census changed: {logical_numeric}")
    baseline_ids, baseline_plans = v2.build_schema_plans(registry, baseline_logical, candidates)
    id_to_name, plans = v2.build_schema_plans(registry, logical, candidates)
    if baseline_ids != id_to_name:
        raise V5Error("protocol registry/ID mapping changed across V5")
    census = dict(Counter(plan.state for plan in plans.values()))
    if census != EXPECTED_PLAN_CENSUS:
        raise V5Error(f"V5 plan census changed: {census}")
    changed: set[tuple[str, str]] = set()
    for key in plans:
        before = baseline_plans[key]
        after = plans[key]
        if v2.schema_plan_key(before) != v2.schema_plan_key(after):
            changed.add(key)
    if changed != set(EXPECTED_TARGET_PLANS):
        raise V5Error(f"V5 changed unexpected schema plans: {sorted(changed)}")
    for key, (before_fields, after_fields) in EXPECTED_TARGET_PLANS.items():
        before = baseline_plans[key]
        after = plans[key]
        if (
            before.state != "STATIC_OPEN"
            or len(before.fields) != before_fields
            or after.state != "APPLICABLE"
            or len(after.fields) != after_fields
            or after.blockers
        ):
            raise V5Error(f"V5 target plan transition changed: {key}")
    v4.verify_item_variants(candidates)
    for message in ("ItemAttr", "VitalData"):
        for direction in ("R", "W"):
            key = (message, direction)
            if v2.schema_plan_key(baseline_plans[key]) != v2.schema_plan_key(plans[key]):
                raise V5Error(f"V5 changed protected {message} plan: {direction}")
    v2.validate_parser_controls(plans)

    # Mutation control: restoring one removed blocker must reopen its direction
    # and make the exact plan census fail.
    mutated = {key: list(fields) for key, fields in logical.items()}
    mutated_key, mutated_field = removed[0]
    mutated[mutated_key].append(mutated_field)
    mutated[mutated_key].sort(key=lambda value: value.sequence)
    _ids, mutated_plans = v2.build_schema_plans(registry, mutated, candidates)
    if mutated_plans[mutated_key].state != "STATIC_OPEN":
        raise V5Error("plan mutation control did not restore STATIC_OPEN")
    if dict(Counter(plan.state for plan in mutated_plans.values())) == EXPECTED_PLAN_CENSUS:
        raise V5Error("plan-census mutation control was not detected")
    return id_to_name, plans, logical


def strict_tsv_mutation_controls() -> None:
    with tempfile.TemporaryDirectory(prefix="pf_v5_tsv_controls_") as raw:
        root = Path(raw)
        cases = {
            "duplicate.tsv": "a\ta\n1\t2\n",
            "extra.tsv": "a\tb\n1\t2\t3\n",
            "missing.tsv": "a\tb\n1\n",
            "nul.tsv": "a\tb\n1\t\x00\n",
        }
        for name, text in cases.items():
            path = root / name
            path.write_text(text, encoding="utf-8", newline="")
            try:
                v4.strict_read_tsv(path)
            except v2.ValidationError:
                continue
            raise V5Error(f"strict TSV mutation control accepted: {name}")


def measure_v5_zero_observations(
    canonical: Mapping[tuple[str, str], v2.MessageAggregate],
    duplicates: Mapping[tuple[str, str], v2.MessageAggregate],
) -> list[dict[str, str]]:
    targets = set(EXPECTED_TARGET_PLANS)

    def require_zero(
        label: str,
        measured: Mapping[tuple[str, str], v2.MessageAggregate],
    ) -> None:
        for key in targets:
            aggregate = measured.get(key)
            if aggregate is None:
                continue
            if aggregate.observed_instances or aggregate.observed_frames:
                raise V5Error(
                    f"V5-touched {label} observation is nonzero: "
                    f"{key[0]} {key[1]} frames={len(aggregate.observed_frames)} "
                    f"instances={aggregate.observed_instances}"
                )

    require_zero("canonical", canonical)
    require_zero("duplicate-path", duplicates)
    rows = v4.measure_zero_observations(
        targets, canonical, duplicates
    )
    if len(rows) != 4:
        raise V5Error(f"V5 zero-observation row census changed: {len(rows)}")
    first_key = sorted(EXPECTED_TARGET_PLANS)[0]
    for label, mutate_canonical, frames, instances in (
        ("canonical-instance", True, set(), 1),
        ("canonical-frame", True, {"SYNTHETIC_FRAME_CONTROL"}, 0),
        ("duplicate-instance", False, set(), 1),
        ("duplicate-frame", False, {"SYNTHETIC_FRAME_CONTROL"}, 0),
    ):
        mutated_canonical = dict(canonical)
        mutated_duplicates = dict(duplicates)
        synthetic = v2.MessageAggregate(observed_instances=instances)
        synthetic.observed_frames.update(frames)
        if mutate_canonical:
            mutated_canonical[first_key] = synthetic
        else:
            mutated_duplicates[first_key] = synthetic
        try:
            require_zero("canonical", mutated_canonical)
            require_zero("duplicate-path", mutated_duplicates)
        except V5Error:
            continue
        raise V5Error(f"injected touched observation was accepted: {label}")
    return rows


def require_canonical_output(external: Path, output_tsv: str) -> None:
    encoded = output_tsv.encode("utf-8")
    if hashlib.sha256(encoded).hexdigest() != CANONICAL_TSV_SHA256:
        raise V5Error("V5 aggregate differs from canonical V2 TSV")
    if (external / CANONICAL_TSV).read_bytes() != encoded:
        raise V5Error("canonical V2 TSV byte equality failed")
    for name in FORBIDDEN_TSV_NAMES:
        if (external / name).exists():
            raise V5Error(f"duplicate versioned A5 TSV must not exist: {name}")


def output_drift_mutation_control(external: Path, output_tsv: str) -> None:
    try:
        require_canonical_output(external, output_tsv + "MUTATION")
    except V5Error:
        return
    raise V5Error("output drift mutation control was accepted")


def validate_report_contract(
    text: str,
    line_roles: Mapping[int, tuple[str, str, int]],
    expected_class_by_line: Mapping[int, str],
) -> None:
    lines = text.split("\n")
    expected_lines = set(range(1, len(line_roles) + 1))
    if set(line_roles) != expected_lines or len(lines) != len(line_roles):
        raise V5Error("V5 report line/order census changed")
    claim_lines = {
        line_number
        for line_number, (role, _value, _pipes) in line_roles.items()
        if role.startswith("claim-")
    }
    if set(expected_class_by_line) != claim_lines:
        raise V5Error("V5 per-line expected-class map is incomplete")
    measured_headings = [line for line in lines if line.startswith("#")]
    if measured_headings != list(REPORT_HEADINGS):
        raise V5Error("V5 report heading/section order changed")
    measured_scaffold = [
        line
        for line in lines
        if line.startswith("| evidence class |") or line.startswith("|---")
    ]
    expected_scaffold = [line for pair in REPORT_TABLE_SCAFFOLD for line in pair]
    if measured_scaffold != expected_scaffold:
        raise V5Error("V5 report table scaffold/order changed")

    for line_number, line in enumerate(lines, 1):
        role, expected, pipe_count = line_roles[line_number]
        if role == "exact":
            if line != expected:
                raise V5Error(f"V5 report structural line changed: {line_number}")
            if REPORT_CLASS_TOKEN_RE.search(line):
                raise V5Error(f"V5 report actionable structural line: {line_number}")
            continue
        expected_class = expected_class_by_line[line_number]
        if expected not in REPORT_CLASSES or expected != expected_class:
            raise V5Error(f"V5 report class-map drift: {line_number}")
        prefixes = {
            "claim-body": expected + " ",
            "claim-bullet": "- " + expected + " ",
            "claim-table": "| " + expected + " | ",
        }
        prefix = prefixes.get(role)
        if prefix is None or not line.startswith(prefix) or len(line) == len(prefix):
            raise V5Error(f"V5 report claim placement changed: {line_number}")
        tokens = REPORT_CLASS_TOKEN_RE.findall(line)
        if tokens != [expected]:
            raise V5Error(f"V5 report claim token changed: {line_number}: {tokens}")
        if line.count("|") != pipe_count:
            raise V5Error(f"V5 report table/body shape changed: {line_number}")


def validate_report_contract_mutations(
    text: str,
    line_roles: Mapping[int, tuple[str, str, int]],
    expected_class_by_line: Mapping[int, str],
) -> None:
    original = text.split("\n")

    def require_rejected(mutated: list[str], label: str) -> None:
        try:
            validate_report_contract(
                "\n".join(mutated), line_roles, expected_class_by_line
            )
        except V5Error:
            return
        raise V5Error(f"V5 report-contract mutation was accepted: {label}")

    actionable = sorted(expected_class_by_line)
    if not actionable:
        raise V5Error("V5 report has no actionable claim lines")
    for line_number in actionable:
        index = line_number - 1
        expected = expected_class_by_line[line_number]
        alternative = next(value for value in REPORT_CLASSES if value != expected)
        mutations = {
            "removed-token": original[index].replace(expected, "", 1),
            "extra-token": original[index].replace(
                expected, expected + " " + alternative, 1
            ),
            "lowercase-token": original[index].replace(expected, expected.lower(), 1),
            "mixed-layer-token": original[index].replace(
                expected, "[MEASURED][IMAGE+CAPTURE]", 1
            ),
        }
        for label, mutated_line in mutations.items():
            mutated = list(original)
            mutated[index] = mutated_line
            require_rejected(mutated, f"{label}-line-{line_number}")
        for wrong_class in REPORT_CLASSES:
            if wrong_class == expected:
                continue
            mutated = list(original)
            mutated[index] = mutated[index].replace(expected, wrong_class, 1)
            require_rejected(
                mutated,
                f"wrong-allowed-class-{wrong_class}-line-{line_number}",
            )

    removed_line = list(original)
    removed_line.pop(actionable[0] - 1)
    require_rejected(removed_line, "removed-actionable-line")
    extra_line = list(original)
    extra_line.insert(actionable[0], original[actionable[0] - 1])
    require_rejected(extra_line, "extra-actionable-line")

    heading_lines = [
        line_number
        for line_number, (role, value, _pipes) in line_roles.items()
        if role == "exact" and value.startswith("#")
    ]
    if len(heading_lines) < 2:
        raise V5Error("V5 report heading-control census is too small")
    actionable_heading = list(original)
    heading_index = heading_lines[0] - 1
    actionable_heading[heading_index] += " [MEASURED][CAPTURE] measured=1"
    require_rejected(actionable_heading, "actionable-heading")
    reordered_headings = list(original)
    first_heading = heading_lines[0] - 1
    second_heading = heading_lines[1] - 1
    reordered_headings[first_heading], reordered_headings[second_heading] = (
        reordered_headings[second_heading],
        reordered_headings[first_heading],
    )
    require_rejected(reordered_headings, "reordered-sections")

    table_line = next(
        line_number
        for line_number, (role, _value, _pipes) in line_roles.items()
        if role == "claim-table"
    )
    malformed_table = list(original)
    parts = malformed_table[table_line - 1].split(" | ")
    if len(parts) < 4:
        raise V5Error("V5 table-shape mutation fixture changed")
    parts.pop(-2)
    malformed_table[table_line - 1] = " | ".join(parts)
    require_rejected(malformed_table, "missing-table-cell")


def report_text(
    values: Mapping[str, int],
    mismatch_points: Mapping[tuple[str, str, str, str], int],
    zero_rows: Sequence[Mapping[str, str]],
    component_hashes: Mapping[str, str],
    corpus_digest: str,
    all_inputs: int,
    canonical_inputs: int,
) -> str:
    locations = {
        (message, direction, identity)
        for message, direction, identity, _reason in mismatch_points
    }
    lines: list[str] = []
    line_roles: dict[int, tuple[str, str, int]] = {}
    expected_class_by_line: dict[int, str] = {}
    claim_slots: list[str] = []
    if len(REPORT_EXPECTED_CLAIM_BY_SLOT) != len(REPORT_CLAIM_GRAMMAR):
        raise V5Error("duplicate V5 report claim-grammar slot")

    def add_exact(value: str) -> None:
        if "\n" in value:
            raise V5Error("V5 report structural line contains a newline")
        lines.append(value)
        line_roles[len(lines)] = ("exact", value, value.count("|"))

    def add_claim(
        slot: str,
        actual_class: str,
        value: str,
        placement: str,
    ) -> None:
        expected = REPORT_EXPECTED_CLAIM_BY_SLOT.get(slot)
        if expected is None or slot in claim_slots:
            raise V5Error(f"unknown/duplicate V5 report claim slot: {slot}")
        expected_class, expected_placement = expected
        if actual_class not in REPORT_CLASSES:
            raise V5Error(f"unsupported V5 report class: {actual_class}")
        if placement != expected_placement or placement == "table":
            raise V5Error(f"V5 report claim placement drift: {slot}")
        if "\n" in value or REPORT_CLASS_TOKEN_RE.search(value):
            raise V5Error("V5 report claim payload contains a class token/newline")
        prefixes = {
            "body": actual_class + " ",
            "bullet": "- " + actual_class + " ",
        }
        if placement not in prefixes or not value:
            raise V5Error("invalid V5 report body-claim placement")
        line = prefixes[placement] + value
        lines.append(line)
        line_roles[len(lines)] = (
            "claim-" + placement,
            expected_class,
            line.count("|"),
        )
        expected_class_by_line[len(lines)] = expected_class
        claim_slots.append(slot)

    def add_table_claim(
        slot: str,
        actual_class: str,
        cells: Sequence[str],
    ) -> None:
        expected = REPORT_EXPECTED_CLAIM_BY_SLOT.get(slot)
        if expected is None or slot in claim_slots:
            raise V5Error(f"unknown/duplicate V5 report table slot: {slot}")
        expected_class, expected_placement = expected
        if (
            actual_class not in REPORT_CLASSES
            or expected_placement != "table"
            or not cells
        ):
            raise V5Error("invalid V5 report table claim")
        if any("\n" in cell or "|" in cell for cell in cells):
            raise V5Error("V5 report table cell contains a delimiter/newline")
        line = "| " + actual_class + " | " + " | ".join(cells) + " |"
        lines.append(line)
        line_roles[len(lines)] = (
            "claim-table",
            expected_class,
            line.count("|"),
        )
        expected_class_by_line[len(lines)] = expected_class
        claim_slots.append(slot)

    add_exact("# A5 V5 field validation")
    add_exact("")
    add_claim(
        "mismatch-summary",
        "[MEASURED][CAPTURE]",
        f"RED: full replay of the SHA-256 content-deduplicated corpus against the exact V5 logical plan measured {values['mismatch']} mismatch instances at {len(locations)} field locations and {len(mismatch_points)} field+reason points.",
        "body",
    )
    add_claim(
        "layer-separation",
        "[MEASURED][OUTPUT-AUDIT]",
        "Layer-separation controls did not edit IMAGE rows to fit CAPTURE observations.",
        "body",
    )
    add_exact("")
    add_exact("## Mismatch detail")
    add_exact("")
    add_exact("| evidence class | message | dir | declared field identity | reason | instances |")
    add_exact("|---|---|:---:|---|---|---:|")
    for index, ((message, direction, identity, reason), count) in enumerate(
        sorted(mismatch_points.items()), 1
    ):
        add_table_claim(
            f"mismatch-row-{index}",
            "[MEASURED][CAPTURE]",
            (f"`{message}`", direction, f"`{identity}`", f"`{reason}`", str(count)),
        )

    add_exact("")
    add_exact("## V5 replay result")
    add_exact("")
    add_claim(
        "replay-summary",
        "[MEASURED][CAPTURE]",
        f"Parser replay measured pass={values['parse_success']}; static-open={values['static_open']}; schema-not-applied={values['schema_not_applied']}; mismatch={values['mismatch']}; observed message/direction rows={values['observed_rows']}.",
        "bullet",
    )
    add_claim(
        "replay-inventory",
        "[MEASURED][CAPTURE]",
        f"Full-file SHA-256 inventory control measured {all_inputs} paths, {canonical_inputs} canonical contents, and {all_inputs-canonical_inputs} rejected exact-content duplicate paths; corpus digest=`{corpus_digest}`.",
        "bullet",
    )
    add_claim(
        "replay-equality",
        "[MEASURED][CAPTURE]",
        "Exact outcome and mismatch-point equality controls measured no aggregate change from V4.",
        "bullet",
    )

    add_exact("")
    add_exact("## V5-touched zero observations")
    add_exact("")
    add_exact("| evidence class | message | dir | observed frames | observed instances | validator-derived reason |")
    add_exact("|---|---|:---:|---:|---:|---|")
    for index, item in enumerate(zero_rows, 1):
        add_table_claim(
            f"zero-row-{index}",
            "[MEASURED][CAPTURE]",
            (
                f"`{item['message']}`",
                item["direction"],
                item["observed_frames"],
                item["observed_instances"],
                f"`{item['reason']}`",
            ),
        )
    add_exact("")
    add_claim(
        "zero-scope",
        "[MEASURED][CAPTURE]",
        "Scope control recorded no reached outer or nested registry ID for each listed message+direction in this canonical corpus replay.",
        "body",
    )
    add_claim(
        "zero-nonclaim",
        "[NONCLAIM][LOCAL]",
        "Zero observation does not prove absence from other runtime sessions or from bytes beyond an earlier unresolved parse boundary.",
        "body",
    )
    add_claim(
        "zero-output-scope",
        "[MEASURED][OUTPUT-AUDIT]",
        "The table contains exactly the four V5-touched rows; the eight historical V4 zero-observation rows are not copied here.",
        "body",
    )

    add_exact("")
    add_exact("## IMAGE schema impact")
    add_exact("")
    add_claim(
        "image-removals",
        "[MEASURED][IMAGE]",
        "Exact full-row-key replay consumed 20/20 unique still-effective V1 rows: five per direction for ServerAddedInfoVital and ItemMallUpdatePersonalDataVital; all rows are source=IMAGE REMOVE_NONWIRE_ROW actions.",
        "bullet",
    )
    add_claim(
        "image-a2",
        "[MEASURED][IMAGE]",
        f"Stored/reference A2 measured {EXPECTED_STORED_ROWS} rows and {EXPECTED_STORED_UNKNOWN} UNKNOWN; validation-only logical view measured {EXPECTED_LOGICAL_ROWS} rows and {EXPECTED_LOGICAL_UNKNOWN} UNKNOWN.",
        "bullet",
    )
    add_claim(
        "image-a3",
        "[MEASURED][IMAGE]",
        f"Numeric-tag census measured stored A3={EXPECTED_STORED_NUMERIC} and validation-only logical={EXPECTED_LOGICAL_NUMERIC}; no A3 row is written.",
        "bullet",
    )
    add_claim(
        "image-plans",
        "[MEASURED][IMAGE]",
        f"Exact schema planner measured APPLICABLE={EXPECTED_PLAN_CENSUS['APPLICABLE']}; STATIC_OPEN={EXPECTED_PLAN_CENSUS['STATIC_OPEN']}; SCHEMA_NOT_APPLIED={EXPECTED_PLAN_CENSUS['SCHEMA_NOT_APPLIED']}.",
        "bullet",
    )
    add_exact("")
    add_exact("| evidence class | message | dir | V4 plan/fields | V5 plan/fields |")
    add_exact("|---|---|:---:|---|---|")
    for index, (key, (before, after)) in enumerate(
        sorted(EXPECTED_TARGET_PLANS.items()), 1
    ):
        add_table_claim(
            f"plan-row-{index}",
            "[MEASURED][IMAGE]",
            (
                f"`{key[0]}`",
                key[1],
                f"STATIC_OPEN / {before}",
                f"APPLICABLE / {after}",
            ),
        )
    add_exact("")
    add_claim(
        "image-no-other-plan",
        "[MEASURED][IMAGE]",
        "Exact plan-key comparison measured no other plan change. ItemAttr candidate schemas remain separate at 26 and 30 rows; VitalData identity activates no V5 A5 schema.",
        "bullet",
    )

    add_exact("")
    add_exact("## Canonical singleton and controls")
    add_exact("")
    add_claim(
        "canonical-singleton",
        "[MEASURED][OUTPUT-AUDIT]",
        f"UTF-8 byte equality and SHA-256 measured the generated aggregate identical to `{CANONICAL_TSV}` (`{CANONICAL_TSV_SHA256}`); no V3, V4, or V5 duplicate A5 TSV exists.",
        "bullet",
    )
    add_claim(
        "controls-mutations",
        "[MEASURED][OUTPUT-AUDIT]",
        "Mutation controls rejected duplicate-header and extra/missing/NUL-cell TSVs; detected restored-row plan/census drift; rejected canonical and duplicate-path instance-only/frame-only touched observations; and detected aggregate output drift. Current-state exactness controls separately enforce unique V5 targets/keys, still-effective base/old contracts, 20 complete removals, ItemAttr/VitalData boundaries, canonical aggregate equality, and exact mismatch-point carry-forward.",
        "bullet",
    )
    add_claim(
        "controls-transaction",
        "[MEASURED][OUTPUT-AUDIT]",
        "Held-handle transaction controls denied a second lock acquisition and pathname unlink/replace while held, verified release did not affect a foreign inode, and injected an interrupt after destination replace that restored prior output or removed newly-created output with zero transaction residue.",
        "bullet",
    )
    add_claim(
        "controls-residue",
        "[MEASURED][OUTPUT-AUDIT]",
        "Casefold positive/negative controls detect the V5 lock plus temporary/rollback publication residue without treating the final Markdown or forbidden TSV name as transaction residue.",
        "bullet",
    )
    add_claim(
        "controls-layer",
        "[MEASURED][OUTPUT-AUDIT]",
        "Source-column, independent-plan, and aggregate controls keep IMAGE structure separate from CAPTURE observations; no DUMP or DATA fact is merged.",
        "bullet",
    )
    add_claim(
        "controls-export",
        "[MEASURED][OUTPUT-AUDIT]",
        "Report schema and raw-byte regex controls export no capture payload, value, path, or hexdump.",
        "bullet",
    )

    add_exact("")
    add_exact("## Pinned inputs")
    add_exact("")
    for name in sorted(component_hashes):
        add_claim(
            f"pin:{name}",
            "[MEASURED][OUTPUT-AUDIT]",
            f"`{name}` SHA-256 `{component_hashes[name]}`.",
            "bullet",
        )
    add_claim(
        "pin:v4-validator",
        "[MEASURED][OUTPUT-AUDIT]",
        f"frozen V4 validator SHA-256 `{V4_MODULE_SHA256}`.",
        "bullet",
    )
    add_claim(
        "pin:client-image",
        "[MEASURED][IMAGE]",
        f"GameClient.local.bin size={v2.EXPECTED_IMAGE_SIZE}; SHA-256 `{v2.EXPECTED_IMAGE_SHA256}`.",
        "bullet",
    )

    add_exact("")
    add_exact("## Reproduction")
    add_exact("")
    add_claim(
        "reproduction",
        "[REPRODUCTION][LOCAL]",
        "Run `py -3 -B pf_validate_v5_effective_capture.py --check` for integrity replay. Add `--fail-on-mismatch` for the deliberately red conformance gate. Direct `py -3 -B` execution is the supported invocation; module import is not claimed.",
        "body",
    )
    add_exact("")

    expected_slots = tuple(slot for slot, _class, _placement in REPORT_CLAIM_GRAMMAR)
    if tuple(claim_slots) != expected_slots:
        raise V5Error("V5 report claim slot/section order changed")

    text = "\n".join(lines)
    validate_report_contract(text, line_roles, expected_class_by_line)
    validate_report_contract_mutations(text, line_roles, expected_class_by_line)
    if v2.RAW_BYTE_RUN_RE.search(text):
        raise V5Error("raw capture-byte V5 report guard fired")
    return text


def is_publication_residue_name(value: str) -> bool:
    lock = PUBLISH_LOCK.casefold()
    output_prefix = f".{OUTPUT_MD}.".casefold()
    name = value.casefold()
    return name == lock or (
        name.startswith(output_prefix)
        and (name.endswith(".tmp") or name.endswith(".rollback"))
    )


def publication_residue(external: Path) -> list[str]:
    residue: list[str] = []
    for child in external.iterdir():
        if is_publication_residue_name(child.name):
            residue.append(child.name)
    return sorted(residue, key=str.casefold)


def casefold_residue_mutation_controls() -> None:
    should_match = (
        PUBLISH_LOCK,
        PUBLISH_LOCK.swapcase(),
        ".PF_V5_FIELD_VALIDATION.md.synthetic.tmp",
        ".pf_v5_field_validation.MD.synthetic.ROLLBACK",
    )
    should_not_match = (
        OUTPUT_MD,
        "PF_V5_FIELD_VALIDATION.tsv",
        ".PF_V5_FIELD_VALIDATION.md.synthetic.safe",
    )
    if any(not is_publication_residue_name(name) for name in should_match):
        raise V5Error("casefold publication-residue positive control failed")
    if any(is_publication_residue_name(name) for name in should_not_match):
        raise V5Error("casefold publication-residue negative control failed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--game-client", type=Path,
        default=Path(__file__).resolve().parents[2] / "GameClient",
    )
    parser.add_argument("--external", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--preview-unpinned", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--fail-on-mismatch", action="store_true")
    args = parser.parse_args()
    if args.preview_unpinned and args.check:
        raise V5Error("--preview-unpinned and --check are mutually exclusive")
    if args.fail_on_mismatch and not args.check:
        raise V5Error("--fail-on-mismatch requires --check")

    external = args.external.resolve()
    game_client = args.game_client.resolve()
    residue_before = publication_residue(external)
    if residue_before:
        raise V5Error("stale/foreign V5 publication recovery state: " + ",".join(residue_before))

    # Reuse the frozen, tested held-handle transaction implementation with a
    # V5-specific lock name in this process only.
    v4.PUBLISH_LOCK = PUBLISH_LOCK
    v4.validate_atomic_publish_controls()
    strict_tsv_mutation_controls()
    casefold_residue_mutation_controls()

    image = game_client / "GameClient.local.bin"
    image_before = sha256_path(image)
    if image.stat().st_size != v2.EXPECTED_IMAGE_SIZE or image_before != v2.EXPECTED_IMAGE_SHA256:
        raise V5Error("pinned client image changed")
    old_hashes_before = v2.verify_pinned_inputs(external, False)
    v3_hashes_before = v4.v3.verify_new_inputs(external, False)
    pin_hashes_before = verify_pins(external)
    run_dependency_checks(external)

    registry, stored, candidates, overlay_counts, references, baseline_stored, removed = (
        apply_v5_removals(external)
    )
    id_to_name, plans, logical = validate_plan_changes(
        registry, candidates, baseline_stored, stored, references, removed
    )

    all_inputs, canonical_inputs, baseline_hashes, corpus_digest = v2.load_capture_inventory(
        game_client,
        external / "PF_INPUT_INVENTORY.tsv",
        external / "PF_CAPTURE_DELTA_20260830.inventory.tsv",
    )
    if corpus_digest != v2.EXPECTED_CORPUS_DIGEST:
        raise V5Error("canonical capture-corpus digest changed")
    baseline_inputs = [item for item in canonical_inputs if item.sha256 in baseline_hashes]
    new_inputs = [item for item in canonical_inputs if item.sha256 not in baseline_hashes]
    if len(baseline_inputs) != 1189 or len(new_inputs) != 320:
        raise V5Error("baseline/new canonical partition changed")
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
    if values != v4.v3.EXPECTED_RUN_COUNTS:
        raise V5Error(f"V5 capture run census changed: {values}")
    mismatch_points = v2.measured_mismatch_points(aggregates)
    if mismatch_points != v4.v3.EXPECTED_MISMATCH_POINTS:
        raise V5Error(f"V5 mismatch-point census changed: {mismatch_points}")
    zero_rows = measure_v5_zero_observations(aggregates, duplicate_aggregates)

    output_tsv, _discarded_md = v2.build_outputs(
        aggregates, baseline_aggregates, new_aggregates, counts,
        duplicate_aggregates, duplicate_counts, plans, corpus_digest,
        all_inputs, canonical_inputs, old_hashes_before, overlay_counts,
    )
    v2.validate_output_mutations(
        output_tsv, aggregates, baseline_aggregates, new_aggregates, plans, corpus_digest
    )
    require_canonical_output(external, output_tsv)
    output_drift_mutation_control(external, output_tsv)
    output_md = report_text(
        values, mismatch_points, zero_rows, pin_hashes_before, corpus_digest,
        len(all_inputs), len(canonical_inputs),
    )
    output_hash = v2.sha256_text(output_md)

    v2.verify_capture_snapshot(game_client, all_inputs)
    old_hashes_after = v2.verify_pinned_inputs(external, False)
    v3_hashes_after = v4.v3.verify_new_inputs(external, False)
    pin_hashes_after = verify_pins(external)
    image_after = sha256_path(image)
    if (
        old_hashes_after != old_hashes_before
        or v3_hashes_after != v3_hashes_before
        or pin_hashes_after != pin_hashes_before
    ):
        raise V5Error("V5 inputs changed during validation")
    if image_after != image_before:
        raise V5Error("client image changed during V5 validation")

    if args.preview_unpinned:
        print("OUTPUT_MD_SHA256=" + output_hash)
        print(
            "CENSUS="
            + json.dumps(
                {
                    "stored_rows": v4.total_rows(stored),
                    "stored_unknown": v4.total_unknown(stored),
                    "logical_rows": v4.total_rows(logical),
                    "logical_unknown": v4.total_unknown(logical),
                    "plans": dict(Counter(plan.state for plan in plans.values())),
                    "zero_observation_rows": len(zero_rows),
                },
                sort_keys=True,
            )
        )
        return 0
    if EXPECTED_OUTPUT_MD_SHA256 == "__PIN_AFTER_PREVIEW__":
        raise V5Error("V5 report hash is not pinned")
    if output_hash != EXPECTED_OUTPUT_MD_SHA256:
        raise V5Error(f"V5 report hash changed: {output_hash} != {EXPECTED_OUTPUT_MD_SHA256}")

    destination = external / OUTPUT_MD
    if args.check:
        if not destination.is_file() or destination.read_bytes() != output_md.encode("utf-8"):
            raise V5Error(f"published V5 output differs: {OUTPUT_MD}")
    else:
        v4.atomic_publish(destination, output_md)
    residue_after = publication_residue(external)
    if residue_after:
        raise V5Error("V5 publication residue remains: " + ",".join(residue_after))
    if args.fail_on_mismatch and values["mismatch"]:
        raise V5Error(
            f"capture conformance failed: mismatch={values['mismatch']} "
            f"field_reason_points={len(mismatch_points)}"
        )
    print(
        "unique_contents=%d duplicate_paths=%d pass=%d static_open=%d "
        "schema_not_applied=%d mismatch=%d mismatch_points=%d plans=%d/%d/%d"
        % (
            len(canonical_inputs), len(all_inputs) - len(canonical_inputs),
            values["parse_success"], values["static_open"],
            values["schema_not_applied"], values["mismatch"], len(mismatch_points),
            EXPECTED_PLAN_CENSUS["APPLICABLE"],
            EXPECTED_PLAN_CENSUS["STATIC_OPEN"],
            EXPECTED_PLAN_CENSUS["SCHEMA_NOT_APPLIED"],
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (V5Error, v2.ValidationError) as exc:
        raise SystemExit(f"ERROR: {exc}")
