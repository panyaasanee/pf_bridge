#!/usr/bin/env python3
"""Verify the GT-047 field_offset guard patch (8 checks, ASCII output only).

Run from anywhere; pass --external to point at the directory that holds
PF_PROTOCOL_REGISTRY.tsv / PF_SERIALIZER_FIELDS.tsv / PF_TAG_CENSUS.tsv
and --validator at the patched pf_validate_capture_fields.py.  Exit 0 =
all checks pass.  No capture corpus is needed: only the schema layer is
exercised, which is exactly the layer the guard lives in.

The first output line echoes the sha256 of the validator file actually
loaded; quote that line in any report so "the mutation went red" is
provably a statement about THIS file.
"""
import argparse
import hashlib
import importlib.util
import sys
from pathlib import Path


def mutate_and_expect_red(v, reg, fld, tag, label, selector, column, value):
    mutated = [dict(r) for r in fld]
    row = next(r for r in mutated if selector(r))
    row[column] = value
    try:
        v.build_schemas(reg, mutated, tag)
    except v.ValidationError as exc:
        print("%s REJECTED: %s" % (label, ascii(str(exc))))
        return True
    print("%s FAILED: mutation accepted" % label)
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external", type=Path, required=True)
    parser.add_argument(
        "--validator",
        type=Path,
        default=Path(__file__).resolve().parent / "pf_validate_capture_fields.py",
    )
    args = parser.parse_args()
    validator_path = args.validator.resolve()
    digest = hashlib.sha256(validator_path.read_bytes()).hexdigest()
    print("validator sha256=%s bytes=%d" % (digest, validator_path.stat().st_size))
    spec = importlib.util.spec_from_file_location("pfv", validator_path)
    v = importlib.util.module_from_spec(spec)
    sys.modules["pfv"] = v
    spec.loader.exec_module(v)
    ext = args.external.resolve()
    reg = v.read_tsv(ext / "PF_PROTOCOL_REGISTRY.tsv")
    fld = v.read_tsv(ext / "PF_SERIALIZER_FIELDS.tsv")
    tag = v.read_tsv(ext / "PF_TAG_CENSUS.tsv")

    id_to_name, _schemas, static_open = v.build_schemas(reg, fld, tag)
    print(
        "T1 pristine build_schemas: PASS (messages=%d static_open=%d)"
        % (len(id_to_name), len(static_open))
    )

    checks = [
        (
            "T2 GT-047 job-3 mutation (TargetPosVital:W:1 +0x14 -> +0x99)",
            lambda r: r["message"] == "TargetPosVital"
            and r["direction(W/R)"] == "W"
            and r["order"] == "1",
            "field_offset",
            "+0x99",
        ),
        (
            "T3 static-open flip (field_offset -> UNKNOWN(+0x99))",
            lambda r: r["message"] == "TargetPosVital"
            and r["direction(W/R)"] == "W"
            and r["order"] == "1",
            "field_offset",
            "UNKNOWN(+0x99)",
        ),
        (
            "T4 one-leg embedded-VA edit (ReliveVital:W:1)",
            lambda r: r["message"] == "ReliveVital"
            and r["direction(W/R)"] == "W"
            and r["order"] == "1",
            "field_offset",
            "STACK@0x00DEADBE+0x14",
        ),
        (
            "T5 one-leg span_sha256 tamper (TargetPosVital:W:1)",
            lambda r: r["message"] == "TargetPosVital"
            and r["direction(W/R)"] == "W"
            and r["order"] == "1",
            "span_sha256",
            "0" * 64,
        ),
    ]
    for label, selector, column, value in checks:
        if not mutate_and_expect_red(v, reg, fld, tag, label, selector, column, value):
            return 1

    mutated = [dict(r) for r in fld]
    for row in mutated:
        if row["message"] == "Activity_BasicVital":
            row["tag"] = "EMPTY"
            row["field_offset"] = "N/A"
            row["len"] = "0"
        elif row["message"] == "Attribute" and row["direction(W/R)"] == "W":
            row["field_offset"] = "UNKNOWN(+0x99)"
    try:
        v.build_schemas(reg, mutated, tag)
        print("T6 FAILED: count-preserving membership swap accepted")
        return 1
    except v.ValidationError as exc:
        print(
            "T6 count-preserving static-open membership swap REJECTED: %s"
            % ascii(str(exc))
        )

    v.validate_parser_regressions()
    v.validate_schema_mutation_regressions(reg, fld, tag)
    print("T7 parser + schema mutation self-tests: PASS")

    orig = v.validate_field_offset_mirror
    v.validate_field_offset_mirror = lambda *a, **k: None
    try:
        v.validate_schema_mutation_regressions(reg, fld, tag)
        print("T8 FAILED: self-test did not detect disabled guard")
        return 1
    except v.ValidationError as exc:
        print("T8 self-test red when guard disabled: %s" % ascii(str(exc)))
    finally:
        v.validate_field_offset_mirror = orig
    print("ALL 8 CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
