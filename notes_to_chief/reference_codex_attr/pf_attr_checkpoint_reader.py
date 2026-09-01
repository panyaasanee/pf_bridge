#!/usr/bin/env python3
"""Strict reader for published Pirate Force attribute checkpoints.

The top-level manifest is the single publication pointer.  This module resolves
that pointer to a content-addressed generation directory, verifies every byte once,
and keeps the verified payloads in memory.  Consumers must use :meth:`bytes`,
:meth:`text`, or :meth:`tsv`; no method reopens an artifact after verification.
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import io
import json
import os
import re
import stat
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping, Sequence, cast


HERE = Path(__file__).resolve().parent
READER_PATH = Path(__file__).absolute()
DEFAULT_MANIFEST_PATH = HERE / "PF_ATTR_GENERATION_MANIFEST.json"
MANIFEST_FORMAT = "PF_ATTR_GENERATION_MANIFEST_V4"
LEGACY_V3_MANIFEST_FORMAT = "PF_ATTR_GENERATION_MANIFEST_V3"
LEGACY_MANIFEST_FORMAT = "PF_ATTR_GENERATION_MANIFEST_V2"
INTERNAL_MANIFEST_NAME = "manifest.json"
AUTHORITATIVE_READER = Path(__file__).name
PUBLICATION_RULE = (
    "resolve artifact_root and parse the same verified in-memory bytes; "
    "top-level artifact mirrors are non-authoritative"
)
LEGACY_V3_READER_SHA256_ALLOWLIST = frozenset(
    {
        "4b3d6b656d6d58c4e995670ed896bcbba2b7a6990380928ea1fffa0dc0246ac5",
        "9da58e71d4d62d82f881051d7e912f862a782dacaa6699151756bfb69168a418",
    }
)

_LEGACY_MANIFEST_FIELDS = frozenset(
    {
        "format",
        "generation_id",
        "image_sha256",
        "generator_sha256",
        "generator_snapshot",
        "artifact_root",
        "artifact_count",
        "artifacts",
        "artifact_sizes",
        "authoritative_reader",
        "compatibility_mirrors_authoritative",
        "publication_rule",
    }
)
_MANIFEST_FIELDS = _LEGACY_MANIFEST_FIELDS | {"authoritative_reader_sha256"}
_LOWER_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
_WINDOWS_RESERVED_RE = re.compile(
    r"(?:con|prn|aux|nul|conin\$|conout\$|com[1-9\u00b9\u00b2\u00b3]|"
    r"lpt[1-9\u00b9\u00b2\u00b3])(?:\..*)?\Z",
    re.IGNORECASE,
)
_WINDOWS_FORBIDDEN_NAME_CHARS = frozenset('<>:"/\\|?*')


class AttrCheckpointError(ValueError):
    """Raised when a checkpoint is absent, malformed, or fails verification."""


def _assert_no_reparse_components(path: Path, label: str) -> None:
    """Reject symlink/junction traversal before reading checkpoint material."""
    absolute = Path(os.path.abspath(path))
    parts = absolute.parts
    if not parts or not absolute.anchor:
        raise AttrCheckpointError("%s path is not absolute" % label)
    current = Path(parts[0])
    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.GetFileAttributesW.argtypes = (ctypes.c_wchar_p,)
        kernel32.GetFileAttributesW.restype = ctypes.c_uint32
        for part in parts[1:]:
            current = current / part
            ctypes.set_last_error(0)
            attributes = kernel32.GetFileAttributesW(str(current))
            if attributes == 0xFFFFFFFF:
                raise AttrCheckpointError(
                    "cannot inspect %s path component (winerror %d)"
                    % (label, ctypes.get_last_error())
                )
            if attributes & 0x00000400:
                raise AttrCheckpointError("%s path traverses a reparse point" % label)
        return
    for part in parts[1:]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except OSError as exc:
            raise AttrCheckpointError("cannot inspect %s path: %s" % (label, exc)) from exc
        if stat.S_ISLNK(mode):
            raise AttrCheckpointError("%s path traverses a symbolic link" % label)


def _immutable_mapping(values: Mapping[str, Any]) -> Mapping[str, Any]:
    """Recursively detach and freeze a JSON-compatible mapping."""

    frozen: dict[str, Any] = {}
    for key, value in values.items():
        if isinstance(value, dict):
            frozen[key] = _immutable_mapping(value)
        elif isinstance(value, list):
            frozen[key] = tuple(value)
        else:
            frozen[key] = value
    return MappingProxyType(frozen)


@dataclass(frozen=True, slots=True)
class VerifiedAttrCheckpoint:
    """A checkpoint whose manifest and artifact bytes have all been verified.

    ``artifact_root`` is the absolute local directory resolved from the exact
    relative ``artifact_root_relative`` value in the manifest.  All mappings
    are read-only and all payloads are immutable ``bytes`` objects.
    """

    manifest_path: Path
    artifact_root: Path
    artifact_root_relative: str
    format: str
    generation_id: str
    image_sha256: str
    generator_sha256: str
    generator_snapshot: str
    generator_snapshot_path: Path
    artifact_count: int
    artifact_hashes: Mapping[str, str]
    artifact_sizes: Mapping[str, int]
    authoritative_reader: str
    authoritative_reader_sha256: str
    compatibility_mirrors_authoritative: bool
    publication_rule: str
    manifest: Mapping[str, Any] = field(repr=False)
    manifest_bytes: bytes = field(repr=False)
    generator_snapshot_bytes: bytes = field(repr=False)
    artifact_bytes: Mapping[str, bytes] = field(repr=False)

    @property
    def artifacts(self) -> Mapping[str, str]:
        """The manifest's immutable ``name -> SHA-256`` mapping."""

        return self.artifact_hashes

    @property
    def artifact_names(self) -> tuple[str, ...]:
        """Artifact basenames in deterministic order."""

        return tuple(sorted(self.artifact_bytes))

    def bytes(self, name: str) -> bytes:
        """Return the already-verified bytes for *name* without reopening it."""

        if not isinstance(name, str):
            raise TypeError("artifact name must be str")
        try:
            return self.artifact_bytes[name]
        except KeyError:
            raise KeyError("artifact is not present in the verified checkpoint: %r" % name) from None

    def text(self, name: str) -> str:
        """Decode an already-verified artifact as strict UTF-8 text."""

        payload = self.bytes(name)
        try:
            return payload.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise AttrCheckpointError(
                "verified artifact is not strict UTF-8: %s" % name
            ) from exc

    def tsv(self, name: str) -> tuple[Mapping[str, str], ...]:
        """Parse a verified TSV artifact into immutable header-keyed rows.

        The header must be non-empty and unique, and every data row must have
        exactly the header's width.  Parsing starts from the retained verified
        bytes; the filesystem is never consulted again.
        """

        if not isinstance(name, str):
            raise TypeError("artifact name must be str")
        if not name.lower().endswith(".tsv"):
            raise AttrCheckpointError("artifact does not have a .tsv basename: %s" % name)
        text = self.text(name)
        if "\x00" in text:
            raise AttrCheckpointError("verified TSV contains a NUL character: %s" % name)
        reader = csv.reader(io.StringIO(text, newline=""), delimiter="\t", strict=True)
        try:
            header = next(reader)
        except StopIteration:
            raise AttrCheckpointError("verified TSV is empty: %s" % name) from None
        except csv.Error as exc:
            raise AttrCheckpointError("verified TSV header is malformed: %s" % name) from exc
        if not header or any(column == "" for column in header):
            raise AttrCheckpointError("verified TSV has an empty header column: %s" % name)
        if len(set(header)) != len(header):
            raise AttrCheckpointError("verified TSV has duplicate header columns: %s" % name)

        rows: list[Mapping[str, str]] = []
        try:
            for row in reader:
                if len(row) != len(header):
                    raise AttrCheckpointError(
                        "verified TSV row %d has %d columns; expected %d: %s"
                        % (reader.line_num, len(row), len(header), name)
                    )
                rows.append(MappingProxyType(dict(zip(header, row))))
        except csv.Error as exc:
            raise AttrCheckpointError(
                "verified TSV is malformed near physical line %d: %s"
                % (reader.line_num, name)
            ) from exc
        return tuple(rows)


