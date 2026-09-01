#!/usr/bin/env python3
"""Fail-closed audit and hash manifest for the frozen PF external v1 box."""

from __future__ import annotations

import csv
import hashlib
import os
import re
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ALLOWED_SOURCES = frozenset({"IMAGE", "DUMP", "CAPTURE", "DATA"})
IMAGE_SHA = "9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623"
OTHER_IMAGE_SHA = "C528BF43070E2789170F41B6E3E28CCEC6B57BDC594EE73DFA061188A5D1E4BD"

ARTIFACTS = (
    "PF_PROTOCOL_REGISTRY.tsv",
    "PF_PROTOCOL_REGISTRY.md",
    "PF_SERIALIZER_FIELDS.tsv",
    "PF_SERIALIZER_FIELDS.md",
    "PF_TAG_CENSUS.tsv",
    "pf_extract_protocol.py",
    "PF_EXTERNAL_REPORT.md",
    "PF_INPUT_INVENTORY.tsv",
    "PF_INPUT_INVENTORY.md",
    "pf_inventory_inputs.py",
    "PF_PROTOCOL_PRIORITY.tsv",
    "PF_PROTOCOL_PRIORITY.md",
    "pf_build_priority.py",
    "PF_FIELD_VALIDATION.tsv",
    "PF_FIELD_VALIDATION.md",
    "pf_validate_capture_fields.py",
    "PF_RUNTIME_CLASSMAP.tsv",
    "PF_RUNTIME_CLASSMAP.md",
    "pf_extract_dump_rtti.py",
    "PF_DATA_EVIDENCE.tsv",
    "PF_DATA_EVIDENCE.md",
    "pf_extract_data_evidence.py",
    "PF_ERRATUM_TWO_IMAGES.md",
    "PF_DUMP_REQUEST.md",
    "PF_HANDOFF_V1.md",
    "pf_build_v1_manifest.py",
)

