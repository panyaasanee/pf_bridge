#!/usr/bin/env python3
"""Decode Pirate Force Lua containers and native NPC scene-placement files.

This is a static, read-only extractor for GameClient inputs.  It writes only below
pf_bridge/gamedata (or the explicitly selected --out directory).

The NPC format contains two collections:
  u16 version
  u16 definition_count
  definition_count * (u32 byte_len + UTF-16LE name + 16-byte payload)
  u16 placement_count
  placement_count * variable-length NPCPlacement records

The second u16 at file offset 2 is therefore not the placement count.  Keeping
definition_count and placement_count separate is necessary for exact-EOF parsing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import random
import re
import struct
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


SCRIPT_VERSION = "1.0.0"
PCZ_MAGIC = b"$pcz"
LUA_SAMPLE_SEED = 20260824
API_RE = re.compile(
    rb"(?<![A-Za-z0-9_])"
    rb"([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)\s*\("
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_console(value: Any) -> str:
    """Return ASCII-only text so Windows cp874 consoles cannot fail."""
    return str(value).encode("ascii", errors="backslashreplace").decode("ascii")


def console(value: Any, *, error: bool = False) -> None:
    print(safe_console(value), file=sys.stderr if error else sys.stdout)


def raw_error(ex: BaseException) -> str:
    return f"{type(ex).__name__}: {ex}".replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n")


def tsv_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n")


def write_tsv(path: Path, header: Iterable[str], rows: Iterable[Iterable[Any]]) -> None:
    parts = ["\t".join(header)]
    parts.extend("\t".join(tsv_cell(v) for v in row) for row in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(("\n".join(parts) + "\n").encode("utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    path.write_bytes(data.encode("utf-8"))


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def source_manifest(entries: Iterable[tuple[str, int, str]]) -> str:
    h = hashlib.sha256()
    for rel, size, sha in sorted(entries):
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(str(size).encode("ascii"))
        h.update(b"\0")
        h.update(sha.encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def stable_generated_time(meta_path: Path, manifest_sha: str) -> str:
    """Reuse time for an unchanged source snapshot so reruns are byte-stable."""
    try:
        old = json.loads(meta_path.read_text(encoding="utf-8"))
        if (
            old.get("script_version") == SCRIPT_VERSION
            and old.get("source_manifest_sha256") == manifest_sha
            and isinstance(old.get("generated_at_plus07"), str)
        ):
            return old["generated_at_plus07"]
    except (OSError, ValueError, TypeError):
        pass
    tz_plus07 = timezone(timedelta(hours=7))
    return datetime.now(tz_plus07).isoformat(timespec="seconds")


def parse_lzma_props(props: bytes) -> dict[str, int]:
    if len(props) != 5:
        raise ValueError(f"LZMA props length {len(props)} != 5")
    first = props[0]
    if first >= 9 * 5 * 5:
        raise ValueError(f"invalid LZMA property byte 0x{first:02X}")
    lc = first % 9
    rest = first // 9
    lp = rest % 5
    pb = rest // 5
    dictionary = struct.unpack_from("<I", props, 1)[0]
    if dictionary == 0:
        raise ValueError("LZMA dictionary size is zero")
    return {"lc": lc, "lp": lp, "pb": pb, "dict_size": dictionary}


def decode_pcz(data: bytes) -> bytes:
    if len(data) < 13:
        raise ValueError(f"container too short: {len(data)} bytes")
    if data[:4] != PCZ_MAGIC:
        raise ValueError(f"bad magic {data[:4].hex()} expected {PCZ_MAGIC.hex()}")
    expected_size = struct.unpack_from("<I", data, 4)[0]
    props = parse_lzma_props(data[8:13])
    filters = [{"id": lzma.FILTER_LZMA1, **props}]
    decoder = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=filters)
    output = decoder.decompress(data[13:], max_length=expected_size + 1)
    if len(output) != expected_size:
        raise ValueError(
            f"decompressed size {len(output)} != header size {expected_size}"
        )
    return output


def _long_bracket_level(data: bytes, pos: int) -> int | None:
    if pos >= len(data) or data[pos] != ord("["):
        return None
    cursor = pos + 1
    while cursor < len(data) and data[cursor] == ord("="):
        cursor += 1
    if cursor < len(data) and data[cursor] == ord("["):
        return cursor - pos - 1
    return None


def mask_lua_comments_and_strings(data: bytes) -> bytes:
    """Mask Lua comments/strings while preserving byte positions and newlines."""
    output = bytearray(data)
    size = len(data)

    def wipe(start: int, end: int) -> None:
        for index in range(start, min(end, size)):
            if output[index] not in (10, 13):
                output[index] = 32

    pos = 0
    while pos < size:
        if data.startswith(b"--", pos):
            start = pos
            level = _long_bracket_level(data, pos + 2)
            if level is None:
                end = data.find(b"\n", pos + 2)
                end = size if end < 0 else end
            else:
                marker = b"]" + (b"=" * level) + b"]"
                close = data.find(marker, pos + 4 + level)
                end = size if close < 0 else close + len(marker)
            wipe(start, end)
            pos = end
            continue

        if data[pos] in (ord('"'), ord("'")):
            start = pos
            quote = data[pos]
            pos += 1
            while pos < size:
                if data[pos] == ord("\\"):
                    pos += 2
                    continue
                if data[pos] == quote:
                    pos += 1
                    break
                pos += 1
            wipe(start, pos)
            continue

        level = _long_bracket_level(data, pos)
        if level is not None:
            start = pos
            marker = b"]" + (b"=" * level) + b"]"
            close = data.find(marker, pos + 2 + level)
            end = size if close < 0 else close + len(marker)
            wipe(start, end)
            pos = end
            continue
        pos += 1
    return bytes(output)


def count_lua_calls(data: bytes) -> tuple[Counter[str], Counter[str]]:
    game_calls: Counter[str] = Counter()
    library_calls: Counter[str] = Counter()
    masked = mask_lua_comments_and_strings(data)
    for match in API_RE.finditer(masked):
        name = match.group(1).decode("ascii")
        root = name.split(".", 1)[0]
        if root[:1].isupper():
            game_calls[name] += 1
        else:
            library_calls[name] += 1
    return game_calls, library_calls


def looks_like_lua_source(data: bytes) -> bool:
    if not data or b"\x00" in data:
        return False
    return bool(
        re.search(
            rb"\b(function|if|return|local|Quest|Player|Mob|Trigger|Scene|Instance|Guild|Party)\b",
            data,
        )
        or data.lstrip().startswith(b"--")
    )


def process_lua(client_root: Path, out_root: Path) -> tuple[dict[str, Any], dict[str, str]]:
    script_root = client_root / "Data" / "Script"
    lua_out_root = out_root / "lua"
    lua_out_root.mkdir(parents=True, exist_ok=True)
    paths = sorted(script_root.rglob("*.lu_"), key=lambda p: relative_posix(p, client_root).casefold())

    # Phase one checks the magic of every file before decompression begins.
    source_rows: list[dict[str, Any]] = []
    initial_hashes: dict[str, str] = {}
    for path in paths:
        data = path.read_bytes()
        rel = relative_posix(path, client_root)
        sha = sha256_bytes(data)
        initial_hashes[rel] = sha
        source_rows.append(
            {
                "path": path,
                "data": data,
                "src_path": rel,
                "src_sha256": sha,
                "src_bytes": len(data),
                "magic_ok": data[:4] == PCZ_MAGIC,
            }
        )

    index_rows: list[list[Any]] = []
    errors: list[dict[str, str]] = []
    magic_failures: list[dict[str, str]] = []
    game_api_calls: Counter[str] = Counter()
    library_calls: Counter[str] = Counter()
    source_like_failures: list[str] = []
    successful_sources: list[tuple[str, bytes]] = []
    total_output_bytes = 0

    for row in source_rows:
        path = row["path"]
        src_path = row["src_path"]
        rel_output = path.relative_to(script_root).with_suffix(".lua")
        rel_output_text = rel_output.as_posix()
        output_path = lua_out_root / rel_output
        status = "OK"
        output_size: int | str = ""
        line_count: int | str = ""

        try:
            if not row["magic_ok"]:
                message = f"bad magic {row['data'][:4].hex()} expected {PCZ_MAGIC.hex()}"
                magic_failures.append({"src_path": src_path, "error": message})
                raise ValueError(message)
            decoded = decode_pcz(row["data"])
            if not looks_like_lua_source(decoded):
                source_like_failures.append(src_path)
                raise ValueError("decompressed bytes did not pass Lua source sanity check")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(decoded)
            output_size = len(decoded)
            line_count = len(decoded.splitlines())
            total_output_bytes += len(decoded)
            successful_sources.append((src_path, decoded))
            calls, std_calls = count_lua_calls(decoded)
            game_api_calls.update(calls)
            library_calls.update(std_calls)
        except Exception as ex:  # one bad input is recorded; the run exits 1 later
            message = raw_error(ex)
            status = f"ERROR: {message}"
            errors.append({"src_path": src_path, "error": message})

        index_rows.append(
            [
                rel_output_text,
                src_path,
                row["src_sha256"],
                row["src_bytes"],
                output_size,
                line_count,
                status,
            ]
        )

    write_tsv(
        out_root / "PF_GAMEDATA_LUA_INDEX.tsv",
        ["rel_path", "src_path", "src_sha256", "src_bytes", "out_bytes", "lines", "status"],
        index_rows,
    )

    manifest_sha = source_manifest(
        (row["src_path"], row["src_bytes"], row["src_sha256"]) for row in source_rows
    )
    meta_path = out_root / "_LUA_meta.json"
    ascii_sample_pool = []
    for src_path, decoded in successful_sources:
        first_five = decoded.splitlines()[:5]
        if len(first_five) == 5 and all(all(byte < 128 for byte in line) for line in first_five):
            ascii_sample_pool.append(src_path)
    sample_rng = random.Random(LUA_SAMPLE_SEED)
    sample_files = sorted(sample_rng.sample(ascii_sample_pool, min(5, len(ascii_sample_pool))))

    changed_sources = [
        rel for rel, before in initial_hashes.items() if sha256_path(client_root / Path(rel)) != before
    ]
    meta: dict[str, Any] = {
        "script": Path(__file__).name,
        "script_version": SCRIPT_VERSION,
        "generated_at_plus07": stable_generated_time(meta_path, manifest_sha),
        "source_root": "Data/Script",
        "source_manifest_sha256": manifest_sha,
        "files": len(source_rows),
        "succeeded": len(source_rows) - len(errors),
        "failed": len(errors),
        "magic_checked": len(source_rows),
        "magic_failed": len(magic_failures),
        "source_like_failed": len(source_like_failures),
        "source_bytes": sum(row["src_bytes"] for row in source_rows),
        "output_bytes": total_output_bytes,
        "game_api_unique": len(game_api_calls),
        "game_api_call_count": sum(game_api_calls.values()),
        "game_api_calls": dict(sorted(game_api_calls.items())),
        "standard_library_calls": dict(sorted(library_calls.items())),
        "sample_seed": LUA_SAMPLE_SEED,
        "sample_files": sample_files,
        "errors": errors,
        "magic_failures": magic_failures,
        "source_integrity_rechecked": len(initial_hashes),
        "source_integrity_changed": changed_sources,
    }
    write_json(meta_path, meta)
    return meta, initial_hashes


class NPCReader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def need(self, count: int, label: str) -> None:
        if count < 0 or self.pos + count > len(self.data):
            remain = len(self.data) - self.pos
            raise ValueError(
                f"{label} past EOF at 0x{self.pos:X}: need={count} remain={remain}"
            )

    def u8(self, label: str) -> int:
        self.need(1, label)
        value = self.data[self.pos]
        self.pos += 1
        return value

    def u16(self, label: str) -> int:
        self.need(2, label)
        value = struct.unpack_from("<H", self.data, self.pos)[0]
        self.pos += 2
        return value

    def u32(self, label: str) -> int:
        self.need(4, label)
        value = struct.unpack_from("<I", self.data, self.pos)[0]
        self.pos += 4
        return value

    def bytes(self, count: int, label: str) -> bytes:
        self.need(count, label)
        value = self.data[self.pos : self.pos + count]
        self.pos += count
        return value

    def utf16(self, label: str) -> str:
        length_offset = self.pos
        byte_length = self.u32(f"{label}.length")
        if byte_length % 2:
            raise ValueError(
                f"{label} odd UTF-16LE byte length {byte_length} at 0x{length_offset:X}"
            )
        raw = self.bytes(byte_length, f"{label}.data")
        try:
            return raw.decode("utf-16le", errors="strict")
        except UnicodeDecodeError as ex:
            raise ValueError(f"{label} invalid UTF-16LE at 0x{length_offset + 4:X}: {ex}") from ex

    def f32_tuple(self, count: int, label: str) -> tuple[float, ...]:
        raw = self.bytes(count * 4, label)
        return struct.unpack("<" + ("f" * count), raw)


def parse_npc(data: bytes) -> dict[str, Any]:
    reader = NPCReader(data)
    version = reader.u16("version")
    if version not in (1, 2):
        raise ValueError(f"unsupported version {version} at 0x0")

    definition_count = reader.u16("definition_count")
    definitions: list[dict[str, Any]] = []
    definition_map: dict[str, list[int]] = {}
    for index in range(definition_count):
        offset = reader.pos
        name = reader.utf16(f"definition[{index}].name")
        payload_offset = reader.pos
        payload = reader.bytes(16, f"definition[{index}].payload")
        template_id = struct.unpack_from("<I", payload, 1)[0]
        definitions.append(
            {
                "index": index,
                "offset": offset,
                "name": name,
                "payload_offset": payload_offset,
                "payload_hex": payload.hex(),
                "template_id": template_id,
            }
        )
        definition_map.setdefault(name.casefold(), []).append(template_id)

    placement_count_offset = reader.pos
    placement_count = reader.u16("placement_count")
    placements: list[dict[str, Any]] = []
    for index in range(placement_count):
        offset = reader.pos
        name = reader.utf16(f"placement[{index}].name")
        xyz_offset = reader.pos
        six_f32_raw = reader.bytes(24, f"placement[{index}].six_f32")
        six_f32 = struct.unpack("<6f", six_f32_raw)
        seven_u16 = tuple(
            reader.u16(f"placement[{index}].u16[{field}]") for field in range(7)
        )
        version2_byte = (
            reader.u8(f"placement[{index}].version2_byte") if version >= 2 else None
        )
        string_count = reader.u16(f"placement[{index}].string_count")
        strings = [
            reader.utf16(f"placement[{index}].string[{string_index}]")
            for string_index in range(string_count)
        ]
        triple_count = reader.u16(f"placement[{index}].extra_triple_count")
        extra_triples = [
            reader.f32_tuple(3, f"placement[{index}].extra_triple[{triple_index}]")
            for triple_index in range(triple_count)
        ]
        template_ids: list[str] = []
        for set_name in strings:
            ids = definition_map.get(set_name.casefold())
            template_ids.append(
                ",".join(str(value) for value in ids) if ids else "UNRESOLVED"
            )
        placements.append(
            {
                "index": index,
                "name": name,
                "offset": offset,
                "end_offset": reader.pos,
                "xyz_offset": xyz_offset,
                "six_f32": six_f32,
                "xyz_raw_hex": six_f32_raw[:12].hex(),
                "seven_u16": seven_u16,
                "version2_byte": version2_byte,
                "strings": strings,
                "template_ids": template_ids,
                "extra_triples": extra_triples,
            }
        )

    if reader.pos != len(data):
        raise ValueError(
            f"trailing bytes at 0x{reader.pos:X}: {len(data) - reader.pos} "
            f"(file size 0x{len(data):X})"
        )
    return {
        "version": version,
        "definition_count": definition_count,
        "definitions": definitions,
        "placement_count_offset": placement_count_offset,
        "placement_count": placement_count,
        "placements": placements,
        "end_offset": reader.pos,
    }


def format_extra_triples(values: list[tuple[float, ...]]) -> str:
    return ";".join(
        ",".join(repr(component) for component in triple) for triple in values
    )


def placement_rows(parsed: dict[str, Any]) -> Iterable[list[Any]]:
    for placement in parsed["placements"]:
        six = placement["six_f32"]
        fields = placement["seven_u16"]
        yield [
            placement["index"],
            placement["name"],
            f"0x{placement['offset']:08X}",
            f"0x{placement['end_offset']:08X}",
            f"0x{placement['xyz_offset']:08X}",
            repr(six[0]),
            repr(six[1]),
            repr(six[2]),
            placement["xyz_raw_hex"],
            repr(six[3]),
            repr(six[4]),
            repr(six[5]),
            *fields,
            placement["version2_byte"],
            "|".join(placement["strings"]),
            "|".join(placement["template_ids"]),
            len(placement["extra_triples"]),
            format_extra_triples(placement["extra_triples"]),
        ]


PLACEMENT_HEADER = [
    "index",
    "name",
    "offset",
    "end_offset",
    "xyz_offset",
    "x",
    "y",
    "z",
    "xyz_raw_hex",
    "f32_3",
    "f32_4",
    "f32_5",
    "u16_0",
    "u16_1",
    "u16_2",
    "u16_3",
    "u16_4",
    "u16_5",
    "u16_6",
    "version2_byte",
    "set_names",
    "template_ids",
    "extra_triple_count",
    "extra_triples_xyz",
]


def process_scenes(client_root: Path, out_root: Path) -> tuple[dict[str, Any], dict[str, str]]:
    scene_out_root = out_root / "scene"
    scene_out_root.mkdir(parents=True, exist_ok=True)
    paths = sorted(
        client_root.rglob("*.npc"),
        key=lambda p: relative_posix(p, client_root).casefold(),
    )

    initial_hashes: dict[str, str] = {}
    sources: list[dict[str, Any]] = []
    for path in paths:
        data = path.read_bytes()
        rel = relative_posix(path, client_root)
        sha = sha256_bytes(data)
        initial_hashes[rel] = sha
        sources.append(
            {"path": path, "data": data, "src_path": rel, "src_sha256": sha, "src_bytes": len(data)}
        )

    index_rows: list[list[Any]] = []
    errors: list[dict[str, str]] = []
    parsed_rows: list[tuple[dict[str, Any], dict[str, Any]]] = []
    output_keys: set[str] = set()
    outside_scene_files: list[str] = []
    scene_tree = (client_root / "Data" / "Scene").resolve()

    for source in sources:
        path = source["path"]
        scene = path.parent.name
        output_path = scene_out_root / scene / f"{path.stem}.placements.tsv"
        output_key = str(output_path.resolve()).casefold()
        status = "OK"
        parsed: dict[str, Any] | None = None
        try:
            if output_key in output_keys:
                raise ValueError(f"output path collision: {output_path}")
            output_keys.add(output_key)
            parsed = parse_npc(source["data"])
            write_tsv(output_path, PLACEMENT_HEADER, placement_rows(parsed))
            parsed_rows.append((source, parsed))
        except Exception as ex:
            message = raw_error(ex)
            status = f"ERROR: {message}"
            errors.append({"src_path": source["src_path"], "error": message})

        try:
            path.resolve().relative_to(scene_tree)
        except ValueError:
            outside_scene_files.append(source["src_path"])

        index_rows.append(
            [
                scene,
                source["src_path"],
                parsed["version"] if parsed else "",
                parsed["placement_count"] if parsed else "",
                source["src_sha256"],
                source["src_bytes"],
                status,
                parsed["definition_count"] if parsed else "",
                f"0x{parsed['placement_count_offset']:08X}" if parsed else "",
                relative_posix(output_path, out_root),
            ]
        )

    write_tsv(
        out_root / "PF_GAMEDATA_SCENE_INDEX.tsv",
        [
            "scene",
            "src_path",
            "version",
            "placement_count",
            "src_sha256",
            "src_bytes",
            "parse_status",
            "definition_count",
            "placement_count_offset",
            "output_path",
        ],
        index_rows,
    )

    bg_check: dict[str, Any] = {}
    for source, parsed in parsed_rows:
        if source["src_path"].casefold() == "data/scene/save/bg0001/bg0001.npc":
            owner = [
                row["index"]
                for row in parsed["placements"]
                if row["offset"] <= 0x1D46 < row["end_offset"]
            ]
            xyz_matches = [
                row["index"] for row in parsed["placements"] if row["xyz_offset"] == 0x1D46
            ]
            bg_check = {
                "version": parsed["version"],
                "definition_count_at_file_offset_2": parsed["definition_count"],
                "placement_count": parsed["placement_count"],
                "placement_count_offset": f"0x{parsed['placement_count_offset']:X}",
                "offset_0x1D46_owner_indices": owner,
                "offset_0x1D46_xyz_indices": xyz_matches,
                "pass_version_2": parsed["version"] == 2,
                "pass_definition_count_113": parsed["definition_count"] == 113,
                "pass_xyz_index_30": xyz_matches == [30],
            }
            if parsed["version"] != 2 or parsed["definition_count"] != 113 or xyz_matches != [30]:
                errors.append(
                    {
                        "src_path": source["src_path"],
                        "error": "bg0001 self-check failed: expected version=2, definition_count=113, xyz_offset_0x1D46=index30",
                    }
                )
            break
    if not bg_check:
        errors.append({"src_path": "Data/Scene/Save/bg0001/bg0001.npc", "error": "bg0001 self-check file missing"})

    manifest_sha = source_manifest(
        (source["src_path"], source["src_bytes"], source["src_sha256"]) for source in sources
    )
    meta_path = out_root / "_SCENE_meta.json"
    changed_sources = [
        rel for rel, before in initial_hashes.items() if sha256_path(client_root / Path(rel)) != before
    ]
    version_counts = Counter(parsed["version"] for _source, parsed in parsed_rows)
    meta: dict[str, Any] = {
        "script": Path(__file__).name,
        "script_version": SCRIPT_VERSION,
        "generated_at_plus07": stable_generated_time(meta_path, manifest_sha),
        "source_root": ".",
        "source_manifest_sha256": manifest_sha,
        "files": len(sources),
        "succeeded": len(parsed_rows),
        "failed": len(errors),
        "files_under_data_scene": len(sources) - len(outside_scene_files),
        "files_outside_data_scene": outside_scene_files,
        "versions": {str(key): value for key, value in sorted(version_counts.items())},
        "definition_count_total": sum(parsed["definition_count"] for _source, parsed in parsed_rows),
        "placement_count_total": sum(parsed["placement_count"] for _source, parsed in parsed_rows),
        "source_bytes": sum(source["src_bytes"] for source in sources),
        "output_bytes": sum(
            (scene_out_root / source["path"].parent.name / f"{source['path'].stem}.placements.tsv").stat().st_size
            for source, _parsed in parsed_rows
        ),
        "bg0001_self_check": bg_check,
        "errors": errors,
        "source_integrity_rechecked": len(initial_hashes),
        "source_integrity_changed": changed_sources,
    }
    write_json(meta_path, meta)
    return meta, initial_hashes


def main(argv: list[str] | None = None) -> int:
    script_path = Path(__file__).resolve()
    default_project = script_path.parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", type=Path, default=default_project / "GameClient")
    parser.add_argument("--out", type=Path, default=script_path.parent)
    args = parser.parse_args(argv)
    client_root = args.client.resolve()
    out_root = args.out.resolve()

    try:
        if not client_root.is_dir():
            raise FileNotFoundError(f"client root not found: {client_root}")
        out_root.mkdir(parents=True, exist_ok=True)
        lua_meta, _lua_hashes = process_lua(client_root, out_root)
        scene_meta, _scene_hashes = process_scenes(client_root, out_root)
        bg = scene_meta.get("bg0001_self_check", {})
        console(
            f"LUA files={lua_meta['files']} ok={lua_meta['succeeded']} failed={lua_meta['failed']} "
            f"api_unique={lua_meta['game_api_unique']} api_calls={lua_meta['game_api_call_count']}"
        )
        console(
            f"NPC files={scene_meta['files']} ok={scene_meta['succeeded']} failed={scene_meta['failed']} "
            f"definitions={scene_meta['definition_count_total']} placements={scene_meta['placement_count_total']}"
        )
        console(
            f"BG0001 version={bg.get('version')} definitions={bg.get('definition_count_at_file_offset_2')} "
            f"placements={bg.get('placement_count')} xyz_0x1D46_indices={bg.get('offset_0x1D46_xyz_indices')}"
        )
        changed = lua_meta["source_integrity_changed"] or scene_meta["source_integrity_changed"]
        failed = lua_meta["failed"] or scene_meta["failed"] or changed
        console("RESULT " + ("FAIL" if failed else "OK"), error=bool(failed))
        return 1 if failed else 0
    except Exception as ex:
        console(f"FATAL {raw_error(ex)}", error=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