def _duplicate_rejecting_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AttrCheckpointError("duplicate JSON key: %r" % key)
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise AttrCheckpointError("non-standard JSON numeric constant: %s" % value)


def _parse_manifest(payload: bytes, source: Path) -> dict[str, Any]:
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise AttrCheckpointError("manifest is not strict UTF-8: %s" % source) from exc
    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_duplicate_rejecting_object,
            parse_constant=_reject_json_constant,
        )
    except AttrCheckpointError:
        raise
    except json.JSONDecodeError as exc:
        raise AttrCheckpointError(
            "manifest is not valid JSON at line %d column %d: %s"
            % (exc.lineno, exc.colno, source)
        ) from exc
    if type(parsed) is not dict:
        raise AttrCheckpointError("manifest top level must be a JSON object: %s" % source)
    return cast(dict[str, Any], parsed)


def _read_regular_file_once(path: Path, label: str) -> bytes:
    """Open *path* once and return one in-memory byte snapshot."""

    try:
        if path.is_symlink():
            raise AttrCheckpointError("%s must not be a symbolic link: %s" % (label, path))
        with path.open("rb") as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                raise AttrCheckpointError("%s is not a regular file: %s" % (label, path))
            return handle.read()
    except AttrCheckpointError:
        raise
    except OSError as exc:
        raise AttrCheckpointError("cannot read %s %s: %s" % (label, path, exc)) from exc


