"""Build the V5 effective status checkpoint from the frozen V4 state.

The builder replays V4 A2 and all 519 priority states, applies the accepted
twenty-row invalid-parameter non-wire overlay and two exact priority
transitions, and publishes only the derived V5 OPEN index and status report.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
import copy
import csv
import dataclasses
import hashlib
import io
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import sys
import tempfile
from typing import Callable, Iterable, Mapping, MutableMapping, Sequence

sys.dont_write_bytecode = True

import pf_build_v4_effective_status as v4
import pf_validate_v4_effective_capture as capture_v4


OUT = Path(__file__).resolve().parent
IMAGE = OUT.parents[1] / "GameClient" / "GameClient.local.bin"
IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"

V4_MANIFEST = OUT / "PF_V4_MANIFEST.md"
V4_MANIFEST_SIZE = 20_919
V4_MANIFEST_SHA256 = "80c55db4f60739f0b1c8086cc28e568025678ce70056a9f045c3f9484443c8f3"
V4_MANIFEST_ROWS = 120
V4_INDEX = OUT / "00_SEARCH_HERE_FIRST.md"
V4_INDEX_SIZE = 14_205
V4_INDEX_SHA256 = "3c04c81025a9e7fe7f3866fc879ba3b2d0d2ea1379de445fbd379cd191d0575d"
V5_INDEX_TAIL_MARKER = (
    "<!-- PF V5 FROZEN V4 INDEX FOLLOWS: "
    f"{V4_INDEX_SIZE} bytes / SHA-256 {V4_INDEX_SHA256.upper()} -->\n"
).encode("ascii")
CANONICAL_V5_INDEX_PREFIX = (
    "# PF V5 current local index\n"
    "\n"
    "[PROPOSED][LOCAL] Read `PF_V5_HANDOFF.md` first, then "
    "`PF_V5_EFFECTIVE_STATUS.md` and `PF_V5_FIELD_VALIDATION.md`.\n"
    "\n"
    "[MEASURED][OUTPUT-AUDIT] V5 adds one IMAGE-static closure component, "
    "one derived status checkpoint, and one capture-validation report; the "
    "frozen V4 index follows byte-for-byte.\n"
    "\n"
    "[DECLARED-SCOPE] Local evidence index only; no client/server runtime, "
    "workflow, queue, lease, Git, raw capture, dump, or GameClient mutation.\n"
    "\n"
).encode("utf-8")

COMPONENT_PINS = {
    "pf_build_v5_invalid_parameter_closure.py": (
        103_855,
        "3f7c6aa4993aa9fa5f1020c0b14fdc119ab568c7e92249003776111355869d73",
    ),
    "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv": (
        14_524,
        "f3d877bbc2f3899d650286df6026d44df6691ef23b78ed3492a45da9c076d277",
    ),
    "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv": (
        1_678,
        "0d02afcbbab22506ef74a3cf50d88dd1dd5e7a2c8b85f9333397275a4996114a",
    ),
    "PF_V5_INVALID_PARAMETER_CLOSURE.md": (
        8_563,
        "12e5790c149324e971d47aae00dca36a7d369ae58ef45755a9422dc97b7f09ff",
    ),
}

A2_INPUT = OUT / "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv"
PRIORITY_INPUT = OUT / "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv"
OPEN_OUT = OUT / "PF_V5_P1_OPEN.tsv"
REPORT_OUT = OUT / "PF_V5_EFFECTIVE_STATUS.md"
OWNED_OUTPUTS = (OPEN_OUT, REPORT_OUT)
OWNED_NAMES = {path.name for path in OWNED_OUTPUTS}

LOCK_NAME = ".PF_V5_EFFECTIVE_STATUS_PUBLISH.lock"
TX_PREFIX = ".PF_V5_EFFECTIVE_STATUS_TXN."

TARGET_MESSAGES = (
    "ItemMallUpdatePersonalDataVital",
    "ServerAddedInfoVital",
)

A2_COLUMNS = (
    "delta_key", "action", "change_type", "base_file", "base_line",
    "base_row_key", "base_delta_key", "message", "direction(W/R)",
    "old_order", "old_tag", "old_field_offset", "old_len",
    "new_wire_order", "new_tag", "new_field_offset", "new_len",
    "new_gate_condition", "resolution", "evidence_ticket",
    "evidence_span_start", "evidence_span_end", "evidence_span_sha256",
    "evidence_file_off", "source",
)

PRIORITY_COLUMNS = (
    "delta_key", "action", "base_file", "base_line", "base_row_key",
    "base_delta_key", "message", "priority",
    "old_registry_identity_status", "new_registry_identity_status",
    "old_registry_identity_missing", "new_registry_identity_missing",
    "old_serializer_status", "new_serializer_status",
    "old_serializer_blockers", "new_serializer_blockers",
    "old_structural_status", "new_structural_status",
    "old_blocker", "new_blocker", "evidence_ticket", "closure_scope",
    "source",
)

ALLOWED_REPORT_LABELS = (
    "[MEASURED][IMAGE]",
    "[MEASURED][OUTPUT-AUDIT]",
    "[PROPOSED][DERIVED]",
    "[PROPOSED][LOCAL]",
    "[NONCLAIM][LOCAL]",
    "[REPRODUCTION][LOCAL]",
    "[DECLARED-SCOPE]",
)
REPORT_HEADING_ORDER = (
    "# PF V5 effective IMAGE-static status checkpoint",
    "## Priority result",
    "## Independently replayed A2 and logical views",
    "## Exact closure residuals",
    "## Priority-1 OPEN blocker groups",
    "## Duplicate and historical-reference audit",
    "## Boundaries",
)
REPORT_HEADING_SECTION = {
    heading: section for heading, section in zip(REPORT_HEADING_ORDER, (
        "preamble", "priority", "a2", "closure", "groups", "audit",
        "boundaries",
    ))
}
REPORT_SECTION_RULES = {
    "preamble": ("[PROPOSED][DERIVED]", frozenset({"plain"}), 1),
    "priority": ("[PROPOSED][DERIVED]", frozenset({"table"}), 6),
    "a2": ("[MEASURED][IMAGE]", frozenset({"table", "bullet"}), 5),
    "closure": ("[MEASURED][IMAGE]", frozenset({"table"}), 4),
    "groups": ("[PROPOSED][DERIVED]", frozenset({"table"}), 4),
    "audit": ("[MEASURED][OUTPUT-AUDIT]", frozenset({"bullet"}), 4),
    "boundaries": (None, frozenset({"plain"}), 4),
}
REPORT_TABLE_SCAFFOLD = {
    "priority": (
        "| claim | priority | V4 | V5 |",
        "|---|---|---:|---:|",
    ),
    "a2": (
        "| claim | view | rows | UNKNOWN | direct invalid | generic CALL/JUMP | numeric |",
        "|---|---|---:|---:|---:|---:|---:|",
    ),
    "closure": (
        "| claim | message | direction | effective rows | residual blockers | proven wire rows |",
        "|---|---|:---:|---:|---:|---:|",
    ),
    "groups": (
        "| claim | blocker group | rows |",
        "|---|---|---:|",
    ),
}
REPORT_TABLE_SCAFFOLD_LINES = frozenset(
    line for lines in REPORT_TABLE_SCAFFOLD.values() for line in lines
)
REPORT_BOUNDARY_LABELS = {
    "This checkpoint does not claim capture agreement, gameplay behavior, field values, import-wide classification, or a VitalData serializer.": "[NONCLAIM][LOCAL]",
    "Treat PF_V5_P1_OPEN.tsv as a derived navigation snapshot. Evidence remains in the pinned component delta and IMAGE proof report.": "[PROPOSED][LOCAL]",
    "Run `py -3 -B pf_build_v5_effective_status.py --self-test-publication`, then `--self-test-mutations`, `--audit-only`, normal publication, and `--check`.": "[REPRODUCTION][LOCAL]",
    "Local-only under pf_bridge/external; no client/server runtime, workflow, queue, lease, Git, capture, dump, index, manifest, A5 TSV, or GameClient mutation.": "[DECLARED-SCOPE]",
}
BRACKET_CLASS_RE = re.compile(r"\[[^\]\r\n]+\]")

MANIFEST_ROW_RE = re.compile(
    r"^\| `([^`]+)` \| ([0-9]+) \| `([0-9A-Fa-f]{64})` \|", re.MULTILINE
)
UNKNOWN_REASON_RE = re.compile(r"UNKNOWN\(([^)]+)\)")


class BuildError(RuntimeError):
    pass


class InjectedPublicationAbort(BaseException):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_row_key(fields: Sequence[str], row: Mapping[str, str]) -> str:
    raw = json.dumps(
        [row[name] for name in fields], ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(raw)


def read_tsv(path: Path) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise BuildError(f"bad or duplicate TSV header: {path.name}")
        fields = list(reader.fieldnames)
        rows: list[tuple[int, dict[str, str]]] = []
        for line, raw in enumerate(reader, start=2):
            if None in raw or any(value is None for value in raw.values()):
                raise BuildError(f"malformed TSV row: {path.name}:{line}")
            rows.append((line, dict(raw)))
    return fields, rows


def format_tsv(fields: Sequence[str], rows: Sequence[Mapping[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=list(fields),
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def parse_v4_manifest() -> dict[str, tuple[int, str]]:
    if (
        not V4_MANIFEST.is_file()
        or V4_MANIFEST.stat().st_size != V4_MANIFEST_SIZE
        or sha256_path(V4_MANIFEST) != V4_MANIFEST_SHA256
    ):
        raise BuildError("frozen V4 manifest identity changed")
    entries = MANIFEST_ROW_RE.findall(V4_MANIFEST.read_text(encoding="utf-8"))
    if len(entries) != V4_MANIFEST_ROWS:
        raise BuildError(f"V4 manifest row census changed: {len(entries)}")
    result: dict[str, tuple[int, str]] = {}
    for name, size_text, digest in entries:
        if name in result:
            raise BuildError(f"duplicate V4 manifest entry: {name}")
        result[name] = (int(size_text), digest.lower())
    if V4_MANIFEST.name in result or OWNED_NAMES.intersection(result):
        raise BuildError("V4 manifest namespace boundary changed")
    if result.get(V4_INDEX.name) != (V4_INDEX_SIZE, V4_INDEX_SHA256):
        raise BuildError("historical V4 index pin changed in V4 manifest")
    return result


def validate_index_bytes(current: bytes) -> str:
    current_hash = sha256_bytes(current)
    if len(current) == V4_INDEX_SIZE and current_hash == V4_INDEX_SHA256:
        return current_hash
    expected_prefix = CANONICAL_V5_INDEX_PREFIX + V5_INDEX_TAIL_MARKER
    if len(current) != len(expected_prefix) + V4_INDEX_SIZE:
        raise BuildError("superseding index byte length is not canonical")
    prefix, tail = current[:len(expected_prefix)], current[len(expected_prefix):]
    if prefix != expected_prefix:
        raise BuildError("superseding index prefix is not the exact canonical V5 prefix")
    if sha256_bytes(tail) != V4_INDEX_SHA256:
        raise BuildError("superseding index does not preserve exact frozen V4 tail")
    return current_hash


def index_prefix_self_test() -> None:
    current = V4_INDEX.read_bytes()
    validate_index_bytes(current)
    if len(current) == V4_INDEX_SIZE:
        tail = current
    else:
        tail = current[-V4_INDEX_SIZE:]
    canonical = CANONICAL_V5_INDEX_PREFIX + V5_INDEX_TAIL_MARKER + tail
    if validate_index_bytes(canonical) != sha256_bytes(canonical):
        raise BuildError("canonical V5 index-prefix acceptance changed")

    mutations = {
        "unlabelled CAPTURE index claim": canonical.replace(
            b"# PF V5 current local index\n",
            b"# PF V5 current local index\nCAPTURE proves runtime agreement.\n",
            1,
        ),
        "raw-byte-looking index claim": canonical.replace(
            b"one IMAGE-static closure component",
            b"DE AD BE EF IMAGE-static closure component",
            1,
        ),
        "mixed index evidence labels": canonical.replace(
            b"[MEASURED][OUTPUT-AUDIT]",
            b"[MEASURED][IMAGE][CAPTURE]",
            1,
        ),
        "missing index claim label": canonical.replace(
            b"[PROPOSED][LOCAL] ", b"", 1
        ),
        "changed V4 tail marker": canonical.replace(
            b"PF V5 FROZEN V4 INDEX FOLLOWS",
            b"PF V5 ALTERED V4 INDEX FOLLOWS",
            1,
        ),
    }
    for label, mutated in mutations.items():
        expect_build_error(label, lambda data=mutated: validate_index_bytes(data))


def verify_historical_index() -> str:
    if not V4_INDEX.is_file():
        raise BuildError("search index is missing")
    return validate_index_bytes(V4_INDEX.read_bytes())


def verify_inputs() -> dict[str, str]:
    entries = parse_v4_manifest()
    measured = {V4_MANIFEST.name: V4_MANIFEST_SHA256}
    for name, (expected_size, expected_hash) in entries.items():
        if name == V4_INDEX.name:
            measured[name] = verify_historical_index()
            continue
        path = OUT / name
        if not path.is_file() or path.stat().st_size != expected_size:
            raise BuildError(f"V4 namespace file missing/size drift: {name}")
        actual = sha256_path(path)
        if actual != expected_hash:
            raise BuildError(f"V4 namespace hash drift: {name}: {actual}")
        measured[name] = actual
    for name, (expected_size, expected_hash) in COMPONENT_PINS.items():
        path = OUT / name
        if not path.is_file() or path.stat().st_size != expected_size:
            raise BuildError(f"V5 component missing/size drift: {name}")
        actual = sha256_path(path)
        if actual != expected_hash:
            raise BuildError(f"V5 component hash drift: {name}: {actual}")
        measured[name] = actual
    if not IMAGE.is_file() or IMAGE.stat().st_size != IMAGE_SIZE:
        raise BuildError("pinned GameClient.local.bin size changed")
    image_hash = sha256_path(IMAGE)
    if image_hash != IMAGE_SHA256:
        raise BuildError(f"pinned GameClient.local.bin hash changed: {image_hash}")
    measured[IMAGE.name] = image_hash
    for forbidden in (
        "PF_V3_FIELD_VALIDATION.tsv",
        "PF_V4_FIELD_VALIDATION.tsv",
        "PF_V5_FIELD_VALIDATION.tsv",
    ):
        if (OUT / forbidden).exists():
            raise BuildError(f"forbidden duplicate A5 TSV exists: {forbidden}")
    return measured


def clone_effective(
    values: Mapping[tuple[str, str], Sequence[object]],
) -> dict[tuple[str, str], list[object]]:
    return {key: list(fields) for key, fields in values.items()}


def unknown_field(field: object) -> bool:
    return bool(
        getattr(field, "tag") == "UNKNOWN"
        or "UNKNOWN(" in str(getattr(field, "field_offset"))
    )


def blocker_reasons(field: object) -> tuple[str, ...]:
    reasons: set[str] = set()
    critical = (
        str(getattr(field, "tag")),
        str(getattr(field, "field_offset")),
        str(getattr(field, "length")),
        str(getattr(field, "gate_condition")),
    )
    for text in critical:
        reasons.update(UNKNOWN_REASON_RE.findall(text))
    tag = str(getattr(field, "tag"))
    if tag == "UNKNOWN":
        reasons.add("unknown_tag")
    if tag.startswith(("CALL_UNCLASSIFIED:", "JUMP_UNCLASSIFIED:")):
        reasons.add("unclassified_control_transfer")
    if tag == "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL":
        reasons.add("invalid_parameter_call_effect_unproved")
    for token in ("UNPROVED", "UNRESOLVED", "AMBIGUOUS"):
        if any(token in text.upper() for text in critical):
            reasons.add(token.lower())
    return tuple(sorted(reasons))


def is_nonempty_proven_wire(field: object) -> bool:
    if blocker_reasons(field):
        return False
    if str(getattr(field, "tag")) in {
        "EMPTY", "PURE_READONLY_CHAIN_PLUS_04_CONTAINS_PREDICATE",
    }:
        return False
    return str(getattr(field, "length")) not in {"", "0", "N/A"}


def effective_metrics(values: Mapping[tuple[str, str], Sequence[object]]) -> dict[str, int]:
    flat = [field for fields in values.values() for field in fields]
    return {
        "rows": len(flat),
        "unknown": sum(unknown_field(field) for field in flat),
        "direct_invalid": sum(
            getattr(field, "tag") == "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
            for field in flat
        ),
        "generic": sum(
            str(getattr(field, "tag")).startswith(("CALL_UNCLASSIFIED:", "JUMP_UNCLASSIFIED:"))
            for field in flat
        ),
        "numeric": sum(
            bool(capture_v4.v2.NUMERIC_TAG_RE.fullmatch(str(getattr(field, "tag"))))
            for field in flat
        ),
    }


def validate_a2_rows(rows: Sequence[Mapping[str, str]]) -> dict[str, int]:
    if len(rows) != 20:
        raise BuildError(f"V5 A2 row count changed: {len(rows)}")
    keys = [row["delta_key"] for row in rows]
    if len(set(keys)) != 20:
        raise BuildError("duplicate V5 A2 delta key")
    natural = {
        (
            row["message"], row["direction(W/R)"], row["old_order"],
            row["old_tag"], row["old_field_offset"], row["old_len"],
        )
        for row in rows
    }
    if len(natural) != 20:
        raise BuildError("duplicate V5 A2 natural removal identity")
    directions: Counter[tuple[str, str]] = Counter()
    sites: dict[tuple[str, str, str], set[str]] = {}
    site_counts: Counter[tuple[str, str, str]] = Counter()
    targets: set[tuple[str, str, str]] = set()
    for row in rows:
        if (
            row["action"] != "REMOVE_NONWIRE_ROW"
            or row["change_type"] != "V5_GUARDED_INVALID_PARAMETER_NONWIRE"
            or row["base_file"] != "PF_SERIALIZER_FIELDS.tsv"
            or row["base_delta_key"] != "N/A"
            or row["source"] != "IMAGE"
            or row["message"] not in TARGET_MESSAGES
            or row["direction(W/R)"] not in {"R", "W"}
            or row["old_tag"] != "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
            or row["old_field_offset"]
            != "UNKNOWN(invalid_parameter_import_call_wire_effect_unproved)"
            or any(row[name] != "N/A" for name in (
                "new_wire_order", "new_tag", "new_field_offset", "new_len",
                "new_gate_condition",
            ))
        ):
            raise BuildError("V5 A2 action/source/layer contract changed")
        target = (row["base_file"], row["base_line"], row["base_row_key"])
        if target in targets:
            raise BuildError(f"duplicate V5 A2 base target: {target}")
        targets.add(target)
        direction = (row["message"], row["direction(W/R)"])
        directions[direction] += 1
        site = (
            row["message"], row["evidence_span_sha256"], row["evidence_file_off"]
        )
        site_counts[site] += 1
        sites.setdefault(site, set()).add(row["direction(W/R)"])
    expected_directions = Counter({(message, direction): 5 for message in TARGET_MESSAGES for direction in ("R", "W")})
    if directions != expected_directions:
        raise BuildError(f"V5 A2 direction census changed: {dict(directions)}")
    if len(sites) != 10 or any(site_counts[key] != 2 or sites[key] != {"R", "W"} for key in sites):
        raise BuildError("V5 physical callsite pairing changed")
    return {
        "rows": len(rows), "natural": len(natural), "sites": len(sites),
        "targets": len(targets),
    }


def validate_priority_rows(rows: Sequence[Mapping[str, str]]) -> None:
    if len(rows) != 2:
        raise BuildError(f"V5 priority row count changed: {len(rows)}")
    if {row["message"] for row in rows} != set(TARGET_MESSAGES):
        raise BuildError("V5 priority message set changed")
    if len({(row["message"], row["priority"]) for row in rows}) != 2:
        raise BuildError("duplicate V5 priority natural identity")
    if len({row["delta_key"] for row in rows}) != 2:
        raise BuildError("duplicate V5 priority delta key")
    for row in rows:
        if (
            row["action"] != "CHANGED"
            or row["source"] != "IMAGE"
            or row["base_file"] != "PF_V4_P1_OPEN.tsv"
            or row["priority"] != "1"
            or row["old_registry_identity_status"] != "KNOWN"
            or row["new_registry_identity_status"] != "KNOWN"
            or row["old_registry_identity_missing"] != "N/A"
            or row["new_registry_identity_missing"] != "N/A"
            or row["old_serializer_status"] != "OPEN"
            or row["new_serializer_status"] != "CLOSED"
            or row["old_structural_status"] != "OPEN"
            or row["new_structural_status"] != "CLOSED"
            or row["old_serializer_blockers"]
            != "invalid_parameter_import_call_wire_effect_unproved"
            or row["old_blocker"]
            != "invalid_parameter_import_call_wire_effect_unproved"
            or row["new_serializer_blockers"] != "N/A"
            or row["new_blocker"] != "N/A"
            or "FULL_V4_A2_REPLAY" not in row["closure_scope"]
            or "ZERO_RESIDUAL_BLOCKERS" not in row["closure_scope"]
            or "NONEMPTY_WIRE_ROWS_REMAIN" not in row["closure_scope"]
        ):
            raise BuildError(f"V5 priority contract changed: {row['message']}")


def load_component_rows() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    a2_fields, a2_numbered = read_tsv(A2_INPUT)
    priority_fields, priority_numbered = read_tsv(PRIORITY_INPUT)
    if tuple(a2_fields) != A2_COLUMNS:
        raise BuildError("V5 A2 schema changed")
    if tuple(priority_fields) != PRIORITY_COLUMNS:
        raise BuildError("V5 priority schema changed")
    a2_rows = [row for _line, row in a2_numbered]
    priority_rows = [row for _line, row in priority_numbered]
    validate_a2_rows(a2_rows)
    validate_priority_rows(priority_rows)
    return a2_rows, priority_rows


def scan_v4_overlay_identity(
    entries: Mapping[str, tuple[int, str]],
) -> tuple[set[str], set[tuple[str, str, str]]]:
    keys: set[str] = set()
    targets: set[tuple[str, str, str]] = set()
    for name in sorted(entries):
        if not name.lower().endswith(".tsv"):
            continue
        fields, numbered = read_tsv(OUT / name)
        for line, row in numbered:
            for key_name in ("delta_key", "dedup_key"):
                value = row.get(key_name, "N/A")
                if value not in {"", "N/A"}:
                    if value in keys:
                        raise BuildError(f"V4 provenance collision: {name}:{line}:{value}")
                    keys.add(value)
            if all(row.get(column, "N/A") not in {"", "N/A"} for column in (
                "base_file", "base_line", "base_row_key",
            )):
                target = (row["base_file"], row["base_line"], row["base_row_key"])
                if target in targets:
                    raise BuildError(f"V4 base-target collision: {name}:{line}:{target}")
                targets.add(target)
    if len(keys) != 3404 or len(targets) != 576:
        raise BuildError(f"frozen V4 identity census changed: keys={len(keys)} targets={len(targets)}")
    return keys, targets


def audit_new_overlay_identity(
    entries: Mapping[str, tuple[int, str]],
    a2_rows: Sequence[Mapping[str, str]],
    priority_rows: Sequence[Mapping[str, str]],
) -> None:
    prior_keys, prior_targets = scan_v4_overlay_identity(entries)
    rows = list(a2_rows) + list(priority_rows)
    keys = [row["delta_key"] for row in rows]
    targets = [(row["base_file"], row["base_line"], row["base_row_key"]) for row in rows]
    if len(keys) != 22 or len(set(keys)) != 22 or prior_keys.intersection(keys):
        raise BuildError("V5 provenance keys collide with frozen V4")
    if len(targets) != 22 or len(set(targets)) != 22 or prior_targets.intersection(targets):
        raise BuildError("V5 base targets collide with frozen V4")


def exact_base_row(
    row: Mapping[str, str],
    fields: Sequence[str],
    by_line: Mapping[int, Mapping[str, str]],
) -> Mapping[str, str]:
    try:
        line = int(row["base_line"])
    except ValueError as exc:
        raise BuildError("V5 A2 base line is not numeric") from exc
    source = by_line.get(line)
    if source is None or canonical_row_key(fields, source) != row["base_row_key"]:
        raise BuildError(f"V5 A2 base target drift: {row['message']}:{row['base_line']}")
    declared = (
        row["message"], row["direction(W/R)"], row["old_order"], row["old_tag"],
        row["old_field_offset"], row["old_len"],
    )
    actual = (
        source["message"], source["direction(W/R)"], source["order"], source["tag"],
        source["field_offset"], source["len"],
    )
    if declared != actual:
        raise BuildError(f"V5 A2 source contract drift: {row['message']}:{row['base_line']}")
    return source


def apply_v5_removals(
    stored: MutableMapping[tuple[str, str], list[object]],
    logical: MutableMapping[tuple[str, str], list[object]],
    rows: Sequence[Mapping[str, str]],
) -> list[tuple[tuple[str, str], object, object]]:
    validate_a2_rows(rows)
    base_fields, base_numbered = read_tsv(OUT / "PF_SERIALIZER_FIELDS.tsv")
    base_by_line = {line: row for line, row in base_numbered}
    removed: list[tuple[tuple[str, str], object, object]] = []
    for row in rows:
        exact_base_row(row, base_fields, base_by_line)
        key = (row["message"], row["direction(W/R)"])
        stored_matches = [
            field for field in stored.get(key, [])
            if getattr(field, "evidence_key") == row["base_row_key"]
        ]
        logical_matches = [
            field for field in logical.get(key, [])
            if getattr(field, "evidence_key") == row["base_row_key"]
        ]
        if len(stored_matches) != 1 or len(logical_matches) != 1:
            raise BuildError(
                f"V5 removal is not uniquely effective: {key}:{row['base_row_key']}"
            )
        stored_field, logical_field = stored_matches[0], logical_matches[0]
        for field in (stored_field, logical_field):
            actual = (
                str(getattr(field, "origin_order")), getattr(field, "tag"),
                getattr(field, "field_offset"), str(getattr(field, "length")),
            )
            declared = (
                row["old_order"], row["old_tag"], row["old_field_offset"],
                row["old_len"],
            )
            if actual != declared:
                raise BuildError(f"V5 effective old-row contract drift: {key}")
        stored[key].remove(stored_field)
        logical[key].remove(logical_field)
        removed.append((key, stored_field, logical_field))
    if len(removed) != 20:
        raise BuildError("V5 exact removal count changed")
    return removed


def validate_closure(
    stored: Mapping[tuple[str, str], Sequence[object]],
) -> dict[str, dict[str, dict[str, int]]]:
    expected_rows = {
        ("ServerAddedInfoVital", "R"): 3,
        ("ServerAddedInfoVital", "W"): 3,
        ("ItemMallUpdatePersonalDataVital", "R"): 9,
        ("ItemMallUpdatePersonalDataVital", "W"): 9,
    }
    result: dict[str, dict[str, dict[str, int]]] = {}
    for message in TARGET_MESSAGES:
        result[message] = {}
        for direction in ("R", "W"):
            key = (message, direction)
            fields = list(stored.get(key, ()))
            blockers = [field for field in fields if blocker_reasons(field)]
            proven_wire = [field for field in fields if is_nonempty_proven_wire(field)]
            if blockers:
                raise BuildError(f"V5 claimed closure retains blockers: {key}:{len(blockers)}")
            if not proven_wire:
                raise BuildError(f"V5 claimed closure has no proven wire rows: {key}")
            if len(fields) != expected_rows[key]:
                raise BuildError(f"V5 residual row census changed: {key}:{len(fields)}")
            result[message][direction] = {
                "rows": len(fields), "blockers": 0, "wire": len(proven_wire),
            }
    return result


def replay_v4_open() -> tuple[
    list[dict[str, str]],
    Counter[str],
    dict[str, dict[str, object]],
    dict[str, int],
]:
    base_fields, base_numbered = read_tsv(OUT / "PF_PROTOCOL_PRIORITY.tsv")
    if len(base_numbered) != 519 or len({row["message"] for _line, row in base_numbered}) != 519:
        raise BuildError("V1 priority universe changed")
    priority_totals = Counter(int(row["priority"]) for _line, row in base_numbered)
    if priority_totals != Counter({1: 365, 2: 16, 3: 138}):
        raise BuildError(f"priority universe totals changed: {dict(priority_totals)}")
    _effective, _candidates, _metrics, residuals = v4.apply_v4_a2()
    static_rows = v4.build_static_priority()
    captured: list[tuple[dict[str, dict[str, object]], dict[str, int]]] = []
    original_checkpoint_builder = v4.build_checkpoint_rows

    def capture_checkpoint(
        states: Mapping[str, Mapping[str, object]],
        base_lines: Mapping[str, int],
    ) -> list[dict[str, str]]:
        captured.append((copy.deepcopy(dict(states)), dict(base_lines)))
        return original_checkpoint_builder(states, base_lines)

    v4.build_checkpoint_rows = capture_checkpoint
    try:
        rows, groups, inherited = v4.replay_status(static_rows, residuals)
    finally:
        v4.build_checkpoint_rows = original_checkpoint_builder
    if inherited != 107 or len(rows) != 110:
        raise BuildError("V4 full status replay census changed")
    expected = format_tsv(v4.OPEN_COLUMNS, rows)
    if (OUT / "PF_V4_P1_OPEN.tsv").read_bytes() != expected:
        raise BuildError("V4 replay no longer reproduces frozen OPEN snapshot")
    if len(captured) != 2:
        raise BuildError(f"full priority-state capture count changed: {len(captured)}")
    states, base_lines = captured[-1]
    if len(states) != 519 or len(base_lines) != 519:
        raise BuildError("full V4 priority-state capture is incomplete")
    measured = v4.status_counts(states)
    if measured != {1: (255, 365), 2: (8, 16), 3: (71, 138)}:
        raise BuildError(f"captured V4 priority census changed: {measured}")
    return rows, groups, states, base_lines


def apply_priority_transitions(
    v4_rows: Sequence[Mapping[str, str]],
    priority_rows: Sequence[Mapping[str, str]],
    closure: Mapping[str, Mapping[str, Mapping[str, int]]],
    v4_states: Mapping[str, Mapping[str, object]],
    base_lines: Mapping[str, int],
) -> tuple[
    list[dict[str, str]],
    Counter[str],
    dict[int, tuple[int, int]],
]:
    validate_priority_rows(priority_rows)
    line_map = {line: row for line, row in enumerate(v4_rows, start=2)}
    states = copy.deepcopy(dict(v4_states))
    if len(states) != 519 or set(states) != set(base_lines):
        raise BuildError("V5 full priority-state universe changed")
    closed: set[str] = set()
    for overlay_line, overlay in enumerate(priority_rows, start=2):
        try:
            line = int(overlay["base_line"])
        except ValueError as exc:
            raise BuildError("V5 priority base line is not numeric") from exc
        base = line_map.get(line)
        if base is None:
            raise BuildError(f"V5 priority predecessor line missing: {line}")
        message = overlay["message"]
        state = states.get(message)
        if state is None:
            raise BuildError(f"V5 priority state is missing: {message}")
        if (
            base["message"] != message
            or canonical_row_key(v4.OPEN_COLUMNS, base) != overlay["base_row_key"]
            or base["status_key"] != overlay["base_delta_key"]
            or base["priority"] != overlay["priority"]
            or base["effective_registry_identity_status"]
            != overlay["old_registry_identity_status"]
            or base["effective_registry_identity_missing"]
            != overlay["old_registry_identity_missing"]
            or base["effective_serializer_status"] != overlay["old_serializer_status"]
            or base["effective_structural_status"] != overlay["old_structural_status"]
            or base["effective_blocker"] != overlay["old_blocker"]
            or base["effective_blocker"] != overlay["old_serializer_blockers"]
            or state["priority"] != overlay["priority"]
            or state["registry_identity_status"]
            != overlay["old_registry_identity_status"]
            or state["registry_identity_missing"]
            != overlay["old_registry_identity_missing"]
            or state["serializer_status"] != overlay["old_serializer_status"]
            or state["serializer_blockers"]
            != overlay["old_serializer_blockers"]
            or state["structural_status"] != overlay["old_structural_status"]
            or state["blocker"] != overlay["old_blocker"]
        ):
            raise BuildError(f"V5 stale/incorrect status predecessor: {message}")
        if message not in closure or any(
            closure[message][direction]["blockers"] != 0
            or closure[message][direction]["wire"] <= 0
            for direction in ("R", "W")
        ):
            raise BuildError(f"V5 priority closure lacks A2 proof: {message}")
        if message in closed:
            raise BuildError(f"duplicate V5 priority transition: {message}")
        closed.add(message)
        state["registry_identity_status"] = overlay["new_registry_identity_status"]
        state["registry_identity_missing"] = overlay["new_registry_identity_missing"]
        state["serializer_status"] = overlay["new_serializer_status"]
        state["serializer_blockers"] = overlay["new_serializer_blockers"]
        state["structural_status"] = overlay["new_structural_status"]
        state["blocker"] = overlay["new_blocker"]
        state["chain"].append(PRIORITY_INPUT.name)  # type: ignore[union-attr]
        state["last_ref_file"] = PRIORITY_INPUT.name
        state["last_ref_line"] = str(overlay_line)
        state["last_ref_key"] = canonical_row_key(PRIORITY_COLUMNS, overlay)
        state["last_delta_key"] = overlay["delta_key"]
    if closed != set(TARGET_MESSAGES):
        raise BuildError("V5 exact priority closure set changed")
    priority_counts = v4.status_counts(states)
    expected_priority = {1: (257, 365), 2: (8, 16), 3: (71, 138)}
    if priority_counts != expected_priority:
        raise BuildError(f"V5 full priority census mismatch: {priority_counts}")
    rebuilt = v4.build_checkpoint_rows(states, base_lines)
    retained = [dict(row) for row in v4_rows if row["message"] not in closed]
    if rebuilt != retained:
        raise BuildError("V5 full-state replay did not preserve retained V4 snapshots")
    if len(retained) != 108:
        raise BuildError(f"V5 OPEN count changed: {len(retained)}")
    if len({row["message"] for row in retained}) != 108:
        raise BuildError("duplicate V5 OPEN message")
    if len({row["status_key"] for row in retained}) != 108:
        raise BuildError("duplicate V5 OPEN status key")
    for row in retained:
        if (
            row["row_semantics"]
            != "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW"
            or row["source"] != "IMAGE"
        ):
            raise BuildError("V5 retained status row lost derived-reference marker")
    groups = Counter(row["primary_blocker_group"] for row in retained)
    expected_groups = Counter({
        "CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED": 12,
        "DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED": 79,
        "OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED": 7,
        "REGISTRY_IDENTITY_UNRESOLVED": 10,
    })
    if groups != expected_groups:
        raise BuildError(f"V5 blocker group census changed: {dict(groups)}")
    return retained, groups, priority_counts


def audit_status_history(v5_rows: Sequence[Mapping[str, str]]) -> dict[str, int]:
    names = ("PF_V2_P1_OPEN.tsv", "PF_V3_P1_OPEN.tsv", "PF_V4_P1_OPEN.tsv")
    sets: dict[str, set[str]] = {}
    for name in names:
        _fields, numbered = read_tsv(OUT / name)
        rows = [row for _line, row in numbered]
        if any(
            row.get("row_semantics")
            != "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW"
            for row in rows
        ):
            raise BuildError(f"historical status snapshot marker changed: {name}")
        keys = {row["status_key"] for row in rows}
        if len(keys) != len(rows):
            raise BuildError(f"duplicate status key within historical snapshot: {name}")
        sets[name] = keys
    sets[OPEN_OUT.name] = {row["status_key"] for row in v5_rows}
    expected_sizes = {
        "PF_V2_P1_OPEN.tsv": 115,
        "PF_V3_P1_OPEN.tsv": 111,
        "PF_V4_P1_OPEN.tsv": 110,
        OPEN_OUT.name: 108,
    }
    if {name: len(values) for name, values in sets.items()} != expected_sizes:
        raise BuildError("status snapshot size census changed")
    expected_pairs = {
        ("PF_V2_P1_OPEN.tsv", "PF_V3_P1_OPEN.tsv"): 95,
        ("PF_V2_P1_OPEN.tsv", "PF_V4_P1_OPEN.tsv"): 92,
        ("PF_V2_P1_OPEN.tsv", OPEN_OUT.name): 92,
        ("PF_V3_P1_OPEN.tsv", "PF_V4_P1_OPEN.tsv"): 107,
        ("PF_V3_P1_OPEN.tsv", OPEN_OUT.name): 105,
        ("PF_V4_P1_OPEN.tsv", OPEN_OUT.name): 108,
    }
    for pair, expected in expected_pairs.items():
        if len(sets[pair[0]].intersection(sets[pair[1]])) != expected:
            raise BuildError(f"historical status-key intersection changed: {pair}")
    multiplicity = Counter(key for values in sets.values() for key in values)
    multiplicity_census = Counter(multiplicity.values())
    if multiplicity_census != Counter({1: 21, 2: 8, 3: 13, 4: 92}):
        raise BuildError(f"historical status-key multiplicity changed: {dict(multiplicity_census)}")
    repeated = [count for count in multiplicity.values() if count > 1]
    measured = {
        "distinct": len(repeated),
        "occurrences": sum(repeated),
        "extras": sum(count - 1 for count in repeated),
    }
    if measured != {"distinct": 113, "occurrences": 423, "extras": 310}:
        raise BuildError(f"historical status-key repeat census changed: {measured}")
    return measured


def expect_build_error(label: str, callback: Callable[[], object]) -> None:
    try:
        callback()
    except BuildError:
        return
    raise BuildError(f"mutation guard failed open: {label}")


def mutation_self_test(
    stored_v4: Mapping[tuple[str, str], Sequence[object]],
    logical_v4: Mapping[tuple[str, str], Sequence[object]],
    a2_rows: Sequence[Mapping[str, str]],
    priority_rows: Sequence[Mapping[str, str]],
    v4_open: Sequence[Mapping[str, str]],
    v4_states: Mapping[str, Mapping[str, object]],
    base_lines: Mapping[str, int],
) -> None:
    missing = [dict(row) for row in a2_rows]
    missing[0]["base_row_key"] = "0" * 64
    expect_build_error(
        "missing A2 base target",
        lambda: apply_v5_removals(
            clone_effective(stored_v4), clone_effective(logical_v4), missing
        ),
    )

    duplicate = [dict(row) for row in a2_rows] + [dict(a2_rows[0])]
    expect_build_error("duplicate A2 row", lambda: validate_a2_rows(duplicate))

    stored = clone_effective(stored_v4)
    logical = clone_effective(logical_v4)
    removed = apply_v5_removals(stored, logical, a2_rows)
    key, stored_field, _logical_field = removed[0]
    stored[key].append(stored_field)
    expect_build_error("residual blocker", lambda: validate_closure(stored))

    good_stored = clone_effective(stored_v4)
    good_logical = clone_effective(logical_v4)
    apply_v5_removals(good_stored, good_logical, a2_rows)
    closure = validate_closure(good_stored)

    mutation_key = ("ServerAddedInfoVital", "R")
    if sum(is_nonempty_proven_wire(field) for field in good_stored[mutation_key]) < 2:
        raise BuildError("residual mutation test lacks independent proven wire control")

    length_only = clone_effective(good_stored)
    length_only[mutation_key][0] = dataclasses.replace(
        length_only[mutation_key][0], length="UNKNOWN(length_only_residual)"
    )
    expect_build_error(
        "length-only residual blocker",
        lambda: validate_closure(length_only),
    )

    gate_only = clone_effective(good_stored)
    gate_only[mutation_key][0] = dataclasses.replace(
        gate_only[mutation_key][0],
        gate_condition="UNKNOWN(gate_only_residual)",
    )
    expect_build_error(
        "gate-only residual blocker",
        lambda: validate_closure(gate_only),
    )

    unclassified = clone_effective(good_stored)
    unclassified[mutation_key][0] = dataclasses.replace(
        unclassified[mutation_key][0], tag="CALL_UNCLASSIFIED:0xDEADBEEF"
    )
    expect_build_error(
        "unclassified-tag residual blocker",
        lambda: validate_closure(unclassified),
    )

    masked = clone_effective(good_stored)
    masked[mutation_key][0] = dataclasses.replace(
        masked[mutation_key][0], gate_condition="AMBIGUOUS_SYNTHETIC_ALIAS"
    )
    if not any(is_nonempty_proven_wire(field) for field in masked[mutation_key][1:]):
        raise BuildError("masking mutation lost its independent proven wire row")
    expect_build_error(
        "residual masked by another proven wire row",
        lambda: validate_closure(masked),
    )

    stale = [dict(row) for row in priority_rows]
    stale[0]["base_row_key"] = "f" * 64
    expect_build_error(
        "stale status predecessor",
        lambda: apply_priority_transitions(
            v4_open, stale, closure, v4_states, base_lines
        ),
    )
    index_prefix_self_test()


def report_text(
    priority_counts: Mapping[int, tuple[int, int]],
    stored: Mapping[str, int],
    logical: Mapping[str, int],
    plans: Mapping[str, int],
    groups: Mapping[str, int],
    closure: Mapping[str, Mapping[str, Mapping[str, int]]],
    history: Mapping[str, int],
) -> bytes:
    overall_closed = sum(value[0] for value in priority_counts.values())
    overall_total = sum(value[1] for value in priority_counts.values())
    overall_open = overall_total - overall_closed
    lines = [
        "# PF V5 effective IMAGE-static status checkpoint",
        "",
        "[PROPOSED][DERIVED] Full V4 A2 and all 519 priority states were replayed before the accepted 20-row removal and two exact P1 transitions were applied.",
        "",
        "## Priority result",
        "",
        "| claim | priority | V4 | V5 |",
        "|---|---|---:|---:|",
        f"| [PROPOSED][DERIVED] | P1 CLOSED / total | 255 / 365 | {priority_counts[1][0]} / {priority_counts[1][1]} |",
        f"| [PROPOSED][DERIVED] | P1 OPEN | 110 | {priority_counts[1][1] - priority_counts[1][0]} |",
        f"| [PROPOSED][DERIVED] | P2 CLOSED / total | 8 / 16 | {priority_counts[2][0]} / {priority_counts[2][1]} |",
        f"| [PROPOSED][DERIVED] | P3 CLOSED / total | 71 / 138 | {priority_counts[3][0]} / {priority_counts[3][1]} |",
        f"| [PROPOSED][DERIVED] | overall CLOSED / total | 334 / 519 | {overall_closed} / {overall_total} |",
        f"| [PROPOSED][DERIVED] | overall OPEN | 185 | {overall_open} |",
        "",
        "## Independently replayed A2 and logical views",
        "",
        "| claim | view | rows | UNKNOWN | direct invalid | generic CALL/JUMP | numeric |",
        "|---|---|---:|---:|---:|---:|---:|",
        f"| [MEASURED][IMAGE] | stored/reference | {stored['rows']} | {stored['unknown']} | {stored['direct_invalid']} | {stored['generic']} | {stored['numeric']} |",
        f"| [MEASURED][IMAGE] | logical validation | {logical['rows']} | {logical['unknown']} | {logical['direct_invalid']} | {logical['generic']} | {logical['numeric']} |",
        "",
        f"- [MEASURED][IMAGE] Schema plans: APPLICABLE {plans['APPLICABLE']}; STATIC_OPEN {plans['STATIC_OPEN']}; SCHEMA_NOT_APPLIED {plans['SCHEMA_NOT_APPLIED']}.",
        "- [MEASURED][IMAGE] Composition remains four references plus two removals; no child field is copied into stored A2.",
        "- [MEASURED][IMAGE] ItemAttr variants remain 13R+13W and 15R+15W; VitalData remains withheld with no activated schema.",
        "",
        "## Exact closure residuals",
        "",
        "| claim | message | direction | effective rows | residual blockers | proven wire rows |",
        "|---|---|:---:|---:|---:|---:|",
    ]
    for message in TARGET_MESSAGES:
        for direction in ("R", "W"):
            values = closure[message][direction]
            lines.append(
                f"| [MEASURED][IMAGE] | `{message}` | {direction} | {values['rows']} | {values['blockers']} | {values['wire']} |"
            )
    lines.extend([
        "",
        "## Priority-1 OPEN blocker groups",
        "",
        "| claim | blocker group | rows |",
        "|---|---|---:|",
    ])
    for name in sorted(groups):
        lines.append(f"| [PROPOSED][DERIVED] | `{name}` | {groups[name]} |")
    lines.extend([
        "",
        "## Duplicate and historical-reference audit",
        "",
        "- [MEASURED][OUTPUT-AUDIT] V5 component natural removals are 20/20 unique; physical IMAGE sites are 10 unique pairs with exact R+W legacy-row coverage; priority natural identities are 2/2 unique.",
        f"- [MEASURED][OUTPUT-AUDIT] Historical status-key repetition is {history['distinct']} distinct / {history['occurrences']} occurrences / {history['extras']} extras, confined to labelled V2-V5 derived status snapshots.",
        "- [MEASURED][OUTPUT-AUDIT] PF_V5_P1_OPEN.tsv contains 108 byte-identical retained V4 rows and no new evidence row.",
        "- [MEASURED][OUTPUT-AUDIT] Canonical A5 remains PF_V2_FIELD_VALIDATION.tsv; this builder emits no A5 TSV and accepts no V3/V4/V5 duplicate A5 TSV.",
        "",
        "## Boundaries",
        "",
        "[NONCLAIM][LOCAL] This checkpoint does not claim capture agreement, gameplay behavior, field values, import-wide classification, or a VitalData serializer.",
        "",
        "[PROPOSED][LOCAL] Treat PF_V5_P1_OPEN.tsv as a derived navigation snapshot. Evidence remains in the pinned component delta and IMAGE proof report.",
        "",
        "[REPRODUCTION][LOCAL] Run `py -3 -B pf_build_v5_effective_status.py --self-test-publication`, then `--self-test-mutations`, `--audit-only`, normal publication, and `--check`.",
        "",
        "[DECLARED-SCOPE] Local-only under pf_bridge/external; no client/server runtime, workflow, queue, lease, Git, capture, dump, index, manifest, A5 TSV, or GameClient mutation.",
        "",
    ])
    return "\n".join(lines).encode("utf-8")


def audit_report_labels(report: bytes) -> Counter[str]:
    text = report.decode("utf-8")
    if "[MEASURED][CAPTURE]" in text or "IMAGE+CAPTURE" in text:
        raise BuildError("status report mixes IMAGE and CAPTURE evidence")
    counts: Counter[str] = Counter()
    section_counts: Counter[str] = Counter()
    headings: list[str] = []
    scaffold_seen: dict[str, list[str]] = {
        section: [] for section in REPORT_TABLE_SCAFFOLD
    }
    current_section: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            if stripped not in REPORT_HEADING_SECTION:
                raise BuildError(
                    f"non-canonical or actionable report heading: {stripped}"
                )
            headings.append(stripped)
            current_section = REPORT_HEADING_SECTION[stripped]
            continue
        if stripped in REPORT_TABLE_SCAFFOLD_LINES:
            expected = REPORT_TABLE_SCAFFOLD.get(current_section or "", ())
            seen = scaffold_seen.get(current_section or "", [])
            if len(seen) >= len(expected) or stripped != expected[len(seen)]:
                raise BuildError(
                    f"report table scaffold in wrong section/order: {stripped}"
                )
            seen.append(stripped)
            continue
        if current_section is None:
            raise BuildError("actionable report content precedes canonical title")
        content = stripped
        line_kind = "plain"
        if content.startswith("- "):
            content = content[2:]
            line_kind = "bullet"
        elif content.startswith("|"):
            content = content[1:].lstrip()
            line_kind = "table"
        matching = [
            value for value in ALLOWED_REPORT_LABELS
            if content.startswith(value)
        ]
        if len(matching) != 1:
            raise BuildError(f"unlabelled actionable report line: {stripped[:120]}")
        label = matching[0]
        remainder = content[len(label):]
        if not remainder.startswith(" "):
            raise BuildError(f"malformed report claim-label boundary: {stripped[:120]}")
        if BRACKET_CLASS_RE.search(remainder):
            raise BuildError(f"extra or mixed report claim class: {stripped[:120]}")
        expected_label, allowed_kinds, _expected_count = REPORT_SECTION_RULES[
            current_section
        ]
        if line_kind not in allowed_kinds:
            raise BuildError(
                f"wrong actionable line shape in {current_section}: {stripped[:120]}"
            )
        claim_text = remainder[1:]
        if current_section == "boundaries":
            expected_label = REPORT_BOUNDARY_LABELS.get(claim_text)
            if expected_label is None:
                raise BuildError(f"unknown boundary claim: {stripped[:120]}")
        if label != expected_label:
            raise BuildError(
                f"wrong report claim class in {current_section}: "
                f"expected {expected_label}, got {label}"
            )
        counts[label] += 1
        section_counts[current_section] += 1
    if tuple(headings) != REPORT_HEADING_ORDER:
        raise BuildError(f"report heading order/census changed: {headings}")
    for section, expected in REPORT_TABLE_SCAFFOLD.items():
        if tuple(scaffold_seen[section]) != expected:
            raise BuildError(f"report table scaffold census changed: {section}")
    expected_sections = Counter({
        section: rule[2] for section, rule in REPORT_SECTION_RULES.items()
    })
    if section_counts != expected_sections:
        raise BuildError(
            f"report actionable section census changed: {dict(section_counts)}"
        )
    expected_labels: Counter[str] = Counter()
    for expected_label, _kinds, expected_count in REPORT_SECTION_RULES.values():
        if expected_label is not None:
            expected_labels[expected_label] += expected_count
    expected_labels.update(REPORT_BOUNDARY_LABELS.values())
    if counts != expected_labels:
        raise BuildError(f"status report label-class census changed: {dict(counts)}")
    return counts


def report_label_self_test(report: bytes) -> None:
    text = report.decode("utf-8")
    audit_report_labels(report)
    lines = text.splitlines()
    actionable: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        content = line.strip()
        if content.startswith("- "):
            content = content[2:]
        elif content.startswith("|"):
            content = content[1:].lstrip()
        matching = [
            label for label in ALLOWED_REPORT_LABELS if content.startswith(label)
        ]
        if len(matching) == 1:
            actionable.append((index, matching[0]))
    if len(actionable) != sum(rule[2] for rule in REPORT_SECTION_RULES.values()):
        raise BuildError("label self-test actionable-line census changed")

    for index, expected in actionable:
        for replacement in ALLOWED_REPORT_LABELS:
            if replacement == expected:
                continue
            mutated = list(lines)
            mutated[index] = mutated[index].replace(expected, replacement, 1)
            expect_build_error(
                f"allowed-class substitution line {index + 1}: {replacement}",
                lambda value="\n".join(mutated).encode("utf-8"):
                    audit_report_labels(value),
            )
        for suffix in ("[CAPTURE]", "[proposed][local]"):
            mutated = list(lines)
            mutated[index] = mutated[index].replace(
                expected, expected + suffix, 1
            )
            expect_build_error(
                f"additional bracket class line {index + 1}: {suffix}",
                lambda value="\n".join(mutated).encode("utf-8"):
                    audit_report_labels(value),
            )
        mutated = list(lines)
        mutated[index] = mutated[index].replace(expected, "", 1)
        expect_build_error(
            f"claim-class removal line {index + 1}",
            lambda value="\n".join(mutated).encode("utf-8"):
                audit_report_labels(value),
        )

    actionable_heading = text.replace(
        "## Priority result", "## All serializers are proven safe", 1
    ).encode("utf-8")
    expect_build_error(
        "actionable heading substitution",
        lambda: audit_report_labels(actionable_heading),
    )

    wrong_class = text.replace(
        "[PROPOSED][DERIVED]", "[MEASURED][DERIVED]", 1
    ).encode("utf-8")
    expect_build_error(
        "wrong report claim class", lambda: audit_report_labels(wrong_class)
    )


def derive(run_mutations: bool = True) -> tuple[dict[Path, bytes], dict[str, object]]:
    before = verify_inputs()
    entries = parse_v4_manifest()
    a2_rows, priority_rows = load_component_rows()
    audit_new_overlay_identity(entries, a2_rows, priority_rows)

    capture_v4.verify_classmap_boundary(OUT)
    registry, stored_v4, candidates, overlay_counts, references, v4_details = (
        capture_v4.apply_daily_and_composition(OUT)
    )
    capture_v4.verify_item_variants(candidates)
    logical_v4, expansion_details = capture_v4.expand_logical_references(
        stored_v4, references
    )
    if len(references) != 4:
        raise BuildError("V4 composition reference census changed")
    if (
        overlay_counts.get("v4_daily_removed") != 12
        or overlay_counts.get("v4_composition_changed") != 4
        or overlay_counts.get("v4_composition_removed") != 2
    ):
        raise BuildError("V4 overlay replay census changed")

    stored = clone_effective(stored_v4)
    logical = clone_effective(logical_v4)
    apply_v5_removals(stored, logical, a2_rows)
    stored_metrics = effective_metrics(stored)
    logical_metrics = effective_metrics(logical)
    if stored_metrics != {
        "rows": 8637, "unknown": 3943, "direct_invalid": 861,
        "generic": 1312, "numeric": 4081,
    }:
        raise BuildError(f"V5 stored A2 census mismatch: {stored_metrics}")
    if logical_metrics != {
        "rows": 8701, "unknown": 3979, "direct_invalid": 869,
        "generic": 1324, "numeric": 4103,
    }:
        raise BuildError(f"V5 logical A2 census mismatch: {logical_metrics}")
    if (
        logical_metrics["rows"] - stored_metrics["rows"] != 64
        or logical_metrics["unknown"] - stored_metrics["unknown"] != 36
    ):
        raise BuildError("V5 composition logical-expansion overhead changed")
    _ids, plans = capture_v4.v2.build_schema_plans(registry, logical, candidates)
    plan_census = Counter(plan.state for plan in plans.values())
    expected_plans = Counter({
        "APPLICABLE": 628,
        "STATIC_OPEN": 364,
        "SCHEMA_NOT_APPLIED": 46,
    })
    if plan_census != expected_plans:
        raise BuildError(f"V5 schema-plan census mismatch: {dict(plan_census)}")
    closure = validate_closure(stored)

    v4_open, _v4_groups, v4_states, base_lines = replay_v4_open()
    v5_open, groups, priority_counts = apply_priority_transitions(
        v4_open, priority_rows, closure, v4_states, base_lines
    )
    history = audit_status_history(v5_open)
    if run_mutations:
        mutation_self_test(
            stored_v4, logical_v4, a2_rows, priority_rows, v4_open,
            v4_states, base_lines,
        )

    report = report_text(
        priority_counts, stored_metrics, logical_metrics, plan_census, groups,
        closure, history
    )
    labels = audit_report_labels(report)
    report_label_self_test(report)
    outputs = {
        OPEN_OUT: format_tsv(v4.OPEN_COLUMNS, v5_open),
        REPORT_OUT: report,
    }
    if set(outputs) != set(OWNED_OUTPUTS):
        raise BuildError("V5 status publication boundary changed")
    after = verify_inputs()
    if before != after:
        raise BuildError("pinned inputs changed during V5 status derivation")
    details: dict[str, object] = {
        "stored": stored_metrics,
        "logical": logical_metrics,
        "plans": dict(plan_census),
        "groups": dict(groups),
        "priority": dict(priority_counts),
        "history": dict(history),
        "labels": dict(labels),
        "closure": closure,
        "v4_details": v4_details,
        "expansion_details": expansion_details,
    }
    return outputs, details


def _publication_module():
    if os.name != "nt":
        raise BuildError("publication is supported only on Windows")
    import pf_build_v5_invalid_parameter_closure as publication
    expected = COMPONENT_PINS["pf_build_v5_invalid_parameter_closure.py"][1]
    if sha256_path(Path(publication.__file__).resolve()) != expected:
        raise BuildError("held-handle publication dependency changed")
    return publication


@contextmanager
def publication_configuration(module, owned_names: set[str], lock_name: str, tx_prefix: str):
    saved = (module.OWNED_NAMES, module.LOCK_NAME, module.TX_PREFIX)
    module.OWNED_NAMES = set(owned_names)
    module.LOCK_NAME = lock_name
    module.TX_PREFIX = tx_prefix
    try:
        yield
    finally:
        module.OWNED_NAMES, module.LOCK_NAME, module.TX_PREFIX = saved


PUBLICATION_TRANSIENT_SUFFIXES = (
    ".stage", ".backup", ".tmp", ".temp", ".next", ".journal",
)


def publication_residue_at(
    root: Path,
    owned_names: set[str],
    lock_name: str,
    tx_prefix: str,
    allowed_lock: Path | None = None,
) -> list[str]:
    """Return every task-owned or cache path requiring manual recovery.

    The lock may be ignored only while its exact pathname is held by the
    publisher.  Unknown contents beneath a transaction/cache path are reported
    as one opaque recovery object; this builder never tries to clean them.
    """
    allowed = (
        os.path.normcase(str(allowed_lock.resolve()))
        if allowed_lock is not None else None
    )
    lock_key = lock_name.casefold()
    tx_key = tx_prefix.casefold()
    owned_transients = {
        (owned + suffix).casefold()
        for owned in owned_names
        for suffix in PUBLICATION_TRANSIENT_SUFFIXES
    }
    found: set[str] = set()
    for child in root.iterdir():
        child_key = child.name.casefold()
        resolved = os.path.normcase(str(child.resolve()))
        if child_key == lock_key:
            if allowed is None or resolved != allowed:
                found.add(child.name)
            continue
        if child_key.startswith(tx_key):
            found.add(child.name)
            continue
        if child_key == "__pycache__" or child.suffix.casefold() == ".pyc":
            found.add(child.name)
            continue
        if child_key in {"journal.json", "journal.json.next"}:
            found.add(child.name)
            continue
        if child_key in owned_transients:
            found.add(child.name)
    return sorted(found)


def assert_publication_clean(
    root: Path,
    owned_names: set[str],
    lock_name: str,
    tx_prefix: str,
    allowed_lock: Path | None = None,
) -> None:
    residue = publication_residue_at(
        root, owned_names, lock_name, tx_prefix, allowed_lock
    )
    if residue:
        raise BuildError(f"publication recovery state exists: {residue}")


def publication_residue() -> list[str]:
    return publication_residue_at(OUT, OWNED_NAMES, LOCK_NAME, TX_PREFIX)


def guarded_publish_transaction(
    publication,
    root: Path,
    outputs: Mapping[Path, bytes],
    verify_callback,
    owned_names: set[str],
    lock_name: str,
    tx_prefix: str,
    hook=None,
) -> None:
    # First check occurs before CreateFileW, transaction staging, or any output
    # replacement.  The held-lock callback closes the preflight race before a
    # transaction directory can be created.
    assert_publication_clean(root, owned_names, lock_name, tx_prefix)

    def guarded_hook(stage: str, target, lock: Path, token: str) -> None:
        if stage == "after_lock":
            assert_publication_clean(
                root, owned_names, lock_name, tx_prefix, allowed_lock=lock
            )
        if hook is not None:
            hook(stage, target, lock, token)

    with publication_configuration(publication, owned_names, lock_name, tx_prefix):
        publication.publish_transaction(
            root, outputs, verify_callback, guarded_hook
        )


def publish(outputs: Mapping[Path, bytes]) -> None:
    assert_publication_clean(OUT, OWNED_NAMES, LOCK_NAME, TX_PREFIX)
    publication = _publication_module()

    def full_verify() -> None:
        rebuilt, _details = derive(run_mutations=False)
        if rebuilt != dict(outputs):
            raise BuildError("full publication re-derivation changed staged outputs")

    try:
        guarded_publish_transaction(
            publication, OUT, outputs, full_verify,
            OWNED_NAMES, LOCK_NAME, TX_PREFIX,
        )
    except publication.BuildError as exc:
        raise BuildError(str(exc)) from exc


def publication_self_test() -> None:
    publication = _publication_module()
    with tempfile.TemporaryDirectory(prefix="pf_v5_status_publication_selftest_") as raw:
        root = Path(raw)
        first = root / "first.txt"
        second = root / "second.txt"
        first.write_bytes(b"old-first")
        outputs = {first: b"new-first", second: b"new-second"}
        lock_name = ".status-selftest.lock"
        tx_prefix = ".status-selftest.tx."
        owned = {first.name, second.name}

        # Reproduce an abandoned transaction with its exact recovery evidence,
        # plus root-level stage/journal and bytecode-cache uncertainty.  The
        # preflight must neither create a lock nor change an owned output or a
        # recovery byte.
        stale_tx = root / (tx_prefix.swapcase() + "STALE")
        stale_tx.mkdir()
        root_temp = root / (first.name + ".tmp").upper()
        root_stage = root / (first.name + ".stage").upper()
        root_backup = root / (second.name + ".backup").upper()
        root_journal = root / "JOURNAL.JSON.NEXT"
        stale_recovery = {
            stale_tx / "JOURNAL.JSON": b'{"status":"REPLACING"}\n',
            stale_tx / (first.name + ".backup").upper(): b"exact-old-first",
            stale_tx / (second.name + ".stage").upper(): b"uncertain-new-second",
            root_temp: b"root-temp",
            root_stage: b"root-stage",
            root_backup: b"root-backup",
            root_journal: b"root-journal-stage",
        }
        cache = root / "__PYCACHE__"
        cache.mkdir()
        stale_recovery[cache / "STATUS.CPYTHON-TEST.PYC"] = b"cache-bytes"
        for path, data in stale_recovery.items():
            path.write_bytes(data)
        expected_residue = sorted({
            stale_tx.name, cache.name, root_temp.name, root_stage.name,
            root_backup.name, root_journal.name,
        })
        actual_residue = publication_residue_at(
            root, owned, lock_name, tx_prefix
        )
        if actual_residue != expected_residue:
            raise BuildError(
                f"stale publication residue census changed: {actual_residue}"
            )
        before_outputs = {first: first.read_bytes(), second: None}
        try:
            guarded_publish_transaction(
                publication, root, outputs, lambda: None,
                owned, lock_name, tx_prefix,
            )
        except BuildError:
            pass
        else:
            raise BuildError("stale transaction preflight failed open")
        if first.read_bytes() != before_outputs[first] or second.exists():
            raise BuildError("stale transaction preflight changed owned outputs")
        if any(path.read_bytes() != data for path, data in stale_recovery.items()):
            raise BuildError("stale transaction preflight changed recovery bytes")
        if (root / lock_name).exists():
            raise BuildError("stale transaction preflight created a publication lock")
        shutil.rmtree(stale_tx)
        shutil.rmtree(cache)
        root_temp.unlink()
        root_stage.unlink()
        root_backup.unlink()
        root_journal.unlink()

        # Inject a stale stage in the narrow gap after CreateFileW.  The second
        # census runs while the owned handle denies unlink/replace, so it must
        # stop before a transaction directory or output replacement appears.
        raced_stage = root / (first.name + ".stage")
        original_create_lock_handle = publication.create_lock_handle

        def create_lock_and_race(lock: Path, token: str):
            handle = original_create_lock_handle(lock, token)
            raced_stage.write_bytes(b"raced-stage")
            return handle

        publication.create_lock_handle = create_lock_and_race
        try:
            try:
                guarded_publish_transaction(
                    publication, root, outputs, lambda: None,
                    owned, lock_name, tx_prefix,
                )
            except BuildError:
                pass
            else:
                raise BuildError("held-lock residue recheck failed open")
        finally:
            publication.create_lock_handle = original_create_lock_handle
        if first.read_bytes() != before_outputs[first] or second.exists():
            raise BuildError("held-lock residue recheck changed owned outputs")
        if raced_stage.read_bytes() != b"raced-stage":
            raise BuildError("held-lock residue recheck changed uncertain stage")
        if list(root.glob(tx_prefix + "*")):
            raise BuildError("held-lock residue recheck created a transaction")
        if not (root / lock_name).is_file():
            raise BuildError("held-lock failure did not retain uncertain lock state")
        raced_stage.unlink()
        (root / lock_name).unlink()

        denial = {"unlink": False, "replace": False}

        def denial_hook(stage: str, _target, lock: Path, _token: str) -> None:
            if stage != "after_lock":
                return
            try:
                lock.unlink()
            except OSError:
                denial["unlink"] = True
            else:
                raise BuildError("held lock allowed pathname unlink")
            attacker = root / "attacker.lock"
            attacker.write_bytes(b"attacker")
            try:
                os.replace(attacker, lock)
            except OSError:
                denial["replace"] = True
            else:
                raise BuildError("held lock allowed pathname replacement")
            attacker.unlink(missing_ok=True)

        guarded_publish_transaction(
            publication, root, outputs, lambda: None,
            owned, lock_name, tx_prefix, denial_hook,
        )
        if denial != {"unlink": True, "replace": True}:
            raise BuildError(f"held-lock denial self-test failed: {denial}")
        if first.read_bytes() != b"new-first" or second.read_bytes() != b"new-second":
            raise BuildError("successful publication self-test output mismatch")
        if (root / lock_name).exists() or list(root.glob(tx_prefix + "*")):
            raise BuildError("successful publication self-test left residue")

        foreign = root / lock_name.swapcase()
        foreign.write_bytes(b"foreign-owner")
        try:
            guarded_publish_transaction(
                publication, root, outputs, lambda: None,
                owned, lock_name, tx_prefix,
            )
        except BuildError:
            pass
        else:
            raise BuildError("foreign lock self-test failed open")
        if foreign.read_bytes() != b"foreign-owner":
            raise BuildError("foreign lock was modified")
        foreign.unlink()

        first.write_bytes(b"rollback-first")
        second.unlink(missing_ok=True)

        def abort_hook(stage: str, target: Path | None, _lock: Path, _token: str) -> None:
            if stage == "after_replace" and target == first:
                raise InjectedPublicationAbort("synthetic BaseException")

        try:
            guarded_publish_transaction(
                publication, root, outputs, lambda: None,
                owned, lock_name, tx_prefix, abort_hook,
            )
        except InjectedPublicationAbort:
            pass
        else:
            raise BuildError("BaseException rollback self-test failed open")
        if first.read_bytes() != b"rollback-first" or second.exists():
            raise BuildError("BaseException rollback did not restore originals")
        residues = [root / lock_name, *root.glob(tx_prefix + "*")]
        if not (root / lock_name).exists() or not list(root.glob(tx_prefix + "*")):
            raise BuildError("failed publication did not preserve recovery state")
        for path in residues:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink(missing_ok=True)


def check_outputs(outputs: Mapping[Path, bytes]) -> None:
    before_residue = publication_residue()
    if before_residue:
        raise BuildError(f"publication residue exists before check: {before_residue}")
    for path, expected in outputs.items():
        if not path.is_file() or path.read_bytes() != expected:
            raise BuildError(f"published V5 status output drift: {path.name}")
    after_residue = publication_residue()
    if after_residue:
        raise BuildError(f"read-only check created publication residue: {after_residue}")


def summary(details: Mapping[str, object]) -> str:
    stored = details["stored"]
    logical = details["logical"]
    return (
        "PASS V5 P1=257/365 OPEN=108 overall=336/519 "
        f"stored={stored['rows']} UNKNOWN={stored['unknown']} "  # type: ignore[index]
        f"direct_invalid={stored['direct_invalid']} "  # type: ignore[index]
        f"logical={logical['rows']} logical_UNKNOWN={logical['unknown']}"  # type: ignore[index]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--audit-only", action="store_true")
    group.add_argument("--self-test-publication", action="store_true")
    group.add_argument("--self-test-mutations", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test_publication:
            publication_self_test()
            print("PASS V5 effective-status held-handle publication self-test")
            return 0
        outputs, details = derive(run_mutations=True)
        if args.self_test_mutations:
            print("PASS V5 effective-status mutation self-test")
            return 0
        if args.audit_only:
            print(summary(details))
            return 0
        if args.check:
            check_outputs(outputs)
            print(summary(details))
            return 0
        publish(outputs)
        rebuilt, rebuilt_details = derive(run_mutations=True)
        check_outputs(rebuilt)
        print(summary(rebuilt_details))
        return 0
    except (BuildError, capture_v4.V4Error, v4.BuildError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