# Freeze oracle: these hashes were measured only after the final A4/A5 run,
# corrective reviews, report addendum, erratum, dump request, and handoff were
# complete.  The auditor itself is reviewed/frozen externally because a file
# cannot safely pin its own hash.
EXPECTED_ARTIFACT_HASHES = {
    "pf_build_priority.py": "77C1E0EFFA3CDB9D89AB3B2F3E1FF40F598EECEDAE5A50367E5BA7E007FBAA5B",
    "PF_DATA_EVIDENCE.md": "91B8D611F82D23DFD68009229C772AACC91A48D2B879FBE7D808016F7E1102B2",
    "PF_DATA_EVIDENCE.tsv": "FBCD7BF14FD33C7340C6FD70F4A0AA5F1A6F7719C429335540383EAB1CCF5B1F",
    "PF_DUMP_REQUEST.md": "5FCE70ADF071120F8C7CD9739AC52B835D5E4EE9C0F70995DC295FCA8199201D",
    "PF_ERRATUM_TWO_IMAGES.md": "8785B715E69399162DBEDD786C63AD914F87C1F1F4DAB5CEB08CC73B60244A7E",
    "PF_EXTERNAL_REPORT.md": "302AABD0882F3A06E2FF0EFE322409FEDDAC553B7F92E5E36611D3DC4C784A95",
    "pf_extract_data_evidence.py": "E8AE936403B548ED1B6A7791BCA8F63B9ABB8F4BC025C46DED24CE489FE9FE49",
    "pf_extract_dump_rtti.py": "54B7BCFECF598007EA468309481F8E41FF64E4139026A0EE200984B03AD82A2B",
    "pf_extract_protocol.py": "0BB792BB6B0561E11592AB7F8C93C65CD1E0FBA0210E2A6BF40C9E5A8579112E",
    "PF_FIELD_VALIDATION.md": "39C8FA913316B674636AE684CDE2FC1B4D77A7BC1DD57016A1E4636E03636FF1",
    "PF_FIELD_VALIDATION.tsv": "080A5F32580DF575632FEE69D3F8FAA6E2E745AD1775D05DAF3E272E4E0941C3",
    "PF_HANDOFF_V1.md": "A2AFFA88576C6D9DC5A8899C26581CFA92E3C4ADC4A645AA7234903622916F60",
    "PF_INPUT_INVENTORY.md": "E5585C43CFEE3FDA85AB0C71CA28F83BC1951F09EDAB237B2486F4099C465D2C",
    "PF_INPUT_INVENTORY.tsv": "729B5E73383DE8FD6E0008875D4B9B685DE2AD8D72A55118AA862093F10259D1",
    "pf_inventory_inputs.py": "82B096C9D5FC137B3BFCDB4C7021B6FB0A5D40BCB02A562C7B4D101C7C821EC0",
    "PF_PROTOCOL_PRIORITY.md": "D9653552DB79911F0E2E3756DFFB354E3197A39EE3BAEBDADB568CB08DF8BB63",
    "PF_PROTOCOL_PRIORITY.tsv": "D9174BC27EBC1159A7B66BA3FC36B0D6025ECF72D9D963C3DEEE9BB780C3DE55",
    "PF_PROTOCOL_REGISTRY.md": "AD2E6474FA3208C5AE757DAE79A9E34F9A86AFD6EC70A2A94C33167DCF014AA6",
    "PF_PROTOCOL_REGISTRY.tsv": "27DAAC0C6FBBC45D88281C31B98E3A8B56F421BD1E8BC16F970FDFF5716CFB4D",
    "PF_RUNTIME_CLASSMAP.md": "9F2DB6244A7C2E33F6F64BD480AE4F45A9659FBDF2452D45601A847D47DC54EA",
    "PF_RUNTIME_CLASSMAP.tsv": "C53A6EAF23911765EBABD5E86CCAECF827FFDD88A1F514FC3F0F3EA2C3484985",
    "PF_SERIALIZER_FIELDS.md": "1D069B20871B3081F013E88E128F78D790C1133838A565F6F11DAB078859139A",
    "PF_SERIALIZER_FIELDS.tsv": "99282BDF3F492EAEBDBAB4918AECC0E37BF8EFB42B904B18E1BA306767B5C123",
    "PF_TAG_CENSUS.tsv": "63BC9A039B5B35E5B2E1F08CE99E91B05DA6E6959B5B4F173EAC66B88AEA337A",
    "pf_validate_capture_fields.py": "0166337CBC8E9E561D9D3CD5F02364F4ED43C49070644D5423387E87B793D8C8",
}

TSV_EXPECTATIONS = {
    "PF_PROTOCOL_REGISTRY.tsv": (519, Counter({"IMAGE": 519})),
    "PF_SERIALIZER_FIELDS.tsv": (6931, Counter({"IMAGE": 6931})),
    "PF_TAG_CENSUS.tsv": (11, Counter({"IMAGE": 11})),
    "PF_PROTOCOL_PRIORITY.tsv": (519, Counter({"IMAGE": 519})),
    "PF_FIELD_VALIDATION.tsv": (1038, Counter({"CAPTURE": 1038})),
    "PF_RUNTIME_CLASSMAP.tsv": (6244, Counter({"DUMP": 6244})),
    "PF_DATA_EVIDENCE.tsv": (290, Counter({"DATA": 290})),
    "PF_INPUT_INVENTORY.tsv": (
        2066,
        Counter({"CAPTURE": 1772, "DATA": 290, "IMAGE": 2, "DUMP": 2}),
    ),
}


class AuditError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def audit_tsv(name: str) -> tuple[int, Counter[str], list[str]]:
    path = ROOT / name
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        headers = list(reader.fieldnames or [])
        if "source" not in headers:
            raise AuditError(f"{name}: missing source column")
        count = 0
        sources: Counter[str] = Counter()
        for row in reader:
            count += 1
            source = row["source"]
            if source not in ALLOWED_SOURCES:
                raise AuditError(f"{name}: invalid source {source!r}")
            sources[source] += 1
    expected_count, expected_sources = TSV_EXPECTATIONS[name]
    if count != expected_count or sources != expected_sources:
        raise AuditError(
            f"{name}: census changed count={count} sources={dict(sources)}"
        )
    return count, sources, headers