def _require_exact_fields(manifest: Mapping[str, Any], expected: frozenset[str]) -> None:
    actual = set(manifest)
    if actual != expected:
        missing = ",".join(sorted(expected - actual)) or "-"
        unknown = ",".join(sorted(actual - expected)) or "-"
        raise AttrCheckpointError(
            "manifest field set mismatch (missing=%s; unknown=%s)" % (missing, unknown)
        )


def _require_string(manifest: Mapping[str, Any], name: str) -> str:
    value = manifest[name]
    if type(value) is not str:
        raise AttrCheckpointError("manifest field %s must be a string" % name)
    return cast(str, value)


def _require_lower_sha256(manifest: Mapping[str, Any], name: str) -> str:
    value = _require_string(manifest, name)
    if _LOWER_SHA256_RE.fullmatch(value) is None:
        raise AttrCheckpointError("manifest field %s must be 64 lowercase hex characters" % name)
    return value


def _require_nonnegative_int(value: Any, label: str) -> int:
    if type(value) is not int or value < 0:
        raise AttrCheckpointError("%s must be a nonnegative JSON integer" % label)
    return cast(int, value)


def _stable_key(*parts: object) -> str:
    text = "|".join(str(part) for part in parts)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _validate_relative_posix_path(value: str, label: str) -> None:
    if not value or "\\" in value or "\x00" in value:
        raise AttrCheckpointError("%s must be a nonempty relative POSIX path" % label)
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value:
        raise AttrCheckpointError("%s must be a normalized relative POSIX path" % label)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise AttrCheckpointError("%s contains an unsafe path component" % label)


def _validate_safe_basename(name: Any) -> str:
    if type(name) is not str or not name:
        raise AttrCheckpointError("artifact keys must be nonempty strings")
    value = cast(str, name)
    if value in {".", ".."} or value[-1] in {" ", "."}:
        raise AttrCheckpointError("unsafe artifact basename: %r" % value)
    if value.casefold() == INTERNAL_MANIFEST_NAME.casefold():
        raise AttrCheckpointError("artifact basename collides with internal manifest: %r" % value)
    if any(character in _WINDOWS_FORBIDDEN_NAME_CHARS for character in value):
        raise AttrCheckpointError("unsafe artifact basename: %r" % value)
    if any(ord(character) < 32 for character in value):
        raise AttrCheckpointError("unsafe artifact basename: %r" % value)
    if _WINDOWS_RESERVED_RE.fullmatch(value) is not None:
        raise AttrCheckpointError("Windows-reserved artifact basename: %r" % value)
    # The checks above deliberately use Windows rules even when imported on a
    # non-Windows verifier, so an accepted checkpoint resolves identically here.
    if Path(value).name != value or Path(value).anchor:
        raise AttrCheckpointError("artifact key is not a safe basename: %r" % value)
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise AttrCheckpointError("artifact basename is not valid Unicode: %r" % value) from exc
    return value


