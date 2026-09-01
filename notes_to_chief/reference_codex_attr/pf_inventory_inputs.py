#!/usr/bin/env python3
"""Hash the authorized Pirate Force evidence inputs without exporting payloads."""

from __future__ import annotations

import csv
import hashlib
import io
import os
import re
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


EVIDENCE_SOURCES = frozenset({"IMAGE", "DUMP", "CAPTURE", "DATA"})
EXPECTED_CAPTURE_DIRECTORY_COUNT = 242
EXPECTED_CAPTURE_FILE_COUNT = 1772
EXPECTED_CAPTURE_TOTAL_BYTES = 595_134_426
EXPECTED_XML_FILE_COUNT = 290
EXPECTED_XML_TOTAL_BYTES = 93_867

EXPECTED_CORE = {
    "GameClient.bin": (
        "IMAGE",
        14_759_424,
        "c528bf43070e2789170f41b6e3e28ccec6b57bdc594ee73dfa061188a5d1e4bd",
    ),
    "GameClient.local.bin": (
        "IMAGE",
        14_759_424,
        "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623",
    ),
    "GameClient.local.bin_1.41.01_69151_20260816_040609.dmp": (
        "DUMP",
        13_258_352,
        "daf63c7d13dc7ca601776cc7e4abbf02aa2e367f91ea420b3b05aaa8af7bffdc",
    ),
    "GameClient.local.bin_1.41.01_69151_20260816_042854.dmp": (
        "DUMP",
        13_266_299,
        "f982d47b6cec71171ccd2129ee9ce955a0cca05a9d5b606b0c97d5dd28169904",
    ),
}


class InventoryError(RuntimeError):
    pass


@dataclass(frozen=True)
class InputRow:
    source: str
    source_id: str
    relative_path: str
    size: int
    sha256: str
    role: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                return digest.hexdigest()
            digest.update(block)


def default_game_client_root() -> Path:
    return Path(__file__).resolve().parents[2] / "GameClient"


def capture_directories(root: Path) -> list[Path]:
    return sorted(
        (path for path in root.rglob("capture_*") if path.is_dir()),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )


