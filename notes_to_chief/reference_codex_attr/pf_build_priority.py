#!/usr/bin/env python3
"""Build the source-separated protocol priority census from A1 and A2.

This tool only consumes the IMAGE-derived TSV artifacts.  Runtime observations
belong in PF_FIELD_VALIDATION.* and are deliberately not merged into these rows.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


SOURCE = "IMAGE"
CAPTURE_STATUS_LINK = "SEPARATE_SOURCE:PF_FIELD_VALIDATION.tsv"
EXPECTED_REGISTRY_ROWS = 519
EXPECTED_PRIORITY_COUNTS = {1: 365, 2: 16, 3: 138}
EXPECTED_CLOSED_COUNTS = {1: 241, 2: 12, 3: 84}
EXPECTED_GROUP_COUNTS = {
    (1, "combat/damage/hp/vital"): 310,
    (1, "actor/npc/monster"): 49,
    (1, "item/inventory/drop/pickup/loot"): 60,
    (1, "move/position/teleport"): 8,
    (1, "login/logout/select/session"): 11,
    (1, "party"): 8,
    (2, "shop/trade/stall"): 2,
    (2, "skill/buff"): 5,
    (2, "quest"): 9,
    (2, "chat/message"): 0,
    (3, "remaining"): 138,
}
PRIORITY_GROUPS: tuple[tuple[int, tuple[tuple[str, tuple[str, ...]], ...]], ...] = (
    (
        1,
        (
            ("combat/damage/hp/vital", ("combat", "damage", "hp", "vital")),
            ("actor/npc/monster", ("actor", "npc", "monster")),
            (
                "item/inventory/drop/pickup/loot",
                ("item", "inventory", "drop", "pickup", "loot"),
            ),
            ("move/position/teleport", ("move", "position", "teleport")),
            (
                "login/logout/select/session",
                ("login", "logout", "select", "session"),
            ),
            ("party", ("party",)),
        ),
    ),
    (
        2,
        (
            ("shop/trade/stall", ("shop", "trade", "stall")),
            ("skill/buff", ("skill", "buff")),
            ("quest", ("quest",)),
            ("chat/message", ("chat", "message")),
        ),
    ),
)


class PriorityError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tsv_text(headers: list[str], rows: list[list[str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return stream.getvalue()


def source_check(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise PriorityError(f"{path.name}: empty TSV")
    if "source" not in rows[0]:
        raise PriorityError(f"{path.name}: missing source column")
    measured = Counter(row["source"] for row in rows)
    if measured != Counter({SOURCE: len(rows)}):
        raise PriorityError(f"{path.name}: expected only source={SOURCE}, got {measured}")


def classify(name: str) -> tuple[int, list[str], list[str]]:
    lowered = name.casefold()
    for priority, groups in PRIORITY_GROUPS:
        matched_groups: list[str] = []
        matched_keywords: list[str] = []
        for group, keywords in groups:
            group_hits = [keyword for keyword in keywords if keyword in lowered]
            if group_hits:
                matched_groups.append(group)
                matched_keywords.extend(group_hits)
        if matched_groups:
            return priority, matched_groups, matched_keywords
    return 3, ["remaining"], []


def unknown_reasons(field_rows: list[dict[str, str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for row in field_rows:
        field_offset = row["field_offset"]
        if row["tag"] == "UNKNOWN" or "UNKNOWN(" in field_offset:
            matches = re.findall(r"UNKNOWN\(([^)]+)\)", field_offset)
            if matches:
                result[row["message"]].update(matches)
            else:
                result[row["message"]].add("unclassified static field")
    return result


def atomic_publish(outputs: dict[Path, str]) -> None:
    if not outputs:
        raise PriorityError("no priority outputs to publish")
    originals = {
        target: (target.read_bytes() if target.exists() else None)
        for target in outputs
    }
    staged: dict[Path, Path] = {}
    committed: list[Path] = []
    try:
        for target, text in outputs.items():
            fd, raw_temp = tempfile.mkstemp(
                prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
            )
            temp = Path(raw_temp)
            staged[target] = temp
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                    handle.write(text)
                    handle.flush()
                    os.fsync(handle.fileno())
            except BaseException:
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise
        for target in outputs:
            temp = staged[target]
            os.replace(temp, target)
            del staged[target]
            committed.append(target)
    except BaseException as commit_error:
        recovery_errors: list[str] = []
        for temp in staged.values():
            try:
                temp.unlink()
            except FileNotFoundError:
                pass
            except OSError as exc:
                recovery_errors.append(
                    f"stage_cleanup:{temp.name}:{type(exc).__name__}"
                )
        for target in reversed(committed):
            original = originals[target]
            rollback_temp: Path | None = None
            try:
                if original is None:
                    target.unlink(missing_ok=True)
                else:
                    fd, raw_temp = tempfile.mkstemp(
                        prefix=f".{target.name}.",
                        suffix=".rollback",
                        dir=target.parent,
                    )
                    rollback_temp = Path(raw_temp)
                    try:
                        with os.fdopen(fd, "wb") as handle:
                            handle.write(original)
                            handle.flush()
                            os.fsync(handle.fileno())
                    except BaseException:
                        try:
                            os.close(fd)
                        except OSError:
                            pass
                        raise
                    os.replace(rollback_temp, target)
                    rollback_temp = None
            except BaseException as exc:
                recovery_errors.append(
                    f"rollback:{target.name}:{type(exc).__name__}"
                )
            finally:
                if rollback_temp is not None:
                    try:
                        rollback_temp.unlink()
                    except FileNotFoundError:
                        pass
                    except OSError as exc:
                        recovery_errors.append(
                            "rollback_cleanup:%s:%s"
                            % (rollback_temp.name, type(exc).__name__)
                        )
        if recovery_errors:
            raise PriorityError(
                "priority output recovery incomplete: "
                + ",".join(recovery_errors)
            ) from commit_error
        raise


def expected_output_row(
    registry_row: dict[str, str], blockers: dict[str, set[str]]
) -> dict[str, str]:
    name = registry_row["name"]
    priority, groups, keywords = classify(name)
    identity_missing = [
        column.removesuffix("_va")
        for column in ("getter_va", "vtable_va", "serializer_va")
        if registry_row[column] == "UNKNOWN"
    ]
    reasons = sorted(blockers.get(name, set()))
    combined = [f"registry {value} UNKNOWN" for value in identity_missing] + reasons
    return {
        "message": name,
        "priority": str(priority),
        "matched_groups": " | ".join(groups),
        "matched_keywords": " | ".join(keywords) if keywords else "N/A",
        "matched_keyword": " | ".join(keywords) if keywords else "N/A",
        "registry_identity_status": "KNOWN" if not identity_missing else "OPEN",
        "registry_identity_missing": " | ".join(identity_missing)
        if identity_missing
        else "N/A",
        "serializer_status": "CLOSED" if not reasons else "OPEN",
        "serializer_blockers": " | ".join(reasons) if reasons else "N/A",
        "structural_status": "CLOSED" if not combined else "OPEN",
        "capture_status": CAPTURE_STATUS_LINK,
        "blocker": " | ".join(combined) if combined else "N/A",
        "source": SOURCE,
    }


def validate_output(
    text: str,
    registry: list[dict[str, str]],
    blockers: dict[str, set[str]],
) -> None:
    rows = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    expected_rows = len(registry)
    if len(rows) != expected_rows:
        raise PriorityError(
            f"priority output row count {len(rows)} != expected {expected_rows}"
        )
    expected_headers = [
        "message",
        "priority",
        "matched_groups",
        "matched_keywords",
        "matched_keyword",
        "registry_identity_status",
        "registry_identity_missing",
        "serializer_status",
        "serializer_blockers",
        "structural_status",
        "capture_status",
        "blocker",
        "source",
    ]
    if list(rows[0]) != expected_headers:
        raise PriorityError("priority output header contract changed")
    if Counter(row["source"] for row in rows) != Counter({SOURCE: expected_rows}):
        raise PriorityError("priority output violates source=IMAGE contract")
    if len({row["message"] for row in rows}) != expected_rows:
        raise PriorityError("priority output message keys are not unique")
    expected_by_name = {
        row["name"]: expected_output_row(row, blockers) for row in registry
    }
    if set(expected_by_name) != {row["message"] for row in rows}:
        raise PriorityError("priority output message key set changed")
    for row in rows:
        expected = expected_by_name[row["message"]]
        if row != expected:
            changed = [key for key in expected_headers if row.get(key) != expected[key]]
            raise PriorityError(
                "%s priority semantic mismatch in %s"
                % (row["message"], ",".join(changed))
            )
    priority_counts = Counter(int(row["priority"]) for row in rows)
    closed_counts = Counter(
        int(row["priority"])
        for row in rows
        if row["structural_status"] == "CLOSED"
    )
    group_counts: Counter[tuple[int, str]] = Counter()
    for row in rows:
        for group in row["matched_groups"].split(" | "):
            group_counts[(int(row["priority"]), group)] += 1
    if dict(priority_counts) != EXPECTED_PRIORITY_COUNTS:
        raise PriorityError(f"priority census changed: {dict(priority_counts)}")
    if {value: closed_counts[value] for value in (1, 2, 3)} != EXPECTED_CLOSED_COUNTS:
        raise PriorityError(f"priority closure census changed: {dict(closed_counts)}")
    if {key: group_counts[key] for key in EXPECTED_GROUP_COUNTS} != EXPECTED_GROUP_COUNTS:
        raise PriorityError("priority keyword-group census changed")


def validate_output_mutation_regressions(
    text: str,
    registry: list[dict[str, str]],
    blockers: dict[str, set[str]],
) -> None:
    rows = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    headers = list(rows[0])
    mutations = {
        "priority": "9",
        "matched_groups": "forged",
        "matched_keyword": "forged",
        "structural_status": "CLOSED"
        if rows[0]["structural_status"] != "CLOSED"
        else "OPEN",
        "capture_status": "PASS",
        "blocker": "forged",
        "source": "DUMP",
    }
    for column, value in mutations.items():
        mutated = [dict(row) for row in rows]
        mutated[0][column] = value
        mutated_text = tsv_text(headers, [[row[key] for key in headers] for row in mutated])
        try:
            validate_output(mutated_text, registry, blockers)
        except PriorityError:
            pass
        else:
            raise PriorityError(
                f"priority {column} mutation was unexpectedly accepted"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--external",
        type=Path,
        default=Path(__file__).resolve().parent,
    )
    args = parser.parse_args()
    external = args.external.resolve()
    registry_path = external / "PF_PROTOCOL_REGISTRY.tsv"
    fields_path = external / "PF_SERIALIZER_FIELDS.tsv"
    before = {path: sha256(path) for path in (registry_path, fields_path)}
    registry = read_tsv(registry_path)
    fields = read_tsv(fields_path)
    source_check(registry_path, registry)
    source_check(fields_path, fields)
    if len(registry) != EXPECTED_REGISTRY_ROWS:
        raise PriorityError(
            f"registry rows {len(registry)} != frozen census {EXPECTED_REGISTRY_ROWS}"
        )
    names = [row["name"] for row in registry]
    if len(set(names)) != len(names):
        raise PriorityError("registry names are not unique")
    field_names = {row["message"] for row in fields}
    missing_fields = sorted(set(names) - field_names)
    extra_fields = sorted(field_names - set(names))
    if missing_fields or extra_fields:
        raise PriorityError(
            "A1/A2 name set mismatch: missing=%r extra=%r"
            % (missing_fields, extra_fields)
        )

    blockers = unknown_reasons(fields)
    output_rows: list[list[str]] = []
    priority_counts: Counter[int] = Counter()
    closed_counts: Counter[int] = Counter()
    group_counts: Counter[tuple[int, str]] = Counter()
    open_rows: dict[int, list[tuple[str, str]]] = defaultdict(list)
    for row in registry:
        name = row["name"]
        priority, groups, keywords = classify(name)
        priority_counts[priority] += 1
        for group in groups:
            group_counts[(priority, group)] += 1
        identity_missing = [
            column.removesuffix("_va")
            for column in ("getter_va", "vtable_va", "serializer_va")
            if row[column] == "UNKNOWN"
        ]
        reasons = sorted(blockers.get(name, set()))
        combined = [f"registry {value} UNKNOWN" for value in identity_missing] + reasons
        status = "CLOSED" if not combined else "OPEN"
        if status == "CLOSED":
            closed_counts[priority] += 1
        else:
            open_rows[priority].append((name, " | ".join(combined)))
        output_rows.append(
            [
                name,
                str(priority),
                " | ".join(groups),
                " | ".join(keywords) if keywords else "N/A",
                " | ".join(keywords) if keywords else "N/A",
                "KNOWN" if not identity_missing else "OPEN",
                " | ".join(identity_missing) if identity_missing else "N/A",
                "CLOSED" if not reasons else "OPEN",
                " | ".join(reasons) if reasons else "N/A",
                status,
                CAPTURE_STATUS_LINK,
                " | ".join(combined) if combined else "N/A",
                SOURCE,
            ]
        )

    headers = [
        "message",
        "priority",
        "matched_groups",
        "matched_keywords",
        "matched_keyword",
        "registry_identity_status",
        "registry_identity_missing",
        "serializer_status",
        "serializer_blockers",
        "structural_status",
        "capture_status",
        "blocker",
        "source",
    ]
    priority_tsv = tsv_text(headers, output_rows)
    validate_output(priority_tsv, registry, blockers)
    validate_output_mutation_regressions(priority_tsv, registry, blockers)

    lines = [
        "# PF protocol priority census",
        "",
        "ตารางนี้จัดกลุ่มจากชื่อในทะเบียน 519 ตัวตามคำสั่งใหม่เท่านั้น และทุกแถวเป็นหลักฐาน `source=IMAGE` จาก A1/A2; ผลจาก capture หรือ dump จะไม่ถูกผสมลงในแถวเหล่านี้",
        "",
        "## กติกา",
        "",
        "- ตรวจชื่อแบบไม่สนตัวพิมพ์ใหญ่เล็ก และใช้ substring ตามรายการคำที่สั่ง",
        "- ถ้าชื่อตรงหลายกลุ่มในลำดับเดียวกัน เก็บทุกกลุ่ม/ทุกคำที่ตรง แต่เลือกเลขลำดับต่ำสุดเพียงลำดับเดียว",
        "- `CLOSED` ต้องมี getter, vtable และ serializer identity พร้อม และ A2 ไม่มี static blocker; handler ไม่ถูกใช้เป็นเกณฑ์ field-serialization closure",
        "- `matched_keyword` เป็น alias ตาม schema ส่งมอบของ `matched_keywords`; validator บังคับให้ค่าตรงกันทุกแถว",
        "- `blocker` รวมเฉพาะ registry/A2 blocker ชั้น IMAGE ของแถวนั้น",
        "- `capture_status` ในแถว IMAGE มีเพียงค่าอ้างอิง `SEPARATE_SOURCE:PF_FIELD_VALIDATION.tsv`; สถานะจริงจาก capture อยู่ในแถว `source=CAPTURE` ของไฟล์นั้นและห้าม merge เข้ามา",
        "- สถานะนี้เป็น structural closure ของ IMAGE ไม่ใช่คำอ้างว่าเคยเห็นบนสายจริง; การยืนยันสายจริงอยู่ใน `PF_FIELD_VALIDATION.*` เท่านั้น",
        "",
        "## จำนวน",
        "",
    ]
    for priority in (1, 2, 3):
        total = priority_counts[priority]
        closed = closed_counts[priority]
        percentage = 100.0 * closed / total if total else 100.0
        lines.append(
            f"- ลำดับ {priority}: ปิดเชิงโครงสร้าง {closed}/{total} ({percentage:.2f}%), เปิด {total - closed}"
        )
    lines.extend(["", "## จำนวนแยกตามกลุ่ม", ""])
    for priority, groups in PRIORITY_GROUPS:
        for group, _keywords in groups:
            lines.append(f"- ลำดับ {priority} `{group}`: {group_counts[(priority, group)]}")
    lines.append(f"- ลำดับ 3 `remaining`: {group_counts[(3, 'remaining')]}")
    lines.extend(["", "## ลำดับ 1 ที่ยังเปิด", ""])
    if open_rows[1]:
        for name, reason in open_rows[1]:
            lines.append(f"- `{name}` — {reason}")
    else:
        lines.append("- ไม่มี")
    lines.extend(
        [
            "",
            "## ขอบเขตหลักฐาน",
            "",
            f"- registry SHA-256 ก่อน/หลัง: `{before[registry_path]}`",
            f"- serializer fields SHA-256 ก่อน/หลัง: `{before[fields_path]}`",
            "- ไม่มีการอ่าน DUMP/CAPTURE/DATA ในขั้นตอนนี้",
            "",
        ]
    )
    after = {path: sha256(path) for path in (registry_path, fields_path)}
    if after != before:
        raise PriorityError("A1/A2 changed during priority census")
    priority_md = "\n".join(lines)
    atomic_publish(
        {
            external / "PF_PROTOCOL_PRIORITY.tsv": priority_tsv,
            external / "PF_PROTOCOL_PRIORITY.md": priority_md,
        }
    )
    print(
        "priority_rows=%d p1=%d p1_closed=%d p1_open=%d"
        % (
            len(output_rows),
            priority_counts[1],
            closed_counts[1],
            priority_counts[1] - closed_counts[1],
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PriorityError as exc:
        raise SystemExit(f"ERROR: {exc}")