def _validate_artifact_maps(
    manifest: Mapping[str, Any],
) -> tuple[dict[str, str], dict[str, int]]:
    raw_hashes = manifest["artifacts"]
    raw_sizes = manifest["artifact_sizes"]
    if type(raw_hashes) is not dict:
        raise AttrCheckpointError("manifest field artifacts must be a JSON object")
    if type(raw_sizes) is not dict:
        raise AttrCheckpointError("manifest field artifact_sizes must be a JSON object")

    hashes: dict[str, str] = {}
    folded_names: dict[str, str] = {}
    for raw_name, raw_hash in raw_hashes.items():
        name = _validate_safe_basename(raw_name)
        folded = name.casefold()
        if folded in folded_names:
            raise AttrCheckpointError(
                "artifact basenames collide case-insensitively: %r and %r"
                % (folded_names[folded], name)
            )
        folded_names[folded] = name
        if type(raw_hash) is not str or _LOWER_SHA256_RE.fullmatch(raw_hash) is None:
            raise AttrCheckpointError("artifact SHA-256 is invalid: %s" % name)
        hashes[name] = cast(str, raw_hash)

    if set(raw_sizes) != set(hashes):
        missing = ",".join(sorted(set(hashes) - set(raw_sizes))) or "-"
        unknown = ",".join(sorted(set(raw_sizes) - set(hashes))) or "-"
        raise AttrCheckpointError(
            "artifact_sizes keys differ from artifacts (missing=%s; unknown=%s)"
            % (missing, unknown)
        )
    sizes = {
        name: _require_nonnegative_int(raw_sizes[name], "artifact size for %s" % name)
        for name in hashes
    }
    count = _require_nonnegative_int(manifest["artifact_count"], "artifact_count")
    if count != len(hashes):
        raise AttrCheckpointError(
            "artifact_count is %d but artifacts contains %d entries" % (count, len(hashes))
        )
    return hashes, sizes