def inventory_paths(root: Path) -> tuple[list[tuple[str, str, Path]], int]:
    items: list[tuple[str, str, Path]] = []
    for name, (source, _size, _sha256) in EXPECTED_CORE.items():
        role = {
            "GameClient.bin": "SECONDARY_DISTINCT_IMAGE",
            "GameClient.local.bin": "PRIMARY_A1_A4_IMAGE",
        }.get(name, "A6_DUMP")
        items.append((source, role, root / name))

    capture_dirs = capture_directories(root)
    capture_files: dict[str, Path] = {}
    for directory in capture_dirs:
        for path in directory.rglob("*"):
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                capture_files[relative.casefold()] = path
    for path in sorted(
        capture_files.values(),
        key=lambda value: value.relative_to(root).as_posix().casefold(),
    ):
        items.append(("CAPTURE", "A5_CAPTURE_INPUT", path))

    data_root = root / "Data"
    xml_files = sorted(
        (path for path in data_root.rglob("*.xml") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )
    for path in xml_files:
        items.append(("DATA", "DATA_XML_INPUT", path))

    capture_total = sum(path.stat().st_size for path in capture_files.values())
    xml_total = sum(path.stat().st_size for path in xml_files)
    if (
        len(capture_dirs) != EXPECTED_CAPTURE_DIRECTORY_COUNT
        or len(capture_files) != EXPECTED_CAPTURE_FILE_COUNT
        or capture_total != EXPECTED_CAPTURE_TOTAL_BYTES
        or len(xml_files) != EXPECTED_XML_FILE_COUNT
        or xml_total != EXPECTED_XML_TOTAL_BYTES
    ):
        raise InventoryError(
            "authorized input census changed: capture_dirs=%d capture_files=%d "
            "capture_bytes=%d xml_files=%d xml_bytes=%d"
            % (
                len(capture_dirs),
                len(capture_files),
                capture_total,
                len(xml_files),
                xml_total,
            )
        )
    return items, len(capture_dirs)


def measure_rows(root: Path, items: list[tuple[str, str, Path]]) -> list[InputRow]:
    rows = []
    for index, (source, role, path) in enumerate(items, 1):
        if source not in EVIDENCE_SOURCES or not path.is_file():
            raise InventoryError("invalid inventory input at row %d" % index)
        relative = path.relative_to(root).as_posix()
        rows.append(
            InputRow(
                source=source,
                source_id="%s-%04d" % (source, index),
                relative_path=relative,
                size=path.stat().st_size,
                sha256=sha256_file(path),
                role=role,
            )
        )
    return rows


def validate_rows(rows: list[InputRow]) -> None:
    expected_count = len(EXPECTED_CORE) + EXPECTED_CAPTURE_FILE_COUNT + EXPECTED_XML_FILE_COUNT
    if len(rows) != expected_count:
        raise InventoryError("input inventory row count mismatch")
    if len({row.relative_path.casefold() for row in rows}) != len(rows):
        raise InventoryError("input inventory contains duplicate paths")
    if any(row.source not in EVIDENCE_SOURCES for row in rows):
        raise InventoryError("input inventory contains invalid source")
    if any(not re.fullmatch(r"[0-9a-f]{64}", row.sha256) for row in rows):
        raise InventoryError("input inventory contains invalid SHA-256")
    by_path = {row.relative_path: row for row in rows}
    for name, (source, size, sha256) in EXPECTED_CORE.items():
        row = by_path.get(name)
        if row is None or (row.source, row.size, row.sha256) != (
            source,
            size,
            sha256,
        ):
            raise InventoryError("core input mismatch for %s" % name)
    original = by_path["GameClient.bin"]
    local = by_path["GameClient.local.bin"]
    if original.size != local.size or original.sha256 == local.sha256:
        raise InventoryError("executable identity oracle mismatch")


def build_tsv(rows: list[InputRow]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, dialect="excel-tab", lineterminator="\n")
    writer.writerow(
        ["source", "source_id", "relative_path", "size", "sha256", "role"]
    )
    for row in rows:
        writer.writerow(
            [
                row.source,
                row.source_id,
                row.relative_path,
                str(row.size),
                row.sha256,
                row.role,
            ]
        )
    return output.getvalue()


def build_md(rows: list[InputRow], capture_dir_count: int) -> str:
    counts = Counter(row.source for row in rows)
    sizes = Counter()
    for row in rows:
        sizes[row.source] += row.size
    by_path = {row.relative_path: row for row in rows}
    original = by_path["GameClient.bin"]
    local = by_path["GameClient.local.bin"]
    lines = [
        "# PF input inventory",
        "",
        "สำรวจและคำนวณ SHA-256 แบบอ่านอย่างเดียว; ไม่รันหรือแก้ input และไม่ส่งออก raw dump/capture bytes",
        "",
        "## Executable identity",
        "",
        "- `GameClient.bin`: size %d, SHA-256 `%s`" % (original.size, original.sha256),
        "- `GameClient.local.bin`: size %d, SHA-256 `%s`" % (local.size, local.sha256),
        "- ผล: ขนาดเท่ากันแต่ SHA-256 ต่างกัน จึงเป็นคนละ `IMAGE` source และ A1-A4 ยังคงผูกกับ `GameClient.local.bin` เท่านั้น",
        "",
        "## Census",
        "",
        "- capture directories: %d" % capture_dir_count,
    ]
    for source in ("IMAGE", "DUMP", "CAPTURE", "DATA"):
        lines.append(
            "- %s: %d file(s), %d byte(s)" % (source, counts[source], sizes[source])
        )
    lines.extend(
        [
            "",
            "DATA census รอบนี้ครอบเฉพาะ XML 290 ไฟล์ที่อนุมัติเป็นหลักฐานนำเข้า; ไฟล์ Data ชนิดอื่นจะต้องเพิ่ม manifest ก่อนใช้อ้างข้อเท็จจริง",
            "",
        ]
    )
    return "\n".join(lines)


def atomic_write_outputs(outputs: tuple[tuple[Path, str], ...]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for destination, text in outputs:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                dir=destination.parent,
                prefix=".%s." % destination.name,
                suffix=".tmp",
                delete=False,
            ) as stream:
                stream.write(text)
                stream.flush()
                os.fsync(stream.fileno())
                staged.append((Path(stream.name), destination))
        for temporary, destination in staged:
            os.replace(temporary, destination)
    finally:
        for temporary, _destination in staged:
            if temporary.exists():
                temporary.unlink()


def main() -> int:
    root = default_game_client_root().resolve()
    before_items, before_capture_dir_count = inventory_paths(root)
    before = measure_rows(root, before_items)
    validate_rows(before)

    after_items, after_capture_dir_count = inventory_paths(root)
    after = measure_rows(root, after_items)
    validate_rows(after)
    if (
        before_items != after_items
        or before_capture_dir_count != after_capture_dir_count
        or before != after
    ):
        raise InventoryError("input inventory changed during read-only census")

    output_dir = Path(__file__).resolve().parent
    atomic_write_outputs(
        (
            (output_dir / "PF_INPUT_INVENTORY.tsv", build_tsv(before)),
            (
                output_dir / "PF_INPUT_INVENTORY.md",
                build_md(before, before_capture_dir_count),
            ),
        )
    )
    print("input_rows=%d" % len(before))
    print("capture_directories=%d" % before_capture_dir_count)
    print("capture_files=%d" % EXPECTED_CAPTURE_FILE_COUNT)
    print("data_xml_files=%d" % EXPECTED_XML_FILE_COUNT)
    print("inputs_unchanged=true")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except InventoryError as exc:
        sys.stderr.write("ERROR: %s\n" % exc)
        raise SystemExit(1)
