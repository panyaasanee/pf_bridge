#!/usr/bin/env python3
"""Build a DATA-only structural census without publishing XML values."""

from __future__ import annotations

import csv
import hashlib
import os
import re
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


GAMECLIENT = Path(r"C:\Users\Panya\Desktop\Pirate Force\GameClient")
DATA_ROOT = GAMECLIENT / "Data"
OUT_ROOT = Path(r"C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external")
INVENTORY = OUT_ROOT / "PF_INPUT_INVENTORY.tsv"
OUT_TSV = OUT_ROOT / "PF_DATA_EVIDENCE.tsv"
OUT_MD = OUT_ROOT / "PF_DATA_EVIDENCE.md"

FIELDS = [
    "source",
    "evidence_id",
    "relative_path",
    "size",
    "sha256",
    "document_kind",
    "parse_status",
    "root_tag",
    "element_count",
    "record_tag",
    "record_count",
    "attribute_names",
    "parser_detail",
]

PSEUDO_ROOT_OPEN = re.compile(rb"^\s*<ScaleOffset>\s*", re.DOTALL)
PSEUDO_ROOT_CLOSE = re.compile(rb"\s*</ScaleOffset>\s*$", re.DOTALL)
PSEUDO_TOKEN = re.compile(
    rb"\s*(?:(?P<comment><!--(?:[^-]|-(?!->))*-->)|"
    rb"(?P<item><\s+Item\s+height\s*=\s*\"[^\"]*\"\s*,\s*"
    rb"offset\s*=\s*\"[^\"]*\"\s*/>))"
)


@dataclass(frozen=True)
class InputRecord:
    source_id: str
    relative_path: str
    size: int
    sha256: str


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def atomic_publish_pair(outputs: tuple[tuple[Path, str], ...]) -> None:
    """Stage both outputs and restore the prior pair if commit is interrupted."""
    if len(outputs) != 2 or len({path for path, _text in outputs}) != 2:
        raise RuntimeError("atomic output pair invariant failed")
    staged: dict[Path, str] = {}
    originals = {
        path: (path.read_bytes() if path.exists() else None)
        for path, _text in outputs
    }
    committed: list[Path] = []
    try:
        for path, content in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(
                prefix=path.name + ".", suffix=".stage", dir=path.parent
            )
            staged[path] = temporary
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                    handle.write(content)
                    handle.flush()
                    os.fsync(handle.fileno())
            except BaseException:
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise
        for path, _content in outputs:
            temporary = staged[path]
            os.replace(temporary, path)
            del staged[path]
            committed.append(path)
    except BaseException as commit_error:
        recovery_errors: list[str] = []
        for temporary in staged.values():
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            except OSError as exc:
                recovery_errors.append(
                    f"stage_cleanup:{Path(temporary).name}:{type(exc).__name__}"
                )
        for path in reversed(committed):
            original = originals[path]
            rollback_temporary: str | None = None
            try:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    fd, rollback_temporary = tempfile.mkstemp(
                        prefix=path.name + ".", suffix=".rollback", dir=path.parent
                    )
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
                    os.replace(rollback_temporary, path)
                    rollback_temporary = None
            except BaseException as exc:
                recovery_errors.append(
                    f"rollback:{path.name}:{type(exc).__name__}"
                )
            finally:
                if rollback_temporary is not None:
                    try:
                        os.unlink(rollback_temporary)
                    except FileNotFoundError:
                        pass
                    except OSError as exc:
                        recovery_errors.append(
                            "rollback_cleanup:%s:%s"
                            % (Path(rollback_temporary).name, type(exc).__name__)
                        )
        if recovery_errors:
            raise RuntimeError(
                "output pair recovery incomplete: " + ",".join(recovery_errors)
            ) from commit_error
        raise


def pseudo_item_count(raw: bytes) -> int | None:
    opening = PSEUDO_ROOT_OPEN.match(raw)
    closing = PSEUDO_ROOT_CLOSE.search(raw)
    if opening is None or closing is None or opening.end() > closing.start():
        return None
    position = opening.end()
    count = 0
    while position < closing.start():
        token = PSEUDO_TOKEN.match(raw, position, closing.start())
        if token is None or token.end() == position:
            return None
        count += token.group("item") is not None
        position = token.end()
    return count if position == closing.start() else None