def read_verified_attr_checkpoint(
    manifest_path: os.PathLike[str] | str = DEFAULT_MANIFEST_PATH,
) -> VerifiedAttrCheckpoint:
    """Read and fully verify one published Attr checkpoint."""

    raw_path = Path(manifest_path)
    path = Path(os.path.abspath(os.fspath(raw_path)))
    _assert_no_reparse_components(path, "top-level manifest")

    # This is the sole read of the publication pointer.  Every later decision
    # uses this immutable byte snapshot.
    manifest_bytes = _read_regular_file_once(path, "top-level manifest")
    manifest = _parse_manifest(manifest_bytes, path)
    format_value = _require_string(manifest, "format")
    if format_value in {MANIFEST_FORMAT, LEGACY_V3_MANIFEST_FORMAT}:
        _require_exact_fields(manifest, _MANIFEST_FIELDS)
    elif format_value == LEGACY_MANIFEST_FORMAT:
        _require_exact_fields(manifest, _LEGACY_MANIFEST_FIELDS)
    else:
        raise AttrCheckpointError("unsupported manifest format")
    generation_id = _require_lower_sha256(manifest, "generation_id")
    image_sha256 = _require_lower_sha256(manifest, "image_sha256")
    generator_sha256 = _require_lower_sha256(manifest, "generator_sha256")

    generator_snapshot = _require_string(manifest, "generator_snapshot")
    _validate_relative_posix_path(generator_snapshot, "generator_snapshot")
    expected_generator_snapshot = (
        ".pf_attr_generator_snapshots/%s/pf_rederive_attr_semantics.py"
        % generator_sha256
    )
    if generator_snapshot != expected_generator_snapshot:
        raise AttrCheckpointError(
            "generator_snapshot must be exactly %s" % expected_generator_snapshot
        )
    generator_snapshot_path = path.parent.joinpath(
        *PurePosixPath(generator_snapshot).parts
    )
    _assert_no_reparse_components(generator_snapshot_path, "generator snapshot")
    generator_snapshot_bytes = _read_regular_file_once(
        generator_snapshot_path, "generator snapshot"
    )
    actual_generator_sha256 = hashlib.sha256(generator_snapshot_bytes).hexdigest()
    if actual_generator_sha256 != generator_sha256:
        raise AttrCheckpointError(
            "generator snapshot SHA-256 mismatch (expected %s; actual %s)"
            % (generator_sha256, actual_generator_sha256)
        )

    artifact_root_relative = _require_string(manifest, "artifact_root")
    expected_artifact_root = ".pf_attr_generations/%s" % generation_id
    if artifact_root_relative != expected_artifact_root:
        raise AttrCheckpointError(
            "artifact_root must be exactly %s" % expected_artifact_root
        )

    if _require_string(manifest, "authoritative_reader") != AUTHORITATIVE_READER:
        raise AttrCheckpointError(
            "authoritative_reader must be exactly %s" % AUTHORITATIVE_READER
        )
    if format_value in {MANIFEST_FORMAT, LEGACY_V3_MANIFEST_FORMAT}:
        authoritative_reader_sha256 = _require_lower_sha256(
            manifest, "authoritative_reader_sha256"
        )
        if format_value == MANIFEST_FORMAT:
            _assert_no_reparse_components(READER_PATH, "authoritative reader")
            reader_bytes = _read_regular_file_once(READER_PATH, "authoritative reader")
            actual_reader_sha256 = hashlib.sha256(reader_bytes).hexdigest()
            if actual_reader_sha256 != authoritative_reader_sha256:
                raise AttrCheckpointError(
                    "authoritative reader SHA-256 mismatch (expected %s; actual %s)"
                    % (authoritative_reader_sha256, actual_reader_sha256)
                )
        elif authoritative_reader_sha256 not in LEGACY_V3_READER_SHA256_ALLOWLIST:
            raise AttrCheckpointError(
                "legacy V3 authoritative_reader_sha256 is not an approved historical pin"
            )
    else:
        authoritative_reader_sha256 = "UNPINNED_LEGACY_V2"
    if manifest["compatibility_mirrors_authoritative"] is not False:
        raise AttrCheckpointError("compatibility_mirrors_authoritative must be false")
    publication_rule = _require_string(manifest, "publication_rule")
    if publication_rule != PUBLICATION_RULE:
        raise AttrCheckpointError(
            "publication_rule must be exactly the pinned checkpoint publication rule"
        )

    artifact_hashes, artifact_sizes = _validate_artifact_maps(manifest)
    artifact_count = cast(int, manifest["artifact_count"])
    generation_label = {
        MANIFEST_FORMAT: "PF_ATTR_GENERATION_V4",
        LEGACY_V3_MANIFEST_FORMAT: "PF_ATTR_GENERATION_V3",
        LEGACY_MANIFEST_FORMAT: "PF_ATTR_GENERATION_V2",
    }[format_value]
    generation_parts: list[object] = [
        generation_label, image_sha256, generator_sha256,
    ]
    if format_value in {MANIFEST_FORMAT, LEGACY_V3_MANIFEST_FORMAT}:
        generation_parts.append(authoritative_reader_sha256)
    if format_value == MANIFEST_FORMAT:
        generation_parts.append("publication_rule=%s" % publication_rule)
    generation_parts.extend(
        "%s=%s" % item for item in sorted(artifact_hashes.items())
    )
    computed_generation_id = _stable_key(*generation_parts)
    if computed_generation_id != generation_id:
        raise AttrCheckpointError(
            "generation_id mismatch (expected %s; computed %s)"
            % (generation_id, computed_generation_id)
        )

    artifact_root = path.parent.joinpath(*PurePosixPath(artifact_root_relative).parts)
    _assert_no_reparse_components(artifact_root, "artifact_root")
    try:
        if artifact_root.is_symlink():
            raise AttrCheckpointError(
                "artifact_root must not be a symbolic link: %s" % artifact_root
            )
        if not artifact_root.is_dir():
            raise AttrCheckpointError(
                "artifact_root is not a directory: %s" % artifact_root
            )
        members = list(artifact_root.iterdir())
    except AttrCheckpointError:
        raise
    except OSError as exc:
        raise AttrCheckpointError(
            "cannot inspect artifact_root %s: %s" % (artifact_root, exc)
        ) from exc
    expected_members = set(artifact_hashes) | {INTERNAL_MANIFEST_NAME}
    actual_members = {member.name for member in members}
    if actual_members != expected_members:
        missing = ",".join(sorted(expected_members - actual_members)) or "-"
        unknown = ",".join(sorted(actual_members - expected_members)) or "-"
        raise AttrCheckpointError(
            "artifact_root member set mismatch (missing=%s; unknown=%s)"
            % (missing, unknown)
        )

    internal_path = artifact_root / INTERNAL_MANIFEST_NAME
    _assert_no_reparse_components(internal_path, "internal manifest")
    internal_bytes = _read_regular_file_once(internal_path, "internal manifest")
    if internal_bytes != manifest_bytes:
        raise AttrCheckpointError(
            "internal manifest bytes differ from the top-level manifest"
        )

    verified_payloads: dict[str, bytes] = {}
    for name in sorted(artifact_hashes):
        artifact_path = artifact_root / name
        _assert_no_reparse_components(artifact_path, "artifact %s" % name)
        payload = _read_regular_file_once(artifact_path, "artifact %s" % name)
        actual_size = len(payload)
        if actual_size != artifact_sizes[name]:
            raise AttrCheckpointError(
                "artifact size mismatch for %s (expected %d; actual %d)"
                % (name, artifact_sizes[name], actual_size)
            )
        actual_hash = hashlib.sha256(payload).hexdigest()
        if actual_hash != artifact_hashes[name]:
            raise AttrCheckpointError(
                "artifact SHA-256 mismatch for %s (expected %s; actual %s)"
                % (name, artifact_hashes[name], actual_hash)
            )
        verified_payloads[name] = payload

    frozen_manifest = _immutable_mapping(manifest)
    frozen_hashes = cast(Mapping[str, str], frozen_manifest["artifacts"])
    frozen_sizes = cast(Mapping[str, int], frozen_manifest["artifact_sizes"])
    return VerifiedAttrCheckpoint(
        manifest_path=path,
        artifact_root=artifact_root,
        artifact_root_relative=artifact_root_relative,
        format=format_value,
        generation_id=generation_id,
        image_sha256=image_sha256,
        generator_sha256=generator_sha256,
        generator_snapshot=generator_snapshot,
        generator_snapshot_path=generator_snapshot_path,
        artifact_count=artifact_count,
        artifact_hashes=frozen_hashes,
        artifact_sizes=frozen_sizes,
        authoritative_reader=AUTHORITATIVE_READER,
        authoritative_reader_sha256=authoritative_reader_sha256,
        compatibility_mirrors_authoritative=False,
        publication_rule=publication_rule,
        manifest=frozen_manifest,
        manifest_bytes=manifest_bytes,
        generator_snapshot_bytes=generator_snapshot_bytes,
        artifact_bytes=MappingProxyType(dict(verified_payloads)),
    )


