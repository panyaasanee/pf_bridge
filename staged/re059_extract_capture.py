#!/usr/bin/env python3
"""RE-059 read-only extractor for the five captured ItemOperateVitalRes frames."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import sys
from pathlib import Path


TARGET_ID = 0x4C13
TARGET_WRAPPER = bytes((0x12, 0x13, 0x4C, 0x0B))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def expect(data: bytes, pos: int, tag: int, width: int) -> tuple[int, int]:
    if pos >= len(data) or data[pos] != tag:
        seen = "EOF" if pos >= len(data) else f"0x{data[pos]:02X}"
        raise ValueError(f"offset {pos}: expected tag 0x{tag:02X}, saw {seen}")
    end = pos + 1 + width
    if end > len(data):
        raise ValueError(f"offset {pos}: tag 0x{tag:02X} value truncated")
    return int.from_bytes(data[pos + 1 : end], "little"), end


def parse_item(data: bytes, pos: int) -> tuple[dict[str, int], int]:
    identity, pos = expect(data, pos, 0x32, 8)
    template_id, pos = expect(data, pos, 0x14, 4)
    quantity, pos = expect(data, pos, 0x0F, 2)
    slot, pos = expect(data, pos, 0x0F, 2)
    byte_a, pos = expect(data, pos, 0x08, 1)
    byte_b, pos = expect(data, pos, 0x08, 1)
    byte_c, pos = expect(data, pos, 0x0B, 1)
    return {
        "identity": identity,
        "template_id": template_id,
        "quantity": quantity,
        "slot": slot,
        "byte_a": byte_a,
        "byte_b": byte_b,
        "byte_c": byte_c,
    }, pos


def parse_target_frame(data: bytes, wrapper_pos: int) -> dict[str, object]:
    start = wrapper_pos
    opcode, pos = expect(data, start, 0x12, 2)
    if opcode != TARGET_ID:
        raise ValueError(f"offset {start}: opcode 0x{opcode:04X} is not 0x{TARGET_ID:04X}")
    version, pos = expect(data, pos, 0x0B, 1)
    result, pos = expect(data, pos, 0x08, 1)
    bag_present, pos = expect(data, pos, 0x0B, 1)

    bag_start = pos
    bag = None
    if bag_present:
        base_mask, pos = expect(data, pos, 0x0B, 1)
        base_identity, pos = expect(data, pos, 0x32, 8)
        update_count, pos = expect(data, pos, 0x0F, 2)
        updates = []
        for _ in range(update_count):
            item, pos = parse_item(data, pos)
            updates.append(item)
        removal_count, pos = expect(data, pos, 0x0F, 2)
        removals = []
        for _ in range(removal_count):
            identity, pos = expect(data, pos, 0x32, 8)
            removals.append(identity)
        bag = {
            "base_mask": base_mask,
            "base_identity": base_identity,
            "update_count": update_count,
            "updates": updates,
            "removal_count": removal_count,
            "removals": removals,
        }
    bag_end = pos

    affected_count, pos = expect(data, pos, 0x08, 1)
    affected = []
    for _ in range(affected_count):
        identity, pos = expect(data, pos, 0x32, 8)
        value, pos = expect(data, pos, 0x08, 1)
        affected.append({"identity": identity, "value": value})

    return {
        "opcode": opcode,
        "version": version,
        "result": result,
        "bag_present": bag_present,
        "bag": bag,
        "bag_hex": data[bag_start:bag_end].hex().upper(),
        "bag_len": bag_end - bag_start,
        "affected_count": affected_count,
        "affected": affected,
        "message_hex": data[start:pos].hex().upper(),
        "message_len": pos - start,
        "end": pos,
    }


def load_validator(path: Path):
    spec = importlib.util.spec_from_file_location("gt047_validator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--validator", type=Path, required=True)
    args = parser.parse_args()

    with args.inventory.open("r", encoding="utf-8", newline="") as handle:
        inventory = list(csv.DictReader(handle, delimiter="\t"))
    inventory_by_rel = {
        row["relative_path"].casefold(): row
        for row in inventory
        if row.get("source") == "CAPTURE"
    }

    validator = load_validator(args.validator)
    results = []
    for path in args.client.rglob("*.txt"):
        relative = path.relative_to(args.client).as_posix()
        row = inventory_by_rel.get(relative.casefold())
        if row is None:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "12 13 4C 0B" not in text.upper():
            continue
        actual_sha = sha256_file(path)
        if actual_sha != row["sha256"].lower() or path.stat().st_size != int(row["size"]):
            raise RuntimeError(f"inventory mismatch: {relative}")
        blocks, errors = validator.extract_pc_blocks(text)
        if errors:
            raise RuntimeError(f"capture parse error in {relative}: {dict(errors)}")
        for ordinal, (kind, data) in enumerate(blocks, 1):
            if kind != "PC":
                continue
            wrapper_pos = data.find(TARGET_WRAPPER)
            if wrapper_pos < 0:
                continue
            parsed = parse_target_frame(data, wrapper_pos)
            parsed.update(
                {
                    "relative_path": relative,
                    "sha256": actual_sha,
                    "pc_ordinal": ordinal,
                    "pc_len": len(data),
                    "wrapper_offset": wrapper_pos,
                    "tail_hex": data[int(parsed["end"]) :].hex().upper(),
                }
            )
            results.append(parsed)

    if len(results) != 5:
        raise RuntimeError(f"expected exactly 5 frames, found {len(results)}")
    if len({str(row["relative_path"]) for row in results}) != 4:
        raise RuntimeError("expected exactly 4 source files")

    print("RE059_FRAME_COUNT=5")
    print("RE059_FILE_COUNT=4")
    for index, row in enumerate(results, 1):
        print(f"FRAME={index}")
        print(f"FILE={row['relative_path']}")
        print(f"SHA256={row['sha256']}")
        print(f"PC_ORDINAL={row['pc_ordinal']}")
        print(f"PC_LEN={row['pc_len']}")
        print(f"WRAPPER_OFFSET={row['wrapper_offset']}")
        print(f"OPCODE=0x{int(row['opcode']):04X}")
        print(f"VERSION={row['version']}")
        print(f"MESSAGE_LEN={row['message_len']}")
        print(f"MESSAGE_HEX={row['message_hex']}")
        print(f"RESULT_R4={row['result']}")
        print(f"BAG_PRESENT_R5={row['bag_present']}")
        print(f"BAG_LEN={row['bag_len']}")
        print(f"BAG_HEX={row['bag_hex']}")
        bag = row["bag"]
        if bag is not None:
            print(f"BAG_BASE_MASK={bag['base_mask']}")
            print(f"BAG_BASE_IDENTITY={bag['base_identity']}")
            print(f"BAG_UPDATE_COUNT={bag['update_count']}")
            print(f"BAG_UPDATES={bag['updates']}")
            print(f"BAG_REMOVAL_COUNT={bag['removal_count']}")
            print(f"BAG_REMOVALS={bag['removals']}")
        print(f"AFFECTED_COUNT_R10={row['affected_count']}")
        print(f"AFFECTED_ELEMENTS={row['affected']}")
        print(f"OUTER_TAIL_HEX={row['tail_hex']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