def validate_pseudo_parser_mutations() -> None:
    good = (
        b"<ScaleOffset>\n<!-- structural comment -->\n"
        b'< Item height="0", offset="1"/>\n</ScaleOffset>\n'
    )
    if pseudo_item_count(good) != 1:
        raise RuntimeError("pseudo-XML positive regression failed")
    mutations = (
        good.replace(b"</ScaleOffset>", b"<Unexpected/></ScaleOffset>"),
        good.replace(b'\", offset', b'\" offset'),
        good.replace(b"</ScaleOffset>", b"<!-- unterminated</ScaleOffset>"),
        good.replace(b"<ScaleOffset>", b"<Other>"),
    )
    if any(pseudo_item_count(mutated) is not None for mutated in mutations):
        raise RuntimeError("pseudo-XML mutation regression failed")


def load_inventory() -> list[InputRecord]:
    with INVENTORY.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    selected = [
        InputRecord(
            source_id=row["source_id"],
            relative_path=row["relative_path"],
            size=int(row["size"]),
            sha256=row["sha256"].upper(),
        )
        for row in rows
        if row["source"] == "DATA" and row["role"] == "DATA_XML_INPUT"
    ]
    if len(selected) != 290:
        raise RuntimeError(f"inventory DATA XML count changed: {len(selected)}")
    return selected


def parse_record(record: InputRecord, raw: bytes) -> dict[str, str]:
    common = {
        "source": "DATA",
        "evidence_id": record.source_id,
        "relative_path": record.relative_path,
        "size": str(len(raw)),
        "sha256": digest(raw),
    }
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        item_count = pseudo_item_count(raw)
        if not (
            record.relative_path.startswith("Data/GC/Avatar-")
            and item_count == 101
        ):
            raise RuntimeError(
                f"unclassified DATA parse failure: {record.relative_path}: {exc}"
            ) from exc
        line, column = exc.position
        return {
            **common,
            "document_kind": "AVATAR_OFFSET_PSEUDO_XML",
            "parse_status": "NONSTANDARD_GRAMMAR",
            "root_tag": "ScaleOffset",
            "element_count": "102",
            "record_tag": "Item",
            "record_count": str(item_count),
            "attribute_names": "height,offset",
            "parser_detail": f"XML_PARSE_ERROR_LINE_{line}_COLUMN_{column}",
        }

    tags = Counter(element.tag for element in root.iter())
    attributes = sorted({name for element in root.iter() for name in element.attrib})
    if root.tag != "Block" or set(tags) - {"Block", "SurfaceMask"}:
        raise RuntimeError(f"unexpected DATA XML structure: {record.relative_path}")
    return {
        **common,
        "document_kind": "SURFACE_MASK_XML",
        "parse_status": "PASS",
        "root_tag": root.tag,
        "element_count": str(sum(tags.values())),
        "record_tag": "SurfaceMask",
        "record_count": str(tags["SurfaceMask"]),
        "attribute_names": ",".join(attributes) if attributes else "NONE",
        "parser_detail": "STANDARD_XML",
    }