def read_rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_semantics(headers_by_name: dict[str, list[str]]) -> None:
    priority_headers = set(headers_by_name["PF_PROTOCOL_PRIORITY.tsv"])
    required_priority = {
        "message",
        "priority",
        "matched_keyword",
        "structural_status",
        "capture_status",
        "blocker",
        "source",
    }
    if not required_priority <= priority_headers:
        raise AuditError("priority minimum schema missing")
    priority = read_rows("PF_PROTOCOL_PRIORITY.tsv")
    p1 = [row for row in priority if row["priority"] == "1"]
    if len(p1) != 365 or Counter(row["structural_status"] for row in p1) != {
        "CLOSED": 241,
        "OPEN": 124,
    }:
        raise AuditError("priority 1 closure census changed")
    if any(
        row["capture_status"] != "SEPARATE_SOURCE:PF_FIELD_VALIDATION.tsv"
        or row["matched_keyword"] != row["matched_keywords"]
        for row in priority
    ):
        raise AuditError("priority source-separation/keyword alias failed")

    capture_headers = set(headers_by_name["PF_FIELD_VALIDATION.tsv"])
    forbidden_capture_columns = {
        "raw",
        "raw_bytes",
        "payload",
        "payload_hex",
        "hexdump",
        "field_value",
    }
    if capture_headers & forbidden_capture_columns:
        raise AuditError("capture output exposes a forbidden raw/value column")
    capture = read_rows("PF_FIELD_VALIDATION.tsv")
    if sum(int(row["mismatch_instances"]) for row in capture) != 0:
        raise AuditError("v1 mismatch oracle changed")
    if Counter(row["status"] for row in capture) != {
        "NOT_OBSERVED": 980,
        "VALIDATED": 37,
        "A2_STATIC_OPEN": 21,
    }:
        raise AuditError("A5 status census changed")

    runtime_headers = set(headers_by_name["PF_RUNTIME_CLASSMAP.tsv"])
    forbidden_runtime_columns = {"raw", "raw_bytes", "payload", "hexdump"}
    if runtime_headers & forbidden_runtime_columns:
        raise AuditError("runtime output exposes a forbidden raw column")
    runtime = read_rows("PF_RUNTIME_CLASSMAP.tsv")
    if Counter(row["record_kind"] for row in runtime) != {
        "TYPE_DESCRIPTOR_UNBOUND": 6242,
        "SUMMARY": 2,
    }:
        raise AuditError("A6 record-kind census changed")
    if any(
        row["record_kind"] == "TYPE_DESCRIPTOR_UNBOUND"
        and (row["vtable_va"] != "UNKNOWN" or row["class_name"] != "UNKNOWN")
        for row in runtime
    ):
        raise AuditError("A6 unbound identity was promoted")

    data = read_rows("PF_DATA_EVIDENCE.tsv")
    if Counter(row["parse_status"] for row in data) != {
        "PASS": 287,
        "NONSTANDARD_GRAMMAR": 3,
    }:
        raise AuditError("DATA parse census changed")

    inventory = read_rows("PF_INPUT_INVENTORY.tsv")
    by_path = {row["relative_path"]: row for row in inventory}
    if by_path["GameClient.local.bin"]["sha256"].upper() != IMAGE_SHA:
        raise AuditError("primary image inventory hash changed")
    if by_path["GameClient.bin"]["sha256"].upper() != OTHER_IMAGE_SHA:
        raise AuditError("secondary image inventory hash changed")
    protected_hashes = {
        row["sha256"].upper()
        for row in inventory
        if row["source"] in {"DUMP", "CAPTURE"}
    }
    for name in ARTIFACTS:
        if sha256(ROOT / name) in protected_hashes:
            raise AuditError(f"{name}: exact protected input copy detected")

    report = (ROOT / "PF_EXTERNAL_REPORT.md").read_text(encoding="utf-8")
    for number in range(1, 7):
        if f"## {number})" not in report:
            raise AuditError(f"external report missing section {number}")
    if "mismatch ระหว่าง A2 กับเฟรมที่ parse ได้: 0" not in report:
        raise AuditError("external report A5 mismatch summary changed")
    report_oracles = (
        "ลำดับ 1 ปิดเชิงโครงสร้าง 241/365 = 66.03%; ยังเปิด 124 รายการ",
        "A5 ยืนยันเพิ่มจากสายจริงให้ Priority 1 ได้ 28 message",
        "ใน 124 รายการที่ยังเปิด ไม่มีรายการใดเป็น `capture-validated`",
        "parse สำเร็จ 11,904 message instance; A2 static-open 52,775",
    )
    if any(value not in report for value in report_oracles):
        raise AuditError("external report frozen claim oracle changed")

    dump_request = (ROOT / "PF_DUMP_REQUEST.md").read_text(encoding="utf-8")
    open_names = {row["message"] for row in p1 if row["structural_status"] == "OPEN"}
    appendix = dump_request.split(
        "## รายการ UNKNOWN เป้าหมายต่อสถานะ", 1
    )[-1].split("## เกณฑ์รับหลักฐานรอบใหม่", 1)[0]
    bound_names = [
        token
        for token in re.findall(r"`([^`]+)`", appendix)
        if token in open_names
    ]
    if len(bound_names) != 124 or set(bound_names) != open_names:
        raise AuditError("dump request does not bind each open P1 name exactly once")
    dump_oracles = (
        "MiniDumpWithFullMemory` (`0x00000002`)",
        "หนึ่ง dump ปิดได้อย่างรับประกันล่วงหน้า `0` ตัว",
        "ใบนี้ไม่กำหนดวิธีเปิดเซิร์ฟเวอร์หรือเกม",
        "ยอดรวมรายการไม่ซ้ำในภาคผนวกนี้เท่ากับ 124 พอดี",
    )
    if any(value not in dump_request for value in dump_oracles):
        raise AuditError("dump request frozen instruction oracle changed")

    erratum = (ROOT / "PF_ERRATUM_TWO_IMAGES.md").read_text(encoding="utf-8")
    if (
        IMAGE_SHA not in erratum
        or OTHER_IMAGE_SHA not in erratum
        or "จึงเป็นคนละ `IMAGE` source" not in erratum
        or "ผูกกับ `GameClient.local.bin` เท่านั้น" not in erratum
    ):
        raise AuditError("two-image erratum oracle changed")

    handoff = (ROOT / "PF_HANDOFF_V1.md").read_text(encoding="utf-8")
    handoff_oracles = (
        "ปิดส่งมอบ v1 ตามคำสั่งล่าสุด",
        "Priority 1 มี 365 รายการ; ปิดเชิงโครงสร้าง 241/365 = 66.03%; เปิด 124",
        "A5 สแกน capture 1,772 ไฟล์ครบ; parse สำเร็จ 11,904 message instances; mismatch ที่พิสูจน์ได้ 0",
        "## 8. สิ่งที่ยังไม่รู้ — ต้องรักษา UNKNOWN ไว้",
        "## 9. สิ่งที่เกือบเดา แต่ห้ามตัวเองไว้",
        "หากไม่มีหลักฐาน runtime ใหม่ ให้ถือ v1 นี้เป็นกล่องปิด",
    )
    if any(value not in handoff for value in handoff_oracles):
        raise AuditError("handoff frozen claim oracle changed")