def load_verified_attr_checkpoint(
    manifest_path: os.PathLike[str] | str = DEFAULT_MANIFEST_PATH,
) -> VerifiedAttrCheckpoint:
    """Compatibility spelling for :func:`read_verified_attr_checkpoint`."""

    return read_verified_attr_checkpoint(manifest_path)


def verify_attr_checkpoint(
    manifest_path: os.PathLike[str] | str = DEFAULT_MANIFEST_PATH,
) -> VerifiedAttrCheckpoint:
    """Verify and return a checkpoint; alias with an imperative name."""

    return read_verified_attr_checkpoint(manifest_path)


def _build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Verify a PF_ATTR_GENERATION_MANIFEST_V2/V3/V4 checkpoint and all of its "
            "content-addressed verified artifacts."
        )
    )
    parser.add_argument(
        "manifest",
        nargs="?",
        default=str(DEFAULT_MANIFEST_PATH),
        help="top-level manifest path (default: %(default)s)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_argument_parser().parse_args(argv)
    try:
        checkpoint = read_verified_attr_checkpoint(args.manifest)
    except AttrCheckpointError as exc:
        print("checkpoint verification failed: %s" % exc, file=sys.stderr)
        return 1
    print("generation_id=%s" % checkpoint.generation_id)
    print("artifact_count=%d" % checkpoint.artifact_count)
    return 0


__all__ = [
    "AUTHORITATIVE_READER",
    "AttrCheckpointError",
    "DEFAULT_MANIFEST_PATH",
    "LEGACY_MANIFEST_FORMAT",
    "LEGACY_V3_MANIFEST_FORMAT",
    "LEGACY_V3_READER_SHA256_ALLOWLIST",
    "MANIFEST_FORMAT",
    "PUBLICATION_RULE",
    "VerifiedAttrCheckpoint",
    "load_verified_attr_checkpoint",
    "read_verified_attr_checkpoint",
    "verify_attr_checkpoint",
]


if __name__ == "__main__":
    raise SystemExit(main())