def render_tsv(rows: list[dict[str, str]]) -> str:
    from io import StringIO

    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def render_md(rows: list[dict[str, str]], hash_groups: dict[str, list[str]]) -> str:
    statuses = Counter(row["parse_status"] for row in rows)
    kinds = Counter(row["document_kind"] for row in rows)
    surface_records = sum(
        int(row["record_count"])
        for row in rows
        if row["document_kind"] == "SURFACE_MASK_XML"
    )
    offset_records = sum(
        int(row["record_count"])
        for row in rows
        if row["document_kind"] == "AVATAR_OFFSET_PSEUDO_XML"
    )
    duplicate_groups = [paths for paths in hash_groups.values() if len(paths) > 1]
    duplicate_files = sum(len(paths) for paths in duplicate_groups)
    lines = [
        "# PF DATA Evidence",
        "",
        "This is a DATA-only structural census. It does not promote DATA observations into IMAGE, DUMP, or CAPTURE facts.",
        "",
        "## Scope and integrity",
        "",
        f"- Input: all {len(rows)} XML files inventoried under `GameClient/Data`.",
        "- Every input size and SHA-256 matched `PF_INPUT_INVENTORY.tsv` before parsing.",
        "- Every input SHA-256 was rechecked after parsing and did not move.",
        "- The TSV contains names, structure, counts, sizes, and SHA-256 only; XML attribute values are not published.",
        "- Every TSV row is labelled `source=DATA`.",
        "",
        "## Results",
        "",
        f"- Standard XML parse: {statuses['PASS']} files.",
        f"- Nonstandard pseudo-XML grammar: {statuses['NONSTANDARD_GRAMMAR']} files.",
        f"- Surface-mask documents: {kinds['SURFACE_MASK_XML']} files, {surface_records} `SurfaceMask` records.",
        f"- Avatar-offset documents: {kinds['AVATAR_OFFSET_PSEUDO_XML']} files, {offset_records} structural `Item` records.",
        f"- Distinct file hashes: {len(hash_groups)}; duplicate-content groups: {len(duplicate_groups)} ({duplicate_files} files).",
        "",
        "The three avatar-offset files have the same deliberate nonstandard item grammar: a space after `<` and a comma between attributes. They are recorded as `NONSTANDARD_GRAMMAR`, not silently repaired.",
        "",
        "## Protocol relevance",
        "",
        "This DATA set describes scene surface masks and avatar display offsets. It supplies no exact serializer field order, thunk target, or runtime class identity, so it does not close any protocol UNKNOWN by itself.",
        "",
        "## Files",
        "",
        "- `PF_DATA_EVIDENCE.tsv`: one DATA-only row per input XML file.",
        "- `PF_DATA_EVIDENCE.md`: this interpretation and integrity summary.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    validate_pseudo_parser_mutations()
    inventory_before = digest(INVENTORY.read_bytes())
    records = load_inventory()
    discovered_before = {
        path.relative_to(GAMECLIENT).as_posix()
        for path in DATA_ROOT.rglob("*.xml")
        if path.is_file()
    }
    expected = {record.relative_path for record in records}
    if discovered_before != expected:
        missing = sorted(expected - discovered_before)
        extra = sorted(discovered_before - expected)
        raise RuntimeError(f"DATA input set changed; missing={missing}, extra={extra}")

    rows: list[dict[str, str]] = []
    before: dict[str, str] = {}
    hash_groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        path = GAMECLIENT / Path(record.relative_path)
        raw = path.read_bytes()
        actual = digest(raw)
        if len(raw) != record.size or actual != record.sha256:
            raise RuntimeError(f"inventory mismatch: {record.relative_path}")
        before[record.relative_path] = actual
        hash_groups[actual].append(record.relative_path)
        row = parse_record(record, raw)
        if row["source"] != "DATA" or set(row) != set(FIELDS):
            raise RuntimeError(f"row schema/source failure: {record.relative_path}")
        rows.append(row)

    for record in records:
        path = GAMECLIENT / Path(record.relative_path)
        if digest(path.read_bytes()) != before[record.relative_path]:
            raise RuntimeError(f"input changed during run: {record.relative_path}")
    discovered_after = {
        path.relative_to(GAMECLIENT).as_posix()
        for path in DATA_ROOT.rglob("*.xml")
        if path.is_file()
    }
    if discovered_after != discovered_before:
        raise RuntimeError("DATA XML namespace changed during run")
    if digest(INVENTORY.read_bytes()) != inventory_before:
        raise RuntimeError("input inventory changed during run")

    if len(rows) != 290 or Counter(row["source"] for row in rows) != {"DATA": 290}:
        raise RuntimeError("DATA output census invariant failed")
    if Counter(row["parse_status"] for row in rows) != {
        "PASS": 287,
        "NONSTANDARD_GRAMMAR": 3,
    }:
        raise RuntimeError("DATA parse-status invariant failed")

    atomic_publish_pair(
        (
            (OUT_TSV, render_tsv(rows)),
            (OUT_MD, render_md(rows, hash_groups)),
        )
    )
    print("DATA files: 290")
    print("standard XML: 287")
    print("nonstandard grammar: 3")
    print("source DATA rows: 290")


if __name__ == "__main__":
    main()