def render_manifest(
    audited: list[tuple[str, int, str]],
    tsv_counts: dict[str, tuple[int, Counter[str]]],
) -> str:
    lines = [
        "# PF v1 final manifest and audit",
        "",
        "กล่อง v1 นี้ผ่าน final audit แบบอ่านอย่างเดียวหลัง A4/A5 รอบสุดท้ายและหลัง input inventory rehash รอบสุดท้าย",
        "",
        "## Audit result",
        "",
        "- result: `PASS`",
        "- frozen expected-hash oracle: `PASS`",
        "- exact external namespace allowlist: `PASS`",
        "- allowed TSV sources: `IMAGE | DUMP | CAPTURE | DATA`",
        "- Priority 1: `241/365 CLOSED`, `124 OPEN`",
        "- A5 mismatch: `0`",
        "- protected input exact-copy check: `PASS`",
        "- UTF-8 decode and required report sections 1–6: `PASS`",
        "- temporary file/directory residue check: `PASS`",
        "",
        "## TSV census",
        "",
        "| file | rows | source counts |",
        "|---|---:|---|",
    ]
    for name in TSV_EXPECTATIONS:
        count, sources = tsv_counts[name]
        source_text = ", ".join(f"{key}={sources[key]}" for key in sorted(sources))
        lines.append(f"| `{name}` | {count} | `{source_text}` |")
    lines.extend(
        [
            "",
            "## Artifact hashes",
            "",
            "`PF_V1_MANIFEST.md` ไม่ hash ตัวเอง; ไฟล์อื่นในกล่องที่รับรองอยู่ด้านล่าง",
            "",
            "| file | bytes | SHA-256 |",
            "|---|---:|---|",
        ]
    )
    for name, size, digest in audited:
        lines.append(f"| `{name}` | {size} | `{digest}` |")
    lines.append("")
    return "\n".join(lines)


