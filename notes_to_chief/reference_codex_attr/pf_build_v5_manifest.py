"""Build the final duplicate-safe V5 local integration checkpoint.

The builder treats the exact V4 manifest as an immutable predecessor, audits
the complete V2--V5 tabular namespace, replays the frozen V5 status and capture
checks, and publishes only the V5 handoff, canonical search index, and manifest.
Normal publication is deliberately separate from read-only audit/check modes.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import csv
import ctypes
from dataclasses import dataclass
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from types import MappingProxyType, ModuleType
from typing import Callable, Iterator, Mapping, MutableMapping, Sequence


sys.dont_write_bytecode = True

OUT = Path(__file__).resolve().parent
INDEX_PATH = OUT / "00_SEARCH_HERE_FIRST.md"
HANDOFF_PATH = OUT / "PF_V5_HANDOFF.md"
MANIFEST_PATH = OUT / "PF_V5_MANIFEST.md"
V4_MANIFEST_PATH = OUT / "PF_V4_MANIFEST.md"
IMAGE_PATH = OUT.parents[1] / "GameClient" / "GameClient.local.bin"
LOCK_PATH = OUT / ".PF_V5_MANIFEST_PUBLISH.lock"
TX_PREFIX = ".PF_V5_MANIFEST_TXN."

IMAGE_SIZE = 14_759_424
IMAGE_SHA256 = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
V4_MANIFEST_SIZE = 20_919
V4_MANIFEST_SHA256 = "80c55db4f60739f0b1c8086cc28e568025678ce70056a9f045c3f9484443c8f3"
V4_MANIFEST_ROWS = 120
V4_INDEX_SIZE = 14_205
V4_INDEX_SHA256 = "3c04c81025a9e7fe7f3866fc879ba3b2d0d2ea1379de445fbd379cd191d0575d"
V5_INDEX_SIZE = 14_799
V5_INDEX_SHA256 = "c42702e2713fabd85d9c86899d18aa9a07b1d14494333887d1ef52145d2c3210"
V5_PREFIX_SIZE = 467
V5_PREFIX_SHA256 = "e28b8f6d19ae1a7887ae7761e4df4ec65dee67869d9ee0fe12a6bbb44d31faf3"
V5_MARKER_SIZE = 127
V5_MARKER_SHA256 = "66093cb73cf149e07aa5130fd6e281248affd41db7e675b7c23a724346b164e7"

CANONICAL_A5_TSV = "PF_V2_FIELD_VALIDATION.tsv"
CANONICAL_A5_SHA256 = "10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806"
DERIVED_STATUS_SEMANTICS = "DERIVED_EFFECTIVE_STATUS_INDEX;NOT_A_NEW_EVIDENCE_ROW"
STATUS_FILES = tuple(f"PF_V{version}_P1_OPEN.tsv" for version in (2, 3, 4, 5))
ALLOWED_SOURCES = {"IMAGE", "DUMP", "CAPTURE", "DATA"}
OWNED_KEY_COLUMNS = {
    "delta_key", "dedup_key", "root_key", "status_key", "validation_key",
    "classmap_key",
}
REFERENCE_KEY_COLUMNS = {
    "base_row_key", "base_delta_key", "effective_schema_key",
    "child_priority_delta_key",
}
EXPECTED_HISTORICAL_STATUS_BASE_REFS = {
    "1152946cae5a93209a40373a511024050285265def9cc2783602575b2cfb19a3",
    "8b5e55e9abec890359065409783812e8d4c85313456ad74ea65e1d7fc9ce7341",
    "bb2509e7781ece1030897b75cea40b1e324635e30e7926a9c38ed49057bcdf00",
    "fd8c6030e96788145cda663ce2323b22785448db18a047e8161b296214a4543e",
}

V5_COMPONENT_FILES = {
    "pf_build_v5_invalid_parameter_closure.py",
    "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv",
    "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv",
    "PF_V5_INVALID_PARAMETER_CLOSURE.md",
    "pf_build_v5_effective_status.py",
    "PF_V5_P1_OPEN.tsv",
    "PF_V5_EFFECTIVE_STATUS.md",
    "pf_validate_v5_effective_capture.py",
    "PF_V5_FIELD_VALIDATION.md",
}
V5_INTEGRATION_FILES = {
    Path(__file__).name, HANDOFF_PATH.name, MANIFEST_PATH.name,
}
V5_FILES = V5_COMPONENT_FILES | V5_INTEGRATION_FILES
PUBLISHED_OUTPUTS = (HANDOFF_PATH.name, INDEX_PATH.name, MANIFEST_PATH.name)
OWNED_NAMES = set(PUBLISHED_OUTPUTS)

REVIEWED_V5_PINS = {
    "pf_build_v5_invalid_parameter_closure.py": (
        103_855, "3f7c6aa4993aa9fa5f1020c0b14fdc119ab568c7e92249003776111355869d73",
    ),
    "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv": (
        14_524, "f3d877bbc2f3899d650286df6026d44df6691ef23b78ed3492a45da9c076d277",
    ),
    "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv": (
        1_678, "0d02afcbbab22506ef74a3cf50d88dd1dd5e7a2c8b85f9333397275a4996114a",
    ),
    "PF_V5_INVALID_PARAMETER_CLOSURE.md": (
        8_563, "12e5790c149324e971d47aae00dca36a7d369ae58ef45755a9422dc97b7f09ff",
    ),
    "pf_build_v5_effective_status.py": (
        71_086, "6a465acafe4544bec4f3f00674bcabe8aeb51e76fcbe33b691e8effb8e70cc0e",
    ),
    "PF_V5_P1_OPEN.tsv": (
        53_841, "9ce1310cce89b6f0c72381ffe684e5c6558b4ad7191d298c958bEE4d28fd533e".lower(),
    ),
    "PF_V5_EFFECTIVE_STATUS.md": (
        3_407, "b2606434c86cfb74cae1e96a0116b0091fe6a02fa0e07bbe669cdbb99296c021",
    ),
    "pf_validate_v5_effective_capture.py": (
        34_305, "a1bd116ebca1ebcc59b7b5a1f4887376cbfc996c74cf38695b90c24b05590e87",
    ),
    "PF_V5_FIELD_VALIDATION.md": (
        7_101, "7e96c0032d67acebc82ed1805a27672705190cd79876fb04d59fccdb3937e67a",
    ),
}

COMPONENT_CHECKS = (
    (
        "pf_build_v5_invalid_parameter_closure.py", ("--check",), 0,
        "PASS V5 invalid-parameter component A2=8637 UNKNOWN=3943 direct_invalid=861 P1=257/365 OPEN=108 prior_A2_directives=3053 prior_A2_targets=451 overlap=0",
    ),
    (
        "pf_build_v5_effective_status.py", ("--check",), 0,
        "PASS V5 P1=257/365 OPEN=108 overall=336/519 stored=8637 UNKNOWN=3943 direct_invalid=861 logical=8701 logical_UNKNOWN=3979",
    ),
    (
        "pf_validate_v5_effective_capture.py",
        ("--check", "--external", str(OUT), "--game-client", str(IMAGE_PATH.parent)),
        0,
        "unique_contents=1509 duplicate_paths=645 pass=22965 static_open=78532 schema_not_applied=0 mismatch=386 mismatch_points=4 plans=628/364/46",
    ),
    (
        "pf_validate_v5_effective_capture.py",
        (
            "--check", "--fail-on-mismatch", "--external", str(OUT),
            "--game-client", str(IMAGE_PATH.parent),
        ),
        1,
        "ERROR: capture conformance failed: mismatch=386 field_reason_points=4",
    ),
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
    "base_delta_key", "message", "priority", "old_registry_identity_status",
    "new_registry_identity_status", "old_registry_identity_missing",
    "new_registry_identity_missing", "old_serializer_status",
    "new_serializer_status", "old_serializer_blockers",
    "new_serializer_blockers", "old_structural_status",
    "new_structural_status", "old_blocker", "new_blocker",
    "evidence_ticket", "closure_scope", "source",
)
STATUS_COLUMNS = (
    "status_key", "message", "priority", "matched_groups", "matched_keywords",
    "base_line", "base_registry_identity_status",
    "effective_registry_identity_status", "effective_registry_identity_missing",
    "base_serializer_status", "effective_serializer_status",
    "base_structural_status", "effective_structural_status",
    "primary_blocker_group", "effective_blocker", "applied_overlay_chain",
    "row_semantics", "source",
)
A5_COLUMNS = (
    "validation_key", "message", "direction(W/R)", "schema_variant",
    "effective_schema_key", "observed_frames", "observed_instances",
    "baseline_observed_instances", "new_observed_instances",
    "parse_success_frames", "parse_success_instances",
    "baseline_parse_success_instances", "new_parse_success_instances",
    "static_open_frames", "static_open_instances",
    "baseline_static_open_instances", "new_static_open_instances",
    "static_open_reason_count", "schema_not_applied_frames",
    "schema_not_applied_instances", "baseline_schema_not_applied_instances",
    "new_schema_not_applied_instances", "schema_not_applied_reason_count",
    "mismatch_frames", "mismatch_instances", "baseline_mismatch_instances",
    "new_mismatch_instances", "mismatch_field_identity_reason_count",
    "record_instances_observed", "record_branch_coverage", "capture_file_count",
    "status", "content_dedup_scope", "source",
)
EXACT_SCHEMAS = {
    "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv": A2_COLUMNS,
    "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv": PRIORITY_COLUMNS,
    "PF_V5_P1_OPEN.tsv": STATUS_COLUMNS,
    CANONICAL_A5_TSV: A5_COLUMNS,
}
EXACT_SOURCE_SETS = {
    "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv": {"IMAGE"},
    "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv": {"IMAGE"},
    "PF_V5_P1_OPEN.tsv": {"IMAGE"},
    CANONICAL_A5_TSV: {"CAPTURE"},
}

EXPECTED_A5 = {
    "rows": 66, "parse_success": 22_965, "static_open": 78_532,
    "schema_not_applied": 0, "mismatch": 386, "mismatch_points": 4,
    "field_locations": 3,
}
EXPECTED_ITEM_VARIANTS = {
    ("ItemAttr", "R", "VTABLE_0x00F0EBB0"): 13,
    ("ItemAttr", "W", "VTABLE_0x00F0EBB0"): 13,
    ("ItemAttr", "R", "VTABLE_0x00F4A188"): 15,
    ("ItemAttr", "W", "VTABLE_0x00F4A188"): 15,
}

V4_TABLE_RE = re.compile(
    r"^\| `([^`]+)` \| ([0-9]+) \| `([0-9A-Fa-f]{64})` \|", re.MULTILINE
)
RAW_BYTE_PATTERNS = (
    re.compile(r"(?:^|\s)(?:[0-9A-Fa-f]{2}\s+){7,}[0-9A-Fa-f]{2}(?:\s|$)"),
    re.compile(r"(?:\\x[0-9A-Fa-f]{2}){4,}"),
    re.compile(r"(?:0x[0-9A-Fa-f]{2}\s*,\s*){7,}0x[0-9A-Fa-f]{2}\b"),
    re.compile(r"data:[^\s]*;base64,", re.IGNORECASE),
    re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{96,}={0,2}(?![A-Za-z0-9+/])"),
)
CLAIM_LABELS = (
    "[MEASURED][CAPTURE]", "[MEASURED][IMAGE]",
    "[MEASURED][OUTPUT-AUDIT]", "[PROPOSED][DERIVED]",
    "[PROPOSED][LOCAL]", "[NONCLAIM][LOCAL]",
    "[REPRODUCTION][LOCAL]", "[DECLARED-SCOPE]",
)
EXTRA_BRACKET_RE = re.compile(r"\[[^\]\r\n]+\]")


class ManifestError(RuntimeError):
    pass


class InjectedAbort(BaseException):
    pass


@dataclass(frozen=True)
class Snapshot:
    expected: frozenset[str]
    files: Mapping[str, bytes]
    identities: Mapping[str, tuple[int, int]]
    v4_hashes: Mapping[str, tuple[int, str]]
    image_fingerprint: tuple[int, str]

    def text(self, name: str) -> str:
        try:
            return self.files[name].decode("utf-8", errors="strict")
        except KeyError as exc:
            raise ManifestError(f"snapshot artifact missing: {name}") from exc
        except UnicodeError as exc:
            raise ManifestError(f"non-UTF-8 artifact: {name}") from exc


@dataclass(frozen=True)
class TsvArtifact:
    fields: tuple[str, ...]
    rows: tuple[dict[str, str], ...]
    raw_lines: tuple[str, ...]


@dataclass(frozen=True)
class TsvAudit:
    tables: Mapping[str, TsvArtifact]
    census: Mapping[str, tuple[int, Counter[str]]]
    total_rows: int
    delta_dedup_count: int
    base_target_count: int
    base_delta_ref_count: int
    repeated_lines: int
    repeated_occurrences: int
    repeated_extras: int
    intersections: Mapping[tuple[str, str], int]
    a2_add_semantic_count: int
    a2_add_semantic_duplicate_groups: int
    v5_physical_pairs: int


@dataclass(frozen=True)
class Audit:
    snapshot: Snapshot
    tsv: TsvAudit
    effective: Mapping[str, object]
    a5: Mapping[str, int]
    frozen_v4_index: bytes
    final_handoff: bytes
    final_index: bytes


@dataclass
class HeldWindowsLock:
    fd: int
    payload: bytes
    path: Path
    retain: bool = False


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_fingerprint() -> tuple[int, str]:
    if not IMAGE_PATH.is_file():
        raise ManifestError("pinned GameClient.local.bin is missing")
    return IMAGE_PATH.stat().st_size, sha256_path(IMAGE_PATH)


def file_identity(path: Path) -> tuple[int, int]:
    stat = path.stat(follow_symlinks=False)
    return int(stat.st_dev), int(stat.st_ino)


def read_stable_file(path: Path) -> tuple[bytes, tuple[int, int]]:
    if path.is_symlink() or not path.is_file() or path.resolve().parent != OUT:
        raise ManifestError(f"nonlocal/symlink/non-file artifact: {path.name}")
    before = path.stat(follow_symlinks=False)
    data = path.read_bytes()
    after = path.stat(follow_symlinks=False)
    before_state = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    after_state = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if before_state != after_state or len(data) != after.st_size:
        raise ManifestError(f"artifact changed while read: {path.name}")
    return data, (int(after.st_dev), int(after.st_ino))


def canonical_row_key(fields: Sequence[str], row: Mapping[str, str]) -> str:
    raw = json.dumps(
        [row[field] for field in fields], ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(raw)


def parse_v4_hashes(data: bytes) -> dict[str, tuple[int, str]]:
    if (len(data), sha256_bytes(data)) != (V4_MANIFEST_SIZE, V4_MANIFEST_SHA256):
        raise ManifestError("frozen V4 manifest identity changed")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ManifestError("frozen V4 manifest is not UTF-8") from exc
    found = V4_TABLE_RE.findall(text)
    if len(found) != V4_MANIFEST_ROWS:
        raise ManifestError(f"V4 manifest table census changed: {len(found)}")
    if len({name.casefold() for name, _size, _digest in found}) != V4_MANIFEST_ROWS:
        raise ManifestError("V4 manifest contains duplicate/case-colliding members")
    result = {name: (int(size), digest.lower()) for name, size, digest in found}
    if result.get(INDEX_PATH.name) != (V4_INDEX_SIZE, V4_INDEX_SHA256):
        raise ManifestError("V4 manifest predecessor-index pin changed")
    if V4_MANIFEST_PATH.name in result or V5_FILES.intersection(result):
        raise ManifestError("V4 manifest crossed its version boundary")
    for name in result:
        if Path(name).name != name or "/" in name or "\\" in name:
            raise ManifestError(f"nonlocal V4 manifest member: {name}")
    return result


def expected_files(v4_hashes: Mapping[str, tuple[int, str]]) -> set[str]:
    expected = set(v4_hashes) | {V4_MANIFEST_PATH.name} | V5_FILES
    if len(expected) != 133:
        raise ManifestError(f"V5 exact namespace census changed: {len(expected)}")
    if len(expected) != len({name.casefold() for name in expected}):
        raise ManifestError("case-insensitive expected namespace collision")
    forbidden_a5 = {
        "PF_V3_FIELD_VALIDATION.tsv", "PF_V4_FIELD_VALIDATION.tsv",
        "PF_V5_FIELD_VALIDATION.tsv",
    }
    if forbidden_a5 & expected:
        raise ManifestError("duplicate versioned A5 TSV entered V5 namespace")
    return expected


PUBLICATION_SUFFIXES = (
    ".new", ".old", ".stage", ".backup", ".tmp", ".temp", ".next",
    ".journal",
)


def publication_residue_at(
    root: Path, *, allowed_lock: Path | None = None,
    allowed_tx: Path | None = None,
) -> list[str]:
    allowed_lock_key = (
        os.path.normcase(str(allowed_lock.resolve())) if allowed_lock else None
    )
    allowed_tx_key = (
        os.path.normcase(str(allowed_tx.resolve())) if allowed_tx else None
    )
    lock_key = LOCK_PATH.name.casefold()
    tx_key = TX_PREFIX.casefold()
    owned_transients = {
        (name + suffix).casefold()
        for name in OWNED_NAMES for suffix in PUBLICATION_SUFFIXES
    }
    found: set[str] = set()
    for child in root.iterdir():
        name_key = child.name.casefold()
        resolved = os.path.normcase(str(child.resolve()))
        if name_key == lock_key:
            if allowed_lock_key is None or resolved != allowed_lock_key:
                found.add(child.name)
            continue
        if name_key.startswith(tx_key):
            if allowed_tx_key is None or resolved != allowed_tx_key:
                found.add(child.name)
            continue
        if name_key == "__pycache__" or child.suffix.casefold() == ".pyc":
            found.add(child.name)
            continue
        if name_key in {"journal.json", "journal.jsonl", "journal.json.next"}:
            found.add(child.name)
            continue
        if name_key in owned_transients:
            found.add(child.name)
            continue
        if name_key.startswith(".pf_v5_manifest_"):
            found.add(child.name)
    return sorted(found, key=str.casefold)


def assert_publication_clean(
    root: Path, *, allowed_lock: Path | None = None,
    allowed_tx: Path | None = None,
) -> None:
    residue = publication_residue_at(
        root, allowed_lock=allowed_lock, allowed_tx=allowed_tx
    )
    if residue:
        raise ManifestError(f"publication recovery state exists: {residue}")


def verify_namespace(
    expected: set[str] | frozenset[str], *, allow_unpublished: bool,
    transients: frozenset[str],
) -> None:
    transient_keys = {name.casefold() for name in transients}
    if len(transient_keys) != len(transients):
        raise ManifestError("case-colliding active transients")
    for name in transients:
        if Path(name).name != name:
            raise ManifestError(f"invalid transient namespace: {name}")
        key = name.casefold()
        if key != LOCK_PATH.name.casefold() and not key.startswith(TX_PREFIX.casefold()):
            raise ManifestError(f"unrecognised active transient: {name}")
    entries = list(OUT.iterdir())
    actual = {path.name for path in entries}
    if len(actual) != len({name.casefold() for name in actual}):
        raise ManifestError("case-insensitive live namespace collision")
    for path in entries:
        if path.is_symlink() or path.resolve().parent != OUT:
            raise ManifestError(f"symlink/reparse/nonlocal output: {path.name}")
        if path.name.casefold() in transient_keys - {LOCK_PATH.name.casefold()}:
            if not path.is_dir():
                raise ManifestError(f"transaction transient is not a directory: {path.name}")
        elif not path.is_file():
            raise ManifestError(f"unexpected directory/non-file: {path.name}")
    complete = frozenset(set(expected) | set(transients))
    accepted = {complete}
    if allow_unpublished:
        accepted.add(frozenset(
            (set(expected) - {HANDOFF_PATH.name, MANIFEST_PATH.name}) | set(transients)
        ))
    if frozenset(actual) not in accepted:
        closest = min(accepted, key=lambda candidate: len(candidate ^ actual))
        raise ManifestError(
            f"namespace mismatch: missing={sorted(closest - actual)} "
            f"extra={sorted(actual - closest)}"
        )


def take_snapshot(*, allow_unpublished: bool, transients: frozenset[str]) -> Snapshot:
    manifest_data, manifest_identity = read_stable_file(V4_MANIFEST_PATH)
    v4_hashes = parse_v4_hashes(manifest_data)
    expected = frozenset(expected_files(v4_hashes))
    verify_namespace(
        expected, allow_unpublished=allow_unpublished, transients=transients
    )
    files: dict[str, bytes] = {V4_MANIFEST_PATH.name: manifest_data}
    identities: dict[str, tuple[int, int]] = {
        V4_MANIFEST_PATH.name: manifest_identity
    }
    for name in sorted(expected - {V4_MANIFEST_PATH.name}, key=str.casefold):
        path = OUT / name
        if (
            allow_unpublished
            and name in {HANDOFF_PATH.name, MANIFEST_PATH.name}
            and not path.exists()
        ):
            continue
        data, identity = read_stable_file(path)
        files[name] = data
        identities[name] = identity
    snapshot = Snapshot(
        expected=expected,
        files=MappingProxyType(files),
        identities=MappingProxyType(identities),
        v4_hashes=MappingProxyType(v4_hashes),
        image_fingerprint=image_fingerprint(),
    )
    assert_snapshot_current(snapshot, transients=transients)
    return snapshot


def assert_snapshot_current(snapshot: Snapshot, *, transients: frozenset[str]) -> None:
    absent = {HANDOFF_PATH.name, MANIFEST_PATH.name} - set(snapshot.files)
    allow_unpublished = absent == {HANDOFF_PATH.name, MANIFEST_PATH.name}
    if absent and not allow_unpublished:
        raise ManifestError(f"partial V5 integration snapshot: {sorted(absent)}")
    verify_namespace(
        snapshot.expected, allow_unpublished=allow_unpublished,
        transients=transients,
    )
    for name in sorted(snapshot.expected, key=str.casefold):
        path = OUT / name
        if name not in snapshot.files:
            if path.exists():
                raise ManifestError(f"CAS absent artifact appeared: {name}")
            continue
        data, identity = read_stable_file(path)
        if data != snapshot.files[name] or identity != snapshot.identities[name]:
            raise ManifestError(f"CAS artifact bytes/identity changed: {name}")
    if image_fingerprint() != snapshot.image_fingerprint:
        raise ManifestError("CAS pinned image changed")


def load_local_module(name: str, path: Path, expected_hash: str) -> ModuleType:
    if not path.is_file() or sha256_path(path) != expected_hash:
        raise ManifestError(f"module pin changed before import: {path.name}")
    cached = sys.modules.get(name)
    if cached is not None:
        return cached
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ManifestError(f"cannot construct module spec: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def status_module() -> ModuleType:
    digest = REVIEWED_V5_PINS["pf_build_v5_effective_status.py"][1]
    return load_local_module(
        "_pf_v5_manifest_status_" + digest[:16],
        OUT / "pf_build_v5_effective_status.py", digest,
    )


def canonical_index_parts() -> tuple[bytes, bytes]:
    status = status_module()
    prefix = status.CANONICAL_V5_INDEX_PREFIX
    marker = status.V5_INDEX_TAIL_MARKER
    if not isinstance(prefix, bytes) or not isinstance(marker, bytes):
        raise ManifestError("status builder canonical index parts are not bytes")
    if (len(prefix), sha256_bytes(prefix)) != (V5_PREFIX_SIZE, V5_PREFIX_SHA256):
        raise ManifestError("canonical V5 index prefix changed")
    if (len(marker), sha256_bytes(marker)) != (V5_MARKER_SIZE, V5_MARKER_SHA256):
        raise ManifestError("canonical V5 index tail marker changed")
    return prefix, marker


def frozen_v4_index(snapshot: Snapshot) -> bytes:
    current = snapshot.files[INDEX_PATH.name]
    if (len(current), sha256_bytes(current)) == (V4_INDEX_SIZE, V4_INDEX_SHA256):
        return current
    prefix, marker = canonical_index_parts()
    expected_prefix = prefix + marker
    if len(current) != len(expected_prefix) + V4_INDEX_SIZE:
        raise ManifestError("current search index is neither exact V4 nor canonical V5")
    if current[:len(expected_prefix)] != expected_prefix:
        raise ManifestError("current V5 search-index prefix/marker is noncanonical")
    tail = current[len(expected_prefix):]
    if (len(tail), sha256_bytes(tail)) != (V4_INDEX_SIZE, V4_INDEX_SHA256):
        raise ManifestError("embedded frozen V4 index tail changed")
    return tail


def verify_inputs(snapshot: Snapshot) -> bytes:
    if snapshot.image_fingerprint != (IMAGE_SIZE, IMAGE_SHA256):
        raise ManifestError("pinned client image changed")
    for name, (size, digest) in snapshot.v4_hashes.items():
        if name == INDEX_PATH.name:
            continue
        data = snapshot.files[name]
        if (len(data), sha256_bytes(data)) != (size, digest):
            raise ManifestError(f"frozen V4 artifact changed: {name}")
    for name, pin in REVIEWED_V5_PINS.items():
        data = snapshot.files.get(name)
        if data is None or (len(data), sha256_bytes(data)) != pin:
            actual = "MISSING" if data is None else (len(data), sha256_bytes(data))
            raise ManifestError(f"reviewed V5 pin changed: {name}: {actual} != {pin}")
    tail = frozen_v4_index(snapshot)
    complete = HANDOFF_PATH.name in snapshot.files
    prefix, marker = canonical_index_parts()
    canonical = prefix + marker + tail
    if (len(canonical), sha256_bytes(canonical)) != (V5_INDEX_SIZE, V5_INDEX_SHA256):
        raise ManifestError("canonical V5 index identity changed")
    if complete:
        if snapshot.files[INDEX_PATH.name] != canonical:
            raise ManifestError("complete V5 namespace has noncanonical search index")
    elif snapshot.files[INDEX_PATH.name] != tail:
        raise ManifestError("unpublished V5 namespace does not retain exact V4 index")
    versioned_a5 = sorted(
        name for name in snapshot.expected
        if re.fullmatch(r"PF_V\d+_FIELD_VALIDATION\.tsv", name)
    )
    if versioned_a5 != [CANONICAL_A5_TSV]:
        raise ManifestError(f"versioned A5 TSV singleton changed: {versioned_a5}")
    return tail


def read_tsv(snapshot: Snapshot, name: str) -> TsvArtifact:
    text = snapshot.text(name)
    try:
        parsed = list(csv.reader(io.StringIO(text, newline=""), delimiter="\t", strict=True))
    except csv.Error as exc:
        raise ManifestError(f"malformed TSV quoting: {name}") from exc
    if not parsed or not parsed[0] or any(not field for field in parsed[0]):
        raise ManifestError(f"empty/blank TSV header: {name}")
    fields = tuple(parsed[0])
    if len(fields) != len(set(fields)):
        raise ManifestError(f"duplicate TSV header: {name}")
    rows: list[dict[str, str]] = []
    for line_number, cells in enumerate(parsed[1:], start=2):
        if len(cells) != len(fields):
            raise ManifestError(f"TSV cell-count mismatch: {name}:{line_number}")
        rows.append(dict(zip(fields, cells, strict=True)))
    raw_lines = tuple(text.splitlines()[1:])
    if len(raw_lines) != len(rows) or any(not line for line in raw_lines):
        raise ManifestError(f"multiline/blank physical TSV row is forbidden: {name}")
    return TsvArtifact(fields, tuple(rows), raw_lines)


def normalise_status_reference(row: Mapping[str, str]) -> dict[str, str]:
    result = dict(row)
    if "applied_overlay" in result:
        result["applied_overlay_chain"] = result.pop("applied_overlay")
    return result


def audit_tsvs(snapshot: Snapshot) -> TsvAudit:
    tables: dict[str, TsvArtifact] = {}
    census: dict[str, tuple[int, Counter[str]]] = {}
    owners: dict[tuple[str, str], list[tuple[str, dict[str, str]]]] = defaultdict(list)
    cross_namespace: dict[str, str] = {}
    raw_occurrences: dict[str, list[tuple[str, int, dict[str, str]]]] = defaultdict(list)
    delta_dedup_values: list[str] = []
    base_targets: list[tuple[str, str, str]] = []
    base_delta_refs: list[str] = []
    total_rows = 0

    for name in sorted(
        (item for item in snapshot.expected if item.endswith(".tsv")),
        key=str.casefold,
    ):
        table = read_tsv(snapshot, name)
        tables[name] = table
        fields, rows = table.fields, table.rows
        total_rows += len(rows)
        if "source" not in fields:
            raise ManifestError(f"TSV missing source column: {name}")
        if name in EXACT_SCHEMAS and fields != EXACT_SCHEMAS[name]:
            raise ManifestError(f"exact TSV schema changed: {name}")
        unknown_keys = {
            field for field in fields if field.endswith("_key")
        } - OWNED_KEY_COLUMNS - REFERENCE_KEY_COLUMNS
        if unknown_keys:
            raise ManifestError(f"unclassified key namespace: {name}:{sorted(unknown_keys)}")
        sources = Counter(row["source"] for row in rows)
        if not sources or not set(sources).issubset(ALLOWED_SOURCES):
            raise ManifestError(f"invalid/empty TSV source layer: {name}:{dict(sources)}")
        if name in EXACT_SOURCE_SETS and set(sources) != EXACT_SOURCE_SETS[name]:
            raise ManifestError(f"exact V5 evidence layer changed: {name}:{dict(sources)}")
        row_tuples = [tuple(row[field] for field in fields) for row in rows]
        if len(row_tuples) != len(set(row_tuples)):
            raise ManifestError(f"exact duplicate row within TSV: {name}")
        for line, (row, raw_line) in enumerate(
            zip(rows, table.raw_lines, strict=True), start=2
        ):
            raw_occurrences[raw_line].append((name, line, row))
            for action_column in ("action", "delta_action"):
                action = row.get(action_column, "").upper()
                if any(token in action for token in ("UNCHANGED", "COPIED")):
                    raise ManifestError(f"duplicative delta action: {name}:{line}:{action}")
            if {"base_file", "base_line", "base_row_key"}.issubset(fields):
                target = (row["base_file"], row["base_line"], row["base_row_key"])
                populated = [value not in {"", "N/A"} for value in target]
                if any(populated) and not all(populated):
                    raise ManifestError(f"partial base target: {name}:{line}")
                if all(populated):
                    base_targets.append(target)
            reference = row.get("base_delta_key")
            if reference not in {None, "", "N/A"}:
                if re.fullmatch(r"[0-9a-f]{64}", reference) is None:
                    raise ManifestError(f"malformed base_delta_key: {name}:{line}")
                base_delta_refs.append(reference)
        for key in OWNED_KEY_COLUMNS:
            if key not in fields:
                continue
            values = [row[key] for row in rows]
            if any(value in {"", "N/A"} for value in values):
                raise ManifestError(f"empty/N-A owned {key}: {name}")
            if len(values) != len(set(values)):
                raise ManifestError(f"duplicate local {key}: {name}")
            if key in {"delta_key", "dedup_key"}:
                delta_dedup_values.extend(values)
            for row in rows:
                value = row[key]
                prior_namespace = cross_namespace.setdefault(value, key)
                if prior_namespace != key:
                    raise ManifestError(
                        f"cross-namespace key collision: {prior_namespace}/{key}:{value}"
                    )
                owners[(key, value)].append((name, row))
        census[name] = (len(rows), sources)

    if len(tables) != 49:
        raise ManifestError(f"global TSV file census changed: {len(tables)} != 49")
    if total_rows != 22_048:
        raise ManifestError(f"global TSV data-row census changed: {total_rows}")
    if len(delta_dedup_values) != 3_426 or len(set(delta_dedup_values)) != 3_426:
        raise ManifestError(
            "global delta_key+dedup_key union changed/collided: "
            f"occurrences={len(delta_dedup_values)} unique={len(set(delta_dedup_values))}"
        )
    if len(base_targets) != 598 or len(set(base_targets)) != 598:
        raise ManifestError(
            "full base-target census/collision changed: "
            f"occurrences={len(base_targets)} unique={len(set(base_targets))}"
        )
    if len(base_delta_refs) != 71 or len(set(base_delta_refs)) != 71:
        raise ManifestError(
            "base_delta_key reference census/collision changed: "
            f"occurrences={len(base_delta_refs)} unique={len(set(base_delta_refs))}"
        )
    delta_values = {value for key, value in owners if key == "delta_key"}
    status_values = {value for key, value in owners if key == "status_key"}
    historical_refs = set(base_delta_refs) - delta_values
    if (
        historical_refs != EXPECTED_HISTORICAL_STATUS_BASE_REFS
        or not historical_refs <= status_values
    ):
        raise ManifestError(
            f"historical status-key base references changed: {sorted(historical_refs)}"
        )

    for (key, value), occurrences in owners.items():
        if len(occurrences) == 1:
            continue
        files = [name for name, _row in occurrences]
        first_row = occurrences[0][1]
        if (
            key != "status_key"
            or len(files) not in {2, 3, 4}
            or len(files) != len(set(files))
            or not set(files) <= set(STATUS_FILES)
            or any(
                row.get("row_semantics") != DERIVED_STATUS_SEMANTICS
                or row.get("source") != "IMAGE"
                for _name, row in occurrences
            )
            or any(
                normalise_status_reference(row) != normalise_status_reference(first_row)
                for _name, row in occurrences[1:]
            )
        ):
            raise ManifestError(f"unauthorised global {key} duplicate: {value}:{files}")

    for status_name in STATUS_FILES:
        status = tables[status_name]
        if any(
            row.get("row_semantics") != DERIVED_STATUS_SEMANTICS
            or row.get("source") != "IMAGE"
            for row in status.rows
        ):
            raise ManifestError(f"status snapshot lost reference-only semantics: {status_name}")
    status_multiplicity = Counter(
        len(occurrences)
        for (key, _value), occurrences in owners.items()
        if key == "status_key"
    )
    if status_multiplicity != Counter({4: 92, 3: 13, 2: 8, 1: 21}):
        raise ManifestError(
            f"historical status-key multiplicity changed: {dict(status_multiplicity)}"
        )

    repeated = {line: items for line, items in raw_occurrences.items() if len(items) > 1}
    repeated_occurrences = sum(len(items) for items in repeated.values())
    repeated_extras = sum(len(items) - 1 for items in repeated.values())
    if (len(repeated), repeated_occurrences, repeated_extras) != (113, 423, 310):
        raise ManifestError(
            "cross-file exact-row census changed: "
            f"distinct={len(repeated)} occurrences={repeated_occurrences} "
            f"extras={repeated_extras}"
        )
    topology = Counter(len(items) for items in repeated.values())
    if topology != Counter({4: 92, 3: 13, 2: 8}):
        raise ManifestError(f"cross-file status-row topology changed: {dict(topology)}")
    for occurrences in repeated.values():
        files = {name for name, _line, _row in occurrences}
        if not files <= set(STATUS_FILES) or len(files) != len(occurrences):
            raise ManifestError(
                f"exact fact row repeated outside status snapshots: {sorted(files)}"
            )
        for name, line, row in occurrences:
            if (
                row.get("row_semantics") != DERIVED_STATUS_SEMANTICS
                or row.get("source") != "IMAGE"
            ):
                raise ManifestError(f"unlabelled repeated status reference: {name}:{line}")

    status_lines = {name: set(tables[name].raw_lines) for name in STATUS_FILES}
    intersections = {
        (left, right): len(status_lines[left] & status_lines[right])
        for index, left in enumerate(STATUS_FILES)
        for right in STATUS_FILES[index + 1:]
    }
    expected_intersections = {
        ("PF_V2_P1_OPEN.tsv", "PF_V3_P1_OPEN.tsv"): 95,
        ("PF_V2_P1_OPEN.tsv", "PF_V4_P1_OPEN.tsv"): 92,
        ("PF_V2_P1_OPEN.tsv", "PF_V5_P1_OPEN.tsv"): 92,
        ("PF_V3_P1_OPEN.tsv", "PF_V4_P1_OPEN.tsv"): 107,
        ("PF_V3_P1_OPEN.tsv", "PF_V5_P1_OPEN.tsv"): 105,
        ("PF_V4_P1_OPEN.tsv", "PF_V5_P1_OPEN.tsv"): 108,
    }
    if intersections != expected_intersections:
        raise ManifestError(f"derived-status pair intersections changed: {intersections}")

    add_rows = [
        (name, row)
        for name, table in tables.items()
        for row in table.rows
        if row.get("action", "").startswith("ADD_")
    ]
    if Counter(name for name, _row in add_rows) != Counter({
        "PF_A2_SERIALIZER_SLOT34_DELTA.tsv": 2_194
    }):
        raise ManifestError("bounded historical A2 ADD file/census changed")
    semantic_columns = (
        "message", "schema_variant", "direction(W/R)", "new_order", "new_tag",
        "new_field_offset", "new_len", "new_gate_condition",
    )
    semantic_counts = Counter(
        tuple(row[column] for column in semantic_columns) for _name, row in add_rows
    )
    semantic_duplicate_groups = sum(count > 1 for count in semantic_counts.values())
    if len(semantic_counts) != 2_194 or semantic_duplicate_groups != 0:
        raise ManifestError(
            "bounded A2 ADD semantic duplicate detected: "
            f"facts={len(add_rows)} unique={len(semantic_counts)} "
            f"duplicate_groups={semantic_duplicate_groups}"
        )
    classmap_values = [
        row["classmap_key"]
        for row in tables["PF_STATIC_TYPE_INFO_CLASSMAP.tsv"].rows
    ]
    if len(classmap_values) != 4 or len(set(classmap_values)) != 4:
        raise ManifestError("classmap key census/collision changed")

    v5_physical_pairs = audit_v5_overlay_references(tables)
    return TsvAudit(
        tables=MappingProxyType(tables),
        census=MappingProxyType(census),
        total_rows=total_rows,
        delta_dedup_count=len(delta_dedup_values),
        base_target_count=len(base_targets),
        base_delta_ref_count=len(base_delta_refs),
        repeated_lines=len(repeated),
        repeated_occurrences=repeated_occurrences,
        repeated_extras=repeated_extras,
        intersections=MappingProxyType(intersections),
        a2_add_semantic_count=len(add_rows),
        a2_add_semantic_duplicate_groups=semantic_duplicate_groups,
        v5_physical_pairs=v5_physical_pairs,
    )


def validate_base_reference(
    tables: Mapping[str, TsvArtifact], owner_name: str,
    row: Mapping[str, str],
) -> None:
    base_name = row["base_file"]
    if base_name not in tables:
        raise ManifestError(f"V5 base reference file is not a TSV: {owner_name}:{base_name}")
    try:
        line = int(row["base_line"])
    except ValueError as exc:
        raise ManifestError(f"V5 base reference line is invalid: {owner_name}") from exc
    table = tables[base_name]
    if line < 2 or line - 2 >= len(table.rows):
        raise ManifestError(f"V5 base reference line is absent: {owner_name}:{base_name}:{line}")
    base = table.rows[line - 2]
    if canonical_row_key(table.fields, base) != row["base_row_key"]:
        raise ManifestError(f"V5 base row key mismatch: {owner_name}:{base_name}:{line}")
    reference = row.get("base_delta_key")
    if reference not in {None, "", "N/A"}:
        candidates = {base.get("delta_key"), base.get("status_key")}
        if reference not in candidates:
            raise ManifestError(
                f"V5 base delta/status reference mismatch: {owner_name}:{base_name}:{line}"
            )


def audit_v5_overlay_references(tables: Mapping[str, TsvArtifact]) -> int:
    a2_name = "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv"
    priority_name = "PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv"
    a2 = tables[a2_name].rows
    priority = tables[priority_name].rows
    if len(a2) != 20 or Counter(row["action"] for row in a2) != Counter({
        "REMOVE_NONWIRE_ROW": 20
    }):
        raise ManifestError("V5 A2 removal action/census changed")
    if Counter((row["message"], row["direction(W/R)"]) for row in a2) != Counter({
        ("ItemMallUpdatePersonalDataVital", "R"): 5,
        ("ItemMallUpdatePersonalDataVital", "W"): 5,
        ("ServerAddedInfoVital", "R"): 5,
        ("ServerAddedInfoVital", "W"): 5,
    }):
        raise ManifestError("V5 A2 target message/direction census changed")
    natural_targets = {
        (row["base_file"], row["base_line"], row["base_row_key"])
        for row in a2
    }
    if len(natural_targets) != 20:
        raise ManifestError("V5 removal full-base natural identity collided")
    physical: dict[tuple[str, str], list[Mapping[str, str]]] = defaultdict(list)
    for row in a2:
        validate_base_reference(tables, a2_name, row)
        if (
            row["source"] != "IMAGE"
            or row["old_tag"] != "PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL"
            or row["new_tag"] != "N/A"
            or row["new_field_offset"] != "N/A"
            or row["new_len"] != "N/A"
            or row["new_gate_condition"] != "N/A"
        ):
            raise ManifestError("V5 removal source/non-wire contract changed")
        physical[(row["message"], row["evidence_file_off"])].append(row)
    if len(physical) != 10 or any(
        len(rows) != 2 or {row["direction(W/R)"] for row in rows} != {"R", "W"}
        for rows in physical.values()
    ):
        raise ManifestError("V5 physical callsite R/W pair census changed")
    if len(priority) != 2 or Counter(row["action"] for row in priority) != Counter({
        "CHANGED": 2
    }):
        raise ManifestError("V5 priority transition action/census changed")
    if {(row["message"], row["priority"]) for row in priority} != {
        ("ItemMallUpdatePersonalDataVital", "1"),
        ("ServerAddedInfoVital", "1"),
    }:
        raise ManifestError("V5 priority natural identity changed")
    for row in priority:
        validate_base_reference(tables, priority_name, row)
        if (
            row["source"] != "IMAGE"
            or row["old_serializer_status"] != "OPEN"
            or row["new_serializer_status"] != "CLOSED"
            or row["new_blocker"] != "N/A"
        ):
            raise ManifestError("V5 priority transition contract changed")
    return len(physical)


def raw_byte_guard(name: str, text: str) -> None:
    if any(pattern.search(text) for pattern in RAW_BYTE_PATTERNS):
        raise ManifestError(f"raw/opaque byte representation in output: {name}")


def audit_no_raw_proprietary(snapshot: Snapshot, tsv: TsvAudit) -> None:
    forbidden_columns = {
        "raw_bytes", "payload", "payload_hex", "packet_hex", "hexdump",
        "field_value", "byte_value", "raw_base64", "payload_base64",
    }
    guarded = {CANONICAL_A5_TSV, INDEX_PATH.name}
    for name, table in tsv.tables.items():
        if {row["source"] for row in table.rows} & {"CAPTURE", "DUMP"}:
            overlap = forbidden_columns & {field.lower() for field in table.fields}
            if overlap:
                raise ManifestError(f"raw proprietary output column: {name}:{sorted(overlap)}")
            guarded.add(name)
    guarded.update(name for name in V5_COMPONENT_FILES if name.endswith(".md"))
    for name in sorted(guarded & set(snapshot.files), key=str.casefold):
        raw_byte_guard(name, snapshot.text(name))
    forbidden_suffixes = {".dmp", ".bin", ".cap", ".pcap", ".pcapng"}
    if {Path(name).suffix.casefold() for name in snapshot.expected} & forbidden_suffixes:
        raise ManifestError("proprietary binary entered output namespace")


def audit_exact_duplicate_files(files: Mapping[str, bytes]) -> int:
    digest_groups: dict[tuple[int, str], list[str]] = defaultdict(list)
    for name, data in files.items():
        digest_groups[(len(data), sha256_bytes(data))].append(name)
    duplicates: list[list[str]] = []
    for names in digest_groups.values():
        if len(names) > 1:
            first = files[names[0]]
            equal = [name for name in names if files[name] == first]
            if len(equal) > 1:
                duplicates.append(equal)
    if duplicates:
        raise ManifestError(f"exact duplicate artifact files: {duplicates}")
    return 0


def run_component_checks() -> None:
    before = image_fingerprint()
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for name, arguments, expected_rc, marker in COMPONENT_CHECKS:
        result = subprocess.run(
            [sys.executable, "-B", str(OUT / name), *arguments],
            cwd=OUT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=900,
            check=False,
        )
        try:
            output = result.stdout.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise ManifestError(f"non-UTF-8 component output: {name}") from exc
        if result.returncode != expected_rc or marker not in output:
            tail = "\n".join(output.splitlines()[-20:])
            raise ManifestError(
                f"required component gate failed: {name}: "
                f"rc={result.returncode} expected={expected_rc}\n{tail}"
            )
        label = "strict expected-negative" if expected_rc else "integrity"
        print(f"component {label} PASS: {name}", flush=True)
    after = image_fingerprint()
    if before != (IMAGE_SIZE, IMAGE_SHA256) or after != before:
        raise ManifestError("client image changed across component gates")


def audit_static_and_composition_boundaries(tsv: TsvAudit) -> None:
    classmap = tsv.tables["PF_STATIC_TYPE_INFO_CLASSMAP.tsv"].rows
    identities = {
        (row["registry_name"], row["class_name"], row["identity_kind"], row["vtable_va"])
        for row in classmap
    }
    expected_identities = {
        ("ItemAttr", "ItemAttr", "EXACT_REGISTRY_CLASS", "0x00F0EBB0"),
        (
            "ItemAttr", "StallItem",
            "POLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER", "0x00F4A188",
        ),
        ("VitalData", "VitalData", "EXACT_REGISTRY_CLASS", "0x00F0B930"),
        (
            "VitalData", "Channel_MessageVtial",
            "POLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER", "0x00F375FC",
        ),
    }
    if identities != expected_identities:
        raise ManifestError(f"ItemAttr/VitalData identity variants changed: {identities}")
    a1 = tsv.tables["PF_A1_STATIC_TYPE_INFO_DELTA.tsv"].rows
    by_name = {row["registry_name"]: row for row in a1}
    if len(a1) != 2 or set(by_name) != {"ItemAttr", "VitalData"}:
        raise ManifestError("static identity A1 row set changed")
    if any(
        row["canonical_a2_action"] != "NO_CHANGE"
        or row["source"] != "IMAGE"
        for row in a1
    ):
        raise ManifestError("static identity attempted canonical A2 activation")
    if (
        by_name["ItemAttr"]["serializer_selection"] != "WITHHELD_NOT_SINGLETON"
        or by_name["VitalData"]["serializer_identity_status"] != "UNKNOWN"
        or by_name["VitalData"]["serializer_selection"] != "WITHHELD"
    ):
        raise ManifestError("ItemAttr/VitalData serializer withholding changed")
    static_priority = tsv.tables["PF_PRIORITY_STATIC_TYPE_INFO_DELTA.tsv"].rows
    if any(row["new_structural_status"] != "OPEN" for row in static_priority):
        raise ManifestError("static identity unexpectedly activated structural closure")

    composition = tsv.tables["PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv"].rows
    if Counter(row["action"] for row in composition) != Counter({
        "CHANGED": 4, "REMOVE_DIRECTIONALLY_IMPOSSIBLE_ROW": 2
    }):
        raise ManifestError("embedded-child composition action census changed")
    changed = [row for row in composition if row["action"] == "CHANGED"]
    if any(
        row["new_tag"] != "STATIC_EMBEDDED_CHILD_REF"
        or row["child_receiver"] != "this+0x18"
        or row["child_slot"] != "+0x34"
        or row["new_gate_condition"] != "DIRECTION_FORWARDED"
        for row in changed
    ):
        raise ManifestError("composition reference-only contract changed")
    if Counter((row["child_message"], row["direction(W/R)"]) for row in changed) != Counter({
        ("DailyActivityState", "R"): 1,
        ("DailyActivityState", "W"): 1,
        ("CGuildStorageAttr", "R"): 1,
        ("CGuildStorageAttr", "W"): 1,
    }):
        raise ManifestError("composition child/direction references changed")
    for name in (
        "PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv",
        "PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv",
        "PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv",
    ):
        if any(row["message"] in {"ItemAttr", "VitalData"} for row in tsv.tables[name].rows):
            raise ManifestError("ItemAttr/VitalData identity improperly activated A2")


def audit_effective_outputs(snapshot: Snapshot, tsv: TsvAudit) -> dict[str, object]:
    status = status_module()
    outputs, details = status.derive(run_mutations=False)
    by_name = {path.name: data for path, data in outputs.items()}
    for name in ("PF_V5_P1_OPEN.tsv", "PF_V5_EFFECTIVE_STATUS.md"):
        if by_name.get(name) != snapshot.files[name]:
            raise ManifestError(f"V5 status output differs from full re-derivation: {name}")
    expected_stored = {
        "rows": 8_637, "unknown": 3_943, "direct_invalid": 861,
        "generic": 1_312, "numeric": 4_081,
    }
    expected_logical = {
        "rows": 8_701, "unknown": 3_979, "direct_invalid": 869,
        "generic": 1_324, "numeric": 4_103,
    }
    if details.get("stored") != expected_stored:
        raise ManifestError(f"V5 stored/reference status census changed: {details.get('stored')}")
    if details.get("logical") != expected_logical:
        raise ManifestError(f"V5 logical status census changed: {details.get('logical')}")
    if details.get("plans") != {
        "APPLICABLE": 628, "STATIC_OPEN": 364, "SCHEMA_NOT_APPLIED": 46,
    }:
        raise ManifestError(f"V5 schema-plan census changed: {details.get('plans')}")
    if details.get("priority") != {1: (257, 365), 2: (8, 16), 3: (71, 138)}:
        raise ManifestError(f"V5 priority census changed: {details.get('priority')}")
    expected_groups = {
        "CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED": 12,
        "DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED": 79,
        "OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED": 7,
        "REGISTRY_IDENTITY_UNRESOLVED": 10,
    }
    if details.get("groups") != expected_groups:
        raise ManifestError(f"V5 P1 blocker groups changed: {details.get('groups')}")
    if details.get("history") != {
        "distinct": 113, "occurrences": 423, "extras": 310,
    }:
        raise ManifestError(f"V5 status history census changed: {details.get('history')}")
    expected_labels = {
        "[MEASURED][IMAGE]": 9,
        "[MEASURED][OUTPUT-AUDIT]": 4,
        "[PROPOSED][DERIVED]": 11,
        "[PROPOSED][LOCAL]": 1,
        "[NONCLAIM][LOCAL]": 1,
        "[REPRODUCTION][LOCAL]": 1,
        "[DECLARED-SCOPE]": 1,
    }
    if details.get("labels") != expected_labels:
        raise ManifestError(f"V5 status label census changed: {details.get('labels')}")
    expected_closure = {
        "ItemMallUpdatePersonalDataVital": {
            "R": {"rows": 9, "blockers": 0, "wire": 8},
            "W": {"rows": 9, "blockers": 0, "wire": 8},
        },
        "ServerAddedInfoVital": {
            "R": {"rows": 3, "blockers": 0, "wire": 3},
            "W": {"rows": 3, "blockers": 0, "wire": 3},
        },
    }
    if details.get("closure") != expected_closure:
        raise ManifestError(f"V5 exact residual/wire proof changed: {details.get('closure')}")
    if details.get("v4_details") != {
        "daily_removed": 12, "composition_changed": 4,
        "composition_removed": 2, "stored_rows": 8_657,
        "stored_unknown": 3_963, "stored_numeric": 4_081,
    }:
        raise ManifestError("V4 replay details changed under V5")
    expansion = details.get("expansion_details")
    if not isinstance(expansion, list) or len(expansion) != 4:
        raise ManifestError("composition reference expansion census changed")
    if sum(int(item["child_rows"]) for item in expansion) != 64:
        raise ManifestError("composition logical-only child-row total changed")

    capture = status.capture_v4
    _registry, _stored, candidates, _counts, references, _v4_details = (
        capture.apply_daily_and_composition(OUT)
    )
    capture.verify_item_variants(candidates)
    item_counts = {
        key: len(rows) for key, rows in candidates.items() if key[0] == "ItemAttr"
    }
    if item_counts != EXPECTED_ITEM_VARIANTS:
        raise ManifestError(f"ItemAttr variants collapsed: {item_counts}")
    if len(references) != 4:
        raise ManifestError("embedded-child reference count changed")

    v4_lines = set(tsv.tables["PF_V4_P1_OPEN.tsv"].raw_lines)
    v5_lines = set(tsv.tables["PF_V5_P1_OPEN.tsv"].raw_lines)
    if len(v4_lines) != 110 or len(v5_lines) != 108 or not v5_lines < v4_lines:
        raise ManifestError("V5 status is not exact V4-minus-two reference snapshot")
    removed = [
        row for row in tsv.tables["PF_V4_P1_OPEN.tsv"].rows
        if tsv.tables["PF_V4_P1_OPEN.tsv"].raw_lines[
            tsv.tables["PF_V4_P1_OPEN.tsv"].rows.index(row)
        ] not in v5_lines
    ]
    if {row["message"] for row in removed} != {
        "ItemMallUpdatePersonalDataVital", "ServerAddedInfoVital"
    }:
        raise ManifestError("V5 status removed unexpected V4 references")
    audit_static_and_composition_boundaries(tsv)
    return {
        "stored": expected_stored,
        "logical": expected_logical,
        "plans": dict(details["plans"]),
        "priority": dict(details["priority"]),
        "groups": expected_groups,
        "closure": expected_closure,
        "composition_references": 4,
        "composition_removals": 2,
        "item_variants": item_counts,
    }


def audit_a5(snapshot: Snapshot, tsv: TsvAudit) -> dict[str, int]:
    if sha256_bytes(snapshot.files[CANONICAL_A5_TSV]) != CANONICAL_A5_SHA256:
        raise ManifestError("canonical V2 A5 TSV identity changed")
    rows = tsv.tables[CANONICAL_A5_TSV].rows
    points: set[tuple[str, str, str, str]] = set()
    locations: set[tuple[str, str, str]] = set()
    for row in rows:
        for item in row["mismatch_field_identity_reason_count"].split(" | "):
            if item in {"", "NONE"}:
                continue
            parts = item.rsplit("~", 2)
            if len(parts) != 3 or not parts[2].isdigit() or int(parts[2]) <= 0:
                raise ManifestError("malformed A5 mismatch identity/reason/count")
            identity, reason, _count = parts
            location = (row["message"], row["direction(W/R)"], identity)
            point = (*location, reason)
            if point in points:
                raise ManifestError("duplicate A5 mismatch identity/reason")
            locations.add(location)
            points.add(point)
    measured = {
        "rows": len(rows),
        "parse_success": sum(int(row["parse_success_instances"]) for row in rows),
        "static_open": sum(int(row["static_open_instances"]) for row in rows),
        "schema_not_applied": sum(
            int(row["schema_not_applied_instances"]) for row in rows
        ),
        "mismatch": sum(int(row["mismatch_instances"]) for row in rows),
        "mismatch_points": len(points),
        "field_locations": len(locations),
    }
    if measured != EXPECTED_A5:
        raise ManifestError(f"A5 measured census changed: {measured}")
    report = snapshot.text("PF_V5_FIELD_VALIDATION.md")
    required = (
        "386 mismatch instances at 3 field locations and 4 field+reason points",
        "Stored/reference A2 measured 8637 rows and 3943 UNKNOWN",
        "validation-only logical view measured 8701 rows and 3979 UNKNOWN",
        "APPLICABLE=628; STATIC_OPEN=364; SCHEMA_NOT_APPLIED=46",
        "no V3, V4, or V5 duplicate A5 TSV exists",
        "The eight historical V4 zero-observation rows are not copied here",
    )
    if any(snippet not in report for snippet in required):
        raise ManifestError("V5 A5 report lost a required carry-forward control")
    try:
        zero_section = report.split("## V5-touched zero observations", 1)[1].split(
            "## IMAGE schema impact", 1
        )[0]
    except IndexError as exc:
        raise ManifestError("V5 A5 zero-observation section changed") from exc
    zero_rows = [
        line for line in zero_section.splitlines()
        if line.startswith("| MEASURED/CAPTURE | `")
    ]
    expected_zero = {
        ("ItemMallUpdatePersonalDataVital", "R"),
        ("ItemMallUpdatePersonalDataVital", "W"),
        ("ServerAddedInfoVital", "R"),
        ("ServerAddedInfoVital", "W"),
    }
    observed_zero: set[tuple[str, str]] = set()
    for line in zero_rows:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 6:
            raise ManifestError("malformed V5 zero-observation report row")
        observed_zero.add((cells[1].strip("`"), cells[2]))
        if cells[3:5] != ["0", "0"]:
            raise ManifestError("V5 zero-observation row is nonzero")
    if len(zero_rows) != 4 or observed_zero != expected_zero:
        raise ManifestError(f"V5 zero-observation key census changed: {observed_zero}")
    return measured


HANDOFF_LABEL_SEQUENCE = (
    "[MEASURED][CAPTURE]", "[MEASURED][CAPTURE]", "[MEASURED][CAPTURE]",
    "[MEASURED][IMAGE]", "[MEASURED][IMAGE]", "[MEASURED][IMAGE]",
    "[MEASURED][IMAGE]", "[PROPOSED][DERIVED]", "[PROPOSED][DERIVED]",
    "[PROPOSED][DERIVED]", "[MEASURED][OUTPUT-AUDIT]",
    "[MEASURED][OUTPUT-AUDIT]", "[MEASURED][OUTPUT-AUDIT]",
    "[MEASURED][OUTPUT-AUDIT]", "[MEASURED][OUTPUT-AUDIT]",
    "[MEASURED][OUTPUT-AUDIT]", "[MEASURED][IMAGE]", "[MEASURED][IMAGE]",
    "[MEASURED][IMAGE]", "[MEASURED][IMAGE]", "[PROPOSED][LOCAL]",
    "[PROPOSED][LOCAL]", "[PROPOSED][LOCAL]", "[PROPOSED][LOCAL]",
    "[NONCLAIM][LOCAL]", "[REPRODUCTION][LOCAL]", "[DECLARED-SCOPE]",
)


def actionable_content(line: str) -> str:
    return re.sub(r"^(?:#{1,6}|[-*+]|\d+\.)\s+", "", line.strip())


def audit_handoff_claims(data: bytes) -> Counter[str]:
    text = data.decode("utf-8", errors="strict")
    measured: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        content = actionable_content(line)
        matching = [label for label in CLAIM_LABELS if content.startswith(label)]
        if len(matching) != 1:
            raise ManifestError(
                f"unlabelled/mixed V5 handoff claim: {line_number}:{line.strip()}"
            )
        label = matching[0]
        remainder = content[len(label):]
        if not remainder.startswith(" ") or EXTRA_BRACKET_RE.search(remainder):
            raise ManifestError(
                f"extra/malformed V5 handoff claim class: {line_number}:{line.strip()}"
            )
        measured.append(label)
    if tuple(measured) != HANDOFF_LABEL_SEQUENCE:
        raise ManifestError(f"V5 handoff claim-class grammar changed: {measured}")
    raw_byte_guard(HANDOFF_PATH.name, text)
    return Counter(measured)


def build_handoff(audit: Audit) -> bytes:
    a5, effective, tsv = audit.a5, audit.effective, audit.tsv
    stored = effective["stored"]
    logical = effective["logical"]
    lines = [
        f"# [MEASURED][CAPTURE] 🔴 A5 V5 ยัง mismatch {a5['mismatch']} instances / {a5['field_locations']} field locations / {a5['mismatch_points']} field+reason points",
        "",
        f"[MEASURED][CAPTURE] Canonical replay วัด pass {a5['parse_success']:,}, static-open {a5['static_open']:,}, schema-not-applied {a5['schema_not_applied']}; ผลแดงนี้ไม่ถูก rewrite เป็น IMAGE fact.",
        "",
        "[MEASURED][CAPTURE] V5 target มี zero observation เฉพาะ ItemMallUpdatePersonalDataVital และ ServerAddedInfoVital อย่างละ R/W รวม 4 keys ใน corpus นี้; ไม่ใช่หลักฐานว่า session อื่นไม่มีข้อมูล.",
        "",
        "## [MEASURED][IMAGE] V4 → V5 ที่เปลี่ยนจริง",
        "",
        "- [MEASURED][IMAGE] ลบ exact still-effective non-wire rows 20/20 จาก ten physical invalid-parameter callsites; ทุก callsite มี legacy R+W pair และไม่ใช้ import name เป็น global classifier.",
        f"- [MEASURED][IMAGE] stored/reference A2 = {stored['rows']:,}, UNKNOWN {stored['unknown']:,}, direct-invalid {stored['direct_invalid']}; logical validation-only = {logical['rows']:,}, UNKNOWN {logical['unknown']:,}, direct-invalid {logical['direct_invalid']}.",
        "- [MEASURED][IMAGE] Residual blocker = 0 ทุก target direction; ItemMall เหลือ 9 rows/8 proven-wire ต่อทิศ และ ServerAddedInfo เหลือ 3/3 ต่อทิศ.",
        "",
        "## [PROPOSED][DERIVED] Effective priority snapshot",
        "",
        "- [PROPOSED][DERIVED] P1 = 257/365 CLOSED, OPEN 108; P2 = 8/16; P3 = 71/138; overall = 336/519 CLOSED, OPEN 183.",
        "- [PROPOSED][DERIVED] P1 blocker groups = CALL/effect 12, dynamic dispatch 79, object alias 7, registry identity 10.",
        "",
        "## [MEASURED][OUTPUT-AUDIT] Duplicate และ reference accounting",
        "",
        f"- [MEASURED][OUTPUT-AUDIT] Full namespace = 133 files / 49 TSV / {tsv.total_rows:,} TSV rows; manifest table 132; exact duplicate files 0 และ within-TSV exact rows 0.",
        f"- [MEASURED][OUTPUT-AUDIT] delta+dedup keys {tsv.delta_dedup_count:,}/{tsv.delta_dedup_count:,} unique; full base targets {tsv.base_target_count}/{tsv.base_target_count}; non-N/A base_delta refs {tsv.base_delta_ref_count}/{tsv.base_delta_ref_count}; classmap keys 4.",
        f"- [MEASURED][OUTPUT-AUDIT] Cross-file raw rows ซ้ำได้เฉพาะ V2–V5 derived status snapshots: {tsv.repeated_lines} distinct / {tsv.repeated_occurrences} occurrences / {tsv.repeated_extras} extras; ทุกแถวเป็น NOT_A_NEW_EVIDENCE_ROW.",
        f"- [MEASURED][OUTPUT-AUDIT] V5 removal natural identity ใช้ full base target 20/20 unique; physical callsite pair {tsv.v5_physical_pairs}/{tsv.v5_physical_pairs}; priority message+priority 2/2. Historical A2 ADD tuple ยัง 2,194/2,194 unique, duplicate groups 0; ไม่ประกาศ universal identity ให้ schema อื่น.",
        "- [MEASURED][OUTPUT-AUDIT] Canonical A5 TSV singleton ยังเป็น PF_V2_FIELD_VALIDATION.tsv; ไม่มี V3/V4/V5 TSV สำเนา และ strict V5 validator ต้อง exit 1 ที่ mismatch 386 / 4 points.",
        "",
        "## [MEASURED][IMAGE] Composition และ serializer boundary",
        "",
        "- [MEASURED][IMAGE] embedded-child composition ยังคง 4 references + 2 removals; materialized child fields, ADD, UNCHANGED และ COPIED = 0.",
        "- [MEASURED][IMAGE] ItemAttr alternatives ยังแยก 13R+13W ที่ base และ 15R+15W ที่ StallItem; canonical_a2_action=NO_CHANGE.",
        "- [MEASURED][IMAGE] VitalData serializer ยัง UNKNOWN/WITHHELD และไม่ activate A2/A5; plans = 628 APPLICABLE / 364 STATIC_OPEN / 46 SCHEMA_NOT_APPLIED.",
        "",
        "## [PROPOSED][LOCAL] ลำดับอ่านและ reproduce",
        "",
        "1. [PROPOSED][LOCAL] อ่าน PF_V5_HANDOFF.md นี้ก่อน แล้ว PF_V5_EFFECTIVE_STATUS.md กับ PF_V5_FIELD_VALIDATION.md.",
        "2. [PROPOSED][LOCAL] ใช้ PF_V5_INVALID_PARAMETER_CLOSURE.md และสอง delta TSV เป็น IMAGE-static proof; compose ตาม REMOVE/CHANGED ห้าม append raw rows.",
        "3. [PROPOSED][LOCAL] ใช้ PF_V4_MANIFEST.md เป็น immutable predecessor; current index = exact canonical V5 prefix + marker + frozen V4 index bytes.",
        "",
        "[NONCLAIM][LOCAL] Checkpoint นี้ไม่ claim capture agreement, gameplay behavior, field values, import-wide invalid-parameter classification หรือ VitalData serializer.",
        "",
        "[REPRODUCTION][LOCAL] รัน `py -3 -B pf_build_v5_manifest.py --check`; integrity ต้อง PASS และ strict capture gate ต้อง fail เฉพาะ 386 mismatches / 4 points.",
        "",
        "[DECLARED-SCOPE] Local evidence integration ใต้ pf_bridge/external เท่านั้น; ไม่มี server/client runtime, workflow, queue, lease, Git, raw capture/dump หรือ GameClient mutation.",
        "",
    ]
    data = "\n".join(lines).encode("utf-8")
    audit_handoff_claims(data)
    return data


def audit_index_prefix(data: bytes) -> Counter[str]:
    prefix, marker = canonical_index_parts()
    if not data.startswith(prefix + marker):
        raise ManifestError("V5 index does not use exact status-builder prefix/marker")
    prefix_text = prefix.decode("utf-8", errors="strict")
    if "DE AD BE EF" in prefix_text or "[CAPTURE]" in prefix_text:
        raise ManifestError("canonical V5 index prefix crossed raw/CAPTURE boundary")
    labels: list[str] = []
    for line in prefix_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "# PF V5 current local index":
            continue
        matching = [label for label in CLAIM_LABELS if stripped.startswith(label)]
        if len(matching) != 1:
            raise ManifestError(f"unlabelled/mixed canonical V5 index line: {stripped}")
        label = matching[0]
        remainder = stripped[len(label):]
        if not remainder.startswith(" ") or EXTRA_BRACKET_RE.search(remainder):
            raise ManifestError(f"extra/malformed V5 index label: {stripped}")
        labels.append(label)
    expected = (
        "[PROPOSED][LOCAL]", "[MEASURED][OUTPUT-AUDIT]", "[DECLARED-SCOPE]",
    )
    if tuple(labels) != expected:
        raise ManifestError(f"canonical V5 index label grammar changed: {labels}")
    raw_byte_guard(INDEX_PATH.name, data.decode("utf-8", errors="strict"))
    return Counter(labels)


def build_index(audit: Audit) -> bytes:
    prefix, marker = canonical_index_parts()
    data = prefix + marker + audit.frozen_v4_index
    if (len(data), sha256_bytes(data)) != (V5_INDEX_SIZE, V5_INDEX_SHA256):
        raise ManifestError("derived canonical V5 index identity changed")
    status = status_module()
    if status.validate_index_bytes(data) != V5_INDEX_SHA256:
        raise ManifestError("status builder rejected canonical V5 index")
    if data[len(prefix + marker):] != audit.frozen_v4_index:
        raise ManifestError("V5 index did not preserve exact frozen V4 tail")
    audit_index_prefix(data)
    return data


def audit_all(
    *, allow_unpublished: bool, require_final: bool,
    transients: frozenset[str],
) -> Audit:
    snapshot = take_snapshot(
        allow_unpublished=allow_unpublished, transients=transients
    )
    frozen = verify_inputs(snapshot)
    for name in sorted(snapshot.files, key=str.casefold):
        snapshot.text(name)
    audit_exact_duplicate_files(snapshot.files)
    tsv = audit_tsvs(snapshot)
    audit_no_raw_proprietary(snapshot, tsv)
    run_component_checks()
    effective = audit_effective_outputs(snapshot, tsv)
    a5 = audit_a5(snapshot, tsv)
    provisional = Audit(snapshot, tsv, effective, a5, frozen, b"", b"")
    handoff = build_handoff(provisional)
    with_handoff = Audit(snapshot, tsv, effective, a5, frozen, handoff, b"")
    index = build_index(with_handoff)
    audit = Audit(snapshot, tsv, effective, a5, frozen, handoff, index)
    if require_final:
        if snapshot.files.get(HANDOFF_PATH.name) != handoff:
            raise ManifestError("PF_V5_HANDOFF.md differs byte-for-byte from derivation")
        if snapshot.files.get(INDEX_PATH.name) != index:
            raise ManifestError("00_SEARCH_HERE_FIRST.md differs from canonical V5 index")
        if MANIFEST_PATH.name not in snapshot.files:
            raise ManifestError("PF_V5_MANIFEST.md is absent")
    else:
        present = {
            name for name in (HANDOFF_PATH.name, MANIFEST_PATH.name)
            if name in snapshot.files
        }
        if not present:
            if snapshot.files[INDEX_PATH.name] != frozen:
                raise ManifestError("unpublished V5 integration lost exact V4 index")
        elif present == {HANDOFF_PATH.name, MANIFEST_PATH.name}:
            if (
                snapshot.files[HANDOFF_PATH.name] != handoff
                or snapshot.files[INDEX_PATH.name] != index
            ):
                raise ManifestError("existing V5 integration bytes are not current derivation")
        else:
            raise ManifestError(f"partial V5 integration state: {sorted(present)}")
    prospective = dict(snapshot.files)
    prospective[HANDOFF_PATH.name] = handoff
    prospective[INDEX_PATH.name] = index
    prospective.pop(MANIFEST_PATH.name, None)
    audit_exact_duplicate_files(prospective)
    assert_snapshot_current(snapshot, transients=transients)
    return audit


def artifact_bytes(audit: Audit, name: str) -> bytes:
    if name == HANDOFF_PATH.name:
        return audit.final_handoff
    if name == INDEX_PATH.name:
        return audit.final_index
    try:
        return audit.snapshot.files[name]
    except KeyError as exc:
        raise ManifestError(f"prospective artifact missing: {name}") from exc


def build_manifest(audit: Audit) -> bytes:
    snapshot, tsv, effective, a5 = (
        audit.snapshot, audit.tsv, audit.effective, audit.a5
    )
    handoff_labels = audit_handoff_claims(audit.final_handoff)
    index_labels = audit_index_prefix(audit.final_index)
    intersections = tsv.intersections
    stored = effective["stored"]
    logical = effective["logical"]
    label_text = lambda values: ", ".join(
        f"{label}={values.get(label, 0)}" for label in CLAIM_LABELS
    )
    lines = [
        "# PF V5 final local manifest and duplicate audit",
        "",
        f"[MEASURED][CAPTURE] 🔴 A5 V5 retains {a5['mismatch']} mismatch instances at {a5['field_locations']} field locations and {a5['mismatch_points']} field+reason points; capture conformance remains deliberately red.",
        "",
        "## Integrity and publication controls",
        "",
        "- [MEASURED][OUTPUT-AUDIT] Exact V4 manifest namespace is pinned byte-for-byte except the controlled search-index replacement; every reviewed V5 component/status/validator hash is pinned.",
        "- [MEASURED][OUTPUT-AUDIT] V5 component, effective-status, and ordinary capture-validator checks pass; strict validator is accepted only at rc=1 with exactly 386 mismatches / 4 points.",
        "- [MEASURED][OUTPUT-AUDIT] Client image size/SHA-256 is measured before and after gates and complete audits; no proprietary binary is included in this namespace.",
        "- [MEASURED][OUTPUT-AUDIT] Publication uses a held Windows CREATE_NEW handle, casefold residue preflight before and after lock acquisition, durable journal-before-replace, exact backups, BaseException rollback, foreign-state retention, and manifest-last replacement.",
        "",
        "## Duplicate and reference census",
        "",
        f"- [MEASURED][OUTPUT-AUDIT] Namespace: 133 files; manifest table: 132; TSV: 49; TSV data rows: {tsv.total_rows}; exact duplicate files: 0; within-TSV exact rows: 0.",
        f"- [MEASURED][OUTPUT-AUDIT] delta_key+dedup_key: {tsv.delta_dedup_count}/{tsv.delta_dedup_count} unique; full base targets: {tsv.base_target_count}/{tsv.base_target_count}; non-N/A base_delta_key references: {tsv.base_delta_ref_count}/{tsv.base_delta_ref_count}; classmap keys: 4.",
        f"- [MEASURED][OUTPUT-AUDIT] Allowed status repetitions: {tsv.repeated_lines} distinct / {tsv.repeated_occurrences} occurrences / {tsv.repeated_extras} extras; topology 4x92, 3x13, 2x8; all are IMAGE reference snapshots marked NOT_A_NEW_EVIDENCE_ROW.",
        f"- [MEASURED][OUTPUT-AUDIT] Pair intersections: V2∩V3={intersections[('PF_V2_P1_OPEN.tsv', 'PF_V3_P1_OPEN.tsv')]}; V2∩V4={intersections[('PF_V2_P1_OPEN.tsv', 'PF_V4_P1_OPEN.tsv')]}; V2∩V5={intersections[('PF_V2_P1_OPEN.tsv', 'PF_V5_P1_OPEN.tsv')]}; V3∩V4={intersections[('PF_V3_P1_OPEN.tsv', 'PF_V4_P1_OPEN.tsv')]}; V3∩V5={intersections[('PF_V3_P1_OPEN.tsv', 'PF_V5_P1_OPEN.tsv')]}; V4∩V5={intersections[('PF_V4_P1_OPEN.tsv', 'PF_V5_P1_OPEN.tsv')]}.",
        f"- [MEASURED][OUTPUT-AUDIT] V5 full-base removal identities: 20/20; physical R+W callsite pairs: {tsv.v5_physical_pairs}; priority message+priority identities: 2/2. Historical A2 ADD tuple remains {tsv.a2_add_semantic_count}/{tsv.a2_add_semantic_count} unique with {tsv.a2_add_semantic_duplicate_groups} duplicate groups; no universal identity is inferred for unrelated schemas.",
        "- [MEASURED][OUTPUT-AUDIT] Canonical A5 singleton is PF_V2_FIELD_VALIDATION.tsv; PF_V3_FIELD_VALIDATION.tsv, PF_V4_FIELD_VALIDATION.tsv, and PF_V5_FIELD_VALIDATION.tsv are forbidden.",
        f"- [MEASURED][OUTPUT-AUDIT] Handoff labels: {label_text(handoff_labels)}; canonical index prefix labels: {label_text(index_labels)}; unlabelled/mixed actionable V5 claims: 0.",
        "",
        "## Effective V5 checkpoint",
        "",
        "| claim class | measured/derived item | result |",
        "|---|---|---:|",
        "| PROPOSED/DERIVED | Priority 1 | 257/365 CLOSED; 108 OPEN |",
        "| PROPOSED/DERIVED | Priority 2 | 8/16 CLOSED; 8 OPEN |",
        "| PROPOSED/DERIVED | Priority 3 | 71/138 CLOSED; 67 OPEN |",
        "| PROPOSED/DERIVED | Overall | 336/519 CLOSED; 183 OPEN |",
        f"| MEASURED/IMAGE | stored/reference A2 | {stored['rows']} rows; UNKNOWN {stored['unknown']}; direct invalid {stored['direct_invalid']} |",
        f"| MEASURED/IMAGE | logical validation-only A2 | {logical['rows']} rows; UNKNOWN {logical['unknown']}; direct invalid {logical['direct_invalid']} |",
        "| MEASURED/IMAGE | numeric rows | stored 4081; logical 4103 |",
        "| MEASURED/IMAGE | schema plans | 628 applicable / 364 static-open / 46 not applied |",
        "| MEASURED/IMAGE | target residuals | 0 in all four message/direction buckets; nonempty wire proof retained |",
        "| MEASURED/IMAGE | embedded-child composition | 4 references + 2 removals; materialized child rows 0 |",
        "| MEASURED/IMAGE | ItemAttr alternatives | 13R+13W and 15R+15W remain separate |",
        "| MEASURED/IMAGE | VitalData boundary | serializer UNKNOWN/WITHHELD; A2/A5 activation 0 |",
        f"| MEASURED/CAPTURE | A5 pass/static-open/not-applied/mismatch | {a5['parse_success']} / {a5['static_open']} / {a5['schema_not_applied']} / {a5['mismatch']} |",
        "",
        "## Immutable index composition",
        "",
        f"- [MEASURED][OUTPUT-AUDIT] Current index is exactly the pinned status-builder prefix ({V5_PREFIX_SIZE} bytes / {V5_PREFIX_SHA256}) plus its exact marker ({V5_MARKER_SIZE} bytes / {V5_MARKER_SHA256}) plus the complete frozen V4 index ({V4_INDEX_SIZE} bytes / {V4_INDEX_SHA256}).",
        f"- [MEASURED][OUTPUT-AUDIT] Final index identity is {V5_INDEX_SIZE} bytes / {V5_INDEX_SHA256}; no other prefix or tail is accepted.",
        "",
        "## Scope",
        "",
        "[NONCLAIM][LOCAL] This integration does not claim capture agreement, gameplay behavior, field values, import-wide invalid-parameter classification, or a VitalData serializer.",
        "",
        "[DECLARED-SCOPE] Local evidence integration only. No server/client runtime, workflow, queue, lease, Git, raw capture/dump, or GameClient mutation is performed.",
        "",
        "## Artifact hashes",
        "",
        "[MEASURED][OUTPUT-AUDIT] PF_V5_MANIFEST.md does not hash itself. Every other row is from one stable audited snapshot, with deterministic handoff/index bytes substituted prospectively before commit.",
        "",
        f"- [MEASURED][OUTPUT-AUDIT] Frozen V4 manifest: {V4_MANIFEST_SIZE} bytes / {V4_MANIFEST_SHA256}.",
        f"- [MEASURED][IMAGE] Pinned client image: {IMAGE_SIZE} bytes / {IMAGE_SHA256}.",
        "",
        "| file | bytes | SHA-256 | TSV rows | source counts |",
        "|---|---:|---|---:|---|",
    ]
    table_rows = 0
    for name in sorted(snapshot.expected - {MANIFEST_PATH.name}, key=str.casefold):
        data = artifact_bytes(audit, name)
        if name in tsv.census:
            row_count, sources = tsv.census[name]
            row_text = str(row_count)
            source_text = ", ".join(
                f"{source}={sources[source]}" for source in sorted(sources)
            )
        else:
            row_text, source_text = "—", "—"
        lines.append(
            f"| `{name}` | {len(data)} | `{sha256_bytes(data).upper()}` | "
            f"{row_text} | `{source_text}` |"
        )
        table_rows += 1
    if table_rows != 132:
        raise ManifestError(f"V5 manifest artifact-table row census changed: {table_rows}")
    lines.extend((
        "", "## Reproduction and red conformance gate", "",
        "[REPRODUCTION][LOCAL] Run `py -3 -B pf_build_v5_manifest.py --check`. It is read-only and re-runs all V5 integrity gates plus the exact expected-negative strict validator.",
        "",
        "[MEASURED][CAPTURE] Ordinary validator integrity must pass while strict conformance must return rc=1 only for mismatch=386 and field_reason_points=4.",
        "",
    ))
    data = "\n".join(lines).encode("utf-8")
    raw_byte_guard(MANIFEST_PATH.name, data.decode("utf-8", errors="strict"))
    found = V4_TABLE_RE.findall(data.decode("utf-8", errors="strict"))
    if len(found) != 132 or len({name.casefold() for name, _s, _h in found}) != 132:
        raise ManifestError("generated V5 manifest table census/uniqueness changed")
    if MANIFEST_PATH.name in {name for name, _size, _digest in found}:
        raise ManifestError("V5 manifest attempted to hash itself")
    return data


def prospective_files(audit: Audit, manifest: bytes) -> dict[str, bytes]:
    files = {
        name: artifact_bytes(audit, name)
        for name in audit.snapshot.expected - {MANIFEST_PATH.name}
    }
    files[MANIFEST_PATH.name] = manifest
    if set(files) != set(audit.snapshot.expected) or len(files) != 133:
        raise ManifestError("prospective V5 namespace is incomplete")
    audit_exact_duplicate_files(files)
    return files


def verify_existing_integration_checkpoint(audit: Audit, manifest: bytes) -> None:
    snapshot = audit.snapshot
    present = {
        name for name in (HANDOFF_PATH.name, MANIFEST_PATH.name)
        if name in snapshot.files
    }
    if not present:
        if snapshot.files[INDEX_PATH.name] != audit.frozen_v4_index:
            raise ManifestError("unpublished integration lost exact V4 index")
        return
    if present != {HANDOFF_PATH.name, MANIFEST_PATH.name}:
        raise ManifestError(f"partial V5 integration checkpoint: {sorted(present)}")
    expected = {
        HANDOFF_PATH.name: audit.final_handoff,
        INDEX_PATH.name: audit.final_index,
        MANIFEST_PATH.name: manifest,
    }
    if any(snapshot.files.get(name) != data for name, data in expected.items()):
        raise ManifestError("complete V5 integration is not exact current derivation")


def windows_kernel32():
    if os.name != "nt":
        raise ManifestError("publication is unsupported outside Windows; audit/check remain read-only")
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.argtypes = (
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    )
    kernel32.CreateFileW.restype = wintypes.HANDLE
    kernel32.SetFileInformationByHandle.argtypes = (
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
    )
    kernel32.SetFileInformationByHandle.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


class FileDispositionInfo(ctypes.Structure):
    _fields_ = (("DeleteFile", ctypes.c_ubyte),)


def acquire_windows_lock(path: Path, scope: str) -> HeldWindowsLock:
    import msvcrt

    kernel32 = windows_kernel32()
    generic_read = 0x80000000
    generic_write = 0x40000000
    delete_access = 0x00010000
    file_share_read = 0x00000001
    create_new = 1
    file_attribute_normal = 0x00000080
    handle = kernel32.CreateFileW(
        str(path), generic_read | generic_write | delete_access,
        file_share_read, None, create_new, file_attribute_normal, None,
    )
    if handle == ctypes.c_void_p(-1).value:
        error = ctypes.get_last_error()
        if error in {80, 183}:
            raise ManifestError(f"active/stale publication lock exists: {path.name}")
        raise ManifestError(f"CreateFileW publication lock failed: winerror={error}")
    try:
        fd = msvcrt.open_osfhandle(int(handle), os.O_RDWR | os.O_BINARY)
    except BaseException:
        kernel32.CloseHandle(handle)
        raise
    payload = (
        json.dumps(
            {"pid": os.getpid(), "scope": scope, "token": os.urandom(24).hex()},
            sort_keys=True, separators=(",", ":"),
        ).encode("ascii") + b"\n"
    )
    try:
        os.write(fd, payload)
        os.fsync(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        if os.read(fd, len(payload) + 1) != payload:
            raise ManifestError("publication lock handle readback failed")
    except BaseException:
        os.close(fd)
        raise
    return HeldWindowsLock(fd=fd, payload=payload, path=path)


def assert_held_windows_lock(held: HeldWindowsLock) -> None:
    try:
        os.lseek(held.fd, 0, os.SEEK_SET)
        data = os.read(held.fd, len(held.payload) + 1)
    except OSError as exc:
        held.retain = True
        raise ManifestError("publication lock handle is no longer readable") from exc
    if data != held.payload:
        held.retain = True
        raise ManifestError("publication lock handle payload changed")


def release_windows_lock(held: HeldWindowsLock) -> None:
    import msvcrt

    if held.retain:
        os.close(held.fd)
        return
    assert_held_windows_lock(held)
    kernel32 = windows_kernel32()
    handle = msvcrt.get_osfhandle(held.fd)
    disposition = FileDispositionInfo(1)
    if not kernel32.SetFileInformationByHandle(
        handle, 4, ctypes.byref(disposition), ctypes.sizeof(disposition)
    ):
        error = ctypes.get_last_error()
        held.retain = True
        os.close(held.fd)
        raise ManifestError(
            f"handle-owned lock disposition failed: winerror={error}"
        )
    os.close(held.fd)
    if held.path.exists():
        raise ManifestError("owned lock release did not remove pathname")


@contextmanager
def exclusive_publication_lock(path: Path, scope: str) -> Iterator[HeldWindowsLock]:
    held = acquire_windows_lock(path, scope)
    try:
        yield held
    finally:
        release_windows_lock(held)


def write_exclusive(path: Path, data: bytes) -> None:
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_BINARY, 0o600
    )
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def append_journal(path: Path, event: Mapping[str, object]) -> None:
    with path.open("ab") as handle:
        handle.write(
            json.dumps(event, sort_keys=True, separators=(",", ":")).encode("ascii")
            + b"\n"
        )
        handle.flush()
        os.fsync(handle.fileno())


def cleanup_transaction(
    root: Path, directory: Path, known_paths: Sequence[Path]
) -> None:
    if (
        directory.resolve().parent != root.resolve()
        or not directory.name.casefold().startswith(TX_PREFIX.casefold())
    ):
        raise ManifestError("refusing cleanup outside exact V5 transaction directory")
    actual, allowed = set(directory.iterdir()), set(known_paths)
    if actual - allowed or any(path.is_symlink() or not path.is_file() for path in actual):
        raise ManifestError("unknown transaction content retained for manual recovery")
    for path in known_paths:
        if path.exists():
            path.unlink()
    directory.rmdir()


def rollback_destination(
    destination: Path, original: bytes | None, original_identity: tuple[int, int] | None,
    backup: Path | None, staged_identity: tuple[int, int], staged_data: bytes,
) -> None:
    if (
        destination.exists()
        and file_identity(destination) == staged_identity
        and destination.read_bytes() == staged_data
    ):
        if original is None:
            destination.unlink()
        else:
            if backup is None or not backup.is_file() or backup.read_bytes() != original:
                raise ManifestError(f"rollback backup missing/drifted: {destination.name}")
            shutil.copyfile(backup, destination)
            with destination.open("r+b") as handle:
                handle.flush()
                os.fsync(handle.fileno())
            if destination.read_bytes() != original:
                raise ManifestError(f"rollback byte verification failed: {destination.name}")
        return
    if original is None and not destination.exists():
        return
    if (
        original is not None
        and destination.exists()
        and original_identity is not None
        and file_identity(destination) == original_identity
        and destination.read_bytes() == original
    ):
        return
    raise ManifestError(
        f"rollback encountered foreign/uncertain destination: {destination.name}"
    )


def replace_transaction(
    root: Path,
    outputs: Mapping[str, bytes],
    before_files: Mapping[str, bytes | None],
    before_identities: Mapping[str, tuple[int, int] | None],
    held: HeldWindowsLock,
    verify_before: Callable[[Path], None],
    verify_after: Callable[[Path], None],
    hook: Callable[[str, Path | None], None] | None = None,
) -> None:
    if tuple(outputs) != PUBLISHED_OUTPUTS or set(outputs) != OWNED_NAMES:
        raise ManifestError("publication order/boundary changed; manifest must be last")
    transaction = Path(tempfile.mkdtemp(prefix=TX_PREFIX, dir=root))
    if transaction.resolve().parent != root.resolve():
        held.retain = True
        raise ManifestError("transaction directory escaped output root")
    journal = transaction / "journal.jsonl"
    staged = {
        name: transaction / f"{index}.new"
        for index, name in enumerate(outputs)
    }
    backups = {
        name: transaction / f"{index}.old"
        for index, name in enumerate(outputs)
    }
    known_paths = [*staged.values(), *backups.values(), journal]
    stage_identities: dict[str, tuple[int, int]] = {}
    attempted: list[str] = []
    journal_created = False
    try:
        for name, data in outputs.items():
            destination = root / name
            if destination.parent.resolve() != root.resolve():
                raise ManifestError(f"publication target escaped root: {name}")
            write_exclusive(staged[name], data)
            stage_identities[name] = file_identity(staged[name])
            original = before_files[name]
            if original is not None:
                write_exclusive(backups[name], original)
        verify_before(transaction)
        write_exclusive(journal, b"")
        journal_created = True
        append_journal(journal, {
            "event": "PREPARED",
            "manifest_last": MANIFEST_PATH.name,
            "destinations": [
                {
                    "name": name,
                    "existed": before_files[name] is not None,
                    "old_sha256": (
                        sha256_bytes(before_files[name])
                        if before_files[name] is not None else None
                    ),
                    "new_sha256": sha256_bytes(data),
                    "staged": staged[name].name,
                    "backup": backups[name].name,
                }
                for name, data in outputs.items()
            ],
        })
        assert_held_windows_lock(held)
        for name, data in outputs.items():
            append_journal(journal, {"event": "REPLACE_INTENT", "name": name})
            attempted.append(name)
            assert_held_windows_lock(held)
            os.replace(staged[name], root / name)
            if hook is not None:
                hook("after_replace", root / name)
            if (root / name).read_bytes() != data:
                raise ManifestError(f"post-replace readback mismatch: {name}")
            append_journal(journal, {"event": "REPLACE_DONE", "name": name})
        verify_after(transaction)
        assert_held_windows_lock(held)
        append_journal(journal, {"event": "FINAL_REDERIVATION_PASS"})
    except BaseException as original_error:
        rollback_errors: list[str] = []
        for name in reversed(attempted):
            try:
                if journal_created:
                    append_journal(journal, {"event": "ROLLBACK_INTENT", "name": name})
                rollback_destination(
                    root / name,
                    before_files[name],
                    before_identities[name],
                    backups[name] if before_files[name] is not None else None,
                    stage_identities[name],
                    outputs[name],
                )
                if journal_created:
                    append_journal(journal, {"event": "ROLLBACK_DONE", "name": name})
            except BaseException as exc:
                rollback_errors.append(f"{name}:{type(exc).__name__}")
        if rollback_errors:
            held.retain = True
            raise ManifestError(
                "publication failed; foreign/uncertain rollback state retained: "
                + ",".join(rollback_errors)
            ) from original_error
        try:
            if journal_created:
                append_journal(journal, {"event": "ROLLED_BACK_AFTER_FAILURE"})
            cleanup_transaction(root, transaction, known_paths)
        except BaseException as cleanup_error:
            held.retain = True
            raise ManifestError(
                "publication failed; rollback cleanup incomplete; lock/transaction retained"
            ) from cleanup_error
        raise
    else:
        try:
            assert_held_windows_lock(held)
            cleanup_transaction(root, transaction, known_paths)
        except BaseException as cleanup_error:
            held.retain = True
            raise ManifestError(
                "checkpoint committed but cleanup failed; lock/transaction retained"
            ) from cleanup_error


def publish_transaction(audit: Audit, manifest: bytes, held: HeldWindowsLock) -> None:
    before = audit.snapshot
    outputs = {
        HANDOFF_PATH.name: audit.final_handoff,
        INDEX_PATH.name: audit.final_index,
        MANIFEST_PATH.name: manifest,
    }
    before_files = {
        name: before.files.get(name) for name in PUBLISHED_OUTPUTS
    }
    before_identities = {
        name: before.identities.get(name) for name in PUBLISHED_OUTPUTS
    }

    def verify_before(transaction: Path) -> None:
        assert_snapshot_current(
            before, transients=frozenset({LOCK_PATH.name, transaction.name})
        )

    def verify_after(transaction: Path) -> None:
        transients = frozenset({LOCK_PATH.name, transaction.name})
        after = audit_all(
            allow_unpublished=False, require_final=True, transients=transients
        )
        for name in before.expected - set(PUBLISHED_OUTPUTS):
            if after.snapshot.files[name] != before.files[name]:
                raise ManifestError(f"nonpublished artifact changed across commit: {name}")
        if after.snapshot.image_fingerprint != before.image_fingerprint:
            raise ManifestError("client image changed across commit")
        rederived_manifest = build_manifest(after)
        prospective_files(after, rederived_manifest)
        if rederived_manifest != manifest:
            raise ManifestError("postcommit re-derived manifest changed")
        for name, data in outputs.items():
            if after.snapshot.files[name] != data:
                raise ManifestError(f"postcommit output readback mismatch: {name}")
        assert_snapshot_current(after.snapshot, transients=transients)

    replace_transaction(
        OUT, outputs, before_files, before_identities, held,
        verify_before, verify_after,
    )


def publication_self_test() -> None:
    if os.name != "nt":
        raise ManifestError("Windows publication self-test is unavailable")
    with tempfile.TemporaryDirectory(prefix="pf_v5_manifest_selftest_") as raw:
        root = Path(raw)
        handoff = root / HANDOFF_PATH.name
        index = root / INDEX_PATH.name
        manifest = root / MANIFEST_PATH.name
        handoff.write_bytes(b"old-handoff")
        index.write_bytes(b"old-index")
        outputs = {
            HANDOFF_PATH.name: b"new-handoff",
            INDEX_PATH.name: b"new-index",
            MANIFEST_PATH.name: b"new-manifest",
        }

        stale_tx = root / (TX_PREFIX.swapcase() + "STALE")
        stale_tx.mkdir()
        stale_journal = stale_tx / "JOURNAL.JSONL"
        stale_backup = stale_tx / "0.OLD"
        stale_stage = root / (HANDOFF_PATH.name + ".stage").upper()
        cache = root / "__PYCACHE__"
        cache.mkdir()
        stale_cache = cache / "MANIFEST.PYC"
        stale_journal.write_bytes(b"journal")
        stale_backup.write_bytes(b"backup")
        stale_stage.write_bytes(b"stage")
        stale_cache.write_bytes(b"cache")
        before_bytes = {handoff: handoff.read_bytes(), index: index.read_bytes()}
        try:
            assert_publication_clean(root)
        except ManifestError:
            pass
        else:
            raise ManifestError("case-variant stale residue preflight failed open")
        if any(path.read_bytes() != data for path, data in before_bytes.items()):
            raise ManifestError("stale residue preflight changed owned outputs")
        if (
            stale_journal.read_bytes() != b"journal"
            or stale_backup.read_bytes() != b"backup"
            or stale_stage.read_bytes() != b"stage"
            or stale_cache.read_bytes() != b"cache"
        ):
            raise ManifestError("stale residue preflight changed recovery bytes")
        shutil.rmtree(stale_tx)
        shutil.rmtree(cache)
        stale_stage.unlink()

        foreign_lock = root / LOCK_PATH.name.swapcase()
        foreign_lock.write_bytes(b"foreign-lock")
        try:
            assert_publication_clean(root)
        except ManifestError:
            pass
        else:
            raise ManifestError("case-variant foreign lock preflight failed open")
        if foreign_lock.read_bytes() != b"foreign-lock":
            raise ManifestError("foreign lock preflight changed bytes")
        foreign_lock.unlink()

        challenger = root / "challenger.lock"
        challenger.write_bytes(b"challenger")
        with exclusive_publication_lock(root / LOCK_PATH.name, "PF_V5_MANIFEST_SELFTEST") as held:
            assert_publication_clean(root, allowed_lock=held.path)
            try:
                acquire_windows_lock(root / LOCK_PATH.name, "SECOND_OWNER")
            except ManifestError:
                pass
            else:
                held.retain = True
                raise ManifestError("held lock admitted a second owner")
            try:
                held.path.unlink()
            except OSError:
                pass
            else:
                held.retain = True
                raise ManifestError("held lock allowed pathname unlink")
            try:
                os.replace(challenger, held.path)
            except OSError:
                pass
            else:
                held.retain = True
                raise ManifestError("held lock allowed pathname replacement")
            raced = root / (INDEX_PATH.name + ".backup").upper()
            raced.write_bytes(b"raced")
            try:
                assert_publication_clean(root, allowed_lock=held.path)
            except ManifestError:
                pass
            else:
                held.retain = True
                raise ManifestError("held-lock residue recheck failed open")
            if any(path.read_bytes() != data for path, data in before_bytes.items()):
                held.retain = True
                raise ManifestError("held-lock residue recheck changed outputs")
            raced.unlink()
        if (root / LOCK_PATH.name).exists() or challenger.read_bytes() != b"challenger":
            raise ManifestError("held-handle lock release self-test failed")

        def before_mapping() -> tuple[dict[str, bytes | None], dict[str, tuple[int, int] | None]]:
            files = {
                name: (root / name).read_bytes() if (root / name).exists() else None
                for name in PUBLISHED_OUTPUTS
            }
            identities = {
                name: file_identity(root / name) if (root / name).exists() else None
                for name in PUBLISHED_OUTPUTS
            }
            return files, identities

        before_files, before_ids = before_mapping()
        with exclusive_publication_lock(root / LOCK_PATH.name, "PF_V5_MANIFEST_SELFTEST") as held:
            assert_publication_clean(root, allowed_lock=held.path)
            replace_transaction(
                root, outputs, before_files, before_ids, held,
                lambda tx: assert_publication_clean(
                    root, allowed_lock=held.path, allowed_tx=tx
                ),
                lambda tx: None,
            )
        if (
            handoff.read_bytes() != outputs[HANDOFF_PATH.name]
            or index.read_bytes() != outputs[INDEX_PATH.name]
            or manifest.read_bytes() != outputs[MANIFEST_PATH.name]
            or publication_residue_at(root)
        ):
            raise ManifestError("successful transaction self-test failed")

        handoff.write_bytes(b"rollback-handoff")
        index.write_bytes(b"rollback-index")
        manifest.unlink()
        before_files, before_ids = before_mapping()

        def abort_after_index(_event: str, target: Path | None) -> None:
            if target == index:
                raise InjectedAbort("synthetic BaseException after index replace")

        try:
            with exclusive_publication_lock(root / LOCK_PATH.name, "PF_V5_MANIFEST_SELFTEST") as held:
                assert_publication_clean(root, allowed_lock=held.path)
                replace_transaction(
                    root, outputs, before_files, before_ids, held,
                    lambda tx: None, lambda tx: None, abort_after_index,
                )
        except InjectedAbort:
            pass
        else:
            raise ManifestError("BaseException rollback injection failed open")
        if (
            handoff.read_bytes() != b"rollback-handoff"
            or index.read_bytes() != b"rollback-index"
            or manifest.exists()
            or publication_residue_at(root)
        ):
            raise ManifestError("BaseException rollback did not restore exact state")

        before_files, before_ids = before_mapping()

        def foreign_after_handoff(_event: str, target: Path | None) -> None:
            if target == handoff:
                target.write_bytes(b"foreign-destination")
                raise InjectedAbort("foreign destination mutation")

        try:
            with exclusive_publication_lock(root / LOCK_PATH.name, "PF_V5_MANIFEST_SELFTEST") as held:
                replace_transaction(
                    root, outputs, before_files, before_ids, held,
                    lambda tx: None, lambda tx: None, foreign_after_handoff,
                )
        except ManifestError:
            pass
        else:
            raise ManifestError("foreign destination rollback test failed open")
        if handoff.read_bytes() != b"foreign-destination":
            raise ManifestError("foreign uncertain destination was overwritten")
        retained = [root / LOCK_PATH.name, *root.glob(TX_PREFIX + "*")]
        if not (root / LOCK_PATH.name).exists() or not list(root.glob(TX_PREFIX + "*")):
            raise ManifestError("foreign uncertain state was not retained")
        for path in retained:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink(missing_ok=True)


def summary(audit: Audit, manifest: bytes) -> str:
    return (
        "PASS V5 manifest namespace=133 table=132 TSV=49 rows=22048 "
        f"delta_dedup={audit.tsv.delta_dedup_count} "
        f"base_targets={audit.tsv.base_target_count} "
        f"status_repeats={audit.tsv.repeated_lines}/"
        f"{audit.tsv.repeated_occurrences}/{audit.tsv.repeated_extras} "
        f"manifest_sha256={sha256_bytes(manifest)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--audit-only", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

    if args.self_test:
        publication_self_test()
        print("PASS V5 manifest held-lock/residue/rollback publication self-test")
        return 0

    if args.check or args.audit_only:
        audit = audit_all(
            allow_unpublished=args.audit_only,
            require_final=args.check,
            transients=frozenset(),
        )
        manifest = build_manifest(audit)
        verify_existing_integration_checkpoint(audit, manifest)
        prospective_files(audit, manifest)
        if args.check and audit.snapshot.files.get(MANIFEST_PATH.name) != manifest:
            raise ManifestError("PF_V5_MANIFEST.md differs from full re-derivation")
        assert_snapshot_current(audit.snapshot, transients=frozenset())
        print(summary(audit, manifest))
        return 0

    assert_publication_clean(OUT)
    success = ""
    with exclusive_publication_lock(LOCK_PATH, "PF_V5_MANIFEST") as held:
        assert_publication_clean(OUT, allowed_lock=held.path)
        audit = audit_all(
            allow_unpublished=True,
            require_final=False,
            transients=frozenset({LOCK_PATH.name}),
        )
        manifest = build_manifest(audit)
        verify_existing_integration_checkpoint(audit, manifest)
        prospective_files(audit, manifest)
        assert_held_windows_lock(held)
        publish_transaction(audit, manifest, held)
        success = f"PF_V5_MANIFEST.md {sha256_bytes(manifest)}"
    print(success)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestError as exc:
        raise SystemExit(f"ERROR: {exc}")