def atomic_write(path: Path, text: str) -> None:
    fd, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp = Path(raw_temp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        try:
            temp.unlink()
        except FileNotFoundError:
            pass


def main() -> None:
    allowed_names = set(ARTIFACTS) | {"PF_V1_MANIFEST.md"}
    actual_entries = {path.name: path for path in ROOT.iterdir()}
    missing = sorted(set(ARTIFACTS) - set(actual_entries))
    extra = sorted(set(actual_entries) - allowed_names)
    nonfiles = sorted(
        name for name, path in actual_entries.items() if not path.is_file()
    )
    if missing or extra or nonfiles:
        raise AuditError(
            f"external namespace mismatch missing={missing} extra={extra} "
            f"nonfiles={nonfiles}"
        )
    expected_hash_names = set(ARTIFACTS) - {"pf_build_v1_manifest.py"}
    if set(EXPECTED_ARTIFACT_HASHES) != expected_hash_names:
        raise AuditError("frozen artifact hash-oracle key set changed")
    mismatched_hashes = [
        name
        for name, expected in EXPECTED_ARTIFACT_HASHES.items()
        if sha256(ROOT / name) != expected
    ]
    if mismatched_hashes:
        raise AuditError(
            "frozen artifact hash mismatch: " + ",".join(sorted(mismatched_hashes))
        )

    tsv_counts: dict[str, tuple[int, Counter[str]]] = {}
    headers_by_name: dict[str, list[str]] = {}
    for name in TSV_EXPECTATIONS:
        count, sources, headers = audit_tsv(name)
        tsv_counts[name] = (count, sources)
        headers_by_name[name] = headers
    validate_semantics(headers_by_name)

    audited = []
    for name in ARTIFACTS:
        path = ROOT / name
        if path.suffix.casefold() in {".md", ".py", ".tsv"}:
            path.read_text(encoding="utf-8")
        audited.append((name, path.stat().st_size, sha256(path)))
    atomic_write(ROOT / "PF_V1_MANIFEST.md", render_manifest(audited, tsv_counts))
    print("v1_audit=PASS")
    print("artifacts=%d" % len(audited))
    print("tsv_sets=%d" % len(tsv_counts))


if __name__ == "__main__":
    try:
        main()
    except AuditError as exc:
        raise SystemExit(f"ERROR: {exc}")
